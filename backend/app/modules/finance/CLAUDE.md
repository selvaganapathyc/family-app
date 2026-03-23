# Finance Module (Backend)

## Purpose
Manages family income/expense transactions, monthly budgets per category, and aggregated summaries.

## Endpoints
| Method | Path | Query Params | Description |
|---|---|---|---|
| GET | `/finance/transactions` | `month`, `year`, `type`, `member` | List transactions (all optional filters) |
| POST | `/finance/transactions` | — | Create a transaction |
| PUT | `/finance/transactions/:id` | — | Update a transaction |
| DELETE | `/finance/transactions/:id` | — | Delete a transaction |
| GET | `/finance/budgets` | `month`, `year` (required) | List budgets for a month |
| POST | `/finance/budgets` | — | Create or update a budget (upsert) |
| GET | `/finance/summary` | `month`, `year` (required) | Aggregated income/expense summary |

All endpoints require Bearer token auth via `get_current_user` dependency.

## File Structure
```
modules/finance/
├── __init__.py
├── router.py       # HTTP layer only — no logic
├── service.py      # Business logic and data transformation
├── models.py       # Pydantic request/response models
└── queries.py      # All Supabase DB calls
```

## Models
| Model | Used for |
|---|---|
| `TransactionCreate` | POST body — all fields required |
| `TransactionUpdate` | PUT body — all fields optional |
| `TransactionResponse` | GET/POST/PUT response |
| `BudgetCreate` | POST body for budgets |
| `BudgetResponse` | Budget response including `spent` field |
| `SummaryResponse` | Aggregated summary with `by_category` list |

## Transaction Validation Rules
- `amount` must be > 0
- `description`, `category`, `member_name` must be non-empty strings
- `type` must be `"income"` or `"expense"`
- All string fields are stripped of whitespace on input

## Budget Upsert Behavior
`POST /finance/budgets` is an upsert — if a budget already exists for `(user_id, month, year, category)`, it updates the amount. Uses Supabase `upsert()` with `on_conflict` on the unique constraint.

## Database Tables
| Table | Key Columns |
|---|---|
| `transactions` | `id`, `user_id`, `date`, `description`, `amount`, `type`, `category`, `member_name` |
| `budgets` | `id`, `user_id`, `month`, `year`, `category`, `amount` |

RLS is enabled on both tables. The backend uses the service role key (bypasses RLS).

## Summary Aggregation
`GET /finance/summary` groups transactions by `(category, type)` and returns totals + counts. The `spent` field on `BudgetResponse` is computed by summing expense transactions for that category in the given month.

## Adding New Transaction Categories
Categories are defined in the **frontend** `modules/finance/index.js` as `FINANCE_CATEGORIES`. The backend accepts any non-empty string — no validation against a fixed list. If you restrict categories, add a `Literal` type or a DB enum.
