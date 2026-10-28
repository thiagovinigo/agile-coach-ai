# Padrão do reel narrado

A lei do que aparece na tela e de como soa. Quem monta o `tomadas.json` lê isto antes, e volta aqui
antes de dizer que terminou. Toda cor e toda fonte saem de `marca/tokens.json`; nenhum valor de cor é
escolhido no olho.

## 1. A forma

```
gancho      de 0 a 3 a 5 s    o momento REAL mais forte da filmagem, em largura cheia, com o cartão de
                              abertura por cima: pílula com o logo oficial e o título entrando palavra
                              por palavra, uma palavra na cor de destaque
corpo       até o fechamento  a filmagem em largura cheia, muda, com a voz dizendo o que acontece
                              enquanto acontece: empurrão lento e anel no que a voz nomeia, transições
                              de 0,30 a 0,42 s entre tomadas, crédito em toda tomada
fechamento  os últimos 5 a 8 s a última tomada desfocada por baixo; a caixa de comentário sobe, a
                              PALAVRA é digitada no instante em que a voz diz ela, o envio pulsa e o item
                              prometido voa para um balão de DM
```

1080 x 1920, 30 quadros por segundo, de 40 a 50 s.

## 2. A filmagem

- **A filmagem real é a heroína, em largura cheia, quase o reel inteiro.** Nunca encolhida num cartão
  pequeno com enfeite em volta. Filmagem 16:9 ocupa os 1080 px de largura; com `recorte` ela fica mais
  alta (4:5 ou 1:1 quando a ação está no centro), até 1320 px de altura.
- **Gente de verdade vale mais que gravação de tela.** Procure o keynote, o evento, as pessoas usando,
  os personagens do filme, antes de se contentar com tela. Tela entra como prova rápida, empurrada e
  recortada até encher a largura.
- **Tela quase branca nunca carrega um beat sozinha.** Empurre ou recorte até o que importa encher a
  largura. O `compor_narrado.py` mede a fração branca de cada tomada e avisa.
- **Filmagem real vale mais que demonstração redesenhada.** Se existe o filme da coisa funcionando, é ele
  que entra. Desenho não substitui prova.
- **O som da filmagem fica mudo**, e uma voz contínua carrega o que as pessoas do filme diriam. Exceção:
  quando **o som é o produto** (uma voz sintética, um recurso de áudio), o trecho toca com o som dele,
  pela `trilha` do `tomadas.json`, com 0,30 s de ar antes e depois.
- **Corte pela energia do áudio**, no meio de um silêncio (abaixo de -38 dB por 0,12 s ou mais), nunca
  num tempo de transcrição: `linha_do_tempo.py --energia`.
- **Crédito em toda tomada**, num chip pequeno ("Filme de lançamento · @marca"), fora da faixa da
  legenda. O chip fica logo abaixo da filmagem e sobe para o topo quando não há espaço embaixo.
- **Faixa promocional com prazo** (oferta, contagem regressiva) sai pelo `recorte`.
- **A fonte não pode acabar antes da tomada.** Tomada que pede mais segundos do que a fonte tem congela
  no último quadro; o compor avisa no plano e a conferência reprova trecho parado de mais de 1 s.

## 3. O movimento

- **Calmo.** Empurrão lento, anel se desenhando, transição suave. Nada de tremor de câmera, nada de
  objeto quicando, nada de animação perpétua.
- **O empurrão cai na palavra.** Ele começa 0,15 s antes da palavra que nomeia a coisa e leva de 0,6 a
  1,6 s, até no máximo 2,2 vezes o enquadramento da tomada. Toda tomada também tem um empurrão de fundo
  de 3% ao longo da duração, para nunca ficar parada.
- **O anel se desenha na palavra**, em 0,45 s, uma volta e pouco com o tremor de quem desenha à mão, na
  cor de destaque com um contorno escuro por baixo. **Um anel por vez**: o novo apaga o anterior, como
  o destaque do pacote, que marca uma coisa só.
- **Transição de 0,30 a 0,42 s**: `desfoque` (padrão), `zoom` (uma entra ampliando enquanto a outra
  chega) ou `corte`. Fora da faixa, o compor ajusta e avisa.
- **Resumo com prints reais em leque.** Numa batida de resumo ("três telas que você já usa"), os prints
  de verdade entram um sobre o outro, inclinados de leve, por cima da filmagem escurecida. São imagens
  reais, nunca cartões de texto.

## 4. Zonas reservadas

| zona | regra |
|---|---|
| y < 150 | nada importante: é onde a plataforma desenha a interface |
| x > 980 | nada importante: são os botões da direita |
| y > 1700 | nada importante: é a legenda do post |
| y de 1480 a 1660 | a faixa da legenda. A filmagem termina antes dela |

As folhas de contato da conferência desenham essas linhas por cima de cada quadro.

## 5. O texto na tela

**Quase nenhum além da legenda.** Um título desenhado na abertura, o crédito, a PALAVRA e o nome do item
no fechamento. Nada de card de citação, card de manchete, rótulo para ler, pilha de texto.

> **A colagem de texto está rejeitada.** Um estilo em camadas, com recortes de pessoas, cards de
> manchete, citações com marca-texto e rótulos empilhados foi tentado neste formato e reprovado: texto
> demais para ler no tempo da tela, e o reel deixa de ser a filmagem. Não construa a partir dele. O que
> se aproveita dele é só a caça a material real com fonte anotada.

## 6. O cartão de abertura

`modelos/abertura.html`, renderizado com fundo transparente por cima da filmagem:

- **pílula** no topo (y 190), com o logo oficial do acervo `componentes/logos/` e um kicker curto em
  caixa alta ("NOVIDADE", "LANÇAMENTO"), já em cena no quadro 0;
- **título** grande, na fonte de título da marca, cada palavra entrando no instante em que a voz diz
  ela, subindo 40 px em 0,28 s; **uma palavra** na cor de destaque. A placa atrás do título cresce
  linha a linha;
- sai num wipe de 167 ms quando a frase do gancho termina (`abertura.ate`), e a legenda assume.

O título ocupa de y 190 a uns 650. Ponha o alvo do empurrão do gancho abaixo disso, ou desça a
filmagem com `centro_y`.

**Nunca desenhe um logo.** Faltou no acervo: `flow-reels componentes/baixar-logo <marca>`. Logo
colorido oficial (página de imprensa da marca) entra como PNG com `logo_monocromatico: false`.

## 7. O fechamento

`modelos/fechamento.html`, por cima da última tomada desfocada, escurecida e ainda andando devagar:

- a caixa de comentário sobe; a PALAVRA é digitada letra por letra a partir do instante em que a voz
  diz ela, na cor de destaque; o botão de envio acende e pulsa no envio;
- um balão de DM sobe e o item prometido voa da caixa até ele, em arco, e pousa com a borda na cor de
  destaque (o destaque passa da PALAVRA para o item);
- segura até o fim, com o fundo ainda em movimento.

## 8. A legenda

Desenhada quadro a quadro pelo `legenda_narrado.py`, com a fonte de legenda da marca:

- **uma linha**, 72 px, centrada em y 1572, entre x 110 e x 970, até 4 palavras por grupo;
- **palavra por palavra**: cada uma entra no instante em que a voz diz, subindo 14 px em 0,16 s; o
  grupo sai 0,12 s antes do próximo;
- a PALAVRA do comentário (e as de `legenda.destaques`) na cor de destaque, **uma por grupo**;
- texto na cor escura da marca com contorno claro; **placa clara atrás do grupo quando o fundo da
  faixa é escuro**, medido no próprio quadro (`--placa sempre` ou `nunca` força);
- **palavra de ligação nunca pendurada no fim do grupo**: de, da, do, das, dos, e, o, a, os, as, em,
  no, na, nos, nas, que, pra, pro, um, uma, com, por, se (e para, ao, pelo, pela, ou, nem). Ela desce
  para o grupo seguinte;
- quebra em pontuação e em pausa de mais de 0,45 s;
- começa depois que o título da abertura sai;
- **travessão é recusado**.

Esta legenda não é a do corte com rosto, que passa na costura entre painel e face com 116 px e grupo
inteiro de uma vez. Aqui não existe costura, e a palavra por palavra acompanha uma voz que não se vê.

## 9. O som

Os números estão em `MIXAGEM.md`. Em uma frase: voz na frente, leito baixo debaixo dela (perto de -23
dB, abaixando quando ela fala), efeitos baixos nos eventos da imagem, -14 LUFS na entrega.

## 10. O que se confere antes da revisão

O `conferir.py` mede; você olha. Sim ou não, sem "mais ou menos":

1. Formato: 1080 x 1920, 30 fps, H.264 yuv420p, SAR 1:1, AAC, faststart. (medido)
2. Volume: -14 LUFS, mais ou menos 0,5. (medido)
3. Nada parado por mais de 1 s. (medido)
4. Duração de 40 a 50 s. (medido, aviso)
5. Nas folhas: nada importante acima de y 150, à direita de x 980 ou abaixo de y 1700?
6. O anel está em volta da coisa que a voz diz naquele instante, e é um só?
7. O empurrão termina na coisa nomeada, e ela fica legível?
8. Toda tomada tem o crédito?
9. A legenda é uma linha só, sem palavra de ligação pendurada?
10. O título da abertura lê inteiro antes de sair, com uma palavra no destaque?
11. A PALAVRA aparece digitada no instante em que a voz diz ela?
12. Cada frase de `afirmacoes.md` confere com a tela?

Só depois disso a página de revisão sobe.
