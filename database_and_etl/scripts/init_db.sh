#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create users
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$ANALYST_DB_USER') THEN
            CREATE USER $ANALYST_DB_USER WITH PASSWORD '$ANALYST_DB_PASSWORD';
            GRANT analyst TO $ANALYST_DB_USER;
        END IF;

        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$MANAGER_DB_USER') THEN
            CREATE USER $MANAGER_DB_USER WITH PASSWORD '$MANAGER_DB_PASSWORD';
            GRANT manager TO $MANAGER_DB_USER;
        END IF;

        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$ADMIN_DB_USER') THEN
            CREATE USER $ADMIN_DB_USER WITH PASSWORD '$ADMIN_DB_PASSWORD';
            GRANT admin TO $ADMIN_DB_USER;
        END IF;
    END
    \$\$;
EOSQL

# Run the init.sql script
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/10-init.sql
