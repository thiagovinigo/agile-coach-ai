with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="s-elite-board"')
end = text.find('id="s-elite-politicas"', start)
if start != -1 and end != -1:
    with open('elite_board_dump.txt', 'w', encoding='utf-8') as f:
        f.write(text[start:end])
    print('Dumped s-elite-board.')
