# Agents

Reference for the configuration options available in your `agent()` call - runtimes, models, tools, permissions, and attachments. See [Deploy](/an/docs/deploy/deploy) for project setup and CLI.

## Runtime & Model

The runtime determines which AI provider executes your agent. Each runtime supports a different set of models with varying capabilities and price points.

### Anthropic - Claude Code
Full-featured agentic runtime with tool use, web access, and sandboxed execution. Best for complex multi-step tasks.

**Available models:** Claude Sonnet 4.6, Claude Opus 4.6, Claude Haiku 4.5

### OpenAI - Codex (Coming soon)
OpenAI's optimized runtime with multiple reasoning levels. Great for structured tasks and analysis.

**Model switching** - you can let end users switch between models at runtime. Enable "Allow model switching" in the agent config and select which models to expose.

## System Prompt

The system prompt defines your agent's persona, behavioral rules, and constraints. It's sent with every message and shapes how the agent responds. Max 4,000 characters.

See [System Prompts](/an/docs/build/system-prompts) for writing tips, examples, and how to reference skills.

## Tools

Tools are the capabilities your agent can use during a conversation. Toggle each tool on or off.

| Category | Tools | Description |
|---|---|---|
| Read-only | Read, Glob, Grep | Search and read files without modifications |
| Edit | Edit, Write | Create and modify files in the sandbox |
| Execution | Bash | Run shell commands in the sandboxed environment |
| Web | WebFetch, WebSearch | Fetch URLs and search the web for information |

Only enable the tools your agent actually needs.

## Permission Modes

| Mode | Behavior |
|---|---|
| Default | Ask the user before risky actions like file writes or shell commands |
| Accept Edits | Auto-approve file edits, but confirm shell commands |
| Bypass All | No confirmation needed. The agent acts autonomously |

**Tip:** For agents embedded in your product where the sandbox is fully isolated, use `Bypass All` to remove friction.

## Max Turns

Limits how many reasoning steps the agent can take per message (1-500). Default: 50.

## Attachments

Allow users to upload files alongside their messages. Configure allowed file types (Images, Documents, Code, or All) and custom extensions.

## Skills

Attach skills in the agent config, then reference them by name in the system prompt. See [Skills](/an/docs/build/skills) for details.