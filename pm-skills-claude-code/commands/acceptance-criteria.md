# /acceptance-criteria

## O que essa skill faz

Gera critérios de aceite estruturados em formato **Given/When/Then** (Gherkin) cobrindo happy path, edge cases, e casos de erro.

Saída: **5-10 cenários** prontos para QA e eng usarem como test cases.

---

## Quando usar

- User story aprovada, precisa detalhar validações
- Vai passar para QA — precisa ter explícito o que testar
- Feature tem regras de negócio complexas

---

## Input esperado

**Mínimo:**
- **Feature ou user story**: O que está sendo testado
- **Regras de negócio**: Constraints, validações, edge cases
- **Contexto**: Que dados já existem

**Opcional:**
- Design mockup (para validações visuais)
- Casos de erro conhecidos
- Performance requirements

---

## Processo

1. **Happy path** — Fluxo ideal, tudo certo
2. **Edge cases** — Variações que são válidas mas diferentes
3. **Error cases** — Entradas inválidas, o que fazer?
4. **Performance/Scale** — Se relevante, como se comporta em volume?
5. **Accessibility** — Pode ser usado por screenreader?

---

## Output

```markdown
# Acceptance Criteria: [Feature Name]

## Cenário 1: Happy Path — [Descrição]

```gherkin
Given que [pré-condição/contexto inicial]
When [ação do usuário]
Then [resultado esperado]
  And [validação adicional]
  And [outra validação]
```

### Notas para QA
- [Se há screenshot esperada, descreva]
- [Se há performance expectativa, mencione]
- [Qualquer detalhe visual importante]

---

## Cenário 2: Happy Path Alternativo — [Variação]

```gherkin
Given que [contexto diferente do cenário 1]
When [ação similar]
Then [resultado diferente]
```

### Notas para QA
[...]

---

## Cenário 3: Edge Case — [Situação limite]

```gherkin
Given que [contexto especial]
When [ação que toca limite]
Then [comportamento esperado para limite]
```

---

## Cenário 4: Error — [Erro esperado]

```gherkin
Given que [contexto que leva a erro]
When [ação que causa erro]
Then [mensagem de erro clara é mostrada]
  And [campo fica highlighted]
  And [user pode corrigir facilmente]
```

---

## Cenário 5...N
[Mesmo formato]

---

## Casos de teste por categoria

### Validação de entrada
- [ ] Campo vazio
- [ ] String muito longa
- [ ] Caracteres especiais
- [ ] Números onde esperado texto

### Fluxo de negócio
- [ ] Happy path completo
- [ ] Cancelamento/Back
- [ ] Reentrar dados
- [ ] Dados pré-populados

### Estado do sistema
- [ ] Primeira vez usando feature
- [ ] Segunda vez (dados existem)
- [ ] Com dados muito antigos
- [ ] Em volume alto (performance)

### Integração
- [ ] Com outros módulos
- [ ] Com dados de terceiros (API)
- [ ] Efeitos colaterais (emails, webhooks)

### Acessibilidade
- [ ] Navegável via tab/keyboard
- [ ] Legível com screenreader
- [ ] Contraste adequate
- [ ] Mobile responsivo

---

## Definição de Pronto

Feature está aceita quando:
- ✅ Todos os cenários passaram (manual ou automatizado)
- ✅ Sem erros em console/logs
- ✅ Performance dentro da spec
- ✅ Mobile funcionando
- ✅ PM fez sign-off em staging
```

---

## Exemplo

**Input:**
```
/acceptance-criteria
Feature: Add Deal Name (Story 2 de tutorial)
Regra: Deal name é obrigatório, máx 100 chars, trim whitespace
Contexto: User está no passo 1 do tutorial
```

**Output:**
```markdown
# Acceptance Criteria: Deal Name Input (Tutorial Step 1)

## Cenário 1: Happy Path — Digitar nome válido

```gherkin
Given que estou no passo 1 do tutorial com modal "Add deal name"
When digito "Acme Inc - $50k contract"
And clico botão "Next"
Then vejo toast verde com checkmark ✓
  And mensagem diz "Great! You added a deal"
  And toast desaparece após 2 segundos
  And avanço para próximo passo (Story 2 - Stakeholders)
  And nome foi salvo em session do usuário
```

### Notas para QA
- Verificar que toast aparece no canto certo (mobile: bottom-right, desktop: top-center)
- Validar que animation é smooth (não é jumpy)

---

## Cenário 2: Happy Path com Espaços Extras

```gherkin
Given que clico no campo "Deal name"
When digito "   Acme Inc   " (com espaços no inicio e fim)
And clico "Next"
Then o nome é salvo como "Acme Inc" (trimmed)
  And vejo toast de sucesso
  And validação passa (não é visto como vazio)
```

### Notas para QA
- Verificar que trim é aplicado — não pode gerar edge case depois

---

## Cenário 3: Campo Vazio — Erro esperado

```gherkin
Given que vejo modal "Add deal name"
When não digito nada
And clico "Next"
Then vejo erro "Deal name é obrigatório"
  And campo fica com borda RED
  And botão "Next" fica disabled/grayed
  And toast vermelho aparece com ⚠️ icon
  And permaneço no mesmo passo (não avanço)
```

### Notas para QA
- Erro deve desaparecer quando user começa a digitar algo
- Verificar que foco automático volta para o campo

---

## Cenário 4: Somente Espaços — Edge Case

```gherkin
Given que vejo campo "Deal name"
When digito "     " (só espaços)
And clico "Next"
Then validação falha (espaços trim para vazio)
  And vejo erro "Deal name é obrigatório"
  And mesmo comportamento que Cenário 3
```

---

## Cenário 5: Máximo de Caracteres (100)

```gherkin
Given que vejo campo "Deal name"
When digito exatamente 100 caracteres válidos
And clico "Next"
Then aceiota validação passa
  And vejo sucesso
```

```gherkin
Given que vejo campo "Deal name"
When digito 101 caracteres
And clico "Next"
Then validação falha
  And vejo erro "Máximo 100 caracteres"
  And mostra contador "101/100" em vermelho
```

### Notas para QA
- Verificar que user NÃO consegue digitar mais que 100 (input deve estar limitado)
- Ou aceita digitar mas error aparece? (Preferência de design)

---

## Cenário 6: Caracteres Especiais — Edge Case

```gherkin
Given que vejo campo "Deal name"
When digito "Acme & Co. [2024] — $50k (Deal)"
And clico "Next"
Then validação passa (caracteres especiais são OK)
  And vejo sucesso
  And nome é salvo exatamente como digitado
```

---

## Cenário 7: Mobile — Responsivo

```gherkin
Given que abro tutorial em mobile (iPhone, < 600px width)
When vejo campo "Deal name" em modal
Then campo é full-width (não transborda)
  And keyboard aparece automaticamente
  And botão "Next" é tapable (> 48px height)
  And mensagem de erro é legível (não é cut off)
```

### Notas para QA
- Testar em iOS Safari e Android Chrome
- Verificar que modal não bloqueia keyboard

---

## Cenário 8: Acessibilidade — Keyboard Navigation

```gherkin
Given que uso teclado para navegar (tab)
When dou tab até campo "Deal name"
Then campo recebe focus (outline visível)
  And consigo digitar

Given que estou digitando no campo
When pressiono "Enter"
Then funciona como clicar "Next" (submit form)

Given que pressiono "Escape"
Then modal fecha (user pode sair)
```

### Notas para QA
- Verificar focus outline contrast (WCAG standard)
- Screenreader deve ler label + error message

---

## Cenário 9: Pré-preenchido (Se aplicável)

```gherkin
Given que voltei ao tutorial após interruption
And havia salvo "Acme Inc" antes
When vejo modal novamente
Then campo "Deal name" já tem "Acme Inc" (não foi perdido)
  And posso editar ou continuar
```

---

## Cenário 10: Performance

```gherkin
Given que tenho slow network (3G)
When digito texto no campo
Then validação é instantânea (não há lag)
  And clico "Next"
Then resposta chegou em < 2 segundos
  And toast aparece (UX não sente lento)
```

### Notas para QA
- Testar com DevTools throttling (3G)
- Verificar que não há cascata de request (validate on every keystroke = bad)

---

## Matriz de Casos

| Cenário | Entrada | Esperado | Status |
|---------|---------|----------|--------|
| 1. Happy path | "Acme Inc - $50k" | Sucesso | ⏳ QA |
| 2. Com espaços | "  Acme Inc  " | Sucesso (trimmed) | ⏳ QA |
| 3. Campo vazio | "" | Erro obrigatório | ⏳ QA |
| 4. Só espaços | "     " | Erro obrigatório | ⏳ QA |
| 5. 100 chars | "A"*100 | Sucesso | ⏳ QA |
| 6. 101 chars | "A"*101 | Erro limite | ⏳ QA |
| 7. Especiais | "Acme & Co [2024]" | Sucesso | ⏳ QA |
| 8. Mobile | Testado em <600px | Full-width, tapable | ⏳ QA |
| 9. Keyboard | Tab + Enter | Navegável | ⏳ QA |
| 10. Pre-filled | Voltar após save | Dados mantidos | ⏳ QA |

---

## Sign-off

- [ ] QA: Todos os cenários passaram
- [ ] Eng: Nenhum erro em logs
- [ ] PM: Validado em staging
- [ ] Data de aprovação: ___________
```

---

## Dicas

- **Gherkin é linguagem, não pseudo-código**: "Given que X When Y Then Z" é sintaxe BDD — eng consegue virar em teste automatizado.
- **Um cenário = um test case**: Se tem 10 cenários, vai ter 10 testes.
- **Edge cases vêm de descoberta**: Se descoberta mencionou "deal com caracteres especiais", aqui vira teste.
- **QA como primeiro usuário**: Se QA consegue entender AC, sig outros vão conseguir também.
