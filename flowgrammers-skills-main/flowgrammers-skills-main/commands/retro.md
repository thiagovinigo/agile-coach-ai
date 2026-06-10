---
name: retro
description: Analisa retrospectivas de sprint para padrões e acompanhamento de itens de ação. Uso: /retro analyze <retro_data.json>
---

# /retro

Analisa dados de retrospectiva em busca de temas recorrentes, tendências de sentimento e eficácia dos itens de ação.

## Uso

```
/retro analyze <retro_data.json>                             Análise completa de retrospectiva
```

## Formato de Entrada

```json
{
  "sprint_name": "Sprint 24",
  "went_well": ["Melhorias no pipeline de CI", "Sessões de pair programming"],
  "improvements": ["Muitas reuniões", "Testes de integração instáveis"],
  "action_items": [
    {"description": "Reduzir daily para 10 min", "owner": "SM", "status": "done"},
    {"description": "Corrigir testes instáveis", "owner": "QA Lead", "status": "in_progress"}
  ],
  "participants": 8
}
```

## Exemplos

```
/retro analyze sprint-24-retro.json
/retro analyze sprint-24-retro.json --format json
```

## Scripts
- `project-management/scrum-master/scripts/retrospective_analyzer.py` — Analisador de retrospectiva (`<arquivo_dados> [--format text|json]`)

## Referência de Skill
> `project-management/scrum-master/SKILL.md`
