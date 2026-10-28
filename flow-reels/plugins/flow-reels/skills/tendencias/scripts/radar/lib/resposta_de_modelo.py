# -*- coding: utf-8 -*-
"""Leitura da resposta das APIs de Responses (OpenAI e xAI).

As duas devolvem o mesmo formato: uma lista em 'output' com mensagens, e o texto
que importa num bloco 'output_text'. Pedimos JSON com uma chave 'items', e e ela
que sai daqui.
"""

import json
import re
from typing import Any, Dict, List


def texto_da_resposta(resposta: Dict[str, Any]) -> str:
    saida = resposta.get("output")
    if isinstance(saida, str):
        return saida
    if isinstance(saida, list):
        for item in saida:
            if isinstance(item, dict):
                if item.get("type") == "message":
                    for c in item.get("content", []):
                        if isinstance(c, dict) and c.get("type") == "output_text":
                            return c.get("text", "")
                elif "text" in item:
                    return item["text"]
            elif isinstance(item, str):
                return item
    for escolha in resposta.get("choices", []) or []:
        if "message" in escolha:
            return escolha["message"].get("content", "")
    return ""


def itens_da_resposta(resposta: Dict[str, Any]) -> List[Dict[str, Any]]:
    texto = texto_da_resposta(resposta or {})
    if not texto:
        return []
    m = re.search(r'\{[\s\S]*"items"[\s\S]*\}', texto)
    if not m:
        return []
    try:
        itens = json.loads(m.group()).get("items", [])
    except json.JSONDecodeError:
        return []
    return [i for i in itens if isinstance(i, dict)]


def erro_da_resposta(resposta: Dict[str, Any]) -> str:
    erro = (resposta or {}).get("error")
    if not erro:
        return ""
    return erro.get("message", str(erro)) if isinstance(erro, dict) else str(erro)


def data_valida(valor) -> bool:
    return bool(valor) and re.match(r"^\d{4}-\d{2}-\d{2}$", str(valor)) is not None
