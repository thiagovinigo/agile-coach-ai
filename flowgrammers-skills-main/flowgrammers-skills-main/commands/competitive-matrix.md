---
name: competitive-matrix
description: Constrói matrizes de análise competitiva com pontuação e análise de lacunas. Uso: /competitive-matrix <analyze> [opções]
---

# /competitive-matrix

Constrói matrizes competitivas com pontuação ponderada, análise de lacunas e insights de posicionamento de mercado.

## Uso

```
/competitive-matrix analyze <competitors.json>                         Análise completa
/competitive-matrix analyze <competitors.json> --weights pricing=2,ux=1.5    Pesos customizados
```

## Formato de Entrada

```json
{
  "your_product": { "name": "MeuApp", "scores": {"ux": 8, "pricing": 7, "features": 9} },
  "competitors": [
    { "name": "Concorrente A", "scores": {"ux": 7, "pricing": 9, "features": 6} }
  ],
  "dimensions": ["ux", "pricing", "features"]
}
```

## Exemplos

```
/competitive-matrix analyze competitors.json
/competitive-matrix analyze competitors.json --format json --output matrix.json
```

## Scripts
- `product-team/competitive-teardown/scripts/competitive_matrix_builder.py` — Construtor de matriz competitiva

## Referência de Skill
→ `product-team/competitive-teardown/SKILL.md`
