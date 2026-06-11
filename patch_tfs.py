import re

with open('tfs_expert.js', 'r', encoding='utf-8') as f:
    code = f.read()

new_card = """
                <!-- Guia 3: Links -->
                <div class="card">
                    <div class="card-icon" style="color: #10b981; background: rgba(16, 185, 129, 0.1);">🔗</div>
                    <div class="card-title">Hierarquia e Links (O que acontece no Board?)</div>
                    <div class="card-desc">
                        No TFS (2018+ / Azure DevOps Server), a forma como você conecta Epics, Features e PBIs dita o comportamento visual e as métricas. Entenda as implicações práticas no Board:
                        <ul style="margin-top: 10px; margin-left: 20px; color: var(--text-muted); line-height: 1.6;">
                            <li><strong>Parent/Child (Pai/Filho):</strong> É a hierarquia estrutural (Epic → Feature → PBI → Task).<br>
                            <span style="color:#ef4444; font-size: 0.9em;">⚠️ Implicação no Board:</span> O Sprint Board <strong>só lê</strong> relações Parent/Child para as Tasks. Se você linkar uma Task a um PBI como "Related", a Task ficará "órfã" e sumirá da raia (swimlane) do PBI no Taskboard. Além disso, apenas o Parent/Child permite o "Rollup" nativo (exibir % de conclusão no card do Epic).</li>
                            
                            <li><strong>Predecessor/Successor (Dependência):</strong> Define ordem de execução lógica (Item A termina para B começar).<br>
                            <span style="color:#ef4444; font-size: 0.9em;">⚠️ Implicação no Board:</span> O TFS nativo <strong>NÃO trava</strong> o card no Kanban. Você consegue arrastar um PBI bloqueado para "Active" sem que o sistema grite. O link apenas adiciona um ícone de "corrente" no card. Para gestão visual de bloqueios, a boa prática é usar a <strong>Tag "Blocked"</strong> (que pinta o card de vermelho) enquanto a dependência não é resolvida.</li>
                            
                            <li><strong>Related (Simples):</strong> Link horizontal plano, serve apenas para atalho rápido de navegação.<br>
                            <span style="color:#ef4444; font-size: 0.9em;">⚠️ Implicação no Board:</span> O impacto no board é praticamente <strong>nulo</strong>. Não cria dependência, não cria hierarquia e não gera métricas. É puramente documentação (ex: "Surgiu na mesma época que outro PBI"). Não use "Related" no lugar de Pai/Filho!</li>
                        </ul>
                    </div>
                </div>
"""

# Insert before <!-- Chat/FAQ -->
if "<!-- Guia 3: Links -->" not in code:
    code = code.replace("<!-- Chat/FAQ -->", new_card + "\n                <!-- Chat/FAQ -->")

with open('tfs_expert.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Card adicionado.")
