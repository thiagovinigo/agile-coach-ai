#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
montar.py  ·  a montagem final do corte

Empilha o painel em cima e a face embaixo, queima a legenda por cima dos dois e
exporta o arquivo de entrega:

    1080 x 1920, 30 fps, H.264 yuv420p, faststart, SAR 1:1, audio AAC.

Uso:

    flow-reels produzir/montar --painel painel.mp4 --face face.mp4 --legenda legenda.ass \
                     --saida corte-01.mp4

    flow-reels produzir/montar --painel painel.mp4 --face face.mp4 --saida previa.mp4 \
                     --sem-legenda

A armadilha que este script existe para evitar
----------------------------------------------
No Windows, caminho absoluto dentro de um filtro do ffmpeg quebra o comando: o
"C:" e lido como separador de opcao e o ffmpeg reclama assim:

    [AVFilterGraph] No option name near 'C:/Users/.../marca/fontes'
    Error initializing filter 'subtitles'

Por isso o arquivo de legenda e a pasta de fontes entram no filtro em caminho
RELATIVO, com o processo rodando dentro da pasta da legenda. Quem cuida disso e
este script: ele faz o cd sozinho e monta o caminho relativo. Se voce for chamar
o ffmpeg na mao, faca o mesmo.

Se a pasta de fontes estiver em outro disco (e ai nao existe caminho relativo
possivel), o script copia os arquivos de fonte para uma pasta ao lado da legenda
e usa ela.

O que este script NAO faz, de proposito: grao.

O grao e aplicado pelo base.js quando o painel e montado no navegador, entao ele ja vem
queimado nos quadros que o painel.py captura. Adicionar uma camada aqui dobraria o grao do
painel e jogaria textura sintetica em cima da face, que e filmagem real. Se o grao parecer
ausente, meca o ruido de alta frequencia numa regiao chapada do painel antes de mexer:
num quadro correto ele fica perto de 3 niveis.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


LARGURA = 1080
ALTURA_PAINEL = 956
ALTURA_FACE = 964
ALTURA = ALTURA_PAINEL + ALTURA_FACE      # 1920
FPS = 30

NOME_SEGURO = re.compile(r"^[A-Za-z0-9._-]+$")


def exigir_ferramenta(nome):
    if shutil.which(nome) is None:
        print("erro: nao encontrei o %s no caminho do sistema." % nome)
        print("      Instale o ffmpeg e abra o terminal de novo. No Windows, o instalador")
        print("      precisa ter marcado a opcao de adicionar ao PATH.")
        raise SystemExit(1)


def exigir_arquivo(caminho, papel):
    if not caminho or not os.path.isfile(caminho):
        print("erro: nao encontrei o arquivo de %s em %s" % (papel, caminho))
        raise SystemExit(1)
    return os.path.abspath(caminho)


def sondar(caminho):
    """Devolve as propriedades de video e audio do arquivo, ou None."""
    comando = ["ffprobe", "-v", "error", "-print_format", "json",
               "-show_streams", "-show_format", caminho]
    try:
        bruto = subprocess.run(comando, capture_output=True, text=True, check=True).stdout
        return json.loads(bruto)
    except Exception:
        return None


def propriedades_de_video(dados):
    if not dados:
        return {}
    for fluxo in dados.get("streams", []):
        if fluxo.get("codec_type") == "video":
            return fluxo
    return {}


def tem_audio(dados):
    if not dados:
        return False
    return any(f.get("codec_type") == "audio" for f in dados.get("streams", []))


def duracao(dados):
    try:
        return float(dados["format"]["duration"])
    except Exception:
        return None


def caminho_relativo(destino, base):
    """Caminho relativo com barra normal, ou None quando nao existe."""
    try:
        relativo = os.path.relpath(destino, base)
    except ValueError:
        return None
    if ":" in relativo:
        return None
    return relativo.replace("\\", "/")


def preparar_fontes(pasta_fontes, pasta_trabalho):
    """Devolve o caminho relativo da pasta de fontes visto de dentro da pasta de trabalho."""
    if not pasta_fontes:
        return None, None
    pasta_fontes = os.path.abspath(pasta_fontes)
    if not os.path.isdir(pasta_fontes):
        print("aviso: a pasta de fontes %s nao existe. A legenda vai sair com a fonte do sistema."
              % pasta_fontes)
        return None, None

    relativo = caminho_relativo(pasta_fontes, pasta_trabalho)
    if relativo:
        return relativo, None

    copia = os.path.join(pasta_trabalho, "_fontes-da-legenda")
    os.makedirs(copia, exist_ok=True)
    for nome in os.listdir(pasta_fontes):
        if nome.lower().endswith((".ttf", ".otf", ".ttc")):
            shutil.copy2(os.path.join(pasta_fontes, nome), os.path.join(copia, nome))
    print("aviso: a pasta de fontes esta em outro disco, entao copiei as fontes para %s" % copia)
    return "_fontes-da-legenda", copia


def montar(opcoes):
    painel = exigir_arquivo(opcoes.painel, "painel")
    face = exigir_arquivo(opcoes.face, "face")
    saida = os.path.abspath(opcoes.saida)
    os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)

    dados_painel = sondar(painel)
    dados_face = sondar(face)
    conferir_entradas(dados_painel, dados_face)

    legenda = None
    if not opcoes.sem_legenda:
        legenda = exigir_arquivo(opcoes.legenda, "legenda") if opcoes.legenda else None
        if legenda is None:
            print("erro: diga --legenda caminho.ass, ou use --sem-legenda para montar sem ela.")
            raise SystemExit(1)

    # A pasta de trabalho e a pasta da legenda. E de dentro dela que o ffmpeg roda,
    # e e por isso que todo caminho do filtro fica relativo e curto.
    pasta_trabalho = os.path.dirname(legenda) if legenda else os.path.dirname(saida)
    pasta_trabalho = pasta_trabalho or os.getcwd()

    temporarios = []
    nome_legenda = None
    if legenda:
        nome_legenda = os.path.basename(legenda)
        if not NOME_SEGURO.match(nome_legenda):
            # Nome com espaco, acento ou colchete tambem confunde o filtro.
            nome_legenda = "_legenda-para-queimar.ass"
            destino = os.path.join(pasta_trabalho, nome_legenda)
            shutil.copy2(legenda, destino)
            temporarios.append(destino)

    pasta_relativa, copia_fontes = preparar_fontes(opcoes.fontes, pasta_trabalho)

    filtro = (
        "[0:v]scale=%d:%d:out_range=tv,setsar=1,setrange=tv[cima];"
        "[1:v]scale=%d:%d:out_range=tv,setsar=1,setrange=tv[baixo];"
        "[cima][baixo]vstack=inputs=2:shortest=1[empilhado]"
        % (LARGURA, ALTURA_PAINEL, LARGURA, ALTURA_FACE)
    )
    if nome_legenda:
        queima = "subtitles=%s" % nome_legenda
        if pasta_relativa:
            queima += ":fontsdir=%s" % pasta_relativa
        filtro += ";[empilhado]%s,format=yuv420p[final]" % queima
        rotulo = "[final]"
    else:
        filtro += ";[empilhado]format=yuv420p[final]"
        rotulo = "[final]"

    comando = [
        "ffmpeg", "-y",
        "-i", painel,
        "-i", face,
        "-filter_complex", filtro,
        "-map", rotulo,
    ]
    if tem_audio(dados_face):
        comando += ["-map", "1:a:0", "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    else:
        print("aviso: a face nao tem audio, entao o corte vai sair mudo.")
    comando += [
        "-r", str(FPS),
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level", "4.1",
        "-preset", opcoes.preset,
        "-crf", str(opcoes.crf),
        "-pix_fmt", "yuv420p",
        "-color_range", "tv", "-colorspace", "bt709",
        "-color_primaries", "bt709", "-color_trc", "bt709",
        "-movflags", "+faststart",
        "-shortest",
        saida,
    ]

    print("montando o corte. Isso leva perto de 1 a 2 minutos para 40 segundos de video.")
    print("pasta de trabalho: %s" % pasta_trabalho)
    print("filtro: %s" % filtro)

    resultado = subprocess.run(comando, cwd=pasta_trabalho,
                               capture_output=True, text=True, errors="replace")

    for caminho in temporarios:
        try:
            os.remove(caminho)
        except OSError:
            pass
    if copia_fontes and not opcoes.guardar_fontes:
        shutil.rmtree(copia_fontes, ignore_errors=True)

    if resultado.returncode != 0:
        print("\nerro: o ffmpeg parou. As ultimas linhas dele:\n")
        print("\n".join(resultado.stderr.strip().splitlines()[-18:]))
        if "No option name near" in resultado.stderr:
            print("\nEsse erro e a armadilha do caminho absoluto no filtro. Confira se a legenda")
            print("e a pasta de fontes estao no mesmo disco da pasta de trabalho.")
        raise SystemExit(1)

    return saida


def conferir_entradas(dados_painel, dados_face):
    painel = propriedades_de_video(dados_painel)
    face = propriedades_de_video(dados_face)

    if painel and (painel.get("width"), painel.get("height")) != (LARGURA, ALTURA_PAINEL):
        print("aviso: o painel esta em %sx%s e o padrao e %dx%d. Vou redimensionar, mas o certo"
              % (painel.get("width"), painel.get("height"), LARGURA, ALTURA_PAINEL))
        print("       e renderizar ele ja no tamanho, senao o texto sai borrado.")
    if face and (face.get("width"), face.get("height")) != (LARGURA, ALTURA_FACE):
        print("aviso: a face esta em %sx%s e o padrao e %dx%d. Vou redimensionar, mas o certo"
              % (face.get("width"), face.get("height"), LARGURA, ALTURA_FACE))
        print("       e recortar ela nesse tamanho com o enquadrar.py.")

    dp = duracao(dados_painel)
    df = duracao(dados_face)
    if dp and df and abs(dp - df) > 0.25:
        print("aviso: painel com %.2f s e face com %.2f s. O corte vai terminar no mais curto."
              % (dp, df))
        print("       Se a diferenca for grande, o painel foi renderizado com a duracao errada.")


def conferir_saida(caminho):
    dados = sondar(caminho)
    fluxo = propriedades_de_video(dados)
    if not fluxo:
        print("erro: o arquivo saiu, mas o ffprobe nao achou video dentro dele.")
        return False

    largura = fluxo.get("width")
    altura = fluxo.get("height")
    sar = fluxo.get("sample_aspect_ratio", "1:1")
    dar = fluxo.get("display_aspect_ratio", "?")
    taxa = fluxo.get("avg_frame_rate", "0/0")
    try:
        numerador, denominador = (float(x) for x in taxa.split("/"))
        fps = numerador / denominador if denominador else 0
    except Exception:
        fps = 0

    tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)

    print("\nconferencia do arquivo entregue")
    print("  caminho ........ %s" % caminho)
    print("  resolucao ...... %sx%s" % (largura, altura))
    print("  fps ............ %.2f" % fps)
    print("  codec .......... %s / %s" % (fluxo.get("codec_name"), fluxo.get("pix_fmt")))
    print("  perfil ......... %s" % fluxo.get("profile"))
    print("  SAR / DAR ...... %s / %s" % (sar, dar))
    print("  duracao ........ %.2f s" % (duracao(dados) or 0))
    print("  tamanho ........ %.1f MB" % tamanho_mb)
    print("  audio .......... %s" % ("sim" if tem_audio(dados) else "nao"))

    problemas = []
    if (largura, altura) != (LARGURA, ALTURA):
        problemas.append("a resolucao nao e %dx%d" % (LARGURA, ALTURA))
    if sar not in ("1:1", "0:1", None):
        problemas.append("o SAR nao e 1:1")
    if fluxo.get("pix_fmt") != "yuv420p":
        problemas.append("o formato de pixel nao e yuv420p")
    if abs(fps - FPS) > 0.2:
        problemas.append("a taxa nao e %d fps" % FPS)

    with open(caminho, "rb") as arquivo:
        cabeca = arquivo.read(4096)
    if b"moov" not in cabeca:
        problemas.append("o indice moov nao esta no comeco, entao o faststart falhou")

    if problemas:
        print("\n  REPROVADO: %s" % "; ".join(problemas))
        return False
    print("\n  aprovado no formato de entrega.")
    return True


def principal(argv=None):
    analisador = argparse.ArgumentParser(
        description="Empilha painel e face, queima a legenda e exporta o corte final.")
    analisador.add_argument("--painel", help="MP4 do painel de cima, 1080x956")
    analisador.add_argument("--face", help="MP4 da face ja recortada, 1080x964")
    analisador.add_argument("--legenda", help="arquivo .ass gerado pelo legenda.py")
    analisador.add_argument("--saida", help="caminho do MP4 final")
    analisador.add_argument("--fontes", default=None,
                            help="pasta com os .ttf usados na legenda (normalmente marca/fontes/ do pacote)")
    analisador.add_argument("--sem-legenda", action="store_true",
                            help="monta so o empilhamento, para conferir enquadramento")
    analisador.add_argument("--crf", type=int, default=18, help="qualidade do H.264 (padrao: 18)")
    analisador.add_argument("--preset", default="medium", help="preset do x264 (padrao: medium)")
    analisador.add_argument("--guardar-fontes", action="store_true",
                            help="nao apaga a copia de fontes feita quando o disco e outro")

    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        analisador.print_help()
        print("\nFaltou dizer o que montar. O minimo e --painel, --face, --legenda e --saida.")
        return 2

    opcoes = analisador.parse_args(argv)
    faltando = [nome for nome in ("painel", "face", "saida") if not getattr(opcoes, nome)]
    if faltando:
        print("erro: faltou %s." % ", ".join("--" + f for f in faltando))
        return 1

    exigir_ferramenta("ffmpeg")
    exigir_ferramenta("ffprobe")

    caminho = montar(opcoes)
    return 0 if conferir_saida(caminho) else 1


if __name__ == "__main__":
    sys.exit(principal())
