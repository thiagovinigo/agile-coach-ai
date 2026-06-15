// fluxo_ia.js

const fluxoIaData = [
  {
    id: 1,
    title: "1. New",
    board: {
      column: "New",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["Business"] },
        { id: 102, title: "Perfil do Usuário", tags: ["UX"] }
      ]
    },
    agent: {
      name: "Agente Ocioso",
      icon: "💤",
      desc: "Nenhum agente opera na coluna New. Os itens aguardam serem puxados (Pull) pelo Agente Planner através de um gatilho."
    },
    skill: `Nenhuma Skill aplicada.
O gatilho de transição (Webhook ou Batch Polling) observa a coluna "New".
Quando disparado, move o Card #101 para "Refinamento Funcional (IA)".`,
    log: `# Ambiente Kiro Idle
// O PO acabou de criar ideias brutas no TFS.
// O Agente de Ronda aguarda para puxar os itens (Cron).`
  },
  {
    id: 2,
    title: "2. Ref Funcional",
    board: {
      column: "Ref. Funcional (IA)",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "Gerando PRD"] }
      ]
    },
    agent: {
      name: "Agente Planner",
      icon: "📋",
      desc: "Lê a descrição bruta do PO e cria um PRD maduro no formato BDD. Exige regras de negócio mínimas."
    },
    skill: `<role>Você é o Agente Planner, especialista BDD.</role>
<instructions>
1. Leia a descrição do item usando MCP.
2. Gere o PRD.md
</instructions>
<governance_rules>
NUNCA alucine. Se faltar dados, rejeite o card aplicando a tag DEP-Negocio via MCP.
</governance_rules>
<mcp_trigger>PATCH System.State = 'Ag. Ref Técnico'</mcp_trigger>`,
    log: `> kiro run ecc/blueprint --work-item=101
[MCP TFS] Lendo Descrição do Work Item 101...
[Steering] Validando Governança (Regras OK).
[Kiro] Artefato 'PRD.md' gerado com sucesso.
[MCP TFS] Movendo para 'Ag. Ref Técnico'.`
  },
  {
    id: 3,
    title: "3. Ag. Ref Técnico",
    board: {
      column: "Ag. Ref Técnico",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["PRD Pronto"] }
      ]
    },
    agent: {
      name: "Fila (Buffer)",
      icon: "⏸️",
      desc: "O Card fica em compasso de espera até que o Kiro Architect tenha capacidade de puxar."
    },
    skill: `Nenhuma configuração ativa. Card em Fila.`,
    log: `# Fila de Transição
// O card está aguardando o Agente Arquiteto puxar (WIP Limit).`
  },
  {
    id: 4,
    title: "4. Ref Técnico (IA)",
    board: {
      column: "Em Ref. Técnico (IA)",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "Arquitetura"] }
      ]
    },
    agent: {
      name: "Agente Architect",
      icon: "📐",
      desc: "Quebra o PRD em Design Técnico e Subtarefas de Engenharia."
    },
    skill: `<role>Você é o Arquiteto de Software.</role>
<instructions>
1. Leia PRD.md
2. Crie Design_Spec.md e quebre em sub-tasks no TFS usando MCP.
</instructions>
<mcp_trigger>PATCH System.State = 'Ag. Avaliação PO'</mcp_trigger>`,
    log: `> kiro run ecc/architecture-decision-records
[MCP TFS] Lendo PRD.md...
[Kiro] Artefato 'Design_Spec.md' gerado.
[MCP TFS] Criando 3 Child Tasks (API, Frontend, DB).
[MCP TFS] Movendo para 'Aguardando PO'.`
  },
  {
    id: 5,
    title: "5. Ag. PO (Gate)",
    board: {
      column: "Aguardando PO",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["Humano Requerido"] }
      ]
    },
    agent: {
      name: "Gate Humano (PO)",
      icon: "🧑‍💼",
      desc: "Quality Gate: A IA para de agir e exige que um ser humano aprove a arquitetura antes de codar."
    },
    skill: `// O Kiro aguarda aprovação humana via chat
@Kiro, aprovar spec.`,
    log: `[Gate Humano] Kiro paralisado.
[Usuário] Digita '/approve'.
[MCP TFS] Movendo para 'Em Desenvolvimento'.`
  },
  {
    id: 6,
    title: "6. Em Dev (IA)",
    board: {
      column: "Em Desenvolvimento",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "Coding"] }
      ]
    },
    agent: {
      name: "Agente Coder (TDD)",
      icon: "🧑‍💻",
      desc: "Escreve o teste, faz falhar (Red), coda a solução (Green), refatora e faz o Commit via Git MCP."
    },
    skill: `<role>Você é o Software Engineer focado em TDD.</role>
<instructions>
1. Escreva o teste.
2. Implemente o código.
3. Faça o commit usando \`git_commit\`.
</instructions>
<mcp_trigger>PATCH System.State = 'Em Teste'</mcp_trigger>`,
    log: `> kiro run ecc/tdd-workflow
[Kiro Test] login.spec.ts -> FALHA (Red).
[Kiro Code] login.ts -> PASSOU (Green).
[Git MCP] git commit -m "feat: login OTP"
[MCP TFS] Movendo para 'Em Teste'.`
  },
  {
    id: 7,
    title: "7. Em Teste (IA)",
    board: {
      column: "Em Teste",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "QA & Sec"] }
      ]
    },
    agent: {
      name: "Agente QA & Sec",
      icon: "🛡️",
      desc: "Roda testes E2E, varredura de segurança OWASP e documenta evidências no TFS Test Plans."
    },
    skill: `<role>Você é o Engenheiro de QA e Segurança.</role>
<instructions>
1. Rode os testes de interface.
2. Escaneie contra OWASP.
3. Anexe evidências ao Card.
</instructions>
<mcp_trigger>PATCH System.State = 'Ag. Liberação PO'</mcp_trigger>`,
    log: `> kiro run ecc/security-review
[QA] Testes End-to-End aprovados.
[Security] Scan OWASP: 0 vulnerabilidades Críticas.
[MCP TFS] Evidências anexadas.
[MCP TFS] Movendo para 'Aguardando PO'.`
  },
  {
    id: 8,
    title: "8. Ag. PO (Final)",
    board: {
      column: "Ag. PO (Final)",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["Pronto para Deploy"] }
      ]
    },
    agent: {
      name: "Gate Humano (PO)",
      icon: "🧑‍💼",
      desc: "O PO revisa os testes e aceita a entrega da IA."
    },
    skill: `// O Kiro aguarda a aprovação final.
@Kiro, aprovar QA e liberar.`,
    log: `[Gate Final] PO revisa as evidências de segurança e negócio.
[Usuário] Digita '/approve-deploy'.
[MCP TFS] Movendo para 'Liberado para Instalar'.`
  },
  {
    id: 9,
    title: "9. Lib Instalar",
    board: {
      column: "Liberado para Instalar",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["CI/CD Pipeline"] }
      ]
    },
    agent: {
      name: "Pipeline (DevOps)",
      icon: "🚀",
      desc: "Esteira automatizada do Azure DevOps (CI/CD) assume o trabalho para jogar em produção."
    },
    skill: `trigger:
- master
pool:
  vmImage: ubuntu-latest
steps:
- script: npm run build`,
    log: `# Azure Pipelines
[Pipeline] Gatilho Webhook disparado.
[Build] Compilando assets... OK.
[Deploy] Enviando para Produção... OK.
[MCP TFS] Atualizando card para 'Done'.`
  },
  {
    id: 10,
    title: "10. Done",
    board: {
      column: "Done",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["Em Produção"] }
      ]
    },
    agent: {
      name: "Métricas TFS",
      icon: "📈",
      desc: "O card morre. O TFS computa o Lead Time automaticamente, mostrando ganho de 80% de produtividade."
    },
    skill: `Nenhuma ação requerida.`,
    log: `✅ Ciclo de vida encerrado.
// Lead Time computado.
// Custo Kiro: $0.08 USD (Claude 3.5).`
  }
];

let currentFluxoStep = 0;

function initFluxoIaView() {
  const container = document.getElementById('fluxo-ia-view');
  if (!container) return;

  container.innerHTML = `
    <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #1e1b4b);">
      <div class="tag" style="background:#8b5cf6;">SIMULADOR DEFINITIVO</div>
      <h2>🚀 Dashboard: Fluxo de IA no TFS</h2>
      <p>Navegue pela linha do tempo abaixo para entender o que o Board mostra, quem é o Agente atuando e qual é a Configuração (Skill) necessária no Kiro para cada passo.</p>
    </div>

    <!-- Timeline Selector -->
    <div style="display:flex; overflow-x:auto; gap:5px; padding-bottom:15px; margin-bottom:20px; border-bottom:1px solid #e2e8f0;" id="fluxo-timeline">
    </div>

    <!-- 3 Panels Grid -->
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; align-items:start;">
      
      <!-- Esquerda: Visão Negócio (Board) -->
      <div style="display:flex; flex-direction:column; gap:20px;">
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:10px; padding:20px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
          <strong style="color:#0f172a; font-size:15px; display:block; margin-bottom:15px; border-bottom:2px solid #3b82f6; padding-bottom:5px;">📊 Visão TFS Kanban</strong>
          <div style="background:#e2e8f0; border-radius:6px; padding:15px; min-height:150px;" id="fluxo-board">
            <!-- Board Render -->
          </div>
        </div>

        <div style="background:#0f172a; border-radius:10px; border:1px solid #334155; padding:20px; box-shadow:0 4px 6px rgba(0,0,0,0.2);">
          <strong style="color:#e2e8f0; font-size:15px; display:block; margin-bottom:15px; border-bottom:2px solid #475569; padding-bottom:5px;">💻 Execução (Terminal Kiro)</strong>
          <div style="font-family:'Courier New', Courier, monospace; font-size:13px; color:#10b981; line-height:1.6; white-space:pre-wrap;" id="fluxo-terminal">
            <!-- Terminal Render -->
          </div>
        </div>
      </div>

      <!-- Direita: Visão Engenharia (Config Kiro) -->
      <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:20px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
        <strong style="color:#0f172a; font-size:15px; display:block; margin-bottom:15px; border-bottom:2px solid #a855f7; padding-bottom:5px;">⚙️ Configuração Kiro (Engenharia)</strong>
        
        <div style="margin-bottom:20px; background:#f0f9ff; padding:15px; border-radius:8px; border:1px solid #bae6fd;">
          <div style="font-size:30px; margin-bottom:5px;" id="fluxo-agent-icon"></div>
          <strong style="color:#0369a1; font-size:16px; display:block;" id="fluxo-agent-name"></strong>
          <p style="color:#0c4a6e; font-size:13px; margin-top:5px; line-height:1.4;" id="fluxo-agent-desc"></p>
        </div>

        <div>
          <strong style="font-size:12px; color:#475569; display:block; margin-bottom:8px;">Código da Skill / Gatilho MCP:</strong>
          <div style="background:#1e293b; color:#f8fafc; padding:15px; border-radius:6px; font-family:monospace; font-size:12px; border-left:4px solid #a855f7; overflow-x:auto; white-space:pre-wrap; line-height:1.5;" id="fluxo-skill-code">
            <!-- Skill Render -->
          </div>
        </div>
      </div>

    </div>
  `;

  renderFluxoStep(0);
}

function renderFluxoStep(index) {
  currentFluxoStep = index;
  const data = fluxoIaData[index];

  // Render Timeline
  const tlContainer = document.getElementById('fluxo-timeline');
  let tlHtml = '';
  fluxoIaData.forEach((step, idx) => {
    const isActive = idx === index;
    tlHtml += \`
      <button onclick="renderFluxoStep(\${idx})" style="
        background: \${isActive ? '#3b82f6' : '#f1f5f9'};
        color: \${isActive ? 'white' : '#475569'};
        border: 1px solid \${isActive ? '#2563eb' : '#cbd5e1'};
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        cursor: pointer;
        min-width: fit-content;
        transition: all 0.2s;
      ">\${step.title}</button>
    \`;
  });
  tlContainer.innerHTML = tlHtml;

  // Render Board
  const boardHtml = \`
    <div style="font-size:12px; color:#475569; font-weight:bold; text-align:center; margin-bottom:15px;">Coluna Atual: \${data.board.column}</div>
    <div style="display:flex; flex-direction:column; gap:10px;">
      \${data.board.cards.map(c => \`
        <div style="background:white; border-left:4px solid #3b82f6; padding:10px; border-radius:4px; box-shadow:0 1px 3px rgba(0,0,0,0.1); animation: pulseCard 2s infinite;">
          <div style="font-size:10px; color:#94a3b8; margin-bottom:4px;">ID: #\${c.id}</div>
          <strong style="font-size:13px; color:#1e293b;">\${c.title}</strong>
          <div style="margin-top:8px; display:flex; gap:5px; flex-wrap:wrap;">
            \${c.tags.map(t => \`<span style="background:#fef08a; color:#854d0e; font-size:9px; padding:2px 6px; border-radius:10px;">\${t}</span>\`).join('')}
          </div>
        </div>
      \`).join('')}
    </div>
  \`;
  document.getElementById('fluxo-board').innerHTML = boardHtml;

  // Render Config
  document.getElementById('fluxo-agent-icon').innerText = data.agent.icon;
  document.getElementById('fluxo-agent-name').innerText = data.agent.name;
  document.getElementById('fluxo-agent-desc').innerText = data.agent.desc;
  
  // Format Skill Code lightly
  let skillHtml = data.skill.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  document.getElementById('fluxo-skill-code').innerHTML = skillHtml;

  // Render Terminal
  document.getElementById('fluxo-terminal').innerText = data.log;
}

// Make globally available
window.initFluxoIaView = initFluxoIaView;
window.renderFluxoStep = renderFluxoStep;
