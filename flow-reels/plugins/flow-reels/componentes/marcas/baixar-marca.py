#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
baixar-marca.py  ·  logos oficiais em cor, PNG sem fundo, para o vídeo

O acervo de logos/ guarda silhuetas de uma cor (Simple Icons), que o painel pinta com a tinta da
marca. Esta pasta guarda o outro caso: o logo oficial EM COR, do jeito que a própria marca publica,
em PNG transparente e grande o bastante para ocupar meio quadro de 1080 x 1920 sem borrar.

De onde vem
-----------
Em ordem de preferência:
1. o kit de imprensa da própria empresa (KITS abaixo: Anthropic e n8n);
2. o SVGL (svgl.app), acervo aberto de logos de tecnologia em SVG, em cor, com a versão para fundo
   claro e para fundo escuro e o link da página de marca de cada empresa (--lote tecnologia, ou
   --svgl "Título");
3. o Simple Icons (CC0) pintado na cor oficial publicada lá, só para marca de UMA cor que não está
   nos dois primeiros (SIMPLE_ICONS abaixo).
Para uma marca nova fora disso, passe o endereço do arquivo oficial (SVG ou PNG) com --url.

Kit que exige aceitar termo de uso (a OpenAI, por exemplo) não é baixado por este script: aceitar o
termo é uma decisão da pessoa, que baixa na mão e passa o arquivo local com --arquivo.

Uso
---
    flow-reels componentes/baixar-marca                          o que já existe no acervo
    flow-reels componentes/baixar-marca --kit anthropic n8n      baixa os kits conhecidos
    flow-reels componentes/baixar-marca --lote tecnologia        as ~85 marcas de tecnologia do LOTE (SVGL + Simple Icons)
    flow-reels componentes/baixar-marca --svgl "Cursor" "Supabase"   marcas avulsas do SVGL, pelo título de lá
    flow-reels componentes/baixar-marca --url https://.../logo.svg --nome supabase-logo --marca Supabase \\
                           --termos "https://supabase.com/brand-assets"
    flow-reels componentes/baixar-marca --arquivo ~/Downloads/chatgpt.svg --nome chatgpt-logo --marca ChatGPT \\
                           --origem "https://openai.com/brand/" --termos "termos de marca da OpenAI"

Cada PNG sai aparado (sem margem transparente sobrando), com no máximo 2400 px no lado maior, e
ganha uma ficha no _acervo.json: marca, variante, fundo indicado, origem e regras de uso.
"""

import argparse
import base64
import datetime
import io
import json
import os
import re
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# o que se baixa vai para a pasta de trabalho (componentes/marcas/), por cima do acervo que o pacote
# traz, e sobrevive a uma atualização do plugin; quem mantém o pacote passa --pacote
AQUI = (Path(__file__).resolve().parent if "--pacote" in sys.argv
        else fabrica.raiz() / "componentes" / "marcas")
AQUI.mkdir(parents=True, exist_ok=True)
ACERVO = AQUI / "_acervo.json"
LADO_MAX = 2400
NAVEGADOR = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")

# Os kits oficiais conhecidos. "arquivos" liga o caminho dentro do zip ao nome no acervo.
KITS = {
    "anthropic": {
        "url": "https://www.anthropic.com/press-kit",
        "origem": "https://www.anthropic.com/news (Download press kit)",
        "regras": "Marcas registradas da Anthropic. Uso editorial para se referir ao produto; não "
                  "alterar cores nem proporções; não sugerir parceria ou endosso.",
        "arquivos": {
            "Claude logos/1 Claude logo/PNG/Claude logo - Ivory.png":
                ("claude-logo", "Claude", "logo completo (faísca + nome)", "escuro"),
            "Claude logos/1 Claude logo/PNG/Claude logo - Slate.png":
                ("claude-logo-fundo-claro", "Claude", "logo completo (faísca + nome)", "claro"),
            "Claude logos/2 Claude Code logo/PNG/Claude Code logo - Ivory.png":
                ("claude-code-logo", "Claude Code", "logo completo (faísca + nome)", "escuro"),
            "Claude logos/2 Claude Code logo/PNG/Claude Code logo - Slate.png":
                ("claude-code-logo-fundo-claro", "Claude Code", "logo completo (faísca + nome)", "claro"),
            "Claude logos/3 Claude Spark/PNG/Claude Spark - Clay.png":
                ("claude-faisca", "Claude", "símbolo (a faísca, cor Clay)", "qualquer"),
            "Claude logos/4 Claude icon/PNG/ClaudeIcon-Rounded.png":
                ("claude-icone", "Claude", "ícone do app (cantos arredondados)", "qualquer"),
            "Anthropic logos/1 Anthropic logo/PNG/Anthropic logo - Ivory.png":
                ("anthropic-logo", "Anthropic", "logo completo", "escuro"),
            "Anthropic logos/1 Anthropic logo/PNG/Anthropic logo - Slate.png":
                ("anthropic-logo-fundo-claro", "Anthropic", "logo completo", "claro"),
            "Anthropic logos/2 Anthropic symbol/PNG/Anthropic symbol - Ivory.png":
                ("anthropic-simbolo", "Anthropic", "símbolo (A\\)", "escuro"),
            "Anthropic logos/2 Anthropic symbol/PNG/Anthropic symbol - Slate.png":
                ("anthropic-simbolo-fundo-claro", "Anthropic", "símbolo (A\\)", "claro"),
        },
    },
    "n8n": {
        "url": "https://n8n.io/brandguidelines/n8n_logos.zip",
        "origem": "https://n8n.io/brandguidelines/",
        "regras": "Marca da n8n. Só nas cores oficiais (rosa #EA4B71 com branco ou preto); sem sombra, "
                  "sem inclinar, sem esticar, sem fundo carregado; 4x de espaço livre; nunca o nome "
                  "sozinho sem o ícone; no mínimo 100 px de largura.",
        "arquivos": {
            "n8n_pink+white_logo.svg": ("n8n-logo", "n8n", "logo completo (ícone + nome)", "escuro"),
            "n8n_pink+black_logo.svg": ("n8n-logo-fundo-claro", "n8n", "logo completo (ícone + nome)", "claro"),
            # o ícone sozinho é o primeiro desenho do SVG oficial, o rosa (o nome vem depois, em branco)
            "n8n_pink+white_logo.svg#icone": ("n8n-icone", "n8n", "ícone (rosa #EA4B71)", "qualquer"),
        },
    },
}


# O lote de tecnologia: (título no SVGL, nome no acervo, pedaço da url da marca para desempatar).
# Claude, Anthropic e n8n vêm dos kits oficiais; a OpenAI (ChatGPT, Codex) pede aceite de termo e
# entra pelo --arquivo, depois que a pessoa baixar o kit dela.
LOTE_TECNOLOGIA = [
    # IA: modelos, laboratórios e ferramentas
    ("Gemini", "gemini", None), ("Google", "google", None), ("DeepSeek", "deepseek", None),
    ("Mistral AI", "mistral", None), ("Grok", "grok", None), ("xAI", "xai", None), ("Meta", "meta", None),
    ("Microsoft Copilot", "microsoft-copilot", None), ("Perplexity AI", "perplexity", None),
    ("Hugging Face", "huggingface", None), ("Ollama", "ollama", None), ("Qwen", "qwen", None),
    ("Kimi", "kimi", None), ("Manus", "manus", None), ("Midjourney", "midjourney", None),
    ("Runway", "runway", None), ("Suno", "suno", None), ("NVIDIA", "nvidia", None),
    ("OpenRouter", "openrouter", None), ("Groq", "groq", None), ("Model Context Protocol", "mcp", None),
    ("LangChain", "langchain", None), ("Google Antigravity", "antigravity", None),
    # programação e infraestrutura
    ("Cursor", "cursor", None), ("GitHub", "github", None), ("GitHub Copilot", "github-copilot", None),
    ("Visual Studio Code", "vscode", None), ("Windsurf", "windsurf", None), ("Lovable", "lovable", None),
    ("bolt", "bolt", None), ("Replit", "replit", None), ("Firebase", "firebase", None),
    ("Vercel", "vercel", None), ("Supabase", "supabase", None), ("Next.js", "nextjs", None),
    ("React", "react", None), ("Python", "python", None), ("Node.js", "nodejs", None),
    ("JavaScript", "javascript", None), ("TypeScript", "typescript", None), ("Tailwind CSS", "tailwind", None),
    ("Docker", "docker", None), ("PostgreSQL", "postgresql", None), ("MongoDB", "mongodb", None),
    ("Redis", "redis", None), ("Cloudflare", "cloudflare", None), ("Netlify", "netlify", None),
    ("Railway", "railway", None), ("Render", "render", None), ("Amazon Web Services", "aws", None),
    ("Google Cloud", "google-cloud", None), ("Microsoft Azure", "azure", None), ("Linux", "linux", None),
    ("Ubuntu", "ubuntu", None), ("Postman", "postman", None),
    # automação e trabalho
    ("Stripe", "stripe", None), ("Notion", "notion", None), ("Slack", "slack", None), ("Trello", "trello", None),
    ("Asana", "asana", None), ("Google Sheets", "google-sheets", None), ("Gmail", "gmail", None),
    ("Google Drive", "google-drive", None), ("Microsoft Excel", "excel", None), ("Microsoft Teams", "teams", None),
    ("Microsoft Outlook", "outlook", None), ("Salesforce", "salesforce", None), ("Figma", "figma", None),
    ("Canva", "canva", None), ("Zoom", "zoom", None),
    # comunicação e redes
    ("WhatsApp", "whatsapp", None), ("Telegram", "telegram", None), ("Instagram", "instagram", None),
    ("YouTube", "youtube", None), ("TikTok", "tiktok", None), ("X (formerly Twitter)", "x", None),
    ("LinkedIn", "linkedin", None), ("Discord", "discord", None),
    # navegadores e sistemas
    ("Chrome", "chrome", None), ("Firefox", "firefox", None), ("Safari", "safari", None), ("Edge", "edge", None),
    ("Brave Browser", "brave", None), ("Arc", "arc", "arc.net"), ("Apple", "apple", None),
    ("Windows", "windows", None), ("Microsoft", "microsoft", None),
]

# Marca de uma cor só que falta nos kits e no SVGL: o desenho CC0 do Simple Icons na cor oficial.
# (slug no Simple Icons, nome no acervo, marca, cor para fundo escuro, cor para fundo claro)
SIMPLE_ICONS = [
    ("zapier", "zapier", "Zapier", "#FF4F00", "#FF4F00"),
    ("make", "make", "Make", "#6D00CC", "#6D00CC"),
    ("hubspot", "hubspot", "HubSpot", "#FF7A59", "#FF7A59"),
    ("elevenlabs", "elevenlabs", "ElevenLabs", "#FFFFFF", "#000000"),
]

SVGL_API = "https://api.svgl.app"


def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": NAVEGADOR})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read(), r.geturl()


def ler_acervo():
    if ACERVO.is_file():
        return json.loads(ACERVO.read_text(encoding="utf-8"))
    return {}


def gravar_acervo(dados):
    ACERVO.write_text(json.dumps(dict(sorted(dados.items())), ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")


def so_icone_n8n(svg):
    """O SVG do n8n traz o ícone (o desenho rosa) e o nome (branco). Fica só o ícone, com o recorte
    da caixa dele: 304 x 160 no desenho original."""
    caminhos = re.findall(r"<path[^>]*/>", svg, flags=re.S)
    rosa = [c for c in caminhos if "#EA4B71" in c.upper()]
    if not rosa:
        raise ValueError("não achei o desenho rosa do ícone no SVG do n8n")
    return ('<svg width="304" height="160" viewBox="0 0 304 160" fill="none" '
            'xmlns="http://www.w3.org/2000/svg">' + rosa[0] + "</svg>")


class Renderizador:
    """SVG para PNG transparente, no Chromium do pacote (o mesmo do compositor). Um navegador só para
    o lote inteiro."""

    def __enter__(self):
        from playwright.sync_api import sync_playwright
        self._p = sync_playwright().start()
        self._nav = self._p.chromium.launch()
        self._pag = self._nav.new_page(viewport={"width": 1700, "height": 1700})
        return self

    def __exit__(self, *a):
        self._nav.close()
        self._p.stop()

    def png(self, svg_texto, lado):
        """Renderiza com o lado MAIOR igual a `lado` px."""
        b64 = base64.b64encode(svg_texto.encode("utf-8")).decode("ascii")
        self._pag.set_content("<html><body style='margin:0;background:transparent'>"
                              f"<img id='l' src='data:image/svg+xml;base64,{b64}' style='display:block'>"
                              "</body></html>")
        self._pag.wait_for_function("document.getElementById('l').complete")
        w, h = self._pag.evaluate("(() => { const i = document.getElementById('l');"
                                  " return [i.naturalWidth || 100, i.naturalHeight || 100]; })()")
        f = lado / max(w, h)
        self._pag.set_viewport_size({"width": int(w * f) + 20, "height": int(h * f) + 20})
        self._pag.evaluate(f"(() => {{ const i = document.getElementById('l'); i.style.width = '{w * f:.1f}px';"
                           f" i.style.height = '{h * f:.1f}px'; }})()")
        return self._pag.locator("#l").screenshot(omit_background=True)


def renderizar_svg(svg_texto, largura):
    with Renderizador() as r:
        return r.png(svg_texto, largura)


def fundo_pela_cor(png_bytes):
    """Logo de uma versão só: escuro demais pede fundo claro; branco pede fundo escuro."""
    import numpy as np
    from PIL import Image
    im = np.asarray(Image.open(io.BytesIO(png_bytes)).convert("RGBA")).astype("float32") / 255.0
    a = im[..., 3] > 0.5
    if not a.any():
        return "qualquer"
    rgb = im[..., :3][a]
    lum = (0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2])
    escuros = (lum < 0.12).mean()
    claros = (lum > 0.9).mean()
    if escuros > 0.85:
        return "claro"
    if claros > 0.85:
        return "escuro"
    return "qualquer"


def aparar(png_bytes):
    """Tira a margem transparente, limita o lado maior e devolve (bytes, largura, altura)."""
    from PIL import Image
    im = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    caixa = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if caixa:
        im = im.crop(caixa)
    if max(im.size) > LADO_MAX:
        f = LADO_MAX / max(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    saida = io.BytesIO()
    im.save(saida, "PNG", optimize=True)
    return saida.getvalue(), im.width, im.height


def registrar(dados, nome, marca, variante, fundo, origem, arquivo_fonte, regras):
    dados[nome] = {
        "arquivo": nome + ".png",
        "marca": marca,
        "variante": variante,
        "fundo": {"escuro": "use sobre fundo escuro", "claro": "use sobre fundo claro",
                  "qualquer": "funciona nos dois"}.get(fundo, fundo),
        "origem": origem,
        "arquivo_na_fonte": arquivo_fonte,
        "regras": regras,
        "baixado_em": datetime.date.today().isoformat(),
    }


def gravar_png(nome, png_bytes):
    png, w, h = aparar(png_bytes)
    (AQUI / (nome + ".png")).write_bytes(png)
    print(f"  ok  {nome}.png  {w}x{h}")


def kit(chave, dados):
    k = KITS[chave]
    print(f"\n{chave}: baixando {k['url']}")
    cru, final = baixar(k["url"])
    z = zipfile.ZipFile(io.BytesIO(cru))
    nomes = [n for n in z.namelist() if not n.startswith("__MACOSX") and not n.endswith(".DS_Store")]
    for dentro, (nome, marca, variante, fundo) in k["arquivos"].items():
        caminho, _, parte = dentro.partition("#")
        achado = next((n for n in nomes if n.endswith(caminho)), None)
        if not achado:
            print(f"  falta  {caminho} (o kit mudou? confira {k['origem']})")
            continue
        conteudo = z.read(achado)
        if achado.lower().endswith(".svg"):
            svg = conteudo.decode("utf-8")
            if parte == "icone":
                svg = so_icone_n8n(svg)
            conteudo = renderizar_svg(svg, 1600)
        gravar_png(nome, conteudo)
        registrar(dados, nome, marca, variante, fundo, k["origem"], f"{final} → {achado}", k["regras"])


def avulso(args, dados):
    if args.url:
        conteudo, origem_arquivo = baixar(args.url)
    else:
        conteudo, origem_arquivo = Path(args.arquivo).expanduser().read_bytes(), str(args.arquivo)
    if conteudo[:2] == b"PK":
        print("  é um zip: extraia, escolha a variante e passe o arquivo com --arquivo")
        sys.exit(1)
    if conteudo.lstrip()[:5] in (b"<?xml", b"<svg ") or conteudo.lstrip()[:4] == b"<svg":
        conteudo = renderizar_svg(conteudo.decode("utf-8"), 1600)
    gravar_png(args.nome, conteudo)
    registrar(dados, args.nome, args.marca or args.nome, args.variante or "logo", args.fundo,
              args.origem or args.url or "", origem_arquivo, args.termos or "")


def catalogo_svgl():
    cru, _ = baixar(SVGL_API)
    return json.loads(cru.decode("utf-8"))


def achar_svgl(cat, titulo, pista=None):
    candidatos = [e for e in cat if e.get("title", "").lower() == titulo.lower()]
    if pista:
        candidatos = [e for e in candidatos if pista in (e.get("url") or "")] or candidatos
    return candidatos[0] if candidatos else None


def importar_svgl(dados, pedidos, cat=None):
    """pedidos: [(título no SVGL, nome no acervo, pista)]"""
    cat = cat or catalogo_svgl()
    faltou = []
    with Renderizador() as r:
        for titulo, nome, pista in pedidos:
            e = achar_svgl(cat, titulo, pista)
            if not e:
                faltou.append(titulo)
                print(f"  falta  {titulo} (não está no SVGL)")
                continue
            origem = e.get("brandUrl") or e.get("url") or ""
            regras = ("Marca registrada da empresa. Uso para se referir ao produto, sem alterar cor nem "
                      "proporção e sem sugerir parceria." + (f" Guia: {e['brandUrl']}" if e.get("brandUrl") else ""))
            for chave, sufixo, lado, variante in (("route", "icone", 1024, "ícone"),
                                                  ("wordmark", "logo", 1600, "logo com nome")):
                fonte = e.get(chave)
                if not fonte:
                    continue
                versoes = ([("dark", "", "escuro"), ("light", "-fundo-claro", "claro")]
                           if isinstance(fonte, dict) else [(None, "", None)])
                for k, fim, fundo in versoes:
                    url = fonte[k] if k else fonte
                    try:
                        svg, _ = baixar(url)
                        png = r.png(svg.decode("utf-8"), lado)
                    except Exception as erro:
                        print(f"  falhou {titulo} {sufixo}{fim} ({erro})")
                        continue
                    nome_arq = f"{nome}-{sufixo}{fim}"
                    gravar_png(nome_arq, png)
                    registrar(dados, nome_arq, e["title"], variante, fundo or fundo_pela_cor(png), origem,
                              url + " (SVGL, svgl.app)", regras)
    return faltou


def importar_simple_icons(dados):
    with Renderizador() as r:
        for slug, nome, marca, cor_escuro, cor_claro in SIMPLE_ICONS:
            url = f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"
            try:
                svg, _ = baixar(url)
            except Exception as erro:
                print(f"  falhou {marca} ({erro})")
                continue
            svg = svg.decode("utf-8")
            versoes = [("", cor_escuro, "escuro"), ("-fundo-claro", cor_claro, "claro")]
            if cor_escuro == cor_claro:
                versoes = [("", cor_escuro, "qualquer")]
            for fim, cor, fundo in versoes:
                pintado = svg.replace("<svg ", f'<svg fill="{cor}" ', 1)
                png = r.png(pintado, 1024)
                nome_arq = f"{nome}-icone{fim}"
                gravar_png(nome_arq, png)
                registrar(dados, nome_arq, marca, f"ícone (desenho CC0 do Simple Icons na cor oficial {cor})",
                          fundo, f"https://simpleicons.org/?q={slug}", url,
                          "Marca registrada da empresa. Uso para se referir ao produto.")


def listar(dados):
    if not dados:
        print("o acervo de marcas em cor está vazio")
        return
    print(f"{len(dados)} logos em cor no acervo:\n")
    for nome, f in dados.items():
        print(f"  {nome + '.png':36s} {f['marca']:12s} {f['variante']}  ·  {f['fundo']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kit", nargs="+", choices=sorted(KITS), help="kits oficiais conhecidos")
    ap.add_argument("--lote", choices=["tecnologia"], help="o lote de marcas de tecnologia (SVGL + Simple Icons)")
    ap.add_argument("--svgl", nargs="+", help="marcas avulsas do SVGL, pelo título de lá")
    ap.add_argument("--url", help="endereço oficial de um SVG ou PNG")
    ap.add_argument("--arquivo", help="arquivo oficial já baixado (SVG ou PNG)")
    ap.add_argument("--nome", help="nome no acervo, sem extensão (ex.: supabase-logo)")
    ap.add_argument("--marca", help="nome da marca, como ela escreve")
    ap.add_argument("--variante", help="logo completo, símbolo, ícone...")
    ap.add_argument("--fundo", default="escuro", choices=["escuro", "claro", "qualquer"])
    ap.add_argument("--origem", help="a página oficial de onde veio")
    ap.add_argument("--termos", help="as regras de uso da marca, em uma linha")
    ap.add_argument("--pacote", action="store_true", help="grava no plugin, e não na pasta de trabalho")
    args = ap.parse_args()

    dados = ler_acervo()
    if args.lote:
        print(f"lote {args.lote}: {len(LOTE_TECNOLOGIA)} marcas do SVGL e {len(SIMPLE_ICONS)} do Simple Icons")
        faltou = importar_svgl(dados, LOTE_TECNOLOGIA)
        importar_simple_icons(dados)
        if faltou:
            print("não achei no SVGL: " + ", ".join(faltou))
    elif args.svgl:
        importar_svgl(dados, [(t, re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-"), None) for t in args.svgl])
    elif args.kit:
        for k in args.kit:
            kit(k, dados)
    elif args.url or args.arquivo:
        if not args.nome:
            ap.error("--nome é obrigatório com --url ou --arquivo")
        avulso(args, dados)
    else:
        listar(dados)
        return
    gravar_acervo(dados)
    print("\nficha gravada em _acervo.json")


if __name__ == "__main__":
    main()
