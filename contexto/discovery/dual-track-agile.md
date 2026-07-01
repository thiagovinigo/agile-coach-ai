# Dual Track Agile (Discovery & Delivery)

Muitos times ágeis falham ao tratar *Discovery* (descobrir o que fazer) e *Delivery* (construir) como fases que acontecem uma depois da outra, no pior estilo Cascata (Waterfall).

O **Dual Track Agile** muda esse jogo. Ele prega que **as duas trilhas acontecem em paralelo, todos os dias, na mesma Sprint**.

---

<div class="card orange">
    <div class="card-title">⚠️ A Grande Armadilha: O Silo de Discovery</div>
    <div class="card-desc">
        <ul>
            <li><strong>Anti-Padrão:</strong> Criar um "Time de Discovery" (só Designers e PMs) e um "Time de Delivery" (só Devs).</li>
            <li><strong>Por que dá errado?</strong> Os devs recebem "especificações fechadas" goela abaixo, sem contexto. Os designers desenham coisas que a tecnologia não aguenta.</li>
            <li><strong>A Solução (Dual Track):</strong> O time é UM SÓ. É o mesmo Product Trio (PM, Tech Lead, Design) e engenheiros colaborando nas duas trilhas o tempo todo.</li>
        </ul>
    </div>
</div>

---

## 📅 Exemplo Prático: Uma Sprint Dual Track (Do Início ao Fim)

Vamos visualizar como uma Sprint de 2 semanas de um time maduro acontece na prática, unindo as duas trilhas.

### 🔴 O Lado Discovery (Validando o Futuro)
Nesta Sprint, o PM, o Designer e o Tech Lead estão preocupados com o que o time vai codificar no **próximo mês**.

<div class="info-box">
  <strong>Exemplo de Ações de Discovery nesta Sprint:</strong><br>
  - <strong>Terça-feira:</strong> PM entrevista 3 clientes que abandonaram o carrinho de compras na semana passada.<br>
  - <strong>Quinta-feira:</strong> Designer cria um protótipo fake (baixa fidelidade) de uma nova tela de Checkout.<br>
  - <strong>Sexta-feira:</strong> Tech Lead analisa o protótipo e alerta: <em>"Essa integração com o Correios demora 2 semanas. Melhor usarmos uma API mais simples pro MVP."</em><br><br>
  <strong>Saída:</strong> Uma hipótese foi validada e um item foi colocado no topo do Backlog para os desenvolvedores puxarem nas próximas semanas, já com o risco técnico mapeado.
</div>

### 🔵 O Lado Delivery (Construindo o Presente)
Enquanto isso, os desenvolvedores estão focados em escrever código para os itens que **já passaram pelo Discovery no mês passado**.

<div class="card dark">
    <div class="card-title">Exemplo de Ações de Delivery nesta Sprint:</div>
    <div class="card-desc">
        <ul>
            <li><strong>Segunda-feira:</strong> Devs puxam a História "Login via Apple", que já foi prototipada e aprovada pelos clientes há 15 dias.</li>
            <li><strong>Quarta-feira:</strong> Pair programming e code review.</li>
            <li><strong>Sexta-feira:</strong> Deploy em produção. O PM mede os resultados.</li>
        </ul>
    </div>
</div>

---

## 🚦 Como Fica o Board Kanban?

Em um time maduro de Dual Track, o board Kanban não começa em "To Do / Doing / Done". Ele tem uma seção de *Upstream* (Discovery) enorme antes de chegar nos Devs.

<div class="info-box" style="background: #f1f5f9; border-left: 4px solid #64748b;">
  <strong>Visualização do Fluxo (Board Completo):</strong><br><br>
  <strong>[ UPSTREAM / DISCOVERY ]</strong><br>
  ➡️ <strong>Ideias/Oportunidades:</strong> (Tirar fricção do carrinho)<br>
  ➡️ <strong>Em Entrevista:</strong> (Falar com 3 clientes)<br>
  ➡️ <strong>Em Prototipação:</strong> (Figma do novo checkout)<br>
  ➡️ <strong>Validação Técnica:</strong> (Tech lead diz OK)<br>
  ➡️ <strong>Ready for Dev:</strong> (A linha de corte. Aqui a magia do Discovery acabou).<br><br>
  <strong>[ DOWNSTREAM / DELIVERY ]</strong><br>
  ➡️ <strong>Em Desenvolvimento:</strong> (Devs codando)<br>
  ➡️ <strong>Code Review:</strong> (Testes e Qualidade)<br>
  ➡️ <strong>Done:</strong> (Em produção).
</div>

<p style="margin-top: 20px; font-weight: bold; color: #0f172a;">O segredo do Dual Track é que o Upstream nunca para de alimentar o Downstream, e o Downstream nunca fica ocioso esperando o PM ter uma ideia.</p>
