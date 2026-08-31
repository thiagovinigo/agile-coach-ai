document.addEventListener('DOMContentLoaded', () => {
    initWorkshopView();
});

function initWorkshopView() {
    const container = document.getElementById('workshop-view');
    if (!container) return;

    // Estrutura de dados do Workshop
    const workshopData = {
        "1. Introdução": [
            { 
                id: 'intro', 
                title: 'O Papel do Agilista', 
                icon: '🎯',
                content: `
                    <div style="text-align: center; padding: 20px;">
                        <h1 style="font-size: 2.5rem; color: #0f172a; margin-bottom: 20px;">O Papel do Agilista no Scrumban</h1>
                        <p style="font-size: 1.3rem; color: #475569; max-width: 800px; margin: 0 auto 40px; line-height: 1.6;">
                            No Scrumban, o Agilista (ou Flow Manager) não é apenas um facilitador de reuniões. 
                            Sua responsabilidade principal é a <strong>Otimização Sistêmica</strong> e a <strong>Gestão Visível do Fluxo de Valor</strong>.
                        </p>
                        <div style="display: flex; gap: 20px; justify-content: center; text-align: left; flex-wrap: wrap;">
                            <div style="background: #f8fafc; border-left: 4px solid #3b82f6; padding: 20px; border-radius: 8px; flex: 1; min-width: 250px; max-width: 300px;">
                                <h3 style="margin-top: 0; color: #1d4ed8;">1. Visibilidade</h3>
                                <p style="color: #334155; margin-bottom:0;">Tirar o trabalho oculto e expor as políticas do time no Board, garantindo que o sistema seja transparente para todos.</p>
                            </div>
                            <div style="background: #f8fafc; border-left: 4px solid #10b981; padding: 20px; border-radius: 8px; flex: 1; min-width: 250px; max-width: 300px;">
                                <h3 style="margin-top: 0; color: #047857;">2. Fluxo Contínuo</h3>
                                <p style="color: #334155; margin-bottom:0;">Focar em itens que estão parados (Wait Time), resolver dependências e gerenciar os limites de WIP.</p>
                            </div>
                            <div style="background: #f8fafc; border-left: 4px solid #f59e0b; padding: 20px; border-radius: 8px; flex: 1; min-width: 250px; max-width: 300px;">
                                <h3 style="margin-top: 0; color: #b45309;">3. Previsibilidade</h3>
                                <p style="color: #334155; margin-bottom:0;">Usar métricas de Lead Time e Throughput para estabelecer Acordos de Nível de Serviço (SLA) confiáveis com o cliente.</p>
                            </div>
                        </div>
                    </div>
                `
            }
        ],
        "2. Fundamentos": [
            { id: 's-agil', title: 'Manifesto Ágil e Valores', icon: '📜' },
            { id: 's-passo-agil', title: 'Passo a Passo da Mudança', icon: '👣' },
            { id: 's-scrum', title: 'Entendendo o Scrum', icon: '🏈' },
            { id: 's-kanban', title: 'O Método Kanban', icon: '🚦' }
        ],
        "3. Tópicos Scrumban": [
            { id: 's-oque', title: 'O que é Scrumban', icon: '📖' },
            { id: 's-vs', title: 'Scrum vs Kanban vs Scrumban', icon: '⚖️' },
            { id: 's-board', title: 'Board Completo', icon: '📋' },
            { id: 's-commitment', title: 'Commitment Point', icon: '🎯' },
            { id: 's-fluxo', title: 'Fluxo de Trabalho', icon: '🌊' },
            { id: 's-scrumban-simulacao', title: 'Simulação Pull Flow', icon: '🎮' },
            { id: 's-cadencias', title: 'Cadências', icon: '🔁' },
            { id: 's-wip', title: 'Limites de WIP', icon: '🚦' },
            { id: 's-daily', title: 'Daily', icon: '☀️' },
            { id: 's-demo', title: 'Demo', icon: '🎬' },
            { id: 's-retro', title: 'Retrospectiva', icon: '🔄' },
            { id: 's-bloqueios', title: 'Bloqueios', icon: '🚧' },
            { id: 's-cos', title: 'Classes de Serviço', icon: '🎯' },
            { id: 's-tradeoffs', title: 'Trade-offs', icon: '⚖️' },
            { id: 's-avancado', title: 'Itens Avançados', icon: '🔬' },
            { id: 's-quando', title: 'Quando Usar', icon: '🗓️' },
            { id: 's-anti', title: 'Anti-Padrões', icon: '⚠️' },
            { id: 's-scrumban-papeis', title: 'Papéis & Responsabilidades', icon: '👥' },
            { id: 's-scrumban-start', title: 'Primeiros 30 Dias', icon: '🌱' },
            { id: 's-scrumban-transicao', title: 'Guia de Transição', icon: '🔄' },
            { id: 's-scrumban-maturidade', title: 'Maturidade do Time', icon: '📈' }
        ],
        "4. Práticas do Time de Elite": [
            { id: 's-elite-politicas', title: 'Regras do Board', icon: '📜' },
            { id: 's-elite-flow', title: 'Touch Time vs Wait Time', icon: '⏱️' },
            { id: 's-elite-sla', title: 'SLA por Classe de Serviço', icon: '🎯' },
            { id: 's-elite-cadencias', title: 'Cadências do Scrumban', icon: '🔄' },
            { id: 's-elite-retro', title: 'A Retrospectiva de Elite', icon: '🕵️‍♂️' },
            { id: 's-elite-metricas', title: 'Métricas Avançadas', icon: '📈' },
            { id: 's-elite-board', title: 'O Board de Elite', icon: '🗂️' },
            { id: 's-elite-sim-func', title: 'Sim. Ref. Funcional', icon: '🎭' },
            { id: 's-elite-sim-tec', title: 'Sim. Ref. Técnico', icon: '⚙️' },
            { id: 's-elite-tamanho', title: 'Tamanho & Previsibilidade', icon: '📐' }
        ],
        "5. Conclusão": [
            {
                id: 'conclusao',
                title: 'Atuando na Trincheira',
                icon: '🏁',
                content: `
                    <div style="text-align: center; padding: 20px;">
                        <h1 style="font-size: 2.5rem; color: #0f172a; margin-bottom: 20px;">Sua Jornada Começa Agora</h1>
                        <p style="font-size: 1.3rem; color: #475569; max-width: 700px; margin: 0 auto 30px; line-height: 1.6;">
                            Gerir o fluxo é como ser um controlador de tráfego aéreo. Se você só olhar para um único avião (item), o aeroporto inteiro (sistema) para.
                        </p>
                        <div style="background: #fff; border: 2px solid #e2e8f0; border-radius: 12px; padding: 30px; max-width: 600px; margin: 0 auto; text-align: left; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                            <h3 style="color: #334155; margin-top: 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px;">Checklist do Agilista de Elite:</h3>
                            <ul style="color: #4a5568; line-height: 1.8; font-size: 1.1rem; padding-left: 20px; margin-bottom:0;">
                                <li>O Board reflete exatamente como o time trabalha hoje?</li>
                                <li>Os Limites de WIP estão sendo respeitados?</li>
                                <li>A idade dos itens (Aging) é discutida ativamente na Daily?</li>
                                <li>As políticas de Definition of Ready (DoR) bloqueiam itens ruins no Upstream?</li>
                                <li>A entrega é pautada por previsibilidade estatística ou "achismo"?</li>
                            </ul>
                        </div>
                    </div>
                `
            }
        ]
    };

    container.innerHTML = `
        <div style="height: 100vh; display: flex; align-items: center; justify-content: center; background: #0f172a;">
            <div style="text-align: center; color: #cbd5e1; font-size: 1.2rem;">⏳ Preparando Workshop...</div>
        </div>
    `;

    fetch('contexto/scrumban_guia.html')
        .then(response => response.text())
        .then(htmlStr => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(htmlStr, 'text/html');
            
            let extractedSections = {};

            Object.values(workshopData).forEach(group => {
                group.forEach(slide => {
                    if(!slide.content && slide.id) {
                        const el = doc.getElementById(slide.id);
                        if(el) {
                            extractedSections[slide.id] = el.innerHTML;
                        } else {
                            extractedSections[slide.id] = `<div style="padding: 20px; color: red; background: #fee2e2; border-radius: 8px;">⚠️ Conteúdo não encontrado para a seção: ${slide.id}</div>`;
                        }
                    }
                });
            });

            renderLayout(workshopData, extractedSections);
        })
        .catch(err => {
            container.innerHTML = `<div style="color:red; padding:40px;">Erro ao carregar o conteúdo do banco de dados de contexto: ${err}</div>`;
        });

    function renderLayout(data, extractedSections) {
        container.innerHTML = '';

        const layout = document.createElement('div');
        layout.className = 'kb-layout';

        // Sidebar
        const sidebar = document.createElement('div');
        sidebar.className = 'kb-sidebar';
        sidebar.style.overflowY = 'auto';

        const sidebarHeader = document.createElement('div');
        sidebarHeader.style.padding = '20px';
        sidebarHeader.style.borderBottom = '1px solid #edebe9';
        sidebarHeader.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size: 24px; color: #0078d4; cursor: pointer;" onclick="document.querySelector('a[href=\\'#agents\\']').click()">⬅️</span>
                <h2 style="margin: 0; color: #0f172a; font-size: 1.2rem;">Workshop: Gestor de Fluxo</h2>
            </div>
            <p style="font-size: 0.9rem; color: #64748b; margin: 0;">Domine o fluxo de valor e ferramentas do Scrumban.</p>
        `;
        sidebar.appendChild(sidebarHeader);

        // Content Area (Immersive Background mas rolando naturalmente)
        const contentArea = document.createElement('div');
        contentArea.className = 'kb-page-content';
        contentArea.style.overflowY = 'auto';
        contentArea.style.backgroundColor = '#0f172a';
        contentArea.style.padding = '40px 20px';

        layout.appendChild(sidebar);
        layout.appendChild(contentArea);
        container.appendChild(layout);

        const categories = Object.keys(data);
        let firstBtn = null;
        
        categories.forEach(category => {
            const catHeader = document.createElement('div');
            catHeader.className = 'kb-category-header';
            catHeader.innerText = category;
            catHeader.style.padding = '12px 15px';
            catHeader.style.fontWeight = 'bold';
            catHeader.style.color = '#323130';
            catHeader.style.backgroundColor = '#f3f2f1';
            catHeader.style.borderLeft = '4px solid #0078d4';
            catHeader.style.marginTop = '10px';
            sidebar.appendChild(catHeader);

            const linkList = document.createElement('div');
            linkList.className = 'kb-link-list';
            linkList.style.display = 'block';
            sidebar.appendChild(linkList);

            data[category].forEach((slide) => {
                const btn = document.createElement('div');
                btn.className = 'kb-nav-btn';
                btn.innerHTML = `
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:1.1rem;">${slide.icon || '📌'}</span>
                        <span style="font-weight:600; color:#323130; font-size:0.95rem;">${slide.title}</span>
                    </div>
                `;
                linkList.appendChild(btn);

                if (!firstBtn) firstBtn = btn;

                btn.onclick = () => {
                    document.querySelectorAll('#workshop-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');

                    let contentHtml = slide.content ? slide.content : extractedSections[slide.id];

                    let fullHtml = `
                        <div style="background: #fff; width: 100%; max-width: 900px; margin: 0 auto; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); overflow: hidden;">
                            <div style="padding: 40px 50px;">
                                ${!slide.content ? `
                                    <h2 style="margin-top: 0; padding-bottom: 15px; border-bottom: 2px solid #e2e8f0; color: #0f172a; margin-bottom: 30px; font-size: 2rem;">
                                        ${slide.icon} ${slide.title}
                                    </h2>
                                ` : ''}
                                
                                <div class="extracted-content" style="font-size: 1.05rem;">
                                    ${contentHtml}
                                </div>
                            </div>
                        </div>
                    `;

                    contentArea.style.opacity = '0';
                    contentArea.style.transform = 'translateY(10px)';
                    
                    setTimeout(() => {
                        contentArea.innerHTML = fullHtml;
                        contentArea.scrollTop = 0;
                        contentArea.style.transition = 'all 0.3s ease';
                        contentArea.style.opacity = '1';
                        contentArea.style.transform = 'translateY(0)';

                        if(slide.id === 's-elite-board') {
                            setTimeout(() => {
                                if (typeof window.showPolicy === 'function') {
                                    window.showPolicy('new');
                                } else if (document.querySelector('[data-col="new"]')) {
                                    document.querySelector('[data-col="new"]').click();
                                }
                            }, 200);
                        }
                    }, 100);
                };
            });
        });

        if (firstBtn) {
            firstBtn.click();
        }
    }
}
