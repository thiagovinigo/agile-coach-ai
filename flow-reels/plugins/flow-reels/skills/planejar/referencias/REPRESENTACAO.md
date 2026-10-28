# A lei da representação

Este arquivo é a lei do **passo 0** da ordem de trabalho, o inventário visual, e manda no campo
`peca` do beat-sheet. A ordem de trabalho inteira está na `SKILL.md` desta skill.

## O defeito que ela mata

O acervo sabe desenhar móvel genérico: card, chip, seta, cronômetro, barra, tile, rótulo, título.
Sem regra, toda coisa concreta que a fala nomeia vira retângulo com o nome escrito dentro, e o
painel passa o corte inteiro repetindo a palavra que a legenda já carrega. Falou em aplicativo de
mensagem, saiu um card escrito o nome do aplicativo. Isso não é preguiça de quem planeja: é o único
desenho que ele tinha à mão.

A matriz **não substitui o desenho abstrato**, que continua sendo o certo para ideia abstrata. Ela
para de aplicar desenho abstrato a coisa concreta.

---

## 1. As quatro rotas

| rota | o que é | quando |
|---|---|---|
| **logo** | o logo de verdade do acervo, sozinho ou dentro de um `tile-de-logo` | a fala só nomeia a ferramenta, e basta reconhecer qual é |
| **mock** | a forma da interface desenhada nos tokens da marca, com o logo real embutido quando houver | o beat precisa da forma, não só da identidade |
| **tela** | a gravação do próprio vídeo, recortada e anotada, sob a lei da seção 9 do `PADRAO-VISUAL.md` | a fala afirma um fato que quem assiste precisa acreditar que aconteceu |
| **palavra** | nada visual, o nome dito resolve o beat | nenhuma das três anteriores serve |

Ideia abstrata (economia de tempo, simplicidade, processo, escala) não entra nesta tabela: ela é
**desenho abstrato** com as peças de sempre, e a matriz não se aplica.

**No motor 2.0** duas rotas se somam, para coisa concreta que **não é interface**:

| rota | o que é | quando |
|---|---|---|
| **foto** | foto de banco livre, licença conferida (`componentes/imagens/buscar-imagem.py`), no `imagem-cheia` ou num card | a fala nomeia um objeto, um lugar, uma cena do mundo |
| **adesivo** | o logo oficial em cor (`componentes/marcas/`) ou o objeto recortado (`tirar-fundo.py`), ao lado da cabeça ou na fila de cima do `rosto-vidro` | a fala nomeia a ferramenta ou o objeto e o rosto continua na tela |

A regra 5 continua valendo: foto de banco nunca faz papel de tela de programa.

O `PADRAO-VISUAL.md` citado aqui e nas seções seguintes é o da produção, em
`skills/produzir/referencias/PADRAO-VISUAL.md`. Ele é lei de lá, e aqui é só
consultado.

---

## 2. A ordem de decisão

Para cada coisa concreta nomeada na fala, nesta ordem, parando no primeiro sim.

### Passo 0. É concreta?

Coisa com nome e forma: produto, ferramenta, plataforma, interface, arquivo, número, resultado. Se
for ideia, a rota é desenho abstrato e a decisão acaba aqui, sem linha no inventário.

### Passo 1. O beat pede crença ou reconhecimento?

- **Crença:** a fala afirma um fato. "ele devolve os três arquivos", "custa vinte dólares por mês",
  "clica aqui e instala em trinta segundos". Vá para o passo 2.
- **Reconhecimento:** a fala só nomeia. "usando o editor de projetos", "para o Instagram e o
  LinkedIn". Vá para o passo 3.

### Passo 2. O caminho da crença

Três perguntas. **As duas primeiras são do inventário, a terceira não é**, e a diferença importa
porque elas não se respondem no mesmo momento.

1. a fonte mostra isso, num instante utilizável?
2. a região sobrevive ao recorte da 9.4 do `PADRAO-VISUAL.md`? Fator maior ou igual a 1,0, e texto
   de interface legível depois da escala.
3. cabe no orçamento de tela do corte?

**As duas primeiras se respondem olhando o arquivo**, e o inventário responde as duas. Dois sins, a
coisa fica registrada como **tela candidata**, com o instante e a região anotados. Qualquer não já
decide ali: vira **mock**, nunca palavra, porque o beat continua precisando mostrar e o que muda é
só quem desenha.

**A terceira não tem como ser respondida no inventário**, e é um erro pedir isso. O orçamento é por
corte, e no passo 0 corte nenhum existe ainda: os ganchos só são escolhidos depois. Então ela é
respondida no beat-sheet, quando o corte já tem duração e já se sabe quantas janelas ele quer.

Ou seja, a rota `tela` se fecha em dois tempos:

| momento | quem decide | o que sai |
|---|---|---|
| inventário, passo 0 | perguntas 1 e 2, olhando a fonte | `tela candidata`, com instante e região, ou `mock` |
| beat-sheet, por corte | pergunta 3, o orçamento | confirma `tela`, ou degrada para `mock` |

Candidata que não couber no orçamento **não some do inventário**. Ela continua registrada, porque o
corte seguinte pode ter espaço para ela, e porque a razão da degradação é do corte, não da coisa.

O número do orçamento vive em `PADRAO-VISUAL.md` seção 9.2 e é de quem produz. Aqui ele só é
consultado.

### Passo 3. O caminho do reconhecimento

- o logo existe no acervo ou dá para baixar, e identificar é tudo que o beat pede: **logo**;
- o beat precisa da forma e não da identidade (uma conversa, uma busca, um feed, uma caixa de
  entrada, uma janela de programa, uma linha de comando): **mock**, com o logo de verdade dentro;
- a coisa é concreta mas não tem marca nem forma de interface, como um número, uma duração ou uma
  quantidade: **desenho abstrato** com as peças de sempre, cronômetro, barra, chip. Esta linha não é
  exceção à matriz, é a frase de abertura dela: o desenho abstrato continua sendo o padrão de tudo
  que não é interface nem marca;
- nada disso: **palavra**.

---

## 3. As cinco regras transversais

### Regra 1, a que mais muda o resultado: olhe o quadro antes de desenhar

**Antes de desenhar um mock de uma ferramenta que aparece na fonte, extraia um quadro e olhe.**

Desenhar de memória é o que produz interface genérica, e interface genérica é o mesmo defeito do
card com texto, só que com mais bordas. A memória entrega "uma janela com uma barra lateral". O
quadro entrega o que está mesmo lá: quantas seções a coluna tem, se o conteúdo é uma lista ou um
bloco de texto, onde fica o botão que a fala aponta, que caixa abre por cima quando ele clica.

```
mkdir -p projetos/<video>/materiais-de-trabalho/inventario
ffmpeg -y -ss <segundo em que a fala nomeia a coisa> -i <fonte> -frames:v 1 \
  projetos/<video>/materiais-de-trabalho/inventario/<coisa>-<t>.png
```

O `mkdir` não é enfeite: o ffmpeg não cria pasta, e sem ela o comando termina em
`Conversion failed!` sem gravar quadro nenhum.

Um quadro por coisa que vai para mock ou tela, tirado no instante em que a fala fala dela. Olhe o quadro
e escreva, na coluna de observação do inventário, **o que você viu e não teria adivinhado**. Se a
observação não tem nada além do que você já sabia de cabeça, você não olhou, você conferiu.

Três coisas que esse olhar costuma revelar, e que mudam o plano:

- **a moldura da gravação.** Muita fonte tem faixa de marca em cima, tarja embaixo e o encarte da
  webcam num canto. Nada disso pode entrar no recorte de tela, e nada disso é da ferramenta;
- **o estado real da tela.** A coisa que a fala nomeia às vezes está dentro de uma caixa aberta por
  cima, não na tela de trás. O mock que copia a tela de trás mostra o lugar errado;
- **o que cabe.** Contando os itens que aparecem no quadro, você já sabe se o teto do mock aguenta,
  antes de escrever texto que vai sair cortado com reticências.

### Regra 2. Orçamento estourado degrada para mock, nunca para palavra

Gasto o orçamento de tela, os beats seguintes que pediriam tela viram mock autorado. A cena não fica
vazia por contabilidade, e o nome dito sozinho não substitui o beat.

### Regra 3. Marca nunca é desenhada à mão

O mock desenha a **forma** da interface; o logo dentro dele é sempre arquivo de verdade, do acervo.
A regra inteira é a seção 7 das convenções do `componentes/REGISTRO.md`, e o critério 7 do
`skills/fabrica/referencias/GATES.md` reprova o corte que a quebra. Sem arquivo, a marca sai do
beat e o beat se resolve com palavra.

### Regra 4. tela nunca entra crua

Destaque na região que a fala aponta e rótulo autorado por cima. A lei é a 9.3 do `PADRAO-VISUAL.md`,
e o beat-sheet cobra as duas coisas nos campos `anotacao` e `por_que`.

### Regra 5. Print de banco de imagem não é rota

Tela vem da gravação do próprio vídeo ou não vem. Imagem de tela pega na internet é ilustração, e
ilustração com cara de tela é proibida pela 9.2 do `PADRAO-VISUAL.md`.

---

## 4. As seis formas de interface, e o que cabe em cada uma

Estas seis peças são o que torna mock possível. Escolher entre elas é decisão do inventário, e o
beat-sheet só executa.

| peça | a forma que ela entrega | escolha quando a fala trata de |
|---|---|---|
| `tela-de-conversa` | celular ou janela com balões alternados | alguém conversando com alguém, ou com uma máquina |
| `janela-de-navegador` | moldura de navegador com aba e barra de endereço | uma página, um endereço, uma coisa publicada |
| `campo-de-busca` | campo com a consulta digitada e resultados | uma pergunta sendo feita a um sistema |
| `lista-de-itens` | linhas com ícone, título e meta | um conjunto que voltou: arquivos, resultados, passos |
| `janela-de-app` | janela com barra lateral e área de conteúdo | onde o trabalho acontece, um programa com seções |
| `card-de-post` | post com avatar, autor, corpo e engajamento | uma publicação, um comentário, um número de rede |

**A linha de comando não é um sétimo mock, ela já tinha peça.** Terminal, prompt, comando digitado e
resposta de máquina são **mock** resolvido pela `caixa-de-comando`, que existe no acervo desde antes
desta lei. A família de mocks continua fechada em seis porque as seis cobrem interface com moldura
de janela, e a caixa de comando cobre a linha de comando. Sem esta linha, todo vídeo de instalação
fica com a coisa mais nomeada da fala sem rota, que é exatamente o buraco que a matriz existe para
tapar. Os parâmetros e os estados dela estão no `componentes/REGISTRO.md`.

**Os tetos são apertados, e o planejamento respeita.** Cada peça tem quanto conteúdo cabe na área
útil do painel, e o texto que passa sai cortado com reticências. Reticências no painel é sinal de
que a frase é longa demais para o corte, não de que a peça é estreita. Os números medidos vivem em
`componentes/REGISTRO.md`, que é o dono deles: antes de escrever conteúdo de mock, leia a abertura
"A família de mocks de interface" e a peça escolhida. Divergiu daqui, o registro vence.

O que você precisa ter em mente já no inventário, sem ir ao registro:

- conteúdo de mock é curto. Três linhas, três mensagens, três resultados, e é isso;
- o mock **é** o objeto herói, e ele ocupa o painel sozinho. Plano com um mock e três peças de apoio
  em volta não cabe;
- texto miúdo não existe. Onde uma interface de verdade teria letra pequena, o mock põe barra.

---

## 5. O inventário visual

### Quando roda

**Sempre, uma vez por vídeo, logo depois de transcrever e antes de qualquer gancho.** Não é etapa
opcional e não é etapa de vídeo difícil. Rodar depois dos ganchos não serve: a rota de cada coisa é
o que diz se o beat tem como existir, e descobrir isso com o brief escrito é descobrir tarde.

### O que ele faz

Quatro coisas, nesta ordem:

1. **varre a transcrição inteira atrás de coisa concreta nomeada** e passa cada uma pela ordem de
   decisão da seção 2;
2. **decide se a fonte é compartilhamento de tela** e registra a resposta, porque ela vale para
   todos os cortes daquele vídeo;
3. **roda o `baixar-logo.py` em lote** para toda marca nomeada que falta no acervo;
4. **lista o que não tem logo e não tem mock**, para a decisão sair aqui e não na hora de desenhar.

O item 3 existe por um motivo visto no uso: a falta de logo só aparecia no render, quando o tile
pinta o buraco hachurado no quadro, e nessa hora o painel já foi autorado e renderizado.

### O formato do arquivo

Um por vídeo, em `projetos/<video>/materiais-de-trabalho/INVENTARIO.md`.

```markdown
# Inventário visual do vídeo <nome da pasta>

- Fonte: `materiais-de-trabalho/fonte/<arquivo>`
- Compartilhamento de tela: <sim | não | só de X a Y>
- Evidência: <a proporção que o ffprobe devolveu e o que os quadros olhados mostram>
- Logos baixados agora: <claude, instagram> ou <nenhum, o acervo já tinha todos>
- Marca nomeada sem logo possível: <o nome, cai em palavra> ou <nenhuma>
- Quadros olhados: `materiais-de-trabalho/inventario/`

| coisa nomeada | onde aparece na fala | rota | recurso concreto | observação |
|---|---|---|---|---|
| <o nome como a fala diz> | <00:24, 03:41> | <logo> | <logos/claude.svg> | <o que o quadro mostrou> |
| <o nome como a fala diz> | <02:32> | <tela candidata> | <fonte, 02:45 a 02:55, a caixa aberta> | <o beat-sheet confirma ou baixa para mock> |

## Sem rota visual

<as coisas que ficaram em palavra, uma linha cada, com o motivo: não existe logo, não existe forma, ou o
beat não precisa>
```

Regras do arquivo:

- **uma linha por coisa, não uma por beat.** A mesma ferramenta citada em quatro momentos é uma
  linha com quatro tempos;
- **a coluna do recurso é concreta.** O nome do arquivo do logo, o nome da peça de mock, ou o
  intervalo na fonte. "Ver depois" não é recurso;
- **ideia abstrata não entra.** Se você está escrevendo "simplicidade" na primeira coluna, essa
  linha não é deste arquivo;
- **palavra é decisão, não sobra.** Toda linha que caiu em palavra traz o motivo escrito, e é por isso que a
  seção final existe separada;
- **`tela` nunca se fecha aqui, só `tela candidata`.** O inventário responde as duas perguntas que
  se respondem olhando o arquivo, e anota o instante e a região. A terceira, o orçamento, é do
  beat-sheet, porque no passo 0 nenhum corte existe ainda. A conta está no passo 2 da seção 2.

### Os logos, em lote

Junte todas as marcas nomeadas e peça de uma vez:

```
flow-reels componentes/baixar-logo claude instagram github
```

O script diz quais chegaram e quais não existem no acervo de origem. No motor 2.0, a marca que vai
aparecer em destaque também pede o logo em cor, em `componentes/marcas/` (`baixar-marca.py`, só de
kit oficial). O que não chegou vira uma de
duas coisas, e as duas são decisão sua, agora: alguém pega o logo oficial na página de imprensa da
marca e salva na pasta, ou aquela marca cai em palavra e o beat se resolve com palavra. O que não vale é
deixar em aberto, porque em aberto quer dizer que o tile vai pintar o buraco no render.

### A fonte é compartilhamento de tela?

Duas leituras, e a segunda é a que vale:

1. **o que a fala diz.** "Vou compartilhar a tela", "olha aqui", "clica aqui": sinal barato de que
   existe tela, e nada mais que sinal;
2. **a medida.** Quem mede é a produção, pelo teste da seção 2.5 da `SKILL.md` do
   `/flow-reels:produzir`, que confere a proporção da fonte, o tamanho do encarte do rosto, onde ele
   encosta e o que os quadros mostram. **Não reescreva esse teste aqui e não invente os números.**

No inventário você registra a resposta e a evidência. Sendo a fonte um compartilhamento de tela, tela
fica disponível para os beats de crença, e o bloco `tela` do beat-sheet vai sem o campo `arquivo`.
Sem isso, tela só existe se houver gravação separada em `materiais-de-trabalho/fonte/tela.mp4`, e onde
ela não existe os beats de crença descem para mock.

### O que o beat-sheet faz com ele

O campo `peca` de todo beat que trata de coisa concreta **resolve contra o inventário**. O beat-sheet
escolhe do que já está decidido, em vez de inventar na hora de escrever o beat. A conferência está na
lista de auditoria do `BEAT-SHEET.md`.

---

## 6. O que esta lei absorveu

Nada aqui é regra nova empilhada em cima do que já existia. Onde a matriz assumiu uma regra, a antiga
saiu do lugar onde estava:

| regra antiga | onde ela está agora |
|---|---|
| o orçamento de tela repetido no `BEAT-SHEET.md` | passo 2 desta lei, que consulta o número no dono, `PADRAO-VISUAL.md` 9.2 |
| "a origem da tela não é decisão sua", nas regras do bloco `tela` do `BEAT-SHEET.md` | rota tela e a seção 5 daqui, que registram a origem uma vez por vídeo |
| "bloco `tela` em beat de ideia abstrata", na tabela de erros do `BEAT-SHEET.md` | passo 0 da ordem de decisão, que separa concreto de ideia antes de qualquer rota |
| escolher a peça na hora de escrever o beat | passo 0 da ordem de trabalho: a rota é decidida uma vez, no inventário, e o beat resolve contra ele |

Se você sentir falta de uma regra que não está aqui nem no dono apontado, ela foi absorvida de
propósito. Não traga de volta.

---

## 7. Erros que esta lei existe para matar

| erro | o que fazer |
|---|---|
| coisa concreta virou card com o nome escrito | rode a ordem de decisão. Card com nome é palavra disfarçado de desenho |
| mock desenhado de memória, com cara de qualquer aplicativo | regra transversal 1: extraia o quadro e olhe antes |
| marca desenhada à mão porque o logo não estava no acervo | regra transversal 3. Baixe, ou tire a marca do beat |
| tela pedida para ilustrar ideia abstrata | passo 0 da ordem de decisão. Ideia é desenho, não é prova |
| beat rebaixado a palavra porque o orçamento de tela acabou | regra transversal 2. O destino do estouro é mock |
| conteúdo de mock escrito sem olhar o teto, e cortado com reticências no render | seção 4, e o teto medido no `componentes/REGISTRO.md` |
| inventário escrito depois dos ganchos, para ganhar tempo | ele é o passo 0 da ordem de trabalho. Depois do brief, a rota já virou improviso |
