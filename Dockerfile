# Stage 1: Builder
FROM python:3.10-slim-buster AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Runner
FROM python:3.10-slim-buster

WORKDIR /app

# Create a non-root user
RUN adduser --system --group appuser
USER appuser

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD curl --fail http://localhost/health || exit 1

CMD ["python", "app.py"]
