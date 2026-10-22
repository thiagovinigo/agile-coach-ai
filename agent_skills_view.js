document.addEventListener('DOMContentLoaded', () => {
    initAgentSkillsView();
});

function initAgentSkillsView() {
    if (typeof agentSkillsData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'agent-skills-view',
        title: 'Agent Skills',
        badge: 'Engineering Capabilities',
        icon: '💻',
        tagline: 'Competências nucleares de engenharia e desenvolvimento para Agentes Autônomos',
        description: 'As <strong>Agent Skills</strong> englobam capacidades técnicas fundamentais para que o agente atue como um engenheiro sênior: design de APIs, testes em navegador real com DevTools MCP, pipelines de CI/CD, engenharia de contexto, refatoração e otimização de performance.',
        themeColor: '#06b6d4',
        themeGradient: 'linear-gradient(135deg, #083344 0%, #0f172a 60%, #164e63 100%)',
        itemType: 'Agent Skills',
        pills: [
            { text: '💻 25+ Skills de Engenharia' },
            { text: '🌐 Chrome DevTools MCP' },
            { text: '🚀 CI/CD & Deploy' },
            { text: '🧠 Context Engineering' },
            { text: '⚡ Performance Profiling' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todas as Agent Skills' },
            { id: 'cheatsheet', label: '⚡ Guia de Invocação Rápida' }
        ],
        data: agentSkillsData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>💻</span> Invocação de Agent Skills no seu Editor
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Instruções para aplicar as habilidades no Cursor, Windsurf ou Claude Code.
                    </p>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #06b6d4;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🌐</span> Testes Reais em Navegador (DevTools)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Peça para o agente verificar o DOM, erros de console e performance real:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Prompt para o Agente</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>Aja seguindo a skill agent-skills/skills/browser-testing-with-devtools/SKILL.md:
Abra a URL no navegador via DevTools, inspecione a renderização e verifique se há exceções no console.</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #8b5cf6;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🧠</span> Otimização de Contexto (Context Engineering)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Evite estourar a janela de contexto selecionando apenas os arquivos estritamente relevantes:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Prompt para o Agente</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>Aplique a skill agent-skills/skills/context-engineering/SKILL.md para podar o contexto e focar apenas no módulo afetado.</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initAgentSkillsView = initAgentSkillsView;
