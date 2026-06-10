# Exemplos Reais de Decomposição de PRD

## Exemplo 1 — SaaS de Gestão de Ideias (Mini CRM)

**PRD resumido**: App web para times cadastrarem, priorizarem e acompanharem ideias de produto. 
Stack: Next.js, Supabase, TypeScript.

**Decomposição resultante:**

```
001-criar-projeto          → setup Next.js + Supabase + estrutura de pastas
002-registrar-usuario      → auth com Supabase (email/senha)
003-login-usuario          → login + session + redirect
004-personalizar-app       → nome do workspace, logo, cores
005-cadastro-tipos-ideia   → CRUD de categorias/tipos
006-carregar-tipos         → listagem e seed de tipos padrão
007-cadastro-ideia         → formulário de criação de ideia com tipo/prioridade
008-modulo-de-ideias       → listagem, filtros, busca de ideias
009-recurrence             → sistema de recorrência de reviews
010-ui-base                → design system, componentes compartilhados
011a-pipeline-kanban       → view kanban de ideias por status
011b-pipeline-lista        → view lista com ordenação
012a-dashboard-analytics   → métricas de ideias por período
012b-dashboard-frontend    → UI do dashboard com gráficos
```

**Por que esta ordem?**
- 001 primeiro: sem projeto, nada funciona
- 002/003 antes de tudo: sem auth, não há usuário logado
- 004 depende de 002 (usuário precisa existir)
- 005/006 antes de 007 (ideia precisa ter tipo)
- 010 pode rodar em paralelo com 007-009
- 011a e 011b são independentes entre si (paralelo)
- 012a antes de 012b (lógica antes de UI)

---

## Exemplo 2 — API de E-commerce

**PRD resumido**: REST API para loja virtual. Stack: FastAPI, PostgreSQL, Redis.

**Decomposição:**
```
001-setup-projeto          → FastAPI + Alembic + estrutura
002-modelo-produto         → tabela produtos + CRUD básico
003-modelo-categoria       → tabela categorias + relacionamento
004-auth-jwt               → login/registro + JWT
005-carrinho-redis          → carrinho de compras em Redis
006-pedido-checkout        → criar pedido a partir do carrinho
007-pagamento-stripe       → integração Stripe
008-notificacao-email      → envio de emails transacionais
009-admin-dashboard        → endpoints administrativos
010-testes-integracao      → suite de testes E2E
```

**Paralelos na Fase 2:** 002, 003, 004 (sem dependência entre si)
**Paralelos na Fase 3:** 005, 008, 009 (após 004)
**Sequencial na Fase 4:** 006 → 007 → 010

---

## Regras Extraídas dos Exemplos

### Sempre na Fase 1 (Sequencial):
- Setup/scaffold do projeto
- Autenticação/usuário base
- Modelos de dados core

### Candidatos a Paralelo:
- Features de UI independentes (ex: 011a/011b)
- Integrações com serviços externos
- CRUD de entidades sem relacionamento entre si
- Componentes de UI e lógica de negócio da mesma feature

### Nunca em Paralelo:
- Migrations de banco de dados
- Setup de infraestrutura
- Features que dependem do resultado de outra

---

## Heurísticas de Granularidade

**Spec muito grande** (dividir):
- Mais de 5 arquivos a criar
- Mais de 8 critérios de aceitação
- Leva mais de 30min para um dev humano implementar

**Spec muito pequena** (juntar):
- Apenas 1 arquivo a criar
- Menos de 2 critérios de aceitação
- Depende de outra spec que já é pequena

**Tamanho ideal:**
- 2-5 arquivos
- 3-6 critérios de aceitação
- ~15-30min de trabalho
