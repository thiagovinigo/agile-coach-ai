---
name: wiki-lint
description: Executa uma verificação de saúde no vault LLM Wiki — checagens mecânicas (páginas órfãs, links quebrados, páginas desatualizadas, frontmatter ausente, lacuna no log, duplicatas) e checagens semânticas (contradições, lacunas de referência cruzada, conceitos sem página própria). Gera um relatório markdown com ações sugeridas. Uso: /wiki-lint [--stale-days N] [--log-gap-days N]
---

# /wiki-lint

Verifica a saúde do wiki. Identifica páginas órfãs, wikilinks quebrados, afirmações desatualizadas, frontmatter ausente, contradições e desvios estruturais. **Reporta, não corrige silenciosamente** — você decide o que alterar.

Execute semanalmente, após ingestões em lote e sempre antes de compartilhar o wiki.

## Uso

```
/wiki-lint
/wiki-lint --stale-days 60
/wiki-lint --log-gap-days 7
```

## O que acontece

### Passagem 1 — Mecânica (scripts)

- `scripts/lint_wiki.py` — páginas órfãs, links quebrados, páginas desatualizadas, frontmatter ausente, títulos duplicados, lacuna no log
- `scripts/graph_analyzer.py` — hubs, sinks, componentes conectados, estatísticas do grafo

### Passagem 2 — Semântica (LLM lê e analisa)

- Contradições entre páginas atualizadas recentemente
- Afirmações desatualizadas superadas por fontes mais recentes
- Conceitos mencionados em texto simples em 3+ páginas sem página própria
- Lacunas de referência cruzada (entidades mencionadas mas não vinculadas via wikilink)
- Desvio do índice (index.md fora de sincronia com wiki/)

### Passagem 3 — Relatório

Um relatório markdown agrupado por severidade:

```markdown
# Wiki lint — <data>

**Total de páginas:** N  **Componentes:** N  **Último log:** <data>

## Encontrado
- ⚠️ <N> contradições (lista)
- <N> páginas órfãs
- <N> links quebrados
- <N> páginas desatualizadas
- ...

## Ações sugeridas
1. Investigar contradição entre [[sources/a]] e [[sources/b]]
2. Criar página de conceito para "<nome>"
3. Corrigir link quebrado em [[concepts/x]]
4. Re-ingerir [[sources/c]] — desatualizado + contraditado
5. ...
```

Em seguida, acrescenta uma entrada `lint` ao `log.md`.

## Sub-agente

Despacha o sub-agente `wiki-linter`. Veja `agents/wiki-linter.md`.

## Scripts

- `engineering/llm-wiki/scripts/lint_wiki.py`
- `engineering/llm-wiki/scripts/graph_analyzer.py`
- `engineering/llm-wiki/scripts/append_log.py`

## Frequência

| Gatilho | Passagem |
|---|---|
| Semanal | Apenas mecânica — rápida |
| Após ingestão em lote | Completa (mecânica + semântica) |
| Mensal | Completa + revisão estrutural |
| Antes de compartilhar | Completa + revisão extra |

## Referência de Skill

→ `engineering/llm-wiki/SKILL.md`
→ `engineering/llm-wiki/references/lint-workflow.md`
