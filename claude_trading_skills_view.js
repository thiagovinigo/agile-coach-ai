// View Controller para Claude Trading Skills (https://github.com/tradermonty/claude-trading-skills)
// Construído sobre a engine universal window.createStandardToolView

function initClaudeTradingSkillsView() {
    const data = typeof claudeTradingSkillsData !== 'undefined' ? claudeTradingSkillsData : window.claudeTradingSkillsData;
    if (!data || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'claude-trading-skills-view',
        title: 'Claude Trading Skills (TraderMonty)',
        badge: 'Systematic Trading & Risk Systems',
        icon: '📈',
        tagline: 'Toolkit open-source de trading em Claude Skills para investidores e swing traders — market regime, risk gates, VCP/CANSLIM screeners, journaling e backtesting',
        description: 'O <strong>Claude Trading Skills (tradermonty/claude-trading-skills)</strong> é um ecossistema completo de fluxos de trabalho e competências em IA para investidores com tempo limitado. Estruturado na filosofia <em>"First for Self, Open for Others"</em>, o projeto não busca terceirizar decisões de compra/venda para a IA, mas sim estruturar a <strong>revisão de regime de mercado, gestão rígida de risco, dimensionamento de posições (Position Sizer), screening (VCP/CANSLIM) e journaling de aprendizado contínuo</strong> com e sem APIs de dados pagas.',
        themeColor: '#059669',
        themeGradient: 'linear-gradient(135deg, #022c22 0%, #0f172a 60%, #064e3b 100%)',
        githubRepo: 'https://github.com/tradermonty/claude-trading-skills',
        itemType: 'Trading Skill',
        pills: [
            { text: '⭐ GitHub: tradermonty/claude-trading-skills', link: 'https://github.com/tradermonty/claude-trading-skills' },
            { text: '🌐 Docs Oficiais', link: 'https://tradermonty.github.io/claude-trading-skills/' },
            { text: '🛡️ Risk First: Drawdown Circuit Breakers' },
            { text: '🎯 74 Skills Catalogadas & 13 Workflows' },
            { text: '🆓 No API Starter Path (Gratuito sem APIs)' },
            { text: '📓 Trade Memory Loop & Journaling' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Catálogo Completo (90)' },
            { id: '1. Visão Geral', label: '🧭 Visão & Workflows (17)' },
            { id: '2. Market Regime', label: '🌐 Market Regime & Macro (16)' },
            { id: '3. Core Portfolio', label: '💼 Core Portfolio & Dividendos (7)' },
            { id: '4. Swing Opportunity', label: '🎯 Swing & Screeners (7)' },
            { id: '5. Trade Planning', label: '🛡️ Trade Planning & Risk (7)' },
            { id: '6. Trade Memory', label: '🧠 Trade Memory & Journal (6)' },
            { id: '7. Strategy Research', label: '🧪 Research & Backtest (14)' },
            { id: '8. Advanced Satellite', label: '🛰️ Advanced & Meta (16)' },
            { id: 'cheatsheet', label: '⚡ Quickstart & 5 Skills Sem API' }
        ],
        data: data,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>📈</span> Claude Trading Skills — Quickstart & Guia Prático
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Instruções para rodar os 5 fluxos operacionais recomendados e como usar as 5 skills sem pagar por APIs de dados.
                    </p>
                </div>

                <!-- 1. Starter Path Sem API -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #059669;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🆓</span> 1. Caminho Inicial Sem API Paga (No API Key Starter Path)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Se você não assina FMP, FINVIZ Elite ou Alpaca, pode rodar o ciclo completo usando CSVs públicos, prints de gráficos e arquivos locais:
                    </p>
                    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:12px; margin-bottom:14px;">
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px;">
                            <strong style="color:#0f172a;">1. 🌐 market-breadth-analyzer</strong>
                            <div style="font-size:13px; color:#64748b; margin-top:4px;">Pontua a amplitude de mercado a partir de CSV público sem chave de API.</div>
                        </div>
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px;">
                            <strong style="color:#0f172a;">2. 📈 uptrend-analyzer</strong>
                            <div style="font-size:13px; color:#64748b; margin-top:4px;">Calcula a participação em tendência de alta (MM50, MM200) via dados abertos.</div>
                        </div>
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px;">
                            <strong style="color:#0f172a;">3. 🛡️ position-sizer</strong>
                            <div style="font-size:13px; color:#64748b; margin-top:4px;">Cálculo puro de risco por trade (1%), distância do stop e Kelly Criterion sem I/O de rede.</div>
                        </div>
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px;">
                            <strong style="color:#0f172a;">4. 🧠 trader-memory-core</strong>
                            <div style="font-size:13px; color:#64748b; margin-top:4px;">Diário de bordo local em YAML com teses, gatilhos de entrada e motivos de saída.</div>
                        </div>
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px;">
                            <strong style="color:#0f172a;">5. 🔍 signal-postmortem</strong>
                            <div style="font-size:13px; color:#64748b; margin-top:4px;">Framework de autópsia após o encerramento do trade para identificar falhas cognitivas ou técnicas.</div>
                        </div>
                    </div>
                </div>

                <!-- 2. Os 5 Workflows Operacionais -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #0284c7;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🔄</span> 2. Os 5 Workflows Operacionais Recomendados
                    </div>
                    <table class="tool-markdown-table" style="margin-top:10px;">
                        <thead>
                            <tr>
                                <th>Objetivo</th>
                                <th>Workflow Manifest</th>
                                <th>Skills Principais</th>
                                <th>Requisito de API</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Checagem diária de 15 min</strong></td>
                                <td><code>market-regime-daily</code></td>
                                <td><code>market-breadth-analyzer</code>, <code>uptrend-analyzer</code>, <code>exposure-coach</code></td>
                                <td>Sem API paga</td>
                            </tr>
                            <tr>
                                <td><strong>Revisão semanal de portfólio</strong></td>
                                <td><code>core-portfolio-weekly</code></td>
                                <td><code>portfolio-manager</code>, <code>kanchi-dividend-review-monitor</code>, <code>trader-memory-core</code></td>
                                <td>Alpaca (ou CSV manual)</td>
                            </tr>
                            <tr>
                                <td><strong>Oportunidades de Swing</strong></td>
                                <td><code>swing-opportunity-daily</code></td>
                                <td><code>vcp-screener</code>, <code>drawdown-circuit-breaker</code>, <code>position-sizer</code>, <code>pre-trade-discipline-gate</code></td>
                                <td>FMP (para screener)</td>
                            </tr>
                            <tr>
                                <td><strong>Ciclo de Memória e Journal</strong></td>
                                <td><code>trade-memory-loop</code></td>
                                <td><code>trader-memory-core</code>, <code>signal-postmortem</code></td>
                                <td>Sem API paga (YAML local)</td>
                            </tr>
                            <tr>
                                <td><strong>Revisão Mensal & Ajuste de Regras</strong></td>
                                <td><code>monthly-performance-review</code></td>
                                <td><code>trader-memory-core</code>, <code>signal-postmortem</code>, <code>backtest-expert</code></td>
                                <td>Sem API paga</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- 3. Exemplo Prático Position Sizer -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #f59e0b;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🧮</span> 3. Como Usar o Position Sizer no Terminal ou Claude
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Calcule o lote ideal de ações respeitando a regra de 1% de risco sobre o patrimônio líquido:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Exemplo de Prompt no Claude ou Terminal</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Exemplo de chamada direta para o Claude com a skill position-sizer:
"Tenho uma conta de US$ 25.000. Quero comprar AAPL a US$ 225,00 com stop em US$ 218,00. 
Risco máximo de 1% do patrimônio por operação. 
Use a skill position-sizer para calcular quantas ações devo comprar e qual será meu risco total em dólares."

# Resposta estruturada retornada:
# - Capital Total: US$ 25.000,00
# - Risco Máximo (1%): US$ 250,00
# - Distância do Stop: US$ 7,00 (3,11%)
# - Quantidade Recomendada: 35 ações (US$ 7.875,00 de exposição = 31,5% da conta)
# - Perda no Stop: US$ 245,00 (dentro do limite)</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initClaudeTradingSkillsView);
} else {
    initClaudeTradingSkillsView();
}
window.renderClaudeTradingSkillsView = initClaudeTradingSkillsView;
