# Transições e palavras (4.0)

Duas peças da 4.0 que mexem no mesmo lugar do reel, a virada entre cenas e a palavra grande acima da
cabeça:

- **nove transições novas** em `web/transicoes-4.js`: `glitch`, `vhs`, `queima`, `pixels`, `persianas`,
  `cubo`, `forma`, `tinta`, `zoom-atraves`;
- **oito efeitos novos da palavra** em `web/sobre/palavra.js`: `decodifica`, `brutal`, `marcatexto`, `neon`,
  `carimbo`, `cromado`, `vazado`, `pixel`. Os cinco antigos (`glitch`, `digitacao`, `extrusao`, `pula`,
  `conta`) continuam iguais, no mesmo código.

Nada pede WebGL: tudo é CSS, SVG (filtros) e canvas 2D, e roda sem GPU. Nenhuma dependência nova (o
`vazado` usa o opentype.js que o texto 3D já trouxe). Nada usa `Math.random`, `Date` ou `performance.now`:
o mesmo quadro sai igual em sequência ou sozinho (`--quadro`). A demo com todas as peças é o corte 44
(`projetos/teste-onda-1/corte-44/corte-44.mp4`), e a folha de quadros dela é
`materiais-de-trabalho/corte-44/folha-4-0.jpg`.

```json
{ "id": "c2", "inicio": 2.92, "fim": 5.72, "entrada": { "transicao": "glitch" } }
{ "id": "c8", "inicio": 17.2, "fim": 19.45, "entrada": { "transicao": "forma", "forma": "circulo", "revela": "pilula", "duracao": 0.6 } }
{ "tipo": "palavra", "efeito": "decodifica", "texto": "AI FIRST", "t": 0.12, "ate": 1.8, "y": 330 }
{ "tipo": "palavra", "efeito": "brutal", "texto": "REPETE|PIOR", "trocas": [11.95], "caixa": true, "t": 10.62, "ate": 12.45, "y": 300 }
```

---

## 1. Transições

### 1.1 O contrato (o mesmo do `transicoes.js`)

- Vão na cena **que entra**: `"entrada": { "transicao": "<nome>", "duracao": <s>, ...parâmetros }`.
- A troca acontece no `inicio` da cena nova. Cada transição mexe numa janela em volta dele (tabela abaixo),
  marca essa janela no motor (`Motor.janela`, que os gates usam para não medir texto no meio da virada) e
  grava **um** evento `transicao` de peso 3 com o seu som.
- Depois da janela nada sobra nas cenas: nem filtro, nem recorte, nem transformação, nem `z-index`. O
  quadro seguinte é o de um corte seco.
- Tudo acontece na camada das cenas, **abaixo da legenda**: a legenda nunca é rasgada, borrada ou girada.
- `"duracao"` fora da faixa da transição é Error (com a faixa na mensagem). Parâmetro de lista fechada com
  valor desconhecido também.
- **Cruzamento.** A janela de entrada e a de saída da mesma cena não podem se cruzar nem passar da cena (as
  duas mexem no estilo dela). A conta vale entre as nove novas e as seis antigas que mexem no estilo da
  cena (`desfoque`, `inclinada`, `mergulho`, `zoom-desfoque`, `chicote`, `mascara`). O plano que faz isso é
  recusado, com o nome da cena e o que fazer: alongar a cena ou encurtar a `duracao`.

### 1.2 As nove

As janelas estão em múltiplos da duração, em relação ao `inicio` (de = o lado da cena que sai, para = o da
que entra).

| nome | padrão | faixa | janela | som | o que faz |
|---|---|---|---|---|---|
| `glitch` | 0,40 s | 0,2 a 1,0 | -0,6 a +0,4 | `glitch` | rasgo digital: faixas horizontais deslocadas, vermelho de um lado e verde/azul do outro, blocos corrompidos e tiras chapadas (rosa, ciano, superfície) nos últimos quadros; a nova assenta no mesmo rasgo, que cai a zero |
| `vhs` | 0,90 s | 0,5 a 1,6 | -0,6 a +0,4 | `rebobina` | rebobinar: linhas tremendo, duas barras de busca subindo cada vez mais rápido, cor vazando, preto levantado, e a imagem perdendo o sincronismo e rolando nos últimos quadros. OSD da fita: `◀◀ REW` e contador `SP` correndo para trás; a nova entra em `PLAY ▶` |
| `queima` | 0,80 s | 0,5 a 1,6 | -0,55 a +0,45 | `clarao` | película queimando: vazamento de luz quente pela borda, a cena superexpõe e a queima avança em faixas chapadas (rosa, laranja, creme, branco). No `inicio` o quadro está branco; a nova sai dele e a queima recua |
| `pixels` | 0,50 s | 0,3 a 1,2 | -0,5 a +0,5 | `bip` | a cena vira mosaico de blocos que crescem "em dois" (um degrau a cada dois quadros), centrado no assunto; a nova resolve do bloco maior ao pixel. Perto do auge, alguns blocos acendem em rosa chapado ou ganham contorno, longe do rosto |
| `persianas` | 0,70 s | 0,4 a 1,4 | -0,5 a +0,5 | `whoosh` | lâminas giram 180° em onda, a cena de antes na frente e a nova no verso, com perspectiva (borda perto mais comprida), sombra na face que vira de lado e um fio rosa na borda. A câmera recua a 0,86 no meio, sobre o palco da marca |
| `cubo` | 0,60 s | 0,35 a 1,2 | -0,5 a +0,5 | `whoosh` | as duas cenas são faces de um cubo: a de antes gira para fora, a nova chega do lado, a câmera recua um pouco no meio e a face de lado escurece |
| `forma` | 0,70 s | 0,4 a 1,4 | -0,5 a +0,5 | `subida` | uma forma da marca (círculo, pílula ou losango) em rosa chapado cresce do assunto e cobre tudo no `inicio`; a nova abre por dentro de uma segunda forma, com um fio claro na borda |
| `tinta` | 0,80 s | 0,5 a 1,6 | -1 a 0 | `whoosh` | a nova cena aparece por uma mancha de tinta orgânica que se espalha do assunto dela, com uma franja rosa na borda. Tudo acaba no `inicio`, como na `mascara` |
| `zoom-atraves` | 0,50 s | 0,3 a 1,0 | -0,6 a +0,4 | `whoosh` | mergulho rápido num ponto (até 3,4x, acelerando) com borrão de velocidade (desfoque mascarado, centro nítido) e riscos saindo do ponto; um brilho curto marca a passagem e a nova sai do mesmo movimento, de 1,5x a 1x |

### 1.3 Parâmetros

| transição | campo | valores | padrão |
|---|---|---|---|
| todas | `duracao` | a faixa da tabela | o padrão da tabela |
| `vhs` | `osd` | `base` (embaixo, dentro da zona segura), `topo` | `base` (no alto ele disputa lugar com a legenda que sobe acima da cabeça) |
| `queima` | `lado` | `direita`, `esquerda`, `baixo`, `cima` | `direita` |
| `pixels` | `bloco` | 24 a 200 px (o maior bloco do auge) | 96 |
| `persianas` | `direcao` | `horizontal`, `vertical` | `horizontal` |
| `persianas` | `tiras` | 3 a 16 | 8 (horizontal), 6 (vertical) |
| `cubo` | `direcao` | `esquerda`, `direita`, `cima`, `baixo` | `esquerda` |
| `forma` | `forma` | `circulo`, `pilula`, `losango` (a que cobre) | `circulo` |
| `forma` | `revela` | idem (a que abre a nova) | a mesma de `forma` |
| `forma`, `zoom-atraves`, `tinta` | `centro` | `"x y"` em px ou %, ou `[x, y]` | o centro do assunto (abaixo) |
| `forma`, `zoom-atraves` | `centro_nova` | idem, para a cena que entra | o `centro`, senão o assunto da nova |

**O centro do assunto.** Quando o plano não dá `centro`: o que o modo declarou (`mergulhoCentro`,
`mascaraCentro`), senão os olhos de quem fala (o rosto do quadro, a 42% da altura da caixa), senão o meio do
quadro um pouco acima (540, 864).

### 1.4 Como desenha (para quem mexe)

- **Sem cópia da cena.** Tudo é feito sobre a própria raiz das duas cenas: filtro SVG (`feTurbulence`,
  `feDisplacementMap`, `feComponentTransfer`, `feImage` de data: URL), `clip-path`, transformação CSS 3D e
  véus na camada das cenas.
- **Um gancho por quadro.** Os parâmetros que mudam a cada quadro (semente, tabela de faixas, tamanho do
  bloco, recorte) são escritos num `M.aCada` só, a partir do índice do quadro e de `M.fx`. Ele começa todo
  quadro apagando o que esta frente escreveu no quadro anterior (e ninguém mudou depois): fora da janela a
  cena volta ao estilo de antes. Visibilidade vai em `tl.set`, como no resto do motor.
- **O mosaico** (`pixels` e os blocos do `glitch`) é um `feDisplacementMap` com um mapa em serra (uma
  célula, repetida pelo `feTile`): custa o mesmo para qualquer bloco. O `feMorphology` custava ~0,6 s por
  quadro com bloco de 96.
- **`feImage` com `href="#id"` não serve:** o Chromium marca a imagem como "tainted" e o deslocamento ignora
  o mapa. O mapa vem de data: URL, pré-carregado com `M.esperar`.
- **A legenda mede o rosto parado.** As que transformam a cena (`persianas`, `cubo`, `forma`,
  `zoom-atraves`) registram a janela em `medirParada`: enquanto ela dura, `M.rostoNaTela` tira a
  transformação por um instante, mede e devolve, como no `transicoes.js`.
- **O evento sonoro** fica perto do `inicio` (no máximo 0,4 s antes): o gate de ritmo junta transição e cena
  nova numa recomposição só quando estão a 0,5 s ou menos. Nos sons que terminam no evento (`rebobina`,
  `subida`) o ponto forte cai na troca.

---

## 2. Palavras

### 2.1 O que vale para os treze efeitos

Tudo o que o cabeçalho do `palavra.js` descreve continua igual para os novos: `t`, `ate`, `y`, `tam`, `cor`,
`sombra`, `fonte`, `id`, `atras`; a névoa por sequência; a saída em desfoque de 0,2 s; o aviso quando a letra
cai sobre a cabeça (só em palavra com névoa); caber nos 940 px da zona segura (o corpo encolhe sozinho). Toda
face leva `data-texto` e `data-cor` com a cor mais escura que ela mostra; o cursor em bloco (`decodifica` e
`digitacao`) também é `data-texto`, com o rosa no `data-cor`; o que não é letra para ler (tubo apagado, moldura
do carimbo, espessura do cromado, estrela) leva `data-zona`.

**`som` em todos os efeitos.** `"som": "raio"` troca o som da entrada do efeito por outra família da
biblioteca (ou um arquivo exato, `"whoosh-2"`); `"som": null` (ou `false`) cala a palavra inteira, os tiques de
detalhe da `digitacao` e do `pula` também. Sem `som`, vale o padrão da tabela abaixo. Nome que não existe
recusa o plano com a lista do que vale. Serve para o som da palavra caber no kit da linguagem do reel (o `neon`
toca `estatica`, fora do kit de várias).

**Sem névoa por padrão** (o fundo dela já é o próprio bloco): `digitacao`, `brutal` com `caixa` e
`marcatexto` com `cor: "escuro"`. Os outros pedem a névoa, que `sombra: false` desliga (por exemplo sobre o
fundo da marca no `painel-rosto`).

### 2.2 Os oito novos

| efeito | o que faz | som |
|---|---|---|
| `decodifica` | o texto se resolve de glifos embaralhados, da esquerda para a direita, com um cursor em bloco na próxima casa. Cada letra mora na casa dela (a caixa nunca muda de largura); o glifo troca a cada dois quadros, do hash da casa e do quadro. Embaralhada em rosa, resolvida na cor da palavra. Fonte padrão: `mono` | `bip` |
| `brutal` | tipografia brutalista: a palavra gigante, passando da largura e cortada pela borda da caixa (que mora dentro da zona segura), entra seca em dois quadros (1,06 e 1) e troca seca. `caixa: true` põe a letra escura sobre um bloco de rosa chapado | `impacto` na entrada e em troca a 1,5 s ou mais da anterior |
| `marcatexto` | uma barra de marca-texto rosa varre da esquerda para a direita em 0,3 s por trás da palavra, inclinada -1,6° e com borda irregular (do hash do texto). `cor: "escuro"`: o marca-texto clássico, a letra escura aparece junto com a barra | `clique` |
| `neon` | tubo apagado (vidro rosa a 16% com um fio) e, por cima, o aceso (miolo rosa claríssimo com quatro halos) e um brilho na parede. Acende piscando: 2 ou 3 apagões curtos nos primeiros ~0,4 s, do hash do texto; depois zumbe de leve | `estatica` |
| `carimbo` | a palavra em rosa numa moldura, com tinta falhada (ruído cortado em furos e borda tremida, filtro fixo). Bate de até 1,6 para 1 em 0,14 s girando até o ângulo (o golpe é o maior que cabe na zona segura no caminho inteiro, nunca menos que 1), a sombra chega borrada e cola; no impacto, um amasso de 1,5% | `carimbo` no impacto |
| `cromado` | letra cromada anos 80/Y2K **sem degradê**: céu claro e chão de aço em faixas chapadas de borda dura, horizonte num fio rosa, contorno fino e espessura em vinho chapado. Entra de 1,18 desfocada (a conta de caber já conta essa escala); um brilho (duas faixas brancas inclinadas) atravessa uma vez e uma estrela de quatro pontas pisca na ponta | `whoosh` |
| `vazado` | só o contorno, que se desenha letra a letra (cada letra é um `<path>` da fonte de título, lida pelo opentype.js, com `stroke-dasharray`) e depois preenche. Sem o opentype, cai no contorno do CSS revelado da esquerda para a direita, com aviso | `whoosh` |
| `pixel` | a palavra em blocos 8-bit: a fonte da marca lida em grade grossa (célula cheia quando a letra cobre 42% dela). Cada bloco cai de até 3 células, em degraus inteiros e "em dois", coluna a coluna da esquerda para a direita, e encaixa seco, com a sombra 8-bit em rosa escuro | `bip` |

### 2.3 Campos novos

| efeito | campo | o que é | padrão |
|---|---|---|---|
| `decodifica` | `duracao` | quanto leva para resolver tudo | o tempo da palavra falada (0,35 a 0,9 s), senão 0,55 |
| `brutal` | `texto` com `\|` | `"NÃO\|É\|HYPE"` troca de palavra no tempo | uma palavra só |
| `brutal` | `trocas` | os instantes absolutos das trocas (um a menos que as palavras) | divididos por igual entre `t` e `ate` |
| `brutal` | `caixa` | letra escura sobre bloco rosa chapado | `false` |
| `brutal` | `sangra` | quanto a palavra passa da largura, 0,6 a 1,6. Teto automático: a borda corta no máximo 40% da tinta da primeira e da última letra (com aviso quando reduz) | 1,14 com caixa, 1,06 sem |
| todos | `som` | troca o som da entrada (família ou `"nome-N"`); `null`/`false` cala | o da tabela 2.2 |
| `brutal` | `tam` | aqui é o **teto** do corpo (a palavra curta não vira meia tela) | 360 |
| `marcatexto` | `cor` | `"escuro"` faz o marca-texto clássico | a tinta, na frente da barra |
| `carimbo` | `giro` | o ângulo final, -20 a 20 graus | -7 |
| `vazado` | `duracao` | quanto leva desenhando cada letra | 0,55 |
| `pixel` | `bloco` | o lado da célula, 4 a 40 px | `tam / 12` (mínimo 6) |

### 2.4 Como desenha (para quem mexe)

- **Tudo seco cai no meio do quadro.** Os `tl.set` que trocam letra, glifo, apagão do neon ou soco do brutal
  vão no meio do quadro anterior (`meioQuadro(k)`), longe do instante exato, onde a ida e a volta da busca
  da linha do tempo discordam (o mesmo cuidado do glitch antigo).
- **Por quadro, a partir do t.** O embaralhador do `decodifica`, o brilho do `neon` e o canvas do `pixel` são
  desenhados num `M.aCada`, só do `t` e do índice do quadro: nada é guardado entre quadros.
- **A caixa medida é a que aparece.** No `brutal` a face é a caixa de recorte (a medida vê o corte); no
  `pixel` o canvas é a face e cobre também a altura de onde os blocos caem; no `carimbo` a caixa conta o giro.
- **Os filtros SVG da palavra** (a tinta do carimbo) moram num `<svg>` só, com id por palavra.

### 2.5 Correções depois dos três reels reais (codex, apis e 5-plugins, corte 02)

| peça | o que acontecia | o que mudou |
|---|---|---|
| `decodifica`, `digitacao` | o cursor em bloco tinha `data-zona`; o `compor.py` grava o quadro do contraste com `Motor.render(t, {semTexto: true})`, que esconde só `[data-texto]` (`body.sem-texto` no `motor.css`), e o bloco rosa ficava no fundo medido, dentro da caixa da face rosa: 1,00:1 no "GLM" (8,5 s) e no "OPENAI" (0,5 s) | o cursor é `data-texto` com `data-cor` rosa e o corpo da letra (`cursorTexto`): some do quadro sem texto e é medido ele mesmo contra a névoa ou o vidro. Os glifos embaralhados já moravam na face (`data-texto`). No "GLM" de teste: antes 1,00:1 (reprovava), depois 3,28:1 |
| todos | o som era fixo (o `neon` toca `estatica`, fora do kit de várias linguagens) | campo `som` (2.1) |
| `carimbo` | o golpe de 1,6 não entrava na conta de caber: a caixa girada saía da zona por 2 a 3 quadros (no teste, até x 0 e y 124) | a largura cabe no golpe mínimo de 1,3 (o corpo encolhe se precisar); na altura, o centro deixa lugar para a caixa girada da entrada (−5° a mais: girando, ela fica mais alta e saía da zona até na escala 1), e a palavra encostada no topo desce só isso (no corte 44, "CARIMBO DE IA" desceu 28 px); o golpe é o maior até 1,6 que cabe no caminho inteiro (amostrado no `power3.in`), e perto do topo ele fica menor. Teste ("SUBAGENTS", corpo 160, y 300): nenhum quadro fora (antes 2 quadros) |
| `brutal` | com `caixa` e `sangra` 1,14 o "I" de "ILIMITADO" sumia inteiro ("LIMITADO") | `sangraMaxima`: a sangria para onde a borda cortaria 40% da tinta da primeira ou da última letra; o corpo diminui e sai um aviso. "ILIMITADO" sangra 1,05 e lê inteiro |
| `cromado` | a entrada em 1,18 não entrava na conta: 56 px fora da zona | `caber` divide a largura por 1,18 (como a extrusão divide por 1,03); na altura, perto do topo ou da base, a entrada parte de menos (`escalaQueCabe`, nunca abaixo de 1). Teste ("+20 MODELOS", corpo 220, y 300): nenhum quadro fora (antes 4 quadros, até x 2) |
| `digitacao` | o aviso "cai sobre a cabeça e a névoa escurece a cabeça" saía para palavra sem névoa | o aviso só vale para palavra com névoa (`sombra` ligada) |

---

## 3. A demo (corte 44)

`projetos/teste-onda-1/materiais-de-trabalho/corte-44/cenas.json`: 36,1 s, 14 cenas, a fala do teste "AI
first ou data first" a 1,15x. Usa as nove transições (uma em cada troca de c1 para c10) e os oito efeitos
novos da palavra, misturados com os antigos `glitch`, `conta` e `digitacao` para conferir que eles não
quebraram.

| cena | t | transição de entrada | palavras |
|---|---|---|---|
| c1 | 0 | (abre) | `decodifica` AI FIRST, `glitch` ERRO |
| c2 | 2,92 | `glitch` | `marcatexto` SALESFORCE, `conta` 26% |
| c3 | 5,72 | `pixels` | (tipografia) |
| c4 | 7,75 | `vhs` | `pixel` 89% |
| c5 | 9,86 | `queima` | `brutal` REPETE / PIOR, com caixa |
| c6 | 12,52 | `persianas` | (lista) |
| c7 | 14,84 | `cubo` | `carimbo` CARIMBO DE IA |
| c8 | 17,2 | `forma` (círculo, revela pílula) | `vazado` ANTES? |
| c9 | 19,45 | `tinta` | `conta` 80%, `cromado` 2027 (sobre o painel) |
| c10 | 22,5 | `zoom-atraves` | `cromado` MUSEU atrás de você, `digitacao` AI FIRST? |
| c12 | 27,25 | (corte seco) | `decodifica` LISTE OS CAMPOS, `marcatexto` escuro PELO RISCO |
| c14 | 32,7 | (corte seco) | `neon` AGENTE?, `brutal` COMENTA atrás de você |

É uma vitrine: tem muito mais transição e efeito do que um reel de verdade deve ter (a regra da 4.0 é uma
linguagem base e no máximo uma convidada). Serve para ver todas as peças no mesmo vídeo e para os gates.

```
flow-reels produzir/compor --projeto projetos/teste-onda-1 --corte 44
flow-reels produzir/audio --projeto projetos/teste-onda-1 --corte 44
flow-reels produzir/conferir_reel --projeto projetos/teste-onda-1 --corte 44
```

---

## 4. Custo

Render inteiro do corte 44 (1084 quadros, 1080x1920, sem GPU): veja a seção 5 do relatório desta frente;
em média ~100 ms por quadro, no mesmo ritmo de um reel sem as peças novas. O que mais pesa é o `queima` e a
`tinta` (dois campos com `feGaussianBlur` grande por quadro) e o `zoom-atraves` (o `backdrop-filter` do
borrão). Um desfoque radial de verdade (média de cópias ampliadas por `feDisplacementMap`) custava 3 s por
quadro no Chromium sem GPU e foi trocado pelo borrão mascarado.

## 5. Limites

- **Prévia.** O `--previa` (540x960) desenha os filtros SVG em pixels da cena inteira: as transições saem
  certas, mas o `backdrop-filter` do `zoom-atraves` tem o mesmo problema da `desfoque` antiga na prévia
  (escala 0,5). Confira essa no render inteiro.
- **Sem GPU por escolha.** Tudo roda no caminho de software do Chromium; com a GPU ligada (reel com 3D) os
  filtros SVG também funcionam, mas o custo não foi medido lá.
- **`vazado`** depende da fonte de título ser lida pelo opentype.js (`TOKENS.fontes.titulo.arquivo`). Com
  fonte variável que ele não lê, a palavra cai no contorno do CSS, com aviso.
- **`brutal` em várias palavras** troca seco: não há transição entre elas, por desenho.
- **`neon` e `cromado`** usam brilho e faixas de luz, as únicas exceções à cor chapada: o miolo do neon é um
  rosa claríssimo e o brilho da parede é luz. Degradê de marca não há.
- **Transições em sequência rápida.** Duas transições longas em cenas curtas (abaixo de ~1,2 s) batem no
  cruzamento de janelas e o plano é recusado; encurte a `duracao`.
