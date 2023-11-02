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
from ibis_birdbrain.messages import Email
from ibis_birdbrain.attachments import (
    TextAttachment,
    WebpageAttachment,
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
data_con = ibis.connect(f"{config['data']['backend_uri']}", read_only=False)
data_bases = config["data"]["databases"]

# ai bot
bot = Bot(sys_con=sys_con, doc_con=docs_con, data_con=data_con, data_bases=data_bases)


# functions
def process_message(message: Email):
    """
    Process message and attachments into appropriate streamlit component.
    """
    results = []
    results.append(st.markdown(message.body))
    for attachment in message.attachments:
        if isinstance(attachment, TextAttachment):
            results.append(st.markdown(attachment.open()))
        elif isinstance(attachment, WebpageAttachment):
            results.append(st.markdown(attachment.open()))  # TODO: better
        elif isinstance(attachment, TableAttachment):
            results.append(st.dataframe(attachment.open(), use_container_width=True))
        elif isinstance(attachment, ChartAttachment):
            results.append(st.plotly_chart(attachment.open(), use_container_width=True))
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
