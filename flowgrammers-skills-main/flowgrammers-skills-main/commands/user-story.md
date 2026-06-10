---
name: user-story
description: Gera user stories com critérios de aceite e planejamento de sprint. Uso: /user-story <generate|sprint> [opções]
---

# /user-story

Gera user stories estruturadas com critérios de aceite, story points e planejamento de capacidade de sprint.

## Uso

```
/user-story generate                                         Gera user stories (interativo)
/user-story sprint <capacidade>                              Planeja sprint com capacidade em story points
```

## Formato de Entrada

O modo interativo solicita o contexto da feature. Para planejamento de sprint, informe a capacidade em story points:

```
/user-story generate
> Feature: Autenticação de usuário
> Persona: Gerente de engenharia
> Épico: Segurança da Plataforma

/user-story sprint 21
> Stories são classificadas por prioridade e cabem dentro de 21 pontos de capacidade
```

## Exemplos

```
/user-story generate
/user-story sprint 34
/user-story sprint 21
```

## Scripts
- `product-team/agile-product-owner/scripts/user_story_generator.py` — Gerador de user story (args posicionais: `sprint <capacidade>`)

## Referência de Skill
> `product-team/agile-product-owner/SKILL.md`
