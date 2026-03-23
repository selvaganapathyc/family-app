# Backend — FastAPI App

## Stack
- Python 3.9+
- FastAPI + Uvicorn
- Supabase Python SDK (`supabase-py`) — DB access over HTTP/REST
- Pydantic v2 + pydantic-settings — request/response models and config
- python-jose — JWT utilities (installed but token verification delegated to Supabase)

## Start
```bash
./start-backend.sh
# or
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload
# runs on http://localhost:8000
# API docs at http://localhost:8000/docs
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
SUPABASE_JWT_SECRET=                         # Optional — not used currently
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
│       └── providers/
│           └── supabase.py  # Current implementation
└── modules/
    ├── overview/            # Cross-module summary endpoint
    └── finance/             # Finance module (see finance/CLAUDE.md)
```

## Auth Flow
```
Request → HTTPBearer → get_current_user (dependencies.py)
       → verify_token (core/auth/__init__.py)
       → active provider → supabase.auth.get_user(token)
       → returns { user_id, email }
```

- Uses `supabase.auth.get_user(token)` — works with Supabase's current ECC (P-256) JWT signing
- Does NOT manually decode JWT — Supabase handles verification
- `get_current_user` is a FastAPI dependency injected into every protected route

## Database Access Pattern
```
router.py → service.py → queries.py → Supabase SDK → Supabase REST API → PostgreSQL
```
- `router.py` — HTTP layer only, no business logic
- `service.py` — business logic, data transformation
- `queries.py` — all DB calls, returns raw dicts from Supabase

## Adding a New Module (e.g. Health)
1. Create `app/modules/health/` with: `__init__.py`, `router.py`, `service.py`, `models.py`, `queries.py`
2. Register in `app/main.py`: `app.include_router(health_router, prefix="/health")`

## Registering Auth Providers
To add a new auth provider (e.g. Clerk):
1. Create `app/core/auth/providers/clerk.py` implementing `AuthProvider.verify_token()`
2. Add entry to `_PROVIDERS` dict in `app/core/auth/__init__.py`
3. Set `AUTH_PROVIDER=clerk` in `.env.dev`

## Railway Deployment
- Config in `railway.toml`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Set all env vars in Railway dashboard (use prod Supabase keys)
- CORS: update `allow_origins` in `main.py` with the Railway frontend URL before deploying
