#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conferir_reel.py  ·  os gates automáticos do reel, antes de qualquer revisão

O motor 2.0 monta o reel inteiro sozinho, e a revisão humana é a etapa mais cara
do pacote: defeito que dá para medir e chega até ela custa uma volta inteira de
render e a paciência de quem revisa. Este script mede esses defeitos antes, lendo
os arquivos que as peças do motor já escrevem (motor/MOTOR.md, seções 1 a 3), e
devolve cada um com o instante em que acontece, que é onde se conserta.

Existe porque assistir uma vez não pega. Texto 20 px acima da zona segura,
legenda 6 px dentro do rosto, palavra acesa 120 ms antes da voz e emenda que come
meia sílaba passam batido no computador de quem produziu e aparecem no celular de
quem recebe. Tudo aqui é gratuito e local: numpy, pillow e ffmpeg/ffprobe.

Os doze gates (do 1 ao 9 da 2.0; do 10 ao 12 da 4.3, docs-4/gates-4-3.md):

  1 ritmo      lido no eventos.json, não no pixel: o rosto falando mexe o quadro
               inteiro e esconderia uma tela parada. Reprova trecho sem nenhum
               evento acima de 2,5 s (do começo ao fim do corte); abertura com
               menos de 3 momentos nos 5 primeiros segundos, ou sem evento de
               peso 2 ou 3 até 1,0 s; e duas recomposições (peso 3) a menos de
               1,5 s uma da outra, que não deixam o olho respirar. Eventos a até
               0,1 s um do outro são um momento só, a cena nova e a transição
               dela a até 0,5 s são a mesma recomposição, e a cena que abre o
               corte em t = 0 não conta: é o quadro inicial, não uma mudança.
  2 zonas      toda caixa de texto e de legenda do layout.jsonl dentro da zona
               segura (setup.json "zonas_seguras"; padrão y 220 a 1440 e 70 px
               das laterais). Quadros seguidos viram um intervalo de tempo. Os
               quadros no meio de uma transição (o layout marca "transicao")
               ficam de fora: ali o texto está de passagem, saindo ou entrando.
  3 contraste  a cor de cada texto contra o quadro renderizado sem texto, dentro
               da caixa dele, em luminância relativa da WCAG. Vale o pior caso
               realista: o contraste que 90% dos pixels do fundo superam
               (percentil 10), para um reflexo pequeno não reprovar e um fundo
               metade claro não passar. Texto de 48 px ou mais e em negrito pede
               3:1; o resto pede 4,5:1. A legenda tem contorno de 3 px em volta
               da letra; para ela vale o contraste da letra contra o contorno,
               que é o que a separa de qualquer fundo. Texto atrás de você
               ("atras": true, MOTOR.md 2.6): a pessoa cobre parte da caixa, e só
               conta o que ela não cobre, pela máscara daquele quadro
               (visao/mascara). E o texto que a pessoa esconde reprova: o
               layout.jsonl diz, quadro a quadro, quanto ela cobre de cada um, e
               mais de 35% coberto por 0,3 s seguidos é palavra sumida atrás da
               cabeça (a mesma régua com que o motor avisa).
  4 rosto      a caixa da legenda não cruza a caixa do rosto, com 8 px de folga,
               em nenhum quadro.
  5 sincronia  cada palavra do palavras-corte.json contra o início real do som
               no fala.mp4 a 16 kHz, numa janela de ±150 ms. Reprova com o p95
               do erro acima de 80 ms e lista as 5 piores.
  6 emendas    a energia do fala.mp4 nos 15 ms de cada lado de cada emenda do
               edicao.json, contra a fala plena (percentil 90 das janelas de 50
               ms, a régua do CORTE-LIMPO.md). Até 8% é silêncio; acima disso é
               aviso de possível sílaba comida; de 25% para cima a emenda caiu
               no meio da fala e reprova.
  7 volume     ebur128 do ffmpeg na entrega: -14 ±1 LUFS integrado e pico
               verdadeiro até -1 dBTP.
  8 efeitos    transições diferentes de "corte" por minuto, no cenas.json. Acima
               do teto (setup.json "gates.teto_transicoes_min", padrão 8) é só
               aviso, porque esse teto ainda vai ser calibrado.
  9 entrega    ffprobe na entrega: 1080x1920, 30 fps constante, h264, yuv420p,
               SAR 1:1, com áudio e com faststart (átomo moov antes do mdat). Se o
               plano usa imagem (campo "imagem" no cenas.json), o CREDITOS.md de
               materiais-de-trabalho/assets/ cita cada arquivo. E a pasta
               corte-NN/ tem o mp4 e mais nada.
 10 som        os efeitos sonoros que o audio.py tocou, lidos do sons.json que ele
               escreve (sem ele, numa entrega de antes da 4.3, a agenda é refeita
               pelo eventos.json). Reprova o defeito claro: um efeito a cada menos
               de 0,75 s no reel, 4 ou mais juntos, o mesmo arquivo em dois efeitos
               seguidos, efeito na sílaba tônica de palavra destacada com a voz a
               menos de 6 dB acima dele, e pico verdadeiro acima de -1 dBTP perto de
               um efeito (na entrega). É "olhe": mais de um a cada 1,5 s, 3 juntos,
               efeito na tônica que a voz ainda cobre, e sons.json mais velho que o
               eventos.json ou o fala.mp4.
 11 linguagem  com "linguagem" no cenas.json, a mesma conferência do linguagem.py
               conferir (a função é importada): o que ela reprova, este reprova; o
               que ela avisa, aqui é aviso. Sem "linguagem": não se aplica.
 13 mundo      só com cena no modo mundo (MOTOR.md 4.14). Reprova a câmera fora do
               modo (o mesmo fiscal do compor.py: mais de 7 chaves na calma, chave na
               parada, mais de um chicote, zoom acima de 1,40) e mais de um whoosh nas
               cenas de mundo. Avisa o rosto ampliado acima de 1,12x a gravação (do
               mundo.json que o compor.py grava), o rosto em cena em menos de dois
               terços do tempo de mundo, e lista os quadros-chave de
               conferencia-mundo/ para olhar em tamanho cheio (o objeto inteiro e
               legível em cada chave e em cada troca de superfície).
 12 variedade  só aviso, nunca reprova: sinais de template da pesquisa 04 (seção
               7). A mesma transição mais de 3 vezes seguidas, o mesmo efeito de
               palavra mais de 2 vezes seguidas, todas as cenas com a mesma duração
               (±10%), os momentos de peso 2 e 3 em metrônomo (variação dos
               intervalos abaixo de 35%), o mesmo arquivo de efeito mais de 4 vezes,
               e contra os reels anteriores (projetos/.historico-linguagens.json, ou
               as entregas que declaram linguagem): linguagem nos últimos 2, herói
               nos últimos 4, trilha nos últimos 8, e 50% ou mais dos traços iguais
               aos do anterior (Jaccard).

Como a sincronia é medida, porque é o gate mais fácil de errar. A régua ingênua
(o ataque de energia mais perto do tempo da palavra) não serve: a fala tem uma
sílaba nova a cada 100 a 200 ms, então qualquer instante tem um ataque perto, e
ela dava p95 de 120 ms numa legenda certa. A medida tem três camadas:

  ataques   o áudio é dividido em seis faixas de frequência e um ataque é uma
            subida rápida em qualquer uma delas. Pega o "s" que nasce depois de
            uma vogal (sobe nos agudos enquanto o total cai) e o "Ga" colado num
            "o" (degrau sem vale antes), que a energia total não vê.
  bloco     o deslocamento da legenda inteira sai da correlação de todas as
            palavras com os ataques; o de cada pedaço de até 10 s (dentro dos
            segmentos do edicao.json) sai da concordância entre os vãos das
            palavras e os silêncios reais, que são raros e nítidos. É o que pega
            legenda inteira deslocada, segmento com o tempo de antes da edição e
            deriva de velocidade, para os dois lados: palavra marcada depois do
            som, no meio de fala contínua, sempre acha uma sílaba perto e
            pareceria certa sozinha.
  palavra   cada palavra fica com o ataque, dentro da janela de ±150 ms, mais
            perto do seu tempo somado ao deslocamento do bloco, desde que esse
            ataque não esteja mais perto de outra palavra. Se o bloco está a
            mais de 150 ms, o erro é o do bloco. Palavra que começa em silêncio
            é erro de pelo menos 150 ms; palavra no meio de fala contínua sem
            ataque próprio fica sem medida.

Calibrado numa fala real de 43 s alinhada pelo WhisperX (165 palavras): p95 de
49 ms com os tempos certos; reprova deslocamento de 80 ms ou mais para qualquer
lado, segmento deslocado a partir de 100 ms, deriva de 0,5% e velocidade não
aplicada. Um deslocamento uniforme de 40 ms fica no limite (p95 de 80 ms).

Uso:

    flow-reels produzir/conferir_reel --projeto projetos/<video> --corte 01
    flow-reels produzir/conferir_reel --projeto projetos/<video> --corte 01 --so ritmo,zonas
    flow-reels produzir/conferir_reel --projeto projetos/<video> --corte 01 --json

--so       roda só os gates da lista: ritmo, zonas, contraste, rosto, sincronia,
           emendas, volume, efeitos, entrega, som, linguagem, variedade.
--json     imprime tudo estruturado, para outro script ler. No contraste, "pior"
           é o texto mais justo pela régua que decidiu cada um (o mesmo que o
           resumo chama de mais justo, ou o pior reprovado; null se todos
           passaram pelo contorno), e a legenda que só passou pelo contorno sai
           à parte, em "pior_pelo_contorno", com a letra contra o contorno.
--estrito  gate PULADO conta como reprovado. É o modo de quem libera o corte
           para a revisão: arquivo faltando é corte não conferido.

Lê da pasta do corte, projetos/<video>/materiais-de-trabalho/corte-NN/:
cenas.json, eventos.json, layout.jsonl, rosto.json (opcional), palavras-corte.json,
edicao.json, fala.mp4, contraste/ (os PNGs e o contraste.jsonl) e sons.json (do
audio.py 4.3; opcional). Lê a entrega em
projetos/<video>/corte-NN/corte-NN.mp4 e o setup.json da raiz do pacote.

O veredito do fim é PASSOU, PASSOU COM AVISOS, INCOMPLETO (algum gate pulado),
NADA CONFERIDO (todos pulados) ou REPROVADO. Gate que não se aplica ao corte (o
11 sem linguagem no plano) sai como N/A e não conta para nada: nem pulado, nem
passou ("PASSOU · os 11 gates passaram; não se aplica: linguagem"). No --json o
status dele é "NÃO SE APLICA" e a contagem ganha essa chave.

Saída 0 = passou (aviso e pulado não bloqueiam, a não ser com --estrito).
Saída 1 = reprovou, com os instantes. Saída 2 = erro de uso.
"""

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# ----------------------------------------------------------------- números

LARGURA = 1080
ALTURA = 1920
FPS = 30

# 1 ritmo
PARADO_MAX = 2.5            # maior trecho sem evento, em segundos
ABERTURA_JANELA = 5.0       # os primeiros segundos que são o trailer do corte
ABERTURA_MIN_MOMENTOS = 3   # momentos mínimos dentro dessa janela
ABERTURA_PESO2_ATE = 1.0    # até quando um elemento grande precisa ter entrado
RESPIRO_MIN = 1.5           # distância mínima entre duas recomposições
JUNTA_MOMENTO = 0.1         # eventos a até 3 quadros um do outro são um momento só
JUNTA_RECOMPOSICAO = 0.5    # cena nova e a transição dela são uma recomposição só
INICIAL = 0.05              # a cena que começa antes disso é o quadro inicial

# 2 zonas
ZONAS_PADRAO = {"topo": 220, "base": 1440, "lateral": 70}

# 3 contraste
CONTRASTE_GRANDE = 3.0      # texto de 48 px ou mais, em negrito
CONTRASTE_NORMAL = 4.5      # o resto
TAMANHO_GRANDE = 48
PERCENTIL_PIOR = 10         # o contraste que 90% dos pixels do fundo superam
# texto atrás de você (MOTOR.md 3): a mesma régua do motor (Motor.ATRAS). A base da letra encostando na
# cabeça cobre uns 10 a 25% da caixa da palavra; acima de 35% por 0,3 s a palavra já não se lê
ATRAS_LIMIAR = 0.35
ATRAS_MIN_S = 0.3

# 4 legenda x rosto
FOLGA_ROSTO = 8
MODOS_COM_ROSTO = {"painel-rosto", "rosto-vidro", "tela-bolha", "manchete", "vidro-liquido"}

# 5 sincronia
SR = 16000
JANELA_SINC = 0.150         # o início real do som é procurado a ±150 ms da palavra
P95_MAX = 0.080
PASSO = 0.005               # passo do envelope
JANELA_FFT = 0.020          # janela de cada medida
BANDAS = [(80, 300), (300, 700), (700, 1500), (1500, 3000), (3000, 5000), (5000, 7900)]
PISO_BANDA = 45.0           # dB abaixo do nível da faixa onde a medida para de descer
AUDIVEL_BANDA = 30.0        # subida que termina abaixo disso, na faixa, não é som
ATRAS = 4                   # a subida é medida contra os 20 ms anteriores
FORCA_MIN = 15.0            # soma das subidas das faixas, em dB, para virar ataque
RAIO_PICO = 3               # quadros de envelope de cada lado para ser pico
RECUO = 0.5                 # do pico da subida, volta até onde ela tem metade da força
RECUO_MAX = 6               # e no máximo 30 ms
LAGS_MAX = 0.6              # deslocamento em bloco procurado, para cada lado
SIGMA_LAG = 0.015
CONFIANCA_LAG = 1.2         # o deslocamento global precisa bater o zero por 20%
TRECHO_MAX = 10.0           # pedaço de medida do deslocamento de trecho
TRECHO_MIN_PALAVRAS = 8
GANHO_TRECHO = 0.03         # o trecho só tem deslocamento próprio se ele concorda 3 pontos mais
AVISO_LAG = 0.040           # deslocamento em bloco a partir disso entra no relatório
SILENCIO_FRACAO = 0.08      # CORTE-LIMPO.md: abaixo de 8% da fala plena é silêncio

# 6 emendas
EMENDA_MEIA = 0.015
EMENDA_REPROVA = 0.25       # 25% da fala plena, cerca de -12 dB: é fala, não pausa

# 7 volume
LUFS_ALVO = -14.0
LUFS_TOLERANCIA = 1.0
PICO_MAX = -1.0

# 8 efeitos
TETO_TRANSICOES_PADRAO = 8.0

# 10 som (4.3)
DENSIDADE_OLHE = 1.5        # um efeito a cada 1,5 s no reel inteiro (pesquisa 04, 4.2): abaixo disso, olhe
DENSIDADE_REPROVA = 0.75    # um a cada 0,75 s (o dobro do teto) já é som em tudo: reprova
JUNTOS_OLHE = 2             # mais de 2 efeitos soando ao mesmo tempo: olhe
JUNTOS_REPROVA = 4          # 4 ou mais juntos é embolado: reprova
FOLGA_TONICA = 6.0          # efeito a menos de 6 dB da voz em cima da tônica de palavra destacada: mascara, reprova
JANELA_PICO = 0.05          # o pico de cada efeito é medido do começo ao fim dele, com 50 ms de cada lado
SOBRE_AMOSTRA = 4           # pico verdadeiro: 4x a taxa (192 kHz), como o ebur128

# 12 variedade (4.3): só avisa
TRANSICAO_SEGUIDA_MAX = 3   # a mesma transição mais de 3 vezes seguidas
PALAVRA_SEGUIDA_MAX = 2     # o mesmo efeito de palavra mais de 2 vezes seguidas
CV_METRONOMO = 0.35         # desvio-padrão dos intervalos abaixo de 35% da média: efeito em metrônomo
DURACAO_IGUAL = 0.10        # todas as cenas com a mesma duração, ±10%
CENAS_MIN_IGUAL = 4         # (com pelo menos 4 cenas)
JACCARD_MAX = 0.5           # traços do reel contra o anterior: 0,5 ou mais é a mesma cara
ARQUIVO_REPETE_MAX = 4      # o mesmo arquivo de efeito mais de 4 vezes no reel (o ouvido reconhece em 3)
MEMORIA = {"linguagem": 2, "heroi": 4, "trilha": 8}   # não repetir nos últimos N reels (linguagens.json)

GATES = ["ritmo", "zonas", "contraste", "rosto", "sincronia", "emendas", "volume", "efeitos", "entrega",
         "som", "linguagem", "variedade", "mundo"]
TITULOS = {
    "ritmo": "ritmo",
    "zonas": "zonas seguras",
    "contraste": "contraste",
    "rosto": "legenda x rosto",
    "sincronia": "sincronia",
    "emendas": "emendas",
    "volume": "volume",
    "efeitos": "excesso de efeito",
    "entrega": "entrega",
    "som": "efeitos sonoros",
    "linguagem": "linguagem",
    "variedade": "variedade",
    "mundo": "modo mundo",
}
APELIDOS = {
    "legenda-rosto": "rosto", "colisao": "rosto", "colisão": "rosto",
    "zona": "zonas", "sinc": "sincronia", "emenda": "emendas", "loudness": "volume",
    "efeito": "efeitos", "excesso": "efeitos", "transicoes": "efeitos", "transições": "efeitos",
    "formato": "entrega",
    "sfx": "som", "sons": "som", "efeitos-sonoros": "som",
    "lingua": "linguagem", "template": "variedade", "repeticao": "variedade", "repetição": "variedade",
}


def erro(msg):
    print("  erro: " + msg, file=sys.stderr)


def carregar_numpy():
    try:
        import numpy
    except ImportError:
        erro("o numpy não está instalado neste Python.\n"
             "       Rode com o Python do pacote: .venv/bin/python, ou instale com: pip install numpy")
        sys.exit(2)
    return numpy


def exigir(ferramenta):
    if shutil.which(ferramenta) is None:
        erro("%s não encontrado no PATH. Rode o instalar.sh na raiz do pacote." % ferramenta)
        sys.exit(2)


# ----------------------------------------------------------------- formatos

def seg(t):
    return "%.2f s" % t


def num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return f


def caixa_de(v):
    """[x, y, w, h] ou {"caixa": [...]} ou {"x":..,"y":..,"w":..,"h":..}. None se não for caixa."""
    if isinstance(v, dict):
        if "caixa" in v:
            return caixa_de(v["caixa"])
        if all(k in v for k in ("x", "y", "w", "h")):
            return caixa_de([v["x"], v["y"], v["w"], v["h"]])
        return None
    if isinstance(v, (list, tuple)) and len(v) >= 4:
        x, y, w, h = (num(a) for a in v[:4])
        if None in (x, y, w, h) or w <= 0 or h <= 0:
            return None
        return (x, y, w, h)
    return None


def cor_de(v):
    """[r, g, b], [r, g, b, a], "#rrggbb", "#rrggbbaa", "rgb(...)" ou "rgba(...)" -> (r, g, b, a)."""
    if isinstance(v, (list, tuple)) and len(v) >= 3:
        r, g, b = (num(a) for a in v[:3])
        if None in (r, g, b):
            return None
        a = num(v[3]) if len(v) >= 4 else 1.0
        if a is None:
            a = 1.0
        if a > 1.0:
            a = a / 255.0
        return (r, g, b, max(0.0, min(1.0, a)))
    if isinstance(v, str):
        s = v.strip().lower()
        m = re.fullmatch(r"#([0-9a-f]{6})([0-9a-f]{2})?", s)
        if m:
            h = m.group(1)
            a = int(m.group(2), 16) / 255.0 if m.group(2) else 1.0
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)
        m = re.fullmatch(r"#([0-9a-f]{3})", s)
        if m:
            h = m.group(1)
            return (int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16), 1.0)
        m = re.fullmatch(r"rgba?\(([^)]*)\)", s)
        if m:
            partes = [p.strip() for p in re.split(r"[,\s/]+", m.group(1)) if p.strip()]
            if len(partes) >= 3:
                try:
                    r, g, b = (float(p) for p in partes[:3])
                    a = float(partes[3].rstrip("%")) / (100.0 if partes[3].endswith("%") else 1.0) \
                        if len(partes) >= 4 else 1.0
                    return (r, g, b, max(0.0, min(1.0, a)))
                except ValueError:
                    return None
    return None


def resumir_erro(texto, caminho=None):
    """Uma linha do erro do ffmpeg, sem o prefixo [demuxer @ 0x...] e sem o caminho inteiro."""
    linhas = []
    for linha in texto.strip().splitlines():
        linha = re.sub(r"^\[[^\]]*@ 0x[0-9a-f]+\]\s*", "", linha.strip())
        if caminho is not None:
            linha = linha.replace(str(caminho) + ": ", "").replace(str(caminho), Path(caminho).name)
        if linha and linha not in linhas:
            linhas.append(linha)
    return "; ".join(linhas)[:240]


def hexa(cor):
    return "#%02x%02x%02x" % tuple(int(round(max(0, min(255, c)))) for c in cor[:3])


def intervalos(itens, chave, fps):
    """Agrupa quadros seguidos com a mesma chave. itens: dicts com i (ou None), t, e o que mais vier."""
    grupos = {}
    abertos = {}
    for it in sorted(itens, key=lambda d: d["t"]):
        k = chave(it)
        g = abertos.get(k)
        seguido = False
        if g is not None:
            if it.get("i") is not None and g["ultimo_i"] is not None:
                seguido = it["i"] - g["ultimo_i"] <= 1
            else:
                seguido = it["t"] - g["ate_t"] <= 1.5 / fps
        if seguido:
            g["ate_t"] = it["t"]
            g["ultimo_i"] = it.get("i")
            g["itens"].append(it)
        else:
            g = {"de": it["t"], "ate_t": it["t"], "ultimo_i": it.get("i"), "itens": [it], "chave": k}
            abertos[k] = g
            grupos.setdefault(k, []).append(g)
    saida = []
    for lista in grupos.values():
        for g in lista:
            g["ate"] = g["ate_t"] + 1.0 / fps
            saida.append(g)
    return sorted(saida, key=lambda g: (g["de"], str(g["chave"])))


# ----------------------------------------------------------------- o corte

class Corte:
    """Os caminhos de um corte e a leitura preguiçosa dos arquivos dele."""

    def __init__(self, projeto, nome, raiz):
        self.projeto = projeto
        self.nome = nome
        self.raiz = raiz
        self.pasta = projeto / "materiais-de-trabalho" / nome
        self.pasta_entrega = projeto / nome
        self.entrega = self.pasta_entrega / (nome + ".mp4")
        self._cache = {}
        self.setup = {}
        self.setup_erro = None
        if raiz is not None:
            dados, falha = self._ler_json_caminho(raiz / "setup.json")
            if falha:
                self.setup_erro = falha
            elif isinstance(dados, dict):
                self.setup = dados

    def mostrar(self, caminho):
        for base in (self.raiz, Path.cwd()):
            if base is None:
                continue
            try:
                return str(Path(caminho).resolve().relative_to(base.resolve()))
            except ValueError:
                continue
        return str(caminho)

    @staticmethod
    def _ler_json_caminho(caminho):
        try:
            return json.loads(Path(caminho).read_text(encoding="utf-8")), None
        except UnicodeDecodeError:
            return None, "não está em UTF-8"
        except json.JSONDecodeError as e:
            return None, "não é um JSON válido (linha %d, coluna %d: %s)" % (e.lineno, e.colno, e.msg)
        except OSError as e:
            return None, "não consegui abrir (%s)" % e.strerror

    def json(self, nome):
        """(dados, problema). problema = None, "faltando" ou a frase do defeito."""
        if nome in self._cache:
            return self._cache[nome]
        caminho = self.pasta / nome
        if not caminho.is_file():
            r = (None, "faltando")
        else:
            dados, falha = self._ler_json_caminho(caminho)
            # os tempos presos à palavra ({"ancora": ...}) viram segundos, como no compor.py
            if nome == "cenas.json" and isinstance(dados, dict) and not falha:
                dados = self._resolver_ancoras(dados)
            r = (dados, falha)
        self._cache[nome] = r
        return r

    def _resolver_ancoras(self, cenas):
        try:
            motor = str(Path(__file__).resolve().parents[1] / "motor")
            if motor not in sys.path:
                sys.path.insert(0, motor)
            import ancoras
        except ImportError:
            return cenas
        palavras, _ = self.json("palavras-corte.json")
        fps = num(cenas.get("fps")) or FPS
        plano, _, _ = ancoras.resolver_ancoras(cenas, palavras if isinstance(palavras, dict) else {}, int(fps))
        return plano

    def layout(self):
        """(linhas, ruins, problema)."""
        if "layout" in self._cache:
            return self._cache["layout"]
        caminho = self.pasta / "layout.jsonl"
        if not caminho.is_file():
            r = (None, 0, "faltando")
        else:
            linhas, ruins = [], 0
            try:
                with open(caminho, encoding="utf-8") as f:
                    for bruta in f:
                        bruta = bruta.strip()
                        if not bruta:
                            continue
                        try:
                            d = json.loads(bruta)
                        except json.JSONDecodeError:
                            ruins += 1
                            continue
                        if isinstance(d, dict):
                            linhas.append(d)
                        else:
                            ruins += 1
                r = (linhas, ruins, None)
            except (OSError, UnicodeDecodeError) as e:
                r = (None, 0, "não consegui ler (%s)" % e)
        self._cache["layout"] = r
        return r

    def fps(self):
        cenas, _ = self.json("cenas.json")
        if isinstance(cenas, dict):
            f = num(cenas.get("fps"))
            if f and f > 0:
                return f
        return float(FPS)

    def duracao_plano(self):
        for nome in ("eventos.json", "cenas.json", "edicao.json"):
            d, _ = self.json(nome)
            if isinstance(d, dict):
                v = num(d.get("duracao"))
                if v and v > 0:
                    return v
        d, _ = self.json("palavras-corte.json")
        if isinstance(d, dict) and isinstance(d.get("meta"), dict):
            v = num(d["meta"].get("duracao"))
            if v and v > 0:
                return v
        return None

    def audio(self, np):
        """(amostras mono 16 kHz, problema)."""
        if "audio" in self._cache:
            return self._cache["audio"]
        caminho = self.pasta / "fala.mp4"
        if not caminho.is_file():
            r = (None, "faltando")
        else:
            cmd = ["ffmpeg", "-v", "error", "-i", str(caminho), "-vn", "-ac", "1", "-ar", str(SR),
                   "-f", "f32le", "-"]
            proc = subprocess.run(cmd, capture_output=True)
            if proc.returncode != 0 or len(proc.stdout) < 4 * SR // 10:
                msg = proc.stderr.decode("utf-8", "ignore")
                if "does not contain any stream" in msg or (proc.returncode == 0 and not proc.stdout):
                    r = (None, "o fala.mp4 não tem faixa de áudio")
                elif proc.returncode == 0:
                    r = (None, "o fala.mp4 tem menos de 0,1 s de áudio")
                else:
                    r = (None, "o ffmpeg não leu o áudio do fala.mp4: " + resumir_erro(msg, caminho))
            else:
                n = len(proc.stdout) // 4
                r = (np.frombuffer(proc.stdout[: n * 4], np.float32).astype(np.float64), None)
        self._cache["audio"] = r
        return r

    def sondar_entrega(self):
        if "sonda" in self._cache:
            return self._cache["sonda"]
        cmd = ["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format",
               str(self.entrega)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            r = (None, resumir_erro(proc.stderr or "", self.entrega) or "o ffprobe falhou")
        else:
            try:
                r = (json.loads(proc.stdout), None)
            except json.JSONDecodeError:
                r = (None, "o ffprobe devolveu uma saída que não entendi")
        self._cache["sonda"] = r
        return r


class Gate:
    def __init__(self, chave):
        self.chave = chave
        self.titulo = TITULOS[chave]
        self.status = "PASSOU"
        self.resumo = ""
        self.linhas = []      # detalhe para gente, já com os instantes
        self.conserto = []
        self.dados = {}       # o mesmo detalhe, estruturado, para o --json

    def pular(self, motivo, faltando=None):
        self.status = "PULADO"
        self.resumo = motivo
        if faltando:
            self.dados["faltando"] = faltando
        return self

    def reprovar(self):
        self.status = "REPROVOU"

    def avisar(self):
        if self.status == "PASSOU":
            self.status = "AVISO"

    def nao_se_aplica(self, motivo):
        """O gate não vale para este corte (ex.: plano sem linguagem). Não bloqueia nem conta como pulado."""
        self.status = "NÃO SE APLICA"
        self.resumo = motivo
        return self

    def como_dict(self):
        d = {"titulo": self.titulo, "status": self.status, "resumo": self.resumo}
        d.update(self.dados)
        if self.linhas:
            d["detalhe"] = self.linhas
        if self.conserto:
            d["conserto"] = " ".join(self.conserto)
        return d


def faltou(c, g, nome, papel):
    """Marca o gate como pulado por arquivo faltando, ou reprovado por arquivo ilegível."""
    _, problema = c.json(nome)
    if problema == "faltando":
        g.pular("faltou %s (%s)" % (nome, papel), [c.mostrar(c.pasta / nome)])
    else:
        g.reprovar()
        g.resumo = "o %s %s" % (nome, problema)
        g.conserto.append("Quem escreve esse arquivo é a peça indicada no MOTOR.md seção 1; gere de novo.")
    return g


# ----------------------------------------------------------------- 1 ritmo

def gate_ritmo(c, np):
    g = Gate("ritmo")
    dados, problema = c.json("eventos.json")
    if problema:
        return faltou(c, g, "eventos.json", "o compor.py escreve")
    if not isinstance(dados, dict):
        g.reprovar()
        g.resumo = "o eventos.json não tem o formato do MOTOR.md 2.4"
        return g

    brutos = dados.get("eventos") if isinstance(dados.get("eventos"), list) else []
    eventos, ignorados = [], 0
    for e in brutos:
        t = num(e.get("t")) if isinstance(e, dict) else None
        if t is None:
            ignorados += 1
            continue
        peso = num(e.get("peso"))
        eventos.append({"t": t, "tipo": str(e.get("tipo") or "?"), "peso": int(peso) if peso else 1,
                        "alvo": e.get("alvo")})
    eventos.sort(key=lambda e: e["t"])

    duracao = num(dados.get("duracao")) or c.duracao_plano()
    if not duracao:
        duracao = eventos[-1]["t"] if eventos else 0.0
        g.linhas.append("o eventos.json não traz a duração; o fim do último trecho ficou no último evento")
    fora = [e for e in eventos if e["t"] < 0 or e["t"] > duracao + 0.01]
    if ignorados or fora:
        g.linhas.append("%d evento(s) sem tempo e %d fora de 0 a %.2f s foram ignorados"
                        % (ignorados, len(fora), duracao))
    eventos = [e for e in eventos if 0 <= e["t"] <= duracao + 0.01]

    def descreve(e):
        alvo = (" " + str(e["alvo"])) if e.get("alvo") not in (None, "") else ""
        return "%s%s (peso %d) em %s" % (e["tipo"], alvo, e["peso"], seg(e["t"]))

    # parado: do começo ao primeiro evento, entre eventos, e do último ao fim
    marcos = [0.0] + [e["t"] for e in eventos] + [duracao]
    paradas = []
    for a, b in zip(marcos, marcos[1:]):
        if b - a > PARADO_MAX:
            antes = [e for e in eventos if e["t"] <= a + 1e-6]
            paradas.append({"de": round(a, 3), "ate": round(b, 3), "dura": round(b - a, 3),
                            "depois_de": descreve(antes[-1]) if antes else None})
    maior = max((b - a for a, b in zip(marcos, marcos[1:])), default=duracao)

    # abertura: a cena que abre o corte em t = 0 é o quadro inicial, não acontecimento
    def inicial(e):
        return e["tipo"] == "cena" and e["t"] < INICIAL

    validos = [e for e in eventos if not inicial(e)]
    momentos = []
    for e in validos:
        if momentos and e["t"] - momentos[-1][-1]["t"] <= JUNTA_MOMENTO:
            momentos[-1].append(e)
        else:
            momentos.append([e])
    momentos_5s = [m for m in momentos if m[0]["t"] < ABERTURA_JANELA]
    grandes = [e for e in validos if e["peso"] >= 2 and e["t"] <= ABERTURA_PESO2_ATE]
    abertura = []
    if len(momentos_5s) < ABERTURA_MIN_MOMENTOS:
        abertura.append("só %d momento(s) nos %.0f primeiros segundos%s; o piso é %d"
                        % (len(momentos_5s), ABERTURA_JANELA,
                           (" (" + ", ".join(seg(m[0]["t"]) for m in momentos_5s) + ")") if momentos_5s else "",
                           ABERTURA_MIN_MOMENTOS))
    if not grandes:
        primeiro = next((e for e in validos if e["peso"] >= 2), None)
        abertura.append("nenhum evento de peso 2 ou 3 até %.1f s%s"
                        % (ABERTURA_PESO2_ATE,
                           ("; o primeiro é " + descreve(primeiro)) if primeiro else "; não há nenhum no corte"))

    # respiro: recomposições de peso 3; a cena nova e a transição dela são uma só
    recomp = []
    for e in (e for e in validos if e["peso"] >= 3):
        g_atual = recomp[-1] if recomp else None
        if (g_atual is not None and e["t"] - g_atual[0]["t"] <= JUNTA_RECOMPOSICAO
                and e["tipo"] not in {x["tipo"] for x in g_atual}):
            g_atual.append(e)
        else:
            recomp.append([e])

    def instante(grupo):
        cena = [x for x in grupo if x["tipo"] == "cena"]
        return (cena[0] if cena else grupo[0])["t"]

    def nomes(grupo):
        return ", ".join(x["tipo"] + (" " + str(x["alvo"]) if x.get("alvo") else "") for x in grupo)

    tempos_recomp = [instante(gr) for gr in recomp]
    pares = list(zip(recomp, tempos_recomp))
    colados = []
    for (ga, ta), (gb, tb) in zip(pares, pares[1:]):
        if tb - ta < RESPIRO_MIN:
            colados.append({"de": round(ta, 3), "ate": round(tb, 3), "distancia": round(tb - ta, 3),
                            "primeira": nomes(ga), "segunda": nomes(gb)})
    menor_respiro = min((b - a for a, b in zip(tempos_recomp, tempos_recomp[1:])), default=None)

    g.dados.update({
        "duracao": round(duracao, 3), "eventos": len(eventos), "momentos": len(momentos),
        "maior_trecho_sem_evento": round(maior, 3), "paradas_acima_do_limite": paradas,
        "momentos_nos_5s": len(momentos_5s), "abertura": abertura,
        "recomposicoes": [round(t, 3) for t in tempos_recomp],
        "recomposicoes_coladas": colados,
        "limites": {"parado_max": PARADO_MAX, "abertura_momentos": ABERTURA_MIN_MOMENTOS,
                    "abertura_peso2_ate": ABERTURA_PESO2_ATE, "respiro_min": RESPIRO_MIN},
    })

    if paradas:
        g.reprovar()
        g.linhas.append("trecho sem evento acima de %.1f s:" % PARADO_MAX)
        for p in paradas:
            g.linhas.append("  %s a %s  ·  %.2f s sem evento%s"
                            % (seg(p["de"]), seg(p["ate"]), p["dura"],
                               ("  ·  depois de " + p["depois_de"]) if p["depois_de"] else "  ·  desde o início"))
        g.conserto.append("Dê um acontecimento a cada trecho parado no cenas.json, no próximo ponto-chave "
                          "da fala: um elemento entra, um número conta, uma parte acende, a câmera aproxima.")
    if abertura:
        g.reprovar()
        g.linhas.append("abertura fraca:")
        for a in abertura:
            g.linhas.append("  " + a)
        g.conserto.append("O primeiro segundo precisa de um elemento grande entrando (peso 2 ou 3), e os 5 "
                          "primeiros segundos de pelo menos 3 momentos: a abertura é o trailer do corte.")
    if colados:
        g.reprovar()
        g.linhas.append("recomposições sem respiro (menos de %.1f s entre elas):" % RESPIRO_MIN)
        for p in colados:
            g.linhas.append("  %s e %s  ·  %.2f s  ·  %s, depois %s"
                            % (seg(p["de"]), seg(p["ate"]), p["distancia"], p["primeira"], p["segunda"]))
        g.conserto.append("Afaste as duas recomposições ou troque uma delas por uma mudança menor "
                          "(peso 1 ou 2) dentro da mesma cena.")

    partes = ["maior trecho sem evento %.2f s" % maior,
              "%d momento(s) nos 5 primeiros s" % len(momentos_5s)]
    if menor_respiro is not None:
        partes.append("menor respiro entre recomposições %.2f s" % menor_respiro)
    g.resumo = "; ".join(partes)
    return g


# ----------------------------------------------------------------- 2 zonas

def zonas_do_setup(c):
    z = dict(ZONAS_PADRAO)
    do_setup = c.setup.get("zonas_seguras") if isinstance(c.setup, dict) else None
    if isinstance(do_setup, dict):
        for k in z:
            v = num(do_setup.get(k))
            if v is not None:
                z[k] = v
    return z


def textos_da_linha(linha):
    """[(rotulo, caixa)] dos textos e da legenda de uma linha do layout."""
    saida = []
    textos = linha.get("textos")
    if isinstance(textos, list):
        for item in textos:
            cx = caixa_de(item)
            if cx:
                nome = None
                if isinstance(item, dict):
                    nome = item.get("id") or item.get("alvo") or item.get("texto")
                saida.append(("texto" + ((" " + str(nome)) if nome else ""), cx))
    cx = caixa_de(linha.get("legenda"))
    if cx:
        saida.append(("legenda", cx))
    return saida


def gate_zonas(c, np):
    g = Gate("zonas")
    linhas, ruins, problema = c.layout()
    if problema == "faltando":
        return g.pular("faltou layout.jsonl (o compor.py escreve)", [c.mostrar(c.pasta / "layout.jsonl")])
    if problema:
        g.reprovar()
        g.resumo = "o layout.jsonl " + problema
        return g
    if not linhas:
        g.reprovar()
        g.resumo = "o layout.jsonl não tem nenhuma linha legível"
        return g

    z = zonas_do_setup(c)
    fps = c.fps()
    x0, y0, x1, y1 = z["lateral"], z["topo"], LARGURA - z["lateral"], z["base"]
    violacoes = []
    caixas = em_transicao = 0
    for linha in linhas:
        t = num(linha.get("t"))
        i = linha.get("i") if isinstance(linha.get("i"), int) else None
        if t is None:
            if i is None:
                continue
            t = i / fps
        if linha.get("transicao") is True:
            em_transicao += 1
            continue
        for rotulo, (x, y, w, h) in textos_da_linha(linha):
            caixas += 1
            lados = []
            if y < y0:
                lados.append(("acima do topo", y0 - y, "y %d, limite %d" % (round(y), y0)))
            if y + h > y1:
                lados.append(("abaixo da base", y + h - y1, "vai até y %d, limite %d" % (round(y + h), y1)))
            if x < x0:
                lados.append(("fora da margem esquerda", x0 - x, "x %d, limite %d" % (round(x), x0)))
            if x + w > x1:
                lados.append(("fora da margem direita", x + w - x1, "vai até x %d, limite %d" % (round(x + w), x1)))
            for lado, excesso, onde in lados:
                tipo = "legenda" if rotulo == "legenda" else rotulo
                violacoes.append({"t": t, "i": i, "tipo": tipo, "lado": lado, "excesso": excesso,
                                  "onde": onde, "caixa": [round(v) for v in (x, y, w, h)],
                                  "cena": linha.get("cena")})

    grupos = intervalos(violacoes, lambda v: (v["tipo"], v["lado"]), fps)
    trechos = []
    for gr in grupos:
        pior = max(gr["itens"], key=lambda v: v["excesso"])
        cenas = sorted({str(v["cena"]) for v in gr["itens"] if v.get("cena")})
        trechos.append({"de": round(gr["de"], 3), "ate": round(gr["ate"], 3),
                        "quadros": len({v["t"] for v in gr["itens"]}),
                        "tipo": gr["chave"][0], "lado": gr["chave"][1], "excesso_px": round(pior["excesso"]),
                        "onde": pior["onde"], "caixa": pior["caixa"], "cenas": cenas})

    g.dados.update({"zona": {"x": [x0, x1], "y": [y0, y1]}, "quadros": len(linhas),
                    "quadros_em_transicao": em_transicao,
                    "caixas_conferidas": caixas, "linhas_ilegiveis": ruins, "fora_da_zona": trechos})
    if ruins:
        g.linhas.append("%d linha(s) ilegível(is) no layout.jsonl foram puladas" % ruins)
    if trechos:
        g.reprovar()
        g.resumo = "%d trecho(s) com texto fora da zona segura (x %d a %d, y %d a %d)" % (
            len(trechos), x0, x1, y0, y1)
        for tr in trechos:
            g.linhas.append("%s a %s  ·  %s %s: %s, %d px além  ·  %d quadro(s)%s"
                            % (seg(tr["de"]), seg(tr["ate"]), tr["tipo"], tr["lado"], tr["onde"],
                               tr["excesso_px"], tr["quadros"],
                               ("  ·  cena " + ", ".join(tr["cenas"])) if tr["cenas"] else ""))
        g.conserto.append("Texto e logo moram entre y %d e y %d e a %d px das laterais (MOTOR.md seção 4). "
                          "Suba, desça ou estreite o elemento na cena indicada; rosto e imagem podem "
                          "ocupar o quadro todo, texto não." % (y0, y1, x0))
    else:
        g.resumo = "%d caixas em %d quadros, todas entre x %d e %d e y %d e %d" % (
            caixas, len(linhas) - em_transicao, x0, x1, y0, y1)
        if em_transicao:
            g.resumo += " (%d quadros de transição não contam)" % em_transicao
    return g


# ----------------------------------------------------------------- 3 contraste

def luminancia(rgb, np):
    """Luminância relativa da WCAG, de sRGB 0 a 255."""
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722


def fora_da_pessoa(c, recorte, xa, ya, xb, yb, passo, ex, ey, cache, np, Image):
    """Na grade de pixels medidos da caixa de um texto atrás de você, onde a pessoa NÃO cobre: True =
    a letra aparece ali. O motor manda o quadro da máscara (0 = o primeiro) e onde a imagem do recorte
    e a janela dele estão na tela; a máscara (visao/mascara/m%06d.png, branco = pessoa) é esticada
    sobre a imagem, como no motor, e só vale dentro da janela. Sem recorte na tela, None: o texto é
    medido inteiro, como os outros."""
    if not isinstance(recorte, dict):
        return None
    q = recorte.get("quadro")
    img = caixa_de(recorte.get("imagem"))
    jan = caixa_de(recorte.get("janela"))
    if not isinstance(q, int) or not img or not jan or img[2] <= 0 or img[3] <= 0:
        return None
    caminho = c.pasta / "visao" / "mascara" / ("m%06d.png" % (q + 1))
    if caminho not in cache:
        try:
            with Image.open(caminho) as im:
                cache.clear()   # uma máscara por vez na memória
                cache[caminho] = np.asarray(im.convert("L"))
        except (OSError, ValueError):
            cache[caminho] = None
    m = cache.get(caminho)
    if m is None:
        return None
    mh, mw = m.shape
    xs = (np.arange(xa, xb, passo) + 0.5) / ex      # o centro de cada pixel medido, em pixels de saída
    ys = (np.arange(ya, yb, passo) + 0.5) / ey
    mx = np.clip(((xs - img[0]) / img[2] * mw).astype(int), 0, mw - 1)
    my = np.clip(((ys - img[1]) / img[3] * mh).astype(int), 0, mh - 1)
    dentro_x = (xs >= jan[0]) & (xs < jan[0] + jan[2]) & (xs >= img[0]) & (xs < img[0] + img[2])
    dentro_y = (ys >= jan[1]) & (ys < jan[1] + jan[3]) & (ys >= img[1]) & (ys < img[1] + img[3])
    pessoa = (m[my[:, None], mx[None, :]] >= 128) & dentro_y[:, None] & dentro_x[None, :]
    return ~pessoa


def textos_escondidos(linhas, fps):
    """As corridas de quadros seguidos em que a pessoa cobre mais que ATRAS_LIMIAR de um texto atrás
    dela (o motor escreve "atras" no layout.jsonl: id, peca, texto, caixa, coberto, topo). Quadro de
    transição interrompe a corrida: ali o texto está de passagem. Devolve as que duram ATRAS_MIN_S ou
    mais, com o pior quadro."""
    minimo = max(1, int(math.ceil(ATRAS_MIN_S * fps - 1e-9)))
    abertas, fechadas = {}, []
    anterior = None
    for linha in sorted((l for l in linhas or [] if isinstance(l, dict) and isinstance(l.get("i"), int)),
                        key=lambda l: l["i"]):
        i = linha["i"]
        seguido = anterior is not None and i == anterior + 1
        cobertos = {}
        if linha.get("transicao") is not True:
            for a in linha.get("atras") or []:
                if not isinstance(a, dict) or not isinstance(a.get("id"), str):
                    continue
                cob = num(a.get("coberto"))
                if cob is not None and cob > ATRAS_LIMIAR:
                    cobertos[a["id"]] = a
        for chave in list(abertas):
            if chave not in cobertos or not seguido:
                fechadas.append(abertas.pop(chave))
        for chave, a in cobertos.items():
            r = abertas.get(chave)
            t = num(linha.get("t"))
            t = t if t is not None else i / float(fps)
            if r is None:
                r = abertas[chave] = {"id": chave, "peca": a.get("peca") or "", "texto": a.get("texto") or "",
                                      "de": t, "ate": t, "quadros": 0, "coberto": 0.0, "topo": None,
                                      "caixa": a.get("caixa")}
            r["ate"] = t
            r["quadros"] += 1
            if num(a.get("coberto")) > r["coberto"]:
                r["coberto"], r["caixa"] = num(a.get("coberto")), a.get("caixa")
            topo = num(a.get("topo"))
            if topo is not None:
                r["topo"] = topo if r["topo"] is None else min(r["topo"], topo)
        anterior = i
    fechadas.extend(abertas.values())
    return sorted([r for r in fechadas if r["quadros"] >= minimo], key=lambda r: r["de"])


def gate_contraste(c, np):
    g = Gate("contraste")
    pasta = c.pasta / "contraste"
    indice = pasta / "contraste.jsonl"
    if not indice.is_file():
        return g.pular("faltou contraste/contraste.jsonl (o compor.py escreve, com os quadros sem texto)",
                       [c.mostrar(indice)])
    try:
        from PIL import Image
    except ImportError:
        erro("o gate de contraste precisa do pillow. Rode com o Python do pacote: .venv/bin/python")
        sys.exit(2)

    amostras, ruins = [], 0
    try:
        with open(indice, encoding="utf-8") as f:
            for bruta in f:
                bruta = bruta.strip()
                if not bruta:
                    continue
                try:
                    d = json.loads(bruta)
                except json.JSONDecodeError:
                    ruins += 1
                    continue
                if isinstance(d, dict):
                    amostras.append(d)
                else:
                    ruins += 1
    except (OSError, UnicodeDecodeError) as e:
        g.reprovar()
        g.resumo = "não consegui ler o contraste.jsonl (%s)" % e
        return g

    fps = c.fps()
    # quadros no meio de uma transição não contam: ali a cena está de passagem (desfocada, varrida)
    em_transicao = set()
    linhas_layout, _, _ = c.layout()
    for linha in linhas_layout or []:
        if isinstance(linha, dict) and linha.get("transicao") is True and isinstance(linha.get("i"), int):
            em_transicao.add(linha["i"])
    medidas, faltando, sem_cor = [], [], 0
    puladas_transicao = 0
    lum_cache = {}
    mascaras_cache = {}
    atras_medidos = atras_escondidos = 0
    for ordem, a in enumerate(amostras):
        nome = a.get("arquivo")
        if not nome:
            ruins += 1
            continue
        if isinstance(a.get("i"), int) and a["i"] in em_transicao:
            puladas_transicao += 1
            continue
        caminho = pasta / str(nome)
        if not caminho.is_file():
            faltando.append(str(nome))
            continue
        if str(nome) not in lum_cache:
            try:
                with Image.open(caminho) as im:
                    rgb = np.asarray(im.convert("RGB"), dtype=np.float64)
            except Exception:
                faltando.append(str(nome) + " (ilegível)")
                continue
            lum_cache = {str(nome): (rgb, luminancia(rgb, np))}  # um quadro por vez na memória
        rgb, lum = lum_cache[str(nome)]
        alt, larg = lum.shape
        ex, ey = larg / float(LARGURA), alt / float(ALTURA)
        t = num(a.get("t"))
        i = a.get("i") if isinstance(a.get("i"), int) else None
        if t is None:
            t = (i / fps) if i is not None else 0.0
        for texto in a.get("textos") or []:
            if not isinstance(texto, dict):
                continue
            cx = caixa_de(texto.get("caixa"))
            cor = cor_de(texto.get("cor"))
            if not cx or not cor:
                sem_cor += 1
                continue
            x, y, w, h = cx
            xa, ya = int(max(0, math.floor(x * ex))), int(max(0, math.floor(y * ey)))
            xb, yb = int(min(larg, math.ceil((x + w) * ex))), int(min(alt, math.ceil((y + h) * ey)))
            if xb <= xa or yb <= ya:
                sem_cor += 1
                continue
            passo = max(1, int(math.sqrt((xb - xa) * (yb - ya) / 200000.0)))
            fundo_l = lum[ya:yb:passo, xa:xb:passo]
            if cor[3] < 1.0:
                misturado = cor[3] * np.array(cor[:3]) + (1.0 - cor[3]) * rgb[ya:yb:passo, xa:xb:passo]
                texto_l = luminancia(misturado, np)
            else:
                texto_l = float(luminancia(np.array(cor[:3]), np))
            # texto atrás de você (MOTOR.md 2.6): a pessoa recortada cobre parte da caixa, e ali a letra
            # não aparece. Vale só o que a pessoa não cobre, pela máscara do quadro (visao/mascara)
            if texto.get("atras"):
                livre = fora_da_pessoa(c, texto.get("recorte"), xa, ya, xb, yb, passo, ex, ey,
                                       mascaras_cache, np, Image)
                if livre is not None:
                    atras_medidos += 1
                    if livre.sum() < max(30, 0.03 * livre.size):
                        atras_escondidos += 1
                        continue
                    fundo_l = fundo_l[livre]
                    if not isinstance(texto_l, float):
                        texto_l = texto_l[livre]
            claro = np.maximum(texto_l, fundo_l)
            escuro = np.minimum(texto_l, fundo_l)
            razoes = (claro + 0.05) / (escuro + 0.05)
            pior = float(np.percentile(razoes, PERCENTIL_PIOR))
            tamanho = num(texto.get("tamanho_px")) or 0
            negrito = bool(texto.get("negrito"))
            grande = tamanho >= TAMANHO_GRANDE and negrito
            limite = CONTRASTE_GRANDE if grande else CONTRASTE_NORMAL
            # letra com contorno de 2 px ou mais (a legenda): o contorno separa a letra de qualquer
            # fundo, então vale o contraste da letra contra o contorno
            pelo_contorno = None
            contorno = texto.get("contorno")
            if (isinstance(contorno, list) and len(contorno) >= 3 and (num(texto.get("contorno_px")) or 0) >= 2
                    and all(isinstance(v, (int, float)) for v in contorno[:3])):
                lc = float(luminancia(np.array(contorno[:3], dtype=np.float64), np))
                lt = float(luminancia(np.array(cor[:3]), np))
                pelo_contorno = (max(lc, lt) + 0.05) / (min(lc, lt) + 0.05)
            passou = pior >= limite or (pelo_contorno is not None and pelo_contorno >= limite)
            medidas.append({"t": t, "i": i, "ordem": ordem, "arquivo": str(nome),
                            "caixa": [round(v) for v in cx], "cor": hexa(cor),
                            "alfa": round(cor[3], 2), "tamanho_px": tamanho, "negrito": negrito,
                            "contraste": round(pior, 2), "mediana": round(float(np.median(razoes)), 2),
                            "contra_contorno": round(pelo_contorno, 2) if pelo_contorno is not None else None,
                            "limite": limite, "passou": passou})

    # o texto atrás de você que a pessoa esconde, pelo layout de todos os quadros (não só os amostrados)
    escondidos = textos_escondidos(linhas_layout, fps)
    if escondidos:
        g.reprovar()
        g.dados["textos_escondidos"] = [{"de": round(r["de"], 3), "ate": round(r["ate"], 3), "peca": r["peca"],
                                         "texto": r["texto"], "coberto": round(r["coberto"], 3),
                                         "topo_pessoa": r["topo"], "caixa": r["caixa"]} for r in escondidos]
        for r in escondidos:
            g.linhas.append("%s a %s  ·  \"%s\" até %d%% atrás da pessoa%s  ·  %s"
                            % (seg(r["de"]), seg(r["ate"]), r["texto"], round(100 * r["coberto"]),
                               (" (a pessoa sobe até y %d)" % r["topo"]) if r["topo"] is not None else "",
                               r["peca"]))
        g.conserto.append("Texto atrás de você que a pessoa esconde: suba a peça (y), diminua o tam ou encurte "
                          "a vida dela. A palavra-chave fica acima do cabelo, e só a base da última linha "
                          "encosta na cabeça (MOTOR.md 3).")

    if not medidas:
        if escondidos:
            g.resumo = "%d texto(s) atrás de você escondidos pela pessoa" % len(escondidos)
            return g
        if amostras and faltando and len(faltando) >= len(amostras):
            return g.pular("nenhum dos %d quadro(s) do contraste.jsonl está na pasta contraste/"
                           % len(amostras), [c.mostrar(pasta / n) for n in faltando[:10]])
        g.avisar()
        g.resumo = ("o contraste.jsonl não tem nenhum texto medível (caixa e cor)" if amostras
                    else "o contraste.jsonl está vazio: nenhum quadro amostrado")
        g.dados.update({"amostras": len(amostras), "textos_sem_caixa_ou_cor": sem_cor})
        return g

    # quadros amostrados seguidos com o mesmo texto reprovado viram um intervalo
    ruins_med = [m for m in medidas if not m["passou"]]
    ordem_por_amostra = sorted({m["ordem"] for m in medidas})
    posicao = {o: k for k, o in enumerate(ordem_por_amostra)}

    def iou(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        ix = max(0, min(ax + aw, bx + bw) - max(ax, bx))
        iy = max(0, min(ay + ah, by + bh) - max(ay, by))
        inter = ix * iy
        return inter / float(aw * ah + bw * bh - inter) if inter else 0.0

    grupos = []
    for m in sorted(ruins_med, key=lambda m: (m["ordem"], m["caixa"][1])):
        alvo = None
        for gr in grupos:
            ult = gr[-1]
            if (posicao[m["ordem"]] - posicao[ult["ordem"]] == 1 and ult["cor"] == m["cor"]
                    and iou(ult["caixa"], m["caixa"]) >= 0.5):
                alvo = gr
                break
        if alvo is not None:
            alvo.append(m)
        else:
            grupos.append([m])

    trechos = []
    for gr in grupos:
        pior = min(gr, key=lambda m: m["contraste"])
        trechos.append({"de": round(gr[0]["t"], 3), "ate": round(gr[-1]["t"], 3), "amostras": len(gr),
                        "contraste": pior["contraste"], "limite": pior["limite"], "cor": pior["cor"],
                        "tamanho_px": pior["tamanho_px"], "negrito": pior["negrito"],
                        "caixa": pior["caixa"], "arquivo": pior["arquivo"]})
    trechos.sort(key=lambda tr: tr["de"])

    # O "pior" do --json é medido pela régua que decidiu cada texto. A legenda que só passou pelo
    # contorno (o fundo sozinho não dá o mínimo) é separada do fundo pelo contorno, e o contraste dela
    # contra o fundo não reprova nada. Ela entrava no mínimo, e o --json dizia 1,05:1 contra 3:1 num
    # gate aprovado cujo resumo dava 3,07:1 como o mais justo. Agora fica fora do "pior" (o mesmo texto
    # que o resumo chama de mais justo, ou o pior reprovado) e sai à parte, em "pior_pelo_contorno",
    # com a letra contra o contorno ao lado
    so_contorno = [m for m in medidas if m["passou"] and m["contraste"] < m["limite"]]
    pela_regua = [m for m in medidas if not (m["passou"] and m["contraste"] < m["limite"])]
    menor = min(pela_regua, key=lambda m: m["contraste"] / m["limite"]) if pela_regua else None
    menor_contorno = min(so_contorno, key=lambda m: m["contraste"] / m["limite"]) if so_contorno else None
    g.dados.update({"amostras": len(amostras), "textos_medidos": len(medidas), "reprovados": len(ruins_med),
                    "pior": ({k: menor[k] for k in ("t", "contraste", "limite", "cor", "caixa", "arquivo")}
                             if menor else None),
                    "pior_pelo_contorno": (dict({"legendas": len(so_contorno)},
                                                **{k: menor_contorno[k] for k in ("t", "contraste", "contra_contorno",
                                                                                  "limite", "cor", "caixa", "arquivo")})
                                           if menor_contorno else None),
                    "trechos_reprovados": trechos, "quadros_faltando": faltando,
                    "textos_sem_caixa_ou_cor": sem_cor, "linhas_ilegiveis": ruins,
                    "amostras_em_transicao": puladas_transicao,
                    "atras_de_voce": {"medidos_fora_da_pessoa": atras_medidos,
                                      "amostras_sem_letra_a_mostra": atras_escondidos,
                                      "limiar_coberto": ATRAS_LIMIAR, "minimo_s": ATRAS_MIN_S,
                                      "trechos_escondidos": len(escondidos)},
                    "limites": {"grande_negrito_48px": CONTRASTE_GRANDE, "normal": CONTRASTE_NORMAL,
                                "percentil_do_fundo": PERCENTIL_PIOR}})
    if faltando:
        g.linhas.append("%d quadro(s) do contraste.jsonl não estão na pasta: %s"
                        % (len(faltando), ", ".join(faltando[:5]) + (" ..." if len(faltando) > 5 else "")))
    if sem_cor:
        g.linhas.append("%d texto(s) sem caixa ou cor legível foram pulados" % sem_cor)

    if trechos:
        g.reprovar()
        g.resumo = "%d de %d texto(s) medidos abaixo do contraste mínimo" % (len(ruins_med), len(medidas))
        if escondidos:
            g.resumo += "; %d texto(s) atrás de você escondidos pela pessoa" % len(escondidos)
        for tr in trechos:
            quando = seg(tr["de"]) if tr["amostras"] == 1 else "%s a %s" % (seg(tr["de"]), seg(tr["ate"]))
            g.linhas.append("%s  ·  %.2f:1, mínimo %.1f:1  ·  texto %s %s%s em [%d, %d, %d, %d]  ·  %s"
                            % (quando, tr["contraste"], tr["limite"], tr["cor"],
                               ("%d px" % tr["tamanho_px"]) if tr["tamanho_px"] else "sem tamanho",
                               " negrito" if tr["negrito"] else "", *tr["caixa"], tr["arquivo"]))
        g.conserto.append("Escureça o vidro ou a sombra atrás do texto, troque a cor do texto, ou mova o "
                          "texto para uma área uniforme. Texto de 48 px ou mais em negrito precisa de 3:1; "
                          "o resto, de 4,5:1.")
    else:
        # o mais justo entre os que passaram pelo fundo (o "pior" do --json); os que passaram pelo contorno
        # contam à parte. Sem nenhum pelo fundo, não há "mais justo" a dar: o contraste de uma legenda
        # contra o fundo, abaixo do mínimo, sairia como se fosse a medida que aprovou
        if menor is not None:
            g.resumo = "%d texto(s) em %d quadro(s) amostrados; o mais justo tem %.2f:1 (mínimo %.1f:1) em %s" % (
                len(medidas), len(amostras), menor["contraste"], menor["limite"], seg(menor["t"]))
            if so_contorno:
                g.resumo += "; %d legenda(s) passaram pelo contorno, sobre fundo claro" % len(so_contorno)
        else:
            g.resumo = ("%d texto(s) em %d quadro(s) amostrados, todos legenda que passou pelo contorno, "
                        "sobre fundo claro" % (len(medidas), len(amostras)))
        if escondidos:
            g.resumo = ("%d texto(s) atrás de você escondidos pela pessoa; " % len(escondidos)) + g.resumo
        if faltando:
            g.avisar()
    return g


# ----------------------------------------------------------------- 4 legenda x rosto

def rosto_tem_face(c):
    """True se o rosto.json acha rosto em algum quadro, False se não acha em nenhum, None sem arquivo."""
    dados, problema = c.json("rosto.json")
    if problema or not isinstance(dados, dict):
        return None
    quadros = dados.get("quadros")
    if not isinstance(quadros, list):
        return None
    return any(q for q in quadros)


def gate_rosto(c, np):
    g = Gate("rosto")
    linhas, _, problema = c.layout()
    if problema == "faltando":
        return g.pular("faltou layout.jsonl (o compor.py escreve)", [c.mostrar(c.pasta / "layout.jsonl")])
    if problema:
        g.reprovar()
        g.resumo = "o layout.jsonl " + problema
        return g

    fps = c.fps()
    colisoes, sem_rosto = [], []
    medidos = com_legenda = 0
    for linha in linhas or []:
        t = num(linha.get("t"))
        i = linha.get("i") if isinstance(linha.get("i"), int) else None
        if t is None:
            if i is None:
                continue
            t = i / fps
        if linha.get("transicao") is True:
            continue
        leg = caixa_de(linha.get("legenda"))
        if not leg:
            continue
        com_legenda += 1
        rosto = caixa_de(linha.get("rosto"))
        if not rosto:
            if str(linha.get("modo")) in MODOS_COM_ROSTO:
                sem_rosto.append({"t": t, "i": i, "modo": linha.get("modo"), "cena": linha.get("cena")})
            continue
        medidos += 1
        lx, ly, lw, lh = leg
        rx, ry, rw, rh = rosto
        rx, ry, rw, rh = rx - FOLGA_ROSTO, ry - FOLGA_ROSTO, rw + 2 * FOLGA_ROSTO, rh + 2 * FOLGA_ROSTO
        ix = min(lx + lw, rx + rw) - max(lx, rx)
        iy = min(ly + lh, ry + rh) - max(ly, ry)
        if ix > 0 and iy > 0:
            colisoes.append({"t": t, "i": i, "invade_px": min(ix, iy), "vertical_px": iy,
                             "horizontal_px": ix, "legenda": [round(v) for v in leg],
                             "rosto": [round(v) for v in rosto], "cena": linha.get("cena"),
                             "modo": linha.get("modo")})

    trechos = []
    for gr in intervalos(colisoes, lambda v: "colisao", fps):
        pior = max(gr["itens"], key=lambda v: v["invade_px"])
        cenas = sorted({str(v["cena"]) for v in gr["itens"] if v.get("cena")})
        trechos.append({"de": round(gr["de"], 3), "ate": round(gr["ate"], 3), "quadros": len(gr["itens"]),
                        "invade_px": round(pior["invade_px"]), "legenda": pior["legenda"],
                        "rosto": pior["rosto"], "cenas": cenas})

    tem_face = rosto_tem_face(c)
    lacunas = []
    if sem_rosto and tem_face is not False:
        for gr in intervalos(sem_rosto, lambda v: "sem", fps):
            modos = sorted({str(v["modo"]) for v in gr["itens"]})
            lacunas.append({"de": round(gr["de"], 3), "ate": round(gr["ate"], 3),
                            "quadros": len(gr["itens"]), "modos": modos})

    g.dados.update({"folga_px": FOLGA_ROSTO, "quadros_com_legenda": com_legenda,
                    "quadros_medidos": medidos, "colisoes": trechos,
                    "quadros_de_rosto_sem_caixa": len(sem_rosto) if lacunas else 0,
                    "rosto_json": {None: "ausente", True: "acha rosto", False: "não acha rosto"}[tem_face]})
    if trechos:
        g.reprovar()
        g.resumo = "a legenda encosta no rosto em %d trecho(s)" % len(trechos)
        for tr in trechos:
            g.linhas.append("%s a %s  ·  invade %d px a folga de %d px  ·  legenda %s, rosto %s  ·  %d quadro(s)%s"
                            % (seg(tr["de"]), seg(tr["ate"]), tr["invade_px"], FOLGA_ROSTO, tr["legenda"],
                               tr["rosto"], tr["quadros"],
                               ("  ·  cena " + ", ".join(tr["cenas"])) if tr["cenas"] else ""))
        leg, rosto = trechos[0]["legenda"], trechos[0]["rosto"]
        if rosto[1] + rosto[3] / 2.0 < leg[1] + leg[3] / 2.0:
            g.conserto.append("O rosto está acima da legenda: desça a legenda (sem passar da base da zona "
                              "segura) ou enquadre o rosto mais alto na cena indicada.")
        else:
            g.conserto.append("O rosto está abaixo da legenda: suba a legenda (sem passar do topo da zona "
                              "segura) ou enquadre o rosto mais baixo; num modo de bolha, mude a bolha de lado.")
    elif medidos:
        g.resumo = "%d quadro(s) com legenda e rosto, nenhuma colisão com %d px de folga" % (medidos, FOLGA_ROSTO)
    elif com_legenda:
        g.resumo = "nenhum quadro com legenda e rosto ao mesmo tempo"
    else:
        g.resumo = "nenhum quadro com legenda no layout.jsonl"
    if lacunas:
        g.avisar()
        total = sum(l["quadros"] for l in lacunas)
        g.linhas.append("%d quadro(s) de modo com rosto na tela sem a caixa do rosto no layout.jsonl; "
                        "ali a colisão não foi medida:" % total)
        for l in lacunas[:6]:
            g.linhas.append("  %s a %s  ·  %s" % (seg(l["de"]), seg(l["ate"]), ", ".join(l["modos"])))
        if len(lacunas) > 6:
            g.linhas.append("  e mais %d trecho(s)" % (len(lacunas) - 6))
    return g


# ----------------------------------------------------------------- 5 sincronia

def energia(x, np, passo=PASSO, janela=JANELA_FFT):
    """Envelope em dB (janela de 20 ms a cada 5 ms) e o instante de início de cada janela."""
    h, w = int(SR * passo), int(SR * janela)
    n = (len(x) - w) // h + 1
    if n <= 0:
        return np.zeros(0), np.zeros(0)
    acum = np.concatenate([[0.0], np.cumsum(x * x)])
    ini = np.arange(n) * h
    e = (acum[ini + w] - acum[ini]) / w
    return ini / float(SR), 10.0 * np.log10(e + 1e-12)


def fala_plena(x, np):
    """Percentil 90 do RMS em janelas de 50 ms: a régua do energia_audio.py e do CORTE-LIMPO.md."""
    w = int(SR * 0.05)
    n = len(x) // w
    if n == 0:
        return 0.0
    rms = np.sqrt((x[: n * w].reshape(n, w) ** 2).mean(axis=1))
    return float(np.percentile(rms, 90))


def ataques_da_fala(x, np):
    """Instantes em que um som começa: subida rápida em alguma das seis faixas de frequência.

    Faixas separadas veem o "s" que nasce depois de uma vogal (sobe nos agudos enquanto o
    total cai) e o "Ga" que entra colado num "o" (degrau nos graves sem vale antes), que a
    energia total não vê. Cada faixa é medida contra o próprio nível, e uma subida só conta
    se termina num nível audível daquela faixa."""
    h, w = int(SR * PASSO), int(SR * JANELA_FFT)
    n = (len(x) - w) // h + 1
    if n < 2 * RAIO_PICO + 2:
        return np.zeros(0)
    freqs = np.fft.rfftfreq(w, 1.0 / SR)
    mascaras = [(freqs >= lo) & (freqs < hi) for lo, hi in BANDAS]
    janela = np.hanning(w)
    bandas = np.zeros((len(BANDAS), n))
    bloco = 4096
    for a in range(0, n, bloco):
        b = min(n, a + bloco)
        idx = (np.arange(a, b) * h)[:, None] + np.arange(w)[None, :]
        espectro = np.fft.rfft(x[idx] * janela, axis=1)
        potencia = espectro.real ** 2 + espectro.imag ** 2
        for k, m in enumerate(mascaras):
            bandas[k, a:b] = potencia[:, m].sum(axis=1)
    forca = np.zeros(n)
    for k in range(len(BANDAS)):
        e = 10.0 * np.log10(bandas[k] + 1e-10)
        ref = float(np.percentile(e, 90))
        e = np.maximum(e, ref - PISO_BANDA)
        subida = np.zeros(n)
        for j in range(1, ATRAS + 1):
            antes = np.concatenate([np.full(j, e[0]), e[:-j]])
            subida = np.maximum(subida, e - antes)
        subida[e < ref - AUDIVEL_BANDA] = 0.0
        forca += subida
    borda = np.concatenate([np.full(RAIO_PICO, -1.0), forca, np.full(RAIO_PICO, -1.0)])
    vizinhos = np.lib.stride_tricks.sliding_window_view(borda, 2 * RAIO_PICO + 1).max(axis=1)
    candidatos = np.where((forca >= FORCA_MIN) & (forca >= vizinhos))[0]
    picos = []
    for k in candidatos:
        if picos and k - picos[-1] <= RAIO_PICO:
            continue
        picos.append(k)
    # o pico da subida chega uns 15 ms depois de o som entrar: recua até onde a subida
    # ainda tem metade da força do pico, que é onde a faixa começou a subir
    instantes = []
    for k in picos:
        j = k
        while j > 0 and k - j < RECUO_MAX and forca[j - 1] >= RECUO * forca[k]:
            j -= 1
        instantes.append(j)
    return np.array(instantes, dtype=np.float64) * h / float(SR)


def placar_de_deslocamento(inicios, ataques, np):
    """Para cada deslocamento em bloco das palavras, quanto elas caem em cima de ataques."""
    lags = np.arange(-LAGS_MAX, LAGS_MAX + 1e-9, PASSO)
    placar = np.zeros(len(lags))
    for s in inicios:
        perto = ataques[(ataques >= s - LAGS_MAX - 0.1) & (ataques <= s + LAGS_MAX + 0.1)]
        if len(perto):
            d = perto[None, :] - (s + lags[:, None])
            placar += np.exp(-0.5 * (d / SIGMA_LAG) ** 2).sum(axis=1)
    return lags, placar


def deslocamento_global(inicios, ataques, np):
    """(deslocamento, confiança) da legenda inteira. Fica em zero se o pico não bate o zero por 20%."""
    lags, placar = placar_de_deslocamento(inicios, ataques, np)
    melhor, zero = int(np.argmax(placar)), int(np.argmin(np.abs(lags)))
    if placar[zero] <= 1e-9:
        return (float(lags[melhor]), 99.0) if placar[melhor] > 0 else (0.0, 0.0)
    confianca = float(placar[melhor] / placar[zero])
    return (float(lags[melhor]) if confianca >= CONFIANCA_LAG else 0.0), confianca


def concordancia(inicios, fins, som, t_env, a, b, np, alcance=LAGS_MAX):
    """Para cada deslocamento em bloco, a fração dos quadros de [a, b) em que palavra cai em
    som e vão entre palavras cai em silêncio. As pausas são raras e nítidas, então o pico
    marca o deslocamento do trecho para os dois lados, coisa que os ataques sozinhos não
    fazem: palavra marcada depois do som, no meio de fala contínua, sempre acha uma sílaba
    perto e parece certa."""
    lags = np.arange(-alcance, alcance + 1e-9, PASSO)
    idx = np.where((t_env >= a) & (t_env < b))[0]
    if len(idx) < 40:
        return lags, None
    tt = t_env[idx]
    w = np.zeros(len(idx))
    for s, f in zip(inicios, fins):
        if f > a and s < b:
            w[(tt >= s) & (tt < f)] = 1.0
    passos = np.round(lags / PASSO).astype(int)
    real = som[np.clip(idx[None, :] + passos[:, None], 0, len(som) - 1)]
    return lags, (w[None, :] * real + (1.0 - w[None, :]) * (1.0 - real)).mean(axis=1)


def segmentos_da_edicao(c):
    segs = []
    edicao, problema = c.json("edicao.json")
    if not problema and isinstance(edicao, dict) and isinstance(edicao.get("segmentos"), list):
        for s in edicao["segmentos"]:
            if isinstance(s, dict):
                a, b = num(s.get("saida_de")), num(s.get("saida_ate"))
                if a is not None and b is not None and b > a:
                    segs.append((a, b))
    return sorted(segs)


def trechos_de_medida(segmentos, duracao):
    """Os segmentos da edição (ou o corte inteiro), partidos em pedaços de até 10 s, para a
    deriva de velocidade também aparecer."""
    base = [(a, b) for a, b in segmentos if b > a] or [(0.0, duracao)]
    saida = []
    for a, b in base:
        n = max(1, int(math.ceil((b - a) / TRECHO_MAX - 1e-9)))
        passo = (b - a) / n
        saida.extend((a + k * passo, a + (k + 1) * passo) for k in range(n))
    return saida


def medir_sincronia(x, palavras, segmentos, np):
    """A medida inteira, sem arquivo nenhum: amostras a 16 kHz, palavras ordenadas
    ({inicio, fim, texto}) e os segmentos (saida_de, saida_ate) da edição, que podem faltar."""
    dur = len(x) / float(SR)
    ataques = ataques_da_fala(x, np)
    t_env, db_env = energia(x, np)
    plena = fala_plena(x, np)
    limiar_silencio = 20.0 * math.log10(plena * SILENCIO_FRACAO + 1e-12)
    inicios = np.array([p["inicio"] for p in palavras])
    fins = np.array([p["fim"] for p in palavras])
    som = (db_env >= limiar_silencio).astype(np.float64)

    lag_global, confianca = deslocamento_global(inicios, ataques, np)
    lag = np.full(len(palavras), lag_global)
    relatorio_segs = []
    trechos = trechos_de_medida(segmentos, dur)
    if len(trechos) > 1 or segmentos:
        bordas = np.array([a for a, _ in trechos]) - 0.05
        dono = np.clip(np.searchsorted(bordas, inicios, side="right") - 1, 0, len(trechos) - 1)
        for k, (a, b) in enumerate(trechos):
            m = dono == k
            lags, acordo = concordancia(inicios[m], fins[m], som, t_env, a, b, np)
            v = None
            if acordo is not None and m.sum() >= TRECHO_MIN_PALAVRAS:
                j = int(np.argmax(acordo))
                base = acordo[int(np.argmin(np.abs(lags - lag_global)))]
                if acordo[j] - base >= GANHO_TRECHO and abs(lags[j] - lag_global) >= PASSO * 4:
                    v = float(lags[j])
                # pico na borda da busca não é pico: em fala de ritmo regular a concordância sobe
                # até a borda sem nunca fazer um máximo. Busca de novo com o dobro do alcance, e o
                # deslocamento só vale se lá ele virar máximo de verdade, longe da borda nova.
                if v is not None and abs(v) >= LAGS_MAX - PASSO / 2:
                    lags2, acordo2 = concordancia(inicios[m], fins[m], som, t_env, a, b, np,
                                                  alcance=2 * LAGS_MAX)
                    v = None
                    if acordo2 is not None:
                        j2 = int(np.argmax(acordo2))
                        base2 = acordo2[int(np.argmin(np.abs(lags2 - lag_global)))]
                        if (abs(lags2[j2]) < 2 * LAGS_MAX - PASSO / 2 and acordo2[j2] - base2 >= GANHO_TRECHO
                                and abs(lags2[j2] - lag_global) >= PASSO * 4):
                            v = float(lags2[j2])
                # e os ataques confirmam: no deslocamento achado, o começo das palavras cai em
                # cima de ataque pelo menos tão bem quanto no deslocamento global. Sem isso, a
                # concordância achou um encaixe de ritmo, não um atraso de legenda.
                if v is not None:
                    lags_a, placar_a = placar_de_deslocamento(inicios[m], ataques, np)
                    no_v = placar_a[int(np.argmin(np.abs(lags_a - v)))] if abs(v) <= LAGS_MAX else 0.0
                    no_global = placar_a[int(np.argmin(np.abs(lags_a - lag_global)))]
                    if abs(v) > LAGS_MAX or no_v < no_global:
                        v = None
            if v is not None:
                lag[m] = v
            relatorio_segs.append({"de": round(a, 3), "ate": round(b, 3), "palavras": int(m.sum()),
                                   "deslocamento_ms": round((v if v is not None else lag_global) * 1000),
                                   "proprio": v is not None})

    deslocadas = inicios + lag
    medidas = []
    for k, p in enumerate(palavras):
        s = p["inicio"]
        item = {"t": round(s, 3), "texto": p["texto"]}
        if s > dur + 0.02:
            item.update({"erro": -max(JANELA_SINC, s - dur), "como": "fora do áudio"})
            medidas.append(item)
            continue
        if abs(lag[k]) > JANELA_SINC:
            # o som desta palavra está fora da janela: o erro é o do trecho inteiro
            item.update({"erro": float(lag[k]), "como": "trecho deslocado"})
            medidas.append(item)
            continue
        alvo = s + lag[k]
        cands = ataques[(ataques >= s - JANELA_SINC) & (ataques <= s + JANELA_SINC)]
        # um ataque só serve a esta palavra se não estiver mais perto de outra
        donos = [a for a in cands if int(np.argmin(np.abs(deslocadas - a))) == k]
        if donos:
            a = min(donos, key=lambda v: abs(v - alvo))
            item.update({"erro": float(a - s), "como": "medida"})
        else:
            k0, k1 = np.searchsorted(t_env, s), np.searchsorted(t_env, s + 0.05)
            if k1 > k0 and float(db_env[k0:k1].max()) < limiar_silencio:
                depois = ataques[ataques > s]
                e = float(depois[0] - s) if len(depois) and depois[0] - s < 1.0 else 1.0
                item.update({"erro": max(e, JANELA_SINC), "como": "começa em silêncio"})
            else:
                item.update({"erro": None, "como": "sem ataque"})
        medidas.append(item)

    medidas_ok = [m for m in medidas if m["erro"] is not None]
    erros = np.array([abs(m["erro"]) for m in medidas_ok])
    return {
        "duracao": dur, "ataques": int(len(ataques)), "lag_global": lag_global, "confianca_global": confianca,
        "segmentos": relatorio_segs, "medidas": medidas, "medidas_ok": medidas_ok,
        "p50": float(np.percentile(erros, 50)) if len(erros) else 0.0,
        "p95": float(np.percentile(erros, 95)) if len(erros) else 0.0,
        "piores": sorted(medidas_ok, key=lambda m: -abs(m["erro"]))[:5],
    }


def gate_sincronia(c, np):
    g = Gate("sincronia")
    dados, problema = c.json("palavras-corte.json")
    if problema:
        return faltou(c, g, "palavras-corte.json", "o editar_fala.py escreve")
    if not (c.pasta / "fala.mp4").is_file():
        return g.pular("faltou fala.mp4 (o editar_fala.py escreve)", [c.mostrar(c.pasta / "fala.mp4")])
    x, problema = c.audio(np)
    if problema:
        g.reprovar()
        g.resumo = problema
        return g

    brutas = dados.get("palavras") if isinstance(dados, dict) else None
    palavras, invalidas = [], 0
    for p in brutas if isinstance(brutas, list) else []:
        s = num(p.get("inicio")) if isinstance(p, dict) else None
        if s is None:
            invalidas += 1
            continue
        palavras.append({"inicio": s, "fim": num(p.get("fim")), "texto": str(p.get("texto", ""))})
    palavras.sort(key=lambda p: p["inicio"])
    for k, p in enumerate(palavras):
        if p["fim"] is None or p["fim"] <= p["inicio"]:
            prox = palavras[k + 1]["inicio"] if k + 1 < len(palavras) else p["inicio"] + 0.25
            p["fim"] = min(prox, p["inicio"] + 0.25) if prox > p["inicio"] else p["inicio"] + 0.05
    if not palavras:
        g.avisar()
        g.resumo = "o palavras-corte.json não tem nenhuma palavra com tempo"
        return g

    r = medir_sincronia(x, palavras, segmentos_da_edicao(c), np)
    for m in r["medidas"]:
        e = m.pop("erro")
        if e is not None:
            m["erro_ms"] = round(e * 1000)
    p50, p95, medidas_ok, piores = r["p50"], r["p95"], r["medidas_ok"], r["piores"]

    meta = dados.get("meta") if isinstance(dados, dict) else None
    dur_meta = num(meta.get("duracao")) if isinstance(meta, dict) else None
    g.dados.update({"palavras": len(palavras), "medidas": len(medidas_ok), "p50_ms": round(p50 * 1000),
                    "p95_ms": round(p95 * 1000), "limite_p95_ms": round(P95_MAX * 1000),
                    "janela_ms": round(JANELA_SINC * 1000), "ataques": r["ataques"],
                    "duracao_audio": round(r["duracao"], 3),
                    "deslocamento_global_ms": round(r["lag_global"] * 1000),
                    "segmentos": r["segmentos"], "piores": piores, "por_palavra": r["medidas"]})

    def quanto(v_ms):
        return "a fala vem %d ms %s da legenda" % (abs(v_ms), "depois" if v_ms > 0 else "antes")

    def frase(m):
        e = m["erro_ms"]
        lado = "legenda adiantada" if e > 0 else "legenda atrasada"
        extra = "" if m["como"] == "medida" else "; " + m["como"]
        return "%s \"%s\" %+d ms (%s%s)" % (seg(m["t"]), m["texto"], e, lado, extra)

    if invalidas:
        g.linhas.append("%d palavra(s) sem tempo de início foram puladas" % invalidas)
    if dur_meta and abs(dur_meta - r["duracao"]) > 0.5:
        g.linhas.append("o palavras-corte.json diz %.2f s e o fala.mp4 tem %.2f s: confira se são do mesmo corte"
                        % (dur_meta, r["duracao"]))
    global_ms = round(r["lag_global"] * 1000)
    if abs(global_ms) >= AVISO_LAG * 1000:
        g.linhas.append("a legenda inteira está deslocada em bloco: %s" % quanto(global_ms))
    proprios = [s for s in r["segmentos"]
                if s["proprio"] and abs(s["deslocamento_ms"] - global_ms) >= AVISO_LAG * 1000]
    if proprios:
        g.linhas.append("segmento(s) da edição deslocado(s) em bloco:")
        for s in proprios:
            g.linhas.append("  %s a %s  ·  %s (%d palavras)"
                            % (seg(s["de"]), seg(s["ate"]), quanto(s["deslocamento_ms"]), s["palavras"]))
    g.linhas.append("5 piores:")
    for m in piores:
        g.linhas.append("  " + frase(m))

    g.resumo = "p95 %d ms (limite %d), mediana %d ms, %d de %d palavras medidas" % (
        round(p95 * 1000), round(P95_MAX * 1000), round(p50 * 1000), len(medidas_ok), len(palavras))
    if p95 > P95_MAX:
        g.reprovar()
        g.conserto.append("Erro em bloco é mapa de tempo errado no editar_fala.py: segmento sem descontar o "
                          "que saiu antes, ou velocidade sem aplicar nas palavras. Erro espalhado é "
                          "alinhamento: realinhe as palavras na energia do fala.mp4.")
    elif len(medidas_ok) < max(5, 0.5 * len(palavras)):
        g.avisar()
        g.linhas.append("poucas palavras com início mensurável (%d de %d): o p95 vale pouco aqui"
                        % (len(medidas_ok), len(palavras)))
    return g


# ----------------------------------------------------------------- 6 emendas

def gate_emendas(c, np):
    g = Gate("emendas")
    edicao, problema = c.json("edicao.json")
    if problema:
        return faltou(c, g, "edicao.json", "o editar_fala.py escreve")
    if not (c.pasta / "fala.mp4").is_file():
        return g.pular("faltou fala.mp4 (o editar_fala.py escreve)", [c.mostrar(c.pasta / "fala.mp4")])
    emendas_brutas = edicao.get("emendas") if isinstance(edicao, dict) else None
    if not isinstance(emendas_brutas, list):
        g.reprovar()
        g.resumo = "o edicao.json não tem a lista \"emendas\" (MOTOR.md 2.2)"
        return g
    x, problema = c.audio(np)
    if problema:
        g.reprovar()
        g.resumo = problema
        return g

    tempos = sorted(t for t in (num(v) for v in emendas_brutas) if t is not None)
    if not tempos:
        g.resumo = "nenhuma emenda no edicao.json: a fala é um trecho só"
        g.dados["emendas"] = []
        return g

    plena = fala_plena(x, np)
    dur = len(x) / float(SR)
    palavras_d, _ = c.json("palavras-corte.json")
    palavras = []
    if isinstance(palavras_d, dict) and isinstance(palavras_d.get("palavras"), list):
        for p in palavras_d["palavras"]:
            if isinstance(p, dict) and num(p.get("inicio")) is not None:
                palavras.append((num(p.get("inicio")), num(p.get("fim")) or num(p.get("inicio")),
                                 str(p.get("texto", ""))))

    def rms(a, b):
        ia, ib = max(0, int(round(a * SR))), min(len(x), int(round(b * SR)))
        return float(np.sqrt(np.mean(x[ia:ib] ** 2))) if ib > ia else 0.0

    resultados = []
    for t in tempos:
        item = {"t": round(t, 3)}
        if t < 0 or t > dur:
            item.update({"situacao": "fora do áudio", "fracao": None})
            resultados.append(item)
            continue
        antes, depois = rms(t - EMENDA_MEIA, t), rms(t, t + EMENDA_MEIA)
        fracao = max(antes, depois) / plena if plena > 0 else 0.0
        item.update({"fracao": round(fracao, 3), "antes": round(antes / plena, 3) if plena else 0,
                     "depois": round(depois / plena, 3) if plena else 0})
        if fracao >= EMENDA_REPROVA:
            item["situacao"] = "no meio da fala"
        elif fracao >= SILENCIO_FRACAO:
            item["situacao"] = "possível sílaba comida"
        else:
            item["situacao"] = "silêncio"
        if palavras:
            ant = [p for p in palavras if p[0] < t - 0.02]
            dep = [p for p in palavras if p[0] >= t - 0.02]
            item["entre"] = [ant[-1][2] if ant else None, dep[0][2] if dep else None]
        resultados.append(item)

    ruins = [r for r in resultados if r["situacao"] in ("no meio da fala", "fora do áudio")]
    duvidas = [r for r in resultados if r["situacao"] == "possível sílaba comida"]
    g.dados.update({"emendas": resultados, "fala_plena_rms": round(plena, 6),
                    "limites": {"silencio": SILENCIO_FRACAO, "reprova": EMENDA_REPROVA, "meia_janela_ms": 15}})

    def linha(r):
        if r["situacao"] == "fora do áudio":
            return "%s  ·  fora do fala.mp4 (%.2f s)" % (seg(r["t"]), dur)
        onde = ""
        if r.get("entre"):
            a, b = r["entre"]
            onde = "  ·  entre \"%s\" e \"%s\"" % (a or "início", b or "fim")
        return "%s  ·  %.0f%% da fala plena (antes %.0f%%, depois %.0f%%)  ·  %s%s" % (
            seg(r["t"]), 100 * r["fracao"], 100 * r["antes"], 100 * r["depois"], r["situacao"], onde)

    for r in ruins + duvidas:
        g.linhas.append(linha(r))
    if ruins:
        g.reprovar()
        g.resumo = "%d de %d emenda(s) caíram no meio da fala" % (len(ruins), len(resultados))
        g.conserto.append("Mova o ponto de corte para dentro de um silêncio de verdade (energia_audio.py), "
                          "com os dois lados da emenda em silêncio (CORTE-LIMPO.md, passo 5).")
    elif duvidas:
        g.avisar()
        g.resumo = "%d de %d emenda(s) com som acima do silêncio: ouça os 2 s em volta" % (
            len(duvidas), len(resultados))
    else:
        maior = max(r["fracao"] for r in resultados)
        g.resumo = "%d emenda(s), todas em silêncio (a mais alta com %.0f%% da fala plena; limite %.0f%%)" % (
            len(resultados), 100 * maior, 100 * SILENCIO_FRACAO)
    return g


# ----------------------------------------------------------------- 7 volume

def tem_audio(sonda):
    return any(s.get("codec_type") == "audio" for s in (sonda or {}).get("streams", []))


def gate_volume(c, np):
    g = Gate("volume")
    if not c.entrega.is_file():
        return g.pular("faltou a entrega %s" % c.mostrar(c.entrega), [c.mostrar(c.entrega)])
    sonda, problema = c.sondar_entrega()
    if problema:
        return g.pular("a entrega não abre no ffprobe (o gate de entrega reprova isso)")
    if not tem_audio(sonda):
        return g.pular("a entrega não tem áudio para medir (o gate de entrega reprova isso)")
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(c.entrega), "-vn",
           "-af", "ebur128=peak=true:framelog=verbose", "-f", "null", "-"]
    proc = subprocess.run(cmd, capture_output=True)
    texto = proc.stderr.decode("utf-8", "ignore")
    resumo = texto[texto.rfind("Summary:"):] if "Summary:" in texto else ""
    m_i = re.search(r"Integrated loudness:\s*\n\s*I:\s*(-?[\d.]+|-inf)\s*LUFS", resumo)
    m_lra = re.search(r"LRA:\s*(-?[\d.]+)\s*LU", resumo)
    m_tp = re.search(r"True peak:\s*\n\s*Peak:\s*(-?[\d.]+|-inf)", resumo)
    if proc.returncode != 0 or not m_i or not m_tp:
        g.reprovar()
        g.resumo = "o ffmpeg não devolveu a medida ebur128 da entrega"
        return g
    integrado = -70.0 if m_i.group(1) == "-inf" else float(m_i.group(1))
    pico = -99.0 if m_tp.group(1) == "-inf" else float(m_tp.group(1))
    lra = float(m_lra.group(1)) if m_lra else None
    g.dados.update({"lufs_integrado": integrado, "pico_verdadeiro_dbtp": pico, "lra_lu": lra,
                    "limites": {"lufs": [LUFS_ALVO - LUFS_TOLERANCIA, LUFS_ALVO + LUFS_TOLERANCIA],
                                "pico_max_dbtp": PICO_MAX}})
    problemas = []
    if abs(integrado - LUFS_ALVO) > LUFS_TOLERANCIA + 1e-9:
        problemas.append("%.1f LUFS integrado, fora de %.0f ±%.0f" % (integrado, LUFS_ALVO, LUFS_TOLERANCIA))
    if pico > PICO_MAX + 1e-9:
        problemas.append("pico verdadeiro %.1f dBTP, acima de %.0f" % (pico, PICO_MAX))
    medida = "%.1f LUFS integrado, pico verdadeiro %.1f dBTP%s" % (
        integrado, pico, (", LRA %.1f LU" % lra) if lra is not None else "")
    if problemas:
        g.reprovar()
        g.resumo = "; ".join(problemas)
        g.linhas.append(medida)
        g.conserto.append("Normalize a mixagem no audio.py (loudnorm em duas passadas, alvo -14 LUFS e "
                          "-1 dBTP) e monte a entrega de novo.")
    else:
        g.resumo = medida
    return g


# ----------------------------------------------------------------- 8 excesso de efeito

def gate_efeitos(c, np):
    g = Gate("efeitos")
    cenas_d, problema = c.json("cenas.json")
    origem = "cenas.json"
    lista = []
    if problema is None:
        if not (isinstance(cenas_d, dict) and isinstance(cenas_d.get("cenas"), list)):
            g.reprovar()
            g.resumo = "o cenas.json não tem a lista \"cenas\" (MOTOR.md seção 3)"
            return g
        for cena in cenas_d["cenas"]:
            if not isinstance(cena, dict):
                continue
            entrada = cena.get("entrada")
            trans = entrada.get("transicao") if isinstance(entrada, dict) else None
            lista.append({"id": cena.get("id"), "t": num(cena.get("inicio")), "transicao": trans or "corte"})
    elif problema != "faltando":
        return faltou(c, g, "cenas.json", "o planejador escreve")
    else:
        eventos_d, problema_ev = c.json("eventos.json")
        if not problema_ev and isinstance(eventos_d, dict) and isinstance(eventos_d.get("cenas"), list):
            origem = "eventos.json (o cenas.json faltou)"
            for cena in eventos_d["cenas"]:
                if isinstance(cena, dict):
                    lista.append({"id": cena.get("id"), "t": num(cena.get("inicio")),
                                  "transicao": cena.get("transicao") or "corte"})
        else:
            return g.pular("faltou cenas.json (o planejador escreve)", [c.mostrar(c.pasta / "cenas.json")])

    duracao = c.duracao_plano()
    if not duracao:
        fins = [num(x.get("fim")) for x in (cenas_d or {}).get("cenas", []) if isinstance(x, dict)] \
            if isinstance(cenas_d, dict) else []
        duracao = max([f for f in fins if f] or [0.0])
    teto = TETO_TRANSICOES_PADRAO
    gates_cfg = c.setup.get("gates") if isinstance(c.setup, dict) else None
    if isinstance(gates_cfg, dict) and num(gates_cfg.get("teto_transicoes_min")):
        teto = num(gates_cfg.get("teto_transicoes_min"))
    # o estilo de produção do plano (motor/estilos.json) manda no teto: o maior entre os escolhidos
    estilo = cenas_d.get("estilo") if isinstance(cenas_d, dict) else None
    if estilo:
        nomes = [estilo] if isinstance(estilo, str) else list(estilo)
        try:
            tabela = json.loads((Path(__file__).resolve().parents[1] / "motor" / "estilos.json").read_text(encoding="utf-8")).get("estilos", {})
            tetos = [num(tabela[n].get("teto_transicoes_min")) for n in nomes if n in tabela]
            if tetos and all(tetos):
                teto = max(tetos)
                g.dados["estilo"] = nomes
        except (OSError, ValueError):
            pass

    efeitos = [x for x in lista if str(x["transicao"]) != "corte"]
    por_min = len(efeitos) / (duracao / 60.0) if duracao else 0.0
    g.dados.update({"origem": origem, "cenas": len(lista), "transicoes": len(efeitos),
                    "por_minuto": round(por_min, 2), "teto_por_minuto": teto, "teto_provisorio": True,
                    "duracao": round(duracao or 0, 3),
                    "lista": [{"t": x["t"], "cena": x["id"], "transicao": x["transicao"]} for x in efeitos]})
    descricao = ", ".join("%s %s" % (seg(x["t"]) if x["t"] is not None else "?", x["transicao"])
                          for x in efeitos)
    if not duracao:
        g.avisar()
        g.resumo = "sem duração no plano: não deu para calcular transições por minuto"
        return g
    if por_min > teto:
        g.avisar()
        g.resumo = "%d transições em %.1f s = %.1f por minuto, acima do teto provisório de %g" % (
            len(efeitos), duracao, por_min, teto)
        g.linhas.append(descricao)
        g.conserto.append("Troque as transições menos importantes por corte seco. O teto ainda vai ser "
                          "calibrado; por enquanto é só aviso.")
    else:
        g.resumo = "%d transição(ões) em %.1f s = %.1f por minuto (teto provisório %g)" % (
            len(efeitos), duracao, por_min, teto)
        if efeitos:
            g.linhas.append(descricao)
    return g


# ----------------------------------------------------------------- 9 entrega

def atomos(caminho):
    """Os átomos de topo do MP4, em ordem: [(tipo, posição)]."""
    lista = []
    with open(caminho, "rb") as f:
        total = os.fstat(f.fileno()).st_size
        pos = 0
        while pos + 8 <= total and len(lista) < 256:
            f.seek(pos)
            cab = f.read(8)
            if len(cab) < 8:
                break
            tam = int.from_bytes(cab[:4], "big")
            tipo = cab[4:8].decode("latin-1")
            minimo = 8
            if tam == 1:
                ext = f.read(8)
                if len(ext) < 8:
                    break
                tam = int.from_bytes(ext, "big")
                minimo = 16
            elif tam == 0:
                tam = total - pos
            if tam < minimo:
                break
            lista.append((tipo, pos))
            pos += tam
    return lista


def imagens_do_plano(no, caminho=""):
    """Todo valor de campo "imagem" do cenas.json, com onde ele está."""
    achadas = []
    if isinstance(no, dict):
        for k, v in no.items():
            onde = caminho + "." + k if caminho else k
            if k == "imagem" and isinstance(v, str) and v.strip():
                achadas.append((v.strip(), onde))
            else:
                achadas.extend(imagens_do_plano(v, onde))
    elif isinstance(no, list):
        for i, v in enumerate(no):
            achadas.extend(imagens_do_plano(v, "%s[%d]" % (caminho, i)))
    return achadas


def gate_entrega(c, np):
    g = Gate("entrega")
    if not c.entrega.is_file():
        return g.pular("faltou a entrega %s" % c.mostrar(c.entrega), [c.mostrar(c.entrega)])
    problemas, conferido = [], []
    sonda, falha = c.sondar_entrega()
    video = {}
    if falha:
        problemas.append("o ffprobe não conseguiu ler o arquivo: " + falha)
    else:
        video = next((s for s in sonda.get("streams", []) if s.get("codec_type") == "video"), {})
        if not video:
            problemas.append("não há vídeo dentro do arquivo")
        else:
            larg, alt = video.get("width"), video.get("height")
            conferido.append("%sx%s" % (larg, alt))
            if (larg, alt) != (LARGURA, ALTURA):
                problemas.append("resolução %sx%s, o certo é %dx%d" % (larg, alt, LARGURA, ALTURA))

            def taxa(v):
                try:
                    a, b = (float(p) for p in str(v).split("/"))
                    return a / b if b else 0.0
                except ValueError:
                    return 0.0

            r, media = taxa(video.get("r_frame_rate")), taxa(video.get("avg_frame_rate"))
            conferido.append("%.3g fps" % media)
            if abs(r - FPS) > 0.01 or abs(media - FPS) > 0.05:
                problemas.append("taxa de quadros %s (média %.3f), o certo é %d fps constante"
                                 % (video.get("r_frame_rate"), media, FPS))
            codec = video.get("codec_name")
            conferido.append(str(codec))
            if codec != "h264":
                problemas.append("codec %s, o certo é h264" % codec)
            pix = video.get("pix_fmt")
            conferido.append(str(pix))
            if pix != "yuv420p":
                problemas.append("formato de pixel %s, o certo é yuv420p%s"
                                 % (pix, " (faixa cheia de PNG vazou para o vídeo)" if pix == "yuvj420p" else ""))
            sar = video.get("sample_aspect_ratio")
            if sar not in (None, "1:1", "0:1", "N/A"):
                problemas.append("SAR %s, o certo é 1:1" % sar)
        if tem_audio(sonda):
            audio = next(s for s in sonda["streams"] if s.get("codec_type") == "audio")
            conferido.append("áudio %s" % audio.get("codec_name"))
        else:
            problemas.append("sem áudio")
    try:
        ordem = [t for t, _ in atomos(c.entrega)]
    except OSError as e:
        ordem = []
        problemas.append("não consegui ler os átomos do MP4 (%s)" % e.strerror)
    if "moov" in ordem and "mdat" in ordem:
        if ordem.index("moov") < ordem.index("mdat"):
            conferido.append("faststart")
        else:
            problemas.append("sem faststart: o átomo moov vem depois do mdat (%s)" % " ".join(ordem[:6]))
    elif ordem:
        problemas.append("não achei moov e mdat no topo do arquivo (%s)" % " ".join(ordem[:6]))

    # a pasta do corte tem só o mp4 (o ls não mostra arquivo oculto, então eles não contam)
    # a capa mora ao lado do mp4, porque é com ela que o corte sobe (capa.py)
    capas = {c.nome + "-capa.jpg", c.nome + "-capa.png"}
    tem_capa = any((c.pasta_entrega / n).is_file() for n in capas)
    sobra = sorted(p.name for p in c.pasta_entrega.iterdir() if not p.name.startswith(".")
                   and p.name != c.entrega.name and p.name not in capas)
    if sobra:
        problemas.append("a pasta %s/ tem mais que o mp4: %s" % (c.nome, ", ".join(sobra)))

    # créditos das imagens do plano
    creditos = {}
    cenas_d, problema_c = c.json("cenas.json")
    if problema_c == "faltando":
        g.linhas.append("sem cenas.json: os créditos das imagens não foram conferidos")
    elif problema_c:
        g.linhas.append("o cenas.json %s: os créditos das imagens não foram conferidos" % problema_c)
    else:
        imagens = imagens_do_plano(cenas_d)
        if imagens:
            opcoes = [c.projeto / "materiais-de-trabalho" / "assets" / "CREDITOS.md",
                      c.pasta / "assets" / "CREDITOS.md"]
            arquivo = next((p for p in opcoes if p.is_file()), None)
            nomes = sorted({os.path.basename(v.replace("\\", "/")) for v, _ in imagens})
            creditos = {"imagens": nomes, "arquivo": c.mostrar(arquivo) if arquivo else None}
            if arquivo is None:
                problemas.append("o plano usa %d imagem(ns) e não existe %s"
                                 % (len(nomes), c.mostrar(opcoes[0])))
                creditos["sem_credito"] = nomes
            else:
                texto = arquivo.read_text(encoding="utf-8", errors="ignore")
                # o nome inteiro, não um pedaço: "foto.jpg" não vale por "minha-foto.jpg"
                sem = [n for n in nomes
                       if not re.search(r"(?<![\w.-])" + re.escape(n) + r"(?![\w-])", texto, re.IGNORECASE)]
                creditos["sem_credito"] = sem
                if sem:
                    problemas.append("o %s não cita: %s" % (arquivo.name, ", ".join(sem)))
                else:
                    conferido.append("créditos de %d imagem(ns)" % len(nomes))

    g.dados.update({"arquivo": c.mostrar(c.entrega), "atomos": ordem[:8], "problemas": problemas,
                    "video": {k: video.get(k) for k in ("width", "height", "r_frame_rate", "avg_frame_rate",
                                                        "codec_name", "pix_fmt", "sample_aspect_ratio")}
                    if video else None, "pasta_sobrando": sobra, "creditos": creditos or None})
    if problemas:
        g.reprovar()
        g.resumo = "%d problema(s) no formato ou na pasta" % len(problemas)
        g.linhas.extend(problemas)
        g.conserto.append("O formato sai do montar.py ou do compor.py (RECEITA-TECNICA.md seção 1); "
                          "material de trabalho mora em materiais-de-trabalho/%s/, e todo crédito de "
                          "imagem vai no CREDITOS.md de materiais-de-trabalho/assets/." % c.nome)
    else:
        g.resumo = ", ".join(conferido) + (", pasta com o mp4 e a capa" if tem_capa else ", pasta só com o mp4")
    return g


# ----------------------------------------------------------------- 10 efeitos sonoros (4.3)

def importar(nome):
    """Um script irmão (audio.py, linguagem.py) como módulo: a lógica fica num lugar só."""
    pasta = str(Path(__file__).resolve().parent)
    if pasta not in sys.path:
        sys.path.insert(0, pasta)
    import importlib
    return importlib.import_module(nome)


def sha256_de(caminho):
    import hashlib
    try:
        return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()
    except OSError:
        return None


def picos_verdadeiros(caminho, janelas, np):
    """O pico verdadeiro (dBTP) de cada janela [de, ate) do áudio, sobreamostrado 4x como no ebur128."""
    taxa = 48000 * SOBRE_AMOSTRA
    cmd = ["ffmpeg", "-v", "error", "-i", str(caminho), "-vn", "-ac", "2", "-ar", str(taxa),
           "-f", "f32le", "-"]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0 or len(proc.stdout) < 8:
        return None
    x = np.abs(np.frombuffer(proc.stdout[: len(proc.stdout) // 8 * 8], np.float32).reshape(-1, 2)).max(axis=1)
    saida = []
    for de, ate in janelas:
        a, b = max(0, int(de * taxa)), min(len(x), int(ate * taxa))
        pico = float(x[a:b].max()) if b > a else 0.0
        saida.append(20.0 * math.log10(pico) if pico > 0 else -99.0)
    return saida


def agenda_dos_sons(c, g):
    """(agenda, origem) do que o audio.py tocou: o sons.json, ou a agenda refeita para entrega antiga."""
    dados, problema = c.json("sons.json")
    if problema is None and isinstance(dados, dict) and isinstance(dados.get("efeitos"), list):
        if dados.get("eventos_sha256") and dados["eventos_sha256"] != sha256_de(c.pasta / "eventos.json"):
            g.avisar()
            g.linhas.append("o eventos.json mudou depois do último audio.py: o som da entrega é de outro plano")
            g.conserto.append("Rode o audio.py de novo para o som seguir o plano de agora.")
        if dados.get("fala_sha256") and dados["fala_sha256"] != sha256_de(c.pasta / "fala.mp4"):
            g.avisar()
            g.linhas.append("o fala.mp4 mudou depois do último audio.py")
            g.conserto.append("Rode o audio.py de novo.")
        return dados, "sons.json do audio.py"
    if problema not in (None, "faltando"):
        g.linhas.append("o sons.json %s; refiz a agenda pelo eventos.json" % problema)
    audio = importar("audio")
    try:
        dados = audio.agenda_do_corte(c.pasta, c.raiz, corrigir_tonica=False)
    except audio.Falha as e:
        return None, str(e)
    return dados, "refeita pelo eventos.json (sem sons.json: áudio de antes da 4.3, sem a correção da tônica)"


def gate_som(c, np):
    g = Gate("som")
    _, problema = c.json("eventos.json")
    if problema:
        return faltou(c, g, "eventos.json", "o compor.py escreve")
    if not (c.pasta / "fala.mp4").is_file():
        return g.pular("faltou fala.mp4 (o editar_fala.py escreve)", [c.mostrar(c.pasta / "fala.mp4")])
    agenda, origem = agenda_dos_sons(c, g)
    if agenda is None:
        return g.pular("não deu para montar a agenda dos efeitos: " + origem)
    efeitos = sorted(agenda.get("efeitos") or [], key=lambda e: e.get("t_som", e["t"]))
    duracao = num(agenda.get("duracao")) or c.duracao_plano() or 0.0
    g.dados.update({"origem": origem, "efeitos": len(efeitos), "duracao": round(duracao, 3),
                    "limites": {"densidade_olhe_s": DENSIDADE_OLHE, "densidade_reprova_s": DENSIDADE_REPROVA,
                                "juntos_olhe": JUNTOS_OLHE, "juntos_reprova": JUNTOS_REPROVA,
                                "folga_tonica_db": FOLGA_TONICA, "pico_max_dbtp": PICO_MAX}})
    if agenda.get("sem_efeitos") or not efeitos:
        g.resumo = "nenhum efeito sonoro no reel (%s)" % origem
        return g
    reprovas, olhes, partes = [], [], []

    # densidade e efeitos juntos
    media = duracao / len(efeitos) if duracao else 0.0
    marcos = sorted([(e["comeca"], 1) for e in efeitos] + [(e["termina"], -1) for e in efeitos])
    agora, juntos, quando = 0, 0, None
    for t, d in marcos:
        agora += d
        if agora > juntos:
            juntos, quando = agora, t
    g.dados.update({"um_a_cada_s": round(media, 3), "mais_juntos": juntos})
    partes.append("%d efeitos em %.1f s, um a cada %.2f s" % (len(efeitos), duracao, media))
    if media and media < DENSIDADE_REPROVA:
        reprovas.append("um efeito a cada %.2f s no reel inteiro: som em tudo (o limite claro é %.2f s; a régua "
                        "da pesquisa, %.1f s)" % (media, DENSIDADE_REPROVA, DENSIDADE_OLHE))
    elif media and media < DENSIDADE_OLHE:
        olhes.append("um efeito a cada %.2f s, mais denso que um a cada %.1f s (pesquisa 04, 4.2): deixe sem som "
                     "os eventos de peso 1 e os de enfeite" % (media, DENSIDADE_OLHE))
    if juntos >= JUNTOS_REPROVA:
        reprovas.append("%d efeitos soando juntos em %s" % (juntos, seg(quando)))
    elif juntos > JUNTOS_OLHE:
        olhes.append("%d efeitos soando juntos em %s (o máximo da pesquisa é %d)" % (juntos, seg(quando), JUNTOS_OLHE))

    # o mesmo arquivo em seguida. Numa agenda refeita (entrega sem sons.json) o arquivo é o que o audio.py
    # de hoje escolheria, com a biblioteca de hoje: a entrega antiga pode ter tocado outro, então não conta
    refeita = "sem sons.json" in origem
    repetidos = [] if refeita else [(a, b) for a, b in zip(efeitos, efeitos[1:]) if a.get("arquivo") == b.get("arquivo")]
    g.dados["repetidos_em_seguida"] = None if refeita else [
        {"de": a["t"], "ate": b["t"], "arquivo": a["arquivo"]} for a, b in repetidos]
    if repetidos:
        reprovas.append("o mesmo arquivo em dois efeitos seguidos: " + ", ".join(
            "%s em %s e %s" % (a["arquivo"], seg(a["t"]), seg(b["t"])) for a, b in repetidos))
    elif refeita:
        partes.append("arquivo repetido não conferido (sem sons.json)")
    else:
        partes.append("nenhum arquivo repetido em seguida")

    # a sílaba tônica da palavra destacada
    na_tonica = [e for e in efeitos if e.get("tonica")]
    resolvidos, baixados, abertos = [], [], []
    for e in na_tonica:
        acao = e["tonica"].get("acao")
        folga = num(e.get("folga_db"))
        mascara = e.get("fala") and folga is not None and folga < FOLGA_TONICA
        texto = "%s em %s, na tônica de \"%s\" (%s)%s" % (
            e["arquivo"], seg(e["t"]), e["tonica"]["palavra"],
            e["tonica"].get("motivo", "destaque"), (", folga da voz %.0f dB" % folga) if folga is not None else "")
        if acao in ("antes do ataque", "antes da tônica"):
            resolvidos.append(e)
        elif acao == "baixou" and not mascara:
            baixados.append(e)
        elif mascara:
            reprovas.append(texto + ": o efeito encobre a palavra")
        else:
            abertos.append(texto)
    g.dados["tonica"] = {"destaques": len(agenda.get("destaques") or []), "cairiam": len(na_tonica),
                         "adiantados": len(resolvidos), "baixados": len(baixados), "abertos": len(abertos),
                         "efeitos": [{"t": e["t"], "arquivo": e["arquivo"], "palavra": e["tonica"]["palavra"],
                                      "acao": e["tonica"].get("acao"), "folga_db": e.get("folga_db"),
                                      "desloca_ms": e.get("desloca_ms", 0.0)} for e in na_tonica]}
    if abertos:
        olhes.append("%d efeito(s) em cima da sílaba tônica de palavra destacada (a voz fica 6 dB ou mais acima, "
                     "então não encobre):" % len(abertos))
        olhes.extend("  " + a for a in abertos)
    if na_tonica:
        partes.append("tônica: %d de %d efeito(s) cairiam numa palavra destacada%s" % (
            len(na_tonica), len(efeitos), "" if not (resolvidos or baixados) else
            " (%d adiantado(s), %d baixado(s))" % (len(resolvidos), len(baixados))))
    else:
        partes.append("nenhum na tônica de palavra destacada (%d)" % len(agenda.get("destaques") or []))

    # o pico em volta de cada efeito, no que vai para a rede
    fonte = c.entrega if c.entrega.is_file() else (c.pasta / "audio-final.wav")
    if fonte.is_file():
        janelas = [(e["comeca"] - JANELA_PICO, e["termina"] + JANELA_PICO) for e in efeitos]
        picos = picos_verdadeiros(fonte, janelas, np)
        if picos is None:
            g.linhas.append("o ffmpeg não leu o áudio de %s: picos não medidos" % fonte.name)
        else:
            pior = max(range(len(picos)), key=lambda i: picos[i])
            g.dados["pico_nos_efeitos_dbtp"] = round(picos[pior], 2)
            partes.append("pico perto dos efeitos %.1f dBTP" % picos[pior])
            acima = [(efeitos[i], p) for i, p in enumerate(picos) if p > PICO_MAX + 1e-9]
            if acima:
                reprovas.append("pico verdadeiro acima de %.0f dBTP em %s" % (PICO_MAX, ", ".join(
                    "%s (%s, %.1f dBTP)" % (seg(e["t"]), e["arquivo"], p) for e, p in acima)))
    else:
        g.linhas.append("sem entrega nem audio-final.wav: picos não medidos")

    g.linhas.insert(0, "agenda: " + origem)
    if reprovas:
        g.reprovar()
        g.linhas.extend(reprovas)
        texto = " ".join(reprovas)
        if "som em tudo" in texto or "soando juntos" in texto:
            g.conserto.append("Tire o som dos eventos de peso 1 e de enfeite no plano (\"som\": null).")
        if "mesmo arquivo" in texto:
            g.conserto.append("Peça a família (\"whoosh\"), não o arquivo (\"whoosh-2\"), para o audio.py variar.")
        if "encobre" in texto:
            g.conserto.append("Baixe o --efeitos-db ou o peso do evento, ou mova o evento para o respiro.")
        if "pico verdadeiro" in texto:
            g.conserto.append("Rode o audio.py de novo (loudnorm com teto de -1 dBTP).")
        g.conserto.append("Depois rode o audio.py de novo.")
    if olhes:
        g.avisar()
        g.linhas.extend(olhes)
        if "sem sons.json" in origem and abertos:
            g.conserto.append("O audio.py da 4.3 afasta esses efeitos da tônica: rode ele de novo neste corte.")
    g.resumo = "; ".join(partes)
    return g


# ----------------------------------------------------------------- 11 linguagem (4.3)

def gate_linguagem(c, np):
    g = Gate("linguagem")
    cenas, problema = c.json("cenas.json")
    if problema:
        return faltou(c, g, "cenas.json", "o planejador escreve")
    if not isinstance(cenas, dict) or not cenas.get("linguagem"):
        return g.nao_se_aplica("o plano não declara \"linguagem\" (reel de antes da 4.0 ou sem linguagem)")
    lg = importar("linguagem")
    try:
        r = lg.avaliar(c.raiz or Path.cwd(), lg.carregar_tabela(), c.pasta)
    except lg.Falha as e:
        g.reprovar()
        g.resumo = str(e)
        return g
    nome = "%s%s" % (r.get("linguagem"), (" + " + r["convidada"]) if r.get("convidada") else "")
    g.dados.update({k: r.get(k) for k in ("linguagem", "convidada", "transicoes", "heroi", "sons")})
    g.dados.update({"problemas": r["problemas"], "avisos": r["avisos"]})
    g.linhas.extend(r["linhas"])
    if r["problemas"]:
        g.reprovar()
        g.linhas.extend(r["problemas"])
        g.resumo = "%s: %d problema(s) do linguagem.py conferir" % (nome, len(r["problemas"]))
        g.conserto.append("Troque as peças de fora pelas da linguagem (motor/linguagens.json) ou declare a "
                          "convidada; o herói vai entre 55% e 80% da duração (docs-4/variedade-e-som.md 3.3).")
    else:
        g.resumo = "%s: as peças batem com a linguagem e o herói está na faixa" % nome
    if r["avisos"]:
        g.avisar()
        g.linhas.extend(r["avisos"])
    return g


# ----------------------------------------------------------------- 13 mundo (3.0)

AMPLIACAO_ROSTO_MAX = 1.12
ROSTO_EM_CENA_MIN = 2.0 / 3.0


def gate_mundo(c, np):
    g = Gate("mundo")
    cenas, problema = c.json("cenas.json")
    if problema:
        return faltou(c, g, "cenas.json", "o planejador escreve")
    lista = [x for x in (cenas.get("cenas") or []) if isinstance(x, dict)] if isinstance(cenas, dict) else []
    do_mundo = [x for x in lista if x.get("modo") == "mundo"]
    if not do_mundo:
        return g.nao_se_aplica("o plano não tem cena no modo mundo")

    # M3: a câmera dentro do modo, pelo mesmo fiscal do compor.py (o plano já vem com as âncoras resolvidas)
    motor = str(Path(__file__).resolve().parents[1] / "motor")
    if motor not in sys.path:
        sys.path.insert(0, motor)
    import ancoras
    erros, avisos = ancoras.conferir_mundos(cenas)

    # M4: no máximo um whoosh nas cenas de mundo
    eventos, _ = c.json("eventos.json")
    faixas = [(num(x.get("inicio")) or 0.0, num(x.get("fim")) or 0.0) for x in do_mundo]
    whooshes = []
    for e in (eventos.get("eventos") or []) if isinstance(eventos, dict) else []:
        t = num(e.get("t")) if isinstance(e, dict) else None
        if t is not None and str(e.get("som") or "").startswith("whoosh") and any(a <= t < b for a, b in faixas):
            whooshes.append(t)
    if len(whooshes) > 1:
        erros.append("%d whooshes nas cenas de mundo (%s); no máximo um, na troca de superfície ou no chicote"
                     % (len(whooshes), ", ".join(seg(t) for t in whooshes)))

    # o rosto em cena: quadro, pip e rosto contam; a tela cheia não
    total = sum(b - a for a, b in faixas)
    com_rosto = sum((num(x.get("fim")) or 0) - (num(x.get("inicio")) or 0) for x in do_mundo
                    if ((x.get("conteudo") or {}).get("superficie") or "quadro") != "tela")
    fracao = com_rosto / total if total > 0 else 1.0
    if fracao < ROSTO_EM_CENA_MIN:
        avisos.append("o rosto fica em cena %.0f%% do tempo de mundo; a meta é dois terços (menos tela cheia, "
                      "mais quadro ou pip)" % (fracao * 100))

    # M2 e M1: o relatório e os quadros-chave que o compor.py grava no render inteiro
    rel, prob_rel = c.json("mundo.json")
    chaves_arq = []
    if prob_rel:
        avisos.append("faltou o mundo.json: rode o compor.py inteiro (ele grava o relatório e os quadros-chave)")
    elif isinstance(rel, dict):
        for nome, m in rel.items():
            amp = num(m.get("ampliacao_rosto")) or 0
            if amp > AMPLIACAO_ROSTO_MAX + 1e-3:
                avisos.append("mundo \"%s\": o rosto chega a %.2fx a gravação (acima de %.2fx lê mole); a fonte é "
                              "pequena para o card, prefira o pip" % (nome, amp, AMPLIACAO_ROSTO_MAX))
            chaves_arq += m.get("quadros_chave_arquivos") or []

    g.dados.update({"cenas_de_mundo": len(do_mundo), "whooshes": [round(t, 3) for t in whooshes],
                    "rosto_em_cena": round(fracao, 3), "quadros_chave": chaves_arq,
                    "erros": erros, "avisos": avisos})
    if erros:
        g.reprovar()
        g.resumo = "%d problema(s) de câmera ou de som no modo mundo" % len(erros)
        g.linhas.extend(erros)
        g.conserto.append("Conserte no cenas.json: menos chaves (o teto da calma é 7), nenhuma na parada, um "
                          "chicote no máximo, zoom até 1,40; o whoosh único fica na primeira troca para a tela.")
    else:
        g.resumo = "%d cena(s) de mundo: câmera no modo, %d whoosh, rosto em cena %.0f%% do tempo" % (
            len(do_mundo), len(whooshes), fracao * 100)
    if avisos:
        g.avisar()
        g.linhas.extend(avisos)
    if chaves_arq:
        g.linhas.append("olhe os %d quadro(s)-chave em conferencia-mundo/ em tamanho cheio: o objeto de que se "
                        "fala inteiro e legível, nada cortado na borda da vista" % len(chaves_arq))
    return g


# ----------------------------------------------------------------- 12 variedade (4.3)

def tracos_do_reel(pasta):
    """O conjunto de traços de um reel (para o Jaccard da pesquisa 04, 6.6) e o resumo dele."""
    try:
        cenas = json.loads((pasta / "cenas.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, {}
    if not isinstance(cenas, dict):
        return None, {}
    ling = cenas.get("linguagem")
    base, conv = (ling, None) if isinstance(ling, str) else ((ling or {}).get("base"), (ling or {}).get("convidada"))
    heroi = cenas.get("heroi").get("nome") if isinstance(cenas.get("heroi"), dict) else None
    trilha = cenas.get("trilha")
    trilha = Path(str(trilha.get("arquivo") if isinstance(trilha, dict) else trilha)).name if trilha else None
    t = set()
    for k, v in (("linguagem", base), ("convidada", conv), ("heroi", heroi), ("trilha", trilha)):
        if v:
            t.add("%s:%s" % (k, v))
    leg = cenas.get("legenda")
    if isinstance(leg, dict) and leg.get("estilo"):
        t.add("legenda:%s" % leg["estilo"])
    estilo = cenas.get("estilo")
    for e in ([estilo] if isinstance(estilo, str) else list(estilo or [])):
        t.add("estilo:%s" % e)
    for cena in cenas.get("cenas") or []:
        if not isinstance(cena, dict):
            continue
        if cena.get("modo"):
            t.add("modo:%s" % cena["modo"])
        entrada = cena.get("entrada")
        if isinstance(entrada, dict) and entrada.get("transicao") not in (None, "corte"):
            t.add("transicao:%s" % entrada["transicao"])
        for item in cena.get("sobre") or []:
            if isinstance(item, dict) and item.get("tipo"):
                t.add("sobre:%s" % item["tipo"])
                if item["tipo"] in ("palavra", "look") and item.get("efeito"):
                    t.add("%s:%s" % (item["tipo"], item["efeito"]))
    try:
        ev = json.loads((pasta / "eventos.json").read_text(encoding="utf-8"))
        for e in ev.get("eventos", []):
            if isinstance(e, dict) and e.get("som"):
                t.add("som:%s" % re.sub(r"-\d+$", "", str(e["som"])))
    except (OSError, ValueError, AttributeError):
        pass
    return t, {"linguagem": base, "convidada": conv, "heroi": heroi, "trilha": trilha}


def historico_de_reels(c):
    """Os reels anteriores, do mais antigo ao mais recente: [(rótulo, pasta ou None, resumo)].

    Primeiro o projetos/.historico-linguagens.json (o linguagem.py registrar). Sem ele, a fábrica ainda
    não registrou nada: o histórico é refeito das entregas que declaram linguagem, pela data do mp4.
    """
    raiz = c.raiz or fabrica.raiz()
    projetos = raiz / "projetos"
    caminho = projetos / ".historico-linguagens.json"
    eu = (c.projeto.name, c.nome[-2:])
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        reels = [r for r in dados.get("reels", []) if isinstance(r, dict)]
        saida = []
        for r in reels:
            if (r.get("projeto"), r.get("corte")) == eu:
                continue
            pasta = projetos / str(r.get("projeto")) / "materiais-de-trabalho" / ("corte-%s" % r.get("corte"))
            saida.append(("%s/corte-%s" % (r.get("projeto"), r.get("corte")), pasta if pasta.is_dir() else None,
                          {k: r.get(k) for k in ("linguagem", "convidada", "heroi", "trilha")}))
        return saida, c.mostrar(caminho)
    except (OSError, ValueError, AttributeError):
        pass
    minha_data = c.entrega.stat().st_mtime if c.entrega.is_file() else float("inf")
    achados = []
    for plano in sorted(projetos.glob("*/materiais-de-trabalho/corte-*/cenas.json")):
        pasta = plano.parent
        projeto = pasta.parents[1]
        if (projeto.name, pasta.name[-2:]) == eu or projeto.name.startswith("teste"):
            continue                # projeto de teste (teste-onda-1) não é reel publicado
        entrega = projeto / pasta.name / (pasta.name + ".mp4")
        if not entrega.is_file() or entrega.stat().st_mtime >= minha_data:
            continue
        tracos, resumo = tracos_do_reel(pasta)
        if tracos is None or not resumo.get("linguagem"):
            continue
        achados.append((entrega.stat().st_mtime, "%s/%s" % (projeto.name, pasta.name), pasta, resumo))
    achados.sort(key=lambda a: a[0])
    return [(r, p, s) for _, r, p, s in achados][-10:], "refeito das entregas com linguagem (não há %s)" % c.mostrar(caminho)


def gate_variedade(c, np):
    g = Gate("variedade")
    cenas, problema = c.json("cenas.json")
    if problema:
        return faltou(c, g, "cenas.json", "o planejador escreve")
    if not isinstance(cenas, dict) or not isinstance(cenas.get("cenas"), list):
        g.avisar()
        g.resumo = "o cenas.json não tem a lista \"cenas\""
        return g
    sinais = []
    lista = [x for x in cenas["cenas"] if isinstance(x, dict)]

    # 1. a mesma transição muitas vezes seguidas (o corte seco não interrompe: o olho vê o mesmo efeito)
    trans = [(x.get("entrada") or {}).get("transicao") if isinstance(x.get("entrada"), dict) else None for x in lista]
    trans = [(t, num(x.get("inicio"))) for t, x in zip(trans, lista) if t and t != "corte"]
    corrida = []
    for item in trans + [(None, None)]:
        if corrida and item[0] == corrida[-1][0]:
            corrida.append(item)
            continue
        if len(corrida) > TRANSICAO_SEGUIDA_MAX:
            sinais.append("a transição %s %d vezes seguidas (%s)" % (corrida[0][0], len(corrida),
                          ", ".join(seg(t) for _, t in corrida if t is not None)))
        corrida = [item]

    # 2. o mesmo efeito de palavra em sequência
    palavras = []
    for x in lista:
        for item in x.get("sobre") or []:
            if isinstance(item, dict) and item.get("tipo") == "palavra" and num(item.get("t")) is not None:
                palavras.append((num(item["t"]), item.get("efeito") or "glitch",
                                 str(item.get("texto") or "%s%s" % (item.get("valor", ""), item.get("sufixo") or ""))))
    for item in cenas.get("sobre") or []:
        if isinstance(item, dict) and item.get("tipo") == "palavra" and num(item.get("t")) is not None:
            palavras.append((num(item["t"]), item.get("efeito") or "glitch", item.get("texto") or ""))
    palavras.sort()
    corrida = []
    for item in palavras + [(None, None, None)]:
        if corrida and item[1] == corrida[-1][1]:
            corrida.append(item)
            continue
        if len(corrida) > PALAVRA_SEGUIDA_MAX:
            sinais.append("a palavra %s %d vezes seguidas (%s)" % (corrida[0][1], len(corrida),
                          ", ".join("%s \"%s\"" % (seg(t), txt) for t, _, txt in corrida)))
        corrida = [item]
    g.dados["palavras"] = len(palavras)

    # 3. cenas todas com a mesma duração
    duracoes = [num(x.get("fim")) - num(x.get("inicio")) for x in lista
                if num(x.get("fim")) is not None and num(x.get("inicio")) is not None]
    if len(duracoes) >= CENAS_MIN_IGUAL:
        mediana = sorted(duracoes)[len(duracoes) // 2]
        if mediana > 0 and all(abs(d - mediana) <= DURACAO_IGUAL * mediana for d in duracoes):
            sinais.append("as %d cenas têm a mesma duração (%.1f s ±%d%%): corte no relógio, não na ideia"
                          % (len(duracoes), mediana, round(DURACAO_IGUAL * 100)))
        g.dados["duracao_das_cenas"] = [round(d, 2) for d in duracoes]

    # 4. efeito em metrônomo: os momentos relevantes (peso 2 ou 3) a intervalo regular
    ev, _ = c.json("eventos.json")
    if isinstance(ev, dict) and isinstance(ev.get("eventos"), list):
        tempos = sorted({round(num(e.get("t")), 1) for e in ev["eventos"]
                         if isinstance(e, dict) and num(e.get("t")) is not None and (num(e.get("peso")) or 1) >= 2})
        momentos = []
        for t in tempos:
            if not momentos or t - momentos[-1] > JUNTA_RECOMPOSICAO:
                momentos.append(t)
        vaos = [b - a for a, b in zip(momentos, momentos[1:])]
        if len(vaos) >= 5:
            media = sum(vaos) / len(vaos)
            dp = (sum((v - media) ** 2 for v in vaos) / len(vaos)) ** 0.5
            cv = dp / media if media else 0.0
            g.dados["cv_dos_intervalos"] = round(cv, 3)
            if cv < CV_METRONOMO:
                sinais.append("os momentos de peso 2 e 3 vêm a intervalo regular (um a cada %.1f s, variação de "
                              "%d%%, o piso é %d%%): efeito em metrônomo" % (media, round(cv * 100), round(CV_METRONOMO * 100)))

    # 5. o mesmo arquivo de som muitas vezes no reel (só com o sons.json da 4.3)
    sons, problema_s = c.json("sons.json")
    if problema_s is None and isinstance(sons, dict):
        conta = {}
        for e in sons.get("efeitos") or []:
            conta[e.get("arquivo")] = conta.get(e.get("arquivo"), 0) + 1
        muitos = sorted((n, a) for a, n in conta.items() if n > ARQUIVO_REPETE_MAX)
        if muitos:
            sinais.append("o mesmo arquivo de efeito muitas vezes no reel: %s (o ouvido reconhece em 3)"
                          % ", ".join("%s %dx" % (a, n) for n, a in reversed(muitos)))

    # 6. contra os reels anteriores
    meus, eu = tracos_do_reel(c.pasta)
    historico, origem = historico_de_reels(c)
    g.dados["historico"] = {"origem": origem, "reels": [r for r, _, _ in historico]}
    if not historico:
        g.linhas.append("histórico: nenhum reel anterior com linguagem (%s)" % origem)
    else:
        g.linhas.append("histórico: %d reel(s) anterior(es), %s" % (len(historico), origem))
        recentes = list(reversed(historico))
        for chave, n in MEMORIA.items():
            if eu.get(chave):
                iguais = [r for r, _, s in recentes[:n] if s.get(chave) == eu[chave]]
                if iguais:
                    sinais.append("%s %s repete um dos últimos %d reels (%s)" % (
                        {"linguagem": "a linguagem", "heroi": "o herói", "trilha": "a trilha"}[chave], eu[chave], n,
                        ", ".join(iguais)))
        rotulo, pasta_ant, _ = recentes[0]
        if meus and pasta_ant is not None:
            deles, _ = tracos_do_reel(pasta_ant)
            if deles:
                j = len(meus & deles) / len(meus | deles)
                g.dados["jaccard_com_o_anterior"] = {"reel": rotulo, "valor": round(j, 3)}
                g.linhas.append("traços em comum com o anterior (%s): %d%%" % (rotulo, round(j * 100)))
                if j >= JACCARD_MAX:
                    sinais.append("%d%% dos traços iguais aos de %s (linguagem, transições, palavras, sons, modos): "
                                  "a mesma cara do anterior (o limite é %d%%)" % (round(j * 100), rotulo,
                                                                                  round(JACCARD_MAX * 100)))

    g.dados["sinais"] = sinais
    if sinais:
        g.avisar()
        g.resumo = "%d sinal(is) de template" % len(sinais)
        g.linhas.extend(sinais)
        g.conserto.append("Varie a peça repetida (outra transição ou efeito de palavra do kit da linguagem), "
                          "solte o tempo das cenas na fala e, se o reel tem a cara do anterior, troque a linguagem "
                          "ou o herói (linguagem.py sugerir). Só aviso: este gate nunca reprova.")
    else:
        g.resumo = "nenhum sinal de template (transições, palavras, ritmo das cenas%s)" % (
            ", histórico" if historico else "")
    return g


# ----------------------------------------------------------------- execução

FUNCOES = {
    "ritmo": gate_ritmo, "zonas": gate_zonas, "contraste": gate_contraste, "rosto": gate_rosto,
    "sincronia": gate_sincronia, "emendas": gate_emendas, "volume": gate_volume,
    "efeitos": gate_efeitos, "entrega": gate_entrega,
    "som": gate_som, "linguagem": gate_linguagem, "variedade": gate_variedade,
    "mundo": gate_mundo,
}
PRECISA_FFMPEG = {"sincronia", "emendas", "volume", "som"}
PRECISA_FFPROBE = {"volume", "entrega"}


def achar_projeto(pedido):
    p = Path(pedido).expanduser()
    if p.is_dir():
        return p.resolve()
    raiz_do_script = fabrica.raiz()
    q = raiz_do_script / pedido
    if q.is_dir():
        return q.resolve()
    return None


def achar_raiz(projeto):
    for p in [projeto] + list(projeto.parents):
        if (p / "setup.json").is_file():
            return p
    padrao = fabrica.raiz()
    return padrao if (padrao / "setup.json").is_file() else None


def main():
    ap = argparse.ArgumentParser(
        description="Roda os gates automáticos de um reel antes da revisão: ritmo, zonas, contraste, "
                    "legenda x rosto, sincronia, emendas, volume, excesso de efeito, entrega, efeitos sonoros, "
                    "linguagem e variedade.")
    ap.add_argument("--projeto", required=True, help="a pasta do vídeo, por exemplo projetos/meu-video")
    ap.add_argument("--corte", required=True, help="o número do corte: 01, 1 ou corte-01")
    ap.add_argument("--so", help="só estes gates, separados por vírgula: " + ", ".join(GATES))
    ap.add_argument("--json", action="store_true", help="imprime o resultado em JSON")
    ap.add_argument("--estrito", action="store_true", help="gate pulado por falta de arquivo conta como reprovado")
    args = ap.parse_args()

    projeto = achar_projeto(args.projeto)
    if projeto is None:
        erro("não achei a pasta do projeto %s" % args.projeto)
        return 2
    m = re.fullmatch(r"(?:corte-?)?0*(\d{1,3})", args.corte.strip().lower())
    if not m:
        erro("--corte é o número do corte, por exemplo 01 ou corte-01; veio '%s'" % args.corte)
        return 2
    nome = "corte-%02d" % int(m.group(1))

    escolhidos = list(GATES)
    if args.so:
        escolhidos = []
        for parte in args.so.split(","):
            chave = parte.strip().lower()
            if not chave:
                continue
            chave = APELIDOS.get(chave, chave)
            if chave not in FUNCOES:
                erro("gate desconhecido em --so: '%s'. Os nomes são: %s" % (parte.strip(), ", ".join(GATES)))
                return 2
            if chave not in escolhidos:
                escolhidos.append(chave)
        escolhidos.sort(key=GATES.index)
        if not escolhidos:
            erro("--so ficou vazio. Os nomes são: " + ", ".join(GATES))
            return 2

    np = carregar_numpy()
    if PRECISA_FFMPEG & set(escolhidos):
        exigir("ffmpeg")
    if PRECISA_FFPROBE & set(escolhidos):
        exigir("ffprobe")

    raiz = achar_raiz(projeto)
    c = Corte(projeto, nome, raiz)
    pasta_existe = c.pasta.is_dir()

    resultados = []
    for chave in escolhidos:
        try:
            g = FUNCOES[chave](c, np)
        except SystemExit:
            raise
        except Exception as e:  # um gate quebrado não derruba os outros
            g = Gate(chave)
            g.reprovar()
            g.resumo = "o gate quebrou: %s: %s" % (type(e).__name__, e)
        resultados.append(g)

    contagem = {s: sum(1 for g in resultados if g.status == s)
                for s in ("PASSOU", "REPROVOU", "AVISO", "PULADO", "NÃO SE APLICA")}
    valeram = len(resultados) - contagem["NÃO SE APLICA"]
    reprovou = contagem["REPROVOU"] > 0 or (args.estrito and contagem["PULADO"] > 0)
    if reprovou:
        veredito = "REPROVADO"
    elif valeram == 0:
        veredito = "NÃO SE APLICA"
    elif contagem["PULADO"] == valeram:
        veredito = "NADA CONFERIDO"
    elif contagem["PULADO"]:
        veredito = "INCOMPLETO"
    elif contagem["AVISO"]:
        veredito = "PASSOU COM AVISOS"
    else:
        veredito = "PASSOU"
    codigo = 1 if reprovou else 0

    if args.json:
        saida = {
            "corte": nome, "projeto": c.mostrar(projeto), "pasta_do_corte": c.mostrar(c.pasta),
            "entrega": c.mostrar(c.entrega), "setup": c.mostrar(raiz / "setup.json") if raiz else None,
            "estrito": args.estrito, "veredito": veredito, "passou": not reprovou,
            "completo": contagem["PULADO"] == 0, "contagem": contagem,
            "gates": {g.chave: g.como_dict() for g in resultados},
        }
        if c.setup_erro:
            saida["setup_erro"] = c.setup_erro
        print(json.dumps(saida, ensure_ascii=False, indent=2))
        return codigo

    print("")
    print("  conferência do reel  ·  %s  ·  %s" % (nome, c.mostrar(projeto)))
    print("  pasta do corte: %s%s" % (c.mostrar(c.pasta), "" if pasta_existe else "  (não existe)"))
    if raiz is None:
        print("  setup.json não encontrado: zonas e teto de transições no padrão")
    elif c.setup_erro:
        print("  setup.json %s: zonas e teto de transições no padrão" % c.setup_erro)
    print("")
    for g in resultados:
        numero = GATES.index(g.chave) + 1
        rotulo = ("%d  %s " % (numero, g.titulo)).ljust(25, ".")
        print("  %s %-9s %s" % (rotulo, "N/A" if g.status == "NÃO SE APLICA" else g.status, g.resumo))
        for linha in g.linhas:
            print("       " + linha)
        if g.conserto and g.status in ("REPROVOU", "AVISO"):
            print("       conserto: " + " ".join(g.conserto))
        if g.linhas or (g.conserto and g.status in ("REPROVOU", "AVISO")):
            print("")
    print("")
    partes = []
    if contagem["REPROVOU"]:
        partes.append("reprovou em %s" % ", ".join(g.chave for g in resultados if g.status == "REPROVOU"))
    if contagem["AVISO"]:
        partes.append("aviso em %s" % ", ".join(g.chave for g in resultados if g.status == "AVISO"))
    if contagem["PULADO"]:
        partes.append("pulou %s%s" % (
            ", ".join(g.chave for g in resultados if g.status == "PULADO"),
            "" if args.estrito else " (não bloqueia; com --estrito, bloqueia)"))
    if not partes and valeram:
        partes.append("os %d gates passaram" % valeram)
    if contagem["NÃO SE APLICA"]:
        partes.append("não se aplica: %s" % ", ".join(g.chave for g in resultados if g.status == "NÃO SE APLICA"))
    print("  %s  ·  %s" % (veredito, "; ".join(partes)))
    if reprovou:
        print("  Conserte e confira de novo antes de mandar para a revisão.")
    elif contagem["PULADO"]:
        print("  O que foi pulado não foi conferido: gere os arquivos que faltam e rode de novo.")
    print("")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
