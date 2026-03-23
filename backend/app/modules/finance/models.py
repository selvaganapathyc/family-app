from pydantic import BaseModel, field_validator
from typing import Optional, Literal, List
from datetime import date, datetime


# ─── Transaction Models ───────────────────────────────────────────────────────

class TransactionCreate(BaseModel):
    date: date
    description: str
    amount: float
    type: Literal["income", "expense"]
    category: str
    member_name: str

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @field_validator("description", "category", "member_name")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field must not be empty")
        return v.strip()


class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = None
    member_name: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class TransactionResponse(BaseModel):
    id: str
    user_id: str
    date: date
    description: str
    amount: float
    type: str
    category: str
    member_name: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── Budget Models ────────────────────────────────────────────────────────────

class BudgetCreate(BaseModel):
    month: int
    year: int
    category: str
    amount: float

    @field_validator("month")
    @classmethod
    def valid_month(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError("Month must be between 1 and 12")
        return v

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Budget amount must be greater than 0")
        return v


class BudgetResponse(BaseModel):
    id: str
    user_id: str
    month: int
    year: int
    category: str
    amount: float
    spent: float = 0.0

    model_config = {"from_attributes": True}


# ─── Summary Models ───────────────────────────────────────────────────────────

class CategorySummary(BaseModel):
    category: str
    type: str
    total: float
    count: int


class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    by_category: List[CategorySummary]
