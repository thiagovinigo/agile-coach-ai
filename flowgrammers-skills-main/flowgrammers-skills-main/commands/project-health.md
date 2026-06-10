---
name: project-health
description: Dashboard de saúde de portfólio e análise de matriz de riscos. Uso: /project-health <dashboard|risk> [opções]
---

# /project-health

Gera dashboards de saúde de portfólio e matrizes de risco para supervisão de projetos.

## Uso

```
/project-health dashboard <project_data.json>                Dashboard de saúde do portfólio
/project-health risk <risk_data.json>                        Análise de matriz de riscos
```

## Formato de Entrada

```json
{
  "project_name": "Reescrita da Plataforma",
  "schedule": {"planned_end": "2026-06-30", "projected_end": "2026-07-15", "milestones_hit": 4, "milestones_total": 6},
  "budget": {"allocated": 500000, "spent": 320000, "forecast": 520000},
  "scope": {"features_planned": 40, "features_delivered": 28, "change_requests": 3},
  "quality": {"defect_rate": 0.05, "test_coverage": 0.82},
  "risks": [{"description": "Engenheiro chave saindo", "probability": 0.3, "impact": 0.8}]
}
```

## Exemplos

```
/project-health dashboard portfolio-q2.json
/project-health risk registro-riscos.json
/project-health dashboard portfolio-q2.json --format json
```

## Scripts
- `project-management/senior-pm/scripts/project_health_dashboard.py` — Dashboard de saúde (`<arquivo_dados> [--format text|json]`)
- `project-management/senior-pm/scripts/risk_matrix_analyzer.py` — Analisador de matriz de riscos (`<arquivo_dados> [--format text|json]`)

## Referência de Skill
> `project-management/senior-pm/SKILL.md`
