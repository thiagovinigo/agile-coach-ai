document.addEventListener('DOMContentLoaded', () => {
    initFlowReelsView();
});

function initFlowReelsView() {
    const container = document.getElementById('flow-reels-view');
    if (!container || typeof flowReelsData === 'undefined') return;

    container.innerHTML = '';

    // Inject scoped styles for Flow Reels View
    const styleEl = document.createElement('style');
    styleEl.textContent = `
        .fr-hero {
            background: linear-gradient(135deg, #090d16 0%, #1e1b4b 55%, #3b0764 100%);
            color: #fff;
            padding: 28px 32px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .fr-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(236, 72, 153, 0.2);
            border: 1px solid rgba(236, 72, 153, 0.45);
            color: #f472b6;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 4px 12px;
            border-radius: 999px;
            margin-bottom: 12px;
        }
        .fr-hero h2 {
            margin: 0 0 8px 0;
            font-size: 1.85rem;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .fr-hero p {
            margin: 0;
            font-size: 1.02rem;
            line-height: 1.6;
            color: #cbd5e1;
            max-width: 920px;
        }
        .fr-mode-bar {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .fr-mode-btn {
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
        .fr-mode-btn:hover {
            background: rgba(255,255,255,0.15);
        }
        .fr-mode-btn.active {
            background: linear-gradient(135deg, #ec4899, #8b5cf6);
            border-color: transparent;
            color: #fff;
            box-shadow: 0 4px 12px rgba(236, 72, 153, 0.35);
        }
        .fr-guide-container {
            padding: 28px 32px;
            max-width: 1280px;
            margin: 0 auto;
        }
        .fr-section-card {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        .fr-section-title {
            margin: 0 0 6px 0;
            font-size: 1.3rem;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .fr-section-sub {
            margin: 0 0 20px 0;
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
        }
        .fr-grid-4 {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
            gap: 16px;
        }
        .fr-grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 16px;
        }
        .fr-skill-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #8b5cf6;
            border-radius: 10px;
            padding: 16px;
            transition: all 0.2s;
            cursor: pointer;
        }
        .fr-skill-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(0,0,0,0.06);
            border-color: #cbd5e1;
            border-left-color: #ec4899;
        }
        .fr-cmd-pill {
            display: inline-block;
            font-family: 'Courier New', monospace;
            font-size: 0.82rem;
            font-weight: 700;
            background: #0f172a;
            color: #38bdf8;
            padding: 4px 10px;
            border-radius: 6px;
            margin-bottom: 8px;
        }
        .fr-pipeline-flow {
            display: flex;
            align-items: stretch;
            gap: 10px;
            overflow-x: auto;
            padding-bottom: 8px;
        }
        .fr-pipe-step {
            flex: 1;
            min-width: 155px;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 14px;
            position: relative;
        }
        .fr-pipe-step.human-stop {
            background: #fffbeb;
            border: 2px solid #f59e0b;
        }
        .fr-pipe-badge {
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 6px;
        }
        .fr-pill-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .fr-pill {
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            color: #1e293b;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .fr-tree-box {
            background: #0f172a;
            color: #e2e8f0;
            padding: 18px 22px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            line-height: 1.65;
            overflow-x: auto;
        }
    `;
    container.appendChild(styleEl);

    // Hero Header
    const hero = document.createElement('div');
    hero.className = 'fr-hero';
    hero.innerHTML = `
        <div class="fr-badge">🎬 PLUGIN CLAUDE CODE + MOTOR 2.0 + STUDIO WEB</div>
        <h2>🎬 Flow Reels 3.0 <span style="font-size:1rem; font-weight:600; color:#f472b6; background:rgba(255,255,255,0.1); padding:4px 10px; border-radius:6px;">Fábrica de Cortes & Reels Narrados</span></h2>
        <p>
            Ecossistema completo que transforma vídeos longos (ou tendências do zero) em Reels verticais 1080×1920 prontos para Instagram, TikTok e Shorts. 
            Lê a transcrição inteira, filtra ganchos com <strong>6 eliminadores + subagente Leitor Frio</strong>, compõe cenas com <strong>Liquid Glass, Visão 3D (Depth Anything + BiRefNet) e Modo Mundo</strong>, audita o vídeo com <strong>13 Gates Automáticos</strong> e publica com funil de DM.
        </p>
        <div class="fr-mode-bar">
            <button class="fr-mode-btn active" id="fr-btn-guide">✨ Guia Visual & Arquitetura</button>
            <button class="fr-mode-btn" id="fr-btn-docs">📚 Explorador de Skills & Documentos (34 arquivos)</button>
        </div>
    `;
    container.appendChild(hero);

    // Mode 1: Visual Guide Container
    const guideWrapper = document.createElement('div');
    guideWrapper.className = 'fr-guide-container';
    guideWrapper.id = 'fr-guide-wrapper';

    // Mode 2: KB Docs Explorer Container
    const docsWrapper = document.createElement('div');
    docsWrapper.className = 'kb-layout';
    docsWrapper.id = 'fr-docs-wrapper';
    docsWrapper.style.display = 'none';

    container.appendChild(guideWrapper);
    container.appendChild(docsWrapper);

    // Helper to jump to a specific doc in Explorer
    window.openFlowReelsDoc = function(docId) {
        document.getElementById('fr-btn-docs').click();
        const targetBtn = document.querySelector(`#fr-docs-wrapper .kb-nav-btn[data-doc-id="${docId}"]`);
        if (targetBtn) {
            targetBtn.click();
            targetBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    };

    // Populate Visual Guide
    guideWrapper.innerHTML = `
        <!-- 1. AS 3 ENTRADAS E O FLUXO COM 3 PARADAS HUMANAS -->
        <div class="fr-section-card">
            <h3 class="fr-section-title">🛣️ Arquitetura de Orquestração & As 3 Paradas de Decisão Humana</h3>
            <p class="fr-section-sub">
                O Flow Reels não é um cortador cego. Ele opera por contratos estritos entre 8 skills e <strong>para obrigatoriamente nos 3 pontos onde a decisão pertence ao humano</strong>. Clique em qualquer etapa para abrir sua especificação completa.
            </p>
            <div class="fr-pipeline-flow">
                <div class="fr-pipe-step" onclick="openFlowReelsDoc('skill-marca')" style="cursor:pointer;">
                    <span class="fr-pipe-badge" style="background:#e0e7ff; color:#4f46e5;">PASSO 0 · UMA VEZ</span>
                    <div style="font-weight:800; color:#0f172a; margin-bottom:4px;">🎨 1. DNA da Marca</div>
                    <div style="font-size:0.8rem; color:#475569;">Extrai cores, fontes, superfície e foto da capa. Gera <code>tokens.json</code> e amostra 1080×956.</div>
                </div>
                <div class="fr-pipe-step" onclick="openFlowReelsDoc('skill-tendencias')" style="cursor:pointer;">
                    <span class="fr-pipe-badge" style="background:#dcfce7; color:#15803d;">OPCIONAL · ANTES</span>
                    <div style="font-weight:800; color:#0f172a; margin-bottom:4px;">📡 2. Tendências</div>
                    <div style="font-size:0.8rem; color:#475569;">Varre Reddit, YT, GitHub e HN. Entrega roteiro de 40-50s medido na fala + kit de gravação.</div>
                </div>
                <div class="fr-pipe-step" onclick="openFlowReelsDoc('skill-transcrever')" style="cursor:pointer;">
                    <span class="fr-pipe-badge" style="background:#f1f5f9; color:#334155;">ETAPA 1 · DADOS</span>
                    <div style="font-weight:800; color:#0f172a; margin-bottom:4px;">🎙️ 3. Transcrever</div>
                    <div style="font-size:0.8rem; color:#475569;">Baixa (Local, YT, Drive) e alinha palavra a palavra (<code>palavras.json</code> + <code>audio16k.wav</code>).</div>
                </div>
                <div class="fr-pipe-step human-stop" onclick="openFlowReelsDoc('skill-planejar')" style="cursor:pointer;">
                    <span class="fr-pipe-badge" style="background:#fef3c7; color:#b45309;">🛑 PARADA HUMANA #1</span>
                    <div style="font-weight:800; color:#0f172a; margin-bottom:4px;">🧠 4. Planejar Ganchos</div>
                    <div style="font-size:0.8rem; color:#78350f;">6 eliminadores + Leitor Frio. Apresenta os ganchos sobreviventes e <strong>espera seu aceite</strong>.</div>
                </div>
                <div class="fr-pipe-step human-stop" onclick="openFlowReelsDoc('skill-produzir')" style="cursor:pointer;">
                    <span class="fr-pipe-badge" style="background:#fef3c7; color:#b45309;">🛑 PARADA HUMANA #2</span>
                    <div style="font-weight:800; color:#0f172a; margin-bottom:4px;">🎬 5. Produzir & Revisar</div>
                    <div style="font-size:0.8rem; color:#78350f;">Subagentes paralelos + 13 Gates Automáticos. Sobe página web (8790) para <strong>aprovação visual</strong>.</div>
                </div>
                <div class="fr-pipe-step human-stop" onclick="openFlowReelsDoc('skill-publicar')" style="cursor:pointer;">
                    <span class="fr-pipe-badge" style="background:#fef3c7; color:#b45309;">🛑 PARADA HUMANA #3</span>
                    <div style="font-weight:800; color:#0f172a; margin-bottom:4px;">📲 6. Publicar & DM</div>
                    <div style="font-size:0.8rem; color:#78350f;">Mostra preview em seco (<code>--seco</code>) + funil "comenta a palavra". Só posta com <strong>SIM explícito</strong>.</div>
                </div>
            </div>
        </div>

        <!-- 2. CATÁLOGO DAS 8 SKILLS -->
        <div class="fr-section-card">
            <h3 class="fr-section-title">🧰 As 8 Skills do Plugin (Comandos Claude Code)</h3>
            <p class="fr-section-sub">
                Você pode acionar cada etapa pelo comando curto ou pedindo em linguagem natural no Claude Code. Clique em um card para ler o <code>SKILL.md</code> original.
            </p>
            <div class="fr-grid-4">
                <div class="fr-skill-card" onclick="openFlowReelsDoc('skill-fabrica')">
                    <span class="fr-cmd-pill">/flow-reels:fabrica</span>
                    <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">🏭 Fábrica (Orquestrador)</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.45;">Porta de entrada principal. Lê o <code>setup.json</code>, identifica se a entrada é corte, tendência ou narrado e coordena todas as skills.</div>
                </div>
                <div class="fr-skill-card" onclick="openFlowReelsDoc('skill-tendencias')">
                    <span class="fr-cmd-pill">/flow-reels:tendencias</span>
                    <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">📡 Radar de Tendências</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.45;">Duas entradas: <strong>Nicho</strong> (Reddit sem chave, YT Brasil, GitHub, HN, Product Hunt) ou <strong>Tema</strong> (pesquisa bilingue PT+EN).</div>
                </div>
                <div class="fr-skill-card" onclick="openFlowReelsDoc('skill-marca')">
                    <span class="fr-cmd-pill">/flow-reels:marca</span>
                    <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">🎨 Onboarding da Marca</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.45;">Extrai identidade de manual PDF ou print de post. Trata fontes variáveis, recorta foto de capa e gera <code>marca/tokens.json</code>.</div>
                </div>
                <div class="fr-skill-card" onclick="openFlowReelsDoc('skill-transcrever')">
                    <span class="fr-cmd-pill">/flow-reels:transcrever</span>
                    <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">🎙️ Transcrição Alinhada</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.45;">Rota nuvem rápida (Replicate) ou gratuita local (WhisperX). Entrega <code>transcricao.md</code>, <code>palavras.json</code> e <code>audio16k.wav</code>.</div>
                </div>
                <div class="fr-skill-card" onclick="openFlowReelsDoc('skill-planejar')">
                    <span class="fr-cmd-pill">/flow-reels:planejar</span>
                    <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">🧠 Planejador & Ganchos</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.45;">Separa levantamento generoso de julgamento impiedoso. Aplica 6 eliminadores, Leitor Frio e âncoras de tempo por palavra.</div>
                </div>
                <div class="fr-skill-card" onclick="openFlowReelsDoc('skill-produzir')">
                    <span class="fr-cmd-pill">/flow-reels:produzir</span>
                    <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">🎬 Produção Paralela</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.45;">Abre 1 subagente por corte aprovado (regra: 1 pasta = 1 dono). Compõe cenas 1080×1920, gera capa e sobe servidor de revisão.</div>
                </div>
                <div class="fr-skill-card" onclick="openFlowReelsDoc('skill-publicar')">
                    <span class="fr-cmd-pill">/flow-reels:publicar</span>
                    <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">📲 Publicação & Funil DM</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.45;">Integra com API Zernio para postar/agendar em Instagram e YouTube e configurar automação "comenta a PALAVRA -> recebe link na DM".</div>
                </div>
                <div class="fr-skill-card" onclick="openFlowReelsDoc('skill-narrado')">
                    <span class="fr-cmd-pill">/flow-reels:narrado</span>
                    <div style="font-weight:700; color:#0f172a; margin-bottom:6px;">🗣️ Reel Narrado (Sem Rosto)</div>
                    <div style="font-size:0.83rem; color:#475569; line-height:1.45;">Gera locução na ElevenLabs sobre filmagem real (keynote, tela), com cartão de logo, zoom guiado + anel desenhado à mão.</div>
                </div>
            </div>
        </div>

        <!-- 3. MOTOR 2.0: MODOS DE CENA & 12 LINGUAGENS VISUAIS -->
        <div class="fr-grid-3" style="margin-bottom: 24px;">
            <div class="fr-section-card" style="margin-bottom:0;">
                <h3 class="fr-section-title">🎥 Modos de Cena (Motor 2.0)</h3>
                <p class="fr-section-sub">Cada trecho do corte é uma cena animada por uma timeline GSAP determinística no Chromium:</p>
                <ul style="margin:0; padding-left:18px; color:#334155; font-size:0.88rem; line-height:1.65;">
                    <li><strong>Rosto + Vidro:</strong> Tela cheia com cards de <em>Liquid Glass</em> entrando por cima.</li>
                    <li><strong>Tela + Bolha:</strong> Gravação de tela com zoom guiado e rosto numa bolha de vidro.</li>
                    <li><strong>Modo Mundo:</strong> O app/planilha ocupa a tela inteira com câmera passeando (até 7 movimentos) e seu rosto entra num card com a cabeça saindo pela borda (máscara BiRefNet).</li>
                    <li><strong>Vidro Líquido:</strong> A cena dentro de uma placa de vidro espessa que inclina, gira e mergulha em 3D.</li>
                    <li><strong>Tela Cortada 3D:</strong> Vídeo separado em camadas reais de profundidade (Depth Anything V2) com tipografia passando atrás de você.</li>
                    <li><strong>Editorial & Dados:</strong> Imagem cheia, Manchete grifada, Lado a Lado (comparação com vencedor), Lista empilhada, Tipografia cinética e Painel + Rosto.</li>
                </ul>
                <button onclick="openFlowReelsDoc('ref-modelos-cenas')" style="margin-top:14px; background:#f1f5f9; border:1px solid #cbd5e1; padding:7px 14px; border-radius:6px; font-weight:700; font-size:0.82rem; cursor:pointer; color:#0f172a;">📖 Ver Catálogo de Modos de Cena</button>
            </div>

            <div class="fr-section-card" style="margin-bottom:0;">
                <h3 class="fr-section-title">🎭 12 Linguagens Visuais & Efeitos</h3>
                <p class="fr-section-sub">O planejador sugere 3 direções de arte por episódio sem repetir os últimos reels:</p>
                <div class="fr-pill-list" style="margin-bottom:16px;">
                    <span class="fr-pill">🧊 Vidro (Liquid Glass)</span>
                    <span class="fr-pill">💻 Terminal</span>
                    <span class="fr-pill">🎬 Cinema</span>
                    <span class="fr-pill">✂️ Recorte</span>
                    <span class="fr-pill">🛸 Sci-Fi</span>
                    <span class="fr-pill">🕹️ Anos 80</span>
                    <span class="fr-pill">🗯️ Mangá</span>
                    <span class="fr-pill">🕶️ Profundidade 3D</span>
                    <span class="fr-pill">📰 Editorial</span>
                    <span class="fr-pill">⚡ Turbo</span>
                    <span class="fr-pill">🌿 Calmo</span>
                    <span class="fr-pill">🗞️ Manchete</span>
                </div>
                <div style="font-size:0.85rem; color:#475569; line-height:1.55; background:#f8fafc; padding:12px; border-radius:8px; border:1px solid #e2e8f0;">
                    <strong>Acabamento & Gatilhos:</strong><br>
                    • <strong>14 Looks de Vídeo + 13 Efeitos Pós:</strong> CRT, VHS, holograma, pontilhado, LUTs da marca (legenda sempre nítida por cima).<br>
                    • <strong>Gatilhos MediaPipe:</strong> Gestos de mãos e expressões faciais disparam efeitos.<br>
                    • <strong>15 Famílias de Som:</strong> Efeitos sintetizados que desviam da sílaba tônica.
                </div>
                <button onclick="openFlowReelsDoc('motor-estetica')" style="margin-top:14px; background:#f1f5f9; border:1px solid #cbd5e1; padding:7px 14px; border-radius:6px; font-weight:700; font-size:0.82rem; cursor:pointer; color:#0f172a;">🎨 Ver Especificação das 12 Linguagens</button>
            </div>

            <div class="fr-section-card" style="margin-bottom:0;">
                <h3 class="fr-section-title">🛡️ 7 Critérios & 13 Gates Automáticos</h3>
                <p class="fr-section-sub"><strong>"Um defeito, um dono."</strong> Antes de subir a revisão, <code>conferir_reel.py</code> audita o MP4:</p>
                <ul style="margin:0; padding-left:18px; color:#334155; font-size:0.85rem; line-height:1.6;">
                    <li><strong>1. Abertura & Formato:</strong> Passa nos 6 eliminadores e na leitura fria de subagente isolado.</li>
                    <li><strong>2. Corte Limpo:</strong> Entrada/saída em silêncio real (&lt;8% de energia por 150ms no <code>audio16k.wav</code>).</li>
                    <li><strong>3. Ritmo Visual:</strong> Algo muda na tela a cada 2 a 2.5 segundos.</li>
                    <li><strong>4. Zonas Seguras:</strong> Topo 220px, base 480px, laterais 70px livres da UI do Instagram/TikTok.</li>
                    <li><strong>5. Contraste & Rosto:</strong> Legenda com contorno medido e zero colisão sobre o rosto.</li>
                    <li><strong>6. Áudio & Emendas:</strong> Normalizado em <strong>-14 LUFS</strong> e zoom alternado nas emendas do editor de fala.</li>
                    <li><strong>7. Acervo Oficial:</strong> Logos reais de 91 marcas (proibido desenhar marca à mão).</li>
                </ul>
                <button onclick="openFlowReelsDoc('ref-gates-7')" style="margin-top:14px; background:#f1f5f9; border:1px solid #cbd5e1; padding:7px 14px; border-radius:6px; font-weight:700; font-size:0.82rem; cursor:pointer; color:#0f172a;">🛡️ Ver Manual dos Gates</button>
            </div>
        </div>

        <!-- 4. STUDIO WEB 3.0 & ISOLAMENTO DE PASTAS -->
        <div class="fr-grid-3">
            <div class="fr-section-card" style="margin-bottom:0;">
                <h3 class="fr-section-title">🖥️ Flow Reels Studio 3.0 (Interface Web)</h3>
                <p class="fr-section-sub">Além do CLI no Claude Code, a pasta traz um estúdio web completo em <code>studio/server.py</code> (porta 8080):</p>
                <ul style="margin:0; padding-left:18px; color:#334155; font-size:0.88rem; line-height:1.65;">
                    <li><strong>🌐 Criador Universal por URL:</strong> Cole o link de qualquer site (ex: clínica, SaaS, e-commerce) e a IA extrai nicho, público, palavra-chave da DM e gera 4 pautas sob medida.</li>
                    <li><strong>✨ Wizard Passo a Passo:</strong> Crie novos reels escolhendo velocidade da fala, trilha sonora com preview de áudio e linguagem visual.</li>
                    <li><strong>🎬 Player HTTP 206 & Validador (8790):</strong> Streaming local com suporte a Range Request e integração direta com a página de revisão de cortes.</li>
                </ul>
                <button onclick="openFlowReelsDoc('studio-server')" style="margin-top:14px; background:#f1f5f9; border:1px solid #cbd5e1; padding:7px 14px; border-radius:6px; font-weight:700; font-size:0.82rem; cursor:pointer; color:#0f172a;">💻 Ver Código do Studio Server</button>
            </div>

            <div class="fr-section-card" style="margin-bottom:0; grid-column: span 2;">
                <h3 class="fr-section-title">📂 Arquitetura de Isolamento da Pasta de Trabalho</h3>
                <p class="fr-section-sub">
                    O código do plugin mora em <code>plugins/flow-reels/</code> e nunca mistura com os seus arquivos. Dentro de cada projeto, <strong>a pasta do corte tem apenas o MP4 final</strong> — todo o material intermediário fica isolado em <code>materiais-de-trabalho/</code>:
                </p>
                <div class="fr-tree-box">projetos/&lt;nome-do-video&gt;/
├── corte-01/
│   └── corte-01.mp4              # A ENTREGA FINAL (e absolutamente mais nada aqui dentro)
├── narrado-01/
│   └── narrado-01.mp4            # Reel sem rosto (ElevenLabs + filmagem real)
├── revisao/                      # Página web interativa onde você assiste e aprova (porta 8790)
├── transcricao.md                # Fala legível com marca de tempo
├── GANCHOS.md                    # Estoque completo de candidatos (aprovados + descartados + leitura fria)
└── materiais-de-trabalho/        # Tudo o que é arquivo de máquina fica isolado aqui
    ├── INVENTARIO.md             # Rota visual de cada ferramenta/conceito falado no vídeo
    ├── fonte/                    # Vídeo bruto original e gravação de tela
    ├── transcricao/              # palavras.json e audio16k.wav (validação de silêncio)
    ├── corte-01/                 # brief.md, cenas.json, fala.mp4, rosto.json, visao/, eventos.json
    └── publicacao/               # Payloads post-NN.json e postIds da Zernio</div>
            </div>
        </div>
    `;

    // Populate KB Docs Explorer (Mode 2)
    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';

    docsWrapper.appendChild(sidebar);
    docsWrapper.appendChild(contentArea);

    const categories = Object.keys(flowReelsData);
    let firstDocItem = null;

    categories.forEach(category => {
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #ec4899';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const linkList = document.createElement('div');
        linkList.style.display = 'block';
        sidebar.appendChild(linkList);

        catHeader.onclick = () => {
            linkList.style.display = linkList.style.display === 'none' ? 'block' : 'none';
        };

        const docsList = flowReelsData[category];
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
                document.querySelectorAll('#fr-docs-wrapper .kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                contentArea.innerHTML = '<div style="padding:40px; text-align:center; color:#64748b;">⏳ Carregando documento...</div>';

                fetch(docItem.path + '?v=' + new Date().getTime())
                    .then(r => {
                        if (!r.ok) throw new Error('Documento não encontrado: ' + docItem.path);
                        return r.text();
                    })
                    .then(text => {
                        const isJsonOrPy = docItem.path.endsWith('.json') || docItem.path.endsWith('.py');
                        let renderedBody = '';

                        if (isJsonOrPy) {
                            const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                            renderedBody = `<pre style="background:#0f172a; color:#f8fafc; padding:20px; border-radius:8px; overflow-x:auto; font-family:monospace; font-size:0.88rem; line-height:1.55;"><code>${escaped}</code></pre>`;
                        } else {
                            // Strip YAML frontmatter if present
                            let cleanText = text.replace(/^---[\s\S]*?---\n/, '');
                            const preBlocks = [];
                            let processedText = cleanText.replace(/```[a-zA-Z0-9_-]*\n([\s\S]*?)```/g, (match, p1) => {
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
                                .replace(/`([^`]+)`/gim, '<code style="background:#f1f5f9; padding:2px 6px; border-radius:4px; font-family:monospace; color:#db2777; font-size:0.88em;">$1</code>')
                                .replace(/^\> (.*$)/gim, '<blockquote style="border-left:4px solid #ec4899; background:#fdf2f8; padding:12px 16px; margin:14px 0; color:#831843; border-radius:0 6px 6px 0;">$1</blockquote>')
                                .replace(/^\- (.*$)/gim, '<li style="margin-left:20px; margin-bottom:6px; line-height:1.6; color:#334155;">$1</li>')
                                .replace(/\n\n/gim, '<br><br>');

                            html = html.replace(/__PRE_BLOCK_(\d+)__/g, (match, idx) => {
                                return `<pre style="background:#0f172a; color:#f8fafc; padding:16px; border-radius:8px; overflow-x:auto; margin:18px 0; font-family:monospace; font-size:0.88rem; line-height:1.5;"><code>${preBlocks[idx]}</code></pre>`;
                            });
                            renderedBody = html;
                        }

                        const headerCard = `
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; margin-bottom: 28px;">
                                <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                                    <div>
                                        <span style="font-size:0.75rem; font-weight:800; color:#db2777; text-transform:uppercase;">${category}</span>
                                        <h3 style="margin:4px 0 0 0; color:#0f172a; font-size:1.25rem;">${docItem.icon || '📄'} ${docItem.title}</h3>
                                    </div>
                                    <div style="display:flex; gap:10px; align-items:center;">
                                        ${window.favoritesManager ? window.favoritesManager.renderButton(docItem.id, docItem.title, 'Flow Reels 3.0', docItem.path) : ''}
                                        <a href="${docItem.path}" download style="background:#ec4899; color:#fff; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.85rem;">⬇️ Baixar Arquivo</a>
                                        <a href="${docItem.path}" target="_blank" style="background:#fff; color:#334155; border:1px solid #cbd5e1; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:700; font-size:0.85rem;">👀 Abrir Original</a>
                                    </div>
                                </div>
                                <p style="margin:0 0 12px 0; color:#475569; font-size:0.92rem;">${docItem.description}</p>
                                <div style="background:#f1f5f9; border:1px solid #cbd5e1; padding:6px 10px; border-radius:4px; font-family:monospace; font-size:0.8rem; color:#475569;">
                                    📂 <strong>Caminho no Portal:</strong> ${docItem.path}
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
                        contentArea.innerHTML = `<div style="padding:40px; color:#ef4444;">Erro ao carregar documento: ${err.message}</div>`;
                    });
            };

            linkList.appendChild(btn);
        });
    });

    // Mode toggle buttons
    const btnGuide = hero.querySelector('#fr-btn-guide');
    const btnDocs = hero.querySelector('#fr-btn-docs');

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
