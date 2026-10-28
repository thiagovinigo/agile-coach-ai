# Visão melhor: profundidade estável e cabelo no recorte (4.3)

Duas mudanças no `scripts/visao.py`, sem mudar o formato do que ele grava em `visao/` (MOTOR.md 2.6):
os mesmos arquivos, nos mesmos tamanhos (`mascara/m%06d.png` no tamanho de análise, `profundidade/p%06d.png`
em 210 x 364 num 9:16), a mesma régua de 0 a 255. O motor não muda nada para usar.

1. **Profundidade estável no tempo.** Padrão novo: o Video Depth Anything Small (Apache-2.0) no lugar do
   Depth Anything V2 Small quadro a quadro. Os mapas param de piscar: o fundo parado treme 9 vezes menos.
2. **Cabelo no recorte.** O BiRefNet lite (MIT) na caixa da cabeça, em quadros-chave, levado aos quadros do
   meio pelo fluxo óptico. Os fios soltos entram, e a parede entre o cabelo comprido e o pescoço sai.

```
flow-reels produzir/visao --projeto projetos/<v> --corte NN
flow-reels produzir/visao --projeto projetos/<v> --corte NN --cabelo nao
flow-reels produzir/visao --projeto projetos/<v> --corte NN --profundidade dav2
```

## Parâmetros

| opção | o que faz | padrão |
|---|---|---|
| `--profundidade` | `vda`: Video Depth Anything Small, estável no tempo. `dav2`: o Depth Anything V2 Small quadro a quadro, de antes. Sem os dois ONNX do VDA em `componentes/modelos/`, cai no `dav2` com aviso | `vda` |
| `--cabelo` | `auto`: liga quando o tempo estimado do cabelo cabe em 3 min (um reel de até ~1 min). `sim`: liga sempre. `nao`: a máscara de antes (com a profundidade nova). Precisa do `rosto.json` (a caixa da cabeça): sem ele, sai sem o cabelo, com aviso | `auto` |

As constantes (no topo do `visao.py`):

| constante | valor | o que é |
|---|---|---|
| `VDA_JANELA`, `VDA_SOBRA`, `VDA_CHAVES`, `VDA_MISTURA` | 32, 10, [0, 12, 24..31], 8 | as do `infer_video_depth` oficial ("do not change") |
| `CABELO_PASSO` | 10 | um quadro-chave do BiRefNet a cada 10 quadros, e nas pontas de cada trecho |
| `CABELO_FLUXO` | 256 | lado maior da caixa da cabeça no fluxo óptico (Farneback) |
| `CABELO_FORA`, `CABELO_DENTRO` | 0,035 e 0,02 da largura | até onde o BiRefNet pode pôr cabelo além da máscara, e tirar para dentro dela |
| `CABELO_ERRO` | 14 | diferença de luma da imagem levada em que o quadro-chave pesa 37% |
| `CABELO_SEGUNDOS`, `CABELO_QUADRO`, `CABELO_TETO` | 0,6 s; 10 ms + 20 ms por quadro 1080 x 1920; 180 s | a estimativa do `--cabelo auto` |

## A profundidade: Video Depth Anything Small

- **Licença conferida no card** (`huggingface.co/depth-anything/Video-Depth-Anything-Small`: `license:
  apache-2.0`) e no README do repositório ("Video-Depth-Anything-Small model is under the Apache-2.0
  license"; Base e Large são CC-BY-NC-4.0, fora).
- **Não há ONNX oficial.** O único de terceiro achado (518 x 910 fixo, para WebGPU) não serve no tamanho do
  motor. Os dois ONNX foram exportados aqui, num venv temporário com torch (o pacote segue sem torch):
  `componentes/modelos/exportar-modelos-4-3.py` (passos, downloads e o que muda no código original).
  Conferido contra o torch original: erro máximo de 0,6% do valor máximo (364 x 210).
- **Dividido em dois.** O codificador (DINOv2-S) roda quadro a quadro na CPU, na thread de sempre, ao lado
  do MediaPipe. A cabeça temporal roda uma vez por janela de 32 quadros, a cada 22; as 10 primeiras
  entradas da janela são quadros-chave da anterior (as características delas ficam guardadas, o
  codificador não roda de novo). A janela nova vai para a escala da anterior por mínimos quadrados nos dois
  quadros-chave em comum, e os 8 quadros que as duas veem passam de uma para a outra em rampa (o mesmo do
  `infer_video_depth` oficial).
- **A cabeça no CoreML.** No Mac, a cabeça roda no CoreML (ML Program, tamanho fixado por vídeo): 0,22 s
  por janela, contra 1,3 s na CPU. O modelo compilado fica em `~/Library/Caches/fabrica-de-cortes/coreml`
  (a primeira vez leva ~14 s, as outras ~3 s). Sem CoreML, a CPU: mesmo resultado, ~2x o custo do DAv2.
- **Emendas.** Nada atravessa emenda: cada trecho fecha as janelas dele (a última completada com o último
  quadro). Do outro lado da emenda o VDA começa numa escala nova, e o trecho é posto na escala do anterior
  por um ajuste robusto (a média dos 3 primeiros quadros contra a dos 3 últimos de lá; a segunda rodada
  fica com os 70% de pixels que melhor batem).
- Depois, a régua de antes: percentis 1 e 99 do vídeo inteiro e o alisamento no tempo com o portão de
  movimento (`finalizar_profundidade`, que ainda tira um pouco do tremor que sobra: 0,077% para 0,051%).
- A `fundo-profundidade.png` (a do cenário sem você, para a nuvem e a malha) continua do DAv2 numa imagem
  só: o VDA é para vídeo.

### Medido (M4, máquina compartilhada com outras frentes; as rodadas antiga e nova seguidas)

A variação quadro a quadro do mapa (0 a 255), entre vizinhos do mesmo trecho, só onde a imagem quase não
mudou (|Δluma| < 3), em % de 255:

| corte | fundo parado | contorno da pessoa | escala (desvio da mediana do fundo) | pessoa (mediana, Δ por quadro) |
|---|---|---|---|---|
| teste-onda-1 52 (576 x 1024, 36 s, 3 trechos) | 0,467% → **0,050%** | 1,84% → **1,41%** | 0,552% → **0,117%** | 2,82 → **1,15** |
| apis-de-ia-gratis 03 (1080 x 1920, 44 s, 10 trechos) | 0,354% → **0,038%** | 1,28% → **1,18%** | 0,445% → **0,117%** | 2,55 → **0,72** |

- Separação pessoa x fundo (medianas, 0 a 255): 154/12 → 175/4 (52) e 131/14 → 137/9 (03). Na emenda, a
  mediana da pessoa pula o mesmo de antes (média 2,0 e 6,3; máx 4 e 16): é o corte de verdade.
- **Custo da parte profundidade:** só a profundidade (`--so profundidade --refazer`) no corte 52: 71,1 s de
  modelo no DAv2 contra 74,0 s no VDA (**1,04x**; o alvo era < 2x). Na rodada inteira, com o MediaPipe
  disputando a CPU: 113,9 s → 136,7 s (52) e 239,8 s → 252,9 s (03).
- **Memória:** pico de 2,19 → 3,43 GB (52) e 4,57 → 5,83 GB (03). O CoreML da cabeça pesa ~0,55 GB, as
  janelas ~0,25 GB, e a fila folgada da thread (256 quadros pequenos) ~0,1 GB.
- **Limite:** o VDA desenha o fundo mais chapado que o DAv2. O relevo do fundo (p95 - p5 do fundo dividido
  pela separação pessoa x fundo) cai de 0,16 para 0,05 no corte 52; no tamanho nativo do modelo (518) ele
  sobe só para 0,12. Numa parede lisa isso é o certo; a prateleira perto da parede quase some do mapa. A
  peça `profundidade` mostra menos degraus no fundo, e o parallax do fundo usa a `fundo-profundidade.png`
  (que não mudou). Quem quiser o relevo de antes roda com `--profundidade dav2`.

## O cabelo: BiRefNet lite na cabeça

- **Licença:** MIT (código e peso, `huggingface.co/ZhengPeng7/BiRefNet_lite`). O BEN2 (MIT) foi descartado:
  é Swin maior, no mesmo 1024, e o lite já custa o que cabe.
- **Por que outro ONNX.** O `birefnet-general-lite.onnx` do pacote (o do rembg, 1024) faz a convolução
  deformável com Gather/Scatter: ~15 s por quadro na CPU, e o CoreML não ajuda (84 s; o ML Program nem
  compila sem `pads` explícitos). Reexportado do peso oficial com o `DeformConv` nativo do ONNX e entrada
  de 640: **0,5 a 0,7 s por quadro na CPU** (o CoreML dá o mesmo: 0,53 s). A caixa da cabeça cabe em 640
  sem perder fio (comparado com o de 1024 nas mesmas cabeças). Pesos em float16 no arquivo (87 MB).
- **Como entra.** A caixa da cabeça sai do `rosto.json`: 2,6 larguras de rosto centradas nele, do alto da
  pessoa até 0,9 largura de rosto abaixo do queixo (o cabelo comprido cai no ombro). O BiRefNet roda nela a
  cada 10 quadros e nas pontas de cada trecho, e o alfa dele passa por um filtro guiado fino na imagem
  (a borda de 640 vai para a borda de verdade). Cada quadro do meio recebe os dois quadros-chave vizinhos
  levados até ele pelo fluxo (Farneback na caixa reduzida a 256 px; só o alfa é levado no tamanho cheio),
  pesados pela distância no tempo e pela confiança do fluxo (cai onde a imagem levada não bate: a mão que
  passou). Ele só manda numa faixa em volta do contorno da máscara de base (até 3,5% da largura para fora,
  2% para dentro), com a força caindo na borda de baixo e nos lados da caixa. O que ele põe a mais só fica
  onde a profundidade não diz "parede" (abaixo de 0,2 na régua pessoa/fundo sai): sem isso, pedacinhos da
  parede acima do ombro entravam. Ilha solta na caixa sai. Depois, a mesma borda firmada de sempre (abaixo
  de 0,25 é fundo, acima de 0,75 é pessoa): borda firme e sem halo, fio que o BiRefNet viu com força entra
  opaco.
- **O que se vê** (folhas antes/depois da cabeça ampliada sobre rosa chapado, e a `folha-visao.png`): no 1080 x 1920 o cabelo
  comprido do lado sai fio por fio, com o fundo entre os fios; o vão de parede entre o cabelo e o pescoço,
  que a máscara antiga pegava como pessoa, sai; os fios soltos do alto da cabeça entram. No 576 x 1024 a
  diferença é menor (o quadro tem menos fio para mostrar).

### Medido

A variação quadro a quadro da máscara (0 a 255, em 288 px de largura), na faixa de ±3 px da borda, onde a
imagem quase não mudou, em % de 255 (menos = menos tremor):

| corte | borda inteira | só a cabeça | quadros-chave | tempo a mais |
|---|---|---|---|---|
| 52 (576 x 1024, 1084 quadros) | 3,11% → 2,91% (só VDA) → **2,50%** | 3,27% → 2,84% → **2,32%** | 113 | BiRefNet 67 a 70 s + levar ~15 ms/quadro: a rodada vai de 136,7 s (só VDA) a 228 s |
| 03 (1080 x 1920, 1330 quadros) | 3,41% → 3,07% → **2,90%** | 3,79% → 3,44% → **3,24%** | 147 | BiRefNet 88 s + levar ~42 ms/quadro (com um render de outro corte disputando a CPU; sozinho, 29 ms): a fase da máscara vai de 92 s a 236 s, a rodada de 253 s a 414 s |

- **Por reel de 40 s** (1200 quadros): ~130 quadros-chave x 0,6 s ≈ 80 s, mais ~15 ms (576) a ~29 ms
  (1080) por quadro para levar o cabelo: **~100 s em 576 x 1024 e ~115 a 130 s em 1080 x 1920** (o pior
  medido, com a máquina dividida: ~145 s). Por isso o `auto` liga até ~3 min estimados.
- No quadro renderizado (`--quadro` do "100 MIL" atrás da cabeça e das `camadas`, no corte 03): a borda
  do cabelo contra a letra sai nítida, com os fios do alto, onde a antiga era uma borda mole; o resto do
  quadro é o mesmo.
- Duas rodadas dão o mesmo resultado, bit a bit (máscaras e profundidades do corte 52 conferidas por hash,
  com o CoreML na cabeça do VDA).

## O que muda no `visao.json` e no `.origem.json`

```json
{
  "modelos": { "selfie": {...}, "multiclasse": {...}, "profundidade": {...}, "maos": {...}, "corpo": {...},
               "objetos": {...},
               "vda_codificador": {"arquivo": "vda-small-codificador.onnx", "nome": "Video Depth Anything Small, codificador (ONNX)", "licenca": "Apache-2.0"},
               "vda_cabeca": {"arquivo": "vda-small-cabeca.onnx", "nome": "Video Depth Anything Small, cabeça temporal (ONNX)", "licenca": "Apache-2.0"},
               "cabelo": {"arquivo": "birefnet-lite-640.onnx", "nome": "BiRefNet lite, 640 px (ONNX)", "licenca": "MIT"} },
  "caminhos": { "segmentador": "cpu", "maos": "metal", "corpo": "metal", "objetos": "metal",
                "profundidade": "cpu (codificador) + coreml (cabeça temporal)", "cabelo": "cpu" },
  "tempos": { "analise": 95.3, "profundidade": 2.2, "profundidade_modelo": 71.3, "mascara": 121.9,
              "cabelo": 69.9, "fundo": 2.6, "total": 226.5 },
  "profundidade": { "modelo": "vda", "percentis_brutos": [...], "escala": "...", "...": "..." },
  "cabelo": { "passo": 10, "quadros_chave": 113, "segundos": 69.9, "modelo": "BiRefNet lite, 640 px (ONNX)" }
}
```

- `modelos` lista só os modelos usados neste vídeo (o DAv2 sempre: é ele que faz a `fundo-profundidade.png`).
- `profundidade.modelo`: `"vda"` ou `"dav2"`. `cabelo`: `null` quando a máscara saiu sem ele.
- `tempos.profundidade_modelo`: segundos de conta da thread da profundidade (corre junto com a análise).
- `.origem.json` ganha `variantes`: `{"profundidade": "vda" | "dav2", "mascara": "cabelo" | "sem-cabelo"}`.
  A parte pedida só é reaproveitada na mesma variante; a variante só conta para a parte pedida (um
  `--so maos` não derruba a máscara feita com o cabelo).
- Versões: `{mascara: 3, fundo: 4, profundidade: 3, maos: 3, corpo: 2, objetos: 2}`. Quem analisou antes
  refaz a máscara, a profundidade e o fundo (que sai da máscara) na próxima rodada.
- A folha de contato diz, na segunda linha do cabeçalho, o modelo da profundidade e se o cabelo entrou.

## Limites

- O cabelo depende do `rosto.json`: rosto não achado naquele quadro-chave = sem cabelo até o próximo.
- O BiRefNet acha "objeto" em qualquer coisa saliente (o neon ao lado da cabeça): a faixa em volta do
  contorno e o veto pela profundidade seguram; neon colado na cabeça e na mesma distância ainda pode entrar
  numa borda de poucos pixels (a máscara antiga também pegava).
- Fio que o BiRefNet vê fraco (alfa < 0,75) sai pela borda firmada: o recorte fica sem halo, mas o fio
  mais fino do contraluz não entra.
- Cabeça que vira rápido entre dois quadros-chave: o fluxo erra, a confiança cai, e ali vale a máscara de
  base (sem tremor, sem o fio).
- O VDA usa o mesmo tamanho de entrada do DAv2 (~76 mil pixels, 210 x 364). O modelo foi treinado em 518:
  no tamanho nativo a separação e o relevo melhoram um pouco, mas o codificador custa ~2x (fora do alvo).

## Pedidos ao integrador

- MOTOR.md 2.6: trocar "Depth Anything V2 Small" pelo VDA na descrição da profundidade (o DAv2 fica no
  `fundo-profundidade.png` e no `--profundidade dav2`); a máscara ganha o cabelo; versões, `variantes`,
  `profundidade.modelo`, `cabelo`, os tempos novos e a memória (pico 3,4 GB em 576 e 5,8 GB em 1080); as
  opções `--profundidade` e `--cabelo`. Hoje o texto diz `fundo: 3`, e o script já estava em 4.
- `.gitignore`: os três ONNX novos ficam abaixo de 100 MB (42, 14 e 87 MB) e podem ir para o repositório
  como o `depth-anything-v2-small.onnx`; o `birefnet-general-lite.onnx` (o do `tirar-fundo.py`) segue
  ignorado.
- Nenhum pacote pip novo: o `onnxruntime` do `instalar.sh` basta (o `onnx` e o torch só no venv de
  exportação). No Windows não há CoreML: a cabeça do VDA roda na CPU (~2x o DAv2).
