document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('templates-view');
    if (!container) return;

    const templates = [
        {
            title: "CLAUDE.md",
            desc: "Instruções base de comportamento, regras e convenções do projeto para a IA (Flowgrammers & ECC).",
            path: "templates/CLAUDE.md"
        },
        {
            title: "PRD (Product Requirements Document)",
            desc: "Template para definir requisitos de produto, escopo, personas e métricas de sucesso.",
            path: "templates/prd.md"
        },
        {
            title: "Especificação Técnica (SPEC)",
            desc: "Template para design técnico, arquitetura de componentes, APIs e fluxo de dados.",
            path: "templates/spec.md"
        },
        {
            title: "Plano de QA / Testes",
            desc: "Documento para mapear casos de teste, cobertura, estratégia E2E e critérios de aceite.",
            path: "templates/qa.md"
        },
        {
            title: "Decisão Arquitetural (ADR)",
            desc: "Registro de decisões de arquitetura, trade-offs, riscos e diagramas de contexto.",
            path: "templates/arquitetural.md"
        },
        {
            title: "Revisão de Segurança (Security)",
            desc: "Checklist de segurança (OWASP), proteção de dados, controle de acessos e auditoria.",
            path: "templates/security.md"
        }
    ];

    container.innerHTML = `
        <div class="card" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:2.5rem; box-shadow:0 4px 6px rgba(0,0,0,0.02); max-width: 900px;">
            <div style="text-transform: uppercase; font-size: 0.85rem; color: #0078d4; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">📄 Base de Conhecimento</div>
            <h3 style="margin-bottom:1.2rem; color:#1a202c; font-size:2rem; border-bottom:1px solid #eee; padding-bottom: 1rem;">Templates Oficiais (.md)</h3>
            <p style="color:#4a5568; margin-bottom:2rem; font-size:1.15rem; line-height:1.7;">
                Esta seção contém templates padrão derivados das melhores práticas dos agentes Flowgrammers e ECC. Utilize estes arquivos para padronizar a documentação técnica, qualidade e segurança nos repositórios do seu time.
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px;">
                ${templates.map(t => `
                    <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; background: #f8fafc; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        <h4 style="margin-top: 0; margin-bottom: 10px; color: #2d3748; font-size: 1.25rem;">${t.title}</h4>
                        <p style="color: #4a5568; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px; min-height: 45px;">${t.desc}</p>
                        
                        <div style="display: flex; gap: 10px;">
                            <a href="${t.path}" download="${t.path.split('/').pop()}" style="flex:1; text-align:center; background-color: #0078d4; color: #fff; padding: 8px 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.9rem; transition: background 0.2s;">
                                ⬇️ Baixar (.md)
                            </a>
                            <a href="${t.path}" target="_blank" style="flex:1; text-align:center; background-color: #f3f2f1; color: #323130; padding: 8px 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.9rem; border: 1px solid #edebe9; transition: background 0.2s;">
                                👀 Visualizar
                            </a>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
});
