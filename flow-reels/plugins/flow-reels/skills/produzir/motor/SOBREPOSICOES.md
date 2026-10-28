# As sobreposições da 3.0

Peças que entram por cima de qualquer modo. Na cena (`cena.sobre: [...]`) nascem, morrem e andam com
ela nas transições; no reel (`CENAS.sobre: [...]`) ficam na `#camada-sobre`, acima das cenas e abaixo
da legenda, e não andam com as transições. Cada uma mora num arquivo de `web/sobre/` e se registra com
`Motor.registrarSobre(tipo, fn)`. O resumo está no `MOTOR.md`, seção 4.10; aqui está o contrato
inteiro de cada uma.

| tipo | arquivo | o que é |
|---|---|---|
| `pilha` | `sobre/pilha.js` | a manchete em pilha no topo, palavra a palavra no tempo da fala, com risco e colchetes de visor |
| `palavra` | `sobre/palavra.js` | a palavra que vira o que diz: glitch, digitação, extrusão, letras que pulam, número que conta |
| `hud` | `sobre/hud.js` | o HUD de capítulos: "EDITANDO AO VIVO" com o timecode correndo e a pílula do capítulo |
| `transcricao`, `prompt`, `timeline`, `comentario`, `dm` | `sobre/mocks.js` | as telas simuladas: a fala virando texto, o pedido sendo digitado, a timeline, o comentário e a DM do CTA |
| `logo-volume` | `sobre/logo-volume.js` | o logo oficial numa placa de app com volume, que pula com faíscas e flutua; com `segue`, presa à mão ou à cabeça (Onda 2) |
| `deteccao`, `maos`, `contorno` | `sobre/visao.js` | (Onda 2) a IA enxergando a cena: caixas de detecção com a confiança medida, o esqueleto das mãos e o contorno da pessoa com as camadas VOCÊ e FUNDO |
| `profundidade` | `sobre/profundidade.js` | (Onda 2) o vídeo vira um mapa de cor falsa que se espalha em onda, do mais perto até a parede, com a régua PERTO/LONGE ao lado da cabeça |

As peças da Onda 2 precisam da visão do corte (`scripts/visao.py`, contrato no `MOTOR.md` 2.6). Sem ela,
ou sem a parte que a peça usa, o motor recusa o plano com o Error que diz o que rodar. Qualquer peça
desta lista aceita `"atras": true` (abaixo).

## Texto atrás de você (`"atras": true`, Onda 2)

Toda sobreposição aceita `"atras": true`. A peça fica atrás da pessoa e na frente do cenário: a cabeça
passa por cima do título, como na abertura da referência. O contrato inteiro está no `MOTOR.md` 3.3.

- Precisa da máscara da `visao/`. Sem ela, o motor recusa o plano.
- O motor abre na peça um furo do formato da pessoa, quadro a quadro. Ali aparecem a pessoa e os cards
  do modo que passam na frente dela.
- A névoa da `palavra`, a sombra e o vidro da `pilha` ficam atrás da pessoa junto com a letra: a pessoa
  não escurece. O vidro continua vendo a cena.
- Na cena, a peça fica logo acima do vídeo e abaixo dos cards. No reel inteiro, fica no começo da camada
  das sobreposições e, fora da pessoa, por cima dos cards. Cena sem rosto na tela: a peça fica por cima,
  com aviso.
- **Numa cena `camadas`** (`MOTOR.md` 4.11), a peça com `atras` da cena vive no plano entre as duas
  placas: com as placas separadas aparece encolhida e de lado, no vão; quando elas se alinham, fica atrás
  da cabeça. Ela confere o próprio lugar no plano dela, que só é a tela com as placas alinhadas, e precisa
  caber no vão (até uns 800 px no plano, com a pose padrão). A linha da distância do modo desvia dela pelo
  `y` e o `tam`.
- A peça confere o próprio lugar, mas não sabe que vai ficar atrás. Quem escolhe o `y` e o `tam` é o
  planejador:
  - a palavra-chave fica acima do cabelo, e só a base da última linha encosta na cabeça (10 a 25% da caixa);
  - mais de 35% de um texto coberto por 0,3 s seguidos vira aviso do motor e reprovação no gate de
    contraste;
  - leia `atras[].topo` e `coberto` no `layout.jsonl` de um `--quadro` no pior instante antes de fechar;
  - o zoom de ênfase e o das emendas sobem a cabeça: ponha a saída da peça antes do zoom.
- O que a peça tiver de vidro com vidro dentro, ou de elemento com máscara própria, não recebe o furo e
  fica por cima da pessoa, com aviso.

## Sobreposição `pilha` (manchete em pilha no topo)

Vai na cena (`cena.sobre`, anda com as transições dela) ou no reel inteiro (`CENAS.sobre`, não anda com as transições).

```json
{ "tipo": "pilha", "t": 3.0, "ate": 7.5, "y": 250, "rotulo": "POR ISSO",
  "linhas": ["A EMPRESA", "AI *FIRST*"], "tam": 72, "tempo": "fala",
  "risco": { "linha": 1, "t": 6.2 },
  "colchetes": { "t": 6.8, "esquerda": "● FOCO", "direita": "4:5" },
  "saida": "desfoque", "fundo": "vidro" }
```

**Uma manchete por vez.**
- Quando a pilha seguinte (da mesma cena ou do reel inteiro) chega antes desta terminar de sair, esta sai mais cedo e some por completo no instante em que o fundo da outra começa a entrar. Isso vale também para a pilha de cena sem `ate`, quando uma pilha do reel inteiro chega no meio da cena.
- A conta lê o cenas.json inteiro e não depende da ordem das peças.
- Pilhas de cenas diferentes não interferem: a troca de cena separa as duas.
- Se a seguinte deixar menos de 0,4 s de tela para esta, o motor recusa o plano.

Campos:
- `t`: quando a pilha começa. O rótulo entra aqui, e a placa chega 0,1 s antes. Padrão: o início da cena. Sem rótulo, a placa chega 0,2 s antes da primeira palavra.
- `ate`: quando a pilha sai. Sem `ate` (ou no fim da cena), ela vai embora com a cena. Pode adiantar por causa da pilha seguinte.
- `y`: o topo da placa. Padrão 250. O texto nunca passa acima de y 220: o topo é recalculado a cada encolhida, e perto do topo a subida da saída encolhe.
- `rotulo`: texto pequeno em mono, maiúsculo e espaçado, entre dois fios, na tinta suave. Opcional. É centrado pelo CSS, então o centro não depende de a fonte ter carregado.
- `linhas`: de cima para baixo, em maiúsculas FC Titulo.
  - `*palavra*` ou `*duas palavras*` = destaque no gradiente (com data-cor).
  - A linha que é toda destaque cresce 1,2x.
  - Um item também pode ser `{ "texto": "...", "escala": 1.2 }` ou `{ "rotulo": "SÓ PRECISA" }`, o rótulo pequeno no meio da pilha, que entra quando a primeira palavra dele é dita. Depois da última linha com colchetes, ele desce para baixo das legendas dos colchetes.
- `tam`: corpo em px, padrão 72.
  - A linha que só caberia abaixo de 80% do corpo quebra sozinha.
  - O corpo encolhe até a mais larga caber em 880 px e até a pilha terminar acima das sobrancelhas e da legenda. Mínimo 44, e se não couber o motor avisa.
- `tempo`:
  - `"fala"` (padrão): cada palavra entra 50 ms antes de ser dita, procurada em ordem entre `t` e o `ate` pedido. Acento e pontuação não contam, e a busca pula até 8 faladas. A palavra não achada fica entre as vizinhas, com aviso.
  - `"uniforme"`: as palavras se espalham por igual até 60% da duração.
  - A última palavra entra até 0,3 s antes da saída. Se isso a obrigar a entrar mais de 0,1 s antes de ser dita, o motor avisa.
- Entrada de cada palavra: foco, de desfocada para nítida em 0,1 s, subindo 14 px. Rótulos: 0,14 s.
- `risco`: `{ "linha", "t" }` ou uma lista deles.
  - Traço no acento (cerca de 6 px, ponta redonda), da esquerda para a direita em 0,13 s.
  - Depois a linha recua para a tinta suave em 0,22 s. Na palavra em gradiente, a tinta suave cobre o gradiente aos poucos, sem salto.
  - Sem `t`: 0,3 s depois da última palavra da linha.
- `colchetes`: `{ "t", "esquerda", "direita" }`.
  - Cantos de visor (traço na tinta, cerca de 4 px) em volta da última linha, de 1,1x para 1x em 0,15 s.
  - As legendas mono ficam na linha de baixo. Um "●" no começo vira o ponto aceso no acento.
  - Sem `t`: 0,3 s depois da última palavra.
- `saida`:
  - `"desfoque"` (padrão), em dois tempos: as letras desfocam e sobem até 12 px em 0,2 s sobre o vidro ainda fechado; aos 0,17 s o vidro sobe junto, encolhe para 0,97 e some em 0,13 s. São 0,3 s ao todo. A `"sombra"` começa a sair na mesma hora, mas clareia em 0,35 s com entrada e saída macias, como a névoa da `palavra` (é a parede de cima inteira, e em 0,13 s virava um clarão): 0,52 s ao todo.
  - `"corte"`: some no quadro do `ate`.
- `fundo`:
  - `"vidro"` (padrão): placa de vidro líquido fumê. O filtro de fundo escurece e desfoca a cena antes da lente, sobre tinta leve. A placa cresce a cada fila, antes da palavra cair.
  - `"sombra"`: degradê escuro do alto do quadro até abaixo da pilha.
  - `"nenhum"`: letra solta. Só serve para vídeo escuro; sobre parede clara o contraste reprova.
- `maiusculas`: `false` mantém a caixa das linhas como foi escrita.

Avisos e eventos:
- Os avisos (palavra não achada, pilha que não coube, palavra adiantada pela pilha seguinte) saem como erro no console, no formato "pilha (nome): aviso: ...". É o tipo de mensagem que o compor.py repassa.
- Eventos:
  - O rótulo (ou a primeira palavra) e cada destaque: `entra` peso 2 com `pop`, no máximo um som a cada 0,25 s.
  - As outras palavras: `entra` peso 1, sem som.
  - Risco: `marca` com `tick`. Colchetes: `marca` com `clique`.
  - Saída: `sai` peso 2.
- Classes CSS com o prefixo `pilha-`.

## Sobreposição `palavra` · a palavra vira o que diz

Uma palavra da fala, grande, acima da cabeça de quem fala, fazendo o que ela significa. É o trecho de 57,2 a 59,5 s do reel de referência: cada palavra vive de meio segundo a um segundo e meio, entra rápido e sai em desfoque. Vai em `cena.sobre` (vive e anda com a cena, inclusive nas transições) ou em `CENAS.sobre` (o reel inteiro, na `#camada-sobre`).

```json
{ "tipo": "palavra", "texto": "CORTE", "efeito": "glitch", "t": 2.0, "ate": 3.0 }
{ "tipo": "palavra", "texto": "LEGENDA", "efeito": "digitacao", "t": 3.1 }
{ "tipo": "palavra", "texto": "3D", "efeito": "extrusao", "t": 4.4, "ate": 5.5 }
{ "tipo": "palavra", "texto": "ANIMAÇÃO", "efeito": "pula", "t": 5.7 }
{ "tipo": "palavra", "efeito": "conta", "valor": 26, "sufixo": "%", "t": 4.96, "ate": 7.3 }
```

| campo | o que é | padrão |
|---|---|---|
| `texto` | a palavra (ou duas), do jeito que aparece: o motor não muda caixa nem acento | obrigatório, menos na `conta` |
| `efeito` | `glitch`, `digitacao`, `extrusao`, `pula` ou `conta` | `glitch` |
| `t` | quando entra, no tempo absoluto. Para o movimento terminar em cima da palavra falada, use o início dela menos 0,2 s. Perto do zero vale: o que viria antes do zero começa no zero, e `t` negativo vira 0 (com aviso no console) | obrigatório |
| `ate` | quando sai, em desfoque com leve subida, em 0,2 s (a subida para no topo da zona segura). Com `ate` no fim da cena ou depois, a palavra sai com a cena | `t + 1,5` |
| `y` | o centro da palavra, na altura das maiúsculas | 360 (acima da cabeça) |
| `tam` | o corpo da letra. Encolhe sozinho até caber nos 940 px da zona segura, já contando o que a palavra anda (tremor, aproximação, soco) | 150; na `conta`, 190 |
| `gradiente` | a face no `--destaque-gradiente` (sem o token, o acento chapado) | sim na `extrusao` e no `pula`; não nos outros |
| `cor` | a face chapada, sem gradiente: `tinta` ou `destaque` | `tinta`; no `pula`, `destaque` |
| `sombra` | se a palavra pede a névoa escura (abaixo). Um número de 0 a 0,95 pede no mínimo essa força de névoa, para fundo mais claro que parede (céu, claraboia) | sim; não na `digitacao`, que já vem em vidro escuro |
| `fonte` | `titulo`, `legenda` ou `mono` | `titulo` |
| `duracao` | `digitacao`: quanto leva digitando; `conta`: quanto leva contando | o tempo da palavra falada no palavras-corte.json; senão 0,35 s (digitação) ou 0,8 s (conta) |
| `valor`, `prefixo`, `sufixo`, `casas` | só na `conta`: o número no lugar do texto | — |
| `id` | sufixo do nome nos eventos | — |

Os efeitos:

- **`glitch`**: um risco de luz cruza a altura da palavra 0,12 s antes. A palavra chega rasgada em 6 faixas, tremendo na horizontal e com a cor separada em duas franjas, e assenta nítida em 0,25 s (8 quadros). O rasgo começa num limite de quadro, e cada quadro dele sai de um hash do índice do quadro: o mesmo quadro sai sempre igual, renderizado em sequência ou sozinho. Som: `clique`.
- **`digitacao`**: um campo de vidro escuro chega do desfoque com o cursor em bloco no acento. As letras aparecem uma a uma no tempo da palavra falada, por recorte (o kerning da fonte fica). O recorte para no vão entre a tinta da letra digitada e a da próxima, então par apertado (ÇÃ) não mostra lasca. O cursor anda junto e some 0,2 s depois da última letra. Som: `clique` na primeira letra e `tick` a cada 0,25 s.
- **`extrusao`**: a face é acesa de cima (um brilho no alto que só clareia), com 14 camadas de espessura para baixo e para a direita, do acento até a superfície. Entra de 0,6 de escala com uma leve inclinação (20° em X, 5° em Y) e assenta em 0,3 s desacelerando, enquanto a espessura cresce. Na vida inteira, uma aproximação de 3% e a luz girando 12 graus, num tween só. Som: `whoosh`.
- **`pula`**: as letras caem uma a uma, com 0,045 s entre elas, alternando de cima e de baixo, com leve passada do ponto, cada uma num tom do gradiente (sem o token, uma rampa do acento clareado até o acento cheio). A viagem vem de amostrar o movimento inteiro na caixa girada e escalada: nenhuma letra encosta na zona segura, em nenhum `y`, e a que não cabe girada entra sem giro. Som: `pop` na primeira e `tick` em até 3 letras.
- **`conta`**: o número chega do desfoque e conta de 0 até o `valor`, ancorado no sufixo: o sufixo fica parado e os algarismos crescem para a esquerda. Só com prefixo e sem sufixo, a âncora é o começo. Quando para, dá um soco de 6% na escala. Som: `tick`.

**A névoa** é uma faixa escura de lado a lado, cheia na altura das palavras e sumindo para baixo (e para cima, longe da borda; perto do topo do quadro, vai cheia até a borda). Ela não pertence a uma palavra, e sim a uma **sequência**:
- **Quem divide uma névoa só:** palavras do mesmo grupo (a cena, ou o reel inteiro), com menos de 1,6 s entre o fim de uma e o começo da próxima, na mesma faixa de altura.
- **Quando liga e desliga:** baixa nos 0,2 s antes da primeira palavra, fica parada entre elas e só clareia 0,35 s depois que a última sumiu.
- **Na troca de cena:** a névoa nunca é cortada no meio da subida (era um flash no terço de cima).
  - Se a cena seguinte entra em corte seco (sem `entrada`) e a primeira palavra dela vem em menos de 1,6 s, na mesma faixa de altura e na mesma camada (as duas com ou sem `atras`), a sequência atravessa a troca: a névoa fica parada até o fim da cena e a da cena seguinte já nasce no mesmo nível, com a mesma faixa. Com transição as duas cenas dividem a tela e as névoas empilhariam, então não atravessa.
  - Senão, quando a subida de 0,35 s não cabe antes do fim da cena, ela é antecipada para chegar a zero no fim, começando no máximo quando a última palavra começa a desfocar (sobe de 0,2 a 0,35 s).
  - Palavra que ainda está na tela no corte (`ate` no fim da cena, ou a saída cortada no meio) leva a névoa junto com a cena, como antes.
- **Quanto escurece:** no meio da sequência ela só escurece (o branco pede ~0,42; um acento como o rosa do exemplo, ~0,74), nunca clareia e nunca empilha.
- **Palavra sem sombra** (a digitação) segura a sequência viva, mas não pede escuro.
- **Para o gate:** não é texto; fica no quadro sem texto e é medida como fundo.

**Gates:** toda face leva `data-texto` e um `data-cor` com a cor mais escura que ela mostra: o acento, quando é pintada pelo gradiente; o pé rosado, na extrusão branca. O cursor leva `data-zona`. Dois sons da mesma palavra nunca ficam a menos de 0,25 s (o audio.py junta os mais perto).

**Regra para o planejador:** duas palavras no mesmo `y` precisam de pelo menos 0,2 s entre o `ate` de uma e o `t` da próxima. A peça não desvia de outra palavra, e as saídas cruzadas das letras ficam sujas. A névoa já não depende desse espaço.

**A palavra sobre a cabeça:** a palavra não se move sozinha, mas, com a visão (`visao.json`, `pessoa.caixas`), avisa no console quando a cabeça (do alto da pessoa até o queixo do `rosto.json`) cobre mais de 30% da altura da letra num quadro da vida dela (já entrada, antes de sair). Quem fala se inclina para a câmera e o cabelo sobe: em y 430 a letra cai sobre o cabelo e a névoa escurece a testa. Letra no peito, abaixo do queixo, não avisa. O aviso diz o instante, o alto da pessoa e até que `y` subir naquele quadro; se não couber na zona segura, use `"atras": true`. Palavra com `atras` não avisa (ali a pessoa cobrir a letra é o efeito), e sem as caixas da visão não há o que medir. Como depende do quadro, o aviso sai no render que passa por ele (o `--quadro` só vê o dele).

## Sobreposição `hud` · o HUD de capítulos

A moldura de "edição ao vivo" da 3.0: duas pílulas pequenas de vidro escuro no alto, em letra mono, em caixa alta e com espaçamento largo.

- **Esquerda:** um ponto no acento, o rótulo e o timecode, que corre quadro a quadro.
- **Direita:** o capítulo da vez. O número (ou a letra de um acrônimo) vai num chip do acento, com letra escura, e o nome fica em branco ao lado.
- **Troca de capítulo:** o nome velho desfoca subindo e a pílula estica ou encolhe, com o chip e o nome presos à borda esquerda. O nome novo chega do desfoque já no lugar, revelado pela pílula que abre, e toca um tique. O chip nunca fica vazio: estoura e recolhe por escala, com os algarismos dentro.
- **Fim:** a pílula do capítulo sai, a da esquerda acende, o ponto vira um visto e o rótulo troca, com o relógio parado.

No reel inteiro vai em `CENAS.sobre` e não anda com as transições. Numa cena vai em `cena.sobre`: nasce, some e anda com ela.

```json
{ "tipo": "hud", "t": 0.2, "y": 236, "rotulo": "EDITANDO AO VIVO",
  "timecode": { "de": 0, "formato": "mm:ss:qq" },
  "capitulos": [ { "t": 0.5, "texto": "01 · O ERRO" }, { "t": 8.0, "texto": "02 · A PESQUISA" },
                 { "t": 14.0, "chip": "B", "texto": "BEGIN WITH PLAN MODE" } ],
  "fim": { "t": 34.0, "rotulo": "EDIÇÃO CONCLUÍDA" } }
```

| campo | o que é |
|---|---|
| `t` | Quando as pílulas entram (padrão: o início da cena, ou 0 no reel). O vidro pousa de cima em foco e a letra chega 0,1 s depois. A pílula do capítulo entra 0,08 s atrás, ou no `t` do primeiro capítulo, se ele vier depois. |
| `ate` | Opcional. As duas saem em desfoque em volta desse instante: começam 0,15 s antes, o vidro e logo atrás a letra, e somem até 0,05 s depois. |
| `y` | O topo das pílulas (padrão 236; nunca acima da zona segura). A altura é ~55 px com a letra em 25. |
| `tam` | A letra em px (padrão 25). As pílulas precisam caber entre x 70 e x 1010: lado a lado e, no fim, a da esquerda com o rótulo do fim. Se não cabem, o espaçamento aperta e depois a letra encolhe, até 17 px. Se nem assim cabe, o texto sai cortado com "…" e o console dá erro dizendo o que cortou. |
| `rotulo` | O texto da esquerda (padrão "EDITANDO AO VIVO"). |
| `timecode` | `{ de, formato }` ou `false` (sem relógio). `formato` junta `hh`, `mm`, `ss` e `qq` (qq = o quadro dentro do segundo); padrão "mm:ss:qq". `de` = o que o relógio mostra no t 0 do reel, em segundos ou em texto lido na ordem do formato: "01:12:00" com "hh:mm:ss:qq" é 1 h 12 min; com "mm:ss:qq" é 1 min 12 s. O relógio é o tempo do reel mais `de`. |
| `capitulos` | `[ { t, texto, chip } ]`. `chip` é o que vai no chip, número ou letra; `false` tira o chip. Sem o campo, um número no começo do texto ("01 · O ERRO", "02 A PESQUISA") ou uma letra seguida de separador ("B · BEGIN WITH PLAN MODE") vai para o chip, e o separador some; "A PESQUISA" continua nome. Capítulo antes do `t` das pílulas só vale se for o último antes delas. Capítulo depois do `fim` (ou do `ate`) não entra. Deixe pelo menos 0,4 s entre dois capítulos. |
| `fim` | `{ t, rotulo }`: a virada para "concluída" (padrão "EDIÇÃO CONCLUÍDA"). A pílula do capítulo sai, a do relógio acende com o tingido do acento, o ponto vira um visto e o relógio para no quadro do `t`. |

**Eventos:**
- A entrada é `entra` com pop, peso 2.
- A pílula do capítulo, se entra 0,25 s ou mais depois, é outro `entra` com tique, peso 2.
- Cada troca de capítulo é `entra` com tique, peso 1.
- O fim é `acende` com clique, peso 1, mais um `sai` sem som da pílula do capítulo, a T − 0,15.
- O relógio não é evento.

**A faixa do HUD:**
- O HUD ocupa de y 236 a ~291, a mesma faixa onde rosto-vidro, painel-rosto, lista, lado-a-lado, imagem-cheia e tela-bolha põem o conteúdo de cima por padrão.
- **Num reel com HUD, dê "y" a partir de ~320 aos elementos do topo.**
- Se algum texto ou logo de outra peça repousar nessa faixa, o console dá erro na montagem, com a cena, o texto e o y para descer o conteúdo.
- Na tela, a pílula sai da frente: desfoca um pouco antes de o outro chegar e volta em foco quando ele sai. Janelas a menos de 0,7 s viram uma só. Assim nunca fica letra sobre letra, mesmo com o plano errado.

**Regras:**
- A letra nunca desbota junto com o fundo dela, e algarismo nunca sai de cima do chip. O gate de contraste toma a cor da letra como opaca e mede a caixa do texto contra o quadro sem texto.
- O texto que muda de tamanho mora numa janela que recorta, e é ela que leva o data-texto.
- Nada se mexe sem fim: o reflexo da borda corre uma vez ao pousar e uma vez no fim.

## Sobreposições · os mocks de interface (`web/sobre/mocks.js`)

Telas de interface simuladas, genéricas, no vidro escuro da marca: nenhuma imita a tela, o logo ou a fonte de aplicativo nenhum. Mostram o processo (a fala virando texto, o pedido virando edição) e fecham o reel com a chamada (comenta a palavra, recebe a DM).

Vão em `cena.sobre` (nascem, morrem e andam com a cena nas transições) ou em `CENAS.sobre` (o reel inteiro). Os tempos são absolutos, como todo o plano. Um `t` antes do início da cena vira o início dela, porque antes disso a cena nem está na tela. `y` é o topo do mock, em pixels de saída; o x e a largura são do próprio mock, sempre dentro da zona segura.

O vidro entra de desfocado para nítido em 0,14 s (`anim.entra`, modo `foco`, com pop) e sai em desfoque em 0,2 s, com leve subida, no `ate`. A DM tem entrada própria, descrita abaixo. A letra entra 0,08 s depois do vidro e começa a sair um quadro antes dele, em 0,1 s. Assim, o vidro meio transparente da entrada e da saída nunca fica atrás de letra, e o gate de contraste passa em qualquer quadro. Sem `ate`, ou com ele no fim da cena (ou do reel), o mock fica até o fim.

O mock nunca muda de lugar sozinho. O console dá erro, e o compor.py mostra o erro nos avisos do motor, nestes casos:
- o mock passa da zona segura;
- o mock cobre o miolo do rosto (da sobrancelha à boca);
- o mock fica embaixo da legenda, que está numa camada acima de cenas e sobreposições;
- a palavra do comentário não cabe na pílula.

A legenda é conferida duas vezes: pela altura que cada cena pede, ao montar, e pela caixa de verdade, quadro a quadro no render inteiro (já com o desvio do rosto, também em `CENAS.sobre`). O `--quadro` fica só com a primeira conferência.

| tipo | tamanho | `y` padrão | sons |
|---|---|---|---|
| `transcricao` | 940 x 224 | 250 | pop na entrada |
| `prompt` | 940 x (altura do texto a 50 px + 244); 364 com duas linhas | 260 | pop; tick por palavra digitada (no máximo um a cada 0,3 s); clique no envio |
| `timeline` | 940 x (80 + 58 por trilha) | 1000 | pop; tick por trilha (0,26 s entre elas) |
| `comentario` | 820 x 104 | se encaixa na legenda (abaixo) | pop; tick no início da digitação; clique no envio; whoosh do avião na saída |
| `dm` | 880 x 166 | se encaixa na legenda (abaixo) | pop |

```json
{ "tipo": "transcricao", "t": 0.2, "ate": 6.5, "y": 250, "arquivo": "fala.mp4", "idioma": "pt-BR" }
```

- As palavras do `palavras-corte.json` correm da direita para a esquerda. A da vez fica no centro, numa caixa de vidro no acento, com o tempo dela em cima (`mm:ss:qq`, em que qq é o quadro) e uma onda de som embaixo.
- Na palavra nova, a fita corre até centrar em 0,06 a 0,16 s, desacelerando. A palavra só acende (branca) quando a fita a traz para dentro da caixa.
- A palavra comprida encolhe para caber no miolo da fita.
- O rodapé mostra `arquivo · idioma` e "PALAVRA n / total". `arquivo` tem como padrão o `fonte.video` do plano.
- Cada palavra nova vira um evento `acende` de peso 1, sem som, no máximo um a cada 0,6 s.

```json
{ "tipo": "prompt", "t": 6.9, "ate": 13.2, "y": 260, "arquivo": "gravacao.mp4", "meta": "VÍDEO · 4K",
  "texto": "A minha própria gravação virou o prompt.", "destaque": ["minha gravação"],
  "digitar": { "de": 7.3, "ate": 9.8 }, "rotulo": "PROMPT" }
```

- Caixa de pedido com o arquivo anexado (ícone, nome, `meta` em mono), o botão de anexar e o `rotulo`.
- O `texto` (obrigatório) é digitado letra a letra, a 50 px, com o cursor no acento.
- Cada entrada de `destaque` é uma palavra ou uma expressão, que acende só onde aparece inteira e na ordem. O destaque vai em negrito (FC Legenda) no acento, em gradiente quando a marca tem um.
- Quando a digitação termina, o botão de enviar acende, afunda, volta com passada e abre um anel no acento.
- Sem `digitar`, a digitação começa 0,35 s depois do `t`, a ~20 letras por segundo.

```json
{ "tipo": "timeline", "t": 14, "ate": 21, "y": 1000, "trilhas": ["CORTE", "LEGENDA", "3D", "ANIMAÇÃO"],
  "arquivo": "fala.mp4", "miniaturas": 8 }
```

- Régua com o tempo do reel inteiro e o nome de cada trilha à esquerda.
- A 1ª trilha são `miniaturas` (de 3 a 14) quadros do próprio `fala.mp4`, recortados em volta do rosto, com as emendas e as trocas de cena marcadas.
- A 2ª trilha são as palavras da fala, cada uma no tempo dela, reveladas por uma varredura.
- Da 3ª em diante, entram de 3 a 5 clipes no acento, sempre nas mesmas posições.
- As trilhas entram uma depois da outra, e os clipes em fila.
- A agulha atravessa a largura uma vez, durante a vida do mock, e acende cada clipe que cruza (evento `acende` de peso 1, sem som).
- Num rosto grande, o y padrão 1000 cobre o rosto, e o console avisa. Nesse caso, ponha a timeline no alto (y 250).

```json
{ "tipo": "comentario", "t": 30, "ate": 33, "palavra": "BUILD",
  "placeholder": "Adicione um comentário…", "digitar": { "de": 30.5, "ate": 31.0 }, "largura": 820 }
```

- Campo de comentário numa pílula. A `palavra` (obrigatória) entra letra a letra, e o botão de enviar acende com um clique.
- A palavra longa encolhe até 26 px para caber antes do botão. Se ainda não couber, o console dá erro.
- No `ate`, a pílula desfoca e um avião de papel sai do botão voando para cima, por cima dos outros mocks da mesma camada. O avião é cheio no acento, com contorno branco, e cresce até 1,25x.
- O voo leva 0,46 s e precisa acabar antes de a cena sumir; no fim do reel, 0,1 s antes do fim (o `-shortest` do audio.py pode comer o último quadro, e o último quadro é o do loop e o da prévia). Sem esse espaço, o voo e o fade encolhem juntos, com aviso no console. Com menos de 0,2 s, o avião não decola: some com a pílula, dentro do botão, e o console avisa até quando terminar o comentário. Para o voo inteiro no fim do reel, termine o comentário pelo menos 0,56 s antes do fim.
- Sem `digitar`, a digitação começa 0,5 s depois do `t`, a 0,085 s por letra.

```json
{ "tipo": "dm", "t": 33.4, "ate": 36, "nome": "Seu Nome", "texto": "te enviou o checklist",
  "rotulo": "DIRECT · agora", "avatar": "/marca/foto.jpg", "avatar_recorte": [213, 199, 696, 696],
  "anexo": true, "largura": 880 }
```

- A DM tem entrada própria: desfocada para nítida em 0,16 s enquanto cai 56 px do alto do próprio lugar, com passada suave (`back.out`, 0,5 s), e um pop. A foto, a pílula, o anexo e o ponto de não lida entram em fila.
- A foto é redonda, com anel no acento. Sem foto, entram as iniciais.
- O nome vai em negrito, e a última palavra do `texto` vai numa pílula no acento, com letra escura: branco sobre o rosa do exemplo dá 3,6:1, pouco para letra pequena.
- Texto que não cabe: sai a miniatura do anexo, depois a frase encolhe até 24 px, e o que ainda sobrar vira reticências (na frase, no nome e no rótulo).
- `avatar_recorte` escolhe o pedaço da foto; o padrão é o quadrado do rosto de um retrato.
- `anexo: false` tira a miniatura do documento.

**Onde o comentário e a DM ficam sem `y`**

- Os dois se encaixam na faixa por onde a legenda passa durante a vida deles, já desviando do rosto.
- Se cabe antes de y 1420, ficam logo abaixo da legenda, no peito, como na referência.
- Se não cabe, ficam logo acima dela. No rosto-vidro, com a legenda em y 1300: comentário em y 1121, DM em y 1059.
- Com a legenda no alto ou desligada, encostam na base da zona segura: comentário em y 1316, DM em y 1254.
- Os dois terminam na mesma linha, porque a DM ocupa o lugar do comentário.
- Com o rosto grande e a legenda na base, acima da legenda cai no queixo ou na boca, e o console dá erro. Nesse caso, dê à cena do CTA `"legenda": {"posicao": "topo"}`.
- Entre o `ate` do comentário e o `t` da DM, deixe 0,4 s. É o tempo do voo do avião, e o audio.py descarta o whoosh com o pop a menos de 0,25 s.

Notas:

- **Pré-carga**: o avatar da DM e os quadros da timeline entram na pré-carga do motor. Ao carregar, o `mocks.js` acrescenta as chaves `imagem` e `_quadros` ao `window.CENAS` em memória (o arquivo não muda).
- **Contraste**: o vidro dos mocks é o escuro da marca, mais fechado (de 88% a 77% da superfície). A letra miúda (18–19 px) usa a tinta suave puxada um terço para a tinta, escrita em `rgb()`.
- **Busca de tempo**: o que entra em fila aparece por um `set` no próprio instante. Uma prévia que volta e salta à frente renderiza o mesmo quadro que um render novo.

## Sobreposição `logo-volume`

O logo oficial em cor numa placa de app com volume. A placa tem corpo escuro opaco com brilho de vidro e espessura em 3D. Ela pula com passada do ponto, solta faíscas, flutua devagar e sai em desfoque. Vai em `cena.sobre` (vive com a cena e anda com as transições) ou em `CENAS.sobre` (o reel inteiro, parada durante as transições).

```json
{ "tipo": "logo-volume", "acervo": "claude-faisca", "t": 4.0, "ate": 7.0,
  "x": 300, "y": 1050, "tam": 190, "particulas": true, "flutua": true, "inclina": [-8, 12] }
```

| campo | padrão | o que faz |
|---|---|---|
| `acervo` | obrigatório | o logo de `componentes/marcas/` (sem extensão). Use o símbolo (`-icone`, `-faisca`, `-simbolo`), não um ícone que já vem com placa própria. `imagem` no lugar aceita um PNG sem fundo da pasta do corte. |
| `t` | início da cena + 0,15 | o pop. Para o pop terminar em cima da palavra, `t` = início da palavra − 0,2 s. |
| `ate` | — | a saída em desfoque (0,2 s), sempre inteira dentro da cena. Um `ate` no fim da cena (ou nos últimos 0,2 s) sai 0,2 s antes do fim. Sem `ate`, a placa fica até o fim e sai com a cena, levada pela transição. Com menos de 0,4 s de vida, a peça fica de fora e o console avisa. |
| `x`, `y` | 540, 1050 | o centro da placa, em pixels de saída. A placa, a passada do pop e a deriva cabem na zona segura; fora dela, o centro é puxado para dentro e o console avisa. |
| `tam` | 190 | o lado da placa (90 a 420). |
| `escala` | 0,62 | a fração da placa que o logo ocupa, medida pela área, com teto de 76% em qualquer direção. |
| `particulas` | true | clarão no acento, anel no formato da placa e de 10 a 14 faíscas (acento e branco) que somem desfocando em ~0,35 s. O sorteio vem do nome da peça: o mesmo plano dá sempre as mesmas faíscas. |
| `flutua` | true | uma deriva só, do pop à saída, em sine.inOut: sobe 14 px e gira até 3° para fora do centro (0 numa placa centrada). A inclinação cai pela metade e a sombra de contato clareia. `{ "y": -20, "giro": 2 }` troca os valores; `false` deixa parada. Nunca é laço. |
| `inclina` | olha para a câmera | `[rotateX, rotateY]` em graus; o que faltar vale 0. O padrão é rotateX 8 abaixo de y 760 e −8 acima. rotateY vira para o meio e cresce com a distância do centro: 12 a 180 px dele ou mais, 0 numa placa centrada, que fica de frente. No pop, a placa chega de uma pose mais forte: de lado, girando em Y; centrada, tombando em X. |
| `tinta` | `"marca"` | `"marca"`: corpo escuro com um fio do acento. `"neutra"`: só a superfície. `"logo"`: nenhum acento na face, na espessura nem no aro, e a luz do logo tinge o corpo. As faíscas e o anel ficam sempre no acento. |
| `luz` | true | a cor do logo acende o corpo por dentro, embaixo (uma cópia do PNG muito desfocada, atrás do logo). |
| `som` | `"pop"` | o efeito do pop; `null` tira. |
| `plano` | false | placa de frente, sem giro e sem a luz do logo. |

- O logo nunca é recolorido, esticado nem coberto: o reflexo passa por baixo dele, e quem inclina é a placa inteira.
- Marca cujo guia proíbe inclinar ou pôr efeito no logo (hoje a n8n) fica sempre `plano`. O console avisa se o plano pedir inclinação ou se o logo sair com menos de 100 px de largura.
- O corpo não é um `M.ui.vidro`. O vidro do motor desfoca o que está atrás dele, e atrás da face estão as lâminas da própria espessura, não o vídeo. É um corpo opaco com fio de luz, aro, reflexo e faixa especular, como as placas da referência.
- O que a placa cobre: a peça fica por cima dos cards do modo, e o gate de contraste não vê texto escondido por ela. A peça confere quadro a quadro, enquanto está na tela (desfoque da saída incluído), se o miolo da placa cruza as letras de um texto, a linha da legenda ou o miolo do rosto (da sobrancelha à boca). Avisa uma vez de cada, com o instante. Mude x/y ou os tempos. Acima da cabeça, deixe ar até o cabelo; no alto, ao lado da cabeça, costuma ter parede livre.
- Todos os avisos vão em `console.error`, que o compor repete no fim do render completo, em "avisos do motor".
- A placa leva `data-zona`: entra no gate de zonas e fica fora do de contraste. As faíscas não levam.
- Eventos: `entra` de peso 2 com som no pop; `sai` de peso 1 sem som na saída.

Exemplo com dois logos nos ombros, 0,8 s um do outro, e um no alto, ao lado da cabeça:

```json
"sobre": [
  { "tipo": "logo-volume", "acervo": "claude-faisca", "t": 24.85, "ate": 27.0, "x": 180, "y": 1062, "tam": 176 },
  { "tipo": "logo-volume", "acervo": "postgresql-icone", "t": 25.65, "ate": 27.0, "x": 900, "y": 1062, "tam": 176, "tinta": "logo" },
  { "tipo": "logo-volume", "acervo": "salesforce-icone", "t": 3.24, "ate": 4.72, "x": 270, "y": 330, "tam": 170 }
]
```

### `logo-volume` presa a você (`segue`, Onda 2)

A placa pode andar presa à mão ou à cabeça, quadro a quadro, como os objetos na palma da referência.
Precisa da visão do corte (`maos.json`; na cabeça, o `rosto.json` e a caixa da pessoa) e da vista do rosto
na cena. Sem `segue`, a peça é exatamente a de antes, pixel a pixel.

```json
{ "tipo": "logo-volume", "acervo": "claude-faisca", "t": 7.35, "ate": 10.0, "tam": 170,
  "segue": "mao-direita", "ancora": "palma", "desvio": [0, -10], "pedestal": true }
```

| campo | padrão | o que faz |
|---|---|---|
| `segue` | — | `"mao"`: qualquer mão, a que está na tela no pop; a placa fica com ela e, quando ela some, passa para a outra. `"mao-esquerda"` e `"mao-direita"`: o lado de quem assiste. `"cabeca"`: o alto do cabelo. Com `segue`, `x`/`y` viram só o lugar de reserva (cena sem vista do rosto). |
| `ancora` | `"palma"` | Só com a mão. `"palma"`: na vertical do centro da palma (média dos pontos 0, 5, 9, 13 e 17), logo acima dela; com a mão em pé, a placa sobe acima dos dedos só até 0,8 mão da palma e cobre as pontas. `"ponta"`: acima da ponta do indicador (ponto 8). Na cabeça, a âncora é o alto do cabelo (`visao.json` → `pessoa.caixas`; sem ela, ~0,45 rosto acima da testa). |
| `desvio` | `[0, 0]` | `[dx, dy]` em px de saída, somado ao lugar padrão, na escala 1 da câmera. Na cabeça, serve para pôr a placa ao lado dela, no alto: num busto o cabelo sobe até perto de y 390, e a placa acima dele bate no topo da zona. |
| `pedestal` | `true` seguindo a palma; `false` no resto | O anel holográfico em perspectiva, no `--destaque-gradiente`, com disco de luz, feixe até a placa e um cone fraco de fios. Fica no ponto seguido e só acende onde há uma palma perto da placa. Acende 0,14 s antes do pop, pulsa no pop e sai desfocando com a placa. Quando o `segue` não consegue seguir (a placa fica parada em `x`, `y`, com aviso), o padrão não acende; só um `true` escrito no plano acende. Sem `segue`, `true` põe o anel 0,45 lado abaixo da placa parada. |

**De onde vem o ponto.** Do quadro do vídeo que a vista do rosto mostra, levado para a tela pela mesma
conta do motor: o enquadre, o zoom de ênfase e o das emendas, lidos da própria linha do tempo. A placa
cresce com os dois zooms, como a mão. Na cena, ela anda com as transições; no reel inteiro, segue a vista
do rosto da cena da vez e fica parada nas transições (com aviso). No `camadas`, com as placas separadas,
ela segue a mão na placa da frente pelo `plano3d` do modo (perspectiva exata) e encolhe com a imagem,
também durante os movimentos; o console avisa os trechos.

**Identidade da mão.** O `maos.json` já traz o lado da trilha inteira (`MOTOR.md` 2.6), e a peça ainda
confere na tela: com as duas mãos, a mais à esquerda é a esquerda; com uma só, ela é do lado cuja última
posição (até 6 quadros atrás) está mais perto; sem nenhuma recente, vale o lado do meio do corpo.

**Mão que some.**
- Falha de até 4 quadros (0,13 s, o detector piscando no gesto rápido): a placa atravessa em linha reta.
- Falha maior, com `"mao"`: a placa passa para a outra mão, se ela estiver na tela.
- Falha maior, com o lado pedido: a placa pega a outra mão emprestada só quando a dela some no meio do
  quadro (ela se escondeu atrás ou na frente da outra) e volta quando ela reaparece.
- Mão que sai pela borda, ou nenhuma mão na tela: a placa espera no último lugar e o pedestal apaga.
  Antes da primeira detecção, ela espera no lugar da primeira, sem trocar de mão.

**Sem tremor e sem atraso.** O `maos.json` já vem sem tremor (One Euro). A peça passa uma gaussiana que
estreita com a velocidade (2 quadros com a mão parada, 3 na cabeça, até 0,6 no gesto rápido): o gesto
rápido segue colado. Só o salto que a velocidade não explica (a troca para uma mão longe, a volta da
espera, a detecção que pula mais de max(50 px, 1,6 mão) da posição prevista) vira uma curva de 0,13 a
0,5 s. Nada disso atravessa uma emenda: ali a placa pula junto com a imagem.

**O pedestal só acende em cima de uma palma e perto da placa.** Apaga quando a mão some, na viagem longa
até outra mão (mais de 1,5 mão) e quando a borda da zona (ou o rosto) tira a placa do lugar dela: começa
a 0,35 lado e apaga de todo a 0,85. Num busto a mão fica abaixo de y 1440, e o feixe esticado até ela,
com o anel na faixa da interface do Instagram, lia como projetor.

**Zona segura e rosto.** A placa, com a passada do pop, a deriva e o zoom, nunca sai da zona: com a mão
abaixo de y 1440, ela segue por cima, na borda de baixo, sem pedestal. Nunca para no miolo do rosto (da
sobrancelha à boca): quando a mão passa na frente, ela escorrega para o lado de fora, aos poucos. Duas
placas que seguem e se encostam se afastam na horizontal, cada uma metade do que falta, sem trocar de
lado.

**Determinismo.** A posição de cada quadro sai só do tempo e dos dados, por um tween de relógio com
`modifier` que roda em toda busca: a legenda que mede outros quadros vê a placa no lugar daquele quadro, e
o `--quadro` dá o mesmo que o render em sequência. No quadro renderizado, a peça confere a conta contra o
`M.fonteParaTela`; se diferem (a vista dentro de uma peça que se mexe), a placa vai para onde o motor põe a
mão, com aviso acima de 3 px.

**Avisos** (`console.error`, em "avisos do motor"): `"segue" precisa do rosto na tela ...; a placa fica
parada em (x, y)`; `no pop (t s) não há mão <lado> no maos.json; a mais perto aparece em … s`; a mão que
some de a a b s (esperas de 0,3 s ou mais na vida que se vê); a mão que passa da zona segura (a placa a
mais de meio lado do lugar dela por 0,3 s); peça do reel que cruza transição; vista do rosto que se mexe;
a conta que não bate; os trechos do `camadas`; e os avisos de antes (texto, legenda e rosto cobertos).
Erros: `segue` ou `ancora` inválidos, `desvio` que não é `[dx, dy]`, mão sem `maos.json`, `"cabeca"` sem
`rosto.json`.

**Para o planejador.** Escolha o trecho olhando o `maos.json` e a `folha-visao.png`: os melhores são os
gestos com a mão aberta e alta, perto de y 1440 na tela ou acima. Abaixo disso, a placa flutua por cima da
mão, sem pedestal. Confira que a mão aparece no pop (o aviso diz quando a mais perto aparece): no corte de
teste, as mãos somem de 3,27 a 4,47 s, bem na palavra "Salesforce", e ali só a cabeça servia. Duas placas,
uma em cada mão, no mesmo trecho funcionam. O pedestal é luz, não logo: como as faíscas, não leva
`data-zona` e pode passar de y 1440.

## Sobreposições da visão: `deteccao`, `maos`, `contorno` (`web/sobre/visao.js`, Onda 2)

As técnicas 2, 6 e 10 do atlas (1 a 4 s, 19 a 21,9 s e 32 a 41 s do reel de referência). As três ficam
presas ao vídeo da fala, quadro a quadro.

```json
{ "tipo": "deteccao", "t": 1.8, "ate": 3.1, "alvos": ["rosto", "maos", "objetos"], "feixe": true, "contador": true }
{ "tipo": "maos", "t": 12.5, "ate": 16.05, "mao": "ambas", "rotulo": true }
{ "tipo": "contorno", "t": 16.4, "ate": 18.75, "rotulos": true, "cor": "tinta", "tingir": true }
```

- **Onde vão.** Em `cena.sobre`, sobre a vista do rosto da cena; numa cena sem rosto, o motor recusa o
  plano com Error. Em `CENAS.sobre`, sobre a vista do rosto da cena da vez; numa transição, elas não
  acompanham a cena que sai (aviso). O modo que combina é o `rosto-vidro`, ou o `vidro-liquido` de frente.
- **Camada.** Na cena, o desenho preso ao vídeo (feixe, miras, esqueletos) fica logo acima da vista do
  rosto e abaixo dos cards do modo: o card passa na frente da mira. As pílulas, os cartões e as guias
  ficam por cima de tudo da cena. No reel inteiro, tudo fica na `#camada-sobre`.
- **De onde vêm os dados.** Do `visao.py` (`maos.json`, `corpo.json`, `objetos.json`, as máscaras) e do
  `rosto.json`.
- **Confiança.** Toda confiança na tela é um número que o modelo deu num quadro medido, e troca no máximo a
  cada 4 quadros. Mãos e objetos: o último quadro com `medido: true` da mesma trilha. Rosto: o `rosto.json`
  interpola os buracos sem marcar quais são, então o número só aparece com `achados` 100 e o quadro
  múltiplo do passo (`fps / fps_analise`); fora disso, a pílula diz só "ROSTO", com aviso. Corpo: sem
  confiança (o `score` do Pose Landmarker é a média da presença dos 33 pontos e lê como dúvida num busto);
  a pílula mostra "CORPO NN PONTOS", os pontos que o modelo vê dentro do quadro.
- **No `camadas`** (`MOTOR.md` 4.11), a vista do rosto é você recortado na placa da frente, e a conta segue
  a placa pela perspectiva exata (`plano3d`). Com as placas separadas, as miras, o esqueleto e as pílulas
  das caixas seguem a placa; a linha do alto da `deteccao` e as pílulas VOCÊ e FUNDO do `contorno` saem da
  frente (o alto é das pílulas das camadas); o traço do contorno gira com a placa da pessoa e o tom do
  cenário vai para a placa do fundo limpo. Com a vista do rosto escondida pela cena, a peça não desenha
  nada e as pílulas saem da frente, com aviso: **nenhum texto-molde ("0,00", "X 0000 Y 0000", "QUADRO
  0000") vai para a tela**.
- **Placa que gira:** no `vidro-liquido` inclinado, as miras, o esqueleto e as pílulas seguem a placa só
  de frente, com aviso. O contorno segue sempre (ele mora dentro da vista).

**Campos comuns**
- `t`: quando entra. Padrão: o início da cena + 0,15 s; antes do início da cena, vira o início.
- `ate`: quando sai, em desfoque de 0,2 s, sempre inteiro dentro da cena. Sem `ate` (ou com ele no fim da
  cena), a peça fica até o fim e sai com a cena; numa transição que segura a cena de antes na tela (o
  chicote, a lâmina), continua presa ao vídeo por até 1 s depois do fim (passar disso avisa).
- Com menos de 0,6 s de vida, a peça fica de fora, com aviso.

**`deteccao`**
- `alvos`: `"rosto"`, `"maos"`, `"corpo"`, `"objetos"`. Padrão: rosto, mãos e objetos; alvo do padrão sem
  dado sai com aviso, alvo pedido sem dado é erro. `"corpo"` desenha o esqueleto do busto (ombros, braços e
  tronco, sem linha do meio, que subia pela barba) com a pílula "CORPO NN PONTOS"; entra só quando pedido,
  porque repete a caixa PESSOA.
- `feixe`: `true` (padrão) faz uma linha de luz (miolo branco, halo no `--destaque-gradiente`) varrer o
  quadro de cima a baixo em 0,6 s; cada caixa trava quando o feixe passa pelo meio dela (os cantos chegam de
  1,3x com brilho no acento, a pílula entra de desfocada para nítida). `false`: as caixas travam em fila, 0,1 s
  uma da outra. O que aparece depois trava no quadro em que aparece.
- `contador`: `true` (padrão) ou `{ "y": 320 }`: a linha do alto, com "● VARRENDO · QUADRO 0037" (que vira
  "RASTREANDO") e "OBJETOS NN". O topo padrão é y 250; num reel com HUD, use 320. A linha fica dentro da
  janela da vista; se outro texto ocupa o `y`, ela desce para o primeiro `y` livre fora do rosto, com aviso,
  e sem lugar assim sai da frente enquanto o outro está lá. `false` tira.
- As pílulas mostram "ROSTO 0,96", "MÃO 0,97", "PESSOA 0,91" e o nome do objeto em português. O que o
  modelo achou por menos de 5 quadros (4 na mão) não entra. A pílula que só acharia lugar a mais de 300 px
  da própria caixa (a mão abaixo da zona segura) não aparece, com aviso.

**`maos`**
- `mao`: `"ambas"` (padrão), `"esquerda"` ou `"direita"`, o `lado` do `maos.json`: a mão que aparece à
  esquerda da tela, e depois a mesma mão, mesmo que cruze o meio. MÃO 01 é a esquerda, na primeira cor do
  gradiente; MÃO 02, a direita, na última.
- O desenho: cada osso cresce da junta mais perto do pulso até a outra, em 0,25 s ao todo; as juntas e os
  halos crescem quando o traço chega nelas, e as pontas dos dedos são maiores. A mão que some esmaece em 5
  quadros, parada na última pose; o buraco de até 3 quadros no meio de um trecho é atravessado parado.
- O que a peça ainda limpa do `maos.json`: duas trilhas em cima da mesma mão (caixas com IoU de 0,45 ou mais
  e os pontos a menos de 0,45 palma em média), ficando a que chegou ao trecho sem saltar; e o quadro
  preenchido que desliza de uma mão para outra.
- `rotulo`: `true` (padrão) mostra o cartão "MÃO 01 · 0,97 / 21 PONTOS / X 0307 Y 0903", com as coordenadas
  em pixels da fonte, do lado de fora da mão na tela (longe da outra mão ou, sozinha, longe do meio do
  rosto), ligado ao pulso por uma guia (com o pulso fora do quadro, à base do dedo médio). `false` deixa só o
  esqueleto.

**`contorno`**
- O traço é a máscara engordada menos ela mesma, com um brilho no gradiente por fora, pintado numa tela
  dentro da vista do rosto (herda o enquadre, os dois zooms, a placa e a janela da vista). A varredura de
  0,3 s começa no alto da pessoa: o primeiro quadro já mostra o alto da cabeça.
- **A máscara do traço é a estável:** a mediana de 5 quadros (sem atravessar emenda); buraco de fundo e ilha
  de pessoa menores que 0,35% da máscara viram o que está em volta; o traço apaga onde a máscara muda muito
  de um quadro para o outro (a mão borrada de um gesto rápido) e apaga até a base da zona segura (y 1440, com
  80 px de rampa), onde só mostrava mesa e braço. O tingido usa a mediana, sem tapar as frestas.
- `cor`: `"tinta"` (padrão: o traço branco da referência) ou `"destaque"` (o gradiente). `espessura`: em px
  de saída, de 2 a 8 (padrão 4).
- `rotulos`: `true` (padrão) mostra "CAMADA 01 · VOCÊ", ao lado da cabeça, com a guia até o ombro por fora
  (sem o corpo, ao canto do queixo), e "CAMADA 02 · FUNDO", que entra 0,75 s depois. O FUNDO fica do outro
  lado, no alto (com um HUD, logo abaixo dele); só sem lugar nenhum do outro lado vai para o mesmo lado,
  acima do VOCÊ. Numa vida curta demais, o FUNDO fica de fora, com aviso.
- `lado`: `"esquerda"` ou `"direita"`, onde fica o VOCÊ. Padrão: o lado com mais parede ao lado da cabeça e
  sem texto de outra peça.
- `fundo_ponto`: `[x, y]` em pixels da fonte, para onde a guia do FUNDO aponta. Padrão: um ponto que a
  máscara mostra como cenário em toda a vida da peça, na zona segura, a 50 px ou mais da pílula (de
  preferência ~130), fora de texto e das outras pílulas, com a guia sem cruzar a cabeça. Sem ponto assim, a
  guia fica de fora, com aviso: aí escolha um olhando a `folha-visao.png`.
- `tingir`: `true` (padrão). Quando o FUNDO entra, o cenário ganha o tom do gradiente (com `cor:
  "destaque"`, só escurece) e volta ao natural antes da saída.

**O lugar das pílulas.** Toda pílula e todo cartão fica dentro da zona segura (e da janela da vista, quando
ela é menor que a tela); nunca cobre os olhos, texto, logo ou card de outra peça, outra pílula da visão nem
a legenda de modo de altura fixa; prefere não ficar no corredor da legenda nem em cima das mãos; escolhe um
lugar para a vida inteira e segue a caixa suavizada (média de 5 a 7 quadros, sem atraso); sem lugar livre,
some em desfoque em 3 quadros e volta, com aviso do trecho e do que cruzava; quando um card a empurra, pisca
em vez de saltar. A legenda desvia das pílulas (são texto) e de uma reserva invisível com `data-zona` na
linha dos ombros e no anel na ponta das guias.

**Eventos.** O feixe é `entra` peso 2 com `whoosh`; a caixa que trava no feixe, `acende` peso 1 com `tick`
(as que aparecem depois, sem som); o esqueleto, `entra` peso 2 com `clique` (a mão que volta, peso 1 sem
som); o contorno, `entra` peso 2 com `subida`, o VOCÊ com `pop` e o FUNDO com `tick`; a saída é `sai`. Entre
dois sons destas peças ficam pelo menos 0,15 s.

**Contraste.** Letra branca em vidro escuro (90% a 80% da superfície), ~16:1 no teste.

**Regras para o planejador**
- **Com mãos no peito, a legenda quer subir.** Num trecho com `deteccao`, a linha do alto ocupa o topo:
  para a legenda ficar no peito, use na cena `"legenda": {"desvia_maos": false}`; para liberar o alto, use
  `"contador": false`.
- **Com `maos`, a legenda vai no topo:** `"legenda": {"posicao": "topo"}`. Se a cena é longa, separe numa
  cena só o trecho das mãos (um corte entre duas `rosto-vidro` é invisível).
- **Com o corpo,** a legenda do peito desce para baixo da linha dos ombros, e pode encostar nas mãos.
- **Com o card no alto,** a linha do alto sai da frente enquanto ele está lá: ponha o card fora da vida da
  peça, ou use `"contador": false`.
- **Com HUD no alto,** do lado estreito da cabeça cabem ~160 px: o FUNDO pode ir para o mesmo lado do VOCÊ,
  e um `lado` forçado para o lado estreito deixa o VOCÊ sem lugar. Deixe o `lado` no padrão.
- **Prefira o `rosto-vidro`.** No `painel-rosto`, a janela do rosto é a metade de baixo, quase toda rosto:
  as pílulas ficam entre a costura e os olhos, a linha do alto em geral fica de fora e a pílula da mão
  abaixo da zona segura não aparece.

## Sobreposição `profundidade` · a IA enxerga a profundidade (Onda 2)

O vídeo vira um mapa de profundidade em cor falsa (a técnica 4 do atlas, 9,5 a 10,6 s da referência). A cor
chega em onda, do que está mais perto da câmera (as mãos) até a parede; segura enquanto a pessoa fala (o mapa
é o de cada quadro, então acompanha as mãos); e sai em onda, recuando do fundo para a frente, ou em
desfoque. Em `cena.sobre`, pinta a vista do rosto da cena; em `CENAS.sobre`, a de cada cena que a peça
cruza. Precisa da `visao/` (parte `profundidade`).

```json
{ "tipo": "profundidade", "t": 9.9, "ate": 11.1, "onda": 0.75, "mistura": 0.8, "regua": true,
  "rotulo": "PROFUNDIDADE", "saida": "onda" }
```

| campo | padrão | o que faz |
|---|---|---|
| `t` | o início da cena | Quando a onda sai do que está mais perto. Antes do início da cena, vira o início. A régua entra em foco 0,1 s antes, com o marcador esperando no PERTO; o rótulo, 0,12 s depois. |
| `ate` | — | Quando a saída começa. A saída inteira cabe na cena: um `ate` tarde demais é adiantado. Sem `ate` (ou no fim da cena), o mapa fica até o fim e sai com a cena. A peça precisa de `onda` + 0,2 s de mapa cheio (mais a saída, com `ate`); se não couber, fica de fora, com aviso. |
| `onda` | 0,75 | Os segundos da onda, do mais perto ao mais longe (de 0,3 a 2). A saída em onda leva o mesmo. |
| `mistura` | 0,8 | A opacidade máxima do mapa sobre o vídeo, no mais perto (de 0,3 a 1). O fundo fica com 84% disso, para o cenário continuar legível. |
| `regua` | `true` | A régua de vidro escuro, 144 px de largura: a barra da paleta, PERTO em cima, LONGE embaixo e o marcador, ao lado da cabeça. `false` tira. `{ "lado": "esquerda", "y": 560, "h": 480 }` muda o lado, o topo e a altura (`h` de 300 a 900); `y` e `h` dados valem como estão, e a peça avisa se tiram o lugar da legenda. |
| `rotulo` | `"PROFUNDIDADE"` | O título da régua, numa pílula de vidro em FC Mono, empilhada 14 px acima dela. `false` tira. |
| `y` | logo acima da régua | O topo da pílula do rótulo. |
| `marcador` | `"PESSOA"` | O nome do marcador quando ele assenta na pessoa (não é "VOCÊ": no reel, "você" é quem assiste). `false` tira o nome, e o marcador para no LONGE. |
| `saida` | `"onda"` | `"onda"`: o mapa recua do fundo para a frente, e as mãos somem por último. `"desfoque"`: o mapa, a régua e o rótulo desfocam e somem em 0,25 s. |

**Onde a régua e o rótulo moram:** ao lado da cabeça, onde a legenda nunca vai. Acima da cabeça e entre o
queixo e as mãos são os lugares para onde a legenda foge das mãos (`MOTOR.md` 3.2); um vidro ali deixa a
legenda por cima das mãos, que são o centro do efeito. A faixa vai do alto do cabelo + 40 px até o queixo
− 2 px, medida na montagem em todos os quadros da vida da peça (o rosto pelo `rosto.json`, o alto pela
`pessoa.caixas` do `visao.json`), e a régua fica centrada nela, com até 520 px. Na lateral, encosta na zona
segura; quando a borda da janela do vídeo cai na coluna dela (a placa do `vidro-liquido`), ela vai para
dentro da janela, a 24 px da borda.

**A onda.** A frente parte exatamente do pixel mais perto do quadro e anda com metade sine.inOut e metade
sine.out. A ordem é sempre a da profundidade: perto primeiro (no teste, as mãos acendem em ~0,1 s, a cabeça e
o corpo até ~0,35 s, a parede fica com a segunda metade). O andamento é alisado dentro de cada camada (a
pessoa e o fundo), para a frente cruzar cada uma como uma faixa larga; a cor de cada pixel continua sendo a
profundidade dele. A frente é uma linha fina (miolo branco, halo no `--destaque-gradiente`) com um clarão
atrás; ela só risca onde a profundidade muda de verdade: na pessoa, o contorno da cabeça e a mão na frente
da camiseta; no fundo, a quina da prateleira, o neon, a cadeira. Na superfície lisa (rosto, peito, parede
lisa) fica só o clarão.

**A cor** (paleta de dado, só desta visualização): 1, o mais perto, âmbar #f7a711; 0,75, o acento
(`var(--destaque)`); 0,45, roxo #420097; 0, a superfície da marca com 30% do roxo. Entra em sobreposição
(overlay) com a luz do quadro, então o rosto, a barba e a textura continuam legíveis.

**A honestidade.** A profundidade é relativa: a peça nunca mostra metro, a régua diz só PERTO e LONGE. A barra
é a legenda da paleta (enche até a frente da onda e esvazia quando ela recua). O marcador anda com a frente e,
com a onda no fundo, assenta na mediana medida da pessoa naquele quadro (`visao.json` →
`profundidade.pessoa`) e a segue quadro a quadro.

**Onde o mapa mora.** Dentro da vista do rosto, irmão da imagem do quadro: herda o enquadre, os dois zooms,
a placa inclinada do `vidro-liquido` (perspectiva exata), o canto redondo e as transições. No
`vidro-liquido`, a cópia do aro recebe a mesma pintura. No `camadas`, o mapa vai em você recortado (com a
máscara do quadro) e no vídeo vivo da placa de trás; com as placas separadas, fica só em você, girando com a
placa, porque o fundo limpo é uma foto montada, sem profundidade medida: a peça avisa que ali a onda não
chega à parede.

**Regras para o planejador**
- Use numa cena com rosto na tela (`rosto-vidro`, `vidro-liquido` com rosto). Numa cena sem `vistaRosto`, a
  peça fica de fora, com aviso; no reel inteiro, a peça que cruza cena sem rosto avisa (ali aparecem só a
  régua e o rótulo).
- Uma peça por vez na mesma cena. Deixe a régua e o rótulo no padrão; só dê `regua.y`, `regua.h` ou `y`
  sabendo para onde a legenda vai fugir das mãos.
- Ponha a onda num gesto: o efeito é a mão acendendo primeiro. Mão parada no colo dá pouco.
- A peça avisa, uma vez cada e com o instante, quando o vidro da régua ou do rótulo cobre outro texto ou o
  miolo do rosto, fica sob a legenda, ou ocupa o lugar para onde a legenda fugiria de uma mão (essas duas
  últimas só no render em sequência). A régua e o rótulo têm `data-zona`.
- `"atras": true` não muda o mapa (ele já pinta a pessoa): só a régua e o rótulo ficam atrás dela, com aviso.

**Eventos.** A onda: `entra` peso 2 com `subida`; a onda que chega ao fundo: `acende` peso 1 com `tick`; a
régua e o rótulo: `entra` peso 1 sem som; a saída: `sai` peso 2 sem som.

**Contraste.** Letra branca sobre vidro escuro fechado (84 a 72% da superfície): 13,05:1 no pior texto do
teste.

**Determinismo e custo.** O mesmo instante dá o mesmo quadro, pixel a pixel, no render em sequência, no
`--quadro`, em ordem embaralhada e de trás para a frente. O PNG da profundidade de cada quadro entra como
fonte do motor, e o render espera ele decodificar antes dos ganchos. No corte de teste (576 x 1024), o
`M.render` passa de 4 a 6 ms sem a peça para 20 a 25 ms com ela (mediana); num 1080 x 1920 a pintura tem 3,5
vezes mais pixels (estimado, não medido).
