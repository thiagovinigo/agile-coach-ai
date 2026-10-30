# /user-stories

## O que essa skill faz

Gera user stories no formato Mike Cohn com critérios de aceite, aplicando princípio INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable).

Saída: **5-8 user stories estruturadas** prontas para eng estimar e implementar.

---

## Quando usar

- Tem PRD aprovado e precisa quebrar em stories para eng
- Vai criar sprint backlog
- Precisa conversa clara entre PM e dev sobre escopo

---

## Input esperado

**Mínimo:**
- **PRD ou feature description**: Contexto completo
- **Personas**: Quem usa cada feature
- **Features principais**: O que cada story cobre

**Opcional:**
- Designs mockups (para contextualizar)
- Métricas (para priorizar)
- Constraints técnicas

---

## Processo

1. **Quebra de features em stories** — Cada feature = 1-2 stories, cada story = 2-5 dias eng
2. **Formato INVEST** — Cada story é independente mas encadeável
3. **Critérios de aceite** — Given/When/Then + casos de edge
4. **Aceitação de prioridade** — Qual story primeira?
5. **Estimativas** — Pede para eng, mas estrutura ajuda

---

## Output

```markdown
# User Stories: [Feature Name]

## Priorização

| # | Story | Prioridade | Razão |
|---|-------|-----------|-------|
| 1 | [Story 1] | P0 | User não consegue começar sem isso |
| 2 | [Story 2] | P0 | Blocka story 1 |
| 3 | [Story 3] | P1 | Nice-to-have para MVP |

---

## Story 1: [Nome claro do user goal]

**Como um** [Persona]
**Eu quero** [Ação clara]
**Para que** [Resultado/Valor]

### Contexto
[Uma frase sobre por que isso importa. Vindo de descoberta/PRD.]

### Critérios de Aceite

#### Happy path
```gherkin
Given que [pré-condição]
When [ação do usuário]
Then [resultado esperado]
```

#### Edge case 1
```gherkin
Given que [variação]
When [ação similar]
Then [resultado diferente]
```

#### Edge case 2
```gherkin
Given que [variação 2]
When [ação similar]
Then [resultado diferente]
```

### Notas técnicas
- [Restrição de implementação, se souber]
- [Integração necessária]
- [Performance requirement]

### Tamanho estimado
[Solicitar de eng durante refinement — esse formato ajuda a estimar mais rápido]

### Dependências
- Precisa de [Story X] ou [Ferramenta Y]

---

## Story 2: [Nome claro do user goal]

**Como um** [Persona]
**Eu quero** [...]
**Para que** [...]

### Contexto
[...]

### Critérios de Aceite

#### Happy path
```gherkin
Given que [...]
When [...]
Then [...]
```

#### Edge cases
[...]

### Notas técnicas
[...]

### Tamanho estimado
[...]

### Dependências
[...]

---

## Story 3...N
[Mesmo formato]

---

## Roadmap de Stories (sugestão de sequência)

### Sprint 1 (Semana 1)
1. Story 1
2. Story 2

### Sprint 2 (Semana 2)
1. Story 3
2. Story 4

### Sprint 3 (Semana 3+)
1. Story 5
2. (Se sobrou time) Story 6

---

## Definição de Done

Para uma story ser considerada feita:
- ✅ Critérios de aceite passaram em manual testing
- ✅ Code review aprovado
- ✅ Integrado em staging
- ✅ QA testou happy path + principais edge cases
- ✅ Documentado (se applicable)
- ✅ PM validou em staging

---

## Notas para eng

1. **Critérios de aceite são contrato**: Se algo não está lá, não é responsabilidade de eng
2. **"Para que" importa**: Ajuda eng a tomar decisões criativas dentro do escopo
3. **Edge cases são reais**: Vieram de descoberta ou são padrão do domínio
4. **Perguntas abertas? Avisar PM agora**: Melhor clarificar que descobrir no meio do build
```

---

## Exemplo

**Input:**
```
/user-stories
PRD: Guided First Deal Experience
Personas: Alex (Sales Rep), Maria (Sales Manager)
Features: Interactive tutorial, Validation, Template deals
```

**Output:**
```markdown
# User Stories: Guided First Deal Experience

## Priorização

| # | Story | Prioridade | Razão |
|---|-------|-----------|-------|
| 1 | Launch tutorial modal | P0 | User vê logo que entra |
| 2 | Guided step 1 (Deal name) | P0 | Core do MVP |
| 3 | Guided step 2 (Stakeholders) | P0 | Sem isso, deal é incompleto |
| 4 | Validation toasts | P0 | UX critical para percepção de sucesso |
| 5 | Skip tutorial button | P1 | Power users querem pular |
| 6 | Analytics tracking | P1 | Precisa saber onde user abandona |
| 7 | Mobile responsive | P1 | 50% de users vêm mobile |

---

## Story 1: Exibir tutorial ao fazer login

**Como um** Sales Rep novo
**Eu quero** ver um guia no meu primeiro login
**Para que** saiba que o sistema vai me ajudar a começar

### Contexto
70% de new users não sabem como começar. Seu primeiro encontro com o sistema é crítico para retenção.

### Critérios de Aceite

#### Happy path
```gherkin
Given que sou um novo usuário fazendo login pela primeira vez
When entro na dashboard
Then vejo um modal titled "Crie seu primeiro deal em 5 minutos"
And botão "Start Tutorial" é proeminente
And botão "Skip" é discreto
```

#### Edge case: User voltou después de skip
```gherkin
Given que fiz skip no tutorial
When entro de novo
Then não vejo modal novamente (remembered)
```

#### Edge case: User com deals antigos
```gherkin
Given que tenho 2+ deals já no sistema
When faço login
Then NÃO vejo tutorial (já sei usar)
```

### Notas técnicas
- Modal deve ser centro da tela, responsive para mobile
- Usar feature flag: `tutorial_enabled` (para desligar se bugado)
- Salvar em user.has_seen_tutorial para não repetir

### Tamanho estimado
[Eng: ~1 dia]

### Dependências
Nenhuma

---

## Story 2: Passo 1 do tutorial (Deal name)

**Como um** Sales Rep novo
**Eu quero** criar um deal com um nome
**Para que** comece a organizar meus deals

### Contexto
Primeiro passo é supertanto: dar nome. Vamos validar que consegue fazer o mais básico.

### Critérios de Aceite

#### Happy path
```gherkin
Given que estou no tutorial (Story 1 completo)
When digito "Acme Inc - $50k deal" no campo "Deal Name"
And clico "Next"
Then vejo toast verde "Great! You added a deal" com checkmark
And passo para Story 3 (Stakeholders)
```

#### Edge case: Sem nome
```gherkin
Given que não digitei nada
When clico "Next"
Then vejo erro "Deal name é obrigatório"
And campo fica vermelho
```

#### Edge case: Nome muito longo
```gherkin
Given que digito 200+ caracteres
When clico "Next"
Then vejo erro "Máximo 100 caracteres"
```

### Notas técnicas
- Campo "Deal Name" já existe, apenas estilizar para tutorial
- Toast deve desaparecer após 2 segundos
- Salvar input em sessão do user (ainda não commit to DB)

### Tamanho estimado
[Eng: ~1 dia]

### Dependências
Story 1

---

## Story 3: Passo 2 do tutorial (Stakeholders)

**Como um** Sales Rep novo
**Eu quero** adicionar alguém ao deal (stakeholder/contact)
**Para que** saiba como colaborar com meu time

### Contexto
Segundo passo mostra collaboration. Vamos deixar rápido e simples.

### Critérios de Aceite

#### Happy path
```gherkin
Given que finalizei passo 1 com deal "Acme Inc"
When vejo campo "Add stakeholder" com sugestão de contatos
And clico em "John Smith" (contato fictício pré-criado)
Then vejo checkmark e toast "Added John! Great job"
And posso adicionar mais ou prosseguir
```

#### Edge case: Adicionar stakeholder que não existe
```gherkin
Given que digito "novo@acme.com"
When clico "Add"
Then vejo toast "Você pode convidar contatos depois"
And não bloqueia progression
```

#### Edge case: Mobile
```gherkin
Given que estou em mobile (< 600px)
When vejo campo "Add stakeholder"
Then campo é tappable, dropdown é acessível
```

### Notas técnicas
- Usar contatos já no sistema de user (pre-load via API)
- Se não tem contatos, oferecer button "Add manually later"
- Não validar emails aqui, aceitar qualquer string

### Tamanho estimado
[Eng: ~2 dias]

### Dependências
Story 2

---

## Story 4: Validation toasts

**Como um** Sales Rep novo
**Eu quero** receber feedback que minha ação funcionou
**Para que** saiba que estou no caminho certo

### Contexto
Psychologically, users precisam de feedback imediato. Sem isso, sentem que estão perdidos.

### Critérios de Aceite

#### Happy path: Deal name
```gherkin
Given que entro com deal name válido
When clico "Next"
Then vejo toast with:
  - Emoji (✓ ou 🎉)
  - Mensagem "Great! You added a deal"
  - Auto-hide após 2 segundos
```

#### Happy path: Stakeholder
```gherkin
Given que adicio um stakeholder
When confirmo
Then vejo toast "Added John! Great job"
```

#### Edge case: Error toast (nome vazio)
```gherkin
Given que clico next sem preencher
When validação falha
Then vejo toast RED with "Deal name é obrigatório"
And fica 4 segundos (mais tempo para ler erro)
```

### Notas técnicas
- Toast componente reutilizável
- Usar design system colors (success green, error red)
- Posicionar em bottom-right mobile, top-center desktop

### Tamanho estimado
[Eng: ~1 dia]

### Dependências
Stories 2 e 3

---

## Story 5: Skip button + remember

**Como um** Power User
**Eu quero** poder pular o tutorial na primeira vez
**Para que** não seja obrigado a ver algo que já sei

### Contexto
Nem todos são new users reais (alguns já usaram CRM antes). Dar opção de skip.

### Critérios de Aceite

#### Happy path
```gherkin
Given que vejo o tutorial
When clico botão "Skip"
Then modal desaparece
And entro direto no CRM normal
And não vejo tutorial novamente nesse usuário
```

#### Edge case: Voltar depois
```gherkin
Given que skipped antes
When faço logout e login de novo
Then NÃO vejo tutorial (remembered)
```

### Notas técnicas
- Salvar `user.tutorial_skipped = true`
- Botão "Skip" é pequeno, texto em gray (não incentiva)

### Tamanho estimado
[Eng: ~1 dia]

### Dependências
Story 1

---

## Story 6: Analytics tracking

**Como um** PM
**Eu quero** saber onde users abandonam o tutorial
**Para que** posso melhorar partes que não funcionam

### Contexto
Métrica crítica: completion rate. Precisa saber em qual passo users saem.

### Critérios de Aceite

#### Happy path: Evento quando tutorial inicia
```
Event: tutorial_started
- user_id
- timestamp
- platform (web/mobile)
```

#### Happy path: Evento para cada step completo
```
Event: tutorial_step_completed
- user_id
- step (1,2,3,...)
- timestamp
- time_spent_on_step
```

#### Happy path: Evento quando abandona
```
Event: tutorial_abandoned
- user_id
- step_at (em qual step saiu)
- reason (skip/close/error)
```

### Notas técnicas
- Usar existing analytics library (Segment, Mixpanel, etc)
- Não bloqueiar UX se analytics falha
- Testar no dev antes de go-live

### Tamanho estimado
[Eng: ~1 dia]

### Dependências
Nenhuma (paralelo com outras stories)

---

## Sequência Sugerida para Sprint

### Sprint 1 (1 semana)
- Story 1: Tutorial modal (D1)
- Story 2: Deal name step (D1)
- Story 4: Validation toasts (D1)
Total: ~3 dias = 60% de velocidade

### Sprint 2 (1 semana)
- Story 3: Stakeholders step (D2)
- Story 5: Skip button (D1)
- Story 6: Analytics (D1)
Total: ~4 dias = 80% de velocidade

### Post-MVP
- Story 7: Mobile responsive polish
- Story 8: Mais steps (deal value, timeline)

---

## Definição de Done

Para "Story 1: Tutorial Modal" estar feito:
- ✅ Modal exibido ao login de novo user
- ✅ Feature flag `tutorial_enabled` testado
- ✅ Responsive em mobile
- ✅ Performance < 200ms adicional no load
- ✅ PM validou em staging
- ✅ QA testou em Chrome, Safari, mobile

---

## Notas para Eng

1. **"Para que" é a chave**: Se story parece estranha, pergunte por que. Pode mudar implementação.
2. **Edge cases viram testes**: Cada "Given/When/Then" é um test case.
3. **Perguntas agora, não depois**: Se aceite não bate com seu entendimento técnico, avisar HOJE.
4. **Refinement sprint anterior**: Essas stories foram refinadas com design. Eng pode perguntar mas não deve re-design.
```

---

## Dicas

- **INVEST**: Uma story não INVEST = quebra menor
  - Independent? Pode fazer fora de ordem?
  - Negotiable? PM pode discutir detalhes?
  - Valuable? Entrega valor ao usuário?
  - Estimable? Eng consegue estimar?
  - Small? Cabe em sprint?
  - Testable? Sabemos quando está pronta?
- **Critérios de aceite são testes**: Escreva como test cases.
- **"Como um" é persona**: Diferencia stories pelo comportamento de quem as usa.
