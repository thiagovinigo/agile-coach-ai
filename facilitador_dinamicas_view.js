document.addEventListener('DOMContentLoaded', () => {
    initFacilitadorDinamicasView();
});

function initFacilitadorDinamicasView() {
    const container = document.getElementById('facilitador-dinamicas-view');
    if(!container) return;

    const dinamicasData = {
        "Lean Inception (Caroli)": [
            {
                title: "Visão do Produto (É / Não É / Faz / Não Faz)",
                icon: "🎯",
                detail: "Dinâmica fundamental para alinhar o que o produto representa. Ajuda a definir os limites do produto de forma colaborativa, evitando escopo excessivo logo no início.",
                examples: "Usada no Kick-off de um novo aplicativo de delivery para garantir que todos entendam que o app 'Não É' uma transportadora e 'Não Faz' compras de supermercado.",
                execution: `
                    <ol>
                        <li>Divida o quadro (físico ou Miro/Mural) em 4 quadrantes: É, Não É, Faz, Não Faz.</li>
                        <li>Dê 5 minutos para os participantes escreverem post-its individualmente sobre o produto.</li>
                        <li>Cada participante cola seus post-its lendo em voz alta.</li>
                        <li>O facilitador agrupa post-its similares e promove debates sobre discordâncias (ex: alguém colocou algo no 'Faz' que o PO acha que é 'Não Faz').</li>
                        <li>A equipe chega a um consenso sobre cada quadrante.</li>
                    </ol>
                `,
                result: "Um quadro consolidado que serve como bússola do produto. Reduz radicalmente dúvidas de escopo nas etapas seguintes."
            },
            {
                title: "Sequenciador de Funcionalidades",
                icon: "🌊",
                detail: "Técnica para organizar as features do produto em 'ondas' de entrega (releases). Foca em entregar valor rápido e testar hipóteses, compondo o MVP.",
                examples: "Priorizar quais features entram no MVP de um e-commerce (ex: 'Carrinho' e 'Pagamento Pix' na Onda 1, 'Recomendações de IA' na Onda 3).",
                execution: `
                    <ol>
                        <li>Apresente as regras do Sequenciador: Uma onda pode ter no máximo 3 cartões. Não pode ter mais de um cartão de alto esforço na mesma onda.</li>
                        <li>Apresente as funcionalidades previamente mapeadas e estimadas (esforço, valor pro negócio, valor pro usuário).</li>
                        <li>O time começa a alocar os cartões nas Ondas (1, 2, 3...).</li>
                        <li>O facilitador provoca: 'Isso é realmente necessário para o MVP?', 'Podemos fatiar essa feature para caber na Onda 1?'.</li>
                        <li>Defina uma linha de corte clara para o MVP.</li>
                    </ol>
                `,
                result: "Um roadmap visual de releases. A 'Onda 1' + 'Onda 2' geralmente formam o MVP, com as ondas seguintes formando o roadmap futuro de evolução do produto."
            }
        ],
        "Scrum & Retrospectivas": [
            {
                title: "Retrospectiva: Barco à Vela (Sailboat)",
                icon: "⛵",
                detail: "Inspirada no 'Fun Retrospectives', usa a metáfora de um barco para identificar o que impulsiona o time e o que os está atrasando.",
                examples: "Ideal para times que estão estagnados ou que acabaram de passar por uma Sprint difícil com muitos impedimentos externos.",
                execution: `
                    <ol>
                        <li>Desenhe um barco com velas, âncoras, vento soprando e recifes de coral à frente.</li>
                        <li><strong>Vento (O que nos empurra pra frente?):</strong> Participantes colocam post-its com coisas boas da Sprint.</li>
                        <li><strong>Âncora (O que nos segura?):</strong> Post-its com problemas e impedimentos.</li>
                        <li><strong>Recifes (Riscos futuros):</strong> O que pode dar errado na próxima Sprint.</li>
                        <li><strong>Ilha (Objetivo):</strong> Onde queremos chegar.</li>
                        <li>Agrupe os itens da Âncora, vote nos mais críticos e defina Planos de Ação (Ação, Responsável, Prazo).</li>
                    </ol>
                `,
                result: "Lista clara de ações de melhoria com donos definidos, além de um mapeamento visual de riscos e celebração dos pontos fortes."
            },
            {
                title: "Planning Poker (Estimativa Relativa)",
                icon: "🃏",
                detail: "Dinâmica de consenso baseada na sequência de Fibonacci para estimar o esforço/complexidade das User Stories, evitando o viés da ancoragem.",
                examples: "Refinamento de Backlog onde um Dev Sênior e um Dev Júnior costumam discordar sobre o tempo de uma tarefa.",
                execution: `
                    <ol>
                        <li>O PO lê a User Story e tira as dúvidas do time.</li>
                        <li>Cada membro do time de desenvolvimento escolhe uma carta (1, 2, 3, 5, 8, 13...) que representa o tamanho do item.</li>
                        <li>Todos revelam as cartas simultaneamente (evita que um influencie o outro).</li>
                        <li>Se houver grande divergência (ex: um votou 2 e outro 13), os dois explicam seus pontos de vista (o de '2' pode saber um atalho, o de '13' pode ter visto um risco de segurança).</li>
                        <li>Vota-se novamente até chegar a um consenso ou maioria próxima.</li>
                    </ol>
                `,
                result: "Histórias estimadas com visão compartilhada de complexidade técnica e riscos mitigados pelo debate."
            }
        ],
        "Kanban & Fluxo": [
            {
                title: "Simulação TWiG (The WiP Game)",
                icon: "🚦",
                detail: "Dinâmica prática para demonstrar o impacto dos limites de WIP (Work in Progress) e gargalos na entrega de valor. Ensina na prática que 'começar a terminar é melhor que terminar de começar'.",
                examples: "Treinamento para um time que trabalha em 15 tarefas ao mesmo tempo e sofre com lead times altíssimos e baixa qualidade.",
                execution: `
                    <ol>
                        <li><strong>Rodada 1 (Sem limite de WIP):</strong> Dê ao time uma tarefa manual simples (ex: escrever nomes em cartões, passar por 3 pessoas para carimbar, assinar e dobrar). Empurre trabalho o mais rápido possível. Meça o tempo da primeira entrega e o estresse.</li>
                        <li><strong>Rodada 2 (Com WIP Limitado a 1 ou 2 por etapa):</strong> Repita o processo. A pessoa 1 só pode começar um novo cartão se a pessoa 2 tiver espaço livre. Se travar, a pessoa 1 ajuda a pessoa 2.</li>
                        <li>Debriefing: Compare os lead times e a sensação da equipe em ambas as rodadas.</li>
                    </ol>
                `,
                result: "Mudança de mindset instantânea. A equipe compreende matematicamente (Lei de Little) e de forma empírica por que limitar o trabalho em progresso aumenta a vazão e reduz o estresse."
            },
            {
                title: "STATIK (Design de Sistema Kanban)",
                icon: "🔄",
                detail: "O STATIK (Systems Thinking Approach to Introducing Kanban) é um workshop iterativo para modelar ou melhorar o sistema Kanban de uma equipe de serviço.",
                examples: "Usado para mapear o fluxo de uma equipe de Sustentação (N3) que recebe chamados não estruturados.",
                execution: `
                    <ol>
                        <li><strong>Propósito:</strong> O que o cliente espera do nosso serviço?</li>
                        <li><strong>Fontes de Insatisfação:</strong> Mapeie dores internas e externas atuais.</li>
                        <li><strong>Análise de Demanda:</strong> Quais tipos de demanda chegam? (Bugs, Melhorias, Dúvidas). Qual a taxa de chegada?</li>
                        <li><strong>Capacidade:</strong> Quanto o time consegue entregar hoje?</li>
                        <li><strong>Mapeamento do Fluxo:</strong> Desenhe as etapas que o item passa desde a solicitação até a entrega.</li>
                        <li><strong>Classes de Serviço:</strong> Defina como tratar itens urgentes (Expedite) vs padrão.</li>
                        <li><strong>Desenho do Quadro:</strong> Crie as colunas e estabeleça os limites de WIP iniciais.</li>
                    </ol>
                `,
                result: "Um quadro Kanban e um sistema de fluxo desenhado sob medida para o contexto atual do time, com políticas explícitas definidas."
            }
        ],
        "Design Thinking & Ideação": [
            {
                title: "Matriz CSD (Certezas, Suposições, Dúvidas)",
                icon: "🤔",
                detail: "Dinâmica rápida para organizar o conhecimento coletivo antes de iniciar uma Discovery. Ajuda a definir o que precisa ser pesquisado.",
                examples: "Início do discovery de um novo portal do cliente. O time de vendas acha que sabe o que o cliente quer, mas precisa alinhar com Produto e UX.",
                execution: `
                    <ol>
                        <li>Crie 3 colunas: Certezas (Fatos comprovados por dados), Suposições (Achismos que acreditamos ser verdade) e Dúvidas (O que não sabemos).</li>
                        <li>Os participantes escrevem post-its e colam nas colunas correspondentes.</li>
                        <li>Revisão em grupo: Se alguém questiona uma 'Certeza' e não há dados para comprovar, o post-it é movido para 'Suposições'.</li>
                        <li>As 'Suposições' e 'Dúvidas' se transformam em roteiros de entrevista e pesquisas com o usuário.</li>
                    </ol>
                `,
                result: "Um backlog de discovery claro. O time sai alinhado sobre as lacunas de conhecimento e focado em validar hipóteses críticas antes de desenvolver."
            },
            {
                title: "Crazy Eights (8 Ideias Loucas)",
                icon: "🎨",
                detail: "Exercício de ideação ultrarrápido (core do Design Sprint) que força os participantes a pensar além das suas primeiras ideias para resolver um problema.",
                examples: "Criar soluções de interface para o checkout de um app mobile que está com alta taxa de abandono.",
                execution: `
                    <ol>
                        <li>Entregue uma folha de papel A4 para cada pessoa e peça para dobrarem ao meio 3 vezes (formando 8 retângulos).</li>
                        <li>Coloque um timer de 8 minutos (1 minuto por retângulo).</li>
                        <li>Cada participante deve desenhar/escrever uma solução diferente para o problema em cada retângulo. O foco é quantidade, não qualidade do desenho.</li>
                        <li>Ao fim do tempo, cada um tem 3 minutos para apresentar suas ideias na parede.</li>
                        <li>O time vota nas melhores ideias (Dot Voting) para prototipação.</li>
                    </ol>
                `,
                result: "Dezenas de ideias geradas em menos de 15 minutos, contornando a inibição criativa e encontrando soluções fora da caixa para problemas complexos."
            }
        ]
    };

    container.innerHTML = '';
    
    // Header
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.innerHTML = `
        <div style="text-transform: uppercase; font-size: 0.85rem; color: #f97316; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">📖 Playbook de Agilidade</div>
        <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px; font-size: 1.8rem;">Material do Facilitador: Dinâmicas</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            Guias de bolso para Agile Coaches e Scrum Masters. Baseado em metodologias ágeis e best-sellers como <strong>Lean Inception</strong> e <strong>Fun Retrospectives</strong> de Paulo Caroli.
        </p>
    `;
    container.appendChild(introHeader);

    // Layout
    const layout = document.createElement('div');
    layout.className = 'kb-layout';

    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';
    contentArea.style.padding = '30px';
    contentArea.style.background = '#f8fafc';

    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    container.appendChild(layout);

    const categories = Object.keys(dinamicasData);
    let firstBtn = null;

    categories.forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #f97316';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const linkList = document.createElement('div');
        linkList.className = 'kb-link-list';
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        const dinList = dinamicasData[category];
        dinList.forEach((din) => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">${din.icon}</span>
                    <span style="font-weight:600; color:#323130; font-size:0.95rem;">${din.title}</span>
                </div>
            `;
            linkList.appendChild(btn);

            if(!firstBtn) firstBtn = btn;

            btn.onclick = () => {
                document.querySelectorAll('#facilitador-dinamicas-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const contentHtml = `
<div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); max-width: 900px; margin: 0 auto;">
    
    <div style="background: linear-gradient(to right, #0f172a, #1e293b); padding: 30px; color: white;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-size: 3rem; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 12px;">${din.icon}</span>
            <div>
                <span style="color: #f97316; font-weight: bold; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px;">${category}</span>
                <h2 style="margin: 5px 0 0 0; font-size: 2rem;">${din.title}</h2>
            </div>
        </div>
    </div>

    <div style="padding: 30px;">
        
        <!-- Detalhamento -->
        <div style="margin-bottom: 25px;">
            <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
                <span>📝</span> Detalhamento
            </h4>
            <p style="color: #475569; font-size: 1.05rem; line-height: 1.6; margin: 0;">
                ${din.detail}
            </p>
        </div>

        <!-- Exemplos -->
        <div style="margin-bottom: 25px; background: #fff7ed; padding: 15px 20px; border-left: 4px solid #f97316; border-radius: 0 8px 8px 0;">
            <h4 style="color: #9a3412; font-size: 1.1rem; margin-top: 0; margin-bottom: 8px; display:flex; align-items:center; gap:8px;">
                <span>💡</span> Exemplo de Cenário
            </h4>
            <p style="color: #7c2d12; font-size: 1.05rem; line-height: 1.6; margin: 0; font-style: italic;">
                "${din.examples}"
            </p>
        </div>

        <!-- A Prática Executada -->
        <div style="margin-bottom: 25px;">
            <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 15px; display:flex; align-items:center; gap:8px;">
                <span>⚙️</span> Passo a Passo da Execução
            </h4>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px;">
                <div style="color: #334155; font-size: 1.05rem; line-height: 1.7; margin-left: 10px;" class="din-execution-list">
                    ${din.execution}
                </div>
            </div>
        </div>

        <!-- Resultado Final Esperado -->
        <div style="margin-bottom: 10px;">
            <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
                <span>🏆</span> Resultado Final Esperado
            </h4>
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 15px 20px; border-radius: 8px;">
                <p style="color: #166534; font-size: 1.1rem; line-height: 1.6; margin: 0; font-weight: 500;">
                    ${din.result}
                </p>
            </div>
        </div>

    </div>
</div>
                `;

                contentArea.innerHTML = contentHtml;

                // Simple CSS injection for ordered lists inside the execution block
                const styleId = 'dinamicas-style';
                if (!document.getElementById(styleId)) {
                    const style = document.createElement('style');
                    style.id = styleId;
                    style.innerHTML = `
                        .din-execution-list ol { padding-left: 20px; margin: 0; }
                        .din-execution-list li { margin-bottom: 12px; }
                        .din-execution-list li strong { color: #0f172a; }
                    `;
                    document.head.appendChild(style);
                }
            };
        });
    });

    if (firstBtn) {
        firstBtn.click();
    }
}
