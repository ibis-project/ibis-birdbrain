"""
Subsystems in Ibis Birdbrain...
"""

# imports
from ibis_birdbrain.logging import log

from ibis_birdbrain.tasks import Tasks
from ibis_birdbrain.messages import Messages, Email

from ibis_birdbrain.ml.models import RelevantMessageExtractor
from ibis_birdbrain.ml.classifiers import to_ml_classifier


# classes
class Subsystem:
    """Ibis Birdbrain subsystem."""

    name: str
    tasks: Tasks
    description: str

    def __init__(self, name: str, tasks: Tasks) -> None:
        self.name = name
        self.tasks = tasks
        self.description = f"{self.__doc__}\ntasks:\n{tasks}"

    def __call__(
        self, ms: Messages, rs: Messages = Messages(), max_depth: int = 1
    ) -> Messages:
        """Run the subsystem."""

        for i in range(max_depth):
            # check if done
            if i != 0 and ms.evaluate():
                return rs

            # run the tasks
            log.info(f"choosing task...")
            task = self.tasks.choose(ms)
            log.info(f"running task: {task.name}")

            temp = "You are to extract relevant messages and attachments from:\n"
            temp += str(ms)
            temp += f"\nto perform the task {task}. Write a message for the task with all relevant details."

            # construct task message
            # TODO: this needs to be LLM-generated; filter relevant messages, write a message
            m = Email(body=f"run {task.name} with attachments:")

            # filter relevant attachments
            a = ms.relevant_attachments(m)
            m.attachments = a

            # add message to messages
            rs.append(m)

            # run the task
            res = task(m)
            rs.append(res)

        return rs

    def __str__(self):
        return f"name: {self.name}\ndescription: {self.description}\n"

    def __repr__(self):
        return str(self)


class Subsystems:
    """A collection of subsystems."""

    subsystems: dict[str, Subsystem]

    def __init__(self, subsystems: list[Subsystem] = []) -> None:
        """Initialize the subsystems."""
        self.subsystems = {s.name: s for s in subsystems}

    def __call__(self, ms: Messages) -> Messages:
        """Run the subsystems."""
        return self.choose(ms)(ms)

    def choose(self, ms: Messages) -> Subsystem:
        """Choose the matching subsystem."""
        subsystem_options = list(self.subsystems)
        subsystem_classifier = to_ml_classifier(
            subsystem_options, f"Choose a subsystem from {self}"
        )
        subsystem = subsystem_classifier(str(ms)).value
        log.info(f"chose subsystem: {subsystem}")
        return self.subsystems[subsystem]

    def add_subsystem(self, subsystem: Subsystem):
        """Add a subsystem to the collection."""
        self.subsystems[subsystem.name] = subsystem

    def append(self, subsystem: Subsystem):
        """Add a subsystem to the collection."""
        self.add_subsystem(subsystem)

    def __getitem__(self, id: str | int) -> Subsystem:
        """Get a subsystem from the collection."""
        if isinstance(id, int):
            return list(self.subsystems.values())[id]
        return self.subsystems[id]

    def __setitem__(self, name: str, subsystem: Subsystem) -> None:
        """Set a subsystem in the collection."""
        self.subsystems[name] = subsystem

    def __len__(self) -> int:
        """Get the length of the collection."""
        return len(self.subsystems)

    def __iter__(self):
        """Iterate over the collection."""
        return iter(self.subsystems.keys())

    def __str__(self):
        return "---\n".join([str(s) for s in self.subsystems.values()])

    def __repr__(self):
        return str(self)


# exports
from ibis_birdbrain.subsystems.eda import EDA
from ibis_birdbrain.subsystems.code import Code
from ibis_birdbrain.subsystems.docs import Docs

__all__ = ["Subsystem", "Subsystems", "EDA", "Code", "Docs"]
