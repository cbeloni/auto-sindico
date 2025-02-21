# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock ./

# Install pipenv and the dependencies
RUN pip install pipenv 
RUN pipenv install

# Copy the rest of the application code to the working directory
COPY . .

# Command to run the application
CMD ["pipenv", "run", "python", "main.py"]