from app.config import client
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory as ChatMessageHistory


prompt_path = Path(__file__).parent / "main_agent_prompt.txt"
with open(prompt_path,'r', encoding='utf-8') as f:
    instructions = f.read()

store = {}
def get_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

llm = ChatOpenAI(model="gpt-4o-2024-11-20", temperature=0)

main_prompt = ChatPromptTemplate.from_messages([
        ("system", instructions),
        MessagesPlaceholder(variable_name="history"),
        ("user","{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
])

main_agent = create_openai_tools_agent(llm, tools=[], prompt=main_prompt)
main_executor = AgentExecutor(agent=main_agent, tools=[], verbose=False)

main_agent_with_memory = RunnableWithMessageHistory(
        main_executor,
        get_session_history=get_history,
        input_messages_key="input",
        history_messages_key="history"
)




