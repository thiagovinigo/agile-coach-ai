import re

path = 'c:/Users/User/.antigravity/Agile Coach AI/app.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

debug_code = """
            // Toggle views
            views.forEach(view => {
                view.classList.remove('active');
            });
            const targetEl = document.getElementById(targetId);
            if(targetEl) {
                targetEl.classList.add('active');
                if (targetId === 'fluxo-ia-view') {
                    if (targetEl.innerHTML.trim() === '') {
                        alert("DIAGNÓSTICO: A div fluxo-ia-view está VAZIA! typeof initFluxoIaView = " + typeof initFluxoIaView);
                    } else {
                        alert("DIAGNÓSTICO: A div tem " + targetEl.innerHTML.length + " bytes de conteudo. Display=" + window.getComputedStyle(targetEl).display);
                    }
                }
            } else {
                alert("DIAGNÓSTICO: elemento targetId nao encontrado: " + targetId);
            }
"""

content = re.sub(
    r'// Toggle views\s*views\.forEach\(view => \{\s*view\.classList\.remove\(\'active\'\);\s*\}\);\s*document\.getElementById\(targetId\)\.classList\.add\(\'active\'\);',
    debug_code.strip(),
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected diagnostic into app.js")
