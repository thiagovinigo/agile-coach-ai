with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()
print('Occurrences of id="s-oque":', text.count('id="s-oque"'))
