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
from ibis_birdbrain.messages import Messages, Message

from ibis_birdbrain.systems import DEFAULT_NAME, DEFAULT_USER_NAME

from ibis_birdbrain.utils.strings import shorten_str


# classes
class BotData:
    """Ibis Birdbrain bot data."""

    data: dict[str, BaseBackend]

    def __init__(self, data: dict[str, str]) -> None:
        """Initialize the bot data."""
        self.data = {k: ibis.connect(v) for k, v in data.items()}

    def __getitem__(self, key: str) -> BaseBackend:
        """Get a data connection."""
        return self.data[key]

    def __setitem__(self, key: str, value: BaseBackend) -> None:
        """Set a data connection."""
        self.data[key] = value

    def __repr__(self):
        """Represent the bot data."""
        return f"<BotData data={self.data}>"


class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime

    lui: Lui
    messages: Messages
    name: str
    user_name: str
    description: str
    system: str
    version: str
    data: BotData

    def __init__(
        self,
        data,
        lui=Lui(),
        messages=Messages(),
        name=DEFAULT_NAME,
        user_name=DEFAULT_USER_NAME,
        description="the portable Python ML-powered data bot",
        system="",
        version="infinity",
    ) -> None:
        """Initialize the bot."""
        self.id = uuid4()
        self.created_at = datetime.now()

        self.data = data
        self.lui = lui
        self.messages = messages
        self.name = name
        self.user_name = user_name
        self.description = description
        self.system = system
        self.version = version

    def __call__(
        self,
        text: str,
        stuff: list[Any] = [],
    ) -> Any:
        """Call upon the bot."""

        # process input
        input_message = self.lui.preprocess(
            text,
            stuff,
            self.data.data,
            first_message=(len(self.messages) == 0),
        )
        input_message.to_address = self.name
        input_message.from_address = self.user_name
        input_message.subject = shorten_str(text)
        self.messages.append(input_message)

        return

        # process system
        # system_message = self.lui.system(input_message)
        # return system_message
        # system_message.to_address = self.name
        # system_message.from_address = self.name
        # system_message.subject = f"[internal] re: {input_message.subject}"
        # self.messages.append(system_message)

        ## process output
        # output_message = self.lui.postprocess(system_message)
        # output_message.to_address = self.user_name
        # output_message.from_address = self.name
        # output_message.subject = f"re: {input_message.subject}"
        # self.messages.append(output_message)

    def __repr__(self):
        """Represent the bot."""
        return f"<Bot name={self.name} description={self.description} version={self.version} id={self.id}>"
