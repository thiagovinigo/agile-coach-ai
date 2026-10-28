#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tirar-fundo.py  ·  recorta o objeto da foto e devolve um PNG sem fundo

Para o adesivo do vídeo: o megafone, o robô, o celular que entram flutuando ao lado do rosto. Roda
na máquina, sem conta e sem serviço pago: o modelo BiRefNet (licença MIT) no onnxruntime. O modelo
fica em componentes/modelos/birefnet-general-lite.onnx (224 MB, baixado uma vez pelo instalador; se
faltar, este script baixa).

Uso
---
    flow-reels componentes/tirar-fundo foto.jpg                       grava foto-sem-fundo.png ao lado
    flow-reels componentes/tirar-fundo a.jpg b.png --saida <pasta>     várias, numa pasta
    flow-reels componentes/tirar-fundo foto.jpg --borda 14             contorno branco de adesivo, em px
    flow-reels componentes/tirar-fundo foto.jpg --sem-aparar           mantém o quadro inteiro da foto

O PNG sai aparado em volta do objeto (com uma folga pequena). Recorte bom pede foto com um objeto
claro no meio; foto de cena cheia (uma sala, uma rua) não tem "objeto" para recortar.
"""

import argparse
import sys
import time
import urllib.request
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

AQUI = Path(__file__).resolve().parent
# baixado uma vez para a pasta de trabalho (componentes/modelos/), ou o que já veio no plugin
MODELO = fabrica.achar("componentes/modelos/birefnet-general-lite.onnx")
if not MODELO.is_file():
    MODELO = fabrica.raiz() / "componentes" / "modelos" / "birefnet-general-lite.onnx"
URL_MODELO = ("https://github.com/danielgatis/rembg/releases/download/v0.0.0/"
              "BiRefNet-general-bb_swin_v1_tiny-epoch_232.onnx")
LADO = 1024
LADO_MAX = 1600  # o adesivo ocupa no máximo meio quadro de 1080: mais que isso é peso à toa
MEDIA = (0.485, 0.456, 0.406)
DESVIO = (0.229, 0.224, 0.225)


def garantir_modelo():
    if MODELO.is_file() and MODELO.stat().st_size > 100_000_000:
        return
    MODELO.parent.mkdir(parents=True, exist_ok=True)
    print(f"  baixando o modelo de recorte (224 MB, uma vez só) para {MODELO}")
    tmp = MODELO.with_suffix(".parcial")
    urllib.request.urlretrieve(URL_MODELO, tmp)
    tmp.rename(MODELO)


def sessao():
    import onnxruntime as ort
    garantir_modelo()
    opcoes = ort.SessionOptions()
    opcoes.log_severity_level = 3
    return ort.InferenceSession(str(MODELO), opcoes, providers=["CPUExecutionProvider"])


def mascara(sess, im):
    import numpy as np
    from PIL import Image
    x = np.asarray(im.convert("RGB").resize((LADO, LADO), Image.BILINEAR), dtype=np.float32) / 255.0
    x = (x - np.array(MEDIA, dtype=np.float32)) / np.array(DESVIO, dtype=np.float32)
    x = x.transpose(2, 0, 1)[None].astype(np.float32)
    saida = sess.run(None, {sess.get_inputs()[0].name: x})[0][0, 0]
    p = 1.0 / (1.0 + np.exp(-saida))
    p = (p - p.min()) / max(p.max() - p.min(), 1e-6)
    m = Image.fromarray((p * 255).astype("uint8"), "L").resize(im.size, Image.LANCZOS)
    return m


def com_borda(rgba, px):
    """Contorno branco de adesivo: a máscara dilatada vira um branco por baixo do recorte. A
    dilatação roda numa cópia pequena da máscara (rápida) e volta ao tamanho cheio já suavizada."""
    from PIL import Image, ImageFilter
    a = rgba.getchannel("A")
    folga = px + 4
    base = Image.new("RGBA", (rgba.width + 2 * folga, rgba.height + 2 * folga), (0, 0, 0, 0))
    a_grande = Image.new("L", base.size, 0)
    a_grande.paste(a, (folga, folga))
    f = min(1.0, 512 / max(base.size))
    pequena = a_grande.resize((max(1, round(base.width * f)), max(1, round(base.height * f))), Image.BILINEAR)
    pequena = pequena.point(lambda v: 255 if v > 100 else 0)
    raio = max(1, round(px * f))
    pequena = pequena.filter(ImageFilter.MaxFilter(2 * raio + 1))
    dil = pequena.resize(base.size, Image.BICUBIC).point(lambda v: 255 if v > 127 else 0)
    dil = dil.filter(ImageFilter.GaussianBlur(1.2))
    branco = Image.new("RGBA", base.size, (255, 255, 255, 255))
    branco.putalpha(dil)
    base.alpha_composite(branco)
    base.alpha_composite(rgba, (folga, folga))
    return base


def aparar(rgba, folga=12):
    caixa = rgba.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    if not caixa:
        return rgba
    x0, y0, x1, y1 = caixa
    return rgba.crop((max(0, x0 - folga), max(0, y0 - folga),
                      min(rgba.width, x1 + folga), min(rgba.height, y1 + folga)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("imagens", nargs="+")
    ap.add_argument("--saida", help="pasta de saída (padrão: ao lado de cada imagem)")
    ap.add_argument("--borda", type=int, default=0, help="contorno branco de adesivo, em px (0 = sem)")
    ap.add_argument("--sem-aparar", action="store_true")
    args = ap.parse_args()

    from PIL import Image
    sess = sessao()
    falhas = 0
    for caminho in args.imagens:
        p = Path(caminho).expanduser()
        try:
            t0 = time.time()
            im = Image.open(p).convert("RGB")
            if max(im.size) > LADO_MAX:
                k = LADO_MAX / max(im.size)
                im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
            m = mascara(sess, im)
            rgba = im.convert("RGBA")
            rgba.putalpha(m)
            if not args.sem_aparar:
                rgba = aparar(rgba)
            if args.borda > 0:
                rgba = com_borda(rgba, args.borda)
            destino = (Path(args.saida) if args.saida else p.parent) / f"{p.stem}-sem-fundo.png"
            destino.parent.mkdir(parents=True, exist_ok=True)
            rgba.save(destino, "PNG", optimize=True)
            import numpy as np
            cobre = float((np.asarray(rgba.getchannel("A")) > 128).mean())
            print(f"  ok  {destino.name}  {rgba.width}x{rgba.height}  ·  objeto em {cobre:.0%} do quadro  ·  "
                  f"{time.time() - t0:.1f} s")
        except Exception as e:
            falhas += 1
            print(f"  falhou  {p.name} ({e})")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
