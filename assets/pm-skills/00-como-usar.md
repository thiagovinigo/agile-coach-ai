# PM Assistant — Quick Start

## O que é o PM Assistant

O PM Assistant é um sistema de **27 skills** que cobre todo o ciclo de vida de Product Management — de discovery a lançamento, de estratégia a comunicação com stakeholders. Cada skill é um comando especializado que gera artefatos prontos para uso, eliminando templates genéricos e acelerando decisões de produto. Você fornece contexto, a skill entrega o artefato estruturado.

---

## Mapa dos 6 Domínios

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PM ASSISTANT — 27 SKILLS                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  DISCOVERY (7)                    STRATEGY (7)                      │
│  ┌─────────────────────────┐     ┌─────────────────────────────┐   │
│  │ persona                 │     │ prioritize                  │   │
│  │ discovery               │     │ strategy                    │   │
│  │ interview-synthesis     │     │ competitive-analysis        │   │
│  │ competitive-analysis    │     │ roadmap                     │   │
│  │ opportunity-tree        │     │ okr                         │   │
│  │ hypothesis              │     │ lean-canvas                 │   │
│  │ customer-journey        │     │ pricing                     │   │
│  └─────────────────────────┘     │ north-star                  │   │
│                                  └─────────────────────────────┘   │
│  DELIVERY (3)                     VALIDATION (3)                    │
│  ┌─────────────────────────┐     ┌─────────────────────────────┐   │
│  │ prd                     │     │ experiment-design           │   │
│  │ user-stories            │     │ measure-pmf                 │   │
│  │ acceptance-criteria     │     │ ab-test-analysis            │   │
│  └─────────────────────────┘     └─────────────────────────────┘   │
│                                                                     │
│  EXECUTION (2)                    COMMUNICATION & GTM (5)           │
│  ┌─────────────────────────┐     ┌─────────────────────────────┐   │
│  │ pre-mortem              │     │ release-notes               │   │
│  │ launch-checklist        │     │ stakeholder-update          │   │
│  └─────────────────────────┘     │ gtm                         │   │
│                                  │ battlecard                   │   │
│                                  │ ideal-customer-profile       │   │
│                                  └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Como Chamar uma Skill

A sintaxe é simples — chame o comando e forneça contexto:

```
/nome-da-skill
Contexto: [seu contexto aqui]
```

### Exemplo rápido com `/discovery`

```
/discovery
Contexto: Somos um SaaS B2B de gestão financeira para PMEs.
Estamos investigando por que 40% dos usuários abandonam
o onboarding na etapa de integração bancária.
Público: donos de pequenas empresas, 10-50 funcionários.
```

A skill retorna: framework de discovery estruturado com hipóteses, perguntas de pesquisa, métodos sugeridos e próximos passos.

---

## Como Encadear Skills (Output → Input)

O verdadeiro poder do PM Assistant está no encadeamento. O output de uma skill vira input da próxima:

```
/persona        →  cria persona detalhada
      ↓
/discovery      →  usa a persona para estruturar discovery
      ↓
/prd            →  usa os achados do discovery para escrever o PRD
      ↓
/user-stories   →  quebra o PRD em user stories para eng
```

**Na prática:**

1. Execute `/persona` e salve o resultado
2. Execute `/discovery` colando a persona como contexto
3. Execute `/prd` colando os achados do discovery
4. Continue a cadeia conforme necessário

---

## Regras de Ouro

| Regra | Por quê |
|-------|---------|
| **Sempre forneça contexto mínimo** (problema + audiência + constraints) | Sem contexto, o output será genérico e pouco útil |
| **Quanto mais específico o input, melhor o output** | "SaaS B2B de RH para empresas de 50-200 pessoas" > "um produto de software" |
| **Use `Refine:` para ajustar outputs** | Não precisa rodar tudo de novo — peça ajustes pontuais |
| **Skills são independentes mas mais poderosas encadeadas** | Cada skill funciona sozinha, mas o encadeamento gera artefatos consistentes |
| **Salve outputs intermediários** | Eles são o contexto das próximas skills na cadeia |

---

## Tabela Completa — 27 Skills

### DISCOVERY

| Skill | Descrição | Quando usar |
|-------|-----------|-------------|
| `/persona` | Gera persona detalhada com jobs-to-be-done, dores e comportamentos | Início de projeto, precisa definir pra quem está construindo |
| `/discovery` | Estrutura plano de discovery com hipóteses e métodos de pesquisa | Vai investigar um problema ou oportunidade nova |
| `/interview-synthesis` | Sintetiza entrevistas em padrões, insights e recomendações | Fez entrevistas e precisa extrair aprendizados |
| `/competitive-analysis` | Análise competitiva estruturada com posicionamento e gaps | Precisa entender o cenário competitivo antes de decidir |
| `/opportunity-tree` | Monta árvore de oportunidades (Opportunity Solution Tree) | Quer organizar oportunidades e mapear soluções possíveis |
| `/hypothesis` | Formula hipóteses testáveis no formato "Se X, então Y, medido por Z" | Precisa transformar achados em hipóteses para validar |
| `/customer-journey` | Mapeia jornada do cliente com touchpoints, emoções e gaps | Quer visualizar a experiência completa do usuário |

### DELIVERY

| Skill | Descrição | Quando usar |
|-------|-----------|-------------|
| `/prd` | Gera PRD completo com problema, solução, métricas e escopo | Hipótese validada, hora de especificar a solução |
| `/user-stories` | Quebra PRD em user stories com critérios de aceite | PRD aprovado, precisa alimentar o backlog de eng |
| `/acceptance-criteria` | Detalha critérios de aceite para uma story específica | Story precisa de mais detalhe para QA e eng |

### STRATEGY

| Skill | Descrição | Quando usar |
|-------|-----------|-------------|
| `/prioritize` | Aplica frameworks de priorização (RICE, ICE, MoSCoW) ao backlog | Tem muitas ideias e precisa decidir o que fazer primeiro |
| `/strategy` | Define estratégia de produto com visão, positioning e moats | Início de ciclo, precisa definir direção de produto |
| `/roadmap` | Gera roadmap orientado a outcomes, não features | Precisa comunicar o plano para time e stakeholders |
| `/okr` | Define OKRs com objetivos e key results mensuráveis | Início de trimestre, precisa alinhar metas do time |
| `/lean-canvas` | Gera Lean Canvas completo para um produto ou feature | Explorando uma ideia nova, precisa de visão 360 rápida |
| `/pricing` | Estrutura estratégia de pricing com tiers e justificativa | Precisa definir ou revisar modelo de monetização |
| `/north-star` | Define North Star Metric com input metrics e leading indicators | Quer alinhar todo o time em torno de uma métrica principal |

### VALIDATION

| Skill | Descrição | Quando usar |
|-------|-----------|-------------|
| `/experiment-design` | Desenha experimento com hipótese, métrica, critério de sucesso | Quer testar algo antes de investir em construção completa |
| `/measure-pmf` | Avalia Product-Market Fit com frameworks (Sean Ellis, retenção) | Precisa evidenciar se o produto tem fit com o mercado |
| `/ab-test-analysis` | Analisa resultado de A/B test com significância e recomendação | Rodou um teste e precisa interpretar os dados |

### EXECUTION

| Skill | Descrição | Quando usar |
|-------|-----------|-------------|
| `/pre-mortem` | Lista riscos e mitigações antes do lançamento | Feature quase pronta, quer antecipar o que pode dar errado |
| `/launch-checklist` | Checklist completo de lançamento por área (eng, marketing, CS) | Preparando lançamento, quer garantir que nada ficou pra trás |

### COMMUNICATION & GTM

| Skill | Descrição | Quando usar |
|-------|-----------|-------------|
| `/release-notes` | Gera release notes claras para diferentes audiências | Lançou algo e precisa comunicar para usuários |
| `/stakeholder-update` | Estrutura update executivo com progresso, riscos e asks | Reunião de status com liderança ou stakeholders |
| `/gtm` | Plano de go-to-market com canais, messaging e timeline | Precisa planejar como levar o produto ao mercado |
| `/battlecard` | Gera battlecard de vendas com comparativo competitivo | Time de vendas precisa de munição contra concorrentes |
| `/ideal-customer-profile` | Define ICP detalhado com firmographics e sinais de compra | Precisa alinhar marketing e vendas em quem é o cliente ideal |

---

## Proximos Passos

- **[Do Zero ao Um — Tutorial completo de Discovery a PRD](01-zero-a-um.md)** — Walkthrough passo a passo de um ciclo completo
- **[Do Um ao Cem — Escalar produto com o PM Assistant](02-um-a-cem.md)** — Estratégia, growth e comunicação
- **[Workflows Prontos](03-workflows.md)** — 7 receitas prontas para cenários reais de PM
