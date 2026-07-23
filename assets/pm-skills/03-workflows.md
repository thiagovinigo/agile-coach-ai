# Workflows Prontos — PM Assistant

7 receitas prontas para cenários reais de Product Management. Cada workflow encadeia skills na ordem certa, com input e output definidos para cada etapa.

---

## 1. Customer Discovery

**Entender o problema antes de construir qualquer coisa**

**Quando usar:** Está começando do zero — novo produto, nova feature grande, ou pivot. Precisa entender profundamente o problema antes de investir em solução.

### Sequência

```
/persona → /discovery → /interview-synthesis → /opportunity-tree
```

| Etapa | Skill | Recebe | Entrega |
|-------|-------|--------|---------|
| 1 | `/persona` | Descrição do público-alvo e contexto do produto | Persona detalhada com JTBD, dores, ganhos e comportamentos |
| 2 | `/discovery` | Persona + problema que quer investigar | Plano de discovery com hipóteses, perguntas e métodos |
| 3 | `/interview-synthesis` | Notas de entrevistas realizadas | Padrões, insights-chave e recomendações |
| 4 | `/opportunity-tree` | Insights do discovery + objetivo de produto | Árvore com oportunidades priorizadas e soluções mapeadas |

### Exemplo prático

```
── Etapa 1 ──
/persona
Contexto: App de controle financeiro pessoal para jovens de 22-30 anos
que estão no primeiro emprego e nunca tiveram educação financeira formal.
→ Output: Persona "Lucas, 25 anos, analista júnior, salário de R$3.500..."

── Etapa 2 ──
/discovery
Contexto: [cola a persona gerada]
Problema: 60% dos usuários criam conta mas não registram
nenhuma transação na primeira semana.
→ Output: Plano de discovery com 5 hipóteses e roteiro de entrevista

── Etapa 3 ──
/interview-synthesis
Contexto: [cola notas das 8 entrevistas realizadas]
→ Output: 3 padrões principais, 7 insights, 4 recomendações

── Etapa 4 ──
/opportunity-tree
Contexto: [cola insights da síntese]
Objetivo: Aumentar ativação (primeira transação em 7 dias) de 40% para 70%.
→ Output: Árvore com 3 oportunidades e 9 soluções candidatas priorizadas
```

---

## 2. Feature Kickoff

**Especificar feature para engenharia**

**Quando usar:** Hipótese validada, decisão tomada de construir. Precisa transformar o aprendizado em especificação que eng consegue executar.

### Sequência

```
/hypothesis → /prd → /user-stories → /acceptance-criteria
```

| Etapa | Skill | Recebe | Entrega |
|-------|-------|--------|---------|
| 1 | `/hypothesis` | Achados de discovery ou intuição de produto | Hipótese estruturada: Se X, então Y, medido por Z |
| 2 | `/prd` | Hipótese + contexto do produto | PRD completo com problema, solução, escopo e métricas |
| 3 | `/user-stories` | PRD validado | User stories priorizadas com critérios de aceite |
| 4 | `/acceptance-criteria` | User story específica | Critérios detalhados com cenários e edge cases |

### Exemplo prático

```
── Etapa 1 ──
/hypothesis
Contexto: Discovery mostrou que usuários querem registrar gastos
mas esquecem. Notificações push no horário do almoço tiveram
80% de abertura nos testes.
→ Output: "Se enviarmos lembretes contextuais às 12h, então
   a taxa de registro diário aumentará de 15% para 40%,
   medido por % de DAU que registra ao menos 1 transação"

── Etapa 2 ──
/prd
Contexto: [cola hipótese + dados de discovery]
Produto: App de finanças pessoais, 50k MAU, mobile-first.
→ Output: PRD com escopo (MVP de notificações), métricas
   de sucesso, riscos e timeline sugerida

── Etapa 3 ──
/user-stories
Contexto: [cola o PRD]
→ Output: 6 user stories priorizadas (P0, P1, P2)

── Etapa 4 ──
/acceptance-criteria
Contexto: [cola a user story P0 — "Como usuário, quero receber
um lembrete para registrar meus gastos do almoço"]
→ Output: 8 critérios de aceite com happy path, edge cases
   e cenários de erro
```

---

## 3. Product Strategy

**Planejar trimestre e alinhar direção**

**Quando usar:** Início de trimestre (ou ciclo). Precisa analisar o cenário, definir direção, alinhar metas e comunicar o plano para time e stakeholders.

### Sequência

```
/competitive-analysis → /strategy → /okr → /roadmap → /stakeholder-update
```

| Etapa | Skill | Recebe | Entrega |
|-------|-------|--------|---------|
| 1 | `/competitive-analysis` | Produto + lista de concorrentes | Análise com posicionamento, gaps e oportunidades |
| 2 | `/strategy` | Análise competitiva + contexto de negócio | Estratégia com visão, positioning, moats e bets |
| 3 | `/okr` | Estratégia definida | OKRs do trimestre com objetivos e key results |
| 4 | `/roadmap` | OKRs + backlog de oportunidades | Roadmap orientado a outcomes por horizonte |
| 5 | `/stakeholder-update` | Estratégia + OKRs + roadmap | Apresentação executiva pronta para stakeholders |

### Exemplo prático

```
── Etapa 1 ──
/competitive-analysis
Contexto: App de finanças pessoais. Concorrentes: Mobills, Organizze,
Guiabolso. Nosso diferencial é foco em jovens e gamificação.
→ Output: Matriz competitiva, gaps no mercado, oportunidades únicas

── Etapa 2 ──
/strategy
Contexto: [cola análise competitiva]
Momento: Temos 50k MAU, Series A fechada, 18 meses de runway.
→ Output: Estratégia Q3 — foco em retenção e monetização,
   positioning "o app que ensina finanças sem parecer aula"

── Etapa 3 ──
/okr
Contexto: [cola estratégia]
Time: 1 PM, 4 devs, 1 designer. Ciclo de 3 meses.
→ Output: 2 objetivos, 6 key results mensuráveis

── Etapa 4 ──
/roadmap
Contexto: [cola OKRs + lista de oportunidades do backlog]
→ Output: Roadmap Now/Next/Later com outcomes, não features

── Etapa 5 ──
/stakeholder-update
Contexto: [cola estratégia + OKRs + roadmap]
Audiência: CEO e board de investidores.
→ Output: Update executivo de 1 página com progresso,
   plano, riscos e asks
```

---

## 4. Validate & Launch

**Testar antes e preparar lançamento**

**Quando usar:** Feature construída (ou quase). Precisa validar com experimento, antecipar riscos e preparar um lançamento sem surpresas.

### Sequência

```
/experiment-design → /pre-mortem → /launch-checklist → /gtm
```

| Etapa | Skill | Recebe | Entrega |
|-------|-------|--------|---------|
| 1 | `/experiment-design` | Feature + hipótese + métrica principal | Experimento com setup, amostra, duração e critério de sucesso |
| 2 | `/pre-mortem` | Feature + contexto de lançamento | Lista de riscos com probabilidade, impacto e mitigações |
| 3 | `/launch-checklist` | Feature + riscos mapeados | Checklist por área (eng, marketing, CS, legal) |
| 4 | `/gtm` | Feature + público + positioning | Plano de GTM com canais, messaging e timeline |

### Exemplo prático

```
── Etapa 1 ──
/experiment-design
Contexto: Vamos lançar gamificação (streaks + badges) para
aumentar retenção D7. Hipótese: streaks aumentam D7 de 35% para 50%.
→ Output: A/B test com 5k usuários por grupo, 14 dias,
   significância de 95%, critério: +10pp em D7

── Etapa 2 ──
/pre-mortem
Contexto: [cola design do experimento + feature de gamificação]
Lançamento previsto para 3 semanas.
→ Output: 12 riscos mapeados, top 3: push notification fatigue,
   edge case de timezone, badge desbloqueado sem ação real

── Etapa 3 ──
/launch-checklist
Contexto: [cola riscos + contexto da feature]
→ Output: 28 itens de checklist em 6 categorias,
   responsáveis e deadlines sugeridos

── Etapa 4 ──
/gtm
Contexto: [cola tudo anterior]
Canais disponíveis: in-app, push, email, Instagram, blog.
→ Output: Plano de GTM com messaging por canal,
   timeline de 2 semanas e métricas de acompanhamento
```

---

## 5. Pricing & GTM

**Monetizar e posicionar o produto**

**Quando usar:** Produto validado (tem PMF ou forte indicação). Precisa definir como cobrar, pra quem vender e como posicionar contra concorrentes.

### Sequência

```
/pricing → /ideal-customer-profile → /battlecard → /gtm
```

| Etapa | Skill | Recebe | Entrega |
|-------|-------|--------|---------|
| 1 | `/pricing` | Produto + mercado + custos + willingness-to-pay | Estratégia de pricing com tiers, preços e justificativa |
| 2 | `/ideal-customer-profile` | Pricing + dados de clientes atuais | ICP detalhado com firmographics e sinais de compra |
| 3 | `/battlecard` | ICP + concorrentes + diferencial | Battlecard de vendas com objeções e contra-argumentos |
| 4 | `/gtm` | ICP + pricing + battlecard | Plano de GTM completo com canais e messaging |

### Exemplo prático

```
── Etapa 1 ──
/pricing
Contexto: App de finanças pessoais. Hoje é 100% grátis com 50k MAU.
Custo por usuário: R$0,80/mês. Pesquisa mostrou willingness-to-pay
de R$9-15/mês para features premium.
→ Output: Modelo freemium com 3 tiers (Free, Plus R$12,90,
   Family R$19,90), feature matrix e projeção de conversão

── Etapa 2 ──
/ideal-customer-profile
Contexto: [cola pricing + dados de uso]
Nossos power users: 25-32 anos, renda R$4-8k, usam app 5x/semana.
→ Output: ICP primário e secundário com demographics,
   comportamentos e sinais de compra

── Etapa 3 ──
/battlecard
Contexto: [cola ICP]
Concorrentes: Mobills (R$17,90/mês), Organizze (R$8,90/mês).
Nosso diferencial: gamificação + conteúdo educacional integrado.
→ Output: Battlecard com comparativo, objeções comuns
   e scripts de resposta

── Etapa 4 ──
/gtm
Contexto: [cola pricing + ICP + battlecard]
Budget de marketing: R$15k/mês. Canais atuais: orgânico + Instagram.
→ Output: Plano de GTM de 90 dias com canais priorizados,
   messaging por ICP e métricas de acompanhamento
```

---

## 6. Growth Sprint

**Construir motor de crescimento**

**Quando usar:** Produto com PMF confirmado. Precisa sair do crescimento orgânico e construir um sistema previsível de aquisição, ativação e retenção.

### Sequência

```
/north-star → /experiment-design → /ab-test-analysis → /okr
```

| Etapa | Skill | Recebe | Entrega |
|-------|-------|--------|---------|
| 1 | `/north-star` | Produto + métricas atuais + modelo de negócio | North Star Metric + input metrics + leading indicators |
| 2 | `/experiment-design` | North Star + lever que quer mover | Experimento focado na métrica com setup completo |
| 3 | `/ab-test-analysis` | Resultados do experimento | Análise com significância, lift e recomendação |
| 4 | `/okr` | Aprendizados + North Star | OKRs de growth para o próximo ciclo |

### Exemplo prático

```
── Etapa 1 ──
/north-star
Contexto: App de finanças pessoais. 50k MAU, 15k WAU,
retenção D30 de 25%. Modelo freemium, 3% de conversão para premium.
→ Output: North Star = "Transações registradas por semana por usuário ativo"
   Input metrics: ativação D1, frequência semanal, transações/sessão

── Etapa 2 ──
/experiment-design
Contexto: [cola North Star]
Lever: ativação D1 (hoje 45%, meta 65%).
Ideia: onboarding com primeira transação guiada em 60 segundos.
→ Output: Experimento com setup, grupo de controle,
   duração de 10 dias, critério de sucesso: +15pp em ativação D1

── Etapa 3 ──
/ab-test-analysis
Contexto: Resultados do teste de onboarding:
- Controle: 44% ativação D1 (n=3.200)
- Variante: 61% ativação D1 (n=3.150)
- D7 retention: controle 32%, variante 41%
→ Output: Teste significativo (p<0.01), lift de +17pp,
   recomendação: ship para 100% + iterar

── Etapa 4 ──
/okr
Contexto: [cola North Star + resultado do experimento]
Próximo trimestre, time de growth (1 PM, 2 devs, 1 analyst).
→ Output: OKRs focados em escalar o que funcionou
   + próximas alavancas de crescimento
```

---

## 7. Board/Exec Update

**Comunicar progresso com evidências**

**Quando usar:** Reunião com board, investidores ou C-level. Precisa mostrar onde o produto está, com dados concretos, e o plano para frente.

### Sequência

```
/measure-pmf → /stakeholder-update → /roadmap
```

| Etapa | Skill | Recebe | Entrega |
|-------|-------|--------|---------|
| 1 | `/measure-pmf` | Métricas do produto + dados de uso/retenção | Avaliação de PMF com score, evidências e gaps |
| 2 | `/stakeholder-update` | PMF assessment + progresso do trimestre | Update executivo com highlights, riscos e asks |
| 3 | `/roadmap` | Direção estratégica + feedback do update | Roadmap atualizado para apresentar na reunião |

### Exemplo prático

```
── Etapa 1 ──
/measure-pmf
Contexto: App de finanças pessoais, 8 meses no mercado.
- 50k MAU, crescimento de 12% MoM
- Sean Ellis survey: 38% "very disappointed" se produto sumisse
- D30 retention: 25%, D90: 14%
- NPS: 42
- Cohort de premium: D90 retention de 68%
→ Output: PMF parcial — forte em nicho premium,
   fraco em base free. Score: 6/10. Gaps e recomendações.

── Etapa 2 ──
/stakeholder-update
Contexto: [cola PMF assessment]
Progresso Q2: lançamos gamificação (+8pp retenção),
pricing (3% conversão), onboarding novo (ativação de 45% → 61%).
Riscos: runway de 14 meses, CAC subindo.
→ Output: Update de 1 página com métricas-chave, wins,
   riscos e 2 asks (budget de marketing + contratação)

── Etapa 3 ──
/roadmap
Contexto: [cola update + feedback esperado do board]
Direção: dobrar aposta em premium + expandir para casal/família.
→ Output: Roadmap Q3-Q4 com 3 bets principais,
   outcomes esperados e milestones
```

---

## Dicas para Todos os Workflows

1. **Salve cada output em arquivo separado** — facilita colar como contexto na próxima skill
2. **Use `Refine:` entre etapas** — ajuste o output antes de passar para a próxima skill
3. **Adapte a sequência** — pule etapas que não fazem sentido para seu contexto
4. **Combine workflows** — ex: comece com Customer Discovery e termine com Feature Kickoff
5. **Mantenha consistência de contexto** — use o mesmo produto/cenário ao longo de todo o workflow

---

## Navegação

- [Voltar ao Quick Start](00-como-usar.md)
- [Do Zero ao Um](01-zero-a-um.md)
- [Do Um ao Cem](02-um-a-cem.md)
