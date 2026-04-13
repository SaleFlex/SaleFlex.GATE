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

## Boundary rules

1. **GATE vs local POS**  
   PyPOS may run offline with a local database and **SyncQueueItem** outbox. GATE reconciles when connectivity returns. Which domain is authoritative (e.g. product master, campaign definitions, loyalty balances) is controlled by PyPOS flags such as `gate.manages_campaign` and related settings.

2. **GATE vs third-party**  
   Direct ERP/payment/campaign connectors can exist in PyPOS (`third_party.*`) when GATE does not manage that service. GATE may still be the long-term integration point so vendors are configured once at the hub.

3. **Multi-tenant isolation**  
   API responses and mutations must be scoped by **company** and **store** (and **device** where applicable). Cross-tenant data leakage is a hard requirement to prevent.

## Non-goals (draft)

- Replacing every ERP function on day one; depth grows iteratively.  
- Mandating online-only POS; offline-first POS remains a supported pattern via sync.

## Related documents

- [02-identity-tenancy-and-rbac.md](02-identity-tenancy-and-rbac.md)  
- [04-rest-api-conventions.md](04-rest-api-conventions.md)
