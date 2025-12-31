#!/bin/bash

# Development environment startup script

echo "=========================================="
echo "Starting Django Election - Development"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
fi

# Build and start services
echo "Building and starting Docker containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 5

echo ""
echo "=========================================="
echo "✓ Development environment is ready!"
echo "=========================================="
echo ""
echo "Access the application:"
echo "  Website: http://localhost:8000"
echo "  Admin:   http://localhost:8000/admin"
echo ""
echo "Useful commands:"
echo "  Create superuser:  docker-compose exec web python manage.py createsuperuser"
echo "  View logs:         docker-compose logs -f"
echo "  Stop services:     docker-compose down"
echo ""
