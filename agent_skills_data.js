const agentSkillsData = {
    "Agent Skills": [
        {
            "id": "agent_skill_api-and-interface-design",
            "title": "Design de API e Interface",
            "path": "agent-skills/skills/api-and-interface-design/SKILL.md",
            "description": "Guia o design de interfaces e APIs estáveis. Use ao projetar APIs, limites de módulos ou qualquer interface pública. Use ao criar endpoints REST ou GraphQL, definir contratos de tipo entre módulos ou estabelecer limites entre frontend e backend."
        },
        {
            "id": "agent_skill_browser-testing-with-devtools",
            "title": "Testes de Navegador com Devtools",
            "path": "agent-skills/skills/browser-testing-with-devtools/SKILL.md",
            "description": "Testa em navegadores reais via Chrome DevTools MCP. Use ao construir ou depurar algo que roda em um navegador. Use quando precisar inspecionar o DOM, capturar erros de console, analisar requisições de rede, traçar perfil de desempenho ou verificar a saída visual com dados reais em tempo de execução."
        },
        {
            "id": "agent_skill_ci-cd-and-automation",
            "title": "CI/CD e Automação",
            "path": "agent-skills/skills/ci-cd-and-automation/SKILL.md",
            "description": "Automatiza a configuração de pipelines de CI/CD. Use ao configurar ou modificar pipelines de build e implantação. Use quando precisar automatizar portões de qualidade, configurar executores de teste em CI ou estabelecer estratégias de implantação."
        },
        {
            "id": "agent_skill_code-review-and-quality",
            "title": "Revisão de Código e Qualidade",
            "path": "agent-skills/skills/code-review-and-quality/SKILL.md",
            "description": "Garante a qualidade do código através de revisões rigorosas. Use ao finalizar uma tarefa, revisar um PR ou auditar uma base de código. Foca em legibilidade, manutenibilidade, segurança e alinhamento com padrões do projeto."
        },
        {
            "id": "agent_skill_code-simplification",
            "title": "Simplificação de Código",
            "path": "agent-skills/skills/code-simplification/SKILL.md",
            "description": "Reduz a complexidade e melhora a clareza do código. Use ao refatorar código legado, simplificar lógicas condicionais aninhadas, remover código morto ou quando o código atual estiver muito difícil de ler ou manter."
        },
        {
            "id": "agent_skill_context-engineering",
            "title": "Engenharia de Contexto",
            "path": "agent-skills/skills/context-engineering/SKILL.md",
            "description": "Gerencia e otimiza o contexto fornecido para modelos de IA. Use para evitar perda de contexto, resumir informações extensas, selecionar arquivos relevantes e garantir que os prompts contenham exatamente o necessário para a tarefa."
        },
        {
            "id": "agent_skill_debugging-and-error-recovery",
            "title": "Depuração e Recuperação de Erros",
            "path": "agent-skills/skills/debugging-and-error-recovery/SKILL.md",
            "description": "Investiga e resolve falhas de forma sistemática. Use ao enfrentar bugs complexos, falhas em produção, mensagens de erro misteriosas ou comportamento inesperado no sistema. Foca em encontrar a causa raiz antes de aplicar soluções."
        },
        {
            "id": "agent_skill_deprecation-and-migration",
            "title": "Depreciação e Migração",
            "path": "agent-skills/skills/deprecation-and-migration/SKILL.md",
            "description": "Gerencia a transição e descontinuidade de código e sistemas antigos. Use ao migrar para novas APIs, atualizar versões principais de dependências ou remover código legado de forma segura sem quebrar clientes existentes."
        },
        {
            "id": "agent_skill_documentation-and-adrs",
            "title": "Documentação e ADRs",
            "path": "agent-skills/skills/documentation-and-adrs/SKILL.md",
            "description": "Registra decisões e documentação técnica. Use ao tomar decisões arquiteturais, alterar APIs públicas, lançar funcionalidades ou quando precisar registrar o contexto para que futuros engenheiros e agentes entendam a base de código."
        },
        {
            "id": "agent_skill_doubt-driven-development",
            "title": "Desenvolvimento Guiado por Dúvidas",
            "path": "agent-skills/skills/doubt-driven-development/SKILL.md",
            "description": "Submete cada decisão não trivial a uma revisão adversária com contexto fresco antes de ser mantida. Use quando a exatidão importa mais que a velocidade, ao trabalhar em código desconhecido ou operações sensíveis."
        },
        {
            "id": "agent_skill_frontend-ui-engineering",
            "title": "Engenharia de UI Frontend",
            "path": "agent-skills/skills/frontend-ui-engineering/SKILL.md",
            "description": "Constrói interfaces de usuário voltadas à produção, acessíveis e responsivas. Use ao construir ou modificar páginas, criar componentes, implementar layouts, cumprir requisitos de acessibilidade WCAG ou gerenciar estado."
        },
        {
            "id": "agent_skill_git-workflow-and-versioning",
            "title": "Fluxo de Trabalho Git e Versionamento",
            "path": "agent-skills/skills/git-workflow-and-versioning/SKILL.md",
            "description": "Estrutura as práticas de fluxo de trabalho no Git. Use ao fazer qualquer alteração de código. Use ao fazer commit, criar branch, resolver conflitos ou organizar trabalho em fluxos paralelos, além de cortes de versão."
        },
        {
            "id": "agent_skill_idea-refine",
            "title": "Refinamento de Ideias",
            "path": "agent-skills/skills/idea-refine/SKILL.md",
            "description": "Refina ideias brutas em conceitos claros e acionáveis através de pensamento estruturado divergente e convergente. Use quando uma ideia ainda é vaga ou quando precisa testar premissas antes de se comprometer com um plano."
        },
        {
            "id": "agent_skill_incremental-implementation",
            "title": "Implementação Incremental",
            "path": "agent-skills/skills/incremental-implementation/SKILL.md",
            "description": "Entrega alterações de forma incremental. Use ao implementar qualquer funcionalidade ou alteração que toque mais de um arquivo. Use quando estiver prestes a escrever muito código de uma vez ou a tarefa parecer muito grande."
        },
        {
            "id": "agent_skill_interview-me",
            "title": "Entreviste-me",
            "path": "agent-skills/skills/interview-me/SKILL.md",
            "description": "Extrai o que o usuário realmente quer em vez do que ele acha que deve querer. Usa entrevistas de uma pergunta por vez para atingir 95% de confiança sobre a intenção antes de criar planos, especificações ou código."
        },
        {
            "id": "agent_skill_observability-and-instrumentation",
            "title": "Observabilidade e Instrumentação",
            "path": "agent-skills/skills/observability-and-instrumentation/SKILL.md",
            "description": "Instrumenta o código para que o comportamento em produção seja visível e diagnosticável. Use ao adicionar logs, métricas, rastreamento ou alertas, e ao precisar de evidências para debugar problemas em produção."
        },
        {
            "id": "agent_skill_performance-optimization",
            "title": "Otimização de Desempenho",
            "path": "agent-skills/skills/performance-optimization/SKILL.md",
            "description": "Otimiza o desempenho da aplicação no frontend, backend, consultas e bancos de dados. Use quando existirem requisitos de desempenho, gargalos forem identificados em perfis ou padrões de consulta N+1 precisarem de correção."
        },
        {
            "id": "agent_skill_planning-and-task-breakdown",
            "title": "Planejamento e Desdobramento de Tarefas",
            "path": "agent-skills/skills/planning-and-task-breakdown/SKILL.md",
            "description": "Quebra o trabalho em tarefas ordenadas. Use quando tiver uma especificação ou requisitos claros e precisar dividir o trabalho em tarefas implementáveis, estimar escopo ou paralelizá-lo."
        },
        {
            "id": "agent_skill_security-and-hardening",
            "title": "Segurança e Hardening",
            "path": "agent-skills/skills/security-and-hardening/SKILL.md",
            "description": "Fortalece o código contra vulnerabilidades. Use ao lidar com entrada de usuários, autenticação, armazenamento de dados ou integrações externas. Fundamental para features que aceitam dados não confiáveis."
        },
        {
            "id": "agent_skill_shipping-and-launch",
            "title": "Lançamento e Entrega",
            "path": "agent-skills/skills/shipping-and-launch/SKILL.md",
            "description": "Prepara lançamentos para produção. Use ao se preparar para implantar em produção. Útil para checklists de pré-lançamento, configuração de monitoramento, lançamentos em etapas ou estratégias de rollback."
        },
        {
            "id": "agent_skill_source-driven-development",
            "title": "Desenvolvimento Guiado por Fontes",
            "path": "agent-skills/skills/source-driven-development/SKILL.md",
            "description": "Baseia cada decisão de implementação na documentação oficial. Use quando quiser código autoritativo, citado por fontes e livre de padrões desatualizados. Ideal para trabalhar com bibliotecas e frameworks."
        },
        {
            "id": "agent_skill_spec-driven-development",
            "title": "Desenvolvimento Guiado por Especificação",
            "path": "agent-skills/skills/spec-driven-development/SKILL.md",
            "description": "Cria especificações antes de programar. Use ao iniciar um novo projeto, funcionalidade ou alteração significativa e nenhuma especificação existir ainda. Útil para requisitos vagos ou ambíguos."
        },
        {
            "id": "agent_skill_test-driven-development",
            "title": "Desenvolvimento Guiado por Testes (TDD)",
            "path": "agent-skills/skills/test-driven-development/SKILL.md",
            "description": "Guia o desenvolvimento através de testes. Use ao implementar lógicas, corrigir bugs ou alterar comportamentos. Indispensável para provar que o código funciona e não quebrar funcionalidades existentes."
        },
        {
            "id": "agent_skill_using-agent-skills",
            "title": "Uso de Skills do Agente",
            "path": "agent-skills/skills/using-agent-skills/SKILL.md",
            "description": "Descobre e invoca as habilidades (skills) do agente. Use ao iniciar uma sessão ou quando precisar descobrir qual skill se aplica à tarefa atual. É a meta-skill que governa a descoberta de todas as outras."
        }
    ]
};

if(typeof module !== 'undefined') module.exports = agentSkillsData;