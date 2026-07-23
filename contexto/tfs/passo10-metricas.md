# Passo 10: Extração de Métricas e Dicas de Automação IA

Parabéns! Você estruturou todo o seu Azure DevOps seguindo uma arquitetura madura de Upstream e Downstream.
O grande benefício dessa arquitetura é que as métricas agora são colhidas nativamente. O relógio liga e desliga nos lugares certos.

## Mapeamento de Métricas por Coluna

Veja como o seu Board agora gera as principais métricas do fluxo ágil:

<div style="overflow-x:auto; margin:20px 0;">
    <table style="width:100%; border-collapse:collapse; border:1px solid #e2e8f0; font-size:0.9rem;">
        <thead>
            <tr>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; text-align:left;">Onde extrair</th>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; text-align:left;">Métrica Medida</th>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; text-align:left;">Forma Nativa de Coleta</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Ponto A (Entrada):</strong> <code>[UP] New</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Lead Time Total</strong></td><td style="padding:8px;">Analytics (TFS) — data de entrada até saída do board inteiro.</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Upstream Ativo:</strong> <code>[UP] Refinamento...</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>WIP (Upstream)</strong></td><td style="padding:8px;">Widget de CFD (Cumulative Flow) ou Query por Contagem.</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Porta do Upstream:</strong> <code>[UP] Aprovacao PO</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Throughput Upstream</strong></td><td style="padding:8px;">Quantos itens a área de negócios definiu por período.</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Ponto B (Início Dev):</strong> <code>[DOWN] Pronto para Dev.</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Cycle Time</strong></td><td style="padding:8px;">O relógio oficial de Delivery inicia aqui (State Category In Progress).</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Gargalos (Split Columns):</strong> <code>... Done</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Tempo de Espera / Fila</strong></td><td style="padding:8px;">Analytics Views no Power BI filtrando por "StateChange = Done".</td></tr>
            <tr><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Ponto C (Saída):</strong> <code>[DOWN] Done</code></td><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Throughput Final</strong></td><td style="padding:8px;">Retrospective — Itens entregues por sprint.</td></tr>
        </tbody>
    </table>
</div>

---

## Bônus: Instruções para Inteligência Artificial (Recriação)

Se você tem acesso a agentes autônomos (como nossa aba **Get Shit Done**), você não precisa configurar todos os 9 passos acima na mão. Copie o prompt abaixo e cole para o seu Bot, que tenha acesso ao seu Azure CLI (`az boards`), e ele criará isso por você:

```text
INSTRUÇÃO DE CONFIGURAÇÃO DE BOARD (Azure DevOps): 
Siga EXATAMENTE esta ordem de execução:
1. Acesse o meu processo customizado via API ou Azure CLI.
2. Crie os campos customizados (Expedite, Blocked, Blocked Reason e Aprovacao PO) no Processo ANTES de mexer no board.
3. Crie todas as colunas de Upstream e Downstream mapeando-as para novos States. Prefixo [UP] e [DOWN]. Marque colunas de gargalo como "Split Column (Doing/Done)".
4. Configure a Swimlane "Urgente / Expedite" associando-a ao campo Expedite=Sim.
5. Crie as Rules para Work Items:
   - Epic (R1, R2, R3 - abrir e fechar se baseando nos filhos)
   - Feature (R1, R2 - abrir baseado no estado dos filhos)
   - Story (Regra de Blocked copiando a data atual para Blocked Start Date e bloqueando transição sem Aprovacao PO).
```

**Parabéns por concluir a jornada de configuração do Azure Boards!** 🎉
