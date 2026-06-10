# User Story Template

Use este template para criar uma user story estruturada. Ou chame `/user-stories` para gerar múltiplas stories a partir de um PRD.

---

## Story: [Nome claro do user goal]

**Priority**: P0 | P1 | P2
**Estimate**: [Dias ou story points]
**Status**: Backlog | In progress | Done

---

### User story statement

**Como um** [Persona]
**Eu quero** [Ação clara]
**Para que** [Resultado/Valor]

---

### Contexto

[Uma ou duas sentenças sobre por que isso importa — vindo de descoberta, PRD, ou feedback]

---

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
When [ação]
Then [resultado]
```

#### Edge case 2
```gherkin
Given que [variação]
When [ação]
Then [resultado]
```

---

### Notas técnicas

- [Restrição de implementação]
- [Integração necessária]
- [Performance requirement]
- [API/data que precisa]

---

### Dependências

- Precisa de [Story X] ou [Ferramenta Y]
- Desbloqueia [Próxima story]

---

### Definition of Done

- ✅ Critérios de aceite passaram em manual testing
- ✅ Code review aprovado
- ✅ Integrado em staging
- ✅ QA testou happy path + principais edge cases
- ✅ Documentação (se applicable)
- ✅ PM validou em staging

---

### Notes para Eng

[Contexto que ajuda eng a tomar decisões criativas dentro do escopo]

---

**Signed off**: [PM/Designer]
**Date**: [Data]
