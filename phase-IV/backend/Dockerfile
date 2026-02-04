# Use an official Python runtime as the base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including libpq-dev for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY pyproject.toml .

# Install Python dependencies using uv (as mentioned in README)
RUN pip install --upgrade pip setuptools \
    && pip install uvicorn[standard] psycopg2-binary

# Install the project dependencies from pyproject.toml
RUN pip install .

# Copy the rest of the application code
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]