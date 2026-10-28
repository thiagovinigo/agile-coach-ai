# Flow Reels 3.0 (Fábrica de Cortes)

Transforma um vídeo longo em reels verticais prontos para Instagram, TikTok e Shorts, com a sua
identidade visual. Não é um cortador automático: ele lê a transcrição inteira, procura as ideias que
se sustentam sozinhas, mostra os ganchos para você aprovar antes de produzir qualquer coisa, e só então
monta o reel inteiro, cena a cena.

E, se você ainda não sabe o que gravar, ele pesquisa o que está em alta e entrega a pauta pronta, com
o roteiro no tamanho da sua fala.

## Os comandos

É um plugin do Claude Code. Cada etapa é uma skill, e você pode chamar pelo nome ou só dizer o que
quer: "quero fazer cortes desse vídeo" já chama a certa.

| comando | o que faz |
|---|---|
| `/flow-reels:fabrica` | a porta de entrada: do vídeo longo aos reels prontos, passando por todas as etapas abaixo |
| `/flow-reels:tendencias` | o que gravar: varre o seu nicho ou pesquisa um tema, e entrega a pauta com roteiro, fatos conferidos e kit de gravação |
| `/flow-reels:marca` | o onboarding da sua identidade: fonte, cores, logo, foto da capa. Roda uma vez |
| `/flow-reels:transcrever` | traz o vídeo (arquivo, YouTube ou Drive) e transcreve palavra a palavra |
| `/flow-reels:planejar` | levanta os ganchos, você aprova, e ele planeja cada reel |
| `/flow-reels:produzir` | monta o reel, confere com 13 gates automáticos e sobe a página de revisão |
| `/flow-reels:publicar` | publica ou agenda no Instagram e no YouTube, só com o seu sim |
| `/flow-reels:narrado` | o reel sem rosto: uma voz da ElevenLabs conta a novidade por cima de filmagem real |

## Instalar

O plugin mora numa pasta (o marketplace), e os seus vídeos, a sua marca e as suas chaves moram em
outra, a **pasta de trabalho**, onde você abre o Claude Code.

**Do zip (o jeito mais simples).** Descompacte, abra o Claude Code na pasta e aceite a confiança da
pasta. O `.claude/settings.json` que vem nela registra o marketplace e liga o `flow-reels` sozinho.
Essa mesma pasta já é a sua pasta de trabalho.

**De um repositório.** Em qualquer pasta de trabalho:

```
/plugin marketplace add <dono>/<repositorio-do-flow-reels>
/plugin install flow-reels@flow-reels
```

No app do Claude (aba Code), o botão **+** ao lado da caixa de mensagem tem **Plugins**, onde você
liga, desliga e atualiza.

Depois, uma vez por pasta de trabalho, peça "instala o flow reels" ou rode no terminal do Claude Code:

```
flow-reels instalar
```

Ele checa o que falta (ffmpeg, Python), cria o `.venv` com as bibliotecas, baixa o Chromium que
renderiza o reel e cria na sua pasta o `setup.json`, o `.env` (onde vão as chaves) e o `.gitignore`.
Não quebra: se faltar algo, ele diz o que é e como resolver.

### O que você precisa

- Claude Code (terminal, app de desktop ou extensão do VS Code)
- ffmpeg com legenda (no Mac, `brew install ffmpeg-full`) e Python 3.10 ou mais novo
- Uma conta na Replicate para transcrever rápido. Sem ela, a transcrição roda local, de graça e mais devagar
- Opcionais: Zernio para publicar daqui, ElevenLabs para o reel narrado, xAI para o X nas tendências

## O primeiro reel

```
quero fazer cortes desse vídeo: /Users/voce/videos/minha-aula.mp4
```

1. **A sua marca**, na primeira vez: fonte, cor de destaque, fundo claro ou escuro, logo e a foto que
   vai em toda capa. Se você tiver um manual de marca ou o print de uma peça sua, ele extrai dali. No
   fim, um painel de amostra para você aprovar.
2. **Transcrição**, palavra por palavra, com tempo.
3. **Ganchos.** Ele varre o vídeo inteiro e apresenta até cinco, cada um com o que quem assiste aprende
   ali. Você aprova quais viram reel.
4. **As escolhas do reel**, sempre suas: a velocidade da fala, a trilha (ou nenhuma), o estilo de
   produção e a linguagem visual do episódio (ele sugere três que combinam com o vídeo e não repetem
   os últimos reels).
5. **Produção.** O reel inteiro em cenas, com a legenda animada, o som e a capa, conferido por 13 gates
   automáticos antes de chegar até você.
6. **Revisão** numa página no navegador, onde você assiste e aprova ou pede mudança.
7. **Publicação**, se quiser, com o funil "comenta a palavra, recebe o link na DM". Nada sai sem o seu sim.

## O reel, cena a cena

Cada trecho do reel é uma cena, e cada cena tem um modo:

| modo | como fica |
|---|---|
| rosto + vidro | você em tela cheia, com cards de liquid glass entrando por cima |
| tela + bolha | a gravação de tela em destaque, com zoom guiado, e você numa bolha de vidro |
| **mundo** | a coisa de que você fala ocupa a tela (um editor, uma planilha, um app) e uma câmera calma passeia por ela; você entra como respiro, num card com a cabeça saindo pela borda |
| vidro líquido | a cena dentro de uma placa de vidro que inclina, gira e mergulha |
| tela cortada | o vídeo separado em camadas 3D, com texto atrás de você e profundidade de verdade |
| imagem cheia, manchete, lado a lado, lista, tipografia, painel + rosto | foto com câmera lenta, a notícia com o trecho marcado, a comparação com vencedor, os itens empilhando, a frase em letra grande, a tela dividida |

Por cima dos modos vêm as **linguagens do episódio** (vidro, terminal, cinema, recorte, sci-fi, anos 80,
mangá, profundidade 3D, editorial, turbo, calmo e manchete), cada uma com as suas peças, sons,
acabamento e momento-herói; os looks no vídeo (CRT, VHS, holograma, pontilhado...); efeitos disparados
pelas suas mãos e pelo seu rosto; frames 3D; transições e palavras animadas; e 15 famílias de efeitos
sonoros sintetizados pelo pacote, que nunca caem em cima da sílaba tônica.

Tudo roda na sua máquina e é gratuito: Python, FFmpeg, Chromium, GSAP, MediaPipe, Depth Anything e
BiRefNet. Nenhum código ou modelo de licença não comercial.

## Antes de gravar: tendências

```
o que está bombando no meu nicho essa semana?
o que tá em alta sobre agentes de IA para programar?
```

O `/flow-reels:tendencias` tem duas entradas. **Nicho**: varre Reddit, YouTube Brasil, GitHub,
Hacker News e Product Hunt atrás do que está subindo no nicho do seu `setup.json`. **Tema**: pesquisa
um assunto que você traz nos últimos 30 dias, em português primeiro e em inglês quando o português
vem fraco, com o que a comunidade pensa e onde a opinião racha. O Reddit funciona sem chave nenhuma,
com voto e comentários de verdade.

As duas passam pela mesma régua (sem fonte, sem número inventado, sem repetir o que você já gravou) e
cada pauta que você escolher vira uma pasta com o roteiro de 40 a 50 s no tamanho da sua fala, os
fatos com link, os prints da ferramenta, os logos e o texto do post.

## O reel narrado

```
narra esse lançamento: https://youtube.com/...  o assunto é a nova função de agenda
```

Para quando não tem você falando: o `/flow-reels:narrado` escreve o roteiro a partir da filmagem e da
fonte oficial, mostra antes de gastar crédito de voz, gera a voz na ElevenLabs e monta o reel com a
filmagem real em destaque, a abertura com o logo, os empurrões no que a voz nomeia e o fechamento
"comenta a palavra". Precisa de `ELEVENLABS_API_KEY` e `ELEVENLABS_VOICE_ID` no `.env`; a trilha e os
efeitos saem do pacote, de graça.

## Onde as coisas ficam

Na sua pasta de trabalho, só o que é seu:

```
minha-pasta/
├── setup.json      as suas preferências
├── .env            as suas chaves (nunca compartilhe)
├── marca/          a sua identidade: tokens.json, marca.md, fontes, logo e a foto da capa
├── projetos/       uma pasta por vídeo; cada corte-NN/ tem só o MP4 e a capa
├── pautas/         as buscas de tendências
└── componentes/    opcional: os logos, trilhas e imagens que você baixar, por cima dos do pacote
```

`marca/` é a única pasta insubstituível. Se você usa mais de uma máquina, é ela que vale copiar.

O código, as peças, os logos de 91 marcas, as trilhas livres, os sons e os modelos ficam no plugin, e
são atualizados com ele sem tocar na sua pasta.

## Rodar numa máquina remota

Dá para deixar o pacote trabalhando numa máquina remota até a revisão, quando o vídeo é longo ou o lote
é grande. A receita está em [instrucoes-de-nuvem.md](instrucoes-de-nuvem.md). A marca continua sendo
configurada na sua máquina, e publicar nunca roda sozinho.

## Refazer a marca

Apague o conteúdo de `marca/`, troque `"marca": true` para `false` no `setup.json` e peça para refazer
a marca. O onboarding roda de novo.
