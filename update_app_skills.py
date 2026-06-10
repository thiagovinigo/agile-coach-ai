import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Append the initSkillsView function
skills_logic = """
function initSkillsView() {
    const container = document.getElementById('skills-view');
    if(!container || typeof skillsData === 'undefined') return;

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

    for(const category in skillsData) {
        const wrapper = document.createElement('div');
        wrapper.className = 'section-group sub-page';
        wrapper.id = 'skill-cat-' + category.replace(/\s+/g, '-').toLowerCase();
        wrapper.style.display = firstPage ? 'block' : 'none';

        const skillsList = skillsData[category];
        
        let html = `<h2 style="margin-bottom:1rem; font-size:1.8rem; border-bottom:2px solid #e8006a; padding-bottom:0.5rem; display:inline-block;">${category} <span style="font-size:1rem; color:#888; font-weight:normal;">(${skillsList.length} skills)</span></h2><div class="skills-grid" style="display:flex; flex-direction:column; gap:2rem; margin-top:1.5rem;">`;

        skillsList.forEach(skill => {
            const triggersList = skill.triggers.map(t => `<span class="tag" style="display:inline-block; background:rgba(232,0,106,.12); border:1px solid rgba(232,0,106,.3); padding:.3em .8em; border-radius:999px; font-size:.85rem; color:#e8006a; margin-right:5px; margin-bottom:5px;">${t}</span>`).join('');
            
            html += `
                <div class="card" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:1.8rem; box-shadow:0 4px 6px rgba(0,0,0,0.02);">
                    <h3 style="margin-bottom:0.8rem; color:#1a202c; font-size:1.5rem;">${skill.title}</h3>
                    <p style="color:#4a5568; margin-bottom:1.5rem; font-size:1.1rem; line-height:1.6;">${skill.description || '<i>Sem descrição fornecida.</i>'}</p>
                    
                    <h4 style="margin-top:1rem; margin-bottom:0.8rem; font-size:1rem; color:#718096; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🎯 Quando Chamar (Triggers):</h4>
                    <div style="margin-bottom:1.5rem;">${triggersList || '<span style="color:#a0aec0; font-size:0.9rem;">Nenhum trigger explícito. Aja de acordo com a descrição.</span>'}</div>
                    
                    <h4 style="margin-top:1rem; margin-bottom:0.8rem; font-size:1rem; color:#718096; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🛠️ Como Instalar (Claude Code):</h4>
                    <pre style="background:#1e1e1e; color:#d4d4d4; padding:1rem; border-radius:8px; font-family:monospace; overflow-x:auto; margin-bottom:1.5rem;">/read flowgrammers-skills-main/flowgrammers-skills-main/${skill.path}</pre>
                    
                    <h4 style="margin-top:1rem; margin-bottom:0.8rem; font-size:1rem; color:#718096; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🚀 Como Executar:</h4>
                    <p style="font-size:0.95rem; color:#4a5568; background:#f7fafc; padding:1rem; border-radius:8px; border-left:4px solid #e8006a;">No Claude Code, após o <strong>/read</strong> acima, simplesmente peça a tarefa na linguagem natural correspondente a um dos <strong>Triggers</strong>. O Claude Code automaticamente engatilhará as instruções do arquivo <code>SKILL.md</code> correspondente.</p>
                </div>
            `;
        });

        html += `</div>`;
        wrapper.innerHTML = html;
        contentArea.appendChild(wrapper);

        // Sidebar button
        const btn = document.createElement('button');
        btn.className = 'kb-nav-btn' + (firstPage ? ' active' : '');
        btn.innerText = category;
        btn.onclick = () => {
            contentArea.querySelectorAll('.sub-page').forEach(p => p.style.display = 'none');
            sidebar.querySelectorAll('.kb-nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            wrapper.style.display = 'block';
            contentArea.scrollTop = 0;
        };

        sidebar.appendChild(btn);
        firstPage = false;
    }
}
"""

if "function initSkillsView" not in app_js:
    app_js += "\n\n" + skills_logic

# Add call to initSkillsView() in DOMContentLoaded
if "initSkillsView();" not in app_js:
    app_js = app_js.replace("loadAndMigrateContent();", "loadAndMigrateContent();\n    initSkillsView();")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
