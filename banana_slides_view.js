document.addEventListener('DOMContentLoaded', () => {
    initBananaSlidesView();
});

function initBananaSlidesView() {
    const container = document.getElementById('banana-slides-view');
    if(!container || typeof bananaSlidesData === 'undefined') return;

    container.innerHTML = '';
    
    // Header
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.style.marginBottom = '20px';
    introHeader.innerHTML = `
        <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px;">🍌 Banana Slides</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            Integração nativa de AI PPT Generator (Projeto open-source). Transforme descrições em apresentações completas.
        </p>
        <p style="margin-top:10px;">
            <a href="https://github.com/Anionex/banana-slides.git" target="_blank" style="display:inline-block; padding:6px 12px; background:#e0e7ff; color:#4f46e5; border-radius:4px; font-weight:bold; text-decoration:none; font-size:14px;">🔗 Acessar Repositório Original</a>
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

    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    container.appendChild(layout);

    const categories = Object.keys(bananaSlidesData);
    let firstBtn = null;

    categories.forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #6366f1';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const linkList = document.createElement('div');
        linkList.className = 'kb-link-list';
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        const skillsList = bananaSlidesData[category];
        skillsList.forEach((skill) => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.innerHTML = `<span style="margin-right:8px;">${skill.icon}</span> ${skill.title}`;
            linkList.appendChild(btn);

            if(!firstBtn) firstBtn = btn;

            btn.onclick = () => {
                document.querySelectorAll('#banana-slides-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Render standard skill content
                contentArea.innerHTML = `
                    <div style="max-width:800px; margin:0 auto; padding:20px; background:#fff; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.05); border:1px solid #edebe9;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem;">
                            <div>
                                <span style="background:#e0e7ff; color:#4f46e5; padding:4px 8px; border-radius:4px; font-size:12px; font-weight:bold; text-transform:uppercase; margin-bottom:10px; display:inline-block;">${category}</span>
                                <h3 style="margin:0; color:#0f172a; font-size:2rem; display:flex; align-items:center; gap:10px;">
                                    ${skill.icon} ${skill.title}
                                </h3>
                            </div>
                        </div>
                        
                        <p style="color:#475569; font-size:1.15rem; line-height:1.6; margin-bottom:1.5rem;">${skill.description}</p>
                        
                        <div style="background:#f8fafc; padding:15px; border-radius:6px; margin-bottom:20px; font-size:0.95rem; color:#334155;">
                            📂 <strong>Repositório Path:</strong> <code>${skill.path}</code>
                        </div>

                        <div style="display:flex; gap:10px; margin-bottom:25px;">
                            <a href="${skill.path}" download="${skill.id}.md" style="display:inline-block; background-color:#4f46e5; color:#fff; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:1rem; box-shadow:0 2px 4px rgba(0,0,0,0.1); transition: background 0.2s;">
                                ⬇️ Baixar Skill
                            </a>
                            <a href="${skill.path}" target="_blank" style="display:inline-block; background-color:#f8fafc; color:#0f172a; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; border: 1px solid #e2e8f0; font-size:1rem; transition: background 0.2s;">
                                👀 Ver Arquivo
                            </a>
                        </div>

                        <div style="margin-top:20px; border-top:1px solid #e2e8f0; padding-top:20px;">
                            <h4 style="margin-top:0; color:#334155; margin-bottom:10px;">Como usar no Claude Code / Terminal:</h4>
                            <pre style="background:#0f172a; color:#e2e8f0; padding:15px; border-radius:8px; font-family:monospace; font-size:14px; overflow-x:auto;">/read ${skill.path}
${skill.title}
Contexto: [Descreva os parâmetros aqui]</pre>
                        </div>
                    </div>
                `;
            };
        });

        // Toggle category
        catHeader.onclick = () => {
            if(linkList.style.display === 'none') {
                linkList.style.display = 'block';
                catHeader.style.borderLeftColor = '#6366f1';
                catHeader.style.backgroundColor = '#f3f2f1';
            } else {
                linkList.style.display = 'none';
                catHeader.style.borderLeftColor = '#ccc';
                catHeader.style.backgroundColor = 'transparent';
            }
        };
    });

    if(firstBtn) firstBtn.click();
}
