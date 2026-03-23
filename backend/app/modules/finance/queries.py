"""
Low-level Supabase query functions for the finance module.
All functions accept user_id to enforce data isolation.
"""
from typing import Optional
from app.core.database import supabase_client as db


# ─── Transactions ─────────────────────────────────────────────────────────────

def get_transactions(user_id: str, filters: dict) -> list:
    """
    Fetch transactions for a user, with optional filters:
    - month (int)
    - year (int)
    - type ('income' | 'expense')
    - member_name (str)
    """
    query = (
        db.table("transactions")
        .select("*")
        .eq("user_id", user_id)
        .order("date", desc=True)
    )

    if filters.get("type"):
        query = query.eq("type", filters["type"])

    if filters.get("member_name"):
        query = query.eq("member_name", filters["member_name"])

    # Filter by month/year using gte/lte on date column
    if filters.get("month") and filters.get("year"):
        month = int(filters["month"])
        year = int(filters["year"])
        from datetime import date
        import calendar
        last_day = calendar.monthrange(year, month)[1]
        start = date(year, month, 1).isoformat()
        end = date(year, month, last_day).isoformat()
        query = query.gte("date", start).lte("date", end)
    elif filters.get("year"):
        year = int(filters["year"])
        from datetime import date
        start = date(year, 1, 1).isoformat()
        end = date(year, 12, 31).isoformat()
        query = query.gte("date", start).lte("date", end)

    response = query.execute()
    return response.data or []


def create_transaction(user_id: str, data: dict) -> dict:
    """Insert a new transaction row and return the created record."""
    payload = {**data, "user_id": user_id}
    # Convert date object to string if needed
    if hasattr(payload.get("date"), "isoformat"):
        payload["date"] = payload["date"].isoformat()

    response = db.table("transactions").insert(payload).execute()
    return response.data[0]


def update_transaction(transaction_id: str, user_id: str, data: dict) -> dict:
    """Update a transaction belonging to user_id. Returns updated record."""
    # Remove None values so we only PATCH provided fields
    payload = {k: v for k, v in data.items() if v is not None}
    if hasattr(payload.get("date"), "isoformat"):
        payload["date"] = payload["date"].isoformat()

    response = (
        db.table("transactions")
        .update(payload)
        .eq("id", transaction_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not response.data:
        return {}
    return response.data[0]


def delete_transaction(transaction_id: str, user_id: str) -> bool:
    """Delete a transaction belonging to user_id. Returns True on success."""
    db.table("transactions").delete().eq("id", transaction_id).eq("user_id", user_id).execute()
    return True


# ─── Budgets ──────────────────────────────────────────────────────────────────

def get_budgets(user_id: str, month: int, year: int) -> list:
    """
    Fetch budgets for a given month/year.
    Enriches each budget with the 'spent' amount from transactions.
    """
    response = (
        db.table("budgets")
        .select("*")
        .eq("user_id", user_id)
        .eq("month", month)
        .eq("year", year)
        .execute()
    )
    budgets = response.data or []

    # Fetch expense transactions for the same month/year to compute spent
    from datetime import date
    import calendar
    last_day = calendar.monthrange(year, month)[1]
    start = date(year, month, 1).isoformat()
    end = date(year, month, last_day).isoformat()

    txn_response = (
        db.table("transactions")
        .select("category, amount")
        .eq("user_id", user_id)
        .eq("type", "expense")
        .gte("date", start)
        .lte("date", end)
        .execute()
    )
    txns = txn_response.data or []

    # Build spent-per-category map
    spent_map: dict[str, float] = {}
    for txn in txns:
        cat = txn["category"]
        spent_map[cat] = spent_map.get(cat, 0.0) + float(txn["amount"])

    # Attach spent to each budget
    for budget in budgets:
        budget["spent"] = spent_map.get(budget["category"], 0.0)

    return budgets


def create_or_update_budget(user_id: str, data: dict) -> dict:
    """
    Upsert a budget for (user_id, month, year, category).
    Uses Supabase upsert with on_conflict to handle duplicates.
    """
    payload = {**data, "user_id": user_id}
    response = (
        db.table("budgets")
        .upsert(payload, on_conflict="user_id,month,year,category")
        .execute()
    )
    result = response.data[0]

    # Compute spent for this single budget entry
    from datetime import date
    import calendar
    month = data["month"]
    year = data["year"]
    last_day = calendar.monthrange(year, month)[1]
    start = date(year, month, 1).isoformat()
    end = date(year, month, last_day).isoformat()

    txn_response = (
        db.table("transactions")
        .select("amount")
        .eq("user_id", user_id)
        .eq("type", "expense")
        .eq("category", data["category"])
        .gte("date", start)
        .lte("date", end)
        .execute()
    )
    spent = sum(float(t["amount"]) for t in (txn_response.data or []))
    result["spent"] = spent
    return result


# ─── Summary ──────────────────────────────────────────────────────────────────

def get_summary(user_id: str, month: int, year: int) -> dict:
    """
    Aggregate transactions for user_id in the given month/year.
    Returns total_income, total_expenses, net_balance, and by_category breakdown.
    """
    from datetime import date
    import calendar

    last_day = calendar.monthrange(year, month)[1]
    start = date(year, month, 1).isoformat()
    end = date(year, month, last_day).isoformat()

    response = (
        db.table("transactions")
        .select("amount, type, category")
        .eq("user_id", user_id)
        .gte("date", start)
        .lte("date", end)
        .execute()
    )
    txns = response.data or []

    total_income = 0.0
    total_expenses = 0.0
    # key: (category, type) → {total, count}
    cat_map: dict[tuple, dict] = {}

    for txn in txns:
        amount = float(txn["amount"])
        txn_type = txn["type"]
        category = txn["category"]

        if txn_type == "income":
            total_income += amount
        else:
            total_expenses += amount

        key = (category, txn_type)
        if key not in cat_map:
            cat_map[key] = {"total": 0.0, "count": 0}
        cat_map[key]["total"] += amount
        cat_map[key]["count"] += 1

    by_category = [
        {
            "category": cat,
            "type": txn_type,
            "total": round(values["total"], 2),
            "count": values["count"],
        }
        for (cat, txn_type), values in cat_map.items()
    ]
    by_category.sort(key=lambda x: x["total"], reverse=True)

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_balance": round(total_income - total_expenses, 2),
        "by_category": by_category,
    }
