const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'contexto', 'scrumban_guia.html');
let content = fs.readFileSync(filePath, 'utf-8');

const playbooksHtml = `
<!-- ===== MASTERCLASS (10k HORAS) ===== -->

<!-- PLAYBOOK 1: DEMANDA -->
<div id="s-mc-demanda" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#1d4ed8,#1e3a8a)">
    <div class="tag">MASTERCLASS 10K HORAS</div><h2>📥 O Lado da Demanda (PO & SRM)</h2>
    <p>Playbook de execução avançada para Product Owners e Service Request Managers</p>
  </div>
  
  <div class="teach-hero" style="background:linear-gradient(135deg, #0f172a, #1e293b);">
    <div class="th-tag">MENTALIDADE DE EXPERTISE</div>
    <h2>Do "Tirador de Pedidos" ao "Gestor de Portfólio"</h2>
    <div class="th-sub">Um PO Júnior diz "sim" para tudo e empilha 50 itens no backlog. Um SRM/PO nível 10k horas entende que o Upstream é um funil com limites (WIP de Upstream). Eles usam matemática (Cost of Delay) para dizer "não, isso custa mais do que vale". Eles sabem que uma fila longa não é segurança, é inflação de expectativas.</div>
  </div>

  <div class="st">🛠️ A Caixa de Ferramentas (Upstream)</div>
  <div class="g2">
    <div class="card blue">
      <div class="card-title">1. WSJF (Weighted Shortest Job First)</div>
      <p>Esqueça "Baixa/Média/Alta". Calcule o <strong>Cost of Delay</strong> (Valor p/ Negócio + Criticidade de Tempo + Redução de Risco) e divida pelo <strong>Tamanho do Esforço</strong>. O item com o maior WSJF sobe para o topo. Isso elimina a política na priorização.</p>
    </div>
    <div class="card blue">
      <div class="card-title">2. Upstream WIP Limits</div>
      <p>A fila de "Discovery" e "Refinamento" também precisa de limites. Se o time tem capacidade de entregar 5 features por mês, o PO não deve ter 40 em refinamento. Limitar o WIP do Upstream força a tomada de decisão antecipada (descarte rápido).</p>
    </div>
  </div>

  <div class="st">🎬 Dinâmica de Execução: Refinamento de Elite</div>
  <div class="how-to-teach">
    <div class="htt-title">Roteiro: Reunião de Triage & Refinamento (45 min)</div>
    <div class="htt-body">
      <strong>Objetivo:</strong> Promover itens da "Fila de Ideias" para "Pronto para Desenvolver" com DoR atingido.<br><br>
      <strong>1. Revisão das Métricas de Upstream (5 min):</strong> "Temos 3 vagas na fila de Dev. Precisamos refinar 3 itens hoje."<br>
      <strong>2. Apresentação do Problema, não da Solução (10 min):</strong> O PO/SRM não traz telas prontas. Traz a "Jornada do Usuário" e o "Cost of Delay". Ex: "Se não fizermos X até dezembro, perdemos $5k/dia."<br>
      <strong>3. Fatiamento Tático (Elevator Pitch) (20 min):</strong> O time técnico participa ativamente quebrando o Épico. A pergunta central: <em>"Qual é a menor fatia possível que valida a hipótese?"</em><br>
      <strong>4. Acordo de Classe de Serviço (10 min):</strong> Este item é Expedite (fura fila) ou Standard? A decisão é registrada no cartão.
    </div>
  </div>
</div>

<!-- PLAYBOOK 2: ENTREGA -->
<div id="s-mc-entrega" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#047857,#065f46)">
    <div class="tag">MASTERCLASS 10K HORAS</div><h2>📤 O Lado da Entrega (SM & SDM)</h2>
    <p>Playbook de execução avançada para Scrum Masters e Service Delivery Managers</p>
  </div>
  
  <div class="teach-hero" style="background:linear-gradient(135deg, #064e3b, #065f46);">
    <div class="th-tag">MENTALIDADE DE EXPERTISE</div>
    <h2>Do "Babá de Time" ao "Engenheiro de Fluxo"</h2>
    <div class="th-sub">Um Scrum Master Júnior foca na pergunta: "O que você fez ontem?". Um SDM de nível 10k horas foca no Board: "Por que esse item não se moveu em 3 dias?". O SDM não gerencia pessoas (elas se autogerenciam); ele gerencia o FLUXO e o SISTEMA onde as pessoas operam.</div>
  </div>

  <div class="st">🛠️ A Caixa de Ferramentas (Downstream)</div>
  <div class="g2">
    <div class="card green">
      <div class="card-title">1. Item Aging Chart (Envelhecimento)</div>
      <p>A ferramenta mais poderosa do SDM para a Daily. Mostra visualmente quais itens estão há mais tempo na mesma coluna. Permite identificar gargalos antes do item violar o SLA de entrega.</p>
    </div>
    <div class="card green">
      <div class="card-title">2. Blocker Clustering</div>
      <p>Não basta destravar. O SDM anota a Categoria de cada bloqueio ("Dependência de Infra", "Aguardando PO"). No fim do mês, aplica um Pareto para atacar a causa raiz que gera 80% do tempo de espera.</p>
    </div>
  </div>

  <div class="st">🎬 Dinâmica de Execução: A Daily Orientada a Fluxo (Walking the Board)</div>
  <div class="how-to-teach">
    <div class="htt-title">Roteiro: Daily Standup de Elite (15 min)</div>
    <div class="htt-body">
      <strong>Regra de Ouro:</strong> Lemos o board da direita para a esquerda (do mais perto de terminar para o mais novo). Focamos no TRABALHO, não no trabalhador.<br><br>
      <strong>1. Bloqueios (3 min):</strong> Olhamos todos os cards com a flag "Blocked". O SDM pergunta: "Quem precisa se unir hoje para resolver o bloqueio X?"<br>
      <strong>2. Aging & Gargalos (7 min):</strong> O SDM aponta para os itens que violaram o WIP limit ou que estão envelhecendo (ex: 5 dias em QA). Pergunta: "Por que não terminou? Podemos fazer um Swarming (mutirão) neste card?"<br>
      <strong>3. Pull (5 min):</strong> Só após garantir que o fluxo existente está se movendo para a direita, olhamos a coluna de "Ready for Dev" para puxar itens novos se houver vaga no WIP limit.
    </div>
  </div>
</div>

<!-- PLAYBOOK 3: SISTÊMICO -->
<div id="s-mc-fluxo" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#9333ea,#7e22ce)">
    <div class="tag">MASTERCLASS 10K HORAS</div><h2>🌊 O Maestro Sistêmico (Flow Manager)</h2>
    <p>Playbook de execução avançada para otimização do End-to-End e Saúde da Organização</p>
  </div>
  
  <div class="teach-hero" style="background:linear-gradient(135deg, #4c1d95, #581c87);">
    <div class="th-tag">MENTALIDADE DE EXPERTISE</div>
    <h2>Visão Sistêmica sobre Local Optima</h2>
    <div class="th-sub">O Flow Manager sabe que otimizar uma etapa isolada (ex: fazer devs codarem mais rápido) enquanto QA está gargalado é burrice ("Local Optima"). Nível 10k horas é focar no "Global Optima": garantir a saúde de ponta a ponta e estabelecer previsibilidade matemática usando dados, não "Story Points" imaginários.</div>
  </div>

  <div class="st">🛠️ A Caixa de Ferramentas (Métricas e Previsão)</div>
  <div class="g2">
    <div class="card purple">
      <div class="card-title">1. Simulação de Monte Carlo</div>
      <p>Adeus planilhas de Burnup! O Flow Manager insere o histórico de Throughput em uma simulação probabilística para responder: "Qual a chance de entregarmos esses 10 épicos até dezembro?". Resultado em percentis (85% de confiança).</p>
    </div>
    <div class="card purple">
      <div class="card-title">2. Lei de Little (Little's Law)</div>
      <p>A fundação matemática (Cycle Time = WIP / Throughput). O Flow Manager usa isso para provar à diretoria: "Se aumentarmos a quantidade de projetos paralelos (WIP), o tempo de entrega de TUDO vai aumentar absurdamente."</p>
    </div>
  </div>

  <div class="st">🎬 Dinâmica de Execução: Operations Review (SDR)</div>
  <div class="how-to-teach">
    <div class="htt-title">Roteiro: Service Delivery Review Mensal (1 hora)</div>
    <div class="htt-body">
      <strong>Público:</strong> Liderança, POs, SDMs, Tech Leads.<br><br>
      <strong>1. Customer Fitness (15 min):</strong> Como estamos em relação ao nosso SLA de entrega de 85%? Apresentação do Cycle Time Scatterplot.<br>
      <strong>2. Eficiência de Fluxo (Flow Efficiency) (15 min):</strong> Onde o tempo foi gasto? "Nosso Touch Time é de 20%, e Wait Time é de 80%." (Analisar gargalos usando o Blocker Clustering).<br>
      <strong>3. Liquidez do Sistema (15 min):</strong> Avaliação do CFD. As bandas estão expandindo? Isso indica acúmulo de WIP ou entrada maior que saída. Onde o gargalo migrou este mês?<br>
      <strong>4. Ações Corretivas (15 min):</strong> "Para o mês que vem, vamos abaixar o WIP de QA de 3 para 2 e cross-treinar 1 Dev para ajudar nos testes."
    </div>
  </div>
</div>

<!-- PLAYBOOK 4: ENGENHARIA -->
<div id="s-mc-engenharia" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#c2410c,#9a3412)">
    <div class="tag">MASTERCLASS 10K HORAS</div><h2>⚙️ Engenharia e Execução (Tech Lead)</h2>
    <p>Playbook de execução avançada para Liderança Técnica e o Time de Desenvolvimento</p>
  </div>
  
  <div class="teach-hero" style="background:linear-gradient(135deg, #7c2d12, #9a3412);">
    <div class="th-tag">MENTALIDADE DE EXPERTISE</div>
    <h2>"Pare de Começar, Comece a Terminar"</h2>
    <div class="th-sub">Um Tech Lead 10k horas sabe que o código escrito mas não validado ou não deployado (Inventory) é passivo, não ativo. Ele defende a redução de WIP e atua politicamente para que o "Refinamento Técnico" quebre épicos de 3 meses em fatias integráveis de 3 dias.</div>
  </div>

  <div class="st">🛠️ A Caixa de Ferramentas (Tática de Engenharia)</div>
  <div class="g2">
    <div class="card orange">
      <div class="card-title">1. Swarming (Mutirão Técnico)</div>
      <p>Quando um item atinge o SLA de risco ou bloqueia o pipeline, o time "enxameia" o problema. Dois ou três devs abandonam suas tarefas menos prioritárias para atuar no gargalo (Pair/Mob Programming), garantindo o escoamento rápido.</p>
    </div>
    <div class="card orange">
      <div class="card-title">2. Políticas de WIP Pessoal e CI/CD</div>
      <p>Implementar limites rigorosos: nenhum dev deve ter mais de 1 PR (Pull Request) aberto ao mesmo tempo em revisão. Integrações devem ocorrer diariamente no "Trunk" para evitar Merge Hell no fim da semana.</p>
    </div>
  </div>

  <div class="st">🎬 Dinâmica de Execução: Quebra Funcional / Técnica</div>
  <div class="how-to-teach">
    <div class="htt-title">Roteiro: O Papel do Tech Lead no Upstream (Continuous Discovery)</div>
    <div class="htt-body">
      <strong>Abordagem:</strong> O Tech Lead não espera histórias escritas passivamente. Ele age junto ao SRM/PO.<br><br>
      <strong>1. Mitigação de Risco Técnico:</strong> O TL examina a fila antes do Refinamento. Identifica que a Feature Y exige migração de banco de dados e cria *Spikes* arquiteturais preventivos.<br>
      <strong>2. Estratégia de "Thin Slicing":</strong> Durante o refinamento com o time, o TL corta verticalmente: "Em vez de fazer o backend inteiro primeiro (que gera wait time), faremos o Cadastro básico full-stack esta semana. Semana que vem a validação avançada."<br>
      <strong>3. Gestão de Débito Técnico no Board:</strong> O TL negocia a alocação de capacidade (Ex: 20% do WIP Limit para itens de categoria 'Débito Técnico').
    </div>
  </div>
</div>

<!-- ======================================= -->
`;

content = content.replace('<div id="s-metricas-fluxo" class="section">', playbooksHtml + '\n<div id="s-metricas-fluxo" class="section">');
fs.writeFileSync(filePath, content, 'utf-8');
console.log('Playbooks inserted successfully.');
