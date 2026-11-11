function initSlides3dView() {
    const data = typeof slides3dData !== 'undefined' ? slides3dData : window.slides3dData;
    if (!data || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'slides-3d-view',
        title: 'Preparação de Slides 3D & Cinematográficos',
        badge: 'Cinematic Slides V1.6 · Three.js WebGL',
        icon: '🎬',
        tagline: 'Framework completo de direção de arte, narrativa em arcos, shaders WebGL, modelos 3D Star Wars (.glb) e apresentações imersivas',
        description: 'O ecossistema <strong>Preparação de Slides 3D</strong> reúne 6 skills de inteligência artificial editorial e cinematográfica (<code>cinematic-slides</code>, <code>composicao-do-slide</code>, <code>mensagem-do-slide</code>, <code>publico-do-slide</code>, <code>roteiro-do-slide</code> e <code>visual-do-slide</code>), mais de 10 referências técnicas (shaders GLSL, física de voo, pares tipográficos e ciclo de cena), um catálogo de <strong>6 modelos 3D GLB oficiais</strong> e a demo interativa <strong>Atlas Galáctico (Star Wars)</strong> em Three.js.',
        themeColor: '#e11d48',
        themeGradient: 'linear-gradient(135deg, #4c0519 0%, #0f172a 60%, #881337 100%)',
        githubRepo: 'https://github.com/mrdoob/three.js',
        itemType: 'Slides 3D',
        pills: [
            { text: '🪐 Abrir Apresentação 3D ao Vivo', link: '#slides-3d-demo-view' },
            { text: '🎬 6 Skills de Slides Cinematográficos' },
            { text: '🚀 6 Modelos 3D (.glb) Prontos para Download' },
            { text: '🪐 Sketchfab (Modelos 3D)', link: 'https://sketchfab.com', isExternal: true },
            { text: '🎨 Behance (Pitch Decks)', link: 'https://www.behance.net', isExternal: true },
            { text: '🔤 DaFont (Tipografia Display)', link: 'https://www.dafont.com', isExternal: true },
            { text: '🔮 Shaders GLSL & Efeito Hiperespaço' },
            { text: '⚡ Three.js + WebGL 60 FPS' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Catálogo Completo 3D (30)' },
            { id: '1. Framework', label: '🎬 Framework Cinematográfico (5)' },
            { id: '2. Direção', label: '🔮 Shaders, Movimento & Behance (5)' },
            { id: '3. Pipeline', label: '📜 Roteiro, Mensagem & Público (3)' },
            { id: '4. Design', label: '🎨 Design, Tipografia & DaFont (6)' },
            { id: '5. Modelos', label: '🪐 Modelos 3D GLB & Sketchfab (8)' },
            { id: '6. Demo', label: '⚡ Demo Star Wars (5)' },
            { id: 'cheatsheet', label: '🚀 Cheatsheet de Criação 3D' }
        ],
        data: data,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🎬</span> Guia Rápido — Criação de Apresentações 3D Cinematográficas
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Comandos e prompts recomendados para projetar apresentações WebGL de altíssimo impacto usando Three.js e as skills do kit.
                    </p>
                </div>

                <!-- 1. Como Criar um Deck Cinematográfico -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #e11d48;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🎯</span> 1. Prompt para o Coding Agent Criar um Novo Deck Cinematográfico
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Use esta instrução no Claude Code, Cursor ou Antigravity ativando a skill <code>cinematic-slides</code>:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Prompt Inicial</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>Atue como diretor criativo cinematográfico e aplique a skill cinematic-slides.
Quero construir uma apresentação épica em HTML puro e Three.js para telão gigante.
Tema da Apresentação: [SEU TEMA AQUI]
Público-Alvo: [DIRETORIA / INVESTIDORES / COMUNIDADE TÉCNICA]
Tom Desejado: [MONUMENTAL, PRECISO E MEMORÁVEL]

Inicie conduzindo as 10 decisões fundamentais (entrevista de briefing) e apresente
a proposta de 5 cenas com transição espacial entre elas.</code></pre>
                    </div>
                </div>

                <!-- 2. Rodar a Demo Localmente -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #6366f1;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🚀</span> 2. Testar e Visualizar a Apresentação 3D no Navegador
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        A demo <strong>Atlas Galáctico (Star Wars)</strong> já está integrada neste portal na aba de Apresentações. Se quiser rodar fora via terminal local:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Terminal</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Entrar na pasta da aplicação 3D
cd slides-3d/app

# Subir servidor HTTP local (Python)
python iniciar.py
# Ou: python -m http.server 8000

# Abrir no navegador: http://localhost:8000</code></pre>
                    </div>
                </div>

                <!-- 3. Download Rápido dos Modelos 3D -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🪐</span> 3. Acesso Direto aos Modelos 3D (.glb)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Baixe os modelos espaciais com um clique para usar em seus próprios projetos 3D:
                    </p>
                    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:8px;">
                        <a href="slides-3d/app/assets/millennium-falcon.glb" download="millennium-falcon.glb" style="background:#e11d48; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">⬇️ Millennium Falcon (1.7MB)</a>
                        <a href="slides-3d/app/assets/tie-fighter.glb" download="tie-fighter.glb" style="background:#0f172a; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">⬇️ TIE Fighter (6.6MB)</a>
                        <a href="slides-3d/app/assets/death-star.glb" download="death-star.glb" style="background:#0f172a; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">⬇️ Death Star (18.3MB)</a>
                        <a href="slides-3d/app/assets/tatooine-base.glb" download="tatooine-base.glb" style="background:#0f172a; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">⬇️ Tatooine Base (23.2MB)</a>
                        <a href="slides-3d/app/assets/jedi-starfighter.glb" download="jedi-starfighter.glb" style="background:#0f172a; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">⬇️ Jedi Starfighter (30.2MB)</a>
                        <a href="slides-3d/app/assets/naboo-base.glb" download="naboo-base.glb" style="background:#0f172a; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-weight:700; font-size:13px;">⬇️ Naboo Base (43.5MB)</a>
                    </div>
                
                <!-- 4. Tríade Criativa: Sketchfab, Behance e DaFont -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #f59e0b;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🌟</span> 4. Tríade de Referências: Sketchfab (3D), Behance (Direção de Arte) e DaFont (Tipografia)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Acelere a criação visual das suas apresentações integrando estes três acervos globais:
                    </p>
                    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:14px; margin-top:10px;">
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
                            <h4 style="margin:0 0 8px 0; color:#0f172a; display:flex; align-items:center; gap:8px;">
                                <span>🪐</span> <a href="https://sketchfab.com" target="_blank" style="color:#e11d48; text-decoration:none; font-weight:700;">Sketchfab.com ↗</a>
                            </h4>
                            <p style="margin:0 0 8px 0; font-size:13px; color:#475569; line-height:1.45;">
                                Milhões de modelos 3D em formato <code>.glb</code> com texturas PBR. Filtre por "Downloadable" e licença "CC Attribution" para baixar e carregar via <code>GLTFLoader</code> no Three.js ou incorporar via Viewer API.
                            </p>
                            <span style="font-size:11px; background:#ffe4e6; color:#9f1239; padding:2px 8px; border-radius:4px; font-weight:600;">Assets 3D WebGL</span>
                        </div>
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
                            <h4 style="margin:0 0 8px 0; color:#0f172a; display:flex; align-items:center; gap:8px;">
                                <span>🎨</span> <a href="https://www.behance.net" target="_blank" style="color:#2563eb; text-decoration:none; font-weight:700;">Behance.net ↗</a>
                            </h4>
                            <p style="margin:0 0 8px 0; font-size:13px; color:#475569; line-height:1.45;">
                                A maior vitrine de pitch decks e direção de arte de estúdios internacionais. Busque por <em>"Presentation Design"</em> e <em>"Editorial Layout"</em> para inspirar grids assimétricos e paletas com no máximo 3 cores.
                            </p>
                            <span style="font-size:11px; background:#dbeafe; color:#1e40af; padding:2px 8px; border-radius:4px; font-weight:600;">Direção de Arte & Moodboards</span>
                        </div>
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
                            <h4 style="margin:0 0 8px 0; color:#0f172a; display:flex; align-items:center; gap:8px;">
                                <span>🔤</span> <a href="https://www.dafont.com" target="_blank" style="color:#d97706; text-decoration:none; font-weight:700;">DaFont.com ↗</a>
                            </h4>
                            <p style="margin:0 0 8px 0; font-size:13px; color:#475569; line-height:1.45;">
                                Mais de 80.000 fontes temáticas (Sci-Fi, Cyberpunk, Retro, Brutalista). Baixe os arquivos <code>.ttf</code> gratuitos e declare no CSS via <code>@font-face</code> para títulos monumentais sem depender de conexão externa.
                            </p>
                            <span style="font-size:11px; background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:4px; font-weight:600;">Tipografia Display</span>
                        </div>
                    </div>
                </div>
</div>
            </div>
        `
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSlides3dView);
} else {
    initSlides3dView();
}
window.renderSlides3dView = initSlides3dView;
