# imports
import ibis

from uuid import uuid4
from typing import Any
from datetime import datetime

from ibis.backends.base import BaseBackend

from ibis_birdbrain.logging import log
from ibis_birdbrain.attachments import (
    Attachments,
    TableAttachment,
    DatabaseAttachment,
)
from ibis_birdbrain.flows import Flows
from ibis_birdbrain.strings import bot_description
from ibis_birdbrain.messages import Message, Messages, Email
from ibis_birdbrain.utils.strings import shorten_str
from ibis_birdbrain.utils.attachments import to_attachments

from ibis_birdbrain.flows.data import DataFlow


# bot
class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime

    con: BaseBackend
    name: str
    user_name: str
    description: str
    data_description: str
    version: str
    messages: Messages
    source_table_attachments: Attachments
    flows: Flows
    lm_response: bool
    conversational: bool

    current_subject: str

    def __init__(
        self,
        con=ibis.connect("duckdb://"),
        name="birdbrain",
        user_name="user",
        description=bot_description,
        data_description="",
        version="infinity",
        messages=Messages(),
        source_table_attachments=None,
        flows=Flows([DataFlow()]),
        lm_response=False,
        conversational=False,
    ) -> None:
        """Initialize the bot."""
        self.id = uuid4()
        self.created_at = datetime.now()

        self.con = con
        self.name = name
        self.user_name = user_name
        self.description = description
        self.data_description = data_description
        self.version = version
        self.messages = messages
        self.flows = flows

        self.lm_response = lm_response
        self.conversational = conversational

        self.current_subject = ""

        source_table_attachments = Attachments()
        for table in con.list_tables():
            a = TableAttachment(con.table(table))
            source_table_attachments.append(a)

        self.source_table_attachments = source_table_attachments

        # TODO: add flows to the description/body
        body = """TODO"""  # noqa

        # system initialization message
        system_message = Email(
            body=self.description,
            subject="system initialization",
            to_address=self.name,
            from_address=self.name,
            attachments=[DatabaseAttachment(con, description=self.data_description)],
        )
        self.messages.append(system_message)
        log.info(f"Bot {self.name} initialized...")

    def __call__(
        self,
        text: str = "Who are you and what can you do?",
        stuff: list[Any] = [],
    ) -> Message:
        """Call upon the bot."""

        log.info(f"Bot {self.name} called with text: {text}")

        # convert user input to message
        if self.current_subject == "":
            self.current_subject = shorten_str(text)

        input_attachments = to_attachments(stuff)

        input_message = Email(
            body=text,
            subject=self.current_subject,
            to_address=self.name,
            from_address=self.user_name,
            attachments=input_attachments,
        )

        # add message to messages
        self.messages.append(input_message)

        # if conversational, use all messages
        if self.conversational:
            flow_messages = self.messages
        else:
            flow_messages = Messages([self.messages[0], self.messages[-1]])

        # select the flow
        flow = self.flows.select_flow(flow_messages)

        # TODO: slight hack
        if flow.name == "data":
            flow_messages[-1].attachments.extend(self.source_table_attachments)

        # execute the flow
        result_messages = flow(flow_messages)

        # extend the messages
        self.messages.extend(result_messages)

        # generate the response
        response_attachments = Attachments()
        # TODO: smarter here
        for message in result_messages:
            response_attachments.extend(result_messages[message].attachments)
        response_message = Email(
            body="TODO",  # TODO: generate body from attachments
            subject=self.current_subject,
            to_address=self.user_name,
            from_address=self.name,
            attachments=response_attachments,
        )

        # update the response body
        if self.lm_response:
            response_message.body = self.respond(self.messages)
        else:
            response_message.body = "Ibis Birdbrain has attached the results."

        # add the response to the messages
        self.messages.append(response_message)

        # return the response
        self.messages[-1].to_address = self.user_name
        self.messages[-1].from_address = self.name
        return self.messages[-1]

    def respond(self, messages: Messages) -> Message:
        """Respond to the messages."""
        ...

    # TODO: for demo
    def translate_sql(self, sql: str, dialect_to: str, dialect_from: str) -> str:
        """Translate SQL from one dialect to another."""
        ...

    # TODO: for demo
    def execute_last_sql(self, con: BaseBackend) -> Message:
        """Execute the last SQL statement."""
        ...
