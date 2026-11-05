# The secure counterpart of examples/vulnerable-app/Dockerfile.

# FIX (EOL base image): a supported Python on a small Alpine base, pinned by
# digest so the build is reproducible. Dependabot updates the digest.
FROM python:3.14.9-alpine3.24@sha256:dbeb11d16bb95c3a7e3c25c842cb9f20cbc8c18f8be0461a4a0dcc861ad386a0 AS build

WORKDIR /build
COPY requirements.txt .
RUN python -m venv /venv \
    && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Runtime stage: only the virtualenv and the app, no build leftovers.
FROM python:3.14.9-alpine3.24@sha256:dbeb11d16bb95c3a7e3c25c842cb9f20cbc8c18f8be0461a4a0dcc861ad386a0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# FIX (runs as root): a dedicated unprivileged user.
RUN addgroup -S app && adduser -S -G app -H app

WORKDIR /app
COPY --from=build /venv /venv
# FIX (ADD): COPY, and only the file the app needs.
COPY app.py .

USER app

# FIX (port 22): only the application port.
EXPOSE 8000

# FIX (no healthcheck): the orchestrator can tell a hung app from a healthy one.
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1:8000/health || exit 1

# FIX (debug server): a production WSGI server instead of Flask's dev server.
CMD ["/venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
