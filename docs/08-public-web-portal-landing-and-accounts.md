# Public web portal: landing and account pages

## Purpose

The **`web_ui_app`** Django app provides a **browser-facing** entry point alongside Django Admin and REST APIs:

- **Landing** — Project overview and calls to action for visitors who are **not** signed in.
- **Session-based accounts** — Register, log in, log out, and change password using Django’s built-in user model and session authentication.

This layer is distinct from **device / merchant token** authentication used by POS clients (see [04-rest-api-conventions.md](04-rest-api-conventions.md)).

## Behaviour

| URL | Visibility | Description |
|-----|------------|-------------|
| `/` | Guests only (signed-in users are redirected) | Landing page describing GATE and linking to register / login. |
| `/dashboard/` | Authenticated | Minimal signed-in home; ERP-style screens will extend this over time. |
| `/accounts/register/` | Guests only (redirect if already signed in) | Create a Django user; optional email field on the form. |
| `/accounts/login/` | Public | Username / password sign-in. |
| `/accounts/logout/` | POST (CSRF-protected) | Ends the session; redirects to `/`. |
| `/accounts/password/change/` | Authenticated | Change password; confirmation at `/accounts/password/change/done/`. |

## Settings

In `gate_project/settings.py`:

- `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` — session auth defaults for the web UI.
- `web_ui_app` is listed in `INSTALLED_APPS`; root `urls.py` includes `web_ui_app.urls` at `''`.

## Relation to identity and tenancy

Registration creates a **hub user account** only. **Company creation, invitations, and RBAC** are described in [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md) and are not fully wired in this first portal slice; future work will connect users to companies and roles.

## Related documents

- [07-web-ui-erp-and-reporting.md](07-web-ui-erp-and-reporting.md) — Broader web UI and reporting roadmap.
