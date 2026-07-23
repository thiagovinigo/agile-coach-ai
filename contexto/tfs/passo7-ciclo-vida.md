# Passo 7: Automação do Ciclo de Vida (Epics e Features)

O Azure DevOps não move os "pais" automaticamente se você não mandar. Precisamos configurar as regras (Rules) para garantir o engajamento e a atualização em cascata conforme as histórias avançam.

> [!NOTE]
> As regras são configuradas em **Organization Settings > Process > [Work Item Type] > Rules > New rule**.

## 1. Ciclo de Vida do Epic

Para que o Epic seja inteligente, vá na aba de Rules do **Epic** e crie 3 regras:

**R1 — Abrir Epic Automaticamente**
- **When:** A child work item changes state → `[DOWN] Em Desenvolvimento` (ou qualquer estado ativo)
- **And:** State = `[UP] New`
- **Then:** Change work item state to → `[UP] Em Progresso` (Estado ativo do Epic)

**R2 — Fechar Epic Automaticamente**
- **When:** A child work item changes state → `[DOWN] Done`
- **And:** All child work items are in state → `[DOWN] Done`
- **Then:** Change work item state to → `[DOWN] Done`

*(Adicione uma R3 para lidar com itens em Canceled / Removed também, se o seu processo exigir).*

## 2. Ciclo de Vida da Feature

A Feature deve acordar ainda mais cedo, no momento do refinamento! Vá na aba de Rules da **Feature** e crie:

**R1 — Abrir Feature no Upstream**
- **When:** A child work item is moved to board column → `[UP] Refinamento Funcional`
- **And:** State = `[UP] New`
- **Then:** Change work item state to → `[UP] Refinando` (Estado ativo da Feature)

> [!WARNING]
> Repare que a regra da Feature usa **"is moved to board column"** (é movida para a coluna) como gatilho, diferente do Epic que usou a mudança de Estado. Ambas são formas válidas de automação no TFS!

**R2 — Fechar Feature Automaticamente**
- **When:** A child work item changes state → `[DOWN] Done`
- **And:** All child work items are in state → `[DOWN] Done`
- **Then:** Change work item state to → `[DOWN] Done`

<hr>
<div style="text-align: right; margin-top: 20px;">
    <strong><a href="#" onclick="document.querySelectorAll('.kb-nav-btn')[7].click(); return false;" style="color: #3b82f6; text-decoration: none;">Avançar para o Passo 8: Rastreador de Bloqueios ➔</a></strong>
</div>
