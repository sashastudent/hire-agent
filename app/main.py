from app.modules.main_agent import main_agent_module as main_agent
from app.modules.interview_scheduling_advisor import interview_scheduling_advisor_module as scheduling_advisor
from app.modules.conversation_exit_advisor import conversation_exit_advisor_module as conversation_exit_advisor
from app.modules.conversation_exit_advisor.conversation_exit_advisor_module import get_exit_decision


def history_to_turns(messages):
     """LangChain memory (human / ai) -> the format the exit advisor was trained on"""
     speaker = {"human": "candidate", "ai": "recruiter"}
     return [{"speaker": speaker[m.type], "text":m.content}
              for m in messages if m.type in speaker]

def orchestrate_conversation_with_memory(user_input, session_id="user1"):
    history = main_agent.get_history(session_id)

    # 1. Exit advisor - runs on EVERY turn, on the conversation including the new message
    turns = history_to_turns(history.messages) + [{"speaker": "candidate", "text": user_input}]
    decision = get_exit_decision(turns)
    print("Exit advisor", decision)

    # 2a. schedule -> the scheduling advisor writes the reply INSTEAD of the main agent
    if decision == "schedule":
        full_convo = "\n".join(f"{t['speaker'].capitalize()}: {t['text']}" for t in turns)
        advisor_response = scheduling_advisor.advisor_executor.invoke({"input": full_convo})["output"]

        # save this turn to memory ourselves (the main agent didn't run, so nothing saved it)
        history.add_user_message(user_input)
        history.add_ai_message(advisor_response)
        return advisor_response

    # 2b. continue / end -> the main agent writes the reply (memory is saved automatically)
    return main_agent.main_agent_with_memory.invoke(
         {"input": user_input, "advisor_decision": decision},
         config={"configurable": {"session_id": session_id}},
    )["output"]


def run_agent(user_input, session_id="user1"):
    return orchestrate_conversation_with_memory(user_input, session_id)    
     

# def main():
#     response = run_agent()

# if __name__ == "__main__":
#     main()