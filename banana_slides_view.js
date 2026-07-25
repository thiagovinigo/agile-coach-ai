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

                const headerCard = `
<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 30px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <h3 style="margin-top:0; color:#0f172a; display:flex; align-items:center; justify-content:space-between; gap:8px; font-size: 1.1rem; margin-bottom: 15px;">
        <span><span>📚</span> Resumo Rápido (${category})</span>
        ${window.favoritesManager ? window.favoritesManager.renderButton(skill.id, skill.title, 'Banana Slides', skill.path) : ''}
    </h3>
    <div style="background:#f1f5f9; border:1px solid #cbd5e1; padding:8px 12px; border-radius:4px; font-family:monospace; font-size:0.85rem; color:#475569; word-break:break-all; margin-bottom: 20px;">
        📂 <strong>Repositório:</strong> ${skill.path}
    </div>
    <div style="display: flex; gap: 10px; margin-bottom: 20px;">
        <a href="${skill.path}" download="${skill.id}.md" style="display:inline-block; background-color:#4f46e5; color:#fff; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:0.95rem; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            ⬇️ Baixar Arquivo da Skill
        </a>
        <a href="${skill.path}" target="_blank" style="display:inline-block; background-color:#f8fafc; color:#334155; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; border: 1px solid #cbd5e1; font-size:0.95rem;">
            👀 Ver Arquivo
        </a>
    </div>
    <h3 style="margin-top:0; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>🧠</span> O que é?
    </h3>
    <p style="margin-top:5px; color:#475569; font-size: 0.95rem;">
        A skill <strong>${skill.title}</strong> é uma ferramenta geradora/formatadora da biblioteca Banana Slides para automação e criação de apresentações e relatórios visuais.
    </p>

    <h3 style="margin-top:20px; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>⏱️</span> Quando usar?
    </h3>
    <p style="margin-top:5px; color:#475569; font-size: 0.95rem; font-weight: 500;">
        ${skill.description}
    </p>

    <h3 style="margin-top:20px; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>🛠️</span> Como usar?
    </h3>
    <ul style="margin-top:5px; color:#475569; font-size: 0.95rem; padding-left: 20px; margin-bottom:0;">
        <li>No seu terminal ou Claude Code, chame a instrução ou faça a leitura do arquivo base.</li>
        <li><strong>Exemplo:</strong> <code>/read ${skill.path}</code> seguido pelo contexto ou comando <code>${skill.title}</code>.</li>
    </ul>
</div>
`;

                contentArea.innerHTML = '<div style="padding:40px; text-align:center; color:#64748b;">⏳ Carregando ' + skill.title + '...</div>';
                
                fetch(skill.path)
                    .then(r => {
                        if(!r.ok) throw new Error("Não foi possível carregar o arquivo.");
                        return r.text();
                    })
                    .then(text => {
                        const preBlocks = [];
                        let processedText = text.replace(/```[a-z]*\n([\s\S]*?)```/g, (match, p1) => {
                            preBlocks.push(p1);
                            return `__PRE_BLOCK_${preBlocks.length - 1}__`;
                        });

                        let html = processedText
                            .replace(/^### (.*$)/gim, '<h3 style="margin-top:35px; margin-bottom:15px; color:#1e293b; font-size:1.4rem;">$1</h3>')
                            .replace(/^## (.*$)/gim, '<h2 style="margin-top:45px; margin-bottom:20px; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:8px; font-size:1.8rem;">$1</h2>')
                            .replace(/^# (.*$)/gim, '<h1 style="color:#0f172a; font-size:2.2rem; margin-bottom:25px;">$1</h1>')
                            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                            .replace(/\[([^\[]+)\]\(([^\)]+)\)/g, '<strong style="color:#4f46e5;">$1</strong>')
                            .replace(/^\> (.*$)/gim, '<blockquote style="background:#f8fafc; border-left:4px solid #cbd5e1; padding:15px 20px; color:#475569; margin:20px 0; border-radius:0 8px 8px 0; font-style:italic;">$1</blockquote>')
                            .replace(/^\|(.*)\|/gim, (match) => {
                                const cells = match.split('|').filter(c => c.trim() !== '');
                                if(cells.every(c => c.replace(/-/g, '').trim() === '')) return '';
                                return '<div style="display:flex; border-bottom:1px solid #e2e8f0; padding:10px 0;">' + cells.map(c => '<div style="flex:1; padding:0 10px;">' + c.trim() + '</div>').join('') + '</div>';
                            })
                            .replace(/^- (.*$)/gim, '<li style="margin-left:25px; margin-bottom:8px;">$1</li>')
                            .replace(/\n\n/g, '</p><p style="margin-bottom:15px;">')
                            .replace(/<p style="margin-bottom:15px;"><\/p>/g, '');

                        preBlocks.forEach((block, index) => {
                            html = html.replace(`__PRE_BLOCK_${index}__`, `<pre style="background:#0f172a; color:#e2e8f0; padding:15px; border-radius:8px; overflow-x:auto; font-family:monospace; font-size:13px; line-height:1.4;">${block}</pre>`);
                        });
                            
                        contentArea.innerHTML = `
                            <div style="max-width:900px; margin:0 auto; padding:40px; background:#fff; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.05); border:1px solid #edebe9; line-height:1.7; font-size:1.05rem; color:#334155;">
                                ${headerCard}
                                <p style="margin-bottom:15px;">${html}</p>
                            </div>
                        `;
                    })
                    .catch(e => {
                        contentArea.innerHTML = `
                            <div style="max-width:900px; margin:0 auto; padding:40px; background:#fff; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.05); border:1px solid #edebe9; line-height:1.7; font-size:1.05rem; color:#334155;">
                                ${headerCard}
                                <div style="padding:20px; color:red; background:#fff5f5; border-radius:6px; margin-top:20px;">Erro ao carregar documento Markdown (.md): ${e.message}</div>
                            </div>
                        `;
                    });
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
