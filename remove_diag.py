import re

path = 'c:/Users/User/.antigravity/Agile Coach AI/app.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the diagnostic alert logic
# We injected it inside the toggle logic.
# The injected block looks like:
# const targetEl = document.getElementById(targetId);
# if(targetEl) {
#     targetEl.classList.add('active');
#     if (targetId === 'fluxo-ia-view') {
#         if (targetEl.innerHTML.trim() === '') { ... alert(...) ... }
#     }
# } else { alert(...) }

new_code = """
            const targetEl = document.getElementById(targetId);
            if(targetEl) {
                targetEl.classList.add('active');
            }
"""

content = re.sub(
    r'const targetEl = document\.getElementById\(targetId\);\s*if\(targetEl\)\s*\{\s*targetEl\.classList\.add\(\'active\'\);\s*if\s*\(targetId === \'fluxo-ia-view\'\)[\s\S]*?\} else \{\s*alert\("DIAGNÓSTICO: elemento targetId nao encontrado: " \+ targetId\);\s*\}',
    new_code.strip(),
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed diagnostic from app.js")
