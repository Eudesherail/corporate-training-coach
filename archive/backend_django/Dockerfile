# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update ; \
   apt-get -y install libpq-dev gcc ;\
   apt-get clean;

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Run the application on port 8000
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py createsu && python manage.py runserver 0.0.0.0:8000"]
