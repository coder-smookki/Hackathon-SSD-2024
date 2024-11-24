FROM python:3.12.4-slim-bullseye as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir=/app/wheels -r requirements.txt

FROM python:3.12.4-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache-dir /wheels/*

COPY ./bot ./bot
COPY ./database ./database
COPY ./migrations ./migrations
COPY ./alembic.ini ./alembic.ini

CMD ["python", "-m", "bot"]
