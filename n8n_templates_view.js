document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('n8n-templates-view');
    if (!container) return;
    
    // n8nTemplatesData is loaded from n8n_templates_data.js
    if (typeof n8nTemplatesData === 'undefined') {
        container.innerHTML = '<p>Error loading templates data.</p>';
        return;
    }
    
    const categories = Object.keys(n8nTemplatesData).sort();
    let totalTemplates = 0;
    categories.forEach(c => totalTemplates += n8nTemplatesData[c].length);

    container.innerHTML = `
        <div class="card" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:2.5rem; box-shadow:0 4px 6px rgba(0,0,0,0.02); max-width: 1200px; margin: 20px auto;">
            <div style="text-transform: uppercase; font-size: 0.85rem; color: #ea580c; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">⚙️ Automação</div>
            <h3 style="margin-bottom:1.2rem; color:#1a202c; font-size:2rem; border-bottom:1px solid #eee; padding-bottom: 1rem;">Templates n8n Flowgrammers</h3>
            
            <div style="display: flex; gap: 2rem; margin-bottom: 2rem; align-items: flex-start; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <p style="color:#4a5568; font-size:1.15rem; line-height:1.7;">
                        O maior acervo de automações n8n e agentes de IA do Brasil. Total de <strong>${totalTemplates} templates</strong> categorizados.
                        Baixe o <code>.json</code> e importe diretamente no seu workspace do n8n.
                    </p>
                </div>
                
                <div style="flex: 1; min-width: 350px; background:#fff7ed; border-left:4px solid #ea580c; padding:1.5rem; border-radius:8px;">
                    <h4 style="margin-top:0; color:#ea580c; margin-bottom:1rem; font-size:1.1rem;">🚀 Como Utilizar?</h4>
                    <ul style="margin:0; padding-left:20px; color:#334155; font-size:0.95rem; line-height:1.6;">
                        <li style="margin-bottom:8px;">Baixe o arquivo <code>.json</code> do fluxo desejado clicando no botão.</li>
                        <li style="margin-bottom:8px;">Acesse o seu n8n e no menu superior escolha <strong>Import from File...</strong></li>
                        <li style="margin-bottom:8px;">Adicione suas credenciais (OpenAI, WhatsApp, etc) nos nós amarelos.</li>
                    </ul>
                </div>
            </div>

            <div style="margin-bottom: 20px;">
                <input type="text" id="n8n-search" placeholder="🔍 Buscar template (ex: RAG, WhatsApp, Lead...)" style="width: 100%; padding: 12px 20px; font-size: 1.1rem; border: 2px solid #e2e8f0; border-radius: 8px; outline: none;">
            </div>
            
            <div id="n8n-catalog-render"></div>
        </div>
    `;

    const renderCatalog = (searchQuery = '') => {
        const renderTarget = document.getElementById('n8n-catalog-render');
        if (!renderTarget) return;

        let html = '';
        
        categories.forEach(cat => {
            let items = n8nTemplatesData[cat];
            if (searchQuery) {
                const q = searchQuery.toLowerCase();
                items = items.filter(t => t.title.toLowerCase().includes(q));
            }

            if (items.length === 0) return;

            html += `
                <div class="n8n-category" style="margin-bottom: 30px;">
                    <h4 style="margin-top: 2rem; margin-bottom: 1.2rem; font-size: 1.3rem; color: #2d3748; border-bottom: 2px solid #f1f5f9; padding-bottom: 0.5rem; display: flex; align-items: center; gap: 8px;">
                        <span style="background: #f1f5f9; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; color: #64748b;">${items.length}</span> ${cat}
                    </h4>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px;">
                        ${items.map(t => `
                            <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; background: #fff; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.02); display: flex; flex-direction: column; justify-content: space-between;">
                                <h5 style="margin-top: 0; margin-bottom: 15px; color: #1e293b; font-size: 0.95rem; line-height: 1.4; word-break: break-word;">${t.title}</h5>
                                
                                <div>
                                    <a href="${t.path}" download="${t.file}" style="display: block; width: 100%; box-sizing: border-box; text-align:center; background-color: #ea580c; color: #fff; padding: 8px 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.85rem; transition: background 0.2s;">
                                        ⬇️ Baixar (.json)
                                    </a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        });
        
        if (!html && searchQuery) {
            html = '<p style="text-align:center; color:#64748b; padding: 40px;">Nenhum template encontrado para a busca.</p>';
        }

        renderTarget.innerHTML = html;
    };

    renderCatalog();

    const searchInput = document.getElementById('n8n-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            renderCatalog(e.target.value);
        });
    }
});
