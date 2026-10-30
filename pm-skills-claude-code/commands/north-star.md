# /north-star

## O que essa skill faz

Define **North Star Metric (NSM)** + constelacao de **Input Metrics** para guiar decisoes de produto. Classifica o tipo de negocio (Attention, Transaction, Productivity), avalia candidatos contra 7 criterios, e monta sistema de metricas acionavel.

Saida: **NSM escolhida** com justificativa, input metrics mapeadas, e dashboard recomendado.

---

## Quando usar

- Produto nao tem metrica clara de sucesso — cada time mede coisa diferente
- Stakeholders pedem "qual o numero mais importante?"
- Revenue e a unica metrica e voce sabe que isso e errado
- Time precisa de foco — muitas metricas, nenhuma direcao
- Revisao semestral de metricas (recomendado a cada 6-12 meses)

---

## Input esperado

**Minimo:**
- **Produto**: O que faz, para quem
- **Modelo de negocio**: Como ganha dinheiro
- **Estagio**: Early, growth, ou scale
- **Metricas atuais**: O que mede hoje (mesmo que informal)

**Opcional:**
- Revenue e unit economics
- Engagement data (DAU, WAU, MAU, feature usage)
- Retention curves
- Segmentos de usuario
- OKRs ou goals do trimestre

---

## 3 Business Games

Primeiro passo: classificar o tipo de negocio. Cada game tem NSM patterns diferentes.

### 1. Attention Game
**O que importa**: Tempo gasto no produto. Mais tempo = mais valor extraido (via ads, engagement, content consumption).

**Exemplos**: Facebook (DAU), Spotify (Time Listening), YouTube (Watch Time), Netflix (Viewing Hours), TikTok (Time Spent)

**NSM patterns**: Time spent, sessions/day, content consumed, DAU/MAU ratio

### 2. Transaction Game
**O que importa**: Volume e valor de transacoes. Cada transacao = valor entregue ao usuario.

**Exemplos**: Amazon (Purchase Frequency), Uber (Rides/Week), Airbnb (Nights Booked), Stripe (Payment Volume), DoorDash (Orders/Month)

**NSM patterns**: Transactions completed, GMV, items sold, bookings

### 3. Productivity Game
**O que importa**: Eficiencia — usuario faz mais em menos tempo ou com menos esforco.

**Exemplos**: Canva (Designs Created), Dropbox (Files Shared), Notion (Pages Created & Shared), Slack (Messages in Channels), Figma (Active Editors)

**NSM patterns**: Tasks completed, content created, workflows automated, collaboration events

---

## 7 Criterios para NSM Efetiva

Cada candidata a NSM deve ser avaliada contra estes 7 criterios:

### 1. Easy to Understand
Time inteiro entende sem explicacao? Se precisa de footnote, esta errado.
**Teste**: Explique para alguem de fora do time em 10 segundos.

### 2. Customer-Centric
Mede valor ENTREGUE ao cliente, nao valor CAPTURADO pela empresa. Revenue nao e NSM.
**Teste**: Se essa metrica sobe, o cliente fica mais feliz?

### 3. Sustainable Value
Nao e vanity metric. Mede valor real e duradouro, nao spike temporario.
**Teste**: Se essa metrica sobe artificialmente (growth hack), o negocio realmente melhora?

### 4. Vision Alignment
Conecta com a visao de longo prazo do produto. Se a visao muda, a NSM pode mudar.
**Teste**: Daqui a 5 anos, essa metrica ainda sera relevante?

### 5. Quantitative
Numero, nao sentimento. Mensuravel com dados que voce ja tem (ou pode coletar facilmente).
**Teste**: Consigo medir isso semanalmente com dados que tenho?

### 6. Actionable
Times podem influenciar diretamente. Se ninguem sabe como mover essa metrica, e inutil.
**Teste**: Se eu disser "aumente essa metrica 10%", o time sabe por onde comecar?

### 7. Leading Indicator
Prediz sucesso futuro (revenue, retention, growth). Nao e lagging como churn ou revenue.
**Teste**: Se essa metrica sobe hoje, revenue sobe em 3-6 meses?

---

## Principios de NSM (Lenny Research)

### 1. Measure value DELIVERED, not captured
Revenue mede quanto VOCE ganha. NSM mede quanto CLIENTE ganha. Se cliente ganha mais, voce ganha mais eventualmente.

### 2. Avoid lagging indicators
Retention e terrivel como NSM — quando sabe que caiu, ja e tarde. Prefira leading indicators (engagement, activation, usage).

### 3. Simple beats sophisticated
"Weekly Active Users who performed 3+ core actions within 7 days of signup weighted by recency" — NINGUEM vai lembrar isso. "Deals Created per Week" — todo mundo entende.

### 4. Name metrics evocatively
Spotify nao usa "Monthly Active Streamers". Usa "Time Spent Listening". Airbnb nao usa "Booking Conversion". Usa "Nights Booked". O nome importa.

### 5. Revenue is NEVER the North Star
Revenue e consequencia de entregar valor. Se otimizar direto para revenue, vai espremer cliente (raise prices, reduce value). Otimize para valor entregue — revenue segue.

### 6. Revisit every 6-12 months
Produto muda, mercado muda, estrategia muda. NSM de 18 meses atras pode estar errada. Revise com dados frescos.

---

## Processo

1. **Classificar business game** — Attention, Transaction, ou Productivity
2. **Brainstorm candidatas** — Listar 3-5 metricas potenciais para NSM
3. **Scoring contra 7 criterios** — Cada candidata recebe score 1-5 por criterio
4. **Selecionar NSM** — Maior score total + gut check do time
5. **Identificar 3-5 Input Metrics** — Metricas que alimentam a NSM
6. **Validar** — Times podem influenciar? Input metrics predizem NSM?
7. **Montar dashboard** — NSM + input metrics com cadencia de review

---

## Output

```markdown
# North Star Metric: [Produto]

## 1. Classificacao do Negocio

### Business Game: [Attention / Transaction / Productivity]

**Justificativa:**
[2-3 frases explicando por que esse game. O produto gera valor primariamente via tempo gasto, transacoes, ou eficiencia?]

**Exemplos similares:**
- [Produto A] (mesmo game) usa [NSM deles]
- [Produto B] (mesmo game) usa [NSM deles]

---

## 2. Candidatas a NSM

### Candidata A: [Nome evocativo da metrica]
- **Definicao**: [O que exatamente mede, com formula se necessario]
- **Frequencia**: [Diaria/Semanal/Mensal]
- **Dados disponíveis**: [Sim/Parcial/Nao]

### Candidata B: [Nome]
- **Definicao**: [...]
- **Frequencia**: [...]
- **Dados disponíveis**: [...]

### Candidata C: [Nome]
- **Definicao**: [...]
- **Frequencia**: [...]
- **Dados disponíveis**: [...]

---

## 3. Scoring

| Criterio | Peso | Candidata A | Candidata B | Candidata C |
|----------|------|-------------|-------------|-------------|
| Easy to Understand | 1x | [1-5] | [1-5] | [1-5] |
| Customer-Centric | 2x | [1-5] | [1-5] | [1-5] |
| Sustainable Value | 2x | [1-5] | [1-5] | [1-5] |
| Vision Alignment | 1x | [1-5] | [1-5] | [1-5] |
| Quantitative | 1x | [1-5] | [1-5] | [1-5] |
| Actionable | 2x | [1-5] | [1-5] | [1-5] |
| Leading Indicator | 2x | [1-5] | [1-5] | [1-5] |
| **Total (weighted)** | | **[X]** | **[Y]** | **[Z]** |

### Analise

**Vencedora: Candidata [X]**
- Maior score em [criterios mais importantes]
- Times ja conseguem influenciar
- Dados disponiveis para medir semanalmente

**Descartadas:**
- Candidata [Y]: [Motivo — ex: lagging indicator, nao acionavel]
- Candidata [Z]: [Motivo — ex: dificil de medir, nao customer-centric]

---

## 4. North Star Metric Definida

### [Nome Evocativo da Metrica]

**Definicao formal**:
[Descricao precisa do que mede, incluindo formula, periodo, e filtros]

**Baseline atual**: [X]
**Target (6 meses)**: [Y]
**Target (12 meses)**: [Z]

**Por que essa NSM?**
1. [Razao 1 — conecta com business game]
2. [Razao 2 — customer-centric]
3. [Razao 3 — leading indicator de revenue]

**Por que NAO revenue?**
[Explicacao de por que revenue seria problematica como NSM para esse produto]

---

## 5. Input Metrics (Constelacao)

Input metrics sao metricas que:
- Sao mais faceis de mover no curto prazo
- Contribuem diretamente para mover a NSM
- Cada time pode ser owner de pelo menos uma

### Constelacao

```
                    [NSM]
                  /   |   \
                /     |     \
     [Input 1]  [Input 2]  [Input 3]
         |           |           |
    [Time A]    [Time B]    [Time C]
```

### Input Metric 1: [Nome]
- **Definicao**: [O que mede]
- **Owner**: [Time responsavel]
- **Como influencia NSM**: [Mecanismo causal]
- **Baseline**: [X]
- **Target**: [Y]
- **Cadencia**: [Diaria/Semanal]

### Input Metric 2: [Nome]
- **Definicao**: [...]
- **Owner**: [...]
- **Como influencia NSM**: [...]
- **Baseline**: [...]
- **Target**: [...]

### Input Metric 3: [Nome]
- **Definicao**: [...]
- **Owner**: [...]
- **Como influencia NSM**: [...]
- **Baseline**: [...]
- **Target**: [...]

### Input Metric 4: [Nome] (opcional)
- [...]

### Input Metric 5: [Nome] (opcional — guardrail)
- **Tipo**: Guardrail (nao queremos piorar)
- **Definicao**: [...]
- **Threshold**: [Nao pode cair abaixo de X]

---

## 6. Validacao

### Teste de causalidade
Para cada input metric, verificar:
- [ ] Se Input 1 sobe, NSM sobe? [Evidencia]
- [ ] Se Input 2 sobe, NSM sobe? [Evidencia]
- [ ] Se Input 3 sobe, NSM sobe? [Evidencia]

### Teste de cobertura
- [ ] Todas as areas do produto tem pelo menos 1 input metric?
- [ ] Nenhum time ficou sem metrica acionavel?

### Teste de conflito
- [ ] Subir Input 1 NAO prejudica Input 2?
- [ ] Nenhuma input metric incentiva comportamento prejudicial?

---

## 7. Dashboard Recomendado

### Visao principal (check diario)
| Metrica | Ontem | 7 dias | 30 dias | Target | Status |
|---------|-------|--------|---------|--------|--------|
| **NSM**: [Nome] | [X] | [Trend] | [Trend] | [Y] | [On/Off track] |
| Input 1: [Nome] | [X] | [Trend] | [Trend] | [Y] | [...] |
| Input 2: [Nome] | [X] | [Trend] | [Trend] | [Y] | [...] |
| Input 3: [Nome] | [X] | [Trend] | [Trend] | [Y] | [...] |
| Guardrail: [Nome] | [X] | [Trend] | [Trend] | [Min Y] | [...] |

### Cadencia de review
| Frequencia | O que | Quem | Acao se off-track |
|-----------|-------|------|-------------------|
| Daily | Check NSM + inputs | PM | Flag anomalias |
| Weekly | Deep dive por input | Time leads | Ajustar taticas |
| Monthly | NSM trend analysis | PM + Exec | Repriorizar roadmap |
| 6 meses | NSM still right? | All leads | Reavaliar/trocar NSM |
```

---

## Exemplo

**Input:**
```
/north-star
Produto: CRM para vendas consultivas, B2B SaaS
Modelo: Per-seat subscription ($65/user/mo)
Estagio: Growth (200 clientes, 1500 users, $97K MRR)
Metricas atuais: MRR, DAU, deals created, churn
Visao: Todo vendedor consultivo fecha mais deals com menos caos
```

**Output:**
```markdown
# North Star Metric: Acme CRM

## 1. Classificacao

### Business Game: Productivity
CRM gera valor quando vendedor faz MAIS (mais deals, mais rapido, menos esforco). Nao e attention (nao quer tempo maximo no CRM) nem transaction (CRM nao e marketplace).

Similares:
- Figma (Productivity) → Active Editors
- Notion (Productivity) → Pages Created & Shared
- Salesforce (Productivity) → Pipeline Value Managed

---

## 2. Candidatas

### A: Deals Advanced per Week
Numero de deals que mudam de stage por semana (sinal de progresso ativo).

### B: Weekly Active Sellers
Usuarios que interagiram com pelo menos 1 deal nos ultimos 7 dias.

### C: Revenue Influenced
Valor total de pipeline que passou pelo CRM nos ultimos 30 dias.

### D: MRR
Receita recorrente mensal.

---

## 3. Scoring

| Criterio | Peso | Deals Advanced | Weekly Active | Rev Influenced | MRR |
|----------|------|---------------|---------------|---------------|-----|
| Easy to Understand | 1x | 5 | 5 | 3 | 5 |
| Customer-Centric | 2x | 5 | 3 | 4 | 1 |
| Sustainable Value | 2x | 5 | 3 | 4 | 2 |
| Vision Alignment | 1x | 5 | 4 | 4 | 3 |
| Quantitative | 1x | 5 | 5 | 4 | 5 |
| Actionable | 2x | 5 | 4 | 3 | 2 |
| Leading Indicator | 2x | 5 | 4 | 4 | 1 |
| **Total** | | **55** | **41** | **40** | **23** |

### Vencedora: Deals Advanced per Week

**Por que**: Mede exatamente o valor que entregamos — ajudar vendedores a progedir deals. E leading indicator (deals avancando hoje = revenue fechando em 2-4 meses). Todo time pode influenciar.

**Descartadas**:
- Weekly Active Sellers: Vanity — estar ativo nao significa produtividade
- Revenue Influenced: Lagging e dificil de atribuir
- MRR: Revenue e consequencia, nao causa. Nunca e NSM.

---

## 4. NSM: Deals Advanced per Week

**Definicao**: Numero total de deals que mudaram de stage (forward) por semana, across todos os usuarios ativos.

**Baseline**: 2,400 deals/semana
**Target (6m)**: 4,000 deals/semana
**Target (12m)**: 6,500 deals/semana

---

## 5. Input Metrics

```
            Deals Advanced per Week (NSM)
           /          |           \
     Activation    Engagement    Deal Quality
      Rate          Depth         Score
       |              |              |
   Growth Squad   Core Squad   AI/Analytics
```

### Input 1: Activation Rate (1o deal criado em 48h)
- Owner: Growth Squad
- Baseline: 35% → Target: 60%
- Influencia NSM: Mais users ativados = mais deals avancando

### Input 2: Engagement Depth (acoes por session)
- Owner: Core Product Squad
- Baseline: 4.2 acoes/session → Target: 7.0
- Influencia NSM: Users mais engajados avancam mais deals

### Input 3: Deal Health Score accuracy
- Owner: AI/Analytics Squad
- Baseline: 62% accuracy → Target: 85%
- Influencia NSM: Deals com health score bom avancam 2x mais rapido

### Guardrail: NPS
- Threshold: Nao cair abaixo de 35 (atual: 42)
- Se cair: Pausar growth e investigar

---

## 7. Dashboard

| Metrica | Ontem | 7d avg | 30d avg | Target | Status |
|---------|-------|--------|---------|--------|--------|
| **Deals Advanced/wk** | 358 | 2,430 | 2,390 | 4,000 | At Risk |
| Activation Rate | 37% | 36% | 35% | 60% | Off Track |
| Engagement Depth | 4.5 | 4.3 | 4.2 | 7.0 | On Track |
| Deal Health Accuracy | 63% | 62% | 62% | 85% | On Track |
| NPS (guardrail) | — | — | 42 | >35 | Healthy |
```

---

## Dicas

- **Revenue nunca e NSM**: Se seu "North Star" e MRR, voce esta otimizando para espremer cliente, nao para entregar valor.
- **Simplicidade ganha**: Se precisa de 30 segundos para explicar a metrica, escolheu errado.
- **Nomeie bem**: "Deals Advanced per Week" e melhor que "Deal Stage Transition Count". O nome inspira.
- **Input metrics sao o dia-a-dia**: NSM e direcao. Input metrics sao o que times movem toda semana.
- **Guardrails previnem otimizacao perversa**: Sempre tenha 1-2 metricas que NAO podem cair.
- **Revise a cada 6 meses**: Produto evolui, NSM pode precisar evoluir tambem.
