# imports
from ibis_birdbrain.strings import CODE_SUBSYSTEM

from ibis_birdbrain.tasks import Tasks, SqlCode, PythonCode
from ibis_birdbrain.messages import Messages, Email
from ibis_birdbrain.subsystems import Subsystem


# classes
class Code(Subsystem):
    """
    Code.
    """

    def __init__(
        self,
        name: str = "code",
        tasks: Tasks = Tasks([SqlCode, PythonCode]),
        system: str = CODE_SUBSYSTEM,
    ):
        super().__init__(name=name, tasks=tasks, system=system)

    def __call__(self, ms: Messages) -> Messages:
        """Run the Code subsystem."""
        m = Email(body="Code subsystem running.")
        return Messages([m])
