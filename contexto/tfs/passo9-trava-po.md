# Passo 9: Trava de Transição (Aprovação do PO)

O funil de Upstream tem um portão final rigoroso: um item só pode descer para Downstream (entrar no radar de *Replenishment* dos desenvolvedores) se o Product Owner der a benção oficial.

Isso previne que a TI gaste horas investigando requisitos que ainda não têm valor de negócio validado.

## Criando a Trava via Rules (User Story)

Nós já criamos o campo customizado `Aprovacao PO` (Sim / Não) lá no **Passo 4**.
Agora, criaremos uma regra que restringe a passagem do bastão no Board se esse campo não estiver em "Sim".

1. Acesse as **Rules** da sua User Story.
2. Adicione a seguinte regra:
   - **When:** Work item state changes to → `[UP] Pronto para Replenishment`
   - **And:** Field `Aprovacao PO` <> (Diferente de) `Sim`
   - **Then:** Restrict the transition

> [!WARNING]
> **O que acontece na prática?** Se um Scrum Master ou Desenvolvedor tentar arrastar um card para a coluna de Pronto para Replenishment sem o "Sim" do PO, o card voltará para trás como elástico e o Azure DevOps exibirá um aviso vermelho exigindo a alteração do campo.

## Nível Avançado (Governança)
Quer garantir que ninguém burle a regra? 
Vá nas configurações da Organização, crie um "Security Group" chamado *Product Owners* e coloque os POs lá. Em seguida, na mesma regra acima, adicione uma cláusula: *"Se o usuário não faz parte do grupo Product Owners, bloqueie a edição do campo Aprovacao PO"*.

<hr>
<div style="text-align: right; margin-top: 20px;">
    <strong><a href="#" onclick="document.querySelectorAll('.kb-nav-btn')[9].click(); return false;" style="color: #3b82f6; text-decoration: none;">Avançar para o Passo 10: Métricas e Dicas IA ➔</a></strong>
</div>
