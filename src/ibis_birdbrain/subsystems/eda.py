# imports
from ibis_birdbrain.tasks import Tasks, SqlCode, TransformTables
from ibis_birdbrain.messages import Messages, Email
from ibis_birdbrain.subsystems import Subsystem


# classes
class EDA(Subsystem):
    """
    Exploratory data analysis.
    """

    def __init__(
        self,
        name: str = "eda",
        tasks: Tasks = Tasks([SqlCode, TransformTables]),
        system: str = "eda",
    ):
        super().__init__(name=name, tasks=tasks, system=system)

    def __call__(self, ms: Messages) -> Messages:
        """Run the EDA subsystem."""
        m = Email(body="EDA subsystem running.")
        return Messages([m])
