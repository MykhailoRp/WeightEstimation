# LAB0

Service used for lab submission: **api** and **db_setup**

- **api**: CRUD interface for frontend
- **db_setup**: alembic script runner singleton

### Avalible env vars:

- POSTGRES_HOST=db
- POSTGRES_PORT=5432
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- POSTGRES_DB=postgres
- POSTGRES_DRIVER=asyncpg

### Commands:

Setup local enviroment for development:

    make setup

Run local dev host with local files mounted as volumes in docker compose:

    make dev

Run tests in separate unmounted docker containers:

    make test