# imports
from ibis_birdbrain.messages import Message


# classes
class Task:
    """Ibis Birdbrain task."""

    name: str | None
    description: str | None

    def __init__(
        self,
        name=None,
        description=None,
    ):
        self.name = name
        self.description = description

    def __call__(self, m: Message) -> Message:
        raise NotImplementedError


class Tasks:
    """Ibis Birdbrain tasks."""

    tasks: dict[str, Task]

    def __init__(self, tasks: list[Task] = []) -> None:
        """Initialize the flows."""
        self.tasks = {t.name: t for t in tasks}

    def __getitem__(self, id: str | int) -> Task:
        """Get a task by its name, index, or a text description."""
        if id in self.tasks.keys():
            return self.tasks[id]
        elif id in range(len(self.tasks)):
            return self.tasks[list(self.tasks.keys())[id]]
        else:
            # TODO: implement LM magic
            raise KeyError

    def select_task(self, ms: Message, instructions: str) -> Task:
        """Select a single task."""
        raise NotImplementedError


# exports
__all__ = [
    "Task",
    "Tasks",
]
