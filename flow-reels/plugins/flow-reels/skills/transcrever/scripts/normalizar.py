# -*- coding: utf-8 -*-
"""Normalizador da transcricao: o contrato do pacote.

As duas rotas de transcricao (replicate.py e local.py) terminam aqui, e as duas
produzem exatamente os mesmos tres arquivos, sempre nos mesmos lugares dentro da
pasta do video:

    transcricao.md                                    legivel, fica a vista
    materiais-de-trabalho/transcricao/palavras.json   palavra a palavra, com tempo
    materiais-de-trabalho/transcricao/audio16k.wav    mono, 16 kHz, valida o corte

So o transcricao.md fica na raiz da pasta do video, porque e o unico dos tres que
uma pessoa abre para ler. Os outros dois sao material de trabalho e moram debaixo
do teto de materiais-de-trabalho/, junto com a resposta crua da API. Quem precisa
achar um deles chama achar_palavras() ou achar_audio(), que sabem procurar tambem
no lugar antigo, na raiz, para nao quebrar projeto feito antes desta mudanca.

FORMATO DO palavras.json (contrato com o `/flow-reels:planejar` e com o legenda.py,
nao mude sem avisar as duas pontas):

    {
      "palavras": [
        {"inicio": 0.59, "fim": 0.71, "texto": "Bom"},
        {"inicio": 0.71, "fim": 1.04, "texto": "gente"}
      ],
      "meta": {
        "fonte": "minha-aula.mp4",
        "video": "materiais-de-trabalho/fonte/minha-aula.mp4",
        "audio": "materiais-de-trabalho/transcricao/audio16k.wav",
        "duracao": 763.42,
        "idioma": "pt",
        "motor": "whisperx large-v3 via replicate (align_output)",
        "alinhado": true,
        "palavras": 1834,
        "gerado_em": "2026-09-18T22:40:11"
      }
    }

Regras do formato, todas obrigatorias:

1. Tres chaves por palavra e mais nenhuma: inicio, fim, texto. Tudo em portugues.
2. inicio e fim sao segundos em ponto flutuante, contados do inicio do audio.
3. A lista vem em ordem crescente de inicio, sem palavra vazia e sem buraco.
4. fim e sempre maior ou igual a inicio.
5. texto vem sem espaco nas pontas e mantem a pontuacao colada na palavra.
6. "alinhado": true significa que os tempos vieram de alinhamento forcado e servem
   para cortar. Se for false, os tempos sao aproximados e o corte precisa ser
   conferido na energia do audio antes de virar entrega.

Este modulo usa so a biblioteca padrao de proposito, porque o local.py roda dentro
de um ambiente isolado do uv e importa daqui.

Uso direto, quando voce ja tem a saida bruta salva em disco:

    flow-reels transcrever/normalizar --projeto projetos/minha-aula \
        --bruto projetos/minha-aula/materiais-de-trabalho/transcricao/bruto-replicate.json
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

try:  # console do Windows costuma vir em cp1252 e engasga com acento
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


PAUSA_DE_FRASE = 0.65      # segundos de silencio que ja quebram frase
MAX_CHARS_FRASE = 160      # tamanho maximo de uma linha do transcricao.md
FIM_DE_FRASE = ".!?...:;"

# ------------------------------------------------- a arvore da pasta do video
#
# Quem abre projetos/<video>/ precisa ver o que interessa: os cortes prontos, a
# transcricao legivel, os ganchos e a pagina de revisao. Todo o resto e material
# de trabalho e mora debaixo de um teto so. Estas funcoes sao a unica definicao
# desses caminhos no pacote inteiro: mudou aqui, mudou em todo mundo.

NOME_TRABALHO = "materiais-de-trabalho"


def pasta_trabalho(projeto):
    """<projeto>/materiais-de-trabalho, o teto de tudo que a pessoa nao precisa ver."""
    return Path(projeto) / NOME_TRABALHO


def pasta_transcricao(projeto):
    """Onde caem palavras.json, audio16k.wav e a resposta crua da transcricao."""
    return pasta_trabalho(projeto) / "transcricao"


def pasta_fonte(projeto):
    """Onde cai o video de origem, baixado ou copiado."""
    return pasta_trabalho(projeto) / "fonte"


def _procurar(projeto, nome):
    """Devolve o arquivo no lugar de hoje, ou no lugar antigo, ou None.

    O lugar antigo e a raiz da pasta do video, que foi onde os tres arquivos
    moraram ate a arvore ganhar o materiais-de-trabalho/. Projeto velho continua
    funcionando sem ninguem ter que mover arquivo na mao.
    """
    projeto = Path(projeto)
    for candidato in (pasta_transcricao(projeto) / nome, projeto / nome):
        if candidato.is_file():
            return candidato
    return None


def achar_palavras(projeto):
    """O palavras.json daquele video, onde quer que ele esteja. None se nao houver."""
    return _procurar(projeto, "palavras.json")


def achar_audio(projeto):
    """O audio16k.wav daquele video, onde quer que ele esteja. None se nao houver."""
    return _procurar(projeto, "audio16k.wav")


# ---------------------------------------------------------------- utilidades

def aviso(msg):
    print("  " + str(msg), file=sys.stderr)


def erro(msg, codigo=1):
    print("\nERRO: " + str(msg) + "\n", file=sys.stderr)
    sys.exit(codigo)


def slug(texto, tamanho=60):
    """Nome de pasta seguro, sem acento e sem espaco."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = texto.encode("ascii", "ignore").decode("ascii").lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto).strip("-")
    return (texto[:tamanho].rstrip("-")) or "video"


def mmss(segundos):
    segundos = max(0.0, float(segundos or 0))
    m, s = divmod(int(round(segundos)), 60)
    h, m = divmod(m, 60)
    if h:
        return "%d:%02d:%02d" % (h, m, s)
    return "%02d:%02d" % (m, s)


def achar(programa):
    return shutil.which(programa)


# ------------------------------------------------- leitura da saida bruta

def extrair_palavras(dados):
    """Aceita as formas que o WhisperX devolve e sai sempre com a nossa.

    Formas aceitas:
      {"segments": [{"words": [{"word","start","end"}]}]}   <- whisperx alinhado
      {"segments": [{"start","end","text"}]}                <- sem alinhamento
      {"words":    [{"word","start","end"}]}                <- ja achatado
      {"palavras": [{"inicio","fim","texto"}]}              <- ja no nosso formato
      [ ... ]                                               <- lista solta
    """
    if isinstance(dados, list):
        bruto = dados
    elif isinstance(dados, dict):
        if dados.get("palavras"):
            bruto = dados["palavras"]
        elif dados.get("words"):
            bruto = dados["words"]
        elif dados.get("segments"):
            bruto = []
            tem_palavra = False
            for seg in dados["segments"]:
                if seg.get("words"):
                    tem_palavra = True
                    bruto.extend(seg["words"])
            if not tem_palavra:
                # sem alinhamento: cada trecho vira uma entrada longa. o meta
                # marca alinhado=false e o corte precisa de conferencia.
                bruto = list(dados["segments"])
        else:
            bruto = []
    else:
        bruto = []

    palavras = []
    for item in bruto:
        if not isinstance(item, dict):
            continue
        texto = item.get("texto", item.get("word", item.get("text", "")))
        texto = re.sub(r"\s+", " ", str(texto)).strip()
        if not texto:
            continue
        inicio = item.get("inicio", item.get("start"))
        fim = item.get("fim", item.get("end"))
        palavras.append({
            "inicio": None if inicio is None else float(inicio),
            "fim": None if fim is None else float(fim),
            "texto": texto,
        })
    return palavras


def alinhado_de_verdade(dados):
    """Diz se a saida trouxe tempo por palavra ou so por trecho."""
    if isinstance(dados, dict) and dados.get("segments"):
        return any(seg.get("words") for seg in dados["segments"])
    if isinstance(dados, dict) and (dados.get("words") or dados.get("palavras")):
        return True
    if isinstance(dados, list):
        return True
    return False


# ------------------------------------------------------------- saneamento

def costurar_tempos(palavras):
    """Preenche tempo faltando e conserta ordem quebrada.

    O WhisperX deixa numeral, sigla e simbolo sem tempo de vez em quando. Uma
    palavra sem tempo no meio derruba o corte, entao ela herda o vizinho e, se a
    lacuna tiver varias palavras seguidas, o intervalo e repartido em partes
    iguais entre elas.
    """
    if not palavras:
        return palavras, []

    problemas = []

    primeiro = next((p for p in palavras if p["inicio"] is not None), None)
    ultimo = next((p for p in reversed(palavras) if p["fim"] is not None), None)
    if primeiro is None or ultimo is None:
        problemas.append("nenhuma palavra veio com tempo, esta transcricao nao serve para cortar")
        base = 0.0
        for p in palavras:
            p["inicio"], p["fim"] = base, base + 0.3
            base += 0.3
        return palavras, problemas

    if palavras[0]["inicio"] is None:
        palavras[0]["inicio"] = max(0.0, float(primeiro["inicio"]))
    if palavras[-1]["fim"] is None:
        palavras[-1]["fim"] = float(ultimo["fim"])

    i = 0
    n = len(palavras)
    while i < n:
        if palavras[i]["inicio"] is not None and palavras[i]["fim"] is not None:
            i += 1
            continue

        j = i
        while j < n and (palavras[j]["inicio"] is None or palavras[j]["fim"] is None):
            j += 1

        antes = palavras[i - 1]["fim"] if i > 0 and palavras[i - 1]["fim"] is not None else 0.0
        if j < n and palavras[j]["inicio"] is not None:
            depois = palavras[j]["inicio"]
        else:
            depois = antes + 0.3 * (j - i)
        if depois < antes:
            depois = antes + 0.3 * (j - i)

        quantidade = j - i
        passo = (depois - antes) / quantidade if quantidade else 0.0
        for k in range(quantidade):
            p = palavras[i + k]
            if p["inicio"] is None:
                p["inicio"] = antes + passo * k
            if p["fim"] is None:
                p["fim"] = antes + passo * (k + 1)
        problemas.append(
            "%d palavra(s) sem tempo perto de %s, tempo estimado pelo vizinho"
            % (quantidade, mmss(antes))
        )
        i = j

    anterior = 0.0
    for p in palavras:
        p["inicio"] = round(max(0.0, float(p["inicio"])), 3)
        p["fim"] = round(max(p["inicio"], float(p["fim"])), 3)
        if p["inicio"] < anterior:
            p["inicio"] = round(anterior, 3)
            if p["fim"] < p["inicio"]:
                p["fim"] = p["inicio"]
        anterior = p["fim"]

    return palavras, problemas


def validar(palavras):
    """Confere o contrato antes de gravar. Devolve a lista de defeitos."""
    defeitos = []
    if not palavras:
        return ["a lista de palavras saiu vazia"]

    anterior = -1.0
    for i, p in enumerate(palavras):
        if set(p.keys()) != {"inicio", "fim", "texto"}:
            defeitos.append("palavra %d tem chaves fora do contrato: %s" % (i, sorted(p.keys())))
            break
        if not isinstance(p["texto"], str) or not p["texto"].strip():
            defeitos.append("palavra %d esta sem texto" % i)
            break
        if p["fim"] < p["inicio"]:
            defeitos.append("palavra %d termina antes de comecar" % i)
            break
        if p["inicio"] < anterior - 0.001:
            defeitos.append("palavra %d comeca antes do fim da anterior" % i)
            break
        anterior = p["fim"]
    return defeitos


# ------------------------------------------------------------- agrupamento

def costurar_frases(palavras, pausa=PAUSA_DE_FRASE, max_chars=MAX_CHARS_FRASE):
    """Junta palavras em frases para o transcricao.md.

    Quebra quando a palavra termina em pontuacao forte, quando o silencio passa
    da pausa, ou quando a linha fica comprida demais para ler.
    """
    frases = []
    atual = []
    for i, p in enumerate(palavras):
        atual.append(p)
        texto_atual = " ".join(x["texto"] for x in atual)
        proximo = palavras[i + 1] if i + 1 < len(palavras) else None

        quebra = False
        if p["texto"][-1] in FIM_DE_FRASE:
            quebra = True
        elif proximo is not None and (proximo["inicio"] - p["fim"]) >= pausa:
            quebra = True
        elif len(texto_atual) >= max_chars:
            quebra = True
        elif proximo is None:
            quebra = True

        if quebra:
            frases.append({
                "inicio": atual[0]["inicio"],
                "fim": atual[-1]["fim"],
                "texto": texto_atual,
            })
            atual = []

    if atual:
        frases.append({
            "inicio": atual[0]["inicio"],
            "fim": atual[-1]["fim"],
            "texto": " ".join(x["texto"] for x in atual),
        })
    return frases


# ------------------------------------------------------------------ audio

def extrair_audio(video, destino):
    """Tira o audio em mono 16 kHz. E o arquivo que valida ponto de corte.

    Aceita caminho local ou URL que o ffmpeg consiga abrir. Devolve o caminho
    gravado, ou None quando nao deu (e ai o aviso ja foi impresso).
    """
    destino = Path(destino)
    if not achar("ffmpeg"):
        aviso("ffmpeg nao encontrado no PATH, o audio16k.wav nao foi gerado.")
        aviso("Instale o ffmpeg e rode de novo, ou o planejador nao consegue validar o corte.")
        return None

    destino.parent.mkdir(parents=True, exist_ok=True)
    comando = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(video),
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(destino),
    ]
    try:
        subprocess.run(comando, check=True)
    except subprocess.CalledProcessError as e:
        aviso("o ffmpeg falhou ao extrair o audio (codigo %s)." % e.returncode)
        return None
    return destino


def duracao_do_arquivo(caminho):
    """Duracao em segundos pelo ffprobe. Devolve None se nao der."""
    if not achar("ffprobe"):
        return None
    try:
        saida = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(caminho)],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return round(float(saida), 3)
    except Exception:
        return None


# ------------------------------------------------------------------ escrita

def caminho_relativo_ao_projeto(caminho, projeto):
    """O caminho visto de dentro da pasta do video, com barra normal.

    E assim que o meta guarda o audio e o video: relativo, para a pasta do
    projeto continuar valendo se ela for movida ou renomeada.
    """
    if not caminho:
        return None
    try:
        return Path(caminho).resolve().relative_to(Path(projeto).resolve()).as_posix()
    except ValueError:
        return str(caminho).replace("\\", "/")


def escrever_palavras_json(palavras, meta, destino):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    pacote = {"palavras": palavras, "meta": meta}
    destino.write_text(json.dumps(pacote, ensure_ascii=False, indent=1), encoding="utf-8")
    return destino


def escrever_transcricao_md(frases, meta, destino):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    linhas = ["# Transcrição", ""]
    linhas.append("- **fonte:** %s" % meta.get("fonte", "não informada"))
    if meta.get("duracao"):
        linhas.append("- **duração:** %s" % mmss(meta["duracao"]))
    linhas.append("- **idioma:** %s" % meta.get("idioma", "não informado"))
    linhas.append("- **motor:** %s" % meta.get("motor", "não informado"))
    linhas.append("- **palavras:** %s" % meta.get("palavras", 0))
    if not meta.get("alinhado", True):
        linhas.append("- **atenção:** os tempos são aproximados, não vieram de alinhamento por palavra")
    linhas.append("- **gerado em:** %s" % meta.get("gerado_em", ""))
    linhas.append("")
    linhas.append("---")
    linhas.append("")
    for f in frases:
        linhas.append("[%s] %s" % (mmss(f["inicio"]), f["texto"]))
        linhas.append("")

    destino.write_text("\n".join(linhas).rstrip() + "\n", encoding="utf-8")
    return destino


def normalizar(dados_brutos, projeto, meta_extra=None, video=None, gerar_audio=True):
    """O caminho unico. As duas rotas chamam esta funcao e nada mais.

    dados_brutos: o que a rota recebeu do WhisperX, em qualquer forma aceita.
    projeto:      diretorio do projeto, onde os tres arquivos vao cair.
    meta_extra:   o que a rota sabe e o normalizador nao (fonte, motor, idioma).
    video:        arquivo (ou URL) de onde tirar o audio16k.wav.
    """
    projeto = Path(projeto)
    projeto.mkdir(parents=True, exist_ok=True)
    destino_trabalho = pasta_transcricao(projeto)
    destino_trabalho.mkdir(parents=True, exist_ok=True)
    meta_extra = dict(meta_extra or {})

    palavras = extrair_palavras(dados_brutos)
    if not palavras:
        erro("a transcrição voltou sem nenhuma palavra. Confira o arquivo de saída bruta "
             "no diretório do projeto antes de gastar outra rodada.")

    palavras, remendos = costurar_tempos(palavras)
    for r in remendos:
        aviso("remendo: " + r)

    defeitos = validar(palavras)
    if defeitos:
        for d in defeitos:
            aviso("defeito: " + d)
        erro("o palavras.json não passou na validação do contrato e não foi gravado.")

    frases = costurar_frases(palavras)

    caminho_audio = None
    if gerar_audio and video:
        caminho_audio = extrair_audio(video, destino_trabalho / "audio16k.wav")

    duracao = None
    if video:
        duracao = duracao_do_arquivo(video)
    if duracao is None and palavras:
        duracao = palavras[-1]["fim"]

    meta = {
        "fonte": meta_extra.get("fonte", str(video) if video else "não informada"),
        "video": meta_extra.get("video", str(video) if video else None),
        "audio": caminho_relativo_ao_projeto(caminho_audio, projeto) if caminho_audio
                 else meta_extra.get("audio"),
        "duracao": duracao,
        "idioma": meta_extra.get("idioma", "pt"),
        "motor": meta_extra.get("motor", "não informado"),
        "alinhado": bool(meta_extra.get("alinhado", alinhado_de_verdade(dados_brutos))),
        "palavras": len(palavras),
        "frases": len(frases),
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
    }
    for chave, valor in meta_extra.items():
        meta.setdefault(chave, valor)

    p_json = escrever_palavras_json(palavras, meta, destino_trabalho / "palavras.json")
    p_md = escrever_transcricao_md(frases, meta, projeto / "transcricao.md")

    print("")
    print("Transcrição normalizada.")
    print("  palavras.json   %s   (%d palavras)" % (p_json, len(palavras)))
    print("  transcricao.md  %s   (%d frases)" % (p_md, len(frases)))
    if caminho_audio:
        print("  audio16k.wav    %s" % caminho_audio)
    else:
        print("  audio16k.wav    NÃO gerado. O planejador precisa dele para validar o corte.")
    if not meta["alinhado"]:
        print("")
        print("  Atenção: esta transcrição não tem tempo por palavra, só por trecho.")
        print("  Serve para ler e para escolher o gancho, mas todo ponto de corte")
        print("  precisa ser conferido na onda do áudio antes de virar entrega.")
    return {"palavras": p_json, "transcricao": p_md, "audio": caminho_audio, "meta": meta}


# ---------------------------------------------------------------------- cli

def main():
    parser = argparse.ArgumentParser(
        description="Normaliza uma saída bruta do WhisperX nos três arquivos do contrato.",
        epilog="Exemplo: flow-reels transcrever/normalizar "
               "--bruto projetos/minha-aula/materiais-de-trabalho/transcricao/bruto-replicate.json "
               "--projeto projetos/minha-aula "
               "--video projetos/minha-aula/materiais-de-trabalho/fonte/minha-aula.mp4",
    )
    parser.add_argument("--bruto", required=True, help="JSON com a saída crua da transcrição")
    parser.add_argument("--projeto", required=True, help="diretório do projeto, onde os três arquivos caem")
    parser.add_argument("--video", help="vídeo ou áudio de origem, para extrair o audio16k.wav")
    parser.add_argument("--idioma", default="pt", help="idioma da fala (padrão: pt)")
    parser.add_argument("--motor", default="não informado", help="quem transcreveu, vai no meta")
    parser.add_argument("--sem-audio", action="store_true", help="não extrair o audio16k.wav")

    if len(sys.argv) == 1:
        parser.print_help()
        print("\nEste script é o contrato da transcrição: ele grava palavras.json, "
              "transcricao.md e audio16k.wav.\nNormalmente quem chama é o replicate.py "
              "ou o local.py. Rodar direto só serve para reaproveitar uma saída bruta "
              "que você já tem em disco.\n")
        sys.exit(2)

    args = parser.parse_args()

    caminho = Path(args.bruto)
    if not caminho.exists():
        erro("não encontrei o arquivo de saída bruta: %s" % caminho)

    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        erro("o arquivo %s não é um JSON válido (%s)." % (caminho, e))

    normalizar(
        dados,
        projeto=args.projeto,
        meta_extra={"idioma": args.idioma, "motor": args.motor,
                    "fonte": args.video or str(caminho)},
        video=args.video,
        gerar_audio=not args.sem_audio,
    )


if __name__ == "__main__":
    main()
