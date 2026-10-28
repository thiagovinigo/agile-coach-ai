# Critérios: o que vira pauta

A busca traz de 150 a 300 itens. Este arquivo é a lei de como eles viram cinco pautas. Ele existe
porque "o que está bombando" não é o mesmo que "o que vai bombar no seu Instagram": o post com mil
upvotes no r/LocalLLaMA sobre quantização de pesos é tendência, e é inútil para um reel.

A ordem é a mesma do planejador de cortes: **primeiro elimina, depois pontua, e nunca ao mesmo
tempo.**

---

## 1. Os eliminadores

Qualquer um derruba o item, sozinho. Não se pontua item eliminado.

| eliminador | derruba quando |
|---|---|
| **P1, sem fonte oficial** | não existe página oficial, repositório ou anúncio da própria empresa para linkar e conferir. Rumor, vazamento e "ouvi dizer" caem aqui. No tema que não é ferramenta (saúde, finanças, comportamento), a fonte é a **primária**: o estudo, o órgão, o documento, e não a matéria sobre ele |
| **P2, não verificável** | os fatos que fariam o reel valer (preço, número, o que faz) não se confirmam abrindo a fonte oficial |
| **P3, já gravado** | o assunto, ou a mesma ferramenta, já tem pasta em `projetos/`, ou a palavra de chamada já foi usada em outra oferta |
| **P4, não se mostra** | não existe nada visual para o painel: nem site, nem demo, nem interface, nem resultado. Reel de ideia pura no nicho de ferramenta morre em três segundos |
| **P5, fora do público** | só serve para quem já é especialista profundo (pesquisa de modelo, infraestrutura de GPU, paper). O público do criador quer usar, não treinar |
| **P6, risco** | golpe, cripto, conteúdo adulto, polêmica política, ferramenta que viola termos de uso de outra, ou que expõe dado de terceiro |

## 2. A pontuação

Cada item sobrevivente recebe de 0 a 5 em sete eixos. O peso diz o que mais pesa no Instagram de
quem é referência em IA e automação.

| eixo | peso | 5 é | 0 é |
|---|---|---|---|
| **novidade** | 3 | lançado ou viralizou nos últimos 3 dias | tem mais de um mês |
| **valor imediato** | 3 | grátis, open source, economiza dinheiro ou horas, substitui algo pago | só é interessante |
| **encaixe no nicho** | 3 | o centro do nicho de `setup.json` → `pautas.nicho` (no pacote de exemplo: Claude Code, Codex, n8n, agentes, MCP). Na entrada tema, o centro do tema pedido | a borda do nicho, ou outro assunto |
| **mostrável** | 2 | tem demo, interface bonita, antes e depois visível | só texto |
| **concreto** | 2 | tem número verificável: estrelas, preço, tempo, idiomas, "3 segundos de áudio" | só adjetivo |
| **tração** | 1 | topo da fonte (upvotes, estrelas na semana, pontos) | sem sinal |
| **acessível** | 1 | quem não programa entende em uma frase | precisa de aula antes |

Pontuação final = soma de nota × peso, máximo 75. Anote a conta no `RANKING.md`, eixo por eixo.
Número sem conta não se confere.

**Tração pesa pouco de propósito.** Ela diz que o assunto já está sendo falado, e isso é metade do
valor: a outra metade é o criador chegar primeiro em português. Um repositório com 400 estrelas
lançado ontem, grátis e que se mostra bem, ganha de um com 20 mil estrelas lançado há dois meses.

## 3. O ângulo decide o formato

Todo item que passa ganha um ângulo, que é a promessa do gancho. Os que já funcionaram no perfil:

| ângulo | quando usar | exemplo que já foi ao ar |
|---|---|---|
| **alternativa grátis a algo pago** | a ferramenta faz o que uma paga faz | OmniVoice contra ElevenLabs |
| **acabou de lançar** | lançamento de empresa grande ou produto que o público conhece | Pomelli |
| **N ferramentas que você precisa ter** | três a cinco itens do mesmo tipo na mesma semana | cinco plugins para Claude Code |
| **resolve uma dor conhecida** | a ferramenta tira um incômodo que todo mundo tem | Humanizer, texto com cara de IA |
| **como eu faço** | bastidor de uso real, com resultado | corte do ECC corrigindo bug pelo print |
| **erro que todo mundo comete** | existe um jeito errado comum e a ferramenta ou técnica conserta | usar o comando errado no Claude Code |

"N ferramentas" é o único ângulo que junta itens: ele pode fundir três achados que sozinhos seriam
fracos. Os outros são de um item só.

## 4. O que vai para a vitrine

A conversa recebe **as cinco pautas mais bem pontuadas**, cada uma com:

- o gancho proposto, escrito como vai ser falado;
- o ângulo, entre parênteses;
- uma linha de "por que agora" (o sinal de novidade e tração, com a fonte);
- o link oficial.

Não vão: a contagem de itens levantados, quantos caíram e por qual eliminador. Isso fica no
`RANKING.md`, que é o estoque, e ela pode pedir. Mesma regra da vitrine do planejador de cortes.
