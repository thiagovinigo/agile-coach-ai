---
name: wiki-init
description: Inicializa um novo vault LLM Wiki com estrutura em três camadas, arquivos de esquema e templates iniciais. Uso: /wiki-init <caminho> --topic "<tópico>" [--tool all|claude-code|codex|cursor|antigravity]
---

# /wiki-init

Inicializa um novo vault LLM Wiki. Cria `raw/`, `wiki/{entities,concepts,sources,comparisons,synthesis}`, o índice e o log, e instala os arquivos de esquema para a CLI de LLM escolhida.

## Uso

```
/wiki-init <caminho> --topic "<tópico em uma linha>"
/wiki-init <caminho> --topic "<tópico>" --tool <claude-code|codex|cursor|antigravity|opencode|gemini-cli|all>
/wiki-init <caminho> --topic "<tópico>" --force    # sobrescreve diretório não vazio
```

## Exemplos

```
/wiki-init ~/vaults/pesquisa --topic "Interpretabilidade de LLMs"
/wiki-init ./wiki-livro --topic "The Power Broker — Robert Caro" --tool all
/wiki-init ~/vaults/fundadores --topic "Playbook de fundadores SaaS" --tool codex
```

## O que cria

```
<caminho>/
├── raw/
│   └── assets/
├── wiki/
│   ├── index.md              # a partir do template
│   ├── log.md                # a partir do template
│   ├── entities/
│   ├── concepts/
│   ├── sources/
│   ├── comparisons/
│   ├── synthesis/
│   └── .templates/           # templates de página para referência
├── CLAUDE.md                 # se --tool claude-code ou all
├── AGENTS.md                 # se --tool codex|cursor|antigravity|opencode|gemini-cli|all
├── .cursorrules              # se --tool cursor ou all
└── .gitignore
```

## Próximos passos

Após inicializar:
1. Abra o vault no Obsidian
2. Coloque uma fonte em `raw/`
3. Execute `/wiki-ingest raw/<seu-arquivo>`

## Script

- `engineering/llm-wiki/scripts/init_vault.py`

## Referência de Skill

→ `engineering/llm-wiki/SKILL.md`
