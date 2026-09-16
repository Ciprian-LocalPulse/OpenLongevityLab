# Database migrations

The runtime database boundary is in `src/openlongevity/db.py`. Install the optional `db` extra and use Alembic to generate environment-specific migrations. The repository intentionally avoids embedding credentials or an assumed cloud provider. `sql/schema.sql` remains a portable bootstrap for local PostgreSQL.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
