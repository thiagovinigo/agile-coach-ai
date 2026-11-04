# API Keys & Environment Variables

How to create, use, and protect API keys that authenticate your app's requests, and how to manage environment variables for your agents.

## API keys

API keys are team-scoped credentials that authenticate your app's requests to the 21st Agents platform. You create and manage them in the dashboard under the API tab.

- **Format** - `21st_sk_` prefix + 64 hex characters. Legacy `an_sk_` keys still work.
- **Scope** - Each key is scoped to a single team
- **Visibility** - The full key is shown only once at creation. Store it securely.
- **Revocation** - Deactivate a key instantly from the dashboard. Active sessions using that key will stop working.

## Token exchange flow

Your API key should never be exposed in client-side code. Instead, use a server-side token route that exchanges the API key for a short-lived JWT token:

1. Client calls your backend → POST /api/an-token
2. Backend uses API key → client.tokens.create({ agent })
3. Backend returns JWT → short-lived, scoped token
4. Client uses JWT → passed to AgentChat / SDK

```typescript
// app/api/an-token/route.ts
import { AgentClient } from "@21st-sdk/node"
import { NextResponse } from "next/server"

const client = new AgentClient({
  apiKey: process.env.API_KEY_21ST!,
})

export async function POST() {
  const token = await client.tokens.create({ agent: "my-agent" })
  return NextResponse.json(token)
}
```

The [Get Started](/an/docs/get-started) guide walks through this setup step by step.

## Key safety practices

| Do | Don't |
|---|---|
| Store in `.env.local` or secret manager | Commit to git or hardcode in source |
| Use the token exchange route | Pass `API_KEY_21ST` to the browser |
| Rotate keys periodically | Share keys between environments |
| Deactivate unused keys immediately | Leave old keys active "just in case" |

## Environment variables

Environment variables let you pass secrets (database URLs, third-party API keys) to your agent's tools without exposing them to the agent process. The [Sandbox Manager](/an/docs/security/overview) injects them at tool execution time only.

## Managing env vars

There are two ways to configure environment variables:

- **Dashboard** - Open your agent in the dashboard, go to the Environment tab, and add key-value pairs. Changes take effect on the next sandbox session.
- **CLI** - Use `@21st-sdk/cli env` to list, set, or remove variables from your terminal. Ideal for CI/CD and scripted workflows.

```bash
# list configured env vars
npx @21st-sdk/cli env list my-agent

# set or update one key
npx @21st-sdk/cli env set my-agent OPENAI_API_KEY sk-live-...

# set or update multiple keys
npx @21st-sdk/cli env set my-agent OPENAI_API_KEY=sk-live-... ANTHROPIC_API_KEY=sk-ant-...

# remove a key
npx @21st-sdk/cli env remove my-agent OPENAI_API_KEY
```

## Isolation

Env vars set via the dashboard or CLI are not ordinary environment variables inside the agent process. They are injected by the Sandbox Manager into tool execution only — tools that need a database connection or third-party API key get the value at call time, but the agent itself cannot read them from `process.env`.

This means even if the agent is tricked into inspecting its own environment, tool secrets remain hidden. See [Security](/an/docs/security/overview) for the full trust model.