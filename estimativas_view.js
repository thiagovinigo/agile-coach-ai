document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('estimativas-view');
    if (!container) return;

    const techniques = [
        {
            title: "Planning Poker (Story Points)",
            desc: "Técnica baseada em consenso onde a equipe usa cartas com a sequência de Fibonacci (1, 2, 3, 5, 8, 13...) para estimar o esforço, complexidade e risco de uma tarefa.",
            when: "Equipes estabelecidas que precisam de conversas aprofundadas sobre requisitos e alinhamento de entendimento.",
            pros: ["Estimula o debate", "Evita o viés de ancoragem do líder", "Leva em conta incertezas"],
            cons: ["Pode ser demorado para backlogs muito grandes"]
        },
        {
            title: "T-Shirt Sizing (Tamanhos de Camiseta)",
            desc: "Estimativa em tamanhos relativos simplificados (PP, P, M, G, GG) sem tentar associar um número ou horas exatas logo de cara.",
            when: "Fases iniciais do projeto (Discovery) ou quando o backlog é muito extenso e precisa de uma estimativa grosseira e rápida.",
            pros: ["Muito rápido", "Fácil compreensão por pessoas não-técnicas", "Reduz a ansiedade dos números exatos"],
            cons: ["Dificuldade em prever velocidade métrica exata (Velocity) sem converter para números depois"]
        },
        {
            title: "Affinity Mapping (Agrupamento por Afinidade)",
            desc: "Os itens do backlog são agrupados visualmente em categorias de tamanho similar de forma silenciosa e colaborativa.",
            when: "Quando há necessidade de estimar dezenas ou centenas de itens rapidamente em uma única sessão (Release Planning).",
            pros: ["Extremamente rápido para grandes volumes", "Foco na comparação relativa e não no valor absoluto"],
            cons: ["Menos espaço para discussões detalhadas de cada item isolado"]
        },
        {
            title: "Magic Estimation",
            desc: "Uma variação do Affinity Mapping misturada com Planning Poker, onde os desenvolvedores colocam os cards de história sob valores de Story Points em silêncio.",
            when: "Refinamentos massivos onde o tempo é escasso e a equipe já tem uma boa sintonia.",
            pros: ["Zero debates intermináveis", "Foca no senso comum da equipe de forma rápida"],
            cons: ["Requer maturidade ágil para funcionar bem"]
        },
        {
            title: "Dot Voting (Votação por Pontos)",
            desc: "Cada membro recebe um número de 'pontos' (adesivos) e os distribui nas tarefas para indicar quais eles acham mais complexas ou prioritárias.",
            when: "Útil não apenas para estimar esforço, mas para definir prioridades e eleger os itens de maior risco.",
            pros: ["Excelente para priorização conjunta", "Garante que a voz de todos seja representada no placar"],
            cons: ["Não gera um 'tamanho' exato, apenas um ranking de complexidade"]
        },
        {
            title: "#NoEstimates (Foco em Fluxo)",
            desc: "A filosofia de parar de tentar prever horas ou pontos. Em vez disso, a equipe quebra todas as tarefas para o menor tamanho possível (itens de mesmo tamanho) e mede o Throughput (itens entregues por semana) usando estatística (Simulação de Monte Carlo).",
            when: "Equipes de alta maturidade (Kanban/Flow) onde a previsibilidade estatística se mostra mais valiosa do que adivinhar tamanhos.",
            pros: ["Elimina tempo desperdiçado em reuniões de estimativa", "Usa dados matemáticos e históricos reais"],
            cons: ["Difícil de vender para gestores tradicionais", "Requer capacidade de quebrar histórias perfeitamente"]
        }
    ];

    container.innerHTML = `
        <div class="card" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:2.5rem; box-shadow:0 4px 6px rgba(0,0,0,0.02); max-width: 1000px;">
            <div style="text-transform: uppercase; font-size: 0.85rem; color: #0078d4; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">📏 Base de Conhecimento</div>
            <h3 style="margin-bottom:1.2rem; color:#1a202c; font-size:2rem; border-bottom:1px solid #eee; padding-bottom: 1rem;">Técnicas de Estimativa Ágil</h3>
            
            <div style="display: flex; gap: 2rem; margin-bottom: 2rem; align-items: flex-start; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <p style="color:#4a5568; font-size:1.15rem; line-height:1.7;">
                        A estimativa ágil <strong>não é sobre acertar o tempo exato</strong> que uma tarefa vai levar (isso é adivinhação). 
                        O verdadeiro propósito das estimativas é gerar <strong>alinhamento de entendimento</strong>, revelar riscos ocultos e permitir o planejamento de capacidade usando comparação relativa.
                    </p>
                </div>
                
                <div style="flex: 1; min-width: 350px; background:#fefcbf; border-left:4px solid #d69e2e; padding:1.5rem; border-radius:8px;">
                    <h4 style="margin-top:0; color:#b7791f; margin-bottom:1rem; font-size:1.1rem;">💡 Princípios de Ouro</h4>
                    <ul style="margin:0; padding-left:20px; color:#5c4b13; font-size:0.95rem; line-height:1.6;">
                        <li style="margin-bottom:8px;">Estime <b>Complexidade, Esforço e Risco</b>, não horas absolutas.</li>
                        <li style="margin-bottom:8px;">Use a <b>Sabedoria das Multidões</b> (consenso da equipe bate a opinião do sênior).</li>
                        <li style="margin-bottom:8px;">O <b>Tamanho Relativo</b> (X é maior que Y) é mais preciso que a previsão exata.</li>
                        <li>Quem desenvolve é quem estima. Ponto final.</li>
                    </ul>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 20px;">
                ${techniques.map((t, i) => `
                    <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 25px; background: ${i % 2 === 0 ? '#f8fafc' : '#ffffff'}; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                        <div style="display:flex; align-items:center; gap: 10px; margin-bottom: 15px;">
                            <div style="background:#0078d4; color:white; width:30px; height:30px; display:flex; align-items:center; justify-content:center; border-radius:50%; font-weight:bold; font-size:1rem;">${i+1}</div>
                            <h4 style="margin: 0; color: #2d3748; font-size: 1.4rem;">${t.title}</h4>
                        </div>
                        
                        <p style="color: #4a5568; font-size: 1.05rem; line-height: 1.6; margin-bottom: 15px;">
                            ${t.desc}
                        </p>
                        
                        <div style="background: rgba(0,120,212,0.05); padding: 15px; border-radius: 6px; border-left: 3px solid #0078d4; margin-bottom: 15px;">
                            <strong style="color: #0078d4; font-size:0.95rem;">🎯 Quando Usar:</strong>
                            <p style="margin: 5px 0 0 0; color: #2d3748; font-size:0.95rem;">${t.when}</p>
                        </div>
                        
                        <div style="display:flex; gap:20px; flex-wrap:wrap;">
                            <div style="flex:1; min-width:250px;">
                                <strong style="color: #38a169; font-size:0.95rem;">✅ Pontos Fortes</strong>
                                <ul style="margin-top:5px; padding-left:20px; color:#4a5568; font-size:0.9rem;">
                                    ${t.pros.map(p => `<li style="margin-bottom:3px;">${p}</li>`).join('')}
                                </ul>
                            </div>
                            <div style="flex:1; min-width:250px;">
                                <strong style="color: #e53e3e; font-size:0.95rem;">⚠️ Atenção</strong>
                                <ul style="margin-top:5px; padding-left:20px; color:#4a5568; font-size:0.9rem;">
                                    ${t.cons.map(c => `<li style="margin-bottom:3px;">${c}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
});
