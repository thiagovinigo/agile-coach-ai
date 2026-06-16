const labsData = [
    {
        "id": "phase-1",
        "icon": "💡",
        "title": "Fase 1: Inception & Ideação Autônoma",
        "labs": [
            [
                "Análise de Mercado com MCP",
                "Ler relatórios PDF locais",
                "O Agente cruza dados da concorrência.",
                "claude mcp run market-analyzer --source report.pdf"
            ],
            [
                "Brainstorming de Produto",
                "Gerar 50 ideias de features",
                "Economiza semanas de reuniões de ideação.",
                "kiro generate-features --epic 'App Pagamentos'"
            ],
            [
                "Validação de Dor do Cliente",
                "Analisar NPS via MCP",
                "Extrai insights do banco de dados de NPS.",
                "claude mcp query nps-db 'select top complaints'"
            ],
            [
                "Criação da Visão do Produto",
                "Draft inicial do Product Vision",
                "Alinhamento C-Level automático.",
                "kiro draft-vision --epic 'App Pagamentos'"
            ],
            [
                "Definição de Personas",
                "Gerar perfis baseados em dados",
                "Personas hiper-realistas baseadas no CRM.",
                "claude mcp run crm-analyzer --extract-personas"
            ],
            [
                "Mapeamento da Jornada do Usuário",
                "User Journey Map autônomo",
                "Visão ponta a ponta da dor ao alívio.",
                "kiro map-journey --persona 'User1'"
            ],
            [
                "Priorização RICE Automática",
                "Dar score para features",
                "Remove viés humano da priorização.",
                "claude mcp run rice-scorer --features data.json"
            ],
            [
                "Análise de Risco Tecnológico",
                "Risk Assessment",
                "Mapear dependências antes de codar.",
                "kiro assess-risk --tech-stack 'React,Node'"
            ],
            [
                "Geração do Lean Canvas",
                "Business Model Canvas via IA",
                "Validação de viabilidade financeira.",
                "claude generate-canvas --market-data market.md"
            ],
            [
                "Sessão de Pitch Pitch Deck",
                "Gerar slides de apresentação",
                "Apresentar para investidores/sponsors.",
                "kiro create-pitch --epic 'App Pagamentos'"
            ]
        ]
    },
    {
        "id": "phase-2",
        "icon": "📝",
        "title": "Fase 2: Upstream & Refinamento",
        "labs": [
            [
                "Quebra de Épico em Histórias",
                "Dividir épico gigante",
                "Histórias INVEST prontas para sprint.",
                "kiro split-epic --file epico.md"
            ],
            [
                "Escrita de Critérios de Aceite",
                "Formatar em Gherkin",
                "BDD escrito em segundos.",
                "claude write-ac --story 'Login via Face'"
            ],
            [
                "Refinamento Técnico (Tech Lead Bot)",
                "Analisar viabilidade",
                "O bot aponta gargalos arquiteturais.",
                "kiro review-story --role tech-lead"
            ],
            [
                "Refinamento de UX/UI",
                "Sugestão de componentes",
                "Design System integrado.",
                "claude mcp run figma-analyzer --story 'Tela Login'"
            ],
            [
                "Estimativa de Esforço (Planning Poker Bot)",
                "Story Points via IA",
                "O bot lê histórias antigas e prevê pontos.",
                "kiro estimate-points --story 'Login'"
            ],
            [
                "Detecção de Dependências",
                "Mapear bloqueios",
                "Evita surpresas na Sprint.",
                "claude detect-deps --backlog sprint.md"
            ],
            [
                "Geração de Wireframes (Mermaid)",
                "Wireframes textuais",
                "Visualização rápida.",
                "kiro generate-wireframe --story 'Login'"
            ],
            [
                "Validação de Regras de Negócio",
                "Compliance Check",
                "Verifica LGPD e políticas.",
                "claude mcp run compliance-checker --story 'Login'"
            ],
            [
                "Sincronização com Jira via MCP",
                "Criar tickets no Jira",
                "Sem copiar e colar manual.",
                "claude mcp run jira-sync --push backlog.md"
            ],
            [
                "Geração de Documentação Funcional",
                "Wiki automática",
                "Mantém a base de conhecimento viva.",
                "kiro generate-wiki --sprint 1"
            ]
        ]
    },
    {
        "id": "phase-3",
        "icon": "🏛️",
        "title": "Fase 3: Engenharia de Requisitos & BDD",
        "labs": [
            [
                "Tradução Story -> BDD",
                "Gerar arquivos .feature",
                "Pronto para automação Cucumber.",
                "kiro generate-bdd --story-file us.md"
            ],
            [
                "Mapeamento de Casos de Borda",
                "Corner cases dinâmicos",
                "IA pensa em fluxos que humanos esquecem.",
                "claude find-edge-cases --feature login.feature"
            ],
            [
                "Geração de Massa de Dados",
                "Seed data para testes",
                "Massa mockada realista.",
                "claude mcp run db-seeder --schema users.sql"
            ],
            [
                "Definição de Dicionário de Dados",
                "Glossário unificado",
                "Nomenclatura padrão no time.",
                "kiro generate-glossary --domain 'Pagamentos'"
            ],
            [
                "Modelagem Conceitual de Banco",
                "Diagrama ER",
                "Cria o Mermaid ERD.",
                "claude generate-erd --bdd login.feature"
            ],
            [
                "Mapeamento de APIs (Swagger Draft)",
                "Gerar OpenAPI spec",
                "Contratos API-first.",
                "kiro generate-openapi --feature login.feature"
            ],
            [
                "Definição de SLIs/SLOs",
                "Métricas de sucesso",
                "Observabilidade by design.",
                "claude define-slo --service 'Auth API'"
            ],
            [
                "Validação Cruzada de Fluxos",
                "Detectar loops",
                "Encontra falhas lógicas no BDD.",
                "kiro validate-flows --dir bdd/"
            ],
            [
                "Sincronização com Confluence",
                "Publicar BDD",
                "Visibilidade corporativa.",
                "claude mcp run confluence-sync --push bdd/"
            ],
            [
                "Aprovação Automatizada de PO",
                "Bot atua como PO",
                "Valida se o BDD atende o Épico.",
                "kiro review-bdd --role product-owner"
            ]
        ]
    },
    {
        "id": "phase-4",
        "icon": "📐",
        "title": "Fase 4: Arquitetura de Software",
        "labs": [
            [
                "Diagramas C4 Model - Context",
                "Nível 1 C4",
                "Visão sistêmica.",
                "claude generate-c4-context --system 'Auth'"
            ],
            [
                "Diagramas C4 Model - Container",
                "Nível 2 C4",
                "Visão de infraestrutura.",
                "kiro generate-c4-container --system 'Auth'"
            ],
            [
                "Diagramas C4 Model - Component",
                "Nível 3 C4",
                "Visão de código.",
                "claude generate-c4-component --container 'API'"
            ],
            [
                "Análise de Trade-offs (ADR)",
                "Architecture Decision Record",
                "Documentar decisões difíceis.",
                "kiro generate-adr --topic 'SQL vs NoSQL'"
            ],
            [
                "Revisão de Segurança (Threat Modeling)",
                "STRIDE via IA",
                "Identifica vetores de ataque.",
                "claude run-threat-model --arch c4-container.md"
            ],
            [
                "Desenho de Cloud (AWS/Azure)",
                "Arquitetura Cloud",
                "Infra as Code draft.",
                "kiro design-cloud --provider AWS --reqs reqs.md"
            ],
            [
                "Modelagem de Filas e Mensageria",
                "Event Storming",
                "Arquitetura orientada a eventos.",
                "claude map-events --domain 'Checkout'"
            ],
            [
                "Estratégia de Cache",
                "Redis/Memcached",
                "Otimização de performance.",
                "kiro design-cache --endpoints api-spec.yaml"
            ],
            [
                "Definição de Topologia de Rede",
                "VPC e Subnets",
                "Isolamento de segurança.",
                "claude design-network --arch cloud.md"
            ],
            [
                "Validação de Arquitetura (Tech Lead)",
                "Revisão por pares (IA)",
                "Peer review arquitetural.",
                "kiro review-arch --file c4-container.md"
            ]
        ]
    },
    {
        "id": "phase-5",
        "icon": "🔌",
        "title": "Fase 5: A Base do MCP",
        "labs": [
            [
                "Instalando SDK do MCP",
                "Setup inicial",
                "Preparação do ambiente.",
                "pip install mcp"
            ],
            [
                "Criando Servidor Stdio",
                "Comunicação via terminal",
                "O básico do protocolo.",
                "python server.py"
            ],
            [
                "Expondo Tools Estáticas",
                "Ferramentas simples",
                "IA chamando funções Python.",
                "@app.list_tools()"
            ],
            [
                "Expondo Resources de Texto",
                "Ler logs locais",
                "IA lendo arquivos do SO.",
                "@app.list_resources()"
            ],
            [
                "Conectando ao PostgreSQL via MCP",
                "Database Tool",
                "IA rodando queries.",
                "claude mcp run pg-server"
            ],
            [
                "Conectando ao GitHub via MCP",
                "Repo Tool",
                "IA lendo código remoto.",
                "claude mcp run github-server"
            ],
            [
                "Criando MCP de Notificações (Slack)",
                "Webhook Tool",
                "IA mandando mensagens.",
                "claude mcp run slack-server"
            ],
            [
                "Gerenciando Permissões no MCP",
                "Segurança",
                "Restringir o que a IA pode acessar.",
                "mcp config --restrict"
            ],
            [
                "Deploy de MCP Server via SSE",
                "Server-Sent Events",
                "MCP rodando via HTTP.",
                "uvicorn mcp_server:app"
            ],
            [
                "Troubleshooting MCP",
                "Lendo logs do MCP",
                "Debug de conexões.",
                "mcp logs --tail"
            ]
        ]
    },
    {
        "id": "phase-6",
        "icon": "💻",
        "title": "Fase 6: Downstream & Claude Code",
        "labs": [
            [
                "Configurando o Claude Code CLI",
                "Setup da CLI",
                "Terminal anabolizado.",
                "npm install -g @anthropic-ai/claude-code"
            ],
            [
                "Conectando Claude ao MCP Local",
                "Add MCP server",
                "Claude ganha superpoderes.",
                "claude mcp add my-server python server.py"
            ],
            [
                "Geração do Skeleton (Boilerplate)",
                "Criar projeto",
                "IA estrutura pastas.",
                "claude 'crie um projeto NestJS'"
            ],
            [
                "Implementação de CRUD Básico",
                "Escrever código",
                "Velocidade na entrega.",
                "claude 'implemente o CRUD de usuários'"
            ],
            [
                "Refatoração de Código Legado",
                "Clean Code",
                "IA melhora código sujo.",
                "claude 'refatore utils.js para SOLID'"
            ],
            [
                "Tradução de Linguagens",
                "Java para Go",
                "Migração de tech stack.",
                "claude 'traduza App.java para main.go'"
            ],
            [
                "Explicar Código Complexo",
                "Engenharia Reversa",
                "Entender o que foi feito.",
                "claude 'explique a função encrypt'"
            ],
            [
                "Otimização de Performance",
                "Big O Notation",
                "Deixar o código mais rápido.",
                "claude 'otimize este loop para O(N)'"
            ],
            [
                "Integração de APIs Externas",
                "Consumir REST",
                "IA escreve o fetch.",
                "claude 'crie um client para a API do Stripe'"
            ],
            [
                "Tratamento de Erros e Logs",
                "Resiliência",
                "Adicionar try-catch robusto.",
                "claude 'adicione Winston logger e try catch'"
            ]
        ]
    },
    {
        "id": "phase-7",
        "icon": "🧪",
        "title": "Fase 7: Test-Driven Development (TDD)",
        "labs": [
            [
                "Escrevendo o Primeiro Teste Falho",
                "Red",
                "IA escreve teste antes do código.",
                "claude 'escreva o teste Jest para sum()'"
            ],
            [
                "Implementando o Código (Green)",
                "Green",
                "IA faz o teste passar.",
                "claude 'implemente sum() para o teste passar'"
            ],
            [
                "Refatorando (Refactor)",
                "Refactor",
                "IA melhora sem quebrar o teste.",
                "claude 'refatore sum() usando reduce'"
            ],
            [
                "Testes de Integração com Banco",
                "Testcontainers",
                "Testes que batem no DB.",
                "kiro generate-integration-tests"
            ],
            [
                "Testes E2E com Cypress/Playwright",
                "Testes de Tela",
                "Automação de navegador.",
                "claude 'crie um teste Playwright para o login'"
            ],
            [
                "Testes de Mutação (Stryker)",
                "Garantir a cobertura",
                "Testando os testes.",
                "kiro run-mutation-tests"
            ],
            [
                "Testes de Carga (K6)",
                "Performance tests",
                "Simulando 10k usuários.",
                "claude 'crie script K6 para /login'"
            ],
            [
                "Mocks e Stubs Inteligentes",
                "Mocking",
                "Isolar dependências.",
                "claude 'mocke a API do Stripe no Jest'"
            ],
            [
                "Geração Automática de Cobertura",
                "Coverage 100%",
                "IA caça linhas não testadas.",
                "claude 'escreva testes para atingir 100% de coverage'"
            ],
            [
                "Validação de Contrato (Pact)",
                "Contract Testing",
                "Testes entre microsserviços.",
                "kiro generate-pact-tests"
            ]
        ]
    },
    {
        "id": "phase-8",
        "icon": "🛡️",
        "title": "Fase 8: Segurança & Code Review",
        "labs": [
            [
                "Análise Estática via IA",
                "SonarQube mental",
                "Lint inteligente.",
                "claude 'analise este código em busca de code smells'"
            ],
            [
                "Caça de Vulnerabilidades (OWASP)",
                "Segurança",
                "Prevenir SQLi e XSS.",
                "claude 'verifique o top 10 OWASP neste arquivo'"
            ],
            [
                "Revisão de Pull Request Automatizada",
                "PR Reviewer Bot",
                "Feedback no GitHub.",
                "kiro review-pr --id 104"
            ],
            [
                "Padronização de Commits (Conventional)",
                "Commits semânticos",
                "Mensagens claras.",
                "claude 'gere uma mensagem de commit para este diff'"
            ],
            [
                "Análise de Dependências Quebradas",
                "SCA",
                "Atualizar pacotes.",
                "claude 'verifique o package.json por libs defasadas'"
            ],
            [
                "Criação de Políticas de Segurança",
                "DevSecOps",
                "Regras no pipeline.",
                "kiro generate-sec-policy"
            ],
            [
                "Escaneamento de Segredos (Secrets)",
                "TruffleHog bot",
                "Evitar chaves no git.",
                "claude 'verifique se há senhas neste código'"
            ],
            [
                "Reforço de Autenticação",
                "JWT/OAuth",
                "Implementar Auth forte.",
                "claude 'adicione validação de JWT na rota'"
            ],
            [
                "Revisão de Acessibilidade (a11y)",
                "WCAG",
                "Tornar acessível.",
                "claude 'avalie o HTML para regras WCAG'"
            ],
            [
                "Geração de Changelog Automático",
                "Release Notes",
                "Resumo das entregas.",
                "kiro generate-changelog --tag v1.0.0"
            ]
        ]
    },
    {
        "id": "phase-9",
        "icon": "🚀",
        "title": "Fase 9: CI/CD & Deploy",
        "labs": [
            [
                "Geração de Dockerfile",
                "Containerização",
                "Empacotar a app.",
                "claude 'crie um Dockerfile multi-stage'"
            ],
            [
                "Geração de Docker Compose",
                "Ambiente Local",
                "Orquestração local.",
                "claude 'crie o docker-compose.yml com Postgres'"
            ],
            [
                "Criação de Pipeline GitHub Actions",
                "CI setup",
                "Build e Test automáticos.",
                "kiro generate-github-actions"
            ],
            [
                "Pipeline do Azure DevOps",
                "Azure YAML",
                "Integração corporativa.",
                "kiro generate-azure-pipeline"
            ],
            [
                "Deploy Automatizado (Terraform)",
                "IaC",
                "Infra as Code gerada por IA.",
                "claude 'escreva Terraform para um bucket S3'"
            ],
            [
                "Monitoramento e Alertas (Prometheus)",
                "Observabilidade",
                "Dashboarding.",
                "claude 'crie as regras do Prometheus'"
            ],
            [
                "Resolução Automática de Build Falho",
                "Fix the Build",
                "IA lê o erro do CI e arruma.",
                "claude 'conserte o erro mostrado no log do Jenkins'"
            ],
            [
                "Estratégia de Rollback",
                "Blue/Green",
                "Deploy seguro.",
                "kiro design-rollback-strategy"
            ],
            [
                "Gerenciamento de Secrets na Cloud",
                "KMS/Vault",
                "IA injeta configs seguras.",
                "claude 'configure o AWS Secrets Manager'"
            ],
            [
                "Automação de Migrations de Banco",
                "Flyway/Liquibase",
                "Evolução do Schema.",
                "claude 'crie uma migration SQL para a tabela users'"
            ]
        ]
    },
    {
        "id": "phase-10",
        "icon": "🧠",
        "title": "Fase 10: Multi-Agents & Mastery",
        "labs": [
            [
                "A Guerra dos Agentes (Debate)",
                "Agentes conversando",
                "Dev vs QA bot.",
                "kiro orchestrate-debate --dev DevBot --qa QaBot"
            ],
            [
                "Cost Guards (Proteção Financeira)",
                "Limites de gastos",
                "Evitar sustos de faturamento.",
                "claude --cost-limit 2.00"
            ],
            [
                "RAG Híbrido Avançado",
                "Vetores + Grafos",
                "Otimizar contexto corporativo.",
                "kiro setup-rag-graph"
            ],
            [
                "Customização de System Prompts",
                "Prompt Eng",
                "Ajuste fino de personalidade.",
                "claude 'configure sua persona global'"
            ],
            [
                "Orquestração de MCPs Múltiplos",
                "Vários servidores",
                "IA conectada a Jira, DB e Slack juntos.",
                "claude mcp list"
            ],
            [
                "Auto-Reflexão e Correção (ReAct)",
                "Agente ReAct",
                "IA que pensa antes de agir.",
                "kiro run-react-loop"
            ],
            [
                "Fine-tuning vs RAG",
                "Decisão de Arquitetura",
                "Quando usar qual.",
                "claude 'compare Fine-Tuning com RAG para nosso caso'"
            ],
            [
                "Geração de UI Dinâmica",
                "v0 / Generative UI",
                "Frontends gerados on-the-fly.",
                "claude 'gere um componente React com Tailwind'"
            ],
            [
                "Otimização de Context Window",
                "Token Management",
                "Economizando tokens em arquivos grandes.",
                "kiro optimize-context"
            ],
            [
                "O Ecossistema 100% Autônomo",
                "O Desafio Final",
                "Discovery ao Deploy em 1 comando.",
                "kiro run-squad --epic 'App Pagamentos'"
            ]
        ]
    }
];
