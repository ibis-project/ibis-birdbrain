# imports
from typing import Any

from plotly.graph_objs import Figure
from ibis.backends.base import BaseBackend
from ibis.expr.types import Table

from ibis_birdbrain.attachments import (
    Attachment,
    TextAttachment,
    DatabaseAttachment,
    TableAttachment,
    ChartAttachment,
    WebpageAttachment,
)

from ibis_birdbrain.utils.web import search_internet, open_browser, webpage_to_str
from ibis_birdbrain.utils.strings import str_to_list_of_str


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
        return DatabaseAttachment(thing)
    elif isinstance(thing, Table):
        return TableAttachment(thing)
    elif isinstance(thing, Figure):
        return ChartAttachment(thing)

    return None
