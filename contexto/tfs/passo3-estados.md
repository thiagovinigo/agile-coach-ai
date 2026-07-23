# Passo 3: Mapeamento de Estados e Categorias

Com a casa limpa (estados antigos ocultos), agora vamos criar os **novos Estados** que vao sustentar o nosso board. O segredo aqui e entender o conceito de **State Categories**.

## Entendendo State Categories
O Azure DevOps utiliza as State Categories para alimentar os motores analiticos nativos (Lead Time, Cycle Time, Widgets). Voce *nao pode* criar categorias novas, apenas associar seus novos estados a uma das categorias obrigatorias:
- **Proposed:** Fila de espera antes de iniciar o relogio (Backlog).
- **In Progress:** Trabalho ativo. O relogio de *Cycle Time* roda ativo aqui.
- **Resolved:** Conclusao tecnica (muitas vezes ignorado, pulando para Completed).
- **Completed:** Trabalho finalizado e entregue (Para o relogio de Lead/Cycle Time).

---

## Criando seus Estados Customizados

1. Ainda na aba **States** do seu Work Item (ex: User Story), clique no botao **New State**.
2. Preencha o nome do estado exatamente como queremos e o vincule a Categoria correta, usando a tabela abaixo:

<div style="overflow-x:auto; margin:20px 0;">
    <table style="width:100%; border-collapse:collapse; border:1px solid #e2e8f0; font-size:0.9rem;">
        <thead>
            <tr>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; text-align:left;">State no Azure (Sua Configuração)</th>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; text-align:left;">Categoria Nativa (Obrigatória)</th>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; text-align:left;">Função no Board</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] New</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Proposed</strong></td><td style="padding:8px;">Fila Inicial</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Refinamento Funcional</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Upstream Ativo</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Refinamento Tecnico</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Upstream Ativo</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Aprovacao PO</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Upstream Ativo</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[UP] Pronto para Replenishment</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Fim do Upstream</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Pronto para Desenvolvimento</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Fila Downstream</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Em Desenvolvimento</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Downstream Ativo</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Ready to Teste</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Downstream Buffer</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Testando</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">QA Ativo</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Ready to Homologacao</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Downstream Buffer</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Em validacao PO</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Validação</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Homologado</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Validação Fim</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Liberado para Instalar</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>In Progress</strong></td><td style="padding:8px;">Fila de Deploy</td></tr>
            <tr><td style="padding:8px; border-right:1px solid #e2e8f0;"><code>[DOWN] Done</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Completed</strong></td><td style="padding:8px;">Entregue</td></tr>
        </tbody>
    </table>
</div>

> [!TIP]
> **Mockup Visual:** A imagem abaixo demonstra como a aba "States" deve ficar. Note como os estados recem-criados sao agrupados automaticamente debaixo de categorias cinzas na barra lateral!

![Mockup Process States](contexto/tfs/img/process_states.png)

<hr>
<div style="text-align: right; margin-top: 20px;">
    <strong><a href="#" onclick="document.querySelectorAll('.kb-nav-btn')[3].click(); return false;" style="color: #3b82f6; text-decoration: none;">Avançar para o Passo 4: Campos Customizados ➔</a></strong>
</div>
