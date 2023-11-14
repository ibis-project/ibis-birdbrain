"""
Messages in Ibis Birdbrain are how humans and computers communicate with each other
effectively and efficiently. Messages are metadata + text + attachments, where
attachments are arbitrary Python objects allowing for interaction with data,
code, visualization, and other useful objects.
"""

# imports
from uuid import uuid4
from datetime import datetime

from ibis_birdbrain.attachments import Attachment, Attachments
from ibis_birdbrain.ml.classifiers import to_ml_classifier


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

    def attachment(self, text: str):
        """Get an attachment from the message."""
        attachment_options = list(self.attachments)
        attachment_classifier = to_ml_classifier(
            attachment_options,
            instructions=f"Choose an attachment from context {self} based on the request of {text}",
        )
        attachment = attachment_classifier(text).value
        return self.attachments[attachment]

    def a(self, text: str):
        """Alias for attachment."""
        return self.attachment(text)


class Messages:
    """A collection of messages."""

    messages: list[Message]
    attachments: Attachments

    def __init__(
        self, messages: list[Message] = [], attachments: list[Attachment] = []
    ) -> None:
        """Initialize the messages."""
        self.messages = messages
        self.attachments = Attachments(attachments=attachments)

    def add_message(self, message: Message):
        """Add a message to the collection."""
        for a in message.attachments:
            if a not in self.attachments:
                self.attachments[a] = message.attachments[a]
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

    # TODO: are these actually needed, especially the last one
    def all_attachment_guids(self) -> list[str]:
        """Get all attachments."""
        return list(set([a for m in self.messages for a in list(m.attachments)]))

    def all_message_guids(self) -> list[str]:
        """Get all messages."""
        return list(set([m.id for m in self.messages]))

    def all_attachments(self) -> list[Attachment]:
        """Get all attachments."""
        attachments = Attachments()
        for a in self.all_attachment_guids():
            attachments[a] = self.attachments[a]

    def attachment(self, text: str):
        """Get an attachment from the message."""
        attachment_options = list(self.attachments)
        attachment_classifier = to_ml_classifier(
            attachment_options,
            instructions=f"Choose an attachment from context {self} based on the request of {text}",
        )
        attachment = attachment_classifier(text).value
        return self.attachments[attachment]

    def a(self, text: str):
        """Alias for attachment."""
        return self.attachment(text)


# exports
from ibis_birdbrain.messages.email import Email

__all__ = ["Message", "Messages", "Email"]
