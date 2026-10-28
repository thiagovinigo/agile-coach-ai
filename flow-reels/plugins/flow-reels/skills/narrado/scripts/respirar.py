# -*- coding: utf-8 -*-
"""Abre um respiro curto depois de cada frase da voz, sem acelerar nada.

A voz sintetica emenda uma frase na outra. Aqui o audio e cortado no meio do
silencio que ja existe depois de cada palavra que termina em . ? ! : ou reticencias,
e entra ali um silencio de 0,16 a 0,22 s. Os tempos das palavras andam junto.

Uso:

    flow-reels narrado/respirar --projeto projetos/x --narrado 01 --take a
    flow-reels narrado/respirar --projeto projetos/x --narrado 01 --take a --pausa 0.2

Le voz/voz-<take>.mp3 (ou .wav) e voz/palavras-<take>.json. Escreve
voz/voz-<take>-respiro.wav e voz/palavras-<take>-respiro.json. No tomadas.json, a
tomada de voz passa a ser "<take>-respiro".
"""

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402

FIM_DE_FRASE = ".?!:\u2026"


def termina_frase(texto):
    t = texto.rstrip("\"'\u201d)")
    return bool(t) and t[-1] in FIM_DE_FRASE


def respirar(amostras, palavras, pausa, sr=cm.SR):
    """Devolve (audio_novo, palavras_novas, numero_de_respiros)."""
    cortes = []
    for i, p in enumerate(palavras[:-1]):
        if termina_frase(p["texto"]):
            meio = (p["fim"] + palavras[i + 1]["inicio"]) / 2.0
            cortes.append((i, meio))
    pedacos, ultimo = [], 0
    silencio = np.zeros(int(round(pausa * sr)), np.float32)
    for _, t in cortes:
        s = int(round(t * sr))
        pedacos += [amostras[ultimo:s], silencio]
        ultimo = s
    pedacos.append(amostras[ultimo:])
    novas = []
    for i, p in enumerate(palavras):
        n = sum(1 for idx, _ in cortes if idx < i)
        novas.append({"texto": p["texto"], "inicio": round(p["inicio"] + n * pausa, 3),
                      "fim": round(p["fim"] + n * pausa, 3)})
    return np.concatenate(pedacos) if pedacos else amostras, novas, len(cortes)


def principal(argv=None):
    an = cm.argumentos_de_reel(argparse.ArgumentParser(
        description="Abre um respiro curto depois de cada frase da voz."))
    an.add_argument("--take", required=True, help="a tomada de voz, por exemplo a")
    an.add_argument("--pausa", type=float, default=0.18,
                    help="silencio acrescentado depois de cada frase, de 0.16 a 0.22 (padrao 0.18)")
    op = an.parse_args(argv)
    cm.exigir_ffmpeg()
    if not 0.16 <= op.pausa <= 0.22:
        cm.aviso("pausa fora de 0.16 a 0.22 s. Mais curta some, mais longa arrasta o reel.")

    cam = cm.Caminhos(op.projeto, op.narrado)
    audio = next((cam.voz / ("voz-%s.%s" % (op.take, e)) for e in ("wav", "mp3")
                  if (cam.voz / ("voz-%s.%s" % (op.take, e))).is_file()), None)
    if audio is None:
        cm.erro("nao achei voz/voz-%s.mp3 nem .wav em %s" % (op.take, cam.voz))
    palavras = cm.ler_palavras(cam.voz / ("palavras-%s.json" % op.take))
    if not palavras:
        cm.erro("o palavras-%s.json esta vazio." % op.take)

    amostras = cm.carregar_audio(audio)
    novo, novas, n = respirar(amostras, palavras, op.pausa)
    destino = cam.voz / ("voz-%s-respiro.wav" % op.take)
    cm.gravar_wav(destino, novo)
    cm.gravar_json(cam.voz / ("palavras-%s-respiro.json" % op.take),
                   {"palavras": novas, "meta": {"origem": op.take, "pausa": op.pausa, "respiros": n}})
    cm.fala("%d respiros de %.2f s. A fala agora termina em %.2f s." % (n, op.pausa, novas[-1]["fim"]))
    cm.fala("  %s" % destino)
    cm.fala('No tomadas.json, use "voz": {"take": "%s-respiro"}.' % op.take)
    return 0


if __name__ == "__main__":
    sys.exit(principal())
