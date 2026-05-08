# Cashier: universal GATE user (custom `AUTH_USER_MODEL`)

> **File name:** `11-gate-user-model.md` — kept for existing links. The previous `GateUser` + separate `auth.User` profile has been replaced by a single **`core.models.Cashier`** model that **is** Django’s user (`settings.AUTH_USER_MODEL = 'core.Cashier'`).

This document describes:

- **`Cashier`** (`core/models/cashier.py`) — Django authentication user plus shared identity fields (avatar, POS PIN, cashier number, soft-delete).
- **`CompanyMembership`** (`core/models/company_membership.py`) — **per-company** roles so the same person can be owner in one tenant, POS cashier in another, store manager elsewhere, etc.
- **`CashierStoreAssignment`** (`core/models/cashier_store_assignment.py`) — **per-store** POS device access for users who are authorised to work the floor.

## Motivation

Previously, a `GateUser` profile row duplicated company-level concepts (`is_company_owner`, `is_company_admin`) on a single extension table keyed 1:1 to `auth.User`. That does not work when one user owns **multiple** companies or needs **different** roles per company.

The ecosystem requirement is unchanged: **one identity** is shared across GATE portal, SaleFlex.OFFICE, PyPOS, and mPOS. That identity is now the **`Cashier`** row itself (no separate `User` + profile split).

## Cashier

```
core/models/cashier.py  →  class Cashier(AbstractUser, BaseModel)
```

`Cashier` subclasses Django’s **`AbstractUser`** and **`BaseModel`**. It is the only user table for session login, audit FKs (`created_by` / `updated_by` on other models), and portal registration.

### Fields (beyond `AbstractUser`)

| Field | Type | Notes |
|-------|------|-------|
| `avatar` | `FileField` | JPG/PNG/GIF/WebP; portal header; sync to clients |
| `cashier_number` | `PositiveIntegerField` (nullable) | Numeric ID for transaction attribution |
| `pin_code` | `CharField(8)` | Quick login on POS / kitchen / mPOS |
| `is_deleted` | `BooleanField` | Soft-delete; record retained for audit |

Login eligibility uses Django’s built-in **`is_active`** on the user (`AbstractUser`).

**Not** on `Cashier`: company owner/admin/store/POS/OFFICE flags — those live on **`CompanyMembership`** for the relevant company.

### Helper methods

| Method / property | Returns |
|-------------------|---------|
| `display_name` | Full name when set, `username` otherwise |
| `get_store_assignments()` | Active `CashierStoreAssignment` rows |
| `get_accessible_pos_devices(store)` | Delegates to the assignment for that store, if any |

### DB table

`Cashier` (explicit `db_table`).

---

## CompanyMembership (per-company roles)

```
core/models/company_membership.py  →  class CompanyMembership
```

| Field | Meaning |
|-------|---------|
| `is_owner` | Owner tag: deletion workflow, grant owner tag; see [09-portal-companies-ownership-and-deletion.md](09-portal-companies-ownership-and-deletion.md) |
| `is_admin` | Company administrator (portal operations; not owner-only actions) |
| `is_store_manager` | May manage store configuration, staff, and reports **for this company** |
| `is_pos_cashier` | May operate POS **for this company** when `CashierStoreAssignment` rows exist |
| `is_office_user` | May use SaleFlex.OFFICE **for this company’s** data |

The same `Cashier` can have different booleans on different `CompanyMembership` rows.

---

## CashierStoreAssignment

```
core/models/cashier_store_assignment.py  →  class CashierStoreAssignment
```

Records **which store** (and optionally which **POS devices**) a cashier may use. Multi-store support: many assignments per cashier.

### Fields

| Field | Type | Notes |
|-------|------|-------|
| `cashier` | `ForeignKey("Cashier")` | `related_name="store_assignments"` |
| `store` | `ForeignKey("Store")` | `related_name="cashier_assignments"` |
| `pos_devices` | `M2M("PointOfSale")` | Ignored when `can_access_all_pos` is True |
| `can_access_all_pos` | `BooleanField` | All active POS in the store |
| `is_active` | `BooleanField` | Inactive rows ignored |
| Audit | from `BaseModel` | `created_by`, `updated_by`, timestamps |

**Unique constraint:** `(cashier, store)` — one assignment row per cashier per store.

### Helper

`get_accessible_pos_devices()` — all active store POS if `can_access_all_pos`, else the M2M subset.

---

## Role hierarchy (conceptual)

```
Cashier (AUTH_USER_MODEL)
    │
    ├── CompanyMembership (per company)
    │       is_owner, is_admin, is_store_manager, is_pos_cashier, is_office_user
    │
    └── CashierStoreAssignment (per store / device)
              store, can_access_all_pos, pos_devices
```

Company **owner** and **admin** rules in the portal are unchanged; they are driven by `CompanyMembership.is_owner` / `is_admin`, not by fields on `Cashier`.

---

## API sync payload (target)

When OFFICE, PyPOS, or mPOS authenticates against GATE, the user payload will include at minimum:

| Field | Source |
|-------|--------|
| `username`, `first_name`, `last_name`, `email` | `Cashier` (`AbstractUser`) |
| `cashier_number`, `pin_code` | `Cashier` |
| `avatar_url` | `Cashier.avatar` |
| `company_roles` | `CompanyMembership` rows for that user (per company) |
| `store_assignments` | `CashierStoreAssignment` rows |

The exact serializer shape belongs in the REST layer (`pos_api_app`; see [04-rest-api-conventions.md](04-rest-api-conventions.md)).

---

## Django Admin

- **`Cashier`** — `core/admin.py`: `CashierAdmin` (`UserAdmin` subclass) with GATE profile fieldsets, audit fields, and `CashierStoreAssignmentInline`.
- **`CashierStoreAssignment`** — separate `ModelAdmin` with `filter_horizontal` for `pos_devices`.

---

## Settings

`gate_project/settings.py` defines:

```python
AUTH_USER_MODEL = 'core.Cashier'
```

---

## Creating / migrating

```bash
python manage.py makemigrations
python manage.py migrate
```

Switching from an older `auth.User` + `GateUser` schema requires a **data migration** or rebuild in development (fresh DB). This repository often omits committed migration files; generate them locally after clone (see [README.md](README.md) in `docs/`).

---

## Related documents

- [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md) — tenancy overview.
- [09-portal-companies-ownership-and-deletion.md](09-portal-companies-ownership-and-deletion.md) — owner tag and administrator rules.
- [12-core-app.md](12-core-app.md) — `core` app layout and `BaseModel`.
- [10-shared-models-package.md](10-shared-models-package.md) — `web_ui_app.models` shim notes.
- [04-rest-api-conventions.md](04-rest-api-conventions.md) — REST conventions.
