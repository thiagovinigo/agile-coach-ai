# Error Codes

All error responses follow a consistent JSON format:

```json
{ "error": { "code": "invalid_request", "message": "...", "status": 400 } }
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (deleted) |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

## Error Codes

| Code | Description |
|------|-------------|
| invalid_request | Malformed request body or missing required fields |
| unauthorized | Invalid, expired, or missing API key |
| forbidden | Insufficient permissions |
| not_found | Resource does not exist |
| rate_limit_exceeded | Too many requests |
| sandbox_error | Sandbox runtime error |
| budget_exceeded | Exceeded a configured budget limit |
| stream_active | A stream is already active for this sandbox |
