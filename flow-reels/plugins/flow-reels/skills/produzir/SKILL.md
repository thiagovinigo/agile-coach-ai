---
name: produzir
description: 'Produz o corte vertical a partir de um brief aprovado, do começo ao fim: enquadra a face, autora e renderiza o painel de cima, gera a legenda, monta o MP4 1080x1920 e sobe a página de revisão. Use quando o usuário disser ''produz o corte'', ''renderiza'', ''monta o short'', ''faz o corte 02'', ''gera o vídeo'', ou depois que ele aprovou os ganchos e o brief do `/flow-reels:planejar`. Não escolhe gancho nem decide o que vira corte, isso é do `/flow-reels:planejar`.'
---

# Produzir (/flow-reels:produzir)

> **Onde mora cada coisa.** Esta skill está em `${CLAUDE_SKILL_DIR}` e o plugin Flow Reels em
> `${CLAUDE_PLUGIN_ROOT}`. Caminhos como `referencias/...` e `scripts/...` são desta skill;
> `skills/...` e `componentes/...` são do plugin (o que a pessoa baixou fica em `componentes/` da pasta
> de trabalho e vale por cima); `projetos/`, `marca/`, `pautas/`, `setup.json` e `.env` são da pasta de
> trabalho, o diretório onde o Claude Code está aberto. Todo script roda com `flow-reels <skill>/<script>`,
> que está no PATH enquanto o plugin está ligado e já usa o Python e o ffmpeg certos
> (`flow-reels lista` mostra todos; `flow-reels instalar` prepara uma pasta nova).

Você é a produção. Entra um brief aprovado, sai um MP4 pronto para publicar e uma página onde a
pessoa assiste e aprova. Nada aqui é decisão de conteúdo: o gancho, o payoff e o beat-sheet já vieram
prontos do `/flow-reels:planejar`, e mexer neles agora é refazer o planejamento por conta própria.

**Antes de desenhar a primeira coisa, leia `referencias/PADRAO-VISUAL.md`.** É a lei do que aparece
na tela, e ela tem número e jeito de conferir. Os comandos e os valores exatos estão em
`referencias/RECEITA-TECNICA.md`. As peças do painel estão catalogadas em `componentes/REGISTRO.md`,
na raiz do pacote, e o molde de um painel inteiro que funciona é `componentes/EXEMPLO-PAINEL.html`.

**Se o lote tem mais de um corte aprovado, leia antes a seção "Vários cortes ao mesmo tempo".** Ela
muda quem faz o quê: você passa a produtor do lote e cada corte ganha o seu subagente.

---

## O que precisa estar pronto antes

**A árvore da pasta do vídeo está em
`${CLAUDE_PLUGIN_ROOT}/skills/fabrica/referencias/PASTA-DO-VIDEO.md`, e ela manda.** Em uma linha: a
pasta do corte guarda só o MP4 de entrega, e tudo que é material de trabalho vive debaixo de
`materiais-de-trabalho/`.

| item | onde | se faltar |
|---|---|---|
| brief aprovado do corte | `projetos/<vídeo>/materiais-de-trabalho/corte-NN/brief.md` | pare e chame o `/flow-reels:planejar` |
| beat-sheet do painel | `projetos/<vídeo>/materiais-de-trabalho/corte-NN/beats.yaml` | pare, sem beat-sheet o painel vira improviso |
| transcrição palavra a palavra | `projetos/<vídeo>/materiais-de-trabalho/transcricao/palavras.json` | pare e chame o `/flow-reels:transcrever` |
| vídeo bruto | `projetos/<vídeo>/materiais-de-trabalho/fonte/`, onde o `/flow-reels:transcrever` deixou | pare e pergunte |
| gravação de tela, só se algum beat traz o bloco `tela` | duas origens, nesta ordem: `projetos/<vídeo>/materiais-de-trabalho/fonte/tela.mp4` se existir, senão a própria fonte, quando ela for compartilhamento de tela com a webcam num canto (o teste está na 2.5) | nenhuma das duas serve: o beat volta ao `/flow-reels:planejar` para virar mock autorado, nunca para sumir |
| marca definida | `marca/tokens.json` | siga, mas avise: o corte vai sair com a marca de exemplo |

Confira os quatro primeiros antes de gastar render. Render feito em cima de brief errado é a forma
mais cara de errar neste pacote.

## As duas pastas de um corte

Um corte tem duas pastas, e a diferença entre elas é a regra desta skill:

```
projetos/<vídeo>/
├── corte-NN/
│   └── corte-NN.mp4                    A ENTREGA, e mais nada nesta pasta
└── materiais-de-trabalho/corte-NN/
    ├── brief.md                        veio do planejador
    ├── beats.yaml                      o plano do painel
    ├── contato.png                     a folha de amostras da face
    ├── contato-recorte.png             a folha do recorte, já aprovada por você
    ├── face.mp4                        1080 x 964, a fala já costurada
    ├── painel.html                     o mundo, autorado para este corte
    ├── painel.mp4                      1080 x 956, render do painel
    ├── legenda.ass                     a legenda no padrão do pacote
    ├── tela/                           os quadros da gravação de tela, quando algum beat pede
    └── quadros/                        os quadros extraídos do MP4 para conferência
```

**Nada além do `corte-NN.mp4` entra em `corte-NN/`.** Nem quadro de conferência, nem prévia, nem
arquivo com `_teste` no nome. Quem abre aquela pasta está procurando o vídeo pronto, e dez arquivos
lá dentro é exatamente a bagunça que esta árvore existe para acabar.

O único arquivo que atravessa a fronteira é o MP4: ele é produzido a partir do que está em
`materiais-de-trabalho/corte-NN/` e escrito direto em `corte-NN/corte-NN.mp4`, que é onde a página
de revisão vai procurar por ele.

---

## Vários cortes ao mesmo tempo

Quando a pessoa aprova mais de um gancho, os cortes **não entram em fila**. Nenhum corte depende do
outro: cada um tem a sua fala, o seu painel, a sua legenda e o seu MP4. O que é comum entre eles
(transcrição, áudio, marca, componentes) só é lido, nunca escrito. Então a produção do lote é
paralela, e o ganho de tempo é quase o número de cortes.

Um corte aprovado, você produz seguindo as etapas 1 a 4 aqui embaixo, com você mesmo na direção.
**Dois ou mais, você vira produtor do lote: abre um subagente por corte e cada um faz as etapas 1 a 4
inteiras, sozinho, dentro da pasta dele.**

### A regra dura: uma pasta, um dono

Cada subagente é **dono exclusivo das duas pastas do corte dele**, `projetos/<vídeo>/corte-NN/` e
`projetos/<vídeo>/materiais-de-trabalho/corte-NN/`, e não escreve em mais nada. Fora dessas duas,
tudo é somente leitura:

| caminho | quem escreve |
|---|---|
| `projetos/<vídeo>/corte-NN/` e `projetos/<vídeo>/materiais-de-trabalho/corte-NN/` | o subagente daquele corte, e só ele |
| `materiais-de-trabalho/transcricao/`, `materiais-de-trabalho/fonte/` | ninguém durante a produção, só leitura |
| `projetos/<vídeo>/transcricao.md`, `projetos/<vídeo>/GANCHOS.md` | ninguém durante a produção, só leitura |
| `marca/`, `componentes/`, o plugin | ninguém durante a produção, só leitura |
| `projetos/<vídeo>/revisao/`, `materiais-de-trabalho/logs/` | você, uma vez, no fim |

O que o subagente devolve para você é texto, na resposta dele. **Relatório que valha a pena guardar,
e saída longa de script que você quiser reler depois, vão para `materiais-de-trabalho/logs/`**, e
quem escreve lá é você, não eles.

Escreva isso no pedido de cada subagente, com essas palavras. Dois agentes escrevendo no mesmo
arquivo é o jeito clássico de perder trabalho sem ninguém perceber: o segundo salva por cima do
primeiro, nada dá erro, e o defeito só aparece na revisão, quando já se gastou render nos dois.

Ainda que um subagente veja um problema fora da pasta dele, por exemplo um beat-sheet furado ou uma
fonte faltando, ele **reporta para você** em vez de consertar. Quem conserta arquivo compartilhado é
você, com os subagentes parados.

### Teto de três ao mesmo tempo

**O teto vem do `max_paralelo` no `setup.json`, e o padrão é três.** Dispare no máximo esse
tanto de subagentes ao mesmo tempo; terminou um, entra o próximo da fila. Se a chave não
existir no arquivo, use três e siga, sem perguntar.

O motivo é o render do painel: cada um sobe um Chromium próprio, que come memória e CPU. Três
Chromium num notebook comum já é bastante; cinco deixam a máquina lenta o suficiente para o
render arrastar ou morrer no meio, e aí você perdeu os cinco em vez de ganhar tempo.

Três é o padrão, não uma lei da física, e por isso mora no `setup.json` em vez de estar decorado
aqui. Em máquina folgada vale subir, em notebook apertado vale baixar para dois. O que não muda é existir um teto: sem teto, o lote inteiro
depende de a máquina aguentar o pico, e ela avisa tarde.

### O que vai no pedido de cada subagente

Monte o pedido com estes campos, todos preenchidos, todos com **caminho absoluto**. Quem segue esta
skill não deveria ter que inventar nenhum deles:

| campo | o que é |
|---|---|
| `corte` | o número, `01`, `02`, e o título curto do brief |
| `pasta_de_trabalho` | `projetos/<vídeo>/materiais-de-trabalho/corte-NN/`, onde ele trabalha |
| `pasta_de_entrega` | `projetos/<vídeo>/corte-NN/`, que recebe só o MP4 final |
| `brief` | caminho do `brief.md` aprovado |
| `beats` | caminho do `beats.yaml` |
| `video_bruto` | caminho do arquivo de origem em `materiais-de-trabalho/fonte/` |
| `segmentos` | os trechos do corte, em `entrada:saída:deslocamento`, na ordem da montagem |
| `duracao_alvo` | a duração do corte montado, em segundos |
| `saida` | `projetos/<vídeo>/corte-NN/corte-NN.mp4` |
| `somente_leitura` | `materiais-de-trabalho/transcricao/palavras.json`, `materiais-de-trabalho/transcricao/audio16k.wav`, `marca/tokens.json`, o arquivo de fonte em `marca/fontes/`, `componentes/REGISTRO.md`, `componentes/EXEMPLO-PAINEL.html` |
| `doutrina` | `referencias/PADRAO-VISUAL.md` e `referencias/RECEITA-TECNICA.md`, caminhos absolutos |
| `tela` | só quando algum beat traz o bloco `tela`: a origem escolhida no passo 0 da 2.5, em caminho absoluto, e o retângulo proibido da webcam em `x:y:largura:altura` quando a origem for a própria fonte |
| `tarefa` | etapas 1 a 4 desta skill, do enquadramento ao MP4 conferido no ffprobe |
| `nao_faz` | não sobe página de revisão, não escreve fora das duas pastas dele, não põe nada além do MP4 na pasta de entrega, não altera brief nem beat-sheet, não publica nada |
| `relatorio` | o que ele devolve: pronto ou falhou, em que etapa, a causa em uma frase, e os caminhos completos do que gerou |

O subagente do corte **autora o painel ele mesmo**, com a doutrina na frente. Ele já é o contexto
limpo que a etapa 2 pede, então não abra mais um nível de subagente dentro dele: o pedido da etapa
2.2 vira o núcleo do pedido dele.

### Falha de um corte não derruba os outros

Cada corte é uma entrega independente, e é assim que você trata a falha:

1. **Não cancele o lote.** Os outros subagentes seguem até o fim.
2. **Nomeie a falha**: qual corte, em que etapa parou, qual a causa. "O corte 03 parou no render do
   painel, o Chromium não estava instalado" é útil; "deu erro no 03" não é.
3. **Entregue o que ficou pronto.** Três de quatro cortes prontos é um lote de três cortes, não um
   lote quebrado. A página de revisão sobe com os que existem.
4. **Diga como refazer só o que faltou**, apontando a etapa exata. O trabalho parcial que está na
   pasta de trabalho do corte não se joga fora: `face.mp4` pronto não se recorta de novo,
   `painel.mp4` pronto não se renderiza de novo.
5. **Duas falhas pelo mesmo motivo param o lote.** Se dois cortes morreram no mesmo ponto, o defeito
   não é do corte, é do ambiente ou da doutrina, e insistir só queima render.

### O que continua sequencial, e por quê

| etapa | paralela? | por quê |
|---|---|---|
| os cortes entre si | sim | não compartilham nada além de arquivo de leitura |
| enquadrar → painel → legenda → montar, dentro de um corte | não | cada etapa come a saída da anterior: a legenda precisa das durações do recorte, e a montagem precisa do painel e da face prontos |
| autorar o painel | não, e é o gargalo | é raciocínio, não processamento; já está delegado a um contexto limpo, e é por isso que paralelizar o conjunto vale mais do que picar as etapas |
| a página de revisão | não, e é só sua | ela lê a pasta inteira do vídeo e precisa de todos os cortes prontos |

---

## A produção 2.0

Com `"motor": "2.0"` no `setup.json`, o corte deixa de ser painel em cima e rosto embaixo e passa a ser
montado inteiro pelo compositor, cena a cena, com os oito modos, o vidro, a legenda animada e as
transições. O contrato de tudo está em `motor/MOTOR.md`, e o plano (`cenas.json`) vem pronto do
`/flow-reels:planejar`, junto com o `fala.mp4` e o `palavras-corte.json` que o editor de fala gerou.

Rode pelo `flow-reels` (ele usa o Python da pasta de trabalho e o ffmpeg completo), nesta
ordem, para cada corte:

1. **Rosto.** `flow-reels produzir/rosto --projeto projetos/<v> --corte NN` grava o `rosto.json` e uma folha
   de contato; olhe a folha. Fonte com a webcam num canto de gravação de tela: passe `--regiao x:y:w:h`
   da webcam.
2. **Visão, se o plano usa as peças da Onda 2.** Quando o `cenas.json` tem `"atras": true`, o modo
   `camadas`, `deteccao`, `maos`, `contorno`, `profundidade` ou um `logo-volume` com `segue`, rode
   `flow-reels produzir/visao --projeto projetos/<v> --corte NN` depois do rosto. Ele grava `visao/` (recorte da
   pessoa, fundo limpo, profundidade, mãos, corpo e objetos, quadro a quadro, contrato em `MOTOR.md` 2.6) e a
   `folha-visao.png`; **olhe a folha** (contorno colado na pessoa, cabelo inteiro, mãos com o lado certo)
   antes de renderizar. Leva uns 2 min para 36 s de vídeo vertical no M4. Precisa da pessoa filmada de frente,
   em plano médio e com a câmera parada: o fundo limpo é a mediana de vários quadros, e o que a pessoa nunca
   descobre é inventado (no teste, quase metade da parede). Se a gravação tem alguns segundos do cenário
   vazio no fim, o fundo sai de verdade. Saída 1 = a pessoa apareceu em menos da metade dos quadros: pare e
   olhe a folha. Sem essas peças no plano, pule este passo; com elas e sem a `visao/`, o motor recusa o plano
   dizendo o que rodar. Depois de reeditar o `fala.mp4`, rode de novo, sem `--so`. Copiar a pasta `visao/` de
   outro corte não serve: o `compor.py` vê que ela é de outro vídeo e segue sem ela. Com a visão na pasta,
   a legenda também foge das mãos sozinha (`MOTOR.md` 3.2; `"desvia_maos": false` desliga).
3. **Cena de painel, se houver.** Para cada cena `painel-rosto`, escreva um `painel-cN.html` no molde do
   `componentes/EXEMPLO-PAINEL.html`, com `window.DURACAO` igual à duração da cena, o tempo zero no
   início dela e o conteúdo a partir de y 230. Renderize com
   `flow-reels produzir/painel --painel <pasta>/painel-cN.html --saida <pasta>/painel-cN.mp4` e declare em
   `cenas.json` → `videos` (MOTOR.md 4.1).
4. **Conferir antes de gastar render.** `flow-reels produzir/compor --projeto projetos/<v> --corte NN --quadro <t>`
   em três instantes (a abertura, uma transição, o fim). Olhe cada PNG. Com peças da Onda 2, olhe também um
   gesto (as mãos e a legenda) e o pior instante de cada texto atrás de você (`atras` no `layout.jsonl`).
5. **Render.** `flow-reels produzir/compor --projeto projetos/<v> --corte NN` grava o `video.mp4` (sem som), o
   `eventos.json`, o `layout.jsonl` e os quadros de `contraste/`. Leva cerca de 2 s por segundo de vídeo.
   Para conferir rápido com som: `--previa` (540x960).
6. **Som e entrega.** `flow-reels produzir/audio --projeto projetos/<v> --corte NN` normaliza a voz em -14 LUFS,
   põe os efeitos sonoros nas transições e grava a entrega `corte-NN/corte-NN.mp4`. Se o `cenas.json` tem
   `"trilha"`, a música de `componentes/trilhas/` entra por baixo da voz e abaixa quando você fala
   (`MOTOR.md` 3.1); sem a chave, o som sai como sempre. A trilha só entra se o criador disse sim a ela
   para este vídeo: se ninguém perguntou, pergunte antes de rodar o `audio.py`.
7. **Gates.** `flow-reels produzir/conferir_reel --projeto projetos/<v> --corte NN`. Reprovou, conserte no dono
   do defeito (plano → planejador; render → aqui) e rode de novo só o que mudou. Os quadros no meio de
   uma transição não contam para zonas, rosto e contraste: ali a cena está de passagem. Na 4.3 são 12
   gates: os 9 de sempre, o 10 (som: densidade, arquivo repetido, efeito na sílaba tônica, pico), o 11
   (linguagem do episódio, N/A sem `"linguagem"` no plano) e o 12 (variedade, só aviso). Os gates 1 a 11
   não podem reprovar; o 12 é para olhar. Mudou o `eventos.json` (novo render), rode o `audio.py` de novo
   antes dos gates: ele grava o `sons.json` que o gate 10 lê. Depois da aprovação,
   `flow-reels produzir/linguagem registrar --projeto projetos/<v> --corte NN` (memória anti-repetição).
8. **Capa.** Escreva `materiais-de-trabalho/corte-NN/capa.json` (o título é a promessa do corte em até
   quatro linhas, a palavra de destaque, um selo curto com o assunto, o fundo e até dois logos em cor) e
   rode `flow-reels produzir/capa --projeto projetos/<v> --corte NN`. A capa sai em `corte-NN/corte-NN-capa.jpg`,
   ao lado do mp4, sempre com a foto da pessoa (`setup.json` → `capa.foto`, por padrão `marca/foto.jpg`,
   que o `/flow-reels:marca` pede no onboarding, recortada uma vez em `marca/foto-recorte.png`). Confira a `capa-grade.jpg`: é o recorte 3:4 que o perfil mostra.
9. **Revisão**, como na Etapa 5.

Os efeitos sonoros são do próprio pacote (`componentes/sons/`, gerados por `scripts/gerar_sons.py`), sem
licença de terceiro. Se o motor 2.0 falhar num corte, as etapas 1 a 4 abaixo continuam funcionando e
entregam o layout de sempre.

---

## Etapa 1, enquadrar a face

Objetivo: uma caixa fixa de recorte, escolhida olhando, conferida olhando.

1. Rode `scripts/enquadrar.py amostrar` no vídeo bruto.
2. **Olhe a folha de contato.** Ela vem com grade de oitavos e cruz no centro, e o script imprime a
   que pixel cada linha da grade corresponde.
3. Escreva a caixa em `x:y:largura:altura`, na proporção 1080 por 964, com os olhos perto do terço de
   cima e ar acima da cabeça.
4. Rode `scripts/enquadrar.py validar` com essa caixa, nos tempos do corte. **Olhe de novo.** Queixo
   cortado, topo da cabeça cortado ou pessoa fora do quadro reprovam a caixa.
5. Recorte a face com o comando que o `validar` imprime no fim, **escrevendo em
   `materiais-de-trabalho/corte-NN/face.mp4`**. As folhas de contato saem na mesma pasta. Corte
   costurado de vários trechos: um comando por trecho e a costura com o concat, receita em
   `RECEITA-TECNICA.md` seção 2.3.
6. Anote a duração de cada trecho com o ffprobe. Esses números são o deslocamento de cada
   `--segmento` na etapa 3, e errar neles joga a legenda fora de sincronia.

Caixa fixa funciona porque webcam em canto e busto em tripé não se mexem. Se a pessoa anda pelo
quadro, isso é caso de detecção de rosto com OpenCV, que não vem instalada: avise o usuário em vez de
entregar um recorte que perde a cabeça no meio.

---

## Etapa 2, autorar e renderizar o painel

Esta é a etapa que decide se o corte parece feito por gente. É também a que mais exige raciocínio,
então **ela é delegada a um subagente dedicado**, que trabalha só nisso, com a doutrina inteira na
frente e sem o resto da produção ocupando a cabeça dele.

Com um corte só, esse subagente é aberto por você aqui. Com o lote em paralelo, quem autora é o
próprio subagente do corte, que já tem o contexto limpo: o pedido de 2.2 entra no pedido dele e
ninguém abre mais um nível.

### 2.1 Por que delegar

Autorar o painel é desenhar um mundo: escolher o objeto herói, decidir como ele muda de estado a cada
frase, calcular o movimento quadro a quadro dentro de `render(t)` e ainda respeitar zona quieta, zona
segura, acento único e contagem de elementos. Misturar isso com recorte de vídeo e comando de ffmpeg
é o caminho conhecido para o painel virar uma sequência de slides. Um subagente por painel, com
contexto limpo.

### 2.2 O que vai no pedido do subagente

Abra o subagente e passe, sem resumir:

1. **o `beats.yaml` do corte**, inteiro, com os tempos em segundos e a fala de cada beat, **mais a
   linha de rotas da seção 4 do `brief.md`**, que diz, para cada coisa concreta nomeada na fala,
   qual rota o inventário decidiu e com que recurso: o arquivo do logo ou a peça de mock. Sem ela o
   subagente decide de novo, na hora de desenhar, o que o passo 0 já tinha decidido;
2. **os caminhos absolutos** de: `referencias/PADRAO-VISUAL.md`, `componentes/REGISTRO.md`,
   `componentes/EXEMPLO-PAINEL.html`, `marca/tokens.json` e a pasta de trabalho do corte,
   `materiais-de-trabalho/corte-NN/`, que é onde o `painel.html` nasce e onde ele fica;
3. **a duração exata do corte**, que é a duração da face montada;
4. **a tarefa**, nestes termos:

   > Autore o `painel.html` deste corte, 1080 x 956, seguindo `PADRAO-VISUAL.md` como lei e
   > `REGISTRO.md` como catálogo de peças. Um mundo só, um objeto herói que muda de estado, algo
   > acontecendo em cada frase, nada de animação perpétua, nada abaixo de y = 786, nada acima de
   > y = 150, um acento por quadro, grão por cima de tudo. Nenhuma cor escrita à mão: tudo sai dos
   > tokens. Todo movimento é conta dentro de `render(t)`, nunca transição de CSS. Mostre a ideia,
   > não a frase: pílula com a palavra que a legenda já está mostrando não é beat. A abertura é o
   > trailer: o herói inteiro em cena no primeiro segundo e três mudanças de verdade antes dos 5 s
   > (`PADRAO-VISUAL.md` seções 2 e 5.1). Nada fica parado mais de 2,5 s, e isso vai ser medido no
   > vídeo depois do render. Antes de dizer que terminou, renderize pelo menos quatro instantes com
   > `flow-reels produzir/painel --painel painel.html --saida quadro.png --so-quadro <t>`, **olhe cada
   > imagem** e corrija. Entregue o `painel.html` e diga quais instantes você olhou.

5. **o que ele não faz**: face, legenda, montagem e publicação não são dele.

Se algum beat do `beats.yaml` traz o bloco `tela`, faça **antes** a extração da seção 2.5 e
acrescente o parágrafo de lá a este pedido. O subagente precisa dos quadros já recortados em mãos,
senão ele autora um desenho no lugar da prova.

### 2.3 O que você confere quando ele volta

Não aceite "pronto" sem olhar. Renderize por conta própria o segundo 0, o meio de duas frases e o
último segundo, e passe a lista de observação do `PADRAO-VISUAL.md` seção 8. Devolva ao subagente com
o defeito nomeado e o quadro em mãos se qualquer item reprovar.

### 2.4 Renderizar o painel inteiro

```
flow-reels produzir/painel \
  --painel projetos/<vídeo>/materiais-de-trabalho/corte-NN/painel.html \
  --saida  projetos/<vídeo>/materiais-de-trabalho/corte-NN/painel.mp4
```

Assim que o `painel.mp4` sair, **meça o ritmo antes de montar**:

```
flow-reels produzir/ritmo_painel \
  projetos/<vídeo>/materiais-de-trabalho/corte-NN/painel.mp4 \
  --beats projetos/<vídeo>/materiais-de-trabalho/corte-NN/beats.yaml
```

Reprovou por trecho parado ou por abertura fraca, o painel volta para quem autorou, com os instantes
e o beat que o script apontou, e só depois se monta. Depois do conserto, meça só o trecho alterado
com `--janela inicio:fim`. A lei e o que cada reprova quer dizer estão em `PADRAO-VISUAL.md` seção
5.2. Montar um painel reprovado é gastar legenda e montagem num corte que vai voltar da revisão.

O render é a etapa longa. A medida está em `RECEITA-TECNICA.md` seção 7, que é a dona do número. O tempo
cresce com a duração do corte, então trate a medida como aproximação, não como promessa, e leia o
andamento que o script imprime. Se o Chromium não estiver instalado, o script diz o
comando exato para instalar.


### 2.5 Quando o beat-sheet pede tela real

Esta subseção só existe quando algum beat do `beats.yaml` traz o bloco `tela`, e ela roda **antes da
2.2**, porque o subagente do painel precisa dos quadros já extraídos. Sem esse bloco, o painel é
desenhado do começo ao fim e não há nada a fazer aqui.

A lei do que é permitido está em `referencias/PADRAO-VISUAL.md` seção 9. Leia o `por_que` do beat
antes de gastar extração: se ele não responde o teste de lá com um fato, não extraia nada e devolva
o beat ao `/flow-reels:planejar`.

**Passo 0, de onde a tela vem.** Duas origens, nesta ordem, e a primeira que existir ganha:

1. `materiais-de-trabalho/fonte/tela.mp4`, a gravação separada. É o caso de quem gravou a tela em um
   arquivo e a câmera em outro.
2. **A própria fonte**, o arquivo bruto que o `/flow-reels:transcrever` deixou em `materiais-de-trabalho/fonte/`,
   quando ela for um compartilhamento de tela com a webcam num canto. Aí a tela e o rosto saem do
   mesmo arquivo: a etapa 1 recorta a webcam para o painel de baixo e esta seção recorta outra região
   do mesmo quadro para o painel de cima.

Nenhuma das duas serve: o beat volta ao `/flow-reels:planejar` para virar mock autorado, desenhado
com as peças do registro e com o logo de verdade dentro quando a coisa for uma marca. Ele não some,
porque o beat continua precisando mostrar; o que muda é quem desenha.

Decida isto **uma vez por vídeo**, não uma vez por corte, porque todo corte daquele vídeo usa os
mesmos números. **No lote em paralelo, quem decide é você, antes de abrir os subagentes**: você
tira a folha de contato da fonte, faz os quatro testes, escreve a origem e o retângulo da webcam em
`materiais-de-trabalho/logs/`, que é pasta sua, e passa os dois no campo `tela` do pedido de cada
subagente. A caixa de rosto que o teste 2 pede é a mesma para todo corte daquele vídeo, então ela
sai dessa folha. Subagente não mede a webcam de novo e não escreve em `logs/`.

**Como saber se a fonte é compartilhamento de tela.** Três medidas e um olhar, nesta ordem. Todos
têm que dar sim, e um não já encerra: a fonte não é tela.

1. **A proporção da fonte.** Tela de monitor é 16:9 ou 16:10.

   ```
   ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 <fonte>
   ```

   Largura dividida por altura entre 1,55 e 1,82 passa. Vídeo vertical, quadrado ou ultrawide não é
   compartilhamento de tela de aula, e aqui já para.

2. **O tamanho da caixa de rosto.** Pegue a caixa `x:y:largura:altura` que você escreveu na etapa 1 e
   faça `largura x altura ÷ (W x H)` em cima do quadro inteiro. **Abaixo de 25% do quadro, o rosto é
   um encarte num canto, e o resto do quadro é outra coisa.** Busto em tripé não passa nesse teste,
   porque ele enche o quadro e a caixa dele fica acima da metade da área.

3. **Onde a caixa encosta.** O encarte é empurrado para um canto. A caixa de rosto fica a menos de 5%
   da largura de uma borda vertical do quadro, e do outro lado sobra uma faixa livre contínua maior
   que metade da largura. Caixa no meio do quadro, com sobra parecida dos dois lados, é
   enquadramento de câmera, não encarte.

4. **O olhar, que é o que confirma.** Extraia três quadros afastados, a um quarto, à metade e a três
   quartos da duração, com uma régua de 100 px por cima para você ler coordenada:

   ```
   ffmpeg -y -ss <t> -i <fonte> -frames:v 1 \
     -vf "drawgrid=w=100:h=100:t=1:c=yellow@0.5" \
     projetos/<vídeo>/materiais-de-trabalho/corte-NN/tela/olhar-fonte-<t>.png
   ```

   Olhe os três, **fora da caixa de rosto**, e responda sim ou não a três perguntas. Tem interface
   ali: barra de endereço, aba, menu, janela, cursor, texto em linhas? Ela fica no mesmo lugar nos
   três quadros, mudando de conteúdo e não de posição? O conteúdo muda de um quadro para o outro,
   provando que é tela viva e não um fundo parado atrás da pessoa?

**A trava da webcam, quando a tela vem da fonte.** O recorte da tela **nunca** pode pegar a região da
webcam. Se pegar, o mesmo rosto aparece duas vezes no mesmo quadro, um no painel de cima e outro no
de baixo, e não existe conserto barato: quando o defeito aparece, a legenda e o painel já foram
feitos em cima daquele recorte.

O retângulo proibido **não é a caixa de rosto da etapa 1**. Aquela caixa é o recorte na proporção
1080 por 964 tirado de dentro do encarte, e o encarte é maior que ela: sobra cabelo, ombro,
microfone e a moldura em volta. Meça o encarte inteiro:

1. Abra um dos quadros do passo 0 com a régua de 100 px.
2. Leia as quatro bordas do encarte na régua e escreva `x:y:largura:altura` em pixel da fonte.
3. Cresça 8 px para cada lado. A borda do encarte é uma linha escura de cerca de 2 px, e 8 px cobre
   ela, a sombra e o que a compressão espalha em volta.

A trava, em conta: com o recorte em `xr:yr:lr:ar` e o retângulo proibido em `xp:yp:lp:ap`, os dois se
cruzam quando `xr < xp+lp` **e** `xp < xr+lr` **e** `yr < yp+ap` **e** `yp < yr+ar`. As quatro
verdadeiras ao mesmo tempo, o recorte está proibido; **basta uma falsa e ele está livre**. Na
prática: o recorte cabe inteiro à esquerda do encarte, à direita dele, acima ou abaixo.

E confira olhando, que é o que pega erro de conta e encarte que se mexeu: abra o primeiro e o último
quadro da janela **já recortados** e responda uma pergunta, **aparece qualquer pedaço da pessoa aqui
dentro?** Cabelo, ombro, mão, microfone e a moldura do encarte contam como sim. Um sim, o recorte é
refeito, e não se salva com mais zoom.

A área útil encolhe, e a 9.4 continua valendo dentro dela: escolha a região da fala no que sobra fora
do retângulo proibido, e se o elemento falado só existe debaixo da webcam, o beat vira mock autorado
pelo passo 0.

**Um exemplo inteiro, medido numa fonte de verdade.** Fonte de 1920 x 1080 com a webcam no canto
direito, aula de instalação de uma ferramenta. Os números saíram de medição, não de estimativa:

| medida | valor | o que ela diz |
|---|---|---|
| proporção da fonte | 1920 ÷ 1080 = 1,778 | dentro de 1,55 a 1,82, passa |
| encarte da webcam | `1587:290:318:491` | 7,5% da área do quadro |
| caixa de rosto da etapa 1, a maior que cabe no encarte | `1587:290:318:284` | 4,4% da área, bem abaixo dos 25% |
| folga até a borda direita | 15 px | 0,8% da largura, o encarte está encostado |
| faixa livre à esquerda | 1587 px | 83% da largura, sobra mundo para recortar |
| retângulo proibido, com os 8 px | `1579:282:334:507` | é ele que entra na conta do cruzamento |
| recorte aprovado | `crop=500:281:330:270`, escala para 870 | fator 1,74, texto da interface medido em 22 px |
| recorte reprovado | `crop=580:326:1340:270` | cruza o proibido nos quatro lados e entrega o rosto inteiro dentro da janela |

O recorte aprovado termina em x = 830 e o retângulo proibido começa em x = 1579: a condição
`xp < xr+lr` dá falso, e por isso ele está livre. A folha de contato da etapa 1 nessa fonte já avisa
o outro lado da conta: o encarte tem 318 px de largura, o painel de baixo tem 1080, então a face sai
esticada. Isso é limite da gravação, não da tela, e não muda nada aqui.

**Onde os arquivos ficam.** A origem escolhida no passo 0 vive em `materiais-de-trabalho/fonte/`,
porque ela é a mesma para todos os cortes daquele vídeo. Os quadros do passo 0 caem na pasta de
trabalho do corte quando o corte é um só, e em `materiais-de-trabalho/logs/` quando quem mediu foi
você, no lote, antes de existir subagente. Os quadros já recortados vivem dentro da
pasta de trabalho do corte:

```
projetos/<vídeo>/materiais-de-trabalho/
├── fonte/
│   ├── <bruto>.mp4           a fonte; quando ela é compartilhamento de tela, é daqui que a tela sai
│   └── tela.mp4              a gravação separada, só quando quem gravou fez dois arquivos
└── corte-NN/
    └── tela/
        ├── olhar-fonte-*.png os quadros com régua, onde você mediu a webcam e escolheu a região
        ├── olhar-b03.png     o quadro cheio no instante do beat, só para você escolher o recorte
        ├── b03-000.png ...   a sequência do beat 03, já recortada, a 12 quadros por segundo
        └── b07.png           quadro único, quando a região não se mexe durante a janela
```

Daqui para baixo, **`<arquivo-de-tela>` é a origem que o passo 0 escolheu**: `fonte/tela.mp4` ou o
próprio bruto em `fonte/`. Os comandos são os mesmos nos dois casos, só o nome do arquivo muda.

**Por que sequência de PNG e não vídeo dentro da página.** O `painel.py` captura um quadro por vez
chamando `render(t)`, e `render(t)` é pura. Um elemento `<video>` dependeria de busca assíncrona no
meio da captura e sairia parado ou fora de sincronia, do mesmo jeito que transição de CSS sai parada.
Com a sequência, o painel só escolhe qual imagem mostrar no instante `t`, e o resultado é igual em
toda rodada. O servidor do `painel.py` serve a pasta do painel primeiro, então dentro do
`painel.html` o caminho é `tela/b03-000.png`, sem prefixo nenhum.

**Passo 1, olhar e escolher o recorte.** Extraia o quadro cheio no instante do beat e olhe. Se a
tela vem da fonte, tenha o retângulo proibido do passo 0 à mão antes de decidir a região:

```
ffmpeg -y -ss 812.4 -i projetos/<vídeo>/materiais-de-trabalho/fonte/<arquivo-de-tela> -frames:v 1 \
  projetos/<vídeo>/materiais-de-trabalho/corte-NN/tela/olhar-b03.png
```

Para ler a coordenada em pixel, a folha de contato com grade de oitavos serve para qualquer vídeo, e
ela imprime a que pixel cada linha corresponde:

```
flow-reels produzir/enquadrar amostrar \
  --video projetos/<vídeo>/materiais-de-trabalho/fonte/<arquivo-de-tela> \
  --saida projetos/<vídeo>/materiais-de-trabalho/corte-NN/tela/contato-tela.png --n 6 --colunas 3
```

Escreva o recorte em `x:y:largura:altura` seguindo a ordem da seção 9.4 do padrão visual, e confira
duas coisas antes de extrair. O **fator**, que é a largura da janela dividida pela largura do
recorte, nunca abaixo de 1,0, com alvo de 1,3 a 1,8. E, quando a tela vem da fonte, a **trava da
webcam** do passo 0: faça a conta do cruzamento com o retângulo proibido e só extraia depois que ela
der livre.

**Passo 2, extrair a sequência do beat.** Um comando por beat com `tela`. O `fps=12` não é opcional:
é o relógio do painel, e qualquer outro valor deixa a tela e o movimento autorado andando em ritmos
diferentes.

```
ffmpeg -y -ss 812.4 -to 817.0 -i projetos/<vídeo>/materiais-de-trabalho/fonte/<arquivo-de-tela> \
  -vf "crop=580:326:980:220,scale=870:-2:flags=lanczos,fps=12" \
  -start_number 0 projetos/<vídeo>/materiais-de-trabalho/corte-NN/tela/b03-%03d.png
```

O `crop` é a região escolhida no passo 1, o `scale` é a largura da janela dentro do painel, entre 580
e 870 px, e o `-2` mantém a proporção do recorte em número par de pixels. O `lanczos` importa porque
a imagem está sendo ampliada e o padrão do ffmpeg borra texto pequeno. Uma janela de 4,6 s dá 56
arquivos, e a extração leva menos de um segundo.

Região que não se mexe durante a janela, um quadro só resolve e pesa menos:

```
ffmpeg -y -ss 812.4 -i projetos/<vídeo>/materiais-de-trabalho/fonte/<arquivo-de-tela> -frames:v 1 \
  -vf "crop=580:326:980:220,scale=870:-2:flags=lanczos" \
  projetos/<vídeo>/materiais-de-trabalho/corte-NN/tela/b07.png
```

**Passo 3, conferir antes de autorar.** Abra o `b03-000.png` e o último arquivo da sequência, e
responda a lista de 9.6 do padrão visual, inclusive a pergunta da webcam. Os dois quadros, não só o
primeiro: a tela se mexe, e menu que abre ou lista que rola tira o elemento falado do recorte no meio
da janela. Recorte errado descoberto depois do painel pronto custa o painel inteiro.

**Passo 4, o que muda no pedido do subagente.** Acrescente ao pedido de 2.2:

> Os beats <N> e <M> usam tela real. Os quadros já estão em `tela/`, nomeados `b<NN>-000.png` em
> diante, a 12 quadros por segundo, já recortados e já no tamanho final da janela. Mostre a imagem de
> índice `Math.min(Math.floor((t - t0) * 12), ultimo)` dentro do herói, sem escalar de novo, sem
> `<video>` e sem CSS animado. Pré-carregue todas as imagens e só ponha `window.PRONTO = true` quando
> todas tiverem carregado, senão o render captura quadro vazio. Cada janela leva destaque na região
> falada e rótulo autorado de 34 px no mínimo, entra com a chegada de 800 ms, sai com wipe de 167 ms,
> e a moldura do herói continua visível em volta. A lei inteira está em `PADRAO-VISUAL.md` seção 9.

**Como a tela e a anotação se compõem**, em uma frase: a tela é a camada de baixo, dentro do herói, e
destaque e rótulo são autorados por cima dela no mesmo `painel.html`. Não existe passo de ffmpeg
sobrepondo a tela no painel já renderizado, porque a anotação ficaria embaixo da imagem e o grão, que
é aplicado dentro do navegador, não alcançaria a tela.

---

## Etapa 3, a legenda

```
flow-reels produzir/legenda \
  --palavras projetos/<vídeo>/materiais-de-trabalho/transcricao/palavras.json \
  --segmento 12.4:19.8:0 --segmento 51.0:58.2:7.4 \
  --arquivo-fonte marca/fontes/Quicksand-Bold.ttf \
  --saida projetos/<vídeo>/materiais-de-trabalho/corte-NN/legenda.ass
```

Três coisas que você precisa saber para não errar aqui:

- **os segmentos são os mesmos do recorte da face.** Entrada e saída na linha do tempo do bruto,
  deslocamento na linha do tempo do corte montado.
- **`--arquivo-fonte` não é opcional na prática.** Com ele o gerador mede a largura real de cada
  grupo; sem ele, estima. E o arquivo tem que ser uma instância estática: fonte variável entregue ao
  queimador sai magra, porque o eixo de peso é ignorado. Receita da conversão em
  `RECEITA-TECNICA.md` seção 4.3.
- **marca diferente, parâmetros diferentes.** Se o `marca/tokens.json` traz outra fonte ou outro tom
  escuro, passe `--fonte`, `--arquivo-fonte` e `--cor-preenchimento` de acordo. O tamanho 116, o
  contorno 5 e o Alignment 5 não mudam.

Leia a saída do script. Ele imprime quantos grupos saíram e qual é o mais largo, em pixels. Se ele
avisar que um grupo vaza, resolva antes de queimar.

**Antes de queimar, confira nome próprio, produto e número.** O reconhecimento automático erra
justamente neles, e eles costumam estar na frase mais importante do corte, porque é dela que o
gancho saiu. Erro de largura o script acha sozinho; erro de grafia, não: `palavras.json` não sabe
que escreveu o nome errado, e a legenda queimada não se conserta sem re-renderizar.

Visto numa transcrição real deste pacote: a mesma ferramenta apareceu escrita de quatro jeitos
diferentes ao longo do vídeo, e um nome de produto virou duas palavras que existem no dicionário,
que é o caso que passa despercebido, porque não parece erro.

Como conferir, e são dois minutos:

1. abra o `.ass` gerado e leia só os grupos do trecho, não o vídeo inteiro;
2. para cada nome próprio, produto, sigla e número, confira contra o que a pessoa **diz** no áudio,
   não contra o que a transcrição escreveu, porque as duas coisas são a mesma fonte de erro;
3. corrigiu, corrija no `palavras.json` e gere o `.ass` de novo. Não edite o `.ass` na mão: ele é
   saída, e na próxima geração a correção some.

---

## Etapa 4, montar

```
flow-reels produzir/montar \
  --painel  projetos/<vídeo>/materiais-de-trabalho/corte-NN/painel.mp4 \
  --face    projetos/<vídeo>/materiais-de-trabalho/corte-NN/face.mp4 \
  --legenda projetos/<vídeo>/materiais-de-trabalho/corte-NN/legenda.ass \
  --fontes  marca/fontes \
  --saida   projetos/<vídeo>/corte-NN/corte-NN.mp4
```

**Repare no `--saida`: é a única coisa que sai de `materiais-de-trabalho/`.** Entram o painel, a
face e a legenda, que são material de trabalho, e sai o MP4 de entrega, sozinho, na pasta do corte.
O script trabalha a partir da pasta da legenda e resolve o destino em caminho absoluto, então as
duas pastas em lugares diferentes não atrapalham em nada.

O script empilha, queima, exporta e confere com o ffprobe, imprimindo aprovado ou reprovado no
formato de entrega. Ele também cuida sozinho da armadilha do caminho absoluto no filtro do ffmpeg, que
no Windows quebra com `No option name near 'C:/...'`.

Depois que ele aprovar o formato, **extraia quadros e olhe**:

Os quadros de conferência são material de trabalho, então eles caem em
`materiais-de-trabalho/corte-NN/quadros/`, e nunca ao lado do MP4:

```
cd projetos/<vídeo>
ffmpeg -y -ss 5.0 -i corte-NN/corte-NN.mp4 -frames:v 1 \
  materiais-de-trabalho/corte-NN/quadros/q-05.png
ffmpeg -y -ss 5.0 -i corte-NN/corte-NN.mp4 -frames:v 1 -vf "crop=1080:420:0:750" \
  materiais-de-trabalho/corte-NN/quadros/costura-05.png
```

O segundo é o zoom na faixa da costura, que é onde mora quase todo defeito de legenda: duas linhas,
vazamento de margem, contorno fino demais, texto que não lê sobre cena clara.

---

## Etapa 5, a página de revisão

**Entrega de corte não se aprova por lista de arquivo nem por print no chat.** Monte a página servida,
onde a pessoa assiste cada corte inteiro, com som, e aprova ou devolve com comentário:

```
flow-reels produzir/nova-revisao projetos/<vídeo>
```

O script varre o projeto, escreve o `revisao.json` e sobe o servidor na porta de `porta_revisao` do
`setup.json`. O resto está em `revisao/COMO-USAR.md`.

**Esta etapa é uma só, no fim, e é sua.** Nenhum subagente sobe revisão: a página lê a pasta inteira
do vídeo, e uma página por corte daria quatro endereços, quatro servidores brigando pela mesma porta
e uma pessoa sem lugar para aprovar o lote. Se algum corte falhou, suba a página com os que ficaram
prontos e diga, na mesma mensagem, qual faltou e por quê.

Só depois do aceite dela o corte está pronto para ir ao ar. O pacote entrega o arquivo e para aí.

---

## Os sete critérios que bloqueiam a entrega

Os sete valem para o pacote inteiro e a definição completa está em
`${CLAUDE_PLUGIN_ROOT}/skills/fabrica/referencias/GATES.md`. Cinco dos sete são de responsabilidade
desta skill. Os outros dois, o do gancho e o do corte limpo, são do `/flow-reels:planejar` e chegam
aqui já fechados:

| critério | o que esta skill garante |
|---|---|
| legenda em uma linha na costura | grupo medido em pixels, uma linha, Alignment 5, contorno branco sobre preenchimento escuro |
| o painel é um mundo só | um herói, algo acontecendo em cada frase, nada de animação perpétua, abertura com o herói inteiro no primeiro segundo, e o `ritmo_painel.py` passando no `painel.mp4` |
| zona segura respeitada | nada acima de y = 150, nada abaixo de y = 786 no painel |
| formato de entrega | 1080 x 1920, 30 fps, H.264 yuv420p, faststart, SAR 1:1, conferido com ffprobe, e a pasta `corte-NN/` com o MP4 e mais nada |
| nenhuma marca desenhada à mão | todo logo vem de `componentes/logos/`, e nenhum tile sai em estado de falta |

Os pontos de entrada e de saída de cada trecho chegam fechados do `/flow-reels:planejar`,
validados na energia do áudio. Você executa esses pontos; quem responde pelo defeito de fala
amputada continua sendo ele.

---

## Quando parar e perguntar

- o corte não tem `beats.yaml`, ou o beat-sheet não fecha com a duração da face;
- a face se mexe pelo quadro e caixa fixa não resolve;
- o `marca/tokens.json` não existe e o usuário não decidiu a identidade;
- o subagente do painel devolveu duas vezes com o mesmo defeito;
- dois cortes do lote morreram na mesma etapa pelo mesmo motivo, o que aponta ambiente, não corte;
- o `montar.py` reprovou o formato e a causa não está na tabela de sintomas.

Nos outros casos, decida e siga. Em caso de defeito conhecido, a tabela de sintoma, causa e correção
está em `referencias/RECEITA-TECNICA.md` seção 9.

## Tudo que você gerar sai em português

Brief, plano, nome de arquivo, comentário de código, texto na tela do painel, legenda e mensagem para
o usuário. O pacote inteiro é em português do Brasil.
