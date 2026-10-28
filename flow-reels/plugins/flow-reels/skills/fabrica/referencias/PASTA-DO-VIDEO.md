# A pasta do vídeo

Este arquivo é a **única definição da árvore** de `projetos/<video>/`. Skill que precisar dizer onde
um arquivo mora aponta para cá em vez de repetir o caminho, porque caminho repetido é caminho que
diverge. Se alguma skill discordar deste arquivo, quem está certo é este arquivo.

## A regra, em uma frase

**Quem abre a pasta do vídeo vê o que interessa, e o resto fica debaixo de um teto só.**

O que interessa para a pessoa: os cortes prontos, a transcrição legível, os ganchos levantados e a
página onde ela aprova. Todo o resto é material de trabalho: prova, plano, arquivo intermediário,
render de etapa, quadro de conferência, resposta crua de API. Nada disso se joga fora, porque é o
que permite refazer só um pedaço, mas nada disso aparece na primeira tela.

## A árvore

```
projetos/<video>/
├── corte-01/
│   ├── corte-01.mp4              a entrega
│   └── corte-01-capa.jpg         a capa do reel (capa.py), que sobe junto com o mp4
├── corte-02/
│   └── corte-02.mp4
├── revisao/
│   ├── revisao.html              a página onde a pessoa assiste e aprova
│   └── revisao.json              os textos daquela revisão
├── transcricao.md                a fala legível, com marca de tempo
├── GANCHOS.md                    o pool de ganchos, com os descartados e o motivo
└── materiais-de-trabalho/
    ├── INVENTARIO.md             as coisas concretas do vídeo, com a rota decidida de cada uma
    ├── inventario/               os quadros da fonte olhados antes de decidir rota
    ├── fonte/                    o vídeo de origem, e a gravação de tela quando houver
    ├── transcricao/
    │   ├── palavras.json         a fala palavra a palavra, com tempo
    │   ├── audio16k.wav          o áudio mono em 16 kHz, que valida os pontos de corte
    │   └── bruto-replicate.json  a resposta crua da transcrição (ou bruto-local.json)
    ├── corte-01/
    │   ├── brief.md              o plano do corte
    │   ├── beats.yaml            o plano do painel
    │   ├── contato.png           a folha de amostras da face
    │   ├── contato-recorte.png   a folha do recorte, já conferida com os olhos
    │   ├── face.mp4              1080 x 964, a fala já costurada
    │   ├── painel.html           o mundo autorado para este corte
    │   ├── painel.mp4            1080 x 956, o render do painel
    │   ├── legenda.ass           a legenda no padrão do pacote
    │   ├── tela/                 os quadros da gravação de tela, quando algum beat pede
    │   └── quadros/              os quadros extraídos do MP4 final, para conferência
    ├── corte-02/
    ├── publicacao/               o payload de cada post, o postId e o automationId do funil
    └── logs/                     relatório de subagente e saída de script que valeu guardar
```

A pasta `publicacao/` só nasce se a pessoa aceitar a etapa opcional de publicar. Vídeo que parou no
MP4 não tem essa pasta, e isso é o normal.

## Por que cada coisa está onde está

| decisão | o motivo |
|---|---|
| a pasta do corte tem só o MP4 | era a reclamação: dez arquivos na pasta e só um era a entrega. Quem abre `corte-02/` quer o `corte-02.mp4` |
| `transcricao.md` fica à vista | é o único dos três arquivos da transcrição que uma pessoa abre para ler |
| `palavras.json` e `audio16k.wav` ficam escondidos | são dados de máquina. Ninguém lê JSON de tempo por palavra por prazer |
| `GANCHOS.md` fica à vista | é o histórico do que já foi usado daquele vídeo, e é o que a pessoa consulta antes de pedir mais cortes |
| `INVENTARIO.md` fica escondido | é decisão de produção, não de conteúdo. Ele é do vídeo inteiro e é lido por todo corte, então mora um nível acima das pastas de corte |
| a resposta crua da API fica guardada | ela já foi paga. Reprocessar com `--reusar` custa zero, transcrever de novo custa de novo |
| nada de `index.html` na raiz | o servidor da revisão redireciona sozinho. Arquivo de servidor não mora na pasta do vídeo |

## O que não muda de lugar, e por quê

O **MP4 de entrega continua em `corte-NN/corte-NN.mp4`**. A página de revisão aponta para ele em
caminho relativo, `../corte-NN/corte-NN.mp4`, com o servidor subindo na pasta do vídeo. Mexer nisso
quebra o player da revisão sem quebrar nada visível antes, que é o pior tipo de defeito.

## Projeto feito antes desta árvore

Nada quebra sozinho. Quem procura `palavras.json`, `audio16k.wav` ou `brief.md` procura primeiro no
lugar de hoje e depois no lugar antigo, a raiz da pasta do vídeo. Isso vale para o `legenda.py`, o
`energia_audio.py`, o `nova-revisao.py` e as funções `achar_palavras()` e `achar_audio()` do
`normalizar.py`.

Para arrumar de vez uma pasta antiga:

```
flow-reels fabrica/arrumar_pasta projetos/<video>
```

Ele mostra o que pretende mover e só move com `--fazer`. Ele nunca move o MP4 de entrega e nunca
apaga nada.

## Quem escreve onde, durante um lote em paralelo

| caminho | quem escreve |
|---|---|
| `corte-NN/` e `materiais-de-trabalho/corte-NN/` | o subagente daquele corte, e só ele |
| `materiais-de-trabalho/transcricao/`, `materiais-de-trabalho/fonte/` | ninguém durante a produção, só leitura |
| `transcricao.md`, `GANCHOS.md` | ninguém durante a produção, só leitura |
| `materiais-de-trabalho/INVENTARIO.md` e `materiais-de-trabalho/inventario/` | o `/flow-reels:planejar`, uma vez por vídeo, antes dos ganchos. Durante a produção é só leitura |
| `revisao/` | quem conduz o lote, uma vez, no fim |
| `materiais-de-trabalho/logs/` | quem conduz o lote |
| `materiais-de-trabalho/publicacao/` | o `/flow-reels:publicar`, depois da revisão, e nunca durante a produção |

Dois agentes escrevendo no mesmo arquivo é o jeito clássico de perder trabalho sem ninguém perceber.
