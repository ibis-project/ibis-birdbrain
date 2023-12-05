"""
Streamlit app to demo Ibis Birdbrain.
"""

# imports
import toml
import ibis

import streamlit as st
import plotly.express as px

from dotenv import load_dotenv

from ibis_birdbrain.bot import Bot
from ibis_birdbrain.subsystems import (
    Subsystems,
    EDA,
    Code,
    Docs,
)
from ibis_birdbrain.messages import Email
from ibis_birdbrain.attachments import (
    TextAttachment,
    WebpageAttachment,
    TableAttachment,
    DataAttachment,
    ChartAttachment,
)

# config
## load .env
load_dotenv()

## streamlit config
st.set_page_config(layout="wide")

## config.toml
config = toml.load("config.toml")

# data platforms
data = config["data"]

# subsystems
# TODO: re-add other subystems
subsystems = [EDA(), Code(), Docs()]
subsystems = Subsystems(subsystems)

# ml-powered data bot
bot = Bot(data, subsystems)


# functions
def process_message(message: Email):
    """
    Process message and attachments into appropriate streamlit component.
    """
    results = []
    results.append(st.markdown(message.body))
    for attachment in message.attachments:
        a = message.attachments[attachment]  # TODO: hack
        if isinstance(a, TextAttachment):
            results.append(st.markdown(a.open()))
        elif isinstance(a, WebpageAttachment):
            results.append(st.markdown(a.open()))  # TODO: better?
        elif isinstance(a, DataAttachment):
            results.append(st.markdown(a.open()))
        elif isinstance(a, TableAttachment):
            results.append(st.dataframe(a.open(), use_container_width=True))
        elif isinstance(a, ChartAttachment):
            results.append(st.plotly_chart(a.open(), use_container_width=True))
        else:
            results.append(st.markdown("Unknown attachment type"))

    return results


# header
f"""
# Ibis Birdbrain
"""

# take input
if prompt := st.chat_input("birdbrain..."):
    bot(prompt)

# display history
for message in bot.messages:
    with st.chat_message(bot.messages[message].from_address):
        process_message(bot.messages[message])
