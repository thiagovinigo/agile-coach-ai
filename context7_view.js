document.addEventListener('DOMContentLoaded', () => {
    initContext7View();
});

function initContext7View() {
    if (typeof context7Data === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'context7-view',
        title: 'Context7 (Upstash)',
        badge: 'Up-to-date Docs for AI Agents',
        icon: '📚',
        tagline: 'Documentação atualizada e específica por versão direto da fonte para Agentes de IA via MCP e CLI (por Upstash)',
        description: 'O <strong>Context7 (Upstash)</strong> elimina exemplos de código desatualizados e APIs alucinadas injetando documentação oficial e exemplos reais específicos da versão diretamente no contexto do seu agente de codificação. Funciona em dois modos: <strong>CLI + Skills (<code>npx ctx7</code>)</strong> e <strong>Servidor MCP (<code>@upstash/context7-mcp</code>)</strong> com as tools <code>resolve-library-id</code> e <code>query-docs</code>.',
        themeColor: '#10b981',
        themeGradient: 'linear-gradient(135deg, #064e3b 0%, #0f172a 60%, #022c22 100%)',
        githubRepo: 'https://github.com/upstash/context7',
        itemType: 'Context7',
        pills: [
            { text: '⭐ GitHub: upstash/context7', link: 'https://github.com/upstash/context7' },
            { text: '🌐 context7.com', link: 'https://context7.com' },
            { text: '🔌 MCP: resolve-library-id & query-docs' },
            { text: '⌨️ CLI: npx ctx7 setup / docs' },
            { text: '📌 Version Pinning (/vercel/next.js/v16.2.9)' },
            { text: '🪐 Plugin Nativo Antigravity, Claude & Cursor' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todos os Documentos & Plugins (30)' },
            { id: '1. Visão Geral', label: '📘 Visão Geral & Guias (8)' },
            { id: '2. Skills, Rules', label: '💻 Skills & Rules Oficiais (7)' },
            { id: '3. Plugins por IDE', label: '🪐 Plugins IDE & Sub-Agentes (9)' },
            { id: '4. Pacotes NPM', label: '📦 NPM, SDK & Enterprise (6)' },
            { id: 'cheatsheet', label: '⚡ Como Usar: CLI, MCP, Regras & Prompts' }
        ],
        data: context7Data,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>📚</span> Context7 (Upstash) — Setup Unificado, Comandos CLI, MCP & Regras
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Acabe com APIs inventadas: veja como configurar o Context7 em segundos e buscar documentação exata por versão.
                    </p>
                </div>

                <!-- 1. Setup Unificado -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🚀</span> 1. Setup em 1 Comando (CLI + Skills ou MCP)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        O comando <code>npx ctx7 setup</code> autentica via OAuth, gera a chave de API e configura automaticamente a skill ou o servidor MCP no seu editor favorito:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Terminal (Requer Node.js >= 20.18 / 22.13)</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Setup interativo automático (escolha entre CLI+Skills ou MCP)
npx ctx7 setup

# Ou direcione para um agente específico:
npx ctx7 setup --claude
npx ctx7 setup --cursor
npx ctx7 setup --opencode

# Adicionar manualmente o servidor MCP no Claude Code (HTTP ou Stdio):
claude mcp add --scope user --transport http context7 https://mcp.context7.com/mcp
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp</code></pre>
                    </div>
                </div>

                <!-- 2. Uso Direto via CLI ctx7 -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #0284c7;">
                    <div class="ruflo-cheatsheet-title">
                        <span>⌨️</span> 2. Comandos da CLI <code>ctx7</code> (Modo Sem MCP)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        A skill <code>context7-cli</code> permite que o agente consulte documentações diretamente pelo terminal sem overhead de ferramentas MCP:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Comandos ctx7 CLI</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Passo 1: Resolver o Library ID oficial (sempre começa com '/')
npx ctx7@latest library next.js "app router proxy"

# Passo 2: Buscar a documentação ranqueada usando o Library ID
npx ctx7@latest docs /vercel/next.js "app router proxy"

# Ou fixando uma versão específica da biblioteca:
npx ctx7@latest docs /vercel/next.js/v16.2.9 "middleware cookies"
npx ctx7@latest docs /supabase/supabase "email password sign-up"</code></pre>
                    </div>
                </div>

                <!-- 3. Prompting & Regra Automática -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #8b5cf6;">
                    <div class="ruflo-cheatsheet-title">
                        <span>💡</span> 3. Dicas de Prompting (Library ID Direto) & Regra Automática (CLAUDE.md)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Use <code>use context7</code> ou informe diretamente o ID da biblioteca com barra (<code>/org/repo</code>) para pular a etapa de busca, ou adicione a regra abaixo no seu <code>CLAUDE.md</code> / <code>.cursorrules</code>:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Exemplos de Prompt & Regra para CLAUDE.md</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Prompt com use context7 e versão específica:
Create a Next.js 16 proxy that checks for a valid JWT in cookies and redirects to /login. use context7

# Prompt com Library ID direto (pula o resolve-library-id):
Implement basic authentication with Supabase. use library /supabase/supabase for API and docs.

# Regra recomendada para CLAUDE.md / Cursor Rules:
Always use Context7 when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initContext7View = initContext7View;
