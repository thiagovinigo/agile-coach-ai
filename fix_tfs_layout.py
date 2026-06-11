import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    guia = f.read()

start_marker = "<!-- ========================================== -->\n<!-- ESPECIALISTA TFS                           -->"
if start_marker in guia:
    base_content = guia.split(start_marker)[0]
else:
    base_content = guia

new_content = """<!-- ========================================== -->
<!-- ESPECIALISTA TFS                           -->
<!-- ========================================== -->

<div id="s-tfs-links" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#1d4ed8,#1e40af)">
    <div class="tag">ARQUITETURA DE DADOS</div>
    <h2>🔗 Hierarquia e Links</h2>
    <p>Como o TFS conecta o trabalho e por que isso muda o seu board</p>
  </div>

  <div class="card blue">
    <div class="card-title">📌 O que é?</div>
    <p>O TFS (Team Foundation Server) e o Azure DevOps Server possuem um sistema rígido de vínculos (Links) entre Work Items. Entender como usá-los é vital para a extração de métricas de fluxo e geração de rollups confiáveis.</p>
  </div>

  <div class="st">🔗 Tipos de Links Principais</div>
  <div class="g3">
    <div class="card blue">
      <div class="card-title">👨‍👦 Parent / Child</div>
      <p>É a espinha dorsal estrutural. (Epic &rarr; Feature &rarr; PBI/User Story &rarr; Task).</p>
      <p><strong>Uso:</strong> Obrigatório para criar hierarquia e permitir o <em>Rollup</em> (progresso automático do pai baseado nos filhos).</p>
    </div>
    <div class="card blue">
      <div class="card-title">➡️ Predecessor / Successor</div>
      <p>Define a ordem de execução. Se A é predecessor de B, B teoricamente espera A terminar.</p>
      <p><strong>Uso:</strong> Gestão de dependências entre times e geração de Delivery Plans.</p>
    </div>
    <div class="card blue">
      <div class="card-title">🔗 Related (Relacionado)</div>
      <p>Link plano, horizontal, indicando correlação de contexto, sem peso estrutural.</p>
      <p><strong>Uso:</strong> Apenas como atalho de navegação (ex: "Surgiu junto com este outro bug").</p>
    </div>
  </div>

  <div class="st">⚠️ Implicações Práticas no Board</div>
  <div class="card red">
    <div class="card-title">🚨 O Taskboard só enxerga Parent/Child</div>
    <p>Se você linkar uma Task a um PBI usando o link "Related", a Task ficará "órfã" e sumirá da raia (swimlane) do PBI no Board da Sprint. <strong>Sempre use Child para tasks!</strong></p>
  </div>
  <div class="card orange">
    <div class="card-title">🔓 Predecessor não trava Kanban nativamente</div>
    <p>Diferente de algumas configurações do Jira, o link Predecessor <strong>NÃO impede</strong> o arraste do card no Kanban. Você consegue arrastar um PBI bloqueado para "Active" sem que o sistema gere bloqueio automático.</p>
    <p><strong>Como fazer:</strong> Para contornar, aplique a Tag <strong>"Blocked"</strong> ao PBI ou use o campo "Blocked = Yes" (pintando o card de vermelho no Styling do board).</p>
  </div>

  <div class="st">🎯 Exemplo Real</div>
  <div class="card dark">
    <div class="card-title">🏦 Cenário: Deploy de API Compartilhada</div>
    <ul class="chk">
      <li><strong>O Erro:</strong> Um time criou uma User Story para "Login Social". Como precisava de uma API, criaram uma Task "Deploy API" e usaram o link "Predecessor". Resultado: a Task sumiu do Board.</li>
      <li><strong>A Solução:</strong> A dependência de outro time não deve ser uma Task solta. O PBI "Login Social" deve receber a Tag "Blocked" e o link "Predecessor" apontando para o PBI do outro time. As Tasks locais devem ser sempre "Child" do PBI local.</li>
    </ul>
  </div>
</div>


<div id="s-tfs-boards" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#047857,#065f46)">
    <div class="tag">FLUXO DE TRABALHO</div>
    <h2>📋 Configuração de Boards Kanban</h2>
    <p>Mapeando o processo real para o Workflow State Machine do TFS</p>
  </div>

  <div class="card green">
    <div class="card-title">📌 O que é?</div>
    <p>A configuração de Boards Kanban no TFS On-Premise exige mapear <strong>Colunas Visuais</strong> para <strong>Estados de Sistema (State Machine)</strong>. A transição real por trás do board é o que dita regras e gatilhos.</p>
  </div>

  <div class="st">⚙️ Boas Práticas de Configuração</div>
  <div class="g3">
    <div class="card green">
      <div class="card-title">🗺️ Mapeamento de Estados</div>
      <p>Garanta que as colunas visuais correspondam ao estado real do Template (ex: "New", "Active", "Resolved", "Closed"). Várias colunas podem apontar para o mesmo estado "Active".</p>
    </div>
    <div class="card green">
      <div class="card-title">✂️ Split Columns (Doing/Done)</div>
      <p>Ative essa opção para dividir a coluna em duas, separando o tempo de trabalho (Doing) do tempo de espera/fila (Done).</p>
    </div>
    <div class="card green">
      <div class="card-title">🚦 Limites WIP</div>
      <p>Configure limites rígidos por coluna. O TFS pintará o topo da coluna de vermelho se o limite for ultrapassado, sinalizando o gargalo.</p>
    </div>
  </div>

  <div class="st">🛠️ Como fazer? (Passo a Passo)</div>
  <div class="card dark">
    <div class="card-title">Navegação no TFS</div>
    <ul class="chk">
      <li>Abra o Board e clique no ícone de engrenagem (⚙️ Settings) no canto superior direito.</li>
      <li>Vá na aba <strong>Columns</strong>.</li>
      <li>Para dividir uma coluna: clique nela e marque o checkbox <strong>"Split column into doing and done"</strong>.</li>
      <li>Para impor limites: defina o campo <strong>WIP limit</strong> com o número acordado pelo time.</li>
      <li>Para destacar gargalos: vá na aba <strong>Styles</strong> e crie uma regra que pinta o card de vermelho se <code>Tags Contains Blocked</code>.</li>
    </ul>
  </div>

  <div class="st">🎯 Exemplo Real</div>
  <div class="card dark">
    <div class="card-title">🏦 Cenário: A Ilusão do Gargalo em QA</div>
    <ul class="chk">
      <li><strong>O Problema:</strong> O Lead Time mostrava que a coluna "QA" demorava 5 dias. O Dev acusava o QA, e o QA jurava que testava em 1 hora.</li>
      <li><strong>A Ação:</strong> O Agile Coach ativou o <em>Split Column</em> (Doing/Done) na coluna "Development".</li>
      <li><strong>O Resultado:</strong> Ficou provado que o card ficava 4 dias parado na subcoluna "Dev - Done" esperando o QA ter capacity para puxar. O problema não era a lentidão do teste, mas a falta de testadores para dar vazão à fila.</li>
    </ul>
  </div>
</div>


<div id="s-tfs-cloud" class="section">
  <div class="page-header" style="background:linear-gradient(135deg,#7e22ce,#6b21a8)">
    <div class="tag">MUDANÇA CULTURAL</div>
    <h2>☁️ Migração TFS para Cloud</h2>
    <p>O Lift and Shift para o Azure DevOps e o papel do Agile Coach</p>
  </div>

  <div class="card purple">
    <div class="card-title">📌 O que é?</div>
    <p>O processo de migração do antigo TFS (On-Premise) para o Azure DevOps (Cloud). Para um Agile Coach, isso não é apenas uma mudança de infraestrutura, mas uma excelente <strong>janela de oportunidade para mudança de cultura</strong>.</p>
  </div>

  <div class="st">🔄 Estratégias de Migração</div>
  <div class="g2">
    <div class="card purple">
      <div class="card-title">📦 Migração Alta Fidelidade (Lift and Shift)</div>
      <p>Usando ferramentas oficiais (TFS Integration Tools) para copiar todo o histórico, código, anexos e work items mantendo as revisões.</p>
      <p><strong>Prós:</strong> Histórico intacto de auditoria.<br><strong>Contras:</strong> Leva o "lixo" junto, replicando processos ruins.</p>
    </div>
    <div class="card purple">
      <div class="card-title">✨ Migração Limpa (Start Over)</div>
      <p>Levar apenas o código fonte atual e iniciar um Backlog limpo do zero.</p>
      <p><strong>Prós:</strong> Elimina burocracia, permite mudar o Process Template para Agile padrão.<br><strong>Contras:</strong> Perda de vínculos históricos antigos (exige backup estático).</p>
    </div>
  </div>

  <div class="st">🛠️ Como fazer? (O Papel do Coach)</div>
  <div class="card dark">
    <div class="card-title">Passos para a Gestão de Mudança</div>
    <ul class="chk">
      <li><strong>Limpeza do Backlog:</strong> Faça um mutirão (Clean-up day) para fechar histórias antigas e deletar rascunhos inúteis semanas antes da migração.</li>
      <li><strong>Simplificação do Template:</strong> Convença a gestão a abandonar templates super customizados (ex: CMMI com 40 campos obrigatórios) e usar o "Agile" padrão do Cloud.</li>
      <li><strong>Retreinamento:</strong> Ensine a nova visão de Azure Boards, Azure Pipelines e Test Plans. O visual muda, e as pessoas ficam perdidas nos primeiros dias.</li>
    </ul>
  </div>

  <div class="st">🎯 Exemplo Real</div>
  <div class="card dark">
    <div class="card-title">🏦 Cenário: Síndrome de Acumulador</div>
    <ul class="chk">
      <li><strong>A Ocorrência:</strong> Durante a migração, o PMO exigiu levar 2.000 Work Items "resolvidos" desde 2018 para o Cloud, atrasando o script de migração em 3 dias.</li>
      <li><strong>A Intervenção:</strong> O Coach estruturou a extração desses itens legados para um Data Warehouse / Power BI para fins de auditoria, e importou <strong>apenas os 150 Work Items Ativos</strong> para o Azure DevOps.</li>
      <li><strong>O Resultado:</strong> Um ambiente Cloud leve, com busca rápida e um time focado apenas no presente.</li>
    </ul>
  </div>
</div>
"""

with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
    f.write(base_content + "\n" + new_content)

print("TFS Content replaced with new CSS layout.")
