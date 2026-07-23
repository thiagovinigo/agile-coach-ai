# Passo 6: Classes de Serviço (Swimlanes e Expedite)

Note que no final do mockup do passo anterior, tínhamos uma linha horizontal separando o board. Aquilo é uma **Swimlane** (Raia). O Azure DevOps permite classificar os work items baseando-se em campos e mostrá-los em faixas horizontais distintas.

Isso é fundamental para implementarmos uma Classe de Serviço de urgência, o famoso **Expedite**.

## Como configurar a Swimlane Expedite

Nós já criamos o campo `Expedite` no **Passo 4**. Agora vamos fazer o board ler esse campo e mover os cards.

1. Acesse: **Boards > Boards > Board settings** (ícone de engrenagem).
2. No menu esquerdo, clique em **Swimlanes > Add swimlane**.
3. **Name:** Urgente / Expedite
4. **Criteria:** Selecione "Set criteria"
   - **Field:** `Custom.Expedite`
   - **Operator:** `=`
   - **Value:** `Sim`
5. Certifique-se de posicionar a swimlane `Urgente / Expedite` no topo da lista, e a swimlane padrão como `Normal`.

## O Comportamento no Dia a Dia

> [!NOTE]
> A swimlane é puramente uma separação **visual**. Mover um item para ela (arrastando para cima) não avança sua coluna e nem muda seu "State". Apenas preenche o campo Expedite para "Sim".

Se um item já está na coluna `[DOWN] Em Desenvolvimento` e alguém edita o campo `Expedite = Sim` no formulário, o item PERMANECE na mesma coluna, mas "flutua" magicamente para a faixa de urgência no topo do board!

<hr>
<div style="text-align: right; margin-top: 20px;">
    <strong><a href="#" onclick="document.querySelectorAll('.kb-nav-btn')[6].click(); return false;" style="color: #3b82f6; text-decoration: none;">Avançar para o Passo 7: Ciclo de Vida (Epic/Feature) ➔</a></strong>
</div>
