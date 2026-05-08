# Legacy shared models package: web_ui_app/models/

This document records the old `web_ui_app/models/` package split. Current model ownership has moved to the central `core` app; `web_ui_app.models` is now only a backward-compatible re-export shim.

## Background

Prior to this change, all `web_ui_app` models lived in a single `web_ui_app/models.py` file. As the portal domain grew (user profiles, companies, memberships, join requests, and multi-owner deletion workflows) the file became long enough to impede navigation and review. Splitting into per-model modules is the standard Django convention for non-trivial apps and makes each concern independently readable and auditable.

## Current layout

```
core/
└── models/
    ├── __init__.py              # Re-exports every model; public surface
    ├── base.py                  # BaseModel audit/timestamp fields
    ├── company.py               # Company
    ├── company_membership.py    # CompanyMembership
    ├── company_join_request.py  # CompanyJoinRequest
    └── company_deletion.py      # CompanyDeletionRequest, CompanyDeletionApproval
```

> **Note:** `UserProfile` was removed in favour of **`core.models.Cashier`** as Django’s **`AUTH_USER_MODEL`** (shared identity for GATE, OFFICE, PyPOS, and mPOS). See [11-gate-user-model.md](11-gate-user-model.md).

### Module responsibilities

| Module | Models |
|--------|--------|
| `company.py` | `Company` — portal tenant; name, slug (unique, fixed after creation), optional UK limited-company registration fields. |
| `company_membership.py` | `CompanyMembership` — cashier ↔ company link; `is_owner`, `is_admin`, `is_store_manager`, `is_pos_cashier`, `is_office_user`; unique per (company, user). |
| `company_join_request.py` | `CompanyJoinRequest` — pending/approved/rejected join requests submitted by users via slug. |
| `company_deletion.py` | `CompanyDeletionRequest` + `CompanyDeletionApproval` — multi-owner deletion workflow; company is removed when every current owner has approved. |

## Public surface

New code imports from `core.models`:

```python
from core.models import Cashier, Company, CompanyMembership
```

`web_ui_app/models/__init__.py` remains a shim that re-exports from `core.models` so older callers are not affected:

```python
from web_ui_app.models import Company, CompanyMembership, ...
# or within the app:
from .models import Company, CompanyMembership, ...
```

No import path in `admin.py`, `forms.py`, `company_permissions.py`, or any view module needed to change.

Session-authenticated portal code uses `request.user`, which is a **`Cashier`** instance:

```python
from django.contrib.auth import get_user_model

User = get_user_model()  # core.Cashier
assert request.user.username
```

Avatar and profile edits use the same model (no separate `get_or_create` profile row).

## Intra-package imports

Within `core/models/`, modules import from each other using relative imports where a dependency exists:

- `company_membership.py` imports `Company` from `.company`
- `company_join_request.py` imports `Company` from `.company`
- `company_deletion.py` imports `Company` from `.company`

`company.py` has no intra-package dependencies.

## Django app label

The Django **app label** for these models is now `core`. Migrations for model changes are generated with `python manage.py makemigrations core`.

## Adding new models

Create a new module in `core/models/` and inherit from `BaseModel` for normal domain models. Add it to `core/models/__init__.py`:

```python
# core/models/__init__.py
from .store import Store          # new line
__all__ = [..., "Store"]          # add to __all__
```

Then run `python manage.py makemigrations core` as usual.

## Related documents

- [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md) — ecosystem tenancy and RBAC overview.
- [09-portal-companies-ownership-and-deletion.md](09-portal-companies-ownership-and-deletion.md) — portal company rules, owner tag, deletion workflow.
- [12-core-app.md](12-core-app.md) — current central model layer and `BaseModel` guidance.
