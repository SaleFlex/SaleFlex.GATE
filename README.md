![Python 3.13](https://img.shields.io/badge/python-%3E=_3.13-success.svg)
![Django](https://img.shields.io/badge/Django-6.0.4-blue.svg)
![License](https://img.shields.io/badge/license-AGPLv3-blue.svg)
![Version](https://img.shields.io/badge/version-0.1.0a1-orange.svg)
![Status](https://img.shields.io/badge/status-alpha-orange.svg)

[SaleFlex Ecosystem](https://github.com/SaleFlex) | [SaleFlex.PyPOS](https://github.com/SaleFlex/SaleFlex.PyPOS) | [SaleFlex.OFFICE](https://github.com/SaleFlex/SaleFlex.OFFICE) | **[SaleFlex.GATE](https://github.com/SaleFlex/SaleFlex.GATE)** | [SaleFlex.KITCHEN](https://github.com/SaleFlex/SaleFlex.KITCHEN) | [SaleFlex.POS](https://github.com/SaleFlex/SaleFlex.POS) | [SaleFlex.mPOS](https://github.com/SaleFlex/SaleFlex.mPOS)

# SaleFlex.GATE

**SaleFlex.GATE** is the central hub of the SaleFlex ecosystem - a Django-powered backend that connects your stores, POS terminals, kitchen displays, and mobile apps in one place.

Whether you run a single store or a multi-location business, GATE gives you a unified platform to manage operations, synchronise data across devices, and integrate with external systems.

> Developed and operated by **[Mousavi.Tech](https://mousavi.tech)**

---

## Who Is This For?

SaleFlex.GATE is built for:

- **Retailers and restaurateurs** who need a self-hosted, open-source point-of-sale backend they can run on their own infrastructure.
- **Developers and integrators** who want a Django-based hub they can extend with custom APIs, ERP connectors, or loyalty systems.
- **Small and medium businesses** looking for a flexible alternative to expensive proprietary POS cloud services.
- **Tech-forward teams** who want full control over their data, deployments, and integrations - without vendor lock-in.

---

## Community Edition

SaleFlex.GATE is fully **open source** under the [GNU Affero General Public License v3.0 (AGPLv3)](LICENSE).

The Community Edition includes everything you need to get started:

- Multi-store, multi-terminal support
- REST API for POS, kitchen, and mobile clients
- Company and user management portal
- Django Admin interface
- Integration gateway for ERP, loyalty, and payment adapters
- Self-hosted - your data stays with you

Anyone can clone, deploy, and modify SaleFlex.GATE for their own needs. Contributions are welcome.

---

## Commercial Services

Need more than the open-source edition? We offer:

- **Custom development** - tailored features, integrations, and workflows built for your business.
- **Implementation & onboarding** - hands-on setup, configuration, and staff training.
- **Priority support** - dedicated support channels with guaranteed response times.
- **Integration services** - connecting SaleFlex.GATE to your existing ERP, accounting, loyalty, or payment systems.

> Contact us at [saleflex.pro](https://saleflex.pro) for commercial enquiries.

---

## Managed Cloud

Don't want to manage your own server? **SaleFlex Cloud** (coming soon) will offer:

- Fully managed hosting - we handle updates, backups, and scaling.
- One-click deployment - get up and running in minutes.
- Built-in monitoring and reporting dashboards.
- Enterprise-grade security and compliance.
- Multi-region availability.

> Join the waitlist at [saleflex.net](https://saleflex.net) to be notified when Managed Cloud launches.

---

## Download Ready Builds

Ready-to-run packages are currently in preparation. Once available, you will be able to download pre-configured builds for common deployment targets.

**Until then, get started with:**

```bash
git clone https://github.com/SaleFlex/SaleFlex.GATE.git
cd SaleFlex.GATE
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open the portal: http://127.0.0.1:8000/
Open Django Admin: http://127.0.0.1:8000/admin/

> **Requirements:** Python 3.12+ - Django 6.x - SQLite (dev) or PostgreSQL (production)

---

## Screenshots

> Screenshots coming soon. The admin interface, company portal, and POS sync dashboard will be showcased here.

---

## Demo Video

> A demo video is being prepared and will be published here and on the SaleFlex YouTube channel shortly.

---

## Roadmap

### Done
- Multi-tenant company and store model
- Universal user identity (GateUser) across all SaleFlex apps
- Company creation, join requests, and multi-owner deletion approvals
- Django Admin with full model management
- Portal UI: landing, login/register, dashboard, company management
- REST API foundation with merchant token authentication
- Integration with SaleFlex.PyPOS (push/pull sync, offline outbox)

### In Progress
- Expanding REST API endpoints (/api/v1/)
- POS terminal and device registry
- Store-level role-based access control (RBAC)

### Planned
- OpenAPI / Swagger documentation
- ERP, loyalty, campaign, and payment adapter framework
- Sales, stock, and KPI reporting layer
- Mobile-oriented endpoints (stocktake, waiter / table service)
- Multi-store management web UI
- SaleFlex Cloud (managed hosting)
- Ready-to-run installer packages

---

## Related Projects

| Project | Description |
|---------|-------------|
| [SaleFlex.PyPOS](https://github.com/SaleFlex/SaleFlex.PyPOS) | Python / PySide6 touch POS terminal |
| [SaleFlex.OFFICE](https://github.com/SaleFlex/SaleFlex.OFFICE) | Back-office and ERP-style management |
| [SaleFlex.KITCHEN](https://github.com/SaleFlex/SaleFlex.KITCHEN) | Kitchen display system |
| [SaleFlex.POS](https://github.com/SaleFlex/SaleFlex.POS) | Legacy .NET POS client |
| [SaleFlex.mPOS](https://github.com/SaleFlex/SaleFlex.mPOS) | Mobile POS (Android) |

---

## License

This project is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](LICENSE) for details.

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

If you find SaleFlex.GATE useful and want to support its development:

- **USDT / BUSD / ETH:** `0xa5a87a939bfcd492f056c26e4febe102ea599b5b`
- **BTC:** `15qyZpi6HjYyVhKKBsCbZSXU4bLdVJ8Phe`
- **SOL:** `Gt3bDczPcJvfBeg9TTBrBJGSHLJVkvnSSTov8W3QMpQf`