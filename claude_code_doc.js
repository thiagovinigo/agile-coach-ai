function initClaudeCodeDocView() {
    const container = document.getElementById('claude-code-view');
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
                background: #ecfdf5;
                border-bottom: 2px solid #10b981;
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
            .mc-code-highlight { color: #34d399; }
            .mc-code-comment { color: #64748b; font-style: italic; }
            .mc-callout {
                background: #eff6ff;
                border-left: 4px solid #3b82f6;
                padding: 15px;
                border-radius: 4px;
                margin: 15px 0;
            }
        </style>

        <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #064e3b);">
            <div class="tag" style="background:#10b981;">MASTERCLASS "10.000 HORAS"</div>
            <h2>💻 Claude Code: A IDE Agentic Raiz</h2>
            <p style="margin-top:10px;">Dominar o Claude Code não é apenas "conversar com uma tela preta". É criar ferramentas customizadas, configurar Git Hooks para autodefesa e entender o REPL profundamente. Abaixo, os módulos avançados do desenvolvedor 10x.</p>
        </div>

        <!-- MÓDULO 1 -->
        <details class="mc-accordion" open>
            <summary><span style="font-size:24px;">⌨️</span> Módulo 1: Engenharia de Prompts no Terminal</summary>
            <div class="mc-content">
                <p>O REPL (Read-Eval-Print Loop) do Claude Code mantém todo o histórico do seu chat em memória durante a sessão. Entender isso é vital para otimizar custo e evitar alucinação.</p>
                
                <h4 style="color:#1e293b; margin-top:20px;">1. Gerenciamento de Contexto (Context Window)</h4>
                <p>Se você pedir para o Claude "refatorar o projeto inteiro", ele vai ler milhares de arquivos, estourar o limite de 200K tokens e custar 3 dólares em uma única chamada. O especialista 10.000 horas usa escopos rígidos.</p>
                <div class="mc-code">
<span class="mc-code-comment"># AMADOR:</span>
> Refatore os testes do projeto.

<span class="mc-code-comment"># ESPECIALISTA:</span>
> Liste os arquivos em /testes/e2e que estão falhando.
> (Claude lista 3 arquivos).
> Focando APENAS no arquivo 'checkout.spec.js', refatore para reduzir o flakiness usando Waits explícitos do Playwright.
                </div>

                <h4 style="color:#1e293b; margin-top:20px;">2. Técnicas de Prompting Interativo</h4>
                <p>Para evitar código destrutivo, ordene que o Claude pare antes de agir.</p>
                <div class="mc-callout">
                    <strong>Padrão "Ask before write":</strong> <code>"Analise o problema de concorrência no DB. Escreva um plano detalhado em Markdown. PARE. Só comece a editar os arquivos de código depois que eu disser 'prossiga'."</code>
                </div>
            </div>
        </details>

        <!-- MÓDULO 2 -->
        <details class="mc-accordion">
            <summary><span style="font-size:24px;">📁</span> Módulo 2: O Poder da Pasta .claudecode</summary>
            <div class="mc-content">
                <p>O Claude lê os arquivos ocultos para entender as regras da casa. Se você não configurá-los, ele escreverá código genérico (ou pior, em JavaScript quando seu projeto é TypeScript estrito).</p>

                <h4 style="color:#1e293b; margin-top:20px;">1. CONVENTIONS.md por Diretório (DDD)</h4>
                <p>Em uma arquitetura hexagonal ou Domain Driven Design, a camada de <code>Domain</code> tem regras diferentes da camada de <code>Infrastructure</code>. Coloque um <code>CONVENTIONS.md</code> em cada pasta.</p>
                <div class="mc-code">
<span class="mc-code-comment"># src/domain/.claudecode/CONVENTIONS.md</span>
Regra Absoluta: NUNCA importe nada da pasta 'src/infrastructure' aqui. 
A camada de Domínio deve ser 100% isolada e não ter dependências externas.
                </div>

                <h4 style="color:#1e293b; margin-top:20px;">2. Lints e Autodefesa via Git Hooks</h4>
                <p>O Claude pode cometer erros de sintaxe. Use o próprio ambiente para barrá-lo.</p>
                <div class="mc-callout" style="border-color:#10b981; background:#ecfdf5;">
                    Adicione ao <code>CONVENTIONS.md</code> global: <code>"Após editar arquivos .ts, VOCÊ DEVE OBRIGATORIAMENTE rodar 'npm run lint'. Se falhar, corrija seus próprios erros sozinho antes de me avisar que terminou."</code>
                </div>
            </div>
        </details>

        <!-- MÓDULO 3 -->
        <details class="mc-accordion">
            <summary><span style="font-size:24px;">🔧</span> Módulo 3: Construindo Custom Skills (MCPs)</summary>
            <div class="mc-content">
                <p>O poder supremo de uma IDE Agentic não é ler arquivos, é executar ações complexas. O Claude Code suporta <strong>MCP (Model Context Protocol)</strong>, permitindo que você injete novas ferramentas nativas.</p>

                <h4 style="color:#1e293b; margin-top:20px;">Estudo de Caso: Refatoração de Testes E2E Flaky</h4>
                <p>Você tem 500 testes Cypress. Alguns falham aleatoriamente ("Flaky"). Você cria um script Python que conecta na API do Cypress Dashboard, baixa o histórico de falhas e lista os testes mais instáveis da semana. Você empacota isso num MCP.</p>
                
                <div class="mc-code">
<span class="mc-code-comment"># Registrando sua ferramenta local</span>
> /plugin add local ./meus-scripts/cypress-mcp-server

<span class="mc-code-comment"># Uso do Claude agora turbinado:</span>
> Claude, chame sua nova tool 'get_flaky_tests'. 
> Ache o teste que mais falhou hoje. Abra o arquivo dele, 
> descubra por que a Promise está vazando, e refatore.
                </div>
                <p>O Claude usa o MCP para buscar o JSON do Cypress, entende o nome do teste, usa a ferramenta <code>read_file</code> para achar o código, conserta a Promise e usa <code>write_file</code> para salvar. Tudo autônomo.</p>
            </div>
        </details>

        <!-- MÓDULO 4 -->
        <details class="mc-accordion">
            <summary><span style="font-size:24px;">🚑</span> Módulo 4: Troubleshooting e Disaster Recovery</summary>
            <div class="mc-content">
                <p>As IAs não são perfeitas. O que você faz quando deixa o Claude refatorando e ele acidentalmente apaga configurações vitais ou entra em loop infinito quebrando o build repetidamente?</p>

                <h4 style="color:#1e293b; margin-top:20px;">1. Lidando com Loop de Dependências (Dependency Hell)</h4>
                <p>Se o Claude entrar num loop de <i>"Rodou teste -> Falhou -> Editou -> Falhou -> Editou"</i>, você interrompe no terminal (Ctrl+C). O primeiro passo é analisar a stack original.</p>
                <div class="mc-callout" style="border-color:#f59e0b; background:#fffbeb;">
                    <strong>Dica de Sobrevivência:</strong> Use o comando <code>/history</code> para ver o histórico do buffer. Diga: <code>"Pare. Esqueça tudo o que você tentou nos últimos 3 passos. Faça um git reset --hard HEAD, vamos recomeçar abordando o problema por outro ângulo."</code>
                </div>

                <h4 style="color:#1e293b; margin-top:20px;">2. Limitando o Blast Radius</h4>
                <p>Quando for pedir uma refatoração em larga escala, crie uma branch isolada e restrinja as permissões de Escrita do Agente até que você tenha confiança na estratégia dele.</p>
            </div>
        </details>

        <!-- MÓDULO 5 -->
        <details class="mc-accordion">
            <summary><span style="font-size:24px;">💰</span> Módulo 5: Nunca Estoure Seus Limites de Tokens</summary>
            <div class="mc-content">
                <p>As ferramentas de código aberto e os hábitos gratuitos que você deve usar para parar de queimar tokens do Claude. Clone, adicione e salve contexto.</p>

                <h4 style="color:#3b82f6; margin-top:20px;">🟦 Servidores MCP</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Serena:</strong> Lê seu código por símbolo, não por arquivos inteiros.</li>
                    <li><strong>Context7:</strong> Documentação atualizada sob demanda, sem desperdício de tokens em APIs ruins.</li>
                    <li><strong>Claude Context:</strong> Busca semântica, traz apenas o código que importa.</li>
                    <li><strong>Token Savior:</strong> Navegação por símbolos + memória de sessão.</li>
                </ul>

                <h4 style="color:#d946ef; margin-top:20px;">🟪 Skills & Plugins</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>Caveman:</strong> Faz o Claude responder no modo curto, com menos tokens de saída.</li>
                    <li><strong>Context Mode:</strong> Coloca a saída da ferramenta (sandbox) em SQLite, não no seu contexto.</li>
                    <li><strong>Token Optimizer:</strong> Caça tokens fantasmas e compacta o contexto de forma inteligente.</li>
                </ul>

                <h4 style="color:#f97316; margin-top:20px;">🟧 Ferramentas de CLI</h4>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li><strong>MarkItDown:</strong> Converte PDFs e arquivos para Markdown limpo.</li>
                    <li><strong>Repomix:</strong> Empacota um repositório inteiro em um único arquivo com contagem de tokens.</li>
                    <li><strong>ccusage:</strong> Mostra uso de tokens e custo a partir de logs locais.</li>
                    <li><strong>Code Review Graph:</strong> Mapa de árvore, carrega apenas o que importa.</li>
                </ul>

                <div class="mc-callout" style="border-color:#10b981; background:#ecfdf5;">
                    <strong style="color:#065f46;">✅ HÁBITOS GRATUITOS (Nenhuma instalação necessária)</strong>
                    <div style="display: flex; gap: 20px; margin-top: 10px; color: #064e3b; font-size: 13.5px;">
                        <div style="flex: 1;">
                            <strong>No Chat do Claude:</strong>
                            <ul style="padding-left: 15px; margin-top: 5px;">
                                <li>Edite sua última mensagem, não empilhe novas</li>
                                <li>Inicie um chat novo a cada 15 mensagens</li>
                                <li>Agrupe suas perguntas em um único prompt</li>
                                <li>Desative Busca e Artefatos quando estiver ocioso</li>
                                <li>Configure Memória para nunca reexplicar</li>
                                <li>Use Projetos para carregar seus arquivos uma vez</li>
                            </ul>
                        </div>
                        <div style="flex: 1;">
                            <strong>No Código do Claude:</strong>
                            <ul style="padding-left: 15px; margin-top: 5px;">
                                <li>Escreva um CLAUDE.md direto na raiz do projeto</li>
                                <li>Execute <code>/compact</code> quando o contexto atingir 50%</li>
                                <li>Use <code>/clear</code> entre tarefas não relacionadas</li>
                                <li>Leia o arquivo exato, não a pasta inteira</li>
                                <li>Planeje antes de construir, não prescreva a correção</li>
                                <li>Combine com o modelo: Sonnet executa, Opus estrategiza</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </details>

        <!-- SEÇÃO: TABELA DE SKILLS (Requerido) -->
        <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:25px; box-shadow:0 4px 6px rgba(0,0,0,0.05); margin-top:30px;">
            <strong style="color:#0f172a; font-size:18px; display:flex; align-items:center; gap:8px; margin-bottom:15px; border-bottom:2px solid #8b5cf6; padding-bottom:10px;">
                <span style="font-size:24px;">🌐</span> Fontes de Skills Públicas (Plugins & Marketplaces)
            </strong>
            <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:15px;">
                O ecossistema permite a importação de Skills/Plugins criados pela comunidade. Abaixo, os principais repositórios para acelerar seu setup:
            </p>

            <div style="display:flex; gap:10px; margin-bottom:20px; flex-wrap:wrap;">
                <a href="https://skillsmp.com/search?q=discovery" target="_blank" style="background:#f3f4f6; color:#4f46e5; padding:8px 12px; border-radius:6px; text-decoration:none; font-size:13px; border:1px solid #e5e7eb; display:flex; align-items:center; gap:5px;">🔍 Skills MP (Discovery)</a>
                <a href="https://goodailist.com/repos?search=research" target="_blank" style="background:#f3f4f6; color:#4f46e5; padding:8px 12px; border-radius:6px; text-decoration:none; font-size:13px; border:1px solid #e5e7eb; display:flex; align-items:center; gap:5px;">🔬 Good AI List (Research)</a>
                <a href="https://aitmpl.com/skills/" target="_blank" style="background:#f3f4f6; color:#4f46e5; padding:8px 12px; border-radius:6px; text-decoration:none; font-size:13px; border:1px solid #e5e7eb; display:flex; align-items:center; gap:5px;">🧩 AI TMPL (Templates)</a>
            </div>

            <div style="overflow-x:auto;">
                <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left;">
                    <thead>
                        <tr style="background:#f8fafc; border-bottom:2px solid #cbd5e1;">
                            <th style="padding:12px; color:#1e293b; font-weight:bold;">Categoria da Fonte</th>
                            <th style="padding:12px; color:#1e293b; font-weight:bold;">Nome do Repositório ou Registro</th>
                            <th style="padding:12px; color:#1e293b; font-weight:bold;">Descritivo Analítico e Foco de Domínio</th>
                            <th style="padding:12px; color:#1e293b; font-weight:bold;">Método Principal de Integração</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom:1px solid #e2e8f0; hover:background:#f1f5f9;">
                            <td style="padding:12px; color:#475569;">Oficial (Anthropic)</td>
                            <td style="padding:12px; color:#3b82f6; font-family:monospace; font-weight:bold;">anthropics/skills</td>
                            <td style="padding:12px; color:#475569; line-height:1.5;">Abriga as Skills oficiais para processamento de documentos corporativos (.docx, .pdf, .xlsx, .pptx) e a vital meta-habilidade <code>skill-creator</code>.</td>
                            <td style="padding:12px; color:#475569; line-height:1.5;">Via CLI nativa: <code>/plugin marketplace add anthropics/skills</code> seguido de <code>/plugin install</code>.</td>
                        </tr>
                        <tr style="border-bottom:1px solid #e2e8f0; hover:background:#f1f5f9;">
                            <td style="padding:12px; color:#475569;">Mega-Coleção Comunitária</td>
                            <td style="padding:12px; color:#3b82f6; font-family:monospace; font-weight:bold;">alirezarezvani/claude-skills</td>
                            <td style="padding:12px; color:#475569; line-height:1.5;">Biblioteca documentada contendo mais de 192 fluxos de trabalho prontos para produção. Forte ênfase em "Personas".</td>
                            <td style="padding:12px; color:#475569; line-height:1.5;">Importação via clonagem tradicional do Git ou registro como plugin de marketplace.</td>
                        </tr>
                        <tr style="border-bottom:1px solid #e2e8f0; hover:background:#f1f5f9;">
                            <td style="padding:12px; color:#475569;">Mega-Coleção Comunitária</td>
                            <td style="padding:12px; color:#3b82f6; font-family:monospace; font-weight:bold;">obra/superpowers</td>
                            <td style="padding:12px; color:#475569; line-height:1.5;">Foco estrito em metodologias avançadas de engenharia de software e práticas de desenvolvimento direcionado a testes (TDD).</td>
                            <td style="padding:12px; color:#475569; line-height:1.5;">Instalação via marketplace oficial estendido do Claude Code ou via scripts de integração.</td>
                        </tr>
                        <tr style="hover:background:#f1f5f9;">
                            <td style="padding:12px; color:#475569;">Lista Curada (Awesome)</td>
                            <td style="padding:12px; color:#3b82f6; font-family:monospace; font-weight:bold;">travisvn/awesome-claude-skills</td>
                            <td style="padding:12px; color:#475569; line-height:1.5;">Índice especializado em ferramentas de design, pesquisa e desenvolvimento tático. Destaca integrações para frameworks.</td>
                            <td style="padding:12px; color:#475569; line-height:1.5;">Manual; clonagem de instâncias individuais e alocação local do arquivo <code>SKILL.md</code>.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

window.initClaudeCodeDocView = initClaudeCodeDocView;
