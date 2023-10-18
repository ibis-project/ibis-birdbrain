# imports
from uuid import uuid4
from typing import Callable
from datetime import datetime

from ibis_birdbrain.attachments import Attachment

# classes
class Task:
    """A task performed by the bot."""

    id: str = str(uuid4())
    created_at: datetime = datetime.now()

    # a task has...
    run: Callable
    results: list[Attachment]

    def __init__(self):
        ...

    def encode(self):
        ...

    def decode(self):
        ...