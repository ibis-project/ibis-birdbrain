# imports
from ibis_birdbrain.messages import Messages, Message, Email


# tasks
def code(m: Message) -> Messages:
    """Writes code for a user.

    Choose this task to write code (SQL or Python/Ibis) for a user."""
    system_messages = Messages()
    system_messages.append(
        Email(
            subject="Writing code",
            body="Ibis Birdbrain is writing code.",
        )
    )
    return system_messages
