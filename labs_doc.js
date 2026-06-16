
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
            <button class="lab-tab-btn active" onclick="switchLabTab('tab-kiro-basic')">⚙️ Kiro: Básicos (1-10)</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-kiro-tfs')">⚙️ Kiro: TFS Lifecycle (11-20)</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-claude-basic')">💻 Claude: Básicos (1-10)</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-claude-tfs')">💻 Claude: TFS Lifecycle (11-20)</button>
        </div>

        <div id="tab-kiro-basic" class="lab-tab-content active">
            
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">🚀</span> 
                <h3>Lab 1: Setup & Daemon Initialization</h3>
            </div>
            <div class="lab-content">
                <p><strong>Cenário:</strong> Inicializando o motor de orquestração no seu repositório local.</p>

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
                <p><strong>Cenário:</strong> Definindo a regra corporativa para o Tech Lead autônomo.</p>

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
                <p><strong>Cenário:</strong> Configurando um PO autônomo que lê épicos.</p>

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
                <p><strong>Cenário:</strong> Implementando Kill Switches de proteção financeira.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Proteção Financeira</strong>
                        <p>Se um loop infinito ocorrer, a conta de API pode explodir. Defina limites por run.</p>
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
                <p><strong>Cenário:</strong> O Kiro pausa e aguarda humanos antes do Deploy.</p>

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
                <p><strong>Cenário:</strong> Execução isolada de comandos bash para o Agente Coder.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Isolamento Estrito</strong>
                        <p>Nunca deixe a IA rodar scripts arbitrários no seu host local.</p>
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
                <p><strong>Cenário:</strong> Conectando o Kiro a um servidor Python interno de banco de dados.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Declaração de Ferramenta Privada</strong>
                        <p>O Kiro repassa o pedido do LLM para o script local via stdio.</p>
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
                <p><strong>Cenário:</strong> O Arquiteto divide a tarefa e invoca Coders simultâneos.</p>

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
                <p><strong>Cenário:</strong> Onde o Kiro guarda a memória para conformidade ISO 27001.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Log Estruturado JSON</strong>
                        <p>Configure o roteamento de logs para sistemas de monitoramento.</p>
                        <div class="lab-code">
# .kiro/config.yaml
logging:
  level: &quot;debug&quot;
  format: &quot;json&quot;
  destinations:
    - type: &quot;file&quot;
      path: &quot;/var/log/kiro/audit.jsonl&quot;
    - type: &quot;datadog&quot;
      api_key: &quot;${DD_API_KEY}&quot;
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
                <p><strong>Cenário:</strong> Se o Provedor Principal falhar, o Kiro se recupera.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Resiliência de API</strong>
                        <p>Tolerância a falhas na infraestrutura de LLMs.</p>
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
                <p><strong>Cenário:</strong> O Kiro precisa saber quando um ticket é criado. Configure o Webhook.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Ouvindo Eventos</strong>
                        <p>Mapeie o evento do Azure DevOps para disparar o Agente Discovery.</p>
                        <div class="lab-code">
# .kiro/triggers.yaml
webhooks:
  - route: &quot;/api/webhooks/tfs&quot;
    secret: &quot;${TFS_SECRET}&quot;
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
                <p><strong>Cenário:</strong> Lendo o Épico e gerando User Stories detalhadas no Azure Boards.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Automação de Backlog</strong>
                        <p>O agente usa a API do TFS para criar tickets filhos.</p>
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
                <p><strong>Cenário:</strong> Escrevendo Gherkin dentro dos tickets automaticamente.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Geração de Cenários</strong>
                        <p>O QA Planner avalia as histórias e gera os critérios Given-When-Then.</p>
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
                <p><strong>Cenário:</strong> Sincronizando discussões técnicas com aprovações de Design.</p>

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
                <p><strong>Cenário:</strong> O Agente preenche o campo Story Points baseado em histórico.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Estimação via IA</strong>
                        <p>O Kiro analisa a complexidade baseada em um documento de regras.</p>
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
                <p><strong>Cenário:</strong> O Coder é forçado a linkar o código ao WorkItem do TFS.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>Validação de Mensagem de Commit</strong>
                        <p>O Kiro intercepta as intenções de commit do Coder.</p>
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
                <p><strong>Cenário:</strong> O Kiro varre vulnerabilidades antes da aprovação do PR.</p>

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
                <p><strong>Cenário:</strong> Entregando o bastão para as pipelines nativas.</p>

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
                <p><strong>Cenário:</strong> Ao fim da Sprint, um Agente compila tudo o que foi entregue.</p>

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
                <p><strong>Cenário:</strong> Coletando inteligência do processo Kanabn.</p>

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
                <p><strong>Cenário:</strong> O fluxo básico de inicialização no terminal.</p>

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
                <p><strong>Cenário:</strong> Bloqueando commits destrutivos da IA via Bash.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>O Pre-Commit Hook</strong>
                        <p>Força a IA a rodar testes antes de salvar o código.</p>
                        <div class="lab-code">
#!/bin/sh
# .git/hooks/pre-commit

npm test
if [ $? -ne 0 ]; then
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
                <p><strong>Cenário:</strong> Evitando o estouro de limite de tokens usando escopos rígidos.</p>

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
                <p><strong>Cenário:</strong> Configurando limites arquiteturais por diretório.</p>

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
                <p><strong>Cenário:</strong> O Claude alterando múltiplos arquivos via terminal.</p>

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
                <p><strong>Cenário:</strong> Fazendo a IA limpar sua própria sujeira.</p>

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
                <p><strong>Cenário:</strong> Plugar uma ferramenta customizada para a IA resolver bugs intermitentes.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>O Plugin Cypress</strong>
                        <p>Um servidor Python local que a IDE consome.</p>
                        <div class="lab-code">
claude /plugin add local ./get_flaky_cypress.py
&gt; Analise o teste mais flaky reportado pela tool e conserte-o usando explicitly waits.
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
                <p><strong>Cenário:</strong> Forçando a IA a escrever o teste antes da implementação.</p>

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
                <p><strong>Cenário:</strong> O que fazer quando a IA entra em loop infinito e destrói código.</p>

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
                <p><strong>Cenário:</strong> Travas de segurança para Desenvolvedores Juniores.</p>

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
                <p><strong>Cenário:</strong> Puxando tarefas do TFS diretamente no terminal.</p>

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
                <p><strong>Cenário:</strong> A IA lê a história do TFS e monta a base do projeto.</p>

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
                <p><strong>Cenário:</strong> Gerando o documento oficial de arquitetura antes de programar.</p>

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
                <p><strong>Cenário:</strong> Lendo o Gherkin BDD gerado pelo Kiro e programando.</p>

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
                <p><strong>Cenário:</strong> Atualizando o TFS em tempo real via terminal.</p>

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
                <p><strong>Cenário:</strong> Convertendo // TODOs no código em tickets reais no Kanban.</p>

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
                <p><strong>Cenário:</strong> Corrigindo Code Smells antes que eles subam no PR.</p>

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
                <p><strong>Cenário:</strong> Abrindo o PR no Azure Repos diretamente do terminal local.</p>

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
                <p><strong>Cenário:</strong> Usando a IA como par crítico na branch de um colega.</p>

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
                <p><strong>Cenário:</strong> Lendo dumps de erro e formalizando a correção no Azure DevOps.</p>

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

    `;
}

window.initLabsView = initLabsView;
window.switchLabTab = function(tabId) {
    document.querySelectorAll('.lab-tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.lab-tab-btn').forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
};
