document.addEventListener('DOMContentLoaded', () => {
    initAuthUI();
});

function initAuthUI() {
    const authSection = document.getElementById('auth-section');
    if (!authSection) return;

    const token = localStorage.getItem('auth_token');
    let profile = null;
    
    try {
        const profileRaw = localStorage.getItem('user_profile');
        if (profileRaw) profile = JSON.parse(profileRaw);
    } catch(e) {}

    if (token) {
        // Usuário logado
        const userName = profile && profile.full_name ? profile.full_name : "Usuário";
        const email = profile && profile.email ? profile.email : "";

        authSection.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <div style="width: 32px; height: 32px; background: #3b82f6; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">
                    ${userName.charAt(0).toUpperCase()}
                </div>
                <div style="overflow: hidden;">
                    <div style="font-weight: 600; color: #323130; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${userName}</div>
                    <div style="font-size: 12px; color: #605e5c; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${email}</div>
                </div>
            </div>
            <button onclick="handleLogout()" style="width: 100%; background: #f3f2f1; border: 1px solid #edebe9; padding: 8px; border-radius: 6px; cursor: pointer; color: #323130; font-weight: 600; font-size: 13px; transition: background 0.2s;">
                Sair
            </button>
        `;
    } else {
        // Usuário deslogado
        authSection.innerHTML = `
            <div style="text-align: center;">
                <p style="font-size: 13px; color: #605e5c; margin-top: 0; margin-bottom: 10px;">Acesse para liberar recursos avançados</p>
                <button onclick="window.location.href='login.html'" style="width: 100%; background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 14px; transition: opacity 0.2s;">
                    Login / Cadastro
                </button>
            </div>
        `;
    }
}

function handleLogout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_profile');
    
    // Tenta avisar o Supabase, mas mesmo se falhar (sem setup), limpa local
    if (window.supabase) {
        window.supabase.auth.signOut().then(() => {
            window.location.reload();
        }).catch(() => {
            window.location.reload();
        });
    } else {
        window.location.reload();
    }
}
