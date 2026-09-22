document.addEventListener('DOMContentLoaded', () => {
    initN8nTemplatesView();
});

function initN8nTemplatesView() {
    const container = document.getElementById('n8n-templates-view');
    if(!container || typeof n8nTemplatesData === 'undefined') return;

    container.innerHTML = '';
    
    let totalTemplates = 0;
    const categories = Object.keys(n8nTemplatesData).sort();
    categories.forEach(c => totalTemplates += n8nTemplatesData[c].length);
    
    // Header
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.innerHTML = `
        <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px; display:flex; align-items:center; gap:10px;">
            ⚙️ Templates n8n Flowgrammers 
            <span style="background-color:#ef4444; color:white; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:bold;">🆕 NOVO!</span>
        </h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            O maior acervo de automações do Brasil! São <strong>${totalTemplates} templates</strong> prontos para você baixar e importar no seu workspace do n8n.
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
    searchBox.innerHTML = `<input type="text" id="n8n-sidebar-search" placeholder="🔍 Buscar template..." style="width:100%; padding:8px 12px; border:1px solid #ccc; border-radius:4px; outline:none;">`;
    sidebar.appendChild(searchBox);

    const navContainer = document.createElement('div');
    sidebar.appendChild(navContainer);

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';

    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    container.appendChild(layout);

    let firstBtn = null;

    function renderSidebar(query = '') {
        navContainer.innerHTML = '';
        firstBtn = null;
        
        categories.forEach(category => {
            const skillsList = n8nTemplatesData[category];
            const filtered = query 
                ? skillsList.filter(s => s.title.toLowerCase().includes(query.toLowerCase()) || category.toLowerCase().includes(query.toLowerCase()))
                : skillsList;
                
            if (filtered.length === 0) return;

            const catHeader = document.createElement('div');
            catHeader.className = 'kb-category-header';
            catHeader.innerText = `${category} (${filtered.length})`;
            catHeader.style.padding = '12px 15px';
            catHeader.style.fontWeight = 'bold';
            catHeader.style.color = '#323130';
            catHeader.style.backgroundColor = '#f3f2f1';
            catHeader.style.borderLeft = '4px solid #ea580c';
            catHeader.style.cursor = 'pointer';
            catHeader.style.marginTop = '10px';
            navContainer.appendChild(catHeader);

            const linkList = document.createElement('div');
            linkList.className = 'kb-link-list';
            linkList.style.display = query ? 'block' : 'none'; // open if searching
            navContainer.appendChild(linkList);
            
            catHeader.onclick = () => {
                linkList.style.display = linkList.style.display === 'none' ? 'block' : 'none';
            };

            filtered.forEach((skill) => {
                const btn = document.createElement('div');
                btn.className = 'kb-nav-btn';
                btn.innerHTML = `
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:1.1rem;">⚡</span>
                        <span style="font-weight:600; color:#323130; font-size:0.95rem; word-break: break-word;">${skill.title}</span>
                    </div>
                `;
                linkList.appendChild(btn);

                if(!firstBtn) firstBtn = btn;

                btn.onclick = () => {
                    document.querySelectorAll('#n8n-templates-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');

                    const headerCard = `
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 30px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h3 style="margin-top:0; color:#0f172a; display:flex; align-items:center; justify-content:space-between; gap:8px; font-size: 1.1rem; margin-bottom: 15px;">
            <span><span>📦</span> ${skill.title}</span>
            ${window.favoritesManager ? window.favoritesManager.renderButton(skill.file, skill.title, 'n8n Templates', skill.path) : ''}
        </h3>
        <div style="display:flex; gap:10px; margin-bottom:15px;">
            <span style="background-color:#ea580c; color:#fff; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:bold;">${category}</span>
            <span style="background-color:#e2e8f0; color:#334155; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:bold;">${skill.file}</span>
        </div>
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <a href="${skill.path}" download="${skill.file}" style="display:inline-block; background-color:#ea580c; color:#fff; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:0.95rem; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                ⬇️ Baixar Template (.json)
            </a>
        </div>
        
        <h4 style="margin-top:0; color:#ea580c; margin-bottom:10px; font-size:1rem;">🚀 Como Utilizar?</h4>
        <ul style="margin:0; padding-left:20px; color:#334155; font-size:0.95rem; line-height:1.6;">
            <li style="margin-bottom:8px;">Baixe o arquivo clicando no botão acima.</li>
            <li style="margin-bottom:8px;">No seu painel do n8n, clique em <strong>Import from File...</strong></li>
            <li style="margin-bottom:8px;">Adicione suas credenciais e ajuste os webhooks!</li>
        </ul>
    </div>
                    `;

                    // We fetch the JSON to show a preview if possible
                    fetch(skill.path).then(r => r.text()).then(text => {
                        let preview = text;
                        if(text.length > 5000) {
                            preview = text.substring(0, 5000) + 'nn... (ARQUIVO TRUNCADO PARA VISUALIZAÇÃO) ...';
                        }
                        
                        const mdContent = `
<div class="markdown-body">
    <h4>Preview do Código (JSON)</h4>
    <pre style="max-height: 400px; overflow: auto; background: #f6f8fa; padding: 16px; border-radius: 6px;"><code class="language-json">${preview.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>
</div>`;
                        contentArea.innerHTML = headerCard + mdContent;
                    }).catch(err => {
                        contentArea.innerHTML = headerCard + '<p>Erro ao carregar preview do arquivo.</p>';
                    });
                };
            });
        });
        
        if (firstBtn && query === '') {
            // open the first category
            navContainer.querySelector('.kb-category-header').click();
            firstBtn.click();
        } else if (firstBtn) {
            firstBtn.click();
        } else {
            contentArea.innerHTML = '<div style="padding: 40px; text-align: center; color: #64748b;">Nenhum template encontrado.</div>';
        }
    }

    renderSidebar();

    setTimeout(() => {
        const input = document.getElementById('n8n-sidebar-search');
        if(input) {
            input.addEventListener('input', (e) => {
                renderSidebar(e.target.value);
            });
        }
    }, 100);
}
