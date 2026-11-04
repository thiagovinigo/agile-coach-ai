# API Reference

REST API for the 21st Agents runtime. Manage sandboxes, threads, files, and stream chat responses.

## Base URL

```
https://relay.an.dev
```

All API requests use HTTPS. Request and response bodies are JSON-encoded.

## Authentication

All endpoints require a bearer token via the `Authorization` header:

```
Authorization: Bearer <your_api_key>
```

## Conventions

- Property names use `camelCase`.
- Timestamps are ISO 8601 strings (e.g. `2026-02-26T12:00:00Z`).
- IDs are prefixed strings (`sb_` for sandboxes, `th_` for threads).
- The chat endpoint returns Server-Sent Events (SSE) for streaming.
- Errors return structured JSON with `code`, `message`, and `status` fields.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/sandboxes | Create sandbox |
| GET | /v1/sandboxes/:id | Get sandbox |
| DELETE | /v1/sandboxes/:id | Delete sandbox |
| POST | /v1/sandboxes/:id/exec | Execute command |
| POST | /v1/sandboxes/:id/files | Write files |
| GET | /v1/sandboxes/:id/files | Read file |
| POST | /v1/sandboxes/:id/git/clone | Clone repository |
| GET | /v1/sandboxes/:id/threads | List threads |
| POST | /v1/sandboxes/:id/threads | Create thread |
| GET | /v1/sandboxes/:id/threads/:threadId | Get thread |
| DELETE | /v1/sandboxes/:id/threads/:threadId | Delete thread |
| POST | /v1/chat/:slug | Send message (SSE) |
| GET | /v1/chat/:slug/:sandboxId/stream | Resume stream |
| DELETE | /v1/chat/:slug/:sandboxId/stream | Cancel stream |
