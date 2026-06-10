
  (function() {
    var prompts = {
      userstory: function(story) {
        return 'Cole o texto abaixo no chat do Claude (Cowork ou Claude.ai) para acionar a skill **userstory-autonomous**:\n\n---\n\nQuero criar uma história de usuário no formato autônomo ONS. Aqui está o contexto:\n\n' + story + '\n\n---\n\n💡 O agente vai exibir um formulário visual pré-preenchido e gerar a história completa nas 6 seções obrigatórias: Título, Problema, Critérios de Aceite, Restrições, DoD e Contexto Técnico.';
      },
      prd: function(story) {
        return 'Cole o texto abaixo no chat para acionar a skill **generating-prd-md-from-userstory-md**:\n\n---\n\nUsando a skill de geração de PRD, transforme a história abaixo em um PRD.md completo.\n\nHistória de usuário:\n' + story + '\n\nO PRD deve incluir:\n- Visão geral e problema de negócio\n- Personas afetadas\n- Requisitos funcionais por área\n- Requisitos não-funcionais (performance, segurança, disponibilidade)\n- Critérios de aceite expandidos com edge cases\n- Dependências e integrações\n- Métricas de sucesso e hipóteses validáveis\n- Fora do escopo (explicit)\n\nSalve como docs/PRD.md.\n\n---\n\n💡 Cole direto no Claude Code ou Cowork após abrir o projeto.';
      },
      spec: function(story) {
        return 'Prompt para gerar Spec Técnica (use no Claude Code após ter o PRD):\n\n---\n\nBaseado na história e PRD do projeto, gere uma Spec Técnica completa para esta história:\n\n' + story + '\n\nA Spec deve cobrir:\n\n**1. Abordagem de Implementação**\n- Componentes e módulos afetados\n- Padrão arquitetural a seguir\n- Decisões de design com justificativa\n\n**2. Contratos de API**\n- Endpoints (método, path, request body, response, status codes)\n- Schemas de dados (criação/alteração de tabelas)\n\n**3. Plano de Testes**\n- Testes unitários obrigatórios (listar casos)\n- Testes de integração (listar cenários)\n- Testes E2E críticos\n\n**4. Riscos e Considerações**\n- Pontos de atenção de segurança\n- Impactos em outros módulos\n- Necessidade de migration ou rollback\n\n**5. Tasks de Desenvolvimento**\n- Lista ordenada de tasks com estimativa P/M/G\n- Dependências entre tasks\n\n---\n\n💡 Com a Spec pronta, você pode passar para o agente de construção.';
      },
      code: function(story) {
        return 'Cole o texto abaixo no Claude Code (terminal) para acionar a skill **ons-construcao** e iniciar o desenvolvimento autônomo:\n\n---\n\nUsando a skill ons-construcao, implemente a seguinte história de usuário de forma autônoma:\n\n' + story + '\n\nAntes de iniciar:\n1. Leia o CLAUDE.md do projeto\n2. Leia o PRD.md e TASKS.md existentes\n3. Implemente seguindo a Spec Técnica\n4. Escreva os testes antes do código (TDD)\n5. Abra um PR com description completa referenciando a história\n6. Atualize o TASKS.md marcando a story como done\n\n---\n\n⚠️ Certifique-se de que CLAUDE.md, PRD.md e TASKS.md estão atualizados antes de acionar.';
      }
    };

    var labels = {
      userstory: '🤖 Prompt para skill: userstory-autonomous',
      prd: '📄 Prompt para skill: generating-prd-md',
      spec: '⚙️ Prompt para gerar Spec Técnica',
      code: '🏗️ Prompt para skill: ons-construcao (Claude Code)'
    };

    window.gerarPromptIA = function(tipo) {
      var story = document.getElementById('ia-story-input').value.trim();
      if (!story) { alert('Cole o texto da história primeiro.'); return; }
      var output = prompts[tipo](story);
      document.getElementById('ia-output-label').textContent = labels[tipo];
      document.getElementById('ia-output-text').textContent = output;
      document.getElementById('ia-output-area').style.display = 'block';
      document.getElementById('ia-copy-ok').style.display = 'none';
      document.getElementById('ia-output-area').scrollIntoView({behavior:'smooth', block:'nearest'});
    };

    window.copiarPromptIA = function() {
      var text = document.getElementById('ia-output-text').textContent;
      navigator.clipboard.writeText(text).then(function() {
        document.getElementById('ia-copy-ok').style.display = 'block';
        setTimeout(function(){ document.getElementById('ia-copy-ok').style.display = 'none'; }, 3000);
      });
    };
  })();
  