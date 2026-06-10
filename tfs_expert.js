document.addEventListener('DOMContentLoaded', () => {
    const tfsView = document.getElementById('tfs-view');

    const renderTfsUI = () => {
        tfsView.innerHTML = `
            <div class="hero-section" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(15, 23, 42, 0)), url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjEiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4wNSkiLz48L3N2Zz4='); border-color: rgba(59, 130, 246, 0.3);">
                <h3 style="color: #60a5fa;">⚙️ Especialista TFS On-Premise</h3>
                <p>Guia definitivo para Agile Coaches lidando com Team Foundation Server (TFS) e Azure DevOps Server. Encontre soluções para configuração de boards, mapeamento de estados e gargalos de infraestrutura.</p>
            </div>

            <div class="grid-cards" style="grid-template-columns: 1fr;">
                
                <!-- Guia 1 -->
                <div class="card">
                    <div class="card-icon" style="color: #60a5fa; background: rgba(59, 130, 246, 0.1);">📋</div>
                    <div class="card-title">Configuração de Boards Kanban no TFS</div>
                    <div class="card-desc">
                        O TFS (versões mais antigas) pode ter limitações ao criar boards complexos de Kanban. Aqui estão as boas práticas:
                        <ul style="margin-top: 10px; margin-left: 20px; color: var(--text-muted); line-height: 1.6;">
                            <li><strong>Mapeamento de Estados:</strong> Garanta que os estados do Process Template (ex: Agile, Scrum, CMMI) reflitam a realidade. Crie colunas no board e mapeie-as para os estados nativos.</li>
                            <li><strong>Split Columns (Doing/Done):</strong> Ative colunas divididas para visualizar onde os itens estão esperando (Wait Time) vs sendo trabalhados (Touch Time).</li>
                            <li><strong>WIP Limits:</strong> Aplique limites de WIP nas colunas e instale uma cultura de não ignorar os alertas visuais vermelhos.</li>
                        </ul>
                    </div>
                </div>

                <!-- Guia 2 -->
                <div class="card">
                    <div class="card-icon" style="color: #f59e0b; background: rgba(245, 158, 11, 0.1);">🔄</div>
                    <div class="card-title">Migração TFS para Azure DevOps (Cloud)</div>
                    <div class="card-desc">
                        Dicas para conduzir times durante a transição do ambiente on-premise para a nuvem.
                        <ul style="margin-top: 10px; margin-left: 20px; color: var(--text-muted); line-height: 1.6;">
                            <li>Use a ferramenta oficial <strong>TFS Integration Tools</strong> ou o <strong>Azure DevOps Migration Tool</strong>.</li>
                            <li>Aproveite a migração para limpar históricos mortos e refatorar a árvore de áreas e iterações.</li>
                            <li>Re-treine a equipe nas novas capacidades (Pipelines, Test Plans integrados).</li>
                        </ul>
                    </div>
                </div>

                <!-- Chat/FAQ -->
                <div class="card" style="border-left: 4px solid #60a5fa;">
                    <div class="card-title" style="display:flex; align-items:center; gap:8px;">
                        <span>💡</span> FAQ Interativo do Especialista
                    </div>
                    <div class="card-desc">
                        Tem uma dúvida específica sobre customização de Work Items, permissões ou queries no TFS? O Especialista pode ajudar.
                    </div>
                    <button class="card-action" style="border-color:#3b82f6; color:#60a5fa;" onclick="alert('Funcionalidade de chat com especialista TFS em desenvolvimento!')">
                        Perguntar ao Especialista
                    </button>
                </div>

            </div>
        `;
    };

    renderTfsUI();
});
