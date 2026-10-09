document.addEventListener('DOMContentLoaded', () => {
    initReferenciasView();
});

function initReferenciasView() {
    const container = document.getElementById('referencias-view');
    if (!container) return;

    const referencesData = [
        {
            category: "Referência de Sites",
            icon: "🌐",
            color: "#3b82f6", // blue
            links: [
                { title: "Context Dev", url: "https://www.context.dev/", desc: "Ferramentas e recursos para desenvolvimento e IA." },
                { title: "Aura Build Templates", url: "https://www.aura.build/templates", desc: "Templates de interface e componentes modernos." },
                { title: "Motion Sites AI", url: "https://motionsites.ai/", desc: "Inspirações e templates para sites com animações fluídas." }
            ]
        },
        {
            category: "Skills",
            icon: "🎒",
            color: "#8b5cf6", // purple
            links: [
                { title: "SkillsMP - Product Owner", url: "https://skillsmp.com/search?q=product+owner", desc: "Diretório de skills focadas em gestão de produtos e PO." },
                { title: "AI Tmpl - Skills", url: "https://aitmpl.com/skills/", desc: "Templates e diretórios de skills de IA para diversas áreas." }
            ]
        },
        {
            category: "Engenharia de IA & RAG",
            icon: "🧠",
            color: "#10b981", // green
            links: [
                { title: "VectifyAI / PageIndex", url: "https://github.com/VectifyAI/PageIndex", desc: "Framework open-source para RAG sem vetores (Vectorless). Ele constrói uma estrutura hierárquica que permite ao LLM navegar pelo documento imitando um humano, garantindo alta precisão em RAGs complexos." }
            ]
        },
        {
            category: "Facilitação e Ferramentas Ágeis",
            icon: "💡",
            color: "#f59e0b",
            links: [
                { title: "FunRetrospectives", url: "https://www.funretrospectives.com/pt/", desc: "Catálogo completo de atividades e dinâmicas para tornar suas retrospectivas ágeis mais envolventes (Team Building, Energizers, Futurespectives)." },
                { title: "Melhores Ferramentas Ágeis 2026", url: "https://echometerapp.com/pt/beste-kostenlose-agile-tools-2026/", desc: "Lista curada pela Echometer das melhores ferramentas gratuitas e pagas para equipes ágeis em 2026." },
                { title: "Masterclass: A Rota da Facilitação", url: "https://drive.google.com/file/d/19022oLGt17pEVo0ev9u6SItYO2KAwcwP/view?usp=sharing", desc: "PDF da Masterclass do Coletivo Ação abordando Diretiva Primária, Os 5 Desafios das Equipes, Projeto Aristóteles do Google e Acordos." }
            ]
        },
        {
            category: "Meus Boards Miro",
            icon: "💛",
            color: "#eab308",
            links: [
                { title: "Miro: Rota da Facilitação", url: "https://miro.com/app/board/uXjVMdUsHFU=/", desc: "Board oficial completo utilizado na dinâmica de facilitação (inclui Acordos, Expectativas, Radar de Felicidade)." },
                { title: "Miro: Área de Trabalho 2", url: "https://miro.com/app/board/uXjVPi2n1KI=/", desc: "Espaço de trabalho secundário no Miro." }
            ]
        }
];

    container.innerHTML = '';
    
    // Header
    const headerHtml = `
        <div style="background:#fff; padding:30px; border-bottom:1px solid #edebe9; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
            <div style="max-width: 1200px; margin: 0 auto;">
                <div style="text-transform: uppercase; font-size: 0.85rem; color: #0078d4; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">🔗 Links e Materiais</div>
                <h2 style="margin-top:0; color:#1a202c; font-size:2rem; margin-bottom:10px;">Referências Úteis</h2>
                <p style="font-size:1.15rem; line-height:1.6; color:#4a5568; margin:0; max-width: 800px;">
                    Curadoria de links externos, repositórios de skills, bibliotecas de templates e sites de referência para inspirar novos desenvolvimentos e produtos.
                </p>
            </div>
        </div>
    `;

    // Main Content
    const content = document.createElement('div');
    content.style.padding = '30px';
    content.style.maxWidth = '1200px';
    content.style.margin = '0 auto';
    
    let html = '';
    
    referencesData.forEach(cat => {
        html += `
            <div style="margin-bottom: 40px;">
                <h3 style="margin-top:0; color:${cat.color}; font-size:1.4rem; margin-bottom:20px; display:flex; align-items:center; gap:10px; border-bottom:2px solid #f1f5f9; padding-bottom:10px;">
                    <span>${cat.icon}</span> ${cat.category}
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px;">
                    ${cat.links.map(link => `
                        <a href="${link.url}" target="_blank" style="display:block; text-decoration:none; background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:20px; transition:all 0.2s; box-shadow:0 1px 3px rgba(0,0,0,0.03);" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 6px rgba(0,0,0,0.05)'; this.style.borderColor='${cat.color}'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.03)'; this.style.borderColor='#e2e8f0'">
                            <h4 style="margin:0 0 10px 0; color:#1e293b; font-size:1.1rem; display:flex; justify-content:space-between; align-items:flex-start;">
                                <span>${link.title}</span>
                                <span style="color:#94a3b8; font-size:0.9rem;">↗</span>
                            </h4>
                            <p style="margin:0 0 15px 0; color:#64748b; font-size:0.95rem; line-height:1.5;">
                                ${link.desc}
                            </p>
                            <div style="font-size:0.8rem; color:#94a3b8; word-break:break-all; background:#f8fafc; padding:6px 10px; border-radius:6px;">
                                ${link.url}
                            </div>
                        </a>
                    `).join('')}
                </div>
            </div>
        `;
    });

    content.innerHTML = html;
    
    container.innerHTML = headerHtml;
    container.appendChild(content);
}
