#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nova-revisao.py

Monta a página de revisão de um projeto e sobe o servidor local.

O que ele faz, nesta ordem:

1. acha a raiz do pacote (a pasta que tem o setup.json) subindo a partir deste arquivo
2. acha a pasta do projeto que você pediu, dentro de projetos/
3. varre as pastas corte-NN, que na árvore de hoje têm só o MP4 de entrega
4. mede cada vídeo com o ffprobe e lê o brief.md, que mora em
   materiais-de-trabalho/corte-NN/brief.md (e, em projeto antigo, dentro da própria
   pasta do corte)
5. escreve projetos/<video>/revisao/revisao.json e copia o modelo.html para revisao.html
6. sobe um servidor na pasta do projeto e imprime o endereço

O script preenche o que dá para medir. Os campos de julgamento (título, gancho, por que,
decisões em aberto) ele deixa vazios de propósito: quem escreve é o agente que produziu os
cortes, editando o revisao.json antes de chamar a pessoa. Rodar o script de novo NÃO apaga
esses textos, a não ser que você peça com --refazer.

Uso:

    flow-reels produzir/nova-revisao projetos/2026-09-14-cafe-em-casa
    flow-reels produzir/nova-revisao cafe-em-casa --lote "Café em casa | primeiro lote"
    flow-reels produzir/nova-revisao cafe-em-casa --porta 8791
    flow-reels produzir/nova-revisao cafe-em-casa --sem-servidor
"""

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import unicodedata
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

PORTA_PADRAO = 8790
AQUI = Path(__file__).resolve().parent
MODELO = AQUI / "modelo.html"

# O teto de tudo que é material de trabalho dentro da pasta do vídeo. A pasta de
# cada corte guarda só o MP4 de entrega; brief, painel, face e legenda moram aqui.
PASTA_TRABALHO = "materiais-de-trabalho"


# ---------------------------------------------------------------- utilidades


def fala(texto=""):
    """Imprime sem quebrar em terminal que não aceita acento."""
    try:
        print(texto)
    except UnicodeEncodeError:
        print(texto.encode("ascii", "replace").decode("ascii"))


def erro(texto):
    fala("")
    fala("  " + texto)
    fala("")


def achar_raiz_do_pacote():
    """A pasta de trabalho, quando ela já tem o setup.json."""
    raiz = fabrica.raiz()
    return raiz if (raiz / "setup.json").is_file() else None


def ler_setup(raiz):
    caminho = raiz / "setup.json"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        erro("Não consegui ler o setup.json (%s). Sigo com os valores padrão." % e)
        return {}


def apelido(texto):
    """Transforma um nome em algo seguro para usar como chave."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = texto.encode("ascii", "ignore").decode("ascii").lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto).strip("-")
    return texto or "revisao"


# ------------------------------------------------------------------- ffprobe


def tem_ffprobe():
    return shutil.which("ffprobe") is not None


def medir_video(caminho):
    """Devolve duração, largura, altura e taxa de quadros. Campos podem vir vazios."""
    medida = {"duracao": None, "largura": None, "altura": None, "fps": None}
    if not tem_ffprobe():
        return medida
    comando = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate:format=duration",
        "-of", "json", str(caminho),
    ]
    try:
        bruto = subprocess.run(comando, capture_output=True, text=True, timeout=60)
        dados = json.loads(bruto.stdout or "{}")
    except Exception:
        return medida

    fluxos = dados.get("streams") or [{}]
    fluxo = fluxos[0]
    medida["largura"] = fluxo.get("width")
    medida["altura"] = fluxo.get("height")

    taxa = fluxo.get("r_frame_rate") or ""
    if "/" in taxa:
        try:
            a, b = taxa.split("/")
            if float(b) != 0:
                medida["fps"] = round(float(a) / float(b), 2)
        except Exception:
            pass

    try:
        medida["duracao"] = round(float((dados.get("format") or {}).get("duration")), 2)
    except Exception:
        pass

    return medida


# --------------------------------------------------------------- leitura do brief


def parece_placeholder(texto):
    """O modelo de brief usa <assim> nos campos não preenchidos."""
    t = (texto or "").strip()
    return (not t) or (t.startswith("<") and t.endswith(">"))


def achar_brief(pasta_corte):
    """O brief.md daquele corte, onde quer que ele esteja.

    Na árvore de hoje a pasta do corte guarda só o MP4 de entrega, e o brief é
    material de trabalho: ele mora em materiais-de-trabalho/corte-NN/brief.md.
    Projeto feito antes da mudança tem o brief dentro da própria pasta do corte,
    e esses dois lugares são os únicos que este script procura.
    """
    projeto = pasta_corte.parent
    candidatos = [
        projeto / PASTA_TRABALHO / pasta_corte.name / "brief.md",
        pasta_corte / "brief.md",
    ]
    for candidato in candidatos:
        if candidato.is_file():
            return candidato
    return None


def ler_brief(pasta_corte):
    """Puxa do brief.md só o que é inequívoco: o título e o texto do gancho."""
    achado = {"titulo": "", "gancho": ""}
    brief = achar_brief(pasta_corte)
    if brief is None:
        return achado
    try:
        texto = brief.read_text(encoding="utf-8")
    except Exception:
        return achado

    cabecalho = re.search(r"^#\s*Corte\s*[^:\n]*:\s*(.+)$", texto, re.MULTILINE | re.IGNORECASE)
    if cabecalho and not parece_placeholder(cabecalho.group(1)):
        achado["titulo"] = cabecalho.group(1).strip()

    secao = re.search(r"##\s*1\.\s*Gancho(.+?)(?=\n##\s|\Z)", texto, re.DOTALL | re.IGNORECASE)
    if secao:
        citacoes = re.findall(r"^\s*>\s?(.*)$", secao.group(1), re.MULTILINE)
        frase = " ".join(c.strip() for c in citacoes if c.strip()).strip()
        if not parece_placeholder(frase):
            achado["gancho"] = frase

    return achado


# ------------------------------------------------------------- varredura dos cortes


def video_do_corte(pasta):
    """O vídeo pronto daquela pasta. Prefere o que tem o nome da pasta."""
    preferido = pasta / (pasta.name + ".mp4")
    if preferido.is_file():
        return preferido
    candidatos = [
        p for p in sorted(pasta.glob("*.mp4"))
        if not p.name.startswith("_") and "parcial" not in p.name.lower()
    ]
    if not candidatos:
        return None
    return max(candidatos, key=lambda p: p.stat().st_mtime)


def varrer(projeto):
    """Lista os cortes prontos, em ordem de nome."""
    pastas = sorted(p for p in projeto.glob("corte-*") if p.is_dir())
    encontrados = []
    sem_video = []
    for pasta in pastas:
        video = video_do_corte(pasta)
        if video is None:
            sem_video.append(pasta.name)
        else:
            encontrados.append((pasta, video))
    return encontrados, sem_video


# ------------------------------------------------------------------ montagem do json


def bloco_anterior(anterior, ident):
    for bloco in anterior.get("cortes", []):
        if bloco.get("id") == ident:
            return bloco
    return {}


def montar_json(projeto, lote, achados, anterior, refazer):
    cortes = []
    for pasta, video in achados:
        ident = pasta.name
        velho = {} if refazer else bloco_anterior(anterior, ident)
        medida = medir_video(video)
        brief = ler_brief(pasta)

        ficha = {}
        if medida["largura"] and medida["altura"]:
            formato = "%sx%s" % (medida["largura"], medida["altura"])
            if medida["fps"]:
                formato += " · %g fps" % medida["fps"]
            ficha["formato"] = formato
        ficha["arquivo"] = video.name

        for chave, valor in (velho.get("ficha") or {}).items():
            if chave not in ficha:
                ficha[chave] = valor

        cortes.append({
            "id": ident,
            "titulo": velho.get("titulo") or brief["titulo"] or "",
            "arquivo": "../%s/%s" % (pasta.name, video.name),
            "duracao_s": medida["duracao"] if medida["duracao"] else velho.get("duracao_s", 0),
            "gancho": velho.get("gancho") or brief["gancho"] or "",
            "porque": velho.get("porque", ""),
            "decisoes": velho.get("decisoes", []),
            "ficha": ficha,
        })

    return {
        "_nota": (
            "Gerado por nova-revisao.py. Os campos titulo, gancho, porque e decisoes são de "
            "julgamento: quem escreve é o agente que produziu os cortes, antes de chamar a "
            "pessoa. O formato está documentado em exemplo.revisao.json, dentro da skill."
        ),
        "versao": "1.0",
        "chave": anterior.get("chave") or apelido(projeto.name),
        "lote": lote,
        "video": projeto.name,
        "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "introducao": anterior.get("introducao", ""),
        "cortes": cortes,
    }


def campos_vazios(revisao):
    faltando = []
    for bloco in revisao["cortes"]:
        pendentes = [c for c in ("titulo", "gancho", "porque") if not bloco.get(c)]
        if not bloco.get("decisoes"):
            pendentes.append("decisoes")
        if pendentes:
            faltando.append((bloco["id"], pendentes))
    return faltando


# ---------------------------------------------------------------------- servidor


class Entregador(SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler com suporte a Range, que é o que deixa o vídeo buscar."""

    def log_message(self, formato, *args):
        pass

    def do_GET(self):
        # A raiz servida e a pasta do video, e quem digita so localhost:porta
        # caia numa listagem de arquivo. O redirecionamento resolve isso aqui
        # dentro, em vez de escrever um index.html na pasta do video: a pasta
        # do video mostra o que interessa, e nada de sujeira de servidor.
        if self.path in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/revisao/revisao.html")
            self.end_headers()
            return

        faixa = self.headers.get("Range")
        if not faixa:
            return SimpleHTTPRequestHandler.do_GET(self)

        caminho = self.translate_path(self.path)
        if not os.path.isfile(caminho):
            return SimpleHTTPRequestHandler.do_GET(self)

        casado = re.match(r"bytes=(\d*)-(\d*)", faixa.strip())
        if not casado:
            return SimpleHTTPRequestHandler.do_GET(self)

        tamanho = os.path.getsize(caminho)
        inicio_txt, fim_txt = casado.groups()
        if inicio_txt == "":
            comprimento = int(fim_txt or 0)
            inicio = max(0, tamanho - comprimento)
            fim = tamanho - 1
        else:
            inicio = int(inicio_txt)
            fim = int(fim_txt) if fim_txt else tamanho - 1
        fim = min(fim, tamanho - 1)

        if inicio > fim or inicio >= tamanho:
            self.send_response(416)
            self.send_header("Content-Range", "bytes */%d" % tamanho)
            self.end_headers()
            return

        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(caminho))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", "bytes %d-%d/%d" % (inicio, fim, tamanho))
        self.send_header("Content-Length", str(fim - inicio + 1))
        self.end_headers()

        restante = fim - inicio + 1
        with open(caminho, "rb") as f:
            f.seek(inicio)
            while restante > 0:
                pedaco = f.read(min(64 * 1024, restante))
                if not pedaco:
                    break
                try:
                    self.wfile.write(pedaco)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                    return
                restante -= len(pedaco)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        SimpleHTTPRequestHandler.end_headers(self)


class Servidor(ThreadingHTTPServer):
    """O servidor da revisão, com a porta exclusiva.

    O `allow_reuse_address` do http.server é ligado por padrão, e no Windows ele
    não significa "reaproveitar porta em TIME_WAIT" como no Linux: ele significa
    dividir a porta com quem já está lá. O resultado é dois servidores ouvindo em
    8790 ao mesmo tempo, com o mais velho respondendo, e a pessoa vendo a revisão
    do lote passado enquanto jura que gerou de novo. Aqui a porta é exclusiva:
    ocupada é ocupada, e o script sobe na próxima.
    """

    allow_reuse_address = False
    daemon_threads = True


def esta_ocupada(porta):
    """True quando já existe alguém ouvindo nesta porta.

    Duas conferências, porque uma só engana. O connect acha quem está ouvindo
    agora; o bind, sem nenhum reuso, acha o resto.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        if s.connect_ex(("127.0.0.1", porta)) == 0:
            return True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", porta))
        except OSError:
            return True
    return False


def porta_livre(porta, tentativas=12):
    for tentativa in range(tentativas):
        alvo = porta + tentativa
        if not esta_ocupada(alvo):
            return alvo
    return None


def servir(pasta, porta):
    alvo = porta_livre(porta)
    if alvo is None:
        erro("Nenhuma porta livre entre %d e %d. Feche a revisão anterior e tente de novo."
             % (porta, porta + 11))
        return 1
    if alvo != porta:
        fala("  A porta %d estava ocupada, subi na %d." % (porta, alvo))

    endereco = "http://localhost:%d/revisao/revisao.html" % alvo
    fala("")
    fala("  Revisão no ar. Qualquer um dos dois abre:")
    fala("  http://localhost:%d" % alvo)
    fala("  " + endereco)
    fala("")
    fala("  Deixe esta janela aberta enquanto revisa. Ctrl+C encerra.")
    fala("")

    # Projeto feito antes desta versao ganhou um index.html de redirecionamento
    # dentro da pasta do video. Ele nao e mais necessario, porque o servidor
    # redireciona sozinho, e ele e exatamente o tipo de arquivo que polui a
    # pasta que a pessoa abre. Entao ele sai.
    indice_velho = pasta / "index.html"
    if indice_velho.is_file() and "revisao/revisao.html" in indice_velho.read_text(
            encoding="utf-8", errors="ignore"):
        try:
            indice_velho.unlink()
        except OSError:
            pass

    try:
        servidor = Servidor(("127.0.0.1", alvo), partial(Entregador, directory=str(pasta)))
    except OSError as falha:
        erro("a porta %d foi ocupada entre a conferência e a subida (%s). Tente de novo."
             % (alvo, falha))
        return 1
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        fala("")
        fala("  Servidor encerrado. As respostas continuam salvas no navegador.")
    finally:
        servidor.server_close()
    return 0


# -------------------------------------------------------------------- argumentos


def ajuda(raiz):
    fala("")
    fala("  nova-revisao.py | monta a página de revisão de um projeto e sobe o servidor.")
    fala("")
    fala("  Uso:")
    fala("    flow-reels produzir/nova-revisao <pasta do projeto> [opções]")
    fala("")
    fala("  Opções:")
    fala("    --lote \"Nome\"    título que aparece no cabeçalho da página")
    fala("    --porta 8790      porta do servidor (o padrão vem do setup.json)")
    fala("    --sem-servidor    só gera os arquivos, não sobe nada")
    fala("    --refazer         descarta os textos já escritos no revisao.json anterior")
    fala("")
    if raiz is not None:
        pasta_projetos = raiz / "projetos"
        existentes = sorted(p.name for p in pasta_projetos.glob("*") if p.is_dir()) if pasta_projetos.is_dir() else []
        if existentes:
            fala("  Projetos que existem hoje:")
            for nome in existentes:
                fala("    " + nome)
        else:
            fala("  A pasta projetos/ ainda está vazia. Produza um corte antes de revisar.")
        fala("")


def resolver_projeto(raiz, pedido):
    alvo = Path(pedido)
    candidatos = [alvo, Path.cwd() / alvo, raiz / alvo, raiz / "projetos" / alvo]
    for caminho in candidatos:
        try:
            if caminho.is_dir():
                return caminho.resolve()
        except OSError:
            continue
    return None


def main(argumentos):
    raiz = achar_raiz_do_pacote()
    if raiz is None:
        erro("Não achei o setup.json subindo a partir deste script. Rode a partir de dentro do pacote.")
        return 1

    if not argumentos or argumentos[0] in ("-h", "--help", "ajuda"):
        ajuda(raiz)
        return 0

    pedido = argumentos[0]
    lote = None
    porta = None
    sem_servidor = False
    refazer = False

    resto = argumentos[1:]
    i = 0
    while i < len(resto):
        opcao = resto[i]
        if opcao == "--lote" and i + 1 < len(resto):
            lote = resto[i + 1]
            i += 2
        elif opcao == "--porta" and i + 1 < len(resto):
            try:
                porta = int(resto[i + 1])
            except ValueError:
                erro("A porta precisa ser um número. Recebi: %s" % resto[i + 1])
                return 1
            i += 2
        elif opcao == "--sem-servidor":
            sem_servidor = True
            i += 1
        elif opcao == "--refazer":
            refazer = True
            i += 1
        else:
            erro("Não reconheci a opção %s. Rode sem argumento para ver a ajuda." % opcao)
            return 1

    projeto = resolver_projeto(raiz, pedido)
    if projeto is None:
        erro("Não achei a pasta do projeto: %s" % pedido)
        ajuda(raiz)
        return 1

    if not MODELO.is_file():
        erro("Falta o modelo.html ao lado deste script. Sem ele não tem página.")
        return 1

    achados, sem_video = varrer(projeto)
    if not achados:
        erro("Nenhum corte pronto em %s." % projeto)
        fala("  Procurei um .mp4 dentro de cada pasta corte-NN e não encontrei nenhum.")
        if sem_video:
            fala("  Pastas sem vídeo: " + ", ".join(sem_video))
        fala("")
        return 1

    setup = ler_setup(raiz)
    if porta is None:
        try:
            porta = int(setup.get("porta_revisao", PORTA_PADRAO))
        except (TypeError, ValueError):
            porta = PORTA_PADRAO

    pasta_revisao = projeto / "revisao"
    pasta_revisao.mkdir(parents=True, exist_ok=True)
    destino_json = pasta_revisao / "revisao.json"

    anterior = {}
    if destino_json.is_file():
        try:
            with open(destino_json, "r", encoding="utf-8") as f:
                anterior = json.load(f)
        except Exception:
            anterior = {}

    if lote is None:
        lote = anterior.get("lote") or projeto.name

    revisao = montar_json(projeto, lote, achados, anterior, refazer)

    with open(destino_json, "w", encoding="utf-8") as f:
        json.dump(revisao, f, ensure_ascii=False, indent=2)
    shutil.copyfile(MODELO, pasta_revisao / "revisao.html")

    fala("")
    fala("  Lote: %s" % lote)
    fala("  Projeto: %s" % projeto)
    fala("  Cortes encontrados: %d" % len(revisao["cortes"]))
    for bloco in revisao["cortes"]:
        duracao = ("%.1f s" % bloco["duracao_s"]) if bloco["duracao_s"] else "duração não medida"
        fala("    %s | %s | %s" % (bloco["id"], duracao, bloco["arquivo"]))
    if sem_video:
        fala("  Pastas sem vídeo pronto (ficaram de fora): " + ", ".join(sem_video))
    if not tem_ffprobe():
        fala("  Aviso: ffprobe não encontrado, então as durações e o formato ficaram em branco.")

    faltando = campos_vazios(revisao)
    if faltando:
        fala("")
        fala("  Antes de chamar a pessoa, preencha no %s:" % destino_json.name)
        for ident, campos in faltando:
            fala("    %s | falta: %s" % (ident, ", ".join(campos)))
        fala("  Arquivo: %s" % destino_json)

    if sem_servidor:
        fala("")
        fala("  Arquivos prontos em %s. Servidor não subiu, porque você pediu --sem-servidor." % pasta_revisao)
        fala("")
        return 0

    return servir(projeto, porta)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main(sys.argv[1:]))
