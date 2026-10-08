document.addEventListener('DOMContentLoaded', () => {
    initTecnicasFacilitacaoView();
});

function initTecnicasFacilitacaoView() {
    const container = document.getElementById('tecnicas-facilitacao-view');
    if(!container) return;

    const tecnicasData = {
        "Comunicação & Escuta": [
            {
                title: "Escuta Ativa e Empática",
                icon: "👂",
                detail: "A habilidade de focar completamente no locutor, compreender a mensagem, compreender as emoções e reter a informação para uso posterior sem interrupções.",
                examples: "Um membro do time desabafa sobre a pressão das entregas. O Agile Coach para de digitar, faz contato visual, concorda com a cabeça e repete a essência do que foi dito: 'Então você sente que o escopo está crescendo sem aviso, correto?'.",
                execution: `
                    <ol>
                        <li><strong>Pare outras atividades:</strong> Feche notebooks e foque no interlocutor.</li>
                        <li><strong>Postura aberta:</strong> Mantenha contato visual e evite braços cruzados.</li>
                        <li><strong>Parafraseie:</strong> Repita com suas palavras o que a pessoa disse para validar o entendimento.</li>
                        <li><strong>Valide a emoção:</strong> Reconheça o sentimento ("Entendo sua frustração").</li>
                    </ol>
                `,
                result: "Exemplo Prático: O membro da equipe se sente ouvido, diminui sua defensiva e se torna mais aberto a discutir soluções de fluxo."
            },
            {
                title: "Perguntas Poderosas (Socráticas)",
                icon: "❓",
                detail: "Técnica de questionamento que força o interlocutor a refletir, encontrar suas próprias respostas e descobrir falhas em seu raciocínio, em vez do facilitador entregar a resposta pronta.",
                examples: "O time pergunta 'O que fazemos com esse bug?'. O Scrum Master devolve: 'O que a nossa política explícita de bugs críticos diz sobre isso?'.",
                execution: `
                    <ol>
                        <li>Use perguntas abertas (Como, O que, Por que).</li>
                        <li>Evite perguntas de 'Sim ou Não'.</li>
                        <li>Deixe o silêncio atuar após a pergunta; dê tempo para a pessoa pensar.</li>
                        <li>Evite embutir a sua opinião na pergunta (Ex errado: 'Você não acha que deveríamos testar mais?').</li>
                    </ol>
                `,
                result: "Exemplo Prático: O time de desenvolvimento para de depender do Scrum Master para decisões diárias e desenvolve auto-organização."
            }
        ],
        "Gestão de Tempo & Foco": [
            {
                title: "Parking Lot (Estacionamento de Ideias)",
                icon: "🅿️",
                detail: "Técnica visual para capturar ideias ou discussões válidas, mas que estão fora do escopo ou foco do objetivo atual da reunião.",
                examples: "Durante a Daily, dois desenvolvedores começam a discutir a arquitetura de banco de dados para uma feature futura.",
                execution: `
                    <ol>
                        <li>Crie um espaço visual na parede ou no Miro chamado 'Parking Lot'.</li>
                        <li>Ao notar um desvio de foco, interrompa educadamente: 'Excelente ponto, mas foge do escopo atual'.</li>
                        <li>Anote o tópico em um post-it e coloque no Parking Lot.</li>
                        <li>Reserve os 5 minutos finais da reunião para revisar o Parking Lot e definir os próximos passos de cada item.</li>
                    </ol>
                `,
                result: "Exemplo Prático: A reunião de Planning acaba no tempo exato de 2 horas. As discussões técnicas de arquitetura foram marcadas para uma reunião separada amanhã à tarde."
            },
            {
                title: "Timeboxing Rigoroso",
                icon: "⏱️",
                detail: "Alocação de um período de tempo fixo e inegociável para uma atividade. Quando o tempo acaba, a atividade para, forçando o foco no que é mais essencial.",
                examples: "Brainstorming infinito em uma Retrospectiva onde as pessoas divagam e nunca chegam a um plano de ação.",
                execution: `
                    <ol>
                        <li>Defina o limite de tempo publicamente (ex: 'Temos 8 minutos para ideação').</li>
                        <li>Use um timer visual e grande (ex: Time Timer) para que todos vejam a regressão.</li>
                        <li>Aise quando faltar metade do tempo e quando faltar 1 minuto.</li>
                        <li>Quando o timer tocar, interrompa imediatamente de forma gentil mas firme.</li>
                    </ol>
                `,
                result: "Exemplo Prático: O time gera 15 ideias objetivas em 8 minutos, parando a atividade no alarme, permitindo tempo de sobra para votação e plano de ação."
            }
        ],
        "Consenso & Decisão": [
            {
                title: "Fist of Five (Punho de Cinco)",
                icon: "🖐️",
                detail: "Técnica rápida para avaliar o grau de consenso de uma equipe sobre uma decisão, variando de 0 (bloqueio) a 5 dedos (total suporte).",
                examples: "A equipe precisa decidir se vai adotar um novo framework de testes ou manter o antigo nesta Sprint.",
                execution: `
                    <ol>
                        <li>Apresente a proposta claramente.</li>
                        <li>Peça que todos levantem a mão ao mesmo tempo mostrando os dedos (1 a 5).</li>
                        <li>5: 'Apoio totalmente e lidero'. 4: 'Gosto e apoio'. 3: 'Concordo, posso viver com isso'. 2: 'Tenho ressalvas, mas não bloqueio'. 1: 'Discordo fortemente'. 0 (Punho fechado): 'Veto/Bloqueio'.</li>
                        <li>Se houver algum 0 ou 1, peça para a pessoa explicar sua preocupação para ajustar a proposta.</li>
                    </ol>
                `,
                result: "Exemplo Prático: 4 pessoas mostram 4 dedos e 1 pessoa mostra o punho (0). A equipe para, escuta o risco técnico apontado pelo punho fechado, ajusta a proposta e vota novamente com sucesso (todos 3+)."
            },
            {
                title: "Dot Voting (Votação por Pontos)",
                icon: "🔴",
                detail: "Método democrático para priorizar uma lista extensa de itens, distribuindo uma quantidade limitada de 'votos' (pontos adesivos) para cada participante.",
                examples: "Selecionar qual experimento de melhoria contínua o time vai puxar dentre 20 problemas levantados na Retrospectiva.",
                execution: `
                    <ol>
                        <li>Agrupe ideias semelhantes para evitar divisão de votos.</li>
                        <li>Distribua votos (ex: 3 pontos por pessoa).</li>
                        <li>Defina a regra: as pessoas podem colocar todos os votos num mesmo cartão ou distribuir.</li>
                        <li>Votação silenciosa: todos colam seus pontos simultaneamente.</li>
                        <li>Ordene os cartões pela quantidade total de pontos recebidos.</li>
                    </ol>
                `,
                result: "Exemplo Prático: O item 'Ajustar CI/CD' recebe 9 votos, enquanto 'Melhorar documentação' recebe 2. O time entra em acordo imediato para focar no CI/CD."
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
        <div style="text-transform: uppercase; font-size: 0.85rem; color: #8b5cf6; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 0.5rem;">🧠 Comportamento e Liderança</div>
        <h2 style="margin-top:0; color:#0f172a; margin-bottom:10px; font-size: 1.8rem;">Técnicas de Facilitação</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            Diferente das "Dinâmicas" (que são jogos e atividades), as <strong>Técnicas de Facilitação</strong> são as habilidades comportamentais, posturas e micro-ferramentas que o Agile Coach usa para guiar reuniões, mediar conflitos e extrair o melhor das pessoas.
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

    const categories = Object.keys(tecnicasData);
    let firstBtn = null;

    categories.forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #8b5cf6';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const linkList = document.createElement('div');
        linkList.className = 'kb-link-list';
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        const dinList = tecnicasData[category];
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
                document.querySelectorAll('#tecnicas-facilitacao-view .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const contentHtml = `
<div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); max-width: 900px; margin: 0 auto;">
    
    <div style="background: linear-gradient(to right, #2e1065, #4c1d95); padding: 30px; color: white;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-size: 3rem; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 12px;">${din.icon}</span>
            <div>
                <span style="color: #c4b5fd; font-weight: bold; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px;">${category}</span>
                <h2 style="margin: 5px 0 0 0; font-size: 2rem;">${din.title}</h2>
            </div>
        </div>
    </div>

    <div style="padding: 30px;">
        
        <!-- Detalhamento -->
        <div style="margin-bottom: 25px;">
            <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
                <span>📝</span> O que é a Técnica?
            </h4>
            <p style="color: #475569; font-size: 1.05rem; line-height: 1.6; margin: 0;">
                ${din.detail}
            </p>
        </div>

        <!-- Exemplos -->
        <div style="margin-bottom: 25px; background: #faf5ff; padding: 15px 20px; border-left: 4px solid #8b5cf6; border-radius: 0 8px 8px 0;">
            <h4 style="color: #5b21b6; font-size: 1.1rem; margin-top: 0; margin-bottom: 8px; display:flex; align-items:center; gap:8px;">
                <span>💡</span> Exemplo de Cenário
            </h4>
            <p style="color: #4c1d95; font-size: 1.05rem; line-height: 1.6; margin: 0; font-style: italic;">
                "${din.examples}"
            </p>
        </div>

        <!-- A Prática Executada -->
        <div style="margin-bottom: 25px;">
            <h4 style="color: #334155; font-size: 1.2rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 15px; display:flex; align-items:center; gap:8px;">
                <span>⚙️</span> Passo a Passo do Facilitador
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
                <span>🎯</span> Resultado na Prática
            </h4>
            <div style="background: #fdf4ff; border: 1px solid #f5d0fe; padding: 15px 20px; border-radius: 8px;">
                <p style="color: #86198f; font-size: 1.1rem; line-height: 1.6; margin: 0; font-weight: 500;">
                    ${din.result}
                </p>
            </div>
        </div>

    </div>
</div>
                `;

                contentArea.innerHTML = contentHtml;
            };
        });
    });

    if (firstBtn) {
        firstBtn.click();
    }
}
