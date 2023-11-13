# imports
from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.attachments import (
    DatabaseAttachment,
    TableAttachment,
    ChartAttachment,
    TextAttachment,
    WebpageAttachment,
)
from ibis_birdbrain.ml.functions import generate_database_description


# tasks
def summarize_doc():
    """Not implemented."""
    ...


def summarize_web():
    """Not implemented."""
    ...


def summarize_database(db: DatabaseAttachment) -> TextAttachment:
    """Summarize a database."""
    tables = db.open().list_tables(database=db.data_base)

    a = TextAttachment(
        "\n".join(tables),
        name=f"{db.name} summary",
    )
    a.description = generate_database_description(a)

    return a


def summarize_table(m: Message) -> Message:
    """Not implemented"""
    ...
