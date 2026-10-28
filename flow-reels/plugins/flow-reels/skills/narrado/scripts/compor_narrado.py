# -*- coding: utf-8 -*-
"""A imagem do reel narrado, muda, em 1080 x 1920 a 30 quadros por segundo.

Tudo sai do tomadas.json e do relogio mestre (construcao/linha_do_tempo.json). Nenhum
tempo esta escrito aqui dentro: cada tomada diz de onde vem na fonte, em que palavra
da voz ela entra, onde a camera empurra, onde o anel se desenha e como ela chega.
Os campos, um por um, estao em referencias/TOMADAS.md.

O que este script monta, por cima da superficie da marca com grao:

  abertura   a tomada mais forte da filmagem, em largura cheia, com o cartao HTML
             (modelos/abertura.html) por cima: pilula com o logo oficial e o titulo
             entrando palavra por palavra, uma palavra na cor de destaque
  corpo      a filmagem em largura cheia, empurroes lentos no que a voz nomeia, o anel
             desenhado a mao se desenhando ali, transicoes de 0,30 a 0,42 s, o credito
             em toda tomada, e as cartas em leque quando a tomada for de resumo
  fechamento a ultima tomada desfocada e escurecida, com o HTML de comentario por cima
             (modelos/fechamento.html): a palavra digitada e o item voando para a DM

Uso:

    flow-reels narrado/compor_narrado --projeto projetos/x --narrado 01
    flow-reels narrado/compor_narrado --projeto projetos/x --narrado 01 --quadros 1.0 6.4 22.0
    flow-reels narrado/compor_narrado --projeto projetos/x --narrado 01 --marca caminho/tokens.json

Com --quadros ele so grava esses instantes em conferencia/quadro-<t>.png, para olhar
antes de gastar o render inteiro. Escreve construcao/imagem.mp4, construcao/plano.json
(os tempos ja resolvidos, que a legenda e a conferencia leem) e construcao/eventos.json
(os momentos que pedem efeito sonoro, que o mixar.py le).
"""

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402
import renderizar_html as rh  # noqa: E402

W, H, FPS = cm.LARGURA, cm.ALTURA, cm.FPS
ESCALA_MAX = 2.2              # empurrao maximo sobre o enquadramento da tomada
TRANSICAO_PADRAO = 0.36
ALTURA_MAX_JANELA = 1320      # a filmagem em largura cheia nao passa disso, para caber entre 150 e 1480
CENTRO_PADRAO = 815
LARGURA_DECODIFICADA = 1920   # a fonte e lida no maximo nesta largura


# ------------------------------------------------------------------- curvas

def suave(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * x * (x * (6 * x - 15) + 10)


def sai(x, p=3):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** p


# ------------------------------------------------------------------- leitura da fonte

class Leitor:
    """Le a fonte quadro a quadro para a frente, a partir de um instante, a 30 fps.

    Volta atras ou pula longe reabrindo o ffmpeg. Quando a fonte acaba, segura o ultimo
    quadro e marca congelado, que a conferencia reprova se passar de 1 s.
    """

    def __init__(self, caminho, inicio):
        self.caminho, self.inicio = str(caminho), float(inicio)
        tam = cm.tamanho_video(caminho)
        if tam is None:
            cm.erro("a fonte %s nao tem video." % caminho)
        ow, oh = tam
        self.fator = min(1.0, LARGURA_DECODIFICADA / float(ow))
        self.w = int(round(ow * self.fator / 2) * 2)
        self.h = int(round(oh * self.fator / 2) * 2)
        self.proc, self.idx, self.ultimo, self.acabou = None, -1, None, False
        self.congelado_em = None

    def _abrir(self, j):
        self.fechar()
        filtro = "fps=%d,scale=%d:%d" % (FPS, self.w, self.h)
        self.proc = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-ss", "%.3f" % (self.inicio + j / float(FPS)), "-i", self.caminho,
             "-an", "-vf", filtro, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10 ** 7)
        self.idx, self.acabou = j - 1, False

    def quadro(self, j):
        j = max(0, int(j))
        if self.proc is None or j < self.idx or j > self.idx + 90:
            self._abrir(j)
        n = self.w * self.h * 3
        while self.idx < j and not self.acabou:
            bruto = self.proc.stdout.read(n)
            if len(bruto) < n:
                self.acabou = True
                break
            self.ultimo = np.frombuffer(bruto, np.uint8).reshape(self.h, self.w, 3)
            self.idx += 1
        if self.acabou and j > self.idx and self.congelado_em is None:
            self.congelado_em = j
        if self.ultimo is None:
            return np.zeros((self.h, self.w, 3), np.uint8)
        return self.ultimo

    def fechar(self):
        if self.proc is not None:
            try:
                self.proc.stdout.close()
                self.proc.kill()
                self.proc.wait(timeout=5)
            except Exception:
                pass
        self.proc = None


# ------------------------------------------------------------------- desenho

def colar(dst, rgba, x, y, op=1.0):
    """Cola uma imagem BGRA (uint8) em dst (BGR uint8) com transparencia."""
    h, w = rgba.shape[:2]
    x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
    if x0 >= x1 or y0 >= y1 or op <= 0:
        return
    s = rgba[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    a = s[..., 3:4] / 255.0 * op
    d = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = (d * (1 - a) + s[..., :3] * a).astype(np.uint8)


def desfocar(img, sigma):
    if sigma < 0.8:
        return img
    p = cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    p = cv2.GaussianBlur(p, (0, 0), max(0.3, sigma / 4.0))
    return cv2.resize(p, (W, H), interpolation=cv2.INTER_LINEAR)


def ampliar(img, s, cx=W / 2, cy=H / 2):
    M = np.float32([[s, 0, cx - s * cx], [0, s, cy - s * cy]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def bgr(rgb):
    return (int(rgb[2]), int(rgb[1]), int(rgb[0]))


def fazer_superficies(cor_rgb, intensidade):
    """Tres superficies com grao fixo, alternadas a cada dois quadros."""
    base = np.zeros((H, W, 3), np.float32)
    base[:] = bgr(cor_rgb)
    amp = 6.0 + 60.0 * float(intensidade)
    rng = np.random.default_rng(7)
    saida = []
    for _ in range(3):
        ruido = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
        ruido = cv2.resize(ruido, (W, H), interpolation=cv2.INTER_NEAREST)[..., None]
        saida.append(np.clip(base + ruido * amp * 0.25, 0, 255).astype(np.uint8))
    return saida


def chip(texto, fonte, cores_marca, tamanho=30):
    f = ImageFont.truetype(str(fonte), tamanho)
    largura = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(texto, font=f))
    pw, ph = 22, 12
    w, h = largura + pw * 2, tamanho + ph * 2 + 6
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=tuple(cores_marca["superficie"]) + (225,))
    d.text((pw, ph - 2), texto, font=f, fill=tuple(cores_marca["tinta"]) + (255,))
    a = np.asarray(im)
    return np.dstack([a[..., 2], a[..., 1], a[..., 0], a[..., 3]])


def preparar_carta(caminho, angulo, cores_marca, raio, largura=600, altura_max=820):
    im = Image.open(caminho).convert("RGB")
    esc = largura / float(im.width)
    if im.height * esc > altura_max:
        esc = altura_max / float(im.height)
    im = im.resize((max(1, int(im.width * esc)), max(1, int(im.height * esc))), Image.LANCZOS)
    w, h = im.size
    borda = 4
    cartao = Image.new("RGBA", (w + borda * 2, h + borda * 2), (0, 0, 0, 0))
    m = Image.new("L", cartao.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, cartao.width - 1, cartao.height - 1), raio + borda, fill=255)
    fundo = Image.new("RGBA", cartao.size, tuple(cores_marca["tinta_suave"]) + (255,))
    cartao.paste(fundo, (0, 0), m)
    mi = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mi).rounded_rectangle((0, 0, w - 1, h - 1), raio, fill=255)
    cartao.paste(im, (borda, borda), mi)
    folga = 60
    tela = Image.new("RGBA", (cartao.width + folga * 2, cartao.height + folga * 2), (0, 0, 0, 0))
    sombra = Image.new("L", tela.size, 0)
    sombra.paste(m, (folga, folga + 18))
    sombra = np.asarray(sombra, np.float32)
    sombra = cv2.GaussianBlur(sombra, (0, 0), 22) * 0.55
    sombra_rgba = np.zeros((tela.height, tela.width, 4), np.uint8)
    sombra_rgba[..., 3] = np.clip(sombra, 0, 255).astype(np.uint8)
    tela = Image.alpha_composite(Image.fromarray(sombra_rgba, "RGBA"), tela)
    tela.paste(cartao, (folga, folga), cartao)
    tela = tela.rotate(angulo, resample=Image.BICUBIC, expand=True)
    a = np.asarray(tela)
    return np.dstack([a[..., 2], a[..., 1], a[..., 0], a[..., 3]])


def pontos_do_anel(cx, cy, rx, ry, semente):
    """Uma volta e pouco, com o tremor de quem desenha a mao. Deterministico."""
    n = 140
    voltas = 1.12
    a0 = -2.25 + 0.3 * math.sin(semente)
    inclinacao = math.radians(-4 + 3 * math.sin(semente * 1.7))
    pts = []
    for i in range(n + 1):
        u = i / float(n)
        th = a0 + 2 * math.pi * voltas * u
        r = 1 + 0.035 * math.sin(3 * th + semente) + 0.02 * math.sin(7 * th + 2 * semente) + 0.03 * u
        x, y = rx * r * math.cos(th), ry * r * math.sin(th)
        xr = x * math.cos(inclinacao) - y * math.sin(inclinacao)
        yr = x * math.sin(inclinacao) + y * math.cos(inclinacao)
        pts.append((cx + xr, cy + yr))
    return pts


# ------------------------------------------------------------------- plano

def caixa_lista(valor, onde):
    if valor is None:
        return None
    if not (isinstance(valor, (list, tuple)) and len(valor) == 4):
        cm.erro("%s precisa ser [x, y, largura, altura] em pixels da fonte." % onde)
    return [float(v) for v in valor]


def como_lista(valor):
    if valor is None:
        return []
    return valor if isinstance(valor, list) else [valor]


def resolver_plano(cam, tomadas, tl):
    palavras = tl["palavras"]
    total = float(tl["duracao"])
    seg_som = {s["nome"]: s for s in tl["segmentos"] if s["tipo"] == "som"}
    fonte_padrao = tomadas.get("fonte_padrao")
    credito_padrao = tomadas.get("credito_padrao")

    lista = tomadas.get("tomadas") or []
    if not lista:
        cm.erro('o tomadas.json nao tem a lista "tomadas".')
    plano = []
    for k, tm in enumerate(lista):
        nome = tm.get("id") or "t%02d" % (k + 1)
        onde = "tomada %s" % nome
        som = tm.get("som")
        if som:
            if som not in seg_som:
                cm.erro('%s diz "som": %r, e a trilha nao tem trecho com esse nome.' % (onde, som))
            t0 = seg_som[som]["t0"]
        elif k == 0:
            t0 = 0.0
        else:
            # a palavra e procurada depois do comeco da tomada anterior, para "voce" ou "isso"
            # repetidos na fala nao puxarem a tomada para tras
            depois = plano[-1]["t0"] + 0.3 if plano else -1.0
            t0 = cm.resolver_instante(tm.get("inicio"), palavras, onde, ajuste_padrao=-0.12, depois=depois)
            if t0 is None:
                cm.erro('%s precisa de "inicio" (segundos ou palavra da fala).' % onde)
        fonte = tm.get("fonte", fonte_padrao)
        cartas = como_lista(tm.get("cartas"))
        if som:
            fonte = seg_som[som].get("fonte") or fonte
        if not fonte and not cartas:
            cm.erro("%s nao tem fonte nem cartas." % onde)
        tipo_tr = tm.get("transicao", "desfoque") if k else "corte"
        if tipo_tr not in ("desfoque", "zoom", "corte"):
            cm.erro('%s: transicao %r nao existe (use desfoque, zoom ou corte).' % (onde, tipo_tr))
        d = 0.0 if tipo_tr == "corte" else float(tm.get("duracao_transicao", TRANSICAO_PADRAO))
        if tipo_tr != "corte" and not 0.30 <= d <= 0.42:
            cm.aviso("%s: transicao de %.2f s; o formato pede de 0,30 a 0,42 s. Ajustei." % (onde, d))
            d = min(max(d, 0.30), 0.42)
        item = {
            "id": nome, "t0": round(t0, 3), "transicao": tipo_tr, "d": d,
            "fonte": str(cam.no_projeto(fonte)) if fonte else None,
            "entrada": float(tm.get("entrada", 0.0)), "saida": tm.get("saida"),
            "pecas": seg_som[som]["pecas"] if som else None, "som": som,
            "recorte": caixa_lista(tm.get("recorte"), onde + " recorte"),
            "tela_cheia": tm.get("tela_cheia"), "centro_y": float(tm.get("centro_y", CENTRO_PADRAO)),
            "escurecer": float(tm.get("escurecer", 0.4 if cartas and fonte else 0.0)),
            "credito": tm.get("credito", credito_padrao),
            "empurroes": [], "aneis": [], "cartas": [],
        }
        if item["credito"] is not None and item["credito"] is not False:
            cm.recusar_travessao(item["credito"], onde + " credito")
        for i, e in enumerate(como_lista(tm.get("empurrao"))):
            item["empurroes"].append({
                "alvo": caixa_lista(e.get("alvo"), onde + " empurrao alvo"),
                "t": cm.resolver_instante(e.get("inicio", t0 + 0.2), palavras, onde + " empurrao",
                                          ajuste_padrao=-0.15, depois=t0 - 0.5),
                "duracao": min(max(float(e.get("duracao", 1.0)), 0.6), 1.6),
                "margem": float(e.get("margem", 0.25))})
        for i, a in enumerate(como_lista(tm.get("anel"))):
            item["aneis"].append({
                "caixa": caixa_lista(a.get("caixa"), onde + " anel caixa"),
                "t": cm.resolver_instante(a.get("palavra", a.get("inicio", t0 + 0.3)), palavras,
                                          onde + " anel", ajuste_padrao=0.0, depois=t0 - 0.5),
                "duracao": float(a.get("duracao", 0.45)), "semente": 1.3 + 2.1 * (k * 7 + i)})
        for i, c in enumerate(cartas):
            c = {"imagem": c} if isinstance(c, str) else c
            caminho = cam.no_projeto(c.get("imagem"))
            if not caminho or not caminho.is_file():
                cm.erro("%s: a carta %s nao existe." % (onde, c.get("imagem")))
            t = c.get("inicio")
            t = cm.resolver_instante(t, palavras, onde + " carta", depois=t0 - 0.5) if t is not None else t0 + 0.15 + 0.35 * i
            item["cartas"].append({"imagem": str(caminho), "t": t})
        plano.append(item)

    for k in range(1, len(plano)):
        if plano[k]["t0"] <= plano[k - 1]["t0"] + 0.5:
            cm.erro("a tomada %s comeca em %.2f s, cedo demais depois da %s (%.2f s)."
                    % (plano[k]["id"], plano[k]["t0"], plano[k - 1]["id"], plano[k - 1]["t0"]))
    for k, item in enumerate(plano):
        item["t1"] = plano[k + 1]["t0"] if k + 1 < len(plano) else total
        item["d_saida"] = plano[k + 1]["d"] if k + 1 < len(plano) else 0.0

    abertura = resolver_abertura(cam, tomadas.get("abertura") or {}, palavras)
    fechamento = resolver_fechamento(tomadas.get("fechamento") or {}, tomadas, palavras, total)
    return {"duracao": total, "tomadas": plano, "abertura": abertura, "fechamento": fechamento,
            "palavra_chave": fechamento.get("palavra"),
            "legenda": tomadas.get("legenda") or {}}


def resolver_abertura(cam, cfg, palavras):
    if not cfg:
        return None
    titulo = str(cfg.get("titulo", "")).strip()
    cm.recusar_travessao(titulo, "o titulo da abertura")
    cm.recusar_travessao(cfg.get("kicker", ""), "o kicker da abertura")
    if cfg.get("ate"):
        fim = cm.resolver_instante(cfg["ate"], palavras, "abertura ate", fim=True) + 0.25
    else:
        i = next((i for i, p in enumerate(palavras) if p["texto"][-1:] in ".?!:"), min(6, len(palavras) - 1))
        fim = palavras[i]["fim"] + 0.25
    destaque = cm.normalizar(cfg.get("destaque", ""))
    termos = titulo.split()
    tempos, cursor = [], 0
    for termo in termos:
        alvo = cm.normalizar(termo)
        achou = None
        for i in range(cursor, len(palavras)):
            if palavras[i]["inicio"] > fim:
                break
            if cm.normalizar(palavras[i]["texto"]) == alvo:
                achou = i
                break
        if achou is None:
            tempos.append(None)
        else:
            tempos.append(palavras[achou]["inicio"])
            cursor = achou + 1
    n = len(tempos)
    conhecidos = [(i, t) for i, t in enumerate(tempos) if t is not None]
    for i in range(n):
        if tempos[i] is not None:
            continue
        antes = [c for c in conhecidos if c[0] < i]
        depois = [c for c in conhecidos if c[0] > i]
        a = antes[-1] if antes else (-1, 0.05)
        b = depois[0] if depois else (n, max(fim - 0.35, a[1] + 0.2))
        tempos[i] = a[1] + (b[1] - a[1]) * (i - a[0]) / float(b[0] - a[0])
    logo = cfg.get("logo")
    url = None
    if logo:
        caminho = cam.no_projeto(logo)
        if not caminho.is_file():
            cm.erro("o logo da abertura nao existe: %s. Baixe com flow-reels componentes/baixar-logo "
                    "(ou componentes/baixar-marca para o logo em cor), nunca desenhe." % logo)
        url = cm.url_de(caminho)
    destaques = sum(1 for t in termos if cm.normalizar(t) == destaque) if destaque else 0
    if destaque and destaques == 0:
        cm.aviso("a palavra de destaque %r nao esta no titulo." % cfg.get("destaque"))
    return {
        "fim": round(fim, 3), "kicker": cfg.get("kicker", ""), "topo": cfg.get("topo", 190),
        "logo": {"url": url, "monocromatico": bool(cfg.get("logo_monocromatico", str(logo).lower().endswith(".svg")))} if url else None,
        "palavras": [{"texto": termo, "t": round(max(0.0, tempos[i]), 3),
                      "destaque": bool(destaque) and cm.normalizar(termo) == destaque}
                     for i, termo in enumerate(termos)],
    }


def resolver_fechamento(cfg, tomadas, palavras, total):
    if not cfg:
        return {}
    palavra = str(cfg.get("palavra") or tomadas.get("palavra_chave") or "").strip().upper()
    if not palavra:
        cm.erro('o fechamento precisa da "palavra" do comentario.')
    item = str(cfg.get("item", "")).strip()
    cm.recusar_travessao(item, "o item do fechamento")
    t_inicio = cm.resolver_instante(cfg.get("inicio"), palavras, "fechamento inicio", ajuste_padrao=-0.2)
    if t_inicio is None:
        cm.erro('o fechamento precisa de "inicio" (a palavra da voz em que a caixa de comentario sobe).')
    i = cm.achar_palavra(palavras, palavra, 1, depois=t_inicio - 0.3)
    t_dig = palavras[i]["inicio"] if i is not None else t_inicio + 0.5
    por_letra = float(cfg.get("por_letra", 0.09))
    t_env = t_dig + len(palavra) * por_letra + 0.2
    if cfg.get("item_palavra"):
        t_voar = cm.resolver_instante(cfg["item_palavra"], palavras, "fechamento item_palavra",
                                      depois=t_inicio)
    else:
        t_voar = t_env + 0.45
    t_voar = max(t_voar, t_env + 0.25)
    if t_voar + 0.5 > total:
        cm.aviso("o item chega na DM depois do fim do reel. Aumente a cauda do fechamento.")
    return {"inicio": round(t_inicio, 3), "palavra": palavra, "item": item,
            "t_digitar": round(t_dig, 3), "por_letra": por_letra, "t_enviar": round(t_env, 3),
            "t_voar": round(t_voar, 3), "campo": cfg.get("campo"), "rotulo_dm": cfg.get("rotulo_dm")}


# ------------------------------------------------------------------- compositor

class Compositor:
    def __init__(self, cam, plano, tokens, origem_tokens):
        self.cam, self.plano = cam, plano
        self.cores = cm.cores(tokens)
        tx = tokens.get("textura") or {}
        self.superficies = fazer_superficies(self.cores["superficie"], tx.get("grao_intensidade", 0.14))
        self.raio = int((tokens.get("forma") or {}).get("raio_canto", 20))
        self.fonte_corpo = cm.arquivo_fonte(tokens, origem_tokens, "corpo")
        self.leitores = {}
        self.chips = {}
        self.cartas = {}
        self.cor_destaque = bgr(self.cores["destaque"])
        self.cor_escura = bgr(self.cores["escuro"])
        self.html = {"abertura": None, "fechamento": None}
        self.congelados = {}
        for item in plano["tomadas"]:
            self._preparar(item)

    # ---- preparo de cada tomada
    def _preparar(self, item):
        if item["fonte"]:
            if not Path(item["fonte"]).is_file():
                cm.erro("a fonte da tomada %s nao existe: %s" % (item["id"], item["fonte"]))
            sonda = Leitor(item["fonte"], 0)
            f = sonda.fator
            sw, sh = sonda.w, sonda.h
            item["_fator"], item["_sw"], item["_sh"] = f, sw, sh
            rec = item["recorte"] or [0, 0, sw / f, sh / f]
            rx, ry, rw, rhh = [v * f for v in rec]
            cheia = item["tela_cheia"]
            if cheia is None:
                cheia = (rw / rhh) < 0.8
            if cheia:
                caixa = (0, 0, W, H)
            else:
                bh = int(round(W * rhh / rw))
                if bh > ALTURA_MAX_JANELA:
                    bh = ALTURA_MAX_JANELA
                # entre a zona reservada de cima e a faixa da legenda, sempre que couber
                alto, baixo = cm.TOPO_RESERVADO + 10, cm.FAIXA_LEGENDA[0] - 20 - bh
                by = int(round(item["centro_y"] - bh / 2.0))
                by = min(max(by, alto), baixo) if baixo >= alto else max(0, baixo)
                caixa = (0, by, W, bh)
            # a vista base tem a proporcao da caixa, centrada no recorte
            alvo_ar = caixa[2] / float(caixa[3])
            if rw / rhh > alvo_ar:
                nw, nh = rhh * alvo_ar, rhh
            else:
                nw, nh = rw, rw / alvo_ar
            item["_base"] = (rx + (rw - nw) / 2, ry + (rhh - nh) / 2, nw, nh)
            item["_caixa"] = caixa
            item["_cheia"] = bool(cheia)
            self._conferir_cobertura(item)
            self._conferir_branco(item, sonda)
            sonda.fechar()
        else:
            item["_caixa"] = None
        if item["credito"]:
            self.chips[item["id"]] = chip(str(item["credito"]), self.fonte_corpo, self.cores)
        n = len(item["cartas"])
        for i, c in enumerate(item["cartas"]):
            ang = (i - (n - 1) / 2.0) * 6.0
            self.cartas[(item["id"], i)] = preparar_carta(c["imagem"], -ang, self.cores, self.raio)

    def _conferir_cobertura(self, item):
        precisa = (item["t1"] - item["t0"]) + item["d_saida"] + 0.05
        if item["pecas"]:
            return
        dur = cm.duracao(item["fonte"])
        limite = min(dur, float(item["saida"])) if item["saida"] is not None else dur
        if item["entrada"] + precisa > limite + 1e-3:
            cm.aviso("a tomada %s pede %.2f s da fonte a partir de %.2f s, e a fonte (ou a saida) acaba "
                     "em %.2f s: o fim congela por %.2f s. Antecipe a entrada ou encurte a tomada."
                     % (item["id"], precisa, item["entrada"], limite, item["entrada"] + precisa - limite))

    def _conferir_branco(self, item, sonda):
        meio = (item["t1"] - item["t0"]) / 2.0
        fr = sonda.quadro(int(meio * FPS))
        vx, vy, vw, vh = [int(round(v)) for v in item["_base"]]
        reg = fr[max(0, vy):vy + vh, max(0, vx):vx + vw]
        if reg.size == 0:
            return
        branco = float((reg.min(axis=2) > 225).mean())
        item["_branco"] = round(branco, 2)
        if branco > 0.6 and not item["empurroes"] and not item["cartas"]:
            cm.aviso("a tomada %s e %.0f%% branca e nao tem empurrao. Tela quase branca nao carrega "
                     "um beat sozinha: recorte ou empurre ate encher a largura." % (item["id"], 100 * branco))

    # ---- a vista da camera dentro da fonte
    def vista(self, item, t):
        bx, by, bw, bh = item["_base"]
        sw, sh = item["_sw"], item["_sh"]
        f = item["_fator"]
        dur = max(1.0, item["t1"] - item["t0"] + item["d_saida"])
        s = 1 + 0.03 * suave((t - item["t0"]) / dur)
        cur = self._escalar((bx, by, bw, bh), 1 / s)
        for e in item["empurroes"]:
            if t < e["t"]:
                break
            ax, ay, aw, ah = [v * f for v in e["alvo"]]
            m = e["margem"]
            aw2, ah2 = aw * (1 + 2 * m), ah * (1 + 2 * m)
            ar = bw / bh
            if aw2 / ah2 > ar:
                tw, th = aw2, aw2 / ar
            else:
                tw, th = ah2 * ar, ah2
            minw = bw / ESCALA_MAX
            if tw < minw:
                tw, th = minw, minw / ar
            cx, cy = ax + aw / 2, ay + ah / 2
            alvo = self._dentro((cx - tw / 2, cy - th / 2, tw, th), sw, sh)
            u = suave((t - e["t"]) / e["duracao"])
            cur = self._interpolar(cur, alvo, u)
            extra = max(0.0, t - e["t"] - e["duracao"])
            cur = self._escalar(cur, 1 / min(1.04, 1 + 0.012 * extra))
        return cur

    @staticmethod
    def _escalar(r, k):
        x, y, w, h = r
        cx, cy = x + w / 2, y + h / 2
        return (cx - w * k / 2, cy - h * k / 2, w * k, h * k)

    @staticmethod
    def _dentro(r, sw, sh):
        x, y, w, h = r
        if w <= sw:
            x = min(max(x, 0), sw - w)
        else:
            x = (sw - w) / 2
        if h <= sh:
            y = min(max(y, 0), sh - h)
        else:
            y = (sh - h) / 2
        return (x, y, w, h)

    @staticmethod
    def _interpolar(a, b, u):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        acx, acy, bcx, bcy = ax + aw / 2, ay + ah / 2, bx + bw / 2, by + bh / 2
        w = aw * (bw / aw) ** u
        h = ah * (bh / ah) ** u
        cx, cy = acx + (bcx - acx) * u, acy + (bcy - acy) * u
        return (cx - w / 2, cy - h / 2, w, h)

    # ---- um quadro de uma tomada
    def _leitor(self, item, peca=0):
        chave = (item["id"], peca)
        if chave not in self.leitores:
            if item["pecas"]:
                inicio = item["pecas"][peca][1]
            else:
                inicio = item["entrada"]
            self.leitores[chave] = Leitor(item["fonte"], inicio)
        return self.leitores[chave]

    def _quadro_fonte(self, item, t):
        if item["pecas"]:
            peca, p0 = 0, item["pecas"][0][0]
            for i, (tp, a, b) in enumerate(item["pecas"]):
                if t >= tp:
                    peca, p0 = i, tp
            leitor = self._leitor(item, peca)
            j = int(round((t - p0) * FPS))
        else:
            leitor = self._leitor(item)
            j = int(round((t - item["t0"]) * FPS))
        fr = leitor.quadro(j)
        if leitor.congelado_em is not None and item["id"] not in self.congelados:
            self.congelados[item["id"]] = round(t, 2)
        return fr

    def tomada(self, k, t, indice):
        item = self.plano["tomadas"][k]
        img = self.superficies[(indice // 2) % 3].copy()
        if item["fonte"]:
            fr = self._quadro_fonte(item, t)
            vx, vy, vw, vh = self.vista(item, t)
            cx, cy, cw, ch = item["_caixa"]
            s = cw / vw
            M = np.float32([[s, 0, -s * vx], [0, s, -s * vy]])
            jan = cv2.warpAffine(fr, M, (cw, ch), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            if item["escurecer"] > 0:
                fundo = np.empty_like(jan)
                fundo[:] = bgr(self.cores["superficie"])
                jan = cv2.addWeighted(jan, 1 - item["escurecer"], fundo, item["escurecer"], 0)
            img[cy:cy + ch, cx:cx + cw] = jan
            self._aneis(img, item, t, (vx, vy, vw, vh), s)
        self._cartas(img, item, t)
        c = self.chips.get(item["id"])
        if c is not None:
            # o credito fica logo abaixo da filmagem, longe do titulo da abertura e da faixa da
            # legenda; sem espaco embaixo, sobe para o topo, dentro da filmagem
            caixa = item["_caixa"] or (0, 400, W, 760)
            abaixo = caixa[1] + caixa[3] + 18
            acima = caixa[1] - c.shape[0] - 18
            if not item.get("_cheia") and abaixo + c.shape[0] <= cm.FAIXA_LEGENDA[0] - 16:
                y = abaixo
            elif not item.get("_cheia") and acima >= cm.TOPO_RESERVADO + 14:
                y = acima
            else:
                y = cm.TOPO_RESERVADO + 24
            colar(img, c, 60, y)
        return img

    def _aneis(self, img, item, t, v, s):
        vx, vy, vw, vh = v
        f = item["_fator"]
        cx0, cy0 = item["_caixa"][0], item["_caixa"][1]
        ativos = [a for a in item["aneis"] if t >= a["t"]]
        if not ativos:
            return
        a = ativos[-1]   # um destaque por vez: o anel novo apaga o anterior
        x, y, w, h = [q * f for q in a["caixa"]]
        cx = cx0 + (x + w / 2 - vx) * s
        cy = cy0 + (y + h / 2 - vy) * s
        rx = w / 2 * s * 1.12 + 18
        ry = h / 2 * s * 1.25 + 18
        u = sai((t - a["t"]) / a["duracao"])
        pts = pontos_do_anel(cx, cy, rx, ry, a["semente"])
        n = max(2, int(len(pts) * u))
        arr = np.array(pts[:n], np.float32).reshape(-1, 1, 2)
        arr = np.round(arr * 4).astype(np.int32)
        cv2.polylines(img, [arr], False, self.cor_escura, 14, cv2.LINE_AA, shift=2)
        cv2.polylines(img, [arr], False, self.cor_destaque, 8, cv2.LINE_AA, shift=2)

    def _cartas(self, img, item, t):
        n = len(item["cartas"])
        for i, c in enumerate(item["cartas"]):
            if t < c["t"]:
                continue
            rgba = self.cartas[(item["id"], i)]
            u = sai((t - c["t"]) / 0.36)
            meio = i - (n - 1) / 2.0
            cx = W / 2 + meio * 190
            cy = 800 + abs(meio) * 24 + 90 * (1 - u)
            colar(img, rgba, cx - rgba.shape[1] / 2, cy - rgba.shape[0] / 2)

    # ---- o quadro final
    def quadro(self, t, indice):
        tms = self.plano["tomadas"]
        k = max(i for i, it in enumerate(tms) if it["t0"] <= t + 1e-6)
        img = self.tomada(k, t, indice)
        it = tms[k]
        if k > 0 and it["d"] > 0 and t < it["t0"] + it["d"]:
            ant = self.tomada(k - 1, t, indice)
            u = suave((t - it["t0"]) / it["d"])
            if it["transicao"] == "zoom":
                ant = ampliar(ant, 1 + 0.22 * u)
                img = ampliar(img, 0.9 + 0.1 * u)
                sig = 10 * math.sin(math.pi * u)
                ant, img = desfocar(ant, sig), desfocar(img, sig)
            else:
                ant = desfocar(ant, 1 + 14 * u)
                img = desfocar(img, 1 + 14 * (1 - u)) if u < 0.98 else img
            img = cv2.addWeighted(ant, 1 - u, img, u, 0)
        fe = self.plano["fechamento"]
        if fe and t >= fe["inicio"]:
            u = sai((t - fe["inicio"]) / 0.36)
            # empurrao lento por baixo do fechamento: o fundo nunca congela, mesmo se a fonte acabar
            resto = max(0.5, self.plano["duracao"] - fe["inicio"])
            img = ampliar(img, 1 + 0.08 * suave((t - fe["inicio"]) / resto))
            img = desfocar(img, 18 * u)
            fundo = np.empty_like(img)
            fundo[:] = bgr(self.cores["superficie"])
            img = cv2.addWeighted(img, 1 - 0.5 * u, fundo, 0.5 * u, 0)
        ab = self.plano["abertura"]
        if ab and self.html["abertura"] and t < ab["fim"] + 0.3:
            self._sobrepor(img, "abertura", int(round(t * FPS)))
        if fe and self.html["fechamento"] and t >= fe["inicio"]:
            self._sobrepor(img, "fechamento", int(round((t - fe["inicio"]) * FPS)))
        return img

    def _sobrepor(self, img, nome, j):
        pasta, n = self.html[nome]
        if n == 0:
            return
        q = cv2.imread(str(pasta / ("q%05d.png" % min(max(j, 0), n - 1))), cv2.IMREAD_UNCHANGED)
        if q is not None and q.shape[2] == 4:
            colar(img, q, 0, 0)

    def fechar(self):
        for l in self.leitores.values():
            l.fechar()


# ------------------------------------------------------------------- html e eventos

def preparar_html(cam, plano, tokens, refazer=False):
    """Renderiza abertura e fechamento, reaproveitando o que ja foi feito com os mesmos dados."""
    saida = {"abertura": None, "fechamento": None}
    modelos = cm.SKILL / "modelos"
    ab, fe = plano["abertura"], plano["fechamento"]
    pedidos = []
    if ab:
        dados = {"duracao": round(ab["fim"] + 0.3, 3), "kicker": ab["kicker"], "logo": ab["logo"],
                 "palavras": ab["palavras"], "saida": ab["fim"], "topo": ab["topo"]}
        pedidos.append(("abertura", modelos / "abertura.html", dados))
    if fe:
        z = fe["inicio"]
        dados = {"duracao": round(plano["duracao"] - z, 3), "palavra": fe["palavra"], "item": fe["item"],
                 "t_digitar": round(fe["t_digitar"] - z, 3), "por_letra": fe["por_letra"],
                 "t_enviar": round(fe["t_enviar"] - z, 3), "t_voar": round(fe["t_voar"] - z, 3)}
        if fe.get("campo"):
            dados["campo"] = fe["campo"]
        if fe.get("rotulo_dm"):
            dados["rotulo_dm"] = fe["rotulo_dm"]
        pedidos.append(("fechamento", modelos / "fechamento.html", dados))
    for nome, pagina, dados in pedidos:
        pasta = cam.construcao / nome
        marca_dados = {"dados": dados, "tokens": tokens}
        guardado = pasta / "dados.json"
        n_esperado = int(round(dados["duracao"] * FPS))
        if (not refazer and guardado.is_file() and cm.ler_json(guardado) == json.loads(json.dumps(marca_dados))
                and len(list(pasta.glob("q*.png"))) == n_esperado):
            cm.fala("%s: reaproveitando %d quadros ja renderizados." % (nome, n_esperado))
        else:
            if pasta.is_dir():
                shutil.rmtree(pasta)
            pasta.mkdir(parents=True)
            cm.fala("%s: renderizando %d quadros do HTML..." % (nome, n_esperado))
            rh.renderizar(pagina, dados, tokens, pasta, pastas_extra=[cam.projeto])
            cm.gravar_json(guardado, marca_dados)
        saida[nome] = (pasta, len(list(pasta.glob("q*.png"))))
    return saida


def eventos_do_plano(plano):
    ev = []
    ab, fe = plano["abertura"], plano["fechamento"]
    if ab:
        ev.append({"t": 0.05, "tipo": "alternar", "nota": "pilula da abertura"})
        for p in ab["palavras"]:
            ev.append({"t": p["t"], "tipo": "pop", "nota": "titulo: " + p["texto"]})
    for it in plano["tomadas"][1:]:
        if it["transicao"] != "corte":
            ev.append({"t": it["t0"], "tipo": "whoosh", "nota": "transicao para " + it["id"]})
    for it in plano["tomadas"]:
        for a in it["aneis"]:
            ev.append({"t": a["t"], "tipo": "varredura", "nota": "anel em " + it["id"]})
        for c in it["cartas"]:
            ev.append({"t": c["t"] + 0.3, "tipo": "pop", "nota": "carta assenta"})
    if fe:
        ev.append({"t": fe["inicio"], "tipo": "whoosh", "nota": "fechamento"})
        fim_dig = fe["t_digitar"] + len(fe["palavra"]) * fe["por_letra"]
        ev.append({"t": fe["t_digitar"], "tipo": "digitar", "fim": round(fim_dig, 3), "nota": "palavra"})
        ev.append({"t": fe["t_enviar"] - 0.03, "tipo": "clique", "nota": "botao de envio"})
        ev.append({"t": fe["t_enviar"], "tipo": "enviar", "nota": "envio"})
        ev.append({"t": fe["t_voar"] + 0.5, "tipo": "assentar", "nota": "item chega na DM"})
    return sorted(ev, key=lambda e: e["t"])


def limpar_plano(plano):
    """O plano sem as chaves internas, para gravar."""
    copia = json.loads(json.dumps(plano, default=str))
    for it in copia["tomadas"]:
        for k in [k for k in it if k.startswith("_") and k not in ("_caixa", "_branco", "_cheia")]:
            it.pop(k)
        if "_caixa" in it:
            it["caixa_na_tela"] = it.pop("_caixa")
        if "_branco" in it:
            it["fracao_branca"] = it.pop("_branco")
        if "_cheia" in it:
            it["tela_cheia"] = it.pop("_cheia")
    return copia


def principal(argv=None):
    an = cm.argumentos_de_reel(argparse.ArgumentParser(description="Monta a imagem do reel narrado."))
    an.add_argument("--marca", default=None, help="tokens.json ou pasta da marca (padrao marca/)")
    an.add_argument("--quadros", type=float, nargs="*", default=None,
                    help="so grava estes instantes em conferencia/, para olhar antes do render")
    an.add_argument("--refazer-html", action="store_true", help="renderiza abertura e fechamento de novo")
    an.add_argument("--crf", type=int, default=17)
    op = an.parse_args(argv)
    cm.exigir_ffmpeg()
    cam = cm.Caminhos(op.projeto, op.narrado)
    if not cam.linha.is_file():
        cm.erro("falta construcao/linha_do_tempo.json. Rode o linha_do_tempo.py antes.")
    tomadas = cm.ler_tomadas(cam)
    tl = cm.ler_json(cam.linha)
    tokens, origem = cm.ler_marca(op.marca)

    plano = resolver_plano(cam, tomadas, tl)
    comp = Compositor(cam, plano, tokens, origem)
    comp.html = preparar_html(cam, plano, tokens, op.refazer_html)
    eventos = eventos_do_plano(plano)
    cm.gravar_json(cam.plano, limpar_plano(plano))

    if op.quadros is not None:
        cam.conferencia.mkdir(parents=True, exist_ok=True)
        for t in op.quadros:
            img = comp.quadro(float(t), int(round(float(t) * FPS)))
            destino = cam.conferencia / ("quadro-%05.2f.png" % float(t))
            cv2.imwrite(str(destino), img)
            cm.fala(str(destino))
        comp.fechar()
        return 0

    total = int(round(plano["duracao"] * FPS))
    cam.construcao.mkdir(parents=True, exist_ok=True)
    cm.fala("compondo %d quadros (%.2f s)..." % (total, plano["duracao"]))
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "%dx%d" % (W, H),
         "-r", str(FPS), "-i", "-",
         "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setsar=1",
         "-c:v", "libx264", "-preset", "medium", "-crf", str(op.crf), "-profile:v", "high",
         "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
         "-r", str(FPS), "-movflags", "+faststart", str(cam.imagem)], stdin=subprocess.PIPE)
    try:
        for i in range(total):
            proc.stdin.write(comp.quadro(i / float(FPS), i).tobytes())
            if i and i % (FPS * 5) == 0:
                cm.fala("  %d de %d quadros" % (i, total))
    finally:
        proc.stdin.close()
        proc.wait()
        comp.fechar()
    if proc.returncode != 0:
        cm.erro("o ffmpeg nao fechou a imagem.")

    gravado = limpar_plano(plano)
    gravado["congelados"] = comp.congelados
    cm.gravar_json(cam.plano, gravado)
    cm.gravar_json(cam.eventos, eventos)
    if comp.congelados:
        cm.aviso("a fonte acabou antes da tomada em: %s. Isso congela a imagem." %
                 ", ".join("%s (%.2f s)" % kv for kv in comp.congelados.items()))
    cm.fala("imagem pronta: %s" % cam.imagem)
    return 0


if __name__ == "__main__":
    sys.exit(principal())
