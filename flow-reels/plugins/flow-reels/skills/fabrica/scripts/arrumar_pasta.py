#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arrumar_pasta.py  ·  poe uma pasta de video antiga na arvore de hoje

A arvore de hoje esta descrita em referencias/PASTA-DO-VIDEO.md, e a regra dela e
uma so: quem abre projetos/<video>/ ve os cortes prontos, a transcricao legivel,
os ganchos e a revisao. Todo o resto vai para materiais-de-trabalho/.

Este script move o que ficou no lugar antigo. Ele nao apaga nada, nao toca no MP4
de entrega e, por padrao, so MOSTRA o que pretende fazer:

    flow-reels fabrica/arrumar_pasta projetos/minha-aula            mostra o plano
    flow-reels fabrica/arrumar_pasta projetos/minha-aula --fazer    move de verdade

Se o destino de algum arquivo ja existir, ele avisa e nao mexe naquele arquivo.
Rodar duas vezes e seguro: na segunda ele diz que nao ha nada a fazer.
"""

import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

TRABALHO = "materiais-de-trabalho"

# O que continua a vista na pasta do video. Qualquer outra coisa solta na raiz
# e material de trabalho e desce um andar.
FICA_A_VISTA = {"transcricao.md", "GANCHOS.md", "revisao", TRABALHO}

# Os tres arquivos da transcricao e a resposta crua, com o nome que cada um passa
# a ter dentro de materiais-de-trabalho/transcricao/.
DA_TRANSCRICAO = {
    "palavras.json": "palavras.json",
    "audio16k.wav": "audio16k.wav",
    "_bruto_replicate.json": "bruto-replicate.json",
    "_bruto_local.json": "bruto-local.json",
    "bruto-replicate.json": "bruto-replicate.json",
    "bruto-local.json": "bruto-local.json",
}


def fala(texto=""):
    try:
        print(texto)
    except UnicodeEncodeError:
        print(texto.encode("ascii", "replace").decode("ascii"))


def achar_raiz():
    raiz = fabrica.raiz()
    return raiz if (raiz / "setup.json").is_file() else None


def resolver_projeto(raiz, pedido):
    alvo = Path(pedido)
    candidatos = [alvo, Path.cwd() / alvo]
    if raiz is not None:
        candidatos += [raiz / alvo, raiz / "projetos" / alvo]
    for caminho in candidatos:
        try:
            if caminho.is_dir():
                return caminho.resolve()
        except OSError:
            continue
    return None


def planejar(projeto):
    """Lista de (origem, destino). Nada e movido aqui."""
    plano = []
    trabalho = projeto / TRABALHO

    for item in sorted(projeto.iterdir()):
        nome = item.name
        if nome in FICA_A_VISTA:
            continue

        # o video de origem e a gravacao de tela
        if item.is_dir() and nome == "fonte":
            for arquivo in sorted(item.rglob("*")):
                if arquivo.is_file():
                    plano.append((arquivo, trabalho / "fonte" / arquivo.relative_to(item)))
            continue
        if item.is_file() and nome == "tela.mp4":
            plano.append((item, trabalho / "fonte" / "tela.mp4"))
            continue

        # a transcricao e a resposta crua
        if item.is_file() and nome in DA_TRANSCRICAO:
            plano.append((item, trabalho / "transcricao" / DA_TRANSCRICAO[nome]))
            continue

        # a pasta de um corte: sai tudo, menos o MP4 de entrega
        if item.is_dir() and nome.startswith("corte-"):
            entrega = nome + ".mp4"
            for filho in sorted(item.iterdir()):
                if filho.name == entrega:
                    continue
                plano.append((filho, trabalho / nome / filho.name))
            continue

        # o resto que estiver solto na raiz, menos o index.html do servidor,
        # que o proprio nova-revisao.py tira quando sobe a pagina
        if nome == "index.html":
            continue
        plano.append((item, trabalho / "logs" / nome))

    return plano


def mover(plano, projeto, fazer):
    movidos = 0
    parados = 0
    for origem, destino in plano:
        relativo_origem = origem.relative_to(projeto).as_posix()
        relativo_destino = destino.relative_to(projeto).as_posix()
        if destino.exists():
            fala("  parado   %s  (ja existe %s)" % (relativo_origem, relativo_destino))
            parados += 1
            continue
        fala("  %s  %s  ->  %s" % ("movendo " if fazer else "mover   ",
                                   relativo_origem, relativo_destino))
        if fazer:
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(origem), str(destino))
        movidos += 1
    return movidos, parados


def limpar_vazias(projeto):
    """Tira as pastas que ficaram vazias depois da mudanca."""
    for pasta in sorted(projeto.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if pasta.is_dir() and not any(pasta.iterdir()):
            try:
                pasta.rmdir()
            except OSError:
                pass


def main(argumentos):
    if not argumentos or argumentos[0] in ("-h", "--help", "ajuda"):
        fala("")
        fala("  arrumar_pasta.py | poe uma pasta de video antiga na arvore de hoje.")
        fala("")
        fala("  Uso:")
        fala("    flow-reels fabrica/arrumar_pasta <pasta do projeto>           mostra o plano")
        fala("    flow-reels fabrica/arrumar_pasta <pasta do projeto> --fazer   move de verdade")
        fala("")
        fala("  A arvore esta descrita em referencias/PASTA-DO-VIDEO.md.")
        fala("")
        return 0

    raiz = achar_raiz()
    projeto = resolver_projeto(raiz, argumentos[0])
    if projeto is None:
        fala("")
        fala("  Nao achei a pasta do projeto: %s" % argumentos[0])
        fala("")
        return 1

    fazer = "--fazer" in argumentos[1:]
    sobrou = [a for a in argumentos[1:] if a != "--fazer"]
    if sobrou:
        fala("")
        fala("  Nao reconheci: %s" % ", ".join(sobrou))
        fala("")
        return 1

    plano = planejar(projeto)
    fala("")
    fala("  Projeto: %s" % projeto)
    if not plano:
        fala("  Nada a mover. Esta pasta ja esta na arvore de hoje.")
        fala("")
        return 0

    movidos, parados = mover(plano, projeto, fazer)
    fala("")
    if fazer:
        limpar_vazias(projeto)
        fala("  Pronto: %d movidos, %d parados." % (movidos, parados))
        fala("  A pasta do corte ficou so com o MP4, e o resto esta em %s/." % TRABALHO)
    else:
        fala("  Isso foi so o plano: %d para mover, %d parados." % (movidos, parados))
        fala("  Rode de novo com --fazer para valer.")
    fala("")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main(sys.argv[1:]))
