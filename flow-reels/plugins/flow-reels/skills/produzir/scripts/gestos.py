#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gestos.py  ·  o que as mãos estão fazendo, quadro a quadro (Fábrica 4.0, frente "mãos e corpo")

A visão do corte (visao.py) dá os 21 pontos de cada mão e os 33 do corpo. Este script lê isso e diz,
por quadro e por mão, QUE GESTO é (aberta, punho, pinça, aponta, vitória, joinha, contando-N), e
lista os EVENTOS que servem de gatilho para os efeitos de mão do motor (sobre/maos-fx.js): a batida
de palmas, o punho que abre, a varrida, o apontar, a contagem nos dedos e a ênfase no ritmo da fala.
É offline: a suavização não atrasa (ida e volta) e o gesto vale desde o primeiro quadro em que ele
começou, não 5 quadros depois.

As fórmulas e os limiares são os da pesquisa (docs/pesquisa-4-0/02-maos-corpo-e-frames-3d.md, 1.2 e
1.3), todos relativos à escala da mão s = d(punho, nó do médio), em 3D (o z do MediaPipe vem na
escala do x), então valem com a mão perto ou longe da câmera.

O caminho:

  lado       "esquerda" = a mão à esquerda na tela (de quem assiste), como no maos.json. O lado é
             conferido pelos pulsos do corpo (pose 15 e 16): quando o pulso da mão está claramente
             no pulso do outro lado por 3 quadros ou mais, as mãos trocam de lado. A leitura repetida
             (duas "mãos" em cima de uma) vira uma.
  limpeza    salto maior que 1,5 s que volta no quadro seguinte é descartado; buraco de até 6
             quadros no meio de um trecho é preenchido (Catmull-Rom). Nada atravessa emenda
             (visao.json → segmentos).
  suavização One Euro para a frente e para trás, média das duas (zero-phase), em unidades de mão
             (coordenada / s mediano do trecho). Pontas dos dedos com corte mais alto (mexem rápido e
             são o que os efeitos seguem), palma e punho mais suaves. A escala s e a distância entre
             as palmas são suavizadas à parte (efeito que cresce com elas não pode tremer).
  dedos      estendido: ângulo no PIP < 35° e d(ponta, punho) > 1,15·d(PIP, punho); curvado: ângulo
             > 70°; no meio, mantém o anterior (histerese). Polegar: d(4,17) > 1,2·d(3,17) e ângulo no
             IP < 40°.
  gesto      pinça (entra < 0,25 s, sai > 0,40 s), punho, joinha, aponta, vitória, aberta,
             contando-N, nenhum. Só vale o gesto que dura 5 quadros ou mais; o trecho mais curto
             herda o vizinho. O gesto estável começa no primeiro quadro em que apareceu.
  presença   "a" de 0 a 1: sobe em 6 quadros quando a mão chega, e quando ela some fica parada na
             última pose e desce em 6 quadros (nunca pula). Também desce quando o centro da palma sai
             pela borda (a mão cortada embaixo, comum no busto).
  duas mãos  distância entre as palmas em mãos (s médio) e em ombros; "segurando" = as duas abertas
             ou semiabertas, de 0,8 a 4 mãos de distância, na mesma altura, palmas de lado (se
             encarando), por 6 quadros ou mais.
  eventos    palmas, abre, varrida, aponta-inicio, aponta-fim, conta, enfase (abaixo).

Saída: visao/gestos.json (contrato em motor/docs-4/maos-corpo.md). O compor.py entrega ao motor em
window.VISAO.gestos quando o gestos.json é do mesmo fala.mp4 da visão (o "origem" dele).

Uso:
    flow-reels produzir/gestos --projeto projetos/<video> --corte NN
    flow-reels produzir/gestos --projeto projetos/<video> --corte NN --resumo     # só imprime os momentos
    flow-reels produzir/gestos --projeto projetos/<video> --corte NN --folha      # e a folha de contato

Saída 0 = gravou; 1 = gravou, mas quase não há mão no vídeo; 2 = erro (falta a visão ou as mãos).
"""
import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

import numpy as np

VERSAO = 1
RAIZ = fabrica.raiz()

# ------------------------------------------------------------------ os limiares (pesquisa 02, 1.2)
L = {
    "pip_reto": 35.0,          # graus: dedo estendido abaixo disto no PIP
    "pip_curvo": 70.0,         # graus: curvado acima disto
    "ponta_longe": 1.15,       # d(ponta, punho) > 1,15·d(PIP, punho)
    "polegar_razao": 1.2,      # d(4,17) > 1,2·d(3,17)
    "polegar_razao_sai": 1.08,
    "polegar_ang": 40.0,       # ângulo no IP
    "polegar_ang_sai": 55.0,
    "pinca_entra": 0.25,       # d(4,8)/s
    "pinca_sai": 0.40,
    "punho_raio": 0.9,         # média de d(ponta, C)/s nos 4 dedos
    "abertura_min": 8.0,       # graus entre direções de dedos vizinhos (mão aberta)
    "vitoria_ang": 15.0,
    "joinha_alto": 0.6,        # P4.y < P2.y − 0,6·s
    "camera": 0.5,             # d(5,8)/s abaixo disto = apontando para a câmera
    "min_gesto": 5,            # quadros: tempo mínimo de um gesto
    "min_conta": 5,
    "fade": 6,                 # quadros de entrada e de saída da presença
    "buraco": 6,               # quadros: buraco preenchido
    "outlier": 1.5,            # s: salto que volta no quadro seguinte
    "segura_min": 0.8, "segura_max": 4.0,
    "segura_min_sai": 0.65, "segura_max_sai": 4.6,
    "segura_quadros": 6,
    "palmas_juntas": 1.0,      # dist/s_médio
    "palmas_queda": 1.2,       # a distância cai mais que isto (em s) em até 5 quadros
    "afasta_vel": 0.15,        # s por quadro, por 4 quadros
    "afasta_quadros": 4,
    "varrida_vel": 0.35,       # s por quadro (horizontal), por 3 quadros
    "varrida_quadros": 3,
    "enfase_vel": 0.10,        # s por quadro (vertical), pico
    "enfase_janela": 3,        # quadros em volta do início da palavra tônica
    "parada": 0.12,            # s por quadro: mão "quieta" para contar
    "conta_em_pe": -0.45,      # y médio da direção dos dedos esticados (para cima é negativo)
    "conta_longe": 1.8,        # dist/s: a outra mão mais perto que isso = mãos juntas, não conta
}

# One Euro (Casiez et al. 2012), em unidades de mão. min_cutoff em Hz, beta em (mão/s)^-1
FILTRO_PONTA = (1.6, 0.6)
FILTRO_PALMA = (1.0, 0.4)
FILTRO_ESCALA = (0.4, 0.1)

PONTAS = (4, 8, 12, 16, 20)
DEDOS = {  # MCP, PIP, DIP, TIP
    "indicador": (5, 6, 7, 8), "medio": (9, 10, 11, 12), "anelar": (13, 14, 15, 16), "minimo": (17, 18, 19, 20),
}
NOMES_DEDOS = ["polegar", "indicador", "medio", "anelar", "minimo"]
LADOS = ("esquerda", "direita")

PARADAS = set("""a o as os um uma uns umas de da do das dos dum duma em na no nas nos num numa e é ou
que se por para pra pro com sem ao aos à às mas mais já não nem ele ela eles elas eu tu você vocês
me te lhe nos vos seu sua seus suas meu minha isso isto aquilo esse essa este esta lá aí aqui então
tem ter foi ser era vai vou vem como quando onde qual quem porque pelo pela pelos pelas até também
só bem muito todo toda todos todas outro outra cada""".split())


def fala(msg):
    print(msg, flush=True)


def erro(msg, codigo=2):
    print("erro: " + msg, file=sys.stderr, flush=True)
    sys.exit(codigo)


def _json(o):
    if hasattr(o, "item"):
        return o.item()
    if hasattr(o, "tolist"):
        return o.tolist()
    raise TypeError(type(o).__name__)


def ler(caminho):
    try:
        return json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# ------------------------------------------------------------------ filtros
def one_euro(x, fps, min_cutoff, beta, d_cutoff=1.0):
    """Um passo do One Euro sobre a série x (n, d), para a frente. Devolve a série filtrada."""
    n = len(x)
    out = np.empty_like(x)
    te = 1.0 / fps

    def alfa(fc):
        tau = 1.0 / (2 * math.pi * fc)
        return 1.0 / (1.0 + tau / te)

    ad = alfa(d_cutoff)
    xp = x[0].copy()
    dxp = np.zeros_like(x[0])
    out[0] = xp
    for i in range(1, n):
        dx = (x[i] - xp) / te
        dxh = dxp + ad * (dx - dxp)
        fc = min_cutoff + beta * np.abs(dxh)
        a = 1.0 / (1.0 + (1.0 / (2 * math.pi * fc)) / te)
        xh = xp + a * (x[i] - xp)
        out[i] = xh
        xp, dxp = xh, dxh
    return out


def zero_fase(x, fps, min_cutoff, beta):
    """One Euro para a frente e para trás, média das duas: não atrasa o pico do gesto."""
    if len(x) < 3:
        return x.copy()
    ida = one_euro(x, fps, min_cutoff, beta)
    volta = one_euro(x[::-1], fps, min_cutoff, beta)[::-1]
    return (ida + volta) / 2


def catmull(p0, p1, p2, p3, u):
    u2, u3 = u * u, u * u * u
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u3)


def corridas(mask):
    """[(a, b)] dos trechos True de mask, b fora."""
    out, a = [], None
    for i, v in enumerate(mask):
        if v and a is None:
            a = i
        elif not v and a is not None:
            out.append((a, i))
            a = None
    if a is not None:
        out.append((a, len(mask)))
    return out


# ------------------------------------------------------------------ geometria da mão
def angulo(a, b, c):
    """Ângulo (graus) entre (a→b) e (b→c): 0 = reto."""
    u, v = b - a, c - b
    nu, nv = np.linalg.norm(u), np.linalg.norm(v)
    if nu < 1e-6 or nv < 1e-6:
        return 0.0
    return math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(u, v) / (nu * nv))))))


def dist(a, b):
    return float(np.linalg.norm(a - b))


def estado_dedos(P, s, antes):
    """[polegar, indicador, médio, anelar, mínimo]: 1 estendido, 0 curvado, com histerese (antes)."""
    est = list(antes) if antes is not None else [0, 0, 0, 0, 0]
    # polegar
    r = dist(P[4], P[17]) / max(1e-6, dist(P[3], P[17]))
    ang = angulo(P[2], P[3], P[4])
    if r > L["polegar_razao"] and ang < L["polegar_ang"]:
        est[0] = 1
    elif r < L["polegar_razao_sai"] or ang > L["polegar_ang_sai"]:
        est[0] = 0
    for i, nome in enumerate(("indicador", "medio", "anelar", "minimo"), start=1):
        mcp, pip, dip, tip = DEDOS[nome]
        ang = angulo(P[mcp], P[pip], P[tip])
        longe = dist(P[tip], P[0]) > L["ponta_longe"] * dist(P[pip], P[0])
        if ang < L["pip_reto"] and longe:
            est[i] = 1
        elif ang > L["pip_curvo"] or not longe:
            est[i] = 0
    return est


def direcao2(a, b):
    v = b[:2] - a[:2]
    n = np.linalg.norm(v)
    return v / n if n > 1e-6 else np.array([0.0, -1.0])


def candidato(P, s, d, pinca_antes):
    """O gesto do quadro (antes da estabilidade), a pinça (com histerese) e a abertura da pinça."""
    dp = dist(P[4], P[8]) / s
    pinca = dp < L["pinca_entra"] or (pinca_antes and dp < L["pinca_sai"])
    abertura = min(1.0, max(0.0, (dp - 0.2) / 0.8))
    C = (P[0] + P[5] + P[9] + P[13] + P[17]) / 5
    n = sum(d)
    if pinca and not (d[2] and d[3] and d[4]):
        return "pinca", pinca, abertura, C
    if pinca:
        return "pinca", pinca, abertura, C  # o "OK": pinça com os outros dedos esticados
    if n == 0 or (n == 1 and d[0] == 1 and P[4][1] >= P[2][1] - L["joinha_alto"] * s):
        raio = np.mean([dist(P[t], C) / s for t in (8, 12, 16, 20)])
        if raio < L["punho_raio"]:
            return "punho", pinca, abertura, C
    if d == [1, 0, 0, 0, 0] and P[4][1] < P[2][1] - L["joinha_alto"] * s:
        return "joinha", pinca, abertura, C
    if d[1] == 1 and d[2] == 0 and d[3] == 0 and d[4] == 0:
        return "aponta", pinca, abertura, C
    if d[1] == 1 and d[2] == 1 and d[3] == 0 and d[4] == 0:
        a = math.degrees(math.acos(max(-1, min(1, float(np.dot(direcao2(P[5], P[8]), direcao2(P[9], P[12])))))))
        if a > L["vitoria_ang"]:
            return "vitoria", pinca, abertura, C
        return "contando-2", pinca, abertura, C
    if n == 5:
        return "aberta", pinca, abertura, C
    if n >= 4:
        dirs = [direcao2(P[m], P[t]) for m, t in ((5, 8), (9, 12), (13, 16), (17, 20))]
        ab = np.mean([math.degrees(math.acos(max(-1, min(1, float(np.dot(dirs[i], dirs[i + 1])))))) for i in range(3)])
        if ab > L["abertura_min"]:
            return "aberta", pinca, abertura, C
        return f"contando-{n}", pinca, abertura, C
    if n >= 1:
        return f"contando-{n}", pinca, abertura, C
    return "nenhum", pinca, abertura, C


CONTAGEM_VALIDA = {
    1: ([0, 1, 0, 0, 0],),  # só o polegar é mais vezes mão entrelaçada (a outra some) que contagem
    2: ([0, 1, 1, 0, 0], [1, 1, 0, 0, 0]),
    3: ([0, 1, 1, 1, 0], [1, 1, 1, 0, 0]),
    4: ([0, 1, 1, 1, 1],),
    5: ([1, 1, 1, 1, 1],),
}


def estabilizar(rotulos, presente, minimo):
    """Rótulo estável: trecho de rótulo igual com menos de `minimo` quadros herda o vizinho (o de
    antes, senão o de depois). Offline: o gesto vale desde o primeiro quadro em que apareceu."""
    n = len(rotulos)
    out = list(rotulos)
    i = 0
    trechos = []
    while i < n:
        if not presente[i]:
            i += 1
            continue
        j = i
        while j < n and presente[j] and rotulos[j] == rotulos[i]:
            j += 1
        trechos.append([i, j, rotulos[i]])
        i = j
    # junta: os curtos herdam o anterior contíguo, ou o seguinte
    for idx, (a, b, r) in enumerate(trechos):
        if b - a >= minimo:
            continue
        ant = trechos[idx - 1] if idx > 0 and trechos[idx - 1][1] == a else None
        seg = trechos[idx + 1] if idx + 1 < len(trechos) and trechos[idx + 1][0] == b else None
        if ant is not None and (ant[1] - ant[0] >= minimo or seg is None):
            novo = ant[2]
        elif seg is not None and seg[1] - seg[0] >= minimo:
            novo = seg[2]
        elif ant is not None:
            novo = ant[2]
        else:
            novo = r
        trechos[idx][2] = novo
        for k in range(a, b):
            out[k] = novo
    return out


# ------------------------------------------------------------------ leitura e trilhas
def caminhos(projeto, corte):
    proj = Path(projeto)
    if not proj.is_absolute():
        proj = (Path.cwd() / proj).resolve()
    nn = f"{int(corte):02d}" if str(corte).isdigit() else str(corte)
    pasta = proj / "materiais-de-trabalho" / f"corte-{nn}"
    return proj, nn, pasta


def segmentos_de(meta, total):
    segs = (meta or {}).get("segmentos") or [[0, total]]
    out = []
    for s in segs:
        if isinstance(s, (list, tuple)) and len(s) == 2:
            out.append((int(s[0]), min(total, int(s[1]))))
    return out or [(0, total)]


def montar_trilhas(maos, corpo, total, W, H):
    """P[lado] (T, 21, 3) com nan onde não há mão; medido e score por quadro. Confere o lado pelos
    pulsos do corpo e tira a leitura repetida."""
    P = {l: np.full((total, 21, 3), np.nan) for l in LADOS}
    med = {l: np.zeros(total, bool) for l in LADOS}
    sc = {l: np.zeros(total) for l in LADOS}
    for k, q in enumerate(maos["quadros"][:total]):
        for h in q or []:
            l = h.get("lado")
            if l not in P:
                continue
            P[l][k] = np.array(h["pontos"], float)
            med[l][k] = bool(h.get("medido", True))
            sc[l][k] = float(h.get("score", 0.5))
    trocas = 0
    repetidas = 0
    # a leitura repetida: as duas trilhas em cima da mesma mão
    for k in range(total):
        a, b = P["esquerda"][k], P["direita"][k]
        if np.isnan(a[0, 0]) or np.isnan(b[0, 0]):
            continue
        s = (dist(a[0], a[9]) + dist(b[0], b[9])) / 2
        if np.mean(np.linalg.norm(a[:, :2] - b[:, :2], axis=1)) < 0.45 * s:
            # fica a que já estava no quadro anterior
            fica_a = k > 0 and not np.isnan(P["esquerda"][k - 1][0, 0])
            fica_b = k > 0 and not np.isnan(P["direita"][k - 1][0, 0])
            sai = "direita" if (fica_a and not fica_b) or (fica_a == fica_b and sc["esquerda"][k] >= sc["direita"][k]) else "esquerda"
            P[sai][k] = np.nan
            repetidas += 1
    # o lado pelos pulsos da pose: o pulso de cada lado da tela
    if corpo and corpo.get("quadros"):
        errado = np.zeros(total, bool)
        for k in range(total):
            c = corpo["quadros"][k] if k < len(corpo["quadros"]) else None
            if not c:
                continue
            pts = c["pontos"]
            w1, w2 = np.array(pts[15][:2]), np.array(pts[16][:2])
            vis = min(pts[15][2], pts[16][2])
            if vis < 0.5 or abs(w1[0] - w2[0]) < 1:
                continue
            pe, pd = (w1, w2) if w1[0] < w2[0] else (w2, w1)
            ruim = False
            for l, proprio, outro in (("esquerda", pe, pd), ("direita", pd, pe)):
                h = P[l][k]
                if np.isnan(h[0, 0]):
                    continue
                s = dist(h[0], h[9])
                d0, d1 = dist(h[0, :2], proprio), dist(h[0, :2], outro)
                if d1 < 0.5 * d0 and d1 < 1.2 * s:
                    ruim = True
            errado[k] = ruim
        for a, b in corridas(errado):
            if b - a < 3:
                continue
            for k in range(a, b):
                P["esquerda"][k], P["direita"][k] = P["direita"][k].copy(), P["esquerda"][k].copy()
                med["esquerda"][k], med["direita"][k] = med["direita"][k], med["esquerda"][k]
                sc["esquerda"][k], sc["direita"][k] = sc["direita"][k], sc["esquerda"][k]
                trocas += 1
    return P, med, sc, trocas, repetidas


def limpar_trilha(P, med, segs, fps):
    """Descarta o salto que volta, preenche buraco curto e suaviza zero-phase, trecho a trecho."""
    T = len(P)
    pres = ~np.isnan(P[:, 0, 0])
    preenchido = np.zeros(T, bool)
    descartes = 0
    # o salto que volta: C pula mais de 1,5 s num quadro e volta no seguinte
    for k in range(1, T - 1):
        if not (pres[k - 1] and pres[k] and pres[k + 1]):
            continue
        C = lambda q: (P[q, 0] + P[q, 5] + P[q, 9] + P[q, 13] + P[q, 17]) / 5
        s = dist(P[k - 1, 0], P[k - 1, 9])
        if dist(C(k), C(k - 1)) > L["outlier"] * s and dist(C(k + 1), C(k - 1)) < 0.5 * s:
            P[k] = np.nan
            pres[k] = False
            descartes += 1
    for a, b in segs:
        # buraco curto dentro do trecho
        k = a
        while k < b:
            if pres[k]:
                k += 1
                continue
            j = k
            while j < b and not pres[j]:
                j += 1
            if k > a and j < b and pres[k - 1] and (j - k) <= L["buraco"]:
                p0 = P[k - 2] if k - 2 >= a and pres[k - 2] else P[k - 1]
                p1, p2 = P[k - 1], P[j]
                p3 = P[j + 1] if j + 1 < b and pres[j + 1] else P[j]
                for i in range(k, j):
                    u = (i - k + 1) / (j - k + 1)
                    P[i] = catmull(p0, p1, p2, p3, u)
                    preenchido[i] = True
                    pres[i] = True
            k = j
        # suaviza cada trecho contínuo, sem atravessar a emenda
        for ra, rb in corridas(pres[a:b]):
            ra += a
            rb += a
            if rb - ra < 3:
                continue
            seg = P[ra:rb]
            s_med = float(np.median(np.linalg.norm(seg[:, 0] - seg[:, 9], axis=1))) or 1.0
            for j in range(21):
                mc, beta = FILTRO_PONTA if j in PONTAS else FILTRO_PALMA
                seg[:, j] = zero_fase(seg[:, j] / s_med, fps, mc, beta) * s_med
            P[ra:rb] = seg
    med = med & ~preenchido
    return P, pres, med, descartes, int(preenchido.sum())


# ------------------------------------------------------------------ análise
def analisar_mao(P, pres, segs, fps, W, H):
    """Gesto, dedos, pinça, C, s, direção e velocidade por quadro, só nos quadros com mão."""
    T = len(P)
    s = np.full(T, np.nan)
    for k in np.where(pres)[0]:
        s[k] = dist(P[k, 0], P[k, 9])
    # a escala suavizada à parte (efeito que cresce com ela não pode tremer)
    for a, b in segs:
        for ra, rb in corridas(pres[a:b]):
            ra += a
            rb += a
            if rb - ra >= 3:
                s[ra:rb] = zero_fase(s[ra:rb, None], fps, *FILTRO_ESCALA)[:, 0]
    dedos = [None] * T
    cand = ["nenhum"] * T
    pinca = np.zeros(T, bool)
    abertura = np.zeros(T)
    C = np.full((T, 3), np.nan)
    antes = None
    pin_antes = False
    for k in range(T):
        if not pres[k]:
            antes, pin_antes = None, False
            continue
        if k > 0 and any(k == a for a, _ in segs):
            antes, pin_antes = None, False
        d = estado_dedos(P[k], s[k], antes)
        g, pin, ab, c = candidato(P[k], s[k], d, pin_antes)
        dedos[k], cand[k], pinca[k], abertura[k], C[k] = d, g, pin, ab, c
        antes, pin_antes = d, pin
    gesto = estabilizar(cand, pres, L["min_gesto"])
    # a contagem estável (o número de dedos, independente do rótulo)
    nrot = [str(sum(d)) if d is not None else "x" for d in dedos]
    nest = estabilizar(nrot, pres, L["min_conta"])
    # velocidade de C (px por quadro), diferença central dentro do trecho
    v = np.zeros((T, 2))
    for a, b in segs:
        for ra, rb in corridas(pres[a:b]):
            ra += a
            rb += a
            for k in range(ra, rb):
                k0, k1 = max(ra, k - 1), min(rb - 1, k + 1)
                if k1 > k0:
                    v[k] = (C[k1, :2] - C[k0, :2]) / (k1 - k0)
    direcao = np.zeros((T, 2))
    camera = np.zeros(T, bool)
    largura = np.zeros(T)
    for k in np.where(pres)[0]:
        direcao[k] = direcao2(P[k, 5], P[k, 8])
        camera[k] = dedos[k][1] == 1 and dist(P[k, 5, :2], P[k, 8, :2]) / s[k] < L["camera"]
        largura[k] = dist(P[k, 5, :2], P[k, 17, :2]) / s[k]
    return {"s": s, "dedos": dedos, "cand": cand, "gesto": gesto, "n": nest, "pinca": pinca,
            "abertura": abertura, "C": C, "v": v, "dir": direcao, "camera": camera, "largura": largura}


def presenca(pres, C, s, segs, W, H):
    """a (0..1): sobe em 6 quadros, segura a última pose e desce em 6 quando a mão some; desce quando
    o centro da palma sai pela borda. Devolve a e o índice do quadro cuja pose vale (o próprio, ou o
    último bom, na saída)."""
    T = len(pres)
    F = L["fade"]
    a = np.zeros(T)
    fonte = np.full(T, -1)
    for sa, sb in segs:
        for ra, rb in corridas(pres[sa:sb]):
            ra += sa
            rb += sa
            for k in range(ra, rb):
                ent = min(1.0, (k - ra + 1) / F) if ra > sa else 1.0
                a[k] = max(a[k], ent)
                fonte[k] = k
            # a saída: parada na última pose, até o próximo trecho ou a emenda
            for i in range(1, F + 1):
                k = rb - 1 + i
                if k >= sb or pres[k]:
                    break
                val = 1.0 - i / F
                if val > a[k]:
                    a[k] = val
                    fonte[k] = rb - 1
    # a borda: o centro da palma saindo do quadro
    for k in range(T):
        j = fonte[k]
        if j < 0 or np.isnan(C[j, 0]):
            continue
        sk = s[j] if not np.isnan(s[j]) else 50
        x, y = C[j, 0], C[j, 1]
        borda = min((H - y) / (0.5 * sk), x / (0.5 * sk), (W - x) / (0.5 * sk), 1.0)
        a[k] *= max(0.0, min(1.0, borda))
    return a, fonte


def palavras_tonicas(palavras, enfase):
    enf = {"".join(ch for ch in w.lower() if ch.isalnum()) for w in (enfase or [])}
    out = []
    for i, w in enumerate(palavras):
        txt = "".join(ch for ch in w["texto"].lower() if ch.isalnum() or ch == "%")
        if not txt:
            continue
        tonica = txt in enf or any(ch.isdigit() for ch in txt) or (txt not in PARADAS and len(txt) >= 4)
        out.append({"i": i, "t": float(w["inicio"]), "fim": float(w["fim"]), "texto": w["texto"], "tonica": tonica})
    return out


def eventos_de(A, duas, a, segs, fps, palavras, W, H):
    ev = []
    seg_de = np.zeros(len(a["esquerda"]), int)
    for i, (sa, sb) in enumerate(segs):
        seg_de[sa:sb] = i

    def add(tipo, k, mao, **kw):
        e = {"tipo": tipo, "quadro": int(k), "t": round(k / fps, 3), "mao": mao}
        e.update(kw)
        ev.append(e)

    tonicas = [p for p in palavras if p["tonica"]]
    for l in LADOS:
        R = A[l]
        T = len(R["gesto"])
        vivo = a[l] > 0.5
        sk = np.where(np.isnan(R["s"]), 50, R["s"])
        # aponta-inicio / aponta-fim
        ap = np.array([g == "aponta" for g in R["gesto"]]) & vivo
        for ra, rb in corridas(ap):
            if rb - ra < L["min_gesto"] + 1:
                continue
            k = ra
            add("aponta-inicio", k, l, x=r1(R["C"][k, 0]), y=r1(R["C"][k, 1]),
                dir=[r3(R["dir"][k, 0]), r3(R["dir"][k, 1])], camera=bool(R["camera"][k]),
                ponta=[r1(Pt(R, k, 8)[0]), r1(Pt(R, k, 8)[1])], dur=round((rb - ra) / fps, 3))
            add("aponta-fim", rb - 1, l, x=r1(R["C"][rb - 1, 0]), y=r1(R["C"][rb - 1, 1]))
        # abre: punho -> aberta em até 10 quadros
        g = R["gesto"]
        k = 1
        while k < T:
            if g[k - 1] == "punho" and g[k] != "punho" and vivo[k]:
                for j in range(k, min(T, k + 10)):
                    if g[j] == "aberta":
                        add("abre", j, l, como="punho", x=r1(R["C"][j, 0]), y=r1(R["C"][j, 1]), s=r1(sk[j]))
                        k = j
                        break
            k += 1
        # varrida: |vx| > 0,35 s por quadro por 3 quadros
        vx = R["v"][:, 0] / sk
        rap = (np.abs(vx) > L["varrida_vel"]) & vivo
        ult = -99
        for ra, rb in corridas(rap):
            if rb - ra < L["varrida_quadros"]:
                continue
            if len(set(np.sign(vx[ra:rb]))) > 1:
                continue
            j = ra + int(np.argmax(np.abs(vx[ra:rb])))
            if j - ult < 12:
                continue
            ult = j
            add("varrida", j, l, sentido=int(np.sign(vx[j])), vel=r3(abs(vx[j])), x=r1(R["C"][j, 0]), y=r1(R["C"][j, 1]),
                de=round(ra / fps, 3), ate=round(rb / fps, 3))
        # conta: n estável, configuração de contagem, mão quieta
        ns = R["n"]
        ant = None
        k = 0
        while k < T:
            if ns[k] in ("x",) or not vivo[k]:
                k += 1
                continue
            j = k
            while j < T and ns[j] == ns[k] and vivo[j]:
                j += 1
            n = int(ns[k])
            if j - k >= L["min_conta"] and 1 <= n <= 5:
                conf = [R["dedos"][q] for q in range(k, j) if R["dedos"][q] is not None]
                moda = max(set(map(tuple, conf)), key=lambda c: sum(1 for x in conf if tuple(x) == c)) if conf else None
                veloc = float(np.mean(np.hypot(R["v"][k:j, 0], R["v"][k:j, 1]) / sk[k:j]))
                valida = moda is not None and list(moda) in [list(c) for c in CONTAGEM_VALIDA.get(n, ())]
                if valida:
                    # a mão que conta fica de pé (os dedos esticados apontam para cima) e longe da outra
                    # (mãos entrelaçadas dão "1" e "4" falsos)
                    pontas_ = [(m, t) for i_, (m, t) in enumerate(((2, 4), (5, 8), (9, 12), (13, 16), (17, 20))) if moda[i_]]
                    em_pe = [np.mean([direcao2(R["P"][q, m], R["P"][q, t])[1] for m, t in pontas_]) < L["conta_em_pe"]
                             for q in range(k, j)]
                    outra = duas["dist"][k:j]
                    perto = np.nanmin(outra) < L["conta_longe"] if np.any(~np.isnan(outra)) else False
                    valida = np.mean(em_pe) >= 0.6 and not perto
                if valida and veloc < L["parada"] and n != ant:
                    ultimo = [4, 8, 12, 16, 20][max(i for i in range(5) if moda[i])]
                    p = Pt(R, k, ultimo)
                    add("conta", k, l, n=n, dedos=list(moda), dedo=ultimo, x=r1(p[0]), y=r1(p[1]),
                        dur=round((j - k) / fps, 3))
                    ant = n
            if j - k >= L["min_conta"] and not (1 <= n <= 5):
                ant = None
            k = j
        # ênfase: pico de |vy| perto do início de palavra tônica
        vy = np.abs(R["v"][:, 1]) / sk
        usadas = set()
        ult = -99
        for p in tonicas:
            kw = int(round(p["t"] * fps))
            lo, hi = max(0, kw - L["enfase_janela"]), min(T, kw + L["enfase_janela"] + 1)
            if hi <= lo or not vivo[lo:hi].any():
                continue
            j = lo + int(np.argmax(np.where(vivo[lo:hi], vy[lo:hi], 0)))
            if vy[j] < L["enfase_vel"] or not vivo[j]:
                continue
            # é pico (maior que os vizinhos de ±2)
            if vy[j] < np.max(vy[max(0, j - 2):j + 3]) - 1e-9:
                continue
            if j in usadas or j - ult < 8:
                continue
            usadas.add(j)
            ult = j
            add("enfase", j, l, palavra=p["texto"], vel=r3(vy[j]), x=r1(R["C"][j, 0]), y=r1(R["C"][j, 1]))
    # duas mãos: palmas e abre (afastando)
    d = duas["dist"]
    T = len(d)
    ult = -99
    for k in range(5, T):
        if np.isnan(d[k]) or d[k] >= L["palmas_juntas"]:
            continue
        janela = d[k - 5:k]
        if np.all(np.isnan(janela)):
            continue
        # o encontro: o primeiro quadro já junto depois de uma queda rápida (a palma desacelera ali)
        if np.nanmax(janela) - d[k] > L["palmas_queda"]:
            if k - ult >= 10 and seg_de[k] == seg_de[k - 5]:
                ult = k
                add("palmas", k, "ambas", x=r1(duas["meio"][k, 0]), y=r1(duas["meio"][k, 1]))
    dd = np.diff(d, prepend=np.nan)
    rap = np.nan_to_num(dd, nan=0) > L["afasta_vel"]
    ult = -99
    for ra, rb in corridas(rap):
        if rb - ra < L["afasta_quadros"]:
            continue
        if seg_de[ra] != seg_de[rb - 1]:
            continue
        if np.isnan(d[ra - 1]) if ra > 0 else True:
            continue
        if d[ra - 1] > 2.5:
            continue
        if ra - ult < 12:
            continue
        ult = ra
        add("abre", ra, "ambas", como="afastando", x=r1(duas["meio"][ra, 0]), y=r1(duas["meio"][ra, 1]),
            de=r3(d[ra - 1]), ate_dist=r3(d[rb - 1]), dur=round((rb - ra) / fps, 3))
    ev.sort(key=lambda e: (e["quadro"], e["tipo"]))
    return ev


def Pt(R, k, j):
    return R["P"][k, j]


def r1(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), 1)


def r3(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), 3)


def duas_maos(A, a, corpo, segs, fps):
    T = len(a["esquerda"])
    dist_ = np.full(T, np.nan)
    ombros = np.full(T, np.nan)
    meio = np.full((T, 2), np.nan)
    for k in range(T):
        if a["esquerda"][k] <= 0 or a["direita"][k] <= 0:
            continue
        je, jd = A["esquerda"]["fonte"][k], A["direita"]["fonte"][k]
        if je < 0 or jd < 0:
            continue
        ce, cd = A["esquerda"]["C"][je, :2], A["direita"]["C"][jd, :2]
        sm = (A["esquerda"]["s"][je] + A["direita"]["s"][jd]) / 2
        dist_[k] = np.linalg.norm(ce - cd) / sm
        meio[k] = (ce + cd) / 2
        c = corpo["quadros"][k] if corpo and k < len(corpo.get("quadros") or []) else None
        if c:
            o1, o2 = np.array(c["pontos"][11][:2]), np.array(c["pontos"][12][:2])
            ow = np.linalg.norm(o1 - o2)
            if ow > 1:
                ombros[k] = np.linalg.norm(ce - cd) / ow
    # a distância suavizada à parte (a esfera cresce com ela)
    ok = ~np.isnan(dist_)
    for sa, sb in segs:
        for ra, rb in corridas(ok[sa:sb]):
            ra += sa
            rb += sa
            if rb - ra >= 3:
                dist_[ra:rb] = zero_fase(dist_[ra:rb, None], fps, 1.0, 0.3)[:, 0]
                meio[ra:rb] = zero_fase(meio[ra:rb], fps, 1.2, 0.3)
    # segurando: as duas abertas ou semiabertas, palmas de lado, na mesma altura, com histerese
    seg = np.zeros(T, bool)
    dentro = False
    for k in range(T):
        if np.isnan(dist_[k]):
            dentro = False
            continue
        je, jd = A["esquerda"]["fonte"][k], A["direita"]["fonte"][k]
        abertas = all(A[l]["dedos"][j] is not None and sum(A[l]["dedos"][j][1:]) >= 3 for l, j in (("esquerda", je), ("direita", jd)))
        sm = (A["esquerda"]["s"][je] + A["direita"]["s"][jd]) / 2
        mesma_altura = abs(A["esquerda"]["C"][je, 1] - A["direita"]["C"][jd, 1]) < 1.3 * sm
        if dentro:
            dentro = abertas and mesma_altura and L["segura_min_sai"] < dist_[k] < L["segura_max_sai"]
        else:
            dentro = abertas and mesma_altura and L["segura_min"] < dist_[k] < L["segura_max"]
        seg[k] = dentro
    for ra, rb in corridas(seg):
        if rb - ra < L["segura_quadros"]:
            seg[ra:rb] = False
    return {"dist": dist_, "ombros": ombros, "meio": meio, "segurando": seg}


# ------------------------------------------------------------------ resumo
def mmss(t):
    return f"{t:5.2f}s"


def palavras_perto(palavras, t, raio=0.6):
    ws = [p["texto"] for p in palavras if p["t"] >= t - raio and p["t"] <= t + raio]
    return " ".join(ws)


def imprimir_resumo(G, palavras):
    fps = G["fps"]
    T = G["total"]
    fala("")
    fala(f"gestos · {G['fonte']} · {T} quadros ({T / fps:.1f} s)")
    for l in LADOS:
        g = [q["g"] for q in G["maos"][l] if q and q["a"] > 0.5]
        if not g:
            fala(f"  mão da {l}: não aparece")
            continue
        cont = {}
        for x in g:
            cont[x] = cont.get(x, 0) + 1
        top = ", ".join(f"{k} {100 * v / T:.0f}%" for k, v in sorted(cont.items(), key=lambda kv: -kv[1]))
        fala(f"  mão da {l}: {100 * len(g) / T:.0f}% do vídeo · {top}")
    # os trechos segurando
    seg = [bool(q and q["segurando"]) for q in G["duas"]]
    tr = [(a, b) for a, b in corridas(seg)]
    fala("")
    fala("segurando (duas mãos abertas se encarando): energia, tela-maos, raio")
    if not tr:
        fala("  nenhum trecho")
    for a, b in tr:
        ds = [G["duas"][k]["dist"] for k in range(a, b)]
        fala(f"  {mmss(a / fps)} a {mmss(b / fps)} ({(b - a) / fps:.2f} s) dist {min(ds):.1f}-{max(ds):.1f} mãos · "
             f"\"{palavras_perto(palavras, (a + b) / 2 / fps, (b - a) / 2 / fps + 0.2)}\"")
    # duas mãos no quadro (para raio e energia mesmo sem segurar)
    ambas = [bool(q and q["dist"] is not None) for q in G["duas"]]
    tr = [(a, b) for a, b in corridas(ambas) if b - a >= 15]
    fala("")
    fala("duas mãos no quadro (≥ 0,5 s): raio, energia")
    for a, b in tr:
        fala(f"  {mmss(a / fps)} a {mmss(b / fps)} ({(b - a) / fps:.2f} s)")
    fala("")
    fala("eventos (gatilhos):")
    por_tipo = {}
    for e in G["eventos"]:
        por_tipo.setdefault(e["tipo"], []).append(e)
    for tipo in ("palmas", "abre", "varrida", "aponta-inicio", "aponta-fim", "conta", "enfase"):
        es = por_tipo.get(tipo, [])
        fala(f"  {tipo} ({len(es)})")
        for e in es:
            extra = ""
            if tipo == "conta":
                extra = f" n={e['n']} dedos={''.join(map(str, e['dedos']))}"
            elif tipo == "varrida":
                extra = f" {'→' if e['sentido'] > 0 else '←'} {e['vel']:.2f} s/q"
            elif tipo == "aponta-inicio":
                extra = f" dir=({e['dir'][0]:+.2f},{e['dir'][1]:+.2f}){' câmera' if e['camera'] else ''} {e['dur']:.2f} s"
            elif tipo == "enfase":
                extra = f" \"{e['palavra']}\" {e['vel']:.2f} s/q"
            elif tipo == "abre":
                extra = f" ({e['como']})"
            fala(f"    {mmss(e['t'])} {e['mao']:<8} y={e['y'] if e.get('y') is not None else '-':>6}{extra} · "
                 f"\"{palavras_perto(palavras, e['t'], 0.5)}\"")
    # os blocos de 2 s com mão acima da metade de baixo (o palco das mãos)
    fala("")
    fala("mãos no palco (centro da palma acima de 80% da altura), por blocos de 2 s:")
    H = G["altura"]
    linha = []
    for b0 in range(0, T, 2 * fps):
        alto = 0
        for k in range(b0, min(T, b0 + 2 * fps)):
            for l in LADOS:
                q = G["maos"][l][k]
                if q and q["a"] > 0.5 and q["C"][1] < 0.8 * H:
                    alto += 1
                    break
        linha.append(f"{b0 // fps:>2}s:{100 * alto / (2 * fps):3.0f}%")
    for i in range(0, len(linha), 6):
        fala("  " + "  ".join(linha[i:i + 6]))


# ------------------------------------------------------------------ folha de contato (debug)
def folha(pasta, G, saida, video):
    """Quadros nos eventos, com o esqueleto suavizado, o gesto e o evento escritos: para conferir no
    olho que o gesto bate com o vídeo."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        fala("  aviso: sem Pillow, sem folha")
        return
    fps = G["fps"]
    ks = []
    for e in G["eventos"]:
        if e["tipo"] in ("aponta-fim",):
            continue
        if not ks or e["quadro"] - ks[-1][0] > 6:
            ks.append((e["quadro"], f"{e['tipo']}{' ' + str(e['n']) if e['tipo'] == 'conta' else ''} {e['mao']}"))
    seg = [bool(q and q["segurando"]) for q in G["duas"]]
    for a, b in corridas(seg):
        ks.append(((a + b) // 2, "segurando"))
    ks.sort()
    ks = ks[:48]
    if not ks:
        return
    W, H = G["largura"], G["altura"]
    tw, th = 216, 384
    cols = 8
    rows = (len(ks) + cols - 1) // cols
    img = Image.new("RGB", (cols * tw, rows * th), (13, 10, 12))
    try:
        fonte = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    except OSError:
        fonte = ImageFont.load_default()
    cores = {"esquerda": (255, 0, 94), "direita": (0, 153, 255)}
    LIG = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9), (9, 10), (10, 11), (11, 12),
           (9, 13), (13, 14), (14, 15), (15, 16), (13, 17), (17, 18), (18, 19), (19, 20), (0, 17)]
    for i, (k, rot) in enumerate(ks):
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{k / fps:.4f}", "-i", str(video), "-frames:v", "1",
                            "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        try:
            from io import BytesIO
            q = Image.open(BytesIO(r.stdout)).convert("RGB").resize((W, H))
        except Exception:
            q = Image.new("RGB", (W, H), (40, 40, 40))
        d = ImageDraw.Draw(q)
        for l in LADOS:
            m = G["maos"][l][k]
            if not m:
                continue
            pts = m["p"]
            for a_, b_ in LIG:
                d.line([tuple(pts[a_]), tuple(pts[b_])], fill=cores[l], width=3)
            C = m["C"]
            d.ellipse([C[0] - 6, C[1] - 6, C[0] + 6, C[1] + 6], outline=(255, 255, 255), width=2)
            for j, ext in zip(PONTAS, m["dedos"]):
                if ext:
                    x, y = pts[j]
                    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 255, 255))
            d.text((C[0] - 40, C[1] + 14), f"{m['g']} n{m['n']} a{m['a']:.1f}", fill=(255, 255, 255), font=fonte)
        q = q.resize((tw, th))
        dd = ImageDraw.Draw(q)
        dd.rectangle([0, 0, tw, 34], fill=(0, 0, 0))
        dd.text((4, 2), f"{k / fps:.2f}s q{k}", fill=(255, 255, 255), font=fonte)
        dd.text((4, 17), rot, fill=(255, 0, 94), font=fonte)
        img.paste(q, ((i % cols) * tw, (i // cols) * th))
    img.save(saida, quality=88)
    fala(f"  folha: {saida}")


# ------------------------------------------------------------------ principal
def main():
    ap = argparse.ArgumentParser(description="gestos das mãos por quadro e eventos para os efeitos de mão")
    ap.add_argument("--projeto", required=True)
    ap.add_argument("--corte", required=True)
    ap.add_argument("--resumo", action="store_true", help="só imprime os momentos úteis (lê o gestos.json; refaz se faltar)")
    ap.add_argument("--folha", nargs="?", const="", default=None,
                    help="grava a folha de contato (padrão: folha-gestos.jpg na pasta do corte)")
    ap.add_argument("--visao", help="pasta visao/ alternativa (para testar com a visão de outro corte)")
    ap.add_argument("--saida", help="gestos.json alternativo")
    args = ap.parse_args()

    proj, nn, pasta = caminhos(args.projeto, args.corte)
    vdir = Path(args.visao).resolve() if args.visao else pasta / "visao"
    saida = Path(args.saida).resolve() if args.saida else vdir / "gestos.json"
    if not vdir.is_dir():
        erro(f"falta a visão do corte ({vdir}): rode o visao.py --projeto {args.projeto} --corte {nn}")
    maos = ler(vdir / "maos.json")
    if not maos or not maos.get("quadros"):
        erro(f"falta o maos.json em {vdir}: rode o visao.py --projeto {args.projeto} --corte {nn} --so maos")
    corpo = ler(vdir / "corpo.json")
    meta = ler(vdir / "visao.json") or {}
    origem = ler(vdir / ".origem.json") or {}
    pal = ler(pasta / "palavras-corte.json") or {"palavras": []}
    cenas = ler(pasta / "cenas.json") or {}
    palavras = palavras_tonicas(pal.get("palavras") or [], (cenas.get("legenda") or {}).get("enfase"))

    if args.resumo and saida.is_file() and args.folha is None:
        G = ler(saida)
        if G and G.get("versao") == VERSAO and G.get("origem", {}).get("mtime") == origem.get("mtime"):
            imprimir_resumo(G, palavras)
            return 0

    fps = int(maos.get("fps") or meta.get("fps") or 30)
    W, H = int(maos["largura"]), int(maos["altura"])
    total = int(meta.get("total") or len(maos["quadros"]))
    segs = segmentos_de(meta, total)

    P, med, sc, trocas, repetidas = montar_trilhas(maos, corpo, total, W, H)
    A = {}
    a = {}
    rel = {"trocas_de_lado": trocas, "repetidas": repetidas}
    for l in LADOS:
        Pl, pres, medl, desc, preen = limpar_trilha(P[l], med[l], segs, fps)
        R = analisar_mao(Pl, pres, segs, fps, W, H)
        R["P"] = Pl
        R["pres"] = pres
        R["medido"] = medl
        al, fonte = presenca(pres, R["C"], R["s"], segs, W, H)
        R["fonte"] = fonte
        A[l] = R
        a[l] = al
        rel[f"descartes_{l}"] = desc
        rel[f"preenchidos_{l}"] = preen
    duas = duas_maos(A, a, corpo, segs, fps)
    eventos = eventos_de(A, duas, a, segs, fps, palavras, W, H)

    # ---------------------------------------------------------------- gravar
    G = {
        "versao": VERSAO,
        "fonte": meta.get("fonte") or "fala.mp4",
        "fps": fps, "largura": W, "altura": H, "total": total,
        "segmentos": [list(s) for s in segs],
        "origem": {k: origem.get(k) for k in ("video", "mtime", "tamanho", "fps")},
        "lado": "de quem assiste: esquerda = a mão à esquerda na tela",
        "limiares": L,
        "relatorio": rel,
        "maos": {}, "duas": [], "eventos": eventos,
    }
    for l in LADOS:
        R = A[l]
        lista = []
        for k in range(total):
            j = R["fonte"][k]
            if a[l][k] <= 0 or j < 0:
                lista.append(None)
                continue
            Pk = R["P"][j]
            d = R["dedos"][j] or [0, 0, 0, 0, 0]
            lista.append({
                "a": round(float(a[l][k]), 3),
                "g": R["gesto"][j],
                "n": int(R["n"][j]) if R["n"][j] != "x" else sum(d),
                "dedos": d,
                "pinca": round(float(R["abertura"][j]), 3),
                "C": [r1(R["C"][j, 0]), r1(R["C"][j, 1])],
                "s": r1(R["s"][j]),
                "dir": [r3(R["dir"][j, 0]), r3(R["dir"][j, 1])],
                "camera": bool(R["camera"][j]),
                "v": [r1(R["v"][j, 0]) if j == k else 0.0, r1(R["v"][j, 1]) if j == k else 0.0],
                "medido": bool(R["medido"][j]) and j == k,
                "p": [[r1(Pk[i, 0]), r1(Pk[i, 1])] for i in range(21)],
            })
        G["maos"][l] = lista
    for k in range(total):
        if np.isnan(duas["dist"][k]):
            G["duas"].append(None)
        else:
            G["duas"].append({"dist": r3(duas["dist"][k]),
                              "ombros": r3(duas["ombros"][k]) if not np.isnan(duas["ombros"][k]) else None,
                              "meio": [r1(duas["meio"][k, 0]), r1(duas["meio"][k, 1])],
                              "segurando": bool(duas["segurando"][k])})
    saida.write_text(json.dumps(G, ensure_ascii=False, separators=(",", ":"), default=_json), encoding="utf-8")
    pres_tot = sum(1 for k in range(total) if any(G["maos"][l][k] and G["maos"][l][k]["a"] > 0.5 for l in LADOS))
    fala(f"gestos.json gravado: {saida} ({saida.stat().st_size / 1024:.0f} KB) · {len(eventos)} eventos · "
         f"mão em {100 * pres_tot / total:.0f}% dos quadros · lado trocado em {trocas} quadros, "
         f"{repetidas} leituras repetidas, {rel['descartes_esquerda'] + rel['descartes_direita']} saltos descartados, "
         f"{rel['preenchidos_esquerda'] + rel['preenchidos_direita']} quadros preenchidos")
    imprimir_resumo(G, palavras)
    if args.folha is not None:
        video = pasta / (cenas.get("fonte", {}).get("video") or "fala.mp4")
        folha(pasta, G, Path(args.folha).resolve() if args.folha else pasta / "folha-gestos.jpg", video)
    return 1 if pres_tot < 0.1 * total else 0


if __name__ == "__main__":
    sys.exit(main())
