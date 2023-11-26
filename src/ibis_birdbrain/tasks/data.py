# imports
from ibis_birdbrain.tasks import Task

from ibis_birdbrain.messages import Message, Email


# classes
class TransformTables(Task):
    """Transform tables.

    Choose this task to transform tables in a database, returning a message with a new table attachment."""

    def __init__(self, name: str = "transform_tables"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the transform tables."""
        m = Email(body="Transform tables running.")
        return m
