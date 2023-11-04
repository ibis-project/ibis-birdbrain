"""
Ibis Birdbrain language user interface (LUI).
"""

# imports
from typing import Any

from ibis_birdbrain.systems import (
    DEFAULT_NAME,
    DEFAULT_INPUT_SYSTEM,
    DEFAULT_OUTPUT_SYSTEM,
    DEFAULT_SYSTEM_SYSTEM,
)

from ibis_birdbrain.messages import Message, Email
from ibis_birdbrain.attachments import (
    DatabaseAttachment,
)  # TODO: this feels hacky to have here, but fairly core to the experience so maybe it's fine?

from ibis_birdbrain.utils.messages import to_message

from ibis_birdbrain.tasks import tasks

from ibis_birdbrain.ml.functions import (
    generate_response,
    filter_attachments,
    choose_task,
)
from ibis_birdbrain.ml.classifiers import TaskType

from ibis.backends.base import BaseBackend


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
        text: str,
        stuff: list[Any],
        data_con: list[BaseBackend],
        data_bases: list[str],
        docs_con: BaseBackend,
    ) -> Message:
        """Preprocess input.""" ""
        m = to_message(text, stuff)
        for data_base in data_bases:
            m.append(DatabaseAttachment(content=data_con, data_base=data_base))
        m.append(DatabaseAttachment(content=docs_con))
        return m

    def postprocess(self, m: Message) -> Message:
        """Postprocess output."""
        body = m.body
        attachments = m.attachments
        r = generate_response(body, instructions=self.output_system)
        r += f"\n\nSee attached.\n\n-{self.name}"

        # TODO:
        # - evaluate
        # - process results, construct response message
        return Email(body=r, attachments=attachments)

    def system(self, m: Message) -> Message:
        """System process."""
        body = m.body
        task_type = TaskType(body)
        task = choose_task(tasks, task_type=task_type.value)
        attachments = filter_attachments(m, task_type=task_type.value)
        attachments = [m.attachments[i] for i in attachments]
        task_message = generate_response(
            body,
            instructions=self.input_system,
        )
        task_message = Email(
            body=task_message,
            to_address=self.name,
            from_address=self.name,
            attachments=attachments,
        )
        task_result = tasks.tasks[task](task_message)
        return task_result
