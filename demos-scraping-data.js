const demosScrapingData = {
    "GUIA DE SETUP & BOAS PRÁTICAS (PLAYWRIGHT)": [
        {
            id: "scr-readme",
            title: "README: Guia Completo (macOS & Windows + Ética)",
            description: "Setup com Python 3.13 + Chromium, Warmup vs Bot da Câmara, Plano B via API Oficial, Troubleshooting e Checklist de Ética/LGPD.",
            icon: "📖",
            path: "demos-scraping/README.md"
        },
        {
            id: "scr-requirements",
            title: "requirements.txt (Stack de Automação)",
            description: "Dependências do projeto: anthropic, playwright, httpx e python-dotenv.",
            icon: "📦",
            path: "demos-scraping/requirements.txt"
        },
        {
            id: "scr-env-example",
            title: ".env.example (Template de Ambiente)",
            description: "Arquivo modelo para configurar a ANTHROPIC_API_KEY com load_dotenv(override=True).",
            icon: "🔑",
            path: "demos-scraping/.env.example"
        }
    ],
    "SCRIPTS DE AUTOMAÇÃO (WARMUP VS AGENTE LEGISLATIVO)": [
        {
            id: "scr-warmup",
            title: "1. warmup_playwright.py (Seletores Frágeis vs Robustos)",
            description: "Extrai 20 livros de books.toscrape.com em modo headed contrastando seletores CSS frágeis (.price_color, img) com locators semânticos resilientes (get_by_text, get_by_role).",
            icon: "🎭",
            path: "demos-scraping/warmup_playwright.py"
        },
        {
            id: "scr-camara-bot",
            title: "2. main_camara_bot.py (Monitor da Câmara + Claude Haiku + Fallback API)",
            description: "Navega na SPA camara.leg.br, extrai proposições de forma defensiva via Regex, possui Plano B automático para a API dadosabertos.camara.leg.br e classifica relevância com Claude Haiku.",
            icon: "🏛️",
            path: "demos-scraping/main_camara_bot.py"
        }
    ],
    "OUTPUTS REAIS GERADOS (DATASETS DE EXEMPLO)": [
        {
            id: "scr-csv-camara",
            title: "proposicoes_classificadas.csv (8 PLs sobre IA Classificados)",
            description: "Resultado real da execução do bot para o tema 'inteligência artificial': PL 750/2026, PL 6237/2025, PL 704/2026, PL 6172/2025, etc., com classificação, resumo, justificativa e entidades.",
            icon: "📊",
            path: "demos-scraping/proposicoes_classificadas.csv"
        },
        {
            id: "scr-json-livros",
            title: "livros.json (20 Livros Extraídos no Warmup)",
            description: "JSON estruturado em UTF-8 gerado pelo warmup_playwright.py contendo título, preço em libras, disponibilidade em estoque e URL da capa.",
            icon: "📚",
            path: "demos-scraping/livros.json"
        }
    ]
};
