import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

sections = list(re.finditer(r'<div id=\"([^\"]+)\" class=\"section\">', text))
print('Found', len(sections), 'sections.')

for i in range(len(sections)):
    start = sections[i].start()
    end = sections[i+1].start() if i+1 < len(sections) else len(text)
    chunk = text[start:end]
    opens = chunk.count('<div')
    closes = chunk.count('</div')
    if opens != closes:
        print('Mismatch in', sections[i].group(1), 'Open:', opens, 'Close:', closes)
