# imports
from typing import Any
from ibis_birdbrain.messages import Message, Email

from ibis_birdbrain.utils.attachments import to_attachment


# functions
def to_message(text: str, stuff: list[Any] = []) -> Message:
    """Convert text and stuff into a message with attachments."""
    attachments = []
    for thing in stuff:
        attachment = to_attachment(thing)
        if attachment is not None:
            attachments.append(attachment)

    return Email(body=text, attachments=attachments)
