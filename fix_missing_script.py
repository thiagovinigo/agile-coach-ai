import re

path = 'c:/Users/User/.antigravity/Agile Coach AI/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure not to duplicate if it already exists
if 'fluxo_ia.js' not in content:
    content = re.sub(r'<script src="app\.js', '<script src="fluxo_ia.js?v=5"></script>\n    <script src="app.js', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected fluxo_ia.js tag!")
