# Jornada 1→100: Do PMF ao Scale

> **O guia para Product Managers que já encontraram PMF e precisam escalar com disciplina.**
> Pré-requisito: ter completado a Jornada 0→1 com PMF confirmado (Sean Ellis >= 40%).

---

## Mapa da Jornada

```
    JORNADA 0→1 COMPLETA
    (PMF Confirmado)
           │
           ▼
┌─────────────────────┐     ┌─────────────────────┐
│      FASE 8         │     │      FASE 9         │
│   GROWTH ENGINE     │────▶│  SCALING &           │
│                     │     │  EXPANSION           │
│  "Como crescer      │     │  "Como expandir      │
│   de forma          │     │   para novos         │
│   sustentável?"     │     │   mercados?"         │
│                     │     │                      │
│  ⚙️ Loops +         │     │  📈 Novos segmentos + │
│  Unit Economics     │     │  Pricing + Processos │
└──────────┬──────────┘     └──────────┬───────────┘
           │                           │
       GATE: Growth loop           GATE: Novas cohorts
       funcionando +               replicam sucesso +
       LTV/CAC > 3x +             revenue 2x YoY +
       Payback < 12M              processos repetíveis
           │                           │
           ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐
│      FASE 10        │     │      FASE 11        │
│  OPTIMIZATION       │────▶│  MATURITY &          │
│  & MOAT             │     │  REINVENTION         │
│                     │     │                      │
│  "Como nos          │     │  "Qual o próximo     │
│   defender?"        │     │   S-curve?"          │
│                     │     │                      │
│  🏰 Flywheel +      │     │  🔄 Three Horizons + │
│  Network Effects    │     │  Portfolio Mgmt      │
└──────────┬──────────┘     └──────────┬───────────┘
           │                           │
       GATE: Gross margins         GATE: H2 com early
       > benchmark +               traction + core
       switching costs altos +     mantendo margins
       moat identificado           │
           │                       ▼
           ▼              ┌─────────────────┐
                          │  NOVO CICLO     │
                          │  (Volta ao 0→1  │
                          │   para H2/H3)   │
                          └─────────────────┘
```

---

## A Grande Mudança: De 0→1 para 1→100

A Jornada 0→1 é sobre **encontrar**. A Jornada 1→100 é sobre **construir máquinas**.

| Dimensão | 0→1 | 1→100 |
|----------|-----|-------|
| Objetivo | Encontrar PMF | Escalar e defender |
| Ritmo | Exploratório, caótico | Cadenciado, processual |
| Decisões | Intuição + quanti leve | Dados + experimentação rigorosa |
| Time | Pequeno, generalista | Crescendo, especializado |
| PM role | Hands-on, faz tudo | Estratégico, lidera PMs |
| Risco | Não encontrar mercado | Crescer sem fundação |
| Erro fatal | Construir sem validar | Escalar sem unit economics |

---

## Como saber em qual fase você está

Responda estas perguntas com honestidade:

### Diagnóstico rápido

| Pergunta | Se SIM → | Se NÃO → |
|----------|----------|-----------|
| Sean Ellis >= 40% no seu segmento principal? | Fase 8+ | Volte para Fase 7 |
| Tem um growth loop funcionando e previsível? | Fase 9+ | Fase 8 |
| Novas cohorts/segmentos replicam o sucesso do ICP original? | Fase 10+ | Fase 9 |
| Tem moat claro (network effects, switching costs, escala)? | Fase 11+ | Fase 10 |
| Receita do core está estabilizando/declinando? | Fase 11 | Fase 8-10 |

### Sinais de alerta por fase

**Você ACHA que está na Fase 9, mas na verdade está na Fase 8 se:**
- Crescimento é linear, não exponencial
- Cada novo cliente custa mais que o anterior
- Não sabe explicar qual é seu growth loop
- LTV/CAC está piorando

**Você ACHA que está na Fase 10, mas na verdade está na Fase 9 se:**
- Novas cohorts têm retention pior que as primeiras
- Pricing não mudou desde o MVP
- Processo de vendas depende do fundador
- Não tem ICP documentado e compartilhado

**Você ACHA que está na Fase 11, mas na verdade está na Fase 10 se:**
- Não tem moat identificável
- Um concorrente novo poderia replicar seu produto em 6 meses
- Gross margins estão abaixo do benchmark da indústria
- Clientes não têm switching costs significativos

---

## FASE 8: GROWTH ENGINE

### Objetivo
Construir um motor de crescimento sustentável e previsível, com unit economics saudáveis.

### O que fazer

1. **Identificar e documentar seu growth loop** — Viral, content, paid, sales-led? Qual é o loop que, uma vez rodando, gera crescimento composto?
2. **Definir NSM + input metrics** — A North Star Metric já existe da Fase 7. Agora defina as 3-5 input metrics que a alimentam.
3. **Construir sistema de experimentação** — Cadência semanal de testes. Priorização por ICE. Documentação de aprendizados.
4. **Otimizar unit economics** — LTV/CAC > 3x é o mínimo. CAC payback < 12 meses. Monitore por cohort.
5. **Instrumentar métricas de retenção** — DAU/MAU, retention curves por cohort, churn por segmento. Retention é a fundação de tudo.

### Skills a usar

```bash
/north-star "LogAlert — Refinar NSM para fase de growth.
NSM atual: % problemas detectados proativamente.
Input metrics candidatas:
1. Número de integrações ativas por cliente
2. Alertas configurados por cliente
3. Tempo médio de resposta a alertas
4. % alertas que geram ação
Objetivo: criar dashboard de growth com NSM + inputs."

/okr "LogAlert Q1 — Growth Engine:
Objetivo: Construir motor de crescimento sustentável
KR1: Atingir 100 clientes pagantes (atual: 28)
KR2: LTV/CAC > 5x (atual: 24x, mas CAC vai subir com paid)
KR3: Implementar referral loop com NPS > 50
KR4: CAC payback < 6 meses em todos os canais"

/experiment-design "Testar referral loop para LogAlert:
Hipótese: se oferecermos 1 mês grátis para quem indicar,
30% dos clientes ativos farão pelo menos 1 indicação.
Cohort: 28 clientes atuais. Duração: 4 semanas.
Métricas: taxa de indicação, conversão dos indicados,
qualidade dos indicados (retention M1)."

/ab-test-analysis "Referral experiment results:
Grupo A (1 mês grátis): 14 clientes, 5 indicações (36%), 3 converteram
Grupo B (feature premium): 14 clientes, 2 indicações (14%), 1 converteu
Baseline: 0 indicações incentivadas antes do teste.
Avaliar: significância, recomendação, projeção de impacto."
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| Growth Loops | Brian Balfour / Reforge | Identificar loops de crescimento sustentáveis |
| Racecar Framework | Lenny Rachitsky | Turbos (growth), Engine (retention), Lubrificante (margin), Freio (churn) |
| NSM + Input Metrics | Amplitude / Sean Ellis | Sistema de métricas hierárquico para growth |

### Artefatos produzidos

- [ ] Growth loop documentado e visualizado
- [ ] Dashboard de growth: NSM + input metrics + unit economics
- [ ] OKRs de growth para o quarter
- [ ] Backlog de experimentos priorizado (ICE)
- [ ] Relatório semanal de experimentos (hipótese → resultado → aprendizado)
- [ ] Cohort analysis atualizada mensalmente

### Decision Gate

> **Critério para avançar:** Growth loop identificado e funcionando (crescimento mês a mês > 15%) + LTV/CAC > 3x em cohorts recentes + CAC payback < 12 meses + retention estável ou melhorando + sistema de experimentação rodando semanalmente.

**Se não passou:** Retention caindo? Volte para o produto. LTV/CAC < 3x? Otimize CAC ou aumente pricing. Sem loop claro? Teste 3 canais diferentes com budget limitado.

### Mudanca no papel do PM

De **generalista que faz tudo** para **Growth PM focado em métricas e experimentos**. Seu dia a dia muda:

- Antes: entrevistas, specs, priorização manual
- Agora: dashboards, experimentos, análise de dados, otimização de funil
- Skill crítica: pensamento analítico + velocidade de execução

### Exemplo prático

```bash
# Passo 1: Mapear o growth loop
/north-star "LogAlert growth loop analysis:
Loop atual (orgânico):
Cliente usa → detecta problema antes → cliente final satisfeito →
gerente conta para outros gerentes → novo cliente.

Loop candidato (product-led):
Cliente usa → convida fornecedor para portal → fornecedor vê valor →
fornecedor recomenda para outros e-commerces → novo cliente.

Qual loop tem maior potencial? Analisar com dados:
- Organic referral rate atual: 18% dos novos clientes
- Fornecedores conectados: 3.5 por cliente em média
- Cada fornecedor atende ~8 e-commerces em média"

# Passo 2: OKRs trimestrais
/okr "LogAlert Q2 — Escalar growth loop:
O1: Product-led growth loop funcionando
  KR1: 50% dos novos clientes vêm por indicação (fornecedor ou cliente)
  KR2: Viral coefficient > 0.5 (cada cliente traz 0.5 novos)
  KR3: Time-to-value < 48h para clientes indicados

O2: Unit economics sustentáveis para scale
  KR1: Blended CAC < R$300
  KR2: LTV projetado > R$6.000 (12 meses)
  KR3: Gross margin > 70%"

# Passo 3: Experimento semanal
/experiment-design "Semana 12 — Testar portal do fornecedor como
growth lever. Hipótese: se fornecedores tiverem portal próprio para
atualizar status, eles recomendarão LogAlert para seus outros clientes.
Setup: criar portal básico para 10 fornecedores dos nossos top clients.
Medir: adoção do portal (DAU), recomendações geradas, conversão."
```

### Armadilhas comuns

1. **Escalar sem unit economics** — Crescer 3x com LTV/CAC de 1.5x significa queimar dinheiro 3x mais rápido. Unit economics primeiro, growth depois. Sempre.
2. **Rodar múltiplos loops simultaneamente** — Escolha UM growth loop principal. Domine-o. Só depois adicione um segundo. Foco gera eficiência.
3. **Ignorar retention enquanto busca acquisition** — Acquisition sem retention é balde furado. Se retention cai, pare TUDO e conserte. Nenhum growth hack salva um produto com churn alto.

---

## FASE 9: SCALING & EXPANSION

### Objetivo
Expandir para novos segmentos, geografias ou verticais, replicando o sucesso do ICP original com processos escaláveis.

### O que fazer

1. **Refinar pricing com base em valor** — Pricing do MVP provavelmente está low. Agora que você sabe o valor entregue, precifique de acordo.
2. **Definir Ideal Customer Profile (ICP) expandido** — Quais segmentos adjacentes ao ICP original têm potencial similar?
3. **Criar battlecards competitivos** — Com mais clientes, concorrentes vão notar. Prepare o time de vendas/CS com material competitivo.
4. **Construir roadmap estratégico** — Não mais "o que construir essa semana", mas "onde queremos estar em 12 meses e por quê".
5. **Padronizar processos** — Vendas, onboarding, CS, development — tudo precisa funcionar sem o fundador presente.

### Skills a usar

```bash
/pricing "LogAlert pricing review:
Valor entregue (medido): redução de 40% em reclamações de clientes,
economia de 12h/semana do gerente de ops (custo médio: R$80/h = R$3.840/mês).
Pricing atual: R$500/mês flat.
Concorrentes: TMS genérico R$2.000-5.000/mês, nenhum faz alertas proativos.
Modelos a considerar: por pedido monitorado, por transportadora,
tiers por volume, value-based."

/ideal-customer-profile "LogAlert ICP expansion:
ICP atual (validado): e-commerce de moda, 100-200 func, 3+ transportadoras.
Segmentos adjacentes a avaliar:
1. E-commerce de eletrônicos (ticket maior, menos volume)
2. E-commerce de alimentos (perecíveis = urgência maior)
3. D2C brands (menores, mas alto volume de pedidos)
4. Marketplaces (muitos sellers = muita logística)
Critérios: retention potencial, WTP, tamanho do mercado, fit com produto."

/battlecard "LogAlert vs principais alternativas:
1. LogAlert vs gestão manual (planilha + WhatsApp)
2. LogAlert vs TMS genérico (ex: Intelipost, Frete Rápido)
3. LogAlert vs ERP com módulo logístico (ex: Bling, Tiny)
Para cada: strengths, weaknesses, quando escolher, objeções comuns,
killer features, proof points."

/roadmap "LogAlert roadmap 12 meses — fase de scaling:
Tema 1: Expansion (novos segmentos e transportadoras)
Tema 2: Platform (self-service, API, integrações)
Tema 3: Intelligence (previsão de atrasos, não só detecção)
Tema 4: Enterprise (multi-loja, permissões, SLA)
Priorizar por: impacto em revenue x esforço x alinhamento estratégico."
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| Value-Based Pricing | Patrick Campbell / ProfitWell | Precificar baseado no valor percebido, não no custo |
| Bowling Pin Strategy | Geoffrey Moore, *Crossing the Chasm* | Conquistar nichos sequencialmente, como pinos de boliche |
| ICP Refinement | Lincoln Murphy / Sixteen Ventures | Processo contínuo de refinar quem é seu cliente ideal |

### Artefatos produzidos

- [ ] Tabela de pricing atualizada com justificativa
- [ ] ICP expandido com critérios de qualificação por segmento
- [ ] Battlecards para top 3 concorrentes
- [ ] Roadmap de 12 meses com temas estratégicos
- [ ] Processos documentados: vendas, onboarding, CS, dev
- [ ] Playbook de expansão para novos segmentos

### Decision Gate

> **Critério para avançar:** Novas cohorts (de novos segmentos) replicam retention e NPS do ICP original + revenue crescendo 2x YoY + processos funcionam sem dependência do fundador + pelo menos 2 segmentos validados além do original.

**Se não passou:** Novas cohorts com retention baixa? Não é o segmento certo. Processos não escalam? Invista em ops antes de expandir. Revenue flat? Pricing ou go-to-market precisam de ajuste.

### Mudanca no papel do PM

De **hands-on execution** para **lideranca estratégica e comunicação formal**:

- Antes: experimentação diária, mexer no produto, falar com todo cliente
- Agora: definir direção, alinhar stakeholders, gerenciar trade-offs, processos
- Skill crítica: comunicação com board/investidores + pensamento estratégico
- Começa a contratar e gerenciar outros PMs

### Exemplo prático

```bash
# Passo 1: Revisão de pricing
/pricing "LogAlert — migrar de flat R$500/mês para tiers:
Tier Starter (até 500 pedidos/mês): R$399/mês
Tier Growth (501-2000 pedidos/mês): R$899/mês
Tier Scale (2001-5000 pedidos/mês): R$1.799/mês
Tier Enterprise (5000+): custom

Justificativa: valor entregue é proporcional ao volume.
Clientes com mais pedidos economizam mais com alertas proativos.
Análise: como isso afeta a base atual de 100 clientes?
Migração: como fazer sem churn?"

# Passo 2: Expansion para novo segmento
/ideal-customer-profile "Testar e-commerce de alimentos como novo segmento:
- Hipótese: perecíveis = urgência 10x maior que moda
- WTP potencial: maior (custo de perda de perecível é alto)
- Diferença do ICP atual: SLA mais apertado, integração com
  cold chain, regulação ANVISA
- Teste: 10 entrevistas + 5 pilotos
- Gate: retention M1 > 80% e NPS > 40"

# Passo 3: Roadmap estratégico
/roadmap "LogAlert 2026 roadmap:
Q1: Consolidar growth engine + pricing migration
Q2: Expandir para alimentos + 5 novas transportadoras
Q3: Platform play — API pública + self-service onboarding
Q4: Intelligence — ML para previsão de atrasos

Contexto estratégico: mercado de e-commerce BR crescendo 20%/ano.
Players de TMS são genéricos. Nossa vantagem: foco em alertas
proativos + WhatsApp-first. Moat futuro: dados de performance
de transportadoras que ninguém mais tem."
```

### Armadilhas comuns

1. **Expandir sem dominar o nicho original** — Se ainda não é referência no seu ICP original, não expanda. Ser medíocre em 3 segmentos é pior que ser excelente em 1.
2. **Pricing muito baixo por medo de churn** — Se Sean Ellis é 46%, seus clientes não vão embora por causa de um aumento justo. Precifique pelo valor. Clientes que churnam por preço provavelmente não eram ICP.
3. **Customizar para cada cliente grande** — Enterprise clients vão pedir features específicas. Dizer sim para tudo cria um Frankenstein. Construa plataforma, não serviços customizados.

---

## FASE 10: OPTIMIZATION & MOAT

### Objetivo
Construir defensibilidade sustentável — o que impede um concorrente bem-financiado de copiar seu produto em 12 meses?

### O que fazer

1. **Identificar e construir seu moat** — Network effects? Dados proprietários? Switching costs? Brand? Escala? Seja honesto sobre o que você tem (e não tem).
2. **Construir flywheel** — Ciclo virtuoso onde cada elemento fortalece os demais. Documente e otimize cada etapa.
3. **Otimizar gross margins** — Na fase de growth, margins podem ser sacrificadas. Agora precisam ser best-in-class. Renegociar custos, automatizar operação.
4. **Monitorar competição sistematicamente** — Alertas, battlecards atualizados, win/loss analysis trimestral.
5. **Preparar para o próximo nível** — Se você é PM, comece a formar outros PMs. Se é líder, comece a pensar em portfolio.

### Skills a usar

```bash
/strategy "LogAlert — análise de defensibilidade:
Moats potenciais:
1. Dados: 18 meses de dados de performance de transportadoras
   (nenhum concorrente tem isso)
2. Network effects: quanto mais e-commerces usam, mais fornecedores
   integram, mais valor para todos
3. Switching costs: integrações configuradas, histórico, workflows
4. Brand: 'LogAlert' virando sinônimo de 'alerta logístico'
Analisar: qual moat é mais forte? Onde investir?"

/competitive-analysis "LogAlert — competitive landscape atualizado:
Novos entrantes detectados: [startup X] levantou R$5M para fazer
algo similar. [TMS Y] adicionou feature de alertas.
Análise: ameaça real? Diferenciação sustentável? Resposta estratégica?"

/okr "LogAlert Q3 — Optimization & Moat:
O1: Fortalecer moat de dados
  KR1: Lançar 'LogAlert Insights' (benchmark de transportadoras)
  KR2: 500 clientes contribuindo dados (massa crítica)
  KR3: 3 artigos/reports publicados com dados exclusivos

O2: Otimizar margins
  KR1: Gross margin > 80% (atual: 72%)
  KR2: Custo de WhatsApp API reduzido em 30% (bulk pricing)
  KR3: Automação de onboarding: 80% self-service"

/stakeholder-update "Board Q3 update — LogAlert Optimization:
- Revenue: R$250K MRR (2x vs Q1)
- Gross margin: 78% (target 80%)
- Moat: dados de 18 meses de 400+ transportadoras
- Competitive response: [Startup X] lançou, mas sem dados históricos
- Net Revenue Retention: 115%
- Próximos passos: lançar LogAlert Insights, preparar Series A"
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| Flywheel | Jim Collins, *Good to Great* / Amazon | Ciclo virtuoso de fortalecimento mútuo |
| Network Effects | NFX / Andrew Chen, *The Cold Start Problem* | Efeitos de rede como moat |
| Platform Strategy | Sangeet Paul Choudary, *Platform Revolution* | Transição de produto para plataforma |

### Artefatos produzidos

- [ ] Mapa de moats com avaliação de força (1-5) e plano de investimento
- [ ] Flywheel documentado e visualizado
- [ ] Análise de gross margins com plano de otimização
- [ ] Win/loss analysis trimestral
- [ ] Competitive monitoring dashboard
- [ ] Plano de transição de liderança (PM → PM leader)

### Decision Gate

> **Critério para avançar:** Gross margins acima do benchmark da indústria (SaaS B2B: >70%) + switching costs identificáveis e mensuráveis + pelo menos 1 moat forte (dados, rede, marca ou escala) + Net Revenue Retention > 110%.

**Se não passou:** Sem moat? Você está vulnerável. Priorize construir defensibilidade antes de expandir mais. Margins baixas? Revise pricing e custos antes de crescer.

### Mudanca no papel do PM

**PM se torna product leader gerenciando outros PMs:**

- Antes: executar strategy, experimentar, optimizar
- Agora: definir visão, alinhar múltiplos PMs, gerenciar portfolio de features
- Skill crítica: liderança, coaching de PMs, negociação com C-level
- Foco: "Estamos construindo a coisa certa?" (não "como construir essa feature?")

### Exemplo prático

```bash
# Passo 1: Mapear flywheel
/strategy "LogAlert flywheel:
1. Mais e-commerces usam → mais dados de transportadoras
2. Mais dados → insights melhores (previsão de atrasos)
3. Insights melhores → mais valor para e-commerces
4. Mais valor → mais e-commerces usam (volta ao 1)

Acelerador: fornecedores integrados criam lock-in E atraem
novos e-commerces (network effect bilateral)

Onde investir para acelerar o flywheel? Qual etapa é o gargalo?"

# Passo 2: Análise competitiva profunda
/competitive-analysis "LogAlert vs [Startup X] — análise detalhada:
[Startup X]: R$5M seed, time de 15 pessoas, foco em alertas logísticos.
Diferenças: não tem dados históricos, não tem integrações com
transportadoras menores, UX mais moderna.
Risco: podem copiar features em 6 meses.
Nossa defesa: 18 meses de dados + 400 transportadoras integradas +
base de 200 clientes com switching costs.
Resposta estratégica: acelerar dados como moat, lançar Insights."

# Passo 3: OKRs de otimização
/okr "LogAlert Q4 — Fortalecer posição:
O1: LogAlert Insights como diferencial competitivo
  KR1: Lançar ranking público de transportadoras (PR + authority)
  KR2: 50% dos clientes usando Insights semanalmente
  KR3: 3 menções em mídia especializada

O2: Operational excellence
  KR1: Uptime > 99.9%
  KR2: Onboarding time < 2h (self-service)
  KR3: Support tickets / cliente < 1 por mês
  KR4: NPS > 60"
```

### Armadilhas comuns

1. **Otimizar sem defender** — Margins de 85% não significam nada se um concorrente pode copiar tudo em 6 meses. Moat primeiro, margins depois.
2. **Ignorar disruptores de baixo** — Clayton Christensen nos ensinou: a disrupção vem de baixo. Fique atento a startups resolvendo uma versão mais simples do seu problema para um segmento que você ignora.
3. **Burocracia mata velocidade** — Com mais processos, o risco é ficar lento. Mantenha cadência de experimentação. Documente, mas não burocratize. Speed is a feature.

---

## FASE 11: MATURITY & REINVENTION

### Objetivo
Identificar quando o produto principal está amadurecendo e investir no próximo S-curve antes que o crescimento estagne.

### O que fazer

1. **Monitorar sinais de maturidade** — Growth desacelerando? Mercado saturando? Margins comprimindo? Estes são sinais de que o S-curve atual está no topo.
2. **Aplicar Three Horizons** — H1 = core business (otimizar). H2 = adjacências (investir). H3 = bets transformacionais (explorar).
3. **Alocar recursos por horizonte** — Regra clássica: 70/20/10 (H1/H2/H3). Adapte para seu contexto.
4. **Criar "mini 0→1" para H2** — Volte para a Jornada 0→1 para cada novo produto/mercado. As fases se aplicam igualmente.
5. **Matar projetos sem tração** — Portfolio management exige disciplina para matar. Kill criteria definidos antes de investir.

### Skills a usar

```bash
/strategy "LogAlert — análise Three Horizons:
H1 (Core — otimizar): Alertas logísticos para e-commerce BR.
  Status: ~R$500K MRR, crescendo 10% MoM (desacelerando de 20%).
  Ação: otimizar margins, defender posição, milk the cow.

H2 (Adjacências — investir): Onde crescer?
  Candidato A: LogAlert para LATAM (mesmo produto, nova geo)
  Candidato B: LogAlert Insights como produto separado (dados como serviço)
  Candidato C: Automação de resolução (não só alertar, mas resolver)

H3 (Bets — explorar): Apostas transformacionais
  Candidato D: Plataforma de supply chain intelligence (além de logística)
  Candidato E: Marketplace de transportadoras (two-sided platform)

Para cada: TAM, fit estratégico, investimento necessário, timeline."

/discovery "Explorar H2 candidato C: automação de resolução logística.
Entrevistar clientes atuais sobre: o que fazem depois de receber o
alerta? Quanto tempo leva para resolver? O que poderia ser automatizado?
Hipótese: 60% das resoluções são padronizáveis."

/lean-canvas "H2: LogAlert Resolution — automação de resolução logística.
Problema: gerentes recebem alerta mas ainda resolvem manualmente.
Segmento: clientes atuais do LogAlert com > 50 alertas/semana.
Solução: workflows automáticos (re-routing, comunicação com cliente,
acionamento de backup). Revenue: upsell de R$500-1000/mês."

/prioritize "Portfolio LogAlert — priorizar investimento H2/H3:
Candidato A (LATAM): TAM alto, execução cara, distrai do core
Candidato B (Insights produto): TAM médio, baixo custo, fortalece moat
Candidato C (Resolução): TAM alto, upsell natural, clientes pedem
Candidato D (Supply chain): TAM enorme, 18+ meses, muito risco
Candidato E (Marketplace): TAM enorme, cold start problem, 24+ meses
Framework: ICE ou RICE com pesos estratégicos."
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| Three Horizons | McKinsey / Baghai, Coley & White | Gerenciar portfolio em 3 horizontes temporais |
| Second Curve | Charles Handy, *The Second Curve* | Iniciar o próximo S-curve antes do pico do atual |
| Portfolio Management | Standard PM practice | Alocar recursos entre múltiplos produtos/bets |

### Artefatos produzidos

- [ ] Análise Three Horizons com status e investimento por horizonte
- [ ] Avaliação de candidatos H2/H3 com critérios explícitos
- [ ] Lean Canvas para top 2 candidatos H2
- [ ] Kill criteria definidos para cada investimento H2/H3
- [ ] Roadmap de portfolio (não só produto)
- [ ] Review trimestral de portfolio com decisões go/kill

### Decision Gate

> **Critério de saúde:** H1 mantendo margins e market share + pelo menos 1 projeto H2 com early traction (passou pela Fase 4 do 0→1) + alocação de recursos documentada e respeitada + projetos sem tração mortos dentro do prazo.

**Se não passou:** Sem projetos H2? Comece agora — quando o H1 estagnar, será tarde demais. H2 sem traction? Revise ou mate. Alocação toda em H1? Você está otimizando para hoje, não para amanhã.

### Mudanca no papel do PM

**VP/CPO focado em portfolio, cultura de produto e visão de longo prazo:**

- Antes: liderar PMs, otimizar produto
- Agora: definir visão de portfolio, alocar recursos entre horizontes, construir cultura
- Skill crítica: pensamento de portfolio + coragem para matar projetos + visão de longo prazo
- Foco: "Em que negócio estamos?" (não "que feature construir?")

### Exemplo prático

```bash
# Passo 1: Análise de maturidade do core
/strategy "LogAlert core (H1) — sinais de maturidade:
- MoM growth: 20% → 15% → 12% → 10% (desacelerando)
- Market share no ICP principal: ~35% (alto, espaço limitado)
- Margins: 82% (excelente, otimizadas)
- NPS: 58 (estável)
- Competição: 3 novos entrantes no último ano

Diagnóstico: topo do primeiro S-curve. Core saudável mas desacelerando.
Urgência para H2: ALTA. Temos 12-18 meses antes de estagnação."

# Passo 2: Validar H2 mais promissor
/discovery "LogAlert Resolution (H2) — discovery com 15 clientes:
Perguntas:
1. Quando recebe alerta, o que faz nos primeiros 5 minutos?
2. Quantas resoluções são sempre iguais (mesmo playbook)?
3. Se pudéssemos resolver automaticamente, quanto pagaria a mais?
4. Quais resoluções NUNCA poderiam ser automatizadas?
5. Quantas horas/semana gasta resolvendo problemas pós-alerta?"

# Passo 3: Decisão de portfolio
/prioritize "LogAlert Portfolio Review Q4:
H1 — Core Alertas: MANTER. Investimento: 60% do time.
H2 — Resolution: GO. Early signals positivos. 30% do time.
H2 — LATAM: HOLD. Não agora. Complexidade operacional alta.
H2 — Insights produto: KILL. Baixa WTP detectada em discovery.
H3 — Supply chain platform: EXPLORE. 10% do time. 2 pessoas.
H3 — Marketplace: KILL. Cold start problem insolúvel no nosso estágio.

Próximo review: em 90 dias. Kill criteria para Resolution:
se não tiver 10 clientes piloto pagantes em 90 dias, matar."
```

### Armadilhas comuns

1. **Só defender o H1** — É natural proteger o que funciona. Mas sem H2, você está construindo numa plataforma que vai encolher. Reserve tempo e recursos para o futuro.
2. **Inovar sem disciplina** — "Vamos explorar tudo!" sem kill criteria gera desperdício. Cada bet precisa de hipótese, timeline e critério de morte. Trate H2/H3 como experimentos, não como hobbies.
3. **Não matar projetos ruins** — Sunk cost fallacy é real. "Já investimos 6 meses nisso" não é motivo para continuar. Se não tem traction, mate. Redirecione recursos para algo com potencial.

---

## Resumo da Jornada 1→100

| Fase | Objetivo | Gate | Mudança no PM |
|------|----------|------|---------------|
| 8. Growth Engine | Motor de crescimento sustentável | Loop funcionando + LTV/CAC > 3x + payback < 12M | Generalista → Growth PM |
| 9. Scaling & Expansion | Expandir mercado | Novas cohorts replicam + 2x YoY + processos | Executor → Estrategista |
| 10. Optimization & Moat | Construir defensibilidade | Margins > benchmark + moat + NRR > 110% | PM → Product Leader |
| 11. Maturity & Reinvention | Próximo S-curve | H2 com traction + core saudável | Leader → VP/CPO |

---

## As 5 Leis do Scaling

1. **Retention antes de Acquisition** — Nenhum growth hack salva um produto com churn alto. Conserte retention primeiro, sempre.

2. **Unit economics são inegociáveis** — Se LTV/CAC < 3x, pare de escalar e conserte. Crescer com economics ruins é acelerar em direção ao precipício.

3. **Processos antes de pessoas** — Antes de contratar, documente. Se o processo não funciona com 5 pessoas, não vai funcionar com 50.

4. **Moat antes de margins** — De que adianta 90% de gross margin se qualquer um pode copiar? Construa defensibilidade antes de otimizar lucro.

5. **O próximo S-curve começa antes do pico** — Quando o growth desacelera, já é tarde para começar H2. Comece quando tudo parece ir bem.

---

## Métricas-chave por Fase

| Métrica | Fase 8 | Fase 9 | Fase 10 | Fase 11 |
|---------|--------|--------|---------|---------|
| MoM Growth | >15% | >10% | >5% | Estável |
| LTV/CAC | >3x | >5x | >7x | >5x (blended) |
| Gross Margin | >60% | >70% | >80% | >75% (blended) |
| NRR | >100% | >110% | >120% | >110% (blended) |
| Sean Ellis | >40% | >50% | >50% | >40% (new products) |
| Payback | <12M | <9M | <6M | Varies |

---

## Checklist Final: Estou Pronto para Escalar?

Antes de investir em growth, verifique:

- [ ] **PMF confirmado** — Sean Ellis >= 40% no segmento principal
- [ ] **Retention estável** — Cohort M3 retém >70%
- [ ] **Unit economics saudáveis** — LTV/CAC > 3x, payback < 12M
- [ ] **Produto instrumentado** — Analytics em cada etapa do funil
- [ ] **ICP definido** — Sabe exatamente para quem vender (e para quem NÃO)
- [ ] **Growth loop identificado** — Sabe como cada cliente gera o próximo
- [ ] **Time minimamente pronto** — Ao menos PM + Eng + Design + 1 vendas/CS
- [ ] **Processos básicos** — Onboarding, suporte e vendas documentados

Se tem 6+ checks, pode escalar. Se tem <6, volte e construa a fundação.

---

*Anterior: [01-zero-a-um.md](01-zero-a-um.md) — Jornada 0→1: Da Ideia ao Product-Market Fit*
