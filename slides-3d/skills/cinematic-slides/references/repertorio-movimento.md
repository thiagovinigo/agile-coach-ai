# Repertório de movimento — estilos 11 a 50

Os números preservam a lista fornecida pelo usuário; não implicam que existam estilos 1 a 10 definidos nesta skill. Selecione pela história, pela identidade e pelos assets disponíveis. As famílias agrupam usos; alguns efeitos podem atuar tanto dentro de uma cena quanto entre cenas.

## Como dirigir uma passagem

Todos os estilos obedecem a [ciclo-de-cena.md](ciclo-de-cena.md): a passagem revela a superfície de destino, que permanece sem conteúdo visível até começar a entrada dos itens. Adapte exemplos de demos que mostram o próximo slide completo; não reproduza esse comportamento. Elementos compartilhados de conteúdo exigem outra conexão se anteciparem a entrada. Para usos de shaders além de passagens, consulte [direcao-shaders.md](direcao-shaders.md).

Para cada passagem significativa, registre no storyboard:

`origem → destino | efeito | elemento/âncora | função narrativa | gatilho | duração + curva de movimento | estado final de leitura | alternativa com movimento reduzido`

Exemplo: `floresta → território | object wipe | folha em primeiro plano | revelar o espaço percorrido | próximo slide | 900 ms, acelera e desacelera | mapa inteiro legível | corte direto`.

A duração depende da sensação: passagens funcionais podem ocupar aproximadamente 250–600 ms, conexões com continuidade 600–1200 ms e revelações contemplativas 1–2,5 s. São pontos de partida, não limites obrigatórios. O intervalo de leitura deve permanecer sob controle do apresentador no modo ao vivo. Dê nome ao movimento dominante e use detalhes de apoio sem competir com ele.

## Trocas de cena e revelações

| Nº | Estilo | Comportamento e uso narrativo | Implementação / condição |
| --- | --- | --- | --- |
| 11 | **Cross dissolve · Fusão** | A cena anterior perde presença enquanto a próxima surge sobreposta. Liga momentos próximos, passagem do tempo e pausas. | Duas cenas sobrepostas, opacidades coordenadas. Evite texto duplo ilegível no meio; títulos podem sair antes da mistura. |
| 12 | **Push · Empurrão** | A nova cena desliza e desloca a anterior para fora. Expressa avanço, sequência ou oposição. | Transformações sincronizadas em dois painéis, palco recortado; direção coerente ao voltar. |
| 13 | **Wipe · Varredura** | Uma borda revela a próxima cena sem deslocar as imagens. Útil para comparar e revelar um novo estado. | Máscara ou clip-path animado sobre o destino; a cena de origem permanece embaixo. |
| 14 | **Iris · Abertura circular** | Um círculo abre ou fecha sobre um ponto escolhido. Direciona atenção para olho, lente ou detalhe. | Máscara circular com centro ancorado no objeto, raio suficiente para cobrir os cantos do palco. |
| 15 | **Clock wipe · Varredura radial** | Um setor gira e revela a cena como um ponteiro. Pode representar ciclo, tempo ou varredura. | Máscara radial/setor SVG ou Canvas; não basta girar a imagem completa. |
| 16 | **Blinds · Persianas** | Faixas paralelas abrem ou fecham. Serve a temas modulares, arquitetônicos ou mecânicos. | Máscara de faixas com aberturas coordenadas; preserve alinhamento da imagem contínua. Evite aparência de preset sem vínculo com o tema. |
| 17 | **Split · Abertura dividida** | Duas partes se afastam e revelam o conteúdo atrás. Materializa separação ou descoberta. | Dois recortes alinhados da origem, deslocamentos opostos, destino sob eles. |
| 18 | **Object wipe · Passagem de objeto** | Um objeto cruza e cobre o quadro; a próxima cena surge atrás dele. Une ambientes por uma ação material. | Objeto de primeiro plano ou silhueta coerente, com área de cobertura suficiente; troque o fundo no momento de oclusão. |
| 19 | **Luma wipe · Revelação por luminosidade** | A luminância de uma máscara determina quais regiões revelam primeiro. Funciona com luz, névoa e textura. | Máscara com limiar de luminância animado, por shader/Canvas ou composição equivalente. Um simples fade de camada branca não produz esse efeito. |
| 20 | **Ink reveal · Revelação por tinta** | Manchas se expandem organicamente e revelam conteúdo. Combina com arte, matéria, memória ou linguagem editorial. | Máscara orgânica animada, textura adequada ou contornos SVG. Evite aplicá-la a fotografia naturalista sem motivação. |

## Câmera, profundidade e espaço

| Nº | Estilo | Comportamento e uso narrativo | Implementação / condição |
| --- | --- | --- | --- |
| 21 | **Parallax · Paralaxe** | Camadas se deslocam em velocidades diferentes. Revela profundidade e relações entre planos. | Primeiro plano, protagonista e fundo independentes, com bordas excedentes para não abrir lacunas; movimento suave, não dependente apenas do mouse. |
| 22 | **Whip pan · Chicote de câmera** | Varredura lateral rápida com borrão liga cenas. Pontua ação ou deslocamento brusco. | Translação e desfoque breves coordenados entre origem e destino; estabilize antes de ler. Reserve para viradas. |
| 23 | **Dolly zoom · Efeito vertigem** | A câmera se desloca enquanto o campo de visão compensa, preservando o tamanho do sujeito e alterando o fundo. Cria tensão ou mudança de percepção. | Cena 3D ou camadas com simulação de perspectiva deliberada. Escalar uma foto inteira não é dolly zoom; identifique uma aproximação em 2,5D como simulação. |
| 24 | **Orbit · Órbita** | A câmera circula ao redor do objeto e mostra outros lados. Revela forma, volume ou contexto. | Geometria 3D ou sequência consistente de múltiplos ângulos. Rotacionar uma foto plana não revela lados novos. |
| 25 | **Fly-through · Travessia** | A câmera atravessa espaço ou planos e termina na próxima cena. Faz o público entrar num ambiente. | Espaço 3D ou planos em profundidade com oclusão, escala e continuidade; um zoom isolado não equivale a atravessar o espaço. |
| 26 | **Match cut · Corte por semelhança** | Um corte conecta formas, posições, cores ou ações equivalentes. Cria associação ou continuidade instantânea. | Prepare enquadramentos e âncora em posições compatíveis; pode ser corte direto, sem interpolação. |
| 27 | **Cube rotation · Rotação de cubo** | Uma face sai enquanto outra chega por rotação. Representa mudança de lado ou dimensão. | Faces em perspectiva, eixos e origem coerentes; mantenha o texto estável ao terminar. |
| 28 | **Carousel 3D · Carrossel tridimensional** | Painéis giram ao redor de um eixo, um se aproxima e os outros recuam. Organiza opções ou vistas de uma coleção. | Profundidade e oclusão consistentes, painel ativo acessível; não use rotação permanente durante a leitura. |
| 29 | **Page turn · Virada de página** | Uma página dobra e vira, revelando a seguinte. Evoca documento, arquivo ou memória. | Dobra/curvatura e sombra coerentes. Uma dobradiça plana é uma versão simplificada, não uma simulação completa de papel. |
| 30 | **Card stack · Pilha de cartões** | Cartões sobrepostos se reorganizam e revelam o próximo. Serve a registros, etapas ou evidências. | Ordenação de camadas, sombras discretas e trajetória legível. Use quando a metáfora de cartões fizer sentido. |

## Transformações e distorções

| Nº | Estilo | Comportamento e uso narrativo | Implementação / condição |
| --- | --- | --- | --- |
| 31 | **Shape morph · Transformação de forma** | Um contorno se transforma gradualmente em outro. Explica relações, evolução ou uma metáfora. | Formas com correspondência de pontos/path ou interpolação adequada. Crossfade de duas formas não é morph. |
| 32 | **Shared element · Elemento compartilhado** | O mesmo objeto mantém identidade enquanto muda de tamanho e posição entre composições. Liga cenas por continuidade. | Use um motivo de ligação separado do conteúdo de destino. Se o objeto for conteúdo, reserve sua transformação para a entrada após a passagem; não o revele antes e reinicie depois. |
| 33 | **Squash and stretch · Compressão e alongamento** | O elemento se comprime e estica para sugerir massa ou elasticidade. Combina com materiais flexíveis ou linguagem lúdica. | Escalas coordenadas e ponto de apoio, preservando volume aparente quando pertinente. Não deforme animais, rostos ou produtos rígidos em apresentações realistas. |
| 34 | **Wave · Ondulação** | Deformação em ondas atravessa a superfície. Sugere vibração, água ou instabilidade. | Deslocamento espacial com filtro, malha ou shader; mexer a imagem inteira lateralmente não a deforma. |
| 35 | **Ripple · Ondas circulares** | Ondas partem de um ponto como uma gota. Mostra propagação ou impacto. | Centro definido e deslocamento radial; círculos decorativos podem ilustrar propagação, mas não são distorção da imagem. |
| 36 | **Twirl · Redemoinho** | A imagem se torce ao redor de um centro. Pode representar mudança radical ou fantasia. | Deformação angular dependente do raio; girar o painel todo é rotação, não torção. |
| 37 | **Liquid distortion · Distorção líquida** | A superfície muda de forma fluidamente. Combina com materiais líquidos ou transformação sensorial. | Campo de deslocamento suave por filtro/malha/shader; limite deformação sobre sujeitos que precisam manter identidade. |
| 38 | **Pixelate · Pixelização** | A imagem se divide em blocos e se reconstrói. Serve a resolução, dados ou passagem digital. | Controle progressivo do tamanho dos blocos e reconstrução do destino. Um desfoque não é pixelização. |
| 39 | **Glitch · Falha digital** | Fragmentos, cortes e deslocamentos produzem uma falha breve. Comunica ruptura ou erro tecnológico. | Recortes e deslocamentos controlados, duração curta, sem afetar leitura estável. Não use como textura contínua por padrão. |
| 40 | **Particle dissolve · Dissolução em partículas** | O conteúdo se desfaz em partículas ou elas formam o destino. Evoca dispersão, composição ou matéria. | Partículas derivadas da silhueta/imagem ou de uma forma representativa; orçamento de partículas e encerramento do loop. Pontos sobre um fade genérico não equivalem à dissolução. |

## Texto, luz e acabamento

| Nº | Estilo | Comportamento e uso narrativo | Implementação / condição |
| --- | --- | --- | --- |
| 41 | **Typewriter · Digitação** | Texto aparece caractere por caractere. Evoca descoberta, registro ou mensagem. | Use em frases curtas, preserve acentos/grupos de caracteres e quebras de linha. Ofereça conteúdo completo acessível sem anunciar cada letra; não atrase parágrafos longos. |
| 42 | **Stagger · Animação em sequência** | Elementos começam com atrasos pequenos. Estabelece ordem e hierarquia. | Ordem de início segue a leitura ou narrativa; controle duração total, evitando uma fila longa de palavras. |
| 43 | **Scramble text · Letras embaralhadas** | Caracteres mudam até formar o texto final. Sugere decodificação ou descoberta digital. | Texto final disponível à acessibilidade, largura reservada para evitar saltos, efeito curto. Não aplique a conteúdo que precisa ser lido imediatamente. |
| 44 | **Draw-on · Desenho progressivo** | Linhas e contornos aparecem como um traço. Explica percursos, mapas e construção de ideias. | Comprimento do path e desenho progressivo; rótulos aparecem em ordem lógica, diagrama completo permanece no estado final. |
| 45 | **Text tracking · Espaçamento animado** | Espaço entre letras muda até chegar à composição. Concentra ou expande uma palavra. | Use em títulos curtos com espaço reservado; evite reflow e quebras variáveis durante o efeito. |
| 46 | **Blur transition · Transição por desfoque** | A cena perde foco, troca conteúdo e recupera nitidez. Liga percepção, lembrança ou mudança de atenção. | Desfoque controlado, troca no ponto adequado, destino totalmente nítido antes de leitura. Avalie custo em palco inteiro. |
| 47 | **Light sweep · Varredura de luz** | Uma faixa de luz percorre a superfície. Destaca material, volume ou um detalhe. | Camada de luz recortada ao elemento, brilho com contraste suficiente; evite brilho indiscriminado sobre todos os textos. |
| 48 | **Flash transition · Transição por clarão** | Um clarão cobre a troca. Pontua impacto, câmera ou ruptura. | Clarão isolado e breve, sem séries de flashes/estrobos. Com movimento reduzido, substitua por corte ou fusão discreta. |
| 49 | **RGB split · Separação de cores** | Canais de cor se deslocam e depois se alinham. Sugere falha, sinal ou intensidade digital. | Cópias/canais coordenados e retorno exato ao alinhamento. Não mantenha franjas sobre texto em leitura. |
| 50 | **Motion trail · Rastro de movimento** | Cópias semitransparentes acompanham o deslocamento e desaparecem. Evidencia direção e velocidade percebida. | Histórico breve de posições ou ecos visuais, com limpeza das cópias no fim. Não deixe rastros ocultarem conteúdo ou falsearem uma medição. |

## Escolha e coerência

- **Intimidade naturalista:** fusão, elemento compartilhado, paralaxe contida, passagem por objeto e desenho de pistas costumam sustentar o tom. Não são um pacote obrigatório.
- **Ação e potência:** um whip pan ou rastro breve pode pontuar uma virada entre momentos calmos, se os assets sustentarem a passagem.
- **Editorial e arquivo:** match cut, ink reveal, page turn ou card stack podem transformar a própria matéria da história em transição.
- **Tecnologia e ruptura:** glitch, pixelate, scramble ou RGB split precisam comunicar uma intenção, não apenas sinalizar modernidade.
- **Transformação material:** morph, ripple e distorção líquida pedem ligação com o que muda; não deforme o protagonista só para exibir técnica.

Evite quotas de estilos, efeitos aleatórios a cada clique e empilhamento de câmera, distorção, luz e texto no mesmo instante. Repetições deliberadas podem criar uma assinatura, mas não devem transformar todas as trocas num único preset automático. Use movimento reduzido como outra direção válida que preserva a narrativa e o conteúdo.
