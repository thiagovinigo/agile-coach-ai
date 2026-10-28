# Padrão visual

A lei do corte. Não é inspiração, é contrato: cada regra aqui tem número, unidade e um jeito de
conferir olhando um quadro. Quem produz o painel lê este arquivo antes de desenhar a primeira coisa,
e volta nele antes de dizer que terminou.

Uma frase para guardar: o que separa um corte bom de um slideshow não é ter animação, é ter **um
mundo só que muda de estado**. Slideshow também tem animação.

---

## 1. Geometria

Tudo é medido em pixels no canvas final. Nada aqui é sugestão.

| peça | tamanho | posição |
|---|---|---|
| canvas | 1080 x 1920, 30 fps | o vídeo entregue |
| painel de cima | 1080 x 956 | y de 0 a 955 |
| face embaixo | 1080 x 964 | y de 956 a 1919 |
| costura | 0 px | a linha em y = 956 |

**A costura não tem enfeite.** Nenhuma linha, nenhum filete de cor, nenhuma sombra, nenhum degradê,
nenhuma borda. Os dois painéis simplesmente encostam. Qualquer marca ali cria uma terceira coisa na
tela e a legenda, que passa exatamente por cima, fica ilegível.

**Margem lateral: 56 px dos dois lados.** Nada que precise ser lido encosta em menos que isso. A
largura útil do painel é 968 px.

**Zona segura de cima: 150 px.** De y = 0 a y = 150 não entra texto nem parte importante do objeto
herói. É onde a plataforma desenha a interface dela por cima do seu vídeo. Fundo, brilho e grão podem
ocupar essa faixa à vontade. Conteúdo não.

**Zona quieta de baixo: 170 px.** De y = 786 a y = 956, ou seja a base do painel, fica sem nenhum
elemento. É por ali que a legenda passa. A legenda em 116 px centrada na costura ocupa de y ≈ 885 a
y ≈ 1035, então a zona quieta dá cerca de 100 px de folga acima dela. Essa folga é o que impede a
sensação de texto colado em desenho.

**Área real de trabalho do painel:** 968 x 636 px, de y = 150 a y = 786. É pouco, e é de propósito. É
o que força o objeto a ser grande.

---

## 2. A lei do mundo único

O painel de cima é **um lugar**, não uma sequência de telas.

- **Um objeto herói por corte.** Uma coisa só carrega o corte inteiro do primeiro ao último segundo.
  Pode ser uma caixa de comando, um card que vira três cards, um cronômetro, um diagrama. Uma coisa.
- **O herói não sai de cena.** Ele muda de estado. Trocar o herói no meio do corte é começar um
  segundo corte dentro do primeiro.

**O que conta como mudança de estado:**

- o herói ganha um filho novo (um item entra na lista, um chip aparece ao lado)
- o herói se reorganiza (uma coluna vira duas, um card se divide)
- o herói muda de valor (o cronômetro anda, a barra enche, o número sobe)
- o herói muda de qualidade (uma linha dele recebe o destaque, uma parte apaga, uma parte risca)
- a câmera do mundo se move (o enquadramento aproxima ou afasta, e o herói continua o mesmo)

**O que NÃO conta como mudança de estado:**

- limpar a tela e desenhar outra coisa
- trocar o fundo
- fazer o objeto entrar de novo com a mesma animação de chegada
- **uma pílula ou um rótulo entrando com a palavra que a fala acabou de dizer.** Isso é enfeite, não
  evento. Quem assiste lê a mesma palavra duas vezes, uma na legenda e outra no painel, e o herói não
  mudou nada. Rótulo continua permitido como acompanhamento de uma mudança de verdade, nomeando o que
  acabou de acontecer, mas ele nunca é o beat sozinho. A regra que decide o que desenhar no lugar dele
  está no `BEAT-SHEET.md` do planejador, regra C: **mostre a ideia, não a frase**.

**O teste do olho semicerrado.** Uma mudança só conta se alguém olhando de relance, com os olhos
semicerrados, percebe que a tela ficou diferente: o herói ganhou uma parte do tamanho de um item da
lista para cima, um número virou outro em escala de título, a câmera aproximou, uma parte inteira
acendeu, riscou ou apagou. Uma etiqueta de 34 px aparecendo no canto não passa nesse teste.

**O corte de fala nunca reinicia o painel.** Quando você costura dois trechos de fala que estavam
longe um do outro no vídeo original, o áudio corta mas o painel continua exatamente de onde estava.
O painel é contínuo do segundo 0 ao fim, com um relógio só. Se o painel piscar junto com o corte de
fala, a pessoa percebe a emenda, e emenda percebida é motivo de saída.

**Teste de continuidade:** pegue o último quadro antes de um corte de fala e o primeiro depois. Se o
painel mudou mais do que um evento normal mudaria, o painel reiniciou. Refaça.

O que preenche esse mundo é desenho autorado, sempre. Gravação de tela real é exceção, tem critério
e só entra anotada por cima, e a lei dela está na seção 9.

---

## 3. A lei do acento

A cor de destaque marca a **única** coisa que a fala está apontando naquele exato momento.

- Um destaque ativo por vez. Se duas coisas estão em destaque no mesmo quadro, a pessoa não sabe onde
  olhar, e a função do acento morre.
- O destaque **se move**: ele sai de um elemento e vai para outro conforme a fala avança. É assim que
  o painel conversa com a voz sem repetir o que a voz diz.
- Fora do momento apontado, o elemento volta para tinta ou tinta_suave. Ele não fica destacado "porque
  é importante". Tudo no painel é importante, senão não estaria lá.
- Elementos de marca que já nascem coloridos, como logo e personagem, não contam como destaque e não
  competem com ele. Por isso a logo não fica parada no canto.

**Orçamento de área:** o destaque ocupa no máximo cerca de 15% da área visível do painel em qualquer
quadro. Um preenchimento grande de destaque conta inteiro. Um texto em destaque conta pouco.

**Como conferir em um quadro:** tampe o quadro com a mão e abra só um buraquinho. Passeie o buraco
pela imagem. Se você encontrar duas manchas de destaque, ou nenhuma, o quadro está errado. Tem que
haver exatamente uma, e ela tem que ser a coisa que a voz está falando naquele segundo.

---

## 4. A lei do preenchimento

O painel é pequeno e é visto no celular, muitas vezes com o polegar por cima de metade da tela.

- **O objeto herói ocupa de 60% a 90% da largura útil**, ou seja de 580 a 870 px. Abaixo de 580 ele
  vira miniatura. As peças da biblioteca já nascem dentro dessa faixa, e o valor padrão de cada uma
  está em `componentes/REGISTRO.md`, que é o dono desse número. Não repita o padrão aqui: quando a
  peça mudar, quem tem que mudar junto é o registro.
- **Nada de coisinha boiando.** Um ícone de 80 px sozinho no meio de 636 px de altura vazia não é
  minimalismo, é planejamento que não terminou.
- **Uma respiração só.** Espaço vazio concentrado em um lugar lê como ar. Espaço vazio espalhado em
  volta de vários objetinhos lê como bagunça.
- **Texto grande.** O menor texto do painel é o rótulo em 34 px. Nada abaixo disso, nunca, em nenhuma
  situação. Se a informação exige texto menor, ela não cabe no painel: transforme em outra coisa ou
  tire.
- **De três a sete elementos visíveis no total**, contando o herói e os filhos dele. Acima de sete o
  painel vira painel de controle de avião.
- A altura também se preenche. Se o objeto tem 200 px de altura em uma área de 636, ou ele cresce, ou
  ganha um segundo andar, ou a câmera aproxima.

---

## 5. A física do movimento

O movimento do pacote é curto, firme e sem elástico. Nada quica, nada estica, nada gira.

| evento | duração | curva | o que muda |
|---|---|---|---|
| chegada de um elemento | 800 ms | cubic-bezier(0.33, 1, 0.68, 1) | sobe 64 px no eixo Y até a posição final; opacidade entra **cheia no primeiro quadro**; escala fixa em 1 |
| irmãos entrando juntos | atraso de 200 ms entre um e o seguinte | cada um usa a curva de chegada | o segundo começa quando o primeiro já andou um quarto do caminho |
| re-fluxo do layout | 667 ms | cubic-bezier(0.73, 0.13, 0.24, 0.86) | o grupo inteiro anda junto para as posições novas, **sem escalonar** |
| saída por corte | 0 ms | nenhuma | no quadro seguinte o elemento simplesmente não está lá |
| saída por wipe | 167 ms | linear | uma máscara varre o elemento em uma direção só |

Regras que acompanham a tabela:

- **Opacidade não faz fade de entrada.** O elemento chega opaco no primeiro quadro e o que se vê é ele
  subindo. Fade de entrada é o que faz um painel parecer apresentação de slides.
- **Escala é sempre 1.** Elemento não nasce pequeno e cresce.
- **Zero overshoot.** A curva de chegada desacelera e para. Não passa do ponto e volta.
- **Não existe saída suave.** Ou corta, ou faz o wipe de 167 ms. Elemento que some desaparecendo aos
  poucos deixa um fantasma na tela por meio segundo e rouba atenção do que entrou no lugar.
- **Re-fluxo é do grupo, não do elemento.** Quando o layout se reorganiza, todo mundo que se move
  parte no mesmo quadro e chega no mesmo quadro. Escalonar re-fluxo faz o layout parecer desmontado.
- **Acontece alguma coisa em cada frase falada.** Um evento por frase é o piso. Parado só vale como
  descanso proposital logo depois de um evento grande, e no máximo por cerca de 2 segundos.
- **Nada de animação perpétua.** Girar, pulsar, flutuar, piscar e respirar sem fim são as formas
  preguiçosas de fingir que o painel está vivo. Elas não contam como evento e são proibidas. A única
  exceção é um valor que a fala está falando enquanto ele corre, como um cronômetro durante a frase
  que fala do tempo, e ele para quando a frase acaba.

### 5.1 A abertura é o trailer

Os primeiros segundos decidem se a pessoa fica. É ali que ela resolve, com o dedo já no gesto de
passar, se o corte merece mais três segundos. Por isso a abertura tem regras mais apertadas que o
resto do corte:

- **O herói chega inteiro no primeiro segundo.** No quadro de 1 s o objeto principal já está em cena
  com o tamanho de trabalho dele, não um cabeçalho sozinho esperando o conteúdo chegar aos 8 s.
  Painel vazio no começo é o defeito mais caro do pacote, porque acontece exatamente onde a pessoa
  está decidindo.
- **Pelo menos três mudanças nos cinco primeiros segundos**, cada uma passando no teste do olho
  semicerrado da seção 2. É o ritmo mais quente do corte. Do sexto segundo em diante vale o piso
  normal: algo muda em cada frase e nada fica parado mais que cerca de 2 segundos.
- **A ideia mais cara do corte mora aqui.** Se existe um gesto que só dá para fazer uma vez, como o
  contador que dispara, a lista que enche de uma vez ou a interface que se monta inteira, ele vai na
  abertura, e não guardado para o meio.

O que a abertura **não** é: um título de painel parado com o nome do assunto. O assunto já está na
fala e na legenda. O painel da abertura mostra a coisa acontecendo.

### 5.2 A medida: `ritmo_painel.py`

A cadência não se confere só olhando quadros soltos, porque cinco quadros de um painel que congelou
seis segundos parecem cinco quadros de um painel vivo. Depois de renderizar o `painel.mp4`, e antes de
montar, meça:

```
flow-reels produzir/ritmo_painel \
  projetos/<vídeo>/materiais-de-trabalho/corte-NN/painel.mp4 \
  --beats projetos/<vídeo>/materiais-de-trabalho/corte-NN/beats.yaml
```

Ele reprova, com os instantes, dois defeitos desta seção:

| defeito | quando reprova |
|---|---|
| **parado** | algum trecho passa de 2,5 s sem nenhuma mudança visível. É o "cerca de 2 segundos" desta seção, com meio segundo de folga para a curva de chegada terminar |
| **abertura fraca** | menos de 3 mudanças nos 5 primeiros segundos, ou, aos 2 s, o painel com menos da metade do conteúdo que ele costuma ter no resto do corte |

E lista, sem reprovar, os quadros em que mais de um terço do painel mudou de uma vez: janela de tela
real abrindo é normal ali, herói trocado ou tela limpa não é.

Com `--beats`, cada trecho parado vem com o beat que veio antes dele, que é onde se conserta. O
conserto é dar mais um ato ao herói naquele trecho, na próxima palavra-chave da fala: um filho entra,
um valor corre, a câmera aproxima, uma parte acende ou risca. Nunca é animação em loop e nunca é
pílula repetindo a legenda, que são os dois jeitos de enganar a medida sem melhorar o painel.

Consertou um trecho, meça só ele de novo com `--janela inicio:fim`, sem medir o corte inteiro.
Para medir um corte já montado, passe o MP4 dele com `--corte`: o script lê só o painel de cima e
para em y = 786, antes da zona onde a legenda passa.

### Os 12 quadros por segundo

O painel é **autorado a 12 quadros por segundo** e depois segurado em 30 no container final, com cada
quadro autorado repetido para preencher.

Por que 12:

- Movimento a 12 lê como **decidido**. Movimento a 30 lê como interpolação de ferramenta, que é
  exatamente a cara de template que estamos evitando.
- Rende 40% dos quadros, então o render cabe em um tempo humano numa máquina comum.
- Os tempos da tabela caem quase todos em quadro exato a 12 fps: o re-fluxo de 667 ms são 8 quadros, o
  wipe de 167 ms são 2 quadros, o atraso entre irmãos de 200 ms são 2 quadros. A chegada de 800 ms cai
  em 9,6 quadros: arredonde para 10 quadros, que dão 833 ms. A diferença não se vê.

Consequência técnica que muda como se escreve o painel: **não se usa transição nem animação de CSS**.
O renderizador tira um quadro por vez e uma transição de CSS não roda entre capturas. Todo movimento é
calculado dentro de `window.render(t)`, avaliando a curva na mão para o instante `t`. O contrato dessa
função está em `componentes/REGISTRO.md`.

---

## 6. A lei da legenda

A legenda do pacote é **invertida** em relação ao que quase todo mundo faz: o preenchimento é escuro e
o contorno é branco. Isso foi testado sobre vídeo real, em cena clara e em cena escura, e é o que lê
nas duas. Preenchimento branco com contorno preto some em parede clara.

**Os valores exatos, em ASS, no canvas de 1080 x 1920:**

```
[Script Info]
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Legenda,Quicksand,116,&H001A1516,&H001A1516,&H00FFFFFF,&H64000000,0,0,0,0,100,100,0,0,1,5,1,5,56,56,0,1
```

Leitura campo a campo do que não pode mudar:

| campo | valor | por quê |
|---|---|---|
| Fontsize | 116 | testado sobre vídeo. Menor que isso perde no feed, maior estoura a largura em grupos normais |
| PrimaryColour | a cor escura da marca | é o preenchimento. No modo escuro é `superficie`, no modo claro é `tinta`. Em ASS a ordem é &HAABBGGRR, então #16151A vira &H001A1516 |
| OutlineColour | &H00FFFFFF | branco puro, sempre, nos dois modos. É ele que faz a legenda sobreviver em cima de qualquer cena |
| BackColour | &H64000000 | a sombra, preta com cerca de 60% de transparência. Só cola a palavra na imagem, não é para ser vista |
| BorderStyle | 1 | contorno mais sombra. **Nunca 3**, que é a caixa opaca atrás do texto |
| Outline | 5 | a espessura do contorno branco |
| Shadow | 1 | a sombra. Um, não três |
| Bold | 0 | o arquivo de fonte já é a instância negrito. Ligar o Bold aqui faz o renderizador engordar a fonte por conta e o resultado fica borrado |
| Alignment | 5 | centralizado na horizontal e na vertical. Põe o centro da linha em y = 960, que é 4 px abaixo da costura. Esses 4 px não se enxergam, e o efeito é a legenda não pertencer nem ao painel nem à face |
| MarginL / MarginR | 56 / 56 | a mesma margem lateral do painel |
| MarginV | 0 | com Alignment 5 a margem vertical não deve empurrar nada |
| WrapStyle | 2 | desliga a quebra automática. Se um grupo passar da largura, ele vaza e o erro fica visível, em vez de virar duas linhas escondidas |

**Uma linha, sempre.** Duas linhas com Alignment 5 atravessam a costura e entram no painel e na face
ao mesmo tempo, tampando o rosto e o desenho. Além disso, duas linhas obrigam o olho a voltar, e no
formato vertical o olho não volta, ele rola.

**O orçamento do grupo é de 16 caracteres.** Medido: o Quicksand negrito em 116 px gasta em média
cerca de 60 px por caractere em texto em português, e a largura útil é 968 px, o que dá 16. O gerador
sempre mede a largura de verdade antes de fechar o grupo e, se passar de 968 px, quebra em dois
grupos, mesmo que ainda não tenha chegado em 16 caracteres.

**Onde quebrar:** em pontuação primeiro, depois em fim de sintagma. Nunca deixe uma palavra de ligação
sozinha no fim de um grupo (de, da, do, em, que, com, para, por, um, uma, os, as, e, ou, se, não).
Essas palavras vão junto com a próxima.

**Um evento por grupo.** O grupo aparece inteiro, fica o tempo da fala dele, e some. Nada de palavra
pintando uma a uma dentro do grupo: em 116 px isso vira tremor.

**Armadilha do queimador:** o caminho da pasta de fontes e o caminho do arquivo de legenda precisam ser
**relativos**, com o processo rodando dentro da pasta certa. Caminho absoluto do Windows quebra o
filtro, porque o `C:` é lido como separador de opção. O detalhe e o comando estão em
`RECEITA-TECNICA.md`.

**Armadilha da fonte:** fonte variável não serve. O queimador ignora o eixo de peso e renderiza no
padrão do arquivo, que normalmente é fino, e a legenda sai magra. Só entra na legenda um arquivo de
instância estática. Qualquer fonte que o usuário traga no onboarding passa por essa conversão antes.

---

## 7. O que o pacote proíbe

Cada item aqui já estragou um corte. Não é questão de gosto.

1. **Animação perpétua.** Girar, pulsar, flutuar, piscar sem fim. É movimento sem informação e o olho
   aprende a ignorar em dois segundos.
2. **Painel que ecoa a legenda.** Se o texto no painel é a mesma frase que a legenda está mostrando, o
   painel não está fazendo nada. O painel mostra a **coisa** de que a fala fala, não as palavras dela.
   No máximo um rótulo curto, que nomeia, não repete.
3. **Superfície chapada.** Sem grão, o painel parece um slide exportado. Grão por cima de tudo,
   sempre, inclusive por cima de imagem e de logo.
4. **Segunda cor de acento.** Uma marca, um destaque. Se você precisa diferenciar dois estados, use
   destaque contra tinta_suave, não destaque contra um verde novo.
5. **Texto pequeno.** Nada abaixo de 34 px no painel. Nada.
6. **Caixa preta atrás da legenda.** BorderStyle 3 é proibido. A legenda vive de contorno e sombra.
7. **Enfeite na costura.** Nenhuma linha, filete, sombra ou degradê em y = 956.
8. **Fade de entrada e fade de saída.** Entrada é subida com opacidade cheia. Saída é corte ou wipe.
9. **Trocar o herói no meio do corte.** Um mundo por corte.
10. **Logo parada no canto o corte inteiro.** Ocupa área útil e não diz nada.
11. **Emoji como ícone.** Cada plataforma desenha um diferente e nenhum é da sua marca.
12. **Cor escolhida na hora.** Toda cor sai de `marca/tokens.json`. Nenhum valor hexadecimal escrito
    direto no painel.
13. **Pílula no lugar da ideia.** Uma sequência de pílulas ou rótulos, cada um com a palavra que a
    fala acabou de dizer, fazendo o papel de beat. É o eco da legenda em pedaços menores. O painel
    mostra a ideia como objeto: número vira contador, lista vira fileira de itens numerados, antes e
    depois vira o herói mudando de estado (seção 2, e a regra C do `BEAT-SHEET.md`).
14. **Abertura vazia.** Um cabeçalho sozinho no primeiro segundo, com o conteúdo chegando depois. O
    herói chega inteiro no primeiro segundo (seção 5.1).

---

## 8. Como conferir por observação

Antes de dizer que terminou, extraia quadros e olhe. A lista abaixo é o que se olha, na ordem. Cada
item é respondido com sim ou não, sem "mais ou menos".

**Quadros a extrair:** o segundo 0, o meio de cada frase falada, o quadro logo antes e logo depois de
cada corte de fala, e o último quadro.

1. **Costura.** No quadro ampliado em volta de y = 956, existe alguma linha, sombra ou mudança de cor
   que não seja o fim de um vídeo e o começo do outro? Se existe, reprovado.
2. **Zona quieta.** Algum elemento do painel entra abaixo de y = 786? Se entra, ele vai brigar com a
   legenda. Reprovado.
3. **Zona segura de cima.** Tem conteúdo acima de y = 150? Reprovado.
4. **Um destaque só.** No quadro, quantas manchas de cor de destaque existem? Se não for exatamente
   uma, reprovado. E ela é a coisa que a voz fala nesse segundo? Se não for, reprovado.
5. **Preenchimento.** Meça o objeto herói. Ele ocupa entre 580 e 870 px de largura? Se for menor,
   reprovado.
6. **Contagem de elementos.** Conte tudo que é visível. Passou de sete, reprovado.
7. **Eco.** Leia a legenda do quadro e leia o texto do painel. São a mesma frase? Reprovado.
8. **Continuidade.** Ponha lado a lado o quadro de antes e o de depois de cada corte de fala. O painel
   continua o mesmo mundo, na mesma posição, com o mesmo herói? Se não, reprovado.
9. **Evento por frase.** Percorra os quadros do meio de cada frase. Existe alguma frase inteira em que
   nada mudou no painel, sem que isso seja um descanso logo depois de um evento grande? Reprovado.
10. **Grão.** Amplie um pedaço liso do fundo em 400%. Tem textura? Se estiver liso, reprovado.
11. **Legenda em uma linha.** Em todos os quadros com legenda, ela tem uma linha só e cabe dentro das
    margens de 56 px? Se qualquer grupo vazou ou quebrou, reprovado.
12. **Legibilidade da legenda.** Pegue o quadro de fundo mais claro e o de fundo mais escuro do corte.
    A legenda lê nos dois? Se em algum ela some, o contorno ou o preenchimento estão errados.
13. **Movimento decidido.** Veja o corte em velocidade normal, sem som. Alguma coisa se mexe sem
    motivo, gira em loop ou fica respirando? Reprovado.
14. **Ritmo medido.** Rode o `ritmo_painel.py` da seção 5.2 no `painel.mp4`. Ele reprovou por trecho
    parado ou por abertura fraca? Reprovado, e o conserto vai no beat que ele apontou.
15. **Pílulas.** Conte os beats em que a única coisa que muda é uma pílula ou rótulo com a palavra da
    fala. Se passar de um em cada quatro beats, o painel está ecoando a legenda em pedaços. Reprovado.

---

## 9. O meio do painel: desenho por padrão, tela real por exceção

**O padrão é o painel autorado, e ele não muda.** Todo corte nasce desenhado, com as peças do
registro, e continua saindo assim. Esta seção abre um caminho a mais, ela não troca o caminho
principal. Gravação de tela entra em beat específico, com critério escrito, e nunca como jeito mais
rápido de encher o painel. Captura de tela crua em formato vertical é pequena, poluída e diz menos
que um desenho bem feito, então liberar geral pioraria o pacote inteiro.

O que a tela real resolve é um buraco específico, e só ele. Quando o vídeo é uma demonstração, o
painel autorado mostra a ideia do que aconteceu, e ideia não convence: a pessoa precisa ver a coisa
acontecendo no produto para acreditar. Só isso. Saber **qual** é a ferramenta é outro problema, e
ele se resolve com o logo de verdade ou com um mock que carregue esse logo, nunca gastando aqui uma
janela de tela.

**De onde a tela vem.** Duas origens, nesta ordem, e a primeira que existir ganha:

1. uma gravação de tela separada, `materiais-de-trabalho/fonte/tela.mp4`, de quem gravou a tela e a
   câmera em arquivos diferentes;
2. **a própria fonte do vídeo**, quando ela for um compartilhamento de tela com a webcam num canto.
   Nesse formato a tela já está no mesmo arquivo do rosto: a face sai do encarte da webcam e a tela
   sai de outra região do mesmo quadro. Pedir um arquivo separado aqui é pedir uma coisa que já se
   tem, e rebaixar para desenho um beat que tinha prova disponível.

Quem faz o teste de qual das duas é o caso, e com quais números, é a `SKILL.md` do
`/flow-reels:produzir`, seção 2.5. Duas coisas valem dos dois lados. **Print de banco de imagem não é
origem:** a tela vem da gravação do próprio vídeo ou não vem, e imagem de tela pega na internet é
ilustração, que é o proibido 1 da 9.2. E **quando a tela vem da fonte, o recorte nunca pega a região
da webcam**, pela trava da 9.4.

De onde o arquivo vem é a única coisa que muda. O teste da 9.1, os proibidos da 9.2, a anotação da
9.3, o recorte da 9.4 e o orçamento de duas janelas continuam iguais para as duas origens.

### 9.1 O teste, em uma pergunta

> **Este beat é o produto fazendo alguma coisa que quem assiste precisa acreditar que aconteceu?**

A pergunta se responde olhando o beat, não discutindo. Se a resposta é sim, tela real é permitida
neste beat. Se a resposta é "seria legal ver", a resposta é não.

Os dois casos que passam no teste:

| caso | como reconhecer |
|---|---|
| ação numa interface | a fala descreve alguém fazendo: clica aqui, escreve o comando, arrasta, aprova |
| resultado que aparece | a fala afirma o que voltou: o arquivo criado, o número que mudou, os três resultados que chegaram |

O segundo caso é o mais forte dos dois. Desenho mostra o resultado que você desenhou, tela mostra o
resultado que aconteceu. Quando a frase é uma afirmação de fato sobre o produto, a prova vale mais
que a ilustração.

**Os dois casos têm a mesma raiz: a fala afirma um fato.** Beat em que a fala só nomeia a ferramenta
não entra aqui, por mais que a tela dela seja bonita. Isso é reconhecimento, e reconhecimento tem
resposta melhor e mais barata do que uma gravação recortada.

**O que saiu daqui, e para onde foi:**

| caso que já passou no teste | onde ele está agora |
|---|---|
| tela que se reconhece, ou seja o beat só pede que a pessoa identifique a ferramenta numa olhada | caminho do reconhecimento da matriz de representação: **logo de verdade** do acervo quando identificar é tudo que o beat pede, ou **mock autorado com o logo real dentro** quando o beat precisa da forma da interface, e a palavra dita quando nem isso serve |

O caso saiu porque a resposta dele ficou melhor fora. Um logo real lê em meio segundo no celular, e
um mock desenhado nos tokens da marca entrega a forma inteira limpa; uma gravação recortada da mesma
coisa chega pequena, poluída e cara, e ainda gasta o orçamento de 9.2 que o beat de crença vai
precisar. Reconhecer não é acreditar: quem só precisa saber qual é a ferramenta não precisa de prova.
Não traga o caso de volta.

### 9.2 Quando ela não é permitida

Cinco situações. As quatro primeiras já estragaram corte; a quinta é a que a matriz de representação
fechou, e é a mesma que saiu da tabela da 9.1:

1. **Para ilustrar ideia abstrata.** "Isso economiza tempo", "o processo fica mais simples". Não há
   nada para acreditar, há uma ideia para representar, e representar é trabalho de desenho.
2. **Para preencher tempo.** Beat sem transformação não se conserta com tela, se conserta com beat.
3. **Para mostrar o que o desenho explicaria melhor.** Comparação de dois caminhos, sequência de
   etapas, número que cresce, arquitetura. Nesses o desenho ganha sempre, porque ele mostra só o que
   importa e a tela mostra tudo.
4. **Porque a gravação existe e autorar dá trabalho.** Este é o motivo real por trás da maioria dos
   casos anteriores, e é o que esta permissão mais convida. Se a justificativa escrita no beat-sheet
   não responde a pergunta de 9.1 com um fato, o beat volta a ser desenhado.
5. **Só para a pessoa reconhecer a ferramenta.** "Usando o navegador", "lá dentro da ferramenta de
   conversa". A fala nomeia e não afirma nada, então não há fato para provar. Reconhecimento se
   resolve com o logo de verdade, ou com um mock autorado carregando esse logo quando o beat precisa
   da forma da interface. Gastar uma janela de tela aqui é queimar o orçamento no beat que menos
   precisa dele.

Orçamento, para a exceção continuar exceção: **no máximo duas janelas de tela real por corte, e no
máximo um terço da duração do corte com tela em cena.** Um corte de 36 s aceita até 12 s de tela,
distribuídos em no máximo duas janelas. Passou disso, o corte deixou de ser um corte com prova e
virou uma captura de tela com legenda.

**Orçamento estourado degrada o beat para mock autorado, nunca para nada.** Gasto o orçamento, os
beats seguintes que pediriam tela real viram desenho: a forma daquela interface, desenhada nos
tokens da marca, com o logo de verdade dentro quando a coisa for uma marca. A cena não fica vazia
por causa de contabilidade, e o nome dito sozinho não substitui o beat. Vale para os dois motivos de
estouro, o da segunda janela e o do terço da duração, e vale também quando a região pedida não
sobrevive ao recorte da 9.4 ou está debaixo da webcam.

### 9.3 A tela nunca entra crua

A tela é o **substrato**. Quem explica é a anotação autorada por cima dela. Tela crua sem anotação é
o defeito que esta permissão mais produz, e ele tem cara conhecida: uma janela pequena, cheia de
elemento que ninguém olha, enquanto a voz fala de uma coisa que está em algum lugar ali dentro.

**Toda janela de tela real carrega, no mínimo:**

- **um destaque na região que a fala aponta.** Contorno ou sublinhado na cor de destaque, nunca
  preenchimento em cima da tela, que taparia justamente o que se quer provar. Continua valendo a lei
  do acento da seção 3: um destaque ativo por quadro, e ele é a coisa que a voz está falando naquele
  segundo;
- **um rótulo autorado**, de 34 px no mínimo, nomeando o que aconteceu. Ele nomeia, não repete a
  legenda. "Três arquivos criados" serve. Transcrever a frase da voz é o defeito 2 da seção 7;
- **um recorte que já aproxima do que está sendo falado**, pela regra de 9.4.

Duas coisas que a tela real não muda:

- **O grão continua por cima de tudo**, inclusive por cima da tela. Ele já é aplicado no painel
  inteiro, então não se acrescenta uma segunda camada só para a imagem.
- **As cores da tela não são acento.** A tela chega com as cores dela e isso é esperado. Se ela tem
  uma área saturada grande que compete com o destaque, escureça a tela fora da região destacada até
  ela ficar claramente em segundo plano. A tela é o fundo da prova, o destaque é o que se olha.

### 9.4 Enquadramento: recortar, nunca encolher

A gravação é 16:9 e a área útil do painel é 968 x 636. Tela inteira nunca cabe com texto legível, e a
conta mostra por quê: uma gravação de 1920 px de largura reduzida para caber em 968 px encolhe cada
pixel para 0,50, e um texto de interface de 15 px vira 7 px na tela do celular. O menor texto
autorado do pacote tem 34 px.

**A regra, então, é recortar a região que a fala nomeia, nunca encolher a tela toda.**

Os números da janela:

| medida | valor |
|---|---|
| largura da janela no painel | de 580 a 870 px, o mesmo orçamento do objeto herói |
| altura da janela | até 490 px, que é o 16:9 de 870 e cabe nos 636 de área útil |
| fator de escala do recorte | nunca abaixo de 1,0. Alvo de 1,3 a 1,8 |
| texto da interface depois da escala | 22 px no mínimo |

O fator é a largura da janela dividida pela largura do recorte. Uma janela de 870 px com fator 1,5
pede um recorte de 580 px de largura no bruto, que numa gravação de 1920 px é perto de um terço da
tela. É isso mesmo: **o recorte é apertado por definição.** Ampliar é o que torna a tela legível no
celular.

Por que 22 px e não 34 px: o piso de 34 px vale para texto autorado, que é o que precisa ser lido. O
texto dentro da tela não precisa ser lido para o beat funcionar, porque quem carrega o sentido é o
rótulo autorado. Os 22 px são o piso para a tela parecer real em vez de borrão, e é um número que se
mede no quadro.

**A região da webcam é proibida, quando a tela vem da fonte.** Na fonte que é compartilhamento de
tela, o encarte da webcam está dentro do mesmo quadro de onde sai o recorte. Recorte que pega esse
encarte põe **o mesmo rosto duas vezes no mesmo quadro**, um no painel de cima e outro no de baixo, e
é um defeito que só aparece depois, com a legenda e o painel já feitos por cima dele. O retângulo
proibido é o encarte inteiro, não a caixa de rosto da etapa 1, que é menor que ele. A medição, a
conta do cruzamento e a margem estão na `SKILL.md` do `/flow-reels:produzir`, seção 2.5.

**Como escolher o recorte, na ordem:**

1. Leia o campo `legenda` do beat e sublinhe o elemento que a fala nomeia. É ele que tem que estar no
   quadro, inteiro.
2. Extraia um quadro cheio da gravação no instante do beat e olhe. Para ler a coordenada em pixel,
   a folha de contato com grade serve para qualquer vídeo, e o comando está na `SKILL.md` do
   `/flow-reels:produzir`, etapa 2.
3. Marque o retângulo do elemento e cresça a partir dele só até ele ficar reconhecível no contexto.
   Um campo de busca sozinho não diz nada, o campo de busca com a barra da janela em volta diz.
4. Calcule o fator. Abaixo de 1,0 o recorte está grande demais: tire contexto, nunca o elemento.
5. Tela vinda da fonte: confira que o recorte não cruza o retângulo da webcam. Cruzou, mova o recorte
   ou tire contexto do lado do encarte, nunca deixe passar "só um pedacinho".
6. Se mesmo tirando contexto o elemento não cabe, ou se ele só existe debaixo da webcam, o beat está
   pedindo o que não se pode recortar. Quebre em dois beats com duas regiões, ou desenhe o beat como
   mock autorado.

**Como conferir que o elemento falado não foi cortado:** extraia o recorte já escalado para o tamanho
final da janela, **no primeiro e no último quadro da janela**, e responda sim ou não a três
perguntas. O elemento que a frase nomeia está inteiro dentro do quadro? O texto dele lê sem apertar
os olhos? O que a fala afirma é visível ali? Os dois quadros são obrigatórios porque a tela se mexe:
menu que abre, lista que rola e resultado que empurra o layout tiram o elemento do recorte no meio da
janela, e quem confere só o primeiro quadro entrega meia janela certa.

### 9.5 Continuidade: a tela entra dentro do mundo

Mesmo com tela real vale a lei da seção 2: o painel é **um mundo só**. A tela não é uma segunda tela
que substitui o painel, ela é conteúdo que aparece dentro do herói que já estava em cena.

- **A janela nasce dentro do herói.** O card, a caixa de comando ou o que estiver carregando o corte
  abre e a tela aparece dentro dele. A moldura autorada continua visível em volta, e é ela que diz
  que o mundo é o mesmo.
- **A entrada usa a chegada de sempre**, 800 ms, subindo 64 px, com opacidade cheia no primeiro
  quadro. Sem fade, sem zoom de câmera, sem cortina.
- **A saída é o wipe de 167 ms, ou o herói fechando por cima.** O herói permanece em cena depois,
  porque trocar o herói no meio do corte continua proibido.
- **Permanência mínima de 3 s por janela.** A tela entra, cumpre o beat e fica pelo menos até o fim
  da frase seguinte. Tela que entra e sai a cada frase pisca, e painel que pisca lê como slideshow,
  que é exatamente o que o pacote evita.
- **Dentro da janela a tela roda no tempo natural dela**, sem acelerar e sem congelar em laço. Se o
  trecho gravado é mais curto que a janela, a janela encurta. Congelar o último quadro por segundos
  conta como parado e reprova pela cadência da seção 5.
- **A tela não reinicia no corte de fala.** Vale a mesma regra do painel: se dois trechos de fala
  foram costurados, a janela continua de onde estava, ela não volta ao começo.

### 9.6 O que se olha antes de aprovar uma janela de tela

Sim ou não, sem "mais ou menos". Esta lista soma com a da seção 8.

1. O beat tem justificativa escrita, e ela responde a pergunta de 9.1 com um fato, no lugar de dizer
   que fica mais bonito?
2. A janela tem destaque na região falada e rótulo autorado de 34 px no mínimo?
3. O recorte tem fator 1,0 ou mais, e o texto da interface passa de 22 px no quadro final?
4. O elemento que a fala nomeia está inteiro no primeiro e no último quadro da janela?
5. A moldura autorada aparece em volta da tela, ou a tela tomou o painel inteiro?
6. A janela dura pelo menos 3 s, e o corte tem no máximo duas janelas somando no máximo um terço da
   duração?
7. O grão está por cima da tela também? Amplie um pedaço liso da tela em 400% e olhe.
8. Tela vinda da fonte: o primeiro e o último quadro da janela estão **sem nenhum pedaço da pessoa**?
   Cabelo, ombro, mão, microfone e a moldura do encarte da webcam contam como pedaço. Rosto no painel
   de cima com rosto no painel de baixo é o defeito que esta pergunta existe para pegar.

## 10. Marca na tela: o logo de verdade, sempre

Quando o painel precisa mostrar uma marca, ela entra com **o logo dela**, e nunca com um desenho
parecido. Forma aproximada é pior que não mostrar: quem conhece a marca percebe o erro na hora e
para de confiar no resto, e quem não conhece aprende errado.

O acervo vem no pacote, em `componentes/logos/`, com vinte marcas. **Leia
`componentes/logos/README.md` antes de autorar qualquer painel que nomeie uma marca**, porque ele
diz o que já está lá, como baixar o que falta e quando a silhueta de uma cor não serve.

Sem o arquivo no acervo, existem duas saídas e nenhuma terceira:

1. baixar, com `flow-reels componentes/baixar-logo <marca>`;
2. não mostrar a marca e resolver o beat com palavra.

Desenhar parecido não é uma das duas. A peça `tile-de-logo` denuncia a falta em vez de improvisar:
o quadro sai hachurado com o aviso, o navegador registra a reclamação e o nome entra em
`FC.logosAusentes`. Quadro entregue com tile nesse estado é defeito de entrega, não detalhe.
