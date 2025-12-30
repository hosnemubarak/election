#!/bin/bash

# Database restore script

BACKUP_FILE=$1
COMPOSE_FILE=${2:-docker-compose.yml}

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: ./restore-db.sh <backup_file> [docker-compose-file]"
    echo ""
    echo "Example:"
    echo "  ./restore-db.sh backups/election_dev_20250101_120000.sql.gz"
    echo "  ./restore-db.sh backups/election_prod_20250101_120000.sql.gz docker-compose.prod.yml"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "ERROR: Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Determine environment
if [[ $COMPOSE_FILE == *"prod"* ]]; then
    ENV="prod"
else
    ENV="dev"
fi

echo "WARNING: This will replace the current $ENV database!"
read -p "Are you sure you want to continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled."
    exit 1
fi

echo "Restoring database from: $BACKUP_FILE"
echo "======================================"

# Get database credentials from .env
source .env

# Decompress if needed
if [[ $BACKUP_FILE == *.gz ]]; then
    echo "Decompressing backup..."
    gunzip -c $BACKUP_FILE > /tmp/restore.sql
    RESTORE_FILE="/tmp/restore.sql"
else
    RESTORE_FILE=$BACKUP_FILE
fi

# Drop and recreate database
echo "Recreating database..."
if [[ $COMPOSE_FILE == *"prod"* ]]; then
    docker-compose -f docker-compose.prod.yml exec db psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
    docker-compose -f docker-compose.prod.yml exec db psql -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME;"
    docker-compose -f docker-compose.prod.yml exec -T db psql -U $DB_USER -d $DB_NAME < $RESTORE_FILE
else
    docker-compose exec db psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
    docker-compose exec db psql -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME;"
    docker-compose exec -T db psql -U $DB_USER -d $DB_NAME < $RESTORE_FILE
fi

# Clean up temporary file
if [ -f "/tmp/restore.sql" ]; then
    rm /tmp/restore.sql
fi

echo ""
echo "Database restore complete!"
echo ""
