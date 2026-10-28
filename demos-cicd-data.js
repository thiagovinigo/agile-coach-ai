const demosCicdData = {
    "GUIA DE SETUP & WORKFLOW (GITHUB ACTIONS)": [
        {
            id: "cicd-readme",
            title: "README: Passo a Passo Completo (macOS & Windows)",
            description: "Guia oficial da demo: setup com gh CLI, Warmup Local vs GitHub Actions, criação do PR de teste, troubleshooting e variações com subagentes.",
            icon: "📖",
            path: "demos-cicd/README.md"
        },
        {
            id: "cicd-workflow-yml",
            title: ".github/workflows/claude-review.yml (Workflow GitHub Actions)",
            description: "Workflow real que dispara em todo pull_request (opened, synchronize, reopened), configura permissões pull-requests: write, faz checkout completo (fetch-depth: 0) e injeta os SHAs no script Python.",
            icon: "⚙️",
            path: "demos-cicd/.github/workflows/claude-review.yml"
        },
        {
            id: "cicd-requirements",
            title: "requirements.txt (Dependência Mínima)",
            description: "Dependência única do bot de code review: SDK oficial da Anthropic (anthropic>=0.40.0).",
            icon: "📦",
            path: "demos-cicd/requirements.txt"
        }
    ],
    "BOT DE CODE REVIEW (WARMUP LOCAL VS RUNNER CI/CD)": [
        {
            id: "cicd-local-review",
            title: "1. local_review.py (Warmup 100% Local na Máquina)",
            description: "Roda o revisor sênior localmente sobre um diff fictício de checkout.py usando Claude Haiku 4.5 com retry exponencial, sem precisar subir nada pro GitHub.",
            icon: "🏠",
            path: "demos-cicd/local_review.py"
        },
        {
            id: "cicd-review-pr",
            title: "2. .github/scripts/review_pr.py (Bot de Produção no Runner)",
            description: "Script executado dentro do GitHub Actions: extrai o git diff entre BASE_SHA e HEAD_SHA (com truncamento de segurança em 30.000 chars), chama o Claude Haiku e posta o comentário no PR via gh pr comment.",
            icon: "🤖",
            path: "demos-cicd/.github/scripts/review_pr.py"
        }
    ],
    "MASSA DE TESTE (BUGS PLANTADOS PARA PR)": [
        {
            id: "cicd-example-bug",
            title: "example-bug.py (Carrinho de Compras com 4 Bugs Sutis)",
            description: "Arquivo preparado para abrir um PR de teste e ver o bot do Claude detectar: chamada de método sem parênteses (self.total), divisão por zero em carrinho vazio e falta de validação de desconto negativo.",
            icon: "🐛",
            path: "demos-cicd/example-bug.py"
        }
    ]
};
