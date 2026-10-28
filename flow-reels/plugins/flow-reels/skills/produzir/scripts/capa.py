#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
capa.py  ·  a capa do reel, com a foto do criador e a promessa do corte

A capa é o que aparece no grid do perfil e no topo do Reels antes do play. Ela sai sempre do mesmo
molde, para o perfil ficar com cara de coleção:

- a foto do criador recortada (setup.json "capa"."foto", por padrão marca/foto.jpg), grande, embaixo;
- o fundo é a cena do próprio corte (uma imagem do assets/ ou um quadro do fala.mp4), desfocado e
  escurecido, com o brilho rosa da marca;
- o título é a promessa do corte em letra grande, na fonte de título da marca, com a palavra de
  destaque no rosa;
- um selo de vidro com o assunto, e até dois logos em cor (componentes/marcas/) ao lado da cabeça.

O que importa fica dentro do recorte do grid do Instagram (3:4, de y 240 a y 1680), porque é ele que
aparece no perfil. A capa inteira é 1080x1920, como o Reels pede.

Uso
---
    flow-reels produzir/capa --projeto projetos/<video> --corte 01

Lê materiais-de-trabalho/corte-NN/capa.json:

    {
      "titulo": "Sua VPS te avisa no WhatsApp",
      "destaque": ["WhatsApp"],
      "selo": "CPU, memória e disco · fluxo n8n",
      "fundo": { "imagem": "assets/data-center-01.jpg" }   ou   { "quadro": 1.0 },
      "adesivos": ["n8n-icone", "whatsapp-icone"]
    }

Grava corte-NN/corte-NN-capa.jpg (a entrega, ao lado do mp4) e, para conferir,
materiais-de-trabalho/corte-NN/capa-grade.jpg, o recorte 3:4 que o perfil mostra.

A foto recortada fica no "capa"."recorte" do setup.json (marca/foto-recorte.png). Se ela não existe,
ou é mais velha que a foto, o script recorta na hora com o componentes/imagens/tirar-fundo.py.
"""

import argparse
import base64
import io
import json
import mimetypes
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

AQUI = Path(__file__).resolve().parent
RAIZ = fabrica.raiz()
W, H = 1080, 1920
GRADE = (240, 1680)  # o recorte 3:4 do perfil


def erro(msg):
    print("  erro: " + msg)
    sys.exit(1)


def data_uri(caminho):
    tipo = mimetypes.guess_type(str(caminho))[0] or "application/octet-stream"
    if str(caminho).endswith(".ttf"):
        tipo = "font/ttf"
    return "data:%s;base64,%s" % (tipo, base64.b64encode(Path(caminho).read_bytes()).decode("ascii"))


def foto_recortada():
    """A foto da capa vem do setup.json ("capa": {"foto", "recorte"}); o recorte sem fundo é gerado uma
    vez, com o tirar-fundo.py, e reaproveitado em toda capa."""
    conf = {}
    try:
        conf = json.loads((RAIZ / "setup.json").read_text(encoding="utf-8")).get("capa", {}) or {}
    except (OSError, ValueError):
        pass
    original = RAIZ / conf.get("foto", "marca/foto.jpg")
    recorte = RAIZ / conf.get("recorte", "marca/foto-recorte.png")
    if recorte.is_file() and (not original.is_file() or recorte.stat().st_mtime >= original.stat().st_mtime):
        return recorte
    if not original.is_file():
        erro("falta a foto da capa (%s, setup.json \"capa\".\"foto\")" % original.relative_to(RAIZ))
    print("  recortando a foto da capa (uma vez só)...")
    r = subprocess.run([sys.executable, str(fabrica.plugin() / "componentes" / "imagens" / "tirar-fundo.py"), str(original),
                        "--saida", str(recorte.parent)], capture_output=True, text=True)
    gerado = recorte.parent / (original.stem + "-sem-fundo.png")
    if r.returncode != 0 or not gerado.is_file():
        erro("o recorte da foto falhou: " + (r.stdout + r.stderr)[-400:])
    gerado.replace(recorte)
    return recorte


def fundo_do_corte(pasta, conf):
    if conf.get("imagem"):
        caminho = (pasta / conf["imagem"]).resolve()
        if not caminho.is_file():
            erro("a imagem de fundo não existe: %s" % caminho)
        return caminho
    t = float(conf.get("quadro", 1.0))
    fala = pasta / "fala.mp4"
    if not fala.is_file():
        erro("sem imagem de fundo e sem fala.mp4 para tirar um quadro")
    destino = Path(tempfile.gettempdir()) / ("capa-quadro-%s.png" % pasta.name)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % t, "-i", str(fala), "-frames:v", "1",
                    str(destino)], check=True)
    return destino


def html_da_capa(c, tokens, foto, fundo, adesivos):
    cores = tokens.get("cores", {})
    fontes = tokens.get("fontes", {})
    sup = cores.get("superficie", "#0D0A0C")
    tinta = cores.get("tinta", "#F7F5F6")
    destaque = cores.get("destaque", "#FF005E")
    # o brilho e o escuro vêm da marca (cores.destaque, ou textura.brilho_cor, e cores.superficie)
    rgb = lambda h: ",".join(str(int(h.lstrip("#")[i:i + 2], 16)) for i in (0, 2, 4))
    br = rgb((tokens.get("textura", {}) or {}).get("brilho_cor") or destaque)
    sr = rgb(sup)
    f_titulo = fabrica.achar(fontes.get("titulo", {}).get("arquivo") or "marca/fontes/Quicksand-Bold.ttf")
    f_corpo = fabrica.achar(fontes.get("corpo", {}).get("arquivo") or "marca/fontes/Quicksand-Medium.ttf")
    palavras = c["titulo"].split()
    marcas = {d.lower() for d in c.get("destaque", [])}
    titulo = " ".join('<span class="acento">%s</span>' % p if p.lower().strip(",.?!") in marcas or p.lower() in marcas
                      else p for p in palavras)
    lados = [(70, 980), (W - 70 - 200, 1040)]
    placas = "".join('<div class="adesivo" style="left:%dpx;top:%dpx"><img src="%s"></div>' % (x, y, data_uri(a))
                     for (x, y), a in zip(lados, adesivos))
    selo = ('<div class="selo"><span>%s</span></div>' % c["selo"]) if c.get("selo") else ""
    return """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:"Titulo";src:url(%(ft)s)}
@font-face{font-family:"Corpo";src:url(%(fc)s)}
html,body{margin:0;width:%(W)dpx;height:%(H)dpx;background:%(sup)s;overflow:hidden}
.fundo{position:absolute;inset:-60px;background:url(%(fundo)s) center/cover no-repeat;
  filter:blur(%(desfoque)dpx) brightness(%(luz).2f) saturate(.85)}
.brilho{position:absolute;left:-380px;top:-260px;width:1500px;height:1500px;
  background:radial-gradient(circle,rgba(%(br)s,.34),rgba(%(br)s,0) 62%%)}
.sombra-alto{position:absolute;left:0;right:0;top:0;height:900px;
  background:linear-gradient(rgba(%(sr)s,.78),rgba(%(sr)s,0))}
.foto{position:absolute;left:50%%;bottom:0;height:%(foto_h)dpx;transform:translateX(-50%%);
  filter:drop-shadow(0 0 46px rgba(%(br)s,.32)) drop-shadow(0 30px 60px rgba(0,0,0,.6))}
.chao{position:absolute;left:0;right:0;bottom:0;height:360px;background:linear-gradient(rgba(%(sr)s,0),%(sup)s 88%%)}
.titulo{position:absolute;left:84px;right:84px;top:300px;font-family:"Titulo";color:%(tinta)s;
  font-size:128px;line-height:1.02;letter-spacing:-.012em;text-shadow:0 8px 34px rgba(0,0,0,.65)}
.acento{color:%(destaque)s}
.selo{position:absolute;left:84px;font-family:"Corpo";font-size:36px;color:%(tinta)s;
  padding:18px 34px;border-radius:999px;letter-spacing:.02em;
  background:linear-gradient(135deg,rgba(%(sr)s,.72),rgba(%(sr)s,.5));
  backdrop-filter:blur(18px) saturate(1.2);-webkit-backdrop-filter:blur(18px) saturate(1.2);
  border:1.5px solid rgba(255,255,255,.16)}
.adesivo{position:absolute;width:200px;height:200px;border-radius:48px;display:flex;align-items:center;
  justify-content:center;background:linear-gradient(135deg,rgba(%(sr)s,.74),rgba(%(sr)s,.52));
  backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1.5px solid rgba(255,255,255,.16)}
.adesivo img{max-width:124px;max-height:124px}
</style></head><body>
<div class="fundo"></div><div class="brilho"></div><div class="sombra-alto"></div>
<img class="foto" src="%(foto)s">
<div class="chao"></div>
%(placas)s
<div class="titulo" id="t">%(titulo)s</div>
%(selo)s
<script>
document.fonts.ready.then(() => {
  const t = document.getElementById('t');
  let tam = 128;
  // cabe em até 4 linhas e termina antes do rosto (y 780)
  while (tam > 72 && (t.offsetTop + t.offsetHeight > 760)) { tam -= 4; t.style.fontSize = tam + 'px'; }
  const s = document.querySelector('.selo');
  if (s) s.style.top = (t.offsetTop + t.offsetHeight + 34) + 'px';
  window.PRONTO = true;
});
</script></body></html>""" % {
        "ft": data_uri(f_titulo), "fc": data_uri(f_corpo), "W": W, "H": H, "sup": sup, "tinta": tinta,
        "destaque": destaque, "fundo": data_uri(fundo), "desfoque": int(c.get("fundo", {}).get("desfoque", 9)),
        "luz": 1.0 - float(c.get("fundo", {}).get("escurecer", 0.58)), "foto": data_uri(foto),
        "foto_h": int(c.get("foto_altura", 1180)), "placas": placas, "titulo": titulo, "selo": selo,
        "br": br, "sr": sr,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--projeto", required=True)
    ap.add_argument("--corte", required=True)
    ap.add_argument("--foto", help="outra foto já recortada (PNG sem fundo), no lugar de marca/foto-recorte.png")
    args = ap.parse_args()

    projeto = (RAIZ / args.projeto) if not Path(args.projeto).is_absolute() else Path(args.projeto)
    nome = "corte-%02d" % int(args.corte)
    pasta = projeto / "materiais-de-trabalho" / nome
    conf_p = pasta / "capa.json"
    if not conf_p.is_file():
        erro("falta %s (título, destaque, selo, fundo, adesivos)" % conf_p)
    c = json.loads(conf_p.read_text(encoding="utf-8"))
    # marca do projeto (um cliente) vale mais que a do pacote, como no compor.py
    marca_projeto = projeto / "materiais-de-trabalho" / "marca" / "tokens.json"
    tokens = json.loads((marca_projeto if marca_projeto.is_file()
                         else RAIZ / "marca" / "tokens.json").read_text(encoding="utf-8"))
    foto = Path(args.foto).expanduser() if args.foto else foto_recortada()
    fundo = fundo_do_corte(pasta, c.get("fundo", {}))
    adesivos = []
    for a in c.get("adesivos", [])[:2]:
        arq = fabrica.achar("componentes/marcas/" + a + ".png")
        if arq.is_file():
            adesivos.append(arq)
        else:
            print("  aviso: o logo %s não está em componentes/marcas/; fica de fora" % a)

    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": W, "height": H})
        pag.set_content(html_da_capa(c, tokens, foto, fundo, adesivos))
        pag.wait_for_function("window.PRONTO === true", timeout=60000)
        png = pag.screenshot(type="png")
        nav.close()
    im = Image.open(io.BytesIO(png)).convert("RGB")
    entrega = projeto / nome / (nome + "-capa.jpg")
    entrega.parent.mkdir(parents=True, exist_ok=True)
    im.save(entrega, "JPEG", quality=92, optimize=True)
    im.crop((0, GRADE[0], W, GRADE[1])).save(pasta / "capa-grade.jpg", "JPEG", quality=88)
    print("  ok  capa       %s" % entrega)
    print("  ok  grade 3:4  %s" % (pasta / "capa-grade.jpg"))


if __name__ == "__main__":
    main()
