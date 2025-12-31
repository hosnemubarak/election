#!/bin/bash

# Production deployment script

echo "=========================================="
echo "Django Election - Production Deployment"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env file with production settings."
    exit 1
fi

# Check critical environment variables
if grep -q "DEBUG=True" .env; then
    echo "WARNING: DEBUG is set to True in .env file!"
    echo "This is not recommended for production."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Pull latest code (if using git)
if [ -d .git ]; then
    echo "Pulling latest code..."
    git pull
    echo ""
fi

# Build production images
echo "Building production Docker images..."
docker compose -f docker-compose.prod.yml build

# Stop existing containers
echo "Stopping existing containers..."
docker compose -f docker-compose.prod.yml down

# Start new containers
echo "Starting production containers..."
docker compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Run migrations
echo "Running database migrations..."
docker compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

echo ""
echo "=========================================="
echo "✓ Production deployment complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Create superuser (if needed):"
echo "     docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
echo ""
echo "  2. Check service status:"
echo "     docker compose -f docker-compose.prod.yml ps"
echo ""
echo "  3. View logs:"
echo "     docker compose -f docker-compose.prod.yml logs -f"
echo ""
