#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
As duas leituras do video inteiro, antes de procurar qualquer trecho.

Leitura 1: quanto a fala se apoia em palavras que apontam para fora dela
mesma (aqui, isso, esse, ele, la). Ela prediz quanto o video rende em
trecho que se sustenta sozinho, e por isso e dita antes de prometer volume.

Leitura 2: onde estao as pausas mais longas. Elas nao servem so para evitar
cortar em cima; elas sao os melhores pontos de entrada e de saida, porque
quem fala pausa onde termina uma ideia.

A lei das duas leituras esta em referencias/LEVANTAMENTO.md, secao 1.
Este script le so o palavras.json. Ele nao fecha ponto de corte: quem fecha
ponto e a energia do audio, em energia_audio.py, pela razao escrita em
referencias/CORTE-LIMPO.md, secao 2.

Depende apenas da biblioteca padrao.
"""

import json
import os
import sys
import unicodedata

PAUSAS_PADRAO = 40      # quantas pausas o mapa lista por padrao
CONTEXTO_PALAVRAS = 4   # quantas palavras mostrar de cada lado da pausa

# As palavras que apontam para fora da fala. A lista e uma medida aproximada,
# de proposito: o que interessa e a ordem de grandeza e a comparacao entre
# videos do mesmo canal, nao um veredicto por palavra.
APONTAM = {
    "aqui", "ali", "la", "ai",
    "isso", "isto", "aquilo",
    "esse", "essa", "esses", "essas",
    "este", "esta", "estes", "estas",
    "aquele", "aquela", "aqueles", "aquelas",
    "ele", "ela", "eles", "elas",
    "dele", "dela", "deles", "delas",
    "nisso", "nesse", "nessa", "nesses", "nessas",
    "disso", "desse", "dessa", "desses", "dessas",
    "daqui", "dali", "dai",
    "assim",
}

FIM_DE_FRASE = (".", "!", "?", "...")

AJUDA = """
leitura_do_video.py: as duas leituras do video inteiro

Uso:
    flow-reels planejar/leitura_do_video <palavras.json ou pasta do video> [opcoes]

Exemplo:
    flow-reels planejar/leitura_do_video projetos/meu-video

Opcoes:
    --pausas N     quantas pausas o mapa lista (padrao 40)
    --minimo MS    so lista pausa a partir desta duracao, em milissegundos
    --json         imprime o resultado em JSON, sem as tabelas
    --ajuda        mostra este texto

O que a saida mostra:
    LEITURA 1, quanto a fala aponta para fora de si mesma, com a taxa por
    100 palavras, a fracao de frases atingidas e as palavras mais usadas.
    LEITURA 2, as pausas mais longas do video, da maior para a menor, com a
    palavra que fecha antes e a que abre depois de cada uma.
"""


def erro(mensagem):
    print("")
    print("Erro: " + mensagem)
    print("")
    print("Rode com --ajuda para ver o uso.")
    sys.exit(1)


def ler_argumentos(argumentos):
    """Le a linha de comando na mao, para toda mensagem sair em portugues."""
    opcoes = {
        "caminho": None,
        "pausas": PAUSAS_PADRAO,
        "minimo": None,
        "json": False,
    }

    esperando = None
    for item in argumentos:
        if esperando is not None:
            try:
                valor = float(item.replace(",", "."))
            except ValueError:
                erro("a opcao " + esperando + " espera um numero, e veio '" + item + "'.")
            if esperando == "--pausas":
                opcoes["pausas"] = int(valor)
            elif esperando == "--minimo":
                opcoes["minimo"] = valor
            esperando = None
            continue

        if item in ("--ajuda", "-h", "--help"):
            print(AJUDA)
            sys.exit(0)
        elif item == "--json":
            opcoes["json"] = True
        elif item in ("--pausas", "--minimo"):
            esperando = item
        elif item.startswith("--"):
            erro("opcao desconhecida: " + item)
        elif opcoes["caminho"] is None:
            opcoes["caminho"] = item
        else:
            erro("nao entendi o argumento '" + item + "'.")

    if esperando is not None:
        erro("a opcao " + esperando + " ficou sem valor.")
    if opcoes["caminho"] is None:
        erro("falta o caminho do palavras.json ou da pasta do video.")

    return opcoes


def achar_palavras(pedido):
    """Resolve o caminho do palavras.json, aceitando tambem a pasta do video."""
    if os.path.isfile(pedido):
        return pedido
    base = pedido if os.path.isdir(pedido) else os.path.dirname(os.path.abspath(pedido))
    tentativas = [
        os.path.join(base, "materiais-de-trabalho", "transcricao", "palavras.json"),
        os.path.join(base, "transcricao", "palavras.json"),
        os.path.join(base, "palavras.json"),
    ]
    for tentativa in tentativas:
        if os.path.isfile(tentativa):
            return tentativa
    erro(
        "nao achei o palavras.json a partir de '" + pedido + "'.\n"
        "       Ele e escrito pela skill transcrever, em\n"
        "       projetos/<video>/materiais-de-trabalho/transcricao/palavras.json"
    )


def carregar(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except ValueError:
        erro("o arquivo '" + caminho + "' nao e um JSON valido.")
    except OSError as falha:
        erro("nao consegui abrir '" + caminho + "': " + str(falha))

    palavras = dados.get("palavras") if isinstance(dados, dict) else None
    if not palavras:
        erro(
            "o arquivo '" + caminho + "' nao tem a lista 'palavras'.\n"
            "       O formato do contrato esta na SKILL.md do `/flow-reels:planejar`."
        )
    return palavras, (dados.get("meta") or {})


def simplificar(texto):
    """Tira acento, pontuacao e caixa, para comparar palavra com palavra."""
    sem_acento = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return "".join(c for c in sem_acento.lower() if c.isalnum())


def leitura_um(palavras):
    """Quanto a fala se apoia em palavra que aponta para fora dela mesma."""
    contagem = {}
    total_apontam = 0
    frases = 0
    frases_atingidas = 0
    frase_tem = False
    frase_viva = False

    for palavra in palavras:
        texto = palavra.get("texto", "")
        limpa = simplificar(texto)
        if limpa:
            frase_viva = True
        if limpa in APONTAM:
            total_apontam += 1
            contagem[limpa] = contagem.get(limpa, 0) + 1
            frase_tem = True
        if texto.strip().endswith(FIM_DE_FRASE) and frase_viva:
            frases += 1
            if frase_tem:
                frases_atingidas += 1
            frase_tem = False
            frase_viva = False

    if frase_viva:
        frases += 1
        if frase_tem:
            frases_atingidas += 1

    total = len(palavras)
    mais_usadas = sorted(contagem.items(), key=lambda par: (-par[1], par[0]))

    return {
        "palavras": total,
        "apontam": total_apontam,
        "por_100_palavras": round(100.0 * total_apontam / total, 1) if total else 0.0,
        "frases": frases,
        "frases_atingidas": frases_atingidas,
        "fracao_das_frases": round(100.0 * frases_atingidas / frases, 0) if frases else 0.0,
        "mais_usadas": mais_usadas,
    }


def leitura_dois(palavras, quantas, minimo_ms):
    """As pausas mais longas, da maior para a menor."""
    pausas = []
    for indice in range(len(palavras) - 1):
        atual = palavras[indice]
        proxima = palavras[indice + 1]
        try:
            fim = float(atual["fim"])
            inicio = float(proxima["inicio"])
        except (KeyError, TypeError, ValueError):
            continue
        duracao = inicio - fim
        if duracao <= 0:
            continue
        if minimo_ms is not None and duracao * 1000.0 < minimo_ms:
            continue
        antes = palavras[max(0, indice - CONTEXTO_PALAVRAS + 1):indice + 1]
        depois = palavras[indice + 1:indice + 1 + CONTEXTO_PALAVRAS]
        pausas.append({
            "comeca": round(fim, 2),
            "termina": round(inicio, 2),
            "duracao": round(duracao, 2),
            "antes": " ".join(p.get("texto", "") for p in antes),
            "depois": " ".join(p.get("texto", "") for p in depois),
        })

    pausas.sort(key=lambda p: -p["duracao"])
    return pausas[:quantas]


def relogio(segundos):
    minutos = int(segundos // 60)
    resto = segundos - minutos * 60
    return "%02d:%05.2f" % (minutos, resto)


def imprimir(uma, duas, caminho, meta):
    print("")
    print("Duas leituras de " + caminho)
    if meta.get("alinhado") is False:
        print("")
        print("  ATENCAO: meta.alinhado e false. Os tempos sao por trecho, nao por")
        print("  palavra, e o mapa de pausas abaixo vale so como regiao aproximada.")

    print("")
    print("LEITURA 1: para onde a fala aponta")
    print("  palavras faladas ................... %d" % uma["palavras"])
    print("  palavras que apontam para fora ..... %d" % uma["apontam"])
    print("  a cada 100 palavras faladas ........ %.1f" % uma["por_100_palavras"])
    print("  frases com pelo menos uma .......... %d de %d (%d%%)"
          % (uma["frases_atingidas"], uma["frases"], uma["fracao_das_frases"]))
    if uma["mais_usadas"]:
        principais = ", ".join(
            "%s %d" % (palavra, vezes) for palavra, vezes in uma["mais_usadas"][:8]
        )
        print("  as mais usadas ..................... " + principais)
    print("")
    print("  Este numero e dito antes de prometer volume. Quanto mais alto, menos")
    print("  o video rende trecho que se sustenta como afirmacao isolada, e mais o")
    print("  material puxa para o formato trajeto (referencias/FORMATOS.md).")

    print("")
    print("LEITURA 2: as pausas mais longas, da maior para a menor")
    if not duas:
        print("  nenhuma pausa encontrada com os limites pedidos.")
    else:
        print("")
        print("     comeca      termina    duracao   ...fecha antes  |  abre depois...")
        for pausa in duas:
            print("  %s  %s  %6.2f s   %-28s | %s" % (
                relogio(pausa["comeca"]),
                relogio(pausa["termina"]),
                pausa["duracao"],
                pausa["antes"][-28:],
                pausa["depois"][:36],
            ))
        print("")
        print("  Sao os melhores candidatos a ponto de entrada e de saida: quem fala")
        print("  pausa onde termina uma ideia. O ponto so fecha depois de conferido")
        print("  no audio com energia_audio.py, porque o tempo da palavra e estimativa.")
    print("")


def principal():
    opcoes = ler_argumentos(sys.argv[1:])
    caminho = achar_palavras(opcoes["caminho"])
    palavras, meta = carregar(caminho)

    uma = leitura_um(palavras)
    duas = leitura_dois(palavras, opcoes["pausas"], opcoes["minimo"])

    if opcoes["json"]:
        print(json.dumps(
            {"arquivo": caminho, "leitura_1": uma, "leitura_2": duas},
            ensure_ascii=False, indent=2,
        ))
        return

    imprimir(uma, duas, caminho, meta)


if __name__ == "__main__":
    principal()
