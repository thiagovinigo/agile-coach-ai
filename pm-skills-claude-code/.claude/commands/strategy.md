# /strategy

## O que essa skill faz

Desenha estratégia de produto em **9 seções** (canvas): Visão, Segmento, Problema, Solução, Diferenciação, Monetização, Métricas, Roadmap, Riscos.

Saída: **Canvas de estratégia** em 1-2 páginas, pronto para alinhamento com stakeholders.

---

## Quando usar

- Trimestre novo, precisa de alinhamento estratégico
- Mudança de direção — precisa comunicar o "why"
- Apresentar para board ou investors — precisa de narrativa coerente

---

## Input esperado

**Mínimo:**
- **Visão**: Onde você quer que o produto seja em 3-5 anos
- **Problema**: Qual market pain está atacando
- **Segmento**: Quem são seus usuários principais

**Opcional:**
- Dados de mercado (TAM, competição)
- Roadmap de 2-3 trimestres
- Constraints (budget, team)

---

## Processo

1. **Visão** — Inspiradora mas realizável
2. **Segmento** — Específico, não "everyone"
3. **Problema-Solução** — Claro e validado
4. **Diferenciação** — Por que você vs outros?
5. **Monetização** — Como ganha dinheiro?
6. **Métricas** — Como sabe que está ganhando?
7. **Roadmap** — Próximos 3 trimestres
8. **Riscos** — O que pode dar errado?
9. **Call to action** — Próximo passo

---

## Output

```markdown
# Estratégia de Produto: [Produto/Divisão]

## 1. Visão (3-5 anos)

**1 frase que inspira:**
[Descrição clara de futuro desejado — não "ser líder", seja específico]

**Expansão:**
[2-3 parágrafos sobre que mundo estamos criando]

---

## 2. Segmento Alvo

### Primário
- **Descrição**: [Tipo de empresa, rol, tamanho]
- **Tamanho de mercado**: [# de empresas × # de users/empresa]
- **TAM**: [$X market size]
- **Porquê esse segmento**: [Razão — problema é urgent, $ disponível, etc]

### Secundário
- **Descrição**: [Outro segmento possível no futuro]
- **Quando**: [Trimestre que vamos atacar]

### Deliberadamente NÃO vamos abordar
- [Segmento A]: Razão — [competing priority / não é rentável / complexidade alta]

---

## 3. Problema

### Problema primário
**Statement:**
Quando [contexto], [persona] quer [job], mas [friction/pain]. Resulta em [consequência].

**Evidência:**
- [X% de users mencionaram em entrevista]
- [Y data metric que valida]
- [Z competitors tentam resolver]

### Problema secundário
[Similar format]

---

## 4. Solução

### Diferenciação
**Posicionamento:**
[Seu produto] é [tipo] que [diferenciação única], diferente de [competitors] porque [razão].

### Features principais (próx. 2-3 trimestres)
1. **Feature A**: Resolve [problema] de forma [diferente]
2. **Feature B**: Só nós fazemos isso
3. **Feature C**: Fazemos 10x melhor que competitors

### Investimentos críticos
- [Investimento técnico/design/brand que vai fazer diferença]

---

## 5. Monetização

### Modelo de receita
- [Subscription / Usage-based / Freemium / Enterprise]: [Razão]

### Pricing
- **Tier 1**: [Preço] para [segmento]
- **Tier 2**: [Preço] para [segmento]
- **Tier 3**: [Preço] para [segmento]

### Benchmark
- Salários/custos salvos: $[X] / ano por cliente
- Disposição a pagar: $[Y] (de entrevistas)
- Pricing de competitors: $[Z]

### Expansão de receita
- [Upgrade path — como expand existing customer]
- [Cross-sell — como vender mais na base]

---

## 6. Métricas (Success Metrics)

### Métrica de negócio (o que mais importa)
- **MRR Growth**: 10% month-over-month
- **Churn**: < 5% month-over-month
- **CAC**: < $[X]
- **LTV**: > $[Y] (LTV:CAC ratio > 3)

### Métricas de produto (indicadores)
- **Engagement**: X% monthly active
- **Feature adoption**: X% using [core feature]
- **NPS**: Target [X]

### Métrica de segmento (se variável)
- [Segmento A]: [Métrica específica]
- [Segmento B]: [Métrica específica]

---

## 7. Roadmap (Próximos 3 trimestres)

### Q[X]: [Tema]
- Goal: [O que vamos conseguir]
- Features: [3-5 features principais]
- Impacto: [Métrica que move]
- Recursos: [Team alocação]

### Q[X+1]: [Tema]
- Goal: [...]
- Features: [...]
- Impacto: [...]

### Q[X+2]: [Tema]
- Goal: [...]
- Features: [...]
- Impacto: [...]

---

## 8. Riscos e Mitigações

| Risk | Probabilidade | Impacto | Mitigação |
|------|-----------|--------|----------|
| [Competitor move] | Alta | Alto | [O que fazemos] |
| [Market shift] | Média | Médio | [O que fazemos] |
| [Tech blocker] | Baixa | Alto | [O que fazemos] |

---

## 9. Call to Action

### Próximo passo
1. [Primeira coisa a fazer — ex: validar hipótese X]
2. [Segunda coisa — ex: hire para role Y]
3. [Terceira coisa — ex: preparar roadmap detalhado]

### Timeline
- [Data]- [Data]: [O que fazemos]

### Quem decide o quê
- PM: [Decisão]
- Eng Lead: [Decisão]
- Executive: [Decisão]

---

## Aprovação

- [ ] CEO/Founder: Alinhado com visão de negócio
- [ ] PM: Viável com time e resources alocados
- [ ] Eng Lead: Tech stack permite implementação
- [ ] Finance: Financeiramente faz sentido

**Versão**: 1.0
**Última atualização**: [Data]
**Próxima review**: [3 meses, ou se contexto muda]
```

---

## Exemplo

**Input:**
```
/strategy
Visão: Melhor CRM para vendas consultivas em mid-market
Segmento: Fortune 500 + mid-market com deal cycles complexos
Problema: Deals complexos têm múltiplas conversas paralelas — ninguém tem visão unified

```

**Output:**
```markdown
# Estratégia: Consultive CRM para Mid-Market

## 1. Visão (3-5 anos)

**"Every consultative seller should win bigger deals, faster, with less chaos."**

## Expansão

Construir um CRM específico para deal consultivos — que reconhece que vendedor não é transação, é colaboração. No futuro, grandes empresas com deals complexos (6-18 meses, múltiplos stakeholders) preferem nosso CRM a Salesforce por simplicidade, speed, e collaboration.

---

## 2. Segmento Alvo

### Primário
- **Descrição**: Mid-market B2B SaaS + Professional Services (100-5000 employees)
- **Pain**: Deal cycles 6-18 meses, 4+ stakeholders por deal, Salesforce é overkill
- **TAM**: 50k empresas × 10 vendedores/empresa = 500k users
- **Market size**: $2.5B (CRM market for this segment)
- **Porquê agora**: HubSpot movendo upmarket, Salesforce ignorando mid-market complexity

### Secundário (Y2)
- **Enterprise Fortune 500**: Maior pay, complexity, political
- **Timing**: Q3-Q4 2025

### NÃO vamos abordar
- **SMB transacional** (Pipedrive wins)
- **Marketing-first** (HubSpot wins)
- **Enterprise massivo** (Salesforce wins, por enquanto)

---

## 3. Problema

### Primário
**Statement:**
Quando um VP Sales em mid-market abre Salesforce, ele vê transações lineares. Mas seu maior deal é conversas paralelas (C-level aqui, technical buyer acolá, procurement em outro lugar). Salesforce faz ele mover deal quando precisa.

**Evidência:**
- 9/10 clientes entrevistados reclamaram: "Salesforce não mostra meu deal claramente"
- 35% de deal stage não corresponde à realidade (pipeline é teatro)
- 50% das conversas internas sobre deals são EMAIL (fora do CRM)

### Secundário
**Integração com email é painful** — Outlook sync perde histórico, Salesforce activity feed é bagunçado.

---

## 4. Solução

### Diferenciação
**"Acme is the CRM built for consultative deals — where collaboration is how you win."**

Diferente de Salesforce (enterprise, bureaucratic), HubSpot (marketing-first), Pipedrive (transactional).

### Features principais

1. **Deal war rooms** (Q1 2025)
   - Real-time collaboration on complex deals
   - Everyone sees the same deal status
   - Resolve in 2 hours what Salesforce takes 2 weeks

2. **Email collaboration** (Q2 2025)
   - Native Outlook/Gmail sync (não terceirizado)
   - Conversa de email linkada a deal (não separa)
   - Who should be talking? "You're talking to wrong person"

3. **Deal health score** (Q2 2025)
   - Not pipeline stage (fake), mas real signals
   - "Stalled", "On track", "Winning" (ML-based)
   - Automatic alerts if deal looks bad

### Investimentos críticos
- **UI/UX design**: Deal visualization diferente de market (não pipeline)
- **ML/analytics**: Prever deal outcome e health
- **Mobile-first**: Deal tracking on the road

---

## 5. Monetização

### Modelo
- **Subscription SaaS**: Per-seat, monthly commitment
- **Razão**: B2B buying model, predictable revenue

### Pricing
- **Tier 1 (Individual)**: $50/user/month
  - Para sales ops ou small teams
  - Features: Basic deal tracking, collaboration

- **Tier 2 (Team)**: $75/user/month
  - Mid-market, 10-50 users
  - Features: Deal war rooms, email sync, analytics

- **Tier 3 (Enterprise)**: Custom
  - 100+ users, customization needed
  - Features: Everything + API, integrations, SLA

### Benchmark
- Deal size saved (avg): $100k
- Value per seat: $100k / (sales team size 10) = $10k/seat/year
- Disposição a pagar: 5-10% of deal value saved = $5-10k/seat/year
- Pricing: $900/user/year ($75/mo) = 9% savings ✓

### Expansão
- Upgrade: Individual → Team tier (mais features)
- Cross-sell: Integração com Slack, Salesforce (data sync)

---

## 6. Métricas

### Métrica de negócio (o que mais importa)
- **MRR Growth**: 15% MoM (agressivo, temos PMF)
- **Churn**: < 5% MoM (consultative deal cycle = long-term)
- **CAC**: < $500 (sales-focused, high spend)
- **LTV**: > $12k (3-year commitment × 30% net revenue retention)

### Métricas de produto
- **Engagement**: 85% MAU (daily active users working on deals)
- **Feature adoption**: 60% usando deal war rooms (core diferenciador)
- **NPS**: 50+ (high for B2B SaaS)

### Por segmento
- **Mid-market**: MRR growth 15%
- **Enterprise**: Lower churn, higher deal size

---

## 7. Roadmap

### Q1: Deal War Rooms (Validar PMF)
- Goal: Deliver collaborative experience que Salesforce não oferece
- Features: Real-time collaboration, deal visualization, integração com Slack
- Impacto: NPS +20, feature adoption 50%+
- Team: 2 backend, 1 frontend, 1 design

### Q2: Email Native + Deal Health
- Goal: Unify conversation + predict deal outcome
- Features: Email sync nativa, ML health score, alerts
- Impacto: +15% engagement, +10% win rate (usuario perspective)
- Team: +1 eng (ML)

### Q3: Expand to Enterprise
- Goal: Featureparity com Salesforce em customization
- Features: Custom fields, workflows, API, SSO
- Impacto: Suportrar 100+ enterprise customers
- Team: +1 eng (infrastructure)

---

## 8. Riscos

| Risk | Prob | Impact | Mitigação |
|------|------|--------|-----------|
| HubSpot moves upmarket em collab | Alta | Alto | Move fast, own deal collab space antes que eles |
| Enterprise customization bottomless | Média | Médio | Say NO a custom fields Y1, only API |
| Sales team churn (deal cycles = tough) | Médio | Médio | Focus on deal-winning, not admin |
| Salesforce discounts us | Média | Médio | Lock in with unique collab features |

---

## 9. Call to Action

### Próximas semanas
1. Refinar Q1 roadmap com Eng Lead (tech feasibility)
2. Validar pricing com 10 prospects
3. Hire 1 ML engineer (para Q2 health score)

### Timeline
- This week: Roadmap refinement
- Next week: Pricing validation
- Month 2: Hiring starts

### Decisões
- CEO: Budget para ML engineer + market expansion
- PM: Scope Q1 (deal war rooms, não email)
- Eng Lead: Tech stack para real-time collab (WebSockets? CRDT?)

---

## Aprovação

- [X] CEO: Aligned com vision
- [X] PM: Viable with current team + 1 ML hire
- [ ] Eng Lead: Tech stack review
- [ ] Finance: Hiring budget approved

Versão: 1.0
Última atualização: Jan 20, 2025
Próxima review: 3 meses (Q1 retrospective)
```

---

## Dicas

- **Visão sem direção = vague**: "Ser líder em [mercado]" é fraco. "Consultative sellers escolhem Acme porque collab é 10x melhor" é forte.
- **Segmento é filtro crítico**: Se vai abordar "everyone", vai perder para someone. Escolha seu beachhead.
- **Risks são chances de mudar estratégia**: Se risk virou realidade, não é fracasso, é learning.
- **Roadmap muda**: Review estratégia a cada trimestre — dados novos podem mudar prioridades.
