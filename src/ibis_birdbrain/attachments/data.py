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
class DataAttachment(Attachment):
    """A database attachment."""

    content: BaseBackend

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.con = self.content  # alias
        if self.name is None:
            try:
                self.name = (
                    self.content.current_database + "." + self.content.current_schema
                )
            except:
                self.name = "unknown"

        try:
            self.sql_dialect = self.content.name
        except:
            self.sql_dialect = "unknown"
        try:
            self.description = "tables:\n\t" + "\n\t".join(
                [t for t in self.content.list_tables()]
            )
        except:
            self.description = "empty database\n"

    def __str__(self):
        return (
            super().__str__()
            + f"""
    **dialect**: {self.sql_dialect}"""
        )


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
