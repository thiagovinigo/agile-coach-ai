# Deploy

Project structure, full configuration reference, CLI commands, and deploy internals.

## Quick start

```bash
npm init -y
npm install @21st-sdk/agent zod
```

Create `agents/my-agent/index.ts`:

```ts
import { agent, tool } from "@21st-sdk/agent"
import { z } from "zod"

export default agent({
  model: "claude-sonnet-4-6",
  systemPrompt: "You are a helpful coding assistant.",
  tools: {
    add: tool({
      description: "Add two numbers",
      inputSchema: z.object({ a: z.number(), b: z.number() }),
      execute: async ({ a, b }) => ({
        content: [{ type: "text", text: \`\${a + b}\` }],
      }),
    }),
  },
})
```

Deploy:

```bash
npx @21st-sdk/cli login
npx @21st-sdk/cli deploy
```

## Project layout

```
21st-agents/
├── package.json              # @21st-sdk/agent + zod
├── agents/
│   └── my-agent/
│       └── index.ts          # Agent configuration (entry point)
├── .an/                      # Generated on first deploy
│   └── project.json          # Links project to deployed agent
├── .env                      # Local env vars (optional)
└── .gitignore                # Should include .an/
```

## Agent configuration

The agent file is where all your configuration lives - model, runtime, system prompt, tools, hooks:

```ts
import { agent, tool } from "@21st-sdk/agent"
import { z } from "zod"

export default agent({
  model: "claude-sonnet-4-6",
  runtime: "claude-code",
  systemPrompt: "You are a helpful coding assistant.",
  permissionMode: "default",
  maxTurns: 50,
  tools: {
    greet: tool({
      description: "Greet a user",
      inputSchema: z.object({ name: z.string() }),
      execute: async ({ name }) => ({
        content: [{ type: "text", text: \`Hello, \${name}!\` }],
      }),
    }),
  },
  onFinish: async ({ result }) => {
    console.log("Done:", result)
  },
})
```

`@21st-sdk/agent` is externalized during bundling - the sandbox provides it at runtime.

## Entry point

When you run `an deploy`, the CLI scans the `agents/` directory. Each deployable agent should live at `agents/<slug>/index.ts` or `agents/<slug>/index.js`.

| File | Notes |
|------|-------|
| agents/my-agent/index.ts or agents/my-agent/index.js | Use one folder per deployable agent so sibling files like template/ can live next to it. |

The entry point must have a `default export` that returns an agent config created with `agent()`.

## package.json

Two required dependencies:

```json
{
  "name": "my-agent",
  "type": "module",
  "dependencies": {
    "@21st-sdk/agent": "latest",
    "zod": "^3.24"
  }
}
```

## CLI reference

### Install

```bash
# Run directly with npx
npx @21st-sdk/cli login
npx @21st-sdk/cli deploy

# Or install globally
npm install -g @21st-sdk/cli
an login
an deploy
```

### Login

Authenticate with your API key from the dashboard.

```bash
$ an login
  Enter your API key: 21st_sk_...
  Authenticated as John (team: my-team)
```

Credentials are saved to `~/.an/credentials`. You only need to log in once.

### Deploy

```bash
$ an deploy
  Bundling agents/my-agent/index.ts...
  Bundled (12.3kb)
  Deploying my-agent...

  ✓ https://api.an.dev/v1/chat/my-agent
```

## How deploy works

1. **Bundle** - esbuild bundles your code (Node 22, ESM, minified). `@21st-sdk/agent` is externalized.
2. **Upload** - Base64-encoded bundle sent to the deploy API with your slug and API key.
3. **Sandbox** - E2B sandbox created with the 21st Agents runtime template (Node 24, git, curl, ripgrep, GitHub CLI).
4. **Live** - Agent config saved to database, agent immediately available at its chat endpoint.

## Environment variables

Set env vars from the dashboard. Defined tools can read them via `process.env` in the trusted remote environment. They are not injected into the sandbox itself.

## Generated files

After your first deploy, the CLI creates a `.an/` directory:

```json
// .an/project.json
{
  "agentId": "a1b2c3d4-...",
  "slug": "my-agent"
}
```

This links your local project to the deployed agent. Add `.an/` to your `.gitignore`.

## Redeploying

Run `an deploy` again. The old sandbox is killed, a new one created with the updated bundle, and the agent URL stays the same.

## What lives where

Agents are **code-first**. Agent behavior lives entirely in your code. The dashboard is for monitoring and managing environment variables.

| What | Where | Managed from |
|------|-------|-------------|
| Agent config (model, runtime, permission mode, max turns) | agents/my-agent/index.ts | Code only |
| System prompt | agents/my-agent/index.ts | Code only |
| Custom tools (Zod schemas) | agents/my-agent/index.ts | Code only |
| Lifecycle hooks (onStart, onToolCall, onFinish) | agents/my-agent/index.ts | Code only |
| Environment variables | Dashboard | Dashboard |
| Deployments (sandbox, bundle hash) | Dashboard | an deploy |
| Logs & costs (conversations, tokens, USD) | Dashboard | View only |