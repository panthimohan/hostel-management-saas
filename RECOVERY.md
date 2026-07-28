# Nestled Production Recovery Guide

This document explains how to restore the Nestled Hostel Management SaaS application after a laptop failure, server replacement, or production recovery event.

## 1. Clone the Repository

Install Git and clone the project:

```bash
git clone https://github.com/panthimohan/hostel-management-saas.git
cd hostel-management-saas
```

## 2. Restore Environment Configuration

The production environment file is stored separately for security.

Restore:

```text
.env
```

Place it in the project root:

```text
hostel-management-saas/
├── backend/
├── frontend/
├── docker-compose.yml
└── .env
```

The `.env` file contains:

* Django configuration
* Database credentials
* Email settings
* Production environment variables

Never commit `.env` to GitHub.

## 3. Start Docker Services

Start the application:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

Expected services:

```text
nestled-backend
nestled-db
```

## 4. Restore PostgreSQL Database

Copy the database backup file to the server:

```bash
scp hostel_saas_backup_YYYY-MM-DD.sql root@SERVER_IP:/opt/nestled/
```

Restore the database:

```bash
docker exec -i nestled-db psql -U postgres hostel_saas < hostel_saas_backup_YYYY-MM-DD.sql
```

Verify database tables:

```bash
docker exec -it nestled-db psql -U postgres hostel_saas
```

Inside PostgreSQL:

```sql
\dt
```

## 5. Restart Backend

After restoring the database:

```bash
docker compose restart backend
```

Check backend logs:

```bash
docker logs nestled-backend --tail 100
```

## 6. Frontend Deployment

Build frontend:

```bash
cd frontend
npm install
npm run build
```

Deploy the generated build files to the web server.

## 7. Verify Application

Check:

* Frontend loads correctly
* Login works
* Owner dashboard loads
* Tenant records exist
* Payments and invoices are available
* Password reset email works

## 8. Backup Strategy

Maintain these backups:

### GitHub

Contains:

* Backend source code
* Frontend source code
* Docker configuration

### Private Backup

Contains:

* `.env`
* PostgreSQL database dumps
* Uploaded media files

Never store production secrets in GitHub.

## 9. Creating a New Database Backup

Create a fresh PostgreSQL backup:

```bash
docker exec nestled-db pg_dump -U postgres hostel_saas > hostel_saas_backup_$(date +%F).sql
```

## 10. Emergency Contacts

Production Server:

```text
IP: 167.172.90.235
Domain: https://traversedw.com.np
```

Repository:

```text
https://github.com/panthimohan/hostel-management-saas
```
