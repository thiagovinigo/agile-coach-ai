# Estética: onze peças de linguagem visual (4.0)

Onze sobreposições (`registrarSobre`), cada uma uma peça de uma família do catálogo
(`docs/pesquisa-4-0/01-linguagens-visuais.md`). Arquivo: `web/sobre/estetica.js`. Nenhuma pede WebGL:
tudo é canvas 2D, SVG e CSS (inclusive `backdrop-filter`), então nada vai para o `gpu.json`.

| tipo | família | o que se vê | som |
|---|---|---|---|
| `moldura-crt` | CRT e terminal | a cena dentro de um monitor de tubo, com liga e desliga | estatica |
| `grade-synthwave` | synthwave | chão de grade correndo, sol em faixas chapadas, serras e estrelas, atrás de você | whoosh (`som` troca) |
| `linhas-foco` | mangá | linhas de velocidade apontando para o rosto, com o quadro de impacto | impacto |
| `mira` | HUD de ficção | mira que trava no rosto (ou na mão, no objeto), anéis, varredura e leituras | bip |
| `diagrama` | planta técnica | rótulos com chamada e cotas com setas que se desenham; grade milimetrada | tick |
| `chuva` | terminal | chuva de caracteres atrás de você | nenhum (ou estatica) |
| `luz` | película | vazamento de luz atravessando o quadro, em screen | nenhum |
| `poeira` | película | grão, poeira, fios, riscos e cintilação | nenhum |
| `recorte` | colagem | você vira adesivo: contorno branco, sombra chapada, 12 qps, fundo de papel | pop |
| `papel` | colagem | moldura de papel rasgado com fita adesiva | nenhum |
| `barras` | explicador (Vox) | mini gráfico de barras com os valores contando e o marca-texto rosa | tick |

```json
"sobre": [ { "tipo": "moldura-crt", "ate": 19.0 },
           { "tipo": "linhas-foco", "cor": "destaque", "impacto": { "t": 2.62, "modo": "negativo" } },
           { "tipo": "grade-synthwave", "atras": true } ]
```

## Regras que valem para as onze

- **Vida.** `t` (padrão: o início da cena) e `ate`. **Com `ate`, a peça sai com animação que termina em
  `ate`**; sem `ate`, ela vai embora com a cena, em corte seco. `"saida": "corte"` força o corte seco
  mesmo com `ate`. Na cena, ninguém passa do fim dela (aviso). Vida curta demais para entrar e sair é
  `Error` com o mínimo da peça.
- **Determinismo.** Tudo é função de `t`. O que se desenha por quadro (canvas, SVG) é refeito do zero no
  gancho (`Motor.aCada`) com `M.fx` (hash e semente por nome e quadro). Grão, poeira, glifos, linhas de
  mangá e o "ferver" do papel trocam por `floor(t * qps)`, nunca por estado. Medido: o mesmo instante
  sozinho (`--quadro`) e dentro do render em sequência dá diferença 0.
- **Texto** (`data-texto`) só aparece e anda pela linha do tempo (sets e tweens): os painéis da `mira`, as
  placas do `diagrama` e o gráfico das `barras`. A legenda `revela` desvia deles. O que troca no gancho é
  só o conteúdo de letras em fonte mono de largura fixa (a decodificação), que não muda a caixa. As
  placas levam `data-zona` (a legenda desvia da placa inteira).
- **Cor.** Destaque é o rosa chapado (`--destaque`). Onde o estilo pede degradê de cor (o sol do
  synthwave), vão faixas chapadas. Gradiente só de opacidade (vinheta, brilho, luz). Os campos de cor
  aceitam `destaque`, `ciano`, `tinta`, `suave`, `escuro`, `quente`, `branco`, `preto` ou `#RRGGBB`.
- **Rosto.** Nada cobre os olhos além de um flash: as linhas de foco deixam uma elipse livre no rosto,
  a `luz` perde 70% em volta dele, a `mira` e o `diagrama` põem o texto fora dos olhos (com aviso quando
  não dá), a grade e a chuva ficam atrás de você. Exceções curtas e de propósito: o quadro de impacto (2
  quadros), o liga e o desliga do CRT (~0,4 s de tela apagada em cada ponta).
- **Erros.** Parâmetro inválido é `Error` com o que pôr. Situação ruim mas renderizável vai para o
  console como `"<tipo> (<nome>): aviso: ..."` (o `compor.py` repete no fim).
- **Sons** no máximo um a cada 1,5 s por peça. Os da 4.0 (`estatica`, `impacto`, `bip`) dependem da frente
  de som; sem o `.wav`, o `audio.py` pula o evento e avisa.
- **Atrás de você.** `grade-synthwave`, `chuva` e a grade do `diagrama` foram feitas para `"atras": true`
  (precisa da visão do corte). Sem `atras`, a grade e a chuva avisam que cobrem você. **Numa peça com
  `atras`, nenhum descendente pode ter `clip-path`**: o Chromium apaga o furo da pessoa que o motor põe na
  raiz (a grade sumia inteira, medido). Por isso, com `atras`, as placas de texto entram em foco (de
  desfocadas para nítidas) em vez da máscara reta.

## `moldura-crt`

A cena vista dentro de um monitor de tubo. O gabinete de plástico escuro tem a tela com cantos
redondos, um bisel em três faixas chapadas, a grade de som e o LED no queixo. No vidro: scanlines com
uma cintilação de ±6%, uma faixa de varredura descendo devagar, uma máscara de fósforo RGB quase
invisível, a vinheta do vidro curvo e o reflexo (uma mancha clara no alto à esquerda e um fio de luz na
borda). Fica por cima da cena e por baixo da legenda; o rosto continua visível.

- **Entrada:** o gabinete chega de 1,16 para 1 (0,42 s, como a câmera recuando e revelando o monitor),
  com a tela apagada. Com `liga`: aos 0,18 s, uma linha branca cresce na horizontal (0,09 s), abre na
  vertical (0,17 s) e a imagem nasce estourada, assentando em 0,35 s. O LED acende quando a linha abre.
- **Saída** (com `ate`): com `desliga`, a imagem fecha de cima e de baixo até a linha (0,13 s), a linha
  encolhe até um ponto (0,09 s), o ponto apaga (0,18 s) e o gabinete sai para 1,14 (0,28 s). Sem
  `desliga`, só o gabinete sai.

| campo | padrão | o que faz |
|---|---|---|
| `tela` | `[46, 118, 988, 1606]` | a tela em px de saída. O queixo (grade e LED) só aparece com mais de 70 px abaixo dela |
| `raio` | 70 | o canto da tela |
| `liga`, `desliga` | `true`, `true` | a linha que abre e o ponto que fecha (`desliga` só vale com `ate`) |
| `linhas` | 0,2 | a força das scanlines (0 a 0,6) |
| `cintila` | 1 | quanto as scanlines cintilam (0 a 3) |
| `fosforo` | `"nenhum"` | `"destaque"` ou `"ciano"`: a imagem vira fósforo de uma cor (a luminância mapeada para claro → rosa claro, meio-tom → rosa, sombra → vinho; uma `feColorMatrix` só, no `backdrop-filter`). Com a `chuva` atrás, a chuva também vira fósforo |
| `led` | `"destaque"` | a cor do LED aceso |

Eventos: `entra` (peso 2) no `t`; `acende` (peso 2, **estatica**) no liga; `sai` (peso 2, estatica se
couber) no desliga. Liga e desliga juntos pedem pelo menos 1,6 s de vida. Moldura forte: uma cena por
reel, e a legenda continua por cima.

**Vinheta mais leve no alto.** A vinheta do vidro (o radial e a sombra de dentro) passa por uma máscara
vertical: 35% da força até 14% da altura, voltando inteira a 40%. Inteira, ela apagava os cards, os logos e
as palavras que moram no terço de cima (o y 300 das palavras, o HUD). Os lados e os cantos de baixo seguem com
o fundo de tubo. Medido no corte 45 (17,5 s): o canto de cima clareou de 96 para 116 de luminância média
(0 a 255) e o de baixo ficou igual (37,6 → 37,7).

```json
{ "tipo": "moldura-crt", "ate": 19.0 }
{ "tipo": "moldura-crt", "fosforo": "destaque", "liga": false, "linhas": 0.28 }
```

## `grade-synthwave`

O cenário vira a cena synthwave, atrás de você (`"atras": true`): céu escuro com três faixas chapadas de
brilho rosa sobre o horizonte, 150 estrelas cintilando, o sol em quatro faixas chapadas (rosa claro,
destaque, dois tons mais fundos) com cortes horizontais que engrossam para baixo e descem devagar, um
halo do próprio sol (a mesma cor, transparente), duas serras de arame (contorno ciano no fundo, rosa na
frente) e o chão: linhas de profundidade correndo para a câmera e linhas fugindo para o ponto central,
cada uma com um traço largo e fraco por baixo (o brilho). A linha do horizonte acende em ciano.

- **Entrada:** o céu e o chão escurecem em 0,45 s, a grade se desenha do horizonte para baixo (0,65 s),
  as serras sobem (0,6 s) e o sol nasce do horizonte (1 s, desacelerando). **Saída** (com `ate`): o sol
  se põe e tudo apaga em 0,45 s.

| campo | padrão | o que faz |
|---|---|---|
| `horizonte` | 1150 | o y do horizonte (500 a 1700). No corte de teste, 1150 é a altura do queixo: o sol aparece em volta da cabeça |
| `cor` | `"destaque"` | a cor da grade |
| `cor_horizonte` | `"ciano"` | a linha do horizonte e a serra de trás |
| `sol`, `estrelas`, `serras` | `true` | ligam e desligam cada parte |
| `sol_raio`, `sol_x` | 330, 540 | o tamanho e o centro do sol |
| `velocidade` | 1 | quanto a grade corre (0 a 4) |
| `escurecer` | 1 | a opacidade do céu e do chão (abaixo de 1 o cenário aparece por trás; o neon vira fantasma) |

Evento: `entra` (peso 2, **whoosh**; antes era subida, que ficava fora do kit das linguagens que listam a
grade). `"som"` troca o som da entrada (uma família da biblioteca ou `"nome-N"`; `null` ou `false` cala).
Pede a visão do corte (`atras`). Bom como momento-herói.

```json
{ "tipo": "grade-synthwave", "atras": true }
{ "tipo": "grade-synthwave", "atras": true, "cor": "ciano", "cor_horizonte": "destaque", "horizonte": 1250, "serras": false }
```

## `linhas-foco`

Linhas de velocidade de mangá convergindo para o rosto (ou para um ponto). São cunhas finas que nascem
fora do quadro e terminam numa elipse em volta do rosto, com a espessura em cauda longa (muitas finas,
poucas grossas) e 14% na cor secundária. Redesenhadas "em dois" (12 qps): tremem como desenho à mão. O
fundo escurece fora do rosto (gradiente de opacidade) para as linhas claras lerem sobre parede clara.

- **Entrada:** as linhas disparam das bordas para dentro em 0,16 s. **Saída** (com `ate`): voltam para as
  bordas e apagam em 0,16 s.
- **Quadro de impacto** (`impacto`): 1 a 3 quadros (padrão 2) em que a cena vira alto contraste rosa e
  preto (`backdrop-filter`), com as linhas pretas e grossas: a capa de mangá da marca. `"modo":
  "contraste"` (o claro vira rosa, o escuro preto) ou `"negativo"` (invertido). O impacto vale no quadro
  `round(t × fps)`.

| campo | padrão | o que faz |
|---|---|---|
| `centro` | `"rosto"` | `"rosto"` (rosto.json, um pouco acima do meio: os olhos) ou `[x, y]` |
| `cor` | `"tinta"` | `"tinta"` (brancas, 14% rosa), `"destaque"` (rosas, 14% brancas) ou `"escuro"` (pretas, para fundo claro) |
| `densidade` | 1 | 150 linhas × densidade (0,2 a 3) |
| `raio` | 1 | o tamanho da elipse livre em volta do rosto (0,5 a 2,5) |
| `escurecer` | 0,5 | o escuro fora do rosto (0 a 0,9) |
| `qps` | 12 | quantas vezes por segundo as linhas são sorteadas de novo |
| `impacto` | nenhum | `true` (no `t`), um número (o instante) ou `{ "t", "modo", "quadros" }` |

Evento: `entra` (peso 2) ou, com impacto, `marca` (peso 3) no impacto, com **impacto**. Vida mínima 0,3 s.
No máximo 2 ou 3 impactos por reel.

```json
{ "tipo": "linhas-foco", "t": 0.0 }
{ "tipo": "linhas-foco", "cor": "destaque", "densidade": 1.4, "impacto": { "t": 2.62, "modo": "negativo" } }
```

## `mira`

O HUD de ficção que trava no alvo: quatro cantos de mira que fecham de 1,6x até a caixa (com uma
cintilação de 4 quadros ao aparecer e um soco de 5% no travamento, quando ficam na cor), um anel de
réguas que se desenha e gira devagar, três arcos grossos girando ao contrário (um na cor), marcas nos
pontos cardeais, a varredura que desce pela caixa no travamento e a cada 2,4 s, e o painel de leituras
ligado por uma guia. O centro segue o alvo suavizado (média de 13 quadros); o tamanho fica parado (a
mediana da vida), para a mira não respirar.

O painel é texto em FC Mono 24 sobre placa escura: o título com o ponto aceso e de 1 a 4 leituras.
Os valores **decodificam** no travamento (glifos semeados que trocam a 24 qps, resolvendo da esquerda
para a direita). `{x}`, `{y}` e `{conf}` viram números ao vivo: a posição do alvo na tela (atualizada a
cada 3 quadros) e a confiança medida do rosto.json no travamento. O painel segue o alvo pela linha do
tempo, quadro a quadro.

**O painel nunca cobre o rosto.** A cabeça é a caixa do rosto (quadro a quadro com o alvo `"rosto"`, a
mediana da vida com outro alvo) crescida 40% para cima (testa e cabelo) e 10% para cada lado. Cada lado é
testado no caminho inteiro, já com o empurrão para dentro da zona segura (era ele que punha o painel na
testa); vale o primeiro sem colisão, na ordem: o lado (direita ou esquerda) com mais espaço, o outro, acima
da cabeça, abaixo do queixo. `lado` no plano é preferência: se ele cobriria o rosto, o painel troca de lado
com aviso. Se nenhum lado escapa, fica o de menos colisão, com aviso.

**O painel abre junto com o texto.** O título e as leituras já estão nele quando a placa abre (os valores
decodificando até o travamento), e a revelação recorta placa e letra juntas. Antes as letras entravam 0,22 s
depois e a placa preta aparecia vazia por 6 a 7 quadros (o CTA do apis, ~43 s). Enquanto abre (0,24 s), o
painel fica com `data-saindo`, fora da conta do contraste (a caixa da letra passa da parte revelada).

| campo | padrão | o que faz |
|---|---|---|
| `alvo` | `"rosto"` | `"rosto"`, `"mao"`, `"mao.esquerda"`, `"mao.direita"`, `"objeto:<categoria>"`, `[x, y, w, h]` (lista de alvos abaixo) |
| `trava` | `t + 0,38` | o instante do travamento (entre `t + 0,15` e `ate − 0,4`) |
| `rotulo` | `"ALVO 01"` | o título do painel |
| `leituras` | CONF, POS, STATUS | `[{ "rotulo", "valor", "destaque" }]`, 1 a 4 |
| `cor` | `"destaque"` | a cor do travamento, do arco e da varredura |
| `lado` | `"auto"` | `"direita"`, `"esquerda"`, `"cima"`, `"baixo"` |

Eventos: `entra` (peso 2) no `t`, `marca` (peso 2, **bip**) no travamento. Aviso quando o painel troca de
lado para não cobrir o rosto, quando não há lado livre ou quando sai da zona segura. Alvo nas mãos (embaixo): ponha a legenda da cena no alto
(`"legenda": {"posicao": "topo"}`), porque o painel fica onde a legenda do peito ficaria.

```json
{ "tipo": "mira", "t": 6.7, "ate": 9.75, "trava": 7.8, "rotulo": "IA em produção",
  "leituras": [ { "rotulo": "ERROU", "valor": "89%", "destaque": true }, { "rotulo": "CONF", "valor": "{conf}" },
                { "rotulo": "POS", "valor": "{x} {y}" } ] }
{ "tipo": "mira", "alvo": "mao.esquerda", "cor": "ciano", "rotulo": "Decisão" }
```

## `diagrama`

Desenho técnico que se desenha no tempo da fala, por cima da cena.

- **Rótulos** (`rotulos`): um ponto no alvo (com anel), uma chamada que sai dele a 45° até a altura do
  rótulo e corre na horizontal até ele (0,24 s), e a placa (FC Mono 28, número na cor e texto em caixa
  alta, barra na cor à esquerda) que abre em máscara reta. O ponto segue o alvo quadro a quadro; a placa
  fica parada (o lugar sai da mediana do alvo), longe dos olhos e dos outros rótulos.
- **Cotas** (`cotas`): a medida entre dois alvos, estática (desenho técnico não anda): as linhas de
  chamada crescem (0,15 s), a linha de cota cresce do meio para as pontas com as setas na cor (0,3 s), e o
  texto abre no meio dela. Cota em pé (mais vertical que horizontal) gira o texto junto, lido de baixo
  para cima, ao lado da linha.
- **Grade** (`grade`): papel milimetrado (linhas de 30 px, fortes a cada 150, cruzes nas interseções),
  revelada de cima para baixo com uma linha acesa na frente (0,7 s). Feita para uma peça própria com
  `"atras": true` (a grade atrás de você, os rótulos numa segunda peça por cima).

| campo | padrão | o que faz |
|---|---|---|
| `rotulos` | `[]` | `[{ "texto", "alvo", "t", "lado", "dx", "dy" }]`. `alvo` padrão `"rosto"`; `lado` padrão: o lado da tela do alvo; `dx` 120, `dy` −110 (onde a placa fica em relação ao alvo) |
| `cotas` | `[]` | `[{ "de", "ate", "texto", "t", "desvio" }]`. `desvio` (70) é a distância da linha de cota aos pontos, para cima (ou para a esquerda na cota em pé); negativo vai para o outro lado |
| `grade` | `false` | `true` ou `"ciano"` (ciano), `"tinta"` |
| `cor` | `"destaque"` | pontos, setas, linha de cota e o texto da cota |
| `linha` | `"tinta"` | chamadas e linhas de chamada da cota |
| `numerar` | `true` | o "01", "02" na frente dos rótulos |

Sem `t` nos elementos, eles se espalham de 0,3 a 0,6 s a partir do `t` da peça. Eventos: `marca` em cada
elemento, **tick** no máximo a cada 1,5 s. Pelo menos um de `rotulos`, `cotas` ou `grade`.

**A placa abre com o texto.** No rótulo e no texto da cota a letra já está na placa quando ela abre (a
máscara recorta as duas). Antes a letra entrava 0,2 s depois e a placa preta vazia aparecia sozinha (o rótulo
"Codex" do codex corte 02, ~14,4 s). Enquanto abre, a placa fica com `data-saindo` (fora do contraste).

**Os alvos** (valem para `mira`, `diagrama` e o `centro` das linhas de foco): `"rosto"` (a caixa),
`"rosto.topo"` (o alto do cabelo, estimado 18% da altura do rosto acima da testa), `"rosto.base"` (o
queixo), `"rosto.esquerda"`, `"rosto.direita"` (as laterais na altura dos olhos); `"mao"` (a maior),
`"mao.esquerda"`, `"mao.direita"` (o lado da tela; `visao/maos.json`); `"ombro.esquerdo"`,
`"ombro.direito"` (`visao/corpo.json`, pelo lado da tela); `"objeto:<categoria>"` (o maior daquela
categoria em `visao/objetos.json`, ex. `"objeto:celular"`); `[x, y]` ou `[x, y, w, h]` fixos em px de
saída. Buraco no dado é preenchido pelo vizinho; alvo que não aparece na vida é aviso (o elemento fica
de fora) ou Error (a mira).

```json
{ "tipo": "diagrama", "ate": 16.2,
  "rotulos": [ { "texto": "Aprova", "alvo": "ombro.esquerdo", "t": 12.55 },
               { "texto": "Cancela", "alvo": "rosto.direita", "t": 13.3, "dy": -60 } ],
  "cotas": [ { "de": "rosto.esquerda", "ate": "rosto.direita", "texto": "carimbo de IA", "t": 14.85, "desvio": 330 } ] }
{ "tipo": "diagrama", "grade": "ciano", "atras": true }
```

## `chuva`

Chuva de caracteres de terminal atrás de você (`"atras": true`), em duas camadas (longe: menores, mais
fracas e mais lentas; perto: maiores). Cada coluna tem velocidade, tamanho e fase próprios (semente da
coluna), e a posição é função de `t`: nada guarda estado. A cabeça é o glifo claro com o brilho da cor
por baixo, as duas seguintes quase cheias, e a cauda apaga em degraus. Os glifos trocam a ritmo próprio
de cada coluna (a cabeça a cada quadro). O cenário escurece por baixo.

- **Entrada:** o escuro sobe em 0,4 s e as colunas descem do alto como cortina. **Saída** (com `ate`):
  apaga em 0,4 s.

| campo | padrão | o que faz |
|---|---|---|
| `cor` | `"destaque"` | a cauda (a cabeça é sempre a tinta) |
| `glifos` | `"misto"` | `"hex"`, `"binario"`, `"codigo"` (símbolos), `"misto"` (hex e símbolos), em FC Mono |
| `densidade` | 1 | colunas (0,2 a 2,5) |
| `velocidade` | 1 | 0,1 a 4 |
| `tam` | 30 | o corpo do glifo da camada da frente |
| `escurecer` | 0,82 | o escuro por baixo da chuva |
| `som` | `null` | `"estatica"` toca no `t` |

Os glifos são desenho (canvas), não texto: não levam `data-texto` nem entram nos gates.

```json
{ "tipo": "chuva", "atras": true }
{ "tipo": "chuva", "atras": true, "cor": "ciano", "glifos": "binario", "densidade": 1.3, "velocidade": 0.7, "som": "estatica" }
```

## `luz`

Vazamento de luz de película atravessando o quadro devagar, em `mix-blend-mode: screen`: três manchas da
mesma cor (só a opacidade cai, a cor é uma), em meia resolução esticada, andando na diagonal a partir
da borda de `de` ao longo da vida, com a intensidade respirando por ruído; e uma faixa macia que pulsa
na borda de entrada (a borda do filme). Em volta do rosto a luz perde 70%. Entra e sai em 0,7 s (seno).

| campo | padrão | o que faz |
|---|---|---|
| `cor` | `"destaque"` | `"quente"` (#FF6A2B) é o vazamento laranja clássico |
| `intensidade` | 0,6 | 0 a 1,5 |
| `de` | `"esquerda"` | `"direita"`, `"topo"`, `"baixo"` |
| `protege_rosto` | 0,7 | quanto a luz perde no rosto (0 a 1) |

Evento: `entra` (peso 2), sem som. Sutil: combina com `poeira`, `papel` e `recorte`.

## `poeira`

Película antiga sobre a cena (por baixo da legenda), na cadência de 24 qps: grão (4 ladrilhos de ruído
gerados uma vez com semente, em `overlay`, deslocados a cada quadro de película), cintilação da
exposição (escurece de 2 a 7%, às vezes clareia 3,5%), poeira (de 4 a 14 manchas irregulares por quadro,
78% escuras), fios (até 2, vivem 8 quadros de película e tremem), riscos verticais (até 3, vivem de 0,4 a
1,2 s, andam devagar e falham em trechos) e uma vinheta. Entra e sai em 0,3 s.

| campo | padrão | o que faz |
|---|---|---|
| `intensidade` | 1 | poeira, fios e riscos (0 a 3) |
| `grao` | 0,45 | 0 a 1 |
| `riscos`, `fios` | `true` | ligam e desligam |
| `cintila` | 1 | 0 a 3 |
| `vinheta` | 0,45 | 0 a 1 |

Evento: `entra` (peso 2), sem som.

## `recorte`

Você vira adesivo, na linguagem da colagem: a pessoa recortada pela máscara do quadro (duas vistas
`recorte: "pessoa"` com o mesmo enquadre da vista da cena e os mesmos zooms de ênfase e de emenda),
contorno grosso e a sombra chapada deslocada, desenhados num canvas na meia resolução da máscara (a
máscara vira alfa, é dilatada por 18 cópias deslocadas no raio do contorno e pintada na cor), por baixo
das vistas e com os mesmos zooms. O fundo da cena some atrás do papel ou da cor.

- **12 qps** (`passos`): as duas vistas se revezam a cada quadro, uma mostrando o quadro anterior: cada
  quadro de vídeo fica 2 vezes na tela (15 qps no vídeo, a pose a 12). O adesivo balança à mão (±0,6°).
- **Entrada:** o fundo sobe em 3 degraus (0,2 s); o adesivo cai de 0,84 e girado, passa de 1,07 e assenta
  no `giro`, em degraus (0,34 s), com **pop**. **Saída** (com `ate`): encolhe girando e some; o fundo sai em
  degraus.
- `"fundo": "papel"` tem dois retalhos rasgados por trás de você (um rosa chapado, um claro).

| campo | padrão | o que faz |
|---|---|---|
| `fundo` | `"papel"` | `"papel"` (escuro), `"kraft"`, `"branco"`, uma cor (`"destaque"`, `#RRGGBB`) ou `"nenhum"` |
| `retalhos` | `true` | os dois retalhos do papel |
| `contorno` | 14 | px do contorno (0 a 40) |
| `cor_contorno` | `"branco"` | |
| `sombra` | `[16, 20]` | `[dx, dy]` em px, ou `false` |
| `cor_sombra` | `"destaque"` | |
| `passos` | `true` | o movimento a 12 qps |
| `giro` | −2 | graus em que o adesivo assenta |

Só em `cena.sobre` (copia a vista da cena) e precisa da máscara da visão (`Error` sem ela). Com
`"fundo": "destaque"`, a palavra da legenda que acende fica rosa sobre rosa (lê pelo contorno escuro):
prefira `papel` ou outra cor quando a fala for longa.

```json
{ "tipo": "recorte", "fundo": "papel", "passos": true }
{ "tipo": "recorte", "fundo": "destaque", "passos": false, "cor_sombra": "escuro", "sombra": [18, 24], "giro": 2 }
```

## `papel`

Moldura de colagem: uma folha de papel procedural (cor base, manchas de ruído suave, grão e fibras,
gerada uma vez com semente) com uma janela rasgada por onde se vê a cena. A borda do rasgo tem o miolo
claro do papel e fibras soltas; a folha faz sombra dentro da janela; fitas adesivas translúcidas
(pontas serrilhadas, listras e vincos) prendem os cantos. A borda "ferve" a 12 qps (3 variações do
detalhe fino, a forma não anda).

- **Entrada:** a folha cai de 1,16 e girada e assenta em 4 degraus (0,34 s); as fitas batem uma a uma
  (0,11 s entre elas). **Saída** (com `ate`): a folha sobe e some em 3 degraus.

| campo | padrão | o que faz |
|---|---|---|
| `cor` | `"escuro"` | `"kraft"`, `"branco"`, `"destaque"` ou `#RRGGBB` |
| `janela` | `[70, 190, 940, 1420]` | o furo em px de saída, antes do giro (aviso se cortar o rosto) |
| `giro` | −1,2 | graus da janela |
| `fitas` | 4 | 0 a 4 (ordem: alto à esquerda, baixo à direita, alto à direita, baixo à esquerda) |
| `ferve` | `true` | a borda viva a 12 qps |
| `rasgo` | 1 | a amplitude do rasgo (0 a 3) |
| `semente` | 3 | muda o papel e o rasgo |

Evento: `entra` (peso 2), sem som.

## `barras`

Mini gráfico de barras no estilo explicador: placa escura (cantos de 16 px) com o título em FC Mono e o
quadrado na cor, o rótulo de cada barra (FC Legenda 36) em cima do trilho, a barra chapada (a marcada na
cor, as outras na tinta suave) crescendo com o valor (FC Titulo 46) correndo junto da ponta e contando,
e a fonte do dado embaixo. Se o valor não cabe depois da ponta, ele entra na própria barra em escuro.
O **marca-texto** varre por trás do rótulo da barra marcada (bloco rosa inclinado, 0,22 s) e o rótulo
vira escuro.

- **Entrada:** a placa abre de cima para baixo (0,3 s); as barras crescem a partir de `t + 0,3`, uma a
  cada 0,14 s, em 0,75 s. **Saída** (com `ate`): desfoque.

| campo | padrão | o que faz |
|---|---|---|
| `dados` | obrigatório | `[{ "rotulo", "valor" }]`, 1 a 5, valores ≥ 0. **Só dado real** |
| `maximo` | o maior valor | o 100% do trilho (use 100 para porcentagens) |
| `prefixo`, `sufixo`, `casas` | `""`, `""`, 0 | o formato (pt-BR: vírgula decimal) |
| `titulo`, `fonte` | nenhum | o título e a linha "FONTE: ..." |
| `marca` | o maior | o índice (de 0) da barra com o marca-texto, ou `false` |
| `t_marca` | o fim das barras + 0,1 | quando o marca-texto passa |
| `passos` | `false` | o crescimento em degraus (12 qps, o "Vox") |
| `x`, `y`, `w` | 70, 290, 940 | a placa (a altura sai das barras: 2 barras ≈ 312 px) |

Eventos: `entra` (peso 2), `conta` (peso 2, **tick**), `marca` (peso 1, tick se couber).

```json
{ "tipo": "barras", "t": 3.15, "ate": 6.5, "titulo": "Líderes de dados", "fonte": "Salesforce",
  "dados": [ { "rotulo": "Confiáveis", "valor": 74 }, { "rotulo": "Não confiáveis", "valor": 26 } ],
  "sufixo": "%", "maximo": 100, "marca": 1, "t_marca": 5.05 }
```

## Custo por quadro

Medido no M4, render inteiro do corte de teste (1080 x 1920, sem GPU): **106 a 136 ms por quadro em
média** no reel de demonstração (a cena sem peça custa ~45 ms). Por trecho, peça já somada à cena:

| trecho | ms por quadro |
|---|---|
| `mira` | 58 |
| `diagrama` (rótulos e cota) | 55 |
| `grade-synthwave` + `barras` | 89 |
| `linhas-foco` + `recorte` (sem 12 qps) + impacto | 100 |
| `chuva` | 103 |
| `moldura-crt` | 112 |
| `papel` + `luz` + `poeira` | 139 |
| `recorte` em 12 qps + `luz` | 154 |
| `moldura-crt` com `fosforo` + `chuva` (o pior) | 163 |

O que pesa: o `backdrop-filter` (fósforo, impacto), o canvas de tela cheia por quadro (chuva, grade,
poeira) e, no `recorte`, as duas vistas com máscara mais a dilatação do contorno (em meia resolução da
máscara; 9 `drop-shadow` em tela cheia custavam 2,5 a 4 s por quadro e foram trocados). O `recorte`
carrega antes do primeiro quadro todas as máscaras da vida dele (~2 MB cada decodificada): avisa acima
de 600 quadros.

## Limites conhecidos

- A `moldura-crt` não curva a imagem (barril): é moldura, vidro e scanlines por cima. O barril de verdade
  é do `look` (`efeito: "crt"`), que trata a imagem do vídeo; os dois combinam.
- O impacto e o fósforo usam `backdrop-filter`, que vê a cena por baixo da peça na mesma cena; peças de
  outras cenas ou do reel inteiro (`CENAS.sobre`) por cima não entram no filtro.
- `recorte` com `"fundo": "nenhum"` mostra a pessoa original por baixo durante o pulo da entrada (de
  propósito: o adesivo descola). Com fundo trocado, a troca sobe em dois degraus (0,13 s) e, nesse
  instante, a cabeça original aparece acima da faixa.
- O alvo `mao` depende de a mão ser vista: buraco no dado repete o último ponto; mãos que somem por
  segundos deixam a mira parada no último lugar.
- Placa de texto no alto (`barras`, `mira` acima da cabeça) tira o lugar da legenda quando a pessoa
  gesticula: a legenda fica sobre a mão e o motor avisa (`legenda (reel)`). Use `y` mais alto ou menos
  barras nesses trechos.
