#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
capturar_assets.py  ·  traz a prova visual de uma ferramenta para a pasta da pauta

Abre cada link num Chromium sem tela e grava o que o painel do reel vai precisar
para mostrar a ferramenta de verdade, em vez de desenhar uma parecida:

  <nome>-hero.png       a primeira dobra da página em 1280 x 800, que é o que
                        a pessoa veria ao abrir o link
  <nome>-pagina.png     a página inteira, cortada em 4000 px de altura, para
                        recortar depois a seção que a fala citar
  <nome>-rolagem.webm   6 segundos de rolagem suave, para a rota tela do painel
  <nome>-og.<ext>       a imagem de compartilhamento oficial (og:image), quando
                        existe, que costuma ser a arte de divulgação da ferramenta
  <nome>.json           título, descrição, url final e o que foi gravado

Uso:

    flow-reels tendencias/capturar_assets --saida projetos/<pauta>/materiais-de-trabalho/assets \
        --link site=https://ferramenta.com --link repo=https://github.com/dono/repo

O nome antes do = vira o prefixo dos arquivos. Sem nome, o script usa o domínio.

O que ele não faz: não faz login, não aceita termos nem cookies, não preenche
formulário. Se um banner cobrir a página, o print sai com o banner e o agente
decide se ele atrapalha, olhando a imagem.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def fala(msg):
    print(msg, file=sys.stderr)


def nome_padrao(url):
    host = urlparse(url).netloc.replace("www.", "")
    return re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-") or "pagina"


def capturar(pagina, contexto_video, url, nome, saida, requests):
    info = {"nome": nome, "url_pedida": url, "arquivos": [], "avisos": []}
    try:
        pagina.goto(url, wait_until="domcontentloaded", timeout=45000)
        pagina.wait_for_timeout(3500)
    except Exception as e:
        info["avisos"].append("não abriu: %s" % e)
        return info

    info["url_final"] = pagina.url
    info["titulo"] = pagina.title()
    meta = pagina.evaluate("""() => {
        const m = n => (document.querySelector(`meta[property="${n}"]`) ||
                        document.querySelector(`meta[name="${n}"]`) || {}).content || null;
        return { descricao: m('og:description') || m('description'), og_imagem: m('og:image') };
    }""")
    info.update(meta)

    hero = saida / ("%s-hero.png" % nome)
    pagina.screenshot(path=str(hero))
    info["arquivos"].append(hero.name)

    altura = pagina.evaluate("() => document.documentElement.scrollHeight")
    completa = saida / ("%s-pagina.png" % nome)
    pagina.screenshot(path=str(completa), full_page=True,
                      clip={"x": 0, "y": 0, "width": 1280, "height": min(int(altura or 800), 4000)})
    info["arquivos"].append(completa.name)
    if altura and altura > 4000:
        info["avisos"].append("página com %d px, o print completo parou em 4000" % altura)

    if meta.get("og_imagem"):
        try:
            og_url = urljoin(pagina.url, meta["og_imagem"])
            r = requests.get(og_url, timeout=20, headers={"User-Agent": "fabrica-de-cortes/0.1"})
            r.raise_for_status()
            tipo = r.headers.get("content-type", "")
            ext = "png" if "png" in tipo else "webp" if "webp" in tipo else "jpg"
            og = saida / ("%s-og.%s" % (nome, ext))
            og.write_bytes(r.content)
            info["arquivos"].append(og.name)
        except Exception as e:
            info["avisos"].append("og:image não baixou: %s" % e)

    # rolagem: uma página nova no contexto que grava vídeo
    try:
        pv = contexto_video.new_page()
        pv.goto(url, wait_until="domcontentloaded", timeout=45000)
        pv.wait_for_timeout(2500)
        for _ in range(24):
            pv.mouse.wheel(0, 90)
            pv.wait_for_timeout(150)
        pv.wait_for_timeout(500)
        caminho_video = pv.video.path()
        pv.close()
        destino = saida / ("%s-rolagem.webm" % nome)
        Path(caminho_video).replace(destino)
        info["arquivos"].append(destino.name)
    except Exception as e:
        info["avisos"].append("rolagem não gravou: %s" % e)

    return info


def main():
    ap = argparse.ArgumentParser(description="Grava print, rolagem e arte oficial de cada link.")
    ap.add_argument("--saida", required=True, help="pasta de assets da pauta")
    ap.add_argument("--link", action="append", required=True, help="nome=url ou só url; pode repetir")
    args = ap.parse_args()

    try:
        import requests
        from playwright.sync_api import sync_playwright
    except ImportError:
        fala("  erro: faltam playwright e requests. Rode com .venv/bin/python, ou rode o instalar.sh.")
        return 2

    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    pedidos = []
    for item in args.link:
        if "=" in item and not item.startswith("http"):
            nome, url = item.split("=", 1)
        else:
            nome, url = nome_padrao(item), item
        pedidos.append((re.sub(r"[^a-z0-9-]+", "-", nome.lower()).strip("-"), url))

    resultados = []
    with sync_playwright() as p:
        try:
            nav = p.chromium.launch()
        except Exception as e:
            fala("  erro: o Chromium do Playwright não abriu (%s).\n"
                 "  Rode: python -m playwright install chromium" % e)
            return 2
        tmp = saida / ".video-tmp"
        ctx = nav.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=2,
                              locale="pt-BR")
        ctx_video = nav.new_context(viewport={"width": 1280, "height": 800}, locale="pt-BR",
                                    record_video_dir=str(tmp),
                                    record_video_size={"width": 1280, "height": 800})
        pagina = ctx.new_page()
        for nome, url in pedidos:
            fala("  %s  ·  %s" % (nome, url))
            info = capturar(pagina, ctx_video, url, nome, saida, requests)
            (saida / ("%s.json" % nome)).write_text(json.dumps(info, ensure_ascii=False, indent=2),
                                                   encoding="utf-8")
            resultados.append(info)
            for a in info["avisos"]:
                fala("      aviso: " + a)
        ctx_video.close()
        ctx.close()
        nav.close()
        if tmp.is_dir():
            for f in tmp.iterdir():
                f.unlink()
            tmp.rmdir()

    fala("")
    for r in resultados:
        fala("  %-14s %d arquivos%s" % (r["nome"], len(r["arquivos"]),
                                        "  ·  %d aviso(s)" % len(r["avisos"]) if r["avisos"] else ""))
    print(saida)
    return 0 if all(r["arquivos"] for r in resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
