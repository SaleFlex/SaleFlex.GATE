# Stores, terminals, and kitchen

## Store

A **store** belongs to exactly one **company**. It represents a site where sales and inventory events occur.

Typical attributes (draft):

- Code and display name  
- Address, timezone  
- Default warehouse / stock location identifiers used for sync  
- Feature flags (restaurant mode, fiscal profile, etc.)

## POS terminals (SaleFlex.PyPOS)

Each store can register **one or more** POS terminals.

- Each terminal has a **profile** in GATE: stable **terminal_id**, authentication secret or certificate, optional `PosSettings`-aligned metadata (name, hardware hints).  
- PyPOS uses `settings.toml` `[gate]` (`base_url`, `terminal_id`, `api_key` or OAuth client, sync intervals) to identify itself.  
- **Push:** transactions, closures, warehouse movements, optional campaign usage audit payloads.  
- **Pull:** products, prices, tax tables, campaign definitions, notifications.

When multiple terminals share a store, **receipt numbering** may remain local to each closure period on the device while GATE stores **globally unique** document identifiers for aggregation.

## Kitchen (SaleFlex.KITCHEN)

For **restaurants**, a store may also register **SaleFlex.KITCHEN** instances:

- Similar registration pattern: store-scoped credentials, device identity.  
- GATE (or a message layer behind it) routes **kitchen tickets**, **course / station** splits, and **bump / done** status according to the product design.  
- Kitchen apps do not replace POS; they complement table-service and QSR flows.

## Operational notes

- **Revoking** a terminal should immediately invalidate its tokens and stop pull/push acceptance after a short grace period if needed for offline queue flush.  
- **Moving** a terminal between stores is an admin action: re-bind profile, reset local sequence policy if required.

## Related documents

- [01-ecosystem-and-boundaries.md](01-ecosystem-and-boundaries.md)  
- [05-mobile-client-scenarios.md](05-mobile-client-scenarios.md)
