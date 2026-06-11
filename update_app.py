with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# kb-kanban
k_kanban = text.find("if(viewId === 'kb-kanban')")
idx = text.find('s-kanban-praticas', k_kanban)
idx_end = text.find('}', idx) + 1
text = text[:idx_end] + ",\n                    { title: 'Papéis do Fluxo', parts: [ { id: 's-kanban-papeis', context: 'Kanban' } ] }" + text[idx_end:]

# kb-apresentacao
k_apres = text.find("if(viewId === 'kb-apresentacao')")
idx_s = text.find('sectionsToExtract = [', k_apres) + 21
text = text[:idx_s] + "\n                    { title: 'O que é Scrumban', parts: [ { id: 's-oque', context: 'Apresentação' } ] },\n                    { title: 'Scrum vs Kanban vs Scrumban', parts: [ { id: 's-vs', context: 'Apresentação' } ] }," + text[idx_s:]

idx_e = text.find('s-elite-cadencias', k_apres)
idx_end_e = text.find('}', idx_e) + 1
text = text[:idx_end_e] + ",\n                    { title: 'Refinamentos (Upstream)', parts: [ { id: 's-apresentacao-refinamentos', context: 'Apresentação' } ] }" + text[idx_end_e:]

# kb-lider
k_lider = text.find("if(viewId === 'kb-lider')")
idx_l = text.find('s-lider-resistencia', k_lider)
idx_end_l = text.find('}', idx_l) + 1
text = text[:idx_end_l] + ",\n                    { title: 'Cadências do Scrumban', parts: [ { id: 's-cadencias', context: 'Guia do Líder' } ] }" + text[idx_end_l:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated app.js')
