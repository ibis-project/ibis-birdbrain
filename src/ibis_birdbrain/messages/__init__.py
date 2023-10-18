# imports
from uuid import uuid4
from datetime import datetime

from ibis_birdbrain.attachments import Attachment


# classes
class Message:
    """A message."""

    id: str = str(uuid4())
    created_at: datetime = datetime.now()

    # like an email, it has...
    to_address: list[str]
    from_address: str
    subject: str
    body: str
    attachments: list[Attachment]

    def __init__(self,
        to_address: list[str] = [],
        from_address: str = "",
        subject: str = "",
        body: str = "",
        attachments: list[Attachment] = [],
    ) -> None:
        """Initialize the message."""
        self.to_address = to_address
        self.from_address = from_address
        self.subject = subject
        self.body = body
        self.attachments = attachments

    def encode(self):
        ...

    def decode(self):
        ...
    
    def __str__(self):
        return f"Message({self.id})"

    def __repr__(self):
        return str(self)

class Email(Message):
    """An email."""

    def add_attachment(self, attachment: Attachment):
        """Add an attachment to the email."""
        self.attachments.append(attachment)

    def __str__(self):
        return f"""
From: {self.from_address}
To: {self.to_address}
Subject: {self.subject}

{self.body}

Attachments: {self.attachments}\n---"""