---
name: "onboarding"
description: |
  Cria planos de onboarding estruturados para novos colaboradores (CLT e PJ) e
  novos clientes. Usa a metodologia 30/60/90 dias para colaboradores e define
  marcos claros de integração, aprendizado e primeiras entregas.
version: 1.0.0
license: MIT
tags:
  - onboarding
  - integracao
  - 30-60-90
  - rh
  - cliente
  - colaborador
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read operacoes-rh/onboarding/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/onboarding.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Onboarding

Especialista em planos de integração para novos colaboradores e clientes no mercado brasileiro. Um bom onboarding reduz turnover e acelera a geração de valor.

## Metodologia 30/60/90 Dias

**Primeiros 30 dias (Aprender)**
- Entender a empresa, as pessoas e os processos
- Configurar todas as ferramentas e acessos
- Fazer sombra nos processos principais
- Primeira reunião 1:1 com gestor na semana 2

**30 a 60 dias (Contribuir)**
- Primeiras entregas independentes (pequenas)
- Participar ativamente das cerimônias do time
- Identificar pontos de melhoria (sem ainda propor mudanças grandes)
- Check-in de 30 dias com feedback bidirecional

**60 a 90 dias (Impactar)**
- Entrega completa de responsabilidades do cargo
- Propor e executar ao menos uma melhoria
- Avaliação de probatório (90 dias CLT — período de experiência)
- Definir metas do próximo trimestre

## Exemplos de Uso

```
Use onboarding para criar o plano de onboarding de 30/60/90 dias para uma
Analista de Customer Success em uma empresa de SaaS B2B. Ela vai gerenciar
uma carteira de 50 clientes. Inclua: semana 1 completa dia a dia, marcos por mês,
critérios de sucesso do probatório e lista de pessoas para conhecer.
```

## Regras

1. Probatório CLT: máximo 90 dias (pode ser 45+45 ou 90 dias direto); rescisão no período não paga multa do FGTS
2. Primeiro dia é impressão permanente — plan para que seja excelente
3. Buddy/padrinho: designar um colega de apoio acelera drasticamente a integração
4. Documentar o onboarding para melhorar a cada novo colaborador
5. Check-in obrigatório ao final do probatório: conversa de feedback genuíno, não protocolar
