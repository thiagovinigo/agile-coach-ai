# -*- coding: utf-8 -*-
"""Hacker News pela API do Algolia. Gratis, sem chave, sem cota.

E a fonte que segura a busca quando o Reddit responde 429. Ela e quase toda em
ingles, entao para tema em portugues o passe em ingles costuma ser o que rende.
"""

import html
import math
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List
from urllib.parse import urlencode

from . import datas, rede
from .consulta import achatar, extrair_assunto
from .relevancia import relevancia

URL_BUSCA = "https://hn.algolia.com/api/v1/search"
URL_ITEM = "https://hn.algolia.com/api/v1/items"

QUANTIDADE = {"rapida": 15, "padrao": 30, "funda": 60}
COMENTADAS = {"rapida": 3, "padrao": 5, "funda": 10}
PONTOS_MINIMOS = 2
FOLGA = 2   # pede o dobro e filtra a baixa audiencia aqui

# Prefixos do HN que fazem casar palavra por engano.
_PREFIXOS_HN = re.compile(r"^(Tell HN|Show HN|Ask HN|Launch HN)\s*:\s*", re.IGNORECASE)
_LIMITES_DE_PALAVRA: Dict[str, "re.Pattern[str]"] = {}


def _log(msg: str) -> None:
    rede.log("Hacker News", msg)


def _limpar_html(texto: str) -> str:
    texto = html.unescape(texto)
    texto = re.sub(r"<p>", "\n", texto)
    return re.sub(r"<[^>]+>", "", texto).strip()


def _titulo_casa(titulo: str, consulta: str) -> bool:
    """Alguma palavra da consulta aparece inteira no titulo, tirando o prefixo do HN.

    Basta uma: exigir todas mata qualquer tema de varias palavras, porque titulo
    real quase nunca traz todas. A nota de relevancia rebaixa quem casou fraco.
    Palavra inteira, e nao pedaco, para "ai" nao casar com "email".
    """
    if not consulta:
        return True
    titulo = _PREFIXOS_HN.sub("", titulo).strip().lower()
    for palavra in [w for w in achatar(consulta.lower()).split() if w]:
        padrao = _LIMITES_DE_PALAVRA.get(palavra)
        if padrao is None:
            padrao = re.compile(rf"\b{re.escape(palavra)}\b")
            _LIMITES_DE_PALAVRA[palavra] = padrao
        if padrao.search(titulo):
            return True
    return False


def _buscar(tema: str, de: str, ate: str, profundidade: str) -> List[Dict[str, Any]]:
    quantos = QUANTIDADE.get(profundidade, QUANTIDADE["padrao"])
    consulta = achatar(extrair_assunto(tema))
    inicio, fim = datas.para_epoch(de), datas.para_epoch(ate) + 86400
    _log(f"buscando '{consulta}' desde {de}")

    # O indice do HN so aceita created_at_i em numericFilters. Um filtro por
    # pontos devolve HTTP 400, entao a baixa audiencia sai aqui, depois.
    parametros = {
        "query": consulta,
        "tags": "story",
        "numericFilters": f"created_at_i>{inicio},created_at_i<{fim}",
        "hitsPerPage": str(quantos * FOLGA),
    }
    # O Algolia exige todas as palavras por padrao. Marcando as demais como
    # opcionais ele ordena por quantas casaram em vez de zerar a busca.
    palavras = consulta.split()
    if len(palavras) > 1:
        parametros["optionalWords"] = " ".join(palavras[1:])

    resposta = rede.obter(f"{URL_BUSCA}?{urlencode(parametros)}", tempo_limite=30)
    brutos = resposta.get("hits", [])
    bons = [h for h in brutos if (h.get("points") or 0) > PONTOS_MINIMOS][:quantos]
    bons = [h for h in bons if _titulo_casa(h.get("title", ""), consulta)]

    itens = []
    for i, h in enumerate(bons):
        pontos = h.get("points") or 0
        posicao = max(0.3, 1.0 - i * 0.02)
        bonus = min(0.2, math.log1p(pontos) / 40)
        rel = min(1.0, 0.6 * posicao + 0.4 * relevancia(consulta, h.get("title", "")) + bonus)
        oid = h.get("objectID", "")
        itens.append({
            "id": oid,
            "fonte": "hackernews",
            "titulo": h.get("title", ""),
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={oid}",
            "url_discussao": f"https://news.ycombinator.com/item?id={oid}",
            "autor": h.get("author", ""),
            "data": datas.de_epoch(h.get("created_at_i")),
            "engajamento": {"pontos": pontos, "comentarios": h.get("num_comments") or 0},
            "relevancia": round(rel, 2),
            "motivo": "historia no Hacker News",
        })
    _log(f"{len(itens)} historias")
    return itens


def _comentarios(oid: str, maximo: int = 5) -> Dict[str, Any]:
    try:
        dados = rede.obter(f"{URL_ITEM}/{oid}", tempo_limite=15)
    except Exception as e:
        _log(f"comentarios de {oid} falharam: {e}")
        return {"comentarios_destaque": [], "ideias_dos_comentarios": []}
    filhos = [c for c in dados.get("children", []) if c.get("text") and c.get("author")]
    filhos.sort(key=lambda c: c.get("points") or 0, reverse=True)
    destaque, ideias = [], []
    for c in filhos[:maximo]:
        texto = _limpar_html(c.get("text", ""))
        corrido = " ".join(texto.split())   # uma linha so, para nao quebrar a lista do resumo
        destaque.append({
            "autor": c.get("author", ""),
            # O HN nao publica voto por comentario, entao fica sem numero.
            "votos": c.get("points") or 0,
            "trecho": corrido[:300] + ("..." if len(corrido) > 300 else ""),
            "url": f"https://news.ycombinator.com/item?id={c.get('id')}" if c.get("id") else "",
            "data": None,
        })
        primeira = texto.split(". ")[0].split("\n")[0][:200]
        if primeira:
            ideias.append(primeira)
    return {"comentarios_destaque": destaque, "ideias_dos_comentarios": ideias}


def buscar(tema: str, de: str, ate: str, profundidade: str = "padrao") -> List[Dict[str, Any]]:
    """Historias da janela, com os comentarios das mais votadas."""
    itens = _buscar(tema, de, ate, profundidade)
    if not itens:
        return itens
    limite = COMENTADAS.get(profundidade, COMENTADAS["padrao"])
    alvo = sorted(range(len(itens)), key=lambda i: itens[i]["engajamento"]["pontos"],
                  reverse=True)[:limite]
    with ThreadPoolExecutor(max_workers=5) as ex:
        futuros = {ex.submit(_comentarios, itens[i]["id"]): i for i in alvo}
        for f in as_completed(futuros):
            i = futuros[f]
            try:
                itens[i].update(f.result(timeout=15))
            except Exception as e:
                _log(f"comentarios da historia {itens[i]['id']} falharam: {e}")
    return itens
