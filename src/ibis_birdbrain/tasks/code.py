# imports
from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.attachments import (
    CodeAttachment,
)
from ibis_birdbrain.ml.functions import generate_code


# tasks
def write_code(m: Message) -> Message:
    """Not implemented"""
    ...
