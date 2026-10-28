#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
buscar_tendencias.py  ·  levanta o que está subindo em IA e automação

Varre as fontes onde as novidades de IA, automação, n8n, Claude Code e Codex
aparecem primeiro, e grava uma lista crua de candidatos em JSON. Ele NÃO julga
nada: quem escolhe a pauta é o agente, com referencias/CRITERIOS.md. Este script
só junta, remove repetido e anota o sinal de tração de cada item.

Fontes, na ordem em que são lidas:

  reddit     os subreddits de setup.json -> pautas.subreddits (top da janela).
             Com REDDIT_CLIENT_ID e REDDIT_CLIENT_SECRET no .env usa a API
             oficial. Sem a chave, usa a listagem do shreddit da busca do radar
             (scripts/radar/lib/reddit_listagem.py), que traz voto e contagem de
             comentários de verdade sem chave nenhuma. O RSS público, que o
             Reddit corta depois de poucas leituras, ficou só de reserva para o
             subreddit que a listagem não trouxe.
  youtube    as buscas de setup.json -> pautas.youtube, enviados na janela, em
             português e região Brasil, com visualizações, pelo yt-dlp (o do
             PATH ou o do .venv). Sem a lista no setup, o YouTube não roda.
  github     trending da semana (ou do dia) e repositórios novos com muitas
             estrelas nos tópicos de IA.
  hackernews histórias da janela com pontos, filtradas pelos termos do nicho.
  producthunt o feed de lançamentos, filtrado pelos termos do nicho.

Uso:

    flow-reels tendencias/buscar_tendencias --saida projetos/_pautas/2026-09-25/tendencias.json
    flow-reels tendencias/buscar_tendencias --janela dia --saida <arquivo>
    flow-reels tendencias/buscar_tendencias --fontes github,hackernews --saida <arquivo>

Para uma busca por tema (não pelo nicho inteiro), o caminho é o radar:
scripts/radar/radar.py "<tema>" --termo-en "<tema em inglês>".

A saída é uma lista de itens com: fonte, titulo, url, link_externo, tracao
(o número que a fonte dá: upvotes, estrelas, pontos), comentarios, data,
resumo e termos (quais termos do nicho bateram).
"""

import argparse
import html
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    import requests
except ImportError:
    print("  erro: falta a biblioteca requests. Rode com .venv/bin/python ou: pip install requests",
          file=sys.stderr)
    sys.exit(2)


RAIZ = fabrica.raiz()

# a busca do radar mora ao lado: o Reddit sem chave e o YouTube vêm de lá
sys.path.insert(0, str(Path(__file__).resolve().parent / "radar"))
from lib import reddit_listagem, youtube  # noqa: E402
UA = "fabrica-de-cortes/0.1 (pesquisa de pautas de conteudo)"
ATOM = {"a": "http://www.w3.org/2005/Atom"}

PADRAO = {
    "subreddits": ["ClaudeAI", "ClaudeCode", "n8n", "OpenAI", "ChatGPT", "ChatGPTCoding",
                   "LocalLLaMA", "AI_Agents", "automation", "singularity", "vibecoding"],
    "termos": ["claude", "anthropic", "codex", "openai", "gpt", "gemini", "llm", "agent", "agente",
               "mcp", "n8n", "automation", "automação", "workflow", "ai ", " ai", "ia ",
               "open source", "open-source", "free", "gratuito", "copilot", "cursor", "vibe",
               "voice", "video", "image", "rag", "skill", "plugin", "local model", "ollama"],
}


def fala(msg):
    print(msg, file=sys.stderr)


def ler_config():
    cfg = dict(PADRAO)
    setup = RAIZ / "setup.json"
    if setup.is_file():
        try:
            dados = json.loads(setup.read_text(encoding="utf-8")).get("pautas", {})
            for chave in ("subreddits", "termos", "youtube"):
                if dados.get(chave):
                    cfg[chave] = dados[chave]
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def ler_env():
    env = {}
    arq = RAIZ / ".env"
    if arq.is_file():
        for linha in arq.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if k.startswith("REDDIT_")})
    return env


def termos_que_batem(texto, termos):
    t = " " + (texto or "").lower() + " "
    return sorted({x.strip() for x in termos if x in t})


def limpar(texto, n=400):
    texto = re.sub(r"<[^>]+>", " ", html.unescape(texto or ""))
    return re.sub(r"\s+", " ", texto).strip()[:n]


# ----------------------------------------------------------------------------- reddit

def reddit_api(subs, janela, env):
    r = requests.post("https://www.reddit.com/api/v1/access_token",
                      auth=(env["REDDIT_CLIENT_ID"], env["REDDIT_CLIENT_SECRET"]),
                      data={"grant_type": "client_credentials"},
                      headers={"User-Agent": UA}, timeout=20)
    r.raise_for_status()
    token = r.json()["access_token"]
    cab = {"Authorization": "bearer " + token, "User-Agent": UA}
    itens, falhas = [], []
    for sub in subs:
        try:
            resp = requests.get("https://oauth.reddit.com/r/%s/top" % sub,
                                params={"t": janela, "limit": 25}, headers=cab, timeout=20)
            resp.raise_for_status()
        except requests.RequestException as e:
            falhas.append("%s (%s)" % (sub, e))
            continue
        for c in resp.json().get("data", {}).get("children", []):
            d = c["data"]
            itens.append({
                "fonte": "reddit/r/" + sub,
                "titulo": d.get("title", ""),
                "url": "https://www.reddit.com" + d.get("permalink", ""),
                "link_externo": None if d.get("is_self") else d.get("url"),
                "tracao": d.get("score", 0),
                "comentarios": d.get("num_comments", 0),
                "data": datetime.fromtimestamp(d.get("created_utc", 0), timezone.utc).isoformat(),
                "resumo": limpar(d.get("selftext", "")),
            })
        time.sleep(1)
    return itens, falhas


def reddit_listagem_sem_chave(subs, janela):
    """O top de cada subreddit pela listagem do shreddit: voto e comentários reais, sem chave."""
    cartoes = reddit_listagem.buscar(subs, ordens=["top"], periodo=janela)
    itens, achados = [], set()
    for c in cartoes:
        sub = c.get("comunidade") or ""
        achados.add(sub.lower())
        eng = c.get("engajamento") or {}
        itens.append({
            "fonte": "reddit/r/" + sub,
            "titulo": c.get("titulo", ""),
            "url": c.get("url", ""),
            "link_externo": None,
            "tracao": eng.get("votos"),
            "comentarios": eng.get("comentarios"),
            "data": c.get("data") or "",
            "resumo": "",
        })
    faltaram = [s for s in subs if s.lower() not in achados]
    return itens, faltaram


def reddit_rss(subs, janela):
    itens, falhas = [], []
    for i, sub in enumerate(subs):
        if i:
            time.sleep(6)  # o RSS público corta com 429 se as chamadas vêm coladas
        url = "https://www.reddit.com/r/%s/top/.rss?t=%s" % (sub, janela)
        conteudo = None
        for tentativa in range(3):
            try:
                resp = requests.get(url, headers={"User-Agent": UA}, timeout=20)
            except requests.RequestException as e:
                falhas.append("%s (%s)" % (sub, e))
                break
            if resp.status_code == 200 and resp.content:
                conteudo = resp.content
                break
            time.sleep(15 * (tentativa + 1))
        if conteudo is None:
            if not falhas or not falhas[-1].startswith(sub):
                falhas.append("%s (o Reddit limitou o acesso sem chave)" % sub)
            continue
        try:
            raiz = ET.fromstring(conteudo)
        except ET.ParseError:
            falhas.append("%s (resposta ilegível)" % sub)
            continue
        entradas = raiz.findall("a:entry", ATOM)
        for pos, e in enumerate(entradas):
            corpo = e.findtext("a:content", default="", namespaces=ATOM)
            externo = None
            m = re.search(r'<a href="([^"]+)">\[link\]</a>', corpo)
            if m and "reddit.com" not in m.group(1):
                externo = html.unescape(m.group(1))
            itens.append({
                "fonte": "reddit/r/" + sub,
                "titulo": e.findtext("a:title", default="", namespaces=ATOM),
                "url": e.find("a:link", ATOM).get("href"),
                "link_externo": externo,
                # o RSS não traz score: a posição no top da janela é o sinal
                "tracao": None,
                "posicao_no_top": pos + 1,
                "comentarios": None,
                "data": e.findtext("a:updated", default="", namespaces=ATOM),
                "resumo": limpar(corpo),
            })
    return itens, falhas


# ----------------------------------------------------------------------------- github

def github(janela):
    itens, falhas = [], []
    periodo = "daily" if janela == "day" else "weekly"
    try:
        h = requests.get("https://github.com/trending?since=" + periodo,
                         headers={"User-Agent": UA}, timeout=20).text
        for bloco in re.findall(r'<article class="Box-row">(.*?)</article>', h, re.S):
            m = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', bloco, re.S)
            if not m:
                continue
            repo = m.group(1).strip()
            desc = re.search(r'<p class="[^"]*col-9[^"]*">\s*(.*?)\s*</p>', bloco, re.S)
            ganho = re.search(r"([\d,]+) stars (this week|today)", bloco)
            total = re.search(r'href="/%s/stargazers"[^>]*>.*?([\d,]+)\s*</a>' % re.escape(repo), bloco, re.S)
            itens.append({
                "fonte": "github/trending",
                "titulo": repo,
                "url": "https://github.com/" + repo,
                "link_externo": None,
                "tracao": int(ganho.group(1).replace(",", "")) if ganho else None,
                "tracao_tipo": "estrelas na janela",
                "estrelas_total": int(total.group(1).replace(",", "")) if total else None,
                "comentarios": None,
                "data": None,
                "resumo": limpar(desc.group(1)) if desc else "",
            })
    except requests.RequestException as e:
        falhas.append("trending (%s)" % e)

    desde = (datetime.now(timezone.utc) - timedelta(days=2 if janela == "day" else 14)).date()
    for topico in ("ai", "llm", "mcp", "ai-agents", "n8n", "claude"):
        try:
            r = requests.get("https://api.github.com/search/repositories",
                             params={"q": "created:>%s topic:%s" % (desde, topico),
                                     "sort": "stars", "order": "desc", "per_page": 10},
                             headers={"User-Agent": UA, "Accept": "application/vnd.github+json"},
                             timeout=20)
            r.raise_for_status()
        except requests.RequestException as e:
            falhas.append("busca topic:%s (%s)" % (topico, e))
            continue
        for d in r.json().get("items", []):
            itens.append({
                "fonte": "github/novos",
                "titulo": d["full_name"],
                "url": d["html_url"],
                "link_externo": d.get("homepage") or None,
                "tracao": d.get("stargazers_count", 0),
                "tracao_tipo": "estrelas totais (repositório novo)",
                "comentarios": None,
                "data": d.get("created_at"),
                "resumo": limpar(d.get("description") or ""),
            })
        time.sleep(1)
    return itens, falhas


# ----------------------------------------------------------------------------- hacker news

def hackernews(janela, termos):
    itens, falhas = [], []
    desde = int(time.time() - (86400 if janela == "day" else 7 * 86400))
    for consulta in ("AI", "LLM", "Claude", "OpenAI", "agent", "MCP", "automation", "open source model"):
        try:
            r = requests.get("https://hn.algolia.com/api/v1/search",
                             params={"tags": "story", "query": consulta,
                                     "numericFilters": "created_at_i>%d,points>40" % desde,
                                     "hitsPerPage": 20},
                             headers={"User-Agent": UA}, timeout=20)
            r.raise_for_status()
        except requests.RequestException as e:
            falhas.append("%s (%s)" % (consulta, e))
            continue
        for d in r.json().get("hits", []):
            itens.append({
                "fonte": "hackernews",
                "titulo": d.get("title") or "",
                "url": "https://news.ycombinator.com/item?id=%s" % d.get("objectID"),
                "link_externo": d.get("url"),
                "tracao": d.get("points", 0),
                "comentarios": d.get("num_comments", 0),
                "data": d.get("created_at"),
                "resumo": "",
            })
    return itens, falhas


# ----------------------------------------------------------------------------- product hunt

def producthunt(termos):
    itens, falhas = [], []
    try:
        r = requests.get("https://www.producthunt.com/feed", headers={"User-Agent": UA}, timeout=20)
        r.raise_for_status()
        raiz = ET.fromstring(r.content)
    except (requests.RequestException, ET.ParseError) as e:
        return itens, ["feed (%s)" % e]
    for e in raiz.findall("a:entry", ATOM):
        titulo = e.findtext("a:title", default="", namespaces=ATOM)
        resumo = limpar(e.findtext("a:content", default="", namespaces=ATOM))
        itens.append({
            "fonte": "producthunt",
            "titulo": titulo,
            "url": e.find("a:link", ATOM).get("href"),
            "link_externo": None,
            "tracao": None,
            "comentarios": None,
            "data": e.findtext("a:published", default="", namespaces=ATOM),
            "resumo": resumo,
        })
    return itens, falhas


# ----------------------------------------------------------------------------- youtube

def buscar_youtube(buscas, janela):
    """Os vídeos enviados na janela para cada busca do nicho, com visualizações."""
    if not youtube.disponivel():
        return [], ["yt-dlp não instalado (pip install yt-dlp no .venv)"]
    dias = 1 if janela == "dia" else 7
    itens, falhas = [], []
    for busca in buscas:
        achados = youtube.buscar(busca, dias=dias, profundidade="rapida", idioma="pt")
        if not achados:
            falhas.append("%s (nada na janela, ou o yt-dlp não respondeu)" % busca)
        for v in achados:
            itens.append({
                "fonte": "youtube",
                "titulo": v.get("titulo", ""),
                "url": v.get("url", ""),
                "link_externo": None,
                "tracao": (v.get("engajamento") or {}).get("visualizacoes"),
                "comentarios": None,
                "data": "",
                "resumo": (v.get("resumo") or "")[:400],
                "canal": v.get("autor", ""),
                "busca": busca,
                "transcricao": (v.get("transcricao") or "")[:1500],
            })
    return itens, falhas


# ----------------------------------------------------------------------------- principal

def main():
    ap = argparse.ArgumentParser(description="Levanta tendências de IA e automação em várias fontes.")
    ap.add_argument("--saida", required=True, help="arquivo JSON de saída")
    ap.add_argument("--janela", choices=["dia", "semana"], default="semana")
    ap.add_argument("--fontes", default="reddit,youtube,github,hackernews,producthunt",
                    help="lista separada por vírgula")
    args = ap.parse_args()

    cfg = ler_config()
    env = ler_env()
    janela = "day" if args.janela == "dia" else "week"
    fontes = [f.strip() for f in args.fontes.split(",") if f.strip()]

    todos, relatorio = [], {}

    if "reddit" in fontes:
        if env.get("REDDIT_CLIENT_ID") and env.get("REDDIT_CLIENT_SECRET"):
            fala("  reddit: API oficial, %d subreddits" % len(cfg["subreddits"]))
            try:
                itens, falhas = reddit_api(cfg["subreddits"], janela, env)
            except requests.RequestException as e:
                fala("  reddit: a chave não funcionou (%s). Caindo no RSS." % e)
                itens, falhas = reddit_rss(cfg["subreddits"], janela)
        else:
            fala("  reddit: sem chave, pela listagem do shreddit (%d subreddits)"
                 % len(cfg["subreddits"]))
            itens, faltaram = reddit_listagem_sem_chave(cfg["subreddits"], janela)
            falhas = []
            if faltaram:
                fala("  reddit: a listagem não trouxe %s; tentando pelo RSS" % ", ".join(faltaram))
                extra, falhas = reddit_rss(faltaram, janela)
                itens += extra
        todos += itens
        relatorio["reddit"] = {"itens": len(itens), "falhas": falhas}

    if "youtube" in fontes and cfg.get("youtube"):
        fala("  youtube: %d buscas, região Brasil" % len(cfg["youtube"]))
        itens, falhas = buscar_youtube(cfg["youtube"], args.janela)
        todos += itens
        relatorio["youtube"] = {"itens": len(itens), "falhas": falhas}

    for nome, func in (("github", lambda: github(janela)),
                       ("hackernews", lambda: hackernews(janela, cfg["termos"])),
                       ("producthunt", lambda: producthunt(cfg["termos"]))):
        if nome in fontes:
            fala("  %s..." % nome)
            itens, falhas = func()
            todos += itens
            relatorio[nome] = {"itens": len(itens), "falhas": falhas}

    # anota os termos do nicho e tira repetido pela url (e pelo link externo)
    vistos, unicos = set(), []
    for it in todos:
        chaves = {it["url"]} | ({it["link_externo"]} if it.get("link_externo") else set())
        if chaves & vistos:
            continue
        vistos |= chaves
        it["termos"] = termos_que_batem(it["titulo"] + " " + it.get("resumo", ""), cfg["termos"])
        unicos.append(it)

    # reddit, youtube e github já são do nicho pela origem; hn e product hunt precisam bater termo
    filtrados = [it for it in unicos
                 if it["fonte"].startswith(("reddit", "youtube", "github")) or it["termos"]]

    saida = Path(args.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps({
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "janela": args.janela,
        "fontes": relatorio,
        "itens": filtrados,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    fala("")
    for nome, r in relatorio.items():
        linha = "  %-12s %3d itens" % (nome, r["itens"])
        if r["falhas"]:
            linha += "  ·  ficou de fora: " + "; ".join(r["falhas"][:4])
            if len(r["falhas"]) > 4:
                linha += " (+%d)" % (len(r["falhas"]) - 4)
        fala(linha)
    fala("  %d candidatos únicos do nicho em %s" % (len(filtrados), saida))
    print(saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
