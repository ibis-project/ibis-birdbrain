# imports
from typing import Any
from ibis_birdbrain.attachments import Attachment


# tasks
def open_attachments(attachments: list[Attachment]) -> list[Any]:
    """Open attachments"""
    results = []
    for attachment in attachments:
        results.append(attachment.open())

    return results
