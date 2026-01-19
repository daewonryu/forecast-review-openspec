# FanEcho MVP Deployment Guide

## Prerequisites

- Python 3.9+
- MySQL 8.0+
- OpenAI API Key
- Anthropic API Key (optional, for fallback)

---

## Environment Configuration

### Development Environment

Create `.env.development`:

```bash
# Application
APP_NAME=FanEcho
VERSION=1.0.0
DEBUG=true
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=mysql+pymysql://fanecho_dev:dev_password@localhost:3306/fanecho_dev

# LLM APIs
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
DEFAULT_LLM_PROVIDER=openai
LLM_TIMEOUT=60
LLM_MAX_RETRIES=2

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Cost Tracking
OPENAI_GPT4O_INPUT_COST_PER_1K=0.0025
OPENAI_GPT4O_OUTPUT_COST_PER_1K=0.01
ANTHROPIC_SONNET_INPUT_COST_PER_1K=0.003
ANTHROPIC_SONNET_OUTPUT_COST_PER_1K=0.015
```

### Production Environment

Create `.env.production`:

```bash
# Application
APP_NAME=FanEcho
VERSION=1.0.0
DEBUG=false
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# Database (use secrets manager)
DATABASE_URL=mysql+pymysql://fanecho_prod:SECURE_PASSWORD@prod-db-host:3306/fanecho_prod

# LLM APIs (use secrets manager)
OPENAI_API_KEY=prod_openai_key
ANTHROPIC_API_KEY=prod_anthropic_key
DEFAULT_LLM_PROVIDER=openai
LLM_TIMEOUT=60
LLM_MAX_RETRIES=2

# CORS
CORS_ORIGINS=["https://yourdomain.com"]

# Cost Tracking
OPENAI_GPT4O_INPUT_COST_PER_1K=0.0025
OPENAI_GPT4O_OUTPUT_COST_PER_1K=0.01
ANTHROPIC_SONNET_INPUT_COST_PER_1K=0.003
ANTHROPIC_SONNET_OUTPUT_COST_PER_1K=0.015
```

---

## Database Setup

### 1. Create Database

```sql
CREATE DATABASE fanecho_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'fanecho_prod'@'%' IDENTIFIED BY 'SECURE_PASSWORD';
GRANT ALL PRIVILEGES ON fanecho_prod.* TO 'fanecho_prod'@'%';
FLUSH PRIVILEGES;
```

### 2. Run Migrations

```bash
cd backend
python init_db.py
```

### 3. Verify Schema

```bash
mysql -u fanecho_prod -p fanecho_prod -e "SHOW TABLES;"
```

Expected tables:
- users
- personas
- drafts
- simulation_results
- insights

---

## Application Deployment

### Option 1: Docker (Recommended)

#### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install uv && uv pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app ./app

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Build and Run

```bash
# Build image
docker build -t fanecho:latest .

# Run container
docker run -d \
  --name fanecho \
  -p 8000:8000 \
  --env-file .env.production \
  fanecho:latest

# Check logs
docker logs -f fanecho
```

### Option 2: systemd Service

Create `/etc/systemd/system/fanecho.service`:

```ini
[Unit]
Description=FanEcho API Service
After=network.target mysql.service

[Service]
Type=simple
User=fanecho
WorkingDirectory=/opt/fanecho/backend
Environment="PATH=/opt/fanecho/venv/bin"
EnvironmentFile=/opt/fanecho/.env.production
ExecStart=/opt/fanecho/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable fanecho
sudo systemctl start fanecho
sudo systemctl status fanecho
```

### Option 3: Cloud Platform (AWS/GCP/Azure)

#### Requirements
- Container registry (ECR, GCR, ACR)
- Container orchestration (ECS, Cloud Run, AKS)
- Managed database (RDS, Cloud SQL, Azure Database)
- Secrets manager (AWS Secrets Manager, Secret Manager, Key Vault)

---

## Nginx Reverse Proxy

Create `/etc/nginx/sites-available/fanecho`:

```nginx
upstream fanecho_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.fanecho.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.fanecho.com;

    ssl_certificate /etc/letsencrypt/live/api.fanecho.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.fanecho.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # API routes
    location / {
        proxy_pass http://fanecho_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for long-running simulations
        proxy_connect_timeout 70s;
        proxy_send_timeout 70s;
        proxy_read_timeout 70s;
    }

    # Health check
    location /health {
        proxy_pass http://fanecho_backend;
        access_log off;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/fanecho /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Monitoring & Logging

### 1. Application Logs

Logs are written to stdout/stderr. Configure log aggregation:

```bash
# View logs (Docker)
docker logs -f fanecho

# View logs (systemd)
journalctl -u fanecho -f

# View logs (file)
tail -f /var/log/fanecho/app.log
```

### 2. Cost Tracking

Monitor LLM API costs:

```bash
# Check logs for cost summaries
grep "LLM Cost" /var/log/fanecho/app.log
```

### 3. Performance Monitoring

Track key metrics:
- Average simulation duration (target: <20s)
- LLM API response times
- Database query times
- Error rates

### 4. Alerting

Set up alerts for:
- High error rate (>5% of requests)
- Slow simulations (>60s)
- Database connection failures
- LLM API failures

---

## Backup & Recovery

### Database Backups

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/fanecho"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/fanecho_$DATE.sql"

mysqldump -u fanecho_prod -p$DB_PASSWORD fanecho_prod > $BACKUP_FILE
gzip $BACKUP_FILE

# Keep last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

### Database Restore

```bash
# Restore from backup
gunzip -c /backups/fanecho/fanecho_20260114.sql.gz | \
  mysql -u fanecho_prod -p fanecho_prod
```

---

## Rollback Procedure

### 1. Application Rollback

```bash
# Docker
docker stop fanecho
docker rm fanecho
docker run -d --name fanecho -p 8000:8000 --env-file .env.production fanecho:previous-version

# systemd
sudo systemctl stop fanecho
cd /opt/fanecho
git checkout previous-tag
sudo systemctl start fanecho
```

### 2. Database Rollback

```bash
# Run rollback migration
mysql -u fanecho_prod -p fanecho_prod < backend/migrations/001_initial_schema_rollback.sql
```

---

## Security Checklist

- [ ] API keys stored in secrets manager (not in code)
- [ ] Database credentials rotated regularly
- [ ] SSL/TLS enabled for all connections
- [ ] Database access restricted by IP
- [ ] Regular security updates applied
- [ ] Rate limiting enabled (future enhancement)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (using ORM)
- [ ] CORS configured correctly

---

## Performance Tuning

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_personas_set_id ON personas(set_id);
CREATE INDEX idx_personas_user_id ON personas(user_id);
CREATE INDEX idx_drafts_user_id ON drafts(user_id);
CREATE INDEX idx_simulation_results_draft_id ON simulation_results(draft_id);
CREATE INDEX idx_insights_draft_id ON insights(draft_id);

-- Analyze query performance
EXPLAIN SELECT * FROM simulation_results WHERE draft_id = 123;
```

### Application Optimization

- Use connection pooling (SQLAlchemy default)
- Enable response caching for static data
- Optimize LLM prompt sizes
- Use async/await for parallel operations

---

## Scaling

### Horizontal Scaling

- Deploy multiple app instances behind load balancer
- Use managed database with read replicas
- Implement request queuing for high load

### Vertical Scaling

- Increase database instance size
- Increase app server resources (CPU/RAM)

---

## Troubleshooting

### Common Issues

**Issue: Simulation timeouts**
```bash
# Check LLM API status
curl https://status.openai.com/
curl https://status.anthropic.com/

# Increase timeout in config
LLM_TIMEOUT=90
```

**Issue: Database connection errors**
```bash
# Check database status
systemctl status mysql

# Check connection
mysql -u fanecho_prod -p -e "SELECT 1"

# Check connection pool
# Look for "Too many connections" in logs
```

**Issue: High memory usage**
```bash
# Restart service
sudo systemctl restart fanecho

# Check for memory leaks
docker stats fanecho
```

---

## Post-Deployment Verification

### 1. Health Check

```bash
curl http://api.fanecho.com/health
```

Expected: `{"status": "healthy", "database": "connected"}`

### 2. End-to-End Test

```bash
# Generate personas
curl -X POST http://api.fanecho.com/api/personas/generate \
  -H "Content-Type: application/json" \
  -d '{
    "audience_description": "Test audience",
    "user_id": 1
  }'

# Run simulation (use set_id from previous response)
curl -X POST http://api.fanecho.com/api/simulations/run \
  -H "Content-Type: application/json" \
  -d '{
    "draft_content": "Test content",
    "persona_set_id": "YOUR_SET_ID",
    "user_id": 1
  }'
```

### 3. Performance Test

```bash
# Check simulation duration
time curl -X POST http://api.fanecho.com/api/simulations/run \
  -H "Content-Type: application/json" \
  -d '...'
```

Expected: < 20 seconds

---

## Support Contacts

- **Production Issues**: ops@fanecho.com
- **API Questions**: api@fanecho.com
- **On-call:** [PagerDuty/Slack channel]

---

## Changelog

### v1.0.0 (2026-01-14)
- Initial MVP release
- Persona generation with GPT-4o/Claude 3.5 Sonnet
- Parallel simulation engine
- AI-powered insights and improvement tips
