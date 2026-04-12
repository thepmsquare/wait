FROM python:3.12-slim

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app/

# make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# run collectstatic
RUN python manage.py collectstatic --no-input

EXPOSE 30001

# use entrypoint script to handle migrations and startup
ENTRYPOINT ["/app/entrypoint.sh"]
