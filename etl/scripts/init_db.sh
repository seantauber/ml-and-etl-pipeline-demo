# This script initializes the PostgreSQL database by creating necessary users and running an initial SQL script.
# 
# Prerequisites:
# - Environment variables POSTGRES_USER, POSTGRES_DB, ANALYST_DB_USER, ANALYST_DB_PASSWORD, MANAGER_DB_USER, MANAGER_DB_PASSWORD, ADMIN_DB_USER, and ADMIN_DB_PASSWORD must be set.
# 
# Steps:
# 1. Connect to the PostgreSQL database using the provided POSTGRES_USER and POSTGRES_DB.
# 2. Create the ANALYST_DB_USER, MANAGER_DB_USER, and ADMIN_DB_USER if they do not already exist, and assign them the appropriate roles.
# 3. Execute the init.sql script located at /docker-entrypoint-initdb.d/10-init.sql to perform additional database initialization tasks.
# 
# Usage:
# This script is typically run as part of a Docker container initialization process.
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
