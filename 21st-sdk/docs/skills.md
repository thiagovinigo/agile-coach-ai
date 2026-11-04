# Skills

Skills are reusable blocks of instructions that give your agent deeper context on specific topics - API details, behavioral rules, step-by-step procedures, or anything else it needs to know.

## What skills are

Think of skills as extra pages in an instruction manual. The system prompt tells the agent who it is and how to behave in general. Skills give it detailed knowledge on specific topics - like how to call a particular API, how to handle refunds, or what tone to use when writing marketing copy.

You write a skill once and attach it to any number of agents. When you update the skill, every agent that uses it picks up the change automatically.

## How skills work with the system prompt

The system prompt is your agent's core identity - it's sent with every message. Skills provide additional context that the agent can reference when it needs to.

The key pattern: in your system prompt, you tell the agent *when* to use each skill. The skill itself contains the *detailed instructions* for that situation.

```
System prompt:
  "You are a support agent for Acme Inc.
   When the user asks about returns, follow the Returns Policy skill.
   When the user asks about billing, follow the Billing FAQ skill."

Skills attached:
  ├─ Returns Policy    (detailed refund steps, eligibility rules, edge cases)
  └─ Billing FAQ       (plan tiers, upgrade flow, invoice questions)
```

This way your system prompt stays short and focused, while the agent still has access to deep context whenever a specific topic comes up.

## What to put in a skill

- **API documentation** - endpoints, parameters, authentication, example requests and responses
- **Procedures** - step-by-step instructions for handling specific situations
- **Behavioral rules** - tone, formatting, what to say and what to avoid in specific contexts
- **Domain knowledge** - product specs, pricing tables, feature comparisons, FAQs
- **Tool calling instructions** - how to use specific tools, what parameters to pass

## Skills vs system prompts

| System prompt | Skill |
|---|---|
| One per agent | Many per agent |
| Sent with every message | Referenced on demand |
| Defines identity, tone, and general rules | Provides detailed context on specific topics |
| Not shareable between agents | Shareable across multiple agents |

**Rule of thumb:** If you'd put it in the agent's "about me", it belongs in the system prompt. If it's reference material the agent needs for specific tasks, make it a skill.

## Create a skill

Open the **Skills** page in the dashboard and click **New Skill**.

| Field | Description |
|---|---|
| Name | Human-readable name (max 100 characters). A slug is auto-generated. |
| Description | Optional - a short summary of what the skill covers. |
| Content | The instructions. Written in plain text or Markdown (up to 10,000 characters). |
| Tags | Optional labels for organization (e.g. support, sales, onboarding). |

## Attach skills to agents

Once created, attach a skill to an agent in the agent's configuration page. A single agent can use multiple skills, and a single skill can be shared across multiple agents.

After attaching, reference the skill in your system prompt so the agent knows when to use it.