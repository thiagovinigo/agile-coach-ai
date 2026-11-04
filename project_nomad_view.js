document.addEventListener('DOMContentLoaded', () => {
    initProjectNomadView();
});

function initProjectNomadView() {
    if (typeof projectNomadData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'project-nomad-view',
        title: 'Project NOMAD',
        badge: 'Offline-First AI & Knowledge Server',
        icon: '🧭',
        tagline: 'Knowledge That Never Goes Offline — Servidor autônomo de Conhecimento, Educação, Mapas e IA Local (Crosstalk Solutions)',
        description: 'O <strong>Project NOMAD</strong> é um servidor 100% <em>Offline-First</em> orquestrado via Docker que reúne <strong>IA Local + RAG Semântico (Ollama & Qdrant)</strong>, <strong>Wikipedia & Biblioteca Médica (Kiwix ZIM)</strong>, <strong>Tradução Neural Offline em 50 idiomas (1.600x mais rápida na CPU via CTranslate2)</strong>, <strong>Khan Academy (Kolibri Gen 2)</strong>, <strong>Bulas Oficiais FDA (openFDA)</strong>, <strong>Mapas Regionais (ProtoMaps)</strong>, <strong>Rádios LoRa Off-Grid (Meshtastic/MeshCore)</strong> e uma suíte determinística de engenharia <strong>AI Quality Harness</strong>.',
        themeColor: '#0284c7',
        themeGradient: 'linear-gradient(135deg, #082f49 0%, #0f172a 60%, #064e3b 100%)',
        githubRepo: 'https://github.com/Crosstalk-Solutions/project-nomad',
        itemType: 'Project NOMAD',
        pills: [
            { text: '⭐ GitHub: Crosstalk-Solutions/project-nomad', link: 'https://github.com/Crosstalk-Solutions/project-nomad' },
            { text: '🌐 projectnomad.us', link: 'https://www.projectnomad.us' },
            { text: '🦙 Ollama + Qdrant RAG' },
            { text: '📚 Kiwix + 50 Idiomas Offline' },
            { text: '💊 FDA Drug Reference (openFDA)' },
            { text: '🧪 AI Quality Harness (RAG Eval)' },
            { text: '📡 Meshtastic & MeshCore LoRa' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todos os Documentos & Scripts (23)' },
            { id: '1. Visão Geral', label: '🧭 Visão Geral & Arquitetura' },
            { id: '2. Documentação', label: '🎛️ Command Center & Supply Depot' },
            { id: '3. Motor RAG', label: '🧪 Motor RAG & AI Eval Harness' },
            { id: '4. Instalação', label: '🐳 Docker Compose & Sidecars' },
            { id: 'cheatsheet', label: '⚡ Guia Completo: Arquitetura, Apps & Comandos' }
        ],
        data: projectNomadData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🧭</span> Project NOMAD — Arquitetura, Ecossistema Offline & Comandos
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Referência rápida da arquitetura de containers, catálogo do Supply Depot, suíte de avaliação científica de RAG e instalação.
                    </p>
                </div>

                <!-- 1. Quickstart & Instalação -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #0284c7;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🚀</span> 1. Instalação Rápida (Ubuntu 26.04 / 24.04 LTS, Debian 12 & WSL2)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Instala automaticamente o Docker, configura o <strong>NVIDIA Container Toolkit</strong> (se houver GPU no host) e sobe o Command Center na porta <code>8080</code>:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Terminal Linux (Requer sudo)</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>sudo apt-get update && \\
sudo apt-get install -y curl && \\
curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/refs/heads/main/install/install_nomad.sh \\
  -o install_nomad.sh && \\
sudo bash install_nomad.sh</code></pre>
                    </div>
                </div>

                <!-- 2. Arquitetura de Containers -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🐳</span> 2. Arquitetura do Command Center & Sidecars (management_compose.yaml)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:14px;">
                        O Command Center gerencia dinamicamente o ciclo de vida dos containers filhos e preserva todo o conteúdo em <code>/opt/project-nomad/storage</code>:
                    </p>
                    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:14px; margin-bottom:12px;">
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px;">
                            <strong style="color:#0f172a; display:block; margin-bottom:4px;">🎛️ nomad_admin (Porta 8080)</strong>
                            <span style="font-size:13px; color:#475569;">AdonisJS 6 + Inertia React + TypeScript. Inspeciona <code>/var/run/docker.sock</code> e mapeia volumes automaticamente para cada app instalado.</span>
                        </div>
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px;">
                            <strong style="color:#0f172a; display:block; margin-bottom:4px;">🦙 Ollama + Qdrant Vector DB</strong>
                            <span style="font-size:13px; color:#475569;">Chat IA local e busca semântica RAG sobre PDFs/manuais enviados na Knowledge Base, além da documentação nativa do NOMAD.</span>
                        </div>
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px;">
                            <strong style="color:#0f172a; display:block; margin-bottom:4px;">🗄️ nomad_mysql + nomad_redis</strong>
                            <span style="font-size:13px; color:#475569;">MySQL 8.0 (chats, manifestos, bulas FDA, benchmarks) e Redis 7 (filas BullMQ para downloads ZIM, extração PMTiles e embeddings).</span>
                        </div>
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px;">
                            <strong style="color:#0f172a; display:block; margin-bottom:4px;">🔄 nomad_updater + disk_collector + dozzle</strong>
                            <span style="font-size:13px; color:#475569;">Sidecars para auto-update seguro com rollback, coleta de uso de disco via <code>/:/host:ro,rslave</code> e visualização de logs na porta <code>9999</code>.</span>
                        </div>
                    </div>
                </div>

                <!-- 3. NOMAD AI Quality Harness -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #8b5cf6;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🧪</span> 3. NOMAD AI Quality Harness — Avaliação Científica e Determinística de RAG
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Localizado em <code>admin/tests/eval/</code>, separa <strong>regressões de código</strong> de <strong>limitações de modelos pequenos</strong> usando um corpus isolado por tag (<code>collection: __nomad_eval__</code>) no Qdrant e 3 modos de geração (<code>oracle</code>, <code>e2e</code>, <code>noretrieval</code> + <code>--model=mock</code>):
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Comandos Ace CLI (Executar em admin/)</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># 1. Validar e ingerir o corpus de avaliação (28 docs de domínio + 6 distractors)
node ace eval:corpus --check
node ace eval:corpus --ingest

# 2. Medir Retrieval determinístico (nDCG, recall@k, precision@k) + ablação do Reranker
node ace eval:retrieval --ablate
node ace eval:retrieval --suite=off_topic --verbose

# 3. Diagnosticar se o gargalo é o Código (Retrieval) ou o Modelo (oracle vs e2e vs noretrieval)
node ace eval:generation --model=llama3.2:latest --all-modes
node ace eval:generation --model=llama3.2:latest --suite=long_context

# 4. Gate de CI: comparar relatório contra baseline com tolerância de regressão (0.02)
node ace eval:compare tests/eval/baselines/&lt;fp&gt;/retrieval.json &lt;new-report.json&gt;</code></pre>
                    </div>
                </div>

                <!-- 4. Auto-Update Dry-Run & Scripts de Manutenção -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #f59e0b;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🛠️</span> 4. Simulação de Auto-Update (Dry-Run) & Scripts de Manutenção
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Teste toda a árvore de decisão do atualizador automático (janelas de horário, período de <em>cool-off</em> e pre-flight checks) sem disparar atualizações reais:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Manutenção & Dry-Run</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Executar a suíte determinística de cenários de Auto-Update (sem precisar de rede ou Docker)
cd admin && node ace auto-update:dry-run --scenarios

# Simular atualização a partir da versão 1.32.0 contra o feed real do GitHub
node ace auto-update:dry-run --current=1.32.0 --force-enabled

# Scripts auxiliares do sistema instalado em /opt/project-nomad
sudo bash /opt/project-nomad/start_nomad.sh
sudo bash /opt/project-nomad/stop_nomad.sh
sudo bash /opt/project-nomad/update_nomad.sh</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initProjectNomadView = initProjectNomadView;
