# Plano de Testes (QA)

## 1. Escopo de Testes
*O que será testado nesta release/feature.*
- **Funcionalidades em Escopo:** [Lista].
- **Funcionalidades Fora de Escopo:** [Lista].

## 2. Tipos de Teste a Serem Executados
- [ ] **Testes Unitários:** [Alvo de cobertura, ex: >80%].
- [ ] **Testes de Integração:** [Sistemas/APIs envolvidos].
- [ ] **Testes E2E (End-to-End):** [Principais fluxos de usuário].
- [ ] **Testes de Regressão:** [Áreas de impacto cruzado].
- [ ] **Testes Exploratórios:** [Cenários não-felizes].

## 3. Casos de Teste Principais
| ID | Título/Cenário | Passos para Reproduzir | Resultado Esperado | Status |
|---|---|---|---|---|
| TC01 | Login com sucesso | 1. Inserir credenciais válidas. 2. Clicar em Entrar. | Usuário redirecionado ao dashboard. | `Pendente` |
| TC02 | Login com senha inválida | 1. Inserir senha errada. 2. Clicar em Entrar. | Mensagem de erro "Credenciais Inválidas". | `Pendente` |

## 4. Estratégia de Automação
- **Ferramentas:** [ex: Jest, Cypress, Playwright].
- **Cenários Críticos para Automação:**
  1. [Fluxo X].
  2. [Fluxo Y].

## 5. Ambientes de Teste
- [ ] **DEV:** [URL ou configuração].
- [ ] **STG/QA:** [URL ou configuração].
- [ ] **PRD:** [Configurações pós-deploy].

## 6. Critérios de Aceite (DoD - Definition of Done)
- [ ] Todos os testes E2E críticos estão passando.
- [ ] Cobertura de testes unitários atingida.
- [ ] Zero bugs de criticidade ALTA ou BLOCKER.
- [ ] Homologação aprovada pelo PO/PM.
