# Finance Module (Frontend)

## Purpose
Track family income and expenses, set monthly budgets per category, and view reports.

## Routes
| Path | View | Description |
|---|---|---|
| `/finance` | redirect | → `/finance/dashboard` |
| `/finance/dashboard` | `DashboardView.vue` | Monthly summary, recent transactions, budget bars |
| `/finance/expenses` | `ExpensesView.vue` | List and add expense transactions |
| `/finance/income` | `IncomeView.vue` | List and add income transactions |
| `/finance/budget` | `BudgetView.vue` | Set and track budgets per category |
| `/finance/reports` | `ReportsView.vue` | Monthly income/expense breakdown |

All routes require auth (`meta.requiresAuth: true`).

## File Structure
```
modules/finance/
├── index.js                      # FINANCE_CATEGORIES, FAMILY_MEMBERS constants, exports routes
├── views/
│   ├── DashboardView.vue
│   ├── ExpensesView.vue
│   ├── IncomeView.vue
│   ├── BudgetView.vue
│   └── ReportsView.vue
├── components/
│   ├── TransactionList.vue       # Reusable table — props: transactions[], loading. Emits: edit, delete
│   └── TransactionForm.vue       # Reusable form — props: transaction, mode. Emits: submit, cancel
├── store/
│   └── finance.store.js          # Pinia store — transactions, budgets, summary state + CRUD actions
├── services/
│   └── finance.service.js        # Axios calls to /finance/* API endpoints
└── router/
    └── finance.routes.js
```

## State (Pinia — finance.store.js)
```js
transactions: []     // loaded per view with filters
budgets: []          // loaded per month/year
summary: {}          // { total_income, total_expenses, net_balance, by_category }
```

## Family Members
Defined in `index.js`:
```js
export const FAMILY_MEMBERS = ['Selva', 'Udhaya', 'Kayal', 'Kathir']
```
Always use this constant in dropdowns — never hardcode member names in components.

## Categories
Defined in `index.js` as `FINANCE_CATEGORIES` — 17 categories covering food, transport, utilities, salary, savings, etc.
Always use this constant in the category dropdown — never hardcode.

## Transaction Fields
| Field | Type | Notes |
|---|---|---|
| `date` | date | Required |
| `description` | string | Required, non-empty |
| `amount` | float | Must be > 0 |
| `type` | `'income'` \| `'expense'` | Required |
| `category` | string | From FINANCE_CATEGORIES |
| `member_name` | string | From FAMILY_MEMBERS |

## API Endpoints Used
```
GET    /finance/transactions?month=&year=&type=&member=
POST   /finance/transactions
PUT    /finance/transactions/:id
DELETE /finance/transactions/:id
GET    /finance/budgets?month=&year=
POST   /finance/budgets
GET    /finance/summary?month=&year=
```
