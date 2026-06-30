# encoding: utf-8
import os

html_content = """
<!-- ===== LABORATÓRIO SKILLS ===== -->
<div id="s-lab-skills" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#1e1b4b,#4c1d95)">
    <div class="tag" style="background:#8b5cf6;">LABORATÓRIO</div>
    <h2>🧪 Criando Skills e Operando em Lote</h2>
    <p>Conheça os Agentes do time de Engenharia, aprenda como criar o seu próprio Agente do zero (End-to-End) e veja como processar múltiplos itens de uma só vez puxando da fila.</p>
  </div>

  <!-- 1. Catálogo de Agentes -->
  <h3 style="margin:30px 0 15px; color:#1e293b; border-bottom:2px solid #8b5cf6; padding-bottom:8px;">👥 1. Catálogo de Agentes (O Time)</h3>
  <div style="display:flex; gap:15px; flex-wrap:wrap; margin-bottom:30px;">
    
    <div style="flex:1; min-width:200px; background:#fff; border:1px solid #d1d5db; border-radius:8px; padding:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05); text-align:center;">
      <div style="font-size:36px; margin-bottom:10px;">📋</div>
      <strong style="color:#111827; font-size:15px; display:block;">Agente Planner</strong>
      <span style="background:#f3f4f6; color:#4b5563; font-size:10px; padding:3px 8px; border-radius:12px;">Refinamento Funcional</span>
      <p style="font-size:12px; color:#475569; margin-top:10px; line-height:1.4;">Lê a demanda bruta, entende o escopo e escreve o PRD em formato BDD (Given/When/Then). Tagueia dependências de negócio.</p>
    </div>

    <div style="flex:1; min-width:200px; background:#fff; border:1px solid #d1d5db; border-radius:8px; padding:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05); text-align:center;">
      <div style="font-size:36px; margin-bottom:10px;">📐</div>
      <strong style="color:#111827; font-size:15px; display:block;">Agente Architect</strong>
      <span style="background:#f3f4f6; color:#4b5563; font-size:10px; padding:3px 8px; border-radius:12px;">Refinamento Técnico</span>
      <p style="font-size:12px; color:#475569; margin-top:10px; line-height:1.4;">Transforma o PRD em Spec Técnica. Define banco de dados, contratos de API e quebra o trabalho em subtarefas no TFS.</p>
    </div>

    <div style="flex:1; min-width:200px; background:#fff; border:1px solid #d1d5db; border-radius:8px; padding:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05); text-align:center;">
      <div style="font-size:36px; margin-bottom:10px;">🧑‍💻</div>
      <strong style="color:#111827; font-size:15px; display:block;">Agente TDD / Coder</strong>
      <span style="background:#f3f4f6; color:#4b5563; font-size:10px; padding:3px 8px; border-radius:12px;">Desenvolvimento</span>
      <p style="font-size:12px; color:#475569; margin-top:10px; line-height:1.4;">Codifica feature. Segue a regra rígida de primeiro escrever o teste (falhar), depois implementar (passar), e então criar o PR.</p>
    </div>

    <div style="flex:1; min-width:200px; background:#fff; border:1px solid #d1d5db; border-radius:8px; padding:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05); text-align:center;">
      <div style="font-size:36px; margin-bottom:10px;">🛡️</div>
      <strong style="color:#111827; font-size:15px; display:block;">Agente QA & Sec</strong>
      <span style="background:#f3f4f6; color:#4b5563; font-size:10px; padding:3px 8px; border-radius:12px;">Validação</span>
      <p style="font-size:12px; color:#475569; margin-top:10px; line-height:1.4;">Varre o código em busca de vulnerabilidades OWASP. Bate o código final contra os ACs originais do PRD. Gera evidência no Test Plan.</p>
    </div>

  </div>

  <!-- 2. Criando uma Skill End-to-End -->
  <h3 style="margin:30px 0 15px; color:#1e293b; border-bottom:2px solid #8b5cf6; padding-bottom:8px;">🛠️ 2. Como criar um Agente (End-to-End)</h3>
  <p style="font-size:14px; color:#475569; margin-bottom:20px;">Você não precisa "programar" Inteligência Artificial. Você só precisa <strong>escrever políticas claras</strong> usando Markdown. Veja como fabricamos uma Skill em 3 passos:</p>

  <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:20px; margin-bottom:30px;">
    
    <div style="margin-bottom:20px;">
      <strong style="color:#0f172a; font-size:15px; display:block; margin-bottom:5px;">Passo A: O Arquivo Base</strong>
      <p style="font-size:13px; color:#475569; margin:0 0 10px 0;">Crie um arquivo chamado <code>SKILL.md</code> dentro do seu repositório de agentes (ex: <code>ecc/skills/gerador-prd/SKILL.md</code>).</p>
    </div>

    <div style="margin-bottom:20px;">
      <strong style="color:#0f172a; font-size:15px; display:block; margin-bottom:5px;">Passo B: Escrevendo a Regra (O Prompt)</strong>
      <p style="font-size:13px; color:#475569; margin:0 0 10px 0;">Defina o Papel, a Tarefa e as Restrições (Governance). É aqui que você amarra a IA.</p>
      <div style="background:#1e293b; color:#f8fafc; padding:15px; border-radius:6px; font-family:monospace; font-size:12px; border-left:4px solid #a855f7;">
        <span style="color:#a855f7;"># Papel</span><br>
        Você é o Agente Planner especializado em refinamento de negócios para o Board.<br><br>
        <span style="color:#a855f7;"># Tarefa Principal</span><br>
        1. Leia a descrição crua do PBI usando a ferramenta `get_work_item`.<br>
        2. Escreva o PRD no formato BDD (Given/When/Then).<br><br>
        <span style="color:#a855f7;"># Restrição de Qualidade (Governance)</span><br>
        Nunca invente regras. Se a descrição do PO for muito curta (menos de 20 palavras), aplique a tag `DEP-Negocio` via `update_work_item` e PARE a execução.
      </div>
    </div>

    <div>
      <strong style="color:#0f172a; font-size:15px; display:block; margin-bottom:5px;">Passo C: Plugar no MCP (O Gatilho)</strong>
      <p style="font-size:13px; color:#475569; margin:0 0 10px 0;">Instrua a IA sobre qual botão "apertar" no TFS para mover o card para a próxima coluna.</p>
      <div style="background:#1e293b; color:#f8fafc; padding:15px; border-radius:6px; font-family:monospace; font-size:12px; border-left:4px solid #10b981;">
        <span style="color:#10b981;"># Ação de Sucesso (Fim de Esteira)</span><br>
        Se o PRD for gerado com sucesso, obrigatoriamente execute a ferramenta `update_work_item` enviando a operação de PATCH:<br>
        `"path": "/fields/System.State"` | `"value": "Aguardando Refinamento Técnico"`
      </div>
    </div>
  </div>

  <!-- 3. Executando Múltiplos Itens (Lote) -->
  <h3 style="margin:30px 0 15px; color:#1e293b; border-bottom:2px solid #8b5cf6; padding-bottom:8px;">🏭 3. Processamento em Lote (Limpando a Fila)</h3>
  <p style="font-size:14px; color:#475569; margin-bottom:20px;">No mundo real, o PO não coloca 1 item na coluna "New". Ele coloca 5 ou 10. Veja como o <strong>Agente de Ronda (Batch)</strong> acorda e puxa vários itens em paralelo.</p>

  <div style="display:flex; gap:15px; flex-wrap:wrap; margin-bottom:20px;">
    
    <!-- Esquerda: Fila Visual -->
    <div style="flex:1; min-width:250px; background:#fff7ed; padding:20px; border:1px solid #fdba74; border-radius:8px;">
      <strong style="color:#9a3412; font-size:15px; display:block; margin-bottom:10px;">Coluna: New (Entrada de Demandas)</strong>
      
      <div style="background:#fff; border-left:4px solid #9ca3af; padding:8px; margin-bottom:8px; font-size:12px; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
        <strong style="color:#374151;">#101</strong> - Login via OTP <span style="float:right; color:#a855f7;">[Na fila]</span>
      </div>
      <div style="background:#fff; border-left:4px solid #9ca3af; padding:8px; margin-bottom:8px; font-size:12px; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
        <strong style="color:#374151;">#102</strong> - Tela de Perfil <span style="float:right; color:#a855f7;">[Na fila]</span>
      </div>
      <div style="background:#fff; border-left:4px solid #9ca3af; padding:8px; margin-bottom:8px; font-size:12px; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
        <strong style="color:#374151;">#103</strong> - Esqueci Senha <span style="float:right; color:#a855f7;">[Na fila]</span>
      </div>
    </div>

    <!-- Direita: Terminal Paralelo -->
    <div style="flex:1.5; min-width:300px; background:#0f172a; padding:20px; border-radius:8px; border:1px solid #334155;">
      <strong style="color:#6ee7b7; font-size:13px; display:block; margin-bottom:10px; font-family:monospace;">> cron_job.sh --trigger-agent=planner --limit=5</strong>
      <div style="font-family:monospace; font-size:11px; color:#e2e8f0; line-height:1.6;">
        <span style="color:#60a5fa;">[MCP Query]</span> SELECT * FROM WorkItems WHERE State='New' LIMIT 5<br>
        <span style="color:#10b981;">[Found]</span> 3 itens retornados: [101, 102, 103].<br>
        <span style="color:#a855f7;">[Kiro Dispatcher]</span> Iniciando 3 threads paralelas...<br>
        <br>
        <span style="color:#9ca3af;">[Thread 1]</span> Card #101 processando PRD...<br>
        <span style="color:#9ca3af;">[Thread 2]</span> Card #102 processando PRD...<br>
        <span style="color:#9ca3af;">[Thread 3]</span> Card #103 processando PRD...<br>
        <br>
        <span style="color:#3b82f6;">[MCP Patch]</span> #101 Movido -> Ref. Funcional.<br>
        <span style="color:#ef4444;">[MCP Patch]</span> #102 REJEITADO (Regra Governance): Descrição vazia. Tag <b>DEP-Negocio</b> aplicada.<br>
        <span style="color:#3b82f6;">[MCP Patch]</span> #103 Movido -> Ref. Funcional.<br>
        <br>
        <span style="color:#10b981;">✅ Execução em Lote Finalizada (Tempo: 42s).</span>
      </div>
    </div>
  </div>
  
  <p style="font-size:13px; color:#475569; background:#f1f5f9; padding:15px; border-radius:6px; border-left:4px solid #cbd5e1;">
    <strong>O Poder da Escala:</strong> Em menos de 1 minuto, a IA limpou a coluna de entrada, empurrou dois itens mastigados com PRD pronto para o refinamento técnico, e bloqueou automaticamente um item mal especificado, cobrando o PO diretamente no card do TFS. Esse é o fluxo contínuo na prática!
  </p>

</div>
<!-- ===== FIM LABORATÓRIO SKILLS ===== -->
"""

# Append to scrumban_guia.html right before the end or after s-simulacao-kiro
with open('c:/Users/User/.antigravity/Agile Coach AI/contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

# We'll inject it just after the s-simulacao-kiro section finishes.
# s-simulacao-kiro ends exactly before <!-- ===== FIM SIMULADOR KIRO ===== -->
target = "<!-- ===== FIM SIMULADOR KIRO ===== -->"
if target in orig_html:
    new_html = orig_html.replace(target, target + "\n\n" + html_content)
    with open('c:/Users/User/.antigravity/Agile Coach AI/contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Injected Laboratorio Skills successfully.")
else:
    print("Target not found for injecting laboratorio.")
