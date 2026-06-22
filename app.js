document.addEventListener('DOMContentLoaded', () => {
    // O portal agora é aberto.
    // Apenas os simuladores exigirão autenticação (tratado dentro da view).

    const navItems = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view');
    const sectionTitle = document.getElementById('current-section-title');

    // Navegação lateral
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = item.getAttribute('data-target');
            
            // Update nav active state
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Update title
            sectionTitle.textContent = item.textContent.trim();

            // Toggle views
            views.forEach(view => {
                view.classList.remove('active');
            });
            const targetEl = document.getElementById(targetId);
            if(targetEl) {
                targetEl.classList.add('active');
            }
        });
    });

    // Função para carregar o conteúdo legado HTML e extrair as seções
    loadAndMigrateContent();
    initSkillsView();
    if (typeof initFluxoIaView === 'function') initFluxoIaView();
    if (typeof initKiroDocView === 'function') initKiroDocView();
    if (typeof initClaudeCodeDocView === 'function') initClaudeCodeDocView();
    if (typeof initLabsView === 'function') initLabsView();
    if (typeof initLiveSimView === 'function') initLiveSimView();
});

async function loadAndMigrateContent() {
    try {
        const response = await fetch('./contexto/scrumban_guia.html?v=' + new Date().getTime());
        const text = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');

        // Extração de conteúdo
        const extractSection = (groupId, viewId) => {
            const container = document.getElementById(viewId);
            if(!container) return;
            container.innerHTML = ''; // Clear loading

            let sectionsToExtract = [];
            if(viewId === 'kb-scrumban') {
                sectionsToExtract = [
                    { title: 'O que é (Visão KCP)', parts: [ { id: 's-oque', context: 'Teoria Base' } ] },
                    { title: 'Scrum vs Kanban vs Scrumban', parts: [ { id: 's-vs', context: 'Teoria Base' } ] },
                    { title: 'Board Completo', parts: [ { id: 's-board', context: 'Teoria Base' } ] },
                    { title: 'Commitment Point', parts: [ { id: 's-commitment', context: 'Teoria Base' }, { id: 's-teach-commitment', context: 'Para Ensinar' } ] },
                    { title: 'Fluxo de Trabalho', parts: [ { id: 's-fluxo', context: 'Teoria Base' } ] },
                    { title: 'Simulação Pull Flow', parts: [ { id: 's-scrumban-simulacao', context: 'Teoria Base' } ] },
                    { title: 'Cadências', parts: [ { id: 's-cadencias', context: 'Teoria Base' }, { id: 's-fac-replenishment', context: 'Facilitador em Campo (Replenishment)' } ] },
                    { title: 'Políticas Explícitas', parts: [ { id: 's-politicas', context: 'Kanban (Teoria Base)' }, { id: 's-teach-politicas', context: 'Para Ensinar' } ] },
                    { title: 'Limites de WIP', parts: [ { id: 's-wip', context: 'Teoria Base' }, { id: 's-teach-wip', context: 'Para Ensinar' }, { id: 's-fac-wip', context: 'Facilitador em Campo' } ] },
                    { title: 'Daily', parts: [ { id: 's-daily', context: 'Teoria Base' }, { id: 's-teach-daily', context: 'Para Ensinar' }, { id: 's-fac-daily', context: 'Facilitador em Campo' } ] },
                    { title: 'Demo', parts: [ { id: 's-demo', context: 'Teoria Base' } ] },
                    { title: 'Retrospectiva', parts: [ { id: 's-retro', context: 'Teoria Base' } ] },
                    { title: 'Bloqueios', parts: [ { id: 's-bloqueios', context: 'Teoria Base' }, { id: 's-fac-bloqueio', context: 'Facilitador em Campo' } ] },
                    { title: 'Classes de Serviço / Expedite', parts: [ { id: 's-cos', context: 'Teoria Base' }, { id: 's-teach-cos', context: 'Para Ensinar' }, { id: 's-fac-expedite', context: 'Facilitador em Campo' } ] },
                    { title: 'Métricas / Fluxo', parts: [ { id: 's-teach-fluxo', context: 'Para Ensinar (Fluxo vs Pessoas)' }, { id: 's-teach-metricas', context: 'Para Ensinar (Métricas)' }, { id: 's-fac-retro', context: 'Facilitador em Campo (Retro de Fluxo)' } ] },
                    { title: 'Trade-offs', parts: [ { id: 's-tradeoffs', context: 'Teoria Base' } ] },
                    { title: 'Itens Avançados', parts: [ { id: 's-avancado', context: 'Teoria Base' } ] },
                    { title: 'Quando Usar', parts: [ { id: 's-quando', context: 'Teoria Base' } ] },
                    { title: 'Anti-Padrões', parts: [ { id: 's-anti', context: 'Teoria Base' } ] },
                    { title: 'Papéis & Responsabilidades', parts: [ { id: 's-scrumban-papeis', context: 'Teoria Base' } ] },
                    { title: 'Primeiros 30 Dias', parts: [ { id: 's-scrumban-start', context: 'Teoria Base' } ] },
                    { title: 'Guia de Transição', parts: [ { id: 's-scrumban-transicao', context: 'Teoria Base' } ] },
                    { title: 'Maturidade do Time', parts: [ { id: 's-scrumban-maturidade', context: 'Teoria Base' }, { id: 's-teach-cultura', context: 'Para Ensinar (Cultura de Melhoria)' } ] },
                    { title: 'Scrumban + OKRs', parts: [ { id: 's-scrumban-okr', context: 'Teoria Base' } ] },
                    { title: 'Times Remotos', parts: [ { id: 's-scrumban-remotos', context: 'Teoria Base' } ] }
                ];
            } else if(viewId === 'kb-elite') {
                sectionsToExtract = [
                    // 0. Fundamentos
                    { title: 'O que é Kanban & Scrumban', parts: [ { id: 's-oque', context: 'Time de Elite' } ] },
                    // 1. Fundação e Acordos
                    { title: 'Tudo Sobre o Board (Regras)', parts: [ { id: 's-elite-politicas', context: 'Time de Elite' } ] },
                    { title: 'SLA por Classe de Serviço', parts: [ { id: 's-elite-sla', context: 'Time de Elite' } ] },
                    { title: 'Tamanho & Previsibilidade', parts: [ { id: 's-elite-tamanho', context: 'Time de Elite' } ] },
                    // 2. Upstream: Produto e Engenharia
                    { title: 'Visão de Produto (Story Map)', parts: [ { id: 's-po-storymap', context: 'Product Owner' } ] },
                    { title: 'Quebrando Features (PBB)', parts: [ { id: 's-po-pbb', context: 'Product Owner' } ] },
                    { title: 'Refinamentos (Upstream)', parts: [ { id: 's-apresentacao-refinamentos', context: 'Time de Elite' } ] },
                    { title: 'Sim. Ref. Funcional', parts: [ { id: 's-elite-sim-func', context: 'Time de Elite' } ] },
                    { title: 'Sim. Ref. Técnico', parts: [ { id: 's-elite-sim-tec', context: 'Time de Elite' } ] },
                    { title: 'Fluxo Git (TST → HML → PROD)', parts: [ { id: 's-elite-gitflow', context: 'Engenharia / CI/CD' } ] },
                    
                    // 3. Operação e Execução
                    { title: 'Board Completo', parts: [ { id: 's-elite-board', context: 'Time de Elite' } ] },
                    { title: 'Cadências do Scrumban', parts: [ { id: 's-elite-cadencias', context: 'Time de Elite' } ] },
                    { title: 'O Guia do Replenishment', parts: [ { id: 's-replenishment', context: 'Time de Elite' } ] },
                    { title: 'A Retrospectiva de Elite', parts: [ { id: 's-elite-retro', context: 'Time de Elite' } ] },
                    { title: 'Templates de Retrospectivas', parts: [ { id: 's-retro-templates', context: 'Time de Elite' } ] },
                    // 4. Avaliação e Melhoria Contínua
                    { title: 'Gestão de Resistência & IA', parts: [ { id: 's-elite-resistencia', context: 'Time de Elite' } ] },
                    { title: 'Touch Time vs Wait Time', parts: [ { id: 's-elite-flow', context: 'Time de Elite' } ] },
                    { title: 'Métricas Avançadas', parts: [ { id: 's-elite-metricas', context: 'Time de Elite' } ] },
                    { title: 'Scrumban Avançado', parts: [ { id: 's-scrumban-avancado', context: 'Time de Elite' } ] },
                    { title: 'Métricas DORA', parts: [ { id: 's-metricas-dora', context: 'Engenharia / Métricas' } ] },
                    { title: 'Health Check do Time', parts: [ { id: 's-healthcheck', context: 'Agile Coach / Métricas' } ] }
                ];
            } else if(viewId === 'kb-arquitetura-ia') {
                sectionsToExtract = [
                    { title: 'Harness & Ambientes da IA', parts: [ { id: 's-elite-harness', context: 'Engenharia / AI' } ] },
                    { title: 'Engenharia e IA no PRD', parts: [ { id: 's-po-ia-dev', context: 'Engenharia / PO' } ] },
                    { title: 'Documentos (PRD, SDD, TDD...)', parts: [ { id: 's-elite-docs', context: 'Engenharia / Arquitetura' } ] },
                    { title: '🎮 Simulador do Orquestrador', parts: [ { id: 's-elite-orchestrator', context: 'Engenharia / Arquitetura' } ] },
                    { title: 'Kiro: Simulador Hands-on', parts: [ { id: 's-kiro-hub', context: 'Engenharia / PO' } ] }
                ];
            } else if(viewId === 'kb-tfs') {
                sectionsToExtract = [
                    { title: 'Hierarquia e Links', parts: [ { id: 's-tfs-links', context: 'Especialista TFS' } ] },
                    { title: 'Configuração de Boards Kanban', parts: [ { id: 's-tfs-boards', context: 'Especialista TFS' } ] },
                    { title: 'Migração TFS para Cloud', parts: [ { id: 's-tfs-cloud', context: 'Especialista TFS' } ] }
                ];
            } else if(viewId === 'kb-agil') {
                sectionsToExtract = [
                    { title: 'Transformação Ágil', parts: [ { id: 's-agil', context: 'Transf. Ágil' } ] },
                    { title: 'Transformação Digital', parts: [ { id: 's-digital', context: 'Transf. Digital' } ] },
                    { title: 'Diferenças Lado a Lado', parts: [ { id: 's-diff', context: 'Diferenças' } ] },
                    { title: 'Fases da Transformação Ágil', parts: [ { id: 's-passo-agil', context: 'Jornada' } ] },
                    { title: 'Fases da Transformação Digital', parts: [ { id: 's-passo-digital', context: 'Jornada' } ] },
                    { title: 'O Case Nubank', parts: [ { id: 's-nubank', context: 'Estudo de Caso' } ] }
                ];
            } else if(viewId === 'kb-kanban') {
                sectionsToExtract = [
                    { title: 'O que é Kanban', parts: [ { id: 's-kanban', context: 'Guia Profundo' } ] },
                    { title: 'Os 9 Valores', parts: [ { id: 's-kanban-valores', context: 'Guia Profundo' } ] },
                    { title: 'Os 6 Princípios', parts: [ { id: 's-kanban-principios', context: 'Guia Profundo' } ] },
                    { title: 'As 6 Práticas', parts: [ { id: 's-kanban-praticas', context: 'Guia Profundo' },
                    { title: 'Papéis do Fluxo', parts: [ { id: 's-kanban-papeis', context: 'Kanban' } ] } ] },
                    { title: 'As 3 Agendas', parts: [ { id: 's-kanban-agendas', context: 'Guia Profundo' } ] },
                    { title: 'Upstream & Downstream', parts: [ { id: 's-kanban-upstream', context: 'Guia Profundo' } ] },
                    { title: 'O Framework STATIK', parts: [ { id: 's-kanban-statik', context: 'Guia Profundo' } ] },
                    { title: 'Classes de Serviço', parts: [ { id: 's-kanban-classes', context: 'Guia Profundo' } ] },
                    { title: 'Previsão & Monte Carlo', parts: [ { id: 's-kanban-previsao', context: 'Guia Profundo' } ] },
                    { title: 'Kanban em Escala', parts: [ { id: 's-kanban-escala', context: 'Guia Profundo' } ] },
                    { title: 'Casos Reais', parts: [ { id: 's-kanban-casos', context: 'Guia Profundo' } ] }
                ];
            } else if(viewId === 'kb-scrum') {
                sectionsToExtract = [
                    { title: 'Scrum Refinado', parts: [ { id: 's-scrum', context: 'Scrum' } ] }
                ];
            } else if(viewId === 'kb-po') {
                sectionsToExtract = [
                    { title: 'O Papel do PO', parts: [ { id: 's-po', context: 'Gestão de Produto' } ] },
                    { title: 'Lean Inception', parts: [ { id: 's-po-lean-inception', context: 'Descoberta de Produto' } ] },
                    { title: 'Continuous Discovery', parts: [ { id: 's-po-continuous-discovery', context: 'Descoberta de Produto' } ] },
                    { title: 'Visão de Produto (Story Map)', parts: [ { id: 's-po-storymap', context: 'Product Owner' } ] },
                    { title: 'Quebrando Features (PBB)', parts: [ { id: 's-po-pbb', context: 'Product Owner' } ] },
                    { title: 'Quebrando Histórias', parts: [ { id: 's-po-quebrando', context: 'Gestão de Produto' } ] },
                    { title: 'Refinamento Eficaz', parts: [ { id: 's-po-refinamento', context: 'Gestão de Produto' } ] },
                    { title: 'Priorização do Backlog', parts: [ { id: 's-po-priorizacao', context: 'Gestão de Produto' } ] },
                    { title: 'Formatos de Histórias', parts: [ { id: 's-po-formatos', context: 'Gestão de Produto' } ] },
                    { title: 'Roadmap Ágil', parts: [ { id: 's-po-roadmap', context: 'Gestão de Produto' } ] },
                    { title: 'Critérios de Aceite & BDD', parts: [ { id: 's-po-ac', context: 'Gestão de Produto' } ] },
                    { title: 'Engenharia e IA no PRD', parts: [ { id: 's-po-ia-dev', context: 'Engenharia / PO' } ] }
                ];
            } else if(viewId === 'kb-apresentacao') {
                sectionsToExtract = [
                    { title: 'O que é Scrumban', parts: [ { id: 's-oque', context: 'Apresentação' } ] },
                    { title: 'Scrum vs Kanban vs Scrumban', parts: [ { id: 's-vs', context: 'Apresentação' } ] },
                    { title: 'Touch Time vs Wait Time', parts: [ { id: 's-elite-flow', context: 'Apresentação' } ] },
                    { title: 'Regras do Board', parts: [ { id: 's-elite-politicas', context: 'Apresentação' } ] },
                    { title: 'SLA por Classe de Serviço', parts: [ { id: 's-elite-sla', context: 'Apresentação' } ] },
                    { title: 'Board Completo', parts: [ { id: 's-elite-board', context: 'Apresentação' } ] },
                    { title: 'Cadências do Scrumban', parts: [ { id: 's-elite-cadencias', context: 'Apresentação' } ] },
                    { title: 'Refinamentos (Upstream)', parts: [ { id: 's-apresentacao-refinamentos', context: 'Apresentação' } ] },
                    { title: 'Scrumban Avançado', parts: [ { id: 's-scrumban-avancado', context: 'Apresentação' } ] }
                ];
            } else if(viewId === 'kb-metricas') {
                sectionsToExtract = [
                    { title: 'Métricas de Fluxo', parts: [ { id: 's-metricas-fluxo', context: 'Métricas' } ] },
                    { title: 'Gráficos Kanban', parts: [ { id: 's-metricas-graficos', context: 'Métricas' } ] },
                    { title: 'Visão Executiva (C-Level)', parts: [ { id: 's-metricas-clevel', context: 'Métricas' } ] }
                ];

            }            // Create layout structure for Light Mode + SubNav
            
            const layout = document.createElement('div');
            layout.className = 'kb-layout';

            const sidebar = document.createElement('div');
            sidebar.className = 'kb-sidebar';

            const contentArea = document.createElement('div');
            contentArea.className = 'kb-page-content';

            layout.appendChild(sidebar);
            layout.appendChild(contentArea);
            container.appendChild(layout);

            let firstPage = true;

            sectionsToExtract.forEach((item, index) => {
                const wrapper = document.createElement('div');
                wrapper.className = 'section-group sub-page';
                wrapper.id = 'sub-topic-' + index;
                wrapper.style.display = firstPage ? 'block' : 'none';
                
                let hasContent = false;

                // Aggregate parts
                item.parts.forEach(part => {
                    const sectionHtml = doc.getElementById(part.id);
                    if(sectionHtml) {
                        hasContent = true;
                        sectionHtml.classList.remove('active');
                        sectionHtml.style.display = 'block';

                        const partContainer = document.createElement('div');
                        partContainer.className = 'aggregated-part';
                        
                        // Context Badge
                        const badge = document.createElement('div');
                        badge.className = 'context-badge';
                        badge.innerHTML = `<span>📌 Origem:</span> <strong>${part.context}</strong>`;
                        partContainer.appendChild(badge);

                        // Content
                        const contentWrapper = document.createElement('div');
                        contentWrapper.innerHTML = sectionHtml.innerHTML;
                        partContainer.appendChild(contentWrapper);

                        wrapper.appendChild(partContainer);
                    }
                });

                if(hasContent) {
                    contentArea.appendChild(wrapper);

                    // Create nav button
                    const btn = document.createElement('button');
                    btn.className = 'kb-nav-btn' + (firstPage ? ' active' : '');
                    btn.innerText = item.title;
                    btn.onclick = () => {
                        // Hide all pages in this section
                        contentArea.querySelectorAll('.sub-page').forEach(p => p.style.display = 'none');
                        // Deactivate all buttons
                        sidebar.querySelectorAll('.kb-nav-btn').forEach(b => b.classList.remove('active'));
                        // Activate current
                        btn.classList.add('active');
                        wrapper.style.display = 'block';
                        // Scroll to top of content
                        contentArea.scrollTop = 0;
                    };

                    sidebar.appendChild(btn);
                    firstPage = false;
                }
            });

            if(sidebar.innerHTML === '') {
                container.innerHTML = '<p>Conteúdo não encontrado ou em extração.</p>';
            }
        };

        // Popula as views
        extractSection('ng-scrumban', 'kb-scrumban');
        extractSection('ng-elite', 'kb-elite');
        extractSection('kb-arquitetura-ia', 'kb-arquitetura-ia');
        extractSection('kb-agil', 'kb-agil');
        extractSection('kb-kanban', 'kb-kanban');
        extractSection('kb-scrum', 'kb-scrum');
        extractSection('kb-po', 'kb-po');
        extractSection('kb-apresentacao', 'kb-apresentacao');
        extractSection('kb-metricas', 'kb-metricas');


        extractSection('kb-tfs', 'kb-tfs');

    } catch (error) {
        console.error('Erro ao carregar o conteúdo HTML:', error);
        document.querySelectorAll('.kb-content-container').forEach(el => {
            el.innerHTML = '<div class="alert alert-danger">Erro ao carregar os dados de contexto. Verifique se o arquivo está na pasta correta.</div>';
        });
    }
}











function initSkillsView() {
    const container = document.getElementById('skills-view');
    if(!container || typeof skillsData === 'undefined') return;

    function getContextualExamples(title) {
        const t = title.toLowerCase();
        if (t.includes('test') || t.includes('jest') || t.includes('cypress') || t.includes('playwright')) {
            return `
                <li style="margin-bottom:8px;"><code>"Por favor, crie testes unitários para este arquivo usando as diretrizes da skill ${title}."</code></li>
                <li><code>"Identifique os edge cases deste componente e gere testes de cobertura via ${title}."</code></li>
            `;
        } else if (t.includes('arch') || t.includes('defensive') || t.includes('securit') || t.includes('design') || t.includes('pattern')) {
            return `
                <li style="margin-bottom:8px;"><code>"Faça uma revisão de arquitetura e segurança neste arquivo aplicando a skill ${title}."</code></li>
                <li><code>"Quais padrões do ${title} estão sendo violados neste código? Sugira a refatoração."</code></li>
            `;
        } else if (t.includes('react') || t.includes('front') || t.includes('a11y') || t.includes('access') || t.includes('ui') || t.includes('css')) {
            return `
                <li style="margin-bottom:8px;"><code>"Revise este componente garantindo aderência às boas práticas e regras visuais do ${title}."</code></li>
                <li><code>"Atue como especialista em ${title} e melhore a estrutura e semântica deste código."</code></li>
            `;
        } else if (t.includes('review') || t.includes('lint') || t.includes('refactor') || t.includes('clean')) {
            return `
                <li style="margin-bottom:8px;"><code>"Atue como ${title} e faça um code review severo buscando code smells neste código."</code></li>
                <li><code>"Refatore esta função para deixá-la mais limpa, seguindo as regras de ${title}."</code></li>
            `;
        } else if (t.includes('build') || t.includes('error') || t.includes('debug') || t.includes('fix') || t.includes('resolve')) {
            return `
                <li style="margin-bottom:8px;"><code>"O código está falhando. Como especialista em ${title}, analise o log de erro e sugira o fix."</code></li>
                <li><code>"Invoque o conhecimento de ${title} para resolver este problema no projeto."</code></li>
            `;
        } else if (t.includes('data') || t.includes('sql') || t.includes('database') || t.includes('api') || t.includes('backend')) {
            return `
                <li style="margin-bottom:8px;"><code>"Otimize esta funcionalidade utilizando as diretrizes de performance do ${title}."</code></li>
                <li><code>"Como especialista em ${title}, estruture os dados para esta nova feature."</code></li>
            `;
        } else {
            return `
                <li style="margin-bottom:8px;"><code>"Analise as modificações deste arquivo garantindo que não estamos violando as políticas da skill ${title}."</code></li>
                <li><code>"Atue como especialista em ${title} e implemente a feature solicitada seguindo suas diretrizes."</code></li>
            `;
        }
    }

    container.innerHTML = '';

    
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.style.marginBottom = '20px';
    introHeader.innerHTML = `
        <h2 style="margin-top:0; color:#0078d4; margin-bottom:10px;">Flowgrammers Skills vs. AI Agents</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            <strong>Qual a diferença?</strong> Os <a href="#agents" style="color:#0078d4; text-decoration:none;">AI Agents</a> (no menu acima) são simuladores interativos embutidos <em>neste portal</em> (você clica e digita aqui). Já as <strong>Flowgrammers Skills</strong> são <em>manuais de instrução avançados</em> (arquivos <code>.md</code>). Você deve baixar esses arquivos e colocá-los no seu próprio ambiente local (Cursor, Windsurf, Claude Code) para que sua Inteligência Artificial aja como o especialista descrito.
        </p>
    `;
    container.appendChild(introHeader);

    const layout = document.createElement('div');
    layout.className = 'kb-layout';

    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';

    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    container.appendChild(introHeader);
    container.appendChild(layout);

    // Get categories and sort them alphabetically
    const categories = Object.keys(skillsData).sort();
    
    let firstGlobalBtn = null;

    categories.forEach((category) => {
        const skillsList = skillsData[category];
        
        // Category Header
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #0078d4';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        catHeader.style.marginBottom = '2px';
        catHeader.style.borderRadius = '0 6px 6px 0';
        catHeader.style.transition = 'background 0.2s';
        catHeader.style.display = 'flex';
        catHeader.style.justifyContent = 'space-between';
        catHeader.style.alignItems = 'center';
        
        const titleSpan = document.createElement('span');
        titleSpan.innerText = category;
        const iconSpan = document.createElement('span');
        iconSpan.innerText = '▼';
        iconSpan.style.fontSize = '0.8rem';
        iconSpan.style.color = '#aaa';
        
        catHeader.appendChild(titleSpan);
        catHeader.appendChild(iconSpan);
        
        const subMenu = document.createElement('div');
        subMenu.className = 'kb-submenu';
        subMenu.style.display = 'none'; 
        subMenu.style.paddingLeft = '5px';
        subMenu.style.marginBottom = '10px';

        catHeader.onmouseover = () => catHeader.style.backgroundColor = '#e1dfdd';
        catHeader.onmouseout = () => catHeader.style.backgroundColor = '#f3f2f1';

        sidebar.appendChild(catHeader);
        sidebar.appendChild(subMenu);

        let firstBtnInCategory = null;

        skillsList.forEach((skill) => {
            const wrapper = document.createElement('div');
            wrapper.className = 'section-group sub-page';
            wrapper.style.display = 'none';
            
            let sTriggers = skill.triggers || [];
            sTriggers = sTriggers.filter(t => {
                if (typeof t !== 'string') return false;
                t = t.trim();
                if (t.length < 2 || t.length > 35) return false;
                if (!t.match(/^\/[a-z0-9-_]+$/i) && !t.match(/^[a-z0-9 ]+$/i)) return false;
                if (['/var', '/etc', '/usr', '/bin', '/tmp', '/dev', '/opt'].includes(t)) return false;
                return true;
            }).map(t => t.trim());
            let visibleTriggers = sTriggers.slice(0, 8);
            let extraCount = sTriggers.length - 8;
            let triggersList = visibleTriggers.map(t => `<span class="tag" style="display:inline-block; background:rgba(0,120,212,.12); border:1px solid rgba(0,120,212,.3); padding:.3em .8em; border-radius:999px; font-size:.85rem; color:#0078d4; margin-right:5px; margin-bottom:5px; word-break: break-all;">${t}</span>`).join('');
            if (extraCount > 0) {
                triggersList += `<span class="tag" style="display:inline-block; background:rgba(0,0,0,.05); border:1px solid rgba(0,0,0,.1); padding:.3em .8em; border-radius:999px; font-size:.85rem; color:#4a5568; margin-right:5px; margin-bottom:5px;">+ ${extraCount} outros</span>`;
            }
            
            wrapper.innerHTML = `
                <div class="card" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:2.5rem; box-shadow:0 4px 6px rgba(0,0,0,0.02); max-width: 900px;">
                    <div style="text-transform: uppercase; font-size: 0.85rem; color: #0078d4; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">📁 ${category}</div>
                    <h3 style="margin-bottom:1.2rem; color:#1a202c; font-size:2rem; border-bottom:1px solid #eee; padding-bottom: 1rem;">${skill.title}</h3>
                    <p style="color:#4a5568; margin-bottom:2rem; font-size:1.15rem; line-height:1.7;">${skill.description || '<i>Sem descrição fornecida.</i>'}</p>
                    
                    
                    <div style="display: flex; gap: 10px; margin-bottom: 2rem;">
                        <a href="flowgrammers-skills-main/flowgrammers-skills-main/${skill.path}" download="${skill.id}.md" style="display:inline-block; background-color:#0078d4; color:#fff; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:1rem; box-shadow:0 2px 4px rgba(0,0,0,0.1); transition: background 0.2s;">
                            ⬇️ Baixar Arquivo da Skill
                        </a>
                        <a href="flowgrammers-skills-main/flowgrammers-skills-main/${skill.path}" target="_blank" style="display:inline-block; background-color:#f3f2f1; color:#323130; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; border: 1px solid #edebe9; font-size:1rem; transition: background 0.2s;">
                            👀 Ver Arquivo
                        </a>
                    </div>


                    
                    
                    ${skill.dependencies && skill.dependencies.length > 0 ? `
                    <div style="background:#f0f8ff; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #0078d4; margin-bottom: 2rem;">
                        <h4 style="margin-top:0; margin-bottom:1rem; font-size:1.1rem; color:#0078d4; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🔗 Skills Vinculadas (Sub-Skills)</h4>
                        <p style="font-size:0.95rem; color:#4a5568; margin-bottom:1rem;">Esta skill possui conexões diretas ou invoca o conhecimento das seguintes skills:</p>
                        <div>
                            ${skill.dependencies.map(d => `<span class="tag" style="display:inline-block; background:rgba(0,120,212,.12); border:1px solid rgba(0,120,212,.3); padding:.3em .8em; border-radius:4px; font-size:.85rem; color:#0078d4; margin-right:5px; margin-bottom:5px; font-weight:bold;">${d}</span>`).join('')}
                        </div>
                    </div>
                    ` : ''}

                    <h4 style="margin-top:1.5rem; margin-bottom:0.8rem; font-size:1rem; color:#718096; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🛠️ Como Instalar (Claude Code):</h4>
                    <pre style="background:#1e1e1e; color:#d4d4d4; padding:1.2rem; border-radius:8px; font-family:monospace; overflow-x:auto; margin-bottom:2rem; font-size:1.05rem;">/read flowgrammers-skills-main/flowgrammers-skills-main/${skill.path}</pre>
                    
                    <h4 style="margin-top:1.5rem; margin-bottom:0.8rem; font-size:1rem; color:#718096; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🚀 Como Executar (Exemplos Práticos):</h4>
                    <p style="font-size:1rem; color:#4a5568; line-height: 1.6;">No Claude Code, após o <strong>/read</strong> acima, peça a tarefa usando linguagem natural. Veja exemplos de acionamento:</p>
                    <div style="background:#f8fafc; padding:15px; border-radius:8px; border-left:4px solid #38bdf8; margin-top:10px;">
                        <ul style="margin:0; padding-left:20px; color:#334155;">
                            ${getContextualExamples(skill.title)}
                        </ul>
                    </div>
                </div>
            `;
            contentArea.appendChild(wrapper);

            const btn = document.createElement('button');
            btn.className = 'kb-nav-btn';
            btn.style.fontSize = '0.9rem';
            btn.style.padding = '8px 10px 8px 25px';
            btn.innerText = skill.title;
            
            btn.onclick = () => {
                contentArea.querySelectorAll('.sub-page').forEach(p => p.style.display = 'none');
                sidebar.querySelectorAll('.kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                wrapper.style.display = 'block';
                contentArea.scrollTop = 0;
            };

            subMenu.appendChild(btn);

            if(!firstBtnInCategory) {
                firstBtnInCategory = btn;
            }
            if(!firstGlobalBtn) {
                firstGlobalBtn = { header: catHeader, submenu: subMenu, btn: btn, wrapper: wrapper };
            }
        });

        // Click on category logic
        catHeader.onclick = () => {
            const isVisible = subMenu.style.display === 'block';
            
            // Close all
            sidebar.querySelectorAll('.kb-submenu').forEach(sm => sm.style.display = 'none');
            sidebar.querySelectorAll('.kb-category-header span:last-child').forEach(sp => sp.innerText = '▼');
            
            if (!isVisible) {
                // Open clicked
                subMenu.style.display = 'block';
                iconSpan.innerText = '▲';
                // Auto-click the first skill so the right panel matches the open category
                if(firstBtnInCategory) {
                    firstBtnInCategory.click();
                }
            }
        };
    });

    // Auto-open first global category
    if(firstGlobalBtn) {
        firstGlobalBtn.submenu.style.display = 'block';
        firstGlobalBtn.header.querySelector('span:last-child').innerText = '▲';
        firstGlobalBtn.btn.click();
    }
}


// --- INJETADO PARA SIMULADOR KIRO ---
window.kiroSim = {
      currentStep: 0,
      columns: [
        { id: 'c1', name: 'New' },
        { id: 'c2', name: 'Ref. Funcional (IA)' },
        { id: 'c3', name: 'Ag. Ref Técnico' },
        { id: 'c4', name: 'Em Ref. (IA)' },
        { id: 'c5', name: 'Aguardando PO' },
        { id: 'c6', name: 'Em Dev (IA)' },
        { id: 'c7', name: 'Em Teste (IA)' },
        { id: 'c8', name: 'Ag. PO (Final)' },
        { id: 'c9', name: 'Lib. Instalar' },
        { id: 'c10', name: 'Done' }
      ],
      steps: [
        { col: 0, cmd: "# Ambiente Kiro Idle", out: "<span style='color:#6b7280;'>// O PO acaba de criar a ideia bruta no TFS.</span><br><span style='color:#6b7280;'>// O Kiro aguarda o item ser puxado para a esteira (Pull).</span>" },
        { col: 1, cmd: "> kiro run ecc/blueprint --work-item=101", out: "<span style='color:#3b82f6;'>[MCP TFS]</span> Lendo Descrição do Work Item 101...<br><span style='color:#a855f7;'>[Steering]</span> Aplicando Política: 'Gerar PRD e Critérios BDD'. <a href='javascript:void(0)' onclick='openInfoModalDirect(&quot;skills/refinamento/SKILL&quot;)' style='color:#fde047; text-decoration:underline;'>[Ver Skill]</a><br><span style='color:#10b981;'>[Kiro]</span> Artefato 'PRD.md' gerado.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Aguardando Refinamento Técnico'" },
        { col: 2, cmd: "# Fila de Transição", out: "<span style='color:#6b7280;'>// O card está em uma fila (buffer). A IA terminou o trabalho funcional.</span><br><span style='color:#6b7280;'>// O Kiro Architect aguarda capacidade para puxar.</span>" },
        { col: 3, cmd: "> kiro run ecc/architecture-decision-records --work-item=101", out: "<span style='color:#3b82f6;'>[MCP TFS]</span> Lendo PRD.md...<br><span style='color:#10b981;'>[Kiro]</span> Artefato 'Design_Spec.md' gerado. <a href='javascript:void(0)' onclick='openInfoModalDirect(&quot;skills/arquitetura/SKILL&quot;)' style='color:#fde047; text-decoration:underline;'>[Ver Skill]</a><br><span style='color:#3b82f6;'>[MCP TFS]</span> Quebrando Work Item 101 em 3 sub-tasks.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Aguardando Avaliação PO'" },
        { col: 4, cmd: "@Kiro, aprovar spec.", out: "<span style='color:#f59e0b;'>[Gate Humano]</span> O Kiro parou de processar.<br><span style='color:#a855f7;'>[Usuário]</span> Digita '/approve'.<br><span style='color:#3b82f6;'>[MCP TFS]</span> Movendo para 'Em Desenvolvimento'." },
        { col: 5, cmd: "> kiro run ecc/tdd-workflow", out: "<span style='color:#ef4444;'>[Kiro Test]</span> Executando login.spec.ts -> <b>FALHA</b>.<br><span style='color:#10b981;'>[Kiro Code]</span> Implementando login.ts -> <b>PASSOU</b>. <a href='javascript:void(0)' onclick='openInfoModalDirect(&quot;skills/engenheiro-software/SKILL&quot;)' style='color:#fde047; text-decoration:underline;'>[Ver Skill]</a><br><span style='color:#eab308;'>[Git]</span> Commit automático: 'feat: add OTP login'.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Em Teste'." },
        { col: 6, cmd: "> kiro run ecc/security-review", out: "<span style='color:#10b981;'>[Kiro QA]</span> Executando testes E2E.<br><span style='color:#a855f7;'>[Kiro Security]</span> Scan OWASP: 0 vulnerabilidades. <a href='javascript:void(0)' onclick='openInfoModalDirect(&quot;skills/engenharia-qa/SKILL&quot;)' style='color:#fde047; text-decoration:underline;'>[Ver Skill]</a><br><span style='color:#3b82f6;'>[MCP TFS]</span> Inserindo evidências no Test Plan.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Aguardando Avaliação PO'." },
        { col: 7, cmd: "@Kiro, aprovar QA.", out: "<span style='color:#f59e0b;'>[Gate Final]</span> O PO analisa evidências.<br><span style='color:#a855f7;'>[Usuário]</span> Digita '/approve-deploy'.<br><span style='color:#3b82f6;'>[MCP TFS]</span> PATCH System.State = 'Liberado para Instalar'." },
        { col: 8, cmd: "# Azure Pipelines Trigger", out: "<span style='color:#10b981;'>[Pipeline]</span> Gatilho detectado via Webhook.<br><span style='color:#6b7280;'>// Pipeline executando build e deploy.</span><br><span style='color:#3b82f6;'>[MCP TFS]</span> Ao sucesso do deploy, move para 'Done'." },
        { col: 9, cmd: "# Concluído", out: "<span style='color:#10b981;'>✅ Ciclo de vida encerrado.</span><br><span style='color:#6b7280;'>// Métricas de Lead Time registradas nativamente no TFS.</span>" }
      ],
      init() {
        const board = document.getElementById('sim-board');
        if(!board) return;
        board.innerHTML = '';
        this.columns.forEach((c, idx) => {
          board.innerHTML += `
            <div class="sim-col ${idx===this.currentStep ? 'active-col' : ''}" id="col-${idx}">
              <div class="sim-col-title">${c.name}</div>
              ${idx === this.currentStep ? this.getCardHTML() : ''}
            </div>
          `;
        });
        this.renderTerminal();
        this.updateButtons();
      },
      getCardHTML() {
        return `
          <div class="sim-card" id="simulated-card">
            <div style="font-size:10px; color:#94a3b8;">ID: #101</div>
            <strong>Login via OTP</strong>
            <div class="tag">AI-Guided</div>
          </div>
        `;
      },
      renderTerminal() {
        const step = this.steps[this.currentStep];
        document.getElementById('sim-step-num').innerText = (this.currentStep + 1);
        document.getElementById('sim-terminal').innerHTML = `
          <div style="color:#fde047; margin-bottom:10px;">${step.cmd}</div>
          <div>${step.out}</div>
        `;
      },
      updateButtons() {
        const btnNext = document.getElementById('btn-next-step');
        const btnPrev = document.getElementById('btn-prev-step');
        
        if(this.currentStep === this.steps.length - 1) {
          btnNext.innerText = "✅ Concluído";
          btnNext.style.background = "#10b981";
          btnNext.disabled = true;
          btnNext.style.opacity = "0.5";
        } else {
          btnNext.innerText = "▶ Próximo Passo";
          btnNext.style.background = "#3b82f6";
          btnNext.disabled = false;
          btnNext.style.opacity = "1";
        }

        if(this.currentStep === 0) {
          btnPrev.disabled = true;
          btnPrev.style.opacity = "0.5";
        } else {
          btnPrev.disabled = false;
          btnPrev.style.opacity = "1";
        }
      },
      nextStep() {
        if (this.currentStep >= this.steps.length - 1) return;
        this.currentStep++;
        this.init(); // re-render
      },
      prevStep() {
        if (this.currentStep <= 0) return;
        this.currentStep--;
        this.init(); // re-render
      },
      resetStep() {
        this.currentStep = 0;
        this.init();
      }
    };

// Auto-init when DOM is ready and elements exist
setInterval(() => {
  if(document.getElementById('sim-board') && !window.kiroSim._initialized) {
    window.kiroSim.init();
    window.kiroSim._initialized = true;
  }
}, 1000);

/* =========================================================================
   Orchestrator vs Worker Simulator Logic
   ========================================================================= */
let simTimeout1, simTimeout2, simTimeout3, simTimeout4, simTimeout5, simTimeout6, simTimeout7;

window.resetOrchestratorSim = function() {
    clearTimeout(simTimeout1); clearTimeout(simTimeout2); clearTimeout(simTimeout3); clearTimeout(simTimeout4); clearTimeout(simTimeout5); clearTimeout(simTimeout6); clearTimeout(simTimeout7);
    const humBox = document.getElementById('sim-hum-box');
    const orqBox = document.getElementById('sim-orq-box');
    const wrkBox = document.getElementById('sim-wrk-box');
    if(!orqBox || !wrkBox || !humBox) return;

    humBox.style.borderColor = '#334155';
    humBox.style.boxShadow = 'none';
    orqBox.style.borderColor = '#334155';
    orqBox.style.boxShadow = 'none';
    wrkBox.style.borderColor = '#334155';
    wrkBox.style.boxShadow = 'none';
    
    document.getElementById('sim-arrow-right-1').style.opacity = '0.2';
    document.getElementById('sim-arrow-left-1').style.opacity = '0.2';
    document.getElementById('sim-arrow-right-2').style.opacity = '0.2';
    document.getElementById('sim-arrow-left-2').style.opacity = '0.2';
    
    document.getElementById('sim-hum-log').innerHTML = '> Pensando...';
    document.getElementById('sim-hum-log').style.color = '#a855f7';
    document.getElementById('sim-orq-log').innerHTML = '> Aguardando comandos...';
    document.getElementById('sim-orq-log').style.color = '#10b981';
    document.getElementById('sim-wrk-log').innerHTML = '> Dormindo...';
    document.getElementById('sim-wrk-log').style.color = '#3b82f6';
};

window.startOrchestratorSim = function() {
    window.resetOrchestratorSim();
    
    const humBox = document.getElementById('sim-hum-box');
    const humLog = document.getElementById('sim-hum-log');
    const orqBox = document.getElementById('sim-orq-box');
    const orqLog = document.getElementById('sim-orq-log');
    const wrkBox = document.getElementById('sim-wrk-box');
    const wrkLog = document.getElementById('sim-wrk-log');
    
    const aR1 = document.getElementById('sim-arrow-right-1');
    const aL1 = document.getElementById('sim-arrow-left-1');
    const aR2 = document.getElementById('sim-arrow-right-2');
    const aL2 = document.getElementById('sim-arrow-left-2');

    if(!orqBox) return;

    // Step 1: Humano escreve a tarefa
    humBox.style.borderColor = '#a855f7';
    humBox.style.boxShadow = '0 0 15px rgba(168,85,247,0.3)';
    humLog.innerHTML = '> Escrevendo PRD no TFS...<br>> Feature: "Criar Tela de Login"<br>> Acionando terminal: `kiro run`';

    // Step 2: Humano manda pro Kiro
    simTimeout1 = setTimeout(() => {
        aR1.style.opacity = '1';
        humLog.innerHTML += '<br><br>> [ENVIANDO] Demanda para o Orquestrador...';
    }, 2000);

    // Step 3: Kiro recebe e atua como Arquiteto
    simTimeout2 = setTimeout(() => {
        aR1.style.opacity = '0.2';
        humBox.style.borderColor = '#334155';
        humBox.style.boxShadow = 'none';
        
        orqBox.style.borderColor = '#10b981';
        orqBox.style.boxShadow = '0 0 15px rgba(16,185,129,0.3)';
        orqLog.innerHTML = '> Lendo TFS...<br>> [SKILL: Arquiteto] Gerando spec.md<br>> Quebrando em 2 Tasks:<br>1. Auth API<br>2. React Form<br>> [Harness] Chamando Claude Code';
    }, 3500);

    // Step 4: Kiro delega pro Claude
    simTimeout3 = setTimeout(() => {
        aR2.style.opacity = '1';
        orqLog.innerHTML += '<br><br>> [DELEGANDO] Task 1: Auth API...';
    }, 6000);

    // Step 5: Claude tenta codar e falha
    simTimeout4 = setTimeout(() => {
        aR2.style.opacity = '0.2';
        orqBox.style.borderColor = '#334155';
        orqBox.style.boxShadow = 'none';
        
        wrkBox.style.borderColor = '#3b82f6';
        wrkBox.style.boxShadow = '0 0 15px rgba(59,130,246,0.3)';
        wrkLog.innerHTML = '> [SKILL: Coder TDD] Lendo spec.md<br>> Rodando testes...<br>> <span style="color:#ef4444;">ERRO: module bcrypt missing</span><br>> Devolvendo para Kiro.';
        aL2.style.opacity = '1';
    }, 8000);

    // Step 6: Kiro resolve e manda de novo
    simTimeout5 = setTimeout(() => {
        aL2.style.opacity = '0.2';
        wrkBox.style.borderColor = '#334155';
        wrkBox.style.boxShadow = 'none';
        
        orqBox.style.borderColor = '#f59e0b';
        orqBox.style.boxShadow = '0 0 15px rgba(245,158,11,0.3)';
        orqLog.innerHTML = '> [ANALISANDO ERRO]<br>> Solução encontrada.<br>> [DELEGANDO] Rode `npm i bcrypt` e prossiga.';
        aR2.style.opacity = '1';
    }, 11000);

    // Step 7: Claude finaliza e devolve pro Kiro
    simTimeout6 = setTimeout(() => {
        aR2.style.opacity = '0.2';
        orqBox.style.borderColor = '#334155';
        orqBox.style.boxShadow = 'none';
        
        wrkBox.style.borderColor = '#10b981';
        wrkBox.style.boxShadow = '0 0 15px rgba(16,185,129,0.3)';
        wrkLog.style.color = '#10b981';
        wrkLog.innerHTML = '> `npm i bcrypt` executado.<br>> Testes passando ✅<br>> Commit efetuado.<br>> [DEVOLVENDO] Task 1 Completa.';
        aL2.style.opacity = '1';
    }, 14000);
    
    // Step 8: Kiro devolve pro Humano
    simTimeout7 = setTimeout(() => {
        aL2.style.opacity = '0.2';
        wrkBox.style.borderColor = '#334155';
        wrkBox.style.boxShadow = 'none';
        
        orqBox.style.borderColor = '#10b981';
        orqBox.style.boxShadow = '0 0 15px rgba(16,185,129,0.3)';
        orqLog.innerHTML = '> [SKILL: Arquiteto] Validando código.<br>> PR gerado.<br>> Atualizando TFS para "Code Review".';
        
        aL1.style.opacity = '1';
        
        setTimeout(() => {
            orqBox.style.borderColor = '#334155';
            orqBox.style.boxShadow = 'none';
            humBox.style.borderColor = '#10b981';
            humBox.style.boxShadow = '0 0 15px rgba(16,185,129,0.3)';
            humLog.style.color = '#10b981';
            humLog.innerHTML = '> Slack: "Chefe, Tela de Login PR enviado!"<br>> Fluxo concluído ✅';
        }, 2000);
    }, 17000);
};

// ==========================================
// REPLENISHMENT SIMULATOR LOGIC
// ==========================================
const repScenarios = [
    {
        title: "Cenário 1: Fome de Downstream",
        board: {
            upstream: ["Épico A", "Épico B", "Épico C"],
            refinement: ["Story 1 (Ready)", "Story 2 (Ready)", "Story 3 (Ready)"],
            readyForDev: ["Story 4"], // Limite 4
            inProgress: ["Story 5"],
            done: ["Story 6", "Story 7", "Story 8", "Story 9"]
        },
        question: "A coluna 'Ready for Dev' (Limite: 4) tem apenas 1 item. A coluna In Progress está tranquila. O que o Flow Master deve fazer agora?",
        options: [
            "Aguardar a próxima Sprint Planning.",
            "Puxar desenvolvedores para ajudar no Refinamento.",
            "Disparar o gatilho do Replenishment imediatamente."
        ],
        correctAnswer: 2,
        explanation: "Exato! O Replenishment não tem data marcada, ele ocorre por 'gatilho'. Como a fila principal de Dev baixou drasticamente do limite (fome), o time deve parar e fazer o Replenishment."
    },
    {
        title: "Cenário 2: O Gargalo no Meio do Fluxo",
        board: {
            upstream: ["Épico D"],
            refinement: ["Story 10", "Story 11"],
            readyForDev: ["Story 12", "Story 13", "Story 14", "Story 15"], // Limite 4 (Cheio)
            inProgress: ["Story 16", "Story 17", "Story 18", "Story 19", "Story 20"], // Limite 3 (Estourado)
            done: ["Story 21"]
        },
        question: "Ready for Dev está cheia (4/4). In Progress está lotada e bloqueada (5/3). Devemos fazer Replenishment para não faltar trabalho futuro?",
        options: [
            "Sim. A esteira não pode parar, o PO precisa priorizar os próximos.",
            "Não. O time deve fazer Swarming (mutirão) para esvaziar o 'In Progress'.",
            "Sim, mas puxando tarefas técnicas em vez de produto."
        ],
        correctAnswer: 1,
        explanation: "Stop starting, start finishing! Fazer Replenishment agora só vai empurrar mais cartões contra um gargalo que já está entupido."
    },
    {
        title: "Cenário 3: Fome de Upstream",
        board: {
            upstream: ["Ideia 1", "Ideia 2"],
            refinement: [], // Vazio!
            readyForDev: ["Story 22"], // Limite 4 (Quase vazio)
            inProgress: ["Story 23", "Story 24"],
            done: ["Story 25", "Story 26"]
        },
        question: "Ready for Dev está acabando e pedindo Replenishment. Porém, não há NADA na coluna de Refinamento pronto. O que fazer na cerimônia?",
        options: [
            "Puxar as Ideias direto do Upstream para o Dev e o time descobre codando.",
            "Acionar o Kiro e o PO urgentemente para Discovery e fatiamento. O Dev terá que focar em dívida técnica ou ajudar o PO por ora.",
            "Fazer o Replenishment normalmente e deixar a coluna vazia."
        ],
        correctAnswer: 1,
        explanation: "Sem itens prontos (DoR), puxar pro Dev é suicídio. A falta de Upstream exige que o fluxo inteiro se desloque para a esquerda temporariamente para reabastecer a 'fábrica'."
    }
];

let currentRepScenario = 0;

window.loadReplenishmentScenario = function() {
    const s = repScenarios[currentRepScenario];
    
    const titleEl = document.getElementById('rep-sim-title');
    if(!titleEl) return; // Se a página ainda não foi carregada
    
    // Atualizar título e pergunta
    titleEl.innerText = s.title;
    document.getElementById('rep-sim-question').innerText = s.question;
    document.getElementById('rep-sim-feedback').style.display = 'none';

    // Limpar colunas e preencher
    const cols = ['upstream', 'refinement', 'readyForDev', 'inProgress', 'done'];
    cols.forEach(col => {
        const el = document.getElementById('rep-col-' + col);
        if(el) {
            el.innerHTML = '';
            s.board[col].forEach(card => {
                el.innerHTML += '<div style="background:#fff; color:#0f172a; padding:8px; border-radius:4px; margin-bottom:8px; font-size:12px; font-weight:bold; box-shadow:0 1px 3px rgba(0,0,0,0.2); border-left:4px solid #38bdf8;">' + card + '</div>';
            });
        }
    });

    // Limpar e preencher botões de resposta
    const optsDiv = document.getElementById('rep-sim-options');
    optsDiv.innerHTML = '';
    s.options.forEach((opt, idx) => {
        const btn = document.createElement('button');
        btn.innerText = opt;
        btn.style.cssText = 'display:block; width:100%; text-align:left; padding:12px; margin-bottom:10px; background:#1e293b; color:#f8fafc; border:1px solid #334155; border-radius:6px; cursor:pointer; transition:all 0.2s; font-size:14px;';
        btn.onmouseover = () => btn.style.background = '#334155';
        btn.onmouseout = () => btn.style.background = '#1e293b';
        btn.onclick = () => window.checkReplenishmentAnswer(idx);
        optsDiv.appendChild(btn);
    });
};

window.checkReplenishmentAnswer = function(answerIdx) {
    const s = repScenarios[currentRepScenario];
    const fb = document.getElementById('rep-sim-feedback');
    fb.style.display = 'block';
    
    if(answerIdx === s.correctAnswer) {
        fb.style.background = '#064e3b';
        fb.style.borderColor = '#059669';
        fb.innerHTML = '<strong>✅ Correto!</strong><br><br>' + s.explanation;
    } else {
        fb.style.background = '#7f1d1d';
        fb.style.borderColor = '#dc2626';
        fb.innerHTML = '<strong>❌ Incorreto.</strong> Tente pensar de forma sistêmica. Lembre-se das regras de puxada do Kanban.';
    }
};

window.nextReplenishmentScenario = function() {
    currentRepScenario = (currentRepScenario + 1) % repScenarios.length;
    window.loadReplenishmentScenario();
};
