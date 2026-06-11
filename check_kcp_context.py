with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Visão KCP Expert')
print(text[max(0, idx-200):idx+100])
