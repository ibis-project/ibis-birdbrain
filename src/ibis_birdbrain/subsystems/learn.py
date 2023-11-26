# imports
from ibis_birdbrain.tasks import Tasks, ReadDocs, SummarizeDocs, WriteDocs
from ibis_birdbrain.messages import Messages, Email
from ibis_birdbrain.subsystems import Subsystem


# classes
class Learn(Subsystem):
    """Learn from documentation (in a database) and external sources.

    Choose this subsystem to add relevant information to the context of the system via messages and attachments."""

    def __init__(
        self,
        name: str = "learn",
        tasks: Tasks = Tasks([ReadDocs(), SummarizeDocs(), WriteDocs()]),
    ):
        super().__init__(name=name, tasks=tasks)

    def __call__(self, ms: Messages) -> Messages:
        """Run the Learn subsystem."""
        m = Email(body="Learn subsystem running.")
        return Messages([m])
