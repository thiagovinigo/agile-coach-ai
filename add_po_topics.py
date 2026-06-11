import re

# 1. UPDATE APP.JS
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Insert in app.js inside kb-po
if "s-po-lean-inception" not in app_js:
    app_target = "{ title: 'O Papel do PO', parts: [ { id: 's-po', context: 'Gestão de Produto' } ] },"
    app_insert = """{ title: 'O Papel do PO', parts: [ { id: 's-po', context: 'Gestão de Produto' } ] },
                    { title: 'Lean Inception', parts: [ { id: 's-po-lean-inception', context: 'Descoberta de Produto' } ] },
                    { title: 'Continuous Discovery', parts: [ { id: 's-po-continuous-discovery', context: 'Descoberta de Produto' } ] },"""
    app_js = app_js.replace(app_target, app_insert)
    
    # bump version in app.js if needed (we'll just rewrite it and bump index.html later)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)

# 2. UPDATE SCRUMBAN_GUIA.HTML
with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    guia = f.read()

if "s-po-lean-inception" not in guia:
    # Insert in nav-group ng-po
    nav_target = """<div class="nav-item" onclick="goTo('s-po',this)"><span class="ni">🧑‍💼</span> PO, Backlog & Hierarquia</div>"""
    nav_insert = nav_target + """\n        <div class="nav-item" onclick="goTo('s-po-lean-inception',this)"><span class="ni">🚀</span> Lean Inception</div>
        <div class="nav-item" onclick="goTo('s-po-continuous-discovery',this)"><span class="ni">🔭</span> Continuous Discovery</div>"""
    guia = guia.replace(nav_target, nav_insert)
    
    # The HTML content blocks
    po_content = """
<!-- ===== LEAN INCEPTION ===== -->
<div id="s-po-lean-inception" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#db2777,#be185d)">
    <div class="tag">DESCOBERTA DE PRODUTO</div>
    <h2>🚀 Lean Inception</h2>
    <p>Alinhando pessoas e construindo o Produto Certo (MVP) em uma semana</p>
  </div>

  <div class="card dark">
    <div class="card-title">📌 O que é?</div>
    <p>Lean Inception é um workshop colaborativo de 5 dias criado por Paulo Caroli, focado em alinhar um grupo de pessoas sobre o <strong>Minimum Viable Product (MVP)</strong> de um produto ou funcionalidade. Ele mistura Design Thinking com Lean StartUp para responder rapidamente: <em>O que vamos construir primeiro?</em></p>
  </div>

  <div class="st">📅 A Agenda de 5 Dias</div>
  <div class="g3">
    <div class="card orange">
      <div class="card-title">Dia 1: Visão & É/Não É</div>
      <p>Escrever a visão do produto. Definir claramente o que o produto É, NÃO É, FAZ e NÃO FAZ para cercar o escopo.</p>
    </div>
    <div class="card orange">
      <div class="card-title">Dia 2: Personas & Jornada</div>
      <p>Quem vai usar? Mapear os usuários (Personas) e desenhar a jornada de como eles resolvem o problema hoje.</p>
    </div>
    <div class="card orange">
      <div class="card-title">Dia 3: Brainstorming de Features</div>
      <p>A partir da jornada, o que o produto precisa ter para atender os usuários? Levantamento maciço de ideias.</p>
    </div>
    <div class="card orange">
      <div class="card-title">Dia 4: Revisão Técnica, UX e Negócio</div>
      <p>O time avalia cada feature com a tríade (Nível de Confiança, Esforço e Valor de Negócio/UX).</p>
    </div>
    <div class="card orange">
      <div class="card-title">Dia 5: Sequenciador e Canvas MVP</div>
      <p>Fatiar as entregas. O que entra na onda 1 (MVP)? O que fica para depois? E formalizar isso no Canvas MVP.</p>
    </div>
  </div>

  <div class="st">🛠️ O Papel do Product Owner</div>
  <div class="card dark">
    <div class="card-title">Como liderar a Lean Inception?</div>
    <ul class="chk">
      <li><strong>Pré-Inception:</strong> Garantir que os Stakeholders certos (Patrocinador, Negócio, Tech, UX) foram convidados e que o problema de negócio está claro.</li>
      <li><strong>Durante:</strong> Ser a voz decisiva em caso de empate (Tie-breaker), garantindo que o escopo não infle (Evitar o "Tudo é prioridade").</li>
      <li><strong>Pós-Inception:</strong> Pegar o Canvas MVP e as Features sequenciadas e transformá-las no <em>Product Backlog</em> inicial, quebrando os épicos em Histórias de Usuário.</li>
    </ul>
  </div>

  <div class="st">🎯 Exemplo Real</div>
  <div class="card blue">
    <div class="card-title">🏦 Cenário: Super App do Banco</div>
    <ul class="chk">
      <li><strong>A Ocorrência:</strong> A diretoria queria lançar um Super App com Conta, Cartão, Investimentos e Seguros tudo no primeiro semestre. O escopo era impossível para os 2 squads disponíveis.</li>
      <li><strong>A Intervenção (Lean Inception):</strong> O PO chamou a diretoria para 5 manhãs de imersão. No "É / Não É", deixaram claro que o app "Não É uma plataforma de Home Broker neste momento". No Sequenciador, a Onda 1 (MVP) virou apenas "Visualizar saldo e Extrato" e "Pagar Boleto". Seguros e Investimentos foram para a Onda 4.</li>
      <li><strong>O Resultado:</strong> O time entregou o MVP em 2 meses, validou a adoção do cliente e só depois começou a investir nas features complexas.</li>
    </ul>
  </div>
</div>

<!-- ===== CONTINUOUS DISCOVERY ===== -->
<div id="s-po-continuous-discovery" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#0d9488,#0f766e)">
    <div class="tag">DESCOBERTA DE PRODUTO</div>
    <h2>🔭 Continuous Discovery (Teresa Torres)</h2>
    <p>O fim da miopia de produto: Descobrir enquanto se constrói</p>
  </div>

  <div class="card dark">
    <div class="card-title">📌 O que é?</div>
    <p>Continuous Discovery Habits (Teresa Torres) é uma abordagem em que a <strong>Tríade de Produto (PO/PM, Tech Lead e UX/Design)</strong> engaja <em>semanalmente</em> com os clientes. O foco muda de entregar soluções (Output) para resolver problemas e atingir resultados de negócio (Outcome).</p>
  </div>

  <div class="st">🌳 A Árvore de Oportunidades (OST)</div>
  <div class="card green">
    <p>A ferramenta central do Continuous Discovery é a <strong>Opportunity Solution Tree</strong>. Ela força o time a pensar de cima para baixo:</p>
    <ul style="margin-top:10px; margin-left: 20px; line-height: 1.6;">
      <li><strong>1. Outcome (Resultado):</strong> O objetivo de negócio (Ex: Aumentar retenção em 20%).</li>
      <li><strong>2. Opportunities (Oportunidades):</strong> Problemas, dores ou desejos dos clientes que, se resolvidos, geram o Outcome (Ex: "Não consigo achar meu histórico de compras").</li>
      <li><strong>3. Solutions (Soluções):</strong> As ideias de features para atacar a oportunidade (Ex: "Barra de busca" ou "Filtro por data").</li>
      <li><strong>4. Experiments (Experimentos):</strong> Testes rápidos para validar se a Solução realmente resolve a Oportunidade.</li>
    </ul>
  </div>

  <div class="st">🛠️ Como aplicar na Prática?</div>
  <div class="g2">
    <div class="card dark">
      <div class="card-title">🔄 Entrevistas Semanais</div>
      <p>Agendar com pelo menos 1 ou 2 clientes toda semana. Não pergunte o que eles querem, peça para eles contarem histórias (Ex: <em>"Me conte sobre a última vez que você tentou transferir dinheiro"</em>). A partir dessas histórias, extraia as <strong>Oportunidades</strong>.</p>
    </div>
    <div class="card dark">
      <div class="card-title">🔬 Compare Soluções</div>
      <p>Nunca avalie uma ideia isolada. Se você tem uma Oportunidade, desenhe 3 soluções diferentes. Teste as suposições críticas de cada uma (usando protótipos rápidos ou fake doors) e compare qual performa melhor antes de codar.</p>
    </div>
  </div>

  <div class="st">🎯 Exemplo Real</div>
  <div class="card blue">
    <div class="card-title">🛒 Cenário: App de Delivery</div>
    <ul class="chk">
      <li><strong>O Outcome:</strong> Aumentar o ticket médio dos pedidos do jantar.</li>
      <li><strong>A Oportunidade (Descoberta):</strong> Nas entrevistas semanais, os clientes diziam: <em>"A gente sempre esquece de pedir a sobremesa e só lembra quando a comida chega"</em>.</li>
      <li><strong>As Soluções:</strong> 1) Notificação push. 2) Popup no carrinho sugerindo doce. 3) Sobremesa inclusa no combo.</li>
      <li><strong>A Intervenção:</strong> O PO fez um teste "Fake Door" com um botão de "Adicionar sobremesa" no carrinho (que não fazia nada, só media clique). O click-through rate foi de 40%.</li>
      <li><strong>O Resultado:</strong> O time focou todo o esforço de Dev no Popup do carrinho (Solução 2) sabendo que iria gerar impacto, reduzindo o desperdício de tempo.</li>
    </ul>
  </div>
</div>
"""
    
    # insert before ESPECIALISTA TFS
    target_split = "<!-- ========================================== -->\n<!-- ESPECIALISTA TFS                           -->"
    if target_split in guia:
        guia = guia.replace(target_split, po_content + "\n" + target_split)
    else:
        guia += po_content

    with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(guia)

print("PO Topics added successfully.")
