# Passo 2: Work Items e Limpeza de Estados Nativos

Antes de começarmos a criar nossos estados complexos de Upstream e Downstream, precisamos limpar a casa. Os processos nativos vêm com estados padrão (`New`, `Active`, `Resolved`, `Closed`) que não usaremos.

Se não os ocultarmos, o usuário ficará confuso ao ver duas opções "New" (o nativo e o nosso) na hora de arrastar o card.

## Como Ocultar (Hide) Estados Antigos:

1. Acesse **Organization Settings > Process**.
2. Clique no seu novo processo recém-criado (ex: *Processo Corporativo V1*).
3. Na lista de "Work item types", clique em **User Story** (ou PBI).
4. Navegue para a aba **States** (no menu superior horizontal).
5. Você verá os estados nativos. Para cada estado (como *New*, *Active*, *Resolved*, *Closed*):
   - Clique nos três pontos (`...`) ao lado do nome do estado.
   - Selecione **Hide** (Ocultar).
6. O estado ficará cinza e riscado, indicando que não aparecerá mais nos formulários e boards daquele tipo de item.

> [!WARNING]
> Repita este processo de ocultação também para o **Epic** e para a **Feature**. Precisamos de uma base limpa em todos os níveis da hierarquia.

<hr>
<div style="text-align: right; margin-top: 20px;">
    <strong><a href="#" onclick="document.querySelectorAll('.kb-nav-btn')[2].click(); return false;" style="color: #3b82f6; text-decoration: none;">Avançar para o Passo 3: Mapeamento de Estados ➔</a></strong>
</div>
