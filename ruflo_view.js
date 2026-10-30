document.addEventListener('DOMContentLoaded', () => {
    initRufloView();
});

function initRufloView() {
    const container = document.getElementById('ruflo-view');
    if (!container || typeof rufloData === 'undefined') return;

    container.innerHTML = '';

    // Inject styles for Ruflo view
    const styleId = 'ruflo-custom-styles';
    if (!document.getElementById(styleId)) {
        const style = document.createElement('style');
        style.id = styleId;
        style.textContent = `
            .ruflo-hero {
                background: linear-gradient(135deg, #092c4c 0%, #0f172a 60%, #1e1b4b 100%);
                border: 1px solid rgba(56, 189, 248, 0.25);
                border-radius: 16px;
                padding: 30px;
                margin-bottom: 24px;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
                position: relative;
                overflow: hidden;
            }
            .ruflo-hero::after {
                content: '';
                position: absolute;
                top: -50%;
                right: -20%;
                width: 400px;
                height: 400px;
                background: radial-gradient(circle, rgba(14, 165, 233, 0.15) 0%, transparent 70%);
                pointer-events: none;
            }
            .ruflo-hero-header {
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: 12px;
            }
            .ruflo-hero-icon {
                font-size: 38px;
                background: rgba(14, 165, 233, 0.15);
                border: 1px solid rgba(56, 189, 248, 0.3);
                width: 60px;
                height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 14px;
                box-shadow: 0 0 15px rgba(14, 165, 233, 0.3);
            }
            .ruflo-hero-title {
                margin: 0;
                font-size: 26px;
                font-weight: 800;
                color: #f8fafc;
                letter-spacing: -0.5px;
            }
            .ruflo-hero-badge {
                display: inline-block;
                background: rgba(14, 165, 233, 0.2);
                color: #38bdf8;
                border: 1px solid rgba(56, 189, 248, 0.4);
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-left: 8px;
                vertical-align: middle;
            }
            .ruflo-hero-desc {
                font-size: 15px;
                line-height: 1.6;
                color: #cbd5e1;
                margin: 0 0 18px 0;
                max-width: 950px;
            }
            .ruflo-pill-bar {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 18px;
            }
            .ruflo-pill {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
                color: #e2e8f0;
                text-decoration: none;
                transition: all 0.2s ease;
            }
            .ruflo-pill:hover {
                background: rgba(14, 165, 233, 0.2);
                border-color: #38bdf8;
                color: #fff;
                transform: translateY(-1px);
            }
            .ruflo-tabs-nav {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding-top: 16px;
            }
            .ruflo-tab-btn {
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #94a3b8;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }
            .ruflo-tab-btn:hover {
                background: rgba(255, 255, 255, 0.08);
                color: #f8fafc;
            }
            .ruflo-tab-btn.active {
                background: #0284c7;
                border-color: #38bdf8;
                color: #fff;
                box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4);
            }
            .ruflo-sidebar-search {
                margin-bottom: 14px;
                position: relative;
            }
            .ruflo-search-input {
                width: 100%;
                background: #fff;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 10px 14px 10px 34px;
                font-size: 13px;
                color: #0f172a;
                outline: none;
                transition: border-color 0.2s, box-shadow 0.2s;
                box-sizing: border-box;
            }
            .ruflo-search-input:focus {
                border-color: #0284c7;
                box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.15);
            }
            .ruflo-search-icon {
                position: absolute;
                left: 11px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 14px;
                color: #94a3b8;
                pointer-events: none;
            }
            .ruflo-cat-count {
                background: #e2e8f0;
                color: #475569;
                font-size: 11px;
                font-weight: 700;
                padding: 2px 7px;
                border-radius: 12px;
                margin-left: 6px;
            }
            .ruflo-code-container {
                position: relative;
                margin: 18px 0;
            }
            .ruflo-code-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: #0f172a;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                border-bottom: 1px solid #334155;
                font-family: monospace;
                font-size: 12px;
                color: #94a3b8;
            }
            .ruflo-copy-btn {
                background: #1e293b;
                border: 1px solid #475569;
                color: #cbd5e1;
                border-radius: 4px;
                padding: 3px 10px;
                font-size: 11px;
                cursor: pointer;
                transition: all 0.2s;
            }
            .ruflo-copy-btn:hover {
                background: #334155;
                color: #fff;
            }
            .ruflo-code-block {
                background: #0f172a;
                color: #e2e8f0;
                padding: 16px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                overflow-x: auto;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.5;
                margin: 0;
            }
            .ruflo-markdown-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 13.5px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                border-radius: 8px;
                overflow: hidden;
                border: 1px solid #e2e8f0;
            }
            .ruflo-markdown-table th {
                background: #f1f5f9;
                color: #0f172a;
                font-weight: 700;
                text-align: left;
                padding: 12px 14px;
                border-bottom: 2px solid #cbd5e1;
            }
            .ruflo-markdown-table td {
                padding: 10px 14px;
                border-bottom: 1px solid #e2e8f0;
                color: #334155;
                vertical-align: top;
            }
            .ruflo-markdown-table tr:nth-child(even) td {
                background: #f8fafc;
            }
            .ruflo-cheatsheet-card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            }
            .ruflo-cheatsheet-title {
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 18px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 12px;
            }
        `;
        document.head.appendChild(style);
    }

    // Hero Header Component
    const hero = document.createElement('div');
    hero.className = 'ruflo-hero';
    hero.innerHTML = `
        <div class="ruflo-hero-header">
            <div class="ruflo-hero-icon">🌊</div>
            <div>
                <h2 class="ruflo-hero-title">
                    Ruflo (Claude-Flow V3)
                    <span class="ruflo-hero-badge">Agent Meta-Harness</span>
                </h2>
                <div style="font-size:13px; color:#38bdf8; font-weight:600; margin-top:2px;">
                    Enterprise Multi-Agent Swarms · Self-Learning Vector Memory · 47 Plugins · 100+ Agentes
                </div>
            </div>
        </div>
        <p class="ruflo-hero-desc">
            O <strong>Ruflo</strong> é a camada de execução e harness meta-agêntico construído em torno do <strong>Claude Code</strong> e do <strong>OpenAI Codex</strong>. 
            Permite orquestrar swarms de múltiplos agentes especializados em topologias hierárquicas e em malha (mesh), equipados com memória vetorial persistente (AgentDB HNSW / RuVector), 
            metodologia SPARC, consenso tolerante a falhas (PBFT/Raft) e guardrails rígidos de governança corporativa.
        </p>
        <div class="ruflo-pill-bar">
            <a href="https://github.com/ruvnet/ruflo" target="_blank" class="ruflo-pill">
                ⭐ GitHub: ruvnet/ruflo
            </a>
            <span class="ruflo-pill" style="cursor:pointer;" onclick="navigator.clipboard.writeText('npx ruflo@latest init wizard'); alert('Comando copiado: npx ruflo@latest init wizard');">
                📦 npx ruflo@latest (Clique p/ copiar)
            </span>
            <span class="ruflo-pill">
                🧩 47 Plugins Oficiais
            </span>
            <span class="ruflo-pill">
                🤖 100+ Agentes Especializados
            </span>
            <span class="ruflo-pill">
                🐝 Topologias Swarm (Mesh / Hierarchical / V3)
            </span>
            <span class="ruflo-pill">
                🧠 RuVector ONNX + FlashAttention-3
            </span>
        </div>
        <div class="ruflo-tabs-nav" id="ruflo-tabs-filter">
            <button class="ruflo-tab-btn active" data-filter="all">🌟 Todos os Módulos (160)</button>
            <button class="ruflo-tab-btn" data-filter="guides">📖 Guias & Conceitos (6)</button>
            <button class="ruflo-tab-btn" data-filter="plugins">🧩 Catálogo de Plugins (47)</button>
            <button class="ruflo-tab-btn" data-filter="agents">🤖 Agentes Especializados (107)</button>
            <button class="ruflo-tab-btn" data-filter="cheatsheet" style="border-color:#38bdf8; color:#38bdf8;">⚡ Terminal & Receitas de Swarm</button>
        </div>
    `;
    container.appendChild(hero);

    // Layout
    const layout = document.createElement('div');
    layout.className = 'kb-layout';

    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.width = '320px';
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';

    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    container.appendChild(layout);

    // Add search bar inside sidebar
    const searchContainer = document.createElement('div');
    searchContainer.className = 'ruflo-sidebar-search';
    searchContainer.innerHTML = `
        <span class="ruflo-search-icon">🔍</span>
        <input type="text" class="ruflo-search-input" id="ruflo-search-box" placeholder="Buscar plugin, agente, doc...">
    `;
    sidebar.appendChild(searchContainer);

    const categoriesContainer = document.createElement('div');
    categoriesContainer.id = 'ruflo-categories-list';
    sidebar.appendChild(categoriesContainer);

    let activeFilter = 'all';
    let searchQuery = '';
    let firstSelectableBtn = null;

    function shouldIncludeCategory(categoryName) {
        if (activeFilter === 'all') return true;
        if (activeFilter === 'guides') return categoryName.includes('VISÃO GERAL') || categoryName.includes('GUIAS');
        if (activeFilter === 'plugins') return categoryName.startsWith('PLUGINS:');
        if (activeFilter === 'agents') return categoryName.startsWith('AGENTES:');
        return true;
    }

    function renderSidebar() {
        categoriesContainer.innerHTML = '';
        firstSelectableBtn = null;
        let totalRendered = 0;

        const categories = Object.keys(rufloData);

        categories.forEach(category => {
            if (!shouldIncludeCategory(category)) return;

            let items = rufloData[category];
            if (searchQuery.trim()) {
                const q = searchQuery.toLowerCase().trim();
                items = items.filter(it => 
                    it.title.toLowerCase().includes(q) || 
                    (it.description && it.description.toLowerCase().includes(q)) ||
                    it.id.toLowerCase().includes(q)
                );
            }

            if (items.length === 0) return;

            totalRendered += items.length;

            const catHeader = document.createElement('div');
            catHeader.className = 'kb-category-header';
            catHeader.style.padding = '10px 14px';
            catHeader.style.fontWeight = 'bold';
            catHeader.style.color = '#1e293b';
            catHeader.style.backgroundColor = '#f1f5f9';
            catHeader.style.borderLeft = category.startsWith('PLUGINS:') ? '4px solid #0284c7' : (category.startsWith('AGENTES:') ? '4px solid #8b5cf6' : '4px solid #10b981');
            catHeader.style.cursor = 'pointer';
            catHeader.style.marginTop = '12px';
            catHeader.style.marginBottom = '2px';
            catHeader.style.borderRadius = '0 6px 6px 0';
            catHeader.style.display = 'flex';
            catHeader.style.alignItems = 'center';
            catHeader.style.justifyContent = 'space-between';
            catHeader.innerHTML = `
                <span style="font-size:0.85rem; letter-spacing:0.3px;">${category}</span>
                <span class="ruflo-cat-count">${items.length}</span>
            `;

            const linkList = document.createElement('div');
            linkList.style.display = 'block';

            catHeader.onclick = () => {
                linkList.style.display = linkList.style.display === 'none' ? 'block' : 'none';
            };

            items.forEach(skill => {
                const btn = document.createElement('div');
                btn.className = 'kb-nav-btn';
                btn.style.padding = '9px 12px';
                btn.style.marginBottom = '4px';
                btn.innerHTML = `
                    <div style="display:flex; align-items:flex-start; gap:8px;">
                        <span style="font-size:1.1rem; flex-shrink:0; margin-top:1px;">${skill.icon || '🧩'}</span>
                        <div style="min-width:0; flex:1;">
                            <div style="font-weight:600; color:#323130; font-size:0.9rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${skill.title}</div>
                            <div style="font-size:0.78rem; color:#64748b; margin-top:2px; line-height:1.25; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                                ${skill.description || 'Documentação oficial do componente Ruflo.'}
                            </div>
                        </div>
                    </div>
                `;

                btn.onclick = () => {
                    document.querySelectorAll('#ruflo-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    loadItemContent(skill, category);
                };

                linkList.appendChild(btn);

                if (!firstSelectableBtn) {
                    firstSelectableBtn = { btn, skill, category };
                }
            });

            categoriesContainer.appendChild(catHeader);
            categoriesContainer.appendChild(linkList);
        });

        if (totalRendered === 0) {
            categoriesContainer.innerHTML = `
                <div style="padding:30px 15px; text-align:center; color:#94a3b8; font-size:13px;">
                    Nenhum resultado encontrado para "<strong>${searchQuery}</strong>".
                </div>
            `;
        }
    }

    // Resolve relative URLs in markdown for images
    function resolveRelativePath(url, docPath) {
        if (!url) return url;
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:') || url.startsWith('/')) {
            return url;
        }
        url = url.replace(/^\.\//, '');
        const lastSlash = docPath.lastIndexOf('/');
        const dir = lastSlash !== -1 ? docPath.substring(0, lastSlash) : '';
        return dir ? `${dir}/${url}` : url;
    }

    // Markdown Parser
    function parseMarkdown(text, docPath) {
        // Strip frontmatter
        text = text.replace(/^---[\s\S]*?---\s*/, '');

        // Extract code blocks first to protect them
        const codeBlocks = [];
        text = text.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
            codeBlocks.push({ lang: lang || 'bash', code: code.trim() });
            return `__RUFLO_CODE_BLOCK_${codeBlocks.length - 1}__`;
        });

        // Resolve Markdown Images: ![alt](url)
        text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (match, alt, url) => {
            const resolvedUrl = resolveRelativePath(url.trim(), docPath);
            return `<div style="text-align:center; margin:24px 0;"><img src="${resolvedUrl}" alt="${alt}" style="max-width:100%; height:auto; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.1); border:1px solid #e2e8f0;"><div style="font-size:12px; color:#64748b; margin-top:6px; font-style:italic;">${alt}</div></div>`;
        });

        // Resolve HTML Images: <img ... src="..." ...>
        text = text.replace(/<img([^>]+)src=["']([^"']+)["']([^>]*)>/gi, (match, before, src, after) => {
            const resolvedSrc = resolveRelativePath(src.trim(), docPath);
            return `<img${before}src="${resolvedSrc}"${after} style="max-width:100%; height:auto; border-radius:8px;">`;
        });

        // Headings
        text = text.replace(/^#### (.*$)/gim, '<h4 style="margin-top:24px; margin-bottom:10px; color:#1e293b; font-size:1.15rem; font-weight:700;">$1</h4>');
        text = text.replace(/^### (.*$)/gim, '<h3 style="margin-top:28px; margin-bottom:12px; color:#0f172a; font-size:1.35rem; font-weight:700;">$1</h3>');
        text = text.replace(/^## (.*$)/gim, '<h2 style="margin-top:36px; margin-bottom:16px; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:8px; font-size:1.65rem; font-weight:800;">$1</h2>');
        text = text.replace(/^# (.*$)/gim, '<h1 style="color:#0f172a; font-size:2rem; margin-bottom:20px; font-weight:800; border-bottom:2px solid #0284c7; padding-bottom:10px;">$1</h1>');

        // Bold & Italic
        text = text.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');

        // Inline Code
        text = text.replace(/`([^`]+)`/g, '<code style="background:#f1f5f9; color:#0284c7; padding:2px 6px; border-radius:4px; font-family:monospace; font-size:0.9em; border:1px solid #e2e8f0;">$1</code>');

        // Links
        text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" style="color:#0284c7; text-decoration:none; font-weight:600; border-bottom:1px dotted #0284c7;">$1 ↗</a>');

        // Blockquotes
        text = text.replace(/^\> (.*$)/gim, '<blockquote style="background:#f0f9ff; border-left:4px solid #0284c7; padding:12px 18px; color:#0369a1; margin:16px 0; border-radius:0 8px 8px 0; font-size:0.95rem; line-height:1.6;">$1</blockquote>');

        // Tables (detect markdown table lines)
        const lines = text.split('\n');
        const processedLines = [];
        let inTable = false;
        let tableRows = [];

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            if (line.startsWith('|') && line.endsWith('|')) {
                inTable = true;
                tableRows.push(line);
            } else {
                if (inTable) {
                    processedLines.push(renderMarkdownTable(tableRows));
                    tableRows = [];
                    inTable = false;
                }
                processedLines.push(lines[i]);
            }
        }
        if (inTable && tableRows.length > 0) {
            processedLines.push(renderMarkdownTable(tableRows));
        }
        text = processedLines.join('\n');

        // Unordered lists
        text = text.replace(/^- (.*$)/gim, '<li style="margin-left:20px; margin-bottom:6px; color:#334155;">$1</li>');
        text = text.replace(/^\* (.*$)/gim, '<li style="margin-left:20px; margin-bottom:6px; color:#334155;">$1</li>');

        // Paragraphs
        text = text.replace(/\n\n/g, '</p><p style="margin-bottom:16px; color:#334155; line-height:1.7;">');

        // Restore Code Blocks
        codeBlocks.forEach((item, idx) => {
            const escapedCode = item.code.replace(/</g, '&lt;').replace(/>/g, '&gt;');
            const snippet = `
                <div class="ruflo-code-container">
                    <div class="ruflo-code-header">
                        <span>${item.lang || 'bash'}</span>
                        <button class="ruflo-copy-btn" onclick="copyRufloSnippet(this)">Copiar</button>
                    </div>
                    <pre class="ruflo-code-block"><code>${escapedCode}</code></pre>
                </div>
            `;
            text = text.replace(`__RUFLO_CODE_BLOCK_${idx}__`, snippet);
        });

        return text;
    }

    function renderMarkdownTable(rows) {
        if (rows.length < 2) return rows.join('\n');
        let html = '<table class="ruflo-markdown-table"><thead><tr>';
        
        // Header
        const headers = rows[0].split('|').slice(1, -1).map(c => c.trim());
        headers.forEach(h => {
            html += `<th>${h}</th>`;
        });
        html += '</tr></thead><tbody>';

        // Skip row 1 (separator)
        for (let i = 2; i < rows.length; i++) {
            const cells = rows[i].split('|').slice(1, -1).map(c => c.trim());
            html += '<tr>';
            cells.forEach(c => {
                html += `<td>${c}</td>`;
            });
            html += '</tr>';
        }
        html += 'tbody></table>';
        return html;
    }

    function loadItemContent(skill, category) {
        contentArea.innerHTML = `
            <div style="padding:60px; text-align:center; color:#0284c7;">
                <div style="font-size:24px; margin-bottom:10px;">⏳</div>
                <div style="font-weight:600; font-size:16px;">Carregando ${skill.title}...</div>
            </div>
        `;

        const loadPromise = (typeof skill.content === 'string')
            ? Promise.resolve(skill.content)
            : fetch(skill.path + '?v=' + new Date().getTime()).then(res => {
                if (!res.ok) throw new Error(`Não foi possível carregar o arquivo (${res.status})`);
                return res.text();
            });

        loadPromise
            .then(rawText => {
                const htmlContent = parseMarkdown(rawText, skill.path);

                // Contextual badges & instructions
                let howToUseCommand = '';
                if (category.startsWith('PLUGINS:')) {
                    howToUseCommand = `/plugin install ${skill.id}@ruflo`;
                } else if (category.startsWith('AGENTES:')) {
                    const agentName = skill.id.replace('agent-', '');
                    howToUseCommand = `npx ruflo agent spawn --type ${agentName} --name ${agentName}-worker`;
                } else {
                    howToUseCommand = `npx ruflo --help`;
                }

                const headerCard = `
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:24px; margin-bottom:28px; box-shadow:0 2px 5px rgba(0,0,0,0.03);">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:16px;">
                            <div>
                                <span style="display:inline-block; font-size:11px; font-weight:800; background:#e0f2fe; color:#0369a1; padding:3px 10px; border-radius:12px; margin-bottom:6px; letter-spacing:0.5px;">
                                    ${category}
                                </span>
                                <h2 style="margin:0; font-size:1.6rem; color:#0f172a; display:flex; align-items:center; gap:8px;">
                                    <span>${skill.icon || '🧩'}</span> ${skill.title}
                                </h2>
                            </div>
                            <div>
                                ${window.favoritesManager ? window.favoritesManager.renderButton(skill.id, skill.title, 'Ruflo', skill.path) : ''}
                            </div>
                        </div>

                        <div style="background:#f1f5f9; border:1px solid #cbd5e1; padding:10px 14px; border-radius:6px; font-family:monospace; font-size:0.85rem; color:#475569; display:flex; align-items:center; justify-content:space-between; margin-bottom:18px;">
                            <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">📂 <strong>Arquivo:</strong> ${skill.path}</span>
                            <button onclick="navigator.clipboard.writeText('${skill.path}'); alert('Caminho copiado!');" style="background:#e2e8f0; border:none; padding:3px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copiar</button>
                        </div>

                        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;">
                            <a href="${skill.path}" download="${skill.id}.md" style="background:#0284c7; color:#fff; padding:9px 18px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.9rem; box-shadow:0 2px 4px rgba(2, 132, 199, 0.3); display:inline-flex; align-items:center; gap:6px;">
                                ⬇️ Baixar Arquivo
                            </a>
                            <a href="${skill.path}" target="_blank" style="background:#fff; color:#334155; padding:9px 18px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.9rem; border:1px solid #cbd5e1; display:inline-flex; align-items:center; gap:6px;">
                                👀 Abrir no Navegador
                            </a>
                            <a href="https://github.com/ruvnet/ruflo" target="_blank" style="background:#fff; color:#334155; padding:9px 18px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.9rem; border:1px solid #cbd5e1; display:inline-flex; align-items:center; gap:6px;">
                                🔗 Repositório GitHub
                            </a>
                        </div>

                        <div style="border-top:1px solid #e2e8f0; padding-top:16px;">
                            <h4 style="margin:0 0 6px 0; color:#0f172a; font-size:0.95rem; display:flex; align-items:center; gap:6px;">
                                <span>🧠</span> Visão Geral & Finalidade
                            </h4>
                            <p style="margin:0 0 12px 0; color:#475569; font-size:0.95rem; line-height:1.5;">
                                ${skill.description || 'Documentação oficial e especificações técnicas de integração com o ecossistema Ruflo.'}
                            </p>

                            <h4 style="margin:14px 0 6px 0; color:#0f172a; font-size:0.95rem; display:flex; align-items:center; gap:6px;">
                                <span>🛠️</span> Execução Rápida
                            </h4>
                            <div style="background:#0f172a; color:#38bdf8; font-family:monospace; padding:10px 14px; border-radius:6px; font-size:12.5px; display:flex; align-items:center; justify-content:space-between;">
                                <span>${howToUseCommand}</span>
                                <button onclick="navigator.clipboard.writeText('${howToUseCommand}'); alert('Comando copiado!');" style="background:#1e293b; color:#cbd5e1; border:1px solid #475569; padding:3px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copiar</button>
                            </div>
                        </div>
                    </div>
                `;

                contentArea.innerHTML = `
                    <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                        ${headerCard}
                        <div class="ruflo-doc-content" style="max-width:980px; margin:0 auto; line-height:1.75; font-size:1.05rem;">
                            ${htmlContent}
                        </div>
                    </div>
                `;
                if (container.classList.contains('active') && window.scrollPortalToTop) {
                    window.scrollPortalToTop(true);
                }
            })
            .catch(err => {
                contentArea.innerHTML = `
                    <div style="padding:40px; text-align:center; color:#ef4444;">
                        <h3>Erro ao carregar o arquivo</h3>
                        <p>${err.message}</p>
                        <p style="font-size:12px; color:#64748b;">Verifique se o arquivo existe em <code>${skill.path}</code>.</p>
                    </div>
                `;
            });
    }

    function renderCheatsheetDashboard() {
        document.querySelectorAll('#ruflo-view .kb-nav-btn').forEach(b => b.classList.remove('active'));

        contentArea.innerHTML = `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>⚡</span> Ruflo Terminal & Swarm Cheat Sheet
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Guia de comandos rápidos, snippets copy-paste e receitas de orquestração prontas para Claude Code e Codex.
                    </p>
                </div>

                <!-- Card 1: Instalação Claude Code -->
                <div class="ruflo-cheatsheet-card">
                    <div class="ruflo-cheatsheet-title">
                        <span>💻</span> 1. Instalação no Claude Code (Plugin Marketplace)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Execute estes comandos dentro do Claude Code (versão 2.1.287 ou superior) para habilitar o Ruflo, o console interativo e os guardrails:
                    </p>
                    <div class="ruflo-code-container">
                        <div class="ruflo-code-header">
                            <span>Claude Code Shell</span>
                            <button class="ruflo-copy-btn" onclick="copyRufloSnippet(this)">Copiar Bloco</button>
                        </div>
                        <pre class="ruflo-code-block"><code>/plugin marketplace add ruvnet/ruflo
/plugin install ruflo-core@ruflo
/plugin install ruflo-console@ruflo
/plugin install ruflo-mods@ruflo
/reload-plugins
/ruflo</code></pre>
                    </div>
                </div>

                <!-- Card 2: Instalação Codex & MCP -->
                <div class="ruflo-cheatsheet-card">
                    <div class="ruflo-cheatsheet-title">
                        <span>⚙️</span> 2. Inicialização do Servidor MCP & Setup Wizard
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Para uso com OpenAI Codex, Cursor ou qualquer cliente MCP:
                    </p>
                    <div class="ruflo-code-container">
                        <div class="ruflo-code-header">
                            <span>Terminal / Bash</span>
                            <button class="ruflo-copy-btn" onclick="copyRufloSnippet(this)">Copiar</button>
                        </div>
                        <pre class="ruflo-code-block"><code># Assistente interativo de configuração
npx ruflo@latest init wizard

# Iniciar servidor MCP local (stdio)
npx -y ruflo@latest mcp start

# Abrir Terminal UI (TUI) standalone
npx ruflo tui</code></pre>
                    </div>
                </div>

                <!-- Card 3: Receita 5-Agent Swarm -->
                <div class="ruflo-cheatsheet-card">
                    <div class="ruflo-cheatsheet-title">
                        <span>🐝</span> 3. Receita: Swarm de Desenvolvimento (5 Agentes Coordenados)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Inicializa topologia hierárquica e spawna Coordinator, Coders, Tester e Reviewer:
                    </p>
                    <div class="ruflo-code-container">
                        <div class="ruflo-code-header">
                            <span>Terminal / Bash</span>
                            <button class="ruflo-copy-btn" onclick="copyRufloSnippet(this)">Copiar Bloco</button>
                        </div>
                        <pre class="ruflo-code-block"><code>npx ruflo swarm init --topology hierarchical --max-agents 8
npx ruflo agent spawn --type coordinator --name coord-lead
npx ruflo agent spawn --type coder --name coder-backend
npx ruflo agent spawn --type coder --name coder-frontend
npx ruflo agent spawn --type tester --name qa-tester
npx ruflo agent spawn --type reviewer --name code-reviewer
npx ruflo swarm start --objective "Implementar autenticação JWT e rotas protegidas" --strategy development</code></pre>
                    </div>
                </div>

                <!-- Card 4: Memória Vetorial & RAG -->
                <div class="ruflo-cheatsheet-card">
                    <div class="ruflo-cheatsheet-title">
                        <span>💾</span> 4. Comandos de Memória Vetorial & Aprendizado Contínuo
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Pesquise experiências anteriores antes de iniciar e registre padrões de sucesso após concluir:
                    </p>
                    <div class="ruflo-code-container">
                        <div class="ruflo-code-header">
                            <span>Terminal / Bash</span>
                            <button class="ruflo-copy-btn" onclick="copyRufloSnippet(this)">Copiar</button>
                        </div>
                        <pre class="ruflo-code-block"><code># 1. Buscar padrões passados relevantes
npx ruflo memory search --query "auth security jwt tokens"

# 2. Armazenar padrão bem-sucedido no AgentDB
npx ruflo memory store --key "jwt-refresh-flow" --value "Utilizado refresh token em cookie httpOnly com CSRF double submit" --namespace patterns

# 3. Listar memórias salvas
npx ruflo memory list --namespace patterns</code></pre>
                    </div>
                </div>

                <!-- Card 5: Divisão de Responsabilidades -->
                <div class="ruflo-cheatsheet-card" style="background:#eff6ff; border-color:#bfdbfe;">
                    <div class="ruflo-cheatsheet-title" style="color:#1d4ed8;">
                        <span>🚨</span> 5. Regra Fundamental de Divisão de Trabalho
                    </div>
                    <p style="color:#1e40af; font-size:14.5px; line-height:1.6; margin:0;">
                        <strong>Ruflo = Ledger & Coordenação</strong> (rastreia estado, gerencia memória, emite eventos).<br>
                        <strong>Codex / Claude Code = Executor</strong> (escreve código, roda testes, edita arquivos).<br><br>
                        <em>Nunca pare a execução após rodar um comando do Ruflo esperando que ele faça o código por você: o Ruflo cria o registro instantaneamente, e o Claude/Codex deve continuar imediatamente com a implementação!</em>
                    </p>
                </div>
            </div>
        `;
    }

    // Copy helper
    window.copyRufloSnippet = function(btn) {
        const pre = btn.parentElement.nextElementSibling;
        if (!pre) return;
        const code = pre.textContent;
        navigator.clipboard.writeText(code).then(() => {
            const originalText = btn.textContent;
            btn.textContent = '✓ Copiado!';
            btn.style.backgroundColor = '#10b981';
            btn.style.color = '#fff';
            btn.style.borderColor = '#10b981';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.backgroundColor = '';
                btn.style.color = '';
                btn.style.borderColor = '';
            }, 2000);
        });
    };

    // Filter Buttons
    const filterButtons = hero.querySelectorAll('.ruflo-tab-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeFilter = btn.getAttribute('data-filter');

            if (activeFilter === 'cheatsheet') {
                renderCheatsheetDashboard();
            } else {
                renderSidebar();
                if (firstSelectableBtn) {
                    firstSelectableBtn.btn.click();
                }
            }
        });
    });

    // Search Input Event
    const searchBox = searchContainer.querySelector('#ruflo-search-box');
    searchBox.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        renderSidebar();
    });

    // Initial render
    renderSidebar();

    if (firstSelectableBtn) {
        firstSelectableBtn.btn.click();
    }

    window.renderRufloView = function(viewId) {
        if (viewId === 'ruflo-view' && !container.innerHTML) {
            initRufloView();
        }
    };
}

window.initRufloView = initRufloView;
