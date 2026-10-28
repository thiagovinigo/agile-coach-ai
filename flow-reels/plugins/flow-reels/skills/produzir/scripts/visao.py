#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visao.py  ·  a visão computacional do corte: recorte da pessoa, fundo limpo, profundidade, mãos,
corpo e objetos, quadro a quadro

A 3.0 mostra a IA enxergando a cena (docs/fabrica-3-0-plano.md, Onda 2): texto atrás da cabeça,
você numa camada e o fundo em outra, a profundidade em onda, as mãos com os 21 pontos, as caixas de
detecção. Tudo isso sai de uma análise por quadro do vídeo da fala, feita uma vez e gravada em
materiais-de-trabalho/corte-NN/visao/, que o compor.py entrega ao motor como window.VISAO
(motor/MOTOR.md, seção 2.6). Tudo gratuito e local: MediaPipe, Video Depth Anything Small e Depth
Anything V2 Small (Apache-2.0) e BiRefNet lite (MIT), rodando no próprio computador.

A grade de quadros é a mesma do compor.py: o ffmpeg lê o vídeo com -vf fps=<fps do plano>, e o
quadro i (a partir de 0) é o instante i/fps, gravado como número i+1 nos arquivos (como os
quadros-fonte/f%06d.jpg). O quadro que o motor mostra e a máscara que ele aplica são sempre o mesmo.

O caminho:

  ler          o ffmpeg entrega os quadros na fps do plano. Quadro com mais de 1920 px de altura é
               reduzido para 1920 (a máscara e o fundo saem nesse tamanho; as coordenadas de mãos,
               corpo, objetos e caixas voltam para o pixel da fonte).

  analisar     numa passada só. Em linha: o Selfie Segmenter (em quadrados sobrepostos, para não
               achatar o quadro vertical no quadrado de 256 do modelo) e o Selfie Multiclass (a
               classe 0 é o fundo; ele pega melhor o cabelo e a mão de lado), as mãos, o corpo e os
               objetos (no Metal, no Mac: na CPU os detectores do MediaPipe 1.0.1 abortam). Ao lado,
               numa thread, a profundidade no onnxruntime, que solta o GIL e corre junto: o Video
               Depth Anything Small (4.3), com o codificador quadro a quadro na CPU e a cabeça temporal
               em janelas de 32 quadros (no CoreML, no Mac), ou o Depth Anything V2 Small quadro a
               quadro (--profundidade dav2, o de antes).

  profundidade a saída do modelo é o inverso relativo da distância (maior = mais perto), sem
               escala: não é metro. O VDA já sai estável no tempo (as janelas se alinham pelos
               quadros-chave em comum, e cada trecho entre emendas se alinha ao anterior); depois, a
               mesma régua de antes: os percentis 1 e 99 do vídeo inteiro (o mesmo 0 a 255 em todos os
               quadros, então dá para comparar um quadro com outro) e a suavização no tempo só onde a
               imagem não mudou (a mão que passa não deixa rastro no mapa), sem atravessar emenda.

  recorte      a confiança da pessoa é o maior dos dois segmentadores, corrigido pela profundidade:
               o que está tão longe quanto a parede perde (o capacete na prateleira, o letreiro), o
               que está tão perto quanto o corpo entra (o braço tatuado que os dois segmentadores
               perdem). Depois, uma média no tempo que só junta quadros vizinhos onde a imagem não
               mudou (o pixel parado deixa de piscar; a mão que passa não deixa rastro), o filtro
               guiado pela imagem colorida (a borda vai para a borda de verdade), buraco pequeno tapado
               e ilha solta apagada.

  cabelo       (4.3, --cabelo) o BiRefNet lite na caixa da cabeça (do rosto.json), em quadros-chave
               (1 a cada 10 e nas pontas de cada trecho), levado aos quadros do meio pelo fluxo óptico
               e pesado pela distância no tempo e por quanto a imagem levada bate com a do quadro. Só
               vale numa faixa em volta do contorno (até 3,5% da largura para fora e 2% para dentro):
               os fios que os segmentadores perdiam entram, a parede entre os fios sai. Depois, a
               mesma borda firmada de antes.

  fundo        a mediana, pixel a pixel, dos quadros em que aquele pixel é fundo (a pessoa dilatada
               em ~12 px), numa amostra do vídeo inteiro. O que a pessoa nunca descobriu é
               inventado: a cor da parede em volta, puxada de perto para longe e lisa (a prateleira
               escura e o neon pesam pouco, para não virarem mancha), e por cima a textura da própria
               parede, em blocos trazidos de cima ou de baixo por um múltiplo do passo das fiadas
               medido nela (o rejunte continua na mesma altura). É uma continuação plausível do
               fundo, não o que estava lá.

  mãos         a mão de cada lado, do ponto de vista de quem assiste ("esquerda" = a mão que
               aparece à esquerda na tela). A leitura repetida da mesma mão vira uma; cada leitura
               segue a trilha de uma mão física (a que sumiu há mais tempo perde para a vista agora);
               o lado é da trilha inteira, decidido pela tela (à esquerda da outra mão, ou do meio do
               corpo quando está sozinha): a mão que cruza o meio continua sendo a mesma. Suavizada
               com o filtro One Euro, numa passada para a frente e outra para trás (a média das duas
               não atrasa).

  confiança    toda mão, corpo e objeto leva "medido": true no quadro em que o modelo rodou e achou,
               e false no quadro preenchido (falha curta das mãos e do corpo, os quadros entre duas
               análises dos objetos). O "score" é sempre um número que o modelo deu: no quadro
               preenchido, o da análise mais perto. Peça que mostra confiança na tela usa o medido.

O que sai em visao/ (o contrato inteiro está no MOTOR.md, seção 2.6):

  mascara/m%06d.png     8 bits, cinza, a pessoa em branco, do tamanho do quadro (altura até 1920)
  fundo-limpo.jpg       o cenário sem a pessoa, do mesmo tamanho
  fundo-buraco.png      branco = a parte do fundo-limpo que foi inventada
  profundidade/p%06d.png  8 bits, 255 = mais perto, na resolução do modelo (210 x 364 no 9:16)
  maos.json, corpo.json, objetos.json
  visao.json            modelos e licenças, tempos, % de quadros com pessoa, a caixa da pessoa por
                        quadro e as medianas de profundidade da pessoa e do fundo
  folha-visao.png       a folha de contato: OLHE antes de usar

Uso:

    flow-reels produzir/visao --projeto projetos/<video> --corte 01
    flow-reels produzir/visao --projeto projetos/<video> --corte 01 --so maos,corpo
    flow-reels produzir/visao --projeto projetos/<video> --corte 01 --refazer
    flow-reels produzir/visao --projeto projetos/<video> --corte 01 --cabelo nao --profundidade dav2

--so            só as partes da lista: mascara, fundo, profundidade, maos, corpo, objetos. O fundo sai
                da máscara: refazer a máscara refaz o fundo junto.
--refazer       refaz mesmo o que já está gravado e vale para este vídeo.
--profundidade  vda (padrão: Video Depth Anything Small, estável no tempo) ou dav2 (o Depth Anything
                V2 Small quadro a quadro, de antes).
--cabelo        auto (padrão: liga quando o tempo estimado do cabelo cabe em 3 min), sim ou nao.

Sem --refazer, cada parte gravada para este mesmo vídeo (caminho, tamanho e data, mesma fps e mesma
versão deste script, em visao/.origem.json) é reaproveitada.

Saída 0 = gravou. Saída 1 = gravou, mas a pessoa apareceu em menos da metade dos quadros (olhe a
folha). Saída 2 = erro de uso ou de ambiente.
"""

import argparse
import json
import math
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
from contextlib import contextmanager
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


VERSAO = 2                 # a versão do script (vai no visao.json e no .origem.json)
# a versão de cada parte: sobe quando o algoritmo daquela parte muda, e só ela é refeita (a 2 do fundo
# trocou o TELEA pela cor de parede puxada de perto; a 2 das mãos, do corpo e dos objetos marca o quadro
# medido e nunca inventa confiança; a 3 das mãos segue a mão física, junta a leitura repetida e decide o
# lado pela tela; a 2 da profundidade só alisa no tempo onde a imagem não mudou, e a 2 da máscara vem
# junto porque ela usa a profundidade; a 3 do fundo continua a parede com a textura dela)
# A 3 da profundidade é o Video Depth Anything (4.3); a 3 da máscara vem com ela e com o cabelo.
VERSOES = {"mascara": 3, "fundo": 4, "profundidade": 3, "maos": 3, "corpo": 2, "objetos": 2}
PARTES = ["mascara", "fundo", "profundidade", "maos", "corpo", "objetos"]
ALTURA_MAX = 1920          # quadro mais alto que isso é reduzido para a análise
LADO_BRUTO = 512           # lado maior da confiança bruta dos segmentadores (o modelo vê 256 por quadrado)
AREA_PROFUNDIDADE = 76440  # pixels de entrada do Depth Anything (364 x 210 num quadro 9:16)
LIMIAR_OBJETO = 0.5        # abaixo disso o EfficientDet acha rosquinha em mão fechada
PASSO_OBJETOS = 3          # o detector de objetos roda 1 quadro a cada 3; o resto é interpolado
BURACO_MAOS = 3            # falha de até 3 quadros na mão ou no corpo é interpolada
RENOVAR_DETECTORES = 100   # quadros: no Metal, cada detector do MediaPipe retém ~2 a 5 MB por quadro até ser
                           # fechado (medido: 3,2 GB em 600 quadros só nas mãos, e a conta cresce com a
                           # duração do vídeo); fechar e abrir de novo a cada 100 quadros (e em cada emenda)
                           # segura os três em ~0,8 GB e custa ~0,8 s por vez
DILATA_FUNDO = 12          # px (num quadro de 576 de largura) em volta da pessoa que não entram no fundo
AMOSTRAS_FUNDO = 150       # quadros, no máximo, na mediana do fundo
PIXELS_FUNDO = 90_000_000  # e no máximo isto de pixels guardados para ela (~150 quadros de 576x1024, ~43 de
                           # 1080x1920): a memória do fundo não cresce com a resolução
MIN_FUNDO = 3              # um pixel do fundo precisa ter sido visto em pelo menos 3 amostras
GUIA_RAIO = 6              # raio do filtro guiado, num quadro de 576 de largura
GUIA_EPS = 1e-3            # quanto o filtro guiado alisa (menor = segue mais a borda da imagem)
SIGMA_TEMPO = 10.0         # diferença de luma (0 a 255) em que o vizinho no tempo pesa 60%
SIGMA_PROF = 12.0          # e a diferença de profundidade (0 a 255) em que ele pesa 60% no mapa de profundidade
POUCO = 0.50               # pessoa em menos que isso dos quadros: saída 1
# Video Depth Anything (o infer_video_depth do repositório oficial, "do not change"): janelas de 32
# quadros; as 10 primeiras de cada janela são quadros-chave da anterior (o primeiro do trecho, o 12.º e
# os 8 últimos), e os 8 que as duas janelas veem juntos são misturados em rampa
VDA_JANELA = 32
VDA_SOBRA = 10
VDA_CHAVES = [0, 12, 24, 25, 26, 27, 28, 29, 30, 31]
VDA_MISTURA = 8
VDA_PASSO = VDA_JANELA - VDA_SOBRA
# O cabelo (BiRefNet na caixa da cabeça, em quadros-chave)
CABELO_PASSO = 10          # um quadro-chave a cada 10 quadros, e nas pontas de cada trecho
CABELO_FLUXO = 256         # lado maior da caixa da cabeça no cálculo do fluxo óptico
CABELO_FORA = 0.035        # até onde, além da máscara, o BiRefNet pode pôr cabelo (fração da largura)
CABELO_DENTRO = 0.02       # e até onde, para dentro dela, ele pode tirar (fração da largura)
CABELO_ERRO = 14.0         # diferença de luma (0 a 255) da imagem levada em que o quadro-chave pesa 37%
CABELO_SEGUNDOS = 0.6      # custo de um quadro-chave do BiRefNet (medido num M4, na CPU: 0,5 a 0,7 s)
CABELO_QUADRO = (0.010, 0.020)  # e o de levar o cabelo a cada quadro: 10 ms + 20 ms por quadro de 1080 x 1920
                           # (medido: 15 ms em 576 x 1024, 29 ms em 1080 x 1920)
CABELO_TETO = 180.0        # --cabelo auto liga quando o estimado cabe nisto (s): um reel de até ~1 min
INSTANTES = 6              # instantes na folha

MODELOS = {
    "selfie": ("selfie_segmenter.tflite", "MediaPipe Selfie Segmenter", "Apache-2.0"),
    "multiclasse": ("selfie_multiclass_256x256.tflite", "MediaPipe Selfie Multiclass 256x256", "Apache-2.0"),
    "profundidade": ("depth-anything-v2-small.onnx", "Depth Anything V2 Small (ONNX)", "Apache-2.0"),
    # 4.3: exportados do original (componentes/modelos/exportar-modelos-4-3.py); só o Small do VDA é Apache
    "vda_codificador": ("vda-small-codificador.onnx", "Video Depth Anything Small, codificador (ONNX)", "Apache-2.0"),
    "vda_cabeca": ("vda-small-cabeca.onnx", "Video Depth Anything Small, cabeça temporal (ONNX)", "Apache-2.0"),
    "cabelo": ("birefnet-lite-640.onnx", "BiRefNet lite, 640 px (ONNX)", "MIT"),
    "maos": ("hand_landmarker.task", "MediaPipe Hand Landmarker", "Apache-2.0"),
    "corpo": ("pose_landmarker_lite.task", "MediaPipe Pose Landmarker Lite", "Apache-2.0"),
    "objetos": ("efficientdet_lite0.tflite", "EfficientDet-Lite0 (COCO), MediaPipe Object Detector", "Apache-2.0"),
}

# os nomes das categorias do COCO em português, para o que vai para a tela
CATEGORIAS = {
    "person": "pessoa", "bicycle": "bicicleta", "car": "carro", "motorcycle": "moto", "airplane": "avião",
    "bus": "ônibus", "train": "trem", "truck": "caminhão", "boat": "barco", "traffic light": "semáforo",
    "fire hydrant": "hidrante", "stop sign": "placa de pare", "parking meter": "parquímetro", "bench": "banco",
    "bird": "pássaro", "cat": "gato", "dog": "cachorro", "horse": "cavalo", "sheep": "ovelha", "cow": "vaca",
    "elephant": "elefante", "bear": "urso", "zebra": "zebra", "giraffe": "girafa", "backpack": "mochila",
    "umbrella": "guarda-chuva", "handbag": "bolsa", "tie": "gravata", "suitcase": "mala", "frisbee": "frisbee",
    "skis": "esqui", "snowboard": "snowboard", "sports ball": "bola", "kite": "pipa", "baseball bat": "taco",
    "baseball glove": "luva", "skateboard": "skate", "surfboard": "prancha", "tennis racket": "raquete",
    "bottle": "garrafa", "wine glass": "taça", "cup": "copo", "fork": "garfo", "knife": "faca", "spoon": "colher",
    "bowl": "tigela", "banana": "banana", "apple": "maçã", "sandwich": "sanduíche", "orange": "laranja",
    "broccoli": "brócolis", "carrot": "cenoura", "hot dog": "cachorro-quente", "pizza": "pizza",
    "donut": "rosquinha", "cake": "bolo", "chair": "cadeira", "couch": "sofá", "potted plant": "planta",
    "bed": "cama", "dining table": "mesa", "toilet": "vaso sanitário", "tv": "tv", "laptop": "laptop",
    "mouse": "mouse", "remote": "controle remoto", "keyboard": "teclado", "cell phone": "celular",
    "microwave": "micro-ondas", "oven": "forno", "toaster": "torradeira", "sink": "pia",
    "refrigerator": "geladeira", "book": "livro", "clock": "relógio", "vase": "vaso", "scissors": "tesoura",
    "teddy bear": "ursinho", "hair drier": "secador", "toothbrush": "escova de dentes",
}

# os ossos da mão (21 pontos) e do corpo (33 pontos), só para a folha de contato
OSSOS_MAO = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9), (9, 10), (10, 11),
             (11, 12), (9, 13), (13, 14), (14, 15), (15, 16), (13, 17), (17, 18), (18, 19), (19, 20), (0, 17)]
OSSOS_CORPO = [(11, 12), (11, 13), (13, 15), (12, 14), (14, 16), (11, 23), (12, 24), (23, 24),
               (0, 2), (0, 5), (2, 7), (5, 8), (9, 10)]

FONTES_DO_SISTEMA = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
)
FUNDO_FOLHA = (16, 16, 20)
BRANCO = (235, 235, 240)
CIANO = (0, 153, 255)      # as cores da marca, só na folha de contato
ROSA = (255, 0, 94)
AMBAR = (247, 167, 17)
VERDE = (61, 220, 132)

# O teste de cada tarefa do MediaPipe roda num processo separado: se o C++ abortar, quem morre é o
# teste, e o script segue sem aquela parte (ou para, se for o recorte).
SONDA = r"""
import sys
import types
sys.modules.setdefault("sounddevice", types.ModuleType("sounddevice"))
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
tarefa, modelo, caminho = sys.argv[1], sys.argv[2], sys.argv[3]
deleg = BaseOptions.Delegate.GPU if caminho == "metal" else BaseOptions.Delegate.CPU
base = BaseOptions(model_asset_path=modelo, delegate=deleg)
if tarefa == "segmentador":
    t = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=base, output_confidence_masks=True))
    t.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.zeros((96, 96, 3), np.uint8)))
else:
    V = vision.RunningMode.VIDEO
    if tarefa == "maos":
        t = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
            base_options=base, num_hands=2, running_mode=V))
    elif tarefa == "corpo":
        t = vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(
            base_options=base, running_mode=V))
    else:
        t = vision.ObjectDetector.create_from_options(vision.ObjectDetectorOptions(
            base_options=base, running_mode=V, score_threshold=0.5))
    t.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGBA, data=np.zeros((96, 96, 4), np.uint8)), 0)
t.close()
print("ok")
"""


def sem_audio():
    """O import do MediaPipe carrega o sounddevice (para as tarefas de áudio, que o visao.py não usa), e
    o sounddevice abre o CoreAudio no import: com o coreaudiod ocupado, cada import esperava ~60 s
    (medido: 61,7 s contra 1,2 s), e o script importa o MediaPipe em 5 processos. Um sounddevice vazio
    no lugar evita isso; o MediaPipe só chama o sounddevice ao gravar áudio."""
    import types
    sys.modules.setdefault("sounddevice", types.ModuleType("sounddevice"))


def erro(msg):
    print("  erro: " + msg, file=sys.stderr, flush=True)


def aviso(msg):
    print("  aviso: " + msg, flush=True)


def fala(msg):
    print(msg, flush=True)


# ---------------------------------------------------------------------------
# Ambiente
# ---------------------------------------------------------------------------

def achar_raiz():
    """A pasta de trabalho; os modelos vêm de componentes/modelos, da pasta ou do plugin."""
    return fabrica.raiz()


def carregar(nome, pip):
    try:
        return __import__(nome)
    except ImportError:
        erro("falta o %s neste Python.\n"
             "       Rode com o Python do pacote: .venv/bin/python, ou instale com: pip install %s" % (nome, pip))
        sys.exit(2)


@contextmanager
def calar_stderr():
    """O MediaPipe escreve log de C++ direto no descritor 2; aqui ele vai para o lixo."""
    try:
        sys.stderr.flush()
        salvo = os.dup(2)
        nulo = os.open(os.devnull, os.O_WRONLY)
        os.dup2(nulo, 2)
        os.close(nulo)
    except OSError:
        salvo = None
    try:
        yield
    finally:
        if salvo is not None:
            sys.stderr.flush()
            os.dup2(salvo, 2)
            os.close(salvo)


def linhas_de_falha(texto):
    uteis = [l.strip() for l in texto.splitlines()
             if any(p in l for p in ("Check failed", "Error", "error", "rror:", "Traceback"))]
    if not uteis:
        uteis = [l.strip() for l in texto.splitlines() if l.strip()][-3:]
    return "\n       ".join(uteis[-3:])


def escolher_caminho(tarefa, modelo):
    """O caminho do MediaPipe que roda nesta máquina para a tarefa, testado num processo separado.
    O segmentador roda na CPU (no Mac o caminho de CPU dele funciona e é rápido); os detectores, no
    Mac, só no Metal. Devolve (caminho, falhas)."""
    if tarefa == "segmentador":
        candidatos = ["cpu"]
    else:
        candidatos = ["metal", "cpu"] if sys.platform == "darwin" else ["cpu"]
    falhas = []
    for nome in candidatos:
        try:
            proc = subprocess.run([sys.executable, "-c", SONDA, tarefa, str(modelo), nome],
                                  capture_output=True, text=True, errors="replace", timeout=180)
        except subprocess.TimeoutExpired:
            falhas.append("%s: o teste passou de 3 minutos" % nome)
            continue
        if proc.returncode == 0 and "ok" in proc.stdout:
            return nome, falhas
        falhas.append("%s: %s" % (nome, linhas_de_falha(proc.stderr)))
    return None, falhas


# ---------------------------------------------------------------------------
# Vídeo
# ---------------------------------------------------------------------------

def sondar_video(caminho):
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-print_format", "json",
           "-show_streams", "-show_format", str(caminho)]
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        erro("o ffprobe não conseguiu ler %s:\n%s" % (caminho, proc.stderr.strip()[-600:]))
        sys.exit(2)
    dados = json.loads(proc.stdout or "{}")
    fluxos = dados.get("streams") or []
    if not fluxos:
        erro("%s não tem trilha de vídeo." % caminho)
        sys.exit(2)
    v = fluxos[0]
    largura, altura = int(v.get("width") or 0), int(v.get("height") or 0)
    rotacao = 0
    for lado in v.get("side_data_list") or []:
        if "rotation" in lado:
            rotacao = int(round(float(lado["rotation"])))
    if abs(rotacao) % 180 == 90:
        largura, altura = altura, largura
    if largura <= 0 or altura <= 0:
        erro("não consegui ler o tamanho do quadro de %s." % caminho)
        sys.exit(2)
    duracao = float((dados.get("format") or {}).get("duration") or v.get("duration") or 0)
    return largura, altura, duracao


def par(n):
    return max(2, int(round(n / 2.0)) * 2)


class Leitor:
    """Os quadros do vídeo, um por vez, na grade de quadros do compor.py (-vf fps=N), no tamanho da
    análise. Ler duas vezes o mesmo vídeo dá os mesmos quadros."""

    def __init__(self, video, fps, tamanho, fonte):
        self.w, self.h = tamanho
        filtros = ["fps=%s" % fps]
        if (self.w, self.h) != tuple(fonte):
            filtros.append("scale=%d:%d:flags=area" % (self.w, self.h))
        cmd = ["ffmpeg", "-v", "error", "-nostdin", "-i", str(video), "-map", "0:v:0",
               "-vf", ",".join(filtros), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.n = self.w * self.h * 3

    def __iter__(self):
        import numpy as np
        try:
            while True:
                bruto = self.proc.stdout.read(self.n)
                if len(bruto) < self.n:
                    break
                yield np.frombuffer(bruto, np.uint8).reshape(self.h, self.w, 3)
        finally:
            if self.proc.poll() is None:
                self.proc.kill()
            self.proc.stdout.close()
            self.proc.wait()


def ler_segmentos(pasta, total, fps, duracao):
    """Os trechos entre as emendas do edicao.json, em índices de quadro [a, b). Nada de suavização
    atravessa uma emenda: ali a imagem pula, e a máscara, a mão e a profundidade pulam junto."""
    emendas = []
    caminho = pasta / "edicao.json"
    if caminho.is_file():
        try:
            dados = json.loads(caminho.read_text(encoding="utf-8"))
            dur = dados.get("duracao")
            if isinstance(dur, (int, float)) and duracao and abs(float(dur) - duracao) > 0.25:
                aviso("o edicao.json diz %.2f s e o vídeo tem %.2f s; ignorei as emendas dele." % (dur, duracao))
            else:
                emendas = sorted({int(round(float(t) * fps)) for t in dados.get("emendas") or []
                                  if isinstance(t, (int, float))})
        except (ValueError, OSError):
            aviso("não consegui ler o edicao.json; segui sem as emendas.")
    limites = [0] + [k for k in emendas if 0 < k < total] + [total]
    return [(a, b) for a, b in zip(limites[:-1], limites[1:]) if b > a]


def segmento_de(segmentos, total):
    import numpy as np
    s = np.zeros(total, np.int32)
    for n, (a, b) in enumerate(segmentos):
        s[a:b] = n
    return s


# ---------------------------------------------------------------------------
# Utilidades numéricas
# ---------------------------------------------------------------------------

def suave(x, a, b, np):
    """smoothstep de a até b: 0 antes, 1 depois, curva suave no meio."""
    t = np.clip((x - a) / float(b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


class UmEuro:
    """O filtro One Euro (Casiez, Roussel e Vogel, 2012): alisa forte quando o ponto está parado e
    quase nada quando ele anda depressa, que é o que a mão pede (parada não treme, gesto não atrasa)."""

    def __init__(self, freq, corte_min, beta, corte_d=1.0):
        self.freq, self.corte_min, self.beta, self.corte_d = freq, corte_min, beta, corte_d

    def _alfa(self, corte, np):
        tau = 1.0 / (2.0 * math.pi * corte)
        return 1.0 / (1.0 + tau * self.freq)

    def _passada(self, x, np):
        out = np.empty_like(x)
        out[0] = x[0]
        anterior, d_anterior = x[0], np.zeros_like(x[0])
        a_d = self._alfa(self.corte_d, np)
        for i in range(1, len(x)):
            d = (x[i] - anterior) * self.freq
            d_hat = a_d * d + (1 - a_d) * d_anterior
            a = self._alfa(self.corte_min + self.beta * np.abs(d_hat), np)
            anterior = a * x[i] + (1 - a) * anterior
            d_anterior = d_hat
            out[i] = anterior
        return out

    def filtrar(self, x, np):
        """Uma passada para a frente e outra para trás, sobre o dado bruto, e a média das duas: o
        atraso de uma cancela o adiantamento da outra."""
        x = np.asarray(x, dtype=np.float64)
        if len(x) < 3:
            return x.copy()
        ida = self._passada(x, np)
        volta = self._passada(x[::-1], np)[::-1]
        return (ida + volta) / 2.0


def corridas(presente):
    """[(a, b)) de cada trecho seguido em que presente é verdadeiro."""
    out, a = [], None
    for i, p in enumerate(list(presente) + [False]):
        if p and a is None:
            a = i
        elif not p and a is not None:
            out.append((a, i))
            a = None
    return out


# ---------------------------------------------------------------------------
# Fase 1: a passada de análise
# ---------------------------------------------------------------------------

def escala_e_desvio(pred, alvo, np):
    """a e b que levam pred para perto de alvo (a * pred + b), por mínimos quadrados."""
    p, t = pred.astype(np.float64).ravel(), alvo.astype(np.float64).ravel()
    a00, a01, a11 = float((p * p).sum()), float(p.sum()), float(p.size)
    b0, b1 = float((p * t).sum()), float(t.sum())
    det = a00 * a11 - a01 * a01
    if det == 0:
        return 1.0, 0.0
    return (a11 * b0 - a01 * b1) / det, (-a01 * b0 + a00 * b1) / det


class JanelasVDA:
    """O Video Depth Anything em fluxo, como o infer_video_depth do repositório oficial: a cabeça
    temporal roda numa janela de 32 quadros a cada 22; as 10 primeiras entradas de cada janela são
    quadros-chave da anterior (o primeiro do trecho, o 12.º e os 8 últimos), e a saída da janela nova
    é posta na escala da anterior por mínimos quadrados nos dois quadros-chave em comum; nos 8 quadros
    que as duas veem, a anterior passa para a nova em rampa. O codificador roda uma vez por quadro (o
    que ele já viu fica guardado até a última janela que usa). Um trecho por vez: fechar() completa a
    última janela com o último quadro e devolve um mapa por quadro do trecho."""

    def __init__(self, cabeca, np):
        self.cabeca, self.np = cabeca, np
        self.novo_trecho()

    def novo_trecho(self):
        self.feats = {}            # índice no trecho -> (c1, c2, c3, c4) do codificador
        self.n = 0
        self.k = 0                 # a próxima janela
        self.anterior = None       # as 32 entradas da janela anterior
        self.alinhada = []         # um mapa por quadro do trecho (float16 quando ninguém mais mexe nele)
        self.ref = None
        self.meio = 0              # até onde a lista já está em float16

    def adicionar(self, f):
        self.feats[self.n] = f
        self.n += 1
        while self.n >= self.k * VDA_PASSO + VDA_JANELA:
            self._janela()

    def fechar(self):
        while self.k * VDA_PASSO < self.n:
            self._janela()
        out = self.alinhada[:self.n]
        self.novo_trecho()
        return out

    def _janela(self):
        np = self.np
        s, n = self.k * VDA_PASSO, self.n
        if self.anterior is None:
            entradas = [self.feats[min(s + j, n - 1)] for j in range(VDA_JANELA)]
        else:
            entradas = [self.anterior[c] for c in VDA_CHAVES] + \
                [self.feats[min(s + j, n - 1)] for j in range(VDA_SOBRA, VDA_JANELA)]
        d = self.cabeca({nome: np.concatenate([e[c] for e in entradas])
                         for c, nome in enumerate(("c1", "c2", "c3", "c4"))})
        if self.anterior is None:
            self.alinhada = [d[j] for j in range(VDA_JANELA)]
            self.ref = [d[0], d[12]]
        else:
            a, b = escala_e_desvio(np.stack([d[0], d[1]]), np.stack(self.ref), np)
            ajusta = lambda x: np.maximum(x * a + b, 0.0).astype(np.float32)
            antes = [x.astype(np.float32) for x in self.alinhada[-VDA_MISTURA:]]
            depois = [ajusta(d[j]) for j in range(VDA_SOBRA - VDA_MISTURA, VDA_SOBRA)]
            for j in range(VDA_MISTURA):
                w = j / float(VDA_MISTURA - 1)
                antes[j] = antes[j] * (1 - w) + depois[j] * w
            self.alinhada[-VDA_MISTURA:] = antes
            self.alinhada += [ajusta(d[j]) for j in range(VDA_SOBRA, VDA_JANELA)]
            self.ref = [self.ref[0], ajusta(d[12])]
        self.anterior = entradas
        self.k += 1
        # o que a próxima janela ainda usa do codificador (e o último quadro, que completa a janela se o
        # trecho acabar ali); o que já não muda vai para float16 (~150 KB por quadro em 210 x 364)
        limite = min(self.k * VDA_PASSO + VDA_SOBRA, self.n - 1)
        for j in [j for j in self.feats if j < limite]:
            del self.feats[j]
        fim = len(self.alinhada) - VDA_MISTURA
        for j in range(self.meio, fim):
            self.alinhada[j] = self.alinhada[j].astype(np.float16)
        self.meio = max(self.meio, fim)


def alinhar_trecho(mapas, anteriores, np):
    """Do outro lado de uma emenda o VDA começa numa escala nova: o trecho é posto na escala do anterior
    pela média dos 3 primeiros quadros contra a dos 3 últimos de lá, num ajuste robusto (a segunda
    rodada fica só com os 70% de pixels que melhor batem: a pessoa que mudou de lugar no corte não puxa
    a escala)."""
    if not anteriores or not mapas:
        return mapas
    p = np.mean([m.astype(np.float32) for m in mapas[:3]], axis=0)
    t = np.mean([m.astype(np.float32) for m in anteriores], axis=0)
    a, b = escala_e_desvio(p, t, np)
    r = np.abs(a * p + b - t)
    bom = r <= np.percentile(r, 70)
    if bom.sum() > 100:
        a, b = escala_e_desvio(p[bom], t[bom], np)
    if not (a > 0 and math.isfinite(a) and math.isfinite(b)):
        return mapas
    return [np.maximum(m.astype(np.float32) * a + b, 0.0).astype(np.float16) for m in mapas]


def abrir_cabeca_vda(caminho, tw, th, ort, np):
    """A cabeça temporal do VDA no tamanho deste vídeo. No Mac, no CoreML (ML Program, com o tamanho
    fixado: na CPU são ~1,3 s por janela, no CoreML ~0,22 s), com o modelo compilado guardado em
    ~/Library/Caches/fabrica-de-cortes/coreml (a primeira vez leva ~14 s, as outras ~3 s). Se o CoreML
    não abrir ou não rodar, a CPU. Devolve (sessão, caminho)."""
    dims = {"h": th // 14, "w": tw // 14, "altura": th, "largura": tw}
    teste = {c: np.zeros((VDA_JANELA, 384, th // 14, tw // 14), np.float32) for c in ("c1", "c2", "c3", "c4")}

    def abrir(provedores):
        o = ort.SessionOptions()
        o.log_severity_level = 3
        for k, v in dims.items():
            o.add_free_dimension_override_by_name(k, v)
        s = ort.InferenceSession(str(caminho), o, providers=provedores)
        d = s.run(None, teste)[0]
        if d.shape != (VDA_JANELA, th, tw) or not np.isfinite(d).all():
            raise RuntimeError("saída inesperada %s" % (d.shape,))
        return s

    if sys.platform == "darwin" and "CoreMLExecutionProvider" in ort.get_available_providers():
        try:
            cache = Path.home() / "Library" / "Caches" / "fabrica-de-cortes" / "coreml"
            cache.mkdir(parents=True, exist_ok=True)
            return abrir([("CoreMLExecutionProvider", {"ModelFormat": "MLProgram", "MLComputeUnits": "ALL",
                                                       "ModelCacheDirectory": str(cache)}),
                          "CPUExecutionProvider"]), "coreml"
        except Exception:  # noqa: BLE001 (sem CoreML, a CPU faz a mesma conta, mais devagar)
            pass
    return abrir(["CPUExecutionProvider"]), "cpu"


class Profundidade(threading.Thread):
    """A profundidade numa thread ao lado: o onnxruntime solta o GIL, então ela corre junto com o
    MediaPipe em vez de esperar a vez. Guarda também a luma do quadro no tamanho do mapa: é ela que diz,
    na média no tempo, onde a imagem mudou (ali o vizinho não entra).

    modo "vda": o codificador do Video Depth Anything Small quadro a quadro (CPU) e a cabeça temporal a
    cada janela (abrir_cabeca_vda); cada trecho entre emendas fecha as janelas dele e se alinha ao
    anterior. modo "dav2": o Depth Anything V2 Small, quadro a quadro, como antes."""

    def __init__(self, modelos, tamanho, np, cv2, ort, modo, inicios):
        super().__init__(daemon=True)
        self.np, self.cv2, self.ort = np, cv2, ort
        self.modo, self.inicios = modo, set(inicios)
        self.modelos = modelos
        opcoes = ort.SessionOptions()
        opcoes.log_severity_level = 3
        nome = MODELOS["vda_codificador" if modo == "vda" else "profundidade"][0]
        self.sessao = ort.InferenceSession(str(modelos / nome), opcoes, providers=["CPUExecutionProvider"])
        self.entrada = self.sessao.get_inputs()[0].name
        self.tw, self.th = tamanho
        # o VDA abre a cabeça no começo da thread (~14 s na primeira vez): a fila folgada não segura a
        # passada de análise enquanto isso (256 quadros de 288 x 512, ~110 MB no máximo)
        self.fila = queue.Queue(maxsize=256 if modo == "vda" else 8)
        self.saida = {}
        self.luma = {}
        self.falha = None
        self.caminho = "cpu"
        self.segundos = 0.0
        self.media = np.array([0.485, 0.456, 0.406], np.float32)
        self.desvio = np.array([0.229, 0.224, 0.225], np.float32)
        self.pendentes, self.ultimos, self.janelas = [], None, None

    def _fechar_trecho(self):
        mapas = alinhar_trecho(self.janelas.fechar(), self.ultimos, self.np)
        for k, d in zip(self.pendentes, mapas):
            self.saida[k] = d.astype(self.np.float16)
        self.ultimos = mapas[-3:]
        self.pendentes = []

    def run(self):
        np, cv2 = self.np, self.cv2
        try:
            if self.modo == "vda":
                t = time.time()
                cabeca, self.caminho = abrir_cabeca_vda(self.modelos / MODELOS["vda_cabeca"][0], self.tw, self.th,
                                                        self.ort, np)
                self.segundos += time.time() - t
                self.janelas = JanelasVDA(lambda feed: cabeca.run(None, feed)[0], np)
            while True:
                item = self.fila.get()
                if item is None:
                    break
                i, quadro = item
                pequeno = cv2.resize(quadro, (self.tw, self.th), interpolation=cv2.INTER_AREA)
                self.luma[i] = cv2.GaussianBlur(cv2.cvtColor(pequeno, cv2.COLOR_RGB2GRAY), (3, 3), 0)
                x = pequeno.astype(np.float32) / 255.0
                x = np.ascontiguousarray(((x - self.media) / self.desvio).transpose(2, 0, 1)[None])
                t = time.time()
                if self.modo == "vda":
                    if i in self.inicios and self.pendentes:
                        self._fechar_trecho()
                    self.janelas.adicionar(self.sessao.run(None, {self.entrada: x}))
                    self.pendentes.append(i)
                else:
                    self.saida[i] = self.sessao.run(None, {self.entrada: x})[0][0].astype(np.float16)
                self.segundos += time.time() - t
            if self.modo == "vda" and self.pendentes:
                t = time.time()
                self._fechar_trecho()
                self.segundos += time.time() - t
        except Exception as e:  # noqa: BLE001 (a falha volta para a thread principal)
            self.falha = e


def tamanho_profundidade(w, h):
    """Altura e largura múltiplas de 14 (o passo do ViT), com ~76 mil pixels e o aspecto do quadro."""
    aspecto = w / float(h)
    tw = max(14, int(round(math.sqrt(AREA_PROFUNDIDADE * aspecto) / 14.0)) * 14)
    th = max(14, int(round(math.sqrt(AREA_PROFUNDIDADE / aspecto) / 14.0)) * 14)
    return tw, th


def quadrados(w, h):
    """Quadrados sobrepostos que cobrem o quadro no eixo comprido: o segmentador vê 256 x 256, e um
    quadro 9:16 inteiro chegaria achatado (meia resolução na vertical)."""
    lado = min(w, h)
    comprido = max(w, h)
    n = max(1, int(math.ceil(comprido / float(lado) - 1e-6)))
    if n == 1:
        return [(0, 0, w, h)]
    passo = (comprido - lado) / float(n - 1)
    caixas = []
    for k in range(n):
        o = int(round(k * passo))
        caixas.append((0, o, lado, lado) if h >= w else (o, 0, lado, lado))
    return caixas


def segmentar_quadrados(seg, mp, np, quadro, caixas, classe_fundo):
    """A confiança da pessoa no quadro inteiro, a partir dos quadrados, misturados nas sobreposições
    por uma rampa (perto da borda do quadrado o modelo vê menos contexto e pesa menos)."""
    h, w = quadro.shape[:2]
    acc = np.zeros((h, w), np.float32)
    soma = np.zeros((h, w), np.float32)
    for x0, y0, cw, ch in caixas:
        recorte = np.ascontiguousarray(quadro[y0:y0 + ch, x0:x0 + cw])
        r = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=recorte))
        m = np.squeeze(r.confidence_masks[0].numpy_view()).astype(np.float32)
        if classe_fundo:
            m = 1.0 - m
        if len(caixas) > 1:
            eixo = np.linspace(-1, 1, ch if h >= w else cw, dtype=np.float32)
            rampa = 1.05 - np.abs(eixo)
            peso = rampa[:, None] if h >= w else rampa[None, :]
        else:
            peso = np.ones((1, 1), np.float32)
        acc[y0:y0 + ch, x0:x0 + cw] += m * peso
        soma[y0:y0 + ch, x0:x0 + cw] += peso
    return acc / np.maximum(soma, 1e-6)


def analisar(ctx, fazer, np, cv2):
    """A passada pelo vídeo inteiro. Guarda, por quadro, o que cada parte pediu: a confiança bruta dos
    dois segmentadores e a luma (em LADO_BRUTO), a profundidade bruta, as mãos, o corpo e os objetos."""
    sem_audio()
    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.core.base_options import BaseOptions

    w, h = ctx["analise"]
    bw, bh = ctx["bruto"]
    caixas = quadrados(bw, bh)
    sw, sh = ctx["fonte_tam"]
    kx, ky = sw / float(w), sh / float(h)
    fps = ctx["fps"]
    tarefas = {}
    with calar_stderr():
        if fazer.get("segmentar"):
            base = lambda nome: BaseOptions(model_asset_path=str(ctx["modelos"] / MODELOS[nome][0]),
                                            delegate=BaseOptions.Delegate.CPU)
            tarefas["selfie"] = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
                base_options=base("selfie"), output_confidence_masks=True))
            tarefas["multi"] = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
                base_options=base("multiclasse"), output_confidence_masks=True))

    def abrir_detectores():
        """As mãos, o corpo e os objetos, no caminho que a sonda escolheu. Abertos de novo a cada
        RENOVAR_DETECTORES quadros e em cada emenda: a memória que o Metal retém só volta no close(), e
        o rastreio de um detector não deve atravessar o corte (do outro lado a imagem pulou)."""
        for nome in ("maos", "corpo", "objetos"):
            caminho = fazer.get(nome)
            if not caminho:
                continue
            if nome in tarefas:
                tarefas[nome].close()
            deleg = BaseOptions.Delegate.GPU if caminho == "metal" else BaseOptions.Delegate.CPU
            base = BaseOptions(model_asset_path=str(ctx["modelos"] / MODELOS[nome][0]), delegate=deleg)
            V = vision.RunningMode.VIDEO
            if nome == "maos":
                tarefas[nome] = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
                    base_options=base, num_hands=2, running_mode=V))
            elif nome == "corpo":
                tarefas[nome] = vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(
                    base_options=base, running_mode=V, num_poses=1))
            else:
                tarefas[nome] = vision.ObjectDetector.create_from_options(vision.ObjectDetectorOptions(
                    base_options=base, running_mode=V, score_threshold=LIMIAR_OBJETO, max_results=10))

    with calar_stderr():
        abrir_detectores()

    # os objetos rodam a cada PASSO_OBJETOS quadros e sempre na ponta de cada trecho, para a
    # interpolação nunca atravessar uma emenda
    pontas = set()
    for a, b in ctx["segmentos"]:
        pontas.update((a, b - 1))
    inicios = {a for a, _ in ctx["segmentos"] if a > 0}

    prof = None
    if fazer.get("profundidade"):
        import onnxruntime as ort
        prof = Profundidade(ctx["modelos"], ctx["prof_tam"], np, cv2, ort, ctx["prof_modo"], inicios)
        prof.start()
    renovado = 0

    r = {"selfie": [], "multi": [], "luma": [], "maos": [], "corpo": [], "objetos": []}
    relogio = time.time()
    ultimo = relogio
    total_esperado = ctx["total_esperado"]
    i = 0
    primeiro = True
    for quadro in Leitor(ctx["video"], fps, ctx["analise"], ctx["fonte_tam"]):
        pequeno = cv2.resize(quadro, (bw, bh), interpolation=cv2.INTER_AREA) if (bw, bh) != (w, h) else quadro
        if prof is not None:
            if prof.falha:
                break
            prof.fila.put((i, pequeno))
        if "selfie" in tarefas:
            r["selfie"].append((np.clip(segmentar_quadrados(tarefas["selfie"], mp, np, pequeno, caixas, False),
                                        0, 1) * 255).astype(np.uint8))
            r["multi"].append((np.clip(segmentar_quadrados(tarefas["multi"], mp, np, pequeno, [(0, 0, bw, bh)], True),
                                       0, 1) * 255).astype(np.uint8))
            r["luma"].append(cv2.GaussianBlur(cv2.cvtColor(pequeno, cv2.COLOR_RGB2GRAY), (5, 5), 0))
        if any(k in tarefas for k in ("maos", "corpo", "objetos")):
            if i in inicios or i - renovado >= RENOVAR_DETECTORES:
                with calar_stderr():
                    abrir_detectores()
                renovado = i
                primeiro = True     # o detector novo fala no primeiro quadro: silencia de novo
            imagem = mp.Image(image_format=mp.ImageFormat.SRGBA, data=cv2.cvtColor(quadro, cv2.COLOR_RGB2RGBA))
            instante = int(round(i * 1000.0 / fps))
            with (calar_stderr() if primeiro else _nada()):
                if "maos" in tarefas:
                    res = tarefas["maos"].detect_for_video(imagem, instante)
                    maos = []
                    for pts, lado in zip(res.hand_landmarks, res.handedness):
                        arr = np.array([[p.x * sw, p.y * sh, p.z * sw] for p in pts], np.float64)
                        maos.append({"score": float(lado[0].score) if lado else 0.0, "medido": True, "pontos": arr,
                                     "rotulo": lado[0].category_name if lado else ""})
                    r["maos"].append(maos)
                if "corpo" in tarefas:
                    res = tarefas["corpo"].detect_for_video(imagem, instante)
                    if res.pose_landmarks:
                        pts = res.pose_landmarks[0]
                        arr = np.array([[p.x * sw, p.y * sh, p.visibility or 0.0] for p in pts], np.float64)
                        pres = [p.presence for p in pts if p.presence is not None]
                        r["corpo"].append({"score": float(np.mean(pres)) if pres else float(np.mean(arr[:, 2])),
                                           "medido": True, "pontos": arr})
                    else:
                        r["corpo"].append(None)
                if "objetos" in tarefas:
                    if i % PASSO_OBJETOS == 0 or i in pontas:
                        res = tarefas["objetos"].detect_for_video(imagem, instante)
                        objs = []
                        for d in res.detections:
                            c = d.categories[0]
                            bb = d.bounding_box
                            objs.append({"en": c.category_name, "score": float(c.score),
                                         "caixa": np.array([bb.origin_x * kx, bb.origin_y * ky,
                                                            bb.width * kx, bb.height * ky], np.float64)})
                        r["objetos"].append(objs)
                    else:
                        r["objetos"].append(None)
            primeiro = False
        i += 1
        agora = time.time()
        if agora - ultimo > 10:
            fala("    analisados %d/%d quadros  ·  %.0f ms por quadro" % (i, total_esperado, (agora - relogio) / i * 1000))
            ultimo = agora
    if prof is not None:
        if not prof.falha:
            prof.fila.put(None)
        prof.join()
        if prof.falha:
            erro("a profundidade parou com erro: %s" % prof.falha)
            sys.exit(2)
        r["profundidade"] = [prof.saida[k] for k in range(i)]
        r["luma_prof"] = [prof.luma[k] for k in range(i)]
        r["prof_caminho"], r["prof_segundos"] = prof.caminho, prof.segundos
    with calar_stderr():
        for t in tarefas.values():
            t.close()
    r["total"] = i
    r["tempo"] = time.time() - relogio
    return r


@contextmanager
def _nada():
    yield


# ---------------------------------------------------------------------------
# Profundidade
# ---------------------------------------------------------------------------

def finalizar_profundidade(brutos, lumas, segs, np):
    """O inverso relativo da distância em 0 a 255 (255 = mais perto), com a mesma régua no vídeo
    inteiro (percentis 1 e 99 de todos os quadros) e alisado no tempo dentro de cada trecho.

    O alisamento é uma média binomial de 5 quadros (1-4-6-4-1) com o mesmo portão de movimento da
    máscara (FiltroTemporal): o peso de cada vizinho cai com a diferença de luma naquele pixel e também
    com a diferença de profundidade. Sem o portão, a mão que passou pelo peito ficava 2 quadros no mapa
    (pesava 5/16 na média): aos 11,67 s do teste o mapa tinha um anel 'perto' no peito, onde a mão já
    não estava, e a onda da peça profundidade riscava esse anel. Só a luma não basta, porque a borda
    do mapa é borrada e passa uns pixels da mão; a diferença de profundidade pega essa franja. O tremor
    do modelo num pixel parado (~2 a 5 tons) quase não perde peso, e continua alisado."""
    amostra = np.concatenate([b.astype(np.float32).ravel()[::7] for b in brutos[::3]])
    lo, hi = (float(v) for v in np.percentile(amostra, [1, 99]))
    escala = 255.0 / max(hi - lo, 1e-6)
    pesos = (1.0, 4.0, 6.0, 4.0, 1.0)
    dois_l, dois_p = 2.0 * SIGMA_TEMPO * SIGMA_TEMPO, 2.0 * SIGMA_PROF * SIGMA_PROF
    n = len(brutos)
    janela = {}

    def norm(j):
        if j not in janela:
            janela[j] = ((brutos[j].astype(np.float32) - lo) * escala, lumas[j].astype(np.float32))
        return janela[j]

    d8 = []
    for i in range(n):
        for j in [j for j in janela if j < i - 2]:
            del janela[j]
        di, li = norm(i)
        acc = di * pesos[2]
        soma = np.full(di.shape, pesos[2], np.float32)
        for k in (-2, -1, 1, 2):
            j = i + k
            if j < 0 or j >= n or segs[j] != segs[i]:
                continue
            dj, lj = norm(j)
            dl, dd = lj - li, dj - di
            p = pesos[k + 2] * np.exp(-(dl * dl) / dois_l - (dd * dd) / dois_p)
            acc = acc + dj * p
            soma += p
        d8.append(np.clip(acc / soma, 0, 255).round().astype(np.uint8))
    return d8, (round(lo, 4), round(hi, 4))


# ---------------------------------------------------------------------------
# Recorte da pessoa
# ---------------------------------------------------------------------------

def confianca_combinada(sq, mc, d8, np, cv2):
    """A confiança da pessoa num quadro, na resolução bruta. O maior dos dois segmentadores (o
    multiclasse tem um piso de ~0,15 no fundo: a rampa de 0,2 a 0,9 tira), corrigido pela
    profundidade relativa: 0 = a mediana do fundo, 1 = a mediana da pessoa. Abaixo de ~0,25 (tão longe
    quanto a parede) a confiança cai; acima de ~0,85 (tão perto quanto o corpo) ela entra mesmo se os
    segmentadores perderam (braço tatuado, mão de lado). Entre os dois, valem os segmentadores, porque
    a borda da profundidade é borrada."""
    a = sq.astype(np.float32) / 255.0
    b = np.clip((mc.astype(np.float32) / 255.0 - 0.2) / 0.7, 0, 1)
    seg = np.maximum(a, b)
    if d8 is None:
        return seg
    h, w = seg.shape
    d = cv2.resize(d8, (w, h), interpolation=cv2.INTER_LINEAR).astype(np.float32)
    certo = (a > 0.9) & (b > 0.9)
    fundo = (a < 0.05) & (b < 0.05)
    if certo.sum() < 200 or fundo.sum() < 200:
        return seg
    dp, df = float(np.median(d[certo])), float(np.median(d[fundo]))
    if dp - df < 12:            # sem separação de profundidade (pessoa colada na parede): só segmentador
        return seg
    rel = (d - df) / (dp - df)
    veto = suave(rel, 0.15, 0.35, np)
    # a borda da profundidade vaza uns pixels para fora da silhueta: a inclusão usa o mapa encolhido
    perto = suave(cv2.erode(rel, np.ones((3, 3), np.uint8)), 0.8, 0.95, np)
    return np.maximum(seg * veto, perto)


class FiltroTemporal:
    """Média de 5 quadros que só junta o vizinho onde a imagem não mudou: o peso de cada vizinho cai
    com a diferença de luma naquele pixel. O fundo parado e o corpo parado deixam de piscar; a mão
    que passa não deixa rastro, porque ali a imagem mudou e o vizinho não conta. Nunca junta quadros
    de lados diferentes de uma emenda. A confiança de cada quadro é calculada uma vez, quando o
    primeiro vizinho pede, e esquecida quando sai da janela: a memória fica em 5 quadros."""

    PESOS = (0.35, 0.7, 1.0, 0.7, 0.35)

    def __init__(self, conf_de, lumas, segs, n, np):
        self.conf_de, self.lumas, self.segs, self.n, self.np = conf_de, lumas, segs, n, np
        self.cache = {}

    def _c(self, j):
        if j not in self.cache:
            self.cache[j] = self.conf_de(j)
        return self.cache[j]

    def quadro(self, i):
        np = self.np
        for j in [j for j in self.cache if j < i - 2]:
            del self.cache[j]
        li = self.lumas[i].astype(np.float32)
        acc = self._c(i) * self.PESOS[2]
        soma = np.full(li.shape, self.PESOS[2], np.float32)
        dois_sigma2 = 2.0 * SIGMA_TEMPO * SIGMA_TEMPO
        for k in (-2, -1, 1, 2):
            j = i + k
            if j < 0 or j >= self.n or self.segs[j] != self.segs[i]:
                continue
            dl = self.lumas[j].astype(np.float32) - li
            p = self.PESOS[k + 2] * np.exp(-(dl * dl) / dois_sigma2)
            acc = acc + self._c(j) * p
            soma += p
        return acc / soma


def limpar_mascara(alfa, np, cv2):
    """Buraco pequeno dentro da pessoa vira pessoa (o segmentador fura a camiseta escura); ilha
    pequena solta no fundo some. O tamanho é relativo ao quadro."""
    h, w = alfa.shape
    area = h * w
    corpo = (alfa > 0.5).astype(np.uint8)
    n, rotulos, est, _ = cv2.connectedComponentsWithStats(1 - corpo, connectivity=4)
    if n > 1:
        x, y, cw, ch, a = (est[:, k] for k in range(5))
        borda = (x == 0) | (y == 0) | (x + cw >= w) | (y + ch >= h)
        tapar = (~borda) & (a < 0.0015 * area)
        tapar[0] = False
        if tapar.any():
            alfa[tapar[rotulos]] = 1.0
    n, rotulos, est, _ = cv2.connectedComponentsWithStats(corpo, connectivity=8)
    if n > 2:
        areas = est[:, cv2.CC_STAT_AREA]
        maior = 1 + int(np.argmax(areas[1:]))
        apagar = areas < 0.003 * area
        apagar[0] = False
        apagar[maior] = False
        if apagar.any():
            ilhas = cv2.dilate(apagar[rotulos].astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
            alfa[ilhas] = 0.0
    return alfa


def caixa_da_cabeca(rosto, alfa, w, h, kx, ky):
    """A caixa da cabeça e do cabelo no tamanho de análise: 2,6 larguras de rosto (rosto.json) centradas
    nele, do alto da pessoa (a máscara, acima do rosto) até 0,9 largura de rosto abaixo do queixo (o
    cabelo comprido cai no ombro). None sem rosto naquele quadro."""
    if not rosto:
        return None
    rx, ry, rw, rh = rosto[0] * kx, rosto[1] * ky, rosto[2] * kx, rosto[3] * ky
    if rw < 8 or rh < 8:
        return None
    import numpy as np
    faixa = alfa[:, max(0, int(rx - rw)):min(w, int(rx + 2 * rw))] > 0.5
    linhas = np.flatnonzero(faixa.any(axis=1)) if faixa.size else np.array([])
    topo = float(linhas[0]) if linhas.size else ry - 0.4 * rh
    lado = min(float(w), 2.6 * rw)
    x0 = int(round(min(max(0.0, rx + rw / 2 - lado / 2), w - lado)))
    y0 = int(round(max(0.0, min(topo, ry) - 0.15 * rw)))
    y1 = int(round(min(float(h), ry + rh + 0.9 * rw)))
    if y1 - y0 < 16:
        return None
    return (x0, y0, int(round(lado)), y1 - y0)


class Cabelo:
    """O cabelo no recorte (4.3): o BiRefNet lite (MIT) na caixa da cabeça, em quadros-chave, levado aos
    quadros do meio pelo fluxo óptico.

    Os segmentadores veem o quadro em 256 px: o fio solto some, e o vão entre o cabelo comprido e o
    pescoço (a parede) entra como pessoa. O BiRefNet em 640 px na caixa da cabeça separa fio por fio,
    mas custa ~0,6 s por quadro na CPU, e sozinho ele acha "objeto" em qualquer coisa saliente (o neon
    ao lado da cabeça). Então:
      - ele roda em 1 quadro a cada CABELO_PASSO e nas pontas de cada trecho (nada atravessa emenda);
      - cada quadro do meio recebe os dois quadros-chave vizinhos levados até ele pelo fluxo óptico
        (Farneback, na caixa reduzida a 256 px), pesados pela distância no tempo e pela confiança do
        fluxo (cai onde a imagem do quadro-chave levada não bate com a do quadro: a mão que passou);
      - ele só manda numa faixa em volta do contorno da máscara de base, até CABELO_FORA da largura para
        fora (o fio que faltava) e CABELO_DENTRO para dentro (a parede entre os fios), com a força caindo
        nas bordas da caixa; o resto do quadro é a máscara de base;
      - o que ele põe a mais só fica onde a profundidade não diz "parede" (a mesma régua da
        confianca_combinada: 0 = a mediana do fundo, 1 = a da pessoa; abaixo de 0,2 sai, acima de 0,4
        fica): sem isso, pedacinhos da parede acima do ombro entravam como cabelo.
    Os quadros saem com atraso (só quando chega o próximo quadro-chave dá para misturar os dois), na
    ordem."""

    def __init__(self, sessao, largura, altura, rostos, kx, ky, segs, np, cv2, d8=None):
        self.s, self.np, self.cv2 = sessao, np, cv2
        self.d8 = d8
        self.ent = sessao.get_inputs()[0].name
        self.lado = int(sessao.get_inputs()[0].shape[2])
        self.w, self.h = largura, altura
        self.rostos, self.kx, self.ky, self.segs = rostos, kx, ky, segs
        self.fila = []             # [(i, quadro, alfa)] depois do último quadro-chave
        self.chave = None          # (i, cinza, caixa, B na caixa)
        self.rodadas = 0
        self.tempo = 0.0
        self.media = np.array([0.485, 0.456, 0.406], np.float32)
        self.desvio = np.array([0.229, 0.224, 0.225], np.float32)

    def _birefnet(self, quadro, caixa):
        np, cv2 = self.np, self.cv2
        x0, y0, cw, ch = caixa
        rec = quadro[y0:y0 + ch, x0:x0 + cw]
        L = self.lado
        x = cv2.resize(rec, (L, L), interpolation=cv2.INTER_AREA if max(rec.shape[:2]) > L else cv2.INTER_CUBIC)
        x = ((x.astype(np.float32) / 255.0 - self.media) / self.desvio).transpose(2, 0, 1)[None]
        t = time.time()
        a = self.s.run(None, {self.ent: np.ascontiguousarray(x)})[0][0, 0]
        self.tempo += time.time() - t
        self.rodadas += 1
        a = cv2.resize(a.astype(np.float32), (cw, ch), interpolation=cv2.INTER_LINEAR)
        # a borda do BiRefNet (640 px para a caixa toda) vai para a borda da imagem: filtro guiado fino
        r = max(2, int(round(2 * self.w / 576.0)))
        return np.clip(cv2.ximgproc.guidedFilter(rec.astype(np.float32) / 255.0, a, r, 1e-4), 0, 1)

    def _fazer_chave(self, i, quadro, alfa):
        r = self.rostos[i] if self.rostos and i < len(self.rostos) else None
        caixa = caixa_da_cabeca(r, alfa, self.w, self.h, self.kx, self.ky)
        cinza = self.cv2.cvtColor(quadro, self.cv2.COLOR_RGB2GRAY)
        return (i, cinza, caixa, self._birefnet(quadro, caixa) if caixa else None)

    def _levar(self, chave, cinza_p, caixa, esc):
        """O B do quadro-chave levado ao quadro i, na caixa: o fluxo (Farneback) e a confiança saem na
        caixa reduzida (cinza_p, lado maior CABELO_FLUXO); só o B é levado no tamanho cheio, para o fio
        não borrar. Devolve (B levado, confiança na caixa reduzida)."""
        np, cv2 = self.np, self.cv2
        k, cinza_k, caixa_k, B = chave
        x0, y0, cw, ch = caixa
        ph, pw = cinza_p.shape
        # a caixa reduzida do quadro-chave não muda entre dois quadros-chave: guardada
        cache = getattr(self, "_reduzidas", {})
        b = cache.get((k, caixa, pw, ph))
        if b is None:
            b = cv2.resize(cinza_k[y0:y0 + ch, x0:x0 + cw], (pw, ph), interpolation=cv2.INTER_AREA)
            cache = {kk: v for kk, v in cache.items() if kk[0] >= k - 2 * CABELO_PASSO}
            cache[(k, caixa, pw, ph)] = b
            self._reduzidas = cache
        fluxo = cv2.calcOpticalFlowFarneback(cinza_p, b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        kx0, ky0, kcw, kch = caixa_k
        # na caixa reduzida: a confiança (a imagem do quadro-chave levada bate com a do quadro?) e onde
        # o quadro-chave tem B (a caixa dele)
        gx, gy = np.meshgrid(np.arange(pw, dtype=np.float32), np.arange(ph, dtype=np.float32))
        mx, my = gx + fluxo[..., 0], gy + fluxo[..., 1]
        bk = cv2.remap(b, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        erro_ = cv2.GaussianBlur(np.abs(bk - cinza_p.astype(np.float32)), (0, 0), 1.0)
        fx, fy = mx / esc + x0, my / esc + y0          # o ponto do quadro-chave, em pixel de análise
        dentro = ((fx >= kx0) & (fx < kx0 + kcw) & (fy >= ky0) & (fy < ky0 + kch)).astype(np.float32)
        conf = np.exp(-(erro_ / CABELO_ERRO) ** 2) * dentro
        # o B no tamanho cheio: o fluxo ampliado
        fl = cv2.resize(fluxo, (cw, ch), interpolation=cv2.INTER_LINEAR) / esc
        gX, gY = self._grade(cw, ch)
        Bi = cv2.remap(B, gX + fl[..., 0] + (x0 - kx0), gY + fl[..., 1] + (y0 - ky0), cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        return Bi, conf

    def _grade(self, cw, ch):
        if getattr(self, "_g", None) is None or self._g[0].shape != (ch, cw):
            self._g = self.np.meshgrid(self.np.arange(cw, dtype=self.np.float32),
                                       self.np.arange(ch, dtype=self.np.float32))
        return self._g

    def _misturar(self, i, quadro, alfa, ka, kb):
        np, cv2 = self.np, self.cv2
        validas = [c for c in (ka, kb) if c is not None and c[2] is not None]
        if not validas:
            return alfa
        x0 = min(c[2][0] for c in validas)
        y0 = min(c[2][1] for c in validas)
        x1 = max(c[2][0] + c[2][2] for c in validas)
        y1 = max(c[2][1] + c[2][3] for c in validas)
        cw, ch = x1 - x0, y1 - y0
        esc = min(1.0, CABELO_FLUXO / float(max(cw, ch)))
        pw, ph = max(8, int(round(cw * esc))), max(8, int(round(ch * esc)))
        esc = pw / float(cw)
        cinza_p = cv2.resize(cv2.cvtColor(quadro[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY), (pw, ph),
                             interpolation=cv2.INTER_AREA)
        soma_p = np.zeros((ph, pw), np.float32)
        partes = []
        dist = abs(kb[0] - ka[0]) if ka is not None and kb is not None else 0
        for chave in validas:
            wt = 1.0 - abs(i - chave[0]) / float(dist) if dist else 1.0
            if wt <= 0:
                continue
            Bi, conf = self._levar(chave, cinza_p, (x0, y0, cw, ch), esc)
            partes.append((Bi, wt * conf))
            soma_p += wt * conf
        if not partes:
            return alfa
        if len(partes) == 1:
            B = partes[0][0]
        else:
            # o peso de cada quadro-chave sai na caixa reduzida e é ampliado uma vez só
            w0 = cv2.resize(partes[0][1] / np.maximum(soma_p, 1e-6), (cw, ch), interpolation=cv2.INTER_LINEAR)
            B = partes[1][0] + w0 * (partes[0][0] - partes[1][0])
        base = alfa[y0:y1, x0:x1]
        # a faixa em volta do contorno (até rf para fora e rd para dentro, borda suave), medida na caixa
        # reduzida e ampliada (ela é lisa)
        corpo = (cv2.resize(base, (pw, ph), interpolation=cv2.INTER_AREA) > 0.5).astype(np.uint8)
        rf = max(1.0, CABELO_FORA * self.w * esc)
        rd = max(1.0, CABELO_DENTRO * self.w * esc)
        d_fora = cv2.distanceTransform(1 - corpo, cv2.DIST_L2, 3)
        d_dentro = cv2.distanceTransform(corpo, cv2.DIST_L2, 3)
        faixa = np.clip((rf - d_fora) / (0.3 * rf), 0, 1) * np.clip((rd - d_dentro) / (0.3 * rd), 0, 1)
        # a força cai na borda de baixo da caixa (o ombro e a mão abaixo da cabeça ficam com a base) e
        # nos lados (onde a caixa corta a pessoa)
        yy, xx = np.arange(ph, dtype=np.float32), np.arange(pw, dtype=np.float32)
        ry = np.clip(np.minimum(yy / max(1.0, 0.05 * ph), (ph - 1 - yy) / max(1.0, 0.2 * ph)), 0, 1)
        rx = np.clip(np.minimum(xx, pw - 1 - xx) / max(1.0, 0.08 * pw), 0, 1)
        peso_p = faixa * np.clip(soma_p, 0, 1) * ry[:, None] * rx[None, :]
        # o que o BiRefNet põe a mais só fica onde a profundidade não diz "parede"
        d = self.d8[i] if self.d8 is not None and i < len(self.d8) else None
        veto_p = None
        if d is not None:
            dh, dw = d.shape
            pequena = cv2.resize(alfa, (dw, dh), interpolation=cv2.INTER_NEAREST)
            certo, longe = pequena > 0.9, pequena < 0.05
            if certo.sum() > 200 and longe.sum() > 200:
                dp, df = float(np.median(d[certo])), float(np.median(d[longe]))
                if dp - df >= 12:
                    kx, ky = dw / float(self.w), dh / float(self.h)
                    gx, gy = np.meshgrid((x0 + (np.arange(pw, dtype=np.float32) + 0.5) / esc) * kx - 0.5,
                                         (y0 + (np.arange(ph, dtype=np.float32) + 0.5) / esc) * ky - 0.5)
                    rel = (cv2.remap(d.astype(np.float32), gx, gy, cv2.INTER_LINEAR,
                                     borderMode=cv2.BORDER_REPLICATE) - df) / (dp - df)
                    veto_p = suave(rel, 0.2, 0.4, np)
        # o peso de pôr (vetado pela profundidade) e o de tirar, ampliados da caixa reduzida
        peso = cv2.resize(peso_p, (cw, ch), interpolation=cv2.INTER_LINEAR)
        mais = B - base
        if veto_p is not None:
            peso_mais = cv2.resize((peso_p * veto_p).astype(np.float32), (cw, ch), interpolation=cv2.INTER_LINEAR)
            novo = base + mais * np.where(mais > 0, peso_mais, peso)
        else:
            novo = base + mais * peso
        out = alfa.copy()
        # a ilha solta que o BiRefNet deixou na caixa sai (a regra de sempre, medida na caixa)
        out[y0:y1, x0:x1] = limpar_mascara(novo.astype(np.float32), np, cv2)
        return out

    def oferecer(self, i, quadro, alfa):
        """Devolve a lista de (i, quadro, alfa) prontos, na ordem (pode ser vazia)."""
        prontos = []
        if self.chave is not None and self.segs[i] != self.segs[self.chave[0]]:
            prontos += self._fechar_fila(fim=True)
        if self.chave is None:
            self.chave = self._fazer_chave(i, quadro, alfa)
            prontos.append((i, quadro, self._misturar(i, quadro, alfa, self.chave, None)))
            return prontos
        self.fila.append((i, quadro, alfa))
        if i - self.chave[0] >= CABELO_PASSO:
            prontos += self._fechar_fila(fim=False)
        return prontos

    def _fechar_fila(self, fim):
        """O último da fila vira quadro-chave; os do meio misturam os dois quadros-chave."""
        if not self.fila:
            if fim:
                self.chave = None
            return []
        j, qj, aj = self.fila[-1]
        kb = self._fazer_chave(j, qj, aj)
        prontos = [(i, q, self._misturar(i, q, a, self.chave, kb)) for i, q, a in self.fila[:-1]]
        prontos.append((j, qj, self._misturar(j, qj, aj, kb, None)))
        self.fila = []
        self.chave = None if fim else kb
        return prontos

    def terminar(self):
        return self._fechar_fila(fim=True)


def fazer_mascaras(ctx, brutos, d8, np, cv2, fundo_amostras, cabelo=None):
    """A máscara final de cada quadro, gravada em mascara/, numa segunda passada pelo vídeo (o filtro
    guiado precisa do quadro colorido inteiro). Guarda as amostras do fundo pelo caminho e mede a
    profundidade da pessoa e do fundo em cada quadro."""
    w, h = ctx["analise"]
    segs = ctx["seg_por_quadro"]
    n = brutos["total"]
    filtro = FiltroTemporal(
        lambda j: confianca_combinada(brutos["selfie"][j], brutos["multi"][j], d8[j] if d8 else None, np, cv2),
        brutos["luma"], segs, n, np)
    pasta = ctx["saida"] / "mascara"
    pasta.mkdir(parents=True, exist_ok=True)
    raio = max(3, int(round(GUIA_RAIO * w / 576.0)))
    caixas, prof_p, prof_f = [], [], []
    sw, sh = ctx["fonte_tam"]
    kx, ky = sw / float(w), sh / float(h)
    relogio = time.time()
    ultimo = relogio
    def gravar(j, quadro, alfa):
        alfa = firmar(alfa, w, np, cv2)
        m8 = (alfa * 255).round().astype(np.uint8)
        cv2.imwrite(str(pasta / ("m%06d.png" % (j + 1))), m8, [cv2.IMWRITE_PNG_COMPRESSION, 3])
        caixas.append(caixa_da_pessoa(m8, kx, ky, np))
        p, f = medianas_profundidade(m8, d8[j] if d8 else None, np, cv2)
        prof_p.append(p)
        prof_f.append(f)
        fundo_amostras.oferecer(j, quadro, m8)

    i = 0
    for quadro in Leitor(ctx["video"], ctx["fps"], ctx["analise"], ctx["fonte_tam"]):
        if i >= n:
            break
        c = cv2.resize(filtro.quadro(i), (w, h), interpolation=cv2.INTER_LINEAR)
        guia = quadro.astype(np.float32) / 255.0
        alfa = np.clip(cv2.ximgproc.guidedFilter(guia, c.astype(np.float32), raio, GUIA_EPS), 0, 1)
        alfa = limpar_mascara(alfa, np, cv2)
        # o cabelo devolve os quadros com atraso (espera o próximo quadro-chave), sempre na ordem
        for j, q, a in (cabelo.oferecer(i, quadro, alfa) if cabelo else [(i, quadro, alfa)]):
            gravar(j, q, a)
        i += 1
        agora = time.time()
        if agora - ultimo > 10:
            fala("    máscaras %d/%d  ·  %.0f ms por quadro" % (i, n, (agora - relogio) / i * 1000))
            ultimo = agora
    if cabelo:
        for j, q, a in cabelo.terminar():
            gravar(j, q, a)
    return caixas, prof_p, prof_f


def firmar(alfa, largura, np, cv2):
    """A borda do filtro guiado é larga e o miolo do cabelo fica meio transparente: com texto atrás,
    a letra aparecia através do cabelo, e a parede clara da borda virava um halo em volta da cabeça
    sobre o fundo escurecido. A curva estreita a borda (abaixo de 0,25 é fundo, acima de 0,75 é
    pessoa) e o miolo (a pessoa encolhida ~4 px) fica opaco, com a transição suave."""
    curva = suave(alfa, 0.25, 0.75, np)
    k = max(3, int(round(9 * largura / 576.0)) | 1)
    miolo = cv2.erode((alfa > 0.5).astype(np.uint8), np.ones((k, k), np.uint8)).astype(np.float32)
    miolo = cv2.GaussianBlur(miolo, (0, 0), max(1.0, 2.0 * largura / 576.0))
    return np.maximum(curva, miolo)


def medianas_profundidade(m8, d, np, cv2):
    """A profundidade relativa (0 a 255) mediana da pessoa e do fundo num quadro."""
    if m8 is None or d is None:
        return None, None
    m = cv2.resize(m8, (d.shape[1], d.shape[0]), interpolation=cv2.INTER_AREA)
    sel_p, sel_f = m > 200, m < 15
    return (int(np.median(d[sel_p])) if sel_p.sum() > 20 else None,
            int(np.median(d[sel_f])) if sel_f.sum() > 20 else None)


def caixa_da_pessoa(m8, kx, ky, np):
    linhas = np.flatnonzero((m8 > 127).any(axis=1))
    colunas = np.flatnonzero((m8 > 127).any(axis=0))
    if linhas.size == 0 or (m8 > 127).mean() < 0.005:
        return None
    x0, x1, y0, y1 = colunas[0], colunas[-1] + 1, linhas[0], linhas[-1] + 1
    return [int(round(x0 * kx)), int(round(y0 * ky)), int(round((x1 - x0) * kx)), int(round((y1 - y0) * ky))]


# ---------------------------------------------------------------------------
# Fundo limpo
# ---------------------------------------------------------------------------

class AmostrasFundo:
    """Uma amostra a cada N quadros, espalhada pelo vídeo inteiro: o quadro e onde ele é fundo. Os
    quadros vão direto para um bloco reservado de uma vez (empilhar uma lista depois dobrava a memória),
    e o número de amostras cai com a resolução (PIXELS_FUNDO)."""

    def __init__(self, total, tamanho, np, cv2, ligado):
        self.np, self.cv2 = np, cv2
        largura, altura = tamanho
        maximo = max(24, min(AMOSTRAS_FUNDO, PIXELS_FUNDO // max(1, largura * altura)))
        self.passo = max(1, int(math.ceil(total / float(maximo))))
        self.capacidade = int(math.ceil(total / float(self.passo))) + 1
        self.ligado = ligado
        r = max(2, int(round(DILATA_FUNDO * largura / 576.0)))
        self.nucleo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
        self.Q = self.V = None
        self.n = 0
        self.indices = []

    def oferecer(self, i, quadro, m8):
        if not self.ligado or i % self.passo or self.n >= self.capacidade:
            return
        if self.Q is None:
            h, w = quadro.shape[:2]
            self.Q = self.np.empty((self.capacidade, h, w, 3), self.np.uint8)
            self.V = self.np.empty((self.capacidade, h, w), bool)
        pessoa = self.cv2.dilate((m8 > 20).astype(self.np.uint8), self.nucleo)
        self.Q[self.n] = quadro
        self.V[self.n] = pessoa == 0
        self.n += 1
        self.indices.append(i)


def empurra_puxa(img, peso, np, cv2):
    """A cor de cada pixel sem dado, puxada dos que têm dado (push-pull): a pirâmide desce somando cor e
    peso, e sobe preenchendo o que falta com o nível de baixo. Sai lisa e sem borda dura, o oposto do
    TELEA, que arrastava a borda da prateleira escura buraco adentro num bloco de canto vivo."""
    niveis = []
    a, w = img * peso[..., None], peso.astype(np.float32)
    niveis.append((a, w))
    while min(w.shape) > 6:
        a, w = cv2.pyrDown(a), cv2.pyrDown(w)
        niveis.append((a, w))
    a, w = niveis[-1]
    media = (img * peso[..., None]).reshape(-1, 3).sum(axis=0) / max(1e-6, float(peso.sum()))
    cor = np.where(w[..., None] > 1e-5, a / np.maximum(w, 1e-6)[..., None], media[None, None, :])
    for a, w in reversed(niveis[:-1]):
        cor = cv2.pyrUp(cor, dstsize=(w.shape[1], w.shape[0]))
        k = np.clip(w * 3.0, 0, 1)[..., None]
        cor = (a / np.maximum(w, 1e-6)[..., None]) * k + cor * (1 - k)
    return cor.astype(np.float32)


def periodo_das_fiadas(lum, fonte, lo, hi, np):
    """O passo vertical que mais se repete na parede (as fiadas de tijolo, o rejunte), pela
    autocorrelação do perfil das linhas (a média da textura em cada linha, só nos pixels de fonte).
    Devolve (passo, correlação), ou (None, 0) sem parede que chegue."""
    n = fonte.sum(axis=1)
    linhas = n >= max(20, 0.05 * fonte.shape[1])
    if linhas.sum() < 3 * hi:
        return None, 0.0
    perfil = np.where(linhas, (lum * fonte).sum(axis=1) / np.maximum(n, 1), 0.0)
    perfil = np.where(linhas, perfil - perfil[linhas].mean(), 0.0)
    melhor, passo = 0.0, None
    for k in range(max(2, lo), hi + 1):
        m = linhas[:-k] & linhas[k:]
        if m.sum() < 3 * k:
            continue
        a, b = perfil[:-k][m], perfil[k:][m]
        c = float((a * b).sum() / math.sqrt((a * a).sum() * (b * b).sum() + 1e-12))
        if passo is None or c > melhor:
            melhor, passo = c, k
    return passo, melhor


def textura_em_blocos(textura, fonte, alvo, passo, fase, largura, np):
    """A textura da parede copiada para dentro do buraco em blocos do tamanho de duas fiadas, cada um
    trazido de cima ou de baixo por um múltiplo do passo: o rejunte cai na mesma altura e o bloco
    copiado é tijolo de verdade, com as juntas e a variação de cor de um tijolo para outro. Os blocos
    começam na linha do rejunte (as emendas de cima e de baixo somem nele) e cada fileira de blocos é
    deslocada meio bloco, como a amarração do tijolo (as emendas do lado não fazem uma linha
    contínua). Fica de cada bloco a cópia mais perto que tenha fonte em pelo menos 97% do que falta."""
    h, w = alvo.shape
    saida = np.zeros_like(textura)
    feito = np.zeros((h, w), bool)
    deslocamentos = []
    for k in range(1, h // passo + 2):
        deslocamentos += [k * passo, -k * passo]
    fileira = 0
    for y0 in range(fase - passo, h, passo):
        recuo = largura // 2 if fileira % 2 else 0
        fileira += 1
        for x0 in range(-recuo, w, largura):
            ya, yb, xa, xb = max(0, y0), min(h, y0 + passo), max(0, x0), min(w, x0 + largura)
            if ya >= yb or xa >= xb:
                continue
            falta = alvo[ya:yb, xa:xb]
            if not falta.any():
                continue
            for d in deslocamentos:
                if ya - d < 0 or yb - d > h:
                    continue
                ok = fonte[ya - d:yb - d, xa:xb]
                if ok[falta].mean() >= 0.97:
                    sel = falta & ok
                    saida[ya:yb, xa:xb][sel] = textura[ya - d:yb - d, xa:xb][sel]
                    feito[ya:yb, xa:xb] |= sel
                    break
    # o que nenhum bloco cobriu (perto de um objeto excluído da fonte): pixel a pixel, a cópia mais perto
    resto = alvo & ~feito
    for d in deslocamentos:
        if not resto.any():
            break
        if abs(d) >= h:
            continue
        ok = np.zeros((h, w), bool)
        if d > 0:
            ok[d:] = fonte[:-d]
        else:
            ok[:d] = fonte[-d:]
        sel = resto & ok
        if sel.any():
            ys, xs = np.nonzero(sel)
            saida[ys, xs] = textura[ys - d, xs]
            feito |= sel
            resto &= ~sel
    return saida, feito


def preencher_buraco(placa, buraco, np, cv2):
    """O que a pessoa nunca descobriu. Duas camadas:
      cor     a cor da parede em volta, puxada de perto para longe (empurra_puxa) em 1/4 do tamanho,
              ampliada e desfocada. Cada pixel conhecido pesa pelo quanto parece a parede (a mediana do
              anel em volta do buraco): a prateleira escura e o neon pesam quase nada, e não viram uma
              mancha escura de canto vivo no meio do tronco.
      textura a parede de verdade, continuada: a textura (a placa sobre a cor local dela, em razão, para
              valer com outra luz) é medida na parte vista, o passo das fiadas sai da própria parede
              (periodo_das_fiadas) e o buraco é coberto com blocos dela trazidos de cima ou de baixo
              por um múltiplo desse passo (textura_em_blocos). Na parede de tijolo, o rejunte e a
              amarração continuam pelo buraco, em vez da mancha lisa no formato da pessoa que a placa
              de trás do camadas mostrava (49% do fundo do teste é inventado). A fonte é só parede: o
              que é escuro, claro ou saturado demais (prateleira, luz, neon) e o detalhe forte ficam de
              fora, com folga.
    Tudo entra com borda suave sobre a placa. É uma continuação plausível, não o que estava lá."""
    h, w = buraco.shape
    s = w / 576.0
    conhecido = buraco == 0
    f = placa.astype(np.float32)
    # a cor de parede: a mediana do anel em volta do buraco
    r = max(3, int(round(40 * s)))
    anel = (cv2.dilate(buraco, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))) > 0) & conhecido
    parede = np.median(f[anel], axis=0) if anel.sum() > 50 else np.median(f[conhecido], axis=0)
    dist = np.sqrt(((f - parede[None, None, :]) ** 2).sum(axis=2))
    peso = conhecido * (0.02 + np.exp(-((dist / 55.0) ** 2)))
    fw, fh = max(8, w // 4), max(8, h // 4)
    cor = empurra_puxa(cv2.resize(f, (fw, fh), interpolation=cv2.INTER_AREA),
                       cv2.resize(peso.astype(np.float32), (fw, fh), interpolation=cv2.INTER_AREA), np, cv2)
    cor = cv2.GaussianBlur(cv2.resize(cor, (w, h), interpolation=cv2.INTER_CUBIC), (0, 0), max(2.0, 6.0 * s))

    # a textura: a placa sobre a média local dela (só dos pixels vistos, para o buraco não entrar na
    # conta), em log; o tijolo e o rejunte cabem nessa escala (16 px num quadro de 576)
    sig = max(4.0, 16.0 * s)
    vistos = conhecido.astype(np.float32)
    media = cv2.GaussianBlur(f * vistos[..., None], (0, 0), sig) / \
        np.maximum(cv2.GaussianBlur(vistos, (0, 0), sig), 1e-3)[..., None]
    textura = np.log(np.maximum(f, 2.0) / np.maximum(media, 2.0))
    lum = textura.mean(axis=2)
    r = max(2, int(round(12 * s)))
    seguro = cv2.erode(conhecido.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))) > 0
    preenchido = cor
    if seguro.sum() > 0.02 * h * w:
        cinza = f.mean(axis=2)
        claro = float(np.median(cinza[seguro]))
        forte = np.abs(lum) > max(0.12, 6.0 * float(np.median(np.abs(lum[seguro]))))
        estranho = (cinza < 0.55 * claro) | (cinza > 1.6 * claro) | (f.max(axis=2) - f.min(axis=2) > 150)
        k = int(15 * s) | 1
        fonte = seguro & ~(cv2.dilate((forte | estranho).astype(np.uint8), np.ones((k, k), np.uint8)) > 0)
        fiada, c1 = periodo_das_fiadas(lum, fonte, int(12 * s), int(45 * s), np)
        # o padrão se repete a cada duas fiadas (a junta vertical alterna); sem fiada clara, um passo
        # qualquer do tamanho de um tijolo ainda copia a textura fina de uma parede lisa
        passo = None
        if fiada and c1 >= 0.15:
            passo, _ = periodo_das_fiadas(lum, fonte, 2 * fiada - max(2, int(4 * s)), 2 * fiada + max(2, int(4 * s)), np)
        if not passo:
            passo = max(8, int(round(48 * s)))
        n = fonte.sum(axis=1)
        linhas = n >= 20
        perfil = np.where(linhas, (lum * fonte).sum(axis=1) / np.maximum(n, 1), np.nan)
        fase, melhor = 0, None
        for ff in range(passo):
            v = perfil[ff::passo]
            v = v[~np.isnan(v)]
            if len(v) and (melhor is None or v.mean() > melhor):
                fase, melhor = ff, float(v.mean())      # o rejunte é a linha mais clara
        tex, feito = textura_em_blocos(textura, fonte, buraco > 0, passo, fase, max(8, int(round(48 * s))), np)
        # 0,9: a parede inventada um tico mais calma que a vista (o olho aceita parede fora de foco)
        preenchido = cor * np.exp(0.9 * tex)
    mistura = cv2.GaussianBlur(cv2.dilate(buraco, np.ones((9, 9), np.uint8)).astype(np.float32),
                               (0, 0), max(2.0, 4.0 * s))[..., None]
    final = f * (1 - mistura) + preenchido * mistura
    return np.clip(final.round(), 0, 255).astype(np.uint8)


def fazer_fundo(ctx, amostras, np, cv2):
    """A mediana, pixel a pixel, das amostras em que o pixel é fundo. O que nunca foi visto (ou foi
    visto menos de MIN_FUNDO vezes) é inventado por preencher_buraco, com borda suave. Devolve a
    fração do quadro que foi inventada e o quanto a câmera andou (a mediana borra se ela andou)."""
    Q = amostras.Q[:amostras.n]               # (n, h, w, 3), sem cópia
    V = amostras.V[:amostras.n]               # (n, h, w)
    n, h, w = V.shape
    contagem = V.sum(axis=0)
    placa = np.zeros((h, w, 3), np.uint8)
    faixa = 64
    for y0 in range(0, h, faixa):
        y1 = min(h, y0 + faixa)
        q = Q[:, y0:y1]
        v = V[:, y0:y1]
        # o inválido vira 255 e vai para o fim da ordenação: as primeiras `contagem` posições são
        # exatamente os valores válidos em ordem, e a mediana é o do meio deles
        x = np.where(v[..., None], q, np.uint8(255))
        x.sort(axis=0)
        c = contagem[y0:y1]
        k = np.clip((c - 1) // 2, 0, n - 1)
        placa[y0:y1] = np.take_along_axis(x, k[None, :, :, None].repeat(3, axis=3), axis=0)[0]
    buraco = (contagem < MIN_FUNDO).astype(np.uint8)
    # a câmera andou? deslocamento do fundo entre a primeira e as outras amostras, na faixa de cima
    andou = 0.0
    try:
        topo = max(32, h // 5)
        cinza = [cv2.cvtColor(f[:topo], cv2.COLOR_RGB2GRAY).astype(np.float32) for f in Q]
        janela = cv2.createHanningWindow((w, topo), cv2.CV_32F)
        for g in cinza[1::max(1, len(cinza) // 12)]:
            (dx, dy), _ = cv2.phaseCorrelate(cinza[0], g, janela)
            andou = max(andou, math.hypot(dx, dy))
    except cv2.error:
        pass
    final = placa.copy()
    if buraco.any():
        final = preencher_buraco(placa, buraco, np, cv2)
    cv2.imwrite(str(ctx["saida"] / "fundo-limpo.jpg"), cv2.cvtColor(final, cv2.COLOR_RGB2BGR),
                [cv2.IMWRITE_JPEG_QUALITY, 93])
    cv2.imwrite(str(ctx["saida"] / "fundo-buraco.png"), buraco * 255)
    profundidade_do_fundo(ctx, final, np, cv2)
    return {"amostras": n, "passo": amostras.passo, "buraco": round(100.0 * float(buraco.mean()), 1),
            "camera_px": round(andou, 2)}, final, buraco


def profundidade_do_fundo(ctx, placa, np, cv2):
    """A profundidade do cenário sem a pessoa (3.0, Onda 3): é dela que a nuvem de pontos e a malha 3D
    tiram o relevo da parede, da prateleira e do que mais estiver atrás. Mais fina que a dos quadros
    (518 px no lado comprido), relativa como ela (255 = mais perto), normalizada pelos percentis 1 e 99
    da própria placa. Grava fundo-profundidade.png do tamanho da análise do Depth Anything."""
    import onnxruntime as ort
    h, w = placa.shape[:2]
    if h >= w:
        th = 518
        tw = max(14, int(round(518 * w / float(h) / 14.0)) * 14)
    else:
        tw = 518
        th = max(14, int(round(518 * h / float(w) / 14.0)) * 14)
    opcoes = ort.SessionOptions()
    opcoes.log_severity_level = 3
    sessao = ort.InferenceSession(str(ctx["modelos"] / MODELOS["profundidade"][0]), opcoes,
                                  providers=["CPUExecutionProvider"])
    x = cv2.resize(placa, (tw, th), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
    x = ((x - np.array([0.485, 0.456, 0.406], np.float32)) / np.array([0.229, 0.224, 0.225], np.float32))
    x = np.ascontiguousarray(x.transpose(2, 0, 1)[None])
    d = sessao.run(None, {sessao.get_inputs()[0].name: x})[0][0].astype(np.float32)
    lo, hi = np.percentile(d, 1), np.percentile(d, 99)
    d8 = np.clip((d - lo) / max(hi - lo, 1e-6) * 255.0, 0, 255).astype(np.uint8)
    cv2.imwrite(str(ctx["saida"] / "fundo-profundidade.png"), d8)


# ---------------------------------------------------------------------------
# Mãos, corpo e objetos
# ---------------------------------------------------------------------------

def meio_do_corpo(i, corpo, rosto, largura):
    """O x do meio do corpo no quadro i: os ombros, senão o rosto do rosto.json, senão o meio."""
    c = corpo[i] if corpo and i < len(corpo) else None
    if c is not None:
        p = c["pontos"]
        if p[11][2] > 0.3 and p[12][2] > 0.3:
            return (p[11][0] + p[12][0]) / 2.0
    if rosto and i < len(rosto) and rosto[i]:
        r = rosto[i]
        return r[0] + r[2] / 2.0
    return largura / 2.0


def palma(p, np):
    """O tamanho da mão, a régua das distâncias entre mãos: a média do pulso ao nó do dedo médio e do nó
    do indicador ao do mindinho (não muda quando a mão abre ou fecha)."""
    return max(8.0, (float(np.hypot(*(p[0, :2] - p[9, :2]))) + float(np.hypot(*(p[5, :2] - p[17, :2])))) / 2.0)


def caixa_dos_pontos(p):
    x0, y0 = float(p[:, 0].min()), float(p[:, 1].min())
    return [x0, y0, float(p[:, 0].max()) - x0, float(p[:, 1].max()) - y0]


def distancia_maos(a, b, np):
    """A distância entre duas leituras de mão, em palmas: (pulso, centro dos 21 pontos)."""
    s = (palma(a, np) + palma(b, np)) / 2.0
    return (float(np.hypot(*(a[0, :2] - b[0, :2]))) / s,
            float(np.hypot(*(a[:, :2].mean(axis=0) - b[:, :2].mean(axis=0)))) / s)


def pulsos_do_corpo(i, corpo):
    """Os dois pulsos do corpo no quadro i ([x, y, visibilidade], pontos 15 e 16), ou None."""
    c = corpo[i] if corpo and i < len(corpo) else None
    if c is None:
        return None
    return [c["pontos"][15], c["pontos"][16]]


def mao_repetida(a, b, pulsos, tamanho, np):
    """As duas leituras do mesmo quadro são a mesma mão? O MediaPipe às vezes acha de novo uma mão que o
    rastreio dele já segue, e devolve duas mãos em cima de uma (medido no teste: os pulsos a menos de
    0,4 palma, ou um esqueleto menor nas pontas dos dedos da mesma mão). Só que duas mãos de verdade
    também chegam perto: entrelaçadas, palma com palma, os pulsos ficam a ~0,5 a 1,5 palma. Então:
      - pulsos a menos de 0,6 palma, caixas com IoU de 0,45 ou mais e as duas apontando para o mesmo
        lado (menos de 25 graus entre pulso e nó do dedo médio): é a mesma, com ou sem corpo;
      - as caixas se tocando (IoU acima de 0,1) ou os centros a menos de 1,6 palma, quando o corpo diz
        que a outra mão não está ali (o pulso dela fora do quadro, ou a mais de 2,5 palmas das duas
        leituras): é a mesma."""
    dp, dc = distancia_maos(a, b, np)
    va, vb = a[9, :2] - a[0, :2], b[9, :2] - b[0, :2]
    giro = abs((math.degrees(math.atan2(va[1], va[0]) - math.atan2(vb[1], vb[0])) + 180.0) % 360.0 - 180.0)
    sobre = iou(caixa_dos_pontos(a), caixa_dos_pontos(b))
    if dp < 0.6 and giro < 25.0 and sobre >= 0.45:
        return True
    if not pulsos or (sobre <= 0.1 and dc >= 1.6):
        return False
    s = (palma(a, np) + palma(b, np)) / 2.0
    meio = (a[0, :2] + b[0, :2]) / 2.0
    perto = [float(np.hypot(p[0] - meio[0], p[1] - meio[1])) for p in pulsos]
    k = 0 if perto[0] <= perto[1] else 1
    if perto[k] > 4.5 * s:
        return False            # o corpo não está vendo esta mão: ele não serve de juiz aqui
    outro = pulsos[1 - k]
    w, h = tamanho
    fora = outro[2] < 0.3 or not (0 <= outro[0] < w and 0 <= outro[1] < h)
    longe = min(float(np.hypot(outro[0] - m[0, 0], outro[1] - m[0, 1])) for m in (a, b)) > 2.5 * s
    return fora or longe


MAO_SUMIDA = 15            # quadros: a trilha que não vê a mão por mais que isso acaba (a que volta é outra)
MAO_NOVA = 1.6             # o custo de abrir uma trilha nova, na régua de custo_trilha
MAO_FIRME = 3              # leituras seguidas com a mesma classificação (Left/Right do MediaPipe) que a firmam


def custo_trilha(t, m, i, np):
    """Quanto custa a leitura m continuar a trilha t no quadro i, ou None se a mão não pode ter andado
    tanto. A distância (pulso e centro, em palmas) até a última leitura da trilha, mais 0,12 por quadro
    em que a trilha não viu mão: a trilha vista no quadro anterior ganha da que sumiu há 12 quadros
    mesmo que a sumida tenha parado mais perto (era isso que trocava as mãos: a trilha velha roubava a
    mão da trilha viva). Mais 0,3 se o MediaPipe classificou a leitura com a outra mão (Left/Right):
    sozinha a classificação erra (mão de lado, mãos entrelaçadas), mas desempata duas mãos perto. A mão
    anda até 1,4 palma por quadro; com a mesma classificação, até 2 (o gesto rápido que entra pelo lado:
    no teste, 1,5 palma num quadro, e a mão que entrou pela esquerda virava uma mão nova à direita)."""
    falha = i - t["ultimo"]
    ultima = t["quadros"][t["ultimo"]]
    dp, dc = distancia_maos(ultima["pontos"], m["pontos"], np)
    d = (dp + dc) / 2.0
    mesma = m.get("rotulo") == ultima.get("rotulo")
    if d > min(3.0, (2.0 if mesma else 1.4) + 0.3 * (falha - 1)):
        return None
    return d + 0.12 * (falha - 1) + (0.0 if mesma else 0.3)


def cortar_na_troca(t):
    """A trilha que passa de uma mão para a outra sem soltar: quando as duas mãos se juntam (palma com
    palma, dedos entrelaçados), o MediaPipe às vezes vê uma só, e a leitura escorrega da mão de um lado
    para a do outro sem salto nenhum. O que denuncia é a classificação Left/Right, que é estável enquanto
    a mão é a mesma: MAO_FIRME leituras de uma, depois MAO_FIRME da outra, é outra mão. A trilha é
    cortada ali (cada pedaço decide o lado dele). Classificação que pisca menos que isso não corta.
    Devolve os pedaços, na ordem."""
    q = sorted(t["quadros"])
    rot = [t["quadros"][i].get("rotulo") or "" for i in q]
    cortes, firme, j = [], None, 0
    while j < len(q):
        k = j
        while k < len(q) and rot[k] == rot[j]:
            k += 1
        if k - j >= MAO_FIRME:
            if firme is not None and rot[j] != firme[0]:
                # o corte vai logo depois da última leitura da mão firme anterior
                cortes.append(firme[1])
            firme = (rot[j], k)
        j = k
    if not cortes:
        return [t]
    pedacos, ini = [], 0
    for c in cortes + [len(q)]:
        if c > ini:
            pedacos.append({"quadros": {i: t["quadros"][i] for i in q[ini:c]}, "ultimo": q[c - 1], "seg": t["seg"]})
        ini = c
    return pedacos


def montar_maos(brutas, ctx, corpo, np):
    """As mãos, do ponto de vista de quem assiste: "esquerda" é a mão que aparece à esquerda na tela.
      1. a mesma mão lida duas vezes no mesmo quadro (mao_repetida) vira uma: fica a leitura que melhor
         continua uma trilha;
      2. cada leitura continua a trilha de uma mão física (custo_trilha, a melhor combinação do quadro),
         ou abre uma nova. A trilha acaba quando a mão some por mais de MAO_SUMIDA quadros ou na emenda;
      3. falha curta interpolada e One Euro, trilha a trilha (nunca de uma trilha para outra);
      4. o lado é da trilha inteira (a identidade segue a continuidade: a mão que cruza o meio continua
         a mesma), decidido pela tela: em cada quadro medido em que a outra mão também está, vota o lado
         em que ela está em relação à outra (peso 1); sozinha, o lado do meio do corpo (os ombros, senão
         o rosto do rosto.json) em que ela apareceu (peso 0,5, que cai a cada leitura sozinha: a mão que
         aparece de novo é decidida por onde aparece). O voto é por palma de distância, até 1: duas mãos
         entrelaçadas quase não votam. A trilha de voto mais forte escolhe primeiro; a que dividiria um
         quadro medido com outra do mesmo lado fica com o outro. A leitura medida vale mais que o quadro
         preenchido de outra trilha (a falha curta interpolada por cima de uma mão que estava lá).
    No teste (corte-20), a regra anterior deixava o pulso da "esquerda" à direita do da "direita" em 245
    de 398 quadros com as duas mãos: a trilha velha roubava a mão viva, e uma leitura repetida virava a
    outra mão."""
    n = len(brutas)
    sw, sh = ctx["fonte_tam"]
    segs = ctx["seg_por_quadro"]
    rosto = ctx.get("rosto")
    trilhas, vivas = [], []
    for i, maos in enumerate(brutas):
        vivas = [t for t in vivas if i - t["ultimo"] <= MAO_SUMIDA and t["seg"] == segs[i]]
        if not maos:
            continue
        maos = list(maos[:2])
        if len(maos) == 2 and mao_repetida(maos[0]["pontos"], maos[1]["pontos"], pulsos_do_corpo(i, corpo),
                                           (sw, sh), np):
            def continua(m):
                cs = [c for c in (custo_trilha(t, m, i, np) for t in vivas) if c is not None]
                return (min(cs) if cs else MAO_NOVA, -m["score"])
            maos = [min(maos, key=continua)]
        # a combinação mais barata do quadro: cada leitura numa trilha viva diferente, ou numa nova
        melhor, escolha = None, None
        nv = len(vivas)
        for combo in _combinacoes(len(maos), nv):
            total = 0.0
            for m, e in zip(maos, combo):
                c = MAO_NOVA if e is None else custo_trilha(vivas[e], m, i, np)
                if c is None:
                    total = None
                    break
                total += c
            if total is not None and (melhor is None or total < melhor - 1e-9):
                melhor, escolha = total, combo
        novas = []
        for m, e in zip(maos, escolha):
            if e is None:
                t = {"quadros": {}, "ultimo": i, "seg": segs[i]}
                trilhas.append(t)
                novas.append(t)
            else:
                t = vivas[e]
            t["quadros"][i] = m
            t["ultimo"] = i
        vivas = vivas + novas

    trilhas = [p for t in trilhas for p in cortar_na_troca(t)]
    # 3. falha curta e One Euro, trilha a trilha
    filtro = UmEuro(ctx["fps"], corte_min=1.2, beta=0.008)
    for t in trilhas:
        serie_t = [None] * n
        for i, m in t["quadros"].items():
            serie_t[i] = m
        preencher_buracos(serie_t, segs, np)
        presente = [x is not None for x in serie_t]
        for a, b in corridas(presente):
            for sa, sb in ctx["segmentos"]:
                x0, x1 = max(a, sa), min(b, sb)
                if x1 - x0 < 1:
                    continue
                serie = np.stack([serie_t[j]["pontos"] for j in range(x0, x1)])
                lisa = filtro.filtrar(serie.reshape(len(serie), -1), np).reshape(serie.shape)
                for j in range(x0, x1):
                    serie_t[j] = {"score": serie_t[j]["score"], "medido": serie_t[j]["medido"],
                                  "pontos": lisa[j - x0]}
        t["quadros"] = {j: serie_t[j] for j in range(n) if serie_t[j] is not None}

    # 4. o lado de cada trilha, pela tela
    em = [[] for _ in range(n)]
    for k, t in enumerate(trilhas):
        for i in t["quadros"]:
            em[i].append(k)

    def x_da_mao(p):
        return (float(p[0, 0]) + float(p[:, 0].mean())) / 2.0     # o pulso e o centro: o braço vem do lado

    for k, t in enumerate(trilhas):
        voto, sozinha = 0.0, 0
        for i in sorted(t["quadros"]):
            m = t["quadros"][i]
            if not m["medido"]:
                continue
            x, s = x_da_mao(m["pontos"]), palma(m["pontos"], np)
            outras = [trilhas[u]["quadros"][i] for u in em[i] if u != k and trilhas[u]["quadros"][i]["medido"]]
            if outras:
                for o in outras:
                    voto += max(-1.0, min(1.0, (x_da_mao(o["pontos"]) - x) / s))
            else:
                # sozinha, vale o lado em que ela apareceu: o peso cai a cada leitura (0,7: as primeiras
                # ~5 decidem), e a mão que entra pela esquerda e cruza o meio continua "esquerda"
                voto += 0.5 * 0.7 ** sozinha * max(-1.0, min(1.0, (meio_do_corpo(i, corpo, rosto, sw) - x) / s))
                sozinha += 1
        if voto == 0.0:     # sem voto nenhum (só quadros preenchidos): o lado do meio do corpo
            i0 = min(t["quadros"])
            voto = 1e-6 if x_da_mao(t["quadros"][i0]["pontos"]) < meio_do_corpo(i0, corpo, rosto, sw) else -1e-6
        t["voto"] = voto
    lados = ("esquerda", "direita")
    trilha = {l: [None] * n for l in lados}
    for k in sorted(range(len(trilhas)), key=lambda k: (-abs(trilhas[k]["voto"]), min(trilhas[k]["quadros"]))):
        t = trilhas[k]
        quer = "esquerda" if t["voto"] > 0 else "direita"
        outro = "direita" if quer == "esquerda" else "esquerda"
        choques = {l: [i for i, m in t["quadros"].items() if trilha[l][i] is not None
                       and (trilha[l][i]["medido"] or not m["medido"])] for l in lados}
        lado = quer if len(choques[quer]) <= len(choques[outro]) else outro
        # com os dois lados ocupados num quadro medido, aquele quadro fica com quem já estava; o quadro
        # preenchido de outra trilha cede à leitura medida
        for i, m in t["quadros"].items():
            if trilha[lado][i] is None or (m["medido"] and not trilha[lado][i]["medido"]):
                trilha[lado][i] = m
    quadros = []
    for i in range(n):
        q = []
        for lado in lados:
            m = trilha[lado][i]
            if m is not None:
                q.append({"lado": lado, "score": round(float(m["score"]), 3), "medido": bool(m["medido"]),
                          "pontos": [[round(float(p[0]), 1), round(float(p[1]), 1), round(float(p[2]), 1)]
                                     for p in m["pontos"]]})
        quadros.append(q)
    return quadros


def _combinacoes(k, nv):
    """As formas de pôr k leituras (0, 1 ou 2) em trilhas vivas diferentes (índices 0..nv-1) ou numa
    nova (None), numa ordem fixa."""
    opcoes = list(range(nv)) + [None]
    if k == 1:
        return [(a,) for a in opcoes]
    return [(a, b) for a in opcoes for b in opcoes if a is None or b is None or a != b]


def preencher_buracos(trilha, segs, np):
    """Falha de até BURACO_MAOS quadros entre duas detecções do mesmo trecho: os pontos são
    interpolados, e o quadro sai com "medido": false. A confiança é a da ponta medida mais perto: um
    número que o modelo deu de verdade (num quadro vizinho), nunca uma mistura inventada."""
    n = len(trilha)
    i = 0
    while i < n:
        if trilha[i] is None:
            a = i - 1
            b = i
            while b < n and trilha[b] is None:
                b += 1
            if a >= 0 and b < n and b - a - 1 <= BURACO_MAOS and segs[a] == segs[b]:
                pa, pb = trilha[a], trilha[b]
                for j in range(a + 1, b):
                    f = (j - a) / float(b - a)
                    trilha[j] = {"score": (pa if f <= 0.5 else pb)["score"], "medido": False,
                                 "pontos": pa["pontos"] * (1 - f) + pb["pontos"] * f}
            i = b
        else:
            i += 1


def montar_corpo(brutos, ctx, np):
    t = list(brutos)
    segs = ctx["seg_por_quadro"]
    preencher_buracos(t, segs, np)
    filtro = UmEuro(ctx["fps"], corte_min=1.0, beta=0.006)
    presente = [x is not None for x in t]
    for a, b in corridas(presente):
        for sa, sb in ctx["segmentos"]:
            x0, x1 = max(a, sa), min(b, sb)
            if x1 - x0 < 1:
                continue
            serie = np.stack([t[j]["pontos"][:, :2] for j in range(x0, x1)])
            lisa = filtro.filtrar(serie.reshape(len(serie), -1), np).reshape(serie.shape)
            for j in range(x0, x1):
                pts = t[j]["pontos"].copy()
                pts[:, :2] = lisa[j - x0]
                t[j] = {"score": t[j]["score"], "medido": t[j]["medido"], "pontos": pts}
    out = []
    for c in t:
        if c is None:
            out.append(None)
        else:
            out.append({"score": round(float(c["score"]), 3), "medido": bool(c["medido"]),
                        "pontos": [[round(float(p[0]), 1), round(float(p[1]), 1), round(float(p[2]), 3)]
                                   for p in c["pontos"]]})
    return out


def iou(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix = max(0.0, min(ax + aw, bx + bw) - max(ax, bx))
    iy = max(0.0, min(ay + ah, by + bh) - max(ay, by))
    inter = ix * iy
    uniao = aw * ah + bw * bh - inter
    return inter / uniao if uniao > 0 else 0.0


def montar_objetos(brutos, ctx, np):
    """Os quadros analisados ficam como saíram, com "medido": true. Entre dois analisados do mesmo
    trecho, a caixa que casa (mesma categoria, IoU >= 0,3) é interpolada; a que não casa vale só nos
    quadros mais perto da análise dela. Nos dois casos o quadro sai com "medido": false, e a confiança
    é a da análise mais perto: um número que o modelo deu de verdade, nunca uma mistura das duas (uma
    peça que mostra "pessoa 0,90" mostra o que o detector disse)."""
    n = len(brutos)
    chaves = [i for i in range(n) if brutos[i] is not None]
    saida = [None] * n

    def formatar(o, medido, caixa=None):
        cx = o["caixa"] if caixa is None else caixa
        return {"categoria": CATEGORIAS.get(o["en"], o["en"]), "categoria_en": o["en"],
                "score": round(float(o["score"]), 3), "medido": medido,
                "caixa": [int(round(v)) for v in cx]}

    for i in chaves:
        saida[i] = [formatar(o, True) for o in brutos[i]]
    for a, b in zip(chaves[:-1], chaves[1:]):
        if b - a <= 1:
            continue
        mesmo = ctx["seg_por_quadro"][a] == ctx["seg_por_quadro"][b]
        pares, usados_a, usados_b = [], set(), set()
        if mesmo:
            candidatos = sorted(((iou(oa["caixa"], ob["caixa"]), ka, kb)
                                 for ka, oa in enumerate(brutos[a]) for kb, ob in enumerate(brutos[b])
                                 if oa["en"] == ob["en"]), reverse=True)
            for v, ka, kb in candidatos:
                if v < 0.3 or ka in usados_a or kb in usados_b:
                    continue
                pares.append((ka, kb))
                usados_a.add(ka)
                usados_b.add(kb)
        for j in range(a + 1, b):
            f = (j - a) / float(b - a)
            lista = []
            for ka, kb in pares:
                oa, ob = brutos[a][ka], brutos[b][kb]
                lista.append(formatar(oa if f <= 0.5 else ob, False, oa["caixa"] * (1 - f) + ob["caixa"] * f))
            perto_de_a = (j - a) <= (b - j) if mesmo else ctx["seg_por_quadro"][j] == ctx["seg_por_quadro"][a]
            if perto_de_a:
                lista += [formatar(o, False) for k, o in enumerate(brutos[a]) if k not in usados_a]
            else:
                lista += [formatar(o, False) for k, o in enumerate(brutos[b]) if k not in usados_b]
            saida[j] = lista
    # antes da primeira análise e depois da última (o último quadro do vídeo cai fora do passo): vale
    # a análise mais perto
    if chaves:
        for j in range(0, chaves[0]):
            saida[j] = [formatar(o, False) for o in brutos[chaves[0]]]
        for j in range(chaves[-1] + 1, n):
            saida[j] = [formatar(o, False) for o in brutos[chaves[-1]]]
    return [s if s is not None else [] for s in saida]


# ---------------------------------------------------------------------------
# Gravação
# ---------------------------------------------------------------------------

def gravar_quadros(destino, cabecalho, quadros):
    """Um quadro por linha: o arquivo continua JSON e dá para ler e comparar."""
    linhas = ["{"]
    for chave, valor in cabecalho.items():
        linhas.append("  %s: %s," % (json.dumps(chave), json.dumps(valor, ensure_ascii=False)))
    linhas.append('  "quadros": [')
    corpo = ["    " + json.dumps(q, ensure_ascii=False, separators=(",", ":")) for q in quadros]
    if corpo:
        linhas.append(",\n".join(corpo))
    linhas.append("  ]")
    linhas.append("}")
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def ler_json(caminho):
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Folha de contato
# ---------------------------------------------------------------------------

def carregar_fonte(tamanho):
    from PIL import ImageFont
    for caminho in FONTES_DO_SISTEMA:
        if os.path.isfile(caminho):
            try:
                return ImageFont.truetype(caminho, tamanho)
            except OSError:
                pass
    try:
        return ImageFont.load_default(size=tamanho)
    except TypeError:
        return ImageFont.load_default()


def cor_profundidade(d8, np, cv2):
    """A régua da folha: roxo da marca longe, ciano no meio, âmbar e branco perto."""
    paleta = np.array([[20, 6, 40], [66, 0, 151], [0, 153, 255], [247, 167, 17], [255, 245, 230]], np.float32)
    x = d8.astype(np.float32) / 255.0 * (len(paleta) - 1)
    k = np.clip(np.floor(x).astype(int), 0, len(paleta) - 2)
    f = (x - k)[..., None]
    return (paleta[k] * (1 - f) + paleta[k + 1] * f).astype(np.uint8)


def folha_de_contato(destino, ctx, np, cv2, mascaras_dir, prof_dir, maos, corpo, objetos, fundo_img, buraco, meta):
    from PIL import Image, ImageDraw
    w, h = ctx["analise"]
    n = ctx["total"]
    sw, sh = ctx["fonte_tam"]
    cel_h = 384
    cel_w = int(round(cel_h * w / float(h)))
    ks = cel_w / float(sw)
    margem, topo = 12, 46
    colunas = 4
    indices = [min(n - 1, int((j + 0.5) * n / INSTANTES)) for j in range(INSTANTES)]
    linha_zoom = int(cel_h * 0.9)
    larg = margem + colunas * (cel_w + margem)
    alt = topo + (cel_h + margem + 24) + INSTANTES * (cel_h + margem) + 30 + linha_zoom + margem
    folha = Image.new("RGB", (larg, alt), FUNDO_FOLHA)
    dd = ImageDraw.Draw(folha)
    f1, f2 = carregar_fonte(17), carregar_fonte(13)
    # sem a parte, o cabeçalho diz que ela não há (um 0% ali seria uma medida que ninguém fez)
    pp, bp = meta.get("pessoa_pct"), meta.get("buraco_pct")
    dd.text((margem, 8), "visao.py  ·  %s  ·  %d quadros  ·  %s  ·  %s"
            % (ctx["video"].name, n, "pessoa em %.1f%%" % pp if pp is not None else "sem máscara",
               "fundo inventado %.1f%%" % bp if bp is not None else "sem fundo limpo"), fill=BRANCO, font=f1)
    extra = []
    if meta.get("prof"):
        extra.append("profundidade %s" % meta["prof"])
    if pp is not None:
        extra.append("cabelo %s" % ("BiRefNet" if meta.get("cabelo") else "sem BiRefNet"))
    if extra:
        dd.text((margem, 29), "  ·  ".join(extra), fill=BRANCO, font=f2)

    def leia_quadro(i):
        r = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", str(ctx["video"]), "-vf",
                            "fps=%s,select=eq(n\\,%d),scale=%d:%d:flags=area" % (ctx["fps"], i, w, h),
                            "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
        if len(r.stdout) < w * h * 3:
            return np.zeros((h, w, 3), np.uint8)
        return np.frombuffer(r.stdout[:w * h * 3], np.uint8).reshape(h, w, 3)

    def cel(img):
        return Image.fromarray(cv2.resize(img, (cel_w, cel_h), interpolation=cv2.INTER_AREA))

    # linha de cima: o fundo limpo, o buraco e a profundidade média
    y = topo
    rotulos = []
    if fundo_img is not None:
        folha.paste(cel(fundo_img), (margem, y))
        rotulos.append((margem, "fundo-limpo.jpg"))
        b = fundo_img.copy()
        if buraco is not None:
            b[buraco > 0] = (b[buraco > 0] * 0.35 + np.array(ROSA) * 0.65).astype(np.uint8)
        folha.paste(cel(b), (margem + cel_w + margem, y))
        rotulos.append((margem + cel_w + margem, "inventado (rosa)"))
    for x, t in rotulos:
        dd.text((x, y + cel_h + 4), t, fill=BRANCO, font=f2)
    y += cel_h + margem + 24

    xadrez = ((np.indices((h, w)).sum(axis=0) // max(8, w // 36)) % 2 * 60 + 70).astype(np.uint8)
    xadrez = np.repeat(xadrez[..., None], 3, axis=2)
    zooms = []
    for i in indices:
        quadro = leia_quadro(i)
        m = cv2.imread(str(mascaras_dir / ("m%06d.png" % (i + 1))), cv2.IMREAD_GRAYSCALE) if mascaras_dir else None
        x = margem
        # 1: a máscara sobre o quadro (fundo escurecido, contorno no acento)
        if m is not None:
            a = (m.astype(np.float32) / 255.0)[..., None]
            sob = (quadro * (0.3 + 0.7 * a)).astype(np.uint8)
            borda = cv2.morphologyEx((m > 127).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
            sob[borda > 0] = ROSA
            folha.paste(cel(sob), (x, y))
            rec = (quadro * a + xadrez * (1 - a)).astype(np.uint8)
            folha.paste(cel(rec), (x + cel_w + margem, y))
            zooms.append((i, rec))
        else:
            folha.paste(cel(quadro), (x, y))
        x += 2 * (cel_w + margem)
        # 3: a profundidade
        if prof_dir and (prof_dir / ("p%06d.png" % (i + 1))).is_file():
            d = cv2.imread(str(prof_dir / ("p%06d.png" % (i + 1))), cv2.IMREAD_GRAYSCALE)
            folha.paste(cel(cor_profundidade(d, np, cv2)), (x, y))
        x += cel_w + margem
        # 4: mãos, corpo e objetos
        c = cel(quadro)
        dc = ImageDraw.Draw(c)
        if objetos and i < len(objetos):
            for o in objetos[i]:
                bx, by, bw_, bh_ = [v * ks for v in o["caixa"]]
                dc.rectangle([bx, by, bx + bw_, by + bh_], outline=AMBAR, width=2)
                dc.text((bx + 3, by + 2), "%s %.2f" % (o["categoria"], o["score"]), fill=AMBAR, font=f2)
        if corpo and i < len(corpo) and corpo[i]:
            p = corpo[i]["pontos"]
            for a_, b_ in OSSOS_CORPO:
                if p[a_][2] > 0.5 and p[b_][2] > 0.5:
                    dc.line([p[a_][0] * ks, p[a_][1] * ks, p[b_][0] * ks, p[b_][1] * ks], fill=BRANCO, width=2)
        if maos and i < len(maos):
            for mao in maos[i]:
                p = mao["pontos"]
                cor = CIANO if mao["lado"] == "esquerda" else ROSA
                for a_, b_ in OSSOS_MAO:
                    dc.line([p[a_][0] * ks, p[a_][1] * ks, p[b_][0] * ks, p[b_][1] * ks], fill=cor, width=2)
                for q in p:
                    dc.ellipse([q[0] * ks - 2, q[1] * ks - 2, q[0] * ks + 2, q[1] * ks + 2], fill=BRANCO)
                dc.text((p[0][0] * ks + 4, p[0][1] * ks + 4), "%s %.2f" % (mao["lado"], mao["score"]),
                        fill=cor, font=f2)
        folha.paste(c, (x, y))
        dd.text((margem + 4, y + 4), "%d  ·  %.2f s" % (i + 1, i / float(ctx["fps"])), fill=BRANCO, font=f2)
        y += cel_h + margem
    dd.text((margem, y + 6), "1 máscara (contorno rosa)   2 recorte no xadrez   3 profundidade (roxo longe, "
            "âmbar perto)   4 mãos (ciano = esquerda na tela, rosa = direita), corpo e objetos", fill=BRANCO, font=f2)
    y += 30
    # a última linha: a cabeça ampliada sobre o xadrez, onde a máscara mais erra (cabelo, orelha)
    xz = margem
    dw = (larg - 4 * margem) // 3
    for i, rec in zooms[::2][:3]:
        r = ctx["rosto"][i] if ctx.get("rosto") and i < len(ctx["rosto"]) and ctx["rosto"][i] else None
        if r:
            cx, cy = (r[0] + r[2] / 2.0) * w / sw, (r[1] + r[3] * 0.2) * h / sh
            larg_z = r[2] * w / sw * 1.7
        else:
            cx, cy, larg_z = w / 2.0, h * 0.3, w * 0.5
        alt_z = larg_z * linha_zoom / float(dw)
        x0 = int(np.clip(cx - larg_z / 2, 0, max(0, w - larg_z)))
        y0 = int(np.clip(cy - alt_z / 2, 0, max(0, h - alt_z)))
        corte = rec[y0:y0 + int(alt_z), x0:x0 + int(larg_z)]
        img = Image.fromarray(cv2.resize(corte, (dw, linha_zoom), interpolation=cv2.INTER_CUBIC))
        folha.paste(img, (xz, y))
        xz += dw + margem
    folha.save(str(destino))


# ---------------------------------------------------------------------------
# Linha de comando
# ---------------------------------------------------------------------------

def origem_do_video(video, fps, total=None):
    st = video.stat()
    o = {"versao": VERSAO, "versoes": dict(VERSOES), "video": str(video.resolve()), "mtime": st.st_mtime,
         "tamanho": st.st_size, "fps": fps}
    if total is not None:
        o["total"] = total
    return o


def parte_valida(nome, pasta, origem_antiga, origem_nova, variante=None):
    """A parte gravada vale para este vídeo, nesta versão (e, se pedida, nesta variante: o modelo da
    profundidade, a máscara com ou sem o cabelo)?"""
    if not origem_antiga:
        return False
    if variante is not None and (origem_antiga.get("variantes") or {}).get(nome) != variante:
        return False
    for chave in ("video", "mtime", "tamanho", "fps"):
        if origem_antiga.get(chave) != origem_nova.get(chave):
            return False
    # a versão daquela parte (gravação antiga, sem "versoes": todas na versão do script de então)
    versoes = origem_antiga.get("versoes") or {p: origem_antiga.get("versao") for p in PARTES}
    if versoes.get(nome) != VERSOES[nome]:
        return False
    if not (origem_antiga.get("partes") or {}).get(nome):
        return False
    total = origem_antiga.get("total") or 0
    if nome == "mascara":
        return total > 0 and len(list((pasta / "mascara").glob("m*.png"))) >= total
    if nome == "profundidade":
        return total > 0 and len(list((pasta / "profundidade").glob("p*.png"))) >= total
    arquivo = {"fundo": "fundo-limpo.jpg", "maos": "maos.json", "corpo": "corpo.json", "objetos": "objetos.json"}[nome]
    return (pasta / arquivo).is_file()


def principal():
    ap = argparse.ArgumentParser(
        description="Recorte da pessoa, fundo limpo, profundidade, mãos, corpo e objetos, quadro a quadro "
                    "(visao/, MOTOR.md 2.6).")
    ap.add_argument("--projeto", help="pasta do projeto, por exemplo projetos/aula")
    ap.add_argument("--corte", help="número do corte, por exemplo 01")
    ap.add_argument("--so", help="só estas partes: " + ",".join(PARTES))
    ap.add_argument("--refazer", action="store_true", help="refaz mesmo o que já vale para este vídeo")
    ap.add_argument("--profundidade", choices=["vda", "dav2"], default="vda",
                    help="vda (padrão: Video Depth Anything Small, estável no tempo) ou dav2 (Depth Anything V2 "
                         "Small, quadro a quadro)")
    ap.add_argument("--cabelo", choices=["auto", "sim", "nao"], default="auto",
                    help="o BiRefNet no cabelo: auto (padrão: liga quando o tempo estimado cabe em %d s), sim ou nao"
                         % CABELO_TETO)
    if len(sys.argv) == 1:
        ap.print_help()
        print("\nFaltou dizer qual corte. Comece por:")
        print("  flow-reels produzir/visao --projeto projetos/<video> --corte 01")
        return 2
    args = ap.parse_args()
    if not args.projeto or not args.corte:
        erro("diga o projeto e o corte: --projeto projetos/<video> --corte 01")
        return 2
    pedidas = PARTES[:]
    if args.so:
        pedidas = [p.strip().lower().replace("ã", "a") for p in args.so.split(",") if p.strip()]
        ruins = [p for p in pedidas if p not in PARTES]
        if ruins:
            erro("--so não conhece %s; as partes são %s" % (", ".join(ruins), ", ".join(PARTES)))
            return 2

    for nome in ("ffmpeg", "ffprobe"):
        if shutil.which(nome) is None:
            erro("%s não encontrado no PATH. Rode o instalar.sh na raiz do pacote." % nome)
            return 2
    np = carregar("numpy", "numpy")
    cv2 = carregar("cv2", "opencv-contrib-python")
    if not hasattr(cv2, "ximgproc"):
        erro("o OpenCV deste Python não tem o ximgproc (filtro guiado). Instale o opencv-contrib-python.")
        return 2

    raiz = achar_raiz()
    numero = re.sub(r"\D", "", args.corte)
    if not numero:
        erro("--corte é o número do corte, por exemplo 01")
        return 2
    projeto = Path(args.projeto)
    if not projeto.is_dir() and not projeto.is_absolute() and (raiz / projeto).is_dir():
        projeto = raiz / projeto
    pasta = projeto / "materiais-de-trabalho" / ("corte-%02d" % int(numero))
    if not pasta.is_dir():
        erro("não achei a pasta do corte %s" % pasta)
        return 2
    cenas = ler_json(pasta / "cenas.json") or {}
    fps = int(cenas.get("fps", 30) or 30)
    video = pasta / ((cenas.get("fonte") or {}).get("video") or "fala.mp4")
    if not video.is_file():
        erro("não achei %s.\n       O fala.mp4 sai do editar_fala.py; rode ele antes (MOTOR.md, seção 7)." % video)
        return 2
    modelos = fabrica.pasta("componentes/modelos")
    for chave in ("selfie", "multiclasse", "profundidade", "maos", "corpo", "objetos"):
        if not (modelos / MODELOS[chave][0]).is_file():
            erro("não achei o modelo %s em componentes/modelos/. Ele vem no pacote (gratuito, %s)."
                 % (MODELOS[chave][0], MODELOS[chave][2]))
            return 2

    sw, sh, duracao = sondar_video(video)
    if sh > ALTURA_MAX:
        w, h = par(sw * ALTURA_MAX / float(sh)), ALTURA_MAX
    else:
        w, h = sw, sh
    escala_b = LADO_BRUTO / float(max(w, h))
    bw, bh = (par(w * escala_b), par(h * escala_b)) if escala_b < 1 else (w, h)
    saida = pasta / "visao"
    saida.mkdir(parents=True, exist_ok=True)
    origem_antiga = ler_json(saida / ".origem.json")
    origem_nova = origem_do_video(video, fps)
    rosto = ler_json(pasta / "rosto.json")
    total_esperado = int(round(duracao * fps)) if duracao else 0

    # a profundidade: o VDA se os dois ONNX estão no pacote, senão o DAv2 de antes
    prof_modo = args.profundidade
    if prof_modo == "vda" and not all((modelos / MODELOS[k][0]).is_file() for k in ("vda_codificador", "vda_cabeca")):
        aviso("não achei %s e %s em componentes/modelos/; a profundidade sai do Depth Anything V2 Small, quadro a "
              "quadro (menos estável no tempo)." % (MODELOS["vda_codificador"][0], MODELOS["vda_cabeca"][0]))
        prof_modo = "dav2"
    # o cabelo: precisa do rosto.json (a caixa da cabeça) e do ONNX; no auto, liga se os quadros-chave
    # estimados cabem em CABELO_TETO
    trechos = len(ler_segmentos(pasta, total_esperado or 1, fps, duracao)) if total_esperado else 1
    chaves_est = int(math.ceil(total_esperado / float(CABELO_PASSO))) + 2 * trechos
    cabelo_est = chaves_est * CABELO_SEGUNDOS + total_esperado * (
        CABELO_QUADRO[0] + CABELO_QUADRO[1] * (w * h) / float(1080 * 1920))
    cabelo_ok = (modelos / MODELOS["cabelo"][0]).is_file() and bool(rosto and isinstance(rosto.get("quadros"), list))
    cabelo = args.cabelo == "sim" or (args.cabelo == "auto" and cabelo_est <= CABELO_TETO)
    if cabelo and not cabelo_ok:
        if args.cabelo == "sim" or (modelos / MODELOS["cabelo"][0]).is_file():
            aviso("o cabelo precisa do rosto.json (a caixa da cabeça) e de %s em componentes/modelos/; "
                  "a máscara sai sem ele." % MODELOS["cabelo"][0])
        cabelo = False
    variantes = {"profundidade": prof_modo, "mascara": "cabelo" if cabelo else "sem-cabelo"}

    # valem = gravadas para este mesmo vídeo; validas = as que esta rodada reaproveita (--refazer
    # refaz as pedidas, mas não invalida as outras). A variante (o modelo da profundidade, o cabelo) só
    # conta para a parte pedida: um --so maos não derruba a máscara feita com o cabelo
    valem = {p: parte_valida(p, saida, origem_antiga, origem_nova,
                             variantes.get(p) if p in pedidas else None) for p in PARTES}
    validas = {p: valem[p] and not (args.refazer and p in pedidas) for p in PARTES}
    fazer = [p for p in pedidas if not validas[p]]
    if "mascara" in fazer and "fundo" not in fazer:
        fazer.append("fundo")      # o fundo sai da máscara: máscara nova, fundo novo
    if "fundo" in fazer and "mascara" not in fazer and not validas["mascara"]:
        fazer.append("mascara")    # e não sai de máscara de outro vídeo: sem uma que valha, ela vem junto
    fala("")
    fala("  visão  ·  %s" % video)
    fala("  %dx%d, %.1f s a %d fps; análise em %dx%d%s" % (sw, sh, duracao, fps, w, h,
                                                      "" if (w, h) == (sw, sh) else " (reduzido)"))
    if not fazer:
        fala("  tudo já está gravado para este vídeo (use --refazer para refazer).")
        fala("")
        return 0
    reaproveitadas = [p for p in pedidas if validas[p]]
    fala("  vou fazer: %s%s" % (", ".join(fazer),
                                ("  ·  reaproveito: " + ", ".join(reaproveitadas)) if reaproveitadas else ""))
    if "profundidade" in fazer or ("mascara" in fazer and not validas["profundidade"]):
        fala("  profundidade: %s" % ("Video Depth Anything Small (estável no tempo)" if prof_modo == "vda"
                                     else "Depth Anything V2 Small (quadro a quadro)"))
    if "mascara" in fazer:
        if cabelo:
            fala("  cabelo: BiRefNet na cabeça, ~%d quadros-chave (~%.0f s a mais)" % (chaves_est, cabelo_est))
        elif args.cabelo == "auto" and cabelo_ok:
            fala("  cabelo: desligado (o BiRefNet levaria ~%.0f s, mais que %.0f s; use --cabelo sim)"
                 % (cabelo_est, CABELO_TETO))

    relogio_total = time.time()
    caminhos = {}
    with_seg = "mascara" in fazer
    if with_seg:
        c, falhas = escolher_caminho("segmentador", modelos / MODELOS["selfie"][0])
        if not c:
            erro("o segmentador do MediaPipe não abriu nesta máquina:\n       " + "\n       ".join(falhas))
            return 2
    for nome in ("maos", "corpo", "objetos"):
        if nome in fazer:
            c, falhas = escolher_caminho(nome, modelos / MODELOS[nome][0])
            if c:
                caminhos[nome] = c
            else:
                aviso("%s: o MediaPipe não abriu nesta máquina; fica sem %s.json.\n         %s"
                      % (nome, nome, "\n         ".join(falhas)))
    precisa_prof_modelo = "profundidade" in fazer or (with_seg and not validas["profundidade"])
    ctx = {"video": video, "fps": fps, "fonte_tam": (sw, sh), "analise": (w, h), "bruto": (bw, bh),
           "modelos": modelos, "prof_tam": tamanho_profundidade(w, h), "saida": saida, "rosto": None,
           "total_esperado": total_esperado, "prof_modo": prof_modo}
    if rosto and isinstance(rosto.get("quadros"), list):
        ctx["rosto"] = rosto["quadros"]

    # ---- 1. a passada de análise
    brutos = {"total": 0, "tempo": 0.0}
    tarefa = {"segmentar": with_seg, "profundidade": precisa_prof_modelo}
    tarefa.update({k: v for k, v in caminhos.items()})
    if any(tarefa.values()):
        fala("  analisando (%s)..." % ", ".join(k for k, v in tarefa.items() if v))
        # os trechos aqui são pela duração (o total exato só se sabe no fim da leitura); servem para o
        # detector de objetos analisar as pontas de cada trecho
        brutos = analisar(dict(ctx, segmentos=ler_segmentos(pasta, total_esperado or 10 ** 6, fps, duracao)),
                          tarefa, np, cv2)
    total = brutos["total"] or (origem_antiga or {}).get("total") or total_esperado
    if not total:
        erro("o ffmpeg não entregou nenhum quadro de %s." % video)
        return 2
    segmentos = ler_segmentos(pasta, total, fps, duracao)
    ctx.update(total=total, segmentos=segmentos, seg_por_quadro=segmento_de(segmentos, total))
    tempos = {"analise": round(brutos["tempo"], 1)}

    # ---- 2. profundidade
    # do visao.json anterior só se aproveita o que é de uma parte reaproveitada (validas): com o
    # fala.mp4 trocado, as caixas da pessoa, as medianas de profundidade, o fundo e os resumos eram do
    # vídeo velho, e saíam no visao.json novo, no relatório e na folha como se fossem deste
    meta_velho = ler_json(saida / "visao.json") or {}
    mesmo_video = bool(origem_antiga) and all(origem_antiga.get(k) == origem_nova.get(k)
                                              for k in ("video", "mtime", "tamanho", "fps"))
    if not mesmo_video:
        meta_velho = {}
    d8 = None
    prof_gravada = False
    meta_prof = dict(meta_velho.get("profundidade") or {}) if validas["profundidade"] else {}
    if precisa_prof_modelo:
        relogio = time.time()
        d8, percentis = finalizar_profundidade(brutos["profundidade"], brutos["luma_prof"], ctx["seg_por_quadro"], np)
        brutos["profundidade"] = brutos["luma_prof"] = None   # a bruta (float16) não serve mais: libera a memória
        if "profundidade" in fazer or not validas["profundidade"]:
            pp = saida / "profundidade"
            pp.mkdir(exist_ok=True)
            for i, d in enumerate(d8):
                cv2.imwrite(str(pp / ("p%06d.png" % (i + 1))), d, [cv2.IMWRITE_PNG_COMPRESSION, 3])
            meta_prof = {"percentis_brutos": list(percentis), "modelo": prof_modo}
            prof_gravada = True
        tempos["profundidade"] = round(time.time() - relogio, 1)
        tempos["profundidade_modelo"] = round(brutos.get("prof_segundos", 0.0), 1)
    elif with_seg:
        d8 = [cv2.imread(str(saida / "profundidade" / ("p%06d.png" % (i + 1))), cv2.IMREAD_GRAYSCALE)
              for i in range(total)]

    # ---- 3. máscaras e fundo
    caixas = prof_pessoa = prof_fundo = None
    info_fundo = meta_velho.get("fundo") if validas["fundo"] else None
    info_cabelo = meta_velho.get("cabelo") if validas["mascara"] else None
    fundo_img = buraco = None
    if "mascara" in fazer or "fundo" in fazer:
        relogio = time.time()
        amostras = AmostrasFundo(total, (w, h), np, cv2, "fundo" in fazer)
        if "mascara" in fazer:
            fala("  recortando a pessoa%s..." % (" (com o cabelo)" if cabelo else ""))
            cab = None
            if cabelo:
                import onnxruntime as ort
                opcoes = ort.SessionOptions()
                opcoes.log_severity_level = 3
                cab = Cabelo(ort.InferenceSession(str(modelos / MODELOS["cabelo"][0]), opcoes,
                                                  providers=["CPUExecutionProvider"]),
                             w, h, ctx["rosto"], w / float(sw), h / float(sh), ctx["seg_por_quadro"], np, cv2, d8)
            caixas, prof_pessoa, prof_fundo = fazer_mascaras(ctx, brutos, d8, np, cv2, amostras, cab)
            brutos["selfie"] = brutos["multi"] = brutos["luma"] = None
            if cab:
                info_cabelo = {"passo": CABELO_PASSO, "quadros_chave": cab.rodadas,
                               "segundos": round(cab.tempo, 1), "modelo": MODELOS["cabelo"][1]}
                tempos["cabelo"] = round(cab.tempo, 1)
        else:
            # só o fundo: as máscaras gravadas valem
            for i, quadro in enumerate(Leitor(video, fps, (w, h), (sw, sh))):
                if i >= total:
                    break
                if i % amostras.passo == 0:
                    m8 = cv2.imread(str(saida / "mascara" / ("m%06d.png" % (i + 1))), cv2.IMREAD_GRAYSCALE)
                    if m8 is not None:
                        amostras.oferecer(i, quadro, m8)
        tempos["mascara"] = round(time.time() - relogio, 1)
        if "fundo" in fazer and amostras.n:
            relogio = time.time()
            fala("  montando o fundo limpo com %d amostras..." % amostras.n)
            info_fundo, fundo_img, buraco = fazer_fundo(ctx, amostras, np, cv2)
            tempos["fundo"] = round(time.time() - relogio, 1)

    # ---- 4. mãos, corpo e objetos
    corpo_q = maos_q = objetos_q = None
    if "corpo" in caminhos:
        corpo_q = montar_corpo(brutos["corpo"], ctx, np)
        gravar_quadros(saida / "corpo.json", {"fps": fps, "largura": sw, "altura": sh,
                                              "modelo": MODELOS["corpo"][1], "licenca": MODELOS["corpo"][2]}, corpo_q)
    if "maos" in caminhos:
        # o corpo (pulsos e ombros) ajuda a separar as mãos: o mesmo que vai para o corpo.json (o desta
        # rodada, senão o gravado que vale), para --so maos dar o mesmo que a rodada inteira
        corpo_ref = corpo_q if corpo_q is not None else ((ler_json(saida / "corpo.json") or {}).get("quadros")
                                                         if validas["corpo"] else None) or []
        maos_q = montar_maos(brutos["maos"], ctx, corpo_ref, np)
        gravar_quadros(saida / "maos.json", {"fps": fps, "largura": sw, "altura": sh,
                                             "modelo": MODELOS["maos"][1], "licenca": MODELOS["maos"][2],
                                             "lado": "de quem assiste: esquerda = a mão à esquerda na tela"},
                       maos_q)
    if "objetos" in caminhos:
        objetos_q = montar_objetos(brutos["objetos"], ctx, np)
        gravar_quadros(saida / "objetos.json", {"fps": fps, "largura": sw, "altura": sh,
                                                "modelo": MODELOS["objetos"][1], "licenca": MODELOS["objetos"][2],
                                                "passo": PASSO_OBJETOS, "limiar": LIMIAR_OBJETO}, objetos_q)
    # o JSON gravado só volta para o resumo e para a folha se ele vale para este vídeo
    if corpo_q is None and validas["corpo"]:
        corpo_q = (ler_json(saida / "corpo.json") or {}).get("quadros")
    if maos_q is None and validas["maos"]:
        maos_q = (ler_json(saida / "maos.json") or {}).get("quadros")
    if objetos_q is None and validas["objetos"]:
        objetos_q = (ler_json(saida / "objetos.json") or {}).get("quadros")

    # ---- 5. o que vale agora, e o visao.json
    feitas = set(fazer) - ({"maos", "corpo", "objetos"} - set(caminhos))
    if "fundo" in fazer and info_fundo is None:
        feitas.discard("fundo")
    if prof_gravada:
        feitas.add("profundidade")      # refeita porque a máscara precisou dela
    partes = {p: p in feitas or (p not in fazer and valem[p]) for p in PARTES}
    antigas = [p for p in PARTES if not partes[p] and (saida / {"mascara": "mascara", "profundidade": "profundidade",
               "fundo": "fundo-limpo.jpg", "maos": "maos.json", "corpo": "corpo.json",
               "objetos": "objetos.json"}[p]).exists()]
    # a variante de cada parte: a desta rodada para o que foi feito agora, a gravada para o resto
    var_antigas = (origem_antiga or {}).get("variantes") or {}
    var_final = {}
    for p, v in variantes.items():
        if p in feitas:
            var_final[p] = v
        elif partes.get(p) and p in var_antigas:
            var_final[p] = var_antigas[p]
    origem_final = dict(origem_nova, total=total, partes=partes, variantes=var_final)
    (saida / ".origem.json").write_text(json.dumps(origem_final, indent=1), encoding="utf-8")

    if caixas is None and validas["mascara"] and isinstance(meta_velho.get("pessoa"), dict):
        caixas = meta_velho["pessoa"].get("caixas")
    pessoa_pct = (100.0 * sum(1 for c in caixas if c) / max(1, len(caixas))) if caixas else 0.0
    # medianas de profundidade da pessoa e do fundo, por quadro (0 a 255, relativas): medidas junto
    # com a máscara; com a máscara reaproveitada e a profundidade nova, medidas agora
    if d8 is not None and partes["mascara"] and prof_pessoa is None:
        prof_pessoa, prof_fundo = [], []
        for i in range(total):
            m = cv2.imread(str(saida / "mascara" / ("m%06d.png" % (i + 1))), cv2.IMREAD_GRAYSCALE)
            p, f = medianas_profundidade(m, d8[i], np, cv2)
            prof_pessoa.append(p)
            prof_fundo.append(f)
    if prof_pessoa is not None:
        meta_prof = dict(meta_prof)
        vp = [v for v in prof_pessoa if v is not None]
        vf = [v for v in prof_fundo if v is not None]
        meta_prof.update({
            "escala": "relativa: inverso da distância normalizado em 0 a 255 (255 = mais perto); não é metro",
            "tamanho": list(tamanho_profundidade(w, h)),
            "mediana_pessoa": int(np.median(vp)) if vp else None,
            "mediana_fundo": int(np.median(vf)) if vf else None,
            "pessoa": prof_pessoa, "fundo": prof_fundo})
    if not partes["mascara"]:
        # as medianas da pessoa e do fundo saem da máscara: sem máscara que valha, não há medida
        for chave in ("pessoa", "fundo", "mediana_pessoa", "mediana_fundo"):
            meta_prof.pop(chave, None)
    if not partes["profundidade"]:
        meta_prof = {}
    caminhos_meta = {k: v for k, v in (meta_velho.get("caminhos") or {}).items() if partes.get(k)}
    if partes["mascara"]:
        caminhos_meta["segmentador"] = "cpu"
    caminhos_meta.update(caminhos)
    if prof_gravada:
        caminhos_meta["profundidade"] = ("cpu (codificador) + %s (cabeça temporal)" % brutos.get("prof_caminho", "cpu")
                                         if prof_modo == "vda" else "cpu")
    if "mascara" in feitas:
        caminhos_meta.pop("cabelo", None)
        if info_cabelo:
            caminhos_meta["cabelo"] = "cpu"
    # os modelos usados neste vídeo (o DAv2 sempre: é ele que faz a fundo-profundidade.png)
    usados = ["selfie", "multiclasse", "profundidade", "maos", "corpo", "objetos"]
    if var_final.get("profundidade") == "vda":
        usados += ["vda_codificador", "vda_cabeca"]
    if info_cabelo:
        usados.append("cabelo")
    meta_final = {
        "versao": VERSAO,
        "fonte": video.name,
        "fps": fps, "largura": sw, "altura": sh, "analise": [w, h], "total": total,
        "segmentos": [[a, b] for a, b in segmentos],
        "modelos": {k: {"arquivo": MODELOS[k][0], "nome": MODELOS[k][1], "licenca": MODELOS[k][2]} for k in usados},
        "caminhos": caminhos_meta,
        "tempos": dict({k: v for k, v in (meta_velho.get("tempos") or {}).items()
                        if not (k == "cabelo" and "mascara" in feitas)
                        and not (k == "profundidade_modelo" and prof_gravada)}, **tempos),
        "partes": partes,
        "pessoa": {"porcentagem": round(pessoa_pct, 1), "caixas": caixas} if caixas else None,
        "profundidade": meta_prof or None,
        "fundo": info_fundo,
        "cabelo": info_cabelo if partes["mascara"] else None,
        "maos": {"porcentagem": round(100.0 * sum(1 for q in maos_q if q) / max(1, len(maos_q)), 1)} if maos_q else None,
        "corpo": {"porcentagem": round(100.0 * sum(1 for q in corpo_q if q) / max(1, len(corpo_q)), 1)} if corpo_q else None,
        "objetos": _resumo_objetos(objetos_q),
    }
    tempo_total = time.time() - relogio_total
    meta_final["tempos"]["total"] = round(tempo_total, 1)
    (saida / "visao.json").write_text(json.dumps(meta_final, ensure_ascii=False, separators=(",", ":")),
                                      encoding="utf-8")

    # ---- 6. folha de contato
    if fundo_img is None and partes["fundo"] and (saida / "fundo-limpo.jpg").is_file():
        f = cv2.imread(str(saida / "fundo-limpo.jpg"))
        fundo_img = cv2.cvtColor(f, cv2.COLOR_BGR2RGB) if f is not None else None
        b = cv2.imread(str(saida / "fundo-buraco.png"), cv2.IMREAD_GRAYSCALE)
        buraco = b if b is not None else None
    folha = pasta / "folha-visao.png"
    try:
        folha_de_contato(folha, ctx, np, cv2, saida / "mascara" if partes["mascara"] else None,
                         saida / "profundidade" if partes["profundidade"] else None,
                         maos_q, corpo_q, objetos_q, fundo_img, buraco,
                         {"pessoa_pct": pessoa_pct if caixas else None,
                          "buraco_pct": (info_fundo or {}).get("buraco") if partes["fundo"] else None,
                          "prof": {"vda": "VDA", "dav2": "DAv2"}.get(var_final.get("profundidade"))
                          if partes["profundidade"] else None,
                          "cabelo": bool(info_cabelo) if partes["mascara"] else None})
        folha_ok = True
    except ImportError:
        aviso("o Pillow não está instalado neste Python, então a folha de contato não saiu.")
        folha_ok = False

    # ---- relatório
    fala("")
    if caixas:
        fala("  pessoa      em %.1f%% dos quadros (máscara com mais de 0,5%% do quadro)" % pessoa_pct)
    if meta_prof and meta_prof.get("mediana_pessoa") is not None:
        fala("  distância   relativa, 0 a 255 (255 = mais perto): pessoa %s, fundo %s; não é metro"
             % (meta_prof["mediana_pessoa"], meta_prof["mediana_fundo"]))
    if prof_gravada:
        fala("  profund.    %s, %.1f s de modelo (%s)" % (
            "Video Depth Anything Small" if prof_modo == "vda" else "Depth Anything V2 Small",
            tempos.get("profundidade_modelo", 0.0), caminhos_meta.get("profundidade", "cpu")))
    if "mascara" in feitas and info_cabelo:
        fala("  cabelo      BiRefNet em %d quadros-chave, %.1f s" % (info_cabelo["quadros_chave"], info_cabelo["segundos"]))
    if info_fundo:
        fala("  fundo       mediana de %d amostras (1 a cada %d quadros); %.1f%% do quadro inventado"
             " (fundo-buraco.png)" % (info_fundo["amostras"], info_fundo["passo"], info_fundo["buraco"]))
        if info_fundo.get("camera_px", 0) > 2:
            aviso("o fundo andou %.1f px entre as amostras: a câmera mexeu, e o fundo limpo sai borrado."
                  % info_fundo["camera_px"])
    if maos_q is not None:
        fala("  mãos        em %.1f%% dos quadros" % meta_final["maos"]["porcentagem"])
    if corpo_q is not None:
        fala("  corpo       em %.1f%% dos quadros" % meta_final["corpo"]["porcentagem"])
    if objetos_q is not None:
        r = meta_final["objetos"] or {}
        cats = ", ".join("%s (%d%%)" % (k, v) for k, v in sorted((r.get("categorias") or {}).items(),
                                                                key=lambda kv: -kv[1])[:6])
        fala("  objetos     %s" % (cats or "nenhum acima de %.1f de confiança" % LIMIAR_OBJETO))
    fala("  tempo       %.1f s para %.1f s de vídeo (análise %.1f s)" % (tempo_total, duracao, tempos["analise"]))
    fala("")
    fala("  gravado     %s" % saida)
    if folha_ok:
        fala("  folha       %s  (OLHE: contorno rosa colado na pessoa, cabelo inteiro, fundo sem fantasma)" % folha)
    if antigas:
        aviso("estas partes são de outro vídeo ou de outra versão e não valem mais: %s. Rode com --so %s."
              % (", ".join(antigas), ",".join(antigas)))
    fala("")
    if caixas and pessoa_pct / 100.0 < POUCO:
        fala("  POUCA PESSOA  o recorte achou alguém em só %.1f%% dos quadros. O motor usa a máscara do"
             " jeito que ela está; olhe a folha antes de pôr texto atrás de você." % pessoa_pct)
        return 1
    return 0


def _resumo_objetos(objetos_q):
    if not objetos_q:
        return None
    cont = {}
    for q in objetos_q:
        for c in {o["categoria"] for o in q}:
            cont[c] = cont.get(c, 0) + 1
    n = max(1, len(objetos_q))
    return {"passo": PASSO_OBJETOS, "limiar": LIMIAR_OBJETO,
            "categorias": {k: int(round(100.0 * v / n)) for k, v in cont.items()}}


if __name__ == "__main__":
    sys.exit(principal())
