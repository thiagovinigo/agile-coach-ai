const tecnicasData = {
    "Liberating Structures": [
        {
            "title": "1-2-4-All",
            "icon": "🗣️",
            "detail": "Engaja todos simultaneamente na geração de ideias ou respostas a perguntas. Ideal para evitar que poucas vozes dominem a conversa.",
            "examples": "Brainstorming sobre como melhorar a comunicação entre equipes remotas.",
            "execution": "<ol><li>Reflexão individual silenciosa sobre o desafio (1 min).</li><li>Compartilhamento e aprofundamento de ideias em pares (2 min).</li><li>Sintetizar as ideias em quartetos, destacando as principais (4 min).</li><li>Compartilhamento com todo o grupo de uma ideia de destaque por quarteto (5 min).</li></ol>",
            "result": "Exemplo Prático: O time gerou 3 ideias claras: 1. Adotar Slack calls diárias de 5 min (João). 2. Desligar câmeras às sextas para diminuir fadiga. 3. Criar canal de 'Dúvidas Urgentes' com SLA de 30 min."
        },
        {
            "title": "Troika Consulting",
            "icon": "🤝",
            "detail": "Obtenha ajuda prática e imediata de colegas para resolver um desafio. Excelente para sessões de mentoria rápida entre pares.",
            "examples": "Um Scrum Master buscando ideias para lidar com um stakeholder difícil.",
            "execution": "<ol><li>Forme grupos de três. Um é o 'cliente', dois são os 'consultores'.</li><li>O cliente apresenta seu desafio (1 min).</li><li>Consultores fazem perguntas de esclarecimento (1-2 min).</li><li>O cliente vira de costas. Consultores discutem ideias e soluções (4-5 min).</li><li>Cliente vira de frente e compartilha o que achou mais útil (1 min). Troque os papéis.</li></ol>",
            "result": "Exemplo Prático: Maria (Scrum Master) recebeu 2 conselhos de Pedro e Lucas: 1. Convidar o stakeholder 'difícil' para uma Daily e não só para as Reviews. 2. Enviar relatórios visuais no WhatsApp dele antes da reunião oficial."
        },
        {
            "title": "Lean Coffee",
            "icon": "☕",
            "detail": "Um formato de reunião sem pauta pré-definida, mas altamente estruturado. Os participantes constroem a agenda democraticamente no início da sessão.",
            "examples": "Comunidade de Prática compartilhando aprendizados semanais.",
            "execution": "<ol><li>Participantes escrevem tópicos em post-its.</li><li>Apresentação rápida de cada tópico (pitch).</li><li>Votação com pontos (Dot Voting) para priorizar os tópicos.</li><li>Discussão dos tópicos em intervalos curtos (ex: 5 min), votando se querem continuar (Roman Voting) ao fim de cada intervalo.</li></ol>",
            "result": "Exemplo Prático: A comunidade de 15 pessoas priorizou 3 pautas. Discutiram 'Testes Unitários em React' por 15 min, 'Gestão de Dependências' por 10 min, e concluíram com 2 tarefas: revisar PRs de teste até quinta, e agendar workshop na sexta."
        },
        {
            "title": "Fishbowl",
            "icon": "🐠",
            "detail": "Permite que pequenos grupos conversem enquanto o grande grupo observa. Ideal para painéis de discussão dinâmicos e participativos.",
            "examples": "Discussão entre líderes sobre a nova estratégia da empresa com toda a equipe observando.",
            "execution": "<ol><li>Coloque 4-5 cadeiras no centro (o aquário) e as demais em círculos concêntricos ao redor.</li><li>Apenas quem está no centro pode falar.</li><li>Deixe uma cadeira vazia no centro. Se alguém de fora quiser falar, deve ocupar a cadeira vazia.</li><li>Quando alguém senta na cadeira vazia, uma pessoa do aquário deve sair voluntariamente.</li></ol>",
            "result": "Exemplo Prático: O Diretor Carlos e 3 gerentes começaram discutindo os cortes de orçamento. Ana, do nível operacional, sentou na cadeira vazia e sugeriu reduzir licenças de softwares não utilizados em vez de demissões, gerando uma nova frente de ação (Projeto Save-SaaS)."
        },
        {
            "title": "Impromptu Networking",
            "icon": "🕸️",
            "detail": "Compartilhamento rápido de ideias e formação de conexões no início de uma sessão. Quebra o gelo de forma produtiva.",
            "examples": "Início de um workshop de planejamento trimestral para alinhar expectativas.",
            "execution": "<ol><li>Apresente um desafio ou pergunta instigante.</li><li>Participantes formam pares aleatórios e compartilham respostas (2-3 min por par).</li><li>Após o tempo, mudam de par. Repita 3 vezes.</li></ol>",
            "result": "Exemplo Prático: Após 3 rodadas de 3 minutos, 20 participantes descobriram que o medo unânime para o trimestre era 'Falha na migração para a nuvem'. Isso fez a liderança colocar o tema como tópico número 1 do planejamento."
        },
        {
            "title": "Appreciative Interviews",
            "icon": "🏆",
            "detail": "Descobrir e construir sobre as causas do sucesso passado. Foca no positivo para desenhar o futuro.",
            "examples": "Sessão de kick-off de um projeto crítico para identificar os pontos fortes da equipe.",
            "execution": "<ol><li>Em pares, entreviste o colega sobre uma história de sucesso na empresa (5 min cada).</li><li>Junte pares em quartetos e compartilhe as histórias ouvidas.</li><li>Identifiquem padrões e condições que permitiram o sucesso.</li><li>Compartilhem os insights com o grande grupo.</li></ol>",
            "result": "Exemplo Prático: A equipe de design concluiu que seus 3 maiores sucessos do passado ocorreram quando envolveram desenvolvedores no dia 1 do protótipo. Decisão: A partir de hoje, 1 Dev participará de todas as sessões iniciais de Wireframing."
        },
        {
            "title": "TRIZ",
            "icon": "🧨",
            "detail": "Liberar espaço para inovação eliminando práticas destrutivas. Ajuda a parar atividades que não agregam valor.",
            "examples": "Equipe sobrecarregada buscando formas de reduzir gargalos no processo.",
            "execution": "<ol><li>Liste tudo que você poderia fazer para garantir o pior resultado possível.</li><li>Revise a lista e marque as coisas que você já está fazendo de alguma forma hoje.</li><li>Para cada item marcado, defina os primeiros passos para parar de fazê-lo.</li></ol>",
            "result": "Exemplo Prático: O time listou 'ignorar bugs até a véspera de produção'. Eles perceberam que estavam fazendo isso parcialmente ao pular a etapa de QA na pressa. Ação imediata: Tornar aprovação do QA bloqueio automático no Github a partir das 16h de amanhã."
        },
        {
            "title": "15% Solutions",
            "icon": "🧩",
            "detail": "Descobrir e focar naquilo que cada pessoa tem a liberdade e os recursos para mudar agora.",
            "examples": "Identificar pequenas melhorias após uma retrospectiva sem depender da diretoria.",
            "execution": "<ol><li>Reflexão individual: Qual é a sua solução de 15%? O que você pode fazer agora sem pedir permissão ou recursos extras? (5 min).</li><li>Compartilhar em pequenos grupos para obter feedback e aprimorar a ideia (10 min).</li></ol>",
            "result": "Exemplo Prático: Roberto (Analista) decidiu que, sem pedir verba ou permissão, ele mesmo gastará 15 minutos por dia limpando a documentação obsoleta do Confluence. Carla decidiu organizar a nomenclatura dos arquivos de design na sexta."
        },
        {
            "title": "Open Space Technology",
            "icon": "🎪",
            "detail": "Criar agendas auto-organizadas para grandes grupos em torno de um tema central complexo.",
            "examples": "Evento interno de inovação (Hackathon ou Chapter Day).",
            "execution": "<ol><li>Apresente o tema central.</li><li>Participantes propõem sessões que querem facilitar em uma grade de horários e locais vazia no mural.</li><li>Mercado: todos escolhem as sessões que querem participar.</li><li>Execução das sessões simultâneas seguindo a Lei dos Dois Pés.</li></ol>",
            "result": "Exemplo Prático: Em um evento de 50 pessoas, foram criadas 8 sessões simultâneas. A sessão improvisada de 'Como usar IA para testes' gerou um guia de 5 páginas que o CTO aprovou na semana seguinte para toda a empresa."
        },
        {
            "title": "World Cafe",
            "icon": "🌎",
            "detail": "Conectar diversas perspectivas através de rodadas de conversas em pequenos grupos. Cria uma rede viva de conversas colaborativas.",
            "examples": "Explorar o impacto de uma nova tecnologia nas diferentes áreas de negócio.",
            "execution": "<ol><li>Crie mesas de 4-5 pessoas com papel kraft e canetas.</li><li>Proponha uma pergunta poderosa para discussão (20 min).</li><li>Ao sinal, um 'anfitrião' fica na mesa, os demais viajam para mesas diferentes.</li><li>O anfitrião resume a conversa anterior para os novos membros e a discussão continua com nova pergunta ou aprofundamento.</li></ol>",
            "result": "Exemplo Prático: Após 3 rodadas trocando de mesa, o papel kraft central estava cheio de desenhos mostrando como a 'IA de atendimento' afeta Marketing, Vendas e Suporte de forma cruzada, resultando na criação de um squad temporário com 1 pessoa de cada área."
        },
        {
            "title": "Min Specs",
            "icon": "📏",
            "detail": "Especificar apenas o que deve absolutamente acontecer e o que absolutamente não deve acontecer, liberando criatividade no meio.",
            "examples": "Definição de regras básicas para lançamento de novos produtos.",
            "execution": "<ol><li>Liste todas as regras (Do's e Don'ts) possíveis para o objetivo.</li><li>Teste cada uma: 'Se quebrarmos esta regra e seguirmos as outras, ainda alcançamos o propósito?'.</li><li>Se a resposta for sim, elimine a regra.</li><li>Mantenha apenas as Especificações Mínimas.</li></ol>",
            "result": "Exemplo Prático: O time de Marketing começou com 20 regras para os novos posts no Instagram. Após o Min Specs, restaram apenas 2 inegociáveis: 1. A paleta de cores deve conter pelo menos 30% do Azul da marca. 2. Nenhum post pode ofender minorias. O resto (tamanho do texto, formato, tom) ficou livre, triplicando a velocidade de criação."
        },
        {
            "title": "Wise Crowds",
            "icon": "🦉",
            "detail": "Aproveitar a sabedoria de todo o grupo para avaliar rapidamente ideias, projetos ou desafios de poucos.",
            "examples": "Revisão de arquitetura de software por especialistas da empresa.",
            "execution": "<ol><li>O 'cliente' apresenta o desafio ao grupo (2 min).</li><li>Consultores fazem perguntas de esclarecimento (3 min).</li><li>Cliente vira de costas e apenas ouve. Consultores discutem soluções, conselhos e ideias (10 min).</li><li>Cliente vira de volta e compartilha o que foi mais útil.</li></ol>",
            "result": "Exemplo Prático: Felipe, arquiteto de software, ouviu de costas por 10 minutos os 8 líderes de TI. Ele descobriu que a AWS tinha um serviço específico (Lambda) que resolveria seu problema de escala por uma fração do preço, descartando a ideia anterior de comprar servidores físicos."
        },
        {
            "title": "Shift & Share",
            "icon": "🔄",
            "detail": "Compartilhar inovação e disseminar ideias rapidamente entre muitos participantes.",
            "examples": "Feira de ciências corporativa para mostrar os produtos de diferentes squads.",
            "execution": "<ol><li>Configure estações para diferentes apresentadores.</li><li>Divida o grupo para que cada estação tenha uma plateia.</li><li>Apresentação e Q&A na estação (10 min).</li><li>Ao sinal, os grupos giram para a próxima estação.</li></ol>",
            "result": "Exemplo Prático: O time de 60 pessoas visitou 6 estações diferentes de 10 min. A estação da 'Nova Intranet' recebeu 45 feedbacks construtivos rápidos. A estação de 'Benefícios' coletou 12 propostas de novos planos de saúde em menos de uma hora."
        },
        {
            "title": "Drawing Together",
            "icon": "🎨",
            "detail": "Revelar insights não verbais desenhando com símbolos padronizados.",
            "examples": "Explorar os sentimentos da equipe em relação a uma grande fusão corporativa.",
            "execution": "<ol><li>Ensine os 5 símbolos básicos: círculo (totalidade), retângulo (suporte), triângulo (meta), espiral (mudança), estrela (relação).</li><li>Convide os participantes a desenharem seu desafio usando apenas esses símbolos.</li><li>Pares analisam os desenhos uns dos outros sem o autor falar, compartilhando impressões.</li></ol>",
            "result": "Exemplo Prático: Um gerente desenhou uma estrela isolada e cercada por espirais caóticas. Seu colega interpretou isso como 'sentimento de solidão em meio a mudanças rápidas'. O gerente chorou e concordou, algo que nunca diria verbalmente, abrindo espaço para receber suporte emocional da liderança."
        },
        {
            "title": "25/10 Crowd Sourcing",
            "icon": "📊",
            "detail": "Gerar e priorizar rapidamente ideias ousadas de um grande grupo em pouco tempo.",
            "examples": "Priorização rápida do backlog de problemas em um workshop de 100 pessoas.",
            "execution": "<ol><li>Todos escrevem uma ideia e uma ação ousada em um cartão (3 min).</li><li>Passam os cartões aleatoriamente pela sala enquanto a música toca.</li><li>Quando a música para, leem o cartão na mão e dão nota de 1 a 5 no verso.</li><li>Repete-se a passagem e pontuação 5 vezes.</li><li>Soma-se os pontos (máx 25). Identificam-se as 10 melhores ideias.</li></ol>",
            "result": "Exemplo Prático: 80 funcionários geraram 80 ideias para cortar custos. Em 25 minutos, as cartas circularam. A ideia vencedora (24 pontos) foi 'Remover as catracas eletrônicas inúteis da garagem', poupando R$ 15.000 de manutenção anual."
        },
        {
            "title": "Conversation Cafe",
            "icon": "🛋️",
            "detail": "Engajar a todos em diálogo sobre um tema complexo e desafiador em um ambiente seguro.",
            "examples": "Debater questões de diversidade e inclusão na liderança.",
            "execution": "<ol><li>Grupos de 4 a 5 com um objeto de fala (talking token).</li><li>Rodada 1: Com o objeto, cada um compartilha o que pensa/sente sem interrupção.</li><li>Rodada 2: Cada um aprofunda o que sentiu ao ouvir os outros.</li><li>Rodada 3: Diálogo aberto sem o objeto.</li><li>Rodada 4: Takeaways finais com o objeto.</li></ol>",
            "result": "Exemplo Prático: Discutindo o burnout do time, a 'bola falante' impediu os gerentes de interromperem. Na rodada final, ficou claro para todos: o problema não era excesso de tarefas, mas a ambiguidade constante das metas passadas pela diretoria."
        },
        {
            "title": "Design Storyboards",
            "icon": "🎞️",
            "detail": "Planejar processos complexos ou sessões como uma série de cenas visuais.",
            "examples": "Desenhando a jornada do cliente para um novo produto.",
            "execution": "<ol><li>Divida a experiência em etapas cronológicas.</li><li>Use quadros para desenhar as ações e emoções dos usuários em cada passo.</li><li>Revise coletivamente para identificar falhas ou oportunidades na narrativa.</li></ol>",
            "result": "Exemplo Prático: Ao desenhar a jornada de onboarding em 6 quadros, a equipe notou que o quadro 4 ('esperar email de confirmação por 24h') desenhava um usuário entediado. Imediatamente decidiram automatizar essa etapa para 5 segundos, mudando a carinha do boneco para 'feliz'."
        },
        {
            "title": "Ecocycle Planning",
            "icon": "♻️",
            "detail": "Analisar portfólios de atividades para identificar gargalos de crescimento e liberação criativa.",
            "examples": "Revisão estratégica do portfólio de produtos da empresa.",
            "execution": "<ol><li>Apresente o mapa do Ecociclo (Gestação, Nascimento, Maturidade, Destruição Criativa e Armadilhas).</li><li>Os participantes posicionam seus projetos ou atividades atuais no mapa.</li><li>Analise áreas sobrecarregadas, projetos presos em armadilhas de pobreza ou rigidez.</li><li>Defina ações para mover as atividades pelo ciclo.</li></ol>",
            "result": "Exemplo Prático: O time notou que 8 dos seus 10 produtos estavam na fase de 'Maturidade/Rigidez' (consumindo manutenção, mas sem crescer), enquanto a fase de 'Gestação' estava vazia. Decidiram matar 2 produtos maduros para liberar 4 engenheiros para iniciarem inovações na fase de gestação."
        },
        {
            "title": "Panarchy",
            "icon": "🌐",
            "detail": "Compreender como as dinâmicas interagem em múltiplos níveis de escala de um sistema.",
            "examples": "Diagnosticar por que uma transformação ágil está travando em diferentes níveis organizacionais.",
            "execution": "<ol><li>Identifique os diferentes níveis do sistema (micro, meso, macro).</li><li>Faça um Ecociclo para cada nível.</li><li>Identifique como as mudanças ou resistências em um nível (ex: equipe) afetam ou são afetadas por outros (ex: diretoria).</li><li>Desenvolva estratégias multicanais.</li></ol>",
            "result": "Exemplo Prático: Mapeando os 3 níveis, descobriram que a Squad (Nível Micro) estava pronta para fazer entregas diárias, mas o setor de Compliance (Nível Macro) exigia 15 dias de auditoria. Ação: Mudar o foco para educar a diretoria em vez de forçar a equipe a trabalhar mais rápido."
        },
        {
            "title": "Purpose-To-Practice (P2P)",
            "icon": "🎯",
            "detail": "Desenhar iniciativas robustas focando em 5 elementos centrais para garantir coerência.",
            "examples": "Criação de uma nova guilda de tecnologia dentro da empresa.",
            "execution": "<ol><li>Definir o Propósito (Por que esse trabalho é importante?).</li><li>Princípios (Quais regras devemos seguir?).</li><li>Participantes (Quem precisa estar envolvido?).</li><li>Estrutura (Como nos organizamos?).</li><li>Práticas (O que vamos fazer de fato?).</li></ol>",
            "result": "Exemplo Prático: Na criação do 'Comitê de IA', saíram de uma ideia vaga para um design robusto. Propósito: Acelerar entregas. Princípios: IA é assistente, não substituto. Participantes: 1 dev senior e 1 junior por squad. Estrutura: Reunião quinzenal 1h. Prática: Compartilhar 1 prompt de sucesso por encontro."
        },
        {
            "title": "What, So What, Now What?",
            "icon": "🤔",
            "detail": "Reflexão estruturada em três passos para fazer sentido compartilhado e agir em seguida.",
            "examples": "Debriefing após o fracasso de uma release de software.",
            "execution": "<ol><li>What? (O que aconteceu? Fatos e observações apenas).</li><li>So What? (E daí? Por que é importante? Padrões e conclusões).</li><li>Now What? (O que faremos agora? Ações claras).</li></ol>",
            "result": "Exemplo Prático: Após queda do servidor. What? A CPU bateu 100% às 14h e travou. So What? Perdemos cerca de 200 carrinhos de compra na Black Friday, nosso momento mais crítico. Now What? Configurar Auto-Scaling imediato na AWS para o final de semana e implementar cache de consultas de estoque."
        },
        {
            "title": "Future~Present",
            "icon": "🚀",
            "detail": "Viajar para um futuro de sucesso e fazer o caminho inverso (backcasting) para planejar.",
            "examples": "Planejamento estratégico de 3 anos do departamento.",
            "execution": "<ol><li>Imagine que estamos em 202X e fomos extremamente bem-sucedidos.</li><li>Descreva como é essa realidade futura vividamente.</li><li>O que fizemos no ano anterior para chegar lá? E dois anos antes?</li><li>Traga até o presente e defina os primeiros passos.</li></ol>",
            "result": "Exemplo Prático: Em 2028, a empresa foi eleita a melhor do Brasil. O time imaginou que, para isso acontecer, em 2027 a taxa de turnover teria caído a 5%. Em 2026, lançaram a semana de 4 dias. No presente, a primeira ação acordada foi testar a 'sexta-feira sem reuniões' imediatamente."
        },
        {
            "title": "Nine Whys",
            "icon": "❓",
            "detail": "Tornar o propósito do trabalho absolutamente claro e profundo, descobrindo o significado subjacente.",
            "examples": "Alinhar o time de produto sobre o porquê estarem construindo uma nova funcionalidade.",
            "execution": "<ol><li>Em pares, um pergunta ao outro: 'O que você faz ao trabalhar nisso?'.</li><li>Depois pergunta repetidamente (até 9 vezes): 'Por que isso é importante para você?'.</li><li>Troquem de papéis.</li><li>Compartilhem as descobertas de propósito com o grupo.</li></ol>",
            "result": "Exemplo Prático: Um programador backend de um app de farmácia, ao se perguntar 'por que?' nove vezes, concluiu: 'No fundo, não estou só conectando APIs, estou garantindo que avós solitários não fiquem sem remédios à meia-noite.' Isso aumentou incrivelmente sua motivação na Sprint."
        },
        {
            "title": "Simple Ethnography",
            "icon": "🕵️",
            "detail": "Observar pessoas e práticas reais em seu contexto real, em vez de perguntar a elas.",
            "examples": "Entender as reais dores do usuário final ao usar o software.",
            "execution": "<ol><li>Vá ao local onde o trabalho ou uso acontece (Gemba).</li><li>Observe silenciosamente e faça anotações sobre o que as pessoas realmente fazem (não o que dizem que fazem).</li><li>Conduza pequenas entrevistas contextuais.</li><li>Sintetize os achados.</li></ol>",
            "result": "Exemplo Prático: Em vez de enviar questionários, 2 analistas de UX passaram 4 horas silenciosas observando os atendentes de call center operando o sistema. Descobriram que os atendentes usavam calculadoras de mesa físicas porque o sistema tinha uma fonte minúscula na tela de taxas. Solução de 5 min do dev aumentou a agilidade deles em 20%."
        },
        {
            "title": "Integrated~Autonomy",
            "icon": "⚖️",
            "detail": "Mover de escolhas Either/Or para Both/And. Integração e Autonomia simultâneas.",
            "examples": "Balancear a padronização global com a flexibilidade local nas filiais.",
            "execution": "<ol><li>Identifique o conflito (ex: Controle vs. Liberdade).</li><li>O que fazemos para obter o benefício do lado A?</li><li>O que fazemos para obter o benefício do lado B?</li><li>Como podemos redesenhar práticas que entreguem ambos os benefícios simultaneamente?</li></ol>",
            "result": "Exemplo Prático: O conflito era 'Segurança Rígida de TI' VS 'Agilidade dos Desenvolvedores que queriam instalar libs livres'. A solução Both/And alcançada: a TI criou um 'Catálogo Automatizado Pré-Aprovado' de milhares de libs que devs podem baixar sem abrir ticket, mas que já vêm com auditoria de segurança da matriz."
        },
        {
            "title": "Critical Uncertainties",
            "icon": "🎲",
            "detail": "Desenvolver estratégias para lidar com uma variedade de futuros plausíveis.",
            "examples": "Planejamento de cenários diante de mudanças regulatórias no mercado financeiro.",
            "execution": "<ol><li>Identifique as incertezas mais críticas e imprevisíveis.</li><li>Selecione as duas principais e crie um eixo X/Y cruzando-as.</li><li>Descreva os 4 cenários extremos resultantes dos quadrantes.</li><li>Desenvolva estratégias para ter sucesso em cada cenário.</li></ol>",
            "result": "Exemplo Prático: Cruzando os eixos 'Dólar sobe para R$ 8' e 'Mercado de TI esfria drasticamente', o time formulou estratégias de sobrevivência para o cenário mais catastrófico. Criaram um comitê permanente de diversificação de portfólio em Euro para se proteger do câmbio."
        },
        {
            "title": "Discovery & Action Dialogue (DAD)",
            "icon": "💡",
            "detail": "Descobrir práticas ocultas que resolvem problemas difíceis e identificar quem pode facilitar a mudança.",
            "examples": "Resolver um problema recorrente de segurança no trabalho.",
            "execution": "<ol><li>Reúna um grupo que enfrenta o desafio.</li><li>Faça 7 perguntas estruturadas (Ex: Como você sabe que o problema está presente? Como você contribui para ele? O que você sabe que funciona para resolvê-lo?).</li><li>Apoie e escute ativamente.</li></ol>",
            "result": "Exemplo Prático: Na discussão sobre atrasos de bugs críticos, descobriram que a Dev Junior Silvia nunca tinha bugs reprovados no QA. O segredo (prática oculta) dela era validar a branch diretamente com o PO na mesa dele antes de abrir o PR oficial. Essa prática virou o padrão ouro para todos a partir daquela semana."
        },
        {
            "title": "Improv Prototyping",
            "icon": "🎭",
            "detail": "Desenvolver soluções para desafios interativos encenando-os improvisadamente.",
            "examples": "Treinar equipe de vendas em lidar com objeções difíceis.",
            "execution": "<ol><li>Defina um cenário desafiador.</li><li>Voluntários encenam as interações em pedaços curtos.</li><li>O grupo observa, para a cena e sugere novas abordagens.</li><li>Reencene aplicando as novas ideias.</li></ol>",
            "result": "Exemplo Prático: Ao simular o cancelamento irritado de um grande cliente, o Atendente João testou falar agressivamente, o que falhou. O grupo pausou a cena, sugeriu usar o tom mais baixo e empático, João reiniciou e encontrou as palavras exatas ('Compreendo sua frustração genuinamente') que acalmavam a encenação na hora."
        },
        {
            "title": "Celebrity Interview",
            "icon": "🎤",
            "detail": "Substituir apresentações chatas por entrevistas dinâmicas estilo talk show para especialistas ou líderes.",
            "examples": "Apresentação dos resultados do trimestre pelo CEO.",
            "execution": "<ol><li>O entrevistador conduz uma conversa com perguntas focadas e provocativas com o líder (a 'celebridade').</li><li>Os participantes ouvem e geram perguntas.</li><li>A 'celebridade' responde as perguntas mais relevantes do público.</li></ol>",
            "result": "Exemplo Prático: Em vez de mostrar 40 slides do DRE financeiro, a Scrum Master mediou um 'talk show' no palco com a Diretora Financeira. Pergunta direta da plateia: 'Haverá PLR (bônus) no fim de ano?'. A diretora respondeu abertamente que sim, e a equipe saiu super engajada, ignorando planilhas chatas."
        },
        {
            "title": "Heard, Seen, Respected (HSR)",
            "icon": "🫂",
            "detail": "Praticar empatia profunda para construir confiança com base no não julgamento.",
            "examples": "Resolver tensões interpessoais e quebras de confiança no time.",
            "execution": "<ol><li>Em pares, pessoa A conta uma história em que sentiu que não foi ouvida, vista ou respeitada (3 min).</li><li>Pessoa B ouve com compaixão absoluta, sem interromper.</li><li>Pessoa B compartilha o que notou e sentiu ao ouvir (2 min).</li><li>Troquem de papéis.</li></ol>",
            "result": "Exemplo Prático: Marcos (QA) ouviu Juliana (Dev) contar chorando quando teve sua ideia roubada na reunião passada. Ele apenas disse: 'Senti um aperto no peito e percebi como você se sentiu anulada'. Eles criaram um vínculo forte e Marcos tornou-se o maior aliado dela em reuniões públicas futuras."
        },
        {
            "title": "Social Network Webbing",
            "icon": "🕸️",
            "detail": "Mapear as conexões informais e revelar como o trabalho e as informações realmente fluem.",
            "examples": "Identificar influenciadores internos ocultos antes de lançar uma mudança cultural.",
            "execution": "<ol><li>Crie uma lenda de cores/formas para diferentes grupos/funções.</li><li>Cada pessoa desenha a si e as conexões-chave com quem interage para o trabalho fluir.</li><li>Junte todos em um grande mapa na parede.</li><li>Analise gargalos, silos e nós centrais.</li></ol>",
            "result": "Exemplo Prático: O mapa feito na parede revelou que TODOS na empresa, independentemente da área, dependiam das informações do estagiário de dados 'Carlos', que funcionava como um super-nó central. A gestão percebeu o risco, o promoveu imediatamente para analista sênior e criou uma equipe sob sua gestão para distribuir o gargalo."
        },
        {
            "title": "Strategy Knotworking",
            "icon": "🪢",
            "detail": "Aprofundar o alinhamento estratégico conectando múltiplos Liberating Structures em sequência.",
            "examples": "Sessão de planejamento anual completa e adaptativa.",
            "execution": "<ol><li>Use uma sequência encadeada de estruturas (Ex: Purpose to Practice -> Context Map -> Ecocycle -> Critical Uncertainties).</li><li>Faça sentido entre as atividades para formar uma estratégia coesa.</li></ol>",
            "result": "Exemplo Prático: O planejamento encadeou um '1-2-4-All' sobre a visão do ano, alimentando diretamente um 'Ecocycle' para descontinuar produtos velhos, que gerou ideias refinadas no '25/10 Crowd Sourcing'. O resultado final de 2 dias de Knotworking foram 3 macroprojetos orçados, assinados pelos líderes no ato."
        },
        {
            "title": "User Experience Fishbowl",
            "icon": "🐠",
            "detail": "Colocar os usuários reais no centro de uma conversa de produto, enquanto criadores escutam.",
            "examples": "Feedback de clientes sobre nova versão do App.",
            "execution": "<ol><li>Usuários sentam-se no centro (aquário) conversando sobre a experiência deles (não com a equipe).</li><li>A equipe (desenvolvedores, POs) senta em volta em total silêncio.</li><li>Equipe anota observações, dores e insights.</li></ol>",
            "result": "Exemplo Prático: Dois idosos foram convidados para o 'aquário' e relataram como o botão 'Resetar Senha' do aplicativo parecia confuso e os fazia bloquear o cartão semanalmente. Sete desenvolvedores ouviram de cabeça baixa anotando. Em 2 dias, reescreveram e mudaram as cores da tela focados em acessibilidade."
        },
        {
            "title": "WINFY (What I Need From You)",
            "icon": "🤲",
            "detail": "Articular clareza de necessidades cruzadas essenciais e obter respostas explícitas de comprometimento.",
            "examples": "Alinhamento de dependências no PI Planning entre diferentes tribos.",
            "execution": "<ol><li>Grupos listam necessidades críticas de outros grupos em formato claro: 'O que eu preciso de você é...'.</li><li>Os pedidos são feitos aos líderes do outro grupo no centro da sala.</li><li>A única resposta permitida de quem recebe é: 'Sim', 'Não', 'Vou tentar', ou 'Custe o que custar'. Não há espaço para justificativas.</li></ol>",
            "result": "Exemplo Prático: O time Front-End declarou: 'Backend, precisamos que a nova API de Login esteja homologada até terça-feira'. O Tech Lead do Backend respondeu secamente, olhando nos olhos: 'Custe o que custar'. Na terça de manhã a API estava entregue sem atrasos."
        },
        {
            "title": "Wicked Questions",
            "icon": "😈",
            "detail": "Articular realidades paradoxais que existem simultaneamente e devem ser gerenciadas, não resolvidas.",
            "examples": "Lidar com a tensão entre velocidade e qualidade técnica.",
            "execution": "<ol><li>Gere pares de opostos evidentes no desafio atual.</li><li>Formule a Pergunta Perversa: 'Como podemos ser simultaneamente [A] e [B]?'.</li><li>Use isso para abrir discussões honestas sobre o paradoxo.</li></ol>",
            "result": "Exemplo Prático: A equipe formulou: 'Como podemos entregar a release nova na sexta (velocidade absurda) E simultaneamente reduzir nossa taxa de bugs a zero na segunda (qualidade máxima)?'. A discussão os levou a adotar o 'Canary Release' liberando a feature primeiro apenas para 5% dos usuários."
        },
        {
            "title": "Agreement-Certainty Matrix",
            "icon": "📐",
            "detail": "Mapear o desafio com base no grau de concordância e certeza para escolher a abordagem correta.",
            "examples": "Decidir qual framework metodológico (Scrum vs Kanban vs Cascata) usar em um projeto.",
            "execution": "<ol><li>Use o gráfico de Ralph Stacey (X: Concordância, Y: Certeza).</li><li>Mapeie suas iniciativas.</li><li>Se alto nos dois, use métodos simples (Best Practices). Se no meio, complexo (Agile/Cynefin). Se baixo em ambos, Caos.</li></ol>",
            "result": "Exemplo Prático: Ao mapear o projeto de Inteligência Artificial para o RH, perceberam que tinham baixa certeza de 'como fazer' e pouca concordância sobre os requisitos. Eles estavam no quadrante do 'Complexo/Caos'. Decidiram usar sprints curtas de prototipagem (Scrum) em vez de escrever um longo documento preditivo tradicional."
        },
        {
            "title": "Talking with Pixies",
            "icon": "🧚",
            "detail": "Expor crenças limitantes e assunções usando arquétipos para encorajar vozes contrárias.",
            "examples": "Explorar razões ocultas do porquê uma iniciativa não decola.",
            "execution": "<ol><li>Peça aos participantes que assumam o papel de 'duendes' sabotadores, que cochicham dúvidas, medos ou desculpas no ouvido dos outros.</li><li>Anotem as 'desculpas' mais comuns e analisem-nas à luz do dia.</li></ol>",
            "result": "Exemplo Prático: Interpretando 'duendes' zombadores, os funcionários finalmente disseram em voz alta o que todos pensavam: 'Esse projeto de bem-estar nunca vai funcionar porque o diretor não cumpre nada'. Ao verem isso, o diretor de fato assinou uma carta de compromisso orçamentário real."
        },
        {
            "title": "Mad Tea",
            "icon": "☕",
            "detail": "Série hiper rápida de conversas intensas completando frases inacabadas.",
            "examples": "Check-in energético em uma reunião de crise.",
            "execution": "<ol><li>Forme dois círculos concêntricos (um virado para o outro).</li><li>O facilitador lê o início de uma frase (Ex: 'Se eu pudesse mudar uma coisa hoje...').</li><li>Em pares frente a frente, completam a frase (1 min total).</li><li>Círculo externo dá um passo à direita, nova frase.</li></ol>",
            "result": "Exemplo Prático: Na frase 'Minha maior frustração silenciosa nessa sprint foi...', 80% das duplas revelaram problemas com o ambiente de testes (staging). O gerente de engenharia estava na roda ouvindo dezenas de queixas sobre o mesmo ponto. Na semana seguinte, focaram apenas na reestruturação desse ambiente."
        },
        {
            "title": "Affinity Mapping",
            "icon": "📌",
            "detail": "Organizar grandes volumes de dados ou ideias em categorias lógicas com base em suas relações naturais.",
            "examples": "Organizar dezenas de insights gerados após entrevistas com usuários.",
            "execution": "<ol><li>Escreva ideias em post-its separadamente.</li><li>Em silêncio absoluto, agrupe post-its similares em clusters na parede.</li><li>Quando pararem, nomeie coletivamente cada cluster com um tema descritivo.</li></ol>",
            "result": "Exemplo Prático: 50 post-its caóticos de reclamações de usuários tornaram-se magicamente 4 grandes clusters na parede de vidro: 'Lentidão no Checkout', 'Imagens Quebradas', 'Ausência de PIX', e 'Erro no Login'. O tema 'Ausência de PIX' tinha 15 papéis, sendo priorizado para o roadmap."
        },
        {
            "title": "Lightning Talks",
            "icon": "⚡",
            "detail": "Apresentações muito curtas focadas na essência da ideia, ideal para não entediar a audiência.",
            "examples": "Demonstração de novas tecnologias que os desenvolvedores estudaram no fim de semana.",
            "execution": "<ol><li>Limite estrito de tempo por pessoa (ex: 3 a 5 minutos).</li><li>Uso mínimo ou zero de slides.</li><li>Campainha toca no limite do tempo, cortando o áudio se necessário.</li></ol>",
            "result": "Exemplo Prático: Um arquiteto apresentou, em exatos 5 minutos, como usar Docker. Ele usou apenas 3 slides de comando terminal e convenceu todos que era mais rápido. Ao estourar o cronômetro uma buzina o interrompeu, gerando aplausos da equipe que detestava reuniões de 1h de PowerPoint."
        },
        {
            "title": "Dot Voting",
            "icon": "🔴",
            "detail": "Método simples para priorizar rapidamente uma lista de ideias usando votos limitados.",
            "examples": "Escolher qual ação de melhoria da retrospectiva aplicar na próxima Sprint.",
            "execution": "<ol><li>Dê a cada pessoa 3 ou 5 'pontos' (adesivos ou marcas de caneta).</li><li>Eles distribuem seus pontos nas ideias que preferem (podem acumular mais de um ponto na mesma ideia).</li><li>As ideias com mais pontos são priorizadas.</li></ol>",
            "result": "Exemplo Prático: Diante de 10 propostas de arquitetura, cada um recebeu 3 bolinhas vermelhas. A proposta de migrar de Vue para React recebeu 18 bolinhas em 3 minutos, ganhando aprovação imediata e incontestável do comitê de Front-End para iniciar a POC."
        },
        {
            "title": "Crazy 8s",
            "icon": "8️⃣",
            "detail": "Técnica de ideação rápida para esboçar 8 ideias distintas em 8 minutos.",
            "examples": "Designers explorando diferentes layouts para a home page.",
            "execution": "<ol><li>Dobre um papel A4 para criar 8 retângulos.</li><li>Coloque um timer de 8 minutos.</li><li>Esboce rapidamente uma ideia em cada retângulo (1 min por ideia).</li></ol>",
            "result": "Exemplo Prático: Thiago (designer) precisava recriar a tela de onboarding. Nos primeiros 4 quadrados ele desenhou telas padrões. No 7º quadrado, sem tempo para raciocinar, esboçou um 'chatbot interativo que ensina brincando', ideia maluca que acabou virando a principal atração de retenção do novo App."
        },
        {
            "title": "Brainwriting",
            "icon": "📝",
            "detail": "Geração de ideias em silêncio. Reduz a influência das vozes dominantes e foca na qualidade da reflexão.",
            "examples": "Ideação de soluções técnicas complexas onde introvertidos têm boas ideias.",
            "execution": "<ol><li>Cada pessoa escreve 3 ideias em um papel (5 min).</li><li>Passa o papel para o colega do lado.</li><li>O colega lê as ideias e adiciona mais 3 ideias inspiradas ou novas (5 min).</li><li>Repita algumas rodadas.</li></ol>",
            "result": "Exemplo Prático: Laura, a dev mais quieta da equipe, escreveu uma ideia tímida de 'otimizar o script X' na rodada 1. O Tech Lead, que nunca a escutava em voz alta, pegou o papel na rodada 2 e acrescentou 'Genial, podemos usar CRON jobs nisso', construindo juntos a solução definitiva do gargalo de performance."
        },
        {
            "title": "SCAMPER",
            "icon": "🛠️",
            "detail": "Ferramenta provocativa de criatividade que estimula pensar sobre produtos/serviços através de 7 verbos.",
            "examples": "Reinventar uma funcionalidade estagnada do produto.",
            "execution": "<ol><li>Passe pelo acrônimo: Substituir, Combinar, Adaptar, Modificar, Procurar outros usos, Eliminar, Reorganizar.</li><li>Para cada letra, questione: Como aplico este verbo ao meu produto?</li></ol>",
            "result": "Exemplo Prático: Aplicando o 'E' de Eliminar, o Product Manager questionou: 'E se eliminarmos a tela inteira de cadastro no nosso App?'. Nasceu ali a solução de login instantâneo com botão Apple/Google, reduzindo a taxa de abandono na entrada em incríveis 65%."
        },
        {
            "title": "Six Thinking Hats",
            "icon": "🎩",
            "detail": "Explorar um problema de diferentes perspectivas separadamente, reduzindo conflitos e egos.",
            "examples": "Análise de uma decisão controversa sobre compra de tecnologia.",
            "execution": "<ol><li>Determine as cores: Branco (fatos), Vermelho (emoção), Preto (riscos), Amarelo (benefícios), Verde (criatividade), Azul (controle).</li><li>O grupo usa 'metaforicamente' um chapéu de cada vez, discutindo apenas sob aquela ótica, em conjunto.</li></ol>",
            "result": "Exemplo Prático: Ao discutir o retorno híbrido ao escritório, a diretoria estava travada em acusações de emoção vs racionalidade. Ao vestir obrigatoriamente o Chapéu Preto, até os otimistas elencaram riscos reais; e no Chapéu Amarelo, os pessimistas criaram benefícios. A decisão final (2x semana presencial) foi unânime e pacífica."
        },
        {
            "title": "Sailboat Retrospective",
            "icon": "⛵",
            "detail": "Metáfora visual para identificar forças que ajudam ou atrapalham a equipe a atingir a meta.",
            "examples": "Retrospectiva de final de trimestre.",
            "execution": "<ol><li>Desenhe um barco.</li><li>Vento/Velas: O que nos empurra para frente?</li><li>Âncoras: O que nos segura?</li><li>Rochedos: Quais são os riscos à frente?</li><li>Ilha: Qual é o objetivo?</li></ol>",
            "result": "Exemplo Prático: O time colocou 'Github Copilot' como o vento nas velas, mas encheu as âncoras no fundo do mar com a frase: 'Revisão burocrática de PR pelo comitê central'. Definiram a ilha como 'Entrega Contínua Diária'. Decidiram cortar a âncora abolindo o comitê central e passando a revisão para os tech leads locais."
        },
        {
            "title": "Starfish Retrospective",
            "icon": "⭐",
            "detail": "Expandir o foco da retrospectiva em 5 direções para gerar feedback mais granular.",
            "examples": "Revisar as práticas de engenharia de uma squad madura.",
            "execution": "<ol><li>Desenhe uma estrela com 5 pontas: Começar a fazer, Parar de fazer, Fazer Mais, Fazer Menos, Continuar fazendo.</li><li>Participantes inserem post-its nas categorias correspondentes.</li></ol>",
            "result": "Exemplo Prático: No braço de 'Fazer Menos', a equipe listou 'Reuniões de Refinamento de 3 horas' e no braço 'Começar a Fazer' surgiu 'Escrever Critérios de Aceite no Jira antes da reunião'. Como resultado, a próxima reunião cortou seu tempo de 3h para 45min com maior eficácia."
        },
        {
            "title": "4 Ls Retrospective",
            "icon": "📚",
            "detail": "Estrutura rápida e eficaz para retrospectivas focada em 4 reflexões com a letra L.",
            "examples": "Retrospectiva curta de uma sprint de 1 semana.",
            "execution": "<ol><li>Crie 4 quadrantes: Liked (Gostei), Learned (Aprendi), Lacked (Senti falta), Longed for (Desejei).</li><li>Time preenche os quadrantes com post-its.</li><li>Agrupa-se os pontos comuns e discute-se soluções.</li></ol>",
            "result": "Exemplo Prático: No quadrante 'Lacked' (Senti falta), 4 desenvolvedores postaram 'Cerveja na sexta'. No quadrante 'Learned' um designer postou 'Descobri que o Figma exporta CSS direto'. Saíram da sala felizes com a nova técnica aprendida e um voucher de iFood garantido para o Happy Hour de sexta."
        },
        {
            "title": "Speed Boat",
            "icon": "🚤",
            "detail": "Dinâmica similar ao veleiro, mas focada primordialmente em identificar os 'freios' e 'motores'.",
            "examples": "Investigar por que a esteira de deployment contínuo está lenta.",
            "execution": "<ol><li>Desenhe um barco a motor.</li><li>Motores: O que nos acelera?</li><li>Âncoras/Pesos: O que nos freia?</li><li>Foque fortemente em identificar formas de 'cortar a corda' das âncoras.</li></ol>",
            "result": "Exemplo Prático: Na lancha da equipe, os post-its nas hélices mostravam o orgulho de baterem metas seguidas. As âncoras revelaram que 'aprovadores ausentes no Slack' seguravam as tarefas na coluna de 'Testing' por 3 dias seguidos. Eles criaram um robô de notificação SMS de emergência focado nesses aprovadores 'freios'."
        },
        {
            "title": "Pomodoro Brainstorming",
            "icon": "🍅",
            "detail": "Combina a técnica Pomodoro com ideação para forçar foco profundo por tempos curtos.",
            "examples": "Sessão de ideação de campanhas de marketing com prazo apertado.",
            "execution": "<ol><li>Defina 25 minutos de foco absoluto (sem distrações, celulares, etc).</li><li>Ideação livre em silêncio.</li><li>Pausa de 5 minutos.</li><li>Segundo pomodoro para agrupamento e seleção.</li></ol>",
            "result": "Exemplo Prático: O time desligou os celulares. Nos primeiros 25 min focados, geraram 120 nomes potenciais para o novo banco digital sem interrupções. Na pausa tomaram café na copa. No 2º Pomodoro, votaram em silêncio e o nome oficial do produto (BankX) foi cravado 15 minutos antes do relógio despertar."
        }
    ],
    "Management 3.0 & Engajamento": [
        {
            "title": "Moving Motivators",
            "icon": "🚀",
            "detail": "Dinâmica para entender os motivadores intrínsecos de cada pessoa usando 10 cartas (CHAMPFROGS). Útil em 1:1s e team buildings.",
            "examples": "Avaliar o impacto de uma mudança organizacional na motivação do time.",
            "execution": "<ol><li>Distribuir as 10 cartas de motivadores.</li><li>Pedir que a pessoa ordene da mais importante à menos importante.</li><li>Mover cartas para cima ou baixo dependendo do impacto da situação atual.</li></ol>",
            "result": "A desenvolvedora sênior 'Ana' mapeou que seus motivadores principais eram 'Maestria' e 'Liberdade'. Após perceberem que a mudança para o novo projeto engessado rebaixou essas cartas, o gerente 'Carlos' combinou que Ana lideraria a arquitetura técnica às sextas-feiras. A motivação de Ana saltou visivelmente, e a entrega de bugs reduziu em 15% em 2 meses."
        },
        {
            "title": "Delegation Poker",
            "icon": "🃏",
            "detail": "Jogo para definir claramente os níveis de delegação e autoridade (de 1 a 7) entre a gestão e o time.",
            "examples": "Decidir quem aprova as férias da equipe ou quem escolhe as ferramentas de trabalho.",
            "execution": "<ol><li>Apresentar um cenário de decisão.</li><li>Cada participante escolhe uma carta de 1 (Tell) a 7 (Delegate).</li><li>Revelar simultaneamente e debater as diferenças.</li></ol>",
            "result": "No board de delegação, a equipe 'Omega' definiu o nível '6 - Perguntar' para 'Escolha de Stack Técnico'. Isso significa que os próprios desenvolvedores (Pedro e Lucas) decidem se usarão Node.js ou Python, e apenas informam a líder técnica 'Marta' após a decisão. Em contrapartida, para 'Contratação de Juniores', o grupo acordou o nível '3 - Consultar', onde Marta decide, mas antes escuta a opinião do time. A autonomia aumentou e as reclamações sobre microgerenciamento caíram a zero."
        },
        {
            "title": "Kudo Cards",
            "icon": "💌",
            "detail": "Sistema de reconhecimento entre pares através de pequenos cartões de agradecimento para promover uma cultura de valorização.",
            "examples": "Agradecer um colega que ajudou a resolver um bug crítico.",
            "execution": "<ol><li>Disponibilizar os Kudo Cards e uma Kudo Box.</li><li>Incentivar o time a escrever agradecimentos.</li><li>Ler os cartões publicamente durante reuniões semanais.</li></ol>",
            "result": "A caixa de Kudos física localizada na entrada do setor acumulou 42 cartões em um único mês. Um dos cartões de destaque foi de 'Juliana' (QA) para 'Ricardo' (Dev), dizendo: 'Obrigada por ficar até as 19h me ajudando a mockar o banco de dados. Salvou a entrega de sexta!'. No fim do mês, o gestor leu todos em voz alta, e os três funcionários com mais Kudos recebidos ganharam um par de ingressos para o cinema."
        },
        {
            "title": "Personal Maps",
            "icon": "🗺️",
            "detail": "Técnica de quebra-gelo para construir proximidade e empatia, criando mapas mentais sobre a vida de cada membro.",
            "examples": "Integração de um novo membro no time (onboarding).",
            "execution": "<ol><li>Colocar o nome da pessoa no centro.</li><li>Criar ramificações com categorias: família, hobbies, valores, amigos.</li><li>Apresentar o mapa para o grupo.</li></ol>",
            "result": "Durante o onboarding de 'Fernando', o novo Product Owner, o time fez uma sessão de 30 minutos. O mapa revelou que ele era colecionador de jogos de tabuleiro, mesma paixão do desenvolvedor 'Bruno'. Isso gerou uma conexão imediata, e no mesmo dia eles marcaram uma noite de jogos. A barreira inicial da chefia foi quebrada, e nos refinamentos seguintes, a comunicação fluiu com muito mais empatia e liberdade."
        },
        {
            "title": "Celebration Grid",
            "icon": "🎉",
            "detail": "Ferramenta visual para analisar o que deu certo, o que deu errado e o que foi aprendido através de experimentos.",
            "examples": "Retrospectiva de um projeto que não atingiu todas as metas.",
            "execution": "<ol><li>Desenhar o grid (Erros, Experimentos, Práticas).</li><li>O time adiciona post-its relatando o que aconteceu.</li><li>Celebrar os aprendizados, independentemente de sucesso ou falha.</li></ol>",
            "result": "Após o fracasso da campanha de Black Friday (o servidor caiu por 2 horas), o squad 'Checkout' montou o grid. Na coluna 'Erros', postaram 'Não testamos a carga limite no banco'. Na coluna 'Experimentos com falha', postaram 'O novo cache Redis não suportou os spikes'. O CTO 'Marcos' aplaudiu o experimento do Redis e a equipe extraiu um aprendizado prático: implementar testes de stress de 50k requests por segundo. A equipe saiu energizada em vez de desmotivada e focada em melhorar."
        },
        {
            "title": "Niko-Niko Calendar",
            "icon": "😊",
            "detail": "Calendário visual onde cada membro registra seu humor diariamente para monitorar o moral da equipe ao longo do tempo.",
            "examples": "Identificar quando o time está muito estressado antes de uma entrega.",
            "execution": "<ol><li>Criar um calendário com os nomes e dias do mês.</li><li>Ao final do dia, cada pessoa desenha um smiley face correspondente ao seu humor.</li><li>Discutir tendências em reuniões regulares.</li></ol>",
            "result": "Na segunda semana da Sprint, a Scrum Master 'Beatriz' notou que o desenvolvedor 'João' desenhou uma carinha triste vermelha ('😟') por três dias consecutivos, e 'Maria' também mudou para amarelo. Na daily, Beatriz perguntou se algo estava atrapalhando. Eles revelaram que a documentação da API do parceiro estava totalmente desatualizada, gerando estresse. Beatriz bloqueou a tarefa imediatamente e escalou o problema para o gerente, aliviando a pressão sobre o time instantaneamente."
        },
        {
            "title": "Feedback Wrap",
            "icon": "🌯",
            "detail": "Formato estruturado para dar feedback construtivo de maneira empática e focado em contexto, observações e emoções.",
            "examples": "Fornecer feedback sobre um comportamento inadequado em reuniões.",
            "execution": "<ol><li>Descrever o contexto.</li><li>Listar observações sem julgamento.</li><li>Expressar emoções pessoais.</li><li>Explicar o valor agregado.</li><li>Sugerir ações futuras.</li></ol>",
            "result": "O gerente 'Rafael' enviou um feedback para 'Sofia': 'Contexto: Na nossa reunião de review ontem de manhã. Observação: Notei que você interrompeu o cliente três vezes enquanto ele descrevia a dor dele. Emoção: Fiquei preocupado porque senti que o cliente pareceu frustrado. Valor: Precisamos que o cliente sinta que suas dores são validadas para manter o contrato ativo. Sugestão: Nas próximas calls, que tal anotar as dúvidas e só perguntar no final da fala dele?'. Sofia compreendeu sem ficar na defensiva e aplicou a mudança na mesma semana."
        },
        {
            "title": "Merit Money",
            "icon": "💰",
            "detail": "Sistema de recompensa distribuída onde os próprios colegas alocam bônus baseados no mérito de cada um.",
            "examples": "Distribuição de um bônus anual do projeto de forma descentralizada.",
            "execution": "<ol><li>Distribuir uma moeda virtual para todos.</li><li>Eles devem dar essas moedas aos colegas com base em ajudas e méritos.</li><li>Converter os pontos em recompensas reais periodicamente.</li></ol>",
            "result": "No final de novembro, o departamento de engenharia distribuiu 100 'Moedas Estrela' virtuais para cada um dos 15 membros. A desenvolvedora 'Camila' doou 30 de suas moedas para 'Felipe' por ele ter refatorado o componente de login sem ninguém pedir. Quando o sistema fechou o ciclo no dia 30, Felipe acumulava 120 moedas, o que ele converteu via plataforma do RH em um vale-compras de R$ 300,00 na Amazon e um jantar pago para duas pessoas."
        },
        {
            "title": "Team Competency Matrix",
            "icon": "📊",
            "detail": "Matriz para mapear e visualizar as habilidades individuais em relação às necessidades da equipe, identificando gaps.",
            "examples": "Planejar contratações ou treinamentos baseados em deficiências do time atual.",
            "execution": "<ol><li>Listar as competências necessárias.</li><li>Cada membro avalia seu nível (Aprendiz, Praticante, Especialista).</li><li>Identificar áreas sem especialistas e criar planos de ação.</li></ol>",
            "result": "A tabela exposta no Miro mostrou uma linha vermelha assustadora: na coluna 'React Native', apenas 'Thiago' era 'Especialista', enquanto outros três eram 'Aprendizes'. Ao ver esse risco sistêmico, o líder do projeto autorizou que 'Thiago' parasse de pegar tarefas complexas e passasse 10 horas semanais fazendo pair programming com 'Sara' e 'Luan'. Três meses depois, a matriz foi atualizada e 'Sara' subiu para 'Praticante', reduzindo o gargalo no mobile."
        },
        {
            "title": "Happiness Door",
            "icon": "🚪",
            "detail": "Combinação de Niko-Niko e feedback instantâneo para avaliar o engajamento e a percepção após reuniões e treinamentos.",
            "examples": "Saber se um workshop foi útil antes de as pessoas saírem da sala.",
            "execution": "<ol><li>Colar post-its de humor (feliz, neutro, triste) perto da porta.</li><li>Ao sair, os participantes colam feedbacks rápidos sob a carinha correspondente.</li><li>Revisar e adaptar para a próxima sessão.</li></ol>",
            "result": "Após a sessão de treinamento de 4 horas sobre Kubernetes, 25 engenheiros saíram da sala. Na porta, havia 3 carinhas coladas (😄, 😐, 😢). 18 pessoas colaram post-its amarelos abaixo do 😄 dizendo 'Exercícios práticos excelentes!', mas 5 pessoas colaram no 😐 dizendo 'Faltou falar sobre Helm charts' e 2 no 😢 com 'Muito rápido, me perdi'. O instrutor 'Leonardo' imediatamente ajustou a ementa do próximo workshop para focar em Helm e desacelerou a introdução."
        },
        {
            "title": "Value Poker",
            "icon": "💎",
            "detail": "Jogo para questionar e alinhar quais são os valores reais da equipe comparados com os valores corporativos desejados.",
            "examples": "Criação de um novo manifesto de equipe.",
            "execution": "<ol><li>Utilizar cartas de valores.</li><li>Cada pessoa escolhe os valores que acha mais importantes.</li><li>Debater até convergir para um conjunto de 5 a 7 valores centrais.</li></ol>",
            "result": "O squad 'Pagamentos' estava sempre em atrito. Jogaram o Value Poker e, no final de uma hora, reduziram de 50 para 4 valores essenciais. O valor número 1 escolhido foi 'Transparência Absoluta'. O desenvolvedor 'Rodrigo' argumentou que não tolerava mais esconder bugs do PO. A partir daquele dia, eles criaram um canal no Slack '#bugs-feios' onde todos os erros são postados em menos de 5 minutos, melhorando o clima drasticamente."
        },
        {
            "title": "Meddlers Game",
            "icon": "🧩",
            "detail": "Ferramenta tátil para visualizar, discutir e projetar a estrutura organizacional e o design de equipes.",
            "examples": "Reestruturar departamentos para adotar o modelo de Tribos e Squads.",
            "execution": "<ol><li>Usar peças (avatares) para representar papéis e pessoas.</li><li>Desenhar conexões e agrupar em times (hexágonos).</li><li>Simular como a comunicação vai fluir e ajustar.</li></ol>",
            "result": "Durante o planejamento de escala, a diretora 'Teresa' e 5 gerentes brincaram com os hexágonos e avatares por duas horas. Eles visualizaram que o 'Time A' dependia de um designer isolado no 'Time B'. Eles moveram o avatar do designer 'Lucas' fisicamente para o centro do hexágono compartilhado, criando um modelo de 'Designer Chapter'. Quando a nova estrutura foi anunciada, Lucas agradeceu, pois finalmente tinha autonomia sem criar bloqueios."
        },
        {
            "title": "Guilds & Communities of Practice",
            "icon": "🤝",
            "detail": "Criação de grupos de interesse voluntários inter-times para compartilhar conhecimento em áreas específicas.",
            "examples": "Desenvolvedores Front-end de diferentes times se reunindo para definir padrões.",
            "execution": "<ol><li>Identificar um tema em comum.</li><li>Encontrar um líder voluntário para a guilda.</li><li>Agendar reuniões periódicas para compartilhar experiências.</li></ol>",
            "result": "A guilda de 'Segurança da Informação' começou com apenas 3 pessoas. Após seis meses de encontros quinzenais às quintas-feiras (com pizza paga pela empresa), agora reúne 22 desenvolvedores de 8 squads diferentes. O líder voluntário 'Arthur' e o time já criaram uma biblioteca padrão de sanitização de inputs que foi adotada por toda a empresa, reduzindo vulnerabilidades XSS reportadas de 12 por mês para zero."
        },
        {
            "title": "Culture Books",
            "icon": "📖",
            "detail": "Livro digital ou físico construído colaborativamente que captura a essência, histórias e identidade do time.",
            "examples": "Um guia para integrar recém-chegados ensinando \"como fazemos as coisas aqui\".",
            "execution": "<ol><li>Coletar histórias e fotos dos membros.</li><li>Escrever sobre os valores vividos na prática.</li><li>Publicar e atualizar anualmente.</li></ol>",
            "result": "O 'Livro de Cultura da Tribo Mobile' foi impresso em capa dura com 40 páginas. A página 15, escrita pela dev 'Fernanda', conta a história hilária de quando eles deletaram o banco de produção de madruga e como a gestão reagiu comprando lanches em vez de demitir alguém. Todo novo contratado agora recebe esse livro na primeira manhã. O índice de turnover nos primeiros 90 dias caiu em 25% após essa iniciativa."
        },
        {
            "title": "Improvement Dialogues",
            "icon": "💬",
            "detail": "Diálogos estruturados entre líderes e membros do time focados não em avaliação, mas em melhoria contínua e mentoria.",
            "examples": "Substituir a avaliação de desempenho anual por conversas mensais de carreira.",
            "execution": "<ol><li>Preparar perguntas focadas no futuro.</li><li>Fazer a reunião num ambiente informal (ex: caminhando).</li><li>Documentar metas de melhoria combinadas.</li></ol>",
            "result": "No passeio até a cafeteria, o gestor 'Paulo' e o júnior 'Diego' esqueceram as notas do antigo 'Avaliação 360'. Paulo apenas perguntou: 'No que você sente que gastou energia à toa este mês?'. Diego revelou que gastava 4 horas por semana configurando o ambiente local de testes. Eles concordaram com a meta de melhoria: Paulo compraria licenças de uma ferramenta cloud, e Diego focaria em aprender testes E2E com Cypress."
        },
        {
            "title": "Exploration Days (Hackathons)",
            "icon": "🧪",
            "detail": "Tempo dedicado (geralmente 24h) para a equipe trabalhar no que quiser, desde que gere valor para a empresa ou para eles mesmos.",
            "examples": "Os 'FedEx Days' ou 'ShipIt Days', onde os times entregam algo inovador em 24h.",
            "execution": "<ol><li>Definir e anunciar a data.</li><li>Equipes se formam organicamente e escolhem as ideias.</li><li>Apresentar os resultados num evento de celebração no final.</li></ol>",
            "result": "Durante o FedEx Day de quinta e sexta-feira, os devs 'Hugo' e 'Bárbara' decidiram ignorar o backlog e criaram um script de automação usando IA para categorizar chamados de suporte. Na apresentação de sexta às 16h, eles mostraram um protótipo funcional. O diretor adorou, financiou o projeto, e a ferramenta foi para produção no mês seguinte, economizando 40 horas semanais do time de atendimento ao cliente."
        },
        {
            "title": "Salary Formula",
            "icon": "⚖️",
            "detail": "Criação de fórmulas salariais abertas e transparentes para remover vieses de negociação e injustiças.",
            "examples": "Divulgar como o salário é calculado com base em cargo, experiência e custo de vida.",
            "execution": "<ol><li>Definir critérios objetivos de remuneração.</li><li>Elaborar a fórmula publicamente.</li><li>Aplicar a todos e deixar aberta para ajustes futuros.</li></ol>",
            "result": "O CTO 'Daniel' publicou na intranet a planilha: Salário = Base(R$ 5000) * Nível(1 a 3) + Adicional Mercado (R$ 1000). A desenvolvedora 'Clarice', que descobriu estar ganhando R$ 2000 a menos que o colega com as mesmas responsabilidades, teve seu salário ajustado automaticamente na folha seguinte. O RH reportou que o sentimento de injustiça medido na pesquisa de clima caiu de 38% para 4%, e as fofocas sobre salários terminaram."
        },
        {
            "title": "Lean Coffee",
            "icon": "☕",
            "detail": "Reunião sem pauta pré-definida, onde os tópicos são levantados, votados e discutidos de forma democratizada (timeboxing).",
            "examples": "Comunidade de prática ou alinhamento matinal de gestão.",
            "execution": "<ol><li>Participantes escrevem temas em post-its.</li><li>Fazem dot-voting para priorizar.</li><li>Discutem o mais votado por 5 minutos e decidem se continuam ou mudam de tópico.</li></ol>",
            "result": "Na comunidade de práticas de DevOps, os participantes trouxeram 15 temas e votaram. O tema mais votado com 8 pontos foi 'Gerenciamento de Segredos no AWS'. O cronômetro marcou 5 minutos e eles focaram exclusivamente nisso. Ao fim, votaram com 'polegar para cima' para continuar por mais 3 minutos. Em 30 minutos, eles resolveram 4 gargalos de infraestrutura de forma estruturada, algo que a reunião tradicional levava 2 horas para não concluir."
        },
        {
            "title": "Starfish Retrospective",
            "icon": "⭐",
            "detail": "Formato de retrospectiva que mapeia as ações em 5 categorias: Começar, Parar, Continuar, Fazer Mais, Fazer Menos.",
            "examples": "Avaliação no final de uma sprint longa.",
            "execution": "<ol><li>Desenhar uma estrela dividindo as 5 áreas.</li><li>O time preenche com post-its.</li><li>Debater os itens e extrair ações de melhoria.</li></ol>",
            "result": "No quadro digital, sob a ponta 'Começar a Fazer', a equipe colou 5 post-its sobre 'Fazer deploy às terças de manhã, não sextas à tarde'. Em 'Parar de Fazer', 'Roberto' colocou: 'Reuniões de status diárias sem propósito'. O resultado tangível: na sprint seguinte, a Daily foi reduzida para 10 minutos focada em bloqueios, e os deploys de sexta foram bloqueados no pipeline do GitLab. A equipe ganhou 3 horas produtivas na semana."
        },
        {
            "title": "Sailboat Retrospective",
            "icon": "⛵",
            "detail": "Retrospectiva visual usando a metáfora de um barco, vento (impulsionadores) e âncoras (impedimentos).",
            "examples": "Identificar riscos e gargalos no time.",
            "execution": "<ol><li>Desenhar um barco, vento, ilha e âncoras.</li><li>O time preenche post-its para cada metáfora.</li><li>Agrupar problemas e priorizar resoluções.</li></ol>",
            "result": "Ao desenharem a metáfora no Miro, a ilha (objetivo) era 'Lançamento do App v2.0'. Os ventos (impulsionadores) incluíam 'A nova API está muito rápida'. Mas as âncoras afundando o barco eram preocupantes: 'Dependência da aprovação da Apple'. O PO 'Marcelo' pegou esse post-it da âncora, transformou num ticket prioritário e antecipou a submissão de aprovação da loja em 15 dias, evitando o atraso que destruiria o cronograma do marketing."
        },
        {
            "title": "1-2-4-All",
            "icon": "🗣️",
            "detail": "Estrutura Libertadora para garantir que todos tenham voz e gerem ideias, escalando da reflexão individual para o grupo.",
            "examples": "Brainstorming para resolver um problema arquitetural complexo.",
            "execution": "<ol><li>1 min refletindo sozinho.</li><li>2 mins debatendo em dupla.</li><li>4 mins debatendo em quarteto.</li><li>O grupo todo compartilha os destaques.</li></ol>",
            "result": "Para resolver a arquitetura de microsserviços, 16 engenheiros silenciaram por 1 minuto (gerando 16 ideias individuais). Depois, duplas discutiram, filtrando para 8 ideias. Nos quartetos, as opções fortes sobreviveram, gerando 4 propostas sólidas. Em 12 minutos, toda a equipe convergiu para uma arquitetura híbrida focada em Serverless sugerida pela arquiteta 'Vanessa', que era muito tímida e jamais teria falado em um brainstorming caótico e barulhento tradicional."
        },
        {
            "title": "Troika Consulting",
            "icon": "👥",
            "detail": "Estrutura Libertadora onde os participantes recebem consultoria rápida de colegas em grupos de três.",
            "examples": "Ajudar gerentes a resolver desafios diários.",
            "execution": "<ol><li>Formar trios.</li><li>Uma pessoa (cliente) explica o problema.</li><li>Os outros dois dão conselhos enquanto o cliente apenas escuta.</li><li>Rotacionar.</li></ol>",
            "result": "O Agile Coach 'Igor' colocou o desafio no trio: 'Meus líderes não engajam nas cerimônias'. Ele virou as costas virtualmente na chamada e só ouviu. 'Tatiana' disse: 'Eu reduziria o tempo e pediria para eles guiarem a pauta'. 'Jonas' sugeriu: 'Já tentou trazer dados de delivery em vez de falar de ritos?'. Em apenas 10 minutos, Igor anotou a ideia de Jonas, mudou a linguagem de 'Cerimônias' para 'Reunião de Métricas' e garantiu 100% de presença gerencial na semana seguinte."
        },
        {
            "title": "Ecocycle Planning",
            "icon": "♻️",
            "detail": "Técnica para analisar o portfólio de projetos, mapeando-os nas fases do ecociclo (nascimento, maturidade, destruição criativa).",
            "examples": "Revisão trimestral de produtos em operação.",
            "execution": "<ol><li>Mapear as fases do ecociclo na parede.</li><li>Colocar todos os projetos nas áreas respectivas.</li><li>Identificar projetos travados ou que precisam ser encerrados.</li></ol>",
            "result": "O time de liderança espalhou 20 produtos no ecociclo desenhado na parede. O produto 'App de Fórum Interno', mantido a custo altíssimo de R$ 15.000 mensais com apenas 10 acessos, estava visivelmente travado na fase de 'Maturidade/Rigidez'. O diretor 'Vitor' concordou em movê-lo para 'Destruição Criativa'. No dia seguinte, eles desligaram o serviço e liberaram 2 desenvolvedores experientes que estavam frustrados apenas corrigindo bugs irrelevantes."
        },
        {
            "title": "Appreciative Interviews",
            "icon": "🎤",
            "detail": "Entrevistas em pares focadas em descobrir condições que geraram sucessos passados, para replicá-los.",
            "examples": "Início de um workshop de engajamento.",
            "execution": "<ol><li>Formar pares.</li><li>Entrevistar focado numa experiência de ápice profissional.</li><li>Extrair o que tornou o sucesso possível.</li></ol>",
            "result": "Em vez de focar na última sprint desastrosa, o Scrum Master 'Caio' pediu pares. 'Alice' perguntou a 'Roberto': 'Conte-me sobre a melhor sprint que já tivemos'. Ele lembrou de janeiro: 'O critério de aceite estava perfeito e tínhamos acesso direto ao usuário final'. A partir dessa entrevista, a equipe aprovou uma regra concreta: Nenhuma história entra no quadro sem validação direta do cliente 'Julia', o que dobrou a precisão das entregas."
        },
        {
            "title": "Fist of Five",
            "icon": "🖐️",
            "detail": "Técnica de consenso rápida onde as pessoas usam os dedos da mão para votar o nível de acordo.",
            "examples": "Votar em uma decisão arquitetural durante uma planning.",
            "execution": "<ol><li>Apresentar a proposta.</li><li>Ao sinal, todos mostram de 1 a 5 dedos (1 = discordo totalmente, 5 = concordo totalmente).</li><li>Se houver 1s ou 2s, debater suas preocupações.</li></ol>",
            "result": "A proposta era 'Migrar do Jira para o Trello'. O líder de engenharia, 'Sérgio', deu 5 (Concordo totalmente). Mas a QA 'Amanda' levantou 2 dedos e explicou: 'No Trello perderemos o rastreamento das nossas suítes de testes automatizados integrados aos tickets'. A votação expôs um risco crítico ignorado. Em 5 minutos, Sérgio alterou a proposta: 'Migrar para o Trello APENAS as tarefas de marketing', recebendo aprovação unânime e evitando um desastre de compliance."
        },
        {
            "title": "Dot Voting",
            "icon": "🔴",
            "detail": "Ferramenta democrática de priorização onde as pessoas distribuem adesivos (pontos) nas opções que preferem.",
            "examples": "Escolher quais tópicos focar após uma retrospectiva.",
            "execution": "<ol><li>Listar as opções.</li><li>Dar um número fixo de votos (pontos) para cada pessoa.</li><li>Votar simultaneamente e contar os resultados.</li></ol>",
            "result": "Após levantar 10 problemas técnicos na retrospectiva, a equipe recebeu 3 pontos adesivos vermelhos cada. 'Refatorar o banco legado' recebeu 18 pontos totais, enquanto 'Trocar a cor do botão admin' teve zero. Com esse respaldo quantitativo, o líder 'Márcio' colocou a refatoração do banco no topo da Sprint Backlog, justificando aos stakeholders que aquela era a prioridade democrática número um da equipe técnica inteira."
        },
        {
            "title": "Magic Estimation",
            "icon": "🪄",
            "detail": "Técnica silenciosa e rápida para estimar o tamanho de muitas tarefas ou histórias de usuário aglomerando-as.",
            "examples": "Estimar um backlog inicial de projeto inteiro em 30 minutos.",
            "execution": "<ol><li>Colocar os valores (ex: Fibonacci) na mesa.</li><li>Distribuir os cartões com as tarefas para a equipe.</li><li>Em silêncio, a equipe coloca as tarefas abaixo dos tamanhos e pode mover as dos outros.</li></ol>",
            "result": "O PO 'Fábio' chegou com 80 histórias de usuário não estimadas. Usando cartões físicos na mesa com a sequência de Fibonacci, 7 desenvolvedores trabalharam em total silêncio. 'Marina' movia um cartão complexo de API para 13 pontos, e 'Claudio' puxava para 8. Quando discordaram movendo 3 vezes o mesmo cartão, separaram para discussão. Em apenas 45 minutos, eles estimaram 72 histórias relativas a um trimestre inteiro, poupando semanas de longas reuniões de planning."
        },
        {
            "title": "Systemic Consensus",
            "icon": "📉",
            "detail": "Método de tomada de decisão que não busca a opção mais amada, mas a opção com menor resistência no grupo.",
            "examples": "Decidir qual ferramenta de gestão adotar para o ano.",
            "execution": "<ol><li>Listar opções.</li><li>Cada membro dá uma nota de resistência de 0 a 10 (10 = forte oposição).</li><li>A opção com menor pontuação de resistência ganha.</li></ol>",
            "result": "O comitê diretivo precisava escolher o destino do retiro anual da empresa. Opção A: Resort de Luxo (Preferida pelo CEO, resistência: 45 pontos devido à viagem de 6 horas de ônibus); Opção B: Chácara próxima (resistência: 12 pontos, fácil acesso). O retiro ocorreu na chácara próxima. Embora não fosse o sonho de consumo luxuoso do CEO, a adesão foi de 95% e não houve opositores reclamando da logística da viagem no Slack."
        },
        {
            "title": "Empathy Map",
            "icon": "🧠",
            "detail": "Ferramenta visual para sintetizar observações sobre os usuários e promover empatia na equipe.",
            "examples": "Entender as necessidades de um novo tipo de cliente.",
            "execution": "<ol><li>Desenhar o mapa: O que vê? O que pensa? O que faz? O que ouve? Dores, Ganhos.</li><li>Preencher com dados de pesquisa.</li><li>Usar como base para criação de produtos.</li></ol>",
            "result": "A equipe de UX estava criando um app para idosos. Preencheram o mapa com insights de campo. O que ouvem? 'Meus netos dizem que é fácil'. O que veem? 'Botões minúsculos, textos claros'. Dores: 'Medo absurdo de clicar e apagar algo, medo de fraudes'. Ganhos: 'Independência financeira'. O resultado material: o time descartou o design 'minimalista moderno', adotando botões gigantes, textos descritivos e alertas verdes amigáveis de confirmação. A retenção no onboarding subiu 60%."
        },
        {
            "title": "Johari Window",
            "icon": "🪟",
            "detail": "Dinâmica para melhorar o autoconhecimento e a comunicação, revelando pontos cegos na percepção pessoal.",
            "examples": "Desenvolvimento de liderança.",
            "execution": "<ol><li>Escolher adjetivos que a pessoa acha que tem.</li><li>Os pares escolhem adjetivos para ela.</li><li>Mapear as respostas nas áreas: Aberta, Cega, Oculta, Desconhecida.</li></ol>",
            "result": "O Tech Lead 'Gustavo' fez o exercício com 4 colegas. Ele se descrevia apenas como 'Técnico' e 'Lógico'. Porém, os colegas consistentemente escolheram adjetivos na área cega dele: 'Impaciente' e 'Intimidador'. Gustavo ficou chocado, pois achava que apenas focava em resolver problemas rápido. O resultado foi um plano de ação imediato com RH para treinamento em comunicação não violenta, e na avaliação do próximo semestre a reclamação de intimidação zerou."
        },
        {
            "title": "Trust Canvas",
            "icon": "🛡️",
            "detail": "Ferramenta para mapear e construir confiança ativa entre membros de um time, abordando vulnerabilidades.",
            "examples": "Kickoff de uma nova equipe com integrantes céticos.",
            "execution": "<ol><li>Preencher os pilares: Transparência, Empatia, Competência, Compromisso.</li><li>Discutir ações diárias que reforçam cada pilar.</li><li>Revisar regularmente.</li></ol>",
            "result": "A equipe 'Gama' estava há meses falhando em entregas. Preencheram o pilar de 'Transparência' e ficou claro: 'Não dizemos ao cliente quando vamos atrasar por medo do gestor'. Ao preencher 'Empatia', revelaram: 'O gestor nunca escuta nossas dores'. Com o canvas pronto, foi formalizado um novo contrato social: o gerente se comprometeu a abolir microgerenciamento diário em troca do time apresentar um relatório honesto e adiantado de riscos toda quarta-feira às 14h."
        },
        {
            "title": "Psychological Safety Assessment",
            "icon": "🩺",
            "detail": "Pesquisa ou dinâmica para medir e melhorar quão seguro o time se sente para assumir riscos sem punição.",
            "examples": "Avaliação periódica do clima do squad.",
            "execution": "<ol><li>Responder a questionários sobre conforto em discordar.</li><li>Realizar discussões anônimas de desafios.</li><li>Criar pactos de equipe para evitar culpas em erros.</li></ol>",
            "result": "A pesquisa trimestral anônima da diretoria mostrou que o squad 4 pontuou '2/10' na frase 'É seguro assumir um risco neste time'. Ao realizar uma sessão de facilitação, a Scrum Master descobriu que um desenvolvedor havia sido exposto publicamente pelo gerente no Slack após quebrar uma build. A ação foi direta: o gerente foi advertido pelo CTO, pediu desculpas formais e introduziram a regra da 'Retrospectiva sem Culpas' com focos em sistemas, e não pessoas."
        },
        {
            "title": "Core Protocols",
            "icon": "📜",
            "detail": "Conjunto de regras de comunicação para times colaborativos, como 'Passar', 'Check-in', e 'Decisão'.",
            "examples": "Eliminar ruídos e passivo-agressividade nas reuniões.",
            "execution": "<ol><li>Treinar o time nos protocolos básicos.</li><li>Implementar o 'Check-in' (como me sinto).</li><li>Permitir o uso da carta de 'Passar' se alguém não quer falar.</li></ol>",
            "result": "A reunião semanal de arquitetura costumava durar 3 horas com discussões circulares. Ao implementar o protocolo de 'Passar', o dev júnior 'Mateus' parou de se forçar a opinar sobre integrações ERP das quais não tinha contexto e usou o 'Passo'. Já com o uso da 'Decisão Rápida' (um polegar para cima/baixo), o time decidiu por AWS Lambda em vez de EC2 em 15 minutos, documentaram o alinhamento, e reduziram o tempo total da reunião para 45 minutos constantes."
        },
        {
            "title": "W3 (What, So What, Now What)",
            "icon": "🧐",
            "detail": "Modelo estruturado de reflexão (Estrutura Libertadora) após um incidente ou experimento.",
            "examples": "Debriefing após queda do sistema de produção.",
            "execution": "<ol><li>What: O que aconteceu (fatos).</li><li>So What: Qual o impacto ou significado disso.</li><li>Now What: Quais serão os próximos passos.</li></ol>",
            "result": "Após a queda do servidor na Black Friday. What: 'O banco atingiu 100% de CPU às 14h e travou'. So What: 'Perdemos cerca de R$ 50 mil em vendas potenciais e danificamos a imagem da marca'. Now What: 'Até amanhã, o DBA Roberto vai configurar réplicas de leitura para desafogar consultas pesadas, e a Dev Ana vai adicionar um limitador de requisições'. O time saiu focado e resolveu o problema sem o drama e busca de culpados que destruíam reuniões anteriores."
        },
        {
            "title": "TRIZ",
            "icon": "💥",
            "detail": "Abordagem inversa (Estrutura Libertadora) onde a equipe cria o pior cenário possível e depois descobre como impedi-lo.",
            "examples": "Aumentar a qualidade do código fonte.",
            "execution": "<ol><li>Como podemos fazer para o código ser impossível de manter?</li><li>Listar todas as más práticas reais.</li><li>Criar ações para evitar essas más práticas hoje.</li></ol>",
            "result": "Objetivo: Piorar a qualidade do produto. O time listou: 'Nunca testar, escrever código todo em um arquivo, ignorar warnings do compilador, usar variáveis como a, b, c'. Todos riram da tragédia. Na segunda etapa, notaram com horror que eles *estavam* ignorando os warnings do compilador atualmente. O CTO instaurou uma regra no SonarQube no dia seguinte proibindo merges com warnings ativos, aumentando a robustez estática do código de 72% para 95% em um mês."
        },
        {
            "title": "Open Space Technology",
            "icon": "🎪",
            "detail": "Formato de des-conferência onde a agenda é construída no momento pelos próprios participantes.",
            "examples": "Encontro anual de engenheiros de software de uma grande empresa.",
            "execution": "<ol><li>Apresentar o mercado das ideias.</li><li>Participantes propõem sessões e colam na grade horária.</li><li>A lei dos 2 pés garante que as pessoas circulem onde agregam mais.</li></ol>",
            "result": "No grande evento anual para 200 funcionários de TI, a diretoria propôs o tema 'Futuro do Trabalho'. Uma grid gigante em branco foi montada. O programador estagiário 'Luiz' colou um post-it: 'Como usar ChatGPT para programar sem vazar dados da empresa' às 10h na Sala B. A sessão dele lotou com 40 pessoas, incluindo diretores, e de lá saiu a primeira diretriz oficial e aprovada de uso de IA generativa da empresa, redigida por ele mesmo."
        },
        {
            "title": "World Cafe",
            "icon": "🌐",
            "detail": "Método para criar conversas significativas sobre grandes questões, movendo pessoas em formato de mesas de café.",
            "examples": "Debater a visão de longo prazo de uma diretoria.",
            "execution": "<ol><li>Dividir em pequenas mesas com perguntas centrais.</li><li>Após 20 minutos, todos trocam de mesa, menos um anfitrião.</li><li>Conectar ideias entre as rodadas.</li></ol>",
            "result": "Com mesas redondas cobertas de toalhas de papel sulfite, o departamento de RH discutiu 'Retenção de Talentos'. Em uma mesa, após 3 trocas de participantes, um padrão emergiu desenhado em canetinha verde: 'Não é o salário, é a falta de plano de carreira claro'. A CEO 'Flávia', lendo a inteligência coletiva nas toalhas ao final de 90 minutos, anunciou um projeto de 2 meses para criar e publicar a primeira 'Árvore de Carreiras e Competências' transparente e oficial."
        },
        {
            "title": "Shift & Share",
            "icon": "🔄",
            "detail": "Sessão dinâmica de pitchs ou inovações, onde pequenos grupos circulam por estações de apresentação.",
            "examples": "Feira de inovações internas (Work Expo).",
            "execution": "<ol><li>Apresentadores montam suas estações.</li><li>Grupos de espectadores visitam estações por 10 min cada.</li><li>Ouvem o pitch e dão feedback.</li></ol>",
            "result": "Em um grande salão, os 5 times do projeto 'Zênite' montaram estações. A cada toque do sino de 10 minutos, o time 'Alfa' via outras apresentações. Na estação do time 'Beta', Alfa descobriu que eles já haviam resolvido a falha de autenticação via OAuth com a qual o Alfa batia cabeça há 3 semanas. Copiaram o link do repositório ali mesmo e implementaram a solução de código naquela tarde, cortando semanas de R&D duplicado."
        },
        {
            "title": "Copilot (Pairing)",
            "icon": "✈️",
            "detail": "Prática de dupla onde duas pessoas trabalham juntas no mesmo problema em tempo real (Pair Programming ou Pair Work).",
            "examples": "Desenvolvimento de uma feature crítica com um júnior e um sênior.",
            "execution": "<ol><li>Definir papéis de Motorista e Navegador.</li><li>Trabalhar na tarefa por um tempo focado (ex: Pomodoro).</li><li>Trocar os papéis.</li></ol>",
            "result": "Na segunda-feira, a Tech Lead 'Carla' sentou-se fisicamente ao lado do júnior 'Miguel' para corrigir um vazamento de memória crítico no backend Node.js. Miguel digitava (Motorista) enquanto Carla orientava os conceitos de Garbage Collection (Navegador). Em 2 horas ininterruptas (usando 4 pomodoros de 25 min), o bug estava isolado, testado e publicado. Miguel adquiriu mais conhecimento real ali do que em seu curso de 20 horas online."
        },
        {
            "title": "Identity Symbols",
            "icon": "🛡️",
            "detail": "Criação de mascotes, nomes, logotipos ou gritos de guerra que formam uma identidade tribal forte.",
            "examples": "Um squad que escolhe o nome 'Thundercats' e cria adesivos próprios.",
            "execution": "<ol><li>Brainstorm de nomes ou conceitos que representam a missão do time.</li><li>Votação ou consenso da equipe.</li><li>Criar e divulgar ativos visuais (camisas, adesivos, slack emojis).</li></ol>",
            "result": "O squad encarregado da segurança dos dados escolheu o nome 'Cyber-Krakens'. Eles solicitaram R$ 500 do orçamento da gerência, criaram um logotipo de polvo tecnológico num escudo e encomendaram canecas roxas exclusivas e emojis animados no Teams. O resultado foi um orgulho imenso de grupo. Quando os desenvolvedores usavam a camisa roxa, membros de outros setores já sabiam quem abordar para tirar dúvidas de segurança."
        },
        {
            "title": "OKRs (Objectives and Key Results)",
            "icon": "🎯",
            "detail": "Framework colaborativo de metas para alinhar objetivos estratégicos em nível macro e micro com métricas-chave.",
            "examples": "Definir metas trimestrais da equipe de produto com visibilidade para todos.",
            "execution": "<ol><li>Definir 1 ou 2 Objetivos inspiradores (O quê).</li><li>Definir 3-5 Resultados-Chave mensuráveis (Como saberemos se chegamos).</li><li>Alinhar entre times para evitar silos.</li></ol>",
            "result": "O objetivo de Q3 era 'Tornar a plataforma irresistível', e o Key Result 1 era 'Reduzir churn mensal de 5% para 2%'. A gestora 'Lúcia' deixou de lado as 20 features prometidas em backlog e o time de produto focou 100% apenas em consertar o onboarding e criar gatilhos de engajamento, que era o maior motivo de cancelamento. No final do trimestre, o churn fechou em 1.8%, e o time ganhou bônus integral pelo foco cirúrgico nos resultados-chave."
        },
        {
            "title": "Kudos Wall",
            "icon": "🧱",
            "detail": "Mural físico ou virtual altamente visível onde todos os reconhecimentos públicos (Kudos) ficam expostos.",
            "examples": "Um quadro físico na copa da empresa ou canal no Slack focado em gratidão.",
            "execution": "<ol><li>Escolher o canal mais visível (físico ou virtual).</li><li>Disponibilizar material fácil (post-its ou integração slack).</li><li>Comemorar mensalmente a quantidade de Kudos gerados.</li></ol>",
            "result": "No saguão da startup, montaram uma parede inteira de cortiça com a placa gigante 'Gratidão'. Na sexta-feira da entrega crítica, a muralha tinha mais de 60 post-its coloridos. Um deles, rosa choque, dizia: 'Ao time de devOps (Beto, Ana e Gui) por manterem a calma sob fogo cruzado na quarta de madrugada. Ass: CEO Marcos'. Visitantes e investidores viam o mural assim que entravam, e a cultura de valorização se tornou o principal atrativo de contratação."
        },
        {
            "title": "Agility Health Radar",
            "icon": "📡",
            "detail": "Métrica visual e colaborativa onde a equipe autoavalia suas competências, práticas e desempenho ao longo de um eixo.",
            "examples": "Avaliar a maturidade ágil (Scrum/Kanban) do squad após 6 meses.",
            "execution": "<ol><li>Escolher as dimensões (Qualidade, Desempenho, Engenharia, Liderança).</li><li>Cada membro avalia o time nas dimensões de 1 a 5.</li><li>Conectar os pontos para criar um 'Radar' e gerar plano de ação nas áreas baixas.</li></ol>",
            "result": "No final do semestre, o squad preencheu a roda de competências. A linha de 'Processos Ágeis' estava na ponta do radar (nota 5), mas a dimensão 'Qualidade Técnica' afundou para nota 1. Visualizando esse desequilíbrio alarmante, o gerente 'Felipe' pausou a cobrança de novas métricas de velocity e investiu duas sprints inteiras apenas para pagar dívida técnica de código e instalar integração contínua e testes automatizados, elevando a nota técnica para 3 no trimestre seguinte."
        },
        {
            "title": "Problem Management",
            "icon": "🛠️",
            "detail": "Processo contínuo de analisar causa raiz e evitar que problemas do dia a dia virem crises constantes.",
            "examples": "Evitar que um pequeno bug de pagamento retorne na próxima release.",
            "execution": "<ol><li>Identificar problemas recorrentes.</li><li>Analisar a causa raiz (ex: 5 Porquês).</li><li>Transformar a solução em itens de backlog (ações preventivas).</li></ol>",
            "result": "Todo mês, o sistema da loja travava os pedidos via PIX por 20 minutos (causa desconhecida). Após aplicarem a técnica de Problem Management e os 5 Porquês, o dev Sênior 'Tiago' descobriu a causa raiz: um cronjob noturno do financeiro travava a tabela temporariamente. O cronjob foi reprogramado para uma fila assíncrona isolada. O ticket que era aberto 15 vezes por mês pela central de atendimento desapareceu para sempre, poupando R$ 8.000 mensais em horas-extras de suporte técnico."
        },
        {
            "title": "Metrics Ecosystem",
            "icon": "🌱",
            "detail": "Conjunto de métricas equilibradas que se contra-balanceiam para evitar otimizações locais e comportamentos destrutivos.",
            "examples": "Equilibrar Velocidade (Lead Time) com Qualidade (Defect Rate).",
            "execution": "<ol><li>Mapear as métricas atuais.</li><li>Encontrar o contrapeso de cada uma.</li><li>Criar um dashboard para observar o ecossistema holístico.</li></ol>",
            "result": "O diretor 'Arthur' comemorou que o 'Tempo de Entrega' (Lead Time) caiu de 14 para 5 dias. Mas o dashboard do Ecossistema mostrou a métrica de contrapeso piscando em vermelho: a 'Taxa de Falha em Produção' (CFR) tinha saltado de 2% para 18%. O time estava correndo às pressas e quebrando tudo. A liderança corrigiu o curso implementando gates de qualidade obrigatórios, equilibrando a balança: o tempo subiu para 7 dias, mas a taxa de falha desabou de volta a zero."
        },
        {
            "title": "Borda Count",
            "icon": "🔢",
            "detail": "Técnica de votação ponderada em que os votantes classificam opções em ordem de preferência para evitar polarização.",
            "examples": "Selecionar os três principais tópicos para a próxima sprint.",
            "execution": "<ol><li>Listar opções.</li><li>Cada eleitor atribui pesos decrescentes (ex: 3 pts para o 1º, 2 pts para o 2º, 1 pt para o 3º).</li><li>Somar todos os pontos.</li></ol>",
            "result": "O time de design precisava escolher o tema visual do novo software entre: Tema Escuro, Tema Claro ou Tema Colorido. Usando os pontos de Borda, o designer 'Luiz' deu 3 pts ao Colorido, 2 ao Escuro, 1 ao Claro. No total consolidado das 10 pessoas, o Tema Escuro venceu com 24 pontos, mesmo que a maioria inicialmente gritasse a favor do Colorido, porque o Escuro se mostrou sistematicamente a segunda opção forte de todo mundo. Não houve ressentimentos e o projeto avançou em 10 minutos."
        },
        {
            "title": "Roles & Responsibilities Matrix",
            "icon": "⚙️",
            "detail": "Adaptação do RACI para a realidade ágil, desenhada de forma colaborativa para alinhar expectativas no time.",
            "examples": "Acabar com o conflito entre o PO e o Scrum Master sobre quem lidera o Refinamento.",
            "execution": "<ol><li>Listar as atividades do squad.</li><li>Os envolvidos colocam suas iniciais no que acham que devem fazer.</li><li>Debater as áreas de sobreposição e as áreas sem responsável.</li></ol>",
            "result": "O analista de QA 'Breno' e o Desenvolvedor 'Davi' brigavam constantemente sobre quem atualizava o card no Jira. Na lousa da matriz RACI simplificada, preencheram as iniciais na tarefa 'Mover card para DONE'. Concordaram que 'Davi' é o Responsável (R) por atualizar, e 'Breno' apenas é Informado (I) via automação de email. A briga terminou no mesmo dia, e Breno passou a usar o tempo livre ganho para escrever mais cenários de teste automatizado."
        },
        {
            "title": "Skill Matrix",
            "icon": "🗂️",
            "detail": "Mapa de habilidades (hard skills) da equipe cruzando os membros do time vs tecnologias necessárias.",
            "examples": "Descobrir que apenas uma pessoa sabe gerenciar o banco de dados legado.",
            "execution": "<ol><li>Listar todas as tecnologias/sistemas no eixo X.</li><li>Membros do time no eixo Y.</li><li>Preencher: Não sabe (0), Sabe o básico (1), Independente (2), Pode ensinar (3).</li></ol>",
            "result": "A tabela na parede mapeava as linguagens no eixo X e os nomes no eixo Y. Na intersecção 'Banco de Dados Oracle', havia apenas zeros, exceto por 'Seu Carlos', que tinha o nível máximo 3 (Pode ensinar). A liderança percebeu que se Carlos ficasse doente, a empresa inteira pararia. Um plano de cross-training foi instaurado: toda terça de manhã, Carlos passou a ministrar aulas práticas de 2h para 'Bianca' e 'Rafa', que subiram para nível 2 em dois meses, eliminando o ponto único de falha."
        },
        {
            "title": "Value Stream Mapping",
            "icon": "🌊",
            "detail": "Técnica lean para visualizar todos os passos entre a ideia e a entrega para o cliente, focando em remover desperdícios.",
            "examples": "Otimizar o processo de aprovação de código que demora dias.",
            "execution": "<ol><li>Mapear estado atual com todas as etapas.</li><li>Identificar tempo de valor agregado e tempo de espera.</li><li>Projetar um fluxo ideal e cortar os gargalos principais.</li></ol>",
            "result": "O mapeamento visual do post-it desde 'Ideia do Cliente' até 'Deploy' chocou a diretoria: de um Lead Time total de 45 dias, apenas 4 dias eram de codificação real (valor agregado); 41 dias eram de esperas em filas de aprovação de comitês de governança. A CEO aprovou uma política de 'Fast Track' para mudanças não críticas. Na medição seguinte, três semanas depois, as entregas menores passaram a levar apenas 5 dias no total, surpreendendo os clientes com a velocidade."
        },
        {
            "title": "Work Expo",
            "icon": "🖼️",
            "detail": "Feira interna onde equipes exibem publicamente o que produziram para aumentar a transparência organizacional e celebrar sucesso.",
            "examples": "Evento semestral onde cada squad mostra os produtos que lançou.",
            "execution": "<ol><li>Cada time monta um estande ou sala de exibição.</li><li>Executivos e colegas passeiam pelas exibições experimentando as novidades.</li><li>Premiar as melhores exibições.</li></ol>",
            "result": "Em um grande galpão alugado, 12 squads montaram estandes físicos com monitores, adesivos e brindes, apresentando as inovações tecnológicas desenvolvidas no ano. O squad 'Zeus', conhecido por ser silencioso, apresentou um motor de recomendação revolucionário que eles criaram e ninguém da empresa sabia que existia. Executivos de vendas que passeavam pelo evento conectaram o motor com um grande cliente na hora, fechando um contrato milionário na semana seguinte derivado unicamente dessa demonstração."
        }
    ],
    "Facilitação Remota": [
        {
            "title": "Brainstorming Silencioso (Silent Brainstorming)",
            "icon": "🤫",
            "detail": "Permite que todos os participantes adicionem ideias em um quadro virtual (ex: Miro) silenciosamente antes de qualquer discussão.",
            "examples": "Início de sessões de ideação para evitar viés de autoridade (efeito HIPPO) e encorajar introvertidos.",
            "execution": "<ol><li>Apresentar o problema.</li><li>Definir timer de 5 min.</li><li>Participantes escrevem post-its em silêncio.</li><li>Agrupar ideias por afinidade.</li></ol>",
            "result": "No quadro Miro gerado pela Tech Lead Ana, a equipe coletou 45 post-its em 5 minutos. O desenvolvedor júnior Carlos enviou 12 sugestões de performance, sendo uma escolhida como arquitetura final."
        },
        {
            "title": "Check-in Assíncrono",
            "icon": "⏳",
            "detail": "Atualizações de status ou alinhamentos diários feitos via texto ou vídeo curto em canais dedicados, sem necessidade de reunião.",
            "examples": "Equipes distribuídas em diferentes fusos horários (ex: Brasil e Europa) atualizando o progresso diário.",
            "execution": "<ol><li>Configurar lembrete no Slack/Teams.</li><li>Definir 3 perguntas curtas.</li><li>Cada membro responde na thread até um horário limite.</li></ol>",
            "result": "Em vez de uma daily às 9h, o dev Sênior Roberto postou no Slack às 08:30: 'Ontem: PR #42. Hoje: Bug ticket-99. Bloqueio: Nenhum'. Isso economizou 25 minutos diários para 6 pessoas distribuídas entre SP e Berlim."
        },
        {
            "title": "Votação por Pontos (Dot Voting) Digital",
            "icon": "🔴",
            "detail": "Técnica rápida para convergir e priorizar ideias usando recursos de votação nativos de ferramentas de whiteboarding.",
            "examples": "Priorizar quais das 20 ideias geradas no brainstorming serão exploradas na próxima etapa do projeto.",
            "execution": "<ol><li>Ativar ferramenta de votação.</li><li>Alocar 3-5 votos por pessoa.</li><li>Votação silenciosa (anônima se possível).</li><li>Revelar e discutir os mais votados.</li></ol>",
            "result": "Usando 3 'dots' vermelhos por pessoa no FigJam, o time de 10 pessoas priorizou o backlog visualmente. A ideia 'Refatorar Checkout' recebeu 14 votos da equipe, decidindo o escopo do Épico Q3."
        },
        {
            "title": "Salas Simultâneas (Breakout Rooms)",
            "icon": "🚪",
            "detail": "Divisão de grandes grupos em pequenos subgrupos de 3-5 pessoas em chamadas de vídeo para discussões mais profundas.",
            "examples": "Dinâmicas de problem-solving onde um grupo de 20 pessoas não conseguiria interagir eficientemente.",
            "execution": "<ol><li>Explicar a tarefa e tempo para o grande grupo.</li><li>Dividir aleatoriamente ou em grupos pré-definidos.</li><li>Facilitador visita as salas.</li><li>Retornar e compartilhar no grupo maior.</li></ol>",
            "result": "O Agile Coach dividiu as 30 pessoas do evento em 6 salas do Zoom. Na Sala 3, Marina, João e Felipe discutiram por 10 minutos e voltaram com um protótipo de tela desenhado no papel."
        },
        {
            "title": "Lean Coffee Assíncrono",
            "icon": "☕",
            "detail": "Variação do Lean Coffee onde a coleta de tópicos e votação ocorrem assincronamente antes da reunião ao vivo.",
            "examples": "Reuniões de Comunidade de Prática (CoP) onde o tempo síncrono é curto e deve ser focado na discussão.",
            "execution": "<ol><li>Disponibilizar board de tópicos 2 dias antes.</li><li>Participantes adicionam e votam em tópicos.</li><li>Iniciar a chamada com os tópicos já priorizados.</li></ol>",
            "result": "Na Comunidade de Prática de QA, 8 tópicos foram adicionados no board EasyRetro. Na quinta, o tópico 'Testes E2E com Cypress' do Lucas já tinha 15 votos, focando totalmente a discussão."
        },
        {
            "title": "Caminhada pelo Mural (Mural/Miro Walk)",
            "icon": "🚶",
            "detail": "Passeio guiado e assíncrono por um board, utilizando comentários, links ou vídeos gravados (Loom) para explicar o conteúdo.",
            "examples": "Apresentação de uma nova arquitetura ou fluxo de usuário para stakeholders revisarem no seu próprio tempo.",
            "execution": "<ol><li>Estruturar o board de forma sequencial.</li><li>Gravar um vídeo de 5 min navegando pelo board.</li><li>Compartilhar o link pedindo comentários assíncronos.</li></ol>",
            "result": "A designer Clara enviou um vídeo no Loom de 6 min navegando pelo protótipo no Miro. O PO Fernando assistiu às 22h e deixou 3 comentários em post-its azuis, poupando uma call de 1h."
        },
        {
            "title": "Retrospectiva Assíncrona",
            "icon": "⏪",
            "detail": "Coleta de feedbacks e pontos de melhoria da sprint de forma assíncrona ao longo dos dias, culminando em uma rápida análise síncrona.",
            "examples": "Times maduros que desejam reduzir o tempo das cerimônias do Scrum.",
            "execution": "<ol><li>Manter um board aberto durante toda a sprint.</li><li>Equipe adiciona pontos (bom/ruim) em tempo real.</li><li>Na reunião, focar apenas na criação de planos de ação.</li></ol>",
            "result": "Ao final da sprint, o board tinha 5 cartões verdes ('Deploy sem erros') e 2 vermelhos ('Falta documentação') adicionados ao vivo. A reunião focou na action item: 'Paulo documentará a API na Sprint 8'."
        },
        {
            "title": "Escrita Cerebral (Brainwriting) em Planilha",
            "icon": "📝",
            "detail": "Evolução sequencial de ideias: um participante escreve uma ideia e o próximo a lê e a expande, feito via Google Sheets ou Excel Online.",
            "examples": "Resolução de problemas complexos que exigem pensamento aprofundado e iterativo.",
            "execution": "<ol><li>Criar planilha com nome dos participantes nas colunas.</li><li>Anotar ideia inicial na linha 1.</li><li>A cada 3 min, rotacionar para a coluna do colega e expandir a ideia dele.</li></ol>",
            "result": "No Google Sheets, Maria escreveu 'Cache no Redis'. Após 2 rotações da planilha, Thiago adicionou 'TTL de 5 min' e Juliana 'Apenas consultas de catálogo', criando uma solução robusta em 15 minutos."
        },
        {
            "title": "Icebreaker Visual",
            "icon": "🖼️",
            "detail": "Dinâmica de quebra-gelo inicial onde participantes colam imagens ou gifs em um board que representam seu estado de espírito.",
            "examples": "Abertura de workshops remotos para criar conexão emocional imediata.",
            "execution": "<ol><li>Criar uma área no board com o nome de cada um.</li><li>Pedir que busquem uma imagem no Google/Giphy que represente sua semana.</li><li>Cada um explica rapidamente em 30 segundos.</li></ol>",
            "result": "12 fotos coladas no Miro. O CTO Ricardo colocou um GIF de um gato digitando rápido, arrancando risadas. O clima ficou leve e todos participaram ativamente das dinâmicas."
        },
        {
            "title": "Sinalização de Mão Virtual (Thumb Voting)",
            "icon": "👍",
            "detail": "Uso de gestos rápidos na câmera (ou reações de emoji) para validar consenso imediato e medir a temperatura da sala.",
            "examples": "Decidir rapidamente se a equipe está pronta para avançar para o próximo tópico da agenda.",
            "execution": "<ol><li>Fazer a pergunta clara.</li><li>Pedir votação: polegar para cima (sim), meio (dúvida), baixo (não).</li><li>Analisar o visual da galeria de vídeos.</li></ol>",
            "result": "Quando o Scrum Master perguntou 'Podemos fechar o escopo da sprint?', 5 pessoas levantaram o polegar na câmera e 1 no meio. A dúvida de Marcos foi resolvida em 2 minutos."
        },
        {
            "title": "Aquário Virtual (Virtual Fishbowl)",
            "icon": "🐠",
            "detail": "Formato de discussão onde apenas um pequeno grupo fala (com câmera/mic ligados), enquanto o resto assiste (câmera/mic desligados). Participantes podem 'entrar no aquário' para falar.",
            "examples": "Debates envolvendo dezenas de pessoas, como em All-Hands ou Town Halls.",
            "execution": "<ol><li>Definir 4 pessoas no 'aquário' (câmera ligada).</li><li>Resto do grupo desliga a câmera.</li><li>Quando alguém de fora quiser falar, liga a câmera. Alguém do aquário deve sair (desligar).</li></ol>",
            "result": "No Town Hall, a dev Sarah quis falar sobre a nova política. Ela ligou a câmera, o CTO desligou a dele, e ela expôs seu ponto tranquilamente para 200 pessoas assistindo."
        },
        {
            "title": "Perguntas e Respostas Anônimas",
            "icon": "🕵️",
            "detail": "Uso de ferramentas como Slido ou Mentimeter para coletar perguntas de forma anônima antes ou durante uma sessão.",
            "examples": "Reuniões de resultados da empresa onde funcionários podem ter receio de fazer perguntas difíceis à liderança.",
            "execution": "<ol><li>Compartilhar link do Slido com a equipe.</li><li>Permitir envio e votação de perguntas de forma anônima.</li><li>Facilitador lê as perguntas mais votadas ao vivo.</li></ol>",
            "result": "No Slido, a pergunta 'Haverá cortes de equipe no Q4?' recebeu 45 upvotes. A diretora de RH, Laura, respondeu ao vivo garantindo que não, eliminando o estresse dos 150 colaboradores."
        },
        {
            "title": "Pomodoro Coletivo (Working Session)",
            "icon": "🍅",
            "detail": "Sessão de trabalho focada em grupo usando chamadas de áudio/vídeo silenciadas, alternando períodos de foco e pausas.",
            "examples": "Sprints de documentação ou mutirão de resolução de bugs.",
            "execution": "<ol><li>Entrar na chamada e declarar o objetivo individual no chat.</li><li>Iniciar timer de 25 min em silêncio.</li><li>Fazer pausa de 5 min conversando.</li><li>Repetir o ciclo.</li></ol>",
            "result": "Em uma call silenciada no Discord, a dupla Amanda e Diego conseguiu reduzir o technical debt do microserviço de pagamentos de 40 para 12 bugs críticos após 4 ciclos Pomodoro."
        },
        {
            "title": "Mapa de Empatia Assíncrono",
            "icon": "🧠",
            "detail": "Construção de perfis de usuário de forma colaborativa e distribuída no tempo usando quadros virtuais estruturados.",
            "examples": "Fase de discovery de um produto onde pesquisadores preenchem dados à medida que finalizam entrevistas.",
            "execution": "<ol><li>Criar template do mapa de empatia.</li><li>Compartilhar com a equipe de pesquisa.</li><li>Membros adicionam insights assincronamente ao longo da semana.</li></ol>",
            "result": "O quadrante 'Dores' no Miro acumulou 18 quotes reais, como 'O botão sumiu' (dita por Joana, cliente #1092), criando uma Persona hiper-realista sem uma reunião exaustiva de 4 horas."
        },
        {
            "title": "Feedback 360 com Formulário Contínuo",
            "icon": "🔄",
            "detail": "Manter um canal ou formulário sempre aberto para que membros do time enviem feedbacks positivos ou construtivos a qualquer momento.",
            "examples": "Incentivar a cultura de feedback contínuo em equipes ágeis, fugindo das avaliações anuais.",
            "execution": "<ol><li>Criar um Typeform ou Google Form estruturado.</li><li>Deixar o link acessível na descrição do canal do time.</li><li>Encaminhar respostas automaticamente via integração.</li></ol>",
            "result": "O bot do Slack enviou: 'Novo feedback para Guilherme! Contexto: Ajudou a debugar o erro 500 no checkout. Impacto: Acelerou a entrega em 2 dias.' - isso logo após o deploy."
        },
        {
            "title": "Delegação Poker Digital",
            "icon": "🃏",
            "detail": "Uso de cartas virtuais para alinhar níveis de delegação e autonomia entre líderes e equipes em diferentes tarefas.",
            "examples": "Onboarding de um novo Tech Lead que precisa definir limites de autonomia com a equipe.",
            "execution": "<ol><li>Listar as decisões chave (ex: escolher stack técnica).</li><li>Usar app web de Delegation Poker.</li><li>Líder e equipe votam simultaneamente no nível (1 a 7).</li><li>Discutir divergências.</li></ol>",
            "result": "O novo Tech Lead Sérgio e seus 5 devs votaram 'Consultar (Nível 3)' para decisões de stack. Ficou documentado no Notion que Sérgio decidirá, mas sempre consultará o time antes."
        },
        {
            "title": "Diário de Bordo (Logbook) Compartilhado",
            "icon": "📓",
            "detail": "Documento centralizado e cronológico (ex: Notion, Confluence) onde a equipe registra decisões chave, vitórias e aprendizados diariamente.",
            "examples": "Manter histórico de contexto para times distribuídos que não têm conversas informais de corredor.",
            "execution": "<ol><li>Criar página no Notion com template diário.</li><li>Rodízio do papel de 'escrivão' da equipe.</li><li>Documentar fatos relevantes e links do dia.</li></ol>",
            "result": "Na página 'Diário' no Notion, a estagiária Bia escreveu: 'Decidimos usar GraphQL em vez de REST'. Três meses depois, o dev Sênior Igor leu isso para entender o contexto antes de implementar a feature."
        },
        {
            "title": "Estacionamento (Parking Lot) Virtual",
            "icon": "🅿️",
            "detail": "Espaço designado no board ou chat para anotar assuntos importantes que surgem, mas estão fora do escopo da reunião atual.",
            "examples": "Evitar que uma reunião de planejamento se desvie para uma discussão arquitetônica profunda.",
            "execution": "<ol><li>Criar área visual de 'Estacionamento'.</li><li>Quando um tópico tangente surgir, movê-lo para lá.</li><li>No fim da reunião, decidir quem e quando abordará os tópicos estacionados.</li></ol>",
            "result": "A discussão derivou para microfrontends. O facilitador Tiago moveu a ideia para o quadro 'Estacionamento'. A Planning terminou no horário, e a arquitetura virou uma agenda de sexta-feira."
        },
        {
            "title": "Votação de Confiança (Fist of Five)",
            "icon": "🖐️",
            "detail": "Mecanismo rápido no chat para medir o grau de confiança da equipe em cumprir o objetivo da sprint ou aceitar um acordo.",
            "examples": "Final do Sprint Planning para confirmar se todos sentem que a meta é realista.",
            "execution": "<ol><li>Facilitador pede a votação no chat do Teams/Zoom.</li><li>Membros digitam um número de 1 a 5.</li><li>Focar a discussão apenas em quem votou 1, 2 ou 3.</li></ol>",
            "result": "Sobre entregar 40 story points, as respostas no chat foram: 5, 4, 4, 2, 4. O voto '2' foi do QA Leandro lembrando do feriado. A meta foi reajustada para 32 pontos na hora."
        },
        {
            "title": "Design Sprint Remoto em Dias Fatiados",
            "icon": "🎨",
            "detail": "Adaptação do modelo de 5 dias do Google Design Sprint para sessões curtas de 3 horas durante duas semanas, misturando trabalho síncrono e assíncrono.",
            "examples": "Equipes com agendas muito cheias que não podem bloquear uma semana inteira, mas precisam inovar.",
            "execution": "<ol><li>Dividir as etapas clássicas em blocos menores.</li><li>Usar trabalho assíncrono para pesquisa e esboço.</li><li>Encontros síncronos curtos apenas para decisão e alinhamento.</li></ol>",
            "result": "Em blocos de 3h, o time desenhou protótipos na terça e entrevistou 5 usuários na quinta. 4 deles confirmaram que o botão 'Comprar com 1 clique' era a solução, sem bloquear a semana toda."
        },
        {
            "title": "Rotação de Papéis na Facilitação",
            "icon": "🎭",
            "detail": "Transferir a responsabilidade de facilitar cerimônias remotas periodicamente entre todos os membros da equipe.",
            "examples": "Evitar que o Scrum Master ou Agile Coach seja o ponto único de falha e dono exclusivo do engajamento.",
            "execution": "<ol><li>Criar escala visível de facilitação.</li><li>Facilitador atual treina o próximo.</li><li>Cada um pode trazer seu toque pessoal e novas dinâmicas.</li></ol>",
            "result": "A Dev Júnior Camila guiou a Retrospectiva usando um template de 'Star Wars'. A equipe se engajou o dobro, e Camila saiu confiante para liderar reuniões de refinamento técnico."
        },
        {
            "title": "Mapeamento de Fluxo de Valor (VSM) Digital",
            "icon": "📈",
            "detail": "Construção de mapas complexos de fluxo de processo de forma colaborativa em infinitos canvas digitais.",
            "examples": "Identificar gargalos no pipeline de deploy de software de uma equipe global.",
            "execution": "<ol><li>Preparar componentes visuais (caixas, setas) no board.</li><li>Dividir o time em subgrupos para mapear diferentes partes do fluxo.</li><li>Juntar as partes e identificar gargalos (lead time vs process time).</li></ol>",
            "result": "No Miro, o time descobriu que a 'Aprovação Manual de QA' levava 48 horas de espera, mas o teste real durava 30 min. Automatizar isso virou prioridade do trimestre."
        },
        {
            "title": "Kudos Board Permanente",
            "icon": "🏆",
            "detail": "Um quadro virtual ou canal específico para reconhecimento contínuo e público entre pares.",
            "examples": "Manter a motivação e cultura de reconhecimento ativa em tempos de isolamento remoto.",
            "execution": "<ol><li>Criar canal #kudos ou usar app como HeyTaco.</li><li>Incentivar liderança a dar o exemplo.</li><li>Ler alguns reconhecimentos na reunião de fechamento da semana.</li></ol>",
            "result": "No #kudos, o bot registrou: '@Fernanda mandou 🌮 para @Thiago por salvar a migração'. No final do mês, Thiago tinha 15 tacos e ganhou um vale-iFood, mantendo o moral em alta."
        },
        {
            "title": "Apresentação com Bastão da Fala (Talking Stick)",
            "icon": "🪄",
            "detail": "Uso da função de 'levantar a mão' ou um objeto virtual rotativo para garantir que apenas uma pessoa fale e todos sejam ouvidos sem interrupções.",
            "examples": "Debates acalorados sobre arquitetura onde as pessoas tendem a falar umas por cima das outras pelo delay de áudio.",
            "execution": "<ol><li>Estabelecer a regra do bastão no início.</li><li>Quem está falando escolhe o próximo chamando o nome.</li><li>O próximo liga o microfone e assume.</li></ol>",
            "result": "Durante o debate de Kafka vs RabbitMQ, quando a dev Roberta falava, os 8 participantes mantinham-se em silêncio por regra do 'bastão virtual', eliminando interrupções bruscas por delay."
        },
        {
            "title": "Sessão de Descompressão Virtual (Watercooler)",
            "icon": "🌊",
            "detail": "Eventos de agenda curtos e opcionais, puramente sociais, com uso de jogos online simples (ex: Gartic, Skribbl, Codenames).",
            "examples": "Sextas-feiras à tarde para criar laços entre novos membros e veteranos do time.",
            "execution": "<ol><li>Bloquear 30 min na agenda semanal (opcional).</li><li>Escolher um jogo colaborativo de browser.</li><li>Não falar de trabalho durante a sessão.</li></ol>",
            "result": "Na sexta, 7 pessoas jogaram Gartic. O CTO desenhou uma 'Capivara' terrível e todos riram por 30 minutos. O time saiu revigorado e o novato Léo se enturmou de vez."
        },
        {
            "title": "Retrospectiva do Barco à Vela (Sailboat) no FigJam",
            "icon": "⛵",
            "detail": "Dinâmica metafórica usando um barco, âncoras (impedimentos), ventos (impulsionadores) e pedras (riscos) mapeados visualmente.",
            "examples": "Avaliar o andamento de um projeto de médio prazo, identificando rapidamente o que está atrasando o time.",
            "execution": "<ol><li>Colar a imagem do barco no centro do board.</li><li>Membros adicionam post-its assincronamente (10 min).</li><li>Agrupar problemas (âncoras) e definir donos para remover os obstáculos.</li></ol>",
            "result": "No FigJam, o 'Débito Técnico' entrou como âncora pesando 40% do tempo. A action item da sprint 12 foi alocar 2 devs exclusivamente para remover a âncora do legado de login."
        },
        {
            "title": "Revisão de Sprint em Vídeo (Demo Async)",
            "icon": "🎬",
            "detail": "Gravação de demonstrações de software funcionais pelos desenvolvedores e envio para os stakeholders antes da sessão de Q&A.",
            "examples": "Stakeholders muito ocupados que não conseguem participar das cerimonias de fim de sprint padrão.",
            "execution": "<ol><li>Dev grava um Loom de 3-5 minutos mostrando a feature.</li><li>Adiciona no card do Jira/Trello e envia no canal.</li><li>Stakeholders assistem e comentam assincronamente.</li></ol>",
            "result": "Lucas gravou um vídeo de 4 min do novo endpoint de relatórios. A PO Sofia assistiu do aeroporto pelo celular, aprovou com um 👍 no Slack, e o deploy rolou 3 dias antes da reunião oficial."
        },
        {
            "title": "Matriz Eisenhower Digital (Urgente x Importante)",
            "icon": "⚖️",
            "detail": "Facilitação visual para priorizar o backlog ou atividades diárias arrastando itens em um grid de 4 quadrantes.",
            "examples": "Time de suporte sobrecarregado com muitos incidentes e melhorias técnicas no backlog.",
            "execution": "<ol><li>Desenhar os 4 quadrantes no board.</li><li>Importar as tarefas (cards).</li><li>A equipe debate rapidamente e posiciona cada card no seu quadrante adequado.</li></ol>",
            "result": "O card 'Atualizar React' foi para 'Urgente e Importante'. 'Refatorar CSS antigo' foi para 'Importante, não urgente', despoluindo a fila imediata de trabalho dos 6 devs."
        },
        {
            "title": "Pair Programming Remoto (Ping Pong)",
            "icon": "💻",
            "detail": "Técnica de programação em pares focada em TDD via ferramentas como VS Code Live Share ou Tuple.",
            "examples": "Treinamento de desenvolvedores júniores ou resolução de um bug complexo no código legado.",
            "execution": "<ol><li>Iniciar sessão de Live Share com chamada de áudio.</li><li>Dev A escreve o teste que falha.</li><li>Dev B escreve o código que passa e o próximo teste que falha.</li></ol>",
            "result": "Aline (MG) escreveu o teste de retorno 404, e falhou. Bruno (SC) assumiu o controle, implementou a resposta 404, e comitou o código em 12 minutos de sessão Live Share perfeitamente alinhada."
        },
        {
            "title": "Sessão de Resolução de Problemas (5 Porquês)",
            "icon": "❓",
            "detail": "Dinâmica estruturada para encontrar a causa raiz de um incidente remoto investigando através de cinco camadas de 'por que'.",
            "examples": "Investigação pós-incidente (Post-mortem) de uma queda de servidor na madrugada.",
            "execution": "<ol><li>Escrever o problema principal no topo do board.</li><li>Perguntar o motivo e documentar abaixo (1º porquê).</li><li>Repetir o processo até chegar na raiz do processo ou sistema.</li></ol>",
            "result": "Após a queda às 02:00, o board apontou: 1. Caiu? Memória estourou. 2. Por que? Loop na fatura. (...) 5. Por que? Falta timeout na API terceira. Solução: circuit breaker implementado."
        },
        {
            "title": "Onboarding em Trilha Assíncrona",
            "icon": "🚀",
            "detail": "Transformação do processo de integração de novos membros em um 'jogo' de tarefas e leituras em ferramentas como Trello ou Notion.",
            "examples": "Integrar novas contratações quando o restante da equipe está focada em entregas críticas.",
            "execution": "<ol><li>Criar um board de Onboarding com colunas (Dia 1, Semana 1, etc).</li><li>Incluir links de vídeos, documentação e pequenas tarefas.</li><li>Atribuir um 'Buddy' para dúvidas esporádicas.</li></ol>",
            "result": "O dev recém-chegado Davi acessou o Trello, arrastou 'Configurar Ambiente' para 'Feito', viu 3 vídeos, e no final do dia 2 fez seu primeiro commit no repo principal sem bloquear a Tech Lead."
        },
        {
            "title": "Construção de Acordos de Trabalho (Working Agreements)",
            "icon": "🤝",
            "detail": "Sessão de cocriação das 'regras do jogo' da equipe, documentando horários, tempo de resposta e comportamentos esperados no formato remoto.",
            "examples": "Formação inicial de um squad ou restruturação de uma equipe disfuncional.",
            "execution": "<ol><li>Propor tópicos (Comunicação, Reuniões, Foco).</li><li>Brainstorming de sugestões de regras.</li><li>Votação para aprovação das regras.</li><li>Publicar as regras na wiki da equipe.</li></ol>",
            "result": "O squad Delta firmou e assinou no Miro: '1. Sem reuniões nas quartas; 2. Responder Slack em até 4h; 3. Câmera opcional'. O número de interrupções diárias despencou 60%."
        },
        {
            "title": "Troca de Conhecimento Rápida (Lightning Talks)",
            "icon": "⚡",
            "detail": "Apresentações curtas de 5 a 10 minutos feitas pela própria equipe sobre qualquer tópico (técnico ou não) durante encontros remotos.",
            "examples": "Promover inovação e compartilhamento do que os devs estão estudando por fora.",
            "execution": "<ol><li>Manter uma lista de interessados em apresentar.</li><li>Reservar os últimos 15 min da reunião de equipe de sexta-feira.</li><li>O apresentador compartilha a tela e ensina o tópico.</li></ol>",
            "result": "O QA Gabriel ensinou 'Regex' em 10 minutos na sexta. Na segunda, o front-end Bruno aplicou a técnica para validar e-mails em um formulário, sem depender mais do backend."
        },
        {
            "title": "Mapa de Calor de Riscos (Risk Heatmap)",
            "icon": "🔥",
            "detail": "Avaliação de riscos de projeto mapeando impacto versus probabilidade em um gráfico visual colaborativo.",
            "examples": "Início de um grande projeto de migração de nuvem com muitas incertezas e dependências.",
            "execution": "<ol><li>Time lista os riscos em post-its.</li><li>Desenhar eixo X (Probabilidade) e Y (Impacto).</li><li>Mover cada post-it para sua zona de calor correspondente (verde, amarelo, vermelho).</li></ol>",
            "result": "No quadrante vermelho escuro estava 'A API de parceiros pode atrasar'. Como mitigação aprovada, a gerente de projeto já alocou um dev para criar mocks dessa API na Sprint 1."
        },
        {
            "title": "Trabalho em Pares Assíncrono (PR Reviews profundos)",
            "icon": "👀",
            "detail": "Estruturação rigorosa de revisões de código (Pull Requests) como mecanismo principal de colaboração assíncrona, usando vídeos e comentários ricos.",
            "examples": "Equipes com fuso horário incompatível para programar em pares simultaneamente.",
            "execution": "<ol><li>Autor do código grava pequeno vídeo guiando pelas mudanças principais.</li><li>Revisor utiliza comentários de linha para sugerir melhorias.</li><li>Discussões complexas são resolvidas em threads detalhadas.</li></ol>",
            "result": "O PR #1042 recebeu 14 comentários cirúrgicos de Júlia sobre vazamento de memória. Vitor refatorou tudo de madrugada em Portugal, e Júlia aprovou pela manhã no Brasil, sem calls síncronas."
        },
        {
            "title": "Planejamento Poker Assíncrono",
            "icon": "🃏",
            "detail": "Estimativa de esforço de histórias de usuário feita individualmente antes da sessão de planejamento, focando o tempo síncrono apenas nas divergências.",
            "examples": "Reduzir o tempo excessivo de sessões de Refinamento ou Planning de 2h para 30min.",
            "execution": "<ol><li>Ferramenta (ex: Parabol ou plugin do Jira) notifica o time para estimar.</li><li>Devs votam no seu próprio tempo ao longo do dia.</li><li>Na reunião síncrona, apenas histórias com discrepâncias altas (ex: um votou 2, outro votou 13) são discutidas.</li></ol>",
            "result": "A ferramenta Parabol avisou às 9h. Carlos votou 3, Ana 8, Bruno 3. Na call das 14h, os 3 debateram o escopo rapidamente, Ana concordou com 5 pontos, e a planning inteira acabou em 25 minutos."
        },
        {
            "title": "Tempestade de Ideias Estruturada (SCAMPER)",
            "icon": "💡",
            "detail": "Técnica de ideação remota orientada por prompts específicos (Substituir, Combinar, Adaptar, Modificar, Procurar outros usos, Eliminar, Reorganizar).",
            "examples": "Time de produto precisa encontrar inovações incrementais para uma feature existente.",
            "execution": "<ol><li>Criar 7 colunas no board, uma para cada letra do SCAMPER.</li><li>Focar o time de forma cronometrada em responder perguntas para cada coluna.</li><li>Consolidar as ideias mais viáveis ao final.</li></ol>",
            "result": "No board de SCAMPER, a coluna 'Combinar' gerou a ideia do João: 'Gorjeta com doação solidária'. Essa feature, lançada no Q4, subiu a retenção do app de delivery em 15%."
        },
        {
            "title": "Mapeamento de Dependências com Fios Virtuais",
            "icon": "🔗",
            "detail": "Uso de conectores visuais (setas/linhas) em ferramentas de whiteboard para desenhar o PI Planning ou mapa de interconexões entre times.",
            "examples": "Eventos de planejamento em escala (SAFe PI Planning) com múltiplos times remotos.",
            "execution": "<ol><li>Cada time posiciona suas entregas (features) no board mensal.</li><li>Se um time A depende do B, eles conectam um 'fio vermelho' visual.</li><li>Reunião geral foca em resolver os gargalos apontados pelos emaranhados de fios.</li></ol>",
            "result": "Uma linha vermelha no Miro cruzava do Épico Pagamentos ao Épico Cadastro. A gerente alocou os Tech Leads na Sprint 1, garantindo a API pronta antes do atraso previsível na Sprint 5."
        },
        {
            "title": "Alinhamento de Expectativas com Team Canvas",
            "icon": "🎯",
            "detail": "Preenchimento de um canvas visual abordando propósito, metas pessoais, papéis, regras e valores do time em formato online.",
            "examples": "Kickoff de uma nova estrutura organizacional de tribos/squads no ambiente remoto.",
            "execution": "<ol><li>Importar template do Team Canvas no Miro.</li><li>Dedicar 10 minutos silenciosos para cada bloco.</li><li>Leitura em voz alta e discussão dos pontos críticos e alinhamentos divergentes.</li></ol>",
            "result": "No Team Canvas, a coluna 'Valores' dizia 'Foco no cliente' e 'Fraquezas' apontava 'Baixa cobertura de testes'. O dev sênior recém-contratado entendeu a dor real no primeiro dia de trabalho."
        },
        {
            "title": "Post-mortem Assíncrono com Documento Vivo",
            "icon": "📄",
            "detail": "Investigação colaborativa de falhas onde a linha do tempo e fatos são coletados em um documento na nuvem sem culpa (Blameless).",
            "examples": "Tratar uma queda de sistema (Outage) sem apontar dedos, reunindo logs e análises de vários fusos.",
            "execution": "<ol><li>Criar template de Post-mortem no Google Docs.</li><li>Todos os envolvidos adicionam dados de log, ações tomadas e observações de forma assíncrona.</li><li>Revisão síncrona final apenas para aprovar as 'Action Items' corretivas.</li></ol>",
            "result": "No Google Docs, o Dev A e SRE B colocaram os logs do Incidente #881. Foi constatado que o certificado expirou. A Action Item blameless gerada foi: 'Automatizar renovação via certbot'."
        },
        {
            "title": "Story Mapping (Mapeamento de Histórias) Remoto",
            "icon": "🗺️",
            "detail": "Organização de épicos e histórias em uma jornada temporal do usuário de forma horizontal e fatias de entrega verticalmente em ferramentas online.",
            "examples": "Sessões de discovery e definição de MVP para lançar um novo produto do zero.",
            "execution": "<ol><li>Escrever as etapas primárias do usuário no topo do board (A espinha dorsal).</li><li>Membros geram e anexam histórias detalhadas abaixo de cada etapa correspondente.</li><li>Traçar linhas horizontais definindo Release 1, Release 2, etc.</li></ol>",
            "result": "O card 'Cupom de desconto' desceu visualmente da Release 1 para a Release 2, garantindo que o MVP fosse restrito a 'Adicionar ao carrinho' e 'PIX', economizando 3 meses de desenvolvimento."
        },
        {
            "title": "Painel de Humor (Mood Board) Semanal",
            "icon": "😊",
            "detail": "Verificação simples e visual do engajamento e estado mental da equipe coletada assincronamente ao longo da semana.",
            "examples": "Monitoramento de burnout em times submetidos a altas cargas de estresse prolongadas no home office.",
            "execution": "<ol><li>Criar um calendário no board ou canal específico.</li><li>Todo final de dia, cada membro coloca um emoji verde, amarelo ou vermelho (ou meme) correspondente ao seu dia.</li><li>Liderança analisa tendências negativas contínuas para intervenções 1:1.</li></ol>",
            "result": "Na sexta, 8 colaboradores botaram o emoji 🔴 na planilha. O gerente notou o cansaço extremo coletivo e cancelou dailys da semana seguinte para focar no descanso da equipe."
        },
        {
            "title": "Celebração de Pequenas Vitórias (Ring the Bell)",
            "icon": "🎉",
            "detail": "Criação de gatilhos virtuais (bots de Slack, canais com GIFs) automatizados ou manuais quando uma entrega pequena ou venda é realizada.",
            "examples": "Incentivar um time comercial ou de engenharia na entrega contínua que perdeu a comemoração física no escritório.",
            "execution": "<ol><li>Integrar ferramentas (ex: webhook do Jira/Github) ao canal #vitorias do Slack.</li><li>Quando algo é feito, o bot avisa.</li><li>Todos reagem ativamente com emojis, gifs ou mensagens de parabéns.</li></ol>",
            "result": "Ao fechar o Épico no Jira, um webhook disparou: '🚀 Mariana entregou a Migração!'. 12 colegas reagiram com GIFs de fogos e cerveja no Slack instantaneamente, comemorando a conquista."
        },
        {
            "title": "Sessão de Mentoria / Coffee Chat Aleatório",
            "icon": "☕",
            "detail": "Uso de ferramentas como Donut app para parear aleatoriamente pessoas da empresa para um encontro virtual de 15 minutos não focado em trabalho.",
            "examples": "Reduzir o efeito de 'silos' entre departamentos que não interagem em um cenário remoto-first.",
            "execution": "<ol><li>Instalar bot no comunicador da empresa.</li><li>O bot pareia duas pessoas a cada quinzena e sugere horários.</li><li>As pessoas fazem uma videochamada rápida para tomar café e bater papo.</li></ol>",
            "result": "O app Donut emparelhou Bruno (Dados) e Carla (Redatora). Eles descobriram um hobby comum por astronomia, o que facilitou e acelerou o trabalho entre suas áreas em projetos futuros."
        },
        {
            "title": "Resolução de Conflitos via Escuta Ativa Virtual",
            "icon": "🕊️",
            "detail": "Facilitação remota de conflitos onde as partes se reúnem com um mediador e têm tempos rígidos estipulados para falar sem interrupção.",
            "examples": "Desgaste de relacionamento e atrito frequente entre área de Design e Engenharia de front-end.",
            "execution": "<ol><li>Mediador convoca reunião.</li><li>Regra de ouro: quando um fala, o microfone do outro é silenciado.</li><li>Pessoa A fala por 3 min. Pessoa B precisa resumir o que ouviu antes de responder.</li></ol>",
            "result": "Mário desabafou por 3 min. A Designer Luiza ouviu em silêncio e repetiu: 'Você sente que os assets bloqueiam seu código'. A validação esfriou a tensão e alinharam um novo hand-off."
        },
        {
            "title": "Estrutura de Rotação de Horários Básicos (Core Hours)",
            "icon": "⏰",
            "detail": "Técnica de alinhamento em que se define blocos mínimos obrigatórios diários para sobreposição de horários, garantindo total flexibilidade no resto do tempo.",
            "examples": "Membros em fusos horários extremos, como Costa Oeste EUA, Europa Central e Índia.",
            "execution": "<ol><li>Mapear a disponibilidade de fuso de cada membro num gráfico comum.</li><li>Encontrar um bloco de 2h a 3h que seja aceitável (ex: entre 10h e 13h no Brasil).</li><li>Definir essas como 'Core Hours' obrigatórias para respostas síncronas.</li></ol>",
            "result": "O dev em Tóquio e o de SP acordaram as 'Core Hours' das 08h às 10h (BR). Nesses horários eles fazem calls, e no restante operam livres sem cobranças de ping imediato no Slack."
        },
        {
            "title": "Feedback Peer-to-Peer Estruturado e Guiado",
            "icon": "💬",
            "detail": "Rodadas de feedback formativas feitas diretamente entre colegas com o suporte de um template claro de Comunicação Não Violenta (CNV), assincronamente ou em sessões agendadas.",
            "examples": "Melhorar a relação entre membros do time de forma orgânica, sem passar exclusivamente pelo gerente.",
            "execution": "<ol><li>Fornecer template 'Situação-Comportamento-Impacto'.</li><li>Fazer o sorteio dos pares.</li><li>Eles escrevem o feedback e trocam os documentos 1h antes da chamada.</li><li>Fazem chamada de 30 min para tirar dúvidas ou agradecer.</li></ol>",
            "result": "Carlos enviou: 'Situação: Ontem. Comportamento: Você apresentou meus slides. Impacto: Me senti invisível'. Joana se desculpou, e na próxima call garantiu a palavra a Carlos para a apresentação."
        },
        {
            "title": "Skill Matrix (Mapeamento de Competências) Virtual",
            "icon": "🛠️",
            "detail": "Autoavaliação e mapeamento coletivo das habilidades de cada membro do time inseridos num board compartilhado.",
            "examples": "Formação de novos times ou planejamento de sessões de pareamento para cobrir deficiências de conhecimento (Bus Factor baixo).",
            "execution": "<ol><li>Listar as habilidades chave do projeto nas colunas e membros nas linhas.</li><li>Cada membro pinta seu quadrado de cores variadas (Aprender, Faz Básico, Especialista).</li><li>Analisar buracos visuais onde o time tem baixo conhecimento geral.</li></ol>",
            "result": "A linha 'Jenkins' mostrou 1 Especialista e 7 'Não Sei's' em vermelho. Fernando foi encarregado de parear com 2 novatos no trimestre para aumentar o Bus Factor do time."
        },
        {
            "title": "Brainstorming Híbrido (1-2-4-All) Remoto",
            "icon": "🌪️",
            "detail": "Adaptação da estrutura libertadora '1-2-4-All' usando salas simultâneas para convergir ideias das partes menores até o todo progressivamente.",
            "examples": "Geração de soluções complexas em grupos grandes (15+ pessoas) online.",
            "execution": "<ol><li>1 min: Reflexão silenciosa e anotações individuais.</li><li>2 min: Salas de 2 pessoas unem e refinam ideias.</li><li>4 min: Salas juntam-se formando grupos de 4 para filtrar as melhores opções.</li><li>All: Apresentação para o grupo principal.</li></ol>",
            "result": "A sessão de 16 devs fluiu em duplas, depois quartetos e no grande grupo aprovaram 1 arquitetura Serverless sólida unanimemente, poupando o time de longas discussões circulares."
        },
        {
            "title": "Cerimônia de Encerramento (Project Closure) Digital",
            "icon": "🏁",
            "detail": "Evento focado inteiramente em celebrar a conclusão, repassar lições aprendidas e desfazer o time ou iniciar uma nova fase, tudo documentado de modo memorável.",
            "examples": "O fim de um trimestre bem sucedido com entregas pesadas da OKR principal.",
            "execution": "<ol><li>Criar uma apresentação tipo 'O caminho até aqui' com números finais e screenshots.</li><li>Rodada livre de agradecimentos ('Shoutouts').</li><li>Brinde virtual e arquivamento formal dos quadros e canais do Slack com a permissão do grupo.</li></ol>",
            "result": "O 'Projeto Apolo' fechou com conversão recorde de +12%. O canal #projeto-apolo foi arquivado sob aplausos e emojis de champanhe no Zoom, trazendo senso máximo de dever cumprido."
        }
    ],
    "Sensemaking & Conflitos": [
        {
            "title": "Cynefin Framework",
            "icon": "🧭",
            "detail": "Framework de sensemaking para entender se um desafio é Simples, Complicado, Complexo ou Caótico, guiando a resposta adequada e evitando conflitos de abordagem.",
            "examples": "Equipe aplicando processos rígidos de domínio Complicado em um cenário de crise Caótica, gerando frustração e inércia.",
            "execution": "<ol><li>Desenhe a matriz de domínios.</li><li>Colecione as dores da equipe em post-its.</li><li>Mapeie os problemas nos domínios correspondentes.</li><li>Ajuste a estratégia de ação para cada grupo de problemas.</li></ol>",
            "result": "A equipe de Plataforma parou de tentar aplicar sprints de 2 semanas (Complicado) para resolver o incidente de segurança X-49 (Caótico). A líder Sarah imediatamente estabeleceu uma 'war room' (agir-sentir-responder), reduzindo o tempo de mitigação de 8 horas para 45 minutos."
        },
        {
            "title": "Comunicação Não-Violenta (CNV)",
            "icon": "🕊️",
            "detail": "Modelo focado em empatia e clareza, separando observações de julgamentos para resolver atritos interpessoais de forma pacífica.",
            "examples": "Um desenvolvedor acusa o outro de 'sempre quebrar a build', gerando um clima hostil na equipe.",
            "execution": "<ol><li>Descreva os fatos observáveis sem julgamento.</li><li>Nomeie o sentimento gerado pelo evento.</li><li>Exponha a necessidade não atendida.</li><li>Formule um pedido claro, positivo e realizável.</li></ol>",
            "result": "Em vez de gritar, João disse: 'Quando o PR #405 foi mergeado sem testes (fato), fiquei frustrado (sentimento) porque precisamos garantir a estabilidade do release (necessidade). Você pode adicionar os testes unitários até as 14h? (pedido)'. Marcos concordou imediatamente, evitando a habitual briga de 3 dias no Slack."
        },
        {
            "title": "5 Porquês (5 Whys)",
            "icon": "🔍",
            "detail": "Técnica iterativa para explorar a causa raiz de um defeito ou conflito sistêmico, indo além dos sintomas superficiais.",
            "examples": "Um bug crítico que continua voltando em diferentes releases e gerando atritos entre QA e Dev.",
            "execution": "<ol><li>Descreva o problema claramente.</li><li>Pergunte 'Por que isso aconteceu?'.</li><li>Para a resposta, pergunte 'Por que?' novamente.</li><li>Repita até chegar à causa estrutural ou sistêmica.</li></ol>",
            "result": "Descobrimos que a instabilidade no login não era 'culpa da Ana', mas sim: 1. Login falhou -> 2. Token expirou -> 3. Cron job de refresh travou -> 4. Memória estourou no pod -> 5. Falta de limite de recursos no Kubernetes. A equipe de SRE ajustou o limite de RAM de 512MB para 1GB, resolvendo o problema definitivamente."
        },
        {
            "title": "Diagrama de Ishikawa",
            "icon": "🐟",
            "detail": "Também conhecido como Espinha de Peixe, categoriza as causas raízes de um problema em diferentes dimensões (ex: pessoas, processos, ferramentas).",
            "examples": "Atrasos recorrentes nas entregas de sprint causando atrito com stakeholders.",
            "execution": "<ol><li>Desenhe a espinha de peixe com o problema na 'cabeça'.</li><li>Crie categorias para as 'espinhas' (Pessoas, Processos, Ferramentas, Ambiente).</li><li>Faça um brainstorm das causas em cada categoria.</li><li>Priorize as causas raízes mais impactantes para ação.</li></ol>",
            "result": "Para o atraso da Sprint 12, mapeamos: Ferramentas (Jira lento), Pessoas (Falta de DevOps sênior), Processos (Code Review demorando 48h). A equipe decidiu criar um bot de alerta para reviews pendentes no Slack, reduzindo o tempo de bloqueio para 4 horas."
        },
        {
            "title": "Causal Loop Diagrams",
            "icon": "🔄",
            "detail": "Ferramenta de System Thinking para mapear variáveis interconectadas e loops de feedback que perpetuam um conflito.",
            "examples": "Pressão por velocidade causa mais bugs, que causam mais retrabalho, que aumenta a pressão (ciclo vicioso).",
            "execution": "<ol><li>Identifique as variáveis-chave do problema.</li><li>Desenhe setas indicando como uma variável afeta a outra (positiva ou negativamente).</li><li>Identifique loops de reforço (viciosos/virtuosos) e de balanceamento.</li><li>Discuta onde intervir para quebrar o ciclo.</li></ol>",
            "result": "O time desenhou o loop: 'Pressão do PO Carlos' -> 'Corte de testes na pipeline' -> 'Bugs em Produção' -> 'Mais reuniões de crise' -> 'Ainda menos tempo para codar' -> 'Mais Pressão'. Ao ver o desenho, Carlos concordou em reduzir o escopo da release 2.1 em 20% para quebrar o ciclo vicioso."
        },
        {
            "title": "O Modelo SCARF",
            "icon": "🧠",
            "detail": "Baseado em neurociência, mapeia ameaças ou recompensas sociais em 5 domínios: Status, Certeza, Autonomia, Relacionamento, Justiça.",
            "examples": "Um membro da equipe se torna agressivo durante uma mudança organizacional abrupta (ameaça à Certeza e Autonomia).",
            "execution": "<ol><li>Analise o conflito através dos 5 domínios do SCARF.</li><li>Identifique qual domínio do indivíduo foi 'ameaçado'.</li><li>Adapte a comunicação para reduzir a ameaça nesse domínio.</li><li>Crie ações que gerem sensação de recompensa nos domínios afetados.</li></ol>",
            "result": "Quando a empresa mudou a stack de React para Vue (ameaça à Certeza e Status de Lucas, o tech lead React), a gestora Marina ofereceu a Lucas a liderança do comitê de arquitetura da migração (reforço de Status e Autonomia), transformando sua resistência ativa em engajamento."
        },
        {
            "title": "Iceberg Model",
            "icon": "🧊",
            "detail": "Modelo de pensamento sistêmico que ajuda a ver abaixo dos eventos superficiais para entender padrões, estruturas e modelos mentais.",
            "examples": "Conflitos frequentes em reuniões de planejamento parecem eventos isolados, mas refletem estruturas de incentivo desalinhadas.",
            "execution": "<ol><li>Mapeie o 'Evento' (o que aconteceu, no topo).</li><li>Identifique 'Padrões' (o que tem acontecido ao longo do tempo).</li><li>Explore as 'Estruturas Sistêmicas' (o que causa os padrões).</li><li>Revele os 'Modelos Mentais' (crenças que sustentam o sistema).</li></ol>",
            "result": "Evento: 'Servidor caiu na Black Friday'. Padrão: 'Todo ano a infra não aguenta o pico'. Estrutura: 'Orçamento de cloud é cortado em outubro'. Modelo Mental: 'A diretoria acha que TI é custo, não investimento'. O CTO usou isso para aprovar um aumento de R$50.000 em instâncias elásticas preemptivas, prevenindo a queda no ano seguinte."
        },
        {
            "title": "Escada da Inferência",
            "icon": "🪜",
            "detail": "Ajuda a revelar como as pessoas tiram conclusões precipitadas a partir de dados selecionados e crenças prévias.",
            "examples": "Um gestor conclui que um desenvolvedor é desmotivado por chegar tarde, sem saber de seus problemas familiares.",
            "execution": "<ol><li>Identifique a conclusão que gerou o conflito.</li><li>Desça a escada perguntando: 'Quais dados sustentam isso?'.</li><li>Explore os filtros e crenças que distorceram os dados originais.</li><li>Subam juntos a escada usando dados objetivos compartilhados.</li></ol>",
            "result": "O gestor Pedro quase demitiu Roberto achando que ele estava fazendo 'quiet quitting' por não falar nas dailys. Ao descer a escada para os fatos, Pedro descobriu que Roberto estava cuidando de seu pai doente na UTI e precisava apenas ajustar o horário da daily para as 11h. A produtividade de Roberto voltou a 100%."
        },
        {
            "title": "Triângulo de Karpman",
            "icon": "🎭",
            "detail": "Identifica dinâmicas destrutivas onde pessoas assumem os papéis de Vítima, Perseguidor ou Salvador em conflitos.",
            "examples": "Um Scrum Master (Salvador) sempre faz o trabalho de um dev atrasado (Vítima), e o PO (Perseguidor) reclama da qualidade.",
            "execution": "<ol><li>Ensine o modelo do Triângulo Dramático à equipe.</li><li>Identifique em qual papel cada um está operando no conflito atual.</li><li>Ajude a equipe a mudar para o Triângulo do Empoderamento (Criador, Desafiador, Coach).</li><li>Estabeleça limites claros de responsabilidade.</li></ol>",
            "result": "A Tech Lead Julia (Salvadora) parou de consertar os bugs do estagiário Tiago (Vítima) às sextas-feiras à noite. Ela mudou para o papel de Coach, dedicando 1h na quinta para fazer pair programming com Tiago. Em 3 semanas, Tiago entregou suas tasks sem erros e o PO (Perseguidor) parou de reclamar da qualidade."
        },
        {
            "title": "Polarity Management",
            "icon": "⚖️",
            "detail": "Usado para gerenciar dilemas contínuos que não podem ser 'resolvidos', apenas balanceados (ex: Inovação vs Estabilidade).",
            "examples": "Conflito eterno entre a equipe de Produto (quer features rápidas) e a equipe de Infra (quer estabilidade).",
            "execution": "<ol><li>Identifique as duas polaridades (não é um problema de 'ou/ou', mas de 'e/e').</li><li>Mapeie os benefícios de focar em cada polo.</li><li>Mapeie os riscos de focar excessivamente em apenas um.</li><li>Crie sinais de alerta e ações para manter o equilíbrio dinâmico.</li></ol>",
            "result": "O time aceitou que 'Inovar Rápido' e 'Manter Sistema Estável' são polos. Estabeleceram alertas: se os bugs críticos passarem de 5 (Sinal de risco da Inovação), o time congela novas features e foca em qualidade. Se ficarmos 3 sprints sem lançar nada (Sinal de risco de Estabilidade), alocamos 30% da capacidade para experimentação. Acabou a briga semanal."
        },
        {
            "title": "Círculos de Paz",
            "icon": "⭕",
            "detail": "Prática restaurativa de diálogo estruturado em círculo, usando um 'bastão de fala' para garantir equidade na comunicação.",
            "examples": "Um conflito grave que quebrou a confiança da equipe e requer uma conversa profunda e segura para reconciliação.",
            "execution": "<ol><li>Sente a equipe em círculo, sem mesas no centro.</li><li>Estabeleça o bastão de fala: só fala quem o detém.</li><li>Faça uma pergunta geradora sobre o impacto do conflito.</li><li>Passe o bastão até que todos tenham se expressado livremente e empatia seja gerada.</li></ol>",
            "result": "Após o projeto Phoenix fracassar e custar R$200k, os 12 membros sentaram em roda com uma 'talking piece'. Quando o arquiteto Sênior admitiu chorando que teve um burnout escondido, a raiva do time virou empatia. Saíram de lá com um novo acordo de convivência de 5 pontos, zerando a toxicidade no ambiente."
        },
        {
            "title": "Diálogo de Bohm",
            "icon": "🗣️",
            "detail": "Forma de conversa livre sem objetivo de decisão, focada apenas na suspensão de julgamentos e compartilhamento de significados.",
            "examples": "A equipe tem crenças fundamentalmente diferentes sobre a arquitetura do sistema e precisa se entender antes de decidir.",
            "execution": "<ol><li>Reúna o grupo sem uma pauta resolutiva.</li><li>Estabeleça o princípio de escuta profunda e suspensão de reações.</li><li>Encoraje que falem para o centro do grupo, construindo um 'pool de significado'.</li><li>Observe os modelos mentais coletivos emergirem.</li></ol>",
            "result": "Os 8 arquitetos de software sentaram por 90 minutos sem pauta para discutir o conceito de 'Microsserviços vs Monolito'. Sem a pressão de decidir a stack do projeto, confessaram seus medos reais sobre complexidade e deployment. Dessa compreensão mútua, emergiu a ideia híbrida (Monolito Modular) que a empresa adotou com sucesso 2 meses depois."
        },
        {
            "title": "Lean Coffee de Conflitos",
            "icon": "☕",
            "detail": "Adaptação do formato Lean Coffee para discutir tensões e conflitos de forma democrática e estruturada por time-boxes.",
            "examples": "Muitas pequenas tensões na equipe de desenvolvimento e não há tempo estruturado para endereçar todas.",
            "execution": "<ol><li>Todos escrevem tópicos de tensão em post-its.</li><li>O grupo vota nos tópicos mais urgentes.</li><li>Discutem o tópico mais votado em time-boxes de 5 minutos (votando para estender ou passar).</li><li>Capturam itens de ação ao final de cada discussão.</li></ol>",
            "result": "Em vez de uma reunião de lavagem de roupa suja de 3 horas, o time votou os tópicos. O mais votado foi 'Pull Requests travados'. Discutiram por 10 minutos (dois time-boxes de 5 min) e saíram com a ação: 'Nenhum PR pode ter mais de 400 linhas de código'. A tensão caiu 80% e a reunião durou apenas 45 minutos."
        },
        {
            "title": "Abordagem de Harvard",
            "icon": "🤝",
            "detail": "Negociação Baseada em Princípios: separa pessoas do problema, foca em interesses e inventa opções de ganho mútuo.",
            "examples": "Dois times disputando recursos limitados de cloud para seus respectivos projetos.",
            "execution": "<ol><li>Separe as pessoas do problema (foco no desafio, não em ataques).</li><li>Foque nos interesses subjacentes, não nas posições declaradas.</li><li>Invente opções criativas de ganho mútuo antes de decidir.</li><li>Insista no uso de critérios objetivos para a avaliação justa.</li></ol>",
            "result": "O Time A queria o único DBA exclusivo por 2 semanas; o Time B também. Em vez de brigarem, exploraram interesses: Time A precisava de migração de dados; Time B de otimização de query. Descobriram que o Time B poderia fazer a otimização na semana 3 sem atrasar a release. Ambos ganharam o que precisavam, economizando 15 horas de negociação infrutífera com o Diretor."
        },
        {
            "title": "World Cafe",
            "icon": "🌍",
            "detail": "Processo de diálogo em pequenos grupos que simula conversas de café para explorar questões complexas e compartilhar conhecimento.",
            "examples": "Sensemaking organizacional após uma grande fusão ou reestruturação departamental.",
            "execution": "<ol><li>Crie mesas de 4-5 pessoas em ambiente acolhedor.</li><li>Apresente uma pergunta poderosa sobre o tema central.</li><li>Após 20 min, as pessoas trocam de mesa, deixando um 'anfitrião' para resumir.</li><li>Reúna os insights principais em uma sessão plenária final.</li></ol>",
            "result": "Na fusão das duas empresas, 60 funcionários discutiram 'Como integrar nossas culturas?' em mesinhas redondas. Após 3 rodadas de 20 minutos trocando de mesa, a ideia de criar um 'Dicionário de Termos Técnicos Unificados' emergiu em 4 mesas diferentes e foi implementada no dia seguinte na intranet, reduzindo as falhas de comunicação."
        },
        {
            "title": "Open Space Technology",
            "icon": "🌌",
            "detail": "Método de facilitação onde os próprios participantes criam e gerenciam a agenda ao redor de um tema central crítico.",
            "examples": "Precisa-se resolver um grande problema técnico de dívida técnica crônica envolvendo mais de 50 desenvolvedores.",
            "execution": "<ol><li>Abra o círculo e apresente o tema urgente.</li><li>Convide qualquer um a propor tópicos no quadro de agenda em branco.</li><li>Explique a Lei dos Dois Pés (mobilidade e responsabilidade).</li><li>Inicie as sessões simultâneas e colha relatórios rápidos de cada uma.</li></ol>",
            "result": "No evento de 1 dia sobre Dívida Técnica para 100 engenheiros, Carlos (Junior) propôs uma sessão sobre 'Refatorar o módulo de Pagamentos'. 15 pessoas apareceram, incluindo a CFO e o Arquiteto Chefe. Em 40 minutos, eles mapearam a solução completa que a gestão tentava resolver há 6 meses sem sucesso."
        },
        {
            "title": "Appreciative Inquiry",
            "icon": "✨",
            "detail": "Foca na exploração dos pontos fortes e no que já funciona bem (Núcleo Positivo), em vez de apenas dissecar o que está quebrado.",
            "examples": "Uma equipe desmoralizada por meses de entregas fracassadas precisa planejar a recuperação sem entrar em depressão coletiva.",
            "execution": "<ol><li>Descobrir (Discovery): O que dá vida à organização quando está no seu melhor?</li><li>Sonhar (Dream): Qual pode ser o futuro ideal?</li><li>Desenhar (Design): Como criar a estrutura para alcançar esse futuro?</li><li>Entregar (Destiny): Como implementar o design de forma contínua?</li></ol>",
            "result": "A equipe de CS estava exausta com o churn alto. Em vez de perguntar 'Por que falhamos?', a facilitação focou em 'Conte sobre um cliente que você salvou no último minuto'. A energia na sala mudou. Eles extraíram 3 táticas de sucesso da história da atendente Maria e criaram um novo playbook de retenção que reduziu o churn em 12% em dois meses."
        },
        {
            "title": "Six Thinking Hats",
            "icon": "🎩",
            "detail": "Técnica de Edward de Bono que obriga o grupo a pensar paralelamente a partir de 6 perspectivas distintas, reduzindo atritos opinativos.",
            "examples": "Discussões acaloradas sobre uma nova arquitetura onde otimistas e pessimistas batem de frente eternamente.",
            "execution": "<ol><li>Apresente o problema.</li><li>Passem juntos pelos chapéus: Branco (fatos), Vermelho (emoções).</li><li>Continuem: Preto (riscos), Amarelo (benefícios), Verde (criatividade).</li><li>Finalize com o Azul (controle e próximos passos).</li></ol>",
            "result": "Para discutir a adoção de IA no código, o time colocou o 'Chapéu Preto' (riscos) por 10 minutos e listou 15 vulnerabilidades legais. Depois, puseram o 'Chapéu Amarelo' (benefícios) e listaram o aumento de 30% na velocidade. No fim, a decisão (Chapéu Azul) foi adotar IA apenas para geração de testes, unindo o receio dos seniores e a empolgação dos juniores."
        },
        {
            "title": "Disney Creative Strategy",
            "icon": "🎢",
            "detail": "Separa os estados de pensamento em Sonhador, Realista e Crítico, evitando que o julgamento precoce mate a criatividade e gere conflito.",
            "examples": "Ideação de soluções para um conflito sistêmico sendo constantemente bloqueada por 'advogados do diabo'.",
            "execution": "<ol><li>Sala do Sonhador: Explore o que é possível sem restrições de realidade.</li><li>Sala do Realista: Como transformar o sonho num plano prático?</li><li>Sala do Crítico: Identifique as falhas no plano do Realista (nunca criticando o Sonhador diretamente).</li></ol>",
            "result": "Na sala do Sonhador, inventaram um app que 'adivinha o pedido do cliente por telepatia'. Na sala do Realista, adaptaram para 'compra com 1 clique baseado no histórico usando machine learning simples'. Na sala do Crítico, viram que precisavam tratar os falsos positivos no cartão de crédito. O MVP foi lançado em 3 semanas com uma taxa de conversão 20% maior."
        },
        {
            "title": "Árvore de Evaporação de Nuvens",
            "icon": "🌩️",
            "detail": "Ferramenta da Teoria das Restrições para resolver conflitos onde as partes parecem ter requisitos mutuamente exclusivos.",
            "examples": "Produto quer lançar amanhã para ganhar mercado; Qualidade quer bloquear o lançamento para testar mais.",
            "execution": "<ol><li>Escreva o Objetivo Comum (ex: Sucesso do produto).</li><li>Escreva as Necessidades de ambos os lados que suportam o objetivo.</li><li>Escreva as Ações (em conflito) que cada lado quer tomar para satisfazer sua necessidade.</li><li>Exponha e desafie as premissas escondidas por trás das setas lógicas para 'evaporar' o conflito.</li></ol>",
            "result": "Vendas precisa dar desconto (A) para fechar meta; Financeiro proíbe descontos (B) para manter a margem. A premissa oculta da seta Vendas -> A era: 'Clientes só compram se tiver redução de preço'. Evaporamos a nuvem mudando o desconto em dinheiro para a inclusão de um módulo extra de software que não custa nada para a empresa reproduzir. Ambos bateram suas metas."
        },
        {
            "title": "ORID (Focused Conversation)",
            "icon": "🎯",
            "detail": "Estrutura de conversa que passa por 4 níveis: Objetivo, Reflexivo, Interpretativo e Decisório. Previne pular para conclusões.",
            "examples": "Revisão de um incidente de segurança grave que causou pânico e acusações.",
            "execution": "<ol><li>Objetivo: O que vimos/ouvimos? (Apenas fatos).</li><li>Reflexivo: Como nos sentimos em relação a isso? (Emoções).</li><li>Interpretativo: Qual o significado/impacto disso? (Sentido).</li><li>Decisório: O que faremos a respeito? (Ação).</li></ol>",
            "result": "O -> 'A API caiu às 14h, voltou às 16h'. R -> 'Ficamos desesperados sem saber quem ligar'. I -> 'Descobrimos que não temos um processo de On-Call claro'. D -> 'Vamos assinar o PagerDuty amanhã e o João fará a primeira rotação na sexta'. A conversa levou 20 minutos e ninguém apontou o dedo para o DevOps."
        },
        {
            "title": "Mapa de Empatia de Conflitos",
            "icon": "🧩",
            "detail": "Adaptação do mapa de empatia de UX para entender a perspectiva da outra parte envolvida em um conflito.",
            "examples": "Product Manager e Tech Lead incapazes de entender as prioridades um do outro.",
            "execution": "<ol><li>Divida as pessoas e peça que cada uma crie um mapa de empatia *sobre o outro*.</li><li>Preencha: O que a outra pessoa Pensa/Sente? Vê? Fala/Faz? Escuta? Suas Dores e Ganhos?</li><li>Compartilhem os mapas, corrigindo suposições incorretas.</li></ol>",
            "result": "Quando o DevTech desenhou o mapa do Product Owner, percebeu que o PO ouvia o CEO ameaçar cortar o budget (Escuta) e sentia medo de perder o emprego (Sentimento/Dor). O DevTech percebeu que a pressão por features não era maldade, mas sobrevivência. Ele parou de bloquear as entregas e começou a negociar escopo."
        },
        {
            "title": "Role-playing de Empatia",
            "icon": "🔀",
            "detail": "Técnica onde as partes em conflito invertem papéis e argumentam a partir do ponto de vista do adversário.",
            "examples": "Impasse em negociação de cronograma entre a equipe de vendas e engenharia.",
            "execution": "<ol><li>Identifique as posições de conflito.</li><li>Solicite que Vendas atue como Engenharia e defenda os prazos técnicos.</li><li>Solicite que Engenharia atue como Vendas e defenda a urgência comercial.</li><li>Realizem um mini-debate nestes papéis cruzados.</li></ol>",
            "result": "O Analista de QA (atuando como Dev) teve que argumentar por que entregar código sujo rápido era importante, enquanto o Dev (atuando como QA) teve que explicar as falhas em produção. Ao trocar os papéis, o Dev sentiu a dor de testar sem documentação. No mesmo dia, eles criaram um template simples de PR com checklist de testes."
        },
        {
            "title": "Práticas Narrativas",
            "icon": "📖",
            "detail": "Externalização do problema: a pessoa não é o problema, o problema é o problema. Muda a semântica do conflito.",
            "examples": "Equipe rotulando um membro como 'O Gargalo' de forma pejorativa.",
            "execution": "<ol><li>Dê um nome ao problema de forma externalizada (ex: 'A Complexidade Sombria').</li><li>Pergunte: 'Como a Complexidade tem afetado nossa rotina?'.</li><li>Pergunte: 'Quando nós conseguimos vencer a Complexidade?'.</li><li>Unam-se contra o problema externalizado.</li></ol>",
            "result": "Eles pararam de chamar o arquiteto sênior de 'Gargalo'. Começaram a referir-se ao processo como 'O Monstro do Acesso aos Dados'. Quando o foco mudou, o time inteiro começou a sugerir formas de automatizar o provisionamento de acesso, derrotando 'O Monstro' em 2 sprints, em vez de isolar o colega."
        },
        {
            "title": "SenseMaker Methodology",
            "icon": "🕸️",
            "detail": "Coleta e interpretação de micro-narrativas da base da empresa para entender a cultura real e conflitos sistêmicos distribuídos.",
            "examples": "Alta gestão querendo entender por que há atrito e resistência generalizada à transformação ágil.",
            "execution": "<ol><li>Colete histórias curtas do dia-a-dia de forma anônima e contínua.</li><li>Peça que o autor da história a signifique usando triângulos conceituais e díades.</li><li>Analise os padrões das narrativas para identificar clusters de significado.</li><li>Crie experimentos seguros ('safe-to-fail') para alterar o padrão das narrativas.</li></ol>",
            "result": "A coleta de 200 micro-histórias anônimas revelou que 70% das narrativas de 'atraso' estavam agrupadas perto do triângulo de 'Falta de Clareza do Cliente', não em 'Falta de Habilidade Técnica'. O CTO imediatamente parou a contratação de novos desenvolvedores sêniores e contratou 3 Product Owners especialistas em Discovery."
        },
        {
            "title": "Aquário (Fishbowl)",
            "icon": "🐠",
            "detail": "Formato para organizar conversas difíceis em grandes grupos. Apenas quem está no 'aquário' (círculo interno) pode falar.",
            "examples": "Reunião de 30 pessoas para debater a mudança de uma tecnologia core, onde muitos falam ao mesmo tempo e dominam a pauta.",
            "execution": "<ol><li>Coloque 4-5 cadeiras no centro (o aquário) e as demais ao redor.</li><li>Apenas quem está no aquário fala. Uma cadeira central fica sempre vazia.</li><li>Alguém de fora senta na cadeira vazia quando quiser contribuir.</li><li>Alguém do aquário deve sair imediatamente para manter uma cadeira vazia.</li></ol>",
            "result": "Na tribo de 50 pessoas, apenas os 4 no centro do 'aquário' debatiam se iríamos de AWS ou Azure. Quando a cadeira vazia foi ocupada pela estagiária de segurança, ela apontou uma vulnerabilidade de compliance na Azure que os arquitetos não sabiam. A decisão final por AWS foi tomada com tranquilidade e escuta atenta dos outros 45 membros."
        },
        {
            "title": "Fist to Five",
            "icon": "🖐️",
            "detail": "Técnica visual e instantânea para checar o nível de consenso em um grupo e externalizar objeções rapidamente.",
            "examples": "Equipe precisa decidir sobre adotar uma nova convenção de código e as opiniões estão divididas e passivas.",
            "execution": "<ol><li>O facilitador apresenta a proposta final.</li><li>No 'já', todos mostram as mãos: punho fechado (bloqueio veto) até 5 dedos (apoio total).</li><li>Se alguém votar com punho ou 1 dedo, o facilitador para e explora a objeção ('Qual sua preocupação?').</li><li>Ajuste a proposta e repita a votação até consenso viável.</li></ol>",
            "result": "Na proposta de trabalhar remoto às sextas, a maioria deu 4 ou 5 dedos. Mas o desenvolvedor sênior Pedro levantou o punho fechado (veto). Ele explicou que sexta é o dia de deploy do cliente principal e precisava de apoio físico. Ajustaram a proposta para remoto às quartas, e a segunda votação teve apenas 4s e 5s. Aprovado em 5 minutos."
        },
        {
            "title": "Tomada de Decisão por Consentimento",
            "icon": "👌",
            "detail": "Princípio da Sociocracia. O objetivo não é o consenso (todos amam a ideia), mas o consentimento (ninguém tem uma objeção de risco fatal).",
            "examples": "O processo de decisão é paralisado porque sempre esperam uma solução perfeita que todos adorem.",
            "execution": "<ol><li>Apresente a proposta. Fila de perguntas para esclarecimento.</li><li>Rodada rápida de reações gerais (sem debater).</li><li>Rodada de objeções formais ('Isso é seguro o suficiente para tentar? Causará danos?').</li><li>Se houver objeções reais, integre-as e adapte a proposta.</li></ol>",
            "result": "A proposta de migrar a base para PostgreSQL gerou desconforto. Em vez de buscar que todos amassem a ideia, a facilitadora perguntou: 'Alguém tem uma objeção baseada em um risco fatal e não contornável?'. Não havia risco fatal, apenas preferência. A proposta foi aceita em 10 minutos para iniciar a Prova de Conceito, destravando um mês de paralisia analítica."
        },
        {
            "title": "Processamento de Tensões",
            "icon": "⚡",
            "detail": "Baseado na Holacracia. Tensão é definida apenas como 'a diferença entre o que é e o que poderia ser'. Transforma reclamação em ação.",
            "examples": "Muitas reclamações de corredor sobre como os code reviews são dolorosos, mas nenhuma mudança estrutural.",
            "execution": "<ol><li>Capture a Tensão (O que você sentiu/observou?).</li><li>Identifique a necessidade (O que você precisa para aliviar a tensão?).</li><li>Processe usando o fluxo tático: pedir uma ação a um papel, alterar uma política, compartilhar informação.</li><li>Saia com um próximo passo claro e atribuído.</li></ol>",
            "result": "A designer Mariana trouxe uma tensão: 'Meus assets não são usados na versão final'. Necessidade: garantir a qualidade visual da UI. Processamento: criou-se a política onde o papel 'Front-end' precisa do 'Design Approval' antes do deploy. Em 15 minutos, a reclamação virou uma regra transparente de governança."
        },
        {
            "title": "Matriz Thomas-Kilmann (TKI)",
            "icon": "📊",
            "detail": "Avalia estilos de lidar com conflitos com base em duas dimensões: Assertividade (foco em si) e Cooperatividade (foco no outro).",
            "examples": "Membros da equipe com perfis muito acomodados que evitando conflitos importantes e deixam a qualidade cair.",
            "execution": "<ol><li>Mapeie os comportamentos da equipe nos 5 estilos: Competir, Colaborar, Comprometer, Evitar ou Acomodar.</li><li>Mostre como o 'Evitar' está gerando dívida técnica e conflito futuro.</li><li>Facilite dinâmicas para exercitar o estilo de 'Colaborar' (alta assertividade e alta cooperação).</li></ol>",
            "result": "O gerente Lucas percebeu que usava muito o estilo 'Evitar' com clientes difíceis, deixando a equipe lidar com a carga excessiva de bugs. Ao aplicar o TKI, mudou para 'Competir' ao defender o escopo contratual (dizendo não a 4 novas features de graça), e depois para 'Colaborar' ao desenhar o roadmap de longo prazo com o cliente."
        },
        {
            "title": "Janela de Johari",
            "icon": "🪟",
            "detail": "Ferramenta para melhorar a autoconsciência e o entendimento mútuo no grupo, explorando áreas abertas, cegas, ocultas e desconhecidas.",
            "examples": "Falta de confiança mútua e comunicação defensiva entre novos membros de uma equipe recém-formada.",
            "execution": "<ol><li>Distribua a lista de adjetivos de Johari.</li><li>Cada pessoa escolhe adjetivos que a definem e pede aos pares que escolham adjetivos sobre ela.</li><li>Mapeiem juntos os resultados nos quadrantes (Área Aberta, Cega, Oculta e Desconhecida).</li><li>Estimule o feedback para diminuir a Área Cega e a autoexposição para diminuir a Área Oculta.</li></ol>",
            "result": "Na dinâmica, o líder técnico Bruno ficou chocado ao ver 'Intimidador' e 'Arrogante' na sua Área Cega (os outros viam, ele não). Ele pensava ser apenas 'Direto'. Com o feedback, ele começou a pedir a opinião dos juniores nas reuniões em vez de ditar a solução logo de cara. O engajamento da equipe aumentou perceptivelmente no mês seguinte."
        },
        {
            "title": "Mapeamento de Stakeholders",
            "icon": "🗺️",
            "detail": "Analisa o poder e o interesse das partes interessadas para gerenciar expectativas e prevenir conflitos de desalinhamento político.",
            "examples": "Conflitos constantes nos comitês diretivos porque os líderes não estão envolvidos no momento certo.",
            "execution": "<ol><li>Liste todos os envolvidos no projeto.</li><li>Posicione-os num gráfico com os eixos: Poder (Influência) vs Interesse.</li><li>Identifique quem deve ser Gerenciado de Perto, Mantido Satisfeito, Mantido Informado ou Monitorado.</li><li>Crie um plano de comunicação alinhado à matriz.</li></ol>",
            "result": "Mapearam que o Diretor Financeiro tinha Alto Poder, mas Baixo Interesse no novo CRM, até descobrir os custos de licença. Eles o moveram para 'Gerenciar de Perto' na matriz, enviando um relatório executivo financeiro a cada 15 dias. Quando a renovação chegou, ele aprovou o orçamento de R$150.000 sem fazer uma única objeção."
        },
        {
            "title": "Troika Consulting",
            "icon": "🤝",
            "detail": "Uma 'Liberating Structure' focada em obter ajuda rápida e prática de colegas de forma segura e imediata.",
            "examples": "Um desenvolvedor travado em um problema complexo hesita em pedir ajuda, o que atrasa a sprint e gera tensão.",
            "execution": "<ol><li>Forme grupos de três pessoas (um 'cliente' e dois 'consultores').</li><li>O cliente expõe o seu desafio (1 min).</li><li>Os consultores fazem perguntas esclarecedoras (1 a 2 min).</li><li>O cliente vira de costas (ou desliga a câmera) enquanto os consultores debatem e dão conselhos entre si (4 a 5 min).</li><li>O cliente volta e compartilha o que achou mais valioso.</li></ol>",
            "result": "Carlos (cliente) virou de costas. Os consultores Ana e João debateram: 'Acho que o Carlos tem medo de dar feedback duro para o estagiário porque não quer parecer chefe autoritário'. Carlos, ao ouvir isso sem poder se defender, percebeu que era verdade. Ele virou e disse: 'Vocês têm razão, vou fazer um treinamento de feedback amanhã'."
        },
        {
            "title": "15% Solutions",
            "icon": "📈",
            "detail": "Outra 'Liberating Structure' que foca em focar no que pode ser feito imediatamente, com recursos e autoridade atuais, ignorando restrições maiores.",
            "examples": "Equipe paralisa frente a um problema enorme de dívida técnica, sentindo-se impotente e frustrada.",
            "execution": "<ol><li>Apresente um desafio complexo.</li><li>Peça que cada um reflita individualmente: \"Qual é a sua solução de 15%? O que você pode fazer agora sem pedir permissão ou recursos extras?\".</li><li>Compartilhem as respostas em pequenos grupos (pares ou trios) e construam ações rápidas.</li></ol>",
            "result": "Não podíamos contratar novos devs para reescrever o sistema legado (100% da solução). Mas a 15% solution da equipe foi: 'Nós controlamos a nossa branch. Vamos aplicar o princípio do escoteiro (deixar mais limpo do que encontrou) em cada arquivo que tocarmos a partir de amanhã'. Em 4 meses, a complexidade ciclomática do sistema caiu 25%."
        },
        {
            "title": "What, So What, Now What? (W3)",
            "icon": "❓",
            "detail": "Estrutura reflexiva simples para construir entendimento compartilhado e alinhar a ação baseada em observações conjuntas.",
            "examples": "Reunião de análise de resultados de sprint termina sem alinhamento sobre as ações futuras ou foco em problemas estruturais.",
            "execution": "<ol><li>\"O Quê?\": O que notamos? Quais foram os fatos?</li><li>\"E Daí?\": Qual a importância disso? Que padrões emergiram?</li><li>\"E Agora?\": Que ações vamos tomar com base nesse entendimento?</li></ol>",
            "result": "What: 'Tivemos 4 indisponibilidades no mês'. So What: 'Clientes estão ameaçando cancelar contratos, e a equipe está perdendo os finais de semana trabalhando'. Now What: 'Vamos pausar o desenvolvimento da Feature Y nesta sprint e dedicar 100% da capacidade para estabilizar o banco de dados'. Alinhamento claro sem busca de culpados."
        },
        {
            "title": "Min Specs",
            "icon": "📏",
            "detail": "Foca em definir apenas as especificações mínimas e absolutamente essenciais para a realização de uma tarefa ou projeto.",
            "examples": "Conflito entre Product Owners sobre o escopo excessivo de uma feature, gerando atrasos crônicos.",
            "execution": "<ol><li>Liste todas as especificações e requisitos propostos.</li><li>Desafie cada uma com a pergunta: \"Se quebrarmos ou removermos essa regra, ainda alcançamos o propósito principal?\".</li><li>Elimine todas as regras que não são absolutamente essenciais.</li></ol>",
            "result": "O compliance exigia um formulário de 40 páginas para aprovar novos fornecedores de TI. Usando Min Specs, reduzimos a lista apenas aos requisitos legais obrigatórios absolutos (apenas 5 perguntas: CNPJ, certidão negativa, dados bancários, LGPD). O tempo de aprovação de fornecedores caiu de 21 dias para 48 horas."
        },
        {
            "title": "Wicked Questions",
            "icon": "😈",
            "detail": "Técnica para trazer à tona paradoxos e desafios aparentemente insolúveis, encorajando o pensamento criativo e realista.",
            "examples": "A equipe precisa entregar código rápido para o cliente e, ao mesmo tempo, não criar dívida técnica.",
            "execution": "<ol><li>Apresente a estrutura da \"Pergunta Perversa\": \"Como podemos ser simultaneamente [A] e [B]?\"</li><li>Exemplo: \"Como podemos acelerar a entrega e, simultaneamente, reduzir a dívida técnica?\"</li><li>Estimule o grupo a explorar as respostas, sem tentar \"resolver\" um dos lados do paradoxo.</li></ol>",
            "result": "A pergunta foi: 'Como podemos encorajar a experimentação arriscada (falhar rápido) e ao mesmo tempo garantir a segurança de missão crítica para os usuários da UTI?'. A solução foi criar um ambiente de 'Chaos Engineering' simulado, onde devs podem destruir os serviços de forma controlada fora do horário de pico, alcançando ambos os lados."
        },
        {
            "title": "TRIZ",
            "icon": "🛠️",
            "detail": "Metodologia para resolução inventiva de problemas, focada em imaginar o pior cenário possível para encontrar soluções criativas.",
            "examples": "Equipe teme um colapso total da infraestrutura, mas não consegue priorizar preventivamente os riscos.",
            "execution": "<ol><li>Peça que o grupo faça uma lista detalhada de \"Como podemos garantir que a infraestrutura caia na próxima Black Friday?\".</li><li>Peça que classifiquem a probabilidade de cada item na lista ocorrer.</li><li>Para os itens prováveis, pergunte: \"Como podemos prevenir isso agora?\"</li></ol>",
            "result": "A equipe focou em 'Como garantir que nossos dados vazem com certeza?'. Listaram: 'Deixar a senha do banco no Github', 'Não usar 2FA', 'Dar acesso de admin para o suporte nível 1'. Perceberam que o acesso de admin do suporte nível 1 já estava ativo! Revogaram os acessos no mesmo dia, fechando uma brecha de segurança crítica."
        },
        {
            "title": "Heard, Seen, Respected (HSR)",
            "icon": "👂",
            "detail": "Prática focada em garantir empatia profunda entre pares através do compartilhamento de histórias pessoais de não se sentir ouvido.",
            "examples": "Membro da equipe desengaja por sentir que suas opiniões são constantemente ignoradas e reprimidas.",
            "execution": "<ol><li>Forme pares. Um fala (o cliente) e outro ouve ativamente (o consultor).</li><li>O cliente relata uma experiência em que se sentiu ignorado, não visto ou desrespeitado (3 min).</li><li>O ouvinte foca apenas em empatizar, sem julgar, diagnosticar ou dar conselhos.</li><li>Troquem de papéis.</li></ol>",
            "result": "O Product Manager, conhecido por ser frio, ouviu em silêncio por 3 minutos o Desenvolvedor contar como se sentiu desrespeitado quando seu código foi deletado sem aviso. O PM apenas agradeceu pela história e demonstrou empatia. No dia seguinte, o clima tóxico desapareceu e eles estavam brincando no café, trabalhando juntos como parceiros."
        },
        {
            "title": "Ecocycle Planning",
            "icon": "🌱",
            "detail": "Analisa o ciclo de vida das atividades de uma equipe (Gestação, Nascimento, Maturidade, Destruição Criativa) para balancear o portfólio.",
            "examples": "Equipe estagnada com projetos zumbis que não agregam valor e impedem a inovação, gerando atritos de prioridade.",
            "execution": "<ol><li>Introduza o conceito do ecociclo (com os 4 estágios principais e as duas armadilhas: Armadilha da Escassez e Armadilha da Rigidez).</li><li>Peça para cada um listar suas principais atividades e projetos.</li><li>Mapeie as atividades no gráfico do ecociclo.</li><li>Identifique as áreas de gargalo e defina ações para mover as atividades estagnadas.</li></ol>",
            "result": "Mapearam que o 'Portal Legado V1' estava na Armadilha da Rigidez (consumia muito tempo, pouco valor) e o 'Novo App Mobile' estava na Armadilha da Escassez (bom potencial, poucos recursos). A equipe concordou, de forma visual e sem brigas, em encerrar o Portal Legado e transferir os 3 desenvolvedores para o App Mobile no dia seguinte."
        },
        {
            "title": "Shift & Share",
            "icon": "🔄",
            "detail": "Estrutura para disseminar inovações e ideias rapidamente através de apresentações curtas e rotativas em pequenos grupos.",
            "examples": "Diversos times têm soluções inovadoras que não são compartilhadas, e acabam criando silos de informação e retrabalho.",
            "execution": "<ol><li>Defina \"Estações\" de apresentação com apresentadores diferentes.</li><li>Divida o grande grupo em equipes menores (cada uma visita uma estação).</li><li>O apresentador da estação compartilha sua inovação (ex: 7 a 10 min).</li><li>Após o tempo, as equipes rodam para a próxima estação.</li></ol>",
            "result": "Em 40 minutos, 5 equipes apresentaram suas ferramentas internas. O Time A descobriu que o Time C já havia criado um script de automação de testes E2E idêntico ao que eles passariam o próximo mês desenvolvendo do zero. Eles apenas clonaram o repositório do Time C, economizando 120 horas de trabalho de desenvolvimento."
        },
        {
            "title": "Critical Uncertainties",
            "icon": "🎲",
            "detail": "Planejamento de cenários futuros focando em duas incertezas críticas para testar a resiliência de estratégias atuais.",
            "examples": "Divergência intensa sobre o futuro do mercado de atuação da empresa, paralisando a alocação de recursos.",
            "execution": "<ol><li>Identifique as duas incertezas mais críticas e imprevisíveis.</li><li>Transforme cada incerteza em um eixo (x, y) com extremos opostos.</li><li>Crie uma matriz 2x2 e nomeie os quatro cenários resultantes.</li><li>Desenvolva estratégias robustas que funcionem em todos os cenários (ou na maioria deles).</li></ol>",
            "result": "A equipe mapeou os cenários para o aumento do dólar e novas leis regulatórias. Eles decidiram que a migração para infra nacional faria sentido em qualquer um dos 4 cenários futuros gerados, evitando brigas baseadas em previsões futuras e focando na robustez estratégica."
        },
        {
            "title": "Conversation Cafe",
            "icon": "☕",
            "detail": "Estrutura segura para conversas profundas sobre temas difíceis e polarizadores, com uso de objeto de fala para evitar interrupções.",
            "examples": "Desentendimento cultural grave após uma fusão corporativa com processos de demissão em andamento.",
            "execution": "<ol><li>Círculos pequenos (4-5 pessoas). Alguém traz um tema ou pergunta provocativa.</li><li>Rodada 1 (com objeto da palavra): Cada um expõe sua visão sobre o tema, sem debate.</li><li>Rodada 2 (com objeto): Cada um compartilha os sentimentos provocados pelas falas da rodada 1.</li><li>Rodada 3 (conversa aberta): Diálogo livre focado em entendimento profundo.</li></ol>",
            "result": "Em pequenos círculos com 5 pessoas, a equipe finalmente falou sobre os boatos de demissão após a fusão. O time de engenharia e os gestores conseguiram trocar percepções sem interrupções, esvaziando o pânico geral e gerando um documento colaborativo com as 10 principais dúvidas encaminhado ao CEO."
        },
        {
            "title": "User Story Mapping de Alinhamento",
            "icon": "🗺️",
            "detail": "Ferramenta visual de produto (Patton) usada para alinhar expectativas entre negócios e engenharia, evitando atritos de escopo oculto.",
            "examples": "Negócios exige 'o app inteiro', enquanto desenvolvimento diz que leva 1 ano. Conflito por falta de visão fatiada.",
            "execution": "<ol><li>Mapeie o fluxo de jornada do usuário (espinha dorsal).</li><li>Abaixo de cada passo, liste as atividades detalhadas em post-its.</li><li>Desenhe linhas horizontais ('slices') para fatiar as entregas em versões (MVP, V2, V3).</li><li>Negocie o que entra e o que sai da primeira linha horizontal.</li></ol>",
            "result": "O cliente pediu 'um sistema imobiliário completo'. A equipe mapeou a jornada e desenhou a primeira fatia horizontal apenas com 'cadastro manual e exibição de fotos'. O cliente concordou com a fatia em 30 minutos, resolvendo semanas de conflitos de escopo sobre integrações complexas de pagamento."
        },
        {
            "title": "Pre-mortem",
            "icon": "🔮",
            "detail": "Técnica de gerenciamento de riscos onde se assume que o projeto falhou espetacularmente antes de começar para antecipar desastres.",
            "examples": "Planejamento excessivamente otimista que esconde riscos estruturais cruciais, criando conflitos futuros.",
            "execution": "<ol><li>Imagine o projeto daqui a seis meses: \"Ele foi um fracasso épico\".</li><li>Peça que cada membro liste os motivos plausíveis para o fracasso.</li><li>Reúna os principais motivos e desenhe planos de contingência preventivos.</li></ol>",
            "result": "Antes da grande migração de dados, a equipe fez um pre-mortem. O arquiteto apontou: 'A base antiga tem encoding não padronizado, e as acentuações viraram lixo'. Como descobriram isso antes, inseriram um passo de sanitização prévia no pipeline, salvando a empresa de um desastre em produção."
        },
        {
            "title": "Retrospectiva Blameless",
            "icon": "🔍",
            "detail": "Foca na revisão de incidentes ou sprints assumindo que todos fizeram o melhor que podiam, dadas as informações e recursos no momento.",
            "examples": "Equipe com medo de assumir erros por cultura de punição, resultando em acobertamentos e atritos.",
            "execution": "<ol><li>Inicie lendo a Diretriz Primária ('Acreditamos que todos fizeram o melhor trabalho possível...').</li><li>Mapeie a cronologia do evento (o quê e quando aconteceu).</li><li>Explore os fatores contribuintes (ferramentas, processos, ambiente) sem focar nas pessoas.</li><li>Defina ações corretivas focadas no sistema.</li></ol>",
            "result": "Ao ler a Diretriz Primária, o DevOps junior finalmente teve coragem de dizer que derrubou o banco de dados porque o script não exigia confirmação. Em vez de punição, o time focou no processo sistêmico e alterou a configuração do script para pedir a flag --force, encerrando o clima de caça às bruxas."
        },
        {
            "title": "Sailboat para Resolução de Conflitos",
            "icon": "⛵",
            "detail": "Adaptação da retrospectiva do Barco à Vela, onde ventos, âncoras e rochas são usados como metáforas para identificar tensões de grupo.",
            "examples": "Sensação geral de estagnação e atrito, mas dificuldade em apontar exatamente o que está bloqueando a equipe.",
            "execution": "<ol><li>Desenhe um barco, ilha (objetivo), vento (propulsores), âncoras (pesos) e rochas (riscos).</li><li>Peça que a equipe coloque post-its na âncora representando atritos ou bloqueios relacionais.</li><li>Agrupe os itens da âncora e use os ventos (pontos fortes) para desenhar planos para 'içar' as âncoras.</li></ol>",
            "result": "Muitos post-its na âncora apontaram para 'Microgerenciamento das tarefas diárias'. A liderança visualizou o impacto destrutivo disso e usou o vento forte ('Boa comunicação síncrona do time') para substituir as cobranças diárias por revisões semanais de progresso, acelerando a equipe."
        },
        {
            "title": "Matriz de Impacto vs Esforço",
            "icon": "🎯",
            "detail": "Ferramenta clássica de priorização que mitiga embates baseados em 'achismos', trazendo a discussão para eixos concretos de valor e custo.",
            "examples": "Discussões circulares sobre qual tarefa o time deve executar primeiro em meio a um backlog infinito.",
            "execution": "<ol><li>Liste todas as demandas ou potenciais soluções.</li><li>Desenhe um gráfico: Eixo Y (Impacto Alto/Baixo) e Eixo X (Esforço Baixo/Alto).</li><li>Mapeie os itens no quadrante, debatendo brevemente seu impacto e custo relativos.</li><li>Ataque as \"Quick Wins\" (Alto Impacto / Baixo Esforço) e elimine os itens de baixo impacto / alto esforço.</li></ol>",
            "result": "A área de marketing exigia 15 melhorias no portal. A equipe plotou as 15 melhorias na matriz. Notaram que o recurso mais cobrado ('Design 3D na Home') daria 4 meses de esforço para baixo impacto. Ele foi imediatamente substituído pela 'Busca Otimizada' (esforço de 1 sprint, impacto direto nas vendas). Acabou a briga."
        },
        {
            "title": "Feedback Wrap",
            "icon": "🌯",
            "detail": "Uma técnica do Management 3.0 focada na estruturação empática e construtiva de um feedback para evitar posturas defensivas e agressivas.",
            "examples": "Membro que apresenta comportamentos disruptivos reage com hostilidade a qualquer tentativa de feedback informal.",
            "execution": "<ol><li>Descreva seu contexto: prepare o terreno para o outro entender de onde você fala.</li><li>Descreva as suas observações: cite dados e fatos neutros, sem acusações.</li><li>Descreva os seus sentimentos: expresse o impacto emocional da ação em você.</li><li>Explique seu valor e sugestão: fale de suas necessidades e sugira melhoria.</li></ol>",
            "result": "Contexto: 'Estou focado na estabilidade da nossa pipeline hoje.' Observação: 'Vi que seus últimos 3 commits não compilaram.' Sentimento: 'Fiquei frustrado pois tive que parar meu fluxo para investigar.' Valor: 'Valorizo nosso tempo; sugiro rodar a suíte local antes de enviar.' O colega pediu desculpas em vez de se defender e passou a testar localmente."
        },
        {
            "title": "Delegation Poker",
            "icon": "🃏",
            "detail": "Técnica Management 3.0 para alinhar claramente a distribuição de autoridade, esclarecendo quem decide o que, do nível 1 (Dizer) ao 7 (Delegar).",
            "examples": "Tensão porque os líderes praticam micro-gerenciamento, mas cobram 'autonomia' do time, sem limites claros de decisão.",
            "execution": "<ol><li>Apresente uma área de decisão (ex: ferramentas de desenvolvimento).</li><li>Todos jogam uma carta com o nível de delegação desejado (1 a 7).</li><li>Debatam as diferenças até entrarem num consenso do nível adequado de autonomia para a tarefa.</li><li>Registre a decisão num quadro (Delegation Board).</li></ol>",
            "result": "Para a decisão 'Escolher bibliotecas JS do front-end', a gerente jogou 3 (Consultar) e o tech lead jogou 6 (Perguntar). O consenso foi o 5 (Aconselhar): o tech lead tem autonomia total para escolher a biblioteca, mas deve aconselhar a gerente antes da implementação para alinhar orçamento. Conflito de autoridade resolvido."
        }
    ]
};