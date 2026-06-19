function initKiroDocView() {
    const container = document.getElementById('kiro-doc-view');
    if (!container) return;

    container.innerHTML = `
        <style>
            .mc-accordion {
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                overflow: hidden;
            }
            .mc-accordion summary {
                padding: 20px 25px;
                cursor: pointer;
                font-size: 18px;
                font-weight: 600;
                color: #0f172a;
                background: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
                display: flex;
                align-items: center;
                gap: 12px;
                transition: background 0.2s;
            }
            .mc-accordion summary:hover {
                background: #f1f5f9;
            }
            .mc-accordion summary::-webkit-details-marker {
                display: none;
            }
            .mc-accordion[open] summary {
                background: #e0e7ff;
                border-bottom: 2px solid #6366f1;
            }
            .mc-content {
                padding: 25px;
                color: #475569;
                font-size: 14.5px;
                line-height: 1.7;
            }
            .mc-code {
                background: #0f172a;
                color: #e2e8f0;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Courier New', Courier, monospace;
                font-size: 13px;
                line-height: 1.5;
                overflow-x: auto;
                margin: 15px 0;
            }
            .mc-code-highlight { color: #a5b4fc; }
            .mc-code-comment { color: #64748b; font-style: italic; }
            .mc-callout {
                background: #eff6ff;
                border-left: 4px solid #3b82f6;
                padding: 15px;
                border-radius: 4px;
                margin: 15px 0;
            }
        </style>

        <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #312e81);">
            <div class="tag" style="background:#6366f1;">MASTERCLASS "10.000 HORAS"</div>
            <h2>📖 Kiro: Engenharia de Orquestração</h2>
            <p style="margin-top:10px;">Para dominar o nível Enterprise de Automação com IA, você não pode apenas rodar scripts locais. O Kiro é o seu <strong>Daemon de Governança</strong>. Abaixo estão os módulos avançados que separam os amadores dos Engenheiros de IA 10x.</p>
        </div>

        <!-- MÓDULO 1 -->
        <details class="mc-accordion" open>
            <summary><span style="font-size:24px;">⚙️</span> Módulo 1: O Motor Kiro (Daemon Internals)</summary>
            <div class="mc-content">
                <p>O Kiro opera como um Daemon persistente no servidor, monitorando ferramentas do mundo real (TFS, Jira, Slack). Entender seu "motor" é vital para escalar sua operação sem estourar limites de API.</p>
                
                <h4 style="color:#1e293b; margin-top:20px;">1. Teoria de Filas e Little's Law</h4>
                <p>Se você tem 50 tickets no Backlog e ativa o Kiro, o que acontece? Ele <strong>não</strong> cria 50 instâncias do Claude simultâneas. O Kiro usa um limitador de concorrência atrelado ao WIP (Work In Progress) do Kanban.</p>
                <div class="mc-callout">
                    <strong>Little's Law na Prática:</strong> <code>L = λW</code> (Itens na fila = Taxa de chegada x Tempo no sistema). O Kiro pausa novas "puxadas" (Pulls) da coluna 'New' se a taxa de Tokens/Minuto do seu provedor (Anthropic/OpenAI) atingir 80% do limite da sua tier.
                </div>

                <h4 style="color:#1e293b; margin-top:20px;">2. Rate Limiting e Backoff Retries</h4>
                <p>As APIs de LLM falham. Seja por Rate Limit (Erro 429) ou Timeout (Erro 504). O Kiro Engine tem resiliência nativa com <i>Exponential Backoff</i>.</p>
                <div class="mc-code">
<span class="mc-code-comment"># .kiro/config.yaml - Seção de Resiliência</span>
<span class="mc-code-highlight">engine:</span>
  <span class="mc-code-highlight">max_concurrent_agents:</span> 5
  <span class="mc-code-highlight">retry_policy:</span>
    <span class="mc-code-highlight">max_attempts:</span> 3
    <span class="mc-code-highlight">backoff_multiplier:</span> 2.0  <span class="mc-code-comment"># Espera 2s, depois 4s, depois 8s...</span>
  <span class="mc-code-highlight">fallback_model:</span> "claude-3-haiku-20240307" <span class="mc-code-comment"># Se Sonnet falhar, use o Haiku</span>
                </div>
            </div>
        </details>

        <!-- MÓDULO 2 -->
        <details class="mc-accordion">
            <summary><span style="font-size:24px;">🛡️</span> Módulo 2: Governança Corporativa e Segurança</summary>
            <div class="mc-content">
                <p>Em ambientes corporativos como Bancos e Seguradoras, IAs não podem ter acesso SSH ilimitado a servidores ou gravar diretamente no banco de dados principal sem supervisão severa.</p>

                <h4 style="color:#1e293b; margin-top:20px;">1. Sandboxes Efêmeras (Docker)</h4>
                <p>Quando o Agente Engenheiro (Coder) roda <code>npm install</code> ou compila testes de integração, o Kiro não executa isso na máquina host. Ele cria um container Docker isolado que morre em 15 minutos.</p>
                <div class="mc-callout" style="border-color:#ef4444; background:#fef2f2;">
                    <strong>Segurança Ofensiva (Red Teaming):</strong> O Kiro intercepta qualquer tentativa do Agente de chamar APIs externas não autorizadas (ex: vazamento de código enviando dados para <code>pastebin.com</code>) usando regras estritas de <code>egress-firewall</code> na sandbox.
                </div>

                <h4 style="color:#1e293b; margin-top:20px;">2. Auditoria e Imutabilidade (Audit Trails)</h4>
                <p>Toda decisão (Prompt enviado, Token Gasto, Mudança no TFS) é gravada num Log centralizado que pode ser exportado para o Datadog ou Splunk da empresa.</p>
                <div class="mc-code">
<span class="mc-code-comment"># O log é JSON-Lines para fácil indexação</span>
{"timestamp": "2026-06-15T10:00:00", "agent": "Planner", "action": "PATCH", "workItem": 101, "cost_usd": 0.045, "reasoning": "Ticket was lacking BDD acceptance criteria. Expanded using Confluence data."}
                </div>
            </div>
        </details>

        <!-- MÓDULO 3 -->
        <details class="mc-accordion">
            <summary><span style="font-size:24px;">🚦</span> Módulo 3: Strong Steering (Direcionamento Avançado)</summary>
            <div class="mc-content">
                <p>O conceito de <i>Steering</i> vai além de "Aprovar" um código. Envolve gerenciar custos dinamicamente e exigir aprovações em múltiplas instâncias antes do Kiro continuar o fluxo autônomo.</p>

                <h4 style="color:#1e293b; margin-top:20px;">1. Interrupções Baseadas em Custo (Cost Guards)</h4>
                <p>O que acontece se o Agente Coder entrar num loop infinito de TDD, tentando consertar um teste e falhando por 50 iterações? Ele vai queimar todo seu orçamento de tokens! O Kiro introduz <code>Cost Guards</code>.</p>
                <div class="mc-code">
<span class="mc-code-comment"># .kiro/skills/coder.yaml</span>
<span class="mc-code-highlight">cost_guard:</span>
  <span class="mc-code-highlight">max_usd_per_run:</span> 2.00
  <span class="mc-code-highlight">action_on_breach:</span> "pause_and_notify"
  <span class="mc-code-highlight">notify:</span> "@tech-lead"
                </div>

                <h4 style="color:#1e293b; margin-top:20px;">2. Multi-Party Approval (Regra de 2 Chaves)</h4>
                <p>Para fluxos críticos (ex: Mover card para 'Liberado para Instalar' em ambiente Produtivo), o Kiro pode exigir consenso de dois humanos de setores diferentes.</p>
                <div class="mc-callout">
                    <strong>Comando Slack:</strong> Quando o Bot avisa <code>"Deploy to Prod pending"</code>, o Kiro só destrava se receber <code>/kiro approve</code> de alguém do grupo <strong>@dev-ops</strong> E <code>/kiro approve</code> de alguém do grupo <strong>@product-managers</strong>.
                </div>
            </div>
        </details>

        <!-- MÓDULO 4 -->
        <details class="mc-accordion">
            <summary><span style="font-size:24px;">🏗️</span> Módulo 4: Padrões de Arquitetura de Skills</summary>
            <div class="mc-content">
                <p>Construir a árvore <code>.kiro/skills/</code> requer padrões arquitetônicos. O padrão de ouro Enterprise é o <strong>Supervisor / Worker</strong>.</p>

                <h4 style="color:#1e293b; margin-top:20px;">1. O Padrão Supervisor/Worker (Map-Reduce para IA)</h4>
                <p>Em vez de um Agente com um prompt monstruoso tentando fazer o backend e o frontend ao mesmo tempo, dividimos as responsabilidades (Single Responsibility Principle).</p>
                <ul style="margin-left:20px; margin-bottom:15px;">
                    <li><strong>Agente Arquiteto (Supervisor):</strong> Lê o ticket, divide o problema em 3 sub-tarefas (DB, API, UI). Mapeia as dependências e despacha para 3 instâncias Workers.</li>
                    <li><strong>Agentes Coder (Workers):</strong> 3 instâncias rodam em paralelo. Cada uma faz apenas sua parte. Quando terminam, enviam os diffs de volta ao Supervisor.</li>
                    <li><strong>Agente Revisor (Supervisor):</strong> Pega as 3 partes, tenta o <code>npm run build</code> conjunto. Se quebrar, repreende os Workers e manda corrigirem.</li>
                </ul>

                <h4 style="color:#1e293b; margin-top:20px;">2. Ferramentas Locais Privadas (Private MCPs)</h4>
                <p>Sua empresa tem um sistema legado Mainframe que não tem API REST pública. O Kiro permite que você crie um MCP Server Privado em Node ou Python rodando na sua intranet.</p>
                <div class="mc-code">
<span class="mc-code-comment"># .kiro/mcp.json</span>
{
  "mcpServers": {
    "mainframe-bridge": {
      "command": "python3",
      "args": ["/var/scripts/mcp_mainframe.py"]
    }
  }
}
<span class="mc-code-comment"># O LLM agora tem uma 'Tool' nova: "query_mainframe". O Kiro roteia o pedido do LLM localmente para seu script python.</span>
                </div>
            </div>
        </details>

        <!-- MÓDULO 5 -->
        <details class="mc-accordion">
            <summary><span style="font-size:24px;">🤖</span> Módulo 5: Orquestração de Subagents</summary>
            <div class="mc-content">
                <p>O verdadeiro poder do Kiro como Orquestrador brilha na sua capacidade de "delegar" (spawn) sub-agentes para resolver problemas em paralelo. Em vez de uma única IA tentar resolver tudo de forma linear, o Kiro atua como um Gerente de Projetos distribuindo a carga.</p>

                <h4 style="color:#1e293b; margin-top:20px;">1. Padrão de Delegação (Spawning)</h4>
                <p>Quando o Kiro recebe um Épico ou Feature grande, ele quebra os requisitos e dispara Subagents específicos (ex: um focado apenas em UI, outro em Banco de Dados, outro em Testes). O Kiro fica aguardando o retorno de cada um (Await).</p>
                <div class="mc-code">
<span class="mc-code-comment"># Exemplo de fluxo do orquestrador (Kiro) delegando:</span>
<span class="mc-code-highlight">@kiro</span>: "Vou criar dois sub-agentes para trabalhar nisso em paralelo."
<span class="mc-code-highlight">[Subagent-1]</span> Iniciado: 'Role: Backend Developer'. Tarefa: Criar a API.
<span class="mc-code-highlight">[Subagent-2]</span> Iniciado: 'Role: Codebase Researcher'. Tarefa: Levantar os modelos de dados atuais.
                </div>

                <h4 style="color:#1e293b; margin-top:20px;">2. Sincronização e Message Passing</h4>
                <p>Os Subagents não trabalham isolados. O Kiro e os Subagents usam ferramentas como <code>send_message</code> para trocar informações. O Pesquisador avisa o Desenvolvedor sobre quais tabelas usar, e o Desenvolvedor retorna o código pronto para o Kiro (Orquestrador) revisar e fazer o Merge.</p>
                <div class="mc-callout">
                    <strong>Benefício Real:</strong> Ao orquestrar Subagents, o Kiro isola o contexto (Context Window) de cada IA. O Agente de Frontend não polui sua memória com logs de queries SQL do Backend, resultando em respostas mais baratas (menos tokens) e menos "alucinações" da IA.
                </div>
            </div>
        </details>
    `;
}

window.initKiroDocView = initKiroDocView;
