import re

index_path = 'c:/Users/User/.antigravity/Agile Coach AI/index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add sidebar link
new_nav_item = """                    <div class="nav-group-title">Portal Principal</div>
                    <a href="#fluxo-ia" class="nav-item" data-target="fluxo-ia-view">
                        <span class="icon">🚀</span> Fluxo com IA
                    </a>"""

content = content.replace('<div class="nav-group-title">Portal Principal</div>', new_nav_item)

# 2. Add view container
new_view = """                <!-- Views -->
                <div id="fluxo-ia-view" class="view"></div>"""

content = content.replace('<!-- Views -->', new_view)

# 3. Add script tag at the end
script_tag = """    <script src="fluxo_ia.js"></script>
    <script src="app.js"></script>"""

content = content.replace('<script src="app.js"></script>', script_tag)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html")
