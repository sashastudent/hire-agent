import streamlit as st
import app.main as agent


st.title("Job Hire Agent")
user_input = st.chat_input()

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    answer = agent.run_agent(user_input)
    with st.chat_message("assistant"):
        st.write(answer)