---
name: wiki-log
description: Exibe entradas recentes do log do LLM Wiki (wiki/log.md). Usa o formato padrão de cabeçalho ## [AAAA-MM-DD] para que grep + tail funcionem. Uso: /wiki-log [--last N] [--op ingest|query|lint|...]
---

# /wiki-log

Exibe entradas recentes de `wiki/log.md`. Cada operação LLM no wiki deixa uma entrada padronizada:

```
## [AAAA-MM-DD] <operação> | <título>
<detalhe opcional>
```

## Uso

```
/wiki-log                            # últimas 10 entradas
/wiki-log --last 20
/wiki-log --op ingest --last 10      # apenas entradas de ingestão
/wiki-log --op lint                  # verificações de lint recentes
/wiki-log --since 2026-04-01
```

## O que faz

Processa `wiki/log.md` e exibe as entradas correspondentes. Não há envolvimento do LLM — equivale essencialmente a:

```bash
grep "^## \[" wiki/log.md | tail -N
```

…mais filtros opcionais por tipo de operação e intervalo de datas.

## Operações válidas

- `ingest` — uma fonte foi lida e integrada
- `query` — uma pergunta foi respondida (quando registrada de volta)
- `lint` — uma verificação de saúde foi executada
- `create` — uma nova página foi criada fora de uma ingestão
- `update` — uma página foi atualizada fora de uma ingestão
- `delete` — uma página foi removida
- `note` — nota livre (contradições sinalizadas, revisões de tese, etc.)

## Exemplo de saída

```
## [2026-04-11] lint | verificação semanal de saúde
3 contradições, 12 órfãos, 2 links quebrados. Links corrigidos; contradições deixadas para a próxima sessão.

## [2026-04-10] ingest | Anthropic Monosemanticity
Adicionado sources/monosemanticity.md. Atualizados concepts/sparse-autoencoder, concepts/polysemanticity, entities/anthropic.

## [2026-04-09] query | SAE vs probing
Registrado de volta em comparisons/sae-vs-probing.md.
```

## Scripts

- Usa `grep` + `tail` diretamente em `wiki/log.md`. Nenhum script dedicado é necessário; esse é o propósito do formato padronizado de cabeçalho.

## Referência de Skill

→ `engineering/llm-wiki/SKILL.md`
