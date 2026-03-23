"""
Business logic layer for the finance module.
Sits between the router (HTTP) and queries (DB).
"""
from typing import Optional
from fastapi import HTTPException, status

from app.modules.finance import queries
from app.modules.finance.models import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    BudgetCreate,
    BudgetResponse,
    SummaryResponse,
    CategorySummary,
)


# ─── Transactions ─────────────────────────────────────────────────────────────

def list_transactions(
    user_id: str,
    month: Optional[int] = None,
    year: Optional[int] = None,
    type_filter: Optional[str] = None,
    member_name: Optional[str] = None,
) -> list[TransactionResponse]:
    filters = {}
    if month:
        filters["month"] = month
    if year:
        filters["year"] = year
    if type_filter:
        filters["type"] = type_filter
    if member_name:
        filters["member_name"] = member_name

    rows = queries.get_transactions(user_id, filters)
    return [TransactionResponse(**row) for row in rows]


def create_transaction(
    user_id: str, data: TransactionCreate
) -> TransactionResponse:
    payload = data.model_dump()
    row = queries.create_transaction(user_id, payload)
    return TransactionResponse(**row)


def update_transaction(
    transaction_id: str, user_id: str, data: TransactionUpdate
) -> TransactionResponse:
    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No fields provided to update",
        )
    row = queries.update_transaction(transaction_id, user_id, payload)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found or access denied",
        )
    return TransactionResponse(**row)


def delete_transaction(transaction_id: str, user_id: str) -> dict:
    queries.delete_transaction(transaction_id, user_id)
    return {"message": "Transaction deleted successfully"}


# ─── Budgets ──────────────────────────────────────────────────────────────────

def list_budgets(user_id: str, month: int, year: int) -> list[BudgetResponse]:
    rows = queries.get_budgets(user_id, month, year)
    return [BudgetResponse(**row) for row in rows]


def upsert_budget(user_id: str, data: BudgetCreate) -> BudgetResponse:
    payload = data.model_dump()
    row = queries.create_or_update_budget(user_id, payload)
    return BudgetResponse(**row)


# ─── Summary ──────────────────────────────────────────────────────────────────

def get_summary(user_id: str, month: int, year: int) -> SummaryResponse:
    data = queries.get_summary(user_id, month, year)
    by_category = [CategorySummary(**cat) for cat in data["by_category"]]
    return SummaryResponse(
        total_income=data["total_income"],
        total_expenses=data["total_expenses"],
        net_balance=data["net_balance"],
        by_category=by_category,
    )
