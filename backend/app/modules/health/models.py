from datetime import date, datetime, time
from typing import Literal, Optional
from pydantic import BaseModel, field_validator


# ─── Vitals ───────────────────────────────────────────────────────────────────

VITAL_UNITS = {
    "Weight": "kg",
    "Blood Pressure Systolic": "mmHg",
    "Blood Pressure Diastolic": "mmHg",
    "Heart Rate": "bpm",
    "Temperature": "°C",
    "Blood Glucose": "mg/dL",
    "SpO2": "%",
}


class VitalCreate(BaseModel):
    member_name: str
    date: date
    vital_type: str
    value: float
    unit: str
    notes: Optional[str] = None

    @field_validator("value")
    def value_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Value must be greater than 0")
        return v


class VitalUpdate(BaseModel):
    member_name: Optional[str] = None
    date: Optional[date] = None
    vital_type: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None


class VitalResponse(BaseModel):
    id: str
    user_id: str
    member_name: str
    date: date
    vital_type: str
    value: float
    unit: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


# ─── Medications ──────────────────────────────────────────────────────────────

class MedicationCreate(BaseModel):
    member_name: str
    name: str
    dosage: str
    frequency: str
    start_date: date
    end_date: Optional[date] = None
    is_active: bool = True
    notes: Optional[str] = None


class MedicationUpdate(BaseModel):
    member_name: Optional[str] = None
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class MedicationResponse(BaseModel):
    id: str
    user_id: str
    member_name: str
    name: str
    dosage: str
    frequency: str
    start_date: date
    end_date: Optional[date] = None
    is_active: bool
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


# ─── Appointments ─────────────────────────────────────────────────────────────

class AppointmentCreate(BaseModel):
    member_name: str
    doctor_name: str
    specialty: str
    date: date
    time: Optional[str] = None
    status: Literal["scheduled", "completed", "cancelled"] = "scheduled"
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    member_name: Optional[str] = None
    doctor_name: Optional[str] = None
    specialty: Optional[str] = None
    date: Optional[date] = None
    time: Optional[str] = None
    status: Optional[Literal["scheduled", "completed", "cancelled"]] = None
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: str
    user_id: str
    member_name: str
    doctor_name: str
    specialty: str
    date: date
    time: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
