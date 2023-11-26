# imports
from ibis_birdbrain.tasks import Tasks, SqlCode, TransformTables
from ibis_birdbrain.messages import Messages, Email
from ibis_birdbrain.subsystems import Subsystem


# classes
class EDA(Subsystem):
    """Exploratory data analysis.

    Choose this subsystem to explore data on behalf of the user like
    a data engineer or data scientist would. Generally, writes SQL
    code and executes it with Ibis, returning messages with code, data,
    visualization, and related attachments.
    """

    def __init__(
        self,
        name: str = "eda",
        tasks: Tasks = Tasks([SqlCode(), TransformTables()]),
    ):
        super().__init__(name=name, tasks=tasks)

    def __call__(self, ms: Messages) -> Messages:
        """Run the EDA subsystem."""
        m = Email(body="EDA subsystem running.")
        return Messages([m])
