# imports
from ibis_birdbrain.tasks import Tasks, SqlCode, PythonCode
from ibis_birdbrain.messages import Messages, Email
from ibis_birdbrain.subsystems import Subsystem


# classes
class Code(Subsystem):
    """Write code, returning code attachments with the message.

    Choose this subsystem to write code and evaluate."""

    def __init__(
        self,
        name: str = "code",
        tasks: Tasks = Tasks([SqlCode(), PythonCode()]),
    ):
        super().__init__(name=name, tasks=tasks)
