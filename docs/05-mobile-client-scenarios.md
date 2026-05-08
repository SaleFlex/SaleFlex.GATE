# Mobile client scenarios

Mobile apps use the **same REST APIs** as desktop clients, with OAuth/JWT for users and optional device-scoped tokens for dedicated handhelds.

## 1. Operations and management

**Users:** company administrators, area managers, IT.

**Typical features:**

- List and edit **companies** (within permission), **stores**, **terminal profiles** (PyPOS, KITCHEN).  
- View **sync health** (last push/pull, queue depth if reported).  
- Open **reports** and dashboards: sales by store, payment mix, campaign performance, stock alerts.

**API emphasis:** read-heavy reporting endpoints, CRUD on org entities where roles allow.

## 2. Stocktake / inventory counting

**Users:** store staff performing physical counts.

**Typical features:**

- Select **store** and **count session** (blind or guided).  
- Scan barcodes or search products; enter quantities; submit **count lines**.  
- GATE reconciles with **on-hand** records and produces **adjustment proposals** or posts adjustments per policy.

**API emphasis:** optimistic concurrency, session state, offline-friendly batch upload (similar philosophy to PyPOS outbox).

## 3. Waiter / table service

**Users:** floor staff in restaurants.

**Typical features:**

- Table or order header selection; add items; send to **kitchen** pipeline.  
- Status visibility (fired, preparing, ready).  
- May integrate with PyPOS for payment at table or central checkout, depending on deployment.

**API emphasis:** real-time or near-real-time updates (WebSockets or polling); tight linkage to **store** and **kitchen terminal** configuration.

## Cross-cutting

- All calls carry **tenant scope** (company/store).  
- **Role checks** differ per app persona; a stocktake clerk must not manage company-wide billing.

## Related documents

- [03-stores-terminals-and-kitchen.md](03-stores-terminals-and-kitchen.md)  
- [04-rest-api-conventions.md](04-rest-api-conventions.md)
