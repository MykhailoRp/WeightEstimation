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

To run tests locally use

    uv run pytest

### Health Check

#### Health check 200:

![health check 200](<screenshots/Screenshot from 2026-02-25 20-36-43.png>)

#### Health check 503:

![health check 503](<screenshots/Screenshot from 2026-02-25 20-37-47.png>)

#### Gracefull stop:

![api stop command](<screenshots/Screenshot from 2026-02-25 20-38-42.png>)

### JSON log example

```log
{"text": "2026-02-25 18:38:33.970 | INFO     | logging:callHandlers:1762 - Shutting down\n", "record": {"elapsed": {"repr": "0:02:33.307449", "seconds": 153.307449}, "exception": null, "extra": {"service": "api"}, "file": {"name": "__init__.py", "path": "/usr/local/lib/python3.12/logging/__init__.py"}, "function": "callHandlers", "level": {"icon": "ℹ️", "name": "INFO", "no": 20}, "line": 1762, "message": "Shutting down", "module": "__init__", "name": "logging", "process": {"id": 11, "name": "SpawnProcess-1"}, "thread": {"id": 127159084788608, "name": "MainThread"}, "time": {"repr": "2026-02-25 18:38:33.970556+00:00", "timestamp": 1772044713.970556}}}
{"text": "2026-02-25 18:38:34.072 | INFO     | logging:callHandlers:1762 - Waiting for application shutdown.\n", "record": {"elapsed": {"repr": "0:02:33.409056", "seconds": 153.409056}, "exception": null, "extra": {"service": "api"}, "file": {"name": "__init__.py", "path": "/usr/local/lib/python3.12/logging/__init__.py"}, "function": "callHandlers", "level": {"icon": "ℹ️", "name": "INFO", "no": 20}, "line": 1762, "message": "Waiting for application shutdown.", "module": "__init__", "name": "logging", "process": {"id": 11, "name": "SpawnProcess-1"}, "thread": {"id": 127159084788608, "name": "MainThread"}, "time": {"repr": "2026-02-25 18:38:34.072163+00:00", "timestamp": 1772044714.072163}}}
{"text": "2026-02-25 18:38:34.072 | INFO     | logging:callHandlers:1762 - Application shutdown complete.\n", "record": {"elapsed": {"repr": "0:02:33.409434", "seconds": 153.409434}, "exception": null, "extra": {"service": "api"}, "file": {"name": "__init__.py", "path": "/usr/local/lib/python3.12/logging/__init__.py"}, "function": "callHandlers", "level": {"icon": "ℹ️", "name": "INFO", "no": 20}, "line": 1762, "message": "Application shutdown complete.", "module": "__init__", "name": "logging", "process": {"id": 11, "name": "SpawnProcess-1"}, "thread": {"id": 127159084788608, "name": "MainThread"}, "time": {"repr": "2026-02-25 18:38:34.072541+00:00", "timestamp": 1772044714.072541}}}
{"text": "2026-02-25 18:38:34.072 | INFO     | logging:callHandlers:1762 - Finished server process [11]\n", "record": {"elapsed": {"repr": "0:02:33.409675", "seconds": 153.409675}, "exception": null, "extra": {"service": "api"}, "file": {"name": "__init__.py", "path": "/usr/local/lib/python3.12/logging/__init__.py"}, "function": "callHandlers", "level": {"icon": "ℹ️", "name": "INFO", "no": 20}, "line": 1762, "message": "Finished server process [11]", "module": "__init__", "name": "logging", "process": {"id": 11, "name": "SpawnProcess-1"}, "thread": {"id": 127159084788608, "name": "MainThread"}, "time": {"repr": "2026-02-25 18:38:34.072782+00:00", "timestamp": 1772044714.072782}}}
```
