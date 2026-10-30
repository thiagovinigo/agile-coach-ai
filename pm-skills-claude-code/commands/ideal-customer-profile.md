# Ideal Customer Profile (ICP)

Definição completa de ICP com 4 componentes: Demographics, Behaviors, Jobs to Be Done e Needs & Pain Points.
Inclui ideal-of-ideal, critérios de desqualificação e implicações para GTM.
Fonte: phuryn ideal-customer-profile.

## Argumentos

- `$ARGUMENTS` — Produto/serviço, mercado-alvo e dados disponíveis sobre clientes atuais

---

## Instruções

Você é um PM sênior especializado em product-market fit, segmentação e GTM strategy.
Sua missão é construir um ICP robusto e acionável que guie decisões de produto, marketing e vendas.

### Etapa 1 — Coleta de dados do cliente

Analise `$ARGUMENTS` e identifique quais fontes de dados estão disponíveis:

**Fontes ideais (peça ao usuário se não fornecidas):**
- Resultados de PMF survey (Sean Ellis test)
- Entrevistas com clientes
- Dados de comportamento de uso (product analytics)
- Análise de churn (por que saíram?)
- Win/loss analysis (por que ganhamos/perdemos deals?)
- NPS/CSAT data
- Revenue data por segmento
- Time-to-value por cohort

Se dados não estiverem disponíveis, construa o ICP baseado em hipóteses informadas
e marque claramente o que precisa ser validado.

### Etapa 2 — Segmentação por valor

Identifique os clientes de maior valor usando estes critérios:
- **Highest LTV**: Quem gasta mais ao longo do tempo?
- **Fastest time-to-value**: Quem ativa mais rápido?
- **Lowest churn**: Quem fica mais tempo?
- **Most enthusiastic**: Quem recomenda mais (NPS promoters)?
- **Lowest CAC**: Quem é mais barato de adquirir?

O ICP deve refletir esse perfil de alto valor, não o cliente médio.

### Etapa 3 — Perfil demográfico

Mapeie padrões nos clientes de maior valor.

### Etapa 4 — Análise comportamental

Identifique padrões de comportamento dos melhores clientes.

### Etapa 5 — Jobs to Be Done

Defina os jobs usando o framework JTBD completo.

### Etapa 6 — Needs & Pain Points

Documente dores específicas com profundidade.

### Etapa 7 — Síntese e implicações

Compile o ICP final com implicações práticas para produto, marketing e vendas.

---

## Formato de saída

```markdown
# Ideal Customer Profile: [Produto/Serviço]

**Data:** [data]
**Baseado em:** [fontes de dados utilizadas]
**Confiança:** [Alta/Média/Baixa — baseada na qualidade dos dados]

---

## Executive Summary

[2-3 parágrafos resumindo quem é o cliente ideal, por que ele é ideal,
e qual o impacto de focar nesse perfil]

---

## 1. Demographics (Quem é)

### Firmográfico (Empresa)

| Dimensão | ICP | Aceitável | Fora do ICP |
|----------|-----|-----------|-------------|
| **Tamanho (funcionários)** | [range ideal] | [range aceitável] | [range a evitar] |
| **Revenue anual** | [range] | [range] | [range] |
| **Indústria** | [top 3 indústrias] | [outras aceitáveis] | [indústrias a evitar] |
| **Geografia** | [regiões ideais] | [outras aceitáveis] | [regiões problemáticas] |
| **Maturidade** | [estágio ideal] | [aceitável] | [a evitar] |
| **Stack tecnológico** | [ferramentas que usam] | [aceitável] | [incompatível] |

### Pessoal (Comprador/Usuário)

| Dimensão | Buyer (quem compra) | Champion (quem defende) | User (quem usa) |
|----------|--------------------|-----------------------|-----------------|
| **Título** | [títulos comuns] | [títulos comuns] | [títulos comuns] |
| **Departamento** | [dept] | [dept] | [dept] |
| **Senioridade** | [nível] | [nível] | [nível] |
| **Experiência** | [anos/background] | [anos/background] | [anos/background] |
| **Reports to** | [cargo acima] | [cargo acima] | [cargo acima] |

### Decision-Making (Como compram)

| Aspecto | Detalhe |
|---------|---------|
| **Buying committee** | [quem participa da decisão — tamanho e papéis] |
| **Budget owner** | [quem tem o budget] |
| **Ciclo de compra típico** | [duração em semanas/meses] |
| **Processo de avaliação** | [RFP, trial, POC, etc.] |
| **Triggers de compra** | [eventos que iniciam a busca] |
| **Deal size médio** | [ACV range] |

---

## 2. Behaviors (Como age)

### Descoberta de soluções
- **Como descobre ferramentas novas:** [canais — peers, comunidades, Google, eventos, etc.]
- **Conteúdo que consome:** [blogs, podcasts, newsletters, etc.]
- **Comunidades que participa:** [Slack groups, LinkedIn, conferências, etc.]
- **Influenciadores que segue:** [referências no segmento]

### Processo de avaliação
- **Primeira ação ao avaliar:** [demo, trial, docs, reviews?]
- **Critérios de decisão (ranked):**
  1. [Critério mais importante]
  2. [Segundo critério]
  3. [Terceiro critério]
  4. [Quarto critério]
- **Número de soluções avaliadas:** [tipicamente N]
- **Quem envolve na avaliação:** [papéis]

### Adoção e uso
- **Velocidade de adoção:** [rápido/gradual/lento]
- **Onboarding expectation:** [self-serve, guided, white-glove]
- **Frequência de uso:** [diário/semanal/mensal]
- **Depth of use:** [power user vs. casual]
- **Frequência de troca de ferramenta:** [a cada N anos]
- **Razões para trocar:** [top 3 motivos]

### Sinais de engajamento
- **Leading indicators de sucesso:**
  - [Ação 1 nos primeiros N dias]
  - [Ação 2 nos primeiros N dias]
  - [Ação 3 nos primeiros N dias]
- **Red flags de churn:**
  - [Sinal 1]
  - [Sinal 2]
  - [Sinal 3]

---

## 3. Jobs to Be Done

### Primary Job (Funcional)
> "Quando eu [situação/trigger], eu quero [ação/capability],
> para que eu consiga [resultado esperado]."

**Frequência:** [diário/semanal/mensal/eventual]
**Métrica de sucesso:** [como medem se o job foi bem feito]
**Alternativas atuais:** [como resolvem hoje sem nosso produto]

### Secondary Jobs (Funcionais)

| Job | Situação | Resultado esperado | Frequência |
|-----|----------|--------------------|------------|
| [Job 2] | [Quando...] | [Para que...] | [freq] |
| [Job 3] | [Quando...] | [Para que...] | [freq] |
| [Job 4] | [Quando...] | [Para que...] | [freq] |

### Emotional Jobs (Como quer se sentir)

| Job emocional | Descrição |
|---------------|-----------|
| **Confiança** | [Quer se sentir seguro de que está fazendo a coisa certa] |
| **Competência** | [Quer parecer competente para peers e liderança] |
| **Controle** | [Quer ter visibilidade e controle do processo] |
| **[Outro]** | [Descrição] |

### Social Jobs (Como quer ser percebido)

| Job social | Descrição |
|------------|-----------|
| **Pelos peers** | [Como quer ser visto pelo time/colegas] |
| **Pela liderança** | [Como quer ser visto pelo chefe/board] |
| **Pelo mercado** | [Como quer ser percebido externamente] |

---

## 4. Needs & Pain Points

### Pain Points detalhados

#### Pain 1: [Nome da dor]
- **Descrição:** [O que está doendo]
- **Estado atual (Before):** [Como é a vida hoje]
- **Estado desejado (After):** [Como deveria ser]
- **Gap:** [Diferença quantificada entre before e after]
- **Workaround atual:** [Como contornam hoje]
- **Custo do workaround:** [Tempo, dinheiro, frustração]
- **Impacto na produtividade:** [Horas/semana perdidas]
- **Impacto emocional:** [Frustração, stress, insegurança]
- **Budget disponível para resolver:** [Disposição a pagar]
- **Urgência:** [Alta/Média/Baixa — quando precisam resolver]

#### Pain 2: [Nome da dor]
[Mesmo formato acima]

#### Pain 3: [Nome da dor]
[Mesmo formato acima]

#### Pain 4: [Nome da dor]
[Mesmo formato acima]

### Ranking de dores por intensidade

| Rank | Pain Point | Intensidade (1-10) | Frequência | Willingness to pay |
|------|------------|-------------------|------------|-------------------|
| 1 | [Pain mais intensa] | [N] | [freq] | [Alta/Média/Baixa] |
| 2 | [Pain] | [N] | [freq] | [nível] |
| 3 | [Pain] | [N] | [freq] | [nível] |
| 4 | [Pain] | [N] | [freq] | [nível] |

---

## 5. Ideal-of-Ideal (Segmento de maior valor)

O sub-segmento dentro do ICP que gera mais valor:

| Dimensão | Ideal-of-Ideal |
|----------|----------------|
| **Perfil** | [Descrição mais específica] |
| **% da base atual** | [estimativa] |
| **LTV relativo** | [N]x a média |
| **Churn rate** | [N]% vs [N]% média |
| **Time-to-value** | [N] dias vs [N] dias média |
| **NPS** | [N] vs [N] média |
| **Por que são melhores** | [Razão principal] |
| **Como encontrar mais** | [Canais e sinais] |

---

## 6. Disqualification Criteria (Quem NÃO perseguir)

### Hard disqualifiers (Não vender — vai dar problema)
- [ ] [Critério 1 — ex: empresa com menos de N funcionários]
- [ ] [Critério 2 — ex: indústria regulada que não suportamos]
- [ ] [Critério 3 — ex: expectativa de customização pesada]
- [ ] [Critério 4 — ex: budget abaixo de $N/mês]

### Soft disqualifiers (Proceder com cautela)
- [ ] [Critério 1 — ex: sem champion interno identificado]
- [ ] [Critério 2 — ex: ciclo de decisão > N meses]
- [ ] [Critério 3 — ex: usa stack incompatível]

### Perfis que parecem ICP mas não são
| Perfil | Por que parece ICP | Por que não é | Resultado típico |
|--------|-------------------|---------------|------------------|
| [Perfil 1] | [Razão] | [Razão] | [O que acontece] |
| [Perfil 2] | [Razão] | [Razão] | [O que acontece] |

---

## 7. GTM Implications (Implicações práticas)

### Para Produto
- **Features prioritárias:** [O que construir primeiro para esse ICP]
- **Features a evitar:** [O que NÃO construir — distração]
- **Onboarding ideal:** [Como deve ser a experiência]
- **Pricing model:** [Modelo que faz sentido para esse ICP]

### Para Marketing
- **Messaging principal:** "[Frase de posicionamento para esse ICP]"
- **Canais prioritários:** [Top 3 canais de aquisição]
- **Conteúdo que ressoa:** [Tipos de conteúdo que convertem]
- **Keywords/temas:** [Termos que esse ICP busca]
- **Case study ideal:** [Perfil de cliente para showcase]

### Para Vendas
- **Qualification perguntas:** [Top 5 perguntas de qualificação]
- **Pitch angle:** [Como posicionar para esse ICP]
- **Objeções mais comuns:** [Top 3 objeções]
- **Competidores mais frequentes:** [Com quem compete nesse segmento]
- **Deal velocity esperada:** [Tempo médio de fechamento]

### Para Customer Success
- **Onboarding milestones:** [Marcos de sucesso nos primeiros 90 dias]
- **Health score indicators:** [O que indica cliente saudável]
- **Expansion triggers:** [Quando oferecer upsell/cross-sell]
- **Churn prevention:** [Sinais de alerta e ações]

---

## Validation Checklist

Itens a validar para confirmar/ajustar esse ICP:

- [ ] Entrevistar [N] clientes do perfil ideal-of-ideal
- [ ] Analisar cohort de clientes high-LTV vs low-LTV
- [ ] Confirmar hipóteses de JTBD com entrevistas
- [ ] Validar willingness-to-pay com teste de pricing
- [ ] Testar messaging com A/B em landing pages
- [ ] Verificar CAC por segmento para confirmar eficiência
- [ ] Revisar win/loss data dos últimos [N] meses
```

---

## Princípios

- **Dados > Opiniões**: Sempre que possível, baseie em dados reais de clientes
- **Específico > Genérico**: ICP amplo demais não serve para nada — seja específico
- **Prático > Teórico**: Cada seção deve gerar ações concretas
- **Honesto sobre gaps**: Marque claramente o que é hipótese vs dado validado
- **Revisão regular**: ICP deve ser revisado a cada trimestre no mínimo
- **Cross-functional**: ICP serve produto, marketing, vendas e CS — todos devem usar

## Exemplo de uso

```
/ideal-customer-profile CRM focado em vendas consultivas B2B.
Clientes atuais: consultorias, agências digitais e empresas de serviços profissionais.
Melhores clientes: 50-200 funcionários, time de vendas de 5-20 pessoas,
ciclo de venda > 30 dias, ticket médio > R$10k.
Maior churn: empresas < 20 funcionários e e-commerce (transacional, não consultivo).
PMF survey: 48% "muito decepcionado" se não pudesse mais usar.
```
