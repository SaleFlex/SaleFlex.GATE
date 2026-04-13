# Third-party integrations

GATE is the preferred **integration gateway** so edge devices (PyPOS, mobile) stay thin. Connectors may run as Django apps, Celery tasks, or sidecar services; the REST contract facing clients should remain stable.

## ERP

**Examples:** SAP, Oracle, Microsoft Dynamics, local vendors (Logo, Netsis, custom).

**Typical flows:**

- Master data sync: items, barcodes, units, cost (if allowed), suppliers.  
- Purchase orders and goods receipt reflection (optional).  
- Financial posting of sales or summaries (batch).

**Direction:** mostly **inbound** to GATE/POS for master data; **outbound** for aggregated sales or inventory deltas.

## Loyalty

**Examples:** external loyalty platforms, coalition programs.

**Behavior:**

- When `gate.manages_*` loyalty in PyPOS defers to hub, GATE becomes source of truth for **earn/redeem** and **balance** at checkout.  
- POS sends **customer identity** (e.g. phone, member id) and basket totals; GATE or adapter returns entitlements.

## Campaign

**Examples:** external promotion engines, coupon clearinghouses.

**Behavior:**

- Parallels PyPOS `gate.manages_campaign`: centralized **campaign evaluation** and **coupon validation** with responses applied on the sale document.  
- Cart snapshot contract (see PyPOS `CampaignSerializer.build_discount_request`) should be honored or versioned.

## Payment

**Examples:** PSPs (Stripe, Adyen, regional acquirers), switch protocols.

**Behavior:**

- Gateway may initiate **online** payments for invoices or **orchestrate** terminal sessions depending on architecture.  
- PCI scope: avoid storing raw card data; use tokenization and provider APIs.

## Design principles

- **Adapter interface** per domain (ERP, loyalty, campaign, payment) inside GATE.  
- **Retry and dead-letter** queues for outbound partner calls.  
- **Configuration per company** (and sometimes per store): base URL, credentials, feature flags.  
- **Observability:** structured logs and correlation ids from POS transaction to partner request.

## Related documents

- [01-ecosystem-and-boundaries.md](01-ecosystem-and-boundaries.md)  
- [04-rest-api-conventions.md](04-rest-api-conventions.md)
