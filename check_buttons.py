with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="s-po-ia-dev"')
end_idx = text.find('class="section"', idx+50)
chunk = text[idx:end_idx]

import re
buttons = re.findall(r'<button[^>]*>.*?</button>', chunk, re.DOTALL)
for i, b in enumerate(buttons):
    print(i, b.encode('ascii', 'ignore').decode('ascii'))
