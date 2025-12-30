#!/bin/bash

# Entrypoint script for Django application
# This script handles database migrations and other startup tasks

set -e

echo "Starting Django application..."

# Wait for database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files in production
if [ "$DEBUG" = "False" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Create logs directory if it doesn't exist
mkdir -p /app/logs

echo "Starting application server..."

# Execute the main command
exec "$@"
