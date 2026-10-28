document.addEventListener('DOMContentLoaded', () => {
    initDemosScrapingView();
});

function initDemosScrapingView() {
    const container = document.getElementById('demos-scraping-view');
    if (!container || typeof demosScrapingData === 'undefined') return;

    container.innerHTML = '';

    // Scoped styles for Demos Scraping View
    const styleEl = document.createElement('style');
    styleEl.textContent = `
        .ds-hero {
            background: linear-gradient(135deg, #431407 0%, #7c2d12 50%, #0f172a 100%);
            color: #fff;
            padding: 28px 32px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .ds-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(245, 158, 11, 0.2);
            border: 1px solid rgba(245, 158, 11, 0.45);
            color: #fbbf24;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 4px 12px;
            border-radius: 999px;
            margin-bottom: 12px;
        }
        .ds-hero h2 {
            margin: 0 0 8px 0;
            font-size: 1.85rem;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        .ds-hero p {
            margin: 0;
            font-size: 1.02rem;
            line-height: 1.6;
            color: #cbd5e1;
            max-width: 920px;
        }
        .ds-mode-bar {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .ds-mode-btn {
            padding: 9px 18px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.08);
            color: #e2e8f0;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .ds-mode-btn:hover {
            background: rgba(255,255,255,0.15);
        }
        .ds-mode-btn.active {
            background: linear-gradient(135deg, #f59e0b, #ea580c);
            border-color: transparent;
            color: #fff;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);
        }
        .ds-guide-container {
            padding: 28px 32px;
            max-width: 1280px;
            margin: 0 auto;
        }
        .ds-card {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        .ds-title {
            margin: 0 0 6px 0;
            font-size: 1.3rem;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .ds-sub {
            margin: 0 0 20px 0;
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
        }
        .ds-grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        .ds-grid-4 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
        }
        .ds-step-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-top: 4px solid #f59e0b;
            border-radius: 10px;
            padding: 16px;
        }
        .ds-code-box {
            background: #0f172a;
            color: #e2e8f0;
            padding: 16px 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.83rem;
            line-height: 1.6;
            overflow-x: auto;
            white-space: pre;
        }
        .ds-file-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #f59e0b;
            border-radius: 10px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .ds-file-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(0,0,0,0.06);
            border-left-color: #ea580c;
        }
        .ds-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.86rem;
        }
        .ds-table th, .ds-table td {
            padding: 10px 13px;
            border: 1px solid #e2e8f0;
            text-align: left;
            vertical-align: top;
        }
        .ds-table th {
            background: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
        }
        .ds-pill-rel {
            background: #dcfce7;
            color: #15803d;
            font-weight: 800;
            font-size: 0.72rem;
            padding: 2px 8px;
            border-radius: 999px;
            display: inline-block;
        }
    `;
    container.appendChild(styleEl);

    // Hero Header
    const hero = document.createElement('div');
    hero.className = 'ds-hero';
    hero.innerHTML = `
        <div class="ds-badge">🕷️ PLAYWRIGHT · WEB SCRAPING · CLAUDE CODE ENGINEERING</div>
        <h2>🕷️ Demos Browser Automation & Web Scraping <span style="font-size:0.95rem; font-weight:600; color:#fbbf24; background:rgba(255,255,255,0.1); padding:4px 10px; border-radius:6px;">Playwright + Câmara dos Deputados + Claude Haiku</span></h2>
        <p>
            Laboratório prático de automação de navegador e coleta inteligente de dados públicos. Demonstra os dois músculos combinados: <strong>Playwright</strong> para renderizar SPAs modernas com locators resilientes (e fallback automático para API oficial) + <strong>Claude Haiku 4.5</strong> para classificar relevância, extrair entidades e resumir Projetos de Lei da Câmara dos Deputados em CSV estruturado.
        </p>
        <div class="ds-mode-bar">
            <button class="ds-mode-btn active" id="ds-btn-guide">✨ Guia de Arquitetura, Seletores & Amostra Real</button>
            <button class="ds-mode-btn" id="ds-btn-docs">💻 Explorador de Código & Datasets (7 arquivos)</button>
        </div>
    `;
    container.appendChild(hero);

    // Mode 1: Visual Guide
    const guideWrapper = document.createElement('div');
    guideWrapper.className = 'ds-guide-container';
    guideWrapper.id = 'ds-guide-wrapper';

    // Mode 2: Code Explorer
    const docsWrapper = document.createElement('div');
    docsWrapper.className = 'kb-layout';
    docsWrapper.id = 'ds-docs-wrapper';
    docsWrapper.style.display = 'none';

    container.appendChild(guideWrapper);
    container.appendChild(docsWrapper);

    window.openDemosScrapingDoc = function(docId) {
        document.getElementById('ds-btn-docs').click();
        const targetBtn = document.querySelector(`#ds-docs-wrapper .kb-nav-btn[data-doc-id="${docId}"]`);
        if (targetBtn) {
            targetBtn.click();
            targetBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    };

    guideWrapper.innerHTML = `
        <!-- 1. ARQUITETURA DO MONITOR LEGISLATIVO -->
        <div class="ds-card">
            <h3 class="ds-title">🏛️ Arquitetura do Bot Monitor da Câmara (Playwright SPA + Plano B + Claude)</h3>
            <p class="ds-sub">Como o script <code>main_camara_bot.py</code> garante resiliência máxima ao vivo combinando automação de browser, Regex defensivo e fallback transparente para API REST:</p>
            <div class="ds-grid-4">
                <div class="ds-step-box">
                    <div style="font-size:0.72rem; font-weight:800; color:#d97706; text-transform:uppercase; margin-bottom:4px;">ETAPA 1 · PLAYWRIGHT SPA</div>
                    <div style="font-weight:800; color:#0f172a; font-size:1rem; margin-bottom:6px;">🌐 Navegação & Wait</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.5;">
                        Abre <code>camara.leg.br/busca-portal</code> em modo visível (<code>headless=False</code>), aguarda a SPA renderizar os cards e extrai as proposições via Regex defensivo (<code>PL|PEC|PLP|MPV \\d+/\\d{4}</code>).
                    </div>
                </div>
                <div class="ds-step-box" style="border-top-color:#ea580c;">
                    <div style="font-size:0.72rem; font-weight:800; color:#ea580c; text-transform:uppercase; margin-bottom:4px;">ETAPA 2 · PLANO B (API)</div>
                    <div style="font-weight:800; color:#0f172a; font-size:1rem; margin-bottom:6px;">🛡️ Fallback Oficial</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.5;">
                        Se o portal governamental mudar o HTML, der timeout ou se você passar <code>--fallback</code>, o bot aciona instantaneamente <code>dadosabertos.camara.leg.br/api/v2/proposicoes</code> via <code>httpx</code>.
                    </div>
                </div>
                <div class="ds-step-box" style="border-top-color:#8b5cf6;">
                    <div style="font-size:0.72rem; font-weight:800; color:#7c3aed; text-transform:uppercase; margin-bottom:4px;">ETAPA 3 · CLAUDE HAIKU</div>
                    <div style="font-weight:800; color:#0f172a; font-size:1rem; margin-bottom:6px;">🧠 Triagem Estruturada</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.5;">
                        Para cada PL, o <code>claude-haiku-4-5</code> analisa título + ementa e devolve um JSON estrito com <code>classificacao</code> (<code>RELEVANTE | TALVEZ | NAO_RELEVANTE</code>), resumo de 2 linhas e entidades.
                    </div>
                </div>
                <div class="ds-step-box" style="border-top-color:#10b981;">
                    <div style="font-size:0.72rem; font-weight:800; color:#059669; text-transform:uppercase; margin-bottom:4px;">ETAPA 4 · ENTREGA</div>
                    <div style="font-weight:800; color:#0f172a; font-size:1rem; margin-bottom:6px;">📊 Terminal + CSV</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.5;">
                        Imprime o relatório executivo com ícones (<code>★ RELEVANTE</code>, <code>◆ TALVEZ</code>, <code>· NAO_RELEVANTE</code>) e exporta tudo para <code>proposicoes_classificadas.csv</code>.
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. COMPARATIVO: WARMUP PLAYWRIGHT VS BOT DA CÂMARA -->
        <div class="ds-card">
            <h3 class="ds-title">⚖️ Os 2 Scripts da Aula: Warmup de Seletores vs Bot da Câmara</h3>
            <p class="ds-sub">Clique em qualquer card para abrir o código Python completo no explorador:</p>
            <div class="ds-grid-2">
                <div class="ds-file-card" onclick="openDemosScrapingDoc('scr-warmup')">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="background:#fef3c7; color:#b45309; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:999px;">1. WARMUP (SEM CHAVE DE IA)</span>
                        <code style="font-size:0.82rem; color:#0f172a; font-weight:700;">warmup_playwright.py</code>
                    </div>
                    <h4 style="margin:0 0 8px 0; color:#0f172a; font-size:1.15rem;">🎭 Prática de Locators em books.toscrape.com</h4>
                    <p style="margin:0 0 12px 0; font-size:0.86rem; color:#475569; line-height:1.5;">
                        Abre o Chromium em modo visível, aguarda os cards renderizarem e extrai os 20 primeiros livros para <code>livros.json</code>, ensinando na prática a diferença entre seletores CSS frágeis e locators semânticos.
                    </p>
                    <ul style="margin:0; padding-left:18px; font-size:0.82rem; color:#334155; line-height:1.6;">
                        <li><strong>Zero fricção:</strong> Site criado para treino de scraping (sem CAPTCHA e sem API key).</li>
                        <li><strong>Didática no código:</strong> Comentários lado a lado mostrando <code>❌ FRÁGIL</code> vs <code>✅ MAIS ROBUSTO</code>.</li>
                    </ul>
                </div>

                <div class="ds-file-card" style="border-left-color:#ea580c;" onclick="openDemosScrapingDoc('scr-camara-bot')">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="background:#ffedd5; color:#c2410c; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:999px;">2. DEMO PRINCIPAL DA AULA</span>
                        <code style="font-size:0.82rem; color:#0f172a; font-weight:700;">main_camara_bot.py</code>
                    </div>
                    <h4 style="margin:0 0 8px 0; color:#0f172a; font-size:1.15rem;">🏛️ Monitor de Projetos de Lei + Classificador Claude</h4>
                    <p style="margin:0 0 12px 0; font-size:0.86rem; color:#475569; line-height:1.5;">
                        Recebe qualquer tema via linha de comando (ex: <code>"inteligência artificial"</code>, <code>"lgpd"</code>, <code>"saúde digital"</code>), coleta as proposições mais recentes na Câmara e aplica triagem cognitiva com Haiku.
                    </p>
                    <ul style="margin:0; padding-left:18px; font-size:0.82rem; color:#334155; line-height:1.6;">
                        <li><strong>Blindado para Demo ao Vivo:</strong> Flag <code>--fallback</code> alterna na hora para a API de Dados Abertos.</li>
                        <li><strong>Boas Práticas:</strong> Usa <code>load_dotenv(override=True)</code>, retry exponencial e rate limit voluntário (<code>sleep(0.5)</code>).</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 3. LIÇÃO DE OURO: SELETORES FRÁGEIS VS ROBUSTOS & ÉTICA/LGPD -->
        <div class="ds-grid-2" style="margin-bottom:24px;">
            <div class="ds-card" style="margin-bottom:0;">
                <h3 class="ds-title">🎯 Lição Técnica: Seletores CSS Frágeis vs Locators Resilientes</h3>
                <p class="ds-sub">Padrão documentado dentro do <code>warmup_playwright.py</code> e do <code>main_camara_bot.py</code> para evitar que scrapers quebrem quando o front-end muda uma classe CSS:</p>
                <table class="ds-table">
                    <thead>
                        <tr>
                            <th>Dado Alvo</th>
                            <th>❌ Seletor CSS Frágil</th>
                            <th>✅ Estratégia Resiliente (Playwright)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Preço</strong></td>
                            <td><code>card.locator(".price_color")</code><br><span style="color:#64748b; font-size:0.78rem;">Quebra se renomearem a classe CSS</span></td>
                            <td><code>card.get_by_text("£")</code><br><span style="color:#059669; font-size:0.78rem;">Busca pelo símbolo semântico da moeda</span></td>
                        </tr>
                        <tr>
                            <td><strong>Estoque</strong></td>
                            <td><code>card.locator(".availability")</code><br><span style="color:#64748b; font-size:0.78rem;">Acoplado ao nome da classe</span></td>
                            <td><code>card.get_by_text("In stock")</code><br><span style="color:#059669; font-size:0.78rem;">Procura pelas strings reais de status</span></td>
                        </tr>
                        <tr>
                            <td><strong>Imagem</strong></td>
                            <td><code>card.locator("img")</code><br><span style="color:#64748b; font-size:0.78rem;">Quebra se mudar a estrutura de tags</span></td>
                            <td><code>card.get_by_role("img").first</code><br><span style="color:#059669; font-size:0.78rem;">Usa semântica de acessibilidade ARIA</span></td>
                        </tr>
                        <tr>
                            <td><strong>Projetos de Lei</strong></td>
                            <td><code>li.l-busca__item h3.titulo</code><br><span style="color:#64748b; font-size:0.78rem;">Quebra em redesign do portal</span></td>
                            <td><code>re.compile(r"(PL|PEC|PLP)\\s*\\d+/\\d{4}")</code><br><span style="color:#059669; font-size:0.78rem;">Extração defensiva sobre <code>inner_text()</code></span></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="ds-card" style="margin-bottom:0;">
                <h3 class="ds-title">⚖️ Checklist de Ética, Legalidade & LGPD em Web Scraping</h3>
                <p class="ds-sub">Os 5 pilares obrigatórios antes de construir qualquer robô de coleta na web:</p>
                <ul style="margin:0; padding-left:18px; color:#334155; font-size:0.88rem; line-height:1.7;">
                    <li><strong>1. Conferir o <code>robots.txt</code>:</strong> Em <code>camara.leg.br/robots.txt</code> o acesso automatizado é amplamente permitido.</li>
                    <li><strong>2. Termos de Uso (ToS):</strong> Dados legislativos são de domínio público (diferente de e-commerces ou jornais pagos com ToS restritivos).</li>
                    <li><strong>3. Conformidade LGPD:</strong> Textos de projetos de lei não são dados pessoais; atuação parlamentar é pública por exercício de função.</li>
                    <li><strong>4. Rate Limit Voluntário:</strong> Respeitar o servidor de destino (ex: <code>time.sleep(0.5)</code> e não disparar dezenas de abas simultâneas).</li>
                    <li><strong>5. Preferir API Oficial (Plano B):</strong> Sempre que existir um endpoint aberto como <code>dadosabertos.camara.leg.br</code>, priorize-o em produção.</li>
                </ul>
                <div style="margin-top:14px; background:#fffbeb; border:1px solid #fde68a; padding:10px 14px; border-radius:8px; font-size:0.82rem; color:#92400e;">
                    ⚠️ <strong>Dica de Setup (Python 3.13 vs 3.14):</strong> No macOS, force <code>python3.13 -m venv .venv</code> para evitar o erro de importação do <code>pip</code> no Python 3.14 recém-instalado pelo Homebrew.
                </div>
            </div>
        </div>

        <!-- 4. AMOSTRA REAL DO DATASET GERADO (PROPOSICOES_CLASSIFICADAS.CSV) -->
        <div class="ds-card">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
                <div>
                    <h3 class="ds-title" style="margin-bottom:4px;">📊 Amostra Real Gerada: Monitoramento de <code>"inteligência artificial"</code> na Câmara</h3>
                    <p class="ds-sub" style="margin-bottom:0;">Abaixo estão 4 das 8 proposições reais extraídas e classificadas pelo Claude Haiku no arquivo <code>proposicoes_classificadas.csv</code>:</p>
                </div>
                <button onclick="openDemosScrapingDoc('scr-csv-camara')" style="background:#f59e0b; color:#fff; border:none; padding:9px 16px; border-radius:8px; font-weight:700; font-size:0.85rem; cursor:pointer;">📊 Ver CSV Completo (8 PLs)</button>
            </div>
            <table class="ds-table" style="margin-bottom:18px;">
                <thead>
                    <tr>
                        <th style="width:110px;">Proposição</th>
                        <th style="width:110px;">Status IA</th>
                        <th>Resumo Executivo (Gerado pelo Claude Haiku)</th>
                        <th style="width:260px;">Entidades Extraídas</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>PL 750/2026</strong></td>
                        <td><span class="ds-pill-rel">★ RELEVANTE</span></td>
                        <td>Cria o Programa Nacional de Monitoramento de Agressores com uso de IA (PNM-IA) para prevenir violência doméstica e garantir efetividade de medidas protetivas.</td>
                        <td><span style="font-size:0.8rem; color:#475569;">Senado Federal, Eduardo Braga, PNM-IA, medidas protetivas</span></td>
                    </tr>
                    <tr>
                        <td><strong>PL 6237/2025</strong></td>
                        <td><span class="ds-pill-rel">★ RELEVANTE</span></td>
                        <td>Cria o Sistema Nacional para Desenvolvimento, Regulação e Governança de Inteligência Artificial, estabelecendo marco regulatório para IA no Brasil.</td>
                        <td><span style="font-size:0.8rem; color:#475569;">Poder Executivo, Sistema Nacional de IA, Governança de IA</span></td>
                    </tr>
                    <tr>
                        <td><strong>PL 6707/2025</strong></td>
                        <td><span class="ds-pill-rel">★ RELEVANTE</span></td>
                        <td>Modifica o Código de Defesa do Consumidor (CDC) para dispor sobre responsabilidade civil por danos causados pelo comportamento autônomo de sistemas de IA.</td>
                        <td><span style="font-size:0.8rem; color:#475569;">Amom Mandel, Lei 8.078/1990, CDC, responsabilidade civil</span></td>
                    </tr>
                    <tr>
                        <td><strong>PL 428/2026</strong></td>
                        <td><span class="ds-pill-rel">★ RELEVANTE</span></td>
                        <td>Altera o art. 171 do Código Penal para tipificar como fraude eletrônica o uso de imagens, vídeos ou áudios gerados por IA (deepfakes) para enganar.</td>
                        <td><span style="font-size:0.8rem; color:#475569;">Chris Tonietto, Código Penal, fraude eletrônica, deepfakes</span></td>
                    </tr>
                </tbody>
            </table>

            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px 18px; font-size:0.88rem; color:#334155;">
                <strong>🚀 5 Variações Práticas para Conectar com os Outros Temas da Formação:</strong>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(230px, 1fr)); gap:10px; margin-top:8px;">
                    <div>• <strong>Múltiplos Termos:</strong> Loop sobre <code>["lgpd", "ia", "saúde digital"]</code> gerando CSV consolidado.</div>
                    <div>• <strong>Persistir no Supabase (Tema 2):</strong> Salvar no banco para alertar apenas quando surgir um PL novo.</div>
                    <div>• <strong>Agendamento Diário (Tema 3):</strong> Rodar via GitHub Actions todo dia às 08h e enviar por e-mail.</div>
                    <div>• <strong>Expor via FastAPI (Tema 4):</strong> Criar endpoint <code>POST /monitorar?tema=ia</code>.</div>
                    <div>• <strong>Filtro Temporal:</strong> Passar <code>?ano=2026</code> na busca para focar apenas na sessão atual.</div>
                </div>
            </div>
        </div>
    `;

    // Populate Mode 2: Code & Datasets Explorer
    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';

    docsWrapper.appendChild(sidebar);
    docsWrapper.appendChild(contentArea);

    const categories = Object.keys(demosScrapingData);
    let firstDocItem = null;

    categories.forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #f59e0b';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const linkList = document.createElement('div');
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        catHeader.onclick = () => {
            linkList.style.display = linkList.style.display === 'none' ? 'block' : 'none';
        };

        const docsList = demosScrapingData[category];
        docsList.forEach(docItem => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.setAttribute('data-doc-id', docItem.id);
            btn.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">${docItem.icon || '📄'}</span>
                    <span style="font-weight:600; color:#323130; font-size:0.93rem;">${docItem.title}</span>
                </div>
                <div style="font-size:0.78rem; color:#605e5c; margin-top:4px; line-height:1.35; white-space:normal;">
                    ${docItem.description}
                </div>
            `;

            if (!firstDocItem) firstDocItem = { btn, docItem, category };

            btn.onclick = () => {
                document.querySelectorAll('#ds-docs-wrapper .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                contentArea.innerHTML = '<div style="padding:40px; text-align:center; color:#64748b;">⏳ Carregando arquivo...</div>';

                fetch(docItem.path + '?v=' + new Date().getTime())
                    .then(r => {
                        if (!r.ok) throw new Error('Arquivo não encontrado: ' + docItem.path);
                        return r.text();
                    })
                    .then(text => {
                        const isCodeFile = docItem.path.endsWith('.py') || docItem.path.endsWith('.json') || docItem.path.endsWith('.csv') || docItem.path.endsWith('.txt') || docItem.path.endsWith('.example');
                        let renderedBody = '';

                        if (isCodeFile) {
                            const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                            renderedBody = `<pre style="background:#0f172a; color:#f8fafc; padding:22px; border-radius:10px; overflow-x:auto; font-family:'Courier New', monospace; font-size:0.86rem; line-height:1.6; border-left:4px solid #f59e0b;"><code>${escaped}</code></pre>`;
                        } else {
                            const preBlocks = [];
                            let processedText = text.replace(/```[a-zA-Z0-9_-]*\n([\s\S]*?)```/g, (match, p1) => {
                                const esc = p1.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                                preBlocks.push(esc);
                                return `__PRE_BLOCK_${preBlocks.length - 1}__`;
                            });

                            let html = processedText
                                .replace(/^### (.*$)/gim, '<h3 style="margin-top:28px; margin-bottom:12px; color:#1e293b; font-size:1.3rem;">$1</h3>')
                                .replace(/^## (.*$)/gim, '<h2 style="margin-top:36px; margin-bottom:16px; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:8px; font-size:1.6rem;">$1</h2>')
                                .replace(/^# (.*$)/gim, '<h1 style="margin-top:10px; margin-bottom:20px; color:#0f172a; font-size:2rem; font-weight:800;">$1</h1>')
                                .replace(/\*\*(.*?)\*\*/gim, '<strong style="color:#0f172a;">$1</strong>')
                                .replace(/\*(.*?)\*/gim, '<em>$1</em>')
                                .replace(/`([^`]+)`/gim, '<code style="background:#f1f5f9; padding:2px 6px; border-radius:4px; font-family:monospace; color:#d97706; font-size:0.88em;">$1</code>')
                                .replace(/^\> (.*$)/gim, '<blockquote style="border-left:4px solid #f59e0b; background:#fffbeb; padding:12px 16px; margin:14px 0; color:#92400e; border-radius:0 6px 6px 0;">$1</blockquote>')
                                .replace(/^\- (.*$)/gim, '<li style="margin-left:20px; margin-bottom:6px; line-height:1.6; color:#334155;">$1</li>')
                                .replace(/\n\n/gim, '<br><br>');

                            html = html.replace(/__PRE_BLOCK_(\d+)__/g, (match, idx) => {
                                return `<pre style="background:#0f172a; color:#f8fafc; padding:16px; border-radius:8px; overflow-x:auto; margin:18px 0; font-family:monospace; font-size:0.88rem; line-height:1.5;"><code>${preBlocks[idx]}</code></pre>`;
                            });
                            renderedBody = html;
                        }

                        const fileName = docItem.path.split('/').pop();
                        const headerCard = `
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; margin-bottom: 28px;">
                                <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                                    <div>
                                        <span style="font-size:0.75rem; font-weight:800; color:#d97706; text-transform:uppercase;">${category}</span>
                                        <h3 style="margin:4px 0 0 0; color:#0f172a; font-size:1.25rem;">${docItem.icon || '📄'} ${docItem.title}</h3>
                                    </div>
                                    <div style="display:flex; gap:10px; align-items:center;">
                                        ${window.favoritesManager ? window.favoritesManager.renderButton(docItem.id, docItem.title, 'Demos Playwright & Scraping', docItem.path) : ''}
                                        <a href="${docItem.path}" download="${fileName}" style="background:#f59e0b; color:#fff; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.85rem;">⬇️ Baixar ${fileName}</a>
                                        <a href="${docItem.path}" target="_blank" style="background:#fff; color:#334155; border:1px solid #cbd5e1; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.85rem;">👀 Abrir Raw</a>
                                    </div>
                                </div>
                                <p style="margin:0 0 12px 0; color:#475569; font-size:0.92rem;">${docItem.description}</p>
                                <div style="background:#f1f5f9; border:1px solid #cbd5e1; padding:6px 10px; border-radius:4px; font-family:monospace; font-size:0.8rem; color:#475569;">
                                    📂 <strong>Arquivo no Portal:</strong> ${docItem.path}
                                </div>
                            </div>
                        `;

                        contentArea.innerHTML = `
                            <div style="max-width: 920px; margin: 0 auto; padding: 24px 32px;">
                                ${headerCard}
                                <div style="color:#1e293b; line-height:1.7; font-size:1rem;">
                                    ${renderedBody}
                                </div>
                            </div>
                        `;
                    })
                    .catch(err => {
                        contentArea.innerHTML = `<div style="padding:40px; color:#ef4444;">Erro ao carregar arquivo: ${err.message}</div>`;
                    });
            };

            linkList.appendChild(btn);
        });
    });

    // Mode toggle buttons
    const btnGuide = hero.querySelector('#ds-btn-guide');
    const btnDocs = hero.querySelector('#ds-btn-docs');

    btnGuide.onclick = () => {
        btnGuide.classList.add('active');
        btnDocs.classList.remove('active');
        guideWrapper.style.display = 'block';
        docsWrapper.style.display = 'none';
    };

    btnDocs.onclick = () => {
        btnDocs.classList.add('active');
        btnGuide.classList.remove('active');
        guideWrapper.style.display = 'none';
        docsWrapper.style.display = 'flex';
        if (firstDocItem && !docsWrapper.querySelector('.kb-nav-btn.active')) {
            firstDocItem.btn.click();
        }
    };
}
