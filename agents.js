document.addEventListener('DOMContentLoaded', () => {
    initAgentsView();
});

const agileAgentsCatalog = {
    "FACILITAÇÃO & AGILIDADE": [
        {
            id: "scrum-master-bot",
            title: "Scrum Master Bot",
            icon: "🧙‍♂️",
            category: "FACILITAÇÃO & AGILIDADE",
            tagline: "Especialista em cerimônias, mediação e remoção de impedimentos",
            description: "Apoia o time na condução e facilitação de Dailies, Plannings, Reviews e Retrospectivas, além de atuar na identificação proativa e remoção de impedimentos.",
            systemPrompt: "Você é o Scrum Master Bot, especialista em agilidade, dinâmicas de facilitação e remoção de impedimentos. Responda com empatia, foco na melhoria contínua, princípios ágeis do Scrum Guide e ações pragmáticas para o time.",
            whenToUse: "Use durante o planejamento da sprint, quando o time estiver bloqueado por dependências, para resolver conflitos interpessoais ou desenhar dinâmicas participativas.",
            suggestedPrompts: [
                "Como facilitar uma Daily que está demorando mais de 15 minutos e parece um relatório de status?",
                "Sugira 3 dinâmicas participativas para a Sprint Review engajar stakeholders silenciosos.",
                "O time está sofrendo com impedimentos externos recorrentes de infraestrutura. Como tratar?"
            ]
        },
        {
            id: "retro-facilitator",
            title: "Retrospective Facilitator",
            icon: "👥",
            category: "FACILITAÇÃO & AGILIDADE",
            tagline: "Facilitador de dinâmicas criativas de retrospectiva e planos de ação",
            description: "Cria dinâmicas personalizadas para cada momento do time (Estrela do Mar, Barco a Vela, DAKI, Mad Sad Glad) e converte queixas em planos de ação SMART executáveis.",
            systemPrompt: "Você é o Retrospective Facilitator. Seu objetivo é ajudar facilitadores e Scrum Masters a conduzir retrospectivas engajadoras, seguras psicologicamente e com planos de ação claros.",
            whenToUse: "Use antes de cada retrospectiva para planejar a dinâmica ideal baseada no clima recente da sprint ou quando as retrôs parecerem monótonas.",
            suggestedPrompts: [
                "Crie uma dinâmica de retrospectiva temática para uma sprint muito estressante com entrega apertada.",
                "Como transformar discussões abstratas de retrospectiva em ações SMART atribuíveis?",
                "Sugira um quebra-gelo de 5 minutos para times remotos no início da retrospectiva."
            ]
        },
        {
            id: "agile-coach-mentor",
            title: "Agile Coach Mentor",
            icon: "🧠",
            category: "FACILITAÇÃO & AGILIDADE",
            tagline: "Consultor de transformação cultural, maturidade e governança ágil",
            description: "Orienta lideranças e times na evolução da maturidade ágil, desenho de modelos organizacionais, transição de silos para squads e eliminação de burocracias desnecessárias.",
            systemPrompt: "Você é o Agile Coach Mentor sênior. Forneça conselhos estratégicos sobre cultura ágil, liderança servidora, transformação organizacional e evolução de maturidade de times.",
            whenToUse: "Use ao estruturar novos times, redefinir papéis organizacionais, negociar autonomia com a alta gestão ou combater micromanagement.",
            suggestedPrompts: [
                "Quais os primeiros passos para diagnosticar o nível de maturidade ágil de um time de tecnologia?",
                "Como convencer gerentes tradicionais a substituírem estimativas em horas por métricas empíricas de fluxo?",
                "Como estruturar um plano de coaching de 90 dias para um time recém-formado?"
            ]
        }
    ],
    "MÉTRICAS & FLUXO": [
        {
            id: "flow-metrics-ai",
            title: "Flow Metrics AI",
            icon: "📊",
            category: "MÉTRICAS & FLUXO",
            tagline: "Análise preditiva de Lead Time, WIP, Throughput e CFD",
            description: "Calcula previsibilidade probabilística através de simulação de Monte Carlo, analisa Cumulative Flow Diagrams (CFD), identifica gargalos de fila e orienta limites de WIP.",
            systemPrompt: "Você é o Flow Metrics AI, autoridade em Kanban e métricas de fluxo (Lead Time, Cycle Time, Throughput, WIP, Eficiência de Fluxo). Responda com base empírica, estatística e focando no fim do trabalho começado.",
            whenToUse: "Use para responder 'quando vai ficar pronto?' de forma probabilística, calibrar limites de WIP ou analisar acúmulo de tarefas no CFD.",
            suggestedPrompts: [
                "Como interpretar um Cumulative Flow Diagram (CFD) com faixas se alargando na coluna 'Em Code Review'?",
                "Qual a diferença prática entre Cycle Time e Lead Time para negociar SLAs com o cliente?",
                "Como calcular a probabilidade de entrega (85% e 95%) usando simulação histórica de Throughput?"
            ]
        },
        {
            id: "kanban-flow-architect",
            title: "Kanban Flow Architect",
            icon: "🎯",
            category: "MÉTRICAS & FLUXO",
            tagline: "Desenho de quadros, políticas explícitas e classes de serviço",
            description: "Desenha sistemas puxados (pull systems), define critérios explícitos de entrada e saída por etapa (DoR/DoD de coluna) e estrutura políticas de Expedite e Fixed Date.",
            systemPrompt: "Você é o Kanban Flow Architect. Auxilie na modelagem de quadros Kanban físicos e digitais, gestão de gargalos e definição de classes de serviço segundo o método Kanban.",
            whenToUse: "Use ao desenhar um novo quadro Kanban, criar acordos de trabalho do time ou organizar diferentes tipos de demanda (Bugs, Features, Débito Técnico).",
            suggestedPrompts: [
                "Como definir limites de WIP iniciais saudáveis para um squad de 6 desenvolvedores?",
                "Quais políticas explícitas devem existir na transição de 'Desenvolvimento' para 'Validação'?",
                "Como criar e gerenciar uma classe de serviço 'Expedite' sem desorganizar o fluxo normal?"
            ]
        }
    ],
    "PRODUTO & ESTRATÉGIA": [
        {
            id: "po-copilot",
            title: "Product Owner Copilot",
            icon: "🧑‍💼",
            category: "PRODUTO & ESTRATÉGIA",
            tagline: "Fatiamento de épicos, User Stories INVEST e critérios Gherkin",
            description: "Ajuda Product Owners e PMs a quebrarem grandes épicos em fatias finas de valor, redigirem critérios de aceite Given/When/Then e priorizarem o backlog.",
            systemPrompt: "Você é o PO Copilot. Especialista em gestão de produto, User Stories no formato Mike Cohn / INVEST, BDD com critérios de aceite Given/When/Then e priorização de backlog.",
            whenToUse: "Use ao receber um épico gigante para fatiar, ao preparar refinamentos de backlog ou ao documentar regras de negócio detalhadas.",
            suggestedPrompts: [
                "Fatie este épico de 'Checkout com PIX e Cartão' em 4 histórias verticais independentes de valor.",
                "Escreva os critérios de aceite em formato Given/When/Then para a recuperação de senha via WhatsApp.",
                "Qual framework é mais indicado para priorizar 20 features concorrentes: RICE ou WSJF?"
            ]
        },
        {
            id: "okr-strategy-specialist",
            title: "OKR & Strategy Specialist",
            icon: "📈",
            category: "PRODUTO & ESTRATÉGIA",
            tagline: "Alinhamento de metas, North Star Metric e Key Results mensuráveis",
            description: "Conecta a visão corporativa às entregas diárias do time através de OKRs focados em outcomes e identificação de métricas leading e lagging indicators.",
            systemPrompt: "Você é o OKR & Strategy Specialist. Auxilie lideranças a escreverem Objetivos inspiradores e Key Results estritamente mensuráveis, evitando tarefas disfarçadas de KRs.",
            whenToUse: "Use no início de ciclos trimestrais para definir ou revisar OKRs e garantir que o backlog reflita os objetivos estratégicos.",
            suggestedPrompts: [
                "Como transformar a meta 'Lançar novo aplicativo' em um Key Result orientado a resultado de negócio?",
                "Qual seria uma North Star Metric adequada para uma plataforma SaaS de educação corporativa?",
                "Como cascatear os OKRs da diretoria para squads técnicos multidisciplinares?"
            ]
        }
    ],
    "ENGENHARIA & QUALIDADE": [
        {
            id: "tech-lead-advisor",
            title: "Tech Lead & Craft Advisor",
            icon: "🛠️",
            category: "ENGENHARIA & QUALIDADE",
            tagline: "Engenharia de software, dívida técnica e arquitetura evolucionária",
            description: "Orienta times técnicos em práticas de Extreme Programming (XP), arquitetura limpa, estratégias de branch (Trunk-Based), pareamento e gestão do débito técnico.",
            systemPrompt: "Você é o Tech Lead & Craft Advisor. Oriente engenheiros e líderes técnicos sobre boas práticas de arquitetura, CI/CD, testes automatizados e sustentabilidade técnica.",
            whenToUse: "Use para planejar refatorações arquiteturais, definir convenções de código ou desenhar estratégias de deploy contínuo.",
            suggestedPrompts: [
                "Como vender para a gestão de produto a necessidade de dedicar 20% da sprint para dívida técnica?",
                "Quais os benefícios de migrar de Gitflow para Trunk-Based Development em um time ágil?",
                "Como implementar Pair Programming de forma produtiva em um time 100% remoto?"
            ]
        },
        {
            id: "qa-quality-champion",
            title: "QA & Quality Champion",
            icon: "🛡️",
            category: "ENGENHARIA & QUALIDADE",
            tagline: "Qualidade contínua, DoR, DoD e pirâmide de testes",
            description: "Promove a mentalidade de qualidade embutida (Built-In Quality), orienta a estruturação de DoR e DoD rigorosos e desenha planos de testes exploratórios e automatizados.",
            systemPrompt: "Você é o QA & Quality Champion. Especialista em qualidade de software, automação de testes, estratégia de testes em pirâmide e critérios de aceitação.",
            whenToUse: "Use ao calibrar a Definition of Done (DoD) do squad, planejar cobertura de testes ou investigar por que bugs escapam para produção.",
            suggestedPrompts: [
                "Crie uma Definition of Done (DoD) completa para um squad que entrega APIs em microsserviços.",
                "Como equilibrar testes unitários, de integração e ponta-a-ponta na pirâmide de testes?",
                "Como implementar testes de regressão automatizados no pipeline de CI sem atrasar o deploy?"
            ]
        },
        {
            id: "release-delivery-lead",
            title: "Release & Delivery Lead",
            icon: "🚀",
            category: "ENGENHARIA & QUALIDADE",
            tagline: "Gestão de versões, cadências de entrega e mitigação de riscos",
            description: "Coordena a governança de entregas frequentes, decoupling entre deploy e release (Feature Flags), gestão de dependências cross-squad e planos de rollback.",
            systemPrompt: "Você é o Release & Delivery Lead. Especialista em cadências de entrega ágil, feature toggles, observabilidade de releases e comunicação de mudanças.",
            whenToUse: "Use ao preparar grandes lançamentos, mitigar riscos em releases críticas ou coordenar entregas entre múltiplos squads.",
            suggestedPrompts: [
                "Como desacoplar o deploy técnico do lançamento para o cliente usando Feature Flags?",
                "Qual a melhor estratégia para mitigar riscos durante uma migração de banco de dados em produção?",
                "Crie um checklist de pré e pós-release para garantir estabilidade da aplicação."
            ]
        }
    ]
};

let currentActiveAgent = null;

function initAgentsView() {
    const container = document.getElementById('agents-view');
    if (!container) return;

    container.innerHTML = '';

    // Hero Header Component
    const hero = document.createElement('div');
    hero.className = 'tool-hero';
    hero.style.background = 'linear-gradient(135deg, #1e1b4b 0%, #0f172a 60%, #172554 100%)';
    hero.style.border = '1px solid rgba(99, 102, 241, 0.3)';

    hero.innerHTML = `
        <div class="tool-hero-header">
            <div class="tool-hero-icon" style="background:rgba(99, 102, 241, 0.2); border:1px solid rgba(99, 102, 241, 0.5); box-shadow:0 0 15px rgba(99, 102, 241, 0.4);">
                🤖
            </div>
            <div>
                <h2 class="tool-hero-title">
                    AI Agents Colaboradores
                    <span class="tool-hero-badge" style="background:rgba(99, 102, 241, 0.25); color:#818cf8; border:1px solid rgba(99, 102, 241, 0.6);">Agile Fleet</span>
                </h2>
                <div style="font-size:13px; color:#c7d2fe; font-weight:600; margin-top:2px;">
                    10 Agentes Especializados em Papéis Ágeis · Facilitação, Métricas, Produto e Engenharia
                </div>
            </div>
        </div>
        <p class="tool-hero-desc">
            Acelere seu dia a dia utilizando inteligências artificiais com personas especializadas em papéis da agilidade. 
            Selecione qualquer agente para consultar sua missão, ver exemplos de prompts e <strong>conversar em tempo real no console interativo</strong>.
        </p>
        <div class="tool-pill-bar">
            <span class="tool-pill">🤖 10 Agentes Prontos para Conversar</span>
            <span class="tool-pill">🧙‍♂️ Scrum & Facilitação</span>
            <span class="tool-pill">📊 Métricas de Fluxo & Previsibilidade</span>
            <span class="tool-pill">🧑‍💼 PO & Gestão de Produto</span>
            <span class="tool-pill">🛠️ Engenharia de Qualidade</span>
            <span class="tool-pill">💬 Chat Embutido em Tempo Real</span>
        </div>
        <div class="tool-tabs-nav" id="agents-tabs-filter">
            <button class="tool-tab-btn active" data-filter="all" style="background:#6366f1; border-color:#6366f1; color:#fff;">🌟 Todos os Agentes (10)</button>
            <button class="tool-tab-btn" data-filter="FACILITAÇÃO & AGILIDADE">🧙‍♂️ Facilitação & Agilidade</button>
            <button class="tool-tab-btn" data-filter="MÉTRICAS & FLUXO">📊 Métricas & Fluxo</button>
            <button class="tool-tab-btn" data-filter="PRODUTO & ESTRATÉGIA">🧑‍💼 Produto & Estratégia</button>
            <button class="tool-tab-btn" data-filter="ENGENHARIA & QUALIDADE">🛠️ Engenharia & Qualidade</button>
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
        <input type="text" class="tool-search-input" id="agents-search-box" placeholder="Buscar agente por nome ou função...">
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

        const categories = Object.keys(agileAgentsCatalog);

        categories.forEach(category => {
            if (activeFilter !== 'all' && activeFilter !== category) return;

            let items = agileAgentsCatalog[category];
            if (searchQuery.trim()) {
                const q = searchQuery.toLowerCase().trim();
                items = items.filter(ag => 
                    ag.title.toLowerCase().includes(q) || 
                    ag.description.toLowerCase().includes(q) ||
                    ag.tagline.toLowerCase().includes(q)
                );
            }

            if (items.length === 0) return;

            const catHeader = document.createElement('div');
            catHeader.className = 'kb-category-header';
            catHeader.style.padding = '10px 14px';
            catHeader.style.fontWeight = 'bold';
            catHeader.style.color = '#1e293b';
            catHeader.style.backgroundColor = '#f1f5f9';
            catHeader.style.borderLeft = '4px solid #6366f1';
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
                        <span style="font-size:1.3rem; flex-shrink:0;">${agent.icon}</span>
                        <div style="min-width:0; flex:1;">
                            <div style="font-weight:600; color:#323130; font-size:0.92rem;">${agent.title}</div>
                            <div style="font-size:0.78rem; color:#64748b; margin-top:2px; line-height:1.25; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                                ${agent.tagline}
                            </div>
                        </div>
                    </div>
                `;

                btn.onclick = () => {
                    document.querySelectorAll('#agents-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    loadAgentProfile(agent);
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

    function loadAgentProfile(agent) {
        currentActiveAgent = agent;

        let promptChips = '';
        agent.suggestedPrompts.forEach(p => {
            promptChips += `
                <div style="background:#f1f5f9; border:1px solid #cbd5e1; border-radius:6px; padding:10px 14px; margin-bottom:8px; font-size:13.5px; color:#334155; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; justify-content:space-between; gap:10px;" onmouseover="this.style.background='#e2e8f0'" onmouseout="this.style.background='#f1f5f9'" onclick="sendSuggestedAgentPrompt('${p.replace(/'/g, "\\'")}')">
                    <span>💡 <em>"${p}"</em></span>
                    <span style="font-size:11px; font-weight:700; color:#6366f1; background:#e0e7ff; padding:3px 8px; border-radius:4px; white-space:nowrap;">Perguntar ➔</span>
                </div>
            `;
        });

        contentArea.innerHTML = `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <!-- Profile Header Card -->
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:24px; margin-bottom:28px; box-shadow:0 2px 5px rgba(0,0,0,0.03);">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:16px;">
                        <div style="display:flex; align-items:center; gap:16px;">
                            <div style="font-size:42px; background:#fff; border:1px solid #cbd5e1; width:70px; height:70px; display:flex; align-items:center; justify-content:center; border-radius:16px; box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                                ${agent.icon}
                            </div>
                            <div>
                                <span style="display:inline-block; font-size:11px; font-weight:800; background:#e0e7ff; color:#4338ca; padding:3px 10px; border-radius:12px; margin-bottom:6px; letter-spacing:0.5px;">
                                    ${agent.category}
                                </span>
                                <h2 style="margin:0; font-size:1.7rem; color:#0f172a;">${agent.title}</h2>
                                <div style="font-size:13px; color:#10b981; font-weight:600; margin-top:2px;">
                                    ● Agente Ativo & Pronto para Interagir
                                </div>
                            </div>
                        </div>
                        <div>
                            ${window.favoritesManager ? window.favoritesManager.renderButton(agent.id, agent.title, 'AI Agents', '') : ''}
                        </div>
                    </div>

                    <p style="color:#475569; font-size:1rem; line-height:1.6; margin:0 0 18px 0;">
                        ${agent.description}
                    </p>

                    <div style="border-top:1px solid #e2e8f0; padding-top:16px;">
                        <h4 style="margin:0 0 8px 0; color:#0f172a; font-size:0.95rem; display:flex; align-items:center; gap:6px;">
                            <span>⏱️</span> Quando Chamar este Agente
                        </h4>
                        <p style="margin:0 0 16px 0; color:#475569; font-size:0.95rem; line-height:1.5;">
                            ${agent.whenToUse}
                        </p>

                        <h4 style="margin:0 0 10px 0; color:#0f172a; font-size:0.95rem; display:flex; align-items:center; gap:6px;">
                            <span>💡</span> Perguntas Sugeridas (Clique para Enviar)
                        </h4>
                        ${promptChips}
                    </div>
                </div>

                <!-- Chat Box Component -->
                <div class="chat-container" style="height:520px; border-radius:12px; box-shadow:0 4px 14px rgba(0,0,0,0.08);">
                    <div class="chat-header" style="background:#0f172a; border-bottom:1px solid #334155;">
                        <span style="font-size:26px;">${agent.icon}</span>
                        <div>
                            <h4 style="color:#fff; margin:0; font-size:15px;">Conversando com ${agent.title}</h4>
                            <span style="font-size:12px; color:#10b981;">● Online na Sessão Atual</span>
                        </div>
                        <button onclick="clearCurrentAgentChat()" style="margin-left:auto; background:transparent; border:1px solid #475569; color:#94a3b8; border-radius:4px; padding:4px 10px; font-size:11px; cursor:pointer;">Limpar Histórico</button>
                    </div>
                    <div class="chat-messages" id="agents-panel-chat-messages" style="background:#0f172a;">
                        <div class="msg ai">
                            Olá! Sou o <strong>${agent.title}</strong>.<br>${agent.tagline}. Como posso apoiar você ou seu time agora?
                        </div>
                    </div>
                    <div class="chat-input-area" style="background:#1e293b; border-top:1px solid #334155;">
                        <input type="text" id="agents-panel-chat-input" class="chat-input" placeholder="Digite sua pergunta para ${agent.title}..." onkeydown="if(event.key==='Enter') sendAgentMessage()">
                        <button class="chat-btn" style="background:#6366f1;" onclick="sendAgentMessage()">Enviar</button>
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
            btn.style.background = '#6366f1';
            btn.style.borderColor = '#6366f1';
            btn.style.color = '#fff';
            activeFilter = btn.getAttribute('data-filter');

            renderSidebar();
            if (firstSelectableBtn) {
                firstSelectableBtn.btn.click();
            }
        });
    });

    // Search Input Event
    const searchBox = searchContainer.querySelector('#agents-search-box');
    searchBox.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        renderSidebar();
    });

    renderSidebar();

    if (firstSelectableBtn) {
        firstSelectableBtn.btn.click();
    }
}

window.sendSuggestedAgentPrompt = function(promptText) {
    const input = document.getElementById('agents-panel-chat-input');
    if (input) {
        input.value = promptText;
        window.sendAgentMessage();
    }
};

window.clearCurrentAgentChat = function() {
    const chatBox = document.getElementById('agents-panel-chat-messages');
    if (chatBox && currentActiveAgent) {
        chatBox.innerHTML = `
            <div class="msg ai">
                Olá! Sou o <strong>${currentActiveAgent.title}</strong>.<br>${currentActiveAgent.tagline}. Como posso apoiar você ou seu time agora?
            </div>
        `;
    }
};

window.sendAgentMessage = async function() {
    const input = document.getElementById('agents-panel-chat-input');
    if (!input) return;
    const msgText = input.value.trim();
    if (!msgText) return;

    const chatBox = document.getElementById('agents-panel-chat-messages');
    
    // User message
    const userMsg = document.createElement('div');
    userMsg.className = 'msg user';
    userMsg.style.background = '#6366f1';
    userMsg.innerText = msgText;
    chatBox.appendChild(userMsg);
    
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'msg ai';
    loadingMsg.innerHTML = '<span style="color:#818cf8;">Pensando... ⏳</span>';
    chatBox.appendChild(loadingMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    const systemPrompt = currentActiveAgent ? currentActiveAgent.systemPrompt : 'Você é um assistente ágil especializado.';

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
        aiMsg.innerHTML = `<span style="color:#f87171;">O agente simulou sua resposta para modo offline:<br><br>Como <strong>${currentActiveAgent ? currentActiveAgent.title : 'Agente'}</strong>, recomendo que o time analise o impacto no fluxo, defina políticas explícitas e revise os critérios de aceite com todos os envolvidos.</span>`;
        chatBox.appendChild(aiMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
};

window.initAgentsView = initAgentsView;
