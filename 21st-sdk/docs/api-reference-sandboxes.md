# Sandboxes API

A sandbox is a persistent runtime environment with its own filesystem, git state, and sessions.

## Create Sandbox

`POST /v1/sandboxes`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| agent | string | Yes | Agent slug |
| files | object | No | Map of file path to content |
| envs | object | No | Environment variables |
| setup | string[] | No | Shell commands to run after creation |

Response: `{ "id": "sb_abc123", "sandboxId": "e2b-sandbox-id", "status": "active", "createdAt": "..." }`

## Get Sandbox

`GET /v1/sandboxes/:id`

Returns sandbox details including agent info, threads list, status, and timestamps.

## Delete Sandbox

`DELETE /v1/sandboxes/:id`

Deletes the sandbox and cascades deletion to all threads. Returns 204 No Content.
