---
name: postgresql-engineering
description: Use when designing, implementing, reviewing, migrating, tuning, or operating PostgreSQL schemas, queries, transactions, indexes, extensions, or production database behavior.
---

# PostgreSQL engineering

Establish the server major version, schema/migration owner, workload shape, transaction boundaries, connection-pool mode, extensions, replication topology, and deployment constraints before recommending SQL or configuration.

## Schema and query principles

- Encode invariants with appropriate types, `NOT NULL`, `CHECK`, uniqueness, foreign keys, and exclusion constraints. Avoid application-only integrity for data shared by multiple writers.
- Bind all values and allowlist dynamic identifiers. Preserve least-privilege roles and separate migration ownership from application runtime privileges where practical.
- Choose indexes from actual predicates, joins, ordering, cardinality, and write rate. Consider multicolumn order, partial predicates, expression indexes, `INCLUDE`, and operator classes; do not index every column.
- Inspect plans with representative parameters and data. Compare estimated versus actual rows, loops, buffers, spills, and lock/I/O behavior—not only total time.
- Keep transactions short and make isolation assumptions explicit. Handle serialization failures and deadlocks with bounded whole-transaction retries where safe.
- Avoid `SELECT *` at durable API boundaries. Make ordering deterministic when pagination or repeatable output matters; prefer keyset pagination for large, stable traversals.
- Use PostgreSQL-native types deliberately (`timestamptz`, `uuid`, arrays, ranges, `jsonb`) while keeping frequently queried relational fields relational.
- Treat connection count as a resource. Size pools against server capacity and understand transaction-pooling restrictions before relying on session state or prepared statements.

## Change workflow

1. Inspect schema, constraints, indexes, statistics, query plans, data volume, locks, and migration conventions.
2. Define compatibility for old/new application versions during rollout and rollback.
3. Separate metadata-only changes from rewrites, validation scans, and lock-heavy operations; test lock acquisition with realistic concurrent traffic.
4. Use concurrent or staged techniques where needed, understanding their transaction restrictions and failure cleanup.
5. Verify plans and correctness before and after, monitor the rollout, and retain a recovery path.

Load `references/performance-and-operations.md` for plan analysis, safe DDL patterns, vacuum/statistics, locking, backup/restore, and replication checks.
