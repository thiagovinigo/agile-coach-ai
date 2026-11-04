# Get Started

Create an agent, deploy it, and add it to your Next.js app.

## 1. Create your agent

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

See [Deploy](/an/docs/deploy/deploy) for all configuration options.

## 2. Deploy

Log in with your [API key](/an/app) from the dashboard, then deploy:

```bash
npx @21st-sdk/cli login
npx @21st-sdk/cli deploy
```

Your agent is now live. Next, integrate it into your app.

## 3. Install the SDK

```bash
pnpm add @21st-sdk/nextjs
```

This also installs `@21st-sdk/react` with all UI components. Peer dependencies: `ai`, `@ai-sdk/react`.

## 4. Create a Token Route

The SDK exchanges your secret API key for short-lived tokens server-side, so credentials are never exposed to the browser.

```typescript
// app/api/an-token/route.ts
import { createTokenHandler } from "@21st-sdk/nextjs/server"

export const POST = createTokenHandler({
  apiKey: process.env.API_KEY_21ST!,
})
```

## 5. Add the Chat Component

Use `createAgentChat` to connect to your agent and `<AgentChat>` to render the UI. It handles streaming, tools, and theming automatically.

```tsx
"use client"

import { AgentChat, createAgentChat } from "@21st-sdk/nextjs"
import { useChat } from "@ai-sdk/react"

const chat = createAgentChat({
  agent: "my-agent",
  tokenUrl: "/api/an-token",
})

export default function Page() {
  const { messages, input, handleInputChange, handleSubmit, status, stop, error } =
    useChat({ chat })

  return (
    <AgentChat
      messages={messages}
      onSend={() => handleSubmit()}
      status={status}
      onStop={stop}
      error={error ?? undefined}
    />
  )
}
```

## Optional: Per-message Runtime Options

Pass `options` inside the AI SDK request body when one browser request should run with different runtime settings without changing the deployed agent config.

```tsx
"use client"

import { AgentChat, createAgentChat } from "@21st-sdk/nextjs"
import { useChat } from "@ai-sdk/react"

const chat = createAgentChat({
  agent: "my-agent",
  tokenUrl: "/api/an-token",
})

const reviewOptions = {
  systemPrompt: {
    type: "preset",
    preset: "claude_code",
    append:
      "You are reviewing a checkout diff. Focus on regressions, risky edge cases, and missing tests. Do not edit files.",
  },
  maxTurns: 4,
  maxBudgetUsd: 0.2,
  disallowedTools: ["Bash"],
}

export default function Page() {
  const { messages, sendMessage, status, stop, error } = useChat({ chat })

  return (
    <AgentChat
      messages={messages}
      onSend={(message) =>
        sendMessage(
          {
            role: "user",
            parts: [{ type: "text", text: message.content }],
          },
          {
            body: { options: reviewOptions },
          },
        )
      }
      status={status}
      onStop={stop}
      error={error ?? undefined}
    />
  )
}
```

Currently applied by the runtime: `systemPrompt`, `maxTurns`, `maxBudgetUsd`, and `disallowedTools`.

## Components

| Component | Description |
|---|---|
| `<AgentChat />` | Full chat interface with messages, input, and tool rendering |
| `<MessageList />` | Standalone message list for custom layouts |
| `<InputBar />` | Chat input with submit handling |
| `<ToolRenderer />` | Individual tool call renderer with expand/collapse |