with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('<div id="s-cadencias"')
if idx != -1:
    end = code.find('<!-- =====', idx)
    with open('debug_cadencias.html', 'w', encoding='utf-8') as out:
        out.write(code[idx:end])
