---
name: tdd
description: Gera testes, analisa cobertura e executa fluxos de TDD. Uso: /tdd <generate|coverage|validate> [opções]
---

# /tdd

Gera testes, analisa cobertura e valida a qualidade dos testes usando a skill TDD Guide.

## Uso

```
/tdd generate <arquivo-ou-dir>  Gera testes para arquivos-fonte
/tdd coverage <dir-de-testes>   Analisa cobertura e lacunas de teste
/tdd validate <arquivo-teste>   Valida qualidade do teste (asserções, casos extremos)
```

## Exemplos

```
/tdd generate src/auth/login.ts
/tdd coverage tests/ --threshold 80
/tdd validate tests/auth.test.ts
```

## Scripts
- `engineering-team/tdd-guide/scripts/test_generator.py` — Geração de casos de teste (módulo biblioteca)
- `engineering-team/tdd-guide/scripts/coverage_analyzer.py` — Análise de cobertura (módulo biblioteca)
- `engineering-team/tdd-guide/scripts/tdd_workflow.py` — Orquestração do fluxo TDD (módulo biblioteca)
- `engineering-team/tdd-guide/scripts/fixture_generator.py` — Geração de fixtures de teste (módulo biblioteca)
- `engineering-team/tdd-guide/scripts/metrics_calculator.py` — Cálculo de métricas TDD (módulo biblioteca)

> **Nota:** Esses scripts são módulos biblioteca sem pontos de entrada CLI. Importe-os em Python ou use via orientação do SKILL.md.

## Referência de Skill
→ `engineering-team/tdd-guide/SKILL.md`
