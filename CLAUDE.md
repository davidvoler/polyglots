# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**Polyglots** is a language learning platform with three applications: Content Manager (importing/generating content), Editor (building courses/lessons), and Student (learning). Each app has a Flutter UI and Python FastAPI server.

## Running the Stack

```bash
# Start all backend services + PostgreSQL
docker-compose up

# Rebuild after Dockerfile changes
docker-compose up --build
```

Services started by docker-compose:
- **PostgreSQL**: port 5433 (user/pass/db: `polyglots`)
- **Editor server**: port 8005 (`editor/server/`)
- **Student server**: port 8004 (`student/server/`)
- Content server is commented out

**Running a server locally** (outside Docker, for debugging):
```bash
cd editor/server/src  # or student/server/src
uvicorn main:app --host 0.0.0.0 --port 8005 --reload
# Uncomment the local POSTGRES_PORT line in main.py (port 5433)
```

**Flutter UIs:**
```bash
cd editor/ui   # or student/ui
flutter pub get
flutter run
```

## Architecture

```
editor/ui  (Flutter)  →  editor/server  (FastAPI, port 8005)
student/ui (Flutter)  →  student/server (FastAPI, port 8004)
content/ui (Flutter)  →  content/server (FastAPI, port 8001, commented out)
                                    ↓
                             PostgreSQL (port 5433)
```

**Database schemas:**
- `content_raw` — raw sentences, words, translations (imported content)
- `content` — processed/structured content
- `course` — courses, modules, lessons, exercises (output of Editor)
- `users_data` — student results and progress
- DDL files live in `common/DDL/` and `editor/DDL/`

## Code Conventions

### Backend (FastAPI / Python)
- Server source lives in `<app>/server/src/`
- Entry point is always `main.py` which registers routers from `routers/`
- DB queries use raw SQL with `psycopg` (async); no ORM
- Pydantic v2 models used for request/response validation
- Environment: `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` (set by Docker Compose or `.env`)

### Frontend (Flutter)
- State management via `flutter_riverpod`
- Screens are in `lib/screens/`, models in `lib/models/`, providers in `lib/providers/`
- API calls go through service classes (e.g., `CourseGenerationService`)
- Environment variables managed via `flutter_dotenv` (`.env` files per UI)

## Key Files

| File | Purpose |
|------|---------|
| `docker-compose.yaml` | Local dev orchestration |
| `editor/server/src/main.py` | Editor API entry point |
| `student/server/src/main.py` | Student API entry point |
| `editor/ui/lib/main.dart` | Editor Flutter entry point |
| `student/ui/lib/main.dart` | Student Flutter entry point |
| `common/DDL/` | Shared database schema definitions |
| `EDITOR_PLAN.md` | Detailed spec for editor wizard implementation |
| `STUDENT_APP_PLAN.md` | Spec for student quiz/learning implementation |
| `ITERATIONS.md` | Development iteration history |

## Editor App Flow

The Editor follows a wizard flow (`EditorFlowScreen`) for course creation:
1. Course setup (name, language)
2. Word selection from content
3. Sentence selection for chosen words
4. Question type configuration
5. Module/lesson generation
6. Preview and review

Editor server routers:
- `/api/v1/course` — course CRUD
- `/api/v1/generate` — word/sentence/exercise generation
- `/api/v1/words_select` — word/sentence selection submission

## Student App Flow

Student server routers:
- `/api/v1/quiz` — fetch quiz exercises for a lesson
- `/api/v1/results` — save user answers
- `/api/v1/stats` — progress statistics
- `/api/v1/course` — course/lesson listing
- `/api/v1/exercise` — individual exercise data
