# O beat-sheet

O beat-sheet é o plano do painel de cima. Ele é escrito aqui, no planejamento, e consumido pelo
`/flow-reels:produzir` na hora de renderizar.

A divisão de trabalho é esta, e vale como lei: **o planejamento decide o QUE e o QUANDO, a produção
decide o QUÃO BEM.** Você diz que no segundo 7,2 o terceiro item entra na lista e o destaque sai do
primeiro. Quem renderiza decide a curva, o espaçamento e o acabamento, seguindo `PADRAO-VISUAL.md`.

Um beat-sheet é um arquivo `beats.yaml` dentro da pasta do corte:
`projetos/<video>/materiais-de-trabalho/corte-NN/beats.yaml`.

**O beat-sheet escolhe, não inventa.** Toda coisa concreta que a fala deste corte nomeia já foi
decidida no `materiais-de-trabalho/INVENTARIO.md`, no passo 0 da ordem de trabalho: qual rota ela
segue e com que recurso. Aqui você resolve o campo `peca` contra aquele arquivo. A lei das rotas é
`REPRESENTACAO.md`, e o que segue neste arquivo é só a forma do plano.

---

## 1. As quatro regras que definem tudo

### Regra A: um beat por palavra-chave

Percorra a fala do corte e sublinhe as palavras em que a ideia vira. Não são as palavras bonitas, são
as palavras que **mudam o que a pessoa sabe**: o número, o nome da coisa, o verbo da ação, a
consequência, a virada.

Cada palavra dessas ganha um beat. O resultado natural é um evento a cada 1 a 3 segundos, que é
exatamente a cadência que `PADRAO-VISUAL.md` exige.

Consequência prática: um corte de 34 segundos tem tipicamente de 12 a 20 beats. Se o seu beat-sheet
tem 5 beats para 34 segundos, o painel vai ficar parado a maior parte do tempo. Se tem 40, ninguém
consegue ler nada.

### Regra B: beat descreve mudança, nunca layout parado

O campo `muda` de todo beat começa com um **verbo de transformação**. Ele responde: o que está
diferente na tela depois deste beat em relação ao anterior?

**Verbos proibidos**, porque descrevem estado e não mudança:

`aparece`, `é exibido`, `é mostrado`, `fica visível`, `tem`, `contém`, `está`, `existe`, `mostra`

**Verbos que servem**, porque descrevem a transformação:

`digita`, `acende`, `apaga`, `risca`, `preenche`, `esvazia`, `desce`, `sobe`, `entra`, `sai`,
`divide`, `junta`, `reorganiza`, `troca`, `desenha`, `corta`, `avança`, `recua`, `marca`, `desmarca`,
`substitui`, `aproxima`, `afasta`

Teste rápido: se você trocar o `muda` de dois beats de lugar e o sentido continuar igual, você
escreveu layout, não mudança.

Exemplo de linha errada e a mesma linha certa:

```yaml
# errado: descreve o que está na tela
muda: "três cards com os nomes das etapas aparecem lado a lado"

# certo: descreve o que se transforma
muda: "o card único se divide em três, e o primeiro acende"
```

### Regra C: mostre a ideia, não a frase

O defeito padrão de um painel é ser literal: a fala afirma uma coisa e o painel escreve a mesma
palavra de volta numa pílula. RITMO, HÁBITOS, REESCRITA, uma atrás da outra, enquanto a legenda já
está dizendo ritmo, hábitos e reescrita. Quem assiste lê tudo duas vezes e não vê nada.

Antes de escrever o `muda` de cada beat, responda: **que objeto, que estado ou que gesto É esta
ideia?** A tipografia repetindo a palavra é o último recurso, não o primeiro.

| a fala diz | o painel não escreve | o painel mostra |
|---|---|---|
| um número ("3 segundos", "40 questões", "500 idiomas") | "40 QUESTÕES" numa pílula | o número como herói, em escala de título, correndo até o valor (`cronometro`, `barra-de-progresso`) |
| uma lista ("cinco plugins", "três passos") | um rótulo por item | os itens como filhos numerados do herói, entrando um a um (`chip-numerado`, `lista-de-itens`) |
| um antes e depois ("quebrado, agora funciona") | "ANTES" e "DEPOIS" | o mesmo herói mudando de estado: a linha riscada vira a linha certa, o erro vira o resultado |
| uma comparação ("pequeno" contra "grande") | as duas palavras lado a lado | uma escala visível que enche pouco e depois enche toda |
| uma ação num programa ("mandei o print", "digitei o comando") | o nome da ação | a ação acontecendo no mock: o texto se digitando, o arquivo entrando, o resultado chegando |
| uma qualidade abstrata ("natural", "com a sua cara") | o adjetivo | o efeito dela no herói: o texto marcado de amarelo fica limpo, a linha genérica vira a linha pessoal |

Duas consequências práticas:

- **Pílula e rótulo não carregam beat sozinhos.** Eles podem acompanhar uma mudança de verdade,
  nomeando o que acabou de acontecer, mas o beat é a mudança, não a etiqueta. Um beat cujo `muda` é
  só "entra a pílula X" está reprovado no item 13 da conferência abaixo.
- **Na contagem da regra A, só vale o beat que muda o herói ou o mundo.** Vinte beats em que quinze
  são pílulas entrando é um painel de cinco beats com legenda repetida por cima.

Quando a ideia realmente não vira objeto, porque é um conceito solto que a fala só menciona de
passagem, a saída é **não criar beat para ela** e deixar o herói fazer o próximo movimento na palavra
seguinte que vire. Pílula para não deixar o beat vazio é pior que beat nenhum.

### Regra D: a abertura é o trailer

Os primeiros cinco segundos são o trecho mais quente do corte, e o plano é escrito assim de
propósito, porque é ali que a pessoa decide se fica. A lei está em
`skills/produzir/referencias/PADRAO-VISUAL.md` seção 5.1, e no plano ela vira três
coisas:

- **o primeiro beat, em `t: 0.0`, já coloca o herói inteiro em cena**, no tamanho de trabalho. Não é
  um cabeçalho esperando o conteúdo: é o objeto com o estado inicial dele montado;
- **pelo menos três beats que mudam o herói antes de `t: 5.0`**, e nenhum deles é pílula;
- **o gesto mais caro do corte vai aqui**, o contador que dispara, a lista que enche, a interface que
  se monta. Se ele só cabe uma vez, é na abertura.

Se a fala dos primeiros cinco segundos é só o gancho falado, sem nada concreto, o herói não espera: ele
mostra a promessa. "Corrigi um bug sem escrever uma linha de código" já é um terminal com o erro
vermelho em cena no primeiro quadro.

---

## 2. O formato

```yaml
corte: 01
titulo: "Planilha é o que faz desistir"
duracao: 34.2

mundo:
  superficie: escura
  objeto_heroi: card
  por_que: "o corte compara duas formas de registrar gasto, e card é a peça que divide e compara"
  estados:
    - id: planilha-cheia
      descricao: "um card grande, com muitas linhas apertadas dentro"
    - id: abandonada
      descricao: "o mesmo card, com as linhas em tinta_suave e o título riscado"
    - id: linha-unica
      descricao: "o card encolhe para uma linha só, centralizada e em destaque"

beats:
  - t: 0.0
    ideia: "o assunto entra nomeado"
    muda: "o card grande sobe para a posição e as primeiras seis linhas se escrevem dentro dele"
    peca: card
    estado: planilha-cheia
    legenda: "Planilha de controle"

  - t: 2.4
    ideia: "a afirmação: é ela que faz desistir"
    muda: "o título do card recebe o destaque e o resto do card cai para tinta_suave"
    peca: card
    estado: planilha-cheia
    legenda: "é o motivo de desistir"

  - t: 5.1
    ideia: "os quarenta e três dias"
    muda: "um contador de dias entra abaixo do card e corre de 1 até 43 enquanto a frase dura"
    peca: cronometro
    estado: planilha-cheia
    legenda: "quarenta e três dias"

  - t: 8.0
    ideia: "descanso depois do contador"
    muda: "nada muda: o contador fica parado em 43"
    descanso: true
    legenda: "e no dia quarenta e quatro"

  - t: 9.6
    ideia: "o abandono"
    muda: "as linhas do card apagam de baixo para cima e o título ganha o risco"
    peca: card
    estado: abandonada
    legenda: "eu não abri mais"
```

### Os campos do cabeçalho

| campo | obrigatório | o que é |
|---|---|---|
| `corte` | sim | o número do corte, igual ao da pasta |
| `titulo` | sim | nome curto, só para achar o arquivo depois. Não vai para a tela |
| `duracao` | sim | a duração do corte em segundos, com uma casa. Tem que bater com o brief |

### O bloco `mundo`

| campo | obrigatório | o que é |
|---|---|---|
| `superficie` | sim | `escura` ou `clara`. Uma só, o corte inteiro. Não alterna |
| `objeto_heroi` | sim | o nome de uma peça do `componentes/REGISTRO.md`. **Um por corte** |
| `rota` | não | a rota do inventário que o mundo executa, quando o herói é uma coisa concreta: `logo`, `mock` ou `tela`. Mundo de ideia abstrata não tem este campo |
| `por_que` | sim | uma frase ligando a escolha da peça ao conteúdo da fala. Existe para impedir a escolha automática de sempre a mesma peça |
| `conteudo` | sim quando o herói é um mock | **o texto literal que o mock mostra**, palavra por palavra, do jeito que vai aparecer na tela. Sem ele, quem desenha inventa o texto, e texto inventado é onde a interface genérica volta |
| `estados` | sim | a lista de estados pelos quais o herói passa, com `id` e `descricao`. De 2 a 5 estados |

O herói **não sai de cena** e **não é trocado no meio**. Se você sentiu vontade de trocar, o corte
está tentando dizer duas coisas, e provavelmente são dois cortes.

Peças de apoio (chip, rótulo, seta, tile) entram e saem à vontade. Elas são filhas do mundo, não
heróis concorrentes.

### Quando o herói é um mock de interface

Seis peças do registro desenham a **forma** de uma interface: `tela-de-conversa`,
`janela-de-navegador`, `campo-de-busca`, `lista-de-itens`, `janela-de-app` e `card-de-post`. Elas
são a rota mock do inventário, e são opção de herói como qualquer outra peça. A `caixa-de-comando`
entra aqui junto: ela não é um dos seis mocks, mas é a forma da linha de comando, e um beat de
terminal é mock resolvido por ela. Qual peça serve para qual fala está na seção 4 do
`REPRESENTACAO.md`, e os tetos de conteúdo estão no `componentes/REGISTRO.md`, que é o dono dos
números.

Três coisas mudam no plano quando o herói é um mock:

- **ele ocupa o painel sozinho.** O registro é explícito: um mock e mais nada. Esqueça a fila de
  peças de apoio em volta;
- **os estados são estados da interface**, não formas novas: a mensagem que entra, a URL que termina
  de ser digitada, a seção que acende, o resultado que chega, o número que sobe;
- **o conteúdo é curto e você o escreve no campo `conteudo` do `mundo`**, literal, não descrito.
  Três linhas, três mensagens, três resultados. "Dois blocos escritos na área" não é conteúdo, é
  descrição, e quem desenha vai preencher com o que imaginar. Texto que passa do teto sai cortado
  com reticências no render, e reticências no painel quer dizer que a frase é longa demais para o
  corte.

```yaml
mundo:
  superficie: escura
  objeto_heroi: janela-de-app
  rota: mock
  conteudo:
    marca: claude
    secoes: ["Conversas", "Projetos", "Artefatos"]
    blocos: ["Escreva como um roteirista", "Nunca use lista com marcador"]
  por_que: "a fala inteira acontece dentro do programa, e o que muda é a seção em que ele está"
  estados:
    - id: vazio
      descricao: "a janela montada na primeira seção, área de conteúdo ainda sem bloco nenhum"
    - id: com-instrucoes
      descricao: "a seção de instruções acesa, com dois blocos escritos na área de conteúdo"

beats:
  - t: 3.4
    ideia: "onde o ajuste é feito"
    muda: "a coluna troca de seção acesa e a área de conteúdo esvazia"
    peca: janela-de-app
    estado: vazio
    legenda: "está nas instruções"
```

### Os campos do beat

| campo | obrigatório | o que é |
|---|---|---|
| `t` | sim | o instante do beat em segundos, na linha do tempo do corte, não do vídeo longo |
| `ideia` | sim | o que este beat comunica, em até 8 palavras |
| `muda` | sim | a transformação, começando por verbo. Uma frase |
| `peca` | sim, salvo em descanso | o nome da peça do registro que sofre a mudança. Tratando o beat de coisa concreta nomeada na fala, a peça é a que o `INVENTARIO.md` decidiu para aquela coisa, e não uma escolhida agora |
| `estado` | não | o `id` do estado do herói depois deste beat, quando o beat muda o herói |
| `legenda` | sim | o pedaço da fala que está na tela neste momento. É o que amarra o painel à voz |
| `descanso` | não | `true` marca uma pausa proposital. Só vale logo depois de um evento grande e por no máximo cerca de 2 segundos |
| `tela` | não | o bloco que manda este beat usar gravação de tela real no lugar de desenho. Formato e regras logo abaixo |

O campo `legenda` não precisa ser o grupo exato que o gerador de legenda vai produzir, porque o
agrupamento final é medido em pixels na hora de gerar. Ele precisa ser **a fala daquele instante**,
para que quem renderiza saiba a qual palavra o movimento tem que chegar.

### O bloco `tela`, quando o beat usa gravação de tela real

O padrão do pacote é painel desenhado, e a maioria dos beats não tem este bloco. Ele existe para o
beat que é uma **demonstração**: a fala afirma que alguma coisa aconteceu numa interface e quem
assiste precisa acreditar que aconteceu. Este bloco é a rota tela, e ela se fecha **aqui**, não no
inventário.

A divisão é esta, e ela não é burocracia: o inventário já respondeu o que se responde olhando o
arquivo, ou seja se a fonte mostra a coisa e se a região aguenta o recorte, e marcou a linha como
`tela candidata` com o instante e a região. O que faltava era o orçamento, que é por corte, e no
passo 0 corte nenhum existia ainda. **Você é o primeiro momento em que o corte existe**, então a
terceira pergunta é sua:

> as janelas que este corte quer cabem no orçamento da 9.2?

Cabe, o bloco `tela` entra com o instante que o inventário anotou. Não cabe, o beat vira **mock** e
o inventário fica como está, porque a candidata continua valendo para outro corte. Degradar para
nada nunca é resposta: o beat continua precisando mostrar.

A lei completa, com os casos permitidos, os proibidos e o orçamento, está em
`skills/produzir/referencias/PADRAO-VISUAL.md` seção 9, e a conta dos dois tempos
está no passo 2 do `REPRESENTACAO.md`.

```yaml
  - t: 12.6
    ideia: "a busca devolve os arquivos"
    muda: "a janela abre dentro do card e o resultado da busca entra com os três arquivos"
    peca: card
    estado: com-tela
    legenda: "e ele devolve os três"
    tela:
      arquivo: tela.mp4
      de: 812.4
      ate: 817.0
      regiao: "o painel de resultados, no canto de cima à direita"
      anotacao: "destaque no primeiro resultado, rótulo TRÊS ARQUIVOS CRIADOS"
      por_que: "a fala afirma que a busca devolveu três arquivos, e isso é fato que precisa ser visto"
```

| campo | obrigatório | o que é |
|---|---|---|
| `arquivo` | não | o nome da gravação de tela separada, que vive em `materiais-de-trabalho/fonte/`, porque é a mesma para todos os cortes. Sem o campo, a tela sai da própria fonte do vídeo, e quem resolve a origem é a produção, na seção 2.5 do `/flow-reels:produzir` |
| `de` | sim | entrada do trecho **na linha do tempo da gravação**, não na do corte |
| `ate` | sim | saída do trecho, na mesma linha do tempo. A janela começa no `t` do beat e dura `ate` menos `de` |
| `regiao` | sim | em palavras, a região que a fala nomeia. O recorte em pixels é decisão da produção, como todo acabamento |
| `anotacao` | sim | o que precisa estar anotado por cima: onde vai o destaque e o que diz o rótulo. Tela crua, sem anotação, é reprovada |
| `por_que` | sim | **uma linha** respondendo o teste de 9.1: este beat é o produto fazendo alguma coisa que quem assiste precisa acreditar que aconteceu? |

**A justificativa é escrita aqui, no beat, e não em outro lugar.** Ela é o que separa prova de
preguiça, e ela é conferida antes de qualquer extração. Justificativa que serviria para qualquer beat
do corte, do tipo "fica mais dinâmico" ou "mostra a ferramenta", não é justificativa: tire o bloco e
escreva o beat como desenho.

Três regras que acompanham o bloco:

- **A origem da tela já está resolvida no inventário.** O campo `arquivo` só aparece quando existe
  uma gravação separada; com a fonte sendo compartilhamento de tela, ele não vai. Qual é o caso deste
  vídeo está escrito no `INVENTARIO.md`, e quem mede é a produção, pela 2.5 do `/flow-reels:produzir`.
- **O beat com `tela` continua sendo um beat normal.** Ele tem `muda` com verbo de transformação, e
  `peca` é o herói que segura a janela. A tela aparece dentro do herói, ela não substitui o painel.
- **Quem abre, fecha.** O fim da janela é escrito como um beat comum, do tipo
  `muda: "a janela fecha por wipe e o card volta inteiro"`. Janela que fica aberta até o fim do corte
  sem motivo vira captura de tela com legenda por cima.

O orçamento de tela saiu daqui: ele é consultado no passo 2 do `REPRESENTACAO.md` e o número vive no
dono, `PADRAO-VISUAL.md` seção 9.2. Estourado, o beat desce para mock autorado, nunca para palavra.

---

## 3. A sincronia com a fala

**O movimento chega na palavra, não perto dela.**

A chegada de um elemento dura 800 ms e é uma subida que desacelera. Para que ela pareça causada pela
palavra, o movimento **começa** cerca de 200 ms antes da palavra e **termina** em cima dela. Na
prática, escreva o `t` do beat 0,2 s antes do início da palavra na transcrição.

Movimento que começa na palavra chega tarde demais e lê como atraso. Movimento que termina antes da
palavra lê como desconexo, e quem assiste sente que o vídeo está dublado.

Regra da palavra literal: o painel mostra **a coisa**, não a palavra. Se a fala diz "quarenta e três
dias", o beat é o contador chegando em 43, não o texto "43 dias" escrito na tela. Painel que escreve
a frase da legenda é o defeito número 2 da lista de proibições do padrão visual.

---

## 4. Como conferir antes de entregar

Percorra a lista. Cada item é sim ou não.

1. **Cadência.** O maior intervalo entre dois beats consecutivos passa de 3 segundos sem estar marcado
   como `descanso`? Se passa, falta beat.
2. **Verbo.** Todo `muda` começa com verbo de transformação e nenhum usa a lista de proibidos?
3. **Um herói.** Todos os beats que mudam o herói citam a mesma peça em `objeto_heroi`?
4. **Estados encadeados.** A sequência de `estado` faz um caminho contínuo, sem voltar ao estado
   inicial no meio e sem estado órfão que nunca é usado?
5. **Eco.** Algum `muda` coloca na tela a mesma frase que está no `legenda` do mesmo beat? Se sim,
   reescreva: o painel mostra a coisa, a legenda carrega a fala.
6. **Peças reais.** Todo `peca` existe em `componentes/REGISTRO.md`? Nome inventado quebra o render.
   E o conteúdo que você escreveu para um mock cabe no teto daquela peça, ou vai sair cortado com
   reticências?
7. **Contagem.** Em qualquer instante, quantos elementos ficam visíveis ao mesmo tempo? Se passar de
   sete, algum beat precisa tirar coisa da tela antes de colocar mais.
8. **Zona quieta.** Algum beat coloca elemento novo na base do painel, onde a legenda passa? Reescreva
   a posição, porque o movimento vai brigar com o texto.
9. **Perpétuo.** Algum `muda` descreve movimento sem fim (girar, pulsar, piscar, flutuar)? Proibido. A
   única exceção é um valor correndo durante a frase que fala dele, e ele para quando a frase acaba.
10. **O último beat.** O corte termina com o mundo em um estado de conclusão, não no meio de uma
    transformação. Se o último beat está pela metade quando o áudio acaba, antecipe o `t`.
11. **Tela real justificada.** Todo beat com bloco `tela` tem `por_que`, e esse `por_que` afirma um
    fato que quem assiste precisa acreditar que aconteceu, no lugar de dizer que fica mais bonito ou
    mais dinâmico? Justificativa que serviria para qualquer beat do corte não é justificativa: tire o
    bloco e desenhe. E o corte inteiro cabe no orçamento de tela, que é consultado no passo 2 do
    `REPRESENTACAO.md`?
12. **Rota decidida para tudo que a fala nomeia.** Toda coisa concreta nomeada na fala deste corte
    tem rota decidida no `INVENTARIO.md`, ou alguma virou card com texto por falta de decisão? Card
    escrevendo o nome de uma ferramenta é a resposta que sai quando ninguém decidiu a rota, e é o
    defeito que a etapa 0 existe para impedir. Achou uma, volte ao inventário e decida lá, não aqui.
13. **Pílulas.** Conte os beats cujo `muda` é só uma pílula ou um rótulo entrando com uma palavra da
    fala. Passou de um em cada quatro beats? Reescreva pela regra C: que objeto é aquela ideia?
14. **Abertura.** O beat de `t: 0.0` coloca o herói inteiro em cena, e existem pelo menos três beats
    que mudam o herói antes de `t: 5.0`, nenhum deles pílula? Se não, reescreva pela regra D.
15. **Parado.** Contando só os beats que mudam o herói ou o mundo, algum intervalo entre dois deles
    passa de 2,5 segundos? É o mesmo número que o `ritmo_painel.py` vai medir no vídeo, e é muito
    mais barato consertar aqui do que depois do render.

---

## 5. Erros frequentes

| erro | o que fazer |
|---|---|
| beat-sheet que é uma sequência de telas | um mundo, um herói, estados. Se cada beat limpa a tela, é slideshow |
| beat sem `legenda` | sem a fala, quem renderiza não tem em que se ancorar e o movimento cai em qualquer lugar |
| sempre a mesma peça como herói | o campo `por_que` existe para isso. Se a justificativa não sai, a peça está errada |
| dez beats no primeiro terço e dois no resto | a cadência vale do primeiro ao último segundo. O fim do corte é onde a pessoa decide compartilhar |
| `muda` com duas transformações na mesma linha | quebre em dois beats. Um beat, uma mudança |
| tempo copiado da transcrição do vídeo longo | o `t` é sempre na linha do tempo do corte montado, começando em 0 |
| rota escolhida aqui, na hora de escrever o beat | a rota é do inventário, passo 0. Aqui você resolve contra ele. A separação entre ideia e coisa concreta, inclusive a de pedir tela para ideia abstrata, é o passo 0 da ordem de decisão do `REPRESENTACAO.md` |
| mock com o conteúdo de uma tela de verdade, cheio de linha | o teto é apertado de propósito. Três itens, e o resto o corte não precisa |
| cada palavra-chave vira uma pílula com a própria palavra | regra C. A palavra já está na legenda; o painel mostra o objeto que ela nomeia |
| herói chegando aos poucos, cabeçalho sozinho nos primeiros segundos | regra D. O herói chega inteiro em `t: 0.0`, e a abertura é o trecho mais quente |
| número dito na fala virando texto pequeno num rótulo | número é herói: escala de título, correndo até o valor |
