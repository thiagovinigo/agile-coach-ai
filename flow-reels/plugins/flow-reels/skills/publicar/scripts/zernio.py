#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cliente de linha de comando da API da Zernio.

Cobre o que a skill `/flow-reels:publicar` precisa: descobrir as contas conectadas,
subir midia, publicar ou agendar um post, conferir onde o post caiu, e montar o
funil "comenta a palavra, recebe o link na DM".

Por que um script e nao um curl solto: tres coisas custam caro aqui e sao
invisiveis num curl. A midia que precisa ser arquivo publico direto, a palavra
do funil que nunca e devolvida e por isso nao pode colidir com outra automacao,
e o link de entrega que precisa continuar dentro do texto da DM e abrir para um
estranho. Tudo isso e conferido antes de qualquer escrita.

Por que Python e nao Node: o pacote inteiro ja roda em Python e ffmpeg. Trazer o
Node so para a ultima etapa seria uma dependencia nova em toda instalacao, para
sempre, por causa de um arquivo so. Este script usa apenas a biblioteca padrao,
entao nao instala nada.

Uso:

    flow-reels publicar/zernio ajuda
    flow-reels publicar/zernio checar
    flow-reels publicar/zernio contas
    flow-reels publicar/zernio midia ./corte-01.mp4
    flow-reels publicar/zernio postar @post.json [--seco]
    flow-reels publicar/zernio situacao <postId>
    flow-reels publicar/zernio palavras
    flow-reels publicar/zernio funil @funil.json [--seco]
    flow-reels publicar/zernio funil-desligar <automationId>
    flow-reels publicar/zernio funil-ligar <automationId>
    flow-reels publicar/zernio api GET /posts

Com --seco nada sai da maquina: o script valida, imprime o que mandaria e para.
"""

import json
import mimetypes
import os
import re
import sys
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


BASE_PADRAO = "https://zernio.com/api/v1"
AGENTE = "fabrica-de-cortes/1.0"
LIMITE_DM = 1000          # limite aproximado da Meta para o texto da DM
MAX_SLIDES_INSTAGRAM = 10
FORMATO_PALAVRA = re.compile(r"^[a-z0-9][a-z0-9-]{1,39}$")


# ----------------------------------------------------------------- saida

def erro(mensagem, codigo=1):
    print("zernio: " + mensagem, file=sys.stderr)
    sys.exit(codigo)


def aviso(mensagem):
    print("aviso: " + mensagem, file=sys.stderr)


def imprimir_json(dado):
    print(json.dumps(dado, indent=2, ensure_ascii=False))


# -------------------------------------------------------------- ambiente

def carregar_env(inicio=None):
    """Le o .env do pacote e joga o conteudo no ambiente.

    Procura na raiz do pacote e na pasta de onde o comando foi rodado, mais as
    pastas acima dela ATE a raiz do pacote. De proposito ele NAO sai do pacote
    subindo.

    Por que o limite existe: uma busca que sobe ate a raiz do disco acaba lendo
    o .env pessoal de quem esta rodando e mandando a chave de outra ferramenta
    numa chamada de API. Credencial de terceiro nunca entra numa chamada deste
    script.

    Nao sobrescreve variavel que ja existe no ambiente, porque quem exportou na
    mao tem prioridade sobre arquivo.
    """
    # a pasta de trabalho (onde moram o setup.json e o .env), e nunca acima dela
    raiz = fabrica.raiz()
    atual = Path(inicio or Path.cwd()).resolve()
    candidatos = [raiz]
    if atual == raiz or raiz in atual.parents:
        candidatos.append(atual)
        candidatos += [p for p in atual.parents if raiz == p or raiz in p.parents]
    vistos = set()
    for pasta in candidatos:
        if pasta in vistos:
            continue
        vistos.add(pasta)
        arquivo = pasta / ".env"
        if not arquivo.exists():
            continue
        for linha in arquivo.read_text(encoding="utf-8", errors="ignore").splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            chave, valor = chave.strip(), valor.strip().strip('"').strip("'")
            if chave and valor and not os.environ.get(chave):
                os.environ[chave] = valor
        return arquivo
    return None


ARQUIVO_ENV = carregar_env()
BASE = os.environ.get("ZERNIO_API_BASE", "").strip() or BASE_PADRAO


FALTA_CHAVE = (
    "falta a chave ZERNIO_API_KEY.\n\n"
    "  Como resolver:\n"
    "  1. Pegue a chave no painel da Zernio, na area de API\n"
    "  2. Copie o arquivo .env.exemplo da raiz do pacote para .env\n"
    "  3. Cole a chave na linha ZERNIO_API_KEY=\n\n"
    "  Sem ela o pacote continua funcionando inteiro ate a revisao.\n"
    "  So a publicacao para aqui, e o seu corte ja esta pronto no disco."
)


def pegar_chave():
    chave = os.environ.get("ZERNIO_API_KEY", "").strip()
    if not chave:
        erro(FALTA_CHAVE, codigo=3)
    return chave


# ------------------------------------------------------------------ http

def tentar_json(texto):
    try:
        return json.loads(texto)
    except Exception:
        return None


def chamar(metodo, caminho, dados=None):
    chave = pegar_chave()
    cabecalhos = {
        "Authorization": "Bearer " + chave,
        "User-Agent": AGENTE,
        "Content-Type": "application/json",
    }
    corpo = None if dados is None else json.dumps(dados).encode("utf-8")
    requisicao = urllib.request.Request(
        BASE + caminho, data=corpo, headers=cabecalhos, method=metodo
    )
    try:
        with urllib.request.urlopen(requisicao, timeout=120) as resposta:
            texto = resposta.read().decode("utf-8", errors="replace")
            return {"status": resposta.status, "ok": True,
                    "json": tentar_json(texto), "texto": texto}
    except urllib.error.HTTPError as e:
        texto = e.read().decode("utf-8", errors="replace")
        return {"status": e.code, "ok": False, "json": tentar_json(texto), "texto": texto}
    except urllib.error.URLError as e:
        erro("nao consegui falar com %s: %s" % (BASE, e.reason), codigo=4)


def erro_de(r):
    dado = r.get("json") or {}
    if isinstance(dado, dict):
        for campo in ("error", "message", "detail"):
            if dado.get(campo):
                return str(dado[campo])
    return (r.get("texto") or "")[:300] or ("HTTP %s" % r.get("status"))


def mostrar(rotulo, r):
    imprimir_json(r.get("json") if r.get("json") is not None else r.get("texto"))
    print("\n[%s] HTTP %s%s" % (rotulo, r["status"], "" if r["ok"] else "  <- falhou"),
          file=sys.stderr)
    if not r["ok"]:
        sys.exit(1)


def lista_de(dado, *campos):
    if isinstance(dado, list):
        return dado
    if isinstance(dado, dict):
        for campo in campos:
            if isinstance(dado.get(campo), list):
                return dado[campo]
    return []


def corpo_do_argumento(arg):
    if not arg:
        return {}
    if arg.startswith("@"):
        caminho = Path(arg[1:])
        if not caminho.exists():
            erro("nao achei o arquivo %s" % caminho)
        cru = caminho.read_text(encoding="utf-8")
    else:
        cru = arg
    try:
        return json.loads(cru)
    except json.JSONDecodeError as e:
        erro("o corpo nao e JSON valido: %s" % e)


# ------------------------------------------------------------- copy padrao
#
# Sai em portugues, como todo o resto do pacote. Quem publica para um publico de
# outra lingua escreve os textos no spec do funil, em "textos". Transacional e
# curto: e uma DM, nao uma pagina de venda.

def dm_padrao(link):
    return (
        "Oi! Obrigado pelo comentario.\n\n"
        "Aqui esta o que prometi:\n\n"
        "%s\n\n"
        "Se ficar qualquer duvida, e so responder por aqui." % link
    )


RESPOSTA_PADRAO = "Mandei na sua DM, da uma olhada."


# ---------------------------------------------------------------- perfil

_perfil_cache = None


def perfil_id():
    global _perfil_cache
    do_ambiente = os.environ.get("ZERNIO_PROFILE_ID", "").strip()
    if do_ambiente:
        return do_ambiente
    if _perfil_cache:
        return _perfil_cache
    r = chamar("GET", "/profiles")
    if not r["ok"]:
        erro("nao consegui listar os perfis: %s" % erro_de(r))
    perfis = lista_de(r["json"], "profiles", "data")
    conta_ig = os.environ.get("ZERNIO_IG_ACCOUNT_ID", "").strip()
    escolhido = None
    if conta_ig:
        for p in perfis:
            if conta_ig in json.dumps(p):
                escolhido = p
                break
    if escolhido is None and perfis:
        escolhido = perfis[0]
    if not isinstance(escolhido, dict):
        erro("nenhum profileId encontrado. Defina ZERNIO_PROFILE_ID no .env.")
    ident = escolhido.get("_id") or escolhido.get("id")
    if not ident:
        erro("o perfil veio sem id. Defina ZERNIO_PROFILE_ID no .env.")
    _perfil_cache = str(ident)
    return _perfil_cache


# ------------------------------------------------------------- link publico
#
# Um link que pede login entrega um muro de login na DM, o que e pior que nao
# entregar nada. A conferencia e anonima, como um estranho veria.

def link_publico(url):
    requisicao = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    try:
        with urllib.request.urlopen(requisicao, timeout=60) as resposta:
            destino = resposta.geturl() or ""
            if "accounts.google.com" in destino:
                return False, "cai num login do Google"
            tipo = (resposta.headers.get("Content-Type") or "").lower()
            if "text/html" not in tipo:
                return True, None
            inicio = resposta.read(20000).decode("utf-8", errors="ignore").lower()
            if "<title>sign in" in inicio or "accounts.google.com/v3/signin" in inicio:
                return False, "responde com uma pagina de login"
            return True, None
    except urllib.error.HTTPError as e:
        return False, "HTTP %s" % e.code
    except Exception as e:
        return False, str(e)


# --------------------------------------------------------------- comandos

AJUDA = """uso: flow-reels publicar/zernio <comando> [argumentos]

  ajuda                              esta tela
  checar                             diz o que esta configurado, sem chamar a API
  contas                             contas conectadas (e de onde saem os accountId)
  perfis                             perfis do workspace (profileId)
  midia <arquivo>                    sobe o arquivo e devolve a url publica
  postar @post.json [--seco]         cria o post (agenda, publica agora ou rascunho)
  situacao <postId>                  status e a url nativa depois que publica
  palavras                           palavras de funil ja em uso
  funil @funil.json [--seco]         cria o funil comenta-a-palavra
  funil-desligar <automationId>      aposenta a oferta (isActive: false)
  funil-ligar <automationId>         traz a oferta de volta
  api <METODO> <caminho> [json]      qualquer endpoint

Com --seco o script valida, imprime o que mandaria e nao chama a API."""


def cmd_checar():
    print("Configuracao da publicacao\n")
    print("  arquivo .env     %s" % (ARQUIVO_ENV if ARQUIVO_ENV
                                     else "nao encontrado dentro do pacote"))
    print("  base da API      %s%s" % (BASE, "" if BASE == BASE_PADRAO
                                       else "  (de ZERNIO_API_BASE)"))
    faltando = []
    for nome, obrigatoria, para_que in (
        ("ZERNIO_API_KEY", True, "falar com a API"),
        ("ZERNIO_IG_ACCOUNT_ID", False, "publicar no Instagram e criar funil"),
        ("ZERNIO_YT_ACCOUNT_ID", False, "publicar no YouTube"),
        ("ZERNIO_PROFILE_ID", False, "fixar o perfil, se a descoberta automatica errar"),
    ):
        valor = os.environ.get(nome, "").strip()
        if valor:
            visivel = (valor[:4] + "...") if nome.endswith("API_KEY") else valor
            print("  %-22s ok    %s" % (nome, visivel))
        else:
            print("  %-22s falta (%s)" % (nome, para_que))
            if obrigatoria:
                faltando.append(nome)
    if faltando:
        print("")
        erro(FALTA_CHAVE, codigo=3)
    print("\nChave no lugar. As contas voce descobre com: flow-reels publicar/zernio contas")


def cmd_midia(argumentos):
    if not argumentos:
        erro("midia precisa do caminho do arquivo")
    caminho = Path(argumentos[0])
    if not caminho.exists():
        erro("nao achei o arquivo %s" % caminho)
    tipo = mimetypes.guess_type(caminho.name)[0] or "application/octet-stream"
    bytes_do_arquivo = caminho.read_bytes()
    pre = chamar("POST", "/media/presign", {"filename": caminho.name, "contentType": tipo})
    if not pre["ok"]:
        erro("o presign falhou: %s" % erro_de(pre))
    dado = pre["json"] or {}
    url_de_subida = dado.get("uploadUrl") or dado.get("url")
    url_publica = dado.get("publicUrl") or dado.get("public_url")
    if not url_de_subida:
        erro("o presign nao devolveu uploadUrl: %s" % json.dumps(dado))
    requisicao = urllib.request.Request(
        url_de_subida, data=bytes_do_arquivo, method="PUT",
        headers={"Content-Type": tipo, "User-Agent": AGENTE},
    )
    try:
        with urllib.request.urlopen(requisicao, timeout=600) as resposta:
            if resposta.status >= 300:
                erro("o PUT falhou: HTTP %s" % resposta.status)
    except urllib.error.HTTPError as e:
        erro("o PUT falhou: HTTP %s" % e.code)
    if not url_publica:
        # Sem publicUrl nao ha o que colar no mediaItems. Imprimir um aviso na
        # saida padrao faria o proprio aviso virar a "url" do payload.
        erro("o arquivo subiu, mas o presign nao devolveu publicUrl.\n"
             "  Resposta do presign: %s\n"
             "  Pegue a url no painel da Zernio, ou investigue a resposta com:\n"
             "    flow-reels publicar/zernio api POST /media/presign" % json.dumps(dado))
    print(url_publica)
    print("\n[midia] %s, %d bytes, %s" % (caminho.name, len(bytes_do_arquivo), tipo),
          file=sys.stderr)


def validar_post(payload):
    problemas = []
    plataformas = payload.get("platforms")
    if not isinstance(plataformas, list) or not plataformas:
        problemas.append("o post precisa de platforms[]")
    midias = payload.get("mediaItems")
    if not isinstance(midias, list) or not midias:
        problemas.append("o post precisa de mediaItems[] com url publica direta")
    if isinstance(midias, list) and "drive.google" in json.dumps(midias):
        problemas.append("a Zernio nao busca link do Drive: suba com 'midia' e use a url publica")
    if payload.get("scheduledFor") and payload.get("publishNow"):
        problemas.append("scheduledFor e publishNow sao alternativas: mande um ou outro")
    if payload.get("scheduledFor") and not payload.get("timezone"):
        problemas.append("scheduledFor pede timezone IANA junto, por exemplo America/Sao_Paulo")
    if isinstance(plataformas, list) and isinstance(midias, list):
        for p in plataformas:
            if isinstance(p, dict) and p.get("platform") == "instagram" \
                    and len(midias) > MAX_SLIDES_INSTAGRAM:
                problemas.append(
                    "carrossel do Instagram aceita ate %d itens e vieram %d"
                    % (MAX_SLIDES_INSTAGRAM, len(midias))
                )
    return problemas


def cmd_postar(argumentos, seco):
    payload = corpo_do_argumento(argumentos[0] if argumentos else None)
    problemas = validar_post(payload)
    if problemas:
        erro("o post nao passou na conferencia:\n  - " + "\n  - ".join(problemas))
    if seco:
        print("MODO SECO: nada foi enviado.\n")
        print("POST %s/posts" % BASE)
        imprimir_json(payload)
        destinos = [p.get("platform") for p in payload.get("platforms", [])
                    if isinstance(p, dict)]
        quando = payload.get("scheduledFor") or ("agora" if payload.get("publishNow")
                                                 else "rascunho")
        print("\niria para: %s, quando: %s" % (", ".join(str(d) for d in destinos), quando),
              file=sys.stderr)
        return
    r = chamar("POST", "/posts", payload)
    if r["ok"]:
        dado = r["json"] or {}
        ident = dado.get("_id") or dado.get("id") or (dado.get("post") or {}).get("_id")
        print("\npostId: %s  (confira depois com: flow-reels publicar/zernio situacao %s)"
              % (ident, ident), file=sys.stderr)
    mostrar("postar", r)


def cmd_situacao(argumentos):
    if not argumentos:
        erro("situacao precisa do id do post")
    r = chamar("GET", "/posts/%s" % argumentos[0])
    dado = r["json"] or {}
    # A atribuicao (id e url nativos da plataforma) vive em post.platforms[],
    # nao num bloco de analytics.
    plataformas = (dado.get("post") or {}).get("platforms") or dado.get("platforms")
    if isinstance(plataformas, list):
        print("\nonde caiu:", file=sys.stderr)
        for p in plataformas:
            print("  %s: %s  %s" % (p.get("platform"), p.get("status"),
                                    p.get("platformPostUrl") or "(sem url ainda)"),
                  file=sys.stderr)
    mostrar("situacao", r)


def automacoes():
    r = chamar("GET", "/comment-automations")
    if not r["ok"]:
        erro("nao consegui listar as automacoes: %s" % erro_de(r))
    return lista_de(r["json"], "automations", "data")


def cmd_palavras():
    lista = automacoes()
    print("PALAVRAS (automacoes de comentario)")
    for a in lista:
        palavras = ", ".join(str(k) for k in (a.get("keywords") or []))
        print("  %-24s %s %s  %s" % (palavras or "?",
                                     "ativa" if a.get("isActive") else "off  ",
                                     a.get("_id") or a.get("id"), a.get("name") or ""))
    print("\n%d automacao(oes)." % len(lista))


def cmd_funil(argumentos, seco):
    spec = corpo_do_argumento(argumentos[0] if argumentos else None)
    palavra = str(spec.get("palavra") or "").strip().lower()
    link = str(spec.get("link") or "").strip()
    textos = spec.get("textos") or {}

    if not palavra:
        erro("o funil precisa de uma palavra")
    if not FORMATO_PALAVRA.match(palavra):
        erro("palavra fora do formato: 2 a 40 caracteres, comeca com letra ou numero, "
             "depois letras, numeros e hifen")
    if not link:
        erro("o funil precisa do link que a DM entrega")

    dm = str(textos.get("dm") or "").strip() or dm_padrao(link)
    if link not in dm:
        erro("a mensagem da DM precisa conter o link que ela entrega")
    if len(dm) > LIMITE_DM:
        aviso("a DM tem %d caracteres e o limite da Meta fica por volta de %d. "
              "Encurte se ela chegar cortada." % (len(dm), LIMITE_DM))
    resposta = str(textos.get("resposta_comentario") or "").strip() or RESPOSTA_PADRAO

    corpo_da_automacao = {
        "name": "Funil - %s" % palavra,
        "trigger": "comment",
        "keywords": [palavra],
        "matchMode": "word",      # o default "contains" dispara dentro de outra palavra
        "typoTolerance": True,    # so funciona em matchMode "word"
        "commentReply": resposta,
        "dmMessage": dm,
    }

    if seco:
        print("MODO SECO: nada foi enviado, e nada foi conferido na API.\n")
        print("POST %s/comment-automations" % BASE)
        prova = {"profileId": "<descoberto na hora>", "accountId": "<ZERNIO_IG_ACCOUNT_ID>"}
        prova.update(corpo_da_automacao)
        imprimir_json(prova)
        print("\nna chamada de verdade, antes de criar, ainda conferiria:", file=sys.stderr)
        print("  - se a palavra \"%s\" ja e de outra automacao" % palavra, file=sys.stderr)
        print("  - se o link abre para um estranho, sem login", file=sys.stderr)
        return

    ok, motivo = link_publico(link)
    if not ok:
        erro("o link de entrega nao e publico (%s). Deixe como \"qualquer pessoa com o "
             "link\" e repita." % motivo)

    for a in automacoes():
        for k in (a.get("keywords") or []):
            if str(k).strip().lower() == palavra:
                erro("a palavra \"%s\" ja e de outra automacao (%s, %s). Escolha outra: "
                     "palavra nao se devolve."
                     % (palavra, a.get("_id") or a.get("id"), a.get("name") or ""))

    conta = os.environ.get("ZERNIO_IG_ACCOUNT_ID", "").strip()
    if not conta:
        erro("falta ZERNIO_IG_ACCOUNT_ID no .env: o funil e de Instagram.\n"
             "  Descubra o id com: flow-reels publicar/zernio contas")

    corpo_da_automacao["profileId"] = perfil_id()
    corpo_da_automacao["accountId"] = conta
    r = chamar("POST", "/comment-automations", corpo_da_automacao)
    if not r["ok"]:
        erro("a criacao do funil falhou: %s" % erro_de(r))
    dado = r["json"] or {}
    automacao = dado.get("automation") if isinstance(dado.get("automation"), dict) else dado
    ident = automacao.get("_id") or automacao.get("id")
    imprimir_json({"palavra": palavra, "link": link, "automationId": ident})
    print("\nfunil no ar: comentar \"%s\" responde em publico e manda a DM com o link."
          % palavra, file=sys.stderr)
    print("guarde o automationId: e por ele que se desliga a oferta.", file=sys.stderr)


def cmd_ligar_desligar(comando, argumentos):
    if not argumentos:
        erro("%s precisa do id da automacao" % comando)
    # Aposentar e PATCH de isActive, nunca DELETE: o objeto vivo e o que permite
    # reativar depois, e a palavra nao e devolvida de qualquer jeito.
    r = chamar("PATCH", "/comment-automations/%s" % argumentos[0],
               {"isActive": comando == "funil-ligar"})
    mostrar(comando, r)


def cmd_api(argumentos):
    if len(argumentos) < 2:
        erro("api precisa de <METODO> <caminho>")
    metodo, caminho = argumentos[0].upper(), argumentos[1]
    dados = corpo_do_argumento(argumentos[2]) if len(argumentos) > 2 else None
    mostrar("%s %s" % (metodo, caminho), chamar(metodo, caminho, dados))


def principal():
    argumentos = sys.argv[1:]
    seco = "--seco" in argumentos
    argumentos = [a for a in argumentos if a != "--seco"]
    comando = argumentos[0] if argumentos else "ajuda"
    resto = argumentos[1:]

    if comando in ("ajuda", "--help", "-h"):
        print(AJUDA)
    elif comando == "checar":
        cmd_checar()
    elif comando in ("contas", "perfis"):
        mostrar(comando, chamar("GET", "/accounts" if comando == "contas" else "/profiles"))
    elif comando == "midia":
        cmd_midia(resto)
    elif comando == "postar":
        cmd_postar(resto, seco)
    elif comando == "situacao":
        cmd_situacao(resto)
    elif comando == "palavras":
        cmd_palavras()
    elif comando == "funil":
        cmd_funil(resto, seco)
    elif comando in ("funil-ligar", "funil-desligar"):
        cmd_ligar_desligar(comando, resto)
    elif comando == "api":
        cmd_api(resto)
    else:
        erro("comando desconhecido \"%s\".\n\n%s" % (comando, AJUDA))


if __name__ == "__main__":
    principal()
