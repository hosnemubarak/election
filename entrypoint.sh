#!/bin/bash

# Entrypoint script for Django application
# This script handles database migrations and other startup tasks

set -e

echo "Starting Django application..."

# Create logs directory if it doesn't exist (must be before Django setup)
mkdir -p /app/logs

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

echo "Starting application server..."

# Execute the main command
exec "$@"
