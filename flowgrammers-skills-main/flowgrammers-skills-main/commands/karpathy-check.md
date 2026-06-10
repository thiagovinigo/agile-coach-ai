---
name: karpathy-check
description: Revisa as alterações em stage (ou o último commit) com base nos 4 princípios de codificação do Karpathy. Verifica complexidade, ruído no diff, suposições ocultas e verificação de objetivos. Uso: /karpathy-check [--last-commit]
---

# /karpathy-check

Revisa suas alterações em stage (ou o último commit) com base nos 4 princípios de codificação do Karpathy.

## Uso

```
/karpathy-check                 # revisa alterações em stage
/karpathy-check --last-commit   # revisa o commit mais recente
```

## O que executa

1. **Princípio #2 (Simplicidade):** `scripts/complexity_checker.py` em todos os arquivos alterados — detecta over-engineering, abstrações prematuras, aninhamento profundo, funções longas
2. **Princípio #3 (Cirúrgico):** `scripts/diff_surgeon.py` no diff — detecta alterações apenas em comentários, ruído de espaços em branco, desvio de estilo, refatorações oportunistas
3. **Princípios #1 + #4 (Pensar + Objetivos):** O agente `karpathy-reviewer` lê o diff e aplica verificações de julgamento humano — suposições ocultas, verificação ausente

## Saída

Um relatório estruturado com veredictos por princípio e recomendações específicas de correção por linha.

## Quando executar

- Antes de commitar (detecta ruído e complicações desnecessárias cedo)
- Após completar uma feature (verificação de sanidade antes do PR)
- Quando você suspeita que o LLM produziu código em excesso

## Sub-agente

Despacha o agente `karpathy-reviewer`. Veja `agents/karpathy-reviewer.md`.

## Scripts

- `engineering/karpathy-coder/scripts/complexity_checker.py`
- `engineering/karpathy-coder/scripts/diff_surgeon.py`
- `engineering/karpathy-coder/scripts/assumption_linter.py`
- `engineering/karpathy-coder/scripts/goal_verifier.py`

## Referência de Skill

→ `engineering/karpathy-coder/SKILL.md`
