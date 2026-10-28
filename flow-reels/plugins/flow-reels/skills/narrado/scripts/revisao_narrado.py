# -*- coding: utf-8 -*-
"""Sobe o reel narrado na MESMA pagina de revisao do pacote.

E o nova-revisao.py do `/flow-reels:produzir`, com uma diferenca so: alem das pastas
corte-NN, ele tambem acha as pastas narrado-NN do projeto, cada uma com o MP4 de
entrega sozinho dentro. O revisao.json, o modelo.html, o servidor, a porta do
setup.json e o botao "Copiar feedback" sao os do pacote, sem copia.

Titulo e gancho do reel vem do tomadas.json ("titulo") e da primeira frase do
roteiro-tts.txt. "porque" e "decisoes" quem escreve e quem produziu, no revisao.json,
antes de chamar a pessoa.

Uso (as opcoes sao as do nova-revisao.py):

    flow-reels narrado/revisao_narrado projetos/x
    flow-reels narrado/revisao_narrado projetos/x --lote "Lancamento X | reel narrado"
    flow-reels narrado/revisao_narrado projetos/x --sem-servidor
"""

import importlib.util
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum as cm  # noqa: E402

REVISAO = cm.PLUGIN / "skills" / "produzir" / "revisao" / "nova-revisao.py"


def carregar_revisao():
    if not REVISAO.is_file():
        cm.erro("nao achei a pagina de revisao do pacote em %s." % REVISAO)
    spec = importlib.util.spec_from_file_location("nova_revisao_do_pacote", str(REVISAO))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def principal(argv=None):
    mod = carregar_revisao()
    varrer_original = mod.varrer
    ler_brief_original = mod.ler_brief

    def varrer(projeto):
        achados, sem_video = varrer_original(projeto)
        for pasta in sorted(p for p in projeto.glob("narrado-*") if p.is_dir()):
            video = mod.video_do_corte(pasta)
            if video is None:
                sem_video.append(pasta.name)
            else:
                achados.append((pasta, video))
        return achados, sem_video

    def ler_brief(pasta):
        if not pasta.name.startswith("narrado-"):
            return ler_brief_original(pasta)
        achado = {"titulo": "", "gancho": ""}
        trabalho = pasta.parent / "materiais-de-trabalho" / pasta.name
        tomadas = trabalho / "tomadas.json"
        if tomadas.is_file():
            try:
                achado["titulo"] = str(cm.ler_json(tomadas).get("titulo", "")).strip()
            except Exception:
                pass
        roteiro = trabalho / "roteiro-tts.txt"
        if roteiro.is_file():
            texto = re.sub(r"\[[^\]]*\]", "", roteiro.read_text(encoding="utf-8")).strip()
            frase = re.split(r"(?<=[.?!])\s", texto, maxsplit=1)[0]
            achado["gancho"] = frase.strip()
        return achado

    mod.varrer = varrer
    mod.ler_brief = ler_brief
    argumentos = list(sys.argv[1:] if argv is None else argv)
    return mod.main(argumentos)


if __name__ == "__main__":
    sys.exit(principal())
