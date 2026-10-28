# Imagens de banco livre e recorte sem fundo

Duas ferramentas para o reel mostrar a coisa nomeada na fala, sem pagar banco de imagem e sem usar
foto de quem não deixou.

## `buscar-imagem.py`: a foto, com licença conferida

```bash
flow-reels componentes/buscar-imagem megafone --saida projetos/<v>/materiais-de-trabalho/corte-01/assets
flow-reels componentes/buscar-imagem "server room" "robot arm" --saida <pasta> --orientacao vertical
```

Busca no **Openverse** (que junta Flickr, Wikimedia, Rawpixel, StockSnap e outros) e no **Wikimedia
Commons**, os dois sem chave. Com chave gratuita no `.env`, soma **Pexels** (`PEXELS_API_KEY`) e
**Pixabay** (`PIXABAY_API_KEY`).

Para cada termo, ele baixa as melhores (6 por padrão) e grava três coisas:

- as imagens, `<termo>-01.jpg`, `<termo>-02.jpg`…;
- o `CREDITOS.md` da pasta, com a página de origem, o autor e a licença de cada arquivo;
- a folha de contato `busca-<termo>.png`, numerada. Olhe antes de escolher.

Licença: por padrão só entra uso comercial liberado sem crédito obrigatório (CC0, domínio público,
licença Pexels, licença Pixabay). `--licenca credito` soma CC BY, que pede o crédito na tela (campo
`credito` do `imagem-cheia`). Nunca entram CC BY-SA, NC ou ND, nem foto marcada no Commons com direito
de imagem de pessoa ou marca registrada.

Busque em inglês quando o português trouxer pouco: os bancos são quase todos em inglês.

## `tirar-fundo.py`: o objeto recortado, para virar adesivo

```bash
flow-reels componentes/tirar-fundo assets/megafone.jpg               # megafone-sem-fundo.png
flow-reels componentes/tirar-fundo assets/robo.jpg --borda 14       # com contorno branco de adesivo
flow-reels componentes/buscar-imagem robot --saida <pasta> --sem-fundo   # busca e recorta
```

Roda na máquina, de graça: o modelo **BiRefNet** (licença MIT) no **onnxruntime**. O modelo tem 224 MB e
é baixado uma vez só, na primeira vez, para `componentes/modelos/`. Cada foto leva de 6 a 10 s.

Recorte bom pede foto com um objeto claro no meio (um megafone, um robô, um celular). Foto de cena
cheia, como uma sala ou uma rua, não tem objeto para recortar: essa vai inteira no `imagem-cheia`.

O PNG recortado entra no reel como **adesivo** do `rosto-vidro` (MOTOR.md 4.2), ao lado da cabeça.
O crédito continua sendo o da foto original, que já está no `CREDITOS.md`.
