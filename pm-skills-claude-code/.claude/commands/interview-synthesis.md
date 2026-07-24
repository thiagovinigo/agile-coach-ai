# /interview-synthesis

## O que essa skill faz

Sintetiza transcrições de entrevistas em **JTBD**, **padrões comportamentais**, **problemas frequentes** e **recomendações acionáveis**.

Saída: **Síntese de entrevistas** com insights estruturados para informar descoberta ou PRD.

---

## Quando usar

- Rodou entrevistas e tem transcricao/notas
- Quer extrair padrões em vez de ler tudo manualmente
- Precisa priorizar problemas descobertos
- Vai referir insights em sync com stakeholders

---

## Input esperado

**Mínimo:**
- **Transcrições ou resumos** de 3+ entrevistas
- **Contexto**: Quem foi entrevistado (persona, rol), qual era a pergunta principal

**Opcional:**
- Dados de sessão (tempo gasto, features usadas)
- Feedback NPS ou CSAT
- Context sobre competidores mencionados

---

## Processo

1. **Extração de JTBD** — Identifica jobs, pains, gains para cada entrevistado
2. **Padrões** — Agrupa temas comuns em 3-5 clusters
3. **Problemas principais** — Ranking por frequência e severidade
4. **Recomendações** — Ações específicas (PRD, experimento, suporte)
5. **Evidência** — Quotes diretos das entrevistas para validar

---

## Output

```markdown
# Síntese de Entrevistas: [Tema]

## Respondentes
- 5 clientes de [segmento], usando produto há [X meses]
- Contexto: Entrevistados sobre [pergunta principal]

## Jobs to Be Done (JTBD)

### JTBD 1: [Job principal]
- **Contexto**: Quando [situação]
- **Job**: Eu quero [ação]
- **Outcome esperado**: Para que [resultado]
- **Frequência**: [X/5 entrevistados mencionaram]

### JTBD 2: [Job secundário]
- **Contexto**: [...]
- **Job**: [...]
- **Outcome esperado**: [...]
- **Frequência**: [X/5]

## Padrões comportamentais

### Padrão 1: [Behavior] (4/5 entrevistados)
- Descrição: O que observamos
- Contexto: Quando acontece
- Impacto: Consequência para produto
- Quote: "Frase direto de entrevistado"

### Padrão 2: [Behavior] (3/5 entrevistados)
- Descrição: [...]
- Contexto: [...]
- Impacto: [...]
- Quote: [...]

## Problemas descobertos (ranking por severidade)

| Problema | Severidade | Frequência | Impacto | Esforço para fix |
|----------|-----------|-----------|--------|-----------------|
| [P1] | Alta | 5/5 | [Churn, NPS, CAC] | [Estimado] |
| [P2] | Alta | 4/5 | [Impact] | [Estimado] |
| [P3] | Média | 3/5 | [Impact] | [Estimado] |
| [P4] | Baixa | 2/5 | [Impact] | [Estimado] |

## Recomendações

1. **Quick win** — [Problema P3]: Fazer [ação] em [timeline curta]
   - Evidência: [X/5 mencionou]
   - Impacto estimado: [X% melhoria em métrica]

2. **Medium priority** — [Problema P1]: Especificar [feature] para [PRD]
   - Evidência: [X/5 + JTBD: ...]
   - Impacto estimado: [X% redução em churn]
   - Próximo passo: Validar com mais dados (experimento ou entrevista com 10 clientes)

3. **Research needed** — [Problema P2]: Investigar [gap]
   - Evidência: [X/5 mencionou, mas não está claro]
   - Próximo passo: Session replay de [X usuários] ou entrevista focada

## Anexo: Quotes por tema

### "Falta de onboarding"
> "I spent 30 mins figuring out how to connect Salesforce. No guide, no tooltip." — Cliente A

> "Primeira coisa que fiz foi abrir um ticket com suporte porque não sabia por onde começar." — Cliente B

### "Performance em dados grandes"
> "Quando tenho > 10k leads, o sistema fica lento." — Cliente C

> "Report leva 5 minutos para carregar. Salesforce carrega em 1 segundo." — Cliente D
```

---

## Exemplo

**Input:**
```
/interview-synthesis

Transcrições: [5 entrevistas com usuários de CRM que desistiram após 7 dias]

Tema: Por que novos usuários não retornam
```

**Output:**
```markdown
# Síntese de Entrevistas: Churn em Onboarding de CRM

## Respondentes
- 5 usuários de PMEs (10-50 funcionários)
- Usaram produto entre 1-7 dias
- Contexto: Entrevistados após 30 dias de inatividade

## JTBD

### JTBD 1: Entender que dados já tenho no sistema
- **Contexto**: Quando você faz login pela primeira vez
- **Job**: Eu quero saber rápido que meus dados foram importados ou sync'ed
- **Outcome**: Para que saiba que posso contar com esse sistema como fonte de verdade
- **Frequência**: 5/5 (100%)

### JTBD 2: Fazer meu primeiro ação útil em < 5 minutos
- **Contexto**: Após entender que estou no lugar certo
- **Job**: Eu quero criar um lead ou completar uma tarefa simples
- **Outcome**: Para que sinta rápida vitória e volte amanhã
- **Frequência**: 4/5 (80%)

### JTBD 3: Ter confiança que dados não vão ser perdidos
- **Contexto**: Quando integro meu Salesforce
- **Job**: Eu quero ver claramente que sync funcionou
- **Outcome**: Para que não tenha medo de confiar no sistema e parar de usar Salesforce
- **Frequência**: 3/5 (60%)

## Padrões comportamentais

### Padrão 1: Primeira ação é investigação, não produção (5/5)
- **Descrição**: Todos os 5 usuários passaram os primeiros minutos explorando sem fazer nada útil
- **Contexto**: Após login, clicam em menus, leem descrições, mas não criam nada
- **Impacto**: Se exploração > 5 minutos sem wins, usuário sai (70% dos casos)
- **Quote**: "I spent 10 minutes just clicking around to understand where things are. I didn't feel like I was making progress."

### Padrão 2: Comparison com Salesforce é o baseline (4/5)
- **Descrição**: Todos mencionam Salesforce, Pipedrive ou HubSpot como comparação
- **Contexto**: Quando encontram diferenças na interface ou workflow
- **Impacto**: Diferenças negativas = motivo principal para parar de usar
- **Quote**: "In Salesforce, I would click here. This is different and I don't understand why."

### Padrão 3: Integração com Salesforce é frição (3/5)
- **Descrição**: Usuários que precisam sincronizar dados levam 20-30 minutos
- **Contexto**: Tentativa de importar leads do Salesforce
- **Impacto**: 3 dos 5 abriram ticket de suporte ou desistiram
- **Quote**: "I tried to sync my Salesforce but there were too many screens asking for permissions. I gave up."

## Problemas descobertos

| Problema | Severidade | Freq | Impacto | Esforço |
|----------|-----------|------|--------|---------|
| Sem guia de first actions | Alta | 5/5 | 35% churn | 1-2 sem |
| Integração Salesforce é complexa | Alta | 3/5 | 15% churn | 2-3 sem |
| UI é diferente de competitors | Média | 4/5 | Cognição lenta | Design |
| Falta feedback de sync | Média | 3/5 | Desconfiança | 3-5 dias |

## Recomendações

1. **Quick win** — Adicionar visual claro que dados foram sincronizados
   - Evidência: 3/5 mencionaram desconfiança pós-sync
   - Impacto: ~5-10% redução em churn (se combinado com #2)
   - Esforço: 3-5 dias eng + design

2. **Medium priority** — Redesenhar fluxo de first actions (tutorial interativo ou demo rápida)
   - Evidência: 5/5 mencionaram exploração sem progresso
   - Impacto: ~15-20% redução em churn
   - Próximo passo: /prd para "Guided first experience" ou A/B test com 10 clientes

3. **Medium priority** — Simplificar integração Salesforce (reduce permission screens)
   - Evidência: 3/5 abriram ticket ou desistiram
   - Impacto: ~10% redução em churn para segmento Salesforce
   - Próximo passo: Tech discovery com eng sobre arquitetura de OAuth

4. **Research** — Investigar por que UI é diferente (design system debt?)
   - Evidência: 4/5 compararam com competitors
   - Próximo passo: Design audit + session replay de onde ocorrem clicks confusos
```

---

## Dicas

- **Frequência importa**: "1/5 mencionou" é sinal de outlier, não padrão. Use para priorizar.
- **JTBD vs. solução**: Se entrevistado disse "precisa de tutorial", extraia o JTBD ("entender como começar") e a evidência separadas.
- **Quotes são ouro**: Salve para apresentações e PRDs. Humanizam dados.
- **Conflito = pesquisa**: Se entrevistados discordam, há segmento aqui — explore com mais entrevistas.
