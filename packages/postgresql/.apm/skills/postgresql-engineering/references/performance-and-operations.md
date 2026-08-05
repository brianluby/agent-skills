# PostgreSQL performance and operations

Never run `EXPLAIN ANALYZE` on a write statement or production-heavy query without understanding that it executes the statement. Use a transaction and rollback only when all side effects are transactional and safe.

## Plans and statistics

```sql
EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS, FORMAT TEXT)
SELECT ...;
```

Adjust options for the discovered server version: `WAL` requires PostgreSQL 13 or newer and must be omitted on older supported servers.

Inspect actual/estimated rows per node, loops, buffer hits/reads/dirtied, temp spill, sort method, join strategy, and time-to-first-row versus total time. Test representative parameter values; prepared plans and skew can change choices. Use `pg_stat_statements` when enabled to prioritize by total impact, not anecdote.

## Safer schema changes

- Set bounded `lock_timeout` and appropriate `statement_timeout` for migrations.
- Add expensive constraints as `NOT VALID`, backfill/repair, then `VALIDATE CONSTRAINT` when semantics permit.
- Build large indexes with `CREATE INDEX CONCURRENTLY` outside a transaction block; detect and remove invalid remnants after failure.
- Add columns and defaults according to the deployed PostgreSQL version's rewrite behavior.
- Backfill in bounded batches with resumability and monitoring; avoid one giant transaction.
- Drop or alter dependencies only after checking views, functions, triggers, publications, and application versions.

## Health and recovery

Monitor autovacuum progress, dead tuples, transaction ID age, replication slots, WAL growth, long transactions, blocked locks, connection saturation, disk, checkpoints, and replica lag. Never disable autovacuum globally as a tuning shortcut.

Backups are not proven until restored. Verify base backup plus WAL/PITR procedures, recovery objectives, required extensions/roles/configuration, and restore into an isolated environment. For logical replication or failover, validate sequence state, replica identity, slot retention, read consistency, and client reconnection behavior.

After a change, record the before/after plan or metric, correctness checks, rollout observation window, and rollback/recovery method. Do not claim an index helps until the intended workload demonstrably uses it.
