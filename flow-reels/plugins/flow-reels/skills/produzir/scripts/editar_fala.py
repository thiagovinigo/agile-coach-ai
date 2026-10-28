#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
editar_fala.py  ·  o editor de fala: do trecho bruto ao fala.mp4 limpo

Primeira peça do motor 2.0 (motor/MOTOR.md, seções 1, 2.1 e 2.2). Pega um ou mais
trechos do vídeo da fonte e entrega o fala.mp4 que todas as outras peças usam como
base: o rosto é seguido nele, as cenas são cronometradas nele, a legenda acende
nele. Por isso ele sai daqui já limpo e já na velocidade final, e junto saem as
palavras na linha do tempo dele (palavras-corte.json) e a conta de tudo o que foi
tirado (edicao.json). Depois desta peça, ninguém precisa saber que a fonte existiu.

O que sai de dentro do trecho, e por quê:

  silêncio    pausa entre duas palavras maior que --pausa-max vira um respiro de
              --respiro. Pausa longa em reel é o segundo em que a pessoa começa a
              ouvir o vazio em vez da ideia.
  hesitação   "é", "éh", "eh", "ã", "hã", "ahn", "hum", "hmm", "ãh", e só quando a
              palavra está sozinha entre duas pausas de pelo menos 0,12 s. "tipo" e
              "né" só com --remover-tipo-ne, porque quase sempre são palavra de
              verdade. O "é" ainda precisa durar 0,25 s ou mais: curto entre pausas,
              ele é o verbo ("não é AI First, é qual a decisão"), e cortar o verbo
              muda a frase.
  repetição   a retomada: a pessoa começa, para e recomeça. Sai a primeira
              tentativa e fica a última versão completa. Contam duas formas: uma
              sequência de 3 ou mais palavras que se repete começando nas próximas
              10 palavras, e um começo em falso seguido de pausa de mais de 0,5 s e
              de uma frase que começa igual.

A regra que manda em todas: o corte cai no silêncio, nunca dentro de uma palavra.
O tempo da palavra vem do alinhador e é uma estimativa (CORTE-LIMPO.md, seção 2):
ele estica a palavra para dentro da pausa. Quem diz onde o som termina de verdade é
a energia do audio16k.wav, medida com a régua da seção 3 daquele arquivo (fala plena
= percentil 90 das janelas de 50 ms, silêncio abaixo de 8% dela), só que em passos
de 10 ms. Silêncio de pelo menos 0,12 s separa "ilhas de som"; abaixo disso é a
oclusiva de dentro da palavra (o "t" de "artificial" fica 90 ms calado), e ali não
se corta. Cada palavra é presa à ilha onde ela soa, e só se corta entre ilhas.

Conservador de propósito: na dúvida, não corta, e registra como suspeita no resumo e
no edicao.json. Uma hesitação que fica incomoda menos que uma sílaba comida. Som
forte sem palavra transcrita no meio do trecho (o transcritor costuma pular "ééé" e
"hum") também fica, e vira suspeita.

Os cortes caem na grade dos quadros (1/30 s). Assim o vídeo e o áudio de cada pedaço
têm exatamente a mesma duração, e a linha do tempo do palavras-corte.json é a do
fala.mp4 sem deriva acumulada de emenda em emenda.

Uso:

    flow-reels produzir/editar_fala --projeto projetos/<video> --corte 01
    flow-reels produzir/editar_fala --projeto projetos/<video> --corte 01 --trechos "0.40-12.31,14.0-41.2"
    flow-reels produzir/editar_fala --projeto projetos/<video> --corte 02 --velocidade auto
    flow-reels produzir/editar_fala --projeto projetos/<video> --corte 01 --ensaio

--trechos     os pedaços da fonte, em segundos, na ordem em que entram no corte (o
              gancho pode vir de depois do corpo). Sem eles, vai do primeiro ao
              último som falado. Com decimal em vírgula, separe os trechos com ponto
              e vírgula: "0,40-12,31; 14,0-41,2". O trecho escolhe as palavras (a que
              tem o meio dentro dele entra); o ponto exato de cada corte é medido.
--grafia      JSON com trocas de grafia: [{"de": "Cloud Code", "para": "Claude Code"}].
              Sem ele, usa materiais-de-trabalho/corte-NN/grafia.json se existir. A
              troca vale só no palavras-corte.json; o áudio é o mesmo.
--velocidade  1.0 (padrão), 1.25, 1.5... ou auto: o múltiplo de 0,05 entre 1,0 e 1,5
              que leva a fala para perto de 3,7 palavras/s. Acima de 3,2 fica 1,0.
--ensaio      calcula e imprime o resumo sem renderizar nem gravar nada.

Entra:  o vídeo da fonte (meta.video do palavras.json, ou o único vídeo em
        materiais-de-trabalho/fonte/), materiais-de-trabalho/transcricao/palavras.json
        e audio16k.wav.
Sai:    materiais-de-trabalho/corte-NN/fala.mp4, palavras-corte.json e edicao.json.
        O edicao.json segue o MOTOR.md 2.2 e traz a mais: trechos, parametros,
        suspeitas e emendas_suspeitas (energia medida em ±20 ms de cada emenda no
        fala.mp4 pronto, acima de 8% da fala plena = possível sílaba comida).

Saída 0 = fala.mp4 gerado e todas as emendas em silêncio. Saída 1 = o render falhou,
ou gerou mas alguma emenda caiu em som (ouça antes de seguir). Saída 2 = erro de uso
ou de entrada, e nada foi gravado.
"""

import argparse
import bisect
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import wave
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------------- a régua
# A medida de silêncio é a de `/flow-reels:planejar`/referencias/CORTE-LIMPO.md, seção 3.
# As folgas foram calibradas no primeiro vídeo do pacote, fala corrida a ~4 palavras/s.

FPS = 30
TAXA_SAIDA = 48000
AMOSTRAS_POR_QUADRO = TAXA_SAIDA // FPS   # 1600: cortar na grade casa vídeo e áudio
PASSO = 0.010              # o envelope de energia anda de 10 em 10 ms
JANELA_REFERENCIA = 5      # a fala plena é medida em janelas de 50 ms (5 passos)
LIMIAR_PADRAO = 0.08       # silêncio = abaixo de 8% da fala plena
PAUSA_MINIMA = 0.12        # silêncio mais curto que isso é oclusiva dentro de palavra
RABO_MINIMO = 0.04         # o corte não encosta no fim do som: o decaimento da vogal fica
ATAQUE_MINIMO = 0.06       # nem no começo: o ataque da consoante fica
FOLGA_VIZINHO = 0.04       # distância mínima de um som que vai sair
FRACAO_RABO = 0.4          # do respiro, 40% fica depois da palavra e 60% antes da próxima
ABERTURA = (0.08, 0.10, 0.12)   # entrada antes do primeiro som (CORTE-LIMPO.md, passo 4)
FECHO = (0.25, 0.30, 0.40)      # saída depois do último som
SOM_ANTES_DEMAIS = 0.40    # som colado antes da primeira palavra além disso não é ela
SOM_DEPOIS_DEMAIS = 0.60   # idem depois da última (o alinhador já estica o fim)
SOM_FORTE = 0.20           # ilha sem palavra com pico acima disso da fala plena pode ser fala
SOM_CURTO = 0.06           # ... a não ser que dure menos que isso: aí é estalo de boca
E_VERBO = 0.25             # "é" entre pausas só é hesitação se durar pelo menos isso
HESITACAO_LONGA = 1.2      # hesitação sozinha numa ilha mais longa que isso esconde outra coisa
JUNTA = 0.04               # pedaços separados por menos que isso viram um só
JANELA_REPETICAO = 10
MINIMO_REPETICAO = 3
PAUSA_FALSO_COMECO = 0.5
MAXIMO_FALSO_COMECO = 6
ALVO_RITMO = 3.7           # palavras por segundo: o ritmo-alvo dos reels do pacote
PISO_RITMO = 3.2           # acima disso a fala já está rápida o bastante
FAIXA_AUTO = (1.0, 1.5)
RAIO_EMENDA = 0.02
FADE = 0.010
GRAFO_LONGO = 8000         # acima disso o grafo vai por arquivo (limite da linha no Windows)

PREENCHIMENTOS = {"é", "éh", "eh", "ã", "hã", "ahn", "hum", "hm", "ãh"}  # já sem letra repetida
TIPO_NE = {"tipo", "né"}
# Palavras de ligação: frase que termina numa delas não fechou (CORTE-LIMPO.md, seção 5).
LIGACAO = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das",
    "e", "ou", "que", "em", "no", "na", "nos", "nas", "com", "por", "para", "pra",
    "pro", "se", "ao", "aos", "à", "às", "num", "numa", "pelo", "pela", "mas",
}
PONTUACAO = ".,;:!?…\"'“”‘’()[]{}«»—–-¿¡*"
EXTENSOES_VIDEO = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
MOTIVOS = ("silencio", "hesitacao", "repeticao", "fora-do-trecho")

RAIZ = fabrica.raiz()   # a pasta de trabalho (projetos/, setup.json)


# ------------------------------------------------------------------- utilidades

def erro(msg):
    print("  erro: " + msg, file=sys.stderr)


def falhar(msg, codigo=2):
    erro(msg)
    sys.exit(codigo)


def aviso(msg):
    print("  aviso: " + msg)


def num(x, casas=2):
    """Número no jeito brasileiro: 0,38."""
    return ("%.*f" % (casas, x)).replace(".", ",")


def carregar_numpy():
    try:
        import numpy
    except ImportError:
        falhar("o numpy não está instalado neste Python.\n"
               "       Rode com o Python do pacote: .venv/bin/python, ou instale com: pip install numpy")
    return numpy


def exigir_ffmpeg():
    for nome in ("ffmpeg", "ffprobe"):
        if shutil.which(nome) is None:
            falhar("%s não encontrado no PATH. Rode o instalar.sh (ou instalar.ps1) na raiz do pacote." % nome)


def normalizar(texto):
    """Minúsculas, sem pontuação nas pontas. O % e o $ ficam, porque são parte do número."""
    t = unicodedata.normalize("NFC", str(texto)).strip().lower()
    return t.strip(PONTUACAO)


def colapsar(texto):
    """'ééé' vira 'é' e 'hmmm' vira 'hm', para a hesitação esticada ser reconhecida."""
    return re.sub(r"(.)\1+", r"\1", texto)


def relativo(caminho, base):
    try:
        return Path(caminho).resolve().relative_to(Path(base).resolve()).as_posix()
    except ValueError:
        return Path(caminho).as_posix()


# ------------------------------------------------------------ achar as entradas

def achar_projeto(pedido):
    p = Path(pedido)
    for candidato in (p, RAIZ / p, RAIZ / "projetos" / p):
        if candidato.is_dir():
            return candidato
    falhar("não achei a pasta do projeto %s. Passe o caminho da pasta do vídeo, por exemplo\n"
           "       --projeto projetos/meu-video" % pedido)


def achar_transcricao(projeto, nome):
    for candidato in (projeto / "materiais-de-trabalho" / "transcricao" / nome, projeto / nome):
        if candidato.is_file():
            return candidato
    return None


def achar_video(projeto, meta):
    tentativas = []
    for chave in ("video", "fonte"):
        valor = meta.get(chave)
        if not valor:
            continue
        v = Path(str(valor).replace("\\", "/"))
        if v.is_absolute():
            tentativas.append(v)
        else:
            tentativas += [projeto / v, Path.cwd() / v, RAIZ / v]
        tentativas.append(projeto / "materiais-de-trabalho" / "fonte" / v.name)
    for t in tentativas:
        if t.is_file() and t.suffix.lower() in EXTENSOES_VIDEO:
            return t
    pasta = projeto / "materiais-de-trabalho" / "fonte"
    videos = sorted(f for f in pasta.iterdir() if f.suffix.lower() in EXTENSOES_VIDEO) if pasta.is_dir() else []
    if len(videos) == 1:
        return videos[0]
    if len(videos) > 1:
        falhar("achei %d vídeos em %s e o palavras.json não diz qual é o da fonte:\n         %s\n"
               "       Deixe só o vídeo da fonte nessa pasta." % (len(videos), pasta, "\n         ".join(v.name for v in videos)))
    falhar("não achei o vídeo da fonte. Ele mora em %s, e quem traz é a skill transcrever." % pasta)


def ler_palavras(caminho):
    try:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, ValueError) as falha:
        falhar("não consegui ler %s: %s" % (caminho, falha))
    lista = dados.get("palavras", dados.get("words")) if isinstance(dados, dict) else None
    if not lista:
        falhar("o arquivo %s não tem a lista 'palavras'. O formato é o da skill transcrever:\n"
               '       {"palavras": [{"inicio": 0.4, "fim": 0.46, "texto": "Sua"}], "meta": {...}}' % caminho)
    palavras = []
    for item in lista:
        texto = str(item.get("texto", item.get("word", ""))).strip()
        ini = item.get("inicio", item.get("start"))
        fim = item.get("fim", item.get("end"))
        if not texto or ini is None or fim is None:
            continue
        ini, fim = float(ini), float(fim)
        palavras.append({"ini": ini, "fim": max(ini, fim), "texto": texto})
    palavras.sort(key=lambda p: (p["ini"], p["fim"]))
    for i, p in enumerate(palavras):
        p["i"] = i
    if not palavras:
        falhar("o palavras.json não tem nenhuma palavra com tempo.")
    return palavras, (dados.get("meta") or {})


def sondar(caminho):
    cmd = ["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(caminho)]
    try:
        return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    except (subprocess.CalledProcessError, ValueError):
        return None


def fluxo(dados, tipo):
    for f in (dados or {}).get("streams", []):
        if f.get("codec_type") == tipo:
            return f
    return None


def flutuante(valor, padrao=0.0):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return padrao


# ------------------------------------------------------------------- a energia

def _quadrados(blocos, passo, np):
    """Média dos quadrados a cada 10 ms, lendo em blocos para não carregar uma hora de áudio."""
    resto = None
    partes = []
    for bloco in blocos:
        if resto is not None and resto.size:
            bloco = np.concatenate([resto, bloco])
        n = len(bloco) // passo
        if n:
            partes.append(np.square(bloco[: n * passo].reshape(n, passo)).mean(axis=1))
        resto = bloco[n * passo:]
    return np.concatenate(partes) if partes else np.zeros(0)


def energia_do_wav(caminho, np):
    try:
        arquivo = wave.open(str(caminho), "rb")
    except (wave.Error, EOFError, OSError):
        return None
    with arquivo:
        canais, largura = arquivo.getnchannels(), arquivo.getsampwidth()
        taxa, total = arquivo.getframerate(), arquivo.getnframes()
        if largura not in (1, 2, 4) or total == 0:
            return None

        def blocos():
            while True:
                dados = arquivo.readframes(taxa * 30)
                if not dados:
                    return
                if largura == 1:
                    x = (np.frombuffer(dados, np.uint8).astype(np.float64) - 128.0) / 128.0
                elif largura == 2:
                    x = np.frombuffer(dados, "<i2").astype(np.float64) / 32768.0
                else:
                    x = np.frombuffer(dados, "<i4").astype(np.float64) / 2147483648.0
                if canais > 1:
                    x = x[: len(x) - len(x) % canais].reshape(-1, canais).mean(axis=1)
                yield x

        return _quadrados(blocos(), int(round(taxa * PASSO)), np)


def energia_do_ffmpeg(caminho, np):
    """O mesmo, decodificando o áudio de um vídeo pelo ffmpeg (mono, 16 kHz)."""
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-i", str(caminho), "-vn",
           "-ac", "1", "-ar", "16000", "-f", "s16le", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def blocos():
        while True:
            dados = proc.stdout.read(16000 * 2 * 30)
            if not dados:
                return
            yield np.frombuffer(dados[: len(dados) - len(dados) % 2], "<i2").astype(np.float64) / 32768.0

    quadrados = _quadrados(blocos(), 160, np)
    proc.stderr.read()
    proc.wait()
    return quadrados if proc.returncode == 0 else None


def medir_envelope(quadrados, np):
    """Envelope em janelas de 30 ms a cada 10 ms, e a fala plena da gravação."""
    suave = np.convolve(quadrados, np.ones(3) / 3.0, mode="same")
    envelope = np.sqrt(np.maximum(suave, 0.0))
    m = len(quadrados) // JANELA_REFERENCIA
    if m:
        janelas = np.sqrt(quadrados[: m * JANELA_REFERENCIA].reshape(m, JANELA_REFERENCIA).mean(axis=1))
        referencia = float(np.percentile(janelas, 90))
    else:
        referencia = float(np.sqrt(quadrados.mean())) if quadrados.size else 0.0
    return envelope, referencia


def achar_ilhas(envelope, limiar, np):
    """Ilhas de som: o que sobra entre silêncios de pelo menos PAUSA_MINIMA."""
    silencio = (envelope < limiar).astype(np.int8)
    borda = np.diff(np.concatenate(([0], silencio, [0])))
    comecos, fins = np.where(borda == 1)[0], np.where(borda == -1)[0]
    minimo = int(round(PAUSA_MINIMA / PASSO))
    ilhas, cursor = [], 0
    for a, b in zip(comecos, fins):
        if b - a < minimo:
            continue
        if a > cursor:
            ilhas.append((cursor, a))
        cursor = b
    if cursor < len(envelope):
        ilhas.append((cursor, len(envelope)))
    return [{"ini": a * PASSO, "fim": b * PASSO, "pico": float(envelope[a:b].max()), "palavras": []}
            for a, b in ilhas]


# ------------------------------------------------------------------- o contexto

class Fala:
    """Tudo o que o plano precisa saber da fonte: palavras, ilhas, energia e a grade."""

    def __init__(self, palavras, envelope, referencia, limiar, duracao, delta, opcoes, np):
        self.palavras = palavras
        self.envelope = envelope
        self.referencia = referencia
        self.limiar = limiar
        self.duracao = duracao
        self.delta = delta              # o áudio começa delta segundos depois do começo do vídeo
        self.op = opcoes
        self.np = np
        self.ilhas = achar_ilhas(envelope, limiar, np)
        self.removida = {}              # índice da palavra -> motivo
        self.suspeitas = []
        self.ancorar()

    # -- ilhas
    def ancorar(self):
        """Prende cada palavra à ilha onde ela soa: a de maior sobreposição, ou a mais perto."""
        fins = [il["fim"] for il in self.ilhas]
        anterior = 0
        self.ilha_de = []
        for p in self.palavras:
            j = bisect.bisect_right(fins, p["ini"])
            melhor, sobra_melhor, k = None, 0.0, j
            while k < len(self.ilhas) and self.ilhas[k]["ini"] < p["fim"]:
                sobra = min(self.ilhas[k]["fim"], p["fim"]) - max(self.ilhas[k]["ini"], p["ini"])
                if sobra > sobra_melhor:
                    melhor, sobra_melhor = k, sobra
                k += 1
            if melhor is None:   # o alinhador pôs a palavra dentro de uma pausa
                candidatas = [c for c in (j - 1, j) if 0 <= c < len(self.ilhas)]
                melhor = min(candidatas, key=lambda c: max(0.0, self.ilhas[c]["ini"] - p["fim"],
                                                           p["ini"] - self.ilhas[c]["fim"]))
            melhor = max(melhor, anterior)
            self.ilha_de.append(melhor)
            self.ilhas[melhor]["palavras"].append(p["i"])
            anterior = melhor
        self.chaves = [(k, 1, i) for i, k in enumerate(self.ilha_de)]   # já em ordem

    def primeira(self, i):
        return i == 0 or self.ilha_de[i - 1] < self.ilha_de[i]

    def ultima(self, i):
        return i == len(self.palavras) - 1 or self.ilha_de[i + 1] > self.ilha_de[i]

    # -- energia e grade
    def e(self, t):
        k = min(max(int(t / PASSO), 0), len(self.envelope) - 1)
        return float(self.envelope[k]) / self.limiar

    def grade(self, lo, hi):
        a = math.ceil((lo + self.delta) * FPS - 1e-6)
        b = math.floor((hi + self.delta) * FPS + 1e-6)
        a = max(a, 0)
        return [k / FPS - self.delta for k in range(a, b + 1)]

    def escolher(self, lo, hi, preferido, peso=3.0):
        pontos = self.grade(lo, hi)
        if not pontos:
            return None
        return min(pontos, key=lambda g: self.e(g) + peso * abs(g - preferido))

    def mais_quieto(self, lo, hi):
        lo, hi = min(lo, hi), max(lo, hi)
        meio = (lo + hi) / 2.0
        pontos = self.grade(lo, hi) or self.grade(meio - 0.5 / FPS, meio + 0.5 / FPS)
        return min(pontos, key=lambda g: self.e(g) + abs(g - meio))

    def suspeita(self, tipo, de, ate, texto, porque):
        self.suspeitas.append({"tipo": tipo, "de": round(de, 3), "ate": round(ate, 3),
                               "texto": texto, "porque": porque})


# ---------------------------------------------------------------- os elementos
# Um elemento é o que fica no corte: uma palavra, ou uma ilha de som forte sem palavra
# (que fica por precaução). As junções entre elementos são onde se decide cortar.

def elemento_palavra(fala, i, trecho):
    p = fala.palavras[i]
    return {"tipo": "palavra", "i": i, "ilha": fala.ilha_de[i], "ini": p["ini"], "fim": p["fim"],
            "texto": p["texto"], "trecho": trecho}


def elemento_som(fala, k, trecho):
    il = fala.ilhas[k]
    return {"tipo": "som", "i": None, "ilha": k, "ini": il["ini"], "fim": il["fim"], "texto": "",
            "trecho": trecho}


def chave(el):
    return (el["ilha"], 1 if el["tipo"] == "palavra" else 0, el["i"] if el["i"] is not None else -1)


def palavras_entre(fala, x, y):
    """Índices das palavras da fonte que ficam entre x e y."""
    cx, cy = chave(x), chave(y)
    if cy <= cx:
        return []
    a, b = bisect.bisect_right(fala.chaves, cx), bisect.bisect_left(fala.chaves, cy)
    return [fala.chaves[k][2] for k in range(a, b)]


def som_fim(fala, el):
    """Onde o som do elemento acaba, ou None se ele está colado no que vem depois."""
    if el["tipo"] == "palavra" and not fala.ultima(el["i"]):
        return None
    return fala.ilhas[el["ilha"]]["fim"]


def som_ini(fala, el):
    if el["tipo"] == "palavra" and not fala.primeira(el["i"]):
        return None
    return fala.ilhas[el["ilha"]]["ini"]


def proximo_som(fala, el):
    k = el["ilha"] + 1
    return fala.ilhas[k]["ini"] if k < len(fala.ilhas) else fala.duracao


def som_anterior(fala, el):
    k = el["ilha"] - 1
    return fala.ilhas[k]["fim"] if k >= 0 else -fala.delta


def vale_depois(fala, x):
    """Corte forçado depois de x: o ponto mais quieto entre x e a palavra colada nele."""
    i = x["i"]
    if x["tipo"] == "palavra" and i + 1 < len(fala.palavras) and fala.ilha_de[i + 1] == x["ilha"]:
        return fala.mais_quieto(x["fim"] - 0.06, fala.palavras[i + 1]["ini"] + 0.06)
    return fala.mais_quieto(x["fim"] + 0.02, x["fim"] + 0.20)


def vale_antes(fala, y):
    i = y["i"]
    if y["tipo"] == "palavra" and i > 0 and fala.ilha_de[i - 1] == y["ilha"]:
        return fala.mais_quieto(fala.palavras[i - 1]["fim"] - 0.06, y["ini"] + 0.06)
    return fala.mais_quieto(y["ini"] - 0.20, y["ini"] - 0.02)


def ponto_de_saida(fala, x, faixa):
    """Onde o pedaço que termina em x acaba: depois do som dele, antes de qualquer som seguinte."""
    fim = som_fim(fala, x)
    if fim is not None and x["tipo"] == "palavra" and fim > x["fim"] + SOM_DEPOIS_DEMAIS:
        fim = None   # o som segue muito depois da palavra: é outra coisa colada nela
    if fim is None:
        return vale_depois(fala, x), True
    teto = min(proximo_som(fala, x) - FOLGA_VIZINHO, fala.duracao)
    minimo, alvo, maximo = faixa
    t = fala.escolher(fim + minimo, min(teto, fim + maximo), fim + alvo)
    if t is None:
        t = fala.escolher(fim + RABO_MINIMO, teto, fim + alvo)
    if t is None:
        return fala.mais_quieto(fim, proximo_som(fala, x)), True
    return t, False


def ponto_de_entrada(fala, y, faixa):
    """Onde o pedaço que começa em y começa: antes do ataque, depois de qualquer som anterior."""
    ini = som_ini(fala, y)
    if ini is not None and y["tipo"] == "palavra" and ini < y["ini"] - SOM_ANTES_DEMAIS:
        ini = None   # tem som demais colado antes da palavra: não é ela
    if ini is None:
        return vale_antes(fala, y), True
    piso = som_anterior(fala, y) + FOLGA_VIZINHO
    minimo, alvo, maximo = faixa
    t = fala.escolher(max(piso, ini - maximo), ini - minimo, ini - alvo)
    if t is None:
        t = fala.escolher(piso, ini - ATAQUE_MINIMO, ini - alvo)
    if t is None:
        return fala.mais_quieto(som_anterior(fala, y), ini), True
    return t, False


def melhor_par(fala, fim, teto_saida, ini, piso_entrada, alvo, mesma_linha):
    """Saída depois de fim e entrada antes de ini, deixando alvo segundos de silêncio no total.

    Entre os pares possíveis fica o de menor energia nos dois pontos, com uma leve
    preferência pela divisão 40% depois da palavra e 60% antes da próxima.
    """
    nominal = FRACAO_RABO * alvo
    um = 1.0 / FPS
    saidas = fala.grade(fim + RABO_MINIMO, min(teto_saida, fim + max(alvo - ATAQUE_MINIMO, RABO_MINIMO) + um))
    entradas = fala.grade(max(piso_entrada, ini - max(alvo - RABO_MINIMO, ATAQUE_MINIMO) - um), ini - ATAQUE_MINIMO)
    melhor = None
    for s in saidas:
        for e in entradas:
            if mesma_linha and e - s < um - 1e-9:
                continue
            rabo, ataque = s - fim, ini - e
            custo = fala.e(s) + fala.e(e) + 10.0 * abs(rabo + ataque - alvo) + 3.0 * abs(rabo - nominal)
            if melhor is None or custo < melhor[0]:
                melhor = (custo, s, e)
    return (melhor[1], melhor[2]) if melhor else None


def planejar_juncao(fala, x, y, adjacentes):
    """Decide a junção entre dois elementos que ficam um depois do outro no corte.

    Devolve None quando não há corte ali, ou (saída, entrada, apertada, pausa original).
    """
    respiro = fala.op.respiro
    if adjacentes:
        if x["ilha"] == y["ilha"]:
            return None                       # fala colada: não existe pausa para cortar
        fim, ini = fala.ilhas[x["ilha"]]["fim"], fala.ilhas[y["ilha"]]["ini"]
        pausa = ini - fim
        if pausa <= fala.op.pausa_max + 1e-9:
            return None
        par = melhor_par(fala, fim, ini - ATAQUE_MINIMO, ini, fim + RABO_MINIMO, respiro, True)
        if par is None or par[1] - par[0] < JUNTA:
            return None
        return par[0], par[1], False, pausa

    fim, ini = som_fim(fala, x), som_ini(fala, y)
    if x["tipo"] == "palavra" and fim is not None and fim > x["fim"] + SOM_DEPOIS_DEMAIS:
        fim = None
    if y["tipo"] == "palavra" and ini is not None and ini < y["ini"] - SOM_ANTES_DEMAIS:
        ini = None
    if fim is not None and ini is not None:
        teto = proximo_som(fala, x) - FOLGA_VIZINHO
        piso = som_anterior(fala, y) + FOLGA_VIZINHO
        mesma_linha = chave(y) > chave(x)
        par = melhor_par(fala, fim, teto, ini, piso, respiro, mesma_linha)
        if par is not None:
            return par[0], par[1], False, None
    s, apertada_s = ponto_de_saida(fala, x, (RABO_MINIMO, FRACAO_RABO * respiro, respiro - ATAQUE_MINIMO))
    e, apertada_e = ponto_de_entrada(fala, y, (ATAQUE_MINIMO, (1 - FRACAO_RABO) * respiro, respiro - RABO_MINIMO))
    return s, e, apertada_s or apertada_e, None


# ------------------------------------------------------- o que sai do trecho

def marcar_hesitacoes(fala, indices, tipo_ne):
    for i in indices:
        p = fala.palavras[i]
        n = normalizar(p["texto"])
        nc = colapsar(n)
        pura = nc in PREENCHIMENTOS
        if not (pura or (tipo_ne and n in TIPO_NE)):
            continue
        ilha = fala.ilhas[fala.ilha_de[i]]
        dura = ilha["fim"] - ilha["ini"]
        if not (fala.primeira(i) and fala.ultima(i)):
            if pura and n != "é":
                fala.suspeita("hesitacao", p["ini"], p["fim"], p["texto"],
                              "colada na fala, sem pausa dos dois lados; ficou")
            continue
        if n == "é" and dura < E_VERBO:
            fala.suspeita("hesitacao", ilha["ini"], ilha["fim"], p["texto"],
                          "'é' curto (%s s) entre pausas pode ser o verbo; ficou" % num(dura))
            continue
        if dura > HESITACAO_LONGA:
            fala.suspeita("hesitacao", ilha["ini"], ilha["fim"], p["texto"],
                          "a ilha de som dura %s s, longa demais para ser só a hesitação; ficou" % num(dura, 1))
            continue
        fala.removida[i] = "hesitacao"


def marcar_retomadas(fala, indices):
    """Sequência de 3+ palavras que se repete começando nas próximas ~10: sai a primeira."""
    seq = [i for i in indices if i not in fala.removida]
    # hesitação que sobrou no meio não conta na comparação; o "é" conta, porque quase sempre é o verbo
    toks = [i for i in seq if normalizar(fala.palavras[i]["texto"]) == "é"
            or colapsar(normalizar(fala.palavras[i]["texto"])) not in PREENCHIMENTOS]
    norms = [normalizar(fala.palavras[i]["texto"]) for i in toks]
    primeira_do_trecho = seq[0] if seq else None
    avisadas = set()   # o mesmo recomeço só vira suspeita uma vez
    k = 0
    while k < len(toks):
        achou, suspeita = None, None
        for j in range(k + MINIMO_REPETICAO, min(k + JANELA_REPETICAO, len(toks) - MINIMO_REPETICAO) + 1):
            tamanho, m = j - k, 0
            while m < tamanho and j + m < len(toks) and norms[k + m] == norms[j + m]:
                m += 1
            if m < MINIMO_REPETICAO:
                continue
            sobra = tamanho - m
            if sobra == 0 or (sobra == 1 and norms[j - 1] in LIGACAO):
                achou = j
                break
            if suspeita is None:
                suspeita = j
        if achou is not None:
            ini_i, recomeco = toks[k], toks[achou]
            limpo = fala.primeira(recomeco) and (fala.primeira(ini_i) or ini_i == primeira_do_trecho)
            texto = " ".join(fala.palavras[i]["texto"] for i in seq if ini_i <= i < recomeco)
            if limpo:
                for i in seq:
                    if ini_i <= i < recomeco:
                        fala.removida[i] = "repeticao"
                k = achou
                continue
            if recomeco not in avisadas:
                avisadas.add(recomeco)
                fala.suspeita("repeticao", fala.palavras[ini_i]["ini"], fala.palavras[recomeco]["ini"], texto,
                              "retomada sem pausa dos dois lados para cortar limpo; ficou")
        elif suspeita is not None and toks[suspeita] not in avisadas:
            a, b = toks[k], toks[suspeita]
            avisadas.add(b)
            texto = " ".join(fala.palavras[i]["texto"] for i in seq if a <= i < b)
            fala.suspeita("repeticao", fala.palavras[a]["ini"], fala.palavras[b]["ini"], texto,
                          "começa igual ao que vem depois mas termina diferente (retomada ou anáfora?); ficou")
        k += 1


def marcar_falsos_comecos(fala, indices):
    """Começo em falso, pausa de mais de 0,5 s e uma frase que começa igual."""
    seq = [i for i in indices if i not in fala.removida]
    for n, i in enumerate(seq[:-1]):
        prox = seq[n + 1]
        if i in fala.removida or not (fala.ultima(i) and fala.primeira(prox)):
            continue
        pausa = fala.ilhas[fala.ilha_de[prox]]["ini"] - fala.ilhas[fala.ilha_de[i]]["fim"]
        if pausa <= PAUSA_FALSO_COMECO:
            continue
        falso = [w for w in seq[: n + 1] if fala.ilha_de[w] == fala.ilha_de[i] and w not in fala.removida]
        if not falso or len(falso) > MAXIMO_FALSO_COMECO:
            continue
        if not (fala.primeira(falso[0]) or falso[0] == seq[0]):
            continue
        texto_final = fala.palavras[i]["texto"].rstrip()
        reticencias = texto_final.endswith(("...", "…", "-"))
        if texto_final.endswith((".", "!", "?")) and not reticencias:
            continue                          # frase fechada não é começo em falso
        depois = [normalizar(fala.palavras[w]["texto"]) for w in seq[n + 1: n + 1 + len(falso)]]
        antes = [normalizar(fala.palavras[w]["texto"]) for w in falso]
        if not depois or antes[0] != depois[0]:
            continue
        corta = (antes == depois[: len(antes)]
                 or reticencias
                 or (len(antes) >= 2 and antes[:-1] == depois[: len(antes) - 1] and antes[-1] in LIGACAO))
        texto = " ".join(fala.palavras[w]["texto"] for w in falso)
        if corta:
            for w in falso:
                fala.removida[w] = "repeticao"
        else:
            fala.suspeita("repeticao", fala.palavras[falso[0]]["ini"], fala.palavras[i]["fim"], texto,
                          "pausa de %s s e a frase seguinte começa igual; ficou" % num(pausa))


# --------------------------------------------------------------------- o plano

def ler_trechos(texto):
    texto = texto.strip()
    virgula_decimal = ";" in texto
    partes = texto.split(";") if virgula_decimal else texto.split(",")
    trechos = []
    for parte in partes:
        parte = parte.strip().replace("–", "-").replace("—", "-")
        if not parte:
            continue
        if virgula_decimal:
            parte = parte.replace(",", ".")
        m = re.match(r"^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$", parte)
        if not m:
            falhar("o trecho '%s' não está no formato inicio-fim em segundos, por exemplo 0.40-12.31.\n"
                   "       Vários trechos vão separados por vírgula: \"0.40-12.31,14.0-41.2\"." % parte)
        ini, fim = float(m.group(1)), float(m.group(2))
        if fim <= ini:
            falhar("no trecho '%s' o fim não é maior que o começo." % parte)
        trechos.append((ini, fim))
    if not trechos:
        falhar("--trechos veio vazio.")
    ordenados = sorted(trechos)
    for (a0, a1), (b0, b1) in zip(ordenados, ordenados[1:]):
        if b0 < a1:
            falhar("os trechos %s-%s e %s-%s se sobrepõem: o mesmo pedaço da fonte entraria duas vezes."
                   % (num(a0), num(a1), num(b0), num(b1)))
    return trechos


def montar_elementos(fala, trechos, opcoes):
    """Escolhe as palavras de cada trecho, marca o que sai e devolve os elementos na ordem do corte."""
    usadas = set()
    por_trecho = []
    for t, (ini, fim) in enumerate(trechos):
        indices = [p["i"] for p in fala.palavras
                   if ini <= (p["ini"] + p["fim"]) / 2.0 < fim and p["i"] not in usadas]
        if not indices:
            falhar("o trecho %s-%s não tem nenhuma palavra. Confira se os tempos são da fonte." % (num(ini), num(fim)))
        usadas.update(indices)
        por_trecho.append(indices)

    for indices in por_trecho:
        if not opcoes.sem_hesitacao:
            marcar_hesitacoes(fala, indices, opcoes.remover_tipo_ne)
        if not opcoes.sem_repeticao:
            marcar_retomadas(fala, indices)
            marcar_falsos_comecos(fala, indices)

    elementos = []
    for t, indices in enumerate(por_trecho):
        ficam = [i for i in indices if i not in fala.removida]
        if not ficam:
            aviso("o trecho %d ficou sem nenhuma palavra depois da limpeza e foi pulado." % (t + 1))
            continue
        for n, i in enumerate(ficam):
            if n:
                anterior = ficam[n - 1]
                for k in range(fala.ilha_de[anterior] + 1, fala.ilha_de[i]):
                    il = fala.ilhas[k]
                    if il["palavras"]:
                        continue
                    forte = il["pico"] >= SOM_FORTE * fala.referencia and il["fim"] - il["ini"] >= SOM_CURTO
                    if forte:
                        elementos.append(elemento_som(fala, k, t))
                        fala.suspeita("som-sem-palavra", il["ini"], il["fim"], "",
                                      "som forte (pico %d%% da fala plena) sem palavra transcrita; ficou"
                                      % round(100 * il["pico"] / fala.referencia))
            elementos.append(elemento_palavra(fala, i, t))
    if not elementos:
        falhar("não sobrou nenhuma palavra para o corte.")
    return elementos, usadas


def planejar(fala, elementos):
    """Percorre os elementos na ordem do corte e decide onde cada pedaço começa e acaba."""
    segmentos, juncoes = [], []
    atual = None
    for n, y in enumerate(elementos):
        if n == 0:
            entrada, apertada = ponto_de_entrada(fala, y, ABERTURA)
            atual = {"de": entrada, "elementos": [], "trechos": {y["trecho"]}}
            if apertada:
                fala.suspeita("emenda", entrada, entrada, y["texto"],
                              "a abertura não tem silêncio antes da primeira palavra; o corte é forçado")
        else:
            x = elementos[n - 1]
            entre = palavras_entre(fala, x, y)
            adjacentes = chave(y) > chave(x) and not entre
            j = planejar_juncao(fala, x, y, adjacentes)
            if j is not None:
                s, e, apertada, pausa = j
                if adjacentes:
                    motivo = "silencio"
                elif x["trecho"] != y["trecho"]:
                    motivo = "fora-do-trecho"
                elif any(fala.removida.get(i) == "repeticao" for i in entre):
                    motivo = "repeticao"
                else:
                    motivo = "hesitacao"
                atual["ate"] = s
                segmentos.append(atual)
                juncoes.append({"saida": s, "entrada": e, "motivo": motivo, "apertada": apertada,
                                "pausa": pausa, "palavras": entre, "x": x, "y": y})
                if apertada:
                    fala.suspeita("emenda", s, e, "%s | %s" % (x["texto"], y["texto"]),
                                  "não há silêncio limpo nesta junção; o corte é forçado no ponto mais quieto")
                atual = {"de": e, "elementos": [], "trechos": {y["trecho"]}}
        atual["elementos"].append(y)
        atual["trechos"].add(y["trecho"])
    saida, apertada = ponto_de_saida(fala, elementos[-1], FECHO)
    atual["ate"] = saida
    segmentos.append(atual)
    if apertada:
        fala.suspeita("emenda", saida, saida, elementos[-1]["texto"],
                      "o fecho não tem silêncio depois da última palavra; o corte é forçado")

    # pedaços vizinhos na fonte, separados por menos de JUNTA, viram um só
    k = len(segmentos) - 1
    while k > 0:
        a, b = segmentos[k - 1], segmentos[k]
        if 0.0 <= b["de"] - a["ate"] < JUNTA:
            a["ate"] = b["ate"]
            a["elementos"] += b["elementos"]
            a["trechos"] |= b["trechos"]
            del segmentos[k]
            del juncoes[k - 1]
        k -= 1

    cursor = 0
    for s in segmentos:
        quadros = int(round((s["ate"] - s["de"]) * FPS))
        if quadros < 1:
            quadros = 1
            s["ate"] = s["de"] + 1.0 / FPS
        s["quadros"] = quadros
        s["saida_q"] = cursor
        cursor += quadros
    return segmentos, juncoes


def escolher_velocidade(pedido, n_palavras, duracao_1x):
    ritmo = n_palavras / duracao_1x if duracao_1x > 0 else 0.0
    if pedido != "auto":
        return pedido, ritmo
    if ritmo > PISO_RITMO or ritmo <= 0:
        return 1.0, ritmo
    v = round((ALVO_RITMO / ritmo) / 0.05) * 0.05
    return round(min(max(v, FAIXA_AUTO[0]), FAIXA_AUTO[1]), 2), ritmo


def remapear(fala, segmentos, velocidade):
    """As palavras que ficaram, na linha do tempo do fala.mp4."""
    saida = []
    for s in segmentos:
        base = s["saida_q"] / float(FPS)
        for el in s["elementos"]:
            if el["tipo"] != "palavra":
                continue
            a = min(max(el["ini"], s["de"]), s["ate"])
            b = min(max(el["fim"], s["de"]), s["ate"])
            saida.append({"inicio": (base + a - s["de"]) / velocidade,
                          "fim": (base + b - s["de"]) / velocidade,
                          "texto": el["texto"]})
    for n, p in enumerate(saida):
        if n and p["inicio"] < saida[n - 1]["inicio"]:
            p["inicio"] = saida[n - 1]["inicio"]
        p["fim"] = max(p["fim"], p["inicio"])
    for n in range(len(saida) - 1):
        if saida[n]["fim"] > saida[n + 1]["inicio"]:
            saida[n]["fim"] = max(saida[n]["inicio"], saida[n + 1]["inicio"])
    for p in saida:
        p["inicio"], p["fim"] = round(p["inicio"], 3), round(p["fim"], 3)
    return saida


# ----------------------------------------------------------------------- grafia

def ler_grafia(caminho):
    try:
        regras = json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, ValueError) as falha:
        falhar("não consegui ler a grafia %s: %s" % (caminho, falha))
    modelo = '[{"de": "Cloud Code", "para": "Claude Code"}]'
    if not isinstance(regras, list):
        falhar("a grafia %s precisa ser uma lista, assim: %s" % (caminho, modelo))
    saida = []
    for n, r in enumerate(regras, 1):
        if not isinstance(r, dict) or not str(r.get("de", "")).strip() or not str(r.get("para", "")).strip():
            falhar("a regra %d da grafia %s precisa de \"de\" e \"para\", assim: %s" % (n, caminho, modelo))
        de = [normalizar(t) for t in str(r["de"]).split()]
        de = [t for t in de if t]
        if not de:
            falhar("a regra %d da grafia %s tem um \"de\" só de pontuação." % (n, caminho))
        saida.append({"de": de, "para": str(r["para"]).split(), "original": (str(r["de"]), str(r["para"]))})
    return saida


def aplicar_grafia(palavras, regras):
    """Troca frases inteiras; a palavra nova ocupa do início da primeira ao fim da última."""
    regras = sorted(regras, key=lambda r: -len(r["de"]))
    norms = [normalizar(p["texto"]) for p in palavras]
    saida, contagem, i = [], {}, 0
    while i < len(palavras):
        for r in regras:
            n = len(r["de"])
            if norms[i: i + n] != r["de"]:
                continue
            velhas = palavras[i: i + n]
            primeira, ultima = velhas[0]["texto"], velhas[-1]["texto"]
            abre = primeira[: len(primeira) - len(primeira.lstrip(PONTUACAO))]
            fecha = ultima[len(ultima.rstrip(PONTUACAO)):]
            para = list(r["para"])
            if len(para) == n:
                novas = [{"inicio": v["inicio"], "fim": v["fim"], "texto": t} for v, t in zip(velhas, para)]
            else:
                ini, fim = velhas[0]["inicio"], velhas[-1]["fim"]
                pesos = [max(1, len(t)) for t in para]
                total, acumulado, novas = float(sum(pesos)), 0, []
                for t, peso in zip(para, pesos):
                    a = ini + (fim - ini) * acumulado / total
                    acumulado += peso
                    novas.append({"inicio": round(a, 3), "fim": round(ini + (fim - ini) * acumulado / total, 3),
                                  "texto": t})
            if abre and not novas[0]["texto"].startswith(abre):
                novas[0]["texto"] = abre + novas[0]["texto"]
            if fecha:
                novas[-1]["texto"] = novas[-1]["texto"].rstrip(PONTUACAO) + fecha
            saida.extend(novas)
            contagem[r["original"]] = contagem.get(r["original"], 0) + 1
            i += n
            break
        else:
            saida.append(palavras[i])
            i += 1
    return saida, contagem


# ---------------------------------------------------------------------- render

def versao_ffmpeg():
    try:
        primeira = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.splitlines()[0]
        m = re.search(r"version\s+n?(\d+)", primeira)
        return int(m.group(1)) if m else 99
    except Exception:
        return 99


def montar_grafo(segmentos, velocidade, delta, largura, altura):
    """Duas entradas do ffmpeg por grupo de pedaços que andam para a frente na fonte.

    O vídeo entra com -ss, para só a parte que interessa ser decodificada, e é posto na
    grade de 30 fps a partir do ponto de leitura. O áudio entra SEM -ss, lido desde o
    começo: no ffmpeg 9, a busca de entrada desloca o AAC em ~20 ms em alguns pontos (a
    pré-carga do codificador é descartada duas vezes), e 20 ms de dessincronia é o que
    faz a boca parecer dublada. Decodificar só o áudio desde o zero custa poucos
    segundos por hora de fonte. Cada pedaço sai por número de quadro e de amostra, e o
    vídeo e o áudio dele têm a mesma duração exata.
    """
    grupos = []
    for k, s in enumerate(segmentos):
        if grupos and s["de"] >= segmentos[k - 1]["ate"] - 1e-6:
            grupos[-1].append(k)
        else:
            grupos.append([k])
    escala = ""
    if largura % 2 or altura % 2:
        escala = ",scale=trunc(iw/2)*2:trunc(ih/2)*2"
    entradas, partes, rotulos = [], [], []
    for g, ks in enumerate(grupos):
        x0 = math.floor(max(0.0, segmentos[ks[0]]["de"] + delta - 1.0) * FPS) / FPS
        fim = max(segmentos[k]["ate"] for k in ks) + delta
        entradas.append(("-an", x0, fim - x0 + 0.5))      # entrada 2g: só o vídeo, com busca
        entradas.append(("-vn", None, fim + 0.5))         # entrada 2g+1: só o áudio, desde o zero
        n = len(ks)
        video = "[%d:v]fps=%d:start_time=0%s" % (2 * g, FPS, escala)
        audio = "[%d:a]aresample=%d,aformat=sample_fmts=fltp:channel_layouts=stereo" % (2 * g + 1, TAXA_SAIDA)
        if n > 1:
            partes.append(video + ",split=%d" % n + "".join("[g%dv%d]" % (g, j) for j in range(n)))
            partes.append(audio + ",asplit=%d" % n + "".join("[g%da%d]" % (g, j) for j in range(n)))
        else:
            partes.append(video + "[g%dv0]" % g)
            partes.append(audio + "[g%da0]" % g)
        for j, k in enumerate(ks):
            s = segmentos[k]
            a = int(round((s["de"] + delta - x0) * FPS))     # quadro, contado do ponto de leitura
            b = a + s["quadros"]
            # o mesmo instante no áudio, contado da primeira amostra dele. Os tempos das palavras já
            # estão na linha do tempo do áudio (a transcrição lê o áudio), e o áudio entra sem busca,
            # desde a primeira amostra: somar o delta aqui contava o atraso duas vezes (a fonte do
            # iPhone, com o áudio 0,8 s depois do vídeo, saía com a voz 0,64 s adiantada a 1,25x)
            q = int(round(s["de"] * FPS))
            dura = s["quadros"] / float(FPS)
            partes.append("[g%dv%d]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS[v%d]" % (g, j, a, b, k))
            # o pedaço que começa antes da primeira amostra do áudio (o vídeo começou antes dele) recebe
            # silêncio na frente, para o áudio e o vídeo do pedaço continuarem com a mesma duração
            antes = max(0, -q) * AMOSTRAS_POR_QUADRO
            atraso = ",adelay=delays=%dS:all=1" % antes if antes else ""
            partes.append("[g%da%d]atrim=start_sample=%d:end_sample=%d,asetpts=PTS-STARTPTS%s,"
                          "afade=t=in:st=0:d=%.3f,afade=t=out:st=%.6f:d=%.3f[a%d]"
                          % (g, j, max(0, q) * AMOSTRAS_POR_QUADRO, (q + s["quadros"]) * AMOSTRAS_POR_QUADRO, atraso,
                             FADE, max(0.0, dura - FADE), FADE, k))
            rotulos.append("[v%d][a%d]" % (k, k))
    partes.append("".join(rotulos) + "concat=n=%d:v=1:a=1[vc][ac]" % len(segmentos))
    if abs(velocidade - 1.0) > 1e-9:
        partes.append("[vc]setpts=PTS/%.4f,fps=%d,format=yuv420p[vo]" % (velocidade, FPS))
        partes.append("[ac]atempo=%.4f[ao]" % velocidade)
    else:
        partes.append("[vc]format=yuv420p[vo]")
        partes.append("[ac]anull[ao]")
    return entradas, ";".join(partes), len(grupos)


def renderizar(video, segmentos, velocidade, delta, sonda, destino, forcar_arquivo=False):
    fv = fluxo(sonda, "video") or {}
    largura, altura = int(fv.get("width") or 0), int(fv.get("height") or 0)
    entradas, grafo, grupos = montar_grafo(segmentos, velocidade, delta, largura, altura)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-v", "error", "-nostdin"]
    for bloqueio, x0, dura in entradas:
        cmd += [bloqueio]
        if x0 is not None:
            cmd += ["-ss", "%.6f" % x0]
        cmd += ["-t", "%.6f" % dura, "-i", str(video)]
    arquivo_grafo = None
    if len(grafo) > GRAFO_LONGO or forcar_arquivo:
        arquivo_grafo = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
        arquivo_grafo.write(grafo)
        arquivo_grafo.close()
        opcao = "-/filter_complex" if versao_ffmpeg() >= 7 else "-filter_complex_script"
        cmd += [opcao, arquivo_grafo.name]
    else:
        cmd += ["-filter_complex", grafo]
    cmd += ["-map", "[vo]", "-map", "[ao]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-ar", str(TAXA_SAIDA), "-ac", "2"]
    for opcao, chave_fv in (("-color_range", "color_range"), ("-colorspace", "color_space"),
                            ("-color_primaries", "color_primaries"), ("-color_trc", "color_transfer")):
        valor = fv.get(chave_fv)
        if valor and valor not in ("unknown", "reserved"):
            cmd += [opcao, valor]
    cmd += ["-movflags", "+faststart", str(destino)]
    resultado = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if arquivo_grafo:
        Path(arquivo_grafo.name).unlink(missing_ok=True)
    return resultado, grupos


def conferir_arquivo(caminho, duracao_esperada):
    """Formato do fala.mp4: 30 fps, yuv420p, AAC 48 kHz, faststart e a duração do plano."""
    dados = sondar(caminho)
    fv, fa = fluxo(dados, "video"), fluxo(dados, "audio")
    problemas = []
    if not fv or not fa:
        return None, ["o arquivo saiu sem vídeo ou sem áudio"]
    try:
        n, d = (float(x) for x in fv.get("avg_frame_rate", "0/1").split("/"))
        fps = n / d if d else 0.0
    except ValueError:
        fps = 0.0
    if abs(fps - FPS) > 0.05:
        problemas.append("a taxa saiu %s fps, não %d" % (num(fps), FPS))
    if fv.get("pix_fmt") != "yuv420p":
        problemas.append("o formato de pixel saiu %s, não yuv420p" % fv.get("pix_fmt"))
    if int(fa.get("sample_rate") or 0) != TAXA_SAIDA:
        problemas.append("o áudio saiu a %s Hz" % fa.get("sample_rate"))
    with open(caminho, "rb") as arquivo:
        if b"moov" not in arquivo.read(4096):
            problemas.append("o índice moov não está no começo (faststart falhou)")
    duracao = flutuante((dados.get("format") or {}).get("duration"))
    if abs(duracao - duracao_esperada) > 0.1:
        problemas.append("a duração saiu %s s e o plano dizia %s s" % (num(duracao, 3), num(duracao_esperada, 3)))
    info = {"largura": fv.get("width"), "altura": fv.get("height"), "fps": fps, "duracao": duracao}
    return info, problemas


def conferir_emendas(caminho, emendas, referencia, limiar, np):
    """Energia em ±20 ms de cada emenda no fala.mp4 pronto: emenda em som é sílaba comida."""
    quadrados = energia_do_ffmpeg(caminho, np)
    if quadrados is None or not quadrados.size:
        return None
    rms = np.sqrt(quadrados)     # janelas de 10 ms sem suavizar: a medida fica dentro dos ±20 ms
    resultado = []
    for t in emendas:
        a = max(0, int(math.ceil((t - RAIO_EMENDA) / PASSO - 0.5)))
        b = min(len(rms), int(math.floor((t + RAIO_EMENDA) / PASSO - 0.5)) + 1)
        pico = float(rms[a:b].max()) if b > a else 0.0
        resultado.append({"t": round(t, 3), "pico": round(pico / referencia, 3), "em_som": pico >= limiar})
    return resultado


# ------------------------------------------------------------------ o resumo

def listar(itens, limite=8):
    if len(itens) <= limite:
        return itens
    return itens[:limite] + ["... e mais %d" % (len(itens) - limite)]


def imprimir_resumo(r):
    print("")
    print("  editor de fala  ·  %s  ·  corte-%s" % (r["projeto"], r["corte"]))
    print("  fonte     %s  (%s s, %s)" % (r["fonte"], num(r["duracao_fonte"], 1), r["resolucao"]))
    if r["implicito"]:
        print("  trechos   do primeiro ao último som falado (cortado em %s s e %s s)"
              % (num(r["trechos"][0][0]), num(r["trechos"][0][1])))
    else:
        print("  trechos   %s" % ", ".join("%s-%s" % (num(a), num(b)) for a, b in r["trechos"]))
    if r["grafia"]:
        print("  grafia    %s  (%d regra(s), %d troca(s))" % (r["grafia"], r["grafia_regras"], sum(r["grafia_trocas"].values())))
    print("")
    print("  antes     %s s de trecho · %d palavras · %s palavras/s"
          % (num(r["antes_dur"], 1), r["antes_palavras"], num(r["antes_ritmo"])))
    print("  depois    %s s de fala.mp4 · %d palavras · %s palavras/s · velocidade %s"
          % (num(r["depois_dur"], 1), r["depois_palavras"], num(r["depois_ritmo"]), r["velocidade_txt"]))
    print("")
    removidos = r["removidos"]
    tirado = sum(x["ate"] - x["de"] for x in removidos)
    print("  cortes    %d no total, %s s da fonte ficaram de fora" % (len(removidos), num(tirado, 2)))
    nomes = {"silencio": "silêncio", "hesitacao": "hesitação", "repeticao": "repetição",
             "fora-do-trecho": "fora do trecho"}
    for motivo in MOTIVOS:
        doles = [x for x in removidos if x["motivo"] == motivo]
        soma = sum(x["ate"] - x["de"] for x in doles)
        print("    %-15s %2d   %s s" % (nomes[motivo], len(doles), num(soma)))
        linhas = []
        for x in doles:
            borda = ""
            if x["de"] <= 1e-3:
                borda = "  (começo da fonte)"
            elif x["ate"] >= r["duracao_audio"] - 1e-3:
                borda = "  (fim da fonte)"
            if motivo == "silencio" and x.get("pausa"):
                linhas.append("%s s: pausa de %s s virou %s s" % (num(x["de"]), num(x["pausa"]), num(x["pausa"] - (x["ate"] - x["de"]))))
            elif x["texto"]:
                texto = x["texto"] if len(x["texto"]) <= 70 else x["texto"][:67] + "..."
                linhas.append("%s-%s s: \"%s\"%s" % (num(x["de"]), num(x["ate"]), texto, borda))
            else:
                linhas.append("%s-%s s%s" % (num(x["de"]), num(x["ate"]), borda))
        for linha in listar(linhas):
            print("        " + linha)
    if r["grafia_trocas"]:
        print("")
        print("  grafia    " + ", ".join("%s → %s (%dx)" % (de, para, n) for (de, para), n in r["grafia_trocas"].items()))
    for de, para in r["grafia_sem_uso"]:
        print("  olhe      a regra de grafia \"%s\" → \"%s\" não achou nada no corte" % (de, para))
    if r["suspeitas"]:
        print("")
        print("  suspeitas (ficaram como estavam; ouça se quiser cortar na mão)")
        for s in listar(["%s-%s s  %s  %s%s" % (num(x["de"]), num(x["ate"]), x["tipo"],
                                               ("\"%s\": " % x["texto"]) if x["texto"] else "", x["porque"])
                         for x in r["suspeitas"]], 12):
            print("    " + s)
    print("")
    if r.get("emendas_conferidas") is None:
        print("  emendas   %d (sem conferência no áudio: ensaio)" % len(r["emendas"]))
    else:
        ruins = [e for e in r["emendas_conferidas"] if e["em_som"]]
        if not r["emendas_conferidas"]:
            print("  ok  nenhuma emenda: o corte é um pedaço só")
        elif ruins:
            print("  OLHE  %d de %d emenda(s) caíram em som (possível sílaba comida):"
                  % (len(ruins), len(r["emendas_conferidas"])))
            for e in ruins:
                print("    %s s no fala.mp4: pico de %d%% da fala plena em ±20 ms (silêncio é abaixo de %d%%)"
                      % (num(e["t"]), round(100 * e["pico"]), round(100 * r["limiar_fracao"])))
        else:
            maior = max(e["pico"] for e in r["emendas_conferidas"])
            print("  ok  %d emenda(s), todas em silêncio (maior pico em ±20 ms: %d%% da fala plena)"
                  % (len(r["emendas_conferidas"]), round(100 * maior)))
    if r["sugestao"]:
        print("  dica      a fala está em %s palavras/s, abaixo de %s. Tente --velocidade %s (ou auto)."
              % (num(r["depois_ritmo"]), num(PISO_RITMO, 1), r["sugestao"]))
    for p in r["problemas"]:
        print("  OLHE  " + p)
    print("")


# ------------------------------------------------------------------- principal

def ler_velocidade(texto):
    t = str(texto).strip().lower().replace(",", ".")
    if t == "auto":
        return "auto"
    try:
        v = float(t)
    except ValueError:
        falhar("--velocidade é um número (1.0, 1.25, 1.5) ou auto, e veio '%s'." % texto)
    if not 0.5 <= v <= 2.0:
        falhar("--velocidade fica entre 0,5 e 2,0; acima de 1,5 a fala já soa estranha.")
    return v


def principal():
    ap = argparse.ArgumentParser(
        description="Transforma um trecho bruto da fonte no fala.mp4 limpo, com palavras-corte.json e edicao.json.")
    ap.add_argument("--projeto", required=True, help="a pasta do vídeo, por exemplo projetos/meu-video")
    ap.add_argument("--corte", required=True, help="o número do corte, por exemplo 01")
    ap.add_argument("--trechos", help='trechos da fonte em segundos, na ordem do corte: "0.40-12.31,14.0-41.2"')
    ap.add_argument("--grafia", help="JSON com trocas de grafia (padrão: corte-NN/grafia.json, se existir)")
    ap.add_argument("--velocidade", default="1.0", help="1.0 (padrão), 1.25, 1.5... ou auto")
    ap.add_argument("--pausa-max", type=float, default=0.35, help="pausa maior que isso vira respiro (padrão 0,35 s)")
    ap.add_argument("--respiro", type=float, default=0.15, help="o silêncio que fica no lugar da pausa (padrão 0,15 s)")
    ap.add_argument("--limiar", type=float, default=LIMIAR_PADRAO,
                    help="fração da fala plena abaixo da qual é silêncio (padrão 0,08, como no CORTE-LIMPO.md)")
    ap.add_argument("--sem-hesitacao", action="store_true", help="não tira hesitação")
    ap.add_argument("--sem-repeticao", action="store_true", help="não tira retomada nem começo em falso")
    ap.add_argument("--remover-tipo-ne", action="store_true", help="tira também 'tipo' e 'né' soltos entre pausas")
    ap.add_argument("--ensaio", action="store_true", help="só calcula e imprime o resumo, sem gravar nada")
    ap.add_argument("--grafo-em-arquivo", action="store_true", help=argparse.SUPPRESS)
    if len(sys.argv) == 1:
        ap.print_help()
        print("\nFaltou dizer o projeto e o corte, por exemplo: --projeto projetos/meu-video --corte 01")
        return 2
    op = ap.parse_args()

    m = re.match(r"^(?:corte-)?(\d{1,3})$", str(op.corte).strip())
    if not m:
        falhar("--corte é o número do corte, por exemplo 01, e veio '%s'." % op.corte)
    corte = "%02d" % int(m.group(1))
    op.velocidade = ler_velocidade(op.velocidade)
    if op.respiro < RABO_MINIMO + ATAQUE_MINIMO:
        falhar("o --respiro mínimo é %s s: %s s de rabo da palavra e %s s de ataque da próxima."
               % (num(RABO_MINIMO + ATAQUE_MINIMO), num(RABO_MINIMO), num(ATAQUE_MINIMO)))
    if op.pausa_max < op.respiro:
        falhar("--pausa-max (%s s) não pode ser menor que --respiro (%s s): a pausa cresceria."
               % (num(op.pausa_max), num(op.respiro)))
    if not 0.01 <= op.limiar <= 0.5:
        falhar("--limiar é uma fração da fala plena, entre 0,01 e 0,5 (padrão 0,08).")

    exigir_ffmpeg()
    np = carregar_numpy()

    projeto = achar_projeto(op.projeto)
    caminho_palavras = achar_transcricao(projeto, "palavras.json")
    if caminho_palavras is None:
        falhar("não achei o palavras.json em %s/materiais-de-trabalho/transcricao/.\n"
               "       Ele nasce da skill transcrever; rode ela antes." % projeto)
    palavras, meta = ler_palavras(caminho_palavras)
    if meta.get("alinhado") is False:
        aviso("o palavras.json diz alinhado: false. Os tempos são por frase, e o corte fica mais cego.")
    video = achar_video(projeto, meta)
    sonda = sondar(video)
    if not sonda or not fluxo(sonda, "video"):
        falhar("o ffprobe não achou vídeo dentro de %s." % video)
    fa = fluxo(sonda, "audio")
    if not fa:
        falhar("a fonte %s não tem áudio. O editor de fala corta pela fala." % video)
    duracao_fonte = flutuante((sonda.get("format") or {}).get("duration"))
    delta = flutuante(fa.get("start_time")) - flutuante((sonda.get("format") or {}).get("start_time"))
    if abs(delta) < 0.002:
        delta = 0.0
    else:
        aviso("o áudio da fonte começa %s s depois do vídeo; os cortes levam isso em conta." % num(delta, 3))

    pasta_corte = projeto / "materiais-de-trabalho" / ("corte-" + corte)
    caminho_grafia = None
    if op.grafia:
        caminho_grafia = Path(op.grafia)
        if not caminho_grafia.is_file() and (projeto / op.grafia).is_file():
            caminho_grafia = projeto / op.grafia
        if not caminho_grafia.is_file():
            falhar("não achei a grafia %s." % op.grafia)
    elif (pasta_corte / "grafia.json").is_file():
        caminho_grafia = pasta_corte / "grafia.json"
    regras = ler_grafia(caminho_grafia) if caminho_grafia else []

    caminho_audio = achar_transcricao(projeto, "audio16k.wav")
    quadrados = energia_do_wav(caminho_audio, np) if caminho_audio else None
    if quadrados is None:
        aviso("não achei um audio16k.wav legível; vou medir a energia direto do vídeo da fonte.")
        quadrados = energia_do_ffmpeg(video, np)
        if quadrados is None:
            falhar("não consegui ler o áudio da fonte %s." % video)
    envelope, referencia = medir_envelope(quadrados, np)
    if referencia <= 1e-6:
        falhar("o áudio da fonte está mudo: não há fala para medir.")
    duracao_audio = len(quadrados) * PASSO
    if abs(duracao_audio - (duracao_fonte - delta)) > 0.5:
        aviso("o audio16k.wav tem %s s e o vídeo %s s. Confira se a transcrição é deste vídeo."
              % (num(duracao_audio, 1), num(duracao_fonte, 1)))
    teto = duracao_audio   # o fecho não passa do fim do áudio nem do último quadro
    for limite in (duracao_fonte, flutuante((fluxo(sonda, "video") or {}).get("duration"))):
        if limite > 0:
            teto = min(teto, limite - delta)
    fala = Fala(palavras, envelope, referencia, referencia * op.limiar, teto, delta, op, np)
    silencio_total = float((envelope < fala.limiar).mean())
    if silencio_total < 0.03:
        aviso("quase não há silêncio abaixo do limiar (%d%% do áudio). Ruído de fundo ou música?\n"
              "         Poucas pausas vão ser achadas; teste --limiar 0.12." % round(100 * silencio_total))

    implicito = not op.trechos
    if implicito:
        trechos = [(palavras[0]["ini"] - 1e-3, palavras[-1]["fim"] + 1e-3)]
    else:
        trechos = ler_trechos(op.trechos)
        for a, b in trechos:
            if a >= fala.duracao:
                falhar("o trecho %s-%s começa depois do fim da fonte (%s s)." % (num(a), num(b), num(fala.duracao)))

    elementos, usadas = montar_elementos(fala, trechos, op)
    segmentos, juncoes = planejar(fala, elementos)

    # a conta do antes: cada trecho cortado só nas bordas, sem nada tirado de dentro (trechos
    # vizinhos na fonte que viraram um pedaço só contam uma vez)
    bordas = {}
    for s in segmentos:
        for t in s["trechos"]:
            a, b = bordas.get(t, (s["de"], s["ate"]))
            bordas[t] = (min(a, s["de"]), max(b, s["ate"]))
    antes_dur, fim_anterior = 0.0, None
    for a, b in sorted(bordas.values()):
        if fim_anterior is not None and a < fim_anterior:
            a = fim_anterior
        if b > a:
            antes_dur += b - a
        fim_anterior = b if fim_anterior is None else max(fim_anterior, b)
    antes_palavras = len(usadas)
    duracao_1x = sum(s["quadros"] for s in segmentos) / float(FPS)
    n_ficam = sum(1 for el in elementos if el["tipo"] == "palavra")
    velocidade, ritmo_1x = escolher_velocidade(op.velocidade, n_ficam, duracao_1x)
    duracao = duracao_1x / velocidade

    palavras_corte = remapear(fala, segmentos, velocidade)
    contagem = {}
    if regras:
        palavras_corte, contagem = aplicar_grafia(palavras_corte, regras)
    for p in palavras_corte:
        p["fim"] = min(p["fim"], round(duracao, 3))
        p["inicio"] = min(p["inicio"], p["fim"])

    # o que saiu da fonte: o complemento dos pedaços usados
    usados = sorted((s["de"], s["ate"]) for s in segmentos)
    uniao = []
    for a, b in usados:
        if uniao and a <= uniao[-1][1] + 1e-6:
            uniao[-1][1] = max(uniao[-1][1], b)
        else:
            uniao.append([a, b])
    removidos, cursor = [], 0.0
    buracos = []
    for a, b in uniao:
        if a - cursor > 1e-3:
            buracos.append((cursor, a))
        cursor = max(cursor, b)
    if fala.duracao - cursor > 1e-3:
        buracos.append((cursor, fala.duracao))
    for a, b in buracos:
        junc = next((j for j in juncoes if j["motivo"] != "fora-do-trecho"
                     and abs(j["saida"] - a) < 1e-3 and abs(j["entrada"] - b) < 1e-3), None)
        dentro = [p for p in palavras if a <= (p["ini"] + p["fim"]) / 2.0 < b]
        texto = " ".join(p["texto"] for p in dentro)
        if junc:
            item = {"de": a, "ate": b, "motivo": junc["motivo"], "texto": texto}
            if junc["pausa"]:
                item["pausa"] = junc["pausa"]
        else:
            motivo = "silencio" if implicito and not dentro else "fora-do-trecho"
            item = {"de": a, "ate": b, "motivo": motivo, "texto": texto}
        removidos.append(item)

    emendas = []
    for k, s in enumerate(segmentos):
        s["saida_de"] = s["saida_q"] / float(FPS) / velocidade
        s["saida_ate"] = (s["saida_q"] + s["quadros"]) / float(FPS) / velocidade
        if k:
            emendas.append(s["saida_de"])

    depois_ritmo = len(palavras_corte) / duracao if duracao else 0.0
    sugestao = None
    if velocidade == 1.0 and op.velocidade != "auto" and ritmo_1x <= PISO_RITMO:
        sugestao = ("%.2f" % escolher_velocidade("auto", n_ficam, duracao_1x)[0]).rstrip("0").rstrip(".")
    resolucao = "%sx%s" % ((fluxo(sonda, "video") or {}).get("width"), (fluxo(sonda, "video") or {}).get("height"))
    resumo = {
        "projeto": relativo(projeto, Path.cwd()), "corte": corte,
        "fonte": relativo(video, projeto), "duracao_fonte": duracao_fonte, "resolucao": resolucao,
        "duracao_audio": fala.duracao,
        "implicito": implicito,
        "trechos": [(segmentos[0]["de"], segmentos[-1]["ate"])] if implicito else trechos,
        "grafia": relativo(caminho_grafia, projeto) if caminho_grafia else None,
        "grafia_regras": len(regras), "grafia_trocas": contagem,
        "grafia_sem_uso": [r["original"] for r in regras if r["original"] not in contagem],
        "antes_dur": antes_dur, "antes_palavras": antes_palavras,
        "antes_ritmo": antes_palavras / antes_dur if antes_dur else 0.0,
        "depois_dur": duracao, "depois_palavras": len(palavras_corte), "depois_ritmo": depois_ritmo,
        "velocidade_txt": (("%.2f" % velocidade).rstrip("0").rstrip(".") if velocidade != 1.0 else "1.0")
                          + (" (auto)" if op.velocidade == "auto" else ""),
        "removidos": removidos, "suspeitas": fala.suspeitas, "emendas": emendas,
        "emendas_conferidas": None, "sugestao": sugestao, "problemas": [], "limiar_fracao": op.limiar,
    }

    edicao = {
        "fonte": relativo(video, projeto),
        "velocidade": velocidade,
        "duracao": round(duracao, 3),
        "segmentos": [{"de": round(s["de"], 3), "ate": round(s["ate"], 3),
                       "saida_de": round(s["saida_de"], 3), "saida_ate": round(s["saida_ate"], 3)}
                      for s in segmentos],
        "removidos": [{"de": round(x["de"], 3), "ate": round(x["ate"], 3), "motivo": x["motivo"], "texto": x["texto"]}
                      for x in removidos],
        "emendas": [round(t, 3) for t in emendas],
        "trechos": None if implicito else [{"de": a, "ate": b} for a, b in trechos],
        "parametros": {"pausa_max": op.pausa_max, "respiro": op.respiro, "limiar": op.limiar,
                       "hesitacao": not op.sem_hesitacao, "repeticao": not op.sem_repeticao,
                       "tipo_ne": op.remover_tipo_ne,
                       "grafia": relativo(caminho_grafia, projeto) if caminho_grafia else None},
        "suspeitas": fala.suspeitas,
    }
    pacote_palavras = {
        "palavras": palavras_corte,
        "meta": {"fonte": "fala.mp4", "duracao": round(duracao, 3), "velocidade": velocidade,
                 "grafia_aplicada": bool(regras)},
    }

    if op.ensaio:
        imprimir_resumo(resumo)
        print("  ensaio: nada foi gravado. %d pedaço(s), %d emenda(s)." % (len(segmentos), len(emendas)))
        print("")
        return 0

    pasta_corte.mkdir(parents=True, exist_ok=True)
    destino = pasta_corte / "fala.mp4"
    temporario = pasta_corte / ".fala-em-render.mp4"
    print("  renderizando %d pedaço(s) da fonte em %s ..." % (len(segmentos), relativo(destino, Path.cwd())))
    resultado, grupos = renderizar(video, segmentos, velocidade, delta, sonda, temporario, op.grafo_em_arquivo)
    if resultado.returncode != 0 or not temporario.is_file():
        temporario.unlink(missing_ok=True)
        erro("o ffmpeg parou. As últimas linhas dele:\n")
        print("\n".join(resultado.stderr.strip().splitlines()[-15:]), file=sys.stderr)
        if "libx264" in resultado.stderr:
            print("\n  O ffmpeg deste PATH não tem o libx264. Use o ffmpeg do pacote (instalar.sh).", file=sys.stderr)
        return 1
    temporario.replace(destino)

    info, problemas = conferir_arquivo(destino, duracao)
    conferidas = conferir_emendas(destino, emendas, referencia, fala.limiar, np)
    if conferidas is None:
        problemas.append("não consegui ler o áudio do fala.mp4 para conferir as emendas")
        conferidas = []
    edicao["emendas_suspeitas"] = [e for e in conferidas if e["em_som"]]

    (pasta_corte / "palavras-corte.json").write_text(
        json.dumps(pacote_palavras, ensure_ascii=False, indent=1), encoding="utf-8")
    (pasta_corte / "edicao.json").write_text(json.dumps(edicao, ensure_ascii=False, indent=1), encoding="utf-8")

    resumo["emendas_conferidas"] = conferidas
    resumo["problemas"] = problemas
    if info:
        resumo["resolucao_saida"] = "%sx%s" % (info["largura"], info["altura"])
    imprimir_resumo(resumo)
    print("  fala.mp4            %s  (%s, %s s, %d fps)" % (relativo(destino, Path.cwd()),
                                                            resumo.get("resolucao_saida", "?"),
                                                            num(info["duracao"] if info else 0, 3), FPS))
    print("  palavras-corte.json %s" % relativo(pasta_corte / "palavras-corte.json", Path.cwd()))
    print("  edicao.json         %s" % relativo(pasta_corte / "edicao.json", Path.cwd()))
    print("")
    ruins = [e for e in conferidas if e["em_som"]]
    if problemas or ruins:
        print("  OLHE: o fala.mp4 saiu, mas tem o que conferir antes de seguir.")
        print("")
        return 1
    print("  PRONTO")
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
