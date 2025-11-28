# Git Workflow & Guidelines  
### Library Management System (PostgreSQL + FastAPI)

This document explains how to properly use Git for this project.

## 1. Initial Setup (One-time only)
```bash
# Clone the repository
git clone https://github.com/your-username/postgreslib.git
cd postgreslib

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate        # Windows
# source .venv/bin/activate     # macOS/Linux

# Install dependencies
pip install sqlalchemy psycopg2-binary fastapi uvicorn pydantic
```

## 2. Daily Workflow (Every time you work)

### Step 1: Always start fresh
```bash
git pull origin main
```

### Step 2: Create a new branch for your work
```bash
git checkout -b feature/your-feature-name
# Examples:
# git checkout -b feature/add-book-validation
# git checkout -b fix/author-delete-bug
# git checkout -b docs/update-readme
```

### Step 3: Do your work → Stage → Commit
```bash
git add .
git commit -m "feat: add full CRUD for books with validation"
# Use conventional commits (recommended):
#   feat:     new feature
#   fix:      bug fix
#   docs:     documentation
#   refactor: code improvement
#   test:     adding tests
#   chore:    maintenance
```

### Step 4: Push your branch
```bash
git push origin feature/your-feature-name
```

### Step 5: Create a Pull Request on GitHub
Go to your repo → You’ll see a banner → Click “Compare & pull request”

## 3. Recommended .gitignore
Create `.gitignore` in project root:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.pyo
*.pyd
.Python
env/
venv/
.venv/
ENV/
env.bak/
venv.bak/

# Virtual Environment
.venv/
venv/

# FastAPI / Uvicorn
*.log
uvicorn.log

# Docker
docker-compose.override.yml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## 4. Branch Naming Convention
```
feature/short-description          → new features
fix/short-description              → bug fixes
docs/short-description             → documentation
refactor/short-description        → code cleanup
test/add-unit-tests                → tests
```

## 5. Keep Main Branch Always Working
- Never commit broken code to `main`
- All changes go through Pull Requests
- At least 1 review before merging (even if solo → self-review)

## 6. Quick Commands Cheat Sheet
```bash
git status                          # See what changed
git add .                           # Stage all
git commit -m "message"             # Commit
git pull origin main                # Update local main
git checkout main                   # Switch to main
git branch                          # List branches
git push origin HEAD                # Push current branch
git log --oneline                   # See commit history
```


