import streamlit as st

from random import randint

import ibis
import marvin
import IPython

from ibis_birdbrain.tools.eda import con
from ibis_birdbrain.bots.birdbrain import bot as birdbrain

# configure Ibis
birdbrain.interactive = False
ibis.options.interactive = True

# Title and description
f"""
# Ibis Birdbrain demo

**work in progress -- extremely experimental**

**MAJOR BUG**: asking the bot to list tables will list Ibis analytics tables (stars, forks, etc.) that the bot doesn't actually have access to. This is a bug in DuckDB, MotherDuck, or Ibis. Only query the imdb tables or the penguins table (after reading the excel file) -- the bot does not have access to the Ibis analytics databases.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "bot" not in st.session_state:
    st.session_state.bot = birdbrain

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me about data!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if prompt == "/test":
        response = str(st.session_state.bot.ai.history)
    else:
        response = st.session_state.bot(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
