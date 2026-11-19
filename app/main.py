from datetime import date
from app.modules.main_agent import main_agent_module as main_agent
from app.modules.interview_scheduling_advisor import interview_scheduling_advisor_module as scheduling_advisor
from app.modules.conversation_exit_advisor import conversation_exit_advisor_module as conversation_exit_advisor
from app.modules.conversation_exit_advisor.conversation_exit_advisor_module import get_exit_decision
from app.modules.conversation_info_advisor.conversation_info_advisor_module import POSITIONS


def history_to_turns(messages):
     """LangChain memory (human / ai) -> the format the exit advisor was trained on"""
     speaker = {"human": "candidate", "ai": "recruiter"}
     return [{"speaker": speaker[m.type], "text":m.content}
              for m in messages if m.type in speaker]

# sessions whose candidate already passed the screening (the main agent called mark_candidate_qualified)
qualified_sessions = set()


def orchestrate_conversation_with_memory(user_input, session_id="user1"):
    history = main_agent.get_history(session_id)

    # 1. Exit advisor - runs on EVERY turn, on the conversation including the new message
    turns = history_to_turns(history.messages) + [{"speaker": "candidate", "text": user_input}]
    decision = get_exit_decision(turns)
    print("Exit advisor", decision)

    # the main agent has the final say: no scheduling before the candidate passed the screening
    if decision == "schedule" and session_id not in qualified_sessions:
        print("schedule -> continue (screening not finished yet)")
        decision = "continue"

    # 2a. schedule -> the scheduling advisor writes the reply INSTEAD of the main agent
    if decision == "schedule":
        advisor_response = suggest_slots(turns)

        # save this turn to memory ourselves (the main agent didn't run, so nothing saved it)
        history.add_user_message(user_input)
        history.add_ai_message(advisor_response)
        return advisor_response

    # 2b. continue / end -> the main agent writes the reply (memory is saved automatically)
    result = main_agent.main_agent_with_memory.invoke(
         {"input": user_input, "advisor_decision": decision, "positions": ", ".join(POSITIONS)},
         config={"configurable": {"session_id": session_id}},
    )

    reply = result["output"]

    # did the main agent decide THIS turn that the candidate meets the requirements?
    tools_called = [action.tool for action, _ in result["intermediate_steps"]]
    if "mark_candidate_qualified" in tools_called and session_id not in qualified_sessions:
        qualified_sessions.add(session_id)
        print("candidate qualified -> offering interview slots")

        # move straight to scheduling: add the 3 slots to the same reply
        turns = history_to_turns(history.messages)
        reply = reply + "\n\n" + suggest_slots(turns)
        history.messages[-1].content = reply      # keep memory = what the candidate actually saw

    return reply


def suggest_slots(turns):
    """Scheduling advisor: the 3 nearest available slots, based on the conversation"""
    full_convo = "\n".join(f"{t['speaker'].capitalize()}: {t['text']}" for t in turns)
    return scheduling_advisor.advisor_executor.invoke(
        {"input": full_convo, "today": str(date.today()), "positions": ", ".join(POSITIONS)}
    )["output"]


def run_agent(user_input, session_id="user1"):
    return orchestrate_conversation_with_memory(user_input, session_id)    
     

# def main():
#     response = run_agent()

# if __name__ == "__main__":
#     main()