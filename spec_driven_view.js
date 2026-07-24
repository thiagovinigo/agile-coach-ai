document.addEventListener('DOMContentLoaded', () => {
    if (window.renderSpecDrivenView) window.renderSpecDrivenView('spec-driven-view');
});

(function() {
    window.renderSpecDrivenView = function(containerId) {
        const container = document.getElementById(containerId);
        if (!container || typeof specDrivenData === 'undefined') return;

        let selectedSkillId = specDrivenData[0].id;

        const render = () => {
            const categories = [...new Set(specDrivenData.map(s => s.category))];

            container.innerHTML = `
                <div style="display:flex; height:100%; gap:20px; background:#f8fafc;">
                    <!-- Sidebar -->
                    <div style="width:300px; background:#fff; border-right:1px solid #e2e8f0; display:flex; flex-direction:column; overflow-y:auto;">
                        <div style="padding:20px; border-bottom:1px solid #e2e8f0; position:sticky; top:0; background:#fff; z-index:10;">
                            <h2 style="margin:0; font-size:1.2rem; color:#0f172a; display:flex; align-items:center; gap:8px;">
                                🎯 Spec-Driven
                            </h2>
                            <p style="margin:5px 0 0 0; font-size:0.85rem; color:#64748b;">
                                Templates de Agentes (Igor Uehara)
                            </p>
                        </div>
                        <div style="padding:15px;">
                            ${categories.map(category => `
                                <div style="margin-bottom:20px;">
                                    <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; color:#94a3b8; font-weight:bold; margin-bottom:10px; padding-left:5px;">
                                        ${category}
                                    </div>
                                    ${specDrivenData.filter(s => s.category === category).map(skill => `
                                        <div class="skill-item ${skill.id === selectedSkillId ? 'active' : ''}" data-id="${skill.id}" style="padding:12px; margin-bottom:8px; border-radius:6px; cursor:pointer; display:flex; gap:10px; align-items:center; transition:all 0.2s; background: ${skill.id === selectedSkillId ? '#e0e7ff' : '#f8fafc'}; border-left: 4px solid ${skill.id === selectedSkillId ? '#4f46e5' : 'transparent'};">
                                            <span style="font-size:1.2rem;">${skill.icon}</span>
                                            <div>
                                                <div style="font-weight:600; color:#1e293b; font-size:0.95rem;">${skill.title}</div>
                                                <div style="font-size:0.8rem; color:#64748b; margin-top:3px; line-height:1.3;">${skill.description}</div>
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Content Area -->
                    <div style="flex:1; overflow-y:auto; background:#f8fafc;" id="spec-driven-content-area">
                        <!-- Content will be injected here -->
                    </div>
                </div>
            `;

            // Attach click listeners
            container.querySelectorAll('.skill-item').forEach(el => {
                el.addEventListener('click', (e) => {
                    selectedSkillId = e.currentTarget.dataset.id;
                    render(); // Re-render sidebar to update active state
                });
            });

            // Render selected content
            renderContent(selectedSkillId);
        };

        function renderContent(skillId) {
            const contentArea = container.querySelector('#spec-driven-content-area');
            if (!contentArea) return;

            const skill = specDrivenData.find(s => s.id === skillId);
            if (!skill) {
                contentArea.innerHTML = '<div style="padding:40px; color:#64748b; text-align:center;">Selecione um tópico para visualizar.</div>';
                return;
            }

            // Show loading state
            contentArea.innerHTML = `
                <div style="display:flex; justify-content:center; align-items:center; height:100%; color:#64748b;">
                    <div style="text-align:center;">
                        <div style="font-size:2rem; margin-bottom:10px;">⏳</div>
                        <div>Carregando conteúdo do repositório...</div>
                    </div>
                </div>
            `;

            fetch(skill.path)
                .then(r => {
                    if (!r.ok) throw new Error("Não encontrado (404) em " + skill.path);
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
                        <div style="padding:40px;">
                            <div style="max-width:900px; margin:0 auto; background:#fff; padding:40px; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,0.1); line-height:1.7; color:#334155; font-size:1.05rem;">
                                <p style="margin-bottom:15px;">${html}</p>
                            </div>
                        </div>
                    `;
                })
                .catch(err => {
                    contentArea.innerHTML = `<div style="padding:40px; color:red; text-align:center;">Erro ao carregar conteúdo: ${err.message}</div>`;
                });
        }

        render();
    };
})();
