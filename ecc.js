document.addEventListener('DOMContentLoaded', () => {
    initEccAgentsView();
    initEccSkillsView();
});

let currentEccActiveAgent = null;

function categorizeEccAgents(agents) {
    const categories = {
        'ARQUITETURA & SISTEMAS': [],
        'ENGENHARIA & DESENVOLVIMENTO': [],
        'QUALIDADE & TESTES': [],
        'DEVOPS & PLATAFORMA': [],
        'GESTÃO & COMUNICAÇÃO': []
    };

    agents.forEach(ag => {
        const text = (ag.title + ' ' + (ag.description || '')).toLowerCase();
        if (text.includes('architect') || text.includes('arquiteto') || text.includes('sistema') || text.includes('design')) {
            categories['ARQUITETURA & SISTEMAS'].push(ag);
        } else if (text.includes('test') || text.includes('teste') || text.includes('review') || text.includes('revisor') || text.includes('qualidade') || text.includes('build-error')) {
            categories['QUALIDADE & TESTES'].push(ag);
        } else if (text.includes('devops') || text.includes('infra') || text.includes('deploy') || text.includes('ci') || text.includes('cloud')) {
            categories['DEVOPS & PLATAFORMA'].push(ag);
        } else if (text.includes('staff') || text.includes('comunicação') || text.includes('gestão') || text.includes('manager') || text.includes('lead')) {
            categories['GESTÃO & COMUNICAÇÃO'].push(ag);
        } else {
            categories['ENGENHARIA & DESENVOLVIMENTO'].push(ag);
        }
    });

    return Object.fromEntries(Object.entries(categories).filter(([k, v]) => v.length > 0));
}

function categorizeEccSkills(skills) {
    const categories = {
        'ARQUITETURA & PADRÕES': [],
        'FRONTEND & DESIGN': [],
        'BACKEND & APIS': [],
        'DEVOPS & CLOUD': [],
        'QUALIDADE & TESTES': [],
        'BANCO DE DADOS & DADOS': [],
        'IA & AGENTES': [],
        'DIVERSOS & UTILITÁRIOS': []
    };

    skills.forEach(s => {
        const text = (s.title + ' ' + (s.description || '') + ' ' + (s.triggers || []).join(' ')).toLowerCase();
        if (text.includes('agent') || text.includes('llm') || text.includes('prompt') || text.includes('eval') || text.includes('ia')) {
            categories['IA & AGENTES'].push(s);
        } else if (text.includes('test') || text.includes('tdd') || text.includes('qa') || text.includes('audit') || text.includes('quality') || text.includes('review')) {
            categories['QUALIDADE & TESTES'].push(s);
        } else if (text.includes('react') || text.includes('vue') || text.includes('css') || text.includes('ui') || text.includes('frontend') || text.includes('tailwind') || text.includes('design') || text.includes('a11y') || text.includes('html')) {
            categories['FRONTEND & DESIGN'].push(s);
        } else if (text.includes('sql') || text.includes('database') || text.includes('postgres') || text.includes('mongo') || text.includes('redis') || text.includes('data')) {
            categories['BANCO DE DADOS & DADOS'].push(s);
        } else if (text.includes('docker') || text.includes('k8s') || text.includes('kubernetes') || text.includes('ci/cd') || text.includes('deploy') || text.includes('aws') || text.includes('cloud') || text.includes('devops')) {
            categories['DEVOPS & CLOUD'].push(s);
        } else if (text.includes('api') || text.includes('rest') || text.includes('graphql') || text.includes('node') || text.includes('backend') || text.includes('server') || text.includes('auth')) {
            categories['BACKEND & APIS'].push(s);
        } else if (text.includes('arch') || text.includes('pattern') || text.includes('ddd') || text.includes('system') || text.includes('clean') || text.includes('solid')) {
            categories['ARQUITETURA & PADRÕES'].push(s);
        } else {
            categories['DIVERSOS & UTILITÁRIOS'].push(s);
        }
    });

    return Object.fromEntries(Object.entries(categories).filter(([k, v]) => v.length > 0));
}

function initEccAgentsView() {
    const container = document.getElementById('ecc-agents-view');
    if (!container || typeof eccAgentsData === 'undefined') return;

    container.innerHTML = '';

    const categorizedAgents = categorizeEccAgents(eccAgentsData);

    // Hero Header Component
    const hero = document.createElement('div');
    hero.className = 'tool-hero';
    hero.style.background = 'linear-gradient(135deg, #3b0764 0%, #0f172a 60%, #1e1b4b 100%)';
    hero.style.border = '1px solid rgba(168, 85, 247, 0.3)';

    hero.innerHTML = `
        <div class="tool-hero-header">
            <div class="tool-hero-icon" style="background:rgba(168, 85, 247, 0.2); border:1px solid rgba(168, 85, 247, 0.5); box-shadow:0 0 15px rgba(168, 85, 247, 0.4);">
                🤖
            </div>
            <div>
                <h2 class="tool-hero-title">
                    ECC AI Agents
                    <span class="tool-hero-badge" style="background:rgba(168, 85, 247, 0.25); color:#c084fc; border:1px solid rgba(168, 85, 247, 0.6);">Enterprise Claude Code</span>
                </h2>
                <div style="font-size:13px; color:#e9d5ff; font-weight:600; margin-top:2px;">
                    ${eccAgentsData.length} Agentes Especializados em Engenharia Avançada e Arquitetura de Software
                </div>
            </div>
        </div>
        <p class="tool-hero-desc">
            O ecossistema <strong>Everything Claude Code (ECC)</strong> disponibiliza um exército de agentes autônomos para tarefas de alta complexidade: 
            design de sistemas, acessibilidade WCAG, resolução de erros de build, exploração de código legado e otimização de performance.
        </p>
        <div class="tool-pill-bar">
            <span class="tool-pill">🤖 ${eccAgentsData.length} Agentes de Engenharia</span>
            <span class="tool-pill">🏛️ Arquiteto de Sistemas</span>
            <span class="tool-pill">🛠️ Resolvedor de Build</span>
            <span class="tool-pill">🔍 Explorador de Código</span>
            <span class="tool-pill">💬 Chat Embutido em Tempo Real</span>
        </div>
        <div class="tool-tabs-nav" id="ecc-agents-tabs-filter">
            <button class="tool-tab-btn active" data-filter="all" style="background:#8b5cf6; border-color:#8b5cf6; color:#fff;">🌟 Todos os Agentes (${eccAgentsData.length})</button>
            <button class="tool-tab-btn" data-filter="ARQUITETURA & SISTEMAS">🏛️ Arquitetura</button>
            <button class="tool-tab-btn" data-filter="ENGENHARIA & DESENVOLVIMENTO">💻 Desenvolvimento</button>
            <button class="tool-tab-btn" data-filter="QUALIDADE & TESTES">🧪 Qualidade & Testes</button>
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

    // Search bar inside sidebar
    const searchContainer = document.createElement('div');
    searchContainer.className = 'tool-sidebar-search';
    searchContainer.innerHTML = `
        <span class="tool-search-icon">🔍</span>
        <input type="text" class="tool-search-input" id="ecc-agents-search-box" placeholder="Buscar agente ECC...">
    `;
    sidebar.appendChild(searchContainer);

    const categoriesContainer = document.createElement('div');
    sidebar.appendChild(categoriesContainer);

    let activeFilter = 'all';
    let searchQuery = '';
    let firstSelectableBtn = null;

    function renderSidebar() {
        categoriesContainer.innerHTML = '';
        firstSelectableBtn = null;

        const categories = Object.keys(categorizedAgents);

        categories.forEach(category => {
            if (activeFilter !== 'all' && activeFilter !== category) return;

            let items = categorizedAgents[category];
            if (searchQuery.trim()) {
                const q = searchQuery.toLowerCase().trim();
                items = items.filter(ag => 
                    ag.title.toLowerCase().includes(q) || 
                    ag.description.toLowerCase().includes(q)
                );
            }

            if (items.length === 0) return;

            const catHeader = document.createElement('div');
            catHeader.className = 'kb-category-header';
            catHeader.style.padding = '10px 14px';
            catHeader.style.fontWeight = 'bold';
            catHeader.style.color = '#1e293b';
            catHeader.style.backgroundColor = '#f1f5f9';
            catHeader.style.borderLeft = '4px solid #8b5cf6';
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

            items.forEach(agent => {
                const btn = document.createElement('div');
                btn.className = 'kb-nav-btn';
                btn.style.padding = '10px 12px';
                btn.style.marginBottom = '4px';
                btn.innerHTML = `
                    <div style="display:flex; align-items:flex-start; gap:8px;">
                        <span style="font-size:1.3rem; flex-shrink:0;">${agent.icon || '🤖'}</span>
                        <div style="min-width:0; flex:1;">
                            <div style="font-weight:600; color:#323130; font-size:0.92rem;">${agent.title}</div>
                            <div style="font-size:0.78rem; color:#64748b; margin-top:2px; line-height:1.25; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                                ${agent.description}
                            </div>
                        </div>
                    </div>
                `;

                btn.onclick = () => {
                    document.querySelectorAll('#ecc-agents-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    loadEccAgentProfile(agent);
                };

                linkList.appendChild(btn);

                if (!firstSelectableBtn) {
                    firstSelectableBtn = { btn, agent };
                }
            });

            categoriesContainer.appendChild(catHeader);
            categoriesContainer.appendChild(linkList);
        });
    }

    function loadEccAgentProfile(agent) {
        currentEccActiveAgent = agent;

        contentArea.innerHTML = `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <!-- Profile Header Card -->
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:24px; margin-bottom:28px; box-shadow:0 2px 5px rgba(0,0,0,0.03);">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:16px;">
                        <div style="display:flex; align-items:center; gap:16px;">
                            <div style="font-size:42px; background:#fff; border:1px solid #cbd5e1; width:70px; height:70px; display:flex; align-items:center; justify-content:center; border-radius:16px; box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                                ${agent.icon || '🤖'}
                            </div>
                            <div>
                                <span style="display:inline-block; font-size:11px; font-weight:800; background:#f3e8ff; color:#7e22ce; padding:3px 10px; border-radius:12px; margin-bottom:6px; letter-spacing:0.5px;">
                                    ECC AGENT
                                </span>
                                <h2 style="margin:0; font-size:1.7rem; color:#0f172a;">${agent.title}</h2>
                                <div style="font-size:13px; color:#10b981; font-weight:600; margin-top:2px;">
                                    ● Especialista ECC Ativo & Disponível
                                </div>
                            </div>
                        </div>
                        <div>
                            ${window.favoritesManager ? window.favoritesManager.renderButton(agent.id, agent.title, 'ECC Agents', agent.path || '') : ''}
                        </div>
                    </div>

                    ${agent.path ? `
                    <div style="background:#f1f5f9; border:1px solid #cbd5e1; padding:10px 14px; border-radius:6px; font-family:monospace; font-size:0.85rem; color:#475569; display:flex; align-items:center; justify-content:space-between; margin-bottom:18px;">
                        <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">📂 <strong>Arquivo de Instrução:</strong> ${agent.path}</span>
                        <button onclick="navigator.clipboard.writeText('${agent.path}'); alert('Caminho copiado!');" style="background:#e2e8f0; border:none; padding:3px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copiar</button>
                    </div>
                    ` : ''}

                    <p style="color:#475569; font-size:1rem; line-height:1.6; margin:0 0 18px 0;">
                        ${agent.description}
                    </p>

                    <div style="display:flex; gap:10px; flex-wrap:wrap;">
                        ${agent.path ? `
                        <a href="${agent.path}" download="${agent.id}.md" style="background:#8b5cf6; color:#fff; padding:9px 18px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.9rem; box-shadow:0 2px 4px rgba(139, 92, 246, 0.4); display:inline-flex; align-items:center; gap:6px;">
                            ⬇️ Baixar Definição
                        </a>
                        <a href="${agent.path}" target="_blank" style="background:#fff; color:#334155; padding:9px 18px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.9rem; border:1px solid #cbd5e1; display:inline-flex; align-items:center; gap:6px;">
                            👀 Ver Arquivo
                        </a>
                        ` : ''}
                    </div>
                </div>

                <!-- Chat Box Component -->
                <div class="chat-container" style="height:520px; border-radius:12px; box-shadow:0 4px 14px rgba(0,0,0,0.08);">
                    <div class="chat-header" style="background:#0f172a; border-bottom:1px solid #334155;">
                        <span style="font-size:26px;">${agent.icon || '🤖'}</span>
                        <div>
                            <h4 style="color:#fff; margin:0; font-size:15px;">Conversando com ${agent.title}</h4>
                            <span style="font-size:12px; color:#10b981;">● Online na Arquitetura ECC</span>
                        </div>
                    </div>
                    <div class="chat-messages" id="ecc-panel-chat-messages" style="background:#0f172a;">
                        <div class="msg ai">
                            Olá! Sou o <strong>${agent.title}</strong> do ECC.<br>${agent.description}<br><br>Como posso apoiar seu projeto hoje?
                        </div>
                    </div>
                    <div class="chat-input-area" style="background:#1e293b; border-top:1px solid #334155;">
                        <input type="text" id="ecc-panel-chat-input" class="chat-input" placeholder="Digite sua pergunta para ${agent.title}..." onkeydown="if(event.key==='Enter') sendEccPanelMessage()">
                        <button class="chat-btn" style="background:#8b5cf6;" onclick="sendEccPanelMessage()">Enviar</button>
                    </div>
                </div>
            </div>
        `;
    }

    // Filter Buttons
    const filterButtons = hero.querySelectorAll('.tool-tab-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => {
                b.classList.remove('active');
                b.style.background = '';
                b.style.borderColor = '';
                b.style.color = '';
            });
            btn.classList.add('active');
            btn.style.background = '#8b5cf6';
            btn.style.borderColor = '#8b5cf6';
            btn.style.color = '#fff';
            activeFilter = btn.getAttribute('data-filter');

            renderSidebar();
            if (firstSelectableBtn) {
                firstSelectableBtn.btn.click();
            }
        });
    });

    const searchBox = searchContainer.querySelector('#ecc-agents-search-box');
    searchBox.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        renderSidebar();
    });

    renderSidebar();

    if (firstSelectableBtn) {
        firstSelectableBtn.btn.click();
    }
}

window.sendEccPanelMessage = async function() {
    const input = document.getElementById('ecc-panel-chat-input');
    if (!input) return;
    const msgText = input.value.trim();
    if (!msgText) return;

    const chatBox = document.getElementById('ecc-panel-chat-messages');
    
    const userMsg = document.createElement('div');
    userMsg.className = 'msg user';
    userMsg.style.background = '#8b5cf6';
    userMsg.innerText = msgText;
    chatBox.appendChild(userMsg);
    
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'msg ai';
    loadingMsg.innerHTML = '<span style="color:#c084fc;">Analisando... ⏳</span>';
    chatBox.appendChild(loadingMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    const systemPrompt = currentEccActiveAgent ? `Você é o agente ${currentEccActiveAgent.title}. ${currentEccActiveAgent.description}` : 'Você é um assistente de engenharia ECC.';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                systemPrompt: systemPrompt,
                messages: [{ role: 'user', content: msgText }]
            })
        });

        const data = await response.json();
        chatBox.removeChild(loadingMsg);

        const aiMsg = document.createElement('div');
        aiMsg.className = 'msg ai';
        if (response.ok) {
            aiMsg.innerText = data.reply;
        } else {
            aiMsg.innerHTML = `<span style="color:var(--danger);">Erro: ${data.error || 'Falha ao responder'}</span>`;
        }
        chatBox.appendChild(aiMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch(err) {
        chatBox.removeChild(loadingMsg);
        const aiMsg = document.createElement('div');
        aiMsg.className = 'msg ai';
        aiMsg.innerHTML = `<span style="color:#f87171;">O agente ECC simulou sua resposta:<br><br>Como <strong>${currentEccActiveAgent ? currentEccActiveAgent.title : 'Agente ECC'}</strong>, recomendo revisar os contratos de tipo e validar os limites de módulo antes de aplicar qualquer alteração.</span>`;
        chatBox.appendChild(aiMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
};

function initEccSkillsView() {
    if (typeof eccSkillsData === 'undefined' || !window.createStandardToolView) return;

    const categorized = categorizeEccSkills(eccSkillsData['Uncategorized'] || []);

    window.createStandardToolView({
        containerId: 'ecc-skills-view',
        title: 'ECC Skills',
        badge: 'Enterprise Skills',
        icon: '🧰',
        tagline: 'Biblioteca de 240+ skills avançadas de engenharia e desenvolvimento da arquitetura ECC',
        description: 'O catálogo de <strong>ECC Skills</strong> fornece instruções detalhadas para agentes e LLMs cobrindo desde testes unitários com TDD e design systems até profiling de performance, segurança contra injeção e pipelines de deploy.',
        themeColor: '#a855f7',
        themeGradient: 'linear-gradient(135deg, #3b0764 0%, #0f172a 60%, #1e1b4b 100%)',
        commandPrefix: '/ecc:',
        itemType: 'ECC Skills',
        pills: [
            { text: '🧰 240+ Skills de Engenharia' },
            { text: '🏛️ Padrões de Arquitetura' },
            { text: '🎨 Design & A11y' },
            { text: '🔒 Segurança & Auditoria' },
            { text: '⚡ Otimização Full-Stack' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todas as Skills (240+)' }
        ],
        data: categorized
    });
}

window.initEccAgentsView = initEccAgentsView;
window.initEccSkillsView = initEccSkillsView;
