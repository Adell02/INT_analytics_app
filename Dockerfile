# Dockerfile

# Use the official Python image as a parent image
FROM python:3.11.5

# Set environment variables for Python to run in unbuffered mode and prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Expose port 80 to allow external connections to this Flask application
EXPOSE 80

# Define an entry point to run your application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:80", "run:app"]
