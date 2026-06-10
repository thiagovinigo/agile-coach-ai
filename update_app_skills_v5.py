import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Add a header explaining the difference before the layout is created
explanation_header = """
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.style.marginBottom = '20px';
    introHeader.innerHTML = `
        <h2 style="margin-top:0; color:#0078d4; margin-bottom:10px;">Flowgrammers Skills vs. AI Agents</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            <strong>Qual a diferença?</strong> Os <a href="#agents" style="color:#0078d4; text-decoration:none;">AI Agents</a> (no menu acima) são simuladores interativos embutidos <em>neste portal</em> (você clica e digita aqui). Já as <strong>Flowgrammers Skills</strong> são <em>manuais de instrução avançados</em> (arquivos <code>.md</code>). Você deve baixar esses arquivos e colocá-los no seu próprio ambiente local (Cursor, Windsurf, Claude Code) para que sua Inteligência Artificial aja como o especialista descrito.
        </p>
    `;
    container.appendChild(introHeader);
"""

if "Qual a diferença?" not in app_js:
    app_js = app_js.replace("container.appendChild(layout);", "container.appendChild(introHeader);\n    container.appendChild(layout);")
    app_js = app_js.replace("const layout = document.createElement('div');", explanation_header + "\n    const layout = document.createElement('div');")

# Add Download Button into the card HTML
download_html = """
                    <div style="display: flex; gap: 10px; margin-bottom: 2rem;">
                        <a href="flowgrammers-skills-main/flowgrammers-skills-main/${skill.path}" download="${skill.id}.md" style="display:inline-block; background-color:#0078d4; color:#fff; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:1rem; box-shadow:0 2px 4px rgba(0,0,0,0.1); transition: background 0.2s;">
                            ⬇️ Baixar Arquivo da Skill
                        </a>
                        <a href="flowgrammers-skills-main/flowgrammers-skills-main/${skill.path}" target="_blank" style="display:inline-block; background-color:#f3f2f1; color:#323130; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; border: 1px solid #edebe9; font-size:1rem; transition: background 0.2s;">
                            👀 Ver Arquivo
                        </a>
                    </div>
"""

# Find where to insert it: maybe right after the description
if "⬇️ Baixar Arquivo da Skill" not in app_js:
    app_js = app_js.replace("<div style=\"background:#f7fafc;", download_html + "\n                    <div style=\"background:#f7fafc;")

# Cache bust string update just in case (optional, we can just replace v=5 with v=6 in the html directly)
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
