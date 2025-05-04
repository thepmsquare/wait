# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 30001 available to the world outside this container
EXPOSE 30001

# Run the Django development server (you'll change this for production)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:30001"]