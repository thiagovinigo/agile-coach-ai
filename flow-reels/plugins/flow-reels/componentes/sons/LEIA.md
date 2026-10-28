# Sons do pacote

Os efeitos desta pasta são **obra do próprio pacote**. Foram calculados, amostra por amostra,
pelo `gerar_sons.py` (só numpy): ruído filtrado, senoides que decaem e envelopes. Não há gravação,
banco de sons nem trecho de obra de terceiro aqui dentro, então não há licença de ninguém para
respeitar. São livres: use, altere e distribua junto com os seus cortes e dentro do pacote,
inclusive em conteúdo pago ou patrocinado, sem crédito obrigatório.

São 15 famílias: `whoosh`, `pop`, `tick`, `clique`, `subida`, `clarao`, `glitch`, `rebobina`, `impacto`, `estatica`, `energia`, `carimbo`, `bip`, `obturador`, `raio`. Cada uma tem o **base**, com o nome da família (`whoosh.wav`), e as
**variações** numeradas (`whoosh-1.wav`, `whoosh-2.wav`...): o mesmo desenho com outro timbre, outra
duração ou outra altura. O base das seis famílias da 3.0 é o mesmo arquivo de antes, bit a bit.

| arquivo | duração | pico verdadeiro | ponto forte | o som | pensado para |
|---|---|---|---|---|---|
| `whoosh.wav` | 0,45 s | -10,5 dBTP | 0,202 s | ruído numa banda que sobe e desce, da esquerda para a direita | transição (lâmina, chicote, desfoque, inclinada, mergulho, zoom-desfoque) |
| `whoosh-1.wav` | 0,30 s | -11,0 dBTP | 0,151 s | variação: curto e mais agudo, da direita para a esquerda | ↳ |
| `whoosh-2.wav` | 0,62 s | -11,7 dBTP | 0,283 s | variação: longo e grave, abre mais o estéreo | ↳ |
| `whoosh-3.wav` | 0,40 s | -11,5 dBTP | 0,151 s | variação: fio de ar mais definido no pico, da direita para a esquerda | ↳ |
| `whoosh-4.wav` | 0,52 s | -11,7 dBTP | 0,252 s | variação: médio e escuro, quase no centro | ↳ |
| `pop.wav` | 0,08 s | -7,2 dBTP | 0,005 s | bolha curta: tom que sobe de altura enquanto some | elemento que entra (card, número, selo) |
| `pop-1.wav` | 0,07 s | -7,3 dBTP | 0,005 s | variação: bolha menor, mais aguda | ↳ |
| `pop-2.wav` | 0,10 s | -8,0 dBTP | 0,006 s | variação: bolha maior, sobe mais | ↳ |
| `pop-3.wav` | 0,06 s | -5,8 dBTP | 0,005 s | variação: gota curta e clara | ↳ |
| `pop-4.wav` | 0,09 s | -6,8 dBTP | 0,005 s | variação: bolha redonda, sobe devagar | ↳ |
| `tick.wav` | 0,02 s | -1,3 dBTP | 0,001 s | estalo seco e claro | contador correndo, item de lista |
| `tick-1.wav` | 0,02 s | -1,3 dBTP | 0,002 s | variação: madeira mais grave | ↳ |
| `tick-2.wav` | 0,02 s | -1,4 dBTP | 0,001 s | variação: mais agudo | ↳ |
| `tick-3.wav` | 0,03 s | -2,1 dBTP | 0,002 s | variação: um pouco mais longo, com mais ressonância | ↳ |
| `tick-4.wav` | 0,02 s | -1,7 dBTP | 0,001 s | variação: agulha: curto, agudo e magro | ↳ |
| `clique.wav` | 0,04 s | -2,2 dBTP | 0,002 s | clique de interface: apertar e soltar | destaque que acende, marca, botão |
| `clique-1.wav` | 0,04 s | -2,2 dBTP | 0,002 s | variação: um pouco mais grave, soltar mais rápido | ↳ |
| `clique-2.wav` | 0,04 s | -2,4 dBTP | 0,002 s | variação: mais agudo, soltar mais fraco | ↳ |
| `clique-3.wav` | 0,04 s | -2,2 dBTP | 0,002 s | variação: botão grande, mais grave | ↳ |
| `clique-4.wav` | 0,04 s | -3,1 dBTP | 0,002 s | variação: tecla pequena e clara | ↳ |
| `subida.wav` | 0,50 s | -11,4 dBTP | 0,470 s | riser: ar abrindo para o agudo e um acorde baixo subindo uma quarta | o instante antes de uma revelação; termina em cima do evento |
| `subida-1.wav` | 0,40 s | -11,1 dBTP | 0,368 s | variação: mais curto, sobe uma quinta | ↳ |
| `subida-2.wav` | 0,65 s | -11,0 dBTP | 0,605 s | variação: mais longo e mais grave | ↳ |
| `subida-3.wav` | 0,55 s | -11,3 dBTP | 0,520 s | variação: mais ar, sobe uma terça | ↳ |
| `subida-4.wav` | 0,45 s | -11,5 dBTP | 0,413 s | variação: mais acorde e mais brilho no fim | ↳ |
| `clarao.wav` | 0,35 s | -6,4 dBTP | 0,008 s | impacto suave: corpo grave curto, sopro médio e brilho de ar | a transição clarão |
| `clarao-1.wav` | 0,30 s | -8,0 dBTP | 0,008 s | variação: mais curto, corpo mais alto | ↳ |
| `clarao-2.wav` | 0,45 s | -7,1 dBTP | 0,014 s | variação: mais grave, com mais sala | ↳ |
| `clarao-3.wav` | 0,32 s | -6,4 dBTP | 0,013 s | variação: mais brilho de ar | ↳ |
| `clarao-4.wav` | 0,40 s | -7,8 dBTP | 0,010 s | variação: sopro mais escuro, mais corpo | ↳ |
| `glitch.wav` | 0,24 s | -9,6 dBTP | 0,016 s | estalos digitais: bits esmagados, tom quadrado que salta e gagueira | transição glitch, palavra decodifica/pixel, erro, virada de opinião |
| `glitch-1.wav` | 0,18 s | -6,9 dBTP | 0,009 s | variação: curto e mais picado | ↳ |
| `glitch-2.wav` | 0,30 s | -6,9 dBTP | 0,025 s | variação: mais longo, bits mais grossos | ↳ |
| `glitch-3.wav` | 0,22 s | -9,0 dBTP | 0,014 s | variação: poucos grãos, mais agudo | ↳ |
| `rebobina.wav` | 0,60 s | -9,6 dBTP | 0,552 s | fita acelerando com wow e flutter, chiado que abre e a trava seca no fim | transição vhs, volta no tempo, "pera, volta"; termina em cima do corte |
| `rebobina-1.wav` | 0,45 s | -7,1 dBTP | 0,415 s | variação: rebobinada curta | ↳ |
| `rebobina-2.wav` | 0,75 s | -8,5 dBTP | 0,690 s | variação: mais longa, mais wow | ↳ |
| `rebobina-3.wav` | 0,55 s | -9,1 dBTP | 0,506 s | variação: mais chiado, trava mais leve | ↳ |
| `impacto.wav` | 0,55 s | -11,8 dBTP | 0,010 s | hit grave curto: senoide que cai saturada, soco abafado e sala pequena | momento-herói, número grande, revelação, palavra brutal (só peso 3) |
| `impacto-1.wav` | 0,45 s | -10,4 dBTP | 0,008 s | variação: mais curto e mais seco | ↳ |
| `impacto-2.wav` | 0,70 s | -12,0 dBTP | 0,016 s | variação: mais grave e mais longo | ↳ |
| `impacto-3.wav` | 0,50 s | -10,1 dBTP | 0,007 s | variação: mais soco, mais saturado | ↳ |
| `estatica.wav` | 0,50 s | -9,6 dBTP | 0,019 s | chiado de TV que liga e desliga, com o tum da rede e o zíper | look crt/vhs ligando, moldura-crt, transição vhs/pixels, liga/desliga de tela |
| `estatica-1.wav` | 0,35 s | -11,7 dBTP | 0,062 s | variação: liga e desliga curto | ↳ |
| `estatica-2.wav` | 0,70 s | -10,3 dBTP | 0,010 s | variação: falhando: apaga e volta duas vezes | ↳ |
| `estatica-3.wav` | 0,45 s | -12,4 dBTP | 0,015 s | variação: abafado, como rádio | ↳ |
| `energia.wav` | 0,90 s | -11,8 dBTP | 0,845 s | zumbido que cresce: tom que sobe, filtro que abre, tremolo que acelera | mãos (energia, aura, feixe, raio), carga antes do herói; termina no evento |
| `energia-1.wav` | 0,70 s | -12,8 dBTP | 0,665 s | variação: carga curta | ↳ |
| `energia-2.wav` | 1,10 s | -12,4 dBTP | 1,056 s | variação: carga longa e grave | ↳ |
| `energia-3.wav` | 0,80 s | -12,7 dBTP | 0,756 s | variação: mais assobio, menos tremolo | ↳ |
| `carimbo.wav` | 0,14 s | -2,7 dBTP | 0,006 s | batida seca de borracha e madeira, com o segundo toque assentando | palavra carimbo/marcatexto, selo que bate, papel, recorte |
| `carimbo-1.wav` | 0,14 s | -3,5 dBTP | 0,006 s | variação: mais grave, borracha mais mole | ↳ |
| `carimbo-2.wav` | 0,14 s | -2,8 dBTP | 0,005 s | variação: madeira mais dura, mais papel | ↳ |
| `carimbo-3.wav` | 0,16 s | -3,4 dBTP | 0,005 s | variação: carimbo que assenta devagar | ↳ |
| `bip.wav` | 0,08 s | -18,6 dBTP | 0,023 s | bip de chip antigo: onda quadrada em 16 degraus | transição pixels, palavra pixel, contador digital, mira travando, terminal |
| `bip-1.wav` | 0,09 s | -18,8 dBTP | 0,019 s | variação: duas notas subindo | ↳ |
| `bip-2.wav` | 0,12 s | -16,0 dBTP | 0,027 s | variação: um bip mais longo e mais anasalado | ↳ |
| `bip-3.wav` | 0,09 s | -19,3 dBTP | 0,036 s | variação: arpejo descendo | ↳ |
| `obturador.wav` | 0,20 s | -1,6 dBTP | 0,004 s | clique de câmera: o estalo que abre, a mola e o estalo que fecha | polaroid, foto, flash branco, print entrando, congela + recorte |
| `obturador-1.wav` | 0,16 s | -3,4 dBTP | 0,004 s | variação: câmera pequena, rápida | ↳ |
| `obturador-2.wav` | 0,24 s | -4,4 dBTP | 0,005 s | variação: câmera grande, mola mais longa | ↳ |
| `obturador-3.wav` | 0,20 s | -2,2 dBTP | 0,005 s | variação: os dois estalos quase iguais | ↳ |
| `raio.wav` | 0,65 s | -4,8 dBTP | 0,007 s | estalo elétrico: craque, arco que zumbe e crepitação | mãos raio/faíscas, palavra neon acendendo, curto-circuito |
| `raio-1.wav` | 0,50 s | -4,4 dBTP | 0,007 s | variação: curto, mais crepitação | ↳ |
| `raio-2.wav` | 0,80 s | -6,3 dBTP | 0,013 s | variação: arco mais grave e mais longo | ↳ |
| `raio-3.wav` | 0,60 s | -5,7 dBTP | 0,027 s | variação: faísca mais aguda | ↳ |

**Ponto forte** é o instante em que o som é mais forte, contado do começo do arquivo. O `audio.py`
põe esse instante em cima do tempo do evento: o whoosh começa uns 0,2 s antes da transição e passa
por ela no auge; a subida, a energia e a rebobinada terminam em cima do que anunciam.

## Como o `audio.py` usa a família

O evento pede a família (`"som": "whoosh"`) e o `audio.py` escolhe o arquivo: o base ou uma das
variações, por um sorteio fixo (o hash do instante e do alvo do evento), nunca o mesmo arquivo em
dois eventos seguidos da mesma família. O mesmo corte sai sempre com os mesmos arquivos. Quem quer
um arquivo exato pede pelo nome dele (`"som": "whoosh-2"`), e aí não há sorteio. O contrato inteiro
está em `skills/produzir/motor/docs-4/variedade-e-som.md`.

## Formato

48 kHz, 16 bits, estéreo. Pico verdadeiro de no máximo -1 dBTP, sem componente contínua, com fade
nas duas pontas (a primeira e a última amostra são zero, então nada estala ao entrar ou sair). Todos
têm o mesmo volume de curto prazo, -18 LUFS numa janela de 100 ms, para soarem parelhos quando
ouvidos soltos (o pico verdadeiro manda primeiro: o som muito seco fica um pouco abaixo). O volume
dentro do corte é decidido pelo `audio.py`, que mede a voz antes e põe cada efeito abaixo dela
(`--efeitos-db`, padrão -20 dB).

## Como refazer

```
flow-reels produzir/gerar_sons
flow-reels produzir/gerar_sons --so glitch,raio
```

Esta pasta foi gerada em 07/10/2026 com a semente 7. A mesma semente, no mesmo numpy, gera os mesmos
arquivos, bit a bit. Para outro grão de ruído do mesmo desenho, passe outra semente: `--semente 8`.
Para mudar o desenho (duração, timbre, envelope), o lugar é a função `som_<nome>` e a lista `SONS`
do `gerar_sons.py` (os parâmetros de cada variação), e a conferência no fim do script diz se o
resultado ainda está limpo e se cada variação continua diferente do base.

## Trocar um som pelo seu

Ponha o seu arquivo nesta pasta com o mesmo nome (`whoosh.wav`, `whoosh-3.wav`). O `audio.py`
acha sozinho o ponto forte de qualquer som e o volume dele, e uma variação a mais (`whoosh-5.wav`)
entra no sorteio da família sem mudar nada no código. Só lembre que rodar o `gerar_sons.py` de novo
grava por cima: guarde uma cópia do seu, e use som que você tem direito de usar.
