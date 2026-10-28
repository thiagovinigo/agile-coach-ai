#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
buscar-imagem.py  ·  imagem de banco livre, com licença conferida e crédito registrado

Para a cena que mostra a coisa nomeada na fala (a foto do megafone, do museu, do robô), sem pagar
banco de imagem e sem usar foto de quem não deixou. Busca nos bancos abaixo, baixa as melhores, grava
uma folha de contato numerada para escolher olhando e escreve o crédito de cada arquivo no
CREDITOS.md da pasta de saída.

Os bancos
---------
Sem chave nenhuma:
  openverse   o buscador de mídia livre do WordPress: junta Flickr, Wikimedia, Rawpixel, StockSnap
              e outros, e filtra pela licença
  wikimedia   o Wikimedia Commons direto (fotos, mapas, diagramas, fotos históricas)
Com chave gratuita no .env da raiz do pacote (entram sozinhos quando a chave existe):
  pexels      PEXELS_API_KEY   (https://www.pexels.com/api/)  licença Pexels, sem crédito obrigatório
  pixabay     PIXABAY_API_KEY  (https://pixabay.com/api/docs/) licença Pixabay, sem crédito obrigatório

As licenças
-----------
  --licenca livre    (padrão) CC0, domínio público, licença Pexels e licença Pixabay: uso comercial
                     liberado, sem crédito obrigatório (o crédito entra no CREDITOS.md mesmo assim)
  --licenca credito  soma CC BY: exige o crédito, que o modo imagem-cheia mostra no campo "credito"
Nunca entram: CC BY-SA, CC BY-NC, CC BY-ND, nem foto marcada com direito de imagem de pessoa ou com
marca registrada no Commons.

Uso
---
    flow-reels componentes/buscar-imagem megafone --saida projetos/<v>/materiais-de-trabalho/corte-01/assets
    flow-reels componentes/buscar-imagem "robot arm" "server room" --saida <pasta> --quantos 4 --orientacao vertical
    flow-reels componentes/buscar-imagem museu --saida <pasta> --licenca credito --sem-fundo

Busque em inglês quando o português trouxer pouco: os bancos são quase todos em inglês. A folha de
contato fica em <saida>/busca-<termo>.png; olhe antes de pôr a imagem numa cena. Com --sem-fundo,
cada imagem baixada também ganha a versão recortada, <nome>-sem-fundo.png (tirar-fundo.py).
"""

import argparse
import html
import io
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

AQUI = Path(__file__).resolve().parent
RAIZ = fabrica.raiz()   # o .env da pasta de trabalho
AGENTE = "FlowReels/3.0 (https://flowgrammers.com.br)"
LADO_MAX = 2400


def ler_env():
    env = {}
    arq = RAIZ / ".env"
    if arq.is_file():
        for linha in arq.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if k.endswith("_API_KEY")})
    return env


def pegar(url, cabecalhos=None, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE, **(cabecalhos or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def pegar_json(url, cabecalhos=None):
    return json.loads(pegar(url, cabecalhos).decode("utf-8"))


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40] or "imagem"


def limpar_html(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t or ""))).strip()


def orientacao_ok(w, h, orient):
    if not w or not h or orient == "qualquer":
        return True
    r = w / h
    return {"vertical": r < 0.9, "horizontal": r > 1.1, "quadrada": 0.9 <= r <= 1.1}[orient]


# ------------------------------------------------------------------ os bancos

def buscar_openverse(termo, args):
    lic = "cc0,pdm" if args.licenca == "livre" else "cc0,pdm,by"
    q = {"q": termo, "license": lic, "page_size": 20}  # sem conta, o Openverse aceita até 20 por página
    asp = {"vertical": "tall", "horizontal": "wide", "quadrada": "square"}.get(args.orientacao)
    if asp:
        q["aspect_ratio"] = asp
    d = pegar_json("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(q))
    for r in d.get("results", []):
        yield {
            "fonte": "openverse/" + (r.get("source") or r.get("provider") or "?"),
            "url": r.get("url"), "pagina": r.get("foreign_landing_url") or r.get("url"),
            "titulo": limpar_html(r.get("title") or termo), "autor": limpar_html(r.get("creator") or ""),
            "licenca": ("CC0 1.0" if r.get("license") == "cc0" else "domínio público" if r.get("license") == "pdm"
                        else f"CC {str(r.get('license')).upper()} {r.get('license_version') or ''}".strip()),
            "credito_obrigatorio": r.get("license") not in ("cc0", "pdm"),
            "w": r.get("width"), "h": r.get("height"),
        }


def buscar_wikimedia(termo, args):
    q = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrlimit": 40,
         "gsrsearch": f"{termo} filetype:bitmap", "prop": "imageinfo",
         "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 2000}
    d = pegar_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q))
    paginas = sorted((d.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))
    for p in paginas:
        ii = (p.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata") or {}
        lic = limpar_html((m.get("LicenseShortName") or {}).get("value", ""))
        restr = limpar_html((m.get("Restrictions") or {}).get("value", "")).lower()
        livre = "public domain" in lic.lower() or lic.upper().startswith("CC0") or lic.upper() == "PD"
        so_by = bool(re.match(r"^CC BY \d", lic.upper()))  # CC BY puro, sem SA/NC/ND
        if not (livre or (args.licenca == "credito" and so_by)):
            continue
        if "personality" in restr or "trademark" in restr:
            continue
        if not str(ii.get("mime", "")).startswith("image/"):
            continue
        yield {
            "fonte": "wikimedia", "url": ii.get("thumburl") or ii.get("url"),
            "pagina": ii.get("descriptionurl") or ii.get("url"),
            "titulo": re.sub(r"\.[a-z0-9]+$", "", p.get("title", "").replace("File:", ""), flags=re.I),
            "autor": limpar_html((m.get("Artist") or {}).get("value", "")),
            "licenca": "domínio público" if "public domain" in lic.lower() else lic,
            "credito_obrigatorio": not livre, "w": ii.get("width"), "h": ii.get("height"),
        }


def buscar_pexels(termo, args, chave):
    q = {"query": termo, "per_page": 30}
    o = {"vertical": "portrait", "horizontal": "landscape", "quadrada": "square"}.get(args.orientacao)
    if o:
        q["orientation"] = o
    d = pegar_json("https://api.pexels.com/v1/search?" + urllib.parse.urlencode(q), {"Authorization": chave})
    for f in d.get("photos", []):
        yield {"fonte": "pexels", "url": (f.get("src") or {}).get("large2x") or (f.get("src") or {}).get("original"),
               "pagina": f.get("url"), "titulo": f.get("alt") or termo, "autor": f.get("photographer") or "",
               "licenca": "licença Pexels", "credito_obrigatorio": False, "w": f.get("width"), "h": f.get("height")}


def buscar_pixabay(termo, args, chave):
    q = {"key": chave, "q": termo, "image_type": "photo", "safesearch": "true", "per_page": 30}
    o = {"vertical": "vertical", "horizontal": "horizontal"}.get(args.orientacao)
    if o:
        q["orientation"] = o
    d = pegar_json("https://pixabay.com/api/?" + urllib.parse.urlencode(q))
    for h in d.get("hits", []):
        yield {"fonte": "pixabay", "url": h.get("largeImageURL"), "pagina": h.get("pageURL"),
               "titulo": h.get("tags") or termo, "autor": h.get("user") or "",
               "licenca": "licença Pixabay", "credito_obrigatorio": False,
               "w": h.get("imageWidth"), "h": h.get("imageHeight")}


# ------------------------------------------------------------------ créditos e folha

CABECALHO = ("# Créditos das imagens\n\n"
             "Imagens de banco livre, baixadas pelo `componentes/imagens/buscar-imagem.py`. Licença conferida "
             "na página de origem de cada uma.\n\n"
             "| arquivo | o que mostra | página de origem | autor | licença |\n|---|---|---|---|---|\n")


def creditos_existentes(saida):
    arq = saida / "CREDITOS.md"
    return arq.read_text(encoding="utf-8") if arq.is_file() else ""


def registrar_credito(saida, nome, item):
    arq = saida / "CREDITOS.md"
    atual = creditos_existentes(saida)
    if not atual:
        atual = CABECALHO
    elif "| arquivo |" not in atual:
        atual = atual.rstrip() + "\n\n| arquivo | o que mostra | página de origem | autor | licença |\n|---|---|---|---|---|\n"
    titulo = item["titulo"].replace("|", "/")[:90]
    autor = (item["autor"] or "não informado").replace("|", "/")[:60]
    lic = item["licenca"] + (" (crédito obrigatório)" if item["credito_obrigatorio"] else "")
    linha = f"| `{nome}` | {titulo} | {item['pagina']} | {autor} | {lic} |\n"
    arq.write_text(atual.rstrip("\n") + "\n" + linha, encoding="utf-8")


def folha_de_contato(saida, termo, baixadas):
    from PIL import Image, ImageDraw
    if not baixadas:
        return None
    cw, ch, cols = 360, 480, 3
    linhas = (len(baixadas) + cols - 1) // cols
    folha = Image.new("RGB", (cols * cw, linhas * (ch + 40)), (24, 22, 28))
    d = ImageDraw.Draw(folha)
    for k, (nome, item) in enumerate(baixadas):
        x, y = (k % cols) * cw, (k // cols) * (ch + 40)
        try:
            im = Image.open(saida / nome).convert("RGB")
            im.thumbnail((cw - 16, ch - 16))
            folha.paste(im, (x + (cw - im.width) // 2, y + (ch - im.height) // 2))
        except Exception:
            pass
        d.text((x + 8, y + ch + 4), f"{k + 1}. {nome}", fill=(255, 230, 0))
        d.text((x + 8, y + ch + 20), f"{item['w']}x{item['h']} · {item['licenca']}"[:58], fill=(200, 200, 200))
    caminho = saida / f"busca-{slug(termo)}.png"
    folha.save(caminho)
    return caminho


# ------------------------------------------------------------------ principal

def baixar_imagem(item, destino_sem_ext):
    from PIL import Image
    cru = pegar(item["url"], timeout=120)
    im = Image.open(io.BytesIO(cru))
    tem_alfa = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if tem_alfa else "RGB")
    if max(im.size) > LADO_MAX:
        f = LADO_MAX / max(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    ext = ".png" if tem_alfa else ".jpg"
    caminho = destino_sem_ext.with_suffix(ext)
    if tem_alfa:
        im.save(caminho, "PNG", optimize=True)
    else:
        im.save(caminho, "JPEG", quality=90)
    item["w"], item["h"] = im.size
    return caminho


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("termos", nargs="+", help="o que buscar (um ou mais termos)")
    ap.add_argument("--saida", required=True, help="pasta onde as imagens e o CREDITOS.md ficam")
    ap.add_argument("--quantos", type=int, default=6, help="quantas baixar por termo (padrão 6)")
    ap.add_argument("--licenca", choices=["livre", "credito"], default="livre")
    ap.add_argument("--orientacao", choices=["qualquer", "vertical", "horizontal", "quadrada"], default="qualquer")
    ap.add_argument("--min", type=int, default=1080, help="lado maior mínimo em px (padrão 1080)")
    ap.add_argument("--fontes", default="", help="lista separada por vírgula (padrão: todas as disponíveis)")
    ap.add_argument("--sem-fundo", action="store_true", help="recorta cada imagem baixada (tirar-fundo.py)")
    args = ap.parse_args()

    saida = Path(args.saida).expanduser()
    saida.mkdir(parents=True, exist_ok=True)
    env = ler_env()
    fontes = {"openverse": lambda t: buscar_openverse(t, args), "wikimedia": lambda t: buscar_wikimedia(t, args)}
    if env.get("PEXELS_API_KEY"):
        fontes["pexels"] = lambda t: buscar_pexels(t, args, env["PEXELS_API_KEY"])
    if env.get("PIXABAY_API_KEY"):
        fontes["pixabay"] = lambda t: buscar_pixabay(t, args, env["PIXABAY_API_KEY"])
    if args.fontes:
        pedidas = [f.strip() for f in args.fontes.split(",") if f.strip()]
        faltam = [f for f in pedidas if f not in fontes]
        if faltam:
            print(f"  aviso: sem acesso a {', '.join(faltam)} (falta a chave no .env?)")
        fontes = {k: v for k, v in fontes.items() if k in pedidas}
    print(f"bancos: {', '.join(fontes)}")

    ja = creditos_existentes(saida)
    total = 0
    for termo in args.termos:
        candidatos = []
        for nome_fonte, fn in fontes.items():
            try:
                achados = [c for c in fn(termo) if c.get("url")
                           and max(c.get("w") or 0, c.get("h") or 0) >= args.min
                           and orientacao_ok(c.get("w"), c.get("h"), args.orientacao)
                           and c["pagina"] not in ja]
            except Exception as e:
                print(f"  {nome_fonte}: falhou ({e})")
                continue
            print(f"  {nome_fonte}: {len(achados)} imagem(ns) para \"{termo}\"")
            candidatos.append(achados)
        # intercala os bancos, para a folha não vir toda de um lugar só
        fila = [c for grupo in zip(*[g + [None] * (max(map(len, candidatos or [[]])) - len(g)) for g in candidatos])
                for c in grupo if c] if candidatos else []
        baixadas = []
        for item in fila:
            if len(baixadas) >= args.quantos:
                break
            n = len(list(saida.glob(f"{slug(termo)}-*"))) + 1
            try:
                caminho = baixar_imagem(item, saida / f"{slug(termo)}-{n:02d}")
            except Exception as e:
                print(f"  pulei uma de {item['fonte']} ({e})")
                continue
            # o tamanho que o banco anuncia às vezes é o do original, e o arquivo servido é menor
            if max(item["w"], item["h"]) < args.min:
                caminho.unlink()
                continue
            registrar_credito(saida, caminho.name, item)
            baixadas.append((caminho.name, item))
            print(f"  ok  {caminho.name}  {item['w']}x{item['h']}  ·  {item['licenca']}  ·  {item['fonte']}")
            if args.sem_fundo:
                r = subprocess.run([sys.executable, str(AQUI / "tirar-fundo.py"), str(caminho)])
                if r.returncode != 0:
                    print("  o recorte falhou nesta imagem; a original ficou")
        folha = folha_de_contato(saida, termo, baixadas)
        if folha:
            print(f"  folha de contato: {folha}")
        total += len(baixadas)
    print(f"\n{total} imagem(ns) em {saida}; créditos em {saida / 'CREDITOS.md'}")
    sys.exit(0 if total else 1)


if __name__ == "__main__":
    main()
