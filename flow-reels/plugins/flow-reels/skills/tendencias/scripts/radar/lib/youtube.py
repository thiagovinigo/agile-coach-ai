# -*- coding: utf-8 -*-
"""YouTube sem chave, pelo yt-dlp instalado na maquina.

A busca roda na propria pagina de resultados do YouTube com o filtro de data de
envio, entao todo resultado ja cai dentro da janela sem pagar uma consulta por
video. Os mais vistos ganham a transcricao automatica, porque o que foi DITO
num video e a parte que nenhuma outra fonte traz.

Em portugues a busca vai com idioma pt e regiao BR. Isso nao e detalhe: sem o
idioma, o YouTube devolve o titulo de video brasileiro traduzido para o ingles,
e o brief citaria um titulo que ninguem escreveu.

Sem yt-dlp, ou com ele lento demais, devolve lista vazia, e o radar diz que o
YouTube nao rodou em vez de quebrar.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

from . import rede
from .ambiente import RAIZ_DO_PACOTE
from .relevancia import relevancia

# Filtros de data de envio da busca do YouTube (parametro sp=), ja com o tipo
# "video" junto, para nao vir canal nem playlist.
FILTROS = [
    (1, "EgQIAhAB", "hoje"),
    (7, "EgQIAxAB", "esta semana"),
    (31, "EgQIBBAB", "este mes"),
    (366, "EgQIBRAB", "este ano"),
]

QUANTIDADE = {"rapida": 6, "padrao": 12, "funda": 20}
TRANSCRITOS = {"rapida": 1, "padrao": 2, "funda": 3}
TEMPO_DA_BUSCA = 90
TEMPO_DA_TRANSCRICAO = 60
CARACTERES_DA_TRANSCRICAO = 4000


def _log(msg: str) -> None:
    rede.log("YouTube", msg)


def _ytdlp() -> Optional[str]:
    """O yt-dlp do PATH, ou o do .venv do pacote, que o instalador poe la."""
    achado = shutil.which("yt-dlp")
    if achado:
        return achado
    for nome in ("bin/yt-dlp", "Scripts/yt-dlp.exe"):
        local = RAIZ_DO_PACOTE / ".venv" / nome
        if local.is_file():
            return str(local)
    return None


def disponivel() -> bool:
    return _ytdlp() is not None


def filtro_da_janela(dias: int):
    """(codigo sp, rotulo) do menor filtro do YouTube que cobre a janela."""
    for limite, codigo, rotulo in FILTROS:
        if dias <= limite:
            return codigo, rotulo
    return FILTROS[-1][1], FILTROS[-1][2]


# Quantas vezes o YouTube respondeu 429 nesta execucao. Entra na cobertura.
LIMITADOS = {"transcricao": 0, "busca": 0}


def _rodar(args: List[str], tempo: int, etapa: str = "busca") -> Optional[str]:
    try:
        proc = subprocess.run(args, capture_output=True, timeout=tempo, text=True,
                              encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        _log(f"o yt-dlp passou de {tempo}s")
        return None
    except OSError as e:
        _log(f"o yt-dlp nao rodou: {e}")
        return None
    if "429" in (proc.stderr or ""):
        LIMITADOS[etapa] = LIMITADOS.get(etapa, 0) + 1
    if proc.returncode != 0 and not proc.stdout:
        _log(f"o yt-dlp saiu com codigo {proc.returncode}: {(proc.stderr or '').strip()[-200:]}")
        return None
    return proc.stdout


def _argumentos_de_idioma(idioma: str) -> List[str]:
    if idioma == "pt":
        return ["--extractor-args", "youtube:lang=pt", "--xff", "BR"]
    return ["--extractor-args", "youtube:lang=en"]


def _buscar(tema: str, dias: int, profundidade: str, idioma: str) -> List[Dict[str, Any]]:
    quantos = QUANTIDADE.get(profundidade, QUANTIDADE["padrao"])
    codigo, rotulo = filtro_da_janela(dias)
    url = f"https://www.youtube.com/results?search_query={quote_plus(tema)}&sp={codigo}"
    if idioma == "pt":
        url += "&hl=pt-BR&gl=BR"
    saida = _rodar([_ytdlp() or "yt-dlp", url, "--flat-playlist", "--dump-json", "--no-warnings",
                    "--playlist-end", str(quantos)] + _argumentos_de_idioma(idioma),
                   TEMPO_DA_BUSCA)
    if not saida:
        return []

    itens: List[Dict[str, Any]] = []
    for linha in saida.splitlines():
        linha = linha.strip()
        if not linha.startswith("{"):
            continue
        try:
            d = json.loads(linha)
        except json.JSONDecodeError:
            continue
        vid = d.get("id")
        if not vid:
            continue
        itens.append({
            "id": vid,
            "fonte": "youtube",
            "titulo": d.get("title") or "",
            "url": d.get("url") or f"https://www.youtube.com/watch?v={vid}",
            "autor": d.get("channel") or d.get("uploader") or "",
            # A busca rapida nao traz a data exata, so garante o filtro de envio.
            "data": None,
            "resumo": (d.get("description") or "")[:400],
            "duracao": d.get("duration"),
            "engajamento": {"visualizacoes": d.get("view_count")},
            "transcricao": "",
            "relevancia": round(relevancia(tema, d.get("title") or ""), 2),
            "motivo": f"YouTube, enviado {rotulo}",
        })
    _log(f"{len(itens)} videos")
    return itens


def _ler_vtt(texto: str) -> str:
    """Achata um arquivo de legenda WebVTT em prosa, sem as linhas repetidas."""
    linhas: List[str] = []
    for bruta in texto.splitlines():
        linha = bruta.strip()
        if not linha or linha.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or "-->" in linha:
            continue
        linha = re.sub(r"<[^>]+>", "", linha)
        if linha and (not linhas or linhas[-1] != linha):
            linhas.append(linha)
    saida: List[str] = []
    for linha in linhas:
        # A legenda automatica repete a linha anterior como janela que rola.
        if saida and (linha in saida[-1] or saida[-1].endswith(linha)):
            continue
        saida.append(linha)
    return " ".join(saida)


def _baixar_legenda(url: str, faixas: str, automatica: bool) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        args = [_ytdlp() or "yt-dlp", url, "--skip-download", "--sub-langs", faixas, "--sub-format", "vtt",
                "--no-warnings", "-o", os.path.join(tmp, "legenda")]
        args.append("--write-auto-subs" if automatica else "--write-subs")
        _rodar(args, TEMPO_DA_TRANSCRICAO, etapa="transcricao")
        for nome in sorted(os.listdir(tmp)):
            if nome.endswith(".vtt"):
                try:
                    with open(os.path.join(tmp, nome), encoding="utf-8", errors="replace") as f:
                        return _ler_vtt(f.read())[:CARACTERES_DA_TRANSCRICAO]
                except OSError:
                    return ""
    return ""


def transcricao(url: str, idioma: str = "pt") -> str:
    """Legenda do video como texto. Vazio se nao houver.

    Pede a faixa automatica ORIGINAL (sufixo -orig), que e a fala reconhecida
    na lingua em que o video foi gravado, nesta ordem: a do idioma do radar, a do
    ingles, e por ultimo a legenda escrita a mao no idioma do radar. Duas faixas
    ficam de fora de proposito: a traduzida pelo YouTube, que responde 429 com
    muito mais frequencia, e o "qualquer -orig", porque video com audio dublado
    tem uma faixa original por lingua e a primeira em ordem alfabetica e arabe.
    """
    tentativas = [(f"{idioma}-orig", True)]
    if idioma != "en":
        tentativas.append(("en-orig", True))
    tentativas.append((f"{idioma}.*", False))
    for faixas, automatica in tentativas:
        texto = _baixar_legenda(url, faixas, automatica)
        if texto:
            return texto
    return ""


def buscar(tema: str, dias: int = 30, profundidade: str = "padrao",
           idioma: str = "pt") -> List[Dict[str, Any]]:
    """Busca na janela e transcreve os mais vistos. Nunca levanta erro."""
    if not disponivel():
        _log("yt-dlp nao instalado; YouTube fica de fora")
        return []
    itens = _buscar(tema, dias, profundidade, idioma)
    if not itens:
        return []
    itens.sort(key=lambda d: d["engajamento"].get("visualizacoes") or 0, reverse=True)
    feitos = 0
    for item in itens[: TRANSCRITOS.get(profundidade, 2)]:
        texto = transcricao(item["url"], idioma)
        if texto:
            item["transcricao"] = texto
            feitos += 1
    if feitos:
        _log(f"transcricao de {feitos} video(s)")
    return itens
