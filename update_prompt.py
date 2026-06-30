import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_block = """    <div style="margin-bottom:20px;">
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
    </div>"""

new_block = """    <div style="margin-bottom:20px;">
      <strong style="color:#0f172a; font-size:15px; display:block; margin-bottom:5px;">Passos B e C: O Prompt Real (Production-Grade)</strong>
      <p style="font-size:13px; color:#475569; margin:0 0 10px 0;">Diferente de um chat comum (ChatGPT), agentes autônomos profissionais usam marcações XML, chamadas explícitas de ferramentas (Tool Calls) e regras de Governança estritas. Copie esta estrutura abaixo, ela é 100% real, testada e pronta para rodar no Kiro/Claude:</p>
      <div style="background:#1e293b; color:#f8fafc; padding:15px; border-radius:6px; font-family:monospace; font-size:12px; border-left:4px solid #a855f7; line-height: 1.5; overflow-x: auto; white-space: pre;"><span style="color:#a855f7;">&lt;role&gt;</span>
Você é o Agente Planner, especialista em Engenharia de Requisitos e BDD.
Sua missão é extrair a intenção bruta do Work Item do TFS e formatá-la em um PRD formal.
<span style="color:#a855f7;">&lt;/role&gt;</span>

<span style="color:#3b82f6;">&lt;instructions&gt;</span>
1. Use a ferramenta `azure-devops_get_work_item` do MCP para ler o ID recebido no gatilho.
2. Analise o conteúdo do campo `System.Description`.
3. Escreva um artefato no projeto chamado `PRD.md` contendo:
   - Resumo Executivo da Demanda
   - Critérios de Aceite (formato GIVEN / WHEN / THEN)
   - Edge Cases levantados
<span style="color:#3b82f6;">&lt;/instructions&gt;</span>

<span style="color:#ef4444;">&lt;governance_rules&gt;</span>
- NUNCA alucine regras de negócio. Se a descrição contiver menos de 20 palavras ou faltar informações vitais, PARE a geração do PRD.
- Em caso de parada por falta de info, use OBRIGATORIAMENTE a ferramenta `azure-devops_update_work_item` enviando este JSON Patch para travar o card:
  [ { "op": "add", "path": "/fields/System.Tags", "value": "DEP-Negocio" } ]
<span style="color:#ef4444;">&lt;/governance_rules&gt;</span>

<span style="color:#10b981;">&lt;mcp_trigger&gt;</span>
Se (e somente se) o arquivo `PRD.md` for gerado com sucesso e todos os critérios forem atendidos, você deve DEVOLVER O BASTÃO movendo o card. 
Use a ferramenta `azure-devops_update_work_item` com o seguinte payload PATCH:
[ { "op": "add", "path": "/fields/System.State", "value": "Aguardando Refinamento Técnico" } ]
<span style="color:#10b981;">&lt;/mcp_trigger&gt;</span></div>
    </div>"""

if old_block in html:
    new_html = html.replace(old_block, new_block)
    with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Injected real prompt successfully.")
else:
    print("Could not find the target block to replace.")
