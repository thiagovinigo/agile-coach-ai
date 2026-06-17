document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('mcp-plugins-view');
    if (!container) return;

    const mcps = [
        { name: "GitHub MCP", desc: "Permite que os Agentes leiam PRs, abram issues e façam code review autônomo.", status: "Ativo", color: "green" },
        { name: "PostgreSQL / Supabase MCP", desc: "Conecta a IA ao banco de dados para rodar queries e modelar schemas.", status: "Beta", color: "yellow" },
        { name: "Jira / Azure DevOps MCP", desc: "Integração bidirecional para atualizar o status das tarefas e estimativas.", status: "Planejado", color: "gray" },
        { name: "Brave Search / Web MCP", desc: "Dá acesso à web em tempo real para pesquisa de documentação atualizada.", status: "Ativo", color: "green" }
    ];

    const hooks = [
        { name: "plugin-hook-bootstrap.js", desc: "Hook do ECC para inicializar contextos de plugins na IDE de forma segura.", status: "Core", color: "blue" },
        { name: "pre-commit AI Audit", desc: "Hook de Git que roda uma análise rápida do Flowgrammers antes do commit.", status: "Ativo", color: "green" },
        { name: "CI/CD Build Error Resolver", desc: "Hook de pipeline que aciona o Agente em caso de falha no GitHub Actions.", status: "Beta", color: "yellow" }
    ];

    const plugins = [
        { name: "Laravel Plugin Discovery", desc: "Plugin ECC para auto-mapeamento de rotas e controllers em PHP/Laravel.", status: "Ativo", color: "green" },
        { name: "Plugin Audit (plugin-audit.md)", desc: "Ferramenta Flowgrammers para auditar dependências e vulnerabilidades CVE.", status: "Core", color: "blue" },
        { name: "OpenCode Integration", desc: "Manifestos (.codex-plugin) para interoperabilidade entre diferentes LLMs na IDE.", status: "Ativo", color: "green" }
    ];

    const renderBadge = (status, color) => {
        const colors = {
            green: "bg-green-100 text-green-800 border-green-200",
            yellow: "bg-yellow-100 text-yellow-800 border-yellow-200",
            blue: "bg-blue-100 text-blue-800 border-blue-200",
            gray: "bg-gray-100 text-gray-800 border-gray-200"
        };
        const c = colors[color] || colors.gray;
        // Simulando classes do tailwind com styles inline pra garantir
        let style = "padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; border: 1px solid;";
        if (color === 'green') style += "background: #c6f6d5; color: #22543d; border-color: #9ae6b4;";
        if (color === 'yellow') style += "background: #fefcbf; color: #744210; border-color: #f6e05e;";
        if (color === 'blue') style += "background: #ebf8ff; color: #2a4365; border-color: #bee3f8;";
        if (color === 'gray') style += "background: #edf2f7; color: #2d3748; border-color: #e2e8f0;";
        
        return `<span style="${style}">${status}</span>`;
    };

    const renderTable = (items, title, icon) => `
        <div style="margin-bottom: 3rem;">
            <h4 style="margin-top:0; color:#2d3748; font-size:1.4rem; margin-bottom: 1rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem;">
                <span style="margin-right: 8px;">${icon}</span>${title}
            </h4>
            <div style="overflow-x: auto; border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <table style="width: 100%; border-collapse: collapse; text-align: left; background: #fff;">
                    <thead style="background: #f8fafc;">
                        <tr>
                            <th style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #4a5568; font-size: 0.9rem; width: 30%;">Nome da Ferramenta</th>
                            <th style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #4a5568; font-size: 0.9rem; width: 55%;">Descrição e Caso de Uso</th>
                            <th style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #4a5568; font-size: 0.9rem; width: 15%;">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${items.map(item => `
                            <tr style="border-bottom: 1px solid #e2e8f0; transition: background 0.2s;" onmouseover="this.style.background='#f0f8ff'" onmouseout="this.style.background='transparent'">
                                <td style="padding: 16px; color: #1a202c; font-weight: 600; font-size: 0.95rem;">${item.name}</td>
                                <td style="padding: 16px; color: #4a5568; font-size: 0.95rem;">${item.desc}</td>
                                <td style="padding: 16px;">${renderBadge(item.status, item.color)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;

    container.innerHTML = `
        <div class="card" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:2.5rem; box-shadow:0 4px 6px rgba(0,0,0,0.02); max-width: 1000px;">
            <div style="text-transform: uppercase; font-size: 0.85rem; color: #0078d4; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">⚙️ Agentes & Ferramentas</div>
            <h3 style="margin-bottom:1.2rem; color:#1a202c; font-size:2rem; border-bottom:1px solid #eee; padding-bottom: 1rem;">MCPs, Hooks e Plugins</h3>
            
            <div style="display: flex; gap: 2rem; margin-bottom: 2rem; align-items: flex-start; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <p style="color:#4a5568; font-size:1.1rem; line-height:1.7;">
                        Para que nossos Agentes (Flowgrammers e ECC) sejam verdadeiramente autônomos e poderosos, eles precisam de ferramentas de conexão com o mundo exterior. 
                        Este é o diretório oficial de <strong>integrações sistêmicas</strong> que expandem o "cérebro" da IA.
                    </p>
                </div>
                
                <div style="flex: 1; min-width: 350px; background:#f0f8ff; border-left:4px solid #0078d4; padding:1.5rem; border-radius:8px;">
                    <h4 style="margin-top:0; color:#0078d4; margin-bottom:1rem; font-size:1.1rem;">Glossário Rápido</h4>
                    <ul style="margin:0; padding-left:20px; color:#334155; font-size:0.95rem; line-height:1.6;">
                        <li style="margin-bottom:8px;"><strong>🔌 MCP (Model Context Protocol):</strong> Servidores locais ou remotos que dão à IA a capacidade de ler/escrever em bancos de dados, APIs ou arquivos com segurança.</li>
                        <li style="margin-bottom:8px;"><strong>🪝 Hooks:</strong> Gatilhos que disparam Agentes de IA em momentos-chave (como num commit de código ou falha de CI/CD).</li>
                        <li><strong>🧩 Plugins:</strong> Extensões específicas (manifestos JSON/MD) instaladas na IDE ou no Agente para estender capacidades de frameworks.</li>
                    </ul>
                </div>
            </div>

            ${renderTable(mcps, "Servidores MCP (Integrações de Contexto)", "🔌")}
            ${renderTable(hooks, "Hooks (Gatilhos Autônomos)", "🪝")}
            ${renderTable(plugins, "Plugins (Extensões de Framework)", "🧩")}

        </div>
    `;
});
