const gsdData = {
    "GSD Agents": [
        {
            "id": "gsd-advisor-researcher",
            "title": "Advisor Researcher",
            "description": "Pesquisa uma área cinzenta de decisão e retorna uma tabela de comparação estruturada com justificativas. Invocado pelo modo consultor na fase de discussão.",
            "path": "contexto/get-shit-done/agents/gsd-advisor-researcher.md"
        },
        {
            "id": "gsd-ai-researcher",
            "title": "Ai Researcher",
            "description": "Pesquisa documentos oficiais de frameworks de IA para produzir guias prontos para implementação — melhores práticas, sintaxe e padrões centrais para o caso de uso. Invocado pelo orquestrador /gsd:ai-integration-phase.",
            "path": "contexto/get-shit-done/agents/gsd-ai-researcher.md"
        },
        {
            "id": "gsd-assumptions-analyzer",
            "title": "Assumptions Analyzer",
            "description": "Analisa profundamente a base de código de uma fase e retorna suposições estruturadas com evidências. Invocado pela fase de discussão.",
            "path": "contexto/get-shit-done/agents/gsd-assumptions-analyzer.md"
        },
        {
            "id": "gsd-code-fixer",
            "title": "Code Fixer",
            "description": "Aplica correções a problemas encontrados em code review no arquivo REVIEW.md. Lê arquivos, aplica correções inteligentes e realiza commits atômicos.",
            "path": "contexto/get-shit-done/agents/gsd-code-fixer.md"
        },
        {
            "id": "gsd-code-reviewer",
            "title": "Code Reviewer",
            "description": "Revisa os arquivos fonte em busca de bugs, vulnerabilidades e problemas de qualidade. Produz o REVIEW.md estruturado.",
            "path": "contexto/get-shit-done/agents/gsd-code-reviewer.md"
        },
        {
            "id": "gsd-codebase-mapper",
            "title": "Codebase Mapper",
            "description": "Explora a base de código e escreve documentos estruturados de análise (tecnologia, arquitetura, qualidade).",
            "path": "contexto/get-shit-done/agents/gsd-codebase-mapper.md"
        },
        {
            "id": "gsd-debug-session-manager",
            "title": "Debug Session Manager",
            "description": "Gerencia ciclos contínuos de debug, cria checkpoints e orquestra o diagnóstico em um ambiente isolado. Retorna o sumário da investigação.",
            "path": "contexto/get-shit-done/agents/gsd-debug-session-manager.md"
        },
        {
            "id": "gsd-debugger",
            "title": "Debugger",
            "description": "Investiga bugs usando o método científico, gerencia sessões de debug e cria pontos de controle da investigação.",
            "path": "contexto/get-shit-done/agents/gsd-debugger.md"
        },
        {
            "id": "gsd-doc-classifier",
            "title": "Doc Classifier",
            "description": "Classifica documentos de planejamento em categorias como ADR, PRD, SPEC, DOC. Extrai o escopo e referências cruzadas.",
            "path": "contexto/get-shit-done/agents/gsd-doc-classifier.md"
        },
        {
            "id": "gsd-doc-synthesizer",
            "title": "Doc Synthesizer",
            "description": "Sintetiza documentos de planejamento em um único contexto unificado. Aplica regras de precedência, resolve loops de referência e conflitos.",
            "path": "contexto/get-shit-done/agents/gsd-doc-synthesizer.md"
        },
        {
            "id": "gsd-doc-verifier",
            "title": "Doc Verifier",
            "description": "Verifica alegações factuais nos documentos gerados em relação ao código real existente. Retorna um JSON estruturado por doc.",
            "path": "contexto/get-shit-done/agents/gsd-doc-verifier.md"
        },
        {
            "id": "gsd-doc-writer",
            "title": "Doc Writer",
            "description": "Escreve e atualiza a documentação do projeto. Invocado com o contexto do projeto para criar ou atualizar specs.",
            "path": "contexto/get-shit-done/agents/gsd-doc-writer.md"
        },
        {
            "id": "gsd-domain-researcher",
            "title": "Domain Researcher",
            "description": "Pesquisa o domínio de negócios e a aplicação no mundo real do sistema IA. Sugere rubricas e critérios de avaliação baseados na indústria.",
            "path": "contexto/get-shit-done/agents/gsd-domain-researcher.md"
        },
        {
            "id": "gsd-eval-auditor",
            "title": "Eval Auditor",
            "description": "Realiza uma auditoria retrospectiva da cobertura de testes em um agente de IA. Produz o EVAL-REVIEW.md pontuando a qualidade.",
            "path": "contexto/get-shit-done/agents/gsd-eval-auditor.md"
        },
        {
            "id": "gsd-eval-planner",
            "title": "Eval Planner",
            "description": "Cria a estratégia de avaliação de uma fase de Inteligência Artificial, identifica falhas e recomenda ferramentas. Escreve a seção Guardrails do projeto.",
            "path": "contexto/get-shit-done/agents/gsd-eval-planner.md"
        },
        {
            "id": "gsd-executor",
            "title": "Executor",
            "description": "Executa planos do GSD de forma autônoma realizando commits atômicos, lidando com desvios, gerenciando checkpoints de aprovação e progresso.",
            "path": "contexto/get-shit-done/agents/gsd-executor.md"
        },
        {
            "id": "gsd-framework-selector",
            "title": "Framework Selector",
            "description": "Apresenta uma matriz de decisão para sugerir e ranquear os frameworks IA/LLM apropriados baseados no cenário de uso.",
            "path": "contexto/get-shit-done/agents/gsd-framework-selector.md"
        },
        {
            "id": "gsd-integration-checker",
            "title": "Integration Checker",
            "description": "Verifica fluxos complexos End-to-End (E2E) checando se os módulos e fases se conectam perfeitamente para entregar valor.",
            "path": "contexto/get-shit-done/agents/gsd-integration-checker.md"
        },
        {
            "id": "gsd-intel-updater",
            "title": "Intel Updater",
            "description": "Analisa o código estrutural e mantém relatórios de inteligência na pasta .planning/intel/ sempre atualizados.",
            "path": "contexto/get-shit-done/agents/gsd-intel-updater.md"
        },
        {
            "id": "gsd-nyquist-auditor",
            "title": "Nyquist Auditor",
            "description": "Preenche lacunas de validação gerando testes massivos e assegurando uma cobertura completa para os requisitos da fase.",
            "path": "contexto/get-shit-done/agents/gsd-nyquist-auditor.md"
        },
        {
            "id": "gsd-pattern-mapper",
            "title": "Pattern Mapper",
            "description": "Mapeia todos os padrões arquiteturais existentes no projeto gerando um PATTERNS.md para guiar o trabalho de desenvolvimento e evitar duplicações.",
            "path": "contexto/get-shit-done/agents/gsd-pattern-mapper.md"
        },
        {
            "id": "gsd-phase-researcher",
            "title": "Phase Researcher",
            "description": "Realiza uma pesquisa profunda investigando formas corretas de implementar o escopo. Produz o RESEARCH.md base da elaboração de planos.",
            "path": "contexto/get-shit-done/agents/gsd-phase-researcher.md"
        },
        {
            "id": "gsd-plan-checker",
            "title": "Plan Checker",
            "description": "Valida se um plano atingirá de fato o objetivo da fase através da engenharia reversa das entregas. Audita a viabilidade.",
            "path": "contexto/get-shit-done/agents/gsd-plan-checker.md"
        },
        {
            "id": "gsd-planner",
            "title": "Planner",
            "description": "Cria a engenharia completa de planos executáveis (GSD Phase) com detalhamento de tarefas, análise de dependências e estimativas de entrega.",
            "path": "contexto/get-shit-done/agents/gsd-planner.md"
        },
        {
            "id": "gsd-project-researcher",
            "title": "Project Researcher",
            "description": "Pesquisa um ecossistema inteiro de produtos para basear o Roadmap macro de um sistema de software complexo.",
            "path": "contexto/get-shit-done/agents/gsd-project-researcher.md"
        },
        {
            "id": "gsd-research-synthesizer",
            "title": "Research Synthesizer",
            "description": "Cruza e condensa inteligência advinda de multiplos agentes de pesquisa em um SUMMARY.md único super robusto.",
            "path": "contexto/get-shit-done/agents/gsd-research-synthesizer.md"
        },
        {
            "id": "gsd-roadmapper",
            "title": "Roadmapper",
            "description": "Arquiteta roadmaps com mapeamento de requisitos, cronograma em fases, engenharia de métricas de sucesso e verificação de cobertura.",
            "path": "contexto/get-shit-done/agents/gsd-roadmapper.md"
        },
        {
            "id": "gsd-security-auditor",
            "title": "Security Auditor",
            "description": "Verifica mitigação de ameaças através do mapeamento do plano tático em cima da arquitetura, alertando sobre riscos de segurança de código.",
            "path": "contexto/get-shit-done/agents/gsd-security-auditor.md"
        },
        {
            "id": "gsd-ui-auditor",
            "title": "Ui Auditor",
            "description": "Conduz auditoria proativa de interface do usuário, medindo design systems em cima dos 6 pilares de UI do framework para criar um UI-REVIEW.",
            "path": "contexto/get-shit-done/agents/gsd-ui-auditor.md"
        },
        {
            "id": "gsd-ui-checker",
            "title": "Ui Checker",
            "description": "Critica a estética e as validações funcionais baseadas no UI-SPEC.md gerando sentenças de validação (BLOCK, FLAG ou PASS).",
            "path": "contexto/get-shit-done/agents/gsd-ui-checker.md"
        },
        {
            "id": "gsd-ui-researcher",
            "title": "Ui Researcher",
            "description": "Produz o contrato de design do frontend UI-SPEC.md lendo documentações upstream e perguntando os detalhes necessários da interface.",
            "path": "contexto/get-shit-done/agents/gsd-ui-researcher.md"
        },
        {
            "id": "gsd-user-profiler",
            "title": "User Profiler",
            "description": "Agente comportamental que infere o perfil analítico do desenvolvedor por meio de seu histórico e mensagens, com alto nível de precisão.",
            "path": "contexto/get-shit-done/agents/gsd-user-profiler.md"
        },
        {
            "id": "gsd-verifier",
            "title": "Verifier",
            "description": "Engenheiro de teste autônomo focado em certificar que a base de código reflete verdadeiramente a promessa das tarefas dadas pelo projeto (VERIFICATION.md).",
            "path": "contexto/get-shit-done/agents/gsd-verifier.md"
        }
    ]
};
if(typeof module !== 'undefined') module.exports = gsdData;
