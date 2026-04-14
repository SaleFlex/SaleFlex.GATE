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

- **Company** — legal or logical tenant: branding, fiscal settings, integration credentials (where shared), user roster. In the session portal (`web_ui_app.Company`), optional fields `companies_house_number`, `vat_number`, and `registered_office` capture typical **UK limited company** registration data; only the **display name** is required when creating a company (see [09-portal-companies-ownership-and-deletion.md](09-portal-companies-ownership-and-deletion.md)).  
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

### Portal implementation: owner tag vs administrator (`web_ui_app`)

The session portal now models two flags on **company membership** (see [09-portal-companies-ownership-and-deletion.md](09-portal-companies-ownership-and-deletion.md)):

- **Owner tag** — marks **ownership** of the portal company. It is **not** removable by other users (including co-owners). Only the **same account** may remove its own owner tag, and only while **another owner** exists. Owners may **assign** the tag to others. **Company deletion** is an **owner-only** flow; with **multiple owners**, **every current owner** must **approve** deletion before the company is removed.
- **Administrator** — **full portal management** except deleting the company and changing **owner tags** on others. Administrators approve join requests and may grant or revoke **administrator** on peers (one administrator cannot revoke **their own** admin flag without another admin or an owner).

Creating a company makes the creator **both** owner and administrator. This is the first slice of **user ↔ company** wiring; REST APIs and linkage to `pos_api_app.Merchant` remain future work.

## Authentication for APIs

- **User JWT** — mobile apps and SPA-style clients after login.  
- **Device or API credentials** — PyPOS/KITCHEN long-lived tokens or client credentials, scoped to one terminal profile and store.  
- Claims should carry **company_id**, **store_id**, and **terminal_id** (or equivalent) for authorization middleware.

## Related documents

- [03-stores-terminals-and-kitchen.md](03-stores-terminals-and-kitchen.md)  
- [04-rest-api-conventions.md](04-rest-api-conventions.md)
