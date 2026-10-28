# -*- coding: utf-8 -*-
"""A legenda do reel narrado, desenhada quadro a quadro em cima da imagem.

A lei esta em referencias/PADRAO-NARRADO.md, secao "Legenda". Em resumo:

  - uma linha so, centrada em y 1572, dentro da faixa de 1480 a 1660, de x 100 a 980;
  - cada palavra entra no proprio instante em que a voz diz ela, subindo 14 px e
    aparecendo em 0,16 s; o grupo inteiro sai 0,12 s antes do proximo chegar;
  - a palavra do comentario (e as palavras pedidas em "legenda.destaques") sai na cor
    de destaque da marca, uma por grupo no maximo;
  - texto na cor escura da marca com contorno claro; quando o fundo atras da faixa e
    escuro, entra uma placa clara atras do grupo (medida no proprio quadro);
  - palavra de ligacao (de, da, do, e, o, a, que, pra, um, com, por, se...) nunca fica
    pendurada no fim do grupo: ela desce para o grupo seguinte;
  - a legenda so comeca depois que o titulo da abertura sai, porque o titulo e a fala
    daquele trecho.

Fonte: o arquivo do papel "legenda" do marca/tokens.json (instancia estatica).

Uso:

    flow-reels narrado/legenda_narrado --projeto projetos/x --narrado 01
    flow-reels narrado/legenda_narrado --projeto projetos/x --narrado 01 --placa sempre

Le construcao/imagem.mp4, construcao/linha_do_tempo.json e construcao/plano.json.
Escreve construcao/legendado.mp4 (sem audio; o som entra no mixar.py).
"""

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402

W, H, FPS = cm.LARGURA, cm.ALTURA, cm.FPS
TAMANHO = 72
LARGURA_MAX = 860            # de x 110 a x 970, longe dos botoes da direita
CENTRO_X = 540
CY = cm.CENTRO_LEGENDA
ESPACO = 20
MAX_PALAVRAS = 4
PAUSA_QUEBRA = 0.45
LIMIAR_PLACA = 140           # brilho medio da faixa abaixo disso pede placa

LIGACAO = {
    "de", "da", "do", "das", "dos", "e", "o", "a", "os", "as", "em", "no", "na", "nos", "nas",
    "que", "pra", "pro", "um", "uma", "com", "por", "se", "para", "ao", "aos", "num", "numa",
    "pelo", "pela", "ou", "nem", "uns", "umas",
}


def termina_pontuado(texto):
    return texto.rstrip("\"'\u201d)")[-1:] in ".,;:!?\u2026"


def eh_ligacao(texto):
    return cm.normalizar(texto) in LIGACAO and not termina_pontuado(texto)


class Regua:
    def __init__(self, fonte):
        self.fonte = ImageFont.truetype(str(fonte), TAMANHO)
        self.d = ImageDraw.Draw(Image.new("L", (1, 1)))

    def largura(self, texto):
        return int(self.d.textlength(texto, font=self.fonte))

    def grupo(self, ws):
        return sum(self.largura(w["texto"]) for w in ws) + ESPACO * max(0, len(ws) - 1)


def agrupar(palavras, regua):
    saida, atual = [], []
    for w in palavras:
        if atual and w["inicio"] - atual[-1]["fim"] > PAUSA_QUEBRA:
            saida.append(atual)
            atual = []
        if atual and (len(atual) + 1 > MAX_PALAVRAS or regua.grupo(atual + [w]) > LARGURA_MAX):
            levar = []
            while len(atual) > 1 and eh_ligacao(atual[-1]["texto"]):
                levar.insert(0, atual.pop())
            saida.append(atual)
            atual = levar
        atual.append(w)
        if termina_pontuado(w["texto"]):
            saida.append(atual)
            atual = []
    if atual:
        saida.append(atual)
    # ultima conferencia: nenhum grupo termina em palavra de ligacao se o seguinte existe
    for i in range(len(saida) - 1):
        while len(saida[i]) > 1 and eh_ligacao(saida[i][-1]["texto"]):
            saida[i + 1].insert(0, saida[i].pop())
    return [g for g in saida if g]


def camada_palavra(texto, regua, cor, contorno):
    w = regua.largura(texto) + 16
    im = Image.new("RGBA", (w, TAMANHO + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((8, 6), texto, font=regua.fonte, fill=tuple(cor) + (255,),
                            stroke_width=3, stroke_fill=tuple(contorno) + (255,))
    a = np.asarray(im)
    return np.dstack([a[..., 2], a[..., 1], a[..., 0], a[..., 3]]).astype(np.float32)


def camada_placa(largura, cor):
    pw, ph = int(largura + 64), int(TAMANHO * 1.3 + 30)
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, pw - 1, ph - 1), 26, fill=tuple(cor) + (236,))
    a = np.asarray(im)
    return np.dstack([a[..., 2], a[..., 1], a[..., 0], a[..., 3]]).astype(np.float32)


def colar(dst, rgba, x, y, op):
    h, w = rgba.shape[:2]
    x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1 or op <= 0:
        return
    s = rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4] / 255.0 * op
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + s[..., :3] * a


def sai(x, p=3):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** p


def montar_plano(palavras, regua, cores_marca, chave, destaques, pular_antes):
    destaques = {cm.normalizar(d) for d in destaques if cm.normalizar(d)}
    if chave:
        destaques.add(cm.normalizar(chave))
    grupos = [g for g in agrupar(palavras, regua) if g[0]["inicio"] >= pular_antes - 1e-6]
    plano = []
    for i, g in enumerate(grupos):
        for w in g:
            cm.recusar_travessao(w["texto"], "a legenda (palavra %r)" % w["texto"])
        largura = regua.grupo(g)
        esc = min(1.0, LARGURA_MAX / float(max(largura, 1)))
        x = CENTRO_X - largura * esc / 2.0
        camadas, usou = [], False
        for w in g:
            acende = not usou and cm.normalizar(w["texto"]) in destaques
            usou = usou or acende
            cor = cores_marca["destaque"] if acende else cores_marca["escuro"]
            lay = camada_palavra(w["texto"].replace('"', ""), regua, cor, cores_marca["claro"])
            if esc < 1.0:
                import cv2
                lay = cv2.resize(lay, None, fx=esc, fy=esc, interpolation=cv2.INTER_AREA)
            camadas.append((w["inicio"], lay, x - 8 * esc))
            x += (regua.largura(w["texto"]) + ESPACO) * esc
        t0 = g[0]["inicio"]
        t1 = grupos[i + 1][0]["inicio"] - 0.10 if i + 1 < len(grupos) else g[-1]["fim"] + 0.6
        t1 = min(t1, g[-1]["fim"] + 0.55)
        plano.append({"t0": t0, "t1": t1, "camadas": camadas, "largura": largura * esc,
                      "placa": None, "texto": " ".join(w["texto"] for w in g)})
    return plano


def principal(argv=None):
    an = cm.argumentos_de_reel(argparse.ArgumentParser(description="Queima a legenda do reel narrado."))
    an.add_argument("--marca", default=None, help="tokens.json ou pasta da marca (padrao marca/)")
    an.add_argument("--entrada", default=None, help="video de entrada (padrao construcao/imagem.mp4)")
    an.add_argument("--saida", default=None, help="video de saida (padrao construcao/legendado.mp4)")
    an.add_argument("--placa", choices=("auto", "sempre", "nunca"), default="auto",
                    help="placa clara atras da legenda: auto mede o fundo (padrao)")
    op = an.parse_args(argv)
    cm.exigir_ffmpeg()
    cam = cm.Caminhos(op.projeto, op.narrado)
    entrada = Path(op.entrada) if op.entrada else cam.imagem
    saida = Path(op.saida) if op.saida else cam.legendado
    if not entrada.is_file():
        cm.erro("nao achei %s. Rode o compor_narrado.py antes." % entrada)
    tl = cm.ler_json(cam.linha)
    plano_reel = cm.ler_json(cam.plano) if cam.plano.is_file() else {}
    tokens, origem = cm.ler_marca(op.marca)
    cores_marca = cm.cores(tokens)
    regua = Regua(cm.arquivo_fonte(tokens, origem, "legenda"))
    pular = (plano_reel.get("abertura") or {}).get("fim", 0.0)
    chave = plano_reel.get("palavra_chave") or ""
    destaques = (plano_reel.get("legenda") or {}).get("destaques", [])
    plano = montar_plano(tl["palavras"], regua, cores_marca, chave, destaques, pular)
    largura_maior = max((g["largura"] for g in plano), default=0)
    cm.fala("%d grupos de legenda, o mais largo com %d px (teto %d)." % (len(plano), largura_maior, LARGURA_MAX))

    ler = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(entrada), "-f", "rawvideo",
                            "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE, bufsize=10 ** 7)
    escrever = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "%dx%d" % (W, H),
         "-r", str(FPS), "-i", "-",
         "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setsar=1",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high",
         "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
         "-movflags", "+faststart", str(saida)], stdin=subprocess.PIPE)
    n = W * H * 3
    i = 0
    placas = 0
    try:
        while True:
            bruto = ler.stdout.read(n)
            if len(bruto) < n:
                break
            t = i / float(FPS)
            fr = np.frombuffer(bruto, np.uint8).reshape(H, W, 3)
            ativos = [g for g in plano if g["t0"] - 0.05 <= t < g["t1"] + 0.12]
            if ativos:
                quadro = fr.astype(np.float32)
                for g in ativos:
                    if g["placa"] is None:
                        faixa = fr[cm.FAIXA_LEGENDA[0] + 10:cm.FAIXA_LEGENDA[1] - 10, 90:990]
                        brilho = float(faixa.mean())
                        usar = op.placa == "sempre" or (op.placa == "auto" and brilho < LIMIAR_PLACA)
                        g["placa"] = camada_placa(g["largura"], cores_marca["claro"]) if usar else False
                        placas += 1 if usar else 0
                    fora = 1 - sai((t - g["t1"]) / 0.12) if t >= g["t1"] else 1.0
                    if g["placa"] is not False:
                        p = g["placa"]
                        colar(quadro, p, CENTRO_X - p.shape[1] / 2.0, CY - p.shape[0] / 2.0,
                              fora * sai((t - g["t0"] + 0.05) / 0.12))
                    for st, lay, x in g["camadas"]:
                        u = sai((t - st + 0.04) / 0.16)
                        if u <= 0:
                            continue
                        y = CY - lay.shape[0] / 2.0 + 14 * (1 - u)
                        colar(quadro, lay, x, y, u * fora)
                fr = np.clip(quadro, 0, 255).astype(np.uint8)
            escrever.stdin.write(fr.tobytes())
            i += 1
    finally:
        escrever.stdin.close()
        escrever.wait()
        ler.stdout.close()
        ler.wait()
    if escrever.returncode != 0:
        cm.erro("o ffmpeg nao fechou o video legendado.")
    cm.fala("legenda queimada em %d quadros, %d grupos com placa: %s" % (i, placas, saida))
    return 0


if __name__ == "__main__":
    sys.exit(principal())
