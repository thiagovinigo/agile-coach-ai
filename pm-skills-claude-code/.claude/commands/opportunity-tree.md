# /opportunity-tree

## O que essa skill faz

Gera uma Opportunity Solution Tree (OST) completa seguindo o framework de Teresa Torres (Continuous Discovery Habits). Estrutura o pensamento de discovery em 4 níveis: Outcome → Opportunities → Solutions → Experiments.

Saída: **Árvore de oportunidades** com scores, soluções comparadas e experimentos desenhados — pronta para alinhar o Product Trio.

---

## Quando usar

- Tem um outcome claro mas não sabe por onde começar
- Quer priorizar oportunidades com base em dados, não intuição
- Precisa gerar múltiplas soluções antes de se comprometer com uma
- Quer alinhar PM, Designer e Tech Lead sobre o que explorar primeiro
- Está preso no modo "feature factory" e quer voltar para discovery

---

## Input esperado

**Mínimo:**
- **Desired Outcome**: Métrica específica que quer mover (ex: "Aumentar retenção de 7 dias de 30% para 50%")
- **Contexto do produto**: O que é o produto, quem usa
- **Dados disponíveis**: Que pesquisas, entrevistas ou analytics existem

**Opcional:**
- Trechos de entrevistas com usuários
- Dados de analytics (funil, retenção, comportamento)
- Oportunidades já identificadas
- Constraints (budget, timeline, capacidade do time)
- Personas definidas

---

## Processo

1. **Definir UM outcome** — Escolher uma única métrica mensurável com baseline e target. Não tente resolver tudo ao mesmo tempo. Ex: "Aumentar 7-day retention de 30% para 50%." Se o input tiver múltiplos outcomes, pedir para priorizar.

2. **Identificar 4-6 oportunidades** — Extrair de pesquisa com usuários (entrevistas, surveys, analytics). Cada oportunidade deve ser um problema ou necessidade do cliente, NUNCA uma feature. Usar framing centrado no usuário: "Eu luto para..." ou "Eu gostaria de poder...". Se não houver dados, marcar como hipótese.

3. **Scorer oportunidades** — Para cada oportunidade, avaliar:
   - **Importância** (1-5): Quanto isso importa para o usuário?
   - **Satisfação** (1-5): Quão bem resolvido está hoje?
   - **Score** = Importância × (1 − Satisfação/5)
   - Priorizar as 2-3 com maior score.

4. **Brainstormar 3+ soluções por oportunidade** — Para cada oportunidade top, gerar mínimo 3 soluções diferentes. Envolver perspectivas de PM, Design e Eng. Soluções podem variar de simples (copy change) a complexas (nova feature). O ponto é comparar e contrastar.

5. **Identificar assumption mais arriscada** — Para cada solução, perguntar: qual assumption, se falsa, invalida tudo? Categorizar em: Value (usuário quer?), Usability (consegue usar?), Viability (negócio sustenta?), Feasibility (eng consegue construir?).

6. **Desenhar experimento por assumption** — Para cada assumption, definir teste leve: protótipo, fake door, survey, concierge, etc. Incluir: método, tamanho de amostra, critério de sucesso, timeline.

7. **Priorizar branch** — Decidir qual ramo da árvore testar primeiro. Critério: maior impacto potencial no outcome × menor custo de experimento.

---

## Output

```markdown
# Opportunity Solution Tree

## Desired Outcome
**Métrica:** [Nome da métrica]
**Baseline:** [Valor atual]
**Target:** [Valor desejado]
**Timeframe:** [Prazo]
**Owner:** [Product Trio responsável]

---

## Árvore

```
[Outcome: Métrica de X% para Y%]
├── Oportunidade 1: [Descrição centrada no usuário] (Score: X.X)
│   ├── Solução A: [Descrição]
│   │   └── Experimento: [Tipo de teste]
│   ├── Solução B: [Descrição]
│   │   └── Experimento: [Tipo de teste]
│   └── Solução C: [Descrição]
│       └── Experimento: [Tipo de teste]
├── Oportunidade 2: [Descrição] (Score: X.X)
│   ├── Solução A: [Descrição]
│   │   └── Experimento: [Tipo de teste]
│   ├── Solução B: [Descrição]
│   └── Solução C: [Descrição]
├── Oportunidade 3: [Descrição] (Score: X.X)
│   └── (explorar após validar Opp 1 e 2)
└── Oportunidade 4: [Descrição] (Score: X.X)
    └── (backlog de discovery)
```

---

## Oportunidades — Detalhe e Scoring

### Oportunidade 1: [Nome]
**Framing:** "[Eu luto para... / Eu gostaria de poder...]"
**Evidência:** [Fonte: entrevista, analytics, survey]
**Importância:** [1-5] | **Satisfação atual:** [1-5]
**Score:** Importância × (1 − Satisfação/5) = [X.X]

### Oportunidade 2: [Nome]
**Framing:** "[Framing centrado no usuário]"
**Evidência:** [Fonte]
**Importância:** [1-5] | **Satisfação atual:** [1-5]
**Score:** [X.X]

### Oportunidade 3: [Nome]
**Framing:** "[Framing centrado no usuário]"
**Evidência:** [Fonte]
**Importância:** [1-5] | **Satisfação atual:** [1-5]
**Score:** [X.X]

*(Repetir para todas as oportunidades)*

---

## Ranking de Oportunidades

| # | Oportunidade | Importância | Satisfação | Score | Status |
|---|-------------|-------------|------------|-------|--------|
| 1 | [Nome] | [1-5] | [1-5] | [X.X] | 🔍 Explorando |
| 2 | [Nome] | [1-5] | [1-5] | [X.X] | 🔍 Explorando |
| 3 | [Nome] | [1-5] | [1-5] | [X.X] | ⏸️ Backlog |
| 4 | [Nome] | [1-5] | [1-5] | [X.X] | ⏸️ Backlog |

---

## Soluções — Top Oportunidades

### Para Oportunidade 1: [Nome]

| Solução | Descrição | Esforço | Impacto Esperado | Risco Principal |
|---------|-----------|---------|-------------------|-----------------|
| A | [Descrição] | [Baixo/Médio/Alto] | [Estimativa] | [Tipo de risco] |
| B | [Descrição] | [Baixo/Médio/Alto] | [Estimativa] | [Tipo de risco] |
| C | [Descrição] | [Baixo/Médio/Alto] | [Estimativa] | [Tipo de risco] |

### Para Oportunidade 2: [Nome]

| Solução | Descrição | Esforço | Impacto Esperado | Risco Principal |
|---------|-----------|---------|-------------------|-----------------|
| A | [Descrição] | [Baixo/Médio/Alto] | [Estimativa] | [Tipo de risco] |
| B | [Descrição] | [Baixo/Médio/Alto] | [Estimativa] | [Tipo de risco] |
| C | [Descrição] | [Baixo/Médio/Alto] | [Estimativa] | [Tipo de risco] |

---

## Experimentos

### Experimento 1: [Nome do teste]
**Solução testada:** [Qual solução]
**Assumption:** [O que estamos testando]
**Categoria:** [Value / Usability / Viability / Feasibility]
**Método:** [Protótipo / Fake door / Survey / Concierge / A-B test / etc.]
**Amostra:** [Tamanho e segmento]
**Critério de sucesso:** [Métrica ≥ X]
**Timeline:** [X dias/semanas]
**Custo estimado:** [Horas de esforço]

### Experimento 2: [Nome do teste]
**Solução testada:** [Qual solução]
**Assumption:** [O que estamos testando]
**Categoria:** [Value / Usability / Viability / Feasibility]
**Método:** [Método]
**Amostra:** [Tamanho]
**Critério de sucesso:** [Métrica ≥ X]
**Timeline:** [X dias/semanas]

---

## Priorização: Próximo Passo

**Branch priorizado:** [Oportunidade X → Solução Y → Experimento Z]
**Razão:** [Maior impacto potencial / Menor custo de teste / Evidência mais forte]
**Ação imediata:** [O que fazer esta semana]
```

---

## Exemplo

**Input:**
> Produto: CRM B2B SaaS para times de vendas mid-market. Outcome: Aumentar 7-day retention de 30% para 50%. Temos dados de 12 entrevistas com novos usuários e analytics de funil de onboarding.

**Output:**

```markdown
# Opportunity Solution Tree

## Desired Outcome
**Métrica:** 7-day retention (% de usuários ativos no dia 7 após signup)
**Baseline:** 30%
**Target:** 50%
**Timeframe:** Q3 2026
**Owner:** Squad Onboarding (PM: Rafael, Design: Ana, Tech Lead: Carlos)

---

## Árvore

```
[Outcome: 7-day retention de 30% → 50%]
├── Opp 1: "Não sei por onde começar quando abro o CRM pela primeira vez" (Score: 4.2)
│   ├── Sol A: Onboarding interativo com checklist guiado
│   │   └── Exp: Protótipo Figma + teste com 8 novos reps
│   ├── Sol B: Template pré-configurado por indústria
│   │   └── Exp: Fake door test (botão no signup)
│   └── Sol C: Video walkthrough de 3 minutos na home
│       └── Exp: A/B test com 200 novos signups
├── Opp 2: "Importar meus dados do CRM anterior é muito doloroso" (Score: 3.6)
│   ├── Sol A: Importação guiada com mapeamento automático
│   │   └── Exp: Concierge (importar manualmente para 10 clientes)
│   ├── Sol B: Integração nativa com top 3 CRMs (Salesforce, HubSpot, Pipedrive)
│   │   └── Exp: Survey para validar quais CRMs priorizar
│   └── Sol C: "Start fresh" mode com dados de exemplo
│       └── Exp: Protótipo + teste com 5 reps
├── Opp 3: "Não consigo ver valor rápido — leva dias para ter dados úteis" (Score: 3.2)
│   └── (explorar após validar Opp 1 e 2)
├── Opp 4: "O CRM não se parece com o que eu já usava" (Score: 2.4)
│   └── (backlog de discovery)
└── Opp 5: "Meu gestor não acompanha se estou usando" (Score: 1.8)
    └── (backlog — low priority)
```

---

## Oportunidades — Detalhe e Scoring

### Oportunidade 1: Paralisia no primeiro acesso
**Framing:** "Eu luto para entender o que fazer primeiro quando abro o CRM. Tem muita opção e nenhum guia."
**Evidência:** 9 de 12 entrevistados mencionaram confusão no primeiro acesso. Analytics: 45% dos novos usuários não completam nenhuma ação no dia 1.
**Importância:** 5 | **Satisfação atual:** 1
**Score:** 5 × (1 − 1/5) = **4.0**

### Oportunidade 2: Dor na migração de dados
**Framing:** "Eu gostaria de poder trazer meus dados do CRM anterior sem perder informação ou gastar um dia inteiro configurando."
**Evidência:** 7 de 12 entrevistados citaram migração como barreira. Analytics: apenas 18% completam importação no dia 1.
**Importância:** 4 | **Satisfação atual:** 1
**Score:** 4 × (1 − 1/5) = **3.2**

### Oportunidade 3: Time-to-value longo
**Framing:** "Eu não consigo ver valor rápido — leva dias até ter dados suficientes para o CRM ser útil."
**Evidência:** 5 de 12 mencionaram. Correlação: usuários que registram ≥5 deals no dia 1 têm 3x mais retenção.
**Importância:** 4 | **Satisfação atual:** 2
**Score:** 4 × (1 − 2/5) = **2.4**

### Oportunidade 4: Interface desconhecida
**Framing:** "O CRM não se parece com o que eu já usava, tenho que reaprender tudo."
**Evidência:** 3 de 12 mencionaram. Impacto menor — mais sobre curva de aprendizado que abandono.
**Importância:** 3 | **Satisfação atual:** 2
**Score:** 3 × (1 − 2/5) = **1.8**

---

## Ranking de Oportunidades

| # | Oportunidade | Importância | Satisfação | Score | Status |
|---|-------------|-------------|------------|-------|--------|
| 1 | Paralisia no primeiro acesso | 5 | 1 | 4.0 | Explorando |
| 2 | Dor na migração de dados | 4 | 1 | 3.2 | Explorando |
| 3 | Time-to-value longo | 4 | 2 | 2.4 | Backlog |
| 4 | Interface desconhecida | 3 | 2 | 1.8 | Backlog |

---

## Soluções — Top Oportunidades

### Para Opp 1: Paralisia no primeiro acesso

| Solução | Descrição | Esforço | Impacto Esperado | Risco Principal |
|---------|-----------|---------|-------------------|-----------------|
| A | Onboarding interativo: checklist de 5 passos que guia o rep a cadastrar primeiro deal, contato e atividade | Médio (2 sprints) | +15pp retenção | Usability — rep pode ignorar o checklist |
| B | Template por indústria: ao fazer signup, escolhe indústria e recebe pipeline, campos e automações pré-configurados | Alto (3 sprints) | +12pp retenção | Value — templates podem não refletir workflow real |
| C | Video walkthrough de 3 min na home: aparece no primeiro login, mostra os 3 passos essenciais | Baixo (3 dias) | +5pp retenção | Value — videos têm taxa de assistir completo baixa |

### Para Opp 2: Dor na migração de dados

| Solução | Descrição | Esforço | Impacto Esperado | Risco Principal |
|---------|-----------|---------|-------------------|-----------------|
| A | Importação guiada: wizard que mapeia campos automaticamente de CSV/Excel | Médio (2 sprints) | +10pp retenção | Feasibility — mapeamento automático de campos é difícil |
| B | Integração nativa com Salesforce, HubSpot, Pipedrive | Alto (4+ sprints) | +12pp retenção | Feasibility — manter 3 integrações é custoso |
| C | "Start fresh" mode: dados de exemplo realistas para testar antes de importar | Baixo (1 sprint) | +5pp retenção | Value — rep pode querer seus dados reais desde o início |

---

## Experimentos

### Experimento 1: Protótipo do Checklist de Onboarding
**Solução testada:** Opp 1 → Solução A
**Assumption:** Novos reps vão seguir um checklist guiado se ele aparecer no primeiro acesso (Value + Usability)
**Categoria:** Value + Usability
**Método:** Protótipo em Figma com 8 novos sales reps. Teste moderado de 30 min. Observar se completam os 5 passos e medir satisfação.
**Amostra:** 8 novos reps (mix de indústrias)
**Critério de sucesso:** ≥6 de 8 completam o checklist sem ajuda. Satisfação ≥4/5.
**Timeline:** 2 semanas (1 semana protótipo + 1 semana testes)
**Custo estimado:** 40h (Design: 20h, PM: 12h, Pesquisa: 8h)

### Experimento 2: Fake Door Test — Templates por Indústria
**Solução testada:** Opp 1 → Solução B
**Assumption:** Reps consideram templates por indústria úteis o suficiente para clicar e querer usar (Value)
**Categoria:** Value
**Método:** Adicionar opção "Usar template para [indústria]" no flow de signup. Medir CTR. Quem clica vai para waitlist com pergunta: "O que você espera que o template inclua?"
**Amostra:** 300 novos signups (split 50/50: com e sem opção)
**Critério de sucesso:** CTR ≥ 25% no grupo com opção
**Timeline:** 2 semanas
**Custo estimado:** 16h (Eng: 8h, PM: 4h, Análise: 4h)

### Experimento 3: Concierge de Importação
**Solução testada:** Opp 2 → Solução A
**Assumption:** Se fizermos a importação pelos clientes, eles retêm melhor (Value)
**Categoria:** Value + Feasibility
**Método:** Para os próximos 10 clientes novos, oferecer importação white-glove. Time de CS importa os dados manualmente. Medir retenção de 7 dias vs. controle.
**Amostra:** 10 clientes (vs. 10 controle)
**Critério de sucesso:** Retenção do grupo concierge ≥ 50% (vs. 30% baseline)
**Timeline:** 3 semanas
**Custo estimado:** 30h de CS

---

## Priorização: Próximo Passo

**Branch priorizado:** Opp 1 → Solução A → Experimento 1 (Protótipo do Checklist)
**Razão:** Maior score de oportunidade (4.0), evidência mais forte (9/12 entrevistas), experimento de menor custo (40h, sem código). Se validar, pode entregar quick win em 2 sprints.
**Ação imediata:** Designer começa protótipo do checklist na segunda. PM recruta 8 reps para teste na semana seguinte.

**Em paralelo:** Rodar Experimento 2 (Fake Door) que é low-effort e valida Solução B sem comprometer recursos.
```

---

## Dicas

- **Oportunidades NÃO são features.** "Adicionar dashboard" é solução. "Não consigo ver meu progresso" é oportunidade. Se a oportunidade descreve algo que você vai construir, está errado.
- **Mínimo 3 soluções por oportunidade.** Se só tem uma solução, você não está fazendo discovery — está fazendo delivery de uma ideia pré-definida. Force-se a comparar e contrastar.
- **Um outcome por vez.** Árvore com 3 outcomes vira bagunça. Foque em um, valide, depois passe para o próximo.
- **Discovery é contínua, não um evento.** A árvore evolui semanalmente. Experimentos falham, novos dados aparecem, oportunidades mudam de score. Trate como documento vivo.
