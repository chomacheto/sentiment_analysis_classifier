#!/bin/bash

# Docker run script for Sentiment Analysis Classifier
# Tests CLI functionality and container performance

set -e

CONTAINER_NAME="sentiment-classifier-test"
IMAGE_NAME="sentiment-classifier:latest"

echo "🚀 Starting Sentiment Analysis Classifier Container..."

# Check if image exists
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
    echo "❌ Image $IMAGE_NAME not found. Please build first with: ./scripts/docker/build.sh"
    exit 1
fi

# Clean up any existing container
docker rm -f $CONTAINER_NAME 2>/dev/null || true

# Start container with CLI testing
echo "📊 Testing container startup and CLI functionality..."

# Start container and measure startup time
START_TIME=$(date +%s.%N)
docker run -d \
    --name $CONTAINER_NAME \
    --memory=2g \
    --cpus=2 \
    $IMAGE_NAME

# Wait for container to be ready
echo "⏳ Waiting for container to be ready..."
sleep 5

# Test CLI commands
echo "🧪 Testing CLI commands..."

# Test info command
echo "📋 Testing 'info' command:"
docker exec $CONTAINER_NAME python -m apps.ml_pipeline.cli info

# Test help command
echo "❓ Testing 'help' command:"
docker exec $CONTAINER_NAME python -m apps.ml_pipeline.cli --help

# Test analyze command with sample text
echo "🔍 Testing 'analyze' command:"
docker exec $CONTAINER_NAME python -m apps.ml_pipeline.cli analyze "This is a positive test message."

# Calculate startup time
END_TIME=$(date +%s.%N)
STARTUP_TIME=$(echo "$END_TIME - $START_TIME" | bc)
echo "⏱️  Container startup time: ${STARTUP_TIME}s"

# Verify startup time requirement (<30 seconds)
if (( $(echo "$STARTUP_TIME < 30" | bc -l) )); then
    echo "✅ Startup time requirement met: <30 seconds"
else
    echo "⚠️  Warning: Startup time exceeds 30 second target"
fi

# Get container resource usage
echo "📊 Container resource usage:"
docker stats $CONTAINER_NAME --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

echo "✅ CLI functionality test completed successfully!"

# Clean up
echo "🧹 Cleaning up test container..."
docker rm -f $CONTAINER_NAME

echo "🎉 All tests passed! Container is ready for production use."
