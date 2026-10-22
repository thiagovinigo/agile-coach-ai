document.addEventListener('DOMContentLoaded', () => {
    initSpecDrivenView();
});

function initSpecDrivenView() {
    if (typeof specDrivenData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'spec-driven-view',
        title: 'Spec-Driven Development (SDD)',
        badge: 'Specification First',
        icon: '🎯',
        tagline: 'Scaffold e arquitetura guiada por especificações rígidas para Agentes de IA',
        description: 'O <strong>Spec-Driven Development</strong> (por Igor Uehara) introduz uma abordagem onde o código só é gerado após a especificação clara dos requisitos, camadas agênticas, diagramas, evals e regras arquiteturais. Elimina retrabalho e alucinações de escopo.',
        themeColor: '#6366f1',
        themeGradient: 'linear-gradient(135deg, #312e81 0%, #0f172a 60%, #1e1b4b 100%)',
        githubRepo: 'https://github.com/igoruehara/spec-driven.git',
        commandPrefix: '/spec-driven:',
        itemType: 'Spec-Driven',
        pills: [
            { text: '⭐ GitHub: igoruehara/spec-driven', link: 'https://github.com/igoruehara/spec-driven.git' },
            { text: '🎯 SDD Architecture' },
            { text: '📐 Camadas Agênticas' },
            { text: '⚖️ Evals & Benchmarks' },
            { text: '🤝 Context Handoff' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todas as Especificações & Skills' },
            { id: 'cheatsheet', label: '⚡ Como Aplicar Spec-Driven' }
        ],
        data: specDrivenData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🎯</span> Guia Rápido: O Ciclo Spec-Driven (SDD)
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Desenvolva funcionalidades à prova de falhas guiando o agente através de especificações completas.
                    </p>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #6366f1;">
                    <div class="ruflo-cheatsheet-title">
                        <span>1️⃣</span> Clarificar Requisitos
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Use a skill <code>clarificar</code> para remover ambiguidades antes de escrever qualquer código.
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Comando</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>Aja conforme spec-driven/template/.claude/skills/clarificar/SKILL.md para auditar os requisitos da tarefa.</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>2️⃣</span> Auditar Código contra a Especificação
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Use a skill <code>auditar</code> para validar se a implementação satisfaz 100% dos contratos descritos.
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Comando</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>Execute a auditoria de conformidade utilizando spec-driven/template/.claude/skills/auditar/SKILL.md.</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initSpecDrivenView = initSpecDrivenView;
