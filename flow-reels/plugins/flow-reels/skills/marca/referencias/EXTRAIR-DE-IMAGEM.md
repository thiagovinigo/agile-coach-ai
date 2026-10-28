# Extrair a identidade de um print

Como tirar cor, superfície, layout e ritmo de uma imagem da marca da pessoa, usando só medição.
Nada aqui depende de API de visão, de serviço pago ou de conexão. São dois scripts e uma régua.

**O que este procedimento entrega:** uma proposta de valores para `marca/tokens.json`, escrita em
texto claro, para a pessoa confirmar ou corrigir. Ele não decide sozinho. Medição erra em marca
excêntrica, e a pessoa sabe a resposta que a imagem não conta.

---

## 0. Antes de medir: a imagem serve?

Peça uma peça **acabada e representativa**: uma capa, um post, um slide, um print do site. Serve
qualquer coisa em que a marca esteja montada de verdade.

| serve | não serve |
|---|---|
| post ou capa em tamanho cheio | foto do celular apontado para a tela |
| print do site inteiro | recorte só do logotipo, sem contexto |
| slide de apresentação da marca | imagem com filtro do Instagram por cima |
| página do manual de marca | montagem com três marcas diferentes juntas |

Se a pessoa mandar só o logotipo, você consegue a cor de acento e nada mais. Diga isso e peça uma
segunda peça. Duas imagens medidas separadamente, com os resultados comparados, valem muito mais que
uma imagem medida com capricho.

**Nunca meça um print de vídeo comprimido.** A compressão inventa cor nas bordas e o acento sai
deslocado. Se for o único material, avise que os valores são aproximados e confirme todos eles.

---

## 1. Cor: rode o script e leia a saída

```bash
flow-reels marca/amostrar_cores caminho/da/imagem.png
```

A saída legível vem assim:

```
Superfície: #1B1A1F  ->  modo escuro
Tinta: #FDFBF8  (contraste 16.74 com a superfície)
Destaque: #E8A541  (ocupa 2.7%, saturação 0.72)
Texto sobre o destaque: #16151A  (contraste 8.55)
Outros candidatos a destaque: #544233
```

E o JSON completo traz a paleta inteira, com a fatia de cada cor, matiz, saturação e luminância, mais
a lista de avisos. Use `--json` quando for só ler de máquina, e `--grade` quando quiser saber **onde**
na imagem o acento aparece.

### Como o script decide

Estes são os critérios. Eles estão no topo do arquivo do script, em constantes, e é lá que se mexe
quando uma marca muito fora do comum engana a medição.

| decisão | critério |
|---|---|
| **superfície** | a cor que ocupa a maior fatia da imagem |
| **modo** | escuro se a luminância relativa da superfície for menor que 0,22, claro caso contrário |
| **tinta** | entre as cores com saturação abaixo de 0,22, a de maior contraste com a superfície |
| **destaque** | saturação de 0,35 para cima, luminosidade HSL entre 0,10 e 0,85, ocupando entre 0,2% e 35% da imagem, e a pelo menos 45 de distância da superfície no espaço RGB |
| **desempate do destaque** | nota igual a saturação vezes um bônus pela fatia ocupada, então cor muito saturada ganha, e entre duas igualmente saturadas ganha a que aparece mais |
| **tinta sobre o destaque** | entre um claro e um escuro, a que der mais contraste, e o script avisa se nem essa passar de 4,5 |

### As duas armadilhas que este script já tem resolvidas

São dois erros medidos nesta máquina, que o script evita e que **qualquer outra rotina de extração
precisa evitar também**. Se um dia alguém reescrever isto, comece por aqui.

**Primeira: quantizador pronto perde o acento.** O quantizador do Pillow distribui as vagas de paleta
por volume de pixel. Numa peça de fundo escuro, ele gasta quinze das dezesseis vagas em tons de fundo
quase idênticos e joga o texto claro e o acento laranja no mesmo balde, devolvendo um marrom que não
existe em lugar nenhum da imagem. A correção é contar numa **grade fixa de 16 níveis por canal**:
grade fixa não tem vaga para disputar, então uma cor que ocupa 2% da tela continua sendo uma cor.

**Segunda: saturação de HSL mente sobre neutros.** No modelo HSL, um branco levemente quente como
`#FDFBF8` aparece com saturação 0,55, e qualquer filtro de neutro o rejeita. Resultado: a tinta creme
da marca é descartada e o script devolve um cinza médio como cor de texto. A conta certa é a
saturação do **HSV**, o canal mais forte menos o mais fraco, dividido pelo mais forte. Nela, o mesmo
creme dá 0,02, que é o que ele é: um neutro.

### Quando o script não acha o acento

Ele avisa em vez de inventar. Aconteceu por um destes motivos:

- a peça é monocromática de verdade, e a marca não tem cor de acento;
- o acento existe mas aparece em menos de 0,2% da imagem, por exemplo um traço fino num print grande;
- o acento é um tom dessaturado, como um bege ou um azul acinzentado, e ficou abaixo do piso de 0,35.

Nos três casos a saída é a mesma: **pergunte a cor direto à pessoa**, mostrando os outros candidatos
que o script listou. Não baixe o piso para forçar um resultado. Piso baixo transforma sombra de card
em cor de marca, e aí o corte inteiro sai pintado de errado.

### Confira sempre o contraste antes de gravar

O script devolve `contraste_tinta_superficie` e `destaque_contraste_sugerido`. O piso é **4,5 para 1**.
Abaixo disso a legenda e o texto do painel somem depois que a plataforma comprime o vídeo. Quando o
contraste não passa, você tem três saídas, nesta ordem de preferência:

1. escurecer ou clarear a **tinta**, mantendo o acento intacto, porque tinta é função e acento é marca;
2. usar o acento só como borda, traço e preenchimento de forma, nunca como fundo de texto;
3. propor um segundo tom da mesma cor de acento, mais escuro ou mais claro, só para quando ele
   precisar carregar texto em cima.

---

## 2. Superfície: confirme o modo antes de seguir

O modo decide o painel inteiro, então vale trinta segundos de conferência. Olhe a imagem e responda:

- o fundo predominante é escuro ou claro?
- ele é chapado ou tem uma variação suave, tipo um brilho atrás do assunto?
- ele é neutro puro, ou tem cor dentro, tipo um preto azulado ou um branco quente?

Fundo chapado e neutro puro é o padrão do mundo e o pior dos padrões. Se a superfície medida vier
como `#000000` ou `#FFFFFF` exatos, proponha à pessoa um deslocamento de poucos pontos na direção do
acento dela. Preto puro achata a imagem e branco puro estoura sobre vídeo. Grave esse valor deslocado.

A diferença entre `superficie` e `superficie_alt` deve ficar entre **6 e 10 pontos de luminosidade**.
Mais que isso e o card vira outra cor; menos e ele some do fundo. Se a imagem não tiver card nenhum
para medir, derive a alternativa da superfície, clareando no modo escuro e escurecendo no modo claro.

---

## 3. Layout: meça a caixa dos elementos

Cor responde "que marca é essa". Layout responde "como essa marca organiza a página", e é isso que
faz o painel parecer da pessoa em vez de parecer um modelo pronto pintado com a cor dela.

A medição é simples: tudo que **não** é a cor da superfície é conteúdo. Marque essas linhas e
colunas, agrupe as vizinhas, e você tem as faixas de conteúdo e as margens.

```python
from PIL import Image, ImageFilter

# 1. O filtro de mediana é obrigatório: ele apaga o grão antes da medição.
#    Sem ele, cada pontinho de textura conta como conteúdo e a margem mede zero.
base = Image.open(caminho).convert("RGB").filter(ImageFilter.MedianFilter(3))
fundo = (27, 26, 31)      # a superfície que o amostrar_cores devolveu
tolerancia = 24           # diferença por canal a partir da qual o pixel é conteúdo

largura, altura = base.size
px = base.load()

def e_conteudo(x, y):
    r, g, b = px[x, y]
    return max(abs(r - fundo[0]), abs(g - fundo[1]), abs(b - fundo[2])) > tolerancia

linhas = [y for y in range(0, altura, 2) if any(e_conteudo(x, y) for x in range(0, largura, 4))]
colunas = [x for x in range(0, largura, 2) if any(e_conteudo(x, y) for y in range(0, altura, 4))]

print("margem esquerda:", colunas[0], "  direita:", largura - 1 - colunas[-1])
print("margem topo:", linhas[0], "  base:", altura - 1 - linhas[-1])

# 2. Agrupa linhas vizinhas em faixas. Um vão de até 16 px ainda é o mesmo bloco.
faixas, atual = [], None
for y in linhas:
    if atual and y - atual[1] <= 16:
        atual[1] = y
    else:
        if atual:
            faixas.append(tuple(atual))
        atual = [y, y]
faixas.append(tuple(atual))

for inicio, fim in faixas:
    cols = [x for x in range(0, largura, 2)
            if any(e_conteudo(x, y) for y in range(inicio, fim + 1, 2))]
    print(f"faixa y {inicio}-{fim} (altura {fim - inicio})  x {cols[0]}-{cols[-1]}")
```

Rodando isso num painel de 1080 por 956, a saída fica assim:

```
margem esquerda: 56   direita: 57
margem topo: 66   base: 155
faixa y 66-90   (altura 24)   x 56-438
faixa y 152-238 (altura 86)   x 60-716
faixa y 276-326 (altura 50)   x 62-336
faixa y 380-654 (altura 274)  x 56-1022
faixa y 690-800 (altura 110)  x 56-808
```

E daí você lê o layout inteiro sem olhar pixel:

- **margem** de 56 px dos dois lados, então a marca trabalha com respiro generoso e a largura útil é 968;
- a primeira faixa tem 24 px de altura e ocupa menos da metade da largura: é um **rótulo**;
- a segunda e a terceira, com 86 e 50 px, alinhadas à esquerda: são as **duas linhas de um título**;
- a quarta, de 274 px, indo de borda a borda: é a faixa de **cards**;
- a última, de 110 px, começando na margem e parando antes do fim: é a linha de **passos**;
- a base de 155 px sem nada é a **zona quieta**, onde a legenda passa depois.

### Duas armadilhas da medição de layout

**O grão zera as margens.** Grão é ruído sobre a imagem inteira, inclusive sobre a área vazia, então
todo pixel vira conteúdo e a medida dá zero. O filtro de mediana de 3 resolve, e sem ele o número não
significa nada. Foi medido: a mesma imagem deu margem 0 sem o filtro e margem 56 com ele.

**Brilho de fundo também engana.** Se a marca usa uma mancha de luz atrás do assunto, a tolerância
precisa ser maior que a variação dessa mancha. Suba a tolerância até que as margens parem de mudar.
Se elas continuarem mudando a cada aumento, a imagem tem um degradê forte e a medição de margem não
se aplica: descreva o degradê e siga sem o número.

### Raio de canto e espessura de borda

Não precisa de script. Dê zoom num card da imagem e compare com três possibilidades:

- canto vivo, sem arredondamento nenhum: raio 0, e a marca é dura e técnica;
- arredondamento discreto, que você só vê de perto: raio entre 8 e 16;
- arredondamento óbvio, que se nota de longe: raio entre 20 e 32.

Acima de 40 o card começa a virar pílula e perde a cara de card. A borda, se existir, quase sempre
tem 1 ou 2 px na imagem original. Grave **2**, porque abaixo disso ela desaparece depois que a
plataforma comprime o vídeo.

---

## 4. Tipografia: o que a imagem conta e o que ela não conta

Um print **não entrega o arquivo da fonte**, e não existe medição que resolva isso. O que dá para
fazer é descrever o que se vê e usar a descrição para conduzir a pergunta.

Olhe o título da peça e classifique em uma das quatro famílias:

| o que você vê | como se chama | o que perguntar |
|---|---|---|
| letras sem pezinho, formas circulares, o "o" quase um círculo perfeito | sem serifa geométrica | "sua fonte de título é arredondada e geométrica, certo? qual é o nome dela?" |
| letras sem pezinho, formas mais fechadas e retas | sem serifa neutra | mesma pergunta, dizendo que parece uma fonte mais seca |
| letras com pezinho, contraste entre traço grosso e fino | serifada | "o título é serifado, tipo revista, confere?" |
| letras de largura toda igual, parecendo terminal | monoespaçada | pergunte se isso é da marca ou só daquele print |

Some duas observações que mudam o painel:

- **peso**: o título é fino, médio ou bem pesado? Marca de peso pesado suporta título grande; marca
  de peso fino precisa de título menor e mais espaço em volta.
- **caixa**: o título aparece em caixa alta, em caixa baixa, ou só com a primeira maiúscula? Isso vira
  regra do painel e não muda entre um corte e outro.

Quando a pessoa disser o nome da fonte, peça o arquivo. Se ela não tiver o arquivo, ofereça a opção
livre mais próxima e diga qual é. Fonte que não está na pasta não existe para o renderizador, e o
painel cairia numa fonte de sistema qualquer, sem aviso.

Toda fonte que entrar passa por `scripts/tratar_fonte.py` antes de ser gravada nos tokens. Fonte
variável precisa virar estática, senão a legenda sai no peso padrão do arquivo, que costuma ser fino.

---

## 5. O acento: onde ele aparece, não só qual é

Rode o script com `--grade` e você recebe uma matriz de 4 por 4 com a fração de cada célula da imagem
ocupada pelo acento:

```
[[0.000, 0.000, 0.053, 0.000],
 [0.060, 0.022, 0.030, 0.000],
 [0.039, 0.000, 0.000, 0.000],
 [0.135, 0.028, 0.099, 0.000]]
```

Isso responde uma pergunta de composição que a cor sozinha não responde:

- acento concentrado na **primeira linha**: a marca usa cor para abrir, tipo etiqueta no topo;
- acento concentrado na **última linha**: a marca usa cor para fechar, tipo botão ou chamada embaixo;
- acento **espalhado por muitas células**: cuidado, ou a marca usa cor com liberdade, ou você está
  medindo uma peça que tem uma foto colorida dentro;
- acento em **duas ou três células apenas**: é uma marca de acento único e disciplinado, que é o
  comportamento que o painel espera.

O painel usa acento em uma coisa por vez. Se a peça medida usa acento em cinco lugares, isso é da
peça, não vira regra do painel. Anote a observação e siga.

---

## 6. Escreva o que você mediu, em texto

Fecha assim, sempre. Antes de gravar qualquer arquivo, apresente à pessoa um resumo em prosa, no
formato abaixo, e peça confirmação item por item. É a etapa que transforma medição em decisão.

> Olhei a imagem que você mandou e é isto que eu vejo:
>
> Sua marca trabalha em **fundo escuro**, um quase preto levemente arroxeado (`#1B1A1F`), com texto
> em **branco quente** (`#FDFBF8`). O acento é um **laranja âmbar** (`#E8A541`), e você usa ele com
> disciplina: ocupa menos de 3% da peça e aparece em dois pontos só.
>
> A organização é de **respiro largo**: 56 px de margem dos dois lados, título grande em duas linhas
> alinhado à esquerda, e os blocos de conteúdo indo de borda a borda. Os cantos são **bem
> arredondados**, uns 20 px.
>
> A fonte do título é **sem serifa e geométrica**, de peso médio para pesado. Preciso do arquivo dela,
> ou do nome, para o painel usar a sua e não uma parecida.
>
> Confere? Me diga qualquer coisa que eu li errado, principalmente o laranja: é exatamente esse tom?

Três regras para esse resumo:

1. **Nomeie as cores em palavras**, não só em hexadecimal. A pessoa reconhece "laranja âmbar" e não
   reconhece `#E8A541`.
2. **Aponte o que você não conseguiu medir** e transforme em pergunta. Silêncio sobre o que falta é
   o que produz painel errado três etapas depois.
3. **Uma imagem é uma amostra, não a lei.** Se o resultado contrariar o que a pessoa já disse na
   conversa, o que ela disse ganha. A medição serve para propor, não para corrigir o dono da marca.

---

## 7. O que não fazer

- **Não grave nada direto nos tokens a partir da medição.** Todo valor passa pela confirmação.
- **Não use a imagem como referência de composição.** Ela dá cor, forma e ritmo, não dá o painel.
  Copiar o arranjo de um post dentro de um vídeo vertical produz uma peça que não cabe na tela.
- **Não extraia cor de imagem com foto dentro.** Foto tem pele, céu e madeira, e tudo isso entra na
  contagem como se fosse marca. Peça uma peça gráfica, ou recorte a área gráfica antes de medir.
- **Não junte duas marcas.** Se a peça tiver logotipo de parceiro, de cliente ou de patrocinador,
  recorte antes. O script não sabe de quem é cada cor.
- **Não meça o mesmo print duas vezes esperando resultado diferente.** O script é determinístico. Se
  o resultado não serve, o problema está na imagem, e a solução é outra imagem.
