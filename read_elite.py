with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

out = open('elite_output.txt', 'w', encoding='utf-8')

def print_section(sid):
    idx = text.find('id="' + sid + '"')
    if idx == -1: return
    out.write('--- ' + sid + ' ---\n')
    out.write(text[idx:idx+2500] + '\n')

print_section('s-elite-board')
print_section('s-elite-politicas')
print_section('s-elite-cadencias')
print_section('s-elite-flow')
out.close()
