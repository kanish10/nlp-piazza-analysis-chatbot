import streamlit as st
import pandas as pd
import subprocess
import platform
import random
import time
import io

from helpers import getResponseFromModel
#=============================================================================
# Chatbot Page
#=============================================================================

st.subheader("Chatbot")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.write("Ask me anything and I'll answer your questions using data from Piazza!")
# Check if chat history is empty
# if st.session_state.messages == []:
#     st.write("Ask me anything and I'll answer your questions using data from Piazza!")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Piazza AI: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(io.StringIO(getResponseFromModel(prompt)))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    