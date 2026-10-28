# Modelo de brief

O `brief.md` é o contrato de um corte. Ele é escrito pelo `/flow-reels:planejar` depois da aprovação
do gancho e lido pelo `/flow-reels:produzir` na hora de produzir.

**Regra que justifica o arquivo existir:** o que não estiver escrito aqui vira improviso na hora de
renderizar, e improviso na hora de renderizar é a diferença entre um corte e cinco cortes parecidos.

Um por corte, em `projetos/<video>/materiais-de-trabalho/corte-NN/brief.md`. Copie o bloco abaixo, troque tudo que está
entre `<` e `>`, e apague as linhas que começarem com `nota:` depois de preencher.

Nada de campo vazio. Se um campo não se aplica, escreva o motivo em uma frase.

---

```markdown
# Corte <NN>: <nome curto, só para achar o arquivo>

- Vídeo de origem: <nome da pasta em projetos/>
- Candidato no pool: <número do candidato em GANCHOS.md>
- Duração prevista: <38.2> s
- Data do plano: <AAAA-MM-DD>

## 0. Valor

- Formato: <afirmacao | trajeto>
- O que a pessoa aprende: <uma frase, no formato "depois de assistir, a pessoa sabe / sabe fazer /
  percebe que ...", copiada do GANCHOS.md>
- Tipo de valor: <V-passo | V-resultado | V-crenca | V-criterio | V-custo>
- Âncora: <a palavra concreta que o gancho nomeou e que o corpo inteiro paga: planilha de gasto>
- Se o formato é trajeto, os quatro blocos: <resultado prometido / caminho em N etapas / onde o
  resultado aparece / qual é o destino>

nota: os tipos e as três conferências do aprendizado estão em referencias/VALOR.md, seção 1. Esta
seção vem antes do gancho de propósito: se ela não fecha, o corte não deveria existir, por melhor que
seja a abertura.
nota: o formato é declarado ANTES da seleção, em referencias/FORMATOS.md, e é ele que diz quais
regras valeram. No trajeto os quatro blocos são obrigatórios: faltando um, o corte não é trajeto e
este brief está descrevendo outra coisa.

## 1. Gancho

> <o texto exato do gancho, palavra por palavra, do jeito que vai ser ouvido>

- Span na transcrição: <412.8 a 421.6> s, contínuo
- Duração falada do gancho: <9.2> s
- Repetição de palavra removida: <não> ou <sim, a segunda ocorrência de "o" em 414.2 s>
- Leitura fria (subagente, que só viu o texto acima):
  1. Do que está falando: <...>
  2. O que promete: <...>
  3. O que faltou: <...>
- Contexto que falta: <uma frase> ou <nenhum>
- Como o contexto é pago: <o segmento 2, papel contexto, dos 388.1 s> ou <não se aplica, nada falta>
- Eliminadores: E1 olhos fechados <passa>, E2 assunto nomeado <passa>, E3 span contínuo <passa>,
  E4 promessa paga <passa>, E5 tese nova <passa>, E6 trabalho nomeado <passa, e a condição que
  torna a afirmação usável é esta, dita dentro do span: ...>

nota: os seis eliminadores estão em referencias/GANCHO.md, seção 3, e qualquer um deles derruba o
candidato. O E6 é o que pega a afirmação condicional cuja condição ficou no vídeo: se aqui estiver
escrito que a condição é paga por um segmento de contexto, o candidato caiu e ninguém percebeu.
Se algum falhou, este corte não deveria existir. Os antigos testes T1 a T7 não existem mais: eles
foram absorvidos pelos seis, e a tabela de quem absorveu o quê está no mesmo arquivo.
nota: o gancho é UM span contínuo do áudio. Se aqui aparecer mais de um trecho, o candidato caiu no
E3 e não deveria ter chegado ao brief. Costurar trechos distantes é liberdade do corpo, que aparece
na seção 3 deste brief, e nunca do gancho.
nota: a leitura fria é copiada do subagente, palavra por palavra. Quem planejou o corte não a
escreve, não a resume e não a melhora, porque quem escolheu o candidato já sabe qual é o assunto.
nota: "Contexto que falta" nunca fica vazio. Vazio não é "não falta nada", é campo não preenchido.

## 2. Payoff

<uma frase só: o que o corte entrega para fechar a lacuna que o gancho abriu>

- Onde o payoff é dito: <1507.9 a 1527.8> s
- O payoff entrega o aprendizado da seção 0: <sim> ou <o aprendizado foi corrigido para baixo, e a
  nova frase é esta, já atualizada na seção 0>
- A última frase volta à âncora da seção 0: <sim, ela termina em "planilha">

nota: as seis regras que escolheram este corpo estão em referencias/VALOR.md, seção 3. A que fecha
aqui é a R6, volta à âncora.

## 3. Segmentos

Na ordem em que tocam no corte, que não precisa ser a ordem do vídeo: o corpo pode montar minuto 4,
depois minuto 1, depois minuto 2. Qual é essa ordem depende do formato declarado na seção 0, e as
duas estão logo abaixo da tabela: **gancho, contexto, prova, fechamento** na afirmação,
**promessa, caminho, resultado, destino** no trajeto.

| # | papel | entrada (s) | saída (s) | duração | na linha do tempo | fala |
|---|---|---|---|---|---|---|
| 1 | gancho | <412.72> | <421.94> | <9.22> | <0.00 a 9.22> | "<primeiras palavras... últimas palavras>" |
| 2 | contexto | <388.10> | <392.05> | <3.95> | <9.22 a 13.17> | "<a frase que nomeia a ferramenta e o resultado>" |
| 3 | desenvolvimento | <730.31> | <735.40> | <5.09> | <13.17 a 18.26> | "<...>" |
| 4 | payoff | <1507.88> | <1527.77> | <19.89> | <18.26 a 38.15> | "<...>" |

Os papéis dependem do formato declarado na seção 0. Todo segmento tem exatamente um.

- **afirmacao:** `gancho`, `contexto`, `desenvolvimento`, `payoff`. `gancho` e `payoff` aparecem uma
  vez cada; `contexto` e `desenvolvimento` podem se repetir. A ordem é gancho, contexto, prova,
  fechamento.
- **trajeto:** `gancho` (a promessa), `desenvolvimento` (uma etapa do caminho por segmento),
  `payoff` (o resultado acontecendo) e `destino` (para onde ir depois, último segmento, e o único
  lugar onde identidade e nome de canal podem aparecer). Não existe `contexto` aqui, porque quem
  paga o contexto é a promessa.

- Todos os pontos validados com `scripts/energia_audio.py`: <sim>
- Pontos que precisaram sair do tempo da palavra: <o ponto 3 moveu de 730.4 para 730.31, porque a
  palavra começava dentro da inspiração>
- Referências soltas conferidas: <sim, nenhum "isso" ou "ele" aponta para fora do corte> (regra R4)
- Uma ideia só, nada aqui é de outro assunto: <sim> (regra R2)
- O corte termina em conclusão e na âncora: <sim>

nota: o procedimento e as margens estão em referencias/CORTE-LIMPO.md. As seis regras que decidem
quais trechos entram estão em referencias/VALOR.md, seção 3.

nota sobre o papel `contexto`: ele existe **só no formato afirmação**, e **só quando** a seção 1
registrou contexto de identidade faltando. O
trecho quase sempre vem de **antes** do gancho no vídeo, porque é lá que a pessoa disse do que estava
falando, e toca **depois** do gancho no corte, como segmento 2. Nunca antes: o gancho é o primeiro
som do corte, e abrir pela explicação entrega contexto a quem ainda não tem motivo para querer
contexto. Com "Contexto que falta: nenhum", este papel não aparece e o segmento 2 já é a prova. Se o
vídeo não tem nenhuma frase que pague a dívida, o corte não existe, e o candidato volta ao pool como
descartado com o motivo "sem trecho de contexto disponível".

## 4. O mundo do painel

- Superfície: <escura|clara>
- Objeto herói: <nome da peça em componentes/REGISTRO.md>
- Por que esta peça: <uma frase ligando a peça ao conteúdo da fala>
- Estados do herói: <planilha-cheia, abandonada, linha-unica>
- Peças de apoio: <chip-numerado, rotulo>
- Coisas concretas que a fala deste corte nomeia, e a rota de cada uma no INVENTARIO.md:
  <a planilha, mock lista-de-itens; o aplicativo de mensagem, logo logos/whatsapp.svg> ou <nenhuma, o
  corte inteiro é ideia abstrata>
- Beat-sheet: `beats.yaml` <número de beats>, cadência <1.8> s em média

nota: o formato do beats.yaml está em referencias/BEAT-SHEET.md. O painel mostra a coisa de que a
fala fala, nunca as palavras da legenda.
nota: as rotas vêm prontas de materiais-de-trabalho/INVENTARIO.md, escrito no passo 0. Se uma coisa
nomeada neste corte não estiver lá, a decisão volta para o inventário, não se resolve no brief.

## 5. Especificações técnicas

| item | valor |
|---|---|
| entrega | MP4 1080x1920, 30 fps, H.264, faststart, SAR 1:1 |
| painel de cima | 1080x956, autorado a 12 fps, segurado em 30 |
| face embaixo | 1080x964 |
| legenda | 116 px, uma linha, centrada na costura (Alignment 5) |
| fonte | <a fonte de legenda declarada em marca/tokens.json, que precisa ser instância estática> |
| grão | sempre, por cima de tudo |

- Vídeo de origem (face): `<caminho do arquivo>`
- Áudio de validação: `projetos/<video>/materiais-de-trabalho/transcricao/audio16k.wav`
- Saída: `projetos/<video>/corte-NN/corte-NN.mp4`

## 6. O que este corte não é

<uma ou duas linhas dizendo o que ficou de fora de propósito, para a produção não tentar incluir.
Exemplo: não entra a parte da comparação entre aplicativos, que vira o corte 03>
```

---

## Como o criador lê este arquivo

| seção | o que a produção faz com ela |
|---|---|
| 0 | confere, no corte pronto, se quem assiste sai sabendo a frase declarada. Se não sai, o corte volta |
| 1 e 2 | confere se o corte montado ainda cumpre a promessa depois de renderizado |
| 3 | monta a linha do tempo da face e do áudio, na ordem e nos papéis declarados |
| 4 | entrega ao subagente que desenha o painel, junto com o `beats.yaml` |
| 5 | parâmetros de render e de queima de legenda |
| 6 | evita o improviso de "já que estamos aqui, vamos colocar também" |

Se a produção precisar mudar um tempo da seção 3, ela volta e **corrige o brief**. Brief que não bate
com o arquivo entregue é pior que brief nenhum, porque a próxima rodada confia nele.
