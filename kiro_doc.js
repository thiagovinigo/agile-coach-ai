function initKiroDocView() {
    const container = document.getElementById('kiro-doc-view');
    if (!container) return;

    container.innerHTML = `
        <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #312e81);">
            <div class="tag" style="background:#6366f1;">DOCUMENTAÇÃO OFICIAL</div>
            <h2>📖 Kiro: O Maestro de Agentes</h2>
            <p style="margin-top:10px;">O Kiro não é um Agente em si. Ele é o <strong>Motor de Orquestração (Daemon)</strong> que escuta eventos do mundo exterior (Azure DevOps, GitHub, Slack) e dispara os Agentes corretos (Planner, Architect, Coder) baseados em regras rígidas de Governança Corporativa.</p>
        </div>

        <div style="display:grid; grid-template-columns: 1fr; gap:20px; align-items:start;">
            
            <!-- Section 1: Core Concepts -->
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:25px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <strong style="color:#0f172a; font-size:18px; display:flex; align-items:center; gap:8px; margin-bottom:15px; border-bottom:2px solid #6366f1; padding-bottom:10px;">
                    <span style="font-size:24px;">🧠</span> 1. Arquitetura e Componentes
                </strong>
                <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:15px;">
                    A arquitetura do Kiro é dividida em 3 camadas principais:
                </p>
                <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; margin-bottom:20px;">
                    <div style="background:#f8fafc; padding:15px; border-radius:8px; border:1px solid #cbd5e1;">
                        <h4 style="color:#1e293b; margin-bottom:5px;">A) The Daemon (Motor)</h4>
                        <p style="font-size:13px; color:#64748b;">Roda em background. Monitora triggers (cron jobs, webhooks). Lê o Kanban e decide quando ativar um agente respeitando limites de WIP.</p>
                    </div>
                    <div style="background:#f8fafc; padding:15px; border-radius:8px; border:1px solid #cbd5e1;">
                        <h4 style="color:#1e293b; margin-bottom:5px;">B) As Skills (Regras)</h4>
                        <p style="font-size:13px; color:#64748b;">Arquivos YAML que definem <i>O QUE</i> deve ser feito. Conectam uma Trigger a um Agente (LLM) e fornecem as ferramentas (MCP) necessárias.</p>
                    </div>
                    <div style="background:#f8fafc; padding:15px; border-radius:8px; border:1px solid #cbd5e1;">
                        <h4 style="color:#1e293b; margin-bottom:5px;">C) Steering (Human-in-the-Loop)</h4>
                        <p style="font-size:13px; color:#64748b;">Mecanismo de controle humano. O Kiro pausa o fluxo e pede permissão no Slack ou Teams antes de realizar ações destrutivas (Deploy, Merge).</p>
                    </div>
                </div>
            </div>

            <!-- Section 2: Folder Structure -->
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:25px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <strong style="color:#0f172a; font-size:18px; display:flex; align-items:center; gap:8px; margin-bottom:15px; border-bottom:2px solid #10b981; padding-bottom:10px;">
                    <span style="font-size:24px;">📁</span> 2. Estrutura de Pastas do Repositório
                </strong>
                <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:15px;">
                    O Kiro exige que você tenha uma pasta oculta chamada <code>.kiro/</code> na raiz do seu projeto. É lá que toda a inteligência e configuração reside.
                </p>
                <div style="background:#0f172a; padding:20px; border-radius:8px; color:#e2e8f0; font-family:monospace; font-size:13px; line-height:1.5; overflow-x:auto;">
meu-projeto/
├── .kiro/
│   ├── config.yaml          <span style="color:#94a3b8;"># Configuração global (Tokens, LLM Provider)</span>
│   ├── mcp.json             <span style="color:#94a3b8;"># Servidores MCP disponíveis globalmente</span>
│   ├── /skills/             <span style="color:#94a3b8;"># Diretório de Inteligência</span>
│   │   ├── planner.yaml     <span style="color:#94a3b8;"># Skill do Product Owner</span>
│   │   ├── architect.yaml   <span style="color:#94a3b8;"># Skill do Tech Lead</span>
│   │   └── coder.yaml       <span style="color:#94a3b8;"># Skill do Engenheiro (TDD)</span>
│   └── /workflows/          <span style="color:#94a3b8;"># Orquestração (Pipelines de Agentes)</span>
│       └── end-to-end.yaml  <span style="color:#94a3b8;"># Ex: Pipeline que liga o planner -> coder</span>
├── src/                     <span style="color:#94a3b8;"># Código fonte real do seu app</span>
└── package.json
                </div>
            </div>

            <!-- Section 3: The Configurations -->
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:25px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <strong style="color:#0f172a; font-size:18px; display:flex; align-items:center; gap:8px; margin-bottom:15px; border-bottom:2px solid #f59e0b; padding-bottom:10px;">
                    <span style="font-size:24px;">⚙️</span> 3. Exemplo Prático de Configuração (Skill)
                </strong>
                <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:15px;">
                    Como transformamos um LLM genérico (Claude) em um <strong>Arquiteto Especialista no Projeto</strong>? Usando um arquivo de Skill no Kiro.
                </p>
                
                <div style="background:#1e293b; border-left:4px solid #f59e0b; padding:15px; border-radius:6px; color:#e2e8f0; font-family:monospace; font-size:13px; white-space:pre-wrap; overflow-x:auto;">
<span style="color:#cbd5e1;"># .kiro/skills/architect.yaml</span>
<span style="color:#818cf8;">agent:</span>
  <span style="color:#a5b4fc;">name:</span> "Architect"
  <span style="color:#a5b4fc;">model:</span> "claude-3-5-sonnet-20241022"
  <span style="color:#a5b4fc;">temperature:</span> 0.2

<span style="color:#818cf8;">mcp_servers:</span>
  - <span style="color:#34d399;">name:</span> "azure-devops"
  - <span style="color:#34d399;">name:</span> "github"

<span style="color:#818cf8;">system_prompt:</span> |
  &lt;role&gt;Você é o Tech Lead / Arquiteto de Software da empresa.&lt;/role&gt;
  &lt;guidelines&gt;
    1. Sempre gere diagramas Mermaid para as arquiteturas propostas.
    2. Use banco de dados PostgreSQL (Padrão da empresa).
    3. Para criar tabelas, obedeça as regras de LGPD vigentes lendo do Confluence.
  &lt;/guidelines&gt;

<span style="color:#818cf8;">on_success:</span>
  <span style="color:#a5b4fc;">patch_state:</span> "Aguardando PO"
  <span style="color:#a5b4fc;">create_children:</span> true
                </div>
            </div>

            <!-- Section 4: Steering -->
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:25px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <strong style="color:#0f172a; font-size:18px; display:flex; align-items:center; gap:8px; margin-bottom:15px; border-bottom:2px solid #ef4444; padding-bottom:10px;">
                    <span style="font-size:24px;">🛑</span> 4. Steering (Intervenção Humana)
                </strong>
                <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:15px;">
                    O Kiro brilha em governança. Você não quer a IA subindo código em produção sem controle. O mecanismo de <strong>Strong Steering</strong> (Direcionamento Forte) pausa o fluxo e aguarda um humano tomar a decisão via Terminal ou Integração de Chat (Slack/Teams).
                </p>

                <div style="display:flex; gap:20px;">
                    <div style="flex:1; background:#fee2e2; padding:15px; border-radius:8px; border:1px solid #fca5a5;">
                        <h4 style="color:#991b1b; margin-bottom:8px;">Exemplo de Gate (YAML)</h4>
                        <pre style="font-size:11px; color:#7f1d1d; margin:0; white-space:pre-wrap; font-family:monospace;">
trigger: "StateChangedTo_QA"
action: 
  type: "pause_and_notify"
  slack_channel: "#engineering-approvals"

commands_available:
  - "/kiro approve {{id}}"
  - "/kiro reject {{id}}"
  - "/kiro grill-me {{id}}"
                        </pre>
                    </div>
                    <div style="flex:1; background:#f8fafc; padding:15px; border-radius:8px; border:1px solid #cbd5e1;">
                        <h4 style="color:#0f172a; margin-bottom:8px;">Ação no Slack (Visão Humano)</h4>
                        <p style="font-size:13px; color:#475569; margin-bottom:10px;">🤖 <strong>Kiro Bot:</strong> A feature "Login OTP" está pronta para homologação. O Arquiteto pede revisão da Spec de Segurança.</p>
                        <p style="font-size:13px; color:#3b82f6; font-family:monospace; margin-bottom:5px;">> /kiro grill-me 101</p>
                        <p style="font-size:13px; color:#475569; margin-bottom:10px;">🤖 <strong>Kiro Bot:</strong> Estou aqui. Que dúvidas você tem sobre a Spec?</p>
                        <p style="font-size:13px; color:#3b82f6; font-family:monospace; margin-bottom:5px;">> /kiro approve 101</p>
                        <p style="font-size:13px; color:#10b981; font-weight:bold;">✅ Feature Aprovada. Movendo Kanban.</p>
                    </div>
                </div>
            </div>

        </div>
    `;
}

window.initKiroDocView = initKiroDocView;
