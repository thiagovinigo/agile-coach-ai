# -*- coding: utf-8 -*-
"""Reddit sem chave, camada de descoberta: os feeds RSS (Atom) publicos.

A busca em .json do Reddit responde 403 para quase todo cliente sem chave. O
RSS ainda responde 200, entao e por ele que o radar descobre os posts, sempre
pela busca:

- global:        /search.rss?q=...
- por subreddit: /r/<sub>/search.rss?q=...&restrict_sr=on

O feed de listagem do subreddit (/r/<sub>/top.rss) fica de fora de proposito:
ele traz o sub inteiro, e nao o tema. A listagem que entra e a do shreddit, que
pelo menos traz o voto, e mesmo ela passa pelo filtro de relevancia.

O RSS nao traz voto nem contagem de comentario. Os dois comecam em zero e sao
preenchidos depois, pela listagem com nota e pelo arquivo do arctic-shift.
"""

import re
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, TimeoutError as EsgotouTempo
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

from . import datas, rede
from .relevancia import relevancia

ATOM = "{http://www.w3.org/2005/Atom}"

LIMITE_POR_PROFUNDIDADE = {"rapida": 10, "padrao": 25, "funda": 50}
TRABALHADORES = 4
TEMPO_DO_FEED = 15

_TAG_HTML = re.compile(r"<[^>]+>")
_ESPACOS = re.compile(r"\s+")


def _log(msg: str) -> None:
    rede.log("Reddit RSS", msg)


def _sub_da_url(categoria: str, url: str) -> str:
    if categoria:
        return categoria
    partes = url.split("/r/", 1)
    return partes[1].split("/", 1)[0] if len(partes) == 2 else ""


def ler_feed(xml: str, consulta: str = "") -> List[Dict[str, Any]]:
    """Le um feed Atom e devolve os posts. Nunca levanta erro."""
    if not xml:
        return []
    try:
        raiz = ET.fromstring(xml)
    except ET.ParseError as e:
        _log(f"feed ilegivel: {e}")
        return []

    posts: List[Dict[str, Any]] = []
    for entrada in raiz.iter(f"{ATOM}entry"):
        link = entrada.find(f"{ATOM}link")
        url = link.get("href", "").strip() if link is not None else ""
        if not url or "/comments/" not in url:
            continue

        el = entrada.find(f"{ATOM}title")
        titulo = (el.text or "").strip() if el is not None else ""

        autor = ""
        el = entrada.find(f"{ATOM}author/{ATOM}name")
        if el is not None and el.text:
            autor = el.text.strip().removeprefix("/u/").removeprefix("u/")
        if autor in ("[deleted]", "[removed]", ""):
            autor = "[apagado]"

        el = entrada.find(f"{ATOM}category")
        sub = _sub_da_url(el.get("term", "").strip() if el is not None else "", url)

        el = entrada.find(f"{ATOM}updated")
        atualizado = (el.text or "").strip() if el is not None else ""

        el = entrada.find(f"{ATOM}content")
        texto = ""
        if el is not None and el.text:
            texto = _ESPACOS.sub(" ", _TAG_HTML.sub(" ", el.text)).strip()[:500]

        posts.append({
            "id": "",
            "fonte": "reddit",
            "titulo": titulo,
            "url": url,
            "comunidade": sub,
            "autor": autor,
            "data": datas.de_iso(atualizado),
            "texto": texto,
            "engajamento": {"votos": 0, "comentarios": 0},
            "relevancia": round(relevancia(consulta, f"{titulo} {texto}"), 3) if consulta else 0.0,
            "motivo": "busca do Reddit",
            "origem": "busca",
        })
    return posts


def _montar_urls(consulta: str, subreddits: Optional[List[str]], periodo: str) -> List[str]:
    q = quote_plus(consulta)
    urls = [f"https://www.reddit.com/search.rss?q={q}&sort=relevance&t={periodo}"]
    for bruto in subreddits or []:
        sub = bruto.removeprefix("r/").strip()
        if not sub:
            continue
        urls.append(f"https://www.reddit.com/r/{sub}/search.rss"
                    f"?q={q}&restrict_sr=on&sort=relevance&t={periodo}")
    return urls


def _baixar_feed(url: str, consulta: str) -> List[Dict[str, Any]]:
    try:
        texto = rede.baixar_texto_reddit(url, tempo_limite=TEMPO_DO_FEED,
                                         aceita="application/atom+xml")
        return ler_feed(texto, consulta) if texto else []
    except Exception as e:  # um feed ruim nao derruba a busca inteira
        _log(f"feed falhou em {url}: {e}")
        return []


def buscar(consulta: str, profundidade: str = "padrao",
           subreddits: Optional[List[str]] = None, periodo: str = "month") -> List[Dict[str, Any]]:
    """Descobre posts pelos feeds RSS. Lista vazia em qualquer falha."""
    limite = LIMITE_POR_PROFUNDIDADE.get(profundidade, LIMITE_POR_PROFUNDIDADE["padrao"])
    urls = _montar_urls(consulta, subreddits, periodo)

    todos: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=min(TRABALHADORES, len(urls)) or 1) as ex:
        futuros = [ex.submit(_baixar_feed, url, consulta) for url in urls]
        for f in futuros:
            try:
                # O teto vale por feed, para a busca global nao ocupar a vaga
                # da busca dentro de cada subreddit pedido.
                todos.extend(f.result(timeout=TEMPO_DO_FEED + 5)[:limite])
            except (Exception, EsgotouTempo) as e:
                _log(f"feed nao respondeu: {e}")

    vistos, unicos = set(), []
    for p in todos:
        if p["url"] not in vistos:
            vistos.add(p["url"])
            unicos.append(p)
    return unicos
