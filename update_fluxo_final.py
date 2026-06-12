import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_content = """  <!-- 12. ANATOMIA DE UM FLUXO COMPLETO E SAUDÁVEL -->
  <h3 style="margin:20px 0 12px">🌱 Anatomia de um Fluxo Completo e Saudável</h3>
  <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:8px; padding:20px; margin-bottom:20px;">
    <p style="font-size:14px; color:#14532d; margin-top:0;">Como sabemos que nosso quadro Kanban/Scrumban está de fato saudável na prática? Eis o cenário perfeito baseando-se no nosso Board de Elite:</p>
    
    <div style="display:flex; flex-direction:column; gap:12px; margin-top:15px;">
      <div style="background:#fff; border-left:4px solid #f59e0b; padding:12px; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
        <strong style="color:#b45309; font-size:14px;">1. Upstream Ágil (O Funil Funciona)</strong>
        <p style="font-size:12px; color:#4b5563; margin-top:5px; margin-bottom:0;">Muitas "Ideias" são descartadas cedo. Os itens em "Refinando" evoluem com critérios claros (ACs). A coluna "Pronto p/ Dev" (WIP=4) funciona como uma geladeira: nunca fica totalmente vazia (o que deixaria o Dev ocioso), mas nunca ultrapassa 4 (o que estragaria o planejamento). O Replenishment foca só em manter essa geladeira abastecida.</p>
      </div>
      <div style="background:#fff; border-left:4px solid #3b82f6; padding:12px; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
        <strong style="color:#1d4ed8; font-size:14px;">2. Downstream Fluido (Puxada Limpa)</strong>
        <p style="font-size:12px; color:#4b5563; margin-top:5px; margin-bottom:0;">Um Dev só puxa da geladeira quando seu WIP (ex: ≤1) permite. Quando ele termina o código, ele <strong>não empurra</strong> para Code Review. Ele arrasta para a fila "Dev Feito" e sinaliza que terminou. O revisor puxa quando tem vaga. O QA puxa quando tem vaga. Tudo acontece sob demanda.</p>
      </div>
      <div style="background:#fff; border-left:4px solid #10b981; padding:12px; border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
        <strong style="color:#047857; font-size:14px;">3. Cartões Não Envelhecem (WIP Age Controlado)</strong>
        <p style="font-size:12px; color:#4b5563; margin-top:5px; margin-bottom:0;">A Daily não foca em "o que eu fiz ontem", mas sim em "por que aquele card da coluna de QA está parado há 3 dias?". O time protege o envelhecimento das demandas. Nenhum card vira "móvel da casa".</p>
      </div>
    </div>
  </div>

  <!-- 13. A DANÇA DOS GARGALOS E FORÇAS TAREFA -->
  <h3 style="margin:20px 0 12px">🚨 Gargalos, Forças-Tarefa (Swarming) e Mudança de Gargalo</h3>
  <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:20px; margin-bottom:20px;">
    <p style="font-size:14px; color:#92400e; margin-top:0;">O gargalo é o ponto mais lento do sistema. Pela <em>Teoria das Restrições</em>, o fluxo inteiro nunca vai ser mais rápido que o seu gargalo. Se você tentar forçar mais demanda do que o gargalo suporta, você só cria filas e estresse.</p>
    
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-top:15px;">
      <div style="background:#fff; border:1px solid #e5e7eb; padding:15px; border-radius:6px;">
        <div style="font-size:24px; margin-bottom:10px;">🚧</div>
        <strong style="color:#b91c1c; font-size:13px; display:block; margin-bottom:5px;">Como identificar o Gargalo?</strong>
        <p style="font-size:12px; color:#4b5563; margin:0;">É fácil: a coluna <em>imediatamente antes</em> dele estará cheia de cartões em fila, e a coluna <em>depois</em> dele estará ociosa ou com pouco trabalho.</p>
        <div style="background:#fef2f2; padding:8px; border-radius:4px; margin-top:10px; font-size:11px; color:#991b1b; font-style:italic;">
          Exemplo: "Dev Feito" tem 6 cards esperando. "QA" está com seu WIP no máximo estourando. "Entregue" está vazia há dias. O QA é o gargalo.
        </div>
      </div>
      <div style="background:#fff; border:1px solid #e5e7eb; padding:15px; border-radius:6px;">
        <div style="font-size:24px; margin-bottom:10px;">🐝</div>
        <strong style="color:#047857; font-size:13px; display:block; margin-bottom:5px;">O Ataque em Bando (Swarming)</strong>
        <p style="font-size:12px; color:#4b5563; margin:0;">Quando o gargalo está travado, o WIP impede que os Devs puxem novas tarefas. O que eles fazem? Força-tarefa no gargalo!</p>
        <div style="background:#f0fdf4; padding:8px; border-radius:4px; margin-top:10px; font-size:11px; color:#166534; font-style:italic;">
          Exemplo: Os Devs param de programar novas features e vão ajudar o QA (escrevendo automação de teste, validando manualmente em outro ambiente, ajudando a revisar regras de negócio).
        </div>
      </div>
    </div>
    
    <div style="background:#fff; border-left:4px solid #8b5cf6; padding:15px; border-radius:4px; margin-top:15px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
      <strong style="color:#6d28d9; font-size:14px; display:block; margin-bottom:8px;">A Mudança do Gargalo (Eleving the Constraint)</strong>
      <p style="font-size:12px; color:#4b5563; margin:0;">O gargalo nunca desaparece, ele apenas se move. Se a equipe automatizar muitos testes e fizer uma força-tarefa incrível, o QA ficará super rápido. O que vai acontecer? Os testes sairão rápido, mas agora pode ser que a etapa de <strong>Deploy</strong> (que depende de infraestrutura) passe a ter uma fila gigante. O gargalo se moveu do QA para Infra.</p>
      <p style="font-size:12px; color:#6d28d9; margin-top:8px; font-weight:bold;">O Kanban e Scrumban existem para dar visibilidade para essa "dança dos gargalos", permitindo que o time foque a melhoria contínua sempre no lugar certo que trava o fluxo.</p>
    </div>
  </div>

  <!-- 14. EVOLUA EXPERIMENTALMENTE -->"""

idx_marker = html.find('<!-- 12. EVOLUA EXPERIMENTALMENTE -->')

if idx_marker != -1:
    new_html = html[:idx_marker] + new_content + html[idx_marker+45:]
    with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Added fluxo completo and swarming successfully.")
else:
    print("Could not find marker.")
