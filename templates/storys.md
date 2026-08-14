# Template: User Stories e Épicos

## 📌 Ótica: O que é este documento e por que ele existe?
Este documento orienta a quebra (breakdown) de épicos e PRDs em fatias testáveis e entregáveis de software: as User Stories (Histórias de Usuário). 
Ele existe para transformar especificações em **tarefas granulares** que o time de engenharia consiga estimar, executar e testar dentro de uma única sprint. Uma boa história de usuário conta a perspectiva do cliente, garantindo que o código escrito gere valor real.

---

## 🛡️ Guard Rails (Limites e Direcionamentos)
- **Formato INVEST:** Toda história deve ser *Independent* (Independente), *Negotiable* (Negociável), *Valuable* (Gera Valor), *Estimable* (Estimável), *Small* (Pequena), e *Testable* (Testável). Se for grande demais, deve voltar a ser um Épico e ser quebrada novamente.
- **Linguagem BDD (Given-When-Then):** Use comportamento esperado para descrever testes, evitando dubiedades para o QA e para o Dev.
- **Fatiamento Vertical:** Entregue valor end-to-end (banco de dados + API + tela) na história, em vez de fatiar por camadas técnicas (ex: "Criar tabela X").

---

## 🚫 Políticas Não Negociáveis
1. **Definition of Ready (DoR):** Nenhuma história entra na Sprint se não tiver critérios de aceite definidos, dependências mapeadas, mockups (se aplicável) e estimativa do time.
2. **Definition of Done (DoD):** Uma história só é concluída quando o código estiver em produção (ou ambiente de homologação), com testes automatizados passando e revisão de código aprovada.
3. **Cenário Negativo Obrigatório:** Toda história que interage com dados do usuário deve ter pelo menos um critério de aceite tratando caminhos de erro (Unhappy Path).

---

## Estrutura da User Story

### Título da História
*Deve ser conciso e focado no valor.* Ex: `[Login] Autenticação via Google`

### 1. Narrativa (As a / I want / So that)
> **Como um** [tipo de usuário/persona] <br>
> **Eu quero** [realizar uma ação ou objetivo] <br>
> **Para que** [eu obtenha um valor ou benefício específico]

### 2. Contexto Adicional
*Informações técnicas ou de negócio que o desenvolvedor precisa saber. Links para designs no Figma, endpoints de API de terceiros, PRDs originais.*

### 3. Critérios de Aceite (Acceptance Criteria)
*Regras que ditam se a história foi concluída com sucesso. Recomendamos o formato Gherkin/BDD.*

- **Cenário 1: [Caminho Feliz]**
  - **Dado que** (Given) [estado inicial / pré-condição]
  - **Quando** (When) [uma ação ocorre]
  - **Então** (Then) [o resultado esperado]

- **Cenário 2: [Caminho de Erro - Ex: Falha de Rede]**
  - **Dado que** (Given) [o sistema está offline]
  - **Quando** (When) [o usuário clica em salvar]
  - **Então** (Then) [uma mensagem de erro amigável é exibida]

### 4. Dependências Técnicas
- A API `/v1/auth/google` deve estar criada (ver Story #1234).

### 5. Checklists de DoD (Definition of Done) Específicos
- [ ] Testes unitários cobrindo cenários de erro de rede.
- [ ] Validação de acessibilidade no componente de botão (WCAG AA).
