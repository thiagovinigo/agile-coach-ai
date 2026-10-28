# O som do reel narrado

Quem faz é o `mixar.py`. Os números abaixo estão nele como constantes; mudar um número aqui sem mudar
lá (ou o contrário) é como os dois divergem.

## As camadas

| camada | de onde | nível |
|---|---|---|
| voz | `construcao/voz.wav` | inteira, sem compressor, na velocidade natural |
| som da filmagem | `construcao/som.wav`, só os trechos em que o som é o produto | nivelado com a voz (95% do volume dela nos trechos ativos) |
| leito | `marca/audio/leito.mp3` | -13 dB sob o título da abertura; -20 dB sob a voz, abaixando 30% quando ela fala, o que dá perto de -23 dB; -31 dB sob os trechos com som; some no último 1,5 s |
| efeitos | `marca/audio/sfx/<tipo>.mp3`, nos eventos de `construcao/eventos.json` | baixos, com passa-baixa, e 7 dB mais baixos sob os trechos com som |

O leito foi abaixado até ficar perto de -23 dB debaixo da voz de propósito: acima disso ele começa a
brigar com a fala no alto-falante do celular. As mudanças de nível são suavizadas em 0,25 s.

## Os efeitos

| tipo | quando a imagem pede | ganho (dB) | passa-baixa |
|---|---|---|---|
| `whoosh` | transição entre tomadas, entrada do fechamento (0,10 s antes) | -25 | 6000 Hz |
| `pop` | palavra do título entrando, carta assentando | -28 | 5000 Hz |
| `alternar` | pílula da abertura | -27 | 4500 Hz |
| `varredura` | anel se desenhando | -28 | 6000 Hz |
| `clique` | toque no botão de envio | -27 | 4500 Hz |
| `digitar` | a PALAVRA sendo digitada, cortado no fim da digitação | -27 | 5000 Hz |
| `enviar` | envio do comentário | -24 | 6000 Hz |
| `assentar` | item pousando na DM | -25 | 3500 Hz |

**No mínimo 0,22 s entre dois efeitos do mesmo tipo.** Efeito repetido em rajada vira ruído. O ganho
vale depois de normalizar o pico do arquivo em -1 dBFS, então trocar o arquivo não muda o nível.

Quem escreve os eventos é o `compor_narrado.py`, a partir do plano: cada transição, cada anel, cada
carta e cada passo do fechamento. Nenhum evento é escrito à mão.

## Leito e efeitos: de onde vêm

Gerados uma vez pela própria pessoa, com a chave dela, pelo `gerar_audio.py`, a partir dos pedidos de
`dados/sons.json` (música por `POST /v1/music`, efeitos por `POST /v1/sound-generation`). Ficam em
`marca/audio/` porque valem para todo reel narrado, de qualquer vídeo, como as fontes da marca.

O pacote não traz áudio pronto. Sem esses arquivos, o reel sai só com a voz, e o `mixar.py` diz
exatamente o que ficou de fora e como gerar.

## Volume de entrega

1. soma as camadas e limita o pico em 0,98;
2. mede o loudness integrado com o filtro `ebur128` do ffmpeg;
3. aplica **um ganho só** até -14 LUFS e um `alimiter` por cima;
4. mede o arquivo pronto e, se ficou a mais de 0,3 LU do alvo, corrige o ganho e refaz (até duas vezes).

Saída: AAC 192k estéreo a 48 kHz, vídeo copiado como veio (H.264 yuv420p, SAR 1:1), `+faststart`. A
conferência reprova fora de -14 mais ou menos 0,5.
