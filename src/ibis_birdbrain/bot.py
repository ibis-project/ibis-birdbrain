"""Ibis Birdbrain bot.

A bot can be called to perform tasks on behalf of a user, in turn calling
its available tools (including other bots) to perform those tasks.
"""

# imports
import ibis

from uuid import uuid4
from typing import Any
from datetime import datetime

from ibis.backends.base import BaseBackend

from ibis_birdbrain.logging import log
from ibis_birdbrain.messages import Message
from ibis_birdbrain.utils.messages import to_message


# classes
class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime

    data: dict[str, BaseBackend]
    name: str
    user_name: str
    description: str
    version: str

    current_subject: str

    def __init__(
        self,
        data: dict[str, str] = {
            "system": "duckdb://birdbrain.ddb",
            "memory": "duckdb://",
        },
        name="birdbrain",
        user_name="user",
        description="Ibis Birdbrain bot.",
        version="infinity",
    ) -> None:
        """Initialize the bot."""
        self.id = uuid4()
        self.created_at = datetime.now()

        self.data = {k: ibis.connect(v) for k, v in data.items()}
        self.name = name
        self.user_name = user_name
        self.description = description
        self.version = version

        self.current_subject = ""

    def __call__(
        self,
        text: str = "Who are you and what can you do?",
        stuff: list[Any] = [],
    ) -> Message:
        """Call upon the bot."""

        log.info(f"Bot {self.name} called with text: {text}")
        im = to_message(text, stuff)

        return im
