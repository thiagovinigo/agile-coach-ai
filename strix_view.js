document.addEventListener('DOMContentLoaded', () => {
    initStrixView();
});

function initStrixView() {
    if (typeof strixData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'strix-view',
        title: 'Strix (AI Pentesting)',
        badge: 'Autonomous AI Hackers',
        icon: '🦉',
        tagline: 'Agentes hackers de IA autônomos que executam seu código dinamicamente, validam vulnerabilidades com PoCs reais e geram autofixes',
        description: 'O <strong>Strix (usestrix/strix)</strong> é uma plataforma open-source de pentesting ofensivo movida por múltiplos agentes de IA (<em>Graph of Agents</em>). Ao contrário de scanners estáticos (SAST) cheios de falsos positivos, os agentes do Strix rodam em sandbox Docker com proxy HTTP <strong>Caido</strong>, navegador automatizado <strong>Playwright</strong> e runtime Python para construir e validar <strong>Proofs-of-Concept (PoCs) reais</strong>, testar contra-evidências e gerar patches de correção.',
        themeColor: '#10b981',
        themeGradient: 'linear-gradient(135deg, #052e16 0%, #0f172a 60%, #14532d 100%)',
        githubRepo: 'https://github.com/usestrix/strix',
        itemType: 'Strix Pentesting',
        pills: [
            { text: '⭐ GitHub: usestrix/strix', link: 'https://github.com/usestrix/strix' },
            { text: '🌐 docs.strix.ai', link: 'https://docs.strix.ai' },
            { text: '🦉 Graph of Agents (Red Team Multi-Agente)' },
            { text: '💥 Validação com PoC Real (Zero Falsos Positivos)' },
            { text: '🧰 Caido Proxy + Browser Exploitation + Sandbox' },
            { text: '🛡️ 9 Skills para Claude/Cursor + 28 Playbooks' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Catálogo Completo Strix (41)' },
            { id: '1. Visão Geral', label: '🦉 Quickstart, CLI, Viewer & CI/CD (10)' },
            { id: '2. Skills para Agentes', label: '💻 Skills para Coding Agents (9)' },
            { id: '3. Playbooks de Vulnerabilidades', label: '💥 Playbooks de Vulnerabilidades (14)' },
            { id: '4. Coordenação Multi-Agente', label: '👑 Coordenação, Contra-Evidência & Stacks (8)' },
            { id: 'cheatsheet', label: '⚡ Comandos de Pentest, API Scan & CI Gate' }
        ],
        data: strixData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🦉</span> Strix — Guia Rápido de Pentest Autônomo, Skills & CI/CD
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Como instalar o Strix, adicionar suas 9 skills de segurança ao seu agente de código e executar auditorias white-box/black-box.
                    </p>
                </div>

                <!-- 1. Instalação & Coding Agent Skills -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🚀</span> 1. Instalar a CLI do Strix & Adicionar as 9 Skills ao seu Agente
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Requer Docker em execução e uma chave de API de qualquer provedor LLM (Anthropic, OpenAI, Google Vertex/Gemini, OpenRouter, Vercel AI Gateway):
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Terminal</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># 1. Instalar o binário do Strix
curl -sSL https://strix.ai/install | bash

# 2. Instalar as 9 Skills do Strix no Claude Code, Cursor, Antigravity ou Codex
npx skills add usestrix/strix

# 3. Configurar o modelo LLM e rodar o primeiro pentest
export STRIX_LLM="anthropic/claude-sonnet-4-5"
export LLM_API_KEY="sua-api-key"
strix --target ./meu-projeto</code></pre>
                    </div>
                </div>

                <!-- 2. Cenários de Pentest (White-Box, Black-Box, OpenAPI) -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #ef4444;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🎯</span> 2. Pentest Combinado (Código-Fonte + App ao Vivo + OpenAPI/Swagger)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        O poder máximo do Strix aparece quando você passa tanto o repositório local (White-Box) quanto a URL em execução (Black-Box/Grey-Box) ou a especificação OpenAPI:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Comandos de Execução</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Pentest Grey-Box com credenciais de teste e instrução customizada:
strix --target https://seu-app.com \\
  --instruction "Realize testes autenticados de IDOR e BFLA usando as contas userA:passA e userB:passB"

# Multi-target: auditar código-fonte + testar exploração real na URL local:
strix -t ./meu-repo -t http://localhost:3000

# Pentest de API guiado por contrato OpenAPI / Swagger / Postman:
strix --target ./openapi.yaml --target https://api.seu-app.com

# Abrir o Dashboard Web Local (porta 8080) para ver PoCs e o Graph of Agents:
strix view</code></pre>
                    </div>
                </div>

                <!-- 3. CI/CD Gate (Headless Mode) -->
                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #0284c7;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🛡️</span> 3. Gate de Segurança em CI/CD (Modo Headless <code>-n</code> + <code>--fail-on</code>)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Use o modo não-interativo (<code>-n</code>) combinado com <code>--scan-mode diff</code> e <code>--fail-on</code> para bloquear Pull Requests vulneráveis:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>CI/CD Pipeline</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code># Falhar o pipeline (exit code != 0) se encontrar vulnerabilidade High ou Critical validada:
strix -n --target ./ --scan-mode diff --fail-on high</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}

window.initStrixView = initStrixView;
