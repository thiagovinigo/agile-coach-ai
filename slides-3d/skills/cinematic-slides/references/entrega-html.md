# Implementação e verificação

## Navegação e estado

- Use cenas identificáveis e uma fonte de estado para navegação, com conteúdo e ordem iguais ao storyboard.
- Ofereça avanço e retorno por teclado e controles visíveis acessíveis, sem cobrir conteúdo. Mostre posição discretamente quando útil.
- Avanço pode revelar uma etapa interna; torne isso previsível e permita voltar. Não prenda o usuário em animações.
- Em reprodução automática, inclua play/pausa que suspenda também timelines, não apenas o contador.
- Não capture teclas quando o usuário digita em campos ou usa controles que dependem delas.
- Finalize estados pertinentes dos controles: normal, foco, hover quando houver mouse, ativo, desabilitado e carregamento/erro quando necessários. Indique início, fim e pausa com clareza. Alvos pequenos visualmente ainda precisam de área de interação utilizável; não dependa de hover para informação essencial.
- Ao sair da cena, encerre ou suspenda animações e renderização. Ao voltar, restaure estado determinístico e legível, sem acumular listeners e loops.

## Motor de transições

- Leia [ciclo-de-cena.md](ciclo-de-cena.md). Exija fases separadas: preparado → transição → vazio → entrada → estável. Pré-carregar não é tornar visível: prepare texto, imagens e Canvas ocultos antes de expor a superfície do destino.
- Para fusões, empurrões e máscaras, mantenha a origem e a superfície/camada de passagem renderizadas durante a troca. O conteúdo final do destino permanece oculto; a passagem não pode revelá-lo inteiro antes das entradas.
- Carregue e decodifique assets antes de iniciar. Conclua a passagem, limpe a origem e a ponte visual, pinte o destino vazio e então inicie uma única timeline de entrada. Fixe o estado final ao concluir. Se ocorrer falha, mostre um estado legível e recuperável.
- Durante a sobreposição, apenas os controles de navegação devem continuar recebendo interação; cenas inativas não recebem foco nem anunciam conteúdo duplicado. Ao estabilizar, ative somente a cena de destino.
- Defina comportamento para cliques rápidos: cancele/retargete de forma determinística ou retenha apenas o último destino pedido. Invalide callbacks antigos; não force um slide intermediário a ficar todo visível antes de atender ao último pedido. Não acumule entradas, bloqueie indefinidamente a navegação ou deixe camadas e máscaras abandonadas.
- Ao retornar, escolha inversão coerente ou corte para o estado estável. Respeite direção espacial quando houver push, wipe ou elemento compartilhado.
- Consulte [repertorio-movimento.md](repertorio-movimento.md) para exigências de cada efeito. Uma simulação em 2D é aceitável quando o briefing a descreve como tal e produz a sensação desejada.

## Movimento e recursos

- Para componentes pesquisados, aplique [pesquisa-componentes.md](pesquisa-componentes.md). Teste a integração no deck: gatilhos de avanço/retorno, pausa, início/fim de renderização, liberação de recursos e fallback. Confirme a versão e dependências usadas, sem carregar a demo inteira como solução.
- Prefira transformações e opacidade. Avalie filtros, vídeo, partículas e 3D pelo custo e contribuição narrativa.
- Reserve espaço para assets e carregue antecipadamente os necessários para a próxima cena. Fontes e imagens não devem causar saltos durante a apresentação.
- Respeite `prefers-reduced-motion`, reduzindo deslocamentos, paralaxe e movimento contínuo sem ocultar conteúdo ou impedir navegação.
- Áudio, se houver, precisa de início explícito e controle de volume/mudo. Não dependa dele para informação essencial.

## Leitura e entrega

- Confira a composição com [repertorio-layouts.md](repertorio-layouts.md): foco dominante, ordem de leitura, apoios junto do que explicam e variação coerente com a narrativa. Verifique especialmente contraste sobre fotografia, rótulos de diagramas e equivalência de enquadramento nas comparações.
- Em gráficos, tabelas e indicadores, confira valores contra a fonte, unidades, período, escalas e conclusão. A animação deve terminar nos valores corretos e preservar sua leitura; decoração não pode distorcer a evidência.
- Aplique a curadoria de [curadoria-tipografica.md](curadoria-tipografica.md). Confirme arquivos e estilos carregados, suporte aos caracteres reais e aparência final no navegador. Uma declaração `font-family` ou um fallback renderizado não prova que a fonte escolhida foi carregada.
- Aguarde o carregamento das fontes críticas antes de iniciar passagens que dependam de medidas de texto. Confira que não há peso/itálico sintetizado por falta do arquivo correto nem títulos cortados após o carregamento.
- Preserve proporção sem esticar a cena. Em viewport menor, adapte ou escale o palco sem cortar texto e controles; priorize leitura também no modo autônomo.
- Garanta contraste, hierarquia, foco visível e nomes acessíveis dos controles. Descreva imagens informativas e ignore as decorativas para leitores de tela.
- Confira ordem de foco e leitura nas cenas ativas e nas notas, texto longo e quebras após resize. Em leitura autônoma móvel, adapte a composição ou ofereça conteúdo textual legível; apenas escalar o palco de projeção não garante leitura.
- Mantenha texto em HTML quando possível. Dados ou cenas em Canvas precisam de equivalentes textuais.
- Use caminhos consistentes. Se houver build, gere a saída e indique como abrir; um projeto incompleto não é um HTML pronto.
- Para offline, inclua fontes, bibliotecas e imagens. Informe dependências de rede ou servidor local quando houver.

## Verificação final

Abra o resultado com as ferramentas disponíveis e faça uma inspeção agrupada. Consulte [direcao-e-acabamento.md](direcao-e-acabamento.md) para avaliar a direção além do funcionamento. Percorra o deck inteiro:

1. Carregamento, fontes reais, imagens, ordem e encerramento.
2. Avançar, voltar, retornar a cenas animadas, pausa e retomada quando aplicáveis.
3. Texto e enquadramentos no tamanho de apresentação e em viewport menor.
4. Movimento reduzido, teclado e foco.
5. Console e recursos ausentes quando acessíveis.

Nas passagens relevantes, observe início, meio, primeiro frame vazio do destino, entradas e estado estável, não apenas screenshots finais. Confira que nenhum conteúdo final aparece antecipado, desaparece e entra novamente. Fotografias e shaders obedecem à ordem tanto quanto títulos. Teste avanço rápido, retorno durante transição/entrada, clique na cena atual, resize e reinício. Sob movimento reduzido, chegue ao mesmo conteúdo final com corte/fusão breve, sem flashes de vazio. Verifique que não restam sobreposições bloqueando cliques, filtros borrando texto, estado vazio preso ou loops da cena anterior. Pausa controla também delays de entrada e relógios dos shaders. Registre evidência temporal conforme [ciclo-de-cena.md](ciclo-de-cena.md).

Agrupe screenshots, observação de transições, verificações e correções na mesma rodada. Corrija os achados em lote e confirme em uma segunda rodada; depois encerre o polimento estético. Se permanecer falha de funcionamento ou requisito, corrija e verifique o ponto afetado sem reiniciar uma revisão ilimitada de estilo. Não declare verificação de navegador sem realizá-la; diga o que foi inspecionado e o que falta. Não escreva uma suíte de testes que apenas espelha o HTML; valide comportamento e riscos concretos.
