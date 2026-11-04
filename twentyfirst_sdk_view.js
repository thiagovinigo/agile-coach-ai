document.addEventListener('DOMContentLoaded', () => {
    initTwentyFirstSdkView();
});

function initTwentyFirstSdkView() {
    if (typeof twentyFirstSdkData === 'undefined' || !window.createStandardToolView) return;

    window.createStandardToolView({
        containerId: 'twentyfirst-sdk-view',
        title: '21st Agents SDK (21st-dev/21st-sdk)',
        badge: 'Agent Infrastructure & Runtime',
        icon: '🧩',
        tagline: 'SDK open-source, runtime em sandbox (E2B / OpenSandbox), Relay server e componentes React/Next.js para construir e embarcar agentes de IA',
        description: 'O <strong>21st Agents SDK (21st-dev/21st-sdk)</strong> fornece a infraestrutura completa para adicionar agentes de IA prontos para produção (<strong>Claude Code</strong> e <strong>OpenAI Codex</strong>) ao seu produto sem precisar construir sandboxing, streaming SSE, gerenciamento de sessões ou UI do zero. Inclui os pacotes <code>@21st-sdk/agent</code>, <code>@21st-sdk/react</code>, <code>@21st-sdk/nextjs</code>, <code>@21st-sdk/node</code>, <code>@21st-sdk/cli</code>, <code>21st-sdk</code> (Python) e os serviços <code>agents-web</code>, <code>relay</code> e <code>proxy</code>.',
        themeColor: '#6366f1',
        themeGradient: 'linear-gradient(135deg, #1e1b4b 0%, #0f172a 60%, #312e81 100%)',
        githubRepo: 'https://github.com/21st-dev/21st-sdk',
        itemType: '21st Agents SDK',
        pills: [
            { text: '⭐ GitHub: 21st-dev/21st-sdk', link: 'https://github.com/21st-dev/21st-sdk' },
            { text: '🌐 Docs: 21st.dev/an/docs', link: 'https://21st.dev/an/docs' },
            { text: '📦 9 Pacotes (@21st-sdk/agent, react, nextjs, node, cli, python)' },
            { text: '🔒 Sandboxes Isolados (E2B & OpenSandbox K8s)' },
            { text: '⚡ Streaming SSE + Runtimes Claude Code & Codex' },
            { text: '🔐 Multi-Vault Credentials & Token Handler' }
        ],
        tabs: [
            { id: 'all', label: '🌟 Catálogo Completo 21st SDK (47)' },
            { id: '1. Início & Conceitos', label: '🧭 Início & Conceitos (6)' },
            { id: '2. Build', label: '🛠️ Build: Agents, Skills & UI (5)' },
            { id: '3. Deploy, CLI', label: '🚢 Deploy, CLI & Observability (4)' },
            { id: '4. Segurança', label: '🔐 Segurança & Vaults (2)' },
            { id: '5. REST API Reference', label: '🔌 REST API Reference (6)' },
            { id: '6. Knowledge Base', label: '📚 Knowledge Base & Sandboxes (5)' },
            { id: '7. Pacotes SDK', label: '📦 Pacotes SDK & Runtime (19)' },
            { id: 'cheatsheet', label: '⚡ Quickstart, CLI & Self-Hosting' }
        ],
        data: twentyFirstSdkData,
        cheatsheetHtml: `
            <div style="padding:10px 20px 40px; background:#fff; min-height:100%; border-radius:12px;">
                <div style="margin-bottom:24px; border-bottom:2px solid #e2e8f0; padding-bottom:16px;">
                    <h2 style="color:#0f172a; margin:0 0 6px 0; display:flex; align-items:center; gap:10px;">
                        <span>🧩</span> 21st Agents SDK — Quickstart, Next.js Embed & Self-Hosting
                    </h2>
                    <p style="color:#64748b; margin:0; font-size:15px;">
                        Comandos prontos para criar seu agente com <code>@21st-sdk/agent</code>, fazer deploy via CLI e embarcar o chat no Next.js.
                    </p>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #6366f1;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🚀</span> 1. Definir um Agente (<code>@21st-sdk/agent</code>) e Fazer Deploy (<code>@21st-sdk/cli</code>)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Defina o modelo (ex.: <code>claude-sonnet-4-6</code>), o system prompt e as tools tipadas com Zod:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Terminal + TypeScript</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>npm install @21st-sdk/agent zod

# Login e deploy para o Relay/Sandbox:
npx @21st-sdk/cli login
npx @21st-sdk/cli deploy
npx @21st-sdk/cli logs</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #10b981;">
                    <div class="ruflo-cheatsheet-title">
                        <span>▲</span> 2. Integrar no Next.js (Token Route + <code>&lt;AgentChat /&gt;</code>)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Troque sua chave secreta por tokens curtos no servidor e renderize o chat completo com suporte a tool renderers e temas:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>app/api/an-token/route.ts</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>pnpm add @21st-sdk/nextjs @21st-sdk/react ai @ai-sdk/react

// app/api/an-token/route.ts
import { createTokenHandler } from "@21st-sdk/nextjs/server"

export const POST = createTokenHandler({
  apiKey: process.env.API_KEY_21ST!,
})</code></pre>
                    </div>
                </div>

                <div class="ruflo-cheatsheet-card" style="border-left: 4px solid #f59e0b;">
                    <div class="ruflo-cheatsheet-title">
                        <span>🏗️</span> 3. Rodar a Stack Completa Localmente (Relay + Model Proxy + Agents Web)
                    </div>
                    <p style="color:#475569; font-size:14px; margin-bottom:12px;">
                        Suba os 3 serviços do monorepo localmente apontando para E2B ou OpenSandbox:
                    </p>
                    <div class="tool-code-container">
                        <div class="tool-code-header">
                            <span>Self-Hosted Stack</span>
                            <button class="tool-copy-btn" onclick="copyToolCodeSnippet(this)">Copiar</button>
                        </div>
                        <pre class="tool-code-block"><code>git clone https://github.com/21st-dev/21st-sdk.git
cd 21st-sdk && pnpm install

cp apps/agents-web/.env.example apps/agents-web/.env
cp apps/relay/.env.example apps/relay/.env
cp apps/proxy/.env.example apps/proxy/.env

# Terminal 1: Model Proxy (3003)
PORT=3003 pnpm --filter proxy dev
# Terminal 2: Relay Service (3002)
PORT=3002 pnpm --filter relay dev
# Terminal 3: Agents Web Dashboard (3000)
pnpm --filter agents-web dev</code></pre>
                    </div>
                </div>
            </div>
        `
    });
}
