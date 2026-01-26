# Docker Setup for Backend

This guide explains how to build and run the backend using Docker, particularly for deployment on Hugging Face Spaces.

## Building the Docker Image

```bash
# From the backend directory
docker build -t todo-backend .
```

## Running Locally for Testing

```bash
# Run the container (exposes port 7860 as expected by Hugging Face)
docker run -p 7860:7860 -e DATABASE_URL="your_db_url" -e BETTER_AUTH_SECRET="your_secret" todo-backend
```

## Environment Variables

The following environment variables should be configured for the application to work properly:

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT secret for authentication
- `PORT`: Port to run the server on (defaults to 7860 for Hugging Face)

## Hugging Face Spaces Deployment

When deploying to Hugging Face Spaces, the Docker image will be built automatically. Make sure your `Dockerfile` is in the root of your repository.

The application expects to run on port 7860 as required by Hugging Face Spaces.

## Notes

- The Dockerfile uses Python 3.13 to match the project requirements
- System dependencies for psycopg2 are installed during build
- The application runs as a non-root user for security