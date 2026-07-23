document.addEventListener('DOMContentLoaded', () => {
    initOpenWikiView();
});

function initOpenWikiView() {
    const container = document.getElementById('openwiki-view');
    if(!container || typeof openwikiData === 'undefined') return;

    let html = `
        <div class="hero-section" style="background:linear-gradient(135deg, #0f172a, #1e293b); padding:40px; text-align:left;">
            <h3 style="font-size:2rem; font-weight:800; color:#fff; margin-bottom:10px;">📖 OpenWiki Skills</h3>
            <p style="font-size:1.1rem; color:#94a3b8; max-width:800px;">
                Catálogo de skills do repositório OpenWiki (LangChain). Estas skills permitem a agentes de IA (como o Kiro ou Claude Code) gerenciar e manter wikis de forma autônoma utilizando a estrutura OKF.
            </p>
            <a href="https://github.com/langchain-ai/openwiki.git" target="_blank" style="display:inline-block; margin-top:16px; padding:8px 16px; background:#38bdf8; color:#fff; border-radius:6px; font-weight:bold; text-decoration:none;">🔗 Acessar Repositório</a>
        </div>
        <div class="grid-cards" style="padding: 20px;">
    `;

    openwikiData.forEach(skill => {
        html += `
            <div class="card" style="position:relative;">
                <button onclick="openAgentInfo(this)" data-title="${skill.title}" data-icon="${skill.icon || '🧰'}" data-desc="${encodeURIComponent(skill.description)}" data-type="skill" data-path="${skill.path}" style="position:absolute; top:12px; right:12px; background:transparent; border:1px solid #c8c6c4; border-radius:50%; width:24px; height:24px; color:#605e5c; cursor:pointer; font-weight:bold; display:flex; justify-content:center; align-items:center;" title="Ver detalhes">?</button>
                <div class="card-icon">${skill.icon || '🧰'}</div>
                <div class="card-title">${skill.title}</div>
                <div class="card-desc" style="height: 60px; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">${skill.description}</div>
                <button class="card-action" onclick="openInfoModalDirect('${skill.title}', '${skill.icon || '🧰'}', '${encodeURIComponent(skill.description)}', 'skill', '${skill.path}')">
                    ⬇️ Baixar Skill
                </button>
            </div>
        `;
    });

    html += `
        </div>
    `;

    container.innerHTML = html;
}
