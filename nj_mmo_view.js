document.addEventListener('DOMContentLoaded', () => {
    initNjMmoView();
});

function initNjMmoView() {
    if (typeof njMmoData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'nj-mmo-view',
        title: 'NJ MMO',
        badge: 'Distributed Systems',
        icon: '🎮',
        tagline: 'Arquitetura, contratos de teste e lições aprendidas em sistemas distribuídos de alta escala',
        description: 'O repositório <strong>NJ MMO</strong> reúne especificações técnicas profundas, padrões arquiteturais (AGENTS.md, ROADMAP.md, STATE.md, LESSONS.md) e contratos para agentes operando em bases de código complexas e sensíveis a concorrência.',
        themeColor: '#ef4444',
        themeGradient: 'linear-gradient(135deg, #450a0a 0%, #0f172a 60%, #1e1b4b 100%)',
        itemType: 'NJ MMO',
        pills: [
            { text: '🎮 Arquitetura de MMO' },
            { text: '🤖 AGENTS.md Contracts' },
            { text: '🗺️ Project Roadmap' },
            { text: '💾 State Persistence' },
            { text: '📚 Lessons Learned' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Todos os Documentos & Specs' }
        ],
        data: njMmoData
    });
}

window.initNjMmoView = initNjMmoView;
