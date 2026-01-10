# Сделано по примеру https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile

# Установка зависимостей с помощью uv
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

ENV UV_NO_DEV=1

ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Запуск с помощью обычного python
FROM python:3.11-slim-bookworm

RUN groupadd --system --gid 10000 nonroot \
    && useradd --system --gid 10000 --uid 10000 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot

WORKDIR /app

CMD ["python", "data_generator/__main__.py"]
