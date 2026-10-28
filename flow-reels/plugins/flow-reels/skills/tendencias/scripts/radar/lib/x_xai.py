# -*- coding: utf-8 -*-
"""X (Twitter) pela API do xAI, com a ferramenta x_search. Precisa de XAI_API_KEY.

Sem a chave o radar nao finge que cobriu o X: a fonte sai como "nao configurado"
na cobertura do brief.
"""

from typing import Any, Dict, List

from . import rede
from .resposta_de_modelo import data_valida, erro_da_resposta, itens_da_resposta

URL = "https://api.x.ai/v1/responses"
QUANTIDADE = {"rapida": (8, 12), "padrao": (20, 30), "funda": (40, 60)}

PEDIDO = """Voce tem acesso a dados do X (Twitter) em tempo real. Busque posts sobre: {tema}

Foque em posts de {de} a {ate}. Encontre de {minimo} a {maximo} posts relevantes e com conteudo.
{idioma}

IMPORTANTE: responda SO com JSON valido, exatamente neste formato, sem nenhum outro texto:
{{
  "items": [
    {{
      "text": "texto do post (cortado se for longo)",
      "url": "https://x.com/usuario/status/...",
      "author_handle": "usuario",
      "date": "AAAA-MM-DD ou null",
      "engagement": {{"likes": 100, "reposts": 25, "replies": 15, "quotes": 5}},
      "why_relevant": "por que e relevante, em uma frase",
      "relevance": 0.85
    }}
  ]
}}

Regras:
- relevance vai de 0.0 a 1.0
- date em AAAA-MM-DD ou null
- engagement pode ser null quando nao souber
- varie as contas quando der
- prefira post com conteudo a post que e so link"""


def _numero(valor):
    try:
        return int(valor) if valor else None
    except (TypeError, ValueError):
        return None


def buscar(chave: str, modelo: str, tema: str, de: str, ate: str,
           profundidade: str = "padrao", idioma: str = "pt"):
    """Devolve (itens, resposta_crua)."""
    minimo, maximo = QUANTIDADE.get(profundidade, QUANTIDADE["padrao"])
    instrucao_idioma = ("Priorize posts em portugues do Brasil e contas brasileiras; "
                        "inclua posts em ingles so se forem os mais relevantes."
                        if idioma == "pt" else "Posts em qualquer idioma.")
    corpo = {
        "model": modelo,
        # A janela vai na ferramenta, que e o filtro nativo da API. Pedir so em
        # texto deixa a criterio do modelo, e ai volta post antigo.
        "tools": [{"type": "x_search", "from_date": de, "to_date": ate}],
        "input": [{"role": "user", "content": PEDIDO.format(
            tema=tema, de=de, ate=ate, minimo=minimo, maximo=maximo, idioma=instrucao_idioma)}],
    }
    tempo = {"rapida": 90, "padrao": 120}.get(profundidade, 180)
    resposta = rede.enviar(URL, corpo, cabecalhos={"Authorization": f"Bearer {chave}"},
                           tempo_limite=tempo)

    erro = erro_da_resposta(resposta)
    if erro:
        rede.log("X", f"erro da API: {erro}")
        return [], resposta

    itens: List[Dict[str, Any]] = []
    for bruto in itens_da_resposta(resposta):
        url = bruto.get("url", "")
        if not url:
            continue
        eng = bruto.get("engagement") if isinstance(bruto.get("engagement"), dict) else {}
        try:
            rel = min(1.0, max(0.0, float(bruto.get("relevance", 0.5))))
        except (TypeError, ValueError):
            rel = 0.5
        texto = str(bruto.get("text", "")).strip()[:500]
        itens.append({
            "id": "",
            "fonte": "x",
            "titulo": texto[:120],
            "texto": texto,
            "url": url,
            "autor": str(bruto.get("author_handle", "")).strip().lstrip("@"),
            "data": bruto.get("date") if data_valida(bruto.get("date")) else None,
            "engajamento": {
                "curtidas": _numero(eng.get("likes")),
                "reposts": _numero(eng.get("reposts")),
                "respostas": _numero(eng.get("replies")),
                "citacoes": _numero(eng.get("quotes")),
            },
            "relevancia": rel,
            "motivo": str(bruto.get("why_relevant", "")).strip(),
        })
    return itens, resposta
