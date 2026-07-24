# /prd

## O que essa skill faz

Gera PRD (Product Requirements Document) completo em 8 seções: problema, usuários, solução, métricas, critérios de sucesso, riscos, dependências, roadmap.

Saída: **PRD formatado** pronto para design, eng e stakeholder review.

---

## Quando usar

- Descoberta validou uma hipótese — hora de especificar
- Tem ideia e precisa estruturar antes de começar
- Vai rodar com múltiplos times e precisa alinhamento escrito

---

## Input esperado

**Mínimo:**
- **Problema**: Qual problema resolve (de descoberta ou entrevistas)
- **Audiência**: Quem usa (personas ou segmentos)
- **Ideia de solução**: O que você vai construir
- **Por quê agora**: Por que esse problema é prioritário

**Opcional:**
- Dados de discovery (trechos de entrevistas, experimentos)
- Métricas hoje (baseline)
- Constraints (timeline, tech, budget)
- Competitors ou benchmark

---

## Processo

1. **Contexto** — Resume problema + audiência + oportunidade
2. **Goals e success metrics** — Que sucesso parece? Como medir?
3. **User stories** — 5-7 stories que cobrem solução
4. **Design constraints** — Restrições técnicas, budget, timeline
5. **Risks e dependencies** — O que pode dar errado?
6. **Roadmap** — Phases de execução
7. **Success criteria** — Como vai saber se funcionou?
8. **Approval** — Quem precisa assinar

---

## Output

```markdown
# PRD: [Nome da Feature]

## 1. Problema e Oportunidade

### Problema
**1 frase clara do problema:**
Usuários de [segmento] gastam [X tempo] em [atividade], quando poderiam gastar [Y tempo].

### Contexto
- **Usuários afetados**: [Segmento], [Volume]
- **Severidade**: [Alto/Médio/Baixo]
- **Evidência**:
  - [X% de usuários mencionaram em entrevista]
  - [Y churn ligado a esse problema]
  - [Z usuários solicitaram no feedback]

### Oportunidade de negócio
- **Mercado**: [Tamanho, crescimento]
- **Segmento**: [Quem mais sofre com isso]
- **Impacto estimado**: [X% churn reduction, Y% revenue uplift]

---

## 2. Audiência

### Persona primária
**[Nome]** — [Role], [Company size]
- Problema: Gasta [X] em [atividade]
- Alternativa atual: [Usa competitors ou workaround]
- Valor que recebe: [Y% melhoria em métrica]

### Persona secundária
**[Nome]** — [Role], [Company size]
- Problema: [...]
- Alternativa atual: [...]
- Valor que recebe: [...]

### Não-audiência
Deliberadamente NÃO building para:
- [Segmento A] porque [razão]
- [Segmento B] porque [razão]

---

## 3. Solução

### Visão (1 parágrafo)
[Descrição da solução em linguagem de usuário, não técnica]

### Features principais

#### Feature 1: [Nome]
- **O que faz**: [Descrição clara]
- **Por quê importa**: Resolve [Parte do problema]
- **Sucesso parece**: User consegue [X] em [Y tempo] vs [Z tempo] hoje
- **MVP**: [Escopo mínimo para essa feature]

#### Feature 2: [Nome]
- [...]

#### Feature 3: [Nome]
- [...]

### Escopo de exclusão (não vamos fazer)
- [Feature mencionada que NÃO vai entrar]
- Razão: [Timeline, tech debt, lower priority]

### Design principles
- [Princípio 1 que guia design decisions]
- [Princípio 2]
- [Princípio 3]

---

## 4. Métricas e Success Criteria

### Metrics de negócio

| Métrica | Baseline | Target | Timeline |
|---------|----------|--------|----------|
| [Métrica 1] | [X] | [Y] | [Timeline] |
| [Métrica 2] | [X] | [Y] | [Timeline] |
| [Métrica 3] | [X] | [Y] | [Timeline] |

### Health metrics (não queremos piorar)
- [Métrica que monitora saúde geral do produto]
- Temos [baseline] hoje, vai manter > [threshold]

### User satisfaction
- **NPS**: [Target]
- **Feature adoption**: [X% de relevant users usando em 30 dias]
- **Feature love**: [X% dizendo "love it" vs "okay" ou "hate it"]

### Go-live criteria
Produto saindo quando:
- ✅ Todas as features principais QA'd
- ✅ Performance metrics atingidos
- ✅ Docs e support materiais prontos
- ✅ Rollout plan executado (beta → general)

---

## 5. Constraints e Dependências

### Constraints técnicas
- **Stack**: [Linguagem, arquitetura afetada]
- **Performance**: [API deve responder em < Xms]
- **Integrations**: [Sistemas que precisa se integrar]
- **Scale**: [Precisa suportar X usuários simultâneos]

### Constraints de negócio
- **Timeline**: Deve sair em [data] por causa de [razão]
- **Budget**: [$X] para feature
- **Team**: [Eng alocação, design, PM]

### Dependências
1. **[Equipe/Sistema]** — Precisa de [O quê] até [Data]
   - Blocker se não: [Impact]
   - Plano B: [Se não conseguir, fazer isso]

2. **[Equipe/Sistema]** — Precisa de [...]
   - [...]

### Risks e mitigações

| Risk | Probabilidade | Impacto | Mitigação |
|------|-----------|--------|----------|
| [Risk 1] | Alta | Alto | [Mitigação] |
| [Risk 2] | Média | Médio | [Mitigação] |
| [Risk 3] | Baixa | Alto | [Mitigação] |

---

## 6. Roadmap

### Phase 1: MVP (Semana 1-3)
Features:
- Feature 1 (core)
- Feature 2 (parte A)

Métricas críticas:
- [Métrica que define sucesso de MVP]

Go-live: [Data aproximada]

### Phase 2: Robustez (Semana 4-6)
Features:
- Feature 2 (parte B)
- Feature 3

Refinamentos:
- Performance optimization
- Bug fixes

### Phase 3: Expand (Semana 7+)
- Feature 4 (se MVP sucesso)
- Suporte para novo segmento

---

## 7. Casos de uso e User Stories

### Caso de uso 1: [Descrição]
```
Dado que [contexto],
Quando [ação],
Então [resultado esperado].
```

### Caso de uso 2: [...]
```
[...]
```

---

## 8. Perguntas abertas

- [ ] [Pergunta para clarificar com stakeholder]
- [ ] [...]

---

## Aprovação

| Role | Responsável | Aprovado? | Data |
|------|-----------|-----------|------|
| Product | [Name] | ☐ | |
| Engineering Lead | [Name] | ☐ | |
| Design | [Name] | ☐ | |
| [Stakeholder] | [Name] | ☐ | |

**Versão**: 1.0
**Última atualização**: [Data]
**Próxima review**: [Data + 1 mês]
```

---

## Exemplo

**Input:**
```
/prd
Problema: Novos usuários desistem em onboarding porque não conseguem criar seu primeiro deal
Audiência: Vendedores individuais em PMEs que usam Salesforce
Ideia: Guia interativo que leva usuário do login até primeiro deal criado em < 5 minutos
Por quê agora: 35% churn em 7 dias, 70% vem de usuários sem primeiro deal
```

**Output:**
```markdown
# PRD: Guided First Deal Experience

## 1. Problema e Oportunidade

### Problema
Novos usuários de CRM passam os primeiros 30 minutos explorando sem criar nada útil, e 70% deles não retornam.

### Contexto
- **Usuários afetados**: ~1000 new users/month (30% churn)
- **Severidade**: Alto (impacto direto em MRR)
- **Evidência**:
  - 5/5 entrevistados mencionaram exploração sem progresso
  - 70% que churnam nunca criaram um deal
  - NPS -15 durante primeiro dia vs +35 para usuários com deal criado

### Oportunidade
- **Impacto**: Reduzir churn de 35% para 15% = +$50k MRR
- **Segmento mais afetado**: Individual contributors, SMB vendedores
- **Timeline sensível**: Onboarding é momento crítico — depois não volta

---

## 2. Audiência

### Persona primária
**Alex** — Sales Rep, 10-50 empresa
- Problema: Quer usar seu novo CRM mas não sabe como começar
- Alternativa: Fica perdido, volta para Salesforce (que conhece)
- Valor: Se conseguir primeira vitória, confia no sistema e fica

### Persona secundária
**Maria** — Sales Manager, 20-200 empresa
- Problema: Time novo não consegue onboarding rápido, requer suporte manual
- Alternativa: Maria gasta 2h treinar cada novo rep = custo operacional alto
- Valor: Self-onboarding reduz seu load e acelera time productivity

---

## 3. Solução

### Visão
Quando um usuário novo entra, vamos guiá-lo em 5 minutos através de um deal de exemplo, mostrando cada passo e validando que consegue fazer sozinho — criando primeira vitória e confiança no sistema.

### Features principais

#### Feature 1: Interactive Tutorial
- **O que faz**: Passo-a-passo guiado (modal + highlights) mostrando como criar um deal
- **Por quê**: User vê estrutura do produto enquanto faz
- **Sucesso parece**: User cria deal de exemplo em < 3 minutos
- **MVP**: 5 steps (deal name → stakeholders → deal value → timeline → save)

#### Feature 2: Validation e Encouragement
- **O que faz**: Após cada step, feedback positivo ("Great! You added a stakeholder")
- **Por quê**: Reinforça que user está no caminho certo
- **Sucesso parece**: User sente progresso e confiança
- **MVP**: Toast notifications com emojis ou checkmarks

#### Feature 3: Data Pre-fill (Optional)
- **O que faz**: Trazer deals já no sistema ou ofertar template de exemplo
- **Por quê**: Reduz ramp time, deixa real data in context
- **Sucesso parece**: User acredita que dados dele já estão ali
- **MVP**: Oferecer 3 deals de template (Tech, Retail, Service)

### Design principles
- Mobile-first (vendedor pode fazer no celular)
- Feedback imediato (user sabe que clicou certo)
- Progressão clara (% progresso visível)

### Escopo de exclusão
- Deep training em features avançadas — isso vem depois
- Integração com Salesforce sync — MVP é deal manual
- Custom fields — tutorial usa campos padrão

---

## 4. Métricas

| Métrica | Baseline | Target | Timeline |
|---------|----------|--------|----------|
| Churn em 7 dias | 35% | 15% | Month 1 |
| First deal creation rate | 30% | 80% | Month 1 |
| Time to first deal | 28 min | 5 min | Month 1 |
| Feature adoption | N/A | 70% of new users | Week 1 |
| NPS improvement | +2 | +8 | Month 1 |

Go-live criteria:
- ✅ Tutorial QA'd end-to-end
- ✅ Mobile responsive
- ✅ Performance < 2s load
- ✅ Rollout plan: beta (100 users) → 20% → 50% → 100%

---

## 5. Constraints

### Tech
- Must work on mobile (50% of signups)
- API calls must be < 500ms
- Needs analytics tracking (where did user drop off?)

### Timeline
Sair em 2 de Março (antes de trial cohort baterem 7 dias)

### Team
- PM: 2 days (spec review)
- Design: 3 days (wireframes + UX)
- Eng: 5 days (build + test)
- QA: 2 days

### Risk: Mobile performance
- Mitigação: Test on low-end devices early

---

## 6. Roadmap

### Phase 1: MVP (Jan 28 - Feb 10)
- Interactive tutorial (5 steps)
- Toast validation
- Template deals
- Analytics tracking

Go-live: Feb 11 (beta, 100 new users)

### Phase 2: Polish (Feb 11 - Feb 24)
- Bugs e performance fixes
- Mobile optimization
- Rollout to 20%, then 50%

### Phase 3: Expansion (Mar 1+)
If successful: Tutorial avançado para features como forecasting, integrations

---

## 7. Success em 30 dias

- 70%+ de new users fazem tutorial
- 60%+ deles criam deal na primeira vez
- Churn em 7 dias < 20% (from 35%)
- NPS of onboarded users = +8 vs -2 today

---

## Aprovação

| Role | Responsável | Status |
|------|-----------|--------|
| Product | Lucas | ☑ Approved |
| Engineering Lead | João | ⏳ Review |
| Design | Ana | ⏳ Review |
| Sales Dir. | Carlos | ⏳ For info |

Versão: 1.0
Última update: Jan 20, 2025
```

---

## Dicas

- **PRD é contrato**: Eng vai build a isso, design vai baseado nisso. Seja claro.
- **Métrica antes de tudo**: Se não sabe como medir sucesso, o PRD não está pronto.
- **Riscos são features não-ditas**: Se tem risco, há uma feature (ou teste) implícita.
- **Perguntas abertas são OK**: Melhor marcar incerteza agora que descobrir no meio do desenvolvimento.
