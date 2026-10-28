# -*- coding: utf-8 -*-
"""Limpeza da consulta: tira o enfeite do pedido e deixa o assunto.

"o que ta em alta sobre creatina" vira "creatina". "best Claude Code skills"
vira "claude code". Vale em portugues e em ingles, porque o radar roda um passe
em cada lingua quando o portugues volta fraco.

A regra que importa: so se tira palavra, nunca se acrescenta. O assunto e o que
a pessoa disse, nao o que o modelo acha que ela quis dizer.
"""

import re
import unicodedata
from typing import FrozenSet, Optional


def sem_acento(texto: str) -> str:
    """Tira acento e cedilha. Serve para comparar, nunca para exibir."""
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


# Prefixos de pedido, do mais longo para o mais curto. So o primeiro que casar sai.
PREFIXOS = [
    # portugues
    "o que esta em alta sobre", "o que ta em alta sobre", "o que tá em alta sobre",
    "o que as pessoas estao falando sobre", "o que as pessoas estão falando sobre",
    "o que estao falando sobre", "o que estão falando sobre",
    "me da ideias de corte sobre", "me dá ideias de corte sobre",
    "ideias de corte sobre", "pesquisa tendencia de", "pesquisa tendência de",
    "pesquisa tendencias de", "pesquisa tendências de",
    "tendencias de", "tendências de", "tendencia de", "tendência de",
    "novidades sobre", "novidades de", "noticias sobre", "notícias sobre",
    "como usar", "como fazer", "dicas de", "dicas para", "melhores", "melhor",
    "o que e", "o que é",
    # ingles
    "what are the best", "what is the best", "what are the latest",
    "what are people saying about", "what do people think about",
    "how do i use", "how to use", "how to",
    "what are", "what is", "tips for", "best practices for",
]

SUFIXOS = [
    "best practices", "use cases", "prompt techniques", "prompting tips",
    "boas praticas", "boas práticas", "casos de uso",
]

# Palavras que nao carregam assunto. Comparadas ja sem acento.
RUIDO = frozenset({
    # ingles: artigos, preposicoes, perguntas
    "a", "an", "the", "is", "are", "was", "were", "and", "or",
    "of", "in", "on", "for", "with", "about", "to",
    "how", "what", "which", "who", "why", "when", "where",
    "does", "should", "could", "would",
    # ingles: descritores de pesquisa
    "best", "top", "good", "great", "awesome", "killer",
    "latest", "new", "news", "update", "updates",
    "trendiest", "trending", "hottest", "hot", "popular", "viral",
    "practices", "features", "guide", "tutorial",
    "recommendations", "advice", "review", "reviews",
    "usecases", "examples", "comparison", "versus", "vs",
    "prompt", "prompts", "prompting", "techniques", "tips",
    "tricks", "methods", "strategies", "approaches",
    "using", "uses", "use", "people", "saying", "think", "said", "lately",
    # portugues: artigos, preposicoes, conectivos
    "o", "os", "as", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas",
    "para", "pra", "pro", "por", "pelo", "pela", "com", "sem", "sobre",
    "ao", "aos", "e", "ou", "que", "como", "qual", "quais", "quem",
    "porque", "quando", "onde",
    # portugues: descritores de pesquisa
    "melhor", "melhores", "bom", "boa", "bons", "boas", "otimo", "otima",
    "novo", "nova", "novos", "novas", "novidade", "novidades",
    "noticia", "noticias", "atualizacao", "atualizacoes",
    "tendencia", "tendencias", "alta", "viral", "virais", "popular",
    "dica", "dicas", "guia", "tutorial", "exemplos", "comparacao",
    "pesquisa", "ideias", "ideia", "corte", "cortes",
    "pessoas", "falando", "dizendo", "acham", "ultimamente",
    "usar", "usando", "uso",
})


def extrair_assunto(tema: str, ruido: Optional[FrozenSet[str]] = None,
                    max_palavras: Optional[int] = None) -> str:
    """Devolve o assunto central do tema, em minusculas.

    Se a limpeza apagar tudo, devolve o tema original: melhor buscar com enfeite
    do que buscar vazio.
    """
    texto = (tema or "").lower().strip()
    if not texto:
        return texto

    for p in PREFIXOS:
        if texto.startswith(p + " "):
            texto = texto[len(p):].strip()
            break

    for s in SUFIXOS:
        if texto.endswith(" " + s):
            texto = texto[: -len(s)].strip()
            break

    conjunto = ruido if ruido is not None else RUIDO
    palavras = texto.split()
    sobra = [w for w in palavras if sem_acento(w.strip("?!.,;:")) not in conjunto]
    if max_palavras is not None and sobra:
        sobra = sobra[:max_palavras]
    resultado = " ".join(sobra) if sobra else texto
    return resultado.strip("?!.,;: ")


def achatar(texto: str) -> str:
    """Virgula e hifen viram espaco. A busca do Hacker News tokeniza mal os dois."""
    return " ".join(texto.replace(",", " ").replace("-", " ").split())


def slug(texto: str, limite: int = 60) -> str:
    """'Agentes de IA para programar' vira 'agentes-de-ia-para-programar'."""
    base = sem_acento((texto or "").lower())
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return base[:limite].rstrip("-") or "tema"
