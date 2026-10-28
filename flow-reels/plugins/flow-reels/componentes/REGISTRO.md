# Registro de componentes

A biblioteca de peças do painel. Ela existe por um motivo só: a qualidade do corte não pode oscilar
entre uma rodada e outra. O painel é autorado toda vez, mas as peças de que ele é feito são sempre as
mesmas, já obedecendo `marca/tokens.json` e a lei de `PADRAO-VISUAL.md`.

Este arquivo é o **contrato**. Ele diz para que cada peça serve, o que ela lê, o que ela aceita e em
que estado ela começa e termina. A implementação em HTML de cada uma vive no arquivo ao lado.

| peça | arquivo | papel |
|---|---|---|
| caixa-de-comando | `caixa-de-comando.html` | terminal, prompt, campo de comando |
| chip-numerado | `chip-numerado.html` | passo, etapa, contagem |
| card | `card.html` | bloco de conteúdo, item comparado |
| seta | `seta.html` | ligação e direção entre duas coisas |
| cronometro | `cronometro.html` | tempo decorrido ou tempo economizado |
| barra-de-progresso | `barra-de-progresso.html` | proporção, avanço, parte de um todo |
| tile-de-logo | `tile-de-logo.html` | uma ferramenta ou marca como objeto físico, sempre com o logo de verdade de `logos/` |
| rotulo | `rotulo.html` | etiqueta curta em caixa alta |
| titulo-de-painel | `titulo-de-painel.html` | a manchete do painel |
| dock-de-apps | `dock-de-apps.html` | um conjunto de ferramentas como a barra de aplicativos da máquina |
| campo-de-proximidade | `campo-de-proximidade.html` | um punhado de ferramentas espalhadas, e o alcance passando por elas |
| tela-de-conversa | `tela-de-conversa.html` | mock de conversa: celular ou janela com balões alternados |
| janela-de-navegador | `janela-de-navegador.html` | mock de navegador: aba, barra de endereço e página |
| campo-de-busca | `campo-de-busca.html` | mock de busca: campo com a consulta e os resultados |
| lista-de-itens | `lista-de-itens.html` | mock de lista: linhas com ícone, título e meta |
| janela-de-app | `janela-de-app.html` | mock de programa: barra lateral e área de conteúdo |
| card-de-post | `card-de-post.html` | mock de publicação: avatar, autor, corpo e engajamento |
| glifo-que-transforma | `glifo-que-transforma.html` | ideia abstrata: uma silhueta só que vira muitas |

---

## Convenção comum

### 1. O formato do arquivo

Cada peça é **um arquivo HTML** em `componentes/`, com exatamente um `<style>` e um `<script>`, e
nenhuma marcação solta no topo. O montador do painel lê o arquivo inteiro e injeta dentro do
`painel.html` antes de renderizar. Não existe importação por rede, nem CDN, nem build. O render tem
que funcionar com a máquina desconectada.

### 2. O registro

O `<script>` da peça termina registrando uma fábrica:

```js
FC.registrar("card", function (parametros) {
  // monta o DOM da peça
  return {
    el,                 // HTMLElement raiz, obrigatório
    definir(estado),    // aplica um estado instantaneamente, obrigatório
    medir()             // devolve { largura, altura } em pixels, obrigatório
  };
});
```

O painel cria instâncias com `FC.criar("card", { titulo: "...", ... })`, que devolve a instância já
embrulhada em um **palco**: um elemento de posicionamento que o painel move, e que a peça não conhece.

### 3. Como os tokens chegam

**Nenhuma peça lê `marca/tokens.json`.** O montador converte os tokens em variáveis de CSS no `:root`
e em um objeto `FC.tokens` para quando o valor precisa ser usado em conta. A peça usa só isto:

| variável de CSS | de onde vem |
|---|---|
| `--superficie`, `--superficie-alt` | `cores.superficie`, `cores.superficie_alt` |
| `--tinta`, `--tinta-suave` | `cores.tinta`, `cores.tinta_suave` |
| `--destaque`, `--destaque-contraste` | `cores.destaque`, `cores.destaque_contraste` |
| `--fonte-titulo`, `--fonte-corpo`, `--fonte-mono` | `fontes.*.familia`, já com `@font-face` declarado |
| `--tam-titulo`, `--tam-rotulo`, `--tam-corpo` | `tipografia.*`, em px |
| `--entrelinha`, `--espacamento-rotulo` | `tipografia.entrelinha`, `tipografia.espacamento_rotulo` |
| `--raio`, `--borda`, `--traco` | `forma.raio_canto`, `forma.espessura_borda`, `forma.espessura_traco` |

Valor hexadecimal escrito direto dentro de uma peça é defeito, sem exceção. Se a peça precisa de uma
cor que não está na lista, a lista está certa e a peça está errada.

### 4. A função obrigatória `window.render(t)`

O painel é renderizado quadro a quadro por um navegador sem tela. O renderizador não deixa o tempo
correr: ele pede um instante, tira a foto, pede o próximo. Por isso o `painel.html` **precisa**
expor três coisas:

```js
window.DURACAO = 28.4;   // duração do painel em segundos
window.PRONTO  = false;  // vira true quando fontes e imagens terminaram de carregar
window.render  = function (t) { /* desenha o estado do mundo no segundo t */ };
```

O renderizador espera `window.PRONTO` virar true e então chama `render(t)` para
`t = 0, 1/12, 2/12, 3/12, ...` até `DURACAO`, capturando um quadro depois de cada chamada.

Regras duras da `render(t)`:

- **É pura.** Chamar `render(3.5)` duas vezes tem que dar exatamente o mesmo pixel. Ela desenha o
  estado do instante, não aplica uma mudança em cima do anterior.
- **Não depende de ordem.** O renderizador pode pedir os instantes fora de sequência, ou repetir um.
- **Não usa `setTimeout`, `setInterval`, `requestAnimationFrame` nem `Math.random()` sem semente.**
  Nada de relógio próprio: o único relógio é o `t` que chega por parâmetro.
- **Não usa `transition` nem `@keyframes` de CSS.** Transição de CSS não roda entre capturas, e o
  resultado seria um painel completamente parado. Todo movimento é conta feita dentro da `render`.
- **Nenhuma peça anima a si mesma.** A peça sabe desenhar o estado dela agora. O movimento é do palco,
  e quem decide é a `render`.

### 5. Os ajudantes de movimento

O movimento sai dos números de `PADRAO-VISUAL.md` e já vem pronto em `FC`. O painel não recalcula
curva na mão:

```js
FC.chegada(t, t0)        // 800 ms, sobe 64 px, opacidade cheia no 1º quadro, escala 1
                         // devolve { visivel, y, opacidade }
FC.escalonar(t, t0, i)   // mesma chegada, atrasada em 200 ms por irmão: FC.chegada(t, t0 + 0.2 * i)
FC.refluxo(t, t0)        // 667 ms, devolve p de 0 a 1 para interpolar posições do grupo inteiro
FC.wipe(t, t0)           // 167 ms, devolve p de 0 a 1 para a máscara de saída
FC.aplicar(peca, estilo) // joga { y, opacidade, visivel } no palco da peça
```

Antes de `t0` a peça fica com `display: none`, não com opacidade 0. Elemento invisível mas presente
ainda empurra layout.

### 6. O grão

O grão não é peça e não se declara. Nenhuma peça desenha textura própria.

**Quem aplica é o `FC.montarPainel` do `base.js`, dentro do navegador**, chamando `FC.grao(painel)`
e lendo `textura.grao_intensidade`. Ou seja, o grão já está queimado nos quadros que o `painel.py`
captura, e chega ao MP4 por ali.

> **Não adicione grão no `montar.py`.** A frase antiga aqui dizia "o montador coloca a camada por
> cima de tudo", e mais de um leitor entendeu que era o `montar.py`, concluiu que ele estava
> quebrado e foi consertar. Seria um estrago: o painel ficaria com grão dobrado e a face, que é
> filmagem real e já tem ruído próprio, ganharia uma textura sintética por cima. Medido num quadro
> entregue: o painel tem 3,0 níveis de ruído de alta frequência numa região chapada, que é o grão
> funcionando. Se você suspeitar que sumiu, meça antes de consertar.

### 7. Marca só entra com o logo de verdade

**Regra dura, sem exceção.** Quando o painel mostra uma marca, ele mostra o logo real dela. Nunca uma
forma parecida, nunca uma aproximação desenhada na hora, nunca um ícone genérico fazendo as vezes de
uma marca nomeada. Vale para logo, símbolo e marca nominativa, e vale em qualquer peça, não só no
tile.

Por que a regra é dura: um logo aproximado é pior do que logo nenhum. Quem conhece a marca vê o erro
no primeiro segundo e desconta a credibilidade do vídeo inteiro, e quem não conhece sai de lá tendo
aprendido uma coisa errada. Foi isso que aconteceu de verdade em um lote: o painel desenhou uma forma
parecida com o logo do Claude, e outra com a do Instagram, e nenhuma das duas era o logo.

Como cumprir:

1. o acervo fica em `componentes/logos/`, e o `tile-de-logo` chega nele pelo parâmetro `marca`;
2. faltou a marca no acervo, baixe: `flow-reels componentes/baixar-logo <marca>`;
3. a marca não existe na fonte, pegue o logo oficial na página de imprensa dela e salve na pasta;
4. **não deu para conseguir o arquivo, tire a marca do beat e resolva com palavra.** Escrever o nome
   da ferramenta é uma saída honesta. Desenhar o logo dela não é.

Nenhuma peça inventa marca para tapar buraco, e nenhuma peça esconde a falta em silêncio: o que falta
aparece no quadro e no console. As regras do acervo, a licença e o que fazer com logo colorido estão
em `componentes/logos/README.md`.

---

## As peças

### caixa-de-comando

**Serve para:** mostrar um comando, um prompt, um trecho de terminal ou uma resposta de máquina. É a
peça mais usada como objeto herói quando a fala é sobre fazer alguma coisa.

**Tokens que lê:** `--superficie-alt` (fundo), `--borda`, `--raio`, `--fonte-mono`, `--tam-corpo`,
`--tinta` (linha de comando), `--tinta-suave` (linha de saída), `--destaque` (cursor e linha apontada).

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `titulo` | texto ou null | `null` | rótulo na barra de cima da caixa. Sem título, a caixa não tem barra |
| `linhas` | lista de `{ texto, tipo }` | obrigatório | `tipo` é `"comando"`, `"saida"` ou `"erro"` |
| `largura` | `"cheia"` ou número em px | `"cheia"` | `"cheia"` ocupa os 968 px úteis |
| `cursor` | booleano | `true` | mostra o bloco de cursor no fim da última linha visível |

**Estados:** `definir({ linhas_visiveis, caracteres, destaque })`. `caracteres` é quantos caracteres da
última linha visível já foram digitados, e é assim que se faz a digitação sem animação própria.
`destaque` é o índice da linha que recebe a cor de acento, ou `null`.

- **inicial:** `{ linhas_visiveis: 0, caracteres: 0, destaque: null }`, a caixa vazia com a barra e o
  cursor piscando em nenhum lugar, só parado.
- **final:** `{ linhas_visiveis: linhas.length, caracteres: -1, destaque: null }`, tudo escrito. O
  valor `-1` em `caracteres` significa linha completa.

---

### chip-numerado

**Serve para:** marcar passo, etapa, posição em uma contagem. Anda em grupo de dois a quatro, um por
passo, e é o jeito canônico de mostrar "primeiro isso, depois aquilo" sem virar lista de texto.

**Tokens que lê:** `--tinta-suave` (apagado), `--destaque` e `--destaque-contraste` (aceso),
`--fonte-titulo`, `--raio`, `--borda`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `numero` | inteiro | obrigatório | o que aparece dentro |
| `texto` | texto ou null | `null` | rótulo curto ao lado do número, no máximo 3 palavras |
| `tamanho` | `"p"` ou `"g"` | `"g"` | `"p"` tem 72 px de diâmetro, `"g"` tem 112 px |

**Estados:** `definir({ estado })`, com `"apagado"`, `"aceso"` ou `"concluido"`.

- **inicial:** `"apagado"`, contorno em tinta_suave e número em tinta_suave.
- **final:** `"concluido"`, contorno em tinta_suave, número trocado por um traço de confirmação.
- No meio, `"aceso"`: preenchimento em destaque e número em destaque_contraste. Só um chip do grupo
  fica aceso por vez, porque o acento é único.

---

### card

**Serve para:** um bloco de conteúdo. É o recipiente genérico, usado sozinho como herói ou em grupo de
dois ou três para comparar.

**Tokens que lê:** `--superficie-alt`, `--borda`, `--raio`, `--tinta`, `--tinta-suave`, `--destaque`,
`--fonte-titulo`, `--fonte-corpo`, `--tam-titulo`, `--tam-corpo`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `titulo` | texto | obrigatório | no máximo 5 palavras |
| `corpo` | texto ou null | `null` | no máximo duas frases curtas. Card não é parágrafo |
| `icone` | caminho local ou null | `null` | arquivo em `marca/` ou `componentes/icones/` |
| `largura` | número em px | `968` | em grupo de três, 304 cada, com 28 de intervalo |
| `alinhamento` | `"esquerda"` ou `"centro"` | `"esquerda"` | |

**Estados:** `definir({ estado })`, com `"neutro"`, `"destacado"`, `"apagado"` ou `"riscado"`.

- **inicial:** `"neutro"`, fundo superficie_alt, título em tinta, corpo em tinta_suave.
- **final:** depende do papel no beat. `"destacado"` põe a borda e o título em destaque, e é o estado
  que responde à fala. `"apagado"` baixa o card para tinta_suave inteiro, e serve para deixar o
  destaque de outro card respirar. `"riscado"` risca o título, para a opção descartada.

---

### seta

**Serve para:** ligar duas coisas e dizer a direção. É como o painel mostra causa, consequência e
caminho sem escrever a palavra.

**Tokens que lê:** `--traco`, `--tinta-suave` (padrão), `--destaque` (quando é ela que a fala aponta).

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `de` | `[x, y]` ou id de uma peça | obrigatório | com id, ela gruda na borda da peça e acompanha o re-fluxo |
| `para` | `[x, y]` ou id de uma peça | obrigatório | |
| `curvatura` | número de -1 a 1 | `0` | `0` é reta, valores maiores arqueiam para um lado |
| `ponta` | `"simples"`, `"dupla"` ou `"nenhuma"` | `"simples"` | |

**Estados:** `definir({ desenhada, cor })`, com `desenhada` de 0 a 1.

- **inicial:** `{ desenhada: 0 }`, ou seja nada na tela.
- **final:** `{ desenhada: 1 }`, o traço inteiro com a ponta desenhada por último.
- A seta se desenha uma vez e fica. Ela nunca fica correndo em loop, e nunca tem traço pontilhado se
  mexendo, que é animação perpétua disfarçada.

---

### cronometro

**Serve para:** tempo. O tempo que uma coisa levava, o tempo que passou a levar, o tempo que sobrou. É
a peça que traduz "muito mais rápido" em uma coisa que se vê.

**Tokens que lê:** `--fonte-titulo`, `--tam-titulo`, `--tinta`, `--destaque`, `--tinta-suave`,
`--traco`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `de` | número em segundos | obrigatório | o valor inicial |
| `para` | número em segundos | obrigatório | o valor final. Pode ser menor que `de`, e aí ele desce |
| `formato` | `"mm:ss"`, `"s"` ou `"min"` | `"mm:ss"` | como o número é escrito |
| `rotulo` | texto ou null | `null` | aparece embaixo, no tamanho de rótulo |
| `anel` | booleano | `true` | desenha o anel em volta, que se preenche junto com o número |

**Estados:** `definir({ valor })`, em segundos. Quem faz o número andar é a `render(t)`, interpolando
entre `de` e `para` no intervalo do beat.

- **inicial:** `{ valor: de }`, parado.
- **final:** `{ valor: para }`, parado.
- O cronômetro só corre durante a frase que fala dele. Acabou a frase, ele para no valor final. Um
  cronômetro correndo o corte inteiro é animação perpétua e está proibido.

---

### barra-de-progresso

**Serve para:** proporção e avanço. Quanto de um todo, quanto já foi, quanto sobrou.

**Tokens que lê:** `--superficie-alt` (trilho), `--destaque` (preenchimento), `--tinta` (número),
`--tinta-suave` (rótulo), `--raio`, `--traco`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `valor` | número de 0 a 1 | `0` | o valor de chegada |
| `rotulo` | texto ou null | `null` | à esquerda, em tamanho de rótulo |
| `mostrar_numero` | booleano | `true` | mostra a porcentagem à direita |
| `segmentos` | inteiro ou null | `null` | com um número, a barra vira blocos em vez de trilho contínuo |
| `altura` | número em px | `24` | |

**Estados:** `definir({ valor })`.

- **inicial:** `{ valor: 0 }`, só o trilho.
- **final:** `{ valor: valor }`. O preenchimento acompanha a curva de chegada, e o número escrito anda
  junto com o preenchimento, nunca depois.

---

### tile-de-logo

**Serve para:** transformar uma ferramenta, um aplicativo ou uma marca em objeto físico dentro do
mundo. É o que substitui escrever o nome da coisa. Vale a regra da seção 7 das convenções: a marca
entra com o logo de verdade ou não entra.

**De onde vem a imagem:** do acervo em `componentes/logos/`, que é um conjunto de SVG de marca
baixados do Simple Icons. O parâmetro `marca` é o nome do arquivo de lá sem a extensão, e o caminho
`logos/<marca>.svg` é resolvido pelo servidor do `painel.py`, que serve a pasta do corte, a raiz do
pacote e a pasta `componentes` como se fossem uma só. Um corte que precise de um logo só dele pode
ter uma pasta `logos/` ao lado do próprio `painel.html`, e ela ganha. O que não existe é buscar
imagem na internet na hora do render.

**Tokens que lê:** `--superficie-alt` ou `--destaque` (fundo), `--tinta` e `--destaque-contraste`
(a silhueta), `--raio`, `--borda`, `--tinta-suave` (nome), `--tam-rotulo`, `--fonte-corpo`,
`--fonte-titulo` e `--fonte-mono` (só no aviso de falta), `--superficie` (só no aviso de falta).

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `marca` | nome de arquivo do acervo | um dos dois | `"claude"` resolve `logos/claude.svg`, a silhueta de uma cor |
| `imagem` | caminho local | um dos dois | o logo colorido oficial que você mesmo colocou na pasta |
| `nome` | texto ou null | `null` | aparece embaixo do tile |
| `tamanho` | número em px | `200` | o lado do quadrado |
| `fundo` | `"alt"` ou `"destaque"` | `"alt"` | `"destaque"` só para o tile que a fala aponta agora |

`marca` e `imagem` são exclusivos: um dos dois é obrigatório, e passar os dois é erro, porque só um
deles pode dizer que imagem entra. Sem nenhum dos dois a peça também recusa, com a mensagem dizendo
qual usar. Nenhum dos dois casos tem desenho de reserva.

**`marca` ou `imagem`, como escolher:** o acervo é **monocromático**, uma silhueta de uma cor só, e
o tile pinta essa silhueta com a tinta do painel. Isso não é recolorir marca: o arquivo já vem sem
cor de marca nenhuma, e é assim que a peça mantém contraste no fundo claro e no escuro. A silhueta
basta quando a marca serve para reconhecer a ferramenta, que é a esmagadora maioria dos beats. Ela
**não** basta quando a cor é parte do que está sendo dito, por exemplo um beat sobre a identidade da
marca, ou duas marcas de silhueta parecida que só a cor separa. Aí você baixa o logo colorido
oficial na página de imprensa da marca, salva em `componentes/logos/` e usa `imagem`. Com `imagem` o
arquivo entra como ele é: nunca recolorido, nunca com a cor de destaque por cima, nunca invertido.

**Estados:** `definir({ estado })`, com `"apagado"`, `"neutro"` ou `"aceso"`.

- **inicial:** `"apagado"`, o quadrado com a superfície e sem a marca.
- **final:** `"neutro"`, a marca visível em cima da superfície alternativa, na cor de tinta.
- `"aceso"` troca o fundo para destaque e a silhueta para a cor de contraste, e vale um tile por vez.
- Logo colorido oficial não muda de cor em estado nenhum. Quem muda é o fundo do tile.

**Quando o arquivo não existe:** a peça **não** cai em desenho genérico e **não** fica só invisível,
que seria pior ainda, porque o corte sairia mudo naquele ponto sem ninguém perceber. Ela faz três
coisas ao mesmo tempo:

1. pinta o quadro hachurado na cor de destaque, com borda tracejada, escreve LOGO AUSENTE e o
   caminho que faltou, e troca o nome de baixo pelo comando que resolve;
2. chama `console.error`, que o `painel.py` coleta e imprime no fim do render;
3. registra o caminho em `FC.logosAusentes`, para quem quiser conferir por código.

A falta é feia de propósito. Quem está produzindo tem que topar com ela antes do público.

---

### rotulo

**Serve para:** nomear uma coisa em duas ou três palavras. Unidade, categoria, nome de coluna, estado.
É a peça que impede o painel de escrever frase.

**Tokens que lê:** `--fonte-corpo`, `--tam-rotulo`, `--espacamento-rotulo`, `--tinta-suave`, `--tinta`,
`--destaque`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `texto` | texto | obrigatório | vai para caixa alta sozinho. No máximo 3 palavras |
| `cor` | `"suave"`, `"tinta"` ou `"destaque"` | `"suave"` | |
| `alinhamento` | `"esquerda"`, `"centro"` ou `"direita"` | `"esquerda"` | |
| `pilula` | booleano | `false` | com `true`, ganha um fundo arredondado em superficie_alt |

**Estados:** `definir({ cor })`. O texto não muda depois de criado: rótulo que troca de texto é rótulo
errado, use dois rótulos e faça um sair.

- **inicial:** `"suave"`.
- **final:** `"suave"` de volta, depois de ter passado por `"destaque"` no beat em que a fala o
  apontou.

---

### titulo-de-painel

**Serve para:** a manchete do painel. Uma por painel, no máximo duas no corte inteiro.

**Tokens que lê:** `--fonte-titulo`, `--tam-titulo`, `--entrelinha`, `--tinta`, `--destaque`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `texto` | texto | obrigatório | no máximo 6 palavras. Se não couber em duas linhas de 968 px, está longo |
| `destaque_em` | texto ou null | `null` | o trecho exato do texto que recebe a cor de acento |
| `alinhamento` | `"esquerda"` ou `"centro"` | `"esquerda"` | |

**Estados:** `definir({ marcado })`, booleano.

- **inicial:** `{ marcado: false }`, o texto inteiro em tinta.
- **final:** `{ marcado: true }`, o trecho de `destaque_em` em cor de acento e o resto em tinta.
- O título **não** repete a frase que está na legenda. Ele nomeia o assunto, a legenda carrega a fala.
  Título que ecoa a legenda é defeito de painel, não de legenda.

---

## A dupla do ponteiro

Duas peças em que a fala não é sobre UMA ferramenta, é sobre um CONJUNTO delas, e em que quem
escolhe é um ponteiro passando. Elas vieram de uma mesma conta: a escala de cada marca é função da
distância até o ponteiro, e nada mais. Escolher entre as duas:

- **dock-de-apps** quando a ideia é **largura numa superfície familiar**: são as ferramentas que a
  máquina tem, enfileiradas numa barra só. A leitura é instantânea, antes da legenda.
- **campo-de-proximidade** quando a ideia é **um punhado espalhado que alguém alcança**: as
  ferramentas não formam uma barra, elas estão soltas, e o que importa é o alcance chegando nelas.

O que vale para as duas:

1. **Nenhuma das duas tem relógio.** A peça sabe desenhar o estado de agora, e quem passeia o
   ponteiro é a `render(t)` do painel. Em cada uma, o passeio é uma linha só: interpolar o estado
   `ponteiro` (ou `x` e `y`) entre paradas, com `FC.curva` e `FC.interpolar`. Isso é o que as
   mantém puras e é o que deixa o `painel.py` pedir os instantes fora de ordem.
2. **O valor delas é a onda, não o piscar.** O que faz a peça valer é o vizinho crescer um pouco
   quando o ponteiro está perto, e a fileira inteira se reacomodar junto. Se a sua versão parecer um
   ícone acendendo sozinho, alguma coisa quebrou a queda suave e a peça perdeu o que ela tinha.
3. **Elas não são animação perpétua.** O ponteiro passeia durante a frase que fala do conjunto e
   para no fim dela, com `intensidade` voltando a 0. Um dock ondulando o corte inteiro é exatamente
   a preguiça que a seção 5 do `PADRAO-VISUAL.md` proíbe.
4. **Marca é sempre o arquivo de verdade.** As duas resolvem `logos/<marca>.svg` pelo mesmo
   mecanismo do `tile-de-logo`: máscara para a silhueta receber a tinta do painel, sentinela para
   segurar o `window.PRONTO`, e, faltando o arquivo, o buraco hachurado no quadro mais
   `console.error` mais o caminho em `FC.logosAusentes`. No tamanho de ícone não cabe o texto do
   aviso, então no quadro aparece só a hachura, e o caminho que falta vai para o console.
5. **Cada uma tem um teto, e ela avisa.** O teto sai da lei do preenchimento: mais marcas do que
   cabe não é uma peça apertada, é um beat que quer dizer duas coisas. Pedindo mais do que o teto, a
   peça escreve no console quantas ficaram de fora e desenha só as que cabem.
6. **O ponteiro é móvel de interface, não marca.** Ele é desenhado em traço, com a tinta do painel,
   pela regra 3 da família de mocks. Vale desligar com `ponteiro: false` quando o beat é o conjunto
   e não alguém escolhendo.

---

### dock-de-apps

**Serve para:** um conjunto de ferramentas, aplicativos ou integrações mostrado como uma superfície
só, a barra de aplicativos da máquina. É a peça de quando a fala diz "tudo isso ele alcança": a
largura é o argumento, e a barra entrega isso sem legenda. Serve também para o beat de estreitar,
"e ele escolhe este aqui", com o ponteiro parando em um ícone e o `destaque` acendendo o ponto dele.

**Não serve para** uma marca sozinha, que é `tile-de-logo`, nem quando as ferramentas precisam de
rótulo, estado ou hierarquia, que é `lista-de-itens`.

**Tokens que lê:** `--superficie-alt` (a barra), `--tinta-suave` (borda da barra e ponto em repouso),
`--tinta` (a silhueta da marca e o ponteiro), `--destaque` (o ponto do aplicativo apontado e a
hachura da falta), `--superficie` (contorno do ponteiro e fundo da falta), `--raio`, `--borda`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `apps` | lista de `{ marca, ativo }` | obrigatório | de dois a seis. `marca` é o nome do arquivo do acervo sem a extensão; `ativo: true` põe o ponto embaixo do ícone |
| `ponteiro` | booleano | `true` | com `false` a peça não desenha o ponteiro, e só a onda conta a história |

**Estados:** `definir({ ponteiro, intensidade, destaque })`. `ponteiro` vai de 0 a 1 e é a posição ao
longo da fileira, do centro do primeiro ícone ao centro do último; `null` é ponteiro nenhum.
`intensidade` vai de 0 a 1 e é o quanto do efeito está ligado, e serve para o dock acordar e voltar
a dormir sem o ponteiro ter que sair de cena. `destaque` é o índice do aplicativo cujo ponto recebe
a cor de acento, ou `null`, e vale um por vez.

- **inicial:** `{ ponteiro: null, intensidade: 0, destaque: null }`, a barra plana e centrada, sem
  ponteiro.
- **final:** o mesmo repouso. O dock acorda durante a frase que fala dele e volta a dormir depois.
- A ampliação é uma **queda de cosseno**: o ícone sob o ponteiro cresce, o vizinho cresce menos e é
  empurrado para o lado pelo seno, e os de fora do alcance levam um empurrão constante. É essa conta
  que faz a fileira andar como líquido.
- A barra **abraça os ícones a cada quadro**: a posição e a largura dela saem do tamanho em que os
  ícones estão agora, então nenhum ícone fica boiando fora da superfície. A fileira também se
  recentra a cada quadro, então o florescimento fica simétrico e nunca corre para uma das beiras.

**O teto, e o porquê: seis aplicativos.** A conta é a da lei do preenchimento. Com os números da
peça (ícone de 74 px, vaga de 90, vaga no pico de 152, respiro de 30), a barra em repouso mede 584 px
e no pico do florescimento mede 830, e os dois valores estão dentro da faixa do herói, de 580 a 870.
O sétimo aplicativo levaria o pico a mais de 900 e estouraria. Pedindo mais de seis, a peça escreve
no console quantos ficaram de fora e desenha os seis primeiros.

**Medidas conferidas**, com a marca de exemplo, seis aplicativos, medidas **no quadro** renderizado
pelo `painel.py`, contando os pixels que diferem do fundo: repouso **584** px de largura, ponteiro
numa das pontas **674**, ponteiro no meio da fileira **830**. A caixa da peça é fixa em
**832 x 184**, e é ela que o `medir()` devolve: o florescimento anda dentro dessa caixa, então o
layout do painel não se mexe quando a onda passa.

---

### campo-de-proximidade

**Serve para:** um punhado de ferramentas espalhadas pelo painel, e o alcance de alguém passando por
elas. É a peça de quando a fala diz "ele chega em todas essas": o que está perto cresce, o que está
longe fica pequeno, e é isso que mostra o alcance sem escrever a palavra alcance.

**Não serve para** as mesmas coisas que o dock recusa, e também não serve quando o conjunto tem
ordem: constelação não tem primeiro nem último. Conjunto ordenado é `lista-de-itens`.

**Tokens que lê:** `--superficie-alt` (a pastilha), `--tinta-suave` (borda em repouso), `--tinta` (a
silhueta da marca e o ponteiro), `--destaque` (o contorno da pastilha alcançada e a hachura da
falta), `--superficie` (contorno do ponteiro e fundo da falta), `--traco` (a espessura do contorno
aceso), `--borda`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `marcas` | lista de `{ marca, x, y, inclinacao }` | obrigatório | de três a oito. `x` e `y` vão de 0 a 100 e são a posição no campo; `inclinacao` é uma inclinação pequena em graus, para a constelação não parecer grade |
| `largura` | número em px | `820` | |
| `altura` | número em px | `560` | |
| `ponteiro` | booleano | `true` | com `false` a peça não desenha o ponteiro |

**Estados:** `definir({ x, y, intensidade })`. `x` e `y` vão de 0 a 1 e são a posição do ponteiro
dentro do campo; faltando um dos dois, não há ponteiro e o campo fica em repouso. `intensidade` vai
de 0 a 1 e é o quanto do efeito está ligado.

- **inicial:** `{ x: null, y: null, intensidade: 0 }`, todas as pastilhas no tamanho de repouso.
- **final:** o mesmo repouso, depois que o passeio acabou.
- A escala cai por **distância radial**: cheia em cima do ponteiro, de volta ao repouso na borda do
  alcance de 250 px, com um suavizador tirando o bico da reta. É isso que faz o campo responder como
  onda em vez de degrau.
- **O acento é um só, e é a pastilha mais dentro do alcance**: ela troca o contorno para a cor de
  destaque, e só enquanto está mesmo dentro dele. Quem cresce passa por cima de quem ficou pequeno, e
  todo mundo passa por baixo do ponteiro.
- As posições são **encolhidas para dentro pelo raio da pastilha no pico**, não pelo de repouso.
  Assim a pastilha da beira continua inteira dentro do campo justamente no quadro em que ela é o
  assunto. Na prática, `x: 0` e `x: 100` são as duas beiras utilizáveis, e vale usá-las: uma
  constelação amontoada no meio desperdiça o campo.

**O teto, e o porquê: oito marcas.** No pico a pastilha vai de 84 px para 155, e com mais de oito
elas se encavalam no meio do passeio, que é justamente quando a peça precisava estar mais legível.
Pedindo mais de oito, a peça escreve no console quantas ficaram de fora e desenha as oito primeiras.

**Medidas conferidas**, com a marca de exemplo, oito marcas espalhadas de 5% a 96% nos dois eixos,
medidas **no quadro** renderizado pelo `painel.py`: a caixa dos pixels desenhados fica entre **682 e
691 px** de largura ao longo do passeio inteiro, dentro da faixa do herói. A caixa da peça é a
`largura` por `altura` pedida, **820 x 560** no padrão, e é ela que o `medir()` devolve: como as
posições já nascem encolhidas pelo raio do pico, nada cresce para fora dessa caixa.

---

## A família de mocks de interface

Seis peças que desenham a **forma** de uma interface. Elas existem porque o acervo só sabia fazer
retângulo com texto: pedindo um aplicativo de mensagem, o painel entregava um tile com a silhueta e
um card escrito o nome. O mock entrega a conversa.

O que vale para as seis, e é o que separa mock de card:

1. **Reconhecimento em meio segundo, no celular.** Quem bate o olho tem que pensar "isso é uma
   conversa", "isso é um navegador", antes de ler qualquer palavra. Quem carrega esse reconhecimento
   é forma, proporção e hierarquia, não detalhe: o canto redondo do aparelho e o balão com o bico
   cortado, a aba sobre a faixa escura e a pílula do endereço, a coluna estreita ao lado da área
   larga. Tirar um desses sinais devolve a peça ao retângulo.
2. **Marca é sempre o arquivo de verdade.** Toda peça daqui aceita `marca` no cabeçalho e resolve
   `logos/<marca>.svg` pelo mesmo mecanismo do `tile-de-logo`: máscara para a silhueta receber a
   tinta do painel, sentinela para segurar o `window.PRONTO`, e, faltando o arquivo, o buraco
   hachurado no quadro mais `console.error` mais o caminho em `FC.logosAusentes`. A regra 7 das
   convenções vale inteira: nenhum mock desenha marca.
3. **Glifo de sistema não é marca.** Lupa, cadeado, seta de voltar, coração, balão de comentário e
   glifo de documento são móveis da interface e são desenhados em traço, com a cor vindo de
   `currentColor`. Eles não identificam empresa nenhuma. O que identifica é o logo, e o logo vem de
   arquivo.
4. **Piso de 34 px.** Todo texto que existe para ser lido é `--tam-corpo` (o conteúdo) ou
   `--tam-rotulo` (a meta). Não existe terceiro degrau. Onde uma interface de verdade teria texto
   miúdo, o mock põe **barra**: a sugestão dentro da barra de escrever, as linhas da página do
   navegador. Barra é forma e não pede leitura.
5. **O mock é o objeto herói, e as seis nascem em 820 px.** Um mock e mais nada é o painel inteiro.
   Quem manda na largura é a lei do preenchimento, `PADRAO-VISUAL.md` seção 4: de 580 a 870 px dos
   968 úteis. O padrão de `largura` das seis peças é o mesmo número, 820, que dá 84,7% da largura
   útil e cai dentro da lei sem encostar no teto. Quem autora sem passar `largura` entrega um herói
   legal. Mexendo nesse valor, o limite continua sendo 870: acima disso a peça sai da lei, e abaixo
   de 580 ela vira miniatura.
6. **Nada se anima sozinho.** Os três pontos de "digitando" ficam parados, o cursor só existe
   enquanto alguém digita, o número de curtida sobe porque a `render(t)` mandou. A peça sabe
   desenhar o estado de agora e só.

**Medidas conferidas**, com a marca de exemplo (Quicksand), na largura padrão de 820 px, no painel
de 1080 x 956. A área útil é 968 x 636, de y = 150 a y = 786. Cada peça foi renderizada pelo
`painel.py --so-quadro` e medida **no quadro**, contando os pixels que diferem do fundo: as seis dão
820 px de largura no PNG, ou seja 84,7% dos 968 úteis. Trocando a fonte da marca, esses números
andam, então meça de novo antes de afirmar qualquer um deles:

| mock | tamanho medido da configuração de referência | sobra medida para o texto |
|---|---|---|
| `tela-de-conversa` | 820 x 617 (celular, três mensagens, uma delas em duas linhas, com a barra de escrever) | balão de 590 px, 534 px de texto dentro dele, cerca de 20 letras por linha |
| `janela-de-navegador` | 820 x 496 (`altura_tela` 280, manchete e três linhas) | 598 px de barra para a URL em mono, cerca de 30 letras; manchete com 708 px, cerca de 27 letras |
| `campo-de-busca` | 820 x 550 (cabeçalho com marca e três resultados) | consulta de 668 px, cerca de 26 letras; linha de resultado com 682 px sem meta, cerca de 26 letras |
| `lista-de-itens` | 820 x 576 (cabeçalho e três linhas com meta) | título de 580 px, cerca de 22 letras |
| `janela-de-app` | 820 x 589 (três seções, manchete e três blocos) | bloco de 434 px, cerca de 16 letras; manchete de 490 px, cerca de 19 letras |
| `card-de-post` | 820 x 468 (autor, corpo de três linhas e régua de engajamento) | corpo de 752 px por linha, cerca de 29 letras |

As contas de letra saem de uma medida só, o alfabeto minúsculo inteiro nas fontes da marca de
exemplo: 26 letras dão 666,9 px em `--tam-corpo`, ou 25,6 px por letra, 436,1 px em `--tam-rotulo`,
ou 16,8 px por letra, e 518,0 px em mono no tamanho de rótulo, ou 19,9 px por letra. Palavra real
varia: entre as frases medidas aqui, a mais econômica gastou 22,7 px por letra e a mais cara 27,4.
Por isso o número confiável é o de pixels, e a contagem de letras é estimativa: com texto de letras
largas, conte menos. Texto que passa do orçamento é cortado com reticências, e reticências no painel
é sinal de que a frase é longa demais para o corte, não de que a peça é estreita demais.

**Como medir de novo, sem cair na armadilha:** a fonte da marca entra por `@font-face`, e o navegador
faz o texto caber de um jeito antes de ela chegar e de outro depois. Lendo `getBoundingClientRect` no
mesmo instante em que a peça é criada, o valor que volta é o de antes, e ele mente para baixo: aqui
um balão de três linhas voltou como duas, e a peça inteira voltou 60 px mais baixa do que saiu no
quadro. Crie a peça, espere o layout assentar e só então meça, ou melhor ainda, renderize com o
`painel.py --so-quadro` e meça a caixa dos pixels no PNG. Quem manda é o quadro.

O bloco da `janela-de-app` é o mais apertado dos seis, e foi ele que mostrou o preço de baixar a
largura: "Legenda queimada" gasta 438,4 px, passa dos 434 px do bloco, quebra em duas linhas e faz a
peça inteira subir para 649 px, acima dos 636 da área útil. Por isso a configuração de referência
usa "Legenda no ar", de 328,9 px. Título que não cabe no bloco é título para encurtar, não largura
para aumentar.

---

### tela-de-conversa

**Serve para:** a conversa, em celular ou em janela. Aplicativo de mensagem, chat de uma ferramenta
de IA, atendimento. É o mock para quando a fala trata de alguém falando com alguém, ou com uma
máquina.

**Tokens que lê:** `--superficie-alt` (o aparelho), `--superficie` (balão recebido e barra de
escrever), `--tinta-suave` (bordas, avatar, alto-falante, glifos, balão enviado), `--tinta` (texto e
silhueta da marca), `--destaque` (balão apontado), `--raio` (canto do aparelho e do balão),
`--borda`, `--traco` (moldura do celular), `--fonte-titulo` (nome no alto), `--fonte-corpo`,
`--tam-corpo` (mensagens e nome), `--tam-rotulo` (a inicial no avatar), `--entrelinha`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `titulo` | texto | obrigatório | o nome no alto da conversa. Sem `marca`, a inicial dele vira o avatar |
| `mensagens` | lista de `{ texto, lado }` | obrigatório | `lado` é `"recebida"` (esquerda) ou `"enviada"` (direita) |
| `marca` | nome de arquivo do acervo ou null | `null` | o logo de verdade no cabeçalho, no lugar do avatar |
| `moldura` | `"celular"` ou `"janela"` | `"celular"` | celular ganha o alto-falante, a moldura grossa e o canto muito redondo |
| `largura` | número em px | `820` | |
| `altura` | número em px ou null | `null` | com altura fixa, as mensagens encostam embaixo e o mock não muda de tamanho quando um balão entra |
| `campo` | booleano | `true` | a barra de escrever no rodapé, com a seta de enviar |

**Estados:** `definir({ mensagens_visiveis, caracteres, digitando, destaque })`. `caracteres` é
quantas letras da última mensagem visível já foram escritas, e `-1` quer dizer a mensagem inteira.
`destaque` é o índice do balão que a fala aponta, ou `null`.

- **inicial:** `{ mensagens_visiveis: 0, caracteres: -1, digitando: false, destaque: null }`, o
  aparelho vazio, só com o cabeçalho e a barra de escrever.
- **final:** `{ mensagens_visiveis: mensagens.length, caracteres: -1, digitando: false, destaque: null }`,
  a conversa inteira em repouso.
- `digitando: true` acende o balão de três pontos no fim da conversa. Ele é um estado parado: não
  pisca, não pula, não respira.
- **O teto, medido com a marca de exemplo:** com a barra de escrever, três mensagens de uma linha
  dão 557 px e a quarta dá 667, que já passa dos 636 da área útil. Com `campo: false` cabem
  quatro, em 587 px, e a quinta dá 697. Mensagem que quebra em duas linhas custa mais uma linha
  de altura, então a conversa da configuração de referência, com uma delas em duas linhas, dá
  617 px. Passando disso, tire a barra de escrever antes de tirar a mensagem.

---

### janela-de-navegador

**Serve para:** a página. Repositório, site da ferramenta, documentação, a URL que a fala cita. É o
mock para quando o beat é "isso está publicado ali".

**Tokens que lê:** `--superficie-alt` (a janela e a aba ativa), `--superficie` (faixa das abas e a
página), `--tinta-suave` (bordas, setas, cadeado, aba fantasma, linhas de apoio), `--tinta` (título
da aba, URL, manchete, silhueta da marca), `--destaque` (o que está apontado e o cursor), `--raio`,
`--borda`, `--traco` (o risco embaixo da aba apontada), `--fonte-titulo` (manchete), `--fonte-corpo`,
`--fonte-mono` (a URL), `--tam-corpo` (manchete), `--tam-rotulo` (aba e URL), `--entrelinha`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `titulo` | texto | obrigatório | o nome escrito na aba |
| `endereco` | texto | obrigatório | a URL na barra. Escreva o endereço curto, sem protocolo |
| `marca` | nome de arquivo do acervo ou null | `null` | o ícone da aba e, com `conteudo` igual a `"logo"`, a marca grande no meio da página |
| `conteudo` | `"blocos"`, `"logo"` ou `"vazio"` | `"blocos"` | `"logo"` exige `marca` e recusa sem ela, porque marca não se desenha |
| `manchete` | texto ou null | `null` | o título da página, em `--tam-corpo` |
| `linhas` | inteiro | `3` | quantas barras de apoio a página tem |
| `largura` | número em px | `820` | |
| `altura_tela` | número em px | `300` | a altura da área de página |

**Estados:** `definir({ caracteres, carregada, destaque })`. `caracteres` é quantas letras da URL já
foram digitadas, e `-1` é a URL inteira. `destaque` é `"aba"`, `"endereco"`, `"tela"` ou `null`.

- **inicial:** `{ caracteres: 0, carregada: false, destaque: null }`, a janela montada, a barra vazia
  com o cursor e a página em branco.
- **final:** `{ caracteres: -1, carregada: true, destaque: null }`, endereço escrito e página no ar.
- O cursor só aparece enquanto `caracteres` é zero ou mais. URL pronta não tem cursor, senão sobraria
  um segundo ponto de acento aceso o corte inteiro.
- `carregada` é o evento que vale a pena: digitar o endereço e a página aparecer são dois beats, e
  dão o movimento sem que nada precise entrar em cena.

---

### campo-de-busca

**Serve para:** o momento de procurar. Busca em um site, busca dentro de um aplicativo, a consulta
que a fala cita. É o mock para quando o beat é uma pergunta sendo feita a um sistema.

**Tokens que lê:** `--superficie-alt` (a pílula do campo e a superfície dos resultados),
`--tinta-suave` (bordas, lupas, meta, botão), `--tinta` (consulta, nome, resultados, silhueta da
marca), `--destaque` (campo ou resultado apontado, e o cursor), `--raio`, `--borda`, `--traco` (o
risco na entrada do resultado apontado), `--fonte-titulo` (nome), `--fonte-corpo`, `--tam-corpo`
(consulta e resultado), `--tam-rotulo` (meta e botão), `--espacamento-rotulo`, `--entrelinha`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `consulta` | texto | obrigatório | o que está escrito no campo |
| `marca` | nome de arquivo do acervo ou null | `null` | o logo de verdade no cabeçalho, acima do campo |
| `titulo` | texto ou null | `null` | o nome do buscador ao lado da marca. Sem marca e sem título, não há cabeçalho |
| `resultados` | lista de textos ou de `{ texto, meta }` | `[]` | as linhas penduradas embaixo do campo. A meta come o texto da linha: sem ela sobram 682 px, e com uma meta de cinco letras, medida com `video`, sobram 543, cerca de 21 letras. Passou disso, a linha sai com reticências |
| `botao` | texto ou null | `null` | rótulo curto do botão dentro da pílula. Ele come 229 px do campo, medido com o rótulo `buscar`: a consulta cai de 668 px para 439, cerca de 17 letras |
| `largura` | número em px | `820` | |

**Estados:** `definir({ caracteres, resultados_visiveis, destaque })`. `caracteres` é quantas letras
da consulta já foram digitadas, e `-1` é a consulta inteira. `destaque` é `"campo"`, o índice de um
resultado, ou `null`.

- **inicial:** `{ caracteres: 0, resultados_visiveis: 0, destaque: null }`, a pílula vazia com o
  cursor e nenhum resultado.
- **final:** `{ caracteres: -1, resultados_visiveis: resultados.length, destaque: null }`, consulta
  escrita e resultados na tela.
- Os resultados entram em ordem, do primeiro para o último. Resultado que aparece no meio da lista
  não tem como sair, e a peça não tenta.

---

### lista-de-itens

**Serve para:** o conjunto. Caixa de entrada, pasta de arquivos, o que uma execução devolveu, os
passos de um resultado. É o mock para quando a fala diz "ele devolveu três coisas".

**Tokens que lê:** `--superficie-alt` (a lista), `--tinta-suave` (bordas, divisores, meta, cela do
ícone, confirmação), `--tinta` (título da linha, nome no cabeçalho, inicial, silhueta da marca),
`--destaque` (a linha apontada), `--raio`, `--borda`, `--traco` (o risco na entrada da linha
apontada), `--fonte-titulo` (nome no cabeçalho), `--fonte-corpo`, `--tam-corpo` (título da linha),
`--tam-rotulo` (meta, contagem, número e inicial), `--espacamento-rotulo`, `--entrelinha`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `itens` | lista de `{ titulo, meta, marca, inicial }` ou de textos | obrigatório | `marca` é o logo do acervo daquele item; `inicial` é uma letra quando não existe logo |
| `marca` | nome de arquivo do acervo ou null | `null` | o logo da lista inteira, no cabeçalho |
| `titulo` | texto ou null | `null` | o nome no cabeçalho. Sem marca e sem título, a lista não tem cabeçalho |
| `numerada` | booleano | `false` | a cela do ícone vira o número da posição, e o logo do item não entra |
| `contador` | booleano | `true` | mostra à direita do cabeçalho quantas linhas estão na tela |
| `largura` | número em px | `820` | |

**Estados:** `definir({ itens_visiveis, marcados, destaque })`. `marcados` é quantas primeiras linhas
aparecem com o sinal de confirmação. `destaque` é o índice da linha apontada, ou `null`.

- **inicial:** `{ itens_visiveis: 0, marcados: 0, destaque: null }`, só o cabeçalho.
- **final:** `{ itens_visiveis: itens.length, marcados: 0, destaque: null }`, todas as linhas em
  repouso. Terminando em confirmação, o final é `marcados: itens.length`.
- O contador escreve o que está na tela, nunca um número fixo. Número escrito na mão aqui mentiria
  na primeira linha que entrasse.
- **O teto, medido com a marca de exemplo:** com cabeçalho, três linhas com meta dão 576 px e a
  quarta dá 731, que passa dos 636 da área útil. Sem meta, cabem quatro, em 584 px, e a quinta
  dá 702. Cada linha com meta custa 155 px, e sem meta custa 118 px.

---

### janela-de-app

**Serve para:** o programa de trabalho. Editor de documento, ferramenta de conversa com IA, quadro de
tarefas, qualquer serviço na tela. É o mock para quando a fala nomeia onde o trabalho acontece.

**Tokens que lê:** `--superficie-alt` (a janela), `--superficie` (a coluna da esquerda e os blocos),
`--tinta-suave` (bordas, pontos da barra, seções em repouso), `--tinta` (nome, manchete, texto do
bloco, seção ativa, silhueta da marca), `--destaque` (seção ou bloco apontado), `--raio`, `--borda`,
`--fonte-titulo` (nome e manchete), `--fonte-corpo`, `--tam-corpo` (nome, manchete e blocos),
`--tam-rotulo` (as seções), `--entrelinha`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `titulo` | texto | obrigatório | o nome do programa na barra de cima |
| `secoes` | lista de textos | obrigatório | de duas a cinco. Com uma só, a coluna não lê como barra lateral, e a peça recusa |
| `marca` | nome de arquivo do acervo ou null | `null` | o logo de verdade na barra de cima |
| `manchete` | texto ou null | `null` | o título da área de conteúdo |
| `conteudo` | lista de textos | `[]` | cada texto vira um bloco na área de conteúdo |
| `largura` | número em px | `820` | a coluna da esquerda fica com 32% dela |
| `altura` | número em px ou null | `null` | com altura fixa, a janela não muda de tamanho quando um bloco entra |

**Estados:** `definir({ secao, conteudo_visivel, destaque })`. `secao` é o índice da seção ativa.
`destaque` é `"secao"` (aponta a seção ativa), o índice de um bloco, ou `null`.

- **inicial:** `{ secao: 0, conteudo_visivel: 0, destaque: null }`, a janela montada na primeira
  seção, com a área de conteúdo ainda vazia.
- **final:** `{ secao: a seção em que o corte termina, conteudo_visivel: conteudo.length, destaque: null }`.
- Trocar de `secao` é o evento mais barato desta peça: o mundo não se desmonta, a coluna só muda
  quem está aceso. É assim que ela atravessa um corte inteiro sem reiniciar.

---

### card-de-post

**Serve para:** a publicação. O post que a fala cita, o comentário que chegou, o número que a
publicação fez. É o mock para quando o beat acontece em uma rede.

**Tokens que lê:** `--superficie-alt` (o card), `--superficie` (a mídia), `--tinta-suave` (bordas,
avatar, arroba, glifos e números, silhueta da plataforma), `--tinta` (autor e corpo),
`--destaque` (autor, corpo ou medida apontada, e o coração cheio), `--raio`, `--borda`,
`--fonte-titulo` (autor e inicial do avatar), `--fonte-corpo`, `--tam-corpo` (autor e corpo),
`--tam-rotulo` (arroba e números), `--entrelinha`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `autor` | texto | obrigatório | o nome de quem publicou. A inicial dele vira o avatar |
| `corpo` | texto | obrigatório | o texto da publicação. A peça corta na terceira linha, com reticências: passou de três linhas, a frase é longa demais para o corte |
| `marca` | nome de arquivo do acervo ou null | `null` | o logo da plataforma no canto do cabeçalho |
| `arroba` | texto ou null | `null` | o identificador embaixo do nome |
| `midia` | booleano | `false` | a superfície de imagem embaixo do texto, com o glifo de imagem no meio |
| `altura_midia` | número em px | `200` | |
| `curtidas` | número ou null | `null` | entra na régua só quando existe |
| `comentarios` | número ou null | `null` | |
| `compartilhamentos` | número ou null | `null` | |
| `largura` | número em px | `820` | |

**Estados:** `definir({ visivel_ate, curtido, proporcao, destaque })`. `visivel_ate` é
`"cabecalho"`, `"corpo"`, `"midia"` ou `"engajamento"`, e revela o post por partes. `proporcao` vai
de 0 a 1 e multiplica os números da régua, que é como a `render(t)` faz a contagem subir. `destaque`
é `"autor"`, `"corpo"`, `"curtidas"`, `"comentarios"`, `"compartilhamentos"` ou `null`.

- **inicial:** `{ visivel_ate: "cabecalho", curtido: false, proporcao: 0, destaque: null }`, só quem
  publicou.
- **final:** `{ visivel_ate: "engajamento", curtido: false, proporcao: 1, destaque: null }`, o post
  inteiro com os números cheios.
- `curtido: true` troca o contorno do coração pelo coração cheio em cor de acento. É o acento do
  quadro, então ele vale durante a frase que fala da curtida e sai depois dela.
- O acento vai para **uma** medida por vez. A régua inteira acesa seriam três manchas de destaque no
  mesmo quadro, e a lei do acento pede exatamente uma.
- O separador de milhar é escrito pela própria peça, sem pedir o idioma da máquina, porque
  `render(t)` tem que dar o mesmo pixel em qualquer computador.

---

### glifo-que-transforma

**Serve para:** o beat de ideia abstrata em que o ponto é **uma coisa virando muitas**. Uma silhueta
cheia, sozinha no painel, atravessando uma sequência de conceitos: versatilidade, a mesma ferramenta
em vários papéis, a faísca que vira coisa entregue. Ela é objeto herói e não divide o palco com
ninguém.

**Não serve para:** objeto real, interface ou marca. Um conceito que tem coisa concreta atrás pede a
coisa, não o glifo, e marca nomeada continua entrando só pelo `tile-de-logo` com o arquivo de verdade
(seção 7). As formas de fábrica são genéricas de propósito e não representam empresa nenhuma. Também
não serve para beat que precisa de rótulo ou hierarquia: o glifo não tem texto.

**Tokens que lê:** `--destaque` (o padrão) ou `--tinta`. Mais nada: a peça não tem fundo, não tem
borda, não tem sombra própria. O brilho atrás do herói e o grão por cima já vêm do `base.js`.

**Parâmetros:**

| nome | tipo | padrão | o que faz |
|---|---|---|---|
| `formas` | lista de nomes | as oito de fábrica | os conceitos que a peça atravessa, na ordem |
| `catalogo` | objeto `nome: caminho d` | `{}` | formas próprias do corte. Sobrepõe o nome de fábrica se repetir |
| `tamanho` | número em px | `620` | o lado da caixa quadrada. Fora de 580 a 636 a peça reclama no console. O teto não é os 870 da largura porque a caixa é quadrada: 636 é a altura da área útil, e um lado maior invade a zona quieta da legenda |
| `cor` | `"destaque"` ou `"tinta"` | `"destaque"` | |

As oito formas de fábrica: `no`, `balao`, `foguete`, `raio`, `joinha`, `losango`, `grade`, `lampada`.
Um corte com universo próprio passa as formas dele em `catalogo`, em uma caixa de 0 a 100, com cada
subcaminho começando em `M` maiúsculo.

**Estados:** `definir({ de, para, avanco })`. `de` e `para` são nomes de forma, e `avanco` vai de 0 a
1. Quem escolhe o par e move o avanço é a `render(t)`, exatamente como faz com o `cronometro`. Com
`de` igual a `para`, ou com `avanco` em 0, a peça fica parada na forma de partida.

- **inicial:** `{ de: formas[0], para: formas[0], avanco: 0 }`, a primeira forma em repouso.
- **final:** de volta à primeira forma, que é o que fecha o ciclo sem emenda visível.
- **Cada forma descansa.** Transformação encostada em transformação vira animação perpétua, que é o
  item 1 dos proibidos. A receita medida é 0,85 s de transição e 0,65 s de repouso em cada forma, o
  que dá 12,0 s para as oito. A conta: `duração = repouso + n·transição + (n−1)·repouso`, com `n`
  igual ao número de transições do ciclo.

**Como a transformação é feita, e por que sem biblioteca:** cada caminho é amostrado em 240 pontos de
mesmo comprimento de arco por subcaminho, os subcaminhos dos dois lados são pareados por área e
alinhados pelo giro de menor percurso, e o desenho de um instante é a interpolação ponto a ponto. É
geometria pura, sem relógio e sem dependência: o mesmo `avanco` devolve o mesmo pixel. Quem tem menos
subcaminhos ganha subcaminhos colapsados em um ponto no centro do buraco que vai nascer, e por isso a
escotilha do foguete e os anéis da lâmpada abrem no lugar certo em vez de virem voando de fora.

**Preenchimento:** cada forma é reencaixada para que o lado maior dela ocupe a caixa inteira. Sem
esse ajuste a lâmpada desenhava 445 px de largura numa peça de 620, abaixo do piso de 580 da lei do
preenchimento. Com ele, medido no quadro do `painel.py`, o lado maior dá os 620 px em todas as oito.
Forma em pé, como o balão, gasta os 620 na altura e deixa ar nos lados: é assim mesmo, porque forçar
a largura jogaria a altura para fora dos 636 úteis.
