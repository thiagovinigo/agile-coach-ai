# CLI

Use `@21st-sdk/cli` to authenticate, deploy agents, manage environment variables, and inspect logs from your terminal.

## Install & Auth

Run the CLI with `npx`:

```bash
npx @21st-sdk/cli login
```

Credentials are saved to `~/.an/credentials`. You can also authenticate non-interactively with `API_KEY_21ST`.

## Project Layout

The current deploy structure is:

```
agents/
  my-agent/
    index.ts
    template/
      ...
```

The primary entrypoint is `agents/<slug>/index.ts`.

## Deploy

```bash
npx @21st-sdk/cli deploy
```

Deploy scans `agents/`, bundles detected agents, uploads them, and prints the Agents dashboard URL.

## Environment Variables

```bash
# list configured keys
npx @21st-sdk/cli env list my-agent

# set or update one key
npx @21st-sdk/cli env set my-agent OPENAI_API_KEY sk-live-...

# remove one key
npx @21st-sdk/cli env remove my-agent OPENAI_API_KEY
```

The list command only returns keys, not secret values.

## Logs

```bash
# list chats
npx @21st-sdk/cli logs my-agent

# inspect one chat
npx @21st-sdk/cli logs my-agent <chat-id>

# inspect one thread
npx @21st-sdk/cli logs my-agent <chat-id> <thread-id>

# machine-readable output
npx @21st-sdk/cli logs my-agent --json
```

## Filtering & Pagination

The logs list supports:

- `--status active|error`
- `--search TEXT`
- `--since ISO`
- `--until ISO`
- `--limit N`
- `--cursor UUID`

To fetch the next page, reuse the same filters together with the returned cursor:

```bash
npx @21st-sdk/cli logs my-agent --status active --limit 20
npx @21st-sdk/cli logs my-agent --status active --limit 20 --cursor <nextCursor>
```

## CLI Environment Variables

- `API_KEY_21ST` - Override the API key used by the CLI