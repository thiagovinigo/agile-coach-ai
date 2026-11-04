# Sandbox Operations API

Run commands, read/write files, and clone repos inside a sandbox.

## Execute Command

`POST /v1/sandboxes/:id/exec`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| command | string | Yes | Shell command to execute |
| cwd | string | No | Working directory |
| envs | object | No | Additional environment variables |
| timeoutMs | number | No | Timeout in milliseconds (default: 30000) |

Response: `{ "stdout": "...", "stderr": "", "exitCode": 0 }`

## Write Files

`POST /v1/sandboxes/:id/files`

Body: `{ "files": [{ "path": "/home/user/workspace/hello.txt", "content": "Hello world!" }] }`

## Read File

`GET /v1/sandboxes/:id/files?path=/home/user/workspace/hello.txt`

Response: `{ "path": "...", "content": "..." }`

## Clone Repository

`POST /v1/sandboxes/:id/git/clone`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | Git repository URL |
| path | string | No | Target directory |
| token | string | No | Auth token for private repos |
| depth | number | No | Clone depth (1 for shallow) |
