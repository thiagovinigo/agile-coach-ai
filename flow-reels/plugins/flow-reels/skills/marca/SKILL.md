---
name: marca
description: 'Onboarding da identidade visual, roda uma vez por pessoa. Conversa para descobrir fonte, cor de destaque, superfície clara ou escura, logo e personagem, extrai o que der de um manual de marca ou de um print, trata fonte variável gerando a estática, e grava marca/marca.md, marca/tokens.json e as fontes em marca/fontes/. Termina renderizando um painel de amostra 1080x956 para aprovação, e só depois marca ''marca'': true no setup.json. Use para ''configurar minha marca'', ''meus cortes estão com a cara errada'', ''trocar a cor do painel'', ''mudar a fonte dos cortes'', ''refazer o onboarding'', e sempre que o setup.json estiver com ''marca'': false. Não produz corte nenhum.'
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Marca (/flow-reels:marca)

> **Onde mora cada coisa.** Esta skill está em `${CLAUDE_SKILL_DIR}` e o plugin Flow Reels em
> `${CLAUDE_PLUGIN_ROOT}`. Caminhos como `referencias/...` e `scripts/...` são desta skill;
> `skills/...` e `componentes/...` são do plugin (o que a pessoa baixou fica em `componentes/` da pasta
> de trabalho e vale por cima); `projetos/`, `marca/`, `pautas/`, `setup.json` e `.env` são da pasta de
> trabalho, o diretório onde o Claude Code está aberto. Todo script roda com `flow-reels <skill>/<script>`,
> que está no PATH enquanto o plugin está ligado e já usa o Python e o ffmpeg certos
> (`flow-reels lista` mostra todos; `flow-reels instalar` prepara uma pasta nova).

Esta skill é o que separa um corte genérico de um corte que parece da pessoa. Ela roda **uma vez**,
antes do primeiro corte, e grava três coisas que todo o resto do pacote lê: a lei da marca em prosa,
os valores em JSON, e os arquivos de fonte dentro da pasta.

Duas coisas mandam aqui:

1. **Quem decide é a pessoa, não a medição.** Você propõe com número na mão, ela confirma ou corrige.
   Print e manual servem para você chegar com uma proposta pronta, não para dispensar a conversa.
2. **Nada fica pronto sem o painel de amostra aprovado.** Enquanto a pessoa não olhar um quadro de
   verdade e disser que é a cara dela, `setup.json` continua com `"marca": false`.

Ela **não produz corte**. Terminou o onboarding, devolva a conversa para quem chamou.

---

## 1. Quando disparar

| situação | o que fazer |
|---|---|
| `setup.json` está com `"marca": false` | dispare, antes de qualquer outra etapa |
| a pessoa pede para trocar cor, fonte ou superfície | dispare em modo ajuste, direto na pergunta que interessa |
| a pessoa diz que o corte "não parece meu" | dispare em modo ajuste e comece mostrando o painel de amostra atual |
| `setup.json` já está com `"marca": true` e ninguém reclamou | **não dispare**, siga o fluxo normal |

No modo ajuste você não refaz as sete perguntas. Pergunta o que mudou, muda, renderiza a amostra de
novo e pede o aceite outra vez. O aceite é sempre necessário, mesmo para trocar uma cor só.

---

## 2. Abertura: material antes de pergunta

A primeira mensagem é uma só, e pede material. Fazer a pessoa responder sete perguntas quando ela
tem um manual de marca no computador é desperdiçar o tempo dela e correr o risco de ela responder de
memória, errado.

> Antes de começar os seus cortes, preciso aprender a sua cara, e isso leva uns cinco minutos.
>
> Você tem algum destes? Manual de marca em PDF, um print de um post ou capa sua, o site, ou os
> arquivos da sua fonte. Qualquer um serve, e quanto mais completo, menos eu te pergunto.
>
> Se você não tiver nada disso agora, tudo bem, eu te pergunto na mão. E se quiser pular tudo e ver
> um corte primeiro, é só dizer: eu uso um padrão neutro e a gente ajusta depois.

Conforme o que vier:

| o que a pessoa mandou | o que você faz |
|---|---|
| **manual de marca** (PDF, doc, página) | leia, extraia cores, fontes e regras de uso, e traga tudo já preenchido para confirmação |
| **print de uma peça** | siga `referencias/EXTRAIR-DE-IMAGEM.md` do começo ao fim, e traga a proposta medida |
| **link do site** | peça um print da página, porque medir imagem é mais confiável que adivinhar CSS |
| **só os arquivos de fonte** | trate as fontes primeiro, e depois pergunte cor e superfície na mão |
| **nada** | vá para as perguntas |
| **"pula isso"** | vá para o item 7, o caminho do padrão |

Com material em mãos, **a conversa encurta mas não some**. Você deixa de perguntar e passa a
confirmar: "medi isso, confere?". Confirmação é rápida, e é o que evita gravar um laranja que na
verdade é vermelho na cabeça da pessoa.

---

## 3. As perguntas

Sete, **uma por mensagem**, na ordem abaixo. Cada uma vem com exemplo, em linguagem de quem não é
designer. Ninguém aqui precisa saber o que é hexadecimal, nem o que é peso de fonte.

**1. A fonte do título.**
> Qual fonte você usa nos títulos? Se você tiver o arquivo (`.ttf` ou `.otf`), me manda que eu uso
> exatamente essa. Se não tiver, me diz o nome, ou me descreve: é arredondada e amigável, é seca e
> técnica, ou tem pezinho tipo revista?

Sem resposta útil, ofereça a Quicksand que já vem no pacote, e diga que ela é arredondada e amigável.

**2. A fonte da legenda.**
> A legenda queimada no vídeo pode ser a mesma do título, e na maioria das vezes é o que fica melhor.
> Quer manter a mesma, ou usar outra?

Uma regra para dizer em voz alta se ela quiser outra: legenda precisa de peso. Fonte fina a 116 px
sobre vídeo some assim que a plataforma comprime.

**3. A cor de destaque.**
> Qual é a sua cor? Aquela que aparece no botão, no detalhe, no que você quer que a pessoa olhe.
> Uma só. Se você tiver o código, manda; se não, me diz o nome e eu te mostro opções.

Se ela mandar duas ou três, pergunte qual é a principal. O painel usa **um** acento. Duas cores de
destaque no mesmo quadro significam duas coisas importantes ao mesmo tempo, e aí nenhuma é.

**4. A superfície.**
> Seus cortes ficam melhores com o painel de cima em **fundo escuro** ou em **fundo claro**? Escuro
> passa uma sensação mais técnica e noturna; claro passa uma sensação mais limpa e direta.

Escolha uma e não alterne entre cortes. Alternar quebra o reconhecimento, que é a única coisa que a
identidade compra.

**5. A logo.**
> Tem logo em PNG com fundo transparente? Ela entra no painel quando a fala falar dela, e no fim do
> corte. Se você tiver uma versão clara, para fundo escuro, manda as duas.

Sem logo, siga sem. Logo não é obrigatória e logo pequena demais vira sujeira.

**6. Mascote ou personagem.**
> Você tem algum boneco, mascote ou figura que te representa? A maioria das marcas não tem, e isso
> não é problema. Se você tiver, e tiver mais de uma pose, manda todas.

Personagem é ator, não adesivo. Ele entra quando a fala pede reação, e nunca é repintado com a cor
de destaque: ele entra com as cores dele.

**7. A foto da capa.**
> Toda capa de reel é montada sobre uma foto sua, recortada, com a promessa do corte em cima. Me manda
> uma foto em que você aparece da cintura para cima, de frente, com boa luz. Fundo simples ajuda, mas
> não precisa: eu tiro o fundo.

Copie para `marca/foto.jpg` (ou `.png`, mantendo a extensão) e grave no `setup.json`, em `capa`,
`{"foto": "marca/foto.jpg", "recorte": "marca/foto-recorte.png"}`. O recorte sem fundo sai sozinho na
primeira capa (`flow-reels produzir/capa` chama o `tirar-fundo`). Sem foto, siga: a capa avisa o que
falta quando chegar a vez dela.

### Como conduzir

- Uma pergunta por mensagem, e **espere a resposta**. Despejar as sete de uma vez faz a pessoa
  responder três e esquecer as outras.
- Resposta vaga vira proposta concreta. "Um azul" vira "azul tipo céu de meio-dia, ou azul mais
  fechado, tipo marinho?", com dois códigos para ela escolher.
- Se ela não souber, **escolha por ela e diga o que escolheu**. Decidir é serviço; empurrar decisão
  de volta para quem já disse que não sabe é o contrário disso.
- Não pergunte raio de canto, espessura de borda, grão nem entrelinha. Isso você deriva, e o valor
  padrão de `marca/tokens.exemplo.json` está certo para quase todo mundo.

---

## 4. Tratar a fonte antes de gravar

Todo arquivo de fonte que entrar passa por aqui, sem exceção, inclusive os que já parecem prontos.

```bash
flow-reels marca/tratar_fonte caminho/da/fonte.ttf \
    --pesos 700,500 --saida marca/fontes
```

O script descobre se a fonte é **variável** e, se for, gera as instâncias estáticas. Isso não é
capricho: o queimador de legenda do ffmpeg ignora o eixo de peso de uma fonte variável e desenha no
peso padrão do arquivo, que na maioria das famílias modernas é Light. O resultado seria uma legenda
fina que some na compressão, e o defeito só apareceria no vídeo pronto.

A saída traz, para cada arquivo gerado, o **nome de família real**. Esse nome é o que vai em
`tokens.json`, e é por ele que a legenda encontra a fonte. Nunca chute o nome a partir do nome do
arquivo: `Quicksand-Medium.ttf` se apresenta como família `Quicksand Medium`, e `Quicksand-Bold.ttf`
se apresenta como família `Quicksand`, com o negrito no estilo. O script resolve isso e ainda diz,
em `negrito_no_ass`, quando a legenda precisa nascer com negrito ligado.

O bloco `para_os_tokens` da saída já vem no formato dos tokens. Complete o caminho com a pasta
(`marca/fontes/<arquivo>`) e cole.

**Copie sempre as fontes para dentro de `marca/fontes/`.** Fonte que mora na pasta de download da
pessoa desaparece, e o corte seguinte renderiza numa fonte de sistema qualquer, sem avisar.

---

## 5. O que gravar

Dois arquivos, e os dois são obrigatórios. Um é para máquina ler, o outro é para agente ler.

### `marca/tokens.json`

Os valores. O esquema, o nome de cada chave e o que cada uma significa estão em
**`marca/tokens.exemplo.json`**, que é o contrato. Leia esse arquivo antes de escrever o seu e siga
exatamente as mesmas chaves. Componente nenhum escolhe cor no olho: tudo sai daqui.

Três conferências antes de salvar:

1. **Contraste da tinta com a superfície**, no mínimo 4,5 para 1. Abaixo disso o texto some no vídeo.
2. **Contraste de `destaque_contraste` sobre `destaque`**, mesmo piso. Se nem o claro nem o escuro
   passarem, grave o melhor dos dois e escreva em `marca.md` que o acento não carrega texto.
3. **Toda fonte com `"variavel": false`** e apontando para um arquivo que existe dentro da pasta.

### `marca/marca.md`

A lei em prosa, escrita para o agente ler antes de desenhar um painel. Não é um resumo do JSON: é o
que o JSON não consegue dizer. Escreva em português, direto, e cubra:

- **quem é a marca em uma frase**, e o que ela não é;
- **a superfície e por quê**, com a regra de não alternar entre cortes;
- **o acento e o critério de uso**: uma coisa por vez, a que a fala está apontando agora;
- **as fontes, com o nome de família real** e onde cada uma entra;
- **a logo**: quando entra, quando não entra, altura mínima;
- **o personagem**, se existir: quando ele aparece e o que ele nunca faz;
- **o que está proibido nesta marca**, que costuma ser a parte mais útil do arquivo. Exemplo de
  frase útil: "nunca use o acento como fundo de bloco de texto, ele só vale como borda e traço".

---

## 6. O painel de amostra e o aceite

```bash
flow-reels marca/painel_amostra
```

Renderiza um quadro de 1080 por 956, que é exatamente o painel de cima de um corte, aplicando
`marca/tokens.json`. O quadro mostra de propósito a superfície, o título com um trecho no acento,
dois cards (um neutro e um destacado), os chips numerados com um aceso, o rótulo em caixa alta, o
grão e o brilho de fundo. Ou seja, quase tudo que a pessoa vai ver nos cortes dela.

Mostre o arquivo com o **caminho completo**, para ela abrir com um clique, e pergunte de um jeito
que dê espaço para ela reclamar:

> Este é o painel de cima dos seus cortes, com a sua marca aplicada. Olha o arquivo:
> `<caminho completo do PNG>`
>
> É a sua cara? Se tiver qualquer coisa fora, me diz agora: cor, fonte, se está escuro demais, se o
> arredondamento não é o seu. Mudar aqui leva um minuto; mudar depois de cinco cortes prontos, não.

Reclamou, você corrige os tokens e renderiza de novo. Quantas vezes forem necessárias. Duas opções
úteis nessa hora:

- `--guias` desenha as margens e a **zona quieta** de 170 px na base, onde a legenda passa. Serve
  para explicar por que o conteúdo não desce até o fim.
- `--titulo "..."` e `--destaque-em "..."` trocam o texto da amostra, o que ajuda quando a pessoa
  quer ver um título de verdade dela, com as palavras e os acentos dela.

**Aprovou, e só então:** grave `"marca": true` no `setup.json` da raiz, mexendo nessa chave e em mais
nenhuma. Confirme para a pessoa que a partir dali todo corte já nasce com a marca dela, e que ela
pode mudar qualquer coisa depois pedindo o ajuste.

---

## 7. O caminho de quem quer pular

Se a pessoa disser que quer pular, **pule de verdade**, sem insistir e sem uma segunda pergunta
disfarçada de confirmação. Grave o padrão:

| token | valor padrão |
|---|---|
| modo | escuro |
| fontes | Quicksand, as estáticas que já vêm em `marca/fontes/` |
| destaque | um acento neutro, âmbar discreto, que não finge ser a marca de ninguém |
| logo e personagem | sem |
| resto | os valores de `marca/tokens.exemplo.json` |

Escreva o `marca.md` mesmo assim, curto, dizendo em uma linha que a identidade ainda não foi
definida e que o padrão está no ar. Renderize a amostra, mostre, e grave `"marca": true` se ela
aceitar seguir. Feche com a porta aberta:

> Beleza, vamos com o padrão para você ver o formato funcionando. Quando quiser deixar com a sua
> cara, é só me dizer "configura minha marca" e a gente faz em cinco minutos.

---

## 8. Erros que já custaram tempo

- **Gravar tokens antes do aceite.** O painel de amostra é o gate. Antes dele, o que você tem é uma
  proposta, e proposta não vira `"marca": true`.
- **Apontar a fonte para fora da pasta.** O caminho tem que ser relativo à raiz do pacote e o arquivo
  tem que estar em `marca/fontes/` ou em `fontes/`. Caminho absoluto quebra na máquina seguinte.
- **Chutar o nome de família.** Use o que `tratar_fonte.py` devolveu, letra por letra.
- **Aceitar duas cores de destaque.** Insista uma vez, com o motivo, e grave uma só.
- **Perguntar coisa de designer.** Raio, grão, entrelinha e espessura de traço você deriva. Perguntar
  isso faz a pessoa achar que precisa entender de design para ter um corte bonito.
- **Deixar a conversa virar consultoria de marca.** O objetivo é sair daqui com o painel aprovado. Se
  a pessoa quiser repensar a identidade dela, ótimo, mas isso é outro dia e outro assunto.
