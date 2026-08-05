# SQLite operations and verification

Use the application's SQLite binding for behavioral tests and the `sqlite3` CLI for inspection when available. Account for library/runtime version differences.

## Connection baseline

Check values rather than assuming them:

```sql
SELECT sqlite_version();
PRAGMA foreign_keys;
PRAGMA journal_mode;
PRAGMA synchronous;
PRAGMA busy_timeout;
PRAGMA integrity_check;
```

Set connection-scoped pragmas in connection initialization. Confirm pooled connections receive the same configuration. Full `integrity_check` can be expensive on a large live database; prefer `quick_check` for routine health checks and run full verification on a protected copy or during an appropriate maintenance window.

## Query and index verification

```sql
EXPLAIN QUERY PLAN
SELECT ...;

PRAGMA index_list('table_name');
PRAGMA index_info('index_name');
PRAGMA foreign_key_check;
```

Test with representative cardinality and data distribution. A plan containing `SCAN` is not automatically wrong for small tables or large result sets.

## Migration verification

- Apply every supported upgrade path and create a fresh database from zero.
- Assert schema objects via `sqlite_schema`, not only application behavior.
- Verify row counts, transformed values, constraints, indexes, triggers, and `PRAGMA foreign_key_check`.
- Test failure midway where DDL or framework behavior may escape a transaction.
- Confirm downgrade policy explicitly; many SQLite migrations are intentionally forward-only.

## Backup and WAL operations

Prefer the online backup API or CLI `.backup`/`VACUUM INTO` according to availability and free-space requirements. Do not copy, upload, or replace only the main database file while `-wal`/`-shm` files may contain committed state. Coordinate checkpoints and process shutdown only through documented application procedures.

For lock or corruption reports, preserve evidence first: record errors and filesystem/storage conditions and stop destructive retries. Quiesce every writer—or use a storage-level atomic snapshot—before preserving the main database file and all present `-wal`/`-shm` sidecars together as one consistent set. Run recovery experiments only on copies of that preserved set, never on the sole original.
