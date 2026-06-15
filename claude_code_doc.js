function initClaudeCodeDocView() {
    const container = document.getElementById('claude-code-view');
    if (!container) return;

    container.innerHTML = `
        <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #064e3b);">
            <div class="tag" style="background:#10b981;">CLAUDE CODE CLI</div>
            <h2>💻 Claude Code: A IA Raiz no seu Terminal</h2>
            <p style="margin-top:10px;">Ao contrário do Kiro (que orquestra o macro), o <strong>Claude Code</strong> é uma ferramenta de terminal baseada em REPL (Read-Eval-Print Loop). Ele fica enraizado no seu repositório local, entendendo sua base de código, executando comandos bash e criando código diretamente na sua máquina.</p>
        </div>

        <div style="display:grid; grid-template-columns: 1fr; gap:20px; align-items:start;">
            
            <!-- Section 1: Overview -->
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:25px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <strong style="color:#0f172a; font-size:18px; display:flex; align-items:center; gap:8px; margin-bottom:15px; border-bottom:2px solid #10b981; padding-bottom:10px;">
                    <span style="font-size:24px;">⌨️</span> 1. O Fluxo de Trabalho (Terminal)
                </strong>
                <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:15px;">
                    O Claude Code é instalado via NPM (<code>npm install -g @anthropic-ai/claude-code</code>). Depois de autenticar (OAuth), você abre o seu repositório e digita <code>claude</code>. A partir daí, o fluxo muda de UI para Texto puro:
                </p>
                <div style="background:#0f172a; padding:20px; border-radius:8px; color:#10b981; font-family:'Courier New', Courier, monospace; font-size:13px; line-height:1.6; overflow-x:auto;">
$ cd /meu-projeto
$ claude
<span style="color:#94a3b8;">╭─────────────────────────╮
│ Bem-vindo ao Claude!    │
╰─────────────────────────╯</span>

<span style="color:#3b82f6;">> Você:</span> Olhe a pasta /src/components/auth e refatore o LoginOTP.jsx para usar TypeScript.

<span style="color:#eab308;">[Claude]</span> Procurando pasta auth...
<span style="color:#eab308;">[Claude]</span> Executando grep_search "LoginOTP"...
<span style="color:#eab308;">[Claude]</span> Renomeando arquivo para LoginOTP.tsx...
<span style="color:#eab308;">[Claude]</span> Executando "npx tsc --noEmit" para checar erros...
<span style="color:#ef4444;">[Claude]</span> Encontrei erros de tipagem na linha 42. Corrigindo...
<span style="color:#10b981;">[Claude]</span> ✔ Refatoração completa. Posso criar o commit? (y/N)
                </div>
            </div>

            <!-- Section 2: Folder Structure & Context -->
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:25px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <strong style="color:#0f172a; font-size:18px; display:flex; align-items:center; gap:8px; margin-bottom:15px; border-bottom:2px solid #3b82f6; padding-bottom:10px;">
                    <span style="font-size:24px;">📁</span> 2. Estrutura de Pastas e Convenções (.claudecode)
                </strong>
                <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:15px;">
                    Para que o Claude não saia quebrando a arquitetura do seu projeto, você deve criar arquivos de convenção (System Prompts).
                </p>
                
                <div style="display:flex; gap:20px; flex-wrap:wrap;">
                    <div style="flex:1; min-width:300px; background:#f8fafc; padding:15px; border-radius:8px; border:1px solid #cbd5e1; font-family:monospace; font-size:12px; line-height:1.5;">
meu-projeto/
├── .claudecode/
│   ├── CONVENTIONS.md  <span style="color:#64748b;">// Regras globais de engenharia</span>
│   ├── README.md       <span style="color:#64748b;">// Arquitetura macro</span>
│   └── plugins/        <span style="color:#64748b;">// Custom tools e bash scripts</span>
├── src/
│   └── utils/
│       └── .claude.md  <span style="color:#64748b;">// Regras específicas só para utils</span>
└── package.json
                    </div>
                    <div style="flex:1; min-width:300px; background:#eff6ff; border-left:4px solid #3b82f6; padding:15px; border-radius:8px;">
                        <h4 style="color:#1e40af; margin-bottom:8px;">Exemplo de CONVENTIONS.md</h4>
                        <p style="font-size:12px; color:#1e3a8a; margin:0; line-height:1.5; font-family:sans-serif;">
                            "Sempre use Arrow Functions no React.<br><br>
                            Sempre que usar a ferramenta <code>write_file</code>, não crie componentes com mais de 150 linhas; quebre-os em arquivos menores.<br><br>
                            Sempre rode <code>npm run lint:fix</code> antes de encerrar o trabalho."
                        </p>
                    </div>
                </div>
            </div>

            <!-- Section 3: Public Skills Table -->
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:25px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <strong style="color:#0f172a; font-size:18px; display:flex; align-items:center; gap:8px; margin-bottom:15px; border-bottom:2px solid #8b5cf6; padding-bottom:10px;">
                    <span style="font-size:24px;">🌐</span> 3. Fontes de Skills Públicas (Plugins & Marketplaces)
                </strong>
                <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:15px;">
                    O ecossistema do Claude Code permite a importação de Skills/Plugins criados pela comunidade para agilizar fluxos de trabalho (como TDD, Parsing de PDFs ou Integrações de Banco). Abaixo, os principais repositórios e registros públicos:
                </p>

                <!-- Helpful Links -->
                <div style="display:flex; gap:10px; margin-bottom:20px; flex-wrap:wrap;">
                    <a href="https://skillsmp.com/search?q=discovery" target="_blank" style="background:#f3f4f6; color:#4f46e5; padding:8px 12px; border-radius:6px; text-decoration:none; font-size:13px; border:1px solid #e5e7eb; display:flex; align-items:center; gap:5px;">
                        🔍 Skills MP (Discovery)
                    </a>
                    <a href="https://goodailist.com/repos?search=research" target="_blank" style="background:#f3f4f6; color:#4f46e5; padding:8px 12px; border-radius:6px; text-decoration:none; font-size:13px; border:1px solid #e5e7eb; display:flex; align-items:center; gap:5px;">
                        🔬 Good AI List (Research)
                    </a>
                    <a href="https://aitmpl.com/skills/" target="_blank" style="background:#f3f4f6; color:#4f46e5; padding:8px 12px; border-radius:6px; text-decoration:none; font-size:13px; border:1px solid #e5e7eb; display:flex; align-items:center; gap:5px;">
                        🧩 AI TMPL (Templates)
                    </a>
                </div>

                <!-- Table -->
                <div style="overflow-x:auto;">
                    <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left;">
                        <thead>
                            <tr style="background:#f8fafc; border-bottom:2px solid #cbd5e1;">
                                <th style="padding:12px; color:#1e293b; font-weight:bold;">Categoria da Fonte</th>
                                <th style="padding:12px; color:#1e293b; font-weight:bold;">Nome do Repositório ou Registro</th>
                                <th style="padding:12px; color:#1e293b; font-weight:bold;">Descritivo Analítico e Foco de Domínio</th>
                                <th style="padding:12px; color:#1e293b; font-weight:bold;">Método Principal de Integração e Instalação</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="border-bottom:1px solid #e2e8f0; hover:background:#f1f5f9;">
                                <td style="padding:12px; color:#475569;">Oficial (Anthropic)</td>
                                <td style="padding:12px; color:#3b82f6; font-family:monospace; font-weight:bold;">anthropics/skills</td>
                                <td style="padding:12px; color:#475569; line-height:1.5;">Abriga as Skills oficiais para processamento de documentos corporativos (.docx, .pdf, .xlsx, .pptx) e a vital meta-habilidade <code>skill-creator</code>.</td>
                                <td style="padding:12px; color:#475569; line-height:1.5;">Via CLI nativa: <code>/plugin marketplace add anthropics/skills</code> seguido de <code>/plugin install</code> para conjuntos de domínio específicos.</td>
                            </tr>
                            <tr style="border-bottom:1px solid #e2e8f0;">
                                <td style="padding:12px; color:#475569;">Mega-Coleção Comunitária</td>
                                <td style="padding:12px; color:#3b82f6; font-family:monospace; font-weight:bold;">alirezarezvani/claude-skills</td>
                                <td style="padding:12px; color:#475569; line-height:1.5;">Biblioteca documentada contendo mais de 192 fluxos de trabalho prontos para produção. Notável por sua forte ênfase em "Personas".</td>
                                <td style="padding:12px; color:#475569; line-height:1.5;">Importação via clonagem tradicional do Git ou registro como plugin de marketplace personalizado.</td>
                            </tr>
                            <tr style="border-bottom:1px solid #e2e8f0;">
                                <td style="padding:12px; color:#475569;">Mega-Coleção Comunitária</td>
                                <td style="padding:12px; color:#3b82f6; font-family:monospace; font-weight:bold;">obra/superpowers</td>
                                <td style="padding:12px; color:#475569; line-height:1.5;">Foco estrito em metodologias avançadas de engenharia de software e práticas de desenvolvimento direcionado a testes (TDD).</td>
                                <td style="padding:12px; color:#475569; line-height:1.5;">Instalação via marketplace oficial estendido do Claude Code ou via scripts de integração incluídos no diretório base.</td>
                            </tr>
                            <tr>
                                <td style="padding:12px; color:#475569;">Lista Curada (Awesome)</td>
                                <td style="padding:12px; color:#3b82f6; font-family:monospace; font-weight:bold;">travisvn/awesome-claude-skills</td>
                                <td style="padding:12px; color:#475569; line-height:1.5;">Índice especializado em ferramentas de design, pesquisa e desenvolvimento tático. Destaca integrações para frameworks específicos.</td>
                                <td style="padding:12px; color:#475569; line-height:1.5;">Manual; requer navegação pelas submissões listadas, clonagem de instâncias individuais e alocação local do arquivo <code>SKILL.md</code>.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>

        </div>
    `;
}

window.initClaudeCodeDocView = initClaudeCodeDocView;
