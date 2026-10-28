#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Envelope de energia do audio em volta de pontos de corte candidatos.

Serve para uma coisa so: dizer se um ponto de corte cai em silencio de verdade
ou no meio de uma palavra. O tempo que vem da transcricao e uma estimativa e
costuma invadir a pausa. O audio e o juiz.

Depende apenas de wave (biblioteca padrao) e numpy.
"""

import json
import os
import sys
import wave

# Valores padrao. A definicao de cada um esta em referencias/CORTE-LIMPO.md.
JANELA_MS = 50.0        # tamanho da janela de medida
LIMIAR_FRACAO = 0.08    # fracao da fala plena abaixo da qual a janela e silencio
MIN_SILENCIO_MS = 150.0 # duracao minima para contar como silencio de verdade
RAIO_S = 0.60           # quanto tempo olhar para cada lado do candidato
LARGURA_BARRA = 28

AJUDA = """
energia_audio.py: envelope de energia em volta de pontos de corte

Uso:
    flow-reels planejar/energia_audio <audio16k.wav> <tempo> [tempo ...] [opcoes]

Exemplo:
    flow-reels planejar/energia_audio projetos/meu-video/materiais-de-trabalho/transcricao/audio16k.wav 412.8 421.6

Os tempos sao em segundos, com ponto decimal. Sao os pontos candidatos que
vieram da transcricao e que voce quer validar antes de fechar o corte.

Opcoes:
    --raio SEG           quanto olhar para cada lado do candidato (padrao 0.60)
    --janela MS          tamanho da janela de medida (padrao 50)
    --limiar FRACAO      fracao da fala plena que ainda conta como silencio (padrao 0.08)
    --min-silencio MS    duracao minima de um silencio de verdade (padrao 150)
    --json               imprime o resultado em JSON, sem as barras
    --ajuda              mostra este texto

O que a saida mostra:
    uma linha por janela de 50 ms, com a energia relativa a fala plena daquela
    gravacao, e a marca SILENCIO nas janelas que estao abaixo do limiar. No fim
    de cada candidato vem o silencio mais proximo e o ponto sugerido.
"""


def erro(mensagem):
    print("")
    print("Erro: " + mensagem)
    print("")
    print("Rode com --ajuda para ver o uso.")
    sys.exit(1)


def carregar_numpy():
    try:
        import numpy
    except ImportError:
        erro(
            "o numpy nao esta instalado neste Python.\n"
            "       Instale com:  pip install numpy"
        )
    return numpy


def ler_argumentos(argumentos):
    """Le a linha de comando na mao, para toda mensagem sair em portugues."""
    opcoes = {
        "caminho": None,
        "tempos": [],
        "raio": RAIO_S,
        "janela": JANELA_MS,
        "limiar": LIMIAR_FRACAO,
        "min_silencio": MIN_SILENCIO_MS,
        "json": False,
    }

    esperando = None
    for item in argumentos:
        if esperando is not None:
            try:
                valor = float(item.replace(",", "."))
            except ValueError:
                erro("a opcao " + esperando + " espera um numero, e veio '" + item + "'.")
            if esperando == "--raio":
                opcoes["raio"] = valor
            elif esperando == "--janela":
                opcoes["janela"] = valor
            elif esperando == "--limiar":
                opcoes["limiar"] = valor
            elif esperando == "--min-silencio":
                opcoes["min_silencio"] = valor
            esperando = None
            continue

        if item in ("--ajuda", "-h", "--help"):
            print(AJUDA)
            sys.exit(0)
        elif item == "--json":
            opcoes["json"] = True
        elif item in ("--raio", "--janela", "--limiar", "--min-silencio"):
            esperando = item
        elif item.startswith("--"):
            erro("opcao desconhecida: " + item)
        elif opcoes["caminho"] is None:
            opcoes["caminho"] = item
        else:
            try:
                opcoes["tempos"].append(float(item.replace(",", ".")))
            except ValueError:
                erro(
                    "'" + item + "' nao e um tempo em segundos.\n"
                    "       Os tempos vem depois do arquivo, assim: audio16k.wav 412.8 421.6"
                )

    if esperando is not None:
        erro("a opcao " + esperando + " ficou sem valor.")

    return opcoes


def achar_audio(pedido):
    """Resolve o caminho do audio, aceitando tambem a pasta do video.

    O audio16k.wav mora em <video>/materiais-de-trabalho/transcricao/, e ate a
    arvore mudar ele morava na raiz da pasta do video. Aqui valem as tres
    formas de pedir: o arquivo, a pasta do video, ou um caminho antigo.
    """
    if os.path.isfile(pedido):
        return pedido
    base = pedido if os.path.isdir(pedido) else os.path.dirname(os.path.abspath(pedido))
    tentativas = [
        os.path.join(base, "materiais-de-trabalho", "transcricao", "audio16k.wav"),
        os.path.join(base, "audio16k.wav"),
    ]
    for tentativa in tentativas:
        if os.path.isfile(tentativa):
            return tentativa
    return None


def ler_wav(caminho, numpy):
    achado = achar_audio(caminho)
    if achado is None:
        erro(
            "nao achei o arquivo: " + caminho + "\n"
            "       O audio16k.wav nasce em <video>/materiais-de-trabalho/transcricao/,\n"
            "       gravado pela skill transcrever."
        )
    caminho = achado

    try:
        arquivo = wave.open(caminho, "rb")
    except (wave.Error, EOFError):
        erro(
            "o arquivo '" + caminho + "' nao e um WAV que eu consiga abrir.\n"
            "       A skill transcrever grava o audio certo em\n"
            "       <video>/materiais-de-trabalho/transcricao/audio16k.wav."
        )
    except OSError as falha:
        erro("nao consegui abrir o arquivo: " + str(falha))

    with arquivo:
        canais = arquivo.getnchannels()
        largura = arquivo.getsampwidth()
        taxa = arquivo.getframerate()
        quadros = arquivo.getnframes()
        if quadros == 0:
            erro("o arquivo de audio esta vazio.")
        dados = arquivo.readframes(quadros)

    if largura == 1:
        amostras = numpy.frombuffer(dados, dtype=numpy.uint8).astype(numpy.float64)
        amostras = (amostras - 128.0) / 128.0
    elif largura == 2:
        amostras = numpy.frombuffer(dados, dtype="<i2").astype(numpy.float64) / 32768.0
    elif largura == 4:
        amostras = numpy.frombuffer(dados, dtype="<i4").astype(numpy.float64) / 2147483648.0
    else:
        erro(
            "este WAV tem " + str(largura * 8) + " bits por amostra, e eu leio 8, 16 ou 32.\n"
            "       Converta com:  ffmpeg -i entrada.wav -ac 1 -ar 16000 -c:a pcm_s16le audio16k.wav"
        )

    if canais > 1:
        sobra = len(amostras) % canais
        if sobra:
            amostras = amostras[:-sobra]
        amostras = amostras.reshape(-1, canais).mean(axis=1)

    return amostras, taxa


def medir_envelope(amostras, taxa, janela_ms, numpy):
    tamanho = max(1, int(round(taxa * janela_ms / 1000.0)))
    total = len(amostras) // tamanho
    if total == 0:
        erro("o audio e mais curto que uma janela de medida.")
    blocos = amostras[: total * tamanho].reshape(total, tamanho)
    rms = numpy.sqrt(numpy.mean(blocos * blocos, axis=1))
    return rms, tamanho / float(taxa)


def achar_silencios(rms, limiar_absoluto, minimo_janelas):
    silencios = []
    indice = 0
    total = len(rms)
    while indice < total:
        if rms[indice] < limiar_absoluto:
            fim = indice
            while fim < total and rms[fim] < limiar_absoluto:
                fim += 1
            if fim - indice >= minimo_janelas:
                silencios.append((indice, fim))
            indice = fim
        else:
            indice += 1
    return silencios


def silencio_mais_proximo(silencios, tempo, passo):
    melhor = None
    melhor_distancia = None
    for inicio, fim in silencios:
        t0 = inicio * passo
        t1 = fim * passo
        if t0 <= tempo <= t1:
            distancia = 0.0
        else:
            distancia = min(abs(tempo - t0), abs(tempo - t1))
        if melhor_distancia is None or distancia < melhor_distancia:
            melhor_distancia = distancia
            melhor = (t0, t1)
    return melhor, melhor_distancia


def barra(valor, referencia):
    if referencia <= 0:
        return ""
    proporcao = min(1.0, valor / referencia)
    cheias = int(round(proporcao * LARGURA_BARRA))
    return "#" * cheias + "." * (LARGURA_BARRA - cheias)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    argumentos = sys.argv[1:]
    if not argumentos:
        print(AJUDA)
        print("Faltou o arquivo de audio e pelo menos um tempo candidato.")
        sys.exit(1)

    opcoes = ler_argumentos(argumentos)

    if opcoes["caminho"] is None:
        erro("faltou o caminho do audio16k.wav.")
    if not opcoes["tempos"]:
        erro(
            "faltou pelo menos um tempo candidato, em segundos.\n"
            "       Exemplo:  flow-reels planejar/energia_audio audio16k.wav 412.8 421.6"
        )

    achado = achar_audio(opcoes["caminho"])
    if achado is not None:
        opcoes["caminho"] = achado

    numpy = carregar_numpy()
    amostras, taxa = ler_wav(opcoes["caminho"], numpy)
    duracao = len(amostras) / float(taxa)

    rms, passo = medir_envelope(amostras, taxa, opcoes["janela"], numpy)
    referencia = float(numpy.percentile(rms, 90))
    limiar_absoluto = referencia * opcoes["limiar"]
    minimo_janelas = max(1, int(round(opcoes["min_silencio"] / opcoes["janela"])))
    silencios = achar_silencios(rms, limiar_absoluto, minimo_janelas)

    resultado = {
        "arquivo": opcoes["caminho"],
        "taxa": taxa,
        "duracao": round(duracao, 3),
        "janela_ms": opcoes["janela"],
        "fala_plena": round(referencia, 6),
        "limiar": round(limiar_absoluto, 6),
        "silencios_encontrados": len(silencios),
        "candidatos": [],
    }

    for tempo in opcoes["tempos"]:
        item = {"tempo": tempo}
        if tempo < 0 or tempo > duracao:
            item["situacao"] = "fora do audio"
            item["aviso"] = (
                "o tempo " + ("%.2f" % tempo) + " s esta fora do audio, que dura "
                + ("%.2f" % duracao) + " s"
            )
            resultado["candidatos"].append(item)
            continue

        perto, distancia = silencio_mais_proximo(silencios, tempo, passo)
        indice = int(round(tempo / passo))
        dentro = bool(rms[min(indice, len(rms) - 1)] < limiar_absoluto)
        item["em_silencio"] = dentro
        if perto is None:
            item["situacao"] = "sem silencio no arquivo"
        else:
            t0, t1 = perto
            item["situacao"] = "ok" if distancia == 0.0 else "mover"
            item["silencio"] = {
                "inicio": round(t0, 3),
                "fim": round(t1, 3),
                "duracao": round(t1 - t0, 3),
                "distancia": round(distancia, 3),
            }
            item["sugestao_entrada"] = round(max(t0, t1 - 0.10), 3)
            item["sugestao_saida"] = round(min(t1, t0 + 0.30), 3)
        resultado["candidatos"].append(item)

    if opcoes["json"]:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return

    print("")
    print("Arquivo: " + opcoes["caminho"])
    print(
        "Taxa: " + str(taxa) + " Hz   Duracao: " + ("%.2f" % duracao) + " s"
        + "   Janela: " + ("%g" % opcoes["janela"]) + " ms"
    )
    if taxa != 16000:
        print("Aviso: o audio nao esta em 16 kHz. A medida funciona, mas o padrao do pacote e 16 kHz.")
    print(
        "Fala plena (percentil 90): " + ("%.5f" % referencia)
        + "   Limiar de silencio: " + ("%.5f" % limiar_absoluto)
        + "  (" + ("%g" % (opcoes["limiar"] * 100)) + "%)"
    )
    print(
        "Silencios de pelo menos " + ("%g" % opcoes["min_silencio"]) + " ms no arquivo inteiro: "
        + str(len(silencios))
    )

    for item in resultado["candidatos"]:
        tempo = item["tempo"]
        print("")
        print("=" * 72)
        print("Candidato em " + ("%.3f" % tempo) + " s")
        print("=" * 72)

        if item["situacao"] == "fora do audio":
            print("  " + item["aviso"])
            continue

        inicio = max(0, int((tempo - opcoes["raio"]) / passo))
        fim = min(len(rms), int((tempo + opcoes["raio"]) / passo) + 1)
        marca = int(round(tempo / passo))

        print("   tempo   energia relativa                    situacao")
        for indice in range(inicio, fim):
            instante = indice * passo
            valor = float(rms[indice])
            relativa = 0.0 if referencia <= 0 else (valor / referencia) * 100.0
            silenciosa = valor < limiar_absoluto
            ponteiro = ">" if indice == marca else " "
            situacao = "SILENCIO" if silenciosa else "fala"
            print(
                " " + ponteiro + " " + ("%7.3f" % instante)
                + "  " + barra(valor, referencia)
                + ("%6.1f" % relativa) + "%  " + situacao
            )

        print("")
        if item["situacao"] == "sem silencio no arquivo":
            print("  Nenhum silencio encontrado no arquivo com os parametros atuais.")
            print("  Ou a fala e emendada do inicio ao fim, ou o limiar esta baixo demais.")
            print("  Tente de novo com --limiar 0.12.")
            continue

        silencio = item["silencio"]
        print(
            "  Silencio mais proximo: de " + ("%.3f" % silencio["inicio"])
            + " s a " + ("%.3f" % silencio["fim"]) + " s"
            + "  (" + ("%.0f" % (silencio["duracao"] * 1000)) + " ms)"
        )
        if item["em_silencio"]:
            print("  O ponto candidato JA cai dentro de silencio.")
        else:
            print(
                "  O ponto candidato esta a " + ("%.0f" % (silencio["distancia"] * 1000))
                + " ms do silencio. Mova ele."
            )
        print("  Se este ponto e ENTRADA, use " + ("%.3f" % item["sugestao_entrada"]) + " s.")
        print("  Se este ponto e SAIDA,   use " + ("%.3f" % item["sugestao_saida"]) + " s.")
        if silencio["duracao"] > 0.700:
            print(
                "  Aviso: esta pausa tem mais de 700 ms. Cortar no meio dela abre o corte"
            )
            print("  com silencio. Aproxime o ponto da fala.")
        elif silencio["duracao"] < 0.400:
            print("  Aviso: esta pausa tem menos de 400 ms, que e o minimo para entrada e")
            print("  saida respirarem. Da para usar como um ponto, nao para emendar dois")
            print("  segmentos dentro dela.")

    print("")
    print("Barra cheia = fala plena daquela gravacao. A regra completa esta em CORTE-LIMPO.md.")
    print("")


if __name__ == "__main__":
    main()
