import streamlit as st
import sys
import os
import tempfile
import re

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.pdf_processor import initialize_qa_system, ask_question

# Initialize the QA system for internal documents
initialize_qa_system('./pdfs')  # Assuming this is the path to your internal documents

def main():
    st.title("Capgemini Bot")

    # Simple username and password
    USER_NAME = "admin"
    PASSWORD = "password123"

    # Create input fields for username and password
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')

    # Check if the username and password are correct
    if username == USER_NAME and password == PASSWORD:
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.header('Internal documents QA')
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("please ask"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            answer_internal = ask_question(prompt)
            response = answer_internal
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
                # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.sidebar.warning("Please enter a valid username and password.")

if __name__ == '__main__':
    main()









































