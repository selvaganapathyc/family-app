# Frontend — Vue 3 App

## Stack
- Vue 3 (Composition API, `<script setup>`)
- Vite (bundler, dev server)
- Pinia (state management)
- Vue Router (client-side routing)
- Axios (HTTP client)
- `@supabase/supabase-js` (auth only — via provider abstraction)

## Start
```bash
./start-frontend.sh
# or
cd frontend && npm run dev   # runs on http://localhost:5173
```

## Environment Files
| File | Purpose |
|---|---|
| `.env.development` | Local dev — points to dev Supabase project |
| `.env.production` | Production — points to prod Supabase project |

Required env vars:
```
VITE_API_URL=http://localhost:8000
VITE_AUTH_PROVIDER=supabase
VITE_SUPABASE_URL=...
VITE_SUPABASE_ANON_KEY=...   # use anon/publishable key, NOT service role
```

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
│   │       └── supabase.provider.js
│   ├── components/
│   │   ├── AppHeader.vue    # Module switcher tabs + user info + logout
│   │   └── AppSidebar.vue   # Dynamic nav — changes based on active module
│   └── store/
│       └── app.store.js     # Global app state: activeModule, MODULES list, MODULE_NAV map
├── modules/
│   ├── overview/            # Home screen — cross-module summary
│   └── finance/             # Finance module (see finance/CLAUDE.md)
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

## Adding a New Module (e.g. Health)
1. Create `src/modules/health/` with: `views/`, `components/`, `store/`, `services/`, `router/`
2. Add routes to `src/router/index.js`
3. Add entry to `MODULES` and `MODULE_NAV` in `src/core/store/app.store.js`
4. Remove `comingSoon: true` flag from the Health entry in `MODULES`

## Auth Rules
- **Never** import from `providers/supabase.provider.js` directly — always import from `core/auth/index.js`
- **Never** use the service role key in frontend — use anon/publishable key only
- JWT is attached to every API request automatically via `axios.js` interceptor

## Currency & Locale
- All amounts displayed in INR (Indian Rupee)
- Use `Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' })` for formatting
