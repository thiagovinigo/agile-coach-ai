# O motor 2.0

O motor monta o reel inteiro, 1080 x 1920, num navegador sem tela: o vídeo da fala entra por baixo
como quadros, e por cima vêm as cenas, o vidro, a legenda e as transições, tudo animado por uma linha
do tempo GSAP pausada que é posicionada no instante de cada quadro. O mesmo instante gera sempre o
mesmo quadro.

Este arquivo é o **contrato** entre as peças. Quem escreve o plano (o planejador), quem renderiza (o
compositor), quem corta a fala, quem segue o rosto, quem faz o áudio e quem confere lêem e escrevem
exatamente os formatos daqui. Mudou um formato, muda aqui primeiro.

Tudo é gratuito: GSAP (licença "No Charge"), Playwright/Chromium, FFmpeg, MediaPipe (Apache-2.0), Depth
Anything V2 Small no onnxruntime (Apache-2.0, a visão do corte, seção 2.6) e efeitos sonoros sintetizados
pelo próprio pacote. Nenhuma peça depende de serviço pago, e tudo roda no próprio computador.

---

## 1. A ordem das peças

```
fonte  ──►  editar_fala.py  ──►  fala.mp4 + palavras-corte.json + edicao.json
                                   │
            rosto.py  ◄────────────┤  (rosto.json, opcional)
                                   │
            visao.py  ◄────────────┤  (visao/, opcional: recorte, fundo limpo, profundidade, mãos...)
                                   │
   cenas.json (o plano)  ──►  compor.py  ──►  video.mp4 (sem som) + eventos.json + layout.jsonl
                                                │
                                   audio.py  ◄──┘  ──►  audio-final.wav  ──►  corte-NN/corte-NN.mp4
                                                │
                              conferir_reel.py  ◄──  (os gates leem tudo isso)
```

Todos os arquivos de trabalho de um corte moram em `projetos/<video>/materiais-de-trabalho/corte-NN/`
(chamada aqui de **pasta do corte**). A entrega continua sozinha em `projetos/<video>/corte-NN/`.

| arquivo | quem escreve | o que é |
|---|---|---|
| `fala.mp4` | `editar_fala.py` | o vídeo da fala já editado: só os trechos do corte, sem silêncio longo, hesitação nem frase repetida, já na velocidade final |
| `palavras-corte.json` | `editar_fala.py` | as palavras na linha do tempo do `fala.mp4`, com a grafia corrigida |
| `edicao.json` | `editar_fala.py` | o que foi mantido, o que saiu e por quê, e onde ficaram as emendas |
| `rosto.json` | `rosto.py` | a caixa do rosto em cada quadro do `fala.mp4`, suavizada |
| `visao/` | `visao.py` | opcional (3.0, Onda 2): recorte da pessoa, fundo limpo, profundidade, mãos, corpo e objetos, quadro a quadro (seção 2.6) |
| `folha-visao.png` | `visao.py` | a folha de contato da visão: olhe antes de planejar texto atrás de você ou camadas |
| `cenas.json` | o planejador | o plano de cenas: modo, conteúdo, tempos, transições |
| `video.mp4` | `compor.py` | o reel renderizado, sem som |
| `eventos.json` | `compor.py` | todo acontecimento visual com seu tempo (base do gate de ritmo e dos efeitos sonoros) |
| `layout.jsonl` | `compor.py` | por quadro: onde estão os textos, a legenda e o rosto (base dos gates de zona e de colisão) e, com texto atrás de você, quanto a pessoa cobre de cada um |
| `contraste/` | `compor.py` | quadros amostrados renderizados sem texto, para medir contraste |
| `audio-final.wav` | `audio.py` | a fala com volume normalizado, os efeitos sonoros e a trilha de fundo (se o plano pedir) mixados |

---

## 2. Formatos dos arquivos de dados

Todos em JSON, UTF-8, tempos em segundos com até 3 casas, coordenadas em pixels inteiros.

### 2.1 `palavras-corte.json`

O mesmo contrato do `palavras.json` da transcrição, só que na linha do tempo do `fala.mp4`:

```json
{ "palavras": [ { "inicio": 0.12, "fim": 0.41, "texto": "Sua" } ],
  "meta": { "fonte": "fala.mp4", "duracao": 41.87, "velocidade": 1.0, "grafia_aplicada": true } }
```

### 2.2 `edicao.json`

```json
{
  "fonte": "materiais-de-trabalho/fonte/AI-DATA-FIRST.mp4",
  "velocidade": 1.0,
  "duracao": 41.87,
  "segmentos": [ { "de": 0.40, "ate": 12.31, "saida_de": 0.0, "saida_ate": 11.91 } ],
  "removidos": [ { "de": 12.31, "ate": 12.95, "motivo": "silencio", "texto": "" },
                 { "de": 20.10, "ate": 20.42, "motivo": "hesitacao", "texto": "é" } ],
  "emendas": [ 11.91 ]
}
```

`de`/`ate` são tempos da fonte; `saida_de`/`saida_ate` e `emendas` são tempos do `fala.mp4`.
`motivo` vale `silencio`, `hesitacao`, `repeticao` ou `fora-do-trecho`. O `compor.py` lê as `emendas`
para esconder o pulo com o zoom alternado (seção 3). O editor também grava
`trechos`, `parametros`, `suspeitas` (o que pareceu hesitação ou repetição mas ficou, para alguém ouvir)
e `emendas_suspeitas` (emenda que caiu em som).

### 2.3 `rosto.json`

```json
{ "fps": 30, "largura": 1080, "altura": 1920,
  "quadros": [ [412, 380, 260, 300, 0.97], null, [414, 381, 259, 301, 0.96] ],
  "mediana": [413, 380, 260, 300] }
```

Uma entrada por quadro do `fala.mp4`, `[x, y, w, h, confiança]` em pixels da fonte, já suavizada.
`null` = rosto não achado naquele quadro (o motor usa o último conhecido ou a mediana).

### 2.4 `eventos.json`

```json
{ "duracao": 41.87,
  "cenas": [ { "id": "c1", "modo": "rosto-vidro", "inicio": 0.0, "fim": 6.2, "transicao": "corte" } ],
  "eventos": [ { "t": 0.0, "tipo": "cena", "peso": 3, "alvo": "c1", "som": null },
               { "t": 1.9, "tipo": "entra", "peso": 2, "alvo": "numero-26", "som": "pop" },
               { "t": 6.2, "tipo": "transicao", "peso": 3, "alvo": "lamina", "som": "whoosh" } ] }
```

`tipo`: `cena`, `entra`, `sai`, `acende`, `conta`, `zoom`, `transicao`, `marca`, `camera`.
`peso`: 1 = detalhe (um destaque muda), 2 = elemento grande entra ou sai, 3 = recomposição (cena nova,
transição). `som`: `whoosh`, `pop`, `tick`, `clique`, `subida`, `clarao` e, na 4.0, `glitch`, `rebobina`,
`impacto`, `estatica`, `energia`, `carimbo`, `bip`, `obturador`, `raio`, ou `null` (os arquivos estão em
`componentes/sons/`, sintetizados pelo próprio pacote). Cada família tem de 3 a 5 variações: o `audio.py`
escolhe uma por hash do instante e do alvo, nunca a mesma em dois eventos seguidos, e toca no máximo um
som a cada 1,5 s por peça (`"whoosh-2"` pede um arquivo exato). Contrato em `docs-4/variedade-e-som.md`.

### 2.5 `layout.jsonl`

Uma linha por quadro renderizado:

```json
{"i": 57, "t": 1.9, "cena": "c1", "modo": "rosto-vidro", "transicao": false,
 "textos": [[90, 300, 900, 420]], "legenda": [120, 1250, 840, 96], "rosto": [300, 420, 480, 560],
 "palavra": "26%"}
```

`textos` = caixas de todo elemento com texto visível (atributo `data-texto`), fora a legenda.
`rosto` = a caixa do rosto já levada para coordenadas de saída, quando há rosto na tela.
`transicao` = o quadro cai dentro da janela de uma transição. Ali o texto está de passagem (a lâmina
varre, o chicote empurra a cena para fora), e os gates de zona e de rosto não contam esse quadro.

Com texto atrás de você no plano (`"atras": true`, seção 3.3), a linha ganha também:

```json
"atras": [ { "id": "pilha (c1-pilha-1)#1", "peca": "pilha (c1-pilha-1)", "texto": "AI FIRST",
             "caixa": [214, 330, 652, 118], "coberto": 0.18, "topo": 402 } ]
```

- `coberto`: a fração da caixa do texto que a pessoa cobre naquele quadro, de 0 a 1 (máscara ≥ 128).
- `topo`: até onde a pessoa sobe na coluna do texto, em y de saída, ou `null` quando ela não chega lá.
- `id`: estável de um quadro para o outro, `"<peça>#<índice do texto dentro da peça>"`.
- Sem `atras` no plano, a chave não existe. O gate de contraste lê essa chave (seção 3.3).

### 2.6 A visão do corte: `visao/` (3.0, Onda 2)

Quem escreve é o `scripts/visao.py`: uma análise do `fala.mp4` quadro a quadro, feita uma vez por corte e
gravada em `materiais-de-trabalho/corte-NN/visao/`. É ela que deixa o motor pôr texto atrás de você,
separar você do fundo em camadas, pintar a profundidade e desenhar as mãos e as caixas de detecção.
Tudo roda local e de graça: MediaPipe (segmentadores, mãos, corpo e objetos) e Depth Anything V2 Small
no onnxruntime, os dois Apache-2.0, com os modelos em `componentes/modelos/`. O `compor.py` entrega o
resultado ao motor como `window.VISAO`. Sem a pasta, `window.VISAO = null` e o motor é exatamente o de
antes; quem pede uma peça que precisa dela recebe um `Error` que manda rodar o `visao.py`.

```
flow-reels produzir/visao --projeto projetos/<v> --corte NN
flow-reels produzir/visao --projeto projetos/<v> --corte NN --so maos,corpo
flow-reels produzir/visao --projeto projetos/<v> --corte NN --refazer
```

**4.3: profundidade estável e cabelo.** A profundidade padrão agora é o Video Depth Anything Small
(Apache-2.0, exportado para ONNX em `componentes/modelos/vda-small-codificador.onnx` e
`vda-small-cabeca.onnx`; a cabeça temporal roda em janelas de 32 quadros no CoreML): 9 vezes menos tremor no
fundo parado, ~1,04x o tempo do DAv2, +1,2 GB de pico. `--profundidade dav2` volta ao modelo antigo (fundo com
mais relevo). O cabelo é refeito pelo BiRefNet_lite (MIT, `birefnet-lite-640.onnx`) na caixa da cabeça, em 1
de cada 10 quadros e nas pontas dos trechos, propagado por fluxo óptico e limitado à faixa do contorno e ao
que a profundidade não diz ser parede: `--cabelo auto|sim|nao` (auto liga quando cabe em ~3 min; +100 a 145 s
por reel de 40 s). Versões: mascara 3, profundidade 3, fundo 4. O `visao.json` ganha `profundidade.modelo`,
`cabelo`, `tempos.profundidade_modelo`, `tempos.cabelo`, `caminhos.profundidade`, `caminhos.cabelo`, e o
`.origem.json` ganha `variantes`. Como refazer os ONNX: `componentes/modelos/exportar-modelos-4-3.py`.
Detalhes e medidas em `docs-4/visao-4-3.md`.

**O que a gravação precisa ter.** A visão só funciona bem com a pessoa de frente, em plano médio, com a
câmera parada no tripé (o fundo limpo é a mediana de vários quadros: câmera que anda borra o fundo, e o
script avisa quando o fundo andou mais de 2 px entre as amostras). As mãos só servem de palco quando
sobem abertas até a altura do peito ou acima: no busto, a mão baixa fica abaixo da zona segura (y 1440).
O cenário com coisas a distâncias diferentes dá uma profundidade que separa você do fundo; parede lisa
colada atrás não separa.

**A grade de quadros é a mesma do `compor.py`.**
- O vídeo é o `cenas.json` → `fonte.video` (padrão `fala.mp4`), lido pelo ffmpeg com `-vf fps=<fps do
  plano, padrão 30>`.
- O quadro `i` (a partir de 0) é o instante `i / fps` e vai gravado com o número `i + 1`, como os
  `quadros-fonte/f%06d.jpg`. O quadro que o motor mostra e a máscara que ele aplica são sempre o mesmo.
- Quadro com mais de 1920 px de altura é reduzido para 1920 na análise. A máscara e o fundo saem nesse
  tamanho (o "tamanho de análise", `analise` no `visao.json`). Mãos, corpo, objetos e caixas voltam para o
  pixel da fonte.
- Nada que é alisado no tempo atravessa uma emenda do `edicao.json`: ali a imagem pula, e a máscara, a
  mão e a profundidade pulam junto. Os trechos entre emendas vão em `visao.json` → `segmentos`
  (`[a, b)` em índices de quadro). Se o `edicao.json` diz uma duração mais de 0,25 s diferente da do
  vídeo, as emendas dele são ignoradas, com aviso.

| arquivo | o que é |
|---|---|
| `mascara/m%06d.png` | 8 bits, cinza, sem alfa: branco = pessoa. Uma por quadro, no tamanho de análise. A confiança da pessoa é o maior dos dois segmentadores (o Selfie Segmenter em quadrados sobrepostos, para o quadro vertical não chegar achatado no quadrado de 256 do modelo, e o Selfie Multiclass, que pega melhor o cabelo e a mão de lado), corrigido pela profundidade: o que está tão longe quanto a parede cai, o que está tão perto quanto o corpo entra (o braço que os dois perdem). Sem separação de profundidade (pessoa colada na parede), valem só os segmentadores. Depois: uma média de 5 quadros que só junta o vizinho onde a imagem não mudou (a mão que passa não deixa rastro), o filtro guiado na imagem colorida (a borda vai para a borda de verdade, fio de cabelo incluído), buraco pequeno tapado (menos de 0,15% do quadro), ilha solta apagada (menos de 0,3%) e a borda firmada: abaixo de 0,25 é fundo, acima de 0,75 é pessoa, e o miolo é opaco. |
| `fundo-limpo.jpg` | O cenário sem a pessoa, tirado do próprio clipe, no tamanho de análise: a mediana pixel a pixel das amostras em que aquele pixel é fundo (a pessoa dilatada ~12 px num quadro de 576 de largura), com até 150 amostras espalhadas pelo vídeo e no máximo 90 milhões de pixels guardados (~43 amostras em 1080 x 1920). O que foi visto em menos de 3 amostras é **inventado** (abaixo). |
| `fundo-buraco.png` | Branco = a parte inventada do `fundo-limpo.jpg`: o que foi visto em menos de 3 amostras. |
| `profundidade/p%06d.png` | 8 bits, **relativa**: o inverso da distância, 255 = mais perto. Não é metro, e nenhuma peça pode mostrar metro a partir dela. Vem na resolução do modelo (múltiplos de 14 com ~76 mil pixels: 210 x 364 num 9:16), normalizada pelos percentis 1 e 99 do vídeo inteiro (a mesma régua em todos os quadros, então dá para comparar um quadro com outro). Suavizada no tempo só onde a imagem não mudou: um binômio de 5 quadros (1-4-6-4-1) em que o peso do vizinho cai com a diferença de luma (σ 10) e com a diferença de profundidade (σ 12), dentro de cada trecho. A mão que passa não deixa rastro no mapa. |
| `maos.json` | `{fps, largura, altura, modelo, licenca, lado, quadros: [ [ {lado, score, medido, pontos: [[x, y, z] × 21]} ] ]}`. Uma lista por quadro (`[]` = nenhuma mão), no máximo uma mão de cada lado, em pixels da fonte. Os 21 pontos são os do Hand Landmarker (0 = pulso, 4 = ponta do polegar, 8 = ponta do indicador, 9 = nó do dedo médio). `z` é a profundidade relativa ao pulso, na escala do `x`; menor = mais perto da câmera. `score` = a confiança da classificação esquerda/direita do MediaPipe. |
| `corpo.json` | `{fps, largura, altura, modelo, licenca, quadros: [ null \| {score, medido, pontos: [[x, y, visibilidade] × 33]} ]}`. Os 33 pontos do Pose Landmarker Lite, em pixels da fonte (11 e 12 = ombros, 15 e 16 = pulsos); um ponto pode cair fora do quadro. `score` = a média da presença dos 33 pontos: num busto, as pernas fora do quadro puxam para baixo (0,33 a 0,69 no corte de teste), então ele não é confiança de nada que apareça na tela. Suavizado com One Euro; falha de até 3 quadros é preenchida. |
| `objetos.json` | `{fps, largura, altura, modelo, licenca, passo: 3, limiar: 0.5, quadros: [ [ {categoria, categoria_en, score, medido, caixa: [x, y, w, h]} ] ]}`. EfficientDet-Lite0 (COCO), com `categoria` em português ("pessoa", "livro", "celular"...) e a caixa em pixels inteiros da fonte. Roda 1 quadro a cada 3 e nas pontas de cada trecho, com confiança mínima 0,5 (abaixo disso ele acha rosquinha em mão fechada). Entre duas análises do mesmo trecho, a caixa que casa (mesma categoria, IoU ≥ 0,3) é interpolada; a que não casa vale só nos quadros mais perto da análise dela. Antes da primeira análise e depois da última, vale a mais perto. |
| `visao.json` | Os metadados, descritos abaixo. |
| `.origem.json` | De que vídeo e de que versão é cada parte (abaixo). Não edite. |
| `../folha-visao.png` | Na pasta do corte: a folha de contato. O fundo limpo e o buraco; 6 instantes com a máscara (contorno no acento), o recorte sobre xadrez, a profundidade (roxo longe, âmbar perto) e as mãos, o corpo e os objetos; e a cabeça ampliada. Parte que não vale para este vídeo aparece como "sem máscara", "sem fundo limpo", nunca como 0%. **Olhe antes de usar:** contorno colado na pessoa, cabelo inteiro, fundo sem fantasma, mãos com o lado certo. |

**O fundo inventado.** Num vídeo de fala sem cenário vazio, a pessoa nunca sai da frente de boa parte da
parede: no corte de teste, 48,9% do fundo é inventado. O script continua a parede em duas camadas. A
cor vem da parede em volta, puxada de perto para longe (push-pull em 1/4 do tamanho); prateleira escura,
neon e luz pesam quase nada, para não virarem mancha. Por cima vai a textura da própria parede, em
blocos de duas fiadas trazidos de cima ou de baixo por múltiplos do passo das fiadas medido nela (27 px
no teste): o rejunte continua na mesma altura e a amarração do tijolo desencontra meio bloco. Isso é
uma continuação plausível, **não o que estava lá**. De perto se vê a repetição dos blocos, a emenda
lateral entre dois blocos corta alguns tijolos, e um canto longe da parede vista pode pegar uma cor
puxada de longe. O `camadas` esconde isso na placa de trás (seção 4.11), mas a solução de verdade é da
gravação: **no fim, saia do quadro e deixe a câmera gravando de 3 a 5 s do cenário vazio**, sem tocar
nela. Esse trecho entra na mediana e o buraco some.

**Mãos.**
- `lado` é de quem assiste: `"esquerda"` é a mão que aparece à esquerda na tela. Com as duas mãos no
  quadro, a "esquerda" está sempre à esquerda da "direita" pelo pulso; com as mãos entrelaçadas, o
  centro dos 21 pontos pode cruzar (os dedos cruzam), o pulso não.
- O lado é da trilha inteira de uma mão física, e não de cada quadro: a mão que cruza o meio continua
  a mesma. Com as duas mãos, decide a posição de uma em relação à outra; sozinha, o lado do meio do corpo
  (os ombros do `corpo.json`, senão o rosto do `rosto.json`) em que ela apareceu.
- A leitura repetida (o MediaPipe às vezes devolve duas "mãos" em cima de uma só) vira uma. A trilha que
  sumiu há mais tempo perde a mão para a trilha vista agora; a trilha acaba depois de 15 quadros sem a
  mão, numa emenda, ou quando a classificação Left/Right do MediaPipe troca firme (3 leituras de cada
  lado): é a leitura escorregando de uma mão para a outra com as mãos juntas.
- Falha de até 3 quadros dentro de um trecho é interpolada; depois, One Euro trilha a trilha, numa
  passada para a frente e outra para trás (a média das duas não atrasa).

**Confiança (`medido`).**
- Toda mão, corpo e objeto leva `"medido": true` no quadro em que o modelo rodou e achou, e `false` no
  quadro preenchido: a falha curta das mãos e do corpo, os quadros entre duas análises dos objetos.
- O `score` é sempre um número que o modelo deu. No quadro preenchido, é o da análise mais perto,
  nunca uma mistura.
- Peça que mostra confiança na tela usa o último quadro medido (seção 4.10).

**`visao.json`.**

| campo | o que é |
|---|---|
| `versao`, `fonte`, `fps`, `largura`, `altura` | a versão do script, o nome do vídeo, a fps e o tamanho da fonte |
| `analise` | `[w, h]` do quadro de análise (o da máscara e do fundo) |
| `total` | quadros analisados |
| `segmentos` | `[[a, b], ...]`: os trechos entre emendas, em índices de quadro, `b` fora |
| `modelos` | `{chave: {arquivo, nome, licenca}}` dos seis modelos |
| `caminhos` | onde cada parte rodou: `segmentador` na CPU; `maos`, `corpo` e `objetos` no Metal (no Mac) |
| `tempos` | segundos de cada fase (`analise`, `profundidade`, `mascara`, `fundo`, `total`) |
| `partes` | `{mascara, fundo, profundidade, maos, corpo, objetos}`: `true` = vale para este vídeo |
| `pessoa` | `{porcentagem, caixas: [[x, y, w, h] \| null por quadro]}`, em pixels da fonte: a caixa da máscara (≥ 128) em cada quadro, `null` com menos de 0,5% do quadro. O `y` é o alto do cabelo de verdade. `null` sem máscara válida |
| `profundidade` | `{escala, tamanho: [w, h], percentis_brutos, mediana_pessoa, mediana_fundo, pessoa: [...], fundo: [...]}`: a mediana da profundidade (0 a 255) da pessoa e do fundo, por quadro (`null` no quadro sem uma das duas). As medianas saem da máscara: sem máscara válida, saem as medianas e as listas por quadro, e fica só a régua (`percentis_brutos`). `null` sem profundidade válida |
| `fundo` | `{amostras, passo, buraco, camera_px}`: quantas amostras e de quantos em quantos quadros, a % do quadro inventada e quanto a câmera andou entre as amostras. `null` sem fundo válido |
| `maos`, `corpo` | `{porcentagem}` de quadros com pelo menos uma leitura, ou `null` |
| `objetos` | `{passo, limiar, categorias: {nome: % de quadros}}`, ou `null` |

**Reaproveitamento e o `.origem.json`.** Ele guarda o vídeo (caminho absoluto, data, tamanho em bytes,
fps), o `total`, a `versao` do script (2), as `versoes` de cada parte e as `partes` que valem. Hoje as
versões são `{mascara: 2, fundo: 3, profundidade: 2, maos: 3, corpo: 2, objetos: 2}`.
- Uma parte gravada vale quando o vídeo é o mesmo, a versão daquela parte é a atual e os arquivos estão
  lá (uma máscara e uma profundidade por quadro). Sem `--refazer`, ela é reaproveitada.
- Subir a versão de uma parte refaz só ela na próxima rodada. Quem analisou com versões anteriores
  refaz máscara, fundo, profundidade e mãos.
- `--so` faz só as partes da lista. O fundo sai da máscara: refazer a máscara refaz o fundo, e o fundo
  sem máscara que valha puxa a máscara junto. A máscara usa a profundidade: sem uma que valha, ela é
  refeita e gravada também. As mãos usam o corpo (os pulsos e os ombros): sem o corpo nesta rodada, vale
  o `corpo.json` gravado, então `--so maos` dá o mesmo que a rodada inteira.
- `--refazer` refaz as partes pedidas sem invalidar as outras.
- Depois de trocar o `fala.mp4`, um `--so` grava `null` no `visao.json` em tudo que não vale para o vídeo
  novo (pessoa, profundidade, fundo e os resumos), e o relatório e a folha só mostram o que vale. O
  script avisa quais partes são de outro vídeo e o `--so` que falta. Rode sem `--so` depois de reeditar.
- O script nunca apaga arquivo: se o vídeo novo é mais curto, as máscaras e profundidades a mais ficam na
  pasta, e o `compor.py` avisa `a visão tem N máscaras e o vídeo tem M quadros`.
- **Copiar a pasta `visao/` de outro corte não serve.** O `.origem.json` aponta para o `fala.mp4` de lá,
  e o `compor.py` segue com `VISAO = null`. Rode o `visao.py` no corte novo (ele refaz tudo, porque a
  origem é outra), mesmo que o vídeo seja uma cópia.

**O que o `compor.py` faz com ela.** Sem `visao/`: `window.VISAO = null`. Com a pasta feita de outro
vídeo (caminho, data, tamanho ou fps diferentes do `.origem.json`): `null` também, com aviso, porque uma
máscara de outra edição cairia fora da pessoa. Senão, a parte que não vale vem `null`:

```js
window.VISAO = {
  mascara: { padrao: "/projetos/<v>/materiais-de-trabalho/corte-NN/visao/mascara/m%06d.png", total, largura, altura },
  fundo: "/…/visao/fundo-limpo.jpg", buraco: "/…/visao/fundo-buraco.png",
  profundidade: { padrao: "/…/visao/profundidade/p%06d.png", total, largura, altura },
  maos: <maos.json>, corpo: <corpo.json>, objetos: <objetos.json>, meta: <visao.json> }
```

O `meta` vem inteiro; desde que o `visao.py` grava `null` nas partes que não valem, ele não traz dado de
outro vídeo. Quem lê `meta.pessoa` ou `meta.profundidade` confere se é `null`.

**Tempo, memória e máquina.**
- 36 s em 576 x 1024, no M4: ~2 min com a máquina livre (111 a 131 s medidos: análise de 83 a 100 s,
  máscaras de ~21 s, fundo de 2,5 s). Com outros renders rodando ao mesmo tempo, passou de 4 min.
  Duas rodadas dão o mesmo resultado, bit a bit.
- Pico medido de 2,15 GB. A memória cresce ~0,6 MB por quadro (a confiança bruta dos segmentadores e a
  profundidade), mais uma parte fixa; a luma guardada para alisar a profundidade soma ~76 KB por quadro
  (estimado pelo tamanho, não medido no pico).
- No Mac, o segmentador roda na CPU; mãos, corpo e objetos só rodam no Metal (o caminho de CPU dos
  detectores do MediaPipe aborta). Cada caminho é testado antes num processo separado; a parte que não
  abre fica de fora, com aviso (sem o segmentador, o script para). Os detectores são fechados e abertos
  de novo a cada 100 quadros e em cada emenda, porque o Metal retém de 2 a 5 MB por quadro até o
  `close()`, e o rastreio do detector não deve atravessar o corte.
- O import do MediaPipe carrega o `sounddevice`, que abre o CoreAudio; com o `coreaudiod` ocupado, cada
  import esperava ~60 s. O script põe um `sounddevice` vazio no lugar antes de importar (ele só serve para
  gravar áudio, que a visão não usa).

Saída 0 = gravou. 1 = gravou, mas a pessoa apareceu em menos da metade dos quadros (olhe a folha antes de
pôr texto atrás de você). 2 = erro de uso ou de ambiente (falta ffmpeg, modelo, `opencv-contrib-python`,
o `fala.mp4` ou o segmentador não abriu).

---

## 3. O plano: `cenas.json`

```json
{
  "versao": 1,
  "fps": 30,
  "duracao": 41.87,
  "fonte": { "video": "fala.mp4" },
  "videos": { "painel": "painel.mp4" },
  "legenda": { "estilo": "palavra-acesa", "enfase": ["26%", "89%", "Salesforce"] },
  "cenas": [
    { "id": "c1", "modo": "rosto-vidro", "inicio": 0.0, "fim": 6.2,
      "entrada": { "transicao": "corte" },
      "zoom": [ { "t": 1.9, "escala": 1.1, "segura": 1.2 } ],
      "conteudo": { ... depende do modo, seção 4 ... } }
  ]
}
```

Regras do plano:

- As cenas cobrem o corte inteiro, sem buraco e sem sobreposição: o `fim` de uma é o `inicio` da
  próxima, a primeira começa em 0 e a última termina em `duracao`.
- Todos os tempos são **absolutos**, na linha do tempo do `fala.mp4` (a mesma do
  `palavras-corte.json`). Um elemento que entra "na palavra 26%" usa o `inicio` dessa palavra menos
  0,2 s, para o movimento terminar em cima da palavra.
- Caminhos de arquivo (`imagem`, `videos`, `painel`) são relativos à pasta do corte.
- `legenda.estilo`: `palavra-acesa` (padrão), `pop`, `caixa` ou `revela` (3.0). Uma cena pode trocar com
  `"legenda": {"estilo": ...}` ou desligar com `"legenda": false`. O contrato inteiro do `revela` e da
  altura está na seção 3.2.
- `legenda.posicao` (`"peito"`, `"topo"`, `"base"`) ou `legenda.y`, no reel ou na cena: a altura da
  legenda, para qualquer estilo (seção 3.2).
- `sobre`: as sobreposições, no reel (`CENAS.sobre`) ou na cena (`cena.sobre`): seção 4.10. Qualquer
  uma aceita `"atras": true`, que a põe atrás de você (seção 3.3, precisa da visão do corte).
- `legenda.desvia_maos`: com a visão do corte, a legenda foge das mãos; `false` desliga (seção 3.2).
- `trilha`: a trilha de fundo, lida só pelo `audio.py`: seção 3.1.
- `legenda.enfase`: palavras que ficam no acento a cena inteira e crescem um pouco. Números entram
  sozinhos.
- `zoom`: zoom de ênfase no rosto da cena. `escala` de 1,05 a 1,15, `segura` = quanto tempo fica
  aproximado antes de voltar (padrão 1,2 s).
- `entrada.transicao`: uma das transições da seção 5. `duracao` opcional.
- `emendas`: a emenda escondida. Em cada emenda do `edicao.json` que cai dentro de uma cena com rosto
  (longe mais de 0,3 s da troca de cena), o rosto troca de escala na hora, alternando 1 e 1,07, como
  uma segunda câmera. `"emendas": {"escala": 1.1}` muda o quanto; `"emendas": false` desliga. Fica
  numa camada própria da vista, então convive com o `zoom` de ênfase.

### 3.1 A trilha de fundo: `trilha` (3.0)

Chave de topo do `cenas.json`, ao lado de `"cenas"`. Quem lê é o `audio.py`. O motor ignora essa chave e não muda nada na imagem.

```json
"trilha": {
  "arquivo": "componentes/trilhas/calma-piano-01.mp3",
  "volume_db": -18,
  "ducking": true,
  "entra": 0.0,
  "fade_entrada": 0.6,
  "fade_saida": 1.2,
  "inicio_no_arquivo": 0.0
}
```

| campo | padrão | o que faz |
|---|---|---|
| `arquivo` | (obrigatório) | a faixa, em qualquer formato que o ffmpeg leia. É procurada primeiro na pasta do corte e depois na raiz do pacote (`componentes/trilhas/...`); também aceita caminho absoluto. Precisa ter pelo menos 1 s de música |
| `volume_db` | -18 | quanto a trilha fica abaixo do LUFS integrado da voz **sem o ducking**: é o nível dela antes de a voz começar e nas pausas longas. É medido só no trecho que toca, antes dos fades. Valor positivo vira negativo, com uma nota. Com o ducking, a trilha fica 24 dB abaixo da voz enquanto ela fala. O reel de referência tinha uns 18 dB com a voz falando, o que pede -12 |
| `ducking` | `true` | com a voz falando e nas pausas curtas, a trilha fica mais 6 dB abaixo. Ela só sobe numa pausa de 1,2 s ou mais. `false` desliga; um número é a profundidade em dB, de 0 a 24 |
| `entra` | 0 | o segundo do reel em que a trilha começa. Antes disso, silêncio. Precisa sobrar pelo menos 1 s até o fim |
| `fade_entrada` | 0,6 | segundos de fade a partir do `entra` (no máximo metade do trecho que toca) |
| `fade_saida` | 1,2 | segundos de fade até o fim do reel (idem) |
| `inicio_no_arquivo` | 0 | de que segundo da faixa ela começa a tocar, para pular uma introdução. O loop repete a partir daí |

- `"trilha": "componentes/trilhas/x.mp3"` é o atalho para informar só o arquivo; o resto fica no padrão.
- `"trilha": false`, ou nenhuma chave, deixa o corte sem trilha. Nesse caso o som sai igual ao de antes, bit a bit (conferido contra o audio.py anterior em três cortes).
- Trilha mais curta que o reel entra em loop: o silêncio das pontas é aparado e cada volta é cruzada em 0,25 s com potência constante. Trilha mais longa é cortada no fim.
- O ducking tem profundidade fixa e é decidido pausa a pausa, com a voz como chave, porque o script tem a fala inteira antes de misturar. A voz é lida em quadros de 10 ms, com ponderação K, e conta como presente a até 24 dB do seu LUFS. Buraco menor que 0,1 s dentro da fala conta como fala; estalo isolado menor que 50 ms não conta.
  - Pausa de menos de 1,2 s não mexe na trilha.
  - Numa pausa mais longa, a trilha espera 0,25 s depois da última sílaba, sobe em 0,5 s numa curva de cosseno e fica lá em cima pelo menos 0,25 s. Depois desce em 0,2 s, e a descida termina no instante em que a voz volta.
  - Antes da primeira palavra, quem sobe a trilha é o fade de entrada; depois da última, quem desce é o de saída.
  - Não há compressor nem portão, porque os dois só sabem que a pausa é longa depois que ela já durou, e por isso bombeiam.
- A ordem da mistura é voz + efeitos + trilha. Depois vêm o loudnorm em duas passadas (-14 LUFS, -1 dBTP) e a entrega, como antes.
- Os gates de sincronia e de emendas leem o `fala.mp4`, então a trilha não interfere neles.

Linha de comando:
- `--musica <arquivo>` troca o `arquivo`; o resto vem do `cenas.json` ou do padrão.
- `--musica-db <dB>` troca o `volume_db`. Num corte sem trilha, ele avisa que não mudou nada.
- `--sem-trilha` ignora a trilha do plano. Junto com `--musica` ou `--musica-db`, é erro de uso (saída 2).

O `audio.py` imprime o que mediu, sempre contra o LUFS integrado da voz e em quadros de 100 ms, sem contar os fades:

```
  trilha                 calma-piano-01.mp3 (cenas.json): fades de 0.6 s e 1.2 s
      pedido              18 dB abaixo da voz; com a voz falando, mais 6 dB (ducking)
      trilha x voz        sem ducking -18.1 dB  ·  voz falando -24.0 dB  ·  pausas curtas -24.6 dB em 17 quadro(s) de 100 ms
      pausas longas       nenhuma de 1.2 s ou mais: a trilha fica abaixada do primeiro ao último som da voz
      voz sobre a trilha  +25.0 dB com a voz falando (o ducking tirou 6.0 dB)
```

Quando alguma pausa solta a trilha: `pausas longas  a trilha subiu em 3: antes da 1ª palavra (até 1.56 s), 13.92 a 15.87 s, 19.39 a 22.43 s; no alto, -17.6 dB`. Quando um fade foi limitado, a linha mostra o fade real e o pedido. Com a voz menos de 12 dB acima da trilha, ele avisa. As regras de licença e de nome dos arquivos estão em `componentes/trilhas/LEIA.md`. O pacote não traz trilha nenhuma.

> Para a seção 1: na tabela, `audio-final.wav` passa a ser "a fala com volume normalizado, os efeitos sonoros e a trilha (se o plano pedir) mixados". No diagrama, o `audio.py` também lê o `cenas.json`, mas só a chave `trilha`. No SKILL.md, passo 6 da produção 2.0, cabe uma linha sobre a trilha opcional.

### 3.2 A legenda que revela e a altura da legenda (3.0)

- `legenda.estilo`: `palavra-acesa` (padrão), `pop`, `caixa` ou `revela`. Uma cena pode trocar com `"legenda": {"estilo": ...}` ou desligar com `"legenda": false`.
- `revela` (a legenda da 3.0):
  - A palavra só aparece quando é falada, 0,03 s antes do `inicio` dela, e se acumula na linha, até 3 por linha.
  - A mais nova fica no acento: no `--destaque-gradiente` quando `cores.destaque_gradiente` tem cores diferentes do acento chapado. As anteriores ficam em branco. Números e `enfase` continuam no acento.
  - Cada palavra nasce com 60% do tamanho e desfocada, e cresce até o tamanho em 0,09 s, presa à linha de base, no lugar que vai ter na linha completa. A linha é centrada pela largura final e nada que já está na tela se mexe.
  - A frase quebra na pontuação (a vírgula inclusive), na pausa acima de 0,4 s e na troca de cena. Depois é repartida em linhas equilibradas (4 palavras = 2 + 2), quebrando de preferência nos respiros da fala e sem fechar linha em artigo, preposição ou conjunção quando dá.
  - Linha que some para o silêncio sai em desfoque com leve subida (0,18 s), nunca antes de a última palavra acabar de ser dita. Com a próxima colada, a troca é seca. A última linha do reel fica até o fim.
  - Linha que ia nascer um quadro antes da cena dela nasce com a cena, e a anterior fica até lá.
  - O gate de contraste mede a cor pintada que menos se separa do contorno (`data-cor` na `.linha`).
  - A legenda não registra evento: o ritmo continua vindo da camada visual.
- Altura da legenda, para qualquer estilo, no `cena.legenda` ou no `CENAS.legenda` (o padrão do reel).
  - O da cena vale mais. O do reel não passa por cima de zona `fixa` (painel-rosto, tela-bolha, manchete): ali só a cena muda a altura.
  - Na mesma fonte, `y` vale mais que `posicao`. Valor inválido avisa no console e é ignorado, e vale a fonte seguinte.
  - `y`: número (ou texto numérico), o centro da linha em px de saída.
  - `posicao: "peito"`: 30 px abaixo do rosto mais baixo que aparece enquanto a linha está na tela, zoom de ênfase incluído. Se não couber antes da base da zona segura, vale a altura do modo: a linha nunca vai para cima da boca.
  - `posicao: "topo"`: y 330, para quando a ação está no peito. Sobe até o topo da zona segura quando a cabeça está alta.
  - `posicao: "base"`: a altura que o modo pede (`zonaLegenda`).
  - Com altura pedida no plano, e sempre no `revela`, a linha vai para o lugar livre mais perto do pedido: dentro da zona segura, sem cruzar card, texto ou logo (`data-texto` e `data-zona`) em nenhum quadro da linha, e sem cruzar o rosto. Numa zona fixa, o lugar pedido vale mesmo encostando no rosto, mas um lugar alternativo não.
  - Linhas vizinhas da mesma cena mantêm a altura quando a diferença é de até 28 px.
  - Os estilos antigos na altura do modo seguem o desvio de sempre: abaixo do queixo ou acima da cabeça, sem olhar os cards.
  - Toda altura é decidida uma vez por linha, a partir dos quadros dela. O mesmo instante dá o mesmo quadro em qualquer ordem de render.

```json
"legenda": { "estilo": "revela", "posicao": "peito" },
"cenas": [ { "id": "c4", "modo": "rosto-vidro", "legenda": { "posicao": "topo" }, ... } ]
```

**A legenda desvia das mãos (3.0, Onda 2).** Vale com as três condições juntas: a visão do corte tem as
mãos (`visao/maos.json`); a cena mostra o vídeo do rosto (a `vistaRosto` dela, nítida, na fonte
principal); e a linha tem altura pedida no plano (`y` ou `posicao`) ou é do `revela`. Os estilos antigos
na altura do modo e a zona `fixa` (a costura do painel-rosto, a faixa acima da bolha, a faixa do
`camadas`) nunca olham as mãos: ali a altura é parte do desenho do modo.

- **A mão** é a caixa dos 21 pontos com 24 px de folga, levada para a tela pelo `Motor.fonteParaTela` e
  cortada pela janela da vista. Conta como um card em todo quadro da linha fora das transições, cada
  quadro com o enquadre dele.
- **A cabeça** vai do alto da pessoa até o queixo. O alto vem de `visao.json` → `pessoa.caixas`, quadro a
  quadro: é o cabelo de verdade, inclusive com a pessoa inclinada para a câmera. Sem as caixas, ele é
  estimado: testa − 0,8 × a altura do rosto.
- **A decisão, uma vez por linha:**
  1. O lugar de antes não cruza mão: a linha fica nele, como sem a visão. Só o lugar alternativo do
     "lugar de antes" (quando um card ou texto toma o pedido) olha a cabeça: sem encostar nela ou, sem
     isso, entrando no cabelo no máximo 15% da caixa. Sem nenhum dos dois, a linha fica no pedido, com o
     aviso `legenda: sem lugar livre`, e o passo 2 vale a partir dali; nunca cai inteira dentro do cabelo
     acima do rosto.
  2. Cruza: a linha vai para o lugar limpo mais perto do pedido (dentro da zona segura e sem mão, card,
     texto, rosto nem cabeça): entre o queixo e as mãos, abaixo das mãos ou acima da cabeça.
  3. Sem lugar limpo: acima da cabeça, com a caixa entrando no cabelo no máximo 15% da altura dela.
  4. Sem nem isso: a linha fica por cima da mão e entra no aviso. Letra sobre a cabeça é pior que letra
     sobre a mão.
- **Lá em cima.** As linhas seguidas que sobem (até 2 s entre uma e outra) são uma corrida e dividem uma
  altura só, a mais perto de y 330 que serve a todas; sem altura comum, a corrida se parte. A linha livre
  presa entre duas que sobem, num vão de até 2 s, sobe junto se tiver lugar acima da cabeça; o vão é um
  só, ou todas sobem ou nenhuma. A corrida com menos de 1,2 s só sobe se a mão de verdade (sem a folga)
  cobre a letra em pelo menos metade dos quadros dela: por uma mão que só passa, dois saltos de 900 px
  são piores que a mão atrás da letra.
- **Histerese.** Continua valendo (até 28 px a linha fica na altura da anterior), mas nunca puxa a linha
  para cima de uma mão ou do cabelo, e a linha que vem depois de uma que subiu não toma a altura dela.
- **Aviso.** Um só por render, no `Motor.fecharAvisos`: `legenda (reel): aviso: N linhas ficam por cima
  de uma mão porque não há lugar sem mão, card, texto, rosto ou cabeça: <tempo> "<texto>" (...)`. Só entra
  a linha com a mão de verdade sob a letra por 3 quadros (0,1 s) ou mais. No `--quadro`, lista as linhas
  decididas naquela chamada.
- **Desligar.** `"desvia_maos": false` no `CENAS.legenda` (o reel) ou no `cena.legenda` (a da cena vale
  mais). Valor que não é `true` ou `false` avisa e é ignorado; `true` sem as mãos na visão avisa. Sem a
  visão, a legenda é a mesma de antes, quadro a quadro.
- A decisão vem só das medidas das linhas: o mesmo instante dá o mesmo quadro em qualquer ordem de render,
  e o `--quadro` mede a corrida inteira da linha dele.

```json
"legenda": { "estilo": "revela", "posicao": "peito" },
"cenas": [ { "id": "c3", "modo": "rosto-vidro", "legenda": { "desvia_maos": false }, ... } ]
```

### 3.3 Texto atrás de você: `"atras": true` (3.0, Onda 2)

Qualquer item de `cena.sobre` ou de `CENAS.sobre` pode levar `"atras": true`: a peça fica atrás da pessoa
e na frente do cenário. A cabeça passa por cima do título, como na abertura da referência.

```json
{ "tipo": "pilha", "t": 0.0, "ate": 1.45, "y": 200, "tam": 92, "linhas": ["A EMPRESA", "AI *FIRST*"],
  "fundo": "sombra", "atras": true }
```

- **Precisa da visão do corte** (a máscara). Sem `visao/`, o motor recusa o plano com o `Error` que manda
  rodar o `visao.py`.
- **O furo.** A cada quadro o motor abre na peça um furo do formato da pessoa: a máscara do quadro que a
  vista do rosto mostra, posta exatamente sobre a imagem da vista e limitada à janela dela (cantos
  redondos e elipse incluídos). No furo aparece a própria cena: a pessoa do vídeo (com zoom, emenda,
  escurecer e desfoque) e os cards do modo por cima dela. Nada é desenhado duas vezes. Com a vista
  desbotando, o furo desbota junto.
  - Sem giro entre a imagem e a peça, a máscara entra como camada CSS na resolução cheia, exata, também
    na transição que escala ou gira a cena inteira com a peça dentro.
  - Com giro (a placa do `vidro-liquido` inclinada, a placa da frente do `camadas`, a cena girando por
    baixo de uma peça do reel), o furo é desenhado pela perspectiva exata da imagem: 4 sondas nos cantos,
    homografia, meia resolução.
  - A máscara não vai na raiz da peça (apagaria o vidro de dentro): vai na maior subárvore sem vidro ou
    no próprio vidro. Vidro com vidro dentro, ou elemento com máscara própria, não recebe o furo e fica por
    cima da pessoa, com aviso.
- **Na cena.** Com `api.camadaAtras` (o `camadas`), a peça é montada lá dentro e o modo cuida da
  profundidade. Sem ela, a peça entra logo acima da vista do rosto (`api.vistaRosto`, inclusive quando ela
  mora dentro da placa) e abaixo dos cards do modo. Cena sem `vistaRosto` (lista, tipografia...): a peça
  fica por cima, como as outras, com aviso.
- **No reel inteiro (`CENAS.sobre`).** As peças com `atras` vão para o começo da `#camada-sobre`, abaixo
  das outras peças do reel. O furo segue a vista do rosto da cena ativa (a da vez pelo tempo). Fora da
  pessoa, a peça continua por cima dos cards do modo; peça perto de card vai em `cena.sobre`. O motor
  avisa quando a peça cruza: uma cena sem `vistaRosto` (ali ela fica por cima); uma transição (o furo
  segue só a cena ativa e não acompanha a cena que sai, nem o recorte da máscara, da lâmina ou da bolha);
  um movimento de câmera do modo (ali os gates de zona e de contraste não conferem a peça).
- **A régua do texto escondido.** A cada quadro o motor mede quanto da caixa de cada texto da peça a pessoa
  cobre e grava em `layout.jsonl` → `atras` (seção 2.5). Coberto acima de **35% por 0,3 s seguidos**
  (`Motor.ATRAS`) é palavra sumida atrás da cabeça: o motor avisa (`pilha (c1-pilha-1): aviso: "AI" fica
  até 100% atrás da pessoa de 1.47 a 2.83 s (a pessoa sobe até y 335 na coluna dele). Suba a peça…`; no
  `--quadro`, daquele quadro) e o gate de contraste reprova pela mesma régua.
- **O gate de contraste** mede só o que a pessoa não cobre: carrega `visao/mascara/m<quadro+1>.png`, estica
  a máscara sobre a caixa `imagem` que o motor informa e vale só dentro da `janela`. Abaixo de 3% da caixa
  (ou de 30 px) à mostra, não dá para medir e a amostra é pulada. O texto escondido (acima de 35% por 0,3 s
  fora das transições) REPROVA, com o trecho, o texto, o pior `coberto`, o `topo` e a peça. No relatório:
  `atras_de_voce: {medidos_fora_da_pessoa, amostras_sem_letra_a_mostra, limiar_coberto, minimo_s,
  trechos_escondidos}` e `textos_escondidos: [{de, ate, peca, texto, coberto, topo_pessoa, caixa}]`.
- **Regra para o planejador.** A palavra-chave fica acima do cabelo, e só a base da última linha encosta
  na cabeça (uns 10 a 25% da caixa). Antes de fechar, rode um `--quadro` no pior instante e leia
  `atras[].topo` e `coberto` no layout. O zoom de ênfase e o das emendas aumentam a cabeça (no teste, o
  cabelo subiu de y ≈ 400 para 335 com o zoom 1,08 sobre a emenda 1,07): ponha a saída da peça antes do
  zoom, ou use uma linha só. A pilha encolhe só até as sobrancelhas, porque não sabe que está atrás.
- A raiz da peça ganha `data-atras="1"` e `data-peca="<tipo> (<nome>)"`; o `Motor.textosInfo` manda ao
  gate o recorte de cada texto dela (seção 6).

### 3.3 O estilo de produção: `estilo` (3.0)

O criador escolhe, em todo vídeo, um ou mais estilos; o plano diz quais em `"estilo": ["liquid-glass",
"imagens"]` (ou uma string só). A tabela mora em `motor/estilos.json`:

| estilo | o que permite | teto de transições |
|---|---|---|
| `essencial` | rosto-vidro, tipografia, lista, lado-a-lado, painel-rosto, tela-bolha, manchete; `palavra`; lâmina, chicote, zoom-desfoque, desfoque, bolha | 5 por minuto |
| `liquid-glass` | vidro-liquido, rosto-vidro, tipografia, lista; `pilha`, `palavra`, `hud`; inclinada, mergulho, desfoque, lâmina | 8 |
| `imagens` | imagem-cheia, manchete, tela-bolha, rosto-vidro, lado-a-lado, tipografia; `logo-volume`, `palavra`, `pilha`; clarão, máscara, zoom-desfoque, chicote, bolha, desfoque | 8 |
| `tela-cortada` | camadas, rosto-vidro, tipografia; `deteccao`, `maos`, `contorno`, `profundidade`, `logo-volume`, `pilha`, `palavra`; desfoque, inclinada. Pede a pasta `visao/` | 8 |
| `completo` | todos os modos, todas as sobreposições (inclusive os mocks e o HUD) e todas as transições | 8 |
| `motion` | o estilo da 4.0: superconjunto de todos os outros (modos, sobreposições e transições da 3.0 e da 4.0, inclusive `vidro-liquido`, `nuvem`, `malha`, `objeto3d`, `deteccao`, `hud`, `transcricao`, `timeline`). Atende o `estilo_minimo` de qualquer linguagem (`docs-4/variedade-e-som.md`) | 8 |

Com mais de um estilo, vale a união do que eles permitem e o maior teto. Rosto-vidro, tipografia, o corte
seco e a legenda valem em todos. O `compor.py` imprime, antes de renderizar, cada cena, sobreposição ou
transição que está fora do estilo ("aviso de estilo: a cena c5 usa o modo \"vidro-liquido\", que não
está em tela-cortada"), e recusa um nome de estilo que não existe. Fora do estilo é aviso, não erro: a
exceção pode ser de propósito, mas o planejador troca a peça ou assume a exceção com o criador. O gate
de efeitos usa o teto do estilo. Sem a chave `estilo`, nada é conferido e o teto é o do `setup.json`.

---

### 3.4 Tempos presos à palavra: `{"ancora": ...}` (3.0)

Qualquer tempo do plano pode ser escrito como a palavra em que ele acontece, em vez do segundo. Quem
resolve é o `motor/ancoras.py`, chamado pelo `compor.py` e pelos gates antes de qualquer outra coisa, contra o
`palavras-corte.json`. Quando o corte muda de duração, roda de novo e tudo se recalcula.

```json
{ "inicio": { "ancora": "Tudo" } }                         a primeira vez que a fala diz "tudo"
{ "t": { "ancora": "linha cem" } }                          a primeira vez que as duas vêm seguidas
{ "t": { "ancora": "planilha#2", "ajuste": 0 } }            a segunda vez, sem recuo
{ "ancora": "fórmula", "cx": 700, "cy": 820, "zoom": 1.3 }   no objeto: vira o "t" dele
```

- Maiúscula, acento e pontuação não contam: `"Planilha,"` acha `planilha`.
- O recuo padrão: o `inicio` e o `fim` de uma cena caem **2 quadros antes** da palavra (o corte vem antes do
  som); a chave de câmera de um mundo chega **1 quadro antes**; todo o resto, **0,2 s antes** (o movimento
  termina em cima da palavra). `ajuste` troca o recuo.
- A cena sem `fim` termina onde a próxima começa; a última, na `duracao`.
- Âncora que não está na fala recusa o plano, com o nome dela e onde ela estava.
- `python ancoras.py --projeto projetos/<v> --corte NN` (ou `flow-reels produzir/ancoras ...`) mostra o plano
  com os tempos resolvidos, sem renderizar.

## 4. Os modos

Cada modo é um arquivo `web/modos/<nome>.js` que chama `Motor.registrarModo(nome, fn)`. A função
recebe o contexto da cena, cria a cena dentro de `ctx.raiz` e põe as animações em `ctx.tl` nos tempos
absolutos. Coordenadas sempre em pixels de saída (1080 x 1920).

As zonas seguras valem para **texto e logo**: nada de texto acima de y 220, abaixo de y 1440 ou a menos
de 70 px das laterais. Rosto e imagem podem ocupar o quadro todo. Esses valores são uma estimativa
conservadora para Reels orgânico e moram em `setup.json` → `zonas_seguras`; para anúncios, o guia da
Meta pede topo 269, base 1248 e lateral 65.

A legenda segue a altura que o modo pedir (`zonaLegenda.y`), mas **desvia do rosto sozinha**: quando a
posição cruza a caixa do rosto na tela, ela desce para logo abaixo do queixo, ou sobe para acima da
cabeça se não couber antes da zona de baixo. A decisão é tomada uma vez por grupo de palavras, para não
tremer. `zonaLegenda.fixa: true` desliga o desvio (o modo painel-rosto usa a costura).

O que uma função de modo devolve: `{ vistaRosto, zonaLegenda: {y, fixa}, legenda: false, legendaForte,
bolha, bolhaCaixa: {x, y, w, h, raio}, mascaraCentro, mergulhoCentro, camadaAtras }`, todos opcionais.
`bolha` e `bolhaCaixa` são obrigatórios para a cena entrar com `bolha-encolhe` ou sair com
`bolha-expande`.

- `vistaRosto` é a vista que mostra você na cena. É nela que o motor aplica o zoom de ênfase e o das
  emendas, e é ela que as peças da visão seguem (`deteccao`, `maos`, `contorno`, `profundidade`, o
  `logo-volume` com `segue`, o furo do `atras` e o desvio das mãos da legenda). Ela precisa estar visível
  quando a pessoa está na tela: o motor não renderiza vista escondida, e uma vista escondida guardaria o
  quadro de antes.
- `camadaAtras` (3.0, Onda 2): um elemento da cena onde o motor monta as peças com `"atras": true` da
  cena. O modo põe por cima dele a sua vista com `recorte: "pessoa"` e cuida da ordem das camadas. Essa
  vista precisa seguir a vista de fundo quadro a quadro, com os mesmos dois zooms (o motor só aplica os
  zooms na `vistaRosto`), por exemplo `M.aCada(() => { pessoa.zoom.style.transform =
  fundo.zoom.style.transform; pessoa.punch.style.transform = fundo.punch.style.transform; })`. O motor
  mede o texto escondido pela vista "pessoa" visível da mesma cena.
- O rosto que o motor mede (`Motor.rostoNaTela`, a legenda e o gate de rosto) vem da primeira vista
  visível que segue o rosto (`seguirRosto`, nítida, fonte principal), na ordem em que as vistas foram
  criadas. Numa vista girada em 3D, a caixa que envolve a imagem sai errada: o modo que gira o rosto põe
  antes uma vista plana e invisível no lugar do rosto projetado (a "sonda do rosto" do `camadas`).

| modo | `conteudo` | onde vai a legenda |
|---|---|---|
| `painel-rosto` | `{ "blocos": [ ... ], "rosto": {...} }` ou `{ "painel": "painel" }` (nome em `videos`) | na costura, y 956 |
| `rosto-vidro` | `{ "elementos": [ ... ] }` | y 1300, desviando do rosto |
| `tela-bolha` | `{ "tela": {...}, "foco": [...], "marcas": [...], "bolha": {...} }` | logo acima da bolha, fixa |
| `imagem-cheia` | `{ "imagem": "...", "movimento": "aproximar", "rotulo": "..." }` | y 1300, com sombra forte |
| `lado-a-lado` | `{ "esquerda": {...}, "direita": {...}, "vencedor": {...} }` | y 1300, ou logo abaixo dos cards |
| `manchete` | `{ "imagem": "...", "recorte": [...], "fonte": "...", "marcas": [...], "bolha": {...} }` | logo acima da bolha, fixa |
| `lista` | `{ "titulo": "...", "itens": [ ... ] }` | logo abaixo da pilha, até a base |
| `tipografia` | `{ "frase": "...", "destaque": [...], "fundo": "rosto" }` | desligada: a frase é a legenda |
| `vidro-liquido` | `{ "camera": [...], "caixa" \| "imagem", "fundo", "selo" }` | y 1330, desviando do rosto |
| `camadas` | `{ "camera": [...], "rotulos", "metros", "fundo", "inclinacao", "escala", "afastamento", "rosto" }` (precisa do `visao.py`) | y 1340, fixa (logo abaixo das placas separadas; no peito com elas alinhadas). Só o `cena.legenda` muda a altura |
| `mundo` | `{ "mundo": "<nome em CENAS.mundos>", "superficie": "quadro" \| "pip" \| "rosto" \| "tela" }` (seção 4.14) | pela superfície: quadro y 1170, pip y 1165, rosto y 1290, tela y 1370; desvia do rosto |

### 4.1 `painel-rosto`

A tela dividida: o painel em cima (1080 x 956) e o rosto nos 964 px de baixo, seguindo o rosto. A
legenda fica na costura, y 956, sobre um fio do acento. O painel vem de um de dois jeitos.

**Blocos vivos** (`blocos`), o jeito de hoje. O próprio motor monta o painel, com o vidro, a fonte e
o som do resto do reel, e cada entrada vira evento (ritmo e efeito sonoro). Atrás dos blocos,
`fundo: "marca"` (padrão: a superfície com o brilho do acento) ou `"rosto"` (o rosto desfocado).

```json
{ "rosto": { "caixa": [1588, 290, 316, 490] }, "fundo": "marca",
  "blocos": [
    { "tipo": "sigla", "letras": "BUILD", "acesa": 0, "t": 7.45, "acende": 8.35, "tam": 110 },
    { "tipo": "titulo", "texto": "Begin with Plan Mode", "destaque": ["Plan", "Mode"], "acervo": "claude-faisca", "t": 8.85 },
    { "tipo": "teclas", "teclas": ["Shift", "Tab", "Tab"], "aperta": [10.45, 10.75, 11.05], "resultado": "plan mode on", "t": 10.05 },
    { "tipo": "fluxo", "colunas": 4, "itens": [ { "t": 12.2, "icone": "plano", "texto": "plano de execução" },
                                               { "t": 13.62, "acervo": "claude-faisca", "texto": "Claude planeja" } ] } ] }
```

- Todo bloco tem `t` (entra), `ate` (sai por varredura) e `y` (o topo; sem `y`, empilha 28 px abaixo
  do anterior a partir de y 236). A faixa útil vai até y 880; passou disso, o console avisa.
- `sigla`: uma pastilha de vidro por letra. A `acesa` ganha o acento no `acende` e cresce; as de
  antes ficam com o visto, as de depois em tinta suave. É o marcador de capítulo de um acrônimo.
- `titulo`: a manchete centrada, com `destaque` no acento e o logo em cor (`acervo`) à esquerda.
- `teclas`: teclas de vidro ligadas por "+", que afundam e acendem no `aperta` (com o clique), e o
  `resultado` numa pílula acesa ao lado.
- `fluxo`: cards com ícone (`icone`, desenhado pelo motor, ou `acervo`, o logo em cor), um por vez,
  ligados por seta (`setas: false` tira), quebrando em linhas pelas `colunas`; o da vez fica no acento.
  `isolar: t` contorna cada linha nesse instante. Ícones: plano, olho, check, codigo, teste,
  documento, commit, nova, cadeado, grafico, terminal, moedas.
- `rosto.caixa`: numa gravação de tela com a webcam num canto, o enquadre do rosto anda só dentro da
  janela da webcam (pixels da fonte). Uma webcam de 316 px de largura aguenta a ampliação para os 1080
  de baixo.

**Painel em vídeo** (`painel`), o jeito do motor 1.0: um vídeo de 1080 x 956 renderizado pelo
`painel.py`, declarado em `videos`. `tempo: "cena"` (padrão) faz o painel começar no início da cena;
`tempo: "corte"` usa o tempo do corte inteiro. O motor não enxerga dentro do vídeo: os acontecimentos
do painel entram em `marcos: [{t, peso, som}]`, para o gate de ritmo e para os efeitos.

O painel em vídeo de uma cena é um `painel-cN.html` no molde do `componentes/EXEMPLO-PAINEL.html`,
com `window.DURACAO` igual à duração da cena e o tempo zero no início dela, renderizado com
`painel.py --painel painel-cN.html --saida painel-cN.mp4`. O conteúdo começa em y 230: a zona segura
do Reels orgânico é 220, e o `FC.TOPO_UTIL` de 150 das peças é a medida do motor 1.0.

### 4.2 `rosto-vidro`

Rosto em tela cheia, seguindo o rosto (`rosto: {caixa}` limita o enquadre à janela da webcam numa
gravação de tela, como na tela dividida). Cards de vidro entram e saem por cima, a partir do topo da zona
segura. Cada elemento:

```json
{ "id": "n26", "tipo": "numero", "valor": 26, "sufixo": "%", "rotulo": "dos dados não são confiáveis",
  "fonte": "SALESFORCE · 2025", "t": 1.7, "ate": 6.0, "acende": [2.4] }
```

`tipo`: `numero` (conta de 0 até `valor`, respeitando `casas`), `texto` (`titulo` e `corpo`), `selo`
(`texto`, `logo` opcional), `logo` (`marca` do acervo e `nome`), `imagem` (`imagem` e `legenda`
opcional), `adesivo` (abaixo). Mais de um elemento ao mesmo tempo empilha de cima para baixo. `acende` = instantes em que
o elemento recebe o acento.

Os cards são de **vidro escuro**: atrás deles está o vídeo cru (parede, neon, pele), e o vidro claro
saturado pegava a cor do cenário e apagava o texto. `claro: true` volta ao vidro claro, para fundo
escuro e liso. Aceso, o vidro escuro ganha o tingido do acento e o número fica branco. Card de
imagem encolhe para terminar acima da testa (o rosto é medido no `rosto.json` durante o tempo do
card); `cobrirRosto: true` desliga isso.

O **adesivo** é um PNG sem fundo: o logo oficial em cor do `componentes/marcas/` (`acervo`, o nome do
arquivo sem extensão) ou um objeto recortado pelo `componentes/imagens/tirar-fundo.py` (`imagem`).

```json
{ "id": "cc", "tipo": "adesivo", "acervo": "claude-code-logo", "t": 3.2, "ate": 6.0, "largura": 760 }
{ "id": "mega", "tipo": "adesivo", "imagem": "assets/megafone-sem-fundo.png", "t": 1.5, "lugar": "lado" }
```

- `lugar`: `pilha` (na fila dos cards de cima, alinhado com eles; o padrão do logo), `lado` (ao lado
  da cabeça, na altura dos olhos, do lado com mais folga; o padrão do recorte), `esquerda`, `direita`
  ou `[x, y]`. Sem 150 px de folga ao lado da cabeça, ele vai para a pilha.
- `largura`: até 900 na pilha e até 300 ao lado (a folga da cabeça manda).
- `placa`: vidro escuro atrás. Padrão sim para logo do acervo (as marcas pedem fundo calmo, e o n8n
  proíbe sombra no logo) e não para recorte. `sombra`: o contrário da placa.
- O motor nunca inclina, estica nem recolore um adesivo. Ele entra subindo, como os cards.

### 4.3 `tela-bolha`

Uma tela em destaque, numa moldura de vidro na faixa de cima (de y 230 até acima da legenda, 1000 px
de largura, altura pelo aspecto), com o rosto numa bolha de vidro de 400 px embaixo, à esquerda, em
(70, 1150). A legenda fica fixa logo acima da bolha (linha de y 1004 a 1126). O fundo é o rosto
desfocado e escurecido.

```json
{ "tela": { "fonte": "video-principal", "caixa": [448, 0, 978, 615] },
  "foco": [ { "t": 12.0, "caixa": [448, 120, 600, 340] }, { "t": 14.5, "caixa": null } ],
  "marcas": [ { "t": 13.1, "ate": 15.0, "caixa": [520, 200, 300, 60], "tipo": "contorno", "rotulo": "botão corrigido" } ],
  "bolha": { "caixa_rosto": [1561, 288, 329, 520] } }
```

- `tela.fonte`: `video-principal` (uma região do próprio `fala.mp4`, em `caixa`; o padrão), um nome de
  `videos`, ou `imagem` com o caminho em `tela.imagem`. `tela.inicio` = quando o vídeo da tela começa
  (padrão: o início da cena).
- `foco`: `{t, caixa | null, dur 0.8, ate}`. A câmera vai até a caixa (coordenadas da fonte da tela)
  e para; `null` volta para a tela inteira; `ate` volta nesse instante. Nunca amplia mais que 2,2x o
  pixel da fonte.
- `marcas`: `{t, ate, caixa, tipo "contorno" | "seta", rotulo, direcao}`. O traço se desenha no `t` e
  se apaga no `ate`; o rótulo vai numa pílula de vidro escuro, de preferência acima do contorno (ele
  desce para baixo se não couber, e aí cobre a linha de baixo: deixe contexto acima da marca na
  `tela.caixa`). Marca nova com a anterior na tela faz a anterior recuar para tinta suave. A marca
  fica presa à coordenada da fonte: marque conteúdo parado, não rolagem. A pílula do rótulo vai em
  pixel inteiro: em posição fracionária, dentro do vidro com desfoque, o Chromium arredondava o texto
  1 px para cima ou para baixo de uma execução para outra, e o mesmo `--quadro` saía diferente.
- `bolha`: `{caixa_rosto, tamanho 400}`. `caixa_rosto` diz de onde vem o rosto quando a fonte é uma
  gravação com a webcam num canto; sem isso, segue o rosto do `rosto.json`.
- `fundo`: `"rosto"` (padrão), `"tela"` ou `"marca"`.

As peças comuns (bolha com anel, câmera, marcas) ficam em `Motor.pecasBolha`, que a `manchete` usa.

### 4.4 `imagem-cheia`

Foto ou print cobrindo o quadro, com câmera lenta que termina com a cena e nunca passa de 1,08 de
escala. Um degradê escuro embaixo segura a legenda, que ganha sombra mais forte.

```json
{ "imagem": "assets/megafone.jpg", "movimento": "aproximar", "foco": [0.5, 0.4],
  "recorte": [0, 0, 842, 1024], "rotulo": { "texto": "MARKETING", "logo": null, "t": 3.2, "ate": 6.0 },
  "credito": "Foto: rawpixel · CC0" }
```

`movimento`: `aproximar` (padrão), `afastar`, `esquerda`, `direita` (para onde a câmera anda) ou
`parado`. `foco` = o ponto, de 0 a 1, para onde a câmera aproxima. `recorte` = a região da imagem que
vale, em pixels da imagem. `rotulo` = texto ou objeto, numa pílula de vidro escuro no alto. `credito`
= texto pequeno embaixo, quando a licença pede atribuição.

### 4.5 `lado-a-lado`

Dois cards de vidro lado a lado sobre o rosto desfocado e sem cor. Cada lado:

```json
{ "titulo": "ElevenLabs", "sub": "pago, na nuvem", "logo": "elevenlabs", "t": 8.1 }
```

Cada lado mostra no máximo uma peça visual, nesta ordem: `logo` do acervo, `imagem` (com `recorte`
opcional) ou `numero` (com `prefixo`, `sufixo`, `casas`), que conta de 0 até o valor quando o card
entra. `t` = quando o card entra (padrão: a esquerda no início, a direita 0,3 s depois).

O resto do `conteudo`: `vencedor: { "lado": "direita" | "esquerda" | "nenhum", "t": 9.4 }` risca o
perdedor com uma barra no acento e depois acende o vencedor (`nenhum` risca os dois);
`separador`: `"VS"` (padrão), `"×"` ou `""`; `titulo` = a pergunta da comparação numa pílula acima
dos cards, que entra em `titulo_t`; `altura_imagem` = altura das imagens (padrão 300).

### 4.6 `manchete`

O print de uma notícia ou comunicado num card claro (até 956 px de largura), com a `fonte` numa pílula
de vidro logo abaixo e o rosto na mesma bolha da `tela-bolha` (as transições `bolha-*` valem aqui).
O print nunca é escurecido nem distorcido, só muda de escala.

```json
{ "imagem": "assets/salesforce-pagina.png", "recorte": [470, 4560, 1290, 680],
  "fonte": "Salesforce · novembro de 2025",
  "marcas": [ { "t": 5.7, "ate": 7.45, "caixa": [1238, 4878, 122, 54], "tipo": "contorno" },
              { "t": 7.5, "ate": 8.95, "caixa": [570, 4930, 330, 46], "tipo": "sublinhado", "rotulo": "não confiáveis" } ] }
```

`recorte` = a região do print que aparece (pixels da imagem; padrão: a imagem inteira). `marcas` em
pixels da imagem inteira, não do recorte: `contorno`, `sublinhado` ou `seta`, com `rotulo` e `volta`
(true leva a câmera de volta ao print inteiro no `ate`). A câmera sai 0,6 s antes do `t` e chega
parada 0,25 s depois. `zoom_max` (padrão 2,2), `camera: false` desliga a câmera, `bolha` como na
`tela-bolha`. Sem marcas, a câmera faz uma aproximação lenta de 4% que termina com a cena.

### 4.7 `lista`

Itens numerados em cards de vidro sobre o rosto desfocado:

```json
{ "titulo": "5 plugins", "numerar": true,
  "itens": [ { "t": 4.6, "texto": "Playwright CLI", "sub": "testa no navegador", "logo": null, "ate": 6.0 } ] }
```

O item da vez fica aceso; quando o próximo chega (ou em `ate`), o anterior recua para tinta suave e
ganha um visto desenhado. Sem `t`, os itens se espalham pela cena. Até 5 itens visíveis; com mais, a
pilha sobe um degrau por item. `numerar: false` tira o chip do número; `chip` num item troca o número
por outro texto curto (a letra de um acrônimo). Item com `t` antes do início da cena já chega no
lugar, recuado e com o visto, sem som: é assim que uma lista se acumula de uma cena para a outra.

`logo` num item: o svg de `componentes/logos/<logo>.svg` (na tinta, como sempre) e, sem ele, o PNG
colorido do acervo de marcas, `componentes/marcas/<logo>.png` ou `<logo>-icone.png` (`Motor.acervo`),
centrado no quadrado do logo; quando o item recua, o PNG perde a cor e baixa para 55%. O motor procura o
acervo na pré-carga (`Motor.logosAcervo`) e o aviso de `LOGO AUSENTE` diz qual PNG a lista vai usar. Sem
nenhum dos dois, o item fica só com o texto.

### 4.8 `tipografia`

A frase da cena em letra grande, palavra por palavra no tempo da fala, sobre o rosto desfocado e
escurecido (`fundo: "rosto"`) ou sobre a superfície da marca (`fundo: "marca"`). `frase` é opcional:
sem ela, o motor usa as palavras do `palavras-corte.json` dentro da cena. `destaque` = palavras no
acento. A legenda fica desligada nesta cena.

---

### 4.9 `vidro-liquido` (3.0)

O modo Liquid Glass: a cena dentro de uma placa de vidro grossa que inclina, gira e mergulha. A placa
tem aro que refrata (uma cópia 10% maior e desfocada, passando pela mesma lente do vidro dos cards, por
baixo de uma faixa que pega luz), verniz, um reflexo que varre a superfície e espessura de verdade,
feita de 12 fatias empilhadas em 3D, que aparece quando ela gira. Funciona com o rosto, com uma região
da gravação de tela (`caixa`) e com imagem (`fonte: "imagem"`).

```json
{ "selo": { "texto": "AI FIRST × DATA FIRST", "t": 0.5 }, "fundo": "rosto",
  "camera": [ { "t": 0.0, "mov": "entra" }, { "t": 2.6, "mov": "gira" }, { "t": 4.6, "mov": "inclina" },
              { "t": 6.0, "mov": "repouso" }, { "t": 7.4, "mov": "mergulha" } ] }
```

- `camera`: `entra` (chega inclinada, 0,62 s desacelerando), `gira` (mostra a espessura e volta, 1,1 s),
  `inclina` (fica inclinada), `repouso` (volta de frente), `mergulha` (avança até o conteúdo encher o
  quadro e termina um quadro antes do fim da cena; precisa de 0,2 s), `sai` (inclina, recua e desfoca).
  Padrão: só `entra`. Os movimentos não se cruzam e nada vem depois de `mergulha` ou `sai`: o plano que
  pede isso é recusado. Com `entra` primeiro, a placa já espera na pose de entrada, então uma transição
  que mostra a cena antes do início (desfoque, chicote, máscara) mostra a placa inclinada.
- No `mergulha`, a emenda escondida para de trocar a escala do conteúdo e a face da frente volta para o
  plano da placa: o último quadro é o enquadre da tela cheia. Não ponha zoom de ênfase que ainda esteja
  ativo durante o mergulho.
- No rosto, o conteúdo tem o aspecto do quadro (9:16): o fim do `mergulha` é o mesmo enquadre da cena
  de tela cheia seguinte (`rosto-vidro`), e a troca por corte seco não pula.
- `placa`: `{x, y, w, h, raio, aro, espessura}` muda o retângulo de repouso (padrão: 800 de largura no
  rosto, 900 no resto, altura pelo aspecto, até 1400). `rosto.caixa` limita o enquadre à janela da
  webcam. `fundo`: `"rosto"` (o vídeo desfocado) ou `"marca"`. `brilho`: instantes do reflexo (padrão:
  no fim da entrada). `respira: false` desliga a deriva lenta (de 0 a 2,5°) nos trechos parados.
  `selo: {texto, t, ate, lugar}`: `"acima"` da placa ou `"dentro"` dela (o lugar num reel com HUD); sem
  `ate`, ele some junto com o vidro no `mergulha`.
- Devolve a vista do rosto (zoom de ênfase e emendas valem), `mascaraCentro` e `mergulhoCentro`.

### 4.10 As sobreposições: `cena.sobre` e `CENAS.sobre` (3.0)

Peças que entram por cima de qualquer modo. Na cena, vivem e andam com ela; no reel, ficam na
`#camada-sobre` (acima das cenas, abaixo da legenda) e não andam com as transições. O contrato inteiro
de cada uma está em `SOBREPOSICOES.md`.

```json
"sobre": [ { "tipo": "hud", "capitulos": [ { "t": 0.3, "texto": "01 · O ALERTA" } ], "fim": { "t": 34.6 } } ],
"cenas": [ { "id": "c2", "modo": "rosto-vidro", "conteudo": { "elementos": [] },
             "sobre": [ { "tipo": "palavra", "efeito": "conta", "valor": 26, "sufixo": "%", "t": 4.96, "ate": 7.3, "y": 430 },
                        { "tipo": "logo-volume", "acervo": "salesforce-icone", "t": 3.24, "ate": 4.75, "x": 250, "y": 430 } ] } ]
```

| tipo | o que é |
|---|---|
| `pilha` | manchete em pilha no topo: rótulo mono, linhas palavra a palavra no tempo da fala, `*destaque*` no gradiente, `risco` e `colchetes` de visor; uma manchete por vez |
| `palavra` | a palavra que vira o que diz: `glitch`, `digitacao`, `extrusao`, `pula`, `conta` (com uma névoa escura que segura o contraste) |
| `hud` | o HUD de capítulos: timecode correndo, pílula do capítulo (chip com o número ou a letra), "EDIÇÃO CONCLUÍDA" no fim |
| `transcricao` | a fita da fala com o tempo de cada palavra e a da vez em destaque |
| `prompt` | a caixa de pedido com arquivo anexado e o texto sendo digitado |
| `timeline` | a timeline do editor com miniaturas do próprio vídeo, as palavras e os clipes |
| `comentario` | o comentário com a palavra do CTA sendo digitada e o avião de papel |
| `dm` | a notificação de DM com a sua foto, no fim do CTA |
| `logo-volume` | o logo oficial numa placa de app com volume, pop com faíscas e deriva; com `segue` (3.0, Onda 2), presa à mão (palma ou ponta do indicador) ou à cabeça, com o pedestal holográfico que só acende sobre a palma |
| `deteccao` | (Onda 2) um feixe varre o quadro e a mira de cantos de visor trava no rosto, nas mãos e nos objetos (e no corpo, quando pedido), com a pílula da confiança medida ("ROSTO 0,96"); no alto, o estado e o contador "OBJETOS NN" |
| `maos` | (Onda 2) o esqueleto da mão (os 21 pontos do MediaPipe) crescendo do pulso para as pontas, com o cartão "MÃO 01 · 0,97 / 21 PONTOS / X Y" |
| `contorno` | (Onda 2) o traço em volta da pessoa, revelado de cima a baixo, as pílulas "CAMADA 01 · VOCÊ" e "CAMADA 02 · FUNDO" e o cenário tingido pelo gradiente |
| `profundidade` | (Onda 2) o vídeo vira um mapa de cor falsa que se espalha em onda, do mais perto até a parede, com a régua PERTO/LONGE ao lado da cabeça |

As peças da Onda 2 (`deteccao`, `maos`, `contorno`, `profundidade` e o `logo-volume` com `segue`)
precisam da visão do corte (`visao.py`, seção 2.6), e o alvo "rosto" da `deteccao` e o `segue: "cabeca"`
precisam também do `rosto.json`. Elas desenham presas à vista do rosto da cena (`api.vistaRosto`). O modo
que combina é o `rosto-vidro`, ou o `vidro-liquido` de frente; no `camadas`, elas seguem você na placa
da frente; no `painel-rosto` cabe pouco. Numa cena sem rosto, a `deteccao`, as `maos` e o `contorno` são
recusados com Error, e a `profundidade` e o `segue` ficam de fora (ou parados) com aviso. Toda peça aceita
`"atras": true` (seção 3.3).

Regras de convívio que valem para o plano:

- **Com HUD, o conteúdo do topo começa em y 320**: o HUD ocupa de y 236 a ~291.
- **Uma manchete (`pilha`) por vez**, e duas `palavra` no mesmo `y` com 0,2 s entre o `ate` de uma e
  o `t` da outra.
- **No CTA com rosto grande**, a cena leva `"legenda": {"posicao": "topo"}`, e o `comentario` e a `dm`
  ficam embaixo; entre o `ate` do comentário e o `t` da DM, 0,4 s.
- **Texto no acento abaixo de 48 px precisa de 4,5:1**: uma pilha que encolhe demais (quatro linhas) reprova.
  Prefira duas pilhas de duas linhas.
- As peças conferem o próprio lugar (zona segura, rosto, legenda, outros textos) e avisam no console,
  que o `compor.py` repete no fim do render inteiro, em "avisos do motor". O `--quadro` não mostra.
- **Cards e selos no alto durante os gestos** (com a legenda desviando das mãos, seção 3.2): enquanto a
  pessoa gesticula, o alto é o lugar da legenda. No `rosto-vidro`, card e selo entram no alto e tiram esse
  lugar: a linha fica no peito, por cima da mão, e entra no aviso. Ponha selo e card de texto nos trechos
  de mãos quietas; nos gestos, use o adesivo ao lado da cabeça (`"lugar": "lado"`).
- **Cabeça alta:** o zoom de ênfase e a pessoa inclinada para a câmera sobem a cabeça. Com o cabelo acima
  de y ~350, não cabe linha acima dele. Evite o zoom de ênfase nos trechos de gesto.
- **Conferir:** antes de fechar o plano, rode o `--quadro` nos gestos e leia o aviso `legenda (reel)`. Se
  não der para liberar o alto, use `"desvia_maos": false` na cena.
- **Peças da visão juntas:** uma `profundidade` por vez na mesma cena; com `deteccao` (linha do alto) ou
  `maos`, a legenda quer o alto (SOBREPOSICOES.md, regras de cada uma).

### 4.11 `camadas` (3.0, Onda 2)

A tela cortada em 3D. A cena começa no rosto em tela cheia, com o mesmo enquadre do `rosto-vidro`, e se
parte em camadas de profundidade:
- **na frente:** você recortado (a vista com `recorte: "pessoa"`), sobre um vidro claro;
- **atrás:** o cenário sem você (o `fundo-limpo.jpg` do `visao.py`), um pouco fora de foco;
- **no meio:** o que o plano põe com `"atras": true` em `cena.sobre` desta cena.

Quando as placas voltam a se alinhar, a peça do meio fica entre você e o fundo, e a cabeça passa por cima
da palavra. Precisa da visão do corte: a máscara e o fundo limpo. Sem elas, o motor recusa a cena com o
Error padrão, que diz o que rodar.

```json
{ "id": "c6", "modo": "camadas", "inicio": 22.45, "fim": 27.3, "entrada": { "transicao": "desfoque" },
  "conteudo": { "fundo": "marca",
    "camera": [ { "t": 22.6, "mov": "separa" }, { "t": 24.4, "mov": "gira" }, { "t": 25.95, "mov": "volta" } ] },
  "sobre": [ { "tipo": "palavra", "efeito": "extrusao", "texto": "MUSEU", "t": 22.9, "ate": 24.1,
               "y": 310, "tam": 190, "atras": true } ] }
```

**`camera`: `[ { t, mov, dur } ]`**
- **`separa` (0,85 s).** O quadro vira uma placa de vidro, com aro que pega luz, o fio do gradiente da
  marca e espessura (quatro paredes finas por placa). Inclina e encolhe saindo do repouso e assentando
  (power2.inOut, em 65% do tempo): os primeiros quadros quase não se mexem, como na referência. A partir
  de um quarto do tempo as placas se afastam em profundidade, até o fim do movimento.
- **`gira` (1,2 s).** A câmera passa para o outro lado das placas: o `ry` é espelhado e a pessoa troca de
  lado na tela.
- **`volta` (0,9 s).** Devagar-rápido-devagar até o quadro cheio. As placas se juntam em 60% do tempo; o
  vidro some até 70%, antes de a placa encostar na beira; o fundo troca da placa limpa para o vídeo vivo
  aos 66%, com as placas já no mesmo plano, para a pessoa não aparecer duas vezes.
- **Deriva.** Com as placas paradas por 0,8 s ou mais, a câmera continua andando: uma deriva só, de 2,5° no
  sentido do giro e 2% mais perto, do fim de um movimento ao começo do seguinte (ou ao fim da cena). Nunca
  é laço; o movimento seguinte parte dela.
- **Padrão:** separa em `inicio + 0,2` e volta 2 s depois. Se a volta não cabe antes do fim, as placas
  ficam separadas até o fim, com aviso.
- **Regras do plano** (quem viola é recusado com Error): `t` é um número em segundos; `separa` só parte do
  quadro cheio; `gira` e `volta` só partem das placas separadas; um movimento não começa antes do fim do
  anterior nem antes da cena; cada um dura pelo menos 0,3 s e termina dentro da cena.
- **Como a cena pode terminar:** separada até o fim (a próxima entra por corte ou transição; o
  `mergulho` vai no rosto da placa da frente), ou separando e voltando, quantas vezes quiser.
- **Janelas.** Cada movimento é uma janela (`Motor.janela`), com evento `camera` de peso 2 e `whoosh`: ali
  os gates de zona, rosto e contraste não contam o quadro.

| campo | padrão | o que faz |
|---|---|---|
| `rotulos` | `true` | As pílulas "01 CAMADA · VOCÊ" e "02 CAMADA · FUNDO" no alto das placas (FC Mono 24 px sobre vidro escuro, o número num anel do gradiente) e uma linha tracejada no gradiente que atravessa o vão, da borda de dentro da placa da frente à de trás. Tudo entra quando as placas param e sai antes do próximo movimento; trecho parado com menos de 0,9 s fica sem nada disso. `false` tira; `{ "voce": "...", "fundo": "..." }` troca os nomes. |
| `metros` | `null` | `{ "voce": 0.8, "fundo": 3.4 }`: a distância de cada camada até a câmera, **medida por quem gravou**, com `fundo > voce > 0` (senão, aviso e a cena fica sem metros). As pílulas mostram "0,8 m" e "3,4 m", e a pílula DISTÂNCIA conta até a diferença. Sem `metros`, nenhum metro na tela e nenhuma pílula DISTÂNCIA, porque a profundidade do `visao.py` é relativa. As pílulas dizem PERTO e LONGE só quando a mediana de `pessoa − fundo` em `visao.json` → `profundidade`, nos quadros da cena, passa de 25 na régua de 0 a 255; senão, avisa e fica sem. |
| `fundo` | `"marca"` | O que aparece em volta das placas separadas. `"marca"`: a superfície, a luz do gradiente e um chão em grade. `"rosto"`: o vídeo desfocado e escurecido. |
| `inclinacao` | `[-6, -54]` | `[rx, ry]` em graus: câmera um pouco acima, olhando de lado, você à esquerda e o fundo à direita. `ry` positivo põe você à direita. Abaixo de 15° de `ry`, avisa: as placas ficam uma atrás da outra e o vão some. |
| `escala` | 0,46 | O tamanho das placas separadas (de 0,3 a 0,8). Acima do padrão, a placa da frente encosta na legenda em y 1340. |
| `afastamento` | 780 | A distância de cada placa até o plano do meio, em px do quadro (de 150 a 1200). |
| `rosto` | — | `{ "caixa": [x, y, w, h] }`: a janela da webcam numa gravação de tela, como no `rosto-vidro`. |

**A linha da distância desvia das peças do meio.** A altura dela no plano é escolhida a cada trecho
parado, entre embaixo (80% da altura), no meio (50%) e no alto (24%): vale a primeira longe das peças do
meio daquele trecho, pelo `y` e o `tam` delas no plano (`palavra`: centro ± 0,8 tam; `logo-volume`:
centro ± 0,7 tam; `pilha`: do topo até as linhas; outra peça conta do `y` até embaixo). Se ainda encostar,
o console avisa. As pílulas conferem quadro a quadro se encostam em texto de outra peça (as do meio, as
outras da cena e as do reel inteiro, como um HUD) e avisam uma vez por peça e trecho.

**O fundo inventado recua.** O pedaço que o `visao.py` inventou onde você estava (`fundo-buraco.png`,
quase metade do fundo no teste) fica mais desfocado e numa sombra larga e macia na placa de trás, como
parede fora de foco na sombra da placa da frente. A emenda com o fundo de verdade não desenha a silhueta.
Mesmo assim, de perto ele é uma continuação, não o cenário (seção 2.6): gravar o cenário vazio resolve.

**O que o modo devolve**
- `vistaRosto` (e `vistaPessoa`): você recortado, na placa da frente, a vista que mostra você na cena
  inteira. Com as placas alinhadas ela cobre o vídeo vivo pixel a pixel; separadas, é você na placa. O zoom
  de ênfase e o das emendas valem nela; o vivo, o fundo limpo e a sonda do rosto copiam os dois a cada
  quadro. As peças da visão seguem esta vista, então continuam presas a você com as placas separadas.
- `vistaVivo`: o vídeo vivo, na placa de trás (aparece com as placas alinhadas e no fim da volta).
  `vistaFundo`: o fundo limpo, na placa de trás (aparece com as placas separadas).
- As três vistas trazem `plano3d`, a placa em que moram: `plano3d.el` (a face da placa, onde a vista mora
  em (0, 0) com 1080 x 1920), `plano3d.separadas(t)` (o 3D está ligado em `t`), `plano3d.paraCena(t, x, y)`
  (um ponto da placa levado para a cena com a perspectiva exata, refeita só do tempo: vale num seek sem
  ganchos e voltando no tempo) e `plano3d.escala(t, x, y)` (quantos px da cena vale 1 px da placa ali).
  O caminho de um ponto da fonte: da fonte até a placa pela conta 2D de sempre, e da placa até a cena pelo
  `paraCena`. O que é desenhado dentro da vista (o mapa da profundidade, o traço do contorno) já gira com a
  placa sem conta nenhuma.
- `camadaAtras`: o plano do meio, 1080 x 1920, com a mesma transformação das placas.
- `zonaLegenda`: `{ "y": 1340, "fixa": true }`. `mascaraCentro`: `"50% 42%"`. `mergulhoCentro`: os olhos de
  quem fala; se a cena termina separada, o rosto na placa da frente, na pose do fim.

**O rosto medido.** Com as placas separadas, o rosto que o motor mede (`Motor.rostoNaTela`, a legenda e o
gate 4) vem da **sonda do rosto**: uma vista invisível (`clip-path: inset(50%)`), plana, criada antes do
vídeo vivo, que segue o rosto e é posta pela linha do tempo, em trechos de 0,1 s, onde o rosto da placa da
frente aparece (a mesma conta do navegador, em DOMMatrix, com as mesmas curvas dos movimentos). Vai na
linha do tempo, e não num gancho, porque a legenda mede outros instantes voltando no tempo sem rodar
ganchos.

**Regras para o planejador**
- **A peça do meio confere o próprio lugar no plano dela,** que só é a tela com as placas alinhadas. Com
  as placas separadas, ela aparece encolhida e de lado, no vão: com a pose padrão, uma palavra de até uns
  800 px no plano cabe. Texto parado em cima da placa de trás reprova no contraste.
- **Névoa e sombra.** Com as placas separadas, a névoa da `palavra` e a sombra da `pilha` somem e voltam na
  segunda metade da volta (viravam uma laje preta entre as placas).
- **Separe pop e whoosh:** 0,25 s entre o `separa` e o pop de uma peça. Com menos, o `audio.py` descarta o
  pop.
- **O `logo-volume` no meio não sabe que está atrás.** Dê `ate` a ele antes do `gira`, com 0,2 s de folga
  para a saída.
- **Peça com `atras` no reel inteiro (`CENAS.sobre`) não entra entre as placas:** fica na camada do reel,
  plana na tela; o furo dela segue você na placa da frente, mas ela passa por cima da placa do fundo, do vão
  e do vidro, e não gira (o modo avisa). A peça do meio vai em `cena.sobre`.
- **As peças da visão aqui:** seguem você na placa da frente (SOBREPOSICOES.md). A `profundidade` pinta só
  você com as placas separadas (a placa de trás é uma foto montada, sem profundidade medida) e avisa; a
  linha do alto da `deteccao` e as pílulas VOCÊ e FUNDO do `contorno` saem da frente com as placas
  separadas, porque o alto é das pílulas das camadas.
- **Zoom de ênfase depois da volta sobe a cabeça.** No teste, 1,08 levou a cobertura de "DECISÃO" de 15%
  para 31%, perto do limite de 35%.
- **Legenda.** A zona é fixa: o `posicao` do reel não vale e o desvio das mãos não roda nesta cena. A cena
  que precisa de outra altura pede no `cena.legenda`.
- **`metros`** só com medida de quem gravou. O valor de exemplo nunca vai para reel publicado.

**Determinismo.** Cada movimento e a deriva são um `fromTo` com a pose de partida escrita; a sonda anda por
`fromTo` lineares calculados ao montar; a visibilidade vai só em sets e a opacidade só nos tweens; o 3D
(`preserve-3d`) só liga com as placas separadas; cada trecho parado tem o seu conjunto de pílulas. Medido:
render em ordem embaralhada numa página só contra página nova, idênticos, num plano com separa, volta,
separa, gira e volta.

### 4.12 O 3D de verdade: `nuvem`, `malha` e `objeto3d` (3.0, Onda 3)

Três sobreposições em WebGL, com o three.js (MIT, `componentes/vendor/three/`) e o opentype.js (MIT,
`componentes/vendor/opentype/`) para o texto 3D na fonte da marca. Quando o plano usa uma delas, o
`compor.py` liga a GPU do Chromium (Metal, no Mac: `--use-angle=metal`); os reels sem 3D seguem no
caminho de sempre e saem iguais aos já entregues. Medido no M4: ~60 ms por quadro com 3D (a GPU acelera
o resto também). Cada peça tem o próprio `<canvas>` e redesenha a partir do `t`, do zero, a cada quadro.

O cenário em 3D vem da visão do corte: `fundo-limpo.jpg` e `fundo-profundidade.png` (a profundidade do
fundo, gravada pelo `visao.py` desde a versão 4 do fundo; rode `visao.py --so fundo --refazer` num corte
antigo). Cada pixel vira um ponto no raio da câmera, na distância da profundidade dele: com a câmera em
casa, o 3D reproduz exatamente o enquadre da cena (vista do rosto, zoom e emendas); quando a câmera dá a
volta, a prateleira e o letreiro saem da parede.

| peça | campos | o que faz |
|---|---|---|
| `nuvem` | `t`, `ate`, `cor` (`"marca"` ou `"real"`), `densidade` (1), `orbita` ([14, -4] graus), `rotulo`, `y` | o cenário vira nuvem de pontos (~150 mil): entra montando do perto para o longe (0,9 s), a câmera faz uma ida e volta e ela sai desmontando com o vídeo reaparecendo. Pílula "NUVEM DE PONTOS" com a contagem real |
| `malha` | `t`, `ate`, `colunas` (64), `orbita`, `rotulo`, `y` | o cenário vira malha 3D em linhas e vértices, com a cor do gradiente da marca pela profundidade, revelada de cima para baixo por uma frente de luz. Pílula "MALHA 3D · VÉRTICES" com a contagem real |
| `objeto3d` | `t`, `ate`, `forma` (`cubo`, `esfera`, `anel`, `texto`, `logo`), `texto`, `acervo`, `x`, `y`, `tam` (altura na tela, px), `giro` (40°), `material` (`"marca"` ou `"vidro"`) | objeto iluminado (luz branca, contorno no acento, preenchimento ciano) que entra girando com leve passada, gira devagar e sai encolhendo. `texto` é extrudado na fonte de título com o gradiente da marca na face; `logo` é o logo em cor numa placa com espessura. Reserva o lugar dele na tela (`data-zona`), e a legenda desvia |

- **`"atras": true`** em todas: a pessoa fica na frente (nuvem e malha cobrem o quadro). Sem isso, o
  console avisa. Dentro de uma cena `camadas`, o `objeto3d` com `atras` vai para o vão entre você e o
  fundo.
- A palavra grande atrás da cabeça (`palavra` com `atras`) fica entre y 280 e 320, com `tam` de 120 a
  170: mais baixo, a cabeça esconde a palavra e o gate de contraste reprova ("texto atrás de você
  escondido pela pessoa").
- Pílulas de contagem ficam no alto à esquerda (`y` 240 ou mais); a peça de digitação (`palavra`
  `digitacao`) tem caixa larga e encosta nelas: use `pula` ou `glitch` na mesma faixa.

### 4.13 A 4.0: looks, mãos, frames 3D, estética, transições e linguagens

A 4.0 acrescenta seis famílias de peças. Cada uma tem o contrato completo num arquivo de `docs-4/`, no
mesmo formato desta seção; aqui fica o mapa. Os nomes são contrato entre o plano e o motor. Nenhuma
dependência nova: todo shader e efeito foi escrito para o pacote (sem LYGIA, Shadertoy nem Book of
Shaders, que não permitem uso comercial). Tudo é determinístico: `fx/comum.js` dá hash, semente,
gerador e ruído (`M.fx`), e nenhuma peça usa `Math.random`, `Date` nem estado entre quadros.

| família | arquivo | peças | doc |
|---|---|---|---|
| Looks no vídeo (shader na imagem da vista, com a máscara: `alvo` `fundo`, `pessoa` ou `tudo`) | `web/sobre/look.js` | `look` com `efeito`: pontilhado, reticula, crt, vhs, pixel, duotone, termico, holograma, grao, ascii, risografia, noir, esboco, posterizar | `docs-4/looks.md` |
| Mãos e corpo (gatilho pelos gestos do `gestos.py`) | `scripts/gestos.py`, `web/sobre/maos-fx.js` | faiscas, rastro, contar, energia, tela-maos, feixe, onda, eco, sombra, raio, aura | `docs-4/maos-corpo.md` |
| Frames 3D | `web/modos/frames3d.js`, `web/sobre/frames3d.js` | modos celular3d, parallax, telas; sobreposições dolly, moldura-pop, polaroid, foco | `docs-4/frames-3d.md` |
| Transições e palavras | `web/transicoes-4.js`, `web/sobre/palavra.js` | transições glitch, vhs, queima, pixels, persianas, cubo, forma, tinta, zoom-atraves; palavra decodifica, brutal, marcatexto, neon, carimbo, cromado, vazado, pixel | `docs-4/transicoes-e-palavras.md` |
| Estética (linguagens visuais) | `web/sobre/estetica.js` | moldura-crt, grade-synthwave, linhas-foco, mira, diagrama, chuva, luz, poeira, recorte, papel, barras | `docs-4/estetica.md` |
| Pós no quadro inteiro (segunda passada: a cena inteira, com cards, palavras e 3D, passa pelo shader; a legenda e a camada de transição ficam por cima, nítidas) | `web/pos.js`, `compor.py` | `pos` (topo ou cena) com `efeito`: crt, vhs, glitch, aberracao, bloom, grao, pontilhado, reticula, pixel, onda, vinheta, lente, ascii; `acabamento` no topo (`lut`, `grao`, `vinheta`, no ffmpeg; LUTs em `componentes/luts/`) | `docs-4/pos.md` |
| Rosto e expressão (gatilho por piscada, boca, sorriso, sobrancelha, cabeça) | `scripts/expressao.py`, `web/sobre/rosto-fx.js` | brilho-olhar, laser, piscada, fala-onda, emoji-reacao, mascara-tech, zoom-reacao | `docs-4/rosto-expressao.md` |
| Variedade e som | `motor/linguagens.json`, `scripts/linguagem.py`, `scripts/gerar_sons.py`, `scripts/audio.py` | 12 linguagens do episódio, 15 famílias de som com variações | `docs-4/variedade-e-som.md` |

**GPU.** O que usa WebGL está em `motor/gpu.json` (hoje: `look`, `energia`, `dolly`, `foco` e os modos
`celular3d`, `parallax`, `telas`); o `compor.py` liga o Metal quando o plano usa um desses nomes, e
`"gpu": true` no topo do `cenas.json` liga sempre. Medido no M4: 60 a 90 ms por quadro nas demos.

**Gestos.** Depois do `visao.py`, rode `scripts/gestos.py --projeto projetos/<v> --corte NN` (cerca de
1 s): ele grava `visao/gestos.json` (gesto estável por mão e por quadro, e os eventos `palmas`, `abre`,
`varrida`, `aponta-inicio`, `aponta-fim`, `conta`, `enfase`), que o `compor.py` entrega em
`VISAO.gestos`. `--resumo` lista os momentos úteis com a palavra dita em cada um, para escolher gatilhos.

**Expressão.** `scripts/expressao.py --projeto projetos/<v> --corte NN` (MediaPipe Face Landmarker,
Apache-2.0, `componentes/modelos/face_landmarker.task`; 8 a 19 ms por quadro) grava `visao/expressao.json`
(blendshapes resumidos, pose da cabeça, pontos do rosto e os eventos `piscada`, `boca-aberta`, `sorriso`,
`sobrancelha`, `cabeca-vira`, `aceno`), que o `compor.py` entrega em `VISAO.expressao`. Lados sempre de
quem assiste. `--resumo` lista os momentos com a palavra dita.

**Pós e acabamento.** `"pos": [{"efeito", "t", "ate", "forca", "entra", "sai", "semente"}]` no topo (o reel)
ou numa cena (preso a ela) e `"acabamento": {"lut": "neutra-quente|fria-tech|filme|noir", "grao": 0..1,
"vinheta": 0..1}` no topo. Com pos, o `compor.py` esconde legenda e transição, fotografa a página (JPEG 95),
passa o quadro pelos shaders em `#camada-pos` (z 18, API `Motor.Pos`) e devolve a legenda por cima; liga a
GPU sozinho. Custo ~41 ms a mais por quadro com pos. O gate de contraste mede o quadro final (o quadro sem
texto passa pelo mesmo pós; `contraste.jsonl` ganha `cor_css` e `cor_medida`). Reel sem `pos` nem
`acabamento` sai pixel a pixel igual. Cuidados: padrão fino (crt, pontilhado, retícula, ascii, pixel) sobre
texto pequeno fica ilegível mesmo passando no contraste; ruído a cada quadro pesa no arquivo (grão do
acabamento de 0,15 a 0,3). Cada linguagem diz quais efeitos de pos aceita (`linguagens.json` →
`pecas.pos`; grão e vinheta valem em todas) e sugere um acabamento; o `linguagem.py conferir` e o gate 11
reprovam pos fora da linguagem.

**Gates e som (4.3).** O `conferir_reel.py` tem 12 gates: 10 · som (reprova efeito a menos de 0,75 s do
anterior, 4 ou mais juntos, o mesmo arquivo seguido, efeito na sílaba tônica de palavra destacada com a voz
a menos de 6 dB acima, pico acima de -1 dBTP; densidade acima de um a cada 1,5 s vira "olhe"), 11 ·
linguagem (a mesma conferência do `linguagem.py`, N/A sem `"linguagem"`) e 12 · variedade (só aviso:
transição repetida, cenas com a mesma duração, metrônomo, repetição dos últimos reels). O `audio.py` estima a
tônica em pt-BR por regra e adianta o som até 80 ms (ou o baixa 6 dB) quando ele cairia sobre a vogal
tônica da palavra destacada, e grava `sons.json` (o que tocou, quando e em que volume). Contrato em
`docs-4/gates-4-3.md`.

**Chaves novas do `cenas.json`.** `"linguagem": "<nome>"` (ou `{"base": ..., "convidada": ...}`) e
`"heroi": {"t": s, "nome": "<peça>"}`: o `compor.py` ignora as duas, e o `linguagem.py conferir` lê.
`"gpu": true` liga a GPU.

**Cuidados aprendidos nas demos.**
- Palavra no acento sobre look que deixa o fundo na cor do acento (pontilhado, retícula, risografia, duotone) reprova no
  contraste: use letra branca, névoa ou o look em `cor: "ciano"`.
- Numa peça com `"atras": true`, `clip-path` em elemento interno apaga o furo da pessoa; e
  `mix-blend-mode` dentro de elemento transformado não enxerga a cena. Contorne dentro da peça.
- Uma demo com todas as transições passa do teto de efeitos (8 por minuto): num reel de verdade, a
  linguagem limita a no máximo 3 famílias de transição.
- O `--de/--ate` deixa `previa-trecho.mp4` na pasta de trabalho do corte.

### 4.14 `mundo` (3.0): a coisa ocupa a tela, a câmera passeia, o rosto é respiro

Veio do layout motion do pacote original (0.2.0), reescrito para o motor. Uma frase para guardar: **a coisa
de que se fala ocupa a tela, e o rosto entra como respiro.** Se a fala não aponta para coisa nenhuma, o mundo
vira slideshow, e o trecho é de outro modo.

| | serve | o teste |
|---|---|---|
| `mundo` | tutorial, "faz exatamente isso", tudo que melhora mostrando o objeto real: um arquivo, uma janela, uma planilha, um gráfico | a fala aponta o tempo todo: "essa linha", "esse arquivo", "digita isso" |
| os outros modos | opinião, história, provocação, lista | a fala não aponta para nada concreto |

#### 4.14.1 O plano: um mundo, várias cenas

O mundo é declarado uma vez, em `CENAS.mundos`, e cada trecho é uma cena `mundo` com a sua superfície. Cenas
seguidas do mesmo mundo trocam de superfície **por dentro** (sem transição do motor: deixe `entrada` vazia ou
`corte`), e a câmera é uma só, função do tempo, contínua de uma cena para a outra. A legenda muda de altura
em cada superfície porque cada superfície é uma cena.

```json
"mundos": {
  "terminal": {
    "fonte": { "html": "mundo.html" },
    "tamanho": [1080, 1350],
    "camera": "calma",
    "chaves": [ { "t": 0, "cx": 540, "cy": 480, "zoom": 1.0 },
                { "ancora": "comandos", "cx": 540, "cy": 610, "zoom": 1.12 },
                { "ancora": "revisão", "cx": 648, "cy": 900, "zoom": 1.25 } ],
    "beats": [ { "nome": "comandos", "ancora": "comandos", "peso": 2 } ],
    "rosto": { "caixa": null, "recorte": true },
    "logo": true
  }
},
"cenas": [
  { "id": "c1", "modo": "mundo", "inicio": 0, "conteudo": { "mundo": "terminal", "superficie": "quadro" } },
  { "id": "c2", "modo": "mundo", "inicio": { "ancora": "Tudo" }, "conteudo": { "mundo": "terminal", "superficie": "tela" } },
  { "id": "c3", "modo": "mundo", "inicio": { "ancora": "Ou até" }, "conteudo": { "mundo": "terminal", "superficie": "rosto" } }
]
```

- `fonte`: `{ "html": "mundo.html" }` (uma página da pasta do corte, abaixo), `{ "imagem": "assets/print.png" }`
  (um print de verdade; o tamanho sai da imagem), `{ "video": "principal", "caixa": [x, y, w, h] }` (a região
  da gravação de tela, em pixels da fonte; o tamanho é a caixa) ou `{ "video": "<nome em CENAS.videos>" }`.
- `tamanho`: obrigatório no html, o mesmo do `window.MUNDO` da página. Recomendado 1080 x 1350: enche o card do
  quadro com folga, e a câmera escolhe o pedaço na tela cheia.
- `chaves`: `{ t | ancora, cx, cy, zoom, mover, chicote }`. `(cx, cy)` são pixels do mundo e caem no centro da
  vista; com `zoom: 1`, a largura do mundo enche a largura da vista. `mover` (padrão 1,1 s) é quanto tempo a
  câmera leva até a chave. Sem chave, a vista mostra o mundo inteiro na largura, alinhado em cima.
- `beats`: o que entra no mundo, com nome e tempo (ou âncora). Viram eventos (o gate de ritmo e os sons) e a
  página lê os tempos já resolvidos (`Mundo.beat("nome")`). É assim que o mundo e a fala nunca discordam.
- `rosto.caixa`: a janela da webcam numa gravação de tela (pixels da fonte). `rosto.recorte: false` desliga a
  cabeça saindo do card (encarte pequeno: a máscara oscila).
- `logo`: o logo da marca salta no canto do card, em 132 px, na primeira vez que o quadro aparece (`false`
  desliga; um caminho troca o arquivo).

#### 4.14.2 As superfícies

| superfície | o que é | geometria (1080 x 1920) | legenda |
|---|---|---|---|
| `quadro` | o mundo num card em cima, o rosto num card embaixo com a cabeça saindo pela borda | mundo 960 x 853 em (60, 236), cantos 26; rosto de x 100 a 980, do y 1384 até a base, cabeça 120 px acima | y 1170, entre os cards |
| `pip` | o mundo grande; embaixo um card baixo que começa no queixo, com a cabeça recortada por cima | mundo 960 x 950 em (60, 150); rosto centrado na base, 300 de altura, até 620 de largura (estreita até a cabeça caber nos 420 px de folga) | y 1165 |
| `rosto` | um card grande do rosto, para as frases que são a pessoa, não a coisa | 900 x 1000 em (90, 400), cantos 44, cabeça 130 px acima; o rosto empurra 5% devagar | y 1290 |
| `tela` | o mundo em tela cheia, quando o objeto precisa da tela inteira | a tela; de y 1330 a 1440 o mundo se funde na superfície da marca, abaixo é fundo liso | y 1370 |

O fundo é papel em `cores.quadro` do `tokens.json` (opcional; sem ela, `superficie_alt`), com quadriculado a
cada 54 px em `tinta` a 6% e uma vinheta leve. Os cards levam contorno de 2 px em `tinta_suave` a 50%, sem
sombra. **O rosto nunca passa de 1,12x a gravação**: a janela do rosto cabe na fonte, e quando a fonte é
pequena demais para o card o relatório avisa (prefira o pip).

**A cabeça saindo do card** vem da máscara da visão (`visao.py --so mascara`): acima da borda só passa a pessoa,
presa numa elipse em volta da cabeça (até 1,24 vez a largura do rosto), para a prateleira encostada no cabelo
não vir junto. Sem a máscara, o card sai com a borda reta e o motor avisa uma vez.

As trocas entre superfícies (em quadros, curva de saída cúbica): quadro → tela 8 (o card cresce até virar a
tela, o rosto desce 420 px); tela → quadro 9 (a tela se dobra no card, o rosto sobe); quadro ↔ rosto 8 (o card
pequeno cresce até o grande, o mundo some); quadro ↔ pip 8; tela → rosto corte seco (o card grande assenta de
93% para 100%); rosto → tela corte seco com soco de câmera. Na volta do rosto para o mundo, a câmera começa 12%
mais perto e assenta em 7 quadros.

#### 4.14.3 A câmera

**A câmera é calma, segura o enquadramento durante a frase inteira e só se mexe quando a ideia muda.**
Câmera reapontada a cada palavra foi reprovada no original duas vezes, por ficar frenética.

| | `calma` (padrão) | `parada` |
|---|---|---|
| chaves | **até 7 por corte** | nenhuma (no máximo uma, com zoom 1: o enquadramento fixo) |
| movimento | de 0,85 a 1,4 s, curva cúbica de entrada e saída, zoom em escala logarítmica | as coisas chegam no lugar dentro do mundo, a câmera não se mexe |
| deriva | 0,4% de zoom por segundo, para a imagem nunca congelar | nenhuma |
| zoom | o objeto inteiro na vista; leitura de perto até 1,32; no máximo 1,40 num close segurado | sempre 1 |
| chicote | um por corte no máximo, como troca de cena dentro do mundo (sai correndo em 5 quadros, entra em 8, com borrão) | não tem |

- A chave chega um quadro antes da palavra: o olho já está lá quando a fala nomeia.
- **O que está sendo falado fica inteiro na vista.** Rótulo que precisa sobreviver a qualquer enquadramento
  mora dentro do objeto. O objeto ocupa pelo menos 60% da largura da vista; se ele não lê nesse tamanho, o
  mundo é redesenhado na escala da câmera, e não se dá zoom num mapa largo.
- **O 9:16 nunca tem faixa vazia.** A vista tem de cair dentro do mundo: na tela cheia, faixa vazia recusa o
  plano; no card, avisa.
- O `motor/ancoras.py` é o fiscal: recusa mais de 7 chaves na calma, chave na parada, mais de um chicote e zoom
  acima de 1,40, e avisa zoom acima de 1,32, movimento fora da faixa e chave que anda antes da anterior chegar.

#### 4.14.4 O mundo em html

A página segue o contrato do painel (`componentes/EXEMPLO-PAINEL.html`): `render(t)` pura, sem relógio próprio,
sem transição de CSS, e `window.PRONTO` quando fontes e imagens carregaram. O `componentes/mundo-base.js` cuida
do resto:

```html
<link rel="stylesheet" href="/componentes/base.css">
<script src="/componentes/base.js"></script>
<script src="/componentes/mundo-base.js"></script>
<script>
Mundo.iniciar({ nome: "terminal", largura: 1080, altura: 1350, pecas: ["caixa-de-comando"] }, function (raiz) {
  var t0 = Mundo.beat("comandos");           // o tempo já resolvido do beat do plano
  var caixa = FC.criar("caixa-de-comando", { titulo: "Claude Code", linhas: [...], largura: 960 });
  FC.adicionar(caixa, raiz); FC.posicionar(caixa, 60, 250);
  caixa.palco.setAttribute("data-objeto", "terminal");
  window.render = function (t) { /* o estado do instante t, com t no tempo do corte */ };
});
</script>
```

- **Conteúdo real.** O arquivo é um editor com as linhas de verdade, a pasta tem os arquivos de verdade, o
  número é o número dito. Texto comprido se corta com reticências, como uma janela estreita, e nunca se finge.
- **O quadro 0 é a coisa**: o objeto do assunto grande, com pelo menos 40% da altura do card, e a frase do
  gancho se montando palavra por palavra em até 5 palavras. Nunca o rosto sozinho, nunca parede de texto.
- **Um herói por ideia, plano e limpo**: nada de sombra, brilho ou adesivo decorativo; letra de pelo menos 44 px
  na tela; um título além do gancho, no máximo, no corte inteiro.
- **Algo novo a cada 1 a 2 s** enquanto a pessoa fala: um chip na palavra que nomeia a coisa, um anel no que a
  fala aponta, uma linha que entra. Quem dá o ritmo são os elementos, não a câmera.
- No pip, o que precisa ser lido no mundo fica abaixo de y 220 da tela (o card começa em 150).

#### 4.14.5 O rosto e o tempo de cada superfície

- A pergunta que decide cada trecho: **a frase aponta para uma coisa, ou a frase é a pessoa?** Coisa vai para o
  mundo (quadro ou tela), pessoa vai para o `rosto`.
- O rosto fica em cena em pelo menos **dois terços** do tempo de mundo (quadro, pip e rosto contam; tela não).
- O `rosto` é respiro de 1 a 2 s; a `tela`, trechos curtos, só quando o objeto precisa da tela inteira.
- A fala fica em 1,0x quando o reel é todo de mundo: a energia vem do corte e do mundo (é sempre pergunta ao
  criador, como em todo reel).

#### 4.14.6 Som

No máximo **um whoosh** nas cenas de mundo: no chicote, se houver; senão na primeira vez que o card vira tela.
Na câmera `parada`, nenhum. As outras trocas de superfície e as chaves entram como evento sem som (o gate de
ritmo conta), e os `beats` só tocam o som que declararem.

#### 4.14.7 Conferir

O render inteiro grava o `mundo.json` (as chaves, as cenas, a maior ampliação do rosto, o whoosh) e um PNG em
tamanho cheio de cada chave de câmera e de cada troca de superfície, em `conferencia-mundo/`. **Olhe cada um**:
texto cortado na borda da vista? letra abaixo de 44 px? Miniatura mente sobre enquadramento: confira em
tamanho cheio antes de reapontar a câmera. O gate 13 (`mundo`, no `conferir_reel.py`) reprova câmera fora do
modo e whoosh a mais, e avisa rosto acima de 1,12x e rosto em cena abaixo de dois terços.

`compor.py --quadros 3,7.7,12` grava vários quadros de uma vez em `quadros/`, sem render inteiro: é o jeito
barato de acertar a câmera antes de gastar o render.

## 5. As transições

| transição | o que faz | som | janela |
|---|---|---|---|
| `corte` | troca seca (padrão) | nenhum | nenhuma |
| `lamina` | uma lâmina de vidro varre o quadro e a cena nova aparece atrás dela | whoosh | ±0,3 s |
| `clarao` | um clarão no acento cobre a troca (no máximo dois por corte) | clarao | 0,18 s em volta do `inicio` |
| `zoom-desfoque` | a cena velha aproxima e desfoca, a nova chega do desfoque | whoosh | ±0,18 s |
| `chicote` | as duas cenas deslizam juntas para a esquerda, com desfoque de movimento | whoosh | ±0,17 s |
| `mascara` | a cena nova abre num círculo a partir do `mascaraCentro` dela (o centro do assunto) | subida | 0,5 s antes do `inicio` |
| `bolha-encolhe` | o rosto em tela cheia encolhe até a bolha da cena nova | whoosh | 0,6 s depois do `inicio` |
| `bolha-expande` | a bolha da cena velha cresce até virar o rosto em tela cheia | whoosh | 0,5 s antes do `inicio` |

**As três da 3.0:**

| transição | o que faz | som | janela |
|---|---|---|---|
| `desfoque` | A cena de antes desfoca e cresce para 1,03. A nova vem por cima, saindo do desfoque e assentando de 0,98 para 1. O véu vai de 0 a 18 px e volta a 0, e o auge cai no meio da janela, que é também o cruzamento das duas. No `inicio`, a de antes já sumiu e a nova está nítida e parada. A legenda e o `CENAS.sobre` não desfocam. | whoosh, no cruzamento (`inicio − dur/2`) | `inicio − dur` a `inicio` (padrão 0,32 s) |
| `inclinada` | Corte seco no `inicio`. O primeiro quadro do vídeo mostra a cena nova inteira como placa de vidro inclinada: girada −20°, tombada 7°, a 80% do quadro, com cantos de 48 px e borda clara com reflexo, sobre o palco da marca. A placa se endireita até o quadro cheio, desacelerando (power3.out). | whoosh, no `inicio` | do `inicio` até o primeiro quadro + `dur` (padrão 0,5 s) |
| `mergulho` | A cena de antes acelera para dentro da câmera (power3.in) até 2,4x, em volta do centro do mergulho. O centro é puxado para o meio do quadro só até onde a cena ampliada ainda cobre o quadro inteiro, com folga para a borda desfocada. No fim há um desfoque de até 6 px, e a nova está lá no corte. | whoosh, no `inicio` | `inicio − dur` a `inicio` (padrão 0,6 s) |

```json
{ "id": "c3", "modo": "rosto-vidro", "inicio": 11.55, "fim": 22.5,
  "entrada": { "transicao": "inclinada", "duracao": 0.5 }, "conteudo": { ... } }
```

**Duração e centro**
- `entrada.duracao` muda a duração padrão das três (0,32, 0,5 e 0,6 s).
- O centro do `mergulho` é o primeiro que existir na cena de antes, nesta ordem:
  1. `mergulhoCentro`, devolvido pelo modo;
  2. `mascaraCentro`;
  3. o rosto da `vistaRosto`, na altura dos olhos;
  4. `"50% 45%"`.
- O centro aceita `[x, y]` em pixels de saída ou `"x y"` em % ou px.
- Um modo que tem uma tela ou placa dentro dele deve devolver `mergulhoCentro` no centro dela. Centros perto da borda do quadro mergulham, mas não chegam ao meio. Exemplo: a `lista` com `"50% 14%"` leva o centro de y 269 só até y ≈ 602.

**Depois da janela, nada sobra**
- Nenhuma das três deixa filtro, transformação, opacidade, canto ou sombra na cena.
- O quadro seguinte, legenda incluída, é idêntico pixel a pixel ao de um corte seco.
- O zoom de ênfase e a próxima transição da mesma cena começam do zero.

**A legenda nas janelas**
- Enquanto uma das três mexe na cena, `M.rostoNaTela` mede o rosto como se a cena estivesse parada: transicoes.js tira a transformação dela por um instante e devolve logo em seguida.
- O grupo de palavras decidido ali cai na altura de um corte seco. A prévia do `--quadro` dentro de uma janela também bate com o render.
- O `layout.jsonl` e os gates continuam medindo o rosto real, pela função interna do motor.

**Janelas não se cruzam (erro)**
- A janela de entrada e a de saída da mesma cena não podem se cruzar nem passar da cena. Essa conta vale entre as três da 3.0, e entre elas e a `zoom-desfoque` e o `chicote`.
- O plano que viola isso é recusado com `Error`, que dá a cena, os tempos e a saída: alongar a cena ou encurtar `duracao`.
- Mínimos no padrão:
  - `inclinada` na entrada e `mergulho` na saída: 1,1 s mais até um quadro;
  - `inclinada` + `desfoque`: 0,82 s mais um quadro;
  - `desfoque` na entrada e `mergulho` na saída: 0,6 s;
  - cena que sai com `desfoque`: pelo menos 0,32 s.

**Ritmo:** as três registram o evento `transicao` (peso 3) a no máximo 0,16 s do evento `cena`. O gate de ritmo conta uma recomposição só.

**O que o motor ganha na camada das cenas:**
- `.tr-veu` (desfoque): backdrop-filter, último filho de `#camada-cenas`, visível só na janela.
- `.tr-palco` (inclinada): logo antes da cena nova.
- `.tr-borda` (inclinada): dentro da cena nova.
- O CSS entra uma vez, em `<style id="estilo-transicoes">`.

A troca acontece no `inicio` da cena nova; a transição cobre a troca, metade antes e metade depois,
exceto as que dizem outra coisa acima. `entrada.duracao` muda a duração padrão. Cada uma registra um evento `transicao` com o seu som e marca a
sua janela (`Motor.janela(a, b)`), que vira o campo `transicao` do `layout.jsonl`.

---

## 6. O runtime (o que um modo pode usar)

Dentro de `web/`, `motor.js` expõe `Motor` com:

- `Motor.registrarModo(nome, fn)` e `Motor.registrarTransicao(nome, fn)`.
- `Motor.vista(pai, {x, y, w, h, raio, fonte, caixa, seguirRosto, enquadre, desfoque, escurecer, inicio})`:
  uma janela para um vídeo (`fonte`: `"principal"` ou um nome de `videos`), com recorte fixo em pixels da
  fonte (`caixa`, que vale mais que tudo) ou seguindo o rosto (`enquadre`: `"busto"` põe o rosto a 40% da
  altura, `"rosto"` a 47%); `limite` é a região onde o enquadre que segue o rosto anda (a janela da
  webcam numa gravação de tela). O
  quadro certo entra sozinho a cada instante; `inicio` faz o vídeo começar do zero naquele instante.
  Com `desfoque`, a vista sai um pouco do quadro (3 vezes o raio) para a borda não escurecer.
- `Motor.ui.*`: `vidro`, `texto`, `numero`, `selo`, `logo`, `imagem`, `contorno`, `chip`, `brilho`,
  `adesivo` (PNG sem fundo, `{acervo | src, x, y, w, h, placa, sombra}`).
- `Motor.acervo(nome)`: o endereço do logo em cor `componentes/marcas/<nome>.png`. O campo `acervo` de
  qualquer cena entra na pré-carga sozinho.
- `Motor.anim.*`: `entra` (padrão: sobe; `modo: "foco"`: de desfocado para nítido em 0,14 s), `sai`
  (`"varre"`, `"corte"` ou `"desfoque"`: desfoca e some em 0,2 s), `pop` (escala com leve passada do
  ponto, para ícone e logo), `acende`, `contar` (respeita as `casas` do número), `camera`, `desenhar`.
  A visibilidade dessas animações vai só em `set`, e o tween leva só o movimento: a legenda `revela`
  mede outros quadros e volta, e um `autoAlpha` dentro de um `fromTo` reacendia o elemento fora de hora.
  Quem escreve animação nova segue o mesmo cuidado.
- `Motor.registrarSobre(tipo, fn)`: registra uma sobreposição (seção 4.10). `fn` recebe `{ raiz, tl, M,
  item, inicio, fim, dur, cena, global, nome, api }`.
- `Motor.evento(t, tipo, peso, alvo, som)`: registra um acontecimento (as `anim.*` já registram).
- `Motor.janela(a, b)`: marca o intervalo de uma transição (só as transições usam).
- `Motor.aCada(fn)`: chama `fn(t)` a cada quadro, depois do seek, para o que não cabe numa timeline.
- `Motor.medirTexto(texto, fonte, tam)`: a largura do texto em px, medida com a fonte da marca.
- `Motor.el`, `Motor.caixa`: criar e posicionar elementos.
- `Motor.rostoNaVista(vista, k)`: a caixa do rosto numa vista que segue o rosto, no quadro `k`, em
  pixels de saída. Serve para o modo, ao montar, não cobrir o rosto.
- `Motor.pecasBolha`: bolha, câmera e marcas, das cenas com bolha (em `modos/tela-bolha.js`).
- `Motor.Z`: as zonas seguras; `Motor.T`: os tokens da marca.

**A visão do corte no runtime (3.0, Onda 2).** Tudo isto lê `window.VISAO` (seção 2.6). Sem ela, nada
disto existe e o motor é o de antes.

- `Motor.vista(pai, { ..., recorte: "pessoa" | "fundo" })`, só na fonte principal (em outra fonte, Error):
  - `"pessoa"`: a imagem do quadro com `mask-image` = a máscara do mesmo quadro, esticada 100% x 100% em
    luminância. O índice é exatamente o do quadro de vídeo, inclusive com `inicio`. O fundo da vista é
    transparente.
  - `"fundo"`: o `fundo-limpo.jpg` no lugar dos quadros, com o mesmo enquadre.
  - O `M.render` carrega e decodifica cada máscara (`new Image` + `decode`) antes de pôr no CSS: a foto do
    quadro nunca sai com a máscara de outro.
  - Sem a visão, ou sem a parte, a vista dá o Error padrão ("... rode o visao.py ...").
- `Motor.visao`: o `window.VISAO` (ou `null`).
- `Motor.exigirVisao(quem, parte)`: lança o Error padrão quando falta a visão ou a parte (`"mascara"`,
  `"fundo"`, `"profundidade"`, `"maos"`, `"corpo"`, `"objetos"`); a mensagem diz o `--so` a rodar.
- `Motor.maosNoQuadro(k)` (lista, `[]` sem dado), `Motor.corpoNoQuadro(k)` (objeto ou `null`) e
  `Motor.objetosNoQuadro(k)` (lista): os dados em pixels da fonte, no quadro `k` (0 = o primeiro; o mesmo
  índice do `fala.mp4` e do reel), com o índice preso às pontas.
- `Motor.mascaraUrl(k)` e `Motor.profundidadeUrl(k)`: o endereço do PNG daquele quadro, ou `null`.
- `Motor.fonteParaTela(vista, x, y)` → `[X, Y]` em pixels de saída: um ponto da fonte levado para a tela no
  quadro que acabou de ser renderizado. Conta a posição da vista, o enquadre, os dois zooms e qualquer
  escala da cena (as transições), pela caixa da imagem na tela: use dentro de `M.aCada` ou depois do
  render. Com a cena girada em 3D, a resposta é a caixa que envolve a imagem, aproximada (o `camadas`
  publica `plano3d` para a conta exata, seção 4.11).
- `Motor.escalaNaTela(vista)`: quantos pixels de saída vale um pixel da fonte nessa vista, agora.
- `Motor.ATRAS = { limiar: 0.35, minimo_s: 0.3 }`: a régua do texto escondido (seção 3.3). O gate usa a
  mesma.
- `Motor.textosInfo()` (a medida de contraste): o texto dentro de `[data-atras="1"]` ganha `atras: true` e
  `recorte: { quadro, imagem: [x, y, w, h], janela: [x, y, w, h] }`, o quadro da máscara e as caixas, na
  tela, da imagem e da janela da vista que fura a peça (com giro, as caixas que envolvem a imagem).
  `recorte` vem `null` quando nada cobre o texto naquele quadro.
- `Motor.fecharAvisos()`: fecha as corridas de texto escondido ainda abertas e avisa delas, e solta o
  aviso único da legenda com as linhas que ficaram por cima de uma mão (o `legenda.js` acrescenta isso ao
  iniciar). O `compor.py` chama no fim do render e depois do `--quadro`.
- `Motor.layout(t, k)` (o `layout.jsonl`) ganha `atras` com texto atrás de você na tela (seção 2.5).
- `M.anim.sai` com `modo: "desfoque"` desfoca até opacidade 0,001, não 0: com 0, o set do fim guardava
  "escondido" como o estado de antes, e voltar no tempo apagava a peça para sempre.

Quem desenha preso ao vídeo (as peças da visão) lê a vista já posta no lugar dentro de `M.aCada`, escreve o
estado de todo quadro em que pode aparecer e esconde o desenho fora dele; o que é texto anda por sets na
linha do tempo, gravados no primeiro render, porque a legenda `revela` busca outros quadros só pela linha
do tempo, sem rodar os ganchos. Um PNG por quadro (a máscara, a profundidade) entra como fonte do motor
com uma vista invisível de 1 px, para o render esperar ele decodificar antes dos ganchos.

O destaque em gradiente vem do token `cores.destaque_gradiente` (duas ou três cores) em
`--destaque-gradiente`; sem o token, é o acento chapado. Texto pintado com ele (classe `t-gradiente`)
leva `data-cor` com a cor sólida, que é a que o gate de contraste mede. Texto no meio da saída
(`sai` com varredura ou desfoque) ganha `data-saindo` e sai da conta do contraste. A fonte mono da marca
(`fontes.mono`, JetBrains Mono) entra como `"FC Mono"`.

Todo texto que um modo põe na tela carrega `data-texto` (as `ui.*` já põem), para os gates acharem.
O atributo vai no elemento que tem a letra, não na caixa em volta: a medida de contraste esconde o que
tem `data-texto` e mede o que sobra atrás. O que não é letra mas mora na zona segura como ela (o
adesivo) leva `data-zona`: entra no gate de zonas e fica fora do de contraste.

Cada camada é um contexto de empilhamento: as cenas ficam embaixo (z 10), a legenda por cima (z 20) e
a camada de transição no topo (z 30). O `z-index` de uma peça dentro da cena nunca passa da legenda.
A legenda não atravessa troca de cena: o grupo de palavras quebra no `inicio` de cada cena, porque
cada cena põe a legenda numa altura.

## 7. Comandos

```
flow-reels produzir/editar_fala --projeto projetos/<v> --corte 01 --trechos "0.40-41.2"
flow-reels produzir/rosto --projeto projetos/<v> --corte 01
flow-reels produzir/visao --projeto projetos/<v> --corte 01   (opcional: Onda 2)
flow-reels produzir/compor --projeto projetos/<v> --corte 01
flow-reels produzir/audio --projeto projetos/<v> --corte 01
flow-reels produzir/conferir_reel --projeto projetos/<v> --corte 01
```

`compor.py --previa` renderiza em 540 x 960 para conferir rápido, e `--quadro 12.4` grava um PNG só
daquele instante e mostra os avisos do motor. Só o render inteiro escreve o `eventos.json`. A legenda
`revela` mede quadros à frente e volta refazendo a busca do zero, então o quadro do render em sequência
e o do `--quadro` são o mesmo; os avisos que dependem da sequência (colisões medidas quadro a quadro)
só saem no render inteiro.

O `visao.py` (seção 2.6) roda depois do `editar_fala.py` e do `rosto.py`, uma vez por corte, só quando o
plano usa as peças da Onda 2: `"atras"`, o modo `camadas`, `deteccao`, `maos`, `contorno`, `profundidade`,
o `logo-volume` com `segue` ou o desvio das mãos da legenda. `--so mascara,fundo,profundidade,maos,corpo,
objetos` faz só essas partes; `--refazer` refaz o que já vale. Depois de reeditar o `fala.mp4`, rode de
novo, sem `--so`.
