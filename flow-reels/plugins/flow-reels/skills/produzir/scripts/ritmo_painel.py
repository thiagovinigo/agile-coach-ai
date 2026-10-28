#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ritmo_painel.py  ·  mede o ritmo do painel no vídeo renderizado, não no plano

O beats.yaml diz quando cada coisa deveria mudar. Este script confere o que de
fato mudou no painel.mp4, quadro a quadro, e reprova o painel antes da montagem
quando ele fica parado demais ou quando abre fraco. Existe porque painel parado
passava na conferência por quadros soltos: olhando cinco quadros, tudo parece
vivo; assistindo, a tela congela por seis segundos.

Três conferências, as três com número:

  parado     o maior trecho sem nenhuma mudança visível. Lei: PADRAO-VISUAL.md
             seção 5, "parado só vale como descanso, no máximo cerca de 2 s".
             Reprova acima de --limite (padrão 2,5 s, a lei com folga de meio
             segundo para a curva de chegada terminar).

  abertura   os primeiros segundos são o trailer do corte (PADRAO-VISUAL.md
             seção 5.1). Reprova se, aos 2 s, o painel ainda tem menos da metade
             do conteúdo que ele costuma ter no resto do corte, ou se os 5
             primeiros segundos têm menos de 3 mudanças.

  trocas     quadro em que mais de um terço do painel muda de uma vez. No mundo
             único isso quase sempre é troca de herói ou tela limpa. Não
             reprova sozinho, porque abrir uma janela de tela real também dispara,
             mas é listado para alguém olhar.

O que conta como mudança: a diferença entre dois quadros seguidos, medida no
painel reduzido a 1/4 (o que apaga o grão), cobrindo pelo menos 0,2% da área.
Um chip, um número que vira outro ou uma palavra digitada contam; um cursor
piscando não. Mudanças separadas por até 3 quadros viram um evento só, porque
uma chegada de 800 ms é um evento e não dez. Os números foram calibrados nos
primeiros oito painéis do pacote.

Uso:

    flow-reels produzir/ritmo_painel projetos/<video>/materiais-de-trabalho/corte-01/painel.mp4
    flow-reels produzir/ritmo_painel <painel.mp4> --beats <beats.yaml>
    flow-reels produzir/ritmo_painel projetos/<video>/corte-01/corte-01.mp4 --corte
    flow-reels produzir/ritmo_painel <painel.mp4> --janela 12.0:20.0

--beats   aponta, para cada trecho parado, o beat que veio antes dele, que é
          onde se conserta.
--corte   mede o MP4 montado, recortando o painel de cima só até y 786, porque
          dali para baixo é a zona quieta onde a legenda passa, e a legenda
          mudando a cada palavra esconderia um painel parado.
--janela  mede só um trecho, em segundos do painel. Serve para conferir um
          conserto sem medir o corte inteiro de novo.
--json    imprime o resultado em JSON, para outro script ler.

Saída 0 = passou. Saída 1 = reprovou, com os instantes. Saída 2 = erro de uso.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


FPS = 12            # o painel é autorado a 12 quadros por segundo
LARGURA = 270       # 1080 / 4: reduzir apaga o grão e acelera a conta
ALTURA = 239        # 956 / 4
DIFERENCA = 12      # quanto um pixel precisa mudar, em 0 a 255, para contar
JUNTA = 3           # quadros de folga que ainda são o mesmo evento
TROCA_GRANDE = 0.35 # fração do painel que muda de uma vez numa troca de tela


def erro(msg):
    print("  erro: " + msg, file=sys.stderr)


def carregar_numpy():
    try:
        import numpy
    except ImportError:
        erro("o numpy não está instalado neste Python.\n"
             "       Rode com o Python do pacote: .venv/bin/python, ou instale com: pip install numpy")
        sys.exit(2)
    return numpy


def ler_quadros(caminho, corte, janela, np):
    if shutil.which("ffmpeg") is None:
        erro("ffmpeg não encontrado no PATH. Rode o instalar.sh na raiz do pacote.")
        sys.exit(2)
    altura = ALTURA
    filtros = []
    if corte:
        filtros.append("crop=1080:786:0:0")
        altura = 196  # 786 / 4
    filtros += ["fps=%d" % FPS, "scale=%d:%d:flags=area" % (LARGURA, altura), "format=gray"]
    cmd = ["ffmpeg", "-v", "error"]
    if janela:
        cmd += ["-ss", "%.3f" % janela[0], "-to", "%.3f" % janela[1]]
    cmd += ["-i", str(caminho), "-vf", ",".join(filtros), "-f", "rawvideo", "-"]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        erro("o ffmpeg não conseguiu ler o vídeo:\n" + proc.stderr.decode("utf-8", "ignore")[-600:])
        sys.exit(2)
    bruto = proc.stdout
    tamanho = LARGURA * altura
    n = len(bruto) // tamanho
    if n < FPS:
        erro("o vídeo tem menos de um segundo de painel. Confira o caminho.")
        sys.exit(2)
    return np.frombuffer(bruto[: n * tamanho], np.uint8).reshape(n, altura, LARGURA).astype(np.int16)


def ler_beats(caminho):
    """Lê só t e ideia de cada beat, sem depender de biblioteca de YAML."""
    beats = []
    atual = None
    for linha in Path(caminho).read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*-\s*t:\s*([0-9.]+)", linha)
        if m:
            atual = {"t": float(m.group(1)), "ideia": "", "descanso": False}
            beats.append(atual)
            continue
        if atual is None:
            continue
        m = re.match(r"\s*ideia:\s*[\"']?(.*?)[\"']?\s*$", linha)
        if m:
            atual["ideia"] = m.group(1)
        if re.match(r"\s*descanso:\s*true", linha):
            atual["descanso"] = True
    return sorted(beats, key=lambda b: b["t"])


def medir(quadros, np, area, inicio):
    fracoes = (np.abs(np.diff(quadros, axis=0)) > DIFERENCA).mean(axis=(1, 2))
    ativos = np.where(fracoes > area)[0] + 1

    eventos = []
    for i in ativos:
        if eventos and i - eventos[-1][1] <= JUNTA:
            eventos[-1][1] = int(i)
        else:
            eventos.append([int(i), int(i)])

    total = len(quadros)
    marcos = [0] + [x for e in eventos for x in e] + [total]
    paradas = []
    for i in range(0, len(marcos), 2):
        de, ate = marcos[i], marcos[i + 1]
        paradas.append({"de": inicio + de / FPS, "ate": inicio + ate / FPS, "dura": (ate - de) / FPS})

    # conteúdo visível: densidade de bordas, que responde a texto, traço e peça, e não ao fundo
    def densidade(q):
        gx = np.abs(np.diff(q, axis=1))[:-1, :]
        gy = np.abs(np.diff(q, axis=0))[:, :-1]
        return float(((gx + gy) > 40).mean())

    amostras = [densidade(quadros[i]) for i in range(0, total, FPS // 2)]
    mediana = float(np.median(amostras)) if amostras else 0.0
    janela_2s = [densidade(quadros[i]) for i in range(int(1.5 * FPS), min(total, int(2.5 * FPS) + 1))]
    aos_2s = max(janela_2s) if janela_2s else 0.0

    trocas = [inicio + (int(i) + 1) / FPS for i in np.where(fracoes > TROCA_GRANDE)[0]]

    return {
        "duracao": total / FPS,
        "eventos": [{"de": inicio + a / FPS, "ate": inicio + b / FPS} for a, b in eventos],
        "paradas": paradas,
        "densidade_mediana": mediana,
        "densidade_aos_2s": aos_2s,
        "trocas_grandes": trocas,
    }


def beat_antes(beats, t):
    anteriores = [b for b in beats if b["t"] <= t + 0.05]
    return anteriores[-1] if anteriores else None


def main():
    ap = argparse.ArgumentParser(
        description="Mede o ritmo do painel renderizado: trechos parados, abertura e trocas grandes.")
    ap.add_argument("video", help="o painel.mp4, ou o corte montado com --corte")
    ap.add_argument("--beats", help="o beats.yaml do corte, para apontar o beat de cada trecho parado")
    ap.add_argument("--corte", action="store_true", help="o vídeo é o corte montado: mede só o painel de cima")
    ap.add_argument("--janela", help="mede só um trecho, no formato inicio:fim em segundos")
    ap.add_argument("--limite", type=float, default=2.5, help="maior trecho parado aceito, em segundos (padrão 2,5)")
    ap.add_argument("--area", type=float, default=0.002, help="fração mínima do painel que precisa mudar (padrão 0,002)")
    ap.add_argument("--json", action="store_true", help="imprime o resultado em JSON")
    args = ap.parse_args()

    caminho = Path(args.video)
    if not caminho.is_file():
        erro("não achei o vídeo %s" % caminho)
        return 2

    janela = None
    if args.janela:
        try:
            a, b = [float(x.replace(",", ".")) for x in args.janela.split(":")]
            janela = (a, b)
        except ValueError:
            erro("--janela é inicio:fim em segundos, por exemplo 12.0:20.0")
            return 2

    np = carregar_numpy()
    quadros = ler_quadros(caminho, args.corte, janela, np)
    inicio = janela[0] if janela else 0.0
    r = medir(quadros, np, args.area, inicio)
    beats = ler_beats(args.beats) if args.beats else []

    reprovas = []

    # o trecho depois do último evento também conta: final parado é o fim que a pessoa
    # vê antes de decidir compartilhar, e a lei do último beat vale até o último quadro
    paradas_ruins = [p for p in r["paradas"] if p["dura"] > args.limite]
    for p in paradas_ruins:
        b = beat_antes(beats, p["de"]) if beats else None
        p["beat"] = ("t=%.1f %s" % (b["t"], b["ideia"])) if b else None
        reprovas.append("parado")

    abertura = []
    if not janela:
        eventos_5s = [e for e in r["eventos"] if e["de"] < 5.0]
        if len(eventos_5s) < 3:
            abertura.append("só %d mudança(s) nos 5 primeiros segundos; o piso é 3" % len(eventos_5s))
        med = r["densidade_mediana"]
        if med > 0 and r["densidade_aos_2s"] < 0.5 * med:
            abertura.append("aos 2 s o painel tem %.0f%% do conteúdo que ele costuma ter; o piso é 50%%"
                            % (100 * r["densidade_aos_2s"] / med))
        if abertura:
            reprovas.append("abertura")

    passou = not reprovas
    minutos = r["duracao"] / 60.0

    if args.json:
        saida = dict(r)
        saida.update({"passou": passou, "limite": args.limite,
                      "paradas_acima_do_limite": paradas_ruins, "abertura": abertura})
        print(json.dumps(saida, ensure_ascii=False, indent=2))
        return 0 if passou else 1

    print("")
    print("  ritmo do painel  ·  %s" % caminho)
    print("  %.1f s de painel, %d eventos (%.0f por minuto)"
          % (r["duracao"], len(r["eventos"]), len(r["eventos"]) / minutos if minutos else 0))
    maiores = sorted(r["paradas"], key=lambda p: -p["dura"])[:3]
    print("  maiores trechos parados: " + ", ".join(
        "%.1f s (em %.1f)" % (p["dura"], p["de"]) for p in maiores))
    print("")

    if paradas_ruins:
        print("  REPROVADO  parado acima de %.1f s:" % args.limite)
        for p in paradas_ruins:
            linha = "    %.1f s a %.1f s  ·  %.1f s sem mudança" % (p["de"], p["ate"], p["dura"])
            if p.get("beat"):
                linha += "  ·  depois do beat %s" % p["beat"]
            print(linha)
        print("    Conserto: dê ao herói mais um ato nesse trecho (um filho entra, um valor corre,")
        print("    a câmera aproxima, uma parte acende ou risca), no próximo beat-chave da fala.")
        print("    Não resolva com animação em loop nem com pílula repetindo a legenda.")
        print("")
    else:
        print("  ok  nenhum trecho parado acima de %.1f s" % args.limite)

    if not janela:
        if abertura:
            print("  REPROVADO  abertura fraca:")
            for a in abertura:
                print("    " + a)
            print("    Conserto: o herói já chega inteiro no primeiro segundo e a abertura tem o")
            print("    ritmo mais quente do corte (PADRAO-VISUAL.md seção 5.1).")
            print("")
        else:
            print("  ok  abertura: painel cheio aos 2 s e ritmo de trailer nos 5 primeiros")

    if r["trocas_grandes"]:
        print("  olhe  %d quadro(s) em que mais de um terço do painel mudou de uma vez: %s"
              % (len(r["trocas_grandes"]), ", ".join("%.1f s" % t for t in r["trocas_grandes"][:8])))
        print("        Janela de tela abrindo é normal. Herói trocado ou tela limpa fere o mundo único.")

    print("")
    print("  %s" % ("PASSOU" if passou else "REPROVADO: conserte e meça de novo antes de montar"))
    print("")
    return 0 if passou else 1


if __name__ == "__main__":
    sys.exit(main())
