# -*- coding: utf-8 -*-
"""Ordena os achados de cada fonte e tira as repeticoes.

A nota de 0 a 100 serve so para decidir a ordem em que o achado aparece no
relatorio. Ela pesa relevancia, quao recente e e engajamento comparado com os
outros achados da MESMA fonte, porque 500 votos no Reddit e 500 curtidas no X
nao sao a mesma coisa. Nao e nota de ideia de corte: ideia o radar nao pontua.
"""

import math
import re
from typing import Any, Dict, List, Optional, Set

from . import datas

PESO_RELEVANCIA = 0.45
PESO_RECENCIA = 0.25
PESO_ENGAJAMENTO = 0.30
ENGAJAMENTO_PADRAO = 35
PENALIDADE_SEM_ENGAJAMENTO = 10
PENALIDADE_DATA_FORA = 10


def _log1p(x) -> float:
    try:
        return math.log1p(x) if x and x > 0 else 0.0
    except TypeError:
        return 0.0


def engajamento_bruto(item: Dict[str, Any]) -> Optional[float]:
    e = item.get("engajamento") or {}
    fonte = item.get("fonte")
    if fonte == "reddit":
        if not e.get("votos") and not e.get("comentarios"):
            return None
        return 0.55 * _log1p(e.get("votos")) + 0.40 * _log1p(e.get("comentarios")) + 0.25
    if fonte == "x":
        if e.get("curtidas") is None and e.get("reposts") is None:
            return None
        return (0.55 * _log1p(e.get("curtidas")) + 0.25 * _log1p(e.get("reposts"))
                + 0.15 * _log1p(e.get("respostas")) + 0.05 * _log1p(e.get("citacoes")))
    if fonte == "hackernews":
        return 0.55 * _log1p(e.get("pontos")) + 0.45 * _log1p(e.get("comentarios"))
    if fonte == "youtube":
        v = e.get("visualizacoes")
        return _log1p(v) if v is not None else None
    return None


def _para_100(valores: List[Optional[float]]) -> List[Optional[float]]:
    validos = [v for v in valores if v is not None]
    if not validos:
        return [None] * len(valores)
    menor, maior = min(validos), max(validos)
    if maior == menor:
        return [None if v is None else 50.0 for v in valores]
    return [None if v is None else (v - menor) / (maior - menor) * 100 for v in valores]


def pontuar(itens: List[Dict[str, Any]], de: str, ate: str, janela_dias: int) -> List[Dict[str, Any]]:
    """Grava 'nota' em cada item e devolve a lista ordenada da maior para a menor."""
    if not itens:
        return itens
    brutos = [engajamento_bruto(i) for i in itens]
    normais = _para_100(brutos)
    for item, bruto, normal in zip(itens, brutos, normais):
        rel = int((item.get("relevancia") or 0) * 100)
        if item.get("fonte") == "youtube" and not item.get("data"):
            # O filtro de envio ja garante a janela. Sem data exata, fica no meio.
            rec = 50
        else:
            rec = datas.nota_de_recencia(item.get("data"), janela_dias)
        eng = int(normal) if normal is not None else ENGAJAMENTO_PADRAO
        nota = PESO_RELEVANCIA * rel + PESO_RECENCIA * rec + PESO_ENGAJAMENTO * eng
        if bruto is None:
            nota -= PENALIDADE_SEM_ENGAJAMENTO
        if item.get("fonte") in ("reddit", "x") and datas.confianca(item.get("data"), de, ate) == "baixa":
            nota -= PENALIDADE_DATA_FORA
        item["nota"] = max(0, min(100, int(nota)))
    return sorted(itens, key=lambda i: (-i["nota"], -(int((i.get("data") or "0").replace("-", "") or 0))))


# ------------------------------------------------------------------ repeticoes

def _trigramas(texto: str) -> Set[str]:
    texto = re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", (texto or "").lower())).strip()
    if len(texto) < 3:
        return {texto}
    return {texto[i:i + 3] for i in range(len(texto) - 2)}


def sem_repeticao(itens: List[Dict[str, Any]], limiar: float = 0.7) -> List[Dict[str, Any]]:
    """Tira a mesma url e o quase igual (Jaccard de trigramas). Fica o de nota maior."""
    vistos_url, unicos = set(), []
    for item in itens:
        chave = (item.get("url") or "").lower().rstrip("/")
        if chave and chave in vistos_url:
            continue
        vistos_url.add(chave)
        unicos.append(item)
    if len(unicos) <= 1:
        return unicos
    gramas = [_trigramas(i.get("titulo") or i.get("texto") or "") for i in unicos]
    fora = set()
    for a in range(len(unicos)):
        for b in range(a + 1, len(unicos)):
            if not gramas[a] or not gramas[b]:
                continue
            j = len(gramas[a] & gramas[b]) / len(gramas[a] | gramas[b])
            if j >= limiar:
                fora.add(b if unicos[a].get("nota", 0) >= unicos[b].get("nota", 0) else a)
    return [i for n, i in enumerate(unicos) if n not in fora]
