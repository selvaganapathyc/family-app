# Overview Module (Backend)

## Purpose
Aggregates data across all modules for the frontend overview screen. Returns budget alerts, recent activity feed, and per-module financial snapshots for the current month.

## Endpoints
| Method | Path | Description |
|---|---|---|
| GET | `/overview/summary` | Full overview data for the logged-in user |

All endpoints require Bearer token auth via `get_current_user` dependency.

## File Structure
```
modules/overview/
├── __init__.py
├── router.py       # Route definitions
└── service.py      # All aggregation logic — queries transactions and budgets directly
```

## Response Shape
```json
{
  "alerts": [
    {
      "id": "budget-Food & Dining",
      "message": "Food & Dining budget at 85%",
      "module": "Finance",
      "icon": "⚠️",
      "severity": "warning"
    }
  ],
  "recentActivity": [
    {
      "id": 0,
      "member": "Selva",
      "memberInitial": "S",
      "action": "added expense · Groceries",
      "amount": 1500.0,
      "type": "expense",
      "module": "Finance",
      "timeAgo": "2h ago"
    }
  ],
  "finance": {
    "totalIncome": 50000.0,
    "totalExpenses": 22000.0,
    "netBalance": 28000.0
  }
}
```

## Alert Thresholds (Finance)
- `>= 80%` of budget used → `warning` severity
- `>= 100%` of budget used → `danger` severity

## Notes
- Overview queries the DB directly — does not call other module services
- Scoped to current calendar month (auto-detected from `date.today()`)
- Returns last 5 transactions as recent activity
- Gracefully returns empty lists if no data exists (no errors)

## Adding Health/Education Alerts
When health or education modules are built, add their alert logic to `service.get_overview_summary()` and append to the `alerts` list before returning.
