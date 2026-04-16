#!/bin/bash
set -e

echo "Running database initialization..."

psql -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" <<-EOSQL

-- =========================================
-- 1. Revoke default dangerous permissions
-- =========================================

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- =========================================
-- 2. Create application role
-- =========================================

DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = '${APP_DB_USER}'
    ) THEN
        CREATE ROLE ${APP_DB_USER} WITH
            LOGIN
            PASSWORD '${APP_DB_PASSWORD}'
            NOSUPERUSER
            NOCREATEDB
            NOCREATEROLE
            NOINHERIT;
    END IF;
END
\$\$;

-- =========================================
-- 3. Create dedicated schema
-- =========================================

CREATE SCHEMA IF NOT EXISTS app AUTHORIZATION ${APP_DB_USER};

-- =========================================
-- 4. Set search path
-- =========================================

ALTER ROLE ${APP_DB_USER} SET search_path = app;

-- =========================================
-- 5. Grant minimal required privileges
-- =========================================

GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO ${APP_DB_USER};
GRANT USAGE ON SCHEMA app TO ${APP_DB_USER};

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA app TO ${APP_DB_USER};

GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA app TO ${APP_DB_USER};

-- =========================================
-- 6. Default privileges for future tables
-- =========================================

ALTER DEFAULT PRIVILEGES IN SCHEMA app
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO ${APP_DB_USER};

ALTER DEFAULT PRIVILEGES IN SCHEMA app
GRANT USAGE, SELECT ON SEQUENCES TO ${APP_DB_USER};


EOSQL

echo "Database initialization complete."