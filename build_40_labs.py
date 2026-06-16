import html
from labs_data_kiro import kiro_basics, kiro_tfs
from labs_data_claude import claude_basics, claude_tfs

def render_lab(lab):
    html_out = f'''
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #3b82f6;">
                <span style="font-size:24px;">{lab["icon"]}</span> 
                <h3>Lab {lab["id"]}: {lab["title"]}</h3>
            </div>
            <div class="lab-content">
                <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #166534; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🎯</span> O Que É</strong>
                    <p style="margin: 5px 0 0 0; color: #166534;">{lab["oque"]}</p>
                </div>
                <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                    <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">💡</span> Por Que Usar (Valor de Negócio)</strong>
                    <p style="margin: 5px 0 0 0; color: #92400e;">{lab["porque"]}</p>
                </div>
                <h4 style="color: #3b82f6; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; display: flex; align-items: center; gap: 8px;"><span style="font-size:18px;">🛠️</span> Como Fazer</h4>
'''
    for idx, step in enumerate(lab["steps"]):
        code_escaped = html.escape(step["code"])
        # Escape dollar signs to prevent JS template literal interpolation ReferenceError
        code_escaped = code_escaped.replace("$", "\\$")
        
        html_out += f'''
                <div class="lab-step">
                    <div class="lab-step-number">{idx+1}</div>
                    <div style="width: 100%;">
                        <strong>{step["title"]}</strong>
                        <p>{step["text"]}</p>
                        <div class="lab-code">
{code_escaped}
                        </div>
                    </div>
                </div>
'''
    html_out += '''
            </div>
        </div>
'''
    return html_out

def build_category(labs_list):
    res = ""
    for lab in labs_list:
        res += render_lab(lab)
    return res

html_content = f'''
function initLabsView() {{
    const container = document.getElementById('labs-view');
    if (!container) return;

    container.innerHTML = `
        <style>
            .lab-card {{
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                overflow: hidden;
            }}
            .lab-header {{
                padding: 20px 25px;
                background: #f8fafc;
                border-bottom: 2px solid #3b82f6;
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .lab-header h3 {{
                margin: 0;
                font-size: 18px;
                color: #0f172a;
            }}
            .lab-content {{
                padding: 25px;
                color: #475569;
                font-size: 14.5px;
                line-height: 1.7;
            }}
            .lab-code {{
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
            }}
            .lab-step {{
                display: flex;
                align-items: flex-start;
                gap: 15px;
                margin-bottom: 20px;
            }}
            .lab-step-number {{
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
            }}
            
            /* Tabs CSS */
            .lab-tabs {{
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
                border-bottom: 2px solid #e2e8f0;
                padding-bottom: 10px;
                overflow-x: auto;
            }}
            .lab-tab-btn {{
                background: #f1f5f9;
                border: 1px solid #cbd5e1;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                color: #475569;
                transition: all 0.2s;
                white-space: nowrap;
            }}
            .lab-tab-btn:hover {{
                background: #e2e8f0;
            }}
            .lab-tab-btn.active {{
                background: #3b82f6;
                color: #fff;
                border-color: #2563eb;
            }}
            .lab-tab-content {{
                display: none;
            }}
            .lab-tab-content.active {{
                display: block;
            }}
        </style>

        <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #000000);">
            <div class="tag" style="background:#3b82f6;">BOOTCAMP "10.000 HORAS"</div>
            <h2>🔬 40 Laboratórios Práticos (Discovery to Delivery)</h2>
            <p style="margin-top:10px;">Aqui o código ganha vida. Abaixo estão catalogados 40 laboratórios detalhados dividindo o ciclo de vida da Engenharia de Software em duas IAs complementares: <strong>Kiro (O Orquestrador)</strong> e <strong>Claude Code (O Worker de Terminal)</strong>. Selecione a aba desejada abaixo.</p>
        </div>

        <div class="lab-tabs" id="lab-tabs">
            <button class="lab-tab-btn active" onclick="switchLabTab('tab-kiro-basic', this)">⚙️ Kiro: Básicos (1-10)</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-kiro-tfs', this)">⚙️ Kiro: TFS Lifecycle (11-20)</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-claude-basic', this)">💻 Claude: Básicos (1-10)</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-claude-tfs', this)">💻 Claude: TFS Lifecycle (11-20)</button>
        </div>

        <div id="tab-kiro-basic" class="lab-tab-content active">
            {build_category(kiro_basics)}
        </div>

        <div id="tab-kiro-tfs" class="lab-tab-content">
            {build_category(kiro_tfs)}
        </div>

        <div id="tab-claude-basic" class="lab-tab-content">
            {build_category(claude_basics)}
        </div>

        <div id="tab-claude-tfs" class="lab-tab-content">
            {build_category(claude_tfs)}
        </div>

    `;
}}

window.initLabsView = initLabsView;
window.switchLabTab = function(tabId, btnElement) {{
    document.querySelectorAll('.lab-tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.lab-tab-btn').forEach(btn => btn.classList.remove('active'));
    
    const targetTab = document.getElementById(tabId);
    if (targetTab) targetTab.classList.add('active');
    if (btnElement) btnElement.classList.add('active');
}};
'''

with open('labs_doc.js', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("labs_doc.js rebuilt with 40 labs.")
