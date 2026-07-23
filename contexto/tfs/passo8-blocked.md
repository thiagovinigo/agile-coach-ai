# Passo 8: Rastreador de Bloqueios (Blocked)

Muitas empresas criam uma coluna chamada "Bloqueado" no Kanban. Nós não faremos isso. Se um desenvolvedor é bloqueado, a atividade permanece na mesma coluna (pois a natureza da etapa não mudou), mas a marcamos visualmente usando nosso campo customizado **Blocked** (criado no Passo 4).

Para sabermos o impacto real (quanto tempo perdemos bloqueados), faremos o TFS capturar as datas de início e fim.

## Configurando as Regras (no processo da User Story)

### Regra 1: Carimbar o Início do Bloqueio
Quando o usuário marcar o botão Blocked para Sim, o sistema grava o carimbo de tempo.
- **When:** A work item field value changes → Field: `Blocked` | Value: `Sim`
- **Then:** Copy the value of `System.ChangedDate` to → `Blocked Start Date`
- **Then:** Clear the value of → `Blocked End Date` *(Isso zera a data de fim para preparar para novos bloqueios futuros no mesmo card).*

### Regra 2: Carimbar o Fim Automaticamente
Para destravar, o usuário só precisa acessar o motivo (`Blocked Reason`) e mudar para "Bloqueio Resolvido". A automação faz o resto!
- **When:** A work item field value changes → Field: `Blocked Reason` | Value: `Bloqueio Resolvido`
- **And:** `Blocked Start Date` is not empty
- **Then:** Copy the value of `System.ChangedDate` to → `Blocked End Date`
- **Then:** Set the value of `Blocked` to → `Não` *(Tira a flag de bloqueio visual)*.

> [!TIP]
> Essa configuração substitui a polêmica coluna "Dependência", entregando métricas incrivelmente precisas (EndDate - StartDate) e deixando o Board limpo.

<hr>
<div style="text-align: right; margin-top: 20px;">
    <strong><a href="#" onclick="document.querySelectorAll('.kb-nav-btn')[8].click(); return false;" style="color: #3b82f6; text-decoration: none;">Avançar para o Passo 9: Trava do PO ➔</a></strong>
</div>
