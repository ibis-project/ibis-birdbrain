"""
Ibis Birdbrain.

This file represents the main logic, user experience, and user interface.
"""

# imports
import ibis

import logging as log

from uuid import uuid4
from typing import Any
from datetime import datetime

from ibis.backends.base import BaseBackend

from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.subsystems import Subsystems
from ibis_birdbrain.attachments import (
    DataAttachment,
)  # everything starts with data

from ibis_birdbrain.strings import (
    DEFAULT_NAME,
    DEFAULT_USER_NAME,
    DEFAULT_DESCRIPTION,
    DEFAULT_VERSION,
    DEFAULT_SYSTEM_SYSTEM,
)

from ibis_birdbrain.utils.strings import shorten_str
from ibis_birdbrain.utils.messages import to_message

# config
log.basicConfig(level=log.INFO)


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

        # initialize system
        init_message = Email(
            body=f"{DEFAULT_SYSTEM_SYSTEM}",
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

        log.info(f"preprocessing input: {text}")
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
        log.info(f"adding message to messages: {m}")
        self.messages.append(m)

    def system(self, depth: int = 13) -> None:
        """System process."""

        # check if done
        log.info(f"running system...")
        if self.messages.evaluate() or depth == 0:
            log.info(f"returning from system...")
            return

        # if not, run a subsystem
        log.info(f"choosing subsystem...")
        subsystem = self.subsystems.choose(self.messages)
        log.info(f"running subsystem: {subsystem.name}")
        ms = subsystem(self.messages)
        for m in ms:
            # extract message
            m = ms[m]  # TODO: jank?

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
        m = self.messages.respond()

        # set message metadata
        m.to_address = self.user_name
        m.from_address = self.name
        m.subject = f"re: {self.current_subject}"

        # add message to messages
        self.messages.append(m)

    def __str__(self):
        """String the bot."""
        return f"<Bot name={self.name} id={self.id} description={self.description} version={self.version} data={list(self.data.keys())}>"

    def __repr__(self):
        """Represent the bot."""
        return str(self)
