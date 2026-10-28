#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compor.py  ·  o compositor 2.0: renderiza o reel inteiro a partir do plano de cenas

Lê o plano (cenas.json) da pasta do corte, extrai o vídeo da fala em quadros, abre o motor
(web/motor.html) num Chromium sem tela e pede um quadro por vez: o motor posiciona a linha do
tempo no instante do quadro, e a foto vai direto para o ffmpeg. O mesmo instante gera sempre o
mesmo quadro, então refazer um trecho dá exatamente o mesmo resultado.

O contrato inteiro (formatos, modos, transições) está em MOTOR.md, ao lado deste arquivo.

Uso:

    flow-reels produzir/compor --projeto projetos/<video> --corte 01
    flow-reels produzir/compor --projeto projetos/<video> --corte 01 --previa          540x960, com som, rápido
    flow-reels produzir/compor --projeto projetos/<video> --corte 01 --quadro 12.4     um PNG só daquele instante
    flow-reels produzir/compor --projeto projetos/<video> --corte 01 --de 10 --ate 16  só um trecho, com som

Entradas, na pasta do corte (projetos/<video>/materiais-de-trabalho/corte-NN/):
    cenas.json            o plano
    fala.mp4              a fala editada (ou o que cenas.fonte.video disser)
    palavras-corte.json   as palavras na linha do tempo da fala
    rosto.json            opcional: a caixa do rosto por quadro
    visao/                opcional (visao.py): recorte da pessoa, fundo limpo, profundidade, mãos,
                          corpo e objetos, entregues ao motor em window.VISAO (MOTOR.md 2.6). Sem a
                          pasta, window.VISAO = null e o motor é o de antes
Saídas, na mesma pasta:
    video.mp4             o reel sem som (o audio.py junta o som e entrega o corte)
    eventos.json          tudo que acontece na tela, com o tempo (ritmo e efeitos sonoros)
    layout.jsonl          por quadro: textos, legenda e rosto (zonas seguras e colisão) e, com texto
                          atrás de você, quanto a pessoa cobre de cada um (atras)
    contraste/            quadros amostrados sem texto, para a medida de contraste

Saída 0 = renderizou. 1 = o plano ou o motor deu erro. 2 = erro de uso ou de ambiente.
"""

import argparse
import http.server
import json
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.parse
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in AQUI.parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)
RAIZ = fabrica.raiz()        # a pasta de trabalho: projetos/, marca/, setup.json
PLUGIN = fabrica.plugin()    # o pacote: o motor, os componentes, a marca de exemplo

sys.path.insert(0, str(AQUI))
import ancoras  # noqa: E402  (os tempos presos à palavra e o fiscal dos mundos)

WEB = AQUI / "web"
ZONAS_PADRAO = {"topo": 220, "base": 1440, "lateral": 70}

# O quadro sai do Chromium como JPEG (faixa cheia, matriz BT.601). O vídeo de entrega é yuv420p de
# faixa limitada em BT.709, o que todo player e toda rede esperam: sem a conversão o arquivo sai
# yuvj420p e o gate de entrega reprova.
COR_SAIDA = ("scale=in_range=full:out_range=limited:in_color_matrix=bt601:out_color_matrix=bt709,"
             "format=yuv420p")
TAGS_COR = ["-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
            "-color_primaries", "bt709", "-color_trc", "bt709"]


def fala(msg):
    print(msg, flush=True)


def erro(msg, codigo=2):
    print("  erro: " + msg, file=sys.stderr, flush=True)
    sys.exit(codigo)


# ----------------------------------------------------------------------------- servidor local

class Entregador(http.server.SimpleHTTPRequestHandler):
    """Serve a pasta de trabalho e o plugin como se fossem uma pasta só: cada endereço é procurado
    primeiro na pasta de trabalho e depois no plugin. É assim que /componentes/marcas/x.png acha o
    logo baixado pela pessoa ou o que veio no pacote, e /marca/fontes/... acha a fonte dela ou a de
    exemplo."""

    def translate_path(self, caminho):
        limpo = caminho.split("?", 1)[0].split("#", 1)[0]
        limpo = urllib.parse.unquote(limpo).lstrip("/")
        partes = [p for p in limpo.split("/") if p and p not in (".", "..")]
        for base in (RAIZ, PLUGIN):
            alvo = base.joinpath(*partes)
            if alvo.exists():
                return str(alvo)
        return str(RAIZ.joinpath(*partes))

    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "max-age=3600")
        super().end_headers()


def porta_livre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Servidor(http.server.ThreadingHTTPServer):
    # o Chromium pede dezenas de arquivos de uma vez; a fila padrão (5) derrubava conexões
    request_queue_size = 128
    daemon_threads = True


def subir_servidor():
    porta = porta_livre()
    srv = Servidor(("127.0.0.1", porta), Entregador)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, porta


# ----------------------------------------------------------------------------- quadros

def url_de(caminho):
    """O endereço de um arquivo no servidor: o caminho dele na pasta de trabalho ou no plugin."""
    p = Path(caminho).resolve()
    for base in (RAIZ, PLUGIN):
        try:
            return "/" + str(p.relative_to(base.resolve())).replace("\\", "/")
        except ValueError:
            continue
    raise ValueError(f"{p} não está na pasta de trabalho ({RAIZ}) nem no plugin ({PLUGIN})")


def extrair_quadros(video, pasta, fps):
    """Extrai o vídeo em JPEG na fps do reel. Reaproveita se já foi extraído do mesmo arquivo."""
    pasta.mkdir(parents=True, exist_ok=True)
    marca = pasta / ".origem.json"
    estado = {"video": str(video.resolve()), "mtime": video.stat().st_mtime, "fps": fps}
    existentes = sorted(pasta.glob("f*.jpg"))
    if marca.is_file() and existentes:
        try:
            antes = json.loads(marca.read_text(encoding="utf-8"))
            if all(antes.get(k) == v for k, v in estado.items()) and antes.get("total") == len(existentes):
                return info_quadros(pasta, existentes)
        except (json.JSONDecodeError, OSError):
            pass
    for f in existentes:
        f.unlink()
    fala(f"  extraindo quadros de {video.name} a {fps} quadros/s...")
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", f"fps={fps}",
                        "-q:v", "2", str(pasta / "f%06d.jpg")], capture_output=True, text=True)
    if r.returncode != 0:
        erro(f"o ffmpeg não conseguiu extrair {video}:\n{r.stderr[-500:]}")
    existentes = sorted(pasta.glob("f*.jpg"))
    estado["total"] = len(existentes)
    marca.write_text(json.dumps(estado), encoding="utf-8")
    return info_quadros(pasta, existentes)


def info_quadros(pasta, arquivos):
    from PIL import Image
    with Image.open(arquivos[0]) as im:
        w, h = im.size
    return {"padrao": url_de(pasta) + "/f%06d.jpg", "total": len(arquivos), "largura": w, "altura": h}


# ----------------------------------------------------------------------------- a visão

def _json_ou_nada(caminho):
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def carregar_visao(pasta, video, fps, total_quadros):
    """O que o visao.py gravou em visao/, no formato de window.VISAO (MOTOR.md 2.6), ou None.

    Sem a pasta: None, e o motor é o de antes. Pasta feita de outro fala.mp4 (outro arquivo, outra
    data ou outra fps, conferidos no visao/.origem.json): None também, com aviso, porque uma máscara
    de outra edição cairia fora da pessoa. Parte que o visao.py não marcou como válida vem null."""
    vdir = pasta / "visao"
    if not vdir.is_dir():
        return None
    origem = _json_ou_nada(vdir / ".origem.json") or {}
    try:
        st = video.stat()
        atual = {"video": str(video.resolve()), "mtime": st.st_mtime, "tamanho": st.st_size, "fps": fps}
    except OSError:
        atual = {}
    if not origem or any(origem.get(k) != v for k, v in atual.items()):
        print(f"  aviso: a pasta visao/ não é deste {video.name} (outra edição ou outra fps); o motor segue "
              f"sem a visão. Rode: flow-reels produzir/visao --projeto "
              f"<projeto> --corte <NN>", flush=True)
        return None
    partes = origem.get("partes") or {}

    def quadros(sub, prefixo):
        d = vdir / sub
        arqs = sorted(d.glob(prefixo + "*.png")) if d.is_dir() else []
        if not arqs:
            return None
        from PIL import Image
        with Image.open(arqs[0]) as im:
            w, h = im.size
        return {"padrao": url_de(d) + f"/{prefixo}%06d.png", "total": len(arqs), "largura": w, "altura": h}

    visao = {
        "mascara": quadros("mascara", "m") if partes.get("mascara") else None,
        "fundo": url_de(vdir / "fundo-limpo.jpg") if partes.get("fundo") and (vdir / "fundo-limpo.jpg").is_file() else None,
        "buraco": url_de(vdir / "fundo-buraco.png") if partes.get("fundo") and (vdir / "fundo-buraco.png").is_file() else None,
        "fundo_profundidade": url_de(vdir / "fundo-profundidade.png") if partes.get("fundo") and (vdir / "fundo-profundidade.png").is_file() else None,
        "profundidade": quadros("profundidade", "p") if partes.get("profundidade") else None,
        "maos": _json_ou_nada(vdir / "maos.json") if partes.get("maos") else None,
        "corpo": _json_ou_nada(vdir / "corpo.json") if partes.get("corpo") else None,
        "objetos": _json_ou_nada(vdir / "objetos.json") if partes.get("objetos") else None,
        "meta": _json_ou_nada(vdir / "visao.json"),
        "gestos": None,
        "expressao": None,
    }
    # os gestos das mãos (scripts/gestos.py, 4.0): só quando o gestos.json é deste mesmo vídeo (o
    # "origem" dele é o .origem.json da visão que ele leu) e as mãos da visão valem
    g = _json_ou_nada(vdir / "gestos.json") if partes.get("maos") else None
    if g:
        go = g.get("origem") or {}
        if all(go.get(k) == origem.get(k) for k in ("video", "mtime", "tamanho", "fps")):
            visao["gestos"] = g
        else:
            print("  aviso: o visao/gestos.json é de outra rodada da visão (outro vídeo ou outra edição); "
                  "rode o gestos.py de novo: flow-reels produzir/gestos "
                  "--projeto <projeto> --corte <NN>", flush=True)
    # o rosto e a expressão (scripts/expressao.py, 4.3): a mesma checagem de origem dos gestos; não depende
    # das mãos, só de ser deste mesmo vídeo
    x = _json_ou_nada(vdir / "expressao.json")
    if x:
        xo = x.get("origem") or {}
        if all(xo.get(k) == origem.get(k) for k in ("video", "mtime", "tamanho", "fps")):
            visao["expressao"] = x
        else:
            print("  aviso: o visao/expressao.json é de outro vídeo ou de outra edição; rode o expressao.py de "
                  "novo: flow-reels produzir/expressao --projeto <projeto> "
                  "--corte <NN>", flush=True)
    m = visao["mascara"]
    if m and abs(m["total"] - total_quadros) > 1:
        print(f"  aviso: a visão tem {m['total']} máscaras e o vídeo tem {total_quadros} quadros; "
              "rode o visao.py --refazer", flush=True)
    return visao


# ----------------------------------------------------------------------------- navegador

PECAS_3D = {"nuvem", "malha", "objeto3d"}


def nomes_gpu():
    """O que pede WebGL (a GPU): as peças da Onda 3 e o que a 4.0 lista em motor/gpu.json (sobreposições,
    modos e transições por nome)."""
    g = ler_json(AQUI / "gpu.json", {}) or {}
    return (PECAS_3D | set(g.get("sobre", [])), set(g.get("modos", [])), set(g.get("transicoes", [])))


def usa_3d(cenas):
    """O plano tem alguma peça em WebGL? Ela pede a GPU; sem ela, o Chromium sem tela cai no
    SwiftShader, que desenha certo mas ~4x mais devagar. "gpu": true no cenas.json liga sempre."""
    if cenas.get("gpu"):
        return True
    # o pós no quadro inteiro (4.3, web/pos.js) é WebGL2: qualquer item de pos, no reel ou numa cena,
    # liga a GPU (o acabamento é do ffmpeg e não pede)
    if tem_pos(cenas):
        return True
    sobre, modos, trans = nomes_gpu()

    def tem(lista):
        return any(isinstance(x, dict) and x.get("tipo") in sobre for x in (lista or []))
    if tem(cenas.get("sobre")) or tem(cenas.get("pos")):
        return True
    for c in cenas.get("cenas") or []:
        if not isinstance(c, dict):
            continue
        if tem(c.get("sobre")) or tem(c.get("pos")) or c.get("modo") in modos:
            return True
        for lado in ("entrada", "saida"):
            tr = c.get(lado)
            if isinstance(tr, dict) and tr.get("transicao") in trans:
                return True
    return False


def args_do_navegador(cenas):
    """Só os reels com 3D ligam a GPU (Metal, no Mac): os outros seguem no caminho de sempre e saem
    iguais aos já entregues, pixel a pixel."""
    if not usa_3d(cenas):
        return []
    if sys.platform == "darwin":
        return ["--use-angle=metal", "--enable-gpu", "--ignore-gpu-blocklist"]
    return ["--enable-gpu", "--ignore-gpu-blocklist"]


# ----------------------------------------------------------------------------- pós e acabamento (4.3)

LUTS = fabrica.pasta("componentes/luts")
# a foto da 1ª passada do pós: JPEG de qualidade alta (o PNG custa ~3x mais e a diferença some no JPEG 92
# da foto final; medido em docs-4/pos.md)
POS_CAPTURA = {"format": "jpeg", "quality": 95, "optimizeForSpeed": True}


def tem_pos(cenas):
    """O plano tem algum item de pós (CENAS.pos ou cena.pos)?"""
    if isinstance(cenas.get("pos"), list) and cenas["pos"]:
        return True
    return any(isinstance(c, dict) and isinstance(c.get("pos"), list) and c["pos"] for c in cenas.get("cenas") or [])


def _escapar_filtro(caminho):
    return "'" + str(caminho).replace("\\", "/").replace("'", "\\'").replace(":", "\\:") + "'"


def ler_cube(caminho):
    """Um .cube 3D (LUT_3D_SIZE N, vermelho variando mais rápido) como array N x N x N x 3 [b][g][r]."""
    import numpy as np
    n, dados = None, []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        if linha.upper().startswith("LUT_3D_SIZE"):
            n = int(linha.split()[1])
        elif linha[0] in "-.0123456789":
            dados.append([float(v) for v in linha.split()[:3]])
    if not n or len(dados) != n ** 3:
        erro(f"a LUT {caminho} não é um .cube 3D válido", 1)
    return np.array(dados, dtype=np.float64).reshape(n, n, n, 3)


def cor_pela_lut(cor, cube):
    """Uma cor [r, g, b] 0-255 levada pela LUT (trilinear), para o gate medir a legenda com a cor final."""
    import numpy as np
    n = cube.shape[0]
    p = np.clip(np.array(cor[:3], dtype=np.float64) / 255.0, 0, 1) * (n - 1)
    i0 = np.floor(p).astype(int)
    i1 = np.minimum(i0 + 1, n - 1)
    f = p - i0
    out = np.zeros(3)
    for db in (0, 1):
        for dg in (0, 1):
            for dr in (0, 1):
                w = (f[2] if db else 1 - f[2]) * (f[1] if dg else 1 - f[1]) * (f[0] if dr else 1 - f[0])
                out += w * cube[(i1 if db else i0)[2], (i1 if dg else i0)[1], (i1 if dr else i0)[0]]
    return [int(round(v)) for v in np.clip(out * 255.0, 0, 255)]


def acabamento_do_plano(cenas, pasta):
    """O acabamento global do cenas.json ("acabamento": {"grao", "vinheta", "lut"}), feito pelo ffmpeg na
    hora de codificar (docs-4/pos.md), ou None. A LUT e a vinheta trabalham em RGB planar (gbrp), antes da
    conversão de saída; o grão entra depois dela, só na luma (grão de película, sem cor)."""
    a = cenas.get("acabamento")
    if not a:
        return None
    if not isinstance(a, dict):
        erro('"acabamento" no cenas.json é um objeto: {"grao": 0..1, "vinheta": 0..1, "lut": "nome"}', 1)
    desconhecidas = set(a) - {"grao", "vinheta", "lut"}
    if desconhecidas:
        erro(f"acabamento: chave desconhecida {', '.join(sorted(desconhecidas))} (as que existem: grao, vinheta, lut)", 1)
    rgb, resumo, cube = [], [], None
    lut = a.get("lut")
    if lut:
        nome = str(lut)
        arq = Path(nome) if nome.endswith(".cube") else LUTS / f"{nome}.cube"
        if not arq.is_absolute():
            arq = (pasta / arq) if (pasta / arq).is_file() else (fabrica.achar(arq) if nome.endswith(".cube") else arq)
        if not arq.is_file():
            existentes = ", ".join(sorted(x.stem for x in LUTS.glob("*.cube"))) or "nenhuma"
            erro(f"acabamento: não achei a LUT {nome} (as da marca, em componentes/luts/: {existentes})", 1)
        rgb.append(f"lut3d=file={_escapar_filtro(arq.resolve())}:interp=tetrahedral")
        cube = ler_cube(arq)
        resumo.append(f"lut {arq.stem}")
    vinheta = float(a.get("vinheta") or 0)
    if not 0 <= vinheta <= 1:
        erro("acabamento: vinheta vai de 0 a 1", 1)
    if vinheta > 0:
        # o ângulo da lente do filtro vignette (0 a PI/2); aspect = o do quadro: a vinheta segue o retângulo
        rgb.append(f"vignette=angle={0.12 + vinheta * 0.78:.4f}:aspect={1080 / 1920:.4f}")
        resumo.append(f"vinheta {vinheta:g}")
    grao = float(a.get("grao") or 0)
    if not 0 <= grao <= 1:
        erro("acabamento: grao vai de 0 a 1", 1)
    filtro_grao = None
    if grao > 0:
        # semente fixa: o render inteiro sai igual em toda rodada. Ruído temporal "médio" (t+a): o grão
        # muda de quadro a quadro com calma. O gaussiano puro (t) com a mesma cara multiplicava o arquivo
        # por 5 a 8 no crf 18 (medido em docs-4/pos.md); o grão custa bits de qualquer jeito
        filtro_grao = f"noise=c0s={max(1, round(grao * 24))}:c0f=t+a:c0_seed=40507"
        resumo.append(f"grão {grao:g}")
    if not rgb and not filtro_grao:
        return None
    return {"rgb": ",".join(rgb) or None, "grao": filtro_grao, "cube": cube, "resumo": " + ".join(resumo)}


def vf_video(ac):
    """O -vf do vídeo: a conversão de saída de sempre, com o acabamento em volta quando o plano pede."""
    if not ac:
        return COR_SAIDA
    partes = []
    if ac["rgb"]:
        partes += ["scale=in_range=full:in_color_matrix=bt601", "format=gbrp", ac["rgb"]]
    partes.append(COR_SAIDA)
    if ac["grao"]:
        partes.append(ac["grao"])
    return ",".join(partes)


def acabar_imagem(dados, ac):
    """Uma imagem (bytes JPEG ou PNG) com o acabamento, em PNG: o --quadro e o contraste veem o quadro final."""
    partes = []
    if ac["rgb"]:
        partes += ["format=gbrp", ac["rgb"]]
    if ac["grao"]:
        partes += ["format=yuv444p", ac["grao"]]
    partes.append("format=rgb24")
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "image2pipe", "-i", "-", "-vf", ",".join(partes),
                        "-frames:v", "1", "-f", "image2pipe", "-c:v", "png", "-"],
                       input=dados, capture_output=True)
    if r.returncode != 0 or not r.stdout:
        erro("o ffmpeg não aplicou o acabamento: " + r.stderr.decode("utf-8", "replace")[-400:], 1)
    return r.stdout


class PassadaPos:
    """A segunda passada do pós (web/pos.js): com pós ativo no instante, o motor esconde a legenda e a
    transição, a página é fotografada pelo CDP (sem decodificar no Python), a foto volta ao motor, passa
    pelos shaders e é desenhada na #camada-pos, embaixo da legenda. A foto seguinte já é o quadro final."""

    def __init__(self, pag):
        self.pag = pag
        self.cdp = pag.context.new_cdp_session(pag)

    def passar(self, t):
        if not self.pag.evaluate("t => window.Motor.Pos.antes(t)", t):
            return False
        r = self.cdp.send("Page.captureScreenshot", POS_CAPTURA)
        self.pag.evaluate("([b, f]) => window.Motor.Pos.aplicar(b, f)", [r["data"], POS_CAPTURA["format"]])
        return True


def medir_cores_finais(info, final, fundo, legenda, ac):
    """O gate de contraste mede a cor de cada texto contra o quadro sem texto. Com o pós ou o acabamento
    ligados, a cor do CSS já não é a que aparece: o texto também passa pelo efeito. Então a cor de cada
    texto (fora a legenda) é MEDIDA no quadro final: os pixels da caixa que mudam entre o quadro com texto
    e o quadro sem texto (os dois com o mesmo pós e o mesmo acabamento) são a letra, e a mediana deles é a
    cor. A legenda fica fora do pós; com LUT, a cor e o contorno dela passam pela LUT. O CSS fica em
    "cor_css"."""
    import io
    import numpy as np
    from PIL import Image
    F = np.asarray(Image.open(io.BytesIO(final)).convert("RGB"), dtype=np.int16)
    B = np.asarray(Image.open(io.BytesIO(fundo)).convert("RGB"), dtype=np.int16)
    if F.shape != B.shape:
        return info
    alt, larg = F.shape[:2]
    ex, ey = larg / 1080.0, alt / 1920.0
    d = np.abs(F - B).sum(axis=2)
    leg = legenda if isinstance(legenda, list) and len(legenda) == 4 else None

    def dentro_da_legenda(cx):
        if not leg:
            return False
        x, y, w, h = cx
        return x >= leg[0] - 4 and y >= leg[1] - 4 and x + w <= leg[0] + leg[2] + 4 and y + h <= leg[1] + leg[3] + 4

    for tx in info:
        cx = tx.get("caixa")
        if not cx or not tx.get("cor"):
            continue
        if dentro_da_legenda(cx):
            if ac and ac.get("cube") is not None:
                tx["cor_css"] = tx["cor"]
                tx["cor"] = cor_pela_lut(tx["cor"], ac["cube"])
                if tx.get("contorno"):
                    tx["contorno"] = cor_pela_lut(tx["contorno"], ac["cube"])
            continue
        xa, ya = max(0, int(cx[0] * ex)), max(0, int(cx[1] * ey))
        xb, yb = min(larg, int((cx[0] + cx[2]) * ex) + 1), min(alt, int((cx[1] + cx[3]) * ey) + 1)
        if xb - xa < 2 or yb - ya < 2:
            continue
        dd = d[ya:yb, xa:xb].copy()
        if leg:
            lx0, ly0 = int(leg[0] * ex) - xa, int(leg[1] * ey) - ya
            lx1, ly1 = int((leg[0] + leg[2]) * ex) + 1 - xa, int((leg[1] + leg[3]) * ey) + 1 - ya
            dd[max(0, ly0):max(0, ly1), max(0, lx0):max(0, lx1)] = 0
        # sem letra que se veja (o texto ainda não entrou, ou some no fundo): fica a cor do CSS, como antes.
        # O piso de 90 deixa de fora o ruído do JPEG num fundo de padrão fino (pontilhado, retícula)
        topo = int(dd.max())
        if topo < 90:
            continue
        sel = dd >= int(topo * 0.6)
        if int(sel.sum()) < max(30, 0.01 * dd.size):
            continue
        px = F[ya:yb, xa:xb][sel]
        tx["cor_css"] = tx["cor"]
        tx["cor"] = [int(v) for v in np.median(px, axis=0)]
        tx["cor_medida"] = True
    return info


# ----------------------------------------------------------------------------- estilo de produção

def estilos_do_plano(cenas):
    """Os estilos pedidos no cenas.json ("estilo": "liquid-glass" ou uma lista) e a união do que eles
    permitem, lidos de motor/estilos.json. Sem a chave, None: nada é conferido (o plano é livre)."""
    pedido = cenas.get("estilo")
    if not pedido:
        return None
    nomes = [pedido] if isinstance(pedido, str) else list(pedido)
    tabela = ler_json(AQUI / "estilos.json", {}) or {}
    todos = tabela.get("estilos", {})
    desconhecidos = [n for n in nomes if n not in todos]
    if desconhecidos:
        erro("estilo desconhecido no cenas.json: %s (os que existem: %s)"
             % (", ".join(desconhecidos), ", ".join(todos)), 1)
    sempre = tabela.get("sempre", {})
    uniao = {k: set(sempre.get(k, [])) for k in ("modos", "sobre", "transicoes")}
    precisa = set()
    for n in nomes:
        for k in uniao:
            uniao[k] |= set(todos[n].get(k, []))
        precisa |= set(todos[n].get("precisa", []))
    return {"nomes": nomes, "teto": max(float(todos[n].get("teto_transicoes_min", 8)) for n in nomes),
            "precisa": precisa, **uniao}


def conferir_estilo(cenas, pasta):
    """O que o plano usa fora do estilo escolhido. Não recusa (o criador pode querer a exceção): avisa,
    cena por cena, para o planejador trocar ou assumir."""
    e = estilos_do_plano(cenas)
    if e is None:
        return []
    avisos = []
    fora = lambda tipo, nome, onde: avisos.append(
        f"aviso de estilo: {onde} usa {tipo} \"{nome}\", que não está em {' + '.join(e['nomes'])}")
    for item in cenas.get("sobre") or []:
        if isinstance(item, dict) and item.get("tipo") not in e["sobre"]:
            fora("a sobreposição", item.get("tipo"), "o reel (sobre)")
    for c in cenas.get("cenas") or []:
        if not isinstance(c, dict):
            continue
        cid = c.get("id", "?")
        if c.get("modo") not in e["modos"]:
            fora("o modo", c.get("modo"), f"a cena {cid}")
        tr = (c.get("entrada") or {}).get("transicao") or "corte"
        if tr not in e["transicoes"]:
            fora("a transição", tr, f"a cena {cid}")
        for item in c.get("sobre") or []:
            if isinstance(item, dict) and item.get("tipo") not in e["sobre"]:
                fora("a sobreposição", item.get("tipo"), f"a cena {cid}")
    if "visao" in e["precisa"] and not (pasta / "visao").is_dir():
        avisos.append("aviso de estilo: o estilo tela-cortada pede a visão do corte; rode o visao.py antes "
                      "(e grave de frente, com a câmera parada)")
    if not avisos:
        avisos.append(f"estilo: {' + '.join(e['nomes'])} (o plano está dentro dele)")
    return avisos


# ----------------------------------------------------------------------------- principal

def ler_json(caminho, padrao=None, obrigatorio=False):
    if not caminho.is_file():
        if obrigatorio:
            erro(f"não achei {caminho}")
        return padrao
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        erro(f"{caminho.name} não é um JSON válido: {e}", 1)


def main():
    ap = argparse.ArgumentParser(description="Renderiza o reel inteiro a partir do cenas.json.")
    ap.add_argument("--projeto", required=True)
    ap.add_argument("--corte", required=True, help="o número do corte, ex.: 01")
    ap.add_argument("--previa", action="store_true", help="540x960 com som, para conferir rápido")
    ap.add_argument("--quadro", type=float, help="grava só o PNG deste instante")
    ap.add_argument("--saida", help="caminho do PNG do --quadro")
    ap.add_argument("--quadros", help="vários instantes de uma vez, separados por vírgula (ex.: 0.5,7.7,12): "
                    "grava um PNG de cada em <pasta do corte>/quadros/, sem render inteiro")
    ap.add_argument("--de", type=float, help="começo do trecho (com --ate)")
    ap.add_argument("--ate", type=float, help="fim do trecho")
    ap.add_argument("--amostras-contraste", type=int, default=15,
                    help="a cada quantos quadros grava um quadro sem texto (0 desliga)")
    args = ap.parse_args()

    if shutil.which("ffmpeg") is None:
        erro("ffmpeg não encontrado no PATH. Rode o instalar.sh na raiz do pacote.")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        erro("falta o playwright. Rode com o Python do pacote (.venv/bin/python) ou o instalar.sh.")

    projeto = Path(args.projeto)
    if not projeto.is_absolute():
        projeto = (Path.cwd() / projeto).resolve()
    corte = f"{int(args.corte):02d}"
    pasta = projeto / "materiais-de-trabalho" / f"corte-{corte}"
    if not pasta.is_dir():
        erro(f"não achei a pasta do corte {pasta}")

    cenas = ler_json(pasta / "cenas.json", obrigatorio=True)
    for aviso in conferir_estilo(cenas, pasta):
        fala("  " + aviso)
    # marca do projeto (materiais-de-trabalho/marca/tokens.json) vale mais que a do pacote: é o caso do
    # reel feito para outra marca (um cliente), sem mexer na marca/ de quem roda o pacote
    marca_projeto = projeto / "materiais-de-trabalho" / "marca" / "tokens.json"
    tokens = ler_json(marca_projeto) if marca_projeto.is_file() else ler_json(RAIZ / "marca" / "tokens.json")
    if marca_projeto.is_file():
        fala(f"  marca do projeto: {marca_projeto.relative_to(RAIZ)}")
    if tokens is None:
        erro("não achei marca/tokens.json. Rode o onboarding da marca (`/flow-reels:marca`) primeiro.")
    palavras = ler_json(pasta / "palavras-corte.json", {"palavras": []})
    # os tempos presos à palavra viram segundos, e o fiscal confere a câmera dos mundos (MOTOR.md 4.14)
    cenas, erros_ancora, n_ancoras = ancoras.resolver_ancoras(cenas, palavras, int(cenas.get("fps", 30)))
    erros_mundo, avisos_mundo = ancoras.conferir_mundos(cenas)
    if n_ancoras:
        fala(f"  {n_ancoras} tempo(s) preso(s) à palavra da fala")
    for a in avisos_mundo:
        fala("  aviso do mundo: " + a)
    if erros_ancora or erros_mundo:
        erro("o plano tem problema:\n  " + "\n  ".join(erros_ancora + erros_mundo), 1)
    rosto = ler_json(pasta / "rosto.json")
    setup = ler_json(RAIZ / "setup.json", {})
    zonas = dict(ZONAS_PADRAO, **(setup.get("zonas_seguras") or {}))

    fps = int(cenas.get("fps", 30))
    video_principal = pasta / ((cenas.get("fonte") or {}).get("video") or "fala.mp4")
    if not video_principal.is_file():
        erro(f"não achei o vídeo da fala {video_principal}. Rode o editar_fala.py antes.")
    fontes = {"principal": dict(extrair_quadros(video_principal, pasta / "quadros-fonte", fps), fps=fps)}
    for nome, rel in (cenas.get("videos") or {}).items():
        v = pasta / rel
        if not v.is_file():
            erro(f"o vídeo \"{nome}\" declarado em cenas.json não existe: {v}", 1)
        fontes[nome] = dict(extrair_quadros(v, pasta / f"quadros-{nome}", fps), fps=fps)

    duracao = float(cenas.get("duracao") or 0)
    if duracao <= 0:
        erro("cenas.json sem duracao", 1)
    total = int(round(duracao * fps))
    i0, i1 = 0, total
    if args.de is not None or args.ate is not None:
        i0 = max(0, int(round((args.de or 0) * fps)))
        i1 = min(total, int(round((args.ate if args.ate is not None else duracao) * fps)))

    # as emendas do editor de fala: o motor alterna o zoom do rosto em cada uma, para esconder o pulo
    edicao = {}
    if (pasta / "edicao.json").is_file():
        try:
            bruto = json.loads((pasta / "edicao.json").read_text(encoding="utf-8"))
            edicao = {"emendas": [float(e) for e in (bruto.get("emendas") or []) if isinstance(e, (int, float))]}
        except (ValueError, OSError):
            print("  aviso: edicao.json ilegível; as emendas ficam sem zoom alternado")

    # a visão do corte (visao.py), quando existe e é deste vídeo; sem ela, null e nada muda
    visao = carregar_visao(pasta, video_principal, fps, fontes["principal"]["total"])

    # 4.3: o pós no quadro inteiro (web/pos.js) e o acabamento global no ffmpeg (docs-4/pos.md). Sem as
    # duas chaves no plano, nada disto entra no caminho e o reel sai igual ao de antes
    com_pos = tem_pos(cenas)
    acab = acabamento_do_plano(cenas, pasta)
    if com_pos or acab:
        fala("  4.3: " + " · ".join(([f"pós no quadro inteiro"] if com_pos else []) +
                                    ([f"acabamento ({acab['resumo']})"] if acab else [])))

    injecao = "".join([
        f"window.CENAS={json.dumps(cenas, ensure_ascii=False)};",
        f"window.VISAO={json.dumps(visao, ensure_ascii=False, separators=(',', ':'))};",
        f"window.EDICAO={json.dumps(edicao)};",
        f"window.TOKENS={json.dumps(tokens, ensure_ascii=False)};",
        f"window.PALAVRAS={json.dumps(palavras, ensure_ascii=False)};",
        f"window.ROSTO={json.dumps(rosto)};",
        f"window.FONTES_VIDEO={json.dumps(fontes)};",
        f"window.ZONAS={json.dumps(zonas)};",
        f"window.BASE_CORTE={json.dumps(url_de(pasta) + '/')};",
    ])

    srv, porta = subir_servidor()
    url = f"http://127.0.0.1:{porta}{url_de(WEB / 'motor.html')}"
    escala = 0.5 if args.previa else 1.0
    console = []

    with sync_playwright() as p:
        try:
            nav = p.chromium.launch(args=args_do_navegador(cenas))
        except Exception as e:
            erro(f"o Chromium do Playwright não abriu ({e}). Rode: python -m playwright install chromium")
        pag = nav.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=escala)
        pag.on("console", lambda m: console.append(f"[{m.type}] {m.text}") if m.type in ("error", "warning") else None)
        pag.on("pageerror", lambda e: console.append(f"[erro de página] {e}"))
        pag.add_init_script(injecao)
        pag.goto(url)
        try:
            pag.wait_for_function("window.PRONTO === true || !!window.ERRO", timeout=120000)
        except Exception:
            erro("o motor não ficou pronto em 2 minutos. Mensagens do navegador:\n  " + "\n  ".join(console[-15:]), 1)
        falha = pag.evaluate("window.ERRO || null")
        if falha:
            print("\n  o motor recusou o plano:\n  " + falha.replace("\n", "\n  "), file=sys.stderr)
            for linha in console[-10:]:
                print("  " + linha, file=sys.stderr)
            sys.exit(1)

        pos = PassadaPos(pag) if com_pos else None

        ev = pag.evaluate("window.EVENTOS")
        # só o render inteiro escreve o eventos.json: a prévia de um quadro ou de um trecho não mexe no
        # que o audio.py e os gates leem
        if args.quadro is None and not args.quadros and not args.previa and args.de is None and args.ate is None:
            (pasta / "eventos.json").write_text(json.dumps(ev, ensure_ascii=False, indent=1), encoding="utf-8")

        if args.quadros:
            destino_q = pasta / "quadros"
            destino_q.mkdir(exist_ok=True)
            for bruto in args.quadros.split(","):
                t_q = float(bruto)
                pag.evaluate("t => window.Motor.render(t)", t_q)
                if pos:
                    pos.passar(t_q)
                arq_q = destino_q / f"quadro-{t_q:06.2f}.png"
                pag.screenshot(path=str(arq_q))
                if acab:
                    arq_q.write_bytes(acabar_imagem(arq_q.read_bytes(), acab))
                fala(f"  {t_q:6.2f} s  →  {arq_q}")
            pag.evaluate("window.Motor.fecharAvisos && window.Motor.fecharAvisos()")
            for a in avisos_do_console(console)[:20]:
                fala("    " + a)
            nav.close()
            return 0

        if args.quadro is not None:
            lay = pag.evaluate("t => window.Motor.render(t)", args.quadro)
            destino = Path(args.saida) if args.saida else pasta / f"quadro-{args.quadro:.2f}.png"
            if pos and pos.passar(args.quadro):
                fala("  pós neste quadro: " + json.dumps(pag.evaluate("t => window.Motor.Pos.ativos(t)", args.quadro),
                                                         ensure_ascii=False))
            pag.screenshot(path=str(destino))
            if acab:
                destino.write_bytes(acabar_imagem(destino.read_bytes(), acab))
            # o texto atrás de você que a pessoa esconde neste quadro (num quadro avulso o motor não mede
            # a duração: avisa do quadro)
            pag.evaluate("window.Motor.fecharAvisos && window.Motor.fecharAvisos()")
            fala(f"  quadro {args.quadro:.2f} s gravado em {destino}")
            fala("  " + json.dumps(lay, ensure_ascii=False))
            avisos_quadro = avisos_do_console(console)
            if avisos_quadro:
                fala("  avisos do motor (da montagem e deste quadro; os que dependem do render em sequência só saem nele):")
                for a in avisos_quadro[:20]:
                    fala("    " + a)
            nav.close()
            return 0

        trecho = args.de is not None or args.ate is not None
        if args.previa or trecho:
            nome_saida = "previa.mp4" if args.previa and not trecho else "previa-trecho.mp4"
            saida = pasta / nome_saida
            cmd = ["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
                   "-ss", f"{i0 / fps:.3f}", "-i", str(video_principal),
                   "-map", "0:v", "-map", "1:a?", "-vf", vf_video(acab), "-c:v", "libx264", "-preset", "veryfast",
                   "-crf", "22", *TAGS_COR, "-c:a", "aac", "-b:a", "160k", "-shortest",
                   "-movflags", "+faststart", str(saida)]
        else:
            saida = pasta / "video.mp4"
            cmd = ["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
                   "-vf", vf_video(acab), "-c:v", "libx264", "-preset", "medium", "-crf", "18", *TAGS_COR,
                   "-profile:v", "high", "-r", str(fps), "-movflags", "+faststart", str(saida)]
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

        medir = args.amostras_contraste > 0 and not args.previa and not trecho
        pasta_contraste = pasta / "contraste"
        if medir:
            if pasta_contraste.exists():
                shutil.rmtree(pasta_contraste)
            pasta_contraste.mkdir()
        layout_f = None if (args.previa or trecho) else open(pasta / "layout.jsonl", "w", encoding="utf-8")
        contraste_f = open(pasta_contraste / "contraste.jsonl", "w", encoding="utf-8") if medir else None

        fala(f"  renderizando {i1 - i0} quadros ({(i1 - i0) / fps:.1f} s) em {'540x960' if args.previa else '1080x1920'}...")
        t_ini = time.time()
        ultimo_aviso = t_ini
        custo_pos = {"com": [0, 0.0], "sem": [0, 0.0]}   # quadros e segundos, com e sem pós ativo
        try:
            for i in range(i0, i1):
                t = i / fps
                t_q = time.time()
                lay = pag.evaluate("t => window.Motor.render(t)", t)
                amostra = medir and (i % args.amostras_contraste == 0)
                info = pag.evaluate("window.Motor.textosInfo()") if amostra else None
                pos_aqui = pos.passar(t) if pos else False
                quadro = pag.screenshot(type="jpeg", quality=92)
                enc.stdin.write(quadro)
                if pos:
                    c = custo_pos["com" if pos_aqui else "sem"]
                    c[0] += 1
                    c[1] += time.time() - t_q
                if layout_f:
                    layout_f.write(json.dumps(lay, ensure_ascii=False) + "\n")
                if amostra and info and (pos or acab):
                    # o quadro sem texto passa pelo mesmo pós e pelo mesmo acabamento, e a cor de cada texto
                    # é medida no quadro final (medir_cores_finais): o gate mede o que se vê. O final vai em
                    # PNG (sem perda): o ruído do JPEG num fundo de padrão fino parecia letra
                    final = pag.screenshot()
                    pag.evaluate("t => window.Motor.render(t, {semTexto: true, layout: false})", t)
                    if pos:
                        pos.passar(t)
                    fundo = pag.screenshot()
                    if acab:
                        fundo = acabar_imagem(fundo, acab)
                        final = acabar_imagem(final, acab)
                    if pos_aqui or acab:
                        info = medir_cores_finais(info, final, fundo, lay.get("legenda") if lay else None, acab)
                    arq = f"f{i:06d}.png"
                    (pasta_contraste / arq).write_bytes(fundo)
                    contraste_f.write(json.dumps({"i": i, "t": round(t, 3), "arquivo": arq, "textos": info},
                                                 ensure_ascii=False) + "\n")
                elif amostra and info:
                    pag.evaluate("t => window.Motor.render(t, {semTexto: true, layout: false})", t)
                    arq = f"f{i:06d}.png"
                    pag.screenshot(path=str(pasta_contraste / arq))
                    contraste_f.write(json.dumps({"i": i, "t": round(t, 3), "arquivo": arq, "textos": info},
                                                 ensure_ascii=False) + "\n")
                agora = time.time()
                if agora - ultimo_aviso > 15:
                    feitos = i - i0 + 1
                    fala(f"    {feitos}/{i1 - i0} quadros  ·  {(agora - t_ini) / feitos * 1000:.0f} ms por quadro")
                    ultimo_aviso = agora
            # o motor avisa do texto atrás de você que a pessoa esconde quando a corrida acaba; a que
            # chega até o último quadro fecha aqui
            pag.evaluate("window.Motor.fecharAvisos && window.Motor.fecharAvisos()")
            # o modo mundo (MOTOR.md 4.14.7): o relatório para o gate e o quadro de cada chave de câmera e
            # de cada troca de superfície, em tamanho cheio (miniatura mente sobre enquadramento)
            if not args.previa and not trecho:
                gravar_mundo(pag, pasta, pos, acab)
        finally:
            enc.stdin.close()
            enc.wait()
            if layout_f:
                layout_f.close()
            if contraste_f:
                contraste_f.close()
            nav.close()
            srv.shutdown()

    dt = time.time() - t_ini
    n = max(1, i1 - i0)
    fala(f"  pronto: {saida}")
    fala(f"  {n} quadros em {dt:.0f} s  ·  {dt / n * 1000:.0f} ms por quadro  ·  "
         f"{dt / (n / fps):.1f} s de render por segundo de vídeo")
    if com_pos:
        c, s_ = custo_pos["com"], custo_pos["sem"]
        fala(f"  pós: {c[0]} quadros com pós a {c[1] / max(1, c[0]) * 1000:.0f} ms por quadro · "
             f"{s_[0]} sem pós a {s_[1] / max(1, s_[0]) * 1000:.0f} ms (render + passada + foto)")
    avisos = avisos_do_console(console)
    if avisos:
        fala("  avisos do motor:")
        for a in avisos[:30]:
            fala("    " + a)
        if len(avisos) > 30:
            fala(f"    ... e mais {len(avisos) - 30}")
    return 0 if enc.returncode == 0 else 1


def gravar_mundo(pag, pasta, pos, acab):
    """Escreve mundo.json e os quadros-chave em conferencia-mundo/, só quando o plano tem mundo."""
    rel = pag.evaluate("window.Motor.mundoRelatorio ? window.Motor.mundoRelatorio() : null")
    arq = pasta / "mundo.json"
    if not rel:
        if arq.is_file():
            arq.unlink()
        return
    destino = pasta / "conferencia-mundo"
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir()
    for nome, m in rel.items():
        feitos = []
        for t in m.get("quadros_chave") or []:
            pag.evaluate("t => window.Motor.render(t)", t)
            if pos:
                pos.passar(t)
            png = destino / f"{nome}-{t:06.2f}.png"
            pag.screenshot(path=str(png))
            if acab:
                png.write_bytes(acabar_imagem(png.read_bytes(), acab))
            feitos.append(png.name)
        m["quadros_chave_arquivos"] = feitos
    arq.write_text(json.dumps(rel, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(len(m.get("quadros_chave") or []) for m in rel.values())
    fala(f"  mundo: {total} quadro(s)-chave em {destino} (olhe cada um em tamanho cheio) e o relatório em {arq.name}")


def avisos_do_console(console):
    """Erros e avisos do navegador que interessam a quem fez o plano: as peças avisam por console.error
    ou console.warn (posição que não coube, palavra não achada, valor inválido)."""
    vistos, out = set(), []
    for c in console:
        if ("LOGO AUSENTE" in c or "não carregou" in c or "erro" in c.lower() or c.startswith("[warning]")
                or "aviso" in c.lower()) and c not in vistos:
            vistos.add(c)
            out.append(c)
    return out


if __name__ == "__main__":
    sys.exit(main())
