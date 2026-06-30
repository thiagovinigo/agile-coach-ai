import re

path = 'c:/Users/User/.antigravity/Agile Coach AI/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Append cache buster
content = re.sub(r'<script src="fluxo_ia\.js(\?v=\d+)?"></script>', '<script src="fluxo_ia.js?v=3"></script>', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added cache buster to index.html")
