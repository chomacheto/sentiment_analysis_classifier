#!/bin/bash

# Docker build script for Sentiment Analysis Classifier
# Ensures optimized build and verifies image size requirements

set -e

echo "🐳 Building Sentiment Analysis Classifier Docker Image..."

# Build the image with multi-stage optimization
docker build \
    --target runtime \
    --tag sentiment-classifier:latest \
    --tag sentiment-classifier:$(date +%Y%m%d-%H%M%S) \
    .

echo "✅ Build completed successfully!"

# Get image size information
echo "📊 Image size analysis:"
docker images sentiment-classifier:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Extract size in bytes for verification
IMAGE_SIZE=$(docker images sentiment-classifier:latest --format "{{.Size}}" | sed 's/[^0-9.]//g')

# Convert to GB for comparison (assuming size is in MB or GB)
if [[ $IMAGE_SIZE == *"GB"* ]]; then
    SIZE_GB=$(echo $IMAGE_SIZE | sed 's/GB//')
elif [[ $IMAGE_SIZE == *"MB"* ]]; then
    SIZE_MB=$(echo $IMAGE_SIZE | sed 's/MB//')
    SIZE_GB=$(echo "scale=2; $SIZE_MB / 1024" | bc)
else
    SIZE_GB=$IMAGE_SIZE
fi

echo "📏 Final image size: ${SIZE_GB}GB"

# Verify size requirement (<2GB)
if (( $(echo "$SIZE_GB < 2" | bc -l) )); then
    echo "✅ Image size requirement met: <2GB"
else
    echo "⚠️  Warning: Image size exceeds 2GB target"
    echo "   Consider optimizing dependencies or using smaller base images"
fi

echo "🚀 Ready to run with: docker run sentiment-classifier:latest"
