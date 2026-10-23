from app.config import client
from pathlib import Path

history = []
prompt_path = Path(__file__).parent / "main_agent_prompt.txt"

with open(prompt_path,'r', encoding='utf-8') as f:
    instructions = f.read()
    
history.append({"role": "system", "content": instructions})

def main_agent(user_input):

    history.append({"role":"user", "content": user_input})
    
    completion = client.chat.completions.create(
        model = "gpt-4o",
        messages=history,
    )

    answer = completion.choices[0].message.content
    history.append({"role":"user", "content": answer})
    
    return answer