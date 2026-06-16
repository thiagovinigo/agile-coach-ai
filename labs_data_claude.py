# labs_data_claude.py

claude_basics = [
    {
        "id": 1, "icon": "🔑", "title": "CLI Autenticação e Primeiros Passos",
        "desc": "O fluxo básico de inicialização no terminal.",
        "steps": [
            {
                "title": "Instalação e Login",
                "text": "O Claude Code roda localmente no seu NPM.",
                "code": "npm install -g @anthropic-ai/claude-code\nclaude login\nclaude\n> \"Você está autenticado!\"",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 2, "icon": "🛡️", "title": "Git Hooks de Defesa Ativa",
        "desc": "Bloqueando commits destrutivos da IA via Bash.",
        "steps": [
            {
                "title": "O Pre-Commit Hook",
                "text": "Força a IA a rodar testes antes de salvar o código.",
                "code": "#!/bin/sh\n# .git/hooks/pre-commit\n\nnpm test\nif [ $? -ne 0 ]; then\n  echo \"Testes falharam! Claude não pode comitar.\"\n  exit 1\nfi\nexit 0",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 3, "icon": "🧠", "title": "Context Window Management",
        "desc": "Evitando o estouro de limite de tokens usando escopos rígidos.",
        "steps": [
            {
                "title": "Comando Compact",
                "text": "Use o REPL para limpar o histórico e economizar USD.",
                "code": "> /compact\n[Claude] Limpando contexto inútil. Você economizou 50k tokens.\n> Focando APENAS em /src/utils, resolva o bug de data.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 4, "icon": "📁", "title": "DDD Conventions (.claudecode)",
        "desc": "Configurando limites arquiteturais por diretório.",
        "steps": [
            {
                "title": "Isolamento de Domínio",
                "text": "Regras específicas que a IA obedece ao ler aquela pasta.",
                "code": "# src/domain/.claudecode/CONVENTIONS.md\nRegra Absoluta: NUNCA importe nada da pasta 'infrastructure'.\nA camada de Domínio deve ser pura e não ter dependências externas.",
                "lang": "markdown"
            }
        ]
    },
    {
        "id": 5, "icon": "🏗️", "title": "Refatoração em Lote (Batching)",
        "desc": "O Claude alterando múltiplos arquivos via terminal.",
        "steps": [
            {
                "title": "Escalando o Refactor",
                "text": "Combine ferramentas Unix com IA.",
                "code": "> Encontre todos os arquivos React usando `var` em /components.\n> Atualize-os para usar `const` e `let` com ES6 functions.\n[Claude] Encontrei 34 arquivos. Refatorando em batch...",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 6, "icon": "🧹", "title": "Integração de Linter Automático",
        "desc": "Fazendo a IA limpar sua própria sujeira.",
        "steps": [
            {
                "title": "Fix On Save",
                "text": "A regra mestre no REPL.",
                "code": "# .claudecode/CONVENTIONS.md\nApós qualquer alteração em arquivos TypeScript, VOCÊ DEVE rodar 'npm run lint:fix'. Se quebrar, corrija sozinho antes de me devolver o prompt.",
                "lang": "markdown"
            }
        ]
    },
    {
        "id": 7, "icon": "🧪", "title": "Custom MCP: API de Testes Flaky",
        "desc": "Plugar uma ferramenta customizada para a IA resolver bugs intermitentes.",
        "steps": [
            {
                "title": "O Plugin Cypress",
                "text": "Um servidor Python local que a IDE consome.",
                "code": "claude /plugin add local ./get_flaky_cypress.py\n> Analise o teste mais flaky reportado pela tool e conserte-o usando explicitly waits.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 8, "icon": "🔄", "title": "O Loop TDD (Test-Driven AI)",
        "desc": "Forçando a IA a escrever o teste antes da implementação.",
        "steps": [
            {
                "title": "Prompting Disciplinado",
                "text": "A ordem das ações importa muito.",
                "code": "> 1. Escreva o teste Jest falhando para a classe Calculator.\n> 2. PARE e rode o teste para provar que falha.\n> 3. Espere minha autorização para implementar o código que passa no teste.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 9, "icon": "⏪", "title": "Revert & History Management",
        "desc": "O que fazer quando a IA entra em loop infinito e destrói código.",
        "steps": [
            {
                "title": "O Botão de Pânico",
                "text": "Parando a máquina e recomeçando.",
                "code": "^C (Ctrl+C)\n> /history\n> Esqueça as últimas 3 tentativas. Elas geraram loop de dependência.\n> Rode `git reset --hard HEAD` e vamos começar do zero abordando por Injeção de Dependência.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 10, "icon": "🗣️", "title": "Perfis de Prompt (Ask Before Write)",
        "desc": "Travas de segurança para Desenvolvedores Juniores.",
        "steps": [
            {
                "title": "Pedindo Permissão",
                "text": "Regra global para proteger arquivos.",
                "code": "# .claudecode/CONVENTIONS.md\nVocê está ajudando um Junior Dev. Sempre que formular uma alteração complexa, escreva o diff em Markdown primeiro.\nPARE. Só aplique o `write_file` após o Dev digitar 'Aprovado'.",
                "lang": "markdown"
            }
        ]
    }
]

claude_tfs = [
    {
        "id": 11, "icon": "📥", "title": "Prompting the Backlog",
        "desc": "Puxando tarefas do TFS diretamente no terminal.",
        "steps": [
            {
                "title": "Consumo de API no Prompt",
                "text": "Pluge a MCP do Azure DevOps.",
                "code": "> Use a tool `tfs_get_my_bugs`.\n> Liste todos os bugs assigned para mim na Sprint 42 e sugira por qual arquivo eu devo começar a olhar para resolver o primeiro.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 12, "icon": "🏗️", "title": "Scaffolding a partir da User Story",
        "desc": "A IA lê a história do TFS e monta a base do projeto.",
        "steps": [
            {
                "title": "Geração Estrutural",
                "text": "Lendo os critérios de aceite e criando pastas.",
                "code": "> Leia o Epic #100 do TFS.\n> Crie a estrutura de pastas seguindo Clean Architecture em /src.\n> Gere o package.json com os pacotes React e Tailwind necessários para cumprir os ACs.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 13, "icon": "🏛️", "title": "Architecture Decision Records (ADR.md)",
        "desc": "Gerando o documento oficial de arquitetura antes de programar.",
        "steps": [
            {
                "title": "O Arquivo ADR",
                "text": "Formalizando escolhas técnicas.",
                "code": "# docs/adr/001-use-redis-for-cache.md\n## Contexto\nA User Story #101 do TFS exige carregamento do Dashboard em < 1s.\n## Decisão\nUsaremos Redis.\n## Consequências\nAumenta custo de infra, mas reduz carga no Postgres.",
                "lang": "markdown"
            }
        ]
    },
    {
        "id": 14, "icon": "✅", "title": "TDD do Discovery ao Código",
        "desc": "Lendo o Gherkin BDD gerado pelo Kiro e programando.",
        "steps": [
            {
                "title": "De Feature para Spec",
                "text": "Traduzindo regras de negócio para Cypress.",
                "code": "> Leia o arquivo `feature.md` anexado à Task #101 no TFS.\n> Para o cenário 'Given user is logged out', escreva um arquivo auth.cy.js no Cypress.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 15, "icon": "⏳", "title": "O Loop de Refatoração e Status",
        "desc": "Atualizando o TFS em tempo real via terminal.",
        "steps": [
            {
                "title": "Atualizando Horas (Remaining Work)",
                "text": "A IA gerencia seu card.",
                "code": "> Acabei de rodar os testes e passaram.\n> Atualize o status do Task #102 no TFS para 'Resolved'.\n> Atualize o campo 'Remaining Work' para 0.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 16, "icon": "💳", "title": "Mapeamento de Dívida Técnica",
        "desc": "Convertendo // TODOs no código em tickets reais no Kanban.",
        "steps": [
            {
                "title": "Varrer e Criar",
                "text": "Delegue o trabalho braçal de criar cards.",
                "code": "> Faça um grep_search por comentários '// TODO' em /src.\n> Para cada um encontrado, crie um ticket de 'Dívida Técnica' no TFS linkando o arquivo e a linha, e atribua ao Tech Lead.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 17, "icon": "🚨", "title": "Linter Local vs SonarQube",
        "desc": "Corrigindo Code Smells antes que eles subam no PR.",
        "steps": [
            {
                "title": "Varredura Local",
                "text": "O Claude executa a ferramenta estática localmente.",
                "code": "> Rode o SonarLint CLI local neste arquivo.\n> Conserte todas as vulnerabilidades de 'Alta Severidade' encontradas antes de eu dar git add.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 18, "icon": "🚀", "title": "Automação do Pull Request (CLI)",
        "desc": "Abrindo o PR no Azure Repos diretamente do terminal local.",
        "steps": [
            {
                "title": "PR Command",
                "text": "Usando ferramentas customizadas de CLI.",
                "code": "> Leia meus commits locais e crie uma descrição rica em Markdown.\n> Use a tool `tfs_create_pr` para abrir o Pull Request na branch master e adicione os revisores padrão.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 19, "icon": "👥", "title": "Peer Review Local",
        "desc": "Usando a IA como par crítico na branch de um colega.",
        "steps": [
            {
                "title": "Crítica Arquitetural",
                "text": "Baixe o código e deixe o Claude achar as falhas.",
                "code": "> git checkout feature/payment-gateway\n> Atue como Arquiteto Sênior. Analise as alterações do último commit.\n> Encontre gargalos de concorrência ou injeção de SQL e me liste as linhas perigosas.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 20, "icon": "🔥", "title": "Post-Mortem de Incidentes",
        "desc": "Lendo dumps de erro e formalizando a correção no Azure DevOps.",
        "steps": [
            {
                "title": "Root Cause Analysis (RCA)",
                "text": "O fechamento do ciclo de vida de um Bug.",
                "code": "> Leia este log de erro do Sentry (error.txt).\n> Descubra qual arquivo causou o NullPointerException e conserte.\n> Crie o documento `root-cause.md` e anexe ao Bug #911 no TFS detalhando a causa raiz.",
                "lang": "bash"
            }
        ]
    }
]
