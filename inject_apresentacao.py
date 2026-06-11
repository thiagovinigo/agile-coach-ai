import re

apresentacao_html = """
<!-- ==========================================
     APRESENTAÇÃO AO TIME (SCRUMBAN PITCH)
     ========================================== -->

<!-- 1. Paradigma do Fluxo -->
<div id="s-apresentacao-fluxo" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#0284c7,#0369a1)">
    <div class="tag">O NOVO MINDSET</div>
    <h2>🎯 A Culpa é do Fluxo, Não das Pessoas</h2>
    <p>Estabilização e previsibilidade através de acordos e limites</p>
  </div>
  
  <div class="card" style="border-left:5px solid #0284c7; padding:24px; margin-bottom:20px;">
    <h3 style="color:#0369a1; margin-top:0;">Por que estamos mudando?</h3>
    <p style="font-size:15px; line-height:1.6;">A mudança que estamos adotando não é para cobrar mais trabalho, mas sim para <strong>expor os problemas do sistema</strong>. Quando os prazos não são cumpridos ou há gargalos, a culpa raramente é do desenvolvedor que está lento. A culpa é do <strong>fluxo que permite a variabilidade desenfreada</strong>.</p>
    
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:20px;">
      <div style="background:#fef2f2; padding:16px; border-radius:8px;">
        <h4 style="color:#dc2626; margin-top:0;">❌ O Círculo Vicioso</h4>
        <ul class="chk" style="font-size:13px; margin:0;">
          <li>Muitas coisas começadas ao mesmo tempo</li>
          <li>Mudanças de contexto constantes (Multitasking)</li>
          <li>Gargalos invisíveis (ninguém sabe onde a tarefa travou)</li>
          <li>Alta pressão por prazo com baixa previsibilidade</li>
        </ul>
      </div>
      <div style="background:#f0fdf4; padding:16px; border-radius:8px;">
        <h4 style="color:#16a34a; margin-top:0;">✅ O Círculo Virtuoso (Scrumban)</h4>
        <ul class="chk" style="font-size:13px; margin:0;">
          <li>Foco total em terminar o que já começou</li>
          <li>Limites de trabalho em progresso (WIP) explícitos</li>
          <li>Trabalho colaborativo para destravar gargalos</li>
          <li>Métricas reais para prever entregas sem achismos</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<!-- 2. Touch vs Wait (Sistema Puxado) -->
<div id="s-apresentacao-pull" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#b45309,#92400e)">
    <div class="tag">MECÂNICA DO JOGO</div>
    <h2>✋ Touch vs Wait: O Fim do Empurrar</h2>
    <p>O verdadeiro significado de um Sistema Puxado</p>
  </div>

  <div class="alert alert-yellow" style="margin-bottom:20px;">
    <strong>O GRANDE MITO:</strong> "Terminei de programar, vou jogar o card para o QA testar."<br>
    <strong>A REALIDADE:</strong> Ninguém empurra trabalho para a próxima etapa. O trabalho é <em>puxado</em> por quem tem capacidade.
  </div>

  <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px;">
    <!-- Touch -->
    <div style="border:2px solid #3b82f6; border-radius:12px; overflow:hidden;">
      <div style="background:#3b82f6; color:#fff; padding:12px; text-align:center; font-weight:bold; font-size:18px;">
        ⚙️ TOUCH TIME (Tempo de Ação)
      </div>
      <div style="padding:16px; background:#eff6ff; font-size:14px; min-height:120px;">
        <p>São as colunas onde alguém está ativamente trabalhando no item.<br>Ex: <em>Em Desenvolvimento</em>, <em>Em Code Review</em>, <em>Em Testes</em>.</p>
        <p><strong>Regra:</strong> Estas colunas possuem <strong>WIP Limits rigorosos</strong> para impedir sobrecarga.</p>
      </div>
    </div>
    
    <!-- Wait -->
    <div style="border:2px solid #94a3b8; border-radius:12px; overflow:hidden;">
      <div style="background:#94a3b8; color:#fff; padding:12px; text-align:center; font-weight:bold; font-size:18px;">
        ⏳ WAIT TIME (Fila de Espera)
      </div>
      <div style="padding:16px; background:#f8fafc; font-size:14px; min-height:120px;">
        <p>São as colunas onde o item está parado, esperando alguém ter capacidade para puxar.<br>Ex: <em>Pronto para QA (Desenvolvido)</em>, <em>Aprovado (Testado)</em>.</p>
        <p><strong>Ação do Dev:</strong> Ao terminar de codar, você move para "Desenvolvido". Você <strong>NÃO</strong> move para "Em Teste". É o QA quem puxa de "Desenvolvido" para "Em Teste" quando ele terminar o teste atual dele.</p>
      </div>
    </div>
  </div>

  <div class="card" style="border-left:5px solid #b45309; padding:20px;">
    <h4 style="margin:0 0 10px; color:#92400e;">O que acontece se a fila de espera (Wait) encher?</h4>
    <p style="font-size:14px; margin:0;">Se a coluna "Desenvolvido" atingir seu limite de segurança, o Desenvolvedor <strong>não pode começar uma nova história</strong>. Em vez disso, ele deve ajudar a esvaziar o gargalo. Como? Ajudando no Code Review, escrevendo testes automatizados, ou pareando com o QA. <em>A meta do time é entregar valor, não apenas produzir código.</em></p>
  </div>
</div>

<!-- 3. O Quadro Completo -->
<div id="s-apresentacao-board" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#4c1d95,#5b21b6)">
    <div class="tag">FLUXO DE VALOR</div>
    <h2>🗺️ O Quadro Completo (Nosso Novo Board)</h2>
    <p>O fluxo de ponta a ponta com os limites de trabalho (WIP)</p>
  </div>

  <div style="overflow-x:auto; margin-bottom:20px; padding-bottom:10px;">
    <div style="display:inline-flex; gap:8px; min-width:max-content; background:#f1f5f9; padding:12px; border-radius:12px;">
      
      <!-- Backlog -->
      <div style="width:180px; background:#e2e8f0; border-radius:8px; padding:10px;">
        <div style="font-size:11px; font-weight:800; color:#475569; text-transform:uppercase;">1. Backlog Sprint</div>
        <div style="font-size:10px; color:#64748b; margin-bottom:12px;">(WIP: ∞) - Aguardando</div>
        <div style="background:#fff; border-left:3px solid #64748b; padding:8px; font-size:11px; margin-bottom:6px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">História A</div>
        <div style="background:#fff; border-left:3px solid #64748b; padding:8px; font-size:11px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">História B</div>
      </div>
      
      <!-- Doing (Touch) -->
      <div style="width:180px; background:#eff6ff; border:2px solid #3b82f6; border-radius:8px; padding:10px;">
        <div style="font-size:11px; font-weight:800; color:#1d4ed8; text-transform:uppercase;">2. Em Desenvol.</div>
        <div style="font-size:10px; color:#2563eb; font-weight:bold; margin-bottom:12px;">(WIP: 3) ⚙️ TOUCH</div>
        <div style="background:#fff; border-left:3px solid #3b82f6; padding:8px; font-size:11px; margin-bottom:6px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">História C <span style="float:right; font-size:10px; background:#dbeafe; padding:2px 4px; border-radius:4px;">Dev1</span></div>
        <div style="background:#fff; border-left:3px solid #3b82f6; padding:8px; font-size:11px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">História D <span style="float:right; font-size:10px; background:#dbeafe; padding:2px 4px; border-radius:4px;">Dev2</span></div>
      </div>
      
      <!-- Done (Wait) -->
      <div style="width:180px; background:#f8fafc; border:2px dashed #94a3b8; border-radius:8px; padding:10px;">
        <div style="font-size:11px; font-weight:800; color:#475569; text-transform:uppercase;">3. Desenvolvido</div>
        <div style="font-size:10px; color:#64748b; font-weight:bold; margin-bottom:12px;">(WIP: 4) ⏳ WAIT</div>
        <div style="background:#fff; border-left:3px solid #94a3b8; padding:8px; font-size:11px; margin-bottom:6px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">História E (Pronto QA)</div>
        <div style="text-align:center; font-size:10px; color:#94a3b8; margin-top:8px;">[Fila para QA puxar]</div>
      </div>
      
      <!-- QA (Touch) -->
      <div style="width:180px; background:#f0fdf4; border:2px solid #16a34a; border-radius:8px; padding:10px;">
        <div style="font-size:11px; font-weight:800; color:#15803d; text-transform:uppercase;">4. Em Teste (QA)</div>
        <div style="font-size:10px; color:#16a34a; font-weight:bold; margin-bottom:12px;">(WIP: 2) ⚙️ TOUCH</div>
        <div style="background:#fff; border-left:3px solid #16a34a; padding:8px; font-size:11px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">História F <span style="float:right; font-size:10px; background:#dcfce3; padding:2px 4px; border-radius:4px;">QA1</span></div>
      </div>
      
      <!-- Done -->
      <div style="width:180px; background:#e2e8f0; border-radius:8px; padding:10px;">
        <div style="font-size:11px; font-weight:800; color:#475569; text-transform:uppercase;">5. Done / Deploy</div>
        <div style="font-size:10px; color:#64748b; margin-bottom:12px;">Finalizado</div>
        <div style="background:#fff; border-left:3px solid #10b981; padding:8px; font-size:11px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">História G ✅</div>
      </div>

    </div>
  </div>

  <p style="font-size:14px;"><strong>Regra de Ouro:</strong> O desenvolvedor move da coluna 2 para a 3 e PARA de atuar naquele card. O QA, quando estiver livre, PUXA da coluna 3 para a coluna 4. O fluxo segue sempre dessa forma, sem jamais ser empurrado por cima de limites.</p>

</div>

<!-- 4. Acordos e Cerimônias -->
<div id="s-apresentacao-cerimonias" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#047857,#065f46)">
    <div class="tag">ROTINA & ACORDOS</div>
    <h2>🤝 Nossas Novas Cerimônias</h2>
    <p>Mudando o foco das pessoas para o fluxo</p>
  </div>

  <p style="font-size:15px; margin-bottom:20px;">No Scrum puro, as pessoas respondem "O que eu fiz ontem e o que vou fazer hoje". No Scrumban, <strong>não focamos nas pessoas, focamos nos cards parados no board</strong>.</p>

  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px; margin-bottom:24px;">
    
    <!-- Daily Kanban -->
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; overflow:hidden; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
      <div style="background:#047857; color:#fff; padding:16px; font-size:18px; font-weight:bold; display:flex; align-items:center; gap:10px;">
        <span>☀️</span> Daily Kanban
      </div>
      <div style="padding:20px;">
        <p style="font-size:13px; color:#475569; margin-top:0;"><strong>Dinâmica:</strong> O time lê o board da <em>DIREITA para a ESQUERDA</em>. Começamos olhando o que está quase terminando para empurrar pro Done, e só depois olhamos o que acabou de começar.</p>
        <div style="background:#f0fdf4; border-left:4px solid #16a34a; padding:12px; margin-top:16px;">
          <strong style="font-size:13px; color:#14532d; display:block; margin-bottom:8px;">Perguntas que DEVEMOS fazer:</strong>
          <ul class="chk" style="font-size:13px; margin:0; color:#166534;">
            <li>"Quem pode me ajudar a destravar esse card na coluna X?"</li>
            <li>"Esse card está há 3 dias no Wait do QA. Alguém do Dev pode ajudar a testar?"</li>
            <li>"Estamos perto do WIP Limit de Desenvolvimento, devemos focar em limpar a fila de testes?"</li>
            <li>"Temos algum card impedido formalmente?"</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Replenishment -->
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; overflow:hidden; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
      <div style="background:#7c3aed; color:#fff; padding:16px; font-size:18px; font-weight:bold; display:flex; align-items:center; gap:10px;">
        <span>🔋</span> Replenishment (Reabastecimento)
      </div>
      <div style="padding:20px;">
        <p style="font-size:13px; color:#475569; margin-top:0;"><strong>Dinâmica:</strong> Substitui parcialmente a Planning pesada. É uma reunião de cadência para pegar itens do Backlog de Produto e colocar no Backlog da Sprint/To Do.</p>
        <div style="background:#faf5ff; border-left:4px solid #7c3aed; padding:12px; margin-top:16px;">
          <strong style="font-size:13px; color:#4c1d95; display:block; margin-bottom:8px;">Perguntas que DEVEMOS fazer:</strong>
          <ul class="chk" style="font-size:13px; margin:0; color:#5b21b6;">
            <li>"Qual a nossa capacidade real de puxar novos itens hoje?"</li>
            <li>"Estes cards respeitam as políticas de Definition of Ready (DoR)?"</li>
            <li>"Qual o card mais valioso ou com maior custo de atraso agora?"</li>
            <li>"Temos classes de serviço expedientes (bugs urgentes) na frente da fila?"</li>
          </ul>
        </div>
      </div>
    </div>

  </div>
</div>
"""

with open('contexto/scrumban_guia.html', 'a', encoding='utf-8') as f:
    f.write("\n" + apresentacao_html)
print("Apresentação content appended successfully!")
