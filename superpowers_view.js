document.addEventListener('DOMContentLoaded', () => {
    initSuperpowersView();
});

function initSuperpowersView() {
    if (typeof superpowersData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'superpowers-view',
        title: 'Superpowers',
        badge: 'Engineering Rigor',
        icon: '⚡',
        tagline: 'Métodos avançados e diretrizes de engenharia disciplinada para Agentes Autônomos',
        description: 'O <strong>Superpowers</strong> fornece um conjunto de skills com regras inquebráveis para agentes de IA: desenvolvimento guiado por testes (TDD), investigação de causa-raiz sistemática antes de propor correções, planos executáveis passo a passo e despacho seguro de sub-agentes paralelos.',
        themeColor: '#f59e0b',
        themeGradient: 'linear-gradient(135deg, #451a03 0%, #0f172a 60%, #1c1917 100%)',
        githubRepo: 'https://github.com/obra/superpowers',
        commandPrefix: '/superpowers:',
        itemType: 'Superpowers',
        pills: [
            { text: '⭐ GitHub: obra/superpowers', link: 'https://github.com/obra/superpowers' },
            { text: '⚡ 14 Superpowers Ativos' },
            { text: '🧪 Test-Driven Development (TDD)' },
            { text: '🛡️ Systematic Debugging' },
            { text: '🤖 Subagent-Driven Development' },
            { text: '📋 Verification Before Completion' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todos os Superpowers (14)' },
            { id: 'cheatsheet', label: '⚡ Como Invocar & Regras de Ouro' }
        ],
        data: superpowersData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>⚡</span> Superpowers Cheat Sheet & Regras de Invocação
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Como ensinar e exigir que sua IA aplique rigor de engenharia e disciplina de software.
                    </p>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #f59e0b;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🧪</span> 1. Test-Driven Development (TDD)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Nunca permita que o agente escreva a implementação antes de ver o teste falhar:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Prompt para o Agente</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>Aja seguindo estritamente o manual /superpowers:test-driven-development:
1. Escreva um teste unitário que falhe cobrindo o novo requisito.
2. Execute a suíte e confirme a falha.
3. Escreva o código mínimo necessário para fazer o teste passar.
4. Refatore mantendo todos os testes verdes.</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #ef4444;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🔍</span> 2. Systematic Debugging (Sem Suposições)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Proíba o agente de propor "chutes" ou correções aleatórias sem prova empírica da causa raiz:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Prompt para o Agente</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>Aplique a skill /superpowers:systematic-debugging para investigar este bug:
- Fase 1: Isole e reproduza o problema com evidência em log ou teste mínimo.
- Fase 2: Identifique a causa raiz exata antes de editar qualquer código produtivo.
- Fase 3: Proponha a correção cirúrgica e valide a não-regressão.</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>✅</span> 3. Verification Before Completion
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Evite alucinações onde o agente diz "tudo pronto" sem ter executado os testes:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Prompt para o Agente</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>Antes de concluir esta tarefa, execute a skill /superpowers:verification-before-completion.
Apresente a saída real do terminal com os testes passando e linters sem erros antes de declarar o trabalho finalizado.</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initSuperpowersView = initSuperpowersView;
