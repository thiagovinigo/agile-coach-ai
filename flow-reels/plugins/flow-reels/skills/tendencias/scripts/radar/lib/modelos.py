# -*- coding: utf-8 -*-
"""Escolha do modelo para as duas fontes pagas e opcionais.

Quem quiser fixar um modelo poe RADAR_MODELO_OPENAI ou RADAR_MODELO_XAI no .env.
Sem isso, a OpenAI escolhe o gpt-5 de linha principal mais novo que a chave
enxerga, e o xAI usa o modelo rapido de busca.
"""

import re
from typing import Dict, Optional, Tuple

from . import rede

URL_MODELOS_OPENAI = "https://api.openai.com/v1/models"
RESERVA_OPENAI = "gpt-5"
PADRAO_XAI = "grok-4-1-fast"


def _versao(modelo: str) -> Tuple[int, ...]:
    m = re.search(r"(\d+(?:\.\d+)*)", modelo)
    return tuple(int(x) for x in m.group(1).split(".")) if m else (0,)


def _linha_principal(modelo: str) -> bool:
    """gpt-5, gpt-5.1, gpt-5.2... sem mini, nano, codex e parentes."""
    m = modelo.lower()
    if not re.match(r"^gpt-5(\.\d+)*$", m):
        return False
    return not any(x in m for x in ("mini", "nano", "chat", "codex", "pro", "preview", "turbo"))


def modelo_openai(chave: str, fixo: Optional[str] = None) -> str:
    if fixo:
        return fixo
    try:
        dados = rede.obter(URL_MODELOS_OPENAI, cabecalhos={"Authorization": f"Bearer {chave}"},
                           tempo_limite=15, tentativas=1)
    except Exception:
        return RESERVA_OPENAI
    candidatos = [m for m in dados.get("data", []) if _linha_principal(m.get("id", ""))]
    if not candidatos:
        return RESERVA_OPENAI
    candidatos.sort(key=lambda m: (_versao(m.get("id", "")), m.get("created", 0)), reverse=True)
    return candidatos[0]["id"]


def escolher(config: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """{'openai': ..., 'xai': ...}, com None para a fonte sem chave."""
    saida = {"openai": None, "xai": None}
    if config.get("XAI_API_KEY"):
        saida["xai"] = config.get("RADAR_MODELO_XAI") or PADRAO_XAI
    return saida


def openai_sob_demanda(config: Dict[str, Optional[str]]) -> Optional[str]:
    """So consulta a lista de modelos da OpenAI quando o reforco do Reddit vai rodar."""
    if not config.get("OPENAI_API_KEY"):
        return None
    return modelo_openai(config["OPENAI_API_KEY"], config.get("RADAR_MODELO_OPENAI"))
