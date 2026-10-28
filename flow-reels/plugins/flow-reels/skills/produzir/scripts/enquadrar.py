#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enquadrar.py  ·  achar a face e conferir o recorte, olhando

O painel de baixo tem 1080 x 964 e recebe o rosto de quem fala. Este script nao
adivinha nada: ele produz imagem para o agente OLHAR e decidir, que e o caminho
que funciona porque webcam em canto de tela e busto em tripe nao se mexem
durante a gravacao. Caixa fixa, decidida uma vez, conferida uma vez.

Sao duas funcoes:

  amostrar   pega N instantes do video, desenha uma grade por cima de cada um e
             junta tudo numa folha de contato. Olhando essa folha, o agente
             escreve a caixa de recorte em pixels do video original.

  validar    recebe a caixa escolhida, recorta varios instantes DO CORTE, escala
             para 1080 x 964 e junta numa segunda folha de contato. E aqui que
             se ve se o queixo ficou de fora ou se a pessoa saiu de quadro. So
             depois disso vale renderizar o corte inteiro.

Uso:

    flow-reels produzir/enquadrar amostrar --video aula.mp4 --saida contato.png
    flow-reels produzir/enquadrar amostrar --video aula.mp4 --saida contato.png --n 12 --colunas 4

    flow-reels produzir/enquadrar validar --video aula.mp4 --caixa 760:120:1080:964 \
                        --saida contato-recorte.png --inicio 12.4 --fim 58.2

A caixa e escrita como  x:y:largura:altura , em pixels do video original, com x
e y no canto de cima e da esquerda.

Caminho opcional, para rosto que se mexe
----------------------------------------
Quando a pessoa anda pelo quadro, caixa fixa nao resolve, e ai entra deteccao de
rosto quadro a quadro com OpenCV, suavizada para a camera nao tremer. Esse
caminho NAO vem instalado com o pacote, de proposito: ele traz uma dependencia
grande, e a esmagadora maioria dos videos de canal e busto parado ou webcam em
canto. Se voce precisar dele, instale com

    python -m pip install opencv-python

e fale com o agente: a receita de suavizacao esta em
referencias/RECEITA-TECNICA.md, na secao do enquadramento.
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


LARGURA_FACE = 1080
ALTURA_FACE = 964
PROPORCAO_FACE = LARGURA_FACE / float(ALTURA_FACE)   # 1,1203

DIVISOES = 8          # a grade da folha de contato


def exigir_ferramenta(nome):
    if shutil.which(nome) is None:
        print("erro: nao encontrei o %s no caminho do sistema. Instale o ffmpeg e tente de novo."
              % nome)
        raise SystemExit(1)


def sondar(caminho):
    comando = ["ffprobe", "-v", "error", "-print_format", "json",
               "-show_streams", "-show_format", caminho]
    try:
        bruto = subprocess.run(comando, capture_output=True, text=True, check=True).stdout
        dados = json.loads(bruto)
    except Exception:
        print("erro: o ffprobe nao conseguiu ler %s" % caminho)
        raise SystemExit(1)

    video = next((f for f in dados.get("streams", []) if f.get("codec_type") == "video"), None)
    if not video:
        print("erro: nao achei fluxo de video em %s" % caminho)
        raise SystemExit(1)
    try:
        duracao = float(dados["format"]["duration"])
    except Exception:
        duracao = 0.0
    return int(video["width"]), int(video["height"]), duracao


def instantes(inicio, fim, quantidade):
    """Reparte o intervalo em N instantes, fugindo das pontas."""
    faixa = fim - inicio
    if faixa <= 0:
        return [inicio] * quantidade
    passo = faixa / float(quantidade + 1)
    return [inicio + passo * (i + 1) for i in range(quantidade)]


def extrair(video, tempo, destino, filtro):
    comando = ["ffmpeg", "-y", "-ss", "%.3f" % tempo, "-i", video,
               "-frames:v", "1", "-vf", filtro, "-q:v", "2", destino]
    resultado = subprocess.run(comando, capture_output=True, text=True, errors="replace")
    if resultado.returncode != 0 or not os.path.isfile(destino):
        print("erro: nao consegui extrair o quadro do segundo %.2f." % tempo)
        print("\n".join(resultado.stderr.strip().splitlines()[-8:]))
        raise SystemExit(1)


def juntar_folha(pasta, quantidade, colunas, saida):
    linhas = int(math.ceil(quantidade / float(colunas)))
    comando = ["ffmpeg", "-y", "-framerate", "1", "-i", os.path.join(pasta, "c%03d.png"),
               "-frames:v", "1",
               "-vf", "tile=%dx%d:margin=8:padding=8:color=0x101014" % (colunas, linhas),
               saida]
    resultado = subprocess.run(comando, capture_output=True, text=True, errors="replace")
    if resultado.returncode != 0 or not os.path.isfile(saida):
        print("erro: nao consegui montar a folha de contato.")
        print("\n".join(resultado.stderr.strip().splitlines()[-10:]))
        raise SystemExit(1)


def tabela_da_grade(largura, altura):
    passo_x = largura / float(DIVISOES)
    passo_y = altura / float(DIVISOES)
    linhas = ["  a grade tem %d colunas de %.0f px e %d linhas de %.0f px."
              % (DIVISOES, passo_x, DIVISOES, passo_y),
              "  colunas (x):  " + "  ".join("%d=%.0f" % (i, i * passo_x) for i in range(DIVISOES + 1)),
              "  linhas  (y):  " + "  ".join("%d=%.0f" % (i, i * passo_y) for i in range(DIVISOES + 1))]
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# amostrar
# ---------------------------------------------------------------------------

def amostrar(opcoes):
    video = os.path.abspath(opcoes.video)
    if not os.path.isfile(video):
        print("erro: nao encontrei o video em %s" % video)
        return 1

    largura, altura, duracao = sondar(video)
    inicio = opcoes.inicio if opcoes.inicio is not None else 0.0
    fim = opcoes.fim if opcoes.fim is not None else (duracao or 60.0)
    if fim <= inicio:
        print("erro: o fim precisa ser maior que o inicio.")
        return 1

    tempos = instantes(inicio, fim, opcoes.n)
    celula = opcoes.largura_celula

    # Duas grades: a fina de oitavos e a grossa de metades, que da o centro.
    filtro = ("drawgrid=w=iw/%d:h=ih/%d:t=2:c=white@0.45,"
              "drawgrid=w=iw/2:h=ih/2:t=5:c=white@0.85,"
              "scale=%d:-2" % (DIVISOES, DIVISOES, celula))

    pasta = tempfile.mkdtemp(prefix="fc-amostra-")
    try:
        for indice, tempo in enumerate(tempos):
            extrair(video, tempo, os.path.join(pasta, "c%03d.png" % indice), filtro)
        saida = os.path.abspath(opcoes.saida)
        os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)
        juntar_folha(pasta, len(tempos), opcoes.colunas, saida)
    finally:
        shutil.rmtree(pasta, ignore_errors=True)

    print("folha de contato em %s" % saida)
    print("  video ..... %dx%d, %.1f s" % (largura, altura, duracao))
    print("  amostras .. %d, de %.1f s a %.1f s, lidas da esquerda para a direita e de cima para baixo:"
          % (len(tempos), inicio, fim))
    print("              " + "  ".join("%.1f s" % t for t in tempos))
    print(tabela_da_grade(largura, altura))
    print("")
    print("Agora OLHE a folha e escreva a caixa de recorte em pixels do video original,")
    print("no formato x:y:largura:altura. Tres coisas a respeitar:")
    print("  1. a proporcao da caixa e 1080 por 964, ou seja largura = altura x %.4f;" % PROPORCAO_FACE)
    print("  2. os olhos ficam perto do terco de cima da caixa, e sobra ar acima da cabeca;")
    print("  3. a caixa cabe dentro de %dx%d, sem passar da borda." % (largura, altura))
    print("")
    print("Sugestao de caixa no tamanho maximo possivel: %s" % caixa_sugerida(largura, altura))
    print("Depois confira com:  flow-reels produzir/enquadrar validar --video ... --caixa ... --saida ...")
    return 0


def caixa_sugerida(largura, altura):
    """A maior caixa na proporcao da face, centrada, que cabe no quadro."""
    if largura / float(altura) > PROPORCAO_FACE:
        a = altura
        l = int(round(a * PROPORCAO_FACE))
    else:
        l = largura
        a = int(round(l / PROPORCAO_FACE))
    x = (largura - l) // 2
    y = (altura - a) // 2
    return "%d:%d:%d:%d" % (x, y, l, a)


# ---------------------------------------------------------------------------
# validar
# ---------------------------------------------------------------------------

def ler_caixa(texto):
    partes = texto.split(":")
    if len(partes) != 4:
        print("erro: a caixa '%s' nao esta no formato x:y:largura:altura." % texto)
        raise SystemExit(1)
    try:
        return [int(round(float(p))) for p in partes]
    except ValueError:
        print("erro: a caixa '%s' tem numero invalido." % texto)
        raise SystemExit(1)


def validar(opcoes):
    video = os.path.abspath(opcoes.video)
    if not os.path.isfile(video):
        print("erro: nao encontrei o video em %s" % video)
        return 1

    largura, altura, duracao = sondar(video)
    x, y, l, a = ler_caixa(opcoes.caixa)

    problemas = []
    if x < 0 or y < 0 or x + l > largura or y + a > altura:
        problemas.append("a caixa passa da borda do video, que tem %dx%d" % (largura, altura))
    proporcao = l / float(a)
    if abs(proporcao - PROPORCAO_FACE) > 0.01:
        altura_certa = int(round(l / PROPORCAO_FACE))
        largura_certa = int(round(a * PROPORCAO_FACE))
        problemas.append(
            "a proporcao esta em %.4f e precisa ser %.4f. Para a mesma largura use altura %d, "
            "ou para a mesma altura use largura %d" % (proporcao, PROPORCAO_FACE, altura_certa, largura_certa))
    if l < LARGURA_FACE:
        problemas.append("a caixa tem %d px de largura e o destino tem %d, entao a imagem vai "
                         "esticar e perder nitidez" % (l, LARGURA_FACE))

    for problema in problemas:
        print("aviso: %s." % problema)

    inicio = opcoes.inicio if opcoes.inicio is not None else 0.0
    fim = opcoes.fim if opcoes.fim is not None else (duracao or 60.0)
    if fim <= inicio:
        print("erro: o fim precisa ser maior que o inicio.")
        return 1

    tempos = instantes(inicio, fim, opcoes.n)
    filtro = ("crop=%d:%d:%d:%d,scale=%d:%d,setsar=1,scale=%d:-2"
              % (l, a, x, y, LARGURA_FACE, ALTURA_FACE, opcoes.largura_celula))

    pasta = tempfile.mkdtemp(prefix="fc-recorte-")
    try:
        for indice, tempo in enumerate(tempos):
            extrair(video, tempo, os.path.join(pasta, "c%03d.png" % indice), filtro)
        saida = os.path.abspath(opcoes.saida)
        os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)
        juntar_folha(pasta, len(tempos), opcoes.colunas, saida)
    finally:
        shutil.rmtree(pasta, ignore_errors=True)

    print("folha do recorte em %s" % saida)
    print("  caixa ..... x=%d y=%d largura=%d altura=%d  (proporcao %.4f)" % (x, y, l, a, proporcao))
    print("  amostras .. %d, de %.1f s a %.1f s:" % (len(tempos), inicio, fim))
    print("              " + "  ".join("%.1f s" % t for t in tempos))
    print("")
    print("OLHE a folha antes de renderizar. Reprovado se, em qualquer amostra,")
    print("o queixo ou o topo da cabeca ficaram cortados, a pessoa saiu do quadro,")
    print("ou sobrou muito teto vazio acima da cabeca.")
    print("")
    print("Aprovou? Entao o recorte da face do corte sai com:")
    print("")
    print("  ffmpeg -y -ss %.3f -to %.3f -i \"%s\" \\" % (inicio, fim, video))
    print("    -vf \"crop=%d:%d:%d:%d,scale=%d:%d,setsar=1,fps=30\" \\" % (l, a, x, y, LARGURA_FACE, ALTURA_FACE))
    print("    -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p \\")
    print("    -c:a aac -b:a 192k face.mp4")
    print("")
    print("Corte costurado de varios trechos: rode um comando desses por trecho e junte com")
    print("o concat do ffmpeg. A receita completa esta em referencias/RECEITA-TECNICA.md.")
    return 0


# ---------------------------------------------------------------------------
# Linha de comando
# ---------------------------------------------------------------------------

def principal(argv=None):
    analisador = argparse.ArgumentParser(
        description="Acha a face por amostragem e confere o recorte antes de renderizar.")
    sub = analisador.add_subparsers(dest="funcao")

    a = sub.add_parser("amostrar", help="folha de contato com grade, para escolher a caixa")
    a.add_argument("--video", required=True, help="o video de origem")
    a.add_argument("--saida", required=True, help="PNG da folha de contato")
    a.add_argument("--n", type=int, default=9, help="quantas amostras (padrao: 9)")
    a.add_argument("--colunas", type=int, default=3, help="colunas da folha (padrao: 3)")
    a.add_argument("--inicio", type=float, default=None, help="segundo inicial")
    a.add_argument("--fim", type=float, default=None, help="segundo final")
    a.add_argument("--largura-celula", type=int, default=480, help="largura de cada amostra em px")

    v = sub.add_parser("validar", help="folha de contato ja recortada, para aprovar a caixa")
    v.add_argument("--video", required=True, help="o video de origem")
    v.add_argument("--caixa", required=True, metavar="X:Y:LARGURA:ALTURA",
                   help="a caixa de recorte em pixels do video original")
    v.add_argument("--saida", required=True, help="PNG da folha de contato recortada")
    v.add_argument("--n", type=int, default=6, help="quantas amostras (padrao: 6)")
    v.add_argument("--colunas", type=int, default=3, help="colunas da folha (padrao: 3)")
    v.add_argument("--inicio", type=float, default=None, help="inicio do corte, em segundos")
    v.add_argument("--fim", type=float, default=None, help="fim do corte, em segundos")
    v.add_argument("--largura-celula", type=int, default=360, help="largura de cada amostra em px")

    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        analisador.print_help()
        print("\nFaltou dizer o que fazer. Comece por:")
        print("  flow-reels produzir/enquadrar amostrar --video seu-video.mp4 --saida contato.png")
        return 2

    opcoes = analisador.parse_args(argv)
    if not opcoes.funcao:
        analisador.print_help()
        return 2

    exigir_ferramenta("ffmpeg")
    exigir_ferramenta("ffprobe")

    if opcoes.funcao == "amostrar":
        return amostrar(opcoes)
    return validar(opcoes)


if __name__ == "__main__":
    sys.exit(principal())
