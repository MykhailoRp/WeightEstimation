FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS base

ENV UV_NO_DEV=1
WORKDIR /workspace

COPY Makefile pyproject.toml .python-version ./

RUN uv sync


FROM base AS common

COPY packages/common packages/common

RUN uv sync --package common


FROM common AS db_setup

COPY packages/db_setup packages/db_setup

RUN uv sync --package db_setup

WORKDIR /workspace/packages/db_setup


FROM common AS api

COPY packages/api packages/api

RUN uv sync --package api


FROM api AS api_tests

COPY tests/testlib tests/testlib
COPY tests/api_tests tests/api_tests
COPY packages/db_setup packages/db_setup

RUN uv sync --package api_tests

WORKDIR /workspace/tests/api_tests/cases


FROM common AS worker

COPY checkpoints checkpoints
COPY packages/worker packages/worker

RUN uv sync --package worker
