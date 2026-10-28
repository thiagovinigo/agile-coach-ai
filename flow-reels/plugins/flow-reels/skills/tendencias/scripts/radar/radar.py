# -*- coding: utf-8 -*-
"""Radar de tendencias: o que esta em alta sobre um tema, com numero e link.

E a camada de evidencia da entrada "tema" do `/flow-reels:tendencias`. Busca nas fontes que dao
engajamento de verdade e devolve um resumo que a skill transforma no brief:

    Reddit        sem chave. RSS, listagem com voto, arctic-shift e comentarios
    Hacker News   sem chave. Algolia, com os comentarios das mais votadas
    YouTube       sem chave. yt-dlp, regiao Brasil, com a transcricao dos mais vistos
    X             opcional, com XAI_API_KEY no .env
    reforco       opcional, com OPENAI_API_KEY: so entra se o Reddit voltar vazio

A web (blogs, noticias, documentacao) nao sai daqui: quem busca e a propria
skill, com a ferramenta WebSearch, depois de ler este resumo.

Dois passes. O primeiro roda o tema em portugues. Toda fonte que voltar fraca
roda de novo com o --termo-en, e o resumo diz quanto veio de cada passe.

Uso:

    flow-reels tendencias/radar "creatina" --termo-en "creatine" --rapida
    flow-reels tendencias/radar "agentes de IA para programar" --termo-en "AI coding agents"
    flow-reels tendencias/radar "investimento em renda fixa" --termo-en "fixed income" \\
        --subreddits investimentos,farialimabets --dias 14
    flow-reels tendencias/radar "creatina" --recentes

Saida: o resumo no stdout, e o material bruto em
pautas/radar/.bruto/<AAAA-MM-DD>-<tema>/ na raiz do pacote.

So usa a biblioteca padrao. O YouTube precisa do yt-dlp no PATH.
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import (  # noqa: E402
    ambiente, consulta, datas, hackernews, modelos, ordenacao, rede, reddit_openai,
    reddit_sem_chave, relatorio, x_xai, youtube,
)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FONTES = ["reddit", "hackernews", "youtube", "x"]
PREFIXO_DO_ID = {"reddit": "R", "hackernews": "H", "youtube": "Y", "x": "X"}

# Abaixo disto, a fonte e considerada fraca no portugues e roda o passe em ingles.
LIMIAR_FRACO = {"rapida": 3, "padrao": 5, "funda": 8}


# ------------------------------------------------------------------- uma fonte

def _rodar_fonte(nome, termo, idioma, ctx):
    """Roda uma fonte num termo. Devolve (itens, erro, bruto)."""
    try:
        if nome == "reddit":
            itens = reddit_sem_chave.buscar(termo, ctx["de"], ctx["ate"], ctx["profundidade"],
                                            subreddits=ctx["subreddits"], periodo=ctx["periodo"])
            return itens, None, None
        if nome == "hackernews":
            return hackernews.buscar(termo, ctx["de"], ctx["ate"], ctx["profundidade"]), None, None
        if nome == "youtube":
            return youtube.buscar(termo, ctx["dias"], ctx["profundidade"], idioma), None, None
        if nome == "x":
            itens, bruto = x_xai.buscar(ctx["config"]["XAI_API_KEY"], ctx["modelos"]["xai"], termo,
                                        ctx["de"], ctx["ate"], ctx["profundidade"], idioma)
            return itens, None, bruto
    except rede.ErroHTTP as e:
        return [], f"erro da API: {e}", None
    except Exception as e:
        return [], f"{type(e).__name__}: {e}", None
    return [], "fonte desconhecida", None


def _juntar(antigos, novos, passe):
    urls = {(i.get("url") or "").lower().rstrip("/") for i in antigos}
    for item in novos:
        item["passe"] = passe
        if (item.get("url") or "").lower().rstrip("/") not in urls:
            antigos.append(item)
    return antigos


def _situacao_reddit(itens, erro):
    """Diz por que o Reddit voltou como voltou, sem chute."""
    falhas = rede.falhas_do_host("reddit.com")
    bloqueios = falhas.get("429", 0) + falhas.get("403", 0)
    if itens:
        obs = (f"o Reddit respondeu {falhas.get('429', 0)} vezes 429 e {falhas.get('403', 0)} "
               f"vezes 403 no caminho, então a lista pode estar incompleta") if bloqueios else ""
        return "ok", obs
    if erro:
        return f"erro ({erro})", ""
    if falhas.get("429"):
        return f"limitado (429, {falhas['429']} respostas)", "espere um minuto e rode de novo"
    if falhas.get("403"):
        return f"bloqueado (403, {falhas['403']} respostas)", ""
    if falhas.get("rede") or falhas.get("conexao"):
        return "sem conexão com o Reddit", ""
    return "vazio de verdade", ""


# ------------------------------------------------------------------- a busca

def pesquisar(args, config):
    de, ate = datas.janela(args.dias)
    profundidade = args.profundidade
    selecionados = modelos.escolher(config)
    ctx = {
        "de": de, "ate": ate, "dias": args.dias, "profundidade": profundidade,
        "periodo": datas.periodo_reddit(args.dias), "config": config, "modelos": selecionados,
        "subreddits": [s.strip().removeprefix("r/") for s in (args.subreddits or "").split(",") if s.strip()],
    }

    pedidas = [f.strip() for f in args.fontes.split(",") if f.strip()] if args.fontes else list(FONTES)
    cobertura = {nome: {} for nome in FONTES}
    itens = {nome: [] for nome in FONTES}
    erros = {nome: None for nome in FONTES}
    brutos = {}

    ativas = []
    for nome in FONTES:
        if nome not in pedidas:
            cobertura[nome] = {"situacao": "não pedida nesta busca"}
        elif nome == "x" and not config.get("XAI_API_KEY"):
            cobertura[nome] = {"situacao": "não configurado (falta XAI_API_KEY no .env)"}
        elif nome == "youtube" and not youtube.disponivel():
            cobertura[nome] = {"situacao": "não instalado (falta o yt-dlp no PATH)"}
        else:
            ativas.append(nome)

    idioma_1 = args.idioma
    rotulo_1 = "pt" if idioma_1 == "pt" else "en"
    termo_1 = args.tema
    rede.log("radar", f"passe 1 em {'português' if rotulo_1 == 'pt' else 'inglês'}: '{termo_1}', "
                      f"{args.dias} dias, profundidade {profundidade}")

    with ThreadPoolExecutor(max_workers=4) as ex:
        futuros = {nome: ex.submit(_rodar_fonte, nome, termo_1, idioma_1, ctx) for nome in ativas}
        for nome, f in futuros.items():
            achados, erro, bruto = f.result()
            itens[nome] = _juntar([], achados, rotulo_1)
            erros[nome] = erro
            cobertura[nome][rotulo_1] = len(achados)
            if bruto:
                brutos[f"{nome}-{rotulo_1}"] = bruto

    # Passe 2: so para quem voltou fraco, e so se existir termo em ingles.
    limiar = LIMIAR_FRACO[profundidade]
    fracas = [n for n in ativas if len(itens[n]) < limiar]
    if rotulo_1 == "pt" and fracas:
        if args.termo_en:
            rede.log("radar", f"passe 2 em inglês: '{args.termo_en}' para {', '.join(fracas)}")
            with ThreadPoolExecutor(max_workers=4) as ex:
                futuros = {n: ex.submit(_rodar_fonte, n, args.termo_en, "en", ctx) for n in fracas}
                for nome, f in futuros.items():
                    achados, erro, bruto = f.result()
                    cobertura[nome]["en"] = len(achados)
                    _juntar(itens[nome], achados, "en")
                    if erro and not itens[nome]:
                        erros[nome] = erro
                    if bruto:
                        brutos[f"{nome}-en"] = bruto
        else:
            for nome in fracas:
                cobertura[nome]["observacao"] = ("fraco em português e sem --termo-en, "
                                                 "então o passe em inglês não rodou")

    # Reforco pela OpenAI: so com o Reddit vazio depois dos dois passes.
    if "reddit" in ativas and not itens["reddit"] and config.get("OPENAI_API_KEY"):
        modelo = modelos.openai_sob_demanda(config)
        selecionados["openai"] = modelo
        rede.log("radar", f"Reddit vazio sem chave; tentando o reforço pela OpenAI ({modelo})")
        try:
            achados, bruto = reddit_openai.buscar(config["OPENAI_API_KEY"], modelo, args.tema, de, ate,
                                                  profundidade, args.idioma)
            brutos["reddit-openai"] = bruto
            reddit_sem_chave.completar_votos(achados)
            achados = reddit_sem_chave.comentar(achados, profundidade)
            _juntar(itens["reddit"], achados, "openai")
            cobertura["reddit"]["openai"] = len(achados)
            cobertura["reddit"]["observacao"] = "threads achadas pela OpenAI, voto e comentário do próprio Reddit"
        except Exception as e:
            cobertura["reddit"]["observacao"] = f"o reforço pela OpenAI falhou: {e}"

    # Situacao final de cada fonte ativa.
    for nome in ativas:
        cob = cobertura[nome]
        if nome == "reddit":
            situacao, obs = _situacao_reddit(itens[nome], erros[nome])
            if obs:
                cob["observacao"] = "; ".join(x for x in (cob.get("observacao"), obs) if x)
        elif itens[nome]:
            situacao = "ok"
        elif erros[nome] and "429" in erros[nome]:
            situacao = "limitado (429)"
        elif erros[nome]:
            situacao = f"erro ({erros[nome]})"
        elif nome == "youtube" and youtube.LIMITADOS.get("busca"):
            situacao = "limitado (429)"
        else:
            situacao = "vazio de verdade"
        if nome == "youtube" and itens[nome]:
            com_fala = sum(1 for i in itens[nome] if i.get("transcricao"))
            obs = f"{com_fala} com transcrição"
            if youtube.LIMITADOS.get("transcricao"):
                obs += (f"; o YouTube limitou (429) {youtube.LIMITADOS['transcricao']} "
                        f"pedidos de legenda")
            cob["observacao"] = "; ".join(x for x in (cob.get("observacao"), obs) if x)
        cob["situacao"] = situacao

    # Nota, ordem, repeticao e id curto, fonte por fonte.
    for nome in FONTES:
        lista = ordenacao.pontuar(itens[nome], de, ate, args.dias)
        lista = ordenacao.sem_repeticao(lista)
        for n, item in enumerate(lista, 1):
            item["id"] = f"{PREFIXO_DO_ID[nome]}{n}"
            item.pop("post_id", None)
        itens[nome] = lista
        if nome in ativas:
            cobertura[nome]["total"] = len(lista)

    rel = {
        "tema": args.tema,
        "termo_en": args.termo_en,
        "idioma": args.idioma,
        "janela_dias": args.dias,
        "de": de,
        "ate": ate,
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profundidade": profundidade,
        "subreddits": ctx["subreddits"],
        "modelos": selecionados,
        "fontes": {n: {"cobertura": cobertura[n], "itens": itens[n]} for n in FONTES},
    }
    return rel, brutos


# ------------------------------------------------------------ briefs recentes

def briefs_recentes(tema: str, dias: int = 7):
    """Briefs em pautas/radar/ dos ultimos `dias` dias que dividem palavra com o tema."""
    pasta = ambiente.PASTA_DO_RADAR
    if not pasta.exists():
        return []
    alvo = set(consulta.slug(consulta.extrair_assunto(tema)).split("-")) - {""}
    limite = date.today() - timedelta(days=dias)
    achados = []
    for arquivo in sorted(pasta.glob("*.md"), reverse=True):
        nome = arquivo.stem
        try:
            quando = date.fromisoformat(nome[:10])
        except ValueError:
            continue
        if quando < limite:
            continue
        palavras = set(nome[11:].split("-"))
        comum = alvo & palavras
        if comum and len(comum) >= max(1, len(alvo) // 2):
            achados.append((quando.isoformat(), arquivo))
    return achados


def bloco_da_web(rel) -> str:
    termo_en = rel.get("termo_en")
    linhas = [
        "",
        "=" * 60,
        "### AGORA A WEB, PELA FERRAMENTA WebSearch ###",
        "=" * 60,
        f"Tema: {rel['tema']}",
        f"Janela: {rel['de']} a {rel['ate']}",
        "Busque em português primeiro (blogs, notícias, documentação, sites brasileiros).",
    ]
    if termo_en:
        linhas.append(f"Se o português vier fraco, repita em inglês com: {termo_en}")
    linhas += [
        "NÃO busque reddit.com, x.com nem twitter.com: essas fontes já vieram daqui.",
        "=" * 60,
    ]
    return "\n".join(linhas)


# ---------------------------------------------------------------------- main

class _AjudaEmPortugues(argparse.HelpFormatter):
    """O argparse escreve 'usage:' em ingles. Aqui vira 'uso:'."""

    def add_usage(self, usage, actions, groups, prefix=None):
        return super().add_usage(usage, actions, groups, prefix or "uso: ")


def principal():
    p = argparse.ArgumentParser(
        prog="radar.py",
        add_help=False,
        formatter_class=_AjudaEmPortugues,
        description="Pesquisa o que está em alta sobre um tema no Reddit, Hacker News, YouTube e X.",
        epilog="Exemplo: flow-reels tendencias/radar \"creatina\" --termo-en \"creatine\" --rapida",
    )
    p._positionals.title = "argumentos"
    p._optionals.title = "opções"
    p.add_argument("-h", "--help", action="help", help="mostra esta ajuda e sai")
    p.add_argument("tema", nargs="?", help="o tema a pesquisar, do jeito que a pessoa falou")
    p.add_argument("--termo-en", help="o mesmo tema em inglês, para o segundo passe quando o português vier fraco")
    p.add_argument("--idioma", choices=["pt", "en"], default="pt",
                   help="idioma do primeiro passe (padrão: pt)")
    p.add_argument("--dias", type=int, default=30, help="tamanho da janela em dias (padrão: 30)")
    prof = p.add_mutually_exclusive_group()
    prof.add_argument("--rapida", dest="profundidade", action="store_const", const="rapida",
                      help="menos itens e menos comentários, mais rápido")
    prof.add_argument("--funda", dest="profundidade", action="store_const", const="funda",
                      help="mais itens, mais comentários e mais transcrições")
    p.set_defaults(profundidade="padrao")
    p.add_argument("--fontes", help="só estas fontes, separadas por vírgula: reddit,hackernews,youtube,x")
    p.add_argument("--subreddits", help="subreddits para buscar dentro, separados por vírgula, sem o r/")
    p.add_argument("--saida", choices=["compacto", "json", "caminho"], default="compacto",
                   help="o que imprimir no fim (padrão: compacto)")
    p.add_argument("--recentes", action="store_true",
                   help="só lista briefs do mesmo tema feitos nos últimos 7 dias, sem pesquisar")
    p.add_argument("--depurar", action="store_true", help="mostra cada pedido de rede")
    args = p.parse_args()

    if not args.tema:
        p.print_help()
        print("\nfaltou o tema. Exemplo: flow-reels tendencias/radar \"creatina\" --termo-en \"creatine\"",
              file=sys.stderr)
        sys.exit(1)
    if args.dias < 1 or args.dias > 365:
        print("a janela vai de 1 a 365 dias.", file=sys.stderr)
        sys.exit(1)
    if args.fontes:
        desconhecidas = [f for f in args.fontes.split(",") if f.strip() and f.strip() not in FONTES]
        if desconhecidas:
            print(f"fonte desconhecida: {', '.join(desconhecidas)}. Use: {', '.join(FONTES)}",
                  file=sys.stderr)
            sys.exit(1)
    if args.depurar:
        os.environ["RADAR_DEPURAR"] = "1"

    if args.recentes:
        achados = briefs_recentes(args.tema)
        if not achados:
            print("nenhum brief deste tema nos últimos 7 dias.")
        for quando, arquivo in achados:
            print(f"{quando}  {arquivo}")
        return

    config = ambiente.configuracao()
    rel, brutos = pesquisar(args, config)
    pasta = relatorio.gravar(rel, brutos)

    if args.saida == "json":
        print(json.dumps(rel, ensure_ascii=False, indent=2))
    elif args.saida == "caminho":
        print(pasta)
    else:
        print(relatorio.compacto(rel))
        print(f"\nMaterial bruto em: {pasta}")
        print(bloco_da_web(rel))


if __name__ == "__main__":
    principal()
