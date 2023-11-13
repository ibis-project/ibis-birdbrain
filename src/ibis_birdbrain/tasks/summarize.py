# imports
from ibis_birdbrain.messages import Messages, Message, Email


# tasks
def summarize(m: Message) -> Messages:
    """Summarizes messages and attachments (including data).

    Choose this task to get a summary of items in the context."""
    system_messages = Messages()
    system_messages.append(
        Email(
            subject="Summarizing messages and attachments",
            body="Ibis Birdbrain is summarizing messages and attachments.",
        )
    )
    return system_messages


def summarize_doc(m: Message) -> Message:
    """Not implemented."""
    ...


def summarize_web(m: Message) -> Message:
    """Not implemented."""
    ...


def summarize_database(m: Message) -> Message:
    """Not implemented."""
    ...


def summarize_table(m: Message) -> Message:
    """Not implemented"""
    ...
