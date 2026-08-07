FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/ParthJadhav/Tkinter-Designer"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY tkdesigner ./tkdesigner

RUN pip install --no-cache-dir . \
    && useradd --create-home --shell /usr/sbin/nologin tkdesigner \
    && mkdir /workspace \
    && chown tkdesigner:tkdesigner /workspace

WORKDIR /workspace
USER tkdesigner

ENTRYPOINT ["tkdesigner"]
