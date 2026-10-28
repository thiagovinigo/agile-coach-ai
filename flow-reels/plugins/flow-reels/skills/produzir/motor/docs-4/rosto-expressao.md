# Rosto e expressão (4.3)

Efeitos presos ao rosto de quem fala e disparados pela expressão dele: o olho que brilha na surpresa, o
laser saindo dos olhos, o "clique" na piscada, a voz saindo da boca, o ícone que salta ao lado da cabeça,
a malha do rosto acendendo e o soco de zoom no "uau". Duas peças:

| arquivo | o que faz |
|---|---|
| `scripts/expressao.py` | roda o MediaPipe Face Landmarker no vídeo do corte e grava `visao/expressao.json`: a expressão, a pose e os pontos do rosto por quadro, e os eventos (piscada, piscada-dupla, boca-aberta, sorriso, sobrancelha, cabeca-vira, aceno) |
| `motor/web/sobre/rosto-fx.js` | as 7 sobreposições: `brilho-olhar`, `laser`, `piscada`, `fala-onda`, `emoji-reacao`, `mascara-tech`, `zoom-reacao` |

O modelo é o `componentes/modelos/face_landmarker.task` (MediaPipe Face Landmarker float16, Apache-2.0,
3,6 MB, origem e sha256 em `componentes/modelos/LEIA.md`). A demo é o corte 51 de `projetos/teste-onda-1`
(o mesmo `fala.mp4` do corte 42).

---

## 1. `expressao.py`: o que o rosto está fazendo

```
flow-reels produzir/expressao --projeto projetos/<v> --corte NN
flow-reels produzir/expressao --projeto projetos/<v> --corte NN --resumo
flow-reels produzir/expressao --projeto projetos/<v> --corte NN --folha
```

- **Precisa** do vídeo do corte e do modelo. O motor só recebe a expressão quando a visão do corte também
  existe e é do mesmo vídeo (o `compor.py` confere o `origem` do `expressao.json` contra o
  `visao/.origem.json`, como faz com o `gestos.json`): rode o `visao.py` antes, ou depois, e rode o
  `expressao.py` de novo sempre que reeditar a fala.
- **Grade de quadros**: a mesma do `compor.py` e do `visao.py` (o `cenas.json` → `fonte.video`, padrão
  `fala.mp4`, com `-vf fps=<fps do plano>`); quadro acima de 1920 px de altura é reduzido para a análise e
  os pontos voltam para o pixel da fonte. Trechos entre as emendas do `edicao.json`: nada alisado
  atravessa uma emenda, e o detector é reaberto nela.
- **MediaPipe no Mac**: o caminho de CPU dos landmarkers aborta; o script testa num processo separado e usa
  o Metal (delegate GPU), em modo VIDEO e com imagem SRGBA. O detector é fechado e aberto de novo a cada
  100 quadros (o Metal retém memória até o `close()`) e em cada emenda. Um `sounddevice` vazio entra antes
  do import (o import do MediaPipe abre o CoreAudio).
- `--resumo` imprime a expressão do vídeo (medianas, p90, faixa da pose) e cada evento com a palavra dita
  ali, para escolher gatilhos (sem refazer, se o `expressao.json` já é deste vídeo).
- `--folha [caminho]` grava a folha de contato (padrão `folha-expressao.jpg` na pasta do corte): um recorte
  do rosto por evento, com a malha, os olhos, a boca, a seta da pose e os valores. **Olhe antes de planejar.**
- Saída 0 = gravou; 1 = gravou, mas o rosto aparece em menos da metade dos quadros; 2 = erro.
- **Custo medido** (M4): 8 a 10 ms por quadro num vídeo 576 x 1024 com a máquina livre (36 s em ~11 s de
  análise, ~20 s no total com a sonda); 15 a 19 ms em 1080 x 1920 (44 s em 20 s, 63 s em 36 s). Com outros
  renders na máquina, sobe junto.

**Lados e sentidos** (conferidos nos três cortes reais da 4.0):
- "esquerda" é o olho à esquerda **na tela** (de quem assiste), como nas mãos. O "Left" dos blendshapes do
  MediaPipe é o lado da pessoa, isto é, o olho da direita na tela: o script troca. Num vídeo espelhado (o
  olho direito da pessoa à direita da tela), ele avisa e troca de volta.
- `pose`: `[yaw, pitch, roll]` em graus. yaw > 0 = o rosto vira para a direita da tela; pitch > 0 = olha
  para cima; roll > 0 = a cabeça inclina no sentido horário. Correlação com o nariz e a linha dos olhos de
  0,88 a 0,99.
- `olhar`: `[x, y]` de −1 a 1 (dos blendshapes eyeLookIn/Out/Up/Down), x > 0 = para a direita da tela,
  y > 0 = para baixo.

**Suavização** (zero-phase, trecho a trecho): One Euro para a frente e para trás nos pontos, em unidades da
distância entre os olhos (`minCutoff 1,2 Hz, beta 0,5`), e na pose (`1,0 / 0,3`, em unidades de 20°);
binômio 1-2-1 nos blendshapes (a piscada de 3 quadros continua lá); o olhar passa por mais dois 1-2-1.
Falha de até 6 quadros dentro de um trecho é preenchida em linha reta (`"m": false`); a presença `a` sobe
em 6 quadros e desce em 6 antes de o rosto sumir (corta seco na emenda).

**Os eventos** (todos com `tipo`, `quadro`, `t` e `x, y` em pixels da fonte):

| tipo | quando | campos extras |
|---|---|---|
| `piscada` | os olhos fecham e abrem em até 12 quadros: a abertura das pálpebras (pálpebra de cima à de baixo sobre canto a canto) cai abaixo de 0,32 da mediana de 2 s em volta e o blendshape (média dos dois) passa de 0,55. Olhar para baixo também fecha a pálpebra, mas devagar e por mais tempo (0,4 a 0,6 da mediana): não conta. Um olho só fechando (abaixo de 0,26) com o outro aberto (acima de 0,8) é a piscadela daquele lado | `olho` (`ambos`, `esquerda`, `direita`), `dupla`, `de`, `ate`, `fundo` |
| `piscada-dupla` | duas piscadas com menos de 0,7 s entre os começos: um evento no começo da primeira (as duas também saem como `piscada`, com `dupla: true`) | `ate` |
| `boca-aberta` | pico do jawOpen ≥ 0,40, com 0,20 acima do mínimo de ±0,5 s e 3 quadros ou mais acima de 0,30; 0,8 s entre dois (fica o maior). A fala normal fica em 0,04 de mediana e 0,21 de p90: o pico é o "uau", o "26%" dito com força | `pico`, `de`, `ate` |
| `sorriso` | a média dos dois cantos passa de 0,50 e fica acima de 0,40 por 8 quadros ou mais, subindo 0,25 sobre o nível (p30) dos 2 s de antes; o evento é onde ele cruza a metade da subida; 1 s entre o fim de um e o começo do outro | `pico`, `ate` |
| `sobrancelha` | pico do maior entre browInnerUp e a média dos browOuterUp ≥ 0,35, com 0,20 acima do mínimo de ±0,6 s; 1 s entre dois. O pico dentro de uma piscada (±3 quadros) ou com o olho meio fechado (piscar > 0,45) **não conta**: a piscada puxa o blendshape da sobrancelha junto (nos testes, 4 de 6 "surpresas" eram piscadas) | `pico`, `de`, `ate` |
| `cabeca-vira` | o yaw anda mais de 60°/s por 3 quadros ou mais no mesmo sentido, somando 10° ou mais; o evento é o quadro mais rápido; 0,5 s entre dois | `sentido` (+1 = para a direita da tela), `de`, `ate` (graus), `vel` (°/s) |
| `aceno` | o pitch sem a tendência (menos a média de 0,8 s) faz 3 passadas seguidas ou mais (desce-sobe-desce), cada uma de 5° ou mais e de 0,1 a 0,5 s, e o pitch anda 1,5 vez o que o yaw anda no trecho (quem só mexe a cabeça falando não acena) | `n` (meias-oscilações), `amplitude` (graus), `ate` |

Os limiares estão no `L` do script e são gravados no `expressao.json` (`limiares`).

**O que os vídeos de teste mostraram** (folhas conferidas no olho, um recorte por evento):

| corte | piscada | boca-aberta | sorriso | sobrancelha | cabeca-vira | aceno |
|---|---|---|---|---|---|---|
| teste-onda-1 / 42 (36 s) | 15 (uma dupla em "Também não") | 6 | 6 | 2 | 4 | 5 |
| apis-de-ia-gratis / 02 (44 s) | 11 | 9 | 2 | 4 | 8 | 1 |
| 5-plugins-claude-code / 02 (63 s) | 15 (uma dupla) | 9 | 15 | 4 | 1 | 1 |

- As piscadas batem com o olho fechado no quadro do evento; o que escapa é a piscada muito rápida (1 a 2
  quadros) num movimento de cabeça.
- A surpresa de verdade (sobrancelha) é rara numa fala: 2 a 4 por reel. O sorriso varia muito de pessoa e
  de assunto (2 a 15).
- O `beicinho` (mouthPucker) fica alto em toda vogal "o"/"u" do português (p90 de 0,34 a 0,82): não serve
  de gatilho, está no arquivo só como valor.
- `bochecha` (cheekPuff) fica em 0 em fala normal.

**`visao/expressao.json`** (o `compor.py` entrega em `window.VISAO.expressao`):

```json
{ "versao": 1, "fonte": "fala.mp4", "fps": 30, "largura": 576, "altura": 1024, "total": 1084,
  "segmentos": [[0, 23], [23, 347], [347, 1084]],
  "origem": { "video": "/…/fala.mp4", "mtime": 1791418438.15, "tamanho": 13048304, "fps": 30 },
  "modelo": "MediaPipe Face Landmarker (blendshapes, float16)", "licenca": "Apache-2.0",
  "lado": "de quem assiste: esquerda = o olho à esquerda na tela", "pose_sentido": "…",
  "pontos": ["olho_e", "olho_d", "canto_e_ext", "canto_e_int", "canto_d_int", "canto_d_ext", "boca", "boca_e",
             "boca_d", "labio_sup", "labio_inf", "nariz", "testa", "queixo", "sobrancelha_e", "sobrancelha_d"],
  "malha": { "indices": [10, 297, …], "arestas": [[0, 1], …], "olhos": [[…], […]] },
  "limiares": { … }, "relatorio": { "medidos": 1084, "preenchidos": 0, "espelhado": false, "caminho": "metal",
                                    "ms_por_quadro": 8.3, "eventos": { "piscada": 15, … } },
  "quadros": [ null | { "a": 1.0, "m": true, "piscar": [0.12, 0.10], "boca": 0.04, "sorriso": 0.01,
                        "sobrancelha": 0.02, "bochecha": 0.0, "beicinho": 0.01, "arregalado": 0.0,
                        "olhar": [0.05, 0.31], "pose": [-5.7, -6.4, 0.6], "io": 140.2,
                        "p": [[x, y] × 16], "malha": [x0, y0, x1, y1, … × 83] } ],
  "eventos": [ { "tipo": "piscada", "quadro": 10, "t": 0.333, "x": 243.1, "y": 371.0, "olho": "ambos",
                 "dupla": false, "de": 0.3, "ate": 0.6, "fundo": 0.1 } ] }
```

- `p` são os 16 pontos de `pontos`, em pixels da fonte: `olho_e`/`olho_d` são os centros das íris; os
  cantos dos olhos (de fora e de dentro); `boca` é o meio entre os lábios; `boca_e`/`boca_d` os cantos;
  `testa` é o alto da malha (não o cabelo) e `queixo` a ponta do queixo.
- `io` é a largura de um canto de fora do olho ao outro, em pixels da fonte (a escala do rosto).
- `malha`: 83 pontos (18 do oval, 8 em cada olho, 5 em cada sobrancelha, 10 dos lábios, 6 do nariz e 23 do
  miolo), inteiros, em pixels da fonte; os primeiros 18 são o oval, em ordem. `arestas` é a triangulação de
  Delaunay do rosto médio do vídeo, sem as arestas que atravessam um olho ou a boca e sem as compridas;
  `olhos` são os índices (na malha) do contorno do olho da esquerda e da direita da tela.
- Tamanho: ~1,2 MB para 36 s, ~2,1 MB para 63 s (o motor carrega tudo no `window.VISAO`).

---

## 2. As sobreposições (`sobre/rosto-fx.js`)

Todas vão em `cena.sobre` (numa cena com o rosto na tela: `rosto-vidro`, `vidro-liquido` de frente,
`camadas`) ou em `CENAS.sobre` (seguem a vista do rosto da cena da vez). Precisam do `expressao.json` deste
vídeo; sem ele, o motor recusa o plano com o Error que diz o que rodar.

**Campos comuns**

| campo | padrão | o que é |
|---|---|---|
| `t`, `ate` | a cena | a vida da peça |
| `gatilho` | o da peça | um tipo de evento do `expressao.json` (ou vários com `"|"`): o efeito acontece em cada evento desse tipo dentro de `[t, ate]`. `null` = sem gatilho (um disparo no `t`) |
| `em` | — | instantes à mão (vale mais que o gatilho): `[11.95]` |
| `cor` | `"destaque"` | `"destaque"` (o rosa chapado), `"tinta"` (branco), `"ciano"` ou `#RRGGBB` |
| `som` | o da peça | um som válido, ou `false`; no máximo um a cada 1,5 s por peça |

Com `gatilho` sem evento no trecho, a peça avisa no console ("rode o expressao.py --resumo") e não aparece
(o `zoom-reacao` e o `brilho-olhar` sem evento também não; use `em`). Cada peça desenha num canvas
1080 x 1920 dentro da própria raiz, preso à vista do rosto pela conta exata do quadro
(`getBoundingClientRect` da imagem: enquadre, zoom de ênfase, zoom das emendas, transição) e recortado pela
janela da vista. **O rosto nunca fica escondido**: o que passa pelos olhos é só flash; laser e ondas da fala
são recortados fora do oval do rosto; o ícone fica ao lado da cabeça, na zona segura.

### `brilho-olhar`

O brilho de anime: em cada olho, uma estrela de quatro pontas no reflexo (acima e para fora da íris), girando
devagar, com o risco horizontal de lente (rosa, miolo branco), um halo e uma faísca pequena do outro lado. Cresce
em 0,08 s, segura e encolhe em 0,3 s; o miolo branco sobre a íris só é forte nos primeiros 0,1 a 0,2 s (o
flash). Com o olho fechando (piscar), apaga junto.

| campo | padrão | |
|---|---|---|
| `gatilho` | `"sobrancelha"` | |
| `dur` | 0,7 | s de cada brilho (0,3 a 2) |
| `tam` | 1 | escala (0,4 a 2,5) |

Som `tick`. 0,4 s entre dois.

```json
{ "tipo": "brilho-olhar", "t": 29.6, "ate": 30.5, "gatilho": "sobrancelha" }
{ "tipo": "brilho-olhar", "t": 3.0, "ate": 3.8, "em": [3.1], "tam": 1.4 }
```

### `laser`

Um feixe saindo de cada olho, para o seu lado, ao longo da linha dos olhos (que já traz o roll da cabeça),
dobrado para cima ou para baixo pelo pitch e mais longo do lado para onde a cabeça vira (yaw); a pose é a
média de ±3 quadros. O feixe nasce no canto de fora do olho: nunca passa por cima de um olho nem do rosto.
Cresce em 0,12 s até o `alcance` (no máximo até 40 px da borda da janela, para o impacto ficar na tela),
tremula, alarga um pouco com a distância, pulsos brancos correm por ele, clarão e faíscas no impacto; no
fim recolhe para o olho com uma rajada de faíscas no canto do olho. Sobre a íris, só o flash do começo
(0,04 a 0,28 s); depois, um halo baixo. (A primeira versão, em V para quem assiste, cruzava a legenda e as
mãos: trocada depois de olhar os quadros.)

| campo | padrão | |
|---|---|---|
| `gatilho` | — | sem gatilho, um disparo no `t` |
| `dur` | 0,9 | s de cada disparo (0,35 a 3) |
| `alcance` | 620 | px de saída do olho até o impacto |
| `alvo` | — | `[x, y]` de saída: os dois feixes vão até lá |
| `dir` | — | `[dx, dy]` do feixe do olho da direita, no lugar da pose (o da esquerda espelha; `"espelha": false` não) |

Som `raio`. Até 6 disparos, 0,5 s entre dois. As faíscas são partículas com semente
(`M.fx.semente(nome, quadro)`) e posição fechada pela idade.

```json
{ "tipo": "laser", "t": 20.35, "ate": 21.3 }
{ "tipo": "laser", "t": 8.0, "ate": 12.0, "gatilho": "cabeca-vira", "dur": 0.7 }
```

### `piscada`

O "clique" visual: no fundo da piscada, um anel fino (rosa com fio branco) abre em volta do olho, quatro
risquinhos saem dele (para cima, em diagonal e para fora; nenhum desce sobre a bochecha) e um brilho baixo
acende a pálpebra só no começo. 0,42 s. Com `olho` no evento (a piscadela), só o olho que piscou.

| campo | padrão | |
|---|---|---|
| `gatilho` | `"piscada"` | `"piscada-dupla"` também serve |
| `dupla` | `false` | `true` = só as piscadas duplas |
| `dur` | 0,42 | s |

Som `clique` (a segunda piscada de uma dupla fica sem som, pela regra de 1,5 s). Boa pontuação de frase
curta ("Também não.").

```json
{ "tipo": "piscada", "t": 18.4, "ate": 19.7, "gatilho": "piscada", "dupla": true }
{ "tipo": "piscada", "t": 6.8, "ate": 9.9 }
```

### `fala-onda`

A voz saindo da boca: a cada 0,1 s nasce, dos dois lados da boca, um arco fino que anda para fora por 0,6 s;
a altura (abertura do arco), o brilho e a grossura dele são os da abertura da boca (jawOpen) no instante em
que nasceu, então as ondas desenham o ritmo da fala e somem no silêncio. Recortadas fora do oval do rosto;
traço de 2 a 4 px, alternando rosa e branco.

| campo | padrão | |
|---|---|---|
| `lado` | `"ambos"` | `"esquerda"`, `"direita"` |
| `intensidade` | 1 | 0,2 a 2 |

Sem som. Entra como evento visual de peso 1, e cada `boca-aberta` dentro da vida (depois de 0,3 s) também
marca um `acende` de peso 1 (as ondas crescem ali, e o gate de ritmo conta). Combina com "megafone", "grito", "a pergunta certa".

```json
{ "tipo": "fala-onda", "t": 24.15, "ate": 26.2 }
```

### `emoji-reacao`

Um ícone vetorial desenhado na própria peça (SVG; nada de emoji de fonte de terceiros): `exclamacao` (!),
`interrogacao` (?), `coracao`, `estrela` e `surpresa` (o rosto surpreso, o selo inteiro no rosa), num selo
escuro de borda rosa. Salta ao lado da cabeça no evento (pop com passada, 0,32 s, com oito raios), balança e
sobe 22 px devagar, e sai encolhendo em 0,18 s. O lugar é escolhido no nascimento: o lado com mais espaço
(ou `lado`), entre a testa e os olhos, fora do oval do rosto, dentro da zona segura. O ícone leva `data-zona`
(entra no gate de zonas; não é letra).

| campo | padrão | |
|---|---|---|
| `gatilho` | `"sorriso|sobrancelha|boca-aberta"` | |
| `icone` | `"auto"` | auto: sorriso → coração, sobrancelha → !, boca-aberta → surpresa, piscada → estrela, cabeca-vira → ? |
| `lado` | `"auto"` | `"esquerda"`, `"direita"` |
| `tam` | 150 | px (80 a 260) |
| `dur` | 1,1 | s de cada ícone (0,5 a 3) |

Som `pop`. Até 6 por peça, um de cada vez.

```json
{ "tipo": "emoji-reacao", "t": 16.3, "ate": 17.5, "gatilho": "sobrancelha", "icone": "interrogacao" }
{ "tipo": "emoji-reacao", "t": 23.2, "ate": 24.4, "gatilho": "sorriso" }
```

### `mascara-tech`

"A IA lendo o rosto": a malha de 83 pontos acende de cima para baixo atrás de uma linha de varredura (a
linha branca com o rastro em ciano), fica pulsando de leve (os pontos piscam em branco), e some numa segunda
varredura de cima para baixo. A aresta e o ponto perto da linha acendem em branco e rosa. Quatro cantos de
mira rosa em volta do rosto. O contorno dos olhos só aparece no instante em que a linha passa (um flash): a
malha nunca fica por cima dos olhos.

| campo | padrão | |
|---|---|---|
| `t`, `ate` | — | ~1 a 1,5 s; a entrada é 40% da vida (até 0,42 s) e a saída 30% (até 0,36 s) |
| `cor` | `"ciano"` | a cor das arestas; o acento é sempre o rosa |

Som `bip` na entrada. Boa abertura de reel ("A empresa AI First").

```json
{ "tipo": "mascara-tech", "t": 0.1, "ate": 1.25 }
```

### `zoom-reacao`

O soco de zoom: no evento, a vista do rosto aproxima de 1 para `escala` em 0,12 s (power4.out), segura e
volta em 0,4 s. Não há uma API de zoom para sobreposição no motor; a peça usa a **mesma camada do zoom de
ênfase** (`vista.zoom`, centrada no rosto pelo motor) através da API pública `M.anim.camera`, então a legenda
(que mede os quadros pela linha do tempo), os gates e as outras peças presas ao rosto enxergam o zoom. Por
cima, um anel rosa em volta do rosto e linhas de velocidade das bordas da janela para o rosto, só nos
primeiros 0,45 s. O soco que cruza um `zoom` de ênfase da mesma cena é recusado com Error (os dois mexem na
mesma camada); o zoom das emendas mora em outra camada e convive.

| campo | padrão | |
|---|---|---|
| `gatilho` | `"boca-aberta|sobrancelha"` | |
| `escala` | 1,12 | 1,03 a 1,3 |
| `segura` | 0,35 | s |
| `linhas` | `true` | `false` tira as linhas de velocidade |

Som `impacto` (evento `zoom`, peso 2; o `M.anim.camera` registra também os eventos `camera`). Evite em trecho
de gesto (o zoom sobe a cabeça e a legenda perde o alto, MOTOR.md 4.10).

```json
{ "tipo": "zoom-reacao", "t": 4.6, "ate": 5.2, "gatilho": "boca-aberta" }
{ "tipo": "zoom-reacao", "t": 32.4, "ate": 32.8, "em": [32.44], "escala": 1.1 }
```

---

## 3. Determinismo, custo e limites

- **Determinismo**: nada de `Math.random`, `Date` ou `requestAnimationFrame`. Tudo é conta fechada do
  instante e dos dados do quadro; as faíscas do laser e as linhas do zoom nascem com `M.fx.semente`.
  Visibilidade do ícone só em `tl.set`; o desenho, por quadro, no `M.aCada`; nada guardado entre quadros fora o
  cache dos sprites de brilho.
- **Custo medido** (M4, demo corte 51, 1084 quadros com 18 peças desta frente, 2 cards e a legenda, sem
  WebGL; a máquina com outros renders rodando): 102 a 105 ms por quadro no render inteiro (110 a 113 s).
  As peças são canvas 2D: o mais caro é o `laser` (um `filter: blur` no brilho largo) e a `mascara-tech`
  (~200 arestas por quadro). Nenhuma pede GPU. O `--quadro` sozinho e o mesmo quadro no render em
  sequência diferem só no ruído do h264 (média 3,0 níveis, p99 9).
- **Limites**:
  - Os efeitos seguem o que o Face Landmarker acha. Rosto muito de lado (mais de ~40° de yaw), mão na frente
    da boca ou do olho, ou rosto pequeno (gravação de tela com a webcam no canto) dão pontos piores: confira a
    folha.
  - A sobrancelha e o sorriso dependem da pessoa: quem fala sempre sorrindo dá sorriso raro (o nível dos 2 s
    de antes sobe junto), quem mexe a sobrancelha o tempo todo dá surpresa demais.
  - O `laser` aponta pela pose da cabeça, não pela íris: com a cabeça de frente, o V para quem assiste é o
    padrão; para mirar em algo da tela, use `alvo`.
  - O `emoji-reacao` escolhe o lugar no nascimento com a conta aproximada (sem os zooms): com zoom de ênfase
    ou soco de zoom no mesmo instante, ele pode ficar até ~60 px mais perto da cabeça. Não ponha o ícone no
    mesmo instante de um `zoom-reacao`.
  - Numa vista girada em 3D, a conta é a caixa que envolve a imagem (como o `M.fonteParaTela`).
