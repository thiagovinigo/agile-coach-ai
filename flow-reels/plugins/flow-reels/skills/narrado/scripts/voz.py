# -*- coding: utf-8 -*-
"""A voz do reel narrado: ElevenLabs, texto para fala COM tempo por caractere.

Os tempos por palavra saem da propria resposta da ElevenLabs (o alinhamento por
caractere), entao o corte das tomadas e a legenda caem no tempo real da fala.
Nenhuma transcricao entra aqui.

So roda depois que a pessoa aprovou o roteiro: cada chamada gasta credito.

Uso:

    flow-reels narrado/voz --checar
    flow-reels narrado/voz --projeto projetos/x --narrado 01 --take a --estabilidade 0.5
    flow-reels narrado/voz --projeto projetos/x --narrado 01 --take b --estabilidade 0.85 --similaridade 0.9
    flow-reels narrado/voz --projeto projetos/x --narrado 01 --take a --reusar

Le materiais-de-trabalho/narrado-NN/roteiro-tts.txt (ou --roteiro) e escreve em
materiais-de-trabalho/narrado-NN/voz/:

    voz-<take>.mp3           o audio, do jeito que veio, na velocidade natural
    palavras-<take>.json     {"palavras": [{"texto", "inicio", "fim"}], "meta": {...}}
    alinhamento-<take>.json  o alinhamento cru, para reprocessar sem gastar (--reusar)

Chaves no .env da raiz do pacote: ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID, as duas
obrigatorias. ELEVENLABS_MODELO e opcional (padrao eleven_multilingual_v2, que fala
portugues). A voz nunca e acelerada: o script nao manda velocidade nenhuma.

So usa a biblioteca padrao.
"""

import argparse
import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402

API = "https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128"
AGENTE = "fabrica-de-cortes/1.0"


# ------------------------------------------------------------------- alinhamento

def palavras_do_alinhamento(alinhamento):
    """Transforma o alinhamento por caractere da ElevenLabs em palavras com tempo.

    Entrada: {"characters": [...], "character_start_times_seconds": [...],
              "character_end_times_seconds": [...]}
    Saida: [{"texto", "inicio", "fim"}]

    Regras:
    - tudo entre colchetes e marcacao de interpretacao ([animado], [pausa]) e some;
    - espaco e quebra de linha separam palavras;
    - um pedaco sem letra nem numero (reticencias soltas, aspas soltas) gruda na
      palavra anterior, em vez de virar uma palavra muda na legenda.
    """
    chars = alinhamento.get("characters") or []
    inicios = alinhamento.get("character_start_times_seconds") or []
    fins = alinhamento.get("character_end_times_seconds") or []
    if not (len(chars) == len(inicios) == len(fins)):
        raise ValueError("alinhamento com listas de tamanhos diferentes")
    palavras, atual, t0, t1, dentro_de_tag = [], "", None, None, False

    def fechar():
        nonlocal atual
        if not atual:
            return
        if not any(c.isalnum() for c in atual) and palavras:
            palavras[-1]["texto"] += atual
            palavras[-1]["fim"] = round(t1, 3)
        elif any(c.isalnum() for c in atual):
            palavras.append({"texto": atual, "inicio": round(t0, 3), "fim": round(t1, 3)})
        atual = ""

    for c, a, b in zip(chars, inicios, fins):
        if c == "[":
            fechar()
            dentro_de_tag = True
            continue
        if dentro_de_tag:
            if c == "]":
                dentro_de_tag = False
            continue
        if c.isspace():
            fechar()
            continue
        if not atual:
            t0 = float(a)
        atual += c
        t1 = float(b)
    fechar()
    return palavras


def escolher_alinhamento(resposta):
    """Prefere o alinhamento do texto original (bate com o roteiro aprovado, que e o
    que a legenda mostra) e cai no normalizado quando o original nao vier."""
    for chave in ("alignment", "normalized_alignment"):
        al = resposta.get(chave)
        if al and al.get("characters"):
            return al, chave
    raise ValueError("a resposta nao trouxe alinhamento nenhum")


# ------------------------------------------------------------------- roteiro

def conferir_roteiro(texto, modelo):
    cm.recusar_travessao(texto, "o roteiro")
    tem_tag = "[" in texto and "]" in texto
    if tem_tag and not modelo.startswith("eleven_v3"):
        cm.erro("o roteiro tem marcacao entre colchetes, e o modelo %s le colchete em voz alta. "
                "Tire as marcacoes ou use --modelo eleven_v3." % modelo)
    sem_tags = []
    dentro = False
    for c in texto:
        if c == "[":
            dentro = True
        elif c == "]":
            dentro = False
        elif not dentro:
            sem_tags.append(c)
    n = len([p for p in "".join(sem_tags).split() if any(ch.isalnum() for ch in p)])
    if n < 90 or n > 130:
        cm.aviso("o roteiro tem %d palavras; o formato pede de 90 a 130 (de 40 a 50 s com a voz "
                 "natural). Siga so se a pessoa aprovou assim." % n)
    return n


# ------------------------------------------------------------------- chamada

def chamar(chave, voz, texto, modelo, ajustes):
    corpo = json.dumps({"text": texto, "model_id": modelo, "voice_settings": ajustes}).encode("utf-8")
    pedido = urllib.request.Request(API % voz, data=corpo, method="POST", headers={
        "xi-api-key": chave, "Content-Type": "application/json", "Accept": "application/json",
        "User-Agent": AGENTE})
    try:
        with urllib.request.urlopen(pedido, timeout=300) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")[:600]
        dica = ""
        if e.code == 401:
            dica = "A chave foi recusada. Confira ELEVENLABS_API_KEY no .env."
        elif e.code == 404 or "voice_not_found" in corpo:
            dica = "A voz nao foi encontrada nesta conta. Confira ELEVENLABS_VOICE_ID."
        elif e.code in (402, 429) or "quota" in corpo.lower() or "credit" in corpo.lower():
            dica = "Faltou credito ou o limite da conta estourou. Nada foi gravado."
        cm.erro("a ElevenLabs respondeu HTTP %d. %s\n  resposta: %s" % (e.code, dica, corpo))
    except urllib.error.URLError as e:
        cm.erro("nao consegui falar com a ElevenLabs (%s). Confira a rede." % e.reason)


def checar():
    arquivo = cm.carregar_env()
    chave, voz = cm.exigir_elevenlabs(precisa_voz=True)
    cm.fala("ElevenLabs configurada.")
    cm.fala("  .env lido: %s" % arquivo)
    cm.fala("  ELEVENLABS_API_KEY: presente (nao mostro o valor)")
    cm.fala("  ELEVENLABS_VOICE_ID: presente")
    cm.fala("  modelo: %s" % cm.modelo_padrao())
    return 0


def principal(argv=None):
    an = argparse.ArgumentParser(
        description="Gera uma tomada de voz pela ElevenLabs, com tempo por palavra.")
    an.add_argument("--checar", action="store_true",
                    help="so confere se as chaves estao no .env, sem gastar nada")
    an.add_argument("--projeto", help="pasta do projeto")
    an.add_argument("--narrado", default="01", help="numero do reel narrado (padrao 01)")
    an.add_argument("--take", default="a", help="nome da tomada de voz: a, b, c...")
    an.add_argument("--roteiro", default=None,
                    help="texto que vai para a voz (padrao: roteiro-tts.txt da pasta do reel)")
    an.add_argument("--modelo", default=None,
                    help="modelo da ElevenLabs (padrao: ELEVENLABS_MODELO ou eleven_multilingual_v2)")
    an.add_argument("--estabilidade", type=float, default=0.5,
                    help="0.5 para gancho animado, 0.85 para leitura calma (padrao 0.5)")
    an.add_argument("--similaridade", type=float, default=0.85,
                    help="de 0.8 a 0.9 (padrao 0.85)")
    an.add_argument("--estilo", type=float, default=None,
                    help="exagero de estilo, opcional (0 a 1). Deixe de fora se nao souber")
    an.add_argument("--reusar", action="store_true",
                    help="nao chama a API: refaz o palavras-<take>.json a partir do alinhamento guardado")
    op = an.parse_args(argv)

    if op.checar:
        return checar()
    if not op.projeto:
        an.print_help()
        return 2

    cam = cm.Caminhos(op.projeto, op.narrado)
    cam.voz.mkdir(parents=True, exist_ok=True)
    mp3 = cam.voz / ("voz-%s.mp3" % op.take)
    saida_palavras = cam.voz / ("palavras-%s.json" % op.take)
    cru = cam.voz / ("alinhamento-%s.json" % op.take)

    if op.reusar:
        if not cru.is_file():
            cm.erro("nao existe %s para reusar." % cru)
        guardado = cm.ler_json(cru)
        palavras = palavras_do_alinhamento(guardado["alinhamento"])
        cm.gravar_json(saida_palavras, {"palavras": palavras, "meta": guardado.get("meta", {})})
        cm.fala("%s refeito: %d palavras." % (saida_palavras, len(palavras)))
        return 0

    roteiro = Path(op.roteiro) if op.roteiro else cam.roteiro_tts
    if not roteiro.is_file():
        cm.erro("nao achei o roteiro em %s. Ele nasce depois que a pessoa aprova o texto." % roteiro)
    texto = roteiro.read_text(encoding="utf-8").strip()
    modelo = op.modelo or cm.modelo_padrao()
    n = conferir_roteiro(texto, modelo)

    chave, voz = cm.exigir_elevenlabs(precisa_voz=True)

    for nome, v in (("estabilidade", op.estabilidade), ("similaridade", op.similaridade)):
        if not 0.0 <= v <= 1.0:
            cm.erro("%s precisa ficar entre 0 e 1." % nome)
    if not 0.8 <= op.similaridade <= 0.9:
        cm.aviso("similaridade fora de 0.8 a 0.9; a voz pode sair menos parecida com ela mesma.")
    ajustes = {"stability": op.estabilidade, "similarity_boost": op.similaridade,
               "use_speaker_boost": True}
    if op.estilo is not None:
        ajustes["style"] = op.estilo

    cm.fala("gerando a tomada %s (%d palavras, modelo %s, estabilidade %.2f)..."
            % (op.take, n, modelo, op.estabilidade))
    resposta = chamar(chave, voz, texto, modelo, ajustes)
    if not resposta.get("audio_base64"):
        cm.erro("a resposta veio sem audio.")
    mp3.write_bytes(base64.b64decode(resposta["audio_base64"]))
    alinhamento, qual = escolher_alinhamento(resposta)
    palavras = palavras_do_alinhamento(alinhamento)
    meta = {"take": op.take, "modelo": modelo, "estabilidade": op.estabilidade,
            "similaridade": op.similaridade, "estilo": op.estilo, "alinhamento": qual,
            "palavras_no_roteiro": n}
    cm.gravar_json(cru, {"alinhamento": alinhamento, "meta": meta})
    cm.gravar_json(saida_palavras, {"palavras": palavras, "meta": meta})

    dur = palavras[-1]["fim"] if palavras else 0.0
    cm.fala("tomada %s pronta: %d palavras, %.2f s de fala, %.2f palavras por segundo."
            % (op.take, len(palavras), dur, len(palavras) / max(dur, 0.1)))
    cm.fala("  %s" % mp3)
    cm.fala("  %s" % saida_palavras)
    if len(palavras) != n:
        cm.aviso("o roteiro tem %d palavras e o alinhamento devolveu %d. Confira numeros e siglas "
                 "na legenda." % (n, len(palavras)))
    if dur > 48.5:
        cm.aviso("a fala passou de 48 s; com a cauda do fechamento o reel estoura 50 s. "
                 "Encurte o roteiro, nunca acelere a voz.")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
