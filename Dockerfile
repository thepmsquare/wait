FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# install dependencies
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-install-project --no-dev

# copy project
COPY . /app/

# make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# run collectstatic
RUN python manage.py collectstatic --no-input

# run as a non-root user
RUN useradd --create-home --uid 10001 app \
    && chown -R app:app /app
USER app

EXPOSE 30001

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:30001/', timeout=4)"

# use entrypoint script to handle migrations and startup
ENTRYPOINT ["/app/entrypoint.sh"]
