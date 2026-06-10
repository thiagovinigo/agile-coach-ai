---
name: rice
description: Priorização de features com pontuação RICE e planejamento de capacidade. Uso: /rice prioritize <features.csv> [opções]
---

# /rice

Prioriza features usando pontuação RICE (Reach, Impact, Confidence, Effort) com restrições opcionais de capacidade.

## Uso

```
/rice prioritize <features.csv>                              Pontua e classifica features
/rice prioritize <features.csv> --capacity 20                Classifica com limite de esforço
```

## Formato de Entrada

```csv
feature,reach,impact,confidence,effort
Modo escuro,5000,2,0.8,3
API v2,12000,3,0.9,8
Integração SSO,3000,2,0.7,5
App mobile,20000,3,0.5,13
```

## Exemplos

```
/rice prioritize features.csv
/rice prioritize features.csv --capacity 20
/rice prioritize features.csv --output json
```

## Scripts
- `product-team/product-manager-toolkit/scripts/rice_prioritizer.py` — Priorizador RICE (`<input.csv> [--capacity N] [--output text|json|csv]`)

## Referência de Skill
> `product-team/product-manager-toolkit/SKILL.md`
