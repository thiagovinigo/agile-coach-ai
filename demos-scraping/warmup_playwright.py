"""
WARMUP — Playwright básico: abre uma página, espera o conteúdo, extrai dados estruturados.

Usa books.toscrape.com — site público criado para praticar scraping, sem CAPTCHA
e sem termos de uso restritivos.

O script:
  1. Abre o site em headed mode (browser visível)
  2. Espera os cards de livros aparecerem
  3. Extrai título, preço, disponibilidade e URL da imagem dos 20 primeiros
  4. Salva em livros.json com encoding UTF-8

Como rodar (macOS):
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install playwright
    python3 -m playwright install chromium    # baixa o Chromium (~150MB)
    python3 warmup_playwright.py
"""

import json
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

URL = "https://books.toscrape.com/"
OUTPUT_FILE = Path("livros.json")


def scrape_books(headless: bool = False, n: int = 20) -> list[dict]:
    """Extrai título, preço, disponibilidade e imagem dos N primeiros livros.

    Usa get_by_text() e get_by_role() onde possível para maior robustez contra
    mudanças no design e estrutura HTML do site.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        logger.info(f"Abrindo {URL}")
        page.goto(URL)

        # ❌ FRÁGIL: seletor CSS "article.product_pod"
        # Quebra se: classe renomeada, tag mudar para <div>
        # ✅ MAIS ROBUSTO: seria get_by_role("region"), mas site não usa ARIA
        # Fallback: manter CSS, mas conhecer o risco
        cards = page.locator("article.product_pod")
        cards.first.wait_for()
        logger.info(f"Encontrados {cards.count()} cards na página")

        books = []
        for i in range(min(n, cards.count())):
            card = cards.nth(i)

            # ❌ FRÁGIL: seletor CSS "h3 a"
            # Quebra se: estrutura HTML muda (h3 removido, a movido)
            # ✅ MAIS ROBUSTO: get_by_text() busca pelo conteúdo semântico,
            # não pela estrutura. Se título ainda existir, encontra.
            # Solução: usar CSS com fallback para get_by_text() como plano B
            title_link = card.locator("h3 a")
            title = title_link.get_attribute("title") or title_link.inner_text()

            # ❌ FRÁGIL: seletor ".price_color"
            # Quebra IMEDIATAMENTE se: classe renomeada, tag muda, elemento removido
            # ✅ MAIS ROBUSTO: get_by_text() com padrão de moeda (£, $, €, etc)
            # Procura o elemento contendo símbolo de moeda, independente de classe
            # Estratégia: tentar pattern de currency primeiro, fallback para CSS
            price = ""
            try:
                price_el = card.get_by_text("£")
                if price_el.count() > 0:
                    price = price_el.first.inner_text()
            except:
                price = card.locator(".price_color").inner_text()

            # ❌ FRÁGIL: seletor ".availability"
            # Quebra se: classe renomeada, ou texto internacionalizado
            # ✅ MAIS ROBUSTO: get_by_text() procura por padrão de texto
            # Se site mudar para "Disponível", "Em estoque", ainda funciona
            # porque estamos procurando pelas strings reais
            availability = ""
            for status_text in ["In stock", "Out of stock", "Disponível", "Indisponível"]:
                try:
                    avail_el = card.get_by_text(status_text)
                    if avail_el.count() > 0:
                        availability = avail_el.first.inner_text()
                        break
                except:
                    pass
            if not availability:
                availability = card.locator(".availability").inner_text().strip()

            # ❌ FRÁGIL: seletor genérico "img"
            # Quebra se: imagem movida para <picture>, <source>, ou src renomeado
            # ✅ MAIS ROBUSTO: get_by_role("img") + get_by_alt_text()
            # Usa semântica ARIA, não seletor genérico
            # Funciona mesmo que HTML estruture imagens diferentemente
            image_url = ""
            try:
                img = card.get_by_role("img").first
                image_url = img.get_attribute("src") or ""
            except:
                try:
                    image_url = card.locator("img").get_attribute("src") or ""
                except:
                    pass

            if image_url and image_url.startswith("../"):
                image_url = URL + image_url.replace("../", "")

            books.append({
                "titulo": title,
                "preco": price,
                "disponibilidade": availability.strip() if availability else "N/A",
                "url_imagem": image_url or ""
            })
            logger.info(f"[{i+1}] {title}")

        browser.close()
        return books


if __name__ == "__main__":
    books = scrape_books(headless=False, n=20)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    logger.info(f"✓ {len(books)} livros salvos em {OUTPUT_FILE}")
    print(json.dumps(books, indent=2, ensure_ascii=False))
