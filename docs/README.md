# SaleFlex.GATE — Documentation (Draft)

This folder describes the **target architecture** of **SaleFlex.GATE** and the integration contract with **SaleFlex.PyPOS**. The application is still maturing; content here is **draft** and will be updated as API paths and model names stabilize.

## Reading order

| # | Document | Topic |
|---|----------|--------|
| 1 | [01-ecosystem-and-boundaries.md](01-ecosystem-and-boundaries.md) | GATE in the ecosystem; PyPOS, KITCHEN, mobile, and third-party boundaries |
| 2 | [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md) | Accounts, companies, stores, membership, and admin approval |
| 3 | [03-stores-terminals-and-kitchen.md](03-stores-terminals-and-kitchen.md) | Registering POS and kitchen apps under a store |
| 4 | [04-rest-api-conventions.md](04-rest-api-conventions.md) | REST principles, authentication, versioning (draft) |
| 5 | [05-mobile-client-scenarios.md](05-mobile-client-scenarios.md) | Management, stocktake, and waiter mobile scenarios |
| 6 | [06-third-party-integrations.md](06-third-party-integrations.md) | ERP, loyalty, campaign, and payment integrations |
| 7 | [07-web-ui-erp-and-reporting.md](07-web-ui-erp-and-reporting.md) | Django web UI, ERP-style capabilities, reporting |
| 8 | [08-public-web-portal-landing-and-accounts.md](08-public-web-portal-landing-and-accounts.md) | Public landing, register, login, logout, password change (`web_ui_app`) |

## PyPOS references

- [SaleFlex.PyPOS — Integration Layer](https://github.com/SaleFlex/SaleFlex.PyPOS/blob/main/docs/40-integration-layer.md)  
- PyPOS `settings.toml` `[gate]` section: `base_url`, `manages_transactions`, `manages_campaign`, etc.

## Contributing

Open an issue or pull request on the GATE repository for corrections or gaps in these drafts.
