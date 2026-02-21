FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS base

ENV UV_NO_DEV=1
WORKDIR /workspace

COPY Makefile pyproject.toml .python-version .

RUN uv sync


FROM base AS common

COPY packages/common packages/common

RUN uv sync --package common


FROM common AS api

COPY packages/api packages/api

RUN uv sync --package api


FROM common AS worker

COPY packages/worker packages/worker

RUN uv sync --package worker
