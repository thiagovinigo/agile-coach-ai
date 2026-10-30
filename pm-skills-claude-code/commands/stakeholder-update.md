# /stakeholder-update

## O que essa skill faz

Transforma notas confusas de sprint em **status executivo limpo**: situação atual, decisões tomadas, próximos passos, riscos.

Saída: **Update de 1-2 páginas** pronto para board, exec, ou stakeholders.

---

## Quando usar

- Final de sprint/semana, precisa briefar executivos
- Descoberta importante que afeta roadmap
- Problema ou decisão que precisa escalação
- Board meeting na semana que vem

---

## Input esperado

**Mínimo:**
- **Notas confusas** da sprint/descoberta/research
- **Contexto**: O que stakeholders precisam saber?
- **Urgência**: É para informar ou para decisão?

**Opcional:**
- Métricas (churn, engagement, revenue impact)
- Dados de descoberta
- Screenshots ou mockups
- Comparação vs plano

---

## Processo

1. **Extração de narrativa** — Qual é a história aqui?
2. **Estrutura clara** — Situação → Impacto → Recomendação
3. **Números quando possível** — "Impacto de $50k/ano" vs "impacto grande"
4. **Decisão clara** — O que precisa ser decidido?
5. **Próximos passos** — Quem faz o quê até quando?

---

## Output

```markdown
# Status Update — [Data/Período]

## Executive Summary
[1 parágrafo que resume: situação, impacto, recomendação]

---

## Situation

### What happened
[Contexto do que ocorreu — descoberta, resultado, problema]

### Impact
**On business**: [$ impacto ou métrica]
**On timeline**: [Roadmap shift ou não?]
**On team**: [Resource impact]

### Data points
- [Métrica 1]: [Número]
- [Métrica 2]: [Número]
- [Discovery insight]: [Frase-chave]

---

## Analysis

### What we learned
[3-5 bullets de insight principal]

### Why it matters
[Contexto maior — como isso muda estratégia ou próximos passos?]

### What we considered
[Opções que analisamos — se decisão é necesária]

---

## Recommendation

### Option A: [Opção 1]
**Pros**: [2-3 vantagens]
**Cons**: [2-3 desvantagens]
**Cost**: [$X ou Y weeks]
**Timeline**: [Quando termina]

### Option B: [Opção 2]
**Pros**: [...]
**Cons**: [...]
**Cost**: [...]
**Timeline**: [...]

### Option C: [Opção 3]
**Pros**: [...]
**Cons**: [...]
**Cost**: [...]
**Timeline**: [...]

### Our recommendation
**Go with Option [A/B/C]** because [razão principal].

**Expected outcome**: [Métrica esperada if decidem isso]

---

## Next Steps

| What | Owner | When | Blocker? |
|------|-------|------|----------|
| [Decision needed] | [Role] | [Date] | [If yes] |
| [Action] | [Owner] | [Date] | [If yes] |
| [Communication] | [Owner] | [Date] | |

---

## Risks

| Risk | Mitigação | Monitoring |
|------|-----------|-----------|
| [Risk] | [Como evitar] | [Como detectar] |

---

## Questions?
Contact: [PM name] - [email]
```

---

## Exemplo

**Input:**
```
/stakeholder-update
Notas da descoberta de onboarding:
- 5 entrevistas com churned users
- 70% nunca criaram deal
- Todos disseram "didn't know how to start"
- Estimado ~$50k/ano em churn reduzível se fixamos isso
- Solução: Guided onboarding (2 weeks build)

Para: CEO + Board
Tipo: Informar + pedir decisão de timing
```

**Output:**
```markdown
# Status Update: Churn Root Cause Found — Action Required

## Executive Summary

**We discovered the #1 reason for our 35% churn: 70% of users who leave never create a single deal.** In customer interviews, the barrier was clear—new users don't know how to get started. We have a 2-week fix (guided onboarding tutorial) that we estimate will reduce churn by 50% ($50k/year). Recommend we prioritize this for February launch.

---

## Situation

### What happened
We ran 5 structured interviews with customers who cancelled in last 30 days. Goal: understand churn root cause.

### Key finding
**5/5 churned users never created a deal.** When asked why, 4/5 said "Didn't know how to start—felt lost in the system."

### Supporting data
- Churn cohort: 35% at day 7 (very high vs 5-10% SaaS baseline)
- % who created deal: Only 30% of new users create deal (vs 85% we'd expect)
- Days to first deal (if created): 28 minutes average (very high friction)
- Time spent: First users spend 30 mins exploring → 70% don't return

### Impact
- **Current churn cost**: ~$140k/year (35% of 400 users × $1000 ACV)
- **Recoverable via fix**: ~$50k/year (if we move 50% of this cohort to retention)
- **Opportunity**: Every point of churn reduction = $4k/year

---

## Analysis

### What we learned
1. **Onboarding is THE leever for early retention**
   - Users with first deal → 70% stay beyond day 7
   - Users without deal → 30% stay beyond day 7

2. **The barrier is not product knowledge, it's confidence**
   - Users could create deal if guided, but afraid to try
   - Fear of "messing something up"
   - Need "happy path" that doesn't require manual

3. **Other solutions (email, integrations) are table stakes, not differentiators**
   - Users want to START first (then optimize later)
   - Trying to sync Salesforce before creating deal = wrong order

4. **Competitors have solved this**
   - HubSpot, Pipedrive both have onboarding tutorials
   - Ours = empty. Users feel abandoned.

5. **Speed to first deal = speed to confidence**
   - If user creates deal in < 5 minutes = "Wow, this works"
   - If takes > 15 minutes = "Too complicated, I'll use something else"

### Why it matters
- **Churn is the #1 lever** for profitability this year
- **Early retention = compounding revenue** (every user we keep = 3 year ARR)
- **This is solvable** (not a "product is bad" issue, just need better onboarding)
- **Time-sensitive**: Every cohort that churns without trying = lost opportunity

### What we considered
1. **Do nothing** — Hope new features (email, etc) fix it later
2. **Minimal fix** — Add a help tooltip to main flow
3. **Guided experience** — Interactive tutorial first time (recommended)
4. **Comprehensive training** — Video, docs, webinar for every user (too heavy)

---

## Recommendation

### Option A: Do Nothing (baseline)
- **Pros**: No dev cost, no timeline impact
- **Cons**: Churn stays at 35%, lose $50k/year of opportunity
- **Timeline**: N/A

### Option B: Add Tooltip Help
- **Pros**: 1 week to build, minimal risk
- **Cons**: Doesn't solve root cause (users don't know they need to create deal, tooltip won't help)
- **Cost**: 1 week eng
- **Expected**: Maybe 5-10% improvement (not enough)

### Option C: Guided Onboarding Tutorial (Recommended)
- **Pros**:
  - Directly addresses "don't know how to start"
  - Quick to build (2 weeks)
  - Low tech risk (can deprecate if wrong)
  - Defensible vs competitors
- **Cons**: Takes 2 weeks of team time, could slip
- **Cost**: 2 weeks eng + design (1 week total)
- **Expected outcome**: 50% reduction in churn (35% → 20%) = +$50k/year

### Our recommendation
**Go with Option C (Guided Onboarding).** This directly removes the friction discovered in research and is achievable in our timeline. The $50k/year upside vs $20k/year cost of implementation makes this a 2.5x return. Every month we delay costs us $4k in preventable churn.

---

## Next Steps

| What | Owner | When | Blocker? |
|------|-------|------|----------|
| **CEO approval** to prioritize onboarding in Feb | Lucas (PM) | This week | YES - gates everything |
| **Design spec** for tutorial UX | Ana (Design) | Jan 10 | No |
| **Eng estimate** and timeline | João (Tech Lead) | Jan 10 | No |
| **Stakeholder communication** (sales/support) about timeline | Lucas (PM) | Jan 13 | No |
| **Launch** of guided onboarding | Team | Feb 15 | Depends on approval |

### Decision required
CEO: Approve Feb 15 launch date for guided onboarding? (Requires descoping something else or adding resource)

---

## Risks

| Risk | Likelihood | Mitigação | Monitoring |
|------|-----------|-----------|-----------|
| Tutorial could feel "spammy" | Low | Design with care, add "skip" button | Monitor support feedback |
| Mobile responsiveness issues | Medium | Test on 3G + low-end devices early | QA on 5 devices before launch |
| Doesn't move churn as expected | Low | We have strong research, but monitor | 7-day churn metric after launch |
| Timeline slips (2 weeks → 3 weeks) | Medium | Build w/ design in parallel, have buffer | Weekly progress checks |

---

## Appendix: Research Summary

### Interview quotes
> "I spent 30 minutes clicking around trying to figure out how to create a deal. No guide, no help text. I gave up." — Churned user #1

> "I was confused about what a deal was vs a contact vs an opportunity. Your terminology is different from Salesforce." — Churned user #2

> "The first thing I did when I got lost was open a ticket with support. That's bad." — Churned user #3

### Competitive benchmark
| CRM | Onboarding? | Type | Time to first deal |
|-----|-----------|------|-------------------|
| HubSpot | ✅ Video | Video + interactive | 3 min |
| Pipedrive | ✅ Tutorial | Interactive modal | 5 min |
| Salesforce | ❌ None | Docs only | 30+ min |
| **Acme** | ❌ None | Empty | 28 min (avg) |

---

**Prepared by**: Lucas (PM)
**Date**: Jan 8, 2025
**Distribution**: CEO, Board, Product Team
**Next review**: After Feb 15 launch (measure 7-day churn impact)
```

---

## Exemplo 2 (Mais curto, só informativo)

**Input:**
```
/stakeholder-update
Tipo: Weekly sprint update
Tom: Casual, quick
Foco: What shipped, metrics, what's next
```

**Output:**
```markdown
# Weekly Update — Week of Jan 8

## 🎯 What we accomplished
- ✅ Guided onboarding design complete (mockups approved)
- ✅ Email sync API spec finalized
- ✅ Started Phase 1 implementation
- ✅ Churn down to 33% (from 35% last week — seasonal dip)

## 📊 Key metrics
| Metric | This week | Last week | Trend |
|--------|-----------|-----------|-------|
| 7-day churn | 33% | 35% | ✅ Better |
| Feature adoption | 15% | 12% | ✅ Better |
| NPS | +5 | +2 | ✅ Better |
| Support tickets | 45 | 52 | ✅ Better |

## 🚀 What's next (this week)
- Frontend build of tutorial (starts Monday)
- QA planning for email integration
- Customer interview on deal health (validation)

## ⚠️ Risks
- Frontend eng sick this week — may impact velocity
- Email API auth more complex than expected (discovered Friday)
- **Mitigation**: Shifted timeline +3 days, adding overflow capacity

## 🤔 Open question
Should we launch with tutorial to 20% or 100% of users? (Impacts QA time)
**Need decision by**: Wednesday

---

**Contact**: Lucas — questions? Ping me
```

---

## Dicas

- **Executivos amam narrativa**: "We found X, recommending Y, expecting Z" é bom. Labirinto de dados é ruim.
- **Dados > opinião**: Se diz "users são frustra," melhor dizer "5/5 users entrevistados disseram 'não sabia começar'".
- **Decision framework**: Sempre 2-3 opções, seus prós/contras, sua recomendação. Executa melhor assim.
- **Próximos passos são essenciais**: Vagos = lembrete esquecido. Claros = coisa que acontece.
