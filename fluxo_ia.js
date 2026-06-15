const fluxoIaData = [
  {
    id: 0,
    title: "0. Setup Kiro",
    board: {
      column: "Pre-Flight (Configuração)",
      cards: [
        { id: 999, title: "Ambiente e Acessos", tags: ["Infra", "Admin"] }
      ]
    },
    agent: {
      name: "Engenheiro de IA (Admin)",
      icon: "🛠️",
      desc: "Antes da mágica acontecer, o ambiente precisa ser configurado. O Kiro precisa de um Personal Access Token (PAT) do Azure DevOps, chaves de API dos provedores LLM (Anthropic/OpenAI) e configuração dos MCP Servers globais na sua máquina ou container."
    },
    skill: `# 1. Instalação Global
# npm install -g @kiro-ai/cli

# 2. Arquivo de Variáveis de Ambiente (.env)
AZURE_DEVOPS_ORG="https://dev.azure.com/SuaEmpresa"
AZURE_DEVOPS_PROJECT="BankingApp"
AZURE_DEVOPS_PAT="hx73...sua-chave-aqui...z8q"
ANTHROPIC_API_KEY="sk-ant-..."

# 3. Registro de Ferramentas (kiro-mcp.json)
{
  "mcpServers": {
    "tfs": {
      "command": "npx",
      "args": ["-y", "@microsoft/azure-devops-mcp"],
      "env": { "ADO_PAT": "\${AZURE_DEVOPS_PAT}" }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}

# 4. Estrutura de Skills
# As skills (como skill-planner.yaml) ficam em 
# ./kiro/skills/ na raiz do seu repositório.`,
    log: `$ kiro init
[Kiro Setup] Inicializando workspace...
[Auth] Validando AZURE_DEVOPS_PAT... Sucesso.
[Auth] Validando chaves LLM (Anthropic)... Sucesso.
[MCP] Instalando servidor @microsoft/azure-devops-mcp... Concluído.
[MCP] Instalando servidor @modelcontextprotocol/server-github... Concluído.

$ kiro validate-skills ./kiro/skills/
✔ skill-planner-po.yaml validada.
✔ skill-architect.yaml validada.
✔ skill-software-engineer.yaml validada.

[Daemon] Ambiente pronto. Para escutar o TFS, rode:
$ kiro start-daemon`
  },
    {
    id: 1,
    title: "1. New",
    board: {
      column: "New",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["Business", "Epic: Security"] },
        { id: 102, title: "Perfil do Usuário", tags: ["UX", "Epic: Core"] }
      ]
    },
    agent: {
      name: "Agente Ocioso (Ronda)",
      icon: "💤",
      desc: "Na coluna 'New', os itens são ideias brutas escritas pelo Product Owner. Nenhum agente de execução opera diretamente aqui. O Kiro mantém um Agente de Ronda (CronJob) rodando a cada 10 minutos para identificar itens que tenham as tags mínimas necessárias para avançar ao refinamento."
    },
    skill: `# kiro-config.yaml
version: 1.0
watchers:
  - name: "TFS-New-Observer"
    trigger:
      type: cron
      schedule: "*/10 * * * *"
    mcp_tool: "@microsoft/azure-devops-mcp"
    action: "query_work_items"
    query: |
      SELECT [System.Id], [System.Title]
      FROM WorkItems 
      WHERE [System.State] = 'New'
      AND [System.Tags] CONTAINS 'Business'
    on_match:
      execute_workflow: "promote_to_refinement"`,
    log: `$ kiro systemctl status watchers
[Kiro Daemon] Monitorando Azure DevOps via MCP...
[Cron] 10:00 - Executando query 'TFS-New-Observer'
[MCP: Azure DevOps] 2 itens encontrados no estado 'New'.
- Avaliando #101: Tags [Business] (Aprovado)
- Avaliando #102: Tags [UX] (Ignorado pelas regras de negócio atuais)
[Kiro Action] Movendo #101 para coluna 'Ref. Funcional (IA)'.`
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
      name: "Agente Planner (PO Assistant)",
      icon: "📋",
      desc: "Assume o card recém-promovido. Este agente tem a skill de um Analista de Negócios Sênior. Ele lê a descrição pobre do PO, pesquisa na base de conhecimento da empresa (Confluence via MCP), e cria um Product Requirements Document (PRD) maduro usando a sintaxe BDD (Given-When-Then)."
    },
    skill: `# skill-planner-po.yaml
agent:
  name: "Planner"
  model: "claude-3-5-sonnet-20241022"
  temperature: 0.2

system_prompt: |
  <role>Você é um Product Manager Sênior.</role>
  <task>
    Sua missão é ler um Work Item bruto, extrair os Acceptance Criteria e
    reescrevê-los no formato BDD (Gherkin).
  </task>
  <governance>
    - Se a descrição não contiver o critério de sucesso principal, aplique a tag 'DEP-Negocio' e devolva para 'New'.
    - NUNCA alucine regras de negócio. Use ferramentas MCP para buscar documentação.
  </governance>

mcp_servers:
  - name: "azure-devops"
    command: "npx"
    args: ["-y", "@microsoft/azure-devops-mcp"]
  - name: "confluence"
    command: "npx"
    args: ["-y", "@atlassian/confluence-mcp"]

on_success:
  patch_state: "Ag. Ref Técnico"
  attach_artifact: "PRD.md"`,
    log: `$ kiro run skill-planner-po.yaml --work-item=101
[MCP] azure-devops: GET WorkItem 101
[Planner] Lendo descrição: "Preciso de um login usando SMS."
[MCP] confluence: SEARCH "Política de Segurança MFA"
[Planner] Expandindo regras de negócio com base na política da empresa.
[Planner] Gerando PRD.md (Gherkin: Given user enters phone... Then send OTP...)
[MCP] azure-devops: ATTACH PRD.md to WorkItem 101
[MCP] azure-devops: PATCH System.State = 'Ag. Ref Técnico'
[Kiro] Sucesso. Custo da operação: $0.02`
  },
  {
    id: 3,
    title: "3. Ag. Ref Técnico",
    board: {
      column: "Ag. Ref Técnico",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["PRD Pronto", "Aguardando Tech"] }
      ]
    },
    agent: {
      name: "Fila de Espera (Buffer)",
      icon: "⏸️",
      desc: "O sistema respeita limites de WIP (Work in Progress). Se os agentes técnicos estiverem ocupados processando outros cards pesados (ex: refatorações massivas), o item fica em compasso de espera até que haja capacidade livre. Isso evita sobrecarga de paralelismo na conta do provedor LLM."
    },
    skill: `# WIP Limit Configuration
# kiro-board-policies.yaml
columns:
  "Ag. Ref Técnico":
    wip_limit: 5
    pull_criteria:
      - HasArtifact: "PRD.md"
      - TimeInColumn: "> 5 minutes"
    next_agent_pool: "Architects"
    
# O Kiro Scheduler monitora as métricas de Little's Law
# para alertar humanos se o Wait Time passar do SLA.`,
    log: `$ kiro metrics --column="Ag. Ref Técnico"
[WIP Check] Coluna 'Ag. Ref Técnico' tem 1 item. (WIP Limit: 5)
[Pool Check] Agentes 'Architect' estão ocupados no card #98.
[Action] Card #101 colocado em FILA DE ESPERA (Wait Time: 0h 12m).
// 15 minutos depois...
[Event] Agente Architect liberado.
[Kiro] Efetuando PULL do card #101 para 'Em Ref. Técnico (IA)'.`
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
      name: "Agente Architect (Tech Lead)",
      icon: "📐",
      desc: "Atua como Arquiteto de Software. Ele lê o PRD.md escrito pelo Planner e cria a Especificação Técnica (Tech Spec). Decide quais tabelas de banco criar, quais APIs desenhar (Swagger/OpenAPI) e, usando MCP, quebra o card pai em várias sub-tarefas (Child Tasks) no TFS."
    },
    skill: `# skill-architect.yaml
agent:
  name: "Architect"
  model: "claude-3-5-sonnet-20241022"

system_prompt: |
  <role>Você é o Tech Lead / Arquiteto de Software.</role>
  <task>
    1. Leia o PRD.md usando ferramentas MCP.
    2. Crie a arquitetura técnica (Architecture Decision Record - ADR).
    3. Quebre a implementação em Subtarefas Filhas de Engenharia no TFS.
  </task>

mcp_servers:
  - name: "azure-devops"
  - name: "github"
    description: "Pesquisar dependências do repositório"

on_success:
  patch_state: "Aguardando PO"
  create_children: true`,
    log: `$ kiro run skill-architect.yaml --work-item=101
[MCP] azure-devops: DOWNLOAD PRD.md
[Architect] Avaliando impacto na base de código via GitHub MCP...
[Architect] Gerando 'ADR-004_OTP_Login.md' com diagramas Mermaid.
[MCP] azure-devops: CREATE Task "API Twilio Integration" (Parent: 101)
[MCP] azure-devops: CREATE Task "Tabela DB AuthOTP" (Parent: 101)
[MCP] azure-devops: CREATE Task "Frontend Auth Modal" (Parent: 101)
[MCP] azure-devops: PATCH System.State = 'Aguardando PO'
[Kiro] Sucesso. Design pronto para aprovação humana.`
  },
  {
    id: 5,
    title: "5. Ag. PO (Gate)",
    board: {
      column: "Aguardando PO",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["Humano Requerido", "Aprovação"] }
      ]
    },
    agent: {
      name: "Gate de Qualidade Humana",
      icon: "🧑‍💼",
      desc: "Neste ponto ocorre um 'Strong Steering' (Intervenção Forte). A IA congela o fluxo e não escreve uma linha de código até que o Product Owner humano e o Líder Técnico leiam a arquitetura gerada e aprovem explicitamente no Kiro Hub."
    },
    skill: `# human-in-the-loop-gate.yaml
trigger: "StateChangedTo_AguardandoPO"
action: 
  type: "pause_and_notify"
  slack_channel: "#engineering-approvals"
  message: "O Card #{{System.Id}} está aguardando aprovação humana."

commands_available:
  - "/kiro approve {{id}}"
  - "/kiro reject {{id}} --reason"
  - "/kiro grill-me {{id}}" # Inicia chat iterativo com a IA`,
    log: `[Kiro Hub] Fluxo pausado. Aguardando Humano.
[Slack Bot] 🔔 "Card #101 requer aprovação de arquitetura."
[Humano] Executa: /kiro grill-me 101
[Kiro] "Olá, sou o Arquiteto. Que dúvidas você tem sobre a spec?"
[Humano] "A Twilio suporta WhatsApp OTP?"
[Kiro] "Sim. Posso atualizar a spec para incluir WhatsApp. Confirma?"
[Humano] "Sim. Depois disso, aprovado."
[Humano] Executa: /kiro approve 101
[Kiro] Movendo Card para 'Em Desenvolvimento'.`
  },
  {
    id: 6,
    title: "6. Em Dev (IA)",
    board: {
      column: "Em Desenvolvimento",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "Coding", "TDD"] }
      ]
    },
    agent: {
      name: "Agente Coder (TDD Flow)",
      icon: "🧑‍💻",
      desc: "A inteligência mais pesada do fluxo. Ele clona o repositório, cria a branch, lê a spec e escreve o código usando Test Driven Development. Ele roda os testes localmente na sandbox, corrige os próprios erros se quebrar, e depois faz o push via git."
    },
    skill: `# skill-software-engineer.yaml
agent:
  name: "Coder"
  model: "claude-3-5-sonnet-20241022"
  tools: ["execute_bash", "read_file", "write_file", "grep_search"]

system_prompt: |
  <role>Software Engineer Sênior focado em TDD.</role>
  <workflow>
    1. Crie uma branch baseada no ID do ticket.
    2. Escreva o Teste Unitário (Deve falhar - Red).
    3. Implemente o código (Deve passar - Green).
    4. Execute lint e formatação.
    5. git commit -m "feat: implementado OTP"
    6. git push
  </workflow>`,
    log: `$ kiro run skill-software-engineer.yaml --work-item=101
[Coder] Executando 'git checkout -b feat/101-otp-login'
[Coder] Lendo spec ADR-004_OTP_Login.md
[Coder] Criando auth.spec.ts...
[Bash] npm run test -> FALHA (Red) - auth module not found.
[Coder] Implementando auth.ts
[Bash] npm run test -> PASSOU (Green) - 14 tests passed.
[Bash] git add . && git commit -m "feat(auth): login via OTP"
[Bash] git push origin feat/101-otp-login
[MCP] azure-devops: PATCH System.State = 'Em Teste'`
  },
  {
    id: 7,
    title: "7. Em Teste (IA)",
    board: {
      column: "Em Teste",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "QA & Sec", "OWASP"] }
      ]
    },
    agent: {
      name: "Agente QA & Security",
      icon: "🛡️",
      desc: "O código já está no repo. Este agente assume o papel de QA e Red Team. Ele escreve testes End-to-End (ex: Cypress/Playwright), roda uma varredura de segurança contra injeções SQL e vulnerabilidades OWASP, e gera o laudo de teste atrelado ao card."
    },
    skill: `# skill-qa-sec.yaml
agent:
  name: "QA_Inspector"
  model: "claude-3-5-sonnet-20241022"

pipeline_steps:
  - run: "npx playwright test"
  - run: "docker run --rm -v $(pwd):/src returntocorp/semgrep --config=auto"
  
system_prompt: |
  <role>Security & QA Engineer</role>
  Verifique os resultados do Semgrep. Se houver falha crítica (CVE > 8),
  REJEITE o card (Devolva para Em Desenvolvimento).
  Se passar, anexe o PDF de evidências no TFS e promova.`,
    log: `$ kiro run skill-qa-sec.yaml --branch=feat/101-otp-login
[QA] Rodando Playwright Tests (Browser Engine: Chromium)...
[QA] 3 UI Tests Passed (Modal OTP renderizado corretamente).
[Security] Iniciando Semgrep SAST Scan...
[Security] Resultados: 0 Vulnerabilidades Críticas. 1 Warning (Dependency).
[QA] Gerando 'QA_Signoff_Report.pdf'.
[MCP] azure-devops: ATTACH QA_Signoff_Report.pdf
[MCP] azure-devops: PATCH System.State = 'Ag. Liberação PO'`
  },
  {
    id: 8,
    title: "8. Ag. PO (Final)",
    board: {
      column: "Ag. Liberação PO",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["Pronto para Deploy", "Validação Final"] }
      ]
    },
    agent: {
      name: "Gate de Aceite (UAT)",
      icon: "🧑‍💼",
      desc: "Último Gate humano. O sistema Kiro gera um ambiente efêmero (Vercel Preview ou Container) contendo a feature implementada. O PO clica no link, testa a funcionalidade de OTP no seu celular real e diz no Slack: 'Aprovado, pode mandar pra prod'."
    },
    skill: `# uat-approval-gate.yaml
trigger: "StateChangedTo_AgLiberacaoPO"
action:
  type: "create_preview_env"
  service: "vercel-preview"
  
notify:
  slack_channel: "#product-releases"
  message: |
    🚀 Feature Preview disponível para Teste (UAT):
    - Link: https://preview-101.empresa.com
    - Aprovar Deploy: /kiro approve-deploy 101
    - Reprovar (Bug): /kiro reject 101 --bug="detalhe"`,
    log: `[Vercel Preview] Deploy efêmero concluído. URL gerada.
[Slack Bot] 🚀 "Preview disponível para UAT."
[Humano] Acessa a URL, testa receber SMS no celular... Funciona!
[Humano] Executa: /kiro approve-deploy 101
[Kiro] Recebido sinal de Deploy Humano.
[MCP] azure-devops: Iniciando Merge para 'master'.
[MCP] azure-devops: PATCH System.State = 'Liberado para Instalar'`
  },
  {
    id: 9,
    title: "9. Lib Instalar",
    board: {
      column: "Liberado para Instalar",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["CI/CD Pipeline", "Deploying"] }
      ]
    },
    agent: {
      name: "Pipeline (Azure DevOps CI/CD)",
      icon: "🚀",
      desc: "Neste estágio, o Kiro sai de cena e delega o trabalho pesado para a esteira tradicional de CI/CD. O código entra na branch master, o Azure Pipelines detecta a mudança, empacota, aplica variáveis de ambiente e faz o Release em Produção."
    },
    skill: `# azure-pipelines.yml
trigger:
  - master
pool:
  vmImage: 'ubuntu-latest'
stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: npm ci && npm run build
- stage: DeployProd
  jobs:
  - job: DeployJob
    steps:
    - task: AzureWebApp@1
      inputs:
        azureSubscription: 'ProdServiceConnection'
        appName: 'app-auth-prod'
        package: '$(System.DefaultWorkingDirectory)/**/*.zip'`,
    log: `# Logs do Azure Pipelines (CI/CD Tradicional)
[Pipeline] Triggering pipeline via Webhook (Commit to master).
[Build] Downloading NPM packages...
[Build] Webpack compilation sucessful (14.2s).
[Deploy] Connecting to Azure Web App...
[Deploy] Updating ZIP package.
[Deploy] Restarting IIS Workers...
[Pipeline] Release Succeeded!
[TFS Auto-Rule] Status alterado para 'Done'.`
  },
  {
    id: 10,
    title: "10. Done",
    board: {
      column: "Done",
      cards: [
        { id: 101, title: "Login via OTP", tags: ["Em Produção", "Lead Time Gerado"] }
      ]
    },
    agent: {
      name: "Métricas TFS (Observabilidade)",
      icon: "📈",
      desc: "O card chegou ao fim. As métricas de fluxo do Kanban calculam que o Lead Time total foi de 24 horas. O custo total pago em tokens para as IAs fazerem o trabalho (Planner + Coder + QA) foi de 14 centavos de dólar. ROI gigantesco!"
    },
    skill: `# kiro-reporting.yaml
trigger: "StateChangedTo_Done"
action: "calculate_roi"
compute:
  time_saved: "HumanAvgLeadTime - KiroLeadTime"
  cost_spent: "Sum(LLM_API_Tokens_Cost)"
  
notify:
  slack_channel: "#engineering-metrics"
  message: "Feature OTP Login em PRD! Custo Kiro: $\{{cost_spent}}."`,
    log: `✅ CICLO DE VIDA ENCERRADO
----------------------------------------
[Métricas Kanban] Lead Time (New -> Done): 24h 15m.
[Eficiência Flow] Wait Time / Touch Time Ratio: 85% Touch Time (Eficiência absurda).
[Custo de IA] 
- Planner: $0.02
- Architect: $0.04
- Coder (TDD): $0.06
- QA: $0.02
[Custo Total API] $0.14 USD.
----------------------------------------
Parabéns, seu fluxo Kiro está otimizado!`
  }
];

let currentFluxoStep = 0;

function initFluxoIaView() {
  const container = document.getElementById('fluxo-ia-view');
  if (!container) return;

  container.innerHTML = `
    <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #1e1b4b);">
      <div class="tag" style="background:#8b5cf6;">SIMULADOR KANBAN + AGENTES</div>
      <h2>🚀 Dashboard: Automação Total com Kiro</h2>
      <p style="margin-top:10px;">Navegue pela linha do tempo abaixo para entender o que o Board de Negócios mostra, quem é o Agente atuando no background, e qual é a Configuração Real (YAML/Skill) injetada no Kiro para garantir Governança Corporativa em cada passo.</p>
    </div>

    <!-- Timeline Selector -->
    <div style="display:flex; overflow-x:auto; gap:5px; padding-bottom:15px; margin-bottom:20px; border-bottom:1px solid #e2e8f0;" id="fluxo-timeline">
    </div>

    <!-- 3 Panels Grid -->
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; align-items:start;">
      
      <!-- Esquerda: Visão Negócio (Board) e Visão Terminal -->
      <div style="display:flex; flex-direction:column; gap:20px;">
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:10px; padding:20px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
          <strong style="color:#0f172a; font-size:15px; display:block; margin-bottom:15px; border-bottom:2px solid #3b82f6; padding-bottom:5px;">📊 Visão Negócio (TFS Board)</strong>
          <div style="background:#e2e8f0; border-radius:6px; padding:15px; min-height:150px;" id="fluxo-board">
            <!-- Board Render -->
          </div>
        </div>

        <div style="background:#0f172a; border-radius:10px; border:1px solid #334155; padding:20px; box-shadow:0 4px 6px rgba(0,0,0,0.2);">
          <strong style="color:#e2e8f0; font-size:15px; display:block; margin-bottom:15px; border-bottom:2px solid #475569; padding-bottom:5px;">💻 Simulação (Terminal Kiro)</strong>
          <div style="font-family:'Courier New', Courier, monospace; font-size:12px; color:#10b981; line-height:1.6; white-space:pre-wrap; max-height: 400px; overflow-y:auto;" id="fluxo-terminal">
            <!-- Terminal Render -->
          </div>
        </div>
      </div>

      <!-- Direita: Visão Engenharia (Config Kiro) -->
      <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:20px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
        <strong style="color:#0f172a; font-size:15px; display:block; margin-bottom:15px; border-bottom:2px solid #a855f7; padding-bottom:5px;">⚙️ Configuração Kiro (Engenharia)</strong>
        
        <div style="margin-bottom:20px; background:#f0f9ff; padding:15px; border-radius:8px; border:1px solid #bae6fd;">
          <div style="font-size:35px; margin-bottom:5px;" id="fluxo-agent-icon"></div>
          <strong style="color:#0369a1; font-size:18px; display:block;" id="fluxo-agent-name"></strong>
          <p style="color:#0c4a6e; font-size:14px; margin-top:10px; line-height:1.5;" id="fluxo-agent-desc"></p>
        </div>

        <div>
          <strong style="font-size:13px; color:#475569; display:block; margin-bottom:8px;">Código Completo da Skill / Trigger:</strong>
          <div style="background:#1e293b; color:#e2e8f0; padding:15px; border-radius:6px; font-family:monospace; font-size:13px; border-left:4px solid #a855f7; overflow-x:auto; white-space:pre-wrap; line-height:1.5; max-height: 500px; overflow-y:auto;" id="fluxo-skill-code">
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
    tlHtml += `
      <button onclick="renderFluxoStep(${idx})" style="
        background: ${isActive ? '#3b82f6' : '#f1f5f9'};
        color: ${isActive ? 'white' : '#475569'};
        border: 1px solid ${isActive ? '#2563eb' : '#cbd5e1'};
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        cursor: pointer;
        min-width: fit-content;
        transition: all 0.2s;
        box-shadow: ${isActive ? '0 2px 4px rgba(59,130,246,0.3)' : 'none'};
      ">${step.title}</button>
    `;
  });
  tlContainer.innerHTML = tlHtml;

  // Render Board
  const boardHtml = `
    <div style="font-size:13px; color:#475569; font-weight:bold; text-align:center; margin-bottom:15px;">Coluna Atual: ${data.board.column}</div>
    <div style="display:flex; flex-direction:column; gap:12px;">
      ${data.board.cards.map(c => `
        <div style="background:white; border-left:4px solid #3b82f6; padding:12px; border-radius:6px; box-shadow:0 2px 4px rgba(0,0,0,0.1); animation: pulseCard 2s infinite;">
          <div style="font-size:11px; color:#94a3b8; margin-bottom:6px; font-family:monospace;">WorkItem ID: #${c.id}</div>
          <strong style="font-size:14px; color:#1e293b;">${c.title}</strong>
          <div style="margin-top:10px; display:flex; gap:6px; flex-wrap:wrap;">
            ${c.tags.map(t => `<span style="background:#fef08a; color:#854d0e; font-size:10px; font-weight:600; padding:3px 8px; border-radius:12px;">${t}</span>`).join('')}
          </div>
        </div>
      `).join('')}
    </div>
  `;
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

window.initFluxoIaView = initFluxoIaView;
window.renderFluxoStep = renderFluxoStep;
