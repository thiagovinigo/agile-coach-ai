# encoding: utf-8
import os

html_content = """
<!-- ===== KIRO HUB ===== -->
<div id="s-kiro-hub" class="section">
  
  <div class="page-header" style="background:linear-gradient(135deg,#000000,#111827)">
    <div class="tag" style="background:#3b82f6;">MÃO NA MASSA</div>
    <h2>💻 Kiro: Simulador Hands-on e Laboratório</h2>
    <p>Simule o ciclo de vida de um card sendo operado por IA no Board em tempo real, e depois aprenda como fabricar essas automações para sua equipe.</p>
  </div>

  <!-- PARTE 1: SIMULADOR JS -->
  <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:10px; padding:20px; margin-bottom:40px; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
      <div>
        <h3 style="margin:0; color:#0f172a;">Simulador Interativo</h3>
        <p style="margin:5px 0 0 0; font-size:12px; color:#475569;">Clique no botão para avançar o card (#101 Login OTP) pelas 10 colunas e veja o comportamento da IDE.</p>
      </div>
      <button id="btn-next-step" onclick="kiroSim.nextStep()" style="background:#3b82f6; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:14px; box-shadow:0 2px 4px rgba(59,130,246,0.3); transition: background 0.2s;">
        ▶ Próximo Passo: Rodar IA
      </button>
    </div>

    <!-- O Board Kanban (Horizontal) -->
    <div style="display:flex; gap:10px; overflow-x:auto; padding-bottom:15px; min-height:180px;" id="sim-board">
      
      <!-- Colunas serão geradas via JS, mas deixamos a estrutura base -->
      <style>
        .sim-col { flex: 0 0 160px; background:#e2e8f0; border-radius:6px; padding:8px; display:flex; flex-direction:column; border: 1px solid #cbd5e1; }
        .sim-col-title { font-size:11px; font-weight:bold; color:#334155; text-align:center; margin-bottom:10px; min-height:30px; display:flex; align-items:center; justify-content:center; }
        .sim-card { background:white; border-left:4px solid #3b82f6; border-radius:4px; padding:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1); font-size:12px; color:#0f172a; transition: all 0.3s ease; animation: pulseCard 2s infinite; }
        .sim-card .tag { font-size:9px; background:#fef08a; padding:2px 4px; border-radius:4px; color:#854d0e; display:inline-block; margin-top:5px; }
        .active-col { background: #dbeafe; border-color: #93c5fd; }
        @keyframes pulseCard { 0% { box-shadow: 0 1px 3px rgba(0,0,0,0.1); } 50% { box-shadow: 0 0 8px rgba(59,130,246,0.6); } 100% { box-shadow: 0 1px 3px rgba(0,0,0,0.1); } }
      </style>

    </div>

    <!-- O Terminal Kiro -->
    <div style="background:#0f172a; border-radius:8px; margin-top:20px; border:1px solid #334155; display:flex; flex-direction:column; overflow:hidden;">
      <div style="background:#1e293b; padding:8px 15px; font-size:11px; color:#94a3b8; font-weight:bold; display:flex; align-items:center; gap:8px; border-bottom:1px solid #334155;">
        <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#ef4444;"></span>
        <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#f59e0b;"></span>
        <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#10b981;"></span>
        <span style="margin-left:10px;">IDE / KIRO TERMINAL - PASSO <span id="sim-step-num">1</span>/10</span>
      </div>
      <div id="sim-terminal" style="padding:15px; font-family:'Courier New', Courier, monospace; font-size:13px; color:#e2e8f0; min-height:120px; line-height:1.6;">
        <div style="color:#fde047; margin-bottom:10px;"># Ambiente Kiro Idle</div>
        <div style="color:#6b7280;">// O PO acaba de criar a ideia bruta no TFS.</div>
        <div style="color:#6b7280;">// O Kiro aguarda o item ser puxado para a esteira (Pull).</div>
      </div>
    </div>
  </div>

  <script>
    const kiroSim = {
      currentStep: 0,
      columns: [
        { id: 'c1', name: 'New' },
        { id: 'c2', name: 'Ref. Funcional (IA)' },
        { id: 'c3', name: 'Ag. Ref Técnico' },
        { id: 'c4', name: 'Em Ref. (IA)' },
        { id: 'c5', name: 'Aguardando PO' },
        { id: 'c6', name: 'Em Dev (IA)' },
        { id: 'c7', name: 'Em Teste (IA)' },
        { id: 'c8', name: 'Ag. PO (Final)' },
        { id: 'c9', name: 'Lib. Instalar' },
        { id: 'c10', name: 'Done' }
      ],
      steps: [
        { col: 0, cmd: "# Ambiente Kiro Idle", out: "<span style='color:#6b7280;'>// O PO acaba de criar a ideia bruta no TFS.</span><br><span style='color:#6b7280;'>// O Kiro aguarda o item ser puxado para a esteira (Pull).</span>" },
        { col: 1, cmd: "> kiro run ecc/blueprint --work-item=101", out: "<span style='color:#3b82f6;'>[MCP TFS]</span> Lendo Descrição do Work Item 101...<br><span style='color:#a855f7;'>[Steering]</span> Aplicando Política: 'Gerar PRD e Critérios BDD'.<br><span style='color:#10b981;'>[Kiro]</span> Artefato 'PRD.md' gerado.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Aguardando Refinamento Técnico'" },
        { col: 2, cmd: "# Fila de Transição", out: "<span style='color:#6b7280;'>// O card está em uma fila (buffer). A IA terminou o trabalho funcional.</span><br><span style='color:#6b7280;'>// O Kiro Architect aguarda capacidade para puxar.</span>" },
        { col: 3, cmd: "> kiro run ecc/architecture-decision-records --work-item=101", out: "<span style='color:#3b82f6;'>[MCP TFS]</span> Lendo PRD.md...<br><span style='color:#10b981;'>[Kiro]</span> Artefato 'Design_Spec.md' gerado.<br><span style='color:#3b82f6;'>[MCP TFS]</span> Quebrando Work Item 101 em 3 sub-tasks.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Aguardando Avaliação PO'" },
        { col: 4, cmd: "@Kiro, aprovar spec.", out: "<span style='color:#f59e0b;'>[Gate Humano]</span> O Kiro parou de processar.<br><span style='color:#a855f7;'>[Usuário]</span> Digita '/approve'.<br><span style='color:#3b82f6;'>[MCP TFS]</span> Movendo para 'Em Desenvolvimento'." },
        { col: 5, cmd: "> kiro run ecc/tdd-workflow", out: "<span style='color:#ef4444;'>[Kiro Test]</span> Executando login.spec.ts -> <b>FALHA</b>.<br><span style='color:#10b981;'>[Kiro Code]</span> Implementando login.ts -> <b>PASSOU</b>.<br><span style='color:#eab308;'>[Git]</span> Commit automático: 'feat: add OTP login'.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Em Teste'." },
        { col: 6, cmd: "> kiro run ecc/security-review", out: "<span style='color:#10b981;'>[Kiro QA]</span> Executando testes E2E.<br><span style='color:#a855f7;'>[Kiro Security]</span> Scan OWASP: 0 vulnerabilidades.<br><span style='color:#3b82f6;'>[MCP TFS]</span> Inserindo evidências no Test Plan.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Aguardando Avaliação PO'." },
        { col: 7, cmd: "@Kiro, aprovar QA.", out: "<span style='color:#f59e0b;'>[Gate Final]</span> O PO analisa evidências.<br><span style='color:#a855f7;'>[Usuário]</span> Digita '/approve-deploy'.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Liberado para Instalar'." },
        { col: 8, cmd: "# Azure Pipelines Trigger", out: "<span style='color:#10b981;'>[Pipeline]</span> Gatilho detectado via Webhook.<br><span style='color:#6b7280;'>// Pipeline executando build e deploy.</span><br><span style='color:#3b82f6;'>[MCP TFS]</span> Ao sucesso do deploy, move para 'Done'." },
        { col: 9, cmd: "# Concluído", out: "<span style='color:#10b981;'>✅ Ciclo de vida encerrado.</span><br><span style='color:#6b7280;'>// Métricas de Lead Time registradas nativamente no TFS.</span>" }
      ],
      init() {
        const board = document.getElementById('sim-board');
        board.innerHTML = '';
        this.columns.forEach((c, idx) => {
          board.innerHTML += `
            <div class="sim-col ${idx===0 ? 'active-col' : ''}" id="col-${idx}">
              <div class="sim-col-title">${c.name}</div>
              ${idx === 0 ? this.getCardHTML() : ''}
            </div>
          `;
        });
      },
      getCardHTML() {
        return `
          <div class="sim-card" id="simulated-card">
            <div style="font-size:10px; color:#94a3b8;">ID: #101</div>
            <strong>Login via OTP</strong>
            <div class="tag">AI-Guided</div>
          </div>
        `;
      },
      nextStep() {
        if (this.currentStep >= this.steps.length - 1) {
          alert("O ciclo já foi concluído e chegou em Done!");
          return;
        }
        
        this.currentStep++;
        const step = this.steps[this.currentStep];
        
        // Remove card from previous columns
        for(let i=0; i<this.columns.length; i++){
          document.getElementById('col-'+i).classList.remove('active-col');
          const card = document.getElementById('col-'+i).querySelector('.sim-card');
          if(card) card.remove();
        }
        
        // Add card to new column
        const targetCol = document.getElementById('col-'+step.col);
        targetCol.classList.add('active-col');
        targetCol.innerHTML += this.getCardHTML();
        
        // Update Terminal
        document.getElementById('sim-step-num').innerText = (this.currentStep + 1);
        document.getElementById('sim-terminal').innerHTML = `
          <div style="color:#fde047; margin-bottom:10px;">${step.cmd}</div>
          <div>${step.out}</div>
        `;

        // Update button text if Done
        if(this.currentStep === this.steps.length - 1) {
          document.getElementById('btn-next-step').innerText = "✅ Fluxo Concluído";
          document.getElementById('btn-next-step').style.background = "#10b981";
        }
      }
    };
    
    // Auto-init when DOM loads or script runs
    setTimeout(() => { kiroSim.init(); }, 500);
  </script>

  <hr style="border:0; border-top:1px solid #e2e8f0; margin:40px 0;">

  <!-- PARTE 2: ESTUDO E IMPLEMENTAÇÃO -->
  <div class="page-header" style="background:linear-gradient(135deg,#1e1b4b,#4c1d95)">
    <div class="tag" style="background:#8b5cf6;">LABORATÓRIO</div>
    <h2>🧪 Criando Skills e Operando em Lote</h2>
    <p>Aprenda como fabricar a automação que você acabou de ver no simulador acima.</p>
  </div>

  <!-- 1. Catálogo de Agentes -->
  <h3 style="margin:30px 0 15px; color:#1e293b; border-bottom:2px solid #8b5cf6; padding-bottom:8px;">👥 1. Catálogo de Agentes Prontos</h3>
  <div style="display:flex; gap:15px; flex-wrap:wrap; margin-bottom:30px;">
    
    <div style="flex:1; min-width:200px; background:#fff; border:1px solid #d1d5db; border-radius:8px; padding:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05); text-align:center;">
      <div style="font-size:36px; margin-bottom:10px;">📋</div>
      <strong style="color:#111827; font-size:15px; display:block;">Agente Planner</strong>
      <p style="font-size:12px; color:#475569; margin-top:10px; line-height:1.4;">Lê a demanda bruta, entende o escopo e escreve o PRD em formato BDD.</p>
    </div>

    <div style="flex:1; min-width:200px; background:#fff; border:1px solid #d1d5db; border-radius:8px; padding:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05); text-align:center;">
      <div style="font-size:36px; margin-bottom:10px;">📐</div>
      <strong style="color:#111827; font-size:15px; display:block;">Agente Architect</strong>
      <p style="font-size:12px; color:#475569; margin-top:10px; line-height:1.4;">Transforma o PRD em Spec Técnica e quebra subtarefas.</p>
    </div>

    <div style="flex:1; min-width:200px; background:#fff; border:1px solid #d1d5db; border-radius:8px; padding:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05); text-align:center;">
      <div style="font-size:36px; margin-bottom:10px;">🧑‍💻</div>
      <strong style="color:#111827; font-size:15px; display:block;">Agente TDD / Coder</strong>
      <p style="font-size:12px; color:#475569; margin-top:10px; line-height:1.4;">Codifica a feature seguindo a regra Red-Green-Refactor.</p>
    </div>

    <div style="flex:1; min-width:200px; background:#fff; border:1px solid #d1d5db; border-radius:8px; padding:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05); text-align:center;">
      <div style="font-size:36px; margin-bottom:10px;">🛡️</div>
      <strong style="color:#111827; font-size:15px; display:block;">Agente QA & Sec</strong>
      <p style="font-size:12px; color:#475569; margin-top:10px; line-height:1.4;">Varre o código contra OWASP e testa os Acceptance Criteria.</p>
    </div>

  </div>

  <!-- 2. Criando uma Skill End-to-End -->
  <h3 style="margin:30px 0 15px; color:#1e293b; border-bottom:2px solid #8b5cf6; padding-bottom:8px;">🛠️ 2. Como criar um Agente (O Código)</h3>
  
  <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:20px; margin-bottom:30px;">
    
    <div style="margin-bottom:20px;">
      <strong style="color:#0f172a; font-size:15px; display:block; margin-bottom:5px;">O Arquivo SKILL.md (O Prompt Real)</strong>
      <p style="font-size:13px; color:#475569; margin:0 0 10px 0;">Copie esta estrutura abaixo, ela é 100% real, usa marcações XML, chamadas de ferramentas e regras de Governança estritas para o Kiro/Claude:</p>
      
      <div style="background:#1e293b; color:#f8fafc; padding:15px; border-radius:6px; font-family:monospace; font-size:12px; border-left:4px solid #a855f7; line-height: 1.5; overflow-x: auto; white-space: pre;"><span style="color:#a855f7;">&lt;role&gt;</span>
Você é o Agente Planner, especialista em Engenharia de Requisitos e BDD.
Sua missão é extrair a intenção bruta do Work Item do TFS e formatá-la em um PRD formal.
<span style="color:#a855f7;">&lt;/role&gt;</span>

<span style="color:#3b82f6;">&lt;instructions&gt;</span>
1. Use a ferramenta `azure-devops_get_work_item` do MCP para ler o ID.
2. Analise o conteúdo do campo `System.Description`.
3. Escreva um artefato no projeto chamado `PRD.md`.
<span style="color:#3b82f6;">&lt;/instructions&gt;</span>

<span style="color:#ef4444;">&lt;governance_rules&gt;</span>
- NUNCA alucine regras de negócio. Se a descrição for curta, PARE.
- Use OBRIGATORIAMENTE a ferramenta `azure-devops_update_work_item` para travar o card:
  [ { "op": "add", "path": "/fields/System.Tags", "value": "DEP-Negocio" } ]
<span style="color:#ef4444;">&lt;/governance_rules&gt;</span>

<span style="color:#10b981;">&lt;mcp_trigger&gt;</span>
Se o arquivo `PRD.md` for gerado, DEVOLVA O BASTÃO movendo o card. 
Use a ferramenta `azure-devops_update_work_item` com o PATCH:
[ { "op": "add", "path": "/fields/System.State", "value": "Aguardando Refinamento Técnico" } ]
<span style="color:#10b981;">&lt;/mcp_trigger&gt;</span></div>
    </div>
  </div>

  <!-- 3. Executando Múltiplos Itens (Lote) -->
  <h3 style="margin:30px 0 15px; color:#1e293b; border-bottom:2px solid #8b5cf6; padding-bottom:8px;">🏭 3. Processamento em Lote (Limpando a Fila)</h3>
  <p style="font-size:14px; color:#475569; margin-bottom:20px;">No mundo real, o PO coloca 5 ou 10 itens na coluna "New". O <strong>Agente de Ronda (Cron Job)</strong> acorda e puxa vários itens em paralelo.</p>

  <div style="display:flex; gap:15px; flex-wrap:wrap; margin-bottom:20px;">
    
    <!-- Esquerda: Fila Visual -->
    <div style="flex:1; min-width:250px; background:#fff7ed; padding:20px; border:1px solid #fdba74; border-radius:8px;">
      <strong style="color:#9a3412; font-size:15px; display:block; margin-bottom:10px;">Coluna: New (Entrada)</strong>
      
      <div style="background:#fff; border-left:4px solid #9ca3af; padding:8px; margin-bottom:8px; font-size:12px; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
        <strong style="color:#374151;">#101</strong> - Login via OTP <span style="float:right; color:#a855f7;">[Na fila]</span>
      </div>
      <div style="background:#fff; border-left:4px solid #9ca3af; padding:8px; margin-bottom:8px; font-size:12px; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
        <strong style="color:#374151;">#102</strong> - Tela de Perfil <span style="float:right; color:#a855f7;">[Na fila]</span>
      </div>
      <div style="background:#fff; border-left:4px solid #9ca3af; padding:8px; margin-bottom:8px; font-size:12px; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
        <strong style="color:#374151;">#103</strong> - Esqueci Senha <span style="float:right; color:#a855f7;">[Na fila]</span>
      </div>
    </div>

    <!-- Direita: Terminal Paralelo -->
    <div style="flex:1.5; min-width:300px; background:#0f172a; padding:20px; border-radius:8px; border:1px solid #334155;">
      <strong style="color:#6ee7b7; font-size:13px; display:block; margin-bottom:10px; font-family:monospace;">> cron_job.sh --trigger-agent=planner --limit=5</strong>
      <div style="font-family:monospace; font-size:11px; color:#e2e8f0; line-height:1.6;">
        <span style="color:#60a5fa;">[MCP Query]</span> SELECT * FROM WorkItems WHERE State='New' LIMIT 5<br>
        <span style="color:#10b981;">[Found]</span> 3 itens retornados: [101, 102, 103].<br>
        <span style="color:#a855f7;">[Kiro Dispatcher]</span> Iniciando 3 threads paralelas...<br>
        <br>
        <span style="color:#9ca3af;">[Thread 1]</span> Card #101 processando PRD...<br>
        <span style="color:#9ca3af;">[Thread 2]</span> Card #102 processando PRD...<br>
        <span style="color:#9ca3af;">[Thread 3]</span> Card #103 processando PRD...<br>
        <br>
        <span style="color:#3b82f6;">[MCP Patch]</span> #101 Movido -> Ref. Funcional.<br>
        <span style="color:#ef4444;">[MCP Patch]</span> #102 REJEITADO (Regra Governance). Tag <b>DEP-Negocio</b> aplicada.<br>
        <span style="color:#3b82f6;">[MCP Patch]</span> #103 Movido -> Ref. Funcional.<br>
        <br>
        <span style="color:#10b981;">✅ Execução em Lote Finalizada (Tempo: 42s).</span>
      </div>
    </div>
  </div>

</div>
<!-- ===== FIM KIRO HUB ===== -->
"""

with open('c:/Users/User/.antigravity/Agile Coach AI/contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

target = "<!-- ===== PO: REFINAMENTO EFICAZ ===== -->"
if target in orig_html:
    new_html = orig_html.replace(target, html_content + "\n" + target)
    with open('c:/Users/User/.antigravity/Agile Coach AI/contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Injected Kiro Hub successfully.")
else:
    print("Target not found for injecting Kiro Hub.")
