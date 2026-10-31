from app.modules.main_agent import main_agent_module as main_agent
from app.modules.interview_scheduling_advisor import interview_scheduling_advisor_module as scheduling_advisor

def orchestrate_conversation_with_memory(user_input, session_id="user1"):
    """
    Handles one turn of user input for the main agent (with memory),
    and if needed, passes the full memory/history to the advisor agent.
    """

    # Main agent receives latest user message (memory auto-injects context)
    main_output = main_agent.main_agent_with_memory.invoke({"input": user_input},config={"configurable": {"session_id": session_id}})["output"]
    print("Main Agent:", main_output)
    print("\n")

    # If scheduling is detected, advisor gets *full conversation* from memory
    if "I will check available slots for you" in main_output:
        
        # Retrieve full history from memory
        full_history = main_agent.get_history(session_id).messages
        full_convo = "\n".join([f"{m.type.capitalize()}: {m.content}" for m in full_history])
        
        advisor_response = scheduling_advisor.advisor_executor.invoke({"input": full_convo})["output"]
        main_agent.get_history(session_id).add_ai_message(advisor_response)
        print("\n\n")
        print("Advisor Agent:\n", advisor_response)
        return advisor_response
    
    return main_output

def run_agent(user_input, session_id="user1"):
    return orchestrate_conversation_with_memory(user_input, session_id)    
     

# def main():
#     response = run_agent()

# if __name__ == "__main__":
#     main()