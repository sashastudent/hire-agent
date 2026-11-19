from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory as ChatMessageHistory
from langchain_core.tools import tool
from app.modules.conversation_info_advisor.conversation_info_advisor_module import get_info_from_pdf, POSITIONS
from app.services import scheduling_service


@tool
def get_job_info(position: str, question: str) -> str:
    """Answer a question about an open job position using its official job description (PDF).
    Use it to learn the position's requirements, and whenever the candidate asks something about the job.
    position: the job title the candidate is applying for, exactly as in the open positions list.
    question: the question to answer, in English."""
    return get_info_from_pdf(position, question)


@tool
def book_interview(position: str, slot_date: str, slot_time: str) -> str:
    """Book (reserve) an interview slot after the candidate chose one of the slots offered to them.
    position: the job title, exactly as in the open positions list.
    slot_date: the chosen date in YYYY-MM-DD format.
    slot_time: the chosen time in HH:MM format (24h)."""
    return scheduling_service.book_interview(position, slot_date, slot_time)


tools = [get_job_info, book_interview]

prompt_path = Path(__file__).parent / "main_agent_prompt.txt"
with open(prompt_path, 'r', encoding='utf-8') as f:
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
        ("system", "Conversation advisor recommendation for this turn: {advisor_decision}. "
                   "continue = keep the conversation going, schedule = move to scheduling an interview, "
                   "end = politely close the conversation."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
]).partial(positions="\n".join(f"- {p}" for p in POSITIONS))   # fill {positions} from the PDFs in Chroma

main_agent = create_openai_tools_agent(llm, tools=tools, prompt=main_prompt)
main_executor = AgentExecutor(agent=main_agent, tools=tools, verbose=False)

main_agent_with_memory = RunnableWithMessageHistory(
        main_executor,
        get_session_history=get_history,
        input_messages_key="input",
        history_messages_key="history"
)
