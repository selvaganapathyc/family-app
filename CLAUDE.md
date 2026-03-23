# Family Personal App — Project Overview

## What this is
A personal family management app for 4 members: Selva (parent), Udhaya (parent/wife), Kayal (child/daughter), Kathir (child/son). Modular design — Finance is live, Health and Education are future modules.

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | Vue 3, Vite, Pinia, Vue Router, Axios |
| Backend | Python, FastAPI, Uvicorn |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth (ECC P-256 JWT signing) |
| Hosting | Railway |

## Repository Structure
```
personal-apps/
├── frontend/        # Vue 3 app
├── backend/         # FastAPI app
├── database/        # SQL migrations and seeds
│   ├── migrations/
│   │   ├── core/    # family_members table
│   │   └── finance/ # transactions, budgets tables
│   └── seeds/
├── start-frontend.sh
├── start-backend.sh
└── CLAUDE.md
```

## Starting the App
```bash
./start-backend.sh    # terminal 1 — runs on :8000
./start-frontend.sh   # terminal 2 — runs on :5173
```

## Two Databases
- **Dev**: `backend/.env.dev` — local development Supabase project
- **Prod**: `backend/.env.prod` — production Supabase project
- Switch via `ENVIRONMENT=prod` env var when starting the backend

## Module Architecture
Each module is fully self-contained in both frontend and backend:
- Frontend: `src/modules/<module>/` has its own views, components, store, services, router
- Backend: `app/modules/<module>/` has its own router, service, models, queries
- Adding a new module = copy the finance folder structure, register in `main.py` and `router/index.js`

## Auth Architecture (Decoupled)
Auth is abstracted behind a provider pattern — the rest of the app never imports from Supabase directly.
- Frontend entry point: `src/core/auth/index.js`
- Backend entry point: `app/core/auth/__init__.py`
- Active provider controlled by `VITE_AUTH_PROVIDER` (frontend) and `AUTH_PROVIDER` (backend) env vars
- Current provider: `supabase`
- To add a new provider: create a file in `providers/`, register it in the index — zero changes elsewhere

## Database Access
- Backend uses Supabase Python SDK over HTTP (not a direct PostgreSQL connection string)
- Uses **service role key** (bypasses RLS) — never expose this to frontend
- Frontend uses **anon/publishable key** for Supabase Auth only

## Key Design Decisions
- Auth is decoupled via provider pattern — swap Supabase Auth for Clerk/custom with 1 env var change
- DB is Supabase/PostgreSQL — migrating to another PostgreSQL (Neon, RDS) = rewrite `queries.py` per module only
- MongoDB would require full rewrite of queries and schema — not planned
- No SQLAlchemy — using Supabase SDK directly for simplicity
