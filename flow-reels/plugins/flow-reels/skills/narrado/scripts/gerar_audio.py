# -*- coding: utf-8 -*-
"""Gera, uma vez, o leito musical e os efeitos sonoros do reel narrado, com a chave da
ElevenLabs da propria pessoa.

Os pedidos estao em dados/sons.json, cada um com a descricao em portugues e o prompt
que vai para a API. O resultado fica em marca/audio/, que e reaproveitado por todo reel
narrado depois, de qualquer video:

    marca/audio/leito.mp3
    marca/audio/sfx/whoosh.mp3, pop.mp3, clique.mp3, alternar.mp3, varredura.mp3,
                    assentar.mp3, digitar.mp3, enviar.mp3

O que ja existe nao e gerado de novo (cada geracao gasta credito). --forcar refaz.

Uso:

    flow-reels narrado/gerar_audio --listar
    flow-reels narrado/gerar_audio
    flow-reels narrado/gerar_audio --so leito
    flow-reels narrado/gerar_audio --so pop --so whoosh --forcar

Sem ELEVENLABS_API_KEY no .env, ou sem credito, ele diz o que faltou e para. O reel
continua saindo, so com a voz.

So usa a biblioteca padrao.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402

API_MUSICA = "https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128"
API_EFEITO = "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128"
AGENTE = "fabrica-de-cortes/1.0"
DADOS = cm.SKILL / "dados" / "sons.json"


def pedir(url, chave, corpo):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode("utf-8"), method="POST", headers={
        "xi-api-key": chave, "Content-Type": "application/json", "Accept": "audio/mpeg",
        "User-Agent": AGENTE})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.read(), None
    except urllib.error.HTTPError as e:
        texto = e.read().decode("utf-8", "replace")[:400]
        if e.code in (401, 403):
            return None, "a chave foi recusada (HTTP %d). %s" % (e.code, texto)
        if e.code in (402, 429) or "quota" in texto.lower() or "credit" in texto.lower():
            return None, "faltou credito ou o limite estourou (HTTP %d)." % e.code
        return None, "HTTP %d: %s" % (e.code, texto)
    except urllib.error.URLError as e:
        return None, "sem conexao com a ElevenLabs (%s)." % e.reason


def principal(argv=None):
    an = argparse.ArgumentParser(description="Gera o leito musical e os efeitos do reel narrado.")
    an.add_argument("--listar", action="store_true", help="mostra o que existe e o que falta, sem gastar")
    an.add_argument("--so", action="append", default=None, help="gera so este item (leito ou nome do efeito)")
    an.add_argument("--forcar", action="store_true", help="gera de novo mesmo que o arquivo exista")
    an.add_argument("--audio", default=None, help="pasta de destino (padrao marca/audio)")
    op = an.parse_args(argv)

    dados = cm.sem_notas(cm.ler_json(DADOS))
    pasta = cm.pasta_de_audio(op.audio)
    itens = [("leito", pasta / dados["leito"]["arquivo"], dados["leito"])]
    itens += [(e["nome"], pasta / "sfx" / (e["nome"] + ".mp3"), e) for e in dados["efeitos"]]
    if op.so:
        nomes = set(op.so)
        desconhecidos = nomes - {n for n, _, _ in itens}
        if desconhecidos:
            cm.erro("nao conheco: %s. Itens: %s" % (", ".join(sorted(desconhecidos)),
                                                   ", ".join(n for n, _, _ in itens)))
        itens = [i for i in itens if i[0] in nomes]

    if op.listar:
        for nome, destino, d in itens:
            cm.fala("  %-10s %-8s %s" % (nome, "existe" if destino.is_file() else "falta", d["descricao"]))
        cm.fala("pasta: %s" % pasta)
        return 0

    pendentes = [i for i in itens if op.forcar or not i[1].is_file()]
    if not pendentes:
        cm.fala("leito e efeitos ja existem em %s. Nada a gerar." % pasta)
        return 0
    chave, _ = cm.exigir_elevenlabs(precisa_voz=False)

    feitos, falhas = 0, []
    for nome, destino, d in pendentes:
        destino.parent.mkdir(parents=True, exist_ok=True)
        if nome == "leito":
            cm.fala("gerando o leito (%d s)..." % (d["duracao_ms"] // 1000))
            audio, falha = pedir(API_MUSICA, chave, {"prompt": d["prompt"], "music_length_ms": int(d["duracao_ms"])})
        else:
            cm.fala("gerando o efeito %s..." % nome)
            audio, falha = pedir(API_EFEITO, chave, {"text": d["prompt"], "duration_seconds": float(d["duracao"]),
                                                     "prompt_influence": 0.35})
        if falha:
            falhas.append((nome, falha))
            cm.aviso("%s: %s" % (nome, falha))
            if "chave" in falha or "credito" in falha:
                break
            continue
        destino.write_bytes(audio)
        feitos += 1
        cm.fala("  %s" % destino)

    cm.fala("")
    cm.fala("%d arquivo(s) gerado(s) em %s." % (feitos, pasta))
    if falhas:
        cm.fala("Ficaram sem gerar: %s." % ", ".join(n for n, _ in falhas))
        cm.fala("O reel narrado continua funcionando: o que faltar sai so com a voz, e o mixar.py avisa.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(principal())
