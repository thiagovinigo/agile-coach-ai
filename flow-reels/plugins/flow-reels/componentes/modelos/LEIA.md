# Modelos do pacote

Pesos de modelo que os scripts do pacote usam, todos rodando local. Só entra aqui modelo com licença que
permite uso comercial (MIT, Apache, BSD, CC0...), baixado da fonte oficial do autor. Cada script lista os
que usa no dicionário `MODELOS` dele (nome do arquivo, nome do modelo, licença).

| arquivo | modelo | licença | origem | tamanho | quem usa |
|---|---|---|---|---|---|
| `face_landmarker.task` | MediaPipe Face Landmarker (float16, com os 52 blendshapes e a matriz da pose) | Apache-2.0 | `https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task` (Google, baixado em 8/10/2026) | 3.758.596 bytes (3,6 MB), sha256 `64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff` | `scripts/expressao.py` (4.3) |
| `vda-small-codificador.onnx` | Video Depth Anything Small, o codificador (DINOv2-S), exportado do original | Apache-2.0 (só o Small; o Base e o Large são CC-BY-NC) | código `github.com/DepthAnything/Video-Depth-Anything` (main) e peso `huggingface.co/depth-anything/Video-Depth-Anything-Small/resolve/main/video_depth_anything_vits.pth` (baixados em 8/10/2026), exportados com `exportar-modelos-4-3.py vda` | 44.374.911 bytes (42 MB), sha256 `ab9aeaeedf16806faff9cd2ce3bf5c89099f75d9da3679df105ae756e92427db` | `scripts/visao.py` (4.3, profundidade) |
| `vda-small-cabeca.onnx` | Video Depth Anything Small, a cabeça DPT temporal (janela de 32 quadros) | Apache-2.0 | o mesmo de cima | 14.583.076 bytes (14 MB), sha256 `5cbabc90604e9b4e833b2f48a68b790da0c0429403028a107a42910ca983362f` | `scripts/visao.py` (4.3, profundidade) |
| `birefnet-lite-640.onnx` | BiRefNet lite (general, Swin-T), entrada fixa de 640, DeformConv nativo | MIT | `huggingface.co/ZhengPeng7/BiRefNet_lite` (`birefnet.py`, `BiRefNet_config.py`, `model.safetensors`, baixados em 8/10/2026), exportado com `exportar-modelos-4-3.py birefnet --lado 640` | 91.638.802 bytes (87 MB), sha256 `cb67152957f0fae7045b11f2c8d3cbceceab4c15bbe502c47ec51f961d8af965` | `scripts/visao.py` (4.3, cabelo) |

Os outros arquivos desta pasta (segmentadores, mãos, corpo, objetos, profundidade) estão no `MODELOS` do
`scripts/visao.py`, com nome e licença.

## Como baixar de novo

Sem `curl | python` (o hook do projeto bloqueia): use o urllib do próprio Python, numa pasta vazia, e mova
o arquivo para cá depois de conferir o tamanho e o sha256 acima.

```python
import urllib.request
url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task"
open("face_landmarker.task", "wb").write(urllib.request.urlopen(url, timeout=120).read())
```

O `.task` é um zip com quatro modelos TFLite (o detector de rosto, a malha de 478 pontos, o modelo dos
blendshapes e a geometria da pose). No Mac, o caminho de CPU dos landmarkers do MediaPipe aborta: o
`expressao.py` testa e usa o Metal (delegate GPU), em modo VIDEO e com imagem SRGBA.

## Os ONNX exportados da visão 4.3

O Video Depth Anything Small e o BiRefNet lite não têm ONNX oficial no tamanho que o `visao.py` usa, e o
pacote não tem torch. Eles foram exportados uma vez, num venv separado e temporário, pelo
`exportar-modelos-4-3.py` desta pasta (a docstring dele tem os passos, os downloads e o que muda em relação
ao código original). Para refazer, siga a docstring (exportado com torch 2.14.1, opset 17 no VDA e 19 no
BiRefNet; duas exportações seguidas da cabeça do VDA deram o mesmo arquivo, byte a byte; com outra versão
do torch o sha256 pode mudar, e o resultado tem de ser conferido com o `--conferir`).

- Os três guardam os pesos em float16 com um Cast para float32 (o arquivo fica abaixo de 100 MB e a conta
  continua em float32). Medido contra o float32: erro máximo de 0,05% (VDA) e 0,0006 no alfa (BiRefNet).
- O VDA exportado bate com o torch original a 0,6% do valor máximo (364 x 210) e 0,9% (280 x 504), quase
  tudo da posição do DINOv2 interpolada pelo tamanho em vez do fator.
- O `birefnet-general-lite.onnx` (o do rembg, 1024, que o `componentes/imagens/tirar-fundo.py` usa) é o
  mesmo modelo, mas faz a convolução deformável com Gather/Scatter: ~15 s por quadro na CPU, contra
  ~0,5 a 0,7 s do `birefnet-lite-640.onnx`. O `tirar-fundo.py` continua com o dele.
- O Base e o Large do Video Depth Anything são CC-BY-NC (não comerciais): nunca entram aqui.
