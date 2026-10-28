# -*- coding: utf-8 -*-
"""Reddit sem chave, camada de comentarios: o parcial de comentarios do shreddit.

O .json da thread responde 403. O endereco /svc/shreddit/comments/r/<sub>/t3_<id>
ainda responde 200 em HTML, com cada comentario num elemento <shreddit-comment>
cujos atributos trazem score, author, created e permalink. O corpo mora num
<div id="<thingId>-post-rtjson-content">.

Daqui sai o que a comunidade disse de verdade, com quem disse e quantas pessoas
concordaram. E a parte do Reddit que vale citar no brief. Esta pagina traz a
contagem real de comentarios, mas nao o voto do post.
"""

import html as _html
import re
from typing import Any, Dict, List, Optional

from . import datas, rede

# Quantos posts recebem comentarios, por profundidade.
LIMITE_DE_POSTS = {"rapida": 3, "padrao": 5, "funda": 8}
MAX_COMENTARIOS = 10
TEMPO = 12

# Casa <shreddit-comment> e nao <shreddit-comment-tree>.
_INICIO = re.compile(r"<shreddit-comment(?=[\s>])[^>]*>")
_TOTAL = re.compile(r'total-comments="(\d+)"')
_PARAGRAFO = re.compile(r"<p[^>]*>(.*?)</p>", re.S)
_TAG = re.compile(r"<[^>]+>")
_ESPACOS = re.compile(r"\s+")
_PROXIMO_CORPO = re.compile(r'id="t1_[A-Za-z0-9]+-(?:comment|post)-rtjson-content"')


def referencia(url: str) -> Optional[tuple]:
    """(subreddit, id) de uma url de thread, ou None."""
    m = re.search(r"/r/([^/]+)/comments/([A-Za-z0-9]+)", url or "")
    return (m.group(1), m.group(2)) if m else None


def _url(sub: str, pid: str) -> str:
    # sort=top faz o Reddit mandar os mais votados na primeira pagina.
    return f"https://www.reddit.com/svc/shreddit/comments/r/{sub}/t3_{pid}?sort=top"


def _atributo(tag: str, nome: str) -> str:
    m = re.search(rf'\b{nome}="([^"]*)"', tag)
    return _html.unescape(m.group(1)) if m else ""


def _corpo(html: str, thing_id: str) -> str:
    """Texto de um comentario, ancorado no thingId, sem engolir a resposta filha."""
    if not thing_id:
        return ""
    ancora = f'id="{thing_id}-post-rtjson-content"'
    i = html.find(ancora)
    if i == -1:
        return ""
    janela = html[i + len(ancora): i + len(ancora) + 8000]
    proximo = _PROXIMO_CORPO.search(janela)
    if proximo:
        janela = janela[: proximo.start()]
    paragrafos = _PARAGRAFO.findall(janela)
    if not paragrafos:
        return ""
    texto = " ".join(_TAG.sub("", p) for p in paragrafos)
    return _ESPACOS.sub(" ", _html.unescape(texto)).strip()


def ler_comentarios(html: str, limite: int = MAX_COMENTARIOS) -> List[Dict[str, Any]]:
    comentarios: List[Dict[str, Any]] = []
    for m in _INICIO.finditer(html or ""):
        tag = m.group(0)
        autor = _atributo(tag, "author") or "[deleted]"
        if autor in ("[deleted]", "[removed]"):
            continue
        corpo = _corpo(html, _atributo(tag, "thingId"))
        if not corpo or corpo in ("[deleted]", "[removed]"):
            continue
        try:
            votos = int(_atributo(tag, "score") or 0)
        except ValueError:
            votos = 0
        link = _atributo(tag, "permalink")
        comentarios.append({
            "votos": votos,
            "autor": autor,
            "trecho": corpo[:300],
            "data": datas.de_iso(_atributo(tag, "created")),
            "url": f"https://reddit.com{link}" if link else "",
        })
    comentarios.sort(key=lambda c: c["votos"], reverse=True)
    return comentarios[:limite]


_SEM_CONTEUDO = [
    r"^(this|same|agreed|exactly|yep|nope|yes|no|thanks|thank you)\.?$",
    r"^(isso|isso ai|exato|concordo|sim|nao|não|valeu|obrigado|obrigada)\.?$",
    r"^(lol|lmao|haha|kkk|rsrs)",
    r"^\[deleted\]", r"^\[removed\]",
]


def ideias(comentarios: List[Dict[str, Any]], limite: int = 7) -> List[str]:
    """A primeira frase de cada comentario que diz alguma coisa."""
    saida: List[str] = []
    for c in comentarios[: limite * 2]:
        corpo = (c.get("trecho") or "").strip()
        if len(corpo) < 30:
            continue
        if any(re.match(p, corpo.lower()) for p in _SEM_CONTEUDO):
            continue
        frase = corpo[:150]
        if len(corpo) > 150:
            for i, ch in enumerate(frase):
                if ch in ".!?" and i > 50:
                    frase = frase[: i + 1]
                    break
            else:
                frase = frase.rstrip() + "..."
        saida.append(frase)
        if len(saida) >= limite:
            break
    return saida


def buscar(url_do_post: str) -> Dict[str, Any]:
    """Comentarios mais votados e contagem real de um post. Nunca levanta erro."""
    vazio = {"comentarios_destaque": [], "ideias_dos_comentarios": [], "total": None}
    ref = referencia(url_do_post)
    if not ref:
        return vazio
    html = rede.baixar_texto_reddit(_url(*ref), tempo_limite=TEMPO, aceita="text/html")
    if not html:
        return vazio
    comentarios = ler_comentarios(html)
    m = _TOTAL.search(html)
    return {
        "comentarios_destaque": comentarios,
        "ideias_dos_comentarios": ideias(comentarios),
        "total": int(m.group(1)) if m else None,
    }
