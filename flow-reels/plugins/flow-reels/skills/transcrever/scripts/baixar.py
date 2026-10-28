# -*- coding: utf-8 -*-
"""Traz o video para dentro do projeto.

Aceita tres tipos de link:

  YouTube            usa o yt-dlp, que baixa ate 1080p em mp4
  Google Drive       link de arquivo (/file/d/ID/view ou ?id=ID), publico ou com link aberto
  link direto        qualquer URL que devolva o arquivo de video ou audio

Uso:

    flow-reels transcrever/baixar --url https://www.youtube.com/watch?v=xxxx --projeto projetos/aula
    flow-reels transcrever/baixar --url https://drive.google.com/file/d/ID/view --projeto projetos/aula

O arquivo cai em <projeto>/materiais-de-trabalho/fonte/ e o caminho dele e a ultima
linha impressa, para
quem chamou poder passar direto para o replicate.py ou o local.py.

Se o yt-dlp nao estiver instalado, o script diz como instalar em vez de quebrar.
Vale so para conteudo que voce tem direito de baixar.
"""

import argparse
import http.cookiejar
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import normalizar as nz  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


NAVEGADOR = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

COMO_INSTALAR_YTDLP = (
    "o yt-dlp não está instalado, e é ele que baixa do YouTube.\n\n"
    "  Escolha um destes:\n"
    "    pip install yt-dlp\n"
    "    uv tool install yt-dlp\n"
    "    winget install yt-dlp.yt-dlp          (Windows)\n"
    "    brew install yt-dlp                   (macOS)\n\n"
    "  Se você preferir não instalar nada, baixe o vídeo na mão e passe o caminho\n"
    "  do arquivo direto para a transcrição."
)


# ------------------------------------------------------------- identificacao

def tipo_do_link(url):
    endereco = url.lower()
    if "youtube.com" in endereco or "youtu.be" in endereco:
        return "youtube"
    if "drive.google.com" in endereco or "docs.google.com" in endereco:
        return "drive"
    return "direto"


def id_do_drive(url):
    for padrao in (r"/file/d/([A-Za-z0-9_-]{10,})",
                   r"[?&]id=([A-Za-z0-9_-]{10,})",
                   r"/d/([A-Za-z0-9_-]{10,})"):
        achado = re.search(padrao, url)
        if achado:
            return achado.group(1)
    return None


def achar_ytdlp():
    """Devolve o comando base do yt-dlp, ou None se nao achar de jeito nenhum."""
    caminho = shutil.which("yt-dlp")
    if caminho:
        return [caminho]
    try:
        subprocess.run([sys.executable, "-m", "yt_dlp", "--version"],
                       capture_output=True, check=True)
        return [sys.executable, "-m", "yt_dlp"]
    except Exception:
        pass
    if shutil.which("uv"):
        try:
            subprocess.run(["uv", "tool", "run", "yt-dlp", "--version"],
                           capture_output=True, check=True, timeout=120)
            return ["uv", "tool", "run", "yt-dlp"]
        except Exception:
            pass
    return None


# ------------------------------------------------------------------ youtube

def baixar_do_youtube(url, destino, apenas_audio):
    comando_base = achar_ytdlp()
    if not comando_base:
        nz.erro(COMO_INSTALAR_YTDLP, codigo=3)

    modelo_de_nome = str(destino / "%(title).80s.%(ext)s")
    comando = list(comando_base) + [
        "--no-playlist",
        "--restrict-filenames",
        "--no-warnings",
        "--progress",
        "-o", modelo_de_nome,
        "--print", "after_move:filepath",
    ]
    if apenas_audio:
        comando += ["-f", "bestaudio/best", "-x", "--audio-format", "m4a"]
    else:
        comando += [
            "-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b",
            "--merge-output-format", "mp4",
        ]
    comando.append(url)

    print("  Baixando do YouTube...")
    resultado = subprocess.run(comando, capture_output=True, text=True)
    if resultado.returncode != 0:
        saida = (resultado.stderr or resultado.stdout or "").strip()[-800:]
        if "Private video" in saida or "Sign in" in saida:
            nz.erro("esse vídeo é privado ou pede login. Baixe pela sua conta e passe o "
                    "caminho do arquivo.", 4)
        if "Video unavailable" in saida:
            nz.erro("o YouTube diz que o vídeo não está disponível. Confira o link.", 4)
        nz.erro("o yt-dlp falhou.\n  %s" % saida, 4)

    caminhos = [linha.strip() for linha in resultado.stdout.splitlines()
                if linha.strip() and Path(linha.strip()).exists()]
    if caminhos:
        return Path(caminhos[-1])

    recentes = sorted(destino.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if recentes:
        return recentes[0]
    nz.erro("o yt-dlp terminou sem erro mas eu não achei o arquivo em %s." % destino, 4)


# -------------------------------------------------------------------- drive

def nome_do_cabecalho(resposta, reserva):
    disposicao = resposta.headers.get("Content-Disposition", "")
    achado = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', disposicao)
    if achado:
        return urllib.parse.unquote(achado.group(1)).strip()
    return reserva


def escrever_do_fluxo(resposta, destino):
    total = int(resposta.headers.get("Content-Length") or 0)
    baixado = 0
    marco = 0
    with open(destino, "wb") as saida:
        while True:
            pedaco = resposta.read(1024 * 256)
            if not pedaco:
                break
            saida.write(pedaco)
            baixado += len(pedaco)
            if total:
                porcento = int(baixado * 100 / total)
                if porcento >= marco + 10:
                    marco = porcento - (porcento % 10)
                    print("    %d%%" % marco)
    return destino


def baixar_do_drive(url, destino):
    identificador = id_do_drive(url)
    if not identificador:
        if "/folders/" in url:
            nz.erro("esse link é de uma pasta do Drive, e eu preciso do link de um arquivo.\n"
                    "  Abra a pasta, clique no vídeo, copie o link dele e tente de novo.", 4)
        nz.erro("não consegui achar o id do arquivo nesse link do Drive.\n"
                "  O formato esperado é https://drive.google.com/file/d/ID/view", 4)

    cookies = http.cookiejar.CookieJar()
    abridor = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))
    abridor.addheaders = [("User-Agent", NAVEGADOR)]

    endereco = "https://drive.usercontent.google.com/download?id=%s&export=download" % identificador
    print("  Baixando do Google Drive...")
    resposta = abridor.open(endereco, timeout=120)
    tipo = (resposta.headers.get("Content-Type") or "").lower()

    # arquivo grande: o Drive devolve uma pagina de confirmacao em vez do arquivo
    if "text/html" in tipo:
        pagina = resposta.read().decode("utf-8", errors="ignore")
        campos = dict(re.findall(r'name="([^"]+)"\s+value="([^"]*)"', pagina))
        if not campos.get("confirm"):
            achado = re.search(r"confirm=([0-9A-Za-z_-]+)", pagina)
            if achado:
                campos["confirm"] = achado.group(1)
        if not campos:
            nz.erro("o Drive respondeu com uma página em vez do arquivo.\n"
                    "  Normalmente é permissão: o arquivo precisa estar com link aberto.\n"
                    "  Abra o compartilhamento, deixe como qualquer pessoa com o link, ou\n"
                    "  baixe na mão e passe o caminho do arquivo.", 4)
        campos.setdefault("id", identificador)
        campos.setdefault("export", "download")
        endereco = "https://drive.usercontent.google.com/download?" + urllib.parse.urlencode(campos)
        resposta = abridor.open(endereco, timeout=120)
        tipo = (resposta.headers.get("Content-Type") or "").lower()
        if "text/html" in tipo:
            nz.erro("o Drive continuou devolvendo página em vez do arquivo.\n"
                    "  Confira se o arquivo está com o link aberto, ou baixe na mão.", 4)

    nome = nome_do_cabecalho(resposta, "drive-%s.mp4" % identificador)
    caminho = destino / nome
    escrever_do_fluxo(resposta, caminho)
    return caminho


# -------------------------------------------------------------- link direto

def baixar_direto(url, destino):
    print("  Baixando o arquivo...")
    requisicao = urllib.request.Request(url, headers={"User-Agent": NAVEGADOR})
    try:
        resposta = urllib.request.urlopen(requisicao, timeout=120)
    except Exception as e:
        nz.erro("não consegui baixar esse link (%s)." % e, 4)

    reserva = Path(urllib.parse.urlparse(url).path).name or "video.mp4"
    nome = nome_do_cabecalho(resposta, reserva)
    caminho = destino / nome
    escrever_do_fluxo(resposta, caminho)
    return caminho


# ---------------------------------------------------------------------- cli

def main():
    parser = argparse.ArgumentParser(
        description="Baixa o vídeo de um link do YouTube, do Google Drive ou de uma URL direta.",
        epilog="Exemplo: flow-reels transcrever/baixar --url https://youtu.be/xxxx --projeto projetos/aula",
    )
    parser.add_argument("--url", required=True, help="o link do vídeo")
    parser.add_argument("--projeto", required=True,
                        help="diretório do projeto. O arquivo cai em "
                             "<projeto>/materiais-de-trabalho/fonte/")
    parser.add_argument("--apenas-audio", action="store_true",
                        help="baixa só o áudio, que basta para transcrever e é muito mais leve")

    if len(sys.argv) == 1:
        parser.print_help()
        print("\nEste script só traz o arquivo para dentro do projeto. Quem transcreve é o\n"
              "replicate.py (nuvem) ou o local.py (na sua máquina), na mesma pasta.\n")
        sys.exit(2)

    args = parser.parse_args()

    # O video de origem e material de trabalho: cai debaixo do teto de
    # materiais-de-trabalho/, e nao na raiz da pasta do video.
    destino = nz.pasta_fonte(args.projeto)
    destino.mkdir(parents=True, exist_ok=True)

    tipo = tipo_do_link(args.url)
    if tipo == "youtube":
        caminho = baixar_do_youtube(args.url, destino, args.apenas_audio)
    elif tipo == "drive":
        caminho = baixar_do_drive(args.url, destino)
    else:
        caminho = baixar_direto(args.url, destino)

    if not caminho or not Path(caminho).exists():
        nz.erro("o download terminou mas o arquivo não apareceu em %s." % destino, 4)

    caminho = Path(caminho).resolve()
    tamanho = caminho.stat().st_size / (1024 * 1024)
    duracao = nz.duracao_do_arquivo(caminho)

    print("")
    print("Baixado.")
    print("  arquivo ..... %s" % caminho.name)
    print("  tamanho ..... %.1f MB" % tamanho)
    if duracao:
        print("  duração ..... %s" % nz.mmss(duracao))
    print("")
    print(caminho)


if __name__ == "__main__":
    main()
