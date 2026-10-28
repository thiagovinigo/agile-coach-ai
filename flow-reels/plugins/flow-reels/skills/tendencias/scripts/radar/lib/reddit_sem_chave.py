# -*- coding: utf-8 -*-
"""Reddit sem chave: descobre, completa o voto e traz os comentarios.

Nao precisa de chave nem custa nada por busca. A ordem e esta:

  Descoberta   os feeds RSS, com a busca global e, quando a skill passa
               subreddits, a busca e as listagens de cada um.
  Nota         a listagem do shreddit, que traz o voto real, e o arctic-shift
               para os posts que nenhuma listagem cobriu.
  Comentarios  os mais votados dos posts que mais importam, com autor e voto.

Devolve [] em vez de levantar erro, para o radar poder tentar o reforco pela
OpenAI quando ha chave, ou dizer que o Reddit voltou vazio e por que.
"""

import concurrent.futures
import math
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from . import rede, reddit_arctic, reddit_comentarios, reddit_listagem, reddit_rss
from .relevancia import MINIMO_NO_TEMA, PISO_DE_RELEVANCIA, ConsultaPreparada, relevancia

ORCAMENTO_DE_COMENTARIOS = 45   # segundos somados para buscar todos os comentarios
TRABALHADORES = 4
MAX_SUBS_DERIVADOS = 5           # subreddits tirados do RSS, so para pegar voto


def _log(msg: str) -> None:
    rede.log("Reddit", msg)


def _chave_final(post: Dict[str, Any]) -> float:
    """Relevancia primeiro. O engajamento entra so como desempate, com teto de 0.25,
    pequeno demais para um post fora do tema passar na frente de um no tema."""
    eng = post.get("engajamento", {})
    total = (eng.get("votos") or 0) + (eng.get("comentarios") or 0)
    return (post.get("relevancia") or 0.0) + min(0.25, math.log10(total + 1) / 20.0)


def _subs_mais_frequentes(posts: List[Dict[str, Any]]) -> List[str]:
    contagem = Counter(p.get("comunidade", "") for p in posts if p.get("comunidade"))
    return [s for s, _ in contagem.most_common(MAX_SUBS_DERIVADOS)]


def _aplicar_votos(post: Dict[str, Any], nota: Dict[str, int]) -> None:
    post.setdefault("engajamento", {})
    post["engajamento"]["votos"] = nota["votos"]
    post["engajamento"]["comentarios"] = nota["comentarios"]


def completar_votos(posts: List[Dict[str, Any]]) -> int:
    """Preenche pelo arctic-shift o voto de quem ainda esta sem. Devolve quantos encheu."""
    falta = [reddit_listagem.id_do_post(p["url"]) for p in posts
             if not p.get("engajamento", {}).get("votos")]
    falta = [pid for pid in falta if pid]
    if not falta:
        return 0
    votos = reddit_arctic.buscar_votos(falta)
    cheios = 0
    for p in posts:
        if p.get("engajamento", {}).get("votos"):
            continue
        pid = reddit_listagem.id_do_post(p["url"])
        if pid in votos:
            _aplicar_votos(p, votos[pid])
            cheios += 1
    return cheios


def _descobrir(tema: str, profundidade: str, subreddits: Optional[List[str]],
               periodo: str) -> List[Dict[str, Any]]:
    rss = reddit_rss.buscar(tema, profundidade=profundidade, subreddits=subreddits, periodo=periodo)

    if subreddits:
        # Subreddits escolhidos a dedo: o que a listagem deles traz esta no tema,
        # entao entra como descoberta e tambem como fonte de voto.
        listagem = reddit_listagem.buscar(subreddits, profundidade, tema, periodo=periodo)
        fonte_de_voto = listagem
    else:
        # Busca global: os subreddits tirados do RSS nao sao confiaveis como tema.
        # A listagem deles serve SO para dar voto aos posts do RSS. Misturar como
        # descoberta enche o resultado de post muito votado e fora do assunto.
        listagem = []
        fonte_de_voto = reddit_listagem.buscar(_subs_mais_frequentes(rss), profundidade,
                                               tema, periodo=periodo)
    _log(f"RSS {len(rss)} posts; listagem {'de descoberta ' + str(len(listagem)) if subreddits else 'so para voto'}; "
         f"{len(fonte_de_voto)} cartoes com nota")

    mapa = {p["post_id"]: p["engajamento"] for p in fonte_de_voto if p.get("post_id")}

    juntos: List[Dict[str, Any]] = []
    vistos = set()
    for p in listagem:
        if p["url"] not in vistos:
            vistos.add(p["url"])
            juntos.append(p)
    for p in rss:
        if p["url"] in vistos:
            continue
        pid = reddit_listagem.id_do_post(p["url"])
        if pid in mapa:
            _aplicar_votos(p, mapa[pid])
        vistos.add(p["url"])
        juntos.append(p)

    cheios = completar_votos(juntos)
    if cheios:
        _log(f"arctic-shift completou o voto de {cheios} posts")
    return juntos


def _comentar_um(post: Dict[str, Any]) -> Dict[str, Any]:
    try:
        dados = reddit_comentarios.buscar(post.get("url", ""))
        if dados["comentarios_destaque"]:
            post["comentarios_destaque"] = dados["comentarios_destaque"]
        if dados["ideias_dos_comentarios"]:
            post["ideias_dos_comentarios"] = dados["ideias_dos_comentarios"]
        if dados["total"] is not None:
            post.setdefault("engajamento", {})["comentarios"] = dados["total"]
    except Exception:
        pass  # fica o post com o que a descoberta trouxe
    return post


def comentar(posts: List[Dict[str, Any]], profundidade: str) -> List[Dict[str, Any]]:
    """Traz os comentarios dos primeiros N posts, dentro de um orcamento de tempo."""
    limite = reddit_comentarios.LIMITE_DE_POSTS.get(profundidade, 5)
    alvo, resto = posts[:limite], posts[limite:]
    if not alvo:
        return posts
    resultado: Dict[int, Dict[str, Any]] = {}
    try:
        with ThreadPoolExecutor(max_workers=min(limite, TRABALHADORES)) as ex:
            futuros = {ex.submit(_comentar_um, p): i for i, p in enumerate(alvo)}
            feitos, pendentes = concurrent.futures.wait(futuros, timeout=ORCAMENTO_DE_COMENTARIOS)
            for f in feitos:
                i = futuros[f]
                try:
                    resultado[i] = f.result(timeout=0)
                except Exception:
                    resultado[i] = alvo[i]
            for f in pendentes:
                resultado[futuros[f]] = alvo[futuros[f]]
                f.cancel()
        alvo = [resultado[i] for i in range(len(alvo))]
    except Exception:
        pass
    return alvo + resto


def _no_tema_primeiro(tema: str, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """As vagas de comentario sao poucas: vao primeiro para quem esta no tema.

    Gastar vaga em post muito votado que cai na ordenacao final deixa sem
    comentario justamente os posts que a pessoa vai ler.
    """
    prep = ConsultaPreparada(tema)
    no_tema, fora = [], []
    for p in posts:
        texto = f"{p.get('titulo') or ''} {p.get('texto') or ''}"
        (no_tema if relevancia(prep, texto) > 0.24 else fora).append(p)
    return no_tema + fora


def buscar(tema: str, de: str, ate: str, profundidade: str = "padrao",
           subreddits: Optional[List[str]] = None, periodo: str = "month") -> List[Dict[str, Any]]:
    """O caminho inteiro do Reddit sem chave."""
    posts = _descobrir(tema, profundidade, subreddits, periodo)
    if not posts:
        return []

    posts = [p for p in posts if p.get("data") is None or de <= p["data"] <= ate]

    # Post que veio de listagem, e nao de busca, so fica se casar com o tema.
    # A listagem traz o subreddit inteiro: sem este corte, "Que horas voce treina?"
    # entra numa pesquisa de creatina so porque mora em r/musculacaonatural.
    antes = len(posts)
    posts = [p for p in posts if p.get("origem") != "listagem" or (p.get("relevancia") or 0) > 0]
    if len(posts) < antes:
        _log(f"{antes - len(posts)} posts de listagem sairam por nao tocar no tema")
    if not posts:
        return []

    # Piso de relevancia: post sem nenhuma palavra do tema sai, desde que sobre o
    # bastante no tema. Sem isso, post muito votado de sub popular enterra o resto.
    antes = len(posts)
    no_tema = [p for p in posts if (p.get("relevancia") or 0) >= PISO_DE_RELEVANCIA]
    if len(no_tema) >= MINIMO_NO_TEMA:
        posts = no_tema
    else:
        algum = [p for p in posts if (p.get("relevancia") or 0) > 0]
        if algum:
            posts = algum
    if len(posts) < antes:
        _log(f"piso de relevancia tirou {antes - len(posts)} posts fora do tema")

    posts.sort(key=lambda p: (p.get("engajamento", {}).get("votos") or 0,
                              p.get("relevancia") or 0, p.get("data") or ""), reverse=True)
    posts = comentar(_no_tema_primeiro(tema, posts), profundidade)
    posts.sort(key=_chave_final, reverse=True)
    return posts
