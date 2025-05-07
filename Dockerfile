FROM arm64v8/python:3.12-slim

WORKDIR /app

# copy requirements first to leverage caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy all the application files
COPY . /app/

EXPOSE 30001

# use entrypoint for the main command
ENTRYPOINT ["python", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:30001"]

# Uncomment for debugging
# ENTRYPOINT ["bash", "-c", "while true; do sleep 60; done"]
