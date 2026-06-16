# labs_data_claude.py

claude_basics = [
    {
        "id": 1, "icon": "🔑", "title": "CLI Autenticação e Primeiros Passos",
        "oque": "O fluxo básico de instalação via gerenciador de pacotes Node (NPM) e o login via terminal para obter o Token Auth da Anthropic.",
        "porque": "Para desenvolvedores, alternar entre a IDE e o navegador (ChatGPT/Claude.ai) destrói o estado de foco mental ('Flow'). Trazer a IA para o Terminal, onde o desenvolvedor já trabalha os testes e o git, reduz o atrito de contexto em 90%.",
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
        "oque": "A escrita de um script em Bash (shell) executado sempre que o sistema operacional tentar consolidar um commit localmente.",
        "porque": "Como o Claude é capaz de salvar arquivos e rodar o `git commit` sem você ver, você precisa de um campo de força. O `pre-commit` hook assegura mecanicamente que código quebrado por 'alucinação' nunca entre no seu histórico Git.",
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
        "oque": "Táticas avançadas de controle de memória do LLM dentro da IDE agentic para limpar e condensar conversas muito longas.",
        "porque": "Provedores cobram o Token em Dólares. Uma conversa de 50 turnos arrasta todo aquele histórico inútil a cada pergunta nova, estourando limites de contexto (Context Window Limit). O comando `/compact` salva a empresa de uma fatura de nuvem absurda no fim do mês.",
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
        "oque": "A injeção de documentos de restrição de regras de negócio em diretórios específicos usando a extensão `.claudecode` nativa.",
        "porque": "Se você usa Clean Architecture ou Domain-Driven Design (DDD), sabe que o 'Dominio' é sagrado e isolado. O Claude, querendo ser 'prestativo', muitas vezes quebra camadas importando views no banco de dados. Essas regras param esse crime arquitetural na raiz.",
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
        "oque": "A combinação do poder de Regex do Unix (Expressões regulares) aliada ao raciocínio em massa (Batch Processing) do Agente.",
        "porque": "Atualizar padrões de sintaxe (como migrar de Classes para Hooks no React ou remover NullPointerExceptions em 50 arquivos legados) pode levar dias para um Dev Jr. A IA via terminal faz essa faxina monumental em 3 minutos sem errar a sintaxe do framework.",
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
        "oque": "A configuração do Claude para reagir autonomamente a falhas reportadas pelas ferramentas de análise estática como o ESLint ou Prettier.",
        "porque": "Devolver código cheio de avisos de aspas duplas, ponto-e-vírgula e chaves mal fechadas gera fricção na equipe de desenvolvimento e polui o Pull Request. Forçamos a IA a entregar a 'mesa limpa' sempre.",
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
        "oque": "O uso de uma ponte entre o Claude e as APIs do framework de testes intermitentes (como Cypress ou Selenium) que reportam falhas sistêmicas.",
        "porque": "Testes 'Flaky' (que passam de manhã e falham de tarde) destroem a credibilidade da automação e do QA. O Agente precisa ler o relatório do teste nativamente, analisar o print de erro na tela do Cypress e fixar com 'waits' inteligentes para parar de irritar o time.",
        "steps": [
            {
                "title": "O Plugin Cypress",
                "text": "Um servidor Python local que a IDE consome.",
                "code": "claude /plugin add local ./get_flaky_cypress.py\n> Analise o teste mais flaky reportado pela tool e conserte-o usando explicit waits em vez de cy.wait().",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 8, "icon": "🔄", "title": "O Loop TDD (Test-Driven AI)",
        "oque": "Técnica de Prompting focada na disciplina do desenvolvimento orientado a testes. A IA deve primeiro entregar a falha estruturada e só depois a lógica.",
        "porque": "Quando você pede o código completo de uma vez, a IA tende a escrever testes que são apenas 'espelhos felizes' (Happy Paths) que ela já sabe que vão passar. O TDD forçado prova a validade funcional do requisito de negócio antes que o código exista.",
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
        "oque": "Comandos vitais de escape e recuperação do terminal quando a IDE entra em colapso e cria dezenas de arquivos inúteis no projeto.",
        "porque": "Às vezes, a tentativa de resolver um bug simples faz o Agente entrar em parafuso, onde cada correção gera outro erro. Saber usar o 'Ctrl+C' mental da IA garante que a arquitetura não vire 'código espaguete' na tentativa cega de fixar um problema.",
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
        "oque": "Trava de segurança na convenção do Claude que obriga o modelo a se comportar como um assistente verbal (que propõe o código e o explica via Diff Markdown) em vez de aplicar no disco.",
        "porque": "Juniores que aceitam o código mágico de olhos fechados tornam-se incapazes de entender sua própria base de código com o passar do tempo. A IA, sendo tutora, estimula a aprendizagem passiva ao invés da mera automação irresponsável.",
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
        "oque": "A integração do Claude Code com as APIs do Microsoft Azure DevOps (TFS) via um Servidor MCP, permitindo buscas dinâmicas sem abrir o navegador.",
        "porque": "O contexto mental do Dev deve continuar no terminal. Sair do VS Code para abrir a aba do Chrome, logar no TFS, buscar a aba Kanban e achar a própria Task consome energia. Aqui, basta dar o comando e a IA lista as prioridades do dia para você codar de imediato.",
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
        "oque": "O ato de ler uma História de Usuário bruta gerada pelos Agentes (Kiro) no TFS e transformá-la automaticamente em arquivos base na árvore local do projeto (pastas, pacotes, index).",
        "porque": "Montar a base chata (os chamados 'Boilerplates') requer muita digitação repetitiva de imports, configs e injeções React/Angular que agregam zero valor final. A IA traduz regras cruas e formata a casca inicial para o Dev apenas preencher o miolo intelectual.",
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
        "oque": "A emissão e o salvamento formal de um documento estruturado listando e justificando o porquê escolhemos uma tecnologia (ex: Redis vs Postgres) para a User Story do TFS.",
        "porque": "Se a equipe técnica mudar amanhã, o conhecimento do porquê certas bibliotecas e caches foram adotadas desaparece. Gerar o ADR mecanicamente pelo terminal atrelado ao número do card documenta o raciocínio sem o 'peso burocrático' odiado pelos Devs.",
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
        "oque": "O fluxo prático de consumir o critério BDD (Given, When, Then) atachado lá atrás pela ferramenta Discovery e transformar aquilo em testes interativos do tipo End-to-End no Cypress ou Jest.",
        "porque": "Isso materializa o 'Pipeline de Qualidade Continua'. O 'Contrato' assinado com o PO no TFS se transforma no código executável real que previne as falhas e dita como a interface deve se comportar antes do deploy.",
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
        "oque": "O envio da requisição (Patch Request) via LLM para a nuvem da Microsoft para atualizar os ponteiros de progresso ('Remaining Work' e estado do Ticket Kanban).",
        "porque": "Desenvolvedores não atualizam Kanban. Isso é um fato na indústria de TI. A integração garante que o burndown chart do Scrum Master permaneça liso e verde, pois a IA assina o ponto assim que o código compila na máquina.",
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
        "oque": "Um scanner reverso. A IA varre o código fonte atual, levanta todas as falhas pontuadas informalmente por humanos e cria Tickets explícitos no Backlog Técnico do TFS.",
        "porque": "Comentários no código do tipo `// TODO: Refatorar isso porque tá muito lento` são ignorados para sempre. Se não virar Card na mesa do Líder Técnico, a dívida esmaga a arquitetura num futuro próximo. O Claude garante essa visibilidade agressiva.",
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
        "oque": "Instruir a IA via terminal a interagir com os logs do SonarQube para sanar os relatórios drásticos de Segurança (OWASP Top 10).",
        "porque": "O SonarQube reprova o PR se notar injeção de dependências inseguras ou criptografia fraca, travando a pipeline inteira. Acionar o LLM no terminal localmente conserta o code-smell na sua máquina, garantindo aprovação verde lá no TFS de primeira.",
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
        "oque": "A formatação textual dos 'git logs' locais de maneira sofisticada e a criação programática do Pull Request via API Rest do Azure DevOps Repos.",
        "porque": "Um PR 'TBD' ou 'Fix Bug' na descrição é o pesadelo do Arquiteto que vai revisar o código. A ferramenta analisa o que você codou no dia inteiro e formula o texto de envio explicando cada classe alterada e linkando a Task do Board perfeitamente.",
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
        "oque": "O download da branch do colega de trabalho pela IDE e a análise do seu código por um modelo poderoso (Claude 3.5 Sonnet) buscando vulnerabilidades arquiteturais profundas.",
        "porque": "Muitas vezes o colega Sênior está ocupado, e revisões no Github são rasas. Usar a IA para encontrar SQL Injection e Race Conditions invisíveis economiza horas de Code Review massante e blinda o projeto.",
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
        "oque": "A dissecação de logs mortos de servidores derrubados e a criação automática e estruturada do documento final RCA (Root Cause Analysis - Causa Raiz).",
        "porque": "Quando ocorre um Bug 911 e a aplicação sangra dinheiro, consertar não é suficiente. É vital fechar o ciclo do DevOps formalizando a falha, o responsável e a ação para evitar aquilo no futuro. O Agente encerra a novela anexando a paz de espírito estruturada no sistema Kanban.",
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
