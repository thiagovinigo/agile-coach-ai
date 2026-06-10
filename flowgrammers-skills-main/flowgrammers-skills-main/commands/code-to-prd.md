---
name: code-to-prd
description: Faz engenharia reversa de um codebase frontend em um PRD. Uso: /code-to-prd [caminho]
---

# /code-to-prd

Faz engenharia reversa de um codebase frontend e gera um Documento de Requisitos de Produto (PRD) completo.

## Uso

```bash
/code-to-prd                    # Analisa o projeto atual
/code-to-prd ./src              # Analisa um diretório específico
/code-to-prd /caminho/projeto   # Analisa um projeto externo
```

## O que faz

1. **Varredura** — Executa `codebase_analyzer.py` para detectar framework, rotas, APIs, enums e estrutura do projeto
2. **Esqueleto** — Executa `prd_scaffolder.py` para criar o diretório `prd/` com README.md, stubs por página e arquivos de apêndice
3. **Análise** — Percorre cada página seguindo o fluxo da Fase 2: campos, interações, dependências de API, relacionamentos entre páginas
4. **Geração** — Produz o PRD final com todas as páginas, dicionário de enums, inventário de APIs e mapa de relacionamentos

## Etapas

### Etapa 1: Analisar

Determina o caminho do projeto (padrão: diretório atual). Executa o analisador:

```bash
python3 {skill_path}/scripts/codebase_analyzer.py {project_path} -o .code-to-prd-analysis.json
```

Exibe um resumo: framework, contagem de páginas, APIs, enums.

### Etapa 2: Criar Esqueleto

Gera a estrutura de diretórios do PRD:

```bash
python3 {skill_path}/scripts/prd_scaffolder.py .code-to-prd-analysis.json -o prd/
```

### Etapa 3: Preencher

Para cada página no inventário, segue o fluxo da Fase 2 do SKILL.md:
- Lê os arquivos de componentes da página
- Documenta campos, interações, dependências de API e relacionamentos
- Preenche o stub correspondente em `prd/pages/`

Para projetos grandes (>15 páginas), trabalha em lotes de 3-5 páginas e pede confirmação após cada lote.

### Etapa 4: Finalizar

Completa os arquivos de apêndice:
- `prd/appendix/enum-dictionary.md` — todos os enums e códigos de status encontrados
- `prd/appendix/api-inventory.md` — referência consolidada de APIs
- `prd/appendix/page-relationships.md` — mapa de navegação e acoplamento de dados

Remove o arquivo de análise temporário:
```bash
rm .code-to-prd-analysis.json
```

## Saída

Um diretório `prd/` contendo:
- `README.md` — visão geral do sistema, mapa de módulos, inventário de páginas
- `pages/*.md` — um arquivo por página com campos, interações e APIs
- `appendix/*.md` — dicionário de enums, inventário de APIs, relacionamentos entre páginas

## Referência de Skill

- `product-team/code-to-prd/SKILL.md`
- `product-team/code-to-prd/scripts/codebase_analyzer.py`
- `product-team/code-to-prd/scripts/prd_scaffolder.py`
- `product-team/code-to-prd/references/prd-quality-checklist.md`
