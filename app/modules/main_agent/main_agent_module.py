from app.config import client

history = []

def main_agent(user_input):

    history.append({"role": "assistant", "message": "You are a hiring agent. Your job is to chat with candidates."})
    history.append({"role":"user", "message": user_input})
    completion = client.chat.completions.create(
        model = "gpt-4o",
        messages=history,
    )

    history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content