document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('templates-view');
    if (!container) return;

    const templates = [
        {
            title: "CLAUDE.md / IA Core",
            desc: "Instruções base de comportamento, regras e convenções do projeto para os agentes (Flowgrammers & ECC).",
            path: "templates/CLAUDE.md"
        },
        {
            title: "PRD (Product Requirements Document)",
            desc: "Padrão Produto: Como mapear problemas, audiência, limites e métricas ANTES de codar.",
            path: "templates/prd.md"
        },
        {
            title: "Especificação Técnica (SPEC)",
            desc: "Padrão Engenharia: Detalhamento de arquitetura, contratos de API e restrições.",
            path: "templates/spec.md"
        },
        {
            title: "User Stories (STORYS)",
            desc: "Padrão Ágil: Como fatiar épicos em histórias de BDD com critérios de aceite e DoD.",
            path: "templates/storys.md"
        },
        {
            title: "Request for Comments (RFC)",
            desc: "Padrão Engenharia: Proposições assíncronas para mudanças de infra ou tecnologia, fomentando discussão sem culpas.",
            path: "templates/rfc.md"
        },
        {
            title: "Decisão Arquitetural (ADR)",
            desc: "Registro definitivo de escolhas de arquitetura que ditarão o rumo do software e seus trade-offs.",
            path: "templates/arquitetural.md"
        },
        {
            title: "Plano de Qualidade (QA)",
            desc: "Estratégia de validação: Testes, mitigação de risco e critérios de release/go-no-go.",
            path: "templates/qa.md"
        },
        {
            title: "Revisão de Segurança",
            desc: "Checklist restrito de InfoSec para proteção de dados, acessos e auditoria (OWASP).",
            path: "templates/security.md"
        },
        {
            title: "Post-mortem / Incidente (RCA)",
            desc: "Cultura blameless: Investigação profunda (5 Porquês) para aprender e previnir problemas críticos em produção.",
            path: "templates/rca.md"
        },
        {
            title: "Agente IA (SKILL)",
            desc: "Padrão skillsmp: Metadados, guard rails e instruções para definir o escopo de atuação autônoma de LLMs.",
            path: "templates/skill.md"
        }
    ];

    container.innerHTML = `
        <div class="card" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:2.5rem; box-shadow:0 4px 6px rgba(0,0,0,0.02); max-width: 1000px;">
            <div style="text-transform: uppercase; font-size: 0.85rem; color: #0078d4; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">📄 Base de Conhecimento</div>
            <h3 style="margin-bottom:1.2rem; color:#1a202c; font-size:2rem; border-bottom:1px solid #eee; padding-bottom: 1rem;">Templates Oficiais (.md)</h3>
            
            <div style="display: flex; gap: 2rem; margin-bottom: 2rem; align-items: flex-start; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <p style="color:#4a5568; font-size:1.15rem; line-height:1.7;">
                        Esta seção contém templates padrão derivados das melhores práticas dos agentes <strong>Flowgrammers e ECC</strong>. 
                        Eles foram desenhados para padronizar a documentação técnica, garantir a qualidade e elevar o nível de segurança nos repositórios do seu time.
                    </p>
                </div>
                
                <div style="flex: 1; min-width: 350px; background:#f0f8ff; border-left:4px solid #0078d4; padding:1.5rem; border-radius:8px;">
                    <h4 style="margin-top:0; color:#0078d4; margin-bottom:1rem; font-size:1.1rem;">🧭 Como e Quando Utilizar?</h4>
                    <ul style="margin:0; padding-left:20px; color:#334155; font-size:0.95rem; line-height:1.6;">
                        <li style="margin-bottom:8px;"><strong>1. Produto & Agilidade:</strong> Alinhe o "O que" com o <b>PRD.md</b>, debata propostas no <b>RFC.md</b> e quebre as entregas em <b>STORYS.md</b>.</li>
                        <li style="margin-bottom:8px;"><strong>2. Engenharia:</strong> Oficialize as escolhas no <b>Arquitetural.md (ADR)</b> e guie o código via <b>SPEC.md</b>.</li>
                        <li style="margin-bottom:8px;"><strong>3. Qualidade Contínua:</strong> Proteja o deploy com <b>QA.md</b>, blinde o código com o <b>Security.md</b>, e evolua após crises com o <b>RCA.md (Post-mortem)</b>.</li>
                        <li><strong>4. Cultura de IA:</strong> Mantenha seu projeto LLM-friendly centralizando regras no <b>CLAUDE.md</b> e crie agentes poderosos usando o formato <b>SKILL.md</b>.</li>
                    </ul>
                </div>
            </div>

            <h4 style="margin-top:2rem; margin-bottom:1rem; font-size:1.3rem; color:#2d3748; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">Arquivos Disponíveis</h4>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
                ${templates.map(t => `
                    <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; background: #fff; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                        <h4 style="margin-top: 0; margin-bottom: 10px; color: #2d3748; font-size: 1.15rem;">${t.title}</h4>
                        <p style="color: #4a5568; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px; min-height: 65px;">${t.desc}</p>
                        
                        <div style="display: flex; gap: 10px;">
                            <a href="${t.path}" download="${t.path.split('/').pop()}" style="flex:1; text-align:center; background-color: #0078d4; color: #fff; padding: 8px 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.85rem; transition: background 0.2s;">
                                ⬇️ Baixar (.md)
                            </a>
                            <a href="${t.path}" target="_blank" style="flex:1; text-align:center; background-color: #f3f2f1; color: #323130; padding: 8px 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.85rem; border: 1px solid #edebe9; transition: background 0.2s;">
                                👀 Visualizar
                            </a>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
});
