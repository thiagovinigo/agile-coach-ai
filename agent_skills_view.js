document.addEventListener('DOMContentLoaded', () => {
    initAgentSkillsView();
});

function initAgentSkillsView() {
    if (typeof agentSkillsData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'agent-skills-view',
        title: 'Agent Skills (Addy Osmani)',
        badge: 'Production Engineering Suite',
        icon: '💻',
        tagline: 'Production-grade engineering skills, slash commands, subagents e quality gates para Agentes de IA (por Addy Osmani)',
        description: 'O repositório <strong>addyosmani/agent-skills</strong> codifica os fluxos de trabalho, <em>quality gates</em> e boas práticas que engenheiros seniores utilizam em todas as fases do ciclo de vida de software (<code>DEFINE /spec</code> → <code>PLAN /plan</code> → <code>BUILD /build</code> → <code>VERIFY /test</code> → <code>REVIEW /review</code> → <code>SHIP /ship</code>), incluindo <strong>24 Skills de Engenharia</strong>, <strong>8 Slash Commands</strong>, <strong>4 Sub-Agentes Especializados</strong>, <strong>Checklists de Referência</strong>, <strong>Hooks</strong> e <strong>Suíte de Evals</strong>.',
        themeColor: '#06b6d4',
        themeGradient: 'linear-gradient(135deg, #083344 0%, #0f172a 60%, #164e63 100%)',
        githubRepo: 'https://github.com/addyosmani/agent-skills',
        itemType: 'Agent Skills',
        pills: [
            { text: '⭐ GitHub: addyosmani/agent-skills', link: 'https://github.com/addyosmani/agent-skills' },
            { text: '💻 24 Skills de Engenharia' },
            { text: '⚡ 8 Slash Commands (/spec → /ship)' },
            { text: '🤖 4 Sub-Agentes Especializados' },
            { text: '✅ 7 Checklists + Hooks + Evals' },
            { text: '🌐 Chrome DevTools MCP & Core Web Vitals' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Catálogo Completo (59)' },
            { id: '1. Visão Geral', label: '📘 Setup & Guias por IDE (13)' },
            { id: '2. Slash Commands', label: '⚡ Slash Commands (8)' },
            { id: '3. Sub-Agentes', label: '🤖 Sub-Agentes (4)' },
            { id: '4. Skills de Engenharia', label: '💻 Skills de Engenharia (24)' },
            { id: '5. Checklists', label: '✅ Checklists, Hooks & Evals (10)' },
            { id: 'cheatsheet', label: '🚀 Ciclo de Vida, CLI & /build auto' }
        ],
        data: agentSkillsData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>💻</span> Addy Osmani Agent Skills — Ciclo de Vida, Instalação & Invocação
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Como instalar em 70+ agentes (Claude Code, Antigravity, Cursor, Windsurf, Copilot, Gemini CLI, Codex) e operar os 8 comandos do ciclo de engenharia.
                    </p>
                </div>

                <!-- 1. Quick Start CLI -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #06b6d4;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🚀</span> 1. Instalação Rápida (Skills CLI & Claude Code Plugin)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Instale todas as 24 skills ou escolha habilidades individuais em qualquer agente compatível:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Terminal / Claude Code</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Instalar todas as 24 skills em 70+ agentes via Skills CLI
npx skills add addyosmani/agent-skills
npx skills add addyosmani/agent-skills --list

# Instalar skills específicas
npx skills add addyosmani/agent-skills --skill code-review-and-quality
npx skills add addyosmani/agent-skills --skill interview-me
npx skills add addyosmani/agent-skills --skill test-driven-development

# Ou instalar como Plugin nativo no Claude Code
/plugin marketplace add https://github.com/addyosmani/agent-skills.git
/plugin install agent-skills@addy-agent-skills</code></pre>
                    </div>
                </div>

                <!-- 2. O Ciclo de 8 Comandos -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🔄</span> 2. Os 8 Slash Commands do Ciclo de Desenvolvimento
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Cada comando ativa automaticamente as skills e checklists correspondentes para aquela etapa:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Fluxo Completo (DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP)</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>/spec           # 1. DEFINE: Especifica o que construir antes de codar (ativa interview-me + spec-driven-development)
/plan           # 2. PLAN: Quebra a spec em tarefas pequenas, atômicas e verificáveis
/build          # 3. BUILD: Implementa uma fatia por vez com TDD (ou use '/build auto' para rodar todo o plano aprovado)
/test           # 4. VERIFY: Prova empírica com testes unitários, integração e DevTools
/review         # 5. REVIEW: Code Review em 5 eixos (Corretude, Legibilidade, Arquitetura, Segurança, Performance)
/webperf        # 6. PERF: Auditoria Core Web Vitals (LCP, CLS, INP) e bundle size
/code-simplify  # 7. SIMPLIFY: Refatora priorizando clareza sobre código 'esperto'
/ship           # 8. SHIP: Checklist pré-lançamento, validação CI e plano de rollback</code></pre>
                    </div>
                </div>

                <!-- 3. Chrome DevTools MCP & Performance -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #8b5cf6;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🌐</span> 3. Testes Reais em Navegador (Chrome DevTools MCP)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Configure o servidor MCP do Chrome DevTools com perfil isolado (<code>--isolated</code>) para dar visão real de runtime ao agente:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>.mcp.json</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--isolated"]
    }
  }
}</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initAgentSkillsView = initAgentSkillsView;
