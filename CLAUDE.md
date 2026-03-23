# Family Personal App — Project Overview

## What this is
A personal family management app for 4 members: Selva (parent), Udhaya (parent/wife), Kayal (child/daughter), Kathir (child/son). Modular design — Finance is live, Health and Education are future modules.

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | Vue 3, Vite, Pinia, Vue Router, Axios |
| Backend | Python, FastAPI, Uvicorn |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth — handled entirely by backend |
| Hosting | Backend → Railway, Frontend → Vercel |

## Repository Structure
```
family-app/
├── frontend/        # Vue 3 app
├── backend/         # FastAPI app
├── database/        # SQL migrations and seeds
│   ├── migrations/
│   │   ├── core/    # family_members table
│   │   └── finance/ # transactions, budgets tables
│   └── seeds/
├── railway.toml     # Railway build config (points to backend/)
├── start-frontend.sh
├── start-backend.sh
└── CLAUDE.md
```

## Starting the App Locally
```bash
./start-backend.sh    # terminal 1 — runs on :8000
./start-frontend.sh   # terminal 2 — runs on :5173
```

## Two Databases
- **Dev**: `backend/.env.dev` — local development Supabase project
- **Prod**: `backend/.env.prod` — production Supabase project (used by Railway)
- Switch via `ENVIRONMENT=prod` env var when starting the backend

## Deployment
| Service | Platform | Config |
|---|---|---|
| Backend | Railway | `railway.toml` at repo root, root directory set to `backend/` in Railway dashboard |
| Frontend | Vercel | Root directory set to `frontend/` in Vercel dashboard |

**Railway env vars required:** `SUPABASE_URL`, `SUPABASE_KEY`, `ENVIRONMENT=prod`, `AUTH_PROVIDER=supabase`
**Vercel env vars required:** `VITE_API_URL`, `VITE_AUTH_PROVIDER=backend`

## Module Architecture
Each module is fully self-contained in both frontend and backend:
- Frontend: `src/modules/<module>/` has its own views, components, store, services, router
- Backend: `app/modules/<module>/` has its own router, service, models, queries
- Adding a new module = copy the finance folder structure, register in `main.py` and `router/index.js`

## Auth Architecture
Auth is fully handled by the backend. The frontend never talks to Supabase directly.

```
Frontend → POST /auth/login (email+password) → Backend → Supabase Auth → JWT token
Frontend stores JWT in localStorage
Frontend sends JWT as Bearer token on every API request
Backend verifies JWT via Supabase on every protected route
```

- Frontend auth entry point: `src/core/auth/index.js` — active provider set by `VITE_AUTH_PROVIDER`
- Current frontend provider: `backend` (`src/core/auth/providers/backend.provider.js`)
- Backend auth endpoints: `POST /auth/login`, `POST /auth/logout`
- Backend token verification: `app/core/auth/` — active provider set by `AUTH_PROVIDER`
- Frontend requires NO Supabase credentials — only `VITE_API_URL` and `VITE_AUTH_PROVIDER`

## Database Access
- Backend uses Supabase Python SDK over HTTP (not a direct PostgreSQL connection string)
- Uses **service role key** (bypasses RLS) — never expose this to frontend
- Frontend has no database credentials — all data access goes through the backend API

## Key Design Decisions
- Auth is decoupled via provider pattern on both frontend and backend — swap providers with 1 env var change
- Frontend is completely database-agnostic — it only knows the backend API URL
- DB is Supabase/PostgreSQL — migrating to another PostgreSQL (Neon, RDS) = rewrite `queries.py` per module only
- No SQLAlchemy — using Supabase SDK directly for simplicity
- `vite.config.js` sets `build.target: 'esnext'` to support top-level await in auth provider loading
