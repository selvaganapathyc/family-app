# Family Personal App

A personal family management app for Selva, Udhaya, Kayal, and Kathir. Currently includes a Finance module. Health and Education modules are planned for the future.

## Tech Stack

- **Frontend**: Vue.js 3 + Vite + Pinia + Vue Router + Axios
- **Backend**: Python FastAPI + Supabase (supabase-py)
- **Database**: Supabase (PostgreSQL with RLS)
- **Hosting**: Railway

---

## Project Structure

```
personal-apps/
  frontend/       # Vue 3 + Vite app
  backend/        # FastAPI app
  database/       # SQL migrations and seeds
```

---

## Setup Instructions

### Prerequisites

- Node.js >= 18
- Python >= 3.11
- A Supabase project (free tier is fine)

---

### Database Setup

1. Go to your Supabase project dashboard.
2. Run the SQL files in order in the Supabase SQL editor:
   - `database/migrations/core/001_users_family.sql`
   - `database/migrations/finance/001_transactions.sql`
   - `database/migrations/finance/002_budgets.sql`
3. Create the 4 family members in Supabase Auth (Authentication > Users) and then run `database/seeds/family_members.sql`.

---

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env with your Supabase credentials
```

Run locally:

```bash
uvicorn app.main:app --reload --port 8000
```

---

### Frontend Setup

```bash
cd frontend
npm install

# Edit .env.development with your Supabase URL and anon key
```

Run locally:

```bash
npm run dev
```

---

### Environment Variables

#### Backend `.env`

| Variable | Description |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Supabase service role key (keep secret) |
| `SUPABASE_JWT_SECRET` | JWT secret from Supabase project settings |
| `ENVIRONMENT` | `dev` or `prod` |

#### Frontend `.env.development`

| Variable | Description |
|---|---|
| `VITE_API_URL` | Backend URL (http://localhost:8000 for local) |
| `VITE_SUPABASE_URL` | Your Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon/public key |

---

### Deploy to Railway

1. Push repo to GitHub.
2. Create a new Railway project, add the `backend/` directory as a service.
3. Set environment variables in Railway dashboard.
4. For frontend, deploy to Railway or Vercel by pointing to the `frontend/` directory.
