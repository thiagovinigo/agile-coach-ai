# -*- coding: utf-8 -*-
"""A conferencia do reel narrado, antes da pagina de revisao.

Mede o que da para medir e monta o que precisa ser olhado:

  formato    1080 x 1920, 30 fps, H.264 yuv420p, SAR 1:1, audio AAC, +faststart
  volume     loudness integrado de -14 LUFS, com tolerancia de 0,5
  duracao    de 40 a 50 s (aviso, nao reprova)
  parado     nenhum trecho congelado por mais de 1 s (filtro freezedetect do ffmpeg)
  folhas     uma folha de contato por tomada, a 6 quadros por segundo, com as zonas
             reservadas desenhadas por cima (faixa da legenda, x 980, y 150 e y 1700),
             mais a tira dos primeiros 5 s. Quem conferiu OLHA cada folha.
  falas      conferencia/afirmacoes.md: cada frase da voz com as tomadas que estao na
             tela quando ela e dita, para conferir afirmacao por afirmacao contra a
             filmagem. Este arquivo e preenchido por quem conferiu, nao pelo script.

Uso:

    flow-reels narrado/conferir --projeto projetos/x --narrado 01
    flow-reels narrado/conferir --folha-da-fonte materiais-de-trabalho/fonte/filme.mp4 --saida folha.png

O segundo modo e a folha de contato da filmagem bruta, para escolher os momentos reais
antes de escrever o roteiro: 24 quadros com o instante e a regua em pixels da fonte.
"""

import argparse
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402

W, H, FPS = cm.LARGURA, cm.ALTURA, cm.FPS


def fonte_pequena(tamanho):
    for nome in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(nome, tamanho)
        except Exception:
            continue
    return ImageFont.load_default()


# ------------------------------------------------------------------- medidas

def atomos_de_topo(caminho):
    ordem = []
    with open(caminho, "rb") as f:
        while True:
            cab = f.read(8)
            if len(cab) < 8:
                break
            tamanho, tipo = struct.unpack(">I4s", cab)
            if tamanho == 1:
                tamanho = struct.unpack(">Q", f.read(8))[0]
                pulo = tamanho - 16
            elif tamanho == 0:
                ordem.append(tipo.decode("latin-1"))
                break
            else:
                pulo = tamanho - 8
            ordem.append(tipo.decode("latin-1"))
            f.seek(pulo, 1)
    return ordem


def trechos_parados(caminho, limite=1.0):
    r = subprocess.run(["ffmpeg", "-v", "info", "-nostats", "-i", str(caminho), "-map", "0:v:0",
                        "-vf", "freezedetect=n=0.003:d=%.2f" % limite, "-f", "null", "-"],
                       capture_output=True, text=True, errors="replace")
    inicios = [float(x) for x in re.findall(r"freeze_start:\s*([\d.]+)", r.stderr)]
    duracoes = [float(x) for x in re.findall(r"freeze_duration:\s*([\d.]+)", r.stderr)]
    saida = []
    for i, a in enumerate(inicios):
        d = duracoes[i] if i < len(duracoes) else None
        saida.append([round(a, 2), round(a + d, 2) if d else None])
    return saida


def conferir_formato(caminho):
    d = cm.sondar(caminho)
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), {})
    fr = v.get("r_frame_rate", "0/1").split("/")
    fps = float(fr[0]) / float(fr[1]) if len(fr) == 2 and float(fr[1]) else 0
    sar = v.get("sample_aspect_ratio", "1:1")
    atomos = atomos_de_topo(caminho)
    moov_antes = "moov" in atomos and "mdat" in atomos and atomos.index("moov") < atomos.index("mdat")
    itens = [
        ("tamanho 1080x1920", v.get("width") == W and v.get("height") == H, "%sx%s" % (v.get("width"), v.get("height"))),
        ("30 fps", abs(fps - 30) < 0.01, "%.2f" % fps),
        ("H.264", v.get("codec_name") == "h264", v.get("codec_name")),
        ("yuv420p", v.get("pix_fmt") == "yuv420p", v.get("pix_fmt")),
        ("SAR 1:1", sar in ("1:1", "0:1", None), sar),
        ("audio AAC", a.get("codec_name") == "aac", a.get("codec_name")),
        ("+faststart (moov antes do mdat)", moov_antes, " ".join(atomos)),
    ]
    return itens, float(d.get("format", {}).get("duration", 0) or 0)


# ------------------------------------------------------------------- folhas

def extrair(caminho, fps, largura, pasta):
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(caminho), "-vf", "fps=%g,scale=%d:-1" % (fps, largura),
                    str(pasta / "%05d.png")], check=True)
    return sorted(pasta.glob("*.png"))


def palavra_em(palavras, t):
    ditas = [p for p in palavras if p["inicio"] <= t <= p["fim"] + 0.25]
    return ditas[-1]["texto"] if ditas else ""


def folha(nome, quadros, t0, t1, palavras, destino, fps=6, colunas=10, largura=162):
    fs = quadros[int(round(t0 * fps)):int(round(t1 * fps))]
    if not fs:
        return None
    alt = largura * H // W
    k = largura / float(W)
    linhas = (len(fs) + colunas - 1) // colunas
    im = Image.new("RGB", (colunas * largura, linhas * (alt + 18) + 30), (18, 18, 18))
    d = ImageDraw.Draw(im)
    f1, f2 = fonte_pequena(13), fonte_pequena(18)
    d.text((6, 5), "%s  %.2f a %.2f s  a %d fps   vermelho: faixa da legenda   magenta: x 980   amarelo: y 150 e y 1700"
           % (nome, t0, t1, fps), fill=(255, 255, 0), font=f2)
    for i, f in enumerate(fs):
        t = (int(round(t0 * fps)) + i) / float(fps)
        x, y = (i % colunas) * largura, 30 + (i // colunas) * (alt + 18)
        im.paste(Image.open(f).convert("RGB"), (x, y))
        d.rectangle([x, y + int(cm.FAIXA_LEGENDA[0] * k), x + largura - 1, y + int(cm.FAIXA_LEGENDA[1] * k)],
                    outline=(255, 0, 0))
        d.line([x + int(cm.DIREITA_RESERVADA * k), y, x + int(cm.DIREITA_RESERVADA * k), y + alt], fill=(255, 0, 255))
        for yy in (cm.TOPO_RESERVADO, cm.BASE_RESERVADA):
            d.line([x, y + int(yy * k), x + largura - 1, y + int(yy * k)], fill=(255, 220, 0))
        d.text((x + 3, y + alt + 2), "%.2f %s" % (t, palavra_em(palavras, t)), fill=(230, 230, 230), font=f1)
    im.save(destino, quality=88)
    return destino


def tira_da_abertura(quadros, palavras, destino, fps=6):
    fs = quadros[:int(5 * fps)]
    if not fs:
        return None
    w, h = 216, 384
    im = Image.new("RGB", (8 * w, 4 * (h + 44)), (0, 0, 0))
    d = ImageDraw.Draw(im)
    f = fonte_pequena(18)
    for i, q in enumerate(fs):
        x, y = (i % 8) * w, (i // 8) * (h + 44)
        im.paste(Image.open(q).convert("RGB").resize((w, h)), (x, y))
        d.text((x + 6, y + h + 2), "%.2f" % (i / float(fps)), fill=(255, 220, 80), font=f)
        d.text((x + 6, y + h + 22), palavra_em(palavras, i / float(fps)), fill=(255, 255, 255), font=f)
    im.save(destino, quality=88)
    return destino


def folha_da_fonte(caminho, destino, n=24, colunas=4):
    dur = cm.duracao(caminho)
    tam = cm.tamanho_video(caminho)
    if not dur or not tam:
        cm.erro("nao consegui ler %s." % caminho)
    ow, oh = tam
    largura = 400
    alt = int(largura * oh / float(ow))
    k = largura / float(ow)
    linhas = (n + colunas - 1) // colunas
    im = Image.new("RGB", (colunas * largura, linhas * (alt + 22) + 30), (18, 18, 18))
    d = ImageDraw.Draw(im)
    f = fonte_pequena(15)
    d.text((6, 6), "%s  %.1f s  %dx%d   linhas da regua a cada 200 px da fonte" % (Path(caminho).name, dur, ow, oh),
           fill=(255, 255, 0), font=fonte_pequena(18))
    tmp = Path(tempfile.mkdtemp(prefix="fc-fonte-"))
    try:
        for i in range(n):
            t = dur * (i + 0.5) / n
            q = tmp / ("%03d.png" % i)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % t, "-i", str(caminho), "-frames:v", "1",
                            "-vf", "scale=%d:%d" % (largura, alt), str(q)])
            x, y = (i % colunas) * largura, 30 + (i // colunas) * (alt + 22)
            if q.is_file():
                im.paste(Image.open(q).convert("RGB"), (x, y))
            for gx in range(200, ow, 200):
                d.line([x + int(gx * k), y, x + int(gx * k), y + alt], fill=(255, 255, 0, 80))
            for gy in range(200, oh, 200):
                d.line([x, y + int(gy * k), x + largura - 1, y + int(gy * k)], fill=(255, 255, 0, 80))
            d.text((x + 4, y + alt + 3), "%.2f s" % t, fill=(230, 230, 230), font=f)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    im.save(destino, quality=88)
    cm.fala(str(destino))
    return 0


# ------------------------------------------------------------------- falas

def escrever_afirmacoes(cam, palavras, plano):
    destino = cam.conferencia / "afirmacoes.md"
    if destino.is_file():
        cm.fala("afirmacoes.md ja existe, deixei como esta: %s" % destino)
        return destino
    frases, atual = [], []
    for p in palavras:
        atual.append(p)
        if p["texto"].rstrip("\"'")[-1:] in ".?!\u2026":
            frases.append(atual)
            atual = []
    if atual:
        frases.append(atual)
    linhas = ["# Cada afirmação contra a filmagem", "",
              "Preencha as duas últimas colunas olhando as folhas de contato e a filmagem. "
              "Afirmação sem prova na tela, ou contra o que a tela mostra, sai do roteiro.", "",
              "| de | até | frase | tomadas na tela | o que a tela mostra | confere |", "|---|---|---|---|---|---|"]
    for fr in frases:
        a, b = fr[0]["inicio"], fr[-1]["fim"]
        ids = [t["id"] for t in plano.get("tomadas", []) if t["t0"] < b and t["t1"] > a]
        texto = " ".join(p["texto"] for p in fr).replace("|", "/")
        linhas.append("| %.2f | %.2f | %s | %s |  |  |" % (a, b, texto, ", ".join(ids)))
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return destino


# ------------------------------------------------------------------- principal

def conferir_reel(cam, arquivo):
    if not arquivo.is_file():
        cm.erro("nao achei %s." % arquivo)
    tl = cm.ler_json(cam.linha)
    plano = cm.ler_json(cam.plano) if cam.plano.is_file() else {"tomadas": []}
    palavras = tl["palavras"]
    cam.conferencia.mkdir(parents=True, exist_ok=True)

    itens, dur = conferir_formato(arquivo)
    lufs = cm.medir_loudness(arquivo)
    itens.append(("loudness -14 LUFS (+-0,5)", lufs is not None and abs(lufs + 14) <= 0.5,
                  "%.2f" % lufs if lufs is not None else "nao medido"))
    parados = trechos_parados(arquivo)
    itens.append(("nada parado por mais de 1 s", not parados, json.dumps(parados)))
    duracao_ok = 40.0 <= dur <= 50.0

    tmp = Path(tempfile.mkdtemp(prefix="fc-conferir-"))
    folhas = []
    try:
        quadros = extrair(arquivo, 6, 162, tmp)
        for t in plano.get("tomadas", []):
            fo = folha("tomada %s" % t["id"], quadros, t["t0"], t["t1"], palavras,
                       cam.conferencia / ("folha-%s.jpg" % t["id"]))
            if fo:
                folhas.append(str(fo))
        fe = plano.get("fechamento") or {}
        if fe.get("inicio"):
            fo = folha("fechamento", quadros, fe["inicio"], dur, palavras, cam.conferencia / "folha-fechamento.jpg")
            if fo:
                folhas.append(str(fo))
        tmp2 = Path(tempfile.mkdtemp(prefix="fc-tira-"))
        try:
            q30 = extrair(arquivo, 6, 216, tmp2)
            fo = tira_da_abertura(q30, palavras, cam.conferencia / "tira-0-5s.jpg")
            if fo:
                folhas.append(str(fo))
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    afirm = escrever_afirmacoes(cam, palavras, plano)

    aprovado = all(ok for _, ok, _ in itens)
    rel = {"arquivo": str(arquivo), "duracao": round(dur, 2), "duracao_no_alvo": duracao_ok,
           "loudness": lufs, "parados": parados, "congelados_no_compor": plano.get("congelados", {}),
           "itens": [{"item": n, "ok": ok, "valor": v} for n, ok, v in itens],
           "folhas": folhas, "afirmacoes": str(afirm), "aprovado_no_medido": aprovado}
    cm.gravar_json(cam.conferencia / "conferencia.json", rel)

    cm.fala("")
    cm.fala("conferencia de %s" % arquivo)
    for n, ok, v in itens:
        cm.fala("  %-9s %-36s %s" % ("ok" if ok else "REPROVADO", n, v))
    cm.fala("  %-9s %-36s %.2f s" % ("ok" if duracao_ok else "aviso", "duracao de 40 a 50 s", dur))
    cm.fala("")
    cm.fala("Olhe cada folha antes de chamar a pessoa (zonas reservadas, anel no lugar, credito em toda")
    cm.fala("tomada, legenda em uma linha) e preencha %s." % afirm)
    for f in folhas:
        cm.fala("  " + f)
    cm.fala("")
    cm.fala("medido: %s" % ("APROVADO" if aprovado else "REPROVADO"))
    return 0 if aprovado else 1


def principal(argv=None):
    an = argparse.ArgumentParser(description="Confere o reel narrado antes da revisao.")
    an.add_argument("--projeto", help="pasta do projeto")
    an.add_argument("--narrado", default="01", help="numero do reel narrado (padrao 01)")
    an.add_argument("--arquivo", default=None, help="o mp4 a conferir (padrao: a entrega)")
    an.add_argument("--folha-da-fonte", default=None, metavar="MIDIA",
                    help="so faz a folha de contato desta filmagem bruta")
    an.add_argument("--saida", default=None, help="com --folha-da-fonte: onde gravar a folha")
    an.add_argument("--n", type=int, default=24, help="com --folha-da-fonte: quantos quadros (padrao 24)")
    op = an.parse_args(argv)
    cm.exigir_ffmpeg()
    if op.folha_da_fonte:
        destino = op.saida or (Path(op.folha_da_fonte).with_suffix("").as_posix() + "-folha.jpg")
        return folha_da_fonte(op.folha_da_fonte, destino, op.n)
    if not op.projeto:
        an.print_help()
        return 2
    cam = cm.Caminhos(op.projeto, op.narrado)
    return conferir_reel(cam, Path(op.arquivo) if op.arquivo else cam.entrega)


if __name__ == "__main__":
    sys.exit(principal())
