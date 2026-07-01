// Global favorites manager
window.favoritesManager = {
    getFavorites: function() {
        try {
            return JSON.parse(localStorage.getItem('ac_favorites')) || [];
        } catch(e) {
            return [];
        }
    },
    saveFavorites: function(favs) {
        localStorage.setItem('ac_favorites', JSON.stringify(favs));
        window.favoritesManager.renderView();
    },
    isFavorite: function(id) {
        const favs = this.getFavorites();
        return favs.some(f => f.id === id);
    },
    toggleFavorite: function(id, title, type, path) {
        let favs = this.getFavorites();
        if(this.isFavorite(id)) {
            favs = favs.filter(f => f.id !== id);
        } else {
            favs.push({ id, title, type, path });
        }
        this.saveFavorites(favs);
        
        // Re-render the current view if it has favorites buttons
        // This is a simple hack to update all buttons without full reload
        document.querySelectorAll(`.fav-btn-${id}`).forEach(btn => {
            if(this.isFavorite(id)) {
                btn.innerHTML = '⭐ Favoritado';
                btn.style.backgroundColor = '#fef08a';
                btn.style.borderColor = '#facc15';
                btn.style.color = '#854d0e';
            } else {
                btn.innerHTML = '☆ Favoritar';
                btn.style.backgroundColor = '#fff';
                btn.style.borderColor = '#cbd5e1';
                btn.style.color = '#334155';
            }
        });
    },
    renderButton: function(id, title, type, path) {
        const isFav = this.isFavorite(id);
        const bg = isFav ? '#fef08a' : '#fff';
        const border = isFav ? '#facc15' : '#cbd5e1';
        const color = isFav ? '#854d0e' : '#334155';
        const text = isFav ? '⭐ Favoritado' : '☆ Favoritar';
        
        return `<button class="fav-btn-${id}" onclick="window.favoritesManager.toggleFavorite('${id}', '${title}', '${type}', '${path}')" style="display:inline-flex; align-items:center; gap:5px; background-color:${bg}; color:${color}; padding:8px 15px; border-radius:6px; cursor:pointer; font-weight:bold; border: 1px solid ${border}; font-size:0.95rem; transition: all 0.2s; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
            ${text}
        </button>`;
    },
    renderView: function() {
        const container = document.getElementById('favorites-view');
        if(!container) return;
        
        const favs = this.getFavorites();
        
        if (favs.length === 0) {
            container.innerHTML = `
            <div class="card" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:3rem; text-align:center; box-shadow:0 4px 6px rgba(0,0,0,0.02); max-width: 800px; margin: 0 auto; margin-top: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⭐</div>
                <h3 style="margin-bottom:1rem; color:#1a202c; font-size:1.8rem;">Nenhum favorito ainda</h3>
                <p style="color:#4a5568; font-size:1.1rem; line-height:1.7; max-width: 500px; margin: 0 auto;">
                    Navegue pelos módulos de Agentes, Skills, Superpowers ou Integrações e clique no botão <strong>☆ Favoritar</strong> para salvar suas ferramentas mais usadas aqui.
                </p>
            </div>`;
            return;
        }

        const grouped = favs.reduce((acc, f) => {
            if(!acc[f.type]) acc[f.type] = [];
            acc[f.type].push(f);
            return acc;
        }, {});

        let html = `
        <div style="padding: 2rem; max-width: 1000px; margin: 0 auto;">
            <div style="margin-bottom: 3rem;">
                <h2 style="color:#0f172a; font-size:2.5rem; margin-bottom:10px; display:flex; align-items:center; gap:15px;">
                    ⭐ Meus Favoritos
                </h2>
                <p style="color:#4a5568; font-size:1.1rem;">Acesso rápido às suas ferramentas e agentes mais utilizados.</p>
            </div>
        `;

        for (const [type, items] of Object.entries(grouped)) {
            html += `
            <div style="margin-bottom: 2.5rem;">
                <h3 style="color:#334155; font-size:1.4rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.05em;">
                    ${type}
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem;">
            `;

            items.forEach(item => {
                html += `
                    <div style="background:#fff; border:1px solid #cbd5e1; border-radius:8px; padding:1.5rem; box-shadow:0 2px 4px rgba(0,0,0,0.05); position: relative;">
                        <button onclick="window.favoritesManager.toggleFavorite('${item.id}', '${item.title}', '${item.type}', '${item.path}')" style="position:absolute; top:15px; right:15px; background:none; border:none; cursor:pointer; font-size:1.2rem; opacity:0.6; transition:opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.6'" title="Remover dos favoritos">❌</button>
                        
                        <h4 style="margin:0 0 10px 0; color:#0f172a; font-size:1.15rem; padding-right: 20px;">${item.title}</h4>
                        
                        ${item.path && item.path !== 'undefined' ? `
                            <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:8px 12px; border-radius:4px; font-family:monospace; font-size:0.8rem; color:#475569; word-break:break-all; margin-bottom: 15px;">
                                📂 ${item.path}
                            </div>
                        ` : ''}
                        
                        <div style="display: flex; gap: 10px;">
                            ${item.path && item.path !== 'undefined' ? `
                            <a href="${item.path}" download="${item.id}.md" style="font-size:0.85rem; color:#0078d4; text-decoration:none; font-weight:600; display:flex; align-items:center; gap:4px;">⬇️ Baixar</a>
                            <a href="${item.path}" target="_blank" style="font-size:0.85rem; color:#475569; text-decoration:none; font-weight:600; display:flex; align-items:center; gap:4px;">👀 Ver</a>
                            ` : ''}
                        </div>
                    </div>
                `;
            });

            html += `</div></div>`;
        }

        html += `</div>`;
        container.innerHTML = html;
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // Escutar mudanças no hash para renderizar a view de favoritos ao abri-la
    window.addEventListener('hashchange', () => {
        if(window.location.hash === '#favorites') {
            window.favoritesManager.renderView();
        }
    });
});
