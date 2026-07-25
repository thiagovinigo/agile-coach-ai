document.addEventListener('DOMContentLoaded', () => {
    initDiscoveryView();
});

function initDiscoveryView() {
    const container = document.getElementById('discovery-view');
    if(!container || typeof discoveryData === 'undefined') return;

    container.innerHTML = '';
    
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.style.marginBottom = '20px';
    introHeader.innerHTML = `
        <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px;">🔍 Product Discovery</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            Base de conhecimento teórica sobre metodologias e frameworks ágeis de Descoberta de Produto.
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
    container.appendChild(layout);

    let firstBtn = null;

    if (discoveryData["Product Discovery"]) {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #14b8a6'; // Teal color
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        catHeader.style.marginBottom = '2px';
        catHeader.style.borderRadius = '0 6px 6px 0';
        catHeader.innerText = 'Tópicos de Discovery';
        sidebar.appendChild(catHeader);

        const skillsContainer = document.createElement('div');
        skillsContainer.className = 'kb-skills-list';
        skillsContainer.style.display = 'block';
        sidebar.appendChild(skillsContainer);

        discoveryData["Product Discovery"].forEach(item => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.innerText = "📄 " + item.title;
            
            btn.onclick = async () => {
                document.querySelectorAll('#discovery-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                contentArea.innerHTML = '<div style="text-align:center; padding:40px; color:#64748b;">⏳ Carregando ' + item.title + '...</div>';
                
                try {
                    const response = await fetch(item.path + '?v=' + new Date().getTime());
                    if(!response.ok) throw new Error('Falha ao carregar');
                    const text = await response.text();
                    
                    let parsed = text
                        .replace(/^### (.*$)/gim, '<h3 style="margin-top:20px; color:#0f172a;">$1</h3>')
                        .replace(/^## (.*$)/gim, '<h2 style="margin-top:25px; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:5px;">$1</h2>')
                        .replace(/^# (.*$)/gim, '<h1 style="color:#0f172a;">$1</h1>')
                        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
                        .replace(/\*(.*?)\*/gim, '<em>$1</em>')
                        .replace(/`(.*?)`/gim, '<code style="background:#e2e8f0; padding:2px 4px; border-radius:3px; font-family:monospace; color:#ef4444;">$1</code>')
                        .replace(/\n\n/gim, '<br><br>');

                    const headerCard = `
<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 30px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <h3 style="margin-top:0; color:#0f172a; display:flex; align-items:center; justify-content:space-between; gap:8px; font-size: 1.1rem; margin-bottom: 15px;">
        <span><span>📚</span> Resumo Rápido</span>
        ${window.favoritesManager ? window.favoritesManager.renderButton(item.id || item.title, item.title, 'Product Discovery', item.path) : ''}
    </h3>
    <div style="background:#f1f5f9; border:1px solid #cbd5e1; padding:8px 12px; border-radius:4px; font-family:monospace; font-size:0.85rem; color:#475569; word-break:break-all; margin-bottom: 20px;">
        📂 <strong>Repositório:</strong> ${item.path}
    </div>
    <div style="display: flex; gap: 10px; margin-bottom: 20px;">
        <a href="${item.path}" download="${item.title}.md" style="display:inline-block; background-color:#14b8a6; color:#fff; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:0.95rem; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            ⬇️ Baixar Arquivo da Skill
        </a>
        <a href="${item.path}" target="_blank" style="display:inline-block; background-color:#f8fafc; color:#334155; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; border: 1px solid #cbd5e1; font-size:0.95rem;">
            👀 Ver Arquivo
        </a>
    </div>
    <h3 style="margin-top:0; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>🧠</span> O que é?
    </h3>
    <p style="margin-top:5px; color:#475569; font-size: 0.95rem;">
        O módulo <strong>${item.title}</strong> é um guia conceitual e prático focado em Product Discovery, pesquisa com usuários e validação de ideias.
    </p>

    <h3 style="margin-top:20px; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>⏱️</span> Quando usar?
    </h3>
    <p style="margin-top:5px; color:#475569; font-size: 0.95rem; font-weight: 500;">
        ${item.description}
    </p>

    <h3 style="margin-top:20px; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>🛠️</span> Como usar?
    </h3>
    <ul style="margin-top:5px; color:#475569; font-size: 0.95rem; padding-left: 20px; margin-bottom:0;">
        <li>No seu terminal ou Claude Code, utilize este guia como referência ou contexto na tomada de decisões.</li>
        <li><strong>Exemplo:</strong> <code>/read ${item.path}</code> seguido pelo problema a ser analisado no discovery.</li>
    </ul>
</div>
`;

                    contentArea.innerHTML = `<div style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color:#333; line-height:1.6;">` + headerCard + parsed + `</div>`;
                } catch(e) {
                    contentArea.innerHTML = '<div style="color:#ef4444; padding:20px;">Erro ao carregar o documento: ' + e.message + '</div>';
                }
            };
            
            skillsContainer.appendChild(btn);
            if(!firstBtn) firstBtn = btn;
        });

        // Click the first button on load
        if(firstBtn) {
            setTimeout(() => {
                firstBtn.click();
            }, 100);
        }
    }
}
