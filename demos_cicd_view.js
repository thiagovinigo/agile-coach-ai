document.addEventListener('DOMContentLoaded', () => {
    initDemosCicdView();
});

function initDemosCicdView() {
    const container = document.getElementById('demos-cicd-view');
    if (!container || typeof demosCicdData === 'undefined') return;

    container.innerHTML = '';

    // Scoped styles for Demos CI/CD View
    const styleEl = document.createElement('style');
    styleEl.textContent = `
        .dc-hero {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #312e81 100%);
            color: #fff;
            padding: 28px 32px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .dc-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(56, 189, 248, 0.2);
            border: 1px solid rgba(56, 189, 248, 0.45);
            color: #38bdf8;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 4px 12px;
            border-radius: 999px;
            margin-bottom: 12px;
        }
        .dc-hero h2 {
            margin: 0 0 8px 0;
            font-size: 1.85rem;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        .dc-hero p {
            margin: 0;
            font-size: 1.02rem;
            line-height: 1.6;
            color: #cbd5e1;
            max-width: 920px;
        }
        .dc-mode-bar {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .dc-mode-btn {
            padding: 9px 18px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.08);
            color: #e2e8f0;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .dc-mode-btn:hover {
            background: rgba(255,255,255,0.15);
        }
        .dc-mode-btn.active {
            background: linear-gradient(135deg, #2563eb, #06b6d4);
            border-color: transparent;
            color: #fff;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
        }
        .dc-guide-container {
            padding: 28px 32px;
            max-width: 1280px;
            margin: 0 auto;
        }
        .dc-card {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        .dc-title {
            margin: 0 0 6px 0;
            font-size: 1.3rem;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .dc-sub {
            margin: 0 0 20px 0;
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
        }
        .dc-grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        .dc-grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
        }
        .dc-grid-5 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 14px;
        }
        .dc-step-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-top: 4px solid #2563eb;
            border-radius: 10px;
            padding: 15px;
        }
        .dc-code-box {
            background: #0f172a;
            color: #e2e8f0;
            padding: 16px 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.83rem;
            line-height: 1.6;
            overflow-x: auto;
            white-space: pre;
        }
        .dc-file-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #2563eb;
            border-radius: 10px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .dc-file-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(0,0,0,0.06);
            border-left-color: #06b6d4;
        }
        .dc-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }
        .dc-table th, .dc-table td {
            padding: 11px 14px;
            border: 1px solid #e2e8f0;
            text-align: left;
        }
        .dc-table th {
            background: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
        }
    `;
    container.appendChild(styleEl);

    // Hero Header
    const hero = document.createElement('div');
    hero.className = 'dc-hero';
    hero.innerHTML = `
        <div class="dc-badge">🐙 GITHUB ACTIONS · CI/CD · CLAUDE CODE ENGINEERING</div>
        <h2>🐙 Demos GitHub & CI/CD: Bot de Code Review em PRs <span style="font-size:0.95rem; font-weight:600; color:#38bdf8; background:rgba(255,255,255,0.1); padding:4px 10px; border-radius:6px;">Warmup Local + Workflow Real</span></h2>
        <p>
            Laboratório completo demonstrando como integrar o <strong>Claude Haiku 4.5</strong> diretamente na esteira de CI/CD do GitHub Actions para revisar todo Pull Request aberto ou atualizado. Inclui o <strong>Warmup 100% Local (<code>local_review.py</code>)</strong>, o <strong>Workflow Oficial (<code>claude-review.yml</code> + <code>review_pr.py</code>)</strong>, arquivo com <strong>bugs plantados (<code>example-bug.py</code>)</strong> e comparativo com a Action oficial <code>anthropics/claude-code-action@v1</code>.
        </p>
        <div class="dc-mode-bar">
            <button class="dc-mode-btn active" id="dc-btn-guide">✨ Guia de Arquitetura, Bugs & CI/CD</button>
            <button class="dc-mode-btn" id="dc-btn-docs">💻 Explorador de Código & Workflows (6 arquivos)</button>
        </div>
    `;
    container.appendChild(hero);

    // Mode 1: Visual Guide
    const guideWrapper = document.createElement('div');
    guideWrapper.className = 'dc-guide-container';
    guideWrapper.id = 'dc-guide-wrapper';

    // Mode 2: Code Explorer
    const docsWrapper = document.createElement('div');
    docsWrapper.className = 'kb-layout';
    docsWrapper.id = 'dc-docs-wrapper';
    docsWrapper.style.display = 'none';

    container.appendChild(guideWrapper);
    container.appendChild(docsWrapper);

    window.openDemosCicdDoc = function(docId) {
        document.getElementById('dc-btn-docs').click();
        const targetBtn = document.querySelector(`#dc-docs-wrapper .kb-nav-btn[data-doc-id="${docId}"]`);
        if (targetBtn) {
            targetBtn.click();
            targetBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    };

    guideWrapper.innerHTML = `
        <!-- 1. PIPELINE DO BOT DE PR REVIEW NO GITHUB ACTIONS -->
        <div class="dc-card">
            <h3 class="dc-title">⚙️ Como Funciona a Esteira de Code Review no GitHub Actions (5 Etapas)</h3>
            <p class="dc-sub">Sempre que um desenvolvedor abre ou atualiza um Pull Request, o runner Ubuntu executa o ciclo abaixo em ~30 segundos:</p>
            <div class="dc-grid-5">
                <div class="dc-step-box">
                    <div style="font-size:0.72rem; font-weight:800; color:#2563eb; text-transform:uppercase; margin-bottom:4px;">PASSO 1 · TRIGGER</div>
                    <div style="font-weight:800; color:#0f172a; font-size:0.98rem; margin-bottom:6px;">🔔 Evento de PR</div>
                    <div style="font-size:0.82rem; color:#475569; line-height:1.5;">
                        Dispara em <code>pull_request: [opened, synchronize, reopened]</code> com permissão explícita <code>pull-requests: write</code>.
                    </div>
                </div>
                <div class="dc-step-box" style="border-top-color:#0284c7;">
                    <div style="font-size:0.72rem; font-weight:800; color:#0284c7; text-transform:uppercase; margin-bottom:4px;">PASSO 2 · CHECKOUT</div>
                    <div style="font-weight:800; color:#0f172a; font-size:0.98rem; margin-bottom:6px;">📥 Histórico Completo</div>
                    <div style="font-size:0.82rem; color:#475569; line-height:1.5;">
                        Roda <code>actions/checkout@v4</code> com <strong><code>fetch-depth: 0</code></strong> para garantir acesso tanto ao <code>BASE_SHA</code> quanto ao <code>HEAD_SHA</code>.
                    </div>
                </div>
                <div class="dc-step-box" style="border-top-color:#0ea5e9;">
                    <div style="font-size:0.72rem; font-weight:800; color:#0ea5e9; text-transform:uppercase; margin-bottom:4px;">PASSO 3 · GIT DIFF</div>
                    <div style="font-weight:800; color:#0f172a; font-size:0.98rem; margin-bottom:6px;">📄 Extração & Trava</div>
                    <div style="font-size:0.82rem; color:#475569; line-height:1.5;">
                        Executa <code>git diff base...head</code> e aplica trava de segurança em <strong><code>MAX_DIFF_CHARS = 30_000</code></strong> para proteger a janela de contexto.
                    </div>
                </div>
                <div class="dc-step-box" style="border-top-color:#8b5cf6;">
                    <div style="font-size:0.72rem; font-weight:800; color:#7c3aed; text-transform:uppercase; margin-bottom:4px;">PASSO 4 · CLAUDE HAIKU</div>
                    <div style="font-weight:800; color:#0f172a; font-size:0.98rem; margin-bottom:6px;">🤖 Análise Sênior</div>
                    <div style="font-size:0.82rem; color:#475569; line-height:1.5;">
                        Envia título, autor e diff ao <code>claude-haiku-4-5</code> (com retry exponencial) pedindo: ✅ Positivos, ⚠️ Problemas e 💡 Melhorias (máx. 250 palavras).
                    </div>
                </div>
                <div class="dc-step-box" style="border-top-color:#10b981;">
                    <div style="font-size:0.72rem; font-weight:800; color:#059669; text-transform:uppercase; margin-bottom:4px;">PASSO 5 · GH COMMENT</div>
                    <div style="font-weight:800; color:#0f172a; font-size:0.98rem; margin-bottom:6px;">💬 Postagem no PR</div>
                    <div style="font-size:0.82rem; color:#475569; line-height:1.5;">
                        Usa o <code>GITHUB_TOKEN</code> nativo do runner para rodar <code>gh pr comment</code> e publicar o feedback formatado direto na timeline do PR.
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. COMPARATIVO: WARMUP LOCAL VS WORKFLOW EM PRODUÇÃO -->
        <div class="dc-card">
            <h3 class="dc-title">⚖️ As 2 Etapas da Demo: Warmup Local vs Bot no GitHub Actions</h3>
            <p class="dc-sub">Clique em qualquer card abaixo para inspecionar e baixar o código-fonte completo:</p>
            <div class="dc-grid-2">
                <div class="dc-file-card" onclick="openDemosCicdDoc('cicd-local-review')">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="background:#dcfce7; color:#15803d; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:999px;">1. WARMUP LOCAL (SEM GITHUB)</span>
                        <code style="font-size:0.82rem; color:#0f172a; font-weight:700;">local_review.py</code>
                    </div>
                    <h4 style="margin:0 0 8px 0; color:#0f172a; font-size:1.15rem;">🏠 Simulador de Code Review no Terminal</h4>
                    <p style="margin:0 0 12px 0; font-size:0.86rem; color:#475569; line-height:1.5;">
                        Perfeito para testar o prompt de revisão antes de configurar o repositório. Contém um <code>SAMPLE_DIFF</code> embutido da classe <code>Checkout</code> (corrigindo <code>self.total</code> para <code>self.total()</code>) e imprime a revisão no terminal.
                    </p>
                    <ul style="margin:0; padding-left:18px; font-size:0.82rem; color:#334155; line-height:1.6;">
                        <li><strong>Dependência única:</strong> <code>ANTHROPIC_API_KEY</code> no ambiente.</li>
                        <li><strong>Comandos prontos:</strong> Instruções lado a lado para <strong>macOS</strong> e <strong>Windows PowerShell</strong>.</li>
                    </ul>
                </div>

                <div class="dc-file-card" style="border-left-color:#06b6d4;" onclick="openDemosCicdDoc('cicd-review-pr')">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="background:#e0f2fe; color:#0369a1; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:999px;">2. PRODUÇÃO NO GITHUB ACTIONS</span>
                        <code style="font-size:0.82rem; color:#0f172a; font-weight:700;">claude-review.yml + review_pr.py</code>
                    </div>
                    <h4 style="margin:0 0 8px 0; color:#0f172a; font-size:1.15rem;">🤖 Bot Automático de Pull Request</h4>
                    <p style="margin:0 0 12px 0; font-size:0.86rem; color:#475569; line-height:1.5;">
                        Combina o arquivo YAML do workflow com o script Python que roda dentro do container Ubuntu, capturando metadados reais do evento (<code>PR_NUMBER</code>, <code>PR_TITLE</code>, <code>PR_AUTHOR</code>, <code>BASE_SHA</code>, <code>HEAD_SHA</code>).
                    </p>
                    <ul style="margin:0; padding-left:18px; font-size:0.82rem; color:#334155; line-height:1.6;">
                        <li><strong>Zero servidor externo:</strong> Roda 100% nos runners gratuitos do GitHub Actions.</li>
                        <li><strong>Segurança de Contexto:</strong> Trunca diffs gigantes em 30.000 caracteres automaticamente.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 3. ANATOMIA DOS BUGS PLANTADOS & PYTHON SCRIPT VS CLAUDE-CODE-ACTION -->
        <div class="dc-grid-2" style="margin-bottom:24px;">
            <div class="dc-card" style="margin-bottom:0;">
                <h3 class="dc-title">🐛 Os 4 Bugs Plantados em <code>example-bug.py</code></h3>
                <p class="dc-sub">Ao copiar <code>example-bug.py</code> para uma branch de teste e abrir o PR, o bot do Claude identifica na hora:</p>
                <div class="dc-code-box">class Checkout:
    def apply_discount(self, percent: float) -> float:
        # BUG 1: chama self.total sem parênteses!
        # Multiplica um method object em vez do float (TypeError)
        return self.total * (1 - percent / 100)

    def discount_per_item(self, percent: float) -> float:
        # BUG 2: ZeroDivisionError se self.items estiver vazio []
        # BUG 3: sem validação para percent negativo ou > 100
        return (self.total() * percent / 100) / len(self.items)</div>
                <button onclick="openDemosCicdDoc('cicd-example-bug')" style="margin-top:14px; background:#f1f5f9; border:1px solid #cbd5e1; padding:8px 14px; border-radius:6px; font-weight:700; font-size:0.82rem; cursor:pointer; color:#0f172a;">🐛 Abrir example-bug.py Completo</button>
            </div>

            <div class="dc-card" style="margin-bottom:0;">
                <h3 class="dc-title">🔄 Script Python Direto vs <code>claude-code-action@v1</code></h3>
                <p class="dc-sub">Quando construir seu próprio script Python no runner vs usar a Action oficial da Anthropic:</p>
                <table class="dc-table">
                    <thead>
                        <tr>
                            <th>Critério</th>
                            <th>🐍 Script Python (<code>review_pr.py</code>)</th>
                            <th>⚡ Action Oficial (<code>claude-code-action@v1</code>)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Transparência</strong></td>
                            <td>100% explícito (você controla o <code>git diff</code>, o prompt e o <code>gh pr comment</code>)</td>
                            <td>Abstraído dentro da Action oficial</td>
                        </tr>
                        <tr>
                            <td><strong>Customização</strong></td>
                            <td>Fácil injetar regras internas, truncamento customizado ou chamar outras APIs</td>
                            <td>Configurado via parâmetros YAML (<code>prompt: "Revise este PR"</code>)</td>
                        </tr>
                        <tr>
                            <td><strong>Uso Recomendado</strong></td>
                            <td>Didática, controle fino de custos (Haiku) e fluxos customizados</td>
                            <td>Plug-and-play rápido em repositórios de produção</td>
                        </tr>
                    </tbody>
                </table>
                <button onclick="openDemosCicdDoc('cicd-workflow-yml')" style="margin-top:14px; background:#f1f5f9; border:1px solid #cbd5e1; padding:8px 14px; border-radius:6px; font-weight:700; font-size:0.82rem; cursor:pointer; color:#0f172a;">⚙️ Ver Workflow YAML Completo</button>
            </div>
        </div>

        <!-- 4. TROUBLESHOOTING DE CAMPO & 5 VARIAÇÕES PARA EXPANDIR -->
        <div class="dc-card">
            <h3 class="dc-title">🛠️ Troubleshooting Rápido & 5 Evoluções para Live Coding</h3>
            <p class="dc-sub">Principais armadilhas ao configurar bots no GitHub Actions e como destravá-las em segundos:</p>
            <table class="dc-table" style="margin-bottom:20px;">
                <thead>
                    <tr>
                        <th>Erro no GitHub Actions</th>
                        <th>Causa Raiz</th>
                        <th>Solução Imediata</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>Resource not accessible by integration</code></td>
                        <td>O token padrão não tem permissão de escrita no PR</td>
                        <td>Garanta <code>permissions: pull-requests: write</code> no <code>claude-review.yml</code></td>
                    </tr>
                    <tr>
                        <td><code>No such file or directory: review_pr.py</code></td>
                        <td>A branch do PR foi criada antes de subir a pasta <code>.github/</code> na <code>main</code></td>
                        <td>Clique em <strong>"Update branch"</strong> no PR ou crie a branch após o push da <code>main</code></td>
                    </tr>
                    <tr>
                        <td><code>ANTHROPIC_API_KEY not found</code></td>
                        <td>Secret ausente no repositório</td>
                        <td>Rode <code>gh secret set ANTHROPIC_API_KEY --body "sk-ant-..."</code></td>
                    </tr>
                </tbody>
            </table>

            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px 18px; font-size:0.88rem; color:#334155;">
                <strong>🚀 5 Variações Avançadas para Expandir na Aula (20 min extras):</strong>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(230px, 1fr)); gap:10px; margin-top:8px;">
                    <div>• <strong>Subagentes Paralelos:</strong> Dividir em 3 agentes simultâneos (Qualidade, Segurança e Performance).</div>
                    <div>• <strong>Auto-Fix Commit:</strong> Pedir ao Claude para aplicar o patch e dar <code>git push</code> na branch do PR.</div>
                    <div>• <strong>Trigger por Comentário:</strong> Disparar em <code>issue_comment</code> apenas quando alguém digitar <code>@claude review</code>.</div>
                    <div>• <strong>Filtro de Caminhos:</strong> Adicionar <code>paths: ['**.py']</code> no YAML para ignorar mudanças de docs.</div>
                    <div>• <strong>Execução Sob Demanda:</strong> Incluir <code>workflow_dispatch</code> para acionar revisão pelo botão da UI.</div>
                </div>
            </div>
        </div>
    `;

    // Populate Mode 2: Code & Docs Explorer
    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';

    docsWrapper.appendChild(sidebar);
    docsWrapper.appendChild(contentArea);

    const categories = Object.keys(demosCicdData);
    let firstDocItem = null;

    categories.forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #2563eb';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const linkList = document.createElement('div');
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        catHeader.onclick = () => {
            linkList.style.display = linkList.style.display === 'none' ? 'block' : 'none';
        };

        const docsList = demosCicdData[category];
        docsList.forEach(docItem => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.setAttribute('data-doc-id', docItem.id);
            btn.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">${docItem.icon || '📄'}</span>
                    <span style="font-weight:600; color:#323130; font-size:0.93rem;">${docItem.title}</span>
                </div>
                <div style="font-size:0.78rem; color:#605e5c; margin-top:4px; line-height:1.35; white-space:normal;">
                    ${docItem.description}
                </div>
            `;

            if (!firstDocItem) firstDocItem = { btn, docItem, category };

            btn.onclick = () => {
                document.querySelectorAll('#dc-docs-wrapper .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                contentArea.innerHTML = '<div style="padding:40px; text-align:center; color:#64748b;">⏳ Carregando arquivo...</div>';

                fetch(docItem.path + '?v=' + new Date().getTime())
                    .then(r => {
                        if (!r.ok) throw new Error('Arquivo não encontrado: ' + docItem.path);
                        return r.text();
                    })
                    .then(text => {
                        const isCodeFile = docItem.path.endsWith('.py') || docItem.path.endsWith('.yml') || docItem.path.endsWith('.txt');
                        let renderedBody = '';

                        if (isCodeFile) {
                            const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                            renderedBody = `<pre style="background:#0f172a; color:#f8fafc; padding:22px; border-radius:10px; overflow-x:auto; font-family:'Courier New', monospace; font-size:0.88rem; line-height:1.6; border-left:4px solid #2563eb;"><code>${escaped}</code></pre>`;
                        } else {
                            const preBlocks = [];
                            let processedText = text.replace(/```[a-zA-Z0-9_-]*\n([\s\S]*?)```/g, (match, p1) => {
                                const esc = p1.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                                preBlocks.push(esc);
                                return `__PRE_BLOCK_${preBlocks.length - 1}__`;
                            });

                            let html = processedText
                                .replace(/^### (.*$)/gim, '<h3 style="margin-top:28px; margin-bottom:12px; color:#1e293b; font-size:1.3rem;">$1</h3>')
                                .replace(/^## (.*$)/gim, '<h2 style="margin-top:36px; margin-bottom:16px; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:8px; font-size:1.6rem;">$1</h2>')
                                .replace(/^# (.*$)/gim, '<h1 style="margin-top:10px; margin-bottom:20px; color:#0f172a; font-size:2rem; font-weight:800;">$1</h1>')
                                .replace(/\*\*(.*?)\*\*/gim, '<strong style="color:#0f172a;">$1</strong>')
                                .replace(/\*(.*?)\*/gim, '<em>$1</em>')
                                .replace(/`([^`]+)`/gim, '<code style="background:#f1f5f9; padding:2px 6px; border-radius:4px; font-family:monospace; color:#2563eb; font-size:0.88em;">$1</code>')
                                .replace(/^\> (.*$)/gim, '<blockquote style="border-left:4px solid #2563eb; background:#eff6ff; padding:12px 16px; margin:14px 0; color:#1e3a8a; border-radius:0 6px 6px 0;">$1</blockquote>')
                                .replace(/^\- (.*$)/gim, '<li style="margin-left:20px; margin-bottom:6px; line-height:1.6; color:#334155;">$1</li>')
                                .replace(/\n\n/gim, '<br><br>');

                            html = html.replace(/__PRE_BLOCK_(\d+)__/g, (match, idx) => {
                                return `<pre style="background:#0f172a; color:#f8fafc; padding:16px; border-radius:8px; overflow-x:auto; margin:18px 0; font-family:monospace; font-size:0.88rem; line-height:1.5;"><code>${preBlocks[idx]}</code></pre>`;
                            });
                            renderedBody = html;
                        }

                        const fileName = docItem.path.split('/').pop();
                        const headerCard = `
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; margin-bottom: 28px;">
                                <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                                    <div>
                                        <span style="font-size:0.75rem; font-weight:800; color:#2563eb; text-transform:uppercase;">${category}</span>
                                        <h3 style="margin:4px 0 0 0; color:#0f172a; font-size:1.25rem;">${docItem.icon || '📄'} ${docItem.title}</h3>
                                    </div>
                                    <div style="display:flex; gap:10px; align-items:center;">
                                        ${window.favoritesManager ? window.favoritesManager.renderButton(docItem.id, docItem.title, 'Demos GitHub & CI/CD', docItem.path) : ''}
                                        <a href="${docItem.path}" download="${fileName}" style="background:#2563eb; color:#fff; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.85rem;">⬇️ Baixar ${fileName}</a>
                                        <a href="${docItem.path}" target="_blank" style="background:#fff; color:#334155; border:1px solid #cbd5e1; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.85rem;">👀 Abrir Raw</a>
                                    </div>
                                </div>
                                <p style="margin:0 0 12px 0; color:#475569; font-size:0.92rem;">${docItem.description}</p>
                                <div style="background:#f1f5f9; border:1px solid #cbd5e1; padding:6px 10px; border-radius:4px; font-family:monospace; font-size:0.8rem; color:#475569;">
                                    📂 <strong>Arquivo no Portal:</strong> ${docItem.path}
                                </div>
                            </div>
                        `;

                        contentArea.innerHTML = `
                            <div style="max-width: 920px; margin: 0 auto; padding: 24px 32px;">
                                ${headerCard}
                                <div style="color:#1e293b; line-height:1.7; font-size:1rem;">
                                    ${renderedBody}
                                </div>
                            </div>
                        `;
                    })
                    .catch(err => {
                        contentArea.innerHTML = `<div style="padding:40px; color:#ef4444;">Erro ao carregar arquivo: ${err.message}</div>`;
                    });
            };

            linkList.appendChild(btn);
        });
    });

    // Mode toggle buttons
    const btnGuide = hero.querySelector('#dc-btn-guide');
    const btnDocs = hero.querySelector('#dc-btn-docs');

    btnGuide.onclick = () => {
        btnGuide.classList.add('active');
        btnDocs.classList.remove('active');
        guideWrapper.style.display = 'block';
        docsWrapper.style.display = 'none';
    };

    btnDocs.onclick = () => {
        btnDocs.classList.add('active');
        btnGuide.classList.remove('active');
        guideWrapper.style.display = 'none';
        docsWrapper.style.display = 'flex';
        if (firstDocItem && !docsWrapper.querySelector('.kb-nav-btn.active')) {
            firstDocItem.btn.click();
        }
    };
}
