FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS base_env

ENV UV_NO_DEV=1
WORKDIR /workspace

COPY pyproject.toml ./

RUN uv sync


FROM base_env AS common_env

COPY packages/common/pyproject.toml  packages/common/pyproject.toml

RUN uv sync --package common --no-install-workspace


FROM common_env AS db_setup_env

COPY packages/db_setup/pyproject.toml  packages/db_setup/pyproject.toml

RUN uv sync --package db_setup --no-install-workspace


FROM common_env AS api_env

COPY packages/api/pyproject.toml  packages/api/pyproject.toml

RUN uv sync --package api --no-install-workspace


FROM common_env AS worker_env

COPY packages/worker/pyproject.toml  packages/worker/pyproject.toml

RUN uv sync --package worker --no-install-workspace


FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS base

ENV UV_NO_DEV=1
WORKDIR /workspace

COPY Makefile pyproject.toml .python-version ./

RUN uv sync


FROM base AS common

COPY --from=common_env /workspace/.venv /workspace/.venv

COPY packages/common packages/common

RUN uv sync --package common


FROM common AS db_setup

COPY --from=db_setup_env /workspace/.venv /workspace/.venv

COPY packages/db_setup packages/db_setup

WORKDIR /workspace/packages/db_setup

RUN uv sync --package db_setup


FROM common AS api

COPY --from=api_env /workspace/.venv /workspace/.venv

COPY packages/api packages/api

RUN uv sync --package api


FROM api AS api_tests

COPY tests/testlib tests/testlib
COPY tests/api_tests tests/api_tests
COPY packages/db_setup packages/db_setup

RUN uv sync --package api_tests

WORKDIR /workspace/tests/api_tests/cases


FROM common AS worker

COPY --from=worker_env /workspace/.venv /workspace/.venv

COPY checkpoints checkpoints
COPY packages/worker packages/worker

RUN uv sync --package worker
