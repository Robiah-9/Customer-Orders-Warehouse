# Customer-Orders Warehouse

A modular Python + PostgreSQL ETL pipeline that loads customer and order data into a relational database with a proper foreign key relationship, built with error handling and idempotent loading.

## Overview

```
Raw CSVs (customers, orders)
    ↓
extract.py — reads both files, handles missing files gracefully
    ↓
clean.py — deduplicates, standardizes, flags missing data, isolates orphaned orders
    ↓
main.py — truncates both tables together, loads customers then orders
    ↓
load.py — inserts data, catches connection and duplicate-key errors
    ↓
PostgreSQL (customers + orders, linked by foreign key)
```

## Data Handling Decisions

- **Duplicate customers** — removed via `drop_duplicates()`.
- **Missing emails** — kept, flagged with `email_missing` rather than dropped, since a missing email doesn't invalidate the customer record.
- **Missing order prices** — filled using per-product mean, since different products have very different price points.
- **Orphaned orders** (referencing a customer_id that doesn't exist) — isolated into their own `orphaned_orders_df` rather than silently dropped or allowed to break the load.
- **Primary keys** — `customer_id` and `order_id` are both genuinely unique per row in this dataset (unlike a prior project), so natural keys were used instead of surrogate `SERIAL` keys.

## Key Engineering Decisions & Bugs Found

- **Idempotent loading** — the pipeline truncates tables before loading, so re-running it never duplicates data.
- **Postgres won't truncate a table referenced by a foreign key, even if empty.** Fixed by truncating both related tables together in a single `TRUNCATE TABLE orders, customers` statement, rather than one at a time.
- **Truncate order and load order follow opposite rules.** Truncating together resolves the foreign key restriction, but *loading* still requires the parent table (`customers`) to be loaded before the child table (`orders`) — otherwise every order insert fails validation against an empty customers table.
- **Error handling in `load()`** catches connection failures (`OperationalError`) and duplicate-key/constraint violations (`IntegrityError`, `DatabaseError` — pandas wraps SQLAlchemy's original error, so both must be caught together).
- Credentials are pulled from a `.env` file, excluded from version control.

## Known Limitations

- Assumes `customer_id` values are stable between runs; the pipeline doesn't yet wrap both table loads in a single database transaction, so a failure partway through a run could leave the two tables temporarily out of sync.
- No automated tests yet (planned).

## Tech Stack

Python, Pandas, PostgreSQL, SQLAlchemy, python-dotenv

## Author

Robiat