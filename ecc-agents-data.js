const eccAgentsData = [
    {
        "id": "a11y-architect",
        "title": "Arquiteto de Acessibilidade",
        "description": "Especialista em acessibilidade com foco em conformidade WCAG 2.2 para plataformas Web e Nativas. Use PROATIVAMENTE ao projetar componentes de UI, estabelecer design systems ou auditar código para experiências de usuário inclusivas.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/a11y-architect.md"
    },
    {
        "id": "architect",
        "title": "Arquiteto",
        "description": "Especialista em arquitetura de software para design de sistemas, escalabilidade e tomada de decisões técnicas. Use PROATIVAMENTE ao planejar novas funcionalidades, refatorar sistemas grandes ou tomar decisões arquiteturais.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/architect.md"
    },
    {
        "id": "build-error-resolver",
        "title": "Resolvedor de Erros de Build",
        "description": "Especialista em resolução de erros de build e TypeScript. Use PROATIVAMENTE quando o build falhar ou ocorrerem erros de tipo. Corrige erros com diffs mínimos, sem edições arquiteturais. Foca em deixar o build verde rapidamente.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/build-error-resolver.md"
    },
    {
        "id": "chief-of-staff",
        "title": "Chefe de Gabinete",
        "description": "Chefe de gabinete de comunicação pessoal que faz a triagem de e-mails, Slack, LINE e Messenger. Classifica mensagens em 4 níveis (ignorar/apenas info/info reunião/ação necessária), gera rascunhos de resposta e garante acompanhamento pós-envio via hooks.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/chief-of-staff.md"
    },
    {
        "id": "code-architect",
        "title": "Arquiteto de Código",
        "description": "Projeta arquiteturas de funcionalidades analisando padrões e convenções da base de código existente, fornecendo blueprints de implementação com arquivos concretos, interfaces, fluxo de dados e ordem de build.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/code-architect.md"
    },
    {
        "id": "code-explorer",
        "title": "Explorador de Código",
        "description": "Analisa profundamente as funcionalidades da base de código existente, rastreando caminhos de execução, mapeando camadas de arquitetura e documentando dependências para informar o novo desenvolvimento.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/code-explorer.md"
    },
    {
        "id": "code-reviewer",
        "title": "Revisor de Código",
        "description": "Especialista em revisão de código. Revisa proativamente o código em busca de qualidade, segurança e manutenibilidade. Use imediatamente após escrever ou modificar o código. DEVE SER USADO para todas as alterações de código.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/code-reviewer.md"
    },
    {
        "id": "code-simplifier",
        "title": "Simplificador de Código",
        "description": "Simplifica e refina o código para clareza, consistência e manutenibilidade, preservando o comportamento. Foca no código modificado recentemente, a menos que instruído de outra forma.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/code-simplifier.md"
    },
    {
        "id": "comment-analyzer",
        "title": "Analisador de Comentários",
        "description": "Analisa comentários de código quanto à precisão, integridade, manutenibilidade e risco de depreciação dos comentários.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/comment-analyzer.md"
    },
    {
        "id": "conversation-analyzer",
        "title": "Analisador de Conversas",
        "description": "Use este agente ao analisar transcrições de conversas para encontrar comportamentos que valem a pena evitar com hooks. Acionado por /hookify sem argumentos.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/conversation-analyzer.md"
    },
    {
        "id": "cpp-build-resolver",
        "title": "Resolvedor de Build C++",
        "description": "Especialista em resolução de erros de build, CMake e compilação em C++. Corrige erros de build, problemas de linker e erros de template com mudanças mínimas. Use quando os builds C++ falharem.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/cpp-build-resolver.md"
    },
    {
        "id": "cpp-reviewer",
        "title": "Revisor C++",
        "description": "Revisor de código C++ especialista em segurança de memória, expressões idiomáticas modernas de C++, concorrência e desempenho. Use para todas as alterações de código C++.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/cpp-reviewer.md"
    },
    {
        "id": "csharp-reviewer",
        "title": "Revisor C#",
        "description": "Revisor de código C# especialista em convenções .NET, padrões assíncronos, segurança, tipos de referência anuláveis e desempenho. Use para todas as alterações de código C#.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/csharp-reviewer.md"
    },
    {
        "id": "dart-build-resolver",
        "title": "Resolvedor de Build Dart",
        "description": "Especialista em resolução de erros de build, análise e dependência em Dart/Flutter. Corrige erros de `dart analyze`, falhas de compilação, conflitos de dependência pub e problemas de build_runner com mudanças mínimas.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/dart-build-resolver.md"
    },
    {
        "id": "database-reviewer",
        "title": "Revisor de Banco de Dados",
        "description": "Especialista em banco de dados PostgreSQL para otimização de consultas, design de esquemas, segurança e desempenho. Use PROATIVAMENTE ao escrever SQL, criar migrações, desenhar esquemas ou solucionar problemas de desempenho.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/database-reviewer.md"
    },
    {
        "id": "django-build-resolver",
        "title": "Resolvedor de Build Django",
        "description": "Especialista em resolução de erros de dependência, migração e build em Django/Python. Corrige erros de pip/Poetry, conflitos de migração e erros de importação com mudanças mínimas.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/django-build-resolver.md"
    },
    {
        "id": "django-reviewer",
        "title": "Revisor Django",
        "description": "Revisor de código Django especialista em correção de ORM, padrões DRF, segurança de migração e práticas de produção. Use para todas as alterações de código Django.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/django-reviewer.md"
    },
    {
        "id": "doc-updater",
        "title": "Atualizador de Documentação",
        "description": "Especialista em documentação e mapas de código. Use PROATIVAMENTE para atualizar mapas de código e documentação. Executa /update-codemaps e /update-docs, gera docs/CODEMAPS/*, atualiza READMEs e guias.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/doc-updater.md"
    },
    {
        "id": "docs-lookup",
        "title": "Busca de Documentação",
        "description": "Quando o usuário perguntar como usar uma biblioteca, framework ou API ou precisar de exemplos de código atualizados, use o MCP Context7 para buscar a documentação atual.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/docs-lookup.md"
    },
    {
        "id": "e2e-runner",
        "title": "Executor E2E",
        "description": "Especialista em testes end-to-end usando Vercel Agent Browser (preferencial) com fallback para Playwright. Use PROATIVAMENTE para gerar, manter e executar testes E2E.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/e2e-runner.md"
    },
    {
        "id": "fastapi-reviewer",
        "title": "Revisor FastAPI",
        "description": "Revisa aplicações FastAPI quanto à correção assíncrona, injeção de dependência, esquemas Pydantic, segurança, qualidade OpenAPI, testes e prontidão para produção.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/fastapi-reviewer.md"
    },
    {
        "id": "flutter-reviewer",
        "title": "Revisor Flutter",
        "description": "Revisor de código Flutter e Dart. Revisa o código em busca de melhores práticas de widgets, padrões de gerenciamento de estado, desempenho, acessibilidade e violações de clean architecture.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/flutter-reviewer.md"
    },
    {
        "id": "fsharp-reviewer",
        "title": "Revisor F#",
        "description": "Revisor de código F# especialista em expressões funcionais, segurança de tipo, pattern matching e desempenho. Use para todas as alterações de código F#.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/fsharp-reviewer.md"
    },
    {
        "id": "gan-evaluator",
        "title": "Avaliador GAN",
        "description": "GAN Harness — Agente avaliador. Testa a aplicação em execução via Playwright, pontua contra a rubrica e fornece feedback acionável para o Gerador.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/gan-evaluator.md"
    },
    {
        "id": "gan-generator",
        "title": "Gerador GAN",
        "description": "GAN Harness — Agente gerador. Implementa funcionalidades de acordo com a especificação, lê o feedback do avaliador e itera até que o limite de qualidade seja atingido.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/gan-generator.md"
    },
    {
        "id": "gan-planner",
        "title": "Planejador GAN",
        "description": "GAN Harness — Agente planejador. Expande um prompt de uma linha em uma especificação completa do produto com funcionalidades, sprints, critérios de avaliação e direção de design.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/gan-planner.md"
    },
    {
        "id": "go-build-resolver",
        "title": "Resolvedor de Build Go",
        "description": "Especialista em resolução de erros de build, vet e compilação em Go. Corrige erros de build, problemas de go vet e avisos de linter com mudanças mínimas.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/go-build-resolver.md"
    },
    {
        "id": "go-reviewer",
        "title": "Revisor Go",
        "description": "Revisor de código Go especialista em Go idiomático, padrões de concorrência, tratamento de erros e desempenho. Use para todas as alterações de código Go.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/go-reviewer.md"
    },
    {
        "id": "harmonyos-app-resolver",
        "title": "Resolvedor de App HarmonyOS",
        "description": "Especialista em desenvolvimento de aplicações HarmonyOS com foco em ArkTS e ArkUI. Revisa o código quanto à conformidade de gerenciamento de estado V2, padrões de roteamento de navegação, uso de API e desempenho.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/harmonyos-app-resolver.md"
    },
    {
        "id": "harness-optimizer",
        "title": "Otimizador de Harness",
        "description": "Analisa e melhora a configuração do ambiente de agente local (harness) para confiabilidade, custo e taxa de transferência.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/harness-optimizer.md"
    },
    {
        "id": "healthcare-reviewer",
        "title": "Revisor de Saúde",
        "description": "Revisa código de aplicações de saúde quanto à segurança clínica, precisão de CDSS, conformidade com PHI e integridade de dados médicos. Especializado em EMR/EHR e sistemas de informação de saúde.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/healthcare-reviewer.md"
    },
    {
        "id": "homelab-architect",
        "title": "Arquiteto Homelab",
        "description": "Desenha planos de arquitetura de rede para residências e pequenos laboratórios a partir de inventário de hardware, metas e nível de experiência do operador, com mudanças seguras e orientação de rollback.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/homelab-architect.md"
    },
    {
        "id": "java-build-resolver",
        "title": "Resolvedor de Build Java",
        "description": "Especialista em resolução de erros de dependência, compilação e build em Java/Maven/Gradle. Detecta automaticamente Spring Boot ou Quarkus e aplica correções específicas do framework.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/java-build-resolver.md"
    },
    {
        "id": "java-reviewer",
        "title": "Revisor Java",
        "description": "Revisor de código Java especialista em projetos Spring Boot e Quarkus. Detecta o framework automaticamente e aplica as regras de revisão apropriadas. Abrange arquitetura em camadas, segurança e concorrência.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/java-reviewer.md"
    },
    {
        "id": "kotlin-build-resolver",
        "title": "Resolvedor de Build Kotlin",
        "description": "Especialista em resolução de erros de dependência, compilação e build em Kotlin/Gradle. Corrige erros de build, erros do compilador Kotlin e problemas do Gradle com mudanças mínimas.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/kotlin-build-resolver.md"
    },
    {
        "id": "kotlin-reviewer",
        "title": "Revisor Kotlin",
        "description": "Revisor de código Kotlin e Android/KMP. Revisa o código Kotlin em busca de padrões idiomáticos, segurança de corrotinas, boas práticas do Compose, violações de clean architecture e armadilhas comuns do Android.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/kotlin-reviewer.md"
    },
    {
        "id": "loop-operator",
        "title": "Operador de Loop",
        "description": "Opera loops de agentes autônomos, monitora o progresso e intervém com segurança quando os loops travam.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/loop-operator.md"
    },
    {
        "id": "marketing-agent",
        "title": "Agente de Marketing",
        "description": "Estrategista de marketing e copywriter para planejamento de campanhas, pesquisa de público, posicionamento, criação de copy e revisão de conteúdo. Cobre landing pages, sequências de e-mail e posts sociais.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/marketing-agent.md"
    },
    {
        "id": "mle-reviewer",
        "title": "Revisor de MLE",
        "description": "Revisor de engenharia de machine learning em produção para contratos de dados, pipelines de features, reprodutibilidade de treinamento, avaliação e monitoramento de modelos.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/mle-reviewer.md"
    },
    {
        "id": "network-architect",
        "title": "Arquiteto de Rede",
        "description": "Desenha arquitetura de rede corporativa ou multi-site a partir de requisitos, usando habilidades de rede existentes para detalhamento de roteamento, validação, automação e solução de problemas.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/network-architect.md"
    },
    {
        "id": "network-config-reviewer",
        "title": "Revisor de Configuração de Rede",
        "description": "Revisa configurações de roteadores e switches quanto à segurança, correção, referências obsoletas, comandos arriscados e falta de proteções operacionais.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/network-config-reviewer.md"
    },
    {
        "id": "network-troubleshooter",
        "title": "Solucionador de Problemas de Rede",
        "description": "Diagnostica sintomas de conectividade de rede, roteamento, DNS, interface e política com um fluxo de trabalho de camada OSI somente leitura e resumo de causa raiz apoiado por evidências.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/network-troubleshooter.md"
    },
    {
        "id": "opensource-forker",
        "title": "Forker Open Source",
        "description": "Faz fork de qualquer projeto para open-sourcing. Copia arquivos, remove segredos e credenciais, substitui referências internas por espaços reservados e limpa o histórico do git.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/opensource-forker.md"
    },
    {
        "id": "opensource-packager",
        "title": "Empacotador Open Source",
        "description": "Gera empacotamento open-source completo para um projeto sanitizado. Produz CLAUDE.md, setup.sh, README.md, LICENSE e templates de issues do GitHub.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/opensource-packager.md"
    },
    {
        "id": "opensource-sanitizer",
        "title": "Sanitizador Open Source",
        "description": "Verifica se um fork open-source está totalmente sanitizado antes do lançamento. Verifica vazamentos de segredos, PII, referências internas e arquivos perigosos usando padrões regex.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/opensource-sanitizer.md"
    },
    {
        "id": "performance-optimizer",
        "title": "Otimizador de Desempenho",
        "description": "Especialista em análise e otimização de desempenho. Use PROATIVAMENTE para identificar gargalos, otimizar código lento, reduzir o tamanho de pacotes e melhorar o desempenho em tempo de execução.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/performance-optimizer.md"
    },
    {
        "id": "planner",
        "title": "Planejador",
        "description": "Especialista em planejamento para funcionalidades complexas e refatoração. Use PROATIVAMENTE quando os usuários solicitarem implementação de funcionalidades, alterações arquiteturais ou refatoração.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/planner.md"
    },
    {
        "id": "pr-test-analyzer",
        "title": "Analisador de Testes de PR",
        "description": "Revisa a qualidade e a integridade da cobertura de testes de pull requests, com ênfase na cobertura comportamental e na prevenção de bugs reais.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/pr-test-analyzer.md"
    },
    {
        "id": "python-reviewer",
        "title": "Revisor Python",
        "description": "Revisor de código Python especialista em conformidade com PEP 8, expressões idiomáticas em Python, type hints, segurança e desempenho. Use para todas as alterações de código Python.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/python-reviewer.md"
    },
    {
        "id": "pytorch-build-resolver",
        "title": "Resolvedor de Build PyTorch",
        "description": "Especialista em resolução de erros de treinamento, CUDA e runtime do PyTorch. Corrige incompatibilidades de forma de tensor, erros de dispositivo e problemas de DataLoader com mudanças mínimas.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/pytorch-build-resolver.md"
    },
    {
        "id": "refactor-cleaner",
        "title": "Limpador de Refatoração",
        "description": "Especialista em limpeza e consolidação de código morto. Use PROATIVAMENTE para remover código não utilizado, duplicatas e refatorar. Executa ferramentas de análise (knip, depcheck).",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/refactor-cleaner.md"
    },
    {
        "id": "rust-build-resolver",
        "title": "Resolvedor de Build Rust",
        "description": "Especialista em resolução de erros de dependência, compilação e build em Rust. Corrige erros do cargo build, problemas do borrow checker e problemas do Cargo.toml com mudanças mínimas.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/rust-build-resolver.md"
    },
    {
        "id": "rust-reviewer",
        "title": "Revisor Rust",
        "description": "Revisor de código Rust especialista em ownership, lifetimes, tratamento de erros, uso de unsafe e padrões idiomáticos. Use para todas as alterações de código Rust.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/rust-reviewer.md"
    },
    {
        "id": "security-reviewer",
        "title": "Revisor de Segurança",
        "description": "Especialista em detecção e mitigação de vulnerabilidades de segurança. Use PROATIVAMENTE após escrever código que lida com entrada de usuário, autenticação, endpoints de API ou dados sensíveis.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/security-reviewer.md"
    },
    {
        "id": "seo-specialist",
        "title": "Especialista em SEO",
        "description": "Especialista em SEO técnico para auditorias, otimização on-page, dados estruturados, Core Web Vitals e mapeamento de palavras-chave. Use para auditorias de sites, revisões de tags meta e planos de remediação de SEO.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/seo-specialist.md"
    },
    {
        "id": "silent-failure-hunter",
        "title": "Caçador de Falhas Silenciosas",
        "description": "Revisa o código em busca de falhas silenciosas, erros ignorados, fallbacks incorretos e falta de propagação de erros.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/silent-failure-hunter.md"
    },
    {
        "id": "swift-build-resolver",
        "title": "Resolvedor de Build Swift",
        "description": "Especialista em resolução de erros de dependência, compilação e build em Swift/Xcode. Corrige falhas do xcodebuild, problemas de dependência do SPM e problemas de assinatura de código com mudanças mínimas.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/swift-build-resolver.md"
    },
    {
        "id": "swift-reviewer",
        "title": "Revisor Swift",
        "description": "Revisor de código Swift especialista em design orientado a protocolos, semântica de valor, gerenciamento de memória ARC, concorrência Swift e padrões idiomáticos. Use para todas as alterações de código Swift.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/swift-reviewer.md"
    },
    {
        "id": "tdd-guide",
        "title": "Guia de TDD",
        "description": "Especialista em Test-Driven Development aplicando a metodologia de escrever testes primeiro. Use PROATIVAMENTE ao escrever novas funcionalidades, corrigir bugs ou refatorar código. Garante mais de 80% de cobertura de testes.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/tdd-guide.md"
    },
    {
        "id": "type-design-analyzer",
        "title": "Analisador de Design de Tipos",
        "description": "Analisa o design de tipos para encapsulamento, expressão de invariantes, utilidade e aplicação.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/type-design-analyzer.md"
    },
    {
        "id": "typescript-reviewer",
        "title": "Revisor TypeScript",
        "description": "Revisor de código TypeScript/JavaScript especialista em segurança de tipo, correção assíncrona, segurança Node/web e padrões idiomáticos. Use para todas as alterações de código TypeScript/JavaScript.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/typescript-reviewer.md"
    }
];

if (typeof module !== 'undefined') module.exports = eccAgentsData;
