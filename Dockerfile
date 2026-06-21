FROM ghcr.io/astral-sh/uv:latest

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

EXPOSE 30001

# use entrypoint script to handle migrations and startup
ENTRYPOINT ["/app/entrypoint.sh"]

