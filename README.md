# wait

## about

weight tracker for my personal user.

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

## changelog

see [changelog](CHANGELOG.md) for full history.

## feedback is appreciated. thank you!
