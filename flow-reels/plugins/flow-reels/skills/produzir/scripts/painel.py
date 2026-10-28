#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
painel.py  ·  o renderizador do painel de cima

Abre o painel.html num navegador sem tela, em 1080 x 956, e pede um quadro por
vez: chama window.render(t) para t = 0, 1/12, 2/12 ... ate a duracao, tira uma
foto depois de cada chamada e junta tudo num MP4 segurado em 30 fps.

Por que 12 quadros por segundo autorados: movimento a 12 le como decidido, e
render a 12 cabe em tempo humano. Cada quadro autorado e repetido para preencher
os 30 do container, entao o arquivo final e 30 fps de verdade e nenhum player
reclama. A lei esta em referencias/PADRAO-VISUAL.md secao 5.

Uso:

    flow-reels produzir/painel --painel projetos/meu-video/corte-01/painel.html \
                     --saida projetos/meu-video/corte-01/painel.mp4

    flow-reels produzir/painel --painel painel.html --saida painel.mp4 --duracao 12.5
    flow-reels produzir/painel --painel painel.html --saida quadro.png --so-quadro 3.2

O painel.html precisa expor tres coisas, e o contrato esta em
componentes/REGISTRO.md secao 4:

    window.DURACAO   duracao em segundos
    window.PRONTO    vira true quando fonte e imagem terminaram de carregar
    window.render(t) desenha o estado do mundo no segundo t, e e pura

Como as pecas e a marca chegam na pagina: este script sobe um servidor local que
serve, na ordem, a pasta do painel, a raiz do pacote e a pasta componentes. Por
isso o painel pode pedir base.css, base.js e card.html sem caminho nenhum, e as
fontes da marca sao achadas a partir da raiz. Antes de abrir a pagina, o script
injeta window.TOKENS com o conteudo de marca/tokens.json e window.RAIZ com "/".
Nenhuma cor e escolhida dentro do painel.
"""

import argparse
import http.server
import json
import os
import shutil
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


LARGURA = 1080
ALTURA = 956
FPS_AUTORADO = 12
FPS_SAIDA = 30

MENSAGEM_CHROMIUM = """
erro: o Chromium do Playwright nao esta instalado nesta maquina.

Rode este comando uma vez e tente de novo:

    python -m playwright install chromium

Se o comando acima falhar dizendo que o playwright nao existe, instale antes:

    python -m pip install playwright
"""

MENSAGEM_PLAYWRIGHT = """
erro: o pacote playwright nao esta instalado nesta maquina.

Rode estes dois comandos e tente de novo:

    python -m pip install playwright
    python -m playwright install chromium
"""


# ---------------------------------------------------------------------------
# O servidor local
# ---------------------------------------------------------------------------

class ServidorDePastas(http.server.SimpleHTTPRequestHandler):
    """Serve varias pastas como se fossem uma so, na ordem em que foram dadas."""

    pastas = []

    def translate_path(self, caminho):
        limpo = caminho.split("?", 1)[0].split("#", 1)[0].lstrip("/")
        limpo = os.path.normpath(limpo).replace("\\", "/")
        if limpo.startswith(".."):
            return os.path.join(self.pastas[0], "arquivo-inexistente")
        for pasta in self.pastas:
            tentativa = os.path.join(pasta, *limpo.split("/")) if limpo else pasta
            if os.path.exists(tentativa):
                return tentativa
        # Ultima cartada: o mesmo nome dentro de qualquer pasta, ignorando o caminho.
        nome = os.path.basename(limpo)
        for pasta in self.pastas:
            tentativa = os.path.join(pasta, nome)
            if nome and os.path.isfile(tentativa):
                return tentativa
        return os.path.join(self.pastas[0], *limpo.split("/")) if limpo else self.pastas[0]

    def log_message(self, formato, *args):
        pass


def porta_livre():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def subir_servidor(pastas):
    classe = type("ServidorConfigurado", (ServidorDePastas,), {"pastas": pastas})
    porta = porta_livre()
    servidor = socketserver.ThreadingTCPServer(("127.0.0.1", porta), classe)
    servidor.daemon_threads = True
    linha = threading.Thread(target=servidor.serve_forever, daemon=True)
    linha.start()
    return servidor, porta


# ---------------------------------------------------------------------------
# Apoio
# ---------------------------------------------------------------------------

def achar_raiz(inicio):
    """A pasta de trabalho (marca/tokens.json); as peças vêm de componentes/, da pasta ou do plugin."""
    return fabrica.raiz()


def ler_tokens(raiz, caminho_pedido):
    if caminho_pedido:
        caminho = Path(caminho_pedido)
    else:
        caminho = raiz / "marca" / "tokens.json"
        if not caminho.is_file():
            exemplo = fabrica.achar("marca/tokens.exemplo.json")
            if exemplo.is_file():
                print("aviso: ainda nao existe marca/tokens.json, entao estou usando o exemplo.")
                print("       Rode a skill `/flow-reels:marca` para o corte sair com a sua identidade.")
                caminho = exemplo
    if not caminho.is_file():
        print("aviso: nao achei arquivo de tokens. O painel vai cair no padrao embutido.")
        return None
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def formatar_tempo(segundos):
    if segundos < 90:
        return "%.0f s" % segundos
    return "%d min %02d s" % (int(segundos // 60), int(segundos % 60))


# ---------------------------------------------------------------------------
# O render
# ---------------------------------------------------------------------------

def renderizar(opcoes):
    caminho_painel = Path(opcoes.painel).resolve()
    if not caminho_painel.is_file():
        print("erro: nao encontrei o painel em %s" % caminho_painel)
        return 1

    raiz = Path(opcoes.raiz).resolve() if opcoes.raiz else achar_raiz(caminho_painel)
    componentes = raiz / "componentes"

    # o servidor olha na pasta do painel, na pasta de trabalho e no plugin, nesta ordem
    pastas = [str(caminho_painel.parent), str(raiz), str(fabrica.plugin())]
    for base in (raiz, fabrica.plugin()):
        if (base / "componentes").is_dir():
            pastas.append(str(base / "componentes"))

    tokens = ler_tokens(raiz, opcoes.tokens)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(MENSAGEM_PLAYWRIGHT)
        return 1

    servidor, porta = subir_servidor(pastas)
    endereco = "http://127.0.0.1:%d/%s" % (porta, caminho_painel.name)

    pasta_quadros = opcoes.quadros or tempfile.mkdtemp(prefix="fc-painel-")
    os.makedirs(pasta_quadros, exist_ok=True)
    limpar_quadros = opcoes.quadros is None

    codigo = 1
    try:
        with sync_playwright() as p:
            try:
                navegador = p.chromium.launch(args=["--force-color-profile=srgb",
                                                    "--disable-lcd-text",
                                                    "--hide-scrollbars"])
            except Exception as erro:
                texto = str(erro)
                if "Executable doesn't exist" in texto or "playwright install" in texto:
                    print(MENSAGEM_CHROMIUM)
                else:
                    print("erro: nao consegui abrir o navegador. %s" % texto)
                return 1

            pagina = navegador.new_page(viewport={"width": LARGURA, "height": ALTURA},
                                        device_scale_factor=1)
            erros = []
            pagina.on("pageerror", lambda e: erros.append(str(e)))
            pagina.on("console", lambda m: erros.append("console %s: %s" % (m.type, m.text))
                      if m.type == "error" else None)

            pagina.add_init_script("window.TOKENS = %s; window.RAIZ = '/'; window.FC_RENDER = true;"
                                   % json.dumps(tokens if tokens else None))

            pagina.goto(endereco, wait_until="load", timeout=30000)

            try:
                pagina.wait_for_function("typeof window.render === 'function'", timeout=15000)
            except Exception:
                print("erro: a pagina abriu, mas nao expos window.render(t).")
                if erros:
                    print("      O navegador reclamou disto: %s" % erros[0])
                print("      Confira o contrato em componentes/REGISTRO.md secao 4.")
                return 1

            try:
                pagina.wait_for_function("window.PRONTO === true", timeout=20000)
            except Exception:
                print("aviso: window.PRONTO nao virou true em 20 s. Sigo mesmo assim, mas a fonte")
                print("       pode sair errada nos primeiros quadros.")
            pagina.wait_for_timeout(250)

            duracao = opcoes.duracao
            if duracao is None:
                duracao = pagina.evaluate("window.DURACAO")
            if not duracao or float(duracao) <= 0:
                print("erro: nao sei a duracao do painel. Defina window.DURACAO no painel.html,")
                print("      ou passe --duracao em segundos.")
                return 1
            duracao = float(duracao)

            if opcoes.so_quadro is not None:
                pagina.evaluate("t => window.render(t)", float(opcoes.so_quadro))
                pagina.wait_for_timeout(60)
                destino = Path(opcoes.saida).resolve()
                os.makedirs(destino.parent, exist_ok=True)
                pagina.screenshot(path=str(destino))
                print("quadro do segundo %.2f salvo em %s" % (float(opcoes.so_quadro), destino))
                # A reclamacao do navegador tambem vale aqui. Antes ela so era impressa no fim do
                # render completo, entao quem conferia por quadro unico nao via logo ausente nem
                # erro de script no terminal, so no proprio quadro.
                if erros:
                    print("aviso: o navegador reclamou. Primeira reclamacao:")
                    print("       %s" % erros[0])
                navegador.close()
                codigo = 0
                return codigo

            total = int(round(duracao * opcoes.fps_autorado))
            print("renderizando %d quadros autorados (%.1f s a %d fps) em %dx%d."
                  % (total, duracao, opcoes.fps_autorado, LARGURA, ALTURA))
            print("costuma sair de 4 a 8 quadros por segundo, entao de %s a %s. Nao travou."
                  % (formatar_tempo(total / 8.0), formatar_tempo(total / 4.0)))

            comeco = time.time()
            for indice in range(total):
                t = indice / float(opcoes.fps_autorado)
                pagina.evaluate("t => window.render(t)", t)
                pagina.screenshot(path=os.path.join(pasta_quadros, "q%05d.png" % indice))
                if indice and indice % opcoes.fps_autorado == 0:
                    passado = time.time() - comeco
                    resta = passado / indice * (total - indice)
                    print("  %d de %d quadros  ·  %.0f%%  ·  faltam cerca de %s"
                          % (indice, total, 100.0 * indice / total, formatar_tempo(resta)),
                          flush=True)

            navegador.close()
            print("  %d de %d quadros  ·  100%%  ·  %s de render"
                  % (total, total, formatar_tempo(time.time() - comeco)))

            if erros:
                print("aviso: o navegador reclamou durante o render. Primeira reclamacao:")
                print("       %s" % erros[0])

            codigo = juntar(pasta_quadros, opcoes)
    finally:
        servidor.shutdown()
        servidor.server_close()
        if limpar_quadros and codigo == 0:
            shutil.rmtree(pasta_quadros, ignore_errors=True)
        elif limpar_quadros and os.path.isdir(pasta_quadros) and os.listdir(pasta_quadros):
            print("os quadros ficaram em %s para voce olhar." % pasta_quadros)

    return codigo


def juntar(pasta_quadros, opcoes):
    if shutil.which("ffmpeg") is None:
        print("erro: nao encontrei o ffmpeg no caminho do sistema, entao nao da para fechar o MP4.")
        print("      Os quadros estao em %s" % pasta_quadros)
        return 1

    saida = Path(opcoes.saida).resolve()
    os.makedirs(saida.parent, exist_ok=True)

    comando = [
        "ffmpeg", "-y",
        "-framerate", str(opcoes.fps_autorado),
        "-i", os.path.join(pasta_quadros, "q%05d.png"),
        "-vf", "fps=%d,scale=in_range=full:out_range=tv,format=yuv420p" % FPS_SAIDA,
        "-color_range", "tv", "-colorspace", "bt709",
        "-color_primaries", "bt709", "-color_trc", "bt709",
        "-r", str(FPS_SAIDA),
        "-c:v", "libx264",
        "-profile:v", "high",
        "-preset", "medium",
        "-crf", str(opcoes.crf),
        "-movflags", "+faststart",
        str(saida),
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True, errors="replace")
    if resultado.returncode != 0:
        print("erro: o ffmpeg nao fechou o MP4. Ultimas linhas:")
        print("\n".join(resultado.stderr.strip().splitlines()[-12:]))
        return 1

    tamanho = saida.stat().st_size / (1024 * 1024)
    print("painel pronto em %s  (%.1f MB, %d fps, %dx%d)" % (saida, tamanho, FPS_SAIDA, LARGURA, ALTURA))
    return 0


def principal(argv=None):
    analisador = argparse.ArgumentParser(
        description="Renderiza o painel de cima quadro a quadro e fecha o MP4 de 1080x956.")
    analisador.add_argument("--painel", help="caminho do painel.html")
    analisador.add_argument("--saida", help="caminho do MP4 de saida, ou do PNG com --so-quadro")
    analisador.add_argument("--duracao", type=float, default=None,
                            help="duracao em segundos, quando quiser mandar mais que window.DURACAO")
    analisador.add_argument("--so-quadro", type=float, default=None, metavar="SEGUNDO",
                            help="renderiza um unico instante e salva um PNG, para conferir rapido")
    analisador.add_argument("--fps-autorado", type=int, default=FPS_AUTORADO,
                            help="quadros autorados por segundo (padrao: %d)" % FPS_AUTORADO)
    analisador.add_argument("--tokens", default=None,
                            help="caminho de um tokens.json especifico (padrao: marca/tokens.json)")
    analisador.add_argument("--raiz", default=None,
                            help="raiz do pacote, quando o script nao conseguir descobrir sozinho")
    analisador.add_argument("--quadros", default=None,
                            help="pasta onde guardar os PNGs (padrao: pasta temporaria, apagada no fim)")
    analisador.add_argument("--crf", type=int, default=16, help="qualidade do H.264 (padrao: 16)")

    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        analisador.print_help()
        print("\nFaltou dizer o que renderizar. O minimo e --painel e --saida.")
        return 2

    opcoes = analisador.parse_args(argv)
    if not opcoes.painel or not opcoes.saida:
        print("erro: faltou --painel ou --saida.")
        return 1

    return renderizar(opcoes)


if __name__ == "__main__":
    sys.exit(principal())
