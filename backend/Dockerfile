FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/pyproject.toml /app/backend/pyproject.toml
COPY sdk/python/pyproject.toml /app/sdk/python/pyproject.toml
COPY sdk/python/README.md /app/sdk/python/README.md
COPY backend/app /app/backend/app
COPY sdk/python/agentlens /app/sdk/python/agentlens
COPY examples /app/examples

RUN pip install --no-cache-dir -e /app/backend -e /app/sdk/python

WORKDIR /app/backend

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
