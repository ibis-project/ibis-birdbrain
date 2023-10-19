# imports
from uuid import uuid4
from datetime import datetime

from ibis_birdbrain.attachments import Attachment, Attachments


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
        attachments=Attachments(),
    ) -> None:
        """Initialize the message."""
        self.id = str(uuid4())
        self.created_at = datetime.now()

        self.to_address = to_address
        self.from_address = from_address
        self.subject = subject
        self.body = body
        self.attachments = Attachments(attachments=attachments)

    def encode(self):
        ...

    def decode(self):
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

    messages: list[Message]

    def __init__(self, messages: list[Message] = []) -> None:
        """Initialize the messages."""
        self.messages = messages

    def add_message(self, message: Message):
        """Add a message to the collection."""
        self.messages.append(message)

    def append(self, message: Message):
        """Alias for add_message."""
        self.add_message(message)

    def __getitem__(self, index: int):
        """Get a message from the collection."""
        return self.messages[index]

    def __len__(self):
        """Get the length of the collection."""
        return len(self.messages)

    def __iter__(self):
        """Iterate over the collection."""
        return iter(self.messages)

    def __str__(self):
        return f"\n\n".join([str(m) for m in self.messages])

    def __repr__(self):
        return str(self)

# exports
from ibis_birdbrain.messages.email import Email

__all__ = ["Message", "Messages", "Email"]