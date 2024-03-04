# imports
from typing import Any

from plotly.graph_objs import Figure

from ibis.expr.types import Table
from ibis.backends.base import BaseBackend

from ibis_birdbrain.attachments import (
    Attachment,
    TextAttachment,
    DataAttachment,
    TableAttachment,
    ChartAttachment,
    WebpageAttachment,
)


# functions
def to_attachment(thing: Any) -> Attachment | None:
    """Converts a thing to an attachment."""
    if isinstance(thing, Attachment):
        return thing
    elif isinstance(thing, str):
        if thing.startswith("http"):
            return WebpageAttachment(thing)
        else:
            return TextAttachment(thing)
    elif isinstance(thing, BaseBackend):
        return DataAttachment(thing)
    elif isinstance(thing, Table):
        return TableAttachment(thing)
    elif isinstance(thing, Figure):
        return ChartAttachment(thing)

    return None


def to_attachments(things: list[Any]) -> list[Attachment]:
    """Converts a list of things to a list of attachments."""
    return [
        to_attachment(thing) for thing in things if to_attachment(thing) is not None
    ]
