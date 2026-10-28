# Receita técnica

Os números e os comandos exatos da produção. O `PADRAO-VISUAL.md` diz o que é certo e o que é errado
no que se vê; aqui está como se faz, com os valores medidos nesta ferramenta e as duas armadilhas que
já custaram render perdido.

Regra de ouro deste arquivo: **valor sem unidade não existe**. Se você precisou escolher um número na
hora, ele está faltando aqui, e o lugar de corrigir é aqui.

---

## 1. O formato de entrega

| propriedade | valor | quem garante |
|---|---|---|
| resolução | 1080 x 1920 | `montar.py` |
| painel de cima | 1080 x 956 | `painel.py` |
| face embaixo | 1080 x 964 | o recorte da etapa 1 |
| taxa de quadros | 30 fps constante | `montar.py` |
| codec de vídeo | H.264, perfil High, nível 4.1 | `montar.py` |
| formato de pixel | yuv420p, faixa de TV | `montar.py` |
| SAR / DAR | 1:1 e 9:16 | `setsar=1` no filtro |
| início rápido | `+faststart`, o índice no começo do arquivo | `montar.py` |
| áudio | AAC 192 kbps, 48 kHz, o áudio da face | `montar.py` |
| duração alvo | a faixa está em `skills/planejar/SKILL.md`, "A duração do corte" | o planejamento, não a montagem |

O `montar.py` confere tudo isso com o ffprobe no fim e imprime o resultado. Se ele disser REPROVADO,
o arquivo não vai para lugar nenhum.

Detalhe que parece detalhe e não é: **faixa de cor**. Quadro vindo de PNG nasce em faixa cheia, e se
ela vazar para o MP4 o arquivo sai marcado como `yuvj420p`. Alguns players mostram isso com preto
lavado e cor estourada. Por isso o painel já sai convertido com `scale=in_range=full:out_range=tv` e
a montagem fecha com `format=yuv420p` e as marcas `bt709`.

---

## 2. Etapa 1, a face

### 2.1 Achar a caixa

```
flow-reels produzir/enquadrar amostrar \
  --video projetos/meu-video/materiais-de-trabalho/fonte/bruto.mp4 \
  --saida projetos/meu-video/materiais-de-trabalho/corte-01/contato.png --n 9 --colunas 3
```

Sai uma folha de contato com grade de oitavos e uma cruz no centro. **Olhe a folha** e escreva a
caixa em pixels do vídeo original, no formato `x:y:largura:altura`.

Três regras da caixa:

1. a proporção é a do destino, 1080 por 964, ou seja `largura = altura x 1,1203`;
2. os olhos ficam perto do terço de cima da caixa, com ar acima da cabeça, nunca com a testa colada
   na borda;
3. a largura da caixa não fica abaixo de 1080 px, senão a imagem estica e perde nitidez. Se o bruto é
   1920 x 1080, a maior caixa possível é 1210 x 1080, e ela cabe.

### 2.2 Conferir a caixa

```
flow-reels produzir/enquadrar validar \
  --video projetos/meu-video/materiais-de-trabalho/fonte/bruto.mp4 --caixa 560:0:1210:1080 \
  --saida projetos/meu-video/materiais-de-trabalho/corte-01/contato-recorte.png --inicio 12.4 --fim 58.2
```

Sai a folha já recortada e escalada para 1080 x 964, nos instantes do corte. Reprovado se em qualquer
amostra o queixo saiu, o topo da cabeça saiu, a pessoa andou para fora, ou sobrou teto vazio. O
script termina imprimindo o comando de recorte pronto para copiar.

### 2.3 Recortar

Os comandos abaixo usam nome curto porque rodam **de dentro da pasta de trabalho do corte**,
`projetos/<video>/materiais-de-trabalho/corte-NN/`. É lá que nascem a face, os trechos, a lista do
concat e tudo o mais que não é a entrega. Na pasta `corte-NN/` só entra o MP4 final.

Um trecho só:

```
ffmpeg -y -ss 12.4 -to 19.8 -i bruto.mp4 \
  -vf "crop=1210:1080:560:0,scale=1080:964,setsar=1,fps=30" \
  -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 face.mp4
```

Corte costurado de vários trechos: um comando desses por trecho, com os mesmos parâmetros, e depois a
costura sem recodificar.

```
ffmpeg -y -ss 12.4 -to 19.8 -i bruto.mp4 -vf "crop=...,scale=1080:964,setsar=1,fps=30" ... trecho-1.mp4
ffmpeg -y -ss 51.0 -to 58.2 -i bruto.mp4 -vf "crop=...,scale=1080:964,setsar=1,fps=30" ... trecho-2.mp4

# lista.txt
file 'trecho-1.mp4'
file 'trecho-2.mp4'

ffmpeg -y -f concat -safe 0 -i lista.txt -c copy face.mp4
```

O `-c copy` só funciona porque os trechos saíram com parâmetros idênticos. Se o ffmpeg reclamar de
fluxo incompatível, troque por `-c:v libx264 -crf 16 -c:a aac -b:a 192k` e aceite a recodificação.

**O deslocamento de cada trecho.** Depois da costura, o trecho 1 começa em 0 e o trecho 2 começa na
duração do trecho 1. Esses são os números que vão para o `--segmento` do `legenda.py`. Meça com o
ffprobe em vez de calcular na mão, porque o corte cai no quadro mais próximo:

```
ffprobe -v error -show_entries format=duration -of csv=p=0 trecho-1.mp4
```

---

## 3. Etapa 2, o painel

### 3.1 O contrato da página

O `painel.html` expõe três coisas, e o detalhe está em `componentes/REGISTRO.md` seção 4:

```js
window.DURACAO = 28.4;    // duração do painel em segundos
window.PRONTO  = false;   // vira true quando fonte e imagem carregaram
window.render  = function (t) { /* desenha o estado do mundo no segundo t */ };
```

`render(t)` é pura: chamada duas vezes com o mesmo `t`, dá o mesmo pixel. Nada de `setTimeout`, nada
de `requestAnimationFrame`, nada de `transition` ou `@keyframes` de CSS. O renderizador captura um
quadro por vez e transição de CSS não roda entre capturas: o painel sairia parado.

### 3.2 Renderizar

```
flow-reels produzir/painel \
  --painel projetos/meu-video/materiais-de-trabalho/corte-01/painel.html \
  --saida  projetos/meu-video/materiais-de-trabalho/corte-01/painel.mp4
```

Conferir um instante antes de gastar o render inteiro:

```
flow-reels produzir/painel \
  --painel projetos/meu-video/materiais-de-trabalho/corte-01/painel.html \
  --saida  projetos/meu-video/materiais-de-trabalho/corte-01/quadro-03.png --so-quadro 3.0
```

O script sobe um servidor local que serve, nesta ordem, a pasta do painel, a raiz do pacote e a pasta
`componentes`. É por isso que o painel pede `base.css`, `base.js` e `card.html` sem caminho nenhum.
Antes de abrir a página, ele injeta `window.TOKENS` com o conteúdo de `marca/tokens.json` e
`window.RAIZ` com `/`, e é assim que a marca entra sem ninguém escolher cor dentro do painel.

### 3.3 Os 12 quadros por segundo

O painel é autorado a 12 quadros por segundo e segurado em 30 no container, com cada quadro autorado
repetido para preencher. Movimento a 12 lê como decidido; a 30 lê como interpolação de ferramenta. E
render a 12 custa 40% dos quadros.

Os tempos do movimento caem quase todos em quadro exato a 12 fps:

| evento | duração | em quadros a 12 fps |
|---|---|---|
| chegada | 800 ms | 9,6, arredonde para 10 quadros (833 ms) |
| atraso entre irmãos | 200 ms | 2 quadros |
| re-fluxo | 667 ms | 8 quadros |
| wipe de saída | 167 ms | 2 quadros |

---

## 4. Etapa 3, a legenda

### 4.1 O estilo, campo a campo

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

| campo | valor | por quê |
|---|---|---|
| Fontsize | 116 | testado sobre vídeo. Menor perde no feed, maior estoura a largura |
| PrimaryColour | a cor escura da marca | o preenchimento. `#16151A` vira `&H001A1516`, porque em ASS a ordem é AABBGGRR |
| OutlineColour | `&H00FFFFFF` | branco puro, sempre. É ele que faz a legenda sobreviver em qualquer cena |
| BackColour | `&H64000000` | a sombra, preta com cerca de 60% de transparência |
| BorderStyle | 1 | contorno mais sombra. Nunca 3, que é a caixa opaca atrás do texto |
| Outline | 5 | a espessura do contorno branco |
| Shadow | 1 | um, não três |
| Bold | 0 | o arquivo já é a instância negrito. Ligar aqui engorda de novo e borra |
| Alignment | 5 | centro na horizontal e na vertical, o que põe a linha em cima da costura |
| MarginL / MarginR | 56 / 56 | a mesma margem lateral do painel |
| MarginV | 0 | com Alignment 5 a margem vertical não deve empurrar nada |
| WrapStyle | 2 | desliga a quebra automática, para o erro aparecer em vez de virar duas linhas |

### 4.2 Gerar

```
flow-reels produzir/legenda \
  --palavras projetos/meu-video/materiais-de-trabalho/transcricao/palavras.json \
  --segmento 12.4:19.8:0 --segmento 51.0:58.2:7.4 \
  --arquivo-fonte marca/fontes/Quicksand-Bold.ttf \
  --saida projetos/meu-video/materiais-de-trabalho/corte-01/legenda.ass
```

Cada `--segmento` é `entrada:saida:deslocamento`: os dois primeiros na linha do tempo do vídeo
original, o terceiro é onde aquele trecho começa dentro do corte montado. São os mesmos números do
recorte da face, e é assim que a legenda acompanha a costura.

O que o gerador faz sozinho:

- **mede a largura de verdade** de cada grupo somando o avanço de cada glifo do arquivo de fonte, em
  vez de chutar por contagem de caractere. Sem `--arquivo-fonte` ele cai numa estimativa conservadora;
- **divide por equilíbrio, não por enchimento.** Ele testa as divisões possíveis de cada trecho de
  fala e fica com a de menor custo. É o que evita a linha cheia seguida de uma palavra órfã;
- **nunca deixa palavra de ligação no fim do grupo** (o, a, de, do, da, e, que, em, no, na, com, por,
  para, pra, pro, se, não, e as parentes). A pessoa lê "de" e fica esperando o resto;
- **fecha o grupo na pontuação e no silêncio** maior que 450 ms;
- **um evento por grupo.** O grupo aparece inteiro e some inteiro. Palavra pintando uma a uma em
  116 px vira tremor;
- **teto de 16 caracteres por grupo**, que é o que cabe em 968 px com Quicksand negrito a 116. Fonte
  diferente muda esse número: o gerador mede e quebra antes de vazar de qualquer jeito.

### 4.3 Armadilha 1, fonte variável sai magra

O libass, que é o que o ffmpeg usa para queimar, **ignora o eixo de peso de uma fonte variável** e
renderiza na instância padrão dela. O Quicksand do Google é variável e o padrão dele é Light 300,
então a legenda sairia fina e sumiria sobre imagem clara.

A correção é gerar a instância estática antes de usar:

```
python -c "from fontTools.ttLib import TTFont; from fontTools.varLib import instancer; \
f = TTFont('marca/fontes/Quicksand.ttf'); \
e = instancer.instantiateVariableFont(f, {'wght': 700}, updateFontNames=True); \
e.save('marca/fontes/Quicksand-Bold.ttf')"
```

O `updateFontNames=True` é obrigatório: sem ele o arquivo continua se chamando "Quicksand Light" por
dentro, e o queimador procura pelo nome. **Qualquer fonte que o usuário trouxer no onboarding passa
por essa conversão**, e o `marca/tokens.json` guarda o campo `variavel: false` no que já foi tratado.

Como saber se uma fonte é variável:

```
python -c "from fontTools.ttLib import TTFont; f=TTFont('arquivo.ttf'); print('variavel' if 'fvar' in f else 'estatica')"
```

---

## 5. Etapa 4, a montagem

```
flow-reels produzir/montar \
  --painel  projetos/meu-video/materiais-de-trabalho/corte-01/painel.mp4 \
  --face    projetos/meu-video/materiais-de-trabalho/corte-01/face.mp4 \
  --legenda projetos/meu-video/materiais-de-trabalho/corte-01/legenda.ass \
  --fontes  marca/fontes \
  --saida   projetos/meu-video/corte-01/corte-01.mp4
```

O que ele roda por dentro, com o processo já dentro da pasta da legenda:

```
ffmpeg -y -i painel.mp4 -i face.mp4 -filter_complex \
 "[0:v]scale=1080:956:out_range=tv,setsar=1,setrange=tv[cima];\
  [1:v]scale=1080:964:out_range=tv,setsar=1,setrange=tv[baixo];\
  [cima][baixo]vstack=inputs=2:shortest=1[empilhado];\
  [empilhado]subtitles=legenda.ass:fontsdir=../../../../marca/fontes,format=yuv420p[final]" \
 -map "[final]" -map 1:a:0 -c:a aac -b:a 192k -ar 48000 \
 -r 30 -c:v libx264 -profile:v high -level 4.1 -preset medium -crf 18 \
 -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
 -movflags +faststart -shortest ../../corte-01/corte-01.mp4
```

Conte os `..` com calma: o processo está em `projetos/<video>/materiais-de-trabalho/corte-01/`,
então a raiz do pacote fica quatro níveis acima e a pasta de entrega do corte fica dois acima e um
ao lado. O `montar.py` monta esses caminhos sozinho, e é por isso que o comando na mão é o último
recurso.

Para conferir enquadramento sem esperar a legenda, existe `--sem-legenda`.

### 5.1 Armadilha 2, caminho absoluto quebra o filtro no Windows

Dentro de um filtro do ffmpeg, dois pontos separam opções. O `C:` de um caminho do Windows é lido
como esse separador e o comando morre assim:

```
[AVFilterGraph @ 000001...] No option name near 'C:/Users/voce/fabrica-de-cortes/marca/fontes'
[AVFilterGraph @ 000001...] Error parsing a filter description around: ...
Error initializing complex filters.
Invalid argument
```

**A regra do pacote: no `subtitles` e no `fontsdir`, caminho sempre relativo**, com o processo rodando
dentro da pasta certa. O `montar.py` já faz o `cd` sozinho, monta o caminho relativo e troca a barra
invertida por barra normal. Quando a pasta de fontes está em outro disco, e aí caminho relativo não
existe, ele copia as fontes para uma pasta ao lado da legenda e usa ela.

Se você chamar o ffmpeg na mão, faça o mesmo: entre na pasta da legenda antes.

---

## 6. A física do movimento

A mesma tabela que o autor do painel usa, aqui em forma de conta. Os ajudantes `FC.chegada`,
`FC.escalonar`, `FC.refluxo` e `FC.wipe` já implementam tudo isto, e o painel não deve recalcular
curva na mão.

| evento | duração | curva | o que muda | o que NÃO muda |
|---|---|---|---|---|
| chegada de elemento | 800 ms | `cubic-bezier(0.33, 1, 0.68, 1)` | sobe 64 px no eixo Y até a posição final | opacidade entra cheia no primeiro quadro, escala fica em 1 |
| irmãos entrando | atraso de 200 ms entre um e o próximo | a mesma curva de chegada | cada um começa 200 ms depois do anterior | nada além do atraso |
| re-fluxo do layout | 667 ms | `cubic-bezier(0.73, 0.13, 0.24, 0.86)` | o grupo inteiro anda junto para as posições novas | ninguém escalona, todos partem e chegam no mesmo quadro |
| saída por corte | 0 ms | nenhuma | no quadro seguinte o elemento não está lá | |
| saída por wipe | 167 ms | linear | uma máscara varre o elemento em uma direção | |

Regras que vêm junto e que o quadro denuncia:

- **zero overshoot.** A curva desacelera e para. Não passa do ponto e volta.
- **não existe fade de entrada nem de saída.** Entrada é subida com opacidade cheia, saída é corte ou
  wipe. Fade é o que faz o painel parecer apresentação de slides.
- **um evento por frase falada** é o piso. Parado só vale como descanso proposital logo depois de um
  evento grande, e por no máximo 2 segundos.
- **nada de animação perpétua.** Girar, pulsar, flutuar e piscar sem fim não contam como evento. A
  única exceção é um valor que a fala está falando enquanto ele corre, como um cronômetro durante a
  frase que fala do tempo, e ele para quando a frase acaba.
- **zona quieta de 170 px na base do painel**, de y = 786 a y = 956. É por ali que a legenda passa.

---

## 7. Quanto tempo leva cada etapa

Medido nesta ferramenta, numa máquina comum de trabalho. Serve para você saber que não travou.

| etapa | medida | o que esperar |
|---|---|---|
| folha de contato da face | 1 a 3 s | 9 amostras |
| recorte da face | perto de 1x a duração do trecho | 40 s de fala levam algo como 30 s |
| render do painel | cerca de 5 quadros por segundo, ou 0,2 s por quadro | 10 s de painel dão 120 quadros e levaram 23 s. Um corte de 30 s leva de 1 a 2 minutos |
| geração da legenda | menos de 1 s | instantâneo, mesmo com transcrição grande |
| montagem com queima | cerca de 0,4 s por segundo de vídeo | 10 s de corte levaram 4 s. Um corte de 40 s leva de 15 a 20 s |
| conferência com ffprobe | menos de 1 s | |

O render do painel é a etapa longa, e é a única que vale acompanhar. Ele imprime o andamento a cada
segundo de material, com quanto falta.

---

## 8. Conferência antes de entregar

```
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,pix_fmt,profile,sample_aspect_ratio,display_aspect_ratio \
  -show_entries format=duration,size -of default=nw=1 corte-01.mp4
```

O `montar.py` já faz isso e imprime aprovado ou reprovado. O que ele checa: resolução 1080 x 1920,
SAR 1:1, `yuv420p`, 30 fps e o índice `moov` nos primeiros 4 KB do arquivo, que é o que prova o
faststart.

Depois do formato, ainda faltam os olhos. Extraia o segundo 0, o meio de cada frase, os dois lados de
cada corte de fala e o último quadro, e passe a lista de observação do `PADRAO-VISUAL.md` seção 8.

```
ffmpeg -y -ss 5.0 -i corte-01.mp4 -frames:v 1 quadro-05.png
ffmpeg -y -ss 5.0 -i corte-01.mp4 -frames:v 1 -vf "crop=1080:420:0:750" costura-05.png
```

O segundo comando é o zoom na faixa da costura, que é onde mora quase todo defeito de legenda.

---

## 9. Sintoma, causa, correção

| o que você vê | causa | correção |
|---|---|---|
| legenda fina, quase sem peso | fonte variável entregue ao queimador | gere a instância estática com o fontTools, seção 4.3 |
| `No option name near 'C:/...'` | caminho absoluto dentro do filtro | caminho relativo com `cd` na pasta certa, seção 5.1 |
| legenda com a fonte errada, tipo Arial | o nome em `Fontname` não bate com o nome interno do arquivo, ou a pasta de fontes não chegou | confira o `--fontes` e refaça a instância com `updateFontNames=True` |
| legenda em duas linhas | grupo maior que a largura útil com a quebra automática ligada | `WrapStyle: 2` e o gerador medindo a largura. Se aconteceu, o `--arquivo-fonte` não foi passado |
| preto lavado, cor estourada no player | faixa de cor cheia vazou do PNG para o MP4 | `scale=in_range=full:out_range=tv` no painel e `format=yuv420p` na montagem |
| painel completamente parado no vídeo | o movimento foi escrito em `transition` ou `@keyframes` de CSS | todo movimento é conta dentro de `render(t)` |
| painel pisca ou volta ao início no meio | `render(t)` não é pura, ou guarda estado entre chamadas | reescreva `render` para desenhar o instante, não a mudança |
| o corte termina antes da fala | painel mais curto que a face, e a montagem corta no mais curto | renderize o painel com a duração do corte, que é o que `window.DURACAO` diz |
| som fora de sincronia depois da costura | trechos recortados com parâmetros diferentes e juntados com `-c copy` | recodifique na costura, seção 2.3 |
| o navegador não abre no render | Chromium do Playwright não instalado | `python -m playwright install chromium` |
| legenda aparece antes ou depois da fala | deslocamento errado no `--segmento` | meça a duração de cada trecho com ffprobe, seção 2.3 |
