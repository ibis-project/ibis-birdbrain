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

    def __init__(self, data_base=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.con = self.content  # alias
        if data_base is None:
            data_base = self.con.current_database
        self.data_base = data_base
        try:
            self.sql_dialect = self.content.name
        except:
            self.sql_dialect = "unknown"
        try:
            self.name = (
                self.data_base + "." + self.content.current_schema
            )
        except:
            self.name = "unknown.main"
        try:
            self.description = "tables:\n\t" + "\n\t".join(
                [t for t in self.content.list_tables(database=data_base)]
            )
        except:
            self.description = "tables:\n\t"


class TableAttachment(Attachment):
    """A table attachment."""

    content: Table

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.name = self.content.get_name()
        except AttributeError:
            self.name = None
        self.schema = self.content.schema()
        self.description = "\n" + str(self.schema)

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
