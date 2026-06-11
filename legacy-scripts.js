
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

    window.gerarPromptIA = function(tipo, btn) {
      var container = btn ? (btn.closest('.aggregated-part') || btn.closest('.section') || document) : document;
      var inputEl = container.querySelector('.ia-story-input') || document.getElementById('ia-story-input');
      var story = inputEl ? inputEl.value.trim() : '';
      if (!story) { alert('Cole o texto da história primeiro.'); return; }
      var output = prompts[tipo](story);
      
      var labelEl = container.querySelector('.ia-output-label') || document.getElementById('ia-output-label');
      var textEl = container.querySelector('.ia-output-text') || document.getElementById('ia-output-text');
      var areaEl = container.querySelector('.ia-output-area') || document.getElementById('ia-output-area');
      var copyOkEl = container.querySelector('.ia-copy-ok') || document.getElementById('ia-copy-ok');
      
      if(labelEl) labelEl.textContent = labels[tipo];
      if(textEl) textEl.textContent = output;
      if(areaEl) {
          areaEl.style.display = 'block';
          areaEl.scrollIntoView({behavior:'smooth', block:'nearest'});
      }
      if(copyOkEl) copyOkEl.style.display = 'none';
    };

    window.copiarPromptIA = function(btn) {
      var container = btn ? (btn.closest('.aggregated-part') || btn.closest('.section') || document) : document;
      var textEl = container.querySelector('.ia-output-text') || document.getElementById('ia-output-text');
      var copyOkEl = container.querySelector('.ia-copy-ok') || document.getElementById('ia-copy-ok');
      
      if(!textEl) return;
      var text = textEl.textContent;
      navigator.clipboard.writeText(text).then(function() {
        if(copyOkEl) {
            copyOkEl.style.display = 'block';
            setTimeout(function(){ copyOkEl.style.display = 'none'; }, 3000);
        }
      });
    };
  })();
  

/* --- */


(function() {

  var policies = {
    'new': {
      title: 'NEW — Buffer de Entrada',
      color: '#3b82f6',
      fields: [
        { label: '♾ WIP Limit', value: 'Ilimitado — é um buffer de entrada, não coluna de trabalho ativo.' },
        { label: '📥 Entry Policy (DoR)', value: 'Qualquer ideia, problema relatado, requisição de stakeholder ou melhoria sugerida. Basta ter um título + problema descrito em 1 linha.' },
        { label: '📤 Exit Policy', value: 'PO aceita analisar: não é duplicata, não contradiz decisão anterior, tem mínima viabilidade de negócio.' },
        { label: '⚙️ Atividades', value: 'Triagem de duplicatas · verificação de valor mínimo · classificação por tema/épico.' },
        { label: '👤 Responsável', value: 'Qualquer stakeholder cria · PO faz a triagem e decide o que entra no refinamento.' },
        { label: '⏱️ SLA', value: 'N/A — não há compromisso de tempo nesta coluna.' }
      ]
    },
    'ref-func': {
      title: 'REFINAMENTO FUNCIONAL — PO + Dev Lead',
      color: '#3b82f6',
      fields: [
        { label: '5️⃣ WIP Limit', value: 'Máximo 5 itens simultâneos. Se cheio, PO e Dev Lead trabalham para fazer itens avançarem antes de puxar novos.' },
        { label: '📥 Entry Policy (DoR)', value: 'Card com título + problema descrito. Persona identificada. Não é duplicata. Prioridade tentativa definida pelo PO.' },
        { label: '📤 Exit Policy (DoD)', value: 'Critérios de aceite escritos (mín. 3 AC no formato Dado/Quando/Então). Persona e problema validados com pelo menos 1 dev. Story estimada em horas (deve ser ≤ 16h ou quebrada).' },
        { label: '⚙️ Atividades', value: 'Sessão de refinamento funcional (PO + Dev Lead, ~45min) · escrita colaborativa de AC · quebra de features grandes · identificação de dúvidas para próximo refinamento técnico.' },
        { label: '👤 Responsável', value: 'PO puxa de New e facilita. Dev Lead co-facilita e valida viabilidade funcional.' },
        { label: '⏱️ SLA', value: 'P85 = 5 dias úteis. Se passar disso, revisar no Flow Review.' }
      ]
    },
    'ref-tec': {
      title: 'REFINAMENTO TÉCNICO — Dev Team',
      color: '#3b82f6',
      fields: [
        { label: '5️⃣ WIP Limit', value: 'Máximo 5 itens. Time garante que nenhuma story passe para Aprovação sem DoR técnica completa.' },
        { label: '📥 Entry Policy (DoR)', value: 'AC escritos e validados pelo PO. Story ≤ 16h. Dependências identificadas (mesmo que não resolvidas ainda).' },
        { label: '📤 Exit Policy (DoD)', value: 'Arquitetura definida (diagrama ou decisão registrada). Tasks técnicas criadas no board. Dependências com owner explícito. Estimativa revisada. DoR técnica = 100%.' },
        { label: '⚙️ Atividades', value: 'Review de arquitetura e design técnico · identificação de riscos e débito técnico · criação de tasks (Dev, QA, DevOps) · estimativa técnica de esforço.' },
        { label: '👤 Responsável', value: 'Dev Lead puxa de Ref. Funcional. Todo o Dev Team participa da sessão (max 3/semana, ~1h por sessão).' },
        { label: '⏱️ SLA', value: 'P85 = 3 dias úteis.' }
      ]
    },
    'aprov-po': {
      title: 'APROVAÇÃO PO — Sign-off final upstream',
      color: '#3b82f6',
      fields: [
        { label: '5️⃣ WIP Limit', value: 'Máximo 5 itens. PO não pode acumular aprovações — deve resolver em até 2 dias úteis.' },
        { label: '📥 Entry Policy (DoR)', value: 'DoR técnica 100%. Tasks criadas. Dependências com owner. Sem riscos abertos sem mitigação.' },
        { label: '📤 Exit Policy (DoD)', value: 'PO assinou digitalmente ou registrou aprovação no card. Prioridade final confirmada. Sem bloqueios de negócio abertos.' },
        { label: '⚙️ Atividades', value: 'PO lê DoR técnica · valida regras de negócio especializadas · confirma prioridade no contexto atual do roadmap · registra aprovação.' },
        { label: '👤 Responsável', value: 'PO é o único que pode mover para Pronto para Replenishment.' },
        { label: '⏱️ SLA', value: 'P85 = 2 dias úteis. Se PO bloqueado: SM escalona para SM/gerente.' }
      ]
    },
    'pronto-replen': {
      title: 'PRONTO PARA REPLENISHMENT — Fila do Upstream',
      color: '#3b82f6',
      fields: [
        { label: '5️⃣ WIP Limit', value: 'Máximo 5 itens — o suficiente para 1–2 semanas de delivery. Mais do que isso é desperdício de refinamento (vai mudar antes de ser feito).' },
        { label: '📥 Entry Policy', value: 'PO aprovou. DoR 100%. Pronto para ser puxado pelo time no próximo Replenishment Meeting.' },
        { label: '📤 Exit Policy', value: 'Puxado para Backlog no Replenishment Meeting semanal, respeitando a capacidade disponível do time.' },
        { label: '⚙️ Atividades', value: 'Aguarda cadência semanal. PO pode reordenar a prioridade relativa dos itens aqui a qualquer momento.' },
        { label: '👤 Responsável', value: 'Dev Team puxa no Replenishment Meeting com facilitação do SM.' },
        { label: '⏱️ SLA', value: 'Máximo 1 semana (próximo replenishment). Se urgente: Replenishment antecipado ou acesso como Expedite.' }
      ]
    },
    'backlog': {
      title: 'BACKLOG — Fila Priorizada do Downstream',
      color: '#6b7280',
      fields: [
        { label: '5️⃣ WIP Limit', value: 'Máximo 5 itens — just-in-time backlog. Evita acúmulo de itens "planejados" que ficam obsoletos antes de serem feitos.' },
        { label: '📥 Entry Policy', value: 'Aprovado no Replenishment Meeting. DoR completa. Prioridade definida pelo PO.' },
        { label: '📤 Exit Policy', value: 'Dev com capacity disponível puxa o item de maior prioridade (topo da fila).' },
        { label: '⚙️ Atividades', value: 'Sequenciamento por prioridade (classe de serviço). SM verifica se há Expedites não puxados.' },
        { label: '👤 Responsável', value: 'Dev sênior puxa o item de maior prioridade quando abre capacity.' },
        { label: '⏱️ SLA', value: 'N/A — fila é puxada por capacidade, não por tempo.' }
      ]
    },
    'dev': {
      title: 'DESENVOLVIMENTO — Dev Ativo',
      color: '#f59e0b',
      fields: [
        { label: '5️⃣ WIP Limit', value: 'Máximo 5 itens. Nenhum dev pode ter mais de 1 item ativo por vez (para evitar multitasking).' },
        { label: '📥 Entry Policy (DoR)', value: 'DoR técnica 100%. Dev tem capacity livre. Sem itens bloqueados que o dev poderia desbloquear primeiro.' },
        { label: '📤 Exit Policy (DoD)', value: 'Código commitado e revisado (PR aprovado por ≥1 dev). Testes unitários passando (≥80% cobertura). Sem dívida crítica de código. PoI de desenvolvimento atualizado.' },
        { label: '⚙️ Atividades', value: 'Desenvolvimento da feature · code review · pair programming · escrita de testes · atualização de documentação técnica.' },
        { label: '👤 Responsável', value: 'Dev faz self-assign do item mais prioritário do Backlog.' },
        { label: '⏱️ SLA', value: 'P85 = 5 dias úteis por story (≤16h). Stories maiores sinalizam falha no refinamento.' }
      ]
    },
    'dev-dep': {
      title: 'DEV FINALIZADO / DEPENDÊNCIA — Espera Externa',
      color: '#ef4444',
      fields: [
        { label: '5️⃣ WIP Limit', value: 'Máximo 5 itens. Se cheio, o time tem um problema sério de dependências externas — revisar no Blocker Clustering.' },
        { label: '📥 Entry Policy', value: 'PR aprovado mas dependência externa bloqueante: API de outro time, ambiente indisponível, decisão de negócio pendente.' },
        { label: '📤 Exit Policy', value: 'Dependência resolvida. Item move para Ready to Test.' },
        { label: '⚙️ Atividades', value: 'Registro obrigatório no card: bloqueador + owner + data início + prazo esperado. Daily: atualização de status. Se >2 dias: escalate obrigatório para SM.' },
        { label: '👤 Responsável', value: 'Dev owner rastreia. SM escalona se necessário. Dev pode puxar novo item do Backlog enquanto aguarda (se WIP < 5).' },
        { label: '⏱️ SLA', value: 'SLA da dependência externa. Escalate automático se >2 dias sem resposta.' }
      ]
    },
    'ready-test': {
      title: 'READY TO TEST — Fila para QA',
      color: '#6b7280',
      fields: [
        { label: '♾ WIP Limit', value: 'Ilimitado — é uma fila. Se acumular muitos itens, o gargalo está no QA (capacidade de teste) ou no Dev (produção maior que capacidade de teste).' },
        { label: '📥 Entry Policy', value: 'Dev finalizado (PR mergeado na branch de test). Dependências resolvidas. PoI de desenvolvimento atualizado. Ambiente de teste estável.' },
        { label: '📤 Exit Policy', value: 'QA puxa quando tem capacity livre.' },
        { label: '⚙️ Atividades', value: 'Aguarda. Dev garante que o PoI (Point of Integration) foi atualizado com instruções de teste.' },
        { label: '👤 Responsável', value: 'QA puxa respeitando a prioridade (Expedites primeiro).' },
        { label: '⏱️ SLA', value: 'N/A — fila puxada por capacidade. Monitorar pelo Aging WIP.' }
      ]
    },
    'tests': {
      title: 'TESTS — QA Ativo',
      color: '#f59e0b',
      fields: [
        { label: '1️⃣ WIP Limit', value: 'Máximo 1 item por QA (analogia com Desenvolvimento — sem multitasking). Se há 2 QAs, WIP = 2.' },
        { label: '📥 Entry Policy', value: 'QA com capacity. PoI atualizado. Ambiente de teste funcional e com dados de teste preparados.' },
        { label: '📤 Exit Policy (DoD)', value: 'Todos os casos de teste executados. 0 bugs críticos (P0/P1) abertos. PoI atualizado com resultado. Bugs não críticos registrados no Backlog.' },
        { label: '⚙️ Atividades', value: 'Execução de testes funcionais · regressão nos fluxos impactados · registro de bugs com screenshot e passos para reproduzir · atualização do PoI.' },
        { label: '👤 Responsável', value: 'QA é owner. Dev que implementou fica disponível para responder dúvidas.' },
        { label: '⏱️ SLA', value: 'P85 = 2 dias úteis por story ≤16h.' }
      ]
    },
    'testes-fin': {
      title: 'TESTES FINALIZADOS — Aguarda PO',
      color: '#6b7280',
      fields: [
        { label: '♾ WIP Limit', value: 'Ilimitado (fila). Se acumular aqui, o PO está sendo o gargalo — revisar capacidade de validação.' },
        { label: '📥 Entry Policy', value: '0 bugs críticos. PoI atualizado com resultado dos testes. Evidence registrada (screenshot ou log).' },
        { label: '📤 Exit Policy', value: 'PO puxa para Em Validação PO.' },
        { label: '⚙️ Atividades', value: 'Aguarda. SM monitora acúmulo — SLA máx. 1 dia nesta coluna.' },
        { label: '👤 Responsável', value: 'PO puxa respeitando seu WIP (máx. 2 em Validação).' },
        { label: '⏱️ SLA', value: 'Máximo 1 dia útil aguardando aqui.' }
      ]
    },
    'validacao-po': {
      title: 'EM VALIDAÇÃO PO — Homologação Funcional',
      color: '#f59e0b',
      fields: [
        { label: '2️⃣ WIP Limit', value: 'Máximo 2 itens — PO não pode validar mais de 2 features em paralelo com qualidade. Força priorização.' },
        { label: '📥 Entry Policy', value: 'WIP PO < 2. Ambiente de homologação funcionando. Dados de teste preparados pelo QA.' },
        { label: '📤 Exit Policy', value: 'PO validou todos os ACs: aprovado → Homologado. Reprovado → Não Homologado (com evidência do que falhou).' },
        { label: '⚙️ Atividades', value: 'PO executa cenários dos ACs · valida regras de negócio · coleta feedback de stakeholders se necessário · registra evidência de aprovação/reprovação.' },
        { label: '👤 Responsável', value: 'PO é owner. Pode convidar stakeholder para validação conjunta.' },
        { label: '⏱️ SLA', value: 'P85 = 1 dia útil.' }
      ]
    },
    'homologado': {
      title: 'HOMOLOGADO — Aprovado para Deploy',
      color: '#22c55e',
      fields: [
        { label: '♾ WIP Limit', value: 'Ilimitado (fila transitória). Items ficam aqui pouco tempo — passam para Liberada para Instalar automaticamente.' },
        { label: '📥 Entry Policy', value: 'PO aprovou todos os ACs. Evidência registrada no card.' },
        { label: '📤 Exit Policy', value: 'Move automaticamente para Liberada para Instalar após sign-off e documentação atualizada.' },
        { label: '⚙️ Atividades', value: 'Atualização de documentação de usuário. Release notes escritas. Comunicação para stakeholders preparada.' },
        { label: '👤 Responsável', value: 'Dev / Tech Writer atualiza docs. PO prepara comunicação.' },
        { label: '⏱️ SLA', value: 'Máximo 1 dia — não deixar acumular aqui.' }
      ]
    },
    'nao-homologado': {
      title: 'NÃO HOMOLOGADO — Reprovado pelo PO',
      color: '#ef4444',
      fields: [
        { label: '♾ WIP Limit', value: 'Ilimitado (buffer temporário). Items não ficam aqui — são processados imediatamente.' },
        { label: '📥 Entry Policy', value: 'PO reprovou: AC não atendido ou comportamento incorreto. Evidência obrigatória: screenshot + descrição do que falhou.' },
        { label: '📤 Exit Policy', value: 'Card de correção criado e movido para Backlog com a prioridade correta (Expedite se crítico, Standard se funcional).' },
        { label: '⚙️ Atividades', value: 'PO cria card de correção com: AC que falhou, evidência, AC revisado mais preciso, critério de teste melhorado. Análise de causa raiz (foi AC ambíguo? DoR incompleta?).' },
        { label: '👤 Responsável', value: 'PO cria o card de correção. SM facilita análise de causa raiz.' },
        { label: '⏱️ SLA', value: 'Processar em até 1 dia útil.' }
      ]
    },
    'liberada': {
      title: 'LIBERADA PARA INSTALAR — Aguarda Deploy',
      color: '#6b7280',
      fields: [
        { label: '♾ WIP Limit', value: 'Ilimitado (fila). Acúmulo aqui indica que a frequência de deploy é baixa — considerar deploy contínuo ou janelas mais frequentes.' },
        { label: '📥 Entry Policy', value: 'Homologado e documentado. Release notes prontas. Comunicação para usuários preparada.' },
        { label: '📤 Exit Policy', value: 'Janela de deploy disponível. Infra/DevOps com capacity e rollback plan definido.' },
        { label: '⚙️ Atividades', value: 'Infra prepara ambiente de produção · smoke test plan definido · rollback procedure documentada · monitoramento configurado.' },
        { label: '👤 Responsável', value: 'Infra / DevOps puxa e executa deploy.' },
        { label: '⏱️ SLA', value: 'Máximo: próxima janela de deploy programada. Expedites têm janela especial.' }
      ]
    },
    'em-producao': {
      title: 'EM PRODUÇÃO — Período de Observação',
      color: '#f59e0b',
      fields: [
        { label: '5️⃣ WIP Limit', value: 'Máximo 5 features em período de observação simultâneo. Mais do que isso compromete a capacidade de resposta a incidentes.' },
        { label: '📥 Entry Policy', value: 'Deploy realizado com sucesso. Smoke test inicial OK. Alertas configurados.' },
        { label: '📤 Exit Policy (DoD)', value: '24–48h de observação sem incidente crítico (P0/P1). PO confirma que métricas de negócio esperadas estão se comportando. Nenhum alerta crítico ativo.' },
        { label: '⚙️ Atividades', value: 'Monitoramento ativo de erros · análise de métricas de uso · resposta a incidentes · ajuste de alertas · coleta de feedback dos primeiros usuários.' },
        { label: '👤 Responsável', value: 'Infra/Dev monitora. PO valida métricas de negócio.' },
        { label: '⏱️ SLA', value: 'Período de observação: 24–48h. Incidentes P0: resposta em 15min.' }
      ]
    },
    'done': {
      title: 'DONE — Entregue e Estável',
      color: '#10b981',
      fields: [
        { label: '✅ Critério', value: '24h+ em produção sem incidente crítico. PO confirmou métricas. Documentação final atualizada.' },
        { label: '📋 Registro', value: 'Lead time final registrado para análise de fluxo. Throughput atualizado. Dados alimentam o Monte Carlo e o CFD.' },
        { label: '🎉 Celebração', value: 'Time reconhece a entrega na Daily ou Retrospectiva. Pequenas vitórias importam para a cultura do time.' },
        { label: '🔁 Aprendizado', value: 'Se houve Não Homologado nesta story: retrospectiva específica do item para melhorar DoR/AC da próxima vez.' },
        { label: '📊 Métricas', value: 'Cycle time, lead time e dias em cada coluna são registrados para análise de fluxo no Flow Review mensal.' },
        { label: '👤 Responsável', value: 'SM fecha o card e registra métricas. Time comemora.' }
      ]
    }
  };

  window.showPolicy = function(colId) {
    var policy = policies[colId];
    if (!policy) return;
    
    var dqKeyMap = {
      'pronto-replen': 'pronto-rep',
      'dev-dep': 'dev-fin',
      'testes-fin': 'tests-fin',
      'validacao-po': 'valid-po',
      'nao-homologado': 'nao-homol',
      'liberada': 'lib-instalar',
      'em-producao': 'em-prod'
    };
    var dqKey = dqKeyMap[colId] || colId;
    
    var panel = document.getElementById('policy-panel');
    var title = document.getElementById('policy-title');
    var body = document.getElementById('policy-body');
    title.textContent = policy.title;
    title.style.color = policy.color;
    
    var html = policy.fields.map(function(f) {
      return '<div style="background:var(--bg-primary,#fff);border:1px solid var(--border,#e2e8f0);border-radius:8px;padding:12px 14px;">' +
        '<div style="font-size:12px;font-weight:700;color:' + policy.color + ';margin-bottom:4px;">' + f.label + '</div>' +
        '<div style="font-size:13px;line-height:1.5;color:var(--text-primary,#1e293b);">' + f.value + '</div>' +
        '</div>';
    }).join('');
    
    if (window.DQ && window.DQ[dqKey] && window.DQ[dqKey].questions && window.DQ[dqKey].questions.length > 0) {
      html += '<div style="margin-top:16px;background:#f8fafc;border:2px dashed #94a3b8;border-radius:8px;padding:12px 14px;">' +
              '<div style="font-size:14px;font-weight:800;color:#334155;margin-bottom:8px;">❓ Perguntas sugeridas para a Daily:</div>' +
              '<ul style="margin:0;padding-left:20px;font-size:13px;color:#475569;">' +
              window.DQ[dqKey].questions.map(function(q){ return '<li style="margin-bottom:6px;">' + q.q + '</li>'; }).join('') +
              '</ul></div>';
    }
    
    body.innerHTML = html;
    
    panel.style.display = 'block';
    panel.style.borderColor = policy.color;
    panel.scrollIntoView({behavior:'smooth', block:'nearest'});
    
    // highlight active column
    document.querySelectorAll('.bcol').forEach(function(el){ el.style.outline = 'none'; });
    var activeCol = document.querySelector('[data-col="' + colId + '"]');
    if (activeCol) activeCol.style.outline = '3px solid ' + policy.color;
  };

  window.toggleScenario = function(id) {
    var el = document.getElementById(id);
    var arrow = document.getElementById(id + '-arrow');
    if (el.style.display === 'none') {
      el.style.display = 'block';
      arrow.style.transform = 'rotate(180deg)';
    } else {
      el.style.display = 'none';
      arrow.style.transform = 'rotate(0deg)';
    }
  };

})();


/* --- */


/* ══════════════════════════════════════════════════════════════
   DAILY QUESTIONS + AGENT — Board Completo (s-elite-board)
   ══════════════════════════════════════════════════════════════ */
(function(){

/* ── 1. DATA: perguntas por coluna ── */
var DQ = {
  'new': {
    label: '📥 New — Buffer de Entrada',
    color: '#1e40af', bg: '#eff6ff', border: '#bfdbfe',
    flag: null,
    questions: [
      { q: 'A demanda tem um objetivo de negócio claro ou apenas uma solução técnica?', risk: ['não sei','sem objetivo','incerto'] },
      { q: 'Há alguma dependência externa (outra squad, fornecedor, PO de outro produto) que precisa ser resolvida antes?', risk: ['sim','depende','esperar'] },
      { q: 'Existe um responsável por conduzir o Refinamento Funcional desta demanda?', risk: ['não','sem dono','ninguém'] },
      { q: 'Há quanto tempo ela está em New? O risco de envelhecer sem avançar é alto?', risk: ['muito','semanas','dias'] }
    ]
  },
  'ref-func': {
    label: '📋 Ref. Funcional',
    color: '#1e40af', bg: '#eff6ff', border: '#bfdbfe',
    flag: 'Itens em Ref. Funcional há mais de 3 dias indicam bloqueio — escale para o SM.',
    questions: [
      { q: 'Os critérios de aceite (ACs) já foram escritos ou estão em andamento?', risk: ['não','sem ac','nada'] },
      { q: 'Há alguma dúvida de negócio que bloqueia a escrita dos ACs?', risk: ['sim','bloqueia','dúvida'] },
      { q: 'O PO está disponível para tirar dúvidas hoje ou há um bloqueio de agenda?', risk: ['não','indisponível','bloqueado'] },
      { q: 'A demanda parece maior que 2 dias de trabalho? Precisa ser quebrada antes de avançar?', risk: ['sim','grande','épico','muito'] }
    ]
  },
  'ref-tec': {
    label: '⚙️ Ref. Técnico',
    color: '#1e40af', bg: '#eff6ff', border: '#bfdbfe',
    flag: 'Se a estimativa ultrapassar 16h, o item deve ser quebrado antes de ir para Aprovação PO.',
    questions: [
      { q: 'A estimativa foi feita? O esforço está ≤ 16h?', risk: ['não','sem estim','acima','mais de 16'] },
      { q: 'As tasks técnicas foram criadas no board/ferramenta?', risk: ['não','sem task','nenhuma'] },
      { q: 'Há dependências técnicas (API, banco, serviço externo, permissão) não resolvidas?', risk: ['sim','depende','não resolvida'] },
      { q: 'Alguma incerteza técnica alta que justifica um Spike antes de colocar no sprint?', risk: ['sim','incerto','não sei como'] }
    ]
  },
  'aprov-po': {
    label: '✅ Aprovação PO',
    color: '#1e40af', bg: '#eff6ff', border: '#bfdbfe',
    flag: null,
    questions: [
      { q: 'O PO já revisou os critérios de aceite desta demanda?', risk: ['não','pendente','ainda não'] },
      { q: 'Existe alguma mudança de escopo ou refinamento adicional solicitado pelo PO?', risk: ['sim','mudou','solicitou'] },
      { q: 'O que está faltando para o PO dar o aceite formal?', risk: [''] },
      { q: 'Há algum dependência que o PO identificou que bloqueia a aprovação?', risk: ['sim','bloqueia','depende'] }
    ]
  },
  'pronto-rep': {
    label: '🏁 Pronto p/ Replenishment',
    color: '#1e40af', bg: '#eff6ff', border: '#bfdbfe',
    flag: 'Se este item ficou em Pronto p/ Replenishment mais de 1 sprint sem ser puxado, revise a prioridade.',
    questions: [
      { q: 'A DoR está 100% completa (ACs, tamanho ≤ 16h, tasks, sem dependências abertas)?', risk: ['não','incompleta','falta'] },
      { q: 'Já tem dev identificado para puxar este item no próximo replenishment?', risk: ['não','ninguém','sem dono'] },
      { q: 'Houve alguma mudança de contexto de negócio desde o refinamento? Os ACs ainda são válidos?', risk: ['sim','mudou','desatualizado'] }
    ]
  },
  'backlog': {
    label: '📦 Backlog (Sprint)',
    color: '#d97706', bg: '#fffbeb', border: '#fde68a',
    flag: 'Um item no Backlog do sprint que não foi puxado até o 3º dia útil precisa ser reavaliado.',
    questions: [
      { q: 'O WIP atual da coluna permite puxar este item sem ultrapassar o limite?', risk: ['não','cheio','limite'] },
      { q: 'Quem vai assumir esta demanda e quando?', risk: ['ninguém','sem dono','não sei'] },
      { q: 'Há algum pré-requisito técnico ou de ambiente não resolvido antes de iniciar?', risk: ['sim','bloqueia','falta'] }
    ]
  },
  'dev': {
    label: '💻 Desenvolvimento',
    color: '#d97706', bg: '#fffbeb', border: '#fde68a',
    flag: 'Itens em Dev há mais de 3 dias estão em risco de ultrapassar o SLA. Investigue bloqueios.',
    questions: [
      { q: 'Há quantos dias este item está em desenvolvimento?', risk: ['3','4','5','6','7','8'] },
      { q: 'Existe algum bloqueio técnico, dúvida ou dependência que impediu o avanço?', risk: ['sim','bloqueia','depende','dúvida'] },
      { q: 'O item vai ser concluído hoje? Se não, o que falta para finalizar?', risk: ['não','amanhã','não sei'] },
      { q: 'O WIP individual está respeitado (≤1 item ativo por dev além do bloqueado)?', risk: ['não','mais de','acima'] },
      { q: 'Os critérios de aceite foram relidos antes de colocar em Dev Finalizado?', risk: ['não','não li','esqueceu'] }
    ]
  },
  'dev-fin': {
    label: '🔗 Dev Fin. / Dependência',
    color: '#d97706', bg: '#fffbeb', border: '#fde68a',
    flag: '⚠️ Itens aqui por mais de 1 dia precisam de ação. Dependência sem owner = bloqueio indefinido.',
    questions: [
      { q: 'O que especificamente está impedindo este item de ir para Ready to Test?', risk: [''] },
      { q: 'Qual é a dependência? Quem é o owner responsável por resolvê-la?', risk: ['não sei','sem dono','ninguém'] },
      { q: 'Há uma data prevista para resolução da dependência?', risk: ['não','sem data','indefinida'] },
      { q: 'O bloqueio foi comunicado ao SM e ao PO?', risk: ['não','ainda não'] }
    ]
  },
  'ready-test': {
    label: '🧪 Ready to Test',
    color: '#d97706', bg: '#fffbeb', border: '#fde68a',
    flag: null,
    questions: [
      { q: 'O ambiente de teste está disponível e com dados preparados?', risk: ['não','indisponível','sem dados'] },
      { q: 'O QA tem capacity hoje para iniciar os testes?', risk: ['não','ocupado','sem capacity'] },
      { q: 'Os casos de teste já foram planejados ou o QA conhece os critérios de aceite?', risk: ['não','sem plano','não leu'] },
      { q: 'Existe alguma dependência de configuração ou acesso que bloqueia o início dos testes?', risk: ['sim','bloqueia','sem acesso'] }
    ]
  },
  'tests': {
    label: '🔍 Tests',
    color: '#d97706', bg: '#fffbeb', border: '#fde68a',
    flag: 'Itens em Tests há mais de 2 dias estão fora do SLA. Revise a prioridade com o QA.',
    questions: [
      { q: 'Há quantos dias este item está em teste?', risk: ['2','3','4','5'] },
      { q: 'Algum bug foi encontrado? Qual é a severidade (P0/P1/P2)?', risk: ['p0','p1','crítico','bloqueante'] },
      { q: 'Todos os casos de teste já foram executados ou faltam cenários?', risk: ['não','faltam','incompleto'] },
      { q: 'Vai ser concluído hoje? O que falta para finalizar?', risk: ['não','amanhã','não sei'] }
    ]
  },
  'tests-fin': {
    label: '✔️ Testes Finalizados',
    color: '#d97706', bg: '#fffbeb', border: '#fde68a',
    flag: null,
    questions: [
      { q: 'O PO foi notificado e está disponível para iniciar a validação?', risk: ['não','indisponível','ainda não'] },
      { q: 'O ambiente de homologação está pronto e acessível para o PO?', risk: ['não','sem acesso','indisponível'] },
      { q: 'Há algum resultado de teste que precisa ser comunicado ao PO antes da validação?', risk: ['sim','aviso','bug'] }
    ]
  },
  'valid-po': {
    label: '👁️ Em Validação PO',
    color: '#d97706', bg: '#fffbeb', border: '#fde68a',
    flag: 'Se o PO não valida em 1 dia útil, o SM deve escalar. Validação não é fila.',
    questions: [
      { q: 'O PO já iniciou a validação? Qual é o feedback até agora?', risk: ['não','ainda não','sem feedback'] },
      { q: 'Algum critério de aceite não passou? O que precisa ser ajustado?', risk: ['sim','falhou','não passou'] },
      { q: 'O PO tem alguma dúvida que precisa ser respondida pelo time?', risk: ['sim','dúvida','precisa'] },
      { q: 'Quando o PO prevê dar a decisão (homologado ou não)?', risk: ['não sei','sem prazo','indefinido'] }
    ]
  },
  'homologado': {
    label: '🟢 Homologado',
    color: '#166534', bg: '#f0fdf4', border: '#86efac',
    flag: null,
    questions: [
      { q: 'Já tem janela de deploy agendada com o time de infra/ops?', risk: ['não','sem janela','ainda não'] },
      { q: 'Há dependência de outros itens que precisam ser deployados juntos?', risk: ['sim','junto','depende'] },
      { q: 'O plano de rollback está definido caso haja problema em produção?', risk: ['não','sem plano','não pensamos'] },
      { q: 'O time de monitoramento foi notificado do deploy iminente?', risk: ['não','ainda não','esqueceu'] }
    ]
  },
  'nao-homol': {
    label: '🔴 Não Homologado',
    color: '#991b1b', bg: '#fff1f2', border: '#fca5a5',
    flag: '🔴 ATENÇÃO: Item rejeitado na homologação. Registre o bug, priorize a correção.',
    questions: [
      { q: 'O que exatamente falhou na validação do PO? Qual critério de aceite não foi atendido?', risk: [''] },
      { q: 'O bug/problema foi registrado no backlog com passos para reproduzir?', risk: ['não','sem registro','esqueceu'] },
      { q: 'Quem vai corrigir e qual é o prazo estimado para a correção?', risk: ['não sei','sem dono','sem prazo'] },
      { q: 'A correção vai impactar outros itens ou fluxos do sistema?', risk: ['sim','impacta','outro'] }
    ]
  },
  'lib-instalar': {
    label: '🚀 Liberada p/ Instalar',
    color: '#166534', bg: '#f0fdf4', border: '#86efac',
    flag: null,
    questions: [
      { q: 'A janela de deploy foi confirmada e comunicada a todos os envolvidos?', risk: ['não','sem confirmação','ainda não'] },
      { q: 'Há riscos de downtime ou impacto em usuários que precisam ser comunicados?', risk: ['sim','downtime','impacto'] },
      { q: 'O monitoramento pós-deploy está configurado (alertas, dashboards, health check)?', risk: ['não','sem monit','não configurou'] }
    ]
  },
  'em-prod': {
    label: '🌐 Em Produção',
    color: '#166534', bg: '#f0fdf4', border: '#86efac',
    flag: null,
    questions: [
      { q: 'O item está estável em produção? Algum alerta de monitoramento foi disparado?', risk: ['não','alerta','erro','instável'] },
      { q: 'Há feedback de usuários ou clientes sobre a feature?', risk: ['sim','problema','reclamação'] },
      { q: 'Está pronto para ser movido para Done ou ainda há observação necessária?', risk: ['não','aguarda','observando'] }
    ]
  },
  'done': {
    label: '🏆 Done',
    color: '#374151', bg: '#f8fafc', border: '#e2e8f0',
    flag: null,
    questions: [] // special case
  }
};

/* ── 2. Daily Questions pill click ── */
window.DQ = DQ;
var currentDQCol = null;
document.addEventListener('click', function(e){
  var pill = e.target.closest('.dq-pill');
  if(!pill) return;
  var col = pill.dataset.col;
  if(!col) return;

  // toggle
  if(currentDQCol === col){
    document.getElementById('dq-panel').style.display = 'none';
    currentDQCol = null;
    document.querySelectorAll('.dq-pill').forEach(p=>p.style.opacity='1');
    return;
  }
  currentDQCol = col;
  document.querySelectorAll('.dq-pill').forEach(p=>p.style.opacity=p.dataset.col===col?'1':'0.5');

  var data = DQ[col];
  if(!data) return;
  var panel = document.getElementById('dq-panel');
  var titleEl = document.getElementById('dq-title');
  var listEl = document.getElementById('dq-list');
  var flagEl = document.getElementById('dq-flag');

  panel.style.display = 'block';
  panel.style.borderColor = data.border;
  panel.style.background = data.bg;
  titleEl.style.color = data.color;
  titleEl.textContent = data.label;

  if(col === 'done'){
    listEl.innerHTML = '<div style="text-align:center;padding:20px;font-size:.95rem;color:#166534;font-weight:600;">🏆 Item concluído — nada a perguntar na daily! Mova para Done e celebre.</div>';
    flagEl.style.display = 'none';
    return;
  }

  listEl.innerHTML = data.questions.map(function(item, i){
    return '<div style="display:flex;gap:10px;align-items:flex-start;padding:10px 12px;background:white;border-radius:8px;border:1px solid '+data.border+';font-size:.88rem;color:#374151;">' +
      '<span style="min-width:22px;height:22px;border-radius:50%;background:'+data.color+';color:white;display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:700;">'+(i+1)+'</span>' +
      '<span>'+item.q+'</span></div>';
  }).join('');

  if(data.flag){
    flagEl.style.display = 'block';
    flagEl.style.background = (col==='nao-homol')?'#fee2e2':'#fef3c7';
    flagEl.style.color = (col==='nao-homol')?'#991b1b':'#92400e';
    flagEl.textContent = data.flag;
  } else {
    flagEl.style.display = 'none';
  }
  panel.scrollIntoView({behavior:'smooth', block:'nearest'});
});

/* ── 3. AGENT ── */
var agentState = {
  col: null, desc: '', days: 1,
  questions: [], currentQ: 0,
  answers: [], flags: []
};

window.agentStart = function(){
  var col = document.getElementById('agent-col').value;
  var desc = document.getElementById('agent-desc').value.trim();
  var days = parseInt(document.getElementById('agent-days').value)||1;
  if(!col){ alert('Selecione a coluna da demanda.'); return; }
  if(!desc){ alert('Descreva brevemente a demanda.'); return; }

  var data = DQ[col];
  agentState = { col:col, desc:desc, days:days, questions: data.questions.slice(), currentQ:0, answers:[], flags:[] };

  document.getElementById('agent-start-btn').style.display = 'none';
  document.getElementById('agent-reset-btn').style.display = 'block';
  document.getElementById('agent-col').disabled = true;
  document.getElementById('agent-desc').disabled = true;
  document.getElementById('agent-days').disabled = true;
  document.getElementById('agent-status-label').textContent = 'Sessão ativa — '+data.label;

  agentClearChat();

  // intro message
  agentBubble('agent', '👋 Vou te ajudar a diagnosticar a demanda <strong>"'+escHtml(desc)+'"</strong> que está em <strong>'+data.label+'</strong> há '+days+' dia(s).');

  if(col === 'done'){
    agentBubble('agent', '🏆 Este item está em <strong>Done</strong> — está concluído! Nada a perguntar. Parabéns ao time.');
    agentDiagnosis([]);
    return;
  }

  // aging warning
  var slaWarn = { dev:3, tests:2, 'ref-func':3, 'dev-fin':1, 'valid-po':1 };
  if(slaWarn[col] && days >= slaWarn[col]){
    agentBubble('agent', '⚠️ <strong>Atenção:</strong> com '+days+' dia(s) nessa coluna, o item está no limiar do SLA. Vou prestar atenção extra nas respostas.');
    if(days >= slaWarn[col]) agentState.flags.push('Aging ≥ SLA ('+days+' dias em '+data.label+')');
  }

  setTimeout(function(){ agentNextQ(); }, 600);
};

function agentNextQ(){
  if(agentState.currentQ >= agentState.questions.length){
    agentDiagnosis(agentState.flags);
    return;
  }
  var q = agentState.questions[agentState.currentQ];
  var num = agentState.currentQ + 1;
  var total = agentState.questions.length;
  agentBubble('agent', '('+ num +'/'+total+') '+q.q);
  document.getElementById('agent-input-area').style.display = 'block';
  document.getElementById('agent-answer').value = '';
  document.getElementById('agent-answer').focus();
  agentQuickBtns(q);
}

function agentAnswer(){
  var val = document.getElementById('agent-answer').value.trim();
  if(!val) return;
  agentBubble('user', escHtml(val));
  document.getElementById('agent-input-area').style.display = 'none';
  document.getElementById('agent-quick').innerHTML = '';

  // check for risk keywords
  var q = agentState.questions[agentState.currentQ];
  var low = val.toLowerCase();
  var risky = q.risk.some(function(r){ return r && low.includes(r); });
  if(risky){
    agentState.flags.push('Risco identificado na pergunta '+(agentState.currentQ+1)+': "'+val+'"');
    setTimeout(function(){ agentBubble('agent', '⚠️ Anotado — isso pode ser um bloqueio. Continuando...'); }, 300);
  }

  agentState.answers.push({ q: q.q, a: val, risky: risky });
  agentState.currentQ++;
  setTimeout(function(){ agentNextQ(); }, risky ? 800 : 400);
}

window.agentAnswer = agentAnswer;

function agentQuickBtns(q){
  var quickEl = document.getElementById('agent-quick');
  var opts = ['Sim, está ok', 'Não, há bloqueio', 'Em andamento', 'Não sei ainda'];
  quickEl.innerHTML = opts.map(function(o){
    return '<button onclick="(function(){document.getElementById(\'agent-answer\').value=\''+o+'\';agentAnswer();})()" style="background:#f1f5f9;color:#374151;border:1px solid #e2e8f0;border-radius:20px;padding:4px 12px;font-size:.78rem;cursor:pointer;">'+o+'</button>';
  }).join('');
}

function agentDiagnosis(flags){
  document.getElementById('agent-input-area').style.display = 'none';
  var hasCritical = flags.some(function(f){ return f.includes('Risco') || f.includes('Aging'); });
  var status = flags.length === 0 ? 'ok' : hasCritical ? 'blocked' : 'attention';

  var statusMap = {
    ok:        { label:'✅ Fluindo', bg:'#dcfce7', color:'#166534', border:'#86efac', msg:'Nenhum bloqueio identificado. Item pode avançar normalmente.' },
    attention: { label:'⚠️ Atenção', bg:'#fef3c7', color:'#92400e', border:'#fde68a', msg:'Há pontos de atenção que precisam ser acompanhados de perto.' },
    blocked:   { label:'🔴 Bloqueado / Em Risco', bg:'#fee2e2', color:'#991b1b', border:'#fca5a5', msg:'Bloqueio identificado. Ação imediata necessária — escale para o SM.' }
  };
  var s = statusMap[status];

  var diagHtml = '<div style="background:'+s.bg+';border:1.5px solid '+s.border+';border-radius:10px;padding:16px;">' +
    '<div style="font-size:1.05rem;font-weight:800;color:'+s.color+';margin-bottom:6px;">Diagnóstico: '+s.label+'</div>' +
    '<div style="font-size:.87rem;color:'+s.color+';margin-bottom:12px;">'+s.msg+'</div>';

  if(flags.length > 0){
    diagHtml += '<div style="font-weight:700;color:'+s.color+';font-size:.82rem;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em;">Pontos registrados:</div>' +
      '<ul style="margin:0 0 0 16px;padding:0;">' +
      flags.map(function(f){ return '<li style="font-size:.84rem;color:'+s.color+';margin-bottom:4px;">'+escHtml(f)+'</li>'; }).join('') +
      '</ul>';
  }

  if(agentState.answers.length > 0){
    diagHtml += '<details style="margin-top:12px;"><summary style="font-size:.82rem;font-weight:600;color:'+s.color+';cursor:pointer;">Ver todas as respostas</summary>' +
      '<div style="margin-top:8px;display:flex;flex-direction:column;gap:6px;">' +
      agentState.answers.map(function(a){
        return '<div style="font-size:.8rem;padding:8px 10px;background:white;border-radius:6px;border:1px solid '+s.border+';">' +
          '<div style="color:#64748b;margin-bottom:2px;">'+escHtml(a.q)+'</div>' +
          '<div style="font-weight:600;color:'+(a.risky?'#dc2626':'#374151')+';">→ '+escHtml(a.a)+'</div>' +
          '</div>';
      }).join('') +
      '</div></details>';
  }

  diagHtml += '</div>';

  var dEl = document.getElementById('agent-diagnosis');
  dEl.style.display = 'block';
  dEl.innerHTML = diagHtml;
  dEl.scrollIntoView({behavior:'smooth', block:'nearest'});
  document.getElementById('agent-status-label').textContent = 'Diagnóstico: '+s.label;
  agentBubble('agent', 'Diagnóstico concluído! Veja o resumo abaixo. 👇');
}

window.agentReset = function(){
  document.getElementById('agent-start-btn').style.display = 'block';
  document.getElementById('agent-reset-btn').style.display = 'none';
  document.getElementById('agent-col').disabled = false;
  document.getElementById('agent-desc').disabled = false;
  document.getElementById('agent-days').disabled = false;
  document.getElementById('agent-col').value = '';
  document.getElementById('agent-desc').value = '';
  document.getElementById('agent-days').value = '1';
  document.getElementById('agent-status-label').textContent = 'Aguardando configuração...';
  document.getElementById('agent-input-area').style.display = 'none';
  document.getElementById('agent-diagnosis').style.display = 'none';
  document.getElementById('agent-quick').innerHTML = '';
  agentClearChat();
};

function agentClearChat(){
  document.getElementById('agent-chat').innerHTML = '';
}

function agentBubble(role, html){
  var chat = document.getElementById('agent-chat');
  var isAgent = role === 'agent';
  var div = document.createElement('div');
  div.style.cssText = 'display:flex;gap:8px;align-items:flex-start;'+(isAgent?'':'flex-direction:row-reverse;');
  var avatar = document.createElement('div');
  avatar.style.cssText = 'min-width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.85rem;background:'+(isAgent?'#3b82f6':'#e2e8f0')+';color:'+(isAgent?'#fff':'#374151')+';';
  avatar.textContent = isAgent ? '🤖' : '👤';
  var bubble = document.createElement('div');
  bubble.style.cssText = 'max-width:80%;padding:9px 13px;border-radius:10px;font-size:.87rem;line-height:1.45;background:'+(isAgent?'#f1f5f9':'#3b82f6')+';color:'+(isAgent?'#374151':'#fff')+';';
  bubble.innerHTML = html;
  div.appendChild(avatar);
  div.appendChild(bubble);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function escHtml(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

})();


/* --- */


(function() {
  var simfStep = 1;
  var simfTotal = 6;
  window.simfNext = function() {
    simfStep++;
    var next = document.getElementById('simf-step-' + simfStep);
    if (next) { next.style.display = 'block'; next.scrollIntoView({behavior:'smooth', block:'nearest'}); }
    var btn = document.getElementById('simf-btn');
    if (simfStep >= simfTotal) {
      btn.style.display = 'none';
      document.getElementById('simf-done').style.display = 'block';
    } else {
      btn.textContent = '▶ Próximo Passo (' + (simfStep+1) + '/' + simfTotal + ')';
    }
  };
  window.updateDorScore = function(groupId) {
    var boxes = document.querySelectorAll('#' + groupId + ' input[type=checkbox]');
    var checked = 0;
    boxes.forEach(function(b){ if(b.checked) checked++; });
    var pct = Math.round(checked / boxes.length * 100);
    var scoreEl = document.getElementById(groupId + '-score');
    if (scoreEl) {
      if (pct === 100) {
        scoreEl.style.color = '#059669';
        scoreEl.textContent = 'DoR: 100% ✅ — passa para Ref. Técnico';
      } else {
        scoreEl.style.color = '#dc2626';
        scoreEl.textContent = 'DoR: ' + pct + '% ❌ — itens faltantes impedem avanço';
      }
    }
  };
})();


/* --- */


(function() {
  var simtStep = 1;
  var simtTotal = 5;
  window.simtNext = function() {
    simtStep++;
    var next = document.getElementById('simt-step-' + simtStep);
    if (next) { next.style.display = 'block'; next.scrollIntoView({behavior:'smooth', block:'nearest'}); }
    var btn = document.getElementById('simt-btn');
    if (simtStep >= simtTotal) {
      btn.style.display = 'none';
      document.getElementById('simt-done').style.display = 'block';
    } else {
      btn.textContent = '▶ Próximo Passo (' + (simtStep+1) + '/' + simtTotal + ')';
    }
  };
  window.updateDortScore = function() {
    var boxes = document.querySelectorAll('#dort-story-b input[type=checkbox]');
    var checked = 0;
    boxes.forEach(function(b){ if(b.checked) checked++; });
    var pct = Math.round(checked / boxes.length * 100);
    var scoreEl = document.getElementById('dort-score');
    if (scoreEl) {
      if (pct === 100) {
        scoreEl.style.color = '#059669';
        scoreEl.textContent = 'DoR Técnica: 100% ✅ — pronto para Aprovação PO';
      } else if (pct >= 70) {
        scoreEl.style.color = '#d97706';
        scoreEl.textContent = 'DoR Técnica: ' + pct + '% ⚠️ — pode avançar com pendências menores mapeadas';
      } else {
        scoreEl.style.color = '#dc2626';
        scoreEl.textContent = 'DoR Técnica: ' + pct + '% ❌ — não pode entrar em desenvolvimento';
      }
    }
  };
})();


/* --- */


function goTo(id, el) {
  const target = document.getElementById(id);
  if (!target) return;
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  target.classList.add('active');
  if (el) {
    el.classList.add('active');
    // Ensure the parent group is expanded and scroll the nav item into view
    const grpItems = el.closest('.nav-group-items');
    if (grpItems) {
      const grp = grpItems.closest('.nav-group');
      if (grp && grp.classList.contains('collapsed')) grp.classList.remove('collapsed');
      setGroupItemsHeight(grpItems);
    }
    setTimeout(() => el.scrollIntoView({block:'nearest', behavior:'smooth'}), 50);
  }
  window.scrollTo(0, 0);
}
function toggleGroup(id) {
  const grp = document.getElementById(id);
  if (!grp) return;
  grp.classList.toggle('collapsed');
  const items = grp.querySelector('.nav-group-items');
  if (items) setGroupItemsHeight(items);
}
function setGroupItemsHeight(items) {
  if (items.closest('.nav-group').classList.contains('collapsed')) {
    items.style.maxHeight = '0';
  } else {
    items.style.maxHeight = items.scrollHeight + 'px';
  }
}
function filterNav(q) {
  q = q.toLowerCase().trim();
  document.querySelectorAll('.nav-group').forEach(grp => {
    const items = grp.querySelectorAll('.nav-item');
    let anyVisible = false;
    items.forEach(item => {
      const match = !q || item.textContent.toLowerCase().includes(q);
      item.classList.toggle('hidden-search', !match);
      if (match) anyVisible = true;
    });
    grp.style.display = anyVisible ? '' : 'none';
    if (q && anyVisible) {
      grp.classList.remove('collapsed');
      const gi = grp.querySelector('.nav-group-items');
      if (gi) gi.style.maxHeight = gi.scrollHeight + 'px';
    }
  });
}
// Init: set max-heights for all groups
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-group-items').forEach(items => {
    items.style.maxHeight = items.scrollHeight + 'px';
  });
});
function switchPhase(prefix, idx, el) {
  const allBtns = el.parentElement.querySelectorAll('.phase-btn');
  allBtns.forEach(b => b.classList.remove('on'));
  el.classList.add('on');
  const section = el.closest('.section, .aggregated-part, .kb-page-content') || document;
  section.querySelectorAll('.phase-panel').forEach(p => p.classList.remove('on'));
  const target = document.getElementById(prefix + '-' + idx);
  if (target) target.classList.add('on');
}
function toggleAcc(header) { header.parentElement.classList.toggle('open'); }
function show(id, el) {
  const section = el.closest('.section, .aggregated-part, .kb-page-content') || document;
  section.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('on'));
  section.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('on'));
  const t = section.querySelector('#' + id);
  if(t) t.classList.add('on');
  el.classList.add('on');
}
function gDay(idx, btn) {
  document.querySelectorAll('.s-panel').forEach(p => p.classList.remove('s-on'));
  document.querySelectorAll('.day-btn').forEach(b => b.classList.remove('s-active'));
  document.getElementById('sd-' + idx).classList.add('s-on');
  btn.classList.add('s-active');
  const expProg = document.getElementById('sexp-prog');
  const prod = document.getElementById('s-prod-extra');
  if(expProg) expProg.innerHTML = '';
  if(prod) prod.innerHTML = '';
  const extrato = document.getElementById('st-extrato');
  const rate = document.getElementById('st-rate');
  if(extrato) { extrato.classList.toggle('s-hi', idx === 0); extrato.classList.toggle('s-done', idx >= 2); }
  if(rate) rate.classList.toggle('s-done', idx >= 1);
  if(idx === 0 && expProg) {
    expProg.innerHTML = '<div class="sk s-urg" style="border-color:#7c3aed"><span class="stag" style="color:#7c3aed">🚨 EXPEDITE</span>Bug cache token</div>';
  }
  if(idx >= 2 && prod) {
    let h = '<div class="sk s-done" style="border-color:#16a34a"><span class="stag" style="color:#16a34a">✓ DONE</span>Extrato Paginado</div>';
    if(idx >= 3) h += '<div class="sk s-done" style="border-color:#16a34a"><span class="stag" style="color:#16a34a">✓ DONE</span>Cursor encoding</div>';
    prod.innerHTML = h;
  }
}

/* =============================================
   PULL FLOW SIMULATION v4 — WIP respeitado end-to-end, backpressure em cascata
   ============================================= */
(function(){
  /* ── COLUMNS ── */
  /* zone:'up' = upstream (before commitment), zone:'down' = committed downstream */
  /* timed-queue = auto-drains to next col after deployMs; wipMax enforced everywhere */
  const COLS=[
    {id:'ideas',      label:'Ideias',           zone:'up',   type:'queue',       color:'#7c3aed'},
    {id:'backlog',    label:'Refinamento',       zone:'up',   type:'queue',       color:'#6d28d9'},
    {id:'ready',      label:'Pronto p/ Commit',  zone:'up',   type:'queue',       color:'#c2410c'},
    /* ← COMMITMENT POINT ← */
    {id:'dev',        label:'Em Dev',            zone:'down', type:'activity',    wipMax:3, color:'#6B7045'},
    {id:'wait_qa',    label:'Aguardando QA',      zone:'down', type:'queue',       wipMax:4, color:'#475569', isWait:true},
    {id:'qa',         label:'Em QA',             zone:'down', type:'activity',    wipMax:2, color:'#2E5E66'},
    {id:'deploy',     label:'Pronto Deploy',      zone:'down', type:'timed-queue', wipMax:3, deployMs:2500, color:'#334155'},
    {id:'delivered',  label:'✓ Entregue',         zone:'down', type:'done',        color:'#065f46'}
  ];

  /* ── WORKERS ── */
  const WORKERS=[
    {id:'dev1',label:'Dev 1',role:'dev',col:'dev', icon:'👩‍💻'},
    {id:'dev2',label:'Dev 2',role:'dev',col:'dev', icon:'👨‍💻'},
    {id:'dev3',label:'Dev 3',role:'dev',col:'dev', icon:'🧑‍💻'},
    {id:'qa1', label:'QA 1', role:'qa', col:'qa',  icon:'🔬'},
    {id:'qa2', label:'QA 2', role:'qa', col:'qa',  icon:'🧪'}
  ];

  const CC={expedite:'#C94040',fixed:'#D97706',standard:'#2E5E66',intangible:'#6B7045'};
  const CL={expedite:'EX',fixed:'FX',standard:'ST',intangible:'IN'};
  const WORK_MS={dev:4200,qa:3100};
  const REFINE_MS=3400; /* ms a card spends in backlog/refinamento before moving to ready */
  const MIN_QUEUE_DWELL=600; /* sim-ms a card must stay in queue before a worker can pull — scales with speedMult */

  let cards={},nextId=1,simRunning=false,speedMult=1,simStarted=false;
  let lastTick=0,spawnTimer=0,expTimer=0,statsTimer=0;
  let deliveredLog=[],tickCount=0,simStartReal=0;
  let wipMode='wip';

  /* ── HELPERS ── */
  function mkCard(cls){
    return{id:'c'+(nextId++),cls,col:'ideas',worker:null,workLeft:0,
           startMs:Date.now(),commitMs:null,doneMs:null,
           refineTimer:0,deployTimer:0,pendingPush:false,deliveredLogged:false,justMoved:false,arrivedAt:0};
  }
  function classRandom(){
    const r=Math.random();
    if(r<0.05)return'expedite';
    if(r<0.20)return'fixed';
    if(r<0.80)return'standard';
    return'intangible';
  }
  function inCol(colId,cls){return Object.values(cards).filter(c=>c.col===colId&&(!cls||c.cls===cls));}
  function wipActive(colId){return Object.values(cards).filter(c=>c.col===colId&&c.worker).length;}
  function expWip(){return Object.values(cards).filter(c=>c.cls==='expedite'&&!['ideas','backlog','delivered'].includes(c.col)).length;}
  function eid(id,v){const e=document.getElementById(id);if(e)e.textContent=v;}
  function fmtMs(ms){const s=Math.round(ms/1000);return s<60?s+'s':Math.round(s/60)+'m';}

  /* advance card to next col; returns true if moved */
  function advanceCard(c){
    const idx=COLS.findIndex(col=>col.id===c.col);
    if(idx<0||idx>=COLS.length-1)return false;
    c.col=COLS[idx+1].id;
    c.deployTimer=0;c.pendingPush=false;c.arrivedAt=tickCount;
    if(c.col==='delivered'&&!c.deliveredLogged){
      c.doneMs=Date.now();c.deliveredLogged=true;
      deliveredLog.push({ct:c.doneMs-(c.commitMs||c.startMs)});
    }
    return true;
  }

  /* check if the next col after cardCol is at its WIP limit */
  function nextColFull(cardCol){
    const idx=COLS.findIndex(c=>c.id===cardCol);
    if(idx<0||idx>=COLS.length-1)return false;
    const nxt=COLS[idx+1];
    if(!nxt.wipMax||wipMode==='chaos')return false;
    return inCol(nxt.id).length>=nxt.wipMax;
  }

  /* ── TICK ── */
  function tick(now){
    if(!simRunning)return;
    const dt=Math.min((now-lastTick)*speedMult,200);
    lastTick=now;tickCount+=dt;spawnTimer+=dt;expTimer+=dt;statsTimer+=dt;

    /* clear justMoved flags from last tick — cards are now eligible for worker pull */
    Object.values(cards).forEach(c=>{c.justMoved=false;});

    /* spawn */
    if(spawnTimer>(wipMode==='chaos'?1700:2900)){
      spawnTimer=0;
      const c=mkCard(classRandom());
      c.justMoved=true;c.arrivedAt=tickCount;
      if(c.cls==='expedite'){c.col='ready';c.commitMs=Date.now();}
      cards[c.id]=c;
    }
    if(expTimer>28000){
      expTimer=0;
      if(Math.random()<0.45){
        const c=mkCard('expedite');c.col='ready';c.commitMs=Date.now();c.justMoved=true;c.arrivedAt=tickCount;cards[c.id]=c;
      }
    }

    /* upstream auto-flow: ideas → backlog (skip cards that just spawned this tick) */
    const blMax=wipMode==='chaos'?99:3;
    if(inCol('backlog').length<blMax){
      const ic=inCol('ideas').filter(c=>!c.justMoved);
      if(ic.length>0){ic[0].col='backlog';ic[0].refineTimer=0;ic[0].arrivedAt=tickCount;ic[0].justMoved=true;}
    }
    /* backlog → ready (arrivedAt + justMoved ensure card is always visible before worker pulls) */
    const rdMax=wipMode==='chaos'?99:5;
    let rCount=inCol('ready').length;
    for(const c of inCol('backlog').filter(c=>!c.justMoved)){
      c.refineTimer+=dt;
      if(c.refineTimer>=REFINE_MS&&rCount<rdMax){c.col='ready';c.commitMs=Date.now();c.arrivedAt=tickCount;c.justMoved=true;rCount++;break;}
    }

    /* ── DEPLOY AUTO-DRAIN: cards in 'deploy' advance to 'delivered' after deployMs ── */
    const depColDef=COLS.find(c=>c.id==='deploy');
    for(const c of inCol('deploy')){
      c.deployTimer+=dt;
      if(c.deployTimer>=(depColDef.deployMs||2500)){advanceCard(c);break;}
    }

    /* ── RETRY pendingPush cards (one per tick) ── */
    for(const c of Object.values(cards).filter(x=>x.pendingPush)){
      if(!nextColFull(c.col)){advanceCard(c);break;}
    }

    /* ── WORKERS ── */
    WORKERS.forEach(w=>{
      const asgn=Object.values(cards).find(c=>c.worker===w.id);
      if(asgn){
        if(asgn.pendingPush)return; /* work done, stuck — skip */
        asgn.workLeft-=dt;
        if(asgn.workLeft<=0){
          asgn.worker=null;
          if(nextColFull(asgn.col)){
            asgn.pendingPush=true; /* finished but next col full → wait */
          } else {
            advanceCard(asgn);
          }
        }
      } else {
        const col=COLS.find(c=>c.id===w.col);
        if(!col||col.type!=='activity')return;
        const prevIdx=COLS.indexOf(col)-1;
        if(prevIdx<0)return;
        const prevId=COLS[prevIdx].id;
        /* WIP check uses TOTAL cards in col (includes pendingPush cards waiting to push out) */
        const colTot=inCol(w.col).length;
        if(wipMode==='wip'&&colTot>=col.wipMax)return;

        let target=null;
        const canPull=c=>!c.justMoved&&(tickCount-(c.arrivedAt||0))>=MIN_QUEUE_DWELL;
        const exps=inCol(prevId,'expedite').filter(canPull);
        if(exps.length>0){target=exps[0];} /* always pull expedite — wipMax on activity col already caps concurrency */
        else{
          for(const p of['fixed','standard','intangible']){
            const f=inCol(prevId,p).filter(canPull);if(f.length){target=f[0];break;}
          }
        }
        if(target){
          target.col=w.col;target.worker=w.id;
          const base=WORK_MS[w.col]||4000;
          target.workLeft=target.cls==='expedite'?base/1.7:base;
        }
      }
    });

    /* banners */
    const expW=expWip();
    const ob=document.getElementById('overflow-banner');
    if(ob)ob.style.display=expW>=2?'block':'none';

    if(statsTimer>500){statsTimer=0;updateStats();}
    render();
    requestAnimationFrame(tick);
  }

  /* ── STATS ── */
  function updateStats(){
    const all=Object.values(cards);
    const wip=all.filter(c=>['dev','wait_qa','qa','deploy'].includes(c.col)).length;
    eid('stat-wip',wip);
    eid('stat-delivered',all.filter(c=>c.col==='delivered').length);
    eid('stat-wait-qa',all.filter(c=>c.col==='wait_qa').length);
    eid('stat-exp-wip',expWip());
    if(deliveredLog.length>0){
      const del=all.filter(c=>c.col==='delivered').length;
      const cts=deliveredLog.map(d=>d.ct).sort((a,b)=>a-b);
      eid('stat-ct',fmtMs(cts[Math.floor(cts.length*.85)]));
      eid('stat-tp',del);
    }
  }

  /* ── RENDER COLUMN (returns HTML string) ── */
  function renderCol(col,all,chaos,colWorkers){
    colWorkers=colWorkers||[];
    const isFocused=COLS.findIndex(c=>c.id===col.id)===focusedColIdx;
    const exps=all.filter(c=>c.col===col.id&&c.cls==='expedite');
    const norms=all.filter(c=>c.col===col.id&&c.cls!=='expedite');
    const totInCol=exps.length+norms.length;
    /* WIP display: activity cols show active workers; queue cols show total */
    const wipDisplay=col.type==='activity'?wipActive(col.id):totInCol;
    const over=col.wipMax&&totInCol>col.wipMax;
    const hBg=chaos&&over?'#991b1b':col.color;
    const isTimed=col.type==='timed-queue';

    const borderClr=over?(chaos?'#ef4444':'#f97316'):isFocused?'#fbbf24':(chaos?'#4a1a1a':'#d1d5db');
    let h=`<div style="width:112px;flex-shrink:0;border-radius:6px;overflow:hidden;border:2px solid ${borderClr};display:flex;flex-direction:column;background:${chaos?'#0f0404':'#fff'};${isFocused?'box-shadow:0 0 0 3px rgba(251,191,36,.45),0 4px 18px rgba(251,191,36,.2);position:relative;z-index:2;':''}">`;

    /* header */
    h+=`<div style="background:${hBg};color:#fff;padding:5px 6px;font-size:9.5px;font-weight:800;text-align:center;line-height:1.35">`;
    h+=col.label;
    if(col.wipMax){
      const bbg=over?(chaos?'#ef4444':'#fef08a'):'rgba(255,255,255,.22)';
      const btxt=over?(chaos?'#fff':'#713f12'):'#fff';
      h+=`<br><span style="background:${bbg};color:${btxt};border-radius:3px;padding:0 4px;font-size:9px;font-weight:900">WIP:${wipDisplay}/${col.wipMax}${over?'⚠':''}</span>`;
    }
    if(col.isWait)h+=`<br><span style="font-size:8px;opacity:.8">⏸ aguarda pull</span>`;
    if(isTimed)h+=`<br><span style="font-size:8px;opacity:.8">🚀 auto-deploy</span>`;
    h+=`</div>`;

    /* helper: card html */
    function cardHtml(c,isEx){
      const pending=c.pendingPush;
      const bg=pending?(isEx?'#b45309':'#92400e'):(isEx?'#C94040':CC[c.cls]);
      const anim=isEx?';animation:wipPulse .8s infinite alternate':'';
      let ch=`<div style="background:${bg};color:#fff;border-radius:3px;margin:2px 0;padding:2px 5px;font-size:9px;font-weight:700;border:${pending?'1px dashed rgba(255,255,255,.7)':'none'}${anim}">`;
      ch+=`<div style="display:flex;align-items:center;gap:2px">`;
      ch+=`<span style="opacity:.85">${CL[c.cls]}</span><span style="opacity:.6;font-size:8px">${c.id}</span>`;
      ch+=c.worker?'<span title="em trabalho">⚙</span>':'';
      ch+=pending?'<span title="aguardando espaço">⏳</span>':'';
      ch+=`</div>`;
      /* deploy progress bar */
      if(isTimed&&(c.deployTimer||0)>0){
        const pct=Math.min(100,Math.round((c.deployTimer||0)/col.deployMs*100));
        ch+=`<div style="background:rgba(255,255,255,.2);height:3px;border-radius:2px;margin-top:2px;overflow:hidden"><div style="background:#fff;width:${pct}%;height:100%;border-radius:2px"></div></div>`;
      }
      ch+=`</div>`;
      return ch;
    }

    /* LANES: activity cols → EX + NORMAL split; queue cols → flat list (expedites stand out by color) */
    if(col.type==='activity'){
      /* expedite lane */
      h+=`<div style="background:${chaos?'#3b0808':'#fff5f5'};border-bottom:1px solid ${chaos?'#7f1d1d':'#fecaca'};padding:3px 3px 2px">`;
      h+=`<div style="font-size:8px;font-weight:800;color:#dc2626;margin-bottom:1px">🚨 EX LANE</div>`;
      if(!exps.length){
        h+=`<div style="height:16px;line-height:16px;text-align:center;font-size:9px;color:${chaos?'#6b2222':'#fca5a5'}">—</div>`;
      } else {
        exps.forEach(c=>{h+=cardHtml(c,true);});
      }
      h+=`</div>`;
      /* normal lane */
      h+=`<div style="background:${chaos?'#120303':'#fafafa'};padding:3px;flex:1;min-height:80px;max-height:200px;overflow-y:auto">`;
      h+=`<div style="font-size:8px;font-weight:700;color:${chaos?'#6b7280':'#94a3b8'};margin-bottom:2px">NORMAL</div>`;
      if(!norms.length){
        h+=`<div style="font-size:9px;color:${chaos?'#374151':'#cbd5e1'};text-align:center;padding:3px 0">vazia</div>`;
      } else {
        norms.forEach(c=>{h+=cardHtml(c,false);});
      }
      h+=`</div>`;
    } else {
      /* flat list — expedites highlighted by color, no dividers */
      h+=`<div style="background:${chaos?'#120303':'#fafafa'};padding:3px;flex:1;min-height:80px;max-height:200px;overflow-y:auto">`;
      if(!totInCol){
        h+=`<div style="font-size:9px;color:${chaos?'#374151':'#cbd5e1'};text-align:center;padding:6px 0">vazia</div>`;
      } else {
        exps.forEach(c=>{h+=cardHtml(c,true);});
        norms.forEach(c=>{h+=cardHtml(c,false);});
      }
      h+=`</div>`;
    }

    /* inline workers — rendered inside activity columns only */
    if(colWorkers.length){
      h+=`<div style="border-top:2px dashed ${chaos?'#4b5563':'#cbd5e1'};background:${chaos?'#0a0101':'#f8fafc'};padding:6px 3px 4px">`;
      h+=`<div style="font-size:7.5px;font-weight:800;color:${chaos?'#6b7280':'#94a3b8'};margin-bottom:3px;letter-spacing:.5px">⚙ WORKERS</div>`;
      colWorkers.forEach(w=>{
        const workCard=all.find(c=>c.worker===w.id);
        const busy=!!workCard;
        const blocked=!busy&&all.some(c=>c.pendingPush&&c.col===w.col);
        const wt=WORK_MS[w.col]||4000;
        const pct=busy?Math.max(0,Math.min(100,Math.round((1-workCard.workLeft/wt)*100))):0;
        const cBg=busy?(CC[workCard.cls]||'#6B7045'):blocked?(chaos?'#78350f':'#fef3c7'):(chaos?'#1f2937':'#f1f5f9');
        const cTxt=busy?'#fff':blocked?(chaos?'#fbbf24':'#92400e'):(chaos?'#6b7280':'#9ca3af');
        h+=`<div style="background:${cBg};color:${cTxt};border-radius:4px;padding:3px 4px;margin-bottom:2px;transition:background .35s">`;
        h+=`<div style="display:flex;align-items:center;gap:3px">`;
        h+=`<span style="font-size:13px;line-height:1">${w.icon}</span>`;
        h+=`<span style="font-size:9px;font-weight:800">${w.label}</span>`;
        h+=`</div>`;
        if(busy){
          h+=`<div style="font-size:8px;opacity:.85;margin:1px 0">${CL[workCard.cls]}·${workCard.id} ${pct}%</div>`;
          h+=`<div style="background:rgba(255,255,255,.2);height:3px;border-radius:2px;overflow:hidden">`;
          h+=`<div style="background:#fff;width:${pct}%;height:100%;transition:width .4s;border-radius:2px"></div></div>`;
        }else if(blocked){
          h+=`<div style="font-size:8px;font-weight:700">⏳ fila cheia</div>`;
        }else{
          h+=`<div style="font-size:8px;opacity:.55">💤 aguardando</div>`;
        }
        h+=`</div>`;
      });
      h+=`</div>`;
    }

    /* footer */
    h+=`<div style="text-align:center;font-size:8px;color:${chaos?'#6b7280':'#94a3b8'};padding:2px;background:${chaos?'#0a0202':'#f1f5f9'}">${totInCol} iten${totInCol!==1?'s':''}</div>`;
    h+=`</div>`;
    return h;
  }

  /* ── RENDER WORKERS ── */
  function renderWorkers(all,chaos){
    const wp=document.getElementById('sim-workers');
    if(!wp)return;
    const groups=[
      {label:'👩‍💻 Dev Team',role:'dev',ws:WORKERS.filter(w=>w.role==='dev')},
      {label:'🔬 QA Team', role:'qa', ws:WORKERS.filter(w=>w.role==='qa')}
    ];
    let h=`<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:14px">`;
    h+=`<div style="width:100%;font-size:11px;font-weight:800;color:${chaos?'#9ca3af':'#475569'};margin-bottom:2px;letter-spacing:.5px">⚙ WORKERS</div>`;
    groups.forEach(g=>{
      const rBg=chaos?'#120303':(g.role==='dev'?'#f0fdf4':'#f0fdfa');
      const rBdr=chaos?'#374151':(g.role==='dev'?'#86efac':'#99f6e4');
      const rClr=g.role==='dev'?'#065f46':'#0f766e';
      h+=`<div style="background:${rBg};border:2px solid ${rBdr};border-radius:10px;padding:10px 12px;flex:1;min-width:190px">`;
      h+=`<div style="font-size:10px;font-weight:800;color:${chaos?'#9ca3af':rClr};margin-bottom:8px;letter-spacing:.3px">${g.label}</div>`;
      h+=`<div style="display:flex;gap:7px;flex-wrap:wrap">`;
      g.ws.forEach(w=>{
        const workCard=all.find(c=>c.worker===w.id);
        const busy=!!workCard;
        const blocked=!busy&&all.some(c=>c.pendingPush&&c.col===w.col);
        const wt=WORK_MS[w.col]||4000;
        const pct=busy?Math.max(0,Math.min(100,Math.round((1-workCard.workLeft/wt)*100))):0;
        const cBg=busy?(CC[workCard.cls]||'#6B7045'):blocked?(chaos?'#78350f':'#fef3c7'):(chaos?'#1f2937':'#f3f4f6');
        const cTxt=busy?'#fff':blocked?(chaos?'#fbbf24':'#92400e'):(chaos?'#6b7280':'#9ca3af');
        h+=`<div style="background:${cBg};color:${cTxt};border-radius:9px;padding:9px 11px;min-width:86px;max-width:110px;transition:background .35s;box-shadow:0 1px 3px rgba(0,0,0,.12)">`;
        h+=`<div style="font-size:20px;margin-bottom:3px;line-height:1">${w.icon}</div>`;
        h+=`<div style="font-size:11px;font-weight:800;margin-bottom:2px">${w.label}</div>`;
        if(busy){
          h+=`<div style="font-size:10px;opacity:.9;margin-bottom:4px">${CL[workCard.cls]} · ${workCard.id}</div>`;
          h+=`<div style="background:rgba(255,255,255,.2);height:5px;border-radius:3px;overflow:hidden;margin-bottom:3px">`;
          h+=`<div style="background:#fff;height:100%;width:${pct}%;transition:width .35s;border-radius:3px"></div>`;
          h+=`</div>`;
          h+=`<div style="font-size:9px;color:rgba(255,255,255,.75)">⚙ ${pct}% concluído</div>`;
        } else if(blocked){
          h+=`<div style="font-size:9px;font-weight:700;margin-top:4px">⏳ bloqueado</div>`;
          h+=`<div style="font-size:8px;opacity:.7;margin-top:2px">fila cheia</div>`;
          h+=`<div style="background:rgba(0,0,0,.12);height:5px;border-radius:3px;margin-top:5px"></div>`;
        } else {
          h+=`<div style="font-size:9px;opacity:.5;margin-top:4px">💤 aguardando</div>`;
          h+=`<div style="background:rgba(0,0,0,.07);height:5px;border-radius:3px;margin-top:6px"></div>`;
        }
        h+=`</div>`;
      });
      h+=`</div></div>`;
    });
    h+=`</div>`;
    wp.innerHTML=h;
  }

  /* ── RENDER BOARD ── */
  function render(){
    const board=document.getElementById('sim-board');
    if(!board)return;
    const all=Object.values(cards);
    const chaos=wipMode==='chaos';

    const upCols=COLS.filter(c=>c.zone==='up');
    const dnCols=COLS.filter(c=>c.zone==='down');

    /* workers map: colId → [worker objects] for inline rendering */
    const workersMap={};
    WORKERS.forEach(w=>{if(!workersMap[w.col])workersMap[w.col]=[];workersMap[w.col].push(w);});

    const COLW=112; /* column width px */
    let html=`<div style="overflow-x:auto;padding-bottom:4px">`;

    /* zone labels row */
    html+=`<div style="display:flex;gap:0;margin-bottom:6px;align-items:stretch">`;
    /* upstream label */
    const upW=upCols.length*COLW+(upCols.length-1)*4+24; /* cols×width + gaps + padding */
    html+=`<div style="width:${upW}px;flex-shrink:0;text-align:center;font-size:10px;font-weight:800;color:${chaos?'#a78bfa':'#6d28d9'};background:${chaos?'rgba(109,40,217,.12)':'#f5f3ff'};padding:4px 6px;border-radius:4px 0 0 4px;border:1px solid ${chaos?'#6d28d9':'#ddd6fe'}">🔍 UPSTREAM — Antes do Compromisso</div>`;
    /* commit point label */
    html+=`<div style="width:72px;flex-shrink:0;background:${chaos?'#7f1d1d':'#c2410c'};border-radius:0"></div>`;
    /* downstream label */
    const dnW=dnCols.length*COLW+(dnCols.length-1)*4+24;
    html+=`<div style="width:${dnW}px;flex-shrink:0;text-align:center;font-size:10px;font-weight:800;color:${chaos?'#6ee7b7':'#065f46'};background:${chaos?'rgba(6,95,70,.12)':'#f0fdf4'};padding:4px 6px;border-radius:0 4px 4px 0;border:1px solid ${chaos?'#065f46':'#bbf7d0'}">⚡ DOWNSTREAM — Fluxo Comprometido</div>`;
    html+=`</div>`;

    /* board row */
    html+=`<div style="display:flex;gap:0;align-items:stretch">`;

    /* upstream zone */
    html+=`<div style="display:flex;gap:4px;background:${chaos?'#160a2e':'#f5f3ff'};border:2px solid ${chaos?'#6d28d9':'#c4b5fd'};border-radius:8px 0 0 8px;padding:10px">`;
    upCols.forEach(col=>{html+=renderCol(col,all,chaos,workersMap[col.id]||[]);});
    html+=`</div>`;

    /* commitment point pillar — wider and more prominent */
    html+=`<div title="Ponto de Compromisso: a partir daqui o time se compromete a entregar o item" style="width:72px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:${chaos?'#7f1d1d':'#c2410c'};gap:6px;cursor:help">`;
    html+=`<span style="color:rgba(255,255,255,.95);font-size:22px;line-height:1">▶</span>`;
    html+=`<span style="writing-mode:vertical-rl;font-size:10px;font-weight:900;color:#fff;letter-spacing:2.5px;text-transform:uppercase">Compromisso</span>`;
    html+=`<span style="writing-mode:vertical-rl;font-size:8px;color:rgba(255,255,255,.65);letter-spacing:1px">comprometidos →</span>`;
    html+=`<span style="color:rgba(255,255,255,.95);font-size:22px;line-height:1">▶</span>`;
    html+=`</div>`;

    /* downstream zone */
    html+=`<div style="display:flex;gap:4px;background:${chaos?'#160404':'#f0fdf4'};border:2px solid ${chaos?'#7f1d1d':'#86efac'};border-left:none;border-radius:0 8px 8px 0;padding:10px">`;
    dnCols.forEach(col=>{html+=renderCol(col,all,chaos,workersMap[col.id]||[]);});
    html+=`</div>`;

    html+=`</div>`; /* board row */
    html+=`</div>`; /* overflow wrapper */

    board.innerHTML=html;
    /* workers are now rendered inline inside each activity column — no separate panel needed */
  }

  /* ── INIT ── */
  function simInit(){
    if(simStarted)return;
    simStarted=true;
    for(let i=0;i<7;i++){const c=mkCard(classRandom());c.arrivedAt=-9999;cards[c.id]=c;}
    /* seed one expedite already in ready */
    const ex=mkCard('expedite');ex.col='ready';ex.commitMs=Date.now();ex.arrivedAt=-9999;cards[ex.id]=ex;
    simRunning=true;lastTick=performance.now();simStartReal=Date.now();
    requestAnimationFrame(tick);
    setTimeout(()=>{scrollToFocused();updateNavUI();},80);
  }

  /* ── PUBLIC API ── */
  window.simToggle=function(){
    simRunning=!simRunning;
    const btn=document.getElementById('sim-btn-pause');
    if(btn)btn.textContent=simRunning?'⏸ Pausar':'▶ Retomar';
    if(simRunning){lastTick=performance.now();requestAnimationFrame(tick);}
  };

  window.simReset=function(){
    simRunning=false;cards={};nextId=1;deliveredLog=[];tickCount=0;simStartReal=0;
    spawnTimer=0;expTimer=0;statsTimer=0;simStarted=false;focusedColIdx=0;
    const btn=document.getElementById('sim-btn-pause');
    if(btn)btn.textContent='⏸ Pausar';
    ['stat-delivered','stat-wip','stat-ct','stat-tp','stat-exp-wip','stat-wait-qa'].forEach(id=>{
      const e=document.getElementById(id);if(e)e.textContent='0';
    });
    const ob=document.getElementById('overflow-banner');if(ob)ob.style.display='none';
    const brd=document.getElementById('sim-board');if(brd)brd.innerHTML='';
    const wp=document.getElementById('sim-workers');if(wp)wp.innerHTML='';
    setTimeout(simInit,100);
  };

  window.simInjectExpedite=function(){
    const c1=mkCard('expedite');c1.col='ready';c1.commitMs=Date.now();cards[c1.id]=c1;
    const c2=mkCard('expedite');c2.col='ready';c2.commitMs=Date.now();cards[c2.id]=c2;
    if(!simRunning){simRunning=true;lastTick=performance.now();requestAnimationFrame(tick);}
  };

  window.simSetSpeed=function(v){speedMult=parseFloat(v);};

  window.simSetMode=function(mode){
    wipMode=mode;
    const bw=document.getElementById('btn-mode-wip');
    const bc=document.getElementById('btn-mode-chaos');
    const cb=document.getElementById('chaos-banner');
    if(mode==='wip'){
      if(bw){bw.style.background='#065f46';bw.style.color='#fff';}
      if(bc){bc.style.background='#f1f5f9';bc.style.color='#64748b';}
      if(cb)cb.style.display='none';
    } else {
      if(bc){bc.style.background='#991b1b';bc.style.color='#fff';}
      if(bw){bw.style.background='#f1f5f9';bw.style.color='#64748b';}
      if(cb)cb.style.display='block';
      for(let i=0;i<4;i++){const c=mkCard(classRandom());cards[c.id]=c;}
    }
    if(!simRunning){simRunning=true;lastTick=performance.now();requestAnimationFrame(tick);}
  };

  /* ── COLUMN NAVIGATION ── */
  let focusedColIdx=0;
  const COL_DESC={
    ideas:   {emoji:'💡',desc:'Cards chegam aqui como ideias brutas. Não refinadas, não comprometidas. O upstream existe para desacoplar a chegada de demanda do comprometimento — o time decide quando há capacidade.'},
    backlog: {emoji:'🔍',desc:'Refinamento ativo: análise, estimativas, critérios de aceite. Um card só sai daqui quando o time tem confiança suficiente para comprometer. O timer de refinamento (REFINE_MS) controla o tempo mínimo aqui.'},
    ready:   {emoji:'✅',desc:'Pronto para cruzar o Ponto de Compromisso. Workers do downstream puxam daqui. <strong>Este é o buffer de regulação</strong>: se encher, o sistema sinaliza para parar de refinar upstream.'},
    dev:     {emoji:'👩‍💻',desc:'Em desenvolvimento ativo. <strong>WIP:3</strong> — no máximo 3 itens simultâneos. Workers puxam de "Pronto p/ Commit". Expedites têm raia separada e são sempre priorizados. Quando cheio, cria backpressure para upstream.'},
    wait_qa: {emoji:'⏸',desc:'Fila de espera antes do QA. Acúmulo aqui é sinal de gargalo: QA está sobrecarregado ou mais lento que Dev. <strong>Esta é a coluna mais importante para monitorar</strong> — é onde a Flow Efficiency costuma colapsar.'},
    qa:      {emoji:'🔬',desc:'Validação de qualidade. <strong>WIP:2</strong> garante foco. Workers de QA puxam desta fila. Expedites têm raia separada e saem 1.7× mais rápido. Quando QA está cheio, Dev deve ajudar — não puxar item novo.'},
    deploy:  {emoji:'🚀',desc:'Validado, aguardando janela de deploy. <strong>Auto-drena para Entregue</strong> após ~2.5s de sim-time (simula CI/CD). WIP:3 garante que não acumule indefinidamente. Em times maduros, este passo é automático.'},
    delivered:{emoji:'✓', desc:'Item entregue e contabilizado. Cycle Time registrado, P85 calculado, Throughput incrementado. <strong>Lei de Little</strong>: tudo que aparece aqui mais rápido = WIP menor ou Throughput maior.'}
  };

  function scrollToFocused(){
    const board=document.getElementById('sim-board');
    if(!board)return;
    const inner=board.firstElementChild;
    if(!inner)return;
    const COLW=112,GAP=4,PAD=12,COMMIT=72,BDR=4;
    const upCount=COLS.filter(c=>c.zone==='up').length;
    const i=focusedColIdx;
    /* x = left edge of focused column inside the scrollable inner div */
    const x=i<upCount
      ? BDR+PAD+i*(COLW+GAP)
      : BDR+PAD+upCount*(COLW+GAP)+COMMIT+BDR+PAD+(i-upCount)*(COLW+GAP);
    /* center it in the board viewport */
    inner.scrollTo({left:x-(board.clientWidth-COLW)/2,behavior:'smooth'});
  }

  function updateNavUI(){
    const col=COLS[focusedColIdx];
    const info=COL_DESC[col.id]||{emoji:'',desc:col.label};
    const isUp=col.zone==='up';
    /* indicator bar */
    const ind=document.getElementById('sim-col-indicator');
    if(ind){
      ind.innerHTML=`<span style="font-weight:800;color:#1e293b;font-size:13px">${info.emoji} ${col.label}</span>&nbsp;&nbsp;<span style="color:#94a3b8;font-size:11px">${focusedColIdx+1} / ${COLS.length}</span>`;
      ind.style.background=isUp?'#f5f3ff':'#f0fdf4';
      ind.style.borderColor=isUp?'#c4b5fd':'#86efac';
    }
    /* description */
    const desc=document.getElementById('sim-col-desc');
    if(desc){
      desc.style.display='block';
      desc.innerHTML=`<strong style="color:#1e293b">${info.emoji} ${col.label}</strong> — ${info.desc}`;
      desc.style.borderLeftColor=col.color||'#334155';
    }
    /* nav arrows opacity */
    const prev=document.getElementById('sim-nav-prev');
    const next=document.getElementById('sim-nav-next');
    if(prev)prev.style.opacity=focusedColIdx>0?'1':'0.3';
    if(next)next.style.opacity=focusedColIdx<COLS.length-1?'1':'0.3';
  }

  window.simNavPrev=function(){
    if(focusedColIdx>0){focusedColIdx--;scrollToFocused();updateNavUI();render();}
  };
  window.simNavNext=function(){
    if(focusedColIdx<COLS.length-1){focusedColIdx++;scrollToFocused();updateNavUI();render();}
  };

  /* keyboard navigation when this section is visible */
  document.addEventListener('keydown',function(e){
    if(!section||!section.classList.contains('active'))return;
    if(e.key==='ArrowRight'){e.preventDefault();window.simNavNext();}
    if(e.key==='ArrowLeft'){e.preventDefault();window.simNavPrev();}
  });

  window.simScenario=function(n){
    simReset();
    const hints=[
      '<strong>🟢 Cenário 1 — Fluxo Saudável</strong><br>📌 <strong>O que observar:</strong> WIP limits criam backpressure natural. Quando "Em Dev" atinge o limite, novos cards aguardam em "Pronto p/ Commit". O Cycle Time se estabiliza. Workers bloqueados (⏳) sinalizam o gargalo — corrija o gargalo, não aumente o WIP.',
      '<strong>🚨 Cenário 2 — Expedite Entra</strong><br>📌 <strong>O que observar:</strong> Em ~4 segundos, dois expedites entrarão na fila. Workers os priorizarão automaticamente — eles chegam à entrega muito mais rápido que os normais. Este é o custo intencional do expedite: interrompe o fluxo padrão e eleva o cycle time dos demais itens.',
      '<strong>🔥 Cenário 3 — Caos sem WIP</strong><br>📌 <strong>O que observar:</strong> Sem limites de WIP, workers puxam tudo ao mesmo tempo. O WIP downstream explode. Acompanhe o <strong>Cycle Time P85</strong> na barra de stats — vai disparar em segundos. <strong>Lei de Little em ação:</strong> Lead Time = WIP ÷ Throughput.'
    ];
    [1,2,3].forEach(i=>{
      const b=document.getElementById('btn-cenario-'+i);
      if(b){
        b.style.opacity=i===n?'1':'0.55';
        b.style.boxShadow=i===n?'0 0 0 3px rgba(255,255,255,.4) inset':'none';
      }
    });
    const hd=document.getElementById('cenario-hint');
    if(hd){hd.style.display='block';hd.innerHTML=hints[n-1];}
    if(n===3){setTimeout(()=>simSetMode('chaos'),250);}
    if(n===2){setTimeout(()=>{simInjectExpedite();},4000);}
  };

  /* auto-start when section becomes visible */
  const section=document.getElementById('s-scrumban-simulacao');
  if(section){
    const obs=new MutationObserver(ms=>{
      ms.forEach(m=>{if(m.attributeName==='class'&&section.classList.contains('active'))simInit();});
    });
    obs.observe(section,{attributes:true});
    if(section.classList.contains('active'))simInit();
  }
})();


/* --- */


(function(){
  /* ── Monte Carlo Simulation ── */
  window.runMonteCarlo = function() {
    const inputs = Array.from(document.querySelectorAll('#s-elite-tamanho .mc-val'));
    const history = inputs.map(i => parseInt(i.value) || 0).filter(v => v >= 0);
    const target = parseInt(document.getElementById('mc-target').value) || 20;
    if(history.length === 0) return;

    const N = 10000;
    const sprintCounts = [];

    for(let sim = 0; sim < N; sim++){
      let total = 0, sprints = 0;
      while(total < target){
        const idx = Math.floor(Math.random() * history.length);
        total += history[idx];
        sprints++;
        if(sprints > 500) break; // safety
      }
      sprintCounts.push(sprints);
    }

    sprintCounts.sort((a,b) => a-b);
    const p50 = sprintCounts[Math.floor(N*0.50)];
    const p75 = sprintCounts[Math.floor(N*0.75)];
    const p85 = sprintCounts[Math.floor(N*0.85)];
    const p95 = sprintCounts[Math.floor(N*0.95)];

    const daysPerSprint = 10;
    const sprintDays = 15;

    // Build result HTML
    const resultDiv = document.getElementById('mc-result');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
      <div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border-radius:10px;padding:20px;border:1px solid #86efac;">
        <div style="font-weight:700;color:#166534;margin-bottom:4px;font-size:1rem;">🎲 Resultado: Para entregar <strong>${target} itens</strong>...</div>
        <p style="color:#166534;font-size:.85rem;margin:0 0 16px;">Baseado em ${N.toLocaleString()} simulações com seu histórico de ${history.length} iterações.</p>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin-bottom:16px;">
          <div style="background:#ffffff90;border-radius:8px;padding:14px;text-align:center;">
            <div style="font-size:.7rem;color:#166534;font-weight:600;text-transform:uppercase;margin-bottom:4px;">P50 — Otimista</div>
            <div style="font-size:2rem;font-weight:800;color:#166534;">${p50}</div>
            <div style="font-size:.75rem;color:#166534;">iteraç${p50>1?'ões':'ão'} ≈ ${Math.round(p50*sprintDays/daysPerSprint)}sem</div>
            <div style="font-size:.7rem;color:#4ade80;margin-top:4px;">50% de chance</div>
          </div>
          <div style="background:#ffffff90;border-radius:8px;padding:14px;text-align:center;">
            <div style="font-size:.7rem;color:#166534;font-weight:600;text-transform:uppercase;margin-bottom:4px;">P75 — Realista</div>
            <div style="font-size:2rem;font-weight:800;color:#166534;">${p75}</div>
            <div style="font-size:.75rem;color:#166534;">iteraç${p75>1?'ões':'ão'} ≈ ${Math.round(p75*sprintDays/daysPerSprint)}sem</div>
            <div style="font-size:.7rem;color:#4ade80;margin-top:4px;">75% de chance</div>
          </div>
          <div style="background:#3b82f620;border:2px solid #3b82f6;border-radius:8px;padding:14px;text-align:center;">
            <div style="font-size:.7rem;color:#1e40af;font-weight:700;text-transform:uppercase;margin-bottom:4px;">⭐ P85 — Recomendado</div>
            <div style="font-size:2rem;font-weight:800;color:#1e40af;">${p85}</div>
            <div style="font-size:.75rem;color:#1e40af;">iteraç${p85>1?'ões':'ão'} ≈ ${Math.round(p85*sprintDays/daysPerSprint)}sem</div>
            <div style="font-size:.75rem;color:#3b82f6;margin-top:4px;font-weight:600;">85% de chance</div>
          </div>
          <div style="background:#ffffff90;border-radius:8px;padding:14px;text-align:center;">
            <div style="font-size:.7rem;color:#166534;font-weight:600;text-transform:uppercase;margin-bottom:4px;">P95 — Conservador</div>
            <div style="font-size:2rem;font-weight:800;color:#166534;">${p95}</div>
            <div style="font-size:.75rem;color:#166534;">iteraç${p95>1?'ões':'ão'} ≈ ${Math.round(p95*sprintDays/daysPerSprint)}sem</div>
            <div style="font-size:.7rem;color:#4ade80;margin-top:4px;">95% de chance</div>
          </div>
        </div>
        <div style="background:#ffffff70;border-radius:8px;padding:12px;font-size:.85rem;color:#166534;">
          💬 <strong>Script para stakeholders:</strong> "Com 85% de confiança, entregamos os ${target} itens em ${p85} iteraç${p85>1?'ões':'ão'} de 15 dias — isso é ${Math.round(p85*sprintDays/7)} semanas. Se priorizarmos os itens críticos e mantivermos o fluxo estável, podemos melhorar para ${p75} iterações."
        </div>
      </div>`;

    // Stats
    const avg = (history.reduce((a,b)=>a+b,0)/history.length).toFixed(1);
    const sorted = [...history].sort((a,b)=>a-b);
    const sMin = sorted[0], sMax = sorted[sorted.length-1];
    const sP85th = sorted[Math.min(Math.floor(sorted.length*0.85), sorted.length-1)];
    const statsDiv = document.getElementById('mc-stats');
    const statsContent = document.getElementById('mc-stats-content');
    statsDiv.style.display = 'block';
    statsContent.innerHTML = `
      <span style="background:#e0f2fe;color:#0c4a6e;padding:5px 12px;border-radius:20px;font-size:.82rem;font-weight:600;">Mín: ${sMin} itens/sprint</span>
      <span style="background:#e0f2fe;color:#0c4a6e;padding:5px 12px;border-radius:20px;font-size:.82rem;font-weight:600;">Máx: ${sMax} itens/sprint</span>
      <span style="background:#e0f2fe;color:#0c4a6e;padding:5px 12px;border-radius:20px;font-size:.82rem;font-weight:600;">Média: ${avg} itens/sprint</span>
      <span style="background:#bfdbfe;color:#1e40af;padding:5px 12px;border-radius:20px;font-size:.82rem;font-weight:700;">P85: ${sP85th} itens/sprint (use para SLA)</span>
      <span style="background:${sMax-sMin>4?'#fee2e2':'#dcfce7'};color:${sMax-sMin>4?'#991b1b':'#166534'};padding:5px 12px;border-radius:20px;font-size:.82rem;font-weight:600;">Variação: ${sMax-sMin} itens (${sMax-sMin>4?'alta — uniformize tamanhos':'ok — fluxo estável'})</span>`;
  };

  /* ── Checklist interativo ── */
  document.addEventListener('change', function(e){
    if(!e.target.closest('#replen-check')) return;
    const checks = document.querySelectorAll('#s-elite-tamanho #replen-check input[type=checkbox]');
    const checked = Array.from(checks).filter(c=>c.checked).length;
    const score = document.getElementById('replen-score');
    if(checked > 0){
      score.style.display = 'block';
      const msgs = ['','','','','', '🔍 Quase lá — 1 item restante para confirmar!','✅ 6/6 — Demanda pronta para entrar na iteração!'];
      const colors = ['','','','','','#fef3c7','#dcfce7'];
      const textColors = ['','','','','','#92400e','#166534'];
      score.style.background = colors[checked] || '#dcfce7';
      score.style.color = textColors[checked] || '#166534';
      score.textContent = msgs[checked] || `✅ ${checked}/6 checado${checked>1?'s':''}`;
    } else {
      score.style.display = 'none';
    }
  });
})();

window.showSplit = function(id) {
    for(let i=1; i<=5; i++) {
        const content = document.getElementById('split-s' + i);
        const btn = document.getElementById('st-s' + i);
        if(content && btn) {
            if('s' + i === id) {
                content.style.display = 'block';
                btn.style.background = '#4c1d95';
                btn.style.color = '#fff';
            } else {
                content.style.display = 'none';
                btn.style.background = '#e2e8f0';
                btn.style.color = '#475569';
            }
        }
    }
};
