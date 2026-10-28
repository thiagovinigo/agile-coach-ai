# -*- coding: utf-8 -*-
"""Reddit sem chave, voto de reserva: o arquivo publico do arctic-shift.

Post achado so pela busca global do RSS nao aparece em listagem nenhuma, entao
fica sem voto. O arctic-shift (https://arctic-shift.photon-reddit.com) e um
arquivo publico do Reddit cujo /api/posts/ids devolve voto e contagem de
comentario para um lote de ids. O numero e uma foto de algumas horas atras,
o que basta para ordenar e para mostrar.

Nunca levanta erro. Com limite de pedido (HTTP 422 "slow down"), erro ou host
fora do ar, devolve {} e o post aparece sem voto em vez de derrubar o Reddit.
"""

import time
from typing import Dict, List

from . import rede

API = "https://arctic-shift.photon-reddit.com/api/posts/ids"
LOTE = 50
TEMPO = 15
MAX_LOTES = 3          # teto de pedidos por busca
PAUSA = 0.4            # folga entre lotes, o servico pede calma
MAX_MEMORIA = 4096

# Memoria da propria execucao, para os dois passes (pt e en) nao pedirem o mesmo id.
_memoria: Dict[str, Dict[str, int]] = {}


def buscar_votos(ids: List[str]) -> Dict[str, Dict[str, int]]:
    """Devolve {id: {'votos', 'comentarios'}} para os ids que o arquivo conhece."""
    saida: Dict[str, Dict[str, int]] = {}
    falta: List[str] = []
    for pid in ids:
        if not pid:
            continue
        if pid in _memoria:
            saida[pid] = _memoria[pid]
        elif pid not in falta:
            falta.append(pid)

    lotes = [falta[i:i + LOTE] for i in range(0, len(falta), LOTE)][:MAX_LOTES]
    for n, lote in enumerate(lotes):
        if n:
            time.sleep(PAUSA)
        try:
            dados = rede.obter(f"{API}?ids={','.join(lote)}",
                               cabecalhos={"User-Agent": rede.AGENTE_NAVEGADOR}, tempo_limite=TEMPO)
        except Exception as e:
            rede.log("arctic-shift", f"consulta falhou ({e}); {len(lote)} posts ficam sem voto")
            break
        linhas = (dados or {}).get("data")
        if not isinstance(linhas, list):
            rede.log("arctic-shift", f"resposta inesperada, talvez limite: {str(dados)[:80]}")
            break
        for linha in linhas:
            if not isinstance(linha, dict):
                continue
            rid = str(linha.get("id") or "").removeprefix("t3_")
            if not rid:
                continue
            try:
                item = {"votos": int(linha.get("score") or 0),
                        "comentarios": int(linha.get("num_comments") or 0)}
            except (TypeError, ValueError):
                continue
            if len(_memoria) < MAX_MEMORIA:
                _memoria[rid] = item
            saida[rid] = item
    return saida
