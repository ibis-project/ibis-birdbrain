# imports
from ibis_birdbrain.tasks import Tasks, GetTables, ReadDocs, SummarizeDocs, WriteDocs
from ibis_birdbrain.messages import Messages, Email
from ibis_birdbrain.subsystems import Subsystem


# classes
class Learn(Subsystem):
    """Learn from documentation (in a database) and external sources.

    Note you must get the documentation tables before reading in docs.

    Choose this subsystem to add relevant information to the context of the system via messages and attachments."""

    def __init__(
        self,
        name: str = "learn",
        tasks: Tasks = Tasks([GetTables(), ReadDocs(), SummarizeDocs(), WriteDocs()]),
    ):
        super().__init__(name=name, tasks=tasks)
