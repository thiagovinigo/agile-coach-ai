# Passo 1: Criação do Projeto e Processo Herdado

Para configurar todo o fluxo detalhado (Upstream e Downstream) sem comprometer templates nativos, precisamos criar o nosso próprio "Processo". Processos nativos (Agile, Scrum, CMMI) no Azure DevOps são bloqueados contra edição de fluxo.

O primeiro passo absoluto é criar um modelo derivado (herdado).

## Como Fazer na Prática:

1. Acesse **Organization Settings** (engrenagem no canto inferior esquerdo da tela inicial da organização).
2. No menu lateral esquerdo, sob a seção **Boards**, clique em **Process**.
3. Localize o processo base atual do seu projeto (recomendamos o `Agile` para este board).
4. Clique nos três pontos (`...`) à direita do processo base e selecione **Create inherited process**.
5. Nomeie o processo (ex: *Processo Corporativo V1*) e adicione uma descrição opcional. Confirme.

## Vinculando ao seu Projeto:
1. Após a criação, na mesma aba de Processes, clique na guia **Projects** do seu novo processo.
2. Lá você não verá nenhum projeto associado.
3. Volte para a guia `All Processes`, clique nos três pontos (`...`) do seu projeto legado e clique em **Change process**.
4. Selecione o seu novo processo recém-criado.

> [!NOTE]
> A partir de agora, qualquer alteração que fizermos nas colunas, campos ou automações valerá exclusivamente para o seu projeto, sem afetar o resto da organização.

<hr>
<div style="text-align: right; margin-top: 20px;">
    <strong><a href="#" onclick="document.querySelectorAll('.kb-nav-btn')[1].click(); return false;" style="color: #3b82f6; text-decoration: none;">Avançar para o Passo 2: Limpeza de Estados Nativos ➔</a></strong>
</div>
