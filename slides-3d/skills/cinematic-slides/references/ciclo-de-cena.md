# Contrato de ordem e visibilidade

Este contrato governa o motor e prevalece sobre exemplos de transições ou componentes que já mostram o destino completo. A sequência normal é:

**transição → cena vazia → entradas dos elementos → leitura estável**

“Vazia” significa sem conteúdo do slide visível: título, apoio, fotos, diagrama, dados e shader de conteúdo ainda estão no estado inicial oculto. A superfície de fundo pode existir, assim como os controles globais. Não significa remover o conteúdo dos arquivos nem apresentar uma tela preta longa.

## Estados distintos

| Estado | Visibilidade e ação |
| --- | --- |
| Preparado | Assets carregados/decodificados e fontes prontas; destino oculto e sem interação. Geometria pode ser medida sem torná-lo visível. |
| Em transição | Origem sai e camada de passagem opera. Destino pode estar montado como superfície, mas seus elementos continuam ocultos. |
| Vazio | Passagem concluída; apenas superfície do destino. Estado inicial oculto já aplicado a todos os elementos de entrada. |
| Entrando | Uma timeline revela elementos na ordem do storyboard. Imagens e shaders também obedecem ao gatilho, não só os textos. |
| Estável | Conteúdo necessário completamente visível, legível e interativo. Sem reinício automático da entrada. |

A visita à cena, e não cada evento de renderização, é a unidade de execução. Reload, resize, font loading, atualização de contador ou fim de uma animação filha não devem iniciar outra entrada.

## Implementar sem o primeiro frame errado

1. Separe superfície, grupos de conteúdo e camada de transição. Marque explicitamente tudo que vai entrar, inclusive Canvas, imagem de fundo informativa, labels e pseudo-elementos relacionados. Uma foto que explica a cena é conteúdo mesmo cobrindo o slide inteiro.
2. Antes de remover `hidden`, ativar a cena ou desenhar o shader, aplique o estado inicial oculto. Use classes/atributos de fase ou styles já presentes; não espere um efeito de montagem posterior para esconder o conteúdo.
3. Pré-carregue fontes e assets sem expor o destino. No fim da passagem, retire a origem e a camada de transição mantendo o destino vazio. Garanta que esse estado seja pintado antes de iniciar as entradas; em um motor DOM, uma barreira de frames pode ser necessária. Não invente uma espera longa: basta um respiro perceptível quando o ritmo pedir.
4. Execute uma timeline única: fundo informativo/foto ou shader → foco/título → apoio/pistas, ou outra ordem justificada no storyboard. Elementos que formam a mesma ideia podem entrar juntos; não crie uma fila longa de animações só para mostrar tudo separado.
5. Ao terminar, fixe o estado final visível antes de cancelar ou limpar animações. Nunca deixe `fill` de uma animação cancelada devolver o conteúdo ao estado oculto. A cena estável não recebe novamente o gatilho de entrada.

Aplicar `opacity: 0` apenas no título não resolve se fotos, labels ou o Canvas já apareceram. Iniciar um shader em estado final e zerar seus uniforms no frame seguinte também produz o bug.

## Passagem não é entrada

Fusão, push, wipe, iris e máscaras podem manter origem e superfície de destino renderizadas, mas isso não autoriza mostrar o conteúdo final do destino. Uma passagem GPU deve usar origem e superfície/ponte visual, não um screenshot completo do próximo slide que será revelado novamente.

Para continuidade, use na passagem um motivo, cor, luz, forma ou textura de ligação. Se um elemento compartilhado for o próprio conteúdo do destino, aquela passagem não serve a este contrato quando o revela antes da fase de entrada; adapte a conexão ou escolha outra transição. Não esconda uma aparição precoce chamando-a de “continuidade”. Uma revelação da foto pode ser a primeira entrada após a passagem, sem repeti-la depois.

## Interrupção, retorno e pausa

- Cada navegação tem um identificador de execução. Finalizações, callbacks e promises só podem alterar a cena se ainda pertencerem à navegação atual.
- Cancelar uma visita cancela sua entrada pendente, callbacks, timers e renderização. Retenha apenas o último destino quando necessário; não acumule filas de entradas.
- Em avanço rápido, não force um slide intermediário a mostrar todo seu conteúdo por um frame antes de ir ao destino solicitado. Limpe a execução anterior e prepare o destino mais recente no estado oculto.
- Ao voltar e ao reiniciar, prepare a nova visita do começo, usando a mesma sequência. Ao clicar no índice da cena atual, não reinicie a entrada. Resize e troca de viewport preservam a fase e o progresso.
- Pausa congela passagem, entrada, delays e tempo do shader. Retomada continua de onde parou; não reexecuta o início. Uma cena não pode ficar indefinidamente vazia por falha de callback ou de recurso.
- Sob movimento reduzido, use corte/fusão breve e conteúdo estável direto, sem introduzir flashes de vazio, deslocamentos ou entradas parceladas. Falha de GPU/asset chega a uma alternativa legível e permite navegação; a exceção preserva a didática.
- Cenas fora de uso ficam sem foco e sem anúncios duplicados. Na entrada, disponibilize o texto completo semanticamente sem anunciar cada letra animada.

## Verificação temporal obrigatória

Além do final de cada slide, inspecione:

1. Destino preparado: conteúdo oculto antes de expor a superfície.
2. Meio da passagem: nenhum elemento final do destino antecipado.
3. Primeiro frame do destino: vazio conforme o contrato, sem um frame de tudo visível.
4. Entrada: ordem do storyboard, inclusive fotos e shader, sem salto do estado final ao inicial.
5. Estado estável: tudo necessário visível, sem animação repetida após esperar, redimensionar ou carregar fonte.

Use registro de frames, gravação ou pausa controlada da timeline com estilos/uniforms observados. Screenshot final e promessa no código não provam a ordem. Teste ainda avanço rápido, retorno durante entrada, clique na cena atual, pausa no estado vazio/entrada e fallback. Registre o que foi realmente observado na revisão do deck.
