# Tools and MCPs

MCP servers are configured almost the same way as skills, but the file is loaded at deploy time instead of from the sandbox filesystem.

## Skills vs MCP servers

- **Skill** - lives in `.claude/skills/<name>/SKILL.md`, contains reusable instructions, usually referenced from the system prompt
- **MCP server** - lives in a sibling `.mcp.json` next to your agent entrypoint, contains Claude Code MCP server configuration, provides an interface for external tools

See [Skills](/an/docs/build/skills) for the related pattern.

## How deploy-time loading works

During deploy, the CLI reads a sibling `.mcp.json` file next to your agent entrypoint and uploads it with the agent bundle.

The runtime stores that file privately and generates Claude's MCP config from it. Do not put MCP config at `/home/user/workspace/.mcp.json` or inside `template/`.

## .mcp.json format

See [Claude's MCP docs](https://platform.claude.com/docs/en/agent-sdk/mcp) for the native format and supported options.

Keep secrets as placeholders here, for example `Bearer ${NIA_TOKEN}`, and set the real value through dashboard env vars.

Do not hardcode secrets directly in `.mcp.json`. Use placeholders and agent env vars instead.

```json
{
  "mcpServers": {
    "nia": {
      "type": "http",
      "url": "https://apigcp.trynia.ai/mcp",
      "headers": {
        "Authorization": "Bearer public-demo-token"
      }
    },
    "svelte": {
      "command": "npx",
      "args": ["-y", "@sveltejs/mcp"]
    }
  }
}
```

## Add the file next to your agent entrypoint

For deployed agents, create a sibling `.mcp.json` file next to `index.ts`, `index.js`, or `index.go`.

The deploy CLI uploads that file automatically. Do not add it through `Sandbox({ files })` or `template/`.

```ts
import { agent } from "@21st-sdk/agent"

export default agent({
  model: "claude-sonnet-4-6",
  systemPrompt: `You are a full-stack coding assistant.
Use the configured MCP servers whenever they are helpful.`,
})
```

Also create `agents/my-agent/.mcp.json` with the JSON above. The platform picks up that sibling file during deploy and wires the MCP servers into the runtime automatically.