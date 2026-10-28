#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rosto.py  ·  acha o rosto em cada quadro da fala e grava a caixa suavizada

Até o motor 2.0, o rosto entrava no corte por uma caixa fixa que o agente
decidia olhando a folha do enquadrar.py. Isso serve para busto em tripé, mas
quem gesticula e se inclina sai do centro, e a caixa fixa não acompanha. Agora
o compositor enquadra sozinho, quadro a quadro, e o gate de colisão precisa
saber onde o rosto está para reprovar texto em cima dele. Os dois leem o mesmo
arquivo, o rosto.json (motor/MOTOR.md, seção 2.3), e quem escreve é este script.

O caminho:

  ler        o ffmpeg entrega os quadros na fps do vídeo, já recortados na
             --regiao e reduzidos a no máximo 640 px no lado maior. O detector
             enxerga em 128 px; reduzir antes, com média de área, só tira
             serrilhado e tempo.

  achar      o BlazeFace do MediaPipe (Apache-2.0, roda no próprio computador)
             devolve os rostos de cada quadro. O principal é o de maior
             confiança x área, com preferência para o que está perto do rosto
             dos quadros anteriores: mão gesticulando, estampa de camiseta ou
             rosto num quadro na parede não roubam a câmera.

  suavizar   como um cinegrafista, não como um detector. O centro tem zona
             morta de 3% do quadro, medida em cada eixo da janela vertical 9:16
             que cabe nele, que é o quadro que o reel mostra (numa fonte
             horizontal, 3% da largura inteira deixaria o rosto passear um
             décimo da tela). Enquanto o rosto balança dentro dela, a caixa não
             se mexe; quando ele sai e fica fora por 0,4 s, a caixa vai atrás
             (aceno de cabeça que volta logo não arrasta a câmera), e quando
             ele para de novo por meio segundo, ela se recentra nele. O seguimento
             tem constante de tempo de 0,4 s. O tamanho anda bem mais devagar,
             1 s, com zona morta própria de 6%, porque zoom que respira é o
             defeito mais visível de enquadramento automático. A suavização
             roda para frente e para trás, então a caixa não chega atrasada:
             ela anda junto com o rosto.

  emendas    o fala.mp4 é costurado de trechos, e na emenda a imagem pula. Se
             há um edicao.json ao lado do vídeo, a suavização roda trecho a
             trecho entre as emendas dele, e a caixa pula junto com a imagem em
             vez de deslizar através do corte (câmera que começa a andar antes
             de um corte seco denuncia a máquina).

  buracos    por dentro da suavização, buraco segura o último rosto conhecido,
             e antes do primeiro rosto achado vale o primeiro achado: a caixa
             nunca anda sozinha para onde não há rosto. No arquivo, buraco
             curto (até 0,5 s: piscada do detector, mão na frente do rosto)
             grava caixa, interpolada entre os vizinhos, com a confiança
             interpolada também. Buraco longo, inclusive no começo, grava null:
             ali o rosto sumiu de verdade (tela preta, cartela, pessoa fora do
             quadro), o gate de colisão não deve ver rosto onde não há, e o
             motor segura a câmera sozinho (MOTOR.md 2.3).

O que sai:

  rosto.json        uma entrada por quadro, [x, y, largura, altura, confiança]
                    em pixels do quadro inteiro (mesmo com --regiao), ou null;
                    mais a mediana, a fonte, o modelo, a % de quadros com rosto
                    (achados) e a fps de análise. Os quadros seguem a grade da
                    fps: a entrada i é o instante i/fps, mesmo quando a fonte tem
                    taxa variável (o ffmpeg repete quadro onde ela pula), que é o
                    instante que o compositor posiciona.
  folha-rosto.png   nove instantes com a caixa desenhada (verde = a que vai para
                    o motor, branca = o que o detector viu, amarela = a região)
                    e, embaixo, o caminho do centro no tempo. OLHE: a verde tem
                    que estar no rosto nos nove, e a linha verde tem que ficar
                    reta onde a pessoa está parada.

Uso:

    flow-reels produzir/rosto --projeto projetos/<video> --corte 01
    flow-reels produzir/rosto --video caminho.mp4 --saida rosto.json
    flow-reels produzir/rosto --video tela.mp4 --saida rosto.json --regiao 1550:270:350:610
    flow-reels produzir/rosto --video fala.mp4 --saida rosto.json --passo 2 --folha conferir.png

--projeto/--corte  lê materiais-de-trabalho/corte-NN/fala.mp4 e grava rosto.json e
                   folha-rosto.png na mesma pasta.
--regiao           x:y:largura:altura em pixels do quadro inteiro. Recorta antes de
                   detectar, para a webcam pequena num canto de gravação de tela:
                   no quadro inteiro, um rosto desse tamanho fica abaixo do que o
                   detector enxerga. As caixas saem no quadro inteiro do mesmo jeito.
--passo N          analisa 1 quadro a cada N e interpola os outros. 2 corta o tempo
                   de detecção pela metade e quase não muda a caixa suavizada.
--folha            onde gravar a folha de contato (padrão: folha-rosto.png ao lado
                   do rosto.json).
--confianca        confiança mínima de uma detecção (padrão 0,5).

MediaPipe no Mac: o 1.0.1 aborta o processo inteiro no caminho de CPU (o
calculador de detecções sempre abre o Metal, e aborto não se captura em Python).
Por isso o script testa antes, num processo separado, o caminho que funciona
nesta máquina: no Mac, o Metal, com o quadro em RGBA, que é o formato que ele
aceita; fora do Mac, a CPU. Tudo local e gratuito do mesmo jeito.

Saída 0 = rosto.json gravado. Saída 1 = gravou, mas o rosto apareceu em menos de
metade dos quadros (o motor vai cair na mediana; o script diz o que tentar).
Saída 2 = erro de uso ou de ambiente.
"""

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import deque
from contextlib import contextmanager
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


MODELO = "blaze_face_short_range.tflite"   # em componentes/modelos/
LADO_ANALISE = 640    # lado maior do quadro que vai para o detector, em px
CONFIANCA = 0.5       # confiança mínima de uma detecção
MEMORIA = 1.0         # por quanto tempo os rostos anteriores ainda puxam a escolha, em s
ZONA_CENTRO = 0.03    # zona morta do centro, fração da janela 9:16 que cabe no quadro (ou na região)
ZONA_TAMANHO = 0.06   # variação relativa do tamanho que a caixa ignora
TAU_CENTRO = 0.4      # constante de tempo do seguimento do centro, em s
TAU_TAMANHO = 1.0     # constante de tempo do tamanho, em s
RECENTRA = 0.5        # parado dentro da zona por isso, a caixa se recentra no rosto, em s
CONFIRMA = 0.4        # o rosto precisa ficar fora da zona por isso para a caixa ir atrás, em s
JANELA_MEDIANA = 0.2  # mediana móvel contra detecção solta, em s
BURACO_CURTO = 0.5    # buraco até isso é piscada do detector: interpola e grava caixa, em s
PARADA = 0.0005       # abaixo disso por quadro (fração do lado menor), a câmera conta como parada
POUCO = 0.50          # rosto em menos que isso dos quadros analisados: saída 1
ATENCAO = 0.85        # abaixo disso, aviso para olhar a folha
INSTANTES = 9         # instantes na folha de contato
CELULA = 480          # lado maior de cada instante na folha, em px

FONTES_DO_SISTEMA = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
)

FUNDO = (16, 16, 20)
VERDE = (61, 220, 132)
BRANCO = (235, 235, 240)
AMARELO = (255, 214, 10)
VERMELHO = (255, 95, 95)
CINZA = (120, 120, 132)
ESCURO = (34, 34, 42)

# O teste do caminho do MediaPipe roda num processo separado: se ele abortar,
# quem morre é o teste, e o script segue para o próximo caminho.
SONDA = r"""
import sys
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
delegado = BaseOptions.Delegate.GPU if sys.argv[2] == "metal" else BaseOptions.Delegate.CPU
det = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path=sys.argv[1], delegate=delegado),
    running_mode=vision.RunningMode.VIDEO))
det.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGBA,
                              data=np.zeros((96, 96, 4), np.uint8)), 0)
det.close()
print("ok")
"""


def erro(msg):
    print("  erro: " + msg, file=sys.stderr)


def aviso(msg):
    print("  aviso: " + msg)


# ---------------------------------------------------------------------------
# Ambiente
# ---------------------------------------------------------------------------

def achar_raiz():
    """A pasta de trabalho; o modelo vem de componentes/modelos, da pasta ou do plugin."""
    return fabrica.raiz()


def exigir_ffmpeg():
    for nome in ("ffmpeg", "ffprobe"):
        if shutil.which(nome) is None:
            erro("%s não encontrado no PATH. Rode o instalar.sh na raiz do pacote." % nome)
            sys.exit(2)


def carregar_numpy():
    try:
        import numpy
    except ImportError:
        erro("o numpy não está instalado neste Python.\n"
             "       Rode com o Python do pacote: .venv/bin/python, ou instale com: pip install numpy")
        sys.exit(2)
    return numpy


def carregar_mediapipe():
    try:
        import mediapipe as mp
        from mediapipe.tasks.python import vision
        from mediapipe.tasks.python.core.base_options import BaseOptions
    except ImportError:
        erro("o mediapipe não está instalado neste Python.\n"
             "       Rode com o Python do pacote: .venv/bin/python, ou instale com: pip install mediapipe")
        sys.exit(2)
    return mp, vision, BaseOptions


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
    """Do log de C++ do MediaPipe, só as linhas que dizem o que quebrou."""
    uteis = [l.strip() for l in texto.splitlines()
             if any(p in l for p in ("Check failed", "Error", "error", "rror:", "Traceback"))]
    if not uteis:
        uteis = [l.strip() for l in texto.splitlines() if l.strip()][-3:]
    return "\n       ".join(uteis[-3:])


def escolher_caminho(modelo):
    """Testa, num processo separado, qual caminho do MediaPipe roda nesta máquina."""
    candidatos = ["metal", "cpu"] if sys.platform == "darwin" else ["cpu"]
    falhas = []
    for nome in candidatos:
        try:
            proc = subprocess.run([sys.executable, "-c", SONDA, str(modelo), nome],
                                  capture_output=True, text=True, errors="replace", timeout=180)
        except subprocess.TimeoutExpired:
            falhas.append("%s: o teste passou de 3 minutos" % nome)
            continue
        if proc.returncode == 0 and "ok" in proc.stdout:
            return nome
        falhas.append("%s: %s" % (nome, linhas_de_falha(proc.stderr)))
    erro("o detector de rosto do MediaPipe não abriu nesta máquina. O que cada caminho disse:\n       "
         + "\n       ".join(falhas)
         + "\n       Confira se o mediapipe do .venv é o 1.0.1 e se o modelo em componentes/modelos/"
           " não está corrompido (ele tem cerca de 225 KB).")
    sys.exit(2)


def criar_detector(vision, BaseOptions, modelo, caminho, confianca):
    delegado = BaseOptions.Delegate.GPU if caminho == "metal" else BaseOptions.Delegate.CPU
    opcoes = vision.FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path=str(modelo), delegate=delegado),
        running_mode=vision.RunningMode.VIDEO,
        min_detection_confidence=confianca)
    with calar_stderr():
        return vision.FaceDetector.create_from_options(opcoes)


# ---------------------------------------------------------------------------
# Vídeo
# ---------------------------------------------------------------------------

def fracao(texto):
    try:
        if "/" in str(texto):
            a, b = str(texto).split("/")
            return float(a) / float(b) if float(b) else 0.0
        return float(texto)
    except (ValueError, TypeError):
        return 0.0


def sondar_video(caminho):
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-print_format", "json",
           "-show_streams", "-show_format", str(caminho)]
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        erro("o ffprobe não conseguiu ler %s:\n%s" % (caminho, proc.stderr.strip()[-600:]))
        sys.exit(2)
    try:
        dados = json.loads(proc.stdout or "{}")
    except ValueError:
        dados = {}
    fluxos = dados.get("streams") or []
    if not fluxos:
        erro("%s não tem trilha de vídeo." % caminho)
        sys.exit(2)
    v = fluxos[0]
    largura, altura = int(v.get("width") or 0), int(v.get("height") or 0)
    if largura <= 0 or altura <= 0:
        erro("não consegui ler o tamanho do quadro de %s." % caminho)
        sys.exit(2)

    # Vídeo de celular vem com rotação: o ffmpeg gira o quadro ao decodificar,
    # então a caixa vive no quadro já girado, e largura e altura trocam.
    rotacao = 0
    for lado in v.get("side_data_list") or []:
        if "rotation" in lado:
            rotacao = int(round(float(lado["rotation"])))
    if not rotacao and (v.get("tags") or {}).get("rotate"):
        rotacao = int(fracao(v["tags"]["rotate"]))
    if abs(rotacao) % 180 == 90:
        largura, altura = altura, largura

    # A fps nominal (r_frame_rate) vale quando é sensata; vídeo de taxa variável de
    # celular cai na média, encostada na taxa padrão mais próxima.
    r_txt, m_txt = v.get("r_frame_rate") or "0/0", v.get("avg_frame_rate") or "0/0"
    r, m = fracao(r_txt), fracao(m_txt)
    if 1 <= r <= 120 and (m <= 0 or abs(r - m) / r < 0.05):
        fps, fps_txt = r, r_txt
    elif 1 <= m <= 120:
        fps, fps_txt = m, m_txt
        for padrao, texto in ((24000 / 1001.0, "24000/1001"), (24.0, "24"), (25.0, "25"),
                              (30000 / 1001.0, "30000/1001"), (30.0, "30"), (50.0, "50"),
                              (60000 / 1001.0, "60000/1001"), (60.0, "60")):
            if abs(m - padrao) / padrao < 0.01:
                fps, fps_txt = padrao, texto
                break
    else:
        fps, fps_txt = 30.0, "30"
    duracao = fracao((dados.get("format") or {}).get("duration") or v.get("duration") or 0)
    return largura, altura, fps, fps_txt, duracao


def ler_regiao(texto, largura, altura):
    partes = re.split(r"[:,x]", texto.strip())
    try:
        x, y, w, h = [int(round(float(p.replace(",", ".")))) for p in partes]
    except ValueError:
        erro("--regiao é x:y:largura:altura em pixels do quadro inteiro, por exemplo 1550:270:350:610")
        sys.exit(2)
    if w <= 0 or h <= 0:
        erro("--regiao precisa de largura e altura positivas; veio %s" % texto)
        sys.exit(2)
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(largura, x + w), min(altura, y + h)
    if x1 - x0 < 32 or y1 - y0 < 32:
        erro("--regiao %s cai fora do quadro de %dx%d (ou sobra menos de 32 px dentro dele)."
             % (texto, largura, altura))
        sys.exit(2)
    if (x0, y0, x1, y1) != (x, y, x + w, y + h):
        aviso("a --regiao passava da borda do quadro de %dx%d; usei %d:%d:%d:%d."
              % (largura, altura, x0, y0, x1 - x0, y1 - y0))
    return x0, y0, x1 - x0, y1 - y0


def par(n):
    return max(2, int(round(n / 2.0)) * 2)


def detectar(video, fps, fps_txt, quadro, regiao, passo, det, mp, np):
    """Passa o vídeo inteiro pelo detector. Devolve, por quadro, o rosto escolhido
    em pixels do quadro inteiro (cx, cy, w, h, confiança) ou None, e se o quadro
    foi analisado."""
    rx, ry, rw, rh = regiao or (0, 0, quadro[0], quadro[1])
    aw, ah = rw, rh
    filtros = ["fps=%s" % fps_txt]
    if regiao:
        filtros.append("crop=%d:%d:%d:%d:exact=1" % (rw, rh, rx, ry))
    if max(rw, rh) > LADO_ANALISE:
        k = LADO_ANALISE / float(max(rw, rh))
        aw, ah = par(rw * k), par(rh * k)
        filtros.append("scale=%d:%d:flags=area" % (aw, ah))
    filtros.append("format=rgba")   # o caminho Metal só aceita quadro de 4 canais
    sx, sy = rw / float(aw), rh / float(ah)

    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-i", str(video), "-map", "0:v:0",
           "-vf", ",".join(filtros), "-fps_mode", "passthrough", "-f", "rawvideo", "-"]
    tamanho = aw * ah * 4
    registro = tempfile.TemporaryFile()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=registro)

    rostos, analisados = [], []
    recentes = deque(maxlen=5)
    i = 0
    primeiro = True
    try:
        while True:
            bruto = proc.stdout.read(tamanho)
            if len(bruto) < tamanho:
                break
            if i % passo:
                rostos.append(None)
                analisados.append(False)
                i += 1
                continue
            imagem = mp.Image(image_format=mp.ImageFormat.SRGBA,
                              data=np.frombuffer(bruto, np.uint8).reshape(ah, aw, 4))
            instante = int(round(i * 1000.0 / fps))
            if primeiro:
                with calar_stderr():   # o primeiro quadro ainda solta log do delegado
                    resultado = det.detect_for_video(imagem, instante)
                primeiro = False
            else:
                resultado = det.detect_for_video(imagem, instante)
            rosto = escolher(resultado.detections, recentes, i, fps)
            if rosto:
                cx, cy, w, h, conf = rosto
                rostos.append((rx + cx * sx, ry + cy * sy, w * sx, h * sy, conf))
            else:
                rostos.append(None)
            analisados.append(True)
            i += 1
    finally:
        if proc.poll() is None:
            proc.kill()
        proc.stdout.close()
        proc.wait()
    registro.seek(0)
    log = registro.read().decode("utf-8", "ignore").strip()
    registro.close()
    if not rostos:
        erro("o ffmpeg não entregou nenhum quadro de %s.%s" % (video, ("\n" + log[-600:]) if log else ""))
        sys.exit(2)
    if proc.returncode != 0:
        aviso("o ffmpeg parou com erro depois de %d quadros; o rosto.json cobre só esses.\n         %s"
              % (len(rostos), log[-300:].replace("\n", "\n         ")))
    return rostos, analisados, (aw, ah)


def escolher(deteccoes, recentes, i, fps):
    """O rosto principal: maior confiança x área, puxado para perto dos rostos do
    último segundo. Longe deles, a nota cai até 30%, então outro rosto só toma a
    câmera se for mais de três vezes mais forte."""
    validos = [r for r in recentes if i - r[0] <= MEMORIA * fps]
    referencia = None
    if validos:
        ordem = sorted(validos, key=lambda r: r[1])
        meio = ordem[len(ordem) // 2]
        referencia = (meio[1], sorted(r[2] for r in validos)[len(validos) // 2],
                      sorted(r[3] for r in validos)[len(validos) // 2])
    melhor, nota_melhor = None, 0.0
    for d in deteccoes:
        bb = d.bounding_box
        w, h = float(bb.width), float(bb.height)
        if w <= 0 or h <= 0:
            continue
        conf = float(d.categories[0].score) if d.categories else 0.0
        cx, cy = bb.origin_x + w / 2.0, bb.origin_y + h / 2.0
        nota = conf * w * h
        if referencia:
            dist = math.hypot(cx - referencia[0], cy - referencia[1]) / max(referencia[2], 1.0)
            nota *= 0.3 + 0.7 * math.exp(-dist * dist)
        if nota > nota_melhor:
            melhor, nota_melhor = (cx, cy, w, h, conf), nota
    if melhor:
        recentes.append((i, melhor[0], melhor[1], math.sqrt(melhor[2] * melhor[3])))
    return melhor


# ---------------------------------------------------------------------------
# Suavização
# ---------------------------------------------------------------------------

def preencher(valores, achado, curto, np):
    """Tapa os buracos. Curto: interpola. Longo: segura o último conhecido. Antes
    do primeiro achado: o primeiro achado. Devolve também onde a caixa vale
    (buraco longo não vale e vira null no JSON)."""
    n = len(valores)
    idx = np.flatnonzero(achado)
    todos = np.arange(n)
    cheio = np.empty_like(valores)
    for c in range(valores.shape[1]):
        cheio[:, c] = np.interp(todos, idx, valores[idx, c])   # nas pontas, segura
    presente = achado.copy()
    if idx[0] <= curto:
        presente[:idx[0]] = True
    if n - 1 - idx[-1] <= curto:
        presente[idx[-1] + 1:] = True
    for k in np.flatnonzero(np.diff(idx) > 1):
        a, b = idx[k], idx[k + 1]
        if b - a - 1 <= curto:
            presente[a + 1:b] = True
        else:
            cheio[a + 1:b] = valores[a]
    return cheio, presente


def mediana_movel(x, janela, np):
    if janela < 3 or len(x) < janela:
        return x.copy()
    meio = janela // 2
    borda = np.pad(x, (meio, meio), mode="edge")
    return np.median(np.lib.stride_tricks.sliding_window_view(borda, janela), axis=1)


def zona_morta(p, dz, recentra, confirma, np):
    """O alvo da câmera num eixo. Parado enquanto o rosto fica a menos de dz dele.
    Quando o rosto sai e fica fora por `confirma` quadros, o alvo vai junto,
    encostado na borda da zona, desde o primeiro quadro fora: o vídeo já está
    inteiro na mão, então dá para olhar adiante sem criar atraso, e aceno de
    cabeça que volta logo não arrasta a câmera. Quando o rosto fica parado por
    `recentra` quadros, o alvo pula para a mediana dele nesse trecho, desde o
    começo do trecho."""
    n = len(p)
    alvo = np.empty(n)
    a = float(np.median(p[:max(1, recentra)]))
    inicio, recentrado, seguindo = 0, False, False
    for i in range(n):
        v = p[i]
        if seguindo:
            if v > a + dz:
                a = v - dz
            elif v < a - dz:
                a = v + dz
            else:
                seguindo, inicio, recentrado = False, i, False
        elif v > a + dz or v < a - dz:
            adiante = p[i:i + confirma]
            fora = adiante > a + dz if v > a else adiante < a - dz
            if np.mean(fora) >= 0.8:
                seguindo = True
                a = v - dz if v > a else v + dz
        if not seguindo and not recentrado and i + 1 - inicio >= recentra:
            a = float(np.median(p[inicio:i + 1]))
            alvo[inicio:i] = a
            recentrado = True
        alvo[i] = a
    return alvo


def suavizar(x, tau, fps, np):
    """Exponencial para frente e depois para trás: sem atraso. Cada passada usa
    tau/raiz(2), para o núcleo somado ter a mesma largura de uma exponencial
    simples de constante tau."""
    n = len(x)
    if n < 2 or tau <= 0:
        return x.copy()
    alfa = 1.0 - math.exp(-1.0 / ((tau / math.sqrt(2.0)) * fps))
    y = np.array(x, dtype=float)
    for i in range(1, n):
        y[i] = y[i - 1] + alfa * (y[i] - y[i - 1])
    for i in range(n - 2, -1, -1):
        y[i] = y[i + 1] + alfa * (y[i] - y[i + 1])
    return y


def janela_vertical(largura, altura):
    """A maior janela 9:16 que cabe na área: é o quadro que o reel mostra."""
    if largura / float(altura) > 9 / 16.0:
        return altura * 9 / 16.0, float(altura)
    return float(largura), largura * 16 / 9.0


def ler_emendas(video, fps, duracao):
    """As emendas do edicao.json que mora ao lado do vídeo, em índice de quadro.
    Um edicao.json de outra edição (duração diferente) é ignorado."""
    caminho = video.parent / "edicao.json"
    if not caminho.is_file():
        return []
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        aviso("não consegui ler %s; segui sem as emendas." % caminho)
        return []
    total = dados.get("duracao")
    if isinstance(total, (int, float)) and duracao and abs(float(total) - duracao) > 0.25:
        aviso("o edicao.json ao lado do vídeo diz %.2f s e o vídeo tem %.2f s; ignorei as emendas"
              " dele (deve ser de outra edição)." % (total, duracao))
        return []
    emendas = [t for t in dados.get("emendas") or [] if isinstance(t, (int, float))]
    return sorted({int(round(float(t) * fps)) for t in emendas})


def caixa_suave(rostos, fps, passo, janela_reel, emendas, np):
    n = len(rostos)
    brutos = np.full((n, 5), np.nan)
    for i, r in enumerate(rostos):
        if r:
            brutos[i] = r
    achado = ~np.isnan(brutos[:, 0])

    curto = max(int(round(BURACO_CURTO * fps)), 2 * passo)
    cheio, presente = preencher(brutos, achado, curto, np)

    janela = max(3, int(round(JANELA_MEDIANA * fps)) | 1)
    recentra = max(2, int(round(RECENTRA * fps)))
    confirma = max(2, int(round(CONFIRMA * fps)))
    dzx, dzy = ZONA_CENTRO * janela_reel[0], ZONA_CENTRO * janela_reel[1]
    dz_tam = math.log(1.0 + ZONA_TAMANHO)

    def eixo(serie, dz, tau):
        return suavizar(zona_morta(mediana_movel(serie, janela, np), dz, recentra, confirma, np), tau, fps, np)

    # Trecho a trecho entre as emendas do fala.mp4: na emenda a imagem pula, e a
    # caixa pula junto, em vez de deslizar através do corte.
    limites = [0] + [k for k in emendas if 0 < k < n] + [n]
    cx, cy, lw, lh = (np.empty(n) for _ in range(4))
    for a, b in zip(limites[:-1], limites[1:]):
        if b > a:
            cx[a:b] = eixo(cheio[a:b, 0], dzx, TAU_CENTRO)
            cy[a:b] = eixo(cheio[a:b, 1], dzy, TAU_CENTRO)
            lw[a:b] = eixo(np.log(cheio[a:b, 2]), dz_tam, TAU_TAMANHO)
            lh[a:b] = eixo(np.log(cheio[a:b, 3]), dz_tam, TAU_TAMANHO)
    w, h = np.exp(lw), np.exp(lh)

    quadros = []
    for i in range(n):
        if not presente[i]:
            quadros.append(None)
            continue
        quadros.append((int(round(cx[i] - w[i] / 2.0)), int(round(cy[i] - h[i] / 2.0)),
                        int(round(w[i])), int(round(h[i])), float(cheio[i, 4])))
    return {"quadros": quadros, "brutos": brutos, "achado": achado, "presente": presente,
            "cx": cx, "cy": cy, "w": w, "h": h, "dz": (dzx, dzy), "emendas": limites[1:-1]}


def medir(s, analisados, passo, lado_menor, np):
    """Os números que o script imprime: quanto achou, quanto a caixa anda."""
    achado, presente, brutos = s["achado"], s["presente"], s["brutos"]
    n_anal = int(np.sum(analisados))
    m = {"achados": 100.0 * int(achado.sum()) / max(1, n_anal),
         "com_caixa": 100.0 * int(presente.sum()) / max(1, len(presente))}
    if not presente.any():
        return m
    cx, cy = s["cx"][presente], s["cy"][presente]
    mx, my = float(np.median(cx)), float(np.median(cy))
    m["desvio"] = (float(np.std(cx)), float(np.std(cy)))
    m["maximo"] = float(np.max(np.hypot(cx - mx, cy - my)))
    juntos = presente[1:] & presente[:-1]
    for k in s.get("emendas", []):   # o pulo na emenda é corte, não câmera andando
        juntos[k - 1] = False
    passos_suaves = np.hypot(np.diff(s["cx"]), np.diff(s["cy"]))[juntos]
    m["tremida_caixa"] = float(np.mean(passos_suaves)) if passos_suaves.size else 0.0
    m["parada"] = (100.0 * float(np.mean(passos_suaves < PARADA * lado_menor))
                   if passos_suaves.size else 100.0)
    idx = np.flatnonzero(achado)
    vizinhos = np.diff(idx) == passo
    if vizinhos.any():
        db = np.hypot(np.diff(brutos[idx, 0]), np.diff(brutos[idx, 1]))[vizinhos] / passo
        m["tremida_detector"] = float(np.mean(db))
    else:
        m["tremida_detector"] = float("nan")
    m["tamanho"] = (float(np.min(s["w"][presente])), float(np.median(s["w"][presente])),
                    float(np.max(s["w"][presente])))
    return m


# ---------------------------------------------------------------------------
# Saídas
# ---------------------------------------------------------------------------

def gravar_json(destino, cabecalho, quadros):
    """Um quadro por linha: o arquivo continua JSON, e dá para ler e comparar."""
    linhas = ["{"]
    for chave, valor in cabecalho.items():
        linhas.append("  %s: %s," % (json.dumps(chave), json.dumps(valor, ensure_ascii=False)))
    corpo = ["    null" if q is None else "    [%d, %d, %d, %d, %.2f]" % q for q in quadros]
    linhas.append('  "quadros": [')
    if corpo:
        linhas.append(",\n".join(corpo))
    linhas.append("  ]")
    linhas.append("}")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def carregar_fonte(tamanho):
    """Uma fonte do sistema com acento. A embutida no Pillow não tem nenhum:
    sem fonte do sistema, a folha sai sem acento, mas sai."""
    from PIL import ImageFont
    for caminho in FONTES_DO_SISTEMA:
        if os.path.isfile(caminho):
            try:
                return ImageFont.truetype(caminho, tamanho), True
            except OSError:
                pass
    try:
        return ImageFont.load_default(size=tamanho), False
    except TypeError:
        return ImageFont.load_default(), False


def sem_acento(texto):
    import unicodedata
    texto = texto.replace("·", "-")
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")


def extrair_quadro(video, t, recorte, celula):
    from PIL import Image
    x0, y0, w0, h0 = recorte
    cw, ch = celula
    filtro = "crop=%d:%d:%d:%d:exact=1,scale=%d:%d:flags=area,format=rgb24" % (w0, h0, x0, y0, cw, ch)
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-ss", "%.3f" % max(0.0, t), "-i", str(video),
           "-map", "0:v:0", "-frames:v", "1", "-vf", filtro, "-f", "rawvideo", "-"]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0 or len(proc.stdout) < cw * ch * 3:
        return Image.new("RGB", (cw, ch), ESCURO)
    return Image.frombytes("RGB", (cw, ch), proc.stdout[:cw * ch * 3])


def retangulo(desenho, caixa, cor, largura):
    x, y, w, h = caixa
    for k in range(largura):
        desenho.rectangle([x - k, y - k, x + w + k, y + h + k], outline=cor)


def escrever(desenho, xy, texto, fonte, cor=BRANCO, fundo=False):
    tipo, completa = fonte
    if not completa:
        texto = sem_acento(texto)
    if fundo:
        caixa = desenho.textbbox(xy, texto, font=tipo)
        desenho.rectangle([caixa[0] - 4, caixa[1] - 3, caixa[2] + 4, caixa[3] + 3], fill=FUNDO)
    desenho.text(xy, texto, fill=cor, font=tipo)


def folha_de_contato(destino, video, quadro, regiao, fps, s, titulo, np):
    """Nove instantes com a caixa desenhada e o caminho do centro no tempo."""
    from PIL import Image, ImageDraw

    largura, altura = quadro
    n = len(s["quadros"])
    indices = [min(n - 1, int((k + 0.5) * n / INSTANTES)) for k in range(INSTANTES)]

    # com --regiao, a célula mostra a região com folga de um quarto em volta;
    # no quadro inteiro, uma webcam de canto ficaria pequena demais para conferir
    if regiao:
        rx, ry, rw, rh = regiao
        x0, y0 = max(0, int(rx - rw * 0.25)), max(0, int(ry - rh * 0.25))
        x1, y1 = min(largura, int(rx + rw * 1.25)), min(altura, int(ry + rh * 1.25))
    else:
        x0, y0, x1, y1 = 0, 0, largura, altura
    w0, h0 = x1 - x0, y1 - y0
    k = CELULA / float(max(w0, h0))
    cw, ch = par(w0 * k), par(h0 * k)
    kx, ky = cw / float(w0), ch / float(h0)

    def leva(caixa):
        x, y, w, h = caixa
        return ((x - x0) * kx, (y - y0) * ky, w * kx, h * ky)

    margem, colunas = 12, 3
    linhas_grade = int(math.ceil(INSTANTES / float(colunas)))
    topo = 44
    faixa = 2 * 132 + 30
    folha_w = margem + colunas * (cw + margem)
    folha_h = topo + linhas_grade * (ch + margem) + faixa
    folha = Image.new("RGB", (folha_w, folha_h), FUNDO)
    desenho = ImageDraw.Draw(folha)
    fonte, fonte_p = carregar_fonte(17), carregar_fonte(13)
    escrever(desenho, (margem, 13), titulo, fonte)

    for ordem, i in enumerate(indices):
        img = extrair_quadro(video, i / fps, (x0, y0, w0, h0), (cw, ch))
        d = ImageDraw.Draw(img)
        if regiao:
            retangulo(d, leva(regiao), AMARELO, 2)
        if s["achado"][i]:
            b = s["brutos"][i]
            retangulo(d, leva((b[0] - b[2] / 2, b[1] - b[3] / 2, b[2], b[3])), BRANCO, 1)
        q = s["quadros"][i]
        if q is None:
            escrever(d, (8, ch - 26), "sem rosto (null)", fonte_p, VERMELHO, fundo=True)
        else:
            retangulo(d, leva(q[:4]), VERDE, 3)
            escrever(d, (8, ch - 26), "conf %.2f%s" % (q[4], "" if s["achado"][i] else " (preenchido)"),
                     fonte_p, fundo=True)
        escrever(d, (8, 8), "%d  ·  %.1f s" % (ordem + 1, i / fps), fonte_p, fundo=True)
        col, lin = ordem % colunas, ordem // colunas
        folha.paste(img, (margem + col * (cw + margem), topo + lin * (ch + margem)))

    # o caminho do centro no tempo: cinza = detector, verde = caixa gravada
    base = topo + linhas_grade * (ch + margem) + 6
    util = folha_w - 2 * margem
    for eixo, nome in ((0, "centro x"), (1, "centro y")):
        y_top, alt = base + eixo * 132 + 18, 104
        desenho.rectangle([margem, y_top, margem + util, y_top + alt], fill=ESCURO)
        brutos = s["brutos"][s["achado"], eixo]
        suaves = (s["cx"] if eixo == 0 else s["cy"])[s["presente"]]
        if brutos.size == 0:
            continue
        dz = s["dz"][eixo]
        vmin = float(min(brutos.min(), suaves.min() if suaves.size else brutos.min())) - dz
        vmax = float(max(brutos.max(), suaves.max() if suaves.size else brutos.max())) + dz
        faixa_v = max(vmax - vmin, 1.0)

        def ponto(i, v):
            return (margem + util * i / max(1, n - 1), y_top + alt - (v - vmin) / faixa_v * alt)

        for i in indices:
            xx = ponto(i, vmin)[0]
            desenho.line([xx, y_top, xx, y_top + alt], fill=(60, 60, 72))
        for k in s.get("emendas", []):   # emenda do fala.mp4: a caixa pode pular aqui
            xx = ponto(k, vmin)[0]
            desenho.line([xx, y_top, xx, y_top + 8], fill=AMARELO, width=2)
        if (~s["presente"]).any():
            for i in np.flatnonzero(~s["presente"]):
                xx = ponto(i, vmin)[0]
                desenho.line([xx, y_top + alt - 4, xx, y_top + alt], fill=VERMELHO)
        for i in np.flatnonzero(s["achado"]):
            xx, yy = ponto(i, s["brutos"][i, eixo])
            desenho.rectangle([xx - 1, yy - 1, xx + 1, yy + 1], fill=CINZA)
        serie = s["cx"] if eixo == 0 else s["cy"]
        trecho = []
        for i in range(n):
            if s["presente"][i]:
                trecho.append(ponto(i, serie[i]))
            elif trecho:
                if len(trecho) > 1:
                    desenho.line(trecho, fill=VERDE, width=2)
                trecho = []
        if len(trecho) > 1:
            desenho.line(trecho, fill=VERDE, width=2)
        escrever(desenho, (margem, y_top - 17),
                 "%s  ·  %.0f a %.0f px  ·  cinza = detector, verde = caixa gravada, zona morta %.0f px"
                 % (nome, vmin + dz, vmax - dz, dz), fonte_p)

    destino.parent.mkdir(parents=True, exist_ok=True)
    folha.save(str(destino))


# ---------------------------------------------------------------------------
# Linha de comando
# ---------------------------------------------------------------------------

def caminho_relativo(alvo, base):
    try:
        rel = os.path.relpath(str(alvo), str(base))
    except ValueError:
        return str(alvo)
    return str(alvo) if rel.startswith("..") else rel


def resolver_caminhos(args, raiz):
    if args.projeto:
        if args.video:
            erro("use --projeto/--corte ou --video/--saida, não os dois.")
            sys.exit(2)
        if not args.corte:
            erro("com --projeto, diga também o corte, por exemplo --corte 01")
            sys.exit(2)
        numero = re.sub(r"\D", "", args.corte)
        if not numero:
            erro("--corte é o número do corte, por exemplo 01")
            sys.exit(2)
        projeto = Path(args.projeto)
        if not projeto.is_dir() and not projeto.is_absolute() and (raiz / projeto).is_dir():
            projeto = raiz / projeto
        if not projeto.is_dir():
            erro("não achei a pasta do projeto %s" % args.projeto)
            sys.exit(2)
        pasta = projeto / "materiais-de-trabalho" / ("corte-%02d" % int(numero))
        video = pasta / "fala.mp4"
        if not video.is_file():
            erro("não achei %s.\n       O fala.mp4 sai do editar_fala.py; rode ele antes (MOTOR.md, seção 7)."
                 % video)
            sys.exit(2)
        saida = Path(args.saida) if args.saida else pasta / "rosto.json"
    else:
        if not args.video:
            erro("diga qual vídeo: --projeto projetos/<video> --corte 01, ou --video caminho.mp4 --saida rosto.json")
            sys.exit(2)
        video = Path(args.video)
        if not video.is_file():
            erro("não achei o vídeo %s" % video)
            sys.exit(2)
        if not args.saida:
            erro("com --video, diga onde gravar: --saida caminho/rosto.json")
            sys.exit(2)
        saida = Path(args.saida)
    folha = Path(args.folha) if args.folha else saida.parent / "folha-rosto.png"
    return video.resolve(), saida.resolve(), folha.resolve()


def principal():
    ap = argparse.ArgumentParser(
        description="Acha o rosto em cada quadro e grava a caixa suavizada (rosto.json, MOTOR.md 2.3).")
    ap.add_argument("--projeto", help="pasta do projeto, por exemplo projetos/aula")
    ap.add_argument("--corte", help="número do corte, por exemplo 01")
    ap.add_argument("--video", help="o vídeo, quando não for o fala.mp4 de um corte")
    ap.add_argument("--saida", help="onde gravar o rosto.json (obrigatório com --video)")
    ap.add_argument("--regiao", metavar="X:Y:LARGURA:ALTURA",
                    help="recorta essa região antes de detectar (webcam num canto de gravação de tela)")
    ap.add_argument("--passo", type=int, default=1, help="analisa 1 quadro a cada N e interpola (padrão 1)")
    ap.add_argument("--folha", help="PNG da folha de contato (padrão: folha-rosto.png ao lado do rosto.json)")
    ap.add_argument("--confianca", type=float, default=CONFIANCA,
                    help="confiança mínima de uma detecção, de 0 a 1 (padrão 0,5)")
    if len(sys.argv) == 1:
        ap.print_help()
        print("\nFaltou dizer qual vídeo. Comece por:")
        print("  flow-reels produzir/rosto --projeto projetos/<video> --corte 01")
        return 2
    args = ap.parse_args()

    if args.passo < 1:
        erro("--passo é um inteiro de 1 para cima")
        return 2
    if not 0.0 < args.confianca < 1.0:
        erro("--confianca fica entre 0 e 1, por exemplo 0.5")
        return 2

    raiz = achar_raiz()
    video, saida, folha = resolver_caminhos(args, raiz)
    modelo = fabrica.achar("componentes/modelos/" + MODELO)
    if not modelo.is_file():
        erro("não achei o modelo %s.\n"
             "       Ele vem no pacote. Se sumiu, baixe (gratuito, Apache-2.0) de\n"
             "       https://storage.googleapis.com/mediapipe-models/face_detector/"
             "blaze_face_short_range/float16/latest/blaze_face_short_range.tflite" % modelo)
        return 2
    exigir_ffmpeg()
    np = carregar_numpy()

    largura, altura, fps, fps_txt, duracao = sondar_video(video)
    regiao = ler_regiao(args.regiao, largura, altura) if args.regiao else None
    area_w, area_h = (regiao[2], regiao[3]) if regiao else (largura, altura)
    lado_menor = float(min(area_w, area_h))
    janela_reel = janela_vertical(area_w, area_h)

    relogio = time.time()
    mp, vision, BaseOptions = carregar_mediapipe()
    caminho = escolher_caminho(modelo)
    det = criar_detector(vision, BaseOptions, modelo, caminho, args.confianca)
    try:
        rostos, analisados, analise = detectar(video, fps, fps_txt, (largura, altura), regiao,
                                               args.passo, det, mp, np)
    except KeyboardInterrupt:
        erro("interrompido.")
        return 2
    finally:
        with calar_stderr():
            det.close()
    analisados = np.array(analisados, dtype=bool)
    n = len(rostos)

    if not any(rostos):
        s = {"quadros": [None] * n, "brutos": np.full((n, 5), np.nan),
             "achado": np.zeros(n, bool), "presente": np.zeros(n, bool),
             "cx": np.zeros(n), "cy": np.zeros(n), "w": np.zeros(n), "h": np.zeros(n),
             "dz": (ZONA_CENTRO * janela_reel[0], ZONA_CENTRO * janela_reel[1]), "emendas": []}
        mediana = None
    else:
        s = caixa_suave(rostos, fps, args.passo, janela_reel,
                        ler_emendas(video, fps, duracao), np)
        b = s["brutos"][s["achado"]]
        mediana = [int(round(float(np.median(b[:, 0] - b[:, 2] / 2)))),
                   int(round(float(np.median(b[:, 1] - b[:, 3] / 2)))),
                   int(round(float(np.median(b[:, 2])))), int(round(float(np.median(b[:, 3]))))]
    m = medir(s, analisados, args.passo, lado_menor, np)
    tempo_analise = time.time() - relogio

    fonte_json = "fala.mp4" if args.projeto else caminho_relativo(video, saida.parent)
    versao = getattr(mp, "__version__", "?")
    cabecalho = {
        "fps": int(round(fps)) if abs(fps - round(fps)) < 1e-6 else round(fps, 3),
        "largura": largura,
        "altura": altura,
        "fonte": fonte_json,
        "modelo": "%s (MediaPipe %s, %s)" % (MODELO.replace(".tflite", ""), versao,
                                            "Metal" if caminho == "metal" else "CPU"),
        "regiao": list(regiao) if regiao else None,
        "fps_analise": round(fps / args.passo, 3),
        "achados": round(m["achados"], 1),
        "mediana": mediana,
    }
    gravar_json(saida, cabecalho, s["quadros"])

    titulo = "rosto.py  ·  %s  ·  rosto em %.1f%% dos quadros%s" % (
        video.name, m["achados"], ("  ·  região %d:%d:%d:%d" % regiao) if regiao else "")
    try:
        folha_de_contato(folha, video, (largura, altura), regiao, fps, s, titulo, np)
        folha_ok = True
    except ImportError:
        aviso("o Pillow não está instalado neste Python, então a folha de contato não saiu.")
        folha_ok = False

    # ---- relatório ----
    print("")
    print("  rosto  ·  %s" % video)
    print("  %dx%d, %.1f s, %d quadros a %s fps%s; analisados %d (passo %d) em %dx%d, detector %s"
          % (largura, altura, duracao, n, cabecalho["fps"],
             ("; região %d:%d:%d:%d" % regiao) if regiao else "",
             int(analisados.sum()), args.passo, analise[0], analise[1],
             "Metal" if caminho == "metal" else "CPU"))
    print("")
    print("  achados     rosto em %.1f%% dos quadros analisados; caixa gravada em %.1f%% do vídeo"
          % (m["achados"], m["com_caixa"]))
    if "desvio" in m:
        print("  centro      desvio padrão %.1f px na horizontal e %.1f px na vertical"
              " (%.1f%% e %.1f%% do quadro do reel); no máximo a %.0f px da mediana"
              % (m["desvio"][0], m["desvio"][1], 100 * m["desvio"][0] / janela_reel[0],
                 100 * m["desvio"][1] / janela_reel[1], m["maximo"]))
        print("  zona morta  %.0f px na horizontal e %.0f px na vertical (3%% do quadro 9:16 de %.0fx%.0f)"
              % (s["dz"][0], s["dz"][1], janela_reel[0], janela_reel[1]))
        if s["emendas"]:
            print("  emendas     %d, do edicao.json (%s s): a caixa corta junto com a imagem"
                  % (len(s["emendas"]), ", ".join("%.2f" % (k / fps) for k in s["emendas"][:8])
                     + (", ..." if len(s["emendas"]) > 8 else "")))
        print("  câmera      parada em %.0f%% do tempo; o detector treme %.2f px por quadro, a caixa %.2f"
              % (m["parada"], m["tremida_detector"], m["tremida_caixa"]))
        print("  tamanho     largura de %.0f a %.0f px, mediana %.0f"
              % (m["tamanho"][0], m["tamanho"][2], m["tamanho"][1]))
        print("  mediana     %d:%d:%d:%d" % tuple(mediana))
    print("  tempo       %.1f s de análise para %.1f s de vídeo (%.1fx o tempo real)"
          % (tempo_analise, duracao or n / fps, (duracao or n / fps) / max(tempo_analise, 1e-6)))
    print("")
    print("  gravado     %s" % saida)
    if folha_ok:
        print("  folha       %s  (OLHE: caixa verde no rosto nos nove instantes)" % folha)
    print("")

    fracao_achada = m["achados"] / 100.0
    if fracao_achada < POUCO:
        print("  POUCO ROSTO  o detector achou rosto em só %.1f%% dos quadros." % m["achados"])
        if not regiao:
            print("    Webcam pequena num canto (gravação de tela) fica abaixo do que o detector enxerga")
            print("    no quadro inteiro, e o pouco que ele acha costuma ser o encarte todo, não o rosto.")
            print("    Rode de novo com --regiao x:y:largura:altura do encarte da webcam (o mesmo")
            print("    retângulo medido para a trava da webcam no SKILL.md, sem os 8 px de folga).")
        else:
            print("    Confira na folha se a região amarela cobre o encarte inteiro da webcam.")
        print("    Rosto de perfil, de costas, coberto ou muito escuro também some; nesses quadros")
        print("    o motor usa o último conhecido ou a mediana.")
        print("")
        return 1
    if fracao_achada < ATENCAO:
        aviso("rosto em %.1f%% dos quadros. Olhe a folha: os trechos sem rosto aparecem em"
              " vermelho no pé do gráfico." % m["achados"])
        print("")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
