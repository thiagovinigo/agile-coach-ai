# O kit de gravação

Uma pauta aprovada vira uma pasta de projeto pronta para gravar. Quando o vídeo gravado chegar, ele
entra nessa mesma pasta e a Fábrica produz o corte sem perguntar de novo o que já foi decidido aqui.

---

## 1. A pasta

A pasta nasce em `projetos/<nome-da-pauta>/`, com o nome curto, em minúsculas e com hífen, tirado do
assunto: `omnivoice-clonar-voz`, e não `pauta-3`. É a mesma árvore de
`skills/fabrica/referencias/PASTA-DO-VIDEO.md`, com três arquivos a mais:

```
projetos/<nome-da-pauta>/
├── ROTEIRO.md                        o que se lê na câmera, à vista
└── materiais-de-trabalho/
    ├── pauta/
    │   ├── PAUTA.md                  por que esta pauta, fontes, fatos conferidos, links da DM
    │   └── cenas-rascunho.md         o roteiro já pensado em cenas: modo, transição e asset de cada
    │                                 bloco (no motor 1.0, painel-rascunho.md, os objetos do painel)
    ├── assets/                       prints, rolagens e arte oficial da ferramenta
    └── publicacao/
        └── legenda-reels.md          o texto do post, com a mesma palavra da chamada
```

O lote da busca, que junta todas as pautas de um dia, não fica em `projetos/`, porque não é vídeo.
Ele fica em `pautas/<data>/`, na raiz do pacote:

```
pautas/2026-09-25/
├── tendencias.json    o que a busca trouxe, cru
└── RANKING.md         os eliminadores e a pontuação de cada item, e as cinco da vitrine
```

## 2. `PAUTA.md`

É o que a produção lê depois, então nada aqui é enfeite.

- **o ângulo e o gancho**, iguais aos do roteiro;
- **por que agora**: o sinal de novidade e tração, com o link de onde veio (post do Reddit, trending
  do GitHub, lançamento no Product Hunt);
- **os fatos conferidos**, cada um com o link oficial e o que exatamente foi lido lá;
- **o link para a DM**: o endereço oficial que a automação da palavra de chamada vai mandar. É o link
  da própria ferramenta, nunca o do post do Reddit;
- **os assets**: a lista do que está em `assets/`, com uma linha dizendo o que cada arquivo mostra;
- **o que falta**: logo sem arquivo no acervo, teste pendente, fato que não se confirmou.

## 3. `cenas-rascunho.md` (motor 2.0) ou `painel-rascunho.md` (motor 1.0)

A Fábrica decide os tempos depois de gravar, porque só aí eles existem. Mas a forma de cada ideia se
decide agora, com o roteiro na mão, e é isso que faz o reel sair forte.

**No motor 2.0**, o `cenas-rascunho.md` diz o ângulo da pauta (um dos cinco de
`skills/planejar/referencias/MODELOS-DE-CENAS.md`) e, para cada bloco do roteiro, uma linha:

| bloco | a fala | modo | entrada | o que entra |
|---|---|---|---|---|
| gancho | "O ElevenLabs cobra" | `rosto-vidro` | — | `numero` com o preço, prefixo US$, aceso em "cobra" |
| a virada | "o VoiceStudio faz de graça" | `lado-a-lado` | `clarao` | logos `elevenlabs` × `voicestudio`, `vencedor` na palavra "graça" |
| prova 1 | "três segundos de áudio" | `tela-bolha` | `bolha-encolhe` | `assets/voicestudio-rolagem.webm`, foco no botão de gerar |

No caminho `mundo`, o rascunho diz também, por bloco, o objeto herói (o arquivo, a janela, a planilha, com o conteúdo real) e a superfície: `quadro` na maior parte, `rosto` nos respiros de opinião, `tela` quando o objeto precisa da tela inteira. A lei é a do modo `mundo` no `MOTOR.md`.

Depois da gravação, o planejador põe os tempos e grava o `cenas.json`. O que a linha pede de asset
(print, rolagem, foto livre com crédito, logo) precisa existir na pasta ou no acervo antes de
gravar.

**No motor 1.0**, o `painel-rascunho.md` diz, para cada bloco do roteiro, o objeto do painel:

| bloco | a fala | o objeto que É a ideia | asset ou peça |
|---|---|---|---|
| gancho | "O ElevenLabs cobra" | o card do ElevenLabs com o preço, que é riscado e vira "grátis" | logo `elevenlabs`, peça `card` |
| prova 1 | "três segundos de áudio" | um cronômetro que corre de 0 a 3 s e para | peça `cronometro`, formato `s` |
| prova 2 | "quase 500 idiomas" | o número 500 em escala de título, subindo quadro a quadro | número desenhado no painel, no tamanho de título |

As regras são as do `BEAT-SHEET.md` do planejador: regra C, **mostre a ideia, não a frase**, e
regra D, **a abertura é o trailer**. O herói do painel é um só, e o rascunho já diz qual é.

Toda marca nomeada no roteiro precisa de logo no acervo. Baixe em lote agora:

```
flow-reels componentes/baixar-logo <marca> <marca> <marca>
```

O que não existir no acervo entra na linha "o que falta" do `PAUTA.md`, e o painel resolve com a
palavra. Nunca uma forma parecida.

## 4. Os assets

Para cada ferramenta da pauta, capture o site oficial e o repositório, quando houver:

```
flow-reels tendencias/capturar_assets \
  --saida projetos/<pauta>/materiais-de-trabalho/assets \
  --link site=https://ferramenta.com --link repo=https://github.com/dono/repo
```

**Abra os prints e olhe.** Se um banner de cookie ou de login cobriu a página, anote no `PAUTA.md`
e capture outra página do mesmo site. Não aceite o banner nem faça login para limpar o print.

Os assets são a prova visual. Na Fábrica eles entram pela rota `tela` ou como imagem dentro do
painel, sempre recortados e anotados, nunca crus (`PADRAO-VISUAL.md` seção 9).

## 5. Instruções de gravação

Vão no fim do `PAUTA.md`, e são sempre as mesmas, porque são as que fazem a Fábrica render bem:

- **vertical, 1080 x 1920**, câmera parada, busto enquadrado com ar acima da cabeça;
- **câmera traseira ou espelhamento desligado.** A frontal espelha o que está escrito na roupa e no
  fundo, e a Fábrica não conserta isso sem pedir;
- **um segundo de silêncio antes de começar e depois de terminar**, para o corte cair no silêncio;
- **ler o roteiro inteiro de uma vez.** Errou, pausa dois segundos e recomeça a frase: a
  transcrição acha a pausa e o planejador corta a tentativa errada;
- **luz de frente**, e o microfone perto. A legenda só é tão boa quanto o áudio.

## 6. Quando o vídeo chegar

A pessoa manda o arquivo gravado dizendo de qual pauta ele é. A Fábrica transcreve, e o planejador,
ao ver o `ROTEIRO.md` na pasta, sabe que o corte é a gravação inteira: ele pula o levantamento de
ganchos, usa a grafia do roteiro para corrigir a legenda, parte do `cenas-rascunho.md` para o
`cenas.json` (ou do `painel-rascunho.md` para o `beats.yaml`, no motor 1.0) e segue direto para a
produção.
