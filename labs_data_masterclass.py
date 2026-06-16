# labs_data_masterclass.py

masterclass_e2e = [
    {
        "id": 41, "icon": "🎭", "title": "Marco 1: Discovery & Backlog",
        "oque": "A recepção da ideia crua (Épico) do sistema 'AutoKanban' via integração com o Azure DevOps e o fatiamento autônomo em User Stories técnicas.",
        "porque": "Sem um refinamento claro de Upstream, o Desenvolvedor IA vai 'alucinar' tentando construir o sistema inteiro de uma vez. O Discovery traduz a visão de negócio para fatias mastigáveis, mantendo o controle no TFS.",
        "steps": [
            {
                "title": "Webhook Trigger",
                "text": "O TFS avisa que o Diretor criou o Épico 'Construir Ferramenta Kanban Autônoma'.",
                "code": "POST /api/webhooks/tfs\nPayload: { \"WorkItemId\": 500, \"Type\": \"Epic\" }\n\n[Kiro Daemon] Webhook Recebido. Acordando Agente Product Owner.",
                "lang": "bash"
            },
            {
                "title": "Product Owner Agent - Fatiamento",
                "text": "A IA lê o Épico e usa as ferramentas (MCP) para criar as tarefas.",
                "code": "[Agente PO] Lendo Épico #500...\n[Agente PO] O Épico contém Validação, TDD e Commit.\n\n> Executando Tool: tfs_create_workitem\n- Criada Story #501: \"Motor de Validação (Linter/Sonar)\"\n- Criada Story #502: \"Motor de Geração BDD\"\n- Criada Story #503: \"Pipeline de Auto-Commit Segura\"",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 42, "icon": "🔬", "title": "Marco 2: Refinamento Técnico (BDD & Arquitetura)",
        "oque": "O Agente Architect escolhendo a Stack do projeto via ADR, enquanto o QA Automation Planner escreve as regras de negócio em formato Gherkin.",
        "porque": "Evitar retrabalho. Ao escrever os cenários de teste Gherkin antes da primeira linha de código ser digitada (Shift-Left Testing), nós engessamos o comportamento esperado. O ADR blindado garante que o Claude Code não escolha linguagens aleatórias.",
        "steps": [
            {
                "title": "Geração do ADR (Tech Lead)",
                "text": "O Arquiteto emite o Documento de Decisão Formal para a Task #502.",
                "code": "# docs/adr/001-motor-bdd.md\n## Contexto\nPrecisamos de um parser Gherkin rápido e testável.\n## Decisão\nO AutoKanban será em TypeScript rodando em Node.js usando Jest e o pacote 'cucumber-jest'.\n\n[Kiro Tech Lead] Fez upload do ADR.md no TFS #502.",
                "lang": "markdown"
            },
            {
                "title": "Geração BDD (QA Agent)",
                "text": "O agente de Qualidade traduz a história #502 em critérios rígidos.",
                "code": "# feature.md (Anexado ao TFS #502)\nFeature: Motor de Geração BDD Automática\n\nScenario: IA gera testes baseados em User Story\n  Given a IA leu o Épico do Kanban\n  When ela processa a funcionalidade de Validação\n  Then o arquivo validator.test.ts deve ser gerado no diretório /__tests__\n  And todos os testes devem estar falhando (RED phase)",
                "lang": "gherkin"
            }
        ]
    },
    {
        "id": 43, "icon": "🔴", "title": "Marco 3: TDD Fase Vermelha (Red)",
        "oque": "A IDE Agentic (Claude Code) consome o `feature.md` e gera os testes unitários sem a implementação da funcionalidade, executando para provar que falham.",
        "porque": "É a base do Test-Driven Development (TDD). A IA comprova que o teste não é um 'Falso Positivo' (que sempre passa). Se a IA tentar codar logo de cara, nós ativamos um Gate Humano para pará-la.",
        "steps": [
            {
                "title": "Consumo de Critérios",
                "text": "O Desenvolvedor usa a IDE (Claude Code) para puxar o Ticket.",
                "code": "> claude /task tfs-get-story 502\n\n[Claude Code] Baixando ADR e feature.md de #502.\n> De acordo com as diretrizes do Tech Lead, devo escrever primeiro o arquivo cucumber.test.ts que falha.\n\n> npm run test -- validator.test.ts\n❌ FAILED - Expected validation to occur, but no module found.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 44, "icon": "🟢", "title": "Marco 4: Codificação e Autocura (Green & Refactor)",
        "oque": "O Claude Code escreve a lógica TypeScript (Phase Green), os testes passam, e ele mesmo aciona o ESLint para corrigir o código (Refactor).",
        "porque": "É aqui que a 'Ferramenta que codifica sozinha' brilha. Ela usa seu próprio loop de erro para se autoconsertar. Se um `import` quebrar, a ferramenta lê a saída de erro do terminal e tenta de novo até compilar verde.",
        "steps": [
            {
                "title": "Implementação e Linter",
                "text": "A mágica do loop de feedback da IA no terminal.",
                "code": "> [Claude Code] Criando validator.ts para passar no teste...\n> npm run test\n✅ PASS validator.test.ts\n\n> [Claude Code] Executando Linter pós-código...\n> npm run lint\n❌ Warning: 'any' is not allowed.\n> [Claude Code] Entendido, alterando o tipagem para interfaces estritas...\n> npm run lint\n✅ Clean.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 45, "icon": "🛡️", "title": "Marco 5: Validação Final e Pre-Commit",
        "oque": "A execução mandatória do Agente de Segurança Local (SonarQube) e do Hook do Git, finalizando com a criação de um Pull Request no Azure DevOps.",
        "porque": "Automação sem governança é caos. A IA não pode empurrar código sujo. A ferramenta garante que não há senhas expostas, aprova o commit, assina a mensagem e atualiza o Kanban para 'Resolved' de forma autônoma.",
        "steps": [
            {
                "title": "SonarQube & Commit",
                "text": "Bloqueando código antes de poluir a branch.",
                "code": "> [Claude Code] Acionando SonarLint CLI...\n✅ 0 Vulnerabilidades detectadas no validator.ts\n\n> [Claude Code] Comitando código com rastreabilidade.\n> git commit -m \"#[502] feat: implementa motor de validacao bdd\"\n\n> [Claude Code] Atualizando TFS via MCP...\nPATCH /api/workitems/502\n{ \"State\": \"Resolved\", \"Remaining Work\": 0 }\n\n> Pull Request criado e encaminhado para @tech-lead.",
                "lang": "bash"
            }
        ]
    }
]
