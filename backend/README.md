# FanEcho MVP - Backend

AI-powered synthetic fan reaction simulator for social media content testing.

## Overview

FanEcho helps content creators test their social media drafts against diverse AI personas before posting, reducing the risk of backlash and improving engagement.

### Key Features

- **Persona Generation**: Create 5 diverse AI personas based on audience descriptions
- **Parallel Simulation**: Run reactions from all personas simultaneously (<20s)
- **AI Insights**: Automatic pain point detection and improvement recommendations
- **Trend Tracking**: Monitor sentiment improvements across draft iterations

---

## Tech Stack

- **Framework**: FastAPI (Python 3.9+)
- **Database**: MySQL 8.0+ with SQLAlchemy ORM
- **LLM Providers**: OpenAI (GPT-4o), Anthropic (Claude 3.5 Sonnet)
- **Async Processing**: asyncio for parallel execution
- **Testing**: pytest, pytest-asyncio, pytest-cov

---

## Quick Start

### 1. Install Dependencies

```bash
cd backend
uv init
uv add -r requirements.txt
```

### 2. Configure Environment

### 2. Configure Environment

Create `.env` file:

```bash
# Application
APP_NAME=FanEcho
VERSION=1.0.0
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/fanecho_dev

# LLM APIs
OPENAI_API_KEY=your_openai_key_here
DEFAULT_LLM_PROVIDER=openai
```

### 3. Setup Database

```bash
# Run MySQL container (creates 'fanecho' database automatically)
podman run --name fanecho-mysql -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=fanecho -p 3306:3306 -d docker.io/library/mysql:8.0

# Wait for MySQL to initialize (~15-20 seconds)
sleep 20

# Run migrations (from host machine, not inside container)
uv run python init_db.py

# Verify tables were created
podman exec fanecho-mysql mysql -u root -ppassword fanecho -e "SHOW TABLES;"
```

### 4. Run Server

```bash
# Development
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

---

## Full Documentation

- **API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **OpenSpec Proposal**: [../openspec/changes/add-fanecho-mvp/](../openspec/changes/add-fanecho-mvp/)

---

## Testing

```bash
# Run all tests with coverage (from backend directory)
cd backend
PYTHONPATH=. uv run pytest tests/ -v --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

Target: 80%+ code coverage ✅

---

## Architecture

### Request Flow

1. Client → POST `/api/simulations/run`
2. API Router → Validates input, creates Draft
3. Simulation Service → Fetches personas, runs parallel execution
4. Persona Service → Generates reactions (asyncio.gather)
5. LLM Service → Calls OpenAI/Anthropic with retry logic
6. Database → Stores SimulationResults
7. API Router → Returns aggregated results (~12-20s)

---

## Performance Benchmarks

- **Persona Generation**: 3-5 seconds
- **Simulation (5 personas)**: 12-20 seconds (parallel)
- **Insights Generation**: 8-12 seconds
- **Total end-to-end**: ~25-35 seconds

---
