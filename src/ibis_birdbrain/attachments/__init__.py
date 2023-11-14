"""
Attachments in Ibis Birdbrain represent arbitrary Python objects
that both a user and a computer can interact with.

They generally consist of metadata + content + optional attributes
based on the type of attachment. They implement an `.open()` method
that does what it should.
"""

# imports
from uuid import uuid4
from typing import Any
from datetime import datetime

from ibis.expr.types.relations import Table


# classes
class Attachment:
    """An attachment."""

    content: Any
    id: str
    created_at: datetime
    name: str | None
    description: str | None

    def __init__(
        self,
        content,
        name=None,
        description=None,
    ):
        self.id = str(uuid4())
        self.created_at = datetime.now()

        self.name = name
        self.description = description
        self.content = content

    def encode(self) -> Table:
        ...

    def decode(self, t: Table) -> str:
        ...

    def open(self) -> Any:
        return self.content

    def __str__(self):
        return f"""{self.__class__.__name__}
    **guid**: {self.id}
    **time**: {self.created_at}
    **name**: {self.name}
    **desc**: {self.description}"""

    def __repr__(self):
        return str(self)


class Attachments:
    """A collection of attachments."""

    attachments: dict[str, Attachment]

    def __init__(self, attachments: list[Attachment] = []) -> None:
        """Initialize the attachments."""
        self.attachments = dict({a.id: a for a in attachments})

    def add_attachment(self, attachment: Attachment):
        """Add an attachment to the collection."""
        self.attachments[attachment.id] = attachment

    def append(self, attachment: Attachment):
        """Alias for add_attachment."""
        self.add_attachment(attachment)

    def __getitem__(self, id: str):
        """Get an attachment from the collection."""
        return self.attachments[id]

    def __setitem__(self, id: str, attachment: Attachment):
        """Set an attachment in the collection."""
        self.attachments[id] = attachment

    def __len__(self):
        """Get the length of the collection."""
        return len(self.attachments.values())

    def __iter__(self):
        """Iterate over the collection."""
        return iter(self.attachments.keys())

    def __str__(self):
        return "\n\n".join([str(a) for a in self.attachments.values()])

    def __repr__(self):
        return str(self)

    def __index__(self, id: str):
        return self.attachments[id]


# exports
from ibis_birdbrain.attachments.viz import ChartAttachment
from ibis_birdbrain.attachments.data import DatabaseAttachment, TableAttachment
from ibis_birdbrain.attachments.text import (
    TextAttachment,
    CodeAttachment,
    WebpageAttachment,
)

__all__ = [
    "Attachment",
    "Attachments",
    "DatabaseAttachment",
    "TableAttachment",
    "ChartAttachment",
    "TextAttachment",
    "CodeAttachment",
    "WebpageAttachment",
]
