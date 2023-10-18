"""
Ibis Birdbrain bot.
"""

# imports
import ibis

import plotly.express as px

from uuid import uuid4
from rich.console import Console
from ibis.backends.base import BaseBackend

from ibis_birdbrain.tasks import Task
from ibis_birdbrain.messages import Message, Email
from ibis_birdbrain.attachments import (
    StringAttachment,
    TableAttachment,
    ChartAttachment,
)

from typing import Any

from random import choice


# classes
class Bot:
    """Ibis Birdbrain bot."""

    bot_id: str = str(uuid4())
    console: Console = Console()
    messages: list[Message] = []

    name: str
    description: str
    system: str
    version: str

    sys_con: BaseBackend | None
    doc_con: BaseBackend | None
    data_cons: dict[str, BaseBackend] | None

    def __init__(
        self,
        name="assistant",
        description="the portable Python AI-powered data bot",
        system="",
        version="infinity",
        sys_con=None,
        doc_con=None,
        data_cons=None,
    ) -> None:
        """Initialize the bot."""

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
        self.data_cons = data_cons if data_cons is not None else {}
        self.data_cons["local_duckdb"] = ibis.connect("duckdb://")

    def __call__(self, text: str) -> Any:
        """Call upon the bot."""
        message = Email(to_address=[self.name], from_address="user", body=text)
        self.messages.append(message)

        t = self.data_cons["tpch"].table("lineitem").limit(1000)

        a = StringAttachment(content="squawk!")
        b = ChartAttachment(
            content=px.bar(
                t.group_by("l_returnflag").agg(ibis._.count().name("count")),
                x="l_returnflag",
                y="count",
            )
        )
        c = TableAttachment(content=t)

        message = Email(
            to_address=["user"],
            from_address=self.name,
            subject=f"re: {self.messages[-1].subject}",
            attachments=[choice([a, b, c])],
        )
        if choice([True, False]):
            message.add_attachment(choice([a, b, c]))
        self.messages.append(message)
        return message

    def __repr__(self):
        """Represent the bot."""
        return f"<Bot name={self.name} description={self.description} version={self.version} id={self.bot_id}>"
