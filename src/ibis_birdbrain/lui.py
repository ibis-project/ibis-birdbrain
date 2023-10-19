"""
Ibis Birdbrain language user interface (LUI).
"""

# imports
from ibis_birdbrain.ml.classifiers import TaskType
from ibis_birdbrain.messages import Message, Messages

DEFAULT_INPUT_SYSTEM = "write a response email"
DEFAULT_OUTPUT_SYSTEM = "write a response email"


# classes
class Lui:
    input_system: str
    output_system: str

    def __init__(
        self,
        input_system: str = DEFAULT_INPUT_SYSTEM,
        output_system: str = DEFAULT_OUTPUT_SYSTEM,
    ) -> None:
        ...

    def __call__(self, message: Message) -> Message:
        ...

    def assign_tasks(self, messages: Messages) -> list[Message]:
        ...
