# imports
import ibis

import plotly.express as px

from uuid import uuid4
from typing import Any
from datetime import datetime

from plotly.graph_objs import Figure
from ibis.backends.base import BaseBackend
from ibis.expr.types.relations import Table

# configure Ibis
ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 10
ibis.options.repr.interactive.max_columns = 20
ibis.options.repr.interactive.max_length = 20


# classes
class Attachment:
    """An attachment."""

    id: str
    created_at: datetime
    name: str
    description: str
    content: Any

    def __init__(
        self,
        id=str(uuid4()),
        created_at=datetime.now(),
        name="attachment",
        description="",
        content=None,
    ):
        self.id = id
        self.created_at = created_at
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
        return f"""
    {self.__class__.__name__}:
        **id**: {self.id}
        **name**: {self.name}
        **created_at**: {self.created_at}
        **description**: {self.description}"""

    def __repr__(self):
        return str(self)

class DatabaseAttachment(Attachment):
    """A database attachment."""

    content: BaseBackend

    def __init__(self, content):
        super().__init__()
        self.content = content
        self.con = content # alias
        self.sql_dialect = content.name

class TextAttachment(Attachment):
    """A text attachment."""

    content: str

    def __init__(self, content):
        super().__init__()
        self.content = content
        if (len(self.content) // 4) > 100:
            self.display_content = self.content[:50] + "..." + self.content[-50:]
        else:
            self.display_content = self.content

    def encode(self):
        ...

    def decode(self):
        ...

    def __str__(self):
        return (
            super().__str__()
            + f"""
        **text**: {self.display_content}"""
        )


class TableAttachment(Attachment):
    """A table attachment."""

    content: Table

    def __init__(self, content):
        super().__init__()
        self.content = content
        self.content = content
        self.name = content.get_name()
        self.description = str(content.schema())

    def encode(self) -> Table:
        ...

    def decode(self, t: Table) -> str:
        ...

    def __str__(self):
        return (
            super().__str__()
            + f"""
        **table**:\n{self.content}"""
        )


class ChartAttachment(Attachment):
    """A chart attachment."""

    content: Figure

    def __init__(self, content):
        super().__init__()
        self.content = content

    def encode(self):
        ...

    def decode(self):
        ...

class Attachments:
    """A collection of attachments."""

    attachments: dict[str, Attachment]

    def __init__(self, attachments: list[Attachment] = []) -> None:
        """Initialize the attachments."""
        self.attachments = attachments

    def add_attachment(self, attachment: Attachment):
        """Add an attachment to the collection."""
        self.attachments.append(attachment)

    def append(self, attachment: Attachment):
        """Alias for add_attachment."""
        self.add_attachment(attachment)

    def __getitem__(self, name: str):
        """Get an attachment from the collection."""
        return self.attachments[str]

    def __len__(self):
        """Get the length of the collection."""
        return len(self.attachments.valeues())

    def __iter__(self):
        """Iterate over the collection."""
        return iter(self.attachments)

    def __str__(self):
        return f"\n".join([str(a) for a in self.attachments])

    def __repr__(self):
        return str(self)
