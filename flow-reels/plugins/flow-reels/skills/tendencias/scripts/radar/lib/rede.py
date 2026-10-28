# -*- coding: utf-8 -*-
"""Rede do radar: pedidos HTTP so com a biblioteca padrao.

Tres coisas moram aqui:

- `pedir`, o pedido com nova tentativa, que devolve JSON ou texto;
- `baixar_texto`, a versao que nunca levanta erro e devolve None, usada pelas
  camadas do Reddit que precisam cair para a proxima quando uma falha;
- o registro de falhas por host. E ele que permite dizer, no fim, que o Reddit
  voltou vazio porque respondeu 429, e nao porque o tema nao tem conversa.
"""

import gzip
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from typing import Any, Dict, Optional
from urllib.parse import urlparse

TEMPO_LIMITE = 30
TENTATIVAS = 3
ESPERA_ENTRE_TENTATIVAS = 1.0
AGENTE = "fabrica-de-cortes-radar/1.0"

# Algumas superficies do Reddit so respondem a um navegador comum.
AGENTE_NAVEGADOR = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def depurando() -> bool:
    return os.environ.get("RADAR_DEPURAR", "").lower() in ("1", "true", "sim", "yes")


def log(prefixo: str, mensagem: str) -> None:
    """Mensagem de andamento no stderr. Sai sempre, porque e o que mostra o que falhou."""
    sys.stderr.write(f"[{prefixo}] {mensagem}\n")
    sys.stderr.flush()


def depurar(mensagem: str) -> None:
    if depurando():
        sys.stderr.write(f"[depurar] {mensagem}\n")
        sys.stderr.flush()


class ErroHTTP(Exception):
    """Erro de pedido, com o codigo quando houver."""

    def __init__(self, mensagem: str, codigo: Optional[int] = None, corpo: Optional[str] = None):
        super().__init__(mensagem)
        self.codigo = codigo
        self.corpo = corpo


# ------------------------------------------------------------ registro de falhas

_trava_falhas = threading.Lock()
_falhas: Dict[str, Counter] = defaultdict(Counter)


def _registrar_falha(url: str, codigo) -> None:
    host = (urlparse(url).netloc or "").lower()
    with _trava_falhas:
        _falhas[host][str(codigo)] += 1


def falhas_do_host(trecho: str) -> Counter:
    """Soma das falhas de todo host que contem `trecho` (ex.: 'reddit.com')."""
    total = Counter()
    with _trava_falhas:
        for host, contagem in _falhas.items():
            if trecho in host:
                total.update(contagem)
    return total


# ---------------------------------------------------------------------- pedidos

def pedir(
    metodo: str,
    url: str,
    cabecalhos: Optional[Dict[str, str]] = None,
    corpo_json: Optional[Dict[str, Any]] = None,
    tempo_limite: int = TEMPO_LIMITE,
    tentativas: int = TENTATIVAS,
    texto: bool = False,
):
    """Faz o pedido e devolve o JSON decodificado, ou o texto cru com texto=True."""
    cabecalhos = dict(cabecalhos or {})
    cabecalhos.setdefault("User-Agent", AGENTE)
    dados = None
    if corpo_json is not None:
        dados = json.dumps(corpo_json).encode("utf-8")
        cabecalhos.setdefault("Content-Type", "application/json")

    pedido = urllib.request.Request(url, data=dados, headers=cabecalhos, method=metodo)
    depurar(f"{metodo} {url}")

    ultimo_erro = None
    for tentativa in range(tentativas):
        try:
            with urllib.request.urlopen(pedido, timeout=tempo_limite) as resposta:
                bruto = resposta.read()
                if resposta.headers.get("Content-Encoding", "").lower() == "gzip":
                    bruto = gzip.decompress(bruto)
                corpo = bruto.decode("utf-8", errors="replace")
                if texto:
                    return corpo
                return json.loads(corpo) if corpo else {}
        except urllib.error.HTTPError as e:
            corpo = None
            try:
                corpo = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            depurar(f"HTTP {e.code} em {url}")
            _registrar_falha(url, e.code)
            ultimo_erro = ErroHTTP(f"HTTP {e.code}: {e.reason}", e.code, corpo)
            # 4xx que nao e 429 nao melhora tentando de novo.
            if 400 <= e.code < 500 and e.code != 429:
                raise ultimo_erro
        except urllib.error.URLError as e:
            _registrar_falha(url, "rede")
            ultimo_erro = ErroHTTP(f"erro de rede: {e.reason}")
        except json.JSONDecodeError as e:
            raise ErroHTTP(f"resposta nao e JSON valido: {e}")
        except (OSError, TimeoutError) as e:
            _registrar_falha(url, "conexao")
            ultimo_erro = ErroHTTP(f"erro de conexao: {type(e).__name__}: {e}")
        if tentativa < tentativas - 1:
            time.sleep(ESPERA_ENTRE_TENTATIVAS * (tentativa + 1))

    raise ultimo_erro or ErroHTTP("o pedido falhou sem detalhe")


def obter(url: str, cabecalhos: Optional[Dict[str, str]] = None, **kw):
    return pedir("GET", url, cabecalhos=cabecalhos, **kw)


def enviar(url: str, corpo_json: Dict[str, Any], cabecalhos: Optional[Dict[str, str]] = None, **kw):
    return pedir("POST", url, cabecalhos=cabecalhos, corpo_json=corpo_json, **kw)


def baixar_texto(
    url: str,
    tempo_limite: int = TEMPO_LIMITE,
    tentativas: int = 2,
    aceita: str = "*/*",
    cabecalhos: Optional[Dict[str, str]] = None,
) -> Optional[str]:
    """Baixa como texto com cara de navegador. Devolve None em qualquer falha."""
    juntos = {
        "User-Agent": AGENTE_NAVEGADOR,
        "Accept": aceita,
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    }
    if cabecalhos:
        juntos.update(cabecalhos)
    try:
        return pedir("GET", url, cabecalhos=juntos, tempo_limite=tempo_limite,
                     tentativas=tentativas, texto=True)
    except ErroHTTP as e:
        depurar(f"baixar_texto falhou ({e}): {url}")
        return None


# ------------------------------------------------------------- freio do Reddit

class Freio:
    """Balde de fichas dividido por todas as camadas do Reddit sem chave.

    Sem ele, uma busca com varios feeds em paralelo bate no mesmo host ao mesmo
    tempo e ganha um 429 logo no primeiro segundo.
    """

    def __init__(self, por_segundo: float, rajada: Optional[int] = None):
        self.taxa = por_segundo
        self.capacidade = rajada if rajada is not None else max(1, int(por_segundo))
        self._fichas = float(self.capacidade)
        self._ultimo = time.monotonic()
        self._trava = threading.Lock()

    def esperar(self) -> None:
        while True:
            with self._trava:
                agora = time.monotonic()
                passou = max(0.0, agora - self._ultimo)
                self._fichas = min(self.capacidade, self._fichas + passou * self.taxa)
                self._ultimo = agora
                if self._fichas >= 1.0:
                    self._fichas -= 1.0
                    return
                espera = (1.0 - self._fichas) / self.taxa
            time.sleep(espera)


# Dois pedidos por segundo, com rajada de tres. Mais que isso e o Reddit sem
# chave comeca a responder 429 ja na segunda busca seguida.
FREIO_REDDIT = Freio(por_segundo=2.0, rajada=3)


def baixar_texto_reddit(url: str, **kw) -> Optional[str]:
    """baixar_texto passando pelo freio comum do Reddit."""
    FREIO_REDDIT.esperar()
    return baixar_texto(url, **kw)
