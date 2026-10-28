# -*- coding: utf-8 -*-
"""Renderiza o cartao de abertura e o fechamento (HTML) quadro a quadro, com fundo
transparente, em 1080 x 1920 e 30 quadros por segundo.

Usa o mesmo motor do painel do pacote (`/flow-reels:produzir`/scripts/painel.py): o
mesmo servidor local que serve a pasta da pagina, a raiz do pacote e componentes/,
e o mesmo contrato de pagina (window.DURACAO, window.PRONTO, window.render(t) pura).
A diferenca e o formato: aqui o quadro e a tela inteira, a captura guarda o canal
alfa (a filmagem fica por baixo, montada pelo compor_narrado.py) e a pagina recebe
alem de window.TOKENS um window.DADOS com os textos e os tempos daquele reel.

Uso direto, para conferir um instante:

    flow-reels narrado/renderizar_html --pagina ../modelos/abertura.html --dados dados.json \
                              --saida quadro.png --so-quadro 1.2

Normalmente quem chama e o compor_narrado.py.
"""

import argparse
import http.server
import importlib.util
import json
import os
import socket
import socketserver
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402

PAINEL = cm.PLUGIN / "skills" / "produzir" / "scripts" / "painel.py"

MENSAGEM_PLAYWRIGHT = """
erro: o pacote playwright nao esta instalado nesta maquina.

Rode estes dois comandos e tente de novo:

    python -m pip install playwright
    python -m playwright install chromium
"""

MENSAGEM_CHROMIUM = """
erro: o Chromium do Playwright nao esta instalado nesta maquina.

Rode este comando uma vez e tente de novo:

    python -m playwright install chromium
"""


def _motor_do_painel():
    """Importa o painel.py do pacote para reaproveitar o servidor dele."""
    try:
        spec = importlib.util.spec_from_file_location("painel_do_pacote", str(PAINEL))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "subir_servidor"):
            return mod
    except Exception:
        pass
    return None


class _Servidor(http.server.SimpleHTTPRequestHandler):
    """Reserva, para o caso de o painel.py nao estar ao alcance: serve varias pastas
    como uma so, na ordem dada."""
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
        return os.path.join(self.pastas[0], *limpo.split("/"))

    def log_message(self, *a):
        pass


def _subir(pastas):
    motor = _motor_do_painel()
    if motor is not None:
        return motor.subir_servidor(pastas)
    classe = type("ServidorDoReel", (_Servidor,), {"pastas": pastas})
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        porta = s.getsockname()[1]
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", porta), classe)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, porta


def renderizar(pagina, dados, tokens, pasta_saida, duracao=None, fps=cm.FPS, so_quadro=None,
               pastas_extra=()):
    """Captura a pagina. Devolve o numero de quadros escritos (q00000.png em diante).

    Com so_quadro, escreve um PNG so em pasta_saida (que entao e o caminho do arquivo).
    """
    pagina = Path(pagina).resolve()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(MENSAGEM_PLAYWRIGHT)
        sys.exit(1)

    # a pasta da pagina, a pasta de trabalho, o plugin e os componentes das duas (a de trabalho por cima)
    pastas = [str(pagina.parent), str(cm.RAIZ), str(cm.PLUGIN), str(cm.RAIZ / "componentes"),
              str(cm.PLUGIN / "componentes")]
    pastas += [str(p) for p in pastas_extra]
    srv, porta = _subir(pastas)
    endereco = "http://127.0.0.1:%d/%s" % (porta, pagina.name)
    escritos = 0
    try:
        with sync_playwright() as p:
            try:
                nav = p.chromium.launch(args=["--force-color-profile=srgb", "--disable-lcd-text",
                                              "--hide-scrollbars"])
            except Exception as e:
                if "Executable doesn't exist" in str(e) or "playwright install" in str(e):
                    print(MENSAGEM_CHROMIUM)
                    sys.exit(1)
                raise
            pg = nav.new_page(viewport={"width": cm.LARGURA, "height": cm.ALTURA},
                              device_scale_factor=1)
            erros = []
            pg.on("pageerror", lambda e: erros.append(str(e)))
            pg.on("console", lambda m: erros.append("console: " + m.text) if m.type == "error" else None)
            pg.add_init_script("window.TOKENS = %s; window.DADOS = %s; window.RAIZ = '/'; "
                               "window.FC_RENDER = true;"
                               % (json.dumps(tokens, ensure_ascii=False),
                                  json.dumps(dados, ensure_ascii=False)))
            pg.goto(endereco, wait_until="load", timeout=30000)
            pg.wait_for_function("typeof window.render === 'function'", timeout=15000)
            try:
                pg.wait_for_function("window.PRONTO === true", timeout=20000)
            except Exception:
                cm.aviso("window.PRONTO nao virou true em 20 s; a fonte pode sair errada.")
            pg.wait_for_timeout(200)
            dur = float(duracao or pg.evaluate("window.DURACAO") or 0)
            if so_quadro is not None:
                pg.evaluate("t => window.render(t)", float(so_quadro))
                Path(pasta_saida).parent.mkdir(parents=True, exist_ok=True)
                pg.screenshot(path=str(pasta_saida), omit_background=True)
                escritos = 1
            else:
                if dur <= 0:
                    cm.erro("a pagina %s nao disse a duracao." % pagina.name)
                Path(pasta_saida).mkdir(parents=True, exist_ok=True)
                total = int(round(dur * fps))
                for i in range(total):
                    pg.evaluate("t => window.render(t)", i / float(fps))
                    pg.screenshot(path=os.path.join(str(pasta_saida), "q%05d.png" % i),
                                  omit_background=True)
                    escritos += 1
            nav.close()
            if erros:
                cm.aviso("o navegador reclamou em %s: %s" % (pagina.name, erros[0]))
    finally:
        srv.shutdown()
        srv.server_close()
    return escritos


def principal(argv=None):
    an = argparse.ArgumentParser(description="Renderiza uma pagina de abertura ou fechamento.")
    an.add_argument("--pagina", required=True, help="o HTML (modelos/abertura.html ou fechamento.html)")
    an.add_argument("--dados", required=True, help="JSON com os dados do reel para a pagina")
    an.add_argument("--marca", default=None, help="tokens.json ou pasta da marca (padrao marca/)")
    an.add_argument("--saida", required=True, help="pasta dos quadros, ou PNG com --so-quadro")
    an.add_argument("--so-quadro", type=float, default=None, help="renderiza so este instante")
    an.add_argument("--duracao", type=float, default=None)
    op = an.parse_args(argv)
    tokens, _ = cm.ler_marca(op.marca)
    dados = cm.ler_json(op.dados)
    n = renderizar(op.pagina, dados, tokens, op.saida, op.duracao, so_quadro=op.so_quadro)
    cm.fala("%d quadro(s) em %s" % (n, op.saida))
    return 0


if __name__ == "__main__":
    sys.exit(principal())
