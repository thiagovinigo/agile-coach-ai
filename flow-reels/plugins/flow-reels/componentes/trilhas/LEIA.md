# Trilhas de fundo

Esta pasta guarda as músicas que tocam por baixo da voz nos cortes. **O pacote não traz trilha
nenhuma**: diferente dos efeitos de `componentes/sons/`, que o próprio pacote calcula, música é obra
de alguém, e quem põe a faixa aqui é quem responde por ela. A pasta chega só com este arquivo.

O `audio.py` mistura a trilha sob a voz quando o `cenas.json` do corte pede (seção "Como pedir num
corte", abaixo). Sem pedido, o corte sai como sempre saiu: voz e efeitos.

## O que pode entrar

Só música que você pode usar em post de rede social, inclusive em conta de empresa e em conteúdo
patrocinado, sem pagar e sem pedir a ninguém. Na prática, duas fontes:

- **Pixabay Music** (pixabay.com/music). A licença do Pixabay libera o uso em vídeo de rede social,
  comercial ou não, sem crédito obrigatório. O que ela não libera é revender ou redistribuir a faixa
  sozinha, como arquivo de música. Leia a licença na página da faixa antes de baixar, porque ela
  pode mudar. Algumas faixas são registradas em sistemas de identificação de conteúdo (como o
  Content ID do YouTube) e podem gerar aviso de direito autoral mesmo com a licença em ordem: quando
  a página da faixa indicar isso, pule.
- **Free Music Archive** (freemusicarchive.org), **só faixas CC0**, que são domínio público. O FMA
  tem faixas em várias licenças Creative Commons, e as outras complicam: a NC proíbe uso comercial (e
  um reel que vende o seu trabalho é uso comercial), a ND proíbe obra derivada (cortar e repetir em
  loop já é derivar), e a BY obriga o crédito em todo post.

Nunca entra: faixa de disco ou de streaming (Spotify, YouTube Music, Apple Music), compilação "sem
direitos autorais" de canal de YouTube, música da biblioteca do Instagram ou do TikTok baixada de
outro vídeo (ela só vale dentro do app, e um vídeo que já chega com ela pode ser silenciado), nem
trilha feita por IA sem uma licença que diga com clareza que o uso comercial é seu.

Para cada faixa que entrar, uma linha no `CREDITOS.md` desta pasta (crie na primeira): o arquivo, o
título, o autor, o link da página da faixa, a licença e a data do download. Se um aviso de direito
autoral aparecer daqui a um ano, é essa linha que resolve.

## Que música funciona embaixo da voz

- **Instrumental.** Letra cantada disputa com a fala, e o ouvido tenta seguir as duas.
- **Energia constante.** Sem drop, sem pausa dramática, sem crescendo no meio: o ritmo do reel vem
  da imagem e dos efeitos, e uma virada da música no lugar errado brigaria com o corte.
- **Grave e médio, pouco agudo brilhante.** A voz vive entre 1 e 4 kHz; piano, pad, baixo e
  percussão leve deixam esse espaço livre. Sintetizador muito agudo e prato aberto o tempo todo, não.
- **Mais longa que o reel**, de preferência com 60 s ou mais. Mais curta, o `audio.py` repete em loop:
  tira o silêncio das pontas e cruza cada volta em 0,25 s, mas emenda de música nunca é tão boa quanto
  a música seguindo.

## Como nomear

Minúsculas, sem acento e sem espaço, com hífen: `<clima>-<instrumento>-<nn>.<extensão>`.

```
calma-piano-01.mp3
tensa-sintetizador-01.mp3
animada-percussao-02.wav
```

**Trilha é sempre pergunta.** Em todo vídeo, antes de produzir, o pacote pergunta se o corte leva trilha
sonora (sim ou não) e, se sim, qual. Sem o sim, o corte sai só com voz e efeitos.

O clima primeiro, porque é por ele que você procura a faixa do corte quando a pasta encher: listada em
ordem, ela já sai agrupada por clima. Quem escolhe a trilha é você, no `cenas.json`; nenhum script do
pacote escolhe por conta própria. Qualquer formato que o ffmpeg leia serve (mp3, wav, m4a, flac, ogg); prefira wav ou mp3 de 320 kbps, porque a trilha ainda vai
ser mixada e comprimida em AAC na entrega.

## Como pedir num corte

No `cenas.json` do corte, uma chave de topo, ao lado de `"cenas"`:

```json
"trilha": {
  "arquivo": "componentes/trilhas/calma-piano-01.mp3",
  "volume_db": -18,
  "ducking": true,
  "entra": 0.0,
  "fade_entrada": 0.6,
  "fade_saida": 1.2,
  "inicio_no_arquivo": 0.0
}
```

| campo | padrão | o que faz |
|---|---|---|
| `arquivo` | (obrigatório) | a faixa. Relativo à raiz do pacote (como acima), à pasta do corte, ou absoluto |
| `volume_db` | -18 | quanto a trilha fica abaixo do volume médio da voz, sem o ducking. É o nível dela antes de a voz começar e nas pausas longas |
| `ducking` | true | com a voz falando e nas pausas curtas, a trilha fica mais 6 dB abaixo. Ela só sobe numa pausa de 1,2 s ou mais, e desce de novo antes de a voz voltar. `false` desliga; um número é a profundidade em dB, de 0 a 24 |
| `entra` | 0 | o segundo do reel em que a trilha começa |
| `fade_entrada` | 0,6 | segundos de fade a partir do `entra` |
| `fade_saida` | 1,2 | segundos de fade até o fim do reel |
| `inicio_no_arquivo` | 0 | de que segundo da faixa ela começa a tocar, para pular uma introdução longa. O loop repete a partir daí |

`"trilha": "componentes/trilhas/calma-piano-01.mp3"` é o atalho para só o arquivo, com o resto no
padrão. `"trilha": false`, ou nenhuma chave, deixa o corte sem trilha.

O volume é sempre medido contra a voz, nunca em número solto, porque uma gravação chega a -24 LUFS e
outra a -10. Com o padrão, a trilha fica 24 dB abaixo da voz enquanto ela fala (18 do `volume_db`
e mais 6 do ducking), e num corte editado é esse o nível do reel inteiro, porque a fala editada não
tem pausa longa. É mais baixo que o reel de referência da 3.0, que tinha a trilha uns 18 dB abaixo
da voz com a voz falando: para chegar nele, `"volume_db": -12`. Abaixo de 12 dB com a voz falando
o `audio.py` avisa, porque ali a música começa a disputar a fala. O volume final do corte (-14 LUFS,
pico de -1 dBTP) continua sendo feito por cima da mistura inteira, com a trilha dentro.

O ducking decide pausa por pausa, com a fala inteira na mão. Pausa de menos de 1,2 s não mexe na
trilha: um fundo que sobe e desce a cada respiro bombeia, e é isso que um compressor comum faz. Numa
pausa mais longa, a trilha espera 0,25 s depois da última sílaba, sobe 6 dB em 0,5 s, fica lá em cima
e desce em 0,2 s, terminando a descida no instante em que a voz volta. Antes da primeira palavra
quem sobe a trilha é o fade de entrada, e depois da última quem desce é o de saída.

Na linha de comando, sem mexer no `cenas.json`:

```
flow-reels produzir/audio --projeto projetos/<video> --corte 01 --musica componentes/trilhas/calma-piano-01.mp3
flow-reels produzir/audio --projeto projetos/<video> --corte 01 --musica-db -14
flow-reels produzir/audio --projeto projetos/<video> --corte 01 --sem-trilha
```

`--musica` troca o arquivo (o resto vem do `cenas.json` ou do padrão), `--musica-db` troca o
`volume_db`, e `--sem-trilha` ignora a trilha do plano, para comparar o corte com e sem ela.

## Como conferir sem ouvir

O `audio.py` imprime o que mediu:

```
  trilha                 calma-piano-01.mp3 (cenas.json): fades de 0.6 s e 1.2 s
      pedido              18 dB abaixo da voz; com a voz falando, mais 6 dB (ducking)
      trilha x voz        sem ducking -18.1 dB  ·  voz falando -24.0 dB  ·  pausas curtas -24.6 dB em 17 quadro(s) de 100 ms
      pausas longas       nenhuma de 1.2 s ou mais: a trilha fica abaixada do primeiro ao último som da voz
      voz sobre a trilha  +25.0 dB com a voz falando (o ducking tirou 6.0 dB)
```

"voz sobre a trilha" é o número que importa: quanto a fala fica por cima da música enquanto alguém
fala. De 20 dB para cima, a fala está clara. "pausas curtas" é a trilha nas pausas em que o ducking
segurou, e deve sair perto do "voz falando". Quando alguma pausa soltou a trilha, a linha "pausas
longas" diz onde, e o nível dela lá em cima, que deve sair perto do `volume_db`:

```
      pausas longas       a trilha subiu em 3: antes da 1ª palavra (até 1.56 s), 13.92 a 15.87 s, 19.39 a 22.43 s; no alto, -17.6 dB
```
