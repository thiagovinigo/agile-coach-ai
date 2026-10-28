"""
DEMO PRINCIPAL — Bot Playwright + Claude monitora proposições na Câmara.

Caso de uso real: monitorar projetos de lei sobre um tema do seu interesse
(ex: "inteligência artificial", "saúde digital", "lgpd"), ler a ementa de cada
um e usar Claude para classificar relevância + escrever um resumo de 2 linhas.

Fluxo:
  1. Playwright abre o portal da Câmara (camara.leg.br)
  2. Navega até a busca de proposições com o termo passado por CLI
  3. Espera os resultados carregarem (SPA — JS renderiza)
  4. Extrai título + autor + ementa dos N primeiros
  5. Claude classifica cada proposição em RELEVANTE / TALVEZ / NÃO RELEVANTE
     e devolve resumo de 2 linhas + entidades-chave
  6. Imprime o relatório no terminal e salva CSV

Por que esse caso é bom didaticamente:
  - 100% público, sem CAPTCHA, sem login
  - Dados reais, atualizados todo dia (Câmara em sessão)
  - Mostra os dois músculos: Playwright (navegação SPA) + Claude (classificação)
  - Tem API oficial (dadosabertos.camara.leg.br) como Plano B confiável

PLANO B — se o portal estiver lento ou bloqueando:
  Rode com --fallback. O bot usa a API oficial dadosabertos.camara.leg.br
  (sem JS, sem espera) e segue o mesmo pipeline de classificação via Claude.

Como rodar (macOS):
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    python3 -m playwright install chromium
    export ANTHROPIC_API_KEY="sua_chave_aqui"
    python3 main_camara_bot.py "inteligência artificial"
    python3 main_camara_bot.py "lgpd" --fallback
"""

import os
import sys
import json
import csv
import time
import logging
import re
import httpx
import anthropic
from anthropic import Anthropic, APIStatusError
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# Carrega .env (override=True faz o .env vencer variáveis já exportadas no shell —
# útil se você tiver uma chave antiga ANTHROPIC_API_KEY no .zshrc ou exportada manualmente)
load_dotenv(override=True)

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Diagnóstico amigável de chave faltando ou errada
if not os.environ.get("ANTHROPIC_API_KEY"):
    print("\n❌ ANTHROPIC_API_KEY não encontrada.")
    print("   Cole sua chave no arquivo .env (formato: ANTHROPIC_API_KEY=sk-ant-...)")
    print("   Ou exporte no shell: export ANTHROPIC_API_KEY=sk-ant-...\n")
    sys.exit(1)

URL_BUSCA = "https://www.camara.leg.br/busca-portal?contextoBusca=BuscaProposicoes&pagina=1&order=relevancia&abaEspecifica=true&filtros=tipo%3DProposicaoUI&q={termo}"
URL_API = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
MODEL = "claude-haiku-4-5"
MAX_RESULTADOS = 8
OUTPUT_CSV = "proposicoes_classificadas.csv"

claude = Anthropic()


# ============================================================
# 1. SCRAPING VIA PLAYWRIGHT (Câmara — SPA, sem CAPTCHA)
# ============================================================

def buscar_proposicoes_playwright(termo: str) -> list[dict]:
    """Abre o portal da Câmara, busca por termo e extrai os primeiros resultados.

    Retorna lista de dicts com {titulo, ementa, link}.
    """
    url = URL_BUSCA.format(termo=termo.replace(" ", "%20"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36",
        )
        page = context.new_page()

        logger.info(f"Abrindo busca por '{termo}'")
        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # SPA — espera os cards de resultado renderizarem
        try:
            page.locator("li.l-busca__item, article.busca__resultado, div.resultado").first.wait_for(timeout=20000)
        except PWTimeout:
            logger.warning("Resultados não apareceram com seletor esperado — tentando fallback")

        # Pega texto bruto da região de resultados (mais robusto que seletor frágil)
        page.wait_for_timeout(2000)
        body_text = page.locator("main, body").first.inner_text()

        # Extração defensiva por padrão de texto ("PL 1234/2024" + linhas)
        # Se a página mudou estrutura, isso ainda pega o que importa.
        proposicoes = []
        # Padrão típico: "PL 1234/2024" ou "PEC 5/2023" ou "PLP 200/2024"
        padrao = re.compile(r"((?:PL|PEC|PLP|PLS|MPV|PDC)\s*\d+/\d{4})", re.IGNORECASE)
        linhas = body_text.splitlines()
        for i, linha in enumerate(linhas):
            m = padrao.search(linha)
            if m:
                titulo = m.group(1).strip()
                # Pega a ementa: linhas próximas, juntas
                ementa_raw = " ".join(linhas[i+1:i+5]).strip()
                ementa = re.sub(r"\s+", " ", ementa_raw)[:500]
                proposicoes.append({
                    "titulo": titulo,
                    "ementa": ementa,
                    "link": f"https://www.camara.leg.br/busca-portal?q={termo.replace(' ', '+')}",
                })
                if len(proposicoes) >= MAX_RESULTADOS:
                    break

        browser.close()

        if not proposicoes:
            logger.warning("Nenhuma proposição extraída do HTML — caia no fallback se necessário")

        return proposicoes


# ============================================================
# 2. PLANO B — API oficial dadosabertos.camara.leg.br
# ============================================================

def buscar_proposicoes_api(termo: str) -> list[dict]:
    """Plano B: API oficial da Câmara, sem CAPTCHA e sem SPA.

    keywords filtra por palavra-chave na ementa. Devolve até 25 por página.
    """
    logger.info(f"Plano B — API oficial: {URL_API}")
    params = {
        "keywords": termo,
        "ordem": "DESC",
        "ordenarPor": "id",
        "itens": MAX_RESULTADOS,
    }
    r = httpx.get(URL_API, params=params, timeout=30)
    r.raise_for_status()
    dados = r.json().get("dados", [])

    proposicoes = []
    for d in dados:
        sigla = d.get("siglaTipo", "")
        numero = d.get("numero", "")
        ano = d.get("ano", "")
        titulo = f"{sigla} {numero}/{ano}"
        proposicoes.append({
            "titulo": titulo,
            "ementa": (d.get("ementa") or "").strip()[:500],
            "link": d.get("uri", ""),
        })
    return proposicoes


# ============================================================
# 3. CLAUDE — classifica e resume cada proposição
# ============================================================

def classificar_com_claude(propostas: list[dict], interesse: str) -> list[dict]:
    """Para cada proposição, Claude devolve {classificacao, resumo, entidades}.

    Retry exponencial para HTTP 429.
    """
    enriquecidas = []
    for prop in propostas:
        prompt = f"""Você está ajudando alguém a monitorar a Câmara dos Deputados \
sobre o tema: "{interesse}".

Proposição:
TÍTULO: {prop['titulo']}
EMENTA: {prop['ementa']}

Devolva APENAS um JSON válido (sem markdown):
{{
  "classificacao": "RELEVANTE" | "TALVEZ" | "NAO_RELEVANTE",
  "justificativa": "1 linha explicando",
  "resumo": "resumo de no máximo 2 linhas em português claro",
  "entidades": ["lista", "de", "entidades-chave", "mencionadas"]
}}

Use NAO_RELEVANTE se a proposição claramente não toca no tema do usuário."""

        for tentativa in range(4):
            try:
                response = claude.messages.create(
                    model=MODEL,
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = response.content[0].text.strip()
                text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
                analise = json.loads(text)
                enriquecidas.append({**prop, **analise})
                break
            except APIStatusError as e:
                if e.status_code == 429 and tentativa < 3:
                    espera = 2 ** tentativa
                    logger.warning(f"429 Anthropic, retry em {espera}s")
                    time.sleep(espera)
                else:
                    raise
            except json.JSONDecodeError:
                logger.error(f"Claude devolveu não-JSON, pulando: {prop['titulo']}")
                enriquecidas.append({**prop, "classificacao": "ERRO", "resumo": "", "entidades": []})
                break

        time.sleep(0.5)  # rate limit voluntário

    return enriquecidas


# ============================================================
# 4. RELATÓRIO + CSV
# ============================================================

def imprimir_relatorio(propostas: list[dict], interesse: str) -> None:
    print("\n" + "=" * 70)
    print(f"  PROPOSIÇÕES NA CÂMARA SOBRE: {interesse.upper()}")
    print("=" * 70)

    for i, p in enumerate(propostas, 1):
        cor = {"RELEVANTE": "★", "TALVEZ": "◆", "NAO_RELEVANTE": "·", "ERRO": "?"}.get(
            p.get("classificacao", "ERRO"), "·"
        )
        print(f"\n{cor} [{i}] {p['titulo']}  —  {p.get('classificacao', '?')}")
        print(f"    {p.get('resumo', '(sem resumo)')}")
        if p.get("entidades"):
            print(f"    entidades: {', '.join(p['entidades'])}")
        if p.get("justificativa"):
            print(f"    motivo: {p['justificativa']}")


def salvar_csv(propostas: list[dict], path: str = OUTPUT_CSV) -> None:
    if not propostas:
        return
    campos = ["titulo", "classificacao", "resumo", "justificativa", "entidades", "ementa", "link"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        writer.writeheader()
        for p in propostas:
            row = {**p, "entidades": ", ".join(p.get("entidades", []))}
            writer.writerow(row)
    logger.info(f"CSV salvo em {path}")


# ============================================================
# 5. ORQUESTRAÇÃO
# ============================================================

def monitorar(interesse: str, use_fallback: bool = False) -> list[dict]:
    if use_fallback:
        propostas = buscar_proposicoes_api(interesse)
    else:
        propostas = buscar_proposicoes_playwright(interesse)
        if not propostas:
            logger.warning("Playwright veio vazio — caindo no Plano B (API)")
            propostas = buscar_proposicoes_api(interesse)

    logger.info(f"Encontradas {len(propostas)} proposições. Classificando com Claude...")
    enriquecidas = classificar_com_claude(propostas, interesse)
    imprimir_relatorio(enriquecidas, interesse)
    salvar_csv(enriquecidas)
    return enriquecidas


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso: python3 main_camara_bot.py "<tema>" [--fallback]')
        print('Ex:  python3 main_camara_bot.py "inteligência artificial"')
        print('     python3 main_camara_bot.py "lgpd" --fallback')
        sys.exit(1)

    tema = sys.argv[1]
    fallback = "--fallback" in sys.argv
    monitorar(tema, use_fallback=fallback)
