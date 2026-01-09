FROM python:3.11-slim

# RUN apt-get update && \
#     apt-get install -y curl build-essential pkg-config libssl-dev git && \
#     rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache-dir uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen
COPY . .

# CMD ["uv", "run", "--no-sync", "data_generator"]
CMD ["uv", "run", "data_generator"]
