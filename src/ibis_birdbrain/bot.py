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
from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.attachments import Attachments


# classes
class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime
    console: Console

    lui: Lui
    messages: Messages
    name: str
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
        name="assistant",
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
        attachments: Attachments = Attachments(),
    ) -> Message:
        """Call upon the bot."""

        input_message = self.lui.preprocess(text)
        system_message = self.lui.system(input_message)
        output_message = self.lui.postprocess(system_message)

        self.messages.append(output_message)

    def __repr__(self):
        """Represent the bot."""
        return f"<Bot name={self.name} description={self.description} version={self.version} id={self.id}>"
