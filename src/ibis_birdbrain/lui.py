"""
Ibis Birdbrain language user interface (LUI).
"""

# imports
from ibis_birdbrain.tasks import tasks
from ibis_birdbrain.systems import (
    DEFAULT_NAME,
    DEFAULT_INPUT_SYSTEM,
    DEFAULT_OUTPUT_SYSTEM,
)

from ibis_birdbrain.messages import Message, Email
from ibis_birdbrain.ml.functions import generate_response
from ibis_birdbrain.ml.classifiers import TaskType
from ibis_birdbrain.utils.attachments import to_attachment


# classes
class Lui:
    """Language user interface (LUI)."""

    input_system: str
    output_system: str

    def __init__(
        self,
        name: str = DEFAULT_NAME,
        input_system: str = DEFAULT_INPUT_SYSTEM,
        output_system: str = DEFAULT_OUTPUT_SYSTEM,
    ) -> None:
        """Initialize the LUI."""
        self.name = name
        self.input_system = input_system
        self.output_system = output_system

    def __call__(
        self, message: Message | str, instructions: str = "", context: str = ""
    ) -> Message:
        """Language user interface logic."""

        # TODO: require message (via bot)
        if isinstance(message, str):
            message = Email(
                body=message,
            )
        r = generate_response(
            message, instructions=self.input_system, additional_context=context
        )
        r = Email(body=r, to_address=self.name, from_address=self.name)
        return r

    def preprocess(self, message: Message) -> Message:
        ...

    def system(self, message: Message) -> Message:
        ...

    def postprocess(self, message: Message) -> Message:
        ...
