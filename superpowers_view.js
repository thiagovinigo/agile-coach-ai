document.addEventListener('DOMContentLoaded', () => {
    initSuperpowersView();
});

function initSuperpowersView() {
    const container = document.getElementById('superpowers-view');
    if(!container || typeof superpowersData === 'undefined') return;

    let html = `
        <div class="hero-section" style="background: linear-gradient(135deg, #1e293b, #0f172a);">
            <h3>⚡ Superpowers (Agent Skills)</h3>
            <p>Diretrizes avançadas e métodos de engenharia contínua (Superpowers) projetados para Agentes Autônomos como Kiro e Claude Code.</p>
        </div>
        <div class="grid-cards">
    `;

    if (superpowersData.Superpowers) {
        superpowersData.Superpowers.forEach(skill => {
            html += `
                <div class="card" style="position:relative; border-left: 4px solid #f59e0b;">
                    <button onclick="openSuperpowerDoc('${skill.path}', '${skill.title}')" style="position:absolute; top:12px; right:12px; background:transparent; border:1px solid #c8c6c4; border-radius:50%; width:24px; height:24px; color:#605e5c; cursor:pointer; font-weight:bold; display:flex; justify-content:center; align-items:center;" title="Ver Documentação">?</button>
                    <div class="card-icon" style="background:#fef3c7; color:#d97706;">⚡</div>
                    <div class="card-title">${skill.title}</div>
                    <div class="card-desc">${skill.description || 'Estratégia de engenharia para Agentes Autônomos.'}</div>
                    <button class="card-action" style="background:var(--secondary); color:#fff; border:none; padding:8px 16px; border-radius:4px; font-weight:bold; cursor:pointer; margin-top:10px; width:100%; transition:background 0.2s;" onmouseover="this.style.background='#272727'" onmouseout="this.style.background='var(--secondary)'" onclick="openSuperpowerDoc('${skill.path}', '${skill.title}')">
                        📖 Ler Skill
                    </button>
                </div>
            `;
        });
    }

    html += `
        </div>
        
        <!-- Modal for Superpower Doc -->
        <div id="sp-doc-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:9999; justify-content:center; align-items:center;">
            <div style="background:#fff; width:90%; max-width:800px; height:90%; border-radius:12px; display:flex; flex-direction:column; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.5);">
                <div style="padding:15px 20px; background:#1e293b; color:#fff; display:flex; justify-content:space-between; align-items:center;">
                    <h3 id="sp-doc-title" style="margin:0; font-size:18px;">Skill Document</h3>
                    <button onclick="closeSuperpowerDoc()" style="background:none; border:none; color:#fff; font-size:24px; cursor:pointer;">&times;</button>
                </div>
                <div id="sp-doc-content" style="padding:20px; flex:1; overflow-y:auto; background:#f8fafc; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; color:#333; line-height:1.6;">
                    Carregando...
                </div>
            </div>
        </div>
    `;

    container.innerHTML = html;
}

window.openSuperpowerDoc = async function(path, title) {
    document.getElementById('sp-doc-modal').style.display = 'flex';
    document.getElementById('sp-doc-title').innerText = "⚡ " + title;
    const contentDiv = document.getElementById('sp-doc-content');
    contentDiv.innerHTML = '<div style="text-align:center; padding:40px; color:#64748b;">⏳ Carregando documento...</div>';

    try {
        const response = await fetch(path + '?v=' + new Date().getTime());
        if(!response.ok) throw new Error('Falha ao carregar o documento');
        const text = await response.text();
        
        // Simples conversão de markdown para HTML para não precisar importar biblioteca pesada
        let parsed = text
            .replace(/---[\s\S]*?---/, '') // remove frontmatter
            .replace(/^### (.*$)/gim, '<h3 style="margin-top:20px; color:#0f172a;">$1</h3>')
            .replace(/^## (.*$)/gim, '<h2 style="margin-top:25px; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:5px;">$1</h2>')
            .replace(/^# (.*$)/gim, '<h1 style="color:#0f172a;">$1</h1>')
            .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/gim, '<em>$1</em>')
            .replace(/`(.*?)`/gim, '<code style="background:#e2e8f0; padding:2px 4px; border-radius:3px; font-family:monospace; color:#ef4444;">$1</code>')
            .replace(/\n/gim, '<br>');
            
        // Limpeza básica para código blocks (simplificada)
        parsed = parsed.replace(/<br>```[\s\S]*?```<br>/gim, function(match) {
            return match.replace(/<br>/gim, '\n');
        });
        parsed = parsed.replace(/```(.*?)[\n\r]([\s\S]*?)```/gim, '<pre style="background:#1e293b; color:#e2e8f0; padding:15px; border-radius:6px; overflow-x:auto; font-family:monospace; margin:15px 0;"><code>$2</code></pre>');

        contentDiv.innerHTML = parsed;
    } catch(e) {
        contentDiv.innerHTML = '<div style="color:#ef4444; padding:20px; text-align:center;">Erro ao carregar o documento: ' + e.message + '</div>';
    }
};

window.closeSuperpowerDoc = function() {
    document.getElementById('sp-doc-modal').style.display = 'none';
};

window.initSuperpowersView = initSuperpowersView;
