"""
Ibis Birdbrain language user interface (LUI).
"""

# imports
from typing import Any
from copy import deepcopy # TODO: remove

from ibis_birdbrain.tasks import tasks
from ibis_birdbrain.systems import (
    DEFAULT_NAME,
    DEFAULT_INPUT_SYSTEM,
    DEFAULT_OUTPUT_SYSTEM,
)

from ibis_birdbrain.messages import Message, Email
from ibis_birdbrain.attachments import DatabaseAttachment # TODO: this feels hacky to have here
from ibis_birdbrain.ml.functions import generate_response
from ibis_birdbrain.utils.messages import to_message
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
    ) -> None:
        """Initialize the LUI."""
        self.name = name
        self.input_system = input_system
        self.output_system = output_system

    def __call__(
        self, message: Message | str, instructions: str = "", context: str = ""
    ) -> Message:
        ...

    def preprocess(self, text: str, stuff: list[Any], data_con: list[BaseBackend], data_bases: list[str], docs_con: BaseBackend) -> Message:
        """Preprocess input."""""
        m = to_message(text, stuff)
        for data_base in data_bases:
            m.append(DatabaseAttachment(content=data_con, data_base=data_base))
        m.append(DatabaseAttachment(content=docs_con))
        return m

    def system(self, m: Message) -> Message:
        """Process system."""
        body = m.body
        attachments = m.attachments
        attachments = [] # TODO: temp
        r = generate_response(body, instructions=self.input_system)

        # TODO:
        # - filter relevant attachments
        # - decide on tasks
        # - run tasks
        # - process results, construct response message
        return Email(body=r, attachments=attachments)

    def postprocess(self, m: Message) -> Message:
        """Postprocess output."""
        body = m.body
        attachments = m.attachments
        r = generate_response(body, instructions=self.output_system)

        # TODO:
        # - evaluate 

        return Email(body=r, attachments=attachments)

