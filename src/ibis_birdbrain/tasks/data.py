# imports
from ibis_birdbrain.tasks import Task

from ibis_birdbrain.messages import Message, Email
from ibis_birdbrain.attachments import Attachments, DataAttachment, TableAttachment

from ibis_birdbrain.ml.functions import filter_tables


# classes
class GetTables(Task):
    """Get tables.

    Choose this task to get tables from a database, returning a message with table attachments. These contain the schema and other useful metadata for transformation queries
    """

    def __init__(self, name: str = "get_tables"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the get tables."""
        table_attachments = Attachments()
        for a in m.attachments:
            a = m.attachments[a]
            if isinstance(a, DataAttachment):
                tables = a.open().list_tables()
                relevant_tables = filter_tables(str(m), options=tables)
                for t in relevant_tables:
                    table_attachments.append(TableAttachment(a.open().table(t)))

        m = Email(body="here are the relevant tables:", attachments=table_attachments)
        return m


class TransformTables(Task):
    """Transform tables.

    Choose this task to transform tables in a database, returning a message with a new table attachment.
    """

    def __init__(self, name: str = "transform_tables"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the transform tables."""
        m = Email(body="Transform tables running.")
        return m
