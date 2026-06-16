# labs_data_kiro.py

kiro_basics = [
    {
        "id": 1, "icon": "🚀", "title": "Setup & Daemon Initialization",
        "desc": "Inicializando o motor de orquestração no seu repositório local.",
        "steps": [
            {
                "title": "A Estrutura Raiz",
                "text": "O Kiro exige um diretório oculto. Crie o arquivo base de configuração global.",
                "code": "# .kiro/config.yaml\nengine:\n  max_concurrent_agents: 3\n  default_llm: \"claude-3-5-sonnet-20241022\"\n  telemetry: true",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 2, "icon": "🏛️", "title": "The Architect Blueprint",
        "desc": "Definindo a regra corporativa para o Tech Lead autônomo.",
        "steps": [
            {
                "title": "A Skill de Arquitetura",
                "text": "Este YAML impede que o Agente codifique e obriga a leitura de regras.",
                "code": "# .kiro/skills/architect.yaml\nagent:\n  name: \"Tech Lead\"\n  role: \"Software Architect\"\nworkspace_rules:\n  allow_write: false\n  allow_bash: false\nsystem_prompt: |\n  Você deve sempre desenhar diagramas Mermaid.\n  Consulte o Confluence antes de decidir a modelagem.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 3, "icon": "📝", "title": "The Planner Blueprint",
        "desc": "Configurando um PO autônomo que lê épicos.",
        "steps": [
            {
                "title": "A Skill de PO",
                "text": "Ele lê o Épico e não pode alterar código, apenas arquivos Markdown.",
                "code": "# .kiro/skills/planner.yaml\nagent:\n  name: \"Planner\"\nworkspace_rules:\n  allow_write: true\n  allowed_extensions: [\".md\", \".txt\"]\nsystem_prompt: |\n  Quebre o Épico em User Stories detalhadas usando o formato padrão da empresa.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 4, "icon": "💸", "title": "Cost Guards & Budgets",
        "desc": "Implementando Kill Switches de proteção financeira.",
        "steps": [
            {
                "title": "Proteção Financeira",
                "text": "Se um loop infinito ocorrer, a conta de API pode explodir. Defina limites por run.",
                "code": "# .kiro/skills/coder.yaml\ncost_guard:\n  max_usd_per_run: 2.50\n  action_on_breach: \"pause_and_notify_slack\"\n  notify: \"@tech-lead\"",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 5, "icon": "👥", "title": "Multi-Party Slack Approvals (Steering)",
        "desc": "O Kiro pausa e aguarda humanos antes do Deploy.",
        "steps": [
            {
                "title": "Regra de Dupla Aprovação",
                "text": "Configuração de Gate para transições de estado críticas.",
                "code": "# .kiro/workflows/deploy.yaml\nstate_transition:\n  from: \"QA Approved\"\n  to: \"Ready for Prod\"\napproval_gate:\n  required_approvals: 2\n  allowed_groups: [\"@dev-ops\", \"@product-managers\"]\n  timeout_hours: 24",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 6, "icon": "🐳", "title": "Ephemeral Docker Sandboxes",
        "desc": "Execução isolada de comandos bash para o Agente Coder.",
        "steps": [
            {
                "title": "Isolamento Estrito",
                "text": "Nunca deixe a IA rodar scripts arbitrários no seu host local.",
                "code": "# .kiro/config.yaml\nsandbox:\n  enabled: true\n  provider: \"docker\"\n  image: \"node:18-alpine\"\n  network: \"host\"\n  timeout_minutes: 15",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 7, "icon": "🔌", "title": "Roteamento de Private MCPs",
        "desc": "Conectando o Kiro a um servidor Python interno de banco de dados.",
        "steps": [
            {
                "title": "Declaração de Ferramenta Privada",
                "text": "O Kiro repassa o pedido do LLM para o script local via stdio.",
                "code": "# .kiro/mcp.json\n{\n  \"mcpServers\": {\n    \"mainframe-db\": {\n      \"command\": \"python3\",\n      \"args\": [\"/opt/scripts/mcp_mainframe.py\"]\n    }\n  }\n}",
                "lang": "json"
            }
        ]
    },
    {
        "id": 8, "icon": "⚡", "title": "Parallel Workers (Map-Reduce)",
        "desc": "O Arquiteto divide a tarefa e invoca Coders simultâneos.",
        "steps": [
            {
                "title": "Invocação Paralela",
                "text": "A transição de sucesso dispara múltiplos sub-agentes.",
                "code": "# .kiro/skills/architect.yaml\non_success:\n  trigger_subagents:\n    - skill: \"coder-backend.yaml\"\n      context: \"Criar API REST\"\n    - skill: \"coder-frontend.yaml\"\n      context: \"Criar Tela React\"",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 9, "icon": "📜", "title": "Audit Trail Logging",
        "desc": "Onde o Kiro guarda a memória para conformidade ISO 27001.",
        "steps": [
            {
                "title": "Log Estruturado JSON",
                "text": "Configure o roteamento de logs para sistemas de monitoramento.",
                "code": "# .kiro/config.yaml\nlogging:\n  level: \"debug\"\n  format: \"json\"\n  destinations:\n    - type: \"file\"\n      path: \"/var/log/kiro/audit.jsonl\"\n    - type: \"datadog\"\n      api_key: \"${DD_API_KEY}\"",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 10, "icon": "🔄", "title": "Failover & Exponential Backoff",
        "desc": "Se o Provedor Principal falhar, o Kiro se recupera.",
        "steps": [
            {
                "title": "Resiliência de API",
                "text": "Tolerância a falhas na infraestrutura de LLMs.",
                "code": "# .kiro/config.yaml\nengine:\n  retry_policy:\n    max_attempts: 3\n    backoff_multiplier: 2.0\n  fallback_chain:\n    - \"claude-3-5-sonnet-20241022\"\n    - \"claude-3-haiku-20240307\"\n    - \"gpt-4o\"",
                "lang": "yaml"
            }
        ]
    }
]

kiro_tfs = [
    {
        "id": 11, "icon": "🎧", "title": "Webhook Listener do TFS",
        "desc": "O Kiro precisa saber quando um ticket é criado. Configure o Webhook.",
        "steps": [
            {
                "title": "Ouvindo Eventos",
                "text": "Mapeie o evento do Azure DevOps para disparar o Agente Discovery.",
                "code": "# .kiro/triggers.yaml\nwebhooks:\n  - route: \"/api/webhooks/tfs\"\n    secret: \"${TFS_SECRET}\"\n    events:\n      - \"workitem.created\"\n    condition: \"payload.resource.fields['System.WorkItemType'] == 'Epic'\"\n    trigger_skill: \"discovery.yaml\"",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 12, "icon": "🔎", "title": "Agente Product Discovery",
        "desc": "Lendo o Épico e gerando User Stories detalhadas no Azure Boards.",
        "steps": [
            {
                "title": "Automação de Backlog",
                "text": "O agente usa a API do TFS para criar tickets filhos.",
                "code": "# .kiro/skills/discovery.yaml\nagent:\n  name: \"Product Discovery\"\nmcp_servers:\n  - name: \"azure-devops\"\nsystem_prompt: |\n  Você receberá o ID de um Épico. \n  Quebre-o em 3 a 5 User Stories factíveis.\n  Para cada história, use a tool `tfs_create_workitem`.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 13, "icon": "🥒", "title": "BDD & Acceptance Criteria",
        "desc": "Escrevendo Gherkin dentro dos tickets automaticamente.",
        "steps": [
            {
                "title": "Geração de Cenários",
                "text": "O QA Planner avalia as histórias e gera os critérios Given-When-Then.",
                "code": "# .kiro/skills/qa-planner.yaml\nagent:\n  name: \"QA Automation Planner\"\nsystem_prompt: |\n  Analise a User Story fornecida.\n  Escreva pelo menos 3 cenários de teste em formato Gherkin.\n  Anexe o conteúdo gerado criando um arquivo `feature.md` e faça upload no ticket via API do TFS.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 14, "icon": "🎨", "title": "UX/UI Design Sync",
        "desc": "Sincronizando discussões técnicas com aprovações de Design.",
        "steps": [
            {
                "title": "Spec de Interface",
                "text": "Lê threads de comentários no TFS e formaliza um doc de design.",
                "code": "# design-spec.md (Gerado pelo Kiro)\n## Componente: Login OTP\n- **Cor Base:** #3b82f6\n- **Comportamento:** O botão de submit deve ficar disabled até o input ter 6 dígitos.\n> Pendente aprovação final da equipe de Design (Tag @ux-team).",
                "lang": "markdown"
            }
        ]
    },
    {
        "id": 15, "icon": "⏱️", "title": "Sprint Planning Autônomo",
        "desc": "O Agente preenche o campo Story Points baseado em histórico.",
        "steps": [
            {
                "title": "Estimação via IA",
                "text": "O Kiro analisa a complexidade baseada em um documento de regras.",
                "code": "# estimation-rules.md\n- Front-end + Back-end (CRUD simples): 3 Pontos\n- Integrações Externas Complexas: 5 Pontos\n- Refatoração profunda sem UI: 2 Pontos\n\n# O agente lê isso e usa `tfs_update_field(id, 'Microsoft.VSTS.Scheduling.StoryPoints', 5)`",
                "lang": "markdown"
            }
        ]
    },
    {
        "id": 16, "icon": "🔗", "title": "Rastreabilidade Obrigatória (Traceability)",
        "desc": "O Coder é forçado a linkar o código ao WorkItem do TFS.",
        "steps": [
            {
                "title": "Validação de Mensagem de Commit",
                "text": "O Kiro intercepta as intenções de commit do Coder.",
                "code": "# .kiro/skills/coder.yaml\nworkspace_rules:\n  require_commit_prefix: \"#[TicketID] - \"\n  on_validation_failure: \"reject_and_prompt\"\n\n# Exemplo: O Coder tentará comitar `git commit -m \"Fix login\"` e o Kiro rejeitará, obrigando-o a formatar como `#101 - Fix login`.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 17, "icon": "👀", "title": "PR Review Automatizado (TFS Repos)",
        "desc": "O Kiro varre vulnerabilidades antes da aprovação do PR.",
        "steps": [
            {
                "title": "O Cão de Guarda do Repositório",
                "text": "Disparado quando um PR é aberto no Azure DevOps.",
                "code": "# .kiro/skills/pr_reviewer.yaml\nagent:\n  name: \"Security PR Reviewer\"\nmcp_servers:\n  - name: \"azure-devops-git\"\nsystem_prompt: |\n  Você receberá o ID de um Pull Request.\n  Busque os Diffs. \n  Se detectar Hardcoded Secrets ou falhas de injeção, use a tool `tfs_add_pr_comment` bloqueando o PR.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 18, "icon": "🛳️", "title": "CI/CD Handoff",
        "desc": "Entregando o bastão para as pipelines nativas.",
        "steps": [
            {
                "title": "Fechando o Ciclo do Agente",
                "text": "O Kiro move o card e a pipeline tradicional assume o build/deploy.",
                "code": "# azure-pipelines.yml (Editado pelo Kiro)\ntrigger:\n  branches:\n    include:\n      - master\nsteps:\n  - script: npm ci && npm run build\n    displayName: 'Build Production'\n  - task: AzureWebApp@1\n    inputs:\n      appName: 'prod-portal'\n# O Kiro marca o TFS WorkItem como 'Resolved'.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 19, "icon": "📋", "title": "Release Notes Generator",
        "desc": "Ao fim da Sprint, um Agente compila tudo o que foi entregue.",
        "steps": [
            {
                "title": "Changelog Automático",
                "text": "Gera documentação executiva via API do TFS e publica no Confluence.",
                "code": "# release-notes.md\n# 🚀 Release v1.4.0\n\n## Novas Features (Épico: Auth)\n- [TFS-101] Login OTP: Usuários agora podem logar via Token SMS.\n- [TFS-102] Dashboard: Gráficos de vendas em tempo real atualizados via WebSocket.\n\n## Correções\n- [TFS-99] Fix memory leak no servidor de relatórios.",
                "lang": "markdown"
            }
        ]
    },
    {
        "id": 20, "icon": "📈", "title": "Métricas de Fluxo (Lead Time)",
        "desc": "Coletando inteligência do processo Kanabn.",
        "steps": [
            {
                "title": "Relatório de Gargalos",
                "text": "Script MCP consumido pelo Kiro para analisar o passado.",
                "code": "# generate_metrics.py\nimport requests\n\ndef get_tfs_transitions(ticket_id):\n    # Chama API do TFS para pegar Histórico\n    # Calcula Data de 'Resolved' - Data de 'New'\n    return lead_time_hours\n\n# O Agente cria um analytics.csv com as maiores demoras da Sprint.",
                "lang": "python"
            }
        ]
    }
]
