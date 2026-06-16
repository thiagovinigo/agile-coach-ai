# labs_data_kiro.py

kiro_basics = [
    {
        "id": 1, "icon": "🚀", "title": "Setup & Daemon Initialization",
        "oque": "É o comando inicial que instala o motor de orquestração do Kiro dentro do seu repositório local, criando a pasta oculta obrigatória `.kiro/`.",
        "porque": "Sem essa estrutura inicial, os agentes não têm onde buscar suas regras corporativas. O Daemon atua como o 'Maestro' em background, lendo esse `config.yaml` constantemente para saber qual LLM usar e qual o limite de paralelismo da sua máquina.",
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
        "oque": "Um arquivo YAML que define o perfil, as ferramentas e as permissões de um 'Tech Lead' autônomo artificial.",
        "porque": "Permite criar uma hierarquia inteligente. Em vez de uma IA que apenas escreve código cegamente, o Arquiteto lê a documentação, entende a Lei Geral de Proteção de Dados (via Confluence) e dita o desenho arquitetural para que os Coders apenas implementem. Isso garante padronização técnica.",
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
        "oque": "A configuração de um Agente Especialista em Produto (Product Owner/Analista de Negócios) que processa demandas brutas.",
        "porque": "Desenvolvedores perdem horas preciosas desvendando requisitos mal escritos ou quebrando histórias gigantes. O Planner automatiza a etapa de refinamento, traduzindo desejos de negócio (Épicos) em tarefas acionáveis e formatadas no padrão que a Engenharia precisa.",
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
        "oque": "A implementação de Kill Switches (Gatilhos de Interrupção) baseados em orçamento financeiro por execução.",
        "porque": "IAs agentic são propensas a 'Loops Infinitos' quando tentam resolver bugs complexos. Deixadas sozinhas, elas podem consumir milhares de dólares em chamadas de API do provedor (OpenAI/Anthropic) em uma única madrugada. O Cost Guard corta a energia antes que o orçamento sangre.",
        "steps": [
            {
                "title": "Proteção Financeira",
                "text": "Defina limites em Dólar por ciclo de execução.",
                "code": "# .kiro/skills/coder.yaml\ncost_guard:\n  max_usd_per_run: 2.50\n  action_on_breach: \"pause_and_notify_slack\"\n  notify: \"@tech-lead\"",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 5, "icon": "👥", "title": "Multi-Party Slack Approvals (Steering)",
        "oque": "Regras de Governança que obrigam a IA a pausar seu workflow e solicitar o 'Ok' humano via chat corporativo (Slack/Teams).",
        "porque": "Para ações altamente destrutivas (Deploy em Produção, DELETE em banco de dados), a máquina não pode ter autonomia absoluta. Essa configuração garante rastreabilidade humana (compliance) e evita apagões causados por alucinações (AI Hallucinations).",
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
        "oque": "Uma cerca de proteção arquitetural que força a IA a executar seus testes e comandos bash apenas dentro de containeres Docker de curta duração.",
        "porque": "Se a IA baixar um pacote NPM malicioso injetado via engenharia social ou rodar comandos destrutivos sem querer (ex: `rm -rf`), ela destruirá apenas o container efêmero, poupando a máquina do desenvolvedor (Host) e prevenindo vazamentos de segurança.",
        "steps": [
            {
                "title": "Isolamento Estrito",
                "text": "Nunca deixe a IA rodar scripts arbitrários diretamente no seu SO.",
                "code": "# .kiro/config.yaml\nsandbox:\n  enabled: true\n  provider: \"docker\"\n  image: \"node:18-alpine\"\n  network: \"host\"\n  timeout_minutes: 15",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 7, "icon": "🔌", "title": "Roteamento de Private MCPs",
        "oque": "A ponte entre as ferramentas (Model Context Protocol) nativas da sua rede corporativa e a inteligência do agente.",
        "porque": "IAs em nuvem não enxergam seus servidores de banco de dados internos. Ao configurar um MCP privado local via stdio (Terminal), você permite que o Kiro seja as 'mãos' da nuvem trabalhando com dados sensíveis que nunca saem da sua VPN.",
        "steps": [
            {
                "title": "Declaração de Ferramenta Privada",
                "text": "O Kiro repassa o pedido do LLM para o script local.",
                "code": "# .kiro/mcp.json\n{\n  \"mcpServers\": {\n    \"mainframe-db\": {\n      \"command\": \"python3\",\n      \"args\": [\"/opt/scripts/mcp_mainframe.py\"]\n    }\n  }\n}",
                "lang": "json"
            }
        ]
    },
    {
        "id": 8, "icon": "⚡", "title": "Parallel Workers (Map-Reduce)",
        "oque": "A orquestração que permite ao agente 'Arquiteto' se ramificar, criando e controlando 2 ou mais agentes menores trabalhando ao mesmo tempo.",
        "porque": "Escalabilidade. Em vez do LLM resolver uma tela de front-end, parar, e depois codar o backend de banco de dados, o orquestrador despacha a tarefa pesada para dois workers independentes, diminuindo o Lead Time brutalmente de horas para minutos.",
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
        "oque": "O registro implacável e estruturado de todas as reflexões (Thoughts) e chamadas de ferramenta executadas pelo Agente.",
        "porque": "Empresas com ISO 27001 ou SOC2 precisam provar QUEM tomou a decisão de apagar um arquivo ou fundir uma branch. O Audit Trail gera Logs JSON nativos que provam matematicamente os motivos pelos quais a IA agiu, essenciais para o Splunk ou Datadog.",
        "steps": [
            {
                "title": "Log Estruturado JSON",
                "text": "Configure o roteamento de logs corporativos.",
                "code": "# .kiro/config.yaml\nlogging:\n  level: \"debug\"\n  format: \"json\"\n  destinations:\n    - type: \"file\"\n      path: \"/var/log/kiro/audit.jsonl\"\n    - type: \"datadog\"\n      api_key: \"${DD_API_KEY}\"",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 10, "icon": "🔄", "title": "Failover & Exponential Backoff",
        "oque": "Políticas de resiliência que trocam automaticamente o LLM de raciocínio caso o provedor primário esteja fora do ar.",
        "porque": "APIs de IA são instáveis. Se o projeto inteiro depende do Anthropic Claude 3.5 e ele sofre instabilidade, sua esteira inteira congela. O Failover inteligente tenta reconectar progressivamente (Backoff) e, se falhar, assume um modelo secundário de outra empresa para não parar a produção.",
        "steps": [
            {
                "title": "Resiliência de API",
                "text": "Tolerância a falhas pesadas na infraestrutura.",
                "code": "# .kiro/config.yaml\nengine:\n  retry_policy:\n    max_attempts: 3\n    backoff_multiplier: 2.0\n  fallback_chain:\n    - \"claude-3-5-sonnet-20241022\"\n    - \"claude-3-haiku-20240307\"\n    - \"gpt-4o\"",
                "lang": "yaml"
            }
        ]
    }
]

kiro_tfs = [
    {
        "id": 11, "icon": "🎧", "title": "Webhook Listener do TFS",
        "oque": "O 'Ouvido' do Kiro. Uma configuração de API que fica escutando os eventos disparados nativamente pelos servidores da Microsoft.",
        "porque": "O Kiro precisa ser reativo para ser invisível aos usuários corporativos. Quando o diretor da área cria um Épico no Board do TFS, o webhook acorda o Kiro de forma automática, garantindo zero atrito (nenhum comando de terminal necessário).",
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
        "oque": "Uma skill de Kiro focada exclusivamente em consumir Épicos enormes, fatiá-los com inteligência e enviar os novos cards para o TFS.",
        "porque": "O maior gargalo das empresas ágeis é o 'Upstream'. Filas enormes de ideias que não são detalhadas por falta de tempo. Este agente desobstrui o funil, adiantando 80% do trabalho de um Product Manager experiente.",
        "steps": [
            {
                "title": "Automação de Backlog",
                "text": "O agente usa a API do TFS para criar tickets filhos tangíveis.",
                "code": "# .kiro/skills/discovery.yaml\nagent:\n  name: \"Product Discovery\"\nmcp_servers:\n  - name: \"azure-devops\"\nsystem_prompt: |\n  Você receberá o ID de um Épico. \n  Quebre-o em 3 a 5 User Stories factíveis.\n  Para cada história, use a tool `tfs_create_workitem`.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 13, "icon": "🥒", "title": "BDD & Acceptance Criteria",
        "oque": "A geração determinística de cenários de teste em formato Gherkin (Given/When/Then) atrelados à User Story original.",
        "porque": "Testes devem ditar a construção do código (TDD), mas QAs são geralmente inseridos tarde demais no fluxo. Gerar os critérios de aceite no momento em que a história nasce garante alinhamento absoluto do 'Definition of Done'.",
        "steps": [
            {
                "title": "Geração de Cenários",
                "text": "O QA Planner avalia as histórias e anexa regras de negócio.",
                "code": "# .kiro/skills/qa-planner.yaml\nagent:\n  name: \"QA Automation Planner\"\nsystem_prompt: |\n  Analise a User Story fornecida.\n  Escreva pelo menos 3 cenários de teste em formato Gherkin.\n  Anexe o conteúdo gerado criando um arquivo `feature.md` e faça upload no ticket via API do TFS.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 14, "icon": "🎨", "title": "UX/UI Design Sync",
        "oque": "Uma skill do orquestrador que converte discussões perdidas em comentários do TFS em especificações visuais de UI definitivas.",
        "porque": "Desenvolvedores não deveriam inferir cores ou comportamentos cegamente. Ao forçar uma especificação de Design explícita com aprovação humana, eliminamos idas e vindas visuais caríssimas com o cliente.",
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
        "oque": "Um processo automatizado onde o LLM pondera arquitetura, integrações externas e dados passados para sugerir os Story Points de uma Task.",
        "porque": "Cerimônias de Planning costumam consumir horas do time inteiro debatendo achismos. A IA traz uma estimativa matemática balizada (Ancoragem), permitindo que a equipe apenas valide o número, focando a reunião no que importa: impedimentos.",
        "steps": [
            {
                "title": "Estimação via IA",
                "text": "O Kiro analisa a complexidade baseada em regras explícitas.",
                "code": "# estimation-rules.md\n- Front-end + Back-end (CRUD simples): 3 Pontos\n- Integrações Externas Complexas: 5 Pontos\n- Refatoração profunda sem UI: 2 Pontos\n\n# O agente lê isso e usa `tfs_update_field(id, 'Microsoft.VSTS.Scheduling.StoryPoints', 5)`",
                "lang": "markdown"
            }
        ]
    },
    {
        "id": 16, "icon": "🔗", "title": "Rastreabilidade Obrigatória (Traceability)",
        "oque": "Um 'Selo de Autenticidade'. O Kiro proíbe qualquer IA programadora local de salvar arquivos no Git sem carimbar de qual ticket originou a mudança.",
        "porque": "Sem a rastreabilidade entre Código e Demanda, a empresa perde controle se sofrer uma auditoria de qualidade. Forçar a marcação `#[ID]` automatiza a ligação visual das branches ao Kanban do TFS.",
        "steps": [
            {
                "title": "Validação de Mensagem de Commit",
                "text": "O Kiro intercepta o Git da IA Coder.",
                "code": "# .kiro/skills/coder.yaml\nworkspace_rules:\n  require_commit_prefix: \"#[TicketID] - \"\n  on_validation_failure: \"reject_and_prompt\"\n\n# Exemplo: O Coder tentará comitar `git commit -m \"Fix login\"` e o Kiro rejeitará, obrigando-o a formatar como `#101 - Fix login`.",
                "lang": "yaml"
            }
        ]
    },
    {
        "id": 17, "icon": "👀", "title": "PR Review Automatizado (TFS Repos)",
        "oque": "A injeção do Agente de Segurança no fluxo de Pull Requests da Microsoft. Ele comenta linhas perigosas da mesma forma que um sênior o faria.",
        "porque": "Humanos sofrem de fadiga ocular em Pull Requests grandes e acabam aprovando vulnerabilidades grotescas. A IA atua como o Cão de Guarda incansável bloqueando vazamento de credenciais 24 horas por dia.",
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
        "oque": "O 'Passar do Bastão'. Quando o Kiro termina suas simulações locais, ele não faz deploy magicamente. Ele aciona as pipelines corporativas oficiais da empresa.",
        "porque": "Usar IA não significa jogar fora as ferramentas de Infraestrutura sólidas da corporação. O Kiro respeita as barreiras de compliance repassando o trabalho para o Azure Pipelines original.",
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
        "oque": "O trabalho glorificado do Gerente de Release. Um relatório elegante em Markdown detalhando todas as entregas do ciclo.",
        "porque": "Montar notas de versão catando dezenas de tickets pelo Board consome muito tempo. A automação consolida o valor entregue da Sprint e divulga o sucesso do time sem esforço humano.",
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
        "oque": "A auditoria de tempo. O script lê cada fase em que o ticket esteve no TFS e calcula quanto tempo o time humano ou a IA levou ali.",
        "porque": "Para aprimorar a maturidade ágil (Escala de Elite), precisamos saber os gargalos de fila (Wait Time). Extrair esses dados nativamente prova matematicamente a velocidade do time e se a adoção de IA Agentic cortou custos de verdade.",
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
