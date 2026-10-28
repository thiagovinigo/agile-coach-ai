#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
buscar-trilha.py  ·  música livre para tocar por baixo da voz, com a licença conferida e o crédito anotado

Busca no Openverse (o buscador de mídia livre do WordPress, sem chave) só faixas em domínio público
(CC0 ou marca de domínio público), quase todas do Freesound. Baixa as candidatas, mede se cada uma
serve embaixo de fala e escreve o crédito no CREDITOS.md desta pasta. Quem escolhe a trilha do corte
continua sendo você, no cenas.json: o script só traz e mede.

O que ele mede (a seção "Que música funciona embaixo da voz" do LEIA.md, em número):
  duracao     mais longa que o reel, de preferência 60 s ou mais
  constancia  a variação do volume de curto prazo (LRA, em LU): abaixo de ~8 é energia constante;
              acima disso tem drop, pausa ou crescendo, que briga com o corte
  silencio    quanto da faixa é silêncio (buracos no meio aparecem como pausa na trilha)
  disputa     quanto da energia mora entre 1 e 4 kHz, a faixa da voz: quanto menor, melhor para fala
  nota        a soma dessas medidas, de 0 a 10. É triagem, não gosto: ouça antes de usar

Uso
---
    flow-reels componentes/buscar-trilha "lofi beat" "ambient music" --quantas 12
    flow-reels componentes/buscar-trilha --medir componentes/trilhas/calma-piano-01.mp3

Baixa em componentes/trilhas/_candidatas/ com o nome do clima que você der em --clima (padrão:
"busca"). Depois de ouvir, renomeie as boas para <clima>-<instrumento>-<nn>.mp3 na pasta de cima,
e a linha do CREDITOS.md acompanha o novo nome (o script corrige com --renomear antigo novo).
"""

import argparse
import datetime
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# o que se baixa e se escolhe vai para a pasta de trabalho (componentes/trilhas/), por cima das
# trilhas que o pacote traz; quem mantém o pacote passa --pacote para gravar no próprio plugin
AQUI = (Path(__file__).resolve().parent if "--pacote" in sys.argv
        else fabrica.raiz() / "componentes" / "trilhas")
CANDIDATAS = AQUI / "_candidatas"
CREDITOS = AQUI / "CREDITOS.md"
UA = {"User-Agent": "fabrica-de-cortes/3.0 (trilha livre para reels)"}

# tags que indicam música (entra) e tags que indicam que não é trilha de fundo (sai)
MUSICA = {"music", "loop", "beat", "beats", "lofi", "lo-fi", "hiphop", "hip-hop", "synth", "piano", "electronic",
          "electronica", "chill", "chillout", "downtempo", "house", "techno", "pad", "groove", "groovy",
          "instrumental", "soundtrack", "background-music", "background", "corporate", "cinematic", "synthwave",
          "ambient", "melody", "keys", "rhodes", "deep-house", "deephouse"}
FORA = {"field-recording", "nature", "voice", "vocal", "vocals", "speech", "singing", "rain", "birds", "bird", "wind",
        "traffic", "city", "foley", "sfx", "noise", "choir", "rap", "talk", "horror", "scary", "creepy", "talkbox",
        "8-bit", "8bit", "chiptune", "chip", "kids", "childrens"}


def erro(msg):
    print("  erro: " + msg)
    sys.exit(1)


def buscar(termo, pagina):
    u = "https://api.openverse.org/v1/audio/?" + urllib.parse.urlencode(
        {"q": termo, "license": "cc0,pdm", "page_size": 20, "page": pagina})
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r:
        return json.load(r)


def candidatas(termos, minimo, maximo):
    vistas = {}
    for termo in termos:
        for pagina in (1, 2):
            try:
                dados = buscar(termo, pagina)
            except Exception as e:  # rede instável: segue com o que já veio
                print(f"  aviso: a busca '{termo}' (página {pagina}) falhou: {e}")
                continue
            for r in dados.get("results", []):
                tags = {t["name"].lower() for t in (r.get("tags") or [])}
                dur = (r.get("duration") or 0) / 1000
                if r["id"] in vistas or not (minimo <= dur <= maximo):
                    continue
                if tags & FORA or not tags & MUSICA:
                    continue
                if r.get("license") not in ("cc0", "pdm"):
                    continue
                vistas[r["id"]] = r
            time.sleep(0.6)  # o Openverse limita quem pede rápido demais sem chave
    return list(vistas.values())


def medir(caminho):
    """Duração, LRA, silêncio e a fração da energia entre 1 e 4 kHz, tudo pelo ffmpeg e numpy."""
    import numpy as np
    sr = 22050
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(caminho), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(pcm, np.float32)
    if len(x) < sr:
        return None
    dur = len(x) / sr
    ebu = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(caminho), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", ebu)
    lra = re.findall(r"LRA:\s+([\d.]+) LU", ebu)
    janela = int(0.1 * sr)
    n = len(x) // janela
    rms = np.sqrt(np.mean(x[:n * janela].reshape(n, janela) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    silencio = float(np.mean(db < np.percentile(db, 90) - 35))
    passo = 4096
    esp = np.zeros(passo // 2 + 1)
    for i in range(0, len(x) - passo, passo * 4):
        esp += np.abs(np.fft.rfft(x[i:i + passo] * np.hanning(passo))) ** 2
    f = np.fft.rfftfreq(passo, 1 / sr)
    disputa = float(esp[(f >= 1000) & (f <= 4000)].sum() / max(esp[f >= 60].sum(), 1e-12))
    m = {"duracao": round(dur, 1), "lufs": float(lufs[-1]) if lufs else None,
         "lra": float(lra[-1]) if lra else None, "silencio": round(silencio, 3), "disputa": round(disputa, 3)}
    nota = 10.0
    nota -= 0 if dur >= 60 else 2 if dur >= 40 else 5
    nota -= max(0.0, (m["lra"] or 0) - 7) * 0.6
    nota -= silencio * 20
    nota -= max(0.0, disputa - 0.12) * 25
    m["nota"] = round(max(0.0, min(10.0, nota)), 1)
    return m


def nome_seguro(texto):
    t = re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")
    return t[:40] or "faixa"


def anotar_credito(arquivo, r):
    if not CREDITOS.is_file():
        CREDITOS.write_text("# Créditos das trilhas\n\nCada faixa desta pasta, de onde veio e sob que licença. "
                            "Se um aviso de direito autoral aparecer, é esta linha que resolve.\n\n"
                            "| arquivo | título | autor | página da faixa | licença | baixada em |\n"
                            "|---|---|---|---|---|---|\n", encoding="utf-8")
    linha = "| `%s` | %s | %s | %s | %s | %s |\n" % (
        arquivo, (r.get("title") or "").replace("|", "/"), (r.get("creator") or "").replace("|", "/"),
        r.get("foreign_landing_url") or "", "domínio público (CC0)" if r.get("license") == "cc0" else "domínio público",
        datetime.date.today().isoformat())
    texto = CREDITOS.read_text(encoding="utf-8")
    if "`%s`" % arquivo not in texto:
        CREDITOS.write_text(texto + linha, encoding="utf-8")


def renomear(antigo, novo):
    a = (AQUI / antigo) if not Path(antigo).is_absolute() else Path(antigo)
    if not a.is_file():
        a = CANDIDATAS / antigo
    if not a.is_file():
        erro(f"não achei {antigo}")
    destino = AQUI / novo
    a.rename(destino)
    if CREDITOS.is_file():
        CREDITOS.write_text(CREDITOS.read_text(encoding="utf-8").replace("`%s`" % a.relative_to(AQUI).as_posix(),
                                                                         "`%s`" % novo), encoding="utf-8")
    print(f"  ok  {a.name} -> {destino.relative_to(AQUI.parent.parent)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("termos", nargs="*")
    ap.add_argument("--pacote", action="store_true", help="grava no plugin, e não na pasta de trabalho")
    ap.add_argument("--quantas", type=int, default=10, help="quantas baixar, as mais longas e com tags de música")
    ap.add_argument("--min", type=float, default=45, help="duração mínima em s (padrão 45)")
    ap.add_argument("--max", type=float, default=420, help="duração máxima em s")
    ap.add_argument("--clima", default="busca", help="prefixo do nome dos arquivos baixados")
    ap.add_argument("--medir", help="só mede um arquivo que já está aqui")
    ap.add_argument("--renomear", nargs=2, metavar=("ANTIGO", "NOVO"))
    a = ap.parse_args()

    if a.medir:
        print(json.dumps(medir(a.medir), ensure_ascii=False))
        return
    if a.renomear:
        renomear(*a.renomear)
        return
    if not a.termos:
        erro("diga o que buscar, por exemplo: flow-reels componentes/buscar-trilha \"lofi beat\" \"ambient music\"")

    achadas = candidatas(a.termos, a.min, a.max)
    achadas.sort(key=lambda r: -(r.get("duration") or 0))
    print(f"  {len(achadas)} faixa(s) em domínio público com cara de música instrumental")
    CANDIDATAS.mkdir(exist_ok=True)
    feitas = []
    for r in achadas[:a.quantas]:
        url = r.get("url")
        if not url:
            continue
        ext = (r.get("filetype") or "mp3").lower().strip(".")
        nome = f"{a.clima}-{nome_seguro(r.get('title') or r['id'])}.{ext}"
        destino = CANDIDATAS / nome
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as resp:
                destino.write_bytes(resp.read())
        except Exception as e:
            print(f"  aviso: não baixou {r.get('title')}: {e}")
            continue
        m = medir(destino)
        if not m:
            print(f"  aviso: {nome} não é áudio que o ffmpeg leia; ficou de fora")
            destino.unlink()
            continue
        anotar_credito(f"_candidatas/{nome}", r)
        feitas.append((m["nota"], nome, m))
        time.sleep(0.4)
    for nota, nome, m in sorted(feitas, reverse=True):
        print(f"  {nota:4.1f}  {nome:60s} {m['duracao']:6.1f} s  LRA {m['lra']} LU  silêncio {m['silencio']:.0%}  "
              f"disputa {m['disputa']:.0%}")
    json.dump({n: m for _, n, m in feitas}, open(CANDIDATAS / "medidas.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
