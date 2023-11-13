"""
Ibis Birdbrain language user interface (LUI).
"""

# imports
from typing import Any

from ibis.backends.base import BaseBackend

from ibis_birdbrain.systems import (
    DEFAULT_NAME,
    DEFAULT_INPUT_SYSTEM,
    DEFAULT_OUTPUT_SYSTEM,
    DEFAULT_SYSTEM_SYSTEM,
)

from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.attachments import (
    DatabaseAttachment,
)  # TODO: this feels hacky to have here, but fairly core to the experience so maybe it's fine?

from ibis_birdbrain.tasks import tasks

from ibis_birdbrain.utils.messages import to_message

from ibis_birdbrain.ml.classifiers import to_ml_classifier
from ibis_birdbrain.ml.functions import (
    generate_response,
    filter_attachments,
)


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
        system_system: str = DEFAULT_SYSTEM_SYSTEM,
    ) -> None:
        """Initialize the LUI."""
        self.name = name
        self.input_system = input_system
        self.output_system = output_system
        self.system_system = system_system

    def __call__(
        self, message: Message | str, instructions: str = "", context: str = ""
    ) -> Message:
        ...

    def preprocess(
        self,
        messages: Messages,
        text: str,
        stuff: list[Any],
        data: dict[str, BaseBackend],
    ) -> Message:
        """Preprocess input."""
        m = to_message(text, stuff)
        if len(messages) == 0:
            for data_con_name, data_con in data.items():
                m.append(DatabaseAttachment(name=data_con_name, content=data_con))
        return m

    def system(self, m: Messages) -> Messages:
        """System process."""
        task = tasks.select(m, m[-1].body)
        attachments = filter_attachments(m)
        attachments = [m.attachments[i] for i in attachments]
        for a in attachments:
            m.attachments[a.id] = a

        system_messages = task(m)
        return system_messages

    def postprocess(self, m: Message) -> Message:
        """Postprocess output."""
        body = m.body
        attachments = m.attachments
        r = generate_response(body, instructions=self.output_system)
        r += f"\n\nSee attached.\n\n-{self.name}"

        # TODO:
        # - evaluate
        # - process results, construct response message
        m = Email(body=r, attachments=attachments)
        return m
