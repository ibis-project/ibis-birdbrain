# imports
from typing import Any
from ibis_birdbrain.messages import Message
from ibis_birdbrain.attachments import Attachment
from ibis_birdbrain.ml.classifiers import to_ml_classifier


# tasks
def open_attachment(m: Message) -> Any:
    """Open attachment"""
    attachment_guids = list(m.attachments)

    attachment_picker = to_ml_classifier(attachment_guids, docstring=f"Pick the relevant attachment from {m}")

    attachment = attachment_picker(str(m)).value

    return m.attachments[attachment].open()
