# -*- coding: utf-8 -*-
"""Reforco opcional do Reddit pela busca web da OpenAI.

So roda quando o Reddit sem chave voltou vazio E existe OPENAI_API_KEY no .env.
A OpenAI acha as threads, e o voto e os comentarios continuam vindo do proprio
Reddit, pelas mesmas camadas sem chave. Assim o numero mostrado no brief e
sempre o do Reddit, nunca um palpite do modelo.
"""

from typing import Any, Dict, List

from . import rede
from .consulta import extrair_assunto
from .resposta_de_modelo import data_valida, erro_da_resposta, itens_da_resposta

URL = "https://api.openai.com/v1/responses"
RESERVAS = ["gpt-4o", "gpt-4o-mini"]
QUANTIDADE = {"rapida": (15, 25), "padrao": (30, 50), "funda": (70, 100)}

PEDIDO = """Encontre threads de discussao no Reddit sobre: {tema}

PASSO 1: TIRE O ASSUNTO CENTRAL
Fique so com o substantivo, produto ou tema principal. Nao inclua "melhor",
"top", "dicas", "praticas", "novidades" na busca.

PASSO 2: BUSQUE AMPLO
1. "[assunto] site:reddit.com"
2. "reddit [assunto]"
3. "[assunto] reddit"
{idioma}

PASSO 3: INCLUA TUDO QUE FOR DO ASSUNTO
- Inclua todas as threads sobre o assunto, de {de} ate {ate} de preferencia
- Ponha a data em "AAAA-MM-DD" quando souber, senao null
- A data e conferida depois, nao filtre demais

OBRIGATORIO: a url tem "/r/" E "/comments/"
RECUSE: developers.reddit.com, business.reddit.com

Encontre de {minimo} a {maximo} threads. Mais e melhor que menos.

Responda so com JSON:
{{
  "items": [
    {{
      "title": "titulo da thread",
      "url": "https://www.reddit.com/r/sub/comments/xyz/titulo/",
      "subreddit": "nome_do_sub",
      "date": "AAAA-MM-DD ou null",
      "why_relevant": "por que e relevante",
      "relevance": 0.85
    }}
  ]
}}"""


def _modelo_sem_acesso(e: rede.ErroHTTP) -> bool:
    if e.codigo != 400 or not e.corpo:
        return False
    corpo = e.corpo.lower()
    return any(t in corpo for t in ("verified", "organization must be", "does not have access",
                                    "not available", "not found"))


def _pedir(chave: str, modelo: str, tema: str, de: str, ate: str, profundidade: str,
           idioma: str) -> Dict[str, Any]:
    minimo, maximo = QUANTIDADE.get(profundidade, QUANTIDADE["padrao"])
    instrucao_idioma = ("Prefira subreddits brasileiros e threads em portugues quando existirem."
                        if idioma == "pt" else "")
    texto = PEDIDO.format(tema=tema, de=de, ate=ate, minimo=minimo, maximo=maximo,
                          idioma=instrucao_idioma)
    tempo = {"rapida": 90, "padrao": 120}.get(profundidade, 180)
    ultimo = None
    for m in [modelo] + [r for r in RESERVAS if r != modelo]:
        corpo = {
            "model": m,
            "tools": [{"type": "web_search", "filters": {"allowed_domains": ["reddit.com"]}}],
            "include": ["web_search_call.action.sources"],
            "input": texto,
        }
        try:
            return rede.enviar(URL, corpo, cabecalhos={"Authorization": f"Bearer {chave}"},
                               tempo_limite=tempo)
        except rede.ErroHTTP as e:
            ultimo = e
            if _modelo_sem_acesso(e):
                rede.log("Reddit OpenAI", f"modelo {m} sem acesso, tentando o proximo")
                continue
            raise
    raise ultimo or rede.ErroHTTP("nenhum modelo disponivel")


def _ler(resposta: Dict[str, Any]) -> List[Dict[str, Any]]:
    erro = erro_da_resposta(resposta)
    if erro:
        rede.log("Reddit OpenAI", f"erro da API: {erro}")
        return []
    itens = []
    for bruto in itens_da_resposta(resposta):
        url = bruto.get("url", "")
        if not url or "reddit.com" not in url or "/comments/" not in url:
            continue
        try:
            rel = min(1.0, max(0.0, float(bruto.get("relevance", 0.5))))
        except (TypeError, ValueError):
            rel = 0.5
        itens.append({
            "id": "",
            "fonte": "reddit",
            "titulo": str(bruto.get("title", "")).strip(),
            "url": url,
            "comunidade": str(bruto.get("subreddit", "")).strip().removeprefix("r/"),
            "autor": "",
            "data": bruto.get("date") if data_valida(bruto.get("date")) else None,
            "texto": "",
            "engajamento": {"votos": 0, "comentarios": 0},
            "relevancia": rel,
            "motivo": "achado pela busca da OpenAI: " + str(bruto.get("why_relevant", "")).strip(),
        })
    return itens


def buscar(chave: str, modelo: str, tema: str, de: str, ate: str,
           profundidade: str = "padrao", idioma: str = "pt"):
    """Devolve (itens, resposta_crua). Tenta de novo com o assunto central se vier pouco."""
    resposta = _pedir(chave, modelo, tema, de, ate, profundidade, idioma)
    itens = _ler(resposta)
    if len(itens) < 5:
        central = extrair_assunto(tema, max_palavras=3)
        if central and central.lower() != tema.lower():
            try:
                mais = _ler(_pedir(chave, modelo, central, de, ate, profundidade, idioma))
                urls = {i["url"] for i in itens}
                itens += [i for i in mais if i["url"] not in urls]
            except Exception:
                pass
    return itens, resposta
