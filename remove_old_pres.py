with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="s-apresentacao-fluxo"')
if idx != -1:
    idx_comment = text.rfind('<!-- ==========================================', 0, idx)
    if idx_comment != -1 and (idx - idx_comment) < 200:
        idx = idx_comment
    new_text = text[:idx]
    with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(new_text.strip() + '\n')
    print('Old presentation content removed.')
