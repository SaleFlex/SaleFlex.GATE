# REST API conventions (draft)

## Style

- **JSON** request and response bodies; UTF-8.  
- **Plural resource nouns** where practical (`/api/v1/stores/`, `/api/v1/terminals/`).  
- **Pagination** for list endpoints: `limit`, `offset` or cursor-based (to be chosen).  
- **Idempotency** for financial writes: clients may send `Idempotency-Key` headers on POST (to be enforced server-side).

## Versioning

- URL prefix **`/api/v1/`** (increment major version for breaking changes).  
- Deprecation: `Sunset` or `Warning` headers and documentation notice.

## Authentication

| Mode | Use case |
|------|----------|
| Bearer JWT | User sessions (mobile, web API) |
| API key / device token | PyPOS, KITCHEN, unattended terminals |
| OAuth2 / OIDC (optional) | Enterprise SSO for hub users |

## Errors

Structured error body (example shape):

```json
{
  "code": "forbidden",
  "message": "User cannot access this store.",
  "detail": {}
}
```

HTTP status: 400 validation, 401 unauthenticated, 403 wrong tenant/role, 404 not found, 409 conflict, 429 rate limit.

## Alignment with PyPOS

Payload shapes for transactions, closures, warehouse, and campaigns should stay aligned with PyPOS serializers under `pos/integration/gate/serializers/` and the cart snapshot contract described in PyPOS campaign/integration docs. When GATE diverges, **schema_version** fields or explicit DRF serializer versions reduce breakage.

## Security

- TLS only in production.  
- Rate limiting per API key and per IP.  
- Audit log for admin and integration configuration changes.

## Related documents

- [06-third-party-integrations.md](06-third-party-integrations.md)
