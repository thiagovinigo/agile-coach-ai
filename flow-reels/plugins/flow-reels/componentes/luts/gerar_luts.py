#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_luts.py  ·  as LUTs da marca para o acabamento global do reel (4.3, motor/docs-4/pos.md)

Gera, por conta fechada (sem foto de referência, sem LUT de terceiro), quatro LUTs 3D .cube de 33 pontos
nesta pasta. O compor.py aplica com o lut3d do ffmpeg quando o cenas.json pede
"acabamento": {"lut": "<nome>"}. Rodar de novo dá exatamente os mesmos arquivos.

    neutra-quente   leve e segura: um pouco mais de contraste e de cor, branco puxando para o quente
    fria-tech       sombras para o azul-ciano da marca, meios-tons limpos, contraste firme
    filme           película: preto levantado, ombro suave nas altas, sombras frias e altas quentes
    noir            preto e branco de contraste alto, com filtro vermelho (pele clara, céu escuro)

O acento da marca (no exemplo, o rosa #FF005E) continua o mesmo nas três primeiras (o gate de contraste mede a cor final de
qualquer jeito: o compor.py mede o texto depois da LUT).

Uso:  flow-reels componentes/gerar_luts
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
N = 33


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def mix(a, b, f):
    return a + (b - a) * f


def suave(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def luma(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(x, k):
    """curva em S em volta de 0,5 (k = 0 nada, 1 = smoothstep inteiro)"""
    return mix(x, suave(x), k)


def saturar(r, g, b, s):
    l = luma(r, g, b)
    return l + (r - l) * s, l + (g - l) * s, l + (b - l) * s


def ombro(x, joelho=0.78):
    """comprime as altas acima do joelho (a película não estoura)"""
    if x <= joelho:
        return x
    resto = 1.0 - joelho
    return joelho + resto * (1.0 - (1.0 - (x - joelho) / resto) ** 2) * 0.96


def neutra_quente(r, g, b):
    r, g, b = (contraste(v, 0.16) for v in (r, g, b))
    r, g, b = saturar(r, g, b, 1.06)
    l = luma(r, g, b)
    r, g, b = r * 1.025 + 0.004, g * 1.0, b * (0.955 + 0.02 * (1 - l))
    return 0.012 + r * 0.988, 0.012 + g * 0.988, 0.014 + b * 0.986


def fria_tech(r, g, b):
    r, g, b = (contraste(v, 0.26) for v in (r, g, b))
    l = luma(r, g, b)
    sombra = (1.0 - l) ** 2
    # sombras para o ciano da marca (#0099FF), altas quase neutras com um toque frio
    r = r * 0.95 - 0.01 * sombra
    g = g * 0.99 + 0.035 * sombra
    b = b * 1.03 + 0.075 * sombra + 0.01
    r, g, b = saturar(r, g, b, 0.94)
    return r, g, b


def filme(r, g, b):
    r, g, b = saturar(r, g, b, 0.86)
    r, g, b = (contraste(v, 0.12) for v in (r, g, b))
    r, g, b = (ombro(v) for v in (r, g, b))
    l = luma(r, g, b)
    sombra, alta = (1.0 - l) ** 2, l ** 2
    # sombras frias (verde-azulado), altas quentes (laranja)
    r += -0.025 * sombra + 0.035 * alta
    g += 0.012 * sombra + 0.012 * alta
    b += 0.03 * sombra - 0.035 * alta
    # preto levantado e branco que não chega a 1
    return tuple(0.045 + clamp(v) * 0.92 for v in (r, g, b))


def noir(r, g, b):
    y = 0.42 * r + 0.5 * g + 0.08 * b    # filtro vermelho: pele clara, azul escuro
    y = contraste(clamp(y), 0.62)
    y = clamp((y - 0.03) / 0.95)
    return y, y, y


LUTS = {"neutra-quente": neutra_quente, "fria-tech": fria_tech, "filme": filme, "noir": noir}


def gravar(nome, fn):
    linhas = [f'TITLE "Fabrica de Cortes - {nome}"', f"LUT_3D_SIZE {N}", "DOMAIN_MIN 0.0 0.0 0.0",
              "DOMAIN_MAX 1.0 1.0 1.0"]
    for bi in range(N):
        for gi in range(N):
            for ri in range(N):
                r, g, b = fn(ri / (N - 1), gi / (N - 1), bi / (N - 1))
                linhas.append(f"{clamp(r):.6f} {clamp(g):.6f} {clamp(b):.6f}")
    (AQUI / f"{nome}.cube").write_text("\n".join(linhas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    for nome, fn in LUTS.items():
        gravar(nome, fn)
        print(f"  {nome}.cube")
