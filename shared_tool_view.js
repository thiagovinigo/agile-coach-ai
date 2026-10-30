// Universal Shared Layout Engine for Tools & Knowledge Base in Agile Coach AI Portal

window.copyToolCodeSnippet = function(btn) {
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

function resolveToolRelativePath(url, docPath) {
    if (!url) return url;
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:') || url.startsWith('/')) {
        return url;
    }
    url = url.replace(/^\.\//, '');
    const lastSlash = docPath.lastIndexOf('/');
    const dir = lastSlash !== -1 ? docPath.substring(0, lastSlash) : '';
    return dir ? `${dir}/${url}` : url;
}

function renderToolMarkdownTable(rows) {
    if (rows.length < 2) return rows.join('\n');
    let html = '<table class="tool-markdown-table"><thead><tr>';
    const headers = rows[0].split('|').slice(1, -1).map(c => c.trim());
    headers.forEach(h => {
        html += `<th>${h}</th>`;
    });
    html += '</tr></thead><tbody>';

    for (let i = 2; i < rows.length; i++) {
        const cells = rows[i].split('|').slice(1, -1).map(c => c.trim());
        html += '<tr>';
        cells.forEach(c => {
            html += `<td>${c}</td>`;
        });
        html += '</tr>';
    }
    html += '</tbody></table>';
    return html;
}

function parseToolMarkdown(text, docPath, themeColor) {
    text = text.replace(/^---[\s\S]*?---\s*/, '');

    const codeBlocks = [];
    text = text.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
        codeBlocks.push({ lang: lang || 'bash', code: code.trim() });
        return `__TOOL_CODE_BLOCK_${codeBlocks.length - 1}__`;
    });

    text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (match, alt, url) => {
        const resolvedUrl = resolveToolRelativePath(url.trim(), docPath);
        return `<div style="text-align:center; margin:24px 0;"><img src="${resolvedUrl}" alt="${alt}" style="max-width:100%; height:auto; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.1); border:1px solid #e2e8f0;"><div style="font-size:12px; color:#64748b; margin-top:6px; font-style:italic;">${alt}</div></div>`;
    });

    text = text.replace(/<img([^>]+)src=["']([^"']+)["']([^>]*)>/gi, (match, before, src, after) => {
        const resolvedSrc = resolveToolRelativePath(src.trim(), docPath);
        return `<img${before}src="${resolvedSrc}"${after} style="max-width:100%; height:auto; border-radius:8px;">`;
    });

    text = text.replace(/^#### (.*$)/gim, '<h4 style="margin-top:24px; margin-bottom:10px; color:#1e293b; font-size:1.15rem; font-weight:700;">$1</h4>');
    text = text.replace(/^### (.*$)/gim, '<h3 style="margin-top:28px; margin-bottom:12px; color:#0f172a; font-size:1.35rem; font-weight:700;">$1</h3>');
    text = text.replace(/^## (.*$)/gim, '<h2 style="margin-top:36px; margin-bottom:16px; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:8px; font-size:1.65rem; font-weight:800;">$1</h2>');
    text = text.replace(/^# (.*$)/gim, `<h1 style="color:#0f172a; font-size:2rem; margin-bottom:20px; font-weight:800; border-bottom:2px solid ${themeColor || '#0284c7'}; padding-bottom:10px;">$1</h1>`);

    text = text.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');

    text = text.replace(/`([^`]+)`/g, `<code style="background:#f1f5f9; color:${themeColor || '#0284c7'}; padding:2px 6px; border-radius:4px; font-family:monospace; font-size:0.9em; border:1px solid #e2e8f0;">$1</code>`);

    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, `<a href="$2" target="_blank" style="color:${themeColor || '#0284c7'}; text-decoration:none; font-weight:600; border-bottom:1px dotted ${themeColor || '#0284c7'};">$1 ↗</a>`);

    text = text.replace(/^\> (.*$)/gim, `<blockquote style="background:#f8fafc; border-left:4px solid ${themeColor || '#0284c7'}; padding:12px 18px; color:#334155; margin:16px 0; border-radius:0 8px 8px 0; font-size:0.95rem; line-height:1.6;">$1</blockquote>`);

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
                processedLines.push(renderToolMarkdownTable(tableRows));
                tableRows = [];
                inTable = false;
            }
            processedLines.push(lines[i]);
        }
    }
    if (inTable && tableRows.length > 0) {
        processedLines.push(renderToolMarkdownTable(tableRows));
    }
    text = processedLines.join('\n');

    text = text.replace(/^- (.*$)/gim, '<li style="margin-left:20px; margin-bottom:6px; color:#334155;">$1</li>');
    text = text.replace(/^\* (.*$)/gim, '<li style="margin-left:20px; margin-bottom:6px; color:#334155;">$1</li>');

    text = text.replace(/\n\n/g, '</p><p style="margin-bottom:16px; color:#334155; line-height:1.7;">');

    codeBlocks.forEach((item, idx) => {
        const escapedCode = item.code.replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const snippet = `
            <div class="tool-code-container">
                <div class="tool-code-header">
                    <span>${item.lang || 'bash'}</span>
                    <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                </div>
                <pre class="tool-code-block"><code>${escapedCode}</code></pre>
            </div>
        `;
        text = text.replace(`__TOOL_CODE_BLOCK_${idx}__`, snippet);
    });

    return text;
}

window.createStandardToolView = function(config) {
    const container = document.getElementById(config.containerId);
    if (!container) return;

    // Normalizing data structure into categories dictionary
    let normalizedData = {};
    if (Array.isArray(config.data)) {
        normalizedData['TODOS'] = config.data;
    } else if (config.data && typeof config.data === 'object') {
        normalizedData = config.data;
    } else {
        return;
    }

    container.innerHTML = '';

    const themeColor = config.themeColor || '#0284c7';
    const themeGradient = config.themeGradient || 'linear-gradient(135deg, #092c4c 0%, #0f172a 60%, #1e1b4b 100%)';

    // Hero Header Component
    const hero = document.createElement('div');
    hero.className = 'tool-hero';
    hero.style.background = themeGradient;
    hero.style.border = `1px solid ${themeColor}40`;

    let pillsHtml = '';
    if (config.pills && Array.isArray(config.pills)) {
        config.pills.forEach(p => {
            if (p.link) {
                pillsHtml += `<a href="${p.link}" target="_blank" class="tool-pill">${p.text}</a>`;
            } else if (p.copyText) {
                pillsHtml += `<span class="tool-pill" style="cursor:pointer;" onclick="navigator.clipboard.writeText('${p.copyText}'); alert('Comando copiado: ${p.copyText}');">${p.text}</span>`;
            } else {
                pillsHtml += `<span class="tool-pill">${p.text}</span>`;
            }
        });
    }

    let tabsHtml = '';
    if (config.tabs && Array.isArray(config.tabs)) {
        config.tabs.forEach((t, idx) => {
            const activeClass = idx === 0 ? 'active' : '';
            const activeStyle = idx === 0 ? `background:${themeColor}; border-color:${themeColor}; color:#fff;` : '';
            tabsHtml += `<button class="tool-tab-btn ${activeClass}" data-filter="${t.id}" style="${activeStyle}">${t.label}</button>`;
        });
    }

    hero.innerHTML = `
        <div class="tool-hero-header">
            <div class="tool-hero-icon" style="background:${themeColor}20; border:1px solid ${themeColor}60; box-shadow:0 0 15px ${themeColor}40;">
                ${config.icon || '🚀'}
            </div>
            <div>
                <h2 class="tool-hero-title">
                    ${config.title}
                    ${config.badge ? `<span class="tool-hero-badge" style="background:${themeColor}25; color:${themeColor}; border:1px solid ${themeColor}60;">${config.badge}</span>` : ''}
                </h2>
                ${config.tagline ? `<div style="font-size:13px; color:#e2e8f0; font-weight:600; margin-top:2px;">${config.tagline}</div>` : ''}
            </div>
        </div>
        <p class="tool-hero-desc">
            ${config.description || ''}
        </p>
        ${pillsHtml ? `<div class="tool-pill-bar">${pillsHtml}</div>` : ''}
        ${tabsHtml ? `<div class="tool-tabs-nav" id="${config.containerId}-tabs">${tabsHtml}</div>` : ''}
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

    // Search bar inside sidebar
    const searchContainer = document.createElement('div');
    searchContainer.className = 'tool-sidebar-search';
    searchContainer.innerHTML = `
        <span class="tool-search-icon">🔍</span>
        <input type="text" class="tool-search-input" id="${config.containerId}-search" placeholder="Buscar no catálogo...">
    `;
    sidebar.appendChild(searchContainer);

    const categoriesContainer = document.createElement('div');
    categoriesContainer.id = `${config.containerId}-categories-list`;
    sidebar.appendChild(categoriesContainer);

    let activeFilter = config.tabs && config.tabs[0] ? config.tabs[0].id : 'all';
    let searchQuery = '';
    let firstSelectableBtn = null;

    function renderSidebar() {
        categoriesContainer.innerHTML = '';
        firstSelectableBtn = null;
        let totalRendered = 0;

        const categories = Object.keys(normalizedData);

        categories.forEach(category => {
            if (activeFilter !== 'all' && activeFilter !== 'cheatsheet') {
                if (category.toLowerCase() !== activeFilter.toLowerCase() && !category.toLowerCase().includes(activeFilter.toLowerCase())) {
                    return;
                }
            }

            let items = normalizedData[category] || [];
            if (searchQuery.trim()) {
                const q = searchQuery.toLowerCase().trim();
                items = items.filter(it => 
                    (it.title && it.title.toLowerCase().includes(q)) || 
                    (it.description && it.description.toLowerCase().includes(q)) ||
                    (it.id && it.id.toLowerCase().includes(q))
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
            catHeader.style.borderLeft = `4px solid ${themeColor}`;
            catHeader.style.cursor = 'pointer';
            catHeader.style.marginTop = '12px';
            catHeader.style.marginBottom = '2px';
            catHeader.style.borderRadius = '0 6px 6px 0';
            catHeader.style.display = 'flex';
            catHeader.style.alignItems = 'center';
            catHeader.style.justifyContent = 'space-between';
            catHeader.innerHTML = `
                <span style="font-size:0.85rem; letter-spacing:0.3px;">${category}</span>
                <span class="tool-cat-count">${items.length}</span>
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
                        <span style="font-size:1.1rem; flex-shrink:0; margin-top:1px;">${skill.icon || config.icon || '📌'}</span>
                        <div style="min-width:0; flex:1;">
                            <div style="font-weight:600; color:#323130; font-size:0.9rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${skill.title}</div>
                            <div style="font-size:0.78rem; color:#64748b; margin-top:2px; line-height:1.25; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                                ${skill.description || 'Documentação detalhada e diretrizes de uso.'}
                            </div>
                        </div>
                    </div>
                `;

                btn.onclick = () => {
                    document.querySelectorAll(`#${config.containerId} .kb-nav-btn`).forEach(b => b.classList.remove('active'));
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

    function loadItemContent(skill, category) {
        contentArea.innerHTML = `
            <div style="padding:60px; text-align:center; color:${themeColor};">
                <div style="font-size:24px; margin-bottom:10px;">⏳</div>
                <div style="font-weight:600; font-size:16px;">Carregando ${skill.title}...</div>
            </div>
        `;

        if (!skill.path) {
            // Render card without external file
            renderInlineCard(skill, category, '');
            return;
        }

        const loadPromise = (typeof skill.content === 'string')
            ? Promise.resolve(skill.content)
            : fetch(skill.path + '?v=' + new Date().getTime()).then(res => {
                if (!res.ok) throw new Error(`Arquivo não encontrado (${res.status})`);
                return res.text();
            });

        loadPromise
            .then(rawText => {
                const htmlContent = parseToolMarkdown(rawText, skill.path, themeColor);
                renderInlineCard(skill, category, htmlContent);
            })
            .catch(err => {
                contentArea.innerHTML = `
                    <div style="padding:40px; text-align:center; color:#ef4444;">
                        <h3>Erro ao carregar o arquivo</h3>
                        <p>${err.message}</p>
                        <p style="font-size:12px; color:#64748b;">Arquivo: <code>${skill.path}</code></p>
                    </div>
                `;
            });
    }

    function renderInlineCard(skill, category, htmlContent) {
        let howToUseCommand = config.commandPrefix ? `${config.commandPrefix} ${skill.id}` : (skill.triggers && skill.triggers[0] ? skill.triggers[0] : `Aja seguindo as instruções de ${skill.title}`);

        const headerCard = `
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:24px; margin-bottom:28px; box-shadow:0 2px 5px rgba(0,0,0,0.03);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:16px;">
                    <div>
                        <span style="display:inline-block; font-size:11px; font-weight:800; background:${themeColor}15; color:${themeColor}; padding:3px 10px; border-radius:12px; margin-bottom:6px; letter-spacing:0.5px;">
                            ${category}
                        </span>
                        <h2 style="margin:0; font-size:1.6rem; color:#0f172a; display:flex; align-items:center; gap:8px;">
                            <span>${skill.icon || config.icon || '📌'}</span> ${skill.title}
                        </h2>
                    </div>
                    <div>
                        ${window.favoritesManager ? window.favoritesManager.renderButton(skill.id, skill.title, config.itemType || config.title, skill.path || '') : ''}
                    </div>
                </div>

                ${skill.path ? `
                <div style="background:#f1f5f9; border:1px solid #cbd5e1; padding:10px 14px; border-radius:6px; font-family:monospace; font-size:0.85rem; color:#475569; display:flex; align-items:center; justify-content:space-between; margin-bottom:18px;">
                    <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">📂 <strong>Arquivo:</strong> ${skill.path}</span>
                    <button onclick="navigator.clipboard.writeText('${skill.path}'); alert('Caminho copiado!');" style="background:#e2e8f0; border:none; padding:3px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copiar</button>
                </div>
                ` : ''}

                <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;">
                    ${skill.path ? `
                    <a href="${skill.path}" download="${skill.id}.md" style="background:${themeColor}; color:#fff; padding:9px 18px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.9rem; box-shadow:0 2px 4px ${themeColor}40; display:inline-flex; align-items:center; gap:6px;">
                        ⬇️ Baixar Arquivo
                    </a>
                    <a href="${skill.path}" target="_blank" style="background:#fff; color:#334155; padding:9px 18px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.9rem; border:1px solid #cbd5e1; display:inline-flex; align-items:center; gap:6px;">
                        👀 Abrir no Navegador
                    </a>
                    ` : ''}
                    ${config.githubRepo ? `
                    <a href="${config.githubRepo}" target="_blank" style="background:#fff; color:#334155; padding:9px 18px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.9rem; border:1px solid #cbd5e1; display:inline-flex; align-items:center; gap:6px;">
                        🔗 Repositório Original
                    </a>
                    ` : ''}
                </div>

                <div style="border-top:1px solid #e2e8f0; padding-top:16px;">
                    <h4 style="margin:0 0 6px 0; color:#0f172a; font-size:0.95rem; display:flex; align-items:center; gap:6px;">
                        <span>🧠</span> O que é & Finalidade
                    </h4>
                    <p style="margin:0 0 12px 0; color:#475569; font-size:0.95rem; line-height:1.5;">
                        ${skill.description || 'Documentação oficial e metodologia recomendada.'}
                    </p>

                    <h4 style="margin:14px 0 6px 0; color:#0f172a; font-size:0.95rem; display:flex; align-items:center; gap:6px;">
                        <span>🛠️</span> Como Executar / Invocação
                    </h4>
                    <div style="background:#0f172a; color:#38bdf8; font-family:monospace; padding:10px 14px; border-radius:6px; font-size:12.5px; display:flex; align-items:center; justify-content:space-between;">
                        <span>${howToUseCommand}</span>
                        <button onclick="navigator.clipboard.writeText('${howToUseCommand.replace(/'/g, "\\'")}'); alert('Comando copiado!');" style="background:#1e293b; color:#cbd5e1; border:1px solid #475569; padding:3px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copiar</button>
                    </div>
                </div>
            </div>
        `;

        contentArea.innerHTML = `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                ${headerCard}
                ${htmlContent ? `<div class="tool-doc-content" style="max-width:980px; margin:0 auto; line-height:1.75; font-size:1.05rem;">${htmlContent}</div>` : ''}
            </div>
        `;
        if (container.classList.contains('active') && window.scrollPortalToTop) {
            window.scrollPortalToTop(true);
        }
    }

    // Tabs Event
    const tabBtns = hero.querySelectorAll('.tool-tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => {
                b.classList.remove('active');
                b.style.background = '';
                b.style.borderColor = '';
                b.style.color = '';
            });
            btn.classList.add('active');
            btn.style.background = themeColor;
            btn.style.borderColor = themeColor;
            btn.style.color = '#fff';
            activeFilter = btn.getAttribute('data-filter');

            if (activeFilter === 'cheatsheet' && config.cheatsheetHtml) {
                document.querySelectorAll(`#${config.containerId} .kb-nav-btn`).forEach(b => b.classList.remove('active'));
                contentArea.innerHTML = config.cheatsheetHtml;
            } else {
                renderSidebar();
                if (firstSelectableBtn) {
                    firstSelectableBtn.btn.click();
                }
            }
        });
    });

    // Search Input Event
    const searchBox = searchContainer.querySelector(`#${config.containerId}-search`);
    searchBox.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        renderSidebar();
    });

    renderSidebar();

    if (firstSelectableBtn) {
        firstSelectableBtn.btn.click();
    }
};
