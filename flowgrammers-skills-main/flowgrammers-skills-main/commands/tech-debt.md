---
name: tech-debt
description: Varre, prioriza e reporta dívida técnica. Uso: /tech-debt <scan|prioritize|report> [opções]
---

# /tech-debt

Varre codebases em busca de dívida técnica, pontua a severidade e gera planos de remediação priorizados.

## Uso

```
/tech-debt scan <diretório>              Varre indicadores de dívida técnica
/tech-debt prioritize <inventory.json>   Prioriza o backlog de dívida
/tech-debt report <diretório>            Dashboard completo com tendências
```

## Exemplos

```
/tech-debt scan ./src
/tech-debt scan . --format json
/tech-debt report . --format json --output relatorio-divida.json
```

## Scripts
- `engineering/tech-debt-tracker/scripts/debt_scanner.py` — Varre padrões de dívida (`debt_scanner.py <diretório> [--format json] [--output arquivo]`)
- `engineering/tech-debt-tracker/scripts/debt_prioritizer.py` — Prioriza backlog de dívida (`debt_prioritizer.py <inventory.json> [--framework cost_of_delay|wsjf|rice] [--format json]`)
- `engineering/tech-debt-tracker/scripts/debt_dashboard.py` — Gera dashboard de dívida (`debt_dashboard.py [arquivos...] [--input-dir dir] [--period weekly|monthly|quarterly] [--format json]`)

## Referência de Skill
→ `engineering/tech-debt-tracker/SKILL.md`
