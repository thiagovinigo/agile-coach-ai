# Pesquisa e adaptação de componentes

## Etapa obrigatória por apresentação

Pesquise depois de compreender conceito, uso e limites de movimento, antes de fechar o storyboard e gerar assets. Pode antecipar a busca durante as perguntas 8–10 para informar alternativas. Reutilize respostas anteriores quando solicitado; pesquisar componentes não exige repetir a entrevista.

1. Traduza a direção em gestos e materiais concretos: camadas de folhagem, reflexo na água, luz atravessando vidro, palavra que vira forma, distância que revela escala. Identifique cenas que ganhariam com isso.
2. Escolha pelo menos três fontes pertinentes do catálogo. Consulte páginas específicas de exemplos, demos, documentação ou código; resultados de busca e homepages servem para descoberta, não bastam para avaliar um componente. Amplie a busca se as primeiras opções forem genéricas ou não servirem ao conceito.
3. Compare pelo menos três candidatos concretos. Inclua uma hipótese menos óbvia e descreva sua adaptação ao tema. Não invente nomes de componentes nem infira comportamento só pelo título da demo. Quando possível, observe a demo em movimento; distinga leitura de código/documentação de observação visual.
4. Selecione pela contribuição narrativa, controle de ritmo, legibilidade, compatibilidade e custo. Experimente o candidato mais promissor no palco real antes de espalhá-lo pelo deck. Não acrescente bibliotecas apenas para cumprir quantidade.
5. Salve a pesquisa e vincule as escolhas às cenas. Personalize e valide a integração. Se a opção falhar, experimente outra candidata ou uma implementação autoral que preserve o gesto; registre a troca sem fingir que usou a biblioteca.

Mapeie também shaders dentro dos slides, conforme [direcao-shaders.md](direcao-shaders.md): atmosfera, revelação e explicação, além de transições. Não pare no primeiro efeito incorporado quando outras cenas tenham oportunidades pertinentes.

## Catálogo — 21 referências oficiais

Os links são pontos de entrada oficiais. Capacidades, APIs, integrações, requisitos e licenças devem ser confirmados na versão consultada. Não trate descrição do catálogo como garantia de compatibilidade.

### Modelos 3D, Assets Espaciais & Cenas Interativas

| Referência | O que procurar | Adaptação ao slide |
| --- | --- | --- |
| [Sketchfab](https://sketchfab.com/) · [Viewer API](https://sketchfab.com/developers/viewer) | Maior repositório mundial de modelos 3D em formato GLTF/GLB, texturas PBR, animações e API de visualização web. | Objeto protagonista 3D (naves, produtos industriais, gadgets, arquitetura, anatomia, esculturas). Baixar assets GLB otimizados com licença Creative Commons para carregar via Three.js `GLTFLoader`, ou incorporar diretamente no slide via Sketchfab Viewer API controlando câmera, anotações e animação via JavaScript. |

### Efeitos e componentes para adaptar

| Referência | O que procurar | Adaptação ao slide |
| --- | --- | --- |
| [React Bits](https://reactbits.dev/) · [código](https://github.com/DavidHDev/react-bits) | Texto animado, fundos, componentes interativos e microinterações. | Títulos e capas com gesto próprio; adaptar ao avanço do apresentador e à tipografia escolhida. |
| [Paper Shaders](https://shaders.paper.design/) · [código](https://github.com/paper-design/shaders) | Filtros de imagem, água, vidro, metal, fumaça, luz e padrões. | Material ou atmosfera ligada ao conceito; preservar áreas estáveis de leitura. |
| [ShaderGradient](https://github.com/ruucm/shadergradient) | Gradientes animados com forma, câmera e parâmetros. | Profundidade abstrata para uma marca ou virada; confirmar a integração escolhida na documentação atual. |
| [Vanta.js](https://www.vantajs.com/) | Fundos animados e parâmetros de interação/cor. | Ambiente vivo com movimento contido; não depender do mouse para a apresentação funcionar. |
| [tsParticles](https://particles.js.org/) | Exemplos de partículas, atmosferas e efeitos configuráveis. | Poeira, pontos de luz ou celebração quando houver motivo; controlar densidade e contraste. |
| [GL Transitions](https://github.com/gl-transitions/gl-transitions) | Shaders GLSL de passagem entre imagens por progresso. | Passagens com máscaras e distorção; exige renderizador e texturas, não é um motor completo de slides. |
| [hover-effect](https://github.com/robin-dela/hover-effect) | Transições de mídia por mapas de deslocamento e controle por código. | Revelação de imagem acionada por avanço; verificar mídia suportada, APIs e versões das dependências. |

### Ferramentas para efeitos autorais

| Referência | O que procurar | Adaptação ao slide |
| --- | --- | --- |
| [gpu-curtains](https://martinlaxenaire.github.io/gpu-curtains/) | Exemplos WebGPU sincronizados ao layout HTML. | Imagens, texto e objetos acompanhando a composição; prever alternativa no navegador alvo. |
| [curtains.js](https://www.curtainsjs.com/) | Planos associados a imagens, vídeos e Canvas; shaders e pós-processamento. | Ondulação e passagem de mídia mantendo alinhamento com HTML. |
| [TypeGPU](https://docs.swmansion.com/TypeGPU/) | Shaders e exemplos de renderização/simulação em TypeScript e WebGPU. | Gesto visual próprio quando exemplos prontos não bastarem; avaliar esforço e suporte. |
| [OGL](https://github.com/oframe/ogl) | Exemplos WebGL e mecanismos de renderização leves. | Distorção, luz e partículas sob direção própria. |
| [Shader Park](https://github.com/shader-park/shader-park-core) | Formas procedurais e experimentos de shaders a partir de JavaScript. | Esculturas, transformação de formas e metáforas visuais. |
| [Three.js](https://threejs.org/) | Exemplos e documentação de cenas, câmera, materiais e iluminação. | Objeto 3D protagonista ou espaço atravessável; exige assets/geometria adequados. |
| [React Three Fiber](https://r3f.docs.pmnd.rs/getting-started/introduction) + [Drei](https://drei.docs.pmnd.rs/) | Integração React com Three.js, utilitários e materiais. | Produto, vidro ou iluminação dirigida; confirmar compatibilidade entre as versões. |
| [PixiJS](https://pixijs.com/) + [PixiJS Filters](https://pixijs.io/filters/docs/) | Composição 2D e filtros adicionais. | Tratamento de imagens, texto e pós-processamento; escolher filtros pelo tema. |

### Exploração visual, Direção de Arte & Técnicas

| Referência | O que procurar | Adaptação ao slide |
| --- | --- | --- |
| [Behance](https://www.behance.net/) | Curadoria global de pitch decks, direção de arte, motion design, tipografia editorial e identidades visuais de estúdios internacionais. | Pesquisa de moodboards, composições assimétricas, tratamento de luz, grades editoriais e ritmo visual antes de desenhar o deck. Buscar por termos como "Presentation Design", "Keynote Deck", "3D Motion", "Editorial Layout" e "Brand Guidelines" para escapar de clichês e compor slides com estética autoral de estúdio. |
| [DaFont](https://www.dafont.com/) | Catálogo mundial de tipografia display, fontes temáticas (Sci-Fi, Cyberpunk, Retro, Brutalismo, Gótica, Manuscrita) para títulos monumentais. | Pesquisa de fontes de impacto para capas e palavras-chave. Baixar arquivos `.ttf`/`.otf` gratuitos/CC, converter para `.woff2` e declarar via `@font-face` local para funcionamento autônomo offline em apresentações ao vivo. |
| [Unicorn Studio](https://www.unicorn.studio/) | Exemplos e documentação de composição visual, exportação e incorporação. | Experimentar uma direção e verificar o caminho real de entrega; não presumir exportação gratuita ou acesso a um projeto. |
| [cables.gl](https://cables.gl/) | Patches, exemplos e documentação de exportação/incorporação. | Combinar formas, materiais e interação, conferindo dependências do patch escolhido. |
| [Codrops](https://tympanus.net/codrops/category/tutorials/) | Tutoriais com demos e código de desenvolvimento criativo. | Adaptar uma técnica menos convencional ao argumento; verificar a licença do código e dos assets separadamente. |

## Registro da curadoria

Crie `component-research.md` junto da entrega, com data, direção buscada e:

| Candidato / link específico | Fonte e evidência consultada | Cena / ganho narrativo | Adaptação prevista | Requisitos / limitações | Decisão e motivo |
| --- | --- | --- | --- | --- | --- |

Use nomes reais e links para demo, tutorial, código ou documentação específicos. Registre o que foi observado, o que foi apenas lido e o que foi testado localmente. Para selecionados, anote versão utilizada, licença, dependências, atribuições necessárias e alternativa de movimento reduzido/compatibilidade. Documente falhas de acesso sem substituir pesquisa por alegações.

No briefing, sintetize a linguagem resultante e as escolhas principais; no storyboard, indique cena, componente/técnica, gatilho e relação com a passagem. Não despeje o relatório técnico na apresentação ou na conversa: uma síntese curta basta.

## Transformar repertório em autoria

- Não copie a aparência completa da demo. Troque os assets e ajuste proporção, recorte, paleta, fonte, velocidade, contraste e comportamento ao projeto. Reaproveite o mecanismo que produz o gesto desejado.
- Explore combinação de técnicas apenas quando produzem uma ideia clara: distorção como reflexo, partículas como rastro ou uma forma procedural como metáfora. Uma cena calma pode ganhar mais com um detalhe sutil que com um fundo inteiro animado.
- Preserve a estrutura existente quando viável. Não migre o deck inteiro para React apenas por um componente; compare uma alternativa em JavaScript ou adaptação permitida pelo código. Quando uma dependência for a melhor escolha, entregue o build executável.
- Controle pelo estado do slide: iniciar ao entrar, pausar quando solicitado, interromper ao sair, voltar de forma determinística e liberar recursos. Hover e scroll de uma demo precisam virar gatilhos compatíveis com o modo de apresentação.
- Uma transição GPU entre texturas não anima automaticamente o HTML inteiro. A textura de destino da passagem representa superfície/ponte visual, não o slide completo. Textos, fotos e shaders de conteúdo entram só depois, conforme [ciclo-de-cena.md](ciclo-de-cena.md), sem aparição antecipada nem repetição da entrada.
- Confirme suporte WebGL/WebGPU no ambiente de entrega e implemente fallback legível. Limite renderização à cena ativa, ajuste resolução e evite múltiplos motores GPU concorrentes sem necessidade.
- Verifique licenças e condições dos componentes e assets antes de incorporar; incluir uma referência no catálogo não autoriza compras, publicação ou mudanças em contas externas.

## Verificação da integração

Teste no navegador a cena real com fontes e assets finais, avanço e retorno rápidos, pausa, redimensionamento e movimento reduzido. Confira legibilidade, erros, carregamento, limpeza de recursos e fallback. O protótipo funcionando isoladamente não prova que funciona no deck. Se não puder testar, declare essa limitação na entrega.
