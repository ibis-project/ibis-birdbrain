# imports
from uuid import uuid4
from typing import Callable
from datetime import datetime

from ibis_birdbrain.attachments import Attachment


# classes
class Task:
    """A task resulting in an attachment."""

    id: str
    created_at: datetime

    # a task has...
    run: Callable
    result: Attachment

    def __init__(self, run=print):
        """Initialize the task."""
        self.id = str(uuid4())
        self.created_at = datetime.now()

        self.run = run

    def encode(self):
        ...

    def decode(self):
        ...

    def __call__(self, *args, **kwargs):
        self.result = Attachment(content=self.run(*args, **kwargs))

        return self.result

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"


class Tasks:
    """A collection of tasks."""

    tasks: dict[str, Task]

    def __init__(self, tasks: list[Task] = []) -> None:
        """Initialize the tasks."""
        self.temp = tasks
        self.tasks = dict({t.id: t for t in tasks})
