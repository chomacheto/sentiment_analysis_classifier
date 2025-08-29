# Docker Setup and Deployment Guide

## Overview

This guide covers the Docker containerization of the Sentiment Analysis Classifier, providing consistent deployment across different environments.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB available RAM
- 10GB available disk space

## Quick Start

### 1. Build the Container

```bash
# Build optimized image
./scripts/docker/build.sh

# Or manually
docker build --target runtime -t sentiment-classifier:latest .
```

### 2. Run the Container

```bash
# Test container functionality
./scripts/docker/run.sh

# Or manually
docker run --rm sentiment-classifier:latest --help
```

### 3. Use Docker Compose

```bash
# Start development environment
docker-compose up -d

# Start with hot-reload (development mode)
docker-compose --profile dev up -d
```

## Container Architecture

### Multi-Stage Build

- **Builder Stage**: Installs Poetry and dependencies
- **Runtime Stage**: Optimized production image
- **Target Size**: <2GB final image

### Security Features

- Non-root user (`appuser`)
- Minimal runtime dependencies
- Secure file permissions

## CLI Integration

The container integrates seamlessly with the existing CLI from Story 1.3:

```bash
# Analyze single text
docker run --rm sentiment-classifier:latest analyze "Your text here"

# Batch processing
docker run --rm -v $(pwd)/data:/app/data sentiment-classifier:latest batch

# Get system info
docker run --rm sentiment-classifier:latest info
```

## Performance Optimization

### Startup Time Target: <30 seconds

The container is optimized for:
- Fast model loading
- Efficient dependency management
- Minimal runtime overhead

### Resource Requirements

- **Memory**: 2GB minimum, 4GB recommended
- **CPU**: 2 cores minimum
- **Storage**: 10GB for models and cache

## Development Workflow

### Hot-Reload Development

```bash
# Start development service
docker-compose --profile dev up -d

# Mount source code for live updates
# Changes in ./packages and ./apps are reflected immediately
```

### Volume Mounts

- `./packages` → `/app/packages` (source code)
- `./apps` → `/app/apps` (applications)
- `./data` → `/app/data` (input/output files)
- `model-cache` → `/app/.cache/huggingface` (model persistence)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PYTHONPATH` | `/app` | Python module search path |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `MODEL_CACHE_DIR` | `/app/.cache/huggingface` | Model cache location |
| `DEVELOPMENT_MODE` | `false` | Enable development features |

## Troubleshooting

### Common Issues

#### 1. Container Won't Start

```bash
# Check container logs
docker logs sentiment-classifier-dev

# Verify image exists
docker images sentiment-classifier:latest
```

#### 2. CLI Commands Fail

```bash
# Test basic functionality
docker run --rm sentiment-classifier:latest --help

# Check Python path
docker run --rm sentiment-classifier:latest python -c "import sys; print(sys.path)"
```

#### 3. Model Loading Issues

```bash
# Check model cache
docker exec sentiment-classifier-dev ls -la /app/.cache/huggingface

# Verify model files
docker exec sentiment-classifier-dev python -c "from packages.ml_core.sentiment_pipeline import SentimentPipeline; print('Model loaded successfully')"
```

#### 4. Performance Issues

```bash
# Monitor resource usage
docker stats sentiment-classifier-dev

# Check startup time
time docker run --rm sentiment-classifier:latest info
```

### Debug Mode

```bash
# Run with debug logging
docker run --rm -e LOG_LEVEL=DEBUG sentiment-classifier:latest info

# Interactive shell for debugging
docker run --rm -it sentiment-classifier:latest /bin/bash
```

## Production Deployment

### Health Checks

The container includes built-in health checks:

```yaml
healthcheck:
  test: ["CMD", "python", "-m", "apps.ml_pipeline.cli", "info"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Resource Limits

```bash
docker run -d \
  --name sentiment-classifier-prod \
  --memory=4g \
  --cpus=2 \
  --restart=unless-stopped \
  sentiment-classifier:latest
```

### Monitoring

```bash
# Container metrics
docker stats sentiment-classifier-prod

# Log monitoring
docker logs -f sentiment-classifier-prod

# Health check status
docker inspect sentiment-classifier-prod --format='{{.State.Health.Status}}'
```

## Best Practices

1. **Always use multi-stage builds** for production images
2. **Mount volumes** for persistent data and development
3. **Set resource limits** to prevent container resource exhaustion
4. **Use health checks** for automated monitoring
5. **Implement proper logging** for debugging and monitoring
6. **Regular image updates** to patch security vulnerabilities

## Support

For additional support:
- Check container logs: `docker logs <container-name>`
- Review this documentation
- Consult the project architecture documentation
- Open an issue in the project repository
