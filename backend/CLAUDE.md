# Backend — FastAPI App

## Stack
- Python 3.9+
- FastAPI + Uvicorn
- Supabase Python SDK (`supabase-py`) — DB access and auth over HTTP/REST
- Pydantic v2 + pydantic-settings — request/response models and config

## Start
```bash
./start-backend.sh
# or
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload
# runs on http://localhost:8000
# API docs at http://localhost:8000/docs
```

If `.venv` is missing or broken (e.g. after moving directories):
```bash
cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

## Environment Files
| File | Purpose |
|---|---|
| `.env.dev` | Local development |
| `.env.prod` | Production |
| `.env.example` | Template — copy to create your env files |

Required env vars:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-secret-key   # NOT the anon key
ENVIRONMENT=dev
AUTH_PROVIDER=supabase
```

Active env file is selected via `ENVIRONMENT` env var (defaults to `dev`).
Set `ENVIRONMENT=prod` before starting for production.

## Folder Structure
```
app/
├── main.py                  # FastAPI app, CORS config, router registration
├── core/
│   ├── config.py            # pydantic-settings — reads .env.{ENVIRONMENT}
│   ├── database.py          # Supabase client singleton (lru_cache)
│   ├── dependencies.py      # get_current_user FastAPI dependency
│   └── auth/                # Auth abstraction layer
│       ├── __init__.py      # ONLY import point — exports verify_token()
│       ├── base.py          # AuthProvider abstract base class
│       ├── router.py        # POST /auth/login, POST /auth/logout endpoints
│       └── providers/
│           └── supabase.py  # Verifies JWT via supabase.auth.get_user(token)
└── modules/
    ├── overview/            # Cross-module summary endpoint
    ├── finance/             # Finance module (see finance/CLAUDE.md)
    └── health/              # Health module (stub — not yet live)
```

## Auth Endpoints
```
POST /auth/login   — body: { email, password } → returns { access_token, user: { id, email } }
POST /auth/logout  — invalidates session on Supabase side
```

These are the only endpoints the frontend calls directly for auth. All other routes are protected.

## Auth Flow (Protected Routes)
```
Request → HTTPBearer → get_current_user (dependencies.py)
       → verify_token (core/auth/__init__.py)
       → active provider → supabase.auth.get_user(token)
       → returns { user_id, email }
```

## Database Access Pattern
```
router.py → service.py → queries.py → Supabase SDK → Supabase REST API → PostgreSQL
```
- `router.py` — HTTP layer only, no business logic
- `service.py` — business logic, data transformation
- `queries.py` — all DB calls, returns raw dicts from Supabase

## CORS
- Dev: allows all origins (`"*"`)
- Prod: update `allow_origins` in `main.py` with the Vercel frontend URL after deployment

## Adding a New Module (e.g. Education)
1. Create `app/modules/education/` with: `__init__.py`, `router.py`, `service.py`, `models.py`, `queries.py`
2. Register in `app/main.py`: `app.include_router(education_router, prefix="/education")`

## Registering Auth Providers
To add a new auth provider (e.g. Clerk):
1. Create `app/core/auth/providers/clerk.py` implementing `AuthProvider.verify_token()`
2. Add entry to `_PROVIDERS` dict in `app/core/auth/__init__.py`
3. Set `AUTH_PROVIDER=clerk` in `.env.dev`

## Railway Deployment
- `railway.toml` is at the **repo root** (not inside `backend/`)
- Root directory is set to `backend/` in the Railway dashboard (Settings → Source)
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Set all env vars in Railway dashboard Variables tab (use prod Supabase keys)
- Live at: `https://family-app-production-5362.up.railway.app`
