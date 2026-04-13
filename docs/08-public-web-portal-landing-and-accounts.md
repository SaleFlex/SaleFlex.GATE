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

## Static assets, styles, and icons

Portal **CSS** is kept out of inline `<style>` blocks: shared rules live in `web_ui_app/static/web_ui_app/css/base.css` and are loaded from `web_ui_app/templates/web_ui_app/base.html` using Django’s `{% static %}` tag.

**Favicons and touch icons:** `web_ui_app/static/web_ui_app/icons/favicon.svg` is wired as the primary `rel="icon"` (SVG, modern browsers) and as `apple-touch-icon`. Replace or extend this file (for example with PNG sizes) if you need broader legacy support.

**JavaScript:** Current templates do not embed inline scripts. Add scripts under `web_ui_app/static/web_ui_app/js/` and reference them from `{% block extra_head %}` on the templates that need them (or extend the base template with an additional block if you prefer scripts at the end of `<body>`).

For production deployments, use `collectstatic` and configure `STATIC_ROOT` and your reverse proxy or object storage according to [Django’s static files deployment guide](https://docs.djangoproject.com/en/stable/howto/static-files/deployment/).

## Relation to identity and tenancy

Registration creates a **hub user account** only. **Company creation, invitations, and RBAC** are described in [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md) and are not fully wired in this first portal slice; future work will connect users to companies and roles.

## Related documents

- [07-web-ui-erp-and-reporting.md](07-web-ui-erp-and-reporting.md) — Broader web UI and reporting roadmap.
