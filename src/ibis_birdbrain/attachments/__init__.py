# imports
import ibis

import plotly.express as px

from uuid import uuid4
from typing import Any
from datetime import datetime

from plotly.graph_objs import Figure
from ibis.expr.types.relations import Table

# configure Ibis
ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 10
ibis.options.repr.interactive.max_columns = 20
ibis.options.repr.interactive.max_length = 20

# classes
class Attachment:
    """An attachment."""

    id: str = str(uuid4())
    created_at: datetime = datetime.now()

    # an attachment has...
    name: str
    description: str

    # and...
    content: Any

    def __init__(self, name="attachment", description="", content=None):
        self.name = name
        self.description = description
        self.content = content


    def encode(self) -> Table:
        ...

    def decode(self, t: Table) -> str:
        ...

    def __str__(self):
        return f"""Attachment:
    **id**: {self.id}
    **created_at**: {self.created_at}
    **name**: {self.name}
    **description**: {self.description}"""

    def __repr__(self):
        return str(self)


class StringAttachment(Attachment):
    """A string attachment."""

    content: str

    def __init__(self, content):
        super().__init__()
        self.content = content

        if len(self.content // 4) > 100:
            self.display_content = self.content[:50] + "..." + self.content[-50:]
        else:
            self.display_content = self.content

    def encode(self):
        ...

    def decode(self):
        ...

    def __str__(self):
        return super().__str__() + f"""
    **string**: {self.display_content}"""

class TableAttachment(Attachment):
    """A table attachment."""

    content: Table

    def __init__(self, content):
        super().__init__()
        self.content = content

    def encode(self) -> Table:
        ...

    def decode(self, t: Table) -> str:
        ...

    def __str__(self):
        return super().__str__() + f"""
    **table**:\n{self.content}"""


class ChartAttachment(Attachment):
    """A chart attachment."""

    content: Figure

    def __init__(self, content)):
        super().__init__()
        self.content = content

    def encode(self):
        ...

    def decode(self):
        ...
