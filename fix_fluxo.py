import re

path = 'c:/Users/User/.antigravity/Agile Coach AI/fluxo_ia.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace \` with `
content = content.replace('\\`', '`')
# Replace \${ with ${
content = content.replace('\\${', '${')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax in fluxo_ia.js")
