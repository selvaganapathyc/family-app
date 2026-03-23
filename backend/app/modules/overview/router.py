from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.modules.overview import service

router = APIRouter(tags=["overview"])


@router.get("/summary")
def get_summary(current_user: dict = Depends(get_current_user)):
    return service.get_overview_summary(current_user["user_id"])
