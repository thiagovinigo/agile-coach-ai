document.addEventListener('DOMContentLoaded', () => {
    initDemosRagView();
});

function initDemosRagView() {
    const container = document.getElementById('demos-rag-view');
    if (!container || typeof demosRagData === 'undefined') return;

    container.innerHTML = '';

    // Scoped styles for Demos RAG View
    const styleEl = document.createElement('style');
    styleEl.textContent = `
        .dr-hero {
            background: linear-gradient(135deg, #064e3b 0%, #0f172a 60%, #1e1b4b 100%);
            color: #fff;
            padding: 28px 32px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .dr-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid rgba(16, 185, 129, 0.45);
            color: #34d399;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 4px 12px;
            border-radius: 999px;
            margin-bottom: 12px;
        }
        .dr-hero h2 {
            margin: 0 0 8px 0;
            font-size: 1.85rem;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        .dr-hero p {
            margin: 0;
            font-size: 1.02rem;
            line-height: 1.6;
            color: #cbd5e1;
            max-width: 920px;
        }
        .dr-mode-bar {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .dr-mode-btn {
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
        .dr-mode-btn:hover {
            background: rgba(255,255,255,0.15);
        }
        .dr-mode-btn.active {
            background: linear-gradient(135deg, #10b981, #0ea5e9);
            border-color: transparent;
            color: #fff;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
        }
        .dr-guide-container {
            padding: 28px 32px;
            max-width: 1280px;
            margin: 0 auto;
        }
        .dr-card {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        .dr-title {
            margin: 0 0 6px 0;
            font-size: 1.3rem;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .dr-sub {
            margin: 0 0 20px 0;
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
        }
        .dr-grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        .dr-grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
        }
        .dr-grid-4 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
        }
        .dr-step-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-top: 4px solid #10b981;
            border-radius: 10px;
            padding: 16px;
        }
        .dr-code-box {
            background: #0f172a;
            color: #e2e8f0;
            padding: 16px 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.84rem;
            line-height: 1.6;
            overflow-x: auto;
            white-space: pre;
        }
        .dr-file-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #10b981;
            border-radius: 10px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .dr-file-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(0,0,0,0.06);
            border-left-color: #0ea5e9;
        }
        .dr-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }
        .dr-table th, .dr-table td {
            padding: 12px 14px;
            border: 1px solid #e2e8f0;
            text-align: left;
        }
        .dr-table th {
            background: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
        }
    `;
    container.appendChild(styleEl);

    // Hero Header
    const hero = document.createElement('div');
    hero.className = 'dr-hero';
    hero.innerHTML = `
        <div class="dr-badge">🗄️ ETAPA 5 · TEMA 2 · CLAUDE CODE ENGINEERING</div>
        <h2>🗄️ Demos RAG: Supabase, pgvector & Voyage-3 <span style="font-size:0.95rem; font-weight:600; color:#34d399; background:rgba(255,255,255,0.1); padding:4px 10px; border-radius:6px;">Warmup Local + Stack de Produção</span></h2>
        <p>
            Laboratório completo e pronto para rodar demonstrando o ciclo de <strong>Retrieval-Augmented Generation (Ingest → Embed → Store → Retrieve → Augment → Generate)</strong> em dois estágios: um <strong>Warmup 100% Local com ChromaDB</strong> (sem nuvem) e a <strong>Stack Real de Produção com Supabase (Postgres + pgvector HNSW) + Embeddings Voyage-3 (1024 dimensões) + Claude Haiku 4.5</strong>, além da decisão arquitetural entre <code>CLAUDE.md</code> vs Busca Vetorial.
        </p>
        <div class="dr-mode-bar">
            <button class="dr-mode-btn active" id="dr-btn-guide">✨ Guia de Arquitetura & Comparativo</button>
            <button class="dr-mode-btn" id="dr-btn-docs">💻 Explorador de Código & Scripts (8 arquivos)</button>
        </div>
    `;
    container.appendChild(hero);

    // Mode 1: Visual Guide
    const guideWrapper = document.createElement('div');
    guideWrapper.className = 'dr-guide-container';
    guideWrapper.id = 'dr-guide-wrapper';

    // Mode 2: Code Explorer
    const docsWrapper = document.createElement('div');
    docsWrapper.className = 'kb-layout';
    docsWrapper.id = 'dr-docs-wrapper';
    docsWrapper.style.display = 'none';

    container.appendChild(guideWrapper);
    container.appendChild(docsWrapper);

    window.openDemosRagDoc = function(docId) {
        document.getElementById('dr-btn-docs').click();
        const targetBtn = document.querySelector(`#dr-docs-wrapper .kb-nav-btn[data-doc-id="${docId}"]`);
        if (targetBtn) {
            targetBtn.click();
            targetBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    };

    guideWrapper.innerHTML = `
        <!-- 1. PIPELINE DO CICLO RAG -->
        <div class="dr-card">
            <h3 class="dr-title">🔄 O Ciclo Completo de RAG (4 Estágios Fundamentais)</h3>
            <p class="dr-sub">Tanto o script de Warmup Local quanto a Demo de Produção executam exatamente os mesmos 4 estágios fundamentais:</p>
            <div class="dr-grid-4">
                <div class="dr-step-box">
                    <div style="font-size:0.75rem; font-weight:800; color:#059669; text-transform:uppercase; margin-bottom:4px;">ESTÁGIO 1 · INGEST</div>
                    <div style="font-weight:800; color:#0f172a; font-size:1.05rem; margin-bottom:6px;">📥 Ingestão & Embeddings</div>
                    <div style="font-size:0.84rem; color:#475569; line-height:1.5;">
                        Quebra a documentação em chunks e transforma cada trecho em um vetor numérico denso. Na produção, usa <code>voyage-3</code> com <code>input_type="document"</code> gerando vetores de <strong>1024 dimensões</strong> em batch.
                    </div>
                </div>
                <div class="dr-step-box" style="border-top-color:#0ea5e9;">
                    <div style="font-size:0.75rem; font-weight:800; color:#0284c7; text-transform:uppercase; margin-bottom:4px;">ESTÁGIO 2 · STORE</div>
                    <div style="font-weight:800; color:#0f172a; font-size:1.05rem; margin-bottom:6px;">🗄️ Armazenamento Vetorial</div>
                    <div style="font-size:0.84rem; color:#475569; line-height:1.5;">
                        Guarda o texto original, metadados JSONB (ex: <code>{"category": "api"}</code>) e o vetor de 1024 dimensões no Postgres com extensão <code>pgvector</code> e índice <strong>HNSW (<code>vector_cosine_ops</code>)</strong>.
                    </div>
                </div>
                <div class="dr-step-box" style="border-top-color:#8b5cf6;">
                    <div style="font-size:0.75rem; font-weight:800; color:#7c3aed; text-transform:uppercase; margin-bottom:4px;">ESTÁGIO 3 · RETRIEVE</div>
                    <div style="font-weight:800; color:#0f172a; font-size:1.05rem; margin-bottom:6px;">🔍 Busca por Cosseno (Top-K)</div>
                    <div style="font-size:0.84rem; color:#475569; line-height:1.5;">
                        Converte a pergunta do usuário com <code>input_type="query"</code> e chama a RPC <code>match_documents</code> no Supabase usando o operador <code>&lt;=&gt;</code> (distância de cosseno) para trazer os <strong>top 3</strong> trechos.
                    </div>
                </div>
                <div class="dr-step-box" style="border-top-color:#f59e0b;">
                    <div style="font-size:0.75rem; font-weight:800; color:#d97706; text-transform:uppercase; margin-bottom:4px;">ESTÁGIO 4 · AUGMENT & GENERATE</div>
                    <div style="font-weight:800; color:#0f172a; font-size:1.05rem; margin-bottom:6px;">💬 Prompt Aumentado + Haiku</div>
                    <div style="font-size:0.84rem; color:#475569; line-height:1.5;">
                        Injeta apenas os 3 documentos recuperados no prompt do <code>claude-haiku-4-5</code> com guarda-corpo restrito (responder apenas com base no contexto) e wrapper de <strong>retry exponencial (HTTP 429)</strong>.
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. COMPARATIVO: WARMUP LOCAL VS PRODUÇÃO SUPABASE -->
        <div class="dr-card">
            <h3 class="dr-title">⚖️ As 2 Implementações: Warmup Local vs Stack de Produção</h3>
            <p class="dr-sub">Clique em qualquer uma das duas implementações para abrir e baixar o código Python comentado:</p>
            <div class="dr-grid-2">
                <div class="dr-file-card" onclick="openDemosRagDoc('rag-local-warmup')">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="background:#dcfce7; color:#15803d; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:999px;">1. WARMUP ANTES DA AULA</span>
                        <code style="font-size:0.82rem; color:#0f172a; font-weight:700;">rag_local_warmup.py</code>
                    </div>
                    <h4 style="margin:0 0 8px 0; color:#0f172a; font-size:1.15rem;">🏠 RAG 100% Local (ChromaDB + Sentence-Transformers)</h4>
                    <p style="margin:0 0 12px 0; font-size:0.86rem; color:#475569; line-height:1.5;">
                        Ideal para entender o ciclo completo sem configurar nuvem. Usa <code>chromadb.Client()</code> em memória com o modelo local <code>all-MiniLM-L6-v2</code> (zero chave de embeddings).
                    </p>
                    <ul style="margin:0; padding-left:18px; font-size:0.82rem; color:#334155; line-height:1.6;">
                        <li><strong>Precisa apenas de:</strong> <code>ANTHROPIC_API_KEY</code></li>
                        <li><strong>Vantagem:</strong> Roda offline após o <code>pip install</code> e sem rate limit de Voyage.</li>
                        <li><strong>Evolução fácil:</strong> Troque por <code>chromadb.PersistentClient(path=".chromadb")</code> para persistir em disco.</li>
                    </ul>
                </div>

                <div class="dr-file-card" style="border-left-color:#0ea5e9;" onclick="openDemosRagDoc('rag-supabase-voyage')">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="background:#e0f2fe; color:#0369a1; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:999px;">2. DEMO PRINCIPAL DE PRODUÇÃO</span>
                        <code style="font-size:0.82rem; color:#0f172a; font-weight:700;">rag_supabase_voyage.py</code>
                    </div>
                    <h4 style="margin:0 0 8px 0; color:#0f172a; font-size:1.15rem;">🚀 RAG Cloud (Supabase pgvector + Voyage-3 + Haiku)</h4>
                    <p style="margin:0 0 12px 0; font-size:0.86rem; color:#475569; line-height:1.5;">
                        Stack real recomendada pela Anthropic: embeddings de 1024 dimensões no <code>voyage-3</code> com separação entre documento e pergunta, persistidos no Postgres via Supabase.
                    </p>
                    <ul style="margin:0; padding-left:18px; font-size:0.82rem; color:#334155; line-height:1.6;">
                        <li><strong>Assimetria Semântica:</strong> Usa <code>input_type="document"</code> na ingestão e <code>input_type="query"</code> na busca.</li>
                        <li><strong>Proteção contra 3 RPM:</strong> Inclui <code>voyage_embed_with_retry()</code> (esperas de 25s, 50s, 100s para free tier sem cartão).</li>
                        <li><strong>Busca SQL Nativa:</strong> Chama <code>supabase.rpc("match_documents", ...)</code> retornando o score exato de similaridade.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 3. DECISÃO ARQUITETURAL: CLAUDE.MD VS RAG (VÍDEO 3) -->
        <div class="dr-grid-2" style="margin-bottom:24px;">
            <div class="dr-card" style="margin-bottom:0;">
                <h3 class="dr-title">🧠 Decisão de Arquitetura: <code>CLAUDE.md</code> vs RAG Vetorial</h3>
                <p class="dr-sub">Padrão ensinado no Vídeo 3 da formação: quando usar memória estática na raiz do projeto vs banco de vetores?</p>
                <table class="dr-table">
                    <thead>
                        <tr>
                            <th>Critério</th>
                            <th>📄 Usar <code>CLAUDE.md</code></th>
                            <th>🗄️ Usar RAG (Supabase + Voyage)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Volume de Dados</strong></td>
                            <td>Cabe em 1 arquivo (até ~200 linhas)</td>
                            <td>Centenas ou milhares de documentos</td>
                        </tr>
                        <tr>
                            <td><strong>Estabilidade</strong></td>
                            <td>Conteúdo estável (arquitetura, padrões, regras)</td>
                            <td>Conteúdo muda com frequência (indexação contínua)</td>
                        </tr>
                        <tr>
                            <td><strong>Escopo de Uso</strong></td>
                            <td>Toda conversa precisa desse contexto inteiro</td>
                            <td>Busca semântica cirúrgica (Top-K por pergunta)</td>
                        </tr>
                        <tr>
                            <td><strong>Infraestrutura</strong></td>
                            <td>Zero latência, lido automaticamente pelo Claude Code</td>
                            <td>Exige pipeline de Embeddings + índice HNSW</td>
                        </tr>
                    </tbody>
                </table>
                <button onclick="openDemosRagDoc('rag-claude-md')" style="margin-top:14px; background:#f1f5f9; border:1px solid #cbd5e1; padding:8px 14px; border-radius:6px; font-weight:700; font-size:0.82rem; cursor:pointer; color:#0f172a;">📄 Abrir CLAUDE.md de Exemplo</button>
            </div>

            <div class="dr-card" style="margin-bottom:0;">
                <h3 class="dr-title">🗄️ Anatomia do Banco Vetorial (<code>supabase_setup.sql</code>)</h3>
                <p class="dr-sub">Os 5 blocos SQL que preparam o Postgres no Supabase em menos de 3 minutos:</p>
                <div class="dr-code-box">-- 1. Ativa extensão pgvector
create extension if not exists vector;

-- 2. Tabela com vetor de 1024 dimensões (voyage-3)
create table if not exists documents (
  id         bigserial primary key,
  content    text not null,
  embedding  vector(1024) not null,
  metadata   jsonb default '{}'::jsonb
);

-- 3. Índice HNSW com similaridade de cosseno (&lt;=&gt;)
create index if not exists documents_embedding_idx
  on documents using hnsw (embedding vector_cosine_ops);

-- 4. RPC match_documents: 1 - (d.embedding &lt;=&gt; query_embedding)</div>
                <button onclick="openDemosRagDoc('rag-supabase-sql')" style="margin-top:14px; background:#f1f5f9; border:1px solid #cbd5e1; padding:8px 14px; border-radius:6px; font-weight:700; font-size:0.82rem; cursor:pointer; color:#0f172a;">🗄️ Ver SQL Completo + Notas de RLS</button>
            </div>
        </div>

        <!-- 4. TODOS OS ARQUIVOS E VARIAÇÕES AVANÇADAS -->
        <div class="dr-card">
            <h3 class="dr-title">🧰 Catálogo Rápido dos 8 Arquivos + Variações para Live Coding</h3>
            <p class="fr-section-sub">Clique em qualquer arquivo para inspecionar o código-fonte ou baixá-lo para sua máquina:</p>
            <div class="dr-grid-4" style="margin-bottom:20px;">
                <div class="dr-file-card" onclick="openDemosRagDoc('rag-readme')">
                    <div style="font-weight:800; color:#0f172a;">📖 README.md</div>
                    <div style="font-size:0.8rem; color:#475569; margin-top:4px;">Guia de setup em 5 min, comandos de terminal e troubleshooting macOS/Rate Limit.</div>
                </div>
                <div class="dr-file-card" onclick="openDemosRagDoc('rag-claude-md')">
                    <div style="font-weight:800; color:#0f172a;">🧠 CLAUDE.md</div>
                    <div style="font-size:0.8rem; color:#475569; margin-top:4px;">Camada de contexto automática com decisões de arquitetura e prompts de teste.</div>
                </div>
                <div class="dr-file-card" onclick="openDemosRagDoc('rag-test-setup')">
                    <div style="font-weight:800; color:#0f172a;">✅ test_setup.py</div>
                    <div style="font-size:0.8rem; color:#475569; margin-top:4px;">Smoke test que valida chaves e testa Anthropic, Voyage (1024d) e Supabase de uma vez.</div>
                </div>
                <div class="dr-file-card" onclick="openDemosRagDoc('rag-embedding-test')">
                    <div style="font-weight:800; color:#0f172a;">🔬 embedding_test.py</div>
                    <div style="font-size:0.8rem; color:#475569; margin-top:4px;">Script enxuto de 10 linhas para mostrar na tela as dimensões e os floats do vetor.</div>
                </div>
            </div>
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px 18px; font-size:0.88rem; color:#334155;">
                <strong>💡 4 Variações Práticas para Expandir na Aula (se sobrar tempo):</strong>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px; margin-top:8px;">
                    <div>• <strong>Chunking Inteligente:</strong> Quebrar docs longos antes de embedar.</div>
                    <div>• <strong>Filtro Metadata:</strong> Usar <code>metadata @&gt; '{"category":"api"}'</code>.</div>
                    <div>• <strong>Re-ranking:</strong> Aplicar <code>voyage-rerank-2</code> após a busca cosseno.</div>
                    <div>• <strong>Persistência Local:</strong> Usar <code>chromadb.PersistentClient(path=".chromadb")</code>.</div>
                </div>
            </div>
        </div>
    `;

    // Populate Mode 2: Code & Docs Explorer
    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';

    docsWrapper.appendChild(sidebar);
    docsWrapper.appendChild(contentArea);

    const categories = Object.keys(demosRagData);
    let firstDocItem = null;

    categories.forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #10b981';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const linkList = document.createElement('div');
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        catHeader.onclick = () => {
            linkList.style.display = linkList.style.display === 'none' ? 'block' : 'none';
        };

        const docsList = demosRagData[category];
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
                document.querySelectorAll('#dr-docs-wrapper .kb-nav-btn').forEach(b => b.classList.remove('active'));
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
                        const isCodeFile = docItem.path.endsWith('.py') || docItem.path.endsWith('.sql') || docItem.path.endsWith('.txt');
                        let renderedBody = '';

                        if (isCodeFile) {
                            const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                            renderedBody = `<pre style="background:#0f172a; color:#f8fafc; padding:22px; border-radius:10px; overflow-x:auto; font-family:'Courier New', monospace; font-size:0.88rem; line-height:1.6; border-left:4px solid #10b981;"><code>${escaped}</code></pre>`;
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
                                .replace(/`([^`]+)`/gim, '<code style="background:#f1f5f9; padding:2px 6px; border-radius:4px; font-family:monospace; color:#059669; font-size:0.88em;">$1</code>')
                                .replace(/^\> (.*$)/gim, '<blockquote style="border-left:4px solid #10b981; background:#ecfdf5; padding:12px 16px; margin:14px 0; color:#065f46; border-radius:0 6px 6px 0;">$1</blockquote>')
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
                                        <span style="font-size:0.75rem; font-weight:800; color:#059669; text-transform:uppercase;">${category}</span>
                                        <h3 style="margin:4px 0 0 0; color:#0f172a; font-size:1.25rem;">${docItem.icon || '📄'} ${docItem.title}</h3>
                                    </div>
                                    <div style="display:flex; gap:10px; align-items:center;">
                                        ${window.favoritesManager ? window.favoritesManager.renderButton(docItem.id, docItem.title, 'Demos RAG', docItem.path) : ''}
                                        <a href="${docItem.path}" download="${fileName}" style="background:#10b981; color:#fff; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.85rem;">⬇️ Baixar ${fileName}</a>
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
    const btnGuide = hero.querySelector('#dr-btn-guide');
    const btnDocs = hero.querySelector('#dr-btn-docs');

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
