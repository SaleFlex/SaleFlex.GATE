# Public web portal: landing and account pages

## Purpose

The **`web_ui_app`** Django app provides a **browser-facing** entry point alongside Django Admin and REST APIs:

- **Landing** — Project overview and calls to action for visitors who are **not** signed in.
- **Session-based accounts** — Register, log in, log out, and change password using Django’s built-in user model and session authentication.
- **Signed-in chrome** — Authenticated pages use a **left sidebar** (**portal** navigation) for **Dashboard**, **Companies** (list, create, request to join), **Profile**, and **Change password**, plus **Coming soon** placeholders for stores, catalog, reports, integrations, and API keys. The header shows the **brand** link and an **account control**: a **profile avatar** (uploaded picture or a built-in default SVG) that opens a **dropdown menu** with **Profile**, **Settings** (nested **Change password**), and **Log out**, implemented with lightweight JavaScript for open/close and the nested Settings section.

This layer is distinct from **device / merchant token** authentication used by POS clients (see [04-rest-api-conventions.md](04-rest-api-conventions.md)).

## Behaviour

| URL | Visibility | Description |
|-----|------------|-------------|
| `/` | Guests only (signed-in users are redirected) | Landing page describing GATE and linking to register / login. |
| `/dashboard/` | Authenticated | Minimal signed-in home; ERP-style screens will extend this over time. |
| `/accounts/profile/` | Authenticated | Edit **first name**, **last name**, **email**, and optional **profile picture** (password changes stay on the dedicated password form). Persists `User` fields plus a `web_ui_app.UserProfile` row (created on demand). |
| `/accounts/register/` | Guests only (redirect if already signed in) | Create a Django user; optional email field on the form. |
| `/accounts/login/` | Public | Username / password sign-in. |
| `/accounts/logout/` | POST (CSRF-protected) | Ends the session; redirects to `/`. |
| `/accounts/password/change/` | Authenticated | Change password; confirmation at `/accounts/password/change/done/`. Linked from **Settings** in the account dropdown. |
| `/accounts/password/change/done/` | Authenticated | Confirmation after a successful password change. |
| `/companies/` | Authenticated | List companies the user belongs to (owner / administrator / member tags). |
| `/companies/create/` | Authenticated | Create a portal company; creator becomes **owner** and **administrator**. Only the **company name** is required; optional registration fields (Companies House, VAT, registered office) can be filled (see [09-portal-companies-ownership-and-deletion.md](09-portal-companies-ownership-and-deletion.md)). |
| `/companies/join/` | Authenticated | Submit a join request using a company **slug**; owners or administrators approve. |
| `/companies/<slug>/` | Authenticated (member only) | Company detail: members, roles, join queue, owner assignment, deletion approvals. **Owners and administrators** can update the company **name** and optional registration fields (the **slug** does not change). Plain members see a read-only summary when any of those fields are set. |

### Django Admin vs portal password change

**End users** change their own password through the **portal** URLs above (`views.password_change` / `views.password_change_done` in `web_ui_app/views/password_change.py` and `web_ui_app/views/password_change_done.py`, re-exported from `web_ui_app/views/__init__.py`; form `GatePasswordChangeForm` in `web_ui_app/forms.py`; templates `web_ui_app/password_change.html` and `password_change_done.html` extending `portal_base.html` → `base.html`). After a successful change, `update_session_auth_hash` keeps the browser session valid.

**Django Admin** (`/admin/`) remains appropriate for **staff** managing model data; it is not positioned as the main UX for hub users updating their login password.

## Settings

In `gate_project/settings.py`:

- `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` — session auth defaults for the web UI.
- `MEDIA_URL` / `MEDIA_ROOT` — user-uploaded files (profile avatars). The repository `.gitignore` excludes `media/`; configure your host or object storage to serve this path in production (Django’s `static()` helper only wires media URLs when `DEBUG` is true; see [Managing files](https://docs.djangoproject.com/en/stable/topics/files/)).
- `web_ui_app.context_processors.user_profile` — ensures each authenticated request has a `UserProfile` instance (`gate_user_profile` in templates) for the header avatar.
- `web_ui_app` is listed in `INSTALLED_APPS`; root `urls.py` includes `web_ui_app.urls` at `''`.

## Static assets, styles, and icons

Portal **CSS** is kept out of inline `<style>` blocks: shared rules live in `web_ui_app/static/web_ui_app/css/base.css` and are loaded from `web_ui_app/templates/web_ui_app/base.html` using Django’s `static` tag.

**Favicons and touch icons:** `web_ui_app/static/web_ui_app/icons/favicon.svg` is wired as the primary `rel="icon"` (SVG, modern browsers) and as `apple-touch-icon`. Replace or extend this file (for example with PNG sizes) if you need broader legacy support.

**JavaScript:** Shared layout loads `web_ui_app/static/web_ui_app/js/user-menu.js` (deferred, authenticated users only) to toggle the account dropdown and the **Settings** nested menu. Add more scripts under `web_ui_app/static/web_ui_app/js/` and reference them from `block extra_head` or an optional `block extra_scripts` if you introduce one.

`STATIC_ROOT` is the project-level `staticfiles/` directory (gitignored). **Every fresh clone** should run `python manage.py collectstatic --noinput` during setup so that directory exists; otherwise deployments (or any server that reads from `STATIC_ROOT`) will miss admin and portal static files. For production, serve that output behind your reverse proxy or object storage per [Django’s static files deployment guide](https://docs.djangoproject.com/en/stable/howto/static-files/deployment/).

## Relation to identity and tenancy

Registration creates a **hub user account**. **Portal companies**, **join requests**, and the **owner tag / administrator** model are implemented in `web_ui_app` (see [09-portal-companies-ownership-and-deletion.md](09-portal-companies-ownership-and-deletion.md)). Broader ecosystem tenancy and device RBAC remain described in [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md); REST exposure and mapping to `pos_api_app.Merchant` are follow-on work.

## Related documents

- [07-web-ui-erp-and-reporting.md](07-web-ui-erp-and-reporting.md) — Broader web UI and reporting roadmap.  
- [09-portal-companies-ownership-and-deletion.md](09-portal-companies-ownership-and-deletion.md) — Portal companies, owner tag, administrators, deletion approvals.
