# Os sete critérios

São sete, e são poucos de propósito. **Um defeito, um dono.** Cada critério nomeia uma única skill
responsável por ele, e nenhum defeito aparece em dois critérios ao mesmo tempo.

A razão é prática. Lista longa de critério parecido faz o agente escolher o critério mais fácil de
alegar como cumprido e seguir em frente. Quando quatro itens diferentes falavam do painel, "painel
vivo" virou "painel que nunca fica parado", e a forma mais barata de nunca ficar parado é girar um
ícone para sempre, que é exatamente o defeito que o critério queria impedir.

Cada critério abaixo traz: o que é, a skill dona, um exemplo que passa, um exemplo que falha, e como
conferir de forma concreta. **"Como conferir" não é opinião.** Ou é um comando que imprime um
resultado, ou é um quadro extraído do vídeo que se olha com os olhos.

| # | critério | dona do defeito |
|---|---|---|
| 1 | a abertura se sustenta sozinha, e o formato declarado se cumpre | `/flow-reels:planejar` |
| 2 | o corte é limpo, sem fala amputada, e fecha em vez de parar | `/flow-reels:planejar` |
| 3 | a legenda é uma linha só, na costura, legível | `/flow-reels:produzir` |
| 4 | o painel é um mundo só, com algo acontecendo a cada frase | `/flow-reels:produzir` |
| 5 | a zona segura é respeitada | `/flow-reels:produzir` |
| 6 | a entrega está no formato certo, e sozinha na pasta do corte | `/flow-reels:produzir` |
| 7 | nenhuma marca é desenhada à mão | `/flow-reels:produzir` |

**Na Fábrica 2.0** (`"motor": "2.0"` no `setup.json`), os critérios 3 a 7 ganham medida automática no
vídeo pronto, com um comando só:

```
flow-reels produzir/conferir_reel --projeto projetos/<vídeo> --corte NN
```

Ele roda nove gates: ritmo (pelos eventos do compositor), zonas seguras, contraste do texto sobre o
vídeo, legenda sobre o rosto, sincronia da legenda com a fala, emendas do editor de fala, volume
(-14 LUFS), excesso de transições e o formato de entrega. Na 2.0 a legenda não fica mais presa à
costura: o critério 3 passa a ser "uma linha, legível, sincronizada e fora do rosto", e o critério 4,
"cada cena é um lugar e algo muda a cada 2 a 3 s". Os critérios 1 e 2 continuam sendo do planejamento.

Duas regras de medida que valem saber antes de discutir um resultado: os quadros no meio de uma
transição ficam fora das zonas, do rosto e do contraste (ali a cena está de passagem); e a legenda, que
tem contorno de 3 px em volta da letra, é medida contra o contorno, porque é ele que a separa de
qualquer fundo. O excesso de transições ainda é só aviso, até o teto ser calibrado.

---

## 1. A abertura se sustenta sozinha, e o formato declarado se cumpre

**O que é.** Duas coisas que são a mesma falha vista de dois ângulos.

A primeira: quem nunca viu o vídeo longo entende o assunto e a promessa ouvindo só as primeiras
frases do corte, sem nenhum contexto de fora. Nessas primeiras frases ele ouve, com todas as letras,
qual é a ferramenta ou o assunto concreto, o que sai dali e, quando a afirmação vale só em certa
situação, qual é a situação. Falado, não escrito na tela.

A segunda: o corte cumpre o formato que o brief declarou. Uma **afirmação** que abre pela introdução
do vídeo não é uma afirmação com um defeito, é um formato que ninguém escolheu; um **trajeto** com
três dos quatro blocos não é um trajeto incompleto, é outra coisa.

**Dona:** `/flow-reels:planejar`. As leis completas estão em
`skills/planejar/referencias/GANCHO.md`, seção 3, os seis eliminadores, e em
`skills/planejar/referencias/FORMATOS.md`, os dois formatos e a tabela do que muda de um para o outro.

**Passa:** "Lista de tarefas é o motivo de você não terminar as suas tarefas. Eu troquei a minha por
uma agenda, e o que sobrou de trabalho por semana caiu pela metade." O assunto aparece nas primeiras
palavras, nenhum pronome aponta para fora, e a lacuna aberta é fechada dentro do corte.

**Passa também:** "A gente vai instalar o plugin que dá um ecossistema de skills para o seu agente
de código, e isso leva trinta segundos." É um trajeto abrindo pela introdução do vídeo, que é o que
esse formato pede: a promessa nomeia o resultado e o meio, e a saudação ficou de fora.

**Falha:** "Aí eu fiz isso que eu te falei e resolveu tudo." Três defeitos de uma vez: "isso" não tem
antecedente, "que eu te falei" aponta para um trecho que ficou no vídeo longo, e "resolveu tudo" não
diz o que foi resolvido.

**Falha mesmo soando perfeita:** "Não precisa usar o modelo mais caro, o menor dá conta." A frase é
completa, nomeia o assunto e afirma algo verdadeiro. Ela vale **dado alguma coisa**, e essa coisa
ficou no vídeo: dá conta de qual trabalho? Isso é o eliminador do trabalho nomeado, e ele derruba
depois de o candidato ter passado no do assunto nomeado.

**Como conferir.**

1. Abra o `GANCHOS.md` e confira que a leitura fria daquele candidato veio do subagente leitor frio,
   com as três respostas registradas, e que o campo "Contexto que falta" está preenchido, nem que
   seja com "nenhum". Leitura fria escrita por quem escolheu o candidato não conta, porque quem
   escolheu já sabia o assunto.
2. Confira que o candidato **declarou o formato** antes dos eliminadores, e que o brief e o corte
   cumprem o formato declarado. Se é `trajeto`, os quatro blocos estão na seção 3 do brief, nesta
   ordem: a promessa, as etapas do caminho, o resultado acontecendo e o destino. Faltando o destino,
   reprovado. Se é `afirmacao`, a abertura não é a introdução do vídeo e não existe bloco de
   destino.
3. Leia a terceira resposta da leitura fria. Se ela pergunta **para que serve** ou **em que
   situação isso se aplica**, e não apenas **o que é**, o candidato tinha caído no trabalho nomeado
   e não deveria ter chegado à produção. Condição não se paga com segmento de contexto.
4. Leia a primeira resposta do subagente. Se ela for vaga ("fala sobre produtividade", "parece
   útil") ou genérica ("uma ferramenta de IA"), está reprovado, porque caiu no eliminador do assunto
   nomeado. Gancho fraco não se conserta reescrevendo: o candidato volta para o pool como
   descartado, com o motivo escrito no `GANCHOS.md`.
5. Confira que o gancho saiu de **um span contínuo** do áudio, e não de dois trechos costurados. No
   brief, a linha "Span na transcrição" traz um intervalo só. Dois intervalos ali significa que o
   candidato caiu no span contínuo e não deveria ter chegado à produção. Costurar trechos distantes
   é liberdade do corpo, nunca do gancho.
6. Se o campo "Contexto que falta" tem conteúdo, confira na seção 3 do brief que existe um segmento
   de papel `contexto` pagando essa dívida, tocando logo depois do gancho e nunca antes dele. A
   ordem do corte é gancho, contexto, prova, fechamento.
7. Percorra a fala inteira do corte procurando "isso", "ele", "essa parte", "como eu falei", "aquele
   caso". Todo antecedente tem que estar dentro do corte. Se não estiver, o segmento cresce para
   incluí-lo ou o segmento cai.

---

## 2. O corte é limpo, sem fala amputada, e fecha em vez de parar

**O que é.** Nenhuma entrada e nenhuma saída de segmento corta no meio de uma palavra, de uma sílaba
ou de uma respiração. As emendas entre trechos não distantes soam como fala contínua. E o último
segmento **termina**: numa virada que fecha, num próximo passo concreto, num pensamento completo que
para, ou na transição em que a pessoa muda de assunto. O fim ruim é um só, o corte no meio do
pensamento, e ele é defeito de seleção, não de montagem.

**Dona:** `/flow-reels:planejar`, que fecha os pontos. A lei completa está em
`skills/planejar/referencias/CORTE-LIMPO.md`.

**Passa:** o ponto de entrada cai dentro de um silêncio de verdade, medido no áudio, logo antes da
primeira palavra. Quem ouve não percebe que ali houve uma emenda.

**Falha:** o ponto de entrada foi copiado do campo `inicio` da palavra no `palavras.json`, e o corte
abre com meia sílaba ou com o "trrr" da inspiração. O alinhador estica a palavra para dentro do
silêncio, então tempo de palavra sozinho nunca fecha um ponto de corte.

**Como conferir.**

```
flow-reels planejar/energia_audio \
  projetos/<video>/materiais-de-trabalho/transcricao/audio16k.wav 412.8 431.2
```

O script imprime o envelope de energia em volta de cada tempo e aponta onde há silêncio de verdade,
que é a janela abaixo de 8% da fala plena por pelo menos 150 ms. **Todo ponto de entrada e de saída
tem que cair dentro de um silêncio apontado por ele**, não perto de um.

Depois do corte montado, a conferência final é com o ouvido: ouça os 2 primeiros e os 2 últimos
segundos, e os 2 segundos em volta de cada emenda. Palavra picada aparece na hora, e fim que não
fecha também: se ao terminar você espera mais uma frase, o corte parou, não terminou.

---

## 3. A legenda é uma linha só, na costura, legível

**O que é.** Cada grupo de legenda ocupa uma única linha, centrado na divisão entre o painel e a
face, com preenchimento escuro e contorno branco, e lê tanto sobre cena clara quanto sobre cena
escura.

**Dona:** `/flow-reels:produzir`. Os valores estão em
`skills/produzir/referencias/PADRAO-VISUAL.md` seção 6, e a receita em
`skills/produzir/referencias/RECEITA-TECNICA.md` seção 4.

**Passa:** grupo dentro do teto de caracteres da seção 6 do `PADRAO-VISUAL.md`, que é o dono desse
número, medido em pixels contra a largura útil, tamanho 116, contorno 5, sombra 1, `Alignment 5`,
quebra na pontuação, e a legenda troca junto com a voz.

**Falha:** o grupo quebrou em duas linhas e invadiu o painel, ou a legenda saiu fina e some quando a
plataforma comprime. Legenda fina quase sempre é a mesma causa: o arquivo de fonte entregue ao
queimador era uma fonte variável, e o eixo de peso foi ignorado, então ela desenhou no peso padrão,
que costuma ser Light.

**Como conferir.**

1. Leia a saída do `legenda.py`. Ele imprime quantos grupos saíram e qual é o mais largo em pixels.
   Se ele avisar que algum grupo vaza, resolva antes de queimar.
2. Confirme que `--arquivo-fonte` apontou para uma instância **estática**, e não para a variável.
3. No corte pronto, extraia a faixa da costura em pelo menos quatro instantes com legenda, incluindo
   o quadro de fundo mais claro e o de fundo mais escuro do corte:

```
cd projetos/<video>
ffmpeg -y -ss 5.0 -i corte-01/corte-01.mp4 -frames:v 1 -vf "crop=1080:420:0:750" \
  materiais-de-trabalho/corte-01/quadros/costura-05.png
```

4. Em cada quadro: uma linha só, dentro das margens, contorno visível, texto legível. Qualquer "mais
   ou menos" conta como reprovado.

---

## 4. O painel é um mundo só, com algo acontecendo a cada frase

**O que é.** O painel de cima é um único ambiente contínuo, com um objeto herói que muda de estado
conforme a fala avança. Não é uma sequência de telas trocadas, e não é um cenário parado com um
enfeite girando.

**Dona:** `/flow-reels:produzir`. A lei está em `skills/produzir/referencias/PADRAO-VISUAL.md` seções 2 e 5, e o plano
que ele executa vem do `beats.yaml` do `/flow-reels:planejar`.

**Passa:** o mesmo objeto herói está em cena do primeiro ao último segundo, na mesma posição, e a
cada frase falada alguma coisa nele muda: um item entra na lista, o número vira outro, o estado passa
de errado para certo. Um corte de fala não reinicia o mundo.

**Falha, dos dois lados opostos:**

- **Parado.** Uma frase inteira se passa e nada mudou na tela, sem que isso seja um descanso logo
  depois de um evento grande. Também é parado o painel que só troca pílulas com a palavra da fala,
  e a abertura em que o herói ainda não chegou inteiro no primeiro segundo.
- **Falso movimento.** Um ícone gira em loop, um card pulsa, alguma coisa flutua sem fim. Isso é
  movimento perpétuo, não é evento, e existe só para fingir que a tela está viva.

**Como conferir.**

0. Meça o `painel.mp4` antes de montar. Reprovou, o painel volta; a lei da medida está em
   `skills/produzir/referencias/PADRAO-VISUAL.md` seção 5.2.

```
flow-reels produzir/ritmo_painel \
  projetos/<vídeo>/materiais-de-trabalho/corte-NN/painel.mp4 \
  --beats projetos/<vídeo>/materiais-de-trabalho/corte-NN/beats.yaml
```

1. Extraia o quadro do meio de cada frase falada e ponha em sequência. De um para o outro, alguma
   coisa mudou? Frase sem mudança reprova.

```
flow-reels produzir/painel --painel painel.html --saida quadro.png --so-quadro 7.4
```

2. Extraia o quadro imediatamente antes e imediatamente depois de cada corte de fala. É o mesmo
   mundo, o mesmo herói, na mesma posição? Se o painel reiniciou na emenda, reprova.
3. Assista ao corte inteiro em velocidade normal, **sem som**. Alguma coisa se mexe sem motivo, gira
   em loop ou fica respirando? Reprova.
4. Leia a legenda do quadro e leia o texto do painel. Se forem a mesma frase, o painel virou eco da
   legenda em vez de mostrar a coisa, e reprova.

---

## 5. A zona segura é respeitada

**O que é.** Nada de importante encosta nas bordas nem na faixa onde a legenda passa, porque a
interface das plataformas cobre o topo, a base e a lateral direita.

**Dona:** `/flow-reels:produzir`. Os números estão em `skills/produzir/referencias/PADRAO-VISUAL.md` seção 1.

**Passa:** no painel de 1080 por 956, todo elemento vive entre y = 150 e y = 786, com margem lateral
de 56 px. A faixa de cerca de 170 px na base do painel fica livre, que é a zona quieta por onde a
legenda passa.

**Falha:** um card desce até y = 830 e a legenda queimada cai por cima dele. Na tela do celular isso
vira duas coisas disputando o mesmo espaço, e nenhuma se lê.

**Como conferir.**

1. Renderize um quadro do painel com as guias ligadas, que desenham as margens e a zona quieta.
2. Ou meça direto no quadro extraído: abra a imagem, olhe a faixa de y = 786 até y = 956 e confirme
   que ela está vazia. Depois olhe a faixa de y = 0 até y = 150.
3. No corte montado, extraia o quadro do topo e da base e confirme que nenhum texto encosta nas
   bordas:

```
cd projetos/<video>
ffmpeg -y -ss 12.0 -i corte-01/corte-01.mp4 -frames:v 1 \
  materiais-de-trabalho/corte-01/quadros/q-12.png
```

Elemento decorativo de fundo pode atravessar essas faixas. Conteúdo que precisa ser lido, não.

---

## 6. A entrega está no formato certo, e sozinha na pasta do corte

**O que é.** Duas coisas, e as duas são medidas, não estimadas. O mp4 final é exatamente o que as
plataformas esperam, e `projetos/<vídeo>/corte-NN/` contém esse mp4 e mais nada. Painel, face,
legenda, quadro de conferência e brief são material de trabalho e moram em
`materiais-de-trabalho/corte-NN/`, conforme
`skills/fabrica/referencias/PASTA-DO-VIDEO.md`.

**Dona:** `/flow-reels:produzir`. A tabela completa está em `skills/produzir/referencias/RECEITA-TECNICA.md` seção 1.

**Passa:** 1080 x 1920, 30 fps constante, H.264 em `yuv420p`, SAR 1:1 e DAR 9:16, `+faststart`, áudio
AAC, a duração dentro da faixa combinada no brief, e `ls corte-NN/` devolvendo uma linha só.

**Falha:** o arquivo saiu em `yuvj420p` porque a faixa de cor cheia do PNG vazou para o vídeo. Em
alguns aparelhos isso aparece como preto lavado e cor estourada, e o defeito não aparece na máquina
de quem produziu. Falha também a pasta do corte com o `painel.mp4`, o `face.mp4` e uma prévia ao
lado da entrega: quem abre não sabe qual dos quatro arquivos é o corte.

**Como conferir.**

```
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,pix_fmt,sample_aspect_ratio,display_aspect_ratio \
  -show_entries format=duration,size -of default=nw=1 projetos/<vídeo>/corte-01/corte-01.mp4

ls projetos/<vídeo>/corte-01/
```

A segunda conferência é a da pasta, e ela tem que devolver uma linha só, `corte-01.mp4`.

O `montar.py` já roda essa conferência no fim e imprime APROVADO ou REPROVADO. **Se ele disser
REPROVADO, o arquivo não vai para lugar nenhum**, nem para a página de revisão. Corrija e monte de
novo.

---

## 7. Nenhuma marca desenhada à mão

**O que é.** Toda marca que aparece no painel entra com o logo de verdade, vindo de
`componentes/logos/`. Nenhuma forma parecida, nenhum ícone genérico no lugar de marca nomeada, e
nenhum tile em estado de falta no quadro entregue.

**Dona do defeito:** `/flow-reels:produzir`. A lei está na seção 10 do `skills/produzir/referencias/PADRAO-VISUAL.md`.

**Passa:** o beat fala em Instagram e aparece o logo do Instagram, tirado do acervo.

**Falha:** o beat fala em Claude e aparece uma forma laranja parecida com o símbolo. Falha também
quando o tile aparece hachurado com LOGO AUSENTE, porque isso é o pacote avisando que o arquivo não
existe e ninguém resolveu.

**Como conferir.** Duas provas, as duas baratas: a saída do `painel.py` imprime as reclamações do
navegador, e logo ausente vira `console.error`. E olhar o quadro: tile hachurado se vê de longe.
Se a marca foi desenhada em vez de carregada, o console fica quieto, então essa parte se confere
com o olho, comparando com o logo real.

---

## Nenhum corte é entregue sem passar pelos sete

Os sete valem juntos, e não existe média: passar em seis não entrega. Um corte que falha em
qualquer um deles não é um corte pronto com um detalhe pendente, é um corte que ainda não está
pronto.

A ordem prática de conferência, porque ela economiza render:

1. Critérios 1 e 2 são conferidos **no planejamento**, antes de qualquer render. Gancho fraco e ponto
   de corte torto descobertos depois do painel pronto custam o painel inteiro.
2. Os critérios 4, 5 e 7 são conferidos **no painel**, antes da montagem.
3. Os critérios 3 e 6 são conferidos **no corte montado**, nos quadros extraídos e no ffprobe.

Reprovou, o conserto é feito pela skill dona do critério. Não se conserta legenda vazando mexendo no
gancho, e não se conserta gancho fraco aumentando o contorno da legenda. Trocar de dono no meio do
conserto é o jeito mais rápido de passar a tarde mexendo no arquivo errado.
