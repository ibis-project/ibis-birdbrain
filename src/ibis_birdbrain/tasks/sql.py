# imports
from ibis_birdbrain.tasks import Task

from ibis_birdbrain.messages import Messages, Message, Email


# classes
class SqlCode(Task):
    """SQL code.

    Write SQL code, returning code attachments with the message."""

    def __init__(self, name: str = "write_sql_code"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the SQL code."""
        m = Email(body="Sql code running.")
        return m
