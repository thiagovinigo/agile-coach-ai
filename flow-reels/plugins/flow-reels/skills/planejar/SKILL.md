---
name: planejar
description: 'Decide o que do vídeo longo vira corte. Levanta primeiro o inventário visual do vídeo, que decide como cada coisa concreta nomeada na fala vai aparecer na tela e baixa em lote os logos que faltam. Depois lê o vídeo inteiro duas vezes, medindo o quanto a fala aponta para fora de si mesma e mapeando os silêncios longos, varre largo sem julgar pelas quatro listas de formas conhecidas, declara o formato de cada candidato entre afirmação e trajeto, passa todos pelos seis eliminadores do gancho, manda cada sobrevivente para um subagente leitor frio que só vê o texto da abertura, ordena os que sobraram por tensão, especificidade, universalidade e payoff visível, apresenta no chat só os escolhidos para você aprovar, e só depois procura no resto do vídeo a prova de cada um e detalha o plano do corte (pontos de entrada e saída validados pela energia do áudio, beat-sheet do painel e brief). Use para "planeja os cortes", "quais ganchos tem nesse vídeo", "monta o plano do corte", "escolhe os trechos", "qual parte vira short". Não renderiza nada, porque quem produz é o `/flow-reels:produzir`.'
---

# Planejar (/flow-reels:planejar)

> **Onde mora cada coisa.** Esta skill está em `${CLAUDE_SKILL_DIR}` e o plugin Flow Reels em
> `${CLAUDE_PLUGIN_ROOT}`. Caminhos como `referencias/...` e `scripts/...` são desta skill;
> `skills/...` e `componentes/...` são do plugin (o que a pessoa baixou fica em `componentes/` da pasta
> de trabalho e vale por cima); `projetos/`, `marca/`, `pautas/`, `setup.json` e `.env` são da pasta de
> trabalho, o diretório onde o Claude Code está aberto. Todo script roda com `flow-reels <skill>/<script>`,
> que está no PATH enquanto o plugin está ligado e já usa o Python e o ffmpeg certos
> (`flow-reels lista` mostra todos; `flow-reels instalar` prepara uma pasta nova).

Esta skill decide **o que** vira corte. É a etapa em que a qualidade do produto inteiro se define.

Ela funciona em torno de duas inversões que valem a pena entender antes de tudo.

**A primeira: você não procura momento bom, você procura forma conhecida.** Momento bom é
impressão, e impressão não se testa. Forma se reconhece e se confere: a frase-tese é uma delas,
sujeito nomeado mais verbo mais afirmação fechada. Depois que a abertura está escolhida, você vai
atrás da prova dela no resto do vídeo. Nunca o contrário.

**A segunda: primeiro se levanta, depois se julga, e nunca ao mesmo tempo.** Quem varre já
perguntando "este trecho passa?" acha os candidatos óbvios e para. A fase de levantamento é
generosa de propósito e a fase de julgamento é impiedosa de propósito. Misturar as duas é o que faz
vídeo bom render pouco.

---

## A ordem de trabalho

**São sete passos, numerados de 0 a 6, e eles estão escritos aqui e em nenhum outro lugar.** As
referências desta skill mandam cada uma no seu bloco de passos, como a tabela abaixo reparte, e
apontam para cá em vez de renumerar.

0. **Levante o inventário visual do vídeo.** Toda coisa concreta nomeada na fala ganha uma rota, e
   os logos que faltam são baixados agora.
1. **Leia o vídeo inteiro duas vezes**, antes de procurar trecho nenhum: quanto a fala se apoia em
   palavras que apontam para fora dela, e onde estão os silêncios longos.
2. **Levante candidatos sem julgar**, pelas quatro listas de varredura, cobrindo os três terços, no
   mínimo seis.
3. **Julgue.** Declare o formato de cada candidato, rode os seis eliminadores, mande os
   sobreviventes para a leitura fria e ordene por tensão, especificidade, universalidade e payoff
   visível.
4. **Só então procure, no resto do vídeo, o trecho que prova aquele candidato específico.**
5. **Veja se falta contexto para o espectador frio.** Se faltar, ache o beat de contexto.
6. **Corte tudo que não serve à promessa, inclusive coisa boa.**

Os passos 1 e 2 são a fase generosa e o passo 3 é a fase dura. **A fronteira entre eles é a coisa
mais importante desta ordem:** nenhum candidato é descartado antes do passo 3, e nenhum candidato
novo nasce depois dele.

As tabelas de eliminadores e de regras que aparecem nas etapas abaixo são **resumo**. A definição, os
exemplos e o motivo de cada uma vivem nas referências, e **em caso de divergência a referência
vence**, e você corrige o resumo.

| passo | lei que manda nele |
|---|---|
| 0 | `referencias/REPRESENTACAO.md` |
| 1 e 2 | `referencias/LEVANTAMENTO.md` |
| 3, a declaração do formato | `referencias/FORMATOS.md` |
| 3, os eliminadores e a escolha | `referencias/GANCHO.md` |
| 4, 5 e 6 | `referencias/VALOR.md` |
| as bordas de cada trecho, em qualquer passo | `referencias/CORTE-LIMPO.md` |
| o painel, depois que o corte está montado | `referencias/BEAT-SHEET.md` |
| o reel inteiro em cenas, com `"motor": "2.0"` no setup.json | `referencias/CENAS.md`, os modelos por ângulo em `referencias/MODELOS-DE-CENAS.md`, o plano completo de exemplo em `referencias/EXEMPLO-CENAS.json` e `${CLAUDE_PLUGIN_ROOT}/skills/produzir/motor/MOTOR.md` |

As etapas da skill, mais abaixo, são cinco e executam esses sete passos com uma parada no meio, que
é a aprovação. A etapa 0 faz o passo 0. A etapa 1 faz os passos 1 e 2. A etapa 2 faz o passo 3. A
etapa 3 é a parada. A etapa 4 faz os passos 4, 5 e 6 e escreve o plano.

---

## A regra da vitrine

**O arquivo registra tudo. A conversa mostra só o que passou.**

Duas coisas diferentes, e misturar as duas é o defeito que esta regra existe para matar.

**O `GANCHOS.md` é estoque.** Ele guarda o levantamento inteiro e o pool inteiro: todos os
candidatos levantados, as duas leituras do vídeo, as que
caíram, o eliminador que derrubou cada uma e o motivo escrito. Ele existe para duas coisas
concretas: não repetir gancho no lote seguinte, que é o que o eliminador E5 confere, e deixar alguém
entender, semanas depois, por que aquele trecho não virou corte. Estoque é completo.

**A conversa é vitrine.** Na vitrine vão **só os candidatos escolhidos**. Especificamente:

- **Não diga quantos foram avaliados nem quantos caíram.** Nada de "levantei nove e quatro não
  passaram".
- **Não nomeie o eliminador que derrubou ninguém** no chat. Isso é linha de arquivo.
- **Não peça opinião sobre descarte.** "O quinto eu quase usei, o que você acha?" é devolver para a
  pessoa uma decisão que é sua.
- **Não peça desculpa pelo número.** Se sobraram três, apresente três, do mesmo jeito que
  apresentaria cinco. A aritmética do funil não interessa a quem vai aprovar.
- **Se ela perguntar**, aí sim responda, e aponte o `GANCHOS.md` pelo caminho completo. Perguntou,
  tem direito à resposta inteira.

**O que a vitrine proíbe é a aritmética do funil, não a leitura do material.** Duas coisas são ditas
no chat e não violam nada:

1. **O rendimento do vídeo, antes de qualquer candidato aparecer.** A primeira leitura do
   `referencias/LEVANTAMENTO.md` mede quanto a fala se apoia em palavra que aponta para fora dela, e
   esse número é dito em uma linha antes de você prometer volume. Ele é afirmação sobre o material, e
   é dito antes de o funil existir.
2. **O diagnóstico, quando nenhum candidato sobrevive.** Aí não há vitrine, e o diagnóstico vira a
   entrega (`referencias/VALOR.md`, seção 7).

---

## O que entra

| arquivo | quem escreve | o que é |
|---|---|---|
| `projetos/<video>/transcricao.md` | skill `/flow-reels:transcrever` | a fala **já quebrada em frases**, uma por linha, com marca de tempo. É o arquivo que você lê e varre, e é dele que saem os greps do `LEVANTAMENTO.md` e da regra R4 |
| `projetos/<video>/materiais-de-trabalho/transcricao/palavras.json` | skill `/flow-reels:transcrever` | a fala palavra a palavra, com tempo |
| `projetos/<video>/materiais-de-trabalho/transcricao/audio16k.wav` | skill `/flow-reels:transcrever` | o áudio em 16 kHz mono, que valida os pontos de corte |
| `projetos/<video>/materiais-de-trabalho/fonte/<video>` | skill `/flow-reels:transcrever` | a fonte, de onde saem os quadros que o inventário olha |
| `componentes/logos/` e `componentes/REGISTRO.md` | o pacote | o acervo de logos e as peças com que o inventário resolve cada rota |
| `setup.json` (na raiz do pacote) | o pacote | `max_cortes` e `aprovar_ganchos` |

O formato do `palavras.json` é fixo e vale como contrato entre as skills:

```json
{ "palavras": [ { "inicio": 0.59, "fim": 0.71, "texto": "Bom" } ] }
```

Se o arquivo não estiver nesse caminho, procure um `palavras.json` dentro da pasta do projeto antes
de reclamar. Se não existir nenhum, **pare e peça a transcrição**. Planejar sem transcrição é chutar.

Se o `audio16k.wav` não existir, você ainda consegue levantar candidatos e escolher gancho, mas
**não** consegue fechar ponto de corte. Avise isso em vez de entregar tempos inventados.

## O que sai

| arquivo | quando | o que é |
|---|---|---|
| `projetos/<video>/materiais-de-trabalho/INVENTARIO.md` | etapa 0, um por vídeo | toda coisa concreta nomeada na fala, com a rota decidida e o recurso concreto de cada uma |
| `projetos/<video>/materiais-de-trabalho/inventario/` | etapa 0, um por vídeo | os quadros da fonte que você olhou antes de decidir rota |
| `projetos/<video>/GANCHOS.md` | etapas 1 e 2, um por vídeo | as duas leituras do vídeo, o levantamento inteiro e o pool julgado: formato, eliminadores, leitura fria, contexto que falta, veredicto e os descartados com o motivo |
| `projetos/<video>/materiais-de-trabalho/corte-NN/brief.md` | etapa 4, um por corte aprovado | o plano do corte, no modelo de `scripts/modelo_brief.md` |
| `projetos/<video>/materiais-de-trabalho/corte-NN/beats.yaml` | etapa 4, um por corte aprovado | o plano do painel, no formato de `referencias/BEAT-SHEET.md` |

O `GANCHOS.md` é do vídeo, não do corte, e ele é a única casa que um candidato descartado tem.

## Antes de começar

1. Leia `setup.json`. Dois campos mandam em você:
   - `max_cortes`: quantos candidatos você propõe. O padrão é 5. É **teto, nunca meta**. Propor menos
     porque o material só deu menos é o comportamento certo (`referencias/VALOR.md`, seção 6).
   - `aprovar_ganchos`: se for `true`, você **não produz nada** antes do aceite. Se for `false`, você
     ainda escreve o `GANCHOS.md` inteiro, só não para para perguntar.
2. Confirme que a marca já existe (`marca/tokens.json`). Se não existir, avise o orquestrador. O
   plano do painel cita peças que leem os tokens, e sem tokens o criador não renderiza.
3. Leia as sete referências desta skill antes de escrever qualquer coisa, na ordem em que o
   trabalho acontece:
   - `referencias/REPRESENTACAO.md`, o passo 0: as quatro rotas, a ordem de decisão, o inventário
   - `referencias/LEVANTAMENTO.md`, os passos 1 e 2: as duas leituras do vídeo, as duas fases, as
     quatro listas de varredura, os dois eixos, os finais
   - `referencias/FORMATOS.md`, a primeira decisão do passo 3: afirmação e trajeto, e a tabela do
     que muda de um para o outro
   - `referencias/GANCHO.md`, o resto do passo 3: forma de tese, os seis eliminadores, leitura fria,
     ordenação
   - `referencias/VALOR.md`, os passos 4 a 6: aprendizado, os cinco tipos, as seis regras do
     desenvolvimento
   - `referencias/CORTE-LIMPO.md`, como escolher entrada e saída de cada trecho
   - `referencias/BEAT-SHEET.md`, o formato do plano do painel

---

## Quando o vídeo é a leitura de uma pauta

Se a pasta do vídeo tem `ROTEIRO.md` na raiz, o vídeo foi gravado a partir de uma pauta da skill
`/flow-reels:tendencias`, e o gancho já foi aprovado junto com ela. Então:

- **a etapa 0 roda normalmente**, lendo também `materiais-de-trabalho/pauta/PAUTA.md` e os arquivos
  de `materiais-de-trabalho/assets/`, que já são a prova visual pronta;
- **as etapas 1 a 3 não rodam.** O `GANCHOS.md` registra um candidato só, a gravação inteira, com
  formato declarado pelo ângulo do roteiro, e a nota "gancho aprovado na pauta". A leitura fria
  ainda vale: mande o gancho gravado para o subagente, porque o que foi falado pode ter saído
  diferente do que foi escrito;
- **a etapa 4 roda inteira**, com três atalhos: os pontos de corte são o primeiro e o último som da
  leitura válida, tirando as tentativas repetidas; a grafia da seção "Grafia para a legenda" do
  roteiro entra no brief; e o `cenas.json` parte do `materiais-de-trabalho/pauta/cenas-rascunho.md`
  (no motor 1.0, o `beats.yaml` parte do `painel-rascunho.md`), agora com os tempos reais da fala.

## Etapa 0: o inventário visual

Isto é o passo 0 da ordem de trabalho, e ele **roda sempre**, uma vez por vídeo, logo depois de
transcrever e antes de qualquer gancho. A lei inteira está em `referencias/REPRESENTACAO.md`. O
resumo operacional:

**0.1 Varra a transcrição atrás de coisa concreta.** Esta varredura procura outra coisa que a da
etapa 1: aqui você caça **produto, ferramenta, plataforma, interface, arquivo, número e resultado
nomeados na fala**, não candidato a corte. Ideia abstrata não entra na lista. A lista de nomes
próprios que sair daqui é a mesma que o marcador de trecho forte da etapa 1 vai usar, então ela é
levantada uma vez e consultada duas.

**0.2 Decida a rota de cada uma.** A ordem de decisão da seção 2 da lei, parando no primeiro sim:
logo, mock, tela, palavra. Coisa concreta sem rota decidida é a coisa que vira card com o nome
escrito dentro, que é o defeito que esta etapa existe para matar.

A rota `tela` é a única que **não** se fecha aqui. Você responde as duas perguntas que se respondem
olhando o arquivo, marca a linha como `tela candidata` e anota o instante e a região. A terceira
pergunta é o orçamento, que é por corte, e neste momento nenhum corte existe ainda: ela é do
beat-sheet, na etapa 4. Fechar `tela` aqui é prometer uma janela que pode não caber.

**0.3 Olhe o quadro antes de decidir por mock ou tela.** Regra transversal 1, e é a que mais muda o
resultado:

```
mkdir -p projetos/<video>/materiais-de-trabalho/inventario
ffmpeg -y -ss <t da fala> -i projetos/<video>/materiais-de-trabalho/fonte/<arquivo da fonte> \
  -frames:v 1 projetos/<video>/materiais-de-trabalho/inventario/<coisa>-<t>.png
```

A pasta `inventario/` é criada por você, na primeira vez. O ffmpeg não cria pasta: sem o `mkdir`
ele grava nada e termina com `Conversion failed!`.

Abra a imagem e olhe mesmo. O que você viu e não teria adivinhado vai para a coluna de observação.
Sem a fonte na pasta, tela não existe e mock sai de memória: escreva isso na evidência do inventário em
vez de deixar parecer que alguém olhou.

**0.4 Registre se a fonte é compartilhamento de tela.** Duas leituras: o que a fala diz, que é
sinal barato, e a medida, que é da produção e vive na seção 2.5 da `SKILL.md` do `/flow-reels:produzir`.
Não reescreva o teste e não invente número. Você registra a resposta e a evidência, e ela vale para
todos os cortes daquele vídeo.

**0.5 Baixe os logos que faltam, em lote.** Junte todas as marcas nomeadas e peça de uma vez:

```
flow-reels componentes/baixar-logo <marca> <marca> <marca>
```

O que não chegou vira decisão agora, aqui: alguém salva o logo oficial na pasta, ou a marca cai em
palavra. Marca em aberto é buraco hachurado no render, depois do painel pronto.

**0.6 Escreva o `INVENTARIO.md`** em
`projetos/<video>/materiais-de-trabalho/INVENTARIO.md`, no formato da seção 5 da lei, incluindo a
lista do que ficou sem rota visual e por quê.

O inventário **não vai para a conversa**. Ele é arquivo de trabalho, e a regra da vitrine vale aqui
igual: o que você diz é uma linha, do tipo "inventário do vídeo pronto, dois logos baixados, um
assunto sem logo disponível". A tabela inteira só aparece se perguntarem.

## Etapa 1: as duas leituras e o levantamento

Isto é os passos 1 e 2 da ordem de trabalho. A lei inteira está em `referencias/LEVANTAMENTO.md`. O
resumo operacional:

**1.1 Leia a transcrição inteira.** Inteira mesmo. Não é leitura por amostragem, não é ler os
primeiros minutos e adivinhar o resto. O material de quase todo corte bom aparece fora do lugar onde
a pessoa achava que ia aparecer, muitas vezes no último terço, quando quem gravou já relaxou e
finalmente disse a frase direta. Se a transcrição for longa, leia em blocos de cerca de 10 minutos,
mas cubra 100%.

**1.2 Rode as duas leituras do vídeo** (passo 1):

```
flow-reels planejar/leitura_do_video projetos/<video>
```

- **Para onde a fala aponta.** Quanto ela se apoia em aqui, isso, esse, ele, lá. Esse número **é
  dito no chat, em uma linha, antes de você prometer qualquer volume**. Ele não é limiar e não
  reprova nada: ele diz quanto o vídeo rende em afirmação isolada, e vídeo que aponta muito puxa
  para o formato trajeto.
- **O mapa dos silêncios.** As pausas mais longas do vídeo, que são os melhores pontos de entrada e
  de saída, porque quem fala pausa onde termina uma ideia. Ele dá a região; quem fecha o ponto é a
  energia do áudio, na etapa 4.

**1.3 Varra largo, sem julgar** (passo 2). Quatro listas, rodadas sobre a transcrição inteira:
formas de abertura, marcadores de trecho forte, tipos de momento e tipos de informação. As listas,
com o que procurar e como achar cada coisa, estão na seção 2 da lei.

Cada candidato levantado sai com duas marcas, uma de cada eixo: o que **acontece** no trecho e o que
ele **contém**. Trecho que pontua nos dois é o alvo.

Levante cada candidato **já com as duas bordas**, entrada e saída, porque a qualidade do fim é
critério de seleção e não consequência do corte (seção 3 da lei).

Mínimo de seis candidatos, cobrindo os três terços. Menos que isso não é escolha, é a primeira ideia
disfarçada. Se um terço não deu nenhum, escreva por quê no `GANCHOS.md`.

**Nada é descartado nesta etapa.** Nenhum eliminador roda aqui, e nenhum candidato nasce com
veredicto. Se você se pegar pensando "esse não presta", você entrou na etapa 2 cedo demais, e o
resultado é o pool pequeno que sempre foi confundido com vídeo pobre.

Produza também, para o `GANCHOS.md`, a **tese do vídeo** em uma frase, com as suas palavras.

## Etapa 2: o formato, os eliminadores e a escolha

Isto é o passo 3. As leis são `referencias/FORMATOS.md` e `referencias/GANCHO.md`, seções 3 a 5. O
resumo operacional:

**2.0 Declare o formato de cada candidato**, `afirmacao` ou `trajeto`, **antes de rodar qualquer
eliminador**. As regras mudam conforme o formato, e julgar sem declarar é julgar por regras que
ninguém escolheu.

| formato | o que ele é | o que é obrigatório |
|---|---|---|
| `afirmacao` | abre afirmando, prova, e fecha na mesma âncora | uma afirmação só, e a introdução do vídeo **nunca** serve de abertura |
| `trajeto` | promete um resultado, mostra o caminho, mostra o resultado, aponta o destino | os quatro blocos, e no máximo um trajeto por vídeo. Aqui a introdução do vídeo **geralmente serve**, se nomear o resultado e o meio |

**2.1 Rode os seis eliminadores.** Qualquer um derruba o candidato, sozinho e sem recuperação:

| eliminador | derruba quando |
|---|---|
| **E1, olhos fechados** | não é frase completa para quem não vê a tela: fragmento, pronome sem antecedente |
| **E2, assunto nomeado** | o assunto concreto não é dito na fala dos primeiros segundos. O que está escrito na tela não conta |
| **E3, span contínuo** | a abertura só existe costurando trechos não adjacentes |
| **E4, promessa paga** | não abre lacuna, ou promete algo que o vídeo não entrega |
| **E5, tese nova** | repete a tese, a prova ou a abertura de um candidato que você já escolheu, neste lote ou em rodada anterior |
| **E6, trabalho nomeado** | a afirmação é condicional e a condição ficou no vídeo. Passa no E2 e morre aqui: nomeou o assunto, não nomeou o trabalho |

Rode **E1, E3, E5, E4 e E6** você mesmo, que são leitura. O **E2 não é você quem julga**, porque quem
escolheu o candidato já sabe do que ele trata e não consegue desconhecer isso.

**2.2 Mande os sobreviventes para a leitura fria.** Um subagente dedicado por candidato, todos
disparados de uma vez. Ele recebe **só o texto do span e a duração falada**, e nada mais: nem título,
nem tese do vídeo, nem outro pedaço da transcrição, nem o número do candidato, nem o motivo da
escolha. Uma linha dessas vazando contamina a resposta e a leitura fria precisa ser refeita.

As três perguntas, o texto exato do pedido e o que fazer com cada resposta estão em
`referencias/GANCHO.md`, seção 4. Resposta 1 vaga ou genérica significa **caiu no E2**, e caiu é
caiu: não reescreva o gancho para salvar.

**2.3 Escreva o aprendizado de cada sobrevivente**, em uma frase, no formato da seção 1 do
`referencias/VALOR.md`. Se você não consegue escrever essa frase, não existe corte ali.

**2.4 Ordene.** Tensão, depois especificidade, depois universalidade, depois payoff visível em tela
(`referencias/GANCHO.md`, seção 5). Os primeiros até o teto de `max_cortes` viram a proposta; os
demais ficam como `reserva`.

**2.5 Sugira o caminho de cada escolhido**: `cenas` (o reel em cenas, com os modos de sempre) ou
`mundo` (o modo mundo do motor, `${CLAUDE_PLUGIN_ROOT}/skills/produzir/motor/MOTOR.md` seção 4.14). O
teste: a fala aponta o tempo todo para uma coisa concreta que dá para mostrar grande (um arquivo, uma
janela, uma planilha, um gráfico)? `mundo`. É opinião, história, provocação, lista? `cenas`. Na dúvida,
`cenas`: mundo sem objeto real vira slideshow. Um reel em `cenas` também pode ter um trecho de mundo,
quando um pedaço da fala aponta para um objeto. A sugestão é sua; quem confirma é a pessoa, na aprovação.

**2.6 Escreva o `GANCHOS.md` inteiro**, no formato da seção 8 do `referencias/GANCHO.md`, com todos
os candidatos, inclusive os derrubados e o motivo de cada um. Isso é estoque, e estoque é completo.

## Etapa 3: aprovação

Com `aprovar_ganchos: true`, esta é a parada obrigatória, e é aqui que a **regra da vitrine** manda.

**Antes da lista, uma linha sobre o material**, que é a primeira leitura da etapa 1: quanto a fala
aponta para fora de si mesma e o que isso faz com o rendimento do vídeo. Isso vem antes de qualquer
candidato, e serve para ninguém esperar um volume que o vídeo não comporta. Não é aritmética de
funil: é o material, dito antes de o funil existir.

Apresente **só os escolhidos**, numerados, curtos, com o formato e o caminho de cada um entre parênteses. A
primeira linha depois do gancho é o que a pessoa aprende, porque é por isso que ela vai decidir, e
decidir só pela abertura é exatamente o viés que produziu os cortes ruins:

```
Este vídeo é narração de tela: a fala se apoia muito em "aqui" e "isso", então ele rende poucos
trechos que se sustentam soltos, e o material puxa para um corte de passo a passo.

1. "Primeiras palavras do gancho..."   (412.8 a 421.6 s, afirmação, cenas)
   O que quem assiste aprende: depois do corte, a pessoa sabe que ...
   Duração estimada: 34 s

2. "Primeiras palavras da promessa..."   (12.4 a 21.0 s, trajeto, mundo)
   O que quem assiste aprende: ...
   Duração estimada: 42 s
```

Depois da lista, uma linha só: "o caminho de cada um está entre parênteses; dá para trocar qualquer um".
E mais nada. Sem contagem de avaliados, sem eliminador citado, sem candidato descartado, sem
"o quarto ficou de fora porque". Se sobraram três, apresente três sem comentar o número.

A linha do aprendizado é escrita do ponto de vista de quem assistiu e sem jargão, do jeito que ela
está no `GANCHOS.md`.

E então **pare**. Pergunte quais viram corte. Não produza brief, não calcule ponto de corte, não
planeje painel antes da resposta. Se a pessoa aprovar menos do que você propôs, ótimo: menos corte
bom vale mais que a cota cheia.

Se ela reprovar tudo, não insista com os mesmos candidatos maquiados. Volte ao mapa da etapa 1 e
pergunte **o que ela acha que o vídeo ensina** que valeria quarenta segundos. O pool novo tem que ser
diferente do antigo, não uma reescrita dele.

## Etapa 4: montar e detalhar cada corte aprovado

Aqui entram os passos 3, 4 e 5 da ordem de trabalho, nesta ordem, para cada gancho aprovado. A lei
inteira está em `referencias/VALOR.md`, seção 3.

**4.1 Declare a âncora.** Uma ou duas palavras: o objeto concreto que o gancho nomeou. Tudo que vem
depois se mede contra ela.

**4.2 Ache a prova (passo 4).** Procure no resto do vídeo o trecho que prova **aquele** candidato.
Vale qualquer parte do vídeo, em qualquer ordem: minuto 4, depois minuto 1, depois minuto 2. No
trajeto, o mesmo vale para as etapas do caminho e para o destino. As seis regras mandam na escolha:

| regra | o que ela exige |
|---|---|
| **R1, paga o gancho** | o corpo usa as mesmas âncoras do gancho. Corpo que deriva mata o corte |
| **R2, uma ideia só** | trecho bom que não serve à promessa fica fora |
| **R3, prova em tela** | prova visível ganha de explicação falada |
| **R4, se sustenta sozinho** | trecho que depende do que ficou de fora, ou traz aquilo junto, ou cai |
| **R5, só o necessário** | o corpo é o menor span que prova a afirmação |
| **R6, volta à âncora** | a última frase fecha na âncora do gancho. No trajeto, quem volta à âncora é o bloco do resultado, e o último segmento é o `destino` |

**4.3 Veja se falta contexto (passo 5).** Só no formato afirmação. Se o `GANCHOS.md` registrou
contexto de identidade faltando, o corte precisa de um segmento de papel `contexto`. Procure a frase mais curta do vídeo que nomeia o assunto
e o resultado, quase sempre antes do gancho no vídeo, e coloque ela como **segmento 2, logo depois do
gancho**. Se essa frase não existe no material, o candidato volta ao pool como descartado, com o
motivo "sem trecho de contexto disponível". Não invente a frase.

Se o que falta não é "o que é isso" e sim "em que situação isso vale", aquele candidato já tinha
caído no E6 e não deveria estar aqui. Contexto de identidade se paga; condição não se paga.

**4.4 Corte tudo que não serve (passo 6).** Demonstração lenta, repetição, "olha só", recapitulação,
e o trecho excelente que é de outra ideia. Este passo dói e é o que salva o corte.

**4.5 Monte os segmentos com os seus papéis.** A ordem depende do formato declarado, e é uma só
dentro de cada um.

No formato **afirmação**:

> **gancho, contexto, prova, fechamento.**

| papel | o que ele faz |
|---|---|
| `gancho` | abre o corte. É sempre o segmento 1, sempre o primeiro som, e é um span contínuo |
| `contexto` | o mínimo que o espectador precisa saber. Primeiro segmento do corpo, nunca antes do gancho, só existe quando falta contexto de identidade |
| `desenvolvimento` | a prova: mecanismo, número, caso, o momento acontecendo na tela |
| `payoff` | fecha a lacuna que o gancho abriu, e a última frase volta à âncora |

`contexto` e `desenvolvimento` podem aparecer mais de uma vez. `gancho` e `payoff` aparecem uma vez
cada. Corte sem `payoff` não é corte, é trecho.

No formato **trajeto** (`referencias/FORMATOS.md`, seção 3):

> **promessa, caminho, resultado, destino.**

| papel | o que ele faz |
|---|---|
| `gancho` | a promessa: nomeia o resultado e o meio. Continua sendo o segmento 1 e um span contínuo |
| `desenvolvimento` | uma etapa do caminho por segmento, na ordem que torna o resultado acreditável |
| `payoff` | o resultado acontecendo, mostrado e não afirmado |
| `destino` | para onde ir depois. É o último segmento, e é onde a identidade entra, se entrar |

Aqui **não existe papel `contexto`**, porque quem paga o contexto é a própria promessa. O `destino`
é obrigatório e costuma já existir gravado, no encerramento do vídeo. Os quatro blocos vêm de
pontos diferentes do vídeo, e isso é montagem de corpo, não costura de abertura.

**4.6 Valide cada ponto com o áudio.** Regra completa em `referencias/CORTE-LIMPO.md`. Rode:

```
flow-reels planejar/energia_audio projetos/<video>/materiais-de-trabalho/transcricao/audio16k.wav 412.8 431.2 730.4
```

O script imprime o envelope em volta de cada ponto e diz onde há silêncio de verdade. Ajuste o tempo
para o silêncio que ele apontou. **Tempo de palavra sozinho não fecha corte.**

**4.7 Confira as referências soltas.** Duas conferências, e a primeira é de graça: rode a busca por
retrorreferência explícita da regra R4 (`referencias/VALOR.md`, seção 3), que acha "como eu falei
antes" e parentes sem ler frase nenhuma. Depois leia a fala montada do começo ao fim como se fosse a
primeira vez, e a cada "isso", "ele" ou "essa parte" pergunte: o antecedente está dentro do corte?
Se não estiver, ou o segmento cresce para incluir o antecedente, ou o segmento cai (regra R4).

**4.8 Planeje o painel ou as cenas.** Com `"motor": "2.0"` no `setup.json`, o plano é o reel inteiro:

1. rode o editor de fala com os trechos que você validou na 4.6 e a grafia do corte
   (`materiais-de-trabalho/corte-NN/grafia.json`, no formato `[{"de": "Cloud Code", "para": "Claude Code"}]`):

   ```
   flow-reels produzir/editar_fala --projeto projetos/<v> --corte NN --trechos "a-b,c-d"
   ```

   Ele tira silêncio longo, hesitação e frase repetida, e grava o `fala.mp4`, o `palavras-corte.json`
   e o `edicao.json`. **A velocidade da fala é decisão do criador, sempre.** Antes de rodar, pergunte
   a velocidade (1,0x, 1,15x, 1,25x, 1,5x...) e diga o que você mediu: as palavras por segundo da
   gravação e a duração que o corte teria em cada opção. Nunca escolha sozinho, nem com
   `--velocidade auto`, e não reaproveite a resposta de um vídeo anterior: cada vídeo tem a sua.
   O ritmo de referência (~3,7 palavras/s nos roteirizados) é informação para a pergunta, não regra.
   **Na mesma mensagem, pergunte se o corte leva trilha sonora (sim ou não)** e, se sim, qual faixa de
   `componentes/trilhas/`; a chave `trilha` só entra no `cenas.json` com o sim dele. **E o estilo de
   produção** (um ou mais, de `${CLAUDE_PLUGIN_ROOT}/skills/produzir/motor/estilos.json`): ele vai no `cenas.json` como
   `"estilo": [...]`, e o plano só usa os modos, sobreposições e transições que o estilo permite
   (`referencias/CENAS.md`, seção "Estilos de produção"). **E a linguagem do episódio** (4.0): mostre as
   3 sugestões do `flow-reels produzir/linguagem sugerir`; a escolhida vai no `cenas.json` como
   `"linguagem": "<nome>"` (ou `{"base", "convidada"}`), com `"heroi": {"t", "nome"}` entre 55% e 80% da
   duração. Antes do render, `linguagem.py conferir`; depois da aprovação, `linguagem.py registrar`.
   Com mãos no vídeo, rode `flow-reels produzir/gestos` depois do `visao.py` e use o
   `--resumo` para escolher os gatilhos dos efeitos de mão (`${CLAUDE_PLUGIN_ROOT}/skills/produzir/motor/docs-4/`); idem o
   `expressao.py --resumo` para os efeitos de rosto. O pós no quadro inteiro (`"pos"`) só usa os efeitos
   que a linguagem aceita (`pecas.pos` do `linguagens.json`; grão e vinheta valem em todas), e o
   `"acabamento"` do topo parte do sugerido pela linguagem (LUT, grão 0,15 a 0,3, vinheta). Com pos, nada de
   padrão fino (crt, pontilhado, retícula, ascii, pixel) sobre texto pequeno;
2. escreva o `cenas.json` nos tempos do `palavras-corte.json`, pela `referencias/CENAS.md` (qual modo
   para qual fala, ritmo, transições, abertura) e pelo formato do `MOTOR.md` do criador. Comece pelo
   modelo do ângulo em `referencias/MODELOS-DE-CENAS.md`; se o corte veio de uma pauta, parta do
   `cenas-rascunho.md` da pasta dela, que já liga cada bloco do roteiro a um modo e a um asset.

O `beats.yaml` abaixo continua valendo para o motor 1.0 e para uma cena `painel-rosto` do 2.0, que usa
o painel de hoje. Escreva `beats.yaml` no formato de `referencias/BEAT-SHEET.md`. Um mundo,
um objeto herói, um beat por palavra-chave, cada beat com o verbo do que **muda**. Cada beat mostra a
ideia como objeto e não repete a palavra numa pílula (regra C), e os cinco primeiros segundos são o
trailer do corte, com o herói inteiro em `t: 0.0` e três mudanças de verdade antes de `t: 5.0`
(regra D).

O painel **escolhe do inventário**: toda coisa concreta que a fala deste corte nomeia já tem rota
decidida no `INVENTARIO.md`, e o campo `peca` resolve contra ela. Beat que precisa de uma coisa que
não está lá é sinal de que a varredura da etapa 0 passou batido: volte, decida a rota e só depois
escreva o beat. Decidir rota na hora de escrever o beat é como o card com texto volta.

**4.9 Escreva o brief.** Use `scripts/modelo_brief.md`. É o arquivo que o `/flow-reels:produzir` lê, e o
que você não escrever ali vira improviso na hora de renderizar.

## A duração do corte

A duração sai da ideia, não da meta. A faixa normal é de 25 a 45 segundos.

- Ideia de uma afirmação só, com um exemplo: 25 a 32 segundos.
- Ideia com contraste (antes e depois, errado e certo): 32 a 42 segundos.
- Acima de 45 segundos só se a prova for uma demonstração que precisa ser vista inteira.

Nunca estique fala para chegar em um número. Corte que se arrasta perde no meio, e perder no meio é
pior do que ser curto, porque a plataforma lê o abandono.

## Quando parar e perguntar

- Não existe transcrição ou não existe áudio de 16 kHz.
- **Nenhum candidato sobrevive.** É a situação mais importante desta lista, porque é a que dá vontade
  de inventar corte para não voltar de mãos vazias. O procedimento inteiro está na seção 7 do
  `referencias/VALOR.md`. Só aqui a vitrine dá lugar ao diagnóstico, e o diagnóstico se diz em uma
  frase no chat.
- O vídeo não tem nenhuma afirmação forte, só narração de tela, **e também não fecha os quatro
  blocos de um trajeto**. Narração de tela sem afirmação é exatamente o material que a primeira
  leitura prevê, e a resposta certa é tentar o trajeto antes de declarar qualquer coisa
  (`referencias/VALOR.md`, seção 7, item 4). Se nem o trajeto fecha, o material não rende corte, e
  isso se diz na cara.
- A pessoa pede um corte específico que cai em um eliminador. Mostre o que falhou e proponha o
  ajuste, em vez de produzir sabendo que vai morrer. Aqui você nomeia o eliminador, porque ela
  perguntou por aquele candidato.
- O melhor gancho está em um trecho onde a fala está cortada ou o áudio está estourado.

## Erros que esta skill já cometeu

| erro | como evitar |
|---|---|
| procurar "o melhor momento" em vez de forma conhecida | momento bom é impressão. Varra pelas quatro listas do `LEVANTAMENTO.md`, que são formas que se reconhecem |
| julgar enquanto varre | são duas fases. Quem varre julgando acha os candidatos óbvios e para, e o pool pequeno vira "vídeo pobre" no relatório |
| prometer volume antes de medir | a primeira leitura do vídeo é dita antes de qualquer candidato. Vídeo de narração de tela rende pouca afirmação isolada, e isso se diz na cara |
| ignorar os silêncios longos | eles são os melhores pontos de entrada e saída, não só o lugar onde não se corta |
| levantar candidato sem saber onde ele termina | a qualidade do fim é critério de seleção. Corte no meio do pensamento é o fim ruim |
| selecionar antes de declarar o formato | é a declaração que diz quais regras valem. Sem ela, o trajeto nunca acontece e a afirmação vira passo a passo |
| descartar a introdução do vídeo por reflexo | ela nunca serve na afirmação e geralmente serve no trajeto, se nomear resultado e meio |
| pagar a condição com um segmento de contexto | contexto de identidade se paga; condição é o E6 e derruba. "Para quê e quando" não se explica depois da afirmação |
| ficar com a primeira ocorrência de uma ideia repetida | compare as ocorrências e fique com a mais bem formada, não com a primeira nem com a mais enfática |
| propor dois cortes que usam a mesma prova | é um corte com duas aberturas. Escolha a melhor e descarte a outra (E5) |
| costurar dois trechos distantes para montar um gancho melhor | caiu no E3. O gancho é span contínuo; só o corpo se monta de vários trechos |
| escolher o corpo antes da tese, e depois procurar um gancho que combine | a ordem de trabalho é uma só, e ela começa na tese |
| contar para a pessoa quantos candidatos caíram | regra da vitrine: o arquivo registra tudo, a conversa mostra só o que passou |
| perguntar se pode descartar um candidato | o descarte é seu. A escolha entre os que passaram é dela |
| empilhar teste novo em cima dos seis eliminadores | lista longa faz o agente escolher o critério mais fácil de alegar como cumprido. Teste novo só entra mostrando um defeito que nenhum eliminador existente derruba |
| aprovar o candidato porque o gancho ficou bonito | gancho bonito na frente de nada é o defeito. O corpo precisa pagar (R1) |
| deixar entrar um trecho excelente que é de outra ideia | R2. Ele volta para a varredura como candidato a outro corte |
| entregar cinco cortes medianos em vez de dois que valem | `max_cortes` é teto (`VALOR.md`, seção 6) |
| inventar um corte ruim porque nada sobreviveu | o diagnóstico é a entrega (`VALOR.md`, seção 7) |
| apresentar o pool mostrando só o gancho | quem decide olhando só a abertura decide pelo mesmo viés que causou o problema. O aprendizado vai na primeira linha |
| propor o começo do vídeo como gancho de uma afirmação | ali o começo é aquecimento. Afirmação é tese, e tese quase nunca está no minuto 1. No trajeto é o contrário, e a introdução costuma ser a abertura |
| cinco candidatos tirados do mesmo trecho de cinco minutos | cobrir os três terços é obrigação, não sugestão |
| dois cortes de trajeto do mesmo vídeo | o trajeto cobre o arco inteiro. O segundo é o primeiro reescrito (`referencias/FORMATOS.md`, seção 5) |
| trajeto entregue sem destino | são quatro blocos obrigatórios. O destino quase sempre já existe gravado, no encerramento do vídeo |
| reescrever candidato derrubado até parecer bom | candidato que caiu, caiu. Texto polido em cima de ideia vazia continua vazio |
| fechar ponto de corte pelo tempo da palavra | o alinhador estica a palavra para dentro do silêncio. Sempre confira a energia |
| planejar painel que repete a legenda | o painel mostra a coisa, a legenda carrega a fala |
| resolver coisa concreta com um card escrevendo o nome dela | rode a ordem de decisão de `referencias/REPRESENTACAO.md`. Card com nome é palavra fingindo ser desenho |
| desenhar o mock de uma ferramenta de memória | ela está na fonte: extraia o quadro e olhe. Memória entrega interface genérica |
| descobrir no render que falta o logo de uma marca | o lote de download é da etapa 0. No render já é tarde, porque o painel foi autorado inteiro |
| pular o inventário em vídeo "simples" | ele roda sempre. Vídeo simples é justamente aquele em que tudo vira card |
| escrever a leitura fria do candidato que você mesmo escolheu | quem escolheu já sabe o assunto e não consegue desconhecer. A leitura fria é do subagente |
| deixar "Contexto que falta" em branco | branco não é "não falta nada", é campo não preenchido. Ou a frase, ou "nenhum" |
| abrir o corte pelo contexto para o gancho ficar claro | a ordem é gancho, contexto, prova, fechamento. O gancho é o primeiro som |
| terminar o corte longe da âncora | R6. Abriu em planilha, fecha em planilha |
