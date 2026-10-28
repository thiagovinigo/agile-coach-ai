# -*- coding: utf-8 -*-
"""Reddit sem chave, camada de nota: a listagem parcial do shreddit.

O endereco /svc/shreddit/community-more-posts/<ordem>/?name=<sub> responde 200
sem chave e traz, renderizado no servidor, o voto de cada post, que nem o RSS
nem a pagina de comentarios trazem. Cada post e um elemento <shreddit-post> com
os atributos score, comment-count, post-title, permalink, author,
subreddit-name e created-timestamp.

O radar usa esta camada de dois jeitos: como descoberta com nota, quando os
subreddits foram escolhidos a dedo, e como fonte de voto para os posts que o
RSS achou.
"""

import html as _html
import re
from concurrent.futures import ThreadPoolExecutor, TimeoutError as EsgotouTempo
from typing import Any, Dict, List, Optional

from . import datas, rede
from .relevancia import relevancia

ORDENS = {"rapida": ["top"], "padrao": ["top", "hot"], "funda": ["top", "hot", "new"]}
TRABALHADORES = 4
TEMPO_DA_LISTAGEM = 15

_CARTAO = re.compile(r"<shreddit-post(?=[\s>])[^>]*>")


def _log(msg: str) -> None:
    rede.log("Reddit listagem", msg)


def _atributo(tag: str, nome: str) -> Optional[str]:
    m = re.search(rf'\b{nome}="([^"]*)"', tag)
    return _html.unescape(m.group(1)) if m else None


def id_do_post(link: str) -> str:
    m = re.search(r"/comments/([A-Za-z0-9]+)", link or "")
    return m.group(1) if m else ""


def _inteiro(valor) -> int:
    try:
        return int(valor or 0)
    except ValueError:
        return 0


def ler_cartoes(html: str, consulta: str = "") -> List[Dict[str, Any]]:
    """Le os <shreddit-post> e devolve os posts com voto de verdade."""
    posts: List[Dict[str, Any]] = []
    for m in _CARTAO.finditer(html or ""):
        tag = m.group(0)
        link = _atributo(tag, "permalink") or ""
        if "/comments/" not in link:
            continue
        titulo = _atributo(tag, "post-title") or ""
        autor = _atributo(tag, "author") or "[apagado]"
        criado = _atributo(tag, "created-timestamp")
        votos = _inteiro(_atributo(tag, "score"))
        comentarios = _inteiro(_atributo(tag, "comment-count"))
        posts.append({
            "id": "",
            "fonte": "reddit",
            "titulo": titulo,
            "url": f"https://www.reddit.com{link}",
            "comunidade": _atributo(tag, "subreddit-name") or "",
            "autor": "[apagado]" if autor in ("[deleted]", "[removed]") else autor,
            "data": datas.de_iso(criado),
            "texto": "",
            "engajamento": {"votos": votos, "comentarios": comentarios},
            "relevancia": round(relevancia(consulta, titulo), 3) if consulta else 0.0,
            "motivo": "listagem do subreddit",
            "origem": "listagem",
            "post_id": id_do_post(link),
        })
    return posts


def _url(sub: str, ordem: str, periodo: str) -> str:
    sub = sub.removeprefix("r/").strip()
    url = f"https://www.reddit.com/svc/shreddit/community-more-posts/{ordem}/?name={sub}"
    if ordem == "top":
        url += f"&t={periodo}"
    return url


def _uma(sub: str, ordem: str, consulta: str, periodo: str) -> List[Dict[str, Any]]:
    try:
        texto = rede.baixar_texto_reddit(_url(sub, ordem, periodo),
                                         tempo_limite=TEMPO_DA_LISTAGEM, aceita="text/html")
        return ler_cartoes(texto, consulta) if texto else []
    except Exception as e:
        _log(f"listagem falhou em r/{sub} {ordem}: {e}")
        return []


def buscar(subreddits: List[str], profundidade: str = "padrao", consulta: str = "",
           ordens: Optional[List[str]] = None, periodo: str = "month") -> List[Dict[str, Any]]:
    """Cartoes com nota de cada subreddit em cada ordem, sem repeticao e sem ordenar."""
    if not subreddits:
        return []
    ordens = ordens or ORDENS.get(profundidade, ORDENS["padrao"])
    tarefas = [(s, o) for s in subreddits for o in ordens]
    todos: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=min(TRABALHADORES, len(tarefas)) or 1) as ex:
        futuros = [ex.submit(_uma, s, o, consulta, periodo) for s, o in tarefas]
        for f in futuros:
            try:
                todos.extend(f.result(timeout=TEMPO_DA_LISTAGEM + 5))
            except (Exception, EsgotouTempo) as e:
                _log(f"listagem nao respondeu: {e}")

    vistos, unicos = set(), []
    for p in todos:
        if p["url"] not in vistos:
            vistos.add(p["url"])
            unicos.append(p)
    return unicos
