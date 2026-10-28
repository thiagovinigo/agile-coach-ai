# Modelo do brief

Formato de todo brief salvo em `pautas/radar/AAAA-MM-DD-<tema-em-slug>.md`, a entrada tema do `/flow-reels:tendencias`. As cinco seções vêm
nesta ordem, com estes títulos, porque é assim que a pessoa acha o que procura: primeiro o que está
acontecendo, depois o que fazer com isso, e no fim o quanto confiar.

Os textos entre chaves são para trocar. Os comentários `<!-- -->` são instrução, e saem do arquivo
final.

---

```markdown
# Radar: {tema}

| | |
|---|---|
| tema | {tema, do jeito que a pessoa falou} |
| data | {AAAA-MM-DD} |
| janela | {de} a {até} ({N} dias) |
| profundidade | {rápida, padrão ou funda} |
| tipo de pergunta | {recomendação, notícia, como fazer ou geral} |
| fontes | {N} threads do Reddit, {N} histórias do Hacker News, {N} vídeos do YouTube, {N} posts do X, {N} páginas da web |
| passe em inglês | {não precisou, ou: entrou no Hacker News e na web, com o termo "{termo_en}"} |

{Duas a quatro frases com o achado mais importante. É o que a pessoa leria se lesse só isto.}

---

## O que está em alta

<!-- De três a seis achados, do mais forte para o mais fraco. Cada um com fonte, número e link. -->

### {título curto do achado}

{O que está acontecendo, com o detalhe concreto: nome, número, frase de quem falou.}

- fonte: {r/sub, canal do YouTube, @perfil, Hacker News ou site}, {data}
- engajamento: {N votos e N comentários | N pontos e N comentários | N visualizações | N curtidas e N reposts | sem número conhecido}
- link: {url}

### {título curto do achado}

...

---

## O que a comunidade pensa

**Concorda:** {o que é consenso, com a fonte}

**Discute:** {onde a opinião racha, com os dois lados e a fonte de cada um}

**Começa a falar:** {o que aparece em poucos lugares e pode crescer, com a fonte. Se veio do passe em inglês, diga}

---

## Ideias de corte para gravar

<!-- De três a cinco, cada uma presa a um achado, já passadas pelos eliminadores de CRITERIOS.md. Pontuação com a conta, nunca previsão de alcance. -->

### 1. {nome curto da ideia}

- **gancho:** "{a frase completa que a pessoa fala nos primeiros segundos}"
- **formato:** {afirmacao | trajeto}
- **ângulo:** {um dos ângulos de `CRITERIOS.md` seção 3}
- **caminho:** {cenas | mundo | narrado}, {meia frase dizendo por quê}
- **pontuação:** {N}/75, com a conta eixo por eixo em `CRITERIOS.md` seção 2
- **por que agora:** {o achado que sustenta, com o id do radar e o número. Ex.: R3, thread de r/musculacaonatural com 32 comentários}

{Opcional, uma ou duas linhas: o que a pessoa precisa ter em mãos para gravar. O laudo, a tela do app, o estudo aberto.}

### 2. {nome curto da ideia}

...

---

## Cobertura por fonte

<!-- Honesta. Copie da cobertura que o radar imprime e acrescente a web. -->

| fonte | resultado |
|---|---|
| Reddit | {N itens (português N, inglês N) | limitado (429) | vazio de verdade | ...} |
| Hacker News | {...} |
| YouTube | {N vídeos, N com transcrição | não instalado | ...} |
| X | {N posts | não configurado} |
| Web | {N páginas, de {domínio}, {domínio} | ...; diga se precisou do inglês} |

{Ressalvas, se houver: "o Reddit respondeu 429 no caminho e a lista pode estar incompleta", "a
conversa forte do Reddit é de comunidades da Argentina e do México".}

Material bruto: `pautas/radar/.bruto/{AAAA-MM-DD}-{tema-em-slug}/`
```

---

## O que não entra no brief

- previsão de alcance ou de desempenho das ideias (a pontuação dos critérios entra, com a conta);
- número estimado, arredondado "para cima" ou tirado da memória;
- achado sem link;
- recomendação de ferramenta para produzir o vídeo. O pacote cuida disso quando o vídeo chegar.
