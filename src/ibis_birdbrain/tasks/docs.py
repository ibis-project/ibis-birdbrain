# imports
from ibis_birdbrain.tasks import Task

from ibis_birdbrain.messages import Message, Email
from ibis_birdbrain.attachments import TextAttachment, TableAttachment


# classes
class ReadDocs(Task):
    """Read docs.

    Choose this task to search and read relevant documentation in a database, returning a message with relevant documentation attachments."""

    def __init__(self, name: str = "read_docs"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the read docs."""
        m = Email(body="Read docs running.")
        return m


class SummarizeDocs(Task):
    """Summarize docs.

    Choose this task to summarize documentation in a database, returning a message with text summary attachments."""

    def __init__(self, name: str = "summarize_docs"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the summarize docs."""
        m = Email(body="Summarize docs running.")
        return m


class WriteDocs(Task):
    """Write docs.

    Choose this task to write documentation in the style of other documents attached to the messages,
    returning a message with new documentation attachments."""

    def __init__(self, name: str = "write_docs"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the write docs."""
        m = Email(body="Write docs running.")
        return m
