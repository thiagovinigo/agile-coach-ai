# Looks no vídeo: a sobreposição `look` (4.0)

Um filtro em shader aplicado à **imagem do vídeo** da cena (a vista do rosto, `api.vistaRosto`), com a
máscara da pessoa (`VISAO.mascara`) escolhendo onde ele vale. Cards, palavras e a legenda ficam por cima,
nítidos, e continuam medidos pelos gates. Arquivo: `web/sobre/look.js`. Pede WebGL2: o `compor.py` liga
a GPU pelo nome `look` em `motor/gpu.json` (ou `"gpu": true` no cenas.json).

```json
{ "tipo": "look", "efeito": "crt", "alvo": "tudo", "t": 0.05, "ate": 2.6 }
{ "tipo": "look", "efeito": "duotone", "alvo": "pessoa", "cor": "destaque", "t": 5.25, "ate": 7.6 }
{ "tipo": "look", "efeito": "pixel", "escala": 24, "t": 12.45, "ate": 14.6 }
```

Em `cena.sobre`, vive na cena e anda com ela. Em `CENAS.sobre`, vale de `t` a `ate` em toda cena com o
vídeo do rosto na tela (cada cena com a sua vista); cena sem rosto (lista, tipografia...) fica sem look,
com aviso.

## Campos

| campo | o que é | padrão |
|---|---|---|
| `efeito` | um dos 14 abaixo | obrigatório |
| `alvo` | `fundo` (o cenário; você intacto, borda da máscara suavizada ~2 px), `pessoa` (o contrário) ou `tudo` | o do efeito (tabela); o geral é `fundo` |
| `t`, `ate` | começo e fim, no tempo absoluto. Na cena, presos ao começo e ao fim dela | a cena inteira (no reel, o reel inteiro) |
| `forca` | 0 a 1: quanto do efeito entra por cima da imagem | 1 |
| `entra`, `sai` | segundos da entrada e da saída. Se as duas não cabem na vida, encolhem juntas (com aviso) | o do efeito (tabela); o geral é 0,25 |
| `cor` | a tinta do efeito, onde ele tem cor: `destaque`, `ciano`, `tinta` (e `preto` na risografia). Cor que o efeito não aceita é Error | o do efeito |
| `escala` | o tamanho do padrão em px de saída (o ponto, a célula, a linha) | o do efeito |
| `niveis` | só no `posterizar`: 3 a 5 | 4 |
| `semente` | inteiro que muda o sorteio do ruído e do glitch | 0 |
| `som` | troca o som do evento (um da lista de sons) ou `false` | o do efeito |

Parâmetro inválido (efeito, alvo, cor, número fora da faixa) é `Error` com o que pôr. Alvo `fundo` ou
`pessoa` (e o `holograma` em qualquer alvo) sem a visão do corte dá o Error padrão do `visao.py`.

## Os efeitos

| efeito | o que se vê | alvo | entra / sai | escala | cor | som |
|---|---|---|---|---|---|---|
| `pontilhado` | dithering ordenado Bayer 8x8 em duas cores (preto da marca e a cor), com posterização leve antes; meios-tons puxados para o escuro para a parede clara não virar um campo rosa. Entra e sai em blocos que acendem na ordem da própria matriz | fundo | 0,4 / 0,3 | 3 (o ponto) | destaque, ciano, tinta | whoosh |
| `reticula` | retícula de pontos numa grade girada 45°, o ponto do tamanho da luz (pontos vizinhos se fundem no claro), na cor sobre o escuro. Os pontos crescem na entrada e encolhem na saída | fundo | 0,4 / 0,3 | 14 (a célula) | destaque, ciano, tinta | whoosh |
| `crt` | tubo abaulado (barril) de cantos redondos, linhas de varredura mais finas no escuro, máscara de fósforo RGB de 1 px por subpixel, convergência imperfeita nas bordas, halação, barra de zumbido subindo, reflexo do vidro na borda, vinheta e tremor de meio pixel. **Liga**: uma linha branca abre na horizontal e depois na vertical, com clarão; **desliga** ao contrário. Com `cor`, vira fósforo monocromático | tudo | 0,5 / 0,4 | 6 (o período da linha) | destaque, ciano, tinta (sem: cor natural) | estatica |
| `vhs` | luma macia com o halo de realce do videocassete, croma borrado e escorrido 6 a 22 px para a direita, saturação de fita, preto levantado, tremor por linha, faixa de tracking descendo (mais fraca sobre você), neve na faixa, riscos brancos raros e a troca de cabeça torta nas últimas linhas. **Entra e sai perdendo o tracking**: a imagem rola com a barra preta do apagamento e uma faixa forte varre o quadro | tudo | 0,45 / 0,3 | — | — | estatica |
| `pixel` | mosaico de blocos quadrados com poucos tons e borda sutil de célula. No alvo, a máscara decide por bloco (o bloco é inteiro ou não é): a borda da pessoa fica em degraus. **Resolve** de blocos 8x para 4x, 2x e o tamanho final, e volta na saída | fundo | 0,45 / 0,35 | 28 (o bloco) | — | bip |
| `duotone` | preto → cor, com o contraste puxado | fundo | 0,25 / 0,25 | — | destaque, ciano | whoosh |
| `termico` | paleta de câmera térmica em 8 faixas chapadas (azul-noite, roxo, magenta, o rosa da marca, laranja, amarelo, branco), com só o pixel da emenda misturado. Com a máscara, você fica quente (laranja no corpo, amarelo e branco no rosto) e a parede fria; o ar ferve de leve. Entra com o sensor varrendo de cima para baixo | tudo | 0,4 / 0,25 | — | — | whoosh |
| `holograma` | você em ciano (ou rosa) translúcido, com o cenário (o fundo limpo) aparecendo através, linhas finas e faixas largas subindo, franja de borda pela máscara borrada (dentro e vazando para fora), cintilação e glitch de linha (faixas que pulam por um quadro). O fundo escurece. Entra de baixo para cima atrás de uma linha de varredura | pessoa | 0,6 / 0,35 | 6 (o período das linhas) | ciano, destaque | glitch |
| `grao` | grão de película mais forte nos meios-tons, balanço do quadro de ~1 px (gate weave), flicker leve, preto e branco de película e vinheta. A assinatura sutil: cabe por cima de trechos longos | tudo | 0,25 / 0,25 | 1,6 (o grão) | — | nenhum |
| `ascii` | a imagem vira grade de caracteres da `FC Mono` (16 degraus de tinta, escolhidos e ordenados medindo cada glifo na carga), a cor mais clara onde a imagem é clara. **Decodifica** na entrada: cada célula chega embaralhada e assenta; na saída, as células somem em ordem sorteada | fundo | 0,5 / 0,3 | 14 (a largura da célula; altura × 1,62) | destaque, tinta, ciano | glitch |
| `risografia` | duas tintas sobre papel (o rosa da marca e o ciano, ou o preto), em retícula grossa por limiar (o ponto acompanha a forma), com desregistro de 2 a 4 px que escorrega a 12 quadros por segundo, tinta irregular e grão de papel. Na entrada, a tinta rosa chega de longe e assenta no registro | fundo | 0,4 / 0,25 | 11 (a retícula) | ciano, preto (a segunda tinta) | whoosh |
| `noir` | preto e branco de alto contraste, com grão e vinheta. Com `cor: "destaque"`, só o rosa e o magenta saturados do **cenário** ficam (o neon), no rosa da marca; você fica sempre em preto e branco (a pele sob luz rosa não acende) | tudo | 0,25 / 0,25 | — | destaque (sem: só preto e branco) | whoosh |
| `esboco` | bordas (Sobel) em traço de tinta sobre o escuro, hachura diagonal nas sombras e cruzada nas sombras fundas, papel milimetrado em ciano bem baixo: o desenho técnico. A pena desce traçando na entrada | fundo | 0,55 / 0,3 | — | tinta, destaque, ciano | whoosh |
| `posterizar` | 3 a 5 níveis chapados de luz mantendo o tom (cel shading), o escuro indo para o cinza do nível, com contorno escuro | fundo | 0,25 / 0,25 | 2 (a espessura do contorno) | — | whoosh |

A força sobe na entrada com `power2.out` (e desce na saída com `power2.in`) só na parte que o efeito não
resolve sozinho: o `crt`, o `pontilhado`, o `ascii` e o `esboco` entram com a força cheia, e a entrada
própria deles faz a passagem.

## Como funciona (o que importa para quem mexe)

- **A tela mora dentro da vista.** Uma tela 2D irmã da `<img>` do quadro, em `v.punch`, logo acima da
  imagem e com a caixa dela copiada a cada quadro. Herda o enquadre, o zoom de ênfase, o das emendas, a
  janela, o canto e qualquer transformação da cena: a placa da `inclinada`, o `mergulho`, o `desfoque`
  (conferido nos três). Nas cópias desfocadas da mesma imagem (o aro do `vidro-liquido`) e no vídeo vivo
  do `camadas`, a mesma pintura é copiada; na vista recortada, a tela leva a máscara da imagem.
- **Uma GPU só.** Um contexto WebGL2 compartilhado por todos os looks do reel, numa tela fora do DOM
  (`preserveDrawingBuffer`). O programa de cada efeito do plano é compilado e aquecido na montagem. O
  quadro (576 x 1024 no teste) sobe como textura com mipmaps (o desfoque barato dos efeitos) uma vez por
  quadro, e o resultado, já na resolução da caixa da imagem (até 2048 no lado maior), é copiado para a
  tela da vista.
- **Quadro e máscara do mesmo índice.** A máscara entra como fonte do motor (`look-mascara`) com uma vista
  invisível de 1 px: o render a decodifica antes dos ganchos, como faz com o quadro. O gancho confere o
  endereço da máscara contra `Motor.mascaraUrl(v.q)`; se não bater (vistas com `inicio` diferente), o
  look sai sem máscara naquele quadro, com aviso, e nunca mistura quadros.
- **Determinismo.** A força, a entrada e a saída são tweens GSAP num objeto (`f`, `e`, `s`) e acompanham
  qualquer seek. Ruído, tremor e glitch vêm de hash inteiro do pixel, do índice do quadro e da `semente`
  (sem seno). Conferido: 20 instantes (vida e entradas) renderizados sozinhos em ordem embaralhada e depois de 20 quadros em
  sequência dão diferença máxima de 1 tom.

## Custo medido (M4, Metal)

- Reel de teste inteiro (36 s, 14 looks, 3 transições, palavras): **63 a 75 ms por quadro** com o
  screenshot.
- O look sozinho: o trecho de 0 a 12 s com 4 looks saiu a 55 e 59 ms por quadro; sem os looks, 52.
  **3 a 7 ms por quadro**, os mais caros sendo a `reticula` (9 amostras por pixel) e o `vhs`.

## Contraste: o que cada efeito pede do texto

O look muda o fundo, e os gates medem o texto sobre o que ficou. No reel de teste (14 looks com a
legenda `revela` e palavras `glitch`, `conta`, `extrusao` e `pula`) os 9 gates passaram; o mais justo foi
3,03:1 (a `extrusao` rosa sobre o `esboco`).

- **A legenda passa sempre**: ela é medida contra o próprio contorno escuro.
- **Palavra rosa sobre `pontilhado`, `reticula`, `risografia` e `duotone` no fundo reprova ou fica no
  limite**: o fundo vira o próprio rosa. Medido: o `pula` rosa ("2027") sobre a `risografia` deu 2,8:1.
  Ali use a palavra em `tinta` (`"cor": "tinta", "gradiente": false`) ou com a névoa (`sombra`), ou ponha
  o look em `ciano`.
- `termico` com o alvo `tudo`: o corpo fica laranja, e a palavra da legenda no rosa ao lado lê menos de
  longe (o gate passa pelo contorno). Prefira o destaque da legenda acima do ombro.
- `crt` e `vhs` escurecem as bordas e levantam o preto; texto no meio passa sem nada.

## Limites

- Só a imagem do vídeo da fala (fonte principal). Cards, palavras e legenda não recebem o look (é a
  decisão 2 do plano; a captura do HTML fica para a 4.3).
- No alvo `fundo`/`pessoa`, os efeitos que amostram em volta (pixel, retícula, ascii) puxam um pouco da
  cor da pessoa para as células da borda: é o "halo" natural do padrão, não um erro.
- O `holograma` mostra o cenário através de você pelo fundo limpo: onde ele é inventado
  (`fundo-buraco.png`), aparece a continuação plausível da parede, escurecida a 30%.
- `crt` e `vhs` no alvo `fundo` deformam o cenário e não você: na borda da pessoa a imagem não casa. Por
  isso o padrão deles é `tudo`.
- O `crt` que liga no começo do reel deixa o quadro preto por ~0,15 s: no gancho, prefira `entra` 0,35.
- Os sons `estatica`, `glitch` e `bip` vêm da frente de som da 4.0.

## Exemplo (o reel de teste, corte 41)

```json
"sobre": [ { "tipo": "look", "efeito": "grao", "t": 31.25, "ate": 36.145 } ],
"cenas": [
  { "id": "c1", "modo": "rosto-vidro", "inicio": 0, "fim": 5.25,
    "sobre": [ { "tipo": "look", "efeito": "crt", "t": 0.05, "ate": 2.6 },
               { "tipo": "look", "efeito": "vhs", "t": 2.65, "ate": 5.2, "semente": 2 } ] },
  { "id": "c5", "modo": "rosto-vidro", "inicio": 23.9, "fim": 28.75,
    "sobre": [ { "tipo": "look", "efeito": "holograma", "alvo": "pessoa", "t": 23.95, "ate": 26.3 },
               { "tipo": "look", "efeito": "noir", "cor": "destaque", "t": 26.35, "ate": 28.75 } ] }
]
```
