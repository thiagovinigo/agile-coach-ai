# Passo 4: Criação de Campos Customizados

Com os estados criados, precisamos definir os campos "invisíveis" que farão nossas automações e métricas funcionarem.

A coleta de métricas robustas e os direcionamentos específicos do board exigem a criação desses campos nos layouts do Azure DevOps.

## Como criar um Campo Customizado
1. Acesse **Organization Settings > Process**.
2. Clique no seu processo customizado.
3. Selecione o work item type desejado (ex: **User Story**).
4. Clique em **New field**, preencha Name, Type e valores (se PickList).
5. Salve. Isso adicionará o campo automaticamente ao layout (aba Details) do Work Item.

---

## Campos Obrigatórios do Nosso Fluxo

Crie os campos abaixo para os tipos **Epic**, **Feature** e **User Story / PBI**:

<div style="overflow-x:auto; margin:20px 0;">
    <table style="width:100%; border-collapse:collapse; border:1px solid #e2e8f0; font-size:0.9rem;">
        <thead>
            <tr>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; text-align:left;">Nome do Campo</th>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; text-align:left;">Tipo (Type)</th>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; border-right:1px solid #e2e8f0; text-align:left;">Valores Possíveis</th>
                <th style="padding:10px; background:#f8fafc; border-bottom:2px solid #cbd5e1; text-align:left;">Uso Principal</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Expedite</strong></td><td style="padding:8px; border-right:1px solid #e2e8f0;">PickList (string)</td><td style="padding:8px; border-right:1px solid #e2e8f0;">Sim / Não</td><td style="padding:8px;">Vai alimentar a nossa <em>Swimlane</em> de urgência (Passo 6).</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Blocked</strong></td><td style="padding:8px; border-right:1px solid #e2e8f0;">Boolean (ou Picklist)</td><td style="padding:8px; border-right:1px solid #e2e8f0;">true / false</td><td style="padding:8px;">Marcar o item como bloqueado por dependência.</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Blocked Reason</strong></td><td style="padding:8px; border-right:1px solid #e2e8f0;">PickList (string)</td><td style="padding:8px; border-right:1px solid #e2e8f0;">(Ver abaixo)</td><td style="padding:8px;">Diz o motivo. Será exigido se Blocked = true.</td></tr>
            <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Review Type</strong></td><td style="padding:8px; border-right:1px solid #e2e8f0;">PickList (string)</td><td style="padding:8px; border-right:1px solid #e2e8f0;">Funcional / Tecnico / PO</td><td style="padding:8px;">Ajuda nas reuniões de upstream.</td></tr>
            <tr><td style="padding:8px; border-right:1px solid #e2e8f0;"><strong>Aprovacao PO</strong></td><td style="padding:8px; border-right:1px solid #e2e8f0;">PickList (string)</td><td style="padding:8px; border-right:1px solid #e2e8f0;">Sim / Não</td><td style="padding:8px;">Vai criar a trava de transição (Passo 9).</td></tr>
        </tbody>
    </table>
</div>

### Opções para o `Blocked Reason`:
- Aguardando dependência de outro time
- Aguardando definição de negócio
- Aguardando ambiente / infraestrutura
- Aguardando aprovação externa
- Outro (descrever nos comentários)
- **Bloqueio Resolvido** *(Muito importante para a automação do Passo 8)*

<hr>
<div style="text-align: right; margin-top: 20px;">
    <strong><a href="#" onclick="document.querySelectorAll('.kb-nav-btn')[4].click(); return false;" style="color: #3b82f6; text-decoration: none;">Avançar para o Passo 5: Colunas, Split e WIP ➔</a></strong>
</div>
