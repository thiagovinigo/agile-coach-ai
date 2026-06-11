with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('id="s-oque"')
end_idx = text.find('<div id="s-vs"', idx)
print('Length of s-oque:', end_idx - idx)
