import re
with open('contexto/scrumban_guia - Copia (7).html', 'r', encoding='utf-8') as f:
    html = f.read()

m1 = re.search(r'<div id="s-po-ia-dev".*?(<div id=|</main>)', html, re.DOTALL)
m2 = re.search(r'<div id="s-elite-board".*?(<div id=|</main>)', html, re.DOTALL)

with open('temp_agents.txt', 'w', encoding='utf-8') as out:
    out.write('--- s-po-ia-dev ---\n')
    out.write(m1.group(0) if m1 else 'Not found')
    out.write('\n\n--- s-elite-board ---\n')
    out.write(m2.group(0) if m2 else 'Not found')
