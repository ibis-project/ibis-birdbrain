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
    ErrorAttachment,
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


class SQLFlows(Enum):
    """Ibis Birdbrain SQL flows."""

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
    """Convert the messages to an English text query.

    Returns the English prose that concisely describes the desired query.
    """


@marvin.fn
def _text_to_sql(text: str, attachments: Attachments) -> str:
    """Convert the text to SQL code to execute on the attachments.

    Return only a SQL SELECT statement.
    """


def text_to_sql(text: str, attachments: Attachments) -> str:
    """Text to SQL"""
    return _text_to_sql(text, attachments).strip().strip(";")


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
                self.respond_flow()
            case Flows.SQL_CODE:
                self.sql_flow()
                self.respond_flow()
                # append the table attachment(s) to the response message
                # TODO: fix this ugliness
                for attachment in self.messages[-2].attachments:
                    if isinstance(
                        self.messages[-2].attachments[attachment], TableAttachment
                    ):
                        self.messages[-1].attachments.append(
                            self.messages[-2].attachments[attachment]
                        )
            case Flows.VISUALIZE:
                pass
            case _:
                pass

        return self.messages[-1]

    def sql_flow(self) -> None:
        extract_guid_instructions = f"""
        Extract relevant attachment GUIDs (ONLY the ATTACHMENT GUIDs) from the messages.

        Options include: {self.messages.attachments()}
        """

        extract_guid_instructions = inspect.cleandoc(extract_guid_instructions)

        guids = marvin.extract(
            self.messages,
            str,
            instructions=extract_guid_instructions,
        )
        log.info(f"Extracted GUIDs: {guids}")

        # get the attachments
        attachments = Attachments()
        # TODO: fix this ugliness
        for guid in guids:
            for message in self.messages:
                if guid in self.messages[message].attachments:
                    attachments.append(self.messages[message].attachments[guid])
        # log.info(f"Attachments: {attachments}")

        # get the text query
        text_query = messages_to_text_query(self.messages)

        # convert the text to SQL
        sql = text_to_sql(text_query, attachments)
        a = CodeAttachment(language="sql", content=sql)

        # run the SQL
        try:
            t = self.con.sql(sql)
            at = TableAttachment(t)
        except Exception as e:
            at = ErrorAttachment(e)
            log.error(f"SQL error: {e}")

        # construct the response message
        m = Email(
            body=f"SQL attachted for query: {text_query}",
            subject="SQL code",
            attachments=[a, at],
        )

        # append the message to the response messages
        self.messages.append(m)

    def respond_flow(self) -> None:
        response = respond(self.messages)
        m = Email(
            body=response,
            subject="response",
            to_address=self.user_name,
            from_address=self.name,
        )
        self.messages.append(m)

    def visualize_flow(self) -> None:
        pass
