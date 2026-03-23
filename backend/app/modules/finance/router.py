from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_current_user
from app.modules.finance import service
from app.modules.finance.models import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    BudgetCreate,
    BudgetResponse,
    SummaryResponse,
)

router = APIRouter(prefix="/finance", tags=["Finance"])


# ─── Transactions ─────────────────────────────────────────────────────────────

@router.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(
    month: Optional[int] = Query(default=None, ge=1, le=12),
    year: Optional[int] = Query(default=None, ge=2000, le=2100),
    type: Optional[str] = Query(default=None, pattern="^(income|expense)$"),
    member: Optional[str] = Query(default=None),
    current_user: dict = Depends(get_current_user),
):
    return service.list_transactions(
        user_id=current_user["user_id"],
        month=month,
        year=year,
        type_filter=type,
        member_name=member,
    )


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    data: TransactionCreate,
    current_user: dict = Depends(get_current_user),
):
    return service.create_transaction(
        user_id=current_user["user_id"], data=data
    )


@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: str,
    data: TransactionUpdate,
    current_user: dict = Depends(get_current_user),
):
    return service.update_transaction(
        transaction_id=transaction_id,
        user_id=current_user["user_id"],
        data=data,
    )


@router.delete(
    "/transactions/{transaction_id}",
    status_code=status.HTTP_200_OK,
)
def delete_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user),
):
    return service.delete_transaction(
        transaction_id=transaction_id,
        user_id=current_user["user_id"],
    )


# ─── Budgets ──────────────────────────────────────────────────────────────────

@router.get("/budgets", response_model=list[BudgetResponse])
def get_budgets(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
    current_user: dict = Depends(get_current_user),
):
    return service.list_budgets(
        user_id=current_user["user_id"], month=month, year=year
    )


@router.post(
    "/budgets",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_budget(
    data: BudgetCreate,
    current_user: dict = Depends(get_current_user),
):
    return service.upsert_budget(user_id=current_user["user_id"], data=data)


# ─── Summary ──────────────────────────────────────────────────────────────────

@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
    current_user: dict = Depends(get_current_user),
):
    return service.get_summary(
        user_id=current_user["user_id"], month=month, year=year
    )
