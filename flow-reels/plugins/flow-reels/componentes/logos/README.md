# O acervo de logos

Esta pasta guarda os logos de verdade que o painel usa. Ela existe por causa de um defeito real:
quando faltava o arquivo, o agente desenhava uma forma parecida com o logo da marca. Sai pior do que
não mostrar nada. Quem conhece a marca vê o erro no primeiro segundo, e quem não conhece aprende
errado.

> **Regra dura, sem exceção.** Marca só aparece com o logo de verdade. Nunca uma forma parecida,
> nunca uma aproximação, nunca um ícone genérico no lugar de uma marca nomeada. Se o logo não está
> aqui, existem duas saídas: baixar, ou não mostrar a marca e resolver o beat com palavra.

## Como o painel usa

O parâmetro `marca` do `tile-de-logo` é o nome do arquivo daqui, sem a extensão:

```js
FC.criar("tile-de-logo", { marca: "claude", nome: "claude", tamanho: 200 });
```

Faltou o arquivo, a peça não inventa desenho nenhum: ela pinta a falta hachurada no quadro, escreve
qual arquivo falta e qual comando resolve, e grita no console, que o `painel.py` imprime no fim do
render. É feio de propósito, para você ver antes do seu público ver.

## O que já está aqui

Vinte marcas, cobrindo redes sociais, ferramentas de IA, ferramentas de trabalho e navegadores.
Todas vieram do Simple Icons, todas são **silhuetas de uma cor só**. A coluna da cor oficial está aí
para você decidir se a silhueta basta (leia a seção seguinte).

| marca | arquivo | categoria | cor oficial |
|---|---|---|---|
| Instagram | `instagram.svg` | rede social | `#FF0069` |
| YouTube | `youtube.svg` | rede social | `#FF0000` |
| TikTok | `tiktok.svg` | rede social | `#000000` |
| X | `x.svg` | rede social | `#000000` |
| WhatsApp | `whatsapp.svg` | rede social | `#25D366` |
| Claude | `claude.svg` | ferramenta de IA | `#D97757` |
| OpenAI | `openai.svg` | ferramenta de IA | `#412991` |
| Google Gemini | `googlegemini.svg` | ferramenta de IA | `#8E75B2` |
| Perplexity | `perplexity.svg` | ferramenta de IA | `#1FB8CD` |
| Hugging Face | `huggingface.svg` | ferramenta de IA | `#FFD21E` |
| Notion | `notion.svg` | ferramenta de trabalho | `#000000` |
| Slack | `slack.svg` | ferramenta de trabalho | `#4A154B` |
| Figma | `figma.svg` | ferramenta de trabalho | `#F24E1E` |
| Canva | `canva.svg` | ferramenta de trabalho | `#00C4CC` |
| GitHub | `github.svg` | ferramenta de trabalho | `#181717` |
| Google Drive | `googledrive.svg` | ferramenta de trabalho | `#4285F4` |
| Zoom | `zoom.svg` | ferramenta de trabalho | `#0B5CFF` |
| Google Chrome | `googlechrome.svg` | navegador | `#4285F4` |
| Firefox | `firefox.svg` | navegador | `#FF7139` |
| Safari | `safari.svg` | navegador | `#006CFF` |

O arquivo `_acervo.json` guarda essa mesma ficha em formato de máquina, com a origem de cada desenho.
Quem escreve nele é o `baixar-logo.py`. Não edite na mão.

## Silhueta de uma cor, e quando ela não basta

Os SVG do Simple Icons são **monocromáticos**: a forma é a da marca, a cor é uma só, e o `tile-de-logo`
pinta essa forma com a tinta do painel (e com a cor de contraste quando o tile está aceso). Isso não é
recolorir a marca de ninguém, porque o arquivo já vem sem cor de marca nenhuma.

**A silhueta basta quando** a marca aparece como objeto, como ícone dentro de um tile, como marca
dágua, como item de uma lista de ferramentas, ou seja, quando ela serve para o público reconhecer
qual ferramenta é. É o caso da grande maioria dos beats.

**A silhueta não basta quando** a cor é parte do que está sendo dito. Os três casos que aparecem de
verdade:

1. o beat fala da própria marca, do rebrand, da identidade dela;
2. o público precisa distinguir duas marcas que têm silhueta parecida e cor diferente;
3. o logo oficial é multicolorido e a versão de uma cor não é reconhecível, que é o caso do Google
   Chrome, do Firefox e de vários logos de plataforma.

Nesses casos, traga o logo colorido oficial:

1. baixe o SVG ou PNG na página de imprensa da própria marca (procure por "brand assets", "press kit"
   ou "logo download");
2. salve nesta pasta com um nome claro, por exemplo `chrome-colorido.svg`;
3. no painel, use o parâmetro `imagem` em vez de `marca`:

```js
FC.criar("tile-de-logo", { imagem: "logos/chrome-colorido.svg", nome: "chrome", tamanho: 200 });
```

Com `imagem`, o arquivo entra exatamente como ele é. O tile nunca recolore, nunca aplica a cor de
destaque por cima, nunca inverte. Cor de marca dos outros não é nossa para mexer.

## Como adicionar um logo que falta

O script ao lado faz o trabalho. Ele roda com Python puro, sem instalar nada.

```bash
cd componentes/logos

flow-reels componentes/baixar-logo                     # ajuda e lista do que já existe
flow-reels componentes/baixar-logo --listar            # só a lista
flow-reels componentes/baixar-logo slack               # baixa uma marca
flow-reels componentes/baixar-logo slack trello figma  # baixa várias
flow-reels componentes/baixar-logo "google docs"       # nome com espaço entre aspas
flow-reels componentes/baixar-logo notion --forcar     # rebaixa por cima do que já existe
```

O script acha o nome certo sozinho: você escreve "Google Docs" e ele salva `googledocs.svg`. Errou o
nome, ele sugere os parecidos que existem. A marca não existe na fonte, ele diz isso com todas as
letras e não grava arquivo nenhum, porque arquivo vazio na pasta é pior do que arquivo ausente: o
painel acharia que tem logo.

## As marcas que não existem no Simple Icons

Algumas marcas grandes pediram para sair do acervo, ou nunca entraram. Conferido em setembro de 2026,
estas **não estão lá** e o script vai dizer isso:

| marca | onde pegar o oficial |
|---|---|
| LinkedIn | <https://brand.linkedin.com/> |
| Microsoft Excel, Word, Teams, Edge e o resto do Office | <https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks> |
| Visual Studio Code | <https://code.visualstudio.com/brand> |
| ChatGPT (a marca do produto; a do laboratório está aqui como `openai.svg`) | <https://openai.com/brand/> |
| Cursor, Midjourney, Runway, DeepSeek, Mistral e boa parte das ferramentas novas de IA | página de imprensa de cada uma |

Para qualquer uma delas o caminho é o mesmo: baixar o arquivo oficial, salvar aqui, usar com o
parâmetro `imagem`. E vale repetir: se você não conseguir o arquivo, não desenhe. Tire a marca do
beat e diga o nome dela com palavra.

## Licença e uso, o que eu encontrei

A fonte é o **Simple Icons** (<https://simpleicons.org>), e os arquivos crus vêm de
`https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg`.

O que a leitura da licença e do aviso do próprio projeto diz, em resumo honesto:

- o projeto Simple Icons é publicado sob **CC0 1.0 Universal**, ou seja, os mantenedores abrem mão
  dos direitos autorais sobre o trabalho deles, e você pode usar, redistribuir e usar comercialmente
  sem pedir permissão e sem atribuir;
- o próprio projeto avisa que CC0 no projeto **não** implica CC0 em cada ícone, porque cada desenho é
  de uma marca. Quando o projeto conhece a licença específica de um ícone, ela vem no índice, e o
  `baixar-logo.py` guarda essa informação no `_acervo.json` quando ela existe;
- direito de marca é coisa separada de direito autoral. Nenhuma licença te dá o direito de sugerir
  patrocínio, parceria ou endosso de uma marca que não é sua. Mostrar o logo do Claude ao falar do
  Claude é uso descritivo, e é o que este acervo serve. Colocar o logo na sua capa como se a marca
  assinasse o seu conteúdo é outra conversa, e aí você precisa olhar as diretrizes da marca;
- o projeto pede que quem usa leia o aviso completo em
  <https://github.com/simple-icons/simple-icons/blob/develop/DISCLAIMER.md> e respeite as diretrizes
  de cada marca. Fica aqui o mesmo pedido.

Em uma frase: a licença resolve o arquivo, não resolve a marca. Use logo para identificar a
ferramenta de que você está falando, e não para insinuar que ela está com você.
