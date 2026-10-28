# Mudanças

## 3.0.0

A Fábrica de Cortes virou o plugin **Flow Reels**. Tudo o que a 0.2.0 fazia continua, e a pasta
`marca/` e as pastas de `projetos/` feitas antes abrem nesta versão sem migrar nada.

### Mudou o jeito de usar

- **Um plugin do Claude Code, com comandos curtos**: `/flow-reels:fabrica`, `:tendencias`, `:marca`,
  `:transcrever`, `:planejar`, `:produzir`, `:publicar` e `:narrado`. Os nomes antigos (`flow-fab-de-cortes`,
  `pautas-de-reels`, `dna-da-marca`, `planejador-de-cortes`, `criador-de-cortes`, `publicar-cortes`)
  saíram.
- **O código mora no plugin e os seus arquivos na sua pasta.** `setup.json`, `.env`, `marca/`,
  `projetos/` e `pautas/` ficam na pasta onde você abre o Claude Code, e uma atualização do plugin
  nunca mexe neles. Logo, trilha ou imagem que você baixa vai para `componentes/` da sua pasta e vale
  por cima do que o pacote traz.
- **Um comando para todos os scripts**: `flow-reels <skill>/<script>`, que já usa o Python da sua pasta
  e o ffmpeg certo (`flow-reels lista` mostra todos, `flow-reels instalar` prepara uma pasta nova).
- **Instalar pelo zip ou por marketplace.** O zip já registra o marketplace e liga o plugin quando você
  abre a pasta.

### Novo

- **O reel inteiro em cenas.** O corte deixou de ser só "painel em cima, rosto embaixo": cada trecho é
  uma cena com um modo (rosto com cards de vidro, tela com bolha, imagem cheia, manchete, lado a lado,
  lista, tipografia, painel + rosto), com legenda que acende palavra a palavra e desvia do rosto, um
  editor de fala que tira silêncio, hesitação e frase repetida, e efeitos sonoros discretos.
- **Liquid Glass**: a cena numa placa de vidro grossa que inclina, gira e mergulha.
- **Tela cortada e visão**: o vídeo separado em camadas 3D, texto atrás de você, profundidade estável
  (Video Depth Anything Small), recorte com cabelo (BiRefNet), mãos, corpo e objetos.
- **Modo mundo**, que veio do layout motion da 0.2.0, reescrito para o motor: a coisa de que se fala
  ocupa a tela e uma câmera calma passeia por ela (no máximo 7 movimentos, ou parada), com o rosto
  entrando como respiro num card com a cabeça saindo pela borda. A câmera anda no navegador, então o
  texto fica nítido em qualquer zoom, e a cabeça sai pela máscara da visão, sem modelo GPL.
- **Tempos presos à palavra** em todo o plano: `{"ancora": "planilha#2"}` no lugar do segundo, e o
  plano se recalcula sozinho quando o corte muda de duração.
- **Linguagens do episódio**: 12 direções de arte (vidro, terminal, cinema, recorte, sci-fi, anos 80,
  mangá, profundidade 3D, editorial, turbo, calmo, manchete), três sugeridas por reel sem repetir as
  últimas.
- **Looks, pós e acabamento**: 14 filtros no vídeo, 13 efeitos sobre o quadro inteiro com a legenda
  sempre nítida, LUTs da marca, grão e vinheta.
- **Mãos, rosto e frames 3D**: gestos e expressões como gatilho de efeito; iPhone 3D, parede de telas,
  câmera 2.5D, dolly zoom, polaroid.
- **Transições e palavras**: glitch, VHS, queima de filme, pixels, persianas, cubo, tinta; palavra que
  decodifica, neon, carimbo, cromado.
- **Som**: 15 famílias de efeitos sintetizados, com variações, nunca em cima da sílaba tônica.
- **13 gates automáticos** antes da revisão: ritmo, zonas seguras, contraste, legenda × rosto,
  sincronia, emendas, volume, excesso de efeito, entrega, som, linguagem, variedade e modo mundo.
- **Capa** de todo reel, montada sobre a sua foto.
- **Logos em cor** de 91 marcas de tecnologia, com versão para fundo escuro e claro; **imagens de banco
  livre** com a licença conferida e o crédito registrado; **recorte de fundo** local.
- **Tendências**, num modo só, com duas entradas: o seu nicho (Reddit sem chave com voto real, YouTube
  Brasil, GitHub Trending, Hacker News, Product Hunt) ou um tema que você traz (a pesquisa do radar da
  0.2.0: Reddit, Hacker News, YouTube com transcrição, X com chave, web, em português e em inglês). Cada
  pauta escolhida vira roteiro medido na sua fala, fatos com link e kit de gravação.
- **Reel narrado** (`/flow-reels:narrado`), que veio na 0.2.0: reel sem rosto, com voz da ElevenLabs por
  cima de filmagem real, cartão de abertura com o logo em cor, empurrão e anel no que a voz nomeia e o
  fechamento "comenta a PALAVRA". Leito e efeitos saem de graça das trilhas e dos sons do pacote; os da
  ElevenLabs são opcionais. A voz precisa de `ELEVENLABS_API_KEY` e `ELEVENLABS_VOICE_ID`.

## 0.2.0

Layout motion, radar de tendências, reel narrado opcional e recorte de pessoa opcional.

## 0.1.0

A primeira versão: do vídeo longo ao corte vertical com painel animado em cima, rosto embaixo e
legenda queimada, com onboarding da marca, transcrição, levantamento de ganchos, página de revisão e
publicação opcional.
