document.addEventListener('DOMContentLoaded', () => {
    initBananaSlidesView();
});

function initBananaSlidesView() {
    if (typeof bananaSlidesData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'banana-slides-view',
        title: 'Banana Slides',
        badge: 'AI PPT Generator',
        icon: '🍌',
        tagline: 'Transforme ideias, outlines e especificações em apresentações PPTX completas com IA',
        description: 'O <strong>Banana Slides</strong> é uma ferramenta open-source que automatiza a geração de slides e apresentações de alta qualidade a partir de descrições em linguagem natural, integrando diagramas, estruturas visuais e design executivo.',
        themeColor: '#eab308',
        themeGradient: 'linear-gradient(135deg, #422006 0%, #0f172a 60%, #1e1b4b 100%)',
        githubRepo: 'https://github.com/Anionex/banana-slides.git',
        commandPrefix: '/banana:',
        itemType: 'Banana Slides',
        pills: [
            { text: '⭐ GitHub: Anionex/banana-slides', link: 'https://github.com/Anionex/banana-slides.git' },
            { text: '🍌 AI PPT Generator' },
            { text: '📊 Exportação PPTX' },
            { text: '🎨 Design Executivo' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Componentes & Skills' },
            { id: 'cheatsheet', label: '⚡ Como Usar o Banana CLI' }
        ],
        data: bananaSlidesData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🍌</span> Banana Slides CLI & Comandos
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Comandos para gerar apresentações diretamente do seu terminal.
                    </p>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #eab308;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🍌</span> Gerar Apresentação por Tema
                    </div>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Comando</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>npx banana-slides generate --topic "Métricas Ágeis de Fluxo e Previsibilidade" --slides 10 --theme dark</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initBananaSlidesView = initBananaSlidesView;
