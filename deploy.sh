#!/bin/bash

# SmogWatch Production Deployment Script
# This script builds and runs the SmogWatch application using Docker Compose

set -e

echo "🚀 Starting SmogWatch Production Deployment..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
timeout=120
elapsed=0
interval=5

while [ $elapsed -lt $timeout ]; do
    if docker-compose ps | grep -q "healthy"; then
        if [ $(docker-compose ps | grep "healthy" | wc -l) -eq 2 ]; then
            echo "✅ All services are healthy!"
            break
        fi
    fi
    
    echo "⏳ Waiting... ($elapsed/$timeout seconds)"
    sleep $interval
    elapsed=$((elapsed + interval))
done

if [ $elapsed -ge $timeout ]; then
    echo "❌ Services failed to become healthy within $timeout seconds"
    echo "📋 Service status:"
    docker-compose ps
    echo "📋 Service logs:"
    docker-compose logs
    exit 1
fi

echo "📋 Service status:"
docker-compose ps

echo ""
echo "🎉 SmogWatch is now running!"
echo "📱 Frontend: http://localhost"
echo "🔌 Backend API: http://localhost:5000"
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"
