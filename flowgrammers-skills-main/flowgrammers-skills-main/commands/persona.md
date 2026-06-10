# /persona

## O que essa skill faz

Gera uma persona de produto completa com integração JTBD (Jobs to Be Done). Combina dados demográficos, comportamentais e motivacionais em um documento que serve como referência viva para decisões de produto.

Saída: **Persona contract** com 9 seções — do perfil demográfico até nível de confiança por seção.

---

## Quando usar

- Início de discovery — precisa definir para quem está construindo
- Está entrando em mercado novo e precisa alinhar o time sobre o usuário-alvo
- Tem dados de pesquisa (entrevistas, surveys) e quer consolidar em persona acionável
- Quer substituir personas vagas ("João, 35 anos, gosta de tecnologia") por personas com JTBD real

---

## Input esperado

**Mínimo:**
- **Produto/contexto**: O que está construindo e para quem
- **Segmento-alvo**: Tipo de usuário, cargo, indústria
- **Problema principal**: O que esse usuário tenta resolver

**Opcional:**
- Trechos de entrevistas ou pesquisa qualitativa
- Dados de analytics (comportamento real)
- Personas existentes para refinar
- Competitors que esse usuário usa hoje
- Tamanho do mercado / empresa típica

---

## Processo

1. **Coletar contexto** — Reunir todas as informações disponíveis sobre o segmento. Se não houver dados primários, deixar explícito que a persona é hipotética (confiança Low).
2. **Definir perfil demográfico** — Nome fictício representativo, cargo, empresa típica, indústria, senioridade. Evitar estereótipos — basear em dados reais quando possível.
3. **Mapear Jobs to Be Done** — Identificar job principal (funcional), jobs secundários, jobs emocionais ("sentir-se no controle") e jobs sociais ("ser visto como competente"). Usar formato: "Quando [situação], eu quero [motivação], para que [resultado]."
4. **Identificar pain points** — Listar top 5 dores, rankeadas por severidade (1-5). Conectar cada dor a um JTBD específico.
5. **Documentar comportamentos** — Como avalia soluções, quem influencia decisão, critérios de compra, ciclo de decisão típico.
6. **Adicionar quotes** — 3-4 frases representativas que humanizam a persona. Se baseadas em entrevistas reais, marcar como [Real]. Se inferidas, marcar como [Inferido].
7. **Avaliar confiança** — Para cada seção, classificar: High (dados primários), Medium (dados secundários/inferência), Low (hipótese). Isso guia onde investir mais pesquisa.

---

## Output

```markdown
# Persona: [Nome da Persona]

> "[Quote principal que resume a essência dessa persona]"

---

## 1. Demographics

| Campo | Detalhe |
|-------|---------|
| **Nome** | [Nome fictício] |
| **Cargo** | [Título] |
| **Empresa** | [Tipo: startup/mid-market/enterprise] |
| **Tamanho** | [Número de funcionários] |
| **Indústria** | [Setor] |
| **Idade** | [Faixa etária] |
| **Localização** | [Região/País] |
| **Senioridade** | [Junior/Mid/Senior/Lead/Executive] |

---

## 2. Background & Context

**Experiência:**
[X anos na função, trajetória profissional, formação relevante]

**Ferramentas que usa diariamente:**
- [Tool 1] — [para quê]
- [Tool 2] — [para quê]
- [Tool 3] — [para quê]

**Workflow típico do dia:**
1. [Manhã: atividade principal]
2. [Meio do dia: reuniões/colaboração]
3. [Tarde: tarefas operacionais]

**Contexto organizacional:**
[Estrutura do time, a quem reporta, com quem colabora]

---

## 3. Jobs to Be Done

### Job Principal (Funcional)
> Quando [situação/trigger], eu quero [motivação/ação], para que [resultado desejado].

### Jobs Secundários
- Quando [situação], eu quero [ação], para que [resultado].
- Quando [situação], eu quero [ação], para que [resultado].

### Jobs Emocionais
- Sentir [emoção desejada] ao [contexto]
- Evitar [emoção negativa] quando [contexto]

### Jobs Sociais
- Ser visto como [percepção desejada] por [audiência]
- Demonstrar [competência] para [stakeholders]

---

## 4. Pain Points & Frustrations

| # | Pain Point | Severidade (1-5) | JTBD Relacionado | Frequência |
|---|-----------|-------------------|-------------------|------------|
| 1 | [Dor mais crítica] | 5 | [Job] | [Diário/Semanal] |
| 2 | [Segunda dor] | 4 | [Job] | [Frequência] |
| 3 | [Terceira dor] | 4 | [Job] | [Frequência] |
| 4 | [Quarta dor] | 3 | [Job] | [Frequência] |
| 5 | [Quinta dor] | 2 | [Job] | [Frequência] |

---

## 5. Goals & Desired Outcomes

**O que sucesso parece para essa persona:**
- [Outcome 1 — mensurável]
- [Outcome 2 — mensurável]
- [Outcome 3 — qualitativo]

**Métricas pessoais de sucesso:**
- [KPI que essa pessoa é cobrada]
- [Meta que quer atingir]

---

## 6. Current Solutions & Workarounds

| Solução Atual | Para Qual Job | Satisfação (1-5) | Limitação Principal |
|---------------|---------------|-------------------|---------------------|
| [Tool/Processo 1] | [Job] | [Score] | [Limitação] |
| [Tool/Processo 2] | [Job] | [Score] | [Limitação] |
| [Workaround manual] | [Job] | [Score] | [Limitação] |

**Custo do status quo:**
[Quanto tempo/dinheiro/frustração o workaround atual custa]

---

## 7. Behaviors & Decision-Making

**Como descobre novas soluções:**
- [Canal 1: peers, blogs, conferences, etc.]
- [Canal 2]

**Critérios de avaliação (em ordem de prioridade):**
1. [Critério mais importante]
2. [Segundo critério]
3. [Terceiro critério]

**Quem influencia a decisão:**
- [Pessoa/cargo — tipo de influência]
- [Pessoa/cargo — tipo de influência]

**Ciclo de decisão típico:** [X semanas/meses]

**Objeções comuns:**
- "[Objeção 1]"
- "[Objeção 2]"

---

## 8. Quotes

> "[Quote 1 — sobre a dor principal]" [Real/Inferido]

> "[Quote 2 — sobre o que deseja]" [Real/Inferido]

> "[Quote 3 — sobre frustração com solução atual]" [Real/Inferido]

> "[Quote 4 — sobre o que sucesso parece]" [Real/Inferido]

---

## 9. Confidence Level

| Seção | Confiança | Base |
|-------|-----------|------|
| Demographics | [High/Medium/Low] | [Fonte] |
| Background | [High/Medium/Low] | [Fonte] |
| JTBD | [High/Medium/Low] | [Fonte] |
| Pain Points | [High/Medium/Low] | [Fonte] |
| Goals | [High/Medium/Low] | [Fonte] |
| Current Solutions | [High/Medium/Low] | [Fonte] |
| Behaviors | [High/Medium/Low] | [Fonte] |

**Próximos passos de pesquisa:**
- [ ] [Área de baixa confiança que precisa validação]
- [ ] [Hipótese que precisa ser testada]
```

---

## Exemplo

**Input:**
> Produto: CRM para times de vendas mid-market. Segmento: PM que está construindo o CRM. Problema: PMs não conseguem priorizar features porque não entendem o workflow real do sales rep.

**Output:**

```markdown
# Persona: Rafael Mendes

> "Eu passo mais tempo tentando entender o que o time de vendas precisa do que efetivamente priorizando o que construir."

---

## 1. Demographics

| Campo | Detalhe |
|-------|---------|
| **Nome** | Rafael Mendes |
| **Cargo** | Product Manager |
| **Empresa** | SaaS mid-market (série B) |
| **Tamanho** | 150-500 funcionários |
| **Indústria** | Software B2B |
| **Idade** | 28-35 anos |
| **Localização** | São Paulo, Brasil |
| **Senioridade** | Mid-level (3-5 anos como PM) |

---

## 2. Background & Context

**Experiência:**
4 anos como PM, começou como analista de negócios. Transição para produto após MBA. Tem background técnico suficiente para conversar com engenharia, mas não codifica. Já trabalhou em 2 empresas SaaS.

**Ferramentas que usa diariamente:**
- **Jira** — gestão de backlog e sprints
- **Figma** — review de designs com UX
- **Amplitude** — análise de métricas de produto
- **Slack** — comunicação com time e stakeholders
- **Google Sheets** — priorização e análises ad-hoc

**Workflow típico do dia:**
1. Manhã: review de métricas no Amplitude, standup com eng
2. Meio do dia: 2-3 reuniões (stakeholders, design reviews, discovery)
3. Tarde: escrita de specs, priorização de backlog, 1:1s

**Contexto organizacional:**
Reporta ao Head de Produto. Trabalha com 1 designer, 1 squad de eng (5 devs), e interage diretamente com VP de Sales e Customer Success.

---

## 3. Jobs to Be Done

### Job Principal (Funcional)
> Quando estou planejando o próximo trimestre, eu quero entender quais problemas dos sales reps causam mais perda de receita, para que eu priorize features que realmente impactem conversão.

### Jobs Secundários
- Quando recebo feedback de vendas, eu quero traduzir pedidos de feature em problemas reais, para que não construa a solução errada.
- Quando apresento o roadmap, eu quero justificar prioridades com dados, para que stakeholders confiem nas decisões.

### Jobs Emocionais
- Sentir confiança de que está construindo a coisa certa
- Evitar a ansiedade de ter priorizado errado quando churn aumenta

### Jobs Sociais
- Ser visto como PM que entende o negócio pelo VP de Sales
- Demonstrar pensamento estratégico para o Head de Produto

---

## 4. Pain Points & Frustrations

| # | Pain Point | Severidade | JTBD Relacionado | Frequência |
|---|-----------|------------|-------------------|------------|
| 1 | Não tem acesso direto ao workflow real do sales rep — depende de relatos filtrados pelo VP Sales | 5 | Job Principal | Semanal |
| 2 | Pedidos de feature chegam como soluções, não como problemas | 4 | Job Secundário 1 | Diário |
| 3 | Dados quantitativos do CRM atual não mostram onde o rep trava no processo | 4 | Job Principal | Semanal |
| 4 | Stakeholders questionam prioridades sem entender o racional | 3 | Job Secundário 2 | Quinzenal |
| 5 | Ciclo de feedback muito longo — lança feature e leva semanas para saber se resolveu | 2 | Job Principal | Mensal |

---

## 5. Goals & Desired Outcomes

**O que sucesso parece para Rafael:**
- Reduzir churn de clientes mid-market de 8% para 5% ao trimestre
- Aumentar NPS do módulo de pipeline de 30 para 50
- Conseguir que 80% do roadmap seja baseado em dados de discovery, não em HiPPO

**Métricas pessoais de sucesso:**
- Feature adoption rate > 60% nos primeiros 30 dias
- Zero features lançadas que ninguém usa (0 zombie features por quarter)

---

## 6. Current Solutions & Workarounds

| Solução Atual | Para Qual Job | Satisfação | Limitação Principal |
|---------------|---------------|------------|---------------------|
| Entrevistas mensais com 3-4 reps | Entender workflow | 3/5 | Amostra pequena, viés de seleção |
| Análise de tickets do CS | Identificar dores | 2/5 | Tickets são sintomas, não causas |
| Google Sheets com matriz de priorização | Priorizar features | 3/5 | Dados de input são fracos |
| Shadowing presencial (quando possível) | Entender workflow real | 4/5 | Não escala, consome dia inteiro |

**Custo do status quo:**
Rafael gasta ~8h/semana coletando e interpretando feedback de vendas. Estima que 30% das features entregues no último ano tiveram adoção abaixo de 20%.

---

## 7. Behaviors & Decision-Making

**Como descobre novas soluções:**
- Comunidade de PMs no Slack (grupos como Mind the Product Brasil)
- Posts no Lenny's Newsletter e Reforge
- Recomendações de outros PMs na empresa

**Critérios de avaliação (em ordem):**
1. Resolve o problema de discovery (acesso a dados reais do usuário)
2. Integra com stack atual (Jira, Amplitude)
3. Time-to-value rápido (não pode levar meses para setup)

**Quem influencia a decisão:**
- Head de Produto — aprovação de budget e ferramentas
- VP de Sales — se não comprar a abordagem, boicota passivamente

**Ciclo de decisão típico:** 4-6 semanas

**Objeções comuns:**
- "Já temos dados no Amplitude, precisa de mais uma ferramenta?"
- "O time de vendas não vai ter tempo de participar de entrevistas recorrentes."

---

## 8. Quotes

> "Toda vez que o VP de Sales vem com 'precisamos de X feature', eu sei que tem um problema real embaixo — mas leva semanas para escavar qual é." [Inferido]

> "Meu maior medo é construir algo que o sales rep não usa e ouvir 'eu avisei que não era isso'." [Inferido]

> "Shadowing é ouro. Cada vez que sento do lado de um rep, descubro algo que nunca apareceu em entrevista. Mas não consigo fazer isso toda semana." [Inferido]

> "Quero chegar na reunião de roadmap e ter dados, não opiniões. Hoje é 50/50." [Inferido]

---

## 9. Confidence Level

| Seção | Confiança | Base |
|-------|-----------|------|
| Demographics | Medium | Perfil típico de PM em SaaS mid-market BR |
| Background | Medium | Padrão observado em comunidades de PM |
| JTBD | Medium | Inferido de contexto + padrões comuns |
| Pain Points | Low | Hipótese — precisa validar com entrevistas |
| Goals | Medium | Métricas típicas de produto B2B |
| Current Solutions | Low | Hipótese baseada em ferramentas comuns |
| Behaviors | Low | Necessita pesquisa primária |

**Próximos passos de pesquisa:**
- [ ] Entrevistar 5-8 PMs que trabalham com CRM mid-market
- [ ] Validar se pain point #1 (acesso a workflow real) é de fato o mais severo
- [ ] Mapear stack real de ferramentas (pode variar muito)
- [ ] Coletar quotes reais para substituir os inferidos
```

---

## Dicas

- **Não invente dados como se fossem reais.** Se a persona é hipotética, marque confiança como Low. Persona com confiança falsa é pior que não ter persona.
- **JTBD não é feature request.** "Quero um dashboard" é feature. "Quero entender onde meu time trava" é job. Sempre traduza.
- **Persona não é estática.** Revise a cada ciclo de discovery. Persona desatualizada vira ficção.
- **Evite persona genérica demais.** Se a persona serve para qualquer produto, está genérica demais. O poder está nos detalhes específicos do contexto.
