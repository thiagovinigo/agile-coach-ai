# Template: EXECUTAR-SPECS.md

Este arquivo é o **orquestrador de subagentes**. Ele é lido pelo Claude Code (ou pelo usuário)
para disparar todos os subagentes em paralelo ou em sequência.

---

```markdown
# EXECUTAR SPECS

> ⚠️ Execute com: `claude --dangerously-skip-permissions`
> 
> Este arquivo dispara subagentes independentes para cada feature.
> Cada agente tem contexto isolado — lê APENAS a sua spec.

---

## PRÉ-REQUISITOS

Antes de executar, confirme:
- [ ] Variáveis de ambiente configuradas (`.env`)
- [ ] Dependências instaladas (`npm install` / `pip install -r requirements.txt`)
- [ ] Banco de dados inicializado (se aplicável)

---

## FASE 1 — Fundação (Executar em SEQUÊNCIA)

Estas tasks têm dependências e devem rodar na ordem:

### Task 001 — [Nome da Feature]
```
Leia o arquivo `.specs/001-nome-feature/spec.md` completamente.
Execute TODOS os critérios de aceitação descritos nele.
Ao finalizar, confirme quais CAs foram concluídos.
```

### Task 002 — [Nome da Feature]
```
Leia o arquivo `.specs/002-nome-feature/spec.md` completamente.
Execute TODOS os critérios de aceitação descritos nele.
Ao finalizar, confirme quais CAs foram concluídos.
```

---

## FASE 2 — Features Independentes (Podem rodar em PARALELO)

As tasks abaixo NÃO têm dependências entre si. Dispare como subagentes simultâneos:

### Task 003 — [Nome da Feature]
```
Leia o arquivo `.specs/003-nome-feature/spec.md` completamente.
Execute TODOS os critérios de aceitação descritos nele.
Ao finalizar, confirme quais CAs foram concluídos.
```

### Task 004 — [Nome da Feature]
```
Leia o arquivo `.specs/004-nome-feature/spec.md` completamente.
Execute TODOS os critérios de aceitação descritos nele.
Ao finalizar, confirme quais CAs foram concluídos.
```

### Task 005 — [Nome da Feature]
```
Leia o arquivo `.specs/005-nome-feature/spec.md` completamente.
Execute TODOS os critérios de aceitação descritos nele.
Ao finalizar, confirme quais CAs foram concluídos.
```

---

## FASE 3 — Integração (Executar após FASE 2)

### Task 006 — [Nome da Feature]
```
Leia o arquivo `.specs/006-nome-feature/spec.md` completamente.
Execute TODOS os critérios de aceitação descritos nele.
Ao finalizar, confirme quais CAs foram concluídos.
```

---

## PÓS-EXECUÇÃO

Após todas as tasks completarem:
1. Mova as specs concluídas para `.specs/archive/`
2. Rode os testes de integração: `[comando aqui]`
3. Verifique o build: `[comando aqui]`

---

## PROGRESSO

| Task | Feature | Status | Agente |
|------|---------|--------|--------|
| 001 | nome-feature | ⏳ Pendente | - |
| 002 | nome-feature | ⏳ Pendente | - |
| 003 | nome-feature | ⏳ Pendente | - |

Status: ⏳ Pendente | 🔄 Executando | ✅ Concluído | ❌ Erro
```
