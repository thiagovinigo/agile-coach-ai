# -*- coding: utf-8 -*-
"""
fabrica.py  ·  onde mora cada coisa no Flow Reels

São duas raízes, e cada arquivo sabe a qual pertence:

    o plugin   o código e o que o pacote traz: as skills, os componentes (peças, logos, sons,
               trilhas, modelos) e a marca de exemplo com as fontes livres. Achado subindo deste
               arquivo até a pasta que tem .claude-plugin/plugin.json. Muda a cada versão
               instalada, então nada se grava aqui.

    a pasta    a pasta de trabalho de quem usa: setup.json, .env, marca/, projetos/, pautas/ e o
               .venv. É a pasta onde o Claude Code foi aberto: a primeira, subindo do diretório
               atual, que tem um setup.json (sem nenhuma, o diretório atual). FLOW_REELS_RAIZ, se
               existir, vale mais que a busca.

Ler é sempre "primeiro a pasta, depois o plugin": achar("componentes/marcas/x.png") devolve o
arquivo da pasta se ele existe, e o do plugin se não. É assim que o logo baixado, a trilha escolhida
e a marca de um cliente moram na pasta de quem usa e valem por cima do que o pacote traz, sem nunca
mexer no plugin. Gravar é sempre na pasta (gravar("componentes/marcas")).

Os scripts acham este módulo com uma linha, que funciona de qualquer profundidade:

    sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents
                                if (p / ".claude-plugin").is_dir()) / "lib"))
    import fabrica
"""

import json
import os
from pathlib import Path

_PLUGIN = None


def plugin():
    """A raiz do plugin: a primeira pasta acima deste arquivo com .claude-plugin/plugin.json."""
    global _PLUGIN
    if _PLUGIN is None:
        aqui = Path(__file__).resolve()
        _PLUGIN = next((p for p in aqui.parents if (p / ".claude-plugin" / "plugin.json").is_file()),
                       aqui.parents[1])
    return _PLUGIN


def raiz():
    """A pasta de trabalho de quem usa (veja o topo deste arquivo)."""
    pedida = os.environ.get("FLOW_REELS_RAIZ")
    if pedida:
        return Path(pedida).expanduser().resolve()
    atual = Path.cwd().resolve()
    casa = Path.home().resolve()
    for pasta in [atual] + list(atual.parents):
        if (pasta / "setup.json").is_file():
            return pasta
        if pasta == casa:
            break
    return atual


def achar(relativo):
    """O arquivo (ou pasta) da pasta de trabalho, se existe; senão o do plugin; senão o caminho na pasta."""
    rel = Path(relativo)
    for base in (raiz(), plugin()):
        p = base / rel
        if p.exists():
            return p
    return raiz() / rel


def listar(relativo, padrao="*"):
    """Os arquivos das duas raízes numa pasta, sem repetir nome: o da pasta de trabalho vence."""
    vistos, out = set(), []
    for base in (raiz(), plugin()):
        d = base / relativo
        if not d.is_dir():
            continue
        for p in sorted(d.glob(padrao)):
            if p.name not in vistos:
                vistos.add(p.name)
                out.append(p)
    return out


class Sobreposta:
    """Uma pasta lida nas duas raízes, que se usa como um Path: pasta / "x.wav" acha o arquivo na
    pasta de trabalho ou no plugin, pasta.glob("whoosh-*.wav") junta as duas sem repetir nome, e
    str(pasta) é a primeira que existe (para mensagem). Serve para sons, modelos, LUTs e trilhas."""

    def __init__(self, relativo):
        self.rel = Path(relativo)

    def __truediv__(self, nome):
        return achar(self.rel / nome)

    def glob(self, padrao):
        return iter(listar(self.rel, padrao))

    def iterdir(self):
        return iter(listar(self.rel))

    def is_dir(self):
        return any((base / self.rel).is_dir() for base in (raiz(), plugin()))

    exists = is_dir

    @property
    def name(self):
        return self.rel.name

    def __fspath__(self):
        return str(achar(self.rel))

    def __str__(self):
        return str(achar(self.rel))

    def __repr__(self):
        return "Sobreposta(%r)" % str(self.rel)


def pasta(relativo):
    """A pasta lida nas duas raízes (veja Sobreposta)."""
    return Sobreposta(relativo)


def gravar(relativo):
    """O caminho para gravar, sempre na pasta de trabalho. Cria a pasta de cima se faltar."""
    p = raiz() / relativo
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def json_mesclado(relativo):
    """Um JSON de dicionário das duas raízes: o do plugin por baixo, o da pasta de trabalho por cima."""
    dados = {}
    for base in (plugin(), raiz()):
        p = base / relativo
        if p.is_file():
            try:
                lido = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(lido, dict):
                dados.update(lido)
    return dados


def setup():
    """O setup.json da pasta de trabalho, ou o de exemplo do plugin quando a pasta ainda não tem."""
    for p in (raiz() / "setup.json", plugin() / "modelo" / "setup.json"):
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                return {}
    return {}


def comando(skill_e_script):
    """Como escrever o comando de um script para a pessoa: flow-reels <skill>/<script>."""
    return "flow-reels " + skill_e_script
