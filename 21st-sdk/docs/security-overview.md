# Security

How the 21st Agents runtime isolates agent execution, protects secrets, and controls access to tools and model providers.

## Trust model

Running an AI agent that can execute code, read files, and call external services creates a trust problem. The runtime splits every session into two layers:

- **Agent process (untrusted)** - The Claude Code process that runs shell commands, scripts, package installs, and code execution. It lives inside an isolated container and never holds real provider credentials or tool secrets.
- **Sandbox Manager (trusted)** - The control layer that prepares the session, starts the agent, manages streaming, proxies tool and MCP calls, and controls access to secrets and model providers.

The part that orchestrates the session is never the same part that runs the untrusted agent workload.

## Runtime isolation

Each session gets its own sandboxed E2B environment. Inside that sandbox, the agent process runs in a separate execution container — it does not run directly on the sandbox host or in the same process as the Sandbox Manager.

The execution container is further isolated with gVisor (`runsc`), adding an extra kernel-level boundary beyond the standard container boundary.

## File access

Project files are prepared on the sandbox host side. The Sandbox Manager creates the workspace and writes runtime files before the agent starts. That workspace is then bind-mounted into the execution container as the agent's working directory.

The agent sees the real project through a mounted workspace, not a copied snapshot. It can read, edit, create, and execute files — but all of that happens inside the isolated container.

## Model access

The agent process does not call Anthropic or OpenRouter directly. Instead, the sandbox receives a short-lived proxy token and uses it to call the 21st private proxy service. The proxy forwards the request upstream with the real provider credentials attached.

| What the agent gets | What stays on the proxy |
|---|---|
| Short-lived proxy token | Real `ANTHROPIC_API_KEY` |
| Access to inference | Provider account credentials |
| Scoped, time-limited access | OpenRouter and other upstream keys |

## Tools & MCP isolation

Tool and MCP requests follow a different route from model inference. The agent process does not connect to integrations directly — all requests go through the Sandbox Manager.

The Sandbox Manager starts MCP servers on the host side (both local stdio and remote servers), manages their lifecycle, and proxies requests from the agent container. It also injects the current environment variables for that execution and sends only the result back into the agent session.

**Key boundary:** The agent can use real integrations, but tool-side secrets and MCP credentials never live inside the untrusted agent process.

## Secrets & credentials

API keys authenticate your app's requests via a short-lived JWT exchange — the raw key never reaches the browser. Environment variables are injected by the Sandbox Manager into tool execution only, so the agent process never has direct access to secrets.

See [API Keys & Env Vars](/an/docs/security/api-keys) for key formats, token exchange flow, safety practices, and environment variable management.

## Summary

| Resource | Agent gets | Boundary |
|---|---|---|
| Workspace | Full file access via bind-mount | Isolated container + gVisor |
| Model | Short-lived proxy token | Private proxy service |
| Tools & MCPs | Proxied through Sandbox Manager | Host-side gateway |
| Secrets | Never directly accessible | Sandbox Manager injects at execution |