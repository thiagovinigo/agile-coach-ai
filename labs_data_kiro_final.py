# labs_data_kiro_final.py

kiro_final = [
    {
        "id": 41, "icon": "🛰️", "title": "Marco 1: O Gatilho do Orquestrador",
        "oque": "O ponto de partida do Upstream. O Kiro (Daemon) escuta um evento no TFS via Webhook e decide iniciar a esteira.",
        "porque": "Demonstrar a automação total. Ninguém precisa abrir o terminal e digitar 'iniciar projeto'. A criação do Épico pelo Diretor no Azure DevOps já é o suficiente para acordar as Inteligências Artificiais.",
        "steps": [
            {
                "title": "A Skill de Webhook do Kiro",
                "text": "O Arquivo .yaml que diz ao Kiro como escutar o TFS.",
                "code": "# .kiro/triggers.yaml\nwebhooks:\n  - route: \"/api/webhooks/tfs\"\n    secret: \"${TFS_SECRET}\"\n    events:\n      - \"workitem.created\"\n    condition: \"payload.resource.fields['System.WorkItemType'] == 'Epic'\"\n    trigger_skill: \"discovery.yaml\"",
                "lang": "yaml"
            },
            {
                "title": "A Saída do Kiro",
                "text": "O Daemon no servidor recebe o payload e inicia a operação.",
                "code": "[Kiro Daemon] Webhook HTTP 200 OK. Épico #500 'Ferramenta Kanban Autônoma' criado.\n[Kiro Daemon] Condição 'Epic' satisfeita.\n[Kiro Daemon] Engatilhando Skill 'discovery.yaml'...",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 42, "icon": "🔎", "title": "Marco 2: Product Discovery (Fatiamento)",
        "oque": "A invocação da Skill `discovery.yaml`. O Agente Product Owner assume o controle, lê a demanda bruta e divide em User Stories acionáveis via API.",
        "porque": "Quebrar Épicos gigantes em fatias pequenas (User Stories) é a essência do Desenvolvimento Ágil. Mostrar a Skill provê a rastreabilidade do raciocínio.",
        "steps": [
            {
                "title": "O Perfil do Agente PO",
                "text": "Este é o YAML que define os poderes de leitura de backlog e as ferramentas de API que o PO possui.",
                "code": "# .kiro/skills/discovery.yaml\nagent:\n  name: \"Product Owner\"\n  role: \"Discovery Specialist\"\nmcp_servers:\n  - name: \"azure-devops-board\"\nsystem_prompt: |\n  Você receberá um Epic ID.\n  Leia a descrição. Divida em pelo menos 3 User Stories focadas em entrega de valor.\n  Para cada Story, utilize a ferramenta `tfs_create_workitem` e faça o link hierárquico com o Épico Pai.",
                "lang": "yaml"
            },
            {
                "title": "A Execução (Logs de Orquestração)",
                "text": "A IA processa e executa os comandos na nuvem da Microsoft.",
                "code": "[Agente PO] Analisando Épico #500...\n[Agente PO] Identificadas 3 frentes de trabalho: Validação Estática, Autocura de Código e Git Hooks.\n\n> Invocando Tool: tfs_create_workitem({\"Title\": \"Story #501: Motor de Linter e Sonar\", \"Parent\": 500})\n> Invocando Tool: tfs_create_workitem({\"Title\": \"Story #502: Loop TDD de Autocura\", \"Parent\": 500})\n> Invocando Tool: tfs_create_workitem({\"Title\": \"Story #503: Pipeline Pre-Commit Segura\", \"Parent\": 500})\n\n[Agente PO] Finalizado. Disparando Transição para Tech Lead.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 43, "icon": "🏛️", "title": "Marco 3: Refinamento Arquitetural (ADR)",
        "oque": "A invocação da Skill `architect.yaml`. O Agente Tech Lead assume o controle da Story #501 e decide o design pattern e a stack tecnológica.",
        "porque": "Garante a sustentabilidade do código. Mostra como o Kiro evita que os agentes de código tomem decisões globais de infraestrutura sozinhos.",
        "steps": [
            {
                "title": "A Skill do Arquiteto",
                "text": "Ele não tem permissão para escrever código fonte, apenas arquivos Markdown de documentação e anexos no TFS.",
                "code": "# .kiro/skills/architect.yaml\nagent:\n  name: \"Tech Lead\"\n  role: \"Software Architect\"\nworkspace_rules:\n  allow_write_code: false\n  allowed_extensions: [\".md\"]\nsystem_prompt: |\n  Analise a User Story e redija um Architecture Decision Record (ADR).\n  Especifique a linguagem, framework e design pattern (Ex: Clean Architecture).",
                "lang": "yaml"
            },
            {
                "title": "A Saída (ADR Gerado)",
                "text": "O Arquiteto faz o upload da diretriz de código para a Task #501.",
                "code": "# docs/adr/001-motor-validacao.md\n## Contexto\nA Story #501 exige um motor de validação assíncrona.\n## Decisão Técnica\n- Linguagem: TypeScript (Strict Mode)\n- Linter: ESLint Flat Config\n- Padrão: Strategy Pattern para injetar validadores diferentes (Linter, SonarQube).\n\n[Kiro Tech Lead] Fez upload do ADR para a Task #501.\n[Kiro Tech Lead] Mudando status do TFS para 'Pronto para Desenvolvimento'.",
                "lang": "markdown"
            }
        ]
    }
]
