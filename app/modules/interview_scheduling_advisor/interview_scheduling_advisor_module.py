from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from app.services import scheduling_service


@tool
def get_next_three_dates(position: str, start_date: str) -> str:
    """Get the next 3 available interview slots for a position, starting from a date.
    position: one of the exact position names from the open positions list (e.g. 'Python Dev').
    start_date: the earliest date to search from, in YYYY-MM-DD format."""
    return scheduling_service.get_available_slots(position, start_date)


tools = [get_next_three_dates]
llm = ChatOpenAI(model="gpt-4o-2024-11-20", temperature=0)

# Advisor agent: Receives the conversation, extracts the desired date, and suggests slots
advisor_prompt = ChatPromptTemplate.from_messages([
("system",
 "You are an appointment advisor. From the full conversation, extract the position the candidate "
 "is applying for and any preferred date. "
 "The open positions are: {positions}. Always pass the position to the tool using one of these exact names "
 "(for example, if the candidate wrote 'Python', use 'Python Dev'). "
 "Then use the get_next_three_dates tool and suggest the 3 slots it returns, in this format:\n"
 "- Option 1: ...\n- Option 2: ...\n- Option 3: ...\n"
 "If no preferred date is found, search from today's date: {today}. "
 "Only suggest slots returned by the tool - never invent slots."),

("user", "{input}"),
MessagesPlaceholder(variable_name="agent_scratchpad")
])



advisor_agent = create_openai_tools_agent(llm, tools, prompt=advisor_prompt)
advisor_executor = AgentExecutor(agent=advisor_agent, tools=tools, verbose=True)


