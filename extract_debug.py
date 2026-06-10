import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    code = f.read()

start = code.find('<div id="s-fac-replenishment"')
end = code.find('<!-- ===== FACILITADOR EM CAMPO: WIP ESTOUROU ===== -->')

with open('debug.html', 'w', encoding='utf-8') as f:
    f.write(code[start:end])
