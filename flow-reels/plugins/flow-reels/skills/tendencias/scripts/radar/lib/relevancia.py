# -*- coding: utf-8 -*-
"""Relevancia por sobreposicao de palavras, de 0 a 1.

A nota e centrada na consulta:

- a frase exata dentro do texto vale muito;
- casar so parte das palavras paga uma penalidade de verdade;
- casar so palavra generica ("dica", "review") nunca passa como relevante.

Tudo e comparado sem acento e sem cedilha, para a palavra escrita dos dois
jeitos casar do mesmo jeito.
"""

import re
from typing import List, Optional, Set

from .consulta import sem_acento

PALAVRAS_VAZIAS = frozenset({
    # ingles
    "the", "a", "an", "to", "for", "how", "is", "in", "of", "on",
    "and", "with", "from", "by", "at", "this", "that", "it", "my",
    "your", "i", "me", "we", "you", "what", "are", "do", "can",
    "its", "be", "or", "not", "no", "so", "if", "but", "about",
    "all", "just", "get", "has", "have", "was", "will",
    # portugues, ja sem acento
    "o", "os", "as", "um", "uma", "uns", "umas", "de", "da", "do", "das", "dos",
    "em", "no", "na", "nos", "nas", "para", "pra", "pro", "por", "pelo", "pela",
    "com", "sem", "que", "se", "como", "mais", "menos", "sobre", "ao", "aos",
    "e", "eh", "ser", "ou", "mas", "meu", "minha", "seu", "sua", "isso", "isto",
    "esse", "essa", "este", "esta", "ele", "ela", "eles", "elas", "eu", "voce",
    "nao", "sim", "ja", "tem", "ter", "foi", "vai", "muito", "tambem", "quando",
    "qual", "quais", "onde", "porque", "entre", "ate", "so",
})

# Sobre esta nota o Reddit decide o que e conversa fora do tema. Abaixo dela o
# post sai, desde que sobrem pelo menos MINIMO_NO_TEMA posts acima.
PISO_DE_RELEVANCIA = 0.1
MINIMO_NO_TEMA = 5

# Expansao nos dois sentidos, para siglas e grafias que se equivalem.
SINONIMOS = {
    "js": {"javascript"}, "javascript": {"js"},
    "ts": {"typescript"}, "typescript": {"ts"},
    "ai": {"ia", "artificial", "intelligence"}, "ia": {"ai", "inteligencia", "artificial"},
    "ml": {"machine", "learning"},
    "react": {"reactjs"}, "reactjs": {"react"},
    "vue": {"vuejs"}, "vuejs": {"vue"},
    "llm": {"llms"}, "llms": {"llm"},
}

# Palavra de consulta que sozinha nao sustenta relevancia.
POUCO_SINAL = frozenset({
    "advice", "best", "compare", "comparison", "explain", "guide", "guides",
    "how", "latest", "news", "opinion", "opinions", "review", "reviews",
    "thoughts", "tip", "tips", "tutorial", "tutorials", "update", "updates",
    "use", "using", "versus", "vs", "worth", "prompt", "prompts",
    "dica", "dicas", "melhor", "melhores", "guia", "novidade", "novidades",
    "noticia", "noticias", "opiniao", "comparacao", "vale", "usar", "uso",
    "tendencia", "tendencias", "alta",
})

_PALAVRA = re.compile(r"\w+")


def tokenizar(texto: str) -> Set[str]:
    """Minusculas, sem acento, sem palavra vazia, sem token de uma letra, com sinonimos."""
    palavras = _PALAVRA.findall(sem_acento((texto or "").lower()))
    tokens = {w for w in palavras if w not in PALAVRAS_VAZIAS and len(w) > 1}
    expandido = set(tokens)
    for t in tokens:
        expandido.update(SINONIMOS.get(t, ()))
    return expandido


def _frase(texto: str) -> str:
    return " ".join(re.sub(r"[^\w\s]", " ", sem_acento(texto.lower())).split())


class ConsultaPreparada:
    """A consulta tokenizada uma vez so, para nao refazer o trabalho por item."""

    __slots__ = ("bruta", "tokens", "informativos", "frase")

    def __init__(self, consulta: str) -> None:
        self.bruta = consulta
        self.tokens = tokenizar(consulta)
        informativos = {t for t in self.tokens if t not in POUCO_SINAL}
        self.informativos = informativos or self.tokens
        self.frase = _frase(consulta)


def relevancia(consulta, texto: str, hashtags: Optional[List[str]] = None) -> float:
    """Nota entre 0 e 1. Consulta vazia devolve 0.5, que e neutro."""
    prep = consulta if isinstance(consulta, ConsultaPreparada) else ConsultaPreparada(consulta)
    q = prep.tokens

    combinado = texto or ""
    if hashtags:
        combinado = f"{combinado} {' '.join(hashtags)}"
    t = tokenizar(combinado)
    if hashtags:
        # hashtag colada ("claudecode") ainda casa com "claude" e "code".
        for tag in hashtags:
            tag = sem_acento(tag.lower())
            for qt in q:
                if qt in tag and qt != tag:
                    t.add(qt)

    if not q:
        return 0.5
    comum = q & t
    if not comum:
        return 0.0

    cobertura = len(comum) / len(q)
    informativa = len(prep.informativos & t) / len(prep.informativos)
    precisao = len(comum) / (min(len(t), len(q) + 4) or 1)

    bonus = 0.0
    if prep.frase and prep.frase in _frase(combinado):
        bonus = 0.12 if len(prep.frase.split()) > 1 else 0.16

    base = 0.55 * (cobertura ** 1.35) + 0.25 * informativa + 0.20 * precisao

    # Casou so palavra generica: fica abaixo do piso de proposito.
    if prep.informativos and not (prep.informativos & t):
        return round(min(0.24, base), 2)
    return round(min(1.0, base + bonus), 2)
