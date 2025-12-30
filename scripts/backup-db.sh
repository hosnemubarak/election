#!/bin/bash

# Database backup script

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
COMPOSE_FILE=${1:-docker-compose.yml}

# Determine environment
if [[ $COMPOSE_FILE == *"prod"* ]]; then
    ENV="prod"
    CONTAINER="election_db_prod"
else
    ENV="dev"
    CONTAINER="election_db_dev"
fi

echo "Creating database backup for $ENV environment..."
echo "================================================"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Get database credentials from .env
source .env

# Create backup
BACKUP_FILE="$BACKUP_DIR/election_${ENV}_${DATE}.sql"

if [[ $COMPOSE_FILE == *"prod"* ]]; then
    docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U $DB_USER $DB_NAME > $BACKUP_FILE
else
    docker-compose exec -T db pg_dump -U $DB_USER $DB_NAME > $BACKUP_FILE
fi

# Compress backup
gzip $BACKUP_FILE

echo ""
echo "Backup created: ${BACKUP_FILE}.gz"
echo "Backup size: $(du -h ${BACKUP_FILE}.gz | cut -f1)"
echo ""

# Keep only last 7 backups
echo "Cleaning old backups (keeping last 7)..."
ls -t $BACKUP_DIR/election_${ENV}_*.sql.gz | tail -n +8 | xargs -r rm

echo "Backup complete!"
