# /roadmap

## O que essa skill faz

Cria **roadmap trimestral** (ou semestral) com fases de features, sequenciamento, dependências e trade-offs.

Saída: **Roadmap visual** com timeline clara, team alocação, e critério de sucesso por fase.

---

## Quando usar

- Fim de trimestre, precisa comunicar Q próximo para todo time
- Muitas features, precisa sequenciar e mostrar dependências
- Board quer ver plano de 3-6 meses

---

## Input esperado

**Mínimo:**
- **Features priorizadas**: Lista de 5-10 features em ordem de prioridade (use /prioritize se não tem)
- **Team size**: Quantos eng, design, PM
- **Constraints**: Holidays, launches, experiments

**Opcional:**
- Timeline detalhada de features (da /user-stories)
- Dependências técnicas
- Marketing calendar
- Eventos de negócio (conference, product release)

---

## Processo

1. **Phases** — Agrupar features em 3-4 fases
2. **Timeline** — Quando cada phase sai (semanas)
3. **Team allocation** — Quem faz cada phase
4. **Dependencies** — Qual phase bloqueia qual
5. **Milestones** — Go-live dates, launch events
6. **Buffer** — Tempo para surpresas

---

## Output

```markdown
# Roadmap: [Produto] — [Trimestre/Período]

## Visão geral

**Meta desse período:** [O que vamos conseguir]
**Team:** [X eng, Y design, Z PM]
**Timeline:** [Data start - data end]

---

## Timeline Visual

```
      Jan   Feb   Mar   Apr
      ─────────────────────────
P1 🔨 ━━━━━                      (Deal war rooms)
P2 🔨      ━━━━━━━━━            (Email sync)
P3 🔨            ━━━━━━         (Deal health)
P4 🔨                ━━━ (Mkt)  (Enterprise features)
      ─────────────────────────
         Budget: [X eng weeks]
```

---

## Phase 1: [Nome] — [Semana start/end]

### O que entra
- Feature A
- Feature B (parte 1)

### Por quê essa phase?
[Razão estratégica — qual meta de negócio resolve]

### Timeline
- Week 1-2: Build core
- Week 3: QA + polish
- Week 4: Rollout + monitoring

### Go-live: [Data]

### Team
- Eng: [X eng dedicadas]
- Design: [Y horas]
- PM: [Z horas]

### Success criteria
- Feature adoption: [X%]
- Métrica move: [Y%]
- No performance regression: < 3% latency increase

### Risks
- [Risk 1]: Mitigação
- [Risk 2]: Mitigação

### Dependencies
- Precisa de [Fase anterior] ou [Ferramenta]
- Desbloqueia [Fase seguinte]

---

## Phase 2: [Nome] — [Semana start/end]

[Mesmo formato]

---

## Phase 3: [Nome] — [Semana start/end]

[Mesmo formato]

---

## Phase 4: [Nome] (Se houver)

[Mesmo formato]

---

## Sequência e Dependências

```
Phase 1 ──────────┐
                  ├──> Phase 2
                  │
Phase 1b ─────────┘

Phase 2 ──────────┐
                  ├──> Phase 3
Buffer ───────────┘

Phase 3 ──────────> Phase 4 (Enterprise)
```

### Explicação
- Phase 1 deve terminar antes Phase 2 começar (Foundation)
- Phase 1b roda em paralelo (independente)
- Phase 3 só começa se Phase 2 pronto + buffer completado
- Phase 4 é opcional se sobrar time

---

## Recursos (Team Allocation)

| Phase | Eng | Design | PM | Total weeks |
|-------|-----|--------|-----|------------|
| 1 | 2 | 1 | 0.5 | 2 weeks |
| 2 | 2 | 1 | 0.5 | 3 weeks |
| 3 | 1 | 0.5 | 0.5 | 2 weeks |
| 4 | 1 | 0.5 | 0.5 | 2 weeks (optional) |
| **Total** | **6** | **2.5** | **2** | **12 person-weeks** |

---

## Buffer e Contingência

### Semanas reservadas
- Week 1-12: Product work (phases)
- Week 13: Holiday/PTO buffer
- Week 1-4 (parallel): Urgent bugs/support

### Se algo toma mais tempo
1. Descope Phase 4 (optional anyway)
2. Extend Phase 3 timeline
3. Escalate para exec (precisa de recursos extras)

---

## Milestones e Launch Events

| Milestone | Data | O que | Impacto |
|-----------|------|-------|--------|
| Phase 1 go-live | [Data] | Deal war rooms saem | +20% NPS |
| Phase 2 go-live | [Data] | Email sync saem | +10% engagement |
| Customer webinar | [Data] | Demo Features 1+2 | Sales enablement |
| Phase 3 go-live | [Data] | Deal health score | Predictive value |
| User conference | [Data] | Keynote sobre strategy | Brand + demand |

---

## Communication Plan

### Week 1
- Share roadmap com team
- 1:1 com cada lead (align expectations)

### Bi-weekly
- All-hands: Roadmap progress
- What's working, what's not

### End of phase
- Retro: What did we learn?
- Update roadmap se necessário

### Stakeholder updates
- Board: Monthly (metrics vs plan)
- Customers: What ships each phase

---

## Roadmap Review Triggers

### Monthly
- [ ] Are we on track? (vs timeline)
- [ ] Any blockers? (tech, resource, discovery)
- [ ] Metric movement? (Is it working?)

### If happens
- [ ] New urgent feature requested
- [ ] Competitor moved
- [ ] Key customer threatening churn
- [ ] Technical blocker discovered
- [ ] Team member left

**Action**: Re-prioritize, update roadmap, communicate change

---

## Success Criteria (End of Period)

### For whole period
- [ ] All Phase 1-3 shipped on time
- [ ] No major bugs in production
- [ ] [Key metric] improved [X%]
- [ ] Team morale/velocity maintained
- [ ] Roadmap tracked 80%+ accuracy

### If Phase 4 happened
- [ ] Enterprise features working
- [ ] 2+ enterprise deals in pipeline

---

## FAQ

**P: Pode usar A antes de B?**
R: Se não há dependência. Veja diagrama. Se B depende de A, não.

**P: E se descobrir bug crítico?**
R: Descope feature em Phase 4 ou fim de Phase 3, foca em bug.

**P: Timeline está otimista?**
R: Propositalmente 80% utilização. 20% buffer para surpresas.

**P: Roadmap pode mudar?**
R: Sim, com aprovação de PM + Exec. Comunique ASAP.
```

---

## Exemplo

**Input:**
```
/roadmap
Trimestre: Q1 2025
Features (priorizadas):
1. Guided onboarding
2. Email + Salesforce
3. Deal health AI
4. Custom fields

Team: 2 backend, 1 frontend, 1 design, 1 PM
Timeline: Jan 1 - Mar 31 (12 weeks)
Constraints: 1 week holiday in Feb
```

**Output:**
```markdown
# Roadmap: CRM Consultive — Q1 2025

## Visão geral

**Meta**: Reduzir churn de 35% para <20%, validar PMF, iniciar enterprise pipeline
**Team**: 2 backend + 1 frontend, 1 design, 1 PM
**Timeline**: Jan 1 - Mar 31, 2025 (12 semanas)

---

## Timeline Visual

```
         Jan      Feb      Mar
         ─────────────────────────
Phase 1 🎯 ━━━━                  (Guided onboarding)
Phase 2 🎯      ━━━━━━━━         (Email + Salesforce)
Phase 3 🎯           ━━━━━       (Deal health AI)
Phase 4 🎯              ━━ (Opt) (Custom fields)
Parallel 🐛 ━━━━━━━━━━━━━━━━     (Bug fixes, support)
         ─────────────────────────
         Total: 12 person-weeks budget
```

---

## Phase 1: Guided Onboarding — Jan 2-15 (2 semanas)

### O que entra
- Interactive tutorial modal
- 5-step guided flow
- Validation toasts
- Analytics tracking

### Por quê?
Maior problema: 70% de churners nunca criaram deal. Se conseguem primeira vitória em < 5 minutos, ficam. Impacto direto em churn (35% → 25%).

### Timeline
- **Jan 2-9**: Build (tutorial modal + 3 steps)
- **Jan 9-13**: QA + polish
- **Jan 13-15**: Rollout (0% → 20% → 100%)

### Go-live: Jan 15

### Team
- Eng (FE): 1 full-time (2 weeks)
- Design: 3 days (mocks + UX review)
- PM: 2 days (refinement + rollout)

### Success criteria
- ✅ 70%+ of new users see tutorial
- ✅ 50%+ completion rate
- ✅ 7-day churn < 25% (vs 35% baseline)
- ✅ No performance regression

### Risks
- Mobile responsivity (50% users): Mitigação = test on 3G early
- Analytics integration: Mitigação = Fallback to server-side tracking

### Dependencies
- Nenhuma — pode rodar independente

---

## Phase 2: Email + Salesforce — Jan 16 - Feb 28 (6 semanas)

### O que entra
- Salesforce OAuth integration
- Email sync (native, not third-party)
- Email UI in deal context
- Sync reliability monitoring

### Por quê?
Second biggest problem: "I need to manually copy emails into CRM". Salesforce is blocker for 50% of mid-market. If we sync email natively, reduces friction by 50%.

### Timeline
- **Jan 16-20**: API setup + Salesforce OAuth spec
- **Jan 23-31**: Email sync engine (backend)
- **Feb 2-10**: Email UI + deal linking
- **Feb 12-20**: QA (lots of edge cases with email)
- **Feb 23-28**: Rollout + monitoring

### Go-live: Feb 28

### Team
- Eng (BE): 1.5 full-time (6 weeks)
- Eng (FE): 0.5 (UI + integration 2 weeks)
- Design: 5 days (email UI spec)
- PM: 3 days (requirements + rollout)

### Success criteria
- ✅ 40%+ adoption in first month
- ✅ Sync reliability > 99%
- ✅ Support tickets for "missing email" drops 50%
- ✅ +10% engagement (time in CRM)

### Risks
- **Salesforce API rate limits**: Mitigação = queue, batch syncs
- **Email sync explosions** (old history): Mitigação = limit to last 90 days on first sync
- **Permissions/OAuth flow**: Mitigação = test with 10 beta users pre-launch

### Dependencies
- Precisa Phase 1 terminado (understand user journey first)
- Desbloqueia Phase 3 (deal health needs email data)

---

## Phase 3: Deal Health Score — Mar 1-20 (3 semanas)

### O que entra
- ML model that predicts deal outcome
- "Stalled", "On track", "Winning" status
- Alerts if deal looks bad
- Recommendations ("You haven't talked to buyer in 2 weeks")

### Por quê?
Third problem: "I don't know if my deal is real". Salesforce pipeline is theater. If we predict deal outcome based on real signals (email activity, # of stakeholders, deal velocity), rep knows what's real.

### Timeline
- **Mar 1-5**: Data prep + model training (offline)
- **Mar 6-15**: API + UI for predictions
- **Mar 16-20**: Testing + rollout

### Go-live: Mar 20

### Team
- Eng (ML): 1 new (3 weeks) — DEPENDENCY: Need to hire by Jan
- Eng (BE): 0.5 (API)
- Design: 3 days (score visualization)
- PM: 2 days

### Success criteria
- ✅ Model accuracy > 75% (on holdout test set)
- ✅ 30%+ users checking deal health weekly
- ✅ Win rate improves 5% (reps focus on real deals)

### Risks
- **ML hiring**: Mitigação = start recruiting in Jan
- **Data quality** (need history): Mitigação = use Phase 2 email data, backfill from Salesforce
- **Model drifts**: Mitigação = retrain monthly, set monitoring

### Dependencies
- Precisa Phase 2 (email data for signals)
- Desbloqueia Phase 4 (health score used in custom alerts)

---

## Phase 4: Custom Fields (Optional) — Mar 1-20 (2 semanas, if time)

### O que entra
- Custom field builder (admin only)
- Support for text, number, dropdown, date
- Persistence on deal record

### Por quê?
Enterprise customers ask for customization. If Phase 1-3 going well, we have runway to add this for upsell.

### Timeline
- If ALL phases on schedule: Start mid-Feb for Mar 1 launch
- If ANY phase slips: Defer to Q2

### Go-live: Mar 20 (if happens)

### Team
- Eng (BE): 1 full-time (2 weeks)
- Design: 2 days

### Success criteria
- ✅ 5+ custom fields created by enterprises
- ✅ No regression in base feature performance

### Risks
- Bottomless customization requests
- Mitigação = Say NO to complex logic, only fields + values

### Dependencies
- Optional — if all prior phases done

---

## Sequência e Dependências

```
                ┌─> Phase 2 ──┐
Phase 1 (Onb) ──┤             ├──> Phase 3 (Health)
                └──────────────┤
                                └──> Phase 4 (Custom fields)
                                        (Optional)
```

### Explicação
1. Phase 1 dura 2 semanas, é foundation (user consegue fazer first deal)
2. Phase 2 começa logo após (1 semana depois), corre paralelo, dura 6 semanas
3. Phase 3 começa fim de Feb (precisa email data de Phase 2)
4. Phase 4 começa se houver time — senão defer para Q2

---

## Team Allocation (Person-weeks)

| Phase | Eng | Design | PM | Duration | Total |
|-------|-----|--------|-----|----------|-------|
| 1 | 2 | 0.3 | 0.2 | 2w | 2.5 |
| 2 | 3 | 0.3 | 0.3 | 6w | 3.6 |
| 3 | 1.5 | 0.3 | 0.2 | 3w | 2.0 |
| 4 | 1 | 0.1 | 0 | 2w | 1.1 |
| Support/bugs | 0.5 | 0 | 0 | 12w | 6 |
| **Total** | **8** | **1** | **0.7** | | **15.2** |

**Available**: 2 BE + 1 FE (4 person-weeks/trimestre) + design + PM
**Issue**: We need ML eng (1 FW for Phase 3). Hire ASAP.

---

## Milestones and Launch Events

| Milestone | Data | O que | Goal |
|-----------|------|-------|------|
| **Phase 1 Launch** | Jan 15 | Guided onboarding live | 70% adoption |
| Customer webinar | Jan 20 | Demo onboarding (free mkt) | Lead gen |
| **Phase 2 Launch** | Feb 28 | Email sync live | 40% adoption |
| **Phase 3 Launch** | Mar 20 | Deal health live | Enterprise conversations |
| Customer conference | Apr 5 | Keynote: "Consultive selling" | Brand positioning |

---

## Communication Plan

### Every Monday (Team standup)
- [ ] What shipped last week?
- [ ] What's blocking?
- [ ] On track vs roadmap?

### Every 2 weeks (All-hands)
- [ ] Roadmap progress
- [ ] Metrics update (churn, engagement, NPS)
- [ ] Customer feedback

### Monthly (Exec/Board)
- [ ] Roadmap vs plan (% on time)
- [ ] Key metrics vs targets
- [ ] Any risk?

### Customer-facing (1x per phase)
- [ ] Launch email
- [ ] Webinar or demo
- [ ] Release notes in-app

---

## Roadmap Health Check

### Weekly
- [ ] Phase 1 on time? (Jan 15 deadline)
- [ ] Blockers? (decisions, resources, tech)

### When to re-plan
- [ ] Phase slips > 1 week
- [ ] Blocker discovered
- [ ] Urgent customer issue
- [ ] Resource leaves

**Action**: Update roadmap, communicate change, reset expectations

---

## Success (End of Q1)

- [ ] Phase 1 shipped Jan 15 (churn moved)
- [ ] Phase 2 shipped Feb 28 (engagement moved)
- [ ] Phase 3 shipped Mar 20 (enterprise conversations started)
- [ ] Churn < 20% (vs 35% baseline)
- [ ] NPS +20 (from +2)
- [ ] Team velocity maintained or improved
- [ ] ML engineer hired

**If all true**: Ready for Q2 (enterprise expansion + Phase 4)
```

---

## Dicas

- **Roadmap é contrato com team**: Se promete feature em Jan 15, delivery em Jan 15.
- **Buffer é crítico**: 80% utilização, 20% para surpresas. Sem isso, timeline sempre explode.
- **Dependencies são reais**: Se Phase B depende Phase A, não paralelize sem motivo.
- **Roadmap muda**: Isso é OK. Comunicar change é essencial.
