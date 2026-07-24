# Jornada 0→1: Da Ideia ao Product-Market Fit

> **O guia definitivo para Product Managers que querem construir produtos com método.**
> Cada fase tem critérios claros de entrada e saída. Não avance sem passar pelo gate.

---

## Mapa da Jornada

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FASE 1    │    │   FASE 2    │    │   FASE 3    │    │   FASE 4    │
│  PROBLEM    │───▶│  PROBLEM    │───▶│  SOLUTION   │───▶│  SOLUTION   │
│  DISCOVERY  │    │  VALIDATION │    │  DISCOVERY  │    │  VALIDATION │
│             │    │             │    │             │    │             │
│ "Existe um  │    │ "O mercado  │    │ "Qual a     │    │ "Alguém     │
│  problema?" │    │  é real?"   │    │  melhor     │    │  pagaria?"  │
│             │    │             │    │  solução?"  │    │             │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
   GATE: 8/15         GATE: SAM +        GATE: 1 solução    GATE: Conversão
   descrevem          gaps claros +      selecionada com    > benchmark +
   problema           WTP detectada      evidência          skin-in-the-game
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FASE 5    │    │   FASE 6    │    │   FASE 7    │
│  MVP SPEC   │───▶│  LAUNCH &   │───▶│  PRODUCT-   │
│  & BUILD    │    │  EARLY      │    │  MARKET     │
│             │    │  TRACTION   │    │  FIT        │
│ "O que      │    │ "Funciona   │    │ "Temos      │
│  construir?"│    │  no mundo   │    │  PMF?"      │
│             │    │  real?"     │    │             │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
   GATE: PRD +         GATE: Retention    GATE: Sean Ellis
   stories +           curve flat +       ≥ 40% + organic
   riscos mapeados     activation > 25%   growth + LTV > 3xCAC
       │                  │                  │
       ▼                  ▼                  ▼
                                        🏁 PMF ALCANÇADO
                                        → Ir para Jornada 1→100
```

---

## Princípios Fundamentais

1. **Evidência antes de opinião** — Cada decisão precisa de dados, mesmo que qualitativos.
2. **Gates são inegociáveis** — Se não passou no gate, não avança. Sem exceção.
3. **Kill criteria definidos antes** — Saiba quando matar a ideia antes de começar.
4. **Velocidade > Perfeição** — O objetivo é aprender rápido, não entregar bonito.
5. **Product Trio sempre** — PM + Design + Eng juntos desde a Fase 1.

---

## FASE 1: PROBLEM DISCOVERY

### Objetivo
Encontrar um problema real que pessoas reais enfrentam com frequência e intensidade suficientes para justificar uma solução.

### O que fazer

1. **Definir personas-alvo** — Criar 2-3 personas com base em hipóteses iniciais. Não invente: baseie-se em observação direta ou experiência profissional.
2. **Conduzir 15+ entrevistas exploratórias** — Seguir o método Mom Test: perguntar sobre o passado e comportamentos reais, nunca sobre intenções futuras.
3. **Mapear a jornada atual do cliente** — Como ele resolve (ou não resolve) o problema hoje? Quais workarounds usa?
4. **Identificar Jobs-to-Be-Done** — Qual o "job" funcional, emocional e social que o cliente está tentando completar?
5. **Sintetizar padrões** — Agrupar insights em temas. Buscar problemas que aparecem espontaneamente em múltiplas entrevistas.

### Skills a usar

```bash
/persona "PM de startup early-stage que precisa validar ideias rápido"
/discovery "Dificuldades de PMs para validar hipóteses de produto"
/customer-journey "PM tentando validar uma ideia de produto novo"
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| Jobs-to-Be-Done (JTBD) | Clayton Christensen, *Competing Against Luck* | Identificar o "job" real por trás do comportamento |
| Mom Test | Rob Fitzpatrick, *The Mom Test* | Estruturar entrevistas que geram verdade, não validação |
| Continuous Discovery Habits | Teresa Torres, *Continuous Discovery Habits* | Criar cadência semanal de contato com clientes |

### Artefatos produzidos

- [ ] 2-3 fichas de persona documentadas
- [ ] 15+ notas de entrevista sintetizadas
- [ ] Mapa de jornada atual (as-is) do cliente
- [ ] Lista de JTBD priorizados por frequência e intensidade
- [ ] Resumo de padrões com citações diretas

### Decision Gate

> **Critério para avançar:** Pelo menos 8 dos 15 entrevistados descrevem o mesmo problema de forma espontânea (sem indução do entrevistador), com evidência de frequência (semanal+) e intensidade (impacto real no trabalho/vida).

**Se não passou:** Volte e entreviste mais pessoas, ou pivote o segmento-alvo.

### Exemplo prático

```bash
# Passo 1: Criar persona inicial
/persona "Gerente de operações de e-commerce médio (50-200 funcionários)
que precisa coordenar logística entre múltiplos fornecedores"

# Passo 2: Preparar guia de discovery
/discovery "Problemas de coordenação logística em e-commerces médios.
Foco em: comunicação com fornecedores, visibilidade de status,
gestão de exceções (atrasos, devoluções)"

# Passo 3: Mapear jornada atual
/customer-journey "Gerente de operações recebendo pedido de cliente,
coordenando com 3 fornecedores diferentes, gerenciando entrega
e lidando com problemas no caminho"
```

### Armadilhas comuns

1. **Confundir solução com problema** — "Precisamos de um app" não é problema. "Perco 3h/dia coordenando fornecedores por WhatsApp" é problema. Sempre pergunte "por quê?" até chegar na dor real.
2. **Entrevistar só amigos e conhecidos** — Amigos são gentis demais. Busque desconhecidos no segmento-alvo. Use LinkedIn, comunidades, cold outreach.
3. **Ignorar workarounds existentes** — Se a pessoa já usa planilha + WhatsApp + e-mail para resolver, o problema existe. Mas seu concorrente é esse combo, não o "nada".

---

## FASE 2: PROBLEM VALIDATION

### Objetivo
Confirmar que o problema identificado existe em um mercado grande o suficiente, com concorrência navegável e disposição real de pagamento.

### O que fazer

1. **Construir Lean Canvas** — Mapear problema, segmentos, proposta de valor única, canais, receita e custos em uma página.
2. **Dimensionar o mercado (TAM/SAM/SOM)** — TAM = mercado total. SAM = mercado endereçável. SOM = o que você pode capturar em 2-3 anos. Seja honesto.
3. **Analisar concorrência** — Mapear todas as alternativas (incluindo "não fazer nada" e workarounds manuais). Identificar gaps reais.
4. **Detectar willingness to pay** — Nas entrevistas, perguntar: "Quanto você gasta hoje tentando resolver isso?" e "Se existisse uma solução, quanto pagaria?"
5. **Formular hipóteses falsificáveis** — Transformar suposições em hipóteses testáveis com critérios claros de sucesso/fracasso.

### Skills a usar

```bash
/lean-canvas "Plataforma de coordenação logística para e-commerces médios"
/competitive-analysis "Soluções de gestão logística para e-commerce no Brasil.
Incluir: ERPs, TMS, soluções verticais, planilhas+WhatsApp"
/hypothesis "Se oferecermos visibilidade em tempo real do status de
fornecedores, gerentes de operações reduzirão tempo de coordenação
em 50% e pagarão R$500/mês pela solução"
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| Lean Canvas | Ash Maurya, *Running Lean* | Síntese do modelo de negócio em 1 página |
| TAM/SAM/SOM | Standard market sizing | Dimensionar oportunidade de mercado |
| Competitive Landscape | Michael Porter + adaptações | Mapear forças competitivas e gaps |

### Artefatos produzidos

- [ ] Lean Canvas preenchido e validado
- [ ] Análise de mercado TAM/SAM/SOM com fontes
- [ ] Mapa competitivo com posicionamento
- [ ] 5-10 hipóteses falsificáveis documentadas
- [ ] Evidência de willingness to pay (citações de entrevistas)

### Decision Gate

> **Critério para avançar:** SAM > R$ 100M (ou threshold relevante para seu contexto) + pelo menos 2 gaps claros na concorrência + evidência qualitativa de willingness to pay em 60%+ dos entrevistados.

**Se não passou:** Mercado pequeno demais? Pivote segmento. Sem gaps? Pivote abordagem. Sem WTP? O problema não dói o suficiente.

### Exemplo prático

```bash
# Passo 1: Lean Canvas
/lean-canvas "Plataforma SaaS de coordenação logística para e-commerces
médios brasileiros. Problema: gerentes perdem 15h/semana coordenando
fornecedores manualmente. Segmento: e-commerces com 50-200 funcionários
e 3+ fornecedores logísticos."

# Passo 2: Análise competitiva
/competitive-analysis "Mercado de gestão logística para e-commerce
no Brasil. Players: Bling, Tiny ERP, VTEX, Magazord, Frenet,
soluções manuais (planilha+WhatsApp). Analisar: preço, funcionalidades,
gaps, satisfação do cliente."

# Passo 3: Hipóteses de mercado
/hypothesis "Hipóteses para validar:
1. E-commerces médios gastam >R$5000/mês em ineficiência logística
2. 70% não usam TMS dedicado
3. Principal dor é visibilidade, não automação
4. Dispostos a pagar R$300-800/mês por solução"
```

### Armadilhas comuns

1. **Mercado grande não significa mercado acessível** — TAM de R$ 10B é irrelevante se seu SOM é R$ 500K. Foque no SOM realista dos primeiros 2 anos.
2. **Ignorar incumbentes e inércia** — "Ninguém resolve isso" quase nunca é verdade. Planilha+WhatsApp é um concorrente. A inércia do "bom o suficiente" é sua maior competidora.
3. **Lean Canvas sem validação** — Canvas é hipótese, não fato. Cada célula precisa ser testada. Um Canvas bonito não significa negócio viável.

---

## FASE 3: SOLUTION DISCOVERY

### Objetivo
Gerar múltiplas soluções possíveis, selecionar a mais promissora com base em evidência, e definir hipóteses de solução testáveis.

### O que fazer

1. **Construir Opportunity Solution Tree** — Partir do outcome desejado, mapear oportunidades (problemas validados) e gerar 3+ soluções para cada.
2. **Sessões de ideação com Product Trio** — PM + Design + Eng juntos. Divergir antes de convergir. Crazy 8s, How Might We, brainwriting.
3. **Avaliar soluções por impacto vs. esforço** — Usar ICE Score, RICE, ou framework similar para priorizar de forma transparente.
4. **Selecionar 1-2 soluções para testar** — Com base em evidência, não opinião do HiPPO (Highest Paid Person's Opinion).
5. **Definir hipóteses de solução** — Para cada solução selecionada, escrever hipótese falsificável com métricas de sucesso.

### Skills a usar

```bash
/opportunity-tree "Outcome: Reduzir tempo de coordenação logística em 50%.
Oportunidades validadas:
1. Falta de visibilidade do status de pedidos
2. Comunicação fragmentada com fornecedores
3. Gestão manual de exceções (atrasos, devoluções)"

/hypothesis "Se criarmos um dashboard unificado de status de fornecedores,
gerentes de operações conseguirão identificar problemas 2h antes
e reduzir tempo de coordenação em 50%"

/experiment-design "Testar se dashboard de visibilidade logística
resolve o problema de coordenação. Público: 20 gerentes de operações
de e-commerce. Duração: 2 semanas. Métrica: tempo gasto em coordenação."
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| Opportunity Solution Tree (OST) | Teresa Torres, *Continuous Discovery Habits* | Estruturar relação outcome → oportunidade → solução |
| Design Sprint | Jake Knapp / Google Ventures, *Sprint* | Testar soluções em 5 dias |
| Dual-Track Agile | Marty Cagan, *Inspired* | Discovery e delivery em paralelo |

### Artefatos produzidos

- [ ] Opportunity Solution Tree visual e documentada
- [ ] 3+ soluções exploradas com prós e contras
- [ ] Matriz de priorização (ICE, RICE ou similar)
- [ ] 1 solução selecionada com justificativa baseada em evidência
- [ ] Hipóteses de solução falsificáveis

### Decision Gate

> **Critério para avançar:** 3 ou mais soluções foram exploradas genuinamente (não só "a minha ideia original + 2 figurantes"). 1 solução selecionada com evidência de que ataca o problema validado. Product Trio alinhado na direção.

**Se não passou:** Volte para ideação. Se só tem 1 ideia, você não explorou o espaço de solução o suficiente.

### Exemplo prático

```bash
# Passo 1: Mapear árvore de oportunidades
/opportunity-tree "Outcome: E-commerces médios reduzem tempo de gestão
logística em 50%.

Oportunidade 1: Falta de visibilidade
  - Solução A: Dashboard unificado de status
  - Solução B: Alertas proativos por WhatsApp
  - Solução C: Integração direta com TMS dos fornecedores

Oportunidade 2: Comunicação fragmentada
  - Solução D: Chat centralizado com fornecedores
  - Solução E: Portal do fornecedor com status automático
  - Solução F: Bot que cobra status automaticamente"

# Passo 2: Hipótese da solução mais promissora
/hypothesis "Solução B (alertas proativos por WhatsApp) será mais efetiva
que Dashboard (Solução A) porque não exige mudança de comportamento.
Critério: 70% dos alertas geram ação em <30min vs. dashboard consultado
<2x/dia"

# Passo 3: Desenhar experimento
/experiment-design "Wizard of Oz: simular alertas WhatsApp manualmente
para 10 gerentes durante 1 semana. Medir: tempo de resposta a problemas,
satisfação (NPS), redução de tempo coordenação (self-report)."
```

### Armadilhas comuns

1. **Apaixonar-se pela primeira ideia** — A primeira solução quase nunca é a melhor. Force-se a gerar pelo menos 3 alternativas genuínas antes de escolher.
2. **Pular direto para código** — "Vamos construir e ver o que acontece" é a armadilha mais cara em produto. Teste a solução ANTES de construir.
3. **Ignorar o Product Trio** — PM decidindo sozinho gera soluções enviesadas. Design traz perspectiva do usuário. Eng traz viabilidade técnica. Os três juntos geram soluções melhores.

---

## FASE 4: SOLUTION VALIDATION

### Objetivo
Testar a solução escolhida com o mínimo de investimento possível, coletando evidência de que pessoas reais pagariam/usariam o produto.

### O que fazer

1. **Criar pretotype ou smoke test** — Landing page, Wizard of Oz, concierge, vídeo explicativo — qualquer coisa que simule o produto sem construí-lo.
2. **Definir métricas de sucesso antes** — Conversão alvo, número de sign-ups, depósitos, cartas de intenção. Defina ANTES de rodar o teste.
3. **Rodar experimento com skin-in-the-game** — Interesse verbal não conta. Precisa de compromisso real: e-mail, cadastro, depósito, pré-venda.
4. **Analisar resultados com rigor** — Usar /ab-test-analysis para calcular significância. Não declare vitória com N=12.
5. **Definir kill criteria** — Se conversão < X%, matar a ideia ou pivotar. Decida isso ANTES dos resultados.

### Skills a usar

```bash
/experiment-design "Smoke test com landing page para plataforma de
coordenação logística. Tráfego: LinkedIn Ads para gerentes de operações
de e-commerce. Conversão alvo: 5% para waitlist com e-mail corporativo.
Budget: R$2000. Duração: 2 semanas."

/ab-test-analysis "Landing page A (foco em economia de tempo) vs
Landing page B (foco em redução de erros).
A: 500 visitas, 32 sign-ups (6.4%)
B: 480 visitas, 18 sign-ups (3.75%)
Significância estatística?"

/hypothesis "Se 5% dos visitantes qualificados deixarem e-mail corporativo
na waitlist, validamos interesse real. Se <2%, pivotamos messaging.
Se <1%, pivotamos solução."
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| Pretotyping | Alberto Savoia, *The Right It* | Testar a ideia antes de construir o produto |
| Smoke Tests | Eric Ries, *The Lean Startup* | Medir demanda real com mínimo investimento |
| XYZ Hypothesis | Alberto Savoia | Formato: "X% de Y farão Z" — específico e falsificável |
| YODA Principle | Alberto Savoia | "Your Own Data, Abundantly" — seus dados, não dados de mercado |

### Artefatos produzidos

- [ ] Pretotype ou smoke test funcional
- [ ] Métricas de sucesso definidas antes do teste
- [ ] Kill criteria documentados
- [ ] Resultados do experimento com análise estatística
- [ ] Decisão documentada: go / pivot / kill

### Decision Gate

> **Critério para avançar:** Conversão acima do benchmark do segmento (tipicamente 3-8% para B2B SaaS) + evidência de skin-in-the-game (e-mail corporativo, pré-cadastro, depósito, carta de intenção) + amostra estatisticamente relevante (N > 100 para quanti).

**Se não passou:** Pivote o messaging, o segmento ou a solução. Se nada funciona em 3 iterações, volte para a Fase 1.

### Exemplo prático

```bash
# Passo 1: Desenhar experimento
/experiment-design "Concierge test: oferecer serviço manual de coordenação
logística para 5 e-commerces. Cobrar R$500/mês. Eu faço manualmente
o que o produto faria. Duração: 1 mês. Métricas: retenção no mês 2,
NPS, tempo economizado (medido), willingness to continue paying."

# Passo 2: Formular hipótese específica
/hypothesis "XYZ Hypothesis: 60% dos 5 e-commerces (3+) continuarão
pagando R$500/mês no mês 2. Se sim: validamos solução e preço.
Se não: entrevistar churners para entender gaps."

# Passo 3: Analisar resultados
/ab-test-analysis "Concierge test results:
- 5 empresas iniciaram, 4 completaram mês 1
- 3/4 renovaram para mês 2 (75% retenção)
- NPS médio: 8.5
- Tempo economizado reportado: 8-12h/semana
- 1 churn reason: 'não resolve exceções internacionais'
Análise de viabilidade e próximos passos?"
```

### Armadilhas comuns

1. **Confundir interesse com compromisso** — "Adorei a ideia!" não é validação. "Aqui está meu cartão de crédito" é validação. Sempre busque skin-in-the-game.
2. **Amostra muito pequena para conclusões** — 5 respostas não provam nada estatisticamente. Para testes quanti, busque N > 100. Para quali, sature os temas (geralmente 12-15 entrevistas).
3. **Não definir kill criteria antes** — Se você decide os critérios depois de ver os resultados, vai racionalizar qualquer número. Defina antes. Seja honesto.

---

## FASE 5: MVP SPEC & BUILD

### Objetivo
Especificar o mínimo absolutamente necessário para testar a proposta de valor no mundo real, com qualidade suficiente para aprender.

### O que fazer

1. **Escrever PRD focado** — Problema, persona, proposta de valor, escopo do MVP (o que entra e o que NÃO entra), métricas de sucesso.
2. **Criar User Story Map** — Mapear a jornada do usuário, definir o "walking skeleton" (fluxo mínimo end-to-end que funciona).
3. **Escrever user stories com acceptance criteria** — Formato Gherkin para clareza. Cada story é independente e testável.
4. **Rodar pre-mortem** — "Imaginem que falhamos espetacularmente. O que deu errado?" Mapear riscos e mitigações antes de começar.
5. **Instrumentar métricas desde o dia 0** — Analytics, eventos, funil de conversão. Se não mede, não aprendeu nada com o MVP.

### Skills a usar

```bash
/prd "Plataforma de alertas logísticos para e-commerce.
MVP: integração com 2 transportadoras + alertas WhatsApp automáticos
quando pedido atrasa > 2h. Persona: gerente de operações.
Métrica norte: tempo médio de resolução de problemas logísticos."

/user-stories "Fluxo MVP: Gerente conecta transportadora → sistema
monitora status → detecta atraso > 2h → envia alerta WhatsApp →
gerente toma ação → sistema registra resolução"

/acceptance-criteria "User story: Como gerente de operações, quero
receber alerta no WhatsApp quando um pedido atrasar mais de 2h,
para que eu possa agir antes do cliente reclamar."

/pre-mortem "MVP de alertas logísticos. Riscos a explorar:
integração com transportadoras falha, WhatsApp API instável,
gerentes ignoram alertas, volume de alertas muito alto (alert fatigue)"
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| User Story Mapping | Jeff Patton, *User Story Mapping* | Definir escopo mínimo do MVP |
| INVEST | Bill Wake | Critérios para boas user stories |
| Gherkin/BDD | Dan North | Formato Given/When/Then para acceptance criteria |
| Pre-mortem | Gary Klein, *Sources of Power* | Antecipar falhas antes de acontecerem |

### Artefatos produzidos

- [ ] PRD completo do MVP (max 3 páginas)
- [ ] User Story Map visual
- [ ] User stories com acceptance criteria (Gherkin)
- [ ] Pre-mortem com riscos e mitigações
- [ ] Plano de instrumentação de métricas
- [ ] Definition of Done para o MVP

### Decision Gate

> **Critério para avançar:** PRD aprovado pelo Product Trio + user stories escritas e estimadas + riscos críticos mapeados com mitigação + plano de métricas definido + QA pass no walking skeleton.

**Se não passou:** PRD incompleto = reescreva. Stories vagas = refine com eng. Sem métricas = não lance.

### Exemplo prático

```bash
# Passo 1: PRD
/prd "MVP LogAlert — Alertas logísticos para e-commerce

PROBLEMA: Gerentes de operações descobrem atrasos logísticos tarde
demais, quando o cliente já reclamou. Perdem 15h/semana monitorando
manualmente.

ESCOPO MVP:
- IN: Integração Correios + Jadlog, alertas WhatsApp, dashboard básico
- OUT: Múltiplas transportadoras, automação de resolução, app mobile
- PERSONA: Gerente de ops, e-commerce 50-200 funcionários
- MÉTRICA NORTE: Tempo médio detecção de problema (target: <30min)
- ANTI-GOALS: Não substituir TMS, não gerenciar estoque"

# Passo 2: Stories do walking skeleton
/user-stories "Walking skeleton LogAlert:
1. Gerente cria conta e conecta API dos Correios
2. Sistema importa pedidos ativos automaticamente
3. Sistema detecta atraso > 2h via polling
4. Sistema envia alerta WhatsApp com detalhes do pedido
5. Gerente marca problema como 'resolvido' via WhatsApp
6. Dashboard mostra métricas: alertas enviados, tempo resolução"

# Passo 3: Pre-mortem
/pre-mortem "LogAlert MVP pode falhar porque:
1. API dos Correios é instável (uptime ~95%)
2. WhatsApp Business API tem custo alto por mensagem
3. Gerentes podem ter alert fatigue com muitos alertas
4. Sem resolução automática, valor percebido pode ser baixo
5. Integração Jadlog pode demorar mais que estimado"
```

### Armadilhas comuns

1. **MVP que não é M (mínimo)** — Se o MVP tem 30 user stories, não é mínimo. Ruthlessly cut. O primeiro MVP do Dropbox foi um vídeo. O do Zappos era comprar sapatos manualmente.
2. **Specs vagas que geram retrabalho** — "O sistema deve ser rápido" não é spec. "Tempo de resposta < 500ms no P95" é spec. Invista tempo aqui para economizar em retrabalho.
3. **Não instrumentar métricas desde o dia 0** — O propósito do MVP é aprender. Se não tem analytics, events, funnels desde o lançamento, você construiu um protótipo caro, não um MVP.

---

## FASE 6: LAUNCH & EARLY TRACTION

### Objetivo
Lançar o MVP para um grupo controlado de early adopters, coletar dados reais de uso e iterar rapidamente com base em evidência.

### O que fazer

1. **Preparar checklist de lançamento** — Tudo que precisa estar pronto: infra, monitoring, suporte, comunicação, métricas.
2. **Definir estratégia de go-to-market** — Para quem lançar primeiro? Como atingir? Qual o messaging? Qual o canal?
3. **Lançar para cohort restrito** — Não lance para o mundo. Lance para 20-50 early adopters que validaram o problema na Fase 1.
4. **Medir AARRR desde o dia 1** — Acquisition, Activation, Retention, Revenue, Referral. Identifique o gargalo mais grave.
5. **Definir North Star Metric** — Uma métrica que captura o valor core entregue ao usuário. Otimize para ela.

### Skills a usar

```bash
/launch-checklist "LogAlert MVP launch. Infra em AWS, WhatsApp Business
API, integração Correios + Jadlog. Target: 30 e-commerces da waitlist.
Data: 2 semanas."

/gtm "Go-to-market LogAlert MVP.
Segmento: e-commerces médios brasileiros (50-200 func).
Canal primário: outbound para waitlist (300 leads).
Canal secundário: LinkedIn do fundador.
Messaging: 'Saiba de problemas logísticos antes do seu cliente.'"

/release-notes "LogAlert v0.1 — MVP Launch.
Novas funcionalidades: monitoramento automático Correios e Jadlog,
alertas WhatsApp em tempo real, dashboard de métricas básico."

/north-star "LogAlert — produto de alertas logísticos para e-commerce.
Proposta de valor: detectar problemas logísticos antes do cliente.
Candidatas a NSM: alertas acionados por dia, tempo médio detecção,
% pedidos com problema detectado proativamente."
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| AARRR (Pirate Metrics) | Dave McClure | Funil de métricas de crescimento |
| North Star Metric | Sean Ellis / Amplitude | Uma métrica que define sucesso do produto |
| Cohort Analysis | Standard analytics | Analisar comportamento por grupo temporal |

### Artefatos produzidos

- [ ] Checklist de lançamento completo
- [ ] Plano de GTM para early adopters
- [ ] Release notes publicadas
- [ ] North Star Metric definida e instrumentada
- [ ] Dashboard de AARRR funcional
- [ ] Plano de iteração semanal (cadência de sprints)

### Decision Gate

> **Critério para avançar:** Retention curve flattening (cohort de semana 1 retém >40% na semana 4) + activation rate > 25% (usuários que completam ação core) + North Star Metric definida e crescendo + feedback qualitativo positivo de 60%+ dos early adopters.

**Se não passou:** Activation baixa? Melhore onboarding. Retention caindo? O produto não entrega valor core. Volte para Fase 4 ou 5.

### Exemplo prático

```bash
# Passo 1: Preparar lançamento
/launch-checklist "LogAlert MVP — Checklist completo:
- [ ] Infra: AWS setup, monitoring, alertas de uptime
- [ ] WhatsApp Business API: conta aprovada, templates prontos
- [ ] Integrações: Correios e Jadlog testadas em produção
- [ ] Analytics: Mixpanel configurado com events do funil
- [ ] Suporte: Intercom configurado, FAQ básico
- [ ] Comunicação: E-mail de boas-vindas, onboarding flow
- [ ] Legal: Termos de uso, política de privacidade
- [ ] Contingência: Playbook para downtime, rollback plan"

# Passo 2: Definir NSM
/north-star "LogAlert. Análise das candidatas:
1. 'Alertas acionados/dia' — vanity, não mede valor
2. 'Tempo médio de detecção' — mede velocidade, não impacto
3. '% problemas detectados antes do cliente reclamar' — ESTA.
   Mede diretamente o valor core: proatividade.
Recomendação: NSM = % problemas detectados proativamente"

# Passo 3: GTM para early adopters
/gtm "LogAlert MVP GTM:
- 300 leads na waitlist, priorizar 30 que participaram de entrevistas
- E-mail pessoal do fundador (não marketing automation)
- Oferta: 3 meses grátis em troca de feedback semanal
- Onboarding: call 1:1 de 30min com cada cliente
- Sucesso = 20/30 ativados na primeira semana"
```

### Armadilhas comuns

1. **Lançar para todo mundo de uma vez** — Se lança para 10.000 pessoas e o produto quebra, perdeu 10.000 oportunidades. Lance para 30, aprenda, itere, lance para 100.
2. **Não medir nada** — "Os clientes parecem gostar" não é métrica. Instrumente tudo. Saiba exatamente onde o funil quebra.
3. **Mudar tudo de uma vez** — Se muda 5 coisas entre sprint 1 e sprint 2, não sabe qual causou a melhoria. Uma mudança por vez. Meça. Aprenda.

---

## FASE 7: PRODUCT-MARKET FIT

### Objetivo
Confirmar que o produto encontrou product-market fit real, não apenas um launch spike temporário, antes de investir em escala.

### O que fazer

1. **Rodar pesquisa Sean Ellis** — Perguntar aos usuários ativos: "Como você se sentiria se não pudesse mais usar [produto]?" Meta: 40%+ respondem "muito desapontado".
2. **Analisar retention por segmento** — PMF raramente é uniforme. Qual segmento tem melhor retention? Esse é seu ICP real.
3. **Verificar organic growth** — Usuários estão recomendando espontaneamente? Tem crescimento orgânico (não-pago)?
4. **Projetar unit economics** — LTV > 3x CAC é o benchmark mínimo. Mesmo que projeção, precisa ser crível.
5. **Documentar e comunicar** — Sintetizar aprendizados para stakeholders. Preparar o caso para investimento em crescimento.

### Skills a usar

```bash
/measure-pmf "LogAlert — dados atuais:
- 28 clientes ativos (de 30 originais)
- Retention M1: 93%, M2: 85%, M3: 82%
- Sean Ellis survey (24 respostas): 46% muito desapontado
- NPS: 52
- 5 clientes vieram por indicação orgânica
- Revenue: R$14.000 MRR (média R$500/cliente)
- CAC atual: R$200 (outbound), LTV projetado: R$4.800 (10 meses avg)"

/interview-synthesis "Sintetizar feedback de 28 clientes ativos:
- 12 entrevistas de profundidade realizadas no M3
- Principais temas: 'não consigo mais viver sem os alertas',
  'reduziu reclamações de clientes em 40%', 'precisa integrar mais
  transportadoras', 'dashboard precisa melhorar'"

/stakeholder-update "Update para investidores/board — LogAlert M3:
PMF confirmado no segmento e-commerce médio (50-200 func).
Sean Ellis: 46%. Retention M3: 82%. LTV/CAC: 24x.
Pedido: investimento para fase de growth. Target: 200 clientes em 6M."
```

### Frameworks teóricos

| Framework | Referência | Uso nesta fase |
|-----------|-----------|----------------|
| Sean Ellis Test (40%) | Sean Ellis, *Hacking Growth* | Pesquisa quantitativa de PMF |
| Superhuman PMF Engine | Rahul Vohra, *First Round Review* | Processo iterativo para melhorar PMF score |
| Reference Customers | Geoffrey Moore, *Crossing the Chasm* | Clientes que vendem seu produto por você |

### Artefatos produzidos

- [ ] Resultado da pesquisa Sean Ellis (% "muito desapontado")
- [ ] Análise de retention por segmento/cohort
- [ ] Evidência de crescimento orgânico
- [ ] Projeção de unit economics (LTV/CAC)
- [ ] Stakeholder update com caso para crescimento
- [ ] Definição de ICP refinada (quem tem mais PMF)

### Decision Gate

> **Critério para avançar para Jornada 1→100:** Sean Ellis >= 40% no segmento-alvo + crescimento orgânico detectado + LTV > 3x CAC (projeção conservadora) + retention curve estabilizada + 5+ reference customers.

**Se não passou:** Analise por segmento. PMF pode existir num subsegmento. Use o Superhuman PMF Engine para iterar: foque nos "muito desapontados", entenda o que amam, entregue mais disso.

### Exemplo prático

```bash
# Passo 1: Medir PMF
/measure-pmf "LogAlert — Rodar análise completa de PMF:
1. Sean Ellis survey para 28 clientes ativos
2. Segmentar resultados por: tamanho da empresa, vertical,
   número de transportadoras, tempo como cliente
3. Analisar retention curves por cohort (M1, M2, M3)
4. Mapear origem dos últimos 10 clientes (orgânico vs. outbound)
5. Calcular unit economics: CAC, LTV, payback period"

# Passo 2: Sintetizar aprendizados
/interview-synthesis "12 entrevistas de profundidade — LogAlert M3.
Padrões encontrados:
- Segmento forte: e-commerces de moda (100-200 func) com 3+ transportadoras
- Feature mais valorizada: alerta proativo no WhatsApp
- Feature mais pedida: integração com mais transportadoras
- Reason to stay: 'reduziu reclamações de cliente final em 40%'
- Reason to churn: 'só funciona com Correios e Jadlog (preciso de mais)'"

# Passo 3: Comunicar resultados
/stakeholder-update "Board update — LogAlert alcançou PMF:
- Sean Ellis: 46% (meta: 40%) ✅
- Retention M3: 82% (benchmark SaaS: 70%) ✅
- LTV/CAC: 24x (meta: 3x) ✅
- Organic growth: 18% dos novos clientes ✅
- ICP refinado: e-commerce de moda, 100-200 func, 3+ transportadoras
PEDIDO: R$500K para crescimento. Target: 200 clientes em 6 meses."
```

### Armadilhas comuns

1. **Confundir launch spike com PMF** — As primeiras semanas sempre parecem boas (novidade, entusiasmo). PMF real se confirma no M3+. Espere retention estabilizar antes de declarar vitória.
2. **Escalar antes de PMF** — Investir em growth antes de PMF é como jogar gasolina em fogo que não pegou. Você vai gastar dinheiro rápido sem resultado. PMF primeiro, growth depois.
3. **Ignorar segmentação** — PMF quase nunca é uniforme. Um segmento pode ter 60% Sean Ellis enquanto outro tem 15%. Identifique SEU segmento de PMF e domine-o antes de expandir.

---

## Resumo dos Gates

| Fase | Gate | Métrica-chave |
|------|------|---------------|
| 1. Problem Discovery | 8/15 descrevem problema espontaneamente | Frequência + intensidade do problema |
| 2. Problem Validation | SAM + gaps + WTP | Tamanho de mercado + disposição a pagar |
| 3. Solution Discovery | 3+ soluções, 1 selecionada com evidência | Diversidade de opções + evidência |
| 4. Solution Validation | Conversão > benchmark + skin-in-the-game | Taxa de conversão + compromisso real |
| 5. MVP Spec & Build | PRD + stories + riscos + QA | Completude e qualidade da spec |
| 6. Launch & Early Traction | Retention flat + activation > 25% | Retention + activation rate |
| 7. Product-Market Fit | Sean Ellis >= 40% + organic growth + LTV > 3xCAC | PMF score + unit economics |

---

## Quanto tempo leva?

Depende. Mas uma referência realista:

| Fase | Duração típica | Investimento |
|------|---------------|-------------|
| 1. Problem Discovery | 2-4 semanas | Tempo do PM |
| 2. Problem Validation | 1-2 semanas | Tempo do PM + pesquisa |
| 3. Solution Discovery | 1-2 semanas | Tempo do Product Trio |
| 4. Solution Validation | 2-4 semanas | R$1-5K em testes |
| 5. MVP Spec & Build | 2-4 semanas (spec) + 4-8 semanas (build) | Custo do time |
| 6. Launch & Early Traction | 4-8 semanas | Marketing + suporte |
| 7. Product-Market Fit | 8-16 semanas | Operação completa |
| **TOTAL** | **6-10 meses** | **Variável** |

> **Nota:** Essas fases não são estritamente sequenciais. Você vai voltar. Você vai iterar. A jornada real é mais como uma espiral do que uma linha reta. Mas os gates são inegociáveis.

---

*Próximo: [02-um-a-cem.md](02-um-a-cem.md) — Jornada 1→100: Do PMF ao Scale*
