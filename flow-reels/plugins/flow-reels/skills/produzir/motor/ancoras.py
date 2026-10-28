#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ancoras.py  ·  tempos presos à palavra da fala, e o fiscal da câmera do modo mundo

Qualquer tempo do cenas.json pode ser escrito como a palavra em que ele acontece, em vez do segundo:

    "t": {"ancora": "planilha"}                  a primeira vez que a fala diz planilha
    "t": {"ancora": "linha cem"}                 a primeira vez que as duas palavras vêm seguidas
    "t": {"ancora": "planilha#2", "ajuste": 0}   a segunda vez, sem recuo
    { "ancora": "fórmula", "cx": 700, ... }      no objeto: vira o "t" dele

Maiúscula, acento e pontuação não contam: "Planilha," acha "planilha". A fala é o
palavras-corte.json, a mesma linha do tempo do plano. Quando o corte muda de duração, roda de
novo e tudo se recalcula: ninguém reescreve número à mão.

O recuo padrão diz onde o tempo cai em relação ao começo da palavra:

    inicio e fim de uma cena                2 quadros antes (o corte cai antes do som)
    chave de câmera de um mundo             1 quadro antes (o olho já está lá quando a fala nomeia)
    todo o resto                            0,2 s antes (o movimento termina em cima da palavra)

A cena sem "fim" termina onde a próxima começa (a última, na duração do corte). A lei do modo mundo
está no MOTOR.md, seção 4.14; o fiscal da câmera (conferir_mundos) recusa o que ela proíbe.

Rodar direto mostra o plano com os tempos resolvidos, sem renderizar nada:

    flow-reels produzir/ancoras --projeto projetos/<video> --corte 03
"""

import argparse
import copy
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RECUO_CENA_QUADROS = 2
RECUO_CHAVE_QUADROS = 1
RECUO_PADRAO = 0.2

# a câmera do mundo (MOTOR.md 4.14, que veio da lei do layout motion)
CAMERAS = ("calma", "parada")
MAX_CHAVES = 7
MAX_CHICOTES = 1
ZOOM_LEITURA = 1.32
ZOOM_MAXIMO = 1.40
MOVER_PADRAO = 1.1
MOVER_FAIXA = (0.85, 1.4)


def normalizar(texto):
    t = unicodedata.normalize("NFD", str(texto or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^\w%]+", " ", t)
    return t.strip()


class Fala:
    """As palavras do corte, prontas para achar uma âncora."""

    def __init__(self, palavras):
        lista = palavras.get("palavras") if isinstance(palavras, dict) else palavras
        self.itens = []
        for p in lista or []:
            if not isinstance(p, dict):
                continue
            for parte in normalizar(p.get("texto") or p.get("palavra") or "").split():
                self.itens.append((parte, float(p.get("inicio", 0.0))))

    def achar(self, ancora):
        """O começo da palavra (ou da sequência) pedida, ou None."""
        texto, _, n = str(ancora).partition("#")
        ocorrencia = int(n) if n.strip().isdigit() else 1
        alvo = normalizar(texto).split()
        if not alvo:
            return None
        achadas = 0
        for i in range(len(self.itens) - len(alvo) + 1):
            if all(self.itens[i + j][0] == alvo[j] for j in range(len(alvo))):
                achadas += 1
                if achadas == ocorrencia:
                    return self.itens[i][1]
        return None


def _recuo(caminho, fps):
    if len(caminho) == 3 and caminho[0] == "cenas" and caminho[2] in ("inicio", "fim"):
        return -RECUO_CENA_QUADROS / fps
    if len(caminho) >= 3 and caminho[0] == "mundos" and "chaves" in caminho:
        return -RECUO_CHAVE_QUADROS / fps
    return -RECUO_PADRAO


def _eh_ancora_pura(v):
    return isinstance(v, dict) and isinstance(v.get("ancora"), str) and set(v) <= {"ancora", "ajuste"}


def resolver_ancoras(cenas, palavras, fps=30):
    """Devolve (plano com os tempos resolvidos, erros, quantas âncoras resolveu). Não mexe no original."""
    plano = copy.deepcopy(cenas)
    fala = Fala(palavras)
    erros, contagem = [], [0]

    def tempo(ancora, ajuste, caminho):
        t = fala.achar(ancora)
        if t is None:
            erros.append('a âncora "%s" (%s) não está na fala do corte' % (ancora, "/".join(map(str, caminho))))
            return None
        contagem[0] += 1
        return round(max(0.0, t + (float(ajuste) if ajuste is not None else _recuo(caminho, fps))), 3)

    def andar(no, caminho):
        if isinstance(no, dict):
            # o objeto com "ancora" e sem "t" ganha o "t" dela (a chave de câmera, o beat)
            if isinstance(no.get("ancora"), str) and "t" not in no and not _eh_ancora_pura(no):
                t = tempo(no["ancora"], no.get("ajuste"), caminho + ["t"])
                if t is not None:
                    no["t"] = t
            for k in list(no.keys()):
                v = no[k]
                if _eh_ancora_pura(v):
                    t = tempo(v["ancora"], v.get("ajuste"), caminho + [k])
                    no[k] = t if t is not None else v
                else:
                    andar(v, caminho + [k])
        elif isinstance(no, list):
            for i, v in enumerate(no):
                if _eh_ancora_pura(v):
                    t = tempo(v["ancora"], v.get("ajuste"), caminho + [i])
                    no[i] = t if t is not None else v
                else:
                    andar(v, caminho + [i])

    andar(plano, [])

    # a cena sem fim termina onde a próxima começa
    lista = plano.get("cenas") or []
    duracao = plano.get("duracao")
    for i, c in enumerate(lista):
        if not isinstance(c, dict):
            continue
        if i == 0 and c.get("inicio") is None:
            c["inicio"] = 0.0
        if c.get("fim") is None:
            prox = lista[i + 1].get("inicio") if i + 1 < len(lista) and isinstance(lista[i + 1], dict) else None
            if isinstance(prox, (int, float)):
                c["fim"] = prox
            elif i == len(lista) - 1 and isinstance(duracao, (int, float)):
                c["fim"] = float(duracao)
    return plano, erros, contagem[0]


def conferir_mundos(plano):
    """O fiscal da câmera dos mundos. Devolve (erros, avisos). Roda com os tempos já resolvidos."""
    erros, avisos = [], []
    mundos = plano.get("mundos") or {}
    usados = {}
    for c in plano.get("cenas") or []:
        if isinstance(c, dict) and c.get("modo") == "mundo":
            nome = (c.get("conteudo") or {}).get("mundo")
            if nome not in mundos:
                erros.append('a cena %s pede o mundo "%s", que não está em "mundos"' % (c.get("id", "?"), nome))
                continue
            usados.setdefault(nome, []).append(c)
            sup = (c.get("conteudo") or {}).get("superficie", "quadro")
            if sup not in ("quadro", "pip", "rosto", "tela"):
                erros.append('a cena %s pede a superfície "%s" (valem quadro, pip, rosto e tela)'
                             % (c.get("id", "?"), sup))
    for nome, m in mundos.items():
        if not isinstance(m, dict):
            erros.append('o mundo "%s" não é um objeto' % nome)
            continue
        onde = 'mundo "%s"' % nome
        fonte = m.get("fonte") or {}
        if not any(k in fonte for k in ("html", "imagem", "video")):
            erros.append('%s: "fonte" precisa de "html", "imagem" ou "video"' % onde)
        if "html" in fonte and not (isinstance(m.get("tamanho"), list) and len(m["tamanho"]) == 2):
            erros.append('%s: mundo em html precisa de "tamanho": [largura, altura] (o mesmo do window.MUNDO '
                         'da página; o recomendado é [1080, 1350])' % onde)
        camera = m.get("camera", "calma")
        if camera not in CAMERAS:
            erros.append('%s: camera "%s" (valem calma e parada)' % (onde, camera))
            continue
        chaves = [k for k in (m.get("chaves") or []) if isinstance(k, dict)]
        sem_t = [i for i, k in enumerate(chaves) if not isinstance(k.get("t"), (int, float))]
        if sem_t:
            erros.append("%s: chave(s) %s sem tempo (\"t\" ou \"ancora\")" % (onde, ", ".join(str(i + 1) for i in sem_t)))
            continue
        if camera == "parada":
            if len(chaves) > 1 or any(float(k.get("zoom", 1)) != 1 for k in chaves):
                erros.append("%s: na câmera parada a câmera não se mexe: no máximo uma chave, com zoom 1 "
                             "(as coisas chegam no lugar dentro do mundo)" % onde)
            if any(k.get("chicote") for k in chaves):
                erros.append("%s: a câmera parada não tem chicote" % onde)
            continue
        if len(chaves) > MAX_CHAVES:
            erros.append("%s: %d chaves de câmera; o teto da câmera calma é %d (com 14 num corte de 35 s "
                         "ninguém consegue ler nada; com 5 ele respira)" % (onde, len(chaves), MAX_CHAVES))
        chicotes = [k for k in chaves if k.get("chicote")]
        if len(chicotes) > MAX_CHICOTES:
            erros.append("%s: %d chicotes; no máximo %d por corte" % (onde, len(chicotes), MAX_CHICOTES))
        anterior = None
        for i, k in enumerate(chaves):
            z = float(k.get("zoom", 1))
            if z > ZOOM_MAXIMO:
                erros.append("%s: chave %d com zoom %.2f; o teto é %.2f (empurrar para 2x cortou o título e o "
                             "número que a fala dizia)" % (onde, i + 1, z, ZOOM_MAXIMO))
            elif z > ZOOM_LEITURA:
                avisos.append("%s: chave %d com zoom %.2f; acima de %.2f só num close segurado"
                              % (onde, i + 1, z, ZOOM_LEITURA))
            mover = float(k.get("mover", MOVER_PADRAO))
            if i and not k.get("chicote") and not (MOVER_FAIXA[0] <= mover <= MOVER_FAIXA[1]):
                avisos.append("%s: chave %d move em %.2f s; a câmera calma move de %.2f a %.2f s"
                              % (onde, i + 1, mover, MOVER_FAIXA[0], MOVER_FAIXA[1]))
            if anterior is not None:
                if k["t"] <= anterior["t"]:
                    erros.append("%s: a chave %d (%.2f s) vem antes ou junto da anterior (%.2f s)"
                                 % (onde, i + 1, k["t"], anterior["t"]))
                elif not k.get("chicote") and k["t"] - mover < anterior["t"]:
                    avisos.append("%s: a chave %d começa a andar (%.2f s) antes da anterior chegar (%.2f s): "
                                  "a câmera não segura o enquadramento" % (onde, i + 1, k["t"] - mover, anterior["t"]))
            anterior = k
        if nome in usados and not chaves:
            avisos.append("%s: câmera calma sem chave nenhuma: a vista fica no mundo inteiro, só com a deriva"
                          % onde)
    for nome in mundos:
        if nome not in usados:
            avisos.append('o mundo "%s" não é usado por nenhuma cena' % nome)
    return erros, avisos


def main():
    ap = argparse.ArgumentParser(description="Mostra o cenas.json com as âncoras resolvidas.")
    ap.add_argument("--projeto", required=True)
    ap.add_argument("--corte", required=True)
    args = ap.parse_args()
    pasta = Path(args.projeto) / "materiais-de-trabalho" / ("corte-%02d" % int(args.corte))
    cenas = json.loads((pasta / "cenas.json").read_text(encoding="utf-8"))
    palavras = json.loads((pasta / "palavras-corte.json").read_text(encoding="utf-8"))
    plano, erros, n = resolver_ancoras(cenas, palavras, int(cenas.get("fps", 30)))
    e2, avisos = conferir_mundos(plano)
    print(json.dumps(plano, ensure_ascii=False, indent=1))
    print("\n%d âncora(s) resolvida(s)" % n, file=sys.stderr)
    for a in avisos:
        print("  aviso: " + a, file=sys.stderr)
    for e in erros + e2:
        print("  erro: " + e, file=sys.stderr)
    return 1 if erros or e2 else 0


if __name__ == "__main__":
    sys.exit(main())
