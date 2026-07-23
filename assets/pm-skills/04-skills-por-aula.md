# Skills por Aula — Arsenal do PM com Claude Code

Mapeamento completo de quais skills usar em cada aula do Bloco B do curso (Aulas 3.7 a 3.18). Para cada aula: skills principais, skills complementares, comandos exatos, e o workflow prático que o aluno deve executar.

---

## Como usar este documento

1. **Leia a aula** — entenda o tema e o objetivo
2. **Abra o Claude Code** no diretório `ProductManager/`
3. **Execute os comandos** na ordem indicada, usando o contexto sugerido
4. **Cada skill gera um artefato** — o output de uma alimenta a próxima

> **Dica**: Todas as skills aceitam contexto livre após o comando. Quanto mais específico seu input, melhor o output.

---

## Aula 3.7 — Analisando Feedback de Usuário

### Objetivo
Transformar feedback bruto (NPS, tickets, pesquisas, reviews) em insights acionáveis e decisões de produto.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/interview-synthesis` | Sintetiza múltiplas fontes de feedback em JTBD, padrões comportamentais e recomendações priorizadas | Input: transcrições, tickets, surveys. Output: padrões + ranking de problemas |
| `/persona` | Gera personas baseadas em feedback real com pain points e behaviors | Input: padrões do feedback. Output: persona atualizada com evidências |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/hypothesis` | Transforma insight do feedback em hipótese testável | Quando um padrão do feedback sugere uma ação mas precisa validação |
| `/prioritize` | Aplica RICE nos problemas descobertos para decidir o que atacar | Quando há 5+ problemas e precisa sequenciar |

### Workflow da aula

```
PASSO 1 → /interview-synthesis
Input: Cole feedback bruto (NPS comments, tickets de suporte, reviews de app store)
Output: Padrões comportamentais + problemas rankeados + quotes representativos

PASSO 2 → /persona
Input: "Atualize/crie persona baseada nos padrões do feedback anterior"
Output: Persona com pain points validados por evidência real

PASSO 3 → /hypothesis
Input: "Top problema do feedback: [problema]. Crie hipótese testável."
Output: Hipótese com métricas, kill criteria, plano de validação

PASSO 4 (opcional) → /prioritize
Input: Lista dos 5 principais problemas do feedback
Output: RICE scoring + recomendação de sequência
```

### Exemplo prático para o aluno

```
/interview-synthesis

Feedback coletado (últimos 30 dias):

NPS Detratores (score 1-6):
- "O app trava quando tento exportar relatórios" (12 menções)
- "Não consigo achar onde configura notificações" (8 menções)
- "Preço subiu mas não vi feature nova" (5 menções)

Tickets de suporte (top 3):
1. Erro de exportação PDF — 45 tickets/mês
2. "Como desativo emails?" — 30 tickets/mês
3. Integração com Slack não funciona — 15 tickets/mês

Reviews App Store (últimas 20):
- 3 estrelas: "Bom produto mas UX confusa"
- 2 estrelas: "Crashou 3 vezes essa semana"
- 4 estrelas: "Amo o produto, se parasse de crashar seria 5"
```

### Artefatos que o aluno produz
- Síntese de feedback com padrões e ranking
- Persona atualizada com evidência de feedback
- 1-2 hipóteses testáveis a partir dos insights
- (Opcional) Backlog priorizado com RICE

---

## Aula 3.8 — Escrevendo PRDs com IA

### Objetivo
Criar um PRD completo e profissional em 8 seções, pronto para alinhamento com design e engenharia.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/prd` | Gera PRD completo em 8 seções: problema, audiência, solução, métricas, constraints, riscos, roadmap, aprovação | Input: problema + audiência + ideia de solução. Output: PRD pronto para review |
| `/hypothesis` | Estrutura a hipótese central do PRD antes de escrever | Input: problema identificado. Output: hipótese testável que fundamenta o PRD |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/lean-canvas` | Valida modelo de negócio rapidamente antes do PRD detalhado | Quando o PRD é para produto novo (não feature incremental) |
| `/pre-mortem` | Identifica riscos antes de finalizar o PRD | Passo final: valida que riscos no PRD estão completos |

### Workflow da aula

```
PASSO 1 → /hypothesis
Input: "Problema: [descreva]. Audiência: [quem]. Crie hipótese testável."
Output: Hipótese formatada com métricas de sucesso

PASSO 2 → /prd
Input: "
Problema: [do hypothesis]
Audiência: [personas]
Ideia de solução: [sua proposta]
Por quê agora: [urgência/timing]
"
Output: PRD completo em 8 seções

PASSO 3 (opcional) → /pre-mortem
Input: "Analise este PRD e faça pre-mortem: [cole PRD]"
Output: Tigers, Paper Tigers, Elephants — complementa seção de riscos

PASSO 4 → Refine
Input: "/prd [contexto anterior] Refine: [ajuste específico]"
Output: PRD atualizado
```

### Exemplo prático para o aluno

```
/prd
Problema: Novos usuários desistem em onboarding porque não conseguem
criar seu primeiro relatório em menos de 10 minutos
Audiência: Analistas de dados em empresas de 50-500 funcionários
Ideia: Wizard guiado que leva usuário do zero ao primeiro relatório em 5 min
Por quê agora: Churn de 40% em 7 dias, 65% nunca criaram relatório
```

### Artefatos que o aluno produz
- PRD completo com 8 seções
- Hipótese central documentada
- (Opcional) Pre-mortem com riscos mapeados
- PRD refinado após feedback

---

## Aula 3.9 — Gerando User Stories e Critérios de Aceite

### Objetivo
Quebrar um PRD em user stories INVEST com critérios de aceite em formato Given/When/Then, prontas para sprint.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/user-stories` | Gera 5-8 user stories no formato Mike Cohn com INVEST, priorizadas e com critérios de aceite | Input: PRD ou feature description + personas. Output: stories prontas para eng |
| `/acceptance-criteria` | Gera cenários detalhados em Given/When/Then cobrindo happy path, edge cases e erros | Input: user story específica. Output: 5-10 cenários de teste |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/persona` | Garante que as stories usam personas reais, não genéricas | Se não tem persona definida antes de escrever stories |
| `/prioritize` | Ordena stories por valor de negócio quando há muitas | Quando o PRD gera 10+ stories e precisa cortar para MVP |

### Workflow da aula

```
PASSO 1 → /user-stories
Input: "
PRD: [Guided First Report Experience]
Personas: Ana (Analista Jr), Carlos (Gerente de Dados)
Features: Wizard guiado, templates, validação em tempo real
"
Output: 5-8 stories priorizadas com aceite básico

PASSO 2 → /acceptance-criteria
Input: "
Feature: [Escolha a Story #1 do output anterior]
Regras de negócio: [constraints específicas]
"
Output: 5-10 cenários Given/When/Then (happy path + edge cases + erros)

PASSO 3 → Repetir Passo 2 para stories P0

PASSO 4 → Revisar Definition of Done
```

### Exemplo prático para o aluno

```
/user-stories
PRD: Wizard de primeiro relatório (onboarding guiado)
Personas: Ana (Analista Jr, primeira vez usando BI tools),
          Carlos (Gerente, quer que time seja produtivo rápido)
Features principais:
1. Wizard step-by-step (4 passos)
2. Templates pré-configurados (3 tipos)
3. Validação em tempo real (feedback visual)
4. Celebração ao completar (confetti + CTA)
```

Depois, para detalhar a story principal:

```
/acceptance-criteria
Feature: Step 1 do Wizard — Selecionar fonte de dados
Regras: Suporta CSV, Google Sheets, PostgreSQL.
Máximo 100MB para CSV. Timeout de 30s para conexão DB.
Contexto: Usuário está no passo 1 do wizard de onboarding.
```

### Artefatos que o aluno produz
- 5-8 user stories INVEST priorizadas
- Critérios de aceite detalhados para top 3 stories
- Sequência sugerida para sprints
- Definition of Done documentada

---

## Aula 3.10 — Análise Competitiva e de Mercado

### Objetivo
Mapear o cenário competitivo com forças, fraquezas, gaps e recomendações de posicionamento.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/competitive-analysis` | Gera feature matrix, SWOT, posicionamento, gaps e recomendações de diferenciação | Input: 3-5 competitors + seu produto + segmento. Output: análise completa |
| `/battlecard` | Cria battlecard para sales com objeções, win themes e landmines | Input: competitor específico. Output: card pronto para calls de venda |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/ideal-customer-profile` | Define ICP para entender QUEM você está disputando | Quando análise competitiva revela que diferentes competitors atendem segmentos diferentes |
| `/pricing` | Compara pricing dos competitors e identifica gaps | Quando preço é fator importante de diferenciação |

### Workflow da aula

```
PASSO 1 → /competitive-analysis
Input: "
Competitors: [Competitor A], [Competitor B], [Competitor C]
Seu produto: [descrição + posicionamento desejado]
Contexto: [segmento de cliente, tipo de uso]
Features que importam: [lista]
"
Output: Feature matrix + SWOT + posicionamento + features prioritárias

PASSO 2 → /battlecard
Input: "Crie battlecard: [Seu produto] vs [Competitor principal]"
Output: Comparison table, where we win/lose, objections, landmines

PASSO 3 (opcional) → /ideal-customer-profile
Input: "Baseado na análise competitiva, defina ICP para nosso produto"
Output: ICP com demographics, behaviors, JTBD, disqualification criteria

PASSO 4 (opcional) → /pricing
Input: "Compare pricing de [competitors] e recomende estratégia"
Output: Análise de pricing + recomendação
```

### Exemplo prático para o aluno

```
/competitive-analysis
Competitors: Notion, Confluence, Google Docs
Seu produto: Wiki corporativa com busca por IA e summarização automática
Contexto: Times de engenharia em empresas de 100-1000 funcionários
Features que importam: Busca semântica, integração com Slack/GitHub,
permissões granulares, templates, analytics de uso
```

### Artefatos que o aluno produz
- Análise competitiva completa (feature matrix + SWOT)
- Posicionamento recomendado (1 frase)
- 1 battlecard contra competitor principal
- (Opcional) ICP refinado
- (Opcional) Análise de pricing comparativa

---

## Aula 3.11 — Síntese de Pesquisa e Entrevistas

### Objetivo
Transformar transcrições e notas de entrevistas em JTBD, padrões comportamentais e recomendações acionáveis.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/interview-synthesis` | Sintetiza transcrições em JTBD, padrões, problemas rankeados e recomendações | Input: transcrições ou resumos de 3+ entrevistas. Output: síntese estruturada |
| `/persona` | Gera/atualiza personas a partir dos padrões da pesquisa | Input: insights da síntese. Output: persona com evidência real |
| `/opportunity-tree` | Mapeia oportunidades descobertas em OST | Input: outcome desejado + oportunidades da pesquisa. Output: árvore priorizada |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/customer-journey` | Mapeia jornada end-to-end a partir das entrevistas | Quando entrevistas revelaram friction points em múltiplos momentos |
| `/hypothesis` | Converte insight da pesquisa em hipótese testável | Quando um padrão forte emerge mas precisa validação quantitativa |

### Workflow da aula

```
PASSO 1 → /interview-synthesis
Input: "
Transcrições de 5 entrevistas com [persona] sobre [tema].
[Cole resumos ou transcrições]
"
Output: JTBD + padrões + problemas rankeados + quotes

PASSO 2 → /persona
Input: "Baseado na síntese de entrevistas, crie persona para [segmento]"
Output: Persona completa com 9 seções e confidence levels

PASSO 3 → /opportunity-tree
Input: "
Outcome desejado: [métrica que queremos mover]
Oportunidades descobertas nas entrevistas:
1. [Oportunidade A]
2. [Oportunidade B]
3. [Oportunidade C]
"
Output: OST com soluções e experimentos por oportunidade

PASSO 4 (opcional) → /customer-journey
Input: "Mapeie jornada de [persona] baseado nas entrevistas"
Output: Journey map com 7 estágios, emoções e pain points
```

### Exemplo prático para o aluno

```
/interview-synthesis

Contexto: 5 entrevistas com gerentes de marketing em scale-ups (50-200 pessoas)
sobre como gerenciam campanhas multi-canal.

Entrevista 1 (Maria, Head of Marketing, SaaS B2B):
"A gente usa 4 ferramentas diferentes para 4 canais. O reporting é um pesadelo.
Passo sexta inteira consolidando dados num Google Sheets."

Entrevista 2 (Pedro, Growth Manager, Fintech):
"O problema não é lançar campanha, é saber qual canal está performando.
Levo 3 dias pra ter um número confiável de CAC por canal."

Entrevista 3 (Ana, CMO, E-commerce):
"Já tentei 2 ferramentas all-in-one. Ambas eram medíocres em tudo.
Prefiro best-of-breed por canal, mas aí perco a visão unificada."

[continue com mais 2 entrevistas...]
```

### Artefatos que o aluno produz
- Síntese completa com JTBD e padrões
- Persona baseada em evidência real
- Opportunity Solution Tree priorizada
- (Opcional) Customer journey map

---

## Aula 3.12 — Priorização de Backlog com RICE

### Objetivo
Aplicar RICE scoring para priorizar features com trade-offs explícitos e recomendação clara.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/prioritize` | Aplica RICE (Reach, Impact, Confidence, Effort) + contexto de negócio. Gera ranking, trade-offs e roadmap | Input: lista de features + constraints + metas. Output: backlog priorizado |
| `/okr` | Define OKRs que orientam a priorização | Input: estratégia do trimestre. Output: OKRs cascateados que servem de filtro |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/north-star` | Define a métrica principal para calibrar Impact no RICE | Quando a equipe discorda sobre o que "Impact" significa |
| `/roadmap` | Transforma priorização em roadmap trimestral com timeline | Após priorizar, para comunicar a sequência ao time |

### Workflow da aula

```
PASSO 1 → /north-star (se não definida)
Input: "Defina NSM para [tipo de negócio] com [contexto]"
Output: North Star Metric + 3-5 input metrics

PASSO 2 → /okr
Input: "Crie OKRs para [estratégia do trimestre]"
Output: OKRs que orientam o que "sucesso" significa

PASSO 3 → /prioritize
Input: "
Features:
1. [Feature A — descrição]
2. [Feature B — descrição]
3. [Feature C — descrição]
4. [Feature D — descrição]
5. [Feature E — descrição]

Team: [X eng, Y design, Z PM]
Timeline: [semanas disponíveis]
Meta: [OKR ou North Star que orienta]
"
Output: RICE scores + top 3 + trade-offs + roadmap sugerido

PASSO 4 → /roadmap
Input: "Baseado na priorização, crie roadmap para [trimestre]"
Output: Timeline visual com fases e dependências
```

### Exemplo prático para o aluno

```
/prioritize
Features:
1. Dashboard unificado de métricas (todos os canais num lugar)
2. Integração nativa com TikTok Ads
3. Alertas automáticos de anomalia em CAC
4. Templates de relatório para board
5. API pública para integrações custom
6. Onboarding guiado para novos usuários

Team: 3 eng backend, 2 eng frontend, 1 design, 1 PM
Timeline: 8 semanas (Q2)
Meta: Reduzir churn de 15% para 8% e aumentar NPS de +20 para +40
```

### Artefatos que o aluno produz
- North Star Metric definida (se aplicável)
- OKRs do trimestre
- Backlog priorizado com RICE scores
- Trade-offs explícitos documentados
- Roadmap trimestral

---

## Aula 3.13 — Criando Dashboards de Métricas e PMF

### Objetivo
Especificar dashboards de métricas de produto — não desenhar gráficos, mas definir QUAIS perguntas o dashboard responde.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/north-star` | Define a métrica principal + input metrics que formam a "constelação" de métricas | Input: tipo de negócio + contexto. Output: NSM + 3-5 inputs + business game |
| `/okr` | Gera OKRs que se traduzem em métricas rastreáveis em dashboard | Input: estratégia. Output: KRs mensuráveis |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/experiment-design` | Define métricas de experimentos que devem aparecer no dashboard | Quando dashboard precisa rastrear A/B tests ativos |
| `/ab-test-analysis` | Mostra como interpretar dados do dashboard quando há testes | Quando dashboard já tem dados e precisa analisar |
| `/measure-pmf` | Define métricas de PMF (Sean Ellis, retention) para dashboard executivo | Para dashboards de board/investors |

### Workflow da aula

```
PASSO 1 → /north-star
Input: "
Produto: [tipo de produto]
Modelo de negócio: [SaaS, marketplace, etc]
Estágio: [early, growth, scale]
"
Output: NSM + input metrics + business game classification

PASSO 2 → /okr
Input: "Crie OKRs para Q2, estratégia: [growth/retention/revenue]"
Output: OKRs com KRs mensuráveis

PASSO 3 → Combinar NSM + OKR KRs em spec de dashboard
O aluno deve montar uma tabela:

| Métrica | Definição | Fórmula | Fonte | Baseline | Target | Visualização |
|---------|-----------|---------|-------|----------|--------|-------------|
| [NSM] | [def] | [calc] | [DB/API] | [atual] | [alvo] | [line chart] |
| [KR1] | [def] | [calc] | [DB/API] | [atual] | [alvo] | [bar chart] |

PASSO 4 (opcional) → /measure-pmf
Input: "Defina métricas de PMF para dashboard executivo"
Output: Sean Ellis score, retention curves, reference customers
```

### Exemplo prático para o aluno

```
/north-star
Produto: Plataforma de marketing analytics multi-canal
Modelo: SaaS B2B, per-seat pricing
Estágio: Growth (200 clientes, $500k ARR)
Segmento: Marketing teams em scale-ups (50-200 pessoas)
Valor principal: Consolidar dados de 4+ canais em visão única
```

### Artefatos que o aluno produz
- North Star Metric + 3-5 input metrics
- OKRs com KRs mensuráveis
- Spec de dashboard (tabela de métricas com definição, fórmula, fonte, visualização)
- (Opcional) Métricas de PMF para dashboard executivo

---

## Aula 3.14 — Escrevendo Release Notes e Comunicados

### Objetivo
Converter features técnicas em release notes orientadas a benefício, para diferentes audiências.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/release-notes` | Converte tickets/features em release notes orientadas a valor (não técnicas) | Input: lista de features/bugs shipped. Output: release notes para clientes |
| `/stakeholder-update` | Transforma notas confusas em status executivo limpo | Input: notas de sprint. Output: update estruturado para liderança |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/gtm` | Planeja comunicação de lançamento quando release é grande | Quando release merece campanha (não só nota) |
| `/launch-checklist` | Checklista de preparação quando release é significativo | Quando release tem impacto cross-functional |

### Workflow da aula

```
PASSO 1 → /release-notes
Input: "
Features que shiparam:
1. [Feature A — descrição técnica]
2. [Feature B — descrição técnica]
3. [Bug fix C]
4. [Performance improvement D]

Público: [todos os users / segmento específico]
Tom: [casual / profissional / técnico]
"
Output: Release notes orientadas a benefício

PASSO 2 → /stakeholder-update
Input: "
Sprint 14 — notas:
- Feature X saiu com 2 dias de atraso
- Bug Y resolvido, impactava 15% dos users
- Métrica Z melhorou 12% vs target de 10%
- Descoberta: entrevistas revelaram problema novo em onboarding
Para: CEO + VP Engineering + VP Sales
"
Output: Status executivo com situação → análise → próximos passos

PASSO 3 (se release grande) → /gtm
Input: "Feature principal do release: [feature]. Audiência: [quem]."
Output: Plano de comunicação com canais, mensagens, timeline
```

### Exemplo prático para o aluno

```
/release-notes
Features que shiparam nessa sprint:
1. Dashboard unificado de métricas (consolida Google Ads, Meta, TikTok)
2. Alertas automáticos quando CAC sobe > 20% vs semana anterior
3. Fix: relatórios PDF não abriam em Safari
4. Performance: tempo de carregamento de dashboards reduziu 40%

Público: Todos os clientes
Tom: Profissional mas acessível
Contexto: Maior release do trimestre
```

### Artefatos que o aluno produz
- Release notes para clientes (formato público)
- Release notes internas (formato técnico)
- Stakeholder update executivo
- (Opcional) Mini-GTM plan se release grande

---

## Aula 3.15 — Go to Market

### Objetivo
Criar estratégia GTM completa com posicionamento, canais, mensagens, métricas e timeline de lançamento.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/gtm` | Cria estratégia GTM com positioning, channels, messaging, timeline, metrics e contingência | Input: feature/produto + audiência + timeline + budget. Output: plano GTM completo |
| `/ideal-customer-profile` | Define ICP com demographics, behaviors, JTBD, needs | Input: dados de clientes/mercado. Output: ICP que orienta todo o GTM |
| `/battlecard` | Cria battlecard competitiva para enablement de sales | Input: competitor específico. Output: card para calls de venda |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/pricing` | Define/valida pricing antes do GTM | Quando lançamento inclui novo tier ou mudança de preço |
| `/launch-checklist` | Prepara checklist operacional de launch | Para garantir que eng, design, mkt, sales, support estão prontos |
| `/release-notes` | Cria as notas que serão usadas no GTM | Para o conteúdo que vai no email de lançamento |

### Workflow da aula

```
PASSO 1 → /ideal-customer-profile
Input: "Defina ICP para [produto] no segmento [segmento]"
Output: ICP com demographics, behaviors, JTBD, needs

PASSO 2 → /pricing (se aplicável)
Input: "Defina pricing para [produto] considerando [competitors e contexto]"
Output: Modelo + tiers + experiments

PASSO 3 → /gtm
Input: "
Feature/produto: [descrição]
Audiência: [ICP do passo 1]
Timeline: [data de launch]
Budget: [$X]
"
Output: Plano GTM completo (positioning, channels, messaging, timeline, metrics)

PASSO 4 → /battlecard
Input: "Crie battlecard: [seu produto] vs [competitor principal]"
Output: Battlecard para sales enablement

PASSO 5 → /launch-checklist
Input: "Crie checklist de lançamento para [produto/feature]"
Output: Checklist cross-functional com owners e dates
```

### Exemplo prático para o aluno

```
/gtm
Produto: Plataforma de marketing analytics com IA
Feature principal do lançamento: Dashboard unificado com alertas automáticos
Audiência: Marketing managers em scale-ups B2B (50-200 pessoas)
Timeline: Lançamento em 15 de Março
Budget: R$ 25.000 (ads, webinar, assets)
Contexto: Primeiro grande lançamento do ano,
          temos 200 clientes atuais + 500 na waitlist
```

### Artefatos que o aluno produz
- ICP documentado
- (Opcional) Pricing strategy
- Plano GTM completo com timeline
- Battlecard contra competitor principal
- Launch checklist operacional

---

## Aula 3.16 — Product Discovery

### Objetivo
Estruturar ciclo completo de descoberta: do problema vago até hipóteses testáveis com plano de experimentos.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/discovery` | Estrutura ciclo de discovery: framing JTBD → hipóteses → plano de experimentos | Input: problema + contexto + restrições. Output: síntese de discovery completa |
| `/opportunity-tree` | Mapeia Opportunity Solution Tree (Teresa Torres) | Input: outcome + oportunidades. Output: árvore hierárquica com soluções e testes |
| `/hypothesis` | Estrutura hipóteses testáveis com kill criteria | Input: crença + audiência. Output: hipótese formatada com métricas |
| `/experiment-design` | Design de pretotypes e testes lean | Input: hipótese a testar. Output: spec de experimento com go/no-go |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/persona` | Cria persona antes de começar discovery | Se não tem persona definida |
| `/customer-journey` | Mapeia jornada para encontrar pain points | Para visualizar onde na jornada o problema ocorre |
| `/lean-canvas` | Valida modelo de negócio se discovery é para produto novo | Para 0→1, não para feature incremental |

### Workflow da aula (Ciclo de Discovery completo)

```
PASSO 1 → /persona
Input: "Crie persona para [segmento] com foco em [domínio]"
Output: Persona com JTBD, pain points, behaviors

PASSO 2 → /discovery
Input: "
Problema: [descreva o problema conforme entendido hoje]
Contexto: [tamanho do mercado, users afetados, constraints]
Restrições: [tempo, budget, dependências]
"
Output: Framing JTBD + 3-5 hipóteses + plano de experimentos

PASSO 3 → /opportunity-tree
Input: "
Outcome: [métrica que queremos mover]
Oportunidades do discovery:
1. [oportunidade A]
2. [oportunidade B]
3. [oportunidade C]
"
Output: OST com soluções e experimentos priorizados

PASSO 4 → /hypothesis
Input: "Hipótese principal: [do discovery]. Detalhe com métricas e kill criteria."
Output: Hypothesis card completa

PASSO 5 → /experiment-design
Input: "Design experimento para testar: [hipótese]"
Output: Spec de experimento (método, amostra, métrica, threshold, timeline)
```

### Exemplo prático para o aluno

```
/discovery
Problema: Gerentes de marketing em scale-ups gastam 1 dia/semana
consolidando dados de múltiplos canais num spreadsheet manual
Contexto: Mercado de marketing analytics ~$5B, 50k+ scale-ups no Brasil,
cada uma com 2-5 profissionais de marketing
Restrições: Precisamos decidir em 3 semanas se construímos MVP
ou pivotamos para outro segmento
```

### Artefatos que o aluno produz
- Persona completa
- Síntese de discovery com framing JTBD
- Opportunity Solution Tree priorizada
- 2-3 hipóteses detalhadas com kill criteria
- 2-3 experimentos desenhados com go/no-go

---

## Aula 3.17 — Estratégia de Produto

### Objetivo
Desenhar estratégia de produto completa com visão, segmentos, métricas, roadmap e defesa para stakeholders.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/strategy` | Canvas de estratégia com 9 seções (visão, segmento, problema, solução, diferenciação, monetização, métricas, roadmap, riscos) | Input: visão + problema + segmento. Output: canvas completo |
| `/okr` | OKRs cascateados que traduzem estratégia em metas | Input: estratégia definida. Output: OKRs company→team |
| `/north-star` | Define NSM que ancora toda a estratégia | Input: modelo de negócio. Output: NSM + input metrics |
| `/roadmap` | Transforma estratégia em roadmap executável | Input: features priorizadas + constraints. Output: timeline trimestral |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/lean-canvas` | Valida modelo de negócio antes de estratégia detalhada | Para produtos novos ou pivots |
| `/competitive-analysis` | Informa posicionamento na estratégia | Se não tem análise competitiva atualizada |
| `/pricing` | Define monetização (seção 5 da estratégia) | Se pricing é parte central da estratégia |
| `/stakeholder-update` | Comunica estratégia para board/exec | Para a apresentação final |

### Workflow da aula

```
PASSO 1 → /north-star
Input: "Defina NSM para [produto/negócio]"
Output: NSM + input metrics + business game

PASSO 2 → /strategy
Input: "
Visão: [onde produto deve estar em 3-5 anos]
Problema: [market pain principal]
Segmento: [quem são os usuários]
"
Output: Canvas de estratégia 9 seções

PASSO 3 → /okr
Input: "Baseado na estratégia, crie OKRs para [próximo trimestre]"
Output: OKRs cascateados

PASSO 4 → /roadmap
Input: "
Features priorizadas: [do strategy]
Team: [recursos disponíveis]
Timeline: [próximo trimestre]
"
Output: Roadmap com fases, dependências, milestones

PASSO 5 → /stakeholder-update
Input: "Resuma a estratégia para apresentar ao board"
Output: Status executivo com visão, dados, recomendação
```

### Exemplo prático para o aluno

```
/strategy
Visão: Ser a plataforma definitiva de analytics para marketing teams
em scale-ups — onde dados de todos os canais viram decisões em minutos,
não dias.
Problema: Marketing teams em scale-ups gastam 20%+ do tempo em
reporting manual em vez de otimizar campanhas.
Segmento: Marketing managers e CMOs em scale-ups B2B/B2C
com 50-500 funcionários que investem $50k+/mês em ads.
```

### Artefatos que o aluno produz
- North Star Metric definida
- Canvas de estratégia completo (9 seções)
- OKRs do próximo trimestre
- Roadmap trimestral com fases
- Stakeholder update para board/exec

---

## Aula 3.18 — Preparando Apresentações para Stakeholders

### Objetivo
Transformar dados, discovery, strategy e progresso em comunicação executiva eficaz para diferentes audiências.

### Skills principais

| Comando | O que faz | Quando usar nesta aula |
|---------|----------|----------------------|
| `/stakeholder-update` | Transforma notas confusas em status executivo: situação → análise → opções → recomendação → próximos passos | Input: notas de sprint/discovery/decisão. Output: update executivo |
| `/measure-pmf` | Gera relatório de PMF com evidências para investors/board | Input: dados de uso. Output: PMF assessment com stage e evidence |
| `/roadmap` | Comunica plano trimestral visual para stakeholders | Input: features priorizadas. Output: timeline com milestones |

### Skills complementares

| Comando | O que faz | Quando usar |
|---------|----------|-------------|
| `/strategy` | Contexto estratégico para apresentação | Quando stakeholders precisam do "big picture" |
| `/okr` | OKRs para mostrar alinhamento de metas | Quando board quer ver metas quantitativas |
| `/release-notes` | Resume o que shipou (para seção de "progresso") | Quando update inclui o que foi entregue |
| `/north-star` | Mostra métrica principal e evolução | Para dashboards de board |

### Workflow da aula

**Cenário A: Board Meeting / Investor Update**
```
PASSO 1 → /measure-pmf
Input: "Avalie PMF para [produto] com [dados de uso]"
Output: PMF stage + score + evidence + action plan

PASSO 2 → /okr
Input: "Mostre OKRs do trimestre com scoring atual"
Output: OKRs com progresso (0.0-1.0)

PASSO 3 → /roadmap
Input: "Roadmap atualizado para próximo trimestre"
Output: Timeline visual para board

PASSO 4 → /stakeholder-update
Input: "
Compile para board meeting:
- PMF: [resultado do passo 1]
- OKRs: [resultado do passo 2]
- Roadmap: [resultado do passo 3]
- Decisão necessária: [se houver]
"
Output: Board update completo (1-2 páginas)
```

**Cenário B: Sprint Review / Weekly Update**
```
PASSO 1 → /release-notes
Input: "O que shipou essa sprint"
Output: Lista de entregas orientada a valor

PASSO 2 → /stakeholder-update
Input: "
Sprint 15 — notas confusas:
[Cole suas notas brutas]
Para: [audiência]
Tipo: [informar ou decisão necessária]
"
Output: Status executivo limpo
```

**Cenário C: Decision Request**
```
PASSO 1 → /stakeholder-update
Input: "
Situação: [contexto da decisão]
Dados: [evidências]
Opções: [A, B, C]
Urgência: [timeline]
Para: [quem decide]
"
Output: Update com opções + prós/contras + recomendação
```

### Exemplo prático para o aluno

```
/stakeholder-update
Notas da última quinzena (para board meeting):

Produto:
- Dashboard unificado lançado, 65% dos users adotaram em 2 semanas
- NPS subiu de +20 para +35 após launch
- 3 enterprise deals in pipeline ($150k total ARR)

Problemas:
- Integração com TikTok atrasou 1 semana (API instável deles)
- Churn subiu de 8% para 10% no segmento SMB (investigando)
- 2 engenheiros saíram, hiring em andamento

Decisões necessárias:
- Aprovar budget de $50k para campanha de Q2
- Decidir se investe em TikTok integration ou prioriza retention

Para: CEO, CFO, VP Sales
Tom: Executivo, transparente, data-driven
```

### Artefatos que o aluno produz
- Board/investor update completo
- Sprint review formatado
- Decision request com opções e recomendação
- (Opcional) PMF assessment para context
- (Opcional) OKR scorecard atualizado

---

## Resumo: Mapa de Skills por Aula

| Aula | Tema | Skills Principais | Skills Complementares |
|------|------|-------------------|----------------------|
| **3.7** | Feedback de Usuário | `/interview-synthesis`, `/persona` | `/hypothesis`, `/prioritize` |
| **3.8** | PRDs com IA | `/prd`, `/hypothesis` | `/lean-canvas`, `/pre-mortem` |
| **3.9** | User Stories & AC | `/user-stories`, `/acceptance-criteria` | `/persona`, `/prioritize` |
| **3.10** | Análise Competitiva | `/competitive-analysis`, `/battlecard` | `/ideal-customer-profile`, `/pricing` |
| **3.11** | Síntese de Pesquisa | `/interview-synthesis`, `/persona`, `/opportunity-tree` | `/customer-journey`, `/hypothesis` |
| **3.12** | Priorização RICE | `/prioritize`, `/okr` | `/north-star`, `/roadmap` |
| **3.13** | Dashboards Métricas | `/north-star`, `/okr` | `/experiment-design`, `/measure-pmf` |
| **3.14** | Release Notes | `/release-notes`, `/stakeholder-update` | `/gtm`, `/launch-checklist` |
| **3.15** | Go to Market | `/gtm`, `/ideal-customer-profile`, `/battlecard` | `/pricing`, `/launch-checklist` |
| **3.16** | Product Discovery | `/discovery`, `/opportunity-tree`, `/hypothesis`, `/experiment-design` | `/persona`, `/customer-journey`, `/lean-canvas` |
| **3.17** | Estratégia de Produto | `/strategy`, `/okr`, `/north-star`, `/roadmap` | `/lean-canvas`, `/competitive-analysis`, `/pricing` |
| **3.18** | Apresentações Stakeholders | `/stakeholder-update`, `/measure-pmf`, `/roadmap` | `/strategy`, `/okr`, `/release-notes` |

---

## Cobertura das 27 Skills nas Aulas

| Skill | Aulas onde aparece | Papel |
|-------|--------------------|-------|
| `/persona` | 3.7, 3.9, 3.11, 3.16 | Principal em 3.7, 3.11 |
| `/discovery` | 3.16 | Principal |
| `/interview-synthesis` | 3.7, 3.11 | Principal em ambas |
| `/competitive-analysis` | 3.10, 3.17 | Principal em 3.10 |
| `/opportunity-tree` | 3.11, 3.16 | Principal em ambas |
| `/hypothesis` | 3.7, 3.8, 3.11, 3.16 | Principal em 3.8, 3.16 |
| `/customer-journey` | 3.11, 3.16 | Complementar |
| `/prd` | 3.8 | Principal |
| `/user-stories` | 3.9 | Principal |
| `/acceptance-criteria` | 3.9 | Principal |
| `/prioritize` | 3.7, 3.9, 3.12 | Principal em 3.12 |
| `/strategy` | 3.17, 3.18 | Principal em 3.17 |
| `/roadmap` | 3.12, 3.17, 3.18 | Principal em 3.17 |
| `/okr` | 3.12, 3.13, 3.17, 3.18 | Principal em 3.12, 3.17 |
| `/lean-canvas` | 3.8, 3.16, 3.17 | Complementar |
| `/pricing` | 3.10, 3.15, 3.17 | Complementar |
| `/north-star` | 3.12, 3.13, 3.17, 3.18 | Principal em 3.13 |
| `/experiment-design` | 3.13, 3.16 | Principal em 3.16 |
| `/measure-pmf` | 3.13, 3.18 | Principal em 3.18 |
| `/ab-test-analysis` | 3.13 | Complementar |
| `/pre-mortem` | 3.8 | Complementar |
| `/launch-checklist` | 3.14, 3.15 | Complementar |
| `/release-notes` | 3.14, 3.18 | Principal em 3.14 |
| `/stakeholder-update` | 3.14, 3.18 | Principal em ambas |
| `/gtm` | 3.14, 3.15 | Principal em 3.15 |
| `/battlecard` | 3.10, 3.15 | Principal em 3.10 |
| `/ideal-customer-profile` | 3.10, 3.15 | Principal em 3.15 |

**Todas as 27 skills aparecem em pelo menos 1 aula. 24 aparecem como skill principal em pelo menos 1 aula.**

---

## Dica Final para o Aluno

O poder deste sistema não está em usar UMA skill isolada — está em **encadear skills** onde o output de uma vira input da próxima. Comece pela aula que mais se conecta com seu trabalho atual, execute o workflow completo, e observe como cada artefato alimenta o próximo.

Quando dominar os workflows individuais, combine aulas. Exemplo: faça 3.16 (Discovery) → 3.8 (PRD) → 3.9 (Stories) → 3.15 (GTM) para executar um ciclo completo de produto.
