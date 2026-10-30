# /experiment-design

## O que essa skill faz

Desenha experimentos Lean para validar hipóteses de produto usando pretotyping (pré-MVP) ou A/B testing (pós-launch). Baseado no framework de Alberto Savoia ("The Right It") e princípios de Lean Experimentation.

Saída: **Experiment Spec** com hipótese XYZ, método, métricas, timeline e critérios go/no-go.

---

## Quando usar

- Antes de construir: validar se a ideia merece investimento (pretotype)
- Pós-launch: otimizar conversão, retenção ou engajamento (A/B test)
- Quando tem opinião forte mas dados fracos sobre demanda
- Quando stakeholder pede "prova" antes de aprovar investimento
- Quando precisa decidir entre duas abordagens de feature

---

## Input esperado

**Mínimo:**
- **Hipótese**: O que você acredita ser verdade sobre o mercado/usuário
- **Estágio**: Pré-MVP (0→1) ou pós-launch (1→100)
- **Contexto**: Produto, segmento, situação atual

**Opcional:**
- Dados existentes (surveys, analytics, feedback)
- Restrições de budget/timeline
- Métricas atuais (baseline para A/B)
- Tamanho da base de usuários

---

## Formato de hipótese XYZ

Toda hipótese deve seguir o formato XYZ de Alberto Savoia:

> "Pelo menos **X%** de **Y** vai **Z**"

- **X%** = porcentagem mínima do mercado-alvo (ex: 10%, 30%)
- **Y** = mercado-alvo específico (ex: "PMs de startups Series A")
- **Z** = como vão se engajar (ex: "se cadastrar na waitlist em 48h")

### Exemplos de hipótese XYZ

- "Pelo menos 15% dos PMs que visitarem a landing page vão deixar email na waitlist"
- "Pelo menos 5% dos leads do email campaign vão fazer pre-order"
- "Pelo menos 40% dos usuários expostos ao novo onboarding vão completar o setup em 24h"

---

## Princípios fundamentais (Savoia)

### 1. Skin-in-the-Game
Teste comprometimento REAL — tempo, dinheiro, ação — não apenas interesse declarado.

- RUIM: "Você usaria isso?" (opinião)
- BOM: "Coloque seu email para ser avisado" (ação leve)
- ÓTIMO: "Pague R$10 para garantir acesso antecipado" (comprometimento real)

### 2. YODA (Your Own Data)
Colete seus próprios dados. Não confie em pesquisas de mercado genéricas, benchmarks de terceiros ou "achismos" de stakeholders.

### 3. Comportamento > Opinião
Meça o que as pessoas FAZEM, não o que DIZEM que fariam. O gap entre intenção e ação é enorme.

---

## Tipos de experimento

### A) Pretotypes (validação pré-MVP)

Use quando: produto ainda não existe ou feature é completamente nova.

| Tipo | Descrição | Skin-in-the-Game | Tempo | Custo |
|------|-----------|-------------------|-------|-------|
| **Landing Page** | Página descrevendo o produto + CTA (waitlist/email) | Email = baixo; Pre-order = alto | 1-2 semanas | Baixo |
| **Explainer Video** | Vídeo demonstrando o conceito + CTA | Tempo assistindo + CTA | 1-2 semanas | Médio |
| **Email Campaign** | Email para segmento-alvo medindo interesse real | Cliques, respostas, pre-orders | 3-5 dias | Baixo |
| **Pre-Order / Waitlist** | Coletar pagamento ou compromisso antes de construir | Dinheiro = máximo | 1-3 semanas | Baixo |
| **Concierge / Manual MVP** | Entregar o serviço manualmente para poucos usuários | Tempo do usuário + pagamento | 2-4 semanas | Médio |

### B) A/B Tests (otimização pós-launch)

Use quando: produto existe e quer otimizar métricas específicas.

| Elemento | Descrição |
|----------|-----------|
| **Hipótese** | O que muda e por que espera impacto |
| **Sample size** | Calculado com base em MDE (Minimum Detectable Effect) |
| **Duração** | Mínimo 1-2 ciclos de negócio completos |
| **Split** | Geralmente 50/50; pode ser 90/10 para testes de risco |
| **Primary metric** | UMA métrica principal de sucesso |
| **Guardrail metrics** | Métricas que NÃO podem degradar |
| **Success criteria** | Threshold de significância (geralmente p < 0.05) |

---

## Processo de design do experimento

### Passo 1 — Formular hipótese XYZ
Transformar a crença em hipótese testável com número concreto.

### Passo 2 — Identificar o risco principal
Qual é a suposição mais arriscada? Geralmente é uma dessas:
- **Desejabilidade**: As pessoas querem isso?
- **Viabilidade**: Conseguimos construir?
- **Usabilidade**: As pessoas conseguem usar?
- **Viabilidade financeira**: O modelo de negócio fecha?

### Passo 3 — Escolher tipo de experimento
- Risco de desejabilidade (0→1) → Pretotype
- Risco de otimização (1→100) → A/B Test
- Risco de usabilidade → Concierge / Prototype test

### Passo 4 — Desenhar o experimento

```
EXPERIMENT SPEC
═══════════════════════════════════════════════════

Hipótese XYZ:
"Pelo menos [X%] de [Y] vai [Z]"

Tipo de experimento: [Landing Page / A/B Test / etc.]

Método:
- O que será criado/modificado
- Como será distribuído
- Para quem será mostrado

Amostra:
- Tamanho necessário: [N]
- Como será recrutada
- Critérios de inclusão/exclusão

Timeline:
- Setup: [X dias]
- Coleta de dados: [X dias/semanas]
- Análise: [X dias]

Métrica primária:
- [Nome da métrica]: [como será medida]
- Baseline atual: [valor ou "desconhecido"]

Métricas guardrail:
- [Métrica 1]: não pode cair abaixo de [valor]
- [Métrica 2]: não pode cair abaixo de [valor]
```

### Passo 5 — Definir threshold de sucesso

```
CRITÉRIOS DE DECISÃO
═══════════════════════════════════════════════════

✅ GO (validado):
   [Métrica] >= [X%] com [condições]

⚠️ INVESTIGAR:
   [Métrica] entre [X%] e [Y%] — precisa de mais dados

❌ NO-GO (invalidado):
   [Métrica] < [Y%] após [período completo]

🔄 PIVOT:
   Se NO-GO, considerar: [alternativas]
```

### Passo 6 — Definir kill criteria
Quando parar o experimento antes do prazo:
- Resultados negativos significativos antes do prazo
- Problemas técnicos comprometendo dados
- Mudança de contexto que invalida o teste

### Passo 7 — Planejar análise
- Quem analisa os dados
- Que ferramenta será usada
- Como resultados serão comunicados a stakeholders
- Próximos passos para cada cenário (go/no-go/pivot)

---

## Template de output

```
╔══════════════════════════════════════════════════════════╗
║              EXPERIMENT DESIGN SPEC                      ║
╠══════════════════════════════════════════════════════════╣

📋 CONTEXTO
Produto: [nome]
Estágio: [Pré-MVP / Growth / Mature]
Risco principal: [Desejabilidade / Viabilidade / Usabilidade]

🎯 HIPÓTESE XYZ
"Pelo menos [X%] de [Y] vai [Z]"

Suposição mais arriscada:
[descrição da suposição]

🧪 DESIGN DO EXPERIMENTO
Tipo: [Pretotype / A/B Test]
Método: [descrição do método]
Amostra: [tamanho e critérios]
Timeline: [duração total]
Budget estimado: [R$ / horas]

📊 MÉTRICAS
Primary: [métrica + como medir]
Guardrails: [métricas que não podem degradar]
Baseline: [valores atuais se disponíveis]

✅ CRITÉRIOS DE DECISÃO
GO: [condição]
NO-GO: [condição]
PIVOT: [alternativas]

📅 CRONOGRAMA
Semana 1: [atividade]
Semana 2: [atividade]
Semana N: [análise e decisão]

⚠️ RISCOS DO EXPERIMENTO
- [Risco 1]: [mitigação]
- [Risco 2]: [mitigação]

╚══════════════════════════════════════════════════════════╝
```

---

## Exemplo de uso

**Input:**
> /experiment-design Validar demanda para ferramenta de AI meeting notes para PMs. Ainda não temos produto, só a ideia.

**Output esperado:**
- Hipótese XYZ: "Pelo menos 12% dos PMs de startups que visitarem a landing page vão se cadastrar na waitlist em 7 dias"
- Tipo: Landing Page Pretotype
- Método: Landing page com proposta de valor + campo de email
- Tráfego: LinkedIn ads para PMs + posts em comunidades
- Métrica: Taxa de conversão visitante → email cadastrado
- GO: >= 12% conversão
- NO-GO: < 5% conversão após 500 visitantes
- Timeline: 2 semanas (3 dias setup + 10 dias coleta + 1 dia análise)

---

## Referências

- Alberto Savoia — "The Right It" (pretotyping framework)
- Eric Ries — "The Lean Startup" (Build-Measure-Learn)
- Teresa Torres — "Continuous Discovery Habits" (assumption testing)
- Itamar Gilad — GIST Framework (Goals, Ideas, Steps, Tasks)

---

## Checklist antes de lançar experimento

- [ ] Hipótese está no formato XYZ com número concreto
- [ ] Risco principal foi identificado
- [ ] Tipo de experimento é adequado ao estágio
- [ ] Sample size é suficiente para conclusões
- [ ] Timeline cobre pelo menos 1 ciclo de negócio
- [ ] Critérios go/no-go estão definidos ANTES de ver dados
- [ ] Stakeholders alinhados com critérios de decisão
- [ ] Kill criteria definidos
- [ ] Plano de análise e próximos passos documentados

$ARGUMENTS
