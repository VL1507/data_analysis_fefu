FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y curl build-essential pkg-config libssl-dev git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .

CMD ["uv", "run", "data_generator"]
