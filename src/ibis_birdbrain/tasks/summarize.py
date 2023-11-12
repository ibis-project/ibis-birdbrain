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
def summarize_docs():
    """Not implemented."""
    ...


def summarize_web():
    """Not implemented."""
    ...


def summarize_databases(m: Message) -> Message:
    """Summarize databases."""
    instructions = m.body
    response = Email(
        to_address=m.from_address, from_address=m.to_address, subject=f"re: {m.subject}"
    )

    for attachment in m.attachments:
        if isinstance(attachment, DatabaseAttachment):
            db_summary = summarize_database(attachment)
            response.attachments.append(db_summary)

    response.body = "Here is a summary of the databases."

    return response


def summarize_database(db: DatabaseAttachment) -> TextAttachment:
    """Summarize a database."""
    tables = db.open().list_tables(database=db.data_base)

    a = TextAttachment(
        "\n".join(tables),
        name=f"{db.name} summary",
    )
    a.description = generate_database_description(a)

    return a


def summarize_tables(m: Message) -> Message:
    """Not implemented"""
    ...
