# Ecosystem and boundaries

## Purpose

**SaleFlex.GATE** is the central backend hub for the SaleFlex product family. It exposes **Django REST Framework** APIs and **Django web** interfaces. Edge clients connect over HTTPS; business rules and cross-store data are anchored here when GATE is authoritative.

## Primary clients

| Client | Responsibility |
|--------|----------------|
| **SaleFlex.PyPOS** | In-store POS: sales documents, payments, end-of-day closure, local inventory operations, optional campaign/loyalty evaluation. Uses `pos/integration/gate/` for push (transactions, closures, warehouse events) and pull (products, prices, campaigns, notifications) when `[gate].enabled` is true. |
| **SaleFlex.KITCHEN** | Kitchen / production display for restaurants: consumes order and status flows from GATE (or store-local relay, depending on deployment). |
| **Mobile apps** | Same REST surface: operations dashboards, stocktake, waiter ordering, reporting. |
| **Web browser** | Django-rendered admin and ERP-style operational screens. |

## SaleFlex.OFFICE — store-level intermediary

In deployments where a GATE connection is not available or desired, **SaleFlex.OFFICE**
acts as the store-level data hub between PyPOS terminals and central systems.

| Role | Detail |
|------|--------|
| **PyPOS bootstrap** | On first startup with no local DB, a PyPOS terminal in `office` mode calls `GET /api/v1/pos/init` on OFFICE to pull all seed data. |
| **Identity triplet** | A terminal is uniquely identified by `(office_code, store_code, terminal_code)`, matching database columns in OFFICE. |
| **OFFICE → GATE sync** | When OFFICE runs in `gate` mode, it periodically pushes store data to GATE and pulls master data back. |

## Boundary rules

1. **GATE vs local POS**  
   PyPOS may run offline with a local database and **SyncQueueItem** outbox. GATE reconciles when connectivity returns. Which domain is authoritative (e.g. product master, campaign definitions, loyalty balances) is controlled by PyPOS flags such as `gate.manages_campaign` and related settings.

2. **GATE vs OFFICE vs POS**  
   In `office` mode, PyPOS communicates with OFFICE, not GATE directly. OFFICE handles GATE sync in the background. In `gate` mode, PyPOS connects to GATE directly — bypassing OFFICE.

3. **GATE vs third-party**  
   Direct ERP/payment/campaign connectors can exist in PyPOS (`third_party.*`) when GATE does not manage that service. GATE may still be the long-term integration point so vendors are configured once at the hub.

4. **Multi-tenant isolation**  
   API responses and mutations must be scoped by **company** and **store** (and **device** where applicable). Cross-tenant data leakage is a hard requirement to prevent.

## Non-goals (draft)

- Replacing every ERP function on day one; depth grows iteratively.  
- Mandating online-only POS; offline-first POS remains a supported pattern via sync.

## Related documents

- [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md)  
- [04-rest-api-conventions.md](04-rest-api-conventions.md)
