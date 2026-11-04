# Troubleshooting

Common issues and how to fix them.

## The API returns fewer messages than expected

Make sure you're sending the full message history on each `sendMessage` call. The platform persists whatever history you send.

## Auth & token issues

- **401 Unauthorized** - API key missing or invalid. Re-run `an login`.
- **Token exchange failing** - ensure `/api/an-token` route calls `createTokenHandler` with a valid key.

## Agent not responding

- **Sandbox expired** - idle sandboxes are destroyed. Next message creates a new one.
- **Max turns reached** - increase `maxTurns` in config or per-request.
- **Budget exceeded** - increase `maxBudgetUsd` or remove the limit.

## Tool permission errors

Check permission mode. Use `bypass` for autonomous agents in isolated sandboxes.

## Deploy fails

- **Missing entry point** - ensure `agents/<slug>/index.ts` exists with `agent()` default export.
- **Invalid API key** - re-run `an login`.
- **Bundle too large** - avoid heavy dependencies in agent entry point.