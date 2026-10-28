# O levantamento

Este arquivo é a lei dos **passos 1 e 2** da ordem de trabalho: ler o vídeo inteiro duas vezes antes
de procurar trecho, e depois varrer largo sem julgar. A ordem inteira, com os passos numerados, está
escrita em um lugar só, no `SKILL.md` desta skill, e não se repete aqui.

**O defeito que este arquivo existe para matar:** filtrar enquanto lê. Quem varre já perguntando "este
trecho passa?" encontra os candidatos óbvios e para. Quem varre listando encontra muito mais, e
quase sempre descobre que o melhor estava no meio do vídeo, num lugar onde ninguém procurou.

A busca acontece em **duas fases**, e misturar as duas é o que faz vídeo bom render pouco:

| fase | o que você faz | onde está a lei |
|---|---|---|
| **levantamento** | anota generosamente tudo que tem chance, sabendo que a maioria vai cair | aqui |
| **julgamento** | aplica os eliminadores e corta sem dó | `FORMATOS.md`, `GANCHO.md` e `VALOR.md` |

Nenhum candidato é descartado neste arquivo. Nenhum eliminador roda aqui. Se você se pegar
escrevendo "esse não presta" durante o levantamento, você já entrou na fase errada.

---

## 1. As duas leituras do vídeo inteiro (passo 1)

**Leia a transcrição inteira antes de selecionar.** A tentação é varrer procurando um momento bom e
cortar em volta dele, e é isso que produz corte que começa no meio de uma frase. Se a transcrição
for longa, leia em blocos, mas cubra 100%.

**Você avalia frases, e o arquivo que traz frases é o `transcricao.md`.** Ele sai do `/flow-reels:transcrever`
já quebrado por pontuação final somada a pausa, uma frase por linha, e é nele que a varredura e os
greps deste arquivo rodam. O `palavras.json` é a fita de palavras soltas: ele serve para medir tempo
e pausa, não para julgar trecho. Quem varre a fita de palavras acaba avaliando fatia de tempo em vez
de frase, e fatia de tempo corta no meio do pensamento. Os critérios da quebra são do
`transcrever/scripts/normalizar.py`, que é o dono deles.

Enquanto lê, repare em duas coisas sobre o vídeo **como um todo**. As duas saem de um comando só:

```
flow-reels planejar/leitura_do_video projetos/<video>
```

O script lê o `palavras.json` e imprime as duas leituras. Ele não fecha ponto de corte nenhum.

### 1.1 Para onde a fala aponta

A primeira leitura é **o quanto a fala se apoia em palavras que apontam para fora dela mesma**:
aqui, isso, esse, ele, lá, aí. Quando a pessoa está demonstrando algo numa tela, essas palavras
dominam a narração inteira, e o resultado é que quase nenhuma frase se sustenta sozinha.

**Isso não é defeito do vídeo.** É como se fala apontando para coisas. Mas significa que esse vídeo
vai render poucos trechos que funcionam como afirmação isolada.

Duas consequências, e as duas são obrigação:

1. **Diga o número antes de prometer volume.** Uma linha, no chat, antes de apresentar qualquer
   candidato: quanto a fala aponta para fora e o que isso faz com o material. Ninguém pode esperar
   um volume que o vídeo não comporta. Isso **não** é aritmética de funil, que a regra da vitrine
   proíbe: é uma afirmação sobre o material, e ela é dita antes de o funil existir.
2. **Fala que aponta para fora puxa o material para o formato trajeto** (`FORMATOS.md`), onde a
   promessa da abertura estabelece o que está sendo feito e as palavras que apontam passam a ter
   para onde apontar dentro da própria peça.

O que o número **não** é: um limiar. Não existe valor a partir do qual o vídeo "não rende". A
comparação que vale é entre vídeos do mesmo canal, e ela se constrói medindo. Não invente uma
fronteira, e não afrouxe nenhum eliminador porque o número veio alto.

### 1.2 O mapa dos silêncios

A segunda leitura é **onde estão as pausas mais longas**. Com tempo por palavra dá para listar as
maiores pausas do vídeo, e essa lista é a mais útil do processo, por um motivo que não é óbvio:

> Os silêncios não servem só para você evitar cortar em cima deles. **Eles são os melhores pontos de
> entrada e de saída de trecho**, porque quem fala pausa onde termina uma ideia.

Procure as bordas de todo candidato ali. Quando um trecho bom não tem pausa perto da borda que você
queria, a borda muda de lugar, não a regra.

**O mapa dá a região, a energia dá o quadro.** O tempo da palavra é estimativa e costuma invadir a
pausa, pelos motivos da seção 2 do `CORTE-LIMPO.md`. Então o mapa serve para escolher **onde**
entrar e sair, e o ponto só se fecha depois de conferido no áudio com o `energia_audio.py`. Um não
substitui o outro.

---

## 2. A varredura generosa (passo 2)

Na fase de levantamento você está procurando **formas conhecidas, não qualidade**. Forma se
reconhece lendo; qualidade se julga depois, com os eliminadores na mão.

Três regras da varredura:

**A transcrição inteira.** Do primeiro ao último segundo, sem amostragem, sem pular a parte que
parece chata. A parte chata é onde mora a frase direta, porque é onde a pessoa parou de performar.

**Cronologia é livre, e o começo não tem preferência.** O melhor material costuma estar no meio e no
fim, justamente onde a busca não chega. Divida a duração em três e levante candidato em cada terço.
Se um terço não produziu nenhum, escreva no `GANCHOS.md` por quê, em uma frase.

**No mínimo seis candidatos levantados.** Seis é o piso da fase generosa, não a meta. Abaixo de seis
você não varreu, você defendeu a primeira ideia que teve. O normal é levantar bem mais do que seis e
ver a maioria cair no julgamento, e isso é o processo funcionando.

São quatro listas de varredura. Rode as quatro sobre a transcrição inteira, uma de cada vez.

### 2.1 Formas de abertura

Procure trechos que **começam** de alguma destas formas:

| forma | como ela soa |
|---|---|
| afirmação contrária ao senso comum | "todo mundo diz para começar pelo planejamento, e é justamente ele que trava" |
| lacuna de curiosidade | "tem uma coisa que ninguém conta sobre isso" |
| promessa de valor | "é assim que se faz tal coisa" |
| quebra de padrão | algo inesperado que interrompe o fluxo do vídeo |
| prévia do resultado | "no fim disso você vai conseguir" |
| conhecimento restrito | "o que quem faz isso não costuma contar" |

E a que **nunca** funciona, que é a mais comum de todas: a genérica, "hoje eu quero falar sobre".
Ela não é mais uma forma da tabela, é a ausência de forma, então ela nunca coloca um trecho na
lista por si mesma. Se o trecho entrou por outra lista, ele fica: quem decide isso é o julgamento, não você aqui.

### 2.2 Marcadores de trecho forte

Coisas rastreáveis direto na transcrição, e as três são greppáveis:

| marcador | o que procurar | como achar |
|---|---|---|
| número concreto | quantidade, tempo, contagem, preço | `grep -nE "[0-9]" transcricao.md`, mais os números por extenso: um, dois, três, dez, vinte, trinta, cem, mil |
| nome próprio reconhecível | pessoa, empresa, ferramenta, produto | palavra com maiúscula no meio da frase, cruzada com o `INVENTARIO.md` do passo 0 |
| marca de experiência vivida | "eu testei", "passei meses nisso", "já perdi dinheiro com isso" | `grep -niE "eu testei\|eu tentei\|eu passei\|eu perdi\|eu fiz isso\|na época\|durante (anos\|meses)"` |

**Trecho que tem qualquer um dos três entra na lista**, mesmo que pareça morno na leitura. Morno na
leitura é impressão, e impressão não decide nada nesta fase.

### 2.3 Tipos de momento: o que ACONTECE no trecho

Do mais forte para o mais fraco:

1. algo que **falhou e foi corrigido** durante a gravação
2. uma **objeção** que a pessoa levanta e responde
3. uma afirmação que **contraria o que o público espera**
4. um **número, custo ou tempo** concreto
5. **explicação e demonstração**

A seleção que erra quase sempre erra pegando **explicação**, porque explicação é o que mais aparece
na transcrição e o que menos prende. Levante a explicação, ela entra na lista como as outras, mas
saiba que ela começa no último lugar desta ordem.

### 2.4 Tipos de informação: o que o trecho CONTÉM

Esta lista é **a mesma** dos cinco tipos de valor, e ela mora em `VALOR.md`, seção 2, com a ordem de
valor, o sinal de reconhecimento na transcrição e a armadilha de cada tipo. Não existe uma segunda
lista aqui, e ela não se repete: no levantamento você marca qual tipo o trecho parece conter, e no
julgamento o candidato declara um.

O que pertence a este arquivo é o piso da lista, que é o que **não** sobe:

- **conselho genérico com algum detalhe** entra na varredura e quase sempre cai no filtro do
  aprendizado (`VALOR.md`, seção 1);
- **platitude vaga** não entra em lista nenhuma.

### 2.5 Os dois eixos se somam

As duas últimas listas são diferentes e se somam: uma classifica o que **acontece** no trecho, a
outra classifica o que o trecho **contém**. Um mesmo trecho recebe uma marca de cada.

> **Trecho que pontua nos dois eixos é o alvo.**

Um erro corrigido ao vivo (momento forte) que entrega um critério de decisão (informação densa) vale
mais que uma explicação impecável de um método. Isso não é nota e não é média: é onde você olha
primeiro quando o julgamento devolver mais sobreviventes do que o teto de cortes.

---

## 3. Procure finais, não só aberturas

Todo trecho precisa terminar em algum lugar, e **a qualidade do fim é critério de seleção, não
consequência do corte**. Levante cada candidato já com as duas bordas: onde ele entra e onde ele
termina.

Os fins bons, em ordem:

1. **virada ou revelação que fecha** o que o trecho abriu
2. **chamada com próximo passo concreto**
3. **pensamento completo que para naturalmente**
4. **o ponto onde a pessoa muda de assunto**, que é útil sem ser brilhante, porque transição é saída
   de graça

O fim ruim é um só: **o corte no meio do pensamento**.

Onde o último ponto cai em segundos, com margem e silêncio conferido, é do `CORTE-LIMPO.md`. Qual
fim você escolhe é daqui.

---

## 4. A mesma ideia dita mais de uma vez

Ela vai aparecer repetida, porque quem fala se repete. Quando isso acontecer, **compare as
ocorrências e fique com a mais bem formada. Não com a primeira, nem com a mais enfática.**

A primeira costuma ser a tentativa, a enfática costuma ser a que tem mais palavra apontando para
fora, e a mais bem formada é a que nomeia as coisas com todas as letras. As outras ocorrências ficam
registradas na linha do pool com o motivo "mesma ideia, ocorrência menos formada", para ninguém
levantar de novo na rodada seguinte.

---

## 5. O que sai do levantamento

A tabela do pool no `GANCHOS.md`, com uma linha por candidato levantado e **nenhum veredicto ainda**:

```markdown
## Levantamento

- Palavras que apontam para fora da fala: 11.2 a cada 100, em 78% das frases
- Pausas longas mapeadas: 18 acima de 0.45 s
- Candidatos levantados: 9
- Cobertura: terço 1 = 3, terço 2 = 3, terço 3 = 3

| # | span (s) | primeiras três palavras | forma de abertura | marcador | momento | informação | fim previsto |
|---|---|---|---|---|---|---|---|
| 01 | 412.8 a 421.6 | "Planilha de controle" | contrária ao senso comum | número | contraria o esperado | V-custo | virada que fecha |
| 02 | 95.2 a 101.0 | "Tem uma coisa" | lacuna de curiosidade | nenhum | explicação | nenhuma | muda de assunto |
```

Só depois desta tabela existir é que o julgamento começa. Candidato que nasce já com veredicto é
candidato que nasceu na fase errada.
