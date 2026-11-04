# Core Concepts

Agents, skills, projects, dialogs, and the Relay runtime - how the pieces fit together.

## How it works

When a user sends a message, your app calls the Chat API. The platform routes the message to a **Relay** runtime that spins up a sandboxed environment, runs the agent with the tools and instructions you configured, and streams the response back via SSE.

```
Your App
  └─ AgentChat component (or raw SDK)
        │
        ▼  SSE streaming
    Relay
        │
        ├─ Agent runtime (Claude Code / Codex)
        ├─ System prompt + skills
        ├─ Tool execution (your configured tools)
        └─ E2B Sandbox (isolated environment)
```

Everything in between - auth, routing, sandboxing, token counting, cost tracking - is handled by the platform.

## Agents

An agent is a configuration that defines what the AI can do and how it behaves. Agents are **code-first** - you define them using `@21st-sdk/agent` (model, system prompt, tools, lifecycle hooks) and deploy with `an deploy`. This creates an E2B sandbox where the agent actually runs. Once deployed, you integrate it into your app with the [React SDK](/an/docs/get-started).

The dashboard is for API keys, environment variables, skills, and monitoring - not for creating or editing agent behavior. See [Deploy](/an/docs/deploy/deploy) for the full breakdown.

## Skills

A skill is a block of additional instructions and context that you can attach to any agent. Unlike the system prompt which is sent every turn, skills act as reference material the agent can draw on when needed.

For example, you might create a "Returns Policy" skill with detailed procedures and attach it to your support agent. In the system prompt you tell the agent: "When the user asks about returns, follow the Returns Policy skill." The agent then has access to the full context without bloating every single message.

## Projects & Dialogs

When a user starts chatting with your agent, the platform creates a **project** - a session that ties together the agent config, a sandbox, and the conversation history.

Each message the user sends within a project creates a **dialog** - a single conversation turn. Dialogs track:

- **Messages** - User input, assistant response, and tool calls
- **Status** - streaming → completed, error, or cancelled
- **Token usage** - Input tokens, output tokens, and total
- **Cost & duration** - USD cost and execution time in milliseconds

The project ID is stable across page refreshes. To start a fresh conversation, rotate the project ID.

## Relay

Relay is the runtime service sitting between your app and the agent. It takes care of:

1. Authenticating the request and resolving the agent config
2. Spinning up an isolated E2B sandbox for safe execution
3. Running the agent with the configured runtime (Claude Code / Codex)
4. Streaming the response back to your app via Server-Sent Events
5. Persisting session state so the agent can resume across turns

You don't interact with Relay directly - the SDK handles it.

## API Keys

API keys authenticate your app's requests to 21st Agents. You create them in the dashboard under the **API** tab.

- **Format:** `21st_sk_` followed by 64 hex characters. Legacy `an_sk_` keys still work.
- **Scope:** Each key is scoped to a team
- **Auth flow:** Your backend exchanges the API key for a short-lived JWT token via `/api/agents/token`, then passes the token to the client

Never expose your API key in client-side code.