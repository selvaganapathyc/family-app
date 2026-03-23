from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.core.dependencies import get_current_user
from app.modules.health import service
from app.modules.health.models import (
    VitalCreate, VitalUpdate, VitalResponse,
    MedicationCreate, MedicationUpdate, MedicationResponse,
    AppointmentCreate, AppointmentUpdate, AppointmentResponse,
)

router = APIRouter(tags=["Health Module"])


# ─── Dashboard ────────────────────────────────────────────────────────────────

@router.get("/dashboard")
def get_dashboard(current_user: dict = Depends(get_current_user)):
    return service.get_dashboard(current_user["user_id"])


# ─── Vitals ───────────────────────────────────────────────────────────────────

@router.get("/vitals", response_model=list[VitalResponse])
def get_vitals(
    member_name: Optional[str] = Query(None),
    vital_type: Optional[str] = Query(None),
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return service.list_vitals(
        user_id=current_user["user_id"],
        member_name=member_name,
        vital_type=vital_type,
        from_date=from_date,
        to_date=to_date,
    )


@router.get("/vitals/latest", response_model=list[VitalResponse])
def get_latest_vitals(current_user: dict = Depends(get_current_user)):
    return service.get_latest_vitals(current_user["user_id"])


@router.post("/vitals", response_model=VitalResponse, status_code=201)
def create_vital(data: VitalCreate, current_user: dict = Depends(get_current_user)):
    return service.create_vital(current_user["user_id"], data)


@router.put("/vitals/{vital_id}", response_model=VitalResponse)
def update_vital(
    vital_id: str,
    data: VitalUpdate,
    current_user: dict = Depends(get_current_user),
):
    return service.update_vital(vital_id, current_user["user_id"], data)


@router.delete("/vitals/{vital_id}", status_code=200)
def delete_vital(vital_id: str, current_user: dict = Depends(get_current_user)):
    return service.delete_vital(vital_id, current_user["user_id"])


# ─── Medications ──────────────────────────────────────────────────────────────

@router.get("/medications", response_model=list[MedicationResponse])
def get_medications(
    member_name: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return service.list_medications(
        user_id=current_user["user_id"],
        member_name=member_name,
        is_active=is_active,
    )


@router.post("/medications", response_model=MedicationResponse, status_code=201)
def create_medication(data: MedicationCreate, current_user: dict = Depends(get_current_user)):
    return service.create_medication(current_user["user_id"], data)


@router.put("/medications/{med_id}", response_model=MedicationResponse)
def update_medication(
    med_id: str,
    data: MedicationUpdate,
    current_user: dict = Depends(get_current_user),
):
    return service.update_medication(med_id, current_user["user_id"], data)


@router.delete("/medications/{med_id}", status_code=200)
def delete_medication(med_id: str, current_user: dict = Depends(get_current_user)):
    return service.delete_medication(med_id, current_user["user_id"])


# ─── Appointments ─────────────────────────────────────────────────────────────

@router.get("/appointments", response_model=list[AppointmentResponse])
def get_appointments(
    member_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None, pattern="^(scheduled|completed|cancelled)$"),
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    return service.list_appointments(
        user_id=current_user["user_id"],
        member_name=member_name,
        status=status,
        from_date=from_date,
        to_date=to_date,
    )


@router.post("/appointments", response_model=AppointmentResponse, status_code=201)
def create_appointment(data: AppointmentCreate, current_user: dict = Depends(get_current_user)):
    return service.create_appointment(current_user["user_id"], data)


@router.put("/appointments/{appt_id}", response_model=AppointmentResponse)
def update_appointment(
    appt_id: str,
    data: AppointmentUpdate,
    current_user: dict = Depends(get_current_user),
):
    return service.update_appointment(appt_id, current_user["user_id"], data)


@router.delete("/appointments/{appt_id}", status_code=200)
def delete_appointment(appt_id: str, current_user: dict = Depends(get_current_user)):
    return service.delete_appointment(appt_id, current_user["user_id"])
