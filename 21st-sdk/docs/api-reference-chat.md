# Chat API

SSE streaming chat endpoint with AI SDK compatibility.

## Send Message

`POST /v1/chat/:slug`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| messages | Message[] | Yes | Array of message objects |
| sandboxId | string | No | Existing sandbox ID |
| threadId | string | No | Existing thread ID (requires sandboxId) |
| options | object | No | Per-request runtime overrides |

### Behavior

- **sandboxId + threadId:** continue an existing thread in a sandbox.
- **sandboxId only:** creates a new thread in the existing sandbox.
- **No sandbox/thread:** creates a new sandbox and thread automatically.
- **threadId without sandboxId:** returns 400 error.

### Options

| Option | Type | Description |
|--------|------|-------------|
| systemPrompt | object | System prompt override (type, preset, append) |
| maxTurns | number | Maximum agent turns |
| maxBudgetUsd | number | Maximum cost in USD |
| disallowedTools | string[] | Tools the agent cannot use |

### SSE Response Format

```
data: {"type":"start"}
data: {"type":"text-start","id":"..."}
data: {"type":"text-delta","id":"...","delta":"Hello world"}
data: {"type":"text-end","id":"..."}
data: {"type":"message-metadata","messageMetadata":{"sessionId":"...","totalCostUsd":0.034}}
data: {"type":"finish"}
data: [DONE]
```

## Resume Stream

`GET /v1/chat/:slug/:sandboxId/stream`

Reconnect to an active SSE stream.

## Cancel Stream

`DELETE /v1/chat/:slug/:sandboxId/stream`

Cancel an active stream. Returns 204 No Content.
