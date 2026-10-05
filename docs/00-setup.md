# Environment Setup Guide

## Prerequisites

Install the following tools before starting any backend exercise:

---

### 1. Python 3.11+

```bash
# Check version
python --version  # Should show 3.11.x or higher

# Install on Ubuntu/Debian
sudo apt update && sudo apt install python3.11 python3.11-venv python3-pip

# On Windows: Download from https://python.org
```

---

### 2. Virtual Environment

Always work inside a virtual environment:

```bash
# Create
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Deactivate
deactivate
```

---

### 3. PostgreSQL (Recommended) or SQLite (Fallback)

For exercises 3.1–3.3, SQLite (built into Django) is sufficient.

For production-like setups:
```bash
# Ubuntu
sudo apt install postgresql postgresql-contrib
sudo service postgresql start

# Create a database
sudo -u postgres psql -c "CREATE DATABASE intern_db;"
sudo -u postgres psql -c "CREATE USER intern_user WITH PASSWORD 'intern_pass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE intern_db TO intern_user;"
```

---

### 4. Redis (Required for Exercise 3.4 — Celery)

```bash
# Ubuntu
sudo apt install redis-server
sudo service redis start

# Test connection
redis-cli ping  # Should return: PONG

# Windows: Use WSL or Docker
docker run -d -p 6379:6379 redis:alpine
```

---

### 5. Verify Your Setup

Run the setup verification script:

```bash
python scripts/verify.py --check-env
```

Expected output:
```
✅ Python 3.11+  found
✅ pip           found
✅ Django        found
✅ DRF           found
✅ Redis         reachable at localhost:6379
✅ All checks passed!
```

---

## Common Issues

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: django` | Activate your venv and run `pip install -r requirements.txt` |
| `redis.exceptions.ConnectionError` | Start Redis: `sudo service redis start` |
| Port 8000 already in use | Use `python manage.py runserver 8001` |
| Migration errors | Run `python manage.py makemigrations && python manage.py migrate` |
| `CSRF verification failed` | Use Postman's CSRF handling or add `X-CSRFToken` header |

---

## IDE Recommendations

- **VS Code** with Python extension
- Install `pylint` or `flake8` for linting
- Install `black` for code formatting

```bash
pip install black flake8
black .          # Format code
flake8 .         # Check style
```
