# wait

## about

weight tracker for my personal use.

## requirements

- python >= 3.12
- PostgreSQL

## getting started

Follow these steps to set up and run the project locally:

### 1. clone and install dependencies

Ensure you have [uv](https://github.com/astral-sh/uv) installed, then run:

```bash
uv sync
```

### 2. database setup

Create an empty database in PostgreSQL:

```sql
CREATE DATABASE wait;
```

### 3. configure environment variables

Copy the example environment file to `.env` and fill in your PostgreSQL credentials:

```bash
cp .env.example .env
```

_(For Windows PowerShell: `Copy-Item .env.example .env`)_

### 4. run database migrations

Apply migrations to set up the database tables:

```bash
uv run python manage.py migrate
```

### 5. start the development server

Run the server locally:

```bash
uv run python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## configuration

Settings are read from environment variables (or a local `.env` file). See
`.env.example` for the full list. The most important ones are:

| variable | purpose | default |
| --- | --- | --- |
| `DEBUG` | enable debug mode; never enable in production | `false` |
| `SECRET_KEY` | Django secret key; required in production | generated (ephemeral) |
| `ALLOWED_HOSTS` | comma-separated host names | `wait.thepmsquare.com,localhost,127.0.0.1,[::1]` |
| `CSRF_TRUSTED_ORIGINS` | comma-separated trusted origins | `https://wait.thepmsquare.com` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL connection | `postgres` / `localhost:5432` |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Google OAuth credentials | placeholders |
| `SECURE_SSL_REDIRECT` | redirect HTTP to HTTPS (enable when the proxy sends `X-Forwarded-Proto`) | `false` |
| `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` | secure cookies | `true` when `DEBUG=false` |

When `DEBUG=false`, secure cookies and HSTS are enabled automatically. Set a
real `SECRET_KEY` in production so sessions survive restarts; otherwise the
entrypoint generates an ephemeral key at startup.

## testing and linting

```bash
uv run pytest
uv run ruff check .
```

## api

The REST API lives under `/api/`. Authentication uses DRF token auth or a
session cookie:

```bash
# obtain a token
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -d "username=your_username&password=your_password"

# list entries (paginated)
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/entries/
```

Interactive docs are available at `/api/schema/swagger-ui/` and
`/api/schema/redoc/` for logged-in users.

## docker

```bash
docker build -t wait .
docker run --env-file .env -p 30001:30001 wait
```

The container runs as a non-root user, applies migrations on startup
(`RUN_MIGRATIONS=1`), and serves the app with gunicorn. Set
`RUN_MIGRATIONS=0` when running multiple replicas and run migrations
separately.

## changelog

see [changelog](CHANGELOG.md) for full history.

## feedback is appreciated. thank you!
