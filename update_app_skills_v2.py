import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Remove the old initSkillsView block entirely
app_js = re.sub(r'function initSkillsView\(\) \{.*?(?=\n\}|\Z)\n\}', '', app_js, flags=re.DOTALL)

# Now define the new initSkillsView with submenus
skills_logic = """
function initSkillsView() {
    const container = document.getElementById('skills-view');
    if(!container || typeof skillsData === 'undefined') return;

    // Clear old layout if re-initialized
    container.innerHTML = '';

    const layout = document.createElement('div');
    layout.className = 'kb-layout';

    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    // Adicionar rolagem na sidebar para suportar muitos itens
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';

    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    container.appendChild(layout);

    let isFirst = true;

    for(const category in skillsData) {
        const skillsList = skillsData[category];
        
        // Category Header
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#fff';
        catHeader.style.backgroundColor = 'rgba(232,0,106,.2)';
        catHeader.style.borderLeft = '3px solid #e8006a';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        catHeader.style.marginBottom = '5px';
        catHeader.style.borderRadius = '0 6px 6px 0';
        catHeader.style.transition = 'background 0.2s';
        catHeader.innerHTML = `${category} <span style="font-size:0.8rem; color:#aaa; float:right;">▼</span>`;
        
        const subMenu = document.createElement('div');
        subMenu.className = 'kb-submenu';
        subMenu.style.display = isFirst ? 'block' : 'none'; 
        subMenu.style.paddingLeft = '5px';

        catHeader.onmouseover = () => catHeader.style.backgroundColor = 'rgba(232,0,106,.4)';
        catHeader.onmouseout = () => catHeader.style.backgroundColor = 'rgba(232,0,106,.2)';

        catHeader.onclick = () => {
            const isVisible = subMenu.style.display === 'block';
            // Fechar todos
            sidebar.querySelectorAll('.kb-submenu').forEach(sm => sm.style.display = 'none');
            sidebar.querySelectorAll('.kb-category-header span').forEach(sp => sp.innerText = '▼');
            
            // Abrir o clicado se estava fechado
            if (!isVisible) {
                subMenu.style.display = 'block';
                catHeader.querySelector('span').innerText = '▲';
            }
        };
        
        if (isFirst) {
            catHeader.querySelector('span').innerText = '▲';
        }

        sidebar.appendChild(catHeader);
        sidebar.appendChild(subMenu);

        skillsList.forEach((skill, idx) => {
            const wrapper = document.createElement('div');
            wrapper.className = 'section-group sub-page';
            wrapper.style.display = (isFirst && idx === 0) ? 'block' : 'none';
            
            const triggersList = skill.triggers.map(t => `<span class="tag" style="display:inline-block; background:rgba(232,0,106,.12); border:1px solid rgba(232,0,106,.3); padding:.3em .8em; border-radius:999px; font-size:.85rem; color:#e8006a; margin-right:5px; margin-bottom:5px;">${t}</span>`).join('');
            
            wrapper.innerHTML = `
                <div class="card" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:2.5rem; box-shadow:0 4px 6px rgba(0,0,0,0.02); max-width: 900px;">
                    <div style="text-transform: uppercase; font-size: 0.85rem; color: #e8006a; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">📁 ${category}</div>
                    <h3 style="margin-bottom:1.2rem; color:#1a202c; font-size:2rem; border-bottom:1px solid #eee; padding-bottom: 1rem;">${skill.title}</h3>
                    <p style="color:#4a5568; margin-bottom:2rem; font-size:1.15rem; line-height:1.7;">${skill.description || '<i>Sem descrição fornecida.</i>'}</p>
                    
                    <div style="background:#f7fafc; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
                        <h4 style="margin-top:0; margin-bottom:1rem; font-size:1.1rem; color:#2d3748; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🎯 Quando Chamar (Triggers)</h4>
                        <div>${triggersList || '<span style="color:#a0aec0; font-size:0.95rem;">Nenhum trigger explícito. Aja de acordo com a descrição.</span>'}</div>
                    </div>
                    
                    <h4 style="margin-top:1.5rem; margin-bottom:0.8rem; font-size:1rem; color:#718096; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🛠️ Como Instalar (Claude Code):</h4>
                    <pre style="background:#1e1e1e; color:#d4d4d4; padding:1.2rem; border-radius:8px; font-family:monospace; overflow-x:auto; margin-bottom:2rem; font-size:1.05rem;">/read flowgrammers-skills-main/flowgrammers-skills-main/${skill.path}</pre>
                    
                    <h4 style="margin-top:1.5rem; margin-bottom:0.8rem; font-size:1rem; color:#718096; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🚀 Como Executar:</h4>
                    <p style="font-size:1rem; color:#4a5568; line-height: 1.6;">No Claude Code, após o <strong>/read</strong> acima, simplesmente peça a tarefa na linguagem natural correspondente a um dos <strong>Triggers</strong>. O Claude Code automaticamente engatilhará as instruções do arquivo <code>SKILL.md</code> correspondente.</p>
                </div>
            `;
            contentArea.appendChild(wrapper);

            // Sidebar sub-button
            const btn = document.createElement('button');
            btn.className = 'kb-nav-btn' + ((isFirst && idx === 0) ? ' active' : '');
            btn.style.fontSize = '0.9rem';
            btn.style.padding = '8px 10px 8px 25px';
            btn.innerText = skill.title;
            
            btn.onclick = () => {
                contentArea.querySelectorAll('.sub-page').forEach(p => p.style.display = 'none');
                sidebar.querySelectorAll('.kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                wrapper.style.display = 'block';
                contentArea.scrollTop = 0;
            };

            subMenu.appendChild(btn);
        });
        
        isFirst = false;
    }
}
"""

app_js += "\n\n" + skills_logic

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
