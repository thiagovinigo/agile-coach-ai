# Template: Plano de Qualidade e Testes (QA)

## 📌 Ótica: O que é este documento e por que ele existe?
O Plano de QA não é apenas uma lista de testes a serem executados; é a estratégia de **mitigação de riscos de qualidade**. 
Ele existe para assegurar que, quando a engenharia disser que algo está "pronto", o time de Produto e o Usuário Final tenham confiança de que a feature entrega o valor prometido sem quebrar fluxos críticos já existentes. Ele tira o QA do final do ciclo (apenas testador) e o coloca no início (estrategista de qualidade).

---

## 🛡️ Guard Rails (Limites e Direcionamentos)
- **Deslocamento à Esquerda (Shift-Left):** A qualidade é responsabilidade de toda a equipe, não apenas do profissional de QA. Os cenários de teste devem ser elaborados em conjunto com a Engenharia antes de escrever o código.
- **Automação Ponderada:** Não automatize 100% dos testes. Priorize a Pirâmide de Testes: grande base de testes Unitários (Engineers), média base de Integração, e poucos (porém vitais) testes End-to-End (E2E) para caminhos críticos.
- **Teste Destrutivo:** QA deve procurar maneiras de quebrar o sistema através de payloads maliciosos, limites de caracteres e concorrência, não apenas seguir o "caminho feliz".

---

## 🚫 Políticas Não Negociáveis
1. **Zero Bugs Blockers para Produção:** O deploy não ocorrerá se existirem bugs classificados como *Blocker* ou *High* em aberto.
2. **Critérios de Aceite:** Histórias não podem ser movidas para a coluna "Testando" (In QA) sem a aprovação do CI (Continuous Integration), incluindo linters e testes unitários verdes.
3. **Massa de Dados Segura:** Sob hipótese alguma, dados reais de clientes (produção) podem ser usados em ambientes de STG/QA sem ofuscação rigorosa.

---

## 1. Escopo de Testes
*O que está sendo coberto e o que estamos assumindo que não precisa ser testado agora?*
- **Funcionalidades em Escopo:** [Ex: Novo fluxo de Checkout, integração com Gateway Pagar.me]
- **Funcionalidades Fora de Escopo:** [Ex: O portal administrativo (Backoffice) será testado em outra fase]

## 2. Tipos e Estratégia de Teste
- [ ] **Testes Unitários:** O time de engenharia se compromete com uma cobertura de `> 80%` no novo serviço.
- [ ] **Testes de Integração:** O contrato entre a API e o Gateway de Pagamento deve ser validado.
- [ ] **Testes E2E (Automação Frontend):** Adicionar script (Playwright/Cypress) cobrindo o caminho feliz de compra.
- [ ] **Testes Exploratórios:** Validar comportamentos de edge case manualmente em diferentes navegadores (Chrome, Safari, Firefox).
- [ ] **Testes de Acessibilidade (Opcional):** Garantir que a navegação por teclado e Screen Readers (Leitores de tela) funciona no checkout.

## 3. Matriz de Casos de Teste (Exemplo)
| ID | Cenário | Passos Resumidos | Resultado Esperado | Prioridade | Status |
|---|---|---|---|---|---|
| TC-01 | Pagamento com cartão inválido | 1. Inserir itens no carrinho. 2. Informar CVV falso. 3. Confirmar. | Mensagem de erro da operadora. Pedido não gerado. | ALTA | ⏳ |
| TC-02 | Carrinho com item sem estoque | 1. Pôr no carrinho. 2. Outro user zera o estoque. 3. Finalizar compra. | Tratamento de lock e aviso de indisponibilidade. | MÉDIA | ⏳ |

## 4. Ambientes de Teste
- **STG (Staging):** [URL e credenciais de teste]. Os serviços de terceiros (ex: envio de SMS, gateway de pagamento) devem estar apontados para Sandboxes (modo dev).

## 5. Critérios de Liberação (Go/No-Go)
- [ ] Execução e passagem de 100% dos testes de regressão automatizados do core product.
- [ ] Sem tickets de gravidade crítica ou alta relatados na sprint.
- [ ] Aprovação do Product Manager após validação visual e de fluxo em ambiente de QA.
