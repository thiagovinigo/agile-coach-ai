# encoding: utf-8
import os

html_content = """
<!-- ===== SIMULADOR KIRO ===== -->
<div id="s-simulacao-kiro" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#000000,#111827)">
    <div class="tag" style="background:#3b82f6;">MÃO NA MASSA</div>
    <h2>💻 Simulador: Kiro no Board (Ciclo de Vida)</h2>
    <p>Acompanhe o passo a passo completo de um Work Item (PBI) cruzando as 10 colunas do nosso board, demonstrando exatamente a tela da IDE do Kiro e o comportamento no TFS via MCP.</p>
  </div>

  <p style="font-size:14px; color:#4b5563; margin-bottom:30px;">Cenário: A diretoria pediu a feature <strong>"Login via OTP (Token SMS)"</strong>. Veja como o fluxo autônomo opera etapa por etapa.</p>

"""

steps = [
    {
        "num": "1",
        "title": "New",
        "board_col": "New",
        "kiro_cmd": "# Ambiente Kiro Idle",
        "kiro_out": "<span style='color:#6b7280;'>// O PO acaba de criar a ideia bruta no TFS.</span>\n<span style='color:#6b7280;'>// O Kiro aguarda o item ser puxado para a esteira (Pull).</span>"
    },
    {
        "num": "2",
        "title": "Refinamento Funcional pela IA",
        "board_col": "Ref. Funcional (IA)",
        "kiro_cmd": "> kiro run ecc/blueprint --work-item=101",
        "kiro_out": "<span style='color:#3b82f6;'>[MCP TFS]</span> Lendo Descrição do Work Item 101...\n<span style='color:#a855f7;'>[Steering]</span> Aplicando Política: 'Gerar PRD e Critérios BDD'.\n<span style='color:#10b981;'>[Kiro]</span> Artefato 'PRD.md' gerado com sucesso.\n<span style='color:#3b82f6;'>[MCP TFS]</span> Atualizando <code>System.State</code> para 'Aguardando Refinamento Técnico' e anexando artefato."
    },
    {
        "num": "3",
        "title": "Aguardando Refinamento Técnico",
        "board_col": "Aguardando Ref. Técnico",
        "kiro_cmd": "# Fila de Transição",
        "kiro_out": "<span style='color:#6b7280;'>// O card está em uma fila (buffer). A IA terminou o trabalho funcional.</span>\n<span style='color:#6b7280;'>// O Kiro Architect (Skill de Spec) está aguardando capacidade para puxar o card.</span>"
    },
    {
        "num": "4",
        "title": "Em Refinamento pela IA (Técnico)",
        "board_col": "Em Ref. pela IA",
        "kiro_cmd": "> kiro run ecc/architecture-decision-records --work-item=101",
        "kiro_out": "<span style='color:#3b82f6;'>[MCP TFS]</span> Lendo PRD.md anexado no Work Item 101...\n<span style='color:#a855f7;'>[Steering]</span> Aplicando Política: 'Gerar Spec Técnica e ADR'.\n<span style='color:#10b981;'>[Kiro]</span> Artefato 'Design_Spec.md' (Contratos API, DB) gerado.\n<span style='color:#3b82f6;'>[MCP TFS]</span> Quebrando Work Item 101 em 3 sub-tasks (Backend, Frontend, Infra).\n<span style='color:#3b82f6;'>[MCP TFS]</span> Atualizando <code>System.State</code> para 'Aguardando Avaliação PO'."
    },
    {
        "num": "5",
        "title": "Aguardando Avaliação PO (Gate Humano)",
        "board_col": "Aguardando Avaliação PO",
        "kiro_cmd": "@Kiro, aprovar a especificação técnica e funcional.",
        "kiro_out": "<span style='color:#f59e0b;'>[Gate Humano]</span> O Kiro parou de processar. O Product Owner precisa ler os artefatos no TFS.\n<br>\n<span style='color:#a855f7;'>[Usuário]</span> Digita '/approve' no chat ou clica no botão Aprovar.\n<span style='color:#3b82f6;'>[MCP TFS]</span> O Kiro move o card para 'Em Desenvolvimento'."
    },
    {
        "num": "6",
        "title": "Em Desenvolvimento",
        "board_col": "Em Desenvolvimento",
        "kiro_cmd": "> kiro run ecc/tdd-workflow",
        "kiro_out": "<span style='color:#a855f7;'>[Steering]</span> Forçando workflow TDD.\n<span style='color:#ef4444;'>[Kiro Test]</span> Escrevendo <code>login.spec.ts</code> -> Executando -> <b>FALHA (Esperado)</b>.\n<span style='color:#10b981;'>[Kiro Code]</span> Implementando código em <code>login.ts</code> -> Executando -> <b>PASSOU</b>.\n<span style='color:#eab308;'>[Git]</span> Commit automático gerado: 'feat: add OTP login'.\n<span style='color:#3b82f6;'>[MCP TFS]</span> Atualizando <code>System.State</code> para 'Em Teste'."
    },
    {
        "num": "7",
        "title": "Em Teste",
        "board_col": "Em Teste",
        "kiro_cmd": "> kiro run ecc/security-review --diff",
        "kiro_out": "<span style='color:#10b981;'>[Kiro QA]</span> Lendo Critérios de Aceite do PRD...\n<span style='color:#10b981;'>[Kiro QA]</span> Executando testes End-to-End no diff recente.\n<span style='color:#a855f7;'>[Kiro Security]</span> Scan OWASP: Nenhuma injeção SQL detectada.\n<span style='color:#3b82f6;'>[MCP TFS]</span> Inserindo evidências de teste (Logs) no Test Plan do TFS.\n<span style='color:#3b82f6;'>[MCP TFS]</span> Atualizando <code>System.State</code> para 'Aguardando Avaliação PO'."
    },
    {
        "num": "8",
        "title": "Aguardando Avaliação PO (Final)",
        "board_col": "Aguardando Avaliação PO",
        "kiro_cmd": "@Kiro, feature testada. Pode prosseguir para release.",
        "kiro_out": "<span style='color:#f59e0b;'>[Gate Humano]</span> Kiro pausado.\nO PO analisa o relatório executivo e as evidências de QA.\n<br>\n<span style='color:#a855f7;'>[Usuário]</span> Digita '/approve-deploy'.\n<span style='color:#3b82f6;'>[MCP TFS]</span> Atualizando <code>System.State</code> para 'Liberado para Instalar'."
    },
    {
        "num": "9",
        "title": "Liberado para Instalar",
        "board_col": "Liberado p/ Instalar",
        "kiro_cmd": "# CI/CD Pipeline Agent",
        "kiro_out": "<span style='color:#10b981;'>[Azure Pipelines]</span> Gatilho detectado via Webhook.\n<span style='color:#6b7280;'>// Pipeline executando build e deploy no ambiente de Staging/Prod.</span>\n<span style='color:#3b82f6;'>[MCP TFS]</span> Ao sucesso do deploy, a pipeline move o estado para 'Done'."
    },
    {
        "num": "10",
        "title": "Done",
        "board_col": "Done",
        "kiro_cmd": "# Concluído",
        "kiro_out": "<span style='color:#10b981;'>✅ Ciclo de vida encerrado.</span>\n<span style='color:#6b7280;'>// O PBI foi refinado, especificado, codificado, testado e feito deploy num fluxo contínuo.</span>\n<span style='color:#6b7280;'>// Métricas de Lead Time registradas nativamente no TFS.</span>"
    }
]

for step in steps:
    html_content += f'''
  <div style="display:flex; margin-bottom:25px; border-radius:10px; overflow:hidden; box-shadow:0 4px 6px rgba(0,0,0,0.1); border:1px solid #d1d5db; flex-wrap:wrap;">
    
    <!-- Esquerda: Visão TFS Board -->
    <div style="flex:1; min-width:250px; background:#f8fafc; padding:20px; border-right:1px solid #e2e8f0;">
      <div style="font-size:11px; color:#64748b; font-weight:bold; letter-spacing:1px; margin-bottom:10px;">PASSO {step["num"]} • TFS BOARD</div>
      <strong style="color:#0f172a; font-size:16px; display:block; margin-bottom:15px;">{step["title"]}</strong>
      
      <!-- Simulação de Coluna Kanban -->
      <div style="background:#e2e8f0; border-radius:6px; padding:10px; min-height:100px;">
        <div style="font-size:12px; color:#475569; font-weight:bold; text-align:center; margin-bottom:10px;">Coluna: {step["board_col"]}</div>
        
        <!-- Card -->
        <div style="background:#ffffff; border-left:4px solid #3b82f6; padding:10px; border-radius:4px; box-shadow:0 1px 3px rgba(0,0,0,0.1); position:relative; animation: pulseCard 2s infinite;">
          <div style="font-size:10px; color:#94a3b8; margin-bottom:4px;">ID: #101</div>
          <strong style="font-size:13px; color:#1e293b;">Login via OTP (Token SMS)</strong>
          <div style="margin-top:8px; display:flex; gap:5px;">
            <span style="background:#dbeafe; color:#1e40af; font-size:9px; padding:2px 6px; border-radius:10px;">Security</span>
            <span style="background:#fef08a; color:#854d0e; font-size:9px; padding:2px 6px; border-radius:10px;">AI-Guided</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Direita: Visão IDE / Kiro -->
    <div style="flex:1.5; min-width:300px; background:#0f172a; padding:20px; display:flex; flex-direction:column;">
      <div style="font-size:11px; color:#94a3b8; font-weight:bold; letter-spacing:1px; margin-bottom:10px; display:flex; align-items:center; gap:8px;">
        <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#ef4444;"></span>
        <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#f59e0b;"></span>
        <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#10b981;"></span>
        <span style="margin-left:10px;">IDE / KIRO TERMINAL</span>
      </div>
      
      <div style="flex:1; background:#1e293b; border-radius:6px; padding:15px; font-family:'Courier New', Courier, monospace; font-size:13px; color:#e2e8f0; overflow-y:auto; border:1px solid #334155;">
        <div style="color:#fde047; margin-bottom:10px;">{step["kiro_cmd"]}</div>
        <div style="line-height:1.5;">
          {step["kiro_out"].replace(chr(10), "<br>")}
        </div>
      </div>
    </div>

  </div>
'''

html_content += """
  <style>
    @keyframes pulseCard {
      0% { box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
      50% { box-shadow: 0 0 8px rgba(59,130,246,0.6); }
      100% { box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    }
  </style>
</div>
<!-- ===== FIM SIMULADOR KIRO ===== -->
"""

# Append to scrumban_guia.html right before the end or after s-po-ia-dev
with open('c:/Users/User/.antigravity/Agile Coach AI/contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

# We'll inject it just after the s-po-ia-dev section finishes. 
# s-po-ia-dev ends exactly before <!-- ===== PO: REFINAMENTO EFICAZ ===== -->
target = "<!-- ===== PO: REFINAMENTO EFICAZ ===== -->"
if target in orig_html:
    new_html = orig_html.replace(target, html_content + "\n" + target)
    with open('c:/Users/User/.antigravity/Agile Coach AI/contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Injected Simulador Kiro successfully.")
else:
    print("Target not found for injecting simulator.")
