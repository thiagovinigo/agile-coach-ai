# O funil: comenta a palavra, recebe o link na DM

O que acontece entre o comentário e o link chegando, o que é criado na Zernio, e como consertar
quando emperra. **Este arquivo é o dono das regras da palavra e do texto da DM.** Quem precisar de
um desses números procura aqui, e não copia para outro lugar.

## A conversa inteira

```
alguém comenta "guia" num post do Instagram
        │
        ├─ a automação responde em público      "Mandei na sua DM, da uma olhada."
        └─ a automação manda a DM com o link dentro do texto
```

Acabou. Não existe segundo passo, não existe pergunta no meio, não existe formulário. Quem comentou
recebe o link na primeira mensagem.

**Um objeto por palavra**, a automação de comentário (`POST /comment-automations`), criada sem
`platformPostId`. Sem esse campo ela vale para a conta inteira, então um objeto cobre todos os posts
que imprimem aquela palavra, inclusive os que você publicar meses depois.

Duas escolhas do create que não são óbvias:

- `matchMode: "word"`, porque o default `contains` dispara a automação quando a palavra aparece
  dentro de outra palavra.
- `typoTolerance: true`, que só funciona em `matchMode: "word"`.

### Por que a DM entrega direto, sem pedir email

Uma versão anterior deste funil mandava a DM com um botão, esperava a batida, pedia o email e só
então entregava o link. Saiu inteira, de propósito. Cada passo a mais entre o comentário e o arquivo
é um lugar onde a pessoa desiste e um lugar onde o funil quebra sem ninguém ver. Se um dia a captura
de email voltar, ela volta como decisão de produto, não como remendo aqui.

## A palavra

- **Formato**: 2 a 40 caracteres, começa com letra ou número, depois letras, números e hífen.
- **Guarde sempre em minúscula.** O gate casa sem ligar para caixa: `GUIA` e `guia` são a mesma
  automação, e é por isso que a legenda pode escrever a palavra em maiúscula sem quebrar nada.
- **Ela nunca é devolvida.** A automação não tem validade e não é apagada, só desligada, então ela
  sobrevive à legenda, ao post e à vontade de reusar a palavra em outra oferta.
- Antes de escolher uma palavra nova, veja o que já está em uso:

```bash
flow-reels publicar/zernio palavras
```

- Aposentar uma oferta é `isActive: false`, nunca `DELETE`:

```bash
flow-reels publicar/zernio funil-desligar <automationId>
flow-reels publicar/zernio funil-ligar  <automationId>
```

O objeto vivo é o que permite voltar atrás em segundos, e a palavra fica reservada de qualquer jeito.

## O texto

| Momento | Padrão do script |
|---|---|
| resposta pública no comentário | `Mandei na sua DM, da uma olhada.` |
| DM | uma linha de agradecimento, o link, e um convite a responder ali mesmo |

Os dois saem em português, como todo o resto do pacote. Publicando para um público de outra língua,
escreva os textos no spec, em `textos.resposta_comentario` e `textos.dm`.

Três regras do texto da DM:

- **ele precisa conter o link**, e o script recusa criar o funil se não contiver. Uma DM que promete
  e não entrega é pior que nenhuma DM;
- o texto cabe em cerca de **1000 caracteres**, que é o limite da Meta para esse campo. O script
  avisa quando passa, em vez de bloquear, porque o limite é aproximado;
- não nomeie arquivo interno. Quem recebe é um estranho, e `corte-03-v2-final.pdf` não diz nada a
  ele.

Depois que o funil existe, **a Zernio é a dona da copy**: editar é no painel dela. Por fora, é
`PATCH /comment-automations/{id}` com `dmMessage`.

## O link

Ele é conferido anonimamente antes da criação, como um estranho veria. Link que responde página de
login entrega um muro de login na DM, o que é pior que não entregar nada. Arquivo em nuvem privada
precisa ficar como "qualquer pessoa com o link" antes de virar oferta.

## Um segundo post com a mesma oferta

Não crie funil de novo. A automação vale para a conta inteira, então basta escrever a mesma palavra
na legenda do post novo e publicar. Uma palavra, um funil, para sempre.

## Depurar

| Sintoma | Causa provável | Conserto |
|---|---|---|
| comentei e não veio DM | dedupe por usuário: quem já recebeu DM daquela automação fica `skipped` num comentário novo | testar com um perfil que nunca recebeu, ou responder na própria thread |
| comentei e não veio DM | a automação está desligada | `funil-ligar <automationId>` |
| a palavra não pegou | a legenda escreveu a palavra grudada em outra, e `matchMode: "word"` casa palavra inteira | escreva a palavra sozinha na legenda |
| criei duas vezes sem querer | a segunda criação foi recusada pela conferência de palavra | confira em `palavras` qual das duas está ativa |
| a DM chegou cortada | o texto passou do limite da Meta | encurte o texto e mande `PATCH dmMessage` |

## Onde ficam os contatos

Na Zernio, em `GET /contacts` e `GET /conversations`. Não existe base espelho em lugar nenhum, e este
pacote não guarda nem exporta nada sobre quem comentou.
