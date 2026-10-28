# Modelos de cenas por ângulo

O ponto de partida do `cenas.json` para os cinco ângulos que mais aparecem nos reels de IA e
automação. O modelo dá a ordem das cenas, o modo de cada uma e a transição. Os tempos saem da fala
gravada (`palavras-corte.json`): os segundos abaixo são de um reel de 45 s e servem só de proporção.

Como usar: escolha o ângulo pela fala (a pauta já diz qual é), copie a sequência, encaixe cada cena
na frase que ela mostra e ajuste pela `CENAS.md`. Uma cena por ideia vale mais que o modelo: se a fala
não tem o beat, a cena sai.

Em produção, três ou quatro transições com efeito por reel bastam (o gate avisa acima de 8 por
minuto). O resto é `corte`.

## 1. Grátis × pago

"O ElevenLabs cobra, o VoiceStudio faz de graça."

| beat | tempo | modo | entrada | o que entra |
|---|---|---|---|---|
| gancho | 0–3 s | `rosto-vidro` | — | o preço do pago num `numero` com prefixo, aceso na palavra "cobra" |
| a virada | 3–7 s | `lado-a-lado` | `clarao` | pago × grátis, com logo e preço; `vencedor` na palavra "grátis" |
| prova | 7–20 s | `tela-bolha` | `bolha-encolhe` | a gravação da ferramenta grátis, foco no resultado, uma marca com rótulo |
| o que ela faz | 20–30 s | `lista` | `bolha-expande` | três a cinco coisas que a grátis faz como a paga |
| a ressalva | 30–37 s | `rosto-vidro` | `corte` | um `selo` com o limite honesto ("só em inglês", "fila de espera") |
| chamada | 37–45 s | `tipografia` | `zoom-desfoque` | a frase final, com a palavra da DM no `destaque` |

## 2. Lista de N

"Cinco plugins do Claude Code que eu uso todo dia."

| beat | tempo | modo | entrada | o que entra |
|---|---|---|---|---|
| gancho | 0–3 s | `rosto-vidro` | — | o `numero` N grande, com o rótulo do que é |
| item a item | 3–36 s | `imagem-cheia` (print ou arte) ou `tela-bolha` (demo), uma cena por item | `chicote` entre os itens | `rotulo` com o número e o nome do item |
| recapitulação | 36–41 s | `lista` | `lamina` | os N itens, cada um com o visto |
| chamada | 41–45 s | `rosto-vidro` | `corte` | `selo` com a palavra da DM |

Com mais de cinco itens, a recapitulação vira a cena principal: uma `lista` só, com os itens entrando
na fala, e as demos ficam para os dois itens mais fortes.

## 3. Notícia ou lançamento

"A OpenAI acabou de lançar o agente que mexe no seu navegador."

| beat | tempo | modo | entrada | o que entra |
|---|---|---|---|---|
| gancho | 0–3 s | `rosto-vidro` | — | `selo` "novo" com o logo da empresa |
| a notícia | 3–10 s | `manchete` | `bolha-encolhe` | o print oficial, contorno no título ou na data |
| o número | 10–16 s | `rosto-vidro` | `bolha-expande` | o `numero` do anúncio, com a `fonte` |
| como funciona | 16–30 s | `tela-bolha` | `lamina` | a demo, com dois ou três focos |
| o que muda | 30–38 s | `lado-a-lado` | `corte` | antes × depois, `vencedor` no depois |
| chamada | 38–45 s | `tipografia` | `zoom-desfoque` | a pergunta para os comentários |

## 4. Tutorial de tela

"Em três passos você liga o n8n no WhatsApp."

| beat | tempo | modo | entrada | o que entra |
|---|---|---|---|---|
| gancho | 0–3 s | `rosto-vidro` | — | o resultado pronto, num card de `imagem` |
| passo a passo | 3–36 s | `tela-bolha`, uma cena por passo | `bolha-encolhe` no primeiro, `lamina` entre os passos | `foco` no clique do passo; marca com rótulo "1 · conecte", "2 · …" |
| recapitulação | 36–41 s | `lista` | `corte` | os passos, cada um com o visto |
| chamada | 41–45 s | `rosto-vidro` | `corte` | `selo` com a palavra da DM, que entrega o modelo pronto |

A gravação de tela com a webcam num canto vai inteira em `tela-bolha` com `bolha.caixa_rosto`; marque
só tela parada (a marca não acompanha rolagem).

**Em mundo** (o caminho `mundo`, MOTOR.md 4.14), quando a fala aponta para um objeto o corte inteiro:

| beat | superfície | o que a câmera e o mundo fazem |
|---|---|---|
| gancho | `quadro` | o objeto grande no quadro 0 e a frase do gancho se montando em até 5 palavras dentro do mundo |
| o objeto precisa da tela inteira (o comando, a fórmula) | `tela` | o card cresce até virar a tela; a câmera aproxima no que a fala nomeia (zoom de leitura até 1,32) |
| cada passo | `quadro` | uma chave de câmera por ideia, presa à palavra (até 7 no corte); algo novo entra no mundo a cada 1 a 2 s |
| a frase que é a pessoa ("o que eu mais gosto...") | `rosto` | o card grande do rosto, 1 a 2 s, e a volta para o mundo com o soco de câmera |
| chamada | `pip` ou `quadro` | a caixa de comentário com a palavra dentro do mundo, o rosto em cena |

Numa gravação de tela com a webcam num canto, o mundo é a própria tela (`fonte: { "video": "principal",
"caixa": [...] }`) e o rosto entra pelo `pip` com `rosto.caixa` e `recorte: false`.

## 5. Opinião ou tese

"Sua empresa é AI First? Talvez ela seja só um megafone pro erro."

| beat | tempo | modo | entrada | o que entra |
|---|---|---|---|---|
| gancho | 0–1,5 s | `tipografia` | — | a pergunta que provoca, com a palavra-chave no `destaque` |
| a metáfora | 1,5–3,5 s | `imagem-cheia` | `clarao` | a imagem da metáfora (foto livre, com crédito) |
| a prova | 3,5–9 s | `manchete` | `bolha-encolhe` | o print com o número, contorno nele |
| o número | 9–13 s | `rosto-vidro` | `bolha-expande` | o `numero` com a `fonte`, aceso na palavra que pesa |
| a consequência | 13–19 s | `lista` | `chicote` | o que dá errado, item a item |
| o contraponto | 19–26 s | `rosto-vidro` ou `tela-bolha` | `corte` ou `lamina` | a objeção, e a prova contra ela |
| a tese | 26–31 s | `tipografia` | `corte` | a frase-tese |
| a aplicação | 31–37 s | `painel-rosto` ou `lado-a-lado` | `corte` | o caminho em passos, ou o contraste |
| chamada | 37–45 s | `tipografia`, depois `rosto-vidro` | `zoom-desfoque` | a pergunta, depois o `selo` da DM |

Este é o reel de teste da Fábrica 2.0. O plano inteiro, aprovado nos nove gates, está em
`EXEMPLO-CENAS.json`.
