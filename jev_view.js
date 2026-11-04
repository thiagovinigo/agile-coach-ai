document.addEventListener('DOMContentLoaded', () => {
    initJevView();
});

function initJevView() {
    if (typeof jevData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'jev-view',
        title: 'Jev — A IA que Decide (Sistema 1 · TypeSafe)',
        badge: 'Mastermind Flowgrammers · Ric Neves',
        icon: '⚡',
        tagline: 'Sistema 1 para Software — De Daniel Kahneman ao Claude Code e ao n8n (70–500ms · US$ 0,042/1M input · output grátis)',
        description: 'O <strong>Jev (<code>jev-latest</code> · TypeSafe AI)</strong> é o primeiro modelo comercial projetado especificamente como <strong>Sistema 1 para software</strong>: ele não conversa e não gera prosa — apenas <strong>decide (<code>choice</code>)</strong>, <strong>pontua (<code>score</code>)</strong> e <strong>extrai (<code>noul</code>)</strong> em <strong>70 a 500ms</strong> por uma fração de centavo. Inclui toda a documentação da aula Mastermind Flowgrammers, o hook <code>jev_gate.py</code> para Claude Code e os <strong>2 workflows n8n prontos para download</strong>.',
        themeColor: '#00c9a7',
        themeGradient: 'linear-gradient(135deg, #042f2e 0%, #0f172a 60%, #115e59 100%)',
        githubRepo: 'https://typesafe.ai',
        itemType: 'Jev Sistema 1',
        pills: [
            { text: '🌐 TypeSafe AI (typesafe.ai)', link: 'https://typesafe.ai' },
            { text: '🎓 Abrir Apresentação Interativa (43 Slides)', link: '#flowgrammers-jev' },
            { text: '⚡ Latência: 70–500 ms (Sistema 1)' },
            { text: '💰 US$ 0,042 / 1M Input · Output Grátis' },
            { text: '🧩 3 Primitivas: choice · score · noul' },
            { text: '⚙️ 2 Workflows n8n + Hook Claude Code' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Catálogo Completo Jev (10)' },
            { id: '1. Fundamentos', label: '🧠 Sistema 1 vs Sistema 2 (2)' },
            { id: '2. API Reference', label: '🔌 API & Primitivas (1)' },
            { id: '3. Claude Code', label: '🛡️ Claude Code Hook & Browser (4)' },
            { id: '4. Workflows n8n', label: '⚙️ Workflows n8n & Regra de Ouro (3)' },
            { id: 'cheatsheet', label: '🚀 Cheatsheet cURL, Hook & n8n' }
        ],
        data: jevData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>⚡</span> Jev (Sistema 1) — Guia Rápido de API, Claude Code Hook & n8n
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Como chamar <code>POST https://api.typesafe.ai/v1/systemone</code>, ativar o guardrail no Claude Code e importar os 2 workflows no n8n.
                    </p>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #00c9a7;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🔌</span> 1. Chamada Multi-Decisão em 150ms (<code>choice</code> + <code>score</code> + <code>noul</code>)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Envie várias decisões no mesmo array <code>decisions</code> — o output é gratuito e retorna JSON determinístico:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>cURL · POST /v1/systemone</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>curl -X POST https://api.typesafe.ai/v1/systemone \\
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "jev-latest",
    "context": "Aluno: Meu webhook do n8n parou em produção durante o lançamento!",
    "decisions": [
      { "name": "area", "type": "choice", "prompt": "Qual área?", "options": ["acesso", "n8n_automacao", "claude_code", "financeiro"] },
      { "name": "complexidade", "type": "choice", "prompt": "Simples ou complexa?", "options": ["simples", "complexa"] },
      { "name": "urgencia", "type": "score", "prompt": "Urgência de 0 a 1" },
      { "name": "ferramenta", "type": "noul", "prompt": "Qual ferramenta foi citada?" }
    ]
  }'</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #6366f1;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🛡️</span> 2. Ativar o Hook <code>PreToolUse</code> no Claude Code (<code>jev_gate.py</code>)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Intercepte comandos <code>Bash</code> em ~150ms para aprovar comandos de leitura (<code>allow</code>), pedir confirmação (<code>ask</code>) ou bloquear comandos destrutivos (<code>deny</code>):
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Terminal</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>export TYPESAFE_API_KEY="ts_live_sua_chave_aqui"
mkdir -p .claude/hooks
cp jev/jev_gate.py .claude/hooks/jev_gate.py
chmod +x .claude/hooks/jev_gate.py</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #ec4899;">
                    <div class="ruflo-cheatsheet-title">
                        <span>⚙️</span> 3. Baixar os 2 Workflows n8n + Apresentação Interativa (43 Slides)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Você pode baixar os JSONs diretamente na aba <strong>Workflows n8n</strong> ao lado ou pelos links abaixo:
                    </p>
                    <div style="display:flex; gap:12px; flex-wrap:wrap; margin-top:10px;">
                        <a href="jev/flowgrammers-jev-triagem-alunos.json" download="flowgrammers-jev-triagem-alunos.json" style="background:#00c9a7; color:#042f2e; padding:10px 18px; border-radius:8px; text-decoration:none; font-weight:700; font-size:14px;">⬇️ Baixar Workflow 1: Triagem de Alunos (.json)</a>
                        <a href="jev/flowgrammers-jev-benchmark.json" download="flowgrammers-jev-benchmark.json" style="background:#0f172a; color:#fff; padding:10px 18px; border-radius:8px; text-decoration:none; font-weight:700; font-size:14px;">⬇️ Baixar Workflow 2: Benchmark Jev (.json)</a>
                        <a href="contexto/jev_ia_que_decide.html" download="Jev_A_IA_que_Decide_Flowgrammers.html" style="background:#f1f5f9; color:#0f172a; border:1px solid #cbd5e1; padding:10px 18px; border-radius:8px; text-decoration:none; font-weight:700; font-size:14px;">🎓 Baixar Apresentação Completa (.html)</a>
                    </div>
                </div>
            </div>
        `
    });
}
