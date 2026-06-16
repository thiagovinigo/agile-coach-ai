
function initLabsView() {
    const container = document.getElementById('labs-view');
    if (!container) return;

    container.innerHTML = `
        <style>
            .lab-card {
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                overflow: hidden;
            }
            .lab-header {
                padding: 20px 25px;
                background: #f8fafc;
                border-bottom: 2px solid #3b82f6;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .lab-header h3 {
                margin: 0;
                font-size: 18px;
                color: #0f172a;
            }
            .lab-content {
                padding: 25px;
                color: #475569;
                font-size: 14.5px;
                line-height: 1.7;
            }
            .lab-code {
                background: #0f172a;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                font-family: 'Courier New', Courier, monospace;
                font-size: 13px;
                line-height: 1.6;
                overflow-x: auto;
                margin: 20px 0;
                border-left: 4px solid #3b82f6;
                white-space: pre;
            }
            .lab-step {
                display: flex;
                align-items: flex-start;
                gap: 15px;
                margin-bottom: 20px;
            }
            .lab-step-number {
                background: #3b82f6;
                color: #fff;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            }
            
            /* Tabs CSS */
            .lab-tabs {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
                border-bottom: 2px solid #e2e8f0;
                padding-bottom: 10px;
                overflow-x: auto;
            }
            .lab-tab-btn {
                background: #f1f5f9;
                border: 1px solid #cbd5e1;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                color: #475569;
                transition: all 0.2s;
                white-space: nowrap;
            }
            .lab-tab-btn:hover {
                background: #e2e8f0;
            }
            .lab-tab-btn.active {
                background: #3b82f6;
                color: #fff;
                border-color: #2563eb;
            }
            .lab-tab-content {
                display: none;
            }
            .lab-tab-content.active {
                display: block;
            }
        </style>

        <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #000000);">
            <div class="tag" style="background:#3b82f6;">BOOTCAMP "10.000 HORAS"</div>
            <h2>🔬 40 Laboratórios Práticos (Discovery to Delivery)</h2>
            <p style="margin-top:10px;">Aqui o código ganha vida. Abaixo estão catalogados 40 laboratórios detalhados dividindo o ciclo de vida da Engenharia de Software em duas IAs complementares: <strong>Kiro (O Orquestrador)</strong> e <strong>Claude Code (O Worker de Terminal)</strong>. Selecione a aba desejada abaixo.</p>
        </div>

        <div class="lab-tabs" id="lab-tabs">
            <button class="lab-tab-btn active" onclick="switchLabTab('tab-kiro-basic', this)">⚙️ Kiro: Básicos (1-10)</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-kiro-tfs', this)">⚙️ Kiro: TFS Lifecycle (11-20)</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-claude-basic', this)">💻 Claude: Básicos (1-10)</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-claude-tfs', this)">💻 Claude: TFS Lifecycle (11-20)</button>
            <button class="lab-tab-btn" style="background:#ffedd5; border:1px solid #fed7aa; color:#9a3412;" onclick="switchLabTab('tab-masterclass', this)">🌟 Projeto Final (E2E)</button>
        </div>

        <div id="tab-kiro-basic" class="lab-tab-content active">
            
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🚀</span> 
                <h3>Lab 1: Setup & Daemon Initialization</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">É o comando inicial que instala o motor de orquestração do Kiro dentro do seu repositório local, criando a pasta oculta obrigatória <code>.kiro/</code>.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Sem essa estrutura inicial, os agentes não têm onde buscar suas regras corporativas. O Daemon atua como o 'Maestro' em background, lendo esse <code>config.yaml</code> constantemente para saber qual LLM usar e qual o limite de paralelismo da sua máquina.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>A Estrutura Raiz</strong>
                        <p>O Kiro exige um diretório oculto. Crie o arquivo base de configuração global.</p>
                        <div class="lab-code">
# .kiro/config.yaml
engine:
  max_concurrent_agents: 3
  default_llm: &quot;claude-3-5-sonnet-20241022&quot;
  telemetry: true
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🏛️</span> 
                <h3>Lab 2: The Architect Blueprint</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Um arquivo YAML que define o perfil, as ferramentas e as permissões de um 'Tech Lead' autônomo artificial.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Permite criar uma hierarquia inteligente. Em vez de uma IA que apenas escreve código cegamente, o Arquiteto lê a documentação, entende a Lei Geral de Proteção de Dados (via Confluence) e dita o desenho arquitetural para que os Coders apenas implementem. Isso garante padronização técnica.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>A Skill de Arquitetura</strong>
                        <p>Este YAML impede que o Agente codifique e obriga a leitura de regras.</p>
                        <div class="lab-code">
# .kiro/skills/architect.yaml
agent:
  name: &quot;Tech Lead&quot;
  role: &quot;Software Architect&quot;
workspace_rules:
  allow_write: false
  allow_bash: false
system_prompt: |
  Você deve sempre desenhar diagramas Mermaid.
  Consulte o Confluence antes de decidir a modelagem.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">📝</span> 
                <h3>Lab 3: The Planner Blueprint</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A configuração de um Agente Especialista em Produto (Product Owner/Analista de Negócios) que processa demandas brutas.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Desenvolvedores perdem horas preciosas desvendando requisitos mal escritos ou quebrando histórias gigantes. O Planner automatiza a etapa de refinamento, traduzindo desejos de negócio (Épicos) em tarefas acionáveis e formatadas no padrão que a Engenharia precisa.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>A Skill de PO</strong>
                        <p>Ele lê o Épico e não pode alterar código, apenas arquivos Markdown.</p>
                        <div class="lab-code">
# .kiro/skills/planner.yaml
agent:
  name: &quot;Planner&quot;
workspace_rules:
  allow_write: true
  allowed_extensions: [&quot;.md&quot;, &quot;.txt&quot;]
system_prompt: |
  Quebre o Épico em User Stories detalhadas usando o formato padrão da empresa.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">💸</span> 
                <h3>Lab 4: Cost Guards & Budgets</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A implementação de Kill Switches (Gatilhos de Interrupção) baseados em orçamento financeiro por execução.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">IAs agentic são propensas a 'Loops Infinitos' quando tentam resolver bugs complexos. Deixadas sozinhas, elas podem consumir milhares de dólares em chamadas de API do provedor (OpenAI/Anthropic) em uma única madrugada. O Cost Guard corta a energia antes que o orçamento sangre.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Proteção Financeira</strong>
                        <p>Defina limites em Dólar por ciclo de execução.</p>
                        <div class="lab-code">
# .kiro/skills/coder.yaml
cost_guard:
  max_usd_per_run: 2.50
  action_on_breach: &quot;pause_and_notify_slack&quot;
  notify: &quot;@tech-lead&quot;
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">👥</span> 
                <h3>Lab 5: Multi-Party Slack Approvals (Steering)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Regras de Governança que obrigam a IA a pausar seu workflow e solicitar o 'Ok' humano via chat corporativo (Slack/Teams).</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Para ações altamente destrutivas (Deploy em Produção, DELETE em banco de dados), a máquina não pode ter autonomia absoluta. Essa configuração garante rastreabilidade humana (compliance) e evita apagões causados por alucinações (AI Hallucinations).</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Regra de Dupla Aprovação</strong>
                        <p>Configuração de Gate para transições de estado críticas.</p>
                        <div class="lab-code">
# .kiro/workflows/deploy.yaml
state_transition:
  from: &quot;QA Approved&quot;
  to: &quot;Ready for Prod&quot;
approval_gate:
  required_approvals: 2
  allowed_groups: [&quot;@dev-ops&quot;, &quot;@product-managers&quot;]
  timeout_hours: 24
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🐳</span> 
                <h3>Lab 6: Ephemeral Docker Sandboxes</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Uma cerca de proteção arquitetural que força a IA a executar seus testes e comandos bash apenas dentro de containeres Docker de curta duração.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Se a IA baixar um pacote NPM malicioso injetado via engenharia social ou rodar comandos destrutivos sem querer (ex: <code>rm -rf</code>), ela destruirá apenas o container efêmero, poupando a máquina do desenvolvedor (Host) e prevenindo vazamentos de segurança.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Isolamento Estrito</strong>
                        <p>Nunca deixe a IA rodar scripts arbitrários diretamente no seu SO.</p>
                        <div class="lab-code">
# .kiro/config.yaml
sandbox:
  enabled: true
  provider: &quot;docker&quot;
  image: &quot;node:18-alpine&quot;
  network: &quot;host&quot;
  timeout_minutes: 15
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🔌</span> 
                <h3>Lab 7: Roteamento de Private MCPs</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A ponte entre as ferramentas (Model Context Protocol) nativas da sua rede corporativa e a inteligência do agente.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">IAs em nuvem não enxergam seus servidores de banco de dados internos. Ao configurar um MCP privado local via stdio (Terminal), você permite que o Kiro seja as 'mãos' da nuvem trabalhando com dados sensíveis que nunca saem da sua VPN.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Declaração de Ferramenta Privada</strong>
                        <p>O Kiro repassa o pedido do LLM para o script local.</p>
                        <div class="lab-code">
# .kiro/mcp.json
{
  &quot;mcpServers&quot;: {
    &quot;mainframe-db&quot;: {
      &quot;command&quot;: &quot;python3&quot;,
      &quot;args&quot;: [&quot;/opt/scripts/mcp_mainframe.py&quot;]
    }
  }
}
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">⚡</span> 
                <h3>Lab 8: Parallel Workers (Map-Reduce)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A orquestração que permite ao agente 'Arquiteto' se ramificar, criando e controlando 2 ou mais agentes menores trabalhando ao mesmo tempo.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Escalabilidade. Em vez do LLM resolver uma tela de front-end, parar, e depois codar o backend de banco de dados, o orquestrador despacha a tarefa pesada para dois workers independentes, diminuindo o Lead Time brutalmente de horas para minutos.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Invocação Paralela</strong>
                        <p>A transição de sucesso dispara múltiplos sub-agentes.</p>
                        <div class="lab-code">
# .kiro/skills/architect.yaml
on_success:
  trigger_subagents:
    - skill: &quot;coder-backend.yaml&quot;
      context: &quot;Criar API REST&quot;
    - skill: &quot;coder-frontend.yaml&quot;
      context: &quot;Criar Tela React&quot;
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">📜</span> 
                <h3>Lab 9: Audit Trail Logging</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O registro implacável e estruturado de todas as reflexões (Thoughts) e chamadas de ferramenta executadas pelo Agente.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Empresas com ISO 27001 ou SOC2 precisam provar QUEM tomou a decisão de apagar um arquivo ou fundir uma branch. O Audit Trail gera Logs JSON nativos que provam matematicamente os motivos pelos quais a IA agiu, essenciais para o Splunk ou Datadog.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Log Estruturado JSON</strong>
                        <p>Configure o roteamento de logs corporativos.</p>
                        <div class="lab-code">
# .kiro/config.yaml
logging:
  level: &quot;debug&quot;
  format: &quot;json&quot;
  destinations:
    - type: &quot;file&quot;
      path: &quot;/var/log/kiro/audit.jsonl&quot;
    - type: &quot;datadog&quot;
      api_key: &quot;\${DD_API_KEY}&quot;
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🔄</span> 
                <h3>Lab 10: Failover & Exponential Backoff</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Políticas de resiliência que trocam automaticamente o LLM de raciocínio caso o provedor primário esteja fora do ar.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">APIs de IA são instáveis. Se o projeto inteiro depende do Anthropic Claude 3.5 e ele sofre instabilidade, sua esteira inteira congela. O Failover inteligente tenta reconectar progressivamente (Backoff) e, se falhar, assume um modelo secundário de outra empresa para não parar a produção.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Resiliência de API</strong>
                        <p>Tolerância a falhas pesadas na infraestrutura.</p>
                        <div class="lab-code">
# .kiro/config.yaml
engine:
  retry_policy:
    max_attempts: 3
    backoff_multiplier: 2.0
  fallback_chain:
    - &quot;claude-3-5-sonnet-20241022&quot;
    - &quot;claude-3-haiku-20240307&quot;
    - &quot;gpt-4o&quot;
                        </div>
                    </div>
                </div>

            </div>
        </div>

        </div>

        <div id="tab-kiro-tfs" class="lab-tab-content">
            
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🎧</span> 
                <h3>Lab 11: Webhook Listener do TFS</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O 'Ouvido' do Kiro. Uma configuração de API que fica escutando os eventos disparados nativamente pelos servidores da Microsoft.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">O Kiro precisa ser reativo para ser invisível aos usuários corporativos. Quando o diretor da área cria um Épico no Board do TFS, o webhook acorda o Kiro de forma automática, garantindo zero atrito (nenhum comando de terminal necessário).</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Ouvindo Eventos</strong>
                        <p>Mapeie o evento do Azure DevOps para disparar o Agente Discovery.</p>
                        <div class="lab-code">
# .kiro/triggers.yaml
webhooks:
  - route: &quot;/api/webhooks/tfs&quot;
    secret: &quot;\${TFS_SECRET}&quot;
    events:
      - &quot;workitem.created&quot;
    condition: &quot;payload.resource.fields[&#x27;System.WorkItemType&#x27;] == &#x27;Epic&#x27;&quot;
    trigger_skill: &quot;discovery.yaml&quot;
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🔎</span> 
                <h3>Lab 12: Agente Product Discovery</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Uma skill de Kiro focada exclusivamente em consumir Épicos enormes, fatiá-los com inteligência e enviar os novos cards para o TFS.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">O maior gargalo das empresas ágeis é o 'Upstream'. Filas enormes de ideias que não são detalhadas por falta de tempo. Este agente desobstrui o funil, adiantando 80% do trabalho de um Product Manager experiente.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Automação de Backlog</strong>
                        <p>O agente usa a API do TFS para criar tickets filhos tangíveis.</p>
                        <div class="lab-code">
# .kiro/skills/discovery.yaml
agent:
  name: &quot;Product Discovery&quot;
mcp_servers:
  - name: &quot;azure-devops&quot;
system_prompt: |
  Você receberá o ID de um Épico. 
  Quebre-o em 3 a 5 User Stories factíveis.
  Para cada história, use a tool <code>tfs_create_workitem</code>.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🥒</span> 
                <h3>Lab 13: BDD & Acceptance Criteria</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A geração determinística de cenários de teste em formato Gherkin (Given/When/Then) atrelados à User Story original.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Testes devem ditar a construção do código (TDD), mas QAs são geralmente inseridos tarde demais no fluxo. Gerar os critérios de aceite no momento em que a história nasce garante alinhamento absoluto do 'Definition of Done'.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Geração de Cenários</strong>
                        <p>O QA Planner avalia as histórias e anexa regras de negócio.</p>
                        <div class="lab-code">
# .kiro/skills/qa-planner.yaml
agent:
  name: &quot;QA Automation Planner&quot;
system_prompt: |
  Analise a User Story fornecida.
  Escreva pelo menos 3 cenários de teste em formato Gherkin.
  Anexe o conteúdo gerado criando um arquivo <code>feature.md</code> e faça upload no ticket via API do TFS.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🎨</span> 
                <h3>Lab 14: UX/UI Design Sync</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Uma skill do orquestrador que converte discussões perdidas em comentários do TFS em especificações visuais de UI definitivas.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Desenvolvedores não deveriam inferir cores ou comportamentos cegamente. Ao forçar uma especificação de Design explícita com aprovação humana, eliminamos idas e vindas visuais caríssimas com o cliente.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Spec de Interface</strong>
                        <p>Lê threads de comentários no TFS e formaliza um doc de design.</p>
                        <div class="lab-code">
# design-spec.md (Gerado pelo Kiro)
## Componente: Login OTP
- **Cor Base:** #3b82f6
- **Comportamento:** O botão de submit deve ficar disabled até o input ter 6 dígitos.
&gt; Pendente aprovação final da equipe de Design (Tag @ux-team).
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">⏱️</span> 
                <h3>Lab 15: Sprint Planning Autônomo</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Um processo automatizado onde o LLM pondera arquitetura, integrações externas e dados passados para sugerir os Story Points de uma Task.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Cerimônias de Planning costumam consumir horas do time inteiro debatendo achismos. A IA traz uma estimativa matemática balizada (Ancoragem), permitindo que a equipe apenas valide o número, focando a reunião no que importa: impedimentos.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Estimação via IA</strong>
                        <p>O Kiro analisa a complexidade baseada em regras explícitas.</p>
                        <div class="lab-code">
# estimation-rules.md
- Front-end + Back-end (CRUD simples): 3 Pontos
- Integrações Externas Complexas: 5 Pontos
- Refatoração profunda sem UI: 2 Pontos

# O agente lê isso e usa <code>tfs_update_field(id, &#x27;Microsoft.VSTS.Scheduling.StoryPoints&#x27;, 5)</code>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🔗</span> 
                <h3>Lab 16: Rastreabilidade Obrigatória (Traceability)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Um 'Selo de Autenticidade'. O Kiro proíbe qualquer IA programadora local de salvar arquivos no Git sem carimbar de qual ticket originou a mudança.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Sem a rastreabilidade entre Código e Demanda, a empresa perde controle se sofrer uma auditoria de qualidade. Forçar a marcação <code>#[ID]</code> automatiza a ligação visual das branches ao Kanban do TFS.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Validação de Mensagem de Commit</strong>
                        <p>O Kiro intercepta o Git da IA Coder.</p>
                        <div class="lab-code">
# .kiro/skills/coder.yaml
workspace_rules:
  require_commit_prefix: &quot;#[TicketID] - &quot;
  on_validation_failure: &quot;reject_and_prompt&quot;

# Exemplo: O Coder tentará comitar <code>git commit -m &quot;Fix login&quot;</code> e o Kiro rejeitará, obrigando-o a formatar como <code>#101 - Fix login</code>.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">👀</span> 
                <h3>Lab 17: PR Review Automatizado (TFS Repos)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A injeção do Agente de Segurança no fluxo de Pull Requests da Microsoft. Ele comenta linhas perigosas da mesma forma que um sênior o faria.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Humanos sofrem de fadiga ocular em Pull Requests grandes e acabam aprovando vulnerabilidades grotescas. A IA atua como o Cão de Guarda incansável bloqueando vazamento de credenciais 24 horas por dia.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>O Cão de Guarda do Repositório</strong>
                        <p>Disparado quando um PR é aberto no Azure DevOps.</p>
                        <div class="lab-code">
# .kiro/skills/pr_reviewer.yaml
agent:
  name: &quot;Security PR Reviewer&quot;
mcp_servers:
  - name: &quot;azure-devops-git&quot;
system_prompt: |
  Você receberá o ID de um Pull Request.
  Busque os Diffs. 
  Se detectar Hardcoded Secrets ou falhas de injeção, use a tool <code>tfs_add_pr_comment</code> bloqueando o PR.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🛳️</span> 
                <h3>Lab 18: CI/CD Handoff</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O 'Passar do Bastão'. Quando o Kiro termina suas simulações locais, ele não faz deploy magicamente. Ele aciona as pipelines corporativas oficiais da empresa.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Usar IA não significa jogar fora as ferramentas de Infraestrutura sólidas da corporação. O Kiro respeita as barreiras de compliance repassando o trabalho para o Azure Pipelines original.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Fechando o Ciclo do Agente</strong>
                        <p>O Kiro move o card e a pipeline tradicional assume o build/deploy.</p>
                        <div class="lab-code">
# azure-pipelines.yml (Editado pelo Kiro)
trigger:
  branches:
    include:
      - master
steps:
  - script: npm ci &amp;&amp; npm run build
    displayName: &#x27;Build Production&#x27;
  - task: AzureWebApp@1
    inputs:
      appName: &#x27;prod-portal&#x27;
# O Kiro marca o TFS WorkItem como &#x27;Resolved&#x27;.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">📋</span> 
                <h3>Lab 19: Release Notes Generator</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O trabalho glorificado do Gerente de Release. Um relatório elegante em Markdown detalhando todas as entregas do ciclo.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Montar notas de versão catando dezenas de tickets pelo Board consome muito tempo. A automação consolida o valor entregue da Sprint e divulga o sucesso do time sem esforço humano.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Changelog Automático</strong>
                        <p>Gera documentação executiva via API do TFS e publica no Confluence.</p>
                        <div class="lab-code">
# release-notes.md
# 🚀 Release v1.4.0

## Novas Features (Épico: Auth)
- [TFS-101] Login OTP: Usuários agora podem logar via Token SMS.
- [TFS-102] Dashboard: Gráficos de vendas em tempo real atualizados via WebSocket.

## Correções
- [TFS-99] Fix memory leak no servidor de relatórios.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">📈</span> 
                <h3>Lab 20: Métricas de Fluxo (Lead Time)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A auditoria de tempo. O script lê cada fase em que o ticket esteve no TFS e calcula quanto tempo o time humano ou a IA levou ali.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Para aprimorar a maturidade ágil (Escala de Elite), precisamos saber os gargalos de fila (Wait Time). Extrair esses dados nativamente prova matematicamente a velocidade do time e se a adoção de IA Agentic cortou custos de verdade.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Relatório de Gargalos</strong>
                        <p>Script MCP consumido pelo Kiro para analisar o passado.</p>
                        <div class="lab-code">
# generate_metrics.py
import requests

def get_tfs_transitions(ticket_id):
    # Chama API do TFS para pegar Histórico
    # Calcula Data de &#x27;Resolved&#x27; - Data de &#x27;New&#x27;
    return lead_time_hours

# O Agente cria um analytics.csv com as maiores demoras da Sprint.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        </div>

        <div id="tab-claude-basic" class="lab-tab-content">
            
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🔑</span> 
                <h3>Lab 1: CLI Autenticação e Primeiros Passos</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O fluxo básico de instalação via gerenciador de pacotes Node (NPM) e o login via terminal para obter o Token Auth da Anthropic.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Para desenvolvedores, alternar entre a IDE e o navegador (ChatGPT/Claude.ai) destrói o estado de foco mental ('Flow'). Trazer a IA para o Terminal, onde o desenvolvedor já trabalha os testes e o git, reduz o atrito de contexto em 90%.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Instalação e Login</strong>
                        <p>O Claude Code roda localmente no seu NPM.</p>
                        <div class="lab-code">
npm install -g @anthropic-ai/claude-code
claude login
claude
&gt; &quot;Você está autenticado!&quot;
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🛡️</span> 
                <h3>Lab 2: Git Hooks de Defesa Ativa</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A escrita de um script em Bash (shell) executado sempre que o sistema operacional tentar consolidar um commit localmente.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Como o Claude é capaz de salvar arquivos e rodar o <code>git commit</code> sem você ver, você precisa de um campo de força. O <code>pre-commit</code> hook assegura mecanicamente que código quebrado por 'alucinação' nunca entre no seu histórico Git.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>O Pre-Commit Hook</strong>
                        <p>Força a IA a rodar testes antes de salvar o código.</p>
                        <div class="lab-code">
#!/bin/sh
# .git/hooks/pre-commit

npm test
if [ \$? -ne 0 ]; then
  echo &quot;Testes falharam! Claude não pode comitar.&quot;
  exit 1
fi
exit 0
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🧠</span> 
                <h3>Lab 3: Context Window Management</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Táticas avançadas de controle de memória do LLM dentro da IDE agentic para limpar e condensar conversas muito longas.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Provedores cobram o Token em Dólares. Uma conversa de 50 turnos arrasta todo aquele histórico inútil a cada pergunta nova, estourando limites de contexto (Context Window Limit). O comando <code>/compact</code> salva a empresa de uma fatura de nuvem absurda no fim do mês.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Comando Compact</strong>
                        <p>Use o REPL para limpar o histórico e economizar USD.</p>
                        <div class="lab-code">
&gt; /compact
[Claude] Limpando contexto inútil. Você economizou 50k tokens.
&gt; Focando APENAS em /src/utils, resolva o bug de data.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">📁</span> 
                <h3>Lab 4: DDD Conventions (.claudecode)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A injeção de documentos de restrição de regras de negócio em diretórios específicos usando a extensão <code>.claudecode</code> nativa.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Se você usa Clean Architecture ou Domain-Driven Design (DDD), sabe que o 'Dominio' é sagrado e isolado. O Claude, querendo ser 'prestativo', muitas vezes quebra camadas importando views no banco de dados. Essas regras param esse crime arquitetural na raiz.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Isolamento de Domínio</strong>
                        <p>Regras específicas que a IA obedece ao ler aquela pasta.</p>
                        <div class="lab-code">
# src/domain/.claudecode/CONVENTIONS.md
Regra Absoluta: NUNCA importe nada da pasta &#x27;infrastructure&#x27;.
A camada de Domínio deve ser pura e não ter dependências externas.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🏗️</span> 
                <h3>Lab 5: Refatoração em Lote (Batching)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A combinação do poder de Regex do Unix (Expressões regulares) aliada ao raciocínio em massa (Batch Processing) do Agente.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Atualizar padrões de sintaxe (como migrar de Classes para Hooks no React ou remover NullPointerExceptions em 50 arquivos legados) pode levar dias para um Dev Jr. A IA via terminal faz essa faxina monumental em 3 minutos sem errar a sintaxe do framework.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Escalando o Refactor</strong>
                        <p>Combine ferramentas Unix com IA.</p>
                        <div class="lab-code">
&gt; Encontre todos os arquivos React usando <code>var</code> em /components.
&gt; Atualize-os para usar <code>const</code> e <code>let</code> com ES6 functions.
[Claude] Encontrei 34 arquivos. Refatorando em batch...
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🧹</span> 
                <h3>Lab 6: Integração de Linter Automático</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A configuração do Claude para reagir autonomamente a falhas reportadas pelas ferramentas de análise estática como o ESLint ou Prettier.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Devolver código cheio de avisos de aspas duplas, ponto-e-vírgula e chaves mal fechadas gera fricção na equipe de desenvolvimento e polui o Pull Request. Forçamos a IA a entregar a 'mesa limpa' sempre.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Fix On Save</strong>
                        <p>A regra mestre no REPL.</p>
                        <div class="lab-code">
# .claudecode/CONVENTIONS.md
Após qualquer alteração em arquivos TypeScript, VOCÊ DEVE rodar &#x27;npm run lint:fix&#x27;. Se quebrar, corrija sozinho antes de me devolver o prompt.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🧪</span> 
                <h3>Lab 7: Custom MCP: API de Testes Flaky</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O uso de uma ponte entre o Claude e as APIs do framework de testes intermitentes (como Cypress ou Selenium) que reportam falhas sistêmicas.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Testes 'Flaky' (que passam de manhã e falham de tarde) destroem a credibilidade da automação e do QA. O Agente precisa ler o relatório do teste nativamente, analisar o print de erro na tela do Cypress e fixar com 'waits' inteligentes para parar de irritar o time.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>O Plugin Cypress</strong>
                        <p>Um servidor Python local que a IDE consome.</p>
                        <div class="lab-code">
claude /plugin add local ./get_flaky_cypress.py
&gt; Analise o teste mais flaky reportado pela tool e conserte-o usando explicit waits em vez de cy.wait().
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🔄</span> 
                <h3>Lab 8: O Loop TDD (Test-Driven AI)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Técnica de Prompting focada na disciplina do desenvolvimento orientado a testes. A IA deve primeiro entregar a falha estruturada e só depois a lógica.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Quando você pede o código completo de uma vez, a IA tende a escrever testes que são apenas 'espelhos felizes' (Happy Paths) que ela já sabe que vão passar. O TDD forçado prova a validade funcional do requisito de negócio antes que o código exista.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Prompting Disciplinado</strong>
                        <p>A ordem das ações importa muito.</p>
                        <div class="lab-code">
&gt; 1. Escreva o teste Jest falhando para a classe Calculator.
&gt; 2. PARE e rode o teste para provar que falha.
&gt; 3. Espere minha autorização para implementar o código que passa no teste.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">⏪</span> 
                <h3>Lab 9: Revert & History Management</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Comandos vitais de escape e recuperação do terminal quando a IDE entra em colapso e cria dezenas de arquivos inúteis no projeto.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Às vezes, a tentativa de resolver um bug simples faz o Agente entrar em parafuso, onde cada correção gera outro erro. Saber usar o 'Ctrl+C' mental da IA garante que a arquitetura não vire 'código espaguete' na tentativa cega de fixar um problema.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>O Botão de Pânico</strong>
                        <p>Parando a máquina e recomeçando.</p>
                        <div class="lab-code">
^C (Ctrl+C)
&gt; /history
&gt; Esqueça as últimas 3 tentativas. Elas geraram loop de dependência.
&gt; Rode <code>git reset --hard HEAD</code> e vamos começar do zero abordando por Injeção de Dependência.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🗣️</span> 
                <h3>Lab 10: Perfis de Prompt (Ask Before Write)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Trava de segurança na convenção do Claude que obriga o modelo a se comportar como um assistente verbal (que propõe o código e o explica via Diff Markdown) em vez de aplicar no disco.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Juniores que aceitam o código mágico de olhos fechados tornam-se incapazes de entender sua própria base de código com o passar do tempo. A IA, sendo tutora, estimula a aprendizagem passiva ao invés da mera automação irresponsável.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Pedindo Permissão</strong>
                        <p>Regra global para proteger arquivos.</p>
                        <div class="lab-code">
# .claudecode/CONVENTIONS.md
Você está ajudando um Junior Dev. Sempre que formular uma alteração complexa, escreva o diff em Markdown primeiro.
PARE. Só aplique o <code>write_file</code> após o Dev digitar &#x27;Aprovado&#x27;.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        </div>

        <div id="tab-claude-tfs" class="lab-tab-content">
            
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">📥</span> 
                <h3>Lab 11: Prompting the Backlog</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A integração do Claude Code com as APIs do Microsoft Azure DevOps (TFS) via um Servidor MCP, permitindo buscas dinâmicas sem abrir o navegador.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">O contexto mental do Dev deve continuar no terminal. Sair do VS Code para abrir a aba do Chrome, logar no TFS, buscar a aba Kanban e achar a própria Task consome energia. Aqui, basta dar o comando e a IA lista as prioridades do dia para você codar de imediato.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Consumo de API no Prompt</strong>
                        <p>Pluge a MCP do Azure DevOps.</p>
                        <div class="lab-code">
&gt; Use a tool <code>tfs_get_my_bugs</code>.
&gt; Liste todos os bugs assigned para mim na Sprint 42 e sugira por qual arquivo eu devo começar a olhar para resolver o primeiro.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🏗️</span> 
                <h3>Lab 12: Scaffolding a partir da User Story</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O ato de ler uma História de Usuário bruta gerada pelos Agentes (Kiro) no TFS e transformá-la automaticamente em arquivos base na árvore local do projeto (pastas, pacotes, index).</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Montar a base chata (os chamados 'Boilerplates') requer muita digitação repetitiva de imports, configs e injeções React/Angular que agregam zero valor final. A IA traduz regras cruas e formata a casca inicial para o Dev apenas preencher o miolo intelectual.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Geração Estrutural</strong>
                        <p>Lendo os critérios de aceite e criando pastas.</p>
                        <div class="lab-code">
&gt; Leia o Epic #100 do TFS.
&gt; Crie a estrutura de pastas seguindo Clean Architecture em /src.
&gt; Gere o package.json com os pacotes React e Tailwind necessários para cumprir os ACs.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🏛️</span> 
                <h3>Lab 13: Architecture Decision Records (ADR.md)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A emissão e o salvamento formal de um documento estruturado listando e justificando o porquê escolhemos uma tecnologia (ex: Redis vs Postgres) para a User Story do TFS.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Se a equipe técnica mudar amanhã, o conhecimento do porquê certas bibliotecas e caches foram adotadas desaparece. Gerar o ADR mecanicamente pelo terminal atrelado ao número do card documenta o raciocínio sem o 'peso burocrático' odiado pelos Devs.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>O Arquivo ADR</strong>
                        <p>Formalizando escolhas técnicas.</p>
                        <div class="lab-code">
# docs/adr/001-use-redis-for-cache.md
## Contexto
A User Story #101 do TFS exige carregamento do Dashboard em &lt; 1s.
## Decisão
Usaremos Redis.
## Consequências
Aumenta custo de infra, mas reduz carga no Postgres.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">✅</span> 
                <h3>Lab 14: TDD do Discovery ao Código</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O fluxo prático de consumir o critério BDD (Given, When, Then) atachado lá atrás pela ferramenta Discovery e transformar aquilo em testes interativos do tipo End-to-End no Cypress ou Jest.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Isso materializa o 'Pipeline de Qualidade Continua'. O 'Contrato' assinado com o PO no TFS se transforma no código executável real que previne as falhas e dita como a interface deve se comportar antes do deploy.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>De Feature para Spec</strong>
                        <p>Traduzindo regras de negócio para Cypress.</p>
                        <div class="lab-code">
&gt; Leia o arquivo <code>feature.md</code> anexado à Task #101 no TFS.
&gt; Para o cenário &#x27;Given user is logged out&#x27;, escreva um arquivo auth.cy.js no Cypress.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">⏳</span> 
                <h3>Lab 15: O Loop de Refatoração e Status</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O envio da requisição (Patch Request) via LLM para a nuvem da Microsoft para atualizar os ponteiros de progresso ('Remaining Work' e estado do Ticket Kanban).</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Desenvolvedores não atualizam Kanban. Isso é um fato na indústria de TI. A integração garante que o burndown chart do Scrum Master permaneça liso e verde, pois a IA assina o ponto assim que o código compila na máquina.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Atualizando Horas (Remaining Work)</strong>
                        <p>A IA gerencia seu card.</p>
                        <div class="lab-code">
&gt; Acabei de rodar os testes e passaram.
&gt; Atualize o status do Task #102 no TFS para &#x27;Resolved&#x27;.
&gt; Atualize o campo &#x27;Remaining Work&#x27; para 0.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">💳</span> 
                <h3>Lab 16: Mapeamento de Dívida Técnica</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Um scanner reverso. A IA varre o código fonte atual, levanta todas as falhas pontuadas informalmente por humanos e cria Tickets explícitos no Backlog Técnico do TFS.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Comentários no código do tipo <code>// TODO: Refatorar isso porque tá muito lento</code> são ignorados para sempre. Se não virar Card na mesa do Líder Técnico, a dívida esmaga a arquitetura num futuro próximo. O Claude garante essa visibilidade agressiva.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Varrer e Criar</strong>
                        <p>Delegue o trabalho braçal de criar cards.</p>
                        <div class="lab-code">
&gt; Faça um grep_search por comentários &#x27;// TODO&#x27; em /src.
&gt; Para cada um encontrado, crie um ticket de &#x27;Dívida Técnica&#x27; no TFS linkando o arquivo e a linha, e atribua ao Tech Lead.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🚨</span> 
                <h3>Lab 17: Linter Local vs SonarQube</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">Instruir a IA via terminal a interagir com os logs do SonarQube para sanar os relatórios drásticos de Segurança (OWASP Top 10).</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">O SonarQube reprova o PR se notar injeção de dependências inseguras ou criptografia fraca, travando a pipeline inteira. Acionar o LLM no terminal localmente conserta o code-smell na sua máquina, garantindo aprovação verde lá no TFS de primeira.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Varredura Local</strong>
                        <p>O Claude executa a ferramenta estática localmente.</p>
                        <div class="lab-code">
&gt; Rode o SonarLint CLI local neste arquivo.
&gt; Conserte todas as vulnerabilidades de &#x27;Alta Severidade&#x27; encontradas antes de eu dar git add.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🚀</span> 
                <h3>Lab 18: Automação do Pull Request (CLI)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A formatação textual dos 'git logs' locais de maneira sofisticada e a criação programática do Pull Request via API Rest do Azure DevOps Repos.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Um PR 'TBD' ou 'Fix Bug' na descrição é o pesadelo do Arquiteto que vai revisar o código. A ferramenta analisa o que você codou no dia inteiro e formula o texto de envio explicando cada classe alterada e linkando a Task do Board perfeitamente.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>PR Command</strong>
                        <p>Usando ferramentas customizadas de CLI.</p>
                        <div class="lab-code">
&gt; Leia meus commits locais e crie uma descrição rica em Markdown.
&gt; Use a tool <code>tfs_create_pr</code> para abrir o Pull Request na branch master e adicione os revisores padrão.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">👥</span> 
                <h3>Lab 19: Peer Review Local</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O download da branch do colega de trabalho pela IDE e a análise do seu código por um modelo poderoso (Claude 3.5 Sonnet) buscando vulnerabilidades arquiteturais profundas.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Muitas vezes o colega Sênior está ocupado, e revisões no Github são rasas. Usar a IA para encontrar SQL Injection e Race Conditions invisíveis economiza horas de Code Review massante e blinda o projeto.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Crítica Arquitetural</strong>
                        <p>Baixe o código e deixe o Claude achar as falhas.</p>
                        <div class="lab-code">
&gt; git checkout feature/payment-gateway
&gt; Atue como Arquiteto Sênior. Analise as alterações do último commit.
&gt; Encontre gargalos de concorrência ou injeção de SQL e me liste as linhas perigosas.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🔥</span> 
                <h3>Lab 20: Post-Mortem de Incidentes</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A dissecação de logs mortos de servidores derrubados e a criação automática e estruturada do documento final RCA (Root Cause Analysis - Causa Raiz).</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Quando ocorre um Bug 911 e a aplicação sangra dinheiro, consertar não é suficiente. É vital fechar o ciclo do DevOps formalizando a falha, o responsável e a ação para evitar aquilo no futuro. O Agente encerra a novela anexando a paz de espírito estruturada no sistema Kanban.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Root Cause Analysis (RCA)</strong>
                        <p>O fechamento do ciclo de vida de um Bug.</p>
                        <div class="lab-code">
&gt; Leia este log de erro do Sentry (error.txt).
&gt; Descubra qual arquivo causou o NullPointerException e conserte.
&gt; Crie o documento <code>root-cause.md</code> e anexe ao Bug #911 no TFS detalhando a causa raiz.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        </div>

        <div id="tab-masterclass" class="lab-tab-content">
            <div style="background:#fff7ed; padding:20px; border-left:4px solid #f97316; margin-bottom:30px; border-radius:6px;">
                <h3 style="margin-top:0; color:#c2410c;">🌟 Masterclass: O Ciclo de Vida Completo</h3>
                <p style="margin:0; color:#9a3412;">Abaixo, detalhamos o fluxo narrativo passo a passo <strong>(End-to-End)</strong> mostrando como as ferramentas Kiro e Claude se unem para construir um "AutoKanban" - validando, testando, codando e commitando de forma 100% autônoma.</p>
            </div>
            
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🎭</span> 
                <h3>Lab 41: Marco 1: Discovery & Backlog</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A recepção da ideia crua (Épico) do sistema 'AutoKanban' via integração com o Azure DevOps e o fatiamento autônomo em User Stories técnicas.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Sem um refinamento claro de Upstream, o Desenvolvedor IA vai 'alucinar' tentando construir o sistema inteiro de uma vez. O Discovery traduz a visão de negócio para fatias mastigáveis, mantendo o controle no TFS.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Webhook Trigger</strong>
                        <p>O TFS avisa que o Diretor criou o Épico 'Construir Ferramenta Kanban Autônoma'.</p>
                        <div class="lab-code">
POST /api/webhooks/tfs
Payload: { &quot;WorkItemId&quot;: 500, &quot;Type&quot;: &quot;Epic&quot; }

[Kiro Daemon] Webhook Recebido. Acordando Agente Product Owner.
                        </div>
                    </div>
                </div>

                <div class="lab-step">
                    <div class="lab-step-number">2</div>
                    <div style="width: 100%;">
                        <strong>Product Owner Agent - Fatiamento</strong>
                        <p>A IA lê o Épico e usa as ferramentas (MCP) para criar as tarefas.</p>
                        <div class="lab-code">
[Agente PO] Lendo Épico #500...
[Agente PO] O Épico contém Validação, TDD e Commit.

&gt; Executando Tool: tfs_create_workitem
- Criada Story #501: &quot;Motor de Validação (Linter/Sonar)&quot;
- Criada Story #502: &quot;Motor de Geração BDD&quot;
- Criada Story #503: &quot;Pipeline de Auto-Commit Segura&quot;
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🔬</span> 
                <h3>Lab 42: Marco 2: Refinamento Técnico (BDD & Arquitetura)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O Agente Architect escolhendo a Stack do projeto via ADR, enquanto o QA Automation Planner escreve as regras de negócio em formato Gherkin.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Evitar retrabalho. Ao escrever os cenários de teste Gherkin antes da primeira linha de código ser digitada (Shift-Left Testing), nós engessamos o comportamento esperado. O ADR blindado garante que o Claude Code não escolha linguagens aleatórias.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Geração do ADR (Tech Lead)</strong>
                        <p>O Arquiteto emite o Documento de Decisão Formal para a Task #502.</p>
                        <div class="lab-code">
# docs/adr/001-motor-bdd.md
## Contexto
Precisamos de um parser Gherkin rápido e testável.
## Decisão
O AutoKanban será em TypeScript rodando em Node.js usando Jest e o pacote &#x27;cucumber-jest&#x27;.

[Kiro Tech Lead] Fez upload do ADR.md no TFS #502.
                        </div>
                    </div>
                </div>

                <div class="lab-step">
                    <div class="lab-step-number">2</div>
                    <div style="width: 100%;">
                        <strong>Geração BDD (QA Agent)</strong>
                        <p>O agente de Qualidade traduz a história #502 em critérios rígidos.</p>
                        <div class="lab-code">
# feature.md (Anexado ao TFS #502)
Feature: Motor de Geração BDD Automática

Scenario: IA gera testes baseados em User Story
  Given a IA leu o Épico do Kanban
  When ela processa a funcionalidade de Validação
  Then o arquivo validator.test.ts deve ser gerado no diretório /__tests__
  And todos os testes devem estar falhando (RED phase)
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🔴</span> 
                <h3>Lab 43: Marco 3: TDD Fase Vermelha (Red)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A IDE Agentic (Claude Code) consome o <code>feature.md</code> e gera os testes unitários sem a implementação da funcionalidade, executando para provar que falham.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">É a base do Test-Driven Development (TDD). A IA comprova que o teste não é um 'Falso Positivo' (que sempre passa). Se a IA tentar codar logo de cara, nós ativamos um Gate Humano para pará-la.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Consumo de Critérios</strong>
                        <p>O Desenvolvedor usa a IDE (Claude Code) para puxar o Ticket.</p>
                        <div class="lab-code">
&gt; claude /task tfs-get-story 502

[Claude Code] Baixando ADR e feature.md de #502.
&gt; De acordo com as diretrizes do Tech Lead, devo escrever primeiro o arquivo cucumber.test.ts que falha.

&gt; npm run test -- validator.test.ts
❌ FAILED - Expected validation to occur, but no module found.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🟢</span> 
                <h3>Lab 44: Marco 4: Codificação e Autocura (Green & Refactor)</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">O Claude Code escreve a lógica TypeScript (Phase Green), os testes passam, e ele mesmo aciona o ESLint para corrigir o código (Refactor).</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">É aqui que a 'Ferramenta que codifica sozinha' brilha. Ela usa seu próprio loop de erro para se autoconsertar. Se um <code>import</code> quebrar, a ferramenta lê a saída de erro do terminal e tenta de novo até compilar verde.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Implementação e Linter</strong>
                        <p>A mágica do loop de feedback da IA no terminal.</p>
                        <div class="lab-code">
&gt; [Claude Code] Criando validator.ts para passar no teste...
&gt; npm run test
✅ PASS validator.test.ts

&gt; [Claude Code] Executando Linter pós-código...
&gt; npm run lint
❌ Warning: &#x27;any&#x27; is not allowed.
&gt; [Claude Code] Entendido, alterando o tipagem para interfaces estritas...
&gt; npm run lint
✅ Clean.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🛡️</span> 
                <h3>Lab 45: Marco 5: Validação Final e Pre-Commit</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">A execução mandatória do Agente de Segurança Local (SonarQube) e do Hook do Git, finalizando com a criação de um Pull Request no Azure DevOps.</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">Automação sem governança é caos. A IA não pode empurrar código sujo. A ferramenta garante que não há senhas expostas, aprova o commit, assina a mensagem e atualiza o Kanban para 'Resolved' de forma autônoma.</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>SonarQube & Commit</strong>
                        <p>Bloqueando código antes de poluir a branch.</p>
                        <div class="lab-code">
&gt; [Claude Code] Acionando SonarLint CLI...
✅ 0 Vulnerabilidades detectadas no validator.ts

&gt; [Claude Code] Comitando código com rastreabilidade.
&gt; git commit -m &quot;#[502] feat: implementa motor de validacao bdd&quot;

&gt; [Claude Code] Atualizando TFS via MCP...
PATCH /api/workitems/502
{ &quot;State&quot;: &quot;Resolved&quot;, &quot;Remaining Work&quot;: 0 }

&gt; Pull Request criado e encaminhado para @tech-lead.
                        </div>
                    </div>
                </div>

            </div>
        </div>

        </div>

    `;
}

window.initLabsView = initLabsView;
window.switchLabTab = function(tabId, btnElement) {
    document.querySelectorAll('.lab-tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.lab-tab-btn').forEach(btn => btn.classList.remove('active'));
    
    const targetTab = document.getElementById(tabId);
    if (targetTab) targetTab.classList.add('active');
    if (btnElement) btnElement.classList.add('active');
};
