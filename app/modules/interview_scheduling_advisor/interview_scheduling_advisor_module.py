from datetime import date
from app.modules.interview_scheduling_advisor.tools import get_next_three_dates
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI


tools = [get_next_three_dates]
llm = ChatOpenAI(model="gpt-4o-2024-11-20", temperature=0)

# Advisor agent: Receives the conversation, extracts the desired date, and suggests slots
advisor_prompt = ChatPromptTemplate.from_messages([
("system",
 "You are an appointment advisor. From the full conversation, extract the position the candidate "
 "is applying for and any preferred date. "
 "Then use the get_next_three_dates tool and suggest the 3 slots it returns, in this format:\n"
 "- Option 1: ...\n- Option 2: ...\n- Option 3: ...\n"
 "If no preferred date is found, search from today's date: {today}. "
 "Only suggest slots returned by the tool - never invent slots."),

("user", "{input}"),
MessagesPlaceholder(variable_name="agent_scratchpad")
]).partial(today=lambda: date.today().isoformat())   # a function -> evaluated on every call



advisor_agent = create_openai_tools_agent(llm, tools, prompt=advisor_prompt)
advisor_executor = AgentExecutor(agent=advisor_agent, tools=tools, verbose=True)


