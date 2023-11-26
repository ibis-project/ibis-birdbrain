"""
Messages in Ibis Birdbrain are how people and computers communicate with each other
effectively and efficiently. Messages are metadata + text + attachments, where
attachments are arbitrary Python objects allowing for interaction with data,
code, visualization, and other useful objects.
"""

# imports
from uuid import uuid4
from datetime import datetime

from ibis.expr.types.relations import Table

from ibis_birdbrain.strings import (
    DEFAULT_MESSAGE_EVALUATION_SYSTEM,
    DEFAULT_RESPONSE_SYSTEM,
)
from ibis_birdbrain.attachments import Attachment, Attachments

from ibis_birdbrain.ml.functions import write_response
from ibis_birdbrain.ml.classifiers import true_or_false


# classes
class Message:
    """A message."""

    id: str
    created_at: datetime
    to_address: str
    from_address: str
    subject: str
    body: str
    attachments: Attachments

    def __init__(
        self,
        to_address="",
        from_address="",
        subject="",
        body="",
        attachments: Attachments | list[Attachment] = [],
    ) -> None:
        """Initialize the message."""
        self.id = str(uuid4())
        self.created_at = datetime.now()

        self.to_address = to_address
        self.from_address = from_address
        self.subject = subject
        self.body = body

        # TODO: feels a little hacky
        if isinstance(attachments, Attachments):
            self.attachments = attachments
        else:
            self.attachments = Attachments(attachments=attachments)

    def encode(self) -> Table:
        ...

    def decode(self, t: Table) -> str:
        ...

    def add_attachment(self, attachment: Attachment):
        """Add an attachment to the email."""
        self.attachments.append(attachment)

    def append(self, attachment: Attachment):
        """Alias for add_attachment."""
        self.add_attachment(attachment)

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"

    def __repr__(self):
        return str(self)


class Messages:
    """A collection of messages."""

    messages: dict[str, Message]

    def __init__(
        self,
        messages: list[Message] = [],
    ) -> None:
        """Initialize the messages."""
        self.messages = {m.id: m for m in messages}

    def add_message(self, message: Message):
        """Add a message to the collection."""
        self.messages[message.id] = message

    def append(self, message: Message):
        """Alias for add_message."""
        self.add_message(message)

    def __getitem__(self, id: str | int):
        """Get a message from the collection."""
        if isinstance(id, int):
            return list(self.messages.values())[id]
        return self.messages[id]

    def __setitem__(self, id: str, message: Message):
        """Set a message in the collection."""
        self.messages[id] = message

    def __len__(self) -> int:
        """Get the length of the collection."""
        return len(self.messages)

    def __iter__(self):
        """Iterate over the collection."""
        return iter(self.messages.keys())

    def __str__(self):
        return f"---\n".join([str(m) for m in self.messages.values()])

    def __repr__(self):
        return str(self)

    def attachments(self) -> list[str]:
        """Get the list of attachment GUIDs from the messages."""
        return list(set([a for m in self.messages.values() for a in m.attachments]))

    def get(self, text: str) -> Message:
        """Get a message by text."""
        # TODO: implement w/ ML
        ...

    def evaluate(self, instructions: str = DEFAULT_MESSAGE_EVALUATION_SYSTEM) -> bool:
        """Evaluate the messages."""
        TrueFalse = true_or_false(instructions=instructions)
        return TrueFalse(str(self)).value

    def respond(self, instructions: str = DEFAULT_RESPONSE_SYSTEM) -> Message:
        """Respond to the messages."""
        r = write_response(str(self), instructions=instructions)
        m = Email(body=r)

        return m


# exports
from ibis_birdbrain.messages.email import Email

__all__ = ["Message", "Messages", "Email"]
