FROM python:3.12.4-slim

RUN pip install --no-cache poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-cache

COPY webapp/backend/ ./

EXPOSE 8001

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
