document.addEventListener('DOMContentLoaded', () => {
    initFacilitadorDinamicasView();
});

function initFacilitadorDinamicasView() {
    const container = document.getElementById('facilitador-dinamicas-view');
    if(!container) return;

    if (typeof facilitadorDinamicasData === 'undefined') {
        container.innerHTML = '<p style="padding:20px;">Erro: Dados não carregados.</p>';
        return;
    }
    const dinamicasData = facilitadorDinamicasData;

    container.innerHTML = '';
    
    // Header
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.innerHTML = `
        <div style="text-transform: uppercase; font-size: 0.85rem; color: #f97316; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">📖 Playbook de Agilidade</div>
        <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px; font-size: 1.8rem;">Material do Facilitador: Dinâmicas</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            Guias de bolso para Agile Coaches e Scrum Masters. Baseado em metodologias ágeis e best-sellers como <strong>Lean Inception</strong> e <strong>Fun Retrospectives</strong> de Paulo Caroli.
        </p>
    `;
    container.appendChild(introHeader);

    // Layout
    const layout = document.createElement('div');
    layout.className = 'kb-layout';

    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.overflowY = 'auto';

    const searchBox = document.createElement('div');
    searchBox.style.padding = '15px';
    searchBox.style.borderBottom = '1px solid #edebe9';
    searchBox.innerHTML = `<input type="text" id="dinamicas-search" placeholder="🔍 Buscar dinâmica..." style="width:100%; padding:8px 12px; border:1px solid #ccc; border-radius:4px; outline:none;">`;
    sidebar.appendChild(searchBox);

    const navContainer = document.createElement('div');
    sidebar.appendChild(navContainer);

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';
    contentArea.style.padding = '30px';
    contentArea.style.background = '#f8fafc';

    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    container.appendChild(layout);

    const categories = Object.keys(dinamicasData);
    let firstBtn = null;

    function renderSidebar(query = '') {
        navContainer.innerHTML = '';
        firstBtn = null;

        categories.forEach(category => {
            const dinList = dinamicasData[category];
            const filtered = query 
                ? dinList.filter(d => d.title.toLowerCase().includes(query.toLowerCase()) || category.toLowerCase().includes(query.toLowerCase()))
                : dinList;

            if (filtered.length === 0) return;

            const catHeader = document.createElement('div');
            catHeader.className = 'kb-category-header';
            catHeader.innerText = `${category} (${filtered.length})`;
            catHeader.style.padding = '12px 15px';
            catHeader.style.fontWeight = 'bold';
            catHeader.style.color = '#323130';
            catHeader.style.backgroundColor = '#f3f2f1';
            catHeader.style.borderLeft = '4px solid #f97316';
            catHeader.style.cursor = 'pointer';
            catHeader.style.marginTop = '10px';
            navContainer.appendChild(catHeader);

            const linkList = document.createElement('div');
            linkList.className = 'kb-link-list';
            linkList.style.display = query ? 'block' : 'none';
            navContainer.appendChild(linkList);

            catHeader.onclick = () => {
                linkList.style.display = linkList.style.display === 'none' ? 'block' : 'none';
            };

            filtered.forEach((din) => {
                const btn = document.createElement('div');
                btn.className = 'kb-nav-btn';
                btn.innerHTML = `
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:1.1rem;">${din.icon || '📌'}</span>
                        <span style="font-weight:600; color:#323130; font-size:0.95rem;">${din.title}</span>
                    </div>
                `;
                linkList.appendChild(btn);

                if(!firstBtn) firstBtn = btn;

                btn.onclick = () => {
                    document.querySelectorAll('#facilitador-dinamicas-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');

                    const contentHtml = `
    <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); max-width: 900px; margin: 0 auto;">
        
        <div style="background: linear-gradient(to right, #0f172a, #1e293b); padding: 30px; color: white;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="font-size: 3rem; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 12px;">${din.icon || '📌'}</span>
                <div>
                    <span style="color: #f97316; font-weight: bold; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px;">${category}</span>
                    <h2 style="margin: 5px 0 0 0; font-size: 2rem;">${din.title}</h2>
                </div>
            </div>
        </div>

        <div style="padding: 30px;">
            
            <!-- Material Necessário -->
            <div style="margin-bottom: 25px; background: #e0f2fe; padding: 15px 20px; border-left: 4px solid #0ea5e9; border-radius: 0 8px 8px 0;">
                <h4 style="color: #0369a1; font-size: 1.1rem; margin-top: 0; margin-bottom: 8px; display:flex; align-items:center; gap:8px;">
                    <span>🛠️</span> Material Necessário / Preparação
                </h4>
                <p style="color: #0c4a6e; font-size: 1.05rem; line-height: 1.6; margin: 0;">
                    ${din.materials || "Material padrão: Post-its, canetas e quadro branco (ou board virtual no Miro/Mural)."}
                </p>
            </div>

            <!-- Imagem Ilustrativa (Placeholder / SVG Dinâmico) -->
            <div style="margin-bottom: 25px; text-align: center; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 20px; background: #f8fafc; position: relative;">
                <h4 style="color: #64748b; font-size: 1.1rem; margin-top: 0; margin-bottom: 15px; display:flex; align-items:center; justify-content:center; gap:8px;">
                    <span>📸</span> Ilustração do Quadro / Execução
                </h4>
                <div style="background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); width: 100%; height: 250px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-direction: column; color: #94a3b8; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 10px;"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                    <span style="font-weight: 600; letter-spacing: 0.5px;">Espaço reservado para o print do seu board Miro/Mural</span>
                    <span style="font-size: 0.85rem; margin-top: 5px;">Salve a imagem como "dinamica_${din.title.replace(/[^a-zA-Z0-9]/g, '')}.png" para substituir</span>
                </div>
            </div>

            <!-- Detalhamento -->
            <div style="margin-bottom: 25px;">
                <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
                    <span>📝</span> Detalhamento
                </h4>
                <p style="color: #475569; font-size: 1.05rem; line-height: 1.6; margin: 0;">
                    ${din.detail}
                </p>
            </div>

            <!-- Exemplos -->
            <div style="margin-bottom: 25px; background: #fff7ed; padding: 15px 20px; border-left: 4px solid #f97316; border-radius: 0 8px 8px 0;">
                <h4 style="color: #9a3412; font-size: 1.1rem; margin-top: 0; margin-bottom: 8px; display:flex; align-items:center; gap:8px;">
                    <span>💡</span> Exemplo de Cenário
                </h4>
                <p style="color: #7c2d12; font-size: 1.05rem; line-height: 1.6; margin: 0; font-style: italic;">
                    "${din.examples}"
                </p>
            </div>

            <!-- A Prática Executada -->
            <div style="margin-bottom: 25px;">
                <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 15px; display:flex; align-items:center; gap:8px;">
                    <span>⚙️</span> Passo a Passo da Execução
                </h4>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px;">
                    <div style="color: #334155; font-size: 1.05rem; line-height: 1.7; margin-left: 10px;" class="din-execution-list">
                        ${din.execution}
                    </div>
                </div>
            </div>

            <!-- Resultado Final Esperado -->
            <div style="margin-bottom: 10px;">
                <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
                    <span>🏆</span> Resultado Final Esperado
                </h4>
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 15px 20px; border-radius: 8px;">
                    <p style="color: #166534; font-size: 1.1rem; line-height: 1.6; margin: 0; font-weight: 500;">
                        ${din.result}
                    </p>
                </div>
            </div>

        </div>
    </div>
                    `;

                    contentArea.innerHTML = contentHtml;

                    const styleId = 'dinamicas-style';
                    if (!document.getElementById(styleId)) {
                        const style = document.createElement('style');
                        style.id = styleId;
                        style.innerHTML = `
                            .din-execution-list ol { padding-left: 20px; margin: 0; }
                            .din-execution-list li { margin-bottom: 12px; }
                            .din-execution-list li strong { color: #0f172a; }
                        `;
                        document.head.appendChild(style);
                    }
                };
            });
        });

        if (firstBtn && query === '') {
            navContainer.querySelector('.kb-category-header').click();
            firstBtn.click();
        } else if (firstBtn) {
            firstBtn.click();
        } else {
            contentArea.innerHTML = '<div style="padding: 40px; text-align: center; color: #64748b;">Nenhuma dinâmica encontrada.</div>';
        }
    }

    renderSidebar();

    setTimeout(() => {
        const input = document.getElementById('dinamicas-search');
        if(input) {
            input.addEventListener('input', (e) => {
                renderSidebar(e.target.value);
            });
        }
    }, 100);
}
