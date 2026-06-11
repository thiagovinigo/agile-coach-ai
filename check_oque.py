with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('id="s-oque"')
end = text.find('class="section"', idx+50)
print(text[idx:end])
