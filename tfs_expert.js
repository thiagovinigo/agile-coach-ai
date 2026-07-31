document.addEventListener('DOMContentLoaded', () => {
    initTfsView();
});

function initTfsView() {
    const container = document.getElementById('tfs-view');
    if(!container || typeof tfsData === 'undefined') return;

    container.innerHTML = '';
    
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.style.marginBottom = '20px';
    introHeader.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px;">⚙️ Especialista TFS / Azure Boards</h2>
                <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
                    Guia definitivo de Configuração e Estruturação do Azure Boards. Explore o fluxo de Upstream/Downstream, automações de Epic/Feature e regras customizadas.
                </p>
            </div>
            <button class="action-btn" style="background:#0f172a; color:white; border:none; padding:8px 16px; border-radius:6px; cursor:pointer;" onclick="alert('Dúvidas avançadas? Em breve, o bot especialista estará disponível para tirar dúvidas de automação no Azure DevOps!')">💬 Perguntar ao Especialista</button>
        </div>
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

    Object.keys(tfsData).forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #3b82f6'; // Blue color
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        catHeader.style.marginBottom = '2px';
        catHeader.style.borderRadius = '0 6px 6px 0';
        catHeader.innerText = category;
        sidebar.appendChild(catHeader);

        const skillsContainer = document.createElement('div');
        skillsContainer.className = 'kb-skills-list';
        skillsContainer.style.display = 'block';
        sidebar.appendChild(skillsContainer);

        tfsData[category].forEach(item => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">📄</span>
                    <span style="font-weight:600; color:#323130; font-size:0.95rem;">${item.title}</span>
                </div>
                <div style="font-size:0.8rem; color:#605e5c; margin-top:4px; line-height:1.3; white-space:normal;">
                    ${item.description || 'Nenhuma descrição fornecida.'}
                </div>
            `;
            
            btn.onclick = async () => {
                document.querySelectorAll('#tfs-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
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
                        .replace(/`(.*?)`/gim, '<code style="background:#f1f5f9; padding:2px 4px; border-radius:3px; font-family:monospace; color:#3b82f6;">$1</code>')
                        .replace(/!\[([^\]]+)\]\(([^)]+)\)/gim, '<img src="$2" alt="$1" style="max-width:100%; border:1px solid #e2e8f0; border-radius:6px; margin:20px 0;">')
                        .replace(/\|(.*)\|/gim, (match) => {
                            const row = match.split('|').filter(c => c).map(c => `<td style="padding:8px; border-bottom:1px solid #e2e8f0; border-right:1px solid #e2e8f0;">${c.trim()}</td>`).join('');
                            return `<tr style="border:1px solid #e2e8f0;">${row}</tr>`;
                        })
                        .replace(/\n\n/gim, '<br><br>');

                    // Wrap tables properly
                    parsed = parsed.replace(/(<tr.*?>.*?<\/tr>)+/gim, (match) => {
                        // Very simple markdown table parsing (to prevent multiple wraps and fix headers)
                        let fixedMatch = match.replace(/<td(.*?)>---.*?<\/td>/gim, '');
                        // Convert first row to th
                        let rowCount = 0;
                        fixedMatch = fixedMatch.replace(/<td(.*?)>(.*?)<\/td>/gim, (m, attrs, content) => {
                            if(rowCount === 0) return `<th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; font-weight:bold; color:#0f172a; text-align:left;">${content}</th>`;
                            return `<td${attrs}>${content}</td>`;
                        });
                        fixedMatch = fixedMatch.replace(/<\/tr>/gi, '</tr>###NEXT###');
                        const parts = fixedMatch.split('###NEXT###');
                        parts[0] = parts[0].replace(/<td/g, '<th').replace(/<\/td>/g, '</th>'); // Force first row headers
                        
                        return `<div style="overflow-x:auto; margin-bottom:20px;"><table style="width:100%; border-collapse:collapse; border:1px solid #e2e8f0; font-size:0.9rem;">${fixedMatch.replace(/###NEXT###/g, '')}</table></div>`;
                    });

                    // Add markdown blockquotes as tips
                    parsed = parsed.replace(/&gt; \[\!TIP\]<br><br>(.*?)(<br><br>|$)/gim, '<div style="background:#f0fdfa; border-left:4px solid #14b8a6; padding:15px; margin:15px 0; border-radius:4px;"><strong style="color:#0f766e;">💡 Dica:</strong><br>$1</div>$2');
                    parsed = parsed.replace(/&gt; \[\!WARNING\]<br><br>(.*?)(<br><br>|$)/gim, '<div style="background:#fffbeb; border-left:4px solid #f59e0b; padding:15px; margin:15px 0; border-radius:4px;"><strong style="color:#b45309;">⚠️ Atenção:</strong><br>$1</div>$2');
                    parsed = parsed.replace(/&gt; \[\!NOTE\]<br><br>(.*?)(<br><br>|$)/gim, '<div style="background:#eff6ff; border-left:4px solid #3b82f6; padding:15px; margin:15px 0; border-radius:4px;"><strong style="color:#1d4ed8;">ℹ️ Nota:</strong><br>$1</div>$2');

                    const headerCard = `
<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 30px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <h3 style="margin-top:0; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>📘</span> Resumo do Tópico
    </h3>
    <p style="margin-top:5px; color:#475569; font-size: 0.95rem; font-weight: 500;">
        ${item.description}
    </p>
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
    });

    // Click the first button on load
    if(firstBtn) {
        setTimeout(() => {
            firstBtn.click();
        }, 100);
    }
}
