import streamlit as st
import app.main as agent

st.title("Job Hire Agent")

# אתחול פעם אחת עבור השיחה הנוכחית
if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת ההודעות הקודמות
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input()

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    answer = agent.run_agent(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)