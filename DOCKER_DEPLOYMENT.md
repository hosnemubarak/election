# Docker Deployment Guide

Complete guide for deploying the Django Election project using Docker for both development and production environments.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start - Development](#quick-start---development)
- [Production Deployment](#production-deployment)
- [Database Migration (SQLite to PostgreSQL)](#database-migration-sqlite-to-postgresql)
- [Database Backup & Restore](#database-backup--restore)
- [Common Commands](#common-commands)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

Verify installation:
```bash
docker --version
docker-compose --version
```

## 🚀 Quick Start - Development

### Option 1: Quick Start Script (Recommended)

```bash
# Make script executable (Linux/Mac)
chmod +x scripts/dev-start.sh

# Run the script
./scripts/dev-start.sh

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Option 2: Manual Setup

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Build and start containers
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Access Application

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

### Development Features

- ✓ Live code reload (volume mounting)
- ✓ PostgreSQL database
- ✓ Debug mode enabled
- ✓ Direct port access

## 🏭 Production Deployment

### 1. Server Setup

```bash
# Clone repository
git clone <repository-url>
cd election

# Copy and configure environment
cp .env.example .env
nano .env
```

### 2. Configure Production Environment

Edit `.env` with production settings:

```env
# Django Settings
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=election_prod_db
DB_USER=election_prod_user
DB_PASSWORD=<strong-password>
DB_HOST=db
DB_PORT=5432

# Timezone
TIME_ZONE=Asia/Dhaka
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Deploy

**Option 1: Quick Deploy Script (Recommended)**

```bash
# Make script executable
chmod +x scripts/prod-deploy.sh

# Run deployment
./scripts/prod-deploy.sh

# Create superuser (if needed)
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

**Option 2: Manual Deployment**

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### 4. Verify Deployment

- **Website**: http://your-server-ip
- **Admin**: http://your-server-ip/admin
- **Health Check**: http://your-server-ip/health/

### Production Architecture

- **Nginx**: Reverse proxy, static file serving (port 80/443)
- **Gunicorn**: WSGI server (3 workers, 2 threads)
- **PostgreSQL**: Database (internal network only)
- **Volumes**: Persistent storage for database, static files, media, logs

## 🔄 Database Migration (SQLite to PostgreSQL)

If you have existing data in SQLite and want to migrate to PostgreSQL:

```bash
# 1. Export from SQLite (ensure DB_ENGINE is not set in .env)
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --exclude contenttypes \
    --exclude auth.permission \
    --indent 2 \
    --output backups/sqlite_backup.json

# 2. Start Docker containers
docker-compose up -d

# 3. Wait for database to be ready
sleep 10

# 4. Import to PostgreSQL
docker-compose exec web python manage.py loaddata /app/backups/sqlite_backup.json

# 5. Verify migration
docker-compose exec web python manage.py shell
```

**Verify in Django shell:**
```python
from django.contrib.auth.models import User
from core.models import Event, PressRelease, Video, ContactMessage

print(f"Users: {User.objects.count()}")
print(f"Events: {Event.objects.count()}")
print(f"Press Releases: {PressRelease.objects.count()}")
print(f"Videos: {Video.objects.count()}")
print(f"Contact Messages: {ContactMessage.objects.count()}")
```

## 💾 Database Backup & Restore

### Create Backup

```bash
# Development
./scripts/backup-db.sh

# Production
./scripts/backup-db.sh docker-compose.prod.yml

# Manual backup
docker-compose exec db pg_dump -U election_user election_db > backups/backup.sql

# Compressed backup
docker-compose exec db pg_dump -U election_user election_db | gzip > backups/backup.sql.gz
```

### Restore Backup

```bash
# Using script
./scripts/restore-db.sh backups/backup.sql.gz

# Manual restore
docker-compose exec -T db psql -U election_user election_db < backups/backup.sql

# From compressed backup
gunzip -c backups/backup.sql.gz | docker-compose exec -T db psql -U election_user election_db
```

### Automated Daily Backups

**Linux/Mac (Cron):**
```bash
# Add to crontab
crontab -e

# Run daily at 2 AM
0 2 * * * cd /path/to/election && ./scripts/backup-db.sh docker-compose.prod.yml >> /var/log/election-backup.log 2>&1
```

**Windows (Task Scheduler):**
```powershell
# Create scheduled task
schtasks /create /tn "Election DB Backup" /tr "D:\personal\election\scripts\backup-db.sh" /sc daily /st 02:00
```

## 🛠️ Common Commands

### Development

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
docker-compose logs -f web

# Restart service
docker-compose restart web

# Access Django shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Collect static files
docker-compose exec web python manage.py collectstatic

# Access database
docker-compose exec db psql -U election_user election_db

# Access container shell
docker-compose exec web bash

# Rebuild containers
docker-compose up -d --build

# Remove all (including volumes)
docker-compose down -v
```

### Production

```bash
# Start services
docker-compose -f docker-compose.prod.yml up -d

# Stop services
docker-compose -f docker-compose.prod.yml down

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart web service
docker-compose -f docker-compose.prod.yml restart web

# Check service status
docker-compose -f docker-compose.prod.yml ps

# Scale web workers
docker-compose -f docker-compose.prod.yml up -d --scale web=3

# Update deployment (after code changes)
git pull
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### Maintenance

```bash
# View Docker disk usage
docker system df

# Clean up unused resources
docker system prune -a

# View container resource usage
docker stats

# Copy files from container
docker cp election_web_prod:/app/logs/django.log ./local-logs/

# Execute command in container
docker-compose exec web python manage.py <command>
```

## 🔍 Troubleshooting

### Database Connection Issues

```bash
# Check if database is running
docker-compose ps

# Check database logs
docker-compose logs db

# Test database connection
docker-compose exec db pg_isready -U election_user

# Restart database
docker-compose restart db
```

### Port Already in Use

```bash
# Windows - Find process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac - Find and kill process
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Permission Errors (Linux/Mac)

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run with sudo
sudo docker-compose up -d
```

### Static Files Not Loading (Production)

```bash
# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check Nginx logs
docker-compose -f docker-compose.prod.yml logs nginx

# Verify volume mounting
docker-compose -f docker-compose.prod.yml exec nginx ls -la /app/staticfiles
```

### Container Keeps Restarting

```bash
# Check logs for errors
docker-compose logs web

# Check entrypoint script
docker-compose exec web cat /entrypoint.sh

# Run container without entrypoint for debugging
docker-compose run --entrypoint /bin/bash web
```

### Migration Errors

```bash
# Check migration status
docker-compose exec web python manage.py showmigrations

# Fake migrations (use carefully!)
docker-compose exec web python manage.py migrate --fake

# Reset migrations (development only!)
docker-compose exec web python manage.py migrate <app> zero
docker-compose exec web python manage.py migrate
```

### Out of Memory

```bash
# Check container memory usage
docker stats

# Reduce Gunicorn workers in docker-compose.prod.yml
command: gunicorn ... --workers 2 --threads 2

# Increase Docker memory limit in Docker Desktop settings
```

## 📊 Project Structure

```
election/
├── Dockerfile                    # Multi-stage Docker image
├── docker-compose.yml            # Development configuration
├── docker-compose.prod.yml       # Production configuration
├── .dockerignore                 # Files excluded from build
├── .env.example                  # Environment template
├── entrypoint.sh                 # Container startup script
├── nginx/
│   └── nginx.conf               # Nginx configuration
├── scripts/
│   ├── dev-start.sh             # Quick development setup
│   ├── prod-deploy.sh           # Production deployment
│   ├── backup-db.sh             # Database backup
│   └── restore-db.sh            # Database restore
├── election_site/               # Django settings
├── core/                        # Main application
├── templates/                   # HTML templates
├── static/                      # Static files
├── media/                       # User uploads
└── requirements.txt             # Python dependencies
```

## 🔒 Security Checklist

### Production Deployment

- [ ] Set `DEBUG=False`
- [ ] Generate new `SECRET_KEY`
- [ ] Use strong database password
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Enable HTTPS/SSL (configure Nginx with certificates)
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Implement rate limiting
- [ ] Configure automated backups
- [ ] Monitor logs for suspicious activity
- [ ] Use environment variables for sensitive data
- [ ] Restrict database access (internal network only)

### SSL/HTTPS Setup

For production with SSL certificates (Let's Encrypt):

```nginx
# Add to nginx/nginx.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of configuration
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## 🎯 Best Practices

1. **Always backup before major changes**
2. **Test in development before deploying to production**
3. **Use version control (Git) for code changes**
4. **Monitor logs regularly**
5. **Keep Docker images updated**
6. **Use strong passwords**
7. **Implement automated backups**
8. **Test restore procedures**
9. **Document custom configurations**
10. **Monitor resource usage**

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

**Need Help?** Check the logs first: `docker-compose logs -f`
