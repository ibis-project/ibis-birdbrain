# imports
from uuid import uuid4
from typing import Callable
from datetime import datetime

from ibis_birdbrain.attachments import Attachment

# classes
class Task:
    """A task resulting in an attachment."""

    id: str = str(uuid4())
    created_at: datetime = datetime.now()

    # a task has...
    run: Callable
    result: Attachment

    def __init__(self, run = print):
        self.run = run

    def encode(self):
        ...

    def decode(self):
        ...

    def __call__(self, *args, **kwargs):
        self.result =  Attachment(content=self.run(*args, **kwargs))
        return self.result