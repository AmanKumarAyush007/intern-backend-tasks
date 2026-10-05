# 🐍 Intern Backend Tasks

> **Track 3 — Django & Python Backend Development**
> Build real backend systems: models, REST APIs, authentication, background tasks, and service integrations.

---

## 📋 Prerequisites

Before starting, ensure you have completed:
- ✅ **Repo 1**: `intern-git-fundamentals` — Git workflow mastery
- ✅ **Repo 2**: `intern-frontend-tasks` — HTML/CSS/JS basics

And have the following installed:
- Python 3.11+
- pip & virtualenv
- PostgreSQL (or SQLite for local dev)
- Redis (for Celery exercises)

---

## 🗺️ Exercise Overview

| Exercise | Topic | Skills Covered | Difficulty |
|----------|-------|----------------|------------|
| 3.1 | Django Models & CRUD | ORM, migrations, admin, views | ⭐⭐ |
| 3.2 | Django REST Framework | Serializers, ViewSets, Routers | ⭐⭐⭐ |
| 3.3 | Authentication & Permissions | JWT, token auth, permission classes | ⭐⭐⭐ |
| 3.4 | Celery Background Tasks | Task queues, Redis, periodic tasks | ⭐⭐⭐⭐ |
| 3.5 | External API Integration | `requests`, error handling, webhooks | ⭐⭐⭐ |

---

## 🚀 Quick Start

```bash
# 1. Clone this repo
git clone <repo-url>
cd intern-backend-tasks

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Navigate to the exercise starter
cd exercises/3.1-django-models-crud/starter

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Start the dev server
python manage.py runserver
```

---

## 📁 Repository Structure

```
intern-backend-tasks/
├── .github/
│   ├── workflows/checks.yml       # CI pipeline (lint, tests)
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── 00-setup.md                # Environment setup guide
│   ├── 01-django-models-crud.md   # Exercise 3.1 guide
│   ├── 02-drf-api.md              # Exercise 3.2 guide
│   ├── 03-authentication.md       # Exercise 3.3 guide
│   ├── 04-celery-tasks.md         # Exercise 3.4 guide
│   ├── 05-api-integration.md      # Exercise 3.5 guide
│   ├── CHEATSHEET.md              # Django/DRF quick reference
│   ├── GRADING.md                 # Grading rubric
│   └── MENTOR_GUIDE.md            # Mentor-only guide
├── exercises/
│   ├── 3.1-django-models-crud/starter/   # Starter Django project
│   ├── 3.2-drf-api/starter/
│   ├── 3.3-authentication/starter/
│   ├── 3.4-celery-tasks/starter/
│   └── 3.5-api-integration/starter/
├── mentor-solutions/              # Reference implementations (mentor only)
├── scripts/
│   ├── verify.py                  # Auto-grader
│   └── setup_env.sh               # Environment bootstrap script
├── submissions/                   # Intern PRs go here
│   └── <your-username>/
└── CONTRIBUTING.md
```

---

## 📤 Submission Workflow

1. **Fork** this repository
2. Create a branch: `git checkout -b feat/<your-name>/exercise-3.X`
3. Copy the `starter/` folder to `submissions/<your-username>/3.X/`
4. Complete the exercise requirements in `docs/0X-<exercise>.md`
5. **Run the verifier**: `python scripts/verify.py --exercise 3.X --user <your-username>`
6. Open a **Pull Request** using the provided PR template
7. Pass CI checks before requesting mentor review

---

## 🧑‍🏫 Mentor Resources

- See `docs/MENTOR_GUIDE.md` for evaluation criteria and common student mistakes
- Reference solutions in `mentor-solutions/` — **do not share with interns**
- Run `python scripts/verify.py --all` to batch-check all submissions
