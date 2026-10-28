---
name: tendencias
description: 'O modo Tendências da Fábrica: decide o que vale gravar. Duas entradas. Nicho: varre o que está bombando no nicho do setup.json (Reddit sem chave com voto real, YouTube Brasil, GitHub Trending, Hacker News, Product Hunt). Tema: pesquisa o que está em alta sobre um assunto que a pessoa traz (Reddit, Hacker News, YouTube com transcrição, X com chave, web), com dois passes, português e inglês. As duas passam pela mesma régua (eliminadores, pontuação, fato conferido na fonte) e entregam cada pauta aprovada pronta para gravar: roteiro de 40 a 50 s no tamanho da fala medida, fatos com link, prints e rolagem, logos no acervo, rascunho das cenas e texto do post com a palavra da DM. Use para ''busca tendências'', ''o que está bombando'', ''me dá pautas'', ''ideias de reels'', ''roteiro de reels'', ''o que gravar essa semana'', ''conteúdo viral'', ''o que tá em alta sobre X'', ''pesquisa tendência de X'', ''me dá ideias de corte sobre X'', ''não tenho vídeo, só o tema''. Não grava nem produz o corte; depois da gravação, quem produz é o `/flow-reels:fabrica`, e o reel sem rosto é do `/flow-reels:narrado`.'
---

# Tendências (/flow-reels:tendencias)

> **Onde mora cada coisa.** Esta skill está em `${CLAUDE_SKILL_DIR}` e o plugin Flow Reels em
> `${CLAUDE_PLUGIN_ROOT}`. Caminhos como `referencias/...` e `scripts/...` são desta skill;
> `skills/...` e `componentes/...` são do plugin (o que a pessoa baixou fica em `componentes/` da pasta
> de trabalho e vale por cima); `projetos/`, `marca/`, `pautas/`, `setup.json` e `.env` são da pasta de
> trabalho, o diretório onde o Claude Code está aberto. Todo script roda com `flow-reels <skill>/<script>`,
> que está no PATH enquanto o plugin está ligado e já usa o Python e o ffmpeg certos
> (`flow-reels lista` mostra todos; `flow-reels instalar` prepara uma pasta nova).

Esta skill fica **antes** da Fábrica de Cortes. A Fábrica transforma vídeo gravado em corte; esta
skill decide o que vale gravar e entrega o que for preciso para gravar sem pensar: o roteiro para ler
e o material para o reel mostrar.

A régua é de quem é **referência no próprio nicho**: não publica rumor nem número inventado. Todo fato
do roteiro é conferido na fonte antes de ir para o papel, e a pesquisa vale pelo que ela traz de fora
do seu conhecimento. O seu treino não sabe o que saiu na semana passada: **pauta sem um achado por
trás é palpite**.

## As duas entradas

| a pessoa disse | a entrada | a busca | onde cai |
|---|---|---|---|
| "o que está bombando", "me dá pautas", "o que gravar essa semana" | **nicho** | `scripts/buscar_tendencias.py`, com o nicho, os subreddits, os termos e as buscas do YouTube de `setup.json` → `pautas` | `pautas/<AAAA-MM-DD>/` |
| "o que tá em alta sobre X", "ideias de corte sobre X", "não tenho vídeo, só o tema" | **tema** | `scripts/radar/radar.py`, só com o tema dela | `pautas/radar/` |

Na dúvida, um assunto nomeado é tema; nenhum assunto é nicho. Da etapa 2 em diante as duas seguem o
mesmo caminho.

## As referências

| arquivo | manda em |
|---|---|
| `referencias/CRITERIOS.md` | eliminadores, pontuação, ângulos e o que vai para a vitrine |
| `referencias/ROTEIRO.md` | tamanho pela fala medida, os cinco blocos, regras de escrita, a palavra da chamada |
| `referencias/KIT.md` | a pasta da pauta, os assets, o rascunho das cenas, as instruções de gravação |
| `referencias/RADAR-METODOLOGIA.md` | entrada tema: o assunto central, as buscas da web por tipo de pergunta, os subreddits brasileiros, o peso de cada fonte |
| `referencias/RADAR-SINTESE.md` | entrada tema: como a pilha de achados vira sinal (consenso, contradição, o que começa a aparecer) |
| `referencias/RADAR-BRIEF.md` | entrada tema: o modelo exato do brief |

Leia `CRITERIOS.md`, `ROTEIRO.md` e `KIT.md` antes da etapa 2, e as três do radar antes da etapa 1B. Em
divergência entre este arquivo e uma referência, a referência vence.

## Ambiente

Todos os scripts rodam pelo `flow-reels`, com o Python da pasta de trabalho, que já traz o `yt-dlp`.

## Etapa 1A: buscar no nicho

```
flow-reels tendencias/buscar_tendencias \
  --saida pautas/<AAAA-MM-DD>/tendencias.json --janela semana
```

`--janela dia` para o que subiu nas últimas 24 horas. O script lê:

- **Reddit**, os subreddits de `pautas.subreddits`. Sem chave nenhuma, pela listagem do shreddit, que
  traz voto e comentários de verdade; o subreddit que a listagem não trouxe cai no RSS. Com
  `REDDIT_CLIENT_ID` e `REDDIT_CLIENT_SECRET` no `.env`, a API oficial;
- **YouTube**, as buscas de `pautas.youtube`, enviados na janela, região Brasil, com visualizações e a
  transcrição do mais visto de cada busca;
- **GitHub** Trending e repositórios novos, **Hacker News** e **Product Hunt**, filtrados pelos termos
  de `pautas.termos`.

O resumo no fim diz quantos itens vieram de cada fonte e o que ficou de fora. Diga em uma linha o que
ficou de fora, sem explicar com palpite.

**Complete com a web.** Com as ferramentas de busca e leitura de página, procure o que a busca
automática não alcança: lançamentos das empresas do nicho nos últimos dias. Acrescente o que achar ao
`tendencias.json` com `"fonte": "web"` e o link.

## Etapa 1B: pesquisar um tema

### 1. Já existe um brief recente desse tema?

```
flow-reels tendencias/radar "<tema>" --recentes
```

Achou um dos últimos 7 dias? Diga em uma linha e pergunte se usa esse, refaz, ou é outro recorte.
Tendência de uma semana atrás ainda é tendência, e refazer gasta o limite do Reddit à toa.

### 2. Entender o pedido

- **o tema**, do jeito que ela falou. Não troque por um sinônimo nem acrescente produto: se ela disse
  "IA para gerar imagem", a busca não vira "Midjourney";
- **o termo em inglês**, do jeito que a comunidade de língua inglesa fala ("AI coding agents", e não
  "AI agents for programming");
- **o tipo de pergunta**: recomendação, notícia, como fazer ou geral (`RADAR-METODOLOGIA.md` seção 2);
- **a profundidade**: `--rapida`, padrão ou `--funda`; sem pedido, `setup.json` → `radar.profundidade`;
- **a janela**: `setup.json` → `radar.dias` (30), a não ser que ela peça outra ("dessa semana" é `--dias 7`);
- **dois a quatro subreddits brasileiros** que caibam no tema (`RADAR-METODOLOGIA.md` seção 3), em
  `--subreddits`.

Tema vago demais ("tecnologia", "saúde") merece **uma** pergunta de recorte. Mais de uma é
interrogatório: escolha o recorte mais provável e diga qual escolheu.

### 3. Rodar o radar, sempre

```
flow-reels tendencias/radar "<tema>" --termo-en "<tema em inglês>" \
  --subreddits <sub1>,<sub2>
```

O primeiro passe roda em português; toda fonte que voltar fraca roda de novo em inglês, e o resumo diz
quanto veio de cada passe. **Quando o inglês entrou, o brief diz**: achado gringo é sinal de que o
assunto está chegando, não de que já chegou aqui.

Reddit, Hacker News e YouTube rodam sem chave. `XAI_API_KEY` liga o X; `OPENAI_API_KEY` só reforça o
Reddit quando ele volta vazio. Chave faltando nunca bloqueia: avise uma vez, numa linha, e siga.

**Ler a cobertura.** Cada fonte sai com o número de itens ou o motivo: `não configurado` (falta
chave), `não instalado` (falta o `yt-dlp`), `limitado (429)` (espere um minuto e rode só ela com
`--fontes reddit`), `bloqueado (403)`, `vazio de verdade`. Nunca explique um buraco com palpite, e
leve a ressalva para o brief.

### 4. A web

Por cima do radar, a ferramenta de busca da web para blogs, notícias e documentação, em português
primeiro, pelas consultas de `RADAR-METODOLOGIA.md` seção 2: de 4 a 6 buscas na rápida, de 6 a 10 na
padrão, de 10 a 15 na funda. **Não busque `site:reddit.com`**: a busca da web não chega no Reddit, e
o Reddit vem do script.

### 5. Sintetizar e escrever o brief

Pelo `RADAR-SINTESE.md`: fique no que as fontes disseram, pese pelo engajamento, procure consenso,
contradição e o que começa a aparecer, e separe o Brasil do resto. Grave o brief em
`pautas/radar/AAAA-MM-DD-<tema-em-slug>.md`, no modelo do `RADAR-BRIEF.md`. As ideias de corte do
brief são as candidatas da etapa 2.

## Etapa 2: julgar e apresentar

Pelo `CRITERIOS.md`: primeiro os eliminadores, depois a pontuação com a conta anotada, depois o
ângulo. Antes de eliminar pelo P3, levante o que já foi gravado:

```
ls projetos/
grep -rhoE "[Cc]omenta[m]? [A-ZÁÉÍÓÚÇ0-9-]{2,}" projetos/*/materiais-de-trabalho/publicacao/ projetos/*/ROTEIRO.md 2>/dev/null | sort -u
```

**Confira o topo antes de apresentar.** Para cada uma das cinco primeiras, abra a fonte e confirme que
ela existe, que diz o que o post diz e que o fato principal do gancho se sustenta. Pauta que não se
confirma cai pelo P2 e a sexta sobe.

**O gancho é falado.** As regras são as da abertura de um corte (`${CLAUDE_PLUGIN_ROOT}/skills/planejar/referencias/FORMATOS.md`
seção 2): frase completa, sem conectivo nem pronome sem antecedente no começo, o assunto nomeado, e
uma afirmação ou uma promessa.

**Cada pauta sugere o caminho de produção**, que o planejador confirma quando o vídeo chegar:

| caminho | o que sai | cabe quando |
|---|---|---|
| `cenas` | o reel inteiro em cenas, com o rosto (o padrão) | a ideia mora em quem fala: opinião, história, provocação, lista |
| `mundo` | a coisa real ocupa a tela, a câmera passeia por ela e o rosto entra como respiro | a fala aponta o tempo todo para um objeto: um app, um arquivo, uma planilha, um gráfico |
| `narrado` | sem rosto, uma voz narra por cima de filmagem real | lançamento ou notícia com imagem pública, quando a pessoa não precisa aparecer |

Grave o estoque inteiro (`pautas/<data>/RANKING.md` no nicho; a seção de ideias do brief no tema) e
apresente na conversa só as cinco da vitrine, no formato da seção 4 do `CRITERIOS.md`:

```
1. "O ElevenLabs cobra. Essa aqui é de graça e clona sua voz com três segundos de áudio."
   (alternativa grátis a algo pago, cenas) · 61/75
   Por que agora: 2.300 estrelas no GitHub em 4 dias, top 3 do r/LocalLLaMA na semana.
   Link: https://github.com/...
```

Na entrada tema, abra com duas ou três frases do que está em alta e cite no "por que agora" o id do
achado do radar (R2, H1, Y3) com o número.

E **pare**. Pergunte quais viram roteiro. Pode ser uma, pode ser todas.

## Etapa 3: montar cada pauta aprovada

Para cada pauta aprovada, na ordem, seguindo o `KIT.md`:

1. **Crie a pasta** `projetos/<nome-da-pauta>/`.
2. **Confira os fatos** na fonte, um por um, e anote cada um com o link no `PAUTA.md`. Fato que não se
   confirma sai.
3. **Meça a fala** com `scripts/medir_fala.py` e **escreva o `ROTEIRO.md`** pelo `ROTEIRO.md` da
   referência: cinco blocos, 40 a 50 s, palavra de chamada inédita, grafia para a legenda, fontes, e o
   que testar antes de gravar. Conte as palavras e ponha o número no cabeçalho.
4. **Baixe os logos** das marcas nomeadas com `componentes/logos/baixar-logo.py`.
5. **Capture os assets** com `scripts/capturar_assets.py`, e olhe os prints.
6. **Escreva o rascunho visual**, o `cenas-rascunho.md`: cada bloco do roteiro com o modo da cena, a
   transição e o que entra, partindo do modelo do ângulo em
   `${CLAUDE_PLUGIN_ROOT}/skills/planejar/referencias/MODELOS-DE-CENAS.md` (seção 3 do `KIT.md`). No caminho `mundo`,
   o rascunho diz o objeto herói de cada bloco e a superfície (seção 3 do `KIT.md`).
7. **Escreva o `legenda-reels.md`** do post, no mesmo tom dos que já existem em
   `projetos/*/materiais-de-trabalho/publicacao/`: primeira linha é o gancho, um bloco curto com as
   provas, a chamada com a mesma palavra do roteiro, cinco hashtags. Sem travessão.
8. **Feche o `PAUTA.md`** com o link da DM, a lista de assets, o que falta e as instruções de gravação.

**Pauta no caminho `narrado`** não ganha `ROTEIRO.md` para gravar: ela vai para o `/flow-reels:narrado`, com
os fatos conferidos e o link da fonte, e o roteiro segue a lei dele (de 90 a 130 palavras, para a voz).

Com mais de uma pauta aprovada, monte cada uma num subagente próprio, em paralelo, até três ao mesmo
tempo. Cada um escreve só na pasta da sua pauta. O `baixar-logo.py` mexe no acervo compartilhado,
então rode o lote de logos de todas as pautas **antes** de abrir os subagentes.

## Etapa 4: entregar

Para cada pauta, uma linha com o caminho completo do `ROTEIRO.md`, a duração, o número de palavras, a
palavra da chamada e o caminho de produção. Depois:

- o que ela precisa testar antes de gravar, quando algum `[TESTAR ANTES DE GRAVAR]` ficou no roteiro;
- as palavras de chamada que precisam ser configuradas na automação de DM, com o link de cada uma;
- a instrução de como mandar o vídeo depois: o arquivo, dizendo de qual pauta ele é.

## Quando o vídeo gravado chegar

Chame o `/flow-reels:fabrica` com o arquivo e a pasta da pauta. A pasta já tem o `ROTEIRO.md`, e é isso
que diz ao planejador que o corte é a gravação inteira (seção 6 do `KIT.md`).

## Quando dá errado

| o que você vê | o que é | o que fazer |
|---|---|---|
| `Reddit: limitado (429)` | buscas seguidas no Reddit (a varredura do nicho logo antes de um tema, por exemplo) | espere um minuto e rode só o Reddit: `--fontes reddit` |
| Reddit com comunidades de outro país | a palavra é igual em outras línguas ("creatina" é espanhol e italiano também) | passe subreddits brasileiros em `--subreddits` e diga no brief de onde é cada conversa |
| `YouTube: não instalado` | falta o `yt-dlp` | `.venv/bin/pip install yt-dlp` |
| YouTube sem transcrição | o YouTube limitou o pedido de legenda, ou o vídeo não tem | o vídeo entra com título e visualizações |
| `X: não configurado` | falta `XAI_API_KEY` | avise uma vez e siga |
| tudo fraco em português | o assunto ainda não chegou aqui, ou o termo está estranho | confira o `--termo-en`; tire os modificadores e busque o substantivo central |
| resultado com cara de velho | a janela está larga para um assunto rápido | `--dias 7` |

## O que esta skill não faz

- Não publica nem agenda nada.
- Não faz login, não aceita termos nem cookies, não preenche formulário em site nenhum.
- Não copia texto de post de terceiro para o roteiro. Ela lê, confere e escreve com as palavras do
  criador.
- Não inventa número. Fato sem fonte não entra, e achado sem engajamento conhecido diz isso.
- Não troca o tema da pessoa pelo que acha mais interessante.
- Não grava o vídeo nem produz o corte.
