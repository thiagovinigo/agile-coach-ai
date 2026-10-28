# O roteiro do reel narrado

O roteiro é escrito por você, a partir da filmagem e dos fatos, e aprovado pela pessoa **antes** de
qualquer crédito de voz. Cada regra aqui já derrubou um roteiro.

## O tamanho

- **De 90 a 130 palavras.** Com a voz natural da ElevenLabs em português, isso dá de 36 a 48 s de fala,
  e o reel fecha entre 40 e 50 s com a cauda do fechamento. O `voz.py` avisa fora da faixa.
- **De 3 a 5 frases longas**, ligadas por "e", "então", "porque", "aí". Frase curta com ponto final
  atrás de ponto final ("Pedido feito. Relatório pronto.") lê como legenda, não como alguém contando.
- Passou do tempo, corte palavra. **Nunca acelere a voz.**

## A forma

```
gancho     o resultado mais surpreendente, dito primeiro, com o nome da coisa e de quem é para
como       o caminho da pessoa pela função: você pede assim, ela faz assado, você muda falando
por quê    o que isso tira da vida dela, em palavra simples
fechamento a frase que fecha e o comentário: "Comenta AGENTE que eu te mando o guia de configuração."
```

O gancho cai em cima do momento real mais forte da filmagem, e o título da abertura é a versão curta
dele. Por isso o título sai das palavras do gancho, e a legenda só começa depois que o título sai.

## As regras de conteúdo

- **Venda a função, não a demonstração.** A voz diz o que a coisa É e o que ela faz PARA quem assiste,
  em afirmação grande e simples. A filmagem é a prova rápida embaixo da afirmação, nunca um passo a
  passo dos personagens, dos dados ou dos cliques da demonstração.
- **No máximo um detalhe concreto por afirmação.** Um número, um nome, um exemplo. Dois já viram
  explicação técnica.
- **Comercial, não técnico.** O que a pessoa ganha e como é fácil, do lado dela: "você diz o que quer,
  ela monta, você muda qualquer coisa falando". Jargão que não vende (API, banco de dados, modelo,
  MP4, integração) sai, a não ser que ele seja o argumento de venda. Se a coisa é personalizável, diga
  e mostre o que dá para mudar: costuma ser o argumento mais forte.
- **Só fato que está na filmagem ou na fonte oficial**, e cada um anotado em `fatos.md` com a prova.
  Na conferência, cada frase é checada contra o que está na tela quando ela é dita
  (`conferencia/afirmacoes.md`). Frase que a tela contradiz sai, por melhor que soe.
- **Diga o que está acontecendo enquanto acontece.** A voz aponta para a tela: quando ela diz
  "a planilha se preenche sozinha", é isso que está na tela.

## O fechamento

- A frase do comentário é a última: **"Comenta PALAVRA que eu te mando <o item concreto>."** O item
  prometido é uma coisa só, com nome: "o guia de configuração", "os três prompts", "o link do teste".
- A PALAVRA é curta, uma palavra só, fácil de digitar e sem acento, porque a pessoa digita no celular e
  o funil compara texto. Se o pacote publica pela Zernio, o `/flow-reels:publicar` confere se a palavra
  está livre antes de montar o funil.
- Na legenda do post, que é do `/flow-reels:publicar`, a PALAVRA vem na primeira linha.

## O texto que vai para a voz

`roteiro-tts.txt` é o roteiro aprovado, exato, sem nota nenhuma. Duas regras:

- **Sem travessão e sem hífen fazendo pausa.** O `voz.py` recusa. Pausa é vírgula, dois pontos ou ponto.
- **Marcação entre colchetes só com `eleven_v3`** (`[animado]`, `[sussurrando]`). Os outros modelos
  leem o colchete em voz alta, e o `voz.py` recusa. O texto limpo, sem marcação, é o ponto de partida;
  marque só a frase que pedir.

Número e sigla: escreva como deve ser falado e conferido na legenda ("três", "dez mil"), porque a
legenda mostra o texto do roteiro, palavra por palavra.

## Como apresentar para aprovação

Em texto, inteiro, com a contagem de palavras, a duração estimada, a PALAVRA, o item e o momento da
filmagem que abre o reel. Espere o sim. Ajuste pedido volta aqui; nenhuma tomada de voz é gerada em
cima de roteiro que a pessoa não aprovou.
