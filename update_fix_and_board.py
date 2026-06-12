import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the broken tag first
html = html.replace('<!-- 14. EVOLUA EXPERIMENTALMENTE -->tyle="margin:20px 0 12px">🧪 Evolua Experimentalmente: Toda mudança é uma hipótese</h3>',
                    '<!-- 14. EVOLUA EXPERIMENTALMENTE -->\n  <h3 style="margin:20px 0 12px">🧪 Evolua Experimentalmente: Toda mudança é uma hipótese</h3>')

# The new board example HTML
new_board_example = """
    <div style="background:#e9d5ff; border:1px solid #c084fc; border-radius:8px; padding:15px; margin-top:20px; box-shadow:0 2px 5px rgba(0,0,0,0.05);">
      <strong style="color:#6b21a8; font-size:15px; display:block; margin-bottom:5px;">🧩 Simulação Prática: Onde o fluxo trava?</strong>
      <p style="font-size:13px; color:#4c1d95; margin-top:0; margin-bottom:15px;">Vamos aplicar a dança dos gargalos em um cenário visual real. Veja este board onde tudo está acontecendo ao mesmo tempo:</p>
      
      <div style="display:flex; margin-top:10px; font-size:11px; text-align:center; color:white; font-weight:bold;">
        <div style="flex:1; background:#ea580c; padding:8px; border-radius:4px 0 0 4px;">UPSTREAM (Descoberta)</div>
        <div style="flex:3; background:#0f766e; padding:8px; border-radius:0 4px 4px 0;">DOWNSTREAM (Entrega)</div>
      </div>
      
      <div style="display:flex; gap:5px; margin-top:10px; overflow-x:auto;">
        <!-- Upstream -->
        <div style="flex:1; min-width:110px; background:#fff; border:1px solid #d1d5db; border-radius:4px; padding:5px;">
          <div style="text-align:center; font-size:10px; color:#6b7280; margin-bottom:5px;">Pronto p/ dev <br> 4</div>
          <div style="border-left:3px solid #ea580c; padding:4px; font-size:10px; background:#f3f4f6; margin-bottom:4px;">FEATLogin social</div>
          <div style="border-left:3px solid #ea580c; padding:4px; font-size:10px; background:#f3f4f6; margin-bottom:4px;">FIXLGPD</div>
        </div>
        <!-- Downstream -->
        <div style="flex:1; min-width:110px; background:#fff; border:2px solid #b91c1c; border-radius:4px; padding:5px; box-shadow:0 0 5px rgba(220,38,38,0.5);">
          <div style="text-align:center; font-size:10px; color:#b91c1c; font-weight:bold; margin-bottom:5px;">Dev · fazendo <br> (Bloqueado)</div>
          <div style="border-left:3px solid #b91c1c; padding:4px; font-size:10px; background:#fee2e2; margin-bottom:4px; border:1px solid #ef4444; color:#7f1d1d; font-weight:bold;">⛔ EXPBug Layout</div>
          <div style="border-left:3px solid #0f766e; padding:4px; font-size:10px; background:#f3f4f6; margin-bottom:4px;">FEATAPI pagto</div>
        </div>
        <div style="flex:1; min-width:110px; background:#fff; border:1px dashed #d1d5db; border-radius:4px; padding:5px; background:#f9fafb;">
          <div style="text-align:center; font-size:10px; color:#ca8a04; font-weight:bold; margin-bottom:5px;">Dev · feito <br> FILA CRESCENDO</div>
          <div style="border-left:3px solid #0f766e; padding:4px; font-size:10px; background:#fff; margin-bottom:4px; box-shadow:0 1px 2px rgba(0,0,0,0.1);">FEATDashboard</div>
          <div style="border-left:3px solid #0f766e; padding:4px; font-size:10px; background:#fff; margin-bottom:4px; box-shadow:0 1px 2px rgba(0,0,0,0.1);">FEATFiltros</div>
          <div style="border-left:3px solid #0f766e; padding:4px; font-size:10px; background:#fff; margin-bottom:4px; box-shadow:0 1px 2px rgba(0,0,0,0.1);">FEATExport PDF</div>
        </div>
        <div style="flex:1; min-width:110px; background:#fff; border:2px solid #ca8a04; border-radius:4px; padding:5px;">
          <div style="text-align:center; font-size:10px; color:#ca8a04; font-weight:bold; margin-bottom:5px;">QA <br> GARGALO (WIP Cheio)</div>
          <div style="border-left:3px solid #f59e0b; padding:4px; font-size:10px; background:#fef3c7; margin-bottom:4px; border:1px solid #f59e0b; color:#92400e; font-weight:bold;">⏳ Pendência API</div>
          <div style="border-left:3px solid #0f766e; padding:4px; font-size:10px; background:#f3f4f6;">FEATNotif. push</div>
        </div>
        <div style="flex:1; min-width:110px; background:#fff; border:1px solid #d1d5db; border-radius:4px; padding:5px; opacity:0.6;">
          <div style="text-align:center; font-size:10px; color:#6b7280; margin-bottom:5px;">Entregue <br> OCIOSO (Fome)</div>
        </div>
      </div>
      
      <div style="display:flex; flex-direction:column; gap:12px; margin-top:20px; font-size:12px; color:#4c1d95;">
        <div style="background:white; padding:15px; border-radius:6px; border-left:4px solid #b91c1c;">
          <strong style="font-size:13px; color:#7f1d1d; display:block; margin-bottom:5px;">1. Impedimento (Bloqueio Interno)</strong> 
          <p style="margin:0; color:#374151;">O card vermelho em DEV está travado por um erro de banco de dados do próprio time (a máquina local não sobe).</p>
          <strong style="color:#b91c1c; display:block; margin-top:5px;">Solução (Trabalho Tático):</strong> Swarming (ataque em bando) técnico. O desenvolvedor levanta a mão na daily e pede pair programming imediatamente com o tech lead ou devops. A prioridade máxima do time passa a ser destravar esse item interno.
        </div>
        <div style="background:white; padding:15px; border-radius:6px; border-left:4px solid #f59e0b;">
          <strong style="font-size:13px; color:#92400e; display:block; margin-bottom:5px;">2. Dependência (Pendência Externa)</strong> 
          <p style="margin:0; color:#374151;">O card amarelo em QA precisa que a equipe de infra do cliente libere uma porta no firewall para testar a notificação push.</p>
          <strong style="color:#f59e0b; display:block; margin-top:5px;">Solução (Trabalho Tático):</strong> O SM/Agile Coach ou PO assume o papel de "Dono da Resolução" e vai acionar as instâncias políticas para cobrar o cliente ativamente (e registra isso no cartão). O WIP Limit impede que o QA puxe novos cards enquanto o ambiente não estiver livre, forçando a dor da espera ficar visível.
        </div>
        <div style="background:white; padding:15px; border-radius:6px; border-left:4px solid #ca8a04;">
          <strong style="font-size:13px; color:#854d0e; display:block; margin-bottom:5px;">3. Gargalo Identificado (A Fila Crescente)</strong> 
          <p style="margin:0; color:#374151;">Observe como a coluna ANTES do QA ("Dev Feito") tem 3 itens esperando, e a coluna DEPOIS do QA ("Entregue") está vazia (fome de fluxo).</p>
          <strong style="color:#ca8a04; display:block; margin-top:5px;">Solução (Trabalho Tático):</strong> Para aliviar o gargalo, os Devs <strong>não puxam</strong> "FEATLogin social" da coluna Pronto p/ dev. Pelo contrário: eles param de programar e vão testar o "FEATDashboard", o "FEATFiltros" ou criar testes unitários para ajudar a vazão do QA, aliviando a restrição.
        </div>
      </div>
    </div>
"""

# Insert new_board_example right before "<!-- 14. EVOLUA EXPERIMENTALMENTE -->"
idx_evolua = html.find('<!-- 14. EVOLUA EXPERIMENTALMENTE -->')
if idx_evolua != -1:
    html = html[:idx_evolua] + new_board_example + "\n  " + html[idx_evolua:]
    with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed formatting and added simulated board successfully.")
else:
    print("Could not find the EVOLUA EXPERIMENTALMENTE tag after fixing.")
