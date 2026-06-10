---
name: changelog
description: Gera changelogs a partir do histórico git e valida commits convencionais. Uso: /changelog <generate|lint> [opções]
---

# /changelog

Gera entradas de changelog no formato Keep a Changelog a partir do histórico git e valida o formato das mensagens de commit.

## Uso

```
/changelog generate [--from-tag <tag>] [--to-tag <tag>]    Gera entradas de changelog
/changelog lint [--from-ref <ref>] [--to-ref <ref>]        Valida mensagens de commit
```

## Exemplos

```
/changelog generate --from-tag v2.0.0
/changelog lint --from-ref main --to-ref dev
/changelog generate --from-tag v2.0.0 --to-tag v2.1.0 --format markdown
```

## Scripts
- `engineering/changelog-generator/scripts/generate_changelog.py` — Processa commits e renderiza changelog (`--from-tag`, `--to-tag`, `--from-ref`, `--to-ref`, `--format markdown|json`)
- `engineering/changelog-generator/scripts/commit_linter.py` — Valida formato de commit convencional (`--from-ref`, `--to-ref`, `--strict`, `--format text|json`)

## Referência de Skill
→ `engineering/changelog-generator/SKILL.md`
