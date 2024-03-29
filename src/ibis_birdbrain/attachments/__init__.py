# imports
from collections import defaultdict
from uuid import uuid4
from typing import Any, Union, List, Type
from datetime import datetime

from ibis.expr.types.relations import Table


# classes
class Attachment:
    """Ibis Birdbrain attachment."""

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
    """Ibis Birdbrain attachments."""

    attachments: dict[str, Attachment]
    type_id_map: dict[Type[Attachment], List[str]]

    def __init__(self, attachments: list[Attachment] = []) -> None:
        """Initialize the attachments."""
        self.attachments = {a.id: a for a in attachments}
        self.type_id_map = defaultdict(list)
        for a in attachments:
            self.type_id_map[type(a)].append(a.id)


    def add_attachment(self, attachment: Attachment):
        """Add an attachment to the collection."""
        self.attachments[attachment.id] = attachment
        self.type_id_map[type(attachment)].append(attachment.id)

    def append(self, attachment: Attachment):
        """Alias for add_attachment."""
        self.add_attachment(attachment)

    def extend(self, attachments: Union[List[Attachment], "Attachments"]):
        """Adds multiple attachments to the collection."""
        if isinstance(attachments, Attachments):
            attachments = list(attachments.attachments.values())
        for attachment in attachments:
            self.add_attachment(attachment)

        return self

    def get_attachment_by_type(self, attachment_type: Type[Attachment]):
        """Get attachments of a specific type."""
        if attachment_type not in self.type_id_map:
            return None

        ids = self.type_id_map[attachment_type]
        if not isinstance(self.attachments[ids[0]], TableAttachment):
            return self.attachments[ids[0]]

        # One messages may have multiple table attachment
        attachments = Attachments()
        for id in ids:
            attachments.append(self.attachments[id])
        return attachments

    def __getitem__(self, id: str | int):
        """Get an attachment from the collection."""
        if isinstance(id, int):
            return list(self.attachments.values())[id]
        return self.attachments[id]

    def __setitem__(self, id: str, attachment: Attachment):
        """Set an attachment in the collection."""
        self.attachments[id] = attachment
        self.type_id_map[type(attachment)].append(id)

    def __len__(self) -> int:
        """Get the length of the collection."""
        return len(self.attachments)

    def __iter__(self):
        """Iterate over the collection."""
        return iter(self.attachments.keys())

    def __str__(self):
        return "\n\n".join([str(a) for a in self.attachments.values()])

    def __repr__(self):
        return str(self)


# exports
from ibis_birdbrain.attachments.viz import ChartAttachment
from ibis_birdbrain.attachments.data import (
    DataAttachment,
    DatabaseAttachment,
    TableAttachment,
)
from ibis_birdbrain.attachments.text import (
    TextAttachment,
    SQLAttachment,
    ErrorAttachment,
    WebpageAttachment,
)

__all__ = [
    "Attachment",
    "Attachments",
    "DataAttachment",
    "DatabaseAttachment",
    "TableAttachment",
    "ChartAttachment",
    "TextAttachment",
    "SQLAttachment",
    "ErrorAttachment",
    "WebpageAttachment",
]
