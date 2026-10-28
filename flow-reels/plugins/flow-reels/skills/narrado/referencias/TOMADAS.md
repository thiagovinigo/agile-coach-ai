# O plano das tomadas (`tomadas.json`)

O `compor_narrado.py` não tem nenhum tempo escrito dentro dele: tudo sai deste arquivo e do relógio
da voz. O modelo inteiro está em `modelos/tomadas.exemplo.json`. Ele mora em
`projetos/<nome>/materiais-de-trabalho/narrado-NN/tomadas.json`.

## Instantes

Todo campo de instante aceita quatro formas:

| forma | exemplo | quer dizer |
|---|---|---|
| segundos | `12.4` | o segundo 12,4 da linha do tempo final |
| uma palavra | `"planilha"` | o começo da primeira vez que a voz diz "planilha" depois do começo da tomada |
| uma sequência | `"você escreve"` | o começo da sequência, para desempatar palavra repetida |
| objeto | `{"palavra": "isso", "ocorrencia": 2, "ajuste": -0.1}` | a segunda ocorrência, 0,1 s antes |

A comparação ignora maiúscula, acento e pontuação. Palavra que não aparece na fala para o script com o
nome da tomada. A fala de referência é `construcao/linha_do_tempo.json`, campo `palavras`.

Cada campo já tem um ajuste padrão: a tomada entra 0,12 s antes da palavra, o empurrão começa 0,15 s
antes, o anel começa na palavra.

## Nível de cima

| campo | o que é |
|---|---|
| `titulo` | nome curto do reel. Vai para a página de revisão |
| `palavra_chave` | a PALAVRA do comentário, em caixa alta e sem acento |
| `fonte_padrao` | a filmagem usada quando a tomada não diz outra (caminho relativo ao projeto) |
| `credito_padrao` | o crédito de toda tomada que não diz outro |
| `voz.take` | a tomada de voz escolhida, por exemplo `"a-respiro"` |
| `trilha` | opcional. Só quando o som da filmagem é o produto (abaixo) |
| `respiro_som` | ar entre a voz e um trecho com som, em s (padrão 0,30) |
| `abertura`, `tomadas`, `fechamento`, `legenda` | abaixo |

## `abertura`

| campo | o que é |
|---|---|
| `titulo` | o título desenhado. Curto, a versão de leitura do gancho. Sem travessão |
| `destaque` | a palavra do título que sai na cor de destaque. Uma só |
| `ate` | a palavra que fecha a frase do gancho. O cartão sai 0,25 s depois do fim dela, e a legenda começa ali |
| `kicker` | o texto da pílula, curto, em caixa alta |
| `logo` | o arquivo do logo oficial, do acervo (`componentes/logos/<marca>.svg`) ou do projeto |
| `logo_monocromatico` | `true` para a silhueta do acervo (padrão em `.svg`), `false` para PNG colorido oficial |
| `topo` | y da pílula (padrão 190) |

As palavras do título entram no instante em que a voz diz cada uma. Palavra do título que a voz não
diz (ou diz em outra ordem) entra entre as vizinhas.

## `tomadas`, uma por trecho de filmagem

| campo | o que é |
|---|---|
| `id` | nome curto, `t01`, `t02`. Aparece nas folhas de contato |
| `inicio` | quando a tomada entra. A primeira é sempre 0. As outras, quase sempre uma palavra |
| `fonte` | a filmagem, se não for a `fonte_padrao` |
| `entrada` | o segundo da fonte em que a tomada começa. Ela corre em velocidade real dali |
| `saida` | opcional: o segundo da fonte que a tomada não pode passar (o compor avisa se passar) |
| `recorte` | `[x, y, largura, altura]` em pixels da fonte: a parte da fonte que enche a largura. Tira faixa promocional, borda, tela vazia. Sem ele, a fonte inteira |
| `tela_cheia` | `true` para filmagem vertical ocupar o quadro inteiro. Automático quando o recorte é vertical |
| `centro_y` | o centro vertical da filmagem na tela (padrão 815). Fica entre y 160 e a faixa da legenda |
| `transicao` | como esta tomada chega: `desfoque` (padrão), `zoom` ou `corte` |
| `duracao_transicao` | de 0,30 a 0,42 s (padrão 0,36) |
| `empurrao` | um objeto ou uma lista: `{"alvo": [x, y, l, a], "inicio": "palavra", "duracao": 1.0, "margem": 0.25}`. O alvo é em pixels da fonte; a câmera termina com ele no centro, com a margem em volta |
| `anel` | um objeto ou uma lista: `{"caixa": [x, y, l, a], "palavra": "palavra", "duracao": 0.45}`. A caixa é em pixels da fonte e acompanha o empurrão |
| `cartas` | lista de prints reais para o resumo em leque: caminho, ou `{"imagem": "...", "inicio": "palavra"}` |
| `escurecer` | de 0 a 1, quanto a filmagem escurece por baixo (padrão 0, e 0,4 quando há cartas) |
| `credito` | o texto do chip desta tomada. `false` tira o crédito (só quando a tomada não tem filmagem de terceiros) |
| `som` | o nome de um trecho `som` da `trilha`: a tomada vira aquele trecho, com o som dele |

Para achar as coordenadas: a folha de contato da fonte (`conferir.py --folha-da-fonte`) tem régua a
cada 200 px da fonte. Para precisão, extraia o quadro com ffmpeg e olhe.

Uma tomada dura até a próxima começar, mais a transição de saída. A fonte precisa cobrir isso a partir
da `entrada`, senão o fim congela.

## `trilha`, só quando o som é o produto

Sem `trilha`, a voz corre inteira e toda filmagem é muda. Com ela, a voz é partida em pedaços e
trechos da filmagem tocam com o som deles entre os pedaços:

```json
"trilha": [
  {"tipo": "voz", "ate": "isso."},
  {"tipo": "som", "nome": "demo", "fonte": "materiais-de-trabalho/fonte/filme.mp4", "entrada": 10.85, "saida": 16.85},
  {"tipo": "voz", "ate": "FIM"}
]
```

`ate` é a palavra que fecha aquele pedaço da voz. Um trecho `som` pode ter `"pecas": [[a, b], [c, d]]`
para pular o meio. Cada ponto de corte cai num silêncio (`linha_do_tempo.py --energia`); o script avisa
quando não cai. Na lista de `tomadas`, a tomada que mostra o trecho leva `"som": "demo"` e herda o
começo e a fonte dele.

## `fechamento`

| campo | o que é |
|---|---|
| `inicio` | a palavra em que a caixa de comentário sobe, quase sempre "Comenta" |
| `palavra` | a PALAVRA, em caixa alta. É digitada a partir do instante em que a voz diz ela |
| `item` | o nome curto do que chega na DM. Sem travessão |
| `item_palavra` | opcional: a palavra em que o item voa para a DM (padrão: logo depois do envio) |
| `cauda` | quanto o reel segura depois da última palavra, em s (padrão 1,2) |
| `por_letra`, `campo`, `rotulo_dm` | opcionais: velocidade da digitação, o texto da caixa vazia e o rótulo do balão |

## `legenda`

| campo | o que é |
|---|---|
| `destaques` | palavras que saem na cor de destaque na legenda, além da PALAVRA. Uma por grupo no máximo |
