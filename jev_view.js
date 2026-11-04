// Jev — A IA que Decide (TypeSafe System One) View
window.initJevView = window.createStandardToolView({
    containerId: 'jev-view',
    dataKey: 'jevData',
    globalVarName: 'jevView',
    themeColor: '#00c9a7',
    badgeText: 'TypeSafe System One · Flowgrammers',
    title: '⚡ Jev — A IA que Decide (Sistema 1)',
    description: 'O primeiro modelo comercial <strong>Sistema 1 para Software</strong> (<code>jev-latest</code>): não conversa e não gera prosa — apenas <strong>decide (<code>choice</code>)</strong>, <strong>pontua (<code>score</code>)</strong> e <strong>extrai (<code>noul</code>)</strong> em <strong>70 a 500ms</strong> por <strong>US$ 0,042 / 1M input tokens</strong> (output grátis). Inclui guia completo da aula Mastermind Flowgrammers, Hook <code>PreToolUse</code> para Claude Code e os <strong>2 workflows n8n prontos para download</strong>.',
    repoUrl: 'https://typesafe.ai',
    statsHtml: `
        <div style="background:#f3f2f1; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600; color:#323130;">⚡ <strong>70–500 ms</strong> Latência</div>
        <div style="background:#e6fcf5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600; color:#087f5b;">💰 <strong>$0.042/1M</strong> Input (Output Grátis)</div>
        <div style="background:#f3f2f1; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600; color:#323130;">🧩 <strong>3 Primitivas:</strong> choice · score · noul</div>
        <div style="background:#fff0f6; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600; color:#c2255c;">⚙️ <strong>2 Workflows n8n</strong> + Hook Claude Code</div>
    `,
    categories: [
        { id: 'all', label: 'Todos', icon: '⚡' },
        { id: 'concepts', label: 'Fundamentos (Sistema 1)', icon: '🧠' },
        { id: 'api', label: 'API & Primitivas', icon: '🔌' },
        { id: 'claude-code', label: 'Claude Code & Browser', icon: '🛡️' },
        { id: 'n8n', label: 'Workflows n8n', icon: '⚙️' }
    ],
    cheatsheet: {
        tabLabel: 'Cheatsheet & cURL',
        tabIcon: '🚀',
        title: '🚀 Guia Rápido — Jev API, Claude Code Hook & n8n',
        subtitle: 'Comandos prontos para chamar o endpoint /v1/systemone, configurar o Hook PreToolUse no Claude Code e abrir a apresentação interativa de 43 slides.',
        cards: [
            {
                title: '1. Chamada Direta via cURL (choice + score + noul)',
                badge: 'POST /v1/systemone',
                badgeBg: '#e6fcf5',
                badgeColor: '#087f5b',
                description: 'Avalie múltiplas decisões estruturadas de uma só vez com latência de Sistema 1 (~150ms):',
                code: `curl -X POST https://api.typesafe.ai/v1/systemone \\
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "jev-latest",
    "context": "Cliente: Meu checkout está retornando erro 502 desde as 14h!",
    "decisions": [
      { "name": "fila", "type": "choice", "prompt": "Qual fila?", "options": ["suporte_n1", "engenharia_critica", "financeiro"] },
      { "name": "urgencia", "type": "score", "prompt": "Urgência de 0 a 1" },
      { "name": "erro_http", "type": "noul", "prompt": "Qual código HTTP de erro foi citado?" }
    ]
  }'`,
                footer: 'Retorna JSON determinístico em results: { fila, urgencia, erro_http }.'
            },
            {
                title: '2. Ativar o Guardrail no Claude Code (.claude/settings.json)',
                badge: 'Claude Code Hook',
                badgeBg: '#eef2ff',
                badgeColor: '#4338ca',
                description: 'Baixe o script jev/jev_gate.py desta aba e configure seu .claude/settings.json:',
                code: `export TYPESAFE_API_KEY="ts_live_sua_chave_aqui"
mkdir -p .claude/hooks
cp jev/jev_gate.py .claude/hooks/jev_gate.py
chmod +x .claude/hooks/jev_gate.py`,
                footer: 'Comandos seguros recebem allow em ~150ms; comandos perigosos recebem deny automático.'
            },
            {
                title: '3. Importar os 2 Workflows no n8n + Ver Apresentação de 43 Slides',
                badge: 'Mastermind Flowgrammers',
                badgeBg: '#fff0f6',
                badgeColor: '#c2255c',
                description: 'Os 2 workflows JSON já estão disponíveis tanto nesta ferramenta (aba Workflows n8n) quanto em Templates n8n, e o deck interativo completo está em Apresentações:',
                code: `# Arquivos prontos para importar no n8n:
jev/flowgrammers-jev-triagem-alunos.json
jev/flowgrammers-jev-benchmark.json

# Apresentação Interativa (43 slides + botões de download):
contexto/jev_ia_que_decide.html`,
                footer: 'Acesse também pelo menu lateral: Apresentações -> ⚡ Jev: A IA que Decide (Flowgrammers).'
            }
        ]
    }
});
