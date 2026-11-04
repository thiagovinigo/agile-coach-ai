# Threads API

A thread is a conversation within a sandbox. Each thread has its own message history, status, and cost tracking.

## List Threads

`GET /v1/sandboxes/:id/threads`

Returns all threads within a sandbox.

## Create Thread

`POST /v1/sandboxes/:id/threads`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | No | Display name for the thread |

## Get Thread

`GET /v1/sandboxes/:id/threads/:threadId`

Returns thread details with full message history.

## Delete Thread

`DELETE /v1/sandboxes/:id/threads/:threadId`

Deletes the thread and its message history. Returns 204 No Content.
