"""
Ibis Birdbrain.

This file represents the main logic, user experience, and user interface.
"""

# imports
import ibis

from uuid import uuid4
from typing import Any
from datetime import datetime

from ibis.backends.base import BaseBackend

from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.attachments import (
    Attachments,
    DataAttachment,
)  # everything starts with data

from ibis_birdbrain.ml.classifiers import to_ml_classifier
from ibis_birdbrain.ml.functions import (
    filter_attachments,
    generate_response,
)

from ibis_birdbrain.tasks import Tasks, tasks

from ibis_birdbrain.systems import (
    DEFAULT_NAME,
    DEFAULT_USER_NAME,
    DEFAULT_DESCRIPTION,
    DEFAULT_VERSION,
    DEFAULT_INPUT_SYSTEM,
    DEFAULT_SYSTEM_SYSTEM,
    DEFAULT_OUTPUT_SYSTEM,
)

from ibis_birdbrain.utils.strings import shorten_str
from ibis_birdbrain.utils.messages import to_message


# classes
class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime

    data: dict[str, BaseBackend]
    tasks: Tasks
    messages: Messages
    sys_messages = list[Messages]
    name: str
    user_name: str
    description: str
    version: str

    def __init__(
        self,
        data: dict[str, str] = {
            "system": "duckdb://birdbrain.ddb",
            "memory": "duckdb://",
        },
        tasks=tasks,
        messages=Messages(),
        sys_messages=[],
        name=DEFAULT_NAME,
        user_name=DEFAULT_USER_NAME,
        description=DEFAULT_DESCRIPTION,
        version=DEFAULT_VERSION,
    ) -> None:
        """Initialize the bot."""
        self.id = uuid4()
        self.created_at = datetime.now()

        self.data = {k: ibis.connect(v) for k, v in data.items()}
        self.tasks = tasks
        self.messages = messages
        self.sys_messages = sys_messages
        self.m = messages  # alias
        self.name = name
        self.user_name = user_name
        self.description = description
        self.version = version

        for data_con_name, data_con in self.data.items():
            self.m.attachments.append(
                DataAttachment(name=data_con_name, content=data_con)
            )

        self.attachments = self.m.attachments  # alias

    def __call__(
        self,
        text: str,
        stuff: list[Any] = [],
    ) -> Message:
        """Call upon the bot."""

        # process input
        self.preprocess(
            text,
            stuff=stuff,
        )

        # process system
        self.system()

        # process output
        self.postprocess()

        return self.messages[-1]

    def preprocess(
        self,
        text: str,
        stuff: list[Any] = [],
    ) -> None:
        """Preprocess input."""

        # convert user input to message
        m = to_message(text, stuff)

        # add relevant attachments
        if len(self.messages) == 0:
            m.attachments = Attachments([self.attachments[a] for a in self.attachments])
        else:
            attachments = filter_attachments(
                self.messages[-11]
            )  # TODO: picked a random number here
            attachments = Attachments(
                [self.messages.attachments[i] for i in attachments]
            )
            m.attachments = attachments

        # set message metadata
        m.to_address = self.name
        m.from_address = self.user_name
        m.subject = shorten_str(text)

        # add message to messages
        self.messages.append(m)

    def system(self) -> None:
        """System process."""

        # select a task
        task = tasks.select(self.messages, self.messages[-1].body)

        # filter relevant attachments
        attachments = filter_attachments(self.messages[-1])
        attachments = Attachments([self.messages.attachments[i] for i in attachments])

        # construct message
        m = Email(body=f"task: {task}", attachments=attachments)

        # append message to messages
        self.messages.append(m)

        # run task and get resulting message
        m, sys_messages = task(m)

        # add message to messages
        self.messages.append(m)

        # add sys messages to sys messages
        self.sys_messages.append(sys_messages)

    def postprocess(self) -> None:
        """Postprocess output."""

        # generate response
        r = "Done."
        # r = generate_response(self.messages, instructions=self.output_system)
        r += f"\n\nSee attached.\n\n-{self.name}"

        # construct message
        m = Email(body=r, attachments=self.messages[-1].attachments)

        # set message metadata
        m.to_address = self.user_name
        m.from_address = self.name

        # add message to messages
        self.messages.append(m)

    def attachment(self, text: str):
        """Get an attachment from the message."""
        attachment_options = list(self.m.attachments)
        attachment_classifier = to_ml_classifier(
            attachment_options,
            instructions=f"Choose an attachment from context {self.attachments if (len(self.messages) == 0) else self.messages} based on the request",
        )
        attachment = attachment_classifier(text).value
        return self.m.attachments[attachment]

    def a(self, text: str):
        """Alias for attachment."""
        return self.attachment(text)

    def clear(self):
        """Clear the messages."""
        self.messages.clear()

    def __repr__(self):
        """Represent the bot."""
        return f"<Bot name={self.name} id={self.id} description={self.description} version={self.version} data={list(self.data.keys())}>"
