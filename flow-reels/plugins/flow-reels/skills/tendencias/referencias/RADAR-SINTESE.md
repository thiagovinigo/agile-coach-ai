# Como sintetizar

Depois das buscas você tem uma pilha de achados de quatro ou cinco fontes. A síntese transforma a
pilha num sinal: o que está em alta, o que a comunidade pensa, e o que disso vira corte.

---

## 1. Fique no que a pesquisa disse

O brief existe para trazer o que o seu treino não tem. Então a base é o achado, e não a sua memória
sobre o tema.

- **Nome exato.** Se o achado fala de "Claude Code", é Claude Code, e não "assistentes de código em
  geral".
- **Frase de quem falou.** O comentário mais votado de uma thread é melhor que qualquer resumo seu.
- **O que a fonte diz, e não o que você acha que o tema é.** Se a pessoa pediu creatina e a conversa
  do mês é um estudo sobre câncer, o brief é sobre o estudo, mesmo que você soubesse dez outras
  coisas sobre creatina.

## 2. Pese pelo engajamento

| sinal | peso |
|---|---|
| thread com mais de 100 votos e mais de 50 comentários | muito alto |
| post do X com mais de 500 curtidas | muito alto |
| vídeo com mais de 100 mil visualizações dentro da janela | muito alto |
| o mesmo achado no Reddit, no YouTube e num blog | muito alto |
| thread entre 20 e 50 votos | alto |
| história do Hacker News entre 20 e 100 pontos | alto |
| thread com menos de 10 votos | médio |
| post do X com menos de 50 curtidas | médio |
| blog genérico sem comentário | baixo |

O número sempre acompanha o achado no brief. Achado sem número conhecido entra dizendo isso, nunca
com número estimado.

## 3. Procure cinco coisas

1. **Consenso**: o que todo mundo concorda. É o sinal mais forte, e o corte menos surpreendente.
2. **Contradição**: onde as fontes discordam. Costuma ser o achado mais interessante, e o melhor
   corte de `afirmacao`.
3. **O que começa a aparecer**: assunto novo que só poucos estão falando. É oportunidade, e é onde o
   passe em inglês mais ajuda: o que está grande lá fora e pequeno aqui.
4. **Recomendação com nome**: ferramenta, técnica, produto citado. É o que vira lista e tutorial.
5. **Alerta**: o que as pessoas avisam para não fazer. Corte de "o erro que todo mundo comete" sai
   daqui.

## 4. A síntese por tipo de pergunta

**Recomendação.** Conte as menções, ordene por menção e engajamento.

```
1. Creatina monohidratada: 5 menções
   - r/musculacaonatural (32 comentários): "é a com mais estudo que comprova"
   - YouTube, Escolha Certa (64 mil visualizações): teste de laudo de 5 marcas
2. Gominha de creatina: 2 menções
```

**Notícia.** Linha do tempo, com o fato que mais mexeu primeiro.

```
O fato: estudo na Nature Communications ligou creatina a metástase em camundongo
- 2026-09-24: Hacker News discute o estudo oposto, creatina e imunidade (186 pontos)
- semana seguinte: quatro vídeos brasileiros sobre "creatina causa câncer?"
- o que a comunidade diz: estudo em camundongo, dose alta, não muda a recomendação
```

**Como fazer.** As técnicas que mais fontes validam, e os erros que mais fontes apontam.

**Geral.** O clima, os temas e onde a opinião racha.

## 5. Das cinco coisas às ideias de corte

Cada ideia sai de um achado, e o tipo do achado sugere o corte:

| o achado é | a ideia costuma ser | formato provável |
|---|---|---|
| uma contradição | tomar um lado, com a prova | `afirmacao` |
| um mito circulando | desfazer o mito | `afirmacao` |
| uma técnica validada | mostrar a técnica funcionando | `trajeto` |
| uma lista de recomendações | as três que mais aparecem, com o porquê | `afirmacao` ou `trajeto` |
| algo novo que está chegando | "testei e isso aconteceu" | `trajeto` |
| um lançamento ou notícia | o que mudou e para quem importa | `afirmacao`, muitas vezes no caminho `narrado` |

As regras de cada campo da ideia estão no `SKILL.md`, etapa 2, e no `CRITERIOS.md`.

## 6. Antes de mostrar, confira

1. A síntese bate com o que os achados dizem? Releia um contra o outro.
2. Cada afirmação tem uma fonte com nome?
3. Os números são do radar ou da página, e não estimados?
4. Tem pelo menos uma contradição ou nuance? Se tudo concorda, você pode estar simplificando.
5. As ideias são deste tema, com estes achados, ou serviriam para qualquer tema? Se serviriam para
   qualquer um, refaça.
6. Cada gancho, lido em voz alta, funciona como a primeira frase de um vídeo para quem nunca te viu?
