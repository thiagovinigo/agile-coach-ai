# -*- coding: utf-8 -*-
"""
amostrar_cores.py
Lê uma imagem (print de uma peça da marca, capa, post, slide) e devolve, em JSON,
as cores dominantes, o candidato a cor de destaque, o candidato a tinta e se a
superfície é clara ou escura.

É a parte mecânica do procedimento descrito em referencias/EXTRAIR-DE-IMAGEM.md.
O script mede; quem decide é a conversa com a pessoa.

Uso:
    flow-reels marca/amostrar_cores <caminho-da-imagem> [--cores 16] [--json] [--grade]

    --cores   quantas cores no máximo aparecem na paleta de saída (padrão 16)
    --json    imprime só o JSON, sem o resumo legível
    --grade   inclui o mapa de 4x4 com a ocupação do destaque em cada célula,
              que ajuda a entender onde a marca coloca o acento

Depende só de Pillow.
"""

import json
import sys
from pathlib import Path

# O terminal do Windows nao nasce em UTF-8, e sem isto todo acento sai quebrado.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


try:
    from PIL import Image
except ImportError:
    print(
        "Falta a biblioteca Pillow. Instale com: pip install pillow",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------- critérios
# Os números abaixo são o critério de decisão. Estão aqui em cima, juntos,
# porque são a única coisa que você mexe quando o script erra em uma marca
# muito fora do comum.

LADO_MAXIMO = 360          # a imagem é reduzida para isso antes de medir
DISTANCIA_FUSAO = 26       # cores a menos disso de distância viram uma só
FATIA_MINIMA = 0.004       # cor que ocupa menos de 0,4% da imagem é ruído

SAT_DESTAQUE = 0.35        # saturação mínima (HSV) para um candidato a destaque
LUZ_DESTAQUE_MIN = 0.10    # luminosidade HSL mínima do destaque
LUZ_DESTAQUE_MAX = 0.85    # luminosidade HSL máxima do destaque
FATIA_DESTAQUE_MIN = 0.002 # o destaque ocupa pouco, mas não pode ser um pixel
FATIA_DESTAQUE_MAX = 0.35  # se ocupa mais que isso, é superfície, não acento
DISTANCIA_DA_SUPERFICIE = 45

SAT_NEUTRO = 0.22          # acima disso (HSV) a cor não serve como tinta
CONTRASTE_MINIMO = 4.5     # o piso de leitura que o onboarding cobra


# ---------------------------------------------------------------- conversões
def para_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def matiz_saturacao_luz(rgb):
    """
    Devolve matiz, saturação e luminosidade.

    A saturação aqui é a do modelo HSV, ou seja a distância entre o canal mais
    forte e o mais fraco dividida pelo mais forte. NÃO é a saturação do HSL, e a
    diferença importa: no HSL um branco levemente quente como #FDFBF8 aparece com
    saturação 0,55, o que faria o script tratar o texto creme como cor de marca e
    rejeitá-lo como tinta. Na conta do HSV esse mesmo creme dá 0,02, que é o que
    ele é de verdade: um neutro. A luminosidade continua sendo a do HSL, porque é
    ela que separa cor clara de cor escura.
    """
    r, g, b = [c / 255.0 for c in rgb]
    alto, baixo = max(r, g, b), min(r, g, b)
    luz = (alto + baixo) / 2.0
    if alto == baixo:
        return 0.0, 0.0, luz
    d = alto - baixo
    sat = d / alto
    if alto == r:
        matiz = ((g - b) / d) % 6
    elif alto == g:
        matiz = (b - r) / d + 2
    else:
        matiz = (r - g) / d + 4
    return matiz * 60.0, sat, luz


def luminancia(rgb):
    """Luminância relativa da WCAG, que é o que decide contraste de leitura."""
    canais = []
    for c in rgb:
        c = c / 255.0
        canais.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = canais
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    claro, escuro = max(la, lb), min(la, lb)
    return round((claro + 0.05) / (escuro + 0.05), 2)


def distancia(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


# ---------------------------------------------------------------- amostragem
def paleta(imagem, quantidade):
    """
    Devolve a lista de cores da imagem com a fatia que cada uma ocupa.

    A contagem é feita numa grade fixa de 16 níveis por canal, e NÃO com o
    quantizador pronto do Pillow. O motivo foi medido: o quantizador distribui as
    vagas dele por volume de pixel, então numa peça de fundo escuro ele gasta as
    dezesseis vagas em tons de fundo e joga o texto claro e o acento laranja no
    mesmo balde, devolvendo uma cor marrom que não existe na imagem. A grade fixa
    não tem vaga para disputar: cada cor cai no balde dela, por menor que seja.
    """
    reduzida = imagem.convert("RGB")
    reduzida.thumbnail((LADO_MAXIMO, LADO_MAXIMO), Image.LANCZOS)
    total = reduzida.width * reduzida.height

    bytes_rgb = reduzida.tobytes()
    baldes = {}
    for i in range(0, len(bytes_rgb), 3):
        r, g, b = bytes_rgb[i], bytes_rgb[i + 1], bytes_rgb[i + 2]
        chave = (r >> 4, g >> 4, b >> 4)
        acumulado = baldes.get(chave)
        if acumulado is None:
            baldes[chave] = [1, r, g, b]
        else:
            acumulado[0] += 1
            acumulado[1] += r
            acumulado[2] += g
            acumulado[3] += b

    # Piso baixo antes da fusão: um acento com grão se espalha por baldes vizinhos,
    # e é a fusão que junta os pedaços de volta antes do corte de verdade.
    piso = max(total * FATIA_MINIMA / 4.0, 1)
    brutas = [
        {
            "rgb": (round(sr / n), round(sg / n), round(sb / n)),
            "pixels": n,
        }
        for n, sr, sg, sb in baldes.values()
        if n >= piso
    ]

    brutas.sort(key=lambda c: -c["pixels"])

    # Funde cores vizinhas, senão um degradê de fundo vira cinco entradas.
    # O centro do balde NÃO se move quando alguém entra nele: se ele fosse a média,
    # cada vizinho puxaria o centro um pouco, o balde caminharia pela paleta e
    # acabaria engolindo o acento. Medido: com o centro móvel, uma peça com grão
    # colapsa para duas cores e o acento some.
    fundidas = []
    for cor in brutas:
        for ja in fundidas:
            if distancia(cor["rgb"], ja["rgb"]) < DISTANCIA_FUSAO:
                ja["pixels"] += cor["pixels"]
                break
        else:
            fundidas.append(dict(cor))

    saida = []
    for cor in fundidas:
        fatia = cor["pixels"] / total
        if fatia < FATIA_MINIMA:
            continue
        matiz, sat, luz = matiz_saturacao_luz(cor["rgb"])
        saida.append(
            {
                "hex": para_hex(cor["rgb"]),
                "rgb": list(cor["rgb"]),
                "fatia": round(fatia, 4),
                "matiz": round(matiz, 1),
                "saturacao": round(sat, 3),
                "luminosidade": round(luz, 3),
                "luminancia": round(luminancia(cor["rgb"]), 4),
            }
        )
    saida.sort(key=lambda c: -c["fatia"])
    return saida[:quantidade]


def escolher_superficie(cores):
    """A superfície é a cor que mais ocupa a imagem. Simples e quase sempre certo."""
    return cores[0]


def escolher_tinta(cores, superficie):
    """
    A tinta é a cor de texto: pouca saturação e muito contraste com a superfície.
    Se nenhuma cor neutra aparecer, cai na de maior contraste, seja qual for.
    """
    neutras = [c for c in cores if c["saturacao"] < SAT_NEUTRO and c is not superficie]
    candidatas = neutras or [c for c in cores if c is not superficie]
    if not candidatas:
        return None
    return max(candidatas, key=lambda c: contraste(c["rgb"], superficie["rgb"]))


def escolher_destaque(cores, superficie):
    """
    O destaque é o pixel mais saturado que não é fundo nem texto: satura alto,
    ocupa pouco, e está longe da superfície.
    """
    candidatos = []
    for cor in cores:
        if cor is superficie:
            continue
        if cor["saturacao"] < SAT_DESTAQUE:
            continue
        if not (LUZ_DESTAQUE_MIN <= cor["luminosidade"] <= LUZ_DESTAQUE_MAX):
            continue
        if not (FATIA_DESTAQUE_MIN <= cor["fatia"] <= FATIA_DESTAQUE_MAX):
            continue
        if distancia(cor["rgb"], superficie["rgb"]) < DISTANCIA_DA_SUPERFICIE:
            continue
        # Saturar muito conta mais que ocupar muito, mas ocupar nada também não serve
        cor = dict(cor)
        cor["nota"] = round(
            cor["saturacao"] * (0.55 + 0.45 * min(cor["fatia"] / 0.05, 1.0)), 4
        )
        candidatos.append(cor)
    candidatos.sort(key=lambda c: -c["nota"])
    return candidatos


def grade_do_destaque(imagem, destaque, divisoes=4):
    """
    Divide a imagem em células e conta em quantas o destaque aparece.
    Serve para responder uma pergunta de layout: a marca usa o acento no topo,
    no rodapé, ou espalhado.
    """
    if not destaque:
        return None
    alvo = tuple(destaque["rgb"])
    reduzida = imagem.convert("RGB")
    reduzida.thumbnail((LADO_MAXIMO, LADO_MAXIMO), Image.LANCZOS)
    l, a = reduzida.width, reduzida.height
    pixels = reduzida.load()
    grade = []
    for linha in range(divisoes):
        faixa = []
        for coluna in range(divisoes):
            x0, x1 = coluna * l // divisoes, (coluna + 1) * l // divisoes
            y0, y1 = linha * a // divisoes, (linha + 1) * a // divisoes
            dentro = perto = 0
            for y in range(y0, y1, 2):
                for x in range(x0, x1, 2):
                    dentro += 1
                    if distancia(pixels[x, y], alvo) < 48:
                        perto += 1
            faixa.append(round(perto / dentro, 3) if dentro else 0.0)
        grade.append(faixa)
    return grade


def analisar(caminho, quantidade=16, com_grade=False):
    imagem = Image.open(caminho)
    cores = paleta(imagem, quantidade)
    if not cores:
        raise ValueError("Não consegui tirar nenhuma cor útil desta imagem.")

    superficie = escolher_superficie(cores)
    tinta = escolher_tinta(cores, superficie)
    candidatos = escolher_destaque(cores, superficie)
    destaque = candidatos[0] if candidatos else None

    modo = "escuro" if superficie["luminancia"] < 0.22 else "claro"

    contraste_texto = (
        contraste(tinta["rgb"], superficie["rgb"]) if tinta else None
    )

    sobre_destaque = None
    if destaque:
        claro, escuro = (245, 242, 238), (22, 21, 26)
        c_claro = contraste(claro, destaque["rgb"])
        c_escuro = contraste(escuro, destaque["rgb"])
        melhor = claro if c_claro >= c_escuro else escuro
        sobre_destaque = {
            "hex": para_hex(melhor),
            "contraste": max(c_claro, c_escuro),
            "passa": max(c_claro, c_escuro) >= CONTRASTE_MINIMO,
        }

    avisos = []
    if contraste_texto is not None and contraste_texto < CONTRASTE_MINIMO:
        avisos.append(
            "A tinta encontrada tem contraste {} com a superfície, abaixo do piso de {}. "
            "Escureça ou clareie o texto antes de gravar nos tokens.".format(
                contraste_texto, CONTRASTE_MINIMO
            )
        )
    if not destaque:
        avisos.append(
            "Nenhuma cor passou nos critérios de destaque. Ou a peça é monocromática, "
            "ou o acento é pequeno demais nesta imagem. Pergunte a cor direto à pessoa."
        )
    if sobre_destaque and not sobre_destaque["passa"]:
        avisos.append(
            "Nenhuma das duas tintas lê bem sobre o destaque (melhor contraste: {}). "
            "Use o destaque só como borda e traço, nunca como fundo de texto.".format(
                sobre_destaque["contraste"]
            )
        )
    if len(cores) <= 2:
        avisos.append(
            "A imagem só tem duas cores úteis. Peça uma segunda peça da marca "
            "antes de concluir a paleta."
        )

    resultado = {
        "arquivo": str(Path(caminho).resolve()),
        "dimensoes": list(imagem.size),
        "modo": modo,
        "superficie": {k: superficie[k] for k in ("hex", "rgb", "fatia", "luminancia")},
        "tinta": ({k: tinta[k] for k in ("hex", "rgb", "fatia")} if tinta else None),
        "contraste_tinta_superficie": contraste_texto,
        "destaque": (
            {k: destaque[k] for k in ("hex", "rgb", "fatia", "saturacao", "matiz", "nota")}
            if destaque
            else None
        ),
        "destaque_contraste_sugerido": sobre_destaque,
        "outros_candidatos_a_destaque": [
            {k: c[k] for k in ("hex", "fatia", "saturacao", "nota")} for c in candidatos[1:4]
        ],
        "paleta": cores,
        "avisos": avisos,
    }

    if com_grade:
        resultado["grade_do_destaque"] = grade_do_destaque(imagem, destaque)

    return resultado


def resumo(r):
    linhas = []
    linhas.append("Imagem: {} ({}x{})".format(r["arquivo"], *r["dimensoes"]))
    linhas.append("Superfície: {}  ->  modo {}".format(r["superficie"]["hex"], r["modo"]))
    if r["tinta"]:
        linhas.append(
            "Tinta: {}  (contraste {} com a superfície)".format(
                r["tinta"]["hex"], r["contraste_tinta_superficie"]
            )
        )
    if r["destaque"]:
        linhas.append(
            "Destaque: {}  (ocupa {:.1%}, saturação {})".format(
                r["destaque"]["hex"], r["destaque"]["fatia"], r["destaque"]["saturacao"]
            )
        )
        if r["destaque_contraste_sugerido"]:
            linhas.append(
                "Texto sobre o destaque: {}  (contraste {})".format(
                    r["destaque_contraste_sugerido"]["hex"],
                    r["destaque_contraste_sugerido"]["contraste"],
                )
            )
    outros = r["outros_candidatos_a_destaque"]
    if outros:
        linhas.append(
            "Outros candidatos a destaque: " + ", ".join(c["hex"] for c in outros)
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
            "Uso: flow-reels marca/amostrar_cores <caminho-da-imagem> [--cores 16] [--json] [--grade]\n"
            "\n"
            "Devolve as cores dominantes da imagem, o candidato a cor de destaque,\n"
            "o candidato a tinta e se a superfície é clara ou escura.\n"
            "Passe --json para receber só o JSON, sem o resumo legível.",
            file=sys.stdout if pediu_ajuda else sys.stderr,
        )
        sys.exit(0 if pediu_ajuda else 1)

    caminho = argumentos[0]
    quantidade = 16
    if "--cores" in argumentos:
        try:
            quantidade = int(argumentos[argumentos.index("--cores") + 1])
        except (IndexError, ValueError):
            print("O valor de --cores precisa ser um número inteiro.", file=sys.stderr)
            sys.exit(1)
    so_json = "--json" in argumentos
    com_grade = "--grade" in argumentos

    if not Path(caminho).exists():
        print("Não encontrei o arquivo: {}".format(caminho), file=sys.stderr)
        sys.exit(1)

    try:
        resultado = analisar(caminho, quantidade, com_grade)
    except Exception as erro:
        print("Não consegui ler esta imagem: {}".format(erro), file=sys.stderr)
        sys.exit(1)

    if not so_json:
        print(resumo(resultado))
        print()
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
