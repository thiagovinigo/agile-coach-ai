#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
expressao.py  ·  o rosto de quem fala, quadro a quadro (Fábrica 4.3, frente "rosto e expressão")

Roda o MediaPipe Face Landmarker (Apache-2.0, com os 52 blendshapes e a matriz da pose da cabeça) no
vídeo do corte e grava visao/expressao.json: por quadro, a expressão resumida (piscar de cada olho, boca
aberta, sorriso, sobrancelha, bochecha, beicinho, olho arregalado, para onde o olhar vai), a pose da
cabeça (yaw, pitch, roll em graus) e os pontos úteis do rosto em pixels da fonte (olhos, cantos, boca,
nariz, testa, queixo, sobrancelhas) e uma malha leve de 83 pontos; e os EVENTOS com tempo, que servem de
gatilho para as sobreposições presas ao rosto do motor (sobre/rosto-fx.js): piscada (a dupla separada),
boca-aberta (o "uau"), sorriso, sobrancelha (surpresa), cabeca-vira e aceno.

O caminho:

  grade      a mesma do compor.py e do visao.py: o vídeo é o cenas.json → fonte.video (padrão
             fala.mp4), lido pelo ffmpeg com -vf fps=<fps do plano>; o quadro i é o instante i/fps.
             Quadro com mais de 1920 px de altura é reduzido para a análise; os pontos voltam para o
             pixel da fonte.
  modelo     Face Landmarker em modo VIDEO, um rosto, com blendshapes e a matriz. No Mac, só no Metal
             (o caminho de CPU dos landmarkers do MediaPipe aborta), testado antes num processo
             separado; imagem SRGBA. O detector é fechado e aberto de novo a cada 100 quadros (o Metal
             retém memória até o close()) e em cada emenda (o rastreio não atravessa o corte).
  lados      de quem assiste: "esquerda" é o olho à esquerda na tela. O "Left" dos blendshapes do
             MediaPipe é o lado da pessoa (o olho da direita na tela), conferido nos três cortes reais
             pela íris (olhar) e pela abertura das pálpebras (piscar).
  pose       yaw > 0 = o rosto vira para a direita da tela; pitch > 0 = olha para cima; roll > 0 = a
             cabeça inclina no sentido horário (o topo vai para a direita da tela). Conferidos contra o
             nariz e a linha dos olhos (correlação de 0,88 a 0,99 nos três cortes).
  limpeza    falha de até 6 quadros dentro de um trecho é preenchida em linha reta ("m": false); a
             presença "a" desce em 6 quadros antes de o rosto sumir e sobe em 6 depois que ele volta
             (nunca pula), e corta seco na emenda (a imagem pula junto).
  suavização zero-phase (ida e volta, média das duas), trecho a trecho, nada atravessa emenda: One Euro
             nos pontos (em unidades da distância entre os olhos) e na pose; binômio 1-2-1 nos
             blendshapes (a piscada de 3 quadros continua lá).
  eventos    medidos nos sinais quase crus (abaixo), dentro de cada trecho.

Os eventos (todos com tipo, quadro, t e x, y em pixels da fonte):

  piscada      os dois olhos fecham e abrem em até 12 quadros (0,4 s): a abertura das pálpebras (EAR)
               cai abaixo de 0,32 da mediana de 2 s em volta e o blendshape passa de 0,55. Olhar para
               baixo também fecha a pálpebra, mas devagar e por mais tempo: não conta. "olho": "ambos",
               ou o lado da piscadela (um olho fecha, o outro fica acima de 0,8 da mediana).
               Duas piscadas com menos de 0,7 s entre os começos são uma "piscada-dupla" (evento próprio,
               no começo da primeira; as duas piscadas levam "dupla": true).
  boca-aberta  pico do jawOpen ≥ 0,40, com proeminência de 0,20 sobre o mínimo de ±0,5 s e 3 quadros
               ou mais acima de 0,30; 0,8 s entre dois (fica o maior). Campos: pico, de, ate.
  sorriso      o sorriso (média dos dois cantos) passa de 0,50 e fica acima de 0,40 por 8 quadros ou mais,
               subindo 0,25 sobre o nível dos 2 s de antes (quem sorri o tempo todo não dispara a cada
               frase); o evento é a subida. Campos: pico, ate.
  sobrancelha  pico da sobrancelha (o maior entre browInnerUp e a média dos browOuterUp) ≥ 0,35, com
               proeminência de 0,20 sobre o mínimo de ±0,6 s; 1 s entre dois; fora de piscada (a piscada
               puxa o blendshape da sobrancelha junto). Campos: pico, de, ate.
  cabeca-vira  o yaw anda mais de 60°/s por 3 quadros ou mais no mesmo sentido, somando 10° ou mais; o
               evento é o quadro mais rápido. Campos: sentido (+1 = para a direita da tela), de, ate (graus
               do começo e do fim), vel (°/s); 0,5 s entre dois.
  aceno        o pitch sem a tendência (menos a média de 0,8 s) oscila: 3 passadas seguidas ou mais
               (desce-sobe-desce), cada uma de 5° ou mais e de 0,1 a 0,5 s, com o pitch andando 1,5 vez
               o que o yaw anda no trecho. Campos: n (meias-oscilações), amplitude (graus), ate.

Saída: visao/expressao.json (contrato em motor/docs-4/rosto-expressao.md). O compor.py entrega ao motor
em window.VISAO.expressao quando o "origem" dele é o mesmo .origem.json da visão (o mesmo fala.mp4).

Uso:
    flow-reels produzir/expressao --projeto projetos/<video> --corte NN
    flow-reels produzir/expressao --projeto projetos/<video> --corte NN --resumo     # só imprime os momentos
    flow-reels produzir/expressao --projeto projetos/<video> --corte NN --folha      # e a folha de contato

Saída 0 = gravou; 1 = gravou, mas o rosto aparece em menos da metade dos quadros; 2 = erro (falta o
vídeo, o modelo, o ffmpeg, ou o Face Landmarker não abriu).
"""
import argparse
import json
import math
import os
import subprocess
import sys
import time
import types
from contextlib import contextmanager
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

VERSAO = 1
ALTURA_MAX = 1920          # quadro mais alto que isso é reduzido para a análise
RENOVAR = 100              # quadros: o detector é fechado e aberto de novo (memória do Metal)
BURACO = 6                 # quadros: falha preenchida dentro de um trecho
FADE = 6                   # quadros de entrada e de saída da presença
POUCO = 0.5                # rosto em menos que isso dos quadros: saída 1

MODELOS = {
    "rosto": ("face_landmarker.task", "MediaPipe Face Landmarker (blendshapes, float16)", "Apache-2.0",
              "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/"
              "face_landmarker.task"),
}

# ------------------------------------------------------------------ os limiares
L = {
    "piscada_ear": 0.32,        # EAR / mediana de 2 s abaixo disto no fundo da piscada
    "piscada_ear_corrida": 0.62,  # o trecho candidato: EAR / mediana abaixo disto
    "piscada_bs": 0.55,         # blendshape do piscar (média dos dois) no fundo
    "piscada_max": 12,          # quadros: mais que isso é olho fechado ou olhar para baixo
    "piscadela_aberto": 0.8,    # o outro olho acima disto da mediana: piscadela de um olho
    "dupla_s": 0.7,             # s entre os começos de duas piscadas
    "boca_pico": 0.40,
    "boca_prom": 0.20,
    "boca_janela_s": 0.5,
    "boca_sustenta": 0.30,
    "boca_min_q": 3,
    "boca_espaco_s": 0.8,
    "sorriso_entra": 0.50,
    "sorriso_fica": 0.40,
    "sorriso_min_q": 8,
    "sorriso_sobe": 0.25,
    "sorriso_antes_s": 2.0,
    "sobrancelha_pico": 0.35,
    "sobrancelha_prom": 0.20,
    "sobrancelha_janela_s": 0.6,
    "sobrancelha_espaco_s": 1.0,
    "sobrancelha_olho_max": 0.45,  # o piscar (média) no pico acima disto: é a piscada, não a sobrancelha
    "vira_vel": 60.0,           # °/s
    "vira_min_q": 3,
    "vira_soma": 10.0,          # graus
    "vira_espaco_s": 0.5,
    "aceno_amp": 5.0,           # graus por passada
    "aceno_min_passadas": 3,    # passadas seguidas (desce-sobe-desce)
    "aceno_domina": 1.5,        # o pitch anda pelo menos 1,5x o que o yaw anda no trecho
    "aceno_meia_min_s": 0.1,
    "aceno_meia_max_s": 0.5,
    "aceno_media_s": 0.8,
}
FILTRO_PONTO = (1.2, 0.5)       # One Euro: min_cutoff (Hz), beta, em unidades da distância entre os olhos
FILTRO_POSE = (1.0, 0.3)        # na pose, em unidades de 20°

# os pontos do Face Landmarker (478: 468 da malha + 10 da íris). "e" e "d" são de quem assiste; num vídeo
# que não é espelhado, o olho da esquerda na tela é o direito da pessoa (33, 133, 468).
P_OLHO_TELA_E = {"ext": 33, "int": 133, "sup": 159, "inf": 145, "iris": 468}
P_OLHO_TELA_D = {"ext": 263, "int": 362, "sup": 386, "inf": 374, "iris": 473}
PONTOS = ["olho_e", "olho_d", "canto_e_ext", "canto_e_int", "canto_d_int", "canto_d_ext", "boca", "boca_e",
          "boca_d", "labio_sup", "labio_inf", "nariz", "testa", "queixo", "sobrancelha_e", "sobrancelha_d"]

OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148,
        176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
OLHO_P_DIR = [33, 163, 145, 154, 133, 157, 159, 161]      # o olho direito da pessoa (contorno, 8)
OLHO_P_ESQ = [263, 390, 374, 381, 362, 384, 386, 388]     # o esquerdo
SOBR_P_DIR = [70, 63, 105, 66, 107]
SOBR_P_ESQ = [300, 293, 334, 296, 336]
LABIOS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]
NARIZ = [168, 6, 197, 1, 98, 327]
MIOLO = [50, 280, 205, 425, 117, 346, 187, 411, 101, 330, 36, 266, 151, 9, 108, 337, 175, 199, 18, 214, 434,
         207, 427]
MALHA = OVAL[::2] + OLHO_P_DIR + OLHO_P_ESQ + SOBR_P_DIR + SOBR_P_ESQ + LABIOS[::2] + NARIZ + MIOLO

TIPOS = ("piscada", "piscada-dupla", "boca-aberta", "sorriso", "sobrancelha", "cabeca-vira", "aceno")

SONDA = r"""
import sys
import types
sys.modules.setdefault("sounddevice", types.ModuleType("sounddevice"))
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
modelo, caminho = sys.argv[1], sys.argv[2]
deleg = BaseOptions.Delegate.GPU if caminho == "metal" else BaseOptions.Delegate.CPU
t = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=modelo, delegate=deleg), running_mode=vision.RunningMode.VIDEO,
    num_faces=1, output_face_blendshapes=True, output_facial_transformation_matrixes=True))
t.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGBA, data=np.zeros((96, 96, 4), np.uint8)), 0)
t.close()
print("ok")
"""


def fala(msg):
    print(msg, flush=True)


def aviso(msg):
    print("  aviso: " + msg, flush=True)


def erro(msg, codigo=2):
    print("erro: " + msg, file=sys.stderr, flush=True)
    sys.exit(codigo)


def ler(caminho):
    try:
        return json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def sem_audio():
    """O import do MediaPipe carrega o sounddevice, que abre o CoreAudio no import (com o coreaudiod
    ocupado, ~60 s por import). Um sounddevice vazio no lugar evita isso: a expressão não grava áudio."""
    sys.modules.setdefault("sounddevice", types.ModuleType("sounddevice"))


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


def escolher_caminho(modelo):
    """O caminho do MediaPipe que roda nesta máquina, testado num processo separado (se o C++ abortar,
    morre o teste). No Mac, só o Metal; fora dele, a CPU. Devolve (caminho, falhas)."""
    candidatos = ["metal", "cpu"] if sys.platform == "darwin" else ["cpu"]
    falhas = []
    for nome in candidatos:
        try:
            proc = subprocess.run([sys.executable, "-c", SONDA, str(modelo), nome], capture_output=True,
                                  text=True, errors="replace", timeout=180)
        except subprocess.TimeoutExpired:
            falhas.append(f"{nome}: o teste passou de 3 minutos")
            continue
        if proc.returncode == 0 and "ok" in proc.stdout:
            return nome, falhas
        linhas = [l.strip() for l in proc.stderr.splitlines() if l.strip()][-2:]
        falhas.append(f"{nome}: " + " / ".join(linhas))
    return None, falhas


# ------------------------------------------------------------------ vídeo e trechos
def sondar_video(caminho):
    proc = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-print_format", "json",
                           "-show_streams", "-show_format", str(caminho)], capture_output=True, text=True,
                          errors="replace")
    if proc.returncode != 0:
        erro(f"o ffprobe não conseguiu ler {caminho}: {proc.stderr.strip()[-300:]}")
    dados = json.loads(proc.stdout or "{}")
    v = (dados.get("streams") or [{}])[0]
    w, h = int(v.get("width") or 0), int(v.get("height") or 0)
    for lado in v.get("side_data_list") or []:
        if "rotation" in lado and abs(int(round(float(lado["rotation"])))) % 180 == 90:
            w, h = h, w
    if w <= 0 or h <= 0:
        erro(f"não consegui ler o tamanho do quadro de {caminho}")
    return w, h, float((dados.get("format") or {}).get("duration") or v.get("duration") or 0)


def par(n):
    return max(2, int(round(n / 2.0)) * 2)


def quadros_do_video(video, fps, tamanho, fonte):
    """Os quadros na grade do compor.py (-vf fps=N), no tamanho da análise, em RGB."""
    w, h = tamanho
    filtros = [f"fps={fps}"]
    if (w, h) != tuple(fonte):
        filtros.append(f"scale={w}:{h}:flags=area")
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-nostdin", "-i", str(video), "-map", "0:v:0", "-vf",
                             ",".join(filtros), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = w * h * 3
    try:
        while True:
            bruto = proc.stdout.read(n)
            if len(bruto) < n:
                break
            yield np.frombuffer(bruto, np.uint8).reshape(h, w, 3)
    finally:
        if proc.poll() is None:
            proc.kill()
        proc.stdout.close()
        proc.wait()


def ler_segmentos(pasta, total, fps, duracao):
    """Os trechos entre as emendas do edicao.json, em índices de quadro [a, b) (o mesmo do visao.py)."""
    emendas = []
    dados = ler(pasta / "edicao.json")
    if dados:
        dur = dados.get("duracao")
        if isinstance(dur, (int, float)) and duracao and abs(float(dur) - duracao) > 0.25:
            aviso(f"o edicao.json diz {dur:.2f} s e o vídeo tem {duracao:.2f} s; ignorei as emendas dele.")
        else:
            emendas = sorted({int(round(float(t) * fps)) for t in dados.get("emendas") or []
                              if isinstance(t, (int, float))})
    limites = [0] + [k for k in emendas if 0 < k < total] + [total]
    return [(a, b) for a, b in zip(limites[:-1], limites[1:]) if b > a]


# ------------------------------------------------------------------ análise
def analisar(video, fps, analise, fonte, modelo, caminho, inicios, total_esperado):
    """A passada pelo vídeo: por quadro, os 478 pontos (pixels da fonte), os 52 blendshapes e a matriz."""
    sem_audio()
    import cv2
    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.core.base_options import BaseOptions

    sw, sh = fonte
    deleg = BaseOptions.Delegate.GPU if caminho == "metal" else BaseOptions.Delegate.CPU
    estado = {"t": None}

    def abrir():
        if estado["t"] is not None:
            estado["t"].close()
        estado["t"] = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(modelo), delegate=deleg),
            running_mode=vision.RunningMode.VIDEO, num_faces=1, output_face_blendshapes=True,
            output_facial_transformation_matrixes=True))

    LM, BS, MT = [], [], []
    nomes = None
    relogio = ultimo = time.time()
    i = renovado = 0
    with calar_stderr():
        abrir()
        for quadro in quadros_do_video(video, fps, analise, fonte):
            if i > 0 and (i in inicios or i - renovado >= RENOVAR):
                abrir()
                renovado = i
            img = mp.Image(image_format=mp.ImageFormat.SRGBA, data=cv2.cvtColor(quadro, cv2.COLOR_RGB2RGBA))
            r = estado["t"].detect_for_video(img, int(round(i * 1000.0 / fps)))
            if r.face_landmarks:
                LM.append([[p.x * sw, p.y * sh] for p in r.face_landmarks[0]])
                BS.append([c.score for c in r.face_blendshapes[0]] if r.face_blendshapes else [np.nan] * 52)
                nomes = nomes or ([c.category_name for c in r.face_blendshapes[0]] if r.face_blendshapes else None)
                MT.append(np.array(r.facial_transformation_matrixes[0], float) if r.facial_transformation_matrixes
                          else np.full((4, 4), np.nan))
            else:
                LM.append(np.full((478, 2), np.nan))
                BS.append([np.nan] * 52)
                MT.append(np.full((4, 4), np.nan))
            i += 1
            agora = time.time()
            if agora - ultimo > 10:
                print(f"    analisados {i}/{total_esperado} quadros · {(agora - relogio) / i * 1000:.0f} ms por quadro",
                      file=sys.__stdout__, flush=True)
                ultimo = agora
        if estado["t"] is not None:
            estado["t"].close()
    return {"lm": np.array(LM, float).reshape(-1, 478, 2), "bs": np.array(BS, float).reshape(-1, 52),
            "mt": np.array(MT, float).reshape(-1, 4, 4), "nomes": nomes, "total": i, "tempo": time.time() - relogio}


# ------------------------------------------------------------------ filtros
def one_euro(x, fps, min_cutoff, beta, d_cutoff=1.0):
    n = len(x)
    out = np.empty_like(x)
    te = 1.0 / fps
    tau_d = 1.0 / (2 * math.pi * d_cutoff)
    ad = 1.0 / (1.0 + tau_d / te)
    xp = x[0].copy()
    dxp = np.zeros_like(x[0])
    out[0] = xp
    for i in range(1, n):
        dx = (x[i] - xp) / te
        dxh = dxp + ad * (dx - dxp)
        fc = min_cutoff + beta * np.abs(dxh)
        a = 1.0 / (1.0 + (1.0 / (2 * math.pi * fc)) / te)
        xh = xp + a * (x[i] - xp)
        out[i] = xh
        xp, dxp = xh, dxh
    return out


def zero_fase(x, fps, min_cutoff, beta):
    """One Euro para a frente e para trás, a média das duas: não atrasa o movimento."""
    if len(x) < 3:
        return x.copy()
    return (one_euro(x, fps, min_cutoff, beta) + one_euro(x[::-1], fps, min_cutoff, beta)[::-1]) / 2


def binomio(x):
    """1-2-1 ida e volta dentro do trecho (as pontas repetem o vizinho)."""
    if len(x) < 3:
        return x.copy()
    p = np.concatenate([x[:1], x, x[-1:]])
    return (p[:-2] + 2 * p[1:-1] + p[2:]) / 4


def media_movel(x, r):
    if len(x) == 0:
        return x.copy()
    p = np.pad(x, r, mode="edge")
    c = np.cumsum(np.concatenate([[0.0], p]))
    return (c[2 * r + 1:] - c[:-(2 * r + 1)]) / (2 * r + 1)


def mediana_movel(x, r):
    if len(x) == 0:
        return x.copy()
    from numpy.lib.stride_tricks import sliding_window_view
    p = np.pad(x, r, mode="edge")
    return np.median(sliding_window_view(p, 2 * r + 1), axis=1)


def corridas(mask):
    out, a = [], None
    for i, v in enumerate(mask):
        if v and a is None:
            a = i
        elif not v and a is not None:
            out.append((a, i))
            a = None
    if a is not None:
        out.append((a, len(mask)))
    return out


# ------------------------------------------------------------------ montagem dos sinais
def preencher(pres, arrays, segs):
    """Falha de até BURACO quadros no meio de um trecho: linha reta entre as pontas. Devolve a máscara do
    que foi preenchido."""
    preench = np.zeros(len(pres), bool)
    for a, b in segs:
        for x0, x1 in corridas(~pres[a:b]):
            g0, g1 = a + x0, a + x1
            if g0 == a or g1 == b or g1 - g0 > BURACO:
                continue
            for arr in arrays:
                for k in range(g0, g1):
                    u = (k - g0 + 1) / (g1 - g0 + 1)
                    arr[k] = arr[g0 - 1] * (1 - u) + arr[g1] * u
            preench[g0:g1] = True
    return preench


def presenca(pres, segs):
    """A presença "a": 0 sem rosto; sobe em FADE quadros depois que ele aparece e desce em FADE antes de
    ele sumir (offline, sem atraso); corta seco na emenda."""
    a = np.zeros(len(pres))
    for s0, s1 in segs:
        for x0, x1 in corridas(pres[s0:s1]):
            g0, g1 = s0 + x0, s0 + x1
            for k in range(g0, g1):
                sobe = 1.0 if g0 == s0 else min(1.0, (k - g0 + 1) / FADE)
                desce = 1.0 if g1 == s1 else min(1.0, (g1 - k) / FADE)
                a[k] = min(sobe, desce)
    return a


def pose_da_matriz(mt):
    """yaw, pitch, roll em graus, no sentido da tela (conferido contra o nariz e a linha dos olhos)."""
    R = mt[:, :3, :3]
    yaw = np.degrees(np.arctan2(R[:, 0, 2], R[:, 2, 2]))
    pitch = -np.degrees(np.arcsin(np.clip(-R[:, 1, 2], -1, 1)))
    roll = -np.degrees(np.arctan2(R[:, 1, 0], R[:, 0, 0]))
    return np.stack([yaw, pitch, roll], axis=1)


def ear(lm, o):
    """Abertura do olho: pálpebra de cima à de baixo sobre canto a canto."""
    v = np.linalg.norm(lm[:, o["sup"]] - lm[:, o["inf"]], axis=1)
    hz = np.linalg.norm(lm[:, o["ext"]] - lm[:, o["int"]], axis=1)
    return v / np.maximum(hz, 1e-6)


def canais(bs, nomes):
    """Os blendshapes resumidos, no lado de quem assiste. O "Left" do MediaPipe é o lado da pessoa (o
    olho da direita na tela): conferido pela íris e pelas pálpebras nos três cortes de teste."""
    B = lambda n: bs[:, nomes.index(n)]
    olhar_x = ((B("eyeLookOutLeft") - B("eyeLookInLeft")) - (B("eyeLookOutRight") - B("eyeLookInRight"))) / 2
    olhar_y = ((B("eyeLookDownLeft") + B("eyeLookDownRight")) - (B("eyeLookUpLeft") + B("eyeLookUpRight"))) / 2
    return {
        "piscar_e": B("eyeBlinkRight"), "piscar_d": B("eyeBlinkLeft"),
        "boca": B("jawOpen"),
        "sorriso": (B("mouthSmileLeft") + B("mouthSmileRight")) / 2,
        "sobrancelha": np.maximum(B("browInnerUp"), (B("browOuterUpLeft") + B("browOuterUpRight")) / 2),
        "bochecha": B("cheekPuff"),
        "beicinho": B("mouthPucker"),
        "arregalado": (B("eyeWideLeft") + B("eyeWideRight")) / 2,
        "olhar_x": olhar_x, "olhar_y": olhar_y,
    }


def pontos_uteis(lm, espelhado):
    """Os 16 pontos de PONTOS, de quem assiste (num vídeo espelhado os lados trocam)."""
    oe, od = (P_OLHO_TELA_D, P_OLHO_TELA_E) if espelhado else (P_OLHO_TELA_E, P_OLHO_TELA_D)
    be, bd = (291, 61) if espelhado else (61, 291)
    se, sd = (105, 334) if not espelhado else (334, 105)
    meio_boca = (lm[:, 13] + lm[:, 14]) / 2
    return np.stack([lm[:, oe["iris"]], lm[:, od["iris"]], lm[:, oe["ext"]], lm[:, oe["int"]], lm[:, od["int"]],
                     lm[:, od["ext"]], meio_boca, lm[:, be], lm[:, bd], lm[:, 13], lm[:, 14], lm[:, 1], lm[:, 10],
                     lm[:, 152], lm[:, se], lm[:, sd]], axis=1)


def arestas_da_malha(lm, pres):
    """A triangulação de Delaunay da malha no rosto médio (normalizado pelos olhos), sem as arestas que
    atravessam os olhos ou a boca e sem as compridas demais. Feita uma vez por vídeo."""
    import cv2
    idx = np.where(pres)[0]
    if len(idx) == 0:
        return []
    amostra = lm[idx[:: max(1, len(idx) // 200)]]
    centro = (amostra[:, 33] + amostra[:, 263]) / 2
    io = np.linalg.norm(amostra[:, 33] - amostra[:, 263], axis=1)[:, None]
    norm = (amostra[:, MALHA] - centro[:, None]) / io[:, None]
    media = np.median(norm, axis=0)
    caixa = (float(media[:, 0].min()) - 1, float(media[:, 1].min()) - 1,
             float(media[:, 0].max() - media[:, 0].min()) + 2, float(media[:, 1].max() - media[:, 1].min()) + 2)
    escala = 1000.0
    sub = cv2.Subdiv2D((int(caixa[0] * escala), int(caixa[1] * escala), int(caixa[2] * escala) + 1,
                        int(caixa[3] * escala) + 1))
    pos = {}
    for i, (x, y) in enumerate(media):
        pos[(round(float(x) * escala, 3), round(float(y) * escala, 3))] = i
        sub.insert((float(x) * escala, float(y) * escala))
    arestas = set()

    def achar(x, y):
        melhor, d = None, 1e18
        for (px, py), i in pos.items():
            dd = (px - x) ** 2 + (py - y) ** 2
            if dd < d:
                melhor, d = i, dd
        return melhor if d < 1.0 else None

    for t in sub.getTriangleList():
        vs = [achar(t[0], t[1]), achar(t[2], t[3]), achar(t[4], t[5])]
        if None in vs:
            continue
        for a, b in ((0, 1), (1, 2), (2, 0)):
            i, j = sorted((vs[a], vs[b]))
            if i != j:
                arestas.add((i, j))
    poli = lambda ids: np.array([media[MALHA.index(k)] for k in ids], np.float32)
    olhos = [poli(OLHO_P_DIR), poli(OLHO_P_ESQ)]
    boca = poli(LABIOS[::2])
    fora = []
    for i, j in sorted(arestas):
        m = ((media[i] + media[j]) / 2).astype(np.float32)
        comp = float(np.linalg.norm(media[i] - media[j]))
        if comp > 0.95:
            continue
        if any(cv2.pointPolygonTest(p, (float(m[0]), float(m[1])), False) > 0 for p in olhos + [boca]):
            continue
        fora.append([int(i), int(j)])
    return fora


# ------------------------------------------------------------------ eventos
def picos(x, a, b, limiar, prom, janela, espaco):
    """Máximos locais de x em [a, b) acima de `limiar` e `prom` acima do menor valor de ±janela; dois a
    menos de `espaco` quadros: fica o maior."""
    out = []
    for k in range(a + 1, b - 1):
        if not (x[k] >= limiar and x[k] >= x[k - 1] and x[k] > x[k + 1]):
            continue
        lo = min(np.nanmin(x[max(a, k - janela):k + 1]), np.nanmin(x[k:min(b, k + janela + 1)]))
        if x[k] - lo >= prom:
            out.append(k)
    out.sort(key=lambda k: -x[k])
    fica = []
    for k in out:
        if all(abs(k - j) >= espaco for j in fica):
            fica.append(k)
    return sorted(fica)


def limites_do_pico(x, k, a, b, nivel):
    """Do pico para os lados até x cair abaixo de nivel: (de, ate) em quadros."""
    i = k
    while i > a and x[i - 1] >= nivel:
        i -= 1
    j = k
    while j < b - 1 and x[j + 1] >= nivel:
        j += 1
    return i, j


def eventos_de(S, segs, fps, pres):
    """Todos os eventos, trecho a trecho. S tem os sinais (quase crus) por quadro."""
    ev = []

    def add(tipo, k, xy, **kw):
        e = {"tipo": tipo, "quadro": int(k), "t": round(k / fps, 3),
             "x": round(float(xy[0]), 1), "y": round(float(xy[1]), 1)}
        e.update(kw)
        ev.append(e)

    olhos_meio = (S["P"][:, 0] + S["P"][:, 1]) / 2
    for a, b in segs:
        if b - a < 4:
            continue
        ok = pres[a:b]
        # ---------------- piscada
        r2 = int(fps)
        en_e = S["ear_e"][a:b] / np.maximum(mediana_movel(S["ear_e"][a:b], r2), 1e-6)
        en_d = S["ear_d"][a:b] / np.maximum(mediana_movel(S["ear_d"][a:b], r2), 1e-6)
        en = (en_e + en_d) / 2
        bsm = (S["piscar_e"][a:b] + S["piscar_d"][a:b]) / 2
        cand = (np.minimum(en_e, en_d) < L["piscada_ear_corrida"]) & ok
        pisc = []
        for x0, x1 in corridas(cand):
            if x1 - x0 > L["piscada_max"]:
                continue
            k = x0 + int(np.argmin(np.minimum(en_e[x0:x1], en_d[x0:x1])))
            ambos = en[k] < L["piscada_ear"] and bsm[k] >= L["piscada_bs"]
            olho = "ambos"
            if not ambos:
                # a piscadela: um olho fecha de verdade, o outro fica aberto
                if en_e[k] < L["piscada_ear"] * 0.8 and en_d[k] > L["piscadela_aberto"] and S["piscar_e"][a + k] >= L["piscada_bs"]:
                    olho = "esquerda"
                elif en_d[k] < L["piscada_ear"] * 0.8 and en_e[k] > L["piscadela_aberto"] and S["piscar_d"][a + k] >= L["piscada_bs"]:
                    olho = "direita"
                else:
                    continue
            pisc.append((a + x0, a + k, a + x1, olho, float(en[k])))
        for i, (g0, k, g1, olho, fundo) in enumerate(pisc):
            dupla = (i > 0 and (g0 - pisc[i - 1][0]) / fps <= L["dupla_s"]) or \
                    (i + 1 < len(pisc) and (pisc[i + 1][0] - g0) / fps <= L["dupla_s"])
            xy = olhos_meio[k] if olho == "ambos" else S["P"][k, 0 if olho == "esquerda" else 1]
            add("piscada", k, xy, olho=olho, dupla=bool(dupla), de=round(g0 / fps, 3), ate=round(g1 / fps, 3),
                fundo=round(fundo, 2))
            if i + 1 < len(pisc) and (pisc[i + 1][0] - g0) / fps <= L["dupla_s"] and \
                    not (i > 0 and (g0 - pisc[i - 1][0]) / fps <= L["dupla_s"]):
                add("piscada-dupla", k, xy, ate=round(pisc[i + 1][2] / fps, 3))
        # ---------------- boca aberta
        bo = S["boca"]
        for k in picos(bo, a, b, L["boca_pico"], L["boca_prom"], int(L["boca_janela_s"] * fps),
                       int(L["boca_espaco_s"] * fps)):
            i, j = limites_do_pico(bo, k, a, b, L["boca_sustenta"])
            if j - i + 1 < L["boca_min_q"] or not pres[k]:
                continue
            add("boca-aberta", k, S["P"][k, 6], pico=round(float(bo[k]), 3), de=round(i / fps, 3),
                ate=round((j + 1) / fps, 3))
        # ---------------- sorriso
        so = S["sorriso"]
        k = a
        ultimo = -10 ** 9
        while k < b:
            if so[k] >= L["sorriso_entra"] and pres[k]:
                j = k
                while j < b and so[j] >= L["sorriso_fica"]:
                    j += 1
                ini = k
                while ini > a and so[ini - 1] >= L["sorriso_fica"]:
                    ini -= 1
                antes = so[max(a, ini - int(L["sorriso_antes_s"] * fps)):ini]
                nivel = float(np.percentile(antes, 30)) if len(antes) >= 6 else 0.0
                if j - ini >= L["sorriso_min_q"] and float(so[ini:j].max()) - nivel >= L["sorriso_sobe"] and \
                        ini - ultimo > fps:
                    # o instante da subida: onde o sorriso cruza a metade entre o nível e o pico
                    meio = nivel + (float(so[ini:j].max()) - nivel) / 2
                    s0 = max(a, ini - 6)
                    kk = next((q for q in range(s0, j) if so[q] >= meio), ini)
                    add("sorriso", kk, S["P"][kk, 6], pico=round(float(so[ini:j].max()), 3),
                        ate=round(j / fps, 3))
                    ultimo = j
                k = j + 1
            else:
                k += 1
        # ---------------- sobrancelha
        sb = S["sobrancelha"]
        for k in picos(sb, a, b, L["sobrancelha_pico"], L["sobrancelha_prom"], int(L["sobrancelha_janela_s"] * fps),
                       int(L["sobrancelha_espaco_s"] * fps)):
            # a piscada puxa o blendshape da sobrancelha junto (o rosto muda em volta do olho): o pico
            # dentro de uma piscada, ou com o olho meio fechado, não é surpresa
            if not pres[k] or bsm[k - a] > L["sobrancelha_olho_max"] or \
                    any(g0 - 3 <= k <= g1 + 3 for g0, _, g1, _, _ in pisc):
                continue
            i, j = limites_do_pico(sb, k, a, b, sb[k] * 0.5)
            meio = (S["P"][k, 14] + S["P"][k, 15]) / 2
            add("sobrancelha", k, meio, pico=round(float(sb[k]), 3), de=round(i / fps, 3), ate=round((j + 1) / fps, 3))
        # ---------------- cabeça vira (yaw)
        yaw = S["pose"][a:b, 0]
        if b - a >= 4:
            vel = np.gradient(yaw) * fps
            ultimo = -10 ** 9
            for sinal in (1, -1):
                for x0, x1 in corridas((sinal * vel > L["vira_vel"]) & ok):
                    if x1 - x0 < L["vira_min_q"]:
                        continue
                    soma = abs(yaw[min(x1, b - a - 1)] - yaw[max(0, x0 - 1)])
                    if soma < L["vira_soma"]:
                        continue
                    k = x0 + int(np.argmax(sinal * vel[x0:x1]))
                    add("cabeca-vira", a + k, S["P"][a + k, 11], sentido=sinal, vel=round(float(abs(vel[k])), 1),
                        de=round(float(yaw[max(0, x0 - 1)]), 1), ate=round(float(yaw[min(x1, b - a - 1)]), 1))
        # ---------------- aceno (pitch oscilando)
        pt = S["pose"][a:b, 1]
        if b - a >= 8:
            dt = pt - media_movel(pt, int(L["aceno_media_s"] * fps / 2))
            ext = []
            for k in range(1, len(dt) - 1):
                if dt[k] >= dt[k - 1] and dt[k] > dt[k + 1]:
                    ext.append((k, 1))
                elif dt[k] <= dt[k - 1] and dt[k] < dt[k + 1]:
                    ext.append((k, -1))
            # junta extremos do mesmo tipo (fica o mais forte) e corre atrás de sequências alternadas
            alt = []
            for k, tipo in ext:
                if alt and alt[-1][1] == tipo:
                    if tipo * dt[k] > tipo * dt[alt[-1][0]]:
                        alt[-1] = (k, tipo)
                    continue
                alt.append((k, tipo))
            seq = []

            def fechar(seq):
                if len(seq) >= L["aceno_min_passadas"] + 1:
                    k0, k9 = seq[0][0], seq[-1][0]
                    dp = float(np.abs(np.diff(pt[k0:k9 + 1])).sum())
                    dy = float(np.abs(np.diff(yaw[k0:k9 + 1])).sum())
                    if dp < L["aceno_domina"] * dy:
                        return
                    amp = max(abs(pt[seq[i + 1][0]] - pt[seq[i][0]]) for i in range(len(seq) - 1))
                    add("aceno", a + k0, S["P"][a + k0, 11], n=len(seq) - 1, amplitude=round(float(amp), 1),
                        ate=round((a + seq[-1][0]) / fps, 3))

            for i in range(len(alt)):
                if not seq:
                    seq = [alt[i]]
                    continue
                k0, k1 = seq[-1][0], alt[i][0]
                passo = abs(pt[k1] - pt[k0])
                meia = (k1 - k0) / fps
                if passo >= L["aceno_amp"] and L["aceno_meia_min_s"] <= meia <= L["aceno_meia_max_s"] and ok[k1]:
                    seq.append(alt[i])
                else:
                    fechar(seq)
                    seq = [alt[i]]
            fechar(seq)
    # cabeca-vira: 0,5 s entre dois
    ev.sort(key=lambda e: (e["t"], e["tipo"]))
    fica, ult = [], {}
    for e in ev:
        if e["tipo"] == "cabeca-vira" and e["t"] - ult.get("cabeca-vira", -9) < L["vira_espaco_s"]:
            continue
        ult[e["tipo"]] = e["t"]
        fica.append(e)
    return fica


# ------------------------------------------------------------------ resumo e folha
def palavras_perto(palavras, t, raio=0.5):
    return " ".join(p["texto"] for p in palavras if p["inicio"] <= t + raio and p["fim"] >= t - raio)


def imprimir_resumo(X, palavras):
    fps = X["fps"]
    T = X["total"]
    q = [x for x in X["quadros"] if x]
    fala("")
    fala(f"expressão · {X['fonte']} · {T} quadros ({T / fps:.1f} s) · rosto em {100 * len(q) / max(1, T):.0f}% dos quadros")
    if q:
        for c in ("boca", "sorriso", "sobrancelha", "beicinho"):
            v = np.array([x[c] for x in q])
            fala(f"  {c:<12} mediana {np.median(v):.2f} · p90 {np.percentile(v, 90):.2f} · máx {v.max():.2f}")
        pose = np.array([x["pose"] for x in q])
        fala(f"  pose         yaw {pose[:, 0].min():+.0f}° a {pose[:, 0].max():+.0f}° · pitch {pose[:, 1].min():+.0f}° a "
             f"{pose[:, 1].max():+.0f}° · roll {pose[:, 2].min():+.0f}° a {pose[:, 2].max():+.0f}°")
    fala("")
    fala("eventos (gatilhos):")
    por = {}
    for e in X["eventos"]:
        por.setdefault(e["tipo"], []).append(e)
    for tipo in TIPOS:
        es = por.get(tipo, [])
        fala(f"  {tipo} ({len(es)})")
        for e in es:
            extra = ""
            if tipo == "piscada":
                extra = f" {e['olho']}{' dupla' if e['dupla'] else ''} fundo {e['fundo']:.2f}"
            elif tipo in ("boca-aberta", "sorriso", "sobrancelha"):
                extra = f" pico {e['pico']:.2f} até {e['ate']:.2f}s"
            elif tipo == "cabeca-vira":
                extra = f" {'→' if e['sentido'] > 0 else '←'} {e['de']:+.0f}° → {e['ate']:+.0f}° ({e['vel']:.0f}°/s)"
            elif tipo == "aceno":
                extra = f" {e['n']} meias · {e['amplitude']:.0f}° até {e['ate']:.2f}s"
            elif tipo == "piscada-dupla":
                extra = f" até {e['ate']:.2f}s"
            fala(f"    {e['t']:6.2f}s{extra} · \"{palavras_perto(palavras, e['t'])}\"")


def folha(X, saida, video):
    """Um quadro por evento com os pontos, a malha e o evento escritos: para conferir no olho."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        from io import BytesIO
    except ImportError:
        aviso("sem Pillow, sem folha")
        return
    fps = X["fps"]
    ks = []
    for e in X["eventos"]:
        if e["tipo"] == "piscada-dupla":
            continue
        rot = e["tipo"] + (f" {e['olho']}" if e["tipo"] == "piscada" and e["olho"] != "ambos" else "") + \
            (" ×2" if e.get("dupla") else "")
        if ks and e["quadro"] == ks[-1][0]:
            ks[-1] = (ks[-1][0], ks[-1][1] + " + " + rot)
            continue
        ks.append((e["quadro"], rot))
    ks = ks[:64]
    if not ks:
        return
    W, H = X["largura"], X["altura"]
    tw, th = 240, 300
    cols = 8
    rows = (len(ks) + cols - 1) // cols
    img = Image.new("RGB", (cols * tw, rows * th), (13, 10, 12))
    try:
        fonte = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    except OSError:
        fonte = ImageFont.load_default()
    arestas = X["malha"]["arestas"]
    for n, (k, rot) in enumerate(ks):
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{k / fps:.4f}", "-i", str(video), "-frames:v", "1",
                            "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        try:
            q = Image.open(BytesIO(r.stdout)).convert("RGB").resize((W, H))
        except Exception:
            q = Image.new("RGB", (W, H), (40, 40, 40))
        x = X["quadros"][k]
        if x:
            d = ImageDraw.Draw(q)
            m = x["malha"]
            pts = [(m[2 * i], m[2 * i + 1]) for i in range(len(m) // 2)]
            for i, j in arestas:
                d.line([pts[i], pts[j]], fill=(0, 153, 255), width=1)
            P = x["p"]
            io = max(8.0, x["io"])
            for i, c in ((0, (255, 0, 94)), (1, (255, 0, 94)), (6, (255, 255, 255)), (11, (247, 167, 17))):
                d.ellipse([P[i][0] - io * 0.06, P[i][1] - io * 0.06, P[i][0] + io * 0.06, P[i][1] + io * 0.06],
                          outline=c, width=2)
            # o olhar e a pose: uma seta a partir do nariz
            yaw, pitch = math.radians(x["pose"][0]), math.radians(x["pose"][1])
            nx, ny = P[11]
            d.line([(nx, ny), (nx + math.sin(yaw) * io * 1.5, ny - math.sin(pitch) * io * 1.5)], fill=(247, 167, 17), width=3)
            # recorte em volta do rosto
            cx, cy = (P[12][0] + P[13][0]) / 2, (P[12][1] + P[13][1]) / 2
            lh = abs(P[13][1] - P[12][1]) * 1.45
            lw = lh * tw / th
            q = q.crop((int(cx - lw / 2), int(cy - lh / 2), int(cx + lw / 2), int(cy + lh / 2)))
        q = q.resize((tw, th))
        dd = ImageDraw.Draw(q)
        dd.rectangle([0, 0, tw, 50], fill=(0, 0, 0))
        dd.text((4, 2), f"{k / fps:.2f}s q{k}", fill=(255, 255, 255), font=fonte)
        dd.text((4, 17), rot[:30], fill=(255, 0, 94), font=fonte)
        if x:
            dd.text((4, 32), f"b{x['boca']:.2f} s{x['sorriso']:.2f} br{x['sobrancelha']:.2f} p{(x['piscar'][0] + x['piscar'][1]) / 2:.2f}",
                    fill=(200, 200, 200), font=fonte)
        img.paste(q, ((n % cols) * tw, (n // cols) * th))
    img.save(saida, quality=88)
    fala(f"  folha: {saida}")


# ------------------------------------------------------------------ principal
def caminhos(projeto, corte):
    proj = Path(projeto)
    if not proj.is_absolute():
        proj = (Path.cwd() / proj).resolve()
    nn = f"{int(corte):02d}" if str(corte).isdigit() else str(corte)
    return proj, nn, proj / "materiais-de-trabalho" / f"corte-{nn}"


def achar_raiz():
    return fabrica.raiz()


def r1(x):
    return round(float(x), 1)


def r3(x):
    return round(float(x), 3)


def main():
    ap = argparse.ArgumentParser(description="o rosto quadro a quadro (expressão, pose, pontos) e os eventos")
    ap.add_argument("--projeto", required=True)
    ap.add_argument("--corte", required=True)
    ap.add_argument("--resumo", action="store_true", help="só imprime os momentos (lê o expressao.json; refaz se faltar)")
    ap.add_argument("--folha", nargs="?", const="", default=None,
                    help="grava a folha de contato (padrão: folha-expressao.jpg na pasta do corte)")
    ap.add_argument("--saida", help="expressao.json alternativo")
    args = ap.parse_args()

    proj, nn, pasta = caminhos(args.projeto, args.corte)
    if not pasta.is_dir():
        erro(f"não achei a pasta do corte: {pasta}")
    cenas = ler(pasta / "cenas.json") or {}
    fps = int(cenas.get("fps", 30) or 30)
    video = pasta / ((cenas.get("fonte") or {}).get("video") or "fala.mp4")
    if not video.is_file():
        erro(f"falta o vídeo do corte: {video}")
    vdir = pasta / "visao"
    vdir.mkdir(exist_ok=True)
    saida = Path(args.saida).resolve() if args.saida else vdir / "expressao.json"
    palavras = (ler(pasta / "palavras-corte.json") or {}).get("palavras") or []

    st = video.stat()
    origem = {"video": str(video.resolve()), "mtime": st.st_mtime, "tamanho": st.st_size, "fps": fps}
    ov = ler(vdir / ".origem.json")
    if ov and any(ov.get(k) != origem[k] for k in origem):
        aviso("a visão (visao/.origem.json) é de outro vídeo ou outra fps; o compor.py só entrega a expressão "
              "ao motor depois de rodar o visao.py de novo neste corte.")
    elif not ov:
        aviso("este corte ainda não tem a visão (visao.py); o compor.py só entrega a expressão ao motor com ela.")

    if args.resumo and saida.is_file() and args.folha is None:
        X = ler(saida)
        if X and X.get("versao") == VERSAO and all(X.get("origem", {}).get(k) == origem[k] for k in origem):
            imprimir_resumo(X, palavras)
            return 0

    raiz = achar_raiz()
    modelo = fabrica.achar("componentes/modelos/" + MODELOS["rosto"][0])
    if not modelo.is_file():
        erro(f"falta o modelo {modelo.name} em componentes/modelos/ (baixe de {MODELOS['rosto'][3]}; "
             "veja componentes/modelos/LEIA.md)")
    for prog in ("ffmpeg", "ffprobe"):
        if subprocess.run(["which", prog], capture_output=True).returncode != 0:
            erro(f"falta o {prog} no PATH")

    sw, sh, duracao = sondar_video(video)
    w, h = (sw, sh) if sh <= ALTURA_MAX else (par(sw * ALTURA_MAX / float(sh)), ALTURA_MAX)
    total_esperado = int(round(duracao * fps)) if duracao else 0
    fala(f"expressão · {video.name}: {sw}x{sh}, {duracao:.1f} s a {fps} fps; análise em {w}x{h}")
    caminho, falhas = escolher_caminho(modelo)
    if not caminho:
        erro("o Face Landmarker não abriu nesta máquina:\n  " + "\n  ".join(falhas))
    fala(f"  Face Landmarker no caminho {'Metal' if caminho == 'metal' else 'CPU'}")

    segs0 = ler_segmentos(pasta, total_esperado or 10 ** 6, fps, duracao)
    inicios = {a for a, _ in segs0 if a > 0}
    R = analisar(video, fps, (w, h), (sw, sh), modelo, caminho, inicios, total_esperado)
    T = R["total"]
    if T == 0 or not R["nomes"]:
        erro("o Face Landmarker não achou rosto nenhum no vídeo")
    segs = ler_segmentos(pasta, T, fps, duracao)
    fala(f"  {T} quadros em {R['tempo']:.1f} s ({R['tempo'] / T * 1000:.1f} ms por quadro), {len(segs)} trecho(s)")

    lm, bs, mt = R["lm"], R["bs"], R["mt"]
    pres_med = ~np.isnan(lm[:, 0, 0])
    # num vídeo espelhado o olho direito da pessoa (33) fica à direita na tela
    espelhado = bool(np.nanmedian(lm[pres_med, 33, 0]) > np.nanmedian(lm[pres_med, 263, 0])) if pres_med.any() else False
    if espelhado:
        aviso("o vídeo parece espelhado (o olho direito da pessoa está à direita na tela); os lados seguem a tela.")
    pose = np.where(pres_med[:, None], pose_da_matriz(np.nan_to_num(mt)), np.nan)
    C = canais(np.nan_to_num(bs), R["nomes"])
    for k in C:
        C[k] = np.where(pres_med, C[k], np.nan)
    if espelhado:
        C["piscar_e"], C["piscar_d"] = C["piscar_d"], C["piscar_e"]
        C["olhar_x"] = -C["olhar_x"]
        pose[:, 0] *= -1
        pose[:, 2] *= -1
    oe, od = (P_OLHO_TELA_D, P_OLHO_TELA_E) if espelhado else (P_OLHO_TELA_E, P_OLHO_TELA_D)
    ear_e = np.where(pres_med, ear(np.nan_to_num(lm), oe), np.nan)
    ear_d = np.where(pres_med, ear(np.nan_to_num(lm), od), np.nan)

    # preenche a falha curta
    arrays = [lm, pose, ear_e, ear_d] + [C[k] for k in C]
    preench = preencher(pres_med, arrays, segs)
    pres = pres_med | preench
    a_pres = presenca(pres, segs)

    # suavização zero-phase, trecho a trecho e corrida a corrida (só onde há rosto)
    io_bruto = np.linalg.norm(lm[:, 33] - lm[:, 263], axis=1)
    lm_s = lm.copy()
    pose_s = pose.copy()
    C_s = {k: v.copy() for k, v in C.items()}
    for a, b in segs:
        for x0, x1 in corridas(pres[a:b]):
            g0, g1 = a + x0, a + x1
            io = float(np.nanmedian(io_bruto[g0:g1])) or 1.0
            pedaco = lm[g0:g1].reshape(g1 - g0, -1) / io
            lm_s[g0:g1] = (zero_fase(pedaco, fps, *FILTRO_PONTO) * io).reshape(g1 - g0, 478, 2)
            pose_s[g0:g1] = zero_fase(pose[g0:g1] / 20.0, fps, *FILTRO_POSE) * 20.0
            for k in C_s:
                C_s[k][g0:g1] = binomio(C[k][g0:g1])
                if k in ("olhar_x", "olhar_y"):
                    C_s[k][g0:g1] = binomio(binomio(C_s[k][g0:g1]))

    P_s = pontos_uteis(lm_s, espelhado)
    io_s = np.linalg.norm(P_s[:, 2] - P_s[:, 5], axis=1)
    arestas = arestas_da_malha(lm_s, pres)

    # eventos: nos sinais quase crus (os blendshapes com o 1-2-1, a pose suavizada, a abertura crua)
    S = {"P": P_s, "ear_e": np.nan_to_num(ear_e, nan=1.0), "ear_d": np.nan_to_num(ear_d, nan=1.0),
         "piscar_e": np.nan_to_num(C["piscar_e"]), "piscar_d": np.nan_to_num(C["piscar_d"]),
         "boca": np.nan_to_num(C_s["boca"]), "sorriso": np.nan_to_num(C_s["sorriso"]),
         "sobrancelha": np.nan_to_num(C_s["sobrancelha"]), "pose": np.nan_to_num(pose_s)}
    eventos = eventos_de(S, segs, fps, pres)

    quadros = []
    for k in range(T):
        if not pres[k] or a_pres[k] <= 0:
            quadros.append(None)
            continue
        quadros.append({
            "a": r3(a_pres[k]),
            "m": bool(pres_med[k]),
            "piscar": [r3(np.clip(C_s["piscar_e"][k], 0, 1)), r3(np.clip(C_s["piscar_d"][k], 0, 1))],
            "boca": r3(np.clip(C_s["boca"][k], 0, 1)),
            "sorriso": r3(np.clip(C_s["sorriso"][k], 0, 1)),
            "sobrancelha": r3(np.clip(C_s["sobrancelha"][k], 0, 1)),
            "bochecha": r3(np.clip(C_s["bochecha"][k], 0, 1)),
            "beicinho": r3(np.clip(C_s["beicinho"][k], 0, 1)),
            "arregalado": r3(np.clip(C_s["arregalado"][k], 0, 1)),
            "olhar": [r3(C_s["olhar_x"][k]), r3(C_s["olhar_y"][k])],
            "pose": [r1(pose_s[k, 0]), r1(pose_s[k, 1]), r1(pose_s[k, 2])],
            "io": r1(io_s[k]),
            "p": [[r1(P_s[k, i, 0]), r1(P_s[k, i, 1])] for i in range(len(PONTOS))],
            "malha": [int(round(v)) for i in MALHA for v in lm_s[k, i]],
        })
    rel = {"medidos": int(pres_med.sum()), "preenchidos": int(preench.sum()), "espelhado": espelhado,
           "caminho": caminho, "ms_por_quadro": round(R["tempo"] / T * 1000, 1), "tempo_s": round(R["tempo"], 1),
           "eventos": {t: sum(1 for e in eventos if e["tipo"] == t) for t in TIPOS}}
    X = {
        "versao": VERSAO, "fonte": video.name, "fps": fps, "largura": sw, "altura": sh, "total": T,
        "segmentos": [list(s) for s in segs], "origem": origem,
        "modelo": MODELOS["rosto"][1], "licenca": MODELOS["rosto"][2],
        "lado": "de quem assiste: esquerda = o olho à esquerda na tela",
        "pose_sentido": "yaw > 0 vira para a direita da tela; pitch > 0 olha para cima; roll > 0 inclina no sentido horário",
        "pontos": PONTOS,
        "malha": {"indices": MALHA, "arestas": arestas,
                  "olhos": [[MALHA.index(i) for i in (OLHO_P_ESQ if espelhado else OLHO_P_DIR)],
                            [MALHA.index(i) for i in (OLHO_P_DIR if espelhado else OLHO_P_ESQ)]]},
        "limiares": L, "relatorio": rel, "quadros": quadros, "eventos": eventos,
    }
    saida.write_text(json.dumps(X, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    fala(f"expressao.json gravado: {saida} ({saida.stat().st_size / 1024:.0f} KB) · rosto em "
         f"{100 * pres.mean():.0f}% dos quadros ({int(preench.sum())} preenchidos) · {len(eventos)} eventos")
    imprimir_resumo(X, palavras)
    if args.folha is not None:
        folha(X, Path(args.folha).resolve() if args.folha else pasta / "folha-expressao.jpg", video)
    return 1 if pres.mean() < POUCO else 0


if __name__ == "__main__":
    sys.exit(main())
