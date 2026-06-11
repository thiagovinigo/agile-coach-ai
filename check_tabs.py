with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('id="s-po-quebrando"')
end_idx = text.find('class="section"', idx+50)
with open('tabs_output.txt', 'w', encoding='utf-8') as f:
    f.write(text[idx:end_idx])
