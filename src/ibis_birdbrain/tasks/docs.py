# imports
from ibis_birdbrain.tasks import Task

from ibis_birdbrain.messages import Message, Email


# classes
class SearchDocs(Task):
    """
    Search docs.
    """

    def __init__(self, name: str = "search_docs"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the search docs."""
        m = Email(body="Search docs running.")
        return m


class SummarizeDocs(Task):
    """
    Summarize docs.
    """

    def __init__(self, name: str = "summarize_docs"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the summarize docs."""
        m = Email(body="Summarize docs running.")
        return m


class WriteDocs(Task):
    """
    Write docs.
    """

    def __init__(self, name: str = "write_docs"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the write docs."""
        m = Email(body="Write docs running.")
        return m
