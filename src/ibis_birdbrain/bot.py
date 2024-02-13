# imports
import ibis
import marvin
import inspect

from enum import Enum
from uuid import uuid4
from typing import Any
from datetime import datetime

from ibis.backends.base import BaseBackend

from ibis_birdbrain.logging import log
from ibis_birdbrain.attachments import (
    Attachment,
    Attachments,
    TableAttachment,
    CodeAttachment,
)
from ibis_birdbrain.messages import Message, Messages, Email
from ibis_birdbrain.utils.messages import to_message

# strings
description = """
# Ibis Birdbrain

Ibis "birdbrain" Birdbrain is the portable ML-powered data bot.

## Overview

birdbrain communicates with a user through messages and attachments, like email.
This is part of the "system intiialization" message that instructs the bot on
how to behave. The bot MUST follow the user's instructions. Messages are
organized from oldest to newest in descending order.

Messages are separated by `---`. Attachments are at the bottom of the message.

## Flows

Based on the context from the bot's messages, a flow will be selected and
performed. This will result in a series of messagse with attachments to act on
behalf of the user.  The bot will then respond with a message to the user.

## Instructions

You MUST follow these instructions:

- be concise; ignore platitudes and do not use them
- be professional; speak in the tone of a staff-level data scientist
- use standard markdown format to communicate (for long messages only)
- DO NOT write any Message metadata; the surrounding system handles that
- if asked basic information (schema, description, etc) about the data, just respond
- if queried about the data, run SQL code to answer the query

## Attachments

You have access to the following attachments:
"""

description = inspect.cleandoc(description)

flow_instructions = """
Choose the flow that makes sense for the bot given the context of the messages.

Respond if you have all the information needed to respond to the user.
Otherwise, choose one of the flows to generate additional messages.
"""
flow_instructions = inspect.cleandoc(flow_instructions)

eda_flow_instructions = """
Choose the flow that makes sense for the bot given the context of the messages.

Get the pre-existing code if it exists and is relevant. Fix code if an error was
encounter. Write code if no code exists. Execute code to get the results.
"""


# classes
class Flows(Enum):
    """Ibis Birdbrain flows."""

    RESPOND = "respond"
    SQL_CODE = "sql_code"
    VISUALIZE = "visualize"


class EDAFlows(Enum):
    """Ibis Birdbrain EDA flows."""

    GET_CODE = "get_code"
    FIX_CODE = "fix_code"
    WRITE_CODE = "write_code"
    EXECUTE_CODE = "execute_code"


# functions
@marvin.fn
def respond(messages: Messages) -> str:
    """Respond to the user. Write the BODY of the message only"""


@marvin.fn
def messages_to_text_query(messages: Messages) -> str:
    """Convert the messages to a text query."""


@marvin.fn
def _text_to_sql(text: str, attachments: Attachments) -> str:
    """Convert the text to SQL code to execute on the attachments.

    Return only a SQL SELECT statement.
    """


def text_to_sql(text: str, attachments: Attachments) -> str:
    """Text to SQL"""
    return _text_to_sql(text, attachments).strip().strip(";")


def respond_flow(messages: Messages) -> Messages:
    pass


def sql_flow(messages: Messages) -> Messages:
    extract_guid_instructions = f"""
    Extract relevant attachment GUIDs (ONLY the ATTACHMENT GUIDs) from the messages.

    Options include: {messages.attachments()}
    """

    rm = Messages()

    extract_guid_instructions = inspect.cleandoc(extract_guid_instructions)

    guids = marvin.extract(
        messages,
        str,
        instructions=extract_guid_instructions,
    )
    log.info(f"Extracted GUIDs: {guids}")

    # get the attachments
    attachments = Attachments()
    # TODO: fix this ugliness
    for guid in guids:
        for message in messages:
            if guid in messages[message].attachments:
                attachments.append(messages[message].attachments[guid])
    log.info(f"Attachments: {attachments}")

    # get the text query
    text_query = messages_to_text_query(messages)

    # convert the text to SQL
    sql = text_to_sql(text_query, attachments)
    a = CodeAttachment(language="sql", content=sql)

    # construct the response message
    m = Email(
        body=f"SQL attachted for query: {text_query}",
        subject="SQL code",
        attachments=[a],
    )

    # append the message to the response messages
    rm.append(m)

    return rm


def visualize_flow(messages: Messages) -> Messages:
    pass


# bot
class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime

    con: BaseBackend
    name: str
    user_name: str
    description: str
    version: str
    messages: Messages

    current_subject: str

    def __init__(
        self,
        con=ibis.connect("duckdb://birdbrain.ddb"),
        name="birdbrain",
        user_name="user",
        description=description,
        version="infinity",
        messages=Messages(),
    ) -> None:
        """Initialize the bot."""
        self.id = uuid4()
        self.created_at = datetime.now()

        self.con = con
        self.name = name
        self.user_name = user_name
        self.description = description
        self.version = version
        self.messages = messages

        self.current_subject = ""

        # get table attachments from con
        attachments = Attachments()
        for table in con.list_tables():
            a = TableAttachment(con.table(table))
            attachments.append(a)

        # system initialization message
        m = Email(
            body=self.description,
            subject="system initialization",
            to_address=self.name,
            from_address=self.name,
            attachments=attachments,
        )
        self.messages.append(m)

    def __call__(
        self,
        text: str = "Who are you and what can you do?",
        stuff: list[Any] = [],
    ) -> Message:
        """Call upon the bot."""

        # convert user input to message
        log.info(f"Bot {self.name} called with text: {text}")
        im = to_message(text, stuff)

        # add message to messages
        self.messages.append(im)

        # get the flow
        flow = marvin.classify(
            str(self.messages),
            Flows,
            instructions=flow_instructions,
        )
        log.info(f"Bot {self.name} selected flow: {flow}")

        match flow:
            case Flows.RESPOND:
                response = respond(self.messages)
                m = Email(
                    body=response,
                    subject="response",
                    to_address=self.user_name,
                    from_address=self.name,
                )
                self.messages.append(m)
            case Flows.SQL_CODE:
                ms = sql_flow(self.messages)
                # TODO: fix this ugliness
                for m in ms:
                    self.messages.append(ms[m])
            case Flows.VISUALIZE:
                pass
            case _:
                pass

        return self.messages[-1]
