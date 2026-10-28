# -*- coding: utf-8 -*-
"""Chaves e caminhos do radar.

Le o .env da raiz do pacote, decide quais fontes pagas estao configuradas e
diz onde gravar o material bruto. Nenhuma chave e obrigatoria: Reddit, Hacker
News e YouTube rodam sem chave. XAI_API_KEY liga o X, e OPENAI_API_KEY so
entra como reforco do Reddit quando a busca sem chave volta vazia.
"""

import os
from pathlib import Path
from typing import Dict, Optional

def _achar_raiz() -> Path:
    """A pasta de trabalho (onde moram o setup.json, o .env e as pautas), pelo lib/fabrica.py do plugin."""
    import sys
    aqui = Path(__file__).resolve()
    lib = next(p for p in aqui.parents if (p / ".claude-plugin").is_dir()) / "lib"
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
    import fabrica
    return fabrica.raiz()


def _pasta_das_pautas(raiz: Path) -> Path:
    """setup.json -> caminhos.pautas (padrao "pautas"), relativo a raiz."""
    try:
        import json
        setup = json.loads((raiz / "setup.json").read_text(encoding="utf-8"))
        return raiz / (setup.get("caminhos", {}).get("pautas") or "pautas")
    except (OSError, ValueError):
        return raiz / "pautas"


RAIZ_DO_PACOTE = _achar_raiz()

# A busca por tema grava ao lado das varreduras do nicho: pautas/radar/<data>-<tema>.md
PASTA_DO_RADAR = _pasta_das_pautas(RAIZ_DO_PACOTE) / "radar"
PASTA_BRUTA = PASTA_DO_RADAR / ".bruto"


def carregar_env(inicio=None) -> Optional[Path]:
    """Le o .env do pacote e joga o conteudo no ambiente.

    Procura na raiz do pacote e na pasta de onde o comando foi rodado, mais as
    pastas acima dela ATE a raiz do pacote. De proposito ele NAO sai do pacote
    subindo: credencial de outra ferramenta, guardada num .env pessoal mais acima,
    nunca deve entrar numa chamada que este script faz.

    Nao sobrescreve variavel que ja existe no ambiente, porque quem exportou na
    mao tem prioridade sobre arquivo.
    """
    raiz = RAIZ_DO_PACOTE
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


def configuracao() -> Dict[str, Optional[str]]:
    """Carrega o .env e devolve so as chaves que o radar usa."""
    carregar_env()
    return {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY") or None,
        "XAI_API_KEY": os.environ.get("XAI_API_KEY") or None,
        # Opcionais: fixam o modelo em vez de deixar o radar escolher.
        "RADAR_MODELO_OPENAI": os.environ.get("RADAR_MODELO_OPENAI") or None,
        "RADAR_MODELO_XAI": os.environ.get("RADAR_MODELO_XAI") or None,
    }
