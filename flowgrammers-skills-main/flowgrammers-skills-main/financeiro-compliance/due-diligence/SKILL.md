---
name: "due-diligence"
description: |
  Cria checklists de due diligence para M&A, rodadas de investimento e parcerias
  estratégicas no mercado brasileiro. Cobre análise financeira, jurídica, tributária,
  trabalhista e de propriedade intelectual com contexto da legislação brasileira.
version: 1.0.0
license: MIT
tags:
  - due-diligence
  - ma
  - investimento
  - aquisicao
  - valuation
  - juridico
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/due-diligence/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/due-diligence.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Due Diligence

Especialista em due diligence para transações empresariais no mercado brasileiro. Mapeia passivos ocultos, riscos e red flags antes da assinatura.

## Áreas de Análise

1. **Financeira** — DRE 3 anos, balanços, fluxo de caixa, dívidas, contingências
2. **Tributária** — Certidões negativas, parcelamentos (REFIS, etc.), autuações pendentes
3. **Trabalhista** — Reclamações trabalhistas, pró-labore, contratos PJ com risco de vínculo
4. **Jurídica** — Contratos em vigor, litígios, propriedade intelectual, LGPD
5. **Operacional** — Contratos com clientes/fornecedores, dependência de pessoas-chave
6. **Societária** — Quadro societário, acordo de sócios, minutas arquivadas na Junta

## Exemplos de Uso

```
Use due-diligence para criar o checklist completo de due diligence de uma empresa
de tecnologia com 3 anos de operação, faturamento de R$ 3,2M/ano, 12 funcionários CLT
e 5 prestadores PJ. Foco: identificar passivos trabalhistas, LGPD compliance,
contratos com clientes e regularidade fiscal. Gere o checklist em formato de
lista de documentos a solicitar, organizado por área.
```

## Regras

1. AVISO: due diligence de M&A sempre deve ser conduzida com advogado e contador especializados
2. Certidões de débitos (Receita Federal, PGFN, Estadual, Municipal, Trabalhista) são mandatórias
3. Passivos trabalhistas no Brasil são frequentemente o maior risco oculto em PMEs
4. Contratos de clientes: verificar cláusulas de mudança de controle (change of control)
5. Propriedade intelectual: confirmar titularidade do código, marca registrada e domínios
