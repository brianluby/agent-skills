---
name: sqlite-engineering
description: Use when designing, implementing, reviewing, migrating, or troubleshooting SQLite databases, queries, transactions, indexes, concurrency, or embedded-database operations.
---

# SQLite engineering

Identify the SQLite library and runtime version, connection lifecycle, transaction model, deployment filesystem, migration mechanism, and durability requirements before changing schema or pragmas. SQLite is an embedded transactional database, not a smaller PostgreSQL server.

## Core rules

- Enable and verify foreign-key enforcement on every connection when the application relies on it; do not assume library defaults.
- Use bound parameters for values. SQL identifiers require explicit allowlists or trusted query construction; parameters cannot substitute table or column names.
- Keep transactions short and deliberate. Use `BEGIN IMMEDIATE` when a write transaction must reserve the writer predictably; never hold a transaction across network calls or user interaction.
- Choose journal and synchronous settings from measured durability/concurrency requirements. WAL improves reader/writer overlap but still has one writer and introduces checkpoint/sidecar-file considerations.
- Configure busy handling rather than treating transient lock contention as corruption. Bound retries, preserve cancellation, and investigate long transactions.
- Design indexes from query predicates and ordering. Verify with `EXPLAIN QUERY PLAN`; extra indexes increase file size and write amplification.
- Use constraints (`NOT NULL`, `CHECK`, `UNIQUE`, foreign keys, `STRICT` tables when supported) to protect invariants at the storage boundary.
- Treat type affinity carefully. Test comparisons, timestamps, booleans, numeric precision, JSON, and `NULL` behavior with actual SQLite semantics.

## Schema and migration workflow

1. Inspect `PRAGMA user_version`, migration history, schema objects, indexes, triggers, and compile/runtime version constraints.
2. Make migrations monotonic, transactional where SQLite permits, and safe for databases at every supported prior version.
3. For table rebuilds, preserve constraints, indexes, triggers, data transformations, and foreign-key integrity; test rollback and interrupted deployment behavior.
4. Exercise migration on a production-shaped copy, run integrity checks, and verify both fresh creation and upgrade paths.
5. Plan backup and restore before risky or large transformations. Copying only the main file is unsafe while WAL mode is active.

Load `references/operations-and-verification.md` for pragmas, plans, migration checks, backup/restore, WAL, and corruption triage.
