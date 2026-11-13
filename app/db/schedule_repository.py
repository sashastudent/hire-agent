from datetime import datetime, timedelta

def get_available_slots(position):
    #replace this with a database query to fetch available slots for the given position
    'This fuction recieves a date and then return 3 optional dates'
    start_date = datetime.now().strftime("%Y-%m-%d")  # Get today's date as a string in the format 'YYYY-MM-DD'
    date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    return [
        (date_obj + timedelta(days=3)).strftime("%Y-%m-%d"),
        (date_obj + timedelta(days=6)).strftime("%Y-%m-%d"),
        (date_obj + timedelta(days=9)).strftime("%Y-%m-%d"),
    ]
    pass

def reserve_slot(schedule_id):
    # UPDATE Schedule
    pass