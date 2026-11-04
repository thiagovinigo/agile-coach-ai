document.addEventListener('DOMContentLoaded', () => {
    initProjectNomadView();
});

function initProjectNomadView() {
    const container = document.getElementById('project-nomad-view');
    if (!container || typeof projectNomadData === 'undefined') return;

    container.innerHTML = '';

    const styleEl = document.createElement('style');
    styleEl.textContent = `
        .pn-hero {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
            color: #fff;
            padding: 28px 32px;
            border-bottom: 1px solid rgba(255,255,255,0.12);
        }
        .pn-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(56, 189, 248, 0.2);
            border: 1px solid rgba(56, 189, 248, 0.45);
            color: #7dd3fc;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 4px 12px;
            border-radius: 999px;
            margin-bottom: 12px;
        }
        .pn-hero h2 {
            margin: 0 0 8px 0;
            font-size: 1.85rem;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        .pn-hero p {
            margin: 0;
            font-size: 1.02rem;
            line-height: 1.6;
            color: #cbd5e1;
            max-width: 960px;
        }
        .pn-mode-bar {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .pn-mode-btn {
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
        .pn-mode-btn:hover {
            background: rgba(255,255,255,0.15);
        }
        .pn-mode-btn.active {
            background: linear-gradient(135deg, #0284c7, #10b981);
            border-color: transparent;
            color: #fff;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
        }
        .pn-guide-container {
            padding: 28px 32px;
            max-width: 1280px;
            margin: 0 auto;
        }
        .pn-card {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        .pn-title {
            margin: 0 0 6px 0;
            font-size: 1.3rem;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .pn-sub {
            margin: 0 0 20px 0;
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
        }
        .pn-grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        .pn-grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
            gap: 16px;
        }
        .pn-grid-4 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 16px;
        }
        .pn-box {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 18px;
        }
        .pn-box h4 {
            margin: 0 0 8px 0;
            font-size: 1.02rem;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .pn-box p {
            margin: 0;
            font-size: 0.88rem;
            color: #475569;
            line-height: 1.55;
        }
        .pn-code {
            background: #0f172a;
            color: #f8fafc;
            padding: 14px 16px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.82rem;
            line-height: 1.55;
            overflow-x: auto;
            margin-top: 10px;
            border-left: 4px solid #0284c7;
        }
        .pn-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }
        .pn-table th {
            background: #f1f5f9;
            color: #0f172a;
            text-align: left;
            padding: 10px 12px;
            border-bottom: 2px solid #cbd5e1;
            font-weight: 700;
        }
        .pn-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #e2e8f0;
            color: #334155;
            vertical-align: top;
        }
        .pn-pill {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 700;
        }
    `;
    container.appendChild(styleEl);

    // Hero Banner
    const hero = document.createElement('div');
    hero.className = 'pn-hero';
    hero.innerHTML = `
        <div class="pn-badge">🛰️ CROSSTALK SOLUTIONS • OFFLINE-FIRST KNOWLEDGE, EDUCATION & AI SERVER</div>
        <h2>
            <span>🧭 Project NOMAD — Knowledge That Never Goes Offline</span>
            <a href="https://github.com/Crosstalk-Solutions/project-nomad" target="_blank" style="font-size: 0.82rem; background: rgba(255,255,255,0.12); color: #fff; padding: 5px 12px; border-radius: 6px; text-decoration: none; font-weight: 600; border: 1px solid rgba(255,255,255,0.2);">🔗 GitHub Oficial</a>
            <a href="https://www.projectnomad.us" target="_blank" style="font-size: 0.82rem; background: rgba(16,185,129,0.2); color: #6ee7b7; padding: 5px 12px; border-radius: 6px; text-decoration: none; font-weight: 600; border: 1px solid rgba(16,185,129,0.4);">🌐 projectnomad.us</a>
        </h2>
        <p>
            Servidor autônomo e <strong>100% Offline-First</strong> de conhecimento, educação e Inteligência Artificial local. Orquestra via Docker um Command Center completo com <strong>IA Local + RAG (Ollama & Qdrant)</strong>, <strong>Wikipedia & Biblioteca Médica (Kiwix ZIM)</strong>, <strong>Tradução Neural Offline em 50 idiomas (1.600x mais rápida na CPU)</strong>, <strong>Khan Academy (Kolibri Gen 2)</strong>, <strong>Bulas Oficiais FDA (openFDA)</strong>, <strong>Mapas Regionais (ProtoMaps)</strong>, <strong>Rádios LoRa Off-Grid (Meshtastic/MeshCore)</strong> e <strong>AI Quality Harness</strong> determinístico.
        </p>
        <div class="pn-mode-bar">
            <button id="pn-btn-guide" class="pn-mode-btn active">📘 Guia de Arquitetura, Apps & RAG Harness</button>
            <button id="pn-btn-docs" class="pn-mode-btn">📂 Explorar Documentação, Código & Scripts (23 Arquivos)</button>
        </div>
    `;
    container.appendChild(hero);

    // 1. Guide Wrapper
    const guideWrapper = document.createElement('div');
    guideWrapper.className = 'pn-guide-container';
    guideWrapper.innerHTML = `
        <!-- Card 1: Arquitetura de Containers & Command Center -->
        <div class="pn-card">
            <h3 class="pn-title">🏗️ 1. Arquitetura do Command Center & Orquestração Docker</h3>
            <p class="pn-sub">O NOMAD opera como um painel de controle unificado (AdonisJS 6 + Inertia React + TypeScript) que gerencia containers filhos, armazenamento centralizado e atualizações seguras via sidecars.</p>
            <div class="pn-grid-3">
                <div class="pn-box" style="border-top: 4px solid #0284c7;">
                    <h4>🎛️ nomad_admin (Command Center)</h4>
                    <p>Aplicação full-stack AdonisJS na porta <code>8080</code> com acesso ao <code>/var/run/docker.sock</code>. Detecta automaticamente o mount de <code>/opt/project-nomad/storage</code> e injeta os volumes corretos em cada app filho (Kiwix, Ollama, Qdrant, Jellyfin, etc.).</p>
                </div>
                <div class="pn-box" style="border-top: 4px solid #10b981;">
                    <h4>🦙 IA Local + RAG (Ollama + Qdrant)</h4>
                    <p>Chat IA integrado ao Command Center. Suporta <strong>Ollama</strong> nativo (com aceleração GPU via NVIDIA Container Toolkit) ou APIs compatíveis com OpenAI (LM Studio / llama.cpp), aliado ao banco vetorial <strong>Qdrant</strong> para busca semântica nos seus PDFs e manuais.</p>
                </div>
                <div class="pn-box" style="border-top: 4px solid #8b5cf6;">
                    <h4>🗄️ MySQL 8.0 + Redis 7 (BullMQ)</h4>
                    <p>Persistência relacional em <code>nomad_mysql</code> (histórico de chats, manifesto de coleções, bulas FDA indexadas, benchmarks) e filas assíncronas em <code>nomad_redis</code> para downloads resilientes de ZIMs, extração de PMTiles e ingestão de embeddings.</p>
                </div>
                <div class="pn-box" style="border-top: 4px solid #f59e0b;">
                    <h4>🔄 nomad_updater (Sidecar de Auto-Update)</h4>
                    <p>Container sidecar dedicado que compartilha o volume <code>nomad-update-shared</code>. Permite que o Command Center atualize sua própria imagem Docker sem cair no meio da operação, aplicando <strong>pre-flight checks</strong>, janela de horário, cool-off e rollback automático.</p>
                </div>
                <div class="pn-box" style="border-top: 4px solid #ec4899;">
                    <h4>💿 nomad_disk_collector (Sidecar Host FS)</h4>
                    <p>Container leve com mount <code>/:/host:ro,rslave</code> que inspeciona <code>/proc</code> e <code>/sys</code> em modo somente leitura para reportar telemetria exata de discos físicos, partições e uso de armazenamento na interface do usuário.</p>
                </div>
                <div class="pn-box" style="border-top: 4px solid #06b6d4;">
                    <h4>📋 nomad_dozzle (Logs em Tempo Real)</h4>
                    <p>Instância Dozzle v10 na porta <code>9999</code> endurecida para LAN (com <code>DOZZLE_ENABLE_ACTIONS=false</code> e <code>DOZZLE_ENABLE_SHELL=false</code>) para inspeção visual de logs e métricas de todos os containers sem risco de escalonamento de privilégios.</p>
                </div>
            </div>
        </div>

        <!-- Card 2: Ferramentas Nativas & Supply Depot -->
        <div class="pn-card">
            <h3 class="pn-title">🧰 2. Ecossistema de Ferramentas Offline & Catálogo Supply Depot</h3>
            <p class="pn-sub">Todas as ferramentas rodam 100% localmente no servidor, sem telemetria e sem depender de nuvem após o download inicial.</p>
            <div style="overflow-x: auto;">
                <table class="pn-table">
                    <thead>
                        <tr>
                            <th>Ferramenta / App</th>
                            <th>Tecnologia Base</th>
                            <th>Função Crítica Offline</th>
                            <th>Destaque Técnico no NOMAD</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>📚 Information Library</strong></td>
                            <td><span class="pn-pill" style="background:#dbeafe; color:#1e40af;">Kiwix (.zim)</span></td>
                            <td>Wikipedia completa, guias médicos, sobrevivência e livros do Project Gutenberg</td>
                            <td>Seletor dedicado de pacotes Wikipedia e gerenciador de coleções em 3 níveis (Essential, Standard, Comprehensive).</td>
                        </tr>
                        <tr>
                            <td><strong>🌐 Translated Library</strong></td>
                            <td><span class="pn-pill" style="background:#dcfce7; color:#166534;">CTranslate2 + MarianMT</span></td>
                            <td>Tradução offline em tempo real de qualquer artigo Kiwix para <strong>50 idiomas</strong> (incl. Português <code>pt</code>)</td>
                            <td><strong>1.600x mais rápido</strong> que traduzir via LLM, roda 100% na CPU (sem precisar de GPU) e preserva nomes próprios.</td>
                        </tr>
                        <tr>
                            <td><strong>💊 FDA Drug Reference</strong></td>
                            <td><span class="pn-pill" style="background:#fee2e2; color:#991b1b;">openFDA SQL Index</span></td>
                            <td>Base oficial de medicamentos OTC e prescritos da FDA (posologia, avisos, princípios ativos)</td>
                            <td>Download resiliente de 1.7 GB (expande para 8–10 GB indexados). Busca por medicamento, por <strong>sintoma/situação</strong> e comparação lado a lado.</td>
                        </tr>
                        <tr>
                            <td><strong>🎓 Education Platform</strong></td>
                            <td><span class="pn-pill" style="background:#fef3c7; color:#92400e;">Kolibri Gen 2</span></td>
                            <td>Cursos completos da Khan Academy (vídeos + exercícios interativos) com controle de progresso</td>
                            <td>Suporte multi-usuário para famílias/escolas e migração direta de canais via rede local da versão Gen 1 (porta 8300).</td>
                        </tr>
                        <tr>
                            <td><strong>🗺️ Offline Maps</strong></td>
                            <td><span class="pn-pill" style="background:#e0e7ff; color:#3730a3;">ProtoMaps (.pmtiles)</span></td>
                            <td>Mapas vetoriais regionais e mundiais navegáveis sem internet com busca local</td>
                            <td>Extração sob demanda de regiões geográficas e suporte a marcadores personalizados no mapa.</td>
                        </tr>
                        <tr>
                            <td><strong>📡 Meshtastic & MeshCore</strong></td>
                            <td><span class="pn-pill" style="background:#f3e8ff; color:#6b21a8;">LoRa Mesh Radio UI</span></td>
                            <td>Painel web para rádios comunicadores LoRa off-grid de longo alcance (mensagens e GPS sem celular)</td>
                            <td>Meshtastic conecta via HTTP Wi-Fi; MeshCore roda sob HTTPS autoassinado para liberar WebUSB e WebBluetooth no navegador.</td>
                        </tr>
                        <tr>
                            <td><strong>🔐 Vaultwarden & Homebox</strong></td>
                            <td><span class="pn-pill" style="background:#f1f5f9; color:#334155;">Bitwarden + Inventário</span></td>
                            <td>Cofre de senhas criptografado (compatível com apps Bitwarden) e sistema de inventário residencial/patrimonial</td>
                            <td>Vaultwarden pré-configurado com HTTPS na porta <code>8480</code> e flag <code>SIGNUPS_ALLOWED=false</code> para trancar novos registros.</td>
                        </tr>
                        <tr>
                            <td><strong>🛠️ Stirling PDF, IT Tools, Calibre, Jellyfin, Excalidraw, FlatNotes, CyberChef</strong></td>
                            <td><span class="pn-pill" style="background:#ccfbf1; color:#115e59;">Supply Depot + BYO Docker</span></td>
                            <td>50+ ferramentas de PDF + OCR, 100+ utilitários dev, leitor de e-books, streaming de mídia local, quadro branco e notas Markdown</td>
                            <td>Além do catálogo curado, o Supply Depot aceita <strong>qualquer container Docker customizado</strong> com validação pre-flight de portas e segurança.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Card 3: NOMAD AI Quality Harness (RAG Evaluation) -->
        <div class="pn-card">
            <h3 class="pn-title">🧪 3. NOMAD AI Quality Harness — Engenharia Científica de Avaliação RAG</h3>
            <p class="pn-sub">Um dos diferenciais mais avançados do repositório (em <code>admin/tests/eval/</code>): uma suíte determinística para medir a qualidade do pipeline RAG e separar <strong>regressões de código</strong> de <strong>limitações de modelos pequenos em hardware modesto</strong>.</p>
            <div class="pn-grid-2">
                <div class="pn-box" style="border-left: 4px solid #10b981;">
                    <h4>🔍 Decomposição em 4 Modos (Código vs. Modelo)</h4>
                    <p>O comando <code>node ace eval:generation --all-modes</code> executa cada pergunta das suítes Golden (<code>core</code> com 99 perguntas, <code>long_context</code> e <code>off_topic</code>) sob diferentes condições:</p>
                    <ul style="margin: 10px 0 0 18px; padding: 0; font-size: 0.86rem; color: #334155; line-height: 1.6;">
                        <li><strong><code>oracle</code></strong>: Injeta os documentos corretos verbatim. Mede o <strong>teto do modelo</strong> com o prompt atual. Se for baixo, nenhum ajuste de busca resolverá — é preciso um modelo maior.</li>
                        <li><strong><code>e2e</code></strong>: Usa o que a busca real (Qdrant + Reranker) retornou. Se <code>oracle - e2e</code> for grande, há um <strong>bug de recuperação (retrieval)</strong>.</li>
                        <li><strong><code>noretrieval</code></strong>: Sem contexto injetado (conhecimento paramétrico puro do LLM). Se <code>e2e - noretrieval ≈ 0</code>, o RAG não está contribuindo.</li>
                        <li><strong><code>--model=mock</code></strong>: Ecoa o contexto injetado sem usar Ollama, medindo o <strong>teto extrativo</strong> puro do retrieval.</li>
                    </ul>
                </div>
                <div class="pn-box" style="border-left: 4px solid #0284c7;">
                    <h4>📏 Métricas Determinísticas & Isolamento no Qdrant</h4>
                    <p>O corpus de avaliação (28 docs de sobrevivência/medicina/rádio + 6 <em>distractors</em> como poemas e tutoriais Python/MDN) convive na mesma coleção Qdrant <code>nomad_knowledge_base</code> usando a tag <code>collection: __nomad_eval__</code>:</p>
                    <ul style="margin: 10px 0 0 18px; padding: 0; font-size: 0.86rem; color: #334155; line-height: 1.6;">
                        <li><strong>Retrieval (100% Determinístico para CI)</strong>: <code>nDCG</code> (validado contra <code>pytrec_eval</code>), <code>recall@1</code>, <code>recall@5</code>, <code>precision@k</code>, <code>MRR</code> e taxa de vazamento em perguntas fora de escopo (<code>nonEmptyRateOnRefusal</code>).</li>
                        <li><strong>Generation & Context Budget</strong>: <code>correctness</code> (regex <code>mustInclude</code>/<code>mustNotInclude</code>), <code>refusalCorrectness</code>, <code>leakageRate</code> (proíbe citar "according to Context 1"), <code>groundedness</code> (verifica se números >10 citados existem no contexto) e <code>promptTokenError</code> (~4.6% no Llama 3 8B).</li>
                    </ul>
                </div>
            </div>
            <div class="pn-code"># 1. Ingerir o corpus de avaliação isolado (__nomad_eval__) e validar suítes Golden
node ace eval:corpus --check
node ace eval:corpus --ingest

# 2. Avaliar Retrieval determinístico + ablação do Reranker (segundos, sem precisar de LLM de chat)
node ace eval:retrieval --ablate

# 3. Avaliar Geração nos 3 modos (oracle, e2e, noretrieval) + suíte de janela de contexto
node ace eval:generation --model=llama3.2:latest --all-modes
node ace eval:generation --model=llama3.2:latest --suite=long_context

# 4. Comparar contra baseline com tolerância de regressão (0.02) para gate de CI
node ace eval:compare tests/eval/baselines/&lt;fp&gt;/retrieval.json &lt;new-report.json&gt;</div>
        </div>

        <!-- Card 4: Requisitos de Hardware & Comandos Rápidos -->
        <div class="pn-card">
            <h3 class="pn-title">⚡ 4. Requisitos de Hardware, Instalação & Simulação de Auto-Update</h3>
            <p class="pn-sub">Compare o perfil leve sem IA com uma estação completa acelerada por GPU, e veja os comandos essenciais de operação.</p>
            <div class="pn-grid-2">
                <div class="pn-box">
                    <h4>🖥️ Dimensionamento de Hardware (Debian 12 / Ubuntu 24.04 & 26.04 LTS / WSL2)</h4>
                    <table class="pn-table" style="margin-top: 10px;">
                        <thead>
                            <tr>
                                <th>Componente</th>
                                <th>Mínimo (Sem IA Local)</th>
                                <th>Recomendado (Com IA Local + RAG)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Processador</strong></td>
                                <td>Dual-Core 2.0 GHz+</td>
                                <td>AMD Ryzen 7 ou Intel Core i7+</td>
                            </tr>
                            <tr>
                                <td><strong>Memória RAM</strong></td>
                                <td>4 GB (stack base usa &lt; 1 GB)</td>
                                <td>32 GB RAM</td>
                            </tr>
                            <tr>
                                <td><strong>GPU (Aceleração)</strong></td>
                                <td>Opcional (Translated Library roda na CPU)</td>
                                <td>NVIDIA RTX 3060+ ou equivalente AMD (10–20x mais rápido)</td>
                            </tr>
                            <tr>
                                <td><strong>Armazenamento</strong></td>
                                <td>5 GB a 10 GB livres (+ pacotes ZIM)</td>
                                <td>250 GB+ SSD NVMe (IA consome ~25 GB + ZIMs/Mapas/FDA)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="pn-box">
                    <h4>🛠️ Quickstart & Comandos de Manutenção</h4>
                    <div class="pn-code" style="margin-top: 4px;"># Instalação Rápida em Ubuntu / Debian (acesso em http://localhost:8080)
sudo apt-get update && sudo apt-get install -y curl && \\
curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/refs/heads/main/install/install_nomad.sh \\
  -o install_nomad.sh && sudo bash install_nomad.sh

# Scripts de manutenção em /opt/project-nomad
sudo bash /opt/project-nomad/start_nomad.sh
sudo bash /opt/project-nomad/stop_nomad.sh
sudo bash /opt/project-nomad/update_nomad.sh

# Simular pipeline de Auto-Update (Dry-Run determinístico sem tocar no sistema)
cd admin && node ace auto-update:dry-run --scenarios
node ace auto-update:dry-run --current=1.32.0 --force-enabled</div>
                </div>
            </div>
        </div>
    `;
    container.appendChild(guideWrapper);

    // 2. Docs Explorer Wrapper
    const docsWrapper = document.createElement('div');
    docsWrapper.id = 'pn-docs-wrapper';
    docsWrapper.style.cssText = 'display: none; min-height: calc(100vh - 220px); background: #fff;';

    const sidebar = document.createElement('div');
    sidebar.style.cssText = 'width: 340px; min-width: 340px; border-right: 1px solid #edebe9; background: #faf9f8; overflow-y: auto; padding-bottom: 32px;';

    const contentArea = document.createElement('div');
    contentArea.style.cssText = 'flex: 1; overflow-y: auto; background: #fff;';

    docsWrapper.appendChild(sidebar);
    docsWrapper.appendChild(contentArea);
    container.appendChild(docsWrapper);

    let firstDocItem = null;
    const categories = Object.keys(projectNomadData);

    categories.forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #0284c7';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const linkList = document.createElement('div');
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        catHeader.onclick = () => {
            linkList.style.display = linkList.style.display === 'none' ? 'block' : 'none';
        };

        const docsList = projectNomadData[category];
        docsList.forEach(docItem => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.setAttribute('data-doc-id', docItem.id);
            btn.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">${docItem.icon || '📄'}</span>
                    <span style="font-weight:600; color:#323130; font-size:0.92rem;">${docItem.title}</span>
                </div>
                <div style="font-size:0.78rem; color:#605e5c; margin-top:4px; line-height:1.35; white-space:normal;">
                    ${docItem.description}
                </div>
            `;

            if (!firstDocItem) firstDocItem = { btn, docItem, category };

            btn.onclick = () => {
                document.querySelectorAll('#pn-docs-wrapper .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                contentArea.innerHTML = '<div style="padding:40px; text-align:center; color:#64748b;">⏳ Carregando arquivo...</div>';

                const loadPromise = (typeof docItem.content === 'string')
                    ? Promise.resolve(docItem.content)
                    : fetch(docItem.path + '?v=' + new Date().getTime()).then(r => {
                        if (!r.ok) throw new Error('Arquivo não encontrado: ' + docItem.path);
                        return r.text();
                    });

                loadPromise
                    .then(text => {
                        const isCodeFile = docItem.path.endsWith('.sh') || docItem.path.endsWith('.yaml') || docItem.path.endsWith('.yml') || docItem.path.endsWith('.ts');
                        let renderedBody = '';

                        if (isCodeFile) {
                            const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                            renderedBody = `<pre style="background:#0f172a; color:#f8fafc; padding:22px; border-radius:10px; overflow-x:auto; font-family:'Courier New', monospace; font-size:0.86rem; line-height:1.6; border-left:4px solid #0284c7;"><code>${escaped}</code></pre>`;
                        } else {
                            const preBlocks = [];
                            let processedText = text.replace(/```[a-zA-Z0-9_-]*\r?\n([\s\S]*?)```/g, (match, p1) => {
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
                                .replace(/`([^`]+)`/gim, '<code style="background:#f1f5f9; padding:2px 6px; border-radius:4px; font-family:monospace; color:#0284c7; font-size:0.88em;">$1</code>')
                                .replace(/^\> (.*$)/gim, '<blockquote style="border-left:4px solid #0284c7; background:#f0f9ff; padding:12px 16px; margin:14px 0; color:#0c4a6e; border-radius:0 6px 6px 0;">$1</blockquote>')
                                .replace(/^\- (.*$)/gim, '<li style="margin-left:20px; margin-bottom:6px; line-height:1.6; color:#334155;">$1</li>')
                                .replace(/\r?\n\r?\n/gim, '<br><br>');

                            html = html.replace(/__PRE_BLOCK_(\d+)__/g, (match, idx) => {
                                return `<pre style="background:#0f172a; color:#f8fafc; padding:16px; border-radius:8px; overflow-x:auto; margin:18px 0; font-family:monospace; font-size:0.86rem; line-height:1.5;"><code>${preBlocks[idx]}</code></pre>`;
                            });
                            renderedBody = html;
                        }

                        const fileName = docItem.path.split('/').pop();
                        const headerCard = `
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; margin-bottom: 28px;">
                                <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                                    <div>
                                        <span style="font-size:0.75rem; font-weight:800; color:#0284c7; text-transform:uppercase;">${category}</span>
                                        <h3 style="margin:4px 0 0 0; color:#0f172a; font-size:1.25rem;">${docItem.icon || '📄'} ${docItem.title}</h3>
                                    </div>
                                    <div style="display:flex; gap:10px; align-items:center;">
                                        ${window.favoritesManager ? window.favoritesManager.renderButton(docItem.id, docItem.title, 'Project NOMAD', docItem.path) : ''}
                                        <a href="${docItem.path}" download="${fileName}" style="background:#0284c7; color:#fff; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.85rem;">⬇️ Baixar ${fileName}</a>
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
                        contentArea.scrollTop = 0;
                        if (window.scrollPortalToTop) window.scrollPortalToTop(true);
                    })
                    .catch(err => {
                        contentArea.innerHTML = `<div style="padding:40px; color:#ef4444;">Erro ao carregar arquivo: ${err.message}</div>`;
                    });
            };

            linkList.appendChild(btn);
        });
    });

    const btnGuide = hero.querySelector('#pn-btn-guide');
    const btnDocs = hero.querySelector('#pn-btn-docs');

    btnGuide.onclick = () => {
        btnGuide.classList.add('active');
        btnDocs.classList.remove('active');
        guideWrapper.style.display = 'block';
        docsWrapper.style.display = 'none';
        if (window.scrollPortalToTop) window.scrollPortalToTop(true);
    };

    btnDocs.onclick = () => {
        btnDocs.classList.add('active');
        btnGuide.classList.remove('active');
        guideWrapper.style.display = 'none';
        docsWrapper.style.display = 'flex';
        if (firstDocItem && !docsWrapper.querySelector('.kb-nav-btn.active')) {
            firstDocItem.btn.click();
        }
        if (window.scrollPortalToTop) window.scrollPortalToTop(true);
    };
}
