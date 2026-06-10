---
name: wiki-query
description: Consulta o LLM Wiki — lê primeiro o index.md, aprofunda em 3 a 10 páginas relevantes, sintetiza uma resposta com citações [[wikilink]] e oferece registrar a resposta como nova página de comparação ou síntese. Uso: /wiki-query "<pergunta>"
---

# /wiki-query

Faça uma pergunta ao wiki. O bibliotecário lê primeiro `index.md`, seleciona páginas relevantes entre categorias, sintetiza uma resposta com citações e oferece registrar a resposta de volta no wiki para que suas explorações se acumulem.

## Uso

```
/wiki-query "<sua pergunta>"
/wiki-query "o que o wiki diz sobre sparse autoencoders?"
/wiki-query "compare monosemanticity e polysemanticity nas minhas fontes"
/wiki-query "quais fontes discordam sobre leis de escala?"
/wiki-query "dê-me uma tabela comparativa de SAE vs linear probing"
```

## O que acontece

1. **Leitura do índice primeiro** — lê `wiki/index.md` para encontrar páginas relevantes
2. **Aprofundamento** — lê 3 a 10 páginas completas (síntese + conceitos + fontes + entidades)
3. **Seguimento de links** — segue wikilinks entre páginas oportunisticamente
4. **Busca fallback** — se o índice não for suficiente, executa `scripts/wiki_search.py` (BM25)
5. **Síntese** — compõe uma resposta direta + detalhe de suporte + citações `[[sources/xxx]]` inline + seção "Páginas relacionadas"
6. **Oferta de registro** — pergunta se deve salvar como nova página wiki (geralmente em `comparisons/` ou `synthesis/`)

## Formatos de saída

O formato da resposta segue a pergunta:

| Formato da pergunta | Saída |
|---|---|
| "O que é X?" | Explicação em markdown com citações |
| "A vs B" | Tabela comparativa |
| "Faça um slide sobre X" | Síntese em markdown → `/wiki-marp` para renderizar |
| "Mostre a tendência de X" | Script Python + gráfico salvo em `wiki/assets/charts/` |

## Sub-agente

Este comando despacha o sub-agente `wiki-librarian`. Veja `agents/wiki-librarian.md`.

## Scripts

- `engineering/llm-wiki/scripts/wiki_search.py` — busca BM25 como fallback
- `engineering/llm-wiki/scripts/append_log.py` — registra respostas arquivadas

## Regras

- **Leia o índice primeiro.** Nada de grep em tudo.
- **Cada afirmação cita uma página** com um `[[wikilink]]`.
- **Ofereça registrar a resposta de volta** — mas apenas para respostas substantivas que valham ser mantidas.

## Referência de Skill

→ `engineering/llm-wiki/SKILL.md`
→ `engineering/llm-wiki/references/query-workflow.md`
