# System Prompts

The system prompt is the single most important setting for your agent. It defines who the agent is, what it knows, and how it behaves.

## How it works

Every time a user sends a message, your system prompt is included at the top of the conversation sent to the model. Max length is 4,000 characters. The field is optional - agents work without a custom prompt, but they won't be tailored to your use case.

## Default prompt layering

Agents ship with a built-in base prompt that handles tool usage and safety. When you write a custom prompt, it gets appended on top of the default. You can turn off defaults for full control.

- **Defaults on (recommended)** - Your custom prompt layers on top of the built-in safety and tool-use instructions.
- **Defaults off** - Your prompt is the only system prompt the agent sees. Use this when you need full control.

**Tip:** Keep defaults on unless you have a specific reason to replace them.

## Writing a good prompt

The best system prompts are short, specific, and structured.

### Customer support agent

```
You are a support agent for Acme Inc.

- Be friendly, concise, and solution-oriented
- Always greet the user and ask how you can help
- When the user asks about returns, follow the Returns Policy skill
- When the user asks about billing, follow the Billing FAQ skill
- If you can't resolve an issue, offer to escalate to a human agent
- Never make up information - if you don't know, say so
```

### Sales assistant

```
You are a sales assistant for Acme SaaS platform.

- Help users understand our pricing and features
- Ask qualifying questions to recommend the right plan
- Compare our product to competitors when asked, but stay factual
- Always include a link to the pricing page when discussing plans
- Tone: professional but approachable, never pushy
```

### Research assistant

```
You are a research assistant. Help users find and summarize information.

- Use web search to find up-to-date information
- Always cite your sources with links
- Provide structured summaries with key takeaways
- When asked to compare options, use a table format
- Flag when information might be outdated or uncertain
```

## Best practices

- **Be specific** - "Be friendly and concise, answer in 2-3 sentences" works better than "be helpful"
- **Keep it under 2,000 characters** - move detailed reference material to [skills](/an/docs/build/skills)
- **Reference your skills** - tell the agent when to use each attached skill by name
- **Test iteratively** - use the live chat preview in the dashboard
- **Structure with lists** - bullet points are easier for the model to follow than dense paragraphs

## When to use skills instead

If your prompt is growing past ~2,000 characters with detailed reference material - API docs, step-by-step procedures, pricing tables - move that content into [skills](/an/docs/build/skills). Keep the system prompt focused on identity, tone, and general rules. The agent will reference skills on demand without bloating every message.