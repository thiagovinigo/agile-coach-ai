#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
baixar-logo.py  ·  traz o logo de verdade para o acervo

Marca so entra no painel como a marca de verdade. Desenhar uma forma parecida
com o logo do Claude, do Instagram ou de quem quer que seja e pior do que nao
mostrar nada: quem conhece a marca percebe o erro na hora, e quem nao conhece
aprende errado. Este script existe para que buscar o arquivo certo seja mais
facil do que improvisar um desenho.

De onde vem
-----------
Do Simple Icons (simpleicons.org), um acervo de SVG de marca publicado sob
CC0 1.0. O arquivo cru fica em um endereco previsivel:

    https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg

O script tambem le o indice do proprio Simple Icons para descobrir o slug a
partir do nome da marca, para conferir a cor oficial e para sugerir nomes
parecidos quando a marca pedida nao existe la.

Limite que voce precisa conhecer
--------------------------------
Os SVG do Simple Icons sao MONOCROMATICOS, uma silhueta de uma cor so. Isso
serve muito bem para tile, marca dagua e icone dentro do painel. Isso NAO serve
quando a cor e parte da identidade da marca e o beat depende dela. Nesse caso
baixe o logo colorido oficial na pagina de imprensa da propria marca e salve na
mao dentro desta pasta. O README.md ao lado explica como.

Uso
---
    flow-reels componentes/baixar-logo                      mostra esta ajuda e o que ja existe
    flow-reels componentes/baixar-logo --listar             so a lista do que ja existe
    flow-reels componentes/baixar-logo claude instagram     baixa uma ou mais marcas
    flow-reels componentes/baixar-logo "google drive"       nome com espaco entre aspas
    flow-reels componentes/baixar-logo notion --forcar      rebaixa por cima do que ja existe

Codigo de saida: 0 quando tudo que foi pedido chegou, 1 quando faltou alguma.
"""

import argparse
import difflib
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# o que se baixa vai para a pasta de trabalho (componentes/logos/), por cima dos logos do pacote
PASTA_PADRAO = str(fabrica.raiz() / "componentes" / "logos")
PASTA_DO_PACOTE = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_ACERVO = "_acervo.json"

ENDERECO_SVG = "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/%s.svg"
ENDERECO_INDICE = "https://cdn.jsdelivr.net/npm/simple-icons@latest/_data/simple-icons.json"
PAGINA_FONTE = "https://simpleicons.org"

TEMPO_LIMITE = 30
AGENTE = "fabrica-de-cortes/baixar-logo"

# Slug que so aceita letra minuscula, numero, ponto, hifen e sublinhado. Serve
# tambem de tranca: nome de marca nunca vira caminho de pasta.
SLUG_VALIDO = re.compile(r"^[a-z0-9._-]+$")

# O Simple Icons troca alguns simbolos por palavra antes de achatar o titulo.
TROCAS = [("+", "plus"), (".", "dot"), ("&", "and"), ("đ", "d"), ("ħ", "h"),
          ("ı", "i"), ("ĸ", "k"), ("ŀ", "l"), ("ł", "l"), ("ß", "ss"),
          ("ŧ", "t")]


# ---------------------------------------------------------------------------
# Nome da marca virando slug
# ---------------------------------------------------------------------------

def normalizar_slug(nome):
    """Aplica no nome da marca a mesma regra de slug do Simple Icons."""
    texto = (nome or "").strip().lower()
    for de, para in TROCAS:
        texto = texto.replace(de, para)
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9]", "", texto)
    return texto


def slug_do_registro(registro):
    if registro.get("slug"):
        return registro["slug"]
    return normalizar_slug(registro.get("title", ""))


def titulos_do_registro(registro):
    """Titulo mais os apelidos, que e por onde o usuario costuma chamar a marca."""
    nomes = [registro.get("title", "")]
    apelidos = registro.get("aliases") or {}
    for chave in ("aka", "dup", "old", "loc"):
        valor = apelidos.get(chave)
        if isinstance(valor, list):
            nomes.extend(v for v in valor if isinstance(v, str))
        elif isinstance(valor, dict):
            nomes.extend(v for v in valor.values() if isinstance(v, str))
        elif isinstance(valor, str):
            nomes.append(valor)
    for item in (apelidos.get("dup") or []):
        if isinstance(item, dict) and item.get("title"):
            nomes.append(item["title"])
    return [n for n in nomes if n]


# ---------------------------------------------------------------------------
# Rede
# ---------------------------------------------------------------------------

def buscar(endereco, binario=False):
    pedido = urllib.request.Request(endereco, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(pedido, timeout=TEMPO_LIMITE) as resposta:
        dados = resposta.read()
    return dados if binario else dados.decode("utf-8")


def baixar_indice():
    """Devolve a lista do Simple Icons, ou None quando a rede nao responde."""
    try:
        return json.loads(buscar(ENDERECO_INDICE))
    except urllib.error.URLError as erro:
        print("aviso: nao consegui ler o indice do Simple Icons (%s)." % erro.reason)
        print("       Sigo mesmo assim, tentando o slug direto, mas sem conferir o nome")
        print("       nem sugerir parecidos.")
        return None
    except Exception as erro:
        print("aviso: o indice do Simple Icons veio quebrado (%s). Sigo sem ele." % erro)
        return None


# ---------------------------------------------------------------------------
# Procurar a marca no indice
# ---------------------------------------------------------------------------

def procurar(nome, indice):
    """Devolve (registro, parecidos). Registro None quando a marca nao existe la."""
    if not indice:
        return None, []

    alvo_slug = normalizar_slug(nome)
    alvo_texto = (nome or "").strip().lower()

    for registro in indice:
        if slug_do_registro(registro) == alvo_slug:
            return registro, []
    for registro in indice:
        for titulo in titulos_do_registro(registro):
            if titulo.strip().lower() == alvo_texto:
                return registro, []
    for registro in indice:
        for titulo in titulos_do_registro(registro):
            if normalizar_slug(titulo) == alvo_slug:
                return registro, []

    catalogo = {}
    for registro in indice:
        catalogo[registro.get("title", "")] = slug_do_registro(registro)
    parecidos = difflib.get_close_matches(nome, list(catalogo), n=5, cutoff=0.5)
    if not parecidos:
        pedaco = alvo_slug
        parecidos = [t for t, s in catalogo.items()
                     if pedaco and (pedaco in s or s in pedaco)][:5]
    return None, [(t, catalogo[t]) for t in parecidos]


# ---------------------------------------------------------------------------
# O acervo
# ---------------------------------------------------------------------------

def caminho_acervo(pasta):
    return os.path.join(pasta, ARQUIVO_ACERVO)


def ler_acervo(pasta):
    caminho = caminho_acervo(pasta)
    if not os.path.isfile(caminho):
        return {}
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados if isinstance(dados, dict) else {}
    except Exception:
        print("aviso: o %s esta ilegivel, entao comeco um novo." % ARQUIVO_ACERVO)
        return {}


def gravar_acervo(pasta, acervo):
    with open(caminho_acervo(pasta), "w", encoding="utf-8") as arquivo:
        json.dump(acervo, arquivo, ensure_ascii=False, indent=2, sort_keys=True)
        arquivo.write("\n")


def listar_baixados(pasta):
    """Devolve [(slug, marca, cor_oficial)] do que ja esta na pasta."""
    if not os.path.isdir(pasta):
        return []
    acervo = ler_acervo(pasta)
    linhas = []
    for nome in sorted(os.listdir(pasta)):
        if not nome.lower().endswith(".svg"):
            continue
        slug = nome[:-4]
        ficha = acervo.get(slug, {})
        linhas.append((slug, ficha.get("marca", slug), ficha.get("cor_oficial", "")))
    return linhas


# ---------------------------------------------------------------------------
# Baixar de fato
# ---------------------------------------------------------------------------

def parece_svg(texto):
    return "<svg" in texto[:400].lower() and "</svg>" in texto[-400:].lower()


def baixar_um(nome, pasta, indice, forcar):
    """Baixa uma marca. Devolve True quando o arquivo certo ficou na pasta."""
    registro, parecidos = procurar(nome, indice)

    if indice is not None and registro is None:
        print("  x %s: nao existe no Simple Icons." % nome)
        if parecidos:
            print("    Parecidos que existem:")
            for titulo, slug in parecidos:
                print("      %-28s flow-reels componentes/baixar-logo %s" % (titulo, slug))
        else:
            print("    Procure o nome exato em %s." % PAGINA_FONTE)
        print("    Se a marca nao estiver la mesmo, o caminho e baixar o logo oficial na")
        print("    pagina de imprensa da propria marca e salvar o SVG nesta pasta na mao.")
        print("    Nao desenhe uma forma parecida: isso e defeito de painel.")
        return False

    slug = slug_do_registro(registro) if registro else normalizar_slug(nome)
    if not slug or not SLUG_VALIDO.match(slug):
        print("  x %s: nao consegui transformar esse nome em um slug de arquivo." % nome)
        return False

    marca = registro.get("title") if registro else nome
    destino = os.path.join(pasta, slug + ".svg")

    no_pacote = os.path.join(PASTA_DO_PACOTE, slug + ".svg")
    if not forcar and not os.path.isfile(destino) and os.path.isfile(no_pacote):
        print("  = %s ja vem no pacote como %s.svg." % (marca, slug))
        return True
    if os.path.isfile(destino) and not forcar:
        print("  = %s ja esta aqui como %s.svg. Use --forcar para rebaixar." % (marca, slug))
        return True

    try:
        conteudo = buscar(ENDERECO_SVG % slug)
    except urllib.error.HTTPError as erro:
        if erro.code == 404:
            print("  x %s: o arquivo %s.svg nao existe na fonte." % (marca, slug))
            print("    Confira o nome em %s ou baixe o logo oficial na mao." % PAGINA_FONTE)
        else:
            print("  x %s: a fonte respondeu %s." % (marca, erro.code))
        return False
    except urllib.error.URLError as erro:
        print("  x %s: nao consegui chegar na fonte (%s)." % (marca, erro.reason))
        print("    Confira a internet e rode de novo.")
        return False

    if not parece_svg(conteudo):
        print("  x %s: o que voltou nao e um SVG, entao nao gravei nada." % marca)
        return False

    os.makedirs(pasta, exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(conteudo if conteudo.endswith("\n") else conteudo + "\n")

    acervo = ler_acervo(pasta)
    ficha = {
        "marca": marca,
        "arquivo": slug + ".svg",
        "cor_oficial": "#" + registro["hex"] if registro and registro.get("hex") else "",
        "fonte": "Simple Icons (CC0 1.0)",
        "monocromatico": True
    }
    if registro and registro.get("source"):
        ficha["origem_do_desenho"] = registro["source"]
    if registro and registro.get("license", {}).get("type"):
        ficha["licenca_do_icone"] = registro["license"]["type"]
    acervo[slug] = ficha
    gravar_acervo(pasta, acervo)

    cor = ficha["cor_oficial"] or "sem cor oficial no indice"
    print("  ok %s salvo como %s.svg (silhueta de uma cor; cor oficial da marca: %s)"
          % (marca, slug, cor))
    return True


# ---------------------------------------------------------------------------
# Ajuda e listagem
# ---------------------------------------------------------------------------

def imprimir_ajuda(pasta):
    print("")
    print("baixar-logo.py  ·  traz o logo de verdade para o acervo")
    print("")
    print("Marca so aparece no painel com o logo de verdade. Nunca desenhe uma forma")
    print("parecida: quem conhece a marca ve o erro, e quem nao conhece aprende errado.")
    print("")
    print("Como usar:")
    print("  flow-reels componentes/baixar-logo                   esta ajuda e o que ja existe")
    print("  flow-reels componentes/baixar-logo --listar          so a lista do que ja existe")
    print("  flow-reels componentes/baixar-logo claude            baixa uma marca")
    print("  flow-reels componentes/baixar-logo claude notion x   baixa varias de uma vez")
    print('  flow-reels componentes/baixar-logo "google drive"    nome com espaco entre aspas')
    print("  flow-reels componentes/baixar-logo notion --forcar   rebaixa por cima do que ja existe")
    print("")
    print("Fonte: Simple Icons (%s), SVG sob CC0 1.0." % PAGINA_FONTE)
    print("Os arquivos sao MONOCROMATICOS, uma silhueta de uma cor so. Quando a cor da")
    print("marca for parte do beat, baixe o logo colorido oficial na pagina de imprensa")
    print("da marca e salve nesta pasta na mao. O README.md ao lado explica.")
    print("")
    imprimir_lista(pasta)


def imprimir_lista(pasta):
    linhas = listar_baixados(pasta)
    if not linhas:
        print("Acervo vazio em %s." % pasta)
        print("Comece por: flow-reels componentes/baixar-logo claude instagram youtube")
        return
    print("Ja estao no acervo (%d):" % len(linhas))
    print("  %-22s %-28s %s" % ("arquivo", "marca", "cor oficial"))
    for slug, marca, cor in linhas:
        print("  %-22s %-28s %s" % (slug + ".svg", marca, cor or "-"))
    print("")
    print("No painel, chame pelo slug: FC.criar(\"tile-de-logo\", { marca: \"claude\" })")


# ---------------------------------------------------------------------------

def principal(argumentos):
    analisador = argparse.ArgumentParser(add_help=False)
    analisador.add_argument("marcas", nargs="*", help="nomes de marca para baixar")
    analisador.add_argument("--pasta", default=PASTA_PADRAO,
                            help="onde salvar (padrao: componentes/logos/ da pasta de trabalho)")
    analisador.add_argument("--forcar", action="store_true",
                            help="rebaixa mesmo quando o arquivo ja existe")
    analisador.add_argument("--listar", action="store_true",
                            help="so mostra o que ja esta no acervo")
    analisador.add_argument("-h", "--help", action="store_true", dest="ajuda")
    opcoes = analisador.parse_args(argumentos)

    pasta = os.path.abspath(opcoes.pasta)

    if opcoes.ajuda or (not opcoes.marcas and not opcoes.listar):
        imprimir_ajuda(pasta)
        return 0

    if opcoes.listar and not opcoes.marcas:
        imprimir_lista(pasta)
        return 0

    print("Baixando %d marca(s) do Simple Icons para %s" % (len(opcoes.marcas), pasta))
    indice = baixar_indice()

    faltou = 0
    for nome in opcoes.marcas:
        if not baixar_um(nome, pasta, indice, opcoes.forcar):
            faltou += 1

    print("")
    if faltou:
        print("Terminou com %d marca(s) sem arquivo. Nenhum desenho aproximado foi criado," % faltou)
        print("e nenhum arquivo vazio ficou na pasta. Resolva cada uma pelo logo oficial,")
        print("ou nao mostre a marca e resolva o beat com palavra.")
        return 1
    print("Tudo que voce pediu esta na pasta.")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal(sys.argv[1:]))
