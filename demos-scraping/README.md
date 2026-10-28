# Demos — Browser Automation e Web Scraping

Código pronto-pra-rodar das demos do tema. Setup escrito para **macOS** (com inputs Windows ao lado quando aplicável).

> Se for a primeira vez que você usa Python no Mac e o `python3` não responder: `brew install python@3.13`.

---

## Os arquivos e quando usar cada um

| Arquivo | Quando rodar | Precisa de |
|---|---|---|
| **`warmup_playwright.py`** | Warmup — Playwright em books.toscrape.com (sem CAPTCHA, sem chave Anthropic) | Apenas Playwright instalado |
| **`main_camara_bot.py`** | **Demo principal da aula** — Playwright + Claude monitora proposições na Câmara dos Deputados | `ANTHROPIC_API_KEY` + Playwright + Chromium |
| **`.env.example`** | Template das variáveis de ambiente | copiar para `.env` e preencher |

---

## Setup base (uma vez só)

### macOS

```bash
brew install python@3.13                  # Python 3.13 (evite 3.14 — pip quebra)

cd demos/
python3.13 -m venv .venv                  # FORÇA 3.13 (não use python3, ele pega 3.14)
source .venv/bin/activate
python --version                          # confirma: deve mostrar 3.13.x
pip install --upgrade pip
pip install -r requirements.txt

# Playwright precisa baixar o Chromium dele (~150MB):
python -m playwright install chromium

cp .env.example .env                      # depois edite o .env com sua chave
```

> **Já criou a venv com 3.14 e o pip quebrou?** `rm -rf .venv` e refaz com `python3.13 -m venv .venv`. O sintoma típico é `ImportError: cannot import name '__version__' from 'pip'`.

### Windows (PowerShell)

```powershell
# Baixe Python 3.13 em python.org (marque "Add to PATH")

cd demos\
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python -m playwright install chromium

copy .env.example .env                     # depois edite o .env com sua chave
```

Edite o `.env` e adicione sua chave da Anthropic:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

---

## Warmup — `warmup_playwright.py` 🚀

Use **antes** de tudo. Abre books.toscrape.com (site de prática), extrai 20 livros (título, preço, disponibilidade, imagem) usando os 3 sabores de locator, e salva `livros.json`.

```bash
python3 warmup_playwright.py
```

O que esperar:

- Janela do Chromium abre (headed mode — pra turma ver o browser)
- Página dos livros carrega
- Console imprime cada livro encontrado + JSON final
- `livros.json` criado na pasta
- Browser fecha sozinho

Se aparecer `Executable doesn't exist...`, rode o install do Chromium:

```bash
python3 -m playwright install chromium
```

---

## Demo principal — `main_camara_bot.py` 🎯

Monitora projetos de lei na Câmara dos Deputados sobre o tema que você passar, e usa Claude para classificar cada um em **RELEVANTE / TALVEZ / NÃO RELEVANTE** + escrever resumo de 2 linhas.

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python3 main_camara_bot.py "inteligência artificial"
```

Fluxo:

1. Chromium abre o portal `camara.leg.br/busca-portal` com sua palavra-chave
2. Playwright espera os resultados renderizarem (SPA)
3. Extrai título + ementa das primeiras 8 proposições
4. Para cada uma, Claude Haiku devolve JSON com classificação, resumo e entidades
5. Imprime relatório no terminal
6. Salva `proposicoes_classificadas.csv` na pasta

Temas que rendem bem para demo ao vivo:

| Tema | Por que é bom |
|---|---|
| `"inteligência artificial"` | Pauta atual, várias proposições recentes |
| `"lgpd"` | Tema regulatório, ementas curtas |
| `"saúde digital"` | Mostra o filtro de relevância funcionando bem |
| `"educação"` | Sempre tem volume — bom pra mostrar a classificação separar joio do trigo |

### Plano B — portal lento ou mudou layout?

A Câmara mantém uma **API pública** em `dadosabertos.camara.leg.br` que devolve as mesmas proposições em JSON, sem CAPTCHA, sem SPA, sem espera. Se a hora de gravar bater ruim:

```bash
python3 main_camara_bot.py "lgpd" --fallback
```

Mesmo pipeline de classificação via Claude. Só muda a fonte: API REST em vez de scraping da página.

---

## Troubleshooting

| Erro | Causa | Solução |
|---|---|---|
| `command not found: python3` (Mac) | Python não instalado | `brew install python@3.13` |
| `Executable doesn't exist at .../chromium` | Chromium do Playwright não baixado | `python3 -m playwright install chromium` |
| `ModuleNotFoundError: playwright` | venv não ativo | `source .venv/bin/activate` |
| `TimeoutError: Timeout 30000ms` | Internet lenta ou portal mudou layout | Use `--fallback` direto na API |
| "Nenhuma proposição extraída do HTML" | Portal mudou estrutura — fallback ativa sozinho | Já cai automaticamente no Plano B |
| HTTP 429 (Anthropic) | Tier 1 estourou (50K tok/min) | Aguarde 60s OU adicione US$5 em console.anthropic.com |
| Browser abre minimizado (Mac) | Mission Control | Cmd+Tab pra focar; ou rode em `headless=True` |
| API devolve `{"dados": []}` | Termo muito específico | Tente palavra-chave mais genérica (ex: "saúde" em vez de "saúde mental adolescente") |

---

## Ética e legalidade (importante!) ⚖️

A Câmara dos Deputados é fonte pública de dados — pode scrapear sem fricção. Mas mesmo aqui, vale internalizar o checklist:

1. **`robots.txt`** — `https://www.camara.leg.br/robots.txt` permite acesso amplo
2. **Termos de uso** — dados legislativos são de domínio público
3. **LGPD** — dados sobre projetos de lei NÃO são pessoais; dados sobre deputados são públicos por exercício de função
4. **Rate limit voluntário** — `time.sleep(0.5)` entre chamadas Claude já está no script
5. **Plano B via API oficial** — sempre que existir API pública, prefira ela

Para sites comerciais (Mercado Livre, Amazon, jornais pagos), a história muda: ToS restritivo + LGPD se houver dados pessoais. Quando em dúvida, consulte um advogado de tecnologia.

---

## Variações para a demo (até 20 min)

- **Múltiplos termos em paralelo**: loop sobre `["lgpd", "ia", "saúde digital"]`, gera CSV consolidado
- **Filtro por ano**: passa `?ano=2025` na busca para pegar só proposições recentes
- **Persistir histórico**: integra com Supabase (do Tema 2) para detectar quando uma nova proposição entra na lista
- **Expor como API**: empacota o bot dentro de FastAPI (do Tema 4), endpoint `POST /monitorar?tema=ia`
- **Disparo automático**: GitHub Action diária (do Tema 3) que roda o monitor e te envia o CSV por e-mail
