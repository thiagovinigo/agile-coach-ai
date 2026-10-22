document.addEventListener('DOMContentLoaded', () => {
    initPmSkillsView();
});

function initPmSkillsView() {
    if (typeof pmSkillsData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'pm-skills-view',
        title: 'Jornada PM Skills',
        badge: 'Product Management Suite',
        icon: '🎒',
        tagline: 'O ecossistema completo de skills de Product Management para Claude Code e IA',
        description: 'A <strong>Jornada PM Skills</strong> equipa seu assistente com playbooks comprovados de Product Management: da concepção e discovery (Personas, JTBD, Árvore de Oportunidades) até delivery (PRD, User Stories, Gherkin), estratégia (RICE, OKRs, North Star Metric) e validação estatística de A/B tests.',
        themeColor: '#0284c7',
        themeGradient: 'linear-gradient(135deg, #082f49 0%, #0f172a 60%, #172554 100%)',
        commandPrefix: '/pm:',
        itemType: 'PM Skills',
        pills: [
            { text: '🎒 30+ Skills de Produto' },
            { text: '🔬 Discovery & JTBD' },
            { text: '📄 PRD & User Stories' },
            { text: '🎯 OKRs & North Star' },
            { text: '📊 A/B Testing & PMF' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todas as PM Skills' },
            { id: 'DISCOVERY', label: '🔬 Discovery' },
            { id: 'DELIVERY', label: '📄 Delivery' },
            { id: 'STRATEGY', label: '🎯 Strategy' },
            { id: 'cheatsheet', label: '⚡ Workflows Prontos de PM' }
        ],
        data: pmSkillsData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🎒</span> Receitas de Workflows Encadeados para PMs
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Combine skills sequencialmente para resolver desafios de produto do mundo real.
                    </p>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #0284c7;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🚀</span> Receita 1: Da Ideia ao PRD Fatiado
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Fluxo de 4 passos para transformar um problema vago em histórias prontas para desenvolvimento:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Sequência de Comandos no Claude Code</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>1. /discovery "Problema dos usuários que não concluem o onboarding"
2. /opportunity-tree "Mapear oportunidades a partir dos achados do discovery"
3. /prd "Escrever PRD para a oportunidade vencedora"
4. /user-stories "Fatiar o PRD em user stories INVEST com critérios de aceite"</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🧪</span> Receita 2: Experimento Lean & A/B Testing
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Validação de hipóteses sem desperdício de esforço de engenharia:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Sequência de Comandos no Claude Code</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>1. /hypothesis "Desenhar hipótese testável com falsifiabilidade"
2. /experiment-design "Criar pretótipo ou A/B test com métrica guardrail"
3. /ab-test-analysis "Avaliar significância estatística e recomendação ship/kill"</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initPmSkillsView = initPmSkillsView;
