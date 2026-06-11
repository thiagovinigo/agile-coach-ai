with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('SDM')
idx_div = text.rfind('<div id="', 0, idx)
print(text[idx_div:idx_div+100])
