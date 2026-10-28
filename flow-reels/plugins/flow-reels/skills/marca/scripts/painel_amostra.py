# -*- coding: utf-8 -*-
"""
painel_amostra.py
Renderiza UM quadro do painel de cima (1080 x 956) com a marca da pessoa
aplicada, para ela olhar e dizer se é a cara dela.

É o último passo do onboarding. Enquanto a pessoa não aprovar este quadro,
setup.json continua com "marca": false e nenhum corte é produzido.

O que este quadro mostra, de propósito:
  - a superfície e o modo (claro ou escuro), que é a primeira coisa que se vê
  - o título na fonte de título, com um trecho na cor de destaque
  - dois cards, um neutro e um destacado, que é como o painel compara coisas
  - os chips numerados, um aceso, que é como o painel conta passos
  - o rótulo em caixa alta, o grão por cima de tudo e o brilho de fundo

O HTML é escrito aqui dentro, em linha. Isto é proposital: a amostra precisa
funcionar mesmo antes de a biblioteca de componentes estar instalada, e ela lê
exclusivamente marca/tokens.json. Nenhuma cor, nenhum tamanho e nenhum raio é
escolhido por este script.

Uso:
    flow-reels marca/painel_amostra [--tokens <caminho>] [--saida <arquivo.png>]
                             [--titulo "..."] [--destaque-em "..."] [--guias]

    --tokens       padrão: marca/tokens.json (cai no exemplo se ainda não existir)
    --saida        padrão: marca/painel-amostra.png
    --titulo       o texto da manchete da amostra
    --destaque-em  o trecho do título que recebe a cor de acento
    --guias        desenha a zona quieta e as margens, para conferência

Depende de playwright (pip install playwright && playwright install chromium).
"""

import base64
import html
import json
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

# O terminal do Windows nao nasce em UTF-8, e sem isto todo acento sai quebrado.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


LARGURA = 1080
ALTURA = 956
MARGEM = 56
UTIL = LARGURA - 2 * MARGEM          # 968 px, a largura útil do painel
ZONA_QUIETA = 170                    # a faixa de baixo onde a legenda passa

TITULO_PADRAO = "Seu painel, sua marca"
DESTAQUE_PADRAO = "sua marca"


def raiz_do_pacote():
    """A pasta de trabalho (setup.json, marca/); o que o pacote traz vem do plugin, por fabrica.achar."""
    return fabrica.raiz()


def carregar_tokens(caminho):
    raiz = raiz_do_pacote()
    if caminho:
        alvo = Path(caminho)
    else:
        alvo = raiz / "marca" / "tokens.json"
        if not alvo.exists():
            alvo = fabrica.achar("marca/tokens.exemplo.json")
    if not alvo.exists():
        raise FileNotFoundError(
            "Não encontrei os tokens da marca em {}. Rode o onboarding da skill "
            "`/flow-reels:marca` antes de pedir a amostra.".format(alvo)
        )
    with open(alvo, encoding="utf-8") as arquivo:
        return json.load(arquivo), alvo


def fonte_embutida(raiz, entrada, apelido):
    """
    Devolve o bloco @font-face com a fonte embutida em base64.
    Embutir evita o problema de caminho de arquivo dentro do navegador sem tela,
    que é o mesmo tipo de dor de cabeça que caminho absoluto causa no ffmpeg.
    """
    if not entrada or not entrada.get("arquivo"):
        return "", None
    caminho = Path(entrada["arquivo"])
    if not caminho.is_absolute():
        caminho = fabrica.achar(caminho)
    if not caminho.exists():
        return "", None
    dados = base64.b64encode(caminho.read_bytes()).decode("ascii")
    formato = "opentype" if caminho.suffix.lower() == ".otf" else "truetype"
    bloco = (
        "@font-face{{font-family:'{apelido}';"
        "src:url(data:font/ttf;base64,{dados}) format('{formato}');"
        "font-weight:{peso};font-style:normal;font-display:block;}}"
    ).format(
        apelido=apelido,
        dados=dados,
        formato=formato,
        peso=entrada.get("peso", 400),
    )
    return bloco, apelido


def imagem_embutida(raiz, caminho):
    if not caminho:
        return None
    alvo = Path(caminho)
    if not alvo.is_absolute():
        alvo = raiz / alvo
    if not alvo.exists():
        return None
    tipo = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
    }.get(alvo.suffix.lower())
    if not tipo:
        return None
    dados = base64.b64encode(alvo.read_bytes()).decode("ascii")
    return "data:{};base64,{}".format(tipo, dados)


def marcar_destaque(texto, trecho, cor):
    """Pinta o trecho exato do título com a cor de acento, sem quebrar o resto."""
    seguro = html.escape(texto)
    if not trecho:
        return seguro
    alvo = html.escape(trecho)
    if alvo not in seguro:
        return seguro
    return seguro.replace(
        alvo, '<span style="color:{}">{}</span>'.format(cor, alvo), 1
    )


def montar_html(tokens, raiz, titulo, destaque_em, guias):
    cores = tokens["cores"]
    tipo = tokens["tipografia"]
    forma = tokens["forma"]
    textura = tokens.get("textura", {})
    fontes = tokens.get("fontes", {})

    face_titulo, nome_titulo = fonte_embutida(raiz, fontes.get("titulo"), "fcTitulo")
    face_corpo, nome_corpo = fonte_embutida(raiz, fontes.get("corpo"), "fcCorpo")
    faces = face_titulo + face_corpo
    pilha_titulo = "'{}', sans-serif".format(nome_titulo) if nome_titulo else "sans-serif"
    pilha_corpo = "'{}', sans-serif".format(nome_corpo) if nome_corpo else "sans-serif"

    logo = tokens.get("logo") or {}
    caminho_logo = None
    if logo.get("tem"):
        preferida = (
            logo.get("versao_clara")
            if tokens.get("modo") == "escuro" and logo.get("versao_clara")
            else logo.get("caminho")
        )
        caminho_logo = imagem_embutida(raiz, preferida) or imagem_embutida(
            raiz, logo.get("caminho")
        )

    brilho = ""
    if textura.get("brilho_fundo"):
        brilho = (
            "<div class='brilho' style=\"background:radial-gradient(circle at 50% 42%,"
            "{cor} 0%, transparent 70%);opacity:{op};width:{raio}px;height:{raio}px\"></div>"
        ).format(
            cor=textura.get("brilho_cor", cores["destaque"]),
            op=textura.get("brilho_opacidade", 0.1),
            raio=textura.get("brilho_raio", 720),
        )

    bloco_logo = ""
    if caminho_logo:
        bloco_logo = "<img class='logo' src='{}' alt=''>".format(caminho_logo)

    bloco_guias = ""
    if guias:
        bloco_guias = (
            "<div class='guia-margem'></div>"
            "<div class='guia-quieta'><span>zona quieta: a legenda passa aqui</span></div>"
        )

    titulo_marcado = marcar_destaque(titulo, destaque_em, cores["destaque"])
    largura_card = (UTIL - 28) // 2
    escuro = tokens.get("modo") == "escuro"
    tom_borda = "rgba(255,255,255,0.07)" if escuro else "rgba(0,0,0,0.08)"

    # O grão é uma camada de pontinhos com transparência variável, não uma
    # textura cinza em modo de mistura. Foi medido nesta máquina: ruído cinza em
    # overlay quase não muda a imagem (desvio de 0,3 nível), enquanto a mesma
    # intensidade em pontinhos dá desvio de 3,5, que é grão de verdade e sobrevive
    # à compressão da plataforma. Em superfície escura os pontos são claros, em
    # superfície clara são escuros, e a intensidade dos tokens vira opacidade direta.
    cor_grao = "1 1 1" if escuro else "0 0 0"

    return """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><style>
{faces}
:root{{
  --superficie:{superficie}; --superficie-alt:{superficie_alt};
  --tinta:{tinta}; --tinta-suave:{tinta_suave};
  --destaque:{destaque}; --destaque-contraste:{destaque_contraste};
  --fonte-titulo:{pilha_titulo}; --fonte-corpo:{pilha_corpo};
  --tam-titulo:{tam_titulo}px; --tam-rotulo:{tam_rotulo}px; --tam-corpo:{tam_corpo}px;
  --entrelinha:{entrelinha}; --espacamento-rotulo:{espacamento_rotulo}em;
  --raio:{raio}px; --borda:{borda}px; --traco:{traco}px;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{largura}px;height:{altura}px;overflow:hidden}}
body{{background:var(--superficie);font-family:var(--fonte-corpo);
  -webkit-font-smoothing:antialiased;position:relative}}
.brilho{{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);
  border-radius:50%;pointer-events:none}}
.painel{{position:relative;width:{largura}px;height:{altura}px;
  padding:{margem}px {margem}px {fundo_util}px {margem}px;
  display:flex;flex-direction:column;gap:34px}}
.topo{{display:flex;align-items:center;justify-content:space-between;gap:24px}}
.rotulo{{font-family:var(--fonte-corpo);font-size:var(--tam-rotulo);
  letter-spacing:var(--espacamento-rotulo);text-transform:uppercase;
  color:var(--tinta-suave);font-weight:500}}
.logo{{height:{altura_logo}px;width:auto;object-fit:contain}}
.titulo{{font-family:var(--fonte-titulo);font-size:var(--tam-titulo);
  line-height:var(--entrelinha);color:var(--tinta);font-weight:700;
  max-width:{util}px}}
.cards{{display:flex;gap:28px}}
.card{{width:{largura_card}px;background:var(--superficie-alt);
  border:var(--borda) solid {tom_borda};border-radius:var(--raio);
  padding:32px 30px;display:flex;flex-direction:column;gap:12px}}
.card.destacado{{border-color:var(--destaque)}}
.card h3{{font-family:var(--fonte-titulo);font-size:var(--tam-corpo);
  color:var(--tinta);font-weight:700;line-height:1.1}}
.card.destacado h3{{color:var(--destaque)}}
.card p{{font-family:var(--fonte-corpo);font-size:{tam_apoio}px;
  color:var(--tinta-suave);line-height:1.3}}
.chips{{display:flex;align-items:center;gap:22px;margin-top:auto}}
.chip{{width:112px;height:112px;border-radius:var(--raio);flex:none;
  display:flex;align-items:center;justify-content:center;
  font-family:var(--fonte-titulo);font-size:{tam_chip}px;font-weight:700;
  border:var(--borda) solid var(--tinta-suave);color:var(--tinta-suave)}}
.chip.aceso{{background:var(--destaque);border-color:var(--destaque);
  color:var(--destaque-contraste)}}
.trilho{{flex:1;height:{altura_trilho}px;border-radius:999px;
  background:var(--superficie-alt);overflow:hidden}}
.trilho i{{display:block;height:100%;width:62%;background:var(--destaque);
  border-radius:999px}}
.grao{{position:absolute;inset:0;pointer-events:none;
  opacity:{grao};background-image:url("data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>\
<filter id='r'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/>\
<feColorMatrix type='matrix' values='0 0 0 0 {cor_grao_r} 0 0 0 0 {cor_grao_g} 0 0 0 0 {cor_grao_b} 1 0 0 0 -0.35'/>\
</filter><rect width='220' height='220' filter='url(%23r)'/></svg>");
  background-size:{grao_tamanho_px}px {grao_tamanho_px}px}}
.guia-margem{{position:absolute;inset:{margem}px;border:1px dashed rgba(255,0,110,.55);
  pointer-events:none}}
.guia-quieta{{position:absolute;left:0;right:0;bottom:0;height:{zona_quieta}px;
  background:rgba(255,0,110,.10);border-top:1px dashed rgba(255,0,110,.55);
  display:flex;align-items:center;justify-content:center;pointer-events:none}}
.guia-quieta span{{font-family:var(--fonte-corpo);font-size:26px;color:rgba(255,0,110,.9);
  letter-spacing:.06em;text-transform:uppercase}}
</style></head><body>
{brilho}
<div class="painel">
  <div class="topo"><div class="rotulo">Amostra da marca</div>{bloco_logo}</div>
  <div class="titulo">{titulo}</div>
  <div class="cards">
    <div class="card"><h3>Antes</h3><p>O jeito comum, sem a sua cara. Está aqui só para comparação.</p></div>
    <div class="card destacado"><h3>Depois</h3><p>A mesma peça lendo os seus tokens. É só isto que muda.</p></div>
  </div>
  <div class="chips">
    <div class="chip aceso">1</div>
    <div class="chip">2</div>
    <div class="chip">3</div>
    <div class="trilho"><i></i></div>
  </div>
</div>
<div class="grao"></div>
{guias}
</body></html>""".format(
        faces=faces,
        superficie=cores["superficie"],
        superficie_alt=cores["superficie_alt"],
        tinta=cores["tinta"],
        tinta_suave=cores["tinta_suave"],
        destaque=cores["destaque"],
        destaque_contraste=cores["destaque_contraste"],
        pilha_titulo=pilha_titulo,
        pilha_corpo=pilha_corpo,
        tam_titulo=tipo["titulo"],
        tam_rotulo=tipo["rotulo"],
        tam_corpo=tipo["corpo"],
        tam_apoio=round(tipo["rotulo"] * 1.05),
        tam_chip=round(tipo["corpo"] * 0.92),
        entrelinha=tipo["entrelinha"],
        espacamento_rotulo=tipo["espacamento_rotulo"],
        raio=forma["raio_canto"],
        borda=forma["espessura_borda"],
        traco=forma["espessura_traco"],
        altura_trilho=max(forma["espessura_traco"] * 6, 24),
        tom_borda=tom_borda,
        largura=LARGURA,
        altura=ALTURA,
        margem=MARGEM,
        util=UTIL,
        largura_card=largura_card,
        zona_quieta=ZONA_QUIETA,
        # 18 px de folga acima da zona quieta: encostar na linha já é invadir,
        # porque a legenda tem contorno e sombra que passam do texto.
        fundo_util=ZONA_QUIETA + 18,
        altura_logo=(logo.get("altura_minima") or 96),
        grao=textura.get("grao_intensidade", 0.14),
        cor_grao_r=cor_grao.split()[0],
        cor_grao_g=cor_grao.split()[1],
        cor_grao_b=cor_grao.split()[2],
        grao_tamanho_px=220 * int(textura.get("grao_tamanho", 1) or 1),
        # 220 é o lado do ladrilho de ruído. Manter 1 para 1 é o que faz o grão
        # existir: reduzir o ladrilho borra o ruído e o painel volta a ficar chapado.
        brilho=brilho,
        bloco_logo=bloco_logo,
        titulo=titulo_marcado,
        guias=bloco_guias,
    )


def renderizar(documento, destino):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Falta o playwright. Rode o instalador do pacote, ou:\n"
            "  pip install playwright\n"
            "  playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(2)

    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as p:
            navegador = p.chromium.launch(args=["--force-color-profile=srgb"])
            pagina = navegador.new_page(
                viewport={"width": LARGURA, "height": ALTURA}, device_scale_factor=1
            )
            pagina.set_content(documento, wait_until="load")
            pagina.evaluate("document.fonts.ready")
            pagina.wait_for_timeout(180)
            pagina.screenshot(path=str(destino))
            navegador.close()
    except Exception as erro:
        texto = str(erro)
        if "Executable doesn" in texto or "playwright install" in texto:
            print(
                "O navegador sem tela não está instalado. Rode:\n"
                "  playwright install chromium",
                file=sys.stderr,
            )
        else:
            print("Não consegui renderizar a amostra: {}".format(texto), file=sys.stderr)
        sys.exit(1)
    return destino


def valor_de(argumentos, bandeira, padrao=None):
    if bandeira in argumentos:
        indice = argumentos.index(bandeira) + 1
        if indice < len(argumentos):
            return argumentos[indice]
        print("Faltou o valor depois de {}.".format(bandeira), file=sys.stderr)
        sys.exit(1)
    return padrao


def main():
    argumentos = sys.argv[1:]
    # Este script roda bem sem argumento nenhum, entao aqui so existe o caso da
    # ajuda pedida, e pedir ajuda nao e erro: stdout e codigo 0.
    if argumentos and argumentos[0] in ("-h", "--ajuda", "--help"):
        print(
            "Uso: flow-reels marca/painel_amostra [--tokens <caminho>] [--saida <arquivo.png>]\n"
            "                              [--titulo \"...\"] [--destaque-em \"...\"] [--guias]\n"
            "\n"
            "Renderiza um quadro 1080x956 do painel com a marca aplicada, para aprovação.\n"
            "Sem argumentos, lê marca/tokens.json e grava marca/painel-amostra.png.",
            file=sys.stdout,
        )
        sys.exit(0)

    raiz = raiz_do_pacote()
    try:
        tokens, origem = carregar_tokens(valor_de(argumentos, "--tokens"))
    except Exception as erro:
        print(str(erro), file=sys.stderr)
        sys.exit(1)

    faltando = [c for c in ("cores", "tipografia", "forma") if c not in tokens]
    if faltando:
        print(
            "O arquivo de tokens está incompleto, faltam: {}.".format(", ".join(faltando)),
            file=sys.stderr,
        )
        sys.exit(1)

    titulo = valor_de(argumentos, "--titulo", TITULO_PADRAO)
    destaque_em = valor_de(argumentos, "--destaque-em", None)
    if destaque_em is None and titulo == TITULO_PADRAO:
        destaque_em = DESTAQUE_PADRAO
    saida = valor_de(argumentos, "--saida", str(raiz / "marca" / "painel-amostra.png"))
    guias = "--guias" in argumentos

    documento = montar_html(tokens, raiz, titulo, destaque_em, guias)
    destino = renderizar(documento, saida)

    print("Tokens lidos de: {}".format(origem))
    print("Amostra gravada em: {}".format(Path(destino).resolve()))


if __name__ == "__main__":
    main()
