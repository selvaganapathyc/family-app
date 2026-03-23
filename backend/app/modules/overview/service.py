from datetime import date, datetime, timedelta
from app.core.database import get_supabase_client


def get_overview_summary(user_id: str) -> dict:
    db = get_supabase_client()
    now = date.today()
    month, year = now.month, now.year

    # --- Finance snapshot ---
    txn_response = (
        db.table("transactions")
        .select("type, amount, description, member_name, created_at")
        .eq("user_id", user_id)
        .gte("date", f"{year}-{month:02d}-01")
        .lte("date", f"{year}-{month:02d}-{now.day:02d}")
        .order("created_at", desc=True)
        .execute()
    )
    transactions = txn_response.data or []

    total_income = sum(float(t["amount"]) for t in transactions if t["type"] == "income")
    total_expenses = sum(float(t["amount"]) for t in transactions if t["type"] == "expense")

    # --- Budget alerts ---
    budget_response = (
        db.table("budgets")
        .select("category, amount")
        .eq("user_id", user_id)
        .eq("month", month)
        .eq("year", year)
        .execute()
    )
    budgets = budget_response.data or []

    alerts = []
    for budget in budgets:
        spent = sum(
            float(t["amount"])
            for t in transactions
            if t["type"] == "expense" and t.get("category") == budget["category"]
        )
        pct = (spent / float(budget["amount"]) * 100) if budget["amount"] else 0
        if pct >= 100:
            alerts.append({
                "id": f"budget-{budget['category']}",
                "message": f"{budget['category']} budget exceeded ({pct:.0f}% used)",
                "module": "Finance",
                "icon": "🚨",
                "severity": "danger",
            })
        elif pct >= 80:
            alerts.append({
                "id": f"budget-{budget['category']}",
                "message": f"{budget['category']} budget at {pct:.0f}%",
                "module": "Finance",
                "icon": "⚠️",
                "severity": "warning",
            })

    # --- Recent activity (last 5 transactions) ---
    def time_ago(created_at_str: str) -> str:
        try:
            created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            diff = datetime.now(created_at.tzinfo) - created_at
            if diff.seconds < 3600:
                return f"{diff.seconds // 60}m ago"
            if diff.days == 0:
                return f"{diff.seconds // 3600}h ago"
            if diff.days == 1:
                return "Yesterday"
            return f"{diff.days}d ago"
        except Exception:
            return ""

    recent_activity = [
        {
            "id": i,
            "member": t["member_name"],
            "memberInitial": t["member_name"][0].upper() if t["member_name"] else "?",
            "action": f"added {t['type']} · {t['description']}",
            "amount": float(t["amount"]),
            "type": t["type"],
            "module": "Finance",
            "timeAgo": time_ago(t["created_at"]),
        }
        for i, t in enumerate(transactions[:5])
    ]

    return {
        "alerts": alerts,
        "recentActivity": recent_activity,
        "finance": {
            "totalIncome": total_income,
            "totalExpenses": total_expenses,
            "netBalance": total_income - total_expenses,
        },
    }
