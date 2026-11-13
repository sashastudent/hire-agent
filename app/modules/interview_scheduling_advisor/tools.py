from langchain_core.tools import tool
from app.services import scheduling_service

@tool
def get_next_three_dates(start_date):
    "Get available interview slots for a position."
    return scheduling_service.get_aailable_slots(start_date)

    