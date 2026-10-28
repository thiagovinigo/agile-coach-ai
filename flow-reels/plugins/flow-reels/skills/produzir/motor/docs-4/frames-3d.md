# Frames 3D (4.0)

Três modos e quatro sobreposições que põem o vídeo em 3D: dentro de um celular, numa câmera 2.5D que anda
pelo cenário, numa parede ou num corredor de monitores, num dolly zoom, numa moldura que você atravessa,
numa polaroid e num rack focus. Os modos moram em `web/modos/frames3d.js` (com a base `M.f3d`, que as
sobreposições usam) e as sobreposições em `web/sobre/frames3d.js`. A pesquisa que embasa tudo é a
`docs/pesquisa-4-0/02-maos-corpo-e-frames-3d.md`, seção 3 (B1, B5, B6, B7, B9, B13, B14, B15).

| peça | tipo | desenho | precisa da visão |
|---|---|---|---|
| `celular3d` | modo | three.js | só com `"rosto": "fora"` (máscara) |
| `parallax` | modo | three.js + vista recortada | máscara, fundo limpo e `fundo-profundidade.png` |
| `telas` | modo | three.js | só com os looks `silhueta` (máscara) e `fundo` (fundo limpo) |
| `dolly` | sobreposição | three.js + vista recortada | máscara, fundo limpo e `fundo-profundidade.png` |
| `moldura-pop` | sobreposição | CSS 3D | máscara |
| `polaroid` | sobreposição | CSS 3D | não |
| `foco` | sobreposição | three.js (shader de desfoque) | máscara e profundidade |

**GPU.** Vão para o `motor/gpu.json`: modos `celular3d`, `parallax` e `telas`; sobreposições `dolly` e
`foco`. A `moldura-pop` e a `polaroid` são CSS e não pedem GPU. Enquanto o `gpu.json` não tiver os nomes, o
plano liga a GPU com `"gpu": true` no topo do `cenas.json`.

## Como funciona (vale para todas)

- **Um renderizador só.** Todas as peças desenham num `WebGLRenderer` compartilhado (`M.f3d.gl()`, 1080 x
  1920, `preserveDrawingBuffer`, antialias) e copiam o resultado para o `<canvas>` 2D delas. O reel nunca
  passa do limite de contextos WebGL do Chromium, por mais peças que use.
- **Tudo é função de t.** A câmera, a pose do celular, a da moldura e a dos monitores saem de curvas
  fechadas do tempo (`gsap.parseEase`), sem nada acumulado. O WebGL redesenha do zero em `M.aCada`.
- **O que a legenda e os gates medem anda pela linha do tempo**, com um set por quadro, no meio do
  intervalo antes do quadro (`M.f3d.porQuadro`): a sonda do rosto, você recortado no `parallax`, os textos
  na tela do celular (homografia em `matrix3d`), os recortes da `moldura-pop`. A legenda `revela` viaja no
  tempo sem rodar ganchos e acha o estado certo.
- **A sonda do rosto.** Quando o rosto aparece dentro do 3D (na tela do celular, no monitor do vivo), o modo
  põe uma vista plana e invisível (`clip-path: inset(50%)`) que segue o rosto exatamente onde ele aparece
  projetado; ela é a `vistaRosto` que o motor, a legenda e o gate 4 medem. Com a tela de costas, ela some.
- **Sets de visibilidade em par.** Todo elemento com set de `visibility` leva o par "escondido no 0 /
  `inherit` no começo". O GSAP guarda como "antes" de um set `hidden` a visibilidade calculada (`visible`),
  e voltar no tempo escrevia `visible` num filho de camada escondida, que aparecia fora da hora: o flash da
  polaroid pintava de branco cenas anteriores.
- **PNG por quadro como fonte do motor.** A máscara, a profundidade e o quadro congelado da polaroid entram
  como fontes do motor (`M.f3d.fonteMascara`, `fonteProfundidade`, `fonteQuadro`) lidas por vistas
  invisíveis de 2 px: o render espera o PNG decodificar antes dos ganchos, e a textura sobe uma vez por
  quadro novo.
- **O cenário em 3D** (`M.f3d.cenario`): cada pixel do `fundo-limpo.jpg` vai para o raio da câmera de casa,
  na distância que o `fundo-profundidade.png` dá (de 3,05 a 4,25 unidades; você fica num plano a 2,0). Com a
  câmera em casa o cenário reproduz o quadro exato. A malha passa 30% de cada lado, com a textura espelhada,
  borrada e escurecida fora do quadro: a câmera anda sem mostrar a beirada. A versão borrada do fundo é
  feita com a imagem espelhada em volta antes do desfoque (senão a borda puxa o transparente e escurece).
- **Determinismo medido** (`--quadro` não basta: página nova contra 12 quadros em sequência contra pular
  para 35 s e 2 s antes), 11 instantes, um em cada peça: diferença máxima de 1 nível (arredondamento da
  GPU), nenhum pixel acima de 2.

## Modo `celular3d`

O vídeo dentro de um celular 3D feito no código (nenhum modelo baixado, nenhuma marca): corpo extrudado com
borda chanfrada de metal (`MeshPhysicalMaterial`, metal 1, verniz), vidro preto envernizado, tela com cantos
contínuos, ilha, lente frontal, quatro botões e o módulo de câmera com três lentes nas costas. Os reflexos
vêm de um estúdio montado na hora (`PMREMGenerator`: softbox branca em cima, faixa no acento à direita, que
acende a borda, recorte branco atrás, rebote ciano fraco embaixo). O palco é a superfície da marca com uma
luz macia no acento atrás do aparelho, vinheta, grão por quadro e sombra de contato.

**Movimento.** Entra pela direita e de cima girando (as costas passam pela câmera e ele vira, de -205° a
-13°, curva quártica, sem passar do ponto), assenta e faz uma órbita curta de ~24° (sine.inOut) até o
fim, com flutuação leve e um dolly de 4%. O reflexo do vidro desliza com o giro. A entrada é curta (até
0,75 s, ou 40% da cena) e **já parte de dentro do quadro**: 0,3 unidade à direita (antes 1,05, fora da tela,
que tem meia largura de ~0,55 na distância do aparelho), um pouco acima e mais fundo, de 0,88 da escala. O
primeiro quadro da cena já mostra o aparelho (as costas, girando); antes ela ficava vazia por ~0,5 s.

```json
{ "id": "c9", "modo": "celular3d", "inicio": 19.0, "fim": 22.5,
  "conteudo": { "rosto": "bolha", "tela": "marca", "rotulo": "GARTNER", "titulo": "80%",
                "linhas": ["das iniciativas de governança", "vão fracassar até 2027"] } }
```

| campo | padrão | o que faz |
|---|---|---|
| `tela` | `"principal"` | `"principal"` (a fala, recortada no aspecto da tela seguindo o rosto), `"marca"` (a tela escura da marca, para o conteúdo), `{ "video": "nome" }` (um vídeo de `CENAS.videos`), `{ "acervo": "nome" }` (logo do acervo, centrado com folga) ou `{ "src": "assets/print.png" }` (print cobrindo a tela a partir do topo; `"ajuste": "conter"` centra) |
| `rosto` | `"nenhum"` com a tela na fala, senão `"bolha"` | `"bolha"`: você numa bolha de 460 px no alto à esquerda (y 330, abaixo do HUD), aro no acento, entra com pop; o aparelho fica a 0,07 à direita e em 0,9 da escala (a 0,13 e 0,98 ele era cortado na borda direita). `"fora"`: você recortado (máscara) a 72% à esquerda, chegando de lado; o celular vai para a direita a 78%. `"nenhum"`: só a tela |
| `rotulo`, `titulo`, `linhas` | — | conteúdo na tela, medido e empilhado (linha que quebra ocupa duas). Na tela `"marca"`: rótulo na tinta com fio no acento, título grande (até 5 letras: 200 px no acento), linhas de 44 px, centrados um pouco abaixo do meio. Sobre vídeo ou imagem: um cartão escuro no alto da tela, abaixo da ilha. Preso à tela pela homografia de cada quadro, com `data-texto` |
| `acabamento` | `"grafite"` | `"grafite"`, `"titanio"` ou `"preto"` |
| `x` | por `rosto` | o centro do aparelho na tela, em px (540 = no meio). Antes era um deslocamento do 3D somado ao lado do rosto, e `"x": 0` não centralizava; número com \|x\| < 2 ainda é lido como o deslocamento antigo, com aviso. O aparelho nunca passa da borda: um `x` que o cortaria é puxado para dentro, com aviso (1 unidade do 3D ≈ 987 px) |
| `orbita`, `giro`, `ry`, `y`, `escala` | por `rosto` | ajuste fino: graus da órbita, giro inicial, ângulo de repouso, deslocamento vertical (unidades do 3D) e escala |
| `bolha` | — | `{ "tam": 460, "x": 52, "y": 330 }`. O `y` padrão fica abaixo da faixa do HUD (236 a 291); antes era 262 e cruzava. `y` abaixo de 300 que cruza a faixa dá aviso. Sem `x`, a bolha vai para a esquerda, ou para a direita quando o aparelho está à esquerda do meio |
| `pessoa` | — | com `"fora"`: `{ "escala": 0.72, "x": -96 }` |
| `saida` | — | `"sai"`: sai girando para cima nos últimos ~0,55 s (whoosh) |

- Devolve `vistaRosto` (a bolha, você recortado ou a sonda do rosto na tela), `zonaLegenda`
  `{ y: 1372, fixa: true }` (com `"fora"`: `{ y: 1360 }`, com desvio), `emendasAte: inicio` (a emenda
  escondida não escala a tela de um celular), `mascaraCentro` e `mergulhoCentro` no aparelho.
- **Legenda fixa embaixo** com a tela na fala e com a bolha: solta, ela subia para cima da ilha, fugindo das
  mãos que aparecem na tela.
- Mínimo de 1,2 s de cena. Sons: whoosh na entrada (e na saída, com `"sai"`), pop no conteúdo.
- O rosto na tela fica com ~36% da largura do quadro; na bolha, ~18%.

## Modo `parallax`

Câmera 2.5D: o fundo limpo projetado na profundidade dele, você recortado num plano à frente (a vista com
`recorte: "pessoa"`, posta pela homografia do plano a cada quadro) e poeira no ar entre os dois (38 pontos
macios, 28% no acento). O buraco atrás de você é coberto pelo fundo limpo. Na casa (o primeiro quadro) a
cena é o vídeo vivo, que some nos primeiros 3,5% do movimento: entra por corte seco depois de uma cena de
rosto em tela cheia.

```json
{ "id": "c3", "modo": "parallax", "inicio": 5.75, "fim": 7.85, "conteudo": { "mov": "orbita" } }
```

| campo | padrão | o que faz |
|---|---|---|
| `mov` | `"orbita"` | `"entra"`: dolly na direção do rosto (você cresce ~18%, a parede ~8%) com 2° de giro. `"orbita"`: gira 7,5° em volta do centro do quadro na profundidade da pessoa, com um dolly leve que guarda a beirada. `"sobe"`: grua de 6,5° para cima olhando o mesmo ponto. `"lateral"`: anda de lado com meio giro de volta |
| `forca` | 1 | de 0,2 a 1,6: multiplica o movimento |
| `sentido` | 1 | `-1` ou `"esquerda"` inverte a órbita e a lateral |
| `volta` | `false` | `true`: vai até 62% da cena e volta para casa antes do fim (corte seco limpo para a próxima) |
| `ease` | `"sine.inOut"` | a curva do movimento (nome do GSAP) |
| `foco` | `true` | o fundo desfoca de leve e escurece 12% enquanto a câmera anda |
| `poeira` | `true` | `false` tira a poeira |

- Devolve `vistaRosto` = você recortado (a legenda e as peças da visão seguem você no plano da frente),
  `zonaLegenda` `{ y: 1330 }` e `emendasAte: inicio` (a emenda escondida escalaria só você; a câmera
  andando já esconde o pulo). Zoom de ênfase na cena é ignorado, com aviso.
- O fundo inventado pelo `visao.py` (48,9% no teste) aparece um pouco perto do contorno quando a câmera
  anda. É uma continuação plausível; gravar 3 a 5 s do cenário vazio resolve (MOTOR.md 2.6).
- De 2 a 3,5 s é o ideal; abaixo de ~1,5 s o movimento não lê.

## Modo `telas`

Uma parede de 3 x 3 monitores em arco ou um corredor de 16 monitores (duas paredes de 2 andares x 4) com a
tela do fim. Cada monitor é uma caixa extrudada de metal escuro com aro fino, a tela e um LED no acento. O
vivo (a fala, sem look) fica no centro da parede ou no fim do corredor; os outros mostram o vídeo atrasado,
com looks, a silhueta no acento, o cenário vazio (fundo limpo) e logos do acervo. Os monitores acendem do
centro para fora, como um tubo (a imagem abre de uma linha no meio, com o fio claro). No corredor, faixas no
acento correm no piso e no teto, e o piso é escuro e envernizado.

**Câmera.** Começa com a tela do vivo enchendo o quadro (o mesmo enquadre do vídeo em tela cheia: entra por
corte seco), recua (power3.inOut, de 0,8 a 1,3 s) até mostrar a parede ou o corredor, deriva devagar e
termina entrando no monitor `alvo` até ele virar a tela cheia (power3.inOut, de 0,7 a 1,1 s). Com o alvo no
vivo, o último quadro é o vídeo em tela cheia, e a cena seguinte de rosto entra por corte seco.

```json
{ "id": "c5", "modo": "telas", "inicio": 9.85, "fim": 12.5,
  "conteudo": { "forma": "grade", "imagens": ["salesforce-icone"] } }
```

| campo | padrão | o que faz |
|---|---|---|
| `forma` | `"grade"` | `"grade"` (3 x 3 em arco) ou `"corredor"` |
| `telas` | variações prontas | até 9 (grade) ou 17 (corredor) itens: `{ "atraso": 0.4, "look": "rosa" }`, `{ "acervo": "nome" }`, `{ "src": "assets/x.png" }`, `{ "fundo": true }`. O que faltar vem das variações padrão |
| `look` (de cada tela) | `"normal"` | `normal`, `rosa` (4 faixas chapadas: superfície, rosa escuro, acento, branco), `ciano` (monocromo no ciano, para um detalhe), `crt` (linhas e separação de cor), `contraste` (preto e branco duro), `silhueta` (você chapado no acento; precisa da máscara) |
| `imagens` | `[]` | logos do acervo para as telas 3, 8 e 12 |
| `alvo` | o vivo | o índice do monitor onde a câmera termina |

- Devolve a sonda do rosto (o rosto no monitor do vivo), `zonaLegenda` `{ y: 1330 }`, `emendasAte: inicio`
  e `mergulhoCentro`.
- **O rosto fica pequeno no meio da cena** (a parede inteira: 12 a 14% da largura). É um momento de
  transição: mantenha a cena entre 2 e 3,5 s. Mínimo 2 s.
- Sons: whoosh no recuo e na entrada no alvo. Sem texto nos monitores (texto no WebGL não teria
  `data-texto`).

## Sobreposição `dolly`

Dolly zoom (vertigo) falso por cima de uma cena com o rosto em tela cheia: você fica do mesmo tamanho (uma
vista recortada que copia a vista do rosto da cena, zooms inclusive) e o cenário (o fundo limpo na
profundidade dele) muda de tamanho no sentido contrário, com a perspectiva de verdade: a câmera anda no eixo
e o FOV compensa, `tan(fov/2) = tan(20°) · zP / (zP + d)`. Rastro radial na velocidade (12 amostras, até
9%), fundo desfocando e escurecendo de leve no pico, poeira no ar.

```json
{ "tipo": "dolly", "t": 0.3, "ate": 2.9, "sentido": "sai", "forca": 1.1 }
```

| campo | padrão | o que faz |
|---|---|---|
| `t`, `ate` | a cena | a vida da peça (mínimo 1 s) |
| `sentido` | `"sai"` | `"sai"`: a câmera recua e fecha o FOV, a parede cresce atrás de você (~40% com força 1). `"entra"`: a câmera avança e abre o FOV, a parede recua (~25%), e a malha espelhada e escurecida aparece nas bordas, como vinheta |
| `forca` | 1 | de 0,3 a 2 |
| `poeira` | `true` | — |

- Vai (power2.inOut, até 62% da vida, no máximo 1,7 s), segue andando 8% e volta rápido (power3.inOut,
  ~0,34 s) para a casa antes do `ate`: a cena reaparece sem pulo. A camada entra em 0,12 s.
- Som: whoosh no começo. Feita para o gancho e o momento-herói.

## Sobreposição `moldura-pop`

Uma moldura 3D (CSS, 9 fatias de espessura, face com reflexo e fio aceso) entra girando e assenta atrás de
você, e você a atravessa: a cabeça sai por cima da borda de cima, ombros e mãos pelos lados, e a barra de
baixo passa na sua frente (uma segunda moldura, só com a faixa de baixo, por cima de você). A janela mostra
o vídeo vivo, recortado na tela pelo contorno projetado da moldura a cada quadro; fora dela, o palco da
marca com uma luz no acento atrás da cabeça. Fora da largura da moldura você some em degradê antes da linha
da barra (o ombro que passa do lado não termina num corte reto no ar).

```json
{ "tipo": "moldura-pop", "t": 22.5, "ate": 24.05, "forma": "retrato", "rotulo": "museu" }
```

| campo | padrão | o que faz |
|---|---|---|
| `forma` | `"retrato"` | `"retrato"` (borda de 46 px), `"quadrado"`, `"celular"` (cantos de 104 px, aro de metal), `"circulo"` (anel; a metade de baixo passa na frente) |
| `cor` | por forma | `"branca"` (retrato), `"rosa"` (quadrado e círculo, acento chapado), `"escura"` (celular, metal) |
| `rotulo` | — | etiqueta de museu no acento (letra na superfície) no canto de baixo da janela, do lado de fora do rosto, sempre acima de y 1440 |
| `lado` | `"direita"` | de que lado ela chega girando |
| `fundo` | `"marca"` | `"rosto"`: o vídeo desfocado e escurecido fora da moldura |
| `janela` | pelo rosto | `{x, y, w, h}` em px de saída |

- A janela sai do rosto mediano da vida da peça: a borda de cima na altura da boca, a de baixo até y 1660,
  1,7x a largura do rosto (820 a 930 px).
- Entra em ~0,75 s (power3.out; back.out(1.25) no giro), deriva e sai girando em ~0,42 s. Mínimo 1,4 s.
- A etiqueta sobe já opaca (sem a entrada "foco"): meio transparente, ela deixava o vídeo escuro passar e a
  letra caía abaixo de 4,5:1 no gate 3.
- Você é a mesma imagem da vista do rosto da cena, no mesmo lugar: o rosto que o motor mede é o de verdade.
  Som: whoosh na entrada.

## Sobreposição `polaroid`

No `t`: flash branco (0,32 s) e obturador; o quadro congela. A foto sai do quadro congelado (começa sobre o
quadrado do rosto) e cai no lugar girando (power3.inOut, back.out na rotação, um tombo de 28° em X), o papel
aparece em volta, a legenda é escrita à mão (revelada da esquerda para a direita) e um risco no acento
sublinha. O vídeo volta por baixo. Ela deriva 1,8° enquanto fica e sai deslizando para o lado de fora.

```json
{ "tipo": "polaroid", "t": 7.92, "ate": 9.8, "texto": "89% viu errar" }
```

| campo | padrão | o que faz |
|---|---|---|
| `t`, `ate` | a cena | o congelamento e a saída (mínimo 1,4 s). A legenda à mão termina de ser escrita 0,25 s antes da saída: com vida abaixo de ~2,05 s a escrita acelera (de 0,55 s até 0,3 s) e, se ainda não couber, começa mais cedo, com o cartão terminando de assentar; sai um aviso com o tempo dela. Antes, com 1,4 s, a saída cortava a escrita no meio ("escar") |
| `texto` | — | a legenda à mão (`data-texto`); encolhe até caber dentro da zona segura |
| `lado` | o de mais espaço | `"esquerda"` ou `"direita"` |
| `tam` | pelo espaço | largura do cartão (300 a 440 px); cabe acima dos olhos |
| `y` | 262 | o topo do cartão |
| `giro` | ±7° | a rotação final |

- **A fonte da legenda** é a de mão do sistema ("Bradley Hand", "Noteworthy", "Marker Felt") e, sem elas,
  a "FC Legenda". Nada é baixado; numa máquina sem essas fontes a legenda sai na fonte da marca.
- O cartão encosta na beira de fora; uma reserva `data-zona` (só com ele parado, só a parte dentro da zona)
  faz a legenda desviar dele. A legenda à mão some em 0,12 s quando ele começa a sair.
- Sons: obturador no flash; whoosh na saída quando ela acontece mais de 1,5 s depois do flash.

## Sobreposição `foco`

Rack focus falso pela profundidade: um shader de desfoque em disco (56 amostras numa espiral de ângulo
áureo, girada por pixel para não fazer anéis) com o círculo de confusão de cada pixel vindo da profundidade
do quadro (`visao/profundidade`), separada pela máscara (o fundo nunca pega a profundidade da pessoa, nem o
contrário). A amostra só conta se o próprio desfoque dela chega até o pixel (espalhar como coleta): a pessoa
nítida não vaza halo no fundo desfocado, e a pessoa desfocada transborda por cima da borda do fundo, como
numa lente. As luzes acima de 55% de luminância pesam mais: o neon vira bokeh.

```json
{ "tipo": "foco", "t": 16.3, "ate": 18.95, "de": "fundo", "para": "pessoa" }
```

| campo | padrão | o que faz |
|---|---|---|
| `de`, `para` | `"pessoa"` → `"fundo"` | onde o foco começa e onde termina |
| `troca` | `t + 0,45` | quando o plano de foco começa a andar |
| `duracao` | 0,75 | a troca (power2.inOut) |
| `forca` | 1 | raio máximo = 20 px x força (de 6 a 40) |
| `bokeh` | `true` | — |

- O desfoque cresce em 0,28 s no começo e some em 0,32 s antes do `ate`: a cena volta nítida.
- **Você fora de foco só por até 1 s:** a peça avisa quando a pessoa fica desfocada por mais que isso.
- Com o foco na pessoa, as mãos (mais perto que o rosto) desfocam um pouco: é a lente de verdade.

## Custo medido (M4, Metal, render inteiro)

Reel de 36,1 s com as sete peças em 16 cenas (corte 43 do teste-onda-1, 1084 quadros): **de 59 a 72 ms por
quadro em média** nas duas últimas rodadas (64 a 78 s, de 1,8 a 2,2 s de render por segundo de vídeo); numa
rodada anterior, com o código de antes, deu 106 ms. O mais caro é o `foco` (56 amostras por pixel em
1080 x 1920) e o corredor do `telas` (17 monitores, 4 texturas de vídeo).

## Limites

- O vídeo de teste tem 576 x 1024: na tela cheia do celular e no fim das `telas` ele é ampliado, como no
  resto do motor.
- `dolly`, `foco`, `moldura-pop` e `polaroid` se alinham ao vídeo pela caixa da vista do rosto na tela;
  num modo que gira a vista (vidro-liquido inclinado), elas avisam e podem sair de lugar. A casa delas é o
  `rosto-vidro`.
- A profundidade é relativa: o `foco` usa as medianas da pessoa e do fundo por quadro (`visao.json`), sem
  metro nenhum.
- `telas`: com a parede inteira na tela o rosto fica abaixo de 18% da largura por ~1 s.
