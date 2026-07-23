const pmSkillsData = {
    "VISÃO GERAL": [
        { id: "como-usar", title: "00. Guia Rápido", description: "Como usar o PM Assistant e regras de encadeamento.", icon: "📖", path: "assets/pm-skills/00-como-usar.md" },
        { id: "zero-a-um", title: "01. Do Zero ao Um", description: "O guia definitivo para Product Managers: Da Ideia ao Product-Market Fit.", icon: "🚀", path: "assets/pm-skills/01-zero-a-um.md" },
        { id: "um-a-cem", title: "02. Do Um ao Cem", description: "Escalar produto com o PM Assistant: Estratégia, growth e comunicação.", icon: "📈", path: "assets/pm-skills/02-um-a-cem.md" },
        { id: "workflows", title: "03. Workflows Prontos", description: "7 receitas prontas encadeando skills para cenários reais de PM.", icon: "🔄", path: "assets/pm-skills/03-workflows.md" },
        { id: "skills-por-aula", title: "04. Skills por Aula", description: "Mapeamento das skills baseadas nas aulas teóricas.", icon: "🎓", path: "assets/pm-skills/04-skills-por-aula.md" }
    ],
    "DISCOVERY": [
        { id: "persona", title: "/persona", description: "Gera persona detalhada com jobs-to-be-done, dores e comportamentos.", icon: "👤", path: "pm-skills-claude-code/.claude/commands/persona.md" },
        { id: "discovery", title: "/discovery", description: "Estrutura plano de discovery com hipóteses e métodos de pesquisa.", icon: "🔬", path: "pm-skills-claude-code/.claude/commands/discovery.md" },
        { id: "interview-synthesis", title: "/interview-synthesis", description: "Sintetiza entrevistas em padrões, insights e recomendações.", icon: "🎙️", path: "pm-skills-claude-code/.claude/commands/interview-synthesis.md" },
        { id: "competitive-analysis", title: "/competitive-analysis", description: "Análise competitiva estruturada com posicionamento e gaps.", icon: "⚔️", path: "pm-skills-claude-code/.claude/commands/competitive-analysis.md" },
        { id: "opportunity-tree", title: "/opportunity-tree", description: "Monta árvore de oportunidades (Opportunity Solution Tree).", icon: "🌳", path: "pm-skills-claude-code/.claude/commands/opportunity-tree.md" },
        { id: "hypothesis", title: "/hypothesis", description: "Formula hipóteses testáveis no formato 'Se X, então Y, medido por Z'.", icon: "🧪", path: "pm-skills-claude-code/.claude/commands/hypothesis.md" },
        { id: "customer-journey", title: "/customer-journey", description: "Mapeia jornada do cliente com touchpoints, emoções e gaps.", icon: "🗺️", path: "pm-skills-claude-code/.claude/commands/customer-journey.md" }
    ],
    "DELIVERY": [
        { id: "prd", title: "/prd", description: "Gera PRD completo com problema, solução, métricas e escopo.", icon: "📄", path: "pm-skills-claude-code/.claude/commands/prd.md" },
        { id: "user-stories", title: "/user-stories", description: "Quebra PRD em user stories com critérios de aceite.", icon: "📝", path: "pm-skills-claude-code/.claude/commands/user-stories.md" },
        { id: "acceptance-criteria", title: "/acceptance-criteria", description: "Detalha critérios de aceite para uma story específica.", icon: "✅", path: "pm-skills-claude-code/.claude/commands/acceptance-criteria.md" }
    ],
    "STRATEGY": [
        { id: "prioritize", title: "/prioritize", description: "Aplica frameworks de priorização (RICE, ICE, MoSCoW) ao backlog.", icon: "⚖️", path: "pm-skills-claude-code/.claude/commands/prioritize.md" },
        { id: "strategy", title: "/strategy", description: "Define estratégia de produto com visão, positioning e moats.", icon: "🎯", path: "pm-skills-claude-code/.claude/commands/strategy.md" },
        { id: "roadmap", title: "/roadmap", description: "Gera roadmap orientado a outcomes, não features.", icon: "🛣️", path: "pm-skills-claude-code/.claude/commands/roadmap.md" },
        { id: "okr", title: "/okr", description: "Define OKRs com objetivos e key results mensuráveis.", icon: "📊", path: "pm-skills-claude-code/.claude/commands/okr.md" },
        { id: "lean-canvas", title: "/lean-canvas", description: "Gera Lean Canvas completo para um produto ou feature.", icon: "🖼️", path: "pm-skills-claude-code/.claude/commands/lean-canvas.md" },
        { id: "pricing", title: "/pricing", description: "Estrutura estratégia de pricing com tiers e justificativa.", icon: "💰", path: "pm-skills-claude-code/.claude/commands/pricing.md" },
        { id: "north-star", title: "/north-star", description: "Define North Star Metric com input metrics e leading indicators.", icon: "⭐", path: "pm-skills-claude-code/.claude/commands/north-star.md" }
    ],
    "VALIDATION": [
        { id: "experiment-design", title: "/experiment-design", description: "Desenha experimento com hipótese, métrica, critério de sucesso.", icon: "📐", path: "pm-skills-claude-code/.claude/commands/experiment-design.md" },
        { id: "measure-pmf", title: "/measure-pmf", description: "Avalia Product-Market Fit com frameworks (Sean Ellis, retenção).", icon: "📈", path: "pm-skills-claude-code/.claude/commands/measure-pmf.md" },
        { id: "ab-test-analysis", title: "/ab-test-analysis", description: "Analisa resultado de A/B test com significância e recomendação.", icon: "🔍", path: "pm-skills-claude-code/.claude/commands/ab-test-analysis.md" }
    ],
    "EXECUTION": [
        { id: "pre-mortem", title: "/pre-mortem", description: "Lista riscos e mitigações antes do lançamento.", icon: "☠️", path: "pm-skills-claude-code/.claude/commands/pre-mortem.md" },
        { id: "launch-checklist", title: "/launch-checklist", description: "Checklist completo de lançamento por área (eng, marketing, CS).", icon: "📋", path: "pm-skills-claude-code/.claude/commands/launch-checklist.md" }
    ],
    "COMMUNICATION & GTM": [
        { id: "release-notes", title: "/release-notes", description: "Gera release notes claras para diferentes audiências.", icon: "📣", path: "pm-skills-claude-code/.claude/commands/release-notes.md" },
        { id: "stakeholder-update", title: "/stakeholder-update", description: "Estrutura update executivo com progresso, riscos e asks.", icon: "👔", path: "pm-skills-claude-code/.claude/commands/stakeholder-update.md" },
        { id: "gtm", title: "/gtm", description: "Plano de go-to-market com canais, messaging e timeline.", icon: "🚀", path: "pm-skills-claude-code/.claude/commands/gtm.md" },
        { id: "battlecard", title: "/battlecard", description: "Gera battlecard de vendas com comparativo competitivo.", icon: "🛡️", path: "pm-skills-claude-code/.claude/commands/battlecard.md" },
        { id: "ideal-customer-profile", title: "/ideal-customer-profile", description: "Define ICP detalhado com firmographics e sinais de compra.", icon: "🎯", path: "pm-skills-claude-code/.claude/commands/ideal-customer-profile.md" }
    ]
};
