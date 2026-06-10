const skillsData = {
    "Agents (Advanced Skills)": [
        {
            "id": "accessibility",
            "category": "Agents (Advanced Skills)",
            "title": "Accessibility",
            "description": "Audit and improve web accessibility following WCAG 2.2 guidelines. Use when asked to \"improve accessibility\", \"a11y audit\", \"WCAG compliance\", \"screen reader support\", \"keyboard navigation\", or \"make accessible\".",
            "triggers": [
                "/sticky",
                "/quickref",
                "/figcaption",
                "/div",
                "/apg",
                "/video",
                "/button",
                "/mp4",
                "/www",
                "/label",
                "/fieldset",
                "/summary",
                "/figure",
                "/cli",
                "/axe",
                "/web-quality-audit",
                "/dequeuniversity",
                "/products",
                "/about",
                "/mp3",
                "/legend",
                "/rules",
                "/audio",
                "/span",
                "/ul",
                "/svg",
                "/style",
                "/example",
                "/details",
                "/li",
                "/nav"
            ],
            "dependencies": [
                "Web Quality Audit"
            ],
            "path": ".agents/skills/accessibility/SKILL.md"
        },
        {
            "id": "bash-defensive-patterns",
            "category": "Agents (Advanced Skills)",
            "title": "Bash Defensive Patterns",
            "description": "Master defensive Bash programming techniques for production-grade scripts. Use when writing robust shell scripts, CI/CD pipelines, or system utilities requiring fault tolerance and safety.",
            "triggers": [
                "/var",
                "/etc",
                "/temp2",
                "/null",
                "/config",
                "/path",
                "/dev",
                "/--output",
                "/bin",
                "/myapp",
                "/cache",
                "/bash",
                "/temp1"
            ],
            "dependencies": [],
            "path": ".agents/skills/bash-defensive-patterns/SKILL.md"
        },
        {
            "id": "frontend-design",
            "category": "Agents (Advanced Skills)",
            "title": "Frontend Design",
            "description": "Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.",
            "triggers": [
                "/refined",
                "/magazine",
                "/geometric",
                "/utilitarian",
                "/toy-like",
                "/beautifying",
                "/pastel",
                "/natural",
                "/raw"
            ],
            "dependencies": [],
            "path": ".agents/skills/frontend-design/SKILL.md"
        },
        {
            "id": "seo",
            "category": "Agents (Advanced Skills)",
            "title": "Seo",
            "description": "Optimize for search engine visibility and ranking. Use when asked to \"improve SEO\", \"optimize for search\", \"fix meta tags\", \"add structured data\", \"sitemap optimization\", or \"search engine optimization\".",
            "triggers": [
                "/api",
                "/lastmod",
                "/article-image",
                "/widget-maintenance",
                "/loc",
                "/www",
                "/test",
                "/jane-smith",
                "/blue-widget",
                "/blue-widget-2024-sale-discount",
                "/urlset",
                "/twitter",
                "/widgets",
                "/fr",
                "/core-web-vitals",
                "/subcategory",
                "/current-page",
                "/priority",
                "/how-to-use-widgets",
                "/linkedin",
                "/image",
                "/search",
                "/web-quality-audit",
                "/item",
                "/admin",
                "/products",
                "/developers",
                "/title",
                "/h2",
                "/robots",
                "/h4",
                "/schema",
                "/private",
                "/ld",
                "/company",
                "/validator",
                "/guides",
                "/logo",
                "/blue-widgets",
                "/rich-results",
                "/schemas",
                "/h3",
                "/script",
                "/authors",
                "/es",
                "/static",
                "/example",
                "/page",
                "/h1",
                "/url",
                "/sitemap",
                "/blog",
                "/category",
                "/changefreq"
            ],
            "dependencies": [
                "Core Web Vitals",
                "Web Quality Audit"
            ],
            "path": ".agents/skills/seo/SKILL.md"
        }
    ],
    "Uncategorized": [
        {
            "id": "business-growth",
            "category": "Uncategorized",
            "title": "Business Growth",
            "description": "\"4 skills de crescimento de negócios para Claude Code. Customer Success (health scoring, prevenção de churn), Sales Engineer (análise de RFP), Revenue Operations (pipeline, GTM), Contract & Proposal Writer (propostas e contratos). Ferramentas Python (apenas stdlib).\"",
            "triggers": [
                "/health",
                "/read",
                "/revenue-operations",
                "/scripts",
                "/pipeline",
                "/contract-and-proposal-writer",
                "/sales-engineer",
                "/customer-success-manager"
            ],
            "dependencies": [],
            "path": "business-growth/SKILL.md"
        },
        {
            "id": "c-level-advisor",
            "category": "Uncategorized",
            "title": "C Level Advisor",
            "description": "\"10 skills de assessoria C-level e plugins para Claude Code. CEO, CTO, COO, CPO, CMO, CFO, CRO, CISO, CHRO, Mentor Executivo. Reuniões de conselho com múltiplos papéis, roteamento estratégico e recomendações estruturadas. Para fundadores que precisam de suporte executivo para tomada de decisões.\"",
            "triggers": [
                "/cs"
            ],
            "dependencies": [],
            "path": "c-level-advisor/SKILL.md"
        },
        {
            "id": "carreira-educacao",
            "category": "Uncategorized",
            "title": "Carreira Educacao",
            "description": "\"Skills para construção de carreira, criação de cursos, mentoria e desenvolvimento de marca pessoal no mercado brasileiro. Use quando precisar otimizar LinkedIn, criar currículo ATS, estruturar um curso online, preparar entrevistas técnicas, montar negócio freelancer ou negociar salário.\"",
            "triggers": [
                "/perfil-linkedin",
                "/ano",
                "/read",
                "/framework-de-mentoria",
                "/busca-de-emprego",
                "/projeto",
                "/curriculo-e-cv",
                "/criador-de-cursos",
                "/marca-pessoal",
                "/carreira-educacao",
                "/rules",
                "/estrutura-freelancer",
                "/skill",
                "/negociacao-salarial",
                "/criador-de-portfolio",
                "/palestra-preparacao"
            ],
            "dependencies": [],
            "path": "carreira-educacao/SKILL.md"
        },
        {
            "id": "codigo-automacao",
            "category": "Uncategorized",
            "title": "Codigo Automacao",
            "description": "\"Skills para desenvolvimento de software, debug, APIs, automações no-code e uso avançado de ferramentas de IA para desenvolvimento. Use quando precisar de diagnóstico de bugs, construção de APIs, containerização, testes automatizados, integrações ou engenharia de prompts.\"",
            "triggers": [
                "/especialista-claude-code",
                "/read",
                "/n8n",
                "/rules",
                "/docker-compose",
                "/engenheiro-de-prompts",
                "/codigo-automacao",
                "/implementacao-de-auth",
                "/skill",
                "/especialista-em-debug",
                "/no-code-automacao",
                "/docstrings",
                "/integrador-de-webhooks",
                "/banco-de-dados-ops",
                "/automacao-de-testes",
                "/construtor-de-api",
                "/response"
            ],
            "dependencies": [],
            "path": "codigo-automacao/SKILL.md"
        },
        {
            "id": "conteudo-copy",
            "category": "Uncategorized",
            "title": "Conteudo Copy",
            "description": "|",
            "triggers": [
                "/solu",
                "/read",
                "/formal",
                "/gerador-de-headlines",
                "/escritor-de-emails",
                "/cart",
                "/profissional",
                "/criador-de-hooks",
                "/rules",
                "/jur",
                "/skill",
                "/conteudo-copy",
                "/sa",
                "/e-commerce"
            ],
            "dependencies": [],
            "path": "conteudo-copy/SKILL.md"
        },
        {
            "id": "design-branding",
            "category": "Uncategorized",
            "title": "Design Branding",
            "description": "\"Skills para identidade visual, criação de materiais de vendas, decks executivos e assets B2B com briefing para designers. Use quando precisar criar, revisar ou orientar projetos de design, branding, apresentações e materiais visuais para o mercado brasileiro.\"",
            "triggers": [
                "/read",
                "/design-branding",
                "/rules",
                "/skill",
                "/reels",
                "/caminho"
            ],
            "dependencies": [],
            "path": "design-branding/SKILL.md"
        },
        {
            "id": "direcao-criativa",
            "category": "Uncategorized",
            "title": "Direcao Criativa",
            "description": "\"Skills para desenvolvimento de conceito criativo, direção de arte, naming, campanhas 360° e storytelling visual para marcas brasileiras. Use quando precisar criar conceitos de campanha, nomear produtos, estruturar narrativas de marca ou orientar produções criativas.\"",
            "triggers": [
                "/read",
                "/aspiracionais",
                "/direcao-criativa",
                "/rules",
                "/diretas",
                "/skill",
                "/caminho"
            ],
            "dependencies": [],
            "path": "direcao-criativa/SKILL.md"
        },
        {
            "id": "engineering",
            "category": "Uncategorized",
            "title": "Engineering",
            "description": "\"25 skills e plugins avançados de engenharia para Claude Code. Design de agentes, RAG, servidores MCP, CI/CD, design de banco de dados, observabilidade, auditoria de segurança e gerenciamento de releases.\"",
            "triggers": [
                "/agent-designer",
                "/read"
            ],
            "dependencies": [],
            "path": "engineering/SKILL.md"
        },
        {
            "id": "engineering-team",
            "category": "Uncategorized",
            "title": "Engineering Team",
            "description": "\"23 skills de engenharia prontas para produção para Claude Code. Arquitetura, frontend, backend, QA, DevOps, segurança, IA/ML, engenharia de dados, Playwright, Stripe, AWS, MS365. ferramentas Node.js, TypeScript e scripts utilitários.\"",
            "triggers": [
                "/senior-fullstack",
                "/read",
                "/scripts"
            ],
            "dependencies": [],
            "path": "engineering-team/SKILL.md"
        },
        {
            "id": "finance",
            "category": "Uncategorized",
            "title": "Finance",
            "description": "\"Skill de agente de analista financeiro para Claude Code. Análise de índices, avaliação DCF, variação orçamentária, previsões contínuas. 4 ferramentas Python (somente stdlib).\"",
            "triggers": [
                "/dcf",
                "/read",
                "/financial-analyst",
                "/budget",
                "/scripts",
                "/forecast",
                "/ratio"
            ],
            "dependencies": [],
            "path": "finance/SKILL.md"
        },
        {
            "id": "financeiro-compliance",
            "category": "Uncategorized",
            "title": "Financeiro Compliance",
            "description": "|",
            "triggers": [
                "/ano",
                "/read",
                "/impostos-br",
                "/rules",
                "/fluxo-caixa",
                "/skill",
                "/financeiro-compliance",
                "/tribut",
                "/conformidade-lgpd",
                "/advogado",
                "/acidente"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/SKILL.md"
        },
        {
            "id": "juridico-advocacia",
            "category": "Uncategorized",
            "title": "Juridico Advocacia",
            "description": "\"Skills para advogados e gestores jurídicos: petições, contratos, captação de clientes, precificação e conformidade com o direito brasileiro. Use quando precisar estruturar documentos jurídicos, estratégias para escritórios de advocacia ou orientação sobre legislação brasileira.\"",
            "triggers": [
                "/read",
                "/rules",
                "/2018",
                "/executado",
                "/2015",
                "/skill",
                "/2002",
                "/juridico-advocacia",
                "/2021",
                "/caminho",
                "/2017"
            ],
            "dependencies": [],
            "path": "juridico-advocacia/SKILL.md"
        },
        {
            "id": "lideranca-equipes",
            "category": "Uncategorized",
            "title": "Lideranca Equipes",
            "description": "\"Skills para gestão de pessoas, feedback estruturado, desenvolvimento de times e liderança em contexto de startups e PMEs brasileiras. Use quando precisar de frameworks de feedback, estruturar 1:1s, resolver conflitos, desenvolver cultura de equipe ou fazer a transição para liderança.\"",
            "triggers": [
                "/2022",
                "/lideranca-equipes",
                "/read",
                "/rules",
                "/manager",
                "/skill",
                "/caminho"
            ],
            "dependencies": [],
            "path": "lideranca-equipes/SKILL.md"
        },
        {
            "id": "marketing-skill",
            "category": "Uncategorized",
            "title": "Marketing Skill",
            "description": "\"42 skills e plugins de marketing para agentes Claude Code. 7 pods: conteúdo, SEO, CRO, canais, crescimento, inteligência, vendas. Contexto base + roteador de orquestração. 27 ferramentas Python (somente stdlib).\"",
            "triggers": [
                "/analytics-tracking",
                "/read",
                "/brand",
                "/ad",
                "/pricing-strategy",
                "/ad-creative",
                "/scripts",
                "/humanizer",
                "/content-humanizer",
                "/content",
                "/pricing",
                "/tracking",
                "/marketing-ops",
                "/content-production"
            ],
            "dependencies": [],
            "path": "marketing-skill/SKILL.md"
        },
        {
            "id": "marketing-vendas",
            "category": "Uncategorized",
            "title": "Marketing Vendas",
            "description": "|",
            "triggers": [
                "/60",
                "/read",
                "/script-vendas",
                "/funil-vendas",
                "/90",
                "/rules",
                "/marketing-vendas",
                "/skill",
                "/proposta-comercial",
                "/contador",
                "/03"
            ],
            "dependencies": [],
            "path": "marketing-vendas/SKILL.md"
        },
        {
            "id": "operacoes-rh",
            "category": "Uncategorized",
            "title": "Operacoes Rh",
            "description": "|",
            "triggers": [
                "/60",
                "/ano",
                "/read",
                "/90",
                "/semana",
                "/criador-de-sop",
                "/gestao-de-okrs",
                "/rules",
                "/n8n",
                "/skill",
                "/operacoes-rh",
                "/onboarding",
                "/dia"
            ],
            "dependencies": [],
            "path": "operacoes-rh/SKILL.md"
        },
        {
            "id": "prd-generator",
            "category": "Uncategorized",
            "title": "Prd Generator",
            "description": "\"Gerador de PRD (Product Requirements Document) em portugues-BR a partir de um Product Brief. Conduz entrevista guiada com 6 perguntas-chave (Nome, Overview, Persona, Objetivo, Requisitos Funcionais, Modelo de Negocio) e gera um PRD completo em Markdown com 9 secoes (Visao Geral, Funcionalidades, Fluxos, Diagrama Mermaid, Design UI, Modelo de Dados com ER e SQL, Arquitetura, Metricas, Roadmap), salvando em .prd/prd_NOME.md para uso em Claude Code. Use SEMPRE que o usuario mencionar gerar PRD, criar PRD, Product Requirements Document, documento de requisitos, transformar brief em PRD, estruturar product brief, preparar requisitos para Lovable Bolt V0, documentar produto, ou enviar um product brief pedindo estruturacao. Trigger TAMBEM quando descrever ideia de produto ou app pedindo estruturar, documentar ou preparar para desenvolvimento. Nao use para specs tecnicas de feature isolada (use sdd-generator).\"",
            "triggers": [
                "/auditoria",
                "/perfis",
                "/prd",
                "/criar",
                "/example",
                "/produto",
                "/cores",
                "/pr",
                "/senha"
            ],
            "dependencies": [],
            "path": "prd-generator/SKILL.md"
        },
        {
            "id": "product-team",
            "category": "Uncategorized",
            "title": "Product Team",
            "description": "\"10 skills e plugins de agentes de produto para Claude Code. Kit de ferramentas para PM (RICE), PO ágil, estrategista de produto (OKR), pesquisador UX, sistema de UI design, análise competitiva, gerador de landing page, scaffolder SaaS, resumidor de pesquisas. Ferramentas Python (somente stdlib).\"",
            "triggers": [
                "/read",
                "/scripts",
                "/product-manager-toolkit",
                "/rice",
                "/okr"
            ],
            "dependencies": [],
            "path": "product-team/SKILL.md"
        },
        {
            "id": "produto-ecommerce",
            "category": "Uncategorized",
            "title": "Produto Ecommerce",
            "description": "\"Skills para lançamento de produtos digitais, estratégias PLG, operações de e-commerce e métricas SaaS com contexto do mercado brasileiro. Use quando precisar de playbooks de lançamento, análise de churn, precificação em R$, operações de marketplace BR ou métricas de produto.\"",
            "triggers": [
                "/read",
                "/analise-de-churn",
                "/upsell-e-crosssell",
                "/estrategia-plg",
                "/precificacao-saas",
                "/analitica-de-produto",
                "/rules",
                "/estrategia-marketplace",
                "/cliente",
                "/lancamento-produto",
                "/skill",
                "/operacoes-ecommerce",
                "/roadmap-de-produto",
                "/produto-ecommerce",
                "/abandono-de-carrinho",
                "/devolu"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/SKILL.md"
        },
        {
            "id": "project-management",
            "category": "Uncategorized",
            "title": "Project Management",
            "description": "\"6 skills de gerenciamento de projetos para Claude Code. Senior PM, scrum master, especialista em Jira (JQL), especialista em Confluence, administrador Atlassian e criador de templates. Integração MCP para automação ao vivo no Jira/Confluence.\"",
            "triggers": [
                "/read",
                "/scripts",
                "/project",
                "/jira-expert",
                "/velocity"
            ],
            "dependencies": [],
            "path": "project-management/SKILL.md"
        },
        {
            "id": "ra-qm-team",
            "category": "Uncategorized",
            "title": "Ra Qm Team",
            "description": "\"12 skills e plugins de agentes para Assuntos Regulatórios e Gestão da Qualidade no Claude Code. Cobre ISO 13485 QMS, MDR 2017/745, FDA 510(k)/PMA, ISO 27001 ISMS, LGPD/DSGVO, gestão de riscos (ISO 14971), CAPA, controle de documentos e auditoria — para o mercado brasileiro e internacional. Python tools (somente stdlib).\"",
            "triggers": [
                "/read",
                "/risk",
                "/745",
                "/scripts",
                "/gdpr",
                "/regulatory-affairs-head"
            ],
            "dependencies": [],
            "path": "ra-qm-team/SKILL.md"
        },
        {
            "id": "rotina-organizacao",
            "category": "Uncategorized",
            "title": "Rotina Organizacao",
            "description": "\"Skills de produtividade pessoal com metodologias GTD, time blocking, gestão de energia e organização de projetos pessoais. Use quando precisar implementar sistema de tarefas, planejar agenda, criar checklists reutilizáveis, delegar eficazmente ou construir hábitos sustentáveis.\"",
            "triggers": [
                "/rotina-organizacao",
                "/read",
                "/delegacao",
                "/prioridades",
                "/caixa-de-entrada-zero",
                "/semana",
                "/20",
                "/habitos",
                "/foco-e-trabalho-profundo",
                "/equilibrio-vida",
                "/rules",
                "/dia",
                "/skill",
                "/criador-de-checklists",
                "/bloqueio-de-tempo",
                "/revisao-semanal",
                "/sistema-gtd"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/SKILL.md"
        },
        {
            "id": "sdd-generator",
            "category": "Uncategorized",
            "title": "Sdd Generator",
            "description": ">",
            "triggers": [
                "/como-executar",
                "/executar-specs-template",
                "/modificar",
                "/valida",
                "/spec-template",
                "/exemplos-decomposicao",
                "/regras-de-nomenclatura"
            ],
            "dependencies": [],
            "path": "sdd-generator/SKILL.md"
        },
        {
            "id": "seguranca-mvs",
            "category": "Uncategorized",
            "title": "Seguranca Mvs",
            "description": "Ative este CISO virtual senior sempre que o usuario mencionar seguranca de servidores, seguranca de aplicacoes, LGPD, protecao de dados pessoais, controle de acesso, IAM, hardening, pentest, vulnerabilidades, OWASP, resposta a incidentes, DevSecOps, ISO 27001, NIST, compliance, ANPD, ataques, malware, ransomware, vazamento de dados, ou qualquer tema de ciberseguranca. Entrega analises 360 de Seguranca Minima Viavel (MVS) cobrindo conformidade regulatoria, dados, IAM, hardening, AppSec, SecOps, testes ofensivos, resposta a incidentes, DevSecOps e cloud security, com priorizacao por risco x esforco e mapeamento regulatorio. Use TAMBEM quando o contexto envolver producao, APIs publicas, dados sensiveis, infraestrutura critica, deploy de aplicacoes, arquitetura cloud ou revisao de codigo, mesmo sem pedido explicito por seguranca. Responde em portugues do Brasil com tom executivo direto.",
            "triggers": [
                "/dominios",
                "/servidor",
                "/reputacional",
                "/complexidade",
                "/armazenam",
                "/performance",
                "/lgpd",
                "/playbooks-ir",
                "/2024"
            ],
            "dependencies": [],
            "path": "seguranca-mvs/SKILL.md"
        },
        {
            "id": "seo-analitica",
            "category": "Uncategorized",
            "title": "Seo Analitica",
            "description": "\"Skills para otimização de SEO técnico, análise de dados, criação de dashboards e inteligência de negócio para empresas brasileiras. Use quando precisar auditar SEO, configurar GA4, criar relatórios de dados, definir KPIs ou garantir conformidade com LGPD na coleta de dados.\"",
            "triggers": [
                "/read",
                "/2023",
                "/rules",
                "/2018",
                "/skill",
                "/caminho",
                "/seo-analitica"
            ],
            "dependencies": [],
            "path": "seo-analitica/SKILL.md"
        }
    ],
    "Business Growth": [
        {
            "id": "account-manager",
            "category": "Business Growth",
            "title": "Account Manager",
            "description": "\"Gerente de Contas (Account Manager) B2B sênior para gestão de carteira, QBRs, expansão (upsell/cross-sell), renovação, prevenção de churn, relacionamento executivo e planos de contas estratégicas. Use ao construir Account Plan, preparar QBR, planejar upsell, renovar contratos, mapear stakeholders, conduzir executive business review ou quando o usuário mencionar Account Manager, AM, Key Account, KAM, renovação, upsell, cross-sell, QBR ou expansão de receita.\"",
            "triggers": [
                "/60",
                "/ano",
                "/90",
                "/tri",
                "/red",
                "/cro-advisor",
                "/usu",
                "/contrato",
                "/anual",
                "/c-level-advisor",
                "/cross-sell"
            ],
            "dependencies": [],
            "path": "business-growth/account-manager/SKILL.md"
        },
        {
            "id": "contract-and-proposal-writer",
            "category": "Business Growth",
            "title": "Contract And Proposal Writer",
            "description": "\"Gerador de contratos e propostas comerciais para o mercado brasileiro. Contratos de prestação de serviço, proposta comercial, SOW, NDA, MSA — todos adaptados à legislação brasileira (Código Civil, CLT, LGPD). Use quando precisar criar contratos de desenvolvimento, propostas para clientes, acordos de confidencialidade, contratos de consultoria ou contratos de parceria comercial.\"",
            "triggers": [
                "/60",
                "/ano",
                "/cart",
                "/96",
                "/90",
                "/05",
                "/98",
                "/domic",
                "/hora",
                "/18",
                "/2001"
            ],
            "dependencies": [],
            "path": "business-growth/contract-and-proposal-writer/SKILL.md"
        },
        {
            "id": "customer-success-manager",
            "category": "Business Growth",
            "title": "Customer Success Manager",
            "description": "Monitora saúde do cliente, prevê risco de churn e identifica oportunidades de expansão usando modelos de pontuação ponderada para sucesso do cliente SaaS. Use ao analisar contas de clientes, revisar métricas de retenção, pontuar clientes em risco, ou quando o usuário mencionar churn, pontuações de saúde do cliente, oportunidades de upsell, receita de expansão, análise de retenção ou análise de clientes. Executa três ferramentas Python CLI para produzir pontuações de saúde determinísticas, tiers de risco de churn e recomendações de expansão priorizadas em segmentos Enterprise, Mid-Market e PME.",
            "triggers": [
                "/health",
                "/executive",
                "/sample",
                "/cs-metrics-benchmarks",
                "/plataforma",
                "/expansion",
                "/cs-playbooks",
                "/health-scoring-framework",
                "/churn",
                "/onboarding",
                "/qbr",
                "/success"
            ],
            "dependencies": [],
            "path": "business-growth/customer-success-manager/SKILL.md"
        },
        {
            "id": "partnerships-manager",
            "category": "Business Growth",
            "title": "Partnerships Manager",
            "description": "\"Partnerships Manager / Business Development sênior para parcerias estratégicas, alianças tecnológicas, canal de vendas (resellers, integradores), co-marketing, programas de afiliados, marketplace e go-to-market conjunto. Use ao estruturar programa de parceiros, negociar acordos comerciais, construir canal indireto, planejar co-marketing, priorizar parceiros ou quando o usuário mencionar partnerships, BD, business development, canal, parceiros, reseller, integrador, marketplace ou aliança.\"",
            "triggers": [
                "/ano",
                "/verticalmente",
                "/c-level-advisor",
                "/email",
                "/cro-advisor",
                "/marketing-skill",
                "/launch-strategy",
                "/influenciado",
                "/cmo-advisor",
                "/comprometimento"
            ],
            "dependencies": [],
            "path": "business-growth/partnerships-manager/SKILL.md"
        },
        {
            "id": "revenue-operations",
            "category": "Business Growth",
            "title": "Revenue Operations",
            "description": "Analisa saúde do pipeline de vendas, precisão de previsão de receita e métricas de eficiência go-to-market para otimização de receita SaaS. Use ao analisar cobertura do pipeline de vendas, prever receita, avaliar desempenho go-to-market, revisar métricas de vendas, avaliar análise de pipeline, rastrear precisão de previsão com MAPE, calcular eficiência GTM ou medir eficiência de vendas e unit economics para equipes SaaS.",
            "triggers": [
                "/integra",
                "/sample",
                "/mensal",
                "/gtm",
                "/forecast",
                "/pipeline-management-framework",
                "/expected",
                "/revops-metrics-guide",
                "/gtm-efficiency-benchmarks",
                "/pipeline"
            ],
            "dependencies": [],
            "path": "business-growth/revenue-operations/SKILL.md"
        },
        {
            "id": "sales-engineer",
            "category": "Business Growth",
            "title": "Sales Engineer",
            "description": "Analisa respostas de RFP/RFI para lacunas de cobertura, constrói matrizes de comparação de funcionalidades competitivas e planeja engajamentos de prova de conceito (POC) para engenharia de pré-vendas. Use ao responder a RFPs, licitações ou solicitações de proposta; comparar funcionalidades do produto contra concorrentes; planejar ou pontuar um POC ou demonstração de vendas para o cliente; preparar uma proposta técnica; ou realizar análise competitiva de vitórias/perdas. Lida com tarefas descritas como 'resposta a RFP', 'resposta a licitação', 'resposta a proposta', 'comparação de concorrente', 'matriz de funcionalidades', 'planejamento de POC', 'preparação de demo de vendas' ou 'engenharia de pré-vendas'.",
            "triggers": [
                "/rfp",
                "/sample",
                "/technical",
                "/demo",
                "/perda",
                "/expected",
                "/perdas",
                "/competitive",
                "/poc",
                "/no-go",
                "/rfp-response-guide",
                "/poc-best-practices",
                "/marketing-skill",
                "/product-team",
                "/c-level-advisor",
                "/competitive-positioning-framework",
                "/customer-success-manager"
            ],
            "dependencies": [],
            "path": "business-growth/sales-engineer/SKILL.md"
        }
    ],
    "C Level Advisor": [
        {
            "id": "agent-protocol",
            "category": "C Level Advisor",
            "title": "Agent Protocol",
            "description": "\"Protocolo de comunicação entre agentes para times de C-suite. Define sintaxe de invocação, prevenção de loops, regras de isolamento e formatos de resposta. Use quando agentes do C-suite precisam consultar uns aos outros, coordenar análises multifuncionais ou conduzir reuniões de conselho com múltiplos papéis.\"",
            "triggers": [
                "/60",
                "/invocation-patterns",
                "/90"
            ],
            "dependencies": [],
            "path": "c-level-advisor/agent-protocol/SKILL.md"
        },
        {
            "id": "board-deck-builder",
            "category": "C Level Advisor",
            "title": "Board Deck Builder",
            "description": "\"Monta apresentações abrangentes para conselhos e atualizações para investidores, reunindo perspectivas de todos os papéis do C-suite. Use ao preparar reuniões de conselho, atualizações para investidores, revisões trimestrais de negócios ou narrativas de captação. Cobre estrutura, framework narrativo, entrega de más notícias e erros comuns.\"",
            "triggers": [
                "/risco",
                "/deck-frameworks",
                "/vis",
                "/board-deck-template",
                "/valor",
                "/board-deck",
                "/travados",
                "/data",
                "/awareness"
            ],
            "dependencies": [],
            "path": "c-level-advisor/board-deck-builder/SKILL.md"
        },
        {
            "id": "board-meeting",
            "category": "C Level Advisor",
            "title": "Board Meeting",
            "description": "\"Protocolo de reunião de conselho com múltiplos agentes para tomada de decisões. Executa uma deliberação estruturada em 6 fases: carregamento de contexto, contribuições independentes do C-suite (isoladas, sem contaminação cruzada), análise crítica, síntese, revisão do fundador e extração de decisão. Use quando o usuário invocar /cs:board, solicitar uma reunião de conselho ou querer deliberação executiva estruturada com múltiplas perspectivas sobre uma questão estratégica.\"",
            "triggers": [
                "/meeting-facilitation",
                "/meeting-agenda",
                "/meeting-minutes",
                "/company-context",
                "/board-meetings",
                "/org",
                "/decisions",
                "/cs"
            ],
            "dependencies": [],
            "path": "c-level-advisor/board-meeting/SKILL.md"
        },
        {
            "id": "caio-advisor",
            "category": "C Level Advisor",
            "title": "Caio Advisor",
            "description": "\"Assessor de Chief AI Officer (CAIO) para estratégia de IA corporativa, governança de IA, build vs. buy, plataforma de ML, AI safety, ROI e conformidade regulatória (LGPD, AI Act, PL 2338/23 Brasil). Use ao definir estratégia de IA, priorizar casos de uso, estruturar time de IA, governar modelos em produção, preparar apresentações para o conselho sobre IA ou quando o usuário mencionar CAIO, Chief AI Officer, estratégia de IA, IA generativa corporativa, AI governance, LLMOps, responsible AI ou AI Act.\"",
            "triggers": [
                "/ano",
                "/23",
                "/rag-architect",
                "/semana",
                "/mcp-server-builder",
                "/baixo",
                "/engineering",
                "/ai-security",
                "/senior-ml-engineer",
                "/propriet",
                "/engineering-team",
                "/15"
            ],
            "dependencies": [],
            "path": "c-level-advisor/caio-advisor/SKILL.md"
        },
        {
            "id": "cdo-advisor",
            "category": "C Level Advisor",
            "title": "Cdo Advisor",
            "description": "\"Assessor de Chief Data Officer (CDO) para estratégia de dados, governança, arquitetura de plataforma de dados, qualidade, LGPD e monetização. Use ao definir estratégia de dados corporativa, desenhar data governance, implementar data mesh/lakehouse, garantir conformidade com LGPD, preparar relatórios para conselho sobre dados, ou quando o usuário mencionar CDO, Chief Data Officer, estratégia de dados, governança de dados, data platform, data quality, data catalog, MDM ou monetização de dados.\"",
            "triggers": [
                "/rag-architect",
                "/engineering",
                "/database-designer",
                "/ra-qm-team",
                "/lakehouse",
                "/18",
                "/gdpr-dsgvo-expert"
            ],
            "dependencies": [],
            "path": "c-level-advisor/cdo-advisor/SKILL.md"
        },
        {
            "id": "ceo-advisor",
            "category": "C Level Advisor",
            "title": "Ceo Advisor",
            "description": "\"Orientação de liderança executiva para tomada de decisões estratégicas, desenvolvimento organizacional e gestão de partes interessadas. Use ao planejar estratégia, preparar apresentações para o conselho, gerenciar investidores, desenvolver cultura organizacional, tomar decisões executivas, captar recursos ou quando o usuário mencionar CEO, planejamento estratégico, reuniões de conselho, atualizações para investidores, liderança organizacional ou estratégia executiva.\"",
            "triggers": [
                "/financial",
                "/executive",
                "/6m",
                "/strategy",
                "/5a",
                "/1a",
                "/2a",
                "/mercados",
                "/leadership",
                "/10",
                "/pessimista",
                "/cultura",
                "/3a",
                "/12m",
                "/otimista",
                "/compliance",
                "/board"
            ],
            "dependencies": [],
            "path": "c-level-advisor/ceo-advisor/SKILL.md"
        },
        {
            "id": "cfo-advisor",
            "category": "C Level Advisor",
            "title": "Cfo Advisor",
            "description": "\"Liderança financeira para startups e empresas em escala. Modelagem financeira, unit economics, estratégia de captação, gestão de caixa e pacotes financeiros para o conselho. Use ao construir modelos financeiros, analisar unit economics, planejar captação, gerenciar runway de caixa, preparar materiais para o conselho ou quando o usuário mencionar CFO, burn rate, runway, captação, unit economics, LTV, CAC, term sheets ou estratégia financeira.\"",
            "triggers": [
                "/financial",
                "/cash",
                "/otimista",
                "/burn",
                "/pessimista",
                "/unit",
                "/fundraising"
            ],
            "dependencies": [],
            "path": "c-level-advisor/cfo-advisor/SKILL.md"
        },
        {
            "id": "change-management",
            "category": "C Level Advisor",
            "title": "Change Management",
            "description": "\"Framework para implementar mudanças organizacionais sem caos. Cobre o modelo ADKAR adaptado para startups, templates de comunicação, padrões de resistência e gestão de fadiga de mudança. Lida com mudanças de processo, reestruturações organizacionais, pivôs estratégicos e mudanças culturais. Use ao anunciar uma reorganização, trocar ferramentas, pivotar a estratégia, encerrar um produto, mudar lideranças ou quando o usuário mencionar gestão de mudanças, rollout de mudança, gestão de resistência, mudança organizacional, reorg ou comunicação de pivô.\"",
            "triggers": [
                "/fus",
                "/processo",
                "/change-playbook"
            ],
            "dependencies": [],
            "path": "c-level-advisor/change-management/SKILL.md"
        },
        {
            "id": "chief-of-staff",
            "category": "C Level Advisor",
            "title": "Chief Of Staff",
            "description": "\"Camada de orquestração do C-suite. Roteia perguntas do fundador para o(s) papel(is) de assessor correto(s), aciona reuniões de conselho com múltiplos papéis para decisões complexas, sintetiza saídas e rastreia decisões. Toda interação com o C-suite começa aqui. Carrega o contexto da empresa automaticamente.\"",
            "triggers": [
                "/synthesis-framework",
                "/routing-matrix",
                "/decision-log"
            ],
            "dependencies": [],
            "path": "c-level-advisor/chief-of-staff/SKILL.md"
        },
        {
            "id": "chro-advisor",
            "category": "C Level Advisor",
            "title": "Chro Advisor",
            "description": "\"Liderança de pessoas para empresas em escala. Estratégia de contratação, design de remuneração, estrutura organizacional, cultura e retenção. Use ao construir planos de contratação, projetar frameworks de remuneração, reestruturar times, gerenciar desempenho, construir cultura ou quando o usuário mencionar CHRO, RH, estratégia de pessoas, talentos, headcount, remuneração, design organizacional, retenção ou gestão de desempenho.\"",
            "triggers": [
                "/60",
                "/comp",
                "/people",
                "/90",
                "/atualiza",
                "/org",
                "/hiring"
            ],
            "dependencies": [],
            "path": "c-level-advisor/chro-advisor/SKILL.md"
        },
        {
            "id": "ciso-advisor",
            "category": "C Level Advisor",
            "title": "Ciso Advisor",
            "description": "\"Liderança de segurança para empresas em estágio de crescimento. Quantificação de risco em reais, roadmap de compliance (SOC 2/ISO 27001/LGPD/ANVISA), estratégia de arquitetura de segurança, liderança de resposta a incidentes e reporte de segurança ao conselho. Use ao construir programas de segurança, justificar orçamento de segurança, selecionar frameworks de compliance, gerenciar incidentes, avaliar risco de fornecedores ou quando o usuário mencionar CISO, estratégia de segurança, roadmap de compliance, zero trust ou reporte de segurança ao conselho.\"",
            "triggers": [
                "/dados",
                "/incidente",
                "/risk",
                "/security",
                "/compliance",
                "/18"
            ],
            "dependencies": [],
            "path": "c-level-advisor/ciso-advisor/SKILL.md"
        },
        {
            "id": "clo-advisor",
            "category": "C Level Advisor",
            "title": "Clo Advisor",
            "description": "\"Assessor de Chief Legal Officer (CLO) / General Counsel para estratégia jurídica corporativa, compliance BR, contratos, societário, M&A, disputas, privacidade (LGPD), trabalhista (CLT/PJ), tributário e relações com reguladores. Use ao estruturar departamento jurídico, avaliar riscos legais de decisões estratégicas, negociar termos de investimento, preparar IPO, gerenciar litígios relevantes ou quando o usuário mencionar CLO, General Counsel, jurídico, compliance, LGPD, CLT, societário, M&A ou disputas.\"",
            "triggers": [
                "/08",
                "/ano",
                "/13",
                "/contract-and-proposal-writer",
                "/ra-qm-team",
                "/business-growth",
                "/18",
                "/gdpr-dsgvo-expert"
            ],
            "dependencies": [],
            "path": "c-level-advisor/clo-advisor/SKILL.md"
        },
        {
            "id": "cmo-advisor",
            "category": "C Level Advisor",
            "title": "Cmo Advisor",
            "description": "\"Liderança de marketing para empresas em escala. Posicionamento de marca, design do modelo de crescimento, alocação de orçamento de marketing e design da organização de marketing. Use ao projetar estratégia de marca, selecionar modelos de crescimento (PLG vs. liderado por vendas vs. liderado por comunidade), alocar orçamentos de marketing, construir times de marketing ou quando o usuário mencionar CMO, estratégia de marca, modelo de crescimento, CAC, LTV, mix de canais ou ROI de marketing.\"",
            "triggers": [
                "/loss",
                "/brand",
                "/growth",
                "/marketing"
            ],
            "dependencies": [],
            "path": "c-level-advisor/cmo-advisor/SKILL.md"
        },
        {
            "id": "company-os",
            "category": "C Level Advisor",
            "title": "Company Os",
            "description": "\"O meta-framework de como uma empresa funciona — o tecido conjuntivo entre todos os papéis do C-suite. Cobre seleção do sistema operacional (EOS, Scaling Up, OKR-nativo, híbrido), gráficos de accountability, scorecards, ritmo de reuniões, resolução de problemas e rocks de 90 dias. Use ao configurar operações da empresa, selecionar um framework de gestão, projetar ritmos de reuniões, construir sistemas de accountability, implementar OKRs ou quando o usuário mencionar EOS, Scaling Up, sistema operacional, reuniões L10, rocks, scorecard, gráfico de accountability ou planejamento trimestral.\"",
            "triggers": [
                "/semana",
                "/amarelo",
                "/10",
                "/verde",
                "/implementation-guide",
                "/os-comparison",
                "/fora",
                "/funcion"
            ],
            "dependencies": [],
            "path": "c-level-advisor/company-os/SKILL.md"
        },
        {
            "id": "competitive-intel",
            "category": "C Level Advisor",
            "title": "Competitive Intel",
            "description": "\"Rastreamento sistemático de concorrentes que alimenta o posicionamento do CMO, battlecards do CRO e decisões de roadmap do CPO. Use ao analisar concorrentes, construir battlecards de vendas, rastrear movimentos de mercado, posicionar-se contra alternativas ou quando o usuário mencionar inteligência competitiva, análise competitiva, pesquisa de concorrentes, battlecards, win/loss ou posicionamento de mercado.\"",
            "triggers": [
                "/remova",
                "/battlecard-template",
                "/perdas",
                "/ci",
                "/ci-playbook",
                "/loss"
            ],
            "dependencies": [],
            "path": "c-level-advisor/competitive-intel/SKILL.md"
        },
        {
            "id": "context-engine",
            "category": "C Level Advisor",
            "title": "Context Engine",
            "description": "\"Carrega e gerencia o contexto da empresa para todos os skills de assessor do C-suite. Lê ~/.claude/company-context.md, detecta contexto desatualizado (>90 dias), enriquece o contexto durante conversas e aplica regras de privacidade/anonimização antes de chamadas externas de API.\"",
            "triggers": [
                "/cs",
                "/anonymization-protocol",
                "/company-context",
                "/incompleto",
                "/anonimiza"
            ],
            "dependencies": [],
            "path": "c-level-advisor/context-engine/SKILL.md"
        },
        {
            "id": "coo-advisor",
            "category": "C Level Advisor",
            "title": "Coo Advisor",
            "description": "\"Liderança de operações para empresas em escala. Design de processos, execução de OKRs, cadência operacional e playbooks de escala. Use ao projetar operações, configurar OKRs, construir processos, escalar times, analisar gargalos, planejar cadência operacional ou quando o usuário mencionar COO, operações, melhoria de processos, OKRs, escala, eficiência operacional ou execução.\"",
            "triggers": [
                "/scaling",
                "/process",
                "/ops",
                "/okr"
            ],
            "dependencies": [],
            "path": "c-level-advisor/coo-advisor/SKILL.md"
        },
        {
            "id": "cpo-advisor",
            "category": "C Level Advisor",
            "title": "Cpo Advisor",
            "description": "\"Liderança de produto para empresas em escala. Visão de produto, estratégia de portfólio, product-market fit e design da organização de produto. Use ao definir visão de produto, gerenciar portfólio de produtos, medir PMF, projetar times de produto, priorizar no nível de portfólio, reportar ao conselho sobre produto ou quando o usuário mencionar CPO, estratégia de produto, product-market fit, organização de produto, priorização de portfólio ou estratégia de roadmap.\"",
            "triggers": [
                "/pmf",
                "/manter",
                "/portfolio",
                "/product",
                "/encerrar",
                "/investir"
            ],
            "dependencies": [],
            "path": "c-level-advisor/cpo-advisor/SKILL.md"
        },
        {
            "id": "cro-advisor",
            "category": "C Level Advisor",
            "title": "Cro Advisor",
            "description": "\"Liderança de receita para empresas B2B SaaS. Previsão de receita, design do modelo de vendas, estratégia de precificação, retenção líquida de receita e escala do time de vendas. Use ao projetar o motor de receita, definir quotas, modelar NRR, avaliar precificação, construir previsões para o conselho ou quando o usuário mencionar CRO, diretor de receita, estratégia de receita, modelo de vendas, crescimento de ARR, NRR, receita de expansão, churn, estratégia de precificação ou capacidade de vendas.\"",
            "triggers": [
                "/base",
                "/nrr",
                "/sales",
                "/trimestral",
                "/revenue",
                "/churn",
                "/otimista",
                "/pricing"
            ],
            "dependencies": [],
            "path": "c-level-advisor/cro-advisor/SKILL.md"
        },
        {
            "id": "cs-onboard",
            "category": "C Level Advisor",
            "title": "Cs Onboard",
            "description": "\"Entrevista de integração do fundador que captura o contexto da empresa em 7 dimensões. Invoque com /cs:setup para a entrevista inicial ou /cs:update para a atualização trimestral. Gera ~/.claude/company-context.md utilizado por todas as skills de assessoria C-suite.\"",
            "triggers": [
                "/pessoas",
                "/interview-guide",
                "/vendas",
                "/crescimento",
                "/operador",
                "/dinheiro",
                "/company-context",
                "/opera",
                "/company-context-template",
                "/cs"
            ],
            "dependencies": [],
            "path": "c-level-advisor/cs-onboard/SKILL.md"
        },
        {
            "id": "cto-advisor",
            "category": "C Level Advisor",
            "title": "Cto Advisor",
            "description": "\"Orientação de liderança técnica para times de engenharia, decisões de arquitetura e estratégia de tecnologia. Use ao avaliar dívida técnica, escalar times de engenharia, avaliar tecnologias, tomar decisões de arquitetura, estabelecer métricas de engenharia ou quando o usuário mencionar CTO, tech debt, dívida técnica, escalabilidade de times, decisões de arquitetura, avaliação de tecnologia, métricas de engenharia, métricas DORA ou estratégia de tecnologia.\"",
            "triggers": [
                "/tech",
                "/architecture",
                "/risco",
                "/technology",
                "/10",
                "/engineering",
                "/team",
                "/times",
                "/total"
            ],
            "dependencies": [],
            "path": "c-level-advisor/cto-advisor/SKILL.md"
        },
        {
            "id": "culture-architect",
            "category": "C Level Advisor",
            "title": "Culture Architect",
            "description": "\"Construa, meça e evolua a cultura da empresa como comportamento operacional — não como cartazes na parede. Abrange workshops de missão/visão/valores, tradução de valores em comportamentos, criação de código de cultura, avaliação de saúde cultural e rituais culturais por estágio. Use ao construir valores da empresa, avaliar saúde cultural, desenhar rituais culturais, criar códigos de cultura, lidar com choques de cultura ou quando o usuário mencionar cultura, valores, dívida cultural, cultura do fundador ou código de cultura.\"",
            "triggers": [
                "/vis",
                "/culture-playbook",
                "/comportamentos",
                "/culture-code-template",
                "/valores"
            ],
            "dependencies": [],
            "path": "c-level-advisor/culture-architect/SKILL.md"
        },
        {
            "id": "decision-logger",
            "category": "C Level Advisor",
            "title": "Decision Logger",
            "description": "\"Arquitetura de memória em duas camadas para decisões de reuniões do conselho. Gerencia transcrições brutas (Camada 1) e decisões aprovadas (Camada 2). Use ao registrar decisões após uma reunião do conselho, revisar decisões passadas com /cs:decisions ou verificar itens de ação vencidos com /cs:review. Invocado automaticamente pela skill de reunião do conselho após aprovação do fundador na Fase 5.\"",
            "triggers": [
                "/decision-entry",
                "/decision",
                "/board-meetings",
                "/decisions",
                "/cs",
                "/archive"
            ],
            "dependencies": [],
            "path": "c-level-advisor/decision-logger/SKILL.md"
        },
        {
            "id": "executive-mentor",
            "category": "C Level Advisor",
            "title": "Executive Mentor",
            "description": "\"Parceiro de pensamento adversarial para fundadores e executivos. Testa planos sob pressão, prepara para reuniões brutais do conselho, disseca decisões sem boas opções e força post-mortems honestos. Use quando precisar que alguém encontre os pontos fracos antes que o conselho encontre, para tomar uma decisão que você vem evitando, ou para entender o que realmente deu errado.\"",
            "triggers": [
                "/stakeholder",
                "/devils-advocate",
                "/hard-call",
                "/em",
                "/10",
                "/postmortem",
                "/crisis",
                "/hard",
                "/decision",
                "/challenge",
                "/stress-test",
                "/board-prep",
                "/board"
            ],
            "dependencies": [],
            "path": "c-level-advisor/executive-mentor/SKILL.md"
        },
        {
            "id": "founder-coach",
            "category": "C Level Advisor",
            "title": "Founder Coach",
            "description": "\"Desenvolvimento de liderança pessoal para fundadores e CEOs de primeira viagem. Abrange identificação de arquétipo do fundador, frameworks de delegação, gestão de energia, auditorias de agenda do CEO, evolução do estilo de liderança, identificação de pontos cegos, síndrome do impostor, saúde mental do fundador e planejamento de sucessão. Use quando um fundador se sente como o gargalo, tem dificuldade em delegar, está em burnout, fazendo a transição de IC para executivo, gerenciando um conselho, ou quando o usuário mencionar founder mode, crescimento do CEO, desenvolvimento de liderança, delegação, burnout ou síndrome do impostor.\"",
            "triggers": [
                "/founder-toolkit",
                "/clientes",
                "/leadership-growth",
                "/parceiros",
                "/bloco"
            ],
            "dependencies": [],
            "path": "c-level-advisor/founder-coach/SKILL.md"
        },
        {
            "id": "internal-narrative",
            "category": "C Level Advisor",
            "title": "Internal Narrative",
            "description": "\"Construa e mantenha uma narrativa coerente da empresa para todos os públicos — funcionários, investidores, clientes, candidatos e parceiros. Detecta contradições narrativas e garante que a mesma verdade seja enquadrada para as necessidades de cada público. Use ao preparar atualizações para investidores, apresentações de all-hands, comunicações do conselho, narrativas de recrutamento, comunicações de crise ou quando o usuário mencionar narrativa da empresa, consistência de mensagens, storytelling, all-hands, atualização para investidores ou comunicação de crise.\"",
            "triggers": [
                "/narrative-frameworks",
                "/all-hands-template"
            ],
            "dependencies": [],
            "path": "c-level-advisor/internal-narrative/SKILL.md"
        },
        {
            "id": "intl-expansion",
            "category": "C Level Advisor",
            "title": "Intl Expansion",
            "description": "\"Estratégia de expansão para mercados internacionais. Seleção de mercado, modos de entrada, localização, conformidade regulatória e go-to-market por região. Use ao expandir para novos países, avaliar mercados internacionais, planejar localização ou construir times regionais.\"",
            "triggers": [
                "/confer",
                "/distribuidor",
                "/market-entry-playbook",
                "/regional-guide",
                "/hora",
                "/18"
            ],
            "dependencies": [],
            "path": "c-level-advisor/intl-expansion/SKILL.md"
        },
        {
            "id": "ma-playbook",
            "category": "C Level Advisor",
            "title": "Ma Playbook",
            "description": "\"Estratégia de M&A para adquirir empresas ou ser adquirido. Due diligence, avaliação, integração e estrutura de negócio. Use ao avaliar aquisições, preparar-se para ser adquirido, due diligence de M&A, planejamento de integração ou negociação de transações.\"",
            "triggers": [
                "/barato",
                "/earnout",
                "/due-diligence-checklist",
                "/integration-playbook"
            ],
            "dependencies": [],
            "path": "c-level-advisor/ma-playbook/SKILL.md"
        },
        {
            "id": "org-health-diagnostic",
            "category": "C Level Advisor",
            "title": "Org Health Diagnostic",
            "description": "\"Verificação de saúde organizacional interfuncional combinando sinais de todas as funções C-suite. Pontua 8 dimensões em uma escala de semáforo com recomendações detalhadas. Use ao avaliar a saúde geral da empresa, preparar revisões do conselho, identificar funções em risco ou quando o usuário mencionar saúde organizacional, verificação de saúde ou painel de saúde.\"",
            "triggers": [
                "/health",
                "/10",
                "/em",
                "/health-benchmarks"
            ],
            "dependencies": [],
            "path": "c-level-advisor/org-health-diagnostic/SKILL.md"
        },
        {
            "id": "scenario-war-room",
            "category": "C Level Advisor",
            "title": "Scenario War Room",
            "description": "\"Modelagem interfuncional de cenários hipotéticos com efeitos cascata e múltiplas variáveis. Ao contrário do teste de estresse de premissa única, este modela adversidade composta em todas as funções do negócio simultaneamente. Use ao enfrentar cenários de risco complexos, decisões estratégicas com grande desvantagem ou quando o usuário perguntar 'e se X E Y acontecerem ao mesmo tempo?'\"",
            "triggers": [
                "/ano",
                "/em",
                "/scenario-planning",
                "/scenario",
                "/war-room"
            ],
            "dependencies": [],
            "path": "c-level-advisor/scenario-war-room/SKILL.md"
        },
        {
            "id": "strategic-alignment",
            "category": "C Level Advisor",
            "title": "Strategic Alignment",
            "description": "\"Cascateia a estratégia da diretoria até o colaborador individual. Detecta e corrige desalinhamentos entre metas da empresa e execução dos times. Abrange articulação de estratégia, mapeamento de cascata, detecção de metas órfãs, identificação de silos, análise de gaps de comunicação e protocolos de realinhamento. Use quando times estão puxando em direções diferentes, OKRs não se conectam, departamentos otimizam localmente à custa da empresa, ou quando o usuário mencionar alinhamento, cascata de estratégia, silo, OKRs conflitantes ou comunicação de estratégia.\"",
            "triggers": [
                "/alignment-playbook",
                "/10",
                "/alignment"
            ],
            "dependencies": [],
            "path": "c-level-advisor/strategic-alignment/SKILL.md"
        }
    ],
    "Skills": [
        {
            "id": "board",
            "category": "Skills",
            "title": "Board",
            "description": "\"Ler, escrever e navegar no quadro de mensagens do AgentHub para coordenação entre agentes.\"",
            "triggers": [
                "/scripts",
                "/board",
                "/hub"
            ],
            "dependencies": [],
            "path": "engineering/agenthub/skills/board/SKILL.md"
        },
        {
            "id": "board-prep",
            "category": "Skills",
            "title": "Board Prep",
            "description": "\"/em:board-prep — Preparação para Reunião do Conselho\"",
            "triggers": [
                "/em"
            ],
            "dependencies": [],
            "path": "c-level-advisor/executive-mentor/skills/board-prep/SKILL.md"
        },
        {
            "id": "browserstack",
            "category": "Skills",
            "title": "Browserstack",
            "description": ">-",
            "triggers": [
                "/cdp",
                "/rede",
                "/falhou",
                "/accounts",
                "/capturas",
                "/pw",
                "/www",
                "/test",
                "/playwright",
                "/settings"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/skills/browserstack/SKILL.md"
        },
        {
            "id": "challenge",
            "category": "Skills",
            "title": "Challenge",
            "description": "\"/em:challenge — Análise Pre-Mortem de Planos\"",
            "triggers": [
                "/60",
                "/em",
                "/pivotar",
                "/90"
            ],
            "dependencies": [],
            "path": "c-level-advisor/executive-mentor/skills/challenge/SKILL.md"
        },
        {
            "id": "coverage",
            "category": "Skills",
            "title": "Coverage",
            "description": ">-",
            "triggers": [
                "/forgot-password",
                "/dashboard",
                "/checkout",
                "/registration",
                "/data-loading",
                "/password-reset",
                "/login",
                "/register",
                "/complexo",
                "/pw",
                "/rotas",
                "/settings"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/skills/coverage/SKILL.md"
        },
        {
            "id": "eval",
            "category": "Skills",
            "title": "Eval",
            "description": "\"Avaliar e classificar resultados dos agentes por métrica ou juiz LLM para uma sessão do AgentHub.\"",
            "triggers": [
                "/session",
                "/hub",
                "/scripts",
                "/agent-",
                "/results",
                "/result",
                "/board"
            ],
            "dependencies": [],
            "path": "engineering/agenthub/skills/eval/SKILL.md"
        },
        {
            "id": "extract",
            "category": "Skills",
            "title": "Extract",
            "description": "\"Transformar um padrão comprovado ou solução de debugging em uma skill standalone reutilizável com SKILL.md, documentação de referência e exemplos.\"",
            "triggers": [
                "/projects",
                "/memory",
                "/examples",
                "/reference",
                "/skills",
                "/si",
                "/plugin"
            ],
            "dependencies": [],
            "path": "engineering-team/self-improving-agent/skills/extract/SKILL.md"
        },
        {
            "id": "fix",
            "category": "Skills",
            "title": "Fix",
            "description": ">-",
            "triggers": [
                "/login",
                "/10",
                "/traces",
                "/debug"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/skills/fix/SKILL.md"
        },
        {
            "id": "generate",
            "category": "Skills",
            "title": "Generate",
            "description": ">-",
            "triggers": [
                "/dados",
                "/crud",
                "/test",
                "/caso",
                "/api",
                "/components",
                "/checkout",
                "/auth",
                "/forms",
                "/dashboard",
                "/accessibility",
                "/login",
                "/onboarding",
                "/pagamento",
                "/filtro",
                "/search",
                "/settings"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/skills/generate/SKILL.md"
        },
        {
            "id": "hard-call",
            "category": "Skills",
            "title": "Hard Call",
            "description": "\"/em:hard-call — Framework para Decisões Sem Boas Opções\"",
            "triggers": [
                "/cultura",
                "/em",
                "/10",
                "/hard"
            ],
            "dependencies": [],
            "path": "c-level-advisor/executive-mentor/skills/hard-call/SKILL.md"
        },
        {
            "id": "init",
            "category": "Skills",
            "title": "Init",
            "description": "\"Criar uma nova sessão de colaboração do AgentHub com tarefa, número de agentes e critérios de avaliação.\"",
            "triggers": [
                "/sessions",
                "/scripts",
                "/config",
                "/hub"
            ],
            "dependencies": [],
            "path": "engineering/agenthub/skills/init/SKILL.md"
        },
        {
            "id": "init",
            "category": "Skills",
            "title": "Init",
            "description": ">-",
            "triggers": [
                "/blob-report",
                "/checkout",
                "/setup-node",
                "/upload-artifact",
                "/playwright-report",
                "/e2e",
                "/workflows",
                "/test",
                "/test-results",
                "/playwright",
                "/localhost"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/skills/init/SKILL.md"
        },
        {
            "id": "loop",
            "category": "Skills",
            "title": "Loop",
            "description": "\"Iniciar um loop autônomo de experimentos com intervalo selecionado pelo usuário (10min, 1h, diário, semanal, mensal). Usa CronCreate para agendamento.\"",
            "triggers": [
                "/api-speed",
                "/config",
                "/run",
                "/scripts",
                "/10",
                "/ar",
                "/program",
                "/results",
                "/loop"
            ],
            "dependencies": [],
            "path": "engineering/autoresearch-agent/skills/loop/SKILL.md"
        },
        {
            "id": "merge",
            "category": "Skills",
            "title": "Merge",
            "description": "\"Mergear o branch do agente vencedor no base, arquivar os perdedores e limpar os worktrees.\"",
            "triggers": [
                "/session",
                "/hub",
                "/board",
                "/merge-summary",
                "/scripts",
                "/attempt-1",
                "/agent-",
                "/results",
                "/archive"
            ],
            "dependencies": [],
            "path": "engineering/agenthub/skills/merge/SKILL.md"
        },
        {
            "id": "migrate",
            "category": "Skills",
            "title": "Migrate",
            "description": ">-",
            "triggers": [
                "/pw",
                "/depois",
                "/batch"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/skills/migrate/SKILL.md"
        },
        {
            "id": "postmortem",
            "category": "Skills",
            "title": "Postmortem",
            "description": "\"/em:postmortem — Análise Honesta do que Deu Errado\"",
            "triggers": [
                "/03",
                "/04",
                "/em",
                "/perdas"
            ],
            "dependencies": [],
            "path": "c-level-advisor/executive-mentor/skills/postmortem/SKILL.md"
        },
        {
            "id": "promote",
            "category": "Skills",
            "title": "Promote",
            "description": "\"Graduar um padrão comprovado da auto-memória (MEMORY.md) para CLAUDE.md ou .claude/rules/ para aplicação permanente.\"",
            "triggers": [
                "/projects",
                "/memory",
                "/200",
                "/api",
                "/testing",
                "/rules",
                "/si"
            ],
            "dependencies": [],
            "path": "engineering-team/self-improving-agent/skills/promote/SKILL.md"
        },
        {
            "id": "remember",
            "category": "Skills",
            "title": "Remember",
            "description": "\"Salvar explicitamente conhecimento importante na auto-memória com timestamp e contexto. Use quando uma descoberta é importante demais para depender da captura automática.\"",
            "triggers": [
                "/projects",
                "/memory",
                "/200",
                "/null",
                "/api",
                "/dev",
                "/components",
                "/auth",
                "/nunca",
                "/si",
                "/upload"
            ],
            "dependencies": [],
            "path": "engineering-team/self-improving-agent/skills/remember/SKILL.md"
        },
        {
            "id": "report",
            "category": "Skills",
            "title": "Report",
            "description": ">-",
            "triggers": [
                "/null",
                "/inst",
                "/dev",
                "/json",
                "/pw",
                "/workflows",
                "/index",
                "/pulado",
                "/reprova"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/skills/report/SKILL.md"
        },
        {
            "id": "resume",
            "category": "Skills",
            "title": "Resume",
            "description": "\"Retomar um experimento pausado. Faz checkout do branch do experimento, lê o histórico de resultados e continua iterando.\"",
            "triggers": [
                "/api-speed",
                "/conclu",
                "/config",
                "/program",
                "/api",
                "/scripts",
                "/setup",
                "/ar",
                "/pausado",
                "/results",
                "/search"
            ],
            "dependencies": [],
            "path": "engineering/autoresearch-agent/skills/resume/SKILL.md"
        },
        {
            "id": "review",
            "category": "Skills",
            "title": "Review",
            "description": ">-",
            "triggers": [
                "/batch",
                "/fixture",
                "/10",
                "/funcionalidades",
                "/borda"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/skills/review/SKILL.md"
        },
        {
            "id": "review",
            "category": "Skills",
            "title": "Review",
            "description": "\"Analisar a auto-memória em busca de candidatos a promoção, entradas desatualizadas, oportunidades de consolidação e métricas de saúde.\"",
            "triggers": [
                "/projects",
                "/memory",
                "/200",
                "/rules",
                "/si"
            ],
            "dependencies": [],
            "path": "engineering-team/self-improving-agent/skills/review/SKILL.md"
        },
        {
            "id": "run",
            "category": "Skills",
            "title": "Run",
            "description": "\"Comando de ciclo de vida completo que encadeia init → baseline → spawn → eval → merge em uma única invocação.\"",
            "triggers": [
                "/config",
                "/scripts",
                "/agent-templates",
                "/sessions",
                "/hub"
            ],
            "dependencies": [],
            "path": "engineering/agenthub/skills/run/SKILL.md"
        },
        {
            "id": "run",
            "category": "Skills",
            "title": "Run",
            "description": "\"Executar uma única iteração de experimento. Editar o arquivo alvo, avaliar, manter ou descartar.\"",
            "triggers": [
                "/api-speed",
                "/config",
                "/program",
                "/run",
                "/scripts",
                "/setup",
                "/ar",
                "/results"
            ],
            "dependencies": [],
            "path": "engineering/autoresearch-agent/skills/run/SKILL.md"
        },
        {
            "id": "setup",
            "category": "Skills",
            "title": "Setup",
            "description": "\"Configurar um novo experimento de autoresearch de forma interativa. Coleta domínio, arquivo alvo, comando de avaliação, métrica, direção e avaliador.\"",
            "triggers": [
                "/api",
                "/scripts",
                "/compila",
                "/setup",
                "/ar"
            ],
            "dependencies": [],
            "path": "engineering/autoresearch-agent/skills/setup/SKILL.md"
        },
        {
            "id": "spawn",
            "category": "Skills",
            "title": "Spawn",
            "description": "\"Lançar N subagentes paralelos em git worktrees isolados para competir na tarefa da sessão.\"",
            "triggers": [
                "/config",
                "/board",
                "/session",
                "/scripts",
                "/dispatch",
                "/agent-templates",
                "/sessions",
                "/agent-",
                "/results",
                "/descartar",
                "/hub"
            ],
            "dependencies": [],
            "path": "engineering/agenthub/skills/spawn/SKILL.md"
        },
        {
            "id": "status",
            "category": "Skills",
            "title": "Status",
            "description": "\"Mostrar estado do DAG, progresso dos agentes e status dos branches para uma sessão do AgentHub.\"",
            "triggers": [
                "/session",
                "/hub",
                "/agent-2",
                "/scripts",
                "/agent-1",
                "/20260317-151200",
                "/dag",
                "/20260317-143022",
                "/attempt-1",
                "/agent-3",
                "/board"
            ],
            "dependencies": [],
            "path": "engineering/agenthub/skills/status/SKILL.md"
        },
        {
            "id": "status",
            "category": "Skills",
            "title": "Status",
            "description": "\"Mostrar painel de experimentos com resultados, loops ativos e progresso.\"",
            "triggers": [
                "/api-speed",
                "/null",
                "/dev",
                "/scripts",
                "/log",
                "/10",
                "/ar",
                "/loop",
                "/100"
            ],
            "dependencies": [],
            "path": "engineering/autoresearch-agent/skills/status/SKILL.md"
        },
        {
            "id": "status",
            "category": "Skills",
            "title": "Status",
            "description": "\"Painel de saúde da memória mostrando contagens de linhas, arquivos por tópico, capacidade, entradas desatualizadas e recomendações.\"",
            "triggers": [
                "/projects",
                "/memory",
                "/200",
                "/null",
                "/cr",
                "/dev",
                "/rules",
                "/si",
                "/aten"
            ],
            "dependencies": [],
            "path": "engineering-team/self-improving-agent/skills/status/SKILL.md"
        },
        {
            "id": "stress-test",
            "category": "Skills",
            "title": "Stress Test",
            "description": "\"/em:stress-test — Teste de Estresse de Premissas de Negócio\"",
            "triggers": [
                "/em"
            ],
            "dependencies": [],
            "path": "c-level-advisor/executive-mentor/skills/stress-test/SKILL.md"
        },
        {
            "id": "testrail",
            "category": "Skills",
            "title": "Testrail",
            "description": ">-",
            "triggers": [
                "/sua-instancia",
                "/resultados",
                "/pw"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/skills/testrail/SKILL.md"
        }
    ],
    "Carreira Educacao": [
        {
            "id": "busca-de-emprego",
            "category": "Carreira Educacao",
            "title": "Busca De Emprego",
            "description": "\"Estratégia completa de busca de emprego no mercado brasileiro: onde procurar vagas, como personalizar candidatura, preparação para entrevistas técnicas (system design, coding, comportamental) e negociação de oferta.\"",
            "triggers": [
                "/read",
                "/rules",
                "/job-hunting",
                "/skill"
            ],
            "dependencies": [],
            "path": "carreira-educacao/busca-de-emprego/SKILL.md"
        },
        {
            "id": "criador-de-cursos",
            "category": "Carreira Educacao",
            "title": "Criador De Cursos",
            "description": "\"Estruturação de cursos online: design instrucional, criação de módulos e aulas, materiais complementares, estratégia de precificação e lançamento nas plataformas brasileiras (Hotmart, Kiwify, Eduzz).\"",
            "triggers": [
                "/read",
                "/rules",
                "/curso-creator",
                "/skill",
                "/etc"
            ],
            "dependencies": [],
            "path": "carreira-educacao/criador-de-cursos/SKILL.md"
        },
        {
            "id": "criador-de-portfolio",
            "category": "Carreira Educacao",
            "title": "Criador De Portfolio",
            "description": "\"Construção de portfólio profissional digital: seleção e apresentação de projetos, estrutura de cases com problema-solução-resultado, showcase de habilidades e estratégia de distribuição para atrair clientes e recrutadores.\"",
            "triggers": [
                "/read",
                "/rules",
                "/portfolio-builder",
                "/skill"
            ],
            "dependencies": [],
            "path": "carreira-educacao/criador-de-portfolio/SKILL.md"
        },
        {
            "id": "curriculo-e-cv",
            "category": "Carreira Educacao",
            "title": "Curriculo E Cv",
            "description": "\"Criação de currículo para o mercado brasileiro: formato ATS para triagem automática, versão visual para apresentação presencial, descrição de experiências com métricas e adaptação por vaga e empresa.\"",
            "triggers": [
                "/read",
                "/estado",
                "/curriculum-vitae",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "carreira-educacao/curriculo-e-cv/SKILL.md"
        },
        {
            "id": "estrutura-freelancer",
            "category": "Carreira Educacao",
            "title": "Estrutura Freelancer",
            "description": "\"Estruturação de negócio freelancer no Brasil: comparativo MEI vs PJ, abertura de empresa, precificação justa considerando impostos e tempo não faturável, contratos simples e gestão financeira básica.\"",
            "triggers": [
                "/ano",
                "/read",
                "/projeto",
                "/freelancer-setup",
                "/rules",
                "/design",
                "/skill"
            ],
            "dependencies": [],
            "path": "carreira-educacao/estrutura-freelancer/SKILL.md"
        },
        {
            "id": "framework-de-mentoria",
            "category": "Carreira Educacao",
            "title": "Framework De Mentoria",
            "description": "\"Frameworks de mentoria estruturada e planos de desenvolvimento individual (PDI): como conduzir sessões de mentoria, criar PDI com metas SMART, dar feedback construtivo e acompanhar progresso do mentorado.\"",
            "triggers": [
                "/read",
                "/rules",
                "/skill",
                "/mentoring-framework",
                "/per"
            ],
            "dependencies": [],
            "path": "carreira-educacao/framework-de-mentoria/SKILL.md"
        },
        {
            "id": "marca-pessoal",
            "category": "Carreira Educacao",
            "title": "Marca Pessoal",
            "description": "\"Construção de autoridade e posicionamento digital para profissionais brasileiros: nicho de posicionamento, estratégia de conteúdo, presença multiplataforma e como monetizar a audiência construída.\"",
            "triggers": [
                "/emprego",
                "/read",
                "/especialidade",
                "/semana",
                "/rules",
                "/diferencial",
                "/skill",
                "/audi",
                "/personal-brand"
            ],
            "dependencies": [],
            "path": "carreira-educacao/marca-pessoal/SKILL.md"
        },
        {
            "id": "negociacao-salarial",
            "category": "Carreira Educacao",
            "title": "Negociacao Salarial",
            "description": "\"Negociação salarial para o mercado brasileiro: pesquisa de benchmarks, scripts de negociação, como avaliar uma proposta completa (salário + benefícios + crescimento) e como lidar com contra-propostas.\"",
            "triggers": [
                "/read",
                "/empresas",
                "/rules",
                "/salary-negotiation",
                "/skill"
            ],
            "dependencies": [],
            "path": "carreira-educacao/negociacao-salarial/SKILL.md"
        },
        {
            "id": "palestra-preparacao",
            "category": "Carreira Educacao",
            "title": "Palestra Preparacao",
            "description": "\"Preparação de palestras técnicas e apresentações em eventos brasileiros: estrutura de conteúdo, storytelling, slides eficazes, técnicas de apresentação e como submeter CFP em eventos de tecnologia BR.\"",
            "triggers": [
                "/read",
                "/palestra-preparacao",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "carreira-educacao/palestra-preparacao/SKILL.md"
        },
        {
            "id": "perfil-linkedin",
            "category": "Carreira Educacao",
            "title": "Perfil Linkedin",
            "description": "\"Otimização de perfil LinkedIn para recrutadores e clientes no mercado brasileiro: headline magnética, seção About com storytelling, experiências com resultados mensuráveis e estratégia de conteúdo para visibilidade.\"",
            "triggers": [
                "/read",
                "/clientes",
                "/rules",
                "/parcerias",
                "/linkedin-profile",
                "/skill",
                "/seunome",
                "/in"
            ],
            "dependencies": [],
            "path": "carreira-educacao/perfil-linkedin/SKILL.md"
        }
    ],
    "Codigo Automacao": [
        {
            "id": "automacao-de-testes",
            "category": "Codigo Automacao",
            "title": "Automacao De Testes",
            "description": "\"Automação de testes: unitários (Jest, Pytest), integração (supertest, httpx) e E2E com Playwright. Inclui estratégia de pirâmide de testes, cobertura mínima, CI/CD integration e testes para contexto brasileiro (CPF, CNPJ, CEP, PIX).\"",
            "triggers": [
                "/----------",
                "/read",
                "/etc",
                "/0001-81",
                "/rules",
                "/------",
                "/--------------",
                "/skill",
                "/test-automation",
                "/produtos",
                "/produto-teste"
            ],
            "dependencies": [],
            "path": "codigo-automacao/automacao-de-testes/SKILL.md"
        },
        {
            "id": "banco-de-dados-ops",
            "category": "Codigo Automacao",
            "title": "Banco De Dados Ops",
            "description": "\"Operações de banco de dados: queries otimizadas, migrations versionadas, estratégia de indexação, modelagem relacional e NoSQL, backup e recovery. Foco em PostgreSQL e MySQL com contexto de dados brasileiros.\"",
            "triggers": [
                "/read",
                "/database-ops",
                "/rules",
                "/skill",
                "/0000-00"
            ],
            "dependencies": [],
            "path": "codigo-automacao/banco-de-dados-ops/SKILL.md"
        },
        {
            "id": "construtor-de-api",
            "category": "Codigo Automacao",
            "title": "Construtor De Api",
            "description": "\"Construção e documentação de APIs REST e GraphQL: design de endpoints, versionamento, autenticação, tratamento de erros, documentação OpenAPI 3.0 e boas práticas de segurança e performance.\"",
            "triggers": [
                "/read",
                "/products",
                "/api",
                "/v1",
                "/users",
                "/rules",
                "/response",
                "/errors",
                "/register",
                "/skill",
                "/orders",
                "/validation-failed",
                "/api-builder"
            ],
            "dependencies": [],
            "path": "codigo-automacao/construtor-de-api/SKILL.md"
        },
        {
            "id": "docker-compose",
            "category": "Codigo Automacao",
            "title": "Docker Compose",
            "description": "\"Containerização com Docker e Docker Compose: configuração para desenvolvimento com hot reload, produção com health checks, multi-stage builds, Docker networks e gestão de secrets e variáveis de ambiente.\"",
            "triggers": [
                "/health",
                "/read",
                "/rules",
                "/docker-compose",
                "/skill",
                "/node",
                "/app",
                "/framework",
                "/localhost"
            ],
            "dependencies": [],
            "path": "codigo-automacao/docker-compose/SKILL.md"
        },
        {
            "id": "engenheiro-de-prompts",
            "category": "Codigo Automacao",
            "title": "Engenheiro De Prompts",
            "description": "\"Engenharia de prompts para máxima produtividade com LLMs: técnicas de chain-of-thought, few-shot, role prompting, structured output e otimização de prompts para casos de uso específicos como classificação, extração e geração.\"",
            "triggers": [
                "/extra",
                "/read",
                "/output",
                "/prompt-engineer",
                "/gera",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "codigo-automacao/engenheiro-de-prompts/SKILL.md"
        },
        {
            "id": "especialista-claude-code",
            "category": "Codigo Automacao",
            "title": "Especialista Claude Code",
            "description": "\"Uso avançado do Claude Code: criação de skills customizadas, subagentes paralelos, worktrees para features isoladas, gestão de contexto e configurações avançadas de CLAUDE.md para máxima produtividade.\"",
            "triggers": [
                "/read",
                "/persona",
                "/api",
                "/auth",
                "/rules",
                "/nova-feature",
                "/skill",
                "/claude-code-expert",
                "/payments",
                "/src",
                "/meu-projeto-feature-x"
            ],
            "dependencies": [],
            "path": "codigo-automacao/especialista-claude-code/SKILL.md"
        },
        {
            "id": "especialista-em-debug",
            "category": "Codigo Automacao",
            "title": "Especialista Em Debug",
            "description": "\"Diagnóstico sistemático de bugs: análise de logs, stack traces, reprodução do problema e estratégia de fix. Framework step-by-step para encontrar e resolver qualquer tipo de bug em aplicações web, mobile ou backend.\"",
            "triggers": [
                "/read",
                "/debug-expert",
                "/config",
                "/response",
                "/rules",
                "/alertas",
                "/skill",
                "/refutar"
            ],
            "dependencies": [],
            "path": "codigo-automacao/especialista-em-debug/SKILL.md"
        },
        {
            "id": "implementacao-de-auth",
            "category": "Codigo Automacao",
            "title": "Implementacao De Auth",
            "description": "\"Implementação de autenticação e autorização: JWT com refresh tokens, OAuth 2.0 (Google, GitHub), Supabase Auth, Firebase Auth e RBAC. Boas práticas de segurança, armazenamento seguro e LGPD compliance.\"",
            "triggers": [
                "/auth-implementer",
                "/read",
                "/callback",
                "/auth",
                "/rules",
                "/meuapp",
                "/login",
                "/skill",
                "/senha"
            ],
            "dependencies": [],
            "path": "codigo-automacao/implementacao-de-auth/SKILL.md"
        },
        {
            "id": "integrador-de-webhooks",
            "category": "Codigo Automacao",
            "title": "Integrador De Webhooks",
            "description": "\"Integração via webhooks, eventos e filas de mensagens: implementação de recebimento e envio de webhooks, idempotência, retry com backoff exponencial, filas com Redis/SQS/RabbitMQ e event-driven architecture.\"",
            "triggers": [
                "/read",
                "/rules",
                "/webhook-integrator",
                "/skill"
            ],
            "dependencies": [],
            "path": "codigo-automacao/integrador-de-webhooks/SKILL.md"
        },
        {
            "id": "no-code-automacao",
            "category": "Codigo Automacao",
            "title": "No Code Automacao",
            "description": "\"Automações com Make (Integromat), Zapier, n8n e ActivePieces: criação de fluxos, integrações entre sistemas, automação de processos repetitivos e blueprints prontos para contexto brasileiro.\"",
            "triggers": [
                "/read",
                "/notas",
                "/n8n",
                "/rules",
                "/skill",
                "/no-code-automacao"
            ],
            "dependencies": [],
            "path": "codigo-automacao/no-code-automacao/SKILL.md"
        }
    ],
    "Conteudo Copy": [
        {
            "id": "copy-de-anuncio",
            "category": "Conteudo Copy",
            "title": "Copy De Anuncio",
            "description": "|",
            "triggers": [
                "/ad-copy",
                "/read",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "conteudo-copy/copy-de-anuncio/SKILL.md"
        },
        {
            "id": "copy-de-vendas",
            "category": "Conteudo Copy",
            "title": "Copy De Vendas",
            "description": "|",
            "triggers": [
                "/read",
                "/cart",
                "/empresa",
                "/rules",
                "/skill",
                "/sales-copy"
            ],
            "dependencies": [],
            "path": "conteudo-copy/copy-de-vendas/SKILL.md"
        },
        {
            "id": "criador-de-hooks",
            "category": "Conteudo Copy",
            "title": "Criador De Hooks",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/hook-writer",
                "/skill"
            ],
            "dependencies": [],
            "path": "conteudo-copy/criador-de-hooks/SKILL.md"
        },
        {
            "id": "descricao-de-produto",
            "category": "Conteudo Copy",
            "title": "Descricao De Produto",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/accordion",
                "/skill",
                "/product-description"
            ],
            "dependencies": [],
            "path": "conteudo-copy/descricao-de-produto/SKILL.md"
        },
        {
            "id": "escritor-de-artigos",
            "category": "Conteudo Copy",
            "title": "Escritor De Artigos",
            "description": "|",
            "triggers": [
                "/read",
                "/sum",
                "/rules",
                "/article-writer",
                "/skill"
            ],
            "dependencies": [],
            "path": "conteudo-copy/escritor-de-artigos/SKILL.md"
        },
        {
            "id": "escritor-de-emails",
            "category": "Conteudo Copy",
            "title": "Escritor De Emails",
            "description": "|",
            "triggers": [
                "/read",
                "/desconto",
                "/rules",
                "/skill",
                "/email-writer"
            ],
            "dependencies": [],
            "path": "conteudo-copy/escritor-de-emails/SKILL.md"
        },
        {
            "id": "gerador-de-headlines",
            "category": "Conteudo Copy",
            "title": "Gerador De Headlines",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/headline-generator",
                "/skill"
            ],
            "dependencies": [],
            "path": "conteudo-copy/gerador-de-headlines/SKILL.md"
        },
        {
            "id": "posts-sociais",
            "category": "Conteudo Copy",
            "title": "Posts Sociais",
            "description": "|",
            "triggers": [
                "/social-posts",
                "/read",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "conteudo-copy/posts-sociais/SKILL.md"
        },
        {
            "id": "reaproveitamento-de-conteudo",
            "category": "Conteudo Copy",
            "title": "Reaproveitamento De Conteudo",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/content-repurposing",
                "/skill"
            ],
            "dependencies": [],
            "path": "conteudo-copy/reaproveitamento-de-conteudo/SKILL.md"
        },
        {
            "id": "storytelling",
            "category": "Conteudo Copy",
            "title": "Storytelling",
            "description": "|",
            "triggers": [
                "/read",
                "/storytelling",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "conteudo-copy/storytelling/SKILL.md"
        }
    ],
    "Design Branding": [
        {
            "id": "apresentacao-slides",
            "category": "Design Branding",
            "title": "Apresentacao Slides",
            "description": "\"Slides executivos: estrutura, narrativa visual e design para apresentações no Brasil\"",
            "triggers": [
                "/solu"
            ],
            "dependencies": [],
            "path": "design-branding/apresentacao-slides/SKILL.md"
        },
        {
            "id": "assets-redes-sociais",
            "category": "Design Branding",
            "title": "Assets Redes Sociais",
            "description": "\"Templates e especificações para redes sociais: feed, stories, banners e thumbnails\"",
            "triggers": [],
            "dependencies": [],
            "path": "design-branding/assets-redes-sociais/SKILL.md"
        },
        {
            "id": "briefing-de-logo",
            "category": "Design Branding",
            "title": "Briefing De Logo",
            "description": "\"Briefing de logo e identidade para designers e agências no mercado brasileiro\"",
            "triggers": [],
            "dependencies": [],
            "path": "design-branding/briefing-de-logo/SKILL.md"
        },
        {
            "id": "briefing-de-video",
            "category": "Design Branding",
            "title": "Briefing De Video",
            "description": "\"Briefing para vídeos institucionais, de produto e publicitários no mercado brasileiro\"",
            "triggers": [],
            "dependencies": [],
            "path": "design-branding/briefing-de-video/SKILL.md"
        },
        {
            "id": "design-de-pitch",
            "category": "Design Branding",
            "title": "Design De Pitch",
            "description": "\"Design e estrutura de pitch decks e apresentações executivas para captação e vendas\"",
            "triggers": [],
            "dependencies": [],
            "path": "design-branding/design-de-pitch/SKILL.md"
        },
        {
            "id": "feedback-de-design",
            "category": "Design Branding",
            "title": "Feedback De Design",
            "description": "\"Feedback estruturado e direção em projetos de UI/UX, protótipos e interfaces\"",
            "triggers": [
                "/importante",
                "/sugest"
            ],
            "dependencies": [],
            "path": "design-branding/feedback-de-design/SKILL.md"
        },
        {
            "id": "identidade-visual",
            "category": "Design Branding",
            "title": "Identidade Visual",
            "description": "\"Criação de identidade visual e brand guidelines completos para marcas brasileiras\"",
            "triggers": [
                "/secund",
                "/cinza"
            ],
            "dependencies": [],
            "path": "design-branding/identidade-visual/SKILL.md"
        },
        {
            "id": "manual-de-marca",
            "category": "Design Branding",
            "title": "Manual De Marca",
            "description": "\"Brandbook completo: aplicações de marca, tipografia, cores e restrições para uso consistente\"",
            "triggers": [
                "/secund",
                "/neutra"
            ],
            "dependencies": [],
            "path": "design-branding/manual-de-marca/SKILL.md"
        },
        {
            "id": "materiais-vendas",
            "category": "Design Branding",
            "title": "Materiais Vendas",
            "description": "\"One-pager, proposta visual, folder e materiais B2B para aceleração de vendas\"",
            "triggers": [
                "/servi"
            ],
            "dependencies": [],
            "path": "design-branding/materiais-vendas/SKILL.md"
        },
        {
            "id": "producao-no-figma",
            "category": "Design Branding",
            "title": "Producao No Figma",
            "description": "\"Orientação para organização e produção em Figma: componentes, auto-layout e sistemas de design\"",
            "triggers": [
                "/frames"
            ],
            "dependencies": [],
            "path": "design-branding/producao-no-figma/SKILL.md"
        }
    ],
    "Direcao Criativa": [
        {
            "id": "ativacao-de-marca",
            "category": "Direcao Criativa",
            "title": "Ativacao De Marca",
            "description": "\"Ativações de marca, experiências e eventos criativos para o mercado brasileiro\"",
            "triggers": [],
            "dependencies": [],
            "path": "direcao-criativa/ativacao-de-marca/SKILL.md"
        },
        {
            "id": "campanha-360",
            "category": "Direcao Criativa",
            "title": "Campanha 360",
            "description": "\"Planejamento de campanha integrada multi-canal para o mercado brasileiro\"",
            "triggers": [],
            "dependencies": [],
            "path": "direcao-criativa/campanha-360/SKILL.md"
        },
        {
            "id": "conceito-criativo",
            "category": "Direcao Criativa",
            "title": "Conceito Criativo",
            "description": "\"Desenvolvimento de big idea e conceito central de campanha para marcas brasileiras\"",
            "triggers": [],
            "dependencies": [],
            "path": "direcao-criativa/conceito-criativo/SKILL.md"
        },
        {
            "id": "direcao-arte",
            "category": "Direcao Criativa",
            "title": "Direcao Arte",
            "description": "\"Briefing e referências para direção de arte e produção visual de campanhas\"",
            "triggers": [
                "/lifestyle"
            ],
            "dependencies": [],
            "path": "direcao-criativa/direcao-arte/SKILL.md"
        },
        {
            "id": "ideacao",
            "category": "Direcao Criativa",
            "title": "Ideacao",
            "description": "\"Facilitação de brainstorming e sessões de ideação criativa para times e projetos\"",
            "triggers": [],
            "dependencies": [],
            "path": "direcao-criativa/ideacao/SKILL.md"
        },
        {
            "id": "moodboard",
            "category": "Direcao Criativa",
            "title": "Moodboard",
            "description": "\"Criação de moodboards textuais e referências visuais para produções criativas\"",
            "triggers": [
                "/campanhas"
            ],
            "dependencies": [],
            "path": "direcao-criativa/moodboard/SKILL.md"
        },
        {
            "id": "naming",
            "category": "Direcao Criativa",
            "title": "Naming",
            "description": "\"Naming de produtos, marcas e campanhas com verificação de disponibilidade para o mercado BR\"",
            "triggers": [
                "/significado"
            ],
            "dependencies": [],
            "path": "direcao-criativa/naming/SKILL.md"
        },
        {
            "id": "narrativa-visual",
            "category": "Direcao Criativa",
            "title": "Narrativa Visual",
            "description": "\"Narrativa visual para marcas: arco dramático, personagens e emoção na comunicação\"",
            "triggers": [],
            "dependencies": [],
            "path": "direcao-criativa/narrativa-visual/SKILL.md"
        },
        {
            "id": "roteiro-video",
            "category": "Direcao Criativa",
            "title": "Roteiro Video",
            "description": "\"Roteiro para vídeos publicitários, institucionais e de produto no mercado brasileiro\"",
            "triggers": [
                "/contato"
            ],
            "dependencies": [],
            "path": "direcao-criativa/roteiro-video/SKILL.md"
        },
        {
            "id": "tagline",
            "category": "Direcao Criativa",
            "title": "Tagline",
            "description": "\"Criação de taglines, slogans e brand promises memoráveis para marcas brasileiras\"",
            "triggers": [
                "/emocional",
                "/funcional",
                "/aspiracional"
            ],
            "dependencies": [],
            "path": "direcao-criativa/tagline/SKILL.md"
        }
    ],
    "Engineering": [
        {
            "id": "agent-designer",
            "category": "Engineering",
            "title": "Agent Designer",
            "description": "\"Use quando o usuário pede para projetar sistemas multi-agente, criar arquiteturas de agentes, definir padrões de comunicação entre agentes ou construir workflows de agentes autônomos.\"",
            "triggers": [
                "/sa"
            ],
            "dependencies": [],
            "path": "engineering/agent-designer/SKILL.md"
        },
        {
            "id": "agent-workflow-designer",
            "category": "Engineering",
            "title": "Agent Workflow Designer",
            "description": "\"Projeta workflows multi-agente de nível produção com escolha clara de padrão, contratos de transferência, tratamento de falhas e controles de custo e contexto.\"",
            "triggers": [
                "/tipo",
                "/incident-triage",
                "/workflow-patterns",
                "/fan-in",
                "/retry",
                "/timeout",
                "/workflow"
            ],
            "dependencies": [],
            "path": "engineering/agent-workflow-designer/SKILL.md"
        },
        {
            "id": "agenthub",
            "category": "Engineering",
            "title": "Agenthub",
            "description": "\"Plugin de colaboração multi-agente que lança N subagentes paralelos competindo na mesma tarefa via isolamento por git worktree. Os agentes trabalham de forma independente, os resultados são avaliados por métrica ou juiz LLM, e o melhor branch é mergeado. Use quando: o usuário quer múltiplas abordagens testadas em paralelo — otimização de código, variação de conteúdo, exploração de pesquisa ou qualquer tarefa que se beneficie de competição paralela. Requer: um repositório git.\"",
            "triggers": [
                "/archive",
                "/config",
                "/board",
                "/attempt-",
                "/escrever",
                "/dispatch",
                "/agent-templates",
                "/dag",
                "/skills",
                "/sessions",
                "/state",
                "/agenthub",
                "/agent-",
                "/results",
                "/descartar",
                "/result",
                "/hub"
            ],
            "dependencies": [],
            "path": "engineering/agenthub/SKILL.md"
        },
        {
            "id": "api-design-reviewer",
            "category": "Engineering",
            "title": "Api Design Reviewer",
            "description": "\"Revisão e análise completa de designs de API com foco em convenções REST, melhores práticas e padrões da indústria. Fornece linting automatizado, detecção de mudanças disruptivas e scorecards de design.\"",
            "triggers": [
                "/api",
                "/profile",
                "/user-profiles",
                "/deactivate",
                "/v1",
                "/openapi",
                "/v2",
                "/scripts",
                "/user",
                "/breaking",
                "/get",
                "/line",
                "/payments",
                "/api-design-reviewer",
                "/activate",
                "/users",
                "/vnd",
                "/modifica",
                "/orders",
                "/line-items",
                "/123",
                "/bash",
                "/bin"
            ],
            "dependencies": [],
            "path": "engineering/api-design-reviewer/SKILL.md"
        },
        {
            "id": "api-test-suite-builder",
            "category": "Engineering",
            "title": "Api Test Suite Builder",
            "description": "\"Use quando o usuário pede para gerar testes de API, criar suites de testes de integração, testar endpoints REST ou construir testes de contrato.\"",
            "triggers": [
                "/422",
                "/null",
                "/api",
                "/404",
                "/dev",
                "/route",
                "/expirados",
                "/500",
                "/vazia",
                "/after",
                "/403",
                "/app",
                "/campos",
                "/example-test-files",
                "/src",
                "/fixtures",
                "/401",
                "/inv"
            ],
            "dependencies": [],
            "path": "engineering/api-test-suite-builder/SKILL.md"
        },
        {
            "id": "autoresearch-agent",
            "category": "Engineering",
            "title": "Autoresearch Agent",
            "description": "\"Loop autônomo de experimentos que otimiza qualquer arquivo por uma métrica mensurável. Inspirado no autoresearch do Karpathy. O agente edita um arquivo alvo, executa uma avaliação fixa, mantém melhorias (git commit), descarta falhas (git reset) e faz loop indefinidamente. Use quando: o usuário quer otimizar velocidade de código, reduzir tamanho de bundle/imagem, melhorar taxa de aprovação em testes, otimizar prompts, melhorar qualidade de conteúdo (headlines, copy, CTR) ou executar qualquer loop de melhoria mensurável. Requer: um arquivo alvo, um comando de avaliação que gere uma métrica e um repositório git.\"",
            "triggers": [
                "/api",
                "/compila",
                "/skills",
                "/usr",
                "/100",
                "/titles",
                "/api-speed",
                "/github",
                "/config",
                "/autoresearch",
                "/claude-skills",
                "/autoresearch-agent",
                "/search",
                "/karpathy",
                "/run",
                "/log",
                "/10",
                "/docs",
                "/imagem",
                "/env",
                "/alirezarezvani",
                "/engineering",
                "/setup",
                "/regras",
                "/ar",
                "/bin"
            ],
            "dependencies": [],
            "path": "engineering/autoresearch-agent/SKILL.md"
        },
        {
            "id": "behuman",
            "category": "Engineering",
            "title": "Behuman",
            "description": "\"Use quando o usuário quiser respostas de IA mais humanas — menos robóticas, menos listadas, mais autênticas. Gatilhos: 'behuman', 'seja real', 'como um humano', 'mais humano', 'menos IA', 'fale como uma pessoa', 'modo espelho', 'pare de ser tão IA', ou quando as conversas forem emocionalmente carregadas (luto, perda de emprego, conselho de relacionamento, medo). NÃO para perguntas técnicas, geração de código ou consultas factuais.\"",
            "triggers": [
                "/github",
                "/api-integration",
                "/content-humanizer",
                "/senior-prompt-engineer",
                "/voidborne-d",
                "/copywriting"
            ],
            "dependencies": [],
            "path": "engineering/behuman/SKILL.md"
        },
        {
            "id": "browser-automation",
            "category": "Engineering",
            "title": "Browser Automation",
            "description": "\"Use quando o usuário pedir para automatizar tarefas no navegador, fazer scraping de sites, preencher formulários, capturar screenshots, extrair dados estruturados de páginas web ou construir workflows de automação web. NÃO para testes — use playwright-pro para isso.\"",
            "triggers": [
                "/finally",
                "/api",
                "/await",
                "/segundo",
                "/anti",
                "/canvas",
                "/except",
                "/encadeados",
                "/data",
                "/playwright",
                "/restaurar"
            ],
            "dependencies": [],
            "path": "engineering/browser-automation/SKILL.md"
        },
        {
            "id": "changelog-generator",
            "category": "Engineering",
            "title": "Changelog Generator",
            "description": "\"Gerador de Changelog — produz notas de versão consistentes e auditáveis a partir de Conventional Commits, com detecção de bump semântico e renderização de seções Keep a Changelog.\"",
            "triggers": [
                "/chore",
                "/ci-integration",
                "/commit",
                "/stdin",
                "/monorepo-strategy",
                "/main",
                "/corpo",
                "/generate",
                "/changelog-formatting-guide"
            ],
            "dependencies": [],
            "path": "engineering/changelog-generator/SKILL.md"
        },
        {
            "id": "ci-cd-pipeline-builder",
            "category": "Engineering",
            "title": "Ci Cd Pipeline Builder",
            "description": "\"Construtor de Pipeline CI/CD — gera pipelines pragmáticos a partir de sinais detectados do stack do projeto, com estágios de lint, test, build e deploy, e suporte a GitHub Actions e GitLab CI.\"",
            "triggers": [
                "/build",
                "/vari",
                "/github-actions-templates",
                "/ambiente",
                "/deployment-gates",
                "/ci",
                "/gitlab-ci-templates",
                "/runtime",
                "/stack",
                "/ambientes",
                "/workflows",
                "/rollback",
                "/test",
                "/aprova",
                "/ferramental",
                "/pipeline"
            ],
            "dependencies": [],
            "path": "engineering/ci-cd-pipeline-builder/SKILL.md"
        },
        {
            "id": "code-tour",
            "category": "Engineering",
            "title": "Code Tour",
            "description": "\"Use quando o usuário pedir para criar um arquivo CodeTour .tour — walkthroughs passo a passo direcionados a personas que linkam para arquivos reais e números de linha. Gatilho para: criar um tour, tour de integração, tour de arquitetura, tour de revisão de PR, explicar como X funciona, vibe check, tour de RCA, guia do contribuidor, ou qualquer solicitação de walkthrough de código estruturado.\"",
            "triggers": [
                "/blob",
                "/github",
                "/aka",
                "/microsoft",
                "/services",
                "/linha",
                "/auth",
                "/codebase-onboarding",
                "/contributing",
                "/encerramento",
                "/codetour",
                "/pr-review-expert",
                "/main",
                "/coder",
                "/codetour-schema",
                "/code-server"
            ],
            "dependencies": [],
            "path": "engineering/code-tour/SKILL.md"
        },
        {
            "id": "codebase-onboarding",
            "category": "Engineering",
            "title": "Codebase Onboarding",
            "description": "\"Onboarding de Base de Código — analisa um repositório e gera documentação de integração para engenheiros, tech leads e contratados, com descoberta de arquitetura e stack, inventário de arquivos-chave e orientação de configuração local.\"",
            "triggers": [
                "/path",
                "/output-format-templates",
                "/onboarding-template",
                "/codebase",
                "/to",
                "/repo"
            ],
            "dependencies": [],
            "path": "engineering/codebase-onboarding/SKILL.md"
        },
        {
            "id": "data-quality-auditor",
            "category": "Engineering",
            "title": "Data Quality Auditor",
            "description": "Audite conjuntos de dados quanto à completude, consistência, precisão e validade. Perfil de distribuições de dados, detecção de anomalias e outliers, identificação de problemas estruturais e produção de um plano de remediação acionável.",
            "triggers": [
                "/data",
                "/financial-analyst",
                "/eventos",
                "/reprovado",
                "/moda",
                "/saas-metrics-coach",
                "/desvio",
                "/data-quality-concepts",
                "/database-designer",
                "/tech-debt-tracker",
                "/product-analytics",
                "/ausentes",
                "/outlier",
                "/100",
                "/missing",
                "/max"
            ],
            "dependencies": [],
            "path": "engineering/data-quality-auditor/SKILL.md"
        },
        {
            "id": "database-designer",
            "category": "Engineering",
            "title": "Database Designer",
            "description": "\"Use quando o usuário pedir para projetar schemas de banco de dados, planejar migrações de dados, otimizar queries, escolher entre SQL e NoSQL, ou modelar relacionamentos de dados.\"",
            "triggers": [
                "/merge",
                "/escrita",
                "/sub",
                "/servidores",
                "/statement",
                "/tabela",
                "/database-design-reference",
                "/edge",
                "/test",
                "/gerentes"
            ],
            "dependencies": [],
            "path": "engineering/database-designer/SKILL.md"
        },
        {
            "id": "database-schema-designer",
            "category": "Engineering",
            "title": "Database Schema Designer",
            "description": "\"Use quando o usuário pedir para criar diagramas ERD, normalizar schemas de banco de dados, projetar relacionamentos de tabelas ou planejar migrações de schema.\"",
            "triggers": [
                "/faker",
                "/auth",
                "/modelos",
                "/src",
                "/cli",
                "/depois",
                "/lib",
                "/schema",
                "/client",
                "/full-schema-examples",
                "/cuid2",
                "/seed"
            ],
            "dependencies": [],
            "path": "engineering/database-schema-designer/SKILL.md"
        },
        {
            "id": "demo-video",
            "category": "Engineering",
            "title": "Demo Video",
            "description": "\"Use quando o usuário pedir para criar um vídeo de demonstração, walkthrough de produto, showcase de funcionalidade, apresentação animada, vídeo de marketing ou GIF a partir de screenshots ou descrições de cenas. Orquestra playwright, ffmpeg e edge-tts MCPs para produzir conteúdo de vídeo polido.\"",
            "triggers": [
                "/terminal",
                "/github",
                "/vaddisrinivas",
                "/scene-design-system",
                "/browser-automation",
                "/framecraft"
            ],
            "dependencies": [],
            "path": "engineering/demo-video/SKILL.md"
        },
        {
            "id": "dependency-auditor",
            "category": "Engineering",
            "title": "Dependency Auditor",
            "description": "\"Auditor de Dependências — analisa, audita e gerencia dependências em projetos multi-linguagem, identificando vulnerabilidades, garantindo conformidade de licença, otimizando árvores de dependência e planejando atualizações seguras.\"",
            "triggers": [
                "/path",
                "/minor",
                "/prod",
                "/staging",
                "/cr",
                "/upgrade",
                "/audit",
                "/to",
                "/propriet",
                "/license",
                "/project",
                "/usadas",
                "/dep"
            ],
            "dependencies": [],
            "path": "engineering/dependency-auditor/SKILL.md"
        },
        {
            "id": "docker-development",
            "category": "Engineering",
            "title": "Docker Development",
            "description": "\"Skill e plugin para desenvolvimento Docker e container no Claude Code para otimização de Dockerfile, orquestração docker-compose, builds multi-stage e hardening de segurança de container. Use quando: o usuário quiser otimizar um Dockerfile, criar ou melhorar configurações docker-compose, implementar builds multi-stage, auditar segurança de container, reduzir tamanho de imagem ou seguir melhores práticas de container.\"",
            "triggers": [
                "/lists",
                "/docker-development",
                "/docker",
                "/dockerfile",
                "/skills",
                "/server",
                "/usr",
                "/app",
                "/framework",
                "/lib",
                "/local",
                "/github",
                "/compose",
                "/node",
                "/index",
                "/claude-skills",
                "/etc",
                "/install",
                "/root",
                "/run",
                "/prod",
                "/distroless",
                "/cmd",
                "/alpine",
                "/to",
                "/var",
                "/apt",
                "/alirezarezvani",
                "/static",
                "/engineering",
                "/static-debian12",
                "/dist"
            ],
            "dependencies": [],
            "path": "engineering/docker-development/SKILL.md"
        },
        {
            "id": "env-secrets-manager",
            "category": "Engineering",
            "title": "Env Secrets Manager",
            "description": "\"Gerenciador de Env e Secrets — gerencia higiene de variáveis de ambiente e segurança de secrets em workflows de desenvolvimento local e produção, com auditoria, detecção de vazamento e orientação de rotação.\"",
            "triggers": [
                "/path",
                "/validation-detection-rotation",
                "/de",
                "/secret-patterns",
                "/github",
                "/infrastructure-as-code",
                "/env",
                "/senior-secops",
                "/configure-aws-credentials",
                "/to",
                "/secrets-vault-manager",
                "/falsos",
                "/repo",
                "/container-orchestration",
                "/resposta",
                "/ci-cd-pipeline-builder",
                "/detect-secrets"
            ],
            "dependencies": [],
            "path": "engineering/env-secrets-manager/SKILL.md"
        },
        {
            "id": "focused-fix",
            "category": "Engineering",
            "title": "Focused Fix",
            "description": "\"Use quando o usuário pedir para corrigir, depurar ou fazer uma funcionalidade/módulo/área específica funcionar de ponta a ponta. Gatilhos: 'faça X funcionar', 'corrija a funcionalidade Y', 'o módulo Z está quebrado', 'foque em [área]'. Não para correções rápidas de bug único — isso é para reparo sistemático e profundo em todos os arquivos e dependências.\"",
            "triggers": [
                "/arquivos",
                "/api",
                "/features",
                "/auth",
                "/service",
                "/login",
                "/app",
                "/assinaturas",
                "/lib",
                "/controle",
                "/db",
                "/repository",
                "/route",
                "/exporta",
                "/23",
                "/interface",
                "/pasta",
                "/jwt",
                "/module",
                "/middleware",
                "/schema",
                "/schemas",
                "/types",
                "/register",
                "/client"
            ],
            "dependencies": [],
            "path": "engineering/focused-fix/SKILL.md"
        },
        {
            "id": "git-worktree-manager",
            "category": "Engineering",
            "title": "Git Worktree Manager",
            "description": "\"Gerenciador de Git Worktree — executa trabalho paralelo em funcionalidades com segurança usando worktrees Git, com isolamento de branch, alocação de porta, sincronização de ambiente e limpeza padronizados.\"",
            "triggers": [
                "/port-allocation-strategy",
                "/logs",
                "/new-auth",
                "/docker-compose-patterns",
                "/worktree",
                "/listar",
                "/persistir",
                "/processo"
            ],
            "dependencies": [],
            "path": "engineering/git-worktree-manager/SKILL.md"
        },
        {
            "id": "helm-chart-builder",
            "category": "Engineering",
            "title": "Helm Chart Builder",
            "description": "\"Skill e plugin para desenvolvimento de Helm chart no Claude Code — scaffolding de chart, design de values, padrões de template, gerenciamento de dependências, hardening de segurança e testes de chart. Use quando: o usuário quiser criar ou melhorar Helm charts, projetar arquivos values.yaml, implementar template helpers, auditar segurança de chart (RBAC, network policies, pod security), gerenciar subcharts ou executar helm lint/test.\"",
            "triggers": [
                "/limits",
                "/skills",
                "/chart",
                "/name",
                "/test",
                "/helm",
                "/github",
                "/v1",
                "/claude-skills",
                "/version",
                "/instance",
                "/tmp",
                "/readiness",
                "/managed-by",
                "/false",
                "/helm-chart-builder",
                "/alirezarezvani",
                "/engineering",
                "/values"
            ],
            "dependencies": [],
            "path": "engineering/helm-chart-builder/SKILL.md"
        },
        {
            "id": "interview-system-designer",
            "category": "Engineering",
            "title": "Interview System Designer",
            "description": "\"Esta skill deve ser usada quando o usuário pedir para 'projetar processos de entrevista', 'criar pipelines de contratação', 'calibrar loops de entrevista', 'gerar perguntas de entrevista', 'projetar matrizes de competência', 'analisar viés do entrevistador', 'criar rubricas de pontuação', 'construir bancos de perguntas' ou 'otimizar sistemas de contratação'. Use para projetar loops de entrevista específicos por função, avaliações de competência e sistemas de calibração de contratação.\"",
            "triggers": [
                "/bias",
                "/competency",
                "/interview-frameworks",
                "/debrief",
                "/interview"
            ],
            "dependencies": [],
            "path": "engineering/interview-system-designer/SKILL.md"
        },
        {
            "id": "karpathy-coder",
            "category": "Engineering",
            "title": "Karpathy Coder",
            "description": "Use quando escrever, revisar ou commitar código para aplicar os 4 princípios de codificação de Karpathy — explicite suposições antes de codificar, mantenha simples, faça mudanças cirúrgicas, defina objetivos verificáveis. Gatilhos em \"revise meu diff\", \"verifique complexidade\", \"estou complicando demais?\", \"karpathy check\", \"antes de commitar\", ou qualquer preocupação de qualidade de código onde o LLM possa estar sobrecodificando.",
            "triggers": [
                "/anti-patterns",
                "/vari",
                "/2015883857489522876",
                "/status",
                "/karpathy-principles",
                "/settings",
                "/enforcement-patterns",
                "/depois",
                "/karpathy-gate",
                "/karpathy-check",
                "/fun",
                "/karpathy"
            ],
            "dependencies": [],
            "path": "engineering/karpathy-coder/SKILL.md"
        },
        {
            "id": "llm-cost-optimizer",
            "category": "Engineering",
            "title": "Llm Cost Optimizer",
            "description": "\"Use quando você precisa reduzir os gastos com API de LLM, controlar o uso de tokens, rotear entre modelos por custo/qualidade, implementar cache de prompts ou construir observabilidade de custos para features de IA. Gatilhos: 'meus custos de IA estão muito altos', 'otimizar uso de tokens', 'qual modelo devo usar', 'gastos com LLM fora de controle', 'implementar cache de prompts'. NÃO para design de pipeline RAG (use rag-architect). NÃO para qualidade de escrita de prompts (use senior-prompt-engineer).\"",
            "triggers": [
                "/similares",
                "/endpoints",
                "/qualidade",
                "/depois",
                "/estruturadas",
                "/markdown",
                "/feature"
            ],
            "dependencies": [],
            "path": "engineering/llm-cost-optimizer/SKILL.md"
        },
        {
            "id": "llm-wiki",
            "category": "Engineering",
            "title": "Llm Wiki",
            "description": "Use quando estiver construindo ou mantendo uma base de conhecimento pessoal persistente (segundo cérebro) no Obsidian, onde um LLM ingere fontes de forma incremental, atualiza páginas de entidades/conceitos, mantém referências cruzadas e mantém uma síntese atualizada. Gatilhos incluem \"segundo cérebro\", \"wiki no Obsidian\", \"gestão de conhecimento pessoal\", \"ingerir este paper/artigo/livro\", \"construir um wiki de pesquisa\", \"conhecimento acumulado\", \"Memex\", ou sempre que o usuário quiser que o conhecimento se acumule entre sessões em vez de ser redescoberto por RAG a cada consulta.",
            "triggers": [
                "/wiki-query",
                "/wiki-lint",
                "/frontmatter",
                "/equipe",
                "/wiki-ingest",
                "/raw",
                "/github",
                "/cross-tool-setup",
                "/livro",
                "/obsidian-setup",
                "/tobi",
                "/gist",
                "/research",
                "/query-workflow",
                "/ingest-workflow",
                "/karpathy",
                "/init",
                "/wiki-init",
                "/listas",
                "/memex-principles",
                "/conceitos",
                "/442a6bf555914893e9891c11519de94f",
                "/lint-workflow",
                "/vaults",
                "/assets",
                "/wiki-log",
                "/page-formats",
                "/artigo",
                "/wiki-schema",
                "/wiki",
                "/qmd",
                "/anthropic-monosemanticity"
            ],
            "dependencies": [],
            "path": "engineering/llm-wiki/SKILL.md"
        },
        {
            "id": "mcp-server-builder",
            "category": "Engineering",
            "title": "Mcp Server Builder",
            "description": "\"Construtor de servidores MCP. Use para projetar e entregar servidores MCP prontos para produção a partir de contratos de API, em vez de wrappers manuais de ferramentas. Foca em scaffolding rápido, qualidade de esquema, validação e evolução segura.\"",
            "triggers": [
                "/alterados",
                "/backend",
                "/openapi",
                "/validation-checklist",
                "/removidos",
                "/mcp",
                "/openapi-extraction-guide",
                "/typescript-server-template",
                "/externa",
                "/python-server-template",
                "/runtime",
                "/opera",
                "/tool",
                "/5xx",
                "/out",
                "/processo"
            ],
            "dependencies": [],
            "path": "engineering/mcp-server-builder/SKILL.md"
        },
        {
            "id": "migration-architect",
            "category": "Engineering",
            "title": "Migration Architect",
            "description": "\"Arquiteto de Migração. Planejamento de migração com zero downtime, validação de compatibilidade e geração de estratégia de rollback.\"",
            "triggers": [
                "/servi",
                "/compatibility",
                "/tabelas",
                "/gateway",
                "/migration",
                "/minuto"
            ],
            "dependencies": [],
            "path": "engineering/migration-architect/SKILL.md"
        },
        {
            "id": "monorepo-navigator",
            "category": "Engineering",
            "title": "Monorepo Navigator",
            "description": "\"Navegador de Monorepo. Navega, gerencia e otimiza monorepos com Turborepo, Nx, pnpm workspaces e Lerna. Análise de impacto entre pacotes, builds seletivos, cache remoto e visualização de grafo de dependências.\"",
            "triggers": [
                "/testes",
                "/projeto",
                "/monorepo-tooling-reference",
                "/para",
                "/types",
                "/monorepo",
                "/monorepo-patterns",
                "/main",
                "/apps",
                "/builds",
                "/caminho"
            ],
            "dependencies": [],
            "path": "engineering/monorepo-navigator/SKILL.md"
        },
        {
            "id": "observability-designer",
            "category": "Engineering",
            "title": "Observability Designer",
            "description": "\"Designer de Observabilidade (PODEROSO). Projeta estratégias abrangentes de observabilidade para sistemas em produção, incluindo frameworks SLI/SLO, otimização de alertas e geração de painéis.\"",
            "triggers": [
                "/sistema"
            ],
            "dependencies": [],
            "path": "engineering/observability-designer/SKILL.md"
        },
        {
            "id": "performance-profiler",
            "category": "Engineering",
            "title": "Performance Profiler",
            "description": "\"Profiler de Desempenho. Profiling sistemático de desempenho para aplicações Node.js, Python e Go. Identifica gargalos de CPU, memória e I/O, gera flamegraphs, analisa tamanhos de bundle, otimiza consultas de banco de dados, detecta vazamentos de memória e executa testes de carga.\"",
            "triggers": [
                "/projeto",
                "/para",
                "/req",
                "/depois",
                "/date-fns",
                "/stringify",
                "/profiling-recipes",
                "/performance",
                "/image",
                "/caminho",
                "/brotli"
            ],
            "dependencies": [],
            "path": "engineering/performance-profiler/SKILL.md"
        },
        {
            "id": "pr-review-expert",
            "category": "Engineering",
            "title": "Pr Review Expert",
            "description": "\"Use quando o usuário pede para revisar pull requests, analisar mudanças de código, verificar questões de segurança em PRs, ou avaliar a qualidade do código de diffs.\"",
            "triggers": [
                "/null",
                "/rest",
                "/api",
                "/your-org",
                "/auth",
                "/esquemas",
                "/pr-",
                "/logs",
                "/db",
                "/map",
                "/reset",
                "/for",
                "/autoriza",
                "/pagamentos",
                "/admin",
                "/dev",
                "/tmp",
                "/mr-",
                "/sanitizadas",
                "/reports",
                "/issue",
                "/interfaces",
                "/services",
                "/users",
                "/linear"
            ],
            "dependencies": [],
            "path": "engineering/pr-review-expert/SKILL.md"
        },
        {
            "id": "prompt-governance",
            "category": "Engineering",
            "title": "Prompt Governance",
            "description": "\"Use quando gerenciar prompts em produção em escala: versionamento de prompts, execução de testes A/B em prompts, construção de registros de prompts, prevenção de regressões de prompts ou criação de pipelines de avaliação para features de IA em produção. Gatilhos: 'gerenciar prompts em produção', 'versionamento de prompts', 'regressão de prompts', 'teste A/B de prompts', 'registro de prompts', 'pipeline de avaliação'. NÃO para escrever ou melhorar prompts individuais (use senior-prompt-engineer). NÃO para design de pipeline RAG (use rag-architect). NÃO para redução de custos de LLM (use llm-cost-optimizer).\"",
            "triggers": [
                "/sa",
                "/extra",
                "/templates",
                "/v1"
            ],
            "dependencies": [],
            "path": "engineering/prompt-governance/SKILL.md"
        },
        {
            "id": "rag-architect",
            "category": "Engineering",
            "title": "Rag Architect",
            "description": "\"Use quando o usuário pede para projetar pipelines RAG, otimizar estratégias de recuperação, escolher modelos de embedding, implementar busca vetorial ou construir sistemas de recuperação de conhecimento.\"",
            "triggers": [
                "/seg",
                "/longos",
                "/frios",
                "/entidades",
                "/all-mpnet-base-v2",
                "/mornos",
                "/all-"
            ],
            "dependencies": [],
            "path": "engineering/rag-architect/SKILL.md"
        },
        {
            "id": "release-manager",
            "category": "Engineering",
            "title": "Release Manager",
            "description": "\"Use quando o usuário pede para planejar releases, gerenciar changelogs, coordenar implantações, criar branches de release ou automatizar versionamento.\"",
            "triggers": [
                "/login",
                "/critical-fix",
                "/package",
                "/payment"
            ],
            "dependencies": [],
            "path": "engineering/release-manager/SKILL.md"
        },
        {
            "id": "runbook-generator",
            "category": "Engineering",
            "title": "Runbook Generator",
            "description": "\"Gerador de Runbook. Gera runbooks operacionais rapidamente a partir do nome do serviço e personaliza para fluxos de trabalho de implantação, resposta a incidentes, manutenção e rollback.\"",
            "triggers": [
                "/runbook",
                "/sa",
                "/runbooks",
                "/runbook-templates",
                "/parada",
                "/payments-api",
                "/rollback",
                "/escalonamento"
            ],
            "dependencies": [],
            "path": "engineering/runbook-generator/SKILL.md"
        },
        {
            "id": "secrets-vault-manager",
            "category": "Engineering",
            "title": "Secrets Vault Manager",
            "description": "\"Use quando o usuário pede para configurar infraestrutura de gerenciamento de segredos, integrar o HashiCorp Vault, configurar armazenamentos de segredos em nuvem (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager), implementar rotação de segredos ou auditar padrões de acesso a segredos.\"",
            "triggers": [
                "/postgres",
                "/staging",
                "/ui",
                "/api",
                "/role",
                "/auth",
                "/faixa",
                "/agent-inject",
                "/atualiza",
                "/app",
                "/roles",
                "/oidc",
                "/data",
                "/api-server",
                "/config",
                "/revoga",
                "/v1beta1",
                "/agent-inject-secret-db",
                "/versions",
                "/payment",
                "/dados",
                "/vault-action",
                "/prod",
                "/creds",
                "/emergency",
                "/payment-readonly",
                "/ci",
                "/deploy",
                "/agent-inject-template-db",
                "/production",
                "/callback",
                "/payment-service",
                "/engineering",
                "/app-readonly",
                "/unseal",
                "/kubernetes",
                "/vault",
                "/approle",
                "/secrets"
            ],
            "dependencies": [],
            "path": "engineering/secrets-vault-manager/SKILL.md"
        },
        {
            "id": "self-eval",
            "category": "Engineering",
            "title": "Self Eval",
            "description": "\"Avalie honestamente a qualidade do trabalho de IA usando um sistema de pontuação em dois eixos. Use após concluir uma tarefa, revisão de código ou sessão de trabalho para obter uma avaliação imparcial. Detecta inflação de pontuação, força raciocínio do advogado do diabo e persiste pontuações entre sessões.\"",
            "triggers": [
                "/self-eval"
            ],
            "dependencies": [],
            "path": "engineering/self-eval/SKILL.md"
        },
        {
            "id": "skill-security-auditor",
            "category": "Engineering",
            "title": "Skill Security Auditor",
            "description": ">",
            "triggers": [
                "/npm",
                "/path",
                "/github",
                "/skill-repo",
                "/scanner",
                "/analyzer",
                "/scripts",
                "/new-skill",
                "/skills",
                "/to",
                "/skill",
                "/user",
                "/helper",
                "/threat-model",
                "/skill-name",
                "/repo",
                "/etc"
            ],
            "dependencies": [],
            "path": "engineering/skill-security-auditor/SKILL.md"
        },
        {
            "id": "skill-tester",
            "category": "Engineering",
            "title": "Skill Tester",
            "description": "\"Testador de Skills — meta-skill para validar, testar e pontuar a qualidade de skills dentro do ecossistema claude-skills. Use para garantir conformidade estrutural, testar scripts Python e realizar avaliação de qualidade multidimensional com notas e recomendações de melhoria.\"",
            "triggers": [
                "/setup-python",
                "/quality",
                "/hooks",
                "/checkout",
                "/script",
                "/scripts",
                "/new-skill",
                "/example-skill",
                "/pre-commit",
                "/bin",
                "/to",
                "/skill",
                "/skill-tester",
                "/25",
                "/sa",
                "/bash",
                "/100",
                "/trend"
            ],
            "dependencies": [],
            "path": "engineering/skill-tester/SKILL.md"
        },
        {
            "id": "spec-driven-workflow",
            "category": "Engineering",
            "title": "Spec Driven Workflow",
            "description": "\"Use quando o usuário pede para escrever specs antes do código, definir critérios de aceitação, planejar funcionalidades antes da implementação, gerar testes a partir de especificações, ou seguir práticas de desenvolvimento spec-first.\"",
            "triggers": [
                "/bounded",
                "/spec-driven-workflow",
                "/rag-architect",
                "/auth",
                "/descri",
                "/focused-fix",
                "/acceptance",
                "/ruins",
                "/test",
                "/tdd-guide",
                "/resposta",
                "/spec"
            ],
            "dependencies": [],
            "path": "engineering/spec-driven-workflow/SKILL.md"
        },
        {
            "id": "sql-database-assistant",
            "category": "Engineering",
            "title": "Sql Database Assistant",
            "description": "\"Use quando o usuário pede para escrever queries SQL, otimizar desempenho de banco de dados, gerar migrações, explorar esquemas de banco de dados, ou trabalhar com ORMs como Prisma, Drizzle, TypeORM ou SQLAlchemy.\"",
            "triggers": [
                "/query",
                "/novo",
                "/linha",
                "/orm",
                "/down",
                "/optimization",
                "/schema",
                "/condi",
                "/migration"
            ],
            "dependencies": [],
            "path": "engineering/sql-database-assistant/SKILL.md"
        },
        {
            "id": "statistical-analyst",
            "category": "Engineering",
            "title": "Statistical Analyst",
            "description": "Execute testes de hipótese, analise resultados de experimentos A/B, calcule tamanhos de amostra e interprete significância estatística com tamanhos de efeito. Use quando precisar validar se diferenças observadas são reais, dimensionar um experimento corretamente antes do lançamento, ou interpretar resultados de testes com confiança.",
            "triggers": [
                "/experiment-designer",
                "/hypothesis",
                "/sample",
                "/saas-metrics-coach",
                "/ab-test-setup",
                "/data-quality-auditor",
                "/campaign-analytics",
                "/product-analytics",
                "/statistical-testing-concepts",
                "/confidence"
            ],
            "dependencies": [],
            "path": "engineering/statistical-analyst/SKILL.md"
        },
        {
            "id": "tc-tracker",
            "category": "Engineering",
            "title": "Tc Tracker",
            "description": "\"Use quando o usuário pede para rastrear mudanças técnicas, criar registros de mudanças, gerenciar ciclos de vida de TCs, ou fazer handoff de trabalho entre sessões de IA. Cobre fluxos de trabalho init/create/update/status/resume/close/export para documentação estruturada de mudanças de código.\"",
            "triggers": [
                "/resume",
                "/status",
                "/auth",
                "/records",
                "/focused-fix",
                "/export",
                "/close",
                "/evidence",
                "/create",
                "/code-reviewer",
                "/tc",
                "/changelog-generator",
                "/docs",
                "/update",
                "/handoff-format",
                "/tc-schema",
                "/tech-debt-tracker",
                "/lifecycle",
                "/decision-log"
            ],
            "dependencies": [],
            "path": "engineering/tc-tracker/SKILL.md"
        },
        {
            "id": "tech-debt-tracker",
            "category": "Engineering",
            "title": "Tech Debt Tracker",
            "description": "Escanear bases de código em busca de dívida técnica, pontuar severidade, rastrear tendências e gerar planos de remediação priorizados. Use quando os usuários mencionarem dívida técnica, qualidade de código, prioridade de refatoração, pontuação de dívida, sprints de limpeza ou avaliação de saúde do código. Também use para planejamento de modernização de código legado e estimativa de custo de manutenção.",
            "triggers": [
                "/debt-frameworks"
            ],
            "dependencies": [],
            "path": "engineering/tech-debt-tracker/SKILL.md"
        },
        {
            "id": "terraform-patterns",
            "category": "Engineering",
            "title": "Terraform Patterns",
            "description": "\"Skill de infraestrutura-como-código com Terraform para Claude Code. Cobre padrões de design de módulos, estratégias de gerenciamento de estado, configuração de providers, hardening de segurança, policy-as-code com Sentinel/OPA e fluxos CI/CD de plan/apply. Use quando o usuário quiser projetar módulos Terraform, gerenciar state backends, revisar segurança Terraform, implementar deploys multi-região ou seguir melhores práticas de IaC.\"",
            "triggers": [
                "/actions",
                "/locals",
                "/modules",
                "/name",
                "/workflows",
                "/apply",
                "/storage",
                "/heads",
                "/3389",
                "/bastion",
                "/infracost",
                "/tmp",
                "/tf",
                "/terragrunt",
                "/16",
                "/google",
                "/vpc",
                "/setup-terraform",
                "/terraform",
                "/azurerm",
                "/eks",
                "/checkout",
                "/random",
                "/setup",
                "/aws",
                "/main"
            ],
            "dependencies": [],
            "path": "engineering/terraform-patterns/SKILL.md"
        }
    ],
    "Assets": [
        {
            "id": "sample-skill",
            "category": "Assets",
            "title": "Sample Skill",
            "description": "",
            "triggers": [],
            "dependencies": [],
            "path": "engineering/skill-tester/assets/sample-skill/SKILL.md"
        }
    ],
    "Engineering Team": [
        {
            "id": "a11y-audit",
            "category": "Engineering Team",
            "title": "A11Y Audit",
            "description": "\"Skill de auditoria de acessibilidade para escanear, corrigir e verificar a conformidade WCAG 2.2 Nível A e AA em codebases React, Next.js, Vue, Angular, Svelte e HTML puro. Use ao auditar acessibilidade, corrigir violações de a11y, verificar contraste de cores, gerar relatórios de conformidade ou integrar verificações de acessibilidade em pipelines CI/CD.\"",
            "triggers": [
                "/blob",
                "/doc",
                "/testing-checklist",
                "/ci-cd-integration",
                "/div",
                "/apg",
                "/a11y",
                "/rule-descriptions",
                "/axe-core",
                "/framework-a11y-patterns",
                "/www",
                "/develop",
                "/github",
                "/a11y-audit",
                "/wcag-quick-ref",
                "/examples-by-framework",
                "/styles",
                "/audit-report-template",
                "/eslint-plugin-jsx-a11y",
                "/to",
                "/project",
                "/product",
                "/span",
                "/reprova",
                "/jsx-eslint",
                "/path",
                "/color-contrast-guide",
                "/components",
                "/contrast",
                "/depois",
                "/aria-patterns",
                "/wcag-22-new-criteria",
                "/dequelabs"
            ],
            "dependencies": [],
            "path": "engineering-team/a11y-audit/SKILL.md"
        },
        {
            "id": "adversarial-reviewer",
            "category": "Engineering Team",
            "title": "Adversarial Reviewer",
            "description": "\"Revisão de código adversarial que quebra a monocultura de auto-revisão. Use quando quiser uma revisão genuinamente crítica de mudanças recentes, antes de fazer merge de um PR, ou quando suspeitar que o Claude está sendo condescendente demais sobre a qualidade do código. Força mudanças de perspectiva por meio de personas de revisores hostis que capturam pontos cegos que o modelo mental do autor compartilha com o revisor.\"",
            "triggers": [
                "/undefined",
                "/auth",
                "/formata",
                "/adversarial-review",
                "/unstaged",
                "/senior-security",
                "/code-reviewer"
            ],
            "dependencies": [],
            "path": "engineering-team/adversarial-reviewer/SKILL.md"
        },
        {
            "id": "ai-security",
            "category": "Engineering Team",
            "title": "Ai Security",
            "description": "\"Use ao avaliar sistemas de IA/ML para injeção de prompt, vulnerabilidades de jailbreak, risco de inversão de modelo, exposição a envenenamento de dados ou abuso de ferramentas por agents. Cobre mapeamento de técnicas MITRE ATLAS, detecção de assinaturas de injeção e pontuação de robustez adversarial.\"",
            "triggers": [
                "/probabilidade",
                "/atlas-coverage",
                "/incident-response",
                "/ai",
                "/white-box",
                "/adversarial",
                "/security-pen-testing",
                "/cloud-security",
                "/threat-detection"
            ],
            "dependencies": [
                "Threat Detection",
                "Security Pen Testing",
                "Incident Response",
                "Cloud Security"
            ],
            "path": "engineering-team/ai-security/SKILL.md"
        },
        {
            "id": "aws-solution-architect",
            "category": "Engineering Team",
            "title": "Aws Solution Architect",
            "description": "Projete arquiteturas AWS para startups usando padrões serverless e templates de IaC. Use ao projetar arquitetura serverless, criar templates CloudFormation, otimizar custos AWS, configurar pipelines CI/CD ou migrar para AWS. Cobre Lambda, API Gateway, DynamoDB, ECS, Aurora e otimização de custos.",
            "triggers": [
                "/architecture",
                "/seg",
                "/best",
                "/service",
                "/serverless",
                "/aws-ecs",
                "/contras",
                "/cost",
                "/template",
                "/aws-ec2",
                "/privadas",
                "/aws-rds",
                "/baixa"
            ],
            "dependencies": [],
            "path": "engineering-team/aws-solution-architect/SKILL.md"
        },
        {
            "id": "azure-cloud-architect",
            "category": "Engineering Team",
            "title": "Azure Cloud Architect",
            "description": "\"Projete arquiteturas Azure para startups e empresas. Use ao projetar infraestrutura Azure, criar templates Bicep/ARM, otimizar custos Azure, configurar pipelines Azure DevOps ou migrar para Azure. Cobre AKS, App Service, Azure Functions, Cosmos DB e otimização de custos.\"",
            "triggers": [
                "/terraform-patterns",
                "/service",
                "/login",
                "/contras",
                "/bicep",
                "/aws-solution-architect",
                "/architecture",
                "/seg",
                "/gcp-cloud-architect",
                "/arm-deploy",
                "/databases",
                "/servers",
                "/infra",
                "/serverfarms",
                "/dia",
                "/sites",
                "/best",
                "/senior-devops",
                "/baixa",
                "/ci-cd-pipeline-builder",
                "/checkout",
                "/cost",
                "/main"
            ],
            "dependencies": [],
            "path": "engineering-team/azure-cloud-architect/SKILL.md"
        },
        {
            "id": "cloud-security",
            "category": "Engineering Team",
            "title": "Cloud Security",
            "description": "\"Use ao avaliar infraestrutura de nuvem para configurações incorretas de segurança, caminhos de escalada de privilégio IAM, exposição pública de S3, regras de grupo de segurança abertas ou lacunas de segurança em IaC. Cobre avaliação de postura em AWS, Azure e GCP com mapeamento MITRE ATT&CK.\"",
            "triggers": [
                "/cspm-checks",
                "/red-team",
                "/falso",
                "/cr",
                "/cloud",
                "/key-id",
                "/incident-response",
                "/security-pen-testing",
                "/threat-detection"
            ],
            "dependencies": [
                "Threat Detection",
                "Security Pen Testing",
                "Red Team",
                "Incident Response"
            ],
            "path": "engineering-team/cloud-security/SKILL.md"
        },
        {
            "id": "code-reviewer",
            "category": "Engineering Team",
            "title": "Code Reviewer",
            "description": "Automação de revisão de código para TypeScript, JavaScript, Python, Go, Swift, Kotlin. Analisa PRs quanto a complexidade e risco, verifica qualidade de código para violações SOLID e code smells, gera relatórios de revisão. Use ao revisar pull requests, analisar qualidade de código, identificar problemas ou gerar checklists de revisão.",
            "triggers": [
                "/path",
                "/common",
                "/await",
                "/pr",
                "/to",
                "/review",
                "/repo",
                "/code",
                "/coding"
            ],
            "dependencies": [],
            "path": "engineering-team/code-reviewer/SKILL.md"
        },
        {
            "id": "email-template-builder",
            "category": "Engineering Team",
            "title": "Email Template Builder",
            "description": "\"Construtor de templates de e-mail transacional. Cria sistemas completos de e-mail com React Email, integração com provedores, servidor de preview, suporte a i18n, modo escuro, otimização anti-spam e rastreamento de analytics. Produz código pronto para produção para Resend, Postmark, SendGrid ou AWS SES.\"",
            "triggers": [
                "/send",
                "/hotmail",
                "/i18n",
                "/tracking",
                "/footer",
                "/templates",
                "/lib",
                "/href",
                "/layout",
                "/localiza",
                "/email-layout",
                "/privacy",
                "/grid",
                "/welcome",
                "/render",
                "/out",
                "/fonts",
                "/inter",
                "/10",
                "/en",
                "/clique",
                "/v13",
                "/yourapp",
                "/logo",
                "/ul",
                "/de",
                "/components",
                "/style",
                "/invoice",
                "/li",
                "/localhost"
            ],
            "dependencies": [],
            "path": "engineering-team/email-template-builder/SKILL.md"
        },
        {
            "id": "epic-design",
            "category": "Engineering Team",
            "title": "Epic Design",
            "description": ">",
            "triggers": [
                "/conte",
                "/luxo",
                "/gsap",
                "/top",
                "/energ",
                "/div",
                "/directional-reveals",
                "/section",
                "/asset-pipeline",
                "/validate-layers",
                "/cinematogr",
                "/examples",
                "/text-animations",
                "/left",
                "/accessibility",
                "/sentimento",
                "/atmosfera",
                "/lados",
                "/cdn",
                "/index",
                "/npm",
                "/inspect-assets",
                "/inter-section-effects",
                "/to",
                "/part",
                "/empilhar",
                "/height",
                "/hero-section",
                "/cursor-microinteractions",
                "/escala",
                "/de",
                "/elemento",
                "/motion-system",
                "/est",
                "/h1",
                "/depth-system",
                "/performance",
                "/branco",
                "/dist"
            ],
            "dependencies": [],
            "path": "engineering-team/epic-design/SKILL.md"
        },
        {
            "id": "gcp-cloud-architect",
            "category": "Engineering Team",
            "title": "Gcp Cloud Architect",
            "description": "\"Projete arquiteturas GCP para startups e empresas. Use ao projetar infraestrutura Google Cloud, implantar no GKE ou Cloud Run, configurar pipelines BigQuery, otimizar custos GCP ou migrar para GCP. Cobre Cloud Run, GKE, Cloud Functions, Cloud SQL, BigQuery e otimização de custos.\"",
            "triggers": [
                "/docker",
                "/terraform-patterns",
                "/service",
                "/cloud-sdk",
                "/contras",
                "/aws-solution-architect",
                "/cloudsdktool",
                "/architecture",
                "/seg",
                "/my-app",
                "/products",
                "/calculator",
                "/cloud-builders",
                "/best",
                "/azure-cloud-architect",
                "/senior-devops",
                "/google",
                "/baixa",
                "/ci-cd-pipeline-builder",
                "/deployment",
                "/cloud",
                "/cost"
            ],
            "dependencies": [],
            "path": "engineering-team/gcp-cloud-architect/SKILL.md"
        },
        {
            "id": "google-workspace-cli",
            "category": "Engineering Team",
            "title": "Google Workspace Cli",
            "description": "\"Administração do Google Workspace via CLI gws. Instale, autentique e automatize Gmail, Drive, Sheets, Calendar, Docs, Chat e Tasks. Execute auditorias de segurança, use 43 receitas integradas e 10 pacotes de persona. Use para administração do Google Workspace, configuração da CLI gws, automação do Gmail, gerenciamento do Drive ou agendamento de Calendar.\"",
            "triggers": [
                "/output",
                "/github",
                "/path",
                "/ndjson",
                "/googleworkspace",
                "/table",
                "/key",
                "/config",
                "/auth",
                "/cli",
                "/to",
                "/gws",
                "/01",
                "/pdf",
                "/workspace",
                "/exportar",
                "/releases",
                "/ocupado"
            ],
            "dependencies": [],
            "path": "engineering-team/google-workspace-cli/SKILL.md"
        },
        {
            "id": "incident-commander",
            "category": "Engineering Team",
            "title": "Incident Commander",
            "description": "\"Skill de Comandante de Incidentes para gerenciar resposta a incidentes tecnológicos, desde a detecção até a resolução e revisão pós-incidente. Cobre classificação de severidade, reconstrução de linha do tempo e geração de PIR.\"",
            "triggers": [
                "/reference-information",
                "/resolvido",
                "/api",
                "/mitigando",
                "/percentagem",
                "/db",
                "/informa",
                "/pir",
                "/timeline",
                "/chat",
                "/teste",
                "/issue",
                "/incident"
            ],
            "dependencies": [],
            "path": "engineering-team/incident-commander/SKILL.md"
        },
        {
            "id": "incident-response",
            "category": "Engineering Team",
            "title": "Incident Response",
            "description": "\"Use quando um incidente de segurança foi detectado ou declarado e precisa de classificação, triagem, determinação de caminho de escalação e coleta de evidências forenses. Cobre classificação SEV1-SEV4, filtragem de falsos positivos, taxonomia de incidentes e ciclo de vida NIST SP 800-61.\"",
            "triggers": [
                "/red-team",
                "/incident",
                "/regulatory-deadlines",
                "/compliance-mapping",
                "/2555",
                "/security-pen-testing",
                "/deploy",
                "/cloud-security",
                "/threat-detection",
                "/18",
                "/679"
            ],
            "dependencies": [
                "Threat Detection",
                "Security Pen Testing",
                "Red Team",
                "Cloud Security"
            ],
            "path": "engineering-team/incident-response/SKILL.md"
        },
        {
            "id": "ms365-tenant-manager",
            "category": "Engineering Team",
            "title": "Ms365 Tenant Manager",
            "description": "Administração de tenant Microsoft 365 para Administradores Globais. Automatize configuração de tenant M365, tarefas de administração do Office 365, gerenciamento de usuários Azure AD, configuração do Exchange Online, administração do Teams e políticas de segurança. Gere scripts PowerShell para operações em massa, políticas de Acesso Condicional, gerenciamento de licenças e relatórios de conformidade. Use para gerenciamento de tenant M365, admin Office 365, usuários Azure AD, Administrador Global, configuração de tenant ou automação Microsoft 365.",
            "triggers": [
                "/catch",
                "/powershell-templates",
                "/troubleshooting",
                "/security-policies"
            ],
            "dependencies": [],
            "path": "engineering-team/ms365-tenant-manager/SKILL.md"
        },
        {
            "id": "playwright-pro",
            "category": "Engineering Team",
            "title": "Playwright Pro",
            "description": "\"Toolkit de testes Playwright de nível produção. Use quando o usuário menciona testes Playwright, testes E2E, automação de navegador, correção de testes instáveis, migração de testes, testes CI/CD ou suites de testes. Gere testes, corrija falhas instáveis, migre do Cypress/Selenium, sincronize com TestRail, execute no BrowserStack. 55 templates, 3 agents, relatórios inteligentes.\"",
            "triggers": [
                "/your-instance",
                "/inst",
                "/auth",
                "/login",
                "/pw"
            ],
            "dependencies": [],
            "path": "engineering-team/playwright-pro/SKILL.md"
        },
        {
            "id": "red-team",
            "category": "Engineering Team",
            "title": "Red Team",
            "description": "\"Use quando planejar ou executar engajamentos de red team autorizados, análise de caminho de ataque ou simulações de segurança ofensiva. Cobre planejamento de kill-chain com MITRE ATT&CK, pontuação de técnicas, identificação de pontos críticos, avaliação de risco OPSEC e identificação de alvos de alto valor.\"",
            "triggers": [
                "/security-pen-testing",
                "/attack-path-methodology",
                "/cloud-security",
                "/incidente-response",
                "/threat-detection",
                "/engagement"
            ],
            "dependencies": [
                "Threat Detection",
                "Cloud Security",
                "Security Pen Testing",
                "Incidente Response"
            ],
            "path": "engineering-team/red-team/SKILL.md"
        },
        {
            "id": "security-pen-testing",
            "category": "Engineering Team",
            "title": "Security Pen Testing",
            "description": "\"Use quando o usuário pedir para realizar auditorias de segurança, testes de penetração, varredura de vulnerabilidades, verificações OWASP Top 10 ou avaliações de segurança ofensiva. Cobre análise estática, varredura de dependências, detecção de segredos, testes de segurança de API e geração de relatórios de pen test.\"",
            "triggers": [
                "/owasp",
                "/pentest",
                "/api",
                "/passwd",
                "/6379",
                "/cwe",
                "/login",
                "/dependency-auditor",
                "/security-audit",
                "/21",
                "/data",
                "/vulnerability",
                "/senior-secops",
                "/89",
                "/decimal",
                "/trufflehog",
                "/branca",
                "/teste",
                "/etc",
                "/dependency",
                "/code-reviewer",
                "/pip",
                "/altos",
                "/23",
                "/definitions",
                "/go",
                "/img",
                "/sink",
                "/profundidade",
                "/bucket",
                "/27017",
                "/target",
                "/info",
                "/senior-security",
                "/batch",
                "/owasp-top-ten",
                "/hex",
                "/svg",
                "/engineering",
                "/attack",
                "/cinza",
                "/responsible"
            ],
            "dependencies": [
                "Senior Secops",
                "Code Reviewer",
                "Senior Security"
            ],
            "path": "engineering-team/security-pen-testing/SKILL.md"
        },
        {
            "id": "self-improving-agent",
            "category": "Engineering Team",
            "title": "Self Improving Agent",
            "description": "\"Curar a auto-memória do Claude Code em conhecimento duradouro de projeto. Analisa MEMORY.md em busca de padrões, promove aprendizados comprovados para CLAUDE.md e .claude/rules/, extrai soluções recorrentes em skills reutilizáveis. Use quando: (1) revisando o que o Claude aprendeu sobre seu projeto, (2) graduando um padrão de notas para regras aplicadas, (3) transformando uma solução de debugging em uma skill, (4) verificando saúde e capacidade da memória.\"",
            "triggers": [
                "/projects",
                "/memory",
                "/api",
                "/pskoett",
                "/api-testing",
                "/docs",
                "/clawhub",
                "/rules",
                "/en",
                "/si",
                "/playwright-pro",
                "/claude-skills",
                "/code",
                "/plugin",
                "/self-improving-agent"
            ],
            "dependencies": [],
            "path": "engineering-team/self-improving-agent/SKILL.md"
        },
        {
            "id": "senior-architect",
            "category": "Engineering Team",
            "title": "Senior Architect",
            "description": "\"Esta skill deve ser usada quando o usuário pedir para 'design system architecture', 'evaluate microsserviços vs monólito', 'create architecture diagrams', 'analyze dependências', 'choose a database', 'plan for escalabilidade', 'make technical decisions', or 'review system design'. Use para registros de decisão arquitetural (ADRs), avaliação de stack tecnológico, revisões de design de sistema, análise de dependências e geração de diagramas de arquitetura nos formatos Mermaid, PlantUML ou ASCII.\"",
            "triggers": [
                "/escrita",
                "/my-project",
                "/architecture",
                "/evolutivo",
                "/system",
                "/tech",
                "/yarn",
                "/project",
                "/dependency",
                "/100"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-architect/SKILL.md"
        },
        {
            "id": "senior-backend",
            "category": "Engineering Team",
            "title": "Senior Backend",
            "description": "\"Projeta e implementa sistemas backend incluindo REST APIs, microsserviços, arquiteturas de banco de dados, fluxos de autenticação e hardening de segurança. Use quando o usuário pedir para 'design REST APIs', 'optimize database queries', 'implement authentication', 'build microsserviços', 'review backend code', 'set up GraphQL', 'handle database migrations', ou 'load test APIs'. Cobre desenvolvimento Node.js/Express/Fastify, otimização PostgreSQL, segurança de API e padrões de arquitetura backend.\"",
            "triggers": [
                "/backend",
                "/api",
                "/login",
                "/routes",
                "/v1",
                "/v2",
                "/json",
                "/database",
                "/add",
                "/endpoint",
                "/20240115",
                "/sec",
                "/validators",
                "/middleware",
                "/components",
                "/schemas",
                "/users",
                "/orders",
                "/mydb",
                "/localhost"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-backend/SKILL.md"
        },
        {
            "id": "senior-computer-vision",
            "category": "Engineering Team",
            "title": "Senior Computer Vision",
            "description": "\"Skill de engenharia de visão computacional para detecção de objetos, segmentação de imagens e sistemas de IA visual. Cobre arquiteturas CNN e Vision Transformer, detecção YOLO/Faster R-CNN/DETR, segmentação Mask R-CNN/SAM e implantação em produção com ONNX/TensorRT. Inclui frameworks PyTorch, torchvision, Ultralytics, Detectron2 e MMDetection. Use quando construir pipelines de detecção, treinar modelos personalizados, otimizar inferência ou implantar sistemas de visão.\"",
            "triggers": [
                "/object",
                "/computer",
                "/cleaned",
                "/inference",
                "/dataset",
                "/weights",
                "/raw",
                "/images",
                "/detect",
                "/v11",
                "/vision",
                "/faster",
                "/best",
                "/calibration",
                "/final",
                "/augmentation",
                "/augmented",
                "/acur",
                "/coco",
                "/annotations",
                "/reference-docs-and-commands",
                "/train",
                "/production",
                "/labels"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-computer-vision/SKILL.md"
        },
        {
            "id": "senior-data-engineer",
            "category": "Engineering Team",
            "title": "Senior Data Engineer",
            "description": "\"Skill de engenharia de dados para construção de pipelines de dados escaláveis, sistemas ETL/ELT e infraestrutura de dados. Expertise em Python, SQL, Spark, Airflow, dbt, Kafka e o stack de dados moderno. Inclui modelagem de dados, orquestração de pipeline, qualidade de dados e DataOps. Use quando projetar arquiteturas de dados, construir pipelines de dados, otimizar fluxos de trabalho de dados, implementar governança de dados ou solucionar problemas de dados.\"",
            "triggers": [
                "/dataops",
                "/sales",
                "/stream",
                "/troubleshooting",
                "/daily",
                "/workflows",
                "/etl",
                "/data",
                "/pipeline"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-data-engineer/SKILL.md"
        },
        {
            "id": "senior-data-scientist",
            "category": "Engineering Team",
            "title": "Senior Data Scientist",
            "description": "\"Skill de cientista de dados sênior de nível mundial especializada em modelagem estatística, design de experimentos, inferência causal e analytics preditivo. Cobre teste A/B (dimensionamento de amostra, testes z de duas proporções, correção de Bonferroni), difference-in-differences, pipelines de feature engineering (Scikit-learn, XGBoost), avaliação de modelo com validação cruzada (AUC-ROC, AUC-PR, SHAP) e rastreamento de experimentos MLflow — usando Python (NumPy, Pandas, Scikit-learn), R e SQL. Use quando projetar ou analisar experimentos controlados, construir e avaliar modelos de classificação ou regressão, realizar análise causal em dados observacionais, fazer feature engineering para datasets tabulares estruturados ou traduzir achados estatísticos em decisões de negócio baseadas em dados.\"",
            "triggers": [
                "/health",
                "/treatment",
                "/train",
                "/charts",
                "/feature",
                "/evaluate",
                "/service",
                "/rolling",
                "/experiment",
                "/teste",
                "/statistical"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-data-scientist/SKILL.md"
        },
        {
            "id": "senior-devops",
            "category": "Engineering Team",
            "title": "Senior Devops",
            "description": "\"Skill DevOps abrangente para CI/CD, automação de infraestrutura, containerização e plataformas cloud (AWS, GCP, Azure). Inclui configuração de pipeline, infraestrutura como código, automação de implantação e monitoramento. Use quando configurar pipelines, implantar aplicações, gerenciar infraestrutura, implementar monitoramento ou otimizar processos de implantação.\"",
            "triggers": [
                "/ecs",
                "/codecov-action",
                "/app",
                "/workflows",
                "/healthz",
                "/ecs-service",
                "/infrastructure",
                "/v1",
                "/heads",
                "/setup-node",
                "/resid",
                "/infra",
                "/pipeline",
                "/green",
                "/app-blue",
                "/ci",
                "/deploy",
                "/cicd",
                "/deployment-blue",
                "/build-push-action",
                "/terraform",
                "/deployment",
                "/checkout",
                "/main",
                "/org"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-devops/SKILL.md"
        },
        {
            "id": "senior-frontend",
            "category": "Engineering Team",
            "title": "Senior Frontend",
            "description": "\"Skill de desenvolvimento frontend para aplicações React, Next.js, TypeScript e Tailwind CSS. Use quando construir componentes React, otimizar performance no Next.js, analisar tamanhos de bundle, criar scaffolding de projetos frontend, implementar acessibilidade ou revisar qualidade de código frontend.\"",
            "triggers": [
                "/hero",
                "/ui",
                "/div",
                "/api",
                "/button",
                "/lib",
                "/webp",
                "/100",
                "/avif",
                "/route",
                "/utils",
                "/react",
                "/nextjs",
                "/user-event",
                "/image",
                "/health",
                "/to",
                "/component",
                "/project",
                "/product",
                "/material",
                "/path",
                "/ul",
                "/components",
                "/frontend",
                "/users",
                "/h1",
                "/bundle"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-frontend/SKILL.md"
        },
        {
            "id": "senior-fullstack",
            "category": "Engineering Team",
            "title": "Senior Fullstack",
            "description": "\"Kit de desenvolvimento fullstack com scaffolding de projetos para stacks Next.js, FastAPI, MERN e Django, análise de qualidade de código com scoring de segurança e complexidade, e orientação na seleção de stack. Use quando o usuário pedir para 'criar scaffolding de um novo projeto', 'criar um app Next.js', 'configurar FastAPI com React', 'analisar qualidade de código', 'auditar minha base de código', 'qual stack devo usar', 'gerar boilerplate de projeto' ou mencionar desenvolvimento fullstack, configuração de projeto ou comparação de tech stack.\"",
            "triggers": [
                "/projects",
                "/path",
                "/tech",
                "/architecture",
                "/development",
                "/scripts",
                "/to",
                "/package",
                "/project",
                "/code",
                "/100"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-fullstack/SKILL.md"
        },
        {
            "id": "senior-ml-engineer",
            "category": "Engineering Team",
            "title": "Senior Ml Engineer",
            "description": "\"Skill de engenharia de ML para colocar modelos em produção, construir pipelines MLOps e integrar LLMs. Cobre implantação de modelos, feature stores, monitoramento de drift, sistemas RAG e otimização de custos. Use quando o usuário perguntar sobre implantar modelos de ML em produção, configurar infraestrutura MLOps (MLflow, Kubeflow, Kubernetes, Docker), monitorar performance ou drift de modelos, construir pipelines RAG ou integrar APIs de LLM com lógica de retry e controles de custo.\"",
            "triggers": [
                "/health",
                "/custo",
                "/mlops",
                "/mensal",
                "/rag",
                "/llm",
                "/model",
                "/user",
                "/app",
                "/ml",
                "/src",
                "/localhost"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-ml-engineer/SKILL.md"
        },
        {
            "id": "senior-mobile-android",
            "category": "Engineering Team",
            "title": "Senior Mobile Android",
            "description": "\"Engenheiro Android sênior especializado em Kotlin, Jetpack Compose, Coroutines, Flow, arquitetura (Clean Architecture, MVI/MVVM), Hilt DI, Room, Retrofit, testes (JUnit5, Turbine, Paparazzi), CI/CD (Gradle, GitHub Actions, Firebase App Distribution) e publicação na Play Store. Use ao desenvolver apps Android nativos, revisar código Kotlin, otimizar performance de UI, implementar Material Design 3, trabalhar com KMP, integrar SDKs ou quando o usuário mencionar Android, Kotlin, Jetpack Compose, Play Store ou Gradle.\"",
            "triggers": [
                "/ios",
                "/density",
                "/docker-development",
                "/android",
                "/engineering",
                "/senior-frontend",
                "/common",
                "/tdd-guide",
                "/src",
                "/ci-cd-pipeline-builder"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-mobile-android/SKILL.md"
        },
        {
            "id": "senior-mobile-ios",
            "category": "Engineering Team",
            "title": "Senior Mobile Ios",
            "description": "\"Engenheiro iOS sênior especializado em Swift 6, SwiftUI, UIKit, Combine, async/await, arquitetura modular (MVVM, TCA, Clean), testes (XCTest, Swift Testing), CI/CD (Fastlane, Xcode Cloud), distribuição (App Store Connect, TestFlight) e integração com HIG da Apple. Use ao desenvolver apps iOS nativos, revisar código Swift, otimizar performance de UI, implementar Live Activities/Widgets/App Clips, integrar SDKs, preparar submissão à App Store ou quando o usuário mencionar iOS, Swift, SwiftUI, UIKit, Xcode, App Store ou TestFlight.\"",
            "triggers": [
                "/xcshareddata",
                "/apple-hig-expert",
                "/await",
                "/product-team",
                "/engineering",
                "/xcschemes",
                "/senior-frontend",
                "/project",
                "/tdd-guide",
                "/ci-cd-pipeline-builder"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-mobile-ios/SKILL.md"
        },
        {
            "id": "senior-prompt-engineer",
            "category": "Engineering Team",
            "title": "Senior Prompt Engineer",
            "description": "\"Esta skill deve ser usada quando o usuário pedir para 'otimizar prompts', 'projetar templates de prompt', 'avaliar saídas de LLM', 'construir sistemas agênticos', 'implementar RAG', 'criar exemplos few-shot', 'analisar uso de tokens' ou 'projetar workflows de IA'. Use para padrões de prompt engineering, frameworks de avaliação de LLM, arquiteturas de agentes e design de saída estruturada.\"",
            "triggers": [
                "/respostas",
                "/persona",
                "/rag",
                "/agentic",
                "/prompt",
                "/llm",
                "/agent",
                "/my",
                "/estruturadas",
                "/execu",
                "/sa",
                "/100"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-prompt-engineer/SKILL.md"
        },
        {
            "id": "senior-qa",
            "category": "Engineering Team",
            "title": "Senior Qa",
            "description": "\"Gera testes unitários, testes de integração e testes E2E para aplicações React/Next.js. Escaneia componentes para criar stubs de testes Jest + React Testing Library, analisa relatórios de cobertura Istanbul/LCOV para identificar lacunas, cria scaffolding de arquivos de teste Playwright a partir de rotas Next.js, mocka chamadas de API com MSW, cria fixtures de teste e configura test runners. Use quando o usuário pedir para 'gerar testes', 'escrever testes unitários', 'analisar cobertura de testes', 'criar scaffolding de testes E2E', 'configurar Playwright', 'configurar Jest', 'implementar padrões de teste' ou 'melhorar qualidade de testes'.\"",
            "triggers": [
                "/carregado",
                "/api",
                "/dashboard",
                "/auth",
                "/testing",
                "/buscar",
                "/qa",
                "/login",
                "/app",
                "/coverage",
                "/workflows",
                "/test",
                "/fixtures",
                "/diret",
                "/coverage-final",
                "/node",
                "/react",
                "/carregando",
                "/clique",
                "/e2e",
                "/enviar",
                "/email",
                "/components",
                "/checkout",
                "/users",
                "/upload-artifact",
                "/src"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-qa/SKILL.md"
        },
        {
            "id": "senior-secops",
            "category": "Engineering Team",
            "title": "Senior Secops",
            "description": "\"Skill de engenheiro SecOps sênior para segurança de aplicações, gerenciamento de vulnerabilidades, verificação de conformidade e práticas de desenvolvimento seguro. Executa scans SAST/DAST, gera planos de remediação de CVEs, verifica vulnerabilidades de dependências, cria políticas de segurança, impõe padrões de codificação segura e automatiza verificações de conformidade contra SOC2, PCI-DSS, LGPD/ANVISA e LGPD. Use ao conduzir uma revisão ou auditoria de segurança, responder a um CVE ou incidente de segurança, fortalecer infraestrutura, implementar autenticação ou gerenciamento de segredos, preparar para testes de penetração, verificar exposição ao OWASP Top 10 ou impor controles de segurança em pipelines CI/CD.\"",
            "triggers": [
                "/20",
                "/workflows",
                "/app",
                "/gitleaks-action",
                "/vulnerability",
                "/alto",
                "/32",
                "/github",
                "/security",
                "/altas",
                "/11",
                "/detect-secrets",
                "/setup-python",
                "/altos",
                "/testes",
                "/token",
                "/reprovado",
                "/backdoors",
                "/to",
                "/entidade",
                "/project",
                "/cosign",
                "/compliance",
                "/path",
                "/key",
                "/checkout",
                "/argon2",
                "/org"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-secops/SKILL.md"
        },
        {
            "id": "senior-security",
            "category": "Engineering Team",
            "title": "Senior Security",
            "description": "\"Kit de engenharia de segurança para modelagem de ameaças, análise de vulnerabilidades, arquitetura segura e testes de penetração. Inclui análise STRIDE, orientação OWASP, padrões de criptografia e ferramentas de escaneamento de segurança. Use quando o usuário perguntar sobre revisões de segurança, análise de ameaças, avaliações de vulnerabilidades, práticas de codificação segura, auditorias de segurança, análise de superfície de ataque, remediação de CVE ou melhores práticas de segurança.\"",
            "triggers": [
                "/owasp",
                "/senior-backend",
                "/threat-modeling-guide",
                "/security-architecture-patterns",
                "/bcrypt",
                "/senior-secops",
                "/backdoors",
                "/secret",
                "/tr",
                "/senior-devops",
                "/cryptography-implementation",
                "/contas",
                "/senior-architect",
                "/exfiltra",
                "/authz",
                "/threat"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-security/SKILL.md"
        },
        {
            "id": "senior-sre",
            "category": "Engineering Team",
            "title": "Senior Sre",
            "description": "\"Site Reliability Engineer sênior especializado em SLI/SLO/SLA, error budgets, observabilidade, postmortems sem culpa, capacity planning, chaos engineering, incident management e toil reduction. Use ao definir SLOs, estruturar on-call, responder a incidentes, conduzir postmortems, projetar sistemas resilientes, reduzir toil operacional, implementar SRE practices ou quando o usuário mencionar SRE, SLO, error budget, postmortem, on-call, chaos engineering ou toil.\"",
            "triggers": [
                "/memory",
                "/offboarding",
                "/p95",
                "/semana",
                "/incident-response",
                "/checkout-api-errors",
                "/docs",
                "/incident-commander",
                "/runbooks",
                "/engineering",
                "/observability-designer",
                "/person",
                "/senior-devops",
                "/p99",
                "/week",
                "/ci-cd-pipeline-builder",
                "/dia"
            ],
            "dependencies": [],
            "path": "engineering-team/senior-sre/SKILL.md"
        },
        {
            "id": "snowflake-development",
            "category": "Engineering Team",
            "title": "Snowflake Development",
            "description": "\"Use quando escrever SQL Snowflake, construir pipelines de dados com Dynamic Tables ou Streams/Tasks, usar funções Cortex AI, criar Cortex Agents, escrever Snowpark Python, configurar dbt para Snowflake ou solucionar problemas de erros Snowflake.\"",
            "triggers": [
                "/github",
                "/snowflake",
                "/imagens",
                "/documentos",
                "/sql-database-assistant",
                "/troubleshooting",
                "/schema",
                "/database-designer",
                "/senior-data-engineer",
                "/cortex",
                "/senior-data-scientist",
                "/senior-devops",
                "/jamescha-earley",
                "/quase",
                "/file"
            ],
            "dependencies": [],
            "path": "engineering-team/snowflake-development/SKILL.md"
        },
        {
            "id": "stripe-integration-expert",
            "category": "Engineering Team",
            "title": "Stripe Integration Expert",
            "description": "\"Especialista em Integração Stripe para implementar integrações Stripe em nível de produção: assinaturas com trials e proration, pagamentos únicos, billing baseado em uso, checkout sessions, handlers de webhook idempotentes, portal do cliente e faturamento. Cobre padrões Next.js, Express e Django.\"",
            "triggers": [
                "/stripe-cli",
                "/api",
                "/downgrades",
                "/checkout",
                "/stripe",
                "/route",
                "/auth",
                "/db",
                "/dashboard",
                "/server",
                "/billing",
                "/webhooks",
                "/subscription",
                "/headers",
                "/lib",
                "/pricing",
                "/settings",
                "/portal"
            ],
            "dependencies": [],
            "path": "engineering-team/stripe-integration-expert/SKILL.md"
        },
        {
            "id": "tdd-guide",
            "category": "Engineering Team",
            "title": "Tdd Guide",
            "description": "\"Skill de desenvolvimento orientado a testes para escrever testes unitários, gerar fixtures e mocks de teste, analisar lacunas de cobertura e guiar workflows red-green-refactor em Jest, Pytest, JUnit, Vitest e Mocha. Use quando o usuário pedir para escrever testes, melhorar cobertura de testes, praticar TDD, gerar mocks ou stubs, ou mencionar frameworks de teste como Jest, pytest ou JUnit.\"",
            "triggers": [
                "/decode",
                "/service",
                "/user-auth",
                "/login",
                "/focused-fix",
                "/coverage",
                "/framework",
                "/tdd",
                "/test",
                "/decodifica",
                "/cart",
                "/requisitos",
                "/senior-qa",
                "/desktop",
                "/sa",
                "/code-reviewer",
                "/senior-fullstack",
                "/spec-driven-workflow",
                "/fixture",
                "/formatting",
                "/desserializa",
                "/conftest",
                "/process",
                "/codec"
            ],
            "dependencies": [],
            "path": "engineering-team/tdd-guide/SKILL.md"
        },
        {
            "id": "tech-stack-evaluator",
            "category": "Engineering Team",
            "title": "Tech Stack Evaluator",
            "description": "\"Avaliação e comparação de stacks tecnológicos com análise TCO, avaliação de segurança e pontuação de saúde do ecossistema. Use ao comparar frameworks, avaliar stacks de tecnologia, calcular custo total de propriedade, avaliar caminhos de migração ou analisar viabilidade de ecossistema.\"",
            "triggers": [
                "/examples",
                "/ano",
                "/backend",
                "/tco",
                "/sample",
                "/metrics",
                "/ecosystem",
                "/stack",
                "/security",
                "/workflows",
                "/sa",
                "/migration"
            ],
            "dependencies": [],
            "path": "engineering-team/tech-stack-evaluator/SKILL.md"
        },
        {
            "id": "threat-detection",
            "category": "Engineering Team",
            "title": "Threat Detection",
            "description": "\"Use ao caçar ameaças em um ambiente, analisar IOCs ou detectar anomalias comportamentais em telemetria. Cobre threat hunting orientado a hipóteses, geração de varredura de IOC, detecção de anomalias por z-score e priorização de sinais mapeados ao MITRE ATT&CK.\"",
            "triggers": [
                "/var",
                "/red-team",
                "/cloud-security",
                "/incident-response",
                "/log",
                "/telemetry",
                "/events",
                "/security-pen-testing",
                "/hunt-playbooks",
                "/threat",
                "/11",
                "/threat-detection"
            ],
            "dependencies": [
                "Security Pen Testing",
                "Red Team",
                "Incident Response",
                "Cloud Security"
            ],
            "path": "engineering-team/threat-detection/SKILL.md"
        }
    ],
    "Finance": [
        {
            "id": "business-investment-advisor",
            "category": "Finance",
            "title": "Business Investment Advisor",
            "description": "\"Consultor de análise de investimentos empresariais e alocação de capital. Use ao avaliar se deve investir em equipamentos, imóveis, um novo negócio, contratação, tecnologia ou qualquer despesa de capital. Também use para cálculos de ROI, TIR, VPL, período de payback, decisões de construir vs comprar, análise de leasing vs compra, avaliação de fornecedores ou para decidir onde alocar orçamento limitado para máximo retorno.\"",
            "triggers": [
                "/ano",
                "/github",
                "/incerto",
                "/contrato",
                "/anos",
                "/chad848",
                "/comprovado",
                "/30",
                "/baixa"
            ],
            "dependencies": [],
            "path": "finance/business-investment-advisor/SKILL.md"
        },
        {
            "id": "controller-contador",
            "category": "Finance",
            "title": "Controller Contador",
            "description": "\"Controller / Contador sênior para contabilidade empresarial brasileira, rotinas fiscais (NF-e, NFS-e, SPED ICMS/Fiscal/Contribuições), fechamento mensal, conciliações, demonstrações financeiras (BP, DRE, DFC), regimes tributários (Simples, Presumido, Real) e controle interno. Use ao estruturar área contábil, preparar fechamento, conciliar contas, apurar impostos, responder auditoria ou quando o usuário mencionar controller, contador, contabilidade, NF-e, SPED, DRE, balanço patrimonial, Simples Nacional, Lucro Presumido ou Lucro Real.\"",
            "triggers": [
                "/ano",
                "/servi",
                "/sa",
                "/cfo-advisor",
                "/despesas",
                "/receber",
                "/03",
                "/mercadorias",
                "/c-level-advisor"
            ],
            "dependencies": [],
            "path": "finance/controller-contador/SKILL.md"
        },
        {
            "id": "financial-analyst",
            "category": "Finance",
            "title": "Financial Analyst",
            "description": "Realiza análise de índices financeiros, avaliação DCF, análise de variação orçamentária e construção de previsões contínuas para tomada de decisões estratégicas. Use ao analisar demonstrações financeiras, construir modelos de avaliação, avaliar variações orçamentárias, ou construir projeções financeiras e previsões. Também aplicável quando os usuários mencionarem modelagem financeira, análise de fluxo de caixa, avaliação de empresa, projeções financeiras, or análise de planilhas.",
            "triggers": [
                "/-3",
                "/dcf",
                "/-5",
                "/sample",
                "/budget",
                "/forecast",
                "/valuation-methodology",
                "/forecasting-best-practices",
                "/despesa",
                "/ratio",
                "/financial-ratios-guide",
                "/pessimista",
                "/desfavor",
                "/industry-adaptations",
                "/variance",
                "/otimista"
            ],
            "dependencies": [],
            "path": "finance/financial-analyst/SKILL.md"
        },
        {
            "id": "fpa-analyst",
            "category": "Finance",
            "title": "Fpa Analyst",
            "description": "\"Analista de FP&A (Financial Planning & Analysis) sênior para orçamento anual, forecast contínuo, análise de variação, unit economics, modelagem financeira 3 statements, business partnering e apresentação ao conselho. Use ao montar budget, fazer rolling forecast, analisar variações, modelar cenários, calcular unit economics ou quando o usuário mencionar FP&A, planejamento financeiro, budget, forecast, variance analysis, unit economics, 3 statements ou board deck financeiro.\"",
            "triggers": [
                "/c-level-advisor",
                "/cfo-advisor",
                "/board"
            ],
            "dependencies": [],
            "path": "finance/fpa-analyst/SKILL.md"
        },
        {
            "id": "saas-metrics-coach",
            "category": "Finance",
            "title": "Saas Metrics Coach",
            "description": "Consultor de saúde financeira SaaS. Use quando o usuário compartilhar números de receita ou clientes, ou mencionar ARR, MRR, churn, LTV, CAC, NRR, ou perguntar como seu negócio SaaS está indo.",
            "triggers": [
                "/base",
                "/metrics",
                "/formulas",
                "/customer-success",
                "/quick",
                "/pior",
                "/churn",
                "/cancelamento",
                "/unit",
                "/input-template",
                "/benchmarks"
            ],
            "dependencies": [],
            "path": "finance/saas-metrics-coach/SKILL.md"
        }
    ],
    "Financeiro Compliance": [
        {
            "id": "cobranca",
            "category": "Financeiro Compliance",
            "title": "Cobranca",
            "description": "|",
            "triggers": [
                "/read",
                "/cobranca",
                "/90",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/cobranca/SKILL.md"
        },
        {
            "id": "conformidade-lgpd",
            "category": "Financeiro Compliance",
            "title": "Conformidade Lgpd",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/2018",
                "/skill",
                "/app",
                "/lgpd-compliance"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/conformidade-lgpd/SKILL.md"
        },
        {
            "id": "contratos-br",
            "category": "Financeiro Compliance",
            "title": "Contratos Br",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/contratos-br",
                "/skill",
                "/contratos"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/contratos-br/SKILL.md"
        },
        {
            "id": "dre-balanco",
            "category": "Financeiro Compliance",
            "title": "Dre Balanco",
            "description": "|",
            "triggers": [
                "/read",
                "/dre-balanco",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/dre-balanco/SKILL.md"
        },
        {
            "id": "due-diligence",
            "category": "Financeiro Compliance",
            "title": "Due Diligence",
            "description": "|",
            "triggers": [
                "/fornecedores",
                "/ano",
                "/read",
                "/rules",
                "/skill",
                "/due-diligence"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/due-diligence/SKILL.md"
        },
        {
            "id": "fluxo-caixa",
            "category": "Financeiro Compliance",
            "title": "Fluxo Caixa",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/realista",
                "/pessimista",
                "/fluxo-caixa",
                "/skill"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/fluxo-caixa/SKILL.md"
        },
        {
            "id": "gestao-riscos",
            "category": "Financeiro Compliance",
            "title": "Gestao Riscos",
            "description": "|",
            "triggers": [
                "/gestao-riscos",
                "/read",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/gestao-riscos/SKILL.md"
        },
        {
            "id": "impostos-br",
            "category": "Financeiro Compliance",
            "title": "Impostos Br",
            "description": "|",
            "triggers": [
                "/ano",
                "/read",
                "/faturamento",
                "/impostos-br",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/impostos-br/SKILL.md"
        },
        {
            "id": "kpis-financeiros",
            "category": "Financeiro Compliance",
            "title": "Kpis Financeiros",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/kpis-financeiros",
                "/skill"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/kpis-financeiros/SKILL.md"
        },
        {
            "id": "open-finance-pix",
            "category": "Financeiro Compliance",
            "title": "Open Finance Pix",
            "description": "|",
            "triggers": [
                "/read",
                "/open-finance-pix",
                "/rules",
                "/2020",
                "/skill"
            ],
            "dependencies": [],
            "path": "financeiro-compliance/open-finance-pix/SKILL.md"
        }
    ],
    "Juridico Advocacia": [
        {
            "id": "captacao-clientes",
            "category": "Juridico Advocacia",
            "title": "Captacao Clientes",
            "description": "\"Estratégias de captação de clientes para advogados respeitando o Código de Ética da OAB\"",
            "triggers": [
                "/2021"
            ],
            "dependencies": [],
            "path": "juridico-advocacia/captacao-clientes/SKILL.md"
        },
        {
            "id": "consumidor",
            "category": "Juridico Advocacia",
            "title": "Consumidor",
            "description": "\"Direito do consumidor: CDC, Procon, Reclame Aqui e mediação de conflitos\"",
            "triggers": [],
            "dependencies": [],
            "path": "juridico-advocacia/consumidor/SKILL.md"
        },
        {
            "id": "contrato-servicos",
            "category": "Juridico Advocacia",
            "title": "Contrato Servicos",
            "description": "\"Contratos de prestação de serviços conforme Código Civil e CDC brasileiro\"",
            "triggers": [
                "/2002"
            ],
            "dependencies": [],
            "path": "juridico-advocacia/contrato-servicos/SKILL.md"
        },
        {
            "id": "empresarial",
            "category": "Juridico Advocacia",
            "title": "Empresarial",
            "description": "\"Constituição de empresa, alterações societárias e regime tributário no Brasil\"",
            "triggers": [],
            "dependencies": [],
            "path": "juridico-advocacia/empresarial/SKILL.md"
        },
        {
            "id": "honorarios",
            "category": "Juridico Advocacia",
            "title": "Honorarios",
            "description": "\"Tabela de honorários e precificação de serviços jurídicos no mercado brasileiro\"",
            "triggers": [
                "/2015"
            ],
            "dependencies": [],
            "path": "juridico-advocacia/honorarios/SKILL.md"
        },
        {
            "id": "lgpd-juridico",
            "category": "Juridico Advocacia",
            "title": "Lgpd Juridico",
            "description": "\"Adequação LGPD para escritórios de advocacia: contratos, políticas, DPA e procedimentos\"",
            "triggers": [
                "/2018"
            ],
            "dependencies": [],
            "path": "juridico-advocacia/lgpd-juridico/SKILL.md"
        },
        {
            "id": "marketing-juridico",
            "category": "Juridico Advocacia",
            "title": "Marketing Juridico",
            "description": "\"Marketing jurídico permitido pela OAB: LinkedIn, Instagram, WhatsApp e conteúdo educativo\"",
            "triggers": [],
            "dependencies": [],
            "path": "juridico-advocacia/marketing-juridico/SKILL.md"
        },
        {
            "id": "peticao-inicial",
            "category": "Juridico Advocacia",
            "title": "Peticao Inicial",
            "description": "\"Estruturação de petições iniciais, contestações e recursos conforme CPC/2015 e legislação brasileira\"",
            "triggers": [
                "/2015"
            ],
            "dependencies": [],
            "path": "juridico-advocacia/peticao-inicial/SKILL.md"
        },
        {
            "id": "rotina-escritorio",
            "category": "Juridico Advocacia",
            "title": "Rotina Escritorio",
            "description": "\"SOP e processos para advocacia solo e boutique: prazos, agenda e gestão de clientes\"",
            "triggers": [],
            "dependencies": [],
            "path": "juridico-advocacia/rotina-escritorio/SKILL.md"
        },
        {
            "id": "trabalhista",
            "category": "Juridico Advocacia",
            "title": "Trabalhista",
            "description": "\"Direito trabalhista brasileiro: CLT, Reforma Trabalhista, TST, dissídio e acordos\"",
            "triggers": [
                "/acordo",
                "/2017"
            ],
            "dependencies": [],
            "path": "juridico-advocacia/trabalhista/SKILL.md"
        }
    ],
    "Lideranca Equipes": [
        {
            "id": "cultura-psicologica",
            "category": "Lideranca Equipes",
            "title": "Cultura Psicologica",
            "description": "\"Segurança psicológica, diversidade e inclusão em equipes brasileiras\"",
            "triggers": [],
            "dependencies": [],
            "path": "lideranca-equipes/cultura-psicologica/SKILL.md"
        },
        {
            "id": "desenvolvimento-time",
            "category": "Lideranca Equipes",
            "title": "Desenvolvimento Time",
            "description": "\"PDIs, trilhas de desenvolvimento e planos de carreira para equipes brasileiras\"",
            "triggers": [],
            "dependencies": [],
            "path": "lideranca-equipes/desenvolvimento-time/SKILL.md"
        },
        {
            "id": "feedback-estruturado",
            "category": "Lideranca Equipes",
            "title": "Feedback Estruturado",
            "description": "\"Feedback 1:1 com SBI, feedforward e frameworks de desenvolvimento para líderes\"",
            "triggers": [],
            "dependencies": [],
            "path": "lideranca-equipes/feedback-estruturado/SKILL.md"
        },
        {
            "id": "gestao-conflitos",
            "category": "Lideranca Equipes",
            "title": "Gestao Conflitos",
            "description": "\"Resolução de conflitos e mediação em times no contexto de startups e PMEs brasileiras\"",
            "triggers": [],
            "dependencies": [],
            "path": "lideranca-equipes/gestao-conflitos/SKILL.md"
        },
        {
            "id": "lider-tecnico",
            "category": "Lideranca Equipes",
            "title": "Lider Tecnico",
            "description": "\"Transição de especialista para líder técnico ou engineering manager em startups\"",
            "triggers": [
                "/analista",
                "/designer"
            ],
            "dependencies": [],
            "path": "lideranca-equipes/lider-tecnico/SKILL.md"
        },
        {
            "id": "reconhecimento",
            "category": "Lideranca Equipes",
            "title": "Reconhecimento",
            "description": "\"Programas de reconhecimento e engajamento de colaboradores em startups e PMEs\"",
            "triggers": [],
            "dependencies": [],
            "path": "lideranca-equipes/reconhecimento/SKILL.md"
        },
        {
            "id": "remoto-hibrido",
            "category": "Lideranca Equipes",
            "title": "Remoto Hibrido",
            "description": "\"Gestão de times remotos e híbridos: rituais, ferramentas e cultura no Brasil\"",
            "triggers": [
                "/2022"
            ],
            "dependencies": [],
            "path": "lideranca-equipes/remoto-hibrido/SKILL.md"
        },
        {
            "id": "reuniao-eficaz",
            "category": "Lideranca Equipes",
            "title": "Reuniao Eficaz",
            "description": "\"Facilitação de reuniões produtivas: pré, durante e pós para times brasileiros\"",
            "triggers": [],
            "dependencies": [],
            "path": "lideranca-equipes/reuniao-eficaz/SKILL.md"
        },
        {
            "id": "reuniao-individual",
            "category": "Lideranca Equipes",
            "title": "Reuniao Individual",
            "description": "\"Preparação e condução de reuniões 1:1 eficazes para desenvolvimento de pessoas\"",
            "triggers": [
                "/45min",
                "/30min"
            ],
            "dependencies": [],
            "path": "lideranca-equipes/reuniao-individual/SKILL.md"
        },
        {
            "id": "time-pequeno",
            "category": "Lideranca Equipes",
            "title": "Time Pequeno",
            "description": "\"Gestão de times de 2-15 pessoas em startups e PMEs brasileiras\"",
            "triggers": [],
            "dependencies": [],
            "path": "lideranca-equipes/time-pequeno/SKILL.md"
        }
    ],
    "Marketing Skill": [
        {
            "id": "ab-test-setup",
            "category": "Marketing Skill",
            "title": "Ab Test Setup",
            "description": "Quando o usuário quiser planejar, projetar ou implementar um teste A/B ou experimento. Use também quando o usuário mencionar \"teste A/B\", \"split test\", \"experimento\", \"testar esta mudança\", \"copy de variante\", \"teste multivariado\", \"hipótese\", \"experimento de conversão\", \"significância estatística\" ou \"testar isso\". Para implementação de rastreamento, veja analytics-tracking.",
            "triggers": [
                "/ab-testing",
                "/dado",
                "/semana",
                "/20",
                "/sample-size",
                "/10",
                "/test-templates",
                "/sample-size-guide",
                "/variante",
                "/product-marketing-context",
                "/como",
                "/50",
                "/www",
                "/sample-size-calculator"
            ],
            "dependencies": [],
            "path": "marketing-skill/ab-test-setup/SKILL.md"
        },
        {
            "id": "ad-creative",
            "category": "Marketing Skill",
            "title": "Ad Creative",
            "description": "\"Quando o usuário precisa gerar, iterar ou escalar criativos de anúncios para publicidade paga. Use quando disserem 'escrever copy de anúncio', 'gerar títulos', 'criar variações de anúncios', 'criativo em massa', 'iterar sobre anúncios', 'validação de copy de anúncio', 'headlines RSA', 'copy de anúncio Meta Ads', 'anúncio LinkedIn' ou 'teste criativo'. Esta é produção criativa pura — distinta de paid-ads (estratégia de campanha). Use ad-creative quando precisar do copy, não do plano de campanha.\"",
            "triggers": [
                "/creative-frameworks",
                "/ad",
                "/empresas",
                "/platform-specs",
                "/plataformas",
                "/depois"
            ],
            "dependencies": [],
            "path": "marketing-skill/ad-creative/SKILL.md"
        },
        {
            "id": "ai-seo",
            "category": "Marketing Skill",
            "title": "Ai Seo",
            "description": "\"Otimize conteúdo para ser citado por mecanismos de busca com IA — ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini, Copilot. Use quando quiser que seu conteúdo apareça em respostas geradas por IA, não apenas ranqueado em links azuis. Gatilhos: 'otimizar para busca IA', 'ser citado pelo ChatGPT', 'AI Overviews', 'citações Perplexity', 'AI SEO', 'busca generativa', 'visibilidade em LLM', 'GEO' (otimização para motores generativos). NÃO para SEO tradicional (use seo-audit). NÃO para criação de conteúdo (use content-production).\"",
            "triggers": [
                "/semana",
                "/monitoramento-guide",
                "/robots",
                "/contras",
                "/ai-search-landscape",
                "/validator",
                "/content-patterns"
            ],
            "dependencies": [],
            "path": "marketing-skill/ai-seo/SKILL.md"
        },
        {
            "id": "analytics-tracking",
            "category": "Marketing Skill",
            "title": "Analytics Tracking",
            "description": "\"Configure, audite e depure a implementação de rastreamento de analytics — GA4, Google Tag Manager, taxonomia de eventos, rastreamento de conversão e qualidade de dados. Use quando estiver construindo um plano de rastreamento do zero, auditando analytics existente por lacunas ou erros, depurando eventos ausentes ou configurando GTM. Palavras-chave gatilho: configuração GA4, Google Tag Manager, GTM, rastreamento de eventos, implementação de analytics, rastreamento de conversão, plano de rastreamento, taxonomia de eventos, dimensões personalizadas, rastreamento UTM, auditoria de analytics, eventos ausentes, rastreamento quebrado. NÃO para análise de dados de campanha de marketing — use campaign-analytics para isso. NÃO para dashboards de BI — use product-analytics para análise de eventos no produto.\"",
            "triggers": [
                "/event-taxonomy-guide",
                "/vari",
                "/fluxos",
                "/trigger",
                "/criativo",
                "/tracking",
                "/app",
                "/valor",
                "/presente",
                "/ou",
                "/pricing",
                "/medium",
                "/gtm-patterns"
            ],
            "dependencies": [],
            "path": "marketing-skill/analytics-tracking/SKILL.md"
        },
        {
            "id": "app-store-optimization",
            "category": "Marketing Skill",
            "title": "App Store Optimization",
            "description": "Kit de ASO (App Store Optimization) para pesquisar palavras-chave, analisar rankings de concorrentes, gerar sugestões de metadados e melhorar a visibilidade do app na Apple App Store e Google Play Store. Use quando o usuário perguntar sobre ASO, rankings na app store, metadados do app, títulos e descrições de apps, listagens na app store, visibilidade do app, ou marketing de apps mobile no iOS ou Android. Suporta pesquisa e pontuação de palavras-chave, análise de palavras-chave de concorrentes, otimização de metadados, planejamento de testes A/B, checklists de lançamento e rastreamento de mudanças de ranking.",
            "triggers": [
                "/descri",
                "/aso-audit-template",
                "/aso-best-practices",
                "/aso",
                "/palavra-chave-research-guide",
                "/ab",
                "/competitor",
                "/estilo",
                "/content-creator",
                "/internos",
                "/review",
                "/platform-requirements",
                "/palavra-chave",
                "/metadata",
                "/localization",
                "/marketing-strategy-pmm",
                "/marketing-demand-acquisition",
                "/launch",
                "/aumentar"
            ],
            "dependencies": [],
            "path": "marketing-skill/app-store-optimization/SKILL.md"
        },
        {
            "id": "brand-guidelines",
            "category": "Marketing Skill",
            "title": "Brand Guidelines",
            "description": "\"Quando o usuário quiser aplicar, documentar ou reforçar diretrizes de marca para qualquer produto ou empresa. Use também quando o usuário mencionar 'diretrizes de marca', 'cores da marca', 'tipografia', 'uso do logo', 'voz da marca', 'identidade visual', 'tom de voz', 'padrões de marca', 'guia de estilo', 'consistência da marca' ou 'padrões de design da empresa'. Cobre sistemas de cores, tipografia, regras de logo, diretrizes de imagens e matriz de tom para qualquer marca.\"",
            "triggers": [
                "/product-marketing-context",
                "/brand-identity-and-framework"
            ],
            "dependencies": [],
            "path": "marketing-skill/brand-guidelines/SKILL.md"
        },
        {
            "id": "campaign-analytics",
            "category": "Marketing Skill",
            "title": "Campaign Analytics",
            "description": "Analisa a performance de campanhas com atribuição multi-touch, análise de conversão do funil e cálculo de ROI para otimização de marketing. Use ao analisar campanhas de marketing, performance de anúncios, modelos de atribuição, taxas de conversão ou ao calcular ROI, ROAS, CPA e métricas de campanha entre canais.",
            "triggers": [
                "/funnel",
                "/campaign",
                "/sample",
                "/attribution-models-guide",
                "/20",
                "/meio",
                "/campaign-metricas-benchmarks",
                "/contras",
                "/funil-optimization-framework",
                "/40",
                "/attribution",
                "/fim"
            ],
            "dependencies": [],
            "path": "marketing-skill/campaign-analytics/SKILL.md"
        },
        {
            "id": "churn-prevention",
            "category": "Marketing Skill",
            "title": "Churn Prevention",
            "description": "\"Reduza o churn voluntário e involuntário por meio do design do fluxo de cancelamento, ofertas de retenção, pesquisas de saída e sequências de dunning. Use ao projetar ou otimizar um fluxo de cancelamento, construir ofertas de retenção, configurar emails de dunning ou reduzir o churn por falha de pagamento. Palavras-chave gatilho: fluxo de cancelamento, redução de churn, ofertas de retenção, dunning, pesquisa de saída, recuperação de pagamento, win-back, churn involuntário, pagamentos com falha, página de cancelamento. NÃO para pontuação de saúde do cliente ou receita de expansão — use customer-success-manager para isso.\"",
            "triggers": [
                "/cancelada",
                "/via",
                "/cancel-flow-playbook",
                "/anual",
                "/churn",
                "/substitu",
                "/dunning-guide"
            ],
            "dependencies": [],
            "path": "marketing-skill/churn-prevention/SKILL.md"
        },
        {
            "id": "cold-email",
            "category": "Marketing Skill",
            "title": "Cold Email",
            "description": "\"Quando o usuário quiser escrever, melhorar ou construir uma sequência de emails de prospecção B2B a frio para prospects que não solicitaram contato. Use quando o usuário mencionar 'cold email', 'prospecção a frio', 'emails de prospecção', 'emails de SDR', 'emails de vendas', 'email de primeiro contato', 'sequência de acompanhamento' ou 'prospecção por email'. Use também quando compartilharem um rascunho de email que soa muito comercial e precisa ser humanizado. Distinto de email-sequence (lifecycle/nutrição para assinantes que optaram em) — este é contato não solicitado para novos prospects. NÃO para emails de lifecycle, newsletters ou campanhas de drip (use email-sequence).\"",
            "triggers": [
                "/nutri",
                "/deliverability-guide",
                "/acompanhamento-playbook",
                "/corpo",
                "/frameworks",
                "/dia"
            ],
            "dependencies": [],
            "path": "marketing-skill/cold-email/SKILL.md"
        },
        {
            "id": "competitor-alternatives",
            "category": "Marketing Skill",
            "title": "Competitor Alternatives",
            "description": "\"Quando o usuário quiser criar páginas de comparação ou alternativas a concorrentes para SEO e capacitação de vendas. Use também quando o usuário mencionar 'página de alternativa', 'página vs', 'comparação de concorrentes', 'página de comparação', '[Produto] vs [Produto]', 'alternativa ao [Produto]', 'landing pages competitivas', 'migrar do concorrente' ou 'conteúdo de comparação'. Cobre quatro formatos: alternativa singular, alternativas no plural, você vs concorrente e concorrente vs concorrente. Enfatiza pesquisa aprofundada, arquitetura de conteúdo modular e tipos de seção variados além de tabelas de funcionalidades.\"",
            "triggers": [
                "/limita",
                "/adjacentes",
                "/alternativas",
                "/comparar",
                "/templates",
                "/product-marketing-context",
                "/alternativa-ao-",
                "/alternativas-ao-",
                "/content-architecture",
                "/reclama",
                "/vs"
            ],
            "dependencies": [],
            "path": "marketing-skill/competitor-alternatives/SKILL.md"
        },
        {
            "id": "content-creator",
            "category": "Marketing Skill",
            "title": "Content Creator",
            "description": "\"Skill de redirecionamento depreciada que direciona solicitações legadas de 'content creator' para a skill especialista correta. Use quando o usuário invocar 'content creator', pedir para escrever um post de blog, artigo, guia ou análise de voz da marca (direcionar para content-production), ou pedir para planejar conteúdo, construir um cluster de tópicos ou criar um calendário editorial (direcionar para content-strategy). Não trata solicitações diretamente — identifica a intenção do usuário e redireciona para content-production (tarefas de redação/SEO/voz da marca) ou content-strategy (tarefas de planejamento).\"",
            "triggers": [
                "/content-strategy",
                "/social-content",
                "/voz",
                "/content-production"
            ],
            "dependencies": [],
            "path": "marketing-skill/content-creator/SKILL.md"
        },
        {
            "id": "content-humanizer",
            "category": "Marketing Skill",
            "title": "Content Humanizer",
            "description": "\"Faz com que conteúdo gerado por IA soe genuinamente humano — não apenas limpo, mas vivo. Use quando o conteúdo parecer robótico, usar muitos clichês de IA, faltar personalidade ou soar como foi escrito por comitê. Gatilhos: 'isso soa como IA', 'torne mais humano', 'adicione personalidade', 'parece genérico', 'soa robótico', 'corrija escrita de IA', 'injete nossa voz'. NÃO para criação inicial de conteúdo (use content-production). NÃO para otimização de SEO (use content-production Modo 3).\"",
            "triggers": [
                "/seg",
                "/depois",
                "/humanizer",
                "/ai-tells-lista",
                "/casual",
                "/irreverente",
                "/voice-techniques"
            ],
            "dependencies": [],
            "path": "marketing-skill/content-humanizer/SKILL.md"
        },
        {
            "id": "content-production",
            "category": "Marketing Skill",
            "title": "Content Production",
            "description": "\"Pipeline completo de produção de conteúdo — leva um tópico da página em branco até a peça pronta para publicação. Use quando precisar executar conteúdo: escrever um post de blog, artigo ou guia do começo ao fim. Gatilhos: 'escrever um post sobre', 'rascunhar um artigo', 'criar conteúdo para', 'me ajude a escrever', 'preciso de um post de blog'. NÃO para estratégia de conteúdo ou planejamento de calendário (use content-strategy). NÃO para reaproveitar conteúdo existente (use content-repurposing). NÃO apenas para legendas de redes sociais.\"",
            "triggers": [
                "/reprovado",
                "/content-brief-template",
                "/optimization-lista",
                "/objetivo",
                "/content",
                "/not",
                "/content-brief-guide"
            ],
            "dependencies": [],
            "path": "marketing-skill/content-production/SKILL.md"
        },
        {
            "id": "content-strategy",
            "category": "Marketing Skill",
            "title": "Content Strategy",
            "description": "\"Quando o usuário quiser planejar uma estratégia de conteúdo, decidir que conteúdo criar ou descobrir quais tópicos abordar. Use também quando o usuário mencionar 'estratégia de conteúdo', 'sobre o que devo escrever', 'ideias de conteúdo', 'estratégia de blog', 'cluster de tópicos' ou 'planejamento de conteúdo'. Para escrever peças individuais, veja copywriting. Para auditorias específicas de SEO, veja seo-audit.\"",
            "triggers": [
                "/mensal",
                "/product-marketing-context",
                "/spoke",
                "/content-strategy-reference"
            ],
            "dependencies": [],
            "path": "marketing-skill/content-strategy/SKILL.md"
        },
        {
            "id": "copy-editing",
            "category": "Marketing Skill",
            "title": "Copy Editing",
            "description": "\"Quando o usuário quiser editar, revisar ou melhorar copy de marketing existente. Use também quando o usuário mencionar 'editar este copy', 'revisar meu copy', 'feedback de copy', 'revisar', 'polir isso', 'tornar isso melhor' ou 'varredura de copy'. Esta skill fornece uma abordagem sistemática para editar copy de marketing por meio de múltiplas passagens focadas.\"",
            "triggers": [
                "/reprovado",
                "/depois",
                "/plain-english-alternatives",
                "/product-marketing-context",
                "/evid"
            ],
            "dependencies": [],
            "path": "marketing-skill/copy-editing/SKILL.md"
        },
        {
            "id": "copywriting",
            "category": "Marketing Skill",
            "title": "Copywriting",
            "description": "\"Quando o usuário quiser escrever, reescrever ou melhorar copy de marketing para qualquer página — incluindo homepage, landing pages, páginas de precificação, páginas de funcionalidades, sobre nós ou páginas de produto. Use também quando o usuário disser 'escreva copy para', 'melhore este copy', 'reescreva esta página', 'copy de marketing', 'ajuda com título' ou 'copy de CTA'. Para copy de email, veja email-sequence. Para copy de popup, veja popup-cro.\"",
            "triggers": [
                "/enterprise",
                "/copy-frameworks",
                "/tr",
                "/product-marketing-context",
                "/conversacional",
                "/natural-transitions"
            ],
            "dependencies": [],
            "path": "marketing-skill/copywriting/SKILL.md"
        },
        {
            "id": "email-sequence",
            "category": "Marketing Skill",
            "title": "Email Sequence",
            "description": "Quando o usuário quiser criar ou otimizar uma sequência de email, campanha de drip, fluxo de email automatizado ou programa de email de lifecycle. Use também quando o usuário mencionar 'sequência de email', 'campanha de drip', 'sequência de nutrição', 'emails de onboarding', 'sequência de boas-vindas', 'emails de reengajamento', 'automação de email' ou 'emails de lifecycle'. Para onboarding no app, veja onboarding-cro.",
            "triggers": [
                "/acreditam",
                "/integrations",
                "/sa",
                "/email-sequence-playbook",
                "/kit",
                "/newsletter",
                "/tools",
                "/mailchimp",
                "/product-marketing-context",
                "/sendgrid",
                "/resend",
                "/onboarding",
                "/customer-io"
            ],
            "dependencies": [],
            "path": "marketing-skill/email-sequence/SKILL.md"
        },
        {
            "id": "form-cro",
            "category": "Marketing Skill",
            "title": "Form Cro",
            "description": "Quando o usuário quiser otimizar qualquer formulário que NÃO seja de cadastro/registro — incluindo formulários de captura de lead, formulários de contato, formulários de solicitação de demo, formulários de inscrição, formulários de pesquisa ou formulários de checkout. Use também quando o usuário mencionar 'otimização de formulário', 'conversões de formulário de lead', 'atrito no formulário', 'campos do formulário', 'taxa de conclusão do formulário' ou 'formulário de contato'. Para formulários de cadastro/registro, veja signup-flow-cro. Para popups com formulários, veja popup-cro.",
            "triggers": [
                "/vendas",
                "/registro",
                "/form-cro-playbook",
                "/organiza",
                "/conhecidos",
                "/sem",
                "/product-marketing-context",
                "/legais",
                "/feedback"
            ],
            "dependencies": [],
            "path": "marketing-skill/form-cro/SKILL.md"
        },
        {
            "id": "free-tool-strategy",
            "category": "Marketing Skill",
            "title": "Free Tool Strategy",
            "description": "\"Quando o usuário quiser construir uma ferramenta gratuita para marketing — geração de leads, valor de SEO ou conscientização de marca. Use quando mencionar 'engineering as marketing', 'ferramenta gratuita', 'calculadora', 'gerador', 'verificador', 'avaliador', 'ferramenta de marketing', 'ferramenta de geração de leads', 'construir algo para tráfego', 'ferramenta interativa' ou 'recurso gratuito'. Cobre avaliação de ideias, design de ferramenta e estratégia de lançamento. Para estratégia de conteúdo SEO puro (sem ferramenta), use seo-audit ou content-strategy.\"",
            "triggers": [
                "/60",
                "/90",
                "/tool-types-guide",
                "/audita",
                "/tool",
                "/backlinks",
                "/template"
            ],
            "dependencies": [],
            "path": "marketing-skill/free-tool-strategy/SKILL.md"
        },
        {
            "id": "launch-strategy",
            "category": "Marketing Skill",
            "title": "Launch Strategy",
            "description": "\"Quando o usuário quiser planejar um lançamento de produto, anúncio de funcionalidade ou estratégia de release. Use também quando o usuário mencionar 'lançamento', 'Product Hunt', 'release de funcionalidade', 'anúncio', 'go-to-market', 'beta launch', 'acesso antecipado', 'lista de espera', 'atualização de produto', 'plano GTM', 'checklist de lançamento' ou 'momentum de lançamento'. Esta skill cobre lançamentos em fases, estratégia de canais e momentum contínuo pós-lançamento.\"",
            "triggers": [
                "/launch-frameworks-and-checklists",
                "/product-marketing-context"
            ],
            "dependencies": [],
            "path": "marketing-skill/launch-strategy/SKILL.md"
        },
        {
            "id": "marketing-context",
            "category": "Marketing Skill",
            "title": "Marketing Context",
            "description": "\"Criar e manter o documento de contexto de marketing que todas as skills de marketing leem antes de começar. Use quando o usuário mencionar 'contexto de marketing', 'voz da marca', 'configurar contexto', 'público-alvo', 'ICP', 'guia de estilo', 'quem é meu cliente', 'posicionamento', ou quando quiser evitar repetir informações fundamentais em diferentes tarefas de marketing. Execute isso no início de qualquer novo projeto antes de usar outras skills de marketing.\"",
            "triggers": [
                "/marketing-context-template",
                "/marketing-context"
            ],
            "dependencies": [],
            "path": "marketing-skill/marketing-context/SKILL.md"
        },
        {
            "id": "marketing-demand-acquisition",
            "category": "Marketing Skill",
            "title": "Marketing Demand Acquisition",
            "description": "Cria campanhas de geração de demanda, otimiza investimentos em anúncios pagos no LinkedIn, Google e Meta, desenvolve estratégias de SEO e estrutura programas de parceria para startups Série A+ em expansão internacional. Use quando estiver planejando estratégia de marketing, growth marketing, campanhas de publicidade, otimização de PPC, geração de leads, geração de pipeline ou orçamentos de marketing para startups. Cobre aquisição multicanal (Google Ads, LinkedIn Ads, Meta Ads), análise de CAC, fluxos de trabalho MQL/SQL, modelagem de atribuição, SEO técnico e parcerias de co-marketing para movimentos híbridos PLG/Liderado por Vendas nos mercados BR/EU/US/Canada.",
            "triggers": [
                "/campaign-templates",
                "/hubspot-workflows",
                "/calculate",
                "/dia",
                "/co-marketing",
                "/international-playbooks",
                "/attribution-guide"
            ],
            "dependencies": [],
            "path": "marketing-skill/marketing-demand-acquisition/SKILL.md"
        },
        {
            "id": "marketing-ideas",
            "category": "Marketing Skill",
            "title": "Marketing Ideas",
            "description": "\"Quando o usuário precisa de ideias de marketing, inspiração ou estratégias para seu produto SaaS ou software. Use também quando o usuário pedir 'ideias de marketing', 'ideias de crescimento', 'como fazer marketing', 'estratégias de marketing', 'táticas de marketing', 'formas de promover' ou 'ideias para crescer'. Esta skill fornece 139 abordagens de marketing comprovadas organizadas por categoria.\"",
            "triggers": [
                "/impacto",
                "/product-marketing-context",
                "/ideas-by-category",
                "/oportunidade"
            ],
            "dependencies": [],
            "path": "marketing-skill/marketing-ideas/SKILL.md"
        },
        {
            "id": "marketing-ops",
            "category": "Marketing Skill",
            "title": "Marketing Ops",
            "description": "\"Roteador central para o ecossistema de skills de marketing. Use quando não tiver certeza de qual skill de marketing usar, ao orquestrar uma campanha multi-skill ou ao coordenar conteúdo, SEO, CRO, canais e analytics. Use também quando o usuário mencionar 'ajuda com marketing', 'plano de campanha', 'o que devo fazer a seguir', 'prioridades de marketing' ou 'coordenar marketing'.\"",
            "triggers": [],
            "dependencies": [],
            "path": "marketing-skill/marketing-ops/SKILL.md"
        },
        {
            "id": "marketing-psychology",
            "category": "Marketing Skill",
            "title": "Marketing Psychology",
            "description": "\"Quando o usuário quer aplicar princípios psicológicos, modelos mentais ou ciência comportamental ao marketing. Use também quando o usuário mencionar 'psicologia', 'modelos mentais', 'viés cognitivo', 'persuasão', 'ciência comportamental', 'por que as pessoas compram', 'tomada de decisão' ou 'comportamento do consumidor'. Esta skill fornece 70+ modelos mentais organizados para aplicação em marketing.\"",
            "triggers": [
                "/ano",
                "/mental-models-catalog",
                "/depois"
            ],
            "dependencies": [],
            "path": "marketing-skill/marketing-psychology/SKILL.md"
        },
        {
            "id": "marketing-strategy-pmm",
            "category": "Marketing Skill",
            "title": "Marketing Strategy Pmm",
            "description": "Skill de product marketing para posicionamento, estratégia GTM, inteligência competitiva e lançamentos de produto. Use quando o usuário perguntar sobre posicionamento de produto, planejamento de go-to-market, análise competitiva, definição de público-alvo, definição de ICP, pesquisa de mercado, planos de lançamento ou capacitação de vendas. Cobre posicionamento April Dunford, definição de ICP, battlecards competitivos, playbooks de lançamento e entrada em mercados internacionais. Produz entregáveis incluindo declarações de posicionamento, documentos de battlecard, planos de lançamento e estratégias go-to-market.",
            "triggers": [
                "/semana",
                "/launch-checklists",
                "/messaging-templates",
                "/positioning-frameworks",
                "/international-gtm",
                "/loss"
            ],
            "dependencies": [],
            "path": "marketing-skill/marketing-strategy-pmm/SKILL.md"
        },
        {
            "id": "onboarding-cro",
            "category": "Marketing Skill",
            "title": "Onboarding Cro",
            "description": "Quando o usuário quer otimizar o onboarding pós-cadastro, ativação de usuários, experiência de primeiro acesso ou tempo-até-valor. Use também quando o usuário mencionar \"fluxo de onboarding\", \"taxa de ativação\", \"ativação de usuário\", \"experiência de primeiro acesso\", \"empty states\", \"checklist de onboarding\", \"momento aha\" ou \"experiência de novo usuário\". Para otimização de cadastro/registro, veja signup-flow-cro. Para sequências de e-mail contínuas, veja email-sequence.",
            "triggers": [
                "/personalizar",
                "/registro",
                "/experiments",
                "/product-marketing-context",
                "/compartilhar",
                "/fonte",
                "/onboarding",
                "/30"
            ],
            "dependencies": [],
            "path": "marketing-skill/onboarding-cro/SKILL.md"
        },
        {
            "id": "page-cro",
            "category": "Marketing Skill",
            "title": "Page Cro",
            "description": "Quando o usuário quer otimizar, melhorar ou aumentar conversões em qualquer página de marketing — incluindo homepage, landing pages, páginas de preços, páginas de funcionalidades ou posts de blog. Use também quando o usuário disser \"CRO\", \"otimização de taxa de conversão\", \"esta página não está convertendo\", \"melhorar conversões\" ou \"por que esta página não está funcionando\". Para fluxos de cadastro/registro, veja signup-flow-cro. Para ativação pós-cadastro, veja onboarding-cro. Para formulários fora do cadastro, veja form-cro. Para popups/modais, veja popup-cro.",
            "triggers": [
                "/comprar",
                "/registro",
                "/modais",
                "/experiments",
                "/product-marketing-context",
                "/valor",
                "/cria",
                "/compra"
            ],
            "dependencies": [],
            "path": "marketing-skill/page-cro/SKILL.md"
        },
        {
            "id": "paid-ads",
            "category": "Marketing Skill",
            "title": "Paid Ads",
            "description": "\"Quando o usuário quer ajuda com campanhas de publicidade paga no Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, TikTok ou outras plataformas de anúncios. Use também quando o usuário mencionar 'PPC', 'mídia paga', 'copy de anúncio', 'criativo de anúncio', 'ROAS', 'CPA', 'campanha de anúncios', 'retargeting' ou 'segmentação de audiência'. Esta skill cobre estratégia de campanha, criação de anúncios, segmentação de audiência e otimização.\"",
            "triggers": [
                "/ad-copy-templates",
                "/audience-targeting",
                "/segment",
                "/seguras",
                "/platform-setup-checklists",
                "/google-ads",
                "/linkedin-ads",
                "/convers",
                "/integrations",
                "/ga4",
                "/criativos",
                "/semanal",
                "/meta-ads",
                "/pontua",
                "/semana",
                "/empresa",
                "/tools",
                "/funcionalidade",
                "/copy",
                "/tiktok-ads",
                "/benef",
                "/depois",
                "/trial",
                "/product-marketing-context"
            ],
            "dependencies": [],
            "path": "marketing-skill/paid-ads/SKILL.md"
        },
        {
            "id": "paywall-upgrade-cro",
            "category": "Marketing Skill",
            "title": "Paywall Upgrade Cro",
            "description": "Quando o usuário quer criar ou otimizar paywalls in-app, telas de upgrade, modais de upsell ou bloqueios de funcionalidade. Use também quando o usuário mencionar \"paywall\", \"tela de upgrade\", \"modal de upgrade\", \"upsell\", \"bloqueio de funcionalidade\", \"converter free para pago\", \"conversão freemium\", \"tela de expiração de trial\", \"tela de limite atingido\", \"prompt de upgrade de plano\" ou \"precificação in-app\". Distinto das páginas públicas de preços (veja page-cro) — esta skill foca em momentos de upgrade dentro do produto onde o usuário já experimentou valor.",
            "triggers": [
                "/captura",
                "/copy",
                "/momento",
                "/experiments",
                "/depois",
                "/product-marketing-context",
                "/mensagem",
                "/layout"
            ],
            "dependencies": [],
            "path": "marketing-skill/paywall-upgrade-cro/SKILL.md"
        },
        {
            "id": "popup-cro",
            "category": "Marketing Skill",
            "title": "Popup Cro",
            "description": "Quando o usuário quer criar ou otimizar popups, modais, overlays, slide-ins ou banners para fins de conversão. Use também quando o usuário mencionar \"exit intent\", \"conversões de popup\", \"otimização de modal\", \"popup de captura de leads\", \"popup de e-mail\", \"banner de anúncio\" ou \"overlay\". Para formulários fora de popups, veja form-cro. Para otimização geral de conversão de página, veja page-cro.",
            "triggers": [
                "/pesquisa",
                "/popup-cro-playbook",
                "/promo",
                "/funcionalidades",
                "/newsletter",
                "/sem",
                "/product-marketing-context",
                "/blog",
                "/scroll"
            ],
            "dependencies": [],
            "path": "marketing-skill/popup-cro/SKILL.md"
        },
        {
            "id": "pricing-strategy",
            "category": "Marketing Skill",
            "title": "Pricing Strategy",
            "description": "\"Projete, otimize e comunique a precificação de SaaS — estrutura de tiers, métricas de valor, páginas de preços e estratégia de aumento de preços. Use ao construir um modelo de precificação do zero, redesenhar a precificação existente, planejar um aumento de preços ou melhorar uma página de preços. Palavras-chave de gatilho: tiers de preços, página de preços, aumento de preços, embalagem, métrica de valor, precificação por assento, precificação baseada em uso, freemium, good-better-best, estratégia de precificação, monetização, conversão de página de preços, Van Westendorp. NÃO para estratégia de produto mais ampla — use product-strategist para isso. NÃO para sucesso do cliente ou renovações — use customer-success-manager para receita de expansão.\"",
            "triggers": [
                "/melhorias",
                "/risco",
                "/pricing-models",
                "/pricing-page-playbook",
                "/pre",
                "/usu",
                "/downgrade",
                "/anual",
                "/assentos",
                "/pricing",
                "/gratuito"
            ],
            "dependencies": [],
            "path": "marketing-skill/pricing-strategy/SKILL.md"
        },
        {
            "id": "programmatic-seo",
            "category": "Marketing Skill",
            "title": "Programmatic Seo",
            "description": "Quando o usuário quer criar páginas otimizadas para SEO em escala usando templates e dados. Use também quando o usuário mencionar \"SEO programático\", \"páginas de template\", \"páginas em escala\", \"páginas de diretório\", \"páginas de localização\", \"páginas [palavra-chave] + [cidade]\", \"páginas de comparação\", \"páginas de integração\" ou \"construindo muitas páginas para SEO\". Para auditar problemas de SEO existentes, veja seo-audit.",
            "triggers": [
                "/curriculo",
                "/servi",
                "/playbooks",
                "/criativo",
                "/meta",
                "/templates",
                "/product-marketing-context",
                "/ent",
                "/expertise",
                "/an",
                "/coletada"
            ],
            "dependencies": [],
            "path": "marketing-skill/programmatic-seo/SKILL.md"
        },
        {
            "id": "prompt-engineer-toolkit",
            "category": "Marketing Skill",
            "title": "Prompt Engineer Toolkit",
            "description": "\"Analisa e reescreve prompts para melhor saída de IA, cria templates de prompt reutilizáveis para casos de uso de marketing (copy de anúncios, campanhas de e-mail, mídia social) e estrutura fluxos de trabalho de conteúdo de IA de ponta a ponta. Use quando o usuário quer melhorar prompts para marketing assistido por IA, construir templates de prompt ou otimizar fluxos de trabalho de conteúdo de IA. Use também quando o usuário mencionar 'engenharia de prompt', 'melhorar meus prompts', 'qualidade de escrita com IA', 'templates de prompt' ou 'fluxo de trabalho de conteúdo com IA'.\"",
            "triggers": [
                "/evaluation-rubric",
                "/conte",
                "/support",
                "/prompt-templates",
                "/prompt",
                "/casos",
                "/formato",
                "/diffs",
                "/technique-guide"
            ],
            "dependencies": [],
            "path": "marketing-skill/prompt-engineer-toolkit/SKILL.md"
        },
        {
            "id": "referral-program",
            "category": "Marketing Skill",
            "title": "Referral Program",
            "description": "\"Quando o usuário quer projetar, lançar ou otimizar um programa de indicação ou afiliados. Use quando mencionarem 'programa de indicação', 'programa de afiliados', 'boca a boca', 'indique um amigo', 'programa de incentivo', 'indicações de clientes', 'embaixador de marca', 'programa de parceiros', 'link de indicação' ou 'crescimento por indicações'. Cobre mecânicas do programa, design de incentivos e otimização — não apenas a ideia de indicações, mas o sistema real.\"",
            "triggers": [
                "/referral",
                "/program-mechanics",
                "/measurement-framework",
                "/indica",
                "/colar"
            ],
            "dependencies": [],
            "path": "marketing-skill/referral-program/SKILL.md"
        },
        {
            "id": "schema-markup",
            "category": "Marketing Skill",
            "title": "Schema Markup",
            "description": "\"Quando o usuário quer implementar, auditar ou validar dados estruturados (schema markup) no seu site. Use quando o usuário mencionar 'dados estruturados', 'schema.org', 'JSON-LD', 'rich results', 'rich snippets', 'schema markup', 'FAQ schema', 'Product schema', 'HowTo schema' ou 'erros de dados estruturados no Search Console'. Use também quando alguém pergunta por que seu conteúdo não está exibindo rich results ou quer melhorar a visibilidade na busca por IA. NÃO para auditorias gerais de SEO (use seo-audit) ou problemas técnicos de rastreamento SEO (use site-architecture).\"",
            "triggers": [
                "/validator",
                "/rich-results",
                "/search",
                "/implementation-patterns",
                "/script",
                "/exemplo",
                "/schema-types-guide",
                "/colar",
                "/schema",
                "/test",
                "/ausentes",
                "/image",
                "/ld",
                "/head"
            ],
            "dependencies": [],
            "path": "marketing-skill/schema-markup/SKILL.md"
        },
        {
            "id": "seo-audit",
            "category": "Marketing Skill",
            "title": "Seo Audit",
            "description": "Quando o usuário quer auditar, revisar ou diagnosticar problemas de SEO no seu site. Use também quando o usuário mencionar \"auditoria de SEO\", \"SEO técnico\", \"por que não estou rankeando\", \"problemas de SEO\", \"SEO on-page\", \"revisão de meta tags\" ou \"verificação de saúde de SEO\". Para construir páginas em escala para segmentar palavras-chave, veja programmatic-seo. Para adicionar dados estruturados, veja schema-markup.",
            "triggers": [
                "/ai-writing-detection",
                "/indexa",
                "/seo-audit-reference",
                "/ranking",
                "/palavras-chave",
                "/product-marketing-context",
                "/aeo-geo-patterns"
            ],
            "dependencies": [],
            "path": "marketing-skill/seo-audit/SKILL.md"
        },
        {
            "id": "signup-flow-cro",
            "category": "Marketing Skill",
            "title": "Signup Flow Cro",
            "description": "Quando o usuário quer otimizar fluxos de cadastro, registro, criação de conta ou ativação de trial. Use também quando o usuário mencionar \"conversões de cadastro\", \"atrito no registro\", \"otimização de formulário de cadastro\", \"cadastro de trial gratuito\", \"reduzir abandono no cadastro\" ou \"fluxo de criação de conta\". Para onboarding pós-cadastro, veja onboarding-cro. Para formulários de captura de leads (não criação de conta), veja form-cro.",
            "triggers": [
                "/acesso",
                "/caso",
                "/organiza",
                "/telas",
                "/product-marketing-context",
                "/signup-cro-playbook",
                "/cria"
            ],
            "dependencies": [],
            "path": "marketing-skill/signup-flow-cro/SKILL.md"
        },
        {
            "id": "site-architecture",
            "category": "Marketing Skill",
            "title": "Site Architecture",
            "description": "\"Quando o usuário quer auditar, redesenhar ou planejar a estrutura do seu site, hierarquia de URL, design de navegação ou estratégia de linking interno. Use quando o usuário mencionar 'arquitetura do site', 'estrutura de URL', 'links internos', 'navegação do site', 'breadcrumbs', 'cluster de tópicos', 'páginas hub', 'páginas órfãs', 'estrutura de silo', 'arquitetura da informação' ou 'reorganização do site'. Use também quando alguém tem problemas de SEO e a causa raiz é estrutural (não conteúdo ou schema). NÃO para decisões de estratégia de conteúdo sobre o que escrever (use content-strategy) ou para schema markup (use schema-markup).\"",
            "triggers": [
                "/pagina",
                "/conte",
                "/como-escrever-emails-frios",
                "/reestrutura",
                "/email-marketing",
                "/solucoes",
                "/automacao-email",
                "/categoria",
                "/auditoria-seo-tecnico",
                "/precos",
                "/dicas-seo-2024",
                "/hub",
                "/seo-on-page",
                "/sobre-nos-info-empresa",
                "/servicos",
                "/marketing",
                "/web-design",
                "/exemplo",
                "/guia",
                "/internal-linking-playbook",
                "/recursos",
                "/link-building",
                "/pesquisa-palavras-chave",
                "/sobre",
                "/depois",
                "/seo",
                "/dicas-email-frio",
                "/palavras-chave-long-tail",
                "/artigo",
                "/como",
                "/auditoria-seo-tecnico-checklist-como-completar-passo-a-passo",
                "/sitemap",
                "/url-design-guide",
                "/blog",
                "/seo-tecnico",
                "/guias",
                "/pagina-de-precos"
            ],
            "dependencies": [],
            "path": "marketing-skill/site-architecture/SKILL.md"
        },
        {
            "id": "social-content",
            "category": "Marketing Skill",
            "title": "Social Content",
            "description": "\"Quando o usuário quer ajuda para criar, agendar ou otimizar conteúdo de mídia social para LinkedIn, Twitter/X, Instagram, TikTok, Facebook ou outras plataformas. Use também quando o usuário mencionar 'post no LinkedIn', 'thread no Twitter', 'mídia social', 'calendário editorial', 'agendamento social', 'engajamento' ou 'conteúdo viral'. Esta skill cobre criação de conteúdo, reaproveitamento e estratégias específicas por plataforma.\"",
            "triggers": [
                "/visual",
                "/semana",
                "/republicar",
                "/tend",
                "/post-templates",
                "/platforms",
                "/republica",
                "/product-marketing-context",
                "/reverse-engineering",
                "/falha",
                "/dia"
            ],
            "dependencies": [],
            "path": "marketing-skill/social-content/SKILL.md"
        },
        {
            "id": "social-media-analyzer",
            "category": "Marketing Skill",
            "title": "Social Media Analyzer",
            "description": "Análise de campanhas de mídia social e rastreamento de desempenho. Calcula taxas de engajamento, ROI e benchmarks entre plataformas. Use para analisar desempenho de mídia social, calcular taxa de engajamento, medir ROI de campanha, comparar métricas de plataforma ou fazer benchmark de engajamento contra padrões do setor.",
            "triggers": [
                "/bookmarks",
                "/sample",
                "/retweets",
                "/expected",
                "/calculate",
                "/rea",
                "/analyze",
                "/platform-benchmarks"
            ],
            "dependencies": [],
            "path": "marketing-skill/social-media-analyzer/SKILL.md"
        },
        {
            "id": "social-media-manager",
            "category": "Marketing Skill",
            "title": "Social Media Manager",
            "description": "\"Quando o usuário quer desenvolver estratégia de mídia social, planejar calendários editoriais, gerenciar engajamento com a comunidade ou crescer sua presença social entre plataformas. Use também quando o usuário mencionar 'estratégia de mídia social', 'calendário social', 'gestão de comunidade', 'plano de mídia social', 'crescer seguidores', 'taxa de engajamento', 'auditoria de mídia social' ou 'quais plataformas devo usar'. Para criar posts sociais individuais, veja social-content. Para analisar dados de desempenho social, veja social-media-analyzer.\"",
            "triggers": [
                "/semana",
                "/conversas",
                "/20",
                "/promo",
                "/salvamento",
                "/dia"
            ],
            "dependencies": [],
            "path": "marketing-skill/social-media-manager/SKILL.md"
        },
        {
            "id": "video-content-strategist",
            "category": "Marketing Skill",
            "title": "Video Content Strategist",
            "description": "\"Use quando planejar estratégia de conteúdo em vídeo, escrever scripts de vídeo, otimizar canais do YouTube, construir pipelines de vídeo curto (Reels, TikTok, Shorts) ou reaproveitar conteúdo longo em vídeo. Gatilhos: 'criar canal no YouTube', 'estratégia de conteúdo em vídeo', 'escrever script de vídeo', 'reaproveitar em vídeo', 'SEO para YouTube', 'vídeo curto'. NÃO para conteúdo escrito em blog (use content-production). NÃO para legendas sociais sem vídeo (use social-media-manager).\"",
            "triggers": [
                "/resumo",
                "/cita",
                "/descoberta",
                "/podcast",
                "/timestamps",
                "/webinar",
                "/or"
            ],
            "dependencies": [],
            "path": "marketing-skill/video-content-strategist/SKILL.md"
        },
        {
            "id": "x-twitter-growth",
            "category": "Marketing Skill",
            "title": "X Twitter Growth",
            "description": "\"Motor de crescimento no X/Twitter para construir audiência, criar conteúdo viral e analisar engajamento. Use quando o usuário quer crescer no X/Twitter, escrever tweets ou threads, analisar o perfil no X, pesquisar concorrentes no X, planejar estratégia de postagem ou otimizar engajamento. Complementa social-content (múltiplas plataformas) com profundidade específica para o X: mecânica do algoritmo, engenharia de threads, estratégia de replies, otimização de perfil e inteligência competitiva via busca na web.\"",
            "triggers": [
                "/contradiz",
                "/profile",
                "/semana",
                "/mensais",
                "/growth",
                "/content",
                "/perspicazes",
                "/threads",
                "/tweet",
                "/competitor",
                "/dia"
            ],
            "dependencies": [],
            "path": "marketing-skill/x-twitter-growth/SKILL.md"
        }
    ],
    "Marketing Vendas": [
        {
            "id": "analise-competitiva",
            "category": "Marketing Vendas",
            "title": "Analise Competitiva",
            "description": "|",
            "triggers": [
                "/competitor-analysis",
                "/read",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "marketing-vendas/analise-competitiva/SKILL.md"
        },
        {
            "id": "deck-de-pitch",
            "category": "Marketing Vendas",
            "title": "Deck De Pitch",
            "description": "|",
            "triggers": [
                "/pitch-deck",
                "/read",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "marketing-vendas/deck-de-pitch/SKILL.md"
        },
        {
            "id": "estrategia-promocional",
            "category": "Marketing Vendas",
            "title": "Estrategia Promocional",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/skill",
                "/promo-strategy",
                "/15"
            ],
            "dependencies": [],
            "path": "marketing-vendas/estrategia-promocional/SKILL.md"
        },
        {
            "id": "estudo-de-caso",
            "category": "Marketing Vendas",
            "title": "Estudo De Caso",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/case-study",
                "/skill"
            ],
            "dependencies": [],
            "path": "marketing-vendas/estudo-de-caso/SKILL.md"
        },
        {
            "id": "follow-up",
            "category": "Marketing Vendas",
            "title": "Follow Up",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/follow-up",
                "/skill",
                "/mensagem"
            ],
            "dependencies": [],
            "path": "marketing-vendas/follow-up/SKILL.md"
        },
        {
            "id": "funil-vendas",
            "category": "Marketing Vendas",
            "title": "Funil Vendas",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/funil-vendas",
                "/skill"
            ],
            "dependencies": [],
            "path": "marketing-vendas/funil-vendas/SKILL.md"
        },
        {
            "id": "objecoes-vendas",
            "category": "Marketing Vendas",
            "title": "Objecoes Vendas",
            "description": "|",
            "triggers": [
                "/read",
                "/turma",
                "/rules",
                "/skill",
                "/objecoes-vendas"
            ],
            "dependencies": [],
            "path": "marketing-vendas/objecoes-vendas/SKILL.md"
        },
        {
            "id": "proposta-comercial",
            "category": "Marketing Vendas",
            "title": "Proposta Comercial",
            "description": "|",
            "triggers": [
                "/60",
                "/ano",
                "/read",
                "/cart",
                "/90",
                "/rules",
                "/skill",
                "/proposta-comercial"
            ],
            "dependencies": [],
            "path": "marketing-vendas/proposta-comercial/SKILL.md"
        },
        {
            "id": "script-vendas",
            "category": "Marketing Vendas",
            "title": "Script Vendas",
            "description": "|",
            "triggers": [
                "/read",
                "/script-vendas",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "marketing-vendas/script-vendas/SKILL.md"
        },
        {
            "id": "voz-da-marca",
            "category": "Marketing Vendas",
            "title": "Voz Da Marca",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/evitado",
                "/skill",
                "/brand-voice"
            ],
            "dependencies": [],
            "path": "marketing-vendas/voz-da-marca/SKILL.md"
        }
    ],
    "Operacoes Rh": [
        {
            "id": "automacao-processos",
            "category": "Operacoes Rh",
            "title": "Automacao Processos",
            "description": "|",
            "triggers": [
                "/read",
                "/automacao-processos",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "operacoes-rh/automacao-processos/SKILL.md"
        },
        {
            "id": "avaliacao-desempenho",
            "category": "Operacoes Rh",
            "title": "Avaliacao Desempenho",
            "description": "|",
            "triggers": [
                "/avaliacao-desempenho",
                "/read",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "operacoes-rh/avaliacao-desempenho/SKILL.md"
        },
        {
            "id": "clt-pj-mei",
            "category": "Operacoes Rh",
            "title": "Clt Pj Mei",
            "description": "|",
            "triggers": [
                "/ano",
                "/read",
                "/semana",
                "/clt-pj-mei",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "operacoes-rh/clt-pj-mei/SKILL.md"
        },
        {
            "id": "criador-de-sop",
            "category": "Operacoes Rh",
            "title": "Criador De Sop",
            "description": "|",
            "triggers": [
                "/read",
                "/sop-creator",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "operacoes-rh/criador-de-sop/SKILL.md"
        },
        {
            "id": "cultura-empresa",
            "category": "Operacoes Rh",
            "title": "Cultura Empresa",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/skill",
                "/cultura-empresa",
                "/presente"
            ],
            "dependencies": [],
            "path": "operacoes-rh/cultura-empresa/SKILL.md"
        },
        {
            "id": "descricao-de-vagas",
            "category": "Operacoes Rh",
            "title": "Descricao De Vagas",
            "description": "|",
            "triggers": [
                "/read",
                "/semana",
                "/remoto",
                "/rules",
                "/job-description",
                "/skill"
            ],
            "dependencies": [],
            "path": "operacoes-rh/descricao-de-vagas/SKILL.md"
        },
        {
            "id": "facilitador-de-reunioes",
            "category": "Operacoes Rh",
            "title": "Facilitador De Reunioes",
            "description": "|",
            "triggers": [
                "/read",
                "/investidores",
                "/rules",
                "/skill",
                "/meeting-facilitator"
            ],
            "dependencies": [],
            "path": "operacoes-rh/facilitador-de-reunioes/SKILL.md"
        },
        {
            "id": "gestao-de-okrs",
            "category": "Operacoes Rh",
            "title": "Gestao De Okrs",
            "description": "|",
            "triggers": [
                "/read",
                "/rules",
                "/skill",
                "/03",
                "/okr-manager"
            ],
            "dependencies": [],
            "path": "operacoes-rh/gestao-de-okrs/SKILL.md"
        },
        {
            "id": "onboarding",
            "category": "Operacoes Rh",
            "title": "Onboarding",
            "description": "|",
            "triggers": [
                "/60",
                "/read",
                "/padrinho",
                "/90",
                "/rules",
                "/skill",
                "/onboarding"
            ],
            "dependencies": [],
            "path": "operacoes-rh/onboarding/SKILL.md"
        },
        {
            "id": "politicas-rh",
            "category": "Operacoes Rh",
            "title": "Politicas Rh",
            "description": "|",
            "triggers": [
                "/read",
                "/politicas-rh",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "operacoes-rh/politicas-rh/SKILL.md"
        }
    ],
    "Product Team": [
        {
            "id": "agile-product-owner",
            "category": "Product Team",
            "title": "Agile Product Owner",
            "description": "Gestão ágil de produto para gerenciamento de backlog e execução de sprint. Cobre escrita de user stories, critérios de aceitação, planejamento de sprint e rastreamento de velocidade. Use para escrever user stories, criar critérios de aceitação, planejar sprints, estimar story points, desmembrar épicos ou priorizar o backlog.",
            "triggers": [
                "/context",
                "/user-story-templates",
                "/trigger",
                "/capability",
                "/sprint-planning-guide",
                "/product-manager-toolkit",
                "/user",
                "/value",
                "/scrum-master"
            ],
            "dependencies": [],
            "path": "product-team/agile-product-owner/SKILL.md"
        },
        {
            "id": "apple-hig-expert",
            "category": "Product Team",
            "title": "Apple Hig Expert",
            "description": "\"Orientação especializada nas Diretrizes de Interface Humana (HIG) da Apple. Abrange iOS, macOS e visionOS com a estética Liquid Glass de 2026 e design com acessibilidade em primeiro lugar.\"",
            "triggers": [
                "/olhar",
                "/hig-audit-template",
                "/platform-specifics",
                "/visual-design",
                "/defer"
            ],
            "dependencies": [],
            "path": "product-team/apple-hig-expert/SKILL.md"
        },
        {
            "id": "code-to-prd",
            "category": "Product Team",
            "title": "Code To Prd",
            "description": "|",
            "triggers": [
                "/pages",
                "/xxx",
                "/base",
                "/api",
                "/role",
                "/urls",
                "/modules",
                "/serializer",
                "/app",
                "/rotas",
                "/campos",
                "/github",
                "/view",
                "/lista",
                "/prd",
                "/direita",
                "/create",
                "/pull",
                "/response",
                "/models",
                "/user",
                "/prd-quality-checklist",
                "/368",
                "/lihanglogan",
                "/sa",
                "/claude-skills",
                "/list",
                "/code-to-prd",
                "/throttle",
                "/framework-patterns",
                "/permiss",
                "/pipes",
                "/endpoint",
                "/fixture",
                "/to",
                "/recursos",
                "/inicializa",
                "/project",
                "/myproject",
                "/hardcoded",
                "/se",
                "/path",
                "/servi",
                "/order",
                "/registro",
                "/codebase",
                "/views",
                "/users",
                "/alirezarezvani",
                "/interceptors",
                "/orders",
                "/apps",
                "/filtro",
                "/01-user-mgmt-list",
                "/src"
            ],
            "dependencies": [],
            "path": "product-team/code-to-prd/SKILL.md"
        },
        {
            "id": "competitive-teardown",
            "category": "Product Team",
            "title": "Competitive Teardown",
            "description": "\"Analisa produtos e empresas concorrentes sintetizando dados de páginas de preços, avaliações de app stores, ofertas de emprego, sinais de SEO e redes sociais em inteligência competitiva estruturada. Produz matrizes de comparação de funcionalidades pontuadas em 12 dimensões, análises SWOT, mapas de posicionamento, auditorias de UX, detalhamentos de modelos de precificação, roadmaps de itens de ação e templates de apresentação para partes interessadas. Use ao realizar análise de concorrentes, comparar produtos com competidores, pesquisar o cenário competitivo, criar battle cards para vendas, preparar uma sessão de estratégia ou roadmap de produto, responder a um novo recurso ou mudança de preço de um concorrente, ou realizar uma revisão competitiva trimestral.\"",
            "triggers": [
                "/enterprise",
                "/data-collection-guide",
                "/itunes",
                "/customerreviews",
                "/sort",
                "/landing-page-generator",
                "/rss",
                "/json",
                "/id",
                "/product-strategist",
                "/analysis-templates",
                "/search"
            ],
            "dependencies": [],
            "path": "product-team/competitive-teardown/SKILL.md"
        },
        {
            "id": "experiment-designer",
            "category": "Product Team",
            "title": "Experiment Designer",
            "description": "Use ao planejar experimentos de produto, escrever hipóteses testáveis, estimar tamanho de amostra, priorizar testes ou interpretar resultados de A/B com rigor estatístico prático.",
            "triggers": [
                "/experiment-playbook",
                "/risco",
                "/sample",
                "/velocidade",
                "/statistics-reference",
                "/sem",
                "/magnitude",
                "/complexidade"
            ],
            "dependencies": [],
            "path": "product-team/experiment-designer/SKILL.md"
        },
        {
            "id": "growth-product-manager",
            "category": "Product Team",
            "title": "Growth Product Manager",
            "description": "\"Growth Product Manager sênior especializado em aquisição, ativação, retenção, receita e referral (AARRR), growth loops, experimentação em escala (A/B tests, multi-arm bandits), PLG, onboarding, activation engineering, north-star metrics e tooling de experimentação. Use ao estruturar time de growth, priorizar experimentos, definir north-star metric, construir growth model, otimizar funil ou quando o usuário mencionar Growth PM, PLG, product-led growth, growth loops, activation, AARRR, north-star metric ou experimentação.\"",
            "triggers": [
                "/ano",
                "/ab-test-setup",
                "/usu",
                "/marketing-skill",
                "/cpo-advisor",
                "/c-level-advisor",
                "/dia"
            ],
            "dependencies": [],
            "path": "product-team/growth-product-manager/SKILL.md"
        },
        {
            "id": "landing-page-generator",
            "category": "Product Team",
            "title": "Landing Page Generator",
            "description": "\"Gera landing pages de alta conversão como componentes Next.js/React (TSX) completos com Tailwind CSS. Cria seções hero, grids de funcionalidades, tabelas de preços, accordions de FAQ, blocos de depoimentos e seções CTA usando frameworks de copy comprovados (PAS, AIDA, BAB). Produz meta tags SEO, dados estruturados e código otimizado para desempenho visando Core Web Vitals (LCP < 1s, CLS < 0.1). Use quando o usuário pede para criar uma landing page, página de marketing, homepage, site de página única, página de captura de leads, página de campanha, página de promoção ou página web otimizada para conversão — ou quando quer testar variantes de landing page A/B ou substituir uma página estática por uma projetada para converter.\"",
            "triggers": [
                "/pro",
                "/div",
                "/20",
                "/bundle-analyzer",
                "/section",
                "/400",
                "/50",
                "/enterprise",
                "/scripts",
                "/competitive-teardown",
                "/content-production",
                "/brand",
                "/ui-design-system",
                "/10",
                "/height",
                "/30",
                "/ld",
                "/span",
                "/h1"
            ],
            "dependencies": [],
            "path": "product-team/landing-page-generator/SKILL.md"
        },
        {
            "id": "product-analytics",
            "category": "Product Team",
            "title": "Product Analytics",
            "description": "Use ao definir KPIs de produto, construir dashboards de métricas, executar análise de coorte ou retenção, ou interpretar tendências de adoção de funcionalidades em diferentes estágios de produto.",
            "triggers": [
                "/experiment-designer",
                "/product-discovery",
                "/metrics",
                "/saas-metrics-coach",
                "/metrics-frameworks",
                "/dashboard-templates",
                "/coorte",
                "/product-manager-toolkit",
                "/oportunidade"
            ],
            "dependencies": [],
            "path": "product-team/product-analytics/SKILL.md"
        },
        {
            "id": "product-discovery",
            "category": "Product Team",
            "title": "Product Discovery",
            "description": "Use ao validar oportunidades de produto, mapear suposições, planejar sprints de descoberta ou testar o fit problema-solução antes de comprometer recursos de entrega.",
            "triggers": [
                "/assumption",
                "/dores",
                "/ativa",
                "/certeza",
                "/experimentos",
                "/tempo",
                "/discovery-frameworks",
                "/operar"
            ],
            "dependencies": [],
            "path": "product-team/product-discovery/SKILL.md"
        },
        {
            "id": "product-manager-toolkit",
            "category": "Product Team",
            "title": "Product Manager Toolkit",
            "description": "Kit de ferramentas abrangente para gerentes de produto incluindo priorização RICE, análise de entrevistas com clientes, templates de PRD, frameworks de descoberta e estratégias de go-to-market. Use para priorização de funcionalidades, síntese de pesquisa com usuários, documentação de requisitos e desenvolvimento de estratégia de produto.",
            "triggers": [
                "/input-output-examples",
                "/prd",
                "/rice",
                "/customer",
                "/frameworks"
            ],
            "dependencies": [],
            "path": "product-team/product-manager-toolkit/SKILL.md"
        },
        {
            "id": "product-strategist",
            "category": "Product Team",
            "title": "Product Strategist",
            "description": "Kit de ferramentas de liderança estratégica de produto para Head of Product cobrindo geração de cascata OKR, planejamento trimestral, análise do cenário competitivo, documentos de visão de produto e propostas de escalabilidade de equipe. Use ao criar documentos OKR trimestrais, definir metas ou KPIs de produto, construir roadmap de produto, executar análise competitiva, redigir estrutura de equipe ou planos de contratação, alinhar estratégia de produto entre engenharia e design, ou gerar hierarquias de metas em cascata do nível da empresa ao nível da equipe.",
            "triggers": [
                "/examples",
                "/sample",
                "/strategy",
                "/senior-pm",
                "/competitive-teardown",
                "/okr"
            ],
            "dependencies": [],
            "path": "product-team/product-strategist/SKILL.md"
        },
        {
            "id": "research-summarizer",
            "category": "Product Team",
            "title": "Research Summarizer",
            "description": "\"Skill de agente de sumarização de pesquisa estruturada para usuários não-dev. Lida com artigos acadêmicos, artigos web, relatórios e documentação. Extrai descobertas principais, gera análises comparativas e produz citações formatadas corretamente. Use quando: o usuário quer resumir um artigo de pesquisa, comparar múltiplas fontes, extrair citações de documentos ou criar briefings de pesquisa estruturados. Plugin para Claude Code.\"",
            "triggers": [
                "/citation-formats",
                "/summary-templates",
                "/github",
                "/research-summarizer",
                "/fazer",
                "/alirezarezvani",
                "/product-team",
                "/skills",
                "/extract",
                "/research",
                "/claude-skills",
                "/format"
            ],
            "dependencies": [],
            "path": "product-team/research-summarizer/SKILL.md"
        },
        {
            "id": "roadmap-communicator",
            "category": "Product Team",
            "title": "Roadmap Communicator",
            "description": "Use ao preparar narrativas de roadmap, notas de versão, changelogs ou atualizações para partes interessadas adaptadas para executivos, equipes de engenharia e clientes.",
            "triggers": [
                "/roadmap-templates",
                "/changelog",
                "/communication-templates",
                "/comportamento"
            ],
            "dependencies": [],
            "path": "product-team/roadmap-communicator/SKILL.md"
        },
        {
            "id": "saas-scaffolder",
            "category": "Product Team",
            "title": "Saas Scaffolder",
            "description": "\"Gera boilerplate completo e pronto para produção de projeto SaaS incluindo autenticação, schemas de banco de dados, integração de billing, rotas de API e um dashboard funcional usando Next.js 14+ App Router, TypeScript, Tailwind CSS, shadcn/ui, Drizzle ORM e Stripe. Use quando o usuário quer criar um novo app SaaS, iniciar um projeto web baseado em assinaturas, scaffoldar uma aplicação Next.js, ou menciona termos como template starter, boilerplate, novo projeto ou configurar auth e pagamentos.\"",
            "triggers": [
                "/ui",
                "/api",
                "/auth",
                "/dashboard",
                "/server",
                "/login",
                "/lib",
                "/portal",
                "/neondb",
                "/db",
                "/route",
                "/pg-core",
                "/user",
                "/index",
                "/pricing",
                "/settings",
                "/ratelimit",
                "/billing",
                "/providers",
                "/google",
                "/schema",
                "/middleware",
                "/checkout",
                "/stripe",
                "/page",
                "/webhooks",
                "/drizzle-adapter",
                "/localhost"
            ],
            "dependencies": [],
            "path": "product-team/saas-scaffolder/SKILL.md"
        },
        {
            "id": "spec-to-repo",
            "category": "Product Team",
            "title": "Spec To Repo",
            "description": "\"Use quando o usuário diz 'crie um app para mim', 'crie um projeto a partir desta especificação', 'scaffolde um novo repo', 'gere um starter', 'transforme esta ideia em código', 'faça bootstrap de um projeto', 'tenho requisitos e preciso de uma base de código', ou fornece uma especificação de projeto em linguagem natural e espera um repositório completo e executável. Agnóstico de stack: Next.js, FastAPI, Rails, Go, Rust, Flutter e mais.\"",
            "triggers": [
                "/comandos",
                "/conclu",
                "/cole",
                "/database-designer",
                "/polimento",
                "/workflows",
                "/em-progresso",
                "/generated-project",
                "/route",
                "/response",
                "/senior-fullstack",
                "/spec-driven-workflow",
                "/saas-scaffolder",
                "/ci",
                "/to",
                "/deploy",
                "/stack-templates",
                "/path",
                "/start",
                "/page",
                "/componente",
                "/validate"
            ],
            "dependencies": [],
            "path": "product-team/spec-to-repo/SKILL.md"
        },
        {
            "id": "ui-design-system",
            "category": "Product Team",
            "title": "Ui Design System",
            "description": "Kit de ferramentas de sistema de UI design para Designer UI Sênior incluindo geração de design tokens, documentação de componentes, cálculos de design responsivo e ferramentas de handoff para desenvolvedores. Use para criar sistemas de design, manter consistência visual e facilitar a colaboração design-dev.",
            "triggers": [
                "/vari",
                "/design-tokens",
                "/ferramentas",
                "/developer-handoff",
                "/padr",
                "/button",
                "/component-architecture",
                "/design",
                "/responsive-calculations"
            ],
            "dependencies": [],
            "path": "product-team/ui-design-system/SKILL.md"
        },
        {
            "id": "ux-researcher-designer",
            "category": "Product Team",
            "title": "Ux Researcher Designer",
            "description": "Kit de ferramentas de pesquisa UX e design para Designer/Pesquisador UX Sênior incluindo geração de personas orientada por dados, mapeamento de jornada, frameworks de testes de usabilidade e síntese de pesquisa. Use para pesquisa com usuários, criação de personas, mapeamento de jornada e validação de design.",
            "triggers": [
                "/usability-testing-frameworks",
                "/semanas",
                "/persona",
                "/ui-design-system",
                "/20",
                "/product-manager-toolkit",
                "/onde",
                "/persona-methodology",
                "/dias",
                "/journey-mapping-guide"
            ],
            "dependencies": [],
            "path": "product-team/ux-researcher-designer/SKILL.md"
        }
    ],
    "Produto Ecommerce": [
        {
            "id": "abandono-de-carrinho",
            "category": "Produto Ecommerce",
            "title": "Abandono De Carrinho",
            "description": "\"Recuperação de carrinho abandonado para e-commerces brasileiros: sequência de email, WhatsApp e retargeting no Meta Ads e Google. Scripts de copy em PT-BR com gatilhos psicológicos adaptados ao mercado nacional.\"",
            "triggers": [
                "/cart-abandonment",
                "/read",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/abandono-de-carrinho/SKILL.md"
        },
        {
            "id": "analise-de-churn",
            "category": "Produto Ecommerce",
            "title": "Analise De Churn",
            "description": "\"Diagnóstico completo de churn para SaaS: identificação de causas, cohort analysis, health scoring de clientes, estratégias de retenção e playbooks de salvamento. Métricas e benchmarks do mercado brasileiro.\"",
            "triggers": [
                "/read",
                "/churn-analysis",
                "/rules",
                "/skill",
                "/opera"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/analise-de-churn/SKILL.md"
        },
        {
            "id": "analitica-de-produto",
            "category": "Produto Ecommerce",
            "title": "Analitica De Produto",
            "description": "\"Métricas de produto digital: DAU, MAU, NPS, retenção, feature adoption e funil de ativação. Inclui como configurar eventos, interpretar dados e tomar decisões baseadas em evidências para produtos BR.\"",
            "triggers": [
                "/read",
                "/skill",
                "/rules",
                "/product-analytics"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/analitica-de-produto/SKILL.md"
        },
        {
            "id": "estrategia-marketplace",
            "category": "Produto Ecommerce",
            "title": "Estrategia Marketplace",
            "description": "\"Estratégia completa para vender em marketplaces brasileiros: Mercado Livre, Amazon BR, Shopee e Magalu. Inclui precificação competitiva, otimização de listing, gestão de reputação e operação logística.\"",
            "triggers": [
                "/read",
                "/rules",
                "/marketplace-strategy",
                "/skill"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/estrategia-marketplace/SKILL.md"
        },
        {
            "id": "estrategia-plg",
            "category": "Produto Ecommerce",
            "title": "Estrategia Plg",
            "description": "\"Product-Led Growth: estratégia para produtos que se vendem sozinhos via uso. Cobre trial gratuito, freemium, expansão de receita, viralidade e loops de crescimento. Adaptado para SaaS brasileiro com métricas em R$.\"",
            "triggers": [
                "/read",
                "/rules",
                "/plg-strategy",
                "/skill",
                "/30"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/estrategia-plg/SKILL.md"
        },
        {
            "id": "lancamento-produto",
            "category": "Produto Ecommerce",
            "title": "Lancamento Produto",
            "description": "\"Playbook completo de lançamento de produto digital: pré-lançamento (lista de espera, validação), lançamento (semana de abertura, sequência de emails) e pós-lançamento (onboarding, retenção inicial). Contexto de mercado brasileiro.\"",
            "triggers": [
                "/lancamento-produto",
                "/read",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/lancamento-produto/SKILL.md"
        },
        {
            "id": "operacoes-ecommerce",
            "category": "Produto Ecommerce",
            "title": "Operacoes Ecommerce",
            "description": "\"Operações completas de e-commerce brasileiro: catálogo de produtos, estratégia de frete, otimização de checkout, política de devoluções e gestão de estoque. Considera plataformas e regulamentações do mercado nacional.\"",
            "triggers": [
                "/ecommerce-ops",
                "/read",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/operacoes-ecommerce/SKILL.md"
        },
        {
            "id": "precificacao-saas",
            "category": "Produto Ecommerce",
            "title": "Precificacao Saas",
            "description": "\"Precificação de SaaS brasileiro: criação de tiers, modelo anual vs. mensal, testes de preço em R$, cálculo de margem e benchmarks de mercado. Considera poder de compra, câmbio e particularidades tributárias do Brasil.\"",
            "triggers": [
                "/read",
                "/cliente",
                "/rules",
                "/skill",
                "/seat",
                "/consumo",
                "/pricing-saas"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/precificacao-saas/SKILL.md"
        },
        {
            "id": "roadmap-de-produto",
            "category": "Produto Ecommerce",
            "title": "Roadmap De Produto",
            "description": "\"Criação de roadmap de produto com frameworks de priorização RICE, ICE e Now/Next/Later. Inclui gestão de stakeholders, comunicação de decisões e métricas de sucesso para cada iniciativa.\"",
            "triggers": [
                "/read",
                "/clientes",
                "/product-roadmap",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/roadmap-de-produto/SKILL.md"
        },
        {
            "id": "upsell-e-crosssell",
            "category": "Produto Ecommerce",
            "title": "Upsell E Crosssell",
            "description": "\"Estratégias de expansão de receita na base de clientes: upsell (upgrade de plano), cross-sell (produtos complementares) e downsell (retenção com plano menor). Playbooks e scripts para contexto brasileiro.\"",
            "triggers": [
                "/read",
                "/rules",
                "/upsell-crosssell",
                "/skill"
            ],
            "dependencies": [],
            "path": "produto-ecommerce/upsell-e-crosssell/SKILL.md"
        }
    ],
    "Project Management": [
        {
            "id": "atlassian-admin",
            "category": "Project Management",
            "title": "Atlassian Admin",
            "description": "Administrador Atlassian para gerenciar e organizar produtos Atlassian (Jira, Confluence, Bitbucket, Trello), usuários, permissões, segurança, integrações, configuração do sistema e governança organizacional. Use quando solicitado a adicionar usuários ao Jira, alterar permissões do Confluence, configurar controle de acesso, atualizar configurações de administrador, gerenciar grupos Atlassian, configurar SSO, instalar apps do marketplace, revisar políticas de segurança ou lidar com qualquer tarefa de administração Atlassian em nível organizacional.",
            "triggers": [
                "/audit-log",
                "/rest",
                "/api",
                "/mensal",
                "/thread",
                "/property",
                "/v1",
                "/cobran",
                "/user",
                "/semanal",
                "/group",
                "/search",
                "/admin",
                "/corrup",
                "/member",
                "/plugins",
                "/espa",
                "/desabilitar",
                "/users",
                "/wiki",
                "/orgs"
            ],
            "dependencies": [],
            "path": "project-management/atlassian-admin/SKILL.md"
        },
        {
            "id": "atlassian-templates",
            "category": "Project Management",
            "title": "Atlassian Templates",
            "description": "Especialista em criação e modificação de templates e arquivos Atlassian para criação, modificação e gestão de templates Jira e Confluence, blueprints, layouts personalizados, componentes reutilizáveis e estruturas de conteúdo padronizadas. Use ao construir templates em toda a organização, blueprints personalizados, layouts de página e geração automatizada de conteúdo.",
            "triggers": [
                "/conte",
                "/projeto",
                "/atualizada"
            ],
            "dependencies": [],
            "path": "project-management/atlassian-templates/SKILL.md"
        },
        {
            "id": "confluence-expert",
            "category": "Project Management",
            "title": "Confluence Expert",
            "description": "Especialista em Atlassian Confluence para criação e gestão de espaços, bases de conhecimento e documentação. Configura permissões de espaço e hierarquias, cria templates de página com macros, estabelece taxonomias de documentação, projeta layouts de página e gerencia governança de conteúdo. Use quando usuários precisam construir ou reestruturar um espaço Confluence, projetar hierarquias de página com estruturas de permissão, criar ou padronizar templates de documentação, incorporar relatórios Jira em páginas, realizar auditorias de base de conhecimento ou estabelecer padrões de documentação e fluxos de trabalho colaborativos.",
            "triggers": [
                "/estrat",
                "/atlassian-templates",
                "/equipe",
                "/autor",
                "/jira-expert",
                "/importa"
            ],
            "dependencies": [],
            "path": "project-management/confluence-expert/SKILL.md"
        },
        {
            "id": "jira-expert",
            "category": "Project Management",
            "title": "Jira Expert",
            "description": "Especialista em Atlassian Jira para criação e gestão de projetos, planejamento, descoberta de produto, consultas JQL, fluxos de trabalho, campos personalizados, automação, relatórios e todos os recursos do Jira. Use para configuração de projeto Jira, configuração avançada de busca, criação de painéis, design de fluxo de trabalho e operações técnicas do Jira.",
            "triggers": [
                "/tipos",
                "/atlassian-admin",
                "/backlog",
                "/cascata",
                "/confluence-expert",
                "/fluxo"
            ],
            "dependencies": [],
            "path": "project-management/jira-expert/SKILL.md"
        },
        {
            "id": "meeting-analyzer",
            "category": "Project Management",
            "title": "Meeting Analyzer",
            "description": "Analisa transcrições e gravações de reuniões para identificar padrões comportamentais, antipadrões de comunicação e feedback de coaching acionável. Use esta skill sempre que o usuário fizer upload ou apontar para transcrições de reuniões (.txt, .md, .vtt, .srt, .docx), perguntar sobre seus hábitos de comunicação, quiser feedback sobre como conduz reuniões, solicitar análise de proporção de fala, mencionar palavras de preenchimento ou evitação de conflitos, ou quiser comparar sua comunicação ao longo do tempo. Acione também quando os usuários mencionarem ferramentas como Granola, Otter, Fireflies ou transcrições do Zoom. Mesmo que o usuário apenas diga \"olhe minhas reuniões\" ou \"como me apresento nas reuniões\" — use esta skill.",
            "triggers": [
                "/github",
                "/construtoras",
                "/esclarecedoras",
                "/plano",
                "/executive-mentor",
                "/senior-pm",
                "/maximcoding",
                "/indutoras",
                "/scrum-master",
                "/confluence-expert",
                "/100",
                "/compara"
            ],
            "dependencies": [],
            "path": "project-management/meeting-analyzer/SKILL.md"
        },
        {
            "id": "program-manager",
            "category": "Project Management",
            "title": "Program Manager",
            "description": "\"Program Manager sênior para gestão de programas multi-projeto, dependências entre times, RAID log (Risks, Assumptions, Issues, Dependencies), stakeholder management, governança de portfólio, status reporting executivo e entrega de iniciativas estratégicas. Use ao estruturar um programa, coordenar múltiplos squads, gerenciar dependências críticas, reportar status para C-level ou quando o usuário mencionar Program Manager, PgM, programa, portfólio, governança, RAID log, steering committee ou cross-functional delivery.\"",
            "triggers": [
                "/2026",
                "/no-go",
                "/produto",
                "/chats",
                "/c-level-advisor",
                "/go-to-market",
                "/coo-advisor"
            ],
            "dependencies": [],
            "path": "project-management/program-manager/SKILL.md"
        },
        {
            "id": "scrum-master",
            "category": "Project Management",
            "title": "Scrum Master",
            "description": "\"Skill avançada de Scrum Master para análise e coaching de equipes ágeis baseados em dados. Use quando o usuário perguntar sobre planejamento de sprint, rastreamento de velocidade, retrospectivas, facilitação de standup, grooming de backlog, story points, burndown charts, resolução de bloqueadores ou saúde de equipes ágeis. Executa scripts Python para analisar exportações JSON de sprint do Jira ou ferramentas similares: velocity_analyzer.py para previsão Monte Carlo de sprint, sprint_health_scorer.py para pontuação de saúde multidimensional e retrospective_analyzer.py para rastreamento de itens de ação e temas. Produz previsões com intervalo de confiança, relatórios de nota de saúde e tendências de velocidade de melhoria para equipes Scrum de alto desempenho.\"",
            "triggers": [
                "/norming",
                "/agile-product-owner",
                "/sample",
                "/expected",
                "/est",
                "/senior-pm",
                "/performing",
                "/team",
                "/respons",
                "/100",
                "/retrospective",
                "/sprint",
                "/velocity-forecasting-guide",
                "/storming",
                "/velocity",
                "/declining",
                "/team-dynamics-framework"
            ],
            "dependencies": [],
            "path": "project-management/scrum-master/SKILL.md"
        },
        {
            "id": "senior-pm",
            "category": "Project Management",
            "title": "Senior Pm",
            "description": "Gerente de Projetos Sênior para projetos de software empresarial, SaaS e transformação digital. Especializa-se em gestão de portfólio, análise quantitativa de riscos, otimização de recursos, alinhamento de partes interessadas e relatórios executivos. Usa metodologias avançadas incluindo análise de EMV, simulação Monte Carlo, priorização WSJF e pontuação de saúde multidimensional. Use quando o usuário precisa de ajuda com planos de projeto, relatórios de status, avaliações de risco, alocação de recursos, roadmaps de projeto, rastreamento de marcos, planejamento de capacidade da equipe, revisões de saúde de portfólio, gestão de programa ou relatórios de nível executivo — especialmente para iniciativas de escala empresarial com múltiplos fluxos de trabalho, dependências complexas ou orçamentos multimilionários.",
            "triggers": [
                "/portfolio-prioritization-models",
                "/risk",
                "/executive",
                "/sample",
                "/risk-management-framework",
                "/10",
                "/expected",
                "/resource",
                "/portfolio-kpis",
                "/product-strategist",
                "/impacto",
                "/scrum-master",
                "/project",
                "/abordagem",
                "/raci"
            ],
            "dependencies": [],
            "path": "project-management/senior-pm/SKILL.md"
        },
        {
            "id": "team-communications",
            "category": "Project Management",
            "title": "Team Communications",
            "description": "Escreve comunicações internas da empresa — atualizações 3P (Progresso/Planos/Problemas), newsletters corporativas, resumos de FAQ, relatórios de incidentes, atualizações de liderança, relatórios de status, atualizações de projeto e comunicações internas em geral. Use esta skill sempre que o usuário solicitar redigir, editar ou formatar algo destinado a audiências internas. Acione com palavras-chave como \"3P\", \"atualização semanal\", \"newsletter\", \"FAQ\", \"comunicação interna\", \"relatório de status\", \"atualização da empresa\", \"atualização da equipe\", \"relatório de incidente\" ou qualquer solicitação de resumir trabalho para liderança, colegas ou a empresa em geral. Mesmo solicitações casuais como \"escreva minha atualização\" ou \"resuma o que minha equipe fez essa semana\" devem acionar esta skill.",
            "triggers": [
                "/general-comms",
                "/github",
                "/mensal",
                "/faq-answers",
                "/senior-pm",
                "/3p-updates",
                "/maximcoding",
                "/company-newsletter",
                "/confluence-expert",
                "/content-production",
                "/meeting-analyzer"
            ],
            "dependencies": [],
            "path": "project-management/team-communications/SKILL.md"
        }
    ],
    "Ra Qm Team": [
        {
            "id": "capa-officer",
            "category": "Ra Qm Team",
            "title": "Capa Officer",
            "description": "Gestão do sistema CAPA para QMS de dispositivos médicos. Cobre análise de causa raiz, planejamento de ações corretivas, verificação de eficácia e métricas de CAPA. Use para investigações CAPA, análise dos 5 Porquês, diagramas de Ishikawa, determinação de causa raiz, rastreamento de ações corretivas, verificação de eficácia ou otimização do programa de CAPA.",
            "triggers": [
                "/rca-methodologies",
                "/reprovado",
                "/observa",
                "/usu",
                "/avalia",
                "/effectiveness-verification-guide",
                "/capa",
                "/inspe"
            ],
            "dependencies": [],
            "path": "ra-qm-team/capa-officer/SKILL.md"
        },
        {
            "id": "fda-consultant-specialist",
            "category": "Ra Qm Team",
            "title": "Fda Consultant Specialist",
            "description": "Consultor regulatório FDA para empresas de dispositivos médicos. Fornece orientação sobre vias 510(k)/PMA/De Novo, conformidade QSR (21 CFR 820), avaliações HIPAA e cibersegurança de dispositivos. Use quando o usuário mencionar submissão FDA, 510(k), PMA, De Novo, QSR, pré-mercado, dispositivo predicado, equivalência substancial, HIPAA para dispositivos médicos ou cibersegurança FDA.",
            "triggers": [
                "/path",
                "/qsr",
                "/padr",
                "/device",
                "/hipaa",
                "/to",
                "/desempenho",
                "/project",
                "/preventivas",
                "/internet",
                "/fda"
            ],
            "dependencies": [],
            "path": "ra-qm-team/fda-consultant-specialist/SKILL.md"
        },
        {
            "id": "gdpr-dsgvo-expert",
            "category": "Ra Qm Team",
            "title": "Gdpr Dsgvo Expert",
            "description": "Automação de conformidade com LGPD (Lei 13.709/2018), GDPR e DSGVO alemã. Escaneia bases de código em busca de riscos de privacidade, gera documentação DPIA, rastreia solicitações de direitos dos titulares de dados. Use para avaliações de conformidade LGPD/GDPR, auditorias de privacidade, planejamento de proteção de dados, geração de DPIA e gestão de direitos dos titulares de dados — com foco no mercado brasileiro.",
            "triggers": [
                "/path",
                "/pesquisa",
                "/german",
                "/gdpr",
                "/2018",
                "/to",
                "/dpia",
                "/project",
                "/code",
                "/data"
            ],
            "dependencies": [],
            "path": "ra-qm-team/gdpr-dsgvo-expert/SKILL.md"
        },
        {
            "id": "information-security-manager-iso27001",
            "category": "Ra Qm Team",
            "title": "Information Security Manager Iso27001",
            "description": "Implementação de ISMS ISO 27001 e governança de cibersegurança para empresas HealthTech e MedTech. Use para design de ISMS, avaliação de riscos de segurança, implementação de controles, certificação ISO 27001, auditorias de segurança, resposta a incidentes e verificação de conformidade. Cobre ISO 27001, ISO 27002, segurança em saúde e cibersegurança de dispositivos médicos — com foco no mercado brasileiro.",
            "triggers": [
                "/risk",
                "/cr",
                "/risk-assessment-guide",
                "/externas",
                "/27002",
                "/incidente-response",
                "/compliance",
                "/iso27001-controls"
            ],
            "dependencies": [],
            "path": "ra-qm-team/information-security-manager-iso27001/SKILL.md"
        },
        {
            "id": "isms-audit-expert",
            "category": "Ra Qm Team",
            "title": "Isms Audit Expert",
            "description": "Especialista em auditoria de Sistema de Gestão de Segurança da Informação (ISMS) para verificação de conformidade ISO 27001, avaliação de controles de segurança e suporte à certificação. Use quando o usuário mencionar ISO 27001, auditoria ISMS, controles do Anexo A, Declaração de Aplicabilidade (SoA), análise de lacunas, gestão de não conformidades, auditoria interna, auditoria de vigilância ou preparação para certificação de segurança.",
            "triggers": [
                "/isms",
                "/cloud-security-audit",
                "/security-control-testing",
                "/iso27001-audit-methodology"
            ],
            "dependencies": [],
            "path": "ra-qm-team/isms-audit-expert/SKILL.md"
        },
        {
            "id": "mdr-745-specialist",
            "category": "Ra Qm Team",
            "title": "Mdr 745 Specialist",
            "description": "Especialista em conformidade EU MDR 2017/745 para classificação de dispositivos médicos, documentação técnica, evidência clínica e vigilância pós-mercado. Cobre regras de classificação do Anexo VIII, arquivos técnicos dos Anexos II/III, avaliação clínica do Anexo XIV e integração EUDAMED.",
            "triggers": [
                "/de",
                "/745",
                "/clinical-evidence-requirements",
                "/technical-documentation-templates",
                "/trata",
                "/mdr-classification-guide",
                "/card",
                "/mdr"
            ],
            "dependencies": [],
            "path": "ra-qm-team/mdr-745-specialist/SKILL.md"
        },
        {
            "id": "qms-audit-expert",
            "category": "Ra Qm Team",
            "title": "Qms Audit Expert",
            "description": "Especialista em auditoria interna ISO 13485 para QMS de dispositivos médicos. Cobre planejamento de auditoria, execução, classificação de não conformidades e verificação de CAPA. Use para planejamento de auditoria interna, execução de auditoria, classificação de achados, preparação para auditoria externa ou gestão do programa de auditoria.",
            "triggers": [
                "/nonconformity-classification",
                "/audit",
                "/iso13485-audit-guide"
            ],
            "dependencies": [],
            "path": "ra-qm-team/qms-audit-expert/SKILL.md"
        },
        {
            "id": "quality-documentation-manager",
            "category": "Ra Qm Team",
            "title": "Quality Documentation Manager",
            "description": "Gestão do sistema de controle de documentos para QMS de dispositivos médicos. Cobre numeração de documentos, controle de versão, gestão de mudanças e conformidade com 21 CFR Part 11. Use para procedimentos de controle de documentos, fluxo de trabalho de controle de mudanças, numeração de documentos, gestão de versões, conformidade de assinatura eletrônica ou revisão de documentação regulatória.",
            "triggers": [
                "/projeto",
                "/document",
                "/document-control-procedures",
                "/distribui",
                "/novos",
                "/conformidade",
                "/21cfr11-compliance-guide",
                "/papel",
                "/preventivas",
                "/processo",
                "/hora"
            ],
            "dependencies": [],
            "path": "ra-qm-team/quality-documentation-manager/SKILL.md"
        },
        {
            "id": "quality-manager-qmr",
            "category": "Ra Qm Team",
            "title": "Quality Manager Qmr",
            "description": "Gerente de Qualidade Sênior — Representante da Direção (RD/QMR) para empresas HealthTech e MedTech. Fornece governança do sistema da qualidade, liderança de revisão gerencial, supervisão de conformidade regulatória e monitoramento de desempenho da qualidade conforme a ISO 13485 Cláusula 5.5.2 — com foco no mercado brasileiro.",
            "triggers": [
                "/2013",
                "/management",
                "/sa",
                "/745",
                "/quality-manager-qms-iso13485",
                "/quality-kpi-framework",
                "/quality-documentation-manager",
                "/capa-officer",
                "/qms-audit-expert",
                "/rejeitar",
                "/management-review-guide"
            ],
            "dependencies": [],
            "path": "ra-qm-team/quality-manager-qmr/SKILL.md"
        },
        {
            "id": "quality-manager-qms-iso13485",
            "category": "Ra Qm Team",
            "title": "Quality Manager Qms Iso13485",
            "description": "Implementação e manutenção de Sistema de Gestão da Qualidade ISO 13485 para organizações de dispositivos médicos. Fornece design do QMS, controle de documentação, auditoria interna, gestão de CAPA e suporte à certificação. Use ao trabalhar com sistemas de qualidade de dispositivos médicos, preparar para auditorias ISO 13485, gerenciar documentação de conformidade regulatória, configurar ações corretivas ou construir programas de preparação para auditoria — com foco no mercado brasileiro e ANVISA.",
            "triggers": [
                "/qms",
                "/iso13485-clause-requirements",
                "/quality-manager-qmr",
                "/capa-officer",
                "/desempenho",
                "/qms-audit-expert",
                "/risk-management-specialist",
                "/quality-documentation-manager",
                "/qms-process-templates"
            ],
            "dependencies": [],
            "path": "ra-qm-team/quality-manager-qms-iso13485/SKILL.md"
        },
        {
            "id": "regulatory-affairs-head",
            "category": "Ra Qm Team",
            "title": "Regulatory Affairs Head",
            "description": "Gerente Sênior de Assuntos Regulatórios para empresas HealthTech e MedTech. Prepara pacotes de submissão FDA 510(k), De Novo e PMA; analisa vias regulatórias para novos dispositivos médicos; redige respostas a cartas de deficiência FDA e consultas de Organismos Notificados; desenvolve documentação técnica de marcação CE sob EU MDR 2017/745; coordena estratégias de aprovação em múltiplos mercados incluindo FDA, UE, ANVISA (Brasil), Health Canada, PMDA e NMPA; e mantém inteligência regulatória sobre normas em evolução. Use quando usuários precisarem planejar ou executar submissões FDA, navegar pelos processos de aprovação 510(k) ou PMA, obter marcação CE, preparar materiais para reunião de pré-submissão, redigir documentos de estratégia regulatória, responder a consultas de agências ou gerenciar documentação de conformidade para acesso ao mercado de dispositivos médicos.",
            "triggers": [
                "/mdr-745-specialist",
                "/reprovado",
                "/745",
                "/quality-manager-qms-iso13485",
                "/efic",
                "/representante",
                "/iso-regulatory-requirements",
                "/notifica",
                "/regulatory",
                "/global-regulatory-pathways",
                "/eu-mdr-submission-guide",
                "/fda-consultant-specialist",
                "/risk-management-specialist",
                "/fda-submission-guide"
            ],
            "dependencies": [],
            "path": "ra-qm-team/regulatory-affairs-head/SKILL.md"
        },
        {
            "id": "risk-management-specialist",
            "category": "Ra Qm Team",
            "title": "Risk Management Specialist",
            "description": "Especialista em gestão de riscos de dispositivos médicos, implementando a ISO 14971 ao longo do ciclo de vida do produto. Fornece análise de riscos, avaliação de riscos, controle de riscos e análise de informações pós-produção. Use quando o usuário mencionar gestão de riscos, ISO 14971, análise de riscos, FMEA, análise de árvore de falhas, identificação de perigos, controle de riscos, matriz de riscos, análise benefício-risco, risco residual, aceitabilidade de riscos ou risco pós-mercado.",
            "triggers": [
                "/de",
                "/risk",
                "/eventos",
                "/risk-assessment-templates",
                "/quality-manager-qms-iso13485",
                "/quality-documentation-manager",
                "/capa-officer",
                "/regulatory-affairs-head",
                "/iso14971-implementation-guide",
                "/risk-analysis-methods",
                "/fun"
            ],
            "dependencies": [],
            "path": "ra-qm-team/risk-management-specialist/SKILL.md"
        },
        {
            "id": "soc2-compliance",
            "category": "Ra Qm Team",
            "title": "Soc2 Compliance",
            "description": "\"Use quando o usuário pedir para preparar auditorias SOC 2, mapear Critérios de Serviço de Confiança, construir matrizes de controles, coletar evidências de auditoria, realizar análise de lacunas ou avaliar a prontidão para SOC 2 Tipo I versus Tipo II.\"",
            "triggers": [
                "/isms-audit-expert",
                "/evidence",
                "/gap",
                "/alta",
                "/type1",
                "/parceiros",
                "/externa",
                "/equipe",
                "/armazena",
                "/information-security-manager-iso27001",
                "/gdpr-dsgvo-expert",
                "/procedimentos",
                "/neg",
                "/falha",
                "/trust",
                "/hora",
                "/control",
                "/opt-out"
            ],
            "dependencies": [
                "Information Security Manager Iso27001",
                "Isms Audit Expert",
                "Gdpr Dsgvo Expert"
            ],
            "path": "ra-qm-team/soc2-compliance/SKILL.md"
        }
    ],
    "Rotina Organizacao": [
        {
            "id": "bloqueio-de-tempo",
            "category": "Rotina Organizacao",
            "title": "Bloqueio De Tempo",
            "description": "\"Planejamento de agenda com time blocking, deep work, temas do dia e agrupamento de reuniões. Framework para criar semana ideal com blocos de foco protegidos, tempo de buffer e rotinas fixas.\"",
            "triggers": [
                "/read",
                "/rules",
                "/time-blocking",
                "/review",
                "/skill",
                "/sem",
                "/muitas"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/bloqueio-de-tempo/SKILL.md"
        },
        {
            "id": "caixa-de-entrada-zero",
            "category": "Rotina Organizacao",
            "title": "Caixa De Entrada Zero",
            "description": "\"Gestão de email e notificações para inbox zero: sistema de triagem, resposta e arquivamento de emails, gestão de notificações de WhatsApp e Slack, e como manter o inbox limpo de forma sustentável.\"",
            "triggers": [
                "/inbox-zero",
                "/read",
                "/rules",
                "/skill",
                "/decis"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/caixa-de-entrada-zero/SKILL.md"
        },
        {
            "id": "criador-de-checklists",
            "category": "Rotina Organizacao",
            "title": "Criador De Checklists",
            "description": "\"Criação de checklists, SOPs pessoais e rotinas repetíveis: estruturação de procedimentos para tarefas recorrentes, onboarding, fechamentos de projeto e processos que precisam de consistência garantida.\"",
            "triggers": [
                "/read",
                "/checklist-builder",
                "/mensal",
                "/rules",
                "/ad-hoc",
                "/skill",
                "/semanal"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/criador-de-checklists/SKILL.md"
        },
        {
            "id": "delegacao",
            "category": "Rotina Organizacao",
            "title": "Delegacao",
            "description": "\"Frameworks de delegação eficaz para líderes e donos de negócio: como escolher o que delegar, preparar o delegado, criar sistema de acompanhamento e sair do microgerenciamento sem perder controle de qualidade.\"",
            "triggers": [
                "/read",
                "/rules",
                "/delegacao",
                "/skill"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/delegacao/SKILL.md"
        },
        {
            "id": "equilibrio-vida",
            "category": "Rotina Organizacao",
            "title": "Equilibrio Vida",
            "description": "\"Work-life balance, prevenção de burnout e saúde mental do trabalho: identificar sinais de burnout, criar limites saudáveis sem prejudicar a carreira, técnicas de recuperação e como sustentar alta performance no longo prazo.\"",
            "triggers": [
                "/emprego",
                "/read",
                "/clientes",
                "/equilibrio-vida",
                "/rules",
                "/skill",
                "/dia"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/equilibrio-vida/SKILL.md"
        },
        {
            "id": "foco-e-trabalho-profundo",
            "category": "Rotina Organizacao",
            "title": "Foco E Trabalho Profundo",
            "description": "\"Técnicas de foco profundo: Deep Work (Cal Newport), Pomodoro adaptado, Flow State, eliminação de distrações digitais e design de ambiente para trabalho cognitivo intenso no contexto brasileiro.\"",
            "triggers": [
                "/fam",
                "/read",
                "/foco-deep-work",
                "/microfone",
                "/escrit",
                "/rules",
                "/skill",
                "/dia"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/foco-e-trabalho-profundo/SKILL.md"
        },
        {
            "id": "habitos",
            "category": "Rotina Organizacao",
            "title": "Habitos",
            "description": "\"Criação e manutenção de hábitos com Atomic Habits e habit stacking: como projetar ambiente para facilitar bons hábitos, estratégias de consistência, recuperação de falhas e como quebrar hábitos ruins.\"",
            "triggers": [
                "/read",
                "/rules",
                "/habitos",
                "/skill"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/habitos/SKILL.md"
        },
        {
            "id": "prioridades",
            "category": "Rotina Organizacao",
            "title": "Prioridades",
            "description": "\"Frameworks de priorização pessoal: Matriz de Eisenhower, RICE pessoal, princípio 80/20 e regra das 3 prioridades. Para profissionais que fazem tudo mas nunca o mais importante.\"",
            "triggers": [
                "/read",
                "/prioridades",
                "/energia",
                "/20",
                "/rules",
                "/skill"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/prioridades/SKILL.md"
        },
        {
            "id": "revisao-semanal",
            "category": "Rotina Organizacao",
            "title": "Revisao Semanal",
            "description": "\"Revisão semanal completa: processamento de capturas, revisão de projetos em aberto, definição de próximas ações prioritárias e planejamento da semana seguinte. Template adaptado para o profissional brasileiro.\"",
            "triggers": [
                "/read",
                "/rules",
                "/skill",
                "/papel",
                "/etc",
                "/weekly-review"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/revisao-semanal/SKILL.md"
        },
        {
            "id": "sistema-gtd",
            "category": "Rotina Organizacao",
            "title": "Sistema Gtd",
            "description": "\"Implementação do método GTD (Getting Things Done) adaptado à realidade brasileira: configuração das caixas de coleta, processamento de inbox, listas de próximas ações e revisão semanal com ferramentas digitais e analógicas.\"",
            "triggers": [
                "/read",
                "/gtd-system",
                "/rules",
                "/skill",
                "/papel"
            ],
            "dependencies": [],
            "path": "rotina-organizacao/sistema-gtd/SKILL.md"
        }
    ],
    "Seo Analitica": [
        {
            "id": "analise-de-coortes",
            "category": "Seo Analitica",
            "title": "Analise De Coortes",
            "description": "\"Análise de coortes, retenção e LTV de usuários para SaaS e e-commerce\"",
            "triggers": [],
            "dependencies": [],
            "path": "seo-analitica/analise-de-coortes/SKILL.md"
        },
        {
            "id": "bi-indicadores",
            "category": "Seo Analitica",
            "title": "Bi Indicadores",
            "description": "\"KPIs e indicadores de negócio para PMEs brasileiras: fórmulas e benchmarks\"",
            "triggers": [
                "/ano",
                "/estrat"
            ],
            "dependencies": [],
            "path": "seo-analitica/bi-indicadores/SKILL.md"
        },
        {
            "id": "dados-lgpd",
            "category": "Seo Analitica",
            "title": "Dados Lgpd",
            "description": "\"Coleta, armazenamento e uso de dados em conformidade com a LGPD brasileira\"",
            "triggers": [
                "/2018"
            ],
            "dependencies": [],
            "path": "seo-analitica/dados-lgpd/SKILL.md"
        },
        {
            "id": "google-analytics",
            "category": "Seo Analitica",
            "title": "Google Analytics",
            "description": "\"Configuração e análise no GA4 com eventos customizados para negócios brasileiros\"",
            "triggers": [],
            "dependencies": [],
            "path": "seo-analitica/google-analytics/SKILL.md"
        },
        {
            "id": "google-search-console",
            "category": "Seo Analitica",
            "title": "Google Search Console",
            "description": "\"Google Search Console para diagnóstico SEO e oportunidades de ranking\"",
            "triggers": [],
            "dependencies": [],
            "path": "seo-analitica/google-search-console/SKILL.md"
        },
        {
            "id": "pesquisa-de-palavras-chave",
            "category": "Seo Analitica",
            "title": "Pesquisa De Palavras Chave",
            "description": "\"Pesquisa de palavras-chave para busca brasileira com volume e intenção de busca\"",
            "triggers": [],
            "dependencies": [],
            "path": "seo-analitica/pesquisa-de-palavras-chave/SKILL.md"
        },
        {
            "id": "rastreamento-utm",
            "category": "Seo Analitica",
            "title": "Rastreamento Utm",
            "description": "\"Estratégia de UTMs, rastreamento de campanhas e atribuição de conversões\"",
            "triggers": [],
            "dependencies": [],
            "path": "seo-analitica/rastreamento-utm/SKILL.md"
        },
        {
            "id": "relatorio-dados",
            "category": "Seo Analitica",
            "title": "Relatorio Dados",
            "description": "\"Criação de relatórios e dashboards executivos com dados reais de marketing digital\"",
            "triggers": [
                "/cliente",
                "/operacional",
                "/diretoria"
            ],
            "dependencies": [],
            "path": "seo-analitica/relatorio-dados/SKILL.md"
        },
        {
            "id": "seo-tecnico",
            "category": "Seo Analitica",
            "title": "Seo Tecnico",
            "description": "\"Auditoria SEO técnica: Core Web Vitals, indexação, schema markup e correções prioritárias\"",
            "triggers": [
                "/complexo"
            ],
            "dependencies": [],
            "path": "seo-analitica/seo-tecnico/SKILL.md"
        },
        {
            "id": "testes-ab",
            "category": "Seo Analitica",
            "title": "Testes Ab",
            "description": "\"Planejamento e análise estatística de testes A/B para otimização de conversão\"",
            "triggers": [],
            "dependencies": [],
            "path": "seo-analitica/testes-ab/SKILL.md"
        }
    ]
};