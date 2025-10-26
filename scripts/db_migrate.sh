#!/usr/bin/env bash
set -euo pipefail

# Stralix DB Migration Runner (psql-based)
# Usage:
#  ./scripts/db_migrate.sh up            # apply all pending migrations
#  ./scripts/db_migrate.sh to 002        # migrate up to specific version
#  ./scripts/db_migrate.sh status        # show applied migrations

MIGRATIONS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)/database/migrations"
SCHEMA_TABLE="schema_migrations"

# Load DATABASE_URL from env if present
: "${DATABASE_URL:?DATABASE_URL env variable is required, e.g. postgresql://user:pass@host:5432/db}"

PSQL="psql ${DATABASE_URL} -v ON_ERROR_STOP=1"

ensure_schema_table() {
  ${PSQL} <<SQL
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '${SCHEMA_TABLE}') THEN
    CREATE TABLE ${SCHEMA_TABLE} (
      version VARCHAR(20) PRIMARY KEY,
      applied_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
      description TEXT
    );
  END IF;
END $$;
SQL
}

applied_versions() {
  ${PSQL} -Atc "SELECT version FROM ${SCHEMA_TABLE} ORDER BY version;" || true
}

apply_migration() {
  local file="$1"
  echo "Applying migration: ${file}"
  ${PSQL} -f "${file}"
}

cmd=${1:-up}

ensure_schema_table

case "$cmd" in
  up)
    APPLIED="$(applied_versions | tr '\n' ' ')"
    for f in $(ls -1 ${MIGRATIONS_DIR}/[0-9][0-9][0-9]_*.sql | sort); do
      ver="$(basename "$f" | cut -d'_' -f1)"
      if [[ " ${APPLIED} " != *" ${ver} "* ]]; then
        apply_migration "$f"
      fi
    done
    echo "All pending migrations applied."
    ;;
  to)
    target=${2:?Target version required}
    APPLIED="$(applied_versions | tr '\n' ' ')"
    for f in $(ls -1 ${MIGRATIONS_DIR}/[0-9][0-9][0-9]_*.sql | sort); do
      ver="$(basename "$f" | cut -d'_' -f1)"
      if [[ "$ver" > "$target" ]]; then break; fi
      if [[ " ${APPLIED} " != *" ${ver} "* ]]; then
        apply_migration "$f"
      fi
    done
    echo "Migrated up to version ${target}."
    ;;
  status)
    ${PSQL} -c "SELECT * FROM ${SCHEMA_TABLE} ORDER BY version;"
    ;;
  *)
    echo "Unknown command: $cmd"
    echo "Usage: $0 [up|to <version>|status]"
    exit 1
    ;;
esac
