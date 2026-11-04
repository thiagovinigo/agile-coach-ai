# Claude Code Agent

How to build, deploy, and embed a production AI agent powered by Claude Code - sandboxing, streaming, custom tools, and React UI.

## What is Claude Code and why run it as a production agent?

Claude Code (the Claude Agent SDK) is Anthropic's agentic runtime with built-in tools for file I/O, terminal, web search, and multi-step reasoning. 21st SDK wraps it with cloud sandboxing, SSE streaming, auth, and a React chat component so you can ship production agents.

## How do I run Claude Code in an E2B cloud sandbox?

Define your agent, deploy with one CLI command, and the platform provisions E2B sandboxes on demand. Each sandbox is an isolated Linux environment with full terminal, network access, and persistence.

## How do I define a Claude Code agent?

Use the agent() function from @21st-sdk/agent with model, runtime, systemPrompt, tools, permissionMode, maxTurns, and maxBudgetUsd options.

## How do I deploy a Claude Code agent to production?

Run npx @21st-sdk/cli login and npx @21st-sdk/cli deploy. No Docker, no Kubernetes.

## How does streaming work with a Claude Code agent?

The platform streams via Server-Sent Events (SSE), compatible with Vercel AI SDK. Text, tool calls, tool results, and thinking blocks all stream in real time.

## How do I add a chat UI for my Claude Code agent in React / Next.js?

Install @21st-sdk/nextjs and @21st-sdk/react, create a token route with createTokenHandler, and use the AgentChat component.

## How do I add custom tools to a Claude Code agent?

Define tools using the tool() function with Zod schemas. They run inside the E2B sandbox alongside the agent.

## How do I control costs and prevent runaway API spend?

Use maxBudgetUsd for per-conversation caps, maxTurns to limit loops, and disallowedTools to restrict tool access.

## How do I monitor and debug my Claude Code agent in production?

The 21st dashboard provides session logs, token and cost tracking, live monitoring, and error tracking.