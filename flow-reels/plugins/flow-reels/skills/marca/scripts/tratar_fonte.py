# -*- coding: utf-8 -*-
"""
tratar_fonte.py
Recebe um arquivo de fonte (.ttf ou .otf), descobre se ele é uma fonte variável
e, se for, gera as instâncias estáticas nos pesos pedidos.

Por que isso existe
-------------------
O queimador de legenda do ffmpeg (libass) NÃO entende o eixo de peso de uma
fonte variável. Ele abre o arquivo e desenha no peso padrão da fonte, que na
maioria das famílias modernas é Light ou Regular. O resultado é uma legenda fina
sobre vídeo, que some na compressão da plataforma. A correção é sempre a mesma:
gerar um arquivo estático no peso desejado e apontar os tokens para ele.

O script imprime, em JSON, os arquivos gerados e o nome de família REAL de cada
um. Esse nome é o que importa: é ele que vai no campo fontes.legenda.familia de
marca/tokens.json e é por ele que a legenda encontra a fonte. Chutar o nome é a
causa número um de legenda que sai na fonte errada.

Uso:
    flow-reels marca/tratar_fonte <arquivo.ttf> [--pesos 700,500] [--saida <pasta>] [--json]

    --pesos   lista separada por vírgula (padrão: 700,500)
    --saida   pasta onde gravar as estáticas (padrão: a pasta do arquivo de entrada)
    --json    imprime só o JSON

Depende de fontTools.
"""

import json
import shutil
import sys
from pathlib import Path

# O terminal do Windows nao nasce em UTF-8, e sem isto todo acento sai quebrado.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


try:
    from fontTools.ttLib import TTFont
except ImportError:
    print(
        "Falta a biblioteca fontTools. Instale com: pip install fonttools",
        file=sys.stderr,
    )
    sys.exit(2)


SUFIXO_POR_PESO = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
    800: "ExtraBold",
    900: "Black",
}


def ler_nome(fonte, ids):
    """Devolve o primeiro nome disponível entre os ids pedidos."""
    tabela = fonte["name"]
    for identificador in ids:
        registro = tabela.getDebugName(identificador)
        if registro:
            return registro
    return None


def descrever(caminho):
    """Abre a fonte e conta o que ela é, sem alterar nada."""
    fonte = TTFont(str(caminho), lazy=True)
    variavel = "fvar" in fonte
    eixos = {}
    if variavel:
        for eixo in fonte["fvar"].axes:
            eixos[eixo.axisTag] = {
                "minimo": eixo.minValue,
                "padrao": eixo.defaultValue,
                "maximo": eixo.maxValue,
            }
    peso_declarado = None
    if "OS/2" in fonte:
        peso_declarado = int(getattr(fonte["OS/2"], "usWeightClass", 400) or 400)

    dados = {
        "arquivo": str(Path(caminho).resolve()),
        "variavel": variavel,
        "eixos": eixos,
        "peso_declarado": peso_declarado,
        "familia": ler_nome(fonte, [16, 1]),
        "familia_nome_id_1": ler_nome(fonte, [1]),
        "subfamilia": ler_nome(fonte, [2]),
        "nome_completo": ler_nome(fonte, [4]),
    }
    if variavel and "wght" in eixos:
        dados["peso_padrao"] = eixos["wght"]["padrao"]
        dados["alerta_peso_padrao"] = (
            "A legenda sairia no peso {}, que é o padrão desta fonte variável. "
            "Por isso geramos as estáticas.".format(int(eixos["wght"]["padrao"]))
        )
    fonte.close()
    return dados


def gerar_estatica(caminho, peso, pasta_saida):
    """Gera uma instância estática no peso pedido e devolve o que foi gravado."""
    from fontTools.varLib import instancer

    fonte = TTFont(str(caminho))
    eixos = {eixo.axisTag: eixo for eixo in fonte["fvar"].axes}
    if "wght" not in eixos:
        fonte.close()
        raise ValueError(
            "Esta fonte variável não tem eixo de peso (wght). "
            "Não dá para gerar instância por peso."
        )

    eixo = eixos["wght"]
    alvo = max(eixo.minValue, min(eixo.maxValue, float(peso)))
    ajustado = alvo != float(peso)

    # updateFontNames é o que faz a instância se apresentar com o nome certo.
    # Sem ele, as estáticas saem todas chamando a mesma coisa e o libass pega
    # qualquer uma delas.
    estatica = instancer.instantiateVariableFont(
        fonte, {"wght": alvo}, updateFontNames=True, inplace=False
    )

    base = Path(caminho).stem.replace("[wght]", "").replace("-VariableFont", "").strip("-_ ")
    sufixo = SUFIXO_POR_PESO.get(int(alvo), str(int(alvo)))
    destino = Path(pasta_saida) / "{}-{}.ttf".format(base, sufixo)
    destino.parent.mkdir(parents=True, exist_ok=True)
    estatica.save(str(destino))

    gerada = TTFont(str(destino), lazy=True)
    familia_1 = ler_nome(gerada, [1])
    familia_16 = ler_nome(gerada, [16])
    subfamilia = ler_nome(gerada, [2])
    nome_completo = ler_nome(gerada, [4])
    gerada.close()
    estatica.close()
    fonte.close()

    return {
        "peso_pedido": int(peso),
        "peso_gerado": int(alvo),
        "peso_ajustado": ajustado,
        "arquivo": str(destino.resolve()),
        "nome_do_arquivo": destino.name,
        "familia_para_usar": familia_1,
        "familia_tipografica": familia_16,
        "subfamilia": subfamilia,
        "nome_completo": nome_completo,
        "negrito_no_ass": (subfamilia or "").lower() in ("bold", "bold italic"),
    }


def tratar(caminho, pesos, pasta_saida):
    caminho = Path(caminho)
    pasta_saida = Path(pasta_saida or caminho.parent)
    info = descrever(caminho)
    resultado = {
        "entrada": info,
        "gerou_estaticas": False,
        "estaticas": [],
        "avisos": [],
        "para_os_tokens": None,
    }

    if not info["variavel"]:
        # Fonte já estática: nada a gerar, só copiar se o destino for outro lugar
        destino = pasta_saida / caminho.name
        if destino.resolve() != caminho.resolve():
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(caminho, destino)
        resultado["estaticas"].append(
            {
                "peso_pedido": info["peso_declarado"],
                "peso_gerado": info["peso_declarado"],
                "peso_ajustado": False,
                "arquivo": str(destino.resolve()),
                "nome_do_arquivo": destino.name,
                "familia_para_usar": info["familia_nome_id_1"] or info["familia"],
                "familia_tipografica": info["familia"],
                "subfamilia": info["subfamilia"],
                "nome_completo": info["nome_completo"],
                "negrito_no_ass": (info["subfamilia"] or "").lower() in ("bold", "bold italic"),
            }
        )
        resultado["avisos"].append(
            "Esta fonte já é estática. Nada foi gerado, o arquivo serve como está."
        )
    else:
        resultado["gerou_estaticas"] = True
        for peso in pesos:
            try:
                resultado["estaticas"].append(gerar_estatica(caminho, peso, pasta_saida))
            except Exception as erro:
                resultado["avisos"].append(
                    "Não consegui gerar o peso {}: {}".format(peso, erro)
                )
        for e in [x for x in resultado["estaticas"] if x["peso_ajustado"]]:
            resultado["avisos"].append(
                "O peso {} não existe nesta fonte. Gerei no peso {}, que é o mais "
                "próximo dentro do eixo.".format(e["peso_pedido"], e["peso_gerado"])
            )

    # O atalho para quem vai preencher os tokens: o peso mais pesado vira título
    # e legenda, o mais leve vira corpo.
    disponiveis = [e for e in resultado["estaticas"] if e.get("arquivo")]
    if disponiveis:
        mais_pesada = max(disponiveis, key=lambda e: e["peso_gerado"] or 0)
        mais_leve = min(disponiveis, key=lambda e: e["peso_gerado"] or 0)
        resultado["para_os_tokens"] = {
            "titulo": {
                "familia": mais_pesada["familia_para_usar"],
                "arquivo": mais_pesada["nome_do_arquivo"],
                "peso": mais_pesada["peso_gerado"],
                "variavel": False,
            },
            "corpo": {
                "familia": mais_leve["familia_para_usar"],
                "arquivo": mais_leve["nome_do_arquivo"],
                "peso": mais_leve["peso_gerado"],
                "variavel": False,
            },
            "legenda": {
                "familia": mais_pesada["familia_para_usar"],
                "arquivo": mais_pesada["nome_do_arquivo"],
                "peso": mais_pesada["peso_gerado"],
                "variavel": False,
                "negrito_no_ass": mais_pesada["negrito_no_ass"],
            },
            "_nota": (
                "O campo arquivo aqui é só o nome. Complete com a pasta onde a fonte "
                "ficou, relativa à raiz do pacote, por exemplo marca/fontes/<nome>. "
                "Quando negrito_no_ass vier true, a legenda precisa nascer com Bold "
                "ligado, porque o nome de família dessa estática é o da família inteira."
            ),
        }
    return resultado


def resumo(r):
    linhas = []
    entrada = r["entrada"]
    linhas.append("Fonte: {}".format(entrada["arquivo"]))
    linhas.append("Família declarada: {}".format(entrada["familia"]))
    if entrada["variavel"]:
        eixos = ", ".join(
            "{} de {} a {} (padrão {})".format(
                tag, v["minimo"], v["maximo"], v["padrao"]
            )
            for tag, v in entrada["eixos"].items()
        )
        linhas.append("É VARIÁVEL. Eixos: {}".format(eixos))
        if "alerta_peso_padrao" in entrada:
            linhas.append("Atenção: " + entrada["alerta_peso_padrao"])
    else:
        linhas.append("É estática. Pode ir direto para a legenda.")
    for e in r["estaticas"]:
        linhas.append(
            "  -> {}  família para usar: \"{}\"  (peso {}{})".format(
                e["nome_do_arquivo"],
                e["familia_para_usar"],
                e["peso_gerado"],
                ", com Bold ligado no ASS" if e["negrito_no_ass"] else "",
            )
        )
    for aviso in r["avisos"]:
        linhas.append("AVISO: " + aviso)
    return "\n".join(linhas)


def main():
    argumentos = sys.argv[1:]
    pediu_ajuda = bool(argumentos) and argumentos[0] in ("-h", "--ajuda", "--help")
    # Pedir ajuda nao e erro: sai por stdout e com codigo 0. Rodar sem argumento
    # nenhum e erro de uso, e ai a mesma ajuda sai por stderr e com codigo 1.
    if pediu_ajuda or not argumentos:
        print(
            "Uso: flow-reels marca/tratar_fonte <arquivo.ttf> [--pesos 700,500] [--saida <pasta>] [--json]\n"
            "\n"
            "Descobre se a fonte é variável e, se for, gera as instâncias estáticas\n"
            "nos pesos pedidos. Imprime os arquivos gerados e o nome de família real\n"
            "de cada um, que é o nome que vai em marca/tokens.json.",
            file=sys.stdout if pediu_ajuda else sys.stderr,
        )
        sys.exit(0 if pediu_ajuda else 1)

    caminho = Path(argumentos[0])
    if not caminho.exists():
        print("Não encontrei o arquivo: {}".format(caminho), file=sys.stderr)
        sys.exit(1)
    if caminho.suffix.lower() not in (".ttf", ".otf"):
        print(
            "Formato não suportado: {}. Use .ttf ou .otf.".format(caminho.suffix),
            file=sys.stderr,
        )
        sys.exit(1)

    pesos = [700, 500]
    if "--pesos" in argumentos:
        try:
            bruto = argumentos[argumentos.index("--pesos") + 1]
            pesos = [int(p.strip()) for p in bruto.split(",") if p.strip()]
        except (IndexError, ValueError):
            print(
                "O valor de --pesos precisa ser uma lista de números, por exemplo 700,500.",
                file=sys.stderr,
            )
            sys.exit(1)

    saida = None
    if "--saida" in argumentos:
        try:
            saida = argumentos[argumentos.index("--saida") + 1]
        except IndexError:
            print("Faltou a pasta depois de --saida.", file=sys.stderr)
            sys.exit(1)

    try:
        resultado = tratar(caminho, pesos, saida)
    except Exception as erro:
        print("Não consegui tratar esta fonte: {}".format(erro), file=sys.stderr)
        sys.exit(1)

    if "--json" not in argumentos:
        print(resumo(resultado))
        print()
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
