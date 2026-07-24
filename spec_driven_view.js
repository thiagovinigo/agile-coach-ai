document.addEventListener('DOMContentLoaded', () => {
    initSpecDrivenView();
});

function initSpecDrivenView() {
    const container = document.getElementById('spec-driven-view');
    if(!container || typeof specDrivenData === 'undefined') return;

    container.innerHTML = '';
    
    // Header
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.style.marginBottom = '20px';
    introHeader.innerHTML = `
        <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px;">🎯 Spec-Driven</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            Scaffold de Spec-Driven Development (SDD) para agentes de IA. Templates, skills e regras arquiteturais.
        </p>
        <p style="margin-top:10px;">
            <a href="https://github.com/igoruehara/spec-driven.git" target="_blank" style="display:inline-block; padding:6px 12px; background:#e0e7ff; color:#4f46e5; border-radius:4px; font-weight:bold; text-decoration:none; font-size:14px;">🔗 Acessar Repositório Original</a>
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

    const categories = Object.keys(specDrivenData);
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
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        const skillsList = specDrivenData[category];
        skillsList.forEach((skill) => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">${skill.icon}</span>
                    <span style="font-weight:600; color:#323130; font-size:0.95rem;">${skill.title}</span>
                </div>
                <div style="font-size:0.8rem; color:#605e5c; margin-top:4px; line-height:1.3; white-space:normal;">
                    ${skill.description}
                </div>
            `;
            
            if(!firstBtn) firstBtn = {btn, skill};

            btn.onclick = () => {
                document.querySelectorAll('#spec-driven-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                contentArea.innerHTML = '<div style="padding:40px; text-align:center;">Carregando conteúdo...</div>';
                
                fetch(skill.path)
                    .then(r => {
                        if (!r.ok) throw new Error("Documento não encontrado.");
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
                            .replace(/\[([^\[]+)\]\(([^\)]+)\)/g, '<strong style="color:#4f46e5; text-decoration:underline;">$1</strong>')
                            .replace(/^\> (.*$)/gim, '<blockquote style="background:#f8fafc; border-left:4px solid #cbd5e1; padding:15px 20px; color:#475569; margin:20px 0; font-style:italic;">$1</blockquote>')
                            .replace(/^\|(.*)\|/gim, (match) => {
                                const cells = match.split('|').filter(c => c.trim() !== '');
                                if(cells.every(c => c.replace(/-/g, '').trim() === '')) return '';
                                return '<div style="display:flex; border-bottom:1px solid #e2e8f0; padding:10px 0;">' + cells.map(c => '<div style="flex:1; padding:0 10px;">' + c.trim() + '</div>').join('') + '</div>';
                            })
                            .replace(/^- (.*$)/gim, '<li style="margin-left:25px; margin-bottom:8px;">$1</li>')
                            .replace(/\n\n/g, '</p><p style="margin-bottom:15px;">')
                            .replace(/<p style="margin-bottom:15px;"><\/p>/g, '');

                        preBlocks.forEach((block, index) => {
                            html = html.replace(`__PRE_BLOCK_${index}__`, `<pre style="background:#0f172a; color:#e2e8f0; padding:15px; border-radius:6px; overflow-x:auto; font-family:monospace; font-size:13px; line-height:1.4; margin:15px 0;">${block}</pre>`);
                        });

                        contentArea.innerHTML = `
                            <div style="padding:40px; background:#fff; min-height:100%;">
                                <div style="max-width:900px; margin:0 auto; line-height:1.7; color:#334155; font-size:1.05rem;">
                                    <p style="margin-bottom:15px;">${html}</p>
                                </div>
                            </div>
                        `;
                    })
                    .catch(err => {
                        contentArea.innerHTML = `<div style="padding:40px; color:red; text-align:center;">Erro ao carregar o documento: ${err.message}</div>`;
                    });
            };
            
            linkList.appendChild(btn);
        });
    });

    if(firstBtn) {
        firstBtn.btn.click();
    }

    window.renderSpecDrivenView = function(viewId) {
        if(viewId === 'spec-driven-view' && !container.innerHTML) {
            initSpecDrivenView();
        }
    };
}
