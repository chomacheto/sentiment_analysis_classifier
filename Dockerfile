# Multi-stage Dockerfile for Sentiment Analysis Classifier
# Target: <2GB final image size with Python 3.11+ and Poetry

# Build stage - Install dependencies and build application
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.7.1

# Configure Poetry to not create virtual environment (we're in a container)
RUN poetry config virtualenvs.create false

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --only=main --no-dev --no-interaction --no-ansi

# Runtime stage - Create optimized runtime image
FROM python:3.11-slim as runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create application directory
WORKDIR /app

# Copy application code
COPY packages/ ./packages/
COPY apps/ ./apps/
COPY setup.py ./

# Install the application in development mode
RUN pip install -e .

# Create cache directory for models
RUN mkdir -p /app/.cache/huggingface && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set the entry point to the CLI
ENTRYPOINT ["python", "-m", "apps.ml_pipeline.cli"]

# Default command (can be overridden)
CMD ["--help"]
