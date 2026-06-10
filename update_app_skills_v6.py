import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Add dependencies rendering logic
# We need to insert a block of HTML if skill.dependencies && skill.dependencies.length > 0

dep_html = """
                    ${skill.dependencies && skill.dependencies.length > 0 ? `
                    <div style="background:#f0f8ff; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #0078d4; margin-bottom: 2rem;">
                        <h4 style="margin-top:0; margin-bottom:1rem; font-size:1.1rem; color:#0078d4; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;">🔗 Skills Vinculadas (Sub-Skills)</h4>
                        <p style="font-size:0.95rem; color:#4a5568; margin-bottom:1rem;">Esta skill possui conexões diretas ou invoca o conhecimento das seguintes skills:</p>
                        <div>
                            ${skill.dependencies.map(d => `<span class="tag" style="display:inline-block; background:rgba(0,120,212,.12); border:1px solid rgba(0,120,212,.3); padding:.3em .8em; border-radius:4px; font-size:.85rem; color:#0078d4; margin-right:5px; margin-bottom:5px; font-weight:bold;">${d}</span>`).join('')}
                        </div>
                    </div>
                    ` : ''}
"""

if "🔗 Skills Vinculadas" not in app_js:
    # Insert it right before "Como Instalar"
    app_js = app_js.replace("<h4 style=\"margin-top:1.5rem; margin-bottom:0.8rem; font-size:1rem; color:#718096; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;\">🛠️ Como Instalar (Claude Code):</h4>", dep_html + "\n                    <h4 style=\"margin-top:1.5rem; margin-bottom:0.8rem; font-size:1rem; color:#718096; text-transform:uppercase; font-weight:700; letter-spacing:0.05em;\">🛠️ Como Instalar (Claude Code):</h4>")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
