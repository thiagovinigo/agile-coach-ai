---
name: wiki-ingest
description: Ingere um arquivo de raw/ no LLM Wiki — lê, discute, escreve página de resumo, atualiza referências cruzadas em 5 a 15 páginas, regenera o índice e adiciona ao log. Uso: /wiki-ingest <caminho-da-fonte>
---

# /wiki-ingest

Ingere uma nova fonte no LLM Wiki. Este é o comando mais utilizado.

O fluxo: lê a fonte → discute o TL;DR e as principais afirmações com você → escreve uma página de resumo da fonte → atualiza todas as páginas de entidades e conceitos relevantes → sinaliza contradições → atualiza `index.md` → adiciona entrada ao `log.md`.

Uma ingestão típica toca **5 a 15 páginas do wiki**. Você (o usuário) participa do processo: o ingestor propõe alterações e aguarda sua confirmação antes de escrever.

## Uso

```
/wiki-ingest <caminho>
/wiki-ingest raw/papers/monosemanticity.pdf
/wiki-ingest raw/articles/2026-04-01-post-interpretabilidade.md
```

## O que acontece

1. **Preparo** — executa `scripts/ingest_source.py` para obter título, prévia e caminho sugerido para o resumo
2. **Leitura** — lê a fonte diretamente
3. **Discussão** — reporta TL;DR, principais afirmações, quais páginas serão tocadas, possíveis contradições
4. **Confirmação** — aguarda seu aval (ou redirecionamento)
5. **Escrita** — cria o resumo da fonte, atualiza 5 a 15 páginas, sinaliza contradições
6. **Índice** — executa `scripts/update_index.py` ou edita `wiki/index.md` diretamente
7. **Log** — executa `scripts/append_log.py --op ingest --title "<título>"`
8. **Relatório** — lista com wikilinks de todas as páginas tocadas

## Sub-agente

Este comando despacha o sub-agente `wiki-ingestor` para o trabalho pesado. Veja `agents/wiki-ingestor.md`.

## Scripts

- `engineering/llm-wiki/scripts/ingest_source.py` — preparação da fonte (metadados + prévia)
- `engineering/llm-wiki/scripts/update_index.py` — regenera o índice
- `engineering/llm-wiki/scripts/append_log.py` — registra a ingestão no log

## Regras

- A fonte deve estar dentro da camada `raw/` do vault. Se não estiver, o comando pedirá que você a mova primeiro.
- `raw/` é imutável — o ingestor apenas lê.
- Se uma página de resumo já existir, o ingestor entra em **modo mesclagem** e acrescenta uma seção de re-ingestão.

## Referência de Skill

→ `engineering/llm-wiki/SKILL.md`
→ `engineering/llm-wiki/references/ingest-workflow.md`
