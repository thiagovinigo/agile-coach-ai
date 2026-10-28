#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
linguagem.py  ·  a linguagem do episódio: sugerir, registrar e conferir

Cada reel da 4.0 tem uma linguagem visual (terminal, cinema, recorte, sci-fi,
anos 80, mangá, profundidade 3D, editorial, turbo, calmo, manchete, vidro), com
as peças que combinam, um momento-herói e um kit de sons. A tabela mora em
motor/linguagens.json; o contrato inteiro em motor/docs-4/variedade-e-som.md.
Este script faz três coisas:

  sugerir    sorteia 3 linguagens para o corte, a primeira recomendada, com o
             herói, a convidada possível, os sons e uma trilha sugerida de cada.
             O sorteio é ponderado e reproduzível: a semente é o nome do projeto
             mais o número do corte, então o mesmo corte sorteia sempre o mesmo.
             Pesa, nesta ordem:
               - o material: a visão do corte (visao/visao.json) diz se há
                 máscara, profundidade que separa você do fundo e mãos; quem
                 pede o que não há fica de fora. --material tela (gravação de
                 tela) tira as que precisam de você em quadro;
               - o assunto (--assunto "texto livre") e o formato da série
                 (--formato), que puxam as linguagens que combinam;
               - a memória (projetos/.historico-linguagens.json, os últimos 10
                 reels): a linguagem não repete nos últimos 2, o herói nos
                 últimos 4 e a trilha nos últimos 8.
  registrar  grava no histórico a escolha do corte: linguagem, convidada, herói,
             trilha e data. Sem as opções, lê do cenas.json ("linguagem",
             "heroi" e "trilha"). O mesmo corte registrado de novo substitui o
             registro anterior.
  conferir   lê o cenas.json e diz se as peças usadas batem com a linguagem
             declarada ("linguagem": "<nome>" ou {"base": ..., "convidada": ...}),
             se a convidada fica em no máximo 2 cenas, se há no máximo 3 famílias
             de transição e se o momento-herói ("heroi": {"t": ..., "nome": ...})
             cai entre 55% e 80% da duração. Com o eventos.json, confere também
             os sons contra o kit da linguagem.

Uso:

    flow-reels produzir/linguagem sugerir   --projeto projetos/<video> --corte 01 [--assunto "..."] [--formato noticia]
    flow-reels produzir/linguagem registrar --projeto projetos/<video> --corte 01 [--linguagem terminal --heroi prompt-executa --trilha x.mp3]
    flow-reels produzir/linguagem conferir  --projeto projetos/<video> --corte 01

--historico  outro arquivo de histórico (padrão: projetos/.historico-linguagens.json na raiz).
--json       sugerir e conferir imprimem o resultado em JSON.

Saída 0 = tudo certo (no conferir: bate com a linguagem). Saída 1 = o conferir
achou problema (peça fora da linguagem, herói fora da faixa, transições demais,
convidada incompatível). Saída 2 = erro de uso (pasta, arquivo, nome errado).
"""

import argparse
import hashlib
import json
import random
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


OPCOES = 3                      # quantas linguagens o sugerir mostra
SEPARA_MINIMO = 40              # profundidade: pessoa - fundo (0 a 255) a partir da qual o mapa separa você da parede
VISAO_MINIMA = 50.0             # % dos quadros com a pessoa na máscara
MAOS_MINIMA = 25.0              # % dos quadros com alguma mão
PESO_ASSUNTO = 1.5              # cada palavra do assunto que bate soma 1,5x no peso (até 2 palavras)
PESO_FORMATO = (2.0, 0.2)       # formato que prefere / que evita
PESO_RECENTE = 0.75             # usada nos reels 3 a 6 do histórico: o peso cai (o "saco embaralhado")
EXTENSOES_TRILHA = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac"}


class Falha(Exception):
    def __init__(self, mensagem, codigo=2):
        super().__init__(mensagem)
        self.codigo = codigo


def erro(msg):
    sys.stdout.flush()
    print("  erro: " + msg, file=sys.stderr)


def achar_raiz():
    """A pasta de trabalho; as trilhas vêm de componentes/trilhas, da pasta ou do plugin."""
    return fabrica.raiz()


def resolver_projeto(raiz, pedido):
    alvo = Path(pedido)
    for caminho in (alvo, Path.cwd() / alvo, raiz / alvo, raiz / "projetos" / alvo):
        try:
            if caminho.is_dir():
                return caminho.resolve()
        except OSError:
            continue
    return None


def nome_do_corte(pedido):
    m = re.match(r"^(?:corte-)?0*(\d{1,3})$", str(pedido).strip())
    if not m or int(m.group(1)) == 0:
        return None
    return "%02d" % int(m.group(1))


def curto(caminho, raiz):
    try:
        return str(Path(caminho).resolve().relative_to(raiz))
    except ValueError:
        return str(caminho)


def ler_json(caminho, papel):
    try:
        return json.loads(Path(caminho).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as e:
        raise Falha("não consegui ler %s (%s): %s" % (caminho, papel, e))


def sem_acento(texto):
    texto = unicodedata.normalize("NFD", str(texto).lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def virgula(v, casas=1):
    return ("%.*f" % (casas, v)).replace(".", ",")


# ---------------------------------------------------------------------------
# A tabela e o histórico
# ---------------------------------------------------------------------------

def carregar_tabela():
    caminho = Path(__file__).resolve().parents[1] / "motor" / "linguagens.json"
    tabela = ler_json(caminho, "a tabela das linguagens")
    if not isinstance(tabela, dict) or not isinstance(tabela.get("linguagens"), dict):
        raise Falha("o %s não tem a chave \"linguagens\"" % caminho)
    # as peças "sempre" do estilos.json (o DNA de todo estilo) valem em toda linguagem, junto com as
    # "sempre" da própria tabela (onde mora o CTA da marca: comentario + dm)
    estilos = ler_json(caminho.parent / "estilos.json", "os estilos de produção")
    sempre = tabela.setdefault("sempre", {})
    for cat in ("modos", "sobre", "transicoes"):
        extra = ((estilos or {}).get("sempre") or {}).get(cat) or []
        sempre[cat] = list(dict.fromkeys(list(sempre.get(cat) or []) + list(extra)))
    return tabela


def eixos_diferentes(a, b):
    return sum(1 for k in ("tempo", "acabamento", "energia") if a["eixos"][k] != b["eixos"][k])


def par_proibido(tabela, a, b):
    return any({a, b} == set(p) for p in tabela["regras"]["pares_proibidos"])


def convidadas_possiveis(tabela, base_id):
    """As que podem entrar como convidada: diferem em um eixo só e não formam par proibido."""
    base = tabela["linguagens"][base_id]
    saida = []
    for lid, lg in sorted(tabela["linguagens"].items()):
        if lid != base_id and eixos_diferentes(base, lg) == tabela["regras"]["convidada_eixos_diferentes"] \
                and not par_proibido(tabela, base_id, lid):
            eixo = next(k for k in ("tempo", "acabamento", "energia") if base["eixos"][k] != lg["eixos"][k])
            saida.append((lid, eixo))
    return saida


def caminho_do_historico(raiz, pedido):
    return Path(pedido) if pedido else raiz / "projetos" / ".historico-linguagens.json"


def ler_historico(caminho):
    dados = ler_json(caminho, "o histórico de linguagens")
    if dados is None:
        return []
    reels = dados.get("reels") if isinstance(dados, dict) else None
    if not isinstance(reels, list):
        raise Falha("o %s não tem a lista \"reels\"; conserte ou mova o arquivo para recomeçar" % caminho)
    return [r for r in reels if isinstance(r, dict)]


def gravar_historico(caminho, reels, tamanho):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    texto = json.dumps({"_leia": "Os últimos %d reels: linguagem, convidada, herói, trilha e data. Escrito pelo "
                                 "linguagem.py registrar; lido pelo linguagem.py sugerir para não repetir." % tamanho,
                        "versao": 1, "reels": reels[-tamanho:]}, ensure_ascii=False, indent=1)
    caminho.write_text(texto + "\n", encoding="utf-8")


def nome_da_trilha(valor):
    if isinstance(valor, dict):
        valor = valor.get("arquivo")
    return Path(str(valor)).name if valor else None


# ---------------------------------------------------------------------------
# O material do corte
# ---------------------------------------------------------------------------

def ler_material(pasta, pedido):
    """O que o corte tem: visão (máscara), profundidade que separa, mãos, rosto. Com --material tela, nada disso."""
    m = {"visao": False, "profundidade": False, "maos": False, "rosto": False,
         "gravacao-de-tela": pedido == "tela", "notas": []}
    if pedido == "tela":
        m["notas"].append("gravação de tela (--material tela): sem visão, mãos nem rosto grande")
        return m
    rosto = ler_json(pasta / "rosto.json", "o rosto.json")
    if isinstance(rosto, dict) and any(q for q in rosto.get("quadros") or []):
        m["rosto"] = True
    visao = ler_json(pasta / "visao" / "visao.json", "a visão do corte")
    if not isinstance(visao, dict):
        m["notas"].append("sem visao/visao.json: rode o visao.py para liberar as linguagens que pedem a visão")
        return m
    origem = ler_json(pasta / "visao" / ".origem.json", "a origem da visão") or {}
    fala = pasta / (str(visao.get("fonte") or "fala.mp4"))
    if origem.get("tamanho") and fala.is_file() and fala.stat().st_size != origem.get("tamanho"):
        m["notas"].append("a visão é de outra edição da fala (o tamanho do vídeo mudou): rode o visao.py de novo")
        return m
    partes = visao.get("partes") or {}
    pessoa = visao.get("pessoa") or {}
    if partes.get("mascara") and (pessoa.get("porcentagem") or 0) >= VISAO_MINIMA:
        m["visao"] = True
        m["notas"].append("visão: a pessoa está na máscara em %s%% dos quadros" % virgula(pessoa.get("porcentagem") or 0, 0))
    else:
        m["notas"].append("visão fraca: a pessoa aparece em menos de %d%% dos quadros" % VISAO_MINIMA)
    prof = visao.get("profundidade") or {}
    if partes.get("profundidade") and prof.get("mediana_pessoa") is not None and prof.get("mediana_fundo") is not None:
        separa = prof["mediana_pessoa"] - prof["mediana_fundo"]
        m["profundidade"] = m["visao"] and separa >= SEPARA_MINIMO
        m["notas"].append("profundidade: você %s do fundo (%d de 255)" % ("se separa" if separa >= SEPARA_MINIMO else "quase não se separa", separa))
    maos = visao.get("maos") or {}
    if partes.get("maos") and (maos.get("porcentagem") or 0) >= MAOS_MINIMA:
        m["maos"] = True
    m["notas"].append("mãos em %s%% dos quadros" % virgula(maos.get("porcentagem") or 0, 0))
    return m


def falta_material(precisa, material):
    return [p for p in precisa if not material.get(p)]


# ---------------------------------------------------------------------------
# sugerir
# ---------------------------------------------------------------------------

def semente(projeto, nn):
    return int.from_bytes(hashlib.sha256(("%s|%s" % (projeto.name, nn)).encode("utf-8")).digest()[:8], "big")


def sorteio_ponderado(rng, itens):
    """itens = [(chave, peso)], já em ordem fixa. Devolve a chave sorteada."""
    total = sum(p for _, p in itens)
    alvo = rng.random() * total
    for chave, peso in itens:
        alvo -= peso
        if alvo <= 0:
            return chave
    return itens[-1][0]


def trilhas_disponiveis(raiz):
    pasta = fabrica.pasta("componentes/trilhas")
    if not pasta.is_dir():
        return []
    return sorted(p.name for p in pasta.iterdir()
                  if p.suffix.lower() in EXTENSOES_TRILHA and not p.name.startswith(("_", ".")))


def pesar(tabela, material, assunto, formato, historico):
    """O peso de cada linguagem, com o porquê, e as que ficam de fora com o motivo."""
    memoria = tabela["regras"]["memoria"]
    recentes = [r.get("linguagem") for r in reversed(historico)]
    bloqueadas = set(recentes[:memoria["linguagem"]])
    meio = recentes[memoria["linguagem"]:6]
    assunto_n = sem_acento(assunto or "")
    formatos = tabela.get("formatos", {})
    pesos, fora = [], []
    for lid, lg in sorted(tabela["linguagens"].items()):
        motivos = []
        falta = falta_material(lg.get("precisa", []), material)
        if falta:
            fora.append((lid, "pede %s, que o corte não tem" % " e ".join(falta)))
            continue
        if material.get("gravacao-de-tela") and "gravacao-de-tela" in lg.get("incompativel", []):
            fora.append((lid, "não roda em gravação de tela"))
            continue
        if lid in bloqueadas:
            fora.append((lid, "foi a linguagem de um dos últimos %d reels" % memoria["linguagem"]))
            continue
        peso = float(lg.get("peso", 1.0))
        if assunto_n:
            batem = [a for a in lg.get("assuntos", [])
                     if re.search(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(sem_acento(a)), assunto_n)]
            if batem:
                peso *= 1.0 + PESO_ASSUNTO * min(len(batem), 2)
                motivos.append("o assunto bate (%s)" % ", ".join(batem[:3]))
        if formato:
            f = formatos.get(formato, {})
            if lid in f.get("preferidas", []):
                peso *= PESO_FORMATO[0]
                motivos.append("combina com o formato %s" % f.get("nome", formato))
            elif lid in f.get("evitar", []):
                peso *= PESO_FORMATO[1]
                motivos.append("o formato %s pede outra (peso baixo)" % f.get("nome", formato))
        if not any(not falta_material(h.get("precisa", []), material) for h in lg.get("heroi", [])):
            peso *= 0.3
            motivos.append("nenhum herói dela cabe no material (peso baixo)")
        vezes = meio.count(lid)
        if vezes:
            peso *= PESO_RECENTE ** vezes
            motivos.append("usada há pouco (peso menor)")
        pesos.append((lid, peso, motivos))
    return pesos, fora


def escolher_heroi(rng, lg, material, historico, memoria):
    usados = [r.get("heroi") for r in reversed(historico)][:memoria["heroi"]]
    possiveis = [h for h in lg.get("heroi", []) if not falta_material(h.get("precisa", []), material)]
    if not possiveis:
        return None, "nenhum herói desta linguagem cabe no material"
    livres = [h for h in possiveis if h["id"] not in usados]
    if livres:
        return livres[rng.randrange(len(livres))], None
    # todos repetiriam: fica o usado há mais tempo, com aviso
    antigo = max(possiveis, key=lambda h: usados.index(h["id"]) if h["id"] in usados else 99)
    return antigo, "todos os heróis desta linguagem estão nos últimos %d reels; ficou o mais antigo" % memoria["heroi"]


def escolher_trilha(rng, lg, trilhas, historico, memoria):
    usadas = {r.get("trilha") for r in list(reversed(historico))[:memoria["trilha"]] if r.get("trilha")}
    climas = [sem_acento(c) for c in lg.get("trilha", {}).get("climas", [])]
    no_clima = [t for t in trilhas if any(sem_acento(t).startswith(c + "-") or c in sem_acento(t) for c in climas)]
    livres = [t for t in no_clima if t not in usadas]
    if not livres:
        return None, [], ("nenhuma trilha nova no clima %s (as do clima estão nos últimos %d reels ou não existem): "
                          "procure com componentes/trilhas/buscar-trilha.py" % (" ou ".join(climas), memoria["trilha"]))
    escolhida = livres[rng.randrange(len(livres))]
    return escolhida, [t for t in livres if t != escolhida][:2], None


def escolher_convidada(rng, tabela, base_id, material):
    possiveis = []
    for lid, eixo in convidadas_possiveis(tabela, base_id):
        lg = tabela["linguagens"][lid]
        if not falta_material(lg.get("precisa", []), material):
            possiveis.append((lid, eixo, float(lg.get("peso", 1.0))))
    if not possiveis:
        return None
    return sorteio_ponderado(rng, [((l, e), p) for l, e, p in possiveis])


def sugerir(args, raiz, tabela, projeto, nn, pasta, historico):
    material = ler_material(pasta, args.material)
    if args.formato and args.formato not in tabela.get("formatos", {}):
        raise Falha("--formato %s não existe (vale %s)" % (
            args.formato, ", ".join(k for k in tabela["formatos"] if not k.startswith("_"))))
    rng = random.Random(semente(projeto, nn))
    pesos, fora = pesar(tabela, material, args.assunto, args.formato, historico)
    if not pesos:
        raise Falha("nenhuma linguagem cabe neste corte (veja as de fora abaixo)", 1)
    memoria = tabela["regras"]["memoria"]
    trilhas = trilhas_disponiveis(raiz)
    restantes = list(pesos)
    opcoes = []
    while restantes and len(opcoes) < OPCOES:
        lid = sorteio_ponderado(rng, [(l, p) for l, p, _ in restantes])
        _, peso, motivos = next(x for x in restantes if x[0] == lid)
        restantes = [x for x in restantes if x[0] != lid]
        lg = tabela["linguagens"][lid]
        heroi, aviso_heroi = escolher_heroi(rng, lg, material, historico, memoria)
        trilha, outras, aviso_trilha = escolher_trilha(rng, lg, trilhas, historico, memoria)
        convidada = escolher_convidada(rng, tabela, lid, material)
        opcoes.append({
            "linguagem": lid, "nome": lg["nome"], "descricao": lg["descricao"], "quando": lg.get("quando"),
            "peso": round(peso, 3), "motivos": motivos,
            "heroi": heroi, "aviso_heroi": aviso_heroi,
            "convidada": {"linguagem": convidada[0], "nome": tabela["linguagens"][convidada[0]]["nome"], "eixo": convidada[1]} if convidada else None,
            "sons": lg.get("sons", {}).get("kit", []),
            "trilha": trilha, "outras_trilhas": outras, "aviso_trilha": aviso_trilha,
            "estilo_minimo": lg.get("estilo_minimo", []),
            "transicoes": lg["pecas"].get("transicoes", []),
        })
    # o sorteio decide quais três aparecem; entre elas, a recomendada é a de maior peso
    ordem = {o["linguagem"]: i for i, o in enumerate(opcoes)}
    opcoes.sort(key=lambda o: (-o["peso"], ordem[o["linguagem"]]))
    resultado = {"projeto": projeto.name, "corte": nn, "semente": "%s|%s" % (projeto.name, nn),
                 "assunto": args.assunto, "formato": args.formato,
                 "material": {k: v for k, v in material.items() if k != "notas"}, "notas_material": material["notas"],
                 "historico": [{"linguagem": r.get("linguagem"), "heroi": r.get("heroi"), "trilha": r.get("trilha"),
                                "data": r.get("data")} for r in historico[-6:]],
                 "opcoes": opcoes, "fora": [{"linguagem": l, "motivo": m} for l, m in fora]}
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=1))
        return 0

    print("")
    print("  linguagem do episódio  ·  corte-%s  ·  %s" % (nn, curto(projeto, raiz)))
    print("")
    sim = lambda v: "sim" if v else "não"
    print("  material   visão %s · profundidade %s · mãos %s · rosto %s%s"
          % (sim(material["visao"]), sim(material["profundidade"]), sim(material["maos"]), sim(material["rosto"]),
             " · gravação de tela" if material["gravacao-de-tela"] else ""))
    for n in material["notas"]:
        print("             %s" % n)
    if args.assunto or args.formato:
        print("  pedido     %s%s" % (('assunto "%s"' % args.assunto) if args.assunto else "",
                                     ("%sformato %s" % (" · " if args.assunto else "", args.formato)) if args.formato else ""))
    if historico:
        print("  memória    " + " · ".join("%s (%s)" % (r.get("linguagem"), r.get("data", "?")) for r in historico[-4:][::-1]))
    else:
        print("  memória    histórico vazio: nada a evitar ainda")
    print("")
    for i, o in enumerate(opcoes, start=1):
        print("  %d. %s%s" % (i, o["nome"], "  (recomendada)" if i == 1 else ""))
        print("     %s" % o["descricao"])
        if o["motivos"]:
            print("     por quê: %s" % "; ".join(o["motivos"]))
        if o["heroi"]:
            print("     herói: %s · %s%s" % (o["heroi"]["id"], o["heroi"]["descricao"],
                                             ("  (%s)" % o["aviso_heroi"]) if o["aviso_heroi"] else ""))
        elif o["aviso_heroi"]:
            print("     herói: %s" % o["aviso_heroi"])
        if o["convidada"]:
            print("     convidada possível: %s (muda só o eixo %s), em 1 ou 2 cenas" % (o["convidada"]["nome"], o["convidada"]["eixo"]))
        else:
            print("     convidada: nenhuma compatível com o material (a linguagem vai sozinha)")
        print("     transições: %s · sons: %s" % (", ".join(o["transicoes"]), ", ".join(o["sons"])))
        if o["trilha"]:
            print("     trilha sugerida: %s%s (a decisão é sua)" % (
                o["trilha"], ("; ou " + ", ".join(o["outras_trilhas"])) if o["outras_trilhas"] else ""))
        else:
            print("     trilha: %s" % o["aviso_trilha"])
        print("     estilo de produção mínimo: %s" % " ou ".join(o["estilo_minimo"]))
        print("")
    if fora:
        print("  fora desta vez: " + "; ".join("%s (%s)" % (l, m) for l, m in fora))
        print("")
    print("  semente: %s|%s  (o mesmo corte sorteia sempre o mesmo)" % (projeto.name, nn))
    print("")
    return 0


# ---------------------------------------------------------------------------
# registrar
# ---------------------------------------------------------------------------

def linguagem_do_plano(cenas):
    """(base, convidada) do cenas.json: "linguagem": "x" ou {"base": "x", "convidada": "y"}."""
    valor = cenas.get("linguagem") if isinstance(cenas, dict) else None
    if isinstance(valor, str):
        return valor.strip() or None, None
    if isinstance(valor, dict):
        return (valor.get("base") or None), (valor.get("convidada") or None)
    return None, None


def heroi_do_plano(cenas):
    """[(t, nome, onde)] de todo momento-herói declarado no plano."""
    achados = []
    h = cenas.get("heroi") if isinstance(cenas, dict) else None
    if isinstance(h, dict) and isinstance(h.get("t"), (int, float)):
        achados.append((float(h["t"]), h.get("nome"), "heroi"))
    for cena in cenas.get("cenas", []) if isinstance(cenas, dict) else []:
        if not isinstance(cena, dict):
            continue
        if cena.get("heroi") is True and isinstance(cena.get("inicio"), (int, float)):
            achados.append((float(cena["inicio"]), None, "cena %s" % cena.get("id")))
        for item in cena.get("sobre") or []:
            if isinstance(item, dict) and item.get("heroi") is True and isinstance(item.get("t"), (int, float)):
                achados.append((float(item["t"]), None, "cena %s, %s" % (cena.get("id"), item.get("tipo"))))
    return achados


def registrar(args, raiz, tabela, projeto, nn, pasta, caminho_hist, historico):
    cenas = ler_json(pasta / "cenas.json", "o plano") or {}
    base_plano, convidada_plano = linguagem_do_plano(cenas)
    lid = args.linguagem or base_plano
    if not lid:
        raise Falha("diga a linguagem: --linguagem <nome>, ou declare \"linguagem\" no cenas.json")
    if lid not in tabela["linguagens"]:
        raise Falha("linguagem desconhecida: %s (vale %s)" % (lid, ", ".join(sorted(tabela["linguagens"]))))
    convidada = args.convidada or convidada_plano
    avisos = []
    if convidada:
        if convidada not in tabela["linguagens"] or convidada == lid:
            raise Falha("convidada inválida: %s" % convidada)
        if convidada not in [c for c, _ in convidadas_possiveis(tabela, lid)]:
            avisos.append("%s não é convidada compatível com %s (um eixo só, sem par proibido)" % (convidada, lid))
    heroi = args.heroi
    if not heroi:
        achados = heroi_do_plano(cenas)
        heroi = next((n for _, n, _ in achados if n), None)
    ids = [h["id"] for h in tabela["linguagens"][lid].get("heroi", [])]
    if heroi and heroi not in ids:
        avisos.append("o herói %s não é um dos da linguagem %s (%s); ficou registrado assim mesmo" % (heroi, lid, ", ".join(ids)))
    trilha = nome_da_trilha(args.trilha) if args.trilha else nome_da_trilha(cenas.get("trilha"))
    data = args.data or date.today().isoformat()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", data):
        raise Falha("--data no formato AAAA-MM-DD (recebi %s)" % data)
    registro = {"projeto": projeto.name, "corte": nn, "linguagem": lid, "convidada": convidada,
                "heroi": heroi, "trilha": trilha, "data": data}
    # o mesmo corte registrado de novo fica no lugar dele; um corte novo entra no fim (o mais recente)
    mesmo = [i for i, r in enumerate(historico) if r.get("projeto") == projeto.name and r.get("corte") == nn]
    if mesmo:
        reels = [r for i, r in enumerate(historico) if i not in mesmo[1:]]
        reels[mesmo[0]] = registro
    else:
        reels = historico + [registro]
    tamanho = tabela["regras"]["memoria"]["historico"]
    gravar_historico(caminho_hist, reels, tamanho)
    print("")
    print("  registrado em %s" % curto(caminho_hist, raiz))
    print("    corte-%s · %s%s · herói %s · trilha %s · %s"
          % (nn, lid, (" + " + convidada) if convidada else "", heroi or "(nenhum)", trilha or "(sem trilha)", data))
    if mesmo:
        print("    (o registro anterior deste corte foi substituído no mesmo lugar)")
    for a in avisos:
        print("  olhe  " + a)
    print("  o histórico guarda os últimos %d reels; agora tem %d" % (tamanho, min(tamanho, len(reels))))
    print("")
    return 0


# ---------------------------------------------------------------------------
# conferir
# ---------------------------------------------------------------------------

def pecas_do_plano(cenas):
    """O que o plano usa, cena a cena: {cena: {modos, sobre, look, palavra, transicoes, legenda}}."""
    def vazio():
        return {"modos": set(), "sobre": set(), "look": set(), "palavra": set(), "transicoes": set(), "legenda": set(),
                "pos": set()}

    def ler_sobre(itens, alvo):
        for item in itens or []:
            if not isinstance(item, dict) or not item.get("tipo"):
                continue
            alvo["sobre"].add(item["tipo"])
            if item["tipo"] == "look":
                alvo["look"].add(item.get("efeito") or "?")
            elif item["tipo"] == "palavra":
                alvo["palavra"].add(item.get("efeito") or "glitch")

    def ler_pos(itens, alvo):
        # o pós no quadro inteiro (4.3): "pos": [{"efeito": ...}] no topo ou na cena
        for item in itens or []:
            if isinstance(item, dict) and item.get("efeito"):
                alvo["pos"].add(item["efeito"])

    uso = {}
    reel = vazio()
    ler_sobre(cenas.get("sobre"), reel)
    ler_pos(cenas.get("pos"), reel)
    leg = cenas.get("legenda")
    if isinstance(leg, dict) and leg.get("estilo"):
        reel["legenda"].add(leg["estilo"])
    uso["(reel)"] = reel
    for cena in cenas.get("cenas", []):
        if not isinstance(cena, dict):
            continue
        u = vazio()
        if cena.get("modo"):
            u["modos"].add(cena["modo"])
        entrada = cena.get("entrada")
        if isinstance(entrada, dict) and entrada.get("transicao"):
            u["transicoes"].add(entrada["transicao"])
        ler_sobre(cena.get("sobre"), u)
        ler_pos(cena.get("pos"), u)
        if isinstance(cena.get("legenda"), dict) and cena["legenda"].get("estilo"):
            u["legenda"].add(cena["legenda"]["estilo"])
        uso[str(cena.get("id"))] = u
    return uso


def permitido(tabela, lid):
    lg = tabela["linguagens"][lid]
    p = lg["pecas"]
    return {"modos": set(p.get("modos", [])), "sobre": set(p.get("sobre", [])), "look": set(p.get("look", [])),
            "palavra": set(p.get("palavra", [])), "transicoes": set(p.get("transicoes", [])),
            "pos": set(p.get("pos", [])),
            "legenda": {lg.get("legenda", {}).get("estilo")} - {None}}


def requisitos_da_peca(tabela, categoria, nome):
    return tabela.get("requisitos", {}).get(categoria, {}).get(nome, [])


def avaliar(raiz, tabela, pasta):
    """A conferência do plano da pasta do corte contra a linguagem dele, sem imprimir nada.

    Devolve o dicionário do --json: linguagem, convidada, duracao, fora, transicoes, heroi, sons e as
    listas "problemas" (reprova), "avisos" (olhe) e "linhas" (o que conferiu). Levanta Falha quando o
    plano falta ou nomeia linguagem que não existe. É o que o gate de linguagem do conferir_reel.py
    importa, para as duas conferências nunca divergirem.
    """
    caminho = pasta / "cenas.json"
    cenas = ler_json(caminho, "o plano")
    if not isinstance(cenas, dict) or not isinstance(cenas.get("cenas"), list):
        raise Falha("não achei o plano %s (ou ele não tem a lista \"cenas\")" % curto(caminho, raiz))
    base, convidada = linguagem_do_plano(cenas)
    problemas, avisos, linhas = [], [], []
    if not base:
        problemas.append("o cenas.json não declara a linguagem: ponha \"linguagem\": \"<nome>\" no topo "
                         "(as opções saem do linguagem.py sugerir)")
    elif base not in tabela["linguagens"]:
        raise Falha("linguagem desconhecida no cenas.json: %s (vale %s)" % (base, ", ".join(sorted(tabela["linguagens"]))))
    if convidada and convidada not in tabela["linguagens"]:
        raise Falha("convidada desconhecida no cenas.json: %s" % convidada)
    material = ler_material(pasta, None)
    uso = pecas_do_plano(cenas)
    duracao = cenas.get("duracao")
    if not isinstance(duracao, (int, float)):
        fins = [c.get("fim") for c in cenas["cenas"] if isinstance(c, dict) and isinstance(c.get("fim"), (int, float))]
        duracao = max(fins) if fins else None
    resultado = {"linguagem": base, "convidada": convidada, "duracao": duracao}

    if base:
        lg = tabela["linguagens"][base]
        sempre = tabela["sempre"]
        livre = {"modos": set(sempre["modos"]), "sobre": set(sempre["sobre"]), "look": set(), "palavra": set(),
                 "transicoes": set(sempre["transicoes"]), "legenda": set(sempre["legenda"]) | {"palavra-acesa", "pop", "caixa"},
                 "pos": set(sempre.get("pos", []))}
        da_base = permitido(tabela, base)
        da_convidada = permitido(tabela, convidada) if convidada else {k: set() for k in da_base}
        if convidada:
            if convidada == base:
                problemas.append("a convidada é a própria base")
            elif par_proibido(tabela, base, convidada):
                problemas.append("%s + %s é par proibido" % (base, convidada))
            elif eixos_diferentes(lg, tabela["linguagens"][convidada]) != tabela["regras"]["convidada_eixos_diferentes"]:
                problemas.append("%s e %s diferem em %d eixos; a convidada difere da base em exatamente 1"
                                 % (base, convidada, eixos_diferentes(lg, tabela["linguagens"][convidada])))
        fora, cenas_convidada, falta = [], [], []
        for cena_id, u in uso.items():
            usou_convidada = False
            for cat, nomes in u.items():
                for nome in sorted(nomes):
                    if nome in livre[cat] or nome in da_base[cat]:
                        pass
                    elif nome in da_convidada[cat]:
                        usou_convidada = True
                    elif cat == "legenda":
                        pass                      # os estilos de legenda do motor valem em toda linguagem
                    else:
                        fora.append((cena_id, cat, nome))
                    if cat in ("modos", "sobre"):
                        req = falta_material(requisitos_da_peca(tabela, cat, nome), material)
                        if req:
                            falta.append((cena_id, nome, req))
            if usou_convidada and cena_id != "(reel)":
                cenas_convidada.append(cena_id)
        rotulo = {"modos": "modo", "sobre": "sobreposição", "look": "look", "palavra": "palavra",
                  "transicoes": "transição", "pos": "pós"}
        for cena_id, cat, nome in fora:
            problemas.append("%s: %s \"%s\" não é da linguagem %s%s"
                             % (cena_id, rotulo.get(cat, cat), nome, base, (" nem da convidada " + convidada) if convidada else ""))
        maximo = tabela["regras"]["convidada_cenas_max"]
        if len(cenas_convidada) > maximo:
            problemas.append("a convidada %s aparece em %d cenas (%s); o máximo é %d"
                             % (convidada, len(cenas_convidada), ", ".join(cenas_convidada), maximo))
        for cena_id, nome, req in falta:
            problemas.append("%s: %s pede %s, que este corte não tem" % (cena_id, nome, " e ".join(req)))
        transicoes = sorted({t for u in uso.values() for t in u["transicoes"]} - {"corte"})
        if len(transicoes) > tabela["regras"]["familias_transicao_max"]:
            problemas.append("%d famílias de transição (%s); o máximo é %d"
                             % (len(transicoes), ", ".join(transicoes), tabela["regras"]["familias_transicao_max"]))
        linhas.append("transições: %s" % (", ".join(transicoes) or "só corte seco"))
        estilo = cenas.get("estilo")
        estilos = [estilo] if isinstance(estilo, str) else list(estilo or [])
        # o completo e o motion (o estilo da 4.0, superconjunto dos outros) atendem qualquer estilo mínimo
        if estilos and not (set(estilos) & set(lg.get("estilo_minimo", [])) or {"completo", "motion"} & set(estilos)):
            avisos.append("o estilo de produção %s é menos do que a linguagem pede (%s)"
                          % (", ".join(estilos), " ou ".join(lg.get("estilo_minimo", []))))
        resultado.update({"fora": [{"cena": c, "categoria": k, "peca": n} for c, k, n in fora],
                          "cenas_da_convidada": cenas_convidada, "transicoes": transicoes})

        # o momento-herói
        achados = heroi_do_plano(cenas)
        faixa = tabela["regras"]["heroi"]["faixa"]
        ids = [h["id"] for h in lg.get("heroi", [])] + ([h["id"] for h in tabela["linguagens"][convidada].get("heroi", [])] if convidada else [])
        resultado["heroi"] = [{"t": t, "nome": n, "onde": o, "fracao": (t / duracao) if duracao else None} for t, n, o in achados]
        if not achados:
            problemas.append("nenhum momento-herói declarado: ponha \"heroi\": {\"t\": <s>, \"nome\": \"<id>\"} no topo "
                             "(candidatos de %s: %s)" % (base, ", ".join(ids)))
            eventos = ler_json(pasta / "eventos.json", "os eventos") or {}
            if duracao:
                fortes = [e for e in eventos.get("eventos", []) if isinstance(e, dict) and e.get("peso") == 3
                          and faixa[0] * duracao <= float(e.get("t", -1)) <= faixa[1] * duracao]
                if fortes:
                    linhas.append("eventos de peso 3 na faixa do herói (%s a %s s): %s" % (
                        virgula(faixa[0] * duracao), virgula(faixa[1] * duracao),
                        ", ".join("%s s %s" % (virgula(float(e["t"]), 2), e.get("alvo")) for e in fortes[:6])))
        for t, n, onde in achados:
            if not duracao:
                avisos.append("sem duração no plano: não deu para medir a posição do herói")
                break
            f = t / duracao
            texto = "herói %s em %s s = %d%% da duração (%s)" % (n or "", virgula(t, 2), round(100 * f), onde)
            if faixa[0] <= f <= faixa[1]:
                linhas.append(texto + ", dentro da faixa de %d%% a %d%%" % (100 * faixa[0], 100 * faixa[1]))
            else:
                problemas.append(texto + ", fora da faixa de %d%% a %d%% (%s a %s s)"
                                 % (100 * faixa[0], 100 * faixa[1], virgula(faixa[0] * duracao), virgula(faixa[1] * duracao)))
            if n and n not in ids:
                avisos.append("o herói %s não é um dos da linguagem (%s)" % (n, ", ".join(ids)))
        if len(achados) > tabela["regras"]["heroi"]["aparicoes_max"]:
            problemas.append("%d momentos-herói declarados; o máximo é %d" % (len(achados), tabela["regras"]["heroi"]["aparicoes_max"]))

        # os sons, se o compor.py já rodou
        eventos = ler_json(pasta / "eventos.json", "os eventos")
        if isinstance(eventos, dict):
            kit = set(lg.get("sons", {}).get("kit", [])) | set(tabela["sempre"]["sons"])
            if convidada:
                kit |= set(tabela["linguagens"][convidada].get("sons", {}).get("kit", []))
            usados = {}
            for e in eventos.get("eventos", []):
                if isinstance(e, dict) and e.get("som"):
                    familia = re.sub(r"-\d+$", "", str(e["som"]))
                    usados[familia] = usados.get(familia, 0) + 1
            alheios = sorted(f for f in usados if f not in kit)
            linhas.append("sons pedidos: %s" % (", ".join("%s %d" % (f, n) for f, n in sorted(usados.items())) or "nenhum"))
            if alheios:
                avisos.append("sons fora do kit de %s: %s (kit: %s)" % (base, ", ".join(alheios), ", ".join(sorted(kit))))
            resultado["sons"] = usados

    resultado.update({"problemas": problemas, "avisos": avisos, "linhas": linhas})
    return resultado


def conferir(args, raiz, tabela, projeto, nn, pasta):
    caminho = pasta / "cenas.json"
    resultado = avaliar(raiz, tabela, pasta)
    base, convidada = resultado["linguagem"], resultado["convidada"]
    problemas, avisos, linhas = resultado["problemas"], resultado["avisos"], resultado["linhas"]
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=1, default=list))
        return 1 if problemas else 0
    print("")
    print("  conferência da linguagem  ·  corte-%s  ·  %s" % (nn, curto(caminho, raiz)))
    print("")
    if base:
        print("  linguagem  %s%s" % (base, (" + convidada " + convidada) if convidada else ""))
    for l in linhas:
        print("  ok    " + l)
    for a in avisos:
        print("  olhe  " + a)
    for p in problemas:
        print("  --    " + p)
    print("")
    if problemas:
        print("  REPROVADO: %d problema(s)" % len(problemas))
        print("")
        return 1
    print("  PASSOU: as peças batem com a linguagem e o herói está na faixa")
    print("")
    return 0


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="A linguagem do episódio: sugerir, registrar e conferir.")
    sub = ap.add_subparsers(dest="comando", required=True)
    comum = argparse.ArgumentParser(add_help=False)
    comum.add_argument("--projeto", required=True, help="a pasta do vídeo, por exemplo projetos/meu-video")
    comum.add_argument("--corte", required=True, help="o número do corte: 01, 1 ou corte-01")
    comum.add_argument("--historico", help="outro arquivo de histórico (padrão: projetos/.historico-linguagens.json)")
    s = sub.add_parser("sugerir", parents=[comum], help="sorteia 3 linguagens para o corte, a primeira recomendada")
    s.add_argument("--assunto", help="o assunto do reel, em texto livre (puxa as linguagens que combinam)")
    s.add_argument("--formato", help="o formato da série: noticia, ferramenta, tutorial, opiniao, lista, teste")
    s.add_argument("--material", choices=["pessoa", "tela"], help="tela = gravação de tela (padrão: lê a visão do corte)")
    s.add_argument("--json", action="store_true", help="imprime em JSON")
    r = sub.add_parser("registrar", parents=[comum], help="grava a escolha do corte no histórico")
    r.add_argument("--linguagem", help="a linguagem base (padrão: a do cenas.json)")
    r.add_argument("--convidada", help="a convidada, se houver")
    r.add_argument("--heroi", help="o id do momento-herói (padrão: o do cenas.json)")
    r.add_argument("--trilha", help="o arquivo da trilha (padrão: a do cenas.json)")
    r.add_argument("--data", help="AAAA-MM-DD (padrão: hoje)")
    c = sub.add_parser("conferir", parents=[comum], help="confere o cenas.json contra a linguagem declarada")
    c.add_argument("--json", action="store_true", help="imprime em JSON")
    args = ap.parse_args()

    try:
        raiz = achar_raiz()
        tabela = carregar_tabela()
        projeto = resolver_projeto(raiz, args.projeto)
        if projeto is None:
            raise Falha("não achei a pasta do projeto %s" % args.projeto)
        nn = nome_do_corte(args.corte)
        if nn is None:
            raise Falha("--corte é o número do corte, como 01 ou 1 (recebi %r)" % args.corte)
        pasta = projeto / "materiais-de-trabalho" / ("corte-%s" % nn)
        if not pasta.is_dir():
            raise Falha("não achei a pasta do corte %s" % curto(pasta, raiz))
        caminho_hist = caminho_do_historico(raiz, args.historico)
        if args.comando == "sugerir":
            return sugerir(args, raiz, tabela, projeto, nn, pasta, ler_historico(caminho_hist))
        if args.comando == "registrar":
            return registrar(args, raiz, tabela, projeto, nn, pasta, caminho_hist, ler_historico(caminho_hist))
        return conferir(args, raiz, tabela, projeto, nn, pasta)
    except Falha as e:
        erro(str(e))
        return e.codigo
    except OSError as e:
        erro(str(e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
