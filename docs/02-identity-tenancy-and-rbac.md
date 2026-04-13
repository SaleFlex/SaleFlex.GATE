# Identity, tenancy, and access control

## User lifecycle

1. **Registration**  
   A person creates a **user account** (email/username, password, MFA when enabled).

2. **Company association**  
   After signup, the user either:
   - **Creates a new company** (becomes the initial company administrator), or  
   - **Is invited or added** to an existing company.

3. **Joining another user’s company**  
   Self-service “join any company” is **not** the default. A user becomes a member of a company created by someone else only when **company administrators** (or a dedicated “org admin” role) **invite** them or **assign** membership. This preserves auditability and prevents unauthorized access to sales and stock data.

## Hierarchy (conceptual)

```
User ──membership──▶ Company ──contains──▶ Store(s) ──registers──▶ Terminal / device profiles
```

- **Company** — legal or logical tenant: branding, fiscal settings, integration credentials (where shared), user roster.  
- **Store** — physical or logical location: address, timezone, warehouse context, registers.  
- **Terminal profile** — a bound **PyPOS** or **KITCHEN** (or future) instance with credentials and sync policy.

## Roles (draft)

Exact role names are implementation details; conceptually:

| Capability | Typical holder |
|------------|----------------|
| Manage company settings, billing, integrations | Company owner / admin |
| Manage users and invitations | Company admin |
| Manage stores and terminals | Store manager / company admin |
| View reports across stores | Finance / area manager |
| Day-to-day POS | Cashier (often local to PyPOS, not full GATE admin) |

**Separation:** GATE may distinguish **hub users** (web/mobile management) from **cashier identities** that exist primarily on the POS database but can be linked for auditing when required.

## Authentication for APIs

- **User JWT** — mobile apps and SPA-style clients after login.  
- **Device or API credentials** — PyPOS/KITCHEN long-lived tokens or client credentials, scoped to one terminal profile and store.  
- Claims should carry **company_id**, **store_id**, and **terminal_id** (or equivalent) for authorization middleware.

## Related documents

- [03-stores-terminals-and-kitchen.md](03-stores-terminals-and-kitchen.md)  
- [04-rest-api-conventions.md](04-rest-api-conventions.md)
