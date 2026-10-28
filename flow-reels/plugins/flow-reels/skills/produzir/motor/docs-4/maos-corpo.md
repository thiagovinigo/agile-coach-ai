# Mãos e corpo (4.0)

Efeitos presos às mãos e ao corpo de quem fala: faíscas nas pontas dos dedos, esfera de energia entre as
mãos, tela segurada, feixe do dedo que aponta, onda nas palmas, eco, sombra, raio e aura. Duas peças:

| arquivo | o que faz |
|---|---|
| `scripts/gestos.py` | lê a visão do corte e grava `visao/gestos.json`: o gesto de cada mão por quadro e os eventos (palmas, abre, varrida, aponta, conta, ênfase) |
| `motor/web/sobre/maos-fx.js` | as 11 sobreposições: `faiscas`, `rastro`, `contar`, `energia`, `tela-maos`, `feixe`, `onda`, `eco`, `sombra`, `raio`, `aura` |

A base é a pesquisa `docs/pesquisa-4-0/02-maos-corpo-e-frames-3d.md` (1.2 gestos, 1.3 suavização,
1.4 máscara da mão, 1.6 determinismo). A demo é o corte 42 de `projetos/teste-onda-1`.

---

## 1. `gestos.py`: o que as mãos estão fazendo

```
flow-reels produzir/gestos --projeto projetos/<v> --corte NN
flow-reels produzir/gestos --projeto projetos/<v> --corte NN --resumo
flow-reels produzir/gestos --projeto projetos/<v> --corte NN --folha
```

- **Precisa** da visão do corte (`visao.py`): `maos.json`, `corpo.json`, `visao.json` (os segmentos entre
  emendas) e `.origem.json`. Lê também `palavras-corte.json` (a ênfase) e `cenas.json` → `legenda.enfase`.
- **Roda em ~1 s** (36 s de vídeo). Rode de novo sempre que rodar o `visao.py`: o `gestos.json` guarda a
  origem da visão que leu, e o `compor.py` só entrega ao motor o que é do mesmo vídeo.
- `--resumo` imprime os momentos úteis para escolher gatilhos (sem regravar, se o `gestos.json` já é
  desta visão): presença e gesto de cada mão, os trechos "segurando", os trechos com as duas mãos, cada
  evento com a palavra dita ali, e a porcentagem de mão "no palco" a cada 2 s.
- `--folha [caminho]` grava a folha de contato (padrão `folha-gestos.jpg` na pasta do corte): um quadro
  por evento com o esqueleto suavizado, os dedos esticados e o gesto escritos. **Olhe antes de planejar.**
- Saída 0 = gravou; 1 = gravou, mas há mão em menos de 10% dos quadros; 2 = falta a visão ou as mãos.

**O caminho.**
1. **Lado**: o do `maos.json` (de quem assiste). Conferido pelos pulsos do corpo (pose 15 e 16): o pulso
   da mão claramente no pulso do outro lado da tela por 3 quadros ou mais troca as mãos. A leitura repetida
   (duas "mãos" a menos de 0,45 palma uma da outra) vira uma.
2. **Limpeza**: salto do centro da palma maior que 1,5 s que volta no quadro seguinte é descartado; buraco
   de até 6 quadros no meio de um trecho é preenchido por Catmull-Rom. Nada atravessa emenda.
3. **Suavização zero-phase**: One Euro para a frente e para trás, a média das duas, em unidades de mão
   (coordenada / s mediano do trecho). Pontas dos dedos `minCutoff 1,6 Hz, beta 0,6`; palma e juntas
   `1,0 / 0,4`; a escala `s` e a distância entre as palmas são suavizadas à parte, mais forte (`0,4 / 0,1`),
   porque efeito que cresce com elas não pode tremer.
4. **Dedos** (3D, o `z` do MediaPipe na escala do `x`): estendido com ângulo no PIP < 35° e
   `d(ponta, punho) > 1,15·d(PIP, punho)`; curvado acima de 70°; no meio, o estado anterior (histerese).
   Polegar: `d(4,17) > 1,2·d(3,17)` e ângulo no IP < 40° (sai abaixo de 1,08 ou acima de 55°).
5. **Gesto**: `pinca` (entra `d(4,8)/s < 0,25`, sai > 0,40), `punho`, `joinha`, `aponta`, `vitoria`,
   `aberta` (5 dedos, ou 4 com abertura > 8°), `contando-N`, `nenhum`. Só vale o gesto que dura 5
   quadros ou mais; o trecho mais curto herda o vizinho. Offline, o gesto estável vale **desde o primeiro
   quadro** em que apareceu (não 5 quadros depois).
6. **Presença** `a` (0 a 1): sobe em 6 quadros quando a mão chega; quando ela some, a mão fica parada na
   última pose e `a` desce em 6 quadros (nunca pula); desce também quando o centro da palma sai pela borda
   (a mão cortada embaixo, comum no busto). A emenda corta seco (a imagem pula junto).
7. **Duas mãos**: distância entre as palmas em mãos (`s` médio) e em ombros (pose 11–12); `segurando` =
   as duas com 3 dedos ou mais esticados, de 0,8 a 4 mãos de distância (sai abaixo de 0,65 ou acima de
   4,6), na mesma altura (< 1,3 s), por 6 quadros ou mais.

**Os eventos** (todos com `tipo`, `quadro`, `t`, `mao` e `x, y` em pixels da fonte):

| tipo | quando | campos extras |
|---|---|---|
| `palmas` | a distância entre as palmas cai mais de 1,2 s em até 5 quadros e fica abaixo de 1,0 s (o primeiro quadro já junto) | `mao: "ambas"` |
| `abre` | punho → aberta em até 10 quadros (`como: "punho"`), ou as mãos se afastando > 0,15 s por quadro por 4 quadros, partindo de menos de 2,5 mãos (`como: "afastando"`) | `de`, `ate_dist`, `dur`, `s` |
| `varrida` | velocidade horizontal da palma > 0,35 s por quadro por 3 quadros, no mesmo sentido; o quadro mais rápido; 12 quadros entre duas | `sentido` (+1 direita), `vel`, `de`, `ate` |
| `aponta-inicio`, `aponta-fim` | gesto `aponta` estável por 6 quadros ou mais | `dir` [dx, dy], `camera` (apontando para a câmera), `ponta`, `dur` |
| `conta` | o número de dedos fica igual por 5 quadros ou mais, numa configuração de contagem (1 = indicador; 2 = indicador e médio ou polegar e indicador; 3, 4, 5), com a mão quieta (< 0,12 s por quadro), de pé (dedos para cima em 60% dos quadros) e longe da outra (> 1,8 mãos: mãos entrelaçadas dão "1" e "4" falsos); só quando o número muda | `n`, `dedos`, `dedo` (a ponta do último levantado), `dur` |
| `enfase` | pico da velocidade vertical da palma (> 0,10 s por quadro) a ±3 quadros do início de uma palavra tônica (fora das paradas, 4 letras ou mais, número ou `legenda.enfase`) | `palavra`, `vel` |

**`visao/gestos.json`** (o `compor.py` entrega em `window.VISAO.gestos`):

```json
{ "versao": 1, "fonte": "fala.mp4", "fps": 30, "largura": 576, "altura": 1024, "total": 1084,
  "segmentos": [[0, 23], [23, 347], [347, 1084]],
  "origem": { "video": "/…/fala.mp4", "mtime": 1791418438.15, "tamanho": 13048304, "fps": 30 },
  "lado": "de quem assiste: esquerda = a mão à esquerda na tela", "limiares": { … }, "relatorio": { … },
  "maos": { "esquerda": [ null | { "a": 1.0, "g": "aberta", "n": 5, "dedos": [1,1,1,1,1], "pinca": 0.84,
                                   "C": [x, y], "s": 92.4, "dir": [dx, dy], "camera": false,
                                   "v": [vx, vy], "medido": true, "p": [[x, y] × 21] } ],
            "direita": [ … ] },
  "duas": [ null | { "dist": 3.1, "ombros": 0.9, "meio": [x, y], "segurando": true } ],
  "eventos": [ { "tipo": "palmas", "quadro": 59, "t": 1.967, "mao": "ambas", "x": 288.1, "y": 895.4 } ] }
```

Um registro por quadro do vídeo (`null` = sem mão). `p` são os 21 pontos já suavizados (o motor desenha
com eles, não com o `maos.json`). `v` é a velocidade do centro da palma em px por quadro; nos quadros da
saída (a mão parada na última pose) vem 0. `medido` é `false` no quadro preenchido e na saída.

**O que o vídeo de teste mostrou** (corte 42, busto, mãos na altura do peito, muitas vezes entrelaçadas):
- O MediaPipe perde a mão rápida e borrada (de 18 a 24 s quase não há mão, embora elas estejam na
  tela). Para esses trechos, use as peças do corpo (`eco` pessoa, `sombra`, `aura`).
- Mãos entrelaçadas e em prece são o gesto mais comum; elas dão `palmas` (bom gatilho de `onda`) e
  "segurando" curto. A contagem verdadeira é rara: o planejador pode marcar os passos do `contar` à mão
  com `em` (abaixo).
- O lado conferido pelos pulsos trocou 9 quadros; 30 leituras repetidas viraram uma.

---

## 2. As sobreposições (`sobre/maos-fx.js`)

Todas vão em `cena.sobre` (numa cena com o rosto na tela: `rosto-vidro`, `vidro-liquido` de frente,
`camadas`) ou em `CENAS.sobre` (seguem a vista do rosto da cena da vez). Precisam do `gestos.json` e da
visão; sem eles, o motor recusa o plano com o Error que diz o que rodar.

**Campos comuns**

| campo | padrão | o que é |
|---|---|---|
| `t`, `ate` | a cena | a vida da peça; entra e sai em 0,2 s |
| `mao` | `"auto"` | `"esquerda"`, `"direita"`, `"ambas"` ou `"auto"` (a mão mais presente e mais alta na vida da peça) |
| `gatilho` | — | um tipo de evento do `gestos.json` (ou vários com `"|"`, como `"varrida|abre"`): o efeito acontece em cada evento desse tipo dentro de `[t, ate]` (e da mão pedida) |
| `cor` | `"destaque"` | `"destaque"` (o rosa chapado), `"tinta"` (branco), `"ciano"` ou `#RRGGBB` |
| `som` | o da peça | um som válido, ou `false`; no máximo um a cada 1,5 s por peça |

Com `gatilho` sem nenhum evento no trecho, a peça avisa no console e não aparece (rode o `--resumo`).

**As camadas** (pesquisa 1.4). Cada peça desenha num canvas 1080 x 1920 dentro da própria raiz, preso à
vista do rosto pela conta exata do quadro (`getBoundingClientRect` da imagem: enquadre, zoom de ênfase,
zoom das emendas, transição) e recortado pela janela da vista:
- **atrás da pessoa** (`eco` pessoa, `sombra`, `aura`): desenhados e furados pela máscara do próprio
  quadro (a máscara vira alfa num canvas). Não precisam de `"atras": true`.
- **entre as mãos** (`energia`, `tela-maos`): por cima do vídeo e, por cima deles, **a mão recortada**:
  os pixels do próprio quadro dentro da máscara da mão = cápsulas nos ossos dos 21 pontos (raio ~0,11 s,
  palma cheia, pontas um pouco mais largas) ∩ máscara da pessoa. Os dedos passam na frente. A mão rápida
  (> 0,28 s por quadro, borrada no vídeo) perde a máscara aos poucos: os pontos não batem com o borrão, e
  recortar ali estampava um pedaço de peito no lugar errado.
- **na frente** (`faiscas`, `rastro`, `raio`, `feixe`, `onda`, o halo da `energia`).

A máscara da pessoa entra como fonte do motor (`mfx-mascara`), com vistas invisíveis de 1 px por atraso
(0 = o quadro, d = d quadros antes), visíveis só na vida da peça: o render espera o PNG decodificado antes
dos ganchos. O `eco` carrega do mesmo jeito os quadros de vídeo anteriores.

### `faiscas`

Partículas saindo das pontas dos dedos esticados: traço curto na direção da velocidade, núcleo branco que
esfria para o rosa, arrasto e gravidade leve. Sem gatilho, emissão contínua (mais forte com a mão rápida,
herdando a velocidade dela) e um brilho pulsando em cada ponta; com gatilho, uma rajada por evento (no
`abre` e nas `palmas`, em leque a partir do centro).

| campo | padrão | |
|---|---|---|
| `dedos` | `"estendidos"` | `"todos"` ou `"indicador"` |
| `quantidade` | 1 | 0,2 a 4 (a rajada tem 34 x quantidade por mão) |
| `vida` | 0,55 | s de vida média de uma partícula (0,2 a 1,5) |
| `gravidade` | 1 | |

Som `tick` (na entrada, ou em cada rajada). Determinística: cada quadro de nascimento emite com semente
`(nome, quadro, mão, dedo)` e a posição é uma conta fechada da idade (sem estado). As partículas vivem no
espaço da fonte: a câmera parada as deixa no lugar quando a mão sai.

```json
{ "tipo": "faiscas", "t": 2.7, "ate": 3.6, "gatilho": "abre", "quantidade": 1.4 }
{ "tipo": "faiscas", "t": 5.0, "ate": 6.8, "mao": "ambas" }
{ "tipo": "faiscas", "t": 20.6, "ate": 21.7, "gatilho": "abre", "quantidade": 1.8, "cor": "tinta" }
```

### `rastro`

Fita de luz que afina e some na cauda: os pontos dos últimos `comprimento` quadros (do mesmo trecho),
alisados por Catmull-Rom, em três passadas aditivas (brilho largo, rosa, núcleo branco) e um brilho na
cabeça. A mão parada não deixa fita.

| campo | padrão | |
|---|---|---|
| `ponto` | `"indicador"` | `"palma"`, `"pontas"` (as cinco: o light painting), `"medio"`, `"polegar"` |
| `comprimento` | 12 | quadros (4 a 30) |
| `largura` | 20 | px de saída na cabeça (na escala 1,875 da vista cheia) |

Com gatilho, aparece nas janelas dos eventos (a `varrida` do `de` ao `ate` + 0,35 s; o `aponta-inicio` até
o `aponta-fim`). Sem som. Fica melhor com `"pontas"` e `"gatilho": "varrida|abre"`.

```json
{ "tipo": "rastro", "t": 14.3, "ate": 15.6, "gatilho": "varrida" }
{ "tipo": "rastro", "t": 26.3, "ate": 27.5, "mao": "direita", "ponto": "pontas", "largura": 14, "comprimento": 10 }
```

### `contar`

O número (e/ou o item da lista) num card escuro ao lado da mão que conta, e as pontas dos dedos esticados
acesas (a do último dedo levantado mais forte), com uma linha fina da ponta até o card. O card nasce com
pop e é trocado a cada passo no mesmo lugar (um contador; um card que pulasse de lado a cada passo cansa),
escolhido no primeiro passo: do lado de fora da mão, acima dela, fora do rosto, na zona segura.

| campo | padrão | |
|---|---|---|
| `itens` | — | a lista: o item `i` entra no passo `i` (em maiúsculas) |
| `numero` | `true` | `false` mostra só o item |
| `em` | — | os instantes dos passos, à mão (vale mais que o gatilho) |
| `gatilho` | `"conta"` | outro evento (ex.: `"enfase"`) faz cada evento avançar um passo |
| `lado` | auto | `"esquerda"` / `"direita"`: de que lado da mão fica o card |

Com o gatilho `conta` e sem itens, o número é o `n` do evento (os dedos); com itens, é o passo. Som `pop` em
cada passo (respeitando 1,5 s). Texto: `data-texto` no número e no item; o card tem o fundo escuro (0,9).

```json
{ "tipo": "contar", "t": 12.55, "ate": 14.3, "mao": "esquerda",
  "itens": ["aprova", "paga", "cancela", "grava"], "em": [12.62, 13.04, 13.3, 13.82] }
```

### `energia` (WebGL2)

Esfera de energia: núcleo branco, corpo de plasma no rosa, borda com fresnel, quatro filamentos girando e
um halo. Entre as duas mãos (centro no meio das palmas, um pouco acima; raio ~0,34 da distância, de 0,55
a 2,4 s), com os dedos por cima (só sobre o corpo da esfera: o halo continua por cima dos dedos, a luz bate
neles). Com uma mão só (ou `modo: "palma"`), flutua na frente da palma, sem recorte. Centro e raio são a
média de ±4 quadros (sem atraso, sem estado). Nasce crescendo com passada (0,35 s), pulsa (1,3 e 3,1 Hz) e
a luz vaza na pessoa (aditiva, só dentro da máscara).

| campo | padrão | |
|---|---|---|
| `modo` | `"auto"` | `"entre"` (só com as duas mãos), `"palma"` |
| `tam` | 1 | escala do raio (0,4 a 2,2) |
| `luz` | `true` | a luz rosa vazando no peito e no rosto |
| `dur` | 1,6 | s de cada aparição com gatilho |

Som `energia`. O shader é próprio (ruído de valor 3D e fbm escritos aqui), num canvas WebGL2 de 1024 x 1024
fora do DOM, copiado para o canvas 2D da peça. **Vai para o `gpu.json`.**

```json
{ "tipo": "energia", "t": 6.9, "ate": 8.8 }
{ "tipo": "energia", "t": 31.3, "ate": 32.6, "modo": "palma", "mao": "direita" }
```

### `tela-maos`

Um painel de vidro escuro (faixa rosa no alto) segurado entre as duas mãos: as bordas laterais presas às
palmas, um pouco para dentro de cada mão (os dedos cobrem a borda), inclinado com a linha das mãos, com a
borda mais alta do lado da mão maior (mais perto) e subindo `sobe` da altura (as palmas seguram pela parte
de baixo). O conteúdo abre de uma linha na entrada. Sem as duas mãos (ou com elas a menos de 1,1 s ou a
mais de 8), o painel encolhe para o centro e some. O texto fica na zona segura: o painel sobe e anda para
dentro quando o miolo do texto passaria da base (y 1440) ou da margem.

| campo | padrão | |
|---|---|---|
| `texto` | — | `*palavra*` no rosa; ou `numero`, ou a imagem (`acervo`, `src`) com texto embaixo |
| `aspecto` | 0,62 | altura / largura (0,3 a 1,4) |
| `sobe` | 0,3 | quanto o painel sobe acima das palmas, em fração da altura (0 a 0,5) |
| `tam` | auto | corpo do texto |

O painel é DOM (o texto tem `data-texto`), posto por `matrix3d` (a homografia dos 4 cantos): por sets na
linha do tempo, um por quadro, com a conta aproximada (para a legenda que mede outros quadros) e reposto no
gancho com a conta exata. No meio da entrada e da saída, o texto leva `data-saindo`. Som `whoosh`.
Precisa de 0,6 s ou mais com as duas mãos abertas e afastadas (`--resumo` → "segurando").

```json
{ "tipo": "tela-maos", "t": 0.1, "ate": 0.85, "texto": "AI *FIRST*" }
{ "tipo": "tela-maos", "t": 25.45, "ate": 26.15, "texto": "DATA *FIRST*", "sobe": 0.45, "aspecto": 0.5 }
```

### `feixe`

Ao apontar, um feixe sai da ponta do indicador e vai até o alvo em 0,22 s; pulsos correm por ele, a ponta
brilha, e o alvo dá um clarão. Com `texto`, um card (borda rosa à esquerda) acende no fim do feixe.

| campo | padrão | |
|---|---|---|
| `gatilho` | `"aponta-inicio"` | cada apontar vira um disparo (até o `aponta-fim` + 0,3 s, no mínimo 0,9 s); `null` = a vida inteira, da mão escolhida |
| `alvo` | auto | `[x, y]` em px de saída; sem ele, 520 px à frente do dedo (fora do rosto) |
| `texto` | — | o card no alvo (cresce para dentro da tela) |
| `dur` | — | s de cada disparo (fixo) |

Som `subida`. Até 4 disparos por peça. O card fica parado onde nasce; o feixe segue a ponta do dedo. Apontar
para a câmera (dedo encurtado) não dá direção: o feixe sobe.

```json
{ "tipo": "feixe", "t": 0.72, "ate": 1.9, "mao": "direita", "texto": "CUIDADO", "alvo": [1000, 700] }
```

### `onda`

Onda de choque: um anel que cresce do ponto do evento (o encontro das palmas, a mão que abre) em 0,75 s,
empurrando a imagem para fora numa faixa (refração falsa: o próprio quadro ampliado 4,5% dentro do anel,
fora do rosto), clareando a faixa, com o traço branco e rosa, um segundo anel mais fino e o clarão do começo.

| campo | padrão | |
|---|---|---|
| `gatilho` | `"palmas|abre"` | sem evento no trecho, uma onda só, no `t` |
| `raio` | 760 | px de saída no fim |
| `forca` | 1 | 0,2 a 2 |
| `dur` | 0,75 | s |

Som `impacto` (peso 3). Uma onda por vez: a seguinte precisa de 0,5 s.

```json
{ "tipo": "onda", "t": 1.85, "ate": 2.7, "gatilho": "palmas" }
{ "tipo": "onda", "t": 16.0, "ate": 16.9, "gatilho": "palmas", "forca": 1.3 }
```

### `eco`

Cópias fantasmas de quadros anteriores (`passo`, `2·passo`, ... quadros antes), cada vez mais fracas (0,68
por cópia), sem atravessar emenda.
- `alvo: "pessoa"`: cada cópia é o quadro antigo recortado pela máscara dele, tingido de rosa, atrás da
  pessoa de agora. Aparece onde o corpo esteve e não está mais (o braço, a cabeça que mexeu).
- `alvo: "maos"`: o eco é a **diferença**: os pixels do quadro antigo perto de onde a mão estava (cápsulas
  engordadas e borradas) que mudaram até agora, multiplicados pelo rosa; o canvas entra em
  `mix-blend-mode: screen` sobre o vídeo. A pele que saiu dali vira luz rosa, a camiseta escura some: o
  fantasma tem os dedos de verdade.

| campo | padrão | |
|---|---|---|
| `alvo` | `"pessoa"` | `"maos"` |
| `copias` | 4 | 1 a 6 |
| `passo` | 3 | quadros entre cópias (1 a 8) |
| `opacidade` | 0,6 | |

Acende um pouco (e marca um evento visual, sem som) em cada gesto rápido da vida dela (varrida, abre,
palmas, ênfase, um a cada 1 s).

```json
{ "tipo": "eco", "t": 10.6, "ate": 12.5, "alvo": "maos", "copias": 4, "passo": 3 }
{ "tipo": "eco", "t": 17.9, "ate": 20.3, "alvo": "pessoa", "copias": 5, "passo": 3, "opacidade": 0.8 }
```

### `sombra`

A sombra dura da pessoa na parede: a máscara (do quadro, ou de `atraso` quadros antes: a sombra que age
sozinha) ondulada em 48 faixas por um seno lento (a parede não é plana), deslocada, inclinada e escalada em
volta da base do quadro, borrada, escura e translúcida, furada pela pessoa.

| campo | padrão | |
|---|---|---|
| `dx`, `dy` | 70, 24 | px de saída (negativo = para a esquerda / para cima) |
| `inclina` | -0,18 | cisalhamento (−0,8 a 0,8) |
| `escala` | 1,03 | |
| `opacidade` | 0,5 | |
| `desfoque` | 3 | px |
| `atraso` | 0 | quadros (0 a 24) |
| `ondula` | 1 | 0 desliga |
| `cor` | quase preto | |

Sem som.

```json
{ "tipo": "sombra", "t": 3.2, "ate": 5.0, "atraso": 8, "dx": 90, "dy": 10 }
{ "tipo": "sombra", "t": 21.9, "ate": 23.9, "dx": -120, "dy": 0, "inclina": 0.3, "opacidade": 0.55, "desfoque": 6 }
```

### `raio`

Raios ramificados: deslocamento de ponto médio recursivo (6 níveis, amplitude 0,22 do comprimento, 0,55 por
nível), semente nova a cada 2 quadros, ramos com chance 0,3, quatro passadas aditivas e o brilho nas duas
pontas. O que cruzaria o rosto faz um arco por baixo dele.
- Duas mãos: entre as pontas iguais dos dedos esticados nas duas (até 3). Com as mãos juntas (as pontas
  iguais a menos de 0,7 s), cruzado: polegar de uma ao mínimo da outra, e assim por diante.
- Uma mão (`modo: "pinca"`, ou `auto` sem a outra): polegar ↔ indicador (com a pinça aberta mais de
  0,35 s) e indicador ↔ médio quando os dois estão esticados.

| campo | padrão | |
|---|---|---|
| `modo` | `"auto"` | `"maos"`, `"pinca"` |
| `dur` | 0,9 | s de cada aparição com gatilho |

Som `raio`.

```json
{ "tipo": "raio", "t": 24.0, "ate": 24.9, "modo": "pinca", "mao": "direita" }
{ "tipo": "raio", "t": 28.0, "ate": 29.6, "modo": "maos" }
```

### `aura`

Contorno neon em volta da pessoa: a máscara borrada (meia resolução) cortada em faixas chapadas do lado de
fora (rosa, cada uma mais fraca: 0,62, 0,36, 0,21...) e um fio claro colado no contorno; a base do quadro não
ganha aura. Respira devagar (0,6 Hz) e pulsa (largura e brilho, queda em ~0,2 s) nos eventos de ênfase do
gesto e, nos buracos de mais de 1,6 s entre eles, no começo das palavras longas da fala (um pulso a cada
0,9 s no máximo). Fica atrás da pessoa.

| campo | padrão | |
|---|---|---|
| `largura` | 30 | px de saída do borrão (8 a 90) |
| `faixas` | 3 | 1 a 6 |
| `pulso` | `"enfase"` | outro tipo de evento, ou `null` (só a fala) |

Cada pulso é um evento visual (sem som); a entrada é peso 2.

```json
{ "tipo": "aura", "t": 32.7, "ate": 36.145 }
```

---

## 3. Determinismo, custo e limites

- **Determinismo**: nada de `Math.random`, `Date` ou `requestAnimationFrame`; a aleatoriedade sai de
  `M.fx.semente(nome, quadro)`. Faíscas, rastro, eco e as médias de janela são recalculados do zero a cada
  quadro a partir dos dados de quadros anteriores. O que fica guardado entre quadros são só caches de
  conteúdo (a máscara convertida em alfa, por endereço; os sprites de brilho). Conferido no corte 42: o
  `--quadro` sozinho e o mesmo quadro no render em sequência diferem só no ruído do h264 (média 2,9 a 3,3
  níveis, igual ao quadro sem efeito).
- **Custo medido** (M4, `"gpu": true`, render inteiro do corte 42 com 21 peças: 59 a 62 ms por quadro; com
  outros renders na máquina, ~100). Por trecho, contra ~50 ms do quadro sem peça: `energia` +4 ms, `aura`
  ~0, `tela-maos`/`feixe`/`onda` +5, `sombra`/`faiscas` +9, `contar` +4, `eco` pessoa ~0, **`eco` mãos
  +28 ms** (a diferença de 4 quadros em pixels, a meia resolução). O pior trecho ficou em 78 ms.
- **GPU**: só a `energia` usa WebGL (WebGL2 puro, shader próprio). Sem `"gpu": true` nem a entrada no
  `gpu.json`, ela roda no SwiftShader (certo, mais lento).
- **Limites**:
  - Os efeitos seguem o que o MediaPipe acha. Mão borrada e rápida some dos dados (o efeito some com ela,
    em 6 quadros) ou fica com os pontos atrasados: `raio` e `tela-maos` em mão rápida podem apontar para
    onde a mão estava. Prefira gestos parados ou lentos para as peças de duas mãos.
  - A máscara da mão é por cápsulas (não há segmentação da mão): com a mão parada, a borda tem ~1 a 2 px de
    peito em volta dos dedos. Por isso a energia só recorta sobre o corpo da esfera.
  - A posição do texto (card do `contar`, do `feixe`, o painel da `tela-maos` na linha do tempo) usa a
    conta aproximada (sem os zooms): ela erra até ~60 px perto da base com o zoom das emendas. O desenho
    preso à mão usa sempre a conta exata.
  - Numa vista girada em 3D, a conta é a caixa que envolve a imagem (como o `M.fonteParaTela`).
  - A `aura` e a `sombra` usam a máscara do quadro; cabelo solto e borda tremendo aparecem nelas.
