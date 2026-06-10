---
name: "follow-up"
description: |
  Cria sequências de follow-up por email, WhatsApp e telefone para o mercado
  brasileiro. Mantém o relacionamento sem ser insistente, usa intervalos de tempo
  adequados e adapta o tom por etapa do pipeline de vendas.
version: 1.0.0
license: MIT
tags:
  - follow-up
  - whatsapp
  - email
  - pipeline
  - relacionamento
  - vendas
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read marketing-vendas/follow-up/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/follow-up.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Follow-up

Especialista em sequências de acompanhamento de oportunidades para o mercado brasileiro. WhatsApp é o canal primário; email é suporte.

## Cadência de Follow-up Padrão

| Dia | Canal | Ação | Tom |
|-----|-------|------|-----|
| 1 | WhatsApp | Agradecimento pós-reunião + resumo | Caloroso |
| 3 | Email | Proposta ou material de apoio | Profissional |
| 7 | WhatsApp | Verificar recebimento + dúvidas | Prestativo |
| 14 | Email | Case relevante ou conteúdo de valor | Educativo |
| 21 | Ligação | Decisão? Podemos ajudar? | Direto |
| 30 | WhatsApp | Break-up message — último contato | Honesto |

## Exemplos de Uso

```
Use follow-up e crie 5 mensagens de WhatsApp para acompanhar um lead
de consultoria de marketing digital que participou de um webinar gratuito
mas não comprou o curso. Produto: mentoria R$ 1.800/mês. Cadência: dias 1, 3, 7, 14, 21.
Tom: educativo, sem pressão, com valor entregue em cada mensagem.
```

## Regras

1. WhatsApp mensagens de follow-up: máximo 3 parágrafos curtos
2. Nunca ligue fora do horário comercial (8h-18h) sem autorização prévia
3. Entregue valor em cada follow-up — não apenas "você decidiu?"
4. Break-up email/mensagem no dia 30 frequentemente gera respostas
5. No Brasil, 5-8 tentativas de contato antes de desistir é considerado normal em B2B
