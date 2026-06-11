import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Isolar SDM e SRM em s-kanban-papeis
# O SDM e SRM estao dentro do s-kanban. Vou procurar a tag '<h2>Papéis Emergentes</h2>' ou os cards diretamente.
idx_sdm = text.find('📤 Service Delivery Manager (SDM)')
if idx_sdm != -1:
    # Eles estao dentro de div class="g2" ou algo parecido
    start_g2 = text.rfind('<div class="g2">', 0, idx_sdm)
    if start_g2 != -1:
        # Wrap the whole g2 block with s-kanban-papeis
        end_g2 = text.find('</div>', text.find('</div>', text.find('SRM')) + 6) + 6 # just approximate or just inject the div wrapper
        # Let's just insert a section header and wrapper before the g2 and close it after
        text = text[:start_g2] + '\n<div id="s-kanban-papeis" class="section">\n  <h2>👔 Papéis de Gestão (Kanban)</h2>\n' + text[start_g2:]
        # Find the end of this g2 block.
        idx_end_g2 = text.find('</div>', text.find('</div>', text.find('SRM', start_g2)) + 10) + 6
        text = text[:idx_end_g2] + '\n</div>\n' + text[idx_end_g2:]

# 2. Board de Elite: Remover Pronto para Replenishment
idx_replen = text.find('<div class="bcol" data-col="pronto-replen"')
if idx_replen != -1:
    # Find the preceding arrow
    start_arrow = text.rfind('<div style="display:flex;align-items:center;color:#94a3b8;font-size:16px;padding:0 2px;">›</div>', 0, idx_replen)
    # Find the end of the pronto-replen div
    end_replen = text.find('</div>', text.find('</div>', text.find('</div>', idx_replen) + 1) + 1) + 6 # Three inner divs
    # Find the real end by counting </div>
    count = 0
    pos = idx_replen
    while True:
        pos_open = text.find('<div', pos)
        pos_close = text.find('</div>', pos)
        if pos_close == -1: break
        if pos_open != -1 and pos_open < pos_close:
            count += 1
            pos = pos_open + 4
        else:
            count -= 1
            pos = pos_close + 6
            if count == 0:
                end_replen = pos
                break
    text = text[:start_arrow] + text[end_replen:]

# 3. Board de Elite: Substituir Seta UP->DOWN por Linha Vermelha
idx_arrow_block = text.find('<!-- SETA UP→DOWN -->')
if idx_arrow_block != -1:
    end_arrow_block = text.find('</div>', text.find('</div>', idx_arrow_block) + 1) + 6
    red_line = '''<!-- COMMITMENT POINT -->
      <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 12px;gap:8px;">
        <div style="flex:1;width:4px;background:#ef4444;border-radius:2px;box-shadow:0 0 8px rgba(239,68,68,0.5);"></div>
        <div style="font-size:11px;font-weight:900;color:#dc2626;text-align:center;writing-mode:vertical-lr;transform:rotate(180deg);letter-spacing:.1em;">COMMITMENT POINT</div>
        <div style="flex:1;width:4px;background:#ef4444;border-radius:2px;box-shadow:0 0 8px rgba(239,68,68,0.5);"></div>
      </div>'''
    # We need to find the exact end of the arrow block
    count = 0
    pos = text.find('<div', idx_arrow_block)
    while True:
        pos_open = text.find('<div', pos)
        pos_close = text.find('</div>', pos)
        if pos_close == -1: break
        if pos_open != -1 and pos_open < pos_close:
            count += 1
            pos = pos_open + 4
        else:
            count -= 1
            pos = pos_close + 6
            if count == 0:
                end_arrow_block = pos
                break
    text = text[:idx_arrow_block] + red_line + text[end_arrow_block:]

# 4. Ajustar min-width do board e remover linha da tabela
text = text.replace('min-width:1600px;', 'min-width:max-content;')

# Remover a row "Pronto p/ Replenishment" da tabela de Pull Rules
# The row ends before the row containing "Backlog"
idx_row_replen = text.find('<td style="padding:9px 12px;"><span style="font-weight:600;color:#1e40af;">Pronto p/ Replenishment</span></td>')
if idx_row_replen != -1:
    start_tr = text.rfind('<tr', 0, idx_row_replen)
    end_tr = text.find('</tr>', idx_row_replen) + 5
    text = text[:start_tr] + text[end_tr:]

# Adjust Backlog row origen
text = text.replace('<td style="padding:9px 12px;">Pronto p/ Replenishment</td>', '<td style="padding:9px 12px;">Aprovação PO</td>')


# 5. Adicionar a nova seção s-apresentacao-refinamentos no final do arquivo
refinamentos = """
<div id="s-apresentacao-refinamentos" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#db2777,#9d174d)">
    <div class="tag">REFINAMENTOS (UPSTREAM)</div>
    <h2>🚪 Check-in e Check-out do Discovery</h2>
    <p>As regras de ouro para um item atravessar o Refinamento Funcional e o Refinamento Técnico</p>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
    <!-- Refinamento Funcional -->
    <div style="background:#fdf2f8;border:2px solid #fbcfe8;border-radius:12px;padding:20px;">
      <h3 style="color:#be185d;margin-top:0;">1. Refinamento Funcional (O Quê)</h3>
      <p style="font-size:13px;color:#831843;">Liderado pelo Product Owner. O objetivo é fatiar a história (PBB) e definir exatamente o que o cliente quer, sem falar de código.</p>
      
      <div style="background:#fff;border-left:4px solid #db2777;padding:12px;margin-bottom:12px;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,0.05);">
        <strong style="color:#9d174d;font-size:12px;">📥 CHECK-IN (Para entrar):</strong>
        <ul class="chk" style="font-size:12px;margin:5px 0 0;color:#4c0519;">
          <li>Épico de negócio claro.</li>
          <li>WIP Limit da coluna respeitado.</li>
          <li>A dor do usuário está mapeada.</li>
        </ul>
      </div>

      <div style="background:#fff;border-left:4px solid #10b981;padding:12px;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,0.05);">
        <strong style="color:#065f46;font-size:12px;">📤 CHECK-OUT (Para sair):</strong>
        <ul class="chk" style="font-size:12px;margin:5px 0 0;color:#022c22;">
          <li>Fatiado verticalmente (menor pedaço de valor).</li>
          <li>Comportamentos desejados descritos (Ex: BDD - Dado, Quando, Então).</li>
          <li>Critérios de Aceite escritos.</li>
        </ul>
      </div>
    </div>

    <!-- Refinamento Técnico -->
    <div style="background:#eff6ff;border:2px solid #bfdbfe;border-radius:12px;padding:20px;">
      <h3 style="color:#1d4ed8;margin-top:0;">2. Refinamento Técnico (Como)</h3>
      <p style="font-size:13px;color:#1e3a8a;">Liderado pelo Dev Lead / Time Técnico. O objetivo é arquitetar a solução, prever impactos e quebrar em tarefas técnicas.</p>
      
      <div style="background:#fff;border-left:4px solid #3b82f6;padding:12px;margin-bottom:12px;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,0.05);">
        <strong style="color:#1e40af;font-size:12px;">📥 CHECK-IN (Para entrar):</strong>
        <ul class="chk" style="font-size:12px;margin:5px 0 0;color:#172554;">
          <li>Check-out Funcional 100% OK.</li>
          <li>PO disponível para tirar dúvidas.</li>
          <li>WIP Limit Técnico respeitado.</li>
        </ul>
      </div>

      <div style="background:#fff;border-left:4px solid #10b981;padding:12px;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,0.05);">
        <strong style="color:#065f46;font-size:12px;">📤 CHECK-OUT (Para sair):</strong>
        <ul class="chk" style="font-size:12px;margin:5px 0 0;color:#022c22;">
          <li>Impactos em banco, API e arquitetura mapeados.</li>
          <li>Tarefas de código (Sub-tasks) criadas.</li>
          <li>Tamanho máximo validado (Ex: cabe em &lt; 5 dias).</li>
          <li><strong>PRONTO PARA COMMITMENT POINT.</strong></li>
        </ul>
      </div>
    </div>
  </div>
</div>
"""
text = text + "\n" + refinamentos

with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done modifying scrumban_guia.html")
