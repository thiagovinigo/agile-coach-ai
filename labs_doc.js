function initLabsView() {
    const container = document.getElementById('labs-view');
    if (!container) return;
    
    // labsData is globally available from labs_data.js
    if (typeof labsData === 'undefined') {
        container.innerHTML = '<div style="padding:20px;color:red;">Erro: labs_data.js não carregado. Verifique o index.html.</div>';
        return;
    }

    let tabsHtml = '';
    let contentHtml = '';

    labsData.forEach((phase, index) => {
        const isActive = index === 0 ? 'active' : '';
        const displayStyle = index === 0 ? 'block' : 'none';
        
        tabsHtml += `<button class="lab-tab-btn ${isActive}" onclick="switchLabTab('${phase.id}', this)">${phase.icon} ${phase.title}</button>`;
        
        let labsHtml = '';
        phase.labs.forEach((lab, labIndex) => {
            const labNumber = (index * 10) + (labIndex + 1);
            labsHtml += `
            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #3b82f6;">
                    <span style="font-size:24px;">${phase.icon}</span> 
                    <h3>Lab ${labNumber}: ${lab[0]}</h3>
                </div>
                <div class="lab-content">
                    <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                        <strong style="color: #166534; display: flex; align-items: center; gap: 8px;">🎯 O Que É</strong>
                        <p style="margin: 5px 0 0 0; color: #166534;">${lab[1]}</p>
                    </div>
                    <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                        <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;">💡 Valor de Negócio</strong>
                        <p style="margin: 5px 0 0 0; color: #92400e;">${lab[2]}</p>
                    </div>
                    <h4 style="color: #3b82f6; margin-bottom: 15px;">🛠️ Como Fazer</h4>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>Terminal / Prompt</strong>
                            <div class="lab-code">
${lab[3]}
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;
        });

        contentHtml += `<div id="${phase.id}" class="lab-tab-content ${isActive}" style="display: ${displayStyle};">${labsHtml}</div>`;
    });

    container.innerHTML = `
        <style>
            .lab-card {
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                overflow: hidden;
            }
            .lab-header {
                padding: 20px 25px;
                background: #f8fafc;
                border-bottom: 2px solid #3b82f6;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .lab-header h3 {
                margin: 0;
                font-size: 18px;
                color: #0f172a;
            }
            .lab-content {
                padding: 25px;
                color: #475569;
                font-size: 14.5px;
                line-height: 1.7;
            }
            .lab-code {
                background: #0f172a;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                font-family: 'Courier New', Courier, monospace;
                font-size: 13px;
                line-height: 1.6;
                overflow-x: auto;
                margin: 20px 0;
                border-left: 4px solid #3b82f6;
                white-space: pre;
            }
            .lab-step {
                display: flex;
                align-items: flex-start;
                gap: 15px;
                margin-bottom: 20px;
            }
            .lab-step-number {
                background: #3b82f6;
                color: #fff;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            }
            .lab-tabs {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
                border-bottom: 2px solid #e2e8f0;
                padding-bottom: 10px;
                overflow-x: auto;
            }
            .lab-tab-btn {
                background: #f1f5f9;
                border: 1px solid #cbd5e1;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                color: #475569;
                transition: all 0.2s;
                white-space: nowrap;
            }
            .lab-tab-btn:hover {
                background: #e2e8f0;
            }
            .lab-tab-btn.active {
                background: #3b82f6;
                color: #fff;
                border-color: #2563eb;
            }
            .lab-tab-content {
                display: none;
            }
            .lab-tab-content.active {
                display: block;
            }
        </style>

        <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #000000);">
            <div class="tag" style="background:#3b82f6;">BOOTCAMP "10.000 HORAS"</div>
            <h2>🔬 100 Laboratórios: Squad 100% Autônoma</h2>
            <p style="margin-top:10px;">A jornada completa de uma equipe que desenvolve e refina tudo via IA, navegando por 10 fases do Discovery ao Delivery usando o Model Context Protocol (MCP).</p>
        </div>

        <div class="lab-tabs" id="lab-tabs">
            ${tabsHtml}
        </div>

        ${contentHtml}
    `;
}

window.initLabsView = initLabsView;
window.switchLabTab = function(tabId, btnElement) {
    document.querySelectorAll('.lab-tab-content').forEach(el => {
        el.classList.remove('active');
        el.style.display = 'none';
    });
    document.querySelectorAll('.lab-tab-btn').forEach(btn => btn.classList.remove('active'));
    
    const targetTab = document.getElementById(tabId);
    if (targetTab) {
        targetTab.classList.add('active');
        targetTab.style.display = 'block';
    }
    if (btnElement) btnElement.classList.add('active');
};
