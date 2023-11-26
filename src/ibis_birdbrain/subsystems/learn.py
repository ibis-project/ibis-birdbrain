# imports
from ibis_birdbrain.tasks import Tasks, SearchDocs, SummarizeDocs, WriteDocs
from ibis_birdbrain.messages import Messages, Email
from ibis_birdbrain.subsystems import Subsystem


# classes
class Learn(Subsystem):
    """Learn."""

    def __init__(
        self,
        name: str = "learn",
        tasks: Tasks = Tasks([SearchDocs(), SummarizeDocs(), WriteDocs()]),
    ):
        super().__init__(name=name, tasks=tasks)

    def __call__(self, ms: Messages) -> Messages:
        """Run the Learn subsystem."""
        m = Email(body="Learn subsystem running.")
        return Messages([m])
