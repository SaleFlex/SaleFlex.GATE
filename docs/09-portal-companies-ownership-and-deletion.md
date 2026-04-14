# Portal companies: ownership tag, administrators, join requests, deletion

This document describes the **first web portal implementation** of hub **companies** in `web_ui_app`. It complements the conceptual tenancy notes in [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md).

## Scope

- **Portal-only models** — `Company`, `CompanyMembership`, `CompanyJoinRequest`, `CompanyDeletionRequest`, and `CompanyDeletionApproval` live in `web_ui_app`. They are the **browser session** source of truth for organization membership until the same rules are mirrored on REST APIs and optionally linked to `pos_api_app.Merchant`.
- **Signed-in layout** — Dashboard, profile, password change, and company pages use a **left sidebar** listing portal areas. Items such as stores and reporting are visible as **Coming soon** placeholders.

## Roles: owner tag vs administrator

| Concept | Meaning |
|--------|---------|
| **Owner tag** (`is_owner` on `CompanyMembership`) | Marks **legal/organizational ownership** of the tenant. It is **not** delegated RBAC in the sense that **no one else can remove** another user’s owner tag—**not even another owner**. Only the **same user** can remove their own owner tag, and **only if at least one other owner** remains. |
| **Administrator** (`is_admin`) | **Company administrator**: treated like a **super-user for portal operations** (members, join requests, granting/revoking administrator on others). Administrators **cannot** delete the company and **cannot** change anyone’s **owner tag** (grant or remove). |
| **Member** | Default membership after an approved join; no owner tag and not an administrator until granted. |

**Effective power users:** anyone who is **owner or administrator** can perform all **routine** portal management **except** the owner-only actions below.

### Owner-only actions

- **Start company deletion** (see multi-owner approval below).
- **Assign the owner tag** to another user (existing member or newly created membership row).

### Administrator-only collaboration rules

- **Grant administrator** to a member: owners **or** administrators.
- **Revoke administrator** from a member who is **not** an owner: **owners**, or **another administrator** from a **different** user (administrators cannot use this flow to revoke **their own** administrator flag; another admin or an owner must do it).
- **Approve or reject join requests**: owners **or** administrators.

### Creating a company

The user who creates a company receives **both** `is_owner=True` and `is_admin=True` on `CompanyMembership`.

### Joining a company

Users submit a **join request** using the company **slug**. An **owner** or **administrator** approves or rejects. Approval creates a **member** row without owner or administrator flags unless changed later.

### Company deletion

- **Only owners** may start deletion or approve a pending deletion.
- **Single owner:** starting deletion records that owner’s approval and **immediately deletes** the company (the only owner has already consented).
- **Multiple owners:** a **pending deletion** record collects **one approval per current owner**. The company is removed only when the set of **approvals covers every user who is an owner at completion time** (so a newly added owner must also approve if they appear before deletion completes).

Removing the **last** owner tag is **blocked** in the UI and views: the company must keep **at least one** owner until it is deleted.

## URLs (session-authenticated)

| Path | Description |
|------|-------------|
| `/companies/` | List companies the user belongs to, with owner/admin/member tags. |
| `/companies/create/` | Create a company (creator becomes owner + administrator). |
| `/companies/join/` | Request to join by slug. |
| `/companies/<slug>/` | Company home: members, join queue (if privileged), owner assignment, deletion workflow. |
| POST `/companies/<slug>/join/<id>/approve/` | Approve a join request. |
| POST `/companies/<slug>/join/<id>/reject/` | Reject a join request. |
| POST `/companies/<slug>/members/<user_id>/grant-admin/` | Grant administrator. |
| POST `/companies/<slug>/members/<user_id>/revoke-admin/` | Revoke administrator (rules above). |
| POST `/companies/<slug>/owners/grant/` | Assign owner tag (owners only). |
| POST `/companies/<slug>/owners/self-remove/` | Remove **your own** owner tag if another owner exists. |
| POST `/companies/<slug>/delete/initiate/` | Start deletion (owners only). |
| POST `/companies/<slug>/delete/approve/` | Approve pending deletion (owners only). |

## Related code

- Models: `web_ui_app/models.py` (`Company`, `CompanyMembership`, …).
- Rules and deletion completion: `web_ui_app/company_permissions.py`.
- Views: `web_ui_app/company_views.py`, URLs in `web_ui_app/urls.py`.
- Layout: `web_ui_app/templates/web_ui_app/portal_base.html`, `web_ui_app/templates/web_ui_app/_portal_nav.html`, styles in `web_ui_app/static/web_ui_app/css/base.css`.

## Related documents

- [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md) — ecosystem tenancy overview.  
- [08-public-web-portal-landing-and-accounts.md](08-public-web-portal-landing-and-accounts.md) — landing, auth, and portal chrome.
