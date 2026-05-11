FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-tk tk \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY tkdesigner ./tkdesigner

RUN pip install --no-cache-dir .

ENTRYPOINT ["tkdesigner"]
