import os

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<div id="tfs-view" class="view"></div>', '<div id="tfs-view" class="view kb-view"><div class="kb-content-container" id="kb-tfs"></div></div>')
html = html.replace('<script src="tfs_expert.js?v=9"></script>', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

if "viewId === 'kb-tfs'" not in app_js:
    tfs_logic = """            } else if(viewId === 'kb-tfs') {
                sectionsToExtract = [
                    { title: 'Hierarquia e Links', parts: [ { id: 's-tfs-links', context: 'Especialista TFS' } ] },
                    { title: 'Configuração de Boards Kanban', parts: [ { id: 's-tfs-boards', context: 'Especialista TFS' } ] },
                    { title: 'Migração TFS para Cloud', parts: [ { id: 's-tfs-cloud', context: 'Especialista TFS' } ] }
                ];
"""
    app_js = app_js.replace("            } else if(viewId === 'kb-agil') {", tfs_logic + "            } else if(viewId === 'kb-agil') {")
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)

# 3. Add content to contexto/scrumban_guia.html
with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    guia = f.read()

tfs_content = """
<!-- ========================================== -->
<!-- ESPECIALISTA TFS                           -->
<!-- ========================================== -->

<section id="s-tfs-links">
  <div class="content-block">
    <div class="subtitle">O que é?</div>
    <p>O TFS (Team Foundation Server) e o Azure DevOps Server possuem um sistema rígido de vínculos (Links) entre Work Items. Entender como usá-los é vital para a extração de métricas de fluxo e geração de rollups confiáveis.</p>
    
    <div class="subtitle">Como usar? (Tipos de Links)</div>
    <ul>
      <li><strong>Parent/Child (Pai/Filho):</strong> É a espinha dorsal estrutural. (Epic &rarr; Feature &rarr; PBI/User Story &rarr; Task).</li>
      <li><strong>Predecessor/Successor (Dependência):</strong> Define a ordem de execução. Se A é predecessor de B, B teoricamente espera A terminar.</li>
      <li><strong>Related (Relacionado):</strong> Link plano, horizontal, que indica apenas que há alguma correlação de contexto, sem peso estrutural.</li>
    </ul>

    <div class="subtitle">Como fazer? (Implicações Práticas)</div>
    <div class="alert warning">
      <strong>Atenção ao Board Kanban/Sprint:</strong> O Sprint Board (Taskboard) <strong>só lê</strong> relações Parent/Child para as Tasks. Se você linkar uma Task a um PBI como "Related", a Task ficará "órfã" e sumirá da raia (swimlane) do PBI.
    </div>
    <p>O link Predecessor <strong>NÃO trava</strong> o card no Kanban. Você consegue arrastar um PBI bloqueado para "Active" sem que o sistema gere bloqueio automático. Para contornar, use a Tag <strong>"Blocked"</strong>.</p>
    
    <div class="subtitle">Exemplo Real</div>
    <div class="example-box">
      <strong>Cenário:</strong> Um time criou uma User Story para "Login Social" e precisava fazer o deploy da API primeiro.<br>
      <strong>Erro Comum:</strong> Eles criaram uma Task "Deploy API" e usaram o link "Predecessor". A Task sumiu do Board.<br>
      <strong>Solução:</strong> A Task deve usar obrigatoriamente o link <strong>Child</strong> para a User Story, e se for uma dependência de outro time, o PBI inteiro recebe a Tag "Blocked" e o link "Predecessor" para o PBI do outro time.
    </div>
  </div>
</section>

<section id="s-tfs-boards">
  <div class="content-block">
    <div class="subtitle">O que é?</div>
    <p>A configuração de Boards Kanban no TFS On-Premise exige mapear Colunas Visuais para Estados de Sistema. Diferente de outras ferramentas, o Workflow State Machine dita as regras de transição por trás do board.</p>

    <div class="subtitle">Como usar?</div>
    <ul>
      <li><strong>Mapeamento de Estados:</strong> Garanta que as colunas visuais correspondam ao estado real (ex: "New", "Active", "Resolved", "Closed").</li>
      <li><strong>Split Columns (Doing/Done):</strong> Ative essa opção nas configurações da coluna. Ela divide a coluna em duas, separando o tempo que o time está de fato trabalhando (Doing) do tempo em que o item está apenas esperando para ser puxado para a próxima etapa (Done).</li>
      <li><strong>Limites WIP:</strong> Configure limites rígidos por coluna. O TFS pintará o topo da coluna de vermelho se o limite for ultrapassado.</li>
    </ul>

    <div class="subtitle">Como fazer?</div>
    <p>1. Abra o Board e clique na engrenagem (⚙️ Settings).<br>
       2. Vá na aba <strong>Columns</strong>.<br>
       3. Adicione sua coluna e marque o checkbox <strong>"Split column into doing and done"</strong>.<br>
       4. Defina o campo <strong>WIP limit</strong> com o número acordado pelo time.</p>

    <div class="subtitle">Exemplo Real</div>
    <div class="example-box">
      <strong>Problema:</strong> O time dizia que a coluna "QA" demorava 5 dias, mas o QA jurava que testava em 1 hora.<br>
      <strong>Ação:</strong> O Agile Coach dividiu a coluna "Development" em Doing/Done. Descobriu-se que o item ficava 4 dias parado na subcoluna "Done" de Development esperando o QA puxar, e apenas 1 hora na coluna de QA real.<br>
      <strong>Resultado:</strong> A métrica de Wait Time vs Touch Time ficou visível, mudando a discussão do gargalo de "Demora pra testar" para "Demora pra iniciar o teste".
    </div>
  </div>
</section>

<section id="s-tfs-cloud">
  <div class="content-block">
    <div class="subtitle">O que é?</div>
    <p>O processo de migração do TFS (On-Premise) para o Azure DevOps (Cloud). Além da mudança de infraestrutura, é uma mudança de cultura de engenharia e agilidade.</p>

    <div class="subtitle">Como usar (Estratégias)?</div>
    <ul>
      <li><strong>Migração Lift and Shift (Alta Fidelidade):</strong> Usando ferramentas como <em>TFS Integration Tools</em> para copiar todo o histórico, código, e work items mantendo as revisões.</li>
      <li><strong>Migração Limpa:</strong> Levar apenas o código fonte atual e iniciar um Backlog limpo do zero. Excelente para times com muito lixo no histórico.</li>
    </ul>

    <div class="subtitle">Como fazer? (Papel do Coach)</div>
    <p>O Agile Coach não roda scripts de migração, mas conduz as pessoas:<br>
       1. <strong>Limpeza do Backlog:</strong> Feche histórias antigas (resolvidas) e delete rascunhos inúteis semanas antes da migração.<br>
       2. <strong>Simplificação do Process Template:</strong> Se no TFS vocês usavam um Template muito burocrático (como CMMI modificado), mude para o modelo "Agile" padrão do Cloud.<br>
       3. <strong>Retreinamento:</strong> Ensine a nova visão de Azure Boards, que é mais rápida e fluida.</p>

    <div class="subtitle">Exemplo Real</div>
    <div class="example-box">
      <strong>Ocorrência:</strong> Durante uma migração para Cloud, um time quis levar 2.000 Work Items "resolvidos" desde 2018 para o novo ambiente apenas por segurança.<br>
      <strong>Intervenção:</strong> O Coach estruturou a extração desses itens para o Power BI e planilhas, mantendo o histórico de auditoria lá, e importou apenas os 150 Work Items "Ativos" para o Azure DevOps, garantindo um start limpo e livre de lentidão.
    </div>
  </div>
</section>
"""

if "<!-- ESPECIALISTA TFS                           -->" not in guia:
    # Append at the end of the file, just before the end
    guia = guia + "\n" + tfs_content
    with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(guia)

print("TFS Tabs successfully injected.")
