# -*- coding: utf-8 -*-
"""Saida do radar: o resumo que vai para a conversa e os arquivos brutos.

O resumo compacto e o que a skill le para escrever o brief. Os arquivos brutos
ficam em pautas/radar/.bruto/<data>-<tema>/, dentro do pacote, para dar para
conferir um numero depois sem rodar a busca de novo.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from .ambiente import PASTA_BRUTA
from .consulta import slug

ROTULOS = {"reddit": "Reddit", "hackernews": "Hacker News", "youtube": "YouTube", "x": "X"}
ORDEM = ["reddit", "hackernews", "youtube", "x"]


def numero(n) -> str:
    """1234567 vira '1.234.567', no jeito brasileiro."""
    if n is None:
        return "?"
    try:
        return f"{int(n):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(n)


def _contagem(n, singular: str, plural: str) -> str:
    return f"{numero(n)} {singular if n == 1 else plural}"


def engajamento(item: Dict[str, Any]) -> str:
    e = item.get("engajamento") or {}
    fonte = item.get("fonte")
    partes: List[str] = []
    if fonte == "reddit":
        if e.get("votos"):
            partes.append(_contagem(e['votos'], 'voto', 'votos'))
        if e.get("comentarios"):
            partes.append(_contagem(e['comentarios'], 'comentário', 'comentários'))
    elif fonte == "hackernews":
        partes.append(_contagem(e.get('pontos'), 'ponto', 'pontos'))
        partes.append(_contagem(e.get('comentarios'), 'comentário', 'comentários'))
    elif fonte == "youtube":
        if e.get("visualizacoes") is not None:
            partes.append(_contagem(e['visualizacoes'], 'visualização', 'visualizações'))
    elif fonte == "x":
        if e.get("curtidas") is not None:
            partes.append(_contagem(e['curtidas'], 'curtida', 'curtidas'))
        if e.get("reposts") is not None:
            partes.append(_contagem(e['reposts'], 'repost', 'reposts'))
        if e.get("respostas") is not None:
            partes.append(_contagem(e['respostas'], 'resposta', 'respostas'))
    return ", ".join(partes) if partes else "sem número de engajamento"


def linha_de_cobertura(nome: str, cob: Dict[str, Any]) -> str:
    rotulo = ROTULOS[nome]
    situacao = cob.get("situacao", "")
    if situacao != "ok":
        texto = f"{rotulo}: {situacao}"
    else:
        texto = f"{rotulo}: {cob.get('total', 0)} itens"
    passes = []
    if cob.get("pt") is not None:
        passes.append(f"passe em português {cob['pt']}")
    if cob.get("en") is not None:
        passes.append(f"passe em inglês {cob['en']}")
    if passes:
        texto += f" ({', '.join(passes)})"
    if cob.get("observacao"):
        texto += f". {cob['observacao']}"
    return texto


def compacto(rel: Dict[str, Any], limite: int = 12) -> str:
    l: List[str] = []
    l.append(f"## Radar: {rel['tema']}")
    l.append("")
    l.append(f"**Janela:** {rel['de']} a {rel['ate']} ({rel['janela_dias']} dias)")
    l.append(f"**Profundidade:** {rel['profundidade']}  **Idioma:** {rel['idioma']}"
             + (f"  **Termo em inglês:** {rel['termo_en']}" if rel.get("termo_en") else ""))
    if rel.get("subreddits"):
        l.append(f"**Subreddits pedidos:** {', '.join('r/' + s for s in rel['subreddits'])}")
    l.append("")
    l.append("### Cobertura por fonte")
    for nome in ORDEM:
        l.append(f"- {linha_de_cobertura(nome, rel['fontes'][nome]['cobertura'])}")
    l.append("")

    for nome in ORDEM:
        itens = rel["fontes"][nome]["itens"]
        if not itens:
            continue
        l.append(f"### {ROTULOS[nome]}")
        l.append("")
        for it in itens[:limite]:
            onde = f"r/{it['comunidade']}" if nome == "reddit" and it.get("comunidade") else ""
            if nome == "x" and it.get("autor"):
                onde = f"@{it['autor']}"
            elif nome in ("youtube", "hackernews") and it.get("autor"):
                onde = it["autor"]
            data = it.get("data") or "data não confirmada"
            l.append(f"**{it['id']}** (nota {it.get('nota', 0)}, passe {it.get('passe', '?')}) "
                     f"{onde} ({data}) [{engajamento(it)}]")
            l.append(f"  {it.get('titulo') or ''}")
            l.append(f"  {it.get('url')}")
            if it.get("url_discussao") and it["url_discussao"] != it.get("url"):
                l.append(f"  discussão: {it['url_discussao']}")
            if nome == "x" and it.get("texto"):
                l.append(f"  {it['texto'][:280]}")
            comentarios = it.get("comentarios_destaque") or []
            if comentarios:
                l.append("  Comentários em destaque:")
                for c in comentarios[:3]:
                    quem = c.get("autor") or "[sem autor]"
                    if nome == "reddit":
                        quem = f"u/{quem}"
                    votos = f"[{_contagem(c['votos'], 'voto', 'votos')}] " if c.get("votos") else ""
                    l.append(f"    - {votos}{quem}: {c.get('trecho', '')}")
            elif it.get("ideias_dos_comentarios"):
                l.append("  Ideias dos comentários:")
                for ideia in it["ideias_dos_comentarios"][:3]:
                    l.append(f"    - {ideia}")
            if it.get("transcricao"):
                l.append(f"  Transcrição ({len(it['transcricao'])} caracteres):")
                l.append(f"    {it['transcricao']}")
            elif it.get("resumo") and not comentarios:
                l.append(f"  {it['resumo'][:200]}")
            l.append("")
    return "\n".join(l)


def pasta_bruta(rel: Dict[str, Any]) -> Path:
    return PASTA_BRUTA / f"{rel['ate']}-{slug(rel['tema'])}"


def gravar(rel: Dict[str, Any], brutos: Dict[str, Any]) -> Path:
    """Grava relatorio.json, relatorio.md e as respostas cruas das APIs pagas."""
    pasta = pasta_bruta(rel)
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "relatorio.json").write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
    (pasta / "relatorio.md").write_text(compacto(rel, limite=100), encoding="utf-8")
    for nome, conteudo in brutos.items():
        if conteudo:
            (pasta / f"bruto-{nome}.json").write_text(
                json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    return pasta
