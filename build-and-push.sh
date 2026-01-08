#!/bin/bash

# Docker Hub repository
DOCKER_REPO="drefault/radio_player"
VERSION="latest"

echo "Building Docker image..."
docker build -t ${DOCKER_REPO}:${VERSION} .

if [ $? -eq 0 ]; then
    echo "✓ Build successful!"
    
    echo "Logging in to Docker Hub..."
    docker login
    
    echo "Pushing image to Docker Hub..."
    docker push ${DOCKER_REPO}:${VERSION}
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully pushed to Docker Hub!"
        echo "Image available at: https://hub.docker.com/r/${DOCKER_REPO}"
    else
        echo "✗ Failed to push image"
        exit 1
    fi
else
    echo "✗ Build failed"
    exit 1
fi
