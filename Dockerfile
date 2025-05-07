FROM --platform=linux/arm64/v8 arm64v8/python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 30001

CMD ["sh", "-c", "python migrate && python manage.py runserver 0.0.0.0:30001"]

# Uncomment for debugging
# CMD ["bash", "-c", "while true; do sleep 60; done"]