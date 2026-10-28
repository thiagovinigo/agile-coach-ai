# -*- coding: utf-8 -*-
"""Teste de fumaca do reel narrado, inteiro, sem gastar um centavo da ElevenLabs.

Monta um projeto falso em projetos/_teste-narrado/ (a pasta projetos/ e ignorada pelo
git) e roda a cadeia inteira:

    filmagem sintetica (ffmpeg testsrc2 + uma "tela" quase branca)
    voz falsa (tons com envelope de fala) + palavras no MESMO formato do voz.py
    marca de teste (copia do marca/tokens.exemplo.json, sem tocar em marca/)
    respirar -> linha_do_tempo -> compor (quadros soltos e render) -> legenda
    -> mixar (sem leito) -> conferir -> revisao (sem servidor)

Uso:

    python skills/narrado/scripts/testes/fumaca.py
    python skills/narrado/scripts/testes/fumaca.py --manter   (nao apaga o projeto antes)
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
SCRIPTS = AQUI.parent
sys.path.insert(0, str(SCRIPTS))
import comum as cm  # noqa: E402

PROJETO = cm.RAIZ / "projetos" / "_teste-narrado"

ROTEIRO = (
    "Agora a sua planilha monta o relatório inteiro sozinha, e você só diz o que quer ver. "
    "Você escreve o pedido em uma frase, ela entende as colunas, cruza os dados e devolve o "
    "gráfico pronto em poucos segundos. Quer mudar alguma coisa? É só pedir de novo, do jeito "
    "que você falaria com alguém do seu lado, e o gráfico se ajusta na hora, sem fórmula "
    "nenhuma e sem abrir menu. Isso tira de você a parte chata do trabalho e deixa o que "
    "importa de verdade, que é olhar o número e decidir o próximo passo. Comenta RELATORIO "
    "que eu te mando o passo a passo completo para montar o seu primeiro relatório hoje."
)


def rodar(nome, args):
    cm.fala("")
    cm.fala("=== %s" % nome)
    t = time.time()
    r = subprocess.run([sys.executable] + [str(a) for a in args], cwd=str(cm.RAIZ))
    cm.fala("--- %s: codigo %d em %.1f s" % (nome, r.returncode, time.time() - t))
    return r.returncode


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + list(args), check=True)


def filmagem(fonte):
    fonte.mkdir(parents=True, exist_ok=True)
    ffmpeg("-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=30:d=30",
           "-f", "lavfi", "-i", "sine=f=330:d=30:sample_rate=48000",
           "-af", "volume='if(lt(mod(t,4),3),0.4,0)':eval=frame",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-shortest",
           str(fonte / "filme.mp4"))
    # uma "tela de produto" quase branca, com blocos cinza e um pedaco vivo andando
    ffmpeg("-f", "lavfi", "-i", "color=c=white:s=1920x1080:r=30:d=14",
           "-f", "lavfi", "-i", "testsrc2=s=480x270:r=30:d=14",
           "-filter_complex",
           "[0]drawbox=x=0:y=0:w=1920:h=90:c=0xE6E6E6:t=fill,"
           "drawbox=x=0:y=90:w=320:h=990:c=0xF2F2F2:t=fill,"
           "drawbox=x=420:y=180:w=900:h=110:c=0xD0D0D0:t=fill,"
           "drawbox=x=420:y=340:w=1200:h=40:c=0xE0E0E0:t=fill,"
           "drawbox=x=420:y=420:w=1000:h=40:c=0xE0E0E0:t=fill[f];"
           "[f][1]overlay=x='560+200*sin(t/2)':y=560",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(fonte / "tela.mp4"))
    fonte_txt = ImageFont.truetype(str(cm.fabrica.achar("marca/fontes/Quicksand-Bold.ttf")), 64)
    for i, cor in enumerate([(52, 120, 200), (40, 160, 110), (200, 90, 60)]):
        im = Image.new("RGB", (1200, 800), (248, 248, 248))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 1200, 90), fill=(230, 230, 230))
        for k in range(6):
            h = 120 + 70 * ((k * 3 + i) % 5)
            d.rectangle((120 + k * 170, 700 - h, 220 + k * 170, 700), fill=cor)
        d.text((120, 130), "Tela %d" % (i + 1), font=fonte_txt, fill=(40, 40, 40))
        im.save(fonte / ("carta-%d.png" % (i + 1)))


def voz_falsa(cam):
    """Tons com envelope, uma rajada por palavra, nos tempos de uma leitura natural."""
    sr = cm.SR
    palavras, t = [], 0.06
    for w in ROTEIRO.split():
        letras = sum(1 for c in w if c.isalnum())
        d = 0.10 + 0.052 * letras
        palavras.append({"texto": w, "inicio": round(t, 3), "fim": round(t + d, 3)})
        t += d + (0.30 if w[-1] in ".?!" else 0.16 if w[-1] in ",:" else 0.05)
    total = t + 0.3
    y = np.zeros(int(total * sr), np.float32)
    for i, p in enumerate(palavras):
        a, b = int(p["inicio"] * sr), int(p["fim"] * sr)
        tt = np.arange(b - a) / sr
        f0 = 140 + 25 * np.sin(i)
        onda = (0.5 * np.sin(2 * np.pi * f0 * tt) + 0.25 * np.sin(2 * np.pi * 3 * f0 * tt)
                + 0.12 * np.sin(2 * np.pi * 5.3 * f0 * tt))
        env = np.hanning(len(tt)) if len(tt) > 2 else np.ones(len(tt))
        y[a:b] += (0.45 * onda * env).astype(np.float32)
    cam.voz.mkdir(parents=True, exist_ok=True)
    wav = cam.voz / "_voz-teste.wav"
    cm.gravar_wav(wav, y)
    ffmpeg("-i", str(wav), "-c:a", "libmp3lame", "-b:a", "128k", str(cam.voz / "voz-teste.mp3"))
    wav.unlink()
    cm.gravar_json(cam.voz / "palavras-teste.json",
                   {"palavras": palavras, "meta": {"take": "teste", "modelo": "falso", "alinhamento": "alignment"}})
    return palavras


def tomadas(cam):
    return {
        "titulo": "Teste de fumaça: a planilha que monta o relatório",
        "palavra_chave": "RELATORIO",
        "fonte_padrao": "materiais-de-trabalho/fonte/filme.mp4",
        "credito_padrao": "Filme de lançamento · @exemplo",
        "voz": {"take": "teste-respiro"},
        "abertura": {"titulo": "Sua planilha agora monta o relatório sozinha", "destaque": "sozinha",
                     "ate": "sozinha,", "kicker": "NOVIDADE", "logo": "componentes/logos/notion.svg"},
        "tomadas": [
            {"id": "t01", "entrada": 2.0,
             "empurrao": {"alvo": [760, 340, 400, 400], "inicio": "relatório", "duracao": 1.2},
             "anel": {"caixa": [860, 440, 200, 200], "palavra": "diz"}},
            {"id": "t02", "inicio": "Você escreve", "fonte": "materiais-de-trabalho/fonte/tela.mp4", "entrada": 0.0,
             "credito": "Demonstração oficial · @exemplo",
             "empurrao": {"alvo": [420, 150, 900, 320], "inicio": "pedido"},
             "anel": {"caixa": [420, 180, 900, 110], "palavra": "frase,"}},
            {"id": "t03", "inicio": "Quer mudar", "entrada": 8.0, "recorte": [480, 0, 960, 1080],
             "transicao": "zoom", "empurrao": {"alvo": [900, 380, 300, 300], "inicio": "ajusta"}},
            {"id": "t04", "inicio": "Isso tira", "entrada": 1.0,
             "cartas": ["materiais-de-trabalho/fonte/carta-1.png", "materiais-de-trabalho/fonte/carta-2.png",
                        {"imagem": "materiais-de-trabalho/fonte/carta-3.png", "inicio": "importa"}]},
        ],
        "fechamento": {"inicio": "Comenta", "palavra": "RELATORIO", "item": "o passo a passo completo",
                       "item_palavra": "passo", "cauda": 1.4},
        "legenda": {"destaques": ["gráfico"]},
    }


def principal(argv=None):
    an = argparse.ArgumentParser(description="Teste de fumaca do reel narrado, sem API.")
    an.add_argument("--manter", action="store_true", help="nao apaga o projeto de teste antes")
    op = an.parse_args(argv)
    cm.exigir_ffmpeg()
    if PROJETO.exists() and not op.manter:
        shutil.rmtree(PROJETO)
    cam = cm.Caminhos(PROJETO, "01")
    cam.trabalho.mkdir(parents=True, exist_ok=True)
    if not (cam.fonte / "filme.mp4").is_file():
        cm.fala("gerando a filmagem sintetica...")
        filmagem(cam.fonte)
    marca = PROJETO / "materiais-de-trabalho" / "marca-teste"
    marca.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(cm.fabrica.achar("marca/tokens.exemplo.json"), marca / "tokens.json")
    cam.roteiro_tts.write_text(ROTEIRO + "\n", encoding="utf-8")
    palavras = voz_falsa(cam)
    cm.fala("roteiro com %d palavras, voz falsa com %.1f s" % (len(palavras), palavras[-1]["fim"]))
    cm.gravar_json(cam.tomadas, tomadas(cam))

    s = SCRIPTS
    p = ["--projeto", PROJETO, "--narrado", "01"]
    codigos = {}
    codigos["energia"] = rodar("energia da filmagem", [s / "linha_do_tempo.py", "--energia", cam.fonte / "filme.mp4"])
    codigos["folha"] = rodar("folha da fonte", [s / "conferir.py", "--folha-da-fonte", cam.fonte / "filme.mp4",
                                                "--saida", cam.conferencia / "folha-da-fonte.jpg", "--n", "8"])
    codigos["respirar"] = rodar("respirar", [s / "respirar.py"] + p + ["--take", "teste"])
    codigos["linha"] = rodar("linha do tempo", [s / "linha_do_tempo.py"] + p)
    codigos["quadros"] = rodar("quadros soltos", [s / "compor_narrado.py"] + p + ["--marca", marca, "--quadros",
                                                  "0.5", "2.4", "5.0", "9.0", "14.0", "22.0", "30.0", "40.0"])
    codigos["compor"] = rodar("compor", [s / "compor_narrado.py"] + p + ["--marca", marca])
    codigos["legenda"] = rodar("legenda", [s / "legenda_narrado.py"] + p + ["--marca", marca])
    codigos["mixar"] = rodar("mixar", [s / "mixar.py"] + p + ["--sem-leito"])
    codigos["conferir"] = rodar("conferir", [s / "conferir.py"] + p)
    codigos["revisao"] = rodar("revisao", [s / "revisao_narrado.py", PROJETO, "--sem-servidor"])
    cm.fala("")
    cm.fala("resumo: " + json.dumps(codigos))
    cm.fala("entrega: %s" % cam.entrega)
    return 0 if all(v == 0 for v in codigos.values()) else 1


if __name__ == "__main__":
    sys.exit(principal())
