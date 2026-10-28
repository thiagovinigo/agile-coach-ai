#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audio.py  ·  o som do corte: a fala, os efeitos nos tempos da tela e o volume final

O compositor renderiza o reel mudo e anota no eventos.json cada coisa que acontece
na tela, com o seu tempo (MOTOR.md seção 2.4). Este script faz o resto do som e
fecha o arquivo de entrega, em quatro passos:

  efeitos   um som da biblioteca (componentes/sons/) para cada evento com "som".
            O ponto forte do som, que o script acha sozinho em cada arquivo, cai
            em cima do tempo do evento: o whoosh começa uns 0,2 s antes da
            transição e passa por ela no auge, a subida termina no evento.
            Quem fica (nesta ordem, o evento de maior peso primeiro e, no
            empate, o mais cedo):
              - dois sons a menos de 0,25 s um do outro viram um só, porque som
                encavalado soa como erro, e não como ritmo;
              - a mesma peça (o alvo sem o sufixo: "c3-maos-2-mao-1" é a peça
                "c3-maos-2") toca no máximo um som a cada 1,5 s.
            O evento pede a família ("whoosh") e o script escolhe o arquivo: o
            base (whoosh.wav) ou uma variação (whoosh-1.wav ...), por um sorteio
            fixo pelo hash do instante e do alvo do evento, nunca o mesmo arquivo
            em dois eventos seguidos da mesma família. Cada evento ganha ainda
            uma diferença pequena de tom (até 1 semitom para cima ou para baixo)
            e de volume (de -2 a +1 dB), fixa pelo mesmo hash. O mesmo corte sai
            sempre igual. "som": "whoosh-2" pede o arquivo exato, sem sorteio.
            E nenhum efeito em cima da sílaba tônica da palavra destacada (4.3):
            a região forte do som (a até 6 dB do auge) não cruza os 60 ms de cada
            lado da vogal tônica, estimada por regra do português. Se cruza, o som
            é adiantado até terminar antes do ataque da palavra, ou antes da
            tônica, no máximo 80 ms; se não dá, toca 6 dB mais baixo no lugar.
            Palavra destacada é a da "enfase" da legenda e a que o plano mostra
            grande na tela enquanto é falada (docs-4/gates-4-3.md).

  trilha    opcional: a música de fundo, declarada no cenas.json ou passada com
            --musica. O volume dela é medido contra a voz, como o dos efeitos:
            18 dB abaixo do volume médio da fala, e mais 6 dB abaixo enquanto a
            voz fala (o ducking). Ela só volta a subir numa pausa de 1,2 s ou
            mais. Mais curta que o reel, entra em loop com um cruzamento curto;
            mais longa, é aparada. Entra e sai em fade.

  volume    loudnorm em duas passadas: a primeira mede, a segunda aplica com os
            números medidos. Assim o ganho fica linear (o mesmo do começo ao fim,
            sem bombear) sempre que o pico permite. Alvo: -14 LUFS integrado, pico
            verdadeiro de -1 dBTP e LRA 11, o que as redes esperam.

  entrega   se o video.mp4 do compositor já está na pasta do corte, o som entra
            nele: vídeo copiado sem recompressão, áudio AAC 192k, faststart, e o
            arquivo sai em projetos/<video>/corte-NN/corte-NN.mp4, sozinho na pasta.
            A entrega é medida de novo depois do AAC, que sobe um pouco os picos
            entre amostras; se ela passar de -1 dBTP, o volume final é refeito
            com a folga que faltou e o arquivo é montado outra vez.

O volume dos efeitos é medido contra a voz, nunca em número solto, porque uma
gravação chega a -24 LUFS e outra a -10. A voz é medida pelo LUFS integrado do
fala.mp4; o efeito, pelo seu momento mais forte numa janela de 100 ms, com a mesma
ponderação K do LUFS. "--efeitos-db -20" quer dizer: no auge, o efeito fica 20 dB
abaixo do volume médio da voz. Eventos de peso 2 ficam mais 2 dB abaixo e os de
peso 1, mais 4 dB, porque um destaque que acende não pode soar como uma cena nova
(a pesquisa da 4.0 põe os efeitos de 10 a 18 dB abaixo da voz e o hit do herói a
4 a 8 dB: com o -20 do padrão e o ajuste por peso, a fábrica fica do lado
discreto disso). Depois de tudo, o script diz a densidade (um efeito a cada
quantos segundos) e avisa quando ela passa de um a cada 1,5 s no reel inteiro.
Para cada efeito o script imprime a folga da voz sobre ele naquele ponto; se a voz
está falando e a folga fica abaixo de 6 dB, ele avisa, porque ali o efeito começa
a encobrir a fala.

A trilha mora no cenas.json, numa chave de topo ao lado de "cenas":

  "trilha": { "arquivo": "componentes/trilhas/calma-piano-01.mp3", "volume_db": -18,
              "ducking": true, "entra": 0.0, "fade_entrada": 0.6, "fade_saida": 1.2,
              "inicio_no_arquivo": 0.0 }

  arquivo            o único obrigatório. Relativo à pasta do corte ou à raiz do
                     pacote, ou absoluto; qualquer formato que o ffmpeg leia.
  volume_db          quanto a trilha fica abaixo da voz sem o ducking (padrão -18):
                     é o nível dela nas pausas longas e antes de a voz começar.
  ducking            true abaixa mais 6 dB enquanto a voz fala e nas pausas curtas;
                     false desliga; um número é a profundidade em dB (de 0 a 24).
  entra              o segundo do reel em que a trilha começa (padrão 0).
  fade_entrada       segundos de fade a partir do "entra" (padrão 0,6).
  fade_saida         segundos de fade até o fim do reel (padrão 1,2).
  inicio_no_arquivo  de que segundo do arquivo a trilha começa a tocar (padrão 0),
                     para pular uma introdução; o loop repete a partir daí.

"trilha": "componentes/trilhas/x.mp3" é atalho para só o arquivo, com o resto no
padrão. Sem a chave, ou com "trilha": false, o som sai como sempre saiu: voz e
efeitos. A pasta componentes/trilhas/ diz que música pode entrar (LEIA.md).

O ducking tem profundidade fixa e é decidido pausa a pausa, com a voz como chave. A
voz é lida em quadros de 10 ms (ponderação K; conta como presente a até 24 dB do seu
LUFS), e a trilha fica exatamente a profundidade pedida abaixo do nível dela do
começo ao fim de cada trecho de fala. Uma pausa só solta a trilha se tiver 1,2 s ou
mais: 0,25 s de espera depois da última sílaba, 0,5 s de subida em cosseno, pelo
menos 0,25 s lá em cima e 0,2 s de descida que termina quando a voz volta. Pausa mais
curta não mexe na trilha. Nada de compressor nem portão, porque os dois só sabem que
a pausa é longa depois que ela já durou: o compressor seguia cada sílaba (de -4 a
-9 dB dentro da mesma frase), e o portão do ffmpeg, segurando 0,35 s, subia a trilha
4 dB em 100 ms num silêncio de 0,38 s e a derrubava em menos de 50 ms quando a voz
voltava. Os dois bombeiam. Aqui o script tem a fala inteira antes de misturar, então
pode olhar o fim da pausa antes de decidir.

Entradas, na pasta do corte (projetos/<video>/materiais-de-trabalho/corte-NN/):

  fala.mp4      o áudio da fala (obrigatório)
  eventos.json  os eventos com "som" (obrigatório, a não ser com --sem-efeitos)
  cenas.json    o plano; daqui saem a "trilha" e as palavras destacadas (opcional)
  video.mp4     o reel mudo do compositor (opcional; sem ele, sai só o wav)
  palavras-corte.json  as palavras com tempo, para a sílaba tônica (opcional)

Saídas: audio-final.wav (48 kHz, estéreo, 16 bits) e sons.json (a agenda dos
efeitos: tempo, arquivo, volume, folga da voz e tônica de cada um, que o gate de
som do conferir_reel.py lê) na pasta do corte e, havendo vídeo,
projetos/<video>/corte-NN/corte-NN.mp4.

Uso:

    flow-reels produzir/audio --projeto projetos/<video> --corte 01
    flow-reels produzir/audio --projeto projetos/<video> --corte 01 --musica componentes/trilhas/x.mp3
    flow-reels produzir/audio --projeto projetos/<video> --corte 01 --sem-trilha
    flow-reels produzir/audio --projeto projetos/<video> --corte 01 --sem-efeitos --so-audio
    flow-reels produzir/audio --projeto projetos/<video> --corte 01 --lufs -14 --efeitos-db -16

--sem-efeitos  só a voz (e a trilha, se houver).
--musica       troca o arquivo da trilha do cenas.json (ou põe uma, se ele não tem);
               o resto da trilha vem do cenas.json ou do padrão.
--musica-db    troca o volume_db da trilha: quanto ela fica abaixo da voz sem o
               ducking (padrão -18). Num corte sem trilha, avisa que não mudou nada.
--sem-trilha   ignora a trilha do cenas.json, para ouvir o corte sem ela. Com
               --musica ou --musica-db junto, é erro de uso.
--lufs         volume integrado final (padrão -14).
--efeitos-db   quanto os efeitos ficam abaixo da voz, no auge (padrão -20).
--so-audio     gera só o audio-final.wav, mesmo havendo video.mp4.
--sons         outra pasta de sons no lugar de componentes/sons/.

Saída 0 = gerou e o volume final conferiu. Saída 1 = o ffmpeg falhou ou o
resultado saiu fora do alvo (LUFS a mais de 1 LU do pedido ou pico acima de
-1 dBTP); com o áudio reprovado o corte-NN.mp4 não é gerado, e um que já exista
fica como estava. Saída 2 = erro de uso: pasta, arquivo ou opção errada.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


SR = 48000                  # toda a mistura acontece em 48 kHz, estéreo
DISTANCIA_MINIMA = 0.25     # dois efeitos mais perto que isso viram um só
ESPACO_POR_PECA = 1.5       # a mesma peça toca no máximo um som a cada 1,5 s
DENSIDADE_ALVO = 1.5        # no reel inteiro, a média de um efeito a cada 1,5 s ou mais (só aviso)
VARIA_TOM = 1.0             # semitons: cada evento toca até 1 st acima ou abaixo, fixo pelo hash
VARIA_GANHO = (-2.0, 1.0)   # dB: e um pouco mais baixo ou mais alto, também fixo pelo hash
AJUSTE_POR_PESO = {3: 0.0, 2: -2.0, 1: -4.0}
JANELA_NIVEL = 0.100        # janela do volume de curto prazo de um efeito
JANELA_PONTO = 0.020        # janela que acha o ponto forte de um som
JANELA_FOLGA = 0.200        # janela em volta do evento onde voz e efeito são comparados
FOLGA_MINIMA = 6.0          # dB que a voz precisa ficar acima do efeito, quando fala
TETO_DBTP = -1.0
LRA_ALVO = 11.0
TOLERANCIA_LUFS = 1.0
TOLERANCIA_PICO = 0.2       # o medidor do ebur128 e o limitador do loudnorm divergem um pouco
TRILHA_PADRAO = {           # o contrato da "trilha" no cenas.json, com os valores de quem não diz nada
    # -18 é o número do plano da 3.0 ("a -18 dB sob a voz, baixando mais quando você fala"). Com o
    # ducking, a trilha fica 24 dB abaixo da voz enquanto ela fala; o reel de referência tinha uns
    # 18 dB com a voz falando, e chegar nele pede "volume_db": -12.
    "volume_db": -18.0,
    "ducking": True,
    "entra": 0.0,
    "fade_entrada": 0.6,
    "fade_saida": 1.2,
    "inicio_no_arquivo": 0.0,
}
DUCKING_DB = 6.0            # o quanto a trilha abaixa a mais com a voz falando (ducking: true)
DUCKING_MAX = 24.0
QUADRO_VOZ = 0.010          # a voz é lida em quadros de 10 ms para saber onde ela soa
LIMIAR_DUCKING = 24.0       # a voz conta como presente a 24 dB do seu LUFS: sílaba fraca conta, ruído de sala não
EMENDA_VOZ = 0.10           # buraco menor que isso dentro da fala (a oclusão do "t", do "p") é fala
SOM_MINIMO = 0.05           # som isolado mais curto que isso (estalo de boca, clique) não é fala
SEGURA_DUCKING = 0.25       # depois da última sílaba, a trilha espera isso antes de subir
SOBE_DUCKING = 0.50         # a subida, em curva de cosseno: no máximo uns 2 dB a cada 100 ms
DESCE_DUCKING = 0.20        # a descida termina quando a voz volta, então começa antes dela
TOPO_MINIMO = 0.25          # a pausa só solta a trilha se ela puder ficar isso tudo lá em cima
PAUSA_QUE_SOLTA = SEGURA_DUCKING + SOBE_DUCKING + TOPO_MINIMO + DESCE_DUCKING   # 1,2 s
EMENDA_TRILHA = 0.25        # cruzamento entre uma volta do loop e a próxima
PISO_PONTAS = 40.0          # dB abaixo do trecho mais forte: o que fica abaixo disso nas pontas é silêncio
TRILHA_MINIMA = 1.0         # segundos de música de verdade para dar um loop
FOLGA_TRILHA_MINIMA = 12.0  # dB da voz sobre a trilha, falando; abaixo disso a trilha disputa com a fala

# 4.3 · efeito x sílaba tônica (docs-4/gates-4-3.md). O auge do efeito não cai na vogal tônica da palavra
# destacada, que é justamente o que ele mascararia; ele anda um pouco para antes ou, se não dá, baixa.
TONICA_RAIO = 0.060         # a zona tônica: 60 ms de cada lado do centro da vogal (pesquisa 04, seção 8)
FORTE_DB = 6.0              # a região forte de um som: onde a energia alisada fica a até 6 dB do auge
DESLOCA_MAX = 0.080         # o som anda no máximo 80 ms para antes do evento: 2,4 quadros, o "1 a 3 quadros antes"
FOLGA_ATAQUE = 0.005        # o fim da região forte fica pelo menos isso antes do alvo (ataque ou zona tônica)
BAIXA_TONICA_DB = -6.0      # quando andar não resolve, o efeito toca 6 dB mais baixo
PESO_TONICA = 1.4           # a sílaba tônica dura ~1,4x uma átona na fala corrida (modelo do tempo dentro da palavra)
NUCLEO_NA_SILABA = 0.55     # a vogal fica um pouco depois do meio da sílaba (a consoante de ataque vem antes)
TIPOS_GRANDES = {"palavra", "objeto3d", "titulo", "manchete", "selo"}   # sobreposições que mostram a palavra grande
TAMANHO_GRANDE = 80         # ou qualquer texto do plano com "tam" a partir disso

# Ponderação K da ITU-R BS.1770 em 48 kHz: o filtro de prateleira e o passa-alta RLB.
K_PRATELEIRA = ((1.53512485958697, -2.69169618940638, 1.19839281085285),
                (1.0, -1.69065929318241, 0.73248077421585))
K_PASSA_ALTA = ((1.0, -2.0, 1.0),
                (1.0, -1.99004745483398, 0.99007225036621))

NOME_DE_SOM = re.compile(r"^[A-Za-z0-9_-]+$")
VARIACAO = re.compile(r"^(?P<familia>.+)-(?P<k>\d+)$")       # whoosh-3: a variação 3 da família whoosh
PECA = re.compile(r"^(.+?-\d+)(?=-|$)")                       # c3-maos-2-mao-1 -> c3-maos-2

np = None  # carregado em main(), para o erro de numpy ausente sair em português


class Falha(Exception):
    """Erro com mensagem para a pessoa. codigo 2 = erro de uso, 1 = falha no meio do caminho."""

    def __init__(self, mensagem, codigo=1):
        super().__init__(mensagem)
        self.codigo = codigo


def erro(msg):
    sys.stdout.flush()
    print("  erro: " + msg, file=sys.stderr)


def aviso(msg):
    print("  aviso: " + msg)


def carregar_numpy():
    try:
        import numpy
    except ImportError:
        raise Falha("o numpy não está instalado neste Python.\n"
                    "        Rode com o Python do pacote: .venv/bin/python, ou instale com: pip install numpy", 2)
    return numpy


def curto(caminho):
    """O caminho relativo à pasta atual quando dá, para a saída caber na tela."""
    try:
        rel = os.path.relpath(caminho)
    except ValueError:
        return str(caminho)
    return rel if not rel.startswith("..") else str(caminho)


# ---------------------------------------------------------------------------
# Pastas
# ---------------------------------------------------------------------------

def achar_raiz():
    """A pasta de trabalho; sons e trilhas vêm de componentes/, da pasta ou do plugin."""
    return fabrica.raiz()


def resolver_projeto(raiz, pedido):
    alvo = Path(pedido)
    for caminho in (alvo, Path.cwd() / alvo, raiz / alvo, raiz / "projetos" / alvo):
        try:
            if caminho.is_dir():
                return caminho.resolve()
        except OSError:
            continue
    return None


def nome_do_corte(pedido):
    m = re.match(r"^(?:corte-)?0*(\d{1,3})$", str(pedido).strip())
    if not m or int(m.group(1)) == 0:
        return None
    return "%02d" % int(m.group(1))


# ---------------------------------------------------------------------------
# ffmpeg
# ---------------------------------------------------------------------------

def exigir_ferramentas():
    for nome in ("ffmpeg", "ffprobe"):
        if shutil.which(nome) is None:
            raise Falha("não encontrei o %s no PATH. Rode o instalar.sh (ou instalar.ps1) na raiz do pacote." % nome, 2)


def ffmpeg(argumentos, papel):
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-nostats"] + argumentos, capture_output=True)
    if proc.returncode != 0:
        fim = proc.stderr.decode("utf-8", "replace").strip().splitlines()[-8:]
        raise Falha("o ffmpeg parou ao %s. As últimas linhas dele:\n        %s"
                    % (papel, "\n        ".join(fim)))
    return proc


def sondar(caminho):
    proc = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json",
                           "-show_streams", "-show_format", str(caminho)],
                          capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except ValueError:
        return None


def fluxo(dados, tipo):
    for f in (dados or {}).get("streams", []):
        if f.get("codec_type") == tipo:
            return f
    return None


def duracao_de(dados):
    try:
        return float(dados["format"]["duration"])
    except (KeyError, TypeError, ValueError):
        return None


def ler_audio(caminho, papel, segundos=None, desde=None):
    """Decodifica o primeiro áudio do arquivo para 48 kHz, estéreo, ponto flutuante."""
    argumentos = ["-v", "error"]
    if desde:
        argumentos += ["-ss", "%.3f" % desde]
    argumentos += ["-i", str(caminho), "-map", "0:a:0", "-vn", "-ac", "2", "-ar", str(SR)]
    if segundos is not None:
        argumentos += ["-t", "%.3f" % segundos]
    argumentos += ["-f", "f32le", "-acodec", "pcm_f32le", "-"]
    bruto = np.frombuffer(ffmpeg(argumentos, papel).stdout, dtype="<f4")
    if bruto.size < 2:
        raise Falha("%s: o arquivo %s não tem áudio que se possa ler" % (papel, curto(caminho)), 2)
    return bruto[: bruto.size // 2 * 2].reshape(-1, 2).astype(np.float64)


def gravar_wav_float(caminho, x):
    """WAV em ponto flutuante de 32 bits: a mistura passa do 0 dBFS sem cortar até o loudnorm."""
    dados = np.ascontiguousarray(x, dtype="<f4").tobytes()
    canais = x.shape[1]
    with open(caminho, "wb") as arquivo:
        arquivo.write(b"RIFF" + struct.pack("<I", 4 + 26 + 12 + 8 + len(dados)) + b"WAVE")
        arquivo.write(b"fmt " + struct.pack("<IHHIIHHH", 18, 3, canais, SR, SR * canais * 4, canais * 4, 32, 0))
        arquivo.write(b"fact" + struct.pack("<II", 4, len(x)))
        arquivo.write(b"data" + struct.pack("<I", len(dados)) + dados)


def medir_volume(caminho):
    """LUFS integrado, LRA e pico verdadeiro, pelo filtro ebur128 do ffmpeg."""
    proc = ffmpeg(["-i", str(caminho), "-map", "0:a:0", "-af", "ebur128=peak=true:framelog=quiet",
                   "-f", "null", "-"], "medir o volume de %s" % Path(caminho).name)
    texto = proc.stderr.decode("utf-8", "replace")
    resumo = texto[texto.rfind("Summary:"):]

    def numero(padrao):
        m = re.search(padrao, resumo)
        if not m:
            return None
        return float("-inf") if "inf" in m.group(1) else float(m.group(1))

    return {"lufs": numero(r"\bI:\s*(-?inf|-?[\d.]+)\s*LUFS"),
            "lra": numero(r"\bLRA:\s*(-?inf|-?[\d.]+)\s*LU\b"),
            "pico": numero(r"\bPeak:\s*(-?inf|-?[\d.]+)\s*dBFS")}


# ---------------------------------------------------------------------------
# Medidas em numpy
# ---------------------------------------------------------------------------

def resposta_biquad(b, a, w):
    z1 = np.exp(-1j * w)
    z2 = z1 * z1
    return (b[0] + b[1] * z1 + b[2] * z2) / (a[0] + a[1] * z1 + a[2] * z2)


def ponderar_k(x):
    """Aplica a ponderação K no espectro (os dois biquads da BS.1770, de uma vez só)."""
    n = len(x)
    m = 1 << int(np.ceil(np.log2(n + SR // 2)))
    espectro = np.fft.rfft(x, m, axis=0)
    w = 2.0 * np.pi * np.arange(espectro.shape[0]) / m
    h = resposta_biquad(*K_PRATELEIRA, w) * resposta_biquad(*K_PASSA_ALTA, w)
    return np.fft.irfft(espectro * h[:, None], m, axis=0)[:n]


def para_lufs(media_quadrada):
    return -0.691 + 10.0 * np.log10(max(float(media_quadrada), 1e-20))


def nivel_curto(x):
    """O volume do som no seu momento mais forte: janela de 100 ms, ponderação K, em LUFS.

    Som mais curto que a janela é medido com silêncio em volta, porque o ouvido
    também soma a energia por perto de um décimo de segundo: um tique de 20 ms
    soa mais fraco do que um tom de 100 ms com o mesmo pico.
    """
    w = int(JANELA_NIVEL * SR)
    y = ponderar_k(np.pad(x, ((w, w), (0, 0))))
    p = np.sum(y ** 2, axis=1)
    acumulado = np.concatenate([[0.0], np.cumsum(p)])
    return para_lufs(np.max((acumulado[w:] - acumulado[:-w]) / w))


def nivel_no_trecho(x, de, ate):
    """LUFS (ponderação K, média de energia) do trecho [de, ate) em amostras."""
    de, ate = max(0, de), min(len(x), ate)
    if ate <= de:
        return float("-inf")
    folga = SR // 4                       # contexto para o filtro assentar antes do trecho
    a, b = max(0, de - folga), min(len(x), ate + folga)
    y = ponderar_k(x[a:b])[de - a: ate - a]
    return para_lufs(np.sum(np.mean(y ** 2, axis=0)))


def ponto_forte(x):
    """Onde o som é mais forte, em amostras desde o começo.

    É o máximo da energia alisada por uma janela de Hann de 20 ms. A janela de
    Hann, e não a retangular, porque num som mais curto que ela (o tique tem
    20 ms) a retangular forma um platô e o máximo cai em qualquer lugar dele.
    Num som de ataque seco o ponto forte fica a 1 ou 2 ms do começo; no whoosh,
    no auge da passagem; na subida, logo antes do fim.
    """
    return int(np.argmax(energia_alisada(x)))


def energia_alisada(x):
    """A energia do som alisada por uma janela de Hann de 20 ms, amostra a amostra."""
    w = int(JANELA_PONTO * SR) | 1
    p = np.sum(x ** 2, axis=1)
    h = np.hanning(w)
    return np.convolve(np.pad(p, (w // 2, w // 2)), h / h.sum(), mode="valid")


def regiao_forte(x, ponto):
    """(antes, depois): amostras, a partir do ponto forte, em que o som fica a até FORTE_DB do auge.

    É o trecho que mascara a fala. Num tique ou num clique tem 10 a 20 ms; num whoosh, o miolo da
    passagem; na subida e na energia, o fim, logo antes do evento.
    """
    e = energia_alisada(x)
    limiar = e[ponto] * 10.0 ** (-FORTE_DB / 10.0)
    abaixo_antes = np.nonzero(e[:ponto] < limiar)[0]
    abaixo_depois = np.nonzero(e[ponto:] < limiar)[0]
    a = int(abaixo_antes[-1]) + 1 if len(abaixo_antes) else 0
    b = ponto + int(abaixo_depois[0]) - 1 if len(abaixo_depois) else len(e) - 1
    return a - ponto, b - ponto


def rampa(n, sobe=True):
    r = 0.5 - 0.5 * np.cos(np.pi * np.arange(n) / max(n, 1))
    return (r if sobe else r[::-1])[:, None]


# ---------------------------------------------------------------------------
# Efeitos
# ---------------------------------------------------------------------------

def ler_eventos(caminho):
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Falha("não consegui ler o %s: %s" % (curto(caminho), e), 2)
    lista = dados.get("eventos") if isinstance(dados, dict) else None
    if not isinstance(lista, list):
        raise Falha("o %s não tem a lista \"eventos\" (o formato está no MOTOR.md, seção 2.4)" % curto(caminho), 2)
    eventos, ruins = [], 0
    for e in lista:
        if not isinstance(e, dict):
            ruins += 1
            continue
        som = e.get("som")
        if som in (None, "", False):
            continue
        try:
            t = float(e["t"])
            peso = min(3, max(1, int(e.get("peso", 1))))   # o contrato vai de 1 a 3
        except (KeyError, TypeError, ValueError):
            ruins += 1
            continue
        eventos.append({"t": t, "tipo": str(e.get("tipo", "?")), "peso": peso,
                        "alvo": str(e.get("alvo", "")), "som": str(som)})
    duracao = dados.get("duracao")
    return (float(duracao) if isinstance(duracao, (int, float)) else None), eventos, ruins


def carregar_sons(pasta, nomes):
    """Lê as famílias pedidas: o base (<nome>.wav) e as variações (<nome>-1.wav, <nome>-2.wav...).

    Devolve a biblioteca, {arquivo sem .wav: dados}, e as famílias, {nome pedido: [arquivos que
    tocam]}. Um nome que já é uma variação existente ("whoosh-2") pede só aquele arquivo. Um som
    mudo fica marcado como None e fora da família: a régua de volume o subiria 70 dB e traria
    só ruído. Família sem arquivo nenhum fica com a lista vazia; com arquivos, mas todos mudos, None.
    """
    biblioteca, familias = {}, {}
    for nome in sorted(nomes):
        if not NOME_DE_SOM.match(nome):
            familias[nome] = []
            continue
        if VARIACAO.match(nome) and (pasta / (nome + ".wav")).is_file():
            arquivos = [nome]
        else:
            variacoes = []
            for caminho in pasta.glob(glob_escapado(nome) + "-*.wav"):
                m = VARIACAO.match(caminho.stem)
                if m and m.group("familia") == nome:
                    variacoes.append((int(m.group("k")), caminho.stem))
            arquivos = ([nome] if (pasta / (nome + ".wav")).is_file() else []) + [a for _, a in sorted(variacoes)]
        for arquivo in arquivos:
            if arquivo not in biblioteca:
                x = ler_audio(pasta / (arquivo + ".wav"), "ler o som %s.wav" % arquivo)
                nivel = nivel_curto(x)
                ponto = ponto_forte(x)
                biblioteca[arquivo] = ({"x": x, "ponto": ponto, "nivel": nivel, "forte": regiao_forte(x, ponto)}
                                       if nivel > -70.0 else None)
        tocam = [a for a in arquivos if biblioteca[a] is not None]
        familias[nome] = tocam if tocam or not arquivos else None
    return biblioteca, familias


def glob_escapado(nome):
    """O nome como padrão do glob, sem que um [ ou um * do nome vire curinga."""
    return re.sub(r"([\[\]*?])", r"[\1]", nome)


def peca_do_evento(e):
    """A peça que fez o evento: o alvo sem o sufixo de dentro da peça.

    O motor nomeia as peças "<cena>-<tipo>-<n>" (c3-maos-2) e os pedaços delas com mais um
    sufixo (c3-maos-2-mao-1, c2-nuvem-1-conta). Alvo sem esse desenho (a transição "desfoque",
    a câmera "c5-separa") é a peça inteira. Alvo vazio não agrupa com nada.
    """
    alvo = e["alvo"].strip()
    if not alvo:
        return None
    m = PECA.match(alvo)
    return m.group(1) if m else alvo


def escolher(eventos, familias, duracao):
    """Fica um som por vez.

    Em ordem de prioridade (o maior peso primeiro e, no empate, o mais cedo), cada evento entra
    se não houver outro já aceito a menos de 0,25 s (de qualquer peça) nem outro da mesma peça a
    menos de 1,5 s.
    """
    validos, fora = [], []
    for e in eventos:
        if familias.get(e["som"]) is None:
            fora.append((e, "os arquivos de %s na biblioteca estão mudos" % e["som"]))
        elif not familias[e["som"]]:
            fora.append((e, "não há %s.wav (nem %s-N.wav) na biblioteca de sons" % (e["som"], e["som"])))
        elif not 0.0 <= e["t"] <= duracao:
            fora.append((e, "fora do vídeo, que tem %.2f s" % duracao))
        else:
            validos.append(dict(e, peca=peca_do_evento(e)))
    aceitos = []
    for e in sorted(validos, key=lambda e: (-e["peso"], e["t"])):
        vizinho = next((a for a in aceitos if abs(a["t"] - e["t"]) < DISTANCIA_MINIMA), None)
        irmao = None if e["peca"] is None else next(
            (a for a in aceitos if a["peca"] == e["peca"] and abs(a["t"] - e["t"]) < ESPACO_POR_PECA), None)
        if vizinho:
            fora.append((e, "a %.2f s do %s de %.2f s, de peso %d"
                         % (abs(vizinho["t"] - e["t"]), vizinho["som"], vizinho["t"], vizinho["peso"])))
        elif irmao:
            fora.append((e, "a mesma peça (%s) já toca o %s de %.2f s, a %.2f s (no máximo um som a cada %.1f s por peça)"
                         % (e["peca"], irmao["som"], irmao["t"], abs(irmao["t"] - e["t"]), ESPACO_POR_PECA)))
        else:
            aceitos.append(e)
    return sorted(aceitos, key=lambda e: e["t"]), sorted(fora, key=lambda par: par[0]["t"])


def hash_do_evento(e):
    """Um número fixo para o evento: o mesmo instante, alvo e som dão sempre o mesmo sorteio."""
    chave = "%.3f|%s|%s" % (e["t"], e["alvo"], e["som"])
    return int.from_bytes(hashlib.sha256(chave.encode("utf-8")).digest()[:8], "big")


def variar(aceitos, familias):
    """Escolhe o arquivo de cada evento e a pequena diferença de tom e de volume dele.

    O arquivo sai do hash do evento; se for o mesmo do evento anterior da mesma família, passa
    para outro da lista, também pelo hash. Tom e volume vêm de outros pedaços do mesmo hash.
    """
    anterior = {}
    for e in aceitos:                      # já em ordem de tempo
        opcoes = familias[e["som"]]
        familia = familia_do_arquivo(opcoes[0])   # "whoosh-2" pedido pelo nome também é da família whoosh
        h = hash_do_evento(e)
        i = h % len(opcoes)
        if len(opcoes) > 1 and opcoes[i] == anterior.get(familia):
            i = (i + 1 + (h >> 16) % (len(opcoes) - 1)) % len(opcoes)
        e["arquivo"], e["familia"] = opcoes[i], familia
        anterior[familia] = opcoes[i]
        e["semitons"] = ((h >> 24) % 10001 / 10000.0 * 2.0 - 1.0) * VARIA_TOM
        e["ganho_db"] = VARIA_GANHO[0] + (h >> 40) % 10001 / 10000.0 * (VARIA_GANHO[1] - VARIA_GANHO[0])
    return aceitos


def familia_do_arquivo(arquivo):
    m = VARIACAO.match(arquivo)
    return m.group("familia") if m else arquivo


def repetidos_em_seguida(colocados):
    """Quantas vezes o mesmo arquivo tocou em dois eventos seguidos da mesma família."""
    ultimo, conta = {}, 0
    for c in colocados:
        conta += ultimo.get(c["familia"]) == c["arquivo"]
        ultimo[c["familia"]] = c["arquivo"]
    return conta


# ---------------------------------------------------------------------------
# A sílaba tônica da palavra destacada (4.3)
# ---------------------------------------------------------------------------

VOGAIS = set("aeiouyáéíóúâêôãõàü")
ACENTO_TONICO = set("áéíóúâêô")
TIL = set("ãõ")
# palavras que não são destaque nem quando o plano as põe na tela (artigo, preposição, conector)
SEM_DESTAQUE = set("a o e as os um uma uns umas de da do das dos em no na nos nas por pra para pro com sem "
                   "que se ao aos ou mas mais ja eu voce ele ela isso esse essa este esta aqui ai la so "
                   "nao sim me te lhe the of and to".split())
# nomes de fora que a regra do português erra (ela lê "Codex" como co-DEX e "Gemini" como ge-mi-NI):
# (fração do tempo da palavra em que a sílaba tônica começa, em que termina). Chave sem acento, minúscula.
TONICA_CONHECIDA = {
    "codex": (0.0, 0.55), "google": (0.0, 0.6), "gemini": (0.0, 0.4), "gems": (0.0, 1.0),
    "openrouter": (0.4, 0.75), "openai": (0.7, 1.0), "anthropic": (0.3, 0.65), "nvidia": (0.25, 0.65),
    "salesforce": (0.0, 0.55), "gartner": (0.0, 0.55), "linkedin": (0.0, 0.5), "notebooklm": (0.8, 1.0),
    "omniroute": (0.0, 0.4), "headroom": (0.0, 0.5), "observer": (0.3, 0.65), "setup": (0.0, 0.5),
    "plugin": (0.0, 0.5), "plugins": (0.0, 0.5), "prompt": (0.0, 1.0), "task": (0.0, 1.0),
    "boost": (0.0, 1.0), "bites": (0.0, 1.0), "badge": (0.0, 1.0), "bytez": (0.0, 1.0),
    "qwen": (0.0, 1.0), "kimi": (0.0, 0.5), "llama": (0.0, 0.55), "claude": (0.0, 0.6),
    "chatgpt": (0.85, 1.0), "github": (0.0, 0.5), "cursor": (0.0, 0.55), "deepseek": (0.0, 0.5),
}


def chave_de_palavra(texto):
    """A palavra para comparar: minúscula, sem acento e só com letra e número ("GLM," = "glm")."""
    t = unicodedata.normalize("NFD", str(texto).lower())
    return "".join(ch for ch in t if unicodedata.category(ch) != "Mn" and ch.isalnum())


def nucleos(palavra):
    """As sílabas da palavra pelo núcleo vocálico: [(início, fim)] em índices das letras.

    Regra do português, sem dicionário: vogais seguidas são um núcleo só quando a segunda é i ou u
    átono (ditongo: pai, meu, muito, partiu) ou no ão/ãe/õe; o resto é hiato (di-a, sa-ú-de). O u do
    que/qui/gue/gui é da consoante. Erra em alguns hiatos sem acento (ra-i-nha), o que mexe pouco no
    tempo estimado da tônica.
    """
    w = palavra.lower()
    vogal = [ch in VOGAIS for ch in w]
    for i in range(1, len(w) - 1):
        if w[i] in "uü" and w[i - 1] in "qg" and w[i + 1] in "eiéêí":
            vogal[i] = False
    saida, i = [], 0
    while i < len(w):
        if not vogal[i]:
            i += 1
            continue
        j = i + 1
        if j < len(w) and vogal[j]:         # um núcleo leva no máximo uma semivogal
            antes, agora = w[i], w[j]
            if (agora in "iu" and antes != agora) or (antes in TIL and agora in "oe"):
                j += 1
        saida.append((i, j))
        i = j
    return saida


def tonica_na_palavra(texto):
    """(início, fim) da sílaba tônica como fração do tempo da palavra, estimada por regra.

    1. sigla de até 4 letras maiúsculas (API, MCP, IA): soletrada, a tônica é a última letra;
    2. nome de fora conhecido (TONICA_CONHECIDA);
    3. acento agudo ou circunflexo marca a tônica (proparoxítona sempre tem); senão o til (não, irmão);
    4. sem acento: terminada em a, e, o (com s), am, em, ens é paroxítona; o resto (i, u, is, us, r, l,
       z, x, n, im, um, om, ns) é oxítona; uma sílaba só é ela mesma.
    O tempo da palavra é dividido entre as sílabas com a tônica pesando 1,4.
    """
    letras = "".join(ch for ch in str(texto) if ch.isalpha())
    if not letras:
        return None
    if letras.isupper() and 2 <= len(letras) <= 4:
        return ((len(letras) - 1) / len(letras), 1.0)
    chave = chave_de_palavra(letras)
    if chave in TONICA_CONHECIDA:
        return TONICA_CONHECIDA[chave]
    w = letras.lower()
    silabas = nucleos(w)
    n = len(silabas)
    if n <= 1:
        return (0.0, 1.0)
    k = next((i for i, (a, b) in enumerate(silabas) if set(w[a:b]) & ACENTO_TONICO), None)
    if k is None:
        k = next((i for i, (a, b) in enumerate(silabas) if set(w[a:b]) & TIL), None)
    if k is None:
        k = n - 2 if re.search(r"(a|e|o|as|es|os|am|em|ens)$", w) else n - 1
    pesos = [PESO_TONICA if i == k else 1.0 for i in range(n)]
    total = sum(pesos)
    inicio = sum(pesos[:k]) / total
    return (inicio, inicio + pesos[k] / total)


def palavras_de_destaque(pasta):
    """As palavras destacadas do corte, cada uma com o tempo dela e a zona da vogal tônica.

    Destacada é a palavra falada que o plano destaca: está na "enfase" da legenda (a do reel ou a de
    uma cena), ou aparece grande na tela enquanto é falada (sobreposição palavra, objeto3d, título,
    manchete, selo ou texto com "tam" de 80 px para cima), que é a palavra do evento quando o evento
    é dela. Artigo, preposição e conector não contam. Sem palavras-corte.json, nenhuma.
    """
    try:
        dados = json.loads((pasta / "palavras-corte.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    palavras = dados.get("palavras") if isinstance(dados, dict) else dados
    if not isinstance(palavras, list):
        return []
    try:
        plano = json.loads((pasta / "cenas.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        plano = {}
    if not isinstance(plano, dict):
        plano = {}
    enfase, grandes = set(), []

    def ler_legenda(leg):
        if isinstance(leg, dict):
            for p in leg.get("enfase") or []:
                enfase.add(chave_de_palavra(p))

    def ler_textos(no, herdado=None):
        if isinstance(no, dict):
            t0 = no.get("t", herdado[0] if herdado else None)
            t1 = no.get("ate", herdado[1] if herdado else None)
            texto = no.get("texto")
            if not isinstance(texto, str) and isinstance(no.get("valor"), (int, float)):
                texto = "%s%s" % (no["valor"], no.get("sufixo") or "")      # a palavra que conta: "80 MODELOS"
            tam = no.get("tam")
            if isinstance(texto, str) and (no.get("tipo") in TIPOS_GRANDES
                                           or (isinstance(tam, (int, float)) and tam >= TAMANHO_GRANDE)):
                if isinstance(t0, (int, float)):
                    fim = t1 if isinstance(t1, (int, float)) else t0 + 2.0
                    grandes.append(({chave_de_palavra(x) for x in texto.split()}, float(t0), float(fim)))
            for v in no.values():
                ler_textos(v, (t0, t1))
        elif isinstance(no, list):
            for v in no:
                ler_textos(v, herdado)

    ler_legenda(plano.get("legenda"))
    ler_textos(plano.get("sobre"))
    for cena in plano.get("cenas") or []:
        if isinstance(cena, dict):
            ler_legenda(cena.get("legenda"))
            janela = (cena.get("inicio"), cena.get("fim"))
            ler_textos(cena.get("sobre"), janela)
            ler_textos(cena.get("conteudo"), janela)
    enfase.discard("")

    saida = []
    for p in palavras:
        if not isinstance(p, dict):
            continue
        try:
            ini, fim = float(p["inicio"]), float(p["fim"])
        except (KeyError, TypeError, ValueError):
            continue
        texto = str(p.get("texto", ""))
        chave = chave_de_palavra(texto)
        if not chave or chave in SEM_DESTAQUE or fim <= ini:
            continue
        motivos = []
        if chave in enfase:
            motivos.append("ênfase da legenda")
        if any(chave in toks and t0 - 1.0 <= ini <= t1 + 0.5 for toks, t0, t1 in grandes):
            motivos.append("grande na tela")
        if not motivos:
            continue
        fracao = tonica_na_palavra(texto)
        if fracao is None:
            continue
        s0, s1 = ini + fracao[0] * (fim - ini), ini + fracao[1] * (fim - ini)
        centro = s0 + NUCLEO_NA_SILABA * (s1 - s0)
        z0, z1 = max(s0, centro - TONICA_RAIO), min(s1, centro + TONICA_RAIO)
        saida.append({"texto": texto, "inicio": ini, "fim": fim, "centro": round(centro, 4),
                      "zona": (round(z0, 4), round(z1, 4)), "motivo": " e ".join(motivos)})
    return saida


def afastar_da_tonica(aceitos, biblioteca, destaques, corrigir=True):
    """Tira o auge de cada efeito de cima da vogal tônica das palavras destacadas.

    Para cada efeito (já com o arquivo e o tom escolhidos), a região forte dele (FORTE_DB do auge)
    é comparada com a zona tônica de cada palavra destacada. Se cruza, em ordem:
      1. adianta o som até a região forte terminar antes do ataque da palavra, se isso for até 80 ms;
      2. senão, adianta até ela terminar antes da zona tônica, também até 80 ms;
      3. senão (ou se adiantar cairia noutra tônica, antes do começo do reel, ou a menos de 0,25 s do
         efeito anterior), o efeito toca BAIXA_TONICA_DB mais baixo, no lugar.
    Determinístico: só depende dos tempos. Com corrigir=False, só anota quem cruza (é o que um
    audio.py de antes da 4.3 tocou, para o gate medir a entrega antiga).
    """
    anterior = None
    for e in aceitos:                                   # já em ordem de tempo
        som = biblioteca[e["arquivo"]]
        fator = 2.0 ** (e["semitons"] / 12.0)
        fa, fb = som["forte"][0] / fator / SR, som["forte"][1] / fator / SR
        e.update(desloca=0.0, baixa_db=0.0, tonica=None, forte=(fa, fb))

        def cruza(t):
            return [d for d in destaques if t + fa < d["zona"][1] and t + fb > d["zona"][0]]

        batidas = cruza(e["t"])
        if batidas:
            d = min(batidas, key=lambda x: x["zona"][0])
            e["tonica"] = {"palavra": d["texto"], "centro": d["centro"], "zona": list(d["zona"]),
                           "motivo": d["motivo"], "acao": "nenhuma"}
            if corrigir:
                fim_forte = e["t"] + fb
                opcoes = [fim_forte - d["inicio"] + FOLGA_ATAQUE, fim_forte - d["zona"][0] + FOLGA_ATAQUE]
                for i, recuo in enumerate(opcoes):
                    novo = e["t"] - recuo
                    if (0.0 < recuo <= DESLOCA_MAX + 1e-9 and novo + fa >= 0.0 and not cruza(novo)
                            and (anterior is None or novo - anterior >= DISTANCIA_MINIMA)):
                        e["desloca"] = -recuo
                        e["tonica"]["acao"] = "antes do ataque" if i == 0 else "antes da tônica"
                        break
                else:
                    e["baixa_db"] = BAIXA_TONICA_DB
                    e["tonica"]["acao"] = "baixou"
        e["t_som"] = e["t"] + e["desloca"]
        anterior = e["t_som"]
    return aceitos


def mudar_tom(x, semitons):
    """Toca o som mais rápido (mais agudo) ou mais devagar (mais grave), como fita: muda a duração junto."""
    fator = 2.0 ** (semitons / 12.0)
    if abs(fator - 1.0) < 1e-4:
        return x, 1.0
    n = len(x)
    pos = np.clip(np.arange(max(2, int(round(n / fator)))) * fator, 0.0, n - 1.0)
    origem = np.arange(n)
    return np.stack([np.interp(pos, origem, x[:, c]) for c in range(x.shape[1])], axis=1), fator


def posicionar(aceitos, biblioteca, n, voz_lufs, efeitos_db):
    """Monta a pista de efeitos: cada som com o ponto forte no tempo do evento e o volume medido contra a voz.

    O tempo é o t_som (o do evento, adiantado pelo afastar_da_tonica quando o auge cairia na tônica
    de uma palavra destacada) e o volume leva o baixa_db de quem não pôde andar.
    """
    pista = np.zeros((n, 2))
    colocados = []
    for e in aceitos:
        som = biblioteca[e["arquivo"]]
        x, fator = mudar_tom(som["x"], e["semitons"])
        ponto = int(round(som["ponto"] / fator))
        alvo = voz_lufs + efeitos_db + AJUSTE_POR_PESO[e["peso"]] + e["ganho_db"] + e.get("baixa_db", 0.0)
        trecho = x * 10.0 ** ((alvo - som["nivel"]) / 20.0)
        inicio = int(round(e.get("t_som", e["t"]) * SR)) - ponto
        a, b = max(0, -inicio), min(len(trecho), n - inicio)
        if b <= a:
            continue
        trecho = trecho[a:b].copy()
        if a > 0:                      # o começo do som ficaria antes do vídeo: corta com rampa
            k = min(len(trecho), int(0.005 * SR))
            trecho[:k] *= rampa(k)
        if b < len(x):                 # o fim passaria do vídeo: fecha com rampa
            k = min(len(trecho), int(0.010 * SR))
            trecho[len(trecho) - k:] *= rampa(k, sobe=False)
        pista[inicio + a: inicio + b] += trecho
        colocados.append(dict(e, comeca=max(0, inicio) / SR, termina=min(n, inicio + len(x)) / SR,
                              nivel=alvo - voz_lufs))
    return pista, colocados


def montar_efeitos(voz, voz_lufs, eventos, sons, efeitos_db, pasta, corrigir_tonica=True):
    """Os efeitos do corte, do eventos.json à pista: (pista, colocados, fora, destaques).

    É o passo 2 do processar, separado para o conferir_reel.py (gate de som) refazer a agenda de
    uma entrega antiga sem misturar nada.
    """
    n = len(voz)
    biblioteca, familias = carregar_sons(sons, {e["som"] for e in eventos})
    aceitos, fora = escolher(eventos, familias, n / SR)
    destaques = palavras_de_destaque(pasta)
    aceitos = afastar_da_tonica(variar(aceitos, familias), biblioteca, destaques, corrigir_tonica)
    pista, colocados = posicionar(aceitos, biblioteca, n, voz_lufs, efeitos_db)
    medir_folgas(colocados, voz, pista, voz_lufs)
    return pista, colocados, fora, destaques


def finito(v, casas=3):
    return None if v is None or not np.isfinite(v) else round(float(v), casas)


def agenda(pasta, colocados, fora, destaques, duracao, voz_lufs, efeitos_db, corrigiu, sem_efeitos=False):
    """O que o audio.py tocou, para o gate de som (conferir_reel.py) ler: o sons.json da pasta do corte."""
    def resumo_hash(nome):
        try:
            return hashlib.sha256((pasta / nome).read_bytes()).hexdigest()
        except OSError:
            return None

    lista = []
    for c in colocados:
        t_som = c.get("t_som", c["t"])
        fa, fb = c.get("forte", (0.0, 0.0))
        lista.append({"t": round(c["t"], 3), "t_som": round(t_som, 4), "desloca_ms": round(c.get("desloca", 0.0) * 1000, 1),
                      "baixa_db": c.get("baixa_db", 0.0), "arquivo": c["arquivo"], "familia": c["familia"],
                      "som": c["som"], "peso": c["peso"], "tipo": c["tipo"], "alvo": c["alvo"],
                      "semitons": round(c["semitons"], 3), "nivel_db": finito(c["nivel"], 2),
                      "folga_db": finito(c.get("folga"), 2), "fala": bool(c.get("fala")),
                      "comeca": round(c["comeca"], 4), "termina": round(c["termina"], 4),
                      "forte": [round(t_som + fa, 4), round(t_som + fb, 4)], "tonica": c.get("tonica")})
    return {
        "_leia": "Os efeitos que o audio.py pôs no audio-final.wav deste corte, com o tempo e o volume de cada um. "
                 "Escrito pelo audio.py; lido pelo gate de som do conferir_reel.py (docs-4/gates-4-3.md).",
        "versao": 1, "gerado_por": "audio.py 4.3", "sem_efeitos": sem_efeitos, "corrigiu_tonica": corrigiu,
        "eventos_sha256": resumo_hash("eventos.json"), "fala_sha256": resumo_hash("fala.mp4"),
        "duracao": round(duracao, 3), "voz_lufs": finito(voz_lufs, 2), "efeitos_db": efeitos_db,
        "parametros": {"tonica_raio_s": TONICA_RAIO, "forte_db": FORTE_DB, "desloca_max_s": DESLOCA_MAX,
                       "baixa_tonica_db": BAIXA_TONICA_DB, "distancia_minima_s": DISTANCIA_MINIMA},
        "efeitos": lista,
        "fora": [{"t": round(e["t"], 3), "som": e["som"], "alvo": e["alvo"], "motivo": m} for e, m in fora],
        "destaques": [{"texto": d["texto"], "inicio": d["inicio"], "fim": d["fim"], "centro": d["centro"],
                       "zona": list(d["zona"]), "motivo": d["motivo"]} for d in destaques],
    }


def gravar_agenda(pasta, dados):
    temporario = pasta / ".sons.json.tmp"
    temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(temporario, pasta / "sons.json")


def agenda_do_corte(pasta, raiz=None, efeitos_db=-20.0, corrigir_tonica=True, sons=None):
    """Refaz a agenda de efeitos de um corte sem misturar nem gravar nada (para o conferir_reel.py).

    Lê o fala.mp4, o eventos.json, o cenas.json e o palavras-corte.json da pasta, mede a voz e devolve
    o mesmo dicionário do sons.json. corrigir_tonica=False reproduz um audio.py de antes da 4.3.
    """
    global np
    if np is None:
        np = carregar_numpy()
    pasta = Path(pasta)
    raiz = Path(raiz) if raiz else achar_raiz()
    sons = Path(sons) if sons else fabrica.pasta("componentes/sons")
    voz = ler_audio(pasta / "fala.mp4", "ler o áudio do fala.mp4")
    voz_lufs = medir_volume(pasta / "fala.mp4")["lufs"]
    if voz_lufs is None or voz_lufs < -60.0:
        raise Falha("a fala está muda ou quase")
    _, eventos, _ = ler_eventos(pasta / "eventos.json")
    if eventos:
        _, colocados, fora, destaques = montar_efeitos(voz, voz_lufs, eventos, sons, efeitos_db, pasta, corrigir_tonica)
    else:
        colocados, fora, destaques = [], [], palavras_de_destaque(pasta)
    return agenda(pasta, colocados, fora, destaques, len(voz) / SR, voz_lufs, efeitos_db, corrigir_tonica)


def medir_folgas(colocados, voz, pista, voz_lufs):
    meia = int(JANELA_FOLGA * SR / 2)
    for c in colocados:
        centro = int(round(c.get("t_som", c["t"]) * SR))
        c["voz_no_ponto"] = nivel_no_trecho(voz, centro - meia, centro + meia)
        c["efeito_no_ponto"] = nivel_no_trecho(pista, centro - meia, centro + meia)
        c["folga"] = c["voz_no_ponto"] - c["efeito_no_ponto"]
        c["fala"] = c["voz_no_ponto"] > voz_lufs - 12.0   # a voz está falando ali, não é pausa


# ---------------------------------------------------------------------------
# Trilha
# ---------------------------------------------------------------------------

def numero_da_trilha(valor, campo, minimo=None, maximo=None):
    """Um campo numérico da trilha, conferido. bool é número para o Python, mas não para o contrato."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise Falha("no cenas.json, \"trilha.%s\" precisa ser um número (recebi %r)" % (campo, valor), 2)
    valor = float(valor)
    if (minimo is not None and valor < minimo) or (maximo is not None and valor > maximo):
        faixa = "de %g a %g" % (minimo, maximo) if maximo is not None else "a partir de %g" % minimo
        raise Falha("no cenas.json, \"trilha.%s\" vai %s (recebi %g)" % (campo, faixa, valor), 2)
    return valor


def achar_arquivo_da_trilha(pedido, lugares):
    """O primeiro lugar onde o arquivo existe: absoluto como veio, relativo em cada pasta da lista."""
    alvo = Path(os.path.expanduser(str(pedido)))
    candidatos = [alvo] if alvo.is_absolute() else [pasta / alvo for pasta in lugares]
    candidatos = [c for i, c in enumerate(candidatos) if c.absolute() not in [d.absolute() for d in candidatos[:i]]]
    for caminho in candidatos:
        if caminho.is_file():
            return caminho.resolve()
    raise Falha("não achei a trilha %s. Procurei em:\n        %s"
                % (pedido, "\n        ".join(curto(c) for c in candidatos)), 2)


def ler_trilha(pasta, raiz, args, duracao, avisos):
    """A trilha deste corte, já conferida e com os padrões, ou None.

    Vem da chave "trilha" do cenas.json; --musica troca o arquivo e --musica-db o volume.
    Caminho do cenas.json é relativo à pasta do corte (como as imagens do plano) ou à raiz
    do pacote (componentes/trilhas/...); o do --musica, também à pasta de onde se rodou.
    Erro de uso para aqui mesmo; aviso e nota vão para `avisos`, que o processar imprime
    depois do cabeçalho do corte, junto com o resto.
    """
    pedido, origem = None, "cenas.json"
    caminho_cenas = pasta / "cenas.json"
    if not args.sem_trilha and caminho_cenas.is_file():
        try:
            plano = json.loads(caminho_cenas.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            # o compor.py já teria parado num cenas.json quebrado; aqui só a trilha depende dele
            avisos.append(("aviso", "não consegui ler o %s (%s); sigo sem a trilha dele" % (curto(caminho_cenas), e)))
            plano = {}
        pedido = plano.get("trilha") if isinstance(plano, dict) else None
    if pedido in (None, False, ""):
        pedido = None
    elif isinstance(pedido, str):
        pedido = {"arquivo": pedido}
    elif not isinstance(pedido, dict):
        raise Falha("no cenas.json, \"trilha\" é um objeto com o \"arquivo\" (ou só o caminho, ou false)", 2)
    if args.musica:
        origem = "--musica" if pedido is None else "--musica, o resto do cenas.json"
        pedido = dict(pedido or {}, arquivo=args.musica)
    if pedido is None:
        if args.musica_db is not None:
            avisos.append(("aviso", "o --musica-db não mudou nada: este corte não tem trilha, nem no %s nem em "
                                    "--musica" % curto(caminho_cenas)))
        return None

    estranhas = sorted(set(pedido) - set(TRILHA_PADRAO) - {"arquivo"})
    if estranhas:
        avisos.append(("aviso", "a trilha do cenas.json tem campo(s) que o audio.py não conhece e ignorou: %s. "
                                "Os que valem: %s" % (", ".join(estranhas), ", ".join(["arquivo"] + list(TRILHA_PADRAO)))))
    arquivo = pedido.get("arquivo")
    if not isinstance(arquivo, str) or not arquivo.strip():
        raise Falha("no cenas.json, a \"trilha\" precisa do \"arquivo\" (por exemplo componentes/trilhas/<nome>.mp3)", 2)
    lugares = ([Path.cwd()] if args.musica else []) + [pasta, raiz, fabrica.plugin()]
    caminho = achar_arquivo_da_trilha(arquivo.strip(), lugares)
    dados = sondar(caminho)
    if not fluxo(dados, "audio"):
        raise Falha("a trilha %s não tem áudio que o ffmpeg leia" % curto(caminho), 2)

    t = {"caminho": caminho, "origem": origem, "duracao_arquivo": duracao_de(dados)}
    volume = pedido.get("volume_db", TRILHA_PADRAO["volume_db"])
    if args.musica_db is not None:
        volume = args.musica_db
    volume = numero_da_trilha(volume, "volume_db", -60.0, 60.0)
    if volume > 0:
        avisos.append(("nota", "\"trilha.volume_db\" é quanto ela fica ABAIXO da voz; entendi %.0f como -%.0f"
                               % (volume, volume)))
        volume = -volume
    t["volume_db"] = volume
    ducking = pedido.get("ducking", TRILHA_PADRAO["ducking"])
    if ducking is True:
        t["ducking_db"] = DUCKING_DB
    elif ducking in (False, None):
        t["ducking_db"] = 0.0
    elif isinstance(ducking, (int, float)) and abs(ducking) <= DUCKING_MAX:
        t["ducking_db"] = float(abs(ducking))          # -8 e 8 dizem a mesma coisa: quanto a trilha abaixa
    else:
        raise Falha("no cenas.json, \"trilha.ducking\" é true, false ou a profundidade em dB, de 0 a %.0f "
                    "(recebi %r)" % (DUCKING_MAX, ducking), 2)
    for campo in ("entra", "fade_entrada", "fade_saida", "inicio_no_arquivo"):
        t[campo] = numero_da_trilha(pedido.get(campo, TRILHA_PADRAO[campo]), campo, 0.0)
    if t["entra"] > duracao - TRILHA_MINIMA:
        raise Falha("\"trilha.entra\" em %.2f s deixa menos de %.0f s de trilha num reel de %.2f s"
                    % (t["entra"], TRILHA_MINIMA, duracao), 2)
    dur = t["duracao_arquivo"]
    if dur is not None and dur < TRILHA_MINIMA:
        raise Falha("a trilha %s tem %.2f s; trilha de fundo precisa de pelo menos %.0f s de música"
                    % (caminho.name, dur, TRILHA_MINIMA), 2)
    if dur is not None and t["inicio_no_arquivo"] > dur - TRILHA_MINIMA:
        raise Falha("\"trilha.inicio_no_arquivo\" em %.2f s, e a trilha %s tem %.2f s"
                    % (t["inicio_no_arquivo"], caminho.name, dur), 2)
    return t


def aparar_pontas(m):
    """Tira o silêncio das pontas antes do loop: a trilha que termina num rabo de reverb ou em
    silêncio faria um buraco no fundo a cada volta."""
    w = int(0.05 * SR)
    q = len(m) // w
    if q < 4:
        return m
    energia = np.mean(m[: q * w].reshape(q, w, 2) ** 2, axis=(1, 2))
    vivos = np.nonzero(energia > energia.max() * 10.0 ** (-PISO_PONTAS / 10.0))[0]
    if not len(vivos):
        return m
    return m[vivos[0] * w: (vivos[-1] + 1) * w]


def em_loop(m, n, k):
    """Repete a trilha até n amostras, cruzando cada volta em k amostras com potência constante,
    para a emenda não estalar nem afundar."""
    if len(m) >= n:
        return m[:n].copy()
    entra, sai = np.sin(np.linspace(0, np.pi / 2, k))[:, None], np.cos(np.linspace(0, np.pi / 2, k))[:, None]
    partes, cauda = [m[:-k]], m[-k:]
    total = len(m) - k
    while total < n:
        partes.append(cauda * sai + m[:k] * entra)
        partes.append(m[k:-k])
        cauda = m[-k:]
        total += len(m) - k
    return np.concatenate(partes)[:n]


def preparar_trilha(t, n, voz_lufs, tmp):
    """A trilha na linha do tempo do reel: em loop ou aparada, no volume pedido contra a voz, com os fades.

    O volume é medido no trecho que toca de fato (do "entra" ao fim), antes dos fades, porque é
    esse trecho que fica embaixo da voz. Antes do "entra", silêncio.
    """
    a = int(round(t["entra"] * SR))
    ativo = n - a
    bruta = ler_audio(t["caminho"], "ler a trilha", segundos=ativo / SR + 1.0, desde=t["inicio_no_arquivo"])
    t["repetiu"] = len(bruta) < ativo
    if t["repetiu"]:
        bruta = aparar_pontas(bruta)
        if len(bruta) < int(TRILHA_MINIMA * SR):
            raise Falha("a trilha %s tem menos de %.0f s de música para dar a volta" % (curto(t["caminho"]), TRILHA_MINIMA), 2)
        t["volta"] = len(bruta) / SR
        corpo = em_loop(bruta, ativo, int(EMENDA_TRILHA * SR))
    else:
        corpo = bruta[:ativo].copy()
    gravar_wav_float(tmp / "trilha-crua.wav", corpo)
    lufs = medir_volume(tmp / "trilha-crua.wav")["lufs"]
    if lufs is None or lufs < -70.0:
        raise Falha("a trilha %s está muda ou quase (%s LUFS)" % (curto(t["caminho"]), numero(lufs, "LUFS")), 2)
    t["lufs_arquivo"] = lufs
    corpo *= 10.0 ** ((voz_lufs + t["volume_db"] - lufs) / 20.0)
    # um fade não passa da metade do trecho que toca; o que vale de fato vai para o t, que o
    # ducking, a medida e o relatório usam
    entrada = min(int(round(t["fade_entrada"] * SR)), ativo // 2)
    saida = min(int(round(t["fade_saida"] * SR)), ativo // 2)
    t["fade_entrada_real"], t["fade_saida_real"] = entrada / SR, saida / SR
    if entrada > 0:
        corpo[:entrada] *= rampa(entrada)
    if saida > 0:
        corpo[ativo - saida:] *= rampa(saida, sobe=False)
    cama = np.zeros((n, 2))
    cama[a:] = corpo
    return cama


def corridas(marcas):
    """Os trechos seguidos de True de um vetor de booleanos, como pares (começo, fim) de índices."""
    d = np.diff(np.concatenate([[0], marcas.astype(np.int8), [0]]))
    return list(zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]))


def onde_a_voz_soa(voz, voz_lufs):
    """Em quadros de 10 ms, onde a voz está soando: a energia com ponderação K a menos de
    LIMIAR_DUCKING dB do LUFS da voz. Buraco curto dentro da fala vira fala, e som isolado
    curto demais (estalo de boca, clique) deixa de ser."""
    w = int(QUADRO_VOZ * SR)
    q = len(voz) // w
    y = ponderar_k(voz[: q * w])
    energia = np.sum(np.mean(y.reshape(q, w, 2) ** 2, axis=1), axis=1)
    soa = -0.691 + 10.0 * np.log10(energia + 1e-20) > voz_lufs - LIMIAR_DUCKING
    for a, b in corridas(~soa):
        if 0 < a and b < q and b - a < EMENDA_VOZ / QUADRO_VOZ:
            soa[a:b] = True
    for a, b in corridas(soa):
        if b - a < SOM_MINIMO / QUADRO_VOZ:
            soa[a:b] = False
    return soa


def curva_do_ducking(soa, n, profundidade, t):
    """O ganho da trilha, em dB e por amostra: -profundidade com a voz falando e nas pausas
    curtas, 0 nas pausas longas, e curvas de cosseno nas passagens.

    Cada pausa é decidida inteira, porque o script tem a fala toda antes de misturar. Ela só
    solta a trilha se couber a espera, a subida, um tempo lá em cima e a descida (1,2 s); a
    descida termina quando a voz volta, então a trilha já está embaixo na primeira sílaba. Antes
    da primeira palavra, quem sobe a trilha é o fade de entrada; depois da última, quem desce é
    o de saída. Devolve a curva e as pausas que soltaram, em segundos (None = a ponta do reel).
    """
    falas = [(float(a * QUADRO_VOZ), float(b * QUADRO_VOZ)) for a, b in corridas(soa)]
    cama_cheia = t["entra"] + t["fade_entrada_real"]          # onde o fade de entrada termina
    cama_some = n / SR - t["fade_saida_real"]                  # onde o de saída começa
    pausas = []
    fim_anterior = None
    for comeco, fim in falas:
        pausas.append((fim_anterior, comeco))
        fim_anterior = fim
    pausas.append((fim_anterior, None))

    g = np.full(n, -profundidade)
    soltas = []

    def amostra(s):
        return min(n, max(0, int(round(s * SR))))

    def cosseno(i0, i1, sobe):
        if i1 > i0:
            r = 0.5 - 0.5 * np.cos(np.pi * np.arange(i1 - i0) / (i1 - i0))
            g[i0:i1] = -profundidade * (1.0 - (r if sobe else r[::-1]))

    for de, ate in pausas:
        topo_de = cama_cheia if de is None else de + SEGURA_DUCKING + SOBE_DUCKING
        topo_ate = cama_some if ate is None else ate - DESCE_DUCKING
        if topo_ate - topo_de < TOPO_MINIMO:
            continue                                            # pausa curta: a trilha fica embaixo
        soltas.append((de, ate))
        if de is not None:
            cosseno(amostra(de + SEGURA_DUCKING), amostra(topo_de), sobe=True)
        g[amostra(0.0 if de is None else topo_de): amostra(n / SR if ate is None else topo_ate)] = 0.0
        if ate is not None:
            cosseno(amostra(topo_ate), amostra(ate), sobe=False)
    return g, soltas


def abaixar_sob_a_voz(cama, voz, voz_lufs, t):
    """O ducking: a trilha perde t["ducking_db"] enquanto a voz fala, com a voz como chave.

    Nada de compressor nem portão: os dois só sabem que a pausa é longa depois que ela já
    durou, então ou soltam antes da hora ou nunca soltam. Com o portão do ffmpeg segurando
    0,35 s, um silêncio de 0,38 s subia a trilha 4 dB em 100 ms e ela despencava 6 dB em
    menos de 50 ms quando a voz voltava: bombeava justo nas pausas de 0,4 a 0,6 s que uma
    fala menos aparada tem. Aqui a decisão é por pausa (curva_do_ducking): pausa de menos de
    1,2 s não mexe na trilha, e a mais longa sobe devagar e desce antes de a voz voltar.
    """
    g, soltas = curva_do_ducking(onde_a_voz_soa(voz, voz_lufs), len(cama), t["ducking_db"], t)
    return cama * (10.0 ** (g / 20.0))[:, None], g, soltas


def medir_trilha(voz, cama, abaixada, voz_lufs, t, g):
    """Quanto a trilha ficou abaixo da voz em quadros de 100 ms: com a voz falando, nas pausas
    curtas (em que o ducking segura) e no alto das pausas longas (em que ele solta).

    Tudo com a ponderação K do LUFS e contra o volume médio da voz, a mesma régua do volume_db.
    Os fades ficam de fora: ali a trilha está entrando ou saindo, e não no nível dela.
    """
    w = int(0.1 * SR)
    de = int(round((t["entra"] + t["fade_entrada_real"]) * SR))
    ate = len(voz) - int(round(t["fade_saida_real"] * SR))
    q = (ate - de) // w
    if q < 1:
        return None

    contexto = max(0, de - SR // 4)                   # para o filtro assentar antes do trecho, como no nivel_no_trecho

    def energia(x):
        y = ponderar_k(x[contexto: de + q * w])[de - contexto:]
        return np.sum(np.mean(y.reshape(q, w, 2) ** 2, axis=1), axis=1) + 1e-20

    e_voz, e_cama, e_trilha = energia(voz), energia(cama), energia(abaixada)
    voz_db = -0.691 + 10.0 * np.log10(e_voz)
    falando = voz_db > voz_lufs - 10.0
    pausa = voz_db < voz_lufs - 30.0
    topo = np.zeros(q, bool)
    if g is not None:
        quadros_g = g[de: de + q * w].reshape(q, w)
        pausa &= quadros_g.max(axis=1) <= -t["ducking_db"] + 0.01   # a pausa em que o ducking segurou
        topo = quadros_g.min(axis=1) >= -0.01                        # o alto de uma pausa que soltou

    def nivel(e, quadros):
        return para_lufs(np.mean(e[quadros])) if np.any(quadros) else None

    r = {"quadros_fala": int(falando.sum()), "quadros_pausa": int(pausa.sum()), "quadros_topo": int(topo.sum()),
         "sem_ducking": nivel(e_cama, np.ones(q, bool)), "fala": nivel(e_trilha, falando),
         "pausa": nivel(e_trilha, pausa), "topo": nivel(e_trilha, topo), "voz_falando": nivel(e_voz, falando)}
    for chave in ("sem_ducking", "fala", "pausa", "topo"):
        if r[chave] is not None:
            r[chave] -= voz_lufs                      # dB em relação ao volume médio da voz
    if r["fala"] is not None:
        r["relacao"] = r["voz_falando"] - (r["fala"] + voz_lufs)
        r["abaixou"] = nivel(e_cama, falando) - voz_lufs - r["fala"]
    return r


# ---------------------------------------------------------------------------
# Volume final e entrega
# ---------------------------------------------------------------------------

def ler_json_do_loudnorm(texto):
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", texto)
    if not m:
        raise Falha("o loudnorm não devolveu as medidas")
    return json.loads(m.group(0))


def normalizar(origem, destino, lufs, teto=TETO_DBTP):
    base = "loudnorm=I=%.1f:TP=%.1f:LRA=%.1f" % (lufs, teto, LRA_ALVO)
    p1 = ffmpeg(["-i", str(origem), "-af", base + ":print_format=json", "-f", "null", "-"],
                "medir a mistura (primeira passada do loudnorm)")
    medido = ler_json_do_loudnorm(p1.stderr.decode("utf-8", "replace"))
    filtro = (base + ":measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s"
              ":linear=true:print_format=json"
              % (medido["input_i"], medido["input_tp"], medido["input_lra"],
                 medido["input_thresh"], medido["target_offset"]))
    p2 = ffmpeg(["-y", "-i", str(origem), "-af", filtro + ",aresample=%d" % SR,
                 "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(destino)],
                "aplicar o volume final (segunda passada do loudnorm)")
    aplicado = ler_json_do_loudnorm(p2.stderr.decode("utf-8", "replace"))
    return aplicado.get("normalization_type", "?")


def juntar(video, audio, destino, pasta_trabalho):
    """Põe o som no reel: vídeo copiado, AAC 192k, faststart. O arquivo nasce fora da pasta de entrega."""
    temporario = pasta_trabalho / (".juntando-%s" % destino.name)
    try:
        ffmpeg(["-y", "-v", "error", "-i", str(video), "-i", str(audio),
                "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2",
                "-movflags", "+faststart", "-shortest", "-f", "mp4", str(temporario)],
               "juntar o som ao video.mp4")
        destino.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.replace(temporario, destino)
        except OSError:
            shutil.move(str(temporario), str(destino))
    finally:
        if temporario.exists():
            temporario.unlink()


def conferir_entrega(destino):
    dados = sondar(destino)
    problemas = []
    v, a = fluxo(dados, "video"), fluxo(dados, "audio")
    if not v:
        problemas.append("não tem vídeo dentro")
    if not a:
        problemas.append("não tem áudio dentro")
    elif (a.get("codec_name"), a.get("sample_rate"), a.get("channels")) != ("aac", str(SR), 2):
        problemas.append("o áudio saiu %s %s Hz %s canais" % (a.get("codec_name"), a.get("sample_rate"), a.get("channels")))
    with open(destino, "rb") as arquivo:
        cabeca = arquivo.read(65536)
    if b"moov" not in cabeca or (b"mdat" in cabeca and cabeca.index(b"mdat") < cabeca.index(b"moov")):
        problemas.append("o índice moov não está no começo, então o faststart falhou")
    return dados, problemas


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------

def numero(v, unidade):
    return "?" if v is None else ("-inf" if v == float("-inf") else "%.1f" % v) + " " + unidade


def linha_volume(rotulo, m):
    return "  %-22s %s   pico %s   LRA %s" % (rotulo, numero(m["lufs"], "LUFS"), numero(m["pico"], "dBTP"),
                                             numero(m["lra"], "LU"))


def descrever_pausa(de, ate):
    if de is None and ate is None:
        return "o reel inteiro (a voz não soa)"
    if de is None:
        return "antes da 1ª palavra (até %.2f s)" % ate
    if ate is None:
        return "depois da última (de %.2f s ao fim)" % de
    return "%.2f a %.2f s" % (de, ate)


def imprimir_trilha(t, m, soltas):
    nome = t["caminho"].name
    detalhes = []
    if t["repetiu"]:
        detalhes.append("em loop, uma volta a cada %.1f s" % t["volta"])
    if t["entra"] > 0:
        detalhes.append("entra em %.2f s" % t["entra"])
    if t["inicio_no_arquivo"] > 0:
        detalhes.append("a partir de %.2f s do arquivo" % t["inicio_no_arquivo"])
    fades = "fades de %.1f s e %.1f s" % (t["fade_entrada_real"], t["fade_saida_real"])
    if (abs(t["fade_entrada_real"] - t["fade_entrada"]) > 0.005 or abs(t["fade_saida_real"] - t["fade_saida"]) > 0.005):
        fades += " (pedidos %.1f e %.1f; um fade não passa da metade do trecho que toca)" % (
            t["fade_entrada"], t["fade_saida"])
    detalhes.append(fades)
    print("  %-22s %s (%s): %s" % ("trilha", nome, t["origem"], ", ".join(detalhes)))
    ducking = t["ducking_db"] > 0
    print("      %-19s %.0f dB abaixo da voz%s" % (
        "pedido", -t["volume_db"],
        "; com a voz falando, mais %.0f dB (ducking)" % t["ducking_db"] if ducking else "; sem ducking"))
    if m is None:
        print("      %-19s a trilha toca menos que os fades; não deu para medir" % "medido")
        return
    pausa = ("%+.1f dB em %d quadro(s) de 100 ms" % (m["pausa"], m["quadros_pausa"])
             if m["pausa"] is not None else "nenhum quadro de 100 ms")
    print("      %-19s sem ducking %+.1f dB  ·  voz falando %s  ·  %s %s" % (
        "trilha x voz", m["sem_ducking"], "?" if m["fala"] is None else "%+.1f dB" % m["fala"],
        "pausas curtas" if ducking else "pausas", pausa))
    if ducking and not soltas:
        print("      %-19s nenhuma de %.1f s ou mais: a trilha fica abaixada do primeiro ao último som da voz"
              % ("pausas longas", PAUSA_QUE_SOLTA))
    elif ducking:
        alto = ("; no alto, %+.1f dB" % m["topo"]) if m["topo"] is not None else ""
        print("      %-19s a trilha subiu em %d: %s%s" % (
            "pausas longas", len(soltas), ", ".join(descrever_pausa(de, ate) for de, ate in soltas), alto))
    if m["fala"] is None:
        return
    print("      %-19s %+.1f dB com a voz falando (%s)" % (
        "voz sobre a trilha", m["relacao"], "o ducking tirou %.1f dB" % m["abaixou"] if ducking else "sem ducking"))
    if m["relacao"] < FOLGA_TRILHA_MINIMA:
        aviso("com a voz falando, a trilha fica só %.0f dB abaixo dela, e começa a disputar a fala. "
              "Baixe o \"volume_db\" da trilha ou ligue o \"ducking\"." % m["relacao"])


def linha_final(m, lufs, teto, modo):
    return (linha_volume("audio-final.wav", m) + "   (alvo %.0f, teto %.1f, ganho %s)"
            % (lufs, teto, "linear" if modo == "linear" else "dinâmico"))


def volume_final(tmp, final, lufs, teto):
    """Loudnorm da mistura para o audio-final.wav. O wav nasce no temporário e troca de lugar inteiro,
    então nunca fica pela metade."""
    modo = normalizar(tmp / "mistura.wav", tmp / final.name, lufs, teto)
    os.replace(tmp / final.name, final)
    return modo, medir_volume(final)


def fora_do_alvo(medida, lufs, teto, quem):
    problemas = []
    if medida["lufs"] is None or abs(medida["lufs"] - lufs) > TOLERANCIA_LUFS:
        problemas.append("%s ficou em %s, e o alvo é %.0f LUFS" % (quem, numero(medida["lufs"], "LUFS"), lufs))
    if medida["pico"] is None or medida["pico"] > teto:
        problemas.append("%s ficou com pico verdadeiro de %s, acima do teto de %.0f dBTP"
                         % (quem, numero(medida["pico"], "dBTP"), TETO_DBTP))
    return problemas


def processar(args):
    global np
    exigir_ferramentas()
    np = carregar_numpy()
    raiz = achar_raiz()

    projeto = resolver_projeto(raiz, args.projeto)
    if projeto is None:
        raise Falha("não achei a pasta do projeto %s" % args.projeto, 2)
    nn = nome_do_corte(args.corte)
    if nn is None:
        raise Falha("--corte é o número do corte, como 01 ou 1 (recebi %r)" % args.corte, 2)
    pasta = projeto / "materiais-de-trabalho" / ("corte-%s" % nn)
    if not pasta.is_dir():
        raise Falha("não achei a pasta do corte %s" % curto(pasta), 2)
    fala = pasta / "fala.mp4"
    if not fala.is_file():
        raise Falha("não achei o %s. Quem escreve ele é o editar_fala.py (MOTOR.md seção 1)." % curto(fala), 2)
    dados_fala = sondar(fala)
    if not fluxo(dados_fala, "audio"):
        raise Falha("o %s não tem áudio" % curto(fala), 2)
    caminho_eventos = pasta / "eventos.json"
    if not args.sem_efeitos and not caminho_eventos.is_file():
        raise Falha("não achei o %s, que diz onde vai cada efeito. Rode o compor.py antes,\n"
                    "        ou use --sem-efeitos para sair só com a voz." % curto(caminho_eventos), 2)
    # a trilha é conferida aqui, antes de qualquer mistura: caminho ou campo errado é erro de uso
    avisos_trilha = []
    trilha = ler_trilha(pasta, raiz, args, duracao_de(dados_fala) or float("inf"), avisos_trilha)
    sons = Path(args.sons) if args.sons else fabrica.pasta("componentes/sons")
    eventos, dur_eventos, ruins = [], None, 0
    if not args.sem_efeitos:
        dur_eventos, eventos, ruins = ler_eventos(caminho_eventos)
        if eventos and not sons.is_dir():
            raise Falha("não achei a pasta de sons %s. Gere com:\n"
                        "        flow-reels produzir/gerar_sons" % curto(sons), 2)
    video = pasta / "video.mp4"
    entrega = projeto / ("corte-%s" % nn) / ("corte-%s.mp4" % nn)
    final = pasta / "audio-final.wav"

    print("")
    print("  áudio do corte %s  ·  %s" % (nn, curto(pasta)))
    print("")
    for tipo, msg in avisos_trilha:
        print("  %s: %s" % (tipo, msg))

    with tempfile.TemporaryDirectory(prefix=".audio-", dir=str(pasta)) as pasta_tmp:
        tmp = Path(pasta_tmp)

        # 1. a voz, medida antes de tudo: é a régua dos efeitos e da trilha
        voz = ler_audio(fala, "ler o áudio do fala.mp4")
        n = len(voz)
        duracao = n / SR
        gravar_wav_float(tmp / "voz.wav", voz)
        med_voz = medir_volume(tmp / "voz.wav")
        if med_voz["lufs"] is None or med_voz["lufs"] < -60.0:
            raise Falha("a fala está muda ou quase (%s LUFS). Confira o fala.mp4." % med_voz["lufs"], 2)
        voz_lufs = med_voz["lufs"]
        print(linha_volume("voz (fala.mp4)", med_voz) + "   %.2f s" % duracao)

        # 2. os efeitos
        mistura = voz.copy()
        colocados, fora, pedidos = [], [], 0
        if not args.sem_efeitos:
            pedidos = len(eventos)
            if ruins:
                aviso("%d evento(s) do eventos.json sem t ou peso legível; ficaram de fora" % ruins)
            if dur_eventos is not None and abs(dur_eventos - duracao) > 0.15:
                aviso("o eventos.json diz %.2f s e a fala tem %.2f s. O compor.py rodou sobre outra fala?"
                      % (dur_eventos, duracao))
            pista, colocados, fora, destaques = montar_efeitos(voz, voz_lufs, eventos, sons, args.efeitos_db, pasta)
            mistura += pista

            print("  %-22s %d de %d pedidos entraram; no auge, %.0f dB abaixo da voz (peso 3)"
                  % ("efeitos", len(colocados), pedidos, -args.efeitos_db))
            if colocados:
                print("      %8s  %-12s %4s  %-10s %-18s %9s %8s %8s %12s  %s"
                      % ("evento", "arquivo", "peso", "tipo", "alvo", "começa", "tom", "nível", "folga da voz",
                         "tônica"))
            for c in colocados:
                folga = "%+.0f dB" % c["folga"] if c["fala"] else "pausa"
                tonica = ""
                if c.get("tonica"):
                    tonica = "\"%s\": %s" % (c["tonica"]["palavra"], {
                        "antes do ataque": "%+.0f ms, antes da palavra" % (c["desloca"] * 1000),
                        "antes da tônica": "%+.0f ms, antes da tônica" % (c["desloca"] * 1000),
                        "baixou": "%.0f dB no lugar" % c["baixa_db"]}.get(c["tonica"]["acao"], "cai na tônica"))
                print("      %6.2f s  %-12s %4d  %-10s %-18s %7.2f s %+5.1f st %5.0f dB %12s  %s"
                      % (c["t"], c["arquivo"], c["peso"], c["tipo"][:10], c["alvo"][:18],
                         c["comeca"], c["semitons"], c["nivel"], folga, tonica))
            for e, motivo in fora:
                print("      %6.2f s  %-12s fora: %s" % (e["t"], e["som"], motivo))
            if colocados:
                media = duracao / len(colocados)
                repetidos = repetidos_em_seguida(colocados)
                print("      densidade: %d efeito(s) em %.1f s, um a cada %.1f s; %d família(s), %d arquivo(s) "
                      "diferente(s); arquivo repetido em seguida: %d"
                      % (len(colocados), duracao, media, len({c["familia"] for c in colocados}),
                         len({c["arquivo"] for c in colocados}), repetidos))
                na_tonica = [c for c in colocados if c.get("tonica")]
                print("      sílaba tônica: %d palavra(s) destacada(s); %d efeito(s) cairiam na tônica de uma delas"
                      "%s" % (len(destaques), len(na_tonica), (": %d adiantado(s) até %.0f ms, %d baixado(s) %.0f dB" % (
                          sum(1 for c in na_tonica if c["desloca"] < 0), DESLOCA_MAX * 1000,
                          sum(1 for c in na_tonica if c["baixa_db"] < 0), -BAIXA_TONICA_DB)) if na_tonica else ""))
                if media < DENSIDADE_ALVO:
                    print("  olhe  mais de um efeito a cada %.1f s no reel inteiro (a régua da pesquisa): som em tudo"
                          " tira a hierarquia. Deixe sem som os eventos de peso 1 e os de enfeite." % DENSIDADE_ALVO)
            apertados = [c for c in colocados if c["fala"] and c["folga"] < FOLGA_MINIMA]
            for c in apertados:
                aviso("o %s de %.2f s fica só %.0f dB abaixo da voz. Ele pode encobrir a fala; "
                      "baixe --efeitos-db ou o peso do evento." % (c["som"], c["t"], c["folga"]))
            gravar_agenda(pasta, agenda(pasta, colocados, fora, destaques, duracao, voz_lufs, args.efeitos_db, True))
        else:
            print("  %-22s desligados (--sem-efeitos)" % "efeitos")
            gravar_agenda(pasta, agenda(pasta, [], [], [], duracao, voz_lufs, args.efeitos_db, True, sem_efeitos=True))

        # 3. a trilha, embaixo de tudo; o loudnorm do passo 4 pega a mistura inteira
        if trilha is not None:
            cama = preparar_trilha(trilha, n, voz_lufs, tmp)
            abaixada, ganho, soltas = cama, None, []
            if trilha["ducking_db"] > 0:
                abaixada, ganho, soltas = abaixar_sob_a_voz(cama, voz, voz_lufs, trilha)
            mistura += abaixada
            imprimir_trilha(trilha, medir_trilha(voz, cama, abaixada, voz_lufs, trilha, ganho), soltas)
        elif args.sem_trilha:
            print("  %-22s desligada (--sem-trilha)" % "trilha")

        # 4. o volume final
        gravar_wav_float(tmp / "mistura.wav", mistura)
        med_mistura = medir_volume(tmp / "mistura.wav")
        print(linha_volume("mistura, antes", med_mistura))
        modo, med_final = volume_final(tmp, final, args.lufs, TETO_DBTP)
        print(linha_final(med_final, args.lufs, TETO_DBTP, modo))
        problemas = fora_do_alvo(med_final, args.lufs, TETO_DBTP + TOLERANCIA_PICO, "o audio-final.wav")

        # 5. a entrega
        entregue = None
        if not args.so_audio and video.is_file() and not problemas:
            dados_video = sondar(video)
            if not fluxo(dados_video, "video"):
                raise Falha("o %s não tem vídeo dentro" % curto(video), 2)
            dv = duracao_de(dados_video)
            if dv is not None and abs(dv - duracao) > 0.1:
                aviso("o video.mp4 tem %.2f s e a fala %.2f s. O arquivo termina no mais curto." % (dv, duracao))
            juntar(video, final, entrega, pasta)
            med_entrega = medir_volume(entrega)
            if med_entrega["pico"] is not None and med_entrega["pico"] > TETO_DBTP:
                # O AAC sobe um pouco os picos entre amostras, e o que vai para a rede é a entrega:
                # refaz o volume com a folga que faltou e junta de novo, uma vez.
                teto = TETO_DBTP - (med_entrega["pico"] - TETO_DBTP) - 0.3
                print("  olhe  o AAC levou o pico da entrega a %.1f dBTP; refiz o volume final com teto de %.1f"
                      % (med_entrega["pico"], teto))
                modo, med_final = volume_final(tmp, final, args.lufs, teto)
                print(linha_final(med_final, args.lufs, teto, modo))
                problemas = fora_do_alvo(med_final, args.lufs, TETO_DBTP + TOLERANCIA_PICO, "o audio-final.wav")
                juntar(video, final, entrega, pasta)
                med_entrega = medir_volume(entrega)
            print(linha_volume("%s (AAC)" % entrega.name, med_entrega))
            dados, falhas = conferir_entrega(entrega)
            falhas += fora_do_alvo(med_entrega, args.lufs, TETO_DBTP, "o áudio da entrega")
            problemas += ["%s: %s" % (entrega.name, f) for f in falhas]
            entregue = (dados, falhas)

    print("")
    if modo != "linear":
        print("  olhe  o loudnorm usou ganho dinâmico: o pico ou a faixa de volume da mistura não")
        print("        deixaram ganho linear. Costuma soar bem em fala, mas confira se não bombeia.")
    print("  %s  audio-final.wav    %s" % ("--" if any("audio-final" in p for p in problemas) else "ok", curto(final)))
    if args.so_audio:
        print("  --  só o áudio, como pedido (--so-audio). O corte-%s.mp4 não foi mexido." % nn)
    elif not video.is_file():
        aviso("não há video.mp4 em %s, então saiu só o audio-final.wav. Rode o compor.py\n"
              "         e depois este script de novo para juntar o som ao reel." % curto(pasta))
    elif entregue is None:
        print("  --  o corte-%s.mp4 não foi gerado, porque o áudio reprovou. Um que já exista ficou como estava." % nn)
    else:
        dados, falhas = entregue
        print("  %s  %-18s %s  (vídeo copiado, AAC 192k, faststart, %.2f s)"
              % ("--" if falhas else "ok", entrega.name, curto(entrega), duracao_de(dados) or 0.0))
        # a capa (corte-NN-capa.jpg, do capa.py) mora ao lado do mp4, como o gate de entrega aceita
        capas = {entrega.stem + "-capa.jpg", entrega.stem + "-capa.png"}
        sobras = [p.name for p in entrega.parent.iterdir()
                  if p.name != entrega.name and p.name not in capas and not p.name.startswith(".")]
        if sobras:
            aviso("a pasta %s devia ter só o %s (e a capa), e tem também: %s. Mova isso para materiais-de-trabalho/."
                  % (curto(entrega.parent), entrega.name, ", ".join(sorted(sobras))))

    print("")
    if problemas:
        print("  REPROVADO:")
        for p in problemas:
            print("    " + p)
        print("")
        return 1
    print("  PASSOU")
    print("")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Mistura a fala com os efeitos do eventos.json (e a trilha, se houver), normaliza o volume e junta ao reel.")
    ap.add_argument("--projeto", required=True, help="a pasta do vídeo, como projetos/<video>")
    ap.add_argument("--corte", required=True, help="o número do corte, como 01")
    ap.add_argument("--sem-efeitos", action="store_true", help="não põe os efeitos sonoros")
    ap.add_argument("--musica", help="arquivo da trilha de fundo, no lugar do arquivo da trilha do cenas.json")
    ap.add_argument("--musica-db", type=float, default=None,
                    help="quanto a trilha fica abaixo da voz sem o ducking (padrão: o volume_db do cenas.json, "
                         "ou %.0f)" % TRILHA_PADRAO["volume_db"])
    ap.add_argument("--sem-trilha", action="store_true", help="ignora a trilha do cenas.json")
    ap.add_argument("--lufs", type=float, default=-14.0, help="volume integrado final em LUFS (padrão -14)")
    ap.add_argument("--efeitos-db", type=float, default=-20.0,
                    help="quanto os efeitos ficam abaixo da voz, no auge (padrão -20)")
    ap.add_argument("--so-audio", action="store_true", help="gera só o audio-final.wav, sem juntar ao video.mp4")
    ap.add_argument("--sons", help="pasta de sons no lugar de componentes/sons/")
    args = ap.parse_args()

    if not -30.0 <= args.lufs <= -5.0:
        erro("--lufs fora do razoável (%.1f). Para redes sociais o certo é perto de -14." % args.lufs)
        return 2
    for outra in ("musica", "musica_db"):
        if args.sem_trilha and getattr(args, outra) is not None:
            erro("--sem-trilha e --%s se anulam: escolha um dos dois." % outra.replace("_", "-"))
            return 2
    for nome in ("efeitos_db", "musica_db"):
        valor = getattr(args, nome)
        if valor is None:
            continue
        if valor > 0:
            print("  nota: --%s é quanto fica ABAIXO da voz; entendi %.0f como -%.0f"
                  % (nome.replace("_", "-"), valor, valor))
            setattr(args, nome, -valor)
        if getattr(args, nome) < -60:
            erro("--%s abaixo de -60 dB some de vez. Para tirar, use --sem-efeitos ou --sem-trilha."
                 % nome.replace("_", "-"))
            return 2

    try:
        return processar(args)
    except Falha as f:
        erro(str(f))
        return f.codigo
    except KeyboardInterrupt:
        erro("interrompido")
        return 1


if __name__ == "__main__":
    sys.exit(main())
