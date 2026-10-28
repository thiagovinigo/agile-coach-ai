# -*- coding: utf-8 -*-
"""O som do reel narrado e o arquivo de entrega.

O que entra no mix (os numeros e o porque estao em referencias/MIXAGEM.md):

  voz      construcao/voz.wav, inteira, sem compressor e sem acelerar
  som      construcao/som.wav, os trechos que tocam com o proprio som, nivelados com a voz
  leito    marca/audio/leito.mp3, a musica de fundo: sobe no titulo da abertura, fica
           perto de -23 dB debaixo da voz (com o abaixamento automatico quando ela fala),
           some quase toda debaixo dos trechos com som e desce no ultimo 1,5 s
  efeitos  marca/audio/sfx/<tipo>.mp3, nos eventos de construcao/eventos.json, baixos,
           com no minimo 0,22 s entre dois efeitos do mesmo tipo

Sem leito ou sem efeitos (a pessoa sem chave ou sem credito na ElevenLabs), o reel sai
so com a voz, e o script diz isso. Para gerar o leito e os efeitos uma vez:
flow-reels narrado/gerar_audio

Volume final: mede o loudness integrado com o ebur128, aplica um ganho so ate -14 LUFS e
um limitador por cima; confere o arquivo pronto e corrige uma vez se ficou fora de
0,3 LU. Audio AAC 192k, video copiado como veio (H.264, SAR 1:1), +faststart.

Uso:

    flow-reels narrado/mixar --projeto projetos/x --narrado 01
    flow-reels narrado/mixar --projeto projetos/x --narrado 01 --sem-leito --sem-efeitos

Saida padrao: projetos/<nome>/narrado-NN/narrado-NN.mp4, sozinho na pasta.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402

SR = cm.SR
ALVO_LUFS = -14.0

# tipo -> (arquivo em sfx/, ganho em dB depois de normalizar o pico em -1 dBFS, deslocamento s, passa-baixa Hz)
EFEITOS = {
    "whoosh": ("whoosh.mp3", -25, -0.10, 6000),
    "pop": ("pop.mp3", -28, 0.0, 5000),
    "clique": ("clique.mp3", -27, 0.0, 4500),
    "alternar": ("alternar.mp3", -27, 0.0, 4500),
    "varredura": ("varredura.mp3", -28, 0.0, 6000),
    "assentar": ("assentar.mp3", -25, 0.0, 3500),
    "digitar": ("digitar.mp3", -27, 0.0, 5000),
    "enviar": ("enviar.mp3", -24, 0.0, 6000),
}
INTERVALO_MINIMO = 0.22

LEITO_TITULO = -13.0
LEITO_VOZ = -20.0          # com o abaixamento de 30% quando a voz fala, fica perto de -23 dB
ABAIXAMENTO = 0.30
LEITO_SOM = -31.0
SAIDA_FINAL = 1.5


def media_movel(x, k):
    k = max(1, int(k))
    c = np.cumsum(np.pad(x.astype(np.float64), (k // 2 + 1, k - k // 2)))
    return ((c[k:] - c[:-k]) / k)[:len(x)].astype(np.float32)


def rms_ativo(x):
    e = np.sqrt(media_movel(x ** 2, int(0.05 * SR)))
    on = e > 0.02
    return float(np.sqrt((x[on] ** 2).mean())) if on.any() else 1e-6


def caber(x, n):
    return np.pad(x, (0, max(0, n - len(x))))[:n]


def montar_leito(caminho, n):
    leito = cm.carregar_audio(caminho)
    if len(leito) == 0:
        return None
    if len(leito) < n:
        # repete com uma emenda de meio segundo, para o leito cobrir o reel inteiro
        emenda = int(0.5 * SR)
        partes = [leito]
        total = len(leito)
        while total < n:
            prox = leito.copy()
            k = min(emenda, len(prox) // 2, len(partes[-1]) // 2)
            if k:
                partes[-1] = partes[-1].copy()
                partes[-1][-k:] *= np.linspace(1, 0, k)
                prox[:k] *= np.linspace(0, 1, k)
            partes.append(prox)
            total += len(prox)
        leito = np.concatenate(partes)
    return leito[:n]


def mixar(cam, op):
    tl = cm.ler_json(cam.linha)
    plano = cm.ler_json(cam.plano) if cam.plano.is_file() else {}
    entrada = Path(op.entrada) if op.entrada else cam.legendado
    if not entrada.is_file():
        cm.erro("nao achei %s. Rode o legenda_narrado.py antes." % entrada)
    dur = cm.duracao(entrada)
    n = int(dur * SR)
    voz = caber(cm.carregar_audio(cam.construcao / "voz.wav"), n)
    som = caber(cm.carregar_audio(cam.construcao / "som.wav"), n) if (cam.construcao / "som.wav").is_file() else np.zeros(n, np.float32)
    if np.abs(som).max() > 0:
        som *= rms_ativo(voz) / rms_ativo(som) * 0.95
    t = np.arange(n) / float(SR)
    em_som = np.zeros(n, bool)
    for s in tl["segmentos"]:
        if s["tipo"] == "som":
            em_som[int(s["t0"] * SR):int(s["t1"] * SR)] = True

    pasta_audio = cm.pasta_de_audio(op.audio)
    faltou = []
    leito = None
    if not op.sem_leito:
        arq = cm.arquivo_de_leito(pasta_audio)
        if arq is not None:
            leito = montar_leito(arq, n)
            if arq.parent != pasta_audio:
                cm.fala("leito: %s, do pacote (sem marca/audio/leito.mp3)" % arq.name)
        else:
            faltou.append("leito (%s)" % (pasta_audio / "leito.mp3"))
    if leito is not None:
        fim_titulo = float((plano.get("abertura") or {}).get("fim", 4.0))
        g = np.where(t < fim_titulo, LEITO_TITULO, LEITO_VOZ).astype(np.float32)
        g[em_som] = LEITO_SOM
        final = t > dur - SAIDA_FINAL
        g[final] -= 20 * ((t[final] - (dur - SAIDA_FINAL)) / SAIDA_FINAL)
        k = int(0.25 * SR)
        g = media_movel(np.pad(g, (k, k), mode="edge"), k)[k:-k]
        fala = media_movel(np.clip(media_movel(np.abs(voz), int(0.05 * SR)) / 0.02, 0, 1), k)
        leito = leito * (10 ** (g / 20) * (1 - ABAIXAMENTO * fala)).astype(np.float32)
    else:
        leito = np.zeros(n, np.float32)

    fx = np.zeros(n + SR * 2, np.float32)
    usados = 0
    if not op.sem_efeitos:
        eventos = cm.ler_json(cam.eventos) if cam.eventos.is_file() else []
        cache, ultimo, ausentes = {}, {}, set()
        for e in sorted(eventos, key=lambda e: e["t"]):
            tipo = e.get("tipo")
            if tipo not in EFEITOS:
                continue
            if e["t"] - ultimo.get(tipo, -9) < INTERVALO_MINIMO:
                continue
            arquivo, db, desloc, hz = EFEITOS[tipo]
            caminho = cm.arquivo_de_efeito(pasta_audio, arquivo)
            if caminho is None:
                ausentes.add(arquivo)
                continue
            ultimo[tipo] = e["t"]
            if arquivo not in cache:
                s = cm.carregar_audio(caminho, filtro="lowpass=f=%d,lowpass=f=%d" % (hz, hz))
                if len(s) == 0:
                    ausentes.add(arquivo)
                    continue
                s = s / max(1e-6, float(np.abs(s).max())) * 10 ** (-1 / 20.0)
                a = int(0.01 * SR)
                s[:a] *= np.linspace(0, 1, a)
                cache[arquivo] = s
            i = max(0, int((e["t"] + desloc) * SR))
            ganho = db - (7 if i < n and em_som[i] else 0)
            s = cache[arquivo] * 10 ** (ganho / 20.0)
            if tipo == "digitar" and e.get("fim"):
                corte = int((float(e["fim"]) - e["t"]) * SR)
                s = s[:max(1, corte)].copy()
                f2 = min(len(s), int(0.06 * SR))
                s[-f2:] *= np.linspace(1, 0, f2)
            fx[i:i + len(s)] += s[:max(0, len(fx) - i)]
            usados += 1
        if ausentes:
            faltou.append("efeitos (%s)" % ", ".join(sorted(ausentes)))

    mix = voz + som + leito + fx[:n]
    pico = float(np.abs(mix).max()) if n else 0
    if pico > 0.98:
        mix *= 0.98 / pico
    wav = cam.construcao / "mix.wav"
    cm.gravar_wav(wav, mix)
    medido = cm.medir_loudness(wav)
    if medido is None:
        cm.erro("nao consegui medir o loudness do mix.")

    saida = Path(op.saida) if op.saida else cam.entrega
    saida.parent.mkdir(parents=True, exist_ok=True)
    ganho = ALVO_LUFS - medido
    for tentativa in range(3):
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(entrada), "-i", str(wav),
               "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
               "-af", "volume=%.2fdB,alimiter=limit=0.84:attack=3:release=60:level=disabled" % ganho,
               "-ar", "48000", "-ac", "2", "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", "-shortest", str(saida)]
        r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        if r.returncode != 0:
            cm.erro("o ffmpeg nao fechou a entrega:\n" + "\n".join(r.stderr.splitlines()[-8:]))
        final = cm.medir_loudness(saida)
        if final is None or abs(final - ALVO_LUFS) <= 0.3:
            break
        ganho += ALVO_LUFS - final
    cm.fala("mix: %.1f LUFS antes, %s LUFS na entrega, %d efeitos." %
            (medido, "%.1f" % final if final is not None else "?", usados))
    if faltou:
        cm.fala("o reel saiu sem: %s. Para ter leito e efeitos da sua voz de marca, rode uma vez "
                "flow-reels narrado/gerar_audio (gasta credito da ElevenLabs)." % "; ".join(faltou))
    cm.fala("entrega: %s" % saida)
    return 0


def principal(argv=None):
    an = cm.argumentos_de_reel(argparse.ArgumentParser(description="Mixa o som e fecha a entrega."))
    an.add_argument("--entrada", default=None, help="video legendado (padrao construcao/legendado.mp4)")
    an.add_argument("--saida", default=None, help="arquivo final (padrao narrado-NN/narrado-NN.mp4)")
    an.add_argument("--audio", default=None, help="pasta do leito e dos efeitos (padrao marca/audio)")
    an.add_argument("--sem-leito", action="store_true", help="nao usa a musica de fundo")
    an.add_argument("--sem-efeitos", action="store_true", help="nao usa os efeitos sonoros")
    op = an.parse_args(argv)
    cm.exigir_ffmpeg()
    cam = cm.Caminhos(op.projeto, op.narrado)
    if not cam.linha.is_file():
        cm.erro("falta construcao/linha_do_tempo.json.")
    return mixar(cam, op)


if __name__ == "__main__":
    sys.exit(principal())
