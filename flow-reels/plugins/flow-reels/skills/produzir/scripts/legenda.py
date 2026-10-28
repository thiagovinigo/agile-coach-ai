#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legenda.py  ·  o gerador de legenda do pacote

O que ele faz: le a transcricao palavra a palavra, remapeia o tempo das palavras
para a linha do tempo do corte, agrupa as palavras em grupos que cabem em UMA
linha e escreve um arquivo .ass pronto para ser queimado pelo montar.py.

O padrao da legenda esta fechado e testado sobre video real, e a lei dele vive em
referencias/PADRAO-VISUAL.md secao 6. Em resumo:

  preenchimento ESCURO, contorno BRANCO de 5, sombra 1, tamanho 116,
  uma linha so, centrada na costura entre os dois paineis (Alignment 5).

Entrada 1, a transcricao (o mesmo arquivo que a skill transcrever escreve):

    {"palavras": [{"inicio": 0.0, "fim": 0.42, "texto": "entao"}, ...]}

Entrada 2, os segmentos do corte, no formato  entrada:saida:deslocamento
(tudo em segundos, na linha do tempo do VIDEO ORIGINAL, e o deslocamento e
onde aquele trecho comeca dentro do corte ja montado):

    --segmento 12.4:19.8:0       o trecho de 12,4 a 19,8 vira o comeco do corte
    --segmento 51.0:58.2:7.4     o trecho de 51,0 a 58,2 entra aos 7,4 s

Exemplos de uso:

    flow-reels produzir/legenda --segmento 12.4:19.8:0 --segmento 51.0:58.2:7.4 \
                      --palavras projetos/<video>/materiais-de-trabalho/transcricao/palavras.json \
                      --saida projetos/<video>/materiais-de-trabalho/corte-01/legenda.ass

    flow-reels produzir/legenda --palavras projetos/<video> --tudo --saida legenda.ass

    flow-reels produzir/legenda --palavras palavras.json --tudo --saida legenda.ass \
                      --fonte "Barlow" --arquivo-fonte marca/fontes/Barlow-Bold.ttf

Sobre a fonte: passe SEMPRE um arquivo de instancia estatica. O queimador ignora
o eixo de peso de fonte variavel e renderiza no padrao dela, que costuma ser
fino, e a legenda sai magra. O arquivo tambem serve para medir a largura de
verdade de cada grupo, em vez de chutar por contagem de caractere.
"""

import argparse
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------------------
# Constantes do padrao. Mexer aqui muda a lei, entao nao mexa sem atualizar o
# PADRAO-VISUAL.md junto.
# ---------------------------------------------------------------------------

LARGURA_CANVAS = 1080
ALTURA_CANVAS = 1920
MARGEM_LATERAL = 56
LARGURA_UTIL = LARGURA_CANVAS - 2 * MARGEM_LATERAL   # 968 px

TAMANHO_PADRAO = 116
CONTORNO_PADRAO = 5
SOMBRA_PADRAO = 1
ORCAMENTO_PADRAO = 16          # caracteres por grupo, teto de seguranca
COR_PREENCHIMENTO_PADRAO = "#16151A"

PAUSA_QUEBRA = 0.45            # silencio entre palavras que fecha o grupo
FOLGA_FINAL = 0.12             # quanto o grupo pode esticar para nao piscar
DURACAO_MINIMA = 0.40          # nenhum grupo fica menos que isso na tela

PONTUACAO_FORTE = ".!?…"
PONTUACAO_FRACA = ",;:"

# As palavras de ligacao do portugues. Nenhuma delas pode terminar um grupo:
# a pessoa le "de" e fica esperando o resto, e o resto so chega no proximo grupo.
LIGACAO = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "e", "ou", "que",
    "em", "no", "na", "nos", "nas", "com", "por",
    "para", "pra", "pro", "se", "ao", "aos", "à", "às",
    "num", "numa", "pelo", "pela", "nem", "nao", "não",
}

# ---------------------------------------------------------------------------
# Medicao de largura
# ---------------------------------------------------------------------------

class Regua:
    """Mede a largura de um texto em pixels, no tamanho da legenda.

    Com o arquivo de fonte na mao, a medida e a de verdade, somando o avanco de
    cada glifo. Sem o arquivo, cai numa estimativa por caractere, que e o
    suficiente para nao estourar mas erra para mais.
    """

    ESTIMATIVA_POR_CARACTERE = 0.52   # fracao do tamanho da fonte

    def __init__(self, arquivo_fonte, tamanho):
        self.tamanho = tamanho
        self.avancos = None
        self.padrao = None
        if arquivo_fonte and os.path.isfile(arquivo_fonte):
            self._carregar(arquivo_fonte)

    def _carregar(self, caminho):
        try:
            from fontTools.ttLib import TTFont
        except ImportError:
            print("aviso: fontTools nao esta instalado, medindo a largura por estimativa.")
            return
        try:
            fonte = TTFont(caminho, lazy=True)
            upem = fonte["head"].unitsPerEm
            cmap = fonte.getBestCmap()
            hmtx = fonte["hmtx"]
            self.avancos = {}
            for codigo, glifo in cmap.items():
                try:
                    self.avancos[chr(codigo)] = hmtx[glifo][0] / upem
                except Exception:
                    continue
            self.padrao = self.avancos.get(" ", 0.25)
            fonte.close()
        except Exception as erro:
            print("aviso: nao consegui ler a fonte (%s), medindo por estimativa." % erro)
            self.avancos = None

    def medir(self, texto):
        if self.avancos:
            total = 0.0
            for caractere in texto:
                total += self.avancos.get(caractere, self.padrao)
            return total * self.tamanho
        return len(texto) * self.ESTIMATIVA_POR_CARACTERE * self.tamanho


# ---------------------------------------------------------------------------
# Leitura e remapeamento
# ---------------------------------------------------------------------------

def achar_palavras(pedido):
    """Resolve o --palavras, aceitando tambem a pasta do video.

    O palavras.json mora em <video>/materiais-de-trabalho/transcricao/, e ate a
    arvore mudar ele morava na raiz da pasta do video. Esta funcao aceita as
    tres formas de pedir: o caminho do arquivo, a pasta do video, ou um caminho
    antigo que nao existe mais. Devolve o caminho achado, ou None.
    """
    pedido = os.path.abspath(pedido)
    if os.path.isfile(pedido):
        return pedido

    # Pediu a pasta do video, ou um caminho antigo: procure nos dois lugares.
    base = pedido if os.path.isdir(pedido) else os.path.dirname(pedido)
    tentativas = [
        os.path.join(base, "materiais-de-trabalho", "transcricao", "palavras.json"),
        os.path.join(base, "palavras.json"),
    ]
    for tentativa in tentativas:
        if os.path.isfile(tentativa):
            return tentativa
    return None


def ler_palavras(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    lista = dados.get("palavras")
    if lista is None:
        lista = dados.get("words")   # aceita o nome em ingles de transcritores externos
    if not lista:
        raise SystemExit(
            "erro: o arquivo %s nao tem a chave 'palavras'. O formato esperado e\n"
            '  {"palavras": [{"inicio": 0.0, "fim": 0.4, "texto": "ola"}]}' % caminho)

    palavras = []
    for item in lista:
        texto = item.get("texto", item.get("word", ""))
        texto = str(texto).strip()
        if not texto:
            continue
        inicio = item.get("inicio", item.get("start"))
        fim = item.get("fim", item.get("end"))
        if inicio is None or fim is None:
            continue
        palavras.append({"inicio": float(inicio), "fim": float(fim), "texto": texto})

    palavras.sort(key=lambda p: p["inicio"])
    return palavras


def ler_segmentos(valores):
    segmentos = []
    for bruto in valores:
        partes = bruto.split(":")
        if len(partes) != 3:
            raise SystemExit(
                "erro: o segmento '%s' nao esta no formato entrada:saida:deslocamento, "
                "por exemplo 12.4:19.8:0" % bruto)
        try:
            entrada, saida, deslocamento = (float(p) for p in partes)
        except ValueError:
            raise SystemExit("erro: o segmento '%s' tem numero invalido." % bruto)
        if saida <= entrada:
            raise SystemExit("erro: no segmento '%s' a saida nao e maior que a entrada." % bruto)
        segmentos.append({"entrada": entrada, "saida": saida, "deslocamento": deslocamento})
    segmentos.sort(key=lambda s: s["deslocamento"])
    return segmentos


def remapear(palavras, segmentos):
    """Joga cada palavra para o tempo dela dentro do corte montado.

    Palavra que cai na emenda entre dois segmentos entra pelo pedaco que sobrou,
    e a ultima palavra de cada trecho fica marcada: duas falas costuradas nunca
    saem no mesmo grupo de legenda.
    """
    saida = []
    for segmento in segmentos:
        entrada = segmento["entrada"]
        fim_seg = segmento["saida"]
        deslocamento = segmento["deslocamento"]
        dentro = []
        for palavra in palavras:
            if palavra["fim"] <= entrada or palavra["inicio"] >= fim_seg:
                continue
            i = max(palavra["inicio"], entrada) - entrada + deslocamento
            f = min(palavra["fim"], fim_seg) - entrada + deslocamento
            if f - i < 0.01:
                continue
            dentro.append({"inicio": i, "fim": f, "texto": palavra["texto"]})
        if not dentro:
            print("aviso: o segmento %.2f:%.2f nao pegou nenhuma palavra. "
                  "Confira se os tempos sao do video original." % (entrada, fim_seg))
        else:
            dentro[-1]["fim_de_trecho"] = True
        saida.extend(dentro)
    saida.sort(key=lambda p: p["inicio"])
    return saida


# ---------------------------------------------------------------------------
# Agrupamento
# ---------------------------------------------------------------------------

def limpa_final(texto):
    return texto.rstrip(PONTUACAO_FORTE + PONTUACAO_FRACA + '"”’)')


def eh_ligacao(texto):
    return limpa_final(texto).lower() in LIGACAO


def termina_forte(texto):
    return any(texto.endswith(p) for p in PONTUACAO_FORTE)


def termina_fraco(texto):
    return any(texto.endswith(p) for p in PONTUACAO_FRACA)


def texto_do_grupo(grupo):
    return " ".join(p["texto"] for p in grupo)


def paredes(palavras):
    """Reparte a fala em trechos separados por parede.

    Parede e todo lugar onde o grupo TEM que fechar, doa a quem doer: fim de um
    trecho costurado, fim de frase e silencio grande. Dentro de cada trecho, a
    divisao e escolhida pelo equilibrio, logo abaixo.
    """
    trechos = []
    atual = []
    for indice, palavra in enumerate(palavras):
        atual.append(palavra)
        fim_de_trecho = palavra.get("fim_de_trecho")
        fim_de_frase = termina_forte(palavra["texto"])
        pausa = False
        if indice + 1 < len(palavras):
            pausa = palavras[indice + 1]["inicio"] - palavra["fim"] >= PAUSA_QUEBRA
        if fim_de_trecho or fim_de_frase or pausa:
            trechos.append(atual)
            atual = []
    if atual:
        trechos.append(atual)
    return trechos


# Os pesos do equilibrio. Eles nao sao gosto: cada um paga por um defeito que
# aparece no quadro, e a escala entre eles e o que decide qual defeito o gerador
# aceita quando nao da para evitar os dois.
PESO_SOBRA = 100.0      # linha curta demais, que desperdicia a largura
PESO_LIGACAO = 600.0    # palavra de ligacao pendurada no fim do grupo
PESO_LIGACAO_FIM = 150.0  # a mesma coisa no ultimo grupo do trecho, onde a parede vem logo
PESO_SOZINHA = 220.0    # grupo de uma palavra curta, que pisca na tela
BONUS_PONTUACAO = 80.0  # fechar o grupo na virgula, que e onde a voz respira
CUSTO_POR_GRUPO = 25.0  # nao picotar a fala em grupos demais


def custo_do_grupo(grupo, regua, largura_maxima, orcamento, ultimo_do_trecho):
    texto = texto_do_grupo(grupo)
    largura = regua.medir(texto)

    if (largura > largura_maxima or len(texto) > orcamento) and len(grupo) > 1:
        return None   # nao cabe em uma linha, e da para dividir

    sobra = max(0.0, (largura_maxima - largura) / float(largura_maxima))
    custo = CUSTO_POR_GRUPO + PESO_SOBRA * sobra * sobra

    ultima = grupo[-1]["texto"]
    if eh_ligacao(ultima) and not termina_forte(ultima) and not termina_fraco(ultima):
        custo += PESO_LIGACAO_FIM if ultimo_do_trecho else PESO_LIGACAO
    if len(grupo) == 1 and len(limpa_final(grupo[0]["texto"])) <= 4:
        custo += PESO_SOZINHA
    if termina_fraco(ultima):
        custo -= BONUS_PONTUACAO
    return custo


def equilibrar(trecho, regua, largura_maxima, orcamento):
    """Escolhe onde quebrar o trecho somando o custo de todas as divisoes possiveis.

    O gerador nao vai enchendo a linha ate estourar, que e o jeito que deixa a
    palavra de ligacao pendurada e a ultima linha com uma palavra so. Ele testa
    as divisoes do trecho inteiro e fica com a de menor custo. O trecho e curto,
    entao isso e instantaneo.
    """
    n = len(trecho)
    if n == 0:
        return []

    melhor = [None] * (n + 1)
    corte = [0] * (n + 1)
    melhor[0] = 0.0

    for fim in range(1, n + 1):
        for inicio in range(fim):
            if melhor[inicio] is None:
                continue
            grupo = trecho[inicio:fim]
            custo = custo_do_grupo(grupo, regua, largura_maxima, orcamento, fim == n)
            if custo is None:
                continue
            total = melhor[inicio] + custo
            if melhor[fim] is None or total < melhor[fim]:
                melhor[fim] = total
                corte[fim] = inicio

    if melhor[n] is None:
        # Acontece quando uma palavra sozinha e mais larga que a linha inteira.
        # Nesse caso ela vai vazar, e o aviso final aponta o grupo.
        return [[palavra] for palavra in trecho]

    grupos = []
    fim = n
    while fim > 0:
        inicio = corte[fim]
        grupos.append(trecho[inicio:fim])
        fim = inicio
    grupos.reverse()
    return grupos


def agrupar(palavras, regua, largura_maxima, orcamento):
    """Quebra a fala em grupos de uma linha, um grupo por evento na tela."""
    grupos = []
    for trecho in paredes(palavras):
        grupos.extend(equilibrar(trecho, regua, largura_maxima, orcamento))
    return [g for g in grupos if g]


# ---------------------------------------------------------------------------
# Escrita do .ass
# ---------------------------------------------------------------------------

def cor_ass(hexadecimal):
    """#RRGGBB vira &HAABBGGRR, que e a ordem invertida que o formato usa."""
    valor = str(hexadecimal).strip().lstrip("#")
    if len(valor) != 6:
        raise SystemExit("erro: a cor '%s' precisa estar no formato #RRGGBB." % hexadecimal)
    r, g, b = valor[0:2], valor[2:4], valor[4:6]
    return "&H00%s%s%s" % (b.upper(), g.upper(), r.upper())


def tempo_ass(segundos):
    if segundos < 0:
        segundos = 0.0
    centesimos = int(round(segundos * 100))
    horas, resto = divmod(centesimos, 360000)
    minutos, resto = divmod(resto, 6000)
    segundo, centesimo = divmod(resto, 100)
    return "%d:%02d:%02d.%02d" % (horas, minutos, segundo, centesimo)


def escapar(texto):
    return texto.replace("\\", "").replace("{", "(").replace("}", ")").replace("\n", " ")


def montar_ass(grupos, opcoes):
    cabecalho = [
        "[Script Info]",
        "; Gerado pelo legenda.py da Fabrica de Cortes.",
        "ScriptType: v4.00+",
        "PlayResX: %d" % LARGURA_CANVAS,
        "PlayResY: %d" % ALTURA_CANVAS,
        "ScaledBorderAndShadow: yes",
        "WrapStyle: 2",
        "YCbCr Matrix: TV.709",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Legenda,%s,%d,%s,%s,&H00FFFFFF,&H64000000,0,0,0,0,100,100,0,0,1,%d,%d,5,%d,%d,0,1" % (
            opcoes["fonte"], opcoes["tamanho"], opcoes["preenchimento"], opcoes["preenchimento"],
            opcoes["contorno"], opcoes["sombra"], MARGEM_LATERAL, MARGEM_LATERAL),
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    linhas = []
    for indice, grupo in enumerate(grupos):
        inicio = grupo[0]["inicio"]
        fim = grupo[-1]["fim"]

        proximo = grupos[indice + 1][0]["inicio"] if indice + 1 < len(grupos) else None
        limite = proximo if proximo is not None else fim + FOLGA_FINAL
        fim = min(fim + FOLGA_FINAL, limite)
        if fim - inicio < DURACAO_MINIMA:
            alvo = inicio + DURACAO_MINIMA
            fim = min(alvo, limite) if proximo is not None else alvo
        if fim <= inicio:
            fim = inicio + 0.08

        linhas.append("Dialogue: 0,%s,%s,Legenda,,0,0,0,,%s" % (
            tempo_ass(inicio), tempo_ass(fim), escapar(texto_do_grupo(grupo))))

    return "\n".join(cabecalho + linhas) + "\n"


# ---------------------------------------------------------------------------
# Linha de comando
# ---------------------------------------------------------------------------

def principal(argv=None):
    analisador = argparse.ArgumentParser(
        description="Gera a legenda .ass do corte, no padrao invertido do pacote.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exemplo:\n"
               "  flow-reels produzir/legenda --palavras palavras.json --segmento 12.4:19.8:0 --saida legenda.ass")
    analisador.add_argument("--palavras", required=True,
                            help="caminho do palavras.json da transcricao, ou a pasta do video")
    analisador.add_argument("--saida", required=True, help="caminho do .ass a escrever")
    analisador.add_argument("--segmento", action="append", default=[], metavar="ENTRADA:SAIDA:DESLOC",
                            help="um trecho do video original que entra no corte. Pode repetir.")
    analisador.add_argument("--tudo", action="store_true",
                            help="usa a transcricao inteira, sem recorte de segmento")
    analisador.add_argument("--fonte", default="Quicksand",
                            help="nome da familia como o queimador enxerga (padrao: Quicksand)")
    analisador.add_argument("--arquivo-fonte", default=None,
                            help="caminho do .ttf estatico, usado para medir a largura de verdade")
    analisador.add_argument("--tamanho", type=int, default=TAMANHO_PADRAO,
                            help="tamanho da legenda em px (padrao: %d)" % TAMANHO_PADRAO)
    analisador.add_argument("--contorno", type=int, default=CONTORNO_PADRAO,
                            help="espessura do contorno branco (padrao: %d)" % CONTORNO_PADRAO)
    analisador.add_argument("--sombra", type=int, default=SOMBRA_PADRAO,
                            help="a sombra (padrao: %d)" % SOMBRA_PADRAO)
    analisador.add_argument("--cor-preenchimento", default=COR_PREENCHIMENTO_PADRAO,
                            help="a cor escura do preenchimento, em #RRGGBB (padrao: %s)"
                                 % COR_PREENCHIMENTO_PADRAO)
    analisador.add_argument("--orcamento", type=int, default=ORCAMENTO_PADRAO,
                            help="teto de caracteres por grupo (padrao: %d)" % ORCAMENTO_PADRAO)
    analisador.add_argument("--largura-util", type=int, default=LARGURA_UTIL,
                            help="largura disponivel em px (padrao: %d)" % LARGURA_UTIL)

    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        analisador.print_help()
        print("\nFaltou dizer o que legendar. O minimo e --palavras, --saida e "
              "--tudo ou pelo menos um --segmento.")
        return 2

    opcoes = analisador.parse_args(argv)

    caminho_palavras = achar_palavras(opcoes.palavras)
    if caminho_palavras is None:
        print("erro: nao encontrei o arquivo de palavras em %s" % opcoes.palavras)
        print("      ele nasce em <video>/materiais-de-trabalho/transcricao/palavras.json,")
        print("      gravado pela skill transcrever. Rode ela antes de legendar.")
        return 1
    if os.path.abspath(caminho_palavras) != os.path.abspath(opcoes.palavras):
        print("aviso: usei o palavras.json que achei em %s" % caminho_palavras)
    if not opcoes.segmento and not opcoes.tudo:
        print("erro: diga pelo menos um --segmento entrada:saida:deslocamento, ou use --tudo.")
        return 1

    palavras = ler_palavras(caminho_palavras)
    if not palavras:
        print("erro: a transcricao esta vazia.")
        return 1

    if opcoes.tudo:
        usadas = [dict(p) for p in palavras]
        usadas[-1]["fim_de_trecho"] = True
    else:
        usadas = remapear(palavras, ler_segmentos(opcoes.segmento))

    if not usadas:
        print("erro: nenhum segmento pegou palavra. Confira se os tempos sao do video original.")
        return 1

    regua = Regua(opcoes.arquivo_fonte, opcoes.tamanho)
    # O contorno cresce para os dois lados e come largura util.
    largura_maxima = opcoes.largura_util - 2 * opcoes.contorno

    grupos = agrupar(usadas, regua, largura_maxima, opcoes.orcamento)

    conteudo = montar_ass(grupos, {
        "fonte": opcoes.fonte,
        "tamanho": opcoes.tamanho,
        "contorno": opcoes.contorno,
        "sombra": opcoes.sombra,
        "preenchimento": cor_ass(opcoes.cor_preenchimento),
    })

    pasta = os.path.dirname(os.path.abspath(opcoes.saida))
    if pasta and not os.path.isdir(pasta):
        os.makedirs(pasta, exist_ok=True)
    with open(opcoes.saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)

    maior = max(grupos, key=lambda g: regua.medir(texto_do_grupo(g)))
    largura_maior = regua.medir(texto_do_grupo(maior))
    duracao = grupos[-1][-1]["fim"]

    print("legenda escrita em %s" % os.path.abspath(opcoes.saida))
    print("  grupos: %d   palavras: %d   duracao coberta: %.1f s" % (len(grupos), len(usadas), duracao))
    print("  medicao: %s" % ("real, pelo arquivo de fonte" if regua.avancos
                             else "estimada, sem arquivo de fonte"))
    print("  grupo mais largo: \"%s\"  =  %.0f px de %d disponiveis" % (
        texto_do_grupo(maior), largura_maior, largura_maxima))
    if largura_maior > largura_maxima:
        print("  ATENCAO: esse grupo vaza a margem. Baixe o --orcamento ou confira a fonte.")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
