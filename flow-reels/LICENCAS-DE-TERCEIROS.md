# Licenças de terceiros

O Flow Reels roda inteiro na sua máquina e só usa peças de uso comercial liberado. Esta é a lista do que
vem dentro do pacote e não foi escrito por nós.

## Bibliotecas (em `componentes/vendor/`)

| peça | licença | onde está o texto |
|---|---|---|
| three.js r170 | MIT | `componentes/vendor/three/LICENSE` |
| opentype.js | MIT | `componentes/vendor/opentype/LICENSE` |
| GSAP 3 (com CustomEase, Flip e SplitText) | GSAP Standard "No Charge" License: uso gratuito, inclusive comercial; não vale para ferramenta que concorra com o Webflow | https://gsap.com/standard-license |

## Modelos (em `componentes/modelos/`)

| modelo | licença |
|---|---|
| MediaPipe: detector de rosto, Face Landmarker, mãos, corpo, segmentadores de pessoa, EfficientDet Lite0 | Apache-2.0 (Google) |
| Depth Anything V2 Small | Apache-2.0 |
| Video Depth Anything Small (só o Small; o Base e o Large não entram, porque são não comerciais) | Apache-2.0 |
| BiRefNet lite (o recorte de cabelo, e o general lite que o tirar-fundo baixa no primeiro uso) | MIT |

A origem, o tamanho e o sha256 de cada arquivo estão em `componentes/modelos/LEIA.md`. O texto da Apache-2.0
está em https://www.apache.org/licenses/LICENSE-2.0 e o da MIT em https://opensource.org/license/mit.

## Fontes (em `marca/fontes/`)

Quicksand e JetBrains Mono, sob a SIL Open Font License 1.1 (`marca/fontes/OFL.txt` e
`marca/fontes/OFL-JetBrainsMono.txt`).

## Trilhas (em `componentes/trilhas/`)

Todas do Freesound, em domínio público (CC0). Autor e página de cada uma em `componentes/trilhas/CREDITOS.md`.

## Sons e LUTs

Os efeitos sonoros de `componentes/sons/` e as LUTs de `componentes/luts/` são gerados pelo próprio pacote
(`gerar_sons.py` e `gerar_luts.py`).

## Logos de marcas (em `componentes/marcas/` e `componentes/logos/`)

Os logos são marcas registradas das empresas donas delas, baixados dos kits de imprensa oficiais, do SVGL
e do Simple Icons (os desenhos do Simple Icons são CC0). Eles entram no reel para **se referir ao
produto** de que você fala, sem alterar cor nem proporção e sem sugerir parceria ou patrocínio. A origem
e a regra de uso de cada logo estão em `componentes/marcas/_acervo.json` e `componentes/logos/_acervo.json`.
Marca que pede aceite de termo de uso (por exemplo, a da OpenAI) não vem no pacote: quem quiser aceita os
termos e baixa com `flow-reels componentes/baixar-marca`.
