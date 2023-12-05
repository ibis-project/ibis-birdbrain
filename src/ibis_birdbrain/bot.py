"""
Ibis Birdbrain.

This file represents the main logic, user experience, and user interface.

Calling the bot will preprocess the message, strategize on the action to take,
run the system, and postprocess the response.
"""

# imports
import ibis

from uuid import uuid4
from typing import Any
from datetime import datetime

from ibis.backends.base import BaseBackend

from ibis_birdbrain.logging import log
from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.subsystems import Subsystems
from ibis_birdbrain.attachments import (
    DataAttachment,
)  # everything starts with data

from ibis_birdbrain.strings import (
    DEFAULT_NAME,
    DEFAULT_VERSION,
    DEFAULT_USER_NAME,
    DEFAULT_DESCRIPTION,
    DEFAULT_SYSTEM_SYSTEM,
    DEFAULT_STRATEGY_SYSTEM,
    DEFAULT_RESPONSE_SYSTEM,
    DEFAULT_MESSAGE_EVALUATION_SYSTEM,
)

from ibis_birdbrain.utils.strings import shorten_str
from ibis_birdbrain.utils.messages import to_message


# classes
class Bot:
    """Ibis Birdbrain bot."""

    id: str
    created_at: datetime

    data: dict[str, BaseBackend]
    subsystems: Subsystems
    messages: Messages
    name: str
    user_name: str
    description: str
    version: str

    current_subject: str

    def __init__(
        self,
        data: dict[str, str] = {
            "system": "duckdb://birdbrain.ddb",
            "memory": "duckdb://",
        },
        subsystems=Subsystems(),
        messages=Messages(),
        name=DEFAULT_NAME,
        user_name=DEFAULT_USER_NAME,
        description=DEFAULT_DESCRIPTION,
        version=DEFAULT_VERSION,
    ) -> None:
        """Initialize the bot."""
        self.id = uuid4()
        self.created_at = datetime.now()

        self.data = {k: ibis.connect(v) for k, v in data.items()}
        self.subsystems = subsystems
        self.messages = messages
        self.m = messages  # alias
        self.name = name
        self.user_name = user_name
        self.description = description
        self.version = version

        self.current_subject = ""

        # get source code
        source_code = open(__file__, "r").read()

        # initialize system
        init_message = Email(
            body=f"{DEFAULT_SYSTEM_SYSTEM}\nYour source code is:\n{source_code}",
            subject="system init",
            to_address=self.name,
            from_address=self.name,
            attachments=[
                DataAttachment(
                    self.data[x],
                )
                for x in self.data
            ],
        )
        self.messages.append(init_message)

    def __call__(
        self,
        text: str = "Who are you and what can you do?",
        stuff: list[Any] = [],
    ) -> Message:
        """Call upon the bot."""

        # process input
        self.preprocess(
            text=text,
            stuff=stuff,
        )

        # strategize
        self.strategize()

        # process system
        self.system()

        # process output
        self.postprocess()

        return self.messages[-1]

    def preprocess(
        self,
        text: str = "",
        stuff: list[Any] = [],
    ) -> None:
        """Preprocess input."""

        log.info(f"preprocessing input...")
        # TODO: update subject dynamically
        if self.current_subject == "":
            self.current_subject = shorten_str(text)

        # convert user input to message
        m = to_message(text, stuff)

        # set message metadata
        m.to_address = self.name
        m.from_address = self.user_name
        m.subject = self.current_subject

        # add message to messages
        self.messages.append(m)

    def strategize(self) -> None:
        """Strategize on the subsystems and tasks to run prior to executing the system."""

        log.info(f"strategizing...")
        m = self.messages.respond(
            instructions=f"""{DEFAULT_STRATEGY_SYSTEM}\nYou have access to: {self.subsystems}"""
        )
        breakpoint()

        # set message metadata
        m.to_address = self.name
        m.from_address = self.name
        m.subject = f"[system strategy] re: {self.current_subject}"

        # add message to messages
        self.messages.append(m)

    def system(self, depth: int = 3) -> None:
        """System process."""

        # check if done
        log.info(f"running system...")
        log.info(f"depth: {depth}")
        if self.messages.evaluate(instructions=DEFAULT_MESSAGE_EVALUATION_SYSTEM):
            log.info(f"evaluated as complete...")
            return
        if depth == 0:
            log.info(f"max depth reached...")
            return

        # if not, run a subsystem
        log.info(f"choosing subsystem...")
        subsystem = self.subsystems.choose(self.messages)
        log.info(f"running subsystem: {subsystem.name}")
        ms = subsystem(self.messages)
        for m in ms:
            # extract message # TODO: jank?
            m = ms[m]

            # set message metadata
            m.to_address = self.name
            m.from_address = self.name
            m.subject = f"[subsystem: {subsystem.name}] re: {self.current_subject}"

            # add message to messages
            self.messages.append(m)

        # recursion
        return self.system(depth=depth - 1)

    def postprocess(self) -> None:
        """Postprocess output."""

        # generate response
        m = self.messages.respond(instructions=DEFAULT_RESPONSE_SYSTEM)

        # set message metadata
        m.to_address = self.user_name
        m.from_address = self.name
        m.subject = f"re: {self.current_subject}"

        # filter relevant attachments
        m.attachments = self.messages.relevant_attachments(m)

        # add message to messages
        self.messages.append(m)

    def __str__(self):
        """String the bot."""
        return f"<Bot name={self.name} id={self.id} description={self.description} version={self.version} subsystems={list(self.subsystems)} data={list(self.data.keys())}>"

    def __repr__(self):
        """Represent the bot."""
        return str(self)
