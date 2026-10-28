# A página de revisão

É o portão. Corte só existe depois que alguém assistiu e aprovou aqui.

**A regra, antes de qualquer instrução:** entrega de vídeo não se aprova por print no chat, nem por
lista de arquivo, nem por "ficou bom?" seguido de um "ficou". Se a pessoa não assistiu o corte
rodando, com som, do começo ao fim, o corte não está aprovado. Vale para o primeiro lote e vale para
o décimo, inclusive quando o único ajuste foi trocar uma palavra da legenda.

O motivo é simples: defeito de vídeo mora no tempo. Legenda que atropela a fala, emenda que dá para
ouvir, painel que fica parado meia frase, respiração cortada no meio. Nada disso aparece em quadro
congelado, e tudo isso aparece nos primeiros dez segundos de reprodução.

## Os arquivos desta pasta

| arquivo | o que é |
|---|---|
| `modelo.html` | a página, genérica. Ela não sabe nada sobre o seu vídeo: lê tudo do `revisao.json` que estiver ao lado dela |
| `exemplo.revisao.json` | um exemplo preenchido com dois cortes fictícios. É ele que documenta o formato, campo por campo |
| `nova-revisao.py` | varre um projeto, acha os cortes prontos, escreve o `revisao.json` e sobe o servidor |
| `COMO-USAR.md` | este arquivo |

Nada aqui é editado por lote. O que muda de um lote para o outro é o `revisao.json`, que nasce
dentro da pasta do projeto.

## 1. Gerar

Da raiz do pacote:

```
flow-reels produzir/nova-revisao projetos/<seu-video>
```

O script procura o `.mp4` dentro de cada pasta `corte-NN`, que na árvore de hoje guarda só a
entrega, mede cada um com o ffprobe, lê o `brief.md` em
`materiais-de-trabalho/corte-NN/brief.md`, e escreve dois arquivos:

```
projetos/<seu-video>/revisao/revisao.json
projetos/<seu-video>/revisao/revisao.html
```

Opções, todas dispensáveis:

| opção | para que serve |
|---|---|
| `--lote "Nome do lote"` | o título que aparece no cabeçalho. Sem isso, usa o nome da pasta |
| `--porta 8791` | outra porta. O padrão vem de `porta_revisao` no `setup.json` |
| `--sem-servidor` | só gera os arquivos |
| `--refazer` | joga fora os textos escritos na rodada anterior e começa em branco |

Rodar de novo é seguro: o script re-mede os vídeos e atualiza a lista de cortes, mas **preserva os
textos** que você já escreveu. Só o `--refazer` apaga.

## 2. Preencher os campos de julgamento

O script preenche o que dá para medir: identificador, caminho do vídeo, duração, formato. Os quatro
campos que sobram são de julgamento, e eles são a razão de a página existir:

| campo | o que escrever |
|---|---|
| `titulo` | nome curto e humano do corte |
| `gancho` | o texto exato do gancho, palavra por palavra, do jeito que é ouvido |
| `porque` | duas ou três frases defendendo a escolha daquele trecho |
| `decisoes` | os pontos em que a produção escolheu um caminho e quer confirmação |

Quem escreve é o agente que produziu os cortes, editando o `revisao.json` antes de chamar a pessoa.
O script avisa no terminal quais blocos ainda estão vazios.

**Página sem esses campos vira uma pilha de vídeos.** A pessoa assiste, sente que tem algo estranho e
não consegue nomear, porque não sabe o que estava sendo tentado. Com o gancho escrito e a decisão
exposta, a resposta vem específica: "a emenda em 6,4 s dá para ouvir, refaz".

Escreva `decisoes` de verdade ou mande a lista vazia. Item inventado só para não deixar o campo vazio
treina a pessoa a pular a seção inteira.

## 3. Servir e revisar

O próprio script sobe o servidor e imprime o endereço:

```
http://localhost:8790/revisao/revisao.html
```

O servidor nasce na pasta do projeto, e é por isso que o caminho do vídeo no JSON começa com `../`:
a página está em `projetos/<video>/revisao/` e o vídeo em `projetos/<video>/corte-NN/`. **É esse par
que faz o player tocar, e mover qualquer um dos dois quebra a revisão sem quebrar nada visível
antes.** Digitar só `localhost:<porta>` também funciona: o servidor redireciona para a página, sem
deixar arquivo nenhum na pasta do vídeo.

Deixe a janela do terminal aberta enquanto a revisão acontece. `Ctrl+C` encerra.

**Não abra o `revisao.html` com dois cliques.** No modo `file://` o navegador bloqueia a leitura do
JSON e do vídeo, e a página não carrega. Ela detecta isso e explica o que fazer, em vez de mostrar
tela branca, mas o caminho certo continua sendo o endereço `http://localhost`.

Na página, cada corte tem o player, o gancho em destaque, a defesa da escolha, as decisões em aberto,
dois botões e um campo de anotação. Clicar de novo no mesmo botão volta o corte para pendente. As
respostas ficam guardadas no navegador, por lote, então dá para fechar a aba, dormir e voltar no dia
seguinte.

Reprovar sem anotação é o único erro de uso que a página não consegue impedir. Sem o motivo escrito, a
produção adivinha, e adivinhação vira uma segunda rodada igual à primeira.

## 4. Devolver o feedback

O botão **Copiar feedback** monta um texto pronto, com o placar, o estado de cada corte, o gancho e a
sua anotação. Cole no chat, e a produção continua dali. Se o navegador bloquear a cópia automática, a
página abre uma caixa com o texto selecionável.

O texto sai mais ou menos assim:

```
REVISÃO: Café em casa | primeiro lote
Vídeo: 2026-09-14-cafe-em-casa
Placar: 1 aprovados, 1 reprovados, 0 pendentes.

[APROVADO] corte-01: O moedor importa mais que o grão
  Gancho: "Você pode comprar o café mais caro da cidade que..."
  Anotação: (nenhuma)

[REPROVADO] corte-02: Os trinta segundos que ninguém espera
  Gancho: "A parte mais importante do preparo acontece antes..."
  Anotação: o cronômetro parece enfeite, troca pelo contador
```

Corte reprovado volta para a produção com essa anotação na mão. Depois de refazer, gere a revisão de
novo: os textos continuam lá, e é só reabrir a página e reavaliar o que mudou.

## Quando alguma coisa não aparece

| sintoma | o que é |
|---|---|
| "Nenhum corte pronto" no terminal | não tem `.mp4` dentro de nenhuma pasta `corte-NN` do projeto |
| a página abre sem nada e reclama do `revisao.json` | o arquivo não está ao lado do `revisao.html`. Gere de novo com o script |
| o player aparece preto e não toca | o caminho em `arquivo` está errado. Ele é relativo à página, e por padrão é `../corte-NN/corte-NN.mp4` |
| o corte não aparece na lista | o MP4 não está em `corte-NN/corte-NN.mp4`. Material de trabalho fica em `materiais-de-trabalho/corte-NN/`, e o script não procura lá |
| a duração e o formato saem em branco | o ffprobe não está instalado ou não está no PATH. Rode o `instalar` do pacote |
| a porta está ocupada | o script sobe na próxima porta livre e avisa. A revisão anterior provavelmente ficou aberta em outro terminal |
