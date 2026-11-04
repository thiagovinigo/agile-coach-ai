# Best Practices

Optimizing cost, choosing between skills and system prompts, and security considerations.

## Optimizing Cost

- **Use the right model** - Haiku for simple tasks, Sonnet/Opus for complex reasoning.
- **Set `maxTurns`** - limit reasoning steps to prevent runaway conversations.
- **Set `maxBudgetUsd`** - cap per-request spend.
- **Keep system prompts concise** - move detailed reference material to skills.

## Skills vs System Prompt

System prompt for identity, tone, and general rules (under 2,000 chars). Skills for detailed reference material - loaded on demand, reducing per-message token usage.

## Security

- Never expose API keys client-side - use `createTokenHandler`.
- Only use `bypass` permission mode in fully isolated sandboxes.
- Only enable tools your agent needs.
- Use the dashboard for secrets, never hardcode them.