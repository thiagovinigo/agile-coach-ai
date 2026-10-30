# /measure-pmf

## O que essa skill faz

Avalia o grau de Product-Market Fit do seu produto usando frameworks quantitativos e qualitativos consolidados por 46 líderes de produto. Baseado no Sean Ellis Test, Superhuman PMF Engine e métricas de retenção.

Saída: **PMF Assessment Report** com score, estágio, evidências e plano de ação.

---

## Quando usar

- Após launch: "será que temos PMF?"
- Antes de escalar: validar se é hora de investir em growth
- Quando métricas estão ambíguas (crescimento + churn alto)
- Para convencer stakeholders com dados, não intuição
- Revisão periódica (PMF pode ser perdido)
- Antes de fundraising: provar tração

---

## Input esperado

**Mínimo:**
- **Produto**: O que é e para quem
- **Base de usuários**: Tamanho e tempo de uso
- **Dados disponíveis**: Quais métricas você tem acesso

**Opcional:**
- Resultados de Sean Ellis Survey (se já rodou)
- Curvas de retenção por cohort
- NPS score
- Unit economics (CAC, LTV)
- Taxa de crescimento orgânico
- Feedback qualitativo de usuários

---

## Princípios fundamentais

### 1. PMF é óbvio quando existe
> "Se você precisa perguntar se tem PMF, você não tem." — Eric Ries

Sinais claros de PMF:
- Demanda maior que capacidade de entrega
- Usuários reclamam quando produto fica fora do ar
- Crescimento orgânico forte (word of mouth)
- Clientes perguntam sobre pricing/timeline, não sobre features
- Time de vendas não consegue acompanhar inbound

### 2. PMF existe em segmentos
Você pode ter PMF forte com um segmento e zero com outro. Sempre segmente a análise.

### 3. PMF não é estático
PMF pode ser perdido por:
- Mudança de mercado
- Entrada de competitor superior
- Crescimento para segmentos sem fit
- Degradação de produto (tech debt, feature bloat)

### 4. PMF é multi-estágio
| Estágio | Descrição | Sean Ellis Score | Retenção |
|---------|-----------|------------------|----------|
| **Nascent** | Sinais iniciais, poucos usuários apaixonados | < 20% | Caindo |
| **Developing** | Segmento claro, mas ainda inconsistente | 20-39% | Estabilizando |
| **Strong** | Maioria dos usuários-alvo são retidos | 40-60% | Flat ou subindo |
| **Extreme** | Produto é indispensável, crescimento viral | > 60% | Smile curve |

---

## Métodos de medição

### 1. Sean Ellis Survey (quantitativo)

A pergunta central:

> "Como você se sentiria se não pudesse mais usar [produto]?"
> - Muito desapontado
> - Um pouco desapontado
> - Não me importaria
> - Não uso mais

**Threshold**: >= 40% "muito desapontado" = PMF

**Regras de aplicação:**
- Enviar apenas para usuários que usaram o produto pelo menos 2x
- Mínimo 40 respostas para significância
- Segmentar por persona/use case
- Incluir pergunta aberta: "Qual é o principal benefício que você recebe?"

### 2. Curvas de retenção

```
PADRÕES DE RETENÇÃO
═══════════════════════════════════════════════════

📉 Sem PMF: Curva cai continuamente, nunca estabiliza
   Mês 1: 40% → Mês 3: 15% → Mês 6: 3% → 0%

📊 PMF Developing: Curva estabiliza em nível baixo
   Mês 1: 40% → Mês 3: 20% → Mês 6: 15% → 15%

📈 PMF Strong: Curva estabiliza em nível saudável
   Mês 1: 60% → Mês 3: 45% → Mês 6: 40% → 40%

😊 PMF Extreme (Smile Curve): Retenção SOBE após queda inicial
   Mês 1: 50% → Mês 3: 35% → Mês 6: 40% → Mês 12: 50%
```

**Como analisar:**
- Plotar por cohort mensal
- Comparar cohorts recentes vs antigos (melhorando?)
- Segmentar por canal de aquisição
- Segmentar por persona

### 3. NPS + profundidade qualitativa

NPS sozinho não mede PMF, mas combinado com qualitativo ajuda.

- **Promoters (9-10)**: Por que amam? Double down nisso
- **Passives (7-8)**: O que falta para virar promoter?
- **Detractors (0-6)**: Por que estão insatisfeitos? É o segmento errado ou problema real?

### 4. Reference customers

Clientes que ativamente recomendam sem incentivo.

| Tipo | Threshold para PMF |
|------|-------------------|
| **B2B** | 6-8 reference customers |
| **B2C** | 15-25 reference customers |
| **Enterprise** | 3-5 reference customers |

### 5. Crescimento orgânico

Sinais de organic pull:
- % de novos usuários via referral/word-of-mouth
- Crescimento sem aumento de spend em paid
- Menções espontâneas em redes sociais/comunidades
- Busca orgânica pelo nome do produto crescendo

### 6. Unit economics

| Métrica | Threshold saudável |
|---------|-------------------|
| **LTV / CAC** | > 3x |
| **CAC Payback** | < 12 meses (B2B), < 3 meses (B2C) |
| **Gross Margin** | > 60% (SaaS) |
| **Net Revenue Retention** | > 100% (B2B SaaS) |

---

## Superhuman PMF Engine (Rahul Vohra)

Framework sistemático para CONSTRUIR PMF, não apenas medir:

### Passo 1 — Segmentar por "very disappointed"
Identificar QUEM são os 40% (ou menos) que marcaram "muito desapontado". Esse é seu ICP real.

### Passo 2 — Entender o que amam
Perguntar: "Qual é o principal benefício que você recebe de [produto]?"
Agrupar respostas por tema. Esses são seus differentiators.

### Passo 3 — Melhorar para os "somewhat disappointed"
Perguntar: "O que melhoraria [produto] para você?"
Filtrar apenas respostas de quem é similar ao ICP do Passo 1.
Implementar melhorias que não comprometam o que os "very disappointed" amam.

### Passo 4 — Tracking contínuo
Rodar Sean Ellis Survey a cada 2-4 semanas. Plotar score ao longo do tempo.
Meta: mover de X% → 40%+ "very disappointed".

---

## Processo de assessment

### Passo 1 — Rodar Sean Ellis Survey
Enviar para base ativa (mínimo 40 respostas). Incluir perguntas abertas.

### Passo 2 — Segmentar respostas
Quem são os "very disappointed"? Perfil, use case, canal de aquisição, tempo de uso.

### Passo 3 — Analisar retenção por cohort
Plotar curvas de retenção. Identificar padrão (queda, flat, smile).

### Passo 4 — Contar reference customers
Quantos clientes recomendam ativamente sem incentivo?

### Passo 5 — Checar sinais orgânicos
% de crescimento orgânico, menções espontâneas, busca por marca.

### Passo 6 — Avaliar unit economics
LTV/CAC, payback period, net revenue retention.

### Passo 7 — Classificar estágio de PMF

```
PMF CLASSIFICATION MATRIX
═══════════════════════════════════════════════════

             Nascent    Developing   Strong    Extreme
Sean Ellis    < 20%     20-39%       40-60%    > 60%
Retenção      Caindo    Estável      Flat/Up   Smile
Ref. Cust.    0-2       3-5          6-15      15+
Organic %     < 10%     10-30%       30-50%    > 50%
LTV/CAC       < 1x      1-3x         3-5x     > 5x
```

### Passo 8 — Definir plano de ação

| Estágio | Ação principal |
|---------|---------------|
| **Nascent** | Voltar para discovery. Entrevistar churned users. Pivotar se necessário. |
| **Developing** | Focar no segmento que mais gosta. Usar Superhuman Engine. |
| **Strong** | Investir em growth. Escalar canais que funcionam. |
| **Extreme** | Proteger PMF. Monitorar degradação. Expandir para adjacências. |

---

## Template de output

```
╔══════════════════════════════════════════════════════════╗
║              PMF ASSESSMENT REPORT                       ║
╠══════════════════════════════════════════════════════════╣

📋 CONTEXTO
Produto: [nome]
Segmento analisado: [quem]
Base de usuários: [N ativos]
Tempo desde launch: [X meses]

📊 SCORES
Sean Ellis: [X%] "very disappointed" (N=[respostas])
NPS: [score] (N=[respostas])
Retenção M6: [X%]
Reference customers: [N]
Crescimento orgânico: [X%]
LTV/CAC: [Xx]

🎯 CLASSIFICAÇÃO
Estágio: [Nascent / Developing / Strong / Extreme]

Evidências:
✅ [sinal positivo 1]
✅ [sinal positivo 2]
⚠️ [sinal de alerta 1]
❌ [sinal negativo 1]

👤 ICP (quem são os "very disappointed")
- Perfil: [descrição]
- Use case principal: [descrição]
- O que mais valorizam: [descrição]

📈 PLANO DE AÇÃO
Prioridade 1: [ação]
Prioridade 2: [ação]
Prioridade 3: [ação]

Timeline recomendado para re-assessment: [X semanas]

╚══════════════════════════════════════════════════════════╝
```

---

## Exemplo de uso

**Input:**
> /measure-pmf CRM para pequenas agências de marketing, 200 usuários ativos, 3 meses pós-launch. Tenho NPS de 45 e retenção M3 de 35%.

**Output esperado:**
- Sean Ellis: Propor questionário (ainda não rodou)
- Retenção M3 35%: sinal de Developing (estabilizando?)
- NPS 45: bom, mas precisa segmentar
- Ação: Rodar Sean Ellis, segmentar por tipo de agência, identificar ICP
- Estágio provável: Developing (com potencial para Strong se segmentar)

---

## Armadilhas comuns

1. **Confundir crescimento com PMF**: Pode crescer via paid sem ter PMF (leaky bucket)
2. **Medir base inteira**: PMF existe em segmentos — sempre segmentar
3. **Ignorar churn**: Alto churn + alto growth = ilusão de PMF
4. **PMF de uma feature**: Usuários amam 1 feature mas não o produto inteiro
5. **Survivorship bias**: Só medir quem ficou, ignorar quem saiu
6. **Declarar PMF cedo demais**: Esperar pelo menos 3 cohorts antes de concluir

---

## Referências

- Sean Ellis — "Hacking Growth" (Sean Ellis Test)
- Rahul Vohra — "How Superhuman Built an Engine to Find PMF"
- Lenny Rachitsky — "Measuring Product-Market Fit" (46 product leaders)
- Marc Andreessen — "The Only Thing That Matters"
- First Round Review — "How to Know If You've Got PMF"

$ARGUMENTS
