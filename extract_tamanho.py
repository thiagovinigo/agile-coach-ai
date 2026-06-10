import re
with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('<div id="s-elite-tamanho"')
if idx != -1:
    end = code.find('<div id="s-', idx + 10)
    with open('debug_tamanho.html', 'w', encoding='utf-8') as out:
        out.write(code[idx:end])
