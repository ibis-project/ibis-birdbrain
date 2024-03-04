# imports
from ibis_birdbrain.messages import Message


# classes
class Email(Message):
    """An email."""

    def __str__(self):
        return f"""To: {self.to_address}
From: {self.from_address}
Subject: {self.subject}
Sent at: {self.created_at}
Message: {self.id}

{self.body}

Attachments:

{self.attachments}\n"""

    def __repr__(self):
        return str(self)
