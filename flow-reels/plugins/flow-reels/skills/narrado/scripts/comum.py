# -*- coding: utf-8 -*-
"""Pecas comuns do reel narrado.

Todo script desta pasta importa daqui: o leitor do .env, os caminhos da pasta do
reel, a leitura da marca, o audio pelo ffmpeg e a busca de palavra na fala.
Nada aqui chama API nenhuma.

A arvore do reel, que este arquivo materializa (a definicao inteira esta no
SKILL.md, secao "A pasta"):

    projetos/<nome>/
    |-- narrado-01/narrado-01.mp4            a entrega, e mais nada
    |-- revisao/                             a pagina de revisao do pacote
    `-- materiais-de-trabalho/
        |-- fonte/                           a filmagem de origem
        `-- narrado-01/
            |-- fatos.md, roteiro.md, roteiro-tts.txt, tomadas.json
            |-- voz/                         as tomadas de voz e os tempos por palavra
            |-- construcao/                  linha do tempo, imagem, legenda, mix
            `-- conferencia/                 folhas de contato e o relatorio de QA
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import wave
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

RAIZ = fabrica.raiz()        # a pasta de trabalho: projetos/, marca/, .env
PLUGIN = fabrica.plugin()    # o pacote: componentes, a marca de exemplo, as outras skills
AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parent

LARGURA, ALTURA, FPS = 1080, 1920, 30
SR = 48000

# Zonas reservadas do quadro final. Nada importante acima de y 150 (a interface da
# plataforma), a direita de x 980 (os botoes) nem abaixo de y 1700 (a legenda do post).
TOPO_RESERVADO = 150
DIREITA_RESERVADA = 980
BASE_RESERVADA = 1700
FAIXA_LEGENDA = (1480, 1660)
CENTRO_LEGENDA = 1572

TRAVESSOES = (chr(0x2014), chr(0x2013))


# ------------------------------------------------------------------- saida

def fala(texto=""):
    try:
        print(texto, flush=True)
    except UnicodeEncodeError:
        print(texto.encode("ascii", "replace").decode("ascii"), flush=True)


def aviso(texto):
    fala("aviso: " + texto)


def erro(texto, codigo=1):
    fala("")
    fala("erro: " + texto)
    fala("")
    sys.exit(codigo)


# ------------------------------------------------------------------- chave

def carregar_env(inicio=None):
    """Le o .env do pacote e joga o conteudo no ambiente.

    Procura na raiz do pacote e na pasta de onde o comando foi rodado, mais as pastas
    acima dela ATE a raiz do pacote. De proposito ele NAO sai do pacote subindo:
    credencial de terceiro, de um .env pessoal acima do pacote, nunca deve entrar numa
    chamada que estes scripts fazem.

    Nao sobrescreve variavel que ja existe no ambiente, porque quem exportou na mao
    tem prioridade sobre arquivo.
    """
    raiz = RAIZ
    atual = Path(inicio or Path.cwd()).resolve()
    candidatos = [raiz]
    if atual == raiz or raiz in atual.parents:
        candidatos.append(atual)
        candidatos += [p for p in atual.parents if raiz == p or raiz in p.parents]
    vistos = set()
    for pasta in candidatos:
        if pasta in vistos:
            continue
        vistos.add(pasta)
        arquivo = pasta / ".env"
        if not arquivo.exists():
            continue
        for linha in arquivo.read_text(encoding="utf-8", errors="ignore").splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            chave, valor = chave.strip(), valor.strip().strip('"').strip("'")
            if chave and valor and not os.environ.get(chave):
                os.environ[chave] = valor
        return arquivo
    return None


def exigir_elevenlabs(precisa_voz=True, parar=True):
    """Confere as chaves da ElevenLabs. Sem elas, diz exatamente o que falta e para.

    Devolve (chave, id_da_voz). Com parar=False devolve (None, None) em vez de sair.
    """
    arquivo = carregar_env()
    chave = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    voz = os.environ.get("ELEVENLABS_VOICE_ID", "").strip()
    faltando = []
    if not chave:
        faltando.append("ELEVENLABS_API_KEY")
    if precisa_voz and not voz:
        faltando.append("ELEVENLABS_VOICE_ID")
    if not faltando:
        return chave, voz
    if not parar:
        return None, None
    onde = str(arquivo) if arquivo else str(RAIZ / ".env") + " (o arquivo ainda nao existe)"
    fala("")
    fala("O reel narrado precisa da ElevenLabs, e falta configurar:")
    for nome in faltando:
        fala("  - " + nome)
    fala("")
    fala("Arquivo lido: " + onde)
    fala("Como resolver:")
    fala("  1. Copie o .env.exemplo da raiz do pacote para .env, se ainda nao copiou.")
    if "ELEVENLABS_API_KEY" in faltando:
        fala("  2. Crie a chave em https://elevenlabs.io/app/settings/api-keys e cole em ELEVENLABS_API_KEY=")
    if "ELEVENLABS_VOICE_ID" in faltando:
        fala("  3. Escolha a voz na biblioteca da ElevenLabs (ou a sua voz clonada), copie o id dela")
        fala("     e cole em ELEVENLABS_VOICE_ID=")
    fala("")
    fala("Nada foi gasto. O resto do pacote continua funcionando sem essas chaves.")
    fala("")
    sys.exit(3)


def modelo_padrao():
    carregar_env()
    return os.environ.get("ELEVENLABS_MODELO", "").strip() or "eleven_multilingual_v2"


# ------------------------------------------------------------------- caminhos

class Caminhos:
    """Os caminhos de um reel narrado, a partir da pasta do projeto e do numero."""

    def __init__(self, projeto, narrado="01"):
        p = Path(projeto)
        if not p.is_absolute():
            for base in (Path.cwd(), RAIZ, RAIZ / "projetos"):
                if (base / p).is_dir():
                    p = base / p
                    break
            else:
                p = Path.cwd() / p
        self.projeto = p.resolve()
        numero = str(narrado).strip()
        if numero.startswith("narrado-"):
            numero = numero[len("narrado-"):]
        if numero.isdigit():
            numero = "%02d" % int(numero)
        self.id = "narrado-" + numero
        self.trabalho = self.projeto / "materiais-de-trabalho" / self.id
        self.fonte = self.projeto / "materiais-de-trabalho" / "fonte"
        self.voz = self.trabalho / "voz"
        self.construcao = self.trabalho / "construcao"
        self.conferencia = self.trabalho / "conferencia"
        self.tomadas = self.trabalho / "tomadas.json"
        self.roteiro_tts = self.trabalho / "roteiro-tts.txt"
        self.linha = self.construcao / "linha_do_tempo.json"
        self.plano = self.construcao / "plano.json"
        self.imagem = self.construcao / "imagem.mp4"
        self.legendado = self.construcao / "legendado.mp4"
        self.eventos = self.construcao / "eventos.json"
        self.entrega_pasta = self.projeto / self.id
        self.entrega = self.entrega_pasta / (self.id + ".mp4")

    def no_projeto(self, relativo):
        """Resolve um caminho escrito no tomadas.json (relativo a pasta do projeto)."""
        if relativo is None:
            return None
        r = Path(relativo)
        if r.is_absolute():
            return r
        for base in (self.projeto, self.trabalho, RAIZ, PLUGIN):
            if (base / r).exists():
                return (base / r).resolve()
        return (self.projeto / r).resolve()


def argumentos_de_reel(analisador):
    analisador.add_argument("--projeto", required=True,
                            help="pasta do projeto, por exemplo projetos/lancamento-x")
    analisador.add_argument("--narrado", default="01",
                            help="numero do reel narrado dentro do projeto (padrao: 01)")
    return analisador


def ler_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def gravar_json(caminho, dados):
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)


def sem_notas(objeto):
    """Tira as chaves que comecam com _ (as notas de leitura dos arquivos de exemplo)."""
    if isinstance(objeto, dict):
        return {k: sem_notas(v) for k, v in objeto.items() if not str(k).startswith("_")}
    if isinstance(objeto, list):
        return [sem_notas(v) for v in objeto]
    return objeto


def ler_tomadas(cam):
    if not cam.tomadas.is_file():
        erro("nao achei o %s. Escreva o plano das tomadas antes (modelo em "
             "modelos/tomadas.exemplo.json, campos em referencias/TOMADAS.md)." % cam.tomadas)
    return sem_notas(ler_json(cam.tomadas))


# ------------------------------------------------------------------- marca

def ler_marca(pedido=None):
    """Devolve (tokens, caminho). Le marca/tokens.json; sem ele, cai no exemplo e avisa.

    pedido pode ser um tokens.json ou uma pasta que contenha um.
    """
    if pedido:
        p = Path(pedido)
        if p.is_dir():
            p = p / "tokens.json"
        if not p.is_file():
            erro("nao achei os tokens da marca em %s" % p)
        return sem_notas(ler_json(p)), p.resolve()
    p = RAIZ / "marca" / "tokens.json"
    if not p.is_file():
        exemplo = fabrica.achar("marca/tokens.exemplo.json")
        if not exemplo.is_file():
            erro("nao achei marca/tokens.json nem marca/tokens.exemplo.json.")
        aviso("ainda nao existe marca/tokens.json, entao estou usando o exemplo. Rode o "
              "/flow-reels:marca para o reel sair com a sua identidade.")
        p = exemplo
    return sem_notas(ler_json(p)), p.resolve()


def arquivo_fonte(tokens, origem, papel):
    """O arquivo de fonte de um papel (titulo, corpo, legenda), em caminho absoluto."""
    fontes = tokens.get("fontes") or {}
    item = fontes.get(papel) or fontes.get("titulo") or {}
    rel = item.get("arquivo")
    candidatos = []
    if rel:
        candidatos += [fabrica.achar(rel), Path(origem).parent / rel, Path(origem).parent / Path(rel).name]
    candidatos += [fabrica.achar("marca/fontes/Quicksand-Bold.ttf")]
    for c in candidatos:
        if c.is_file():
            return c
    erro("nao achei o arquivo de fonte do papel %s (%s)." % (papel, rel))


def hex_para_rgb(valor):
    v = str(valor or "#000000").lstrip("#")
    if len(v) != 6:
        return (0, 0, 0)
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cores(tokens):
    """As cores da marca em RGB, mais o par claro e escuro que a legenda usa."""
    c = tokens.get("cores") or {}
    saida = {k: hex_para_rgb(v) for k, v in c.items() if isinstance(v, str)}
    for chave, padrao in (("superficie", "#16151A"), ("superficie_alt", "#211F28"),
                          ("tinta", "#F5F2EE"), ("tinta_suave", "#9E99A8"),
                          ("destaque", "#E8A33D"), ("destaque_contraste", "#16151A")):
        saida.setdefault(chave, hex_para_rgb(padrao))
    a, b = saida["tinta"], saida["superficie"]
    saida["escuro"], saida["claro"] = (a, b) if luminancia(a) < luminancia(b) else (b, a)
    return saida


def pasta_de_audio(pedido=None):
    """Onde o leito e os efeitos ficam. Padrao: marca/audio, reaproveitado entre videos."""
    return Path(pedido).resolve() if pedido else RAIZ / "marca" / "audio"


# Sem o leito e os efeitos da ElevenLabs em marca/audio, o reel usa o que o pacote traz, de graca: uma
# trilha livre de componentes/trilhas e os sons sintetizados de componentes/sons, nesta troca de nomes.
SONS_DO_PACOTE = {"whoosh": "whoosh", "pop": "pop", "clique": "clique", "alternar": "bip",
                  "varredura": "subida", "assentar": "impacto", "digitar": "tick", "enviar": "pop"}
LEITO_DO_PACOTE = ("calma-pads-01.mp3", "calma-lofi-01.mp3")


def arquivo_de_efeito(pasta_audio, arquivo):
    """O efeito da marca (marca/audio/sfx/<arquivo>) ou, sem ele, o do pacote. None se nenhum."""
    proprio = Path(pasta_audio) / "sfx" / arquivo
    if proprio.is_file():
        return proprio
    familia = SONS_DO_PACOTE.get(Path(arquivo).stem)
    if not familia:
        return None
    for nome in (familia + ".wav", familia + "-1.wav"):
        p = fabrica.achar("componentes/sons/" + nome)
        if p.is_file():
            return p
    return None


def arquivo_de_leito(pasta_audio):
    """O leito da marca (marca/audio/leito.mp3) ou, sem ele, uma trilha calma do pacote. None se nenhum."""
    proprio = Path(pasta_audio) / "leito.mp3"
    if proprio.is_file():
        return proprio
    for nome in LEITO_DO_PACOTE:
        p = fabrica.achar("componentes/trilhas/" + nome)
        if p.is_file():
            return p
    return None


def url_de(caminho):
    """O endereco de um arquivo no servidor local, que serve a pasta de trabalho e o plugin."""
    p = Path(caminho).resolve()
    for base in (RAIZ, PLUGIN):
        try:
            return "/" + p.relative_to(base.resolve()).as_posix()
        except ValueError:
            continue
    return "/" + p.name


# ------------------------------------------------------------------- texto

def sem_acento(texto):
    t = unicodedata.normalize("NFKD", str(texto))
    return t.encode("ascii", "ignore").decode("ascii")


def normalizar(palavra):
    """Forma de comparacao: minuscula, sem acento, sem pontuacao nas pontas."""
    t = sem_acento(palavra).lower()
    return re.sub(r"^[^a-z0-9]+|[^a-z0-9]+$", "", t)


def recusar_travessao(texto, onde):
    """O pacote nao usa travessao. Texto com travessao para aqui, com o lugar dito."""
    for c in TRAVESSOES:
        if c in str(texto):
            erro("%s tem travessao (%s). Reescreva a frase com virgula, dois pontos ou ponto. "
                 "Trecho: %r" % (onde, c, str(texto)[:120]))
    if re.search(r"\s-\s", str(texto)):
        erro("%s tem hifen fazendo papel de pausa (' - '). Reescreva com virgula ou dois pontos. "
             "Trecho: %r" % (onde, str(texto)[:120]))


def ler_palavras(caminho):
    """Le o JSON de palavras que o voz.py escreve: {"palavras": [{texto, inicio, fim}]}."""
    dados = ler_json(caminho)
    lista = dados.get("palavras") if isinstance(dados, dict) else dados
    saida = []
    for p in lista or []:
        texto = p.get("texto", p.get("word"))
        ini = p.get("inicio", p.get("start"))
        fim = p.get("fim", p.get("end"))
        if texto is None or ini is None or fim is None:
            continue
        saida.append({"texto": str(texto), "inicio": float(ini), "fim": float(fim)})
    return saida


def achar_palavra(palavras, alvo, ocorrencia=1, depois=-1.0):
    """Indice da palavra (ou sequencia de palavras) alvo na fala, ou None.

    alvo pode ter mais de uma palavra ("nova versao"). ocorrencia conta a partir de 1,
    e so considera palavras que comecam depois do instante 'depois'.
    """
    partes = [normalizar(x) for x in str(alvo).split() if normalizar(x)]
    if not partes:
        return None
    vistas = 0
    for i in range(len(palavras) - len(partes) + 1):
        if palavras[i]["inicio"] < depois:
            continue
        if all(normalizar(palavras[i + k]["texto"]) == partes[k] for k in range(len(partes))):
            vistas += 1
            if vistas == int(ocorrencia or 1):
                return i
    return None


def resolver_instante(valor, palavras, onde, ajuste_padrao=0.0, depois=-1.0, fim=False):
    """Transforma um instante do tomadas.json em segundos da linha do tempo final.

    Aceita: numero (segundos), texto (uma palavra ou sequencia da fala) ou objeto
    {"palavra": "...", "ocorrencia": 2, "ajuste": -0.1}. Com fim=True devolve o fim da
    palavra em vez do comeco.
    """
    if valor is None:
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    ajuste, ocorr = ajuste_padrao, 1
    if isinstance(valor, dict):
        texto = valor.get("palavra")
        ocorr = valor.get("ocorrencia", 1)
        ajuste = float(valor.get("ajuste", ajuste_padrao))
        fim = bool(valor.get("fim", fim))
    else:
        texto = str(valor)
    i = achar_palavra(palavras, texto, ocorr, depois)
    if i is None:
        erro("%s: a palavra %r (ocorrencia %s) nao aparece na fala. Confira o texto contra "
             "construcao/linha_do_tempo.json." % (onde, texto, ocorr))
    n = len([x for x in str(texto).split() if normalizar(x)])
    t = palavras[i + n - 1]["fim"] if fim else palavras[i]["inicio"]
    return max(0.0, t + ajuste)


# ------------------------------------------------------------------- midia

def exigir_ffmpeg():
    for prog in ("ffmpeg", "ffprobe"):
        if shutil.which(prog) is None:
            erro("nao achei o %s no PATH. Rode o instalador do pacote." % prog)


def sondar(caminho):
    """ffprobe em JSON: streams e format."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json",
                        str(caminho)], capture_output=True, text=True, errors="replace")
    try:
        return json.loads(r.stdout or "{}")
    except Exception:
        return {}


def duracao(caminho):
    d = sondar(caminho)
    try:
        return float(d["format"]["duration"])
    except Exception:
        return 0.0


def tamanho_video(caminho):
    d = sondar(caminho)
    for s in d.get("streams", []):
        if s.get("codec_type") == "video":
            return int(s["width"]), int(s["height"])
    return None


def carregar_audio(caminho, sr=SR, filtro=None):
    """Audio mono float32 em [-1, 1], pelo ffmpeg. Arquivo sem audio devolve vazio."""
    import numpy as np
    cmd = ["ffmpeg", "-v", "error", "-i", str(caminho)]
    if filtro:
        cmd += ["-af", filtro]
    cmd += ["-vn", "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]
    bruto = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(bruto, np.int16).astype(np.float32) / 32768.0


def gravar_wav(caminho, amostras, sr=SR):
    import numpy as np
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(caminho), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(amostras, -1, 1) * 32767).astype(np.int16).tobytes())


def niveis(amostras, sr=SR, fps=FPS):
    """RMS por quadro, para o movimento cair no som de verdade."""
    import numpy as np
    k = sr // fps
    n = len(amostras) // k
    if n == 0:
        return []
    return [round(float(v), 4) for v in np.sqrt((amostras[:n * k].reshape(n, k) ** 2).mean(1))]


def medir_loudness(caminho):
    """Loudness integrado (LUFS) pelo filtro ebur128 do ffmpeg."""
    r = subprocess.run(["ffmpeg", "-v", "info", "-nostats", "-i", str(caminho), "-vn",
                        "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, errors="replace")
    linhas = [l for l in r.stderr.splitlines() if l.strip().startswith("I:")]
    if not linhas:
        return None
    try:
        return float(linhas[-1].split()[1])
    except Exception:
        return None
