# imports
import time
import ibis
import inspect

import streamlit as st

from dotenv import load_dotenv

from ibis_birdbrain.bot import Bot
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
description = f"""
This is the IMDB database with a few tables.

Join them on `tconst`. If asked about `movies`, make sure to filter on `titleType` of `movie`.
"""
description = inspect.cleandoc(description)

# ml-powered data bot
bot = Bot(con=con, data_description=description)


# functions
def process_message(message, include_attachments=False):
    """
    Process message and attachments into appropriate streamlit component.
    """
    results = []
    results.append(st.markdown(message.body))
    if include_attachments:
        for attachment in message.attachments:
            a = message.attachments[attachment]  # TODO: hack
            if isinstance(a, CodeAttachment):
                expander = st.expander(label=a.language, expanded=False)
                results.append(expander.markdown(f"```{a.language}\n{a.open()}"))
            # elif isinstance(a, TextAttachment):
            #     results.append(st.markdown(a.open()))
            # elif isinstance(a, ErrorAttachment):
            #     results.append(st.markdown(a.open()))
            # elif isinstance(a, WebpageAttachment):
            #     results.append(st.markdown(a.open()))  # TODO: better?
            # elif isinstance(a, DataAttachment):
            # results.append(st.markdown(a.open()))
            elif isinstance(a, TableAttachment):
                results.append(
                    st.dataframe(
                        a.open().limit(1000).to_pandas(), use_container_width=True
                    )
                )
            # elif isinstance(a, ChartAttachment):
            #     results.append(st.plotly_chart(a.open(), use_container_width=True))
            # else:
            #     results.append(st.markdown("Unknown attachment type"))

    return results


# header
f"""
# Ibis Birdbrain
"""

with st.expander(label="data", expanded=False):
    tables_str = ""
    for table in con.list_tables():
        tables_str += f"- {table} ({str(con.table(table).schema())})\n"

    st.markdown(tables_str)

# take input
if prompt := st.chat_input("ask birdbrain..."):
    with st.spinner("birdbrain is thinking..."):
        time.sleep(3)
        bot(prompt)

# display history
for message in bot.messages:
    # user-to-bot message
    if (
        bot.messages[message].from_address == bot.user_name
        and bot.messages[message].to_address == bot.name
    ):
        with st.chat_message("user"):  # bot.messages[message].from_address):
            process_message(bot.messages[message])
    # bot-to-user message
    elif (
        bot.messages[message].from_address == bot.name
        and bot.messages[message].to_address == bot.user_name
    ):
        with st.chat_message("assistant"):  # bot.messages[message].from_address):
            process_message(bot.messages[message], include_attachments=True)
