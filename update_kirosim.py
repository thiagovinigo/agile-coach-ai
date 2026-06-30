import re

app_js_path = 'c:/Users/User/.antigravity/Agile Coach AI/app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_kiro_sim = """{
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
        { col: 1, cmd: "> kiro run ecc/blueprint --work-item=101", out: "<span style='color:#3b82f6;'>[MCP TFS]</span> Lendo Descrição do Work Item 101...<br><span style='color:#a855f7;'>[Steering]</span> Aplicando Política: 'Gerar PRD e Critérios BDD'. <a href='javascript:void(0)' onclick='openInfoModalDirect(\"skills/refinamento/SKILL\")' style='color:#fde047; text-decoration:underline;'>[Ver Skill]</a><br><span style='color:#10b981;'>[Kiro]</span> Artefato 'PRD.md' gerado.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Aguardando Refinamento Técnico'" },
        { col: 2, cmd: "# Fila de Transição", out: "<span style='color:#6b7280;'>// O card está em uma fila (buffer). A IA terminou o trabalho funcional.</span><br><span style='color:#6b7280;'>// O Kiro Architect aguarda capacidade para puxar.</span>" },
        { col: 3, cmd: "> kiro run ecc/architecture-decision-records --work-item=101", out: "<span style='color:#3b82f6;'>[MCP TFS]</span> Lendo PRD.md...<br><span style='color:#10b981;'>[Kiro]</span> Artefato 'Design_Spec.md' gerado. <a href='javascript:void(0)' onclick='openInfoModalDirect(\"skills/arquitetura/SKILL\")' style='color:#fde047; text-decoration:underline;'>[Ver Skill]</a><br><span style='color:#3b82f6;'>[MCP TFS]</span> Quebrando Work Item 101 em 3 sub-tasks.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Aguardando Avaliação PO'" },
        { col: 4, cmd: "@Kiro, aprovar spec.", out: "<span style='color:#f59e0b;'>[Gate Humano]</span> O Kiro parou de processar.<br><span style='color:#a855f7;'>[Usuário]</span> Digita '/approve'.<br><span style='color:#3b82f6;'>[MCP TFS]</span> Movendo para 'Em Desenvolvimento'." },
        { col: 5, cmd: "> kiro run ecc/tdd-workflow", out: "<span style='color:#ef4444;'>[Kiro Test]</span> Executando login.spec.ts -> <b>FALHA</b>.<br><span style='color:#10b981;'>[Kiro Code]</span> Implementando login.ts -> <b>PASSOU</b>. <a href='javascript:void(0)' onclick='openInfoModalDirect(\"skills/engenheiro-software/SKILL\")' style='color:#fde047; text-decoration:underline;'>[Ver Skill]</a><br><span style='color:#eab308;'>[Git]</span> Commit automático: 'feat: add OTP login'.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Em Teste'." },
        { col: 6, cmd: "> kiro run ecc/security-review", out: "<span style='color:#10b981;'>[Kiro QA]</span> Executando testes E2E.<br><span style='color:#a855f7;'>[Kiro Security]</span> Scan OWASP: 0 vulnerabilidades. <a href='javascript:void(0)' onclick='openInfoModalDirect(\"skills/engenharia-qa/SKILL\")' style='color:#fde047; text-decoration:underline;'>[Ver Skill]</a><br><span style='color:#3b82f6;'>[MCP TFS]</span> Inserindo evidências no Test Plan.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Aguardando Avaliação PO'." },
        { col: 7, cmd: "@Kiro, aprovar QA.", out: "<span style='color:#f59e0b;'>[Gate Final]</span> O PO analisa evidências.<br><span style='color:#a855f7;'>[Usuário]</span> Digita '/approve-deploy'.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Liberado para Instalar'." },
        { col: 8, cmd: "# Azure Pipelines Trigger", out: "<span style='color:#10b981;'>[Pipeline]</span> Gatilho detectado via Webhook.<br><span style='color:#6b7280;'>// Pipeline executando build e deploy.</span><br><span style='color:#3b82f6;'>[MCP TFS]</span> Ao sucesso do deploy, move para 'Done'." },
        { col: 9, cmd: "# Concluído", out: "<span style='color:#10b981;'>✅ Ciclo de vida encerrado.</span><br><span style='color:#6b7280;'>// Métricas de Lead Time registradas nativamente no TFS.</span>" }
      ],
      init() {
        const board = document.getElementById('sim-board');
        if(!board) return;
        board.innerHTML = '';
        this.columns.forEach((c, idx) => {
          board.innerHTML += `
            <div class="sim-col ${idx===this.currentStep ? 'active-col' : ''}" id="col-${idx}">
              <div class="sim-col-title">${c.name}</div>
              ${idx === this.currentStep ? this.getCardHTML() : ''}
            </div>
          `;
        });
        this.renderTerminal();
        this.updateButtons();
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
      renderTerminal() {
        const step = this.steps[this.currentStep];
        document.getElementById('sim-step-num').innerText = (this.currentStep + 1);
        document.getElementById('sim-terminal').innerHTML = `
          <div style="color:#fde047; margin-bottom:10px;">${step.cmd}</div>
          <div>${step.out}</div>
        `;
      },
      updateButtons() {
        const btnNext = document.getElementById('btn-next-step');
        const btnPrev = document.getElementById('btn-prev-step');
        
        if(this.currentStep === this.steps.length - 1) {
          btnNext.innerText = "✅ Concluído";
          btnNext.style.background = "#10b981";
          btnNext.disabled = true;
          btnNext.style.opacity = "0.5";
        } else {
          btnNext.innerText = "▶ Próximo Passo";
          btnNext.style.background = "#3b82f6";
          btnNext.disabled = false;
          btnNext.style.opacity = "1";
        }

        if(this.currentStep === 0) {
          btnPrev.disabled = true;
          btnPrev.style.opacity = "0.5";
        } else {
          btnPrev.disabled = false;
          btnPrev.style.opacity = "1";
        }
      },
      nextStep() {
        if (this.currentStep >= this.steps.length - 1) return;
        this.currentStep++;
        this.init(); // re-render
      },
      prevStep() {
        if (this.currentStep <= 0) return;
        this.currentStep--;
        this.init(); // re-render
      },
      resetStep() {
        this.currentStep = 0;
        this.init();
      }
    }"""

new_content = re.sub(r'window\.kiroSim = \{.*?\};\n', f'window.kiroSim = {new_kiro_sim};\n', content, flags=re.DOTALL)

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated kiroSim in app.js")
