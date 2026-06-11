import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    guia = f.read()

# Locate boundaries
start_marker = "<!-- ===== LEAN INCEPTION ===== -->"
end_marker = "<!-- ========================================== -->\n<!-- ESPECIALISTA TFS                           -->"

if start_marker in guia and end_marker in guia:
    top_part = guia.split(start_marker)[0]
    bottom_part = end_marker + guia.split(end_marker)[1]
else:
    print("Markers not found!")
    exit(1)

new_content = """<!-- ===== LEAN INCEPTION ===== -->
<div id="s-po-lean-inception" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#db2777,#be185d)">
    <div class="tag">DESCOBERTA DE PRODUTO</div>
    <h2>🚀 Lean Inception</h2>
    <p>O framework de 5 dias para alinhar pessoas e descobrir o Produto Certo (MVP)</p>
  </div>

  <div class="card dark">
    <div class="card-title">📌 O que é?</div>
    <p>Criado por Paulo Caroli, o Lean Inception é um workshop colaborativo intensivo (geralmente de segunda a sexta) desenhado para alinhar Stakeholders, Negócios, UX e Tecnologia sobre o que construir primeiro: o <strong>MVP (Minimum Viable Product)</strong>. Ele evita o desperdício de passar meses escrevendo requisitos para algo que não entrega valor rápido.</p>
  </div>

  <div class="st">📅 A Dinâmica: Como fazer os 5 Dias</div>
  <div class="g2">
    <div class="card orange">
      <div class="card-title">📍 Dia 1: Alinhamento e Fronteiras</div>
      <p><strong>Atividade 1: Visão do Produto.</strong> Usamos o formato de <em>Elevator Pitch</em>: "Para [cliente], que tem [necessidade], o [nome do produto] é um [categoria] que [benefício principal]. Diferente de [concorrente], o nosso produto [diferencial]".</p>
      <p><strong>Atividade 2: O Produto É / Não É / Faz / Não Faz.</strong> Desenhe um quadro com 4 quadrantes. Cada pessoa escreve post-its. É aqui que o PO corta as "viagens" (ex: "Não é uma rede social", "Não faz cálculos complexos agora"). Isso cria a primeira cerca de escopo.</p>
    </div>
    <div class="card orange">
      <div class="card-title">👥 Dia 2: Personas e Jornada</div>
      <p><strong>Atividade 1: Personas.</strong> Quem vai usar? Construam 2 a 3 perfis fictícios extremos. Descreva suas necessidades reais, não apenas demografia.</p>
      <p><strong>Atividade 2: Jornada do Usuário.</strong> Como a Persona resolve o problema hoje? Mapeie o passo a passo em post-its sequenciais (ex: 1. Acorda, 2. Abre o app, 3. Fica confuso com a tela...).</p>
    </div>
    <div class="card orange">
      <div class="card-title">💡 Dia 3: Brainstorming de Features</div>
      <p><strong>A Dinâmica:</strong> Olhando para os passos da jornada desenhada ontem, perguntem: <em>"O que o nosso produto precisa ter de funcionalidade para ajudar a persona neste passo exato?"</em>.</p>
      <p>Nesta fase, não há restrições. Todas as ideias viram post-its e são coladas embaixo do respective passo da jornada.</p>
    </div>
    <div class="card orange">
      <div class="card-title">⚖️ Dia 4: Revisão Técnica, de UX e Negócio</div>
      <p><strong>A Dinâmica do Semáforo:</strong> Pegue cada feature do Dia 3 e aplique três avaliações visuais:</p>
      <ul class="chk" style="margin-top:10px">
        <li><strong>Nível de Confiança (Cor):</strong> Sabe como fazer? (Verde), Tem dúvidas? (Amarelo), Não faz ideia de como fazer? (Vermelho).</li>
        <li><strong>Esforço (Tamanho):</strong> Vote com P, M, G ou GG.</li>
        <li><strong>Valor de Negócio e Valor para UX:</strong> De $$ a $$$ e de ♥ a ♥♥♥.</li>
      </ul>
      <p>Nesta etapa, o Tech Lead pode alertar que uma feature é "GG e Vermelha".</p>
    </div>
  </div>

  <div class="card dark" style="margin-top: 16px;">
    <div class="card-title">🧩 Dia 5: O Sequenciador e Canvas MVP</div>
    <p>Aqui ocorre a negociação final. Usamos um quadro chamado "Sequenciador", que é dividido em "Ondas" (linhas).</p>
    <p><strong>As Regras do Sequenciador:</strong></p>
    <ul class="chk" style="margin-top:10px">
      <li>Cada onda (linha) pode ter no máximo 3 cards de funcionalidade.</li>
      <li>Uma onda não pode ter todas as features do tamanho "GG" ou "G".</li>
      <li>Se um card é "Vermelho" (alta incerteza), ele ocupa espaço de dois cards.</li>
    </ul>
    <p>A "Onda 1" e possivelmente a "Onda 2" vão compor o Canvas do MVP. O resto é futuro (Backlog).</p>
  </div>

  <div class="st">🎯 O Papel do PO na Facilitação</div>
  <div class="card blue">
    <ul class="chk">
      <li><strong>O "Tie-breaker":</strong> Quando o time de negócios e o time técnico não chegam a um acordo no Dia 4 (se uma feature tem muito ou pouco valor), o PO dá o voto de desempate.</li>
      <li><strong>Defesa do "Lean":</strong> O PO atua como um "cortador de gordura". No Dia 5, quando os stakeholders tentam empurrar 10 features para a Onda 1, o PO aplica as restrições do sequenciador com firmeza.</li>
      <li><strong>Saída:</strong> A saída do Dia 5 é o insumo para o PO montar o Backlog de Produto no Jira/TFS, quebrando as features da Onda 1 em histórias menores.</li>
    </ul>
  </div>

  <div class="st">🏦 Exemplo Real (Super App de Banco)</div>
  <div class="card dark">
    <div class="card-title">Do Sonho ao MVP Enxuto</div>
    <p><strong>O Cenário (Pré-Inception):</strong> A diretoria queria lançar um Super App com Conta Corrente, Cartão de Crédito, Investimentos Complexos e Seguros de Vida. Tudo em 3 meses. Havia 2 squads apenas. A engenharia estava em pânico.</p>
    <p><strong>Dia 1 (O que Não É):</strong> Durante a atividade, o PO guiou a diretoria para colar o post-it: <em>"Não é uma plataforma de Home Broker"</em>. Primeira vitória: Investimentos complexos foram descartados do escopo imediato.</p>
    <p><strong>Dia 4 (Revisão):</strong> A feature "Contratação de Seguro de Vida via App" recebeu post-it Vermelho (nível de confiança zero, pois a API da seguradora parceira não existia) e tamanho GG.</p>
    <p><strong>Dia 5 (O Sequenciador):</strong> Ao tentar colocar Conta Corrente, Cartão e Seguro na Onda 1, as regras estouraram (muitos GGs, muitas cores vermelhas). O PO facilitou a negociação: <em>"Vamos colocar 'Visualizar Saldo' e 'Pagar Boleto' na Onda 1 para validar se o cliente abre o nosso App em vez do App do banco concorrente. Seguro vai para a Onda 4"</em>.</p>
    <p><strong>Resultado:</strong> O MVP foi lançado em 2 meses, com alta adoção. Seguro de vida só foi feito no ano seguinte, quando a API do parceiro ficou pronta, evitando meses de código jogado fora.</p>
  </div>
</div>

<!-- ===== CONTINUOUS DISCOVERY ===== -->
<div id="s-po-continuous-discovery" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#0d9488,#0f766e)">
    <div class="tag">DESCOBERTA DE PRODUTO</div>
    <h2>🔭 Continuous Discovery (Teresa Torres)</h2>
    <p>Descobrir enquanto se constrói: O fim do "achismo" no Backlog</p>
  </div>

  <div class="card dark">
    <div class="card-title">📌 O que é?</div>
    <p>O <em>Continuous Discovery Habits</em>, popularizado por Teresa Torres, é a prática onde o <strong>Trio de Produto (Product Manager/PO, Tech Lead e Product Designer)</strong> engaja <em>no mínimo semanalmente</em> com clientes reais. O objetivo é tomar decisões diárias de produto baseadas em feedbacks contínuos, abandonando o modelo de "uma grande pesquisa de mercado por ano".</p>
    <p>O foco muda de <strong>Output</strong> (Quantas features entregamos?) para <strong>Outcome</strong> (Que impacto ou comportamento nós mudamos?).</p>
  </div>

  <div class="st">🌳 A Árvore de Oportunidades (Opportunity Solution Tree)</div>
  <div class="card green">
    <p>A OST é a ferramenta visual de facilitação que o Trio usa para conectar o objetivo de negócio às tarefas de engenharia, garantindo que ninguém se apaixone por uma solução sem antes validar o problema.</p>
    <ul class="chk" style="margin-top:10px;">
      <li><strong>1. Outcome (O Topo):</strong> É a métrica ou OKR que o time precisa mexer. <em>Ex: Aumentar a retenção no 1º mês em 15%.</em></li>
      <li><strong>2. Opportunities (Galhos):</strong> Problemas, dores ou desejos dos clientes descobertos nas entrevistas, que atrapalham o Outcome. <em>Ex: "Não entendi como configuro minha conta no primeiro acesso."</em></li>
      <li><strong>3. Solutions (Folhas):</strong> Múltiplas ideias para resolver a MESMA oportunidade. <em>Ex: "Vídeo de Onboarding", "Wizard passo-a-passo", "Pop-up de ajuda".</em></li>
      <li><strong>4. Experiments (Raízes):</strong> Testes rápidos para validar as suposições críticas de cada solução.</li>
    </ul>
  </div>

  <div class="st">🛠️ Como fazer a dinâmica semanal</div>
  <div class="g2">
    <div class="card dark">
      <div class="card-title">🗣️ 1. Entrevistas Contínuas</div>
      <p><strong>A Regra:</strong> Automatize o recrutamento. Ao invés de o PO caçar usuários, configure um pop-up no produto: <em>"Quer falar conosco por 15 min em troca de um cupom de $50?"</em>.</p>
      <p><strong>Como Conduzir:</strong> Nunca pergunte "O que você acharia de uma feature X?" (isso gera respostas falsas). Foco no passado: <strong>"Me conte sobre a última vez que você usou o nosso produto para fazer Y"</strong>. Deixe a pessoa contar a história e anote as dores (Oportunidades).</p>
    </div>
    <div class="card dark">
      <div class="card-title">⚖️ 2. Regra das 3 Soluções</div>
      <p>O ser humano tem viés de confirmação. Se o PO tem uma ideia e faz um teste, ele fará de tudo para o teste dar certo.</p>
      <p><strong>Como Conduzir:</strong> Para cada Oportunidade que o time decidir atacar, eles são <strong>obrigados a desenhar 3 soluções diferentes</strong> e testá-las em paralelo. O teste não é "Qual é boa?", mas sim "Qual das 3 é a MELHOR?".</p>
    </div>
  </div>

  <div class="card orange" style="margin-top:16px;">
    <div class="card-title">🧪 3. Mapeando e Testando Suposições (Assumptions)</div>
    <p>Não construa as 3 soluções (isso demoraria meses). Ao invés disso, o Trio de Produto lista as <strong>suposições</strong> necessárias para que a solução funcione: <em>Desejabilidade (Alguém quer?), Viabilidade Técnica (Conseguimos fazer?), Viabilidade de Negócio (Dá lucro?) e Usabilidade (Sabem usar?).</em></p>
    <p><strong>Como testar (Exemplos de Experimentos):</strong></p>
    <ul class="chk" style="margin-top:10px">
      <li><strong>Fake Door:</strong> Um botão no sistema que diz "Novo Recurso". Quando o cliente clica, abre um modal: "Estamos desenvolvendo isso, quer entrar na lista de espera?". Serve para medir Desejabilidade (Click-through rate) gastando 2 horas de Dev.</li>
      <li><strong>Protótipo de um Dia:</strong> O Designer desenha telas não funcionais no Figma, o PO liga para 3 usuários e pede para eles tentarem "clicar" onde acham que deveriam. Mede Usabilidade em 1 dia.</li>
    </ul>
  </div>

  <div class="st">🎯 Exemplo Real Completo (Delivery App)</div>
  <div class="card blue">
    <div class="card-title">🛒 O caso do "Esqueci a Sobremesa"</div>
    <p><strong>O Outcome (OKR):</strong> O board do app de delivery pediu para o Squad aumentar o <em>Ticket Médio (AOV)</em> dos pedidos feitos entre 19h e 22h.</p>
    <p><strong>A Descoberta (Oportunidade):</strong> O PO conduziu entrevistas na quinta-feira pedindo: <em>"Me contem como foi o jantar de vocês ontem usando nosso app"</em>. Três clientes relataram a mesma coisa: "Nós pedimos a pizza, e só quando o motoboy chegou a gente percebeu que esquecemos de pedir um doce."</p>
    <p><strong>As 3 Soluções Levantadas:</strong><br>
    1. Mandar uma notificação Push 5 minutos após o pedido.<br>
    2. Colocar uma seção piscante "Não esqueça a sobremesa" na Home.<br>
    3. Ao clicar em "Finalizar Pedido", abrir um Pop-up (Upsell) sugerindo 3 doces do restaurante.</p>
    <p><strong>O Experimento (Fake Door):</strong> Para testar a Solução 3, a equipe subiu um botão "Adicionar Brigadeiro R$5" estático na tela de checkout, apenas para 5% dos usuários. Se clicassem, dizia "Infelizmente este restaurante está sem sobremesas agora".</p>
    <p><strong>O Resultado:</strong> O botão teve uma taxa de conversão gigantesca (35%). O Tech Lead viu que a solução 3 era muito mais fácil de codar (esforço) do que as outras. Eles enviaram a Solução 3 inteira para a Sprint seguinte, e o Ticket Médio subiu 12% em duas semanas.</p>
  </div>
</div>
"""

with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
    f.write(top_part + new_content + "\n" + bottom_part)

print("Detailed content expanded successfully.")
