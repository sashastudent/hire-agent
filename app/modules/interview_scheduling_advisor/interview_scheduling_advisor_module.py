from langchain_core.tools import tool
from datetime import datetime, timedelta
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI

#Creating the function
@tool
def get_next_three_dates(start_date):
    'This fuction recieves a date and then return 3 optional dates'
    # start_date should be a string in the format 'YYYY-MM-DD'
    date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    return [
        (date_obj + timedelta(days=3)).strftime("%Y-%m-%d"),
        (date_obj + timedelta(days=6)).strftime("%Y-%m-%d"),
        (date_obj + timedelta(days=9)).strftime("%Y-%m-%d"),
    ]


tools = [get_next_three_dates]
llm = ChatOpenAI(model="gpt-4o-2024-11-20", temperature=0)

# Advisor agent: Receives the conversation, extracts the desired date, and suggests slots
advisor_prompt = ChatPromptTemplate.from_messages([
("system", 
 "You are an appointment advisor. Extract any preferred dates from the full conversation. "
 "Then, suggest 3 possible appointment slots for the user, in this format:\n"
 "- Option 1: ...\n- Option 2: ...\n- Option 3: ...\n"
 "You can use the tools provided"
 "If no date is found, suggest generic options for next week."),

("user", "{input}"),
MessagesPlaceholder(variable_name="agent_scratchpad")
])



advisor_agent = create_openai_tools_agent(llm, tools, prompt=advisor_prompt)
advisor_executor = AgentExecutor(agent=advisor_agent, tools=tools, verbose=True)


