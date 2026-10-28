# O plano de cenas (Fábrica 2.0)

Com `"motor": "2.0"` no `setup.json`, o plano do corte deixa de ser só o painel de cima e passa a ser o
reel inteiro: uma sequência de cenas, cada uma com um **modo**, o conteúdo dela, os tempos e a
transição de entrada. O arquivo é `materiais-de-trabalho/corte-NN/cenas.json`, e o formato exato, com
cada campo, é o contrato do motor: `skills/produzir/motor/MOTOR.md`, seções 3 a 5.
Este arquivo diz **como escolher**; o MOTOR.md diz **como escrever**.

O plano é escrito depois do `editar_fala.py`, nos tempos do `palavras-corte.json` (a fala já limpa),
nunca nos tempos do vídeo bruto. Para começar, pegue o modelo do ângulo da fala em
`MODELOS-DE-CENAS.md` (grátis × pago, lista de N, notícia, tutorial de tela, opinião); quando o corte
veio de uma pauta, o `cenas-rascunho.md` da pasta já traz o modelo aplicado ao roteiro.

---

## 0. Estilos de produção

O criador escolhe o estilo de cada vídeo (um ou mais), e o plano começa por ele: `"estilo": [...]` no
`cenas.json`, e só as peças que o estilo permite (a tabela está no `MOTOR.md` do criador, seção 3.3, e
o `compor.py` avisa o que escapar).

- **Essencial**: o rosto conduz. Cards de vidro com número, selo e lista nas enumerações; no máximo
  5 transições por minuto, quase todas corte seco. É o estilo de quando a fala é forte sozinha.
- **Liquid Glass**: abra e feche blocos com a placa de vidro (`vidro-liquido` com `entra` e `mergulha`),
  a tese numa `pilha` e as viradas com `inclinada` e `mergulho`. O HUD de capítulos organiza vídeos com
  partes.
- **Imagens**: cada coisa concreta da fala vira imagem (`imagem-cheia` com foto livre, `logo-volume`,
  `manchete` com print) e as trocas usam `clarao`, `mascara` e `zoom-desfoque`.
- **Tela cortada / visão**: o efeito é a IA enxergando você. Texto `atras` da cabeça, `deteccao` com
  feixe na abertura, `profundidade` numa palavra de impacto, `contorno` quando fala de você, `maos` no
  gesto, e a `camadas` (tela cortada 3D) num momento-chave, com a palavra ou o logo entre você e o fundo.
  Só serve para gravação de frente com a câmera parada; gravação de tela não tem com o que trabalhar.
- **Completo**: os quatro juntos, mais os mocks (transcrição, prompt, timeline) e o CTA com comentário e
  DM. Dosar: um efeito grande por ideia, nunca dois disputando o mesmo segundo.

Combinar é somar o que cada um permite (Liquid Glass + Imagens, por exemplo). O ritmo do estilo não
muda a velocidade da fala: ela é pergunta à parte, decidida pelo criador.

## 1. Uma cena por ideia

Uma cena dura enquanto a fala sustenta a mesma ideia. A troca de cena acompanha a mudança de ideia,
não o relógio. As fronteiras caem no começo de uma palavra (a palavra que muda de assunto), e de
preferência logo depois de um respiro.

| trecho | duração de cada cena | dentro da cena |
|---|---|---|
| abertura (os primeiros 5 s) | 1,5 a 3 s | algo muda a cada 1 a 2 s |
| o resto | 4 a 8 s | algo muda a cada 2 a 3 s: um elemento entra, um número corre, algo acende, zoom |

Duas trocas grandes (cena nova com transição) nunca a menos de 1,5 s uma da outra: a pessoa não lê
nada. Nada fica parado mais de 2,5 s: o gate de ritmo reprova.

## 2. Qual modo, para qual fala

A escolha sai do que a fala está fazendo naquele trecho, e o `INVENTARIO.md` já disse a rota de cada
coisa concreta nomeada. A tabela casa as duas coisas:

| a fala está... | modo | por quê |
|---|---|---|
| abrindo com a tese, provocando, opinando | `tipografia` ou `rosto-vidro` | é onde a pessoa decide se fica: a frase grande ou o rosto com o primeiro objeto |
| dando um número, citando uma fonte | `rosto-vidro` com elemento `numero` e `fonte` | o número é o herói, em escala de título, correndo até o valor |
| nomeando uma ferramenta ou marca (rota logo) | `rosto-vidro` com `selo` ou `logo` | o logo de verdade do acervo; sem logo, a palavra |
| mostrando algo acontecendo numa tela (rota tela) | `tela-bolha` | a prova é a tela; o rosto vira bolha |
| citando uma pesquisa, notícia, comunicado oficial | `manchete` | o print da fonte com o trecho marcado é a prova |
| usando uma metáfora forte (museu vazio, megafone) | `imagem-cheia` | a imagem é a ideia; de 1,5 a 3 s |
| comparando duas coisas (pago × grátis, A × B) | `lado-a-lado` | o contraste é o objeto; o vencedor acende |
| listando (N ferramentas, passos) | `lista` | os itens numerados empilham e o da vez acende |
| fechando: a frase-tese e a chamada (comenta PALAVRA) | `tipografia` | a frase é a legenda |
| abrindo um capítulo de um método (B, U, I, L, D; passo 1, 2, 3) | `painel-rosto` com blocos `sigla` e `titulo` | a tela dividida: o rosto grande embaixo e o capítulo aceso em cima |
| explicando um processo, um fluxo, um atalho | `painel-rosto` com blocos `fluxo` e `teclas` | cards com ícone que entram no tempo da fala, ligados por seta |
| virando a página: a abertura, a troca de assunto, a volta para você depois de uma prova | `vidro-liquido` | o Liquid Glass: a cena numa placa de vidro que entra inclinada, gira e mergulha de volta na tela cheia |
| mostrando um print ou um trecho da tela como objeto | `vidro-liquido` com `fonte: "imagem"` ou `caixa` | o print vira uma placa de vidro com espessura, e não um retângulo chapado |
| separando duas coisas: a pessoa e o contexto, o que é seu e o que é do mundo, a frente e o fundo (precisa da visão do corte) | `camadas` | a tela se parte em 3D: você numa placa, o cenário em outra, e a palavra no meio |
| apontando o tempo todo para um objeto: "essa linha", "esse arquivo", "digita isso" | `mundo` (MOTOR.md 4.14) | o objeto real ocupa a tela e uma câmera calma passeia por ele; você entra como respiro, num card com a cabeça saindo pela borda. Um mundo cobre várias cenas seguidas, uma por superfície (`quadro`, `pip`, `rosto`, `tela`), com a câmera presa às palavras da fala |

Um reel típico usa de dois a quatro modos. Mais que isso vira vitrine de efeitos. Dois reels seguidos
do mesmo perfil não abrem no mesmo modo.

**Mostre a ideia, não a frase** continua valendo (regra C do `BEAT-SHEET.md`): a legenda já carrega
a fala. Um elemento `texto` que repete o que está sendo dito é eco. Prefira `numero`, `logo`, `selo` com a
fonte, `imagem` e os modos de prova. O `texto` serve para nomear uma ideia que a fala não diz com
todas as letras.

### Tela dividida e bolinha, alternando

O reel não fica num jeito só de mostrar o rosto. A **tela dividida** (`painel-rosto` com `blocos`) põe o
rosto grande embaixo e um painel vivo em cima: é o momento de conversa, de capítulo, de explicação com
cards e ícones. A **bolinha** (`manchete`, `tela-bolha`) põe a prova em primeiro plano e o rosto
pequeno. Alterne os dois ao longo do corte, com imagem cheia e tipografia entre eles, e deixe sempre
alguma coisa entrando ou acendendo: card, ícone, logo, tecla. Gravação de tela com a webcam num canto
também vira tela dividida: `"rosto": {"caixa": [x, y, w, h]}` com a janela da webcam. O exemplo
completo é o reel do BUILD (`projetos/framework-build/materiais-de-trabalho/corte-01/cenas.json`).

### As sobreposições da 3.0 (por cima de qualquer modo)

Com a 3.0, boa parte do que antes era cena virou **sobreposição** (`cena.sobre` ou `CENAS.sobre`, contrato
em `skills/produzir/motor/SOBREPOSICOES.md`). O rosto continua na tela e a ideia entra por cima:

| a fala está... | sobreposição |
|---|---|
| dizendo a tese ou o contraste da frase ("não precisa saber editar, só dirigir") | `pilha`, com `risco` no que é negado e `colchetes` no que fica |
| dizendo uma palavra com cara (corte, 3D, museu, erro) ou um número | `palavra` com o efeito que é o significado (`glitch`, `extrusao`, `conta`...) |
| nomeando uma ferramenta | `logo-volume` com o logo oficial, perto da cabeça ou das mãos |
| mostrando o processo (a fala virando texto, o pedido, a edição) | `transcricao`, `prompt`, `timeline` |
| chamando para o comentário | `comentario` com a palavra e, 0,4 s depois, a `dm` |
| organizando o reel em partes | `hud` no `CENAS.sobre`, um capítulo por bloco de ideia |

Regras que evitam reprovação: com `hud`, nada de conteúdo do topo acima de y 320; uma `pilha` por vez e
de no máximo duas linhas (com mais, ela encolhe e o acento reprova no contraste); no CTA com rosto grande,
`"legenda": {"posicao": "topo"}` na cena. A legenda da 3.0 é `"estilo": "revela"`, com `"posicao":
"peito"` como padrão do reel. O reel completo de exemplo é o `projetos/teste-onda-1/materiais-de-trabalho/corte-11/cenas.json`.

### A IA enxergando a cena (Onda 2)

A Onda 2 mostra a máquina vendo o vídeo: o texto que fica atrás da cabeça, a tela que se parte em
camadas, a profundidade em cor, os 21 pontos da mão, as caixas de detecção. Tudo sai da **visão do
corte** (`visao.py`, `MOTOR.md` 2.6), que o criador roda depois do `rosto.py`. Contrato de cada peça em
`SOBREPOSICOES.md`; do modo `camadas`, em `MOTOR.md` 4.11.

| a fala está... | peça | por quê |
|---|---|---|
| abrindo com a tese em duas palavras ("A EMPRESA / AI FIRST") | `pilha` ou `palavra` com `"atras": true` | o título fica atrás da cabeça: é a abertura da referência, a pessoa na frente da manchete |
| falando de rastrear, enxergar, detectar, "a IA vê" | `deteccao` | o feixe varre e a mira trava no rosto, nas mãos e nos objetos, com a confiança medida |
| falando de profundidade, distância, perto e longe, "o que está na frente" | `profundidade` | a cor chega em onda das mãos até a parede; a régua diz PERTO e LONGE, nunca metro |
| gesticulando ao explicar um processo, contando nos dedos, "com as mãos" | `maos` | o esqueleto de 21 pontos cresce sobre a mão; o gesto vira dado |
| falando de recorte, camada, "você e o fundo", separar o assunto do contexto | `contorno` | o traço revela a pessoa, e as pílulas VOCÊ e FUNDO nomeiam as camadas |
| virando o argumento em três dimensões: o que fica na frente, o que fica atrás, a palavra no meio | modo `camadas` com a palavra em `cena.sobre` e `"atras": true` | a palavra mora entre você e a parede, e a cabeça passa por cima dela quando as placas se juntam |
| citando uma ferramenta com a mão aberta, "isto aqui" | `logo-volume` com `"segue": "mao"` | o logo flutua na palma, com o pedestal holográfico |
| citando uma ferramenta sem gesto | `logo-volume` com `"segue": "cabeca"` e `desvio` para o lado | a placa anda com a cabeça, ao lado dela, no alto |

**A linguagem da referência.** Uma peça de visão por cena, e no trecho exato em que a fala fala daquilo:
a detecção quando ela diz "rastreia", a profundidade quando diz "profundidade". No reel de
demonstração, cada uma dura de 1,3 a 3,6 s e sai antes da próxima ideia; duas peças de visão ao mesmo tempo viram painel de laboratório. O texto
que aparece é dado medido (a confiança, os pontos, PERTO/LONGE), letra branca em vidro escuro, mono e
pequena; o destaque é o gradiente da marca nos traços, nunca atrás de letra. Os capítulos do HUD podem
nomear a técnica ("02 · PROFUNDIDADE"), e o reel de demonstração com todas elas é o
`projetos/teste-onda-1/materiais-de-trabalho/corte-20/cenas.json`.

**Regras que evitam falha:**
- **A gravação manda.** Tudo isto pede a pessoa filmada de frente, em plano médio, com a câmera parada.
  As mãos só servem de palco quando sobem abertas até o peito ou acima: com a mão no colo, a `maos`
  desenha fora da zona segura e o `logo-volume` na mão flutua sem pedestal. Antes de planejar uma peça na
  mão, olhe o `maos.json` e a `folha-visao.png` no trecho: no teste, as mãos sumiram justo na palavra
  "Salesforce", e o logo foi para a cabeça.
- **O fundo das camadas é inventado onde a pessoa nunca saiu** (quase metade da parede no teste): de perto
  ele repete blocos da própria parede. Peça ao criador, na pauta, de 3 a 5 s do cenário vazio no fim da
  gravação; sem isso, deixe as placas separadas por pouco tempo.
- **Texto atrás de você:** a palavra-chave fica acima do cabelo; só a base da última linha encosta na
  cabeça (10 a 25% da caixa). Mais de 35% coberto por 0,3 s reprova no contraste. Sem zoom de ênfase
  durante a peça (ele sobe a cabeça), e nada de `atras` no `CENAS.sobre` cruzando cena sem rosto ou o
  `camadas`: ponha a peça em `cena.sobre` da cena com rosto.
- **`camadas`:** a palavra do meio cabe no vão até uns 800 px de largura; deixe 0,25 s entre o `separa`
  e o pop de uma peça (senão o pop some no áudio); `logo-volume` no meio sai antes do `gira`; `metros` só
  com a medida de quem gravou. A legenda fica fixa em y 1340 nesta cena.
- **Com `maos`, a legenda vai no topo** (`"legenda": {"posicao": "topo"}` na cena). Com `deteccao`, a linha
  do alto ocupa o topo: use `"contador": false` ou `"legenda": {"desvia_maos": false}`. Com HUD, a linha
  do alto vai em `{"y": 320}`.
- **A legenda foge das mãos sozinha** quando a visão existe: nos gestos, o alto é dela. Card e selo de texto
  vão nos trechos de mãos quietas; nos gestos, o adesivo ao lado da cabeça.
- **`contorno` com HUD:** deixe o `lado` no padrão; do lado estreito da cabeça cabem ~160 px.
- **`profundidade`:** uma por cena, numa cena com rosto, e com a onda caindo num gesto. A peça nunca mostra
  metro; nenhum texto do plano pode prometer distância em metro tirada dela.
- **Nunca escreva número de confiança, coordenada ou distância no plano:** a peça mostra o que o modelo
  mediu, e fica sem número quando não há medida.

### O 3D de verdade (Onda 3)

No estilo Tela cortada e no Completo: `nuvem` quando a fala é sobre dados, leitura do mundo, "a IA vê";
`malha` quando é sobre estrutura, sistema, reconstrução; `objeto3d` `texto` na palavra-tese (atrás da
cabeça, na abertura, como o título da referência) e `objeto3d` `logo` na ferramenta nomeada. Uma peça 3D
grande por vez, com 1,5 a 6 s de vida; as palavras e números da fala vão por cima delas com `palavra` e
`atras`. O plano completo de exemplo é `projetos/teste-onda-1/materiais-de-trabalho/corte-40/cenas.json`.

### Logo e objeto na tela: o adesivo

Quando a fala nomeia uma ferramenta numa cena de rosto, o logo oficial em cor entra como **adesivo**
do `rosto-vidro`, na palavra do nome: `"acervo": "claude-code-logo"` na fila de cima. O acervo em cor
está em `componentes/marcas/` (91 marcas de tecnologia; a lista e a folha `_amostra.png` estão no
`LEIA.md` de lá); marca que não está lá entra pela
silhueta do `logos/` num `selo` ou `logo`, ou pelo `baixar-marca.py` antes do plano.

Quando a fala nomeia um objeto ("um megafone", "um robô"), o recorte do objeto entra ao lado da
cabeça: `buscar-imagem.py <objeto> --sem-fundo` traz a foto livre já recortada, e o adesivo vai com
`"imagem": "assets/<objeto>-01-sem-fundo.png"`. Um adesivo por vez, e só na palavra que nomeia a
coisa: adesivo demais vira álbum de figurinha.

## 3. A abertura é o trailer

A regra D do `BEAT-SHEET.md`, aplicada a cenas:

- a primeira cena é `tipografia` ou `rosto-vidro`;
- o primeiro elemento grande entra até 1,0 s;
- há pelo menos três mudanças antes dos 5 s;
- a ideia mais cara do corte (o número de impacto, a imagem mais forte) vai aqui.

## 4. Transições

`corte` é o padrão e deve ser a maioria. Transição com efeito é tempero: o gate avisa acima de 8 por
minuto.

| transição | use quando |
|---|---|
| `corte` | a próxima cena continua o mesmo assunto |
| `lamina` | muda o modo e muda o assunto |
| `bolha-encolhe` | do rosto para `tela-bolha` ou `manchete` (a cena nova precisa ter bolha) |
| `bolha-expande` | de `tela-bolha` ou `manchete` de volta para o rosto |
| `zoom-desfoque` | entrar num detalhe |
| `chicote` | passar para o próximo item de uma sequência |
| `mascara` | revelar uma imagem ou um print |
| `clarao` | a virada do argumento e a chamada final; no máximo duas vezes por reel |
| `desfoque` (3.0) | a troca suave de assunto: a cena desfoca e a nova chega do desfoque (0,32 s antes do início) |
| `inclinada` (3.0) | a cena nova chega como placa inclinada e se endireita (0,5 s depois do início): abre um bloco |
| `mergulho` (3.0) | a câmera mergulha na cena que sai (numa placa, numa tela): de dentro dela para a próxima |

As três da 3.0 têm duração mínima de cena: `inclinada` na entrada e `mergulho` na saída pedem ~1,1 s;
`inclinada` + `desfoque`, ~0,82 s; `desfoque` + `mergulho`, 0,6 s. Plano que não respeita é recusado.

## 5. Tempos

- Elemento que aparece "na palavra": `t` = início da palavra − 0,2 s. O movimento termina em cima dela.
- `acende` no início da palavra que aponta para o elemento.
- Número que conta: entra 0,1 s antes da palavra do número, e a contagem dura de 0,6 a 0,9 s.
- Zoom de ênfase (`zoom`): nas duas ou três palavras mais fortes do corte, `escala` de 1,06 a 1,12.
  Nunca em cenas seguidas.
- `legenda.enfase`: nomes de ferramenta e as palavras que carregam a tese. Números já entram sozinhos.
- `legenda.estilo`: na 3.0, `revela` no reel todo, com `"posicao": "peito"` (a palavra aparece quando é
  dita, logo abaixo do queixo, e foge sozinha de card e texto). Os estilos da 2.0 continuam valendo:
  `palavra-acesa`; `pop` só na abertura em `rosto-vidro`; `caixa` quando o fundo for agitado demais
  (`imagem-cheia` com foto cheia de detalhe). Fundo claro sozinho não pede caixa: o contorno da legenda
  já separa a letra, e é contra ele que o gate mede.
- A altura da legenda (`posicao` ou `y` na cena) só muda na troca de cena: não quebre uma cena no meio de
  uma frase só para mudar a legenda de lugar, porque a linha salta. Prefira uma cena só e deixe o
  `revela` desviar das peças.
- `vencedor` do `lado-a-lado`: pelo menos 0,6 s antes do fim da cena. A barra leva 0,34 s e o
  vencedor precisa ficar aceso na tela antes da troca.
- Nada de `acende`, `vencedor` ou marca nova nos 0,4 s antes de uma transição com efeito: o olho não
  vê o que acontece dentro da janela dela.
- Abertura em `tipografia`: a primeira palavra e as de `destaque` contam como elemento grande, então a
  regra do 1,0 s se cumpre se a primeira palavra cair antes dele.

## 6. Armadilhas que o primeiro reel completo mostrou

- **Rótulo de marca em print.** Na `tela-bolha` e na `manchete`, o rótulo vai acima do contorno; se a
  marca está na primeira linha visível, ele desce e cobre a linha de baixo. Deixe contexto acima da
  marca no `recorte` ou na `tela.caixa`.
- **Recorte frouxo.** Linha em branco dentro do `recorte` vira faixa branca no card. Recorte justo no
  trecho citado, com uma linha de contexto em cima.
- **Imagem no `rosto-vidro`.** O card encolhe para terminar acima da testa. Foto paisagem cabe; foto
  retrato vira uma faixa estreita. Foto retrato vai para `imagem-cheia`.
- **Foto pequena.** Em `imagem-cheia` a foto cobre 1080 x 1920; com menos de uns 900 px de largura
  útil depois do recorte, ela borra. Foto pequena vai num card do `rosto-vidro`.
- **Texto cinza sobre o rosto.** Nos cards do `rosto-vidro`, o vidro é escuro e todo texto é branco:
  cinza suave e acento sobre a parede clara não passam no contraste.
- **Muitas transições.** Um reel que usa todas passa de 8 por minuto, e o gate avisa. Em produção, três
  ou quatro por reel bastam.

## 7. Exemplo (o reel de teste do AI First × Data First)

O plano inteiro, com os oito modos e as sete transições, aprovado nos nove gates, está em
`EXEMPLO-CENAS.json`, nesta pasta. O começo:

```json
{
  "versao": 1, "fps": 30, "duracao": 41.567, "fonte": { "video": "fala.mp4" },
  "videos": { "painel": "painel-c10.mp4" },
  "legenda": { "estilo": "palavra-acesa", "enfase": ["Salesforce", "Gartner"] },
  "cenas": [
    { "id": "c1", "modo": "tipografia", "inicio": 0.0, "fim": 1.4,
      "conteudo": { "fundo": "rosto", "destaque": ["Cuidado!"] } },
    { "id": "c2", "modo": "imagem-cheia", "inicio": 1.4, "fim": 3.4, "entrada": { "transicao": "clarao" },
      "conteudo": { "imagem": "assets/megafone.jpg", "movimento": "aproximar", "foco": [0.5, 0.42] } },
    { "id": "c3", "modo": "manchete", "inicio": 3.4, "fim": 8.95, "entrada": { "transicao": "bolha-encolhe" },
      "conteudo": { "imagem": "assets/salesforce-pagina.png", "recorte": [470, 4560, 1290, 680],
        "fonte": "Salesforce · novembro de 2025",
        "marcas": [ { "t": 5.7, "ate": 7.45, "caixa": [1238, 4878, 122, 54], "tipo": "contorno" },
                    { "t": 7.5, "ate": 8.95, "caixa": [570, 4930, 330, 46], "tipo": "sublinhado", "rotulo": "não confiáveis" } ] } },
    { "id": "c4", "modo": "rosto-vidro", "inicio": 8.95, "fim": 13.25, "entrada": { "transicao": "bolha-expande" },
      "zoom": [ { "t": 12.68, "escala": 1.08, "segura": 0.5 } ],
      "conteudo": { "elementos": [
        { "id": "n89", "tipo": "numero", "valor": 89, "sufixo": "%", "rotulo": "já viu a IA errar em produção",
          "fonte": "SALESFORCE · 2025", "t": 8.95, "ate": 12.05, "acende": [10.77] },
        { "id": "conviccao", "tipo": "selo", "texto": "repete com convicção", "t": 12.12 }
      ] } }
  ]
}
```

## 8. Antes de mandar renderizar

1. As cenas cobrem o corte inteiro, sem buraco nem sobreposição, e a última termina em `duracao`.
2. A abertura cumpre a seção 3.
3. Nenhum trecho fica mais de 2,5 s sem mudança.
4. Toda imagem tem origem e licença no `assets/CREDITOS.md`; todo logo existe no acervo.
5. Cada `bolha-encolhe` entra numa cena com bolha; cada `bolha-expande` sai de uma.
6. Rode `compor.py --quadro` em três instantes (abertura, uma transição, o fim) e olhe antes do render
   completo. É barato, pega o erro grosso e mostra os avisos do motor da montagem.
7. Com as peças da 3.0: as durações mínimas das transições novas (seção 4), uma `pilha` por vez e com
   pelo menos ~1,2 s de leitura, o CTA (comentário e DM) antes do último segundo e meio, e os avisos do
   motor do render inteiro lidos e resolvidos.
8. Com as peças da Onda 2: a `visao/` existe para este `fala.mp4` (o criador roda o `visao.py`), a
   `folha-visao.png` foi olhada, e o `--quadro` no pior instante de cada texto atrás de você e de cada
   gesto mostra a palavra inteira acima do cabelo e a legenda fora das mãos.
