document.addEventListener('DOMContentLoaded', () => {
    initOpenwikiView();
});

function initOpenwikiView() {
    if (typeof openwikiData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'openwiki-view',
        title: 'OpenWiki',
        badge: 'Knowledge Federation',
        icon: '📖',
        tagline: 'Ecossistema aberto de documentação e conectores de conhecimento para agentes',
        description: 'O <strong>OpenWiki</strong> fornece ferramentas e conectores para federar wikis de conhecimento para agentes autônomos, com migração de documentações para conformidade OKF (Open Knowledge Format) e conectores de dados universais.',
        themeColor: '#14b8a6',
        themeGradient: 'linear-gradient(135deg, #134e4a 0%, #0f172a 60%, #042f2e 100%)',
        itemType: 'OpenWiki',
        pills: [
            { text: '📖 OpenWiki Framework' },
            { text: '🧰 Conectores Universais' },
            { text: '📑 Migração OKF' },
            { text: '🕸️ Federated Knowledge' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Habilidades OpenWiki' }
        ],
        data: openwikiData
    });
}

window.initOpenwikiView = initOpenwikiView;
