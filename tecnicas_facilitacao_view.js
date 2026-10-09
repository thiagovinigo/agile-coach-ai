document.addEventListener('DOMContentLoaded', () => {
    initTecnicasFacilitacaoView();
});

function initTecnicasFacilitacaoView() {
    const container = document.getElementById('tecnicas-facilitacao-view');
    if(!container) return;

    if (typeof tecnicasData === 'undefined') {
        container.innerHTML = '<p style="padding:20px;">Erro: Dados das técnicas não carregados.</p>';
        return;
    }

    container.innerHTML = '';
    
    // Header
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.innerHTML = `
        <div style="text-transform: uppercase; font-size: 0.85rem; color: #8b5cf6; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">🧠 Comportamento e Liderança</div>
        <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px; font-size: 1.8rem;">Técnicas de Facilitação</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            Diferente das "Dinâmicas" (que são jogos e atividades), as <strong>Técnicas de Facilitação</strong> são as habilidades comportamentais, posturas e micro-ferramentas que o Agile Coach usa para guiar reuniões, mediar conflitos e extrair o melhor das pessoas.
        </p>
    `;
    container.appendChild(introHeader);

    // Layout
    const layout = document.createElement('div');
    layout.className = 'kb-layout';

    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';
    contentArea.style.padding = '30px';
    contentArea.style.background = '#f8fafc';

    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    container.appendChild(layout);

    const categories = Object.keys(tecnicasData);
    let firstBtn = null;

    categories.forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #8b5cf6';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const linkList = document.createElement('div');
        linkList.className = 'kb-link-list';
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        const dinList = tecnicasData[category];
        dinList.forEach((din) => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">${din.icon}</span>
                    <span style="font-weight:600; color:#323130; font-size:0.95rem;">${din.title}</span>
                </div>
            `;
            linkList.appendChild(btn);

            if(!firstBtn) firstBtn = btn;

            btn.onclick = () => {
                document.querySelectorAll('#tecnicas-facilitacao-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const contentHtml = `
<div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); max-width: 900px; margin: 0 auto;">
    
    <div style="background: linear-gradient(to right, #2e1065, #4c1d95); padding: 30px; color: white;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-size: 3rem; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 12px;">${din.icon}</span>
            <div>
                <span style="color: #c4b5fd; font-weight: bold; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px;">${category}</span>
                <h2 style="margin: 5px 0 0 0; font-size: 2rem;">${din.title}</h2>
            </div>
        </div>
    </div>

    <div style="padding: 30px;">
        
        <!-- Detalhamento -->
        <div style="margin-bottom: 25px;">
            <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
                <span>📝</span> O que é a Técnica?
            </h4>
            <p style="color: #475569; font-size: 1.05rem; line-height: 1.6; margin: 0;">
                ${din.detail}
            </p>
        </div>

        <!-- Exemplos -->
        <div style="margin-bottom: 25px; background: #faf5ff; padding: 15px 20px; border-left: 4px solid #8b5cf6; border-radius: 0 8px 8px 0;">
            <h4 style="color: #5b21b6; font-size: 1.1rem; margin-top: 0; margin-bottom: 8px; display:flex; align-items:center; gap:8px;">
                <span>💡</span> Exemplo de Cenário
            </h4>
            <p style="color: #4c1d95; font-size: 1.05rem; line-height: 1.6; margin: 0; font-style: italic;">
                "${din.examples}"
            </p>
        </div>

        <!-- A Prática Executada -->
        <div style="margin-bottom: 25px;">
            <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 15px; display:flex; align-items:center; gap:8px;">
                <span>⚙️</span> Passo a Passo do Facilitador
            </h4>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px;">
                <div style="color: #334155; font-size: 1.05rem; line-height: 1.7; margin-left: 10px;" class="din-execution-list">
                    ${din.execution}
                </div>
            </div>
        </div>

            <!-- Canvas Visual da Técnica / Exemplo Real -->
            <div style="margin-bottom: 25px; text-align: center; border: 2px solid #e2e8f0; border-radius: 12px; padding: 20px; background: #f8fafc; position: relative;">
                <h4 style="color: #475569; font-size: 1.1rem; margin-top: 0; margin-bottom: 15px; display:flex; align-items:center; justify-content:center; gap:8px;">
                    <span>📸</span> Canvas Visual da Técnica / Exemplo Real
                </h4>
                ${din.board_html ? `
                    <div style="width: 100%; text-align: left; overflow-x: auto;">
                        ${din.board_html}
                    </div>
                ` : `
                    <div style="background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); width: 100%; height: 250px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-direction: column; color: #94a3b8; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 10px;"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                        <span style="font-weight: 600; letter-spacing: 0.5px;">Espaço reservado para o visual da técnica</span>
                    </div>
                `}
            </div>

        </div>
</div>
                `;

                contentArea.innerHTML = contentHtml;
            };
        });
    });

    if (firstBtn) {
        firstBtn.click();
    }
}
