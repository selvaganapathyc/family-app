from fastapi import HTTPException
from app.modules.health import queries
from app.modules.health.models import (
    VitalCreate, VitalUpdate, VitalResponse,
    MedicationCreate, MedicationUpdate, MedicationResponse,
    AppointmentCreate, AppointmentUpdate, AppointmentResponse,
)


# ─── Vitals ───────────────────────────────────────────────────────────────────

def list_vitals(user_id: str, member_name=None, vital_type=None, from_date=None, to_date=None):
    filters = {}
    if member_name:
        filters["member_name"] = member_name
    if vital_type:
        filters["vital_type"] = vital_type
    if from_date:
        filters["from_date"] = from_date
    if to_date:
        filters["to_date"] = to_date
    rows = queries.get_vitals(user_id, filters)
    return [VitalResponse(**row) for row in rows]


def create_vital(user_id: str, data: VitalCreate):
    payload = data.model_dump()
    row = queries.create_vital(user_id, payload)
    return VitalResponse(**row)


def update_vital(vital_id: str, user_id: str, data: VitalUpdate):
    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise HTTPException(status_code=422, detail="No fields provided to update")
    row = queries.update_vital(vital_id, user_id, payload)
    if not row:
        raise HTTPException(status_code=404, detail="Vital not found or access denied")
    return VitalResponse(**row)


def delete_vital(vital_id: str, user_id: str):
    queries.delete_vital(vital_id, user_id)
    return {"message": "Deleted successfully"}


def get_latest_vitals(user_id: str):
    rows = queries.get_latest_vitals_per_member(user_id)
    return [VitalResponse(**row) for row in rows]


# ─── Medications ──────────────────────────────────────────────────────────────

def list_medications(user_id: str, member_name=None, is_active=None):
    filters = {}
    if member_name:
        filters["member_name"] = member_name
    if is_active is not None:
        filters["is_active"] = is_active
    rows = queries.get_medications(user_id, filters)
    return [MedicationResponse(**row) for row in rows]


def create_medication(user_id: str, data: MedicationCreate):
    payload = data.model_dump()
    row = queries.create_medication(user_id, payload)
    return MedicationResponse(**row)


def update_medication(med_id: str, user_id: str, data: MedicationUpdate):
    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise HTTPException(status_code=422, detail="No fields provided to update")
    row = queries.update_medication(med_id, user_id, payload)
    if not row:
        raise HTTPException(status_code=404, detail="Medication not found or access denied")
    return MedicationResponse(**row)


def delete_medication(med_id: str, user_id: str):
    queries.delete_medication(med_id, user_id)
    return {"message": "Deleted successfully"}


# ─── Appointments ─────────────────────────────────────────────────────────────

def list_appointments(user_id: str, member_name=None, status=None, from_date=None, to_date=None):
    filters = {}
    if member_name:
        filters["member_name"] = member_name
    if status:
        filters["status"] = status
    if from_date:
        filters["from_date"] = from_date
    if to_date:
        filters["to_date"] = to_date
    rows = queries.get_appointments(user_id, filters)
    return [AppointmentResponse(**row) for row in rows]


def create_appointment(user_id: str, data: AppointmentCreate):
    payload = data.model_dump()
    row = queries.create_appointment(user_id, payload)
    return AppointmentResponse(**row)


def update_appointment(appt_id: str, user_id: str, data: AppointmentUpdate):
    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise HTTPException(status_code=422, detail="No fields provided to update")
    row = queries.update_appointment(appt_id, user_id, payload)
    if not row:
        raise HTTPException(status_code=404, detail="Appointment not found or access denied")
    return AppointmentResponse(**row)


def delete_appointment(appt_id: str, user_id: str):
    queries.delete_appointment(appt_id, user_id)
    return {"message": "Deleted successfully"}


# ─── Dashboard ────────────────────────────────────────────────────────────────

def get_dashboard(user_id: str):
    latest_vitals = queries.get_latest_vitals_per_member(user_id)
    upcoming_appointments = queries.get_upcoming_appointments(user_id)
    active_medications = queries.get_medications(user_id, {"is_active": True})

    return {
        "latest_vitals": latest_vitals,
        "upcoming_appointments": upcoming_appointments,
        "active_medications": active_medications,
    }
