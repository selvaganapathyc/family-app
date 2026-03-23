# Frontend — Vue 3 App

## Stack
- Vue 3 (Composition API, `<script setup>`)
- Vite (bundler, dev server) — `build.target: 'esnext'` required for top-level await
- Pinia (state management)
- Vue Router (client-side routing)
- Axios (HTTP client)

**No Supabase dependency** — auth is fully handled by the backend API.

## Start
```bash
./start-frontend.sh
# or
cd frontend && npm run dev   # runs on http://localhost:5173
```

## Environment Files
| File | Purpose |
|---|---|
| `.env.development` | Local dev — points to local backend |
| `.env.production` | Production — points to Railway backend |
| `.env.local` | Local overrides (gitignored) — takes highest priority |

Required env vars (only 2):
```
VITE_API_URL=http://localhost:8000
VITE_AUTH_PROVIDER=backend
```

To test locally against Railway backend, create/edit `.env.local`:
```
VITE_API_URL=https://family-app-production-5362.up.railway.app:8080
VITE_AUTH_PROVIDER=backend
```

## Auth Architecture
The frontend is completely abstracted from Supabase:
- Auth is managed via a provider pattern in `src/core/auth/`
- Active provider set by `VITE_AUTH_PROVIDER` env var
- Current provider: `backend` — calls `POST /auth/login` and `POST /auth/logout` on the backend
- JWT token stored in `localStorage` under key `family_app_token`
- Token auto-attached to every API request via Axios interceptor in `axios.js`
- **Never** import from a provider file directly — always import from `core/auth/index.js`

## Folder Structure
```
src/
├── core/                    # Shared across all modules
│   ├── api/
│   │   └── axios.js         # Axios instance — auto-attaches JWT on every request
│   ├── auth/                # Auth abstraction layer
│   │   ├── index.js         # ONLY import point for auth — never import providers directly
│   │   ├── auth.store.js    # Pinia auth store (user, session, isAuthenticated)
│   │   ├── auth.routes.js   # /login route
│   │   ├── LoginView.vue
│   │   └── providers/
│   │       ├── backend.provider.js   # Active — calls backend /auth/* endpoints
│   │       └── supabase.provider.js  # Unused — kept for reference
│   ├── components/
│   │   ├── AppHeader.vue    # Module switcher tabs + user info + logout
│   │   └── AppSidebar.vue   # Dynamic nav — changes based on active module
│   └── store/
│       └── app.store.js     # Global app state: activeModule, MODULES list, MODULE_NAV map
├── modules/
│   ├── overview/            # Home screen — cross-module summary
│   ├── finance/             # Finance module (see finance/CLAUDE.md)
│   └── health/              # Health module (stub — not yet live)
├── router/
│   └── index.js             # Imports routes from all modules, global auth guard
├── App.vue                  # Root — syncs activeModule from route on navigation
└── main.js
```

## Routing & Navigation
- Default route `/` redirects to `/overview`
- After login redirects to `/overview`
- Route guard in `router/index.js` — unauthenticated users → `/login`
- `app.store.js` tracks `activeModule` — synced automatically from the URL via `App.vue` watcher
- Clicking a module tab in the header sets `activeModule` and navigates to that module's default route

## Adding a New Module (e.g. Education)
1. Create `src/modules/education/` with: `views/`, `components/`, `store/`, `services/`, `router/`
2. Add routes to `src/router/index.js`
3. Add entry to `MODULES` and `MODULE_NAV` in `src/core/store/app.store.js`
4. Remove `comingSoon: true` flag from the entry in `MODULES`

## Adding a New Auth Provider
1. Create `src/core/auth/providers/<name>.provider.js` implementing: `signIn`, `signOut`, `getSession`, `onAuthStateChange`, `getAccessToken`
2. Register in `src/core/auth/index.js` providers map
3. Set `VITE_AUTH_PROVIDER=<name>` in env file

## Currency & Locale
- All amounts displayed in INR (Indian Rupee)
- Use `Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' })` for formatting

## Vercel Deployment
- Root directory must be set to `frontend/` in Vercel dashboard
- Set env vars in Vercel dashboard:
  - `VITE_API_URL=https://family-app-production-5362.up.railway.app:8080`
  - `VITE_AUTH_PROVIDER=backend`
