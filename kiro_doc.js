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
        <!-- MÓDULO 6: CASE PRÁTICO TFS -->
        <details class="mc-accordion" open>
            <summary><span style="font-size:24px;">🚀</span> Módulo 6: Case Prático - Fluxo TFS Completo (End-to-End)</summary>
            <div class="mc-content" style="background: #fafafa;">
                <p>Neste cenário avançado, vemos como o Kiro e o ecossistema de Agentes atuam sobre o ciclo de vida completo de um PBI (Product Backlog Item) no <strong>Azure DevOps (TFS)</strong>. Da concepção da ideia até o aceite final (UAT).</p>
                
                <style>
                    .tfs-board { display: flex; gap: 10px; overflow-x: auto; padding: 15px 0; margin: 20px 0; }
                    .tfs-col { background: #f1f5f9; min-width: 150px; border-radius: 8px; padding: 10px; border-top: 4px solid #94a3b8; }
                    .tfs-col.active { border-top-color: #3b82f6; background: #eff6ff; }
                    .tfs-col-title { font-size: 11px; text-transform: uppercase; font-weight: bold; color: #475569; margin-bottom: 10px; }
                    .tfs-card { background: #fff; border: 1px solid #cbd5e1; border-left: 4px solid #0ea5e9; padding: 10px; border-radius: 4px; font-size: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
                    .tfs-tag { display: inline-block; background: #e0f2fe; color: #0284c7; padding: 2px 6px; border-radius: 999px; font-size: 9px; font-weight: bold; margin-right: 4px; margin-top: 5px; }
                    
                    .phase-box { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
                    .phase-title { display: flex; align-items: center; gap: 10px; font-size: 16px; font-weight: bold; color: #0f172a; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; margin-bottom: 15px; }
                    .phase-badge { background: #1e293b; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; }
                    
                    .ai-action { display: flex; align-items: flex-start; gap: 15px; margin-top: 15px; background: #f8fafc; padding: 15px; border-radius: 6px; border-left: 3px solid #8b5cf6; }
                    .ai-avatar { font-size: 24px; }
                    .ai-desc { font-size: 13.5px; color: #334155; }
                    .file-attachment { display: inline-flex; align-items: center; gap: 5px; background: #fff; border: 1px solid #cbd5e1; padding: 5px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; color: #b91c1c; margin-top: 8px; }
                </style>

                <!-- FASE 1 -->
                <div class="phase-box">
                    <div class="phase-title"><span class="phase-badge">Fase 1</span> New ➔ Refinamento Funcional</div>
                    <div class="tfs-board">
                        <div class="tfs-col"><div class="tfs-col-title">New</div></div>
                        <div class="tfs-col active">
                            <div class="tfs-col-title">Ref. Funcional</div>
                            <div class="tfs-card">
                                <strong>PBI 8492:</strong> Portal de Pagamentos
                                <div><span class="tfs-tag">AI-Started</span></div>
                            </div>
                        </div>
                        <div class="tfs-col"><div class="tfs-col-title">Ref. Técnico</div></div>
                        <div class="tfs-col"><div class="tfs-col-title">Replenishment</div></div>
                    </div>
                    <p>O PO cria o card apenas com a Ideia. O <strong>Agente de PRD (Product Requirements Document)</strong> assume o card automaticamente via Webhook do TFS.</p>
                    <div class="ai-action">
                        <div class="ai-avatar">🤖</div>
                        <div class="ai-desc">
                            <strong>Ação do Agente PRD:</strong> Lê a descrição pífia, pesquisa a base de conhecimento de negócios no Confluence (RAG), formata User Stories, Critérios de Aceite (BDD) e anexa um documento formal de PRD. Atualiza a Description do TFS e adiciona a Tag <code>PRD-Ready</code>.
                            <br>
                            <span class="file-attachment">📄 Funcional_PRD_8492.pdf</span>
                        </div>
                    </div>

                    <div style="margin-top: 20px; border-top: 1px dashed #cbd5e1; padding-top: 15px;">
                        <details style="background: #f1f5f9; border-radius: 6px; padding: 10px; border: 1px solid #cbd5e1;">
                            <summary style="font-weight: bold; color: #334155; cursor: pointer; display: flex; align-items: center; gap: 8px;">
                                ⚙️ Behind the Scenes: Como configurar isso no Kiro?
                            </summary>
                            <div style="margin-top: 15px; font-size: 13.5px; color: #475569;">
                                <p>Para essa mágica acontecer, o Kiro precisa de 3 configurações simples:</p>
                                
                                <strong>1. O Webhook (Escuta o TFS)</strong>
                                <div class="mc-code" style="margin-bottom: 15px;">
<span class="mc-code-comment"># .kiro/hooks/tfs-new-pbi.json</span>
{
  "event": "workitem.created",
  "condition": "payload.fields['System.State'] == 'New'",
  "action": {
    "type": "spawn_agent",
    "agent": "prd-agent",
    "args": { "pbi_id": "{{payload.id}}" }
  }
}
                                </div>

                                <strong>2. O Agent Prompt (Instrui a IA)</strong>
                                <div class="mc-code" style="margin-bottom: 15px;">
<span class="mc-code-comment"># .kiro/agents/prd-agent.md</span>
Você é o Agente de PRD. Seu objetivo é refinar PBIs novos.
Sempre que for acionado com um PBI ID:
1. Use a tool 'tfs_get_workitem' para ler a ideia do PO.
2. Use a tool 'search_confluence_knowledge' (RAG) para buscar regras de negócio relevantes ao tema.
3. Formate a história de usuário e os critérios de aceite em BDD.
4. Use 'tfs_update_description' para salvar no card.
5. Use 'tfs_add_tag' para adicionar a tag "PRD-Ready".
                                </div>

                                <strong>3. Roteamento de Ferramentas (MCPs)</strong>
                                <p>O Kiro injeta essas "tools" no LLM do agente lendo o arquivo principal de servidores MCP:</p>
                                <div class="mc-code">
<span class="mc-code-comment"># .kiro/mcp.json</span>
{
  "mcpServers": {
    "tfs-plugin": {
      "command": "node",
      "args": ["plugins/tfs-mcp.js"]
    },
    "confluence-rag": {
      "command": "python3",
      "args": ["plugins/rag-confluence.py"]
    }
  }
}
                                </div>
                            </div>
                        </details>
                    </div>
                </div>

                <!-- FASE 2 -->
                <div class="phase-box">
                    <div class="phase-title"><span class="phase-badge">Fase 2</span> Refinamento Técnico</div>
                    <div class="tfs-board">
                        <div class="tfs-col"><div class="tfs-col-title">New</div></div>
                        <div class="tfs-col"><div class="tfs-col-title">Ref. Funcional</div></div>
                        <div class="tfs-col active">
                            <div class="tfs-col-title">Ref. Técnico</div>
                            <div class="tfs-card">
                                <strong>PBI 8492:</strong> Portal de Pagamentos
                                <div><span class="tfs-tag">PRD-Ready</span> <span class="tfs-tag">Tech-Spec</span></div>
                            </div>
                        </div>
                        <div class="tfs-col"><div class="tfs-col-title">Replenishment</div></div>
                    </div>
                    <p>Com o Funcional aprovado, a trigger move o card e aciona o <strong>Agente de Spec (Tech Lead AI)</strong>.</p>
                    <div class="ai-action">
                        <div class="ai-avatar">🛠️</div>
                        <div class="ai-desc">
                            <strong>Ação do Agente Spec:</strong> Lê o PDF do PRD, acessa o Github via MCP para entender a arquitetura atual. Gera o modelo de dados (SQL), diagramas Mermaid (C4 Model) e a estratégia de branch. Anexa a Especificação Técnica no PBI.
                            <br>
                            <span class="file-attachment">🧩 Tech_Architecture_8492.md</span>
                        </div>
                    </div>
                </div>

                <!-- FASE 3 -->
                <div class="phase-box">
                    <div class="phase-title"><span class="phase-badge">Fase 3</span> Pronto para Replenishment</div>
                    <p>O card agora contém: <strong>Descrição Refinada, User Stories, BDD, Diagramas e Contratos de API</strong>. O time (humanos) faz a cerimônia de Replenishment, avalia o trabalho já pré-mastigado pela IA, estima e puxa para a Sprint.</p>
                </div>

                <!-- FASE 4 -->
                <div class="phase-box">
                    <div class="phase-title"><span class="phase-badge">Fase 4</span> Em Desenvolvimento (Coleta no Git / End-to-End)</div>
                    <div class="tfs-board">
                        <div class="tfs-col"><div class="tfs-col-title">Sprint Backlog</div></div>
                        <div class="tfs-col active">
                            <div class="tfs-col-title">Em Dev</div>
                            <div class="tfs-card">
                                <strong>PBI 8492:</strong> Portal de Pagamentos
                                <div><span class="tfs-tag">In-Progress</span> <span class="tfs-tag">Kiro-Assigned</span></div>
                            </div>
                        </div>
                        <div class="tfs-col"><div class="tfs-col-title">Em Teste</div></div>
                    </div>
                    <p>Aqui o desenvolvedor entra em ação localmente usando o Kiro na linha de comando.</p>
                    
                    <div class="mc-code">
<span class="mc-code-comment"># O Dev clona o repo publicado e cria a branch baseada no PBI</span>
$ git checkout -b feature/pbi-8492-portal

<span class="mc-code-comment"># Inicia o Kiro passando o ID do PBI. O Kiro usa o MCP do Azure DevOps para ler TODOS os anexos (PRD, Tech Spec) que os agentes anteriores geraram!</span>
$ kiro start --pbi 8492

<span class="mc-code-highlight">[Kiro]</span>: "Baixei o PRD e a Tech Spec. Vejo que precisamos criar o endpoint de pagamentos. Posso iniciar os sub-agentes de Backend e Frontend?"
<span class="mc-code-highlight">[Dev]</span>: "Sim. Use a skill de TDD e crie o código."

<span class="mc-code-comment"># Kiro assume a direção (Steering).</span>
<span class="mc-code-highlight">[Kiro Sub-Agent Backend]</span>: Escrevendo testes (test_payment.py)... Falhou (Red). Escrevendo implementação... Passou (Green).
<span class="mc-code-highlight">[Kiro Sub-Agent Frontend]</span>: Criando formulário em React e vinculando à nova API.

<span class="mc-code-comment"># Coleta no Git - O Kiro faz o commit de cada etapa logando o esforço:</span>
$ git commit -m "feat(pbi-8492): implementa API baseada na Tech Spec"
$ git commit -m "test(pbi-8492): adiciona cobertura BDD validada pelo PRD"

<span class="mc-code-highlight">[Kiro]</span>: "Desenvolvimento concluído. Gostaria que eu abrisse o Pull Request e movesse o PBI para 'Em Teste'?"
<span class="mc-code-highlight">[Dev]</span>: "Sim."
                    </div>
                </div>

                <!-- FASE 5 -->
                <div class="phase-box">
                    <div class="phase-title"><span class="phase-badge">Fase 5</span> Em Teste ➔ Aceite UAT</div>
                    <div class="tfs-board">
                        <div class="tfs-col"><div class="tfs-col-title">Em Dev</div></div>
                        <div class="tfs-col"><div class="tfs-col-title">Em Teste</div></div>
                        <div class="tfs-col active">
                            <div class="tfs-col-title">Aceite UAT</div>
                            <div class="tfs-card">
                                <strong>PBI 8492:</strong> Portal de Pagamentos
                                <div><span class="tfs-tag">QA-Passed</span> <span class="tfs-tag">Ready-Release</span></div>
                            </div>
                        </div>
                    </div>
                    <div class="ai-action">
                        <div class="ai-avatar">🧪</div>
                        <div class="ai-desc">
                            <strong>Ação do Agente QA:</strong> O Pull Request dispara o Pipeline. O agente lê o código gerado, escreve testes E2E em Playwright automatizados, roda contra o ambiente de Staging. Como tudo passa, ele move o TFS para Aceite UAT (User Acceptance Testing) para a aprovação final humana.
                        </div>
                    </div>
                </div>
                <!-- ANIMATED SIMULATOR -->
                <div class="phase-box" style="margin-top: 40px; background: #1e293b; color: white; border: 1px solid #334155;">
                    <div class="phase-title" style="color: white; border-bottom-color: #334155;">
                        <span style="font-size: 20px;">🎬</span> Simulação Animada do Card Kiro
                    </div>
                    <p style="color: #94a3b8; font-size: 13px; margin-bottom: 20px;">Acompanhe o PBI se movendo pelo quadro enquanto a IA anexa os artefatos automaticamente.</p>
                    
                    <div style="display: flex; gap: 10px; position: relative; min-height: 180px;" id="sim-board">
                        <div class="tfs-col" style="flex: 1; background: #334155; border-color: #64748b;" id="col-1"><div class="tfs-col-title" style="color: #cbd5e1;">New</div></div>
                        <div class="tfs-col" style="flex: 1; background: #334155; border-color: #64748b;" id="col-2"><div class="tfs-col-title" style="color: #cbd5e1;">Ref. Funcional</div></div>
                        <div class="tfs-col" style="flex: 1; background: #334155; border-color: #64748b;" id="col-3"><div class="tfs-col-title" style="color: #cbd5e1;">Ref. Técnico</div></div>
                        <div class="tfs-col" style="flex: 1; background: #334155; border-color: #64748b;" id="col-4"><div class="tfs-col-title" style="color: #cbd5e1;">Em Dev</div></div>
                        <div class="tfs-col" style="flex: 1; background: #334155; border-color: #64748b;" id="col-5"><div class="tfs-col-title" style="color: #cbd5e1;">Aceite UAT</div></div>
                        
                        <!-- Animated Card -->
                        <div id="sim-card" style="background: #fff; border: 1px solid #0ea5e9; border-left: 4px solid #0ea5e9; padding: 10px; border-radius: 4px; font-size: 12px; color: #0f172a; position: absolute; width: calc(20% - 20px); transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); opacity: 0; z-index: 10;">
                            <strong>PBI 8492:</strong> Portal de Pagamentos
                            <div id="sim-tags" style="margin-top: 8px; min-height: 20px; display:flex; flex-wrap:wrap; gap:4px;">
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </details>
    `;

    // Start simulation loop
    if (window.kiroSimulationInterval) clearInterval(window.kiroSimulationInterval);
    
    setTimeout(() => {
        const card = document.getElementById('sim-card');
        const tags = document.getElementById('sim-tags');
        if (!card || !tags) return;
        
        let step = 0;
        
        window.kiroSimulationInterval = setInterval(() => {
            const cols = [
                document.getElementById('col-1'),
                document.getElementById('col-2'),
                document.getElementById('col-3'),
                document.getElementById('col-4'),
                document.getElementById('col-5')
            ];
            
            if (!cols[0]) {
                clearInterval(window.kiroSimulationInterval);
                return;
            }
            
            if (step === 0) {
                // Reset to col-1
                card.style.opacity = '0'; // fade out briefly
                setTimeout(() => {
                    card.style.left = cols[0].offsetLeft + 10 + 'px';
                    card.style.top = cols[0].offsetTop + 40 + 'px';
                    tags.innerHTML = '';
                    card.style.opacity = '1';
                }, 300);
            } else if (step === 1) {
                // Funcional
                card.style.left = cols[1].offsetLeft + 10 + 'px';
                setTimeout(() => {
                    tags.innerHTML += '<span class="tfs-tag" style="background:#fef08a; color:#854d0e;">📄 PRD</span>';
                }, 600);
            } else if (step === 2) {
                // Tech
                card.style.left = cols[2].offsetLeft + 10 + 'px';
                setTimeout(() => {
                    tags.innerHTML += '<span class="tfs-tag" style="background:#e0e7ff; color:#3730a3;">🧩 Spec</span>';
                    tags.innerHTML += '<span class="tfs-tag" style="background:#fee2e2; color:#991b1b;">🛡️ ADR</span>';
                }, 600);
            } else if (step === 3) {
                // Dev
                card.style.left = cols[3].offsetLeft + 10 + 'px';
                setTimeout(() => {
                    tags.innerHTML += '<span class="tfs-tag" style="background:#dcfce7; color:#166534;">⚙️ Code</span>';
                }, 600);
            } else if (step === 4) {
                // Test
                card.style.left = cols[4].offsetLeft + 10 + 'px';
                setTimeout(() => {
                    tags.innerHTML += '<span class="tfs-tag" style="background:#ccfbf1; color:#115e59;">🧪 Passed</span>';
                }, 600);
            }
            
            step++;
            if (step > 6) step = 0; // Pause for 2 ticks before resetting
            
        }, 2200);
        
        // Initial positioning
        card.style.left = document.getElementById('col-1').offsetLeft + 10 + 'px';
        card.style.top = document.getElementById('col-1').offsetTop + 40 + 'px';
        card.style.opacity = '1';
        
    }, 500);
}

window.initKiroDocView = initKiroDocView;
