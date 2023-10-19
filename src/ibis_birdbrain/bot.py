"""
Ibis Birdbrain bot.
"""

# imports
import ibis
import plotly.express as px

from uuid import uuid4
from datetime import datetime

from rich.console import Console
from ibis.backends.base import BaseBackend

from ibis_birdbrain.lui import Lui
from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.attachments import (
    Attachments,
    TextAttachment,
    TableAttachment,
    ChartAttachment,
)

from random import choice  # temp


# classes
class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime
    console: Console
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

    def __call__(
        self,
        text: str,
        subject: str = "help me with my data",
        attachments: Attachments = Attachments(),
    ) -> Message:
        """Call upon the bot."""

        # TODO: LUI for attachments
        message = Email(
            to_address=self.name,
            from_address="user",
            body=text,
            subject=subject,
            attachments=attachments,
        )
        self.messages.append(message)

        # TODO: LUI for tasks
        # t = ibis.examples.penguins.fetch()
        t = self.data_con.table("stars", schema="ibis_analytics.main")
        a = TextAttachment(content=f"squawk!"*100+" you've been squawked!")
        b = ChartAttachment(
            content=px.bar(
                t.group_by("company")
                .agg(ibis._.count().name("count"))
                .order_by(ibis._["count"].desc()),
                x="company",
                y="count",
            )
        )
        c = TableAttachment(content=t)

        # TODO: LUI for response
        message = Email(
            to_address="user",
            from_address=self.name,
            subject=f"re: {self.messages[-1].subject}",
            body="squawk!",
            attachments=[choice([a, b, c])],
        )
        if choice([False, True, False]):
            message.add_attachment(choice([a, b, c]))
        self.messages.append(message)
        return message
    
    def __repr__(self):
        """Represent the bot."""
        return f"<Bot name={self.name} description={self.description} version={self.version} id={self.id}>"
