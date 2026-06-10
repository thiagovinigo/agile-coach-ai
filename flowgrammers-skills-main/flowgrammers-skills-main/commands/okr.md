# /okr

## O que essa skill faz

Gera **OKR cascade completo** (Objectives and Key Results) em 3 niveis: empresa → departamento → time. Baseado nos 9 principios de 55 product leaders (pesquisa Lenny Rachitsky) + framework Rezvani.

Saida: **OKR cascade formatado** com objetivos inspiradores, key results mensuraveis, e cadencia de review.

---

## Quando usar

- Trimestre novo, precisa definir metas claras para times
- Empresa cresceu e precisa alinhar multiplos times em direção unica
- Stakeholders pedem "qual a meta?" e ninguem tem resposta clara
- Quer sair de output-driven (features entregues) para outcome-driven (resultados alcançados)

---

## Input esperado

**Minimo:**
- **Estrategia**: Growth, retention, revenue, innovation ou operational
- **Contexto do produto**: O que faz, quem usa, estagio (early, growth, scale)
- **Metricas atuais**: Baseline dos numeros principais (users, revenue, churn, etc)

**Opcional:**
- Missao/visao da empresa
- OKRs do trimestre anterior (o que funcionou, o que nao)
- Numero de times/departamentos
- Constraints (budget, headcount, timeline)

---

## 9 Principios de OKR (Lenny Research)

Antes de gerar OKRs, aplicar estes principios:

### 1. Goals one step from company goals
Nao cascade em 5 niveis. Time-level OKR deve estar a 1 passo do company-level. Se precisa de 3+ niveis para conectar, o goal esta errado.

### 2. Build systems, not just goals
OKR sem sistema de execucao e review e wishful thinking. Defina: quem revisa, quando, como corrige rota.

### 3. Triangulate with 3 Key Results
Para cada Objective, usar 3 KRs complementares:
- **Hardcore number**: Metrica quantitativa dura (ex: 10K DAU)
- **Squishier quality**: Metrica de qualidade/satisfacao (ex: NPS > 50)
- **Dollar sign**: Metrica financeira (ex: $100K MRR)

### 4. Use absolute numbers, not ratios
"Aumentar conversao de 2% para 4%" e facil de gamer (reduz denominador). Prefira: "Converter 500 usuarios pagos por mes".

### 5. Ambitious goals force new thinking
Se o time consegue atingir com 10% mais esforco, o goal nao e ambicioso. Bons OKRs forcam repensar a abordagem.

### 6. Max 3 company goals
Mais que 3 = nenhum e prioridade. Single owner per goal — se 2 pessoas sao donas, ninguem e.

### 7. Focus on outcomes, not outputs
"Lancar feature X" e output. "Reduzir churn de 35% para 20%" e outcome. OKRs medem resultados, nao entregas.

### 8. Scoring 0.0 to 1.0
- 0.0-0.3: Failed (red)
- 0.4-0.6: Progress but fell short (yellow)
- 0.7: Sweet spot — ambicioso e atingivel
- 0.8-1.0: Ou overachieved ou goal era conservador

### 9. Review cadence matters
- **Weekly**: Check-in rapido (5 min por OKR — on track?)
- **Monthly**: Scoring parcial + ajuste de tatica
- **Quarterly**: Retro completa + set proximo ciclo

---

## Processo

1. **Classificar estrategia** — Growth, retention, revenue, innovation ou operational
2. **Definir Company-level Objective** — Inspirador, qualitativo, time-bound
3. **Set 3 Key Results por Objective** — Triangulando: number + quality + dollar
4. **Cascade para Department-level** — Alinhado mas com ownership claro
5. **Cascade para Team-level** — Acionavel, time pode influenciar diretamente
6. **Validar** — KRs sao outcomes? Sao mensuraveis? Times podem influenciar?
7. **Definir scoring** — 0.0-1.0, target 0.7
8. **Definir cadencia** — Weekly check-in, monthly scoring, quarterly retro

---

## Output

```markdown
# OKR Cascade: [Trimestre] — [Estrategia]

## Contexto

### Estrategia dominante
**[Growth / Retention / Revenue / Innovation / Operational]**

### Situacao atual
- **Produto**: [Nome, estagio]
- **Usuarios**: [X ativos, Y total]
- **Revenue**: [$X MRR]
- **Churn**: [X%]
- **NPS**: [X]

### Principios aplicados
- Max 3 objectives, single owner cada
- KRs em numeros absolutos (nao ratios)
- Triangulacao: hardcore number + quality + dollar
- Target 0.7 no scoring

---

## Company-Level OKRs

### Objective 1: [Frase inspiradora e qualitativa]
**Owner**: [Nome, Role]
**Periodo**: [Q1 2025 / Q2 2025 / etc]

| # | Key Result | Baseline | Target | Tipo | Score Atual |
|---|-----------|----------|--------|------|------------|
| KR1 | [Metrica quantitativa dura] | [X] | [Y] | Hardcore Number | 0.0 |
| KR2 | [Metrica de qualidade/satisfacao] | [X] | [Y] | Quality | 0.0 |
| KR3 | [Metrica financeira] | [$X] | [$Y] | Dollar Sign | 0.0 |

**Por que esse Objective?**
[1-2 frases conectando ao momento do negocio]

**Como sabemos que KRs estao certos?**
- KR1 mede [volume/escala]
- KR2 garante que [qualidade nao cai]
- KR3 conecta a [resultado financeiro]

---

### Objective 2: [Frase inspiradora]
**Owner**: [Nome, Role]

| # | Key Result | Baseline | Target | Tipo | Score |
|---|-----------|----------|--------|------|-------|
| KR1 | [...] | [...] | [...] | Hardcore Number | 0.0 |
| KR2 | [...] | [...] | [...] | Quality | 0.0 |
| KR3 | [...] | [...] | [...] | Dollar Sign | 0.0 |

---

## Department-Level OKRs

### [Departamento: Product]

#### Objective: [Conectado ao Company Obj 1]
**Owner**: [PM Lead]
**Alinha com**: Company Objective 1

| # | Key Result | Baseline | Target | Tipo | Score |
|---|-----------|----------|--------|------|-------|
| KR1 | [...] | [...] | [...] | Hardcore Number | 0.0 |
| KR2 | [...] | [...] | [...] | Quality | 0.0 |
| KR3 | [...] | [...] | [...] | Dollar Sign | 0.0 |

### [Departamento: Engineering]

#### Objective: [Conectado ao Company Obj 1 ou 2]
**Owner**: [Eng Lead]
**Alinha com**: Company Objective [X]

| # | Key Result | Baseline | Target | Tipo | Score |
|---|-----------|----------|--------|------|-------|
| KR1 | [...] | [...] | [...] | [...] | 0.0 |
| KR2 | [...] | [...] | [...] | [...] | 0.0 |
| KR3 | [...] | [...] | [...] | [...] | 0.0 |

### [Departamento: Sales/Marketing]

#### Objective: [Conectado ao Company Obj]
**Owner**: [Sales/Mkt Lead]

| # | Key Result | Baseline | Target | Tipo | Score |
|---|-----------|----------|--------|------|-------|
| KR1 | [...] | [...] | [...] | [...] | 0.0 |
| KR2 | [...] | [...] | [...] | [...] | 0.0 |
| KR3 | [...] | [...] | [...] | [...] | 0.0 |

---

## Team-Level OKRs

### [Time: Growth Squad]
**Alinha com**: Department Product → Company Obj 1

#### Objective: [Acionavel pelo time]

| # | Key Result | Baseline | Target | Owner | Score |
|---|-----------|----------|--------|-------|-------|
| KR1 | [...] | [...] | [...] | [Dev] | 0.0 |
| KR2 | [...] | [...] | [...] | [Designer] | 0.0 |
| KR3 | [...] | [...] | [...] | [PM] | 0.0 |

**Iniciativas planejadas:**
1. [Iniciativa A] — contribui para KR1
2. [Iniciativa B] — contribui para KR2
3. [Iniciativa C] — contribui para KR3

---

## Alignment Map

```
Company Obj 1 ──┬── Product Dept ──── Growth Squad
                 │                 └── Platform Squad
                 └── Sales Dept ───── SDR Team

Company Obj 2 ──┬── Engineering ───── Infra Squad
                 └── Product Dept ──── Retention Squad
```

---

## Cadencia de Review

| Frequencia | O que | Quem | Duracao |
|-----------|-------|------|---------|
| Weekly | Check-in: on track? blockers? | Time + PM | 15 min |
| Monthly | Scoring parcial + ajuste tatica | Dept leads | 30 min |
| Quarterly | Retro completa + set proximo ciclo | All leads + exec | 2h |

### Template de Weekly Check-in
Para cada KR:
- **Status**: On track / At risk / Off track
- **Progresso**: [X] de [Target] (score parcial: 0.X)
- **Blocker**: [Se houver]
- **Acao**: [O que muda essa semana]

### Criterios de Scoring Final
- **1.0**: Atingiu ou superou — goal era conservador?
- **0.7**: Sweet spot — ambicioso e entregou bem
- **0.5**: Progresso significativo mas ficou aquem
- **0.3**: Pouco progresso — o que deu errado?
- **0.0**: Nao moveu — OKR estava errado ou time nao priorizou

---

## Anti-patterns a Evitar

- **OKR como to-do list**: "Lancar feature X" nao e KR, e task
- **Ratio gaming**: "Melhorar conversao" sem numero absoluto
- **Cascade em 5 niveis**: Se precisa de 5 niveis, simplifique
- **Muitos OKRs**: Se tem 7 objectives, nenhum e prioridade
- **Sem owner**: Se 2 pessoas sao donas, ninguem e
- **Set and forget**: OKR sem review semanal e poster na parede
```

---

## Exemplo

**Input:**
```
/okr
Estrategia: growth
Contexto: B2B SaaS CRM com 500 usuarios ativos, $25K MRR
Churn: 8% mensal
NPS: 32
Meta: dobrar base de usuarios em 6 meses
```

**Output:**
```markdown
# OKR Cascade: Q2 2025 — Growth

## Contexto

### Estrategia dominante
**Growth** — produto tem PMF validado (NPS 32), hora de escalar.

### Situacao atual
- Produto: CRM consultivo, estagio growth
- Usuarios: 500 ativos (800 total)
- Revenue: $25K MRR
- Churn: 8% mensal (alto — precisa resolver em paralelo)
- NPS: 32 (bom para B2B)

---

## Company-Level OKRs

### Objective 1: Tornar nosso CRM a escolha obvia para times de venda consultiva
**Owner**: CEO
**Periodo**: Q2 2025

| # | Key Result | Baseline | Target | Tipo | Score |
|---|-----------|----------|--------|------|-------|
| KR1 | Atingir 1000 usuarios ativos mensais | 500 | 1000 | Hardcore Number | 0.0 |
| KR2 | Manter NPS acima de 40 durante crescimento | 32 | 40 | Quality | 0.0 |
| KR3 | Atingir $50K MRR | $25K | $50K | Dollar Sign | 0.0 |

**Por que esse Objective?**
PMF esta validado. Momento de capturar mercado antes que competitors copiem nossa abordagem de deal collaboration.

**Triangulacao:**
- KR1 mede escala (estamos crescendo?)
- KR2 garante que qualidade nao degrada com growth
- KR3 conecta crescimento a receita real

---

### Objective 2: Transformar churn em retenção como vantagem competitiva
**Owner**: VP Product
**Periodo**: Q2 2025

| # | Key Result | Baseline | Target | Tipo | Score |
|---|-----------|----------|--------|------|-------|
| KR1 | Reduzir usuarios que cancelam para max 25 por mes | 40/mes | 25/mes | Hardcore Number | 0.0 |
| KR2 | 80% dos usuarios completam onboarding em 48h | 45% | 80% | Quality | 0.0 |
| KR3 | Net Revenue Retention acima de 105% | 92% | 105% | Dollar Sign | 0.0 |

---

## Department-Level: Product

### Objective: Criar experiencia de primeiro uso que vicia
**Owner**: PM Lead
**Alinha com**: Company Obj 1 (KR1) + Company Obj 2 (KR2)

| # | Key Result | Baseline | Target | Tipo | Score |
|---|-----------|----------|--------|------|-------|
| KR1 | 300 novos usuarios completam setup no trimestre | 80/tri | 300/tri | Hardcore Number | 0.0 |
| KR2 | Time-to-value abaixo de 10 minutos | 45 min | 10 min | Quality | 0.0 |
| KR3 | Upgrade de free para paid: 150 usuarios | 40/tri | 150/tri | Dollar Sign | 0.0 |

---

## Team-Level: Growth Squad

### Objective: Fazer acquisition virar um motor previsivel
**Alinha com**: Product Dept → Company Obj 1

| # | Key Result | Baseline | Target | Owner | Score |
|---|-----------|----------|--------|-------|-------|
| KR1 | 500 signups qualificados por mes | 150/mes | 500/mes | Growth Dev | 0.0 |
| KR2 | Activation rate (1o deal criado em 24h) acima de 60% | 25% | 60% | Designer | 0.0 |
| KR3 | CAC abaixo de $50 por usuario ativo | $120 | $50 | PM | 0.0 |

**Iniciativas planejadas:**
1. Guided onboarding interativo — contribui para KR2
2. Referral program com incentivo — contribui para KR1
3. Otimizacao de paid channels — contribui para KR3

---

## Cadencia

| Freq | O que | Quem | Duracao |
|------|-------|------|---------|
| Weekly | Check-in por KR | Growth Squad + PM | 15 min |
| Monthly | Score parcial + ajustes | PM Lead + VP Product | 30 min |
| Quarterly | Retro + set Q3 | All leads + CEO | 2h |
```

---

## Dicas

- **OKR nao e contrato**: Se dados mudam, OKR pode mudar mid-quarter. Melhor ajustar que fingir.
- **Numero absoluto sempre**: "500 usuarios ativos" e melhor que "100% growth" — mais dificil de gamer.
- **Owner unico e inegociavel**: Se 2 pessoas sao donas, ninguem e responsavel quando falha.
- **0.7 e sucesso**: Se time atinge 1.0 em tudo, goals eram conservadores. Celebre o 0.7.
- **Iniciativas nao sao KRs**: KR = resultado. Iniciativa = como chegar la. Nao misture.
