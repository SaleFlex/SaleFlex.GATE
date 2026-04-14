> **Under development.** The project is not production-ready yet. APIs and data models described here reflect the **target architecture** aligned with [SaleFlex.PyPOS](https://github.com/SaleFlex/SaleFlex.PyPOS).

# SaleFlex.GATE

**SaleFlex.GATE** is the central **hub** for the SaleFlex ecosystem: a **Django** and **Django REST Framework** backend that ties together stores, terminals, restaurant flows, mobile apps, and optional third-party systems.

It is the primary integration point for **[SaleFlex.PyPOS](https://github.com/SaleFlex/SaleFlex.PyPOS)** (touch POS), **[SaleFlex.KITCHEN](https://github.com/SaleFlex/SaleFlex.KITCHEN)** (kitchen / production display where applicable), and future **[SaleFlex.POS](https://github.com/SaleFlex/SaleFlex.POS)** clients. PyPOS connects through `pos/integration/gate/` (HTTP client, auth, push/pull sync, offline outbox) as documented in PyPOS [Integration Layer](https://github.com/SaleFlex/SaleFlex.PyPOS/blob/main/docs/40-integration-layer.md).

---

## Key Features

- **Multi-tenant hub** — Companies, stores, and terminal profiles as the basis for isolating data and API access.
- **Django REST Framework** — Versioned JSON APIs for devices (PyPOS, KITCHEN) and mobile clients; merchant token authentication (see `pos_api_app.authentication`).
- **POS-aligned domain models** — Merchant, store, POS, closure, warehouse, customer, and related reference entities under `pos_api_app` (evolving toward full sync with PyPOS payloads).
- **Django Admin** — Built-in staff site for direct ORM/data management (`/admin/`). It is not the primary place for end-user account tasks.
- **Web UI & public portal** — `web_ui_app` provides a landing page (guests), session login/register/logout, **portal-only** change password (`/accounts/password/change/`, templates under `web_ui_app/templates/web_ui_app/`), a signed-in **left sidebar** (dashboard, **companies**, profile, password, plus “coming soon” placeholders), **company creation** and **join-by-slug requests** with **owner tag** vs **administrator** rules, multi-owner **deletion approvals**, a dashboard stub, an account menu (avatar with default placeholder, profile edit, settings submenu with change password), and optional profile picture uploads; ERP-style screens will extend this.
- **Integration gateway** — Designed to front ERP, loyalty, campaign, and payment adapters so edge apps stay thin.
- **Reporting & back office (roadmap)** — Aggregated sales, stock, and KPIs via web UI and APIs.
- **Open source** — Extend and deploy for your own infrastructure.

---

## Architecture Overview

GATE sits between **edge clients** (POS, kitchen, mobile) and **optional enterprise systems**. Clients authenticate and call REST endpoints; the hub persists and routes data according to company/store scope.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Clients (HTTPS)                             │
│  SaleFlex.PyPOS · SaleFlex.KITCHEN · Mobile apps · Future SPA   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SaleFlex.GATE (Django)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ Django Admin │  │ REST (DRF)   │  │ Web UI (web_ui_app)    │ │
│  │ staff / data │  │ + auth       │  │ landing + portal auth  │ │
│  └──────────────┘  └──────────────┘  └────────────────────────┘ │
│                             │                                   │
│  ┌──────────────────────────┴───────────────────────────────┐   │
│  │  Domain layer: merchants, stores, POS, closures, stock   │   │
│  └──────────────────────────┬───────────────────────────────┘   │
└─────────────────────────────┼───────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────────┐
        │ SQLite / │   │ ERP      │   │ Loyalty /    │
        │ Postgres │   │ adapters │   │ Campaign /   │
        │ (DB)     │   │ (future) │   │ Payment      │
        └──────────┘   └──────────┘   └──────────────┘
```

**Layers (conceptual):**

- **API layer** — DRF views/serializers (to be expanded), authentication, throttling, versioning (`/api/v1/...` target; see [docs/04-rest-api-conventions.md](docs/04-rest-api-conventions.md)).
- **Application layer** — Services for sync ingestion, reporting, and integration jobs (strengthened over time).
- **Data layer** — Django ORM models in `pos_api_app` (and future apps) backed by SQLite (dev) or PostgreSQL (recommended production).

---

## Project Structure

```
SaleFlex.GATE/
├── manage.py                 # Django entry point
├── requirements.txt          # django, djangorestframework
├── db.sqlite3                # Default dev DB (after migrate; may be gitignored)
├── staticfiles/              # After collectstatic (gitignored; not shipped in the repo)
│
├── gate_project/             # Project settings package
│   ├── settings.py           # INSTALLED_APPS, REST_FRAMEWORK, DATABASES
│   ├── urls.py               # Root URLconf (admin, future API includes)
│   ├── wsgi.py
│   └── asgi.py
│
├── pos_api_app/              # POS / merchant API app
│   ├── authentication/       # e.g. MerchantTokenAuthentication
│   ├── models/               # Merchant, Store, Pos, Closure, Warehouse, …
│   ├── admin.py
│   ├── apps.py
│   └── tests.py
│
├── web_ui_app/               # Public landing + session auth; base for future ERP-style UI
│   ├── forms.py              # Registration (UserCreationForm extension)
│   ├── context_processors.py # gate_user_profile for header avatar
│   ├── urls.py               # /, /dashboard/, /accounts/...
│   ├── static/web_ui_app/    # Portal CSS, favicon, and optional JS (Django staticfiles)
│   │   ├── css/base.css
│   │   ├── icons/favicon.svg
│   │   ├── icons/avatar-default.svg
│   │   └── js/               # e.g. user-menu.js for account dropdown
│   ├── templates/            # Landing, login/register, profile, password_change (portal chrome)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             # UserProfile; portal Company, membership, join & deletion flows
│   ├── views.py
│   └── tests.py
│
└── docs/                     # Architecture drafts (English)
    ├── README.md
    └── 01-…07-*.md
```

---

## System Requirements

### Runtime

- **Python** 3.12 or newer (required for **Django 6.x**; check [Django supported versions](https://docs.djangoproject.com/en/stable/faq/install/#faq-python-version-support) if you change the Django major version).
- **pip** (current toolchain).

### Python dependencies

Pinned in `requirements.txt` (example versions in-repo):

- `django`
- `djangorestframework`

Uploaded profile pictures are stored under `MEDIA_ROOT` (project `media/` by default, gitignored). Install **Pillow** if you switch the profile field to `ImageField` or need server-side image processing; the stock portal uses `FileField` with extension validation so a basic install works without it.

### Database

- **SQLite** — default in `settings.py` for local development.
- **PostgreSQL** — recommended for production (configure `DATABASES` and drivers when you deploy).

### Optional (future / production)

- Reverse proxy (nginx, Caddy) and TLS termination  
- Redis or similar for caching, sessions, or task queues when async jobs are added  
- Container runtime (Docker) if you package the service

---

## Quick Start

```bash
git clone https://github.com/SaleFlex/SaleFlex.GATE.git
cd SaleFlex.GATE
python -m venv .venv

# Windows
.venv\Scripts\activate.bat

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser   # optional — for Django Admin
python manage.py runserver
```

Open the **public site** (landing for guests): [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
Open **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

> REST API routes are still being expanded. Follow the [Development Roadmap](#development-roadmap) and `docs/` for the target API surface. Browser routes are summarized in [docs/08-public-web-portal-landing-and-accounts.md](docs/08-public-web-portal-landing-and-accounts.md).

---

## Installation & Setup

### Prerequisites

1. Install [Python 3.12+](https://www.python.org/downloads/).
2. Ensure `pip` is available (`python -m pip install --upgrade pip`).

### Steps

1. **Clone the repository** (or extract the sources) and change into the project directory.

2. **Create and activate a virtual environment** (recommended):

   **Windows:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Collect static files** into `staticfiles/` (this folder is gitignored; every fresh clone needs this step so Django Admin assets and `web_ui_app` static files are available when you serve `STATIC_ROOT`):
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

### Configuration notes

- **SECRET_KEY** — Replace the development key in `gate_project/settings.py` before any production deployment; use environment variables or a secrets manager.
- **DEBUG** — Set `DEBUG = False` and configure `ALLOWED_HOSTS` in production.
- **Database** — Point `DATABASES['default']` to PostgreSQL when moving beyond local SQLite.
- **`web_ui_app`** — Enabled in `INSTALLED_APPS` with URLs at the site root (`/`). Adjust `LOGIN_*` / `LOGOUT_REDIRECT_URL` in `settings.py` if you change paths.

### Web UI static files and icons

- **Styles** — Shared layout and components for the portal live in `web_ui_app/static/web_ui_app/css/base.css` and are linked from `templates/web_ui_app/base.html` via `{% static %}`.
- **Favicon** — `web_ui_app/static/web_ui_app/icons/favicon.svg` is referenced as `rel="icon"` (SVG) and `apple-touch-icon` for bookmarks and home-screen shortcuts.
- **JavaScript** — There is no inline script in the current templates; add files under `web_ui_app/static/web_ui_app/js/` and include them from `{% block extra_head %}` (or a dedicated `{% block extra_js %}` if you introduce one) when a page needs behaviour.
- **Collected output** — `STATIC_ROOT` is `staticfiles/` at the project root; it is listed in `.gitignore`. After cloning, run `python manage.py collectstatic --noinput` as part of setup (see [Installation & Setup](#installation--setup)).
- **Production** — Serve the contents of `staticfiles/` behind your web server or CDN (see [Django static files](https://docs.djangoproject.com/en/stable/howto/static-files/deployment/)).

---

## Role in the ecosystem

| Client | Role |
|--------|------|
| **SaleFlex.PyPOS** | Store-floor POS: sales, payments, closure, local warehouse movements, campaigns/loyalty (local or GATE-managed). Syncs transactions, closures, stock events, and pulls master data and campaign definitions from GATE when enabled. |
| **SaleFlex.KITCHEN** | Restaurant kitchen line: order display and preparation workflow; registered per store like a terminal profile. |
| **Django web UI** | Administration and **ERP-style** operational screens (master data, purchasing-style flows, configuration). |
| **Mobile apps** | Same REST surface as POS/kitchen: management, stocktake, waiter ordering, and reporting (see below). |
| **Third-party systems** | ERP, loyalty, campaign orchestration, payment switches—connected via GATE as the integration boundary. |

---

## Tenancy: accounts, companies, and stores

1. **User account**  
   When a user registers, they either **create their own company (or companies)** or are **added to an existing company**.

2. **Joining another company**  
   Membership in a company defined by someone else is granted only by **company administrators** (or equivalent “manage users / organization” role). Self-service join without admin approval is not the default model.

3. **Company → stores**  
   Under each company, one or more **stores** (locations) are defined.

4. **Store → terminals**  
   Each store has one or more **POS terminal registrations** (SaleFlex.PyPOS instances: identity, credentials, sync policy).  
   For restaurants, the same store may also register **SaleFlex.KITCHEN** application instances.

This hierarchy is the basis for **authorization**, **data partitioning**, and **API scoping** (JWT / API keys bound to company, store, and device).

The **session portal** now persists companies and membership in `web_ui_app` (**owner tag**, **administrator**, join-by-slug, multi-owner deletion). Details: [docs/09-portal-companies-ownership-and-deletion.md](docs/09-portal-companies-ownership-and-deletion.md). Mapping to `pos_api_app.Merchant` and device APIs is still to be aligned.

---

## REST API and clients

- **Django REST Framework** exposes versioned APIs for:
  - Authentication and device/session management  
  - Company and store configuration  
  - Product and price distribution, campaigns, notifications (consumed by PyPOS pull/sync)  
  - Transaction and closure ingestion (PyPOS push)  
  - Warehouse events and stock alignment (where GATE is authoritative)  
  - Kitchen / order flows where GATE is the hub  

- **Mobile applications** (outside the Django HTML UI) authenticate against the same APIs:
  - **Operations / management:** companies, stores, POS (and kitchen) definitions, dashboards, **reports**.  
  - **Stocktake / inventory counting:** field staff at stores; mobile captures counts and adjustments according to store policy.  
  - **Waiter / table service:** order capture for restaurant scenarios, aligned with kitchen and POS backends.

Detailed drafts: [docs/README.md](docs/README.md).

---

## Third-party integrations

GATE is designed as the **integration gateway** so edge clients stay simple. Examples of external systems:

- **ERP** — items, cost centers, purchase orders, financial postings (adapter-specific).  
- **Loyalty** — member lookup, earn/burn rules, balances (may override or complement PyPOS local loyalty when `gate.manages_*` flags apply).  
- **Campaign** — central promotion engine and coupon validation when campaign management is delegated to GATE (see PyPOS `gate.manages_campaign`).  
- **Payment** — routing to PSPs, reconciliation, or terminal orchestration where applicable.

Connectors are intended to live behind clear **service interfaces** so core REST and web UI do not embed vendor-specific logic.

---

## Web application: ERP-style UI and reporting

Beyond REST consumers, GATE ships (or will ship) **Django-based web interfaces** that provide:

- **ERP-like** operational depth: organizational setup, master data, inventory and procurement-style processes as the product matures.  
- **Reporting:** aggregated sales, stock, and operational KPIs across companies and stores, exportable and suitable for management users.

---

## Documentation

| Resource | Description |
|----------|-------------|
| [docs/README.md](docs/README.md) | Documentation index (draft). |
| [docs/01-ecosystem-and-boundaries.md](docs/01-ecosystem-and-boundaries.md) | How GATE relates to PyPOS, KITCHEN, mobile, and third parties. |
| [docs/02-identity-tenancy-and-rbac.md](docs/02-identity-tenancy-and-rbac.md) | Accounts, companies, store membership, admin-invited users. |
| [docs/03-stores-terminals-and-kitchen.md](docs/03-stores-terminals-and-kitchen.md) | Stores, PyPOS and KITCHEN registration. |
| [docs/04-rest-api-conventions.md](docs/04-rest-api-conventions.md) | API style, auth, versioning (draft). |
| [docs/05-mobile-client-scenarios.md](docs/05-mobile-client-scenarios.md) | Management, stocktake, waiter apps. |
| [docs/06-third-party-integrations.md](docs/06-third-party-integrations.md) | ERP, loyalty, campaign, payment. |
| [docs/07-web-ui-erp-and-reporting.md](docs/07-web-ui-erp-and-reporting.md) | Django UI and reporting scope. |
| [docs/08-public-web-portal-landing-and-accounts.md](docs/08-public-web-portal-landing-and-accounts.md) | Landing page and session account URLs (`web_ui_app`). |
| [docs/09-portal-companies-ownership-and-deletion.md](docs/09-portal-companies-ownership-and-deletion.md) | Portal companies, owner tag vs administrator, join requests, deletion approvals. |

---

## Development Roadmap

### Platform & security

- [ ] Production settings: environment-based `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, HTTPS headers  
- [ ] PostgreSQL configuration template and migration path from SQLite  
- [ ] Rate limiting and structured logging for API access  

### Data model & tenancy

- [x] First-class **user ↔ company** membership and **admin-approved join** (portal: `web_ui_app` companies + join requests; REST/Merchant linkage pending)  
- [ ] RBAC roles scoped by company and store  
- [ ] Terminal/device registry linked to **PyPOS** / **KITCHEN** identities and sync policy  

### REST API

- [ ] Versioned public API (`/api/v1/`) with OpenAPI schema  
- [ ] Push endpoints: transactions, closures, warehouse events (aligned with PyPOS serializers)  
- [ ] Pull endpoints: products, prices, campaigns, notifications  
- [ ] JWT (users) vs long-lived device tokens — documented in [docs/04-rest-api-conventions.md](docs/04-rest-api-conventions.md)  

### Web & mobile consumers

- [ ] Multi-store and multi-terminal management in web UI  
- [x] Register `web_ui_app` — landing, session register/login/logout, portal password change (not Django Admin), dashboard stub, **sidebar portal nav**, **companies** (create, join requests, owner/admin rules, multi-owner delete)  
- [ ] ERP-style operational screens beyond the portal stub  
- [ ] Mobile-oriented endpoints: management dashboards, stocktake sessions, waiter/order flows  

### Integrations & reporting

- [ ] Third-party adapter framework (ERP, loyalty, campaign, payment)  
- [ ] Reporting layer: sales, stock, campaign/loyalty KPIs, exports  

---

## Related repositories

- [SaleFlex.PyPOS](https://github.com/SaleFlex/SaleFlex.PyPOS) — Python/PySide6 POS (GATE integration in `pos/integration/gate/`).  
- [SaleFlex.KITCHEN](https://github.com/SaleFlex/SaleFlex.KITCHEN) — Kitchen client.  
- [SaleFlex.POS](https://github.com/SaleFlex/SaleFlex.POS) — Related POS line (ecosystem).  

---

## Contributors

<table>
<tr>
    <td align="center">
        <a href="https://github.com/ferhat-mousavi">
            <img src="https://avatars.githubusercontent.com/u/5930760?v=4" width="100;" alt="Ferhat Mousavi"/>
            <br />
            <sub><b>Ferhat Mousavi</b></sub>
        </a>
    </td>
</tr>
</table>

## Donation and Support

If you like the project and want to support it or if you want to contribute to the development of new modules, you can donate to the following crypto addresses.

- USDT: `0xa5a87a939bfcd492f056c26e4febe102ea599b5b`
- BUSD: `0xa5a87a939bfcd492f056c26e4febe102ea599b5b`
- BTC: `15qyZpi6HjYyVhKKBsCbZSXU4bLdVJ8Phe`
- ETH: `0xa5a87a939bfcd492f056c26e4febe102ea599b5b`
- SOL: `Gt3bDczPcJvfBeg9TTBrBJGSHLJVkvnSSTov8W3QMpQf`
