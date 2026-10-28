# -*- coding: utf-8 -*-
"""O relogio mestre do reel narrado.

Monta a linha do tempo final a partir da tomada de voz escolhida e, quando houver,
dos trechos da filmagem que tocam com o som deles (so quando O SOM E O PRODUTO).
Tudo que vem depois, imagem, legenda e mix, le este relogio.

Dois modos:

    flow-reels narrado/linha_do_tempo --energia materiais-de-trabalho/fonte/filme.mp4
        imprime os trechos quietos da midia (abaixo de -38 dB por 0,12 s ou mais).
        Corte de filmagem cai no meio de um deles, nunca num tempo de transcricao.

    flow-reels narrado/linha_do_tempo --projeto projetos/x --narrado 01
        le tomadas.json ("voz" e, opcional, "trilha") e escreve em construcao/:
        linha_do_tempo.json, voz.wav, som.wav e niveis.json.

A trilha, quando existe, intercala a voz com trechos que tocam com o proprio som:

    "trilha": [
      {"tipo": "voz", "ate": "isso."},
      {"tipo": "som", "nome": "demo", "fonte": "materiais-de-trabalho/fonte/filme.mp4",
       "entrada": 10.85, "saida": 16.85},
      {"tipo": "voz", "ate": "FIM"}
    ]

Sem "trilha", a voz corre inteira, do comeco ao fim, e a filmagem fica muda. Entre a
voz e um trecho com som entram 0,30 s de ar dos dois lados ("respiro_som").
"""

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402

ESMAECER = 0.025
LIMIAR_DB = -38.0
MINIMO_QUIETO = 0.12


def esmaecer(x):
    k = min(int(ESMAECER * cm.SR), len(x) // 2)
    x = x.copy()
    if k:
        x[:k] *= np.linspace(0, 1, k)
        x[-k:] *= np.linspace(1, 0, k)
    return x


def trechos_quietos(amostras, limiar=LIMIAR_DB, minimo=MINIMO_QUIETO):
    lv = np.array(cm.niveis(amostras))
    if len(lv) == 0:
        return []
    db = 20 * np.log10(lv + 1e-9)
    quietos, comeco = [], None
    for i, q in enumerate(list(db < limiar) + [False]):
        if q and comeco is None:
            comeco = i
        if not q and comeco is not None:
            if (i - comeco) / cm.FPS >= minimo:
                quietos.append((comeco / cm.FPS, i / cm.FPS))
            comeco = None
    return quietos


def nivel_db_em(amostras, t, janela=0.05):
    a = max(0, int((t - janela) * cm.SR))
    b = min(len(amostras), int((t + janela) * cm.SR))
    if b <= a:
        return -120.0
    return float(20 * np.log10(np.sqrt((amostras[a:b] ** 2).mean()) + 1e-9))


def modo_energia(caminho, limiar, minimo):
    cm.exigir_ffmpeg()
    x = cm.carregar_audio(caminho)
    if len(x) == 0:
        cm.fala("%s nao tem audio. Corte onde a imagem pedir." % caminho)
        return 0
    q = trechos_quietos(x, limiar, minimo)
    cm.fala("%s: %.2f s. Trechos quietos abaixo de %.0f dB por %.2f s ou mais (corte no meio):"
            % (caminho, len(x) / cm.SR, limiar, minimo))
    for a, b in q:
        cm.fala("  %7.2f a %7.2f   meio %7.2f" % (a, b, (a + b) / 2))
    if not q:
        cm.fala("  nenhum. A filmagem nao para de soar; corte onde a imagem muda e esmaeca.")
    return 0


def montar(cam, tomadas):
    voz_cfg = tomadas.get("voz") or {}
    take = voz_cfg.get("take")
    if not take:
        cm.erro('o tomadas.json precisa de "voz": {"take": "a-respiro"} (ou outra tomada).')
    audio = next((cam.voz / ("voz-%s.%s" % (take, e)) for e in ("wav", "mp3")
                  if (cam.voz / ("voz-%s.%s" % (take, e))).is_file()), None)
    if audio is None:
        cm.erro("nao achei voz/voz-%s.wav nem .mp3. Gere a voz antes (voz.py, respirar.py)." % take)
    palavras = cm.ler_palavras(cam.voz / ("palavras-%s.json" % take))
    if not palavras:
        cm.erro("palavras-%s.json vazio." % take)
    voz = cm.carregar_audio(audio)

    trilha = tomadas.get("trilha") or [{"tipo": "voz", "ate": "FIM"}]
    ar = float(tomadas.get("respiro_som", 0.30))
    cauda = float((tomadas.get("fechamento") or {}).get("cauda", 1.2))

    t, anterior, cursor = 0.0, None, 0
    saida_voz, saida_som, segmentos, mestre = [], [], [], []
    for n, seg in enumerate(trilha):
        tipo = seg.get("tipo")
        if tipo == "voz":
            if cursor >= len(palavras):
                cm.erro("a trilha pede mais voz do que a tomada tem (segmento %d)." % (n + 1))
            ate = seg.get("ate", "FIM")
            if ate == "FIM":
                i1 = len(palavras) - 1
            else:
                alvo = cm.normalizar(ate)
                i1 = next((i for i in range(cursor, len(palavras))
                           if cm.normalizar(palavras[i]["texto"]) == alvo), None)
                if i1 is None:
                    cm.erro('a trilha manda a voz ir "ate" %r, e essa palavra nao aparece depois '
                            'da palavra %d.' % (ate, cursor + 1))
            ws = palavras[cursor:i1 + 1]
            cursor = i1 + 1
            a = max(0.0, ws[0]["inicio"] - 0.06)
            b = min(len(voz) / cm.SR, ws[-1]["fim"] + 0.14)
            t += ar if anterior == "som" else (0.10 if anterior == "voz" else 0.0)
            saida_voz.append((int(round(t * cm.SR)), esmaecer(voz[int(a * cm.SR):int(b * cm.SR)])))
            segmentos.append({"tipo": "voz", "nome": seg.get("nome", "voz-%d" % (n + 1)),
                              "t0": round(t, 3), "t1": round(t + b - a, 3),
                              "texto": " ".join(w["texto"] for w in ws)})
            mestre += [{"texto": w["texto"], "inicio": round(t + w["inicio"] - a, 3),
                        "fim": round(t + w["fim"] - a, 3)} for w in ws]
            t += b - a
            anterior = "voz"
        elif tipo == "som":
            fonte = cam.no_projeto(seg.get("fonte") or tomadas.get("fonte_padrao"))
            if not fonte or not fonte.is_file():
                cm.erro("o trecho com som %r aponta para uma fonte que nao existe: %s"
                        % (seg.get("nome"), fonte))
            t += ar if anterior else 0.0
            cheio = cm.carregar_audio(fonte)
            pecas_pedidas = seg.get("pecas") or [[seg["entrada"], seg["saida"]]]
            pecas, t0 = [], t
            for p in pecas_pedidas:
                a, b = float(p[0]), float(p[1])
                for ponto in (a, b):
                    db = nivel_db_em(cheio, ponto)
                    if db > LIMIAR_DB:
                        cm.aviso("o trecho %r corta em %.2f s com o som em %.0f dB. Procure um "
                                 "silencio com --energia." % (seg.get("nome"), ponto, db))
                saida_som.append((int(round(t * cm.SR)), esmaecer(cheio[int(a * cm.SR):int(b * cm.SR)])))
                pecas.append([round(t, 3), a, b])
                t += b - a
            segmentos.append({"tipo": "som", "nome": seg.get("nome", "som-%d" % (n + 1)),
                              "fonte": seg.get("fonte") or tomadas.get("fonte_padrao"),
                              "t0": round(t0, 3), "t1": round(t, 3), "pecas": pecas})
            anterior = "som"
        else:
            cm.erro("tipo de segmento desconhecido na trilha: %r (use voz ou som)." % tipo)

    if cursor < len(palavras):
        cm.aviso("a trilha terminou e sobraram %d palavras da voz sem uso." % (len(palavras) - cursor))

    total = round(t + cauda, 3)
    n = int(total * cm.SR)
    trilhas = {}
    for buf, nome in ((saida_voz, "voz"), (saida_som, "som")):
        y = np.zeros(n, np.float32)
        for em, x in buf:
            y[em:em + len(x)] += x[:max(0, n - em)]
        cm.gravar_wav(cam.construcao / (nome + ".wav"), y)
        trilhas[nome] = cm.niveis(y)

    cm.gravar_json(cam.linha, {"duracao": total, "take": take, "segmentos": segmentos,
                               "palavras": mestre})
    cm.gravar_json(cam.construcao / "niveis.json", trilhas)
    for s in segmentos:
        cm.fala("%-4s %-12s %6.2f a %6.2f  %s" % (s["tipo"], s["nome"], s["t0"], s["t1"],
                                                 (s.get("texto") or s.get("fonte") or "")[:60]))
    cm.fala("duracao total %.2f s (com %.2f s de cauda)" % (total, cauda))
    if not 40.0 <= total <= 50.0:
        cm.aviso("o reel fica com %.1f s; o formato pede de 40 a 50 s. Ajuste o roteiro, nunca a "
                 "velocidade da voz." % total)
    cm.fala(str(cam.linha))
    return 0


def principal(argv=None):
    an = argparse.ArgumentParser(description="Monta o relogio mestre do reel narrado.")
    an.add_argument("--energia", metavar="MIDIA", help="so lista os trechos quietos desta midia")
    an.add_argument("--limiar", type=float, default=LIMIAR_DB, help="limiar de silencio em dB (padrao -38)")
    an.add_argument("--minimo", type=float, default=MINIMO_QUIETO, help="silencio minimo em s (padrao 0.12)")
    an.add_argument("--projeto", help="pasta do projeto")
    an.add_argument("--narrado", default="01", help="numero do reel narrado (padrao 01)")
    op = an.parse_args(argv)
    if op.energia:
        return modo_energia(op.energia, op.limiar, op.minimo)
    if not op.projeto:
        an.print_help()
        return 2
    cm.exigir_ffmpeg()
    cam = cm.Caminhos(op.projeto, op.narrado)
    cam.construcao.mkdir(parents=True, exist_ok=True)
    return montar(cam, cm.ler_tomadas(cam))


if __name__ == "__main__":
    sys.exit(principal())
