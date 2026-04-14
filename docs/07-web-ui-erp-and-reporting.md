# Web UI, ERP-style operations, and reporting

## Django web interface

Besides REST consumers, GATE provides **browser-based** UIs built with Django (templates and/or a future SPA front end).

**Intended users:** company administrators, back-office staff, finance, operations.

### Public portal (current)

The **`web_ui_app`** package is registered in the project and serves:

- A **landing page** at `/` for anonymous visitors (signed-in users are redirected to `/dashboard/`).
- **Session authentication** pages: register, log in, log out, and **portal** change password (implemented in `web_ui_app`, not the Django Admin UI; see [08-public-web-portal-landing-and-accounts.md](08-public-web-portal-landing-and-accounts.md)).

This complements **Django Admin** (`/admin/`), which targets staff and direct data operations, and will grow into deeper ERP-style screens over time.

Shared **styles and icons** for the public portal are served as Django static files under `web_ui_app/static/web_ui_app/` (see [08-public-web-portal-landing-and-accounts.md](08-public-web-portal-landing-and-accounts.md)).

## ERP-style depth (roadmap)

The web layer is not only CRUD; it aims toward **ERP-like** capabilities over time:

- Organization: companies, stores, warehouses, users, roles.  
- Master data: products, assortments, price lists (possibly fed from ERP).  
- Inventory: movements, transfers, adjustments (aligned with POS and stocktake mobile).  
- Purchasing (optional phase): purchase orders, vendor invoices.  
- Fiscal and compliance settings per region.

Depth is delivered **iteratively**; early releases may focus on multi-store POS administration and sync visibility.

## Reporting

**Goals:**

- Aggregated **sales** and **tax** breakdowns across stores and date ranges.  
- **Inventory** valuation and movement reports.  
- **Campaign and loyalty** performance when those modules are hub-managed.  
- **Export** (CSV/Excel) and scheduled reports (future).

**Implementation options (draft):** SQL views + DRF read endpoints, dedicated reporting service, or BI export to external tools.

## Coexistence with mobile

The same **underlying models and queries** power web dashboards and mobile report screens; avoid duplicating business logic in the client.

## Related documents

- [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md)  
- [05-mobile-client-scenarios.md](05-mobile-client-scenarios.md)
