---
name: pipeline
description: Detecta o stack e gera configurações de pipeline CI/CD. Uso: /pipeline <detect|generate> [opções]
---

# /pipeline

Detecta o stack do projeto e gera configurações de pipeline CI/CD para GitHub Actions ou GitLab CI.

## Uso

```
/pipeline detect [--repo <diretório>]                       Detecta stack, ferramentas e serviços
/pipeline generate --platform github|gitlab [--repo <dir>]  Gera YAML do pipeline
```

## Exemplos

```
/pipeline detect --repo ./meu-projeto
/pipeline generate --platform github --repo .
/pipeline generate --platform gitlab --repo .
```

## Scripts
- `engineering/ci-cd-pipeline-builder/scripts/stack_detector.py` — Detecta stack e ferramentas (`--repo <caminho>`, `--format text|json`)
- `engineering/ci-cd-pipeline-builder/scripts/pipeline_generator.py` — Gera YAML do pipeline (`--platform github|gitlab`, `--repo <caminho>`, `--input <stack.json>`, `--output <arquivo>`)

## Referência de Skill
→ `engineering/ci-cd-pipeline-builder/SKILL.md`
