document.addEventListener('DOMContentLoaded', () => {
    initGraphifyView();
});

function initGraphifyView() {
    if (typeof graphifyData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'graphify-view',
        title: 'Graphify (Graphify Labs)',
        badge: 'Codebase Knowledge Graph',
        icon: '🕸️',
        tagline: 'Transforme código, docs, PDFs, imagens e vídeos em um Knowledge Graph navegável e reduza o gasto de tokens em 80%',
        description: 'O <strong>Graphify</strong> mapeia toda a sua base de código (~40 linguagens via <code>tree-sitter</code> AST local, zero LLM), documentação, PDFs, imagens e vídeos em um grafo de conhecimento real (<code>graph.html</code>, <code>GRAPH_REPORT.md</code> e <code>graph.json</code>). Cada aresta possui tag de confiança (<code>EXTRACTED</code> vs <code>INFERRED</code>), detecção de comunidades (algoritmo Leiden) e God Nodes para que o agente consulte relações estruturais em vez de gastar tokens com buscas cegas de <code>grep</code>.',
        themeColor: '#8b5cf6',
        themeGradient: 'linear-gradient(135deg, #2e1065 0%, #0f172a 60%, #1e1b4b 100%)',
        githubRepo: 'https://github.com/Graphify-Labs/graphify',
        itemType: 'Graphify',
        pills: [
            { text: '⭐ GitHub: Graphify-Labs/graphify', link: 'https://github.com/Graphify-Labs/graphify' },
            { text: '🌐 docs.graphify.com', link: 'https://docs.graphify.com' },
            { text: '🌳 Tree-Sitter AST (~40 Linguagens)' },
            { text: '🏷️ Arestas EXTRACTED vs INFERRED' },
            { text: '📊 0.497 recall@10 (LOCOMO) • -80% Tokens' },
            { text: '🪐 Suporte Nativo Antigravity, Claude & Cursor' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todos os Documentos & Skills (26)' },
            { id: '1. Visão Geral', label: '🕸️ Visão Geral, Arquitetura & Benchmarks (8)' },
            { id: '2. Skills & Regras', label: '🪐 Skills & Regras Always-On (8)' },
            { id: '3. Referências', label: '🔍 Query, Path, Watch & Exports (8)' },
            { id: '4. Motor Python', label: '🐍 Motor Python Core (2)' },
            { id: 'cheatsheet', label: '⚡ Como Usar: CLI, /graphify & Consultas' }
        ],
        data: graphifyData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🕸️</span> Graphify — Instalação, Construção do Grafo & Comandos de Consulta
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Substitua buscas cegas por travessia determinística de grafo no seu assistente de IA.
                    </p>
                </div>

                <!-- 1. Instalação -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #8b5cf6;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🚀</span> 1. Instalação Rápida (Pacote Oficial PyPI: <code>graphifyy</code> com dois 'y')
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Instale via <code>uv</code> ou <code>pipx</code> e registre automaticamente a skill e a regra Always-On no seu agente (Antigravity, Claude Code, Cursor, Codex, Copilot, Kiro, Gemini CLI):
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Terminal</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Instalar a CLI (pacote PyPI oficial é graphifyy com duplo y)
uv tool install graphifyy
# ou: pipx install graphifyy

# Auto-detectar seu assistente e registrar a skill globalmente ou no projeto:
graphify install
graphify install --project

# Instalação específica por plataforma:
graphify antigravity install
graphify claude install --project
graphify cursor install</code></pre>
                    </div>
                </div>

                <!-- 2. Construindo e Consultando o Grafo -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🔍</span> 2. Mapeando o Projeto e Consultando (<code>explain</code>, <code>path</code>, <code>query</code>)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Gere <code>graphify-out/graph.html</code>, <code>GRAPH_REPORT.md</code> e <code>graph.json</code> e navegue pelas conexões com tags <code>[EXTRACTED]</code> e <code>[INFERRED]</code>:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>No Assistente ou Terminal</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># No chat do assistente de IA:
/graphify .

# Explicar todas as conexões de entrada/saída, comunidade Leiden e grau de um nó:
graphify explain "APIRouter"

# Descobrir o menor caminho (shortest path hop-by-hop) entre dois conceitos:
graphify path "FastAPI" "ModelField"

# Buscar um subgrafo com orçamento de tokens controlado para uma pergunta:
graphify query "como funciona o fluxo de autenticação?" --budget 2000</code></pre>
                    </div>
                </div>

                <!-- 3. Git Hooks, Watch, PR Blast Radius & Exports -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #0284c7;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🪝</span> 3. Sincronização Contínua (Watch / Git Hooks), Raio de Explosão de PRs & Exportações
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Mantenha o grafo sempre atualizado a cada commit e exporte para Obsidian, Neo4j ou servidor MCP:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Workflows Avançados</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Instalar Git Hooks (post-commit / post-checkout) ou rodar em modo Watch:
graphify hook install
graphify watch .

# Analisar o raio de explosão (nós e comunidades afetadas) de uma branch/PR:
graphify affected --base main

# Exportar como Wiki navegável do Obsidian ou subir servidor MCP local:
graphify ./src --obsidian ./meu-vault
python -m graphify.serve graphify-out/graph.json</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initGraphifyView = initGraphifyView;
