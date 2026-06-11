import re

new_content = """
    <!-- Visão KCP Expert -->
    <div style="margin-top:24px;border:2px solid #0284c7;border-radius:8px;overflow:hidden;background:#f0f9ff;">
      <div style="background:#0284c7;color:#fff;padding:10px 16px;font-weight:700;font-size:15px;display:flex;align-items:center;gap:8px;">
        <span>🥋</span> Visão Especialista KCP (Kanban Coaching Professional)
      </div>
      <div style="padding:16px;">
        <h4 style="color:#0369a1;margin:0 0 12px 0;font-size:16px;">O que é? (A Lente do Fluxo)</h4>
        <p style="font-size:14px;color:#334155;line-height:1.6;margin-bottom:12px;">
          No Kanban avançado aplicado ao Scrumban, se um problema ocorreu, <strong>o fluxo permitiu que ele ocorresse</strong>. Não buscamos culpados individuais ("quem atrasou?"), mas sim entender onde as regras do nosso sistema falharam. O objetivo primário é <strong>reduzir a variabilidade do fluxo para alcançar previsibilidade</strong>.
        </p>

        <h4 style="color:#0369a1;margin:0 0 12px 0;font-size:16px;">Como usar e Como fazer?</h4>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px;margin-bottom:16px;">
          <div style="background:#fff;border:1px solid #bae6fd;border-radius:8px;padding:12px;">
            <strong style="color:#0284c7;display:block;margin-bottom:6px;">1. Políticas Explícitas e Acordos</strong>
            <p style="font-size:13px;color:#475569;margin:0;">Como fazer: Documente regras claras (Definition of Ready, Definition of Done, critérios de puxar). Se a regra não está escrita, ela não existe e o fluxo sofrerá com variabilidade.</p>
          </div>
          <div style="background:#fff;border:1px solid #bae6fd;border-radius:8px;padding:12px;">
            <strong style="color:#0284c7;display:block;margin-bottom:6px;">2. Limites de WIP (Work in Progress)</strong>
            <p style="font-size:13px;color:#475569;margin:0;">Como fazer: Estabeleça o limite máximo de itens em paralelo por coluna ou por pessoa. É o mecanismo que força a regra suprema: <em>"Pare de começar e comece a terminar"</em>.</p>
          </div>
          <div style="background:#fff;border:1px solid #bae6fd;border-radius:8px;padding:12px;">
            <strong style="color:#0284c7;display:block;margin-bottom:6px;">3. Tratamento de Gargalos</strong>
            <p style="font-size:13px;color:#475569;margin:0;">Como fazer: Observe onde os itens se acumulam (filas invisíveis). Antes do gargalo, limite a entrada. No gargalo, adicione capacidade (pairing/swarming). Após o gargalo, puxe rapidamente.</p>
          </div>
        </div>

        <div style="background:#e0f2fe;border-left:4px solid #0284c7;padding:12px 16px;border-radius:4px;">
          <strong style="color:#0369a1;display:block;margin-bottom:6px;">Exemplo Real de Aplicação 💡</strong>
          <p style="font-size:14px;color:#0f172a;margin:0;line-height:1.5;">
            <strong>Cenário:</strong> Um time de engenharia percebeu que as entregas estavam demorando 20 dias (Lead Time alto) e o QA estava sobrecarregado (Gargalo). A primeira reação foi culpar o QA pela lentidão.<br><br>
            <strong>Ação do Agilista (KCP):</strong> Em vez de culpar, o time definiu uma <strong>política explícita</strong>: a coluna de "Code Review" tem um Limite de WIP igual a 3. Se atingir 3 itens, nenhum desenvolvedor pode puxar uma nova tarefa de <em>"To Do"</em> (<strong>parar de começar</strong>). Eles devem se juntar ao QA para testar, fazer swarm ou revisar o que está parado (<strong>começar a terminar</strong>). O Lead Time caiu para 8 dias e a variabilidade diminuiu porque o fluxo impôs a colaboração.
          </p>
        </div>
      </div>
    </div>
"""

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

# We need to insert `new_content` at the end of `s-oque`, right before the next `class="section"` div.
idx = text.find('id="s-oque"')
if idx != -1:
    end_idx = text.find('<div id="', idx + 50) # find the start of the next section
    if end_idx != -1:
        # insert before end_idx
        modified_text = text[:end_idx] + new_content + "\n" + text[end_idx:]
        with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
            f.write(modified_text)
        print("Successfully updated s-oque")
    else:
        print("Could not find next section")
else:
    print("Could not find s-oque")
