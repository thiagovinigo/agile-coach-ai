function initDiscoveryIaView() {
    const data = typeof discoveryIaData !== 'undefined' ? discoveryIaData : window.discoveryIaData;
    if (!data || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'discovery-ia-view',
        title: 'Discovery de IA e Automação (Flow Mastermind)',
        badge: 'Metodologia Oficial · Ric Neves',
        icon: '🧭',
        tagline: 'O método completo de 3 semanas para sair do pedido "queremos usar IA" para um inventário auditável com horas, custo e roadmap de 90 dias',
        description: 'A metodologia de <strong>Discovery de IA e Automação (Flow Mastermind · Ric Neves)</strong> estrutura entrevistas de 2 horas por área, aplica a <em>regra de ouro dos 4 números</em>, calcula capacidade liberada (horas × custo-hora), gera o score ponderado de priorização, posiciona oportunidades na Matriz Impacto × Esforço e entrega um <strong>roadmap executivo em 3 ondas</strong> com governança e aprovação dos sponsors.',
        themeColor: '#0d9488',
        themeGradient: 'linear-gradient(135deg, #042f2e 0%, #0f172a 60%, #115e59 100%)',
        githubRepo: 'https://ricneves.ai',
        itemType: 'Discovery de IA',
        pills: [
            { text: '🔍 Abrir Apresentação Interativa', link: '#flowgrammers-discovery-view' },
            { text: '📊 10 Abas & Inventário Automático' },
            { text: '🎙️ Roteiro 2h com 40 Perguntas' },
            { text: '📝 Ficha de Processo com 22 Campos' },
            { text: '🧮 Score Ponderado & 4 Quadrantes' },
            { text: '📥 Planilhas XLSX & Guia PDF Inclusos' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Metodologia Completa (8)' },
            { id: '1. Metodologia', label: '🧭 Guia do Consultor (3)' },
            { id: '2. Roteiro', label: '🎙️ Roteiro 2h (40 Perguntas) (2)' },
            { id: '3. Fichas', label: '📝 Fichas de Processo (2)' },
            { id: '4. As Contas', label: '🧮 Score, Fórmulas & Matriz (1)' },
            { id: '5. Inventário', label: '🏢 Inventário 10 Áreas (1)' },
            { id: '6. Top 10', label: '🏆 Top 10 & Roadmap (1)' },
            { id: '7. Downloads', label: '📦 Downloads & Skills (1)' },
            { id: 'cheatsheet', label: '🚀 Checklist Rápido de 2 Horas' }
        ],
        data: data,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🧭</span> Discovery de IA — Checklist & Roteiro Rápido da Entrevista
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Passo a passo para conduzir a entrevista de 2 horas e links diretos para baixar o kit de planilhas.
                    </p>
                </div>

                <!-- 1. Cronômetro da Entrevista -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #0d9488;">
                    <div class="ruflo-cheatsheet-title">
                        <span>⏱️</span> 1. Distribuição dos 120 Minutos da Entrevista
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Mantenha o controle do tempo olhando para o relógio e gravando com Plaud ou Granola:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Agenda 2 Horas</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>B1 · Abertura e combinados (10 min)  -> Gravação + combinados (não é auditoria)
B2 · Contexto e estratégia (15 min) -> Missão, KPIs e onde colocar 20% de ganho
B3 · Mapa de processos (40 min)     -> 5 a 8 processos, demo na tela, 4 números
B4 · Dados e sistemas (15 min)      -> Formatos (XML, PDF, fotos), APIs e LGPD
B5 · Dores e custos (15 min)        -> Custo do erro, travas e controles paralelos
B6 · Oportunidades (15 min)         -> Assistente 24h, relatórios e vitória em 30d
B7 · Riscos e governança (5 min)    -> Onde erro é inaceitável + embaixadores
B8 · Fechamento (5 min)             -> Recap 3 achados + agendamento de 15 min</code></pre>
                    </div>
                </div>

                <!-- 2. A Regra dos 4 Números -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #f59e0b;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🔢</span> 2. Os 4 Números Obrigatórios de Cada Processo
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Nunca encerre a discussão de um processo sem colher:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Sondagem em Campo</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>1. Volume por mês: "Quantas vezes esse processo roda no mês típico?"
2. Minutos no caso padrão: "No caso simples sem divergência, quantos minutos leva?"
3. Pessoas envolvidas: "Quantas pessoas do time executam essa tarefa?"
4. % de exceções: "Que porcentagem dos casos dá algum problema ou foge da regra?"</code></pre>
                    </div>
                </div>

                <!-- 3. Downloads Imediatos -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #6366f1;">
                    <div class="ruflo-cheatsheet-title">
                        <span>📥</span> 3. Baixar Materiais do Kit de Discovery
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Arquivos prontos para uso em clientes reais:
                    </p>
                    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:8px;">
                        <a href="contexto/discovery/discovery-ia-template.xlsx" download="discovery-ia-template.xlsx" style="background:#0d9488; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">⬇️ Planilha Template (.xlsx)</a>
                        <a href="contexto/discovery/discovery-ia-exemplo-preenchido.xlsx" download="discovery-ia-exemplo-preenchido.xlsx" style="background:#0f172a; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">⬇️ Exemplo Preenchido Atacarejo (.xlsx)</a>
                        <a href="contexto/discovery/guia-do-consultor-discovery-ia.pdf" download="guia-do-consultor-discovery-ia.pdf" style="background:#0f172a; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">⬇️ Guia do Consultor (PDF 48 págs)</a>
                        <a href="contexto/discovery_que_vira_projeto.html" download="Discovery_que_Vira_Projeto_Flowgrammers.html" style="background:#f1f5f9; color:#0f172a; border:1px solid #cbd5e1; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">🎓 Baixar Apresentação Interativa (.html)</a>
                    </div>
                </div>
            </div>
        `
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDiscoveryIaView);
} else {
    initDiscoveryIaView();
}
window.renderDiscoveryIaView = initDiscoveryIaView;
