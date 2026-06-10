---
name: sprint-health
description: Pontuação de saúde de sprint e análise de velocidade para times ágeis. Uso: /sprint-health <analyze|velocity> [opções]
---

# /sprint-health

Pontua a saúde do sprint em entrega, qualidade e métricas de time, com análise de tendência de velocidade.

## Uso

```
/sprint-health analyze <sprint_data.json>                    Pontuação completa de saúde do sprint
/sprint-health velocity <sprint_data.json>                   Análise de tendência de velocidade
```

## Formato de Entrada

```json
{
  "sprint_name": "Sprint 24",
  "committed_points": 34,
  "completed_points": 29,
  "stories": {"total": 12, "completed": 10, "carried_over": 2},
  "blockers": [{"description": "Dependência de API", "days_blocked": 3}],
  "ceremonies": {"planning": true, "daily": true, "review": true, "retro": true}
}
```

## Exemplos

```
/sprint-health analyze sprint-24.json
/sprint-health velocity ultimos-6-sprints.json
/sprint-health analyze sprint-24.json --format json
```

## Scripts
- `project-management/scrum-master/scripts/sprint_health_scorer.py` — Pontuador de saúde de sprint (`<arquivo_dados> [--format text|json]`)
- `project-management/scrum-master/scripts/velocity_analyzer.py` — Analisador de velocidade (`<arquivo_dados> [--format text|json]`)

## Referência de Skill
> `project-management/scrum-master/SKILL.md`
