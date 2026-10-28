#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
medir_fala.py  ·  quantas palavras por segundo a pessoa fala nos reels

Lê o palavras.json de cada projeto já transcrito e mede a velocidade de fala,
para o roteiro sair com o número de palavras certo para 40 a 50 segundos. Usa
só vídeos curtos (até 2 minutos), porque aula longa tem pausa de tela e puxa a
média para baixo.

Uso:

    flow-reels tendencias/medir_fala                 mede e imprime a tabela de tamanhos
    flow-reels tendencias/medir_fala --json          só o número, para outro script ler
"""

import argparse
import json
import statistics
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RAIZ = fabrica.raiz()
PADRAO = 3.7  # medido nos primeiros reels do pacote


def main():
    ap = argparse.ArgumentParser(description="Mede a velocidade de fala nos reels já transcritos.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    medidas = []
    for arq in sorted((RAIZ / "projetos").glob("*/materiais-de-trabalho/transcricao/palavras.json")):
        try:
            palavras = json.loads(arq.read_text(encoding="utf-8"))["palavras"]
        except (json.JSONDecodeError, KeyError, OSError):
            continue
        if len(palavras) < 30:
            continue
        dur = palavras[-1]["fim"] - palavras[0]["inicio"]
        if 0 < dur <= 120:
            medidas.append((arq.parts[-4], len(palavras) / dur))

    taxa = statistics.median([m[1] for m in medidas]) if medidas else PADRAO

    if args.json:
        print(json.dumps({"palavras_por_segundo": round(taxa, 2), "videos": len(medidas)}))
        return 0

    print("")
    if medidas:
        for nome, t in medidas:
            print("  %-32s %.2f palavras/s" % (nome, t))
        print("")
        print("  mediana: %.2f palavras por segundo, em %d vídeos curtos" % (taxa, len(medidas)))
    else:
        print("  nenhum vídeo curto transcrito ainda; usando o padrão de %.1f palavras/s" % PADRAO)
    print("")
    for s in (40, 45, 50):
        print("  %d s  ->  cerca de %d palavras" % (s, round(s * taxa)))
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
