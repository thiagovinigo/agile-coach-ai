---
name: narrado
description: 'Formato opcional do pacote: um reel vertical sem rosto, de 40 a 50 s, em que uma voz da ElevenLabs narra por cima de filmagem real (filme de lançamento, gravação de tela, filmagem da própria pessoa sem fala), com o som da filmagem mudo, cartão de abertura com o logo oficial, empurrões e anel desenhado no que a voz nomeia, legenda palavra a palavra e fechamento "comenta a palavra". Use para ''reel narrado'', ''reel sem rosto'', ''narra esse lançamento'', ''faz um reel com voz por cima desse vídeo'', ''reel de lançamento'', ''quero um reel com locução em cima dessa gravação de tela''. Precisa de ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID no .env. Não corta vídeo longo com o rosto da pessoa em cortes (isso é o `/flow-reels:fabrica`), não clona voz, não usa outro serviço de voz e não publica: publicar é do `/flow-reels:publicar`, com sim explícito.'
---

# Narrado (/flow-reels:narrado)

> **Onde mora cada coisa.** Esta skill está em `${CLAUDE_SKILL_DIR}` e o plugin Flow Reels em
> `${CLAUDE_PLUGIN_ROOT}`. Caminhos como `referencias/...`, `modelos/...` e `scripts/...` são desta skill;
> `skills/...` e `componentes/...` são do plugin (o que a pessoa baixou fica em `componentes/` da pasta
> de trabalho e vale por cima); `projetos/`, `marca/`, `setup.json` e `.env` são da pasta de trabalho, o
> diretório onde o Claude Code está aberto. Todo script roda com `flow-reels <skill>/<script>`, que está no
> PATH enquanto o plugin está ligado e já usa o Python e o ffmpeg certos (`flow-reels lista` mostra todos).

Um reel vertical de 40 a 50 s, 1080 x 1920, sem rosto. Uma voz da ElevenLabs conta o que a filmagem
mostra, do quadro zero: a filmagem real é a heroína em largura cheia, o som dela fica mudo, a câmera
empurra devagar no que a voz nomeia e um anel desenhado à mão se desenha ali. Abre com o momento
real mais forte e um cartão de título, fecha com "comenta a PALAVRA" e o item prometido voando para a
DM. É um formato opcional do pacote, ao lado dos cortes: ele não depende de vídeo com fala.

**Antes de montar a primeira tomada, leia `referencias/PADRAO-NARRADO.md`.** É a lei do formato. O
roteiro tem a lei dele em `referencias/ROTEIRO.md`, o plano das tomadas em `referencias/TOMADAS.md` e
o som em `referencias/MIXAGEM.md`.

## O que precisa existir antes

| item | onde | se faltar |
|---|---|---|
| chaves da ElevenLabs | `ELEVENLABS_API_KEY` e `ELEVENLABS_VOICE_ID` no `.env` da raiz do pacote | **diga exatamente o que falta e pare**, como abaixo |
| marca definida | `marca/tokens.json`, com `"marca": true` no `setup.json` | chame o `/flow-reels:marca` antes, como o `/flow-reels:fabrica` faz |
| filmagem | arquivo ou link | peça. Sem filmagem real não existe este formato |
| assunto e fonte dos fatos | link oficial ou notas da pessoa | peça. Fato sem fonte não entra no roteiro |
| a PALAVRA e o item prometido | o que a pessoa comenta e o que ela recebe na DM | pergunte, ou proponha e espere o aceite junto com o roteiro |

Confira as chaves sem gastar nada:

```
flow-reels narrado/voz --checar
```

Sem as chaves, o comando lista o que falta, onde colar e sai com código 3. **Repasse essas linhas e
pare ali**, do mesmo jeito que o `/flow-reels:publicar` faz sem a chave da Zernio: não é falha do pacote, é
uma chave que a pessoa ainda não pôs. Nada de outro serviço de voz, nada de voz do sistema, nada de
"faço sem voz por enquanto".

`ELEVENLABS_MODELO` é opcional. O padrão é `eleven_multilingual_v2`, que fala português; `eleven_v3`
também serve e é o único que aceita marcação de interpretação entre colchetes.

**Leito e efeitos: de graça por padrão.** Sem nada em `marca/audio/`, o reel usa o que o pacote traz:
uma trilha calma de `componentes/trilhas/` e os sons sintetizados de `componentes/sons/` (whoosh, pop,
clique, bip, subida, impacto e tick no lugar dos oito efeitos), e o `mixar.py` diz que usou os do pacote.
Quem quer leito e efeitos próprios gera uma vez, com a chave da ElevenLabs, e eles ficam em
`marca/audio/`, valendo por cima dos do pacote em todo reel narrado:

```
flow-reels narrado/gerar_audio --listar
flow-reels narrado/gerar_audio
```

Os pedidos estão em `dados/sons.json`. Só gere se a pessoa pedir: gasta crédito, e o reel já sai
completo com os sons do pacote.

## A pasta

O reel mora na pasta do projeto, com a mesma regra dos cortes: **a pasta de entrega tem o MP4 e mais
nada**, e todo o resto fica debaixo de `materiais-de-trabalho/`.

```
projetos/<nome>/
├── narrado-01/
│   └── narrado-01.mp4                  a entrega, sozinha
├── revisao/                            a página de revisão do pacote
└── materiais-de-trabalho/
    ├── fonte/                          a filmagem, os prints das cartas
    └── narrado-01/
        ├── fatos.md                    cada fato com a fonte dele
        ├── momentos.md                 os momentos reais da filmagem, com o instante
        ├── roteiro.md                  o roteiro aprovado, e as versões anteriores
        ├── roteiro-tts.txt             o texto exato que vai para a voz
        ├── tomadas.json                o plano das tomadas
        ├── voz/                        as tomadas de voz e os tempos por palavra
        ├── construcao/                 linha do tempo, imagem, legenda, mix, abertura e fechamento
        └── conferencia/                folhas de contato, afirmações, relatório
```

O nome da pasta do projeto segue a regra do pacote: curto, minúsculo, com hífen, tirado do assunto.
Se o reel sai de um vídeo que já tem pasta (porque ele também virou cortes), use a mesma pasta: o
`narrado-01/` fica ao lado dos `corte-NN/`, e a revisão mostra os dois. Segundo reel do mesmo
material, `narrado-02`.

## O caminho, etapa por etapa

### 1. Trazer a filmagem

Link: `flow-reels transcrever/baixar --url <link> --projeto projetos/<nome>`, que
deixa o arquivo em `materiais-de-trabalho/fonte/`. Arquivo local: copie para lá. Prefira o filme oficial
inteiro, o keynote ou a gravação mais longa: gente de verdade em cena vale mais que tela.

### 2. Levantar os momentos e os fatos

1. Folha de contato da filmagem, com instante e régua em pixels da fonte:
   `flow-reels narrado/conferir --folha-da-fonte materiais-de-trabalho/fonte/<arquivo> --saida projetos/<nome>/materiais-de-trabalho/narrado-01/conferencia/folha-da-fonte.jpg`
   **Olhe a folha.** Extraia quadros soltos com ffmpeg onde precisar ver de perto.
2. Escreva `momentos.md`: os momentos reais que mostram o produto funcionando, com instante, o que
   aparece e se é gente, resultado ou tela. O mais forte deles abre o reel.
3. Pontos de corte pela energia do áudio, nunca por tempo de transcrição:
   `flow-reels narrado/linha_do_tempo --energia <arquivo>`.
4. Escreva `fatos.md`: cada fato que pode entrar no roteiro, com o link ou o instante da filmagem que
   prova. Se a filmagem tem fala com fatos, a transcrição do pacote serve para ler; nenhum tempo do reel
   sai dela.

### 3. O roteiro, e a primeira parada

Escreva o roteiro pela lei de `referencias/ROTEIRO.md`: de 90 a 130 palavras, de 3 a 5 frases longas
que correm, comercial e não técnico, vendendo a função e não a demonstração, só com fato da filmagem
ou da fonte oficial, e a PALAVRA no fechamento. Guarde em `roteiro.md`.

**Pare e mostre**, em texto, antes de gastar qualquer crédito de voz:

```
Roteiro do reel narrado (112 palavras, cerca de 44 s com a voz natural):

<o roteiro inteiro>

Comentário: AGENTE. Na DM chega: o guia de configuração.
Abre em: o momento em que a planilha se preenche sozinha (41 s do filme).
```

E espere o aceite. Ajuste pedido volta para o roteiro, não para a voz. Aprovado, grave o texto exato
em `roteiro-tts.txt`.

### 4. A voz

Duas ou três tomadas, nunca aceleradas:

```
flow-reels narrado/voz --projeto projetos/<nome> --take a --estabilidade 0.5
flow-reels narrado/voz --projeto projetos/<nome> --take b --estabilidade 0.85 --similaridade 0.9
flow-reels narrado/respirar --projeto projetos/<nome> --take a
```

0,5 dá o gancho animado, 0,85 dá a leitura calma. O `respirar.py` abre de 0,16 a 0,22 s depois de cada
frase. Escolha a tomada pela duração (a fala inteira entre 38 e 48 s) e pelo tempo de cada palavra no
`palavras-<take>.json`; se a pessoa quiser ouvir as tomadas antes, mande os caminhos dos MP3. Fala que
passou de 48 s se resolve cortando roteiro, nunca acelerando.

### 5. O plano das tomadas

Escreva `tomadas.json` a partir de `modelos/tomadas.exemplo.json`, com os campos de
`referencias/TOMADAS.md`: de onde cada tomada vem na fonte, em que palavra ela entra, onde a câmera
empurra, onde o anel se desenha, como ela chega e o crédito. O logo da pílula vem do acervo: em cor,
`componentes/marcas/<nome>.png` com `"logo_monocromatico": false` (o preferido), ou a silhueta de
`componentes/logos/<nome>.svg`. Faltou, `flow-reels componentes/baixar-marca` (em cor, do kit oficial) ou
`flow-reels componentes/baixar-logo <marca>`. Nunca desenhe logo.

### 6. Montar

```
flow-reels narrado/linha_do_tempo --projeto projetos/<nome>
flow-reels narrado/compor_narrado --projeto projetos/<nome> --quadros 0.5 2.5 8 15 30 42
```

**Olhe os quadros soltos** em `conferencia/` antes do render inteiro: título lendo, alvo do empurrão
no lugar, anel em volta da coisa certa, crédito presente, nada importante acima de y 150, à direita de
x 980 ou abaixo de y 1700. Corrija o `tomadas.json` e repita. Depois:

```
flow-reels narrado/compor_narrado --projeto projetos/<nome>
flow-reels narrado/legenda_narrado --projeto projetos/<nome>
flow-reels narrado/mixar --projeto projetos/<nome>
```

O compor avisa quando uma tomada pede mais filmagem do que a fonte tem (o fim congela) e quando uma
tela quase branca está sem empurrão. Aviso desses se resolve no plano, não se ignora.

### 7. Conferir

```
flow-reels narrado/conferir --projeto projetos/<nome>
```

Ele mede formato, faststart, loudness, duração e trecho parado, e monta uma folha de contato por
tomada e a tira dos 5 primeiros segundos. **Olhe cada folha.** Depois preencha
`conferencia/afirmacoes.md`: cada frase da voz contra o que está na tela quando ela é dita. Afirmação
sem prova na tela, ou contra o que a tela mostra, volta para o roteiro, e o roteiro volta para a
pessoa. "Medido: REPROVADO" não vai para a revisão.

### 8. A revisão, a segunda parada

O reel é revisado na **mesma página de revisão do pacote**, servida, com som. Nunca por print, nunca por
lista de arquivo:

```
flow-reels narrado/revisao_narrado projetos/<nome>
```

Antes de chamar a pessoa, escreva no `revisao/revisao.json` o `porque` (o que o reel vende e por que
abre naquele momento) e as `decisoes` de verdade (a tomada escolhida, uma tomada de tela que você não
tinha como trocar por gente). Mande o endereço e o caminho completo do MP4, e espere o veredito pelo
"Copiar feedback". Reprovado volta para a etapa dona do defeito: fala ruim é roteiro ou voz, tomada
errada é plano, legenda é legenda.

### 9. Publicar, só com sim

Aprovado, diga o caminho completo da entrega, `projetos/<nome>/narrado-01/narrado-01.mp4`. Com
`oferecer_publicacao: true` no `setup.json`, ofereça uma vez publicar ou agendar. Aceitou, chame o
`/flow-reels:publicar` com esse caminho: ele escreve a legenda do post (a PALAVRA na primeira linha), monta
o funil "comenta a palavra, recebe na DM", mostra tudo em modo seco e só manda com um sim explícito.
Esta skill não publica nada.

## Retomar no meio

| o que já existe | onde retomar |
|---|---|
| a filmagem em `fonte/`, sem `roteiro-tts.txt` | etapa 2 ou 3. Não baixe de novo |
| `roteiro-tts.txt` sem `voz/` | etapa 4. O roteiro já foi aprovado |
| `voz/palavras-<take>.json` | não gere voz de novo: cada tomada custou crédito. Se só os tempos estragaram, `voz.py --reusar` refaz a partir do alinhamento guardado |
| `tomadas.json` e `construcao/linha_do_tempo.json` | etapa 6, a partir do compor |
| `construcao/abertura/` e `construcao/fechamento/` | o compor reaproveita sozinho enquanto os dados não mudam |
| `construcao/imagem.mp4` sem `legendado.mp4` | só legenda e mix |
| `narrado-NN/narrado-NN.mp4` | etapa 7, conferir, e depois a revisão |

## Como você se comporta

- **Tudo em português do Brasil**, inclusive o texto na tela. Sem travessão em lugar nenhum: os scripts
  recusam roteiro, título, item e legenda com travessão.
- **Três portas são da pessoa:** o roteiro antes da voz, o reel na página de revisão e o sim de
  publicar. Você conduz até a porta.
- **Crédito se gasta uma vez.** Voz só depois do roteiro aprovado; leito e efeitos só com aceite; nada
  de regenerar tomada de voz que já existe sem dizer por que a anterior não serve.
- **Caminho completo** de todo arquivo que a pessoa pode querer abrir.

## O que esta skill não faz

- Não corta vídeo longo com rosto em cortes verticais: isso é o `/flow-reels:fabrica`.
- Não usa outro serviço de voz, não clona voz e não acelera voz.
- Não desenha logo, não inventa fato e não refaz demonstração em desenho quando existe filmagem real.
- Não monta colagem de texto (cards de citação, manchetes, pilhas de rótulo). A razão está em
  `referencias/PADRAO-NARRADO.md`.
- Não publica. Publicar é do `/flow-reels:publicar`, depois da revisão, com sim explícito.
