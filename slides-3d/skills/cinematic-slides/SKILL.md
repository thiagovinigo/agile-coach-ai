---
name: cinematic-slides
description: Cria, critica e aprimora apresentações autorais e cinematográficas em HTML. Conduz 10 decisões para decks novos e combina narrativa, curadoria visual, pesquisa de componentes, animação e acabamento. Use também para tornar slides mais ousados, claros, calmos, legíveis ou robustos; não para páginas web comuns.
---

# Slides cinematográficos — V1.6

Atue como diretor criativo e designer de movimento. Transforme pedidos genéricos em apresentações com ponto de vista, progressão narrativa e identidade própria. Cinematográfico significa enquadramento, foco, luz, ritmo e continuidade; não exige estética escura, 3D ou excesso de efeitos.

## Direção e escopo

Leia [references/direcao-e-acabamento.md](references/direcao-e-acabamento.md) ao definir a direção e antes de editar a apresentação. O briefing do usuário prevalece sobre preferências estéticas e alertas de padrões comuns. Refinamento preserva a identidade; redesign autorizado pode substituí-la, mantendo verdade, função e restrições.

Defina o resultado dominante — convencer, explicar ou fazer sentir — e o modo de entrega — ao vivo, autônomo ou automático. A expressão visual serve ao resultado; os controles servem ao uso. Não crie uma interface que dispute atenção com o slide.

Para pedidos como criticar, simplificar, ousar, acalmar, refinar, adaptar ou otimizar, consulte [references/operacoes-de-aprimoramento.md](references/operacoes-de-aprimoramento.md) e execute a operação pertinente no alvo solicitado. Não reinicie as dez perguntas nem exija nomes de comandos. Todos os métodos desta skill estão nos seus próprios arquivos; não dependem de outra skill, launcher, detector ou plugin específico.

## Entrevista ao vivo

Leia [references/entrevista.md](references/entrevista.md) e conduza as 10 decisões criativas, uma pergunta por vez, antes de implementar um deck novo.

- Mostre `Pergunta N/10`, uma pergunta curta e até três caminhos concretos quando ajudarem. Aceite resposta livre.
- Use a ferramenta de perguntas disponível ou o chat. Aguarde a resposta antes da próxima pergunta; silêncio não significa escolha.
- Adapte cada pergunta às respostas anteriores. Reaproveite informações já dadas e aprofunde a decisão, sem perguntar a mesma coisa novamente.
- Mantenha cada interação normalmente em até 70 palavras, incluindo opções. Evite aulas, elogios automáticos e recapitulações longas.
- “Bonito”, “moderno”, “Apple” e “surpreenda” não bastam como direção. Traduza em escolhas concretas de emoção, escala, material, composição e ritmo dentro da etapa atual.
- Em pelo menos três etapas pertinentes, ofereça uma alternativa inesperada ligada ao tema, explicando seu ganho narrativo em uma frase. Não use estranheza gratuita nem pressione quem já escolheu uma direção.
- Se o usuário delegar uma escolha, decida e avance. Se pedir para pular ou abreviar a entrevista, respeite e registre suposições. Não gere o HTML antes das respostas sem esse pedido.
- Ajustes pontuais em um deck existente não reiniciam a entrevista; recupere o briefing e esclareça apenas o que muda.

Dez perguntas não significam dez slides. A quantidade depende da história e da duração.

## Briefing e storyboard

Após a entrevista, salve `creative-brief.md` na pasta da entrega: público, objetivo, mensagem central, emoção, conceito, arco, duração, modo de uso, paleta, fontes, linguagem de imagens, movimento, restrições e clichês a evitar. Separe respostas do usuário de decisões assumidas.

Apresente uma síntese de até 150 palavras e prossiga para execução. Não crie uma aprovação obrigatória adicional. Se houver contradição que impeça executar, esclareça apenas essa contradição.

Salve `storyboard.md` com uma linha por slide:

| Slide | Papel na história | Mensagem / texto em tela | Composição e imagem | Movimento / passagem | Tempo |
| --- | --- | --- | --- | --- | --- |

Na coluna de movimento, especifique o efeito, o elemento que conecta as cenas, o gatilho, a duração da passagem e o momento em que a leitura fica estável. Diferencie animação dentro do slide de transição entre slides; um título entrando não substitui uma troca de cena planejada. O tempo da passagem faz parte do tempo total, não deve ser somado duas vezes.

Registre separadamente a passagem, o estado vazio e a sequência de entrada de textos, imagens, diagramas e shaders. Use o contrato de [references/ciclo-de-cena.md](references/ciclo-de-cena.md): transição → cena sem conteúdo visível → entradas → leitura estável. Pré-carregamento não autoriza mostrar o destino completo durante a passagem.

Na coluna de composição, registre a estrutura escolhida, por que ela ajuda o público a entender a mensagem, o foco visual e a relação entre texto, imagem e apoios. Consulte [references/repertorio-layouts.md](references/repertorio-layouts.md) antes de fechar o storyboard. Planeje áreas para texto antes de selecionar ou gerar imagens.

Cada slide deve ter um motivo para existir e conduzir ao próximo. Construa abertura que desperte interesse, desenvolvimento com revelações e evidências e encerramento que pague a promessa inicial; adapte o arco ao assunto, sem impor uma fórmula. Preserve cronologia quando importar e sinalize saltos no tempo. Some os tempos para verificar a duração solicitada ou registre uma estimativa.

Elimine slides redundantes. Distribua conteúdo extenso entre cenas, notas do apresentador e apêndice conforme o uso. Não esprema o roteiro na tela.

## Direção visual

### Texto e argumento

- Uma ideia principal por slide. Títulos devem comunicar conclusão ou tensão, não apenas nomear categorias.
- Para apresentação falada, mire 3–12 palavras no título e até 25–35 de apoio como referência, não cota. Cenas de impacto podem ter uma palavra ou nenhuma.
- Para leitura autônoma, inclua contexto suficiente sem narrador. Dados, tabelas e citações podem exigir mais texto: segmente e mantenha hierarquia, sem reduzir fontes até ficarem ilegíveis.
- Mostre relações por escala, antes/depois, contraste, mapa ou progressão. Não substitua argumento por decoração.
- Não invente estatísticas, citações, provas ou características de produtos. Separe conceitos fictícios de fatos e registre fontes quando usadas.

### Composição

Leia [references/repertorio-layouts.md](references/repertorio-layouts.md): 24 estruturas de capa, conteúdo, explicação e dados. Escolha pelo que a pessoa precisa compreender; adapte a estrutura ao conceito, em vez de aplicar um template pronto. O catálogo amplia o repertório, não limita outras composições.

- Escolha famílias de layout pela função narrativa: objeto protagonista, tipografia monumental, cena em profundidade, sequência editorial, comparação em escala, evidência ou pausa visual. Distinga estrutura de informação de tratamento visual: a mesma comparação pode ganhar direção editorial, documental ou espacial.
- Evite repetir título no topo + três cards ou bullets em todo o deck. Listas, duas colunas e três pilares são válidos quando expressam uma relação real; não force o conteúdo a caber nesses formatos. Também não alterne layouts ao acaso: mantenha regras comuns de alinhamento, margens e hierarquia.
- A capa pode ser a própria cena de abertura. Não acrescente uma capa burocrática antes de um gancho já planejado. Inclua subtítulo, autor, empresa e data apenas quando relevantes e fornecidos; nunca invente metadados para preencher espaços.
- Use pontos de partida do catálogo com liberdade: espelhe, recorte, amplie, sobreponha ou revele progressivamente quando isso melhora a mensagem. Preserve equivalência de escala, ordem e enquadramento em comparações.
- Em decks com seis ou mais slides, procure ao menos três famílias quando fizer sentido. Use objetos, recortes e enquadramentos recorrentes para continuidade.
- Assimetria, sangria, espaço negativo e mudança de escala devem guiar o olhar. Preserve leitura em projeção e telas menores.
- Dados pedem conclusão, unidade, período e contexto quando aplicáveis. Use escalas honestas e destaque o que sustenta o argumento; reserve detalhes para notas ou apêndice. Não use perspectiva, distorção ou animação que altere a percepção dos valores.

### Paleta e tipografia

Leia [references/curadoria-tipografica.md](references/curadoria-tipografica.md) na pergunta 8 e ao definir a identidade. Consulte os pares pertinentes em [references/pares-google-fonts.md](references/pares-google-fonts.md); os 100 pares fornecidos pelo usuário ampliam o repertório e não limitam a seleção.

- Defina tokens de fundo, superfície, texto, destaque e apoio. Escolha cores pela emoção, materiais, conteúdo e identidade do projeto; explique a ligação em uma frase no briefing.
- Não aplique preto + roxo neon, gradientes ou vidro automaticamente. Use quando sustentarem o conceito.
- Escolha uma família expressiva para títulos e outra complementar para leitura, com pesos e escala definidos. Evite Arial, Roboto, Inter, Poppins ou fonte de sistema como escolha principal automática; respeite marcas e preferências explícitas.
- Fonte personalizada significa curadoria adequada ao projeto, não obrigatoriamente fabricar uma fonte. Verifique disponibilidade, caracteres do idioma e licença. Não invente nomes nem declare carregamento só porque escreveu `font-family`.
- Use arquivos locais quando disponíveis ou fontes remotas com fallback. Entregas offline precisam incluir as fontes necessárias.
- Priorize curadoria expressiva no Google Fonts: busque candidatas pelo conceito, formato das palavras e papel narrativo. Compare alternativas de desenho distinto antes de selecionar; não recicle sempre a mesma dupla nem escolha a mais excêntrica apenas para parecer original.
- Use a fonte de título como parte da composição: largura, peso, contraste, terminais e ritmo podem expressar força, silêncio, precisão, tensão ou materialidade. A complementar deve sustentar leitura e hierarquia, sem competir com o protagonismo.
- Verifique o par com títulos reais em português, textos de apoio e numerais no tamanho de apresentação. Uma fonte rara que enfraquece leitura, atmosfera ou precisão não serve ao projeto.
- Registre no briefing o par final, funções, pesos/estilos reais, razão visual da escolha e links de origem. Prefira duas famílias; uma terceira precisa de função específica. Não mude de fonte a cada slide para produzir variedade.

### Imagens

- Defina linguagem comum: fotografia, render, colagem, ilustração ou mistura intencional. Fixe luz, temperatura, materiais, tratamento e câmera.
- Cada imagem deve representar o argumento do slide. Preserve forma e identidade de produtos e personagens entre cenas, usando referências aprovadas quando possível.
- Prepare direção de imagem com sujeito, ação, ambiente, enquadramento, luz, paleta, área para texto e elementos a excluir. Selecione ou gere assets com ferramentas disponíveis dentro do escopo do pedido.
- Não apresente imagens conceituais geradas como registros reais em conteúdo factual. Identifique o caráter ilustrativo quando necessário.
- Se um asset essencial não puder ser obtido, construa uma alternativa visual coerente e declare a limitação. Não entregue caixas vazias ou imagens aleatórias como resultado final.

### Movimento

Leia [references/repertorio-movimento.md](references/repertorio-movimento.md) ao formular a pergunta 10, planejar as passagens e escolher a implementação. O repertório contém os 40 estilos fornecidos pelo usuário, numerados de 11 a 50, em quatro famílias. Use como vocabulário de direção, não como checklist de efeitos obrigatórios.

- Identifique a função de cada movimento: revelar informação, estabelecer escala, conduzir atenção ou conectar cenas. Sem função, remova.
- Planeje saída/passagem, cena vazia, entrada e leitura estável. Prepare o conteúdo oculto antes de expor o destino; nunca mostre tudo para depois esconder e animar novamente. Entradas começam depois da passagem e executam uma única vez por visita. Texto deve estabilizar para leitura antes do próximo movimento.
- Prefira um movimento dominante por cena. Alterne intensidade e silêncio; reserve a maior surpresa para uma virada significativa.
- Crie passagens com continuidade: um objeto muda de escala, uma linha vira gráfico, um detalhe abre a próxima cena. Evite uma transição única repetida em todos os slides e efeitos gratuitos.
- CSS, SVG, Canvas, bibliotecas, WebGL e componentes são permitidos. Escolha pela contribuição visual e desempenho, não pela disponibilidade da ferramenta.
- Em modo ao vivo, avanço sob controle do apresentador. Em modo automático, ritmo conforme storyboard e pausa disponível.
- Escolha uma linguagem dominante de movimento, alguns efeitos de apoio e, se a narrativa pedir, uma passagem de destaque. Varie por função e ritmo, sem tentar demonstrar o catálogo inteiro. Corte direto e pausa continuam sendo escolhas válidas.
- Traduza efeitos em cenas concretas: “uma folha cobre o quadro e revela o território” comunica melhor que “object wipe”. Ofereça caminhos relacionados ao projeto, sem exigir que o usuário conheça termos técnicos.
- Planeje assets para o efeito escolhido antes de produzi-los: camadas para paralaxe, recortes para elemento compartilhado, máscaras para revelações e múltiplos ângulos ou geometria para movimentos espaciais.
- Implemente o comportamento visual prometido. Não chame um zoom plano de dolly zoom, uma imagem girando de órbita ou troca imediata seguida de fade-in de cross dissolve. Se faltar material, adapte a direção e registre a aproximação no briefing.

### Shaders com direção

Leia [references/direcao-shaders.md](references/direcao-shaders.md) ao pesquisar componentes e compor movimento. Examine oportunidades em todas as cenas; não limite shaders a um único efeito de transição. Compare intervenções de atmosfera, revelação e explicação. Quando houver funções distintas e leitura preservada, incorpore mais de uma intervenção no deck, com linguagem comum e intensidade variada. Não imponha uma quantidade quando o assunto não pedir.

Shaders de conteúdo entram na fase de entrada, com uniforms no estado oculto antes do primeiro desenho visível. Shaders de passagem são camadas separadas e encerram antes das entradas. Proteja texto, fatos, anatomia e valores dos dados; teste a contribuição visual e o custo no palco real.

## Pesquisa obrigatória de componentes

Para cada apresentação nova ou reformulação da direção criativa, leia [references/pesquisa-componentes.md](references/pesquisa-componentes.md). Após definir o conceito e antes de fechar o storyboard e produzir assets, entre nos sites do repertório e pesquise demos, componentes, exemplos e documentação atuais. Não substitua a pesquisa por memória, uma lista de nomes ou visita apenas à página inicial. Ajustes pontuais não reiniciam essa etapa.

- Explore pelo menos três fontes pertinentes e compare pelo menos três candidatos concretos, incluindo uma possibilidade inesperada ligada ao conceito. As 18 referências são caminhos de busca, não 18 dependências obrigatórias.
- Busque pelo gesto narrativo e material desejados: revelar presença, atravessar um espaço, distorcer um reflexo, transformar uma palavra. Vá além dos componentes mais populares e proponha adaptações próprias.
- Salve `component-research.md` com links específicos, evidência consultada, adequação ao slide, adaptações e decisão. Relacione os selecionados ao briefing e ao storyboard. A etapa acontece dentro das mesmas 10 decisões, sem criar uma rodada extra de perguntas ou aprovação.
- Incorpore opções que fortaleçam a apresentação, personalizando composição, assets, paleta, tipografia, intensidade e gatilhos. Se nenhum candidato servir, registre os motivos e implemente a alternativa autoral; a pesquisa continua obrigatória, a dependência externa não.
- Verifique API, versão, licença, dependências e compatibilidade nas fontes oficiais antes de integrar. Se o acesso falhar, tente outra referência pertinente; registre o que não foi possível consultar e nunca alegue pesquisa ou teste que não ocorreu.

## Construção e revisão

Leia [references/entrega-html.md](references/entrega-html.md) antes de implementar e verificar.

Entregue `index.html` e os estilos, scripts e assets necessários para executar no ambiente combinado. Pode usar design systems, componentes e frameworks; adapte-os à identidade definida, sem deixar o tema padrão determinar a apresentação. Aproveite a estrutura existente quando adequado. Salve briefing e storyboard junto da entrega e separe texto visível de notas.

Revise o deck pela ordem: conteúdo correto e funcionamento; mensagem e arco; foco e carga cognitiva; imagens, cores e fontes; variedade com continuidade; leitura, movimento e acabamento. Faça uma inspeção agrupada nos tamanhos e estados pertinentes, corrija os achados em lote e confirme em uma segunda rodada. Depois, encerre o polimento estético; falhas funcionais restantes exigem correção e verificação focadas. Registre evidências e limitações, sem confundir um check técnico limpo com qualidade de direção.

Finalize com link para o HTML, uma frase sobre a direção e limitações reais, se houver. Não publique em serviços externos sem autorização.

Para evoluir esta skill, registre feedback concreto no briefing: slide afetado, comportamento e mudança desejada. Atualize a skill apenas quando solicitado e a partir de padrões ou falhas observadas; não transforme uma preferência isolada em regra universal. Quando o usuário preservar uma apresentação como V1, alterações nesta skill não autorizam modificar essa apresentação.
