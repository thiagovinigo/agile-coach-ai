---
name: pulse-example
description: Golden example — produto fictício levado pela esteira ponta a ponta (prova do fluxo).
alwaysApply: false
---

# Exemplo golden — Pulse

Produto fictício (widget de feedback in-app) construído **com a própria esteira** para provar o
fluxo ponta a ponta: **discovery** (vision/features) → **spec** (critérios de aceite) → **tasks**
→ **implementação** → **testes** → **eval**.

Rode da raiz do repositório:

```bash
node template/scripts/audit-esteira.mjs examples/pulse        # conformidade estrutural
node template/scripts/eval-spec-fidelity.mjs examples/pulse   # fidelidade spec→código
node --test examples/pulse/src/                               # os testes passam
```

O **eval** mostra os 3 AC **cobertos por task e por teste (3/3)** e os testes passam de verdade —
o loop fechado, não só artefatos soltos.
