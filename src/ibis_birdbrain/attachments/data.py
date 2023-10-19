# imports
import ibis

from ibis.backends.base import BaseBackend
from ibis.expr.types.relations import Table

from ibis_birdbrain.attachments import Attachment

# configure Ibis
ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 10
ibis.options.repr.interactive.max_columns = 20
ibis.options.repr.interactive.max_length = 20

# classes
class DatabaseAttachment(Attachment):
    """A database attachment."""

    content: BaseBackend

    def __init__(self, content):
        super().__init__()
        self.content = content
        self.con = content # alias
        self.sql_dialect = content.name

class TableAttachment(Attachment):
    """A table attachment."""

    content: Table

    def __init__(self, content):
        super().__init__()
        self.content = content
        self.content = content
        self.name = content.get_name()
        self.description = "\n"+str(content.schema())

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
