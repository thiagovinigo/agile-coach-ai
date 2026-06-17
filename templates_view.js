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
                        <li style="margin-bottom:8px;"><strong>1. Planejamento:</strong> Inicie com o <b>PRD.md</b> para alinhar as regras de negócio e escopo com Produto.</li>
                        <li style="margin-bottom:8px;"><strong>2. Arquitetura:</strong> Use o <b>Arquitetural.md (ADR)</b> para registrar escolhas técnicas (ex: mudar de REST para GraphQL).</li>
                        <li style="margin-bottom:8px;"><strong>3. Refinamento Técnico:</strong> Detalhe APIs, dependências e fluxos no <b>SPEC.md</b> antes de iniciar a codificação.</li>
                        <li style="margin-bottom:8px;"><strong>4. Qualidade & Segurança:</strong> Use o <b>QA.md</b> para testes E2E e passe o <b>Security.md</b> em fluxos críticos.</li>
                        <li><strong>5. Desenvolvimento IA:</strong> Mantenha o <b>CLAUDE.md</b> atualizado na raiz do projeto para balizar o comportamento dos Agentes.</li>
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
