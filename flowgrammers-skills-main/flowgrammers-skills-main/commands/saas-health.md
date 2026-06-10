---
name: saas-health
description: Calcula métricas de saúde SaaS (ARR, MRR, churn, CAC, LTV, NRR) e compara com benchmarks do setor. Uso: /saas-health <metrics|quick-ratio|simulate> [opções]
---

# /saas-health

Calcula métricas de saúde financeira SaaS a partir de números brutos do negócio, compara com benchmarks do setor e projeta resultados futuros.

## Uso

```
/saas-health metrics --mrr <valor> [--customers <n>] [--churned <n>] [--json]
/saas-health quick-ratio --new-mrr <valor> --churned <valor> [--expansion <valor>]
/saas-health simulate --mrr <valor> --growth <pct> --churn <pct> --cac <valor> [--json]
```

## Exemplos

```
/saas-health metrics --mrr 80000 --customers 200 --churned 3 --new-customers 15 --sm-spend 25000
/saas-health quick-ratio --new-mrr 10000 --expansion 2000 --churned 3000 --contraction 500
/saas-health simulate --mrr 50000 --growth 10 --churn 3 --cac 2000
```

## Scripts
- `finance/saas-metrics-coach/scripts/metrics_calculator.py` — Métricas SaaS principais (ARR, MRR, churn, CAC, LTV, NRR, payback)
- `finance/saas-metrics-coach/scripts/quick_ratio_calculator.py` — Índice de eficiência de crescimento
- `finance/saas-metrics-coach/scripts/unit_economics_simulator.py` — Projeção de 12 meses

## Referência de Skill
→ `finance/saas-metrics-coach/SKILL.md`

## Comandos Relacionados
- `/financial-health` — Análise financeira tradicional (índices, DCF, orçamentos)
