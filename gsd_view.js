document.addEventListener('DOMContentLoaded', () => {
    initGsdView();
});

function initGsdView() {
    const container = document.getElementById('gsd-view');
    if(!container || typeof gsdData === 'undefined') return;

    container.innerHTML = '';
    
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.style.marginBottom = '20px';
    introHeader.innerHTML = `
        <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px;">🎯 Get-Shit-Done (GSD) Agents</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            Exército de agentes altamente especializados e focados em execução do framework GSD.
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

    if (gsdData['GSD Agents']) {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #10b981';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        catHeader.style.marginBottom = '2px';
        catHeader.style.borderRadius = '0 6px 6px 0';
        catHeader.innerText = 'Agentes GSD';
        sidebar.appendChild(catHeader);

        const skillsContainer = document.createElement('div');
        skillsContainer.className = 'kb-skills-list';
        skillsContainer.style.display = 'block';
        sidebar.appendChild(skillsContainer);

        gsdData['GSD Agents'].forEach(agent => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.innerText = "🎯 " + agent.title;
            
            btn.onclick = async () => {
                document.querySelectorAll('#gsd-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                contentArea.innerHTML = '<div style="text-align:center; padding:40px; color:#64748b;">⏳ Carregando ' + agent.title + '...</div>';
                
                try {
                    const response = await fetch(agent.path + '?v=' + new Date().getTime());
                    if(!response.ok) throw new Error('Falha ao carregar');
                    const text = await response.text();
                    
                    let parsed = text
                        .replace(/---[\s\S]*?---/, '')
                        .replace(/^### (.*$)/gim, '<h3 style="margin-top:20px; color:#0f172a;">$1</h3>')
                        .replace(/^## (.*$)/gim, '<h2 style="margin-top:25px; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:5px;">$1</h2>')
                        .replace(/^# (.*$)/gim, '<h1 style="color:#0f172a;">$1</h1>')
                        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
                        .replace(/\*(.*?)\*/gim, '<em>$1</em>')
                        .replace(/`(.*?)`/gim, '<code style="background:#e2e8f0; padding:2px 4px; border-radius:3px; font-family:monospace; color:#ef4444;">$1</code>')
                        .replace(/\n/gim, '<br>');
                        
                    parsed = parsed.replace(/<br>```[\s\S]*?```<br>/gim, function(match) {
                        return match.replace(/<br>/gim, '\n');
                    });
                    parsed = parsed.replace(/```(.*?)[\n\r]([\s\S]*?)```/gim, '<pre style="background:#1e293b; color:#e2e8f0; padding:15px; border-radius:6px; overflow-x:auto; font-family:monospace; margin:15px 0;"><code>$2</code></pre>');

                    contentArea.innerHTML = `<div style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color:#333; line-height:1.6;">` + parsed + `</div>`;
                } catch(e) {
                    contentArea.innerHTML = '<div style="color:#ef4444; padding:20px;">Erro ao carregar o documento: ' + e.message + '</div>';
                }
            };
            
            skillsContainer.appendChild(btn);
            if(!firstBtn) firstBtn = btn;
        });
    }

    if(firstBtn) firstBtn.click();
}

window.initGsdView = initGsdView;
