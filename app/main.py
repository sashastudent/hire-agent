from app.modules.main_agent import main_agent_module as main_agent


def run_agent(user_input):
    return main_agent.main_agent(user_input)    
     
#def assitent():
    #assit_agent

def main():
    response = run_agent()

if __name__ == "__main__":
    main()