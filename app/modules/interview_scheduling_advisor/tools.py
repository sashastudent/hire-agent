from langchain_core.tools import tool
from app.services import scheduling_service


@tool
def get_next_three_dates(position: str, start_date: str) -> str:
    """Get the next 3 available interview slots for a position, starting from a date.
    position: the job title exactly as it appears in the conversation (e.g. 'Python Dev').
    start_date: the earliest date to search from, in YYYY-MM-DD format."""
    return scheduling_service.get_available_slots(position, start_date)
