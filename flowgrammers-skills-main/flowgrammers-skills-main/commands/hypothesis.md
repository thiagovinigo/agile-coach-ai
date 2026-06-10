# /hypothesis

## O que essa skill faz

Gera uma hipótese testável e estruturada com métricas de sucesso, avaliação de risco em 4 categorias (Value, Usability, Viability, Feasibility) e plano de validação. Transforma intuições vagas em statements falsificáveis com kill criteria.

Saída: **Hypothesis card** completa — pronta para alinhar o time e desenhar experimento.

---

## Quando usar

- Tem uma ideia de feature e quer validar antes de construir
- Precisa estruturar o pensamento antes de pedir recursos ao time
- Quer definir critérios claros de sucesso e fracasso antes de começar
- Está usando Opportunity Solution Tree e precisa formalizar a hypothesis de uma solução
- Quer evitar o viés de confirmação — definir o que te faria desistir ANTES de testar

---

## Input esperado

**Mínimo:**
- **Ideia/mudança proposta**: O que quer fazer ou mudar
- **Usuário-alvo**: Quem será impactado
- **Problema que resolve**: Qual dor ou necessidade endereça

**Opcional:**
- Dados de discovery (entrevistas, analytics)
- Baseline atual da métrica
- Constraints (timeline, budget, capacidade técnica)
- Experimentos anteriores relacionados
- Opportunity Solution Tree (se já existe)

---

## Processo

1. **Formular a crença (Belief)** — Escrever a hipótese no formato: "Acreditamos que [ação/mudança] para [usuário-alvo] vai [resultado esperado] medido por [métrica] atingindo [target] em [prazo]." A hipótese DEVE ser falsificável — se qualquer resultado confirma, não é hipótese.

2. **Especificar o usuário-alvo** — Definir segmento específico, não "usuários". Incluir: quem é, qual o contexto, por que esse grupo especificamente. Quanto mais específico, mais útil o teste.

3. **Definir resultado esperado** — Descrever a mudança de comportamento do usuário (não métrica interna). Ex: "usuários vão completar onboarding" em vez de "vamos reduzir churn". O comportamento causa a métrica, não o contrário.

4. **Estabelecer métricas de sucesso** — Definir 3 tipos:
   - **Primary metric**: A métrica principal que a hipótese move
   - **Secondary metric**: Métrica complementar que confirma o mecanismo
   - **Guardrail metric**: Métrica que NÃO pode piorar (efeito colateral)

5. **Avaliar riscos em 4 categorias** — Para cada categoria, identificar a assumption principal e classificar risco (High/Medium/Low):
   - **Value**: O usuário quer isso? Resolve uma dor real?
   - **Usability**: O usuário consegue usar? Entende como funciona?
   - **Viability**: O negócio sustenta? Modelo de negócio funciona?
   - **Feasibility**: Eng consegue construir? No prazo? Com a stack atual?

6. **Descrever abordagem de validação** — Definir método (A/B test, protótipo, fake door, concierge, survey), tamanho de amostra, duração e critério de significância estatística quando aplicável.

7. **Definir kill criteria** — Especificar condições que fariam abandonar a hipótese. Isso é o mais importante e o mais ignorado. Se não tem kill criteria, você vai racionalizar qualquer resultado como sucesso.

---

## Output

```markdown
# Hypothesis Card

## Hipótese

> Acreditamos que **[ação/mudança]**
> para **[usuário-alvo específico]**
> vai **[resultado esperado — comportamento do usuário]**
> medido por **[métrica primária]**
> atingindo **[target numérico]**
> em **[prazo]**.

---

## Contexto

**Problema que endereça:**
[Descrição do problema, com evidências]

**Evidências que suportam:**
- [Dado 1: entrevista, analytics, benchmark]
- [Dado 2]
- [Dado 3]

**Confiança inicial:** [High / Medium / Low]
**Razão da confiança:** [Por que esse nível]

---

## Usuário-Alvo

**Segmento:** [Descrição específica]
**Tamanho do segmento:** [Número estimado de usuários]
**Contexto:** [Quando e onde esse usuário encontra o problema]
**Por que esse segmento:** [Razão para começar por esse grupo]

---

## Métricas de Sucesso

### Primary Metric
| Métrica | Baseline | Target | Prazo |
|---------|----------|--------|-------|
| [Nome da métrica] | [Valor atual] | [Valor desejado] | [Timeframe] |

### Secondary Metric
| Métrica | Baseline | Expectativa |
|---------|----------|-------------|
| [Métrica que confirma o mecanismo] | [Valor atual] | [Direção esperada] |

### Guardrail Metric
| Métrica | Valor Atual | Limite Aceitável |
|---------|-------------|------------------|
| [Métrica que NÃO pode piorar] | [Valor] | [Mínimo aceitável] |

---

## Risk Assessment

### Matriz de Risco

| Categoria | Assumption Principal | Risco | Evidência |
|-----------|---------------------|-------|-----------|
| **Value** | [O usuário quer isso?] | [H/M/L] | [O que sabemos] |
| **Usability** | [O usuário consegue usar?] | [H/M/L] | [O que sabemos] |
| **Viability** | [O negócio sustenta?] | [H/M/L] | [O que sabemos] |
| **Feasibility** | [Eng consegue construir?] | [H/M/L] | [O que sabemos] |

**Risco mais crítico:** [Qual categoria] — [Por quê]
**Ação para mitigar:** [O que fazer primeiro]

---

## Plano de Validação

**Método:** [A/B test / Protótipo / Fake door / Concierge / Survey / Entrevista]
**Descrição:** [Como o teste vai funcionar]
**Amostra:** [Tamanho e critérios de seleção]
**Duração:** [Período do teste]
**Responsável:** [Quem executa]
**Custo estimado:** [Horas/budget]

### Timeline

| Semana | Atividade |
|--------|-----------|
| 1 | [Setup / Preparação] |
| 2 | [Execução do teste] |
| 3 | [Coleta e análise] |
| 4 | [Decisão: prosseguir / pivotar / abandonar] |

---

## Kill Criteria

**Abandonar a hipótese se:**
- [ ] [Condição 1 — métrica abaixo de X]
- [ ] [Condição 2 — efeito colateral Y]
- [ ] [Condição 3 — prazo Z estourado sem resultado]

**Pivotar se:**
- [ ] [Condição que sugere ajuste em vez de abandono]

**Prosseguir para build se:**
- [ ] [Todas as condições de sucesso atingidas]
- [ ] [Guardrail metrics dentro do aceitável]

---

## Decision Log

| Data | Decisão | Razão | Próximo passo |
|------|---------|-------|---------------|
| [Data] | [Decisão tomada] | [Baseado em quê] | [Ação] |
```

---

## Exemplo

**Input:**
> Ideia: Adicionar tutorial de onboarding interativo para novos sales reps. Produto: CRM B2B mid-market. Problema: 70% dos novos usuários não completam nenhuma ação significativa no dia 1. Temos dados de 12 entrevistas e analytics de funil.

**Output:**

```markdown
# Hypothesis Card

## Hipótese

> Acreditamos que **adicionar um tutorial de onboarding interativo com checklist de 5 passos**
> para **novos sales reps que fazem signup no CRM (primeiros 100 dias de conta)**
> vai **aumentar a taxa de completar a primeira ação significativa (criar deal + contato) no dia 1**
> medido por **Day-1 Activation Rate**
> atingindo **50% (vs. baseline de 30%)**
> em **8 semanas após lançamento**.

---

## Contexto

**Problema que endereça:**
70% dos novos usuários não completam nenhuma ação significativa no dia 1. Correlação forte entre ação no dia 1 e retenção de 7 dias (reps que criam ≥1 deal no D1 têm 3x mais retenção).

**Evidências que suportam:**
- 9 de 12 entrevistados mencionaram "não saber por onde começar" como frustração principal
- Analytics: 45% dos novos reps não clicam em nada nos primeiros 10 minutos
- Heatmap mostra que reps ficam na home sem navegar — paralisia de escolha
- Benchmark: CRMs concorrentes com onboarding guiado reportam 50-65% Day-1 activation

**Confiança inicial:** Medium
**Razão da confiança:** Evidência qualitativa forte (9/12 entrevistas), mas não testamos se a solução específica (checklist) resolve. O problema é validado, a solução não.

---

## Usuário-Alvo

**Segmento:** Novos sales reps (SDRs e AEs) em empresas mid-market (50-500 funcionários) que estão migrando de outro CRM ou usando CRM pela primeira vez.
**Tamanho do segmento:** ~800 novos signups/mês nesse perfil
**Contexto:** Primeiro login no CRM, geralmente na primeira semana no novo emprego ou após decisão de migração do gestor.
**Por que esse segmento:** Maior volume de novos usuários + maior drop-off no Day 1. Se resolver para esse grupo, impacto direto na retenção overall.

---

## Métricas de Sucesso

### Primary Metric
| Métrica | Baseline | Target | Prazo |
|---------|----------|--------|-------|
| Day-1 Activation Rate (% que cria ≥1 deal + ≥1 contato no D1) | 30% | 50% | 8 semanas |

### Secondary Metric
| Métrica | Baseline | Expectativa |
|---------|----------|-------------|
| Checklist completion rate | N/A (novo) | ≥ 60% completam todos os 5 passos |
| Time-to-first-action | 47 min (mediana) | ≤ 15 min |

### Guardrail Metric
| Métrica | Valor Atual | Limite Aceitável |
|---------|-------------|------------------|
| Signup-to-trial conversion | 22% | Não pode cair abaixo de 20% |
| Support ticket volume (onboarding) | 45/semana | Não pode subir acima de 55/semana |

---

## Risk Assessment

### Matriz de Risco

| Categoria | Assumption Principal | Risco | Evidência |
|-----------|---------------------|-------|-----------|
| **Value** | Reps querem ser guiados (vs. explorar sozinhos) | Medium | 9/12 pediram guia, mas 3 disseram preferir "fuçar". Pode precisar de opt-out. |
| **Usability** | Checklist de 5 passos é intuitivo e não confunde | Medium | Não testamos o flow ainda. Reps variam muito em tech-savviness. |
| **Viability** | Tutorial não aumenta custo de suporte | Low | Espera-se reduzir tickets, não aumentar. |
| **Feasibility** | Eng consegue implementar checklist interativo em 2 sprints | Low | Tech Lead confirmou — componentes reutilizáveis do design system existem. |

**Risco mais crítico:** Value — Se uma parcela significativa dos reps não quiser onboarding guiado, o checklist pode ser ignorado ou gerar frustração.
**Ação para mitigar:** Testar com protótipo antes de construir. Incluir opção "Pular tutorial" visível.

---

## Plano de Validação

**Método:** Protótipo + teste de usabilidade moderado
**Descrição:** Criar protótipo em Figma do checklist de onboarding. Testar com 8 novos reps em sessões de 30 min. Observar: completam os passos? Onde travam? Pulam? Depois, se protótipo validar, A/B test em produção com 50% dos novos signups.
**Amostra:** Fase 1: 8 reps (teste qualitativo). Fase 2: 400 novos signups por grupo (A/B test).
**Duração:** Fase 1: 2 semanas. Fase 2: 4 semanas.
**Responsável:** PM (Rafael) + Designer (Ana) + Pesquisadora (Julia)
**Custo estimado:** Fase 1: 40h. Fase 2: 60h de eng + 20h de análise.

### Timeline

| Semana | Atividade |
|--------|-----------|
| 1 | Designer cria protótipo. PM recruta 8 reps para teste. |
| 2 | Testes de usabilidade (4 sessões de 30 min). Análise. |
| 3 | Go/No-Go. Se go: eng implementa + setup A/B test. |
| 4-5 | Eng implementa checklist no produto. |
| 6-9 | A/B test rodando (4 semanas, 400 por grupo). |
| 10 | Análise final. Decisão: roll out / pivotar / kill. |

---

## Kill Criteria

**Abandonar a hipótese se:**
- [ ] Day-1 Activation Rate não atinge 40% (mínimo) após 4 semanas de A/B test
- [ ] Mais de 70% dos reps pulam o tutorial sem completar nenhum passo
- [ ] Support tickets aumentam mais de 30% no grupo de teste

**Pivotar se:**
- [ ] Activation melhora mas não atinge 50% — considerar ajustar o checklist (menos passos, conteúdo diferente)
- [ ] Reps completam checklist mas não retêm no D7 — problema pode não ser onboarding

**Prosseguir para build se:**
- [ ] Day-1 Activation ≥ 50% no grupo de teste
- [ ] Checklist completion ≥ 60%
- [ ] Guardrail metrics dentro do aceitável
- [ ] Feedback qualitativo positivo (≥ 4/5 satisfação)

---

## Decision Log

| Data | Decisão | Razão | Próximo passo |
|------|---------|-------|---------------|
| [Data] | Iniciar Fase 1 (protótipo) | Evidência qualitativa forte, risco baixo de investimento | Recrutar reps para teste |
```

---

## Dicas

- **Hipótese NÃO é statement de solução.** "Vamos adicionar onboarding" não é hipótese. "Acreditamos que onboarding guiado vai aumentar activation de 30% para 50%" é hipótese. A diferença é a falsificabilidade.
- **Sempre defina kill criteria ANTES de testar.** Se definir depois, vai racionalizar o resultado. O viés de confirmação é o inimigo número 1 de discovery.
- **Guardrail metrics salvam carreiras.** Você pode dobrar activation e destruir conversão de signup. Sem guardrail, descobre tarde demais.
- **Confiança "High" sem dados primários é mentira.** Se não falou com usuários reais, sua confiança é Medium no máximo. Seja honesto — isso guia onde investir pesquisa.
