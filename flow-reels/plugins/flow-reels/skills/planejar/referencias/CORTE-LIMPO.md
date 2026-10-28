# Corte limpo

Como escolher o ponto de entrada e o ponto de saída de cada segmento sem amputar fala. Vale em
qualquer passo da ordem de trabalho, que está escrita no `SKILL.md` desta skill. É a lei da regra
"bordas em silêncio": todo trecho entra e sai depois da palavra terminada, nunca no meio da
respiração.

Fala amputada é o defeito mais barato de evitar e o mais caro de deixar passar. Um corte que começa
com meia sílaba, ou que termina cortando o ar da última palavra, avisa a quem assiste que aquilo é um
pedaço de outra coisa. E a partir do momento em que a pessoa percebe a emenda, ela para de ouvir o
conteúdo e passa a ouvir a edição.

## Quantos pontos cada coisa tem

O gancho e o corpo não dão o mesmo trabalho aqui, porque não têm a mesma liberdade.

- **O gancho tem dois pontos, e só dois:** onde ele entra e onde ele sai. Ele é um span contínuo do
  áudio, e não existe emenda interna para conferir (`GANCHO.md`, seção 2). A única edição permitida
  dentro dele é apagar a repetição de uma palavra gaguejada, e ela também se fecha nos dois sinais
  da seção 1: o pedaço que sai precisa ter silêncio dos dois lados, senão fica um soluço no meio da
  abertura. Se não tem silêncio dos dois lados, deixe a repetição, que ela incomoda menos que o
  soluço.
- **O corpo tem dois pontos por trecho, mais uma emenda por junção.** Ele é montado de vários
  trechos, em qualquer ordem, então é nele que mora a conferência de emenda da seção 4, passo 5 do
  procedimento.

---

## 1. A regra dos dois sinais

**Nenhum ponto de corte se fecha com um sinal só.** Todo ponto precisa concordar em dois:

| sinal | o que ele diz | de onde vem |
|---|---|---|
| **a palavra** | onde, mais ou menos, a frase começa e termina | `palavras.json`, em `materiais-de-trabalho/transcricao/` |
| **a energia** | onde, exatamente, existe silêncio de verdade | `audio16k.wav`, na mesma pasta, medido pelo script |

A palavra dá a região. A energia dá o quadro.

**O mapa de silêncios do passo 1 é o primeiro sinal, não um terceiro.** Ele sai do mesmo
`palavras.json`, lista as pausas mais longas do vídeo e diz onde procurar borda, porque quem fala
pausa onde termina uma ideia (`LEVANTAMENTO.md`, seção 1.2). Ele escolhe a região; quem fecha o
ponto continua sendo a energia. Usar o mapa como se fosse medida é o mesmo erro de usar o tempo da
palavra, com outro nome. Quem usa só a palavra corta cedo ou tarde por alguns
décimos, e alguns décimos são exatamente o tamanho de uma sílaba.

---

## 2. Por que o tempo da palavra mente

O `palavras.json` não é uma medição, é uma estimativa. O alinhador recebe o texto reconhecido e
encaixa cada palavra em um intervalo de tempo. Esse encaixe erra de forma previsível:

1. **O alinhador estica a palavra para dentro do silêncio.** Quando existe uma pausa depois de uma
   palavra, o tempo de `fim` costuma invadir essa pausa, porque o modelo prefere não deixar buraco
   entre palavras. Resultado: se você cortar exatamente no `fim`, você corta depois da pausa ter
   começado, e o corte fica com um rabo de silêncio. Se cortar no `inicio` da próxima, você entra
   dentro do ar dela.
2. **A primeira palavra costuma começar cedo demais.** O `inicio` da primeira palavra de uma frase
   frequentemente inclui a inspiração. Cortar ali traz um "trrr" de respiração para a abertura do
   corte.
3. **Número escrito por extenso desalinha.** Quando a pessoa fala "quarenta e três" e o texto vira
   "43", o alinhador tem três palavras faladas para uma palavra escrita, e reparte o tempo de um jeito
   que não corresponde ao que se ouve.
4. **Hesitação vira tempo de palavra.** "É... então" costuma entrar dentro do intervalo da palavra
   seguinte.

Nada disso é defeito do transcritor, é o que a ferramenta é. Por isso o áudio é o juiz.

---

## 3. O que conta como silêncio de verdade

Silêncio não é zero. Toda gravação tem ruído de sala, ar condicionado, computador. O que interessa é
o silêncio **relativo à fala daquela gravação**.

O critério que o script usa, e que vale como definição do pacote:

- a energia é medida em janelas de **50 ms**
- a referência de fala plena é o **percentil 90** de todas as janelas do arquivo
- uma janela é **silenciosa** quando fica abaixo de **8%** dessa referência
- um **silêncio de verdade** é uma sequência de pelo menos **3 janelas silenciosas seguidas**, ou
  seja 150 ms

Abaixo de 150 ms não é pausa, é o intervalo entre duas sílabas, e cortar ali corta palavra no meio.

### O buraco dentro do trecho, que não é problema de borda

As seções acima tratam de **onde entrar e sair**. Esta trata do que fica **no meio**, e é um defeito
diferente: o trecho pode ter as duas bordas perfeitas e ainda assim ter um silêncio lá dentro que
soa como travamento.

A diferença entre respiração e buraco se percebe ouvindo, e ela aparece no número: **buraco é um
salto bem maior que as outras pausas daquele mesmo falante**, não um valor absoluto. Gente que fala
devagar pausa 700 ms o tempo todo, e ali 700 ms é respiração; gente que fala rápido pausa 200 ms, e
ali 700 ms é buraco. Por isso a régua é a distribuição de pausas do próprio arquivo, que o
`energia_audio.py` já levanta, e não um teto que eu escreveria aqui.

**Como conferir:** liste as pausas internas do trecho e compare com as pausas daquele falante no
vídeo inteiro. Pausa muito acima das outras é buraco, e buraco se resolve cortando o silêncio ou
mudando as bordas do segmento, nunca deixando passar porque as bordas estão certas.

**O que isto não proíbe:** a pausa **entre** dois segmentos montados. Ali o corte é intencional e a
pausa é o lugar onde a transição entra. Buraco é dentro de um segmento contínuo.

---

## 4. O procedimento

Para cada ponto candidato, sempre nesta ordem.

**Passo 1. Tire o tempo da palavra.** Ache no `palavras.json` a primeira palavra do segmento e a
última. Anote `inicio` da primeira e `fim` da última.

**Passo 2. Rode o script com os dois tempos.**

```
flow-reels planejar/energia_audio \
  projetos/<video>/materiais-de-trabalho/transcricao/audio16k.wav 412.8 421.6
```

Ele imprime o envelope em janelas de 50 ms em volta de cada candidato, marca as janelas silenciosas e
sugere o silêncio mais próximo.

**Passo 3. Leia o envelope, não só a sugestão.** O que você procura é o **vale**: uma sequência de
janelas baixas com fala dos dois lados. A saída do script mostra isso como uma escada de barras que
desce, fica baixa por algumas janelas e sobe de novo.

Situações que a leitura revela e a sugestão sozinha não:

- **Não existe vale na região.** A pessoa emendou as frases sem respirar. Aí o ponto tem que se mover
  para a fronteira de frase anterior ou posterior, mesmo que isso mude a duração do corte. Não existe
  corte limpo onde não existe silêncio.
- **Existem dois vales próximos.** Escolha o que está do lado certo da palavra, não o mais fundo. Um
  vale fundo depois de uma palavra de ligação ainda é um corte no meio da ideia.
- **O vale é curto demais**, abaixo de 400 ms. Entrada e saída juntas precisam de pelo menos 400 ms
  de pausa para caberem com folga. Uma pausa curta serve como ponto único, e não serve para emendar
  dois segmentos dentro dela.
- **O vale é longo demais**, acima de 700 ms. Aí você está cortando no meio de uma pausa dramática, e
  o corte vai abrir com silêncio. Aproxime o ponto do começo da fala seguinte.

**Passo 4. Aplique as margens.**

| ponto | onde cai | por quê |
|---|---|---|
| **entrada** | de 80 a 120 ms antes do primeiro som da fala | dá o ataque da consoante inteiro. Sem essa folga, um "p" ou um "t" inicial some e a palavra soa cortada |
| **saída** | de 250 a 400 ms depois do último som | deixa a frase fechar. Cortar colado na última vogal soa como interrupção |
| **respiração** | a inspiração pertence à frase que vem **depois** dela | pode entrar até cerca de 150 ms de inspiração antes da fala, e isso soa natural. Mais que isso vira ruído na abertura |

**Passo 5. Confira a emenda entre segmentos.** Quando dois segmentos que não eram vizinhos se
encostam, os dois lados precisam estar em silêncio. Um lado limpo e o outro colado na fala gera a
emenda audível clássica: a voz muda de ritmo no meio da frase.

Se o timbre do ruído de sala dos dois trechos for muito diferente, prefira outro par de trechos. Isso
se percebe ouvindo, não medindo.

---

## 5. Terminar em frase fechada

O ponto de saída de **cada segmento** cai em fim de frase, não em fim de palavra.

Como reconhecer fim de frase sem ouvir: leia a fala do segmento em voz alta. Se para terminar você
precisa continuar lendo a próxima palavra, o segmento não fechou.

Nunca termine um segmento em:

- conjunção: e, mas, porque, então, aí, que, ou
- preposição: de, em, para, com, por
- artigo: o, a, um, uma
- verbo auxiliar solto: "eu tinha", "ela vai", "a gente foi"

**Como o trecho começa é outra regra, e ela é de formato, não de borda.** Não começar por conectivo
vale para a **abertura** do corte; dentro do miolo, conectivo é o que encadeia um trecho no outro e
não se tira (`FORMATOS.md`, seção 4). Aqui você só decide onde o ponto cai.

**Qual fim escolher também não é decisão desta lei.** A qualidade do fim é critério de seleção e
está em `LEVANTAMENTO.md`, seção 3: virada que fecha, próximo passo concreto, pensamento completo
que para, ou a transição em que a pessoa muda de assunto. Este arquivo pega o fim já escolhido e
diz em que segundo ele cai.

E o corte inteiro, além disso, **termina em conclusão e na âncora do gancho**, nunca em gancho novo.
O último segmento entrega o payoff, volta à palavra concreta que a abertura usou e cala. Se abriu
falando de planilha, fecha falando de planilha: é isso que dá a sensação de completo. Terminar
prometendo mais uma coisa faz a pessoa procurar a continuação que não existe, e a frustração vira
comentário ruim. A regra inteira é a R6 do `VALOR.md`, seção 3, inclusive a forma que ela toma no
formato trajeto, onde o último segmento é o `destino`; aqui ela só decide onde o último
ponto cai.

---

## 6. Lista de conferência

Antes de escrever os tempos no brief, responda sim ou não para cada segmento:

1. O ponto de entrada caiu dentro de um silêncio de pelo menos 150 ms, medido pelo script?
2. O ponto de saída também?
3. A entrada deixou de 80 a 120 ms de folga antes do primeiro som?
4. A saída deixou de 250 a 400 ms depois do último som?
5. O segmento começa em começo de frase e termina em frase fechada?
6. Nenhum segmento termina em conjunção, preposição, artigo ou verbo auxiliar?
7. Cada emenda entre dois segmentos tem silêncio dos dois lados?
7b. Dentro de cada segmento, nenhuma pausa destoa das pausas normais daquele falante?
8. Lendo a fala montada inteira, em voz alta, não sobrou nenhuma palavra pela metade nem nenhuma
   frase sem fim?
9. O corte inteiro termina em conclusão, e a última frase volta à âncora do gancho?
10. O gancho saiu de um span contínuo, com dois pontos só, sem nenhuma emenda interna?

Um "não" em qualquer item significa voltar ao script, não ajustar no olho.
