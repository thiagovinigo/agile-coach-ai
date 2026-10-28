# Variedade e som (4.0)

Esta frente cuida de duas coisas que fazem um reel não parecer o anterior: o **som** (cada efeito com
variações, escolhidas sem repetir) e a **linguagem do episódio** (o sotaque visual do reel, sorteado com
memória). A pesquisa por trás está em `docs/pesquisa-4-0/04-edicao-retencao-e-som.md` (seções 4, 6 e 7) e
`01-linguagens-visuais.md` (seção 5, "como evitar que pareça template").

| arquivo | o que é |
|---|---|
| `scripts/gerar_sons.py` | sintetiza a biblioteca: 15 famílias, 66 arquivos |
| `componentes/sons/` | os `.wav` e o `LEIA.md` com as medidas de cada um |
| `scripts/audio.py` | escolhe o arquivo de cada evento (família → variação), junta e espaça os efeitos |
| `motor/linguagens.json` | as 12 linguagens, as regras de convívio e o que cada peça pede do material |
| `scripts/linguagem.py` | `sugerir`, `registrar` e `conferir` a linguagem de um corte |
| `projetos/.historico-linguagens.json` | a memória: os últimos 10 reels (nasce no primeiro `registrar`) |

As quatro camadas da pesquisa, e onde cada uma mora:

```
1. DNA da marca        fixo em todo reel: fontes, rosa chapado, legenda revela, capa, fim seco, -14 LUFS
2. formato da série    notícia, ferramenta, tutorial, opinião, lista, teste  (linguagens.json → formatos)
3. linguagem           o sotaque deste reel: peças, herói, sons, trilha       (linguagens.json → linguagens)
4. estilo de produção  quanto de produção: essencial ... completo             (estilos.json)
```

O estilo responde "quanto". A linguagem responde "com que cara". As duas convivem: a linguagem diz o estilo
mínimo que ela pede (`estilo_minimo`).

---

## 1. Os sons

### 1.1 A biblioteca

Tudo é sintetizado pelo `gerar_sons.py` (só numpy, sem download, sem banco de terceiros): pode ir dentro do
pacote distribuído. 48 kHz, 16 bits, estéreo; pico verdadeiro ≤ -1 dBTP; sem DC; primeira e última amostra
em zero; todos com -18 LUFS de curto prazo (janela de 100 ms, ponderação K), para soarem parelhos soltos.

Cada **família** tem o **base** (`<nome>.wav`) e as **variações** (`<nome>-1.wav`, `<nome>-2.wav`...): o mesmo
desenho com outro timbre, outra duração ou outra altura. O base das seis famílias da 3.0 é o arquivo de antes,
bit a bit (os cortes antigos soam igual).

| família | base | variações | o som | para que evento |
|---|---|---|---|---|
| `whoosh` | 0,45 s | 4 (0,30 a 0,62 s) | ruído numa banda que sobe e desce, passando de um lado para o outro | transição, câmera, elemento grande que entra |
| `pop` | 0,08 s | 4 | bolha: tom curto que sobe enquanto some | card, número, selo, ícone |
| `tick` | 0,02 s | 4 | estalo seco de madeira clara | contador, item de lista |
| `clique` | 0,04 s | 4 | clique de interface: apertar e soltar | destaque que acende, botão, marca |
| `subida` | 0,50 s | 4 (0,40 a 0,65 s) | riser: ar abrindo e acorde subindo | o instante antes da revelação (termina no evento) |
| `clarao` | 0,35 s | 4 | impacto suave: corpo grave, sopro, brilho de ar | transição clarão, luz |
| `glitch` | 0,24 s | 3 | grãos digitais: bits esmagados, tom quadrado que salta, gagueira | transição glitch, palavra decodifica, "bug", virada |
| `rebobina` | 0,60 s | 3 | fita acelerando com wow e flutter, chiado que abre, trava seca | transição vhs, "pera, volta" (termina no evento) |
| `impacto` | 0,55 s | 3 | hit grave saturado com soco e sala pequena | herói, número grande, palavra brutal (só peso 3) |
| `estatica` | 0,50 s | 3 | chiado de TV que liga (tum da rede) e desliga (zíper) | look crt/vhs ligando, moldura-crt, transição pixels/vhs |
| `energia` | 0,90 s | 3 (0,70 a 1,10 s) | zumbido que cresce: tom sobe, filtro abre, tremolo acelera | mãos energia/aura/feixe, carga antes do herói (termina no evento) |
| `carimbo` | 0,14 s | 3 | baque de borracha e madeira, tapa do papel, segundo toque | palavra carimbo/marcatexto, selo, papel |
| `bip` | 0,08 s | 3 | bip de chip antigo: onda quadrada em 16 degraus (uma, duas ou três notas) | transição pixels, palavra pixel, mira travando, terminal |
| `obturador` | 0,20 s | 3 | câmera: estalo que abre, mola, estalo que fecha | polaroid, flash, print entrando, congela |
| `raio` | 0,65 s | 3 | craque elétrico, arco que zumbe, crepitação que rareia | mãos raio/faíscas, palavra neon acendendo |

As medidas de cada arquivo (duração, pico verdadeiro, ponto forte) estão no `componentes/sons/LEIA.md`, que o
script reescreve a cada rodada.

**Ponto forte.** É o instante mais forte do arquivo (energia alisada por Hann de 20 ms). O `audio.py` põe esse
instante em cima do `t` do evento. Nos sons de ataque seco ele fica nos primeiros 30 ms (na estática, nos primeiros 60 ms); no whoosh, no auge
da passagem (0,13 a 0,30 s); na `subida`, na `energia` e na `rebobina`, no fim (o som anuncia e termina no
evento). A `estatica` começa com um golpe que assenta, para o ponto forte ficar sempre no começo.

**Refazer.** `flow-reels produzir/gerar_sons` (2 s, 66 arquivos, 4,2 MB). A
mesma `--semente` dá os mesmos arquivos, bit a bit. `--so glitch,raio` refaz só essas famílias. O script
imprime a escuta técnica de cada arquivo (duração, pico, pico verdadeiro, RMS, DC, pontas, nível de 100 ms,
ponto forte, centroide e a **distância espectral para o base**, em dB por banda de terço de oitava) e reprova,
sem gravar nada, se algum passar do teto, tiver DC, não fechar em zero, sair mudo ou se uma variação ficar
igual ao base (menos de 0,5 dB de distância e a mesma duração). Mudar um desenho: a função `som_<nome>`; mudar
ou acrescentar uma variação: a lista `SONS` (os parâmetros de cada uma). Família nova entra no fim da lista,
para não mudar a semente das outras.

**Trocar por um som seu.** Um arquivo com o mesmo nome na pasta substitui o sintetizado; um `<família>-5.wav`
a mais entra no sorteio da família sem mudar código. Use só som que você tem direito de usar.

### 1.2 Como o evento pede o som

A peça chama `M.evento(t, tipo, peso, alvo, som)` com o **nome da família** (`"whoosh"`, `"glitch"`). O
`eventos.json` leva o mesmo nome. Quem quer um arquivo exato pede pelo nome dele (`"whoosh-2"`): aí não há
sorteio. Nome que não existe na pasta não toca e aparece na lista de "fora" do `audio.py`.

### 1.3 O que o `audio.py` faz com os eventos

Em ordem:

1. **Lê as famílias pedidas.** Para cada nome, o base e as variações que existem na pasta. Arquivo mudo fica
   fora da família.
2. **Escolhe quem toca.** Por prioridade (maior peso primeiro; no empate, o mais cedo), um evento entra se:
   - não há outro já aceito a menos de **0,25 s** (de qualquer peça). Som encavalado soa como erro, não como
     ritmo. (Regra da 2.0, mantida.)
   - a **mesma peça** não tocou nada a menos de **1,5 s**. A peça é o alvo sem o sufixo de dentro dela: o motor
     nomeia as peças `<cena>-<tipo>-<n>` (`c3-maos-2`) e os pedaços com mais um sufixo (`c3-maos-2-mao-1`,
     `c2-nuvem-1-conta`). Alvo sem esse desenho (a transição `desfoque`, a câmera `c5-separa`) é a peça
     inteira; alvo vazio não agrupa.
3. **Escolhe o arquivo de cada evento.** `h = sha256("<t com 3 casas>|<alvo>|<som>")`. O arquivo é
   `opções[h % n]`, na ordem base, `-1`, `-2`...; se for o mesmo do evento anterior da mesma família, passa
   para outro (`(i + 1 + (h >> 16) % (n - 1)) % n`). Nunca o mesmo arquivo em dois eventos seguidos da mesma
   família (um `"whoosh-2"` pedido pelo nome conta como da família `whoosh`).
4. **Varia um pouco cada toque**, também pelo hash: tom de -1 a +1 semitom (reamostragem linear, como fita:
   a duração muda junto e o ponto forte é recalculado) e volume de -2 a +1 dB. É o "pitch ±1–2 st, ganho
   ±2 dB" da pesquisa, do lado discreto.
5. **Põe no lugar e no volume.** O ponto forte cai no `t`; o nível é medido contra a voz: no auge, o efeito
   fica `--efeitos-db` (padrão -20) abaixo do LUFS integrado da fala, mais -2 dB no peso 2 e -4 dB no peso 1,
   mais a variação do passo 4.
6. **Mede e avisa.** Para cada efeito, a folga da voz sobre ele (aviso abaixo de 6 dB com a voz falando). No
   fim, a densidade: `densidade: 22 efeito(s) em 36.1 s, um a cada 1.6 s; 5 família(s), 14 arquivo(s)
   diferente(s); arquivo repetido em seguida: 0`. Mais de um efeito a cada 1,5 s no reel inteiro dá um
   `olhe` (não reprova).

O mesmo corte sai sempre igual: duas rodadas dão o mesmo `audio-final.wav`, bit a bit.

**Níveis, conferidos com a pesquisa (04, seção 4.1 e 4.2).** A pesquisa põe whoosh e pop de 10 a 14 dB abaixo
da voz, swish e clique de 14 a 18 dB, o hit do herói de 4 a 8 dB, e a mistura final em -14 LUFS com pico até
-1 dBTP. A fábrica fica do lado discreto: -20 dB no peso 3, -22 no peso 2, -24 no peso 1 (± a variação). No
corte 40, a folga medida da voz sobre os efeitos ficou entre +14 e +29 dB. Quem quiser o hit mais presente no
herói usa `--efeitos-db -16` ou pede o `impacto` com peso 3. O teto de -1 dBTP é garantido pelo loudnorm no
fim (o gate de volume mede a entrega).

**Medido no corte 40 (`teste-onda-1`):** 28 eventos com som, 22 tocaram (6 saíram: um pela regra de 0,25 s e
cinco pela de 1,5 s por peça), 14 arquivos diferentes, nenhum repetido em seguida. Os 9 gates do
`conferir_reel.py` passaram (volume -14,0 LUFS, -1,4 dBTP; sincronia p95 47 ms). O `audio.py` inteiro roda em
~5 s para 36 s de fala.

### 1.4 Que som para cada peça (sugestão para as frentes)

Quem decide o padrão de cada peça é a frente dela; esta tabela é o ponto de partida coerente com os kits das
linguagens. Só eventos de peso 2 ou 3 deveriam ter som; detalhe (peso 1) fica mudo.

| peça | som sugerido |
|---|---|
| transições `glitch` / `vhs` / `queima` / `pixels` | `glitch` / `rebobina` / `clarao` / `bip` |
| transições `persianas`, `cubo`, `forma`, `tinta`, `zoom-atraves` | `whoosh` (`zoom-atraves`: `subida` terminando no corte) |
| palavra `decodifica` / `pixel` / `brutal` / `carimbo` / `marcatexto` | `glitch` / `bip` / `impacto` (só no herói) / `carimbo` / `carimbo` |
| palavra `neon` / `cromado` / `vazado` | `raio` / `clarao` / `pop` |
| mãos `faiscas`, `raio` / `energia`, `aura`, `tela-maos`, `feixe` | `raio` / `energia` |
| mãos `contar` / `onda` / `rastro`, `eco` / `sombra` | `tick` / `impacto` / `whoosh` / nenhum |
| frames `polaroid` / `moldura-pop` / `dolly` / `foco` | `obturador` / `pop` / `subida` / `clique` |
| estética `moldura-crt` / `mira` / `linhas-foco` / `diagrama` / `recorte` / `papel` | `estatica` / `bip` / `impacto` / `tick` / `obturador` / `carimbo` |
| estética `luz` / `grade-synthwave` / `chuva`, `poeira`, `barras` | `clarao` / `subida` / nenhum (são textura) |
| look ligando (`crt`, `vhs`) | `estatica` |

### 1.5 O som padrão de cada peça (o que o código toca) e os kits

A tabela 1.4 foi o ponto de partida; o que vale é o que cada peça pede no `M.evento`. Cruzado peça a peça
com os kits (outubro de 2026, depois dos três reels reais), e todo kit de linguagem agora contém o som padrão
de cada peça que ela lista (contando o `sempre`: pop, clique, tick):

| peça | som padrão |
|---|---|
| palavra `glitch` / `digitacao` / `extrusao` / `pula` / `conta` | clique / clique + tick / whoosh / pop + tick / tick |
| palavra `decodifica` / `brutal` / `marcatexto` / `neon` / `carimbo` / `cromado` / `vazado` / `pixel` | bip / impacto / clique / estatica / carimbo / whoosh / whoosh / bip |
| transições `lamina`, `zoom-desfoque`, `chicote`, `desfoque`, `inclinada`, `mergulho`, `persianas`, `cubo`, `tinta`, `zoom-atraves`, `bolha-*` | whoosh |
| transições `clarao` / `queima` / `mascara` / `forma` / `glitch` / `vhs` / `pixels` | clarao / clarao / subida / subida / glitch / rebobina / bip |
| looks `crt`, `vhs` / `pixel` / `holograma`, `ascii` / `grao` / os outros | estatica / bip / glitch / nenhum / whoosh |
| estética `moldura-crt` / `grade-synthwave` / `linhas-foco` / `mira` / `diagrama`, `barras` / `recorte` | estatica / whoosh / impacto / bip / tick / pop |
| mãos `faiscas` / `contar` / `energia` / `tela-maos` / `feixe` / `onda` / `raio` | tick / pop / energia / whoosh / subida / impacto / raio |
| frames `celular3d` / `parallax`, `telas`, `dolly`, `moldura-pop` / `polaroid` | whoosh + pop / whoosh / obturador + whoosh |
| `nuvem`, `malha` / `objeto3d`, `logo-volume`, `dm` / `contorno`, `profundidade` / `deteccao` / `maos` / `hud`, `prompt`, `comentario` | whoosh / pop / subida / whoosh + tick / clique / tick + clique (comentário: tick + whoosh) |

O que entrou nos kits: `whoosh` no terminal (persianas, telas, looks), `impacto` e `subida` no recorte (brutal,
forma), `subida`, `glitch` e `estatica` no sci-fi (feixe, holograma, neon), `raio` e `subida` no mangá (raio,
forma), `glitch` na profundidade-3d (holograma), `subida` no editorial (máscara), `whoosh` no calmo (looks,
vazado, desfoque) e `clarao` na manchete (clarão). O anos-80 já tinha `whoosh`. A `grade-synthwave` passou a
tocar `whoosh` por padrão (a `subida` dela ficava fora dos kits).

**Trocar o som de uma peça.** A `palavra` (todos os efeitos) e a `grade-synthwave` aceitam `"som"`: uma família
(ou `"nome-N"`), ou `null`/`false` para calar (docs-4/transicoes-e-palavras.md, 2.1; docs-4/estetica.md). O
`look` e as mãos já aceitavam.

---

## 2. As linguagens (`motor/linguagens.json`)

### 2.1 As doze

| id | nome | eixos (tempo · acabamento · energia) | transições | herói | kit de sons | precisa |
|---|---|---|---|---|---|---|
| `vidro` | Vidro (a 3.0) | presente · limpo · baixa | inclinada, mergulho, desfoque | placa que gira; mergulho no celular | whoosh, pop, clique, subida | — |
| `terminal` | Terminal | retrô · sujo · média | glitch, pixels, persianas | prompt que executa; CRT desliga e volta | bip, glitch, clique, tick, estatica, whoosh | — |
| `cinema` | Cinema | retrô · sujo · baixa | queima, clarao, desfoque | dolly na tese; queima antes da tese | impacto, subida, clarao, whoosh | — |
| `recorte` | Recorte / colagem | atemporal · sujo · alta | tinta, forma, chicote | você vira adesivo; carimbo na lista | carimbo, obturador, pop, whoosh, impacto, subida | visão |
| `sci-fi` | Sci-fi / holograma | futuro · limpo · média | zoom-atraves, mergulho, desfoque | holograma nas mãos; varredura holograma | energia, bip, whoosh, raio, subida, glitch, estatica | visão |
| `anos-80` | Anos 80 | retrô · sujo · alta | vhs, persianas, chicote | grade nasce atrás; rebobina e volta | rebobina, estatica, whoosh, impacto | — |
| `manga` | Mangá | atemporal · sujo · alta | lamina, chicote, forma | quadro de impacto; onda de choque | impacto, whoosh, carimbo, pop, raio, subida | — |
| `profundidade-3d` | Profundidade 3D | futuro · limpo · baixa | zoom-atraves, desfoque, cubo | atravessa a moldura; camadas com objeto; dolly | subida, impacto, whoosh, bip, energia, glitch | visão + profundidade |
| `editorial` | Editorial / dados | atemporal · limpo · baixa | lamina, persianas, mascara | número que cresce; marca-texto no print | tick, clique, pop, whoosh, subida | — |
| `turbo` | Turbo | presente · limpo · alta | chicote, zoom-desfoque, cubo | palavra gigante; congela em polaroid | whoosh, pop, impacto, obturador | — |
| `calmo` | Calmo | presente · limpo · baixa | desfoque | zoom lento na frase | pop, clique, whoosh (1 ou 2 no reel) | — |
| `manchete` | Manchete | presente · sujo · alta | clarao, chicote, zoom-desfoque | marca-texto na notícia; carimbo de NOVO | obturador, impacto, whoosh, carimbo, clarao | — |

### 2.2 Os campos de cada linguagem

```json
"terminal": {
  "nome": "Terminal",
  "descricao": "o texto curto que o criador lê para escolher",
  "quando": "assuntos e formatos em que ela funciona",
  "assuntos": ["codigo", "claude code", ...],          // palavras que o --assunto casa (sem acento, palavra inteira)
  "eixos": {"tempo": "retro", "acabamento": "sujo", "energia": "media"},
  "peso": 1.0,                                          // peso de partida no sorteio (vidro 0,7: cansou)
  "estilo_minimo": ["essencial"],                       // estilos.json que dão conta dela
  "precisa": [],                                        // visao, profundidade, maos, rosto
  "incompativel": [],                                   // gravacao-de-tela
  "pecas": {"modos": [...], "sobre": [...], "look": [...], "palavra": [...], "transicoes": [...]},
  "legenda": {"estilo": "revela", "posicao": "base", "nota": "..."},
  "heroi": [{"id": "prompt-executa", "descricao": "...", "pecas": [...], "precisa": []}],
  "sons": {"kit": [...], "entra": "bip", "transicao": "glitch", "heroi": "estatica"},
  "trilha": {"climas": ["tech", "tensa"], "nota": "synth pulsante"},
  "ritmo": {"mudanca_s": [2.0, 3.0], "transicoes_por_reel": [3, 6], "nota": "..."},
  "cor_secundaria": "ciano #0099FF nas linhas e no HUD"
}
```

- `pecas` usa só os nomes do contrato da 4.0 e as peças da 3.0. `look` e `palavra` listam os `efeito`s; a
  transição `corte`, os modos `rosto-vidro` e `tipografia`, a sobreposição `palavra` e o CTA da marca
  (`comentario` + `dm`) valem em toda linguagem (chave `sempre`); o `linguagem.py` junta a ela as peças
  `sempre` do `estilos.json`.
- `contar` (os dedos contando, um efeito de mão que se lê) entrou no recorte e nas linguagens que já têm
  efeitos de mão: sci-fi, profundidade-3d e mangá. Pede as mãos no quadro (`requisitos`).
- O terminal recomenda a legenda `revela` na base: a `caixa` (pílula rosa sobre vidro translúcido) reprovou
  em contraste e passou 5 px da zona nos reels reais.
- Em `heroi.pecas`, `look:crt` e `palavra:carimbo` querem dizer "a sobreposição look (ou palavra) com esse
  efeito"; `zoom` é o zoom de ênfase da cena.
- `legenda` fica dentro do que o motor tem (`revela`, `palavra-acesa`, `pop`, `caixa`; `posicao` peito, topo,
  base). A legenda base da marca continua; a linguagem só muda o tratamento. Fonte e cor de destaque nunca.
- `cor_secundaria` mora em superfícies e linhas, nunca no texto, e não traz cor nova além do ciano. O destaque
  é sempre o rosa chapado.
- `requisitos` (topo do arquivo) diz o que cada peça pede do material. Os das peças novas seguem o plano; a
  frente de cada peça confirma no docs-4 dela, e o integrador corrige aqui.

### 2.3 As regras (`regras` no JSON)

1. **Uma base e no máximo uma convidada.** A base em pelo menos 70% das cenas; a convidada em 1 ou 2 cenas,
   como pontuação (o gancho ou a virada). A convidada difere da base em **exatamente um eixo** e não forma par
   proibido. Hoje isso dá:

   | base | convidadas possíveis (o eixo que muda) |
   |---|---|
   | vidro | editorial (tempo), profundidade-3d (tempo), turbo (energia) |
   | terminal | anos-80 (energia), cinema (energia) |
   | cinema | terminal (energia) |
   | recorte | anos-80 (tempo), manchete (tempo) |
   | sci-fi | profundidade-3d (energia) |
   | anos-80 | manchete, manga, recorte (tempo); terminal (energia) |
   | manga | anos-80, manchete (tempo) |
   | profundidade-3d | calmo, editorial, vidro (tempo); sci-fi (energia) |
   | editorial | calmo, profundidade-3d, vidro (tempo) |
   | turbo | manchete (acabamento), vidro (energia) |
   | calmo | editorial, profundidade-3d (tempo) |
   | manchete | anos-80, manga, recorte (tempo); turbo (acabamento) |

2. **Pares proibidos:** vidro + anos-80, vidro + terminal, sci-fi + recorte, anos-80 + cinema, manga +
   editorial, turbo + calmo, manga + calmo, profundidade-3d + recorte.
3. **No máximo 3 famílias de transição** por reel (o corte seco não conta), as da linguagem.
4. **Um momento-herói**, no máximo 2 aparições, entre **55% e 80% da duração**.
5. **Curva de intensidade:** alta nos 0 a 3 s (capa, fala em 0,3 s, primeira troca até 3,5 s); baixa a média dos
   3 aos 10 s; um reengate de peso 3 a cada 8 a 15 s; o pico no herói; média nos últimos 3 a 5 s (CTA de
   frente, corte seco que emenda no começo).
6. **Ritmo:** uma mudança relevante (peso ≥ 2) a cada 2 a 4 s, nunca mais de 5 s parado, teto de 0,5 por
   segundo. Cada linguagem afina o alvo (`ritmo.mudanca_s`).
7. **Um kit de sons por reel** (o da linguagem; a convidada só nas cenas dela).
8. **Memória:** a linguagem não repete nos últimos 2 reels, o herói nos últimos 4, a trilha nos últimos 8.

### 2.4 Como o plano declara

No topo do `cenas.json`, ao lado de `"estilo"`:

```json
"estilo": ["essencial"],
"linguagem": "terminal",
"heroi": { "t": 27.4, "nome": "prompt-executa" },
```

Com convidada: `"linguagem": {"base": "terminal", "convidada": "anos-80"}`. O herói também pode ser marcado
com `"heroi": true` numa cena (vale o `inicio` dela) ou num item de `sobre` (vale o `t` dele). O motor e o
`compor.py` ignoram as duas chaves; quem lê é o `linguagem.py` (e, na 4.2, o gate).

---

## 3. `scripts/linguagem.py`

```
flow-reels produzir/linguagem sugerir   --projeto projetos/<v> --corte NN [--assunto "..."] [--formato noticia] [--material tela] [--json]
flow-reels produzir/linguagem registrar --projeto projetos/<v> --corte NN [--linguagem x --convidada y --heroi h --trilha t --data AAAA-MM-DD]
flow-reels produzir/linguagem conferir  --projeto projetos/<v> --corte NN [--json]
```

`--historico <arquivo>` troca o histórico (padrão `projetos/.historico-linguagens.json`), para teste.
Saída 0 = certo; 1 = o `conferir` achou problema (ou nenhuma linguagem cabe); 2 = erro de uso.

### 3.1 `sugerir`

Sorteia 3 linguagens e imprime cada uma com a descrição, o porquê, o herói, a convidada possível, as
transições, o kit de sons, uma trilha sugerida e o estilo mínimo. Entre as três sorteadas, a de maior peso vem
primeiro, marcada "recomendada".

- **Semente:** `"<nome da pasta do projeto>|<NN>"` (sha256). O mesmo corte, com o mesmo histórico e as mesmas
  opções, sorteia sempre o mesmo.
- **Material** (lido da pasta do corte):
  - visão = `visao/visao.json` com a máscara valendo e a pessoa em ≥ 50% dos quadros, e o `.origem.json`
    com o tamanho do `fala.mp4` de agora;
  - profundidade = a mediana da pessoa ≥ 40 acima da do fundo (de 0 a 255: parede colada não separa);
  - mãos = mãos em ≥ 25% dos quadros; rosto = `rosto.json`.
  - `--material tela` (gravação de tela) desliga tudo isso.
  - Linguagem que `precisa` do que falta, ou `incompativel` com gravação de tela, fica de fora com o motivo.
    Herói que precisa do que falta não é sugerido; linguagem sem nenhum herói possível pesa 0,3x.
- **Pesos:** o `peso` da linguagem; × (1 + 1,5 × palavras do `--assunto` que batem, até 2) em `assuntos`
  (sem acento, palavra inteira); × 2 se o `--formato` a prefere, × 0,2 se a evita; × 0,75 por vez que
  apareceu nos reels 3 a 6 do histórico.
- **Memória:** a linguagem dos últimos 2 reels sai; o herói dos últimos 4 não é sugerido (se todos
  repetiriam, fica o mais antigo, com aviso); a trilha dos últimos 8 não é sugerida.
- **Trilha:** um arquivo de `componentes/trilhas/` cujo nome começa com (ou contém) um clima da linguagem,
  fora os dos últimos 8 reels. É só sugestão: trilha é sempre pergunta, e o criador escolhe. Sem faixa nova
  no clima, o script manda buscar com `buscar-trilha.py`.
- **Convidada:** sorteada entre as compatíveis com a base e com o material.

### 3.2 `registrar`

Grava `{projeto, corte, linguagem, convidada, heroi, trilha, data}` no histórico, que guarda os últimos 10.
Sem as opções, lê do `cenas.json` (`linguagem`, `heroi.nome`, `trilha.arquivo`). O mesmo corte registrado de
novo substitui o registro dele, no mesmo lugar. Avisa (sem recusar) convidada incompatível e herói que não é da
linguagem. Rode depois que o criador aprovar o corte.

### 3.3 `conferir`

Lê o `cenas.json` e diz, cena a cena:

- peça (modo, sobreposição, efeito de look ou de palavra, transição) que não é da base, da convidada nem do
  `sempre` → problema;
- a convidada em mais de 2 cenas, convidada que não difere em exatamente um eixo, par proibido → problema;
- peça que pede material que o corte não tem (`requisitos`) → problema;
- mais de 3 famílias de transição → problema;
- herói: nenhum declarado, fora de 55–80%, ou mais de 2 → problema; nome que não é da linguagem → aviso. Sem
  herói, lista os eventos de peso 3 que caem na faixa (se o `eventos.json` existe), como candidatos;
- estilo de produção abaixo do `estilo_minimo` → aviso (o `motion`, estilo da 4.0 e superconjunto dos outros, e
  o `completo` atendem qualquer mínimo);
- peças `sempre` (da tabela e do `estilos.json`) e o CTA da marca (`comentario`, `dm`) valem em toda linguagem;
- com o `eventos.json`: os sons pedidos, por família, e os que estão fora do kit → aviso.

---

## 4. A pergunta ao criador

Junto com velocidade, trilha e estilo, numa mensagem só, antes do `editar_fala.py`. O planejador roda o
`linguagem.py sugerir` (com `--assunto` e `--formato` do corte) e monta a quarta pergunta com as 3 opções que
ele imprimir. Modelo:

> **Antes de produzir o corte NN, quatro decisões** (pode responder numa linha, tipo "1,15x · sem trilha ·
> essencial · 1"):
>
> 1. **Velocidade da fala:** 1,0x (X palavras/s, Y s) · 1,15x (...) · 1,25x (...) · 1,5x (...)
> 2. **Trilha sonora:** sim ou não? Se sim, qual: *(as do clima; a sugerida pela linguagem primeiro)*
> 3. **Estilo de produção:** Essencial · Liquid Glass · Imagens · Tela cortada · Completo (pode juntar)
> 4. **Linguagem do episódio** (a cara deste reel; sorteada para não repetir os últimos):
>    1. **Terminal** *(recomendada)*: monitor CRT e linha de comando, texto que decodifica, glitch e pixel.
>       Herói: o prompt termina de digitar e a cena se monta em pixels. Sons: bip, glitch, estática.
>    2. **Cinema**: película, preto e branco no fundo, tarja e queima de filme. Herói: a película queima e a
>       tese entra em P&B.
>    3. **Editorial / dados**: número que cresce, diagrama que se desenha, marca-texto rosa no print.
>       Herói: o número conta enquanto o diagrama se desenha.
>
>    Ou outra: vidro, recorte, sci-fi, anos 80, mangá, profundidade 3D, turbo, calmo, manchete. Dá para
>    pedir uma convidada em 1 ou 2 cenas (ex.: "Terminal com Anos 80 no gancho").

Regras da pergunta:

- Sempre as 3 do `sugerir`, na ordem dele, com a descrição curta e o herói. Nunca escolher sozinho.
- Linguagem que pede a visão só aparece se o corte tem a visão; se o estilo escolhido for menor que o
  `estilo_minimo` da linguagem, dizer ("Profundidade 3D pede o estilo Tela cortada").
- Depois da resposta: `"linguagem"` e `"heroi"` no `cenas.json`, as peças só da linguagem, o `conferir` antes
  do render, e o `registrar` depois da aprovação.

---

## 5. Limites

- Os sons são sintetizados: soam limpos e "de interface", não como foley gravado. O `impacto` tem o corpo
  grave abaixo de 100 Hz, que o alto-falante do celular quase não toca; o soco e o estalo em médio-agudo são o
  que se ouve ali.
- A variação de tom é reamostragem linear (tira um pouco do agudo acima de ~15 kHz, inaudível no celular).
- A densidade global (um efeito a cada 1,5 s) só avisa; quem corta é o plano (som só em peso 2 ou 3).
- O `audio.py` não sabe da sílaba tônica da palavra destacada (a pesquisa pede o efeito 1 a 3 quadros antes ou
  no respiro): fica para o gate de SFX da 4.2.
- `requisitos` das peças novas é a leitura do plano; confirmar com os docs-4 das outras frentes. Em especial,
  `barras` foi tratada como tarja de cinema (se for o gráfico de barras, entra no `editorial`).


## 4.3 · pós no quadro inteiro e acabamento por linguagem

Cada linguagem do `linguagens.json` ganhou `pecas.pos` (os efeitos de `web/pos.js` que combinam com ela) e
`acabamento` (a LUT da marca sugerida, grão 0,2 e vinheta 0,15). `sempre.pos` = grão e vinheta, que valem em
qualquer linguagem. O `linguagem.py` lê `"pos"` do topo e de cada cena do `cenas.json` e reprova o efeito
que não é da base nem da convidada (a convidada conta como cena dela, como as outras peças).

| linguagem | pos | LUT |
|---|---|---|
| vidro | bloom, lente, aberracao | neutra-quente |
| terminal | crt, ascii, glitch, pixel, aberracao | fria-tech |
| cinema | lente, bloom | filme |
| recorte | reticula, pontilhado | neutra-quente |
| sci-fi | glitch, aberracao, bloom, onda, crt | fria-tech |
| anos-80 | vhs, crt, bloom, aberracao, onda | neutra-quente |
| manga | reticula, pontilhado, glitch | neutra-quente |
| profundidade-3d | lente, bloom, aberracao | fria-tech |
| editorial | reticula | neutra-quente |
| turbo | glitch, pixel, onda, aberracao, vhs | fria-tech |
| calmo | bloom | filme |
| manchete | reticula | noir |
