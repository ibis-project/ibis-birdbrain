# imports
from uuid import uuid4
from typing import Union, List
from datetime import datetime

from ibis.expr.types.relations import Table

from ibis_birdbrain.attachments import Attachment, Attachments


# classes
class Message:
    """Ibis Birdbrain message."""

    id: str
    created_at: datetime
    to_address: str
    from_address: str
    subject: str
    body: str
    attachments: Attachments

    def __init__(
        self,
        body="",
        to_address="",
        from_address="",
        subject="",
        attachments: Attachments | list[Attachment] = [],
    ) -> None:
        """Initialize the message."""
        self.id = str(uuid4())
        self.created_at = datetime.now()

        self.body = body
        self.to_address = to_address
        self.from_address = from_address
        self.subject = subject

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
    """Ibis Birdbrain messages."""

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

    def extend(self, messages: Union[List[Message], "Messages"]):
        """Add multiple messages to the collection."""
        if isinstance(messages, Messages):
            messages = list(messages.messages.values())
        for message in messages:
            self.append(message)

        return self

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


# exports
from ibis_birdbrain.messages.email import Email

__all__ = ["Message", "Messages", "Email"]
