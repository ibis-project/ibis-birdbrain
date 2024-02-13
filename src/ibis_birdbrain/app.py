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
    CodeAttachment,
    ErrorAttachment,
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

## ibis config
ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 20
ibis.options.repr.interactive.max_columns = None

# TODO: move to config.toml or something
con = ibis.connect("duckdb://app.ddb")

# ml-powered data bot
bot = Bot(con=con)


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
        elif isinstance(a, CodeAttachment):
            results.append(st.markdown(a.open()))
        elif isinstance(a, ErrorAttachment):
            results.append(st.markdown(a.open()))
        elif isinstance(a, WebpageAttachment):
            results.append(st.markdown(a.open()))  # TODO: better?
        elif isinstance(a, DataAttachment):
            results.append(st.markdown(a.open()))
        elif isinstance(a, TableAttachment):
            results.append(
                st.dataframe(a.open().limit(10).to_pandas(), use_container_width=True)
            )
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
    if (
        bot.messages[message].from_address == bot.name
        and bot.messages[message].to_address == bot.user_name
    ) or (
        bot.messages[message].from_address == bot.user_name
        and bot.messages[message].to_address == bot.name
    ):
        with st.chat_message(bot.messages[message].from_address):
            process_message(bot.messages[message])
