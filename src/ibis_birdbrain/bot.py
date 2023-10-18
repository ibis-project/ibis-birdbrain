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

from ibis_birdbrain.tasks import Task
from ibis_birdbrain.messages import Message, Email, Messages
from ibis_birdbrain.attachments import (
    Attachment,
    TextAttachment,
    TableAttachment,
    ChartAttachment,
    Attachments,
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
    sys_con: BaseBackend | None
    doc_con: BaseBackend | None
    data_con: BaseBackend | None
    data_bases: list[str]

    def __init__(
        self,
        id=str(uuid4()),
        console=Console(),
        created_at=datetime.now(),
        messages=Messages(),
        name="assistant",
        description="the portable Python AI-powered data bot",
        system="",
        version="infinity",
        sys_con=None,
        doc_con=None,
        data_con=None,
        data_bases=None,
    ) -> None:
        """Initialize the bot."""
        self.id = id
        self.created_at = created_at
        self.console = console
        self.messages = messages
        self.name = name
        self.description = description
        self.system = system
        self.version = version

        self.sys_con = (
            sys_con if sys_con is not None else ibis.connect("duckdb://sys.ddb")
        )
        self.doc_con = (
            doc_con if doc_con is not None else ibis.connect("duckdb://docs.ddb")
        )
        self.data_con = data_con if data_con is not None else ibis.connect("duckdb://")
        self.data_bases = data_bases if data_bases is not None else []

    def __call__(
        self,
        text: str,
        subject: str = "help me with my data",
        attachment: Attachments = Attachments(),
    ) -> Message:
        """Call upon the bot."""
        message = Email(
            to_address=self.name, from_address="user", body=text, subject=subject
        )
        self.messages.append(message)

        # t = ibis.examples.penguins.fetch()
        t = self.data_con.table("stars")
        a = TextAttachment(content=f"squawk!\n\nyou've been squawked!")
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
