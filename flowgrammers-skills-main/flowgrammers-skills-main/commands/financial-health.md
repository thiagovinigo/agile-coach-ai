---
name: financial-health
description: Executa análise de índices financeiros, valuation por DCF, análise de variação orçamentária e previsões. Uso: /financial-health <ratios|dcf|budget|forecast> <data.json>
---

# /financial-health

Analisa demonstrações financeiras, constrói modelos de valuation, avalia variações orçamentárias e elabora projeções.

## Uso

```
/financial-health ratios <financial_data.json> [--format json|text]
/financial-health dcf <valuation_data.json> [--format json|text]
/financial-health budget <budget_data.json> [--format json|text]
/financial-health forecast <forecast_data.json> [--format json|text]
```

## Exemplos

```
/financial-health ratios financeiros_trimestre.json --format json
/financial-health dcf valuation_empresa.json
/financial-health budget orcamento_q1.json --format json
/financial-health forecast historico_receita.json
```

## Scripts
- `finance/financial-analyst/scripts/ratio_calculator.py` — Índices de rentabilidade, liquidez, alavancagem, eficiência e valuation
- `finance/financial-analyst/scripts/dcf_valuation.py` — Valuation DCF de empresa e equity com análise de sensibilidade
- `finance/financial-analyst/scripts/budget_variance_analyzer.py` — Análise de variação realizado vs orçado vs ano anterior
- `finance/financial-analyst/scripts/forecast_builder.py` — Previsão de receita baseada em drivers com modelagem de cenários

## Referência de Skill
→ `finance/financial-analyst/SKILL.md`

## Comandos Relacionados
- `/saas-health` — Métricas específicas de SaaS (ARR, MRR, churn, CAC, LTV, Quick Ratio)
