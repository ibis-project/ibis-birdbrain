"""
Ibis Birdbrain.
"""

# imports
import ibis

from uuid import uuid4
from typing import Any
from datetime import datetime

from rich.console import Console
from ibis.backends.base import BaseBackend

from ibis_birdbrain.lui import Lui
from ibis_birdbrain.messages import Messages, Message

from ibis_birdbrain.systems import DEFAULT_NAME, DEFAULT_USER_NAME

from ibis_birdbrain.utils.strings import shorten_str


# classes
class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime
    console: Console

    lui: Lui
    messages: Messages
    name: str
    user_name: str
    description: str
    system: str
    version: str
    sys_con: BaseBackend
    doc_con: BaseBackend
    data_con: BaseBackend
    data_bases: list[str]

    def __init__(
        self,
        lui=Lui(),
        messages=Messages(),
        name=DEFAULT_NAME,
        user_name=DEFAULT_USER_NAME,
        description="the portable Python AI-powered data bot",
        system="",
        version="infinity",
        sys_con=ibis.connect("duckdb://birdbrain.ddb"),
        doc_con=ibis.connect("duckdb://docs.ddb"),
        data_con=ibis.connect("duckdb://"),
        data_bases=[],
    ) -> None:
        """Initialize the bot."""
        self.id = uuid4()
        self.created_at = datetime.now()
        self.console = Console()

        self.messages = messages
        self.name = name
        self.user_name = user_name
        self.description = description
        self.system = system
        self.version = version
        self.sys_con = sys_con
        self.doc_con = doc_con
        self.data_con = data_con
        self.data_bases = data_bases

        self.lui = lui

    def __call__(
        self,
        text: str,
        stuff: list[Any] = [],
    ) -> Message:
        """Call upon the bot."""

        # process input
        input_message = self.lui.preprocess(text, stuff, self.data_con, self.data_bases, self.doc_con)
        input_message.to_address = self.name
        input_message.from_address = self.user_name
        input_message.subject = shorten_str(text)
        self.messages.append(input_message)

        # process system
        system_message = self.lui.system(input_message)
        system_message.to_address = self.name
        system_message.from_address = self.name
        system_message.subject = f"[internal] re: {input_message.subject}"
        self.messages.append(system_message)

        # process output
        output_message = self.lui.postprocess(system_message)
        output_message.to_address = self.user_name
        output_message.from_address = self.name
        output_message.subject = f"re: {input_message.subject}"
        self.messages.append(output_message)

    def __repr__(self):
        """Represent the bot."""
        return f"<Bot name={self.name} description={self.description} version={self.version} id={self.id}>"
