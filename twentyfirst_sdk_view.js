// 21st Agents SDK (21st-dev/21st-sdk) View
window.initTwentyFirstSdkView = window.createStandardToolView({
    containerId: 'twentyfirst-sdk-view',
    dataKey: 'twentyFirstSdkData',
    globalVarName: 'twentyFirstSdkView',
    themeColor: '#111827',
    badgeText: '21st-dev/21st-sdk · Agent Infrastructure',
    title: '🧩 21st Agents SDK (Runtime, Sandboxes & UI)',
    description: 'SDK open-source, runtime em sandbox (<strong>E2B / OpenSandbox</strong>), Relay server, Model Proxy e componentes <strong>React / Next.js / Node / Python / CLI</strong> para construir, fazer deploy e embarcar agentes de IA (Claude Code & OpenAI Codex) em produção com streaming SSE e observabilidade.',
    repoUrl: 'https://github.com/21st-dev/21st-sdk',
    statsHtml: `
        <div style="background:#f3f2f1; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600; color:#323130;">📦 <strong>${window.twentyFirstSdkData ? window.twentyFirstSdkData.length : 47}</strong> Documentos & Guias SDK</div>
        <div style="background:#eef2ff; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600; color:#4338ca;">⚛️ <strong>9 Pacotes:</strong> agent · react · nextjs · node · python · cli</div>
        <div style="background:#ecfdf5; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600; color:#047857;">🔒 <strong>Sandboxes:</strong> E2B & OpenSandbox (K8s)</div>
        <div style="background:#fff7ed; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600; color:#c2410c;">⚡ <strong>Runtimes:</strong> Claude Code & Codex</div>
    `,
    categories: [
        { id: 'all', label: 'Todos', icon: '🧩' },
        { id: 'getting-started', label: 'Início & Conceitos', icon: '🧭' },
        { id: 'build', label: 'Build (Agents, Skills & UI)', icon: '🛠️' },
        { id: 'deploy-operate', label: 'Deploy, CLI & Observability', icon: '🚢' },
        { id: 'security', label: 'Segurança, Vaults & API Keys', icon: '🔐' },
        { id: 'api-reference', label: 'REST API Reference', icon: '🔌' },
        { id: 'knowledge-base', label: 'Knowledge Base & Sandboxes', icon: '📚' },
        { id: 'packages', label: 'Pacotes SDK & Runtime', icon: '📦' }
    ],
    cheatsheet: {
        tabLabel: 'Quickstart & CLI',
        tabIcon: '⚡',
        title: '⚡ Quickstart — 21st Agents SDK (@21st-sdk)',
        subtitle: 'Comandos essenciais para definir um agente com @21st-sdk/agent, fazer deploy com @21st-sdk/cli e embarcar o chat com @21st-sdk/nextjs.',
        cards: [
            {
                title: '1. Criar e Fazer Deploy de um Agente',
                badge: '@21st-sdk/agent + cli',
                badgeBg: '#eef2ff',
                badgeColor: '#4338ca',
                description: 'Instale o SDK de definição de agentes e faça o deploy pelo CLI oficial:',
                code: `pnpm add @21st-sdk/agent zod
npx @21st-sdk/cli login
npx @21st-sdk/cli deploy
npx @21st-sdk/cli logs`,
                footer: 'O CLI empacota seu agente e registra o deployment no Relay/Sandbox.'
            },
            {
                title: '2. Integrar no Next.js (Token Route + <AgentChat />)',
                badge: '@21st-sdk/nextjs + react',
                badgeBg: '#ecfdf5',
                badgeColor: '#047857',
                description: 'Adicione o token handler server-side e o componente de chat com suporte nativo a tools e streaming SSE:',
                code: `pnpm add @21st-sdk/nextjs @21st-sdk/react ai @ai-sdk/react

// app/api/an-token/route.ts
import { createTokenHandler } from "@21st-sdk/nextjs/server"
export const POST = createTokenHandler({ apiKey: process.env.API_KEY_21ST! })`,
                footer: 'Nunca expõe sua API_KEY_21ST no navegador — gera tokens efêmeros por sessão.'
            },
            {
                title: '3. Rodar a Stack Completa Localmente (Self-Hosted)',
                badge: 'Relay + Proxy + Web',
                badgeBg: '#fff7ed',
                badgeColor: '#c2410c',
                description: 'Suba os 3 serviços principais do monorepo (Model Proxy na 3003, Relay na 3002 e Agents Web na 3000):',
                code: `git clone https://github.com/21st-dev/21st-sdk.git
cd 21st-sdk && pnpm install
PORT=3003 pnpm --filter proxy dev
PORT=3002 pnpm --filter relay dev
pnpm --filter agents-web dev`,
                footer: 'Compatível com E2B Cloud ou OpenSandbox self-hosted via Kubernetes.'
            }
        ]
    }
});
