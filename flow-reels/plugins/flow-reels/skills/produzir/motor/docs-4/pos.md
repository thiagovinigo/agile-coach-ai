# Pós no quadro inteiro e acabamento (4.3)

O `look` da 4.0 (`web/sobre/look.js`) trata só a imagem do vídeo. O **pós** trata o quadro inteiro:
a cena com os cards, as palavras, as sobreposições e o 3D. A **legenda fica sempre fora**, nítida e por
cima. O **acabamento** é um grading global barato (LUT, vinheta e grão), feito pelo ffmpeg na hora de
codificar.

Arquivos: `web/pos.js` (efeitos e shaders), `motor.js` (2 linhas: `M.Pos.iniciar()` na montagem e
`M.Pos.limpar()` no começo de todo render), `motor.html` (carrega o `pos.js`), `compor.py` (a segunda
passada, o acabamento, a GPU e a medida honesta do contraste), `componentes/luts/` (as LUTs da marca e o
gerador).

## 1. A escolha: segunda passada (opção b)

| opção | o que a prova mostrou nesta máquina (Chromium 153, M4) | veredito |
|---|---|---|
| (a) HTML-in-Canvas (`CanvasDrawElement`) | Funciona com a flag, mas **um `<canvas>` WebGL dentro do palco não sai na captura** (some: aparece o que está atrás dele). Um canvas 2D saiu certo. Quase toda peça da 4.0 que conta (three.js, `nuvem`, `malha`, `objeto3d`, frames 3D, mãos, `look`) desenha em WebGL. Seria preciso compor cada canvas à parte, esperar o evento `paint` e prender o Playwright, porque a API muda de nome no Chrome 155 e o Origin Trial acaba no 160. | fora, por agora |
| **(b) segunda passada** | Foto da página sem a legenda (CDP), shader numa tela WebGL do próprio motor, legenda por cima. Pega tudo, inclusive WebGL, `backdrop-filter`, máscaras e transições. API estável. | **escolhida** |
| (c) híbrido com reserva | Só faria sentido se (a) pegasse o WebGL. | fora |

O custo extra da (b) só existe nos quadros com pós ativo e ficou bem abaixo do alvo (seção 6).

### Como um quadro com pós é feito

```
compor.py                         motor (pos.js)
 render(t)  ───────────────────►  M.Pos.limpar() esconde a tela do pós; o quadro de sempre
 Pos.antes(t) ─────────────────►  há efeito com força > 0 em t? se não: false (fim)
                                  se sim: body.pos-captura (legenda e transição com opacidade 0)
 CDP captureScreenshot (JPEG 95)  a foto do quadro sem legenda, em base64, sem passar pelo Python
 Pos.aplicar(b64) ─────────────►  createImageBitmap → textura (com mipmaps) → cadeia de shaders
                                  → #camada-pos (z 18) visível; legenda e transição de volta
 screenshot JPEG 92 → ffmpeg      o quadro final
```

A tela `#camada-pos` fica entre as sobreposições (z 15) e a legenda (z 20). A camada das transições
(z 30) também fica fora do pós e continua por cima da legenda, como sempre esteve.

**Reel sem `pos` e sem `acabamento` sai pixel a pixel igual ao de antes**: não há tela nem estilo, o
caminho do `compor.py` é o mesmo, e a GPU só liga com pos. Conferido com `--quadro` no corte 40
(1,5 / 12 / 24 / 30 s) e no 44 (6,5 / 20 s): diferença máxima 0.

## 2. O contrato: `pos` no `cenas.json`

```json
{
  "pos": [ { "efeito": "grao", "quantidade": 0.06 } ],
  "acabamento": { "lut": "neutra-quente", "grao": 0.25, "vinheta": 0.15 },
  "cenas": [
    { "id": "c4", "modo": "rosto-vidro", "inicio": 7.75, "fim": 9.86,
      "pos": [ { "efeito": "vhs", "forca": 0.85 }, { "efeito": "aberracao", "px": 16 } ] },
    { "id": "c2", "modo": "rosto-vidro", "inicio": 2.92, "fim": 5.72,
      "pos": [ { "efeito": "glitch", "t": 3.2, "ate": 3.62, "semente": 7 } ] }
  ]
}
```

- **Onde mora.** `pos` no topo vale para o reel inteiro; `cena.pos` vive na cena (o tempo fica preso a
  `[inicio, fim]` dela; na última, até o fim do reel).
- **Tempo.** `t` e `ate` são **absolutos**, como todo o plano (MOTOR.md 3). Sem `t`/`ate`, o efeito vale
  a cena inteira (ou o reel inteiro). Durante uma transição de entrada, o pós da cena nova só começa no
  `inicio` dela, e pega o quadro inteiro (as duas cenas).
- **Força.** `forca` de 0 a 1 (padrão 1). `entra` e `sai` são rampas em segundos; o padrão vem do efeito
  quando há `t`/`ate` próprios, e é 0 (entra seco, com o corte) quando o efeito ocupa a cena. `curva`:
  qualquer ease do GSAP (`"power2.out"`); padrão smoothstep. A força é uma conta fechada de t: sem
  estado, sem relógio.
- **Parâmetros.** Direto no item (`"px": 16`) ou em `"params": {...}`. Valores em px são px de saída num
  quadro de 1080 de largura; a prévia (540 x 960) escala sozinha.
- **Semente.** `semente` (inteiro) muda o sorteio do glitch, do ruído e da fita. Padrão: a posição do item.
- **Som.** O item com `t` próprio registra um evento `pos` (peso 2) no `eventos.json`, com o som do
  efeito (tabela abaixo); `"som": "<nome>"` troca e `"som": false` cala. Sem `t`, nenhum evento (a cena já
  tem o dela).
- **Ordem.** A cadeia segue uma ordem fixa, não a do plano: `onda, lente, glitch, vhs, pixel, ascii,
  pontilhado, reticula, aberracao, bloom, crt, grao, vinheta` (geometria, estilo, luz, tela, película).
- **Avisos** (console, repetidos pelo compor.py): soma das forças ativas acima de 2,2 num quadro (sopa de
  efeito); glitch com mais de 1,5 s seguidos e força acima de 0,4; efeito ou parâmetro inválido é Error.

### Os efeitos

| efeito | o que faz | parâmetros (padrão) | rampa | som |
|---|---|---|---|---|
| `crt` | barril, convergência, linhas de varredura, máscara de fósforo, halação, cantos do tubo | `curvatura` 0.1, `linhas` 4 (px por linha), `mascara` 0.35, `brilho` 0.5, `cor` original \| destaque \| ciano (fósforo de uma cor) | 0.35 / 0.3 | estatica |
| `vhs` | tremor de linha, croma escorrido, realce de borda, faixa de tracking, troca de cabeça, ruído e neve | `ruido` 1, `tracking` 1 | 0.3 / 0.25 | rebobina |
| `glitch` | fatias deslocadas com RGB separado, macroblocos, fatias tingidas (rosa/ciano), sorteadas por quadro | `densidade` 0.35, `desloca` 70 px, `rgb` 14 px, `ritmo` 0.6 (chance do quadro falhar), `segura` 2 (quadros por sorteio), `cor` destaque \| ciano | 0 / 0 | glitch |
| `aberracao` | aberração cromática radial (vermelho para fora, azul para dentro), mais forte nas bordas | `px` 14 (no canto), `centro` null (meio) \| [x, y] \| "50% 40%" \| "rosto" | 0.25 / 0.25 | — |
| `bloom` | as luzes acima do limiar vazam, borradas e tingidas de rosa, somadas em "tela" | `limiar` 0.62, `intensidade` 1.1, `tingir` 0.6, `raio` 0 (+1 = dobro), `cor` destaque \| ciano \| branco | 0.3 / 0.3 | — |
| `grao` | grão de película, mais forte nos meios-tons | `quantidade` 0.09, `tamanho` 1.5 px, `segura` 2 (quadros por sorteio: grão novo a cada quadro custa o dobro de bits) | 0.2 / 0.2 | — |
| `pontilhado` | pontilhado ordenado Bayer 8x8, por canal em poucos níveis, ou em duas cores; entra em blocos | `escala` 3 px, `niveis` 4, `cor` original \| destaque \| ciano | 0.35 / 0.3 | whoosh |
| `reticula` | retícula de impressão (pontos numa grade girada, raio pela luz) sobre papel escuro; os pontos crescem na entrada | `escala` 12 px, `angulo` 45, `cor` original \| destaque \| ciano \| tinta | 0.4 / 0.3 | whoosh |
| `pixel` | blocos que crescem com a força (ótimo com `entra: 0, sai: 0.6` para "resolver" a imagem) | `escala` 16 px | 0.35 / 0.3 | bip |
| `onda` | distorção senoidal com ruído (água, calor, sonho) | `amplitude` 16 px, `comprimento` 260 px, `velocidade` 1.2 (ciclos/s), `ruido` 0.35, `direcao` horizontal \| vertical | 0.3 / 0.3 | whoosh |
| `vinheta` | bordas escurecem (ou vão para um rosa escuro) | `quantidade` 0.6, `raio` 0.75, `cor` escuro \| destaque | 0.3 / 0.3 | — |
| `lente` | barril com os cantos presos (o meio aproxima), desfoque e franja de cor nas bordas | `distorcao` 0.14 (só positiva), `desfoque` 7 px, `aberracao` 4 px | 0.3 / 0.3 | — |
| `ascii` | cada célula vira o caractere da fonte mono (FC Mono) com a tinta da luz dela; entra decodificando | `escala` 14 px (largura da célula), `cor` original \| destaque \| ciano \| tinta | 0.5 / 0.3 | glitch |

Os shaders são nossos (WebGL2, um contexto só, programas aquecidos na montagem); o hash inteiro sem
seno, o Bayer e o atlas do ascii seguem a receita do `look.js` (que não foi alterado).

## 3. O acabamento: `acabamento` no topo

```json
"acabamento": { "lut": "neutra-quente", "grao": 0.25, "vinheta": 0.15 }
```

| chave | o que é | como vira ffmpeg |
|---|---|---|
| `lut` | nome de uma LUT de `componentes/luts/` (sem `.cube`) ou caminho de um `.cube` (relativo à pasta do corte ou à raiz) | `lut3d` tetraédrico, em RGB planar (`gbrp`) antes da conversão de saída |
| `vinheta` | 0 a 1 | `vignette` com o aspecto do quadro (segue o retângulo); 0,15 escurece 2% em y 300 e 6% no canto; 1,0, 17% e 56% |
| `grao` | 0 a 1 | `noise` só na luma, temporal "médio" (`c0f=t+a`, `c0s` = grao x 24), semente fixa, depois da conversão para yuv420p |

Sai no `video.mp4`, na `--previa`, no `--de/--ate` e também no PNG do `--quadro` (o compor.py passa o
PNG pelo mesmo filtro). Com LUT identidade, a diferença para o caminho sem acabamento é 0,5 de média
(máx. 6, arredondamento do croma): a cor não desvia.

**As LUTs da marca** (`componentes/luts/gerar_luts.py`, conta fechada, 33 pontos, refazer dá os mesmos
arquivos): `neutra-quente` (leve, branco puxando para o quente), `fria-tech` (sombras para o ciano da
marca), `filme` (preto levantado, ombro nas altas, sombras frias e altas quentes), `noir` (P&B de
contraste alto, filtro vermelho). O rosa #FF005E continua rosa nas três primeiras (pela neutra-quente sai
#FF005D).

## 4. Os gates continuam honestos

- **Contraste.** O quadro sem texto da amostra (`contraste/fNNNNNN.png`) passa pelo **mesmo pós** e pelo
  **mesmo acabamento**. E a cor de cada texto (fora a legenda) deixa de ser a do CSS: é **medida no quadro
  final**. Os pixels da caixa que mudam entre o quadro final (PNG, sem perda) e o quadro sem texto são a
  letra, e a mediana deles é a cor que o gate usa (`cor`; o CSS fica em `cor_css`, e `cor_medida: true`).
  Sem letra que se veja (diferença máxima abaixo de 90, ou menos de 1% da caixa), fica a cor do CSS, como
  antes. A legenda está fora do pós; com LUT, a cor e o contorno dela passam pela LUT.
- **O que isso pega de verdade** (visto no corte 50 enquanto o plano era ajustado): número escuro num
  chip rosa sob `crt` (as linhas escurecem o rosa: 1,9:1), a `lente` desfocando um número pequeno na
  borda (1,5:1), `pontilhado` com rosa no fundo atrás de palavra rosa (1,04:1), `vinheta` forte numa
  palavra rosa no alto (2,7:1). Todos reprovaram, e eram problemas reais.
- **Zonas, rosto, ritmo** seguem iguais: o layout é medido antes da passada. Os efeitos que entortam
  (`onda`, `lente`, `crt`, `glitch`) mexem alguns px na posição real do texto; o layout não conta isso.
- **Ritmo e som**: o `pos` com `t` próprio entra no `eventos.json` como evento de peso 2.

## 5. GPU

Qualquer item de `pos` (no reel ou numa cena) liga a GPU (Metal) no `compor.py` (`usa_3d` → `tem_pos`).
O acabamento é do ffmpeg e não pede GPU. Não precisa mexer no `gpu.json`: o pos não usa nome de peça.

## 6. Custo medido (M4, 1080 x 1920, corte 50)

| medida | ms |
|---|---|
| a passada sozinha: foto CDP JPEG 95 | ~26 |
| a passada sozinha: decodificar, subir, mipmaps, cadeia, desenhar | ~14 (ascii) |
| quadro com pós (render + passada + foto final), reel inteiro | **81 a 113** (81 no render final) |
| quadro sem pós no mesmo reel | 41 a 54 |
| mesma passada com a 1ª foto em PNG (sem perda) | 201 por quadro: por isso JPEG 95 |
| fidelidade da passada com força 0 (JPEG 95 de ida) | média 0,47, p99 3, máx. 19 (sem desvio de cor) |
| amostra de contraste com pós/acabamento (PNG extra + 2 ffmpeg) | ~0,7 s por amostra (71 no corte 50) |

Render inteiro do corte 50 (697 de 1084 quadros com pós, acabamento ligado, 71 amostras): 196 s, 181 ms
por quadro no total. O alvo de menos de 200 ms nos quadros com pós ficou com folga. Determinismo: o mesmo
`--quadro` (glitch, ascii embaralhando, vhs) duas vezes deu diferença 0.

### O peso no arquivo (x264, crf 18)

Ruído que muda a cada quadro é o que o x264 menos consegue comprimir. Medido no corte 50 (MB a cada 2 s;
o mesmo plano sem pós, o corte 44, fica em ~1,7):

| trecho | MB / 2 s |
|---|---|
| só o acabamento (LUT, vinheta 0,15, grão 0,25 em `t+a`) | 1,7 a 2,6 |
| `pontilhado` (o padrão treme com o ruído do vídeo) | 6,3 |
| `vhs` + `aberracao` | 11,7 |
| `grao` do pós (`segura` 2) / `bloom` + `grao` | 8,0 / 11,4 |

Com o grão gaussiano puro (`c0f=t`) no acabamento, o reel inteiro dava 252 MB (12 MB a cada 2 s em
toda parte); com `t+a`, 78 MB no total. O corte 44 tem 31 MB. Grão forte no acabamento (0,5 ou mais)
volta a pesar: prefira 0,15 a 0,3 e o `grao` do pós só nas cenas que pedem.

## 7. Limites

- O pós pega o quadro inteiro: não há `alvo` pessoa/fundo (isso é o `look`, no vídeo). Palavras e cards
  sofrem o efeito, e o gate mede o que sobra.
- O grão do acabamento é do ffmpeg: sai igual a cada render inteiro (semente fixa), mas num `--de/--ate`
  ou num `--quadro` o padrão do grão é outro (a mesma aparência, não o mesmo pixel).
- A transição fica fora do pós (sempre por cima). Uma lâmina ou um clarão não ganham o efeito.
- `lente` com `distorcao` negativa (almofada) não é aceita (cortaria as bordas).
- O gate mede cor, não forma: `ascii`, `pixel` e `pontilhado` fortes sobre palavra pequena podem passar no
  contraste e ainda assim ficar ilegíveis. Use-os em cena de texto grande ou sem texto.
- Os efeitos de padrão fino (`crt`, `pontilhado`, `reticula`) reprovam com facilidade texto pequeno ou
  rosa sobre rosa: é o gate fazendo o trabalho dele.

## 8. Teste de referência

`projetos/teste-onda-1` corte 50: a fala do corte 40, o plano do 44 (4 transições), visão rodada, os 13
efeitos em cenas diferentes e o acabamento `neutra-quente` + grão 0,25 + vinheta 0,15. Os 9 gates
passaram (contraste: 174 textos, o mais justo 3,02:1); aviso só no som, que já vinha do plano base. A
folha de contato está em `materiais-de-trabalho/corte-50/folha-pos.jpg`.
