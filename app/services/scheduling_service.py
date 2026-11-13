from app.db import schedule_repository as schedule_repo

def get_aailable_slots(position):
    return schedule_repo.get_available_slots(position)