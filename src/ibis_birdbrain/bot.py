"""
Ibis Birdbrain.
"""

# imports
import ibis

from uuid import uuid4
from typing import Any
from datetime import datetime

from ibis.backends.base import BaseBackend

from ibis_birdbrain.lui import Lui
from ibis_birdbrain.tasks import Tasks, tasks
from ibis_birdbrain.systems import (
    DEFAULT_NAME,
    DEFAULT_USER_NAME,
    DEFAULT_DESCRIPTION,
    DEFAULT_VERSION,
)
from ibis_birdbrain.messages import Messages, Message
from ibis_birdbrain.utils.strings import shorten_str


class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime

    data: dict[str, BaseBackend]
    lui: Lui
    tasks: Tasks
    messages: Messages
    name: str
    user_name: str
    description: str
    version: str

    def __init__(
        self,
        data: dict[str, str] = {"system": "duckdb://birdbrain.ddb"},
        tasks=tasks,
        lui=Lui(),
        messages=Messages(),
        name=DEFAULT_NAME,
        user_name=DEFAULT_USER_NAME,
        description=DEFAULT_DESCRIPTION,
        version=DEFAULT_VERSION,
    ) -> None:
        """Initialize the bot."""
        self.id = uuid4()
        self.created_at = datetime.now()

        self.data = {k: ibis.connect(v) for k, v in data.items()}
        self.lui = lui
        self.tasks = tasks
        self.messages = messages
        self.name = name
        self.user_name = user_name
        self.description = description
        self.version = version

    def __call__(
        self,
        text: str,
        stuff: list[Any] = [],
    ) -> Message:
        """Call upon the bot."""

        # process input
        input_message = self.lui.preprocess(
            self.messages,
            text,
            stuff,
            self.data,
        )
        input_message.to_address = self.name
        input_message.from_address = self.user_name
        input_message.subject = shorten_str(text)
        self.messages.append(input_message)

        # process system
        system_messages = self.lui.system(self.messages)
        for m in system_messages:
            m.to_address = self.name
            m.from_address = self.name
            m.subject = f"[internal] {m.subject}"
            self.messages.append(m)

        return self.messages[-1]

        ## process output
        # output_message = self.lui.postprocess(system_message)
        # output_message.to_address = self.user_name
        # output_message.from_address = self.name
        # output_message.subject = f"re: {input_message.subject}"
        # self.messages.append(output_message)

    def __repr__(self):
        """Represent the bot."""
        return f"<Bot name={self.name} id={self.id} description={self.description} version={self.version} data={list(self.data.keys())}>"
