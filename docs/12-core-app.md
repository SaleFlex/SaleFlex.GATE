# `core` app — centralised model layer

This document describes the `core` Django application introduced to unify all shared models
under a single, authoritative source.

## Why a separate `core` app?

Previously models were split across two apps:

| App | Models it owned | Problem |
|-----|----------------|---------|
| `pos_api_app` | `Cashier`, `CashierStoreAssignment`, POS domain (Merchant, Store, PointOfSale, Closure, Warehouse, …) | Not the right home for portal/company models |
| `web_ui_app` | `Company`, `CompanyMembership`, `CompanyJoinRequest`, `CompanyDeletionRequest/Approval` | Not the right home for POS/identity models |

All SaleFlex applications (GATE portal, OFFICE, PyPOS, mPOS) need to consume the same
entities. A `core` app makes the ownership unambiguous:

- **One migration source** — all tables live under `core_*` prefix; `pos_api_app` and
  `web_ui_app` have zero migrations.
- **One import path** — `from core.models import Cashier, Store, Company, …`
- **One audit base** — concrete core models inherit `created_by`, `updated_by`,
  `created_at`, and `updated_at` from `core.models.BaseModel`.
- **Clean separation** — `pos_api_app` = API authentication + views; `web_ui_app` = portal
  views, forms, templates; `core` = data layer.

---

## Package layout

```
core/
├── __init__.py
├── apps.py                      # CoreConfig — verbose_name = "SaleFlex Core"
├── admin.py                     # All model admin registrations
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py          # Single migration for all core models
└── models/
    ├── __init__.py              # Re-exports every model; full __all__
    ├── base.py                  # BaseModel — shared audit/timestamp fields
    │
    ├── cashier.py               # Cashier — AUTH_USER_MODEL (AbstractUser + BaseModel)
    ├── cashier_store_assignment.py  # CashierStoreAssignment — per-store POS access
    │
    ├── company.py               # Company
    ├── company_membership.py    # CompanyMembership
    ├── company_join_request.py  # CompanyJoinRequest
    ├── company_deletion.py      # CompanyDeletionRequest, CompanyDeletionApproval
    │
    ├── merchant.py              # Merchant
    ├── store.py                 # Store
    ├── pos.py                   # PointOfSale
    ├── closure.py               # Closure
    ├── closure_cashier.py       # ClosureCashier
    ├── closure_currency.py      # ClosureCurrency
    ├── closure_department.py    # ClosureDepartment
    ├── closure_payment.py       # ClosurePayment
    ├── closure_vat.py           # ClosureVat
    ├── warehouse.py             # Warehouse
    ├── warehouse_product.py     # WarehouseProduct
    ├── warehouse_transaction.py # WarehouseTransaction
    ├── customer.py              # Customer
    ├── customer_type.py         # CustomerType
    ├── contact.py               # Contact
    ├── contact_authority.py     # ContactAuthority
    ├── contact_position.py      # ContactPosition
    ├── merchant_api_token.py    # MerchantAPIToken
    ├── merchant_activity_sector.py     # MerchantActivitySector
    ├── merchant_business_operation_type.py  # MerchantBusinessOperationType
    ├── merchant_company_type.py        # MerchantCompanyType
    ├── pos_currency.py          # PosCurrency
    ├── pos_department.py        # PosDepartment
    ├── pos_form.py              # PosForm
    ├── pos_form_control.py      # PosFormControl
    ├── pos_label_value.py       # PosLabelValue
    ├── pos_payment_type.py      # PosPaymentType
    ├── pos_vat.py               # PosVat
    ├── city.py                  # City
    ├── state.py                 # State
    ├── country.py               # Country
    └── tag.py                   # Tag
```

---

## Importing models

Always import directly from `core.models`:

```python
from core.models import Cashier, Store, Company, Merchant, PointOfSale
```

### Backward-compatible shims

`pos_api_app/models/__init__.py` and `web_ui_app/models/__init__.py` are thin shims that
re-export from `core.models`. This means existing code using `from pos_api_app.models import …`
or `from web_ui_app.models import …` (or the relative `from .models import …` inside each app)
continues to work without changes.

**New code should always use `from core.models import …` directly.**

---

## BaseModel

All concrete models in `core/models/` should inherit from `BaseModel` unless there is a
specific reason not to. The **`Cashier`** user model is the exception: it subclasses
**`AbstractUser`** and **`BaseModel`** (see [11-gate-user-model.md](11-gate-user-model.md)).
Other domain models should use `BaseModel` only. The abstract base provides:

| Field | Type | Notes |
|-------|------|-------|
| `created_by` | `ForeignKey(AUTH_USER_MODEL, SET_NULL)` | Nullable audit user. |
| `updated_by` | `ForeignKey(AUTH_USER_MODEL, SET_NULL)` | Nullable audit user. |
| `created_at` | `DateTimeField(auto_now_add=True)` | Creation timestamp. |
| `updated_at` | `DateTimeField(auto_now=True)` | Last update timestamp. |

The audit user fields use Django's abstract-model placeholders in `related_name`
(`%(app_label)s_%(class)s_created` / `%(app_label)s_%(class)s_updated`) so reverse
relations remain unique after inheritance.

When adding a new model, do **not** redeclare these four fields in the model file. **`Cashier`** already inherits `BaseModel` **and** `AbstractUser`; other domain models should use `BaseModel` only unless you intentionally extend auth.

---

## Admin

All model admin classes are registered in `core/admin.py`.

`pos_api_app/admin.py` and `web_ui_app/admin.py` are intentionally empty (contain only
`from django.contrib import admin`) so future app-specific admin extensions can be added there
without conflict.

---

## Adding a new model

1. Create `core/models/<model_name>.py`.
2. Inherit from `BaseModel` for normal domain models:

   ```python
   from .base import BaseModel

   class Example(BaseModel):
       ...
   ```

3. Add the import and `__all__` entry to `core/models/__init__.py`.
4. Run `python manage.py makemigrations core`.
5. Register the model in `core/admin.py` if needed.

---

## INSTALLED_APPS order

```python
INSTALLED_APPS = [
    # Django built-ins …
    'rest_framework',
    'core',        # ← data layer; must come before pos_api_app and web_ui_app
    'pos_api_app', # ← API auth + views only
    'web_ui_app',  # ← portal views, forms, templates only
]
```

`core` must appear **before** the other two apps so Django resolves the model registry in the
correct order when lazy FK strings like `"Cashier"` are evaluated.

---

## Related documents

- [11-gate-user-model.md](11-gate-user-model.md) — `Cashier`, `CompanyMembership`, and `CashierStoreAssignment`.
- [10-shared-models-package.md](10-shared-models-package.md) — legacy `web_ui_app/models/` package notes (now a shim).
- [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md) — identity and tenancy overview.
- [04-rest-api-conventions.md](04-rest-api-conventions.md) — REST API conventions for `pos_api_app`.
