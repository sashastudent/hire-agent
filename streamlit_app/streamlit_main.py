import streamlit as st
import app.main as agent
from uuid import uuid4

st.title("Job Hire Agent")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

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

    answer = agent.orchestrate_conversation_with_memory(user_input, st.session_state.session_id)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)


