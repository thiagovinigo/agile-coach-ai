# -*- coding: utf-8 -*-
"""Transcricao na nuvem: WhisperX large-v3 pela API da Replicate.

E a rota recomendada. Roda em poucos minutos, nao baixa modelo nenhum na sua
maquina e devolve tempo por palavra de qualidade de alinhamento, que e o que o
planejador precisa para cortar sem amputar fala.

Ela cobra por minuto de audio, poucos centavos por video. O script nao pede
confirmacao: quem configurou a chave ja escolheu essa rota.

Uso:

    flow-reels transcrever/replicate --entrada minha-aula.mp4 --projeto projetos/minha-aula
    flow-reels transcrever/replicate --entrada https://.../aula.mp4 --projeto projetos/aula

Saida: os tres arquivos do contrato, gravados pelo normalizar.py. A resposta crua
fica em materiais-de-trabalho/transcricao/bruto-replicate.json, dentro da pasta do
video, para o caso de precisar reprocessar sem gastar de novo (--reusar). Projeto
antigo, com o arquivo na raiz e com o nome velho, continua sendo reaproveitado.

So usa a biblioteca padrao. Nao precisa instalar nada.
"""

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import normalizar as nz  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


MODELO = "victor-upmeet/whisperx"
# Dois endpoints diferentes, e a escolha depende de quem publicou o modelo:
#   /v1/models/<dono>/<nome>/predictions  so funciona em modelo OFICIAL da Replicate
#   /v1/predictions  com o id da versao no corpo  e o caminho de modelo da COMUNIDADE
# O whisperx e da comunidade (is_official: false), entao o primeiro devolve 404.
# Por isso o script busca a versao mais recente antes de disparar.
API_MODELO = "https://api.replicate.com/v1/models/%s" % MODELO
API_PREDICOES = "https://api.replicate.com/v1/predictions"
AGENTE = "fabrica-de-cortes/1.0 (+https://replicate.com)"
API_ARQUIVOS = "https://api.replicate.com/v1/files"

INTERVALO_DE_CONSULTA = 5          # segundos entre uma consulta e outra
TEMPO_MAXIMO = 3600                # desiste depois de uma hora


# ------------------------------------------------------------------- chave

def carregar_env(inicio=None):
    """Le o .env do pacote e joga o conteudo no ambiente.

    Procura na raiz do pacote e na pasta de onde o comando foi rodado, mais as pastas
    acima dela ATE a raiz do pacote. De proposito ele NAO sai do pacote subindo.

    Por que o limite existe: a versao antiga subia ate a raiz do disco e, num teste, leu o
    .env pessoal da pasta do usuario e mandou a chave de outra ferramenta numa chamada de
    API. Credencial de terceiro nunca deve entrar numa chamada que este script faz.

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


def pegar_token():
    token = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if token:
        return token
    nz.erro(
        "não achei a chave REPLICATE_API_TOKEN.\n\n"
        "  Como resolver:\n"
        "  1. Crie uma chave em https://replicate.com/account/api-tokens\n"
        "  2. Copie o arquivo .env.exemplo da raiz do pacote para .env\n"
        "  3. Cole a chave na linha REPLICATE_API_TOKEN=\n\n"
        "  Se você não quer usar a nuvem, existe a rota gratuita:\n"
        "  uv run local.py --entrada <seu vídeo> --projeto <pasta do projeto>",
        codigo=3,
    )


# --------------------------------------------------------------------- http

def chamar(url, token, dados=None, metodo=None, corpo_bruto=None, content_type=None):
    # O User-Agent nao e enfeite: a Cloudflare da Replicate responde 403 com codigo 1010
    # ao User-Agent padrao do urllib ("Python-urllib/3.x"). Qualquer agente identificavel passa.
    cabecalhos = {"Authorization": "Bearer " + token, "User-Agent": AGENTE}
    corpo = None
    if dados is not None:
        corpo = json.dumps(dados).encode("utf-8")
        cabecalhos["Content-Type"] = "application/json"
    elif corpo_bruto is not None:
        corpo = corpo_bruto
        if content_type:
            cabecalhos["Content-Type"] = content_type

    requisicao = urllib.request.Request(url, data=corpo, headers=cabecalhos, method=metodo)
    try:
        with urllib.request.urlopen(requisicao, timeout=300) as resposta:
            return json.loads(resposta.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detalhe = ""
        try:
            detalhe = e.read().decode("utf-8", errors="ignore")[:500]
        except Exception:
            pass
        if e.code == 401:
            nz.erro("a Replicate recusou a chave (401). Confira o REPLICATE_API_TOKEN no seu .env.", 3)
        if e.code == 402:
            nz.erro("a Replicate pediu forma de pagamento (402). Cadastre um cartão na conta "
                    "ou use a rota local, que é gratuita.", 3)
        if e.code == 404:
            nz.erro("a Replicate devolveu 404 em %s.\n"
                    "  Se a URL for /v1/models/.../predictions, a causa provável é o modelo ser da\n"
                    "  comunidade: esse endpoint só vale para modelo oficial. O caminho certo é\n"
                    "  POST /v1/predictions com o id da versão no corpo." % url, 3)
        if e.code == 429:
            nz.erro("a Replicate está limitando as chamadas (429). Espere um minuto e tente de novo.", 4)
        nz.erro("a Replicate respondeu com erro %s.\n  %s" % (e.code, detalhe), 4)
    except urllib.error.URLError as e:
        nz.erro("não consegui falar com a Replicate (%s). Confira sua conexão." % e.reason, 4)


def enviar_arquivo(caminho, token):
    """Sobe o arquivo pela API de arquivos da Replicate e devolve a URL dele."""
    caminho = Path(caminho)
    tamanho_mb = caminho.stat().st_size / (1024 * 1024)
    if tamanho_mb > 100:
        nz.erro(
            "o arquivo tem %.0f MB e o limite de envio da Replicate é 100 MB.\n"
            "  Mande só o áudio, que é bem menor: o audio16k.wav que este script gera "
            "já serve.\n  Ou publique o arquivo numa URL e passe a URL em --entrada."
            % tamanho_mb
        )

    print("  Enviando %s (%.1f MB) para a Replicate..." % (caminho.name, tamanho_mb))

    fronteira = "----fabricadecortes" + uuid.uuid4().hex
    tipo = mimetypes.guess_type(caminho.name)[0] or "application/octet-stream"
    cabeca = (
        "--%s\r\n"
        'Content-Disposition: form-data; name="content"; filename="%s"\r\n'
        "Content-Type: %s\r\n\r\n" % (fronteira, caminho.name, tipo)
    ).encode("utf-8")
    rabo = ("\r\n--%s--\r\n" % fronteira).encode("utf-8")
    corpo = cabeca + caminho.read_bytes() + rabo

    resposta = chamar(
        API_ARQUIVOS, token,
        corpo_bruto=corpo,
        content_type="multipart/form-data; boundary=" + fronteira,
        metodo="POST",
    )
    url = (resposta.get("urls") or {}).get("get")
    if not url:
        nz.erro("o envio do arquivo não devolveu uma URL utilizável. Resposta: %s"
                % json.dumps(resposta)[:300])
    return url


# ------------------------------------------------------------------- aviso

def avisar(duracao):
    """Diz o que vai acontecer e segue. Sem pedir permissao.

    Decisao do dono do produto em 20/09: nada de estimativa de custo nem de confirmacao.
    A conta e de centavos, o pedido de confirmacao no meio do fluxo atrapalhava mais do que
    protegia, e quem configurou a chave ja sabe que a rota cobra.
    """
    print("")
    print("Transcrição na nuvem, WhisperX large-v3 na Replicate.")
    if duracao:
        print("  duração do áudio ....... %s" % nz.mmss(duracao))
    print("  tempo estimado ......... de 1 a 4 minutos")
    print("")


# --------------------------------------------------------------- predicao

def pegar_versao(token):
    """Descobre o id da versao mais recente do modelo.

    Modelo da comunidade nao tem endpoint proprio de predicao: a chamada vai para
    /v1/predictions e o corpo precisa dizer QUAL versao rodar. Esse id muda quando o
    autor publica uma versao nova, entao ele e buscado na hora em vez de ficar fixo no
    codigo, que envelheceria calado.
    """
    resposta = chamar(API_MODELO, token)
    versao = (resposta.get("latest_version") or {}).get("id")
    if not versao:
        nz.erro("a Replicate respondeu sobre o modelo %s mas não disse qual é a versão mais\n"
                "  recente. Veja se o modelo ainda existe em https://replicate.com/%s"
                % (MODELO, MODELO), 4)
    return versao


def criar_predicao(url_audio, token, idioma, vocabulario):
    entrada = {
        "audio_file": url_audio,
        # align_output vem desligado por padrao no modelo. Sem ele nao existe
        # tempo por palavra, e sem tempo por palavra nao da para cortar nem
        # legendar. E o parametro mais importante desta chamada.
        "align_output": True,
    }
    if idioma:
        entrada["language"] = idioma
    if vocabulario:
        # conserta o que o modelo OUVE, nao o que ele ja escreveu. Nomes proprios,
        # siglas e jargao do seu nicho entram aqui.
        entrada["initial_prompt"] = vocabulario

    versao = pegar_versao(token)
    print("  Criando a transcrição...")
    resposta = chamar(API_PREDICOES, token,
                      dados={"version": versao, "input": entrada}, metodo="POST")
    consulta = (resposta.get("urls") or {}).get("get")
    if not consulta:
        nz.erro("a Replicate aceitou o pedido mas não devolveu onde consultar o resultado.")
    return resposta, consulta


def esperar(consulta, token):
    inicio = time.time()
    ultimo_estado = None
    while True:
        atual = chamar(consulta, token)
        estado = atual.get("status")
        if estado != ultimo_estado:
            print("  status: %s" % estado)
            ultimo_estado = estado

        if estado == "succeeded":
            return atual
        if estado in ("failed", "canceled"):
            nz.erro("a transcrição terminou como %s.\n  %s"
                    % (estado, atual.get("error") or "sem detalhe da Replicate"))

        if time.time() - inicio > TEMPO_MAXIMO:
            nz.erro("passou de uma hora esperando e eu desisti.\n"
                    "  A transcrição pode ainda estar rodando em %s" % consulta)
        time.sleep(INTERVALO_DE_CONSULTA)


# ---------------------------------------------------------------------- cli

def main():
    parser = argparse.ArgumentParser(
        description="Transcreve com WhisperX large-v3 na Replicate e grava os três arquivos do contrato.",
        epilog="Exemplo: flow-reels transcrever/replicate --entrada aula.mp4 --projeto projetos/aula",
    )
    parser.add_argument("--entrada", required=True,
                        help="arquivo de vídeo ou áudio local, ou uma URL pública")
    parser.add_argument("--projeto", required=True,
                        help="diretório do projeto, onde os três arquivos vão cair")
    parser.add_argument("--idioma", default="pt",
                        help="idioma da fala (padrão: pt). Use vazio para deixar o modelo detectar")
    parser.add_argument("--vocabulario", default="",
                        help="palavras difíceis do seu nicho, separadas por vírgula, "
                             "para o modelo ouvir certo")
    parser.add_argument("--sim", action="store_true",
                        help="não faz mais nada. Existia para confirmar o custo, que saiu. "
                             "Fica aceito só para não quebrar comando já escrito.")
    parser.add_argument("--reusar", action="store_true",
                        help="não chama a API, reprocessa a resposta crua que já está no projeto")
    parser.add_argument("--sem-audio", action="store_true",
                        help="não extrair o audio16k.wav")

    if len(sys.argv) == 1:
        parser.print_help()
        print("\nEsta é a rota da nuvem: rápida, cobra poucos centavos por vídeo e não baixa\n"
              "modelo nenhum na sua máquina. A rota gratuita é o local.py, na mesma pasta.\n")
        sys.exit(2)

    args = parser.parse_args()
    projeto = Path(args.projeto)
    projeto.mkdir(parents=True, exist_ok=True)

    # A resposta crua e material de trabalho: mora com o resto dele, nunca na
    # raiz da pasta do video, que e o que a pessoa abre.
    pasta_transcricao = nz.pasta_transcricao(projeto)
    pasta_transcricao.mkdir(parents=True, exist_ok=True)
    bruto = pasta_transcricao / "bruto-replicate.json"
    bruto_antigo = projeto / "_bruto_replicate.json"   # onde ficava antes da arvore mudar

    entrada = str(args.entrada)
    e_url = entrada.lower().startswith(("http://", "https://"))
    arquivo_local = None
    if not e_url:
        arquivo_local = Path(entrada)
        if not arquivo_local.exists():
            nz.erro("não encontrei o arquivo %s.\n"
                    "  Se o vídeo está no YouTube ou no Drive, baixe primeiro:\n"
                    "  flow-reels transcrever/baixar --url <link> --projeto %s" % (arquivo_local, projeto))

    # rota curta: ja tem a resposta crua salva, so normaliza de novo
    if args.reusar:
        guardado = bruto if bruto.exists() else (bruto_antigo if bruto_antigo.exists() else None)
        if guardado is None:
            nz.erro("pedi --reusar mas não existe %s para reaproveitar." % bruto)
        print("Reaproveitando %s, sem chamar a Replicate." % guardado)
        dados = json.loads(guardado.read_text(encoding="utf-8"))
        nz.normalizar(
            dados, projeto=projeto,
            meta_extra={"fonte": entrada, "idioma": args.idioma or "detectado",
                        "motor": "whisperx large-v3 via replicate (align_output)",
                        "alinhado": True},
            video=entrada, gerar_audio=not args.sem_audio,
        )
        return

    carregar_env(projeto)
    token = pegar_token()

    # o audio16k.wav faz parte do contrato e tambem e o que sobe para a nuvem:
    # um wav de 16 kHz mono pesa uma fracao do video e evita o limite de 100 MB.
    caminho_audio = None
    if not args.sem_audio:
        caminho_audio = nz.extrair_audio(entrada, pasta_transcricao / "audio16k.wav")

    duracao = nz.duracao_do_arquivo(caminho_audio or entrada)
    avisar(duracao)

    if caminho_audio:
        url_audio = enviar_arquivo(caminho_audio, token)
    elif e_url:
        url_audio = entrada
    else:
        url_audio = enviar_arquivo(arquivo_local, token)

    _, consulta = criar_predicao(url_audio, token, args.idioma, args.vocabulario)
    pronto = esperar(consulta, token)

    saida = pronto.get("output")
    if not saida:
        nz.erro("a transcrição terminou sem saída nenhuma. Resposta: %s"
                % json.dumps(pronto)[:300])

    bruto.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    print("  Resposta crua guardada em %s" % bruto)

    idioma_detectado = args.idioma or saida.get("detected_language") or "detectado"
    nz.normalizar(
        saida, projeto=projeto,
        meta_extra={"fonte": entrada, "idioma": idioma_detectado,
                    "motor": "whisperx large-v3 via replicate (align_output)",
                    "alinhado": True,
                    "audio": nz.caminho_relativo_ao_projeto(caminho_audio, projeto)
                             if caminho_audio else None},
        video=entrada,
        # o wav ja foi extraido la em cima, nao precisa refazer
        gerar_audio=False,
    )
    if caminho_audio:
        print("  audio16k.wav    %s" % caminho_audio)


if __name__ == "__main__":
    main()
