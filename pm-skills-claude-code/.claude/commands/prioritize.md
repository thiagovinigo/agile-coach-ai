# /prioritize

## O que essa skill faz

Aplica **RICE scoring** (Reach, Impact, Confidence, Effort) + contexto de negócio para priorizar backlog.

Saída: **Backlog priorizado** com scores, trade-offs explícitos, e recomendação de sequência.

---

## Quando usar

- Tem 5+ features/ideias e não sabe por onde começar
- Stakeholders discordam sobre prioridade
- Precisa explicar por quê escolheu A antes de B

---

## Input esperado

**Mínimo:**
- **Lista de features/ideias**: Nomes e breves descrições
- **Contexto de negócio**: Metas desse trimestre
- **Constraints**: Team size, deadline

**Opcional:**
- Dados de impacto (churn reduction, revenue, CAC)
- Dependências técnicas
- Recursos de discovery já feitos

---

## Processo

1. **RICE scoring** — Cada feature scores em 4 dimensões
2. **Ranking**: Divide by effort, ordena por score
3. **Trade-offs**: Se top 3 não cabem, qual deixa?
4. **Sequência**: Ordem de execução considerando dependências
5. **Roadmap**: Qual sprint faz qual feature?

---

## Output

```markdown
# Priorização: [Nome do Trimestre ou Iniciativa]

## Contexto

### Metas desse trimestre
- [Meta 1]
- [Meta 2]
- [Meta 3]

### Constraints
- Team: [X eng, Y design, Z PM]
- Timeline: [Semanas disponíveis]
- Dependências: [O que bloqueia]

---

## RICE Scoring

### Explicação de cada dimensão

**Reach** (alcance de usuários)
- 100+ = 3 pontos
- 10-100 = 2 pontos
- 1-10 = 1 ponto

**Impact** (tamanho do efeito em cada usuário)
- Massivo (+50% métrica) = 3 pontos
- Grande (+10-50%) = 2 pontos
- Pequeno (+1-10%) = 1 ponto

**Confidence** (quão certo você está dos números)
- Muito certo (dados/descoberta) = 100%
- Confiante (validação informal) = 80%
- Suposição (hipótese não testada) = 50%

**Effort** (semanas de trabalho)
- RICE = (Reach × Impact × Confidence) / Effort
- Maior score = maior prioridade

---

## Features Priorizadas

| # | Feature | Reach | Impact | Conf | Effort | Score | Razão |
|---|---------|-------|--------|------|--------|-------|-------|
| 1 | [Feature A] | 3 | 3 | 100% | 2 | **4.5** | Alinha com meta 1, dados sólidos |
| 2 | [Feature B] | 2 | 2 | 80% | 3 | **1.07** | Nice-to-have, menos urgente |
| 3 | [Feature C] | 3 | 1 | 50% | 5 | **0.3** | Risky, sem validação ainda |

---

## Top 3 Recomendados

### 1. [Feature A] — Score 4.5 ⭐ Recomendado

**Caso de negócio**
- Reach: 200+ usuários (30% da base)
- Impact: +25% engagement (de 60% para 75%)
- Esforço: 2 semanas
- Alinha com: Meta 1 (Aumentar engagement)

**Detalhe**
- Já temos descoberta completa
- Risk baixo (feature similar existe no competitor)
- Quick win 1º

**Se fizer agora**
- Go-live: Semana 2
- Impacto esperado: +X MRR em 30 dias

---

### 2. [Feature B] — Score 1.07 ⭐ Considerar se tempo sobra

**Caso de negócio**
- Reach: 50 usuários (7% da base)
- Impact: +15% NPS (de 35 para 50)
- Esforço: 3 semanas
- Alinha com: Meta 2 (Customer satisfaction)

**Detalhe**
- Valor alto para essas 50 users mas impacto baixo no todo
- Confiança: 80% (validação com 5 clientes)
- Medium risk (requer integração externa)

**Se fizer depois**
- Seria prioridade para Q2
- Mantém cliente quality alta

---

### 3. [Feature C] — Score 0.3 ❌ Defer para Q2

**Caso de negócio**
- Reach: 150+ usuários
- Impact: +5% conversão (de 10% para 15%)
- Esforço: 5 semanas
- Alinha com: Meta 3 (Growth)

**Detalhe**
- HUGE incerteza (hipótese não testada)
- Effort alto = risco
- Recomendação: Validar com experimento ANTES de PRD

**Se não fizer agora**
- Não afeta trimestre
- Ganho tempo para validar melhor no Q2

---

## Trade-offs Explícitos

### Cenário A: Time pode fazer 2 features em paralelo
```
Semana 1-2: Feature A (1ª eng + design)
Semana 1-3: Feature B (2ª eng)
Semana 4: Buffer/polish
```

✅ Vantagem: Máximo impacto, ambas saem no mês
❌ Desvantagem: Team estressado, possível delay

### Cenário B: Time faz 1 feature por vez
```
Semana 1-2: Feature A → go-live
Semana 3-5: Feature B → go-live
Semana 6: Buffer
```

✅ Vantagem: Menos stress, mais qualidade, time pode responder bugs
❌ Desvantagem: Feature B sai mais tarde, possível pierde market window

### Recomendação
**Scenario B** — Feature A é quick win, deixa time com morale boost. Feature B é lower priority assim.

---

## Roadmap recomendado

### Semana 1-2: Feature A (MVP)
- Lançamento: Final da semana 2
- Métrica target: 20% de users ativos
- Go/No-go: Se < 10% de users adoptam, voltar ao drawing board

### Semana 3-5: Feature B (se aprovado)
- Dependência: A saiu + feedback coletado
- Lançamento: Final da semana 5
- Métrica target: 50% de segment satisfaction

### Semana 6: Polish/buffer
- Bugs de A ou B
- Surpresas

---

## O que fazer com Feature C

**Não é "cancela", é "defer + validate"**

1. Semana 1: Desenhar experimento para testar hipótese de C
2. Week 2-3: Rodar experimento com 100 usuários
3. Week 4: Análise — se validado, goes para Q2 roadmap como P0

Dessa forma, Q2 começa com Feature C já validado, sem risco.

---

## Aprovação

- [ ] PM: Priorização alinhada com metas
- [ ] Eng Lead: Estimates realistas
- [ ] Executive: Trade-offs aceitáveis

**Decisão**: [Feature A] vai para próximo sprint
**Data**: ________
**Próxima review**: [2 semanas, ou quando nova ideia aparecer]
```

---

## Exemplo

**Input:**
```
/prioritize
Features:
1. Guided onboarding (story 2 context)
2. Email integration com Salesforce
3. AI deal prediction
4. Custom fields v2
5. Dashboard personalizável

Time: 2 eng, 1 design, 1 PM
Timeline: 6 semanas
Meta: Aumentar churn de 35% para < 20%
```

**Output:**
```markdown
# Priorização: Q1 2025 — Reduzir Churn

## Contexto

### Metas
1. Reduzir churn de 35% para < 20% (em 90 dias)
2. Manter NPS acima de +20
3. Não impactar performance (<2s load time)

### Constraints
- Team: 2 backend eng, 1 frontend, 1 design, 1 PM
- Timeline: 6 semanas até fim de trimestre
- Tech debt: Email integration é dependency para 2 outras features

---

## RICE Scoring

| Feature | Reach | Impact | Confidence | Effort | Score | Rank |
|---------|-------|--------|-----------|--------|-------|------|
| Guided onboarding | 3 (1k new/month) | 3 (70% dos que onboard → stay) | 100% | 2 sem | **4.5** | 🥇 |
| Email + Salesforce | 2 (50% base) | 2 (+10% productivity) | 80% | 2 sem | **1.6** | 🥈 |
| Custom fields v2 | 2 (mid-market) | 1 (+5% satisfaction) | 50% | 4 sem | **0.25** | 🥉 |
| AI prediction | 1 (10 early adopters) | 3 (transformational) | 30% | 6 sem | **0.075** | ❌ |
| Dashboard person. | 3 (95% users) | 1 (nice-to-have) | 60% | 3 sem | **0.6** | ❌ |

---

## Top 3 Recomendados

### 🥇 1. Guided Onboarding — Score 4.5

**Caso de negócio**
- Reach: 1000+ new users/month
- Impact: 70% que fazem guia FICA (vs 30% hoje sem guia)
- Esforço: 2 semanas
- Metas: Alinha diretamente com meta 1 (reduzir churn)

**Validação**
- ✅ 5 entrevistas com churned users (todos disseram "não sabia começar")
- ✅ 3 competitors tem onboarding guiado
- ✅ Low tech risk (é UX pura, pode deprecate depois se quiser)

**Timeline**
- Semana 1-2: Build + QA
- Semana 3: Rollout (0% → 20% → 50% → 100%)
- Métrica: % of new users que completa onboarding + 7-day retention

**Impacto esperado**
- 30% redução em 7-day churn = 105 usuários retidos/mês = +$15k MRR

---

### 🥈 2. Email + Salesforce Integration — Score 1.6

**Caso de negócio**
- Reach: 500+ usuários (50% base de mid-market)
- Impact: Salesman consegue ver histórico de email sem sair do CRM (+10% time/user)
- Esforço: 2 semanas
- Metas: Alinha com saúde geral

**Validação**
- ✅ "Integration é simples" disse 4/10 clientes
- ✅ HubSpot + Pipedrive tem isso
- ⚠️ Salesforce API é complexa (medium risk)

**Timeline**
- Semana 1: API auth + setup
- Semana 2: Email sync + UI
- Semana 3: Bugs
- Métrica: Feature adoption rate, sync reliability

**Impacto**
- Se bem feito: +$20k MRR
- Se bugado: -$10k MRR (churn de frustrado)

**Dependência para**: Custom fields, AI prediction (ambas precisam email data)

---

### 🥉 3. Custom Fields v2 — Score 0.25 ❌ DEFER

**Por que não agora**
- Mid-market (50 users) é small reach
- +5% satisfaction é small impact
- HUGE uncertainty (qual custom field importa?)
- 4 semanas = perde 2/6 timeline

**Recomendação**
1. Se Salesforce integration sair bem (semana 2), considerar
2. Ou defer para Q2 e fazer bem

---

## Trade-off Decision

### Opção A: Guided onboarding + Email integration
- Semana 1-2: Guided onboarding
- Semana 1-2: Email API setup (paralelo, 2º eng)
- Semana 2-3: Email UI
- Semana 4-6: Polish + Surprise bugs

✅ Máximo impacto em churn
✅ Email desbloqueia future features
❌ Team estressado semana 1-2

### Opção B: Guided onboarding ONLY, depois Email
- Semana 1-2: Guided onboarding
- Semana 3-4: Email integration (1º eng)
- Semana 5-6: Polish/buffer

✅ Menos risco
✅ Time respira
❌ Email atrasa 1 semana

**RECOMENDAÇÃO: Opção A** — Guided onboarding é must-have (score 4.5), Email é parallelizável. Apert agora enquanto team tem energy.

---

## Roadmap

### Semana 1-2
- **Guided onboarding**: Build interactive tutorial modal + steps
- **Email + Salesforce**: Start API auth, read docs
- Team: (Frontend) onboarding, (Backend) email, (Design) onboarding UX

### Semana 2-3
- **Guided onboarding**: QA + rollout start (0% → 20%)
- **Email + Salesforce**: Finish API + email sync logic
- **Custom fields**: START planning (if time) — don't build yet, just design

### Semana 3-4
- **Email UI**: Build UI for synced emails
- **Guided onboarding**: Rollout continue (50% → 100%), monitor churn
- Merge custom fields planning into "Q2 backlog"

### Semana 5-6
- **Email integration**: QA + rollout
- **General polish**: Bugs, performance, edge cases
- **Customer success**: Comms about new features

---

## Metricas de Sucesso (30 dias)

| Feature | Métrica | Target | Baseline |
|---------|---------|--------|----------|
| Guided onboarding | 7-day retention | 50%+ | 30% |
| Email + Salesforce | Feature adoption | 40%+ | N/A |
| Combined | Churn | < 25% | 35% |

---

## Decisão Final

```
✅ P0: Guided onboarding (semana 1-2)
✅ P0: Email + Salesforce (semana 1-4)
❌ P2: Custom fields (defer para Q2)
❌ P3: AI prediction (defer, validate first)
❌ P3: Dashboard personalization (defer)
```

**Owner**: Lucas (PM)
**Data**: Jan 20, 2025
**Próxima review**: Semana 2 (go/no-go de onboarding antes de email)
```

---

## Dicas

- **RICE não é lei**: Se stakeholder discorda, conversa. Score é input, não output.
- **Confidence muda**: No mês 1 você tem 50% confiança. Mês 2 talvez 80%. Re-score.
- **Effort em semanas reais**: Inclua QA, design review, bugs. Não só "desenvolvimento".
- **Score muda com contexto**: Feature A era P3 em Janeiro, vira P0 em Março se contexto muda.
