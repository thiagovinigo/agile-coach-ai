# Como pesquisar

Este arquivo manda em três decisões da entrada tema do `SKILL.md` (etapa 1B): o que buscar na web, em quais subreddits
brasileiros procurar, e quanto peso cada fonte leva. Reddit, Hacker News, YouTube e X vêm do
`scripts/radar/radar.py`. As consultas daqui são o complemento do WebSearch, para blog, notícia e
documentação.

---

## 1. O assunto central vem antes de qualquer busca

Tire do tema o enfeite do pedido e fique com o substantivo:

| a pessoa disse | o assunto central |
|---|---|
| "o que tá em alta sobre creatina" | creatina |
| "me dá ideias de corte sobre agentes de IA para programar" | agentes de IA para programar |
| "melhores dicas de renda fixa" | renda fixa |
| "best Claude Code skills" | Claude Code skills |

**Só se tira palavra, nunca se acrescenta.** Se ela disse "IA para gerar imagem", a busca não vira
"Midjourney". O seu treino pode estar velho, e o motivo de pesquisar é justamente saber o que mudou.

O script faz essa limpeza sozinho, em português e em inglês. Você só precisa passar o tema do jeito
que ela falou e o termo em inglês.

---

## 2. As consultas da web, por tipo de pergunta

Rode em português primeiro. Se vier pouco, troque `{tema}` por `{termo_en}` e rode de novo, em
inglês. `{ano}` é o ano corrente.

### Recomendação ("qual a melhor X")

| # | consulta | para quê |
|---|---|---|
| 1 | `melhores {tema} {ano}` | listas e comparativos recentes |
| 2 | `{tema} vale a pena` | review com opinião |
| 3 | `{tema} comparativo` | quem testou mais de um |
| 4 | `{tema} site:x.com` | só sem `XAI_API_KEY`, e sem número |

### Notícia ("o que tá acontecendo com X")

| # | consulta | para quê |
|---|---|---|
| 1 | `{tema} notícia {ano}` | cobertura da imprensa |
| 2 | `{tema} lançamento` ou `{tema} anúncio` | o que saiu oficialmente |
| 3 | `{tema} estudo` | quando o assunto é ciência ou saúde |
| 4 | `{tema} site:x.com` | só sem `XAI_API_KEY` |

### Como fazer ("como fazer X", "dicas de X")

| # | consulta | para quê |
|---|---|---|
| 1 | `como {tema} {ano}` | guias publicados |
| 2 | `{tema} passo a passo` | tutorial |
| 3 | `{tema} erros comuns` | o que dá errado |
| 4 | `{tema} boas práticas` | o que funciona |

### Geral

| # | consulta | para quê |
|---|---|---|
| 1 | `{tema} {ano}` | o que saiu recente |
| 2 | `{tema} opinião` | quem se posicionou |
| 3 | `{tema} polêmica` | onde a discussão racha |

Na rápida, as três ou quatro primeiras da tabela. Na padrão, a tabela inteira e mais duas ou três
buscas puxadas pelo que o radar trouxe: se o Reddit falou de um produto específico, busque o
produto. Na funda, some buscas pelas pessoas que apareceram como autoridade, pelos assuntos
vizinhos que surgiram, e comparações "X vs Y" quando houver alternativa na mesa.

---

## 3. Subreddits brasileiros: a heurística

O Reddit global puxa a conversa de qualquer país que use a mesma palavra. "Creatina" é romeno,
espanhol e italiano também, e uma busca sem direção devolve r/gymRO e r/FitnessArgentina. Para
trazer o Brasil, passe em `--subreddits` dois a quatro subreddits brasileiros que caibam no tema.

Isso é heurística, não lista fixa: escolha pelo assunto, e não passe nenhum quando o tema não tem
casa óbvia aqui. A tabela é o ponto de partida.

| o tema é de | subreddits que costumam render |
|---|---|
| programação, carreira em tecnologia, IA aplicada a código | `brdev`, `programacao`, `devBR` |
| carreira, emprego, salário, entrevista | `conselhodecarreira`, `brdev`, `empregos` |
| investimento, finanças pessoais, renda fixa, ações | `investimentos`, `farialimabets`, `financaspessoais` |
| treino, suplemento, dieta | `musculacaonatural`, `academia`, `nutricao` |
| saúde, medicamento, bem-estar | `saude`, `medicina` |
| comportamento, notícia, política, cotidiano | `brasil`, `brasilivre`, `desabafos` |
| jogos | `gamesEcultura`, `jogatina` |
| empreendedorismo, marketing, pequeno negócio | `empreendedorismo`, `marketingdigital` |

Três cuidados:

- **o subreddit precisa existir.** Se a lista do radar voltar vazia para um deles, ele pode ter outro
  nome ou estar fechado. Tire e siga;
- **subreddit demais custa 429.** Cada um soma uma busca e duas listagens ao pedido. Quatro é o teto;
- **a busca global continua rodando junto.** Os subreddits brasileiros acrescentam, não substituem,
  e é por isso que o brief precisa dizer de onde vem cada conversa.

---

## 4. Quanto vale cada fonte

| fonte | peso | por quê |
|---|---|---|
| thread do Reddit com 50 votos ou mais e discussão ativa | alto | validada pela comunidade, opinião de verdade |
| post do X com muito engajamento | alto | sinal de que o assunto está quente agora |
| vídeo do YouTube com muita visualização na janela | alto | gente assistindo, e a transcrição diz o que foi dito |
| história do Hacker News com 100 pontos ou mais | alto | discussão técnica funda, quase sempre em inglês |
| blog ou portal de quem entende do assunto | médio a alto | argumento costuma ser mais pensado |
| thread do Reddit com menos de 10 votos | médio | opinião real, pouco validada |
| matéria de portal de notícia | médio | atual, mas muitas vezes rasa |
| blog genérico | baixo | pode ser texto feito para buscador |

**O mesmo achado em duas fontes vale mais que qualquer um sozinho.** Reddit e YouTube falando da
mesma coisa na mesma semana é o sinal mais forte que esta pesquisa produz.

### O engajamento da web

O radar traz os números das quatro fontes dele. Na web, olhe a data da publicação (prefira dentro
da janela), quem assina, quantos comentários a página tem e a data de atualização.

---

## 5. Erros comuns

1. **Pôr na busca o que você sabe.** Busque o que a pessoa disse.
2. **Tratar toda fonte igual.** 500 votos no Reddit pesam mais que um blog sem comentário.
3. **Esconder a contradição.** Se o Reddit diz que funciona e o YouTube diz que é golpe, os dois
   entram. A contradição é o achado.
4. **Filtrar data demais.** Thread antiga que ganhou comentário esta semana ainda é conversa de agora.
5. **Parar na primeira página.** Veio pouco? Reformule e busque de novo, e só então conclua que o
   assunto está frio.
6. **Confundir o Brasil com o mundo.** Achado em inglês ou de outro país entra dizendo de onde é.
