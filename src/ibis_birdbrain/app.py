"""
Streamlit app to demo Ibis Birdbrain.
"""

# imports
import time
import toml
import ibis
import plotly

import streamlit as st
import plotly.express as px

from rich import print
from dotenv import load_dotenv
from datetime import datetime, timedelta

from ibis_birdbrain.bot import Bot
from ibis_birdbrain.messages import Message, Email
from ibis_birdbrain.attachments import (
    StringAttachment,
    TableAttachment,
    ChartAttachment,
)

# config
## load .env
load_dotenv()

## config.toml
config = toml.load("config.toml")

## streamlit config
st.set_page_config(layout="wide")

# data platforms
sys_con = ibis.connect(f"{config['system']['backend_uri']}", read_only=False)
docs_con = ibis.connect(f"{config['docs']['backend_uri']}", read_only=True)
data_cons = {
    c.split(":")[-1]: ibis.connect(c, read_only=True)
    for c in config["data"]["backend_uris"]
}

# ai bot
bot = Bot(sys_con=sys_con, doc_con=docs_con, data_cons=data_cons)


# functions
def process_message(message: Email):
    """
    Process message content into appropriate streamlit component.
    """
    results = []
    results.append(st.markdown(message.body))
    for attachment in message.attachments:
        if isinstance(attachment, StringAttachment):
            results.append(st.markdown(attachment.content))
        elif isinstance(attachment, TableAttachment):
            results.append(st.dataframe(attachment.content, use_container_width=True))
        elif isinstance(attachment, ChartAttachment):
            results.append(
                st.plotly_chart(attachment.content, use_container_width=True)
            )
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
    with st.chat_message(message.from_address):
        process_message(message)
