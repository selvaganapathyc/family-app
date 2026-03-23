from datetime import date
from app.core.database import supabase_client as db


# ─── Vitals ───────────────────────────────────────────────────────────────────

def get_vitals(user_id: str, filters: dict) -> list:
    query = (
        db.table("health_vitals")
        .select("*")
        .eq("user_id", user_id)
        .order("date", desc=True)
    )
    if filters.get("member_name"):
        query = query.eq("member_name", filters["member_name"])
    if filters.get("vital_type"):
        query = query.eq("vital_type", filters["vital_type"])
    if filters.get("from_date"):
        query = query.gte("date", filters["from_date"])
    if filters.get("to_date"):
        query = query.lte("date", filters["to_date"])
    response = query.execute()
    return response.data or []


def create_vital(user_id: str, data: dict) -> dict:
    payload = {**data, "user_id": user_id}
    if hasattr(payload.get("date"), "isoformat"):
        payload["date"] = payload["date"].isoformat()
    response = db.table("health_vitals").insert(payload).execute()
    return response.data[0]


def update_vital(vital_id: str, user_id: str, data: dict) -> dict:
    if "date" in data and hasattr(data["date"], "isoformat"):
        data["date"] = data["date"].isoformat()
    response = (
        db.table("health_vitals")
        .update(data)
        .eq("id", vital_id)
        .eq("user_id", user_id)
        .execute()
    )
    return response.data[0] if response.data else {}


def delete_vital(vital_id: str, user_id: str) -> bool:
    db.table("health_vitals").delete().eq("id", vital_id).eq("user_id", user_id).execute()
    return True


def get_latest_vitals_per_member(user_id: str) -> list:
    """Fetch the most recent reading of each vital type per member for dashboard."""
    response = (
        db.table("health_vitals")
        .select("*")
        .eq("user_id", user_id)
        .order("date", desc=True)
        .limit(100)
        .execute()
    )
    rows = response.data or []

    # Keep only the latest entry per (member_name, vital_type)
    seen = set()
    result = []
    for row in rows:
        key = (row["member_name"], row["vital_type"])
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result


# ─── Medications ──────────────────────────────────────────────────────────────

def get_medications(user_id: str, filters: dict) -> list:
    query = (
        db.table("health_medications")
        .select("*")
        .eq("user_id", user_id)
        .order("start_date", desc=True)
    )
    if filters.get("member_name"):
        query = query.eq("member_name", filters["member_name"])
    if filters.get("is_active") is not None:
        query = query.eq("is_active", filters["is_active"])
    response = query.execute()
    return response.data or []


def create_medication(user_id: str, data: dict) -> dict:
    payload = {**data, "user_id": user_id}
    for field in ("start_date", "end_date"):
        if payload.get(field) and hasattr(payload[field], "isoformat"):
            payload[field] = payload[field].isoformat()
    response = db.table("health_medications").insert(payload).execute()
    return response.data[0]


def update_medication(med_id: str, user_id: str, data: dict) -> dict:
    for field in ("start_date", "end_date"):
        if field in data and data[field] and hasattr(data[field], "isoformat"):
            data[field] = data[field].isoformat()
    response = (
        db.table("health_medications")
        .update(data)
        .eq("id", med_id)
        .eq("user_id", user_id)
        .execute()
    )
    return response.data[0] if response.data else {}


def delete_medication(med_id: str, user_id: str) -> bool:
    db.table("health_medications").delete().eq("id", med_id).eq("user_id", user_id).execute()
    return True


# ─── Appointments ─────────────────────────────────────────────────────────────

def get_appointments(user_id: str, filters: dict) -> list:
    query = (
        db.table("health_appointments")
        .select("*")
        .eq("user_id", user_id)
        .order("date", desc=True)
    )
    if filters.get("member_name"):
        query = query.eq("member_name", filters["member_name"])
    if filters.get("status"):
        query = query.eq("status", filters["status"])
    if filters.get("from_date"):
        query = query.gte("date", filters["from_date"])
    if filters.get("to_date"):
        query = query.lte("date", filters["to_date"])
    response = query.execute()
    return response.data or []


def create_appointment(user_id: str, data: dict) -> dict:
    payload = {**data, "user_id": user_id}
    if hasattr(payload.get("date"), "isoformat"):
        payload["date"] = payload["date"].isoformat()
    response = db.table("health_appointments").insert(payload).execute()
    return response.data[0]


def update_appointment(appt_id: str, user_id: str, data: dict) -> dict:
    if "date" in data and hasattr(data["date"], "isoformat"):
        data["date"] = data["date"].isoformat()
    response = (
        db.table("health_appointments")
        .update(data)
        .eq("id", appt_id)
        .eq("user_id", user_id)
        .execute()
    )
    return response.data[0] if response.data else {}


def delete_appointment(appt_id: str, user_id: str) -> bool:
    db.table("health_appointments").delete().eq("id", appt_id).eq("user_id", user_id).execute()
    return True


def get_upcoming_appointments(user_id: str) -> list:
    today = date.today().isoformat()
    response = (
        db.table("health_appointments")
        .select("*")
        .eq("user_id", user_id)
        .eq("status", "scheduled")
        .gte("date", today)
        .order("date", desc=False)
        .limit(10)
        .execute()
    )
    return response.data or []
