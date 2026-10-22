document.addEventListener('DOMContentLoaded', () => {
    initGsdView();
});

function initGsdView() {
    if (typeof gsdData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'gsd-view',
        title: 'Get Shit Done (GSD)',
        badge: 'Execution Framework',
        icon: '🎯',
        tagline: 'Esquadrão de agentes focados em execução veloz, pragmática e sem burocracia',
        description: 'O <strong>Get-Shit-Done (GSD)</strong> é um framework de agentes especializados que dividem e executam fases complexas de desenvolvimento de software: mapeamento de base de código, análise de suposições técnicas, facilitação de discussões, geração de planos, code review automático e correção de pendências.',
        themeColor: '#10b981',
        themeGradient: 'linear-gradient(135deg, #064e3b 0%, #0f172a 60%, #022c22 100%)',
        commandPrefix: '/gsd:',
        itemType: 'GSD Agents',
        pills: [
            { text: '🎯 30+ Agentes Especializados' },
            { text: '⚡ Execução Pragmática' },
            { text: '🗺️ Codebase Mapping' },
            { text: '🔍 Automated Code Review' },
            { text: '🛠️ Fast Issue Fixing' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todos os Agentes GSD (30+)' },
            { id: 'cheatsheet', label: '⚡ Fases do Framework GSD' }
        ],
        data: gsdData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🎯</span> Fluxo Operacional das Fases GSD
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Como o framework coordena seus agentes para entregar funcionalidades completas.
                    </p>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>1️⃣</span> Fase de Descoberta & Mapeamento
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        O <code>gsd-codebase-mapper</code> e o <code>gsd-assumptions-analyzer</code> examinam o repositório e identificam padrões arquiteturais sem alterar nada.
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Comando de Execução</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>/gsd:map-codebase "Mapear a arquitetura e fluxos de dados deste módulo"</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #0284c7;">
                    <div class="ruflo-cheatsheet-title">
                        <span>2️⃣</span> Fase de Planejamento & Fatiamento
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        O <code>gsd-plan-generator</code> quebra a entrega em passos atômicos, seguros e fáceis de testar.
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Comando de Execução</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>/gsd:plan-feature "Gerar plano de implementação com critérios de aceite"</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #8b5cf6;">
                    <div class="ruflo-cheatsheet-title">
                        <span>3️⃣</span> Fase de Review & Fix Automatizado
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        O <code>gsd-code-reviewer</code> detecta violações e o <code>gsd-code-fixer</code> aplica correções cirúrgicas de código.
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Comando de Execução</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>/gsd:review-and-fix "Auditar o último commit e corrigir apontamentos"</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initGsdView = initGsdView;
