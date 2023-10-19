# imports
from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.attachments import (
    DatabaseAttachment,
    TableAttachment,
    ChartAttachment,
)


# tasks
def summarize_database(m: Message) -> Message:
    """Summarize the database."""
    instructions = m.body
    response = Message(
        to_address=m.from_address, from_address=m.to_address, subject=f"re: {m.subject}"
    )

    for attachment in m.attachments:
        if isinstance(attachment, DatabaseAttachment):
            table_summaries = Messages()
            for table in attachment.tables:
                table_summaries.append(summarize_table(table))

    return response


def summarize_table(m: Message) -> Message:
    """Summarize a table."""
    instructions = m.body
    response = Message(
        to_address=m.from_address, from_address=m.to_address, subject=f"re: {m.subject}"
    )

    return Message(body="Summarizing a table...")


def visualize_table(m: Message) -> Message:
    """Visualize a table."""
    instructions = m.body
    response = Message(
        to_address=m.from_address, from_address=m.to_address, subject=f"re: {m.subject}"
    )

    return Message(body="Visualizing a table...")
