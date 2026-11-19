from datetime import date, time
from app.db import schedule_repository as schedule_repo


def get_available_slots(position, start_date):
    """start_date: 'YYYY-MM-DD'. Returns the slots as readable text for the LLM."""
    rows = schedule_repo.get_available_slots(position, date.fromisoformat(start_date))
    if not rows:
        return f"No available slots for '{position}' from {start_date}."
    return "\n".join(
        f"ScheduleID {r.ScheduleID}: {r.date:%A %Y-%m-%d} at {r.time:%H:%M}" for r in rows
    )


def book_interview(position, slot_date, slot_time):
    """slot_date: 'YYYY-MM-DD', slot_time: 'HH:MM'. Reserves the slot and returns the result as text for the LLM."""
    d = date.fromisoformat(slot_date)
    t = time.fromisoformat(slot_time)

    schedule_id = schedule_repo.find_slot(position, d, t)
    if schedule_id is None:
        return f"There is no '{position}' interview slot on {slot_date} at {slot_time}."

    if not schedule_repo.reserve_slot(schedule_id):
        return f"The slot on {slot_date} at {slot_time} is already taken. Offer the candidate other slots."

    return f"Booked: '{position}' interview on {d:%A %Y-%m-%d} at {t:%H:%M} (ScheduleID {schedule_id})."
