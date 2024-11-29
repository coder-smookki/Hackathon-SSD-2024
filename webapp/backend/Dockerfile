FROM python:3.12.4-slim

RUN pip install --no-cache poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-cache

COPY webapp/__main__.py/ ./webapp/__main__.py
COPY webapp/application.py/ ./webapp/application.py
COPY webapp/backend/ ./webapp/backend
COPY ./database ./database

EXPOSE 8001

CMD ["poetry", "run", "uvicorn", "webapp.application:app", "--host", "0.0.0.0", "--port", "8001"]